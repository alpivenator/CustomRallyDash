"""Interactive first-run setup for DiRT Rally 2.0 Telemetry Dashboard."""

from __future__ import annotations

import ast
import importlib.util
import ipaddress
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any

# Ensure project root is in sys.path when executed directly
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from tools.cli_ui import (  # noqa: E402
    ChoiceItem,
    CliUI,
    InputFunction,
    OutputFunction,
    Text,
    UserCancelled,
)

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 20777
DEFAULT_DASH_STYLE = "digital"
DEFAULT_ENABLE_OVERLAY = True
DEFAULT_ENABLE_LEDS = False
CONFIG_KEYS = ("LISTEN_IP", "DASH_STYLE", "ENABLE_OVERLAY", "ENABLE_LEDS")
CONFIG_DEFAULTS: dict[str, object] = {
    "LISTEN_IP": DEFAULT_IP,
    "DASH_STYLE": DEFAULT_DASH_STYLE,
    "ENABLE_OVERLAY": DEFAULT_ENABLE_OVERLAY,
    "ENABLE_LEDS": DEFAULT_ENABLE_LEDS,
}
GAME_CONFIG_RELATIVE_PATH = Path(
    "Documents",
    "My Games",
    "DiRT Rally 2.0",
    "hardwaresettings",
    "hardware_settings_config.xml",
)

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "lang_prompt": "Select language / Dil seçin [en/tr] (en): ",
        "lang_invalid": "Invalid choice. Please enter 'en' or 'tr'.",
        "banner_title": "CustomRallyDash - Initial Setup",
        "banner_note": (
            "DiRT Rally 2.0 must be closed. Configuration files will be backed up "
            "before updating."
        ),
        "step_network": "Network Configuration",
        "step_style": "Dashboard Style",
        "step_overlay": "Windows Overlay",
        "step_leds": "Raspberry Pi GPIO LEDs",
        "step_confirm": "Review & Confirm",
        "prompt_ip": "Dashboard computer IPv4 address",
        "invalid_ip": "Invalid IPv4 address. Example: 127.0.0.1 or 192.168.1.25",
        "prompt_dash_style": "Dashboard style",
        "style_digital": "digital  (Modern gear + RPM bar)",
        "style_analog": "analog   (Classic needle tachometer)",
        "invalid_choice": "Invalid choice. Please choose one of: {choices}",
        "prompt_overlay": "Enable Windows overlay?",
        "overlay_windows_only": "Windows only (skipped on this OS)",
        "prompt_leds": "Enable Raspberry Pi GPIO shift-light LEDs?",
        "invalid_yes_no": "Invalid answer. Please enter {yes} or {no}.",
        "config_read_error": "Could not read config.py: {error}",
        "game_xml_invalid": "Game XML could not be verified: {error}",
        "summary_title": "Selected Settings",
        "table_setting": "Setting",
        "table_value": "Selected Value",
        "label_ip": "Dashboard IPv4",
        "label_style": "Dashboard style",
        "label_overlay": "Windows overlay",
        "label_leds": "Raspberry Pi LEDs",
        "label_port": "UDP port",
        "label_xml": "Game XML",
        "summary_xml_missing": "not found automatically (manual steps below)",
        "prompt_confirm": "Proceed with these settings?",
        "setup_cancelled": "Setup cancelled. No files were modified.",
        "config_update_error": "Failed to update config.py: {error}",
        "game_xml_update_error": "Failed to update game XML: {error}",
        "config_backup_info": "config.py backup: {path}",
        "game_xml_not_found_header": (
            "DiRT Rally 2.0 XML file could not be found automatically."
        ),
        "game_xml_expected_location": (
            "Expected location: Documents\\My Games\\DiRT Rally 2.0\\"
            "hardwaresettings\\hardware_settings_config.xml"
        ),
        "game_xml_manual_prefix": "Manually add this UDP element:",
        "game_xml_updated": "Game XML updated.",
        "config_updated": "config.py updated.",
        "backup_detail": "backup: {path}",
        "leds_missing_gpiozero": (
            "ENABLE_LEDS is True, but 'gpiozero' is not installed in this environment."
        ),
        "leds_install_hint": "Install it with:",
        "leds_install_cmd": "pip install -r requirements-pi.txt (or ./install.sh --pi)",
        "completion_banner": "Setup Completed Successfully!",
        "next_steps_header": "Next steps:",
        "step_hint_telemetry": "1. Telemetry check (stage on, dash off):",
        "step_hint_mock": "2. Mock telemetry preview:",
        "step_hint_theme": "3. Theme selector:",
        "step_hint_launch": "4. Launch dashboard:",
        "cmd_telemetry_win": (
            "check_telemetry.bat  (.venv\\Scripts\\python.exe tools\\telemetry_check.py)"
        ),
        "cmd_mock_win": "run_mock.bat  (python main.py --mock)",
        "cmd_theme_win": (
            "select_theme.bat  (.venv\\Scripts\\python.exe tools\\theme_selector.py)"
        ),
        "cmd_launch_win": "run_dash.bat",
        "cmd_telemetry_unix": ".venv/bin/python tools/telemetry_check.py",
        "cmd_mock_unix": ".venv/bin/python main.py --mock",
        "cmd_theme_unix": ".venv/bin/python tools/theme_selector.py",
        "cmd_launch_unix": ".venv/bin/python main.py",
        "yes_label": "Yes",
        "no_label": "No",
        "yes_short": "Y",
        "no_short": "N",
    },
    "tr": {
        "lang_prompt": "Select language / Dil seçin [en/tr] (en): ",
        "lang_invalid": "Geçersiz seçim. Lütfen 'en' veya 'tr' girin.",
        "banner_title": "CustomRallyDash - İlk Kurulum",
        "banner_note": (
            "DiRT Rally 2.0 kapalı olmalıdır; yapılandırma dosyaları onayınızdan sonra "
            "yedeklenerek güncellenir."
        ),
        "step_network": "Ağ Yapılandırması",
        "step_style": "Dashboard Türü",
        "step_overlay": "Windows Overlay",
        "step_leds": "Raspberry Pi GPIO LED",
        "step_confirm": "Özet ve Onay",
        "prompt_ip": "Dashboard bilgisayarının IPv4 adresi",
        "invalid_ip": "Geçersiz IPv4 adresi. Örnek: 127.0.0.1 veya 192.168.1.25",
        "prompt_dash_style": "Dashboard türü",
        "style_digital": "digital  (Modern vites + devir şeridi)",
        "style_analog": "analog   (Klasik ibreli takometre)",
        "invalid_choice": "Geçersiz seçim. Şunlardan birini kullanın: {choices}",
        "prompt_overlay": "Windows overlay etkinleştirilsin mi?",
        "overlay_windows_only": "Yalnızca Windows'ta desteklenir (atlandı)",
        "prompt_leds": "Raspberry Pi GPIO vites ışıkları (LED) etkinleştirilsin mi?",
        "invalid_yes_no": "Geçersiz cevap. Lütfen {yes} veya {no} girin.",
        "config_read_error": "Mevcut config.py okunamadı: {error}",
        "game_xml_invalid": "Oyun XML'i doğrulanamadı: {error}",
        "summary_title": "Seçilen Ayarlar",
        "table_setting": "Ayar",
        "table_value": "Seçilen Değer",
        "label_ip": "Dashboard IPv4",
        "label_style": "Dashboard türü",
        "label_overlay": "Windows overlay",
        "label_leds": "Raspberry Pi LED'leri",
        "label_port": "UDP portu",
        "label_xml": "Oyun XML'i",
        "summary_xml_missing": "otomatik bulunamadı (manuel adımlar aşağıda)",
        "prompt_confirm": "Bu ayarlarla devam edilsin mi?",
        "setup_cancelled": "Kurulum iptal edildi. Dosyalarda değişiklik yapılmadı.",
        "config_update_error": "config.py güncellenemedi: {error}",
        "game_xml_update_error": "Oyun XML'i güncellenemedi: {error}",
        "config_backup_info": "config.py yedeği: {path}",
        "game_xml_not_found_header": "DiRT Rally 2.0 XML dosyası otomatik bulunamadı.",
        "game_xml_expected_location": (
            "Beklenen konum: Documents\\My Games\\DiRT Rally 2.0\\"
            "hardwaresettings\\hardware_settings_config.xml"
        ),
        "game_xml_manual_prefix": "Manuel olarak şu UDP satırını ekleyin:",
        "game_xml_updated": "Oyun XML'i güncellendi.",
        "config_updated": "config.py güncellendi.",
        "backup_detail": "yedek: {path}",
        "leds_missing_gpiozero": (
            "ENABLE_LEDS etkin ancak bu ortamda 'gpiozero' kurulu değil."
        ),
        "leds_install_hint": "Kurmak için:",
        "leds_install_cmd": "pip install -r requirements-pi.txt (veya ./install.sh --pi)",
        "completion_banner": "Kurulum Başarıyla Tamamlandı!",
        "next_steps_header": "Sonraki adımlar:",
        "step_hint_telemetry": "1. Telemetri testi (etap açık, dash kapalı):",
        "step_hint_mock": "2. Mock telemetri önizleme:",
        "step_hint_theme": "3. Tema seçici:",
        "step_hint_launch": "4. Göstergeyi başlat:",
        "cmd_telemetry_win": (
            "check_telemetry.bat  (.venv\\Scripts\\python.exe tools\\telemetry_check.py)"
        ),
        "cmd_mock_win": "run_mock.bat  (python main.py --mock)",
        "cmd_theme_win": (
            "select_theme.bat  (.venv\\Scripts\\python.exe tools\\theme_selector.py)"
        ),
        "cmd_launch_win": "run_dash.bat",
        "cmd_telemetry_unix": ".venv/bin/python tools/telemetry_check.py",
        "cmd_mock_unix": ".venv/bin/python main.py --mock",
        "cmd_theme_unix": ".venv/bin/python tools/theme_selector.py",
        "cmd_launch_unix": ".venv/bin/python main.py",
        "yes_label": "Evet",
        "no_label": "Hayır",
        "yes_short": "E",
        "no_short": "H",
    },
}


