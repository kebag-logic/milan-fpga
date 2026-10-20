"""Reproduce the four added record edits and independently grade frame terms."""
import binascii
import os
from pathlib import Path
import struct
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch" / "record-terms"
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
sets = {
    0x60: [(0, 6, 0, 0), (0, 0, 3, 0), (0, 1, 5, 0)],
    0x70: [(0, 0, 7, 0), (0, 4, 2, 0)],
}
for tag, rid, offset, value, expected_bad in [
    ("crc", 0x60, 13, 4, "crc"),
    ("layout", 0x60, 2, 3, "layout"),
    ("id", 0x70, 3, 0x71, "id"),
    ("magic", 0x70, 0, 0x18, "magic"),
]:
    # This shape has eight input clusters and seventeen output clusters.
    capacity = 8 if rid == 0x60 else 17
    payload = b"".join(struct.pack(">HHHH", *v) for v in sets[rid])
    payload += b"\xff" * (capacity * 8 - len(payload))
    out = scratch / (tag + ".txt")
    result = subprocess.run([
        sys.executable, str(root / "tb/verilator/milan_dp/gen_nvm_window.py"),
        str(root / "configs/endstation_ax7101_1x1_tdm8.yaml"), str(out),
        "--record", f"{rid:#x}={payload.hex()}",
    ], env=env, cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    lines = out.read_text().splitlines()
    records = [line.split() for line in lines if line.startswith("record ")]
    assert len(records) == 1 and int(records[0][1], 0) == rid
    off, plen = map(int, records[0][2:])
    area = bytearray.fromhex(next(l[5:] for l in lines if l.startswith("area ")))
    assert plen == capacity * 8
    assert all(b == 255 for b in area[:off])
    # Container alignment padding may be zero; all other record spans are erased.
    tail = area[off + 8 + plen:]
    assert all(b == 255 for b in tail.rstrip(b"\0"))
    area[off + offset] = value
    rec = area[off:off + 8 + plen]
    if offset < 8:
        rec[6:8] = binascii.crc_hqx(rec[:6] + rec[8:], 0xffff).to_bytes(2, "big")
    checks = {
        "magic": rec[:2] == b"\x17\x22",
        "layout": rec[2] == 2,
        "id": rec[3] == rid,
        "length": int.from_bytes(rec[4:6], "big") == plen,
        "crc": int.from_bytes(rec[6:8], "big") ==
               binascii.crc_hqx(rec[:6] + rec[8:], 0xffff),
    }
    bad = [k for k, good in checks.items() if not good]
    assert bad == [expected_bad], (tag, checks)
    print(f"PASS {tag}: sole record {rid:#x}, payload {plen}, failing term {bad[0]}")
print("PASS four windows; independent CRC computation; no RTL execution claimed")
