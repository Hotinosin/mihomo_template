import unittest

from update import convert


class ConversionTests(unittest.TestCase):
    def test_domain_semantics_and_duplicates(self):
        self.assertEqual(convert("geosite", "# header\nexample.com\n+.example.org\nexample.com\n"),
                         ["DOMAIN,example.com", "DOMAIN-SUFFIX,example.org"])

    def test_both_ip_families(self):
        self.assertEqual(convert("geoip", "192.0.2.0/24\n2001:db8::/32\n"),
                         ["IP-CIDR,192.0.2.0/24", "IP-CIDR6,2001:db8::/32"])

    def test_unknown_or_empty_inputs_fail(self):
        for kind, content in [("geosite", "regexp:.*example"), ("geosite", "*.example.com"),
                              ("geosite", "DOMAIN,example.com"), ("geosite", "# empty"),
                              ("geoip", "192.0.2.1/24"), ("geoip", "not-an-ip")]:
            with self.subTest(kind=kind, content=content), self.assertRaises(ValueError):
                convert(kind, content)


if __name__ == "__main__":
    unittest.main()
