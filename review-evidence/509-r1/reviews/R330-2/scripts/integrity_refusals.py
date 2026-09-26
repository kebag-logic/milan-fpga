#!/usr/bin/env python3
"""Feed tampered copies of one tracked image to the audit decoder.

Usage: python3 -O integrity_refusals.py <tree>   (also run without -O)
Imports <tree>/scripts/audit_pp_descriptors.py, packs arty_current through its
own generate(), then checks each integrity refusal still fires. Uses no assert,
so the probe itself also survives -O.
"""
import json
import struct
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import audit_pp_descriptors as audit  # noqa: E402


def outcome(blob: bytes) -> str:
    try:
        audit.packed_rows(bytes(blob))
        return "decoded"
    except audit.AuditError as exc:
        return f"AuditError: {exc}"
    except Exception as exc:  # noqa: BLE001 - classify, do not hide
        return f"{type(exc).__name__}: {exc}"


cfg = audit.builder.load_config(tree / "configs" / "endstation_arty_current.yaml")
_, pristine = audit.generate(cfg)
rows = audit.packed_rows(pristine)
index_off = audit.uint(pristine, 12, 4)
cases = {}
cases["pristine"] = bytearray(pristine)
b = bytearray(pristine); b[0] ^= 1; cases["magic"] = b
b = bytearray(pristine); struct.pack_into(">H", b, 4, 2); cases["version"] = b
b = bytearray(pristine) + b"\x00"; cases["trailing byte (declared length)"] = b
b = bytearray(pristine); b[28] ^= 1; cases["header checksum"] = b
# body type/index vs directory: row 0's first body, header untouched
_, _, _, _, base, _, _ = struct.unpack_from(">HHHHIHH", pristine, index_off)
b = bytearray(pristine); b[base + 1] ^= 1; cases["body type vs directory"] = b
b = bytearray(pristine); b[base + 3] ^= 1; cases["body index vs directory"] = b
# descriptor extends beyond image: enlarge row 0 length in the index table
b = bytearray(pristine); struct.pack_into(">H", b, index_off + 6, len(pristine)); cases["row beyond image"] = b
result = dict(optimize=sys.flags.optimize, rows=len(rows),
              outcomes={k: outcome(v) for k, v in cases.items()})
print(json.dumps(result, indent=2))
