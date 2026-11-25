#!/usr/bin/env python3
"""The board's own LeaveAll in a budget-harness log: la_window.py LOG [LOG...].

For each LeaveAll timer run-out (`ENTRY <cycle> on_la_timer if<n> <app>`), the commit of that application's first
MRPDU after it that flags LeaveAll (`WIRE <cycle> <if> <channel> <frame hex>`: a VectorHeader whose top three bits
are 1), and the longest work pass (`PASS <n> <start> <..> <cycles>`) and idle run starting within 1 s of the run-out.
Also the longest pass of the whole log, against THE SHARE (200,000 cycles at 100 MHz). Cycles are the bus's (100 MHz).
"""
import re
import sys

SHARE = 200_000
HZ = 100_000_000
ETHERTYPE = {"MSRP": "22ea", "MVRP": "88f5"}


def leave_all(frame_hex: str, app: str) -> bool:
    b = bytes.fromhex(frame_hex)
    if b[12:14].hex() != ETHERTYPE[app]:
        return False
    p, off = b[14:], 1
    msrp = app == "MSRP"
    while off + 2 <= len(p) and (p[off] or p[off + 1]):
        atype, width = p[off], p[off + 1]
        end = off + 4 + int.from_bytes(p[off + 2:off + 4], "big") if msrp else len(p)
        off += 4 if msrp else 2
        while off + 2 <= min(end, len(p)) and (p[off] or p[off + 1]):
            vh = int.from_bytes(p[off:off + 2], "big")
            if vh >> 13 == 1:
                return True
            n = vh & 8191
            off += 2 + width + (n + 2) // 3 + ((n + 3) // 4 if msrp and atype == 3 else 0)
        if not msrp:
            return False
        off = end
    return False


def main():
    for path in sys.argv[1:]:
        text = open(path, errors="replace").read()
        passes = [(int(m[1]), int(m[2])) for m in re.finditer(r"^PASS \d+ (\d+) \d+ (\d+)", text, re.M)]
        wires = [(int(m[1]), m[2]) for m in re.finditer(r"^WIRE (\d+) \d+ \d+ ([0-9a-f]+)", text, re.M)]
        longest = max((c for _, c in passes), default=0)
        last = max((s for s, _ in passes), default=0)
        print(f"== {path.split('/')[-1]}: {len(passes)} passes to {last / HZ:.3f} s; longest {longest:,} cycles "
              f"({'within' if longest <= SHARE else 'OVER'} THE SHARE {SHARE:,})")
        for m in re.finditer(r"^ENTRY (\d+) on_la_timer (if\d+) (\w+)", text, re.M):
            at, app = int(m[1]), m[3]
            sent = next((c for c, f in wires if c > at and leave_all(f, app)), None)
            window = [c for s, c in passes if at <= s <= at + HZ]
            print(f"  {app} {m[2]} leavealltimer at {at / HZ:.3f} s; its LeaveAll MRPDU "
                  + (f"on the wire {(sent - at) / 1e5:.3f} ms later" if sent else "not seen")
                  + f"; {len(window)} passes in the next 1 s, longest {max(window, default=0):,} cycles")


if __name__ == "__main__":
    main()
