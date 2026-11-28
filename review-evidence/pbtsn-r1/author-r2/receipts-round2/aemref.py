import struct, sys
from pathlib import Path
root = Path(sys.argv[1]); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as b
cfg = b.load_config(sys.argv[2]); ov = b.emit_aem_overlay(cfg)
blob = b._entity_model_image(cfg, ov)["aem_desc.bin"]
n = struct.unpack_from(">H", blob, 8)[0]; off = struct.unpack_from(">I", blob, 12)[0]
for r in range(n):
    cfgi, t, cnt, ln, doff, nm, stride = struct.unpack_from(">HHHHIHH", blob, off + r*16)
    for i in range(cnt):
        d = blob[doff + i*stride: doff + i*stride + ln]
        print(f"{int.from_bytes(d[0:2],'big')} {int.from_bytes(d[2:4],'big')} {len(d)} {d.hex()}")
