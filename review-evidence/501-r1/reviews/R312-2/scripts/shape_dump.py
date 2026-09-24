#!/usr/bin/env python3
"""[R312] probe: dump each shipped shape's output ports, derived map entries,
record inventory and image figures. Run from the repository root."""
import sys, tempfile, math
from pathlib import Path
sys.path.insert(0, "scripts")
from nvm_contract import Shape, MAP_ENTRY
from nvm_shape import build, inventory, output_map_entries, commit_worst_ms, firmware_constants, binding_base, layout_version
from nvm_contract import Donor
import nvm_contract, inspect
for cfg in sorted(Path("configs").glob("endstation_*.yaml")):
    with tempfile.TemporaryDirectory() as t:
        names, dc, spi, spo = build(cfg, Path(t))
    sh = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    print(f"== {cfg.stem} STREAM_OUTPUT={dc.get('STREAM_OUTPUT')} STREAM_INPUT={dc.get('STREAM_INPUT')} SPO={dc.get('STREAM_PORT_OUTPUT')} SPI={dc.get('STREAM_PORT_INPUT')}")
    for p in spo:
        print(f"   OUT port {p['index']} mode={p.get('map_mode')} clusters={p['clusters']} entries={output_map_entries(sh,p)}")
    for p in spi:
        print(f"   IN  port {p['index']} mode={p.get('map_mode')} clusters={p['clusters']}")
    recs = inventory(sh, binding_base())
    mo = [(g,i,r,pl) for g,i,r,pl,_b in recs if g=="MAPS_OUT"]
    print("   MAPS_OUT recs:", [(i, hex(r), pl) for g,i,r,pl in mo])
    body = sum(8+pl for _g,_i,_r,pl,_b in recs); body += (-body)%4
    print(f"   nrec={len(recs)} top=0x{max(r for *_ ,r,_p,_b in [(g,i,r,p,b) for g,i,r,p,b in recs]):02X} body={body} image={40+body+4} worst={commit_worst_ms(40+body+4):.4f}")
