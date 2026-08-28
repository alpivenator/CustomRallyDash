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
        # Acceleration & upshifting phase (0s - 14s)
        # 6 gears over 14 seconds
        gear_idx = min(6, int(cycle / 2.33) + 1)
        gear_t = (cycle % 2.33) / 2.33
        # RPM builds up, drops on shift
        rpm = 3000.0 + (gear_t**0.8) * (max_rpm - 2600.0)
        speed_kmh = (gear_idx - 1) * 28.0 + gear_t * 32.0
        throttle = 1.0 if gear_t < 0.9 else 0.85
        brake = 0.0
        gear_str = str(gear_idx)
    elif cycle < 17.5:
        # Hard braking & downshift hairpin corner (14s - 17.5s)
        brake_t = (cycle - 14.0) / 3.5
        speed_kmh = max(25.0, 170.0 - (brake_t * 145.0))
        gear_idx = max(2, 6 - int(brake_t * 4))
        rpm = 5500.0 - (brake_t * 2500.0) + (math.sin(cycle * 15.0) * 400.0)
        throttle = 0.0
        brake = max(0.0, min(1.0, 1.0 - (brake_t * 0.4)))
        gear_str = str(gear_idx)
    else:
        # Corner exit acceleration (17.5s - 20s)
        exit_t = (cycle - 17.5) / 2.5
        speed_kmh = 25.0 + (exit_t * 40.0)
        gear_idx = 2
        rpm = 3200.0 + (exit_t * 3800.0)
        throttle = min(1.0, exit_t * 1.2)
        brake = 0.0
        gear_str = "2"

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
