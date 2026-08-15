"""Check whether DiRT Rally 2.0 telemetry reaches the configured UDP port."""

from __future__ import annotations

import errno
import socket
import time
from typing import Any, Callable

import config

EXPECTED_PACKET_SIZE = 264
DEFAULT_TIMEOUT = 5.0
OutputFunction = Callable[[str], Any]


def check_telemetry(
    listen_ip: str = config.LISTEN_IP,
    listen_port: int = config.LISTEN_PORT,
    timeout: float = DEFAULT_TIMEOUT,
    output_fn: OutputFunction = print,
) -> int:
    """Wait for one valid telemetry packet and return a process exit code."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        try:
            sock.bind((listen_ip, listen_port))
        except OSError as error:
            if error.errno in {errno.EADDRINUSE, 10048}:
                output_fn(
                    f"UDP portu {listen_port} zaten kullanımda. "
                    "Dashboard kapalı olmalıdır."
                )
            else:
                output_fn(
                    f"UDP dinleme adresi açılamadı ({listen_ip}:{listen_port}): {error}"
                )
            return 1

        wait_timeout = min(max(timeout, 0.0), DEFAULT_TIMEOUT)
        deadline = time.monotonic() + wait_timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            sock.settimeout(remaining)
            try:
                packet, source = sock.recvfrom(65535)
            except socket.timeout:
                break
            except OSError as error:
                output_fn(f"UDP telemetri okunamadı: {error}")
                return 1

            if len(packet) == EXPECTED_PACKET_SIZE:
                output_fn(
                    f"Telemetri paketi alındı: {source[0]}:{source[1]} "
                    f"({len(packet)} byte)."
                )
                return 0

        output_fn(
            f"{wait_timeout:.0f} saniye içinde {EXPECTED_PACKET_SIZE} byte uzunluğunda "
            "telemetri paketi alınamadı."
        )
        output_fn(
            "Firewall ayarını, oyun XML'indeki IP/port değerlerini ve oyunun açık "
            "olduğunu kontrol edin."
        )
        return 1
    finally:
        sock.close()


if __name__ == "__main__":
    raise SystemExit(check_telemetry())
