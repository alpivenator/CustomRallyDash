# tools/mock_telemetry.py
# DiRT Rally 2.0 — Mock Telemetry Packet Generator
#
# Broadcasts synthetic 264-byte Extradata=3 UDP packets at 60 Hz to enable
# live dashboard preview and theme testing without running the actual game.

from __future__ import annotations

import math
import socket
import struct
import sys
import time
from pathlib import Path

# Add project root to sys.path if executed directly
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import config  # noqa: E402


def generate_packet(
    elapsed_time: float, max_rpm: float = 8000.0
) -> tuple[bytes, float, int, float, str]:
    """Generate a single 264-byte Extradata=3 packet for a synthetic rally stage loop."""
    # 20-second stage loop
    cycle = elapsed_time % 20.0

    if cycle < 14.0:
        # Acceleration & sequential upshifts (0s - 14s: 1st -> 6th gear, ~2.33s per gear)
        gear_duration = 14.0 / 6.0
        gear_idx = min(6, int(cycle / gear_duration) + 1)
        gear_t = (cycle % gear_duration) / gear_duration
        
        # 1st gear launches from 2500 RPM; 2nd-6th drop to close-ratio ~5800 RPM on upshift
        min_gear_rpm = 2500.0 if gear_idx == 1 else 5800.0
        rpm = min_gear_rpm + (gear_t**0.85) * (max_rpm - min_gear_rpm)
        speed_kmh = (gear_idx - 1) * 28.0 + (gear_t * 32.0)
        throttle = 1.0 if gear_t < 0.92 else 0.85
        brake = 0.0
        gear_str = str(gear_idx)
    else:
        # Braking & sequential downshifts with auto-blip / rev-matching (14s - 20s)
        brake_elapsed = cycle - 14.0  # 0.0s to 6.0s
        downshift_step = min(5, int(brake_elapsed))  # 0 (6th) -> 1 (5th) -> 2 (4th) -> 3 (3rd) -> 4 (2nd) -> 5 (1st)
        step_t = brake_elapsed % 1.0  # 0.0 to 1.0 within each 1-second gear window
        brake_progress = brake_elapsed / 6.0
        
        gear_idx = max(1, 6 - downshift_step)
        speed_kmh = max(0.0, 175.0 * ((1.0 - brake_progress)**1.1))
        
        # Auto-blip throttle pulse on downshifts (first 150ms of steps 1-4)
        if downshift_step > 0 and step_t < 0.15:
            blip_phase = step_t / 0.15
            throttle = 0.5 * math.sin(blip_phase * math.pi)
            rpm = 6800.0 - (blip_phase * 400.0)
        elif downshift_step == 0:
            # Initial braking in 6th gear before first downshift
            throttle = 0.0
            rpm = max(5200.0, 8000.0 - (step_t * 2800.0))
        elif downshift_step == 5:
            # Final deceleration to full stop and idle in 1st gear (19s - 20s)
            throttle = 0.0
            decay_t = step_t
            rpm = max(1200.0, 4200.0 * (1.0 - decay_t) + 1200.0 * decay_t)
        else:
            # Engine braking decay after blip (~6400 RPM -> ~4200 RPM)
            throttle = 0.0
            decay_t = (step_t - 0.15) / 0.85
            rpm = max(4200.0, 6400.0 - (decay_t * 2200.0))
            
        # Brake pedal pressure with release as vehicle comes to halt
        if brake_elapsed < 4.8:
            brake = 0.9
        else:
            brake = max(0.0, 0.9 * (1.0 - ((brake_elapsed - 4.8) / 1.2)))
            
        gear_str = str(gear_idx)

    car_speed_ms = speed_kmh / 3.6
    # Add slight wheel slip during hard acceleration / braking
    slip_factor = 1.08 if throttle > 0.8 else (0.92 if brake > 0.5 else 1.0)
    wheel_speed_ms = car_speed_ms * slip_factor

    # Pack 66 floats (264 bytes)
    # [7] = car_speed, [25-28] = wheel_speeds, [29] = throttle, [31] = brake,
    # [33] = gear, [37] = engine_rpm (unscaled), [63] = max_rpm (unscaled)
    fields = [0.0] * 66
    fields[7] = car_speed_ms
    fields[25] = wheel_speed_ms
    fields[26] = wheel_speed_ms
    fields[27] = wheel_speed_ms
    fields[28] = wheel_speed_ms
    fields[29] = throttle
    fields[31] = brake
    fields[33] = float(gear_idx)
    fields[37] = rpm / 10.0  # Listener multiplies by 10
    fields[63] = max_rpm / 10.0

    packet = struct.pack("66f", *fields)
    return packet, speed_kmh, int(rpm), throttle, gear_str


def run_mock_server(
    ip: str | None = None,
    port: int | None = None,
    duration: float | None = None,
) -> None:
    """Run the 60 Hz UDP mock broadcaster."""
    target_ip = ip or config.LISTEN_IP
    target_port = port or config.LISTEN_PORT

    # If configured as 0.0.0.0, send to localhost
    if target_ip == "0.0.0.0":  # nosec B104
        target_ip = "127.0.0.1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("=" * 60)
    print(" DiRT Rally 2.0 — Mock Telemetry Broadcaster")
    print("=" * 60)
    print(f" Target: {target_ip}:{target_port} @ 60 Hz")
    print(" Simulating: Acceleration -> Upshifts -> Heavy Braking -> Hairpin Exit")
    print(" Press Ctrl+C to stop broadcasting.\n")

    start_time = time.time()
    frame_interval = 1.0 / 60.0
    packet_count = 0

    try:
        while True:
            now = time.time()
            elapsed = now - start_time
            if duration is not None and elapsed >= duration:
                break

            packet, _speed, _rpm, _thr, _gear = generate_packet(elapsed)
            sock.sendto(packet, (target_ip, target_port))
            packet_count += 1

            if packet_count % 120 == 0:  # Every 2 seconds
                print(
                    f" [{elapsed:05.1f}s] Speed: {_speed:3.0f} km/h | "
                    f"RPM: {_rpm:4d} | Gear: {_gear} | Thr: {_thr:.1f}",
                    end="\r",
                    flush=True,
                )

            next_frame_time = start_time + (packet_count * frame_interval)
            sleep_duration = next_frame_time - time.time()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    except KeyboardInterrupt:
        print("\n\nMock broadcaster stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    run_mock_server()
