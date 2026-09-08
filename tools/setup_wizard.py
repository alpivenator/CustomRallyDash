"""Interactive first-run setup for DiRT Rally 2.0 Telemetry Dashboard."""

from __future__ import annotations

import ast
import ipaddress
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 20777
DEFAULT_DASH_STYLE = "digital"
DEFAULT_ENABLE_OVERLAY = True
CONFIG_KEYS = ("LISTEN_IP", "DASH_STYLE", "ENABLE_OVERLAY")
CONFIG_DEFAULTS: dict[str, object] = {
    "LISTEN_IP": DEFAULT_IP,
    "DASH_STYLE": DEFAULT_DASH_STYLE,
    "ENABLE_OVERLAY": DEFAULT_ENABLE_OVERLAY,
}
GAME_CONFIG_RELATIVE_PATH = Path(
    "Documents",
    "My Games",
    "DiRT Rally 2.0",
    "hardwaresettings",
    "hardware_settings_config.xml",
)

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], Any]

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "lang_prompt": "Select language / Dil seçin [en/tr] (en): ",
        "lang_invalid": "Invalid choice. Please enter 'en' or 'tr'.",
        "banner_title": "CustomRallyDash - Initial Setup",
        "banner_note": (
            "DiRT Rally 2.0 must be closed. Configuration files will be backed up "
            "before updating.\n"
        ),
        "prompt_ip": "Dashboard computer IPv4 address [{default}]: ",
        "invalid_ip": "Invalid IPv4 address. Example: 127.0.0.1 or 192.168.1.25",
        "prompt_dash_style": "Dashboard style",
        "invalid_choice": "Invalid choice. Please choose one of: {choices}",
        "prompt_overlay": "Enable Windows overlay?",
        "invalid_yes_no": "Invalid answer. Please enter {yes} or {no}.",
        "config_read_error": "Could not read config.py: {error}",
        "game_xml_invalid": "Game XML could not be verified: {error}",
        "summary_title": "\nSelected settings:",
        "summary_ip": "- Dashboard computer IPv4 address: {ip}",
        "summary_style": "- Dashboard style: {style}",
        "summary_overlay": "- Windows overlay: {overlay}",
        "summary_port": "- UDP port: {port}",
        "summary_xml_found": "- Game XML: {path}",
        "summary_xml_missing": (
            "- Game XML: not found automatically (manual configuration required)"
        ),
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
        "game_xml_manual_instruction": (
            "Manually add this UDP element:\n"
            '<udp enabled="true" extradata="3" ip="{ip}" port="{port}" delay="1" />'
        ),
        "game_xml_updated": "Game XML updated. Backup: {path}",
        "config_updated": "config.py updated. Backup: {path}",
        "completion_banner": (
            "\n======================================================\n"
            "  Setup Completed Successfully!\n"
            "======================================================"
        ),
        "completion_instructions": (
            "\nNext steps:\n"
            "  1. Test telemetry connection (with DiRT Rally 2.0 in a stage):\n"
            "     run check_telemetry.bat  (or: .venv\\Scripts\\python.exe "
            "tools\\telemetry_check.py)\n"
            "     Note: The dashboard must be closed while testing.\n\n"
            "  2. Preview without the game (mock telemetry):\n"
            "     run run_mock.bat  (or: python main.py --mock)\n\n"
            "  3. Customise visual theme:\n"
            "     run select_theme.bat  (or: .venv\\Scripts\\python.exe "
            "tools\\theme_selector.py)\n\n"
            "  4. Launch the dashboard:\n"
            "     run run_dash.bat\n"
        ),
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
            "yedeklenerek güncellenir.\n"
        ),
        "prompt_ip": "Dashboard bilgisayarının IPv4 adresi [{default}]: ",
        "invalid_ip": "Geçersiz IPv4 adresi. Örnek: 127.0.0.1 veya 192.168.1.25",
        "prompt_dash_style": "Dashboard türü",
        "invalid_choice": "Geçersiz seçim. Şunlardan birini kullanın: {choices}",
        "prompt_overlay": "Windows overlay etkinleştirilsin mi?",
        "invalid_yes_no": "Geçersiz cevap. Lütfen {yes} veya {no} girin.",
        "config_read_error": "Mevcut config.py okunamadı: {error}",
        "game_xml_invalid": "Oyun XML'i doğrulanamadı: {error}",
        "summary_title": "\nSeçilen ayarlar:",
        "summary_ip": "- Dashboard bilgisayarının IPv4 adresi: {ip}",
        "summary_style": "- Dashboard türü: {style}",
        "summary_overlay": "- Windows overlay: {overlay}",
        "summary_port": "- UDP portu: {port}",
        "summary_xml_found": "- Oyun XML'i: {path}",
        "summary_xml_missing": (
            "- Oyun XML'i: otomatik bulunamadı (manuel yapılandırma gerekiyor)"
        ),
        "prompt_confirm": "Bu ayarlarla devam edilsin mi?",
        "setup_cancelled": "Kurulum iptal edildi. Dosyalarda değişiklik yapılmadı.",
        "config_update_error": "config.py güncellenemedi: {error}",
        "game_xml_update_error": "Oyun XML'i güncellenemedi: {error}",
        "config_backup_info": "config.py yedeği: {path}",
        "game_xml_not_found_header": ("DiRT Rally 2.0 XML dosyası otomatik bulunamadı."),
        "game_xml_expected_location": (
            "Beklenen konum: Documents\\My Games\\DiRT Rally 2.0\\"
            "hardwaresettings\\hardware_settings_config.xml"
        ),
        "game_xml_manual_instruction": (
            "Manuel olarak şu UDP satırını ekleyin:\n"
            '<udp enabled="true" extradata="3" ip="{ip}" port="{port}" delay="1" />'
        ),
        "game_xml_updated": "Oyun XML'i güncellendi. Yedek: {path}",
        "config_updated": "config.py güncellendi. Yedek: {path}",
        "completion_banner": (
            "\n======================================================\n"
            "  Kurulum Başarıyla Tamamlandı!\n"
            "======================================================"
        ),
        "completion_instructions": (
            "\nSonraki adımlar:\n"
            "  1. Telemetri bağlantısını test edin (DiRT Rally 2.0 yarıştayken):\n"
            "     check_telemetry.bat çalıştırın  (veya: .venv\\Scripts\\python.exe "
            "tools\\telemetry_check.py)\n"
            "     Not: Test sırasında dashboard kapalı olmalıdır.\n\n"
            "  2. Oyun olmadan sahte telemetri ile test edin / önizleyin:\n"
            "     run_mock.bat çalıştırın  (veya: python main.py --mock)\n\n"
            "  3. Görsel temayı özelleştirin:\n"
            "     select_theme.bat çalıştırın  (veya: .venv\\Scripts\\python.exe "
            "tools\\theme_selector.py)\n\n"
            "  4. Dashboard'u başlatın:\n"
            "     run_dash.bat çalıştırın\n"
        ),
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

    return values


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
) -> str:
    """Ask user to select interface language, defaulting to English."""
    while True:
        answer = input_fn(MESSAGES["en"]["lang_prompt"]).strip().lower()
        if not answer or answer in {"en", "1", "english", "ingilizce"}:
            return "en"
        if answer in {"tr", "2", "turkish", "türkçe", "turkce"}:
            return "tr"
        output_fn(MESSAGES["en"]["lang_invalid"])


