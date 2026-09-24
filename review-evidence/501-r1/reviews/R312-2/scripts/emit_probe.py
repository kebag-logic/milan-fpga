#!/usr/bin/env python3
"""[R312] probe: emit the complete KLJ2 image of every shipped shape from the
scripts of a given tree (base overlay or head) and print per-record rows and
the image SHA-256. Usage: emit_probe.py <tree_root> <shadow_sv_path>.
The shadow path override only replaces the donor-file lookup, which needs a
git index; the donor pin is identical at base and head."""
import hashlib, json, sys, tempfile
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); shadow = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import nvm_shape
nvm_shape.shadow_path = lambda: shadow
from nvm_contract import Shape, Donor, Ident, REC_HDR
from nvm_klj2 import frame_record, klj2_assemble, payload_bytes
import check_nvm_record_space as g
out = {}
for cfg in sorted((tree / "configs").glob("endstation_*.yaml")):
    with tempfile.TemporaryDirectory() as t:
        names, dc, spi, spo = nvm_shape.build(cfg, Path(t))
    sh = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    donor = Donor(base=nvm_shape.binding_base(), layout=nvm_shape.layout_version())
    recs = nvm_shape.inventory(sh, donor.base)
    frames = {r: frame_record(r, payload_bytes(gr, i, r, p), donor.layout)
              for gr, i, r, p, _b in recs if r is not None}
    blob, offs = klj2_assemble(frames, donor, Ident(7, 0x0011223344556677, 0x8899AABBCCDDEEFF))
    rows = sorted((r, offs[r], REC_HDR + p, p, gr, i) for gr, i, r, p, _b in recs)
    out[cfg.stem] = {"sha256": hashlib.sha256(blob).hexdigest(), "imglen": len(blob),
                     "nrec": len(rows), "top": max(r[0] for r in rows), "rows": rows}
    print(f"{cfg.stem}: imglen={len(blob)} nrec={len(rows)} top=0x{out[cfg.stem]['top']:02X} sha256={out[cfg.stem]['sha256']}")
json.dump(out, open(sys.argv[3], "w"), indent=0)
