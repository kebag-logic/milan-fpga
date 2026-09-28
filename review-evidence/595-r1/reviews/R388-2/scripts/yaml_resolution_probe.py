#!/usr/bin/env python3
"""Show how the local PyYAML safe_load resolves each unquoted/quoted spelling."""
import sys
import yaml

SPELLINGS = [
    "020000000002", "0x020000000002", "123456789012", "10:20:30:40:50:02",
    "02:00:00:00:00:02", "02-00-00-00-00-02", "0x0200_0000_0002", "0200_0000_0002",
    "0o17", "017", "0b101", "1_000", "190:20:30", "123456", "001234", "10:20:30",
    "0x001BC5", "001BC5", "0x0000C588", "0000C588",
    "true", "false", "yes", "no", "on", "off", "y", "n", "Yes", "NO",
    "null", "~", "", "1.5", "1e3", ".inf", ".nan", "1:30.5",
    "2026-09-28", "[]", "{}", '"020000000002"', "'10:20:30:40:50:02'",
    "0205022000806000", "0x0205022000806000",
]
print(f"PyYAML {yaml.__version__} python {sys.version.split()[0]}")
for s in SPELLINGS:
    v = yaml.safe_load(f"k: {s}")["k"]
    print(f"{s!r:28} -> {type(v).__name__:8} {v!r}")
