#!/usr/bin/env python3
"""Re-check prior findings at a tree (run from its root): F1 literal absence, S1 lenient MAC shape."""
import sys
from pathlib import Path
sys.path.insert(0, "sw/builder")
import endstation_builder as eb  # noqa: E402
text = Path("sw/builder/test_declarations.py").read_text()
print("F1 literal present:", "protocol-processor/hdl/adp/pp_adp_pkg.sv" in text)
for v in ("2:0:0:0:0:2", "02:00:00:00:02", "-2", " 020000000002 "):
    try:
        print(f"S1 _mac48({v!r}) = 0x{eb._mac48(v, 'probe'):012X}")
    except eb.ConfigError as exc:
        print(f"S1 _mac48({v!r}) refused: {exc}")
for v in ("+1BC5",):
    try:
        print(f"S1 _declared_uint({v!r}) = 0x{eb._declared_uint(v, 24, 'probe'):06X}")
    except eb.ConfigError as exc:
        print(f"S1 _declared_uint({v!r}) refused: {exc}")
