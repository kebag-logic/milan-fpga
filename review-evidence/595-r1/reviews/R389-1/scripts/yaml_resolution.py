#!/usr/bin/env python3
"""Show how the installed PyYAML SafeLoader resolves hex-looking scalars."""
import yaml

SPELLINGS = [
    "020000000002", "0x020000000002", "02:00:00:00:00:02", "10:20:30:40:50:02",
    "02-00-00-00-00-02", "0200_0000_0002", "0x0200_0000_0002", "123456",
    "001234", "0o17", "0b101", "017", "08", "1_000", "+12", "-1", "190:20:30",
    "1e3", "1.5", ".inf", ".nan", "1:30.5", "0x1BC5", "001BC5", "1BC5", "E1",
    "1E1", "true", "false", "yes", "no", "on", "off", "y", "n", "Y", "N",
    "~", "null", "", "[]", "{}", "12:34:56:78:9a:bc", "0000000000",
    "2e0", "0e5",
]

print(f"pyyaml {yaml.__version__} libyaml={getattr(yaml, '__with_libyaml__', None)}")
for s in SPELLINGS:
    v = yaml.safe_load(f"k: {s}")["k"]
    print(f"{s!r:24} -> {type(v).__name__:6} {v!r}")
