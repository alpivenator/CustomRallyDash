"""Interactive first-run setup for DiRT Rally 2.0 Telemetry Dashboard."""

from __future__ import annotations

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
CONFIG_KEYS = ("DASH_STYLE", "ENABLE_OVERLAY")
GAME_CONFIG_RELATIVE_PATH = Path(
    "Documents",
    "My Games",
    "DiRT Rally 2.0",
    "hardwaresettings",
    "hardware_settings_config.xml",
)

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], Any]


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


def update_config_file(path: Path, updates: dict[str, object]) -> Path:
    """Back up config.py and update existing top-level assignment lines."""
    content = path.read_text(encoding="utf-8")
    backup = make_backup(path)

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
            raise SetupError(f"Expected one assignment for {key}, found {replacement_count}.")

    _atomic_write(path, content)
    return backup


def configure_game_xml(path: Path, ip: str, port: int = DEFAULT_PORT) -> Path:
    """Back up and update the game's motion-platform UDP configuration."""
    try:
        tree = ET.parse(path)
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


def _ask_ip(input_fn: InputFunction, output_fn: OutputFunction) -> str:
    while True:
        answer = input_fn(f"Alıcı bilgisayarın IPv4 adresi [{DEFAULT_IP}]: ").strip()
        value = answer or DEFAULT_IP
        try:
            normalized = validate_ipv4(value)
        except ValueError:
            output_fn("Geçersiz IPv4 adresi. Örnek: 127.0.0.1 veya 192.168.1.25")
            continue

        if normalized == DEFAULT_IP:
            output_fn(
                "Uyarı: 127.0.0.1 bazı Windows sistemlerinde loopback/Firewall "
                "nedeniyle sorun çıkarabilir. Telemetri alınamazsa bu bilgisayarın "
                "yerel ağ IP adresini kullanın."
            )
        return normalized


def _ask_choice(
    prompt: str,
    choices: tuple[str, ...],
    default: str,
    input_fn: InputFunction,
    output_fn: OutputFunction,
) -> str:
    choices_text = "/".join(choices)
    while True:
        answer = input_fn(f"{prompt} ({choices_text}) [{default}]: ").strip().lower()
        value = answer or default
        if value in choices:
            return value
        output_fn(f"Geçersiz seçim. Şunlardan birini kullanın: {choices_text}")


def _ask_yes_no(prompt: str, default: bool, input_fn: InputFunction) -> bool:
    default_text = "E" if default else "H"
    answer = input_fn(f"{prompt} (E/H) [{default_text}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"e", "evet", "y", "yes"}


def run_setup(
    project_root: Path | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> int:
    """Run the interactive setup flow and return a process exit code."""
    project_root = project_root or Path(__file__).resolve().parent
    config_path = project_root / "config.py"

    output_fn("DiRT Rally 2.0 Telemetry Dashboard - İlk Kurulum")
    output_fn("Oyun kapalı olmalıdır; XML dosyası yedeklenerek güncellenecektir.\n")

    destination_ip = _ask_ip(input_fn, output_fn)
    dash_style = _ask_choice(
        "Dashboard türü",
        ("digital", "analog"),
        "digital",
        input_fn,
        output_fn,
    )
    enable_overlay = _ask_yes_no("Windows overlay etkinleştirilsin mi?", True, input_fn)

    try:
        config_backup = update_config_file(
            config_path,
            {"DASH_STYLE": dash_style, "ENABLE_OVERLAY": enable_overlay},
        )
    except (OSError, SetupError) as error:
        output_fn(f"config.py güncellenemedi: {error}")
        return 1

    game_config = find_game_config()
    if game_config is None:
        output_fn("DiRT Rally 2.0 XML dosyası otomatik bulunamadı.")
        output_fn(
            "Beklenen konum: Documents\\My Games\\DiRT Rally 2.0\\hardwaresettings\\"
            "hardware_settings_config.xml"
        )
        output_fn(
            f'Manuel olarak şu UDP satırını ekleyin: <udp enabled="true" '
            f'extradata="3" ip="{destination_ip}" port="{DEFAULT_PORT}" delay="1" />'
        )
    else:
        try:
            game_backup = configure_game_xml(game_config, destination_ip)
        except (OSError, SetupError) as error:
            output_fn(f"Oyun XML'i güncellenemedi: {error}")
            output_fn(f"config.py yedeği: {config_backup}")
            return 1
        output_fn(f"Oyun XML'i güncellendi. Yedek: {game_backup}")

    output_fn(f"config.py güncellendi. Yedek: {config_backup}")
    output_fn("Kurulum tamamlandı. Programı run_dash.bat ile başlatabilirsiniz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_setup())
