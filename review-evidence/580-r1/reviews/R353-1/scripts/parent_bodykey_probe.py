#!/usr/bin/env python3
"""Parent-level body/key probe.

Loads each shipping configuration's generated kl-aem-image document (aem.json,
written by avdecc/gen_aemi_image.py --json) and packs it with the processor
packer of the old and new pin trees: pristine, then with one descriptor's
body type or body index bytes changed so they disagree with its directory key.
The new pin must refuse each mismatch and the old pin must accept it (so the
probe discriminates); pristine documents must pack to the shipped aem.bin.
Usage: parent_bodykey_probe.py <pin_eq work dir>
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

WORK = Path(sys.argv[1])


def packer(side):
    path = WORK / side / "tree/protocol-processor/hdl/aecp/desc/gen_desc_image.py"
    spec = importlib.util.spec_from_file_location("gdi_" + side, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mutate(doc, kind):
    """Rewrite only the body's own type or index bytes (bytes 0..3) of the
    last descriptor of a multi-instance type. The directory key, name binding
    and length are unchanged, so only a body/key comparison can refuse it."""
    by_type = {}
    for i, d in enumerate(doc["descriptors"]):
        by_type.setdefault((str(d.get("configuration", 0)), str(d["type"])), []).append(i)
    for key, idxs in by_type.items():
        if len(idxs) >= 2:
            out = copy.deepcopy(doc)
            d = out["descriptors"][idxs[-1]]
            body = bytearray.fromhex(d["bytes"])
            if kind == "index":
                body[2] ^= 0x01          # body index high byte flipped
            else:
                body[0] ^= 0x01          # body type high byte flipped
            d["bytes"] = body.hex()
            return out, (f"{kind}: body bytes of type {key[1]} index "
                         f"{d.get('index', 0)} altered")
    raise SystemExit("no multi-instance type")


fail = 0
mods = {side: packer(side) for side in ("old", "new")}
for run in sorted((WORK / "new/run").iterdir()):
    doc = json.loads((run / "aem.json").read_text())
    shipped = (run / "aem.bin").read_bytes()
    for side, mod in mods.items():
        img, _ = mod.build(copy.deepcopy(doc), 576)
        same = img == shipped
        print(f"{run.name} {side}: pristine packs to shipped aem.bin: {same}")
        fail |= not same
        for kind in ("type", "index"):
            bad, what = mutate(doc, kind)
            try:
                mod.build(bad, 576)
                res = "ACCEPTED"
            except mod.ImageError as exc:
                res = f"REFUSED ({exc})"
            print(f"  {side} mismatch [{what}]: {res}")
            if side == "new" and not res.startswith("REFUSED"):
                fail = 1
            if side == "old" and res.startswith("REFUSED"):
                print("  (old pin already refuses: probe not discriminating)")
                fail = 1
print("RESULT:", "FAIL" if fail else
      "new pin refuses every planted body/key mismatch; pristine images unchanged")
sys.exit(fail)
