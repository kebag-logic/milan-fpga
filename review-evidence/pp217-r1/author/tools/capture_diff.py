#!/usr/bin/env python3
"""capture_diff.py <base-dir> <head-dir>: compare the twin's fabric and split captures (obj_twin/fabric.json,
split.json) of a base-pinned and a head-pinned copy, frame by frame: count, each frame's ms and every byte.
Prints each difference; for a READ_DESCRIPTOR(ENTITY) response it names the descriptor's available_index
(descriptor octet 36, wire bytes 78..81). Exit 0 always; the report is the result."""
import json, sys
from pathlib import Path


def load(d: Path, name: str):
    return json.loads((d / "tb/verilator/milan_dp/obj_twin" / name).read_text())["frames"]


def main() -> int:
    base, head = Path(sys.argv[1]), Path(sys.argv[2])
    for name in ("fabric.json", "split.json"):
        b, h = load(base, name), load(head, name)
        print(f"{name}: base {len(b)} frames, head {len(h)} frames")
        diffs = 0
        for i, (fb, fh) in enumerate(zip(b, h)):
            if fb["ms"] != fh["ms"]:
                diffs += 1
                print(f"  frame {i}: ms base {fb['ms']} head {fh['ms']}")
            xb, xh = bytes.fromhex(fb["hex"]), bytes.fromhex(fh["hex"])
            if xb != xh:
                diffs += 1
                if len(xb) != len(xh):
                    print(f"  frame {i} at ms {fb['ms']}: length base {len(xb)} head {len(xh)}")
                    continue
                at = [k for k in range(len(xb)) if xb[k] != xh[k]]
                print(f"  frame {i} at ms {fb['ms']}: wire bytes {at} differ")
                if all(78 <= k <= 81 for k in at):
                    ib = int.from_bytes(xb[78:82], "big")
                    ih = int.from_bytes(xh[78:82], "big")
                    print(f"    all inside descriptor octets 36..39 (available_index): base {ib}, head {ih}")
        print(f"  {diffs} difference(s) in time or bytes; frame counts equal: {len(b) == len(h)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