class SetupError(Exception):
    """Raised when a setup file cannot be safely updated."""


def validate_ipv4(value: str) -> str:
    """Return a normalized IPv4 address or raise ValueError."""
    address = ipaddress.ip_address(value.strip())
    if address.version != 4:
        raise ValueError("Only IPv4 addresses are supported.")
    return str(address)


def make_backup(path: Path) -> Path:
    """Create a timestamped backup beside path and return its location."""
    if not path.is_file():
        raise SetupError(f"File not found: {path}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.bak-{stamp}")
    counter = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.bak-{stamp}-{counter}")
        counter += 1
    shutil.copy2(path, backup)
    return backup


def _atomic_write(path: Path, content: str) -> None:
    """Replace a text file atomically within its existing directory."""
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        delete=False,
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)

    try:
        temporary_path.replace(path)
    except OSError:
        temporary_path.unlink(missing_ok=True)
        raise


def read_config_defaults(path: Path) -> dict[str, object]:
    """Read setup values from config.py without importing the project module."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as error:
        raise SetupError(f"Could not read config.py: {path}") from error

    values = CONFIG_DEFAULTS.copy()
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name) or target.id not in CONFIG_KEYS:
            continue
        try:
            values[target.id] = ast.literal_eval(statement.value)
        except (ValueError, TypeError, SyntaxError) as error:
            raise SetupError(f"Invalid value for {target.id} in config.py.") from error

    listen_ip = values["LISTEN_IP"]
    if not isinstance(listen_ip, str):
        raise SetupError("LISTEN_IP in config.py must be an IPv4 address.")
    try:
        values["LISTEN_IP"] = validate_ipv4(listen_ip)
    except ValueError as error:
        raise SetupError(f"Invalid LISTEN_IP in config.py: {listen_ip}") from error

    dash_style = values["DASH_STYLE"]
    if dash_style not in {"digital", "analog"}:
        raise SetupError("DASH_STYLE in config.py must be digital or analog.")
    if not isinstance(values["ENABLE_OVERLAY"], bool):
        raise SetupError("ENABLE_OVERLAY in config.py must be True or False.")
    if not isinstance(values["ENABLE_LEDS"], bool):
        raise SetupError("ENABLE_LEDS in config.py must be True or False.")

    return values


def _config_has_key(path: Path, key: str) -> bool:
    """Return True if path contains a top-level assignment for key."""
    content = path.read_text(encoding="utf-8")
    return bool(re.search(rf"^\s*{re.escape(key)}\s*=", content, re.MULTILINE))


def update_config_file(path: Path, updates: dict[str, object]) -> Path:
    """Back up config.py and update existing top-level assignment lines."""
    content = path.read_text(encoding="utf-8")

    for key, value in updates.items():
        if key not in CONFIG_KEYS:
            raise SetupError(f"Unsupported config key: {key}")

        pattern = re.compile(rf"^(\s*{re.escape(key)}\s*=\s*).*$", re.MULTILINE)
        replacement_count = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal replacement_count
            replacement_count += 1
            if isinstance(value, str):
                current_value = match.group(0).split("=", 1)[1].strip()
                quote = '"' if current_value.startswith('"') else "'"
                serialized = f"{quote}{value}{quote}"
            else:
                serialized = repr(value)
            return f"{match.group(1)}{serialized}"

        content = pattern.sub(replace, content)
        if replacement_count != 1:
            raise SetupError(
                f"Expected one assignment for {key}, found {replacement_count}."
            )

    backup = make_backup(path)
    _atomic_write(path, content)
    return backup


def configure_game_xml(path: Path, ip: str, port: int = DEFAULT_PORT) -> Path:
    """Back up and update the game's motion-platform UDP configuration."""
    try:
        tree = ET.parse(path)  # noqa: S314 — Local game config XML
    except (ET.ParseError, OSError) as error:
        raise SetupError(f"Could not read game configuration: {path}") from error

    motion_platform = tree.getroot().find(".//motion_platform")
    if motion_platform is None:
        raise SetupError("The game XML does not contain a motion_platform section.")

    udp = motion_platform.find("udp")
    if udp is None:
        udp = ET.SubElement(motion_platform, "udp")

    udp.set("enabled", "true")
    udp.set("extradata", "3")
    udp.set("ip", validate_ipv4(ip))
    udp.set("port", str(port))
    if "delay" not in udp.attrib:
        udp.set("delay", "1")

    backup = make_backup(path)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)

    try:
        tree.write(temporary_path, encoding="utf-8", xml_declaration=True)
        temporary_path.replace(path)
    except OSError:
        temporary_path.unlink(missing_ok=True)
        raise

    return backup


