"""Setup and diagnostic utilities."""

from .setup_wizard import run_setup
from .telemetry_check import check_telemetry

__all__ = [
    "run_setup",
    "check_telemetry",
]
