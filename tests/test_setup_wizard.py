import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from setup_wizard import (
    _ask_language,
    configure_game_xml,
    run_setup,
    update_config_file,
    validate_ipv4,
)
from telemetry_check import check_telemetry


class SetupWizardTests(unittest.TestCase):
    def test_ask_language_defaults_to_english_on_empty(self):
        self.assertEqual(_ask_language(lambda _p: "", lambda _m: None), "en")

    def test_ask_language_accepts_turkish_and_retries_invalid(self):
        inputs = iter(["de", "tr"])
        outputs = []
        result = _ask_language(lambda _p: next(inputs), outputs.append)
        self.assertEqual(result, "tr")
        self.assertTrue(len(outputs) >= 1)

    def test_telemetry_check_times_out_gracefully(self):
        output = []
        result = check_telemetry(listen_ip="127.0.0.1", listen_port=29999, timeout=0.01, output_fn=output.append)
        self.assertEqual(result, 1)
        self.assertTrue(any("telemetry packet received" in line for line in output))

    def test_validate_ipv4_accepts_and_normalizes_address(self):
        self.assertEqual(validate_ipv4(" 192.168.1.25 "), "192.168.1.25")

    def test_validate_ipv4_rejects_invalid_and_ipv6_addresses(self):
        with self.assertRaises(ValueError):
            validate_ipv4("not-an-ip")
        with self.assertRaises(ValueError):
            validate_ipv4("::1")

    def test_update_config_file_creates_backup_and_updates_values(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.py"
            config_path.write_text(
                'DASH_STYLE = "digital"\nENABLE_OVERLAY = True\n',
                encoding="utf-8",
            )

            backup = update_config_file(
                config_path,
                {"DASH_STYLE": "analog", "ENABLE_OVERLAY": False},
            )

            self.assertTrue(backup.is_file())
            self.assertEqual(
                config_path.read_text(encoding="utf-8"),
                'DASH_STYLE = "analog"\nENABLE_OVERLAY = False\n',
            )
            self.assertEqual(
                backup.read_text(encoding="utf-8"),
                'DASH_STYLE = "digital"\nENABLE_OVERLAY = True\n',
            )

    def test_configure_game_xml_creates_backup_and_updates_udp_node(self):
        with tempfile.TemporaryDirectory() as directory:
            xml_path = Path(directory) / "hardware_settings_config.xml"
            xml_path.write_text(
                """<?xml version='1.0' encoding='utf-8'?>
<hardware_settings_config>
  <motion_platform>
    <udp enabled="false" extradata="0" ip="127.0.0.1" port="10000"
         delay="1" custom="keep" />
  </motion_platform>
</hardware_settings_config>
""",
                encoding="utf-8",
            )

            backup = configure_game_xml(xml_path, "192.168.1.25")
            root = ET.parse(xml_path).getroot()
            udp = root.find(".//motion_platform/udp")

            self.assertTrue(backup.is_file())
            self.assertIsNotNone(udp)
            assert udp is not None
            self.assertEqual(udp.attrib["enabled"], "true")
            self.assertEqual(udp.attrib["extradata"], "3")
            self.assertEqual(udp.attrib["ip"], "192.168.1.25")
            self.assertEqual(udp.attrib["port"], "20777")
            self.assertEqual(udp.attrib["custom"], "keep")

    def test_configure_game_xml_adds_missing_udp_node(self):
        with tempfile.TemporaryDirectory() as directory:
            xml_path = Path(directory) / "hardware_settings_config.xml"
            xml_path.write_text(
                "<hardware_settings_config>"
                "<motion_platform /></hardware_settings_config>",
                encoding="utf-8",
            )

            configure_game_xml(xml_path, "127.0.0.1")
            udp = ET.parse(xml_path).getroot().find(".//motion_platform/udp")

            self.assertIsNotNone(udp)
            assert udp is not None
            self.assertEqual(udp.attrib["enabled"], "true")
            self.assertEqual(udp.attrib["extradata"], "3")
            self.assertEqual(udp.attrib["delay"], "1")

    def test_run_setup_updates_listen_ip_and_xml_after_confirmation_english(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            config_path = project_root / "config.py"
            config_path.write_text(
                'LISTEN_IP = "127.0.0.1"\n'
                'DASH_STYLE = "digital"\n'
                "ENABLE_OVERLAY = True\n",
                encoding="utf-8",
            )
            xml_path = project_root / "hardware_settings_config.xml"
            xml_path.write_text(
                "<hardware_settings_config><motion_platform>"
                '<udp custom="keep" /></motion_platform></hardware_settings_config>',
                encoding="utf-8",
            )
            answers = iter(["en", "192.168.1.25", "analog", "N", "Y"])
            output = []

            with patch("setup_wizard.find_game_config", return_value=xml_path):
                result = run_setup(
                    project_root=project_root,
                    input_fn=lambda _prompt: next(answers),
                    output_fn=output.append,
                )

            self.assertEqual(result, 0)
            self.assertIn('LISTEN_IP = "192.168.1.25"', config_path.read_text())
            self.assertIn('DASH_STYLE = "analog"', config_path.read_text())
            self.assertIn("ENABLE_OVERLAY = False", config_path.read_text())
            udp = ET.parse(xml_path).getroot().find(".//motion_platform/udp")
            self.assertIsNotNone(udp)
            assert udp is not None
            self.assertEqual(udp.attrib["ip"], "192.168.1.25")
            self.assertEqual(udp.attrib["custom"], "keep")
            self.assertTrue(list(project_root.glob("config.py.bak-*")))
            self.assertTrue(list(project_root.glob("hardware_settings_config.xml.bak-*")))
            self.assertTrue(any("Setup Completed Successfully" in line for line in output))

    def test_run_setup_updates_listen_ip_and_xml_after_confirmation_turkish(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            config_path = project_root / "config.py"
            config_path.write_text(
                'LISTEN_IP = "127.0.0.1"\n'
                'DASH_STYLE = "digital"\n'
                "ENABLE_OVERLAY = True\n",
                encoding="utf-8",
            )
            xml_path = project_root / "hardware_settings_config.xml"
            xml_path.write_text(
                "<hardware_settings_config><motion_platform>"
                '<udp custom="keep" /></motion_platform></hardware_settings_config>',
                encoding="utf-8",
            )
            answers = iter(["tr", "192.168.1.25", "analog", "H", "E"])
            output = []

            with patch("setup_wizard.find_game_config", return_value=xml_path):
                result = run_setup(
                    project_root=project_root,
                    input_fn=lambda _prompt: next(answers),
                    output_fn=output.append,
                )

            self.assertEqual(result, 0)
            self.assertIn('LISTEN_IP = "192.168.1.25"', config_path.read_text())
            self.assertIn('DASH_STYLE = "analog"', config_path.read_text())
            self.assertIn("ENABLE_OVERLAY = False", config_path.read_text())
            self.assertTrue(any("Kurulum Başarıyla Tamamlandı" in line for line in output))

    def test_run_setup_preserves_current_values_and_retries_invalid_yes_no(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            config_path = project_root / "config.py"
            original = (
                'LISTEN_IP = "0.0.0.0"\nDASH_STYLE = "analog"\nENABLE_OVERLAY = False\n'
            )
            config_path.write_text(original, encoding="utf-8")
            answers = iter(["tr", "", "", "belki", "", ""])
            output = []

            with patch("setup_wizard.find_game_config", return_value=None):
                result = run_setup(
                    project_root=project_root,
                    input_fn=lambda _prompt: next(answers),
                    output_fn=output.append,
                )

            self.assertEqual(result, 0)
            self.assertEqual(
                config_path.read_text(encoding="utf-8"),
                original,
            )
            self.assertTrue(any("Geçersiz cevap" in message for message in output))

    def test_run_setup_does_not_change_files_without_confirmation(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            config_path = project_root / "config.py"
            original = (
                'LISTEN_IP = "127.0.0.1"\nDASH_STYLE = "digital"\nENABLE_OVERLAY = True\n'
            )
            config_path.write_text(original, encoding="utf-8")
            answers = iter(["en", "192.168.1.25", "analog", "N", "N"])

            with patch("setup_wizard.find_game_config", return_value=None):
                result = run_setup(
                    project_root=project_root,
                    input_fn=lambda _prompt: next(answers),
                    output_fn=lambda _message: None,
                )

            self.assertEqual(result, 0)
            self.assertEqual(config_path.read_text(encoding="utf-8"), original)
            self.assertEqual(list(project_root.glob("*.bak-*")), [])


if __name__ == "__main__":
    unittest.main()
