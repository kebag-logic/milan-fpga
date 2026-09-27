#!/usr/bin/env python3
"""Round-2 parent-side mutants of the new amap_edit_live_wr_p derivation.

Usage: r329_dp_mutants.py <tree> <outdir> [mutant ...]

Each mutant rewrites the one amap_edit_live_wr_p assign in a COPY of
hdl/milan/milan_datapath.sv (the store's own write branches are untouched),
substitutes it into the pp_shadow source list and runs the same two legs and
verdict rules as the unchanged round-1 campaign (imported from
r329_mutants.py). The shipping datapath is verified byte-identical after.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r329_mutants as m  # noqa: E402

ANCHOR = ("      && (amap_edit_in_change_w || amap_edit_out_change_w);")
MUTANTS = {
    "D1_pulse_no_out_change": "      && amap_edit_in_change_w;",
    "D2_pulse_no_in_change": "      && amap_edit_out_change_w;",
    "D3_pulse_any_phase5_record": "      && 1'b1;",
}


def main() -> None:
    tree = Path(sys.argv[1]).resolve()
    outdir = Path(sys.argv[2]).resolve()
    chosen = sys.argv[3:] or list(MUTANTS)
    outdir.mkdir(parents=True, exist_ok=True)
    tb = tree / "tb/verilator/pp_shadow"
    dp = tree / "hdl/milan/milan_datapath.sv"
    before = hashlib.sha256(dp.read_bytes()).hexdigest()
    original = dp.read_text()
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"],
                             cwd=tb, check=True, capture_output=True, text=True)
    srcs = [(tb / p).resolve() for p in listing.stdout.split()]
    assert srcs.count(dp) == 1, "expected exactly one shipping datapath"
    with (outdir / "RESULTS.txt").open("a") as res:
        res.write(f"# shipping milan_datapath.sv sha256 {before}\n")
        for name in chosen:
            if original.count(ANCHOR) != 1:
                res.write(f"{name:28s} REFUSED anchor count {original.count(ANCHOR)}\n")
                continue
            mdir = outdir / "src" / name / "hdl" / "milan"
            mdir.mkdir(parents=True, exist_ok=True)
            mut = mdir / "milan_datapath.sv"
            mut.write_text(original.replace(ANCHOR, MUTANTS[name]))
            use = [mut if p == dp else p for p in srcs]
            for leg in ("dyn", "static"):
                line = m.run_leg(tb, outdir, name, leg, use)
                res.write(line)
                res.flush()
                print(line, end="", flush=True)
        after = hashlib.sha256(dp.read_bytes()).hexdigest()
        res.write(f"# shipping datapath unchanged after campaign: {after == before}\n")


if __name__ == "__main__":
    main()
