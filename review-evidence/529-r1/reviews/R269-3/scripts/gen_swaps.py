#!/usr/bin/env python3
"""R269-3: the 45 pairwise exchanges of the ten KL_crf_rx tally bindings.

usage: gen_swaps.py <exact-head tree> <out dir>

Inside the crf_rx instance only, the root wires of two tally ports are
exchanged; each wire must occur exactly once in the instance. Writes
<out>/S_<a>__<b>/milan_datapath.sv and <out>/SWAPS.tsv (name, wire a, quadlet
a, wire b, quadlet b).
"""
import itertools
import pathlib
import sys

# root wire -> (quadlet, Table 5.16 symbol) as REGISTER_MAP's table states it
WIRES = {
    "crf_lockcnt_w": (0, "MEDIA_LOCKED"),
    "crf_unlockcnt_w": (1, "MEDIA_UNLOCKED"),
    "crf_intrcnt_w": (2, "STREAM_INTERRUPTED"),
    "crf_seqerr_w": (3, "SEQ_NUM_MISMATCH"),
    "crf_mrcnt_w": (4, "MEDIA_RESET"),
    "crf_tucnt_w": (5, "TIMESTAMP_UNCERTAIN"),
    "crf_fmterr_w": (8, "UNSUPPORTED_FORMAT"),
    "crf_latecnt_w": (9, "LATE_TIMESTAMP"),
    "crf_earlycnt_w": (10, "EARLY_TIMESTAMP"),
    "crf_pducnt_w": (11, "FRAMES_RX"),
}


def main():
    tree, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    rtl = (tree / "hdl/milan/milan_datapath.sv").read_text()
    start = rtl.index("  ) crf_rx (\n")
    end = rtl.index("\n  );\n", start)
    block = rtl[start:end]
    for w in WIRES:
        if block.count(f"({w})") != 1:
            sys.exit(f"{w}: not exactly one binding in the crf_rx instance")
    rows = []
    for a, b in itertools.combinations(WIRES, 2):
        swapped = (block.replace(f"({a})", "(@@A@@)")
                        .replace(f"({b})", f"({a})")
                        .replace("(@@A@@)", f"({b})"))
        name = f"S_{a[4:-2]}__{b[4:-2]}"
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "milan_datapath.sv").write_text(rtl[:start] + swapped + rtl[end:])
        rows.append((name, a, WIRES[a][0], WIRES[a][1], b, WIRES[b][0], WIRES[b][1]))
    with open(out / "SWAPS.tsv", "w") as f:
        f.write("name\twire_a\tq_a\tsym_a\twire_b\tq_b\tsym_b\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    print(f"{len(rows)} exchanges written to {out}")


if __name__ == "__main__":
    main()
