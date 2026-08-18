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
                    f"UDP port {listen_port} is already in use. "
                    "Ensure the dashboard is closed."
                )
            else:
                output_fn(f"Could not bind to UDP {listen_ip}:{listen_port}: {error}")
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
                output_fn(f"Error reading UDP telemetry: {error}")
                return 1

            if len(packet) == EXPECTED_PACKET_SIZE:
                output_fn(
                    f"Telemetry packet received from {source[0]}:{source[1]} "
                    f"({len(packet)} bytes)."
                )
                return 0

        output_fn(
            f"No {EXPECTED_PACKET_SIZE}-byte telemetry packet received "
            f"within {wait_timeout:.0f} seconds."
        )
        output_fn(
            "Check your firewall settings, game XML IP/port values, and ensure "
            "DiRT Rally 2.0 is running and in a stage."
        )
        return 1
    finally:
        sock.close()


if __name__ == "__main__":
    raise SystemExit(check_telemetry())