def _validate_game_config(path: Path) -> None:
    """Validate the game XML before the user approves any file changes."""
    try:
        tree = ET.parse(path)  # noqa: S314 — Local game config XML
    except (ET.ParseError, OSError) as error:
        raise SetupError(f"Could not read game configuration: {path}") from error
    if tree.getroot().find(".//motion_platform") is None:
        raise SetupError("The game XML does not contain a motion_platform section.")


def find_game_config(home: Path | None = None) -> Path | None:
    """Find the standard game configuration under common Windows Documents paths."""
    home = home or Path.home()
    candidates = [home / GAME_CONFIG_RELATIVE_PATH]

    onedrive = home / "OneDrive" / GAME_CONFIG_RELATIVE_PATH
    if onedrive not in candidates:
        candidates.append(onedrive)

    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _ask_language(
    input_fn: InputFunction,
    output_fn: OutputFunction,
    ui: CliUI | None = None,
) -> str:
    """Ask user to select interface language, defaulting to English."""
    active_ui = ui or CliUI(input_fn=input_fn, output_fn=output_fn)
    choices = [
        ChoiceItem("en", "English", ("1", "english", "ingilizce")),
        ChoiceItem("tr", "Türkçe", ("2", "turkish", "türkçe", "turkce")),
    ]
    return active_ui.ask_select(
        "Select language / Dil seçin",
        choices=choices,
        default="en",
        invalid_message=MESSAGES["en"]["lang_invalid"],
        fallback_prompt=MESSAGES["en"]["lang_prompt"],
    )


