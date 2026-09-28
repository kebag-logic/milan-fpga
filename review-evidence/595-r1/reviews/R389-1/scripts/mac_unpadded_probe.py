#!/usr/bin/env python3
"""Pre-existing quoted-MAC behaviour: separators are deleted, not parsed as
octet boundaries. Usage: mac_unpadded_probe.py <tree>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "sw/builder"))
import endstation_builder as eb
for s in ("02:00:00:00:00:02", "2:0:0:0:0:2", "2-0-0-0-0-2", "02:00:00:00:02", "0200:0000:0002", "-2"):
    try:
        n = eb._mac48(s, "platform.mac_address")
        print(f"{s!r:22} -> {':'.join(f'{(n >> k) & 0xFF:02x}' for k in range(40, -8, -8))}")
    except eb.ConfigError as e:
        print(f"{s!r:22} -> REFUSED {e}")
