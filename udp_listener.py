# udp_listener.py
# DiRT Rally 2.0 — Shared UDP Telemetry Listener
#
# Decodes 264-byte Extradata=3 packets broadcast by the game at 60 Hz.
# Returns parsed telemetry as a TelemetryData namedtuple.

import socket
import struct
from collections import namedtuple

TelemetryData = namedtuple(
    "TelemetryData",
    [
        "wheel_speed_kmh",
        "car_speed_kmh",
        "rpm",
        "max_rpm",
        "gear_str",
        "throttle",
        "brake",
    ],
    defaults=[0, 0, 0, 8000, "N", 0.0, 0.0],
)


class UDPListener:
    def __init__(self, ip: str = "0.0.0.0", port: int = 20777) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(0.01)
        self._data = TelemetryData()

    def receive(self) -> TelemetryData:
        last_packet: bytes | None = None
        try:
            while True:
                raw, _addr = self.sock.recvfrom(1024)
                if len(raw) == 264:
                    last_packet = raw
        except socket.timeout:
            pass

        if last_packet is not None:
            self._data = self._parse(last_packet)

        return self._data

    def close(self) -> None:
        self.sock.close()

    def _parse(self, packet: bytes) -> TelemetryData:
        f = struct.unpack("66f", packet)

        # Field index reference (Extradata=3 format):
        # [7]    = car_speed (m/s)
        # [25-28]= wheel_speeds (m/s)
        # [29]   = throttle (0-1)
        # [31]   = brake (0-1)
        # [33]   = gear (-1=Rev, 0=Neutral, 1-6=Forward)
        # [37]   = engine_rpm
        # [63]   = max_rpm

        speed_ms = (f[25] + f[26] + f[27] + f[28]) / 4.0
        wheel_speed_kmh = int(speed_ms * 3.6)
        car_speed_kmh = int(f[7] * 3.6)
        rpm = int(f[37] * 10)

        read_max = int(f[63] * 10)
        max_rpm = read_max if read_max > 0 else 8000

        gear = int(f[33])
        if gear == 0:
            gear_str = "N"
        elif gear == -1:
            gear_str = "R"
        else:
            gear_str = str(gear)

        throttle = max(0.0, min(1.0, f[29]))
        brake = max(0.0, min(1.0, f[31]))

        return TelemetryData(
            wheel_speed_kmh=wheel_speed_kmh,
            car_speed_kmh=car_speed_kmh,
            rpm=rpm,
            max_rpm=max_rpm,
            gear_str=gear_str,
            throttle=throttle,
            brake=brake,
        )
