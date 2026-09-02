#!/usr/bin/python3

from pathlib import Path
import unittest


SERVICE = Path(__file__).resolve().parents[1] / "debian/hubdns.service"


class HubDNSServiceTests(unittest.TestCase):
    def test_release_runs_only_when_the_service_is_stopped(self):
        service = SERVICE.read_text(encoding="utf-8")
        self.assertIn("Type=oneshot\nRemainAfterExit=yes\n", service)
        self.assertIn("ExecStart=/usr/bin/hubdns-update\n", service)
        self.assertIn("ExecStop=/usr/bin/hubdns-release\n", service)


if __name__ == "__main__":
    unittest.main(verbosity=2)
