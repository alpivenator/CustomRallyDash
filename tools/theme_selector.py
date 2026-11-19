"""Interactive Theme Selector for DiRT Rally 2.0 Telemetry Dashboard."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Callable

# Add project root to sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dashboards.themes import THEMES  # noqa: E402
from tools.cli_ui import ChoiceItem, CliUI, Text, UserCancelled  # noqa: E402
from tools.setup_wizard import make_backup  # noqa: E402

SETTINGS_PATH = _ROOT / "settings.py"
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], Any]


def _theme_swatch(colors: dict[str, Any]) -> Any:
    """Build a compact 3-block colour preview for Rich tables."""
    if Text is None:
        return "#"
    bg = colors["COLOR_BG"][:3]
    accent = colors["COLOR_RPM_NORMAL"][:3]
    warn = colors["COLOR_RPM_WARNING"][:3]
    swatch = Text()
    swatch.append("  ", style=f"on rgb({bg[0]},{bg[1]},{bg[2]})")
    swatch.append(" ")
    swatch.append("■", style=f"rgb({accent[0]},{accent[1]},{accent[2]})")
    swatch.append(" ")
    swatch.append("■", style=f"rgb({warn[0]},{warn[1]},{warn[2]})")
    return swatch


def select_language(
    input_func: InputFunction = input,
    output_func: OutputFunction = print,
    ui: CliUI | None = None,
) -> str:
    """Prompt user for UI language (en or tr)."""
    active_ui = ui or CliUI(input_fn=input_func, output_fn=output_func)
    choices = [
        ChoiceItem("en", "English", ("1", "english", "ingilizce")),
        ChoiceItem("tr", "Türkçe", ("2", "turkish", "türkçe", "turkce")),
    ]
    return active_ui.ask_select(
        "Select language / Dil seçin",
        choices=choices,
        default="en",
        invalid_message="Invalid choice. Please enter 'en' or 'tr'.",
        fallback_prompt="Select language / Dil seçin [en/tr] (en): ",
    )


def backup_settings_file(
    settings_path: Path = SETTINGS_PATH,
    output_func: OutputFunction = print,
    lang: str = "en",
) -> Path:
    """Create a timestamped backup of settings.py."""
    backup_path = make_backup(settings_path)
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
            content += f"\n{replacement}"

    settings_path.write_text(content, encoding="utf-8")
    return True


def _theme_text(theme: dict[str, Any], field: str, is_tr: bool) -> str:
    """Return localized theme metadata with an English fallback."""
    key = f"{field}_tr" if is_tr else field
    return str(theme.get(key) or theme[field])


def run_theme_selector(
    input_func: InputFunction = input,
    output_func: OutputFunction = print,
) -> None:
    """CLI loop for theme selection."""
    ui = CliUI(input_fn=input_func, output_fn=output_func)
    lang = "en"

    try:
        lang = select_language(input_func, output_func, ui=ui)
        is_tr = lang == "tr"
        ui.banner(
            (
                "CustomRallyDash - Tema Seçici"
                if is_tr
                else "CustomRallyDash - Theme Selector"
            ),
            (
                "settings.py güncellenmeden önce otomatik yedek alınır."
                if is_tr
                else "settings.py is backed up automatically before applying changes."
            ),
        )
        theme_keys = list(THEMES.keys())

        table_rows = []
        choice_items = []
        for idx, key in enumerate(theme_keys, start=1):
            item = THEMES[key]
            theme_name = _theme_text(item, "name", is_tr)
            theme_desc = _theme_text(item, "description", is_tr)
            table_rows.append(
                [
                    f"[{idx}] {theme_name}",
                    _theme_swatch(item["colors"]),
                    theme_desc,
                ]
            )
            choice_items.append(
                ChoiceItem(key, f"[{idx}] {theme_name}", aliases=(str(idx),))
            )

        cancel_label = "[0] İptal / Çıkış" if is_tr else "[0] Cancel / Exit"
        choice_items.append(
            ChoiceItem("__cancel__", cancel_label, aliases=("0", "cancel", "iptal"))
        )

        ui.table(
            title="Mevcut Temalar" if is_tr else "Available Themes",
            headers=[
                "Tema" if is_tr else "Theme",
                "Palet" if is_tr else "Palette",
                "Açıklama" if is_tr else "Description",
            ],
            rows=table_rows,
            col_styles=["bold", "", "dim"],
        )

        prompt_label = "Tema seçin" if is_tr else "Select theme"
        fallback_prompt = (
            f"Tema seçin [1-{len(theme_keys)}, 0] (1): "
            if is_tr
            else f"Select theme [1-{len(theme_keys)}, 0] (1): "
        )
        invalid_msg = (
            "Geçersiz seçim. Tekrar deneyin."
            if is_tr
            else "Invalid choice. Please try again."
        )

        selected_key = ui.ask_select(
            prompt_label,
            choices=choice_items,
            default=theme_keys[0],
            invalid_message=invalid_msg,
            fallback_prompt=fallback_prompt,
        )

        if selected_key == "__cancel__":
            ui.status("warn", "İptal edildi." if is_tr else "Cancelled.")
            return

        selected_theme = THEMES[selected_key]
        ui.blank()
        success = apply_theme_to_settings(
            selected_key,
            SETTINGS_PATH,
            lambda msg: ui.status("info", msg),
            lang,
        )
        if success:
            t_name = _theme_text(selected_theme, "name", is_tr)
            applied_msg = (
                f"'{t_name}' teması settings.py dosyasına uygulandı."
                if is_tr
                else f"'{t_name}' theme applied to settings.py."
            )
            preview_cmd = (
                "run_mock.bat  (python main.py --mock)"
                if sys.platform == "win32"
                else ".venv/bin/python main.py --mock"
            )
            ui.status("ok", applied_msg)
            ui.command_hint(
                "Canlı önizleme:" if is_tr else "Live preview:",
                preview_cmd,
            )
    except UserCancelled:
        ui.status("warn", "İptal edildi." if lang == "tr" else "Cancelled.")


if __name__ == "__main__":
    run_theme_selector()
