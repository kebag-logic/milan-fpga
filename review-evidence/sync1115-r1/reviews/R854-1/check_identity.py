#!/usr/bin/env python3
"""Derive two split AEM images in memory and inspect independent field offsets."""
import hashlib
import json
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/"sw/builder"))
import endstation_builder as b
for name in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    cfg=b.with_placement(b.load_config(str(root/"configs"/(name+".yaml"))),"split")
    image=b._entity_model_image(cfg,b.emit_aem_overlay(cfg))
    blob=image["aem_desc.bin"]
    row=next(x.split() for x in image["aem_desc.map"].splitlines() if "0x0009" in x)
    at=int(row[6],16)
    d=blob[at:at+102]
    assert d[:2]==bytes.fromhex("0009")
    assert d[70:76]==bytes.fromhex("024b4c4b4c01")
    assert d[78:86]==bytes.fromhex("024b4cfffe4b4c01")
    assert d[90]==0x22
    args=b.gptp_ucode_args(cfg)
    assert args[args.index("--clock-accuracy")+1].lower()=="0x22"
    assert args[args.index("--mac")+1].lower()=="0x024b4c4b4c01"
    print(json.dumps(dict(config=name,placement=cfg["control"]["placement"],gptp_args=args,
          aem_sha256=hashlib.sha256(blob).hexdigest(),avb_offset=at,
          mac=d[70:76].hex(),clock_identity=d[78:86].hex(),clock_accuracy=hex(d[90]))))
print("PASS both split AEM byte fields and fabric engine arguments")
