#!/usr/bin/env python3
"""Reviewer's disposable probes against tb/pp_top: each probe is one exact edit
planted in a private copy of hdl/, tb/common/ and tb/pp_top/ under a scratch
directory; the copy is built and run, and every FAIL line is recorded.
The repository the script reads is never written.

Usage: probe.py --repo R --scratch S --out O --verilator V --mode d3|default NAME...
"""
import argparse, concurrent.futures, json, shutil, subprocess
from pathlib import Path

DYN = "hdl/aecp/KL_aecp_dyn_state.sv"
WRITER = "hdl/aecp/KL_aecp_nvm_writer.sv"
UCODE = "hdl/aecp/ucode/gen_ucode.py"
SCLKS_CHECK = "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_W,       # index < count, else BAD_ARGS\n"
PROBES = {
    # none: the unmutated head, the probe driver's own golden
    "golden": (),
    # the exported index narrowed to its low three bits
    "export_low3": ((DYN, "  assign clk_src_index_o = clksrc_r[0];\n",
                     "  assign clk_src_index_o = {13'd0, clksrc_r[0][2:0]};\n"),),
    # the restore rule reads clock_sources_offset (lane [63:48], 76) as the count
    "restore_reads_offset": ((WRITER, "      lane_accept_w = rval_r[15:0] < sb_rdata_i[47:32];\n",
                              "      lane_accept_w = rval_r[15:0] < sb_rdata_i[63:48];\n"),),
    # the SET range check compares bytes, not words (index low byte < count)
    "sclks_byte_compare": ((UCODE, SCLKS_CHECK,
                            "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_B,       # index < count, else BAD_ARGS\n"),),
    # aecp_dispatch_mutations/sclks-bound-three.patch as an exact edit
    "sclks_bound_three": ((UCODE, "    u('MOVE', rd=9, ra=7, fmt=FMT_W),            # r9 = clock_sources_count\n",
                           "    u('MOVE', rd=9, ra=0, imm=3),                # r9 = clock_sources_count\n"),),
    # the clock-source row's low two bits only (d3_mutants clks_row_two_bits)
    "clks_row_two_bits": ((DYN, "          13'(SEL_CLKSRC_C): begin clksrc_r[cd_ix_w]  <= st_wdata_i[15:0];\n",
                           "          13'(SEL_CLKSRC_C): begin clksrc_r[cd_ix_w]  <= {14'd0, st_wdata_i[1:0]};\n"),),
}

def one(name, a):
    tree = Path(a.scratch) / f"probe-{a.mode}-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for d in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(Path(a.repo) / d, tree / d, ignore=skip)
    for rel, old, new in PROBES[name]:
        p = tree / rel
        t = p.read_text()
        if t.count(old) != 1:
            return {"probe": name, "verdict": "REFUSED", "rel": rel, "count": t.count(old)}
        p.write_text(t.replace(old, new, 1))
    log = Path(a.out) / f"{a.mode}-{name}.log"
    bench = tree / "tb" / "pp_top"
    with log.open("w") as s:
        b = subprocess.run(["make", "gsi-build", "VERILATOR=" + a.verilator], cwd=bench,
                           stdout=s, stderr=subprocess.STDOUT).returncode
        r = None
        if b == 0:
            argv = ["./obj_dir/Vpp_top_sim"] + (["--d3-only"] if a.mode == "d3" else [])
            r = subprocess.run(argv, cwd=bench, stdout=s, stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    fails = [l[6:] for l in text.splitlines() if l.startswith("FAIL: ")]
    tally = [l for l in text.splitlines() if l.startswith("[build default,") or l.startswith("D3: ")]
    shutil.rmtree(tree)
    return {"probe": name, "mode": a.mode, "build_rc": b, "run_rc": r, "tally": tally,
            "failing": len(fails), "d3c_failing": sum(f.startswith("D3C") for f in fails),
            "non_d3c_failing": [f for f in fails if not f.startswith("D3C")], "fails": fails}

def main():
    ap = argparse.ArgumentParser()
    for k in ("--repo", "--scratch", "--out", "--verilator"):
        ap.add_argument(k, required=True)
    ap.add_argument("--mode", choices=("d3", "default"), required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("names", nargs="+")
    a = ap.parse_args()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        res = list(pool.map(lambda n: one(n, a), a.names))
    for r in res:
        print(json.dumps({k: r.get(k) for k in ("probe", "build_rc", "run_rc", "tally", "failing", "d3c_failing")}))
        for f in r.get("non_d3c_failing", [])[:10]:
            print("   non-D3C:", f[:160])
    (Path(a.out) / f"results-{a.mode}-{'-'.join(a.names)}.json").write_text(json.dumps(res, indent=1) + "\n")

if __name__ == "__main__":
    main()