def _ask_ip(
    ui: CliUI,
    default_ip: str = DEFAULT_IP,
    lang: str = "en",
) -> str:
    msg = MESSAGES[lang]
    while True:
        answer = ui.ask_text(msg["prompt_ip"], default=default_ip).strip()
        value = answer or default_ip
        try:
            return validate_ipv4(value)
        except ValueError:
            ui.status("err", msg["invalid_ip"])


def _ask_yes_no(
    ui: CliUI,
    prompt: str,
    default: bool,
    lang: str = "en",
) -> bool:
    msg = MESSAGES[lang]
    return ui.ask_yes_no(
        prompt,
        default=default,
        yes_label=msg["yes_label"],
        no_label=msg["no_label"],
        yes_short=msg["yes_short"],
        no_short=msg["no_short"],
        invalid_message=msg["invalid_yes_no"].format(
            yes=msg["yes_short"], no=msg["no_short"]
        ),
    )


def _print_summary(
    ui: CliUI,
    msg: dict[str, str],
    destination_ip: str,
    dash_style: str,
    enable_overlay: bool | None,
    enable_leds: bool | None,
    game_config: Path | None,
) -> None:
    """Render chosen configuration values as a clean horizontal-rule table."""
    overlay_val: Any = (
        (msg["yes_label"] if enable_overlay else msg["no_label"])
        if enable_overlay is not None
        else msg["overlay_windows_only"]
    )
    rows: list[tuple[str, Any]] = [
        (msg["label_ip"], destination_ip),
        (msg["label_style"], dash_style),
        (msg["label_overlay"], overlay_val),
    ]
    if enable_leds is not None:
        rows.append(
            (msg["label_leds"], msg["yes_label"] if enable_leds else msg["no_label"])
        )
    rows.append((msg["label_port"], str(DEFAULT_PORT)))

    xml_cell: Any
    if game_config is None:
        xml_cell = (
            Text(msg["summary_xml_missing"], style="yellow")
            if Text is not None
            else msg["summary_xml_missing"]
        )
    else:
        xml_cell = str(game_config)
    rows.append((msg["label_xml"], xml_cell))

    ui.table(
        title=msg["summary_title"],
        headers=[msg["table_setting"], msg["table_value"]],
        rows=rows,
        col_styles=["dim", "bold"],
    )


