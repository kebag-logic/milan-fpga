#!/usr/bin/env python3
"""Judge spellings with one tree's builder parsers.

usage: item6_judge.py <tree-root> <spellings.json> <out.json>
spellings.json: [[field_kind, spelling], ...]; field_kind in
mac, dmac, eui64, oui, caps. Output: [[kind, spelling, verdict], ...] where
verdict is "ACCEPT 0x..." or "REFUSE <message>".
"""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location("eb_under_test", root / "sw/builder/endstation_builder.py")
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)

def dmac(v):
    s = {"stream_dmac_base": v}
    if hasattr(eb, "_srp_dmac"):
        return eb._srp_dmac(s)
    raise RuntimeError("no _srp_dmac")

KIND = {
    "mac": lambda v: eb._mac48(v, "platform.mac_address"),
    "dmac": dmac,
    "eui64": lambda v: eb._eui64(v, "entity.entity_id"),
    "oui": lambda v: eb._declared_uint(v, 24, "entity.vendor_oui"),
    "caps": lambda v: eb._declared_uint(v, 32, "entity.entity_capabilities"),
}
out = []
for kind, spelling in json.loads(Path(sys.argv[2]).read_text()):
    try:
        n = KIND[kind](spelling)
        out.append([kind, spelling, f"ACCEPT 0x{n:X}" if isinstance(n, int) else f"ACCEPT {n!r}"])
    except eb.ConfigError as exc:
        out.append([kind, spelling, f"REFUSE {exc}"])
    except Exception as exc:  # a crash is a finding, not a verdict
        out.append([kind, spelling, f"CRASH {type(exc).__name__}: {exc}"])
Path(sys.argv[3]).write_text(json.dumps(out, indent=0))
