# main.py
# DiRT Rally 2.0 — Unified Entry Point
#
# Launches either the digital or analog dashboard based on the DASH_STYLE
# setting in config.py. Supports --mock flag for standalone preview.

import sys
import threading

import config


def main() -> None:
    if "--mock" in sys.argv:
        from tools.mock_telemetry import run_mock_server

        mock_thread = threading.Thread(
            target=run_mock_server,
            kwargs={"ip": "127.0.0.1", "port": config.LISTEN_PORT},
            daemon=True,
        )
        mock_thread.start()

    if config.DASH_STYLE == "analog":
        from dashboards.analog_dash import run
    else:
        from dashboards.digital_dash import run
    run()


if __name__ == "__main__":
    main()
