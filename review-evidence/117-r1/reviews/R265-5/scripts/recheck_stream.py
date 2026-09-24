#!/usr/bin/env python3
"""Recheck the step 3 stream rows (cycles 4 to 6) from raw tap and console files.

Usage: recheck_stream.py <bench-a202/bench directory>

Reuses the clock placement of recompute_step3.py (same directory). For each
bound cycle: CRF PDUs the DUT sent (tap port 3, AVTP subtype 0x04), the first
with tu=1 at the loss, how many carried tu=1, when emission ended, the first
PDU after the return and whether every later PDU has tu=0; from the console,
the CRFT_CTRL word (the only mem_read whose value toggles between 0x3 and
0x3002E3) and when it changed.
"""
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import recompute_step3 as r3  # noqa: E402


def main():
    base = Path(sys.argv[1])
    for n in (4, 5, 6):
        cdir = base / f"cycle{n}"
        off = r3.offsets(cdir)
        ps = (cdir / "powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1)) - off["pi"]
        # tap with the CRF tu bit
        raw = (cdir / f"tap-c{n}.pcap").read_bytes()
        recs, _fit = r3.tap(cdir, n)
        # recompute per-record tu by walking the file again in the same order
        tus = []
        o = 24
        while o + 16 <= len(raw):
            s, us, incl, _ = struct.unpack("<IIII", raw[o:o + 16])
            o += 16
            pkt = raw[o:o + incl]
            o += incl
            if len(pkt) < 42:
                continue
            tag, _l, port = struct.unpack("<III", pkt[:12])
            w5 = struct.unpack("<I", pkt[20:24])[0]
            if tag != 6 or port not in (2, 3) or w5 != incl - 28:
                continue
            fr = pkt[28:]
            et = struct.unpack(">H", fr[12:14])[0]
            body = fr[18:] if et == 0x8100 else fr[14:]
            if et == 0x8100:
                et = struct.unpack(">H", fr[16:18])[0]
            tus.append((port, et == 0x22F0 and body[0] == 0x04, body[1] & 1 if len(body) > 1 else 0))
        assert len(tus) == len(recs)
        crf = [(s - off["ubuntu-server"] - t_off, tu) for (s, p, k), (p2, is_crf, tu)
               in zip(recs, tus) if p == 3 and is_crf]
        loss = [(t, tu) for t, tu in crf if 0 < t < 10]
        first_tu1 = next(t for t, tu in loss if tu)
        n_tu1 = sum(tu for _, tu in loss)
        end = max(t for t, _ in loss)
        ret = [(t, tu) for t, tu in crf if t > 10]
        first_ret = ret[0][0] if ret else None
        tu1_after = sum(tu for _, tu in ret)
        # console CRFT_CTRL
        text = (cdir / "console.txt").read_text(errors="replace")
        vals = []
        for blk in text.split("### ")[1:]:
            m = re.match(r"(\S+) cmd='mem_read (0x[0-9a-f]+) 4'", blk)
            if not m:
                continue
            d = re.search(r"0x[0-9a-f]+\s+((?:[0-9a-f]{2} ){4})", blk)
            if not d:
                continue
            v = int.from_bytes(bytes.fromhex(d.group(1).replace(" ", "")), "little")
            vals.append((r3.iso(m.group(1)) - t_off, m.group(2), v))
        ctrl = [(t, v) for t, a, v in vals if v in (0x3, 0x3002E3)]
        addrs = {a for t, a, v in vals if v == 0x3002E3}
        ctrl = [(t, v) for t, a, v in vals if a in addrs]
        drop = next(t for t, v in ctrl if t > 0 and v == 0x3)
        relic = next(t for t, v in ctrl if t > 10 and v == 0x3002E3)
        print(f"cycle {n}: CRF PDUs {len(crf)}; loss: first tu=1 {first_tu1:.2f} s, tu=1 PDUs {n_tu1}, "
              f"emission end {end:.2f} s; licence drop (CRFT_CTRL {sorted(addrs)} -> 0x3) {drop:.2f} s; "
              f"relicensed {relic:.2f} s; first PDU after return {first_ret:.2f} s; tu=1 after return {tu1_after}")


if __name__ == "__main__":
    main()
