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


def _validate_game_config(path: Path) -> None:
    """Validate the game XML before the user approves any file changes."""
    try:
        tree = ET.parse(path)
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


def _ask_ip(
    input_fn: InputFunction,
    output_fn: OutputFunction,
    default_ip: str = DEFAULT_IP,
) -> str:
    while True:
        answer = input_fn(
            f"Dashboard bilgisayarının IPv4 adresi [{default_ip}]: "
        ).strip()
        value = answer or default_ip
        try:
            normalized = validate_ipv4(value)
        except ValueError:
            output_fn("Geçersiz IPv4 adresi. Örnek: 127.0.0.1 veya 192.168.1.25")
            continue

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


def _ask_yes_no(
    prompt: str,
    default: bool,
    input_fn: InputFunction,
    output_fn: OutputFunction = print,
) -> bool:
    default_text = "E" if default else "H"
    while True:
        answer = input_fn(f"{prompt} (E/H) [{default_text}]: ").strip().lower()
        if not answer:
            return default
        if answer in {"e", "evet", "y", "yes"}:
            return True
        if answer in {"h", "hayır", "hayir", "n", "no"}:
            return False
        output_fn("Geçersiz cevap. Lütfen E veya H girin.")


def run_setup(
    project_root: Path | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> int:
    """Run the interactive setup flow and return a process exit code."""
    project_root = project_root or Path(__file__).resolve().parent
    config_path = project_root / "config.py"

    output_fn("DiRT Rally 2.0 Telemetry Dashboard - İlk Kurulum")
    output_fn(
        "Oyun kapalı olmalıdır; XML dosyası onaydan sonra yedeklenerek güncellenir.\n"
    )
    try:
        current_config = read_config_defaults(config_path)
    except (OSError, SetupError) as error:
        output_fn(f"Mevcut config.py okunamadı: {error}")
        return 1

    destination_ip = _ask_ip(
        input_fn,
        output_fn,
        str(current_config["LISTEN_IP"]),
    )
    dash_style = _ask_choice(
        "Dashboard türü",
        ("digital", "analog"),
        str(current_config["DASH_STYLE"]),
        input_fn,
        output_fn,
    )
    enable_overlay = _ask_yes_no(
        "Windows overlay etkinleştirilsin mi?",
        bool(current_config["ENABLE_OVERLAY"]),
        input_fn,
        output_fn,
    )

    game_config = find_game_config()
    if game_config is not None:
        try:
            _validate_game_config(game_config)
        except SetupError as error:
            output_fn(f"Oyun XML'i doğrulanamadı: {error}")
            return 1

    output_fn("\nSeçilen ayarlar:")
    output_fn(f"- Dashboard bilgisayarının IPv4 adresi: {destination_ip}")
    output_fn(f"- Dashboard türü: {dash_style}")
    output_fn(f"- Windows overlay: {'Evet' if enable_overlay else 'Hayır'}")
    output_fn(f"- UDP portu: {DEFAULT_PORT}")
    if game_config is None:
        output_fn("- Oyun XML'i: otomatik bulunamadı; manuel yapılandırma gerekiyor")
    else:
        output_fn(f"- Oyun XML'i: {game_config}")

    if not _ask_yes_no(
        "Bu ayarlarla devam edilsin mi?",
        True,
        input_fn,
        output_fn,
    ):
        output_fn("Kurulum iptal edildi. Dosyalarda değişiklik yapılmadı.")
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
        output_fn(f"config.py güncellenemedi: {error}")
        return 1

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
    output_fn(
        "Bağlantıyı kontrol etmek için dashboard kapalıyken "
        "python telemetry_check.py komutunu çalıştırın."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run_setup())
