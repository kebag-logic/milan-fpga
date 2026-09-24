#!/usr/bin/env python3
"""R308 probe: build and run the milan_dp timed notification leg at the
candidate head, then under nonzero CTLR_DIAG mutants, without touching any
tracked file. Mutated sources and build trees live under SCRATCH.

Usage (from the candidate root's tb/verilator/milan_dp, after
`make ltn_rom.hex ucode.hex`):
  r308_notify_probe.py DRYRUN_LOG VERILATOR SCRATCH RECEIPTS [NAME...]
With NAMEs, only those arms run (each writes <name>-result.json); with the
single NAME `verdict`, nothing is built and the per-arm results are judged.
DRYRUN_LOG is the output of `make -n VERILATOR=<v> VERILATOR_JOBS=8 run`.
"""
import json, shlex, subprocess, sys, time
from pathlib import Path

dryrun, verilator, scratch, receipts = (Path(a) for a in sys.argv[1:5])
HERE = Path.cwd()
ROOT = HERE.parents[2]
LABEL = "[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic"
results = []

lines = dryrun.read_text().replace("\\\n", " ").splitlines()
recipes = [shlex.split(l) for l in lines if "--Mdir obj_notify" in l]
assert len(recipes) == 1, f"expected one notify recipe, got {len(recipes)}"
base = recipes[0]
assert base[0] == str(verilator), f"recipe does not use the pinned tool: {base[0]}"

MUTANTS = {
    # name: (relative source, exact original line, replacement line)
    "clean": None,
    # the author's arm, reproduced independently
    "m1_tie_01001001": ("hdl/milan/milan_datapath.sv",
                        "  assign aecp_ctlr_diag = 32'd0;",
                        "  assign aecp_ctlr_diag = 32'h01001001;"),
    # reviewer-owned arm: a different injection point (the CSR read decode on
    # the AXI-Lite path) and a different bit (only the old eviction MSB)
    "m2_csr_decode_msb": ("hdl/common/csr/milan_csr.sv",
                          "      A_CTLR_DIAG:  live_mux = i_ctlr_diag;",
                          "      A_CTLR_DIAG:  live_mux = i_ctlr_diag | 32'h8000_0000;"),
    # reviewer-owned arm: the smallest nonzero value (old probe-count LSB)
    "m3_tie_lsb": ("hdl/milan/milan_datapath.sv",
                   "  assign aecp_ctlr_diag = 32'd0;",
                   "  assign aecp_ctlr_diag = 32'd1;"),
}

def run(name, cmd, cwd):
    t = time.monotonic()
    with (receipts / f"{name}.log").open("w") as log:
        rc = subprocess.run(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    rec = {"step": name, "rc": rc, "seconds": round(time.monotonic() - t, 1),
           "command": shlex.join(cmd)}
    results.append(rec)
    print(f"{name}: rc={rc} {rec['seconds']}s", flush=True)
    return rc

selected = sys.argv[5:] or list(MUTANTS)
for name, mut in MUTANTS.items():
    if name not in selected:
        continue
    cmd = base.copy()
    mdir = scratch / f"obj_{name}"
    cmd[cmd.index("--Mdir") + 1] = str(mdir)
    if mut:
        rel, before, after = mut
        text = (ROOT / rel).read_text()
        assert text.count(before) == 1, f"{name}: anchor not unique in {rel}"
        mfile = scratch / f"src_{name}" / Path(rel).name
        mfile.parent.mkdir(parents=True, exist_ok=True)
        mfile.write_text(text.replace(before, after))
        idx = [i for i, a in enumerate(cmd) if a.endswith("/" + rel.split("/", 1)[1])]
        if not idx:
            # the CSR file may arrive through an include dir / file list
            idx = [i for i, a in enumerate(cmd) if a.endswith("/" + Path(rel).name)]
        assert len(idx) == 1, f"{name}: {rel} appears {len(idx)} times in the recipe"
        cmd[idx[0]] = str(mfile)
    if run(f"{name}-build", cmd, HERE):
        continue
    rc = run(f"{name}-run", [str(mdir / "Vmilan_dp_notify")], HERE)
    out = (receipts / f"{name}-run.log").read_text().splitlines()
    fails = [l for l in out if "[FAIL]" in l]
    oks = [l for l in out if "[ok]" in l and LABEL in l]
    summ = [l for l in out if l.startswith("checks:")]
    results[-1].update(fails=fails, label_ok=bool(oks), summary=summ)
    (receipts / f"{name}-result.json").write_text(
        json.dumps([r for r in results if r["step"].startswith(name + "-")], indent=2) + "\n")

if selected != ["verdict"]:
    sys.exit(0)
results = [r for n in MUTANTS for r in json.loads((receipts / f"{n}-result.json").read_text())]
ok = True
for r in results:
    if r["step"] == "clean-run":
        ok &= r["rc"] == 0 and r["label_ok"] and r["fails"] == []
    elif r["step"].endswith("-run"):
        ok &= r["rc"] == 1 and len(r["fails"]) == 1 and LABEL in r["fails"][0]
ok &= sum(r["step"].endswith("-run") for r in results) == len(MUTANTS)
print("VERDICT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
