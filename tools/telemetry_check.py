"""Check whether DiRT Rally 2.0 telemetry reaches the configured UDP port."""

from __future__ import annotations

import errno
import socket
import sys
import time
from pathlib import Path
from typing import Any, Callable

# Ensure project root is in sys.path when executed directly
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import config  # noqa: E402
from tools.cli_ui import CliUI  # noqa: E402

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
    ui = CliUI(output_fn=output_fn)
    wait_timeout = min(max(timeout, 0.0), DEFAULT_TIMEOUT)
    ui.header_line(
        "CustomRallyDash - UDP Telemetry Check",
        f"{listen_ip}:{listen_port} | {EXPECTED_PACKET_SIZE} bytes | {wait_timeout:.0f}s",
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        try:
            sock.bind((listen_ip, listen_port))
        except OSError as error:
            if error.errno in {errno.EADDRINUSE, 10048}:
                ui.status(
                    "err",
                    f"UDP port {listen_port} is already in use.",
                    "ensure the dashboard is closed",
                )
            else:
                ui.status(
                    "err",
                    f"Could not bind to UDP {listen_ip}:{listen_port}: {error}",
                )
            return 1

        received: tuple[tuple[str, int], int] | None = None
        recv_error: OSError | None = None
        deadline = time.monotonic() + wait_timeout

        with ui.wait_status(
            f"Listening on {listen_ip}:{listen_port} for a "
            f"{EXPECTED_PACKET_SIZE}-byte packet..."
        ):
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
                    recv_error = error
                    break

                if len(packet) == EXPECTED_PACKET_SIZE:
                    received = (source, len(packet))
                    break

        if recv_error is not None:
            ui.status("err", f"Error reading UDP telemetry: {recv_error}")
            return 1

        if received is not None:
            source, packet_len = received
            ui.status(
                "ok",
                f"Telemetry packet received from {source[0]}:{source[1]}",
                f"{packet_len} bytes",
            )
            return 0

        ui.status(
            "err",
            f"No {EXPECTED_PACKET_SIZE}-byte telemetry packet received "
            f"within {wait_timeout:.0f} seconds.",
        )
        ui.bullet("Check firewall rules and hardware_settings_config.xml IP/port values.")
        ui.bullet("Ensure DiRT Rally 2.0 is running and actively in a stage.")
        return 1
    finally:
        sock.close()


if __name__ == "__main__":
    raise SystemExit(check_telemetry())
