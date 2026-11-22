#!/usr/bin/env python3
"""bitheader.py A.bit B.bit: the Xilinx .bit header of two images, field by field, and every differing byte of the
whole file named by the field (or payload region) that holds it.

The header (UG470 / the de-facto .bit layout): a 2-byte length (9), 9 bytes of magic, a 2-byte length (1), then
tagged fields (the length 1 counts the first key), each a 1-byte key, a 2-byte big-endian length and that many bytes (NUL-terminated text):
  'a' design name (Vivado appends ';UserID=...;Version=...' and its own ';SW_CRC=...;SW_HDR_SHA256=...'),
  'b' part, 'c' date, 'd' time,
  'e' a 4-byte big-endian payload length, then the configuration payload (the bytes the device loads).
Also checks two digest hypotheses for the 'a' field's SW_* values against the payload, so the header digests can be
tied to what they cover. Exit 0 when every differing byte is classified."""
import binascii
import hashlib
import sys
from pathlib import Path


def fields(data: bytes):
    """[(key, value_offset, value_bytes)] of the header and the payload offset."""
    n = int.from_bytes(data[0:2], "big")
    pos = 2 + n
    pos += 2  # the 2-byte length 1 whose one byte is the first field's key, 'a'
    out = []
    while True:
        key = chr(data[pos])
        if key == "e":
            length = int.from_bytes(data[pos + 1:pos + 5], "big")
            out.append(("e", pos + 1, data[pos + 1:pos + 5]))
            return out, pos + 5, length
        n = int.from_bytes(data[pos + 1:pos + 3], "big")
        out.append((key, pos + 3, data[pos + 3:pos + 3 + n]))
        pos += 3 + n


NAMES = {"a": "design name", "b": "part", "c": "date", "d": "time", "e": "payload length"}


def describe(path: Path):
    data = path.read_bytes()
    hdr, start, length = fields(data)
    print(f"{path.name}: {len(data)} B, sha256 {hashlib.sha256(data).hexdigest()}")
    for key, off, val in hdr:
        shown = val.rstrip(b"\0").decode(errors="replace") if key != "e" else str(int.from_bytes(val, "big"))
        print(f"  field '{key}' ({NAMES[key]}) bytes {off}..{off + len(val) - 1}: {shown}")
    print(f"  payload bytes {start}..{start + length - 1} ({length} B), file ends at {len(data) - 1}")
    name = dict((k, v) for k, _, v in hdr)["a"].rstrip(b"\0").decode()
    kv = dict(p.split("=", 1) for p in name.split(";")[1:] if "=" in p)
    payload = data[start:start + length]
    checks = {
        "SW_HDR_SHA256 == sha256(payload)": kv.get("SW_HDR_SHA256", "").lower() == hashlib.sha256(payload).hexdigest(),
        "SW_CRC == crc32(payload)": kv.get("SW_CRC", "").lower() == f"{binascii.crc32(payload):08x}",
    }
    for label, ok in checks.items():
        print(f"  {label}: {'yes' if ok else 'no'}")
    return data, hdr, start, length


a_path, b_path = Path(sys.argv[1]), Path(sys.argv[2])
a, ha, sa, la = describe(a_path)
b, hb, sb, lb = describe(b_path)
if len(a) != len(b) or sa != sb or la != lb or [(k, o, len(v)) for k, o, v in ha] != [(k, o, len(v)) for k, o, v in hb]:
    print("LAYOUT DIFFERS: header field offsets/lengths or payload length differ")
    sys.exit(1)
diff = [i for i in range(len(a)) if a[i] != b[i]]
where = {}
for i in diff:
    label = None
    for key, off, val in ha:
        if off <= i < off + len(val):
            label = f"header '{key}' ({NAMES[key]})"
            if key == "a":
                text = val.decode(errors="replace")
                sub = text[:i - off + 1].split(";")[-1].split("=")[0]
                label += f" {sub}"
    if label is None:
        label = "payload" if sa <= i < sa + la else "outside header and payload"
    where.setdefault(label, []).append(i)
print(f"differing bytes: {len(diff)}")
for label, offs in where.items():
    print(f"  {len(offs):4d}  {label}: offsets {offs if len(offs) <= 12 else offs[:6] + ['...'] + offs[-3:]}")
hdr_n = sum(len(v) for k, v in where.items() if k.startswith("header"))
print(f"header bytes differing: {hdr_n}; payload bytes differing: {len(where.get('payload', []))}; "
      f"unclassified: {len(where.get('outside header and payload', []))}")
sys.exit(1 if "outside header and payload" in where else 0)
