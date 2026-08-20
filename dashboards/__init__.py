"""Pygame dashboard renderers for DiRT Rally 2.0."""

from .analog_dash import run as run_analog_dash
from .digital_dash import run as run_digital_dash

__all__ = [
    "run_digital_dash",
    "run_analog_dash",
]
