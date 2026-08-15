import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from setup_wizard import configure_game_xml, update_config_file, validate_ipv4


class SetupWizardTests(unittest.TestCase):
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
    <udp enabled="false" extradata="0" ip="127.0.0.1" port="10000" delay="1" custom="keep" />
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
                "<hardware_settings_config><motion_platform /></hardware_settings_config>",
                encoding="utf-8",
            )

            configure_game_xml(xml_path, "127.0.0.1")
            udp = ET.parse(xml_path).getroot().find(".//motion_platform/udp")

            self.assertIsNotNone(udp)
            assert udp is not None
            self.assertEqual(udp.attrib["enabled"], "true")
            self.assertEqual(udp.attrib["extradata"], "3")
            self.assertEqual(udp.attrib["delay"], "1")


if __name__ == "__main__":
    unittest.main()