def _ask_ip(
    input_fn: InputFunction,
    output_fn: OutputFunction,
    default_ip: str = DEFAULT_IP,
    lang: str = "en",
) -> str:
    msg = MESSAGES[lang]
    prompt_text = msg["prompt_ip"].format(default=default_ip)
    while True:
        answer = input_fn(prompt_text).strip()
        value = answer or default_ip
        try:
            normalized = validate_ipv4(value)
        except ValueError:
            output_fn(msg["invalid_ip"])
            continue

        return normalized


def _ask_choice(
    prompt: str,
    choices: tuple[str, ...],
    default: str,
    input_fn: InputFunction,
    output_fn: OutputFunction,
    lang: str = "en",
) -> str:
    msg = MESSAGES[lang]
    choices_text = "/".join(choices)
    prompt_text = f"{prompt} ({choices_text}) [{default}]: "
    while True:
        answer = input_fn(prompt_text).strip().lower()
        value = answer or default
        if value in choices:
            return value
        output_fn(msg["invalid_choice"].format(choices=choices_text))


def _ask_yes_no(
    prompt: str,
    default: bool,
    input_fn: InputFunction,
    output_fn: OutputFunction = print,
    lang: str = "en",
) -> bool:
    msg = MESSAGES[lang]
    yes_short = msg["yes_short"]
    no_short = msg["no_short"]
    default_text = yes_short if default else no_short
    prompt_text = f"{prompt} ({yes_short}/{no_short}) [{default_text}]: "

    while True:
        answer = input_fn(prompt_text).strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes", "e", "evet", "1", "true"}:
            return True
        if answer in {"n", "no", "h", "hayır", "hayir", "0", "false"}:
            return False
        output_fn(msg["invalid_yes_no"].format(yes=yes_short, no=no_short))


