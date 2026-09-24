#!/usr/bin/env python3
"""Reviewer probe for #548: build the timed notification leg (obj_notify) from
a plain copy of the exact head, run it clean, then run source mutants that
make CTLR_DIAG (0x6F4) read nonzero, each from a separate temporary source.

Usage:
  notify_probe.py <tree> <recipe.txt> <outdir>

<tree>       a copy of the exact-head working tree (submodules checked out);
             builds and hex files land only inside it.
<recipe.txt> output of `make -n run VERILATOR=verilator VERILATOR_JOBS=8`
             taken in tb/verilator/milan_dp of the exact-head clone.
<outdir>     receives one log per step and results.json.

`verilator` must be first on PATH. Exit 0 only when the clean run passes the
named check with zero failures and every mutant exits 1 with exactly that
check as its only failure.
"""
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

LABEL = "[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic"
DP = "hdl/milan/milan_datapath.sv"
CSR = "hdl/common/csr/milan_csr.sv"
DP_TIE = "  assign aecp_ctlr_diag = 32'd0;"
CSR_MUX = "      A_CTLR_DIAG:  live_mux = i_ctlr_diag;"

# name, file, exact original line, replacement line
MUTANTS = [
    ("m1-dp-01001001", DP, DP_TIE, "  assign aecp_ctlr_diag = 32'h01001001;"),
    ("m2-dp-lsb", DP, DP_TIE, "  assign aecp_ctlr_diag = 32'h00000001;"),
    ("m3-dp-msb", DP, DP_TIE, "  assign aecp_ctlr_diag = 32'h80000000;"),
    ("m4-csr-mux", CSR, CSR_MUX, "      A_CTLR_DIAG:  live_mux = i_ctlr_diag | 32'h00000100;"),
]


def run(out, results, name, cmd, cwd):
    t0 = time.monotonic()
    with (out / f"{name}.log").open("w") as log:
        rc = subprocess.run(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                            check=False).returncode
    results.append({"name": name, "rc": rc, "seconds": round(time.monotonic() - t0, 1),
                    "command": shlex.join(cmd)})
    (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{name}: rc={rc} ({results[-1]['seconds']} s)", flush=True)
    return rc


def verdict(log_path):
    text = log_path.read_text()
    fails = [ln for ln in text.splitlines() if "[FAIL]" in ln]
    oks = [ln for ln in text.splitlines() if "[ok]" in ln and LABEL in ln]
    summary = [ln for ln in text.splitlines() if ln.startswith("checks:")]
    return fails, oks, summary


def main():
    tree, recipe_file, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    tb = tree / "tb/verilator/milan_dp"
    lines = recipe_file.read_text().replace("\\\n", " ").splitlines()
    hexes = [shlex.split(ln) for ln in lines
             if ln.startswith("python3 ") and ln.rstrip().endswith((" ltn_rom.hex", " ucode.hex"))]
    recipes = [shlex.split(ln) for ln in lines if "--Mdir obj_notify" in ln]
    if len(recipes) != 1 or len(hexes) != 2:
        raise SystemExit(f"recipe shape unexpected: {len(recipes)} notify, {len(hexes)} hex")
    recipe = recipes[0]
    results = []
    for i, cmd in enumerate(hexes):
        if run(out, results, f"hex-{i}", cmd, tb):
            return 1
    if run(out, results, "clean-build", recipe, tb):
        return 1
    run(out, results, "clean-run", ["./obj_notify/Vmilan_dp_notify"], tb)
    fails, oks, summary = verdict(out / "clean-run.log")
    ok = results[-1]["rc"] == 0 and not fails and len(oks) == 1
    print(f"clean: rc={results[-1]['rc']} fails={len(fails)} named_ok={len(oks)} {summary}", flush=True)
    for name, rel, before, after in MUTANTS:
        src = (tree / rel).read_text()
        if src.count(before) != 1:
            raise SystemExit(f"{name}: anchor not unique in {rel}")
        work = tree.parent / f"mut-{name}"
        work.mkdir(parents=True, exist_ok=True)
        mfile = work / Path(rel).name
        mfile.write_text(src.replace(before, after))
        cmd = recipe.copy()
        cmd[cmd.index("--Mdir") + 1] = str(work / "obj")
        idx = [i for i, a in enumerate(cmd) if a.endswith("/" + rel)]
        if len(idx) != 1:
            raise SystemExit(f"{name}: source not unique in recipe")
        cmd[idx[0]] = str(mfile)
        if run(out, results, f"{name}-build", cmd, tb):
            ok = False
            continue
        run(out, results, f"{name}-run", [str(work / "obj/Vmilan_dp_notify")], tb)
        mf, _, ms = verdict(out / f"{name}-run.log")
        caught = results[-1]["rc"] == 1 and len(mf) == 1 and LABEL in mf[0]
        print(f"{name}: rc={results[-1]['rc']} fails={len(mf)} caught_exactly={caught} {ms}", flush=True)
        for ln in mf:
            print("   " + ln.strip(), flush=True)
        ok = ok and caught
    print("PROBE PASS" if ok else "PROBE FAIL", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
