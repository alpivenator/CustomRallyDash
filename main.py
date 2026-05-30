# main.py
# DiRT Rally 2.0 — Unified Entry Point
#
# Launches either the digital or analog dashboard based on the DASH_STYLE
# setting in config.py, eliminating the need to run the .py files directly.

import config


def main() -> None:
    if config.DASH_STYLE == "analog":
        from analogdash import run
    else:
        from digital_dash import run
    run()


if __name__ == "__main__":
    main()