def _print_next_steps(ui: CliUI, msg: dict[str, str], is_windows: bool) -> None:
    """Print completion status and highlighted post-setup commands."""
    ui.blank()
    ui.status("ok", msg["completion_banner"])
    ui.blank()
    suffix = "win" if is_windows else "unix"
    ui.status("info", msg["next_steps_header"])
    for key in ("telemetry", "mock", "theme", "launch"):
        ui.command_hint(msg[f"step_hint_{key}"], msg[f"cmd_{key}_{suffix}"])


def run_setup(
    project_root: Path | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    lang: str | None = None,
    platform: str | None = None,
) -> int:
    """Run the interactive setup flow and return a process exit code."""
    project_root = project_root or Path(__file__).resolve().parent.parent
    config_path = project_root / "config.py"
    active_platform = platform if platform is not None else sys.platform
    is_windows = active_platform == "win32"
    ui = CliUI(input_fn=input_fn, output_fn=output_fn)

    try:
        if lang is None:
            selected_lang = _ask_language(input_fn, output_fn, ui=ui)
        else:
            selected_lang = "tr" if lang.lower().startswith("tr") else "en"

        msg = MESSAGES[selected_lang]
        ui.banner(msg["banner_title"], msg["banner_note"])

        try:
            current_config = read_config_defaults(config_path)
        except (OSError, SetupError) as error:
            ui.status("err", msg["config_read_error"].format(error=error))
            return 1

        has_leds_key = not is_windows and _config_has_key(config_path, "ENABLE_LEDS")
        has_platform_step = is_windows or has_leds_key
        total_steps = 4 if has_platform_step else 3

        ui.step(1, total_steps, msg["step_network"])
        destination_ip = _ask_ip(ui, str(current_config["LISTEN_IP"]), selected_lang)

        ui.step(2, total_steps, msg["step_style"])
        current_style = str(current_config["DASH_STYLE"])
        style_choices = [
            ChoiceItem("digital", msg["style_digital"]),
            ChoiceItem("analog", msg["style_analog"]),
        ]
        dash_style = ui.ask_select(
            msg["prompt_dash_style"],
            choices=style_choices,
            default=current_style,
            invalid_message=msg["invalid_choice"].format(choices="digital/analog"),
        )

        updates: dict[str, object] = {
            "LISTEN_IP": destination_ip,
            "DASH_STYLE": dash_style,
        }
        enable_overlay: bool | None = None
        enable_leds: bool | None = None

        if is_windows:
            ui.step(3, total_steps, msg["step_overlay"])
            enable_overlay = _ask_yes_no(
                ui,
                msg["prompt_overlay"],
                bool(current_config["ENABLE_OVERLAY"]),
                selected_lang,
            )
            updates["ENABLE_OVERLAY"] = enable_overlay
        elif has_leds_key:
            ui.step(3, total_steps, msg["step_leds"])
            enable_leds = _ask_yes_no(
                ui,
                msg["prompt_leds"],
                bool(current_config["ENABLE_LEDS"]),
                selected_lang,
            )
            updates["ENABLE_LEDS"] = enable_leds

        game_config = find_game_config()
        if game_config is not None:
            try:
                _validate_game_config(game_config)
            except SetupError as error:
                ui.status("err", msg["game_xml_invalid"].format(error=error))
                return 1

        ui.step(total_steps, total_steps, msg["step_confirm"])
        _print_summary(
            ui, msg, destination_ip, dash_style, enable_overlay, enable_leds, game_config
        )

        if not _ask_yes_no(ui, msg["prompt_confirm"], True, selected_lang):
            ui.status("warn", msg["setup_cancelled"])
            return 0
    except UserCancelled:
        cancel_msg = MESSAGES["en"]["setup_cancelled"]
        ui.status("warn", cancel_msg)
        return 0

    try:
        config_backup = update_config_file(config_path, updates)
    except (OSError, SetupError) as error:
        ui.status("err", msg["config_update_error"].format(error=error))
        return 1

    ui.blank()
    ui.status(
        "ok",
        msg["config_updated"],
        msg["backup_detail"].format(path=config_backup.name),
    )

    if game_config is None:
        ui.blank()
        ui.status("warn", msg["game_xml_not_found_header"])
        ui.bullet(msg["game_xml_expected_location"])
        ui.bullet(msg["game_xml_manual_prefix"])
        xml_snippet = (
            f'<udp enabled="true" extradata="3" '
            f'ip="{destination_ip}" port="{DEFAULT_PORT}" delay="1" />'
        )
        ui.command_hint("   ", xml_snippet)
    else:
        try:
            game_backup = configure_game_xml(game_config, destination_ip)
        except (OSError, SetupError) as error:
            ui.status("err", msg["game_xml_update_error"].format(error=error))
            ui.status("info", msg["config_backup_info"].format(path=config_backup))
            return 1
        ui.status(
            "ok",
            msg["game_xml_updated"],
            msg["backup_detail"].format(path=game_backup.name),
        )

    _print_next_steps(ui, msg, is_windows)

    if (
        updates.get("ENABLE_LEDS") is True
        and importlib.util.find_spec("gpiozero") is None
    ):
        ui.blank()
        ui.status("warn", msg["leds_missing_gpiozero"])
        ui.command_hint(msg["leds_install_hint"], msg["leds_install_cmd"])
    return 0


if __name__ == "__main__":
    raise SystemExit(run_setup())
