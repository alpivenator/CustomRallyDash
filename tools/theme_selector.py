"""Interactive Theme Selector for DiRT Rally 2.0 Telemetry Dashboard."""

from __future__ import annotations

import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

# Add project root to sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dashboards.themes import THEMES  # noqa: E402

SETTINGS_PATH = _ROOT / "settings.py"
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], Any]


def select_language(
    input_func: InputFunction = input,
    output_func: OutputFunction = print,
) -> str:
    """Prompt user for UI language (en or tr)."""
    while True:
        choice = input_func("Select language / Dil seçin [en/tr] (en): ").strip().lower()
        if not choice or choice == "en":
            return "en"
        if choice == "tr":
            return "tr"
        output_func("Invalid choice. Please enter 'en' or 'tr'.")


def backup_settings_file(
    settings_path: Path = SETTINGS_PATH,
    output_func: OutputFunction = print,
    lang: str = "en",
) -> Path:
    """Create a timestamped backup of settings.py."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = settings_path.with_name(f"settings.py.bak.{timestamp}")
    shutil.copy2(settings_path, backup_path)
    if lang == "tr":
        output_func(f"Yedek oluşturuldu: {backup_path.name}")
    else:
        output_func(f"Backup created: {backup_path.name}")
    return backup_path


def apply_theme_to_settings(
    theme_key: str,
    settings_path: Path = SETTINGS_PATH,
    output_func: OutputFunction = print,
    lang: str = "en",
) -> bool:
    """Apply chosen theme colour definitions into settings.py safely."""
    if theme_key not in THEMES:
        return False

    theme = THEMES[theme_key]
    colors = theme["colors"]

    try:
        content = settings_path.read_text(encoding="utf-8")
    except OSError as err:
        output_func(f"Error reading {settings_path.name}: {err}")
        return False

    backup_settings_file(settings_path, output_func, lang)

    # Update each COLOR_* constant in settings.py
    for color_name, color_tuple in colors.items():
        pattern = rf"^{color_name}\s*=\s*.*$"
        replacement = f"{color_name} = {color_tuple}"
        content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        if count == 0:
            # If not found, append before font sizes
            content += f"\n{replacement}"

    settings_path.write_text(content, encoding="utf-8")
    return True


def run_theme_selector(
    input_func: InputFunction = input,
    output_func: OutputFunction = print,
) -> None:
    """CLI loop for theme selection."""
    output_func("\n" + "=" * 60)
    output_func(" DiRT Rally 2.0 Dashboard — Theme Selector")
    output_func("=" * 60 + "\n")

    lang = select_language(input_func, output_func)

    theme_keys = list(THEMES.keys())

    output_func("\n" + ("Mevcut Temalar:" if lang == "tr" else "Available Themes:"))
    for idx, key in enumerate(theme_keys, start=1):
        item = THEMES[key]
        output_func(f" [{idx}] {item['name']}")
        output_func(f"     -> {item['description']}")

    output_func(f" [0] {'İptal / Çıkış' if lang == 'tr' else 'Cancel / Exit'}\n")

    while True:
        prompt_text = (
            f"Tema seçin [1-{len(theme_keys)}] (1): "
            if lang == "tr"
            else f"Select theme [1-{len(theme_keys)}] (1): "
        )
        choice = input_func(prompt_text).strip()
        if not choice:
            choice = "1"

        if choice == "0":
            output_func("İptal edildi." if lang == "tr" else "Cancelled.")
            return

        if choice.isdigit() and 1 <= int(choice) <= len(theme_keys):
            selected_key = theme_keys[int(choice) - 1]
            selected_theme = THEMES[selected_key]
            success = apply_theme_to_settings(
                selected_key, SETTINGS_PATH, output_func, lang
            )
            if success:
                msg = (
                    f"\n[✓] '{selected_theme['name']}' teması settings.py dosyasına başarıyla uygulandı!"
                    if lang == "tr"
                    else f"\n[✓] '{selected_theme['name']}' theme successfully applied to settings.py!"
                )
                output_func(msg)
                output_func(
                    "Canlı önizlemek için: python main.py --mock"
                    if lang == "tr"
                    else "To preview live: python main.py --mock"
                )
            break
        output_func(
            "Geçersiz seçim. Tekrar deneyin."
            if lang == "tr"
            else "Invalid choice. Please try again."
        )


if __name__ == "__main__":
    run_theme_selector()
