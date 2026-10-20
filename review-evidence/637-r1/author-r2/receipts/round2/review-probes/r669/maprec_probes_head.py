#!/usr/bin/env python3
"""Reviewer probes for #637 at the reviewed head: plant one defect each in a
COPY of hdl/milan/milan_datapath.sv, in arms of the map restore that the
[MAPREC] section has no planted control for, build the dynmap leg through
its own Makefile recipe (DP_SRC and DYNMAP_MDIR overridden), and record the
leg's tally.

A probe that leaves "checks: N   failures: 0" is a SURVIVOR: the leg cannot
see that defect. Nothing in the source tree is modified.

usage: maprec_probes.py TREE OUTDIR plant      # write the mutant copies
       maprec_probes.py TREE OUTDIR build NAME # build one (VERILATOR env)
       maprec_probes.py TREE OUTDIR run NAME   # run one, write NAME.log/.rc
       maprec_probes.py TREE OUTDIR summary
"""
import os
import re
import subprocess
import sys
from pathlib import Path

PROBES = {
    # a framed, crc-clean record the ADD rule refuses must put the reset set
    # back (amr_fsm AS_EEND step 2); the mutant leaves the port EMPTY
    "no_putback": [(
        "            if (!amr_ok_r) amr_pb_r <= amr_pb_r | amr_rmask_w;\n",
        "            if (1'b0) amr_pb_r <= amr_pb_r | amr_rmask_w;\n")],
    # the hole rule: a mapping after an UNUSED entry is malformed
    "no_hole_rule": [("amr_malformed_r <= 1'b1;", "amr_malformed_r <= 1'b0;")],
    # layout_version and record_id are not judged
    "no_layout_id": [("          if (!amr_hframe_r || !amr_hid_r || (amr_hcrc_r != amr_crc_r)\n",
                      "          if (!amr_hframe_r || 1'b0 || (amr_hcrc_r != amr_crc_r)\n")],
    # an entry outside every ADD range is silently dropped, not refused
    "no_range_refuse": [(
        "                    //! outside every range an ADD accepts\n"
        "                    amr_refuse_r <= 1'b1;",
        "                    //! outside every range an ADD accepts\n"
        "                    amr_refuse_r <= 1'b0;")],
    # one cluster, two mappings: the later one silently wins
    "no_dup_cluster": [(
        "                          amr_refuse_r <= 1'b1;   //! one cluster, two mappings",
        "                          amr_refuse_r <= 1'b0;   //! one cluster, two mappings")],
    # a D3 pass-0 abort (DEFAULTS with cause != 0, restore_rb 0) still
    # restores the maps
    "restore_on_pass0_defaults": [(
        "(pp_restore_rb_w || (pp_rs_cause_w != 3'd0))", "(pp_restore_rb_w)")],
}

DP_REL = "hdl/milan/milan_datapath.sv"
SUITE_REL = "tb/verilator/milan_dp"


def plant(tree: Path, out: Path) -> int:
    text = (tree / DP_REL).read_text()
    out.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name, edits in PROBES.items():
        t = text
        for pat, rep in edits:
            n = t.count(pat)
            if n != 1:
                print(f"[FAIL] {name}: pattern found {n} times")
                bad += 1
                break
            t = t.replace(pat, rep)
        else:
            (out / f"milan_datapath_{name}.sv").write_text(t)
            print(f"[ok] planted {name}")
    return 1 if bad else 0


def build(tree: Path, out: Path, name: str) -> int:
    suite = tree / SUITE_REL
    dp = out / f"milan_datapath_{name}.sv" if name != "clean" else tree / DP_REL
    mdir = out / f"obj_{name}"
    cmd = ["make", "-s", "-j8", "-C", str(suite), "-o", "ltn_rom.hex", "-o",
           "ucode.hex", "dynmap-build", f"DP_SRC={dp}", f"DYNMAP_MDIR={mdir}",
           f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}"]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    (out / f"{name}.build.log").write_text(r.stdout[-4000:] + r.stderr[-4000:])
    ok = r.returncode == 0 and (mdir / "Vmilan_dp_dynmap").is_file()
    print(f"{name}: build rc {r.returncode}{'' if ok else ' (no executable)'}")
    return 0 if ok else 1


def run(tree: Path, out: Path, name: str) -> int:
    exe = out / f"obj_{name}" / "Vmilan_dp_dynmap"
    r = subprocess.run([str(exe)], cwd=str(tree / SUITE_REL),
                       capture_output=True, text=True, check=False)
    (out / f"{name}.log").write_text(r.stdout + r.stderr)
    (out / f"{name}.rc").write_text(f"{r.returncode}\n")
    return 0


def summary(out: Path) -> int:
    for name in ["clean", *PROBES]:
        log = out / f"{name}.log"
        if not log.is_file():
            print(f"{name}: NOT RUN")
            continue
        text = log.read_text()
        m = re.search(r"checks: (\d+)\s+failures: (\d+)", text)
        rc = (out / f"{name}.rc").read_text().strip()
        if not m:
            print(f"{name}: rc {rc}, no tally (a crash is not a catch)")
            continue
        fails = int(m.group(2))
        if name == "clean":
            verdict = "PASS" if fails == 0 and rc == "0" else "FAIL"
        else:
            verdict = "CAUGHT" if fails > 0 else "SURVIVED"
        failed = [ln.strip() for ln in text.splitlines() if ln.lstrip().startswith("[FAIL")]
        print(f"{name}: rc {rc}, checks {m.group(1)}, failures {fails}: {verdict}")
        for ln in failed[:5]:
            print(f"    {ln}")
    return 0


def main() -> int:
    tree, out, verb = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    if verb == "plant":
        return plant(tree, out)
    if verb == "build":
        return build(tree, out, sys.argv[4])
    if verb == "run":
        return run(tree, out, sys.argv[4])
    if verb == "summary":
        return summary(out)
    return 2


if __name__ == "__main__":
    sys.exit(main())