def run_setup(
    project_root: Path | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    lang: str | None = None,
) -> int:
    """Run the interactive setup flow and return a process exit code."""
    project_root = project_root or Path(__file__).resolve().parent.parent
    config_path = project_root / "config.py"

    if lang is None:
        selected_lang = _ask_language(input_fn, output_fn)
    else:
        selected_lang = "tr" if lang.lower().startswith("tr") else "en"

    msg = MESSAGES[selected_lang]

    output_fn(f"\n{msg['banner_title']}")
    output_fn(msg["banner_note"])

    try:
        current_config = read_config_defaults(config_path)
    except (OSError, SetupError) as error:
        output_fn(msg["config_read_error"].format(error=error))
        return 1

    destination_ip = _ask_ip(
        input_fn,
        output_fn,
        str(current_config["LISTEN_IP"]),
        lang=selected_lang,
    )
    dash_style = _ask_choice(
        msg["prompt_dash_style"],
        ("digital", "analog"),
        str(current_config["DASH_STYLE"]),
        input_fn,
        output_fn,
        lang=selected_lang,
    )
    enable_overlay = _ask_yes_no(
        msg["prompt_overlay"],
        bool(current_config["ENABLE_OVERLAY"]),
        input_fn,
        output_fn,
        lang=selected_lang,
    )

    game_config = find_game_config()
    if game_config is not None:
        try:
            _validate_game_config(game_config)
        except SetupError as error:
            output_fn(msg["game_xml_invalid"].format(error=error))
            return 1

    output_fn(msg["summary_title"])
    output_fn(msg["summary_ip"].format(ip=destination_ip))
    output_fn(msg["summary_style"].format(style=dash_style))
    overlay_text = msg["yes_label"] if enable_overlay else msg["no_label"]
    output_fn(msg["summary_overlay"].format(overlay=overlay_text))
    output_fn(msg["summary_port"].format(port=DEFAULT_PORT))
    if game_config is None:
        output_fn(msg["summary_xml_missing"])
    else:
        output_fn(msg["summary_xml_found"].format(path=game_config))

    output_fn("")
    if not _ask_yes_no(
        msg["prompt_confirm"],
        True,
        input_fn,
        output_fn,
        lang=selected_lang,
    ):
        output_fn(msg["setup_cancelled"])
        return 0

    try:
        config_backup = update_config_file(
            config_path,
            {
                "LISTEN_IP": destination_ip,
                "DASH_STYLE": dash_style,
                "ENABLE_OVERLAY": enable_overlay,
            },
        )
    except (OSError, SetupError) as error:
        output_fn(msg["config_update_error"].format(error=error))
        return 1

    if game_config is None:
        output_fn(f"\n{msg['game_xml_not_found_header']}")
        output_fn(msg["game_xml_expected_location"])
        output_fn(
            msg["game_xml_manual_instruction"].format(
                ip=destination_ip, port=DEFAULT_PORT
            )
        )
    else:
        try:
            game_backup = configure_game_xml(game_config, destination_ip)
        except (OSError, SetupError) as error:
            output_fn(msg["game_xml_update_error"].format(error=error))
            output_fn(msg["config_backup_info"].format(path=config_backup))
            return 1
        output_fn(msg["game_xml_updated"].format(path=game_backup))

    output_fn(msg["config_updated"].format(path=config_backup))
    output_fn(msg["completion_banner"])
    output_fn(msg["completion_instructions"])
    return 0


if __name__ == "__main__":
    raise SystemExit(run_setup())
