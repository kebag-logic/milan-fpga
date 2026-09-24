#!/usr/bin/env python3
"""Reviewer probe (R313-1): dump one tree's own NVM figures as JSON.

Usage: python3 tree_figures.py <tree-root> <out.json>

Imports the TREE's own scripts/nvm_* modules (so base and head are each
measured by their own code), builds the two AX7101 shapes through the tree's
builder, assembles the complete KLJ2 image exactly as --emit-record-table
does, and records: full-image SHA-256, record table, decoded MAPS_OUT payload
lengths, generated firmware constants, and the shape counts the figures
derive from. No file in the tree is written; builds go to a temp dir.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
from nvm_contract import Donor, Shape, REC_HDR  # noqa: E402
from nvm_klj2 import frame_record, klj2_assemble, klj2_decode, payload_bytes  # noqa: E402
import nvm_shape  # noqa: E402

try:
    from nvm_contract import Ident
except ImportError:  # pragma: no cover
    from nvm_klj2 import Ident

donor = Donor(base=nvm_shape.binding_base(), layout=nvm_shape.layout_version())
ident = Ident(seq=7, entity_id=0x0011223344556677, model_id=0x8899AABBCCDDEEFF)
out = {"tree": str(tree), "donor_base": donor.base, "layout": donor.layout}
for stem in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    cfg = tree / "configs" / f"{stem}.yaml"
    with tempfile.TemporaryDirectory(prefix="r313fig.") as tmp:
        names, dc, spi, spo = nvm_shape.build(cfg, Path(tmp))
    shape = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    recs = nvm_shape.inventory(shape, donor.base)
    live = [(g, i, r, p) for g, i, r, p, _b in recs if r is not None]
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), donor.layout)
              for g, i, r, p in live}
    blob, offs = klj2_assemble(frames, donor, ident)
    expect = {(g, i): p for g, i, _r, p in live}
    verdict, applied = klj2_decode(blob, donor, ident, expect)
    fw = nvm_shape.firmware_constants(shape, donor)
    out[stem] = {
        "names": names,
        "dc": {k: v for k, v in dc.items() if isinstance(v, int)},
        "spi": [{"index": p["index"], "clusters": p["clusters"],
                 "map_mode": p.get("map_mode")} for p in spi],
        "spo": [{"index": p["index"], "clusters": p["clusters"],
                 "map_mode": p.get("map_mode")} for p in spo],
        "image_len": len(blob),
        "image_sha256": hashlib.sha256(blob).hexdigest(),
        "nrec": len(frames),
        "top_id": max(frames),
        "records": [[g, i, r, offs[r], REC_HDR + p, p] for g, i, r, p in
                    sorted(live, key=lambda t: t[2])],
        "decode_verdict": verdict,
        "decoded_maps_out_len": {str(i): len(v) for (g, i), v in applied.items()
                                 if g == "MAPS_OUT"},
        "fw_map_consts": {k: v for k, v in fw.items() if "_MAP" in k},
        "commit_worst_ms": nvm_shape.commit_worst_ms(len(blob)),
    }
Path(sys.argv[2]).write_text(json.dumps(out, indent=1, sort_keys=True))
print("wrote", sys.argv[2])
