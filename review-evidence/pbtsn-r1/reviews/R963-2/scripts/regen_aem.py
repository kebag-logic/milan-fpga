# Usage: python3 -I regen_aem.py <milan-fpga checkout> <config.yaml>
# Generates the AEM image with milan-fpga's endstation builder and prints one line per descriptor,
# "type index length hex", type and index read from the descriptor's own header, then the CRC-32
# and the hash-derived model ID on stderr.
import struct, sys, zlib
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
import endstation_builder as b
cfg = b.load_config(sys.argv[2])
overlay = b.emit_aem_overlay(cfg)
blob = b._entity_model_image(cfg, overlay)["aem_desc.bin"]
rows = struct.unpack_from(">H", blob, 8)[0]
table = struct.unpack_from(">I", blob, 12)[0]
out = []
for r in range(rows):
    _cfg, _type, count, length, offset, _name, stride = struct.unpack_from(">HHHHIHH", blob, table + 16 * r)
    for i in range(count):
        d = blob[offset + i * stride: offset + i * stride + length]
        out.append((int.from_bytes(d[0:2], "big"), int.from_bytes(d[2:4], "big"), d))
order = [0, 1, 2, 5, 6, 9, 10, 12, 13, 14, 15, 20, 23, 26, 36]
out.sort(key=lambda x: (order.index(x[0]) if x[0] in order else 99, x[1]))
crc = 0
for t, i, d in out:
    print(f"{t} {i} {len(d)} {d.hex()}")
    crc = zlib.crc32(d, crc)
entity = [d for t, i, d in out if t == 0][0]
sys.stderr.write(f"descriptors {len(out)} octets {sum(len(d) for _, _, d in out)} crc32 0x{crc:08x} model_id 0x{entity[12:20].hex()}\n")
