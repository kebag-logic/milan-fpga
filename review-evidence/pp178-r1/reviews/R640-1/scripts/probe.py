#!/usr/bin/env python3
"""Reviewer fault probes for PR #180 (E_SCFG): each probe copies hdl/, tb/common/
and tb/pp_top/ of a source tree into its own scratch directory, applies exact
string edits (each old text must occur exactly once), builds the default
tb/pp_top bench and runs the named sections. The source tree is never written.

Usage: probe.py --src TREE --out DIR --verilator V [--only NAME ...]
"""
import argparse
import shutil
import subprocess
from pathlib import Path

UCODE = "hdl/aecp/ucode/gen_ucode.py"

PROBES = {
    # a real change must still notify: skip NOTIFY_ENQ unconditionally
    "never_notify": ([(UCODE, "    u('BR_STATUS', cnd=2, imm=E_SCFG + 22),\n",
                       "    u('BRANCH', imm=E_SCFG + 22),\n")],
                     [["--notify-only"]]),
    # the dynamic-store arm of the no-change compare reads a wrong value:
    # only NP1c (stored index) may fail
    "store_arm_misread": ([(UCODE, "    u('READ_ST', rd=6, imm=RGN_DYN + SEL_CFG),\n",
                            "    u('MOVE', rd=6, ra=0, imm=0x7FFF),\n")],
                          [["--notify-only"]]),
    # the image arm of the no-change compare reads a wrong value:
    # only NP1a (image index) may fail
    "image_arm_misread": ([(UCODE, "    u('READ_ST', rd=6, imm=RGN_DATA + ENT_CURCFG_LANE),\n",
                            "    u('MOVE', rd=6, ra=0, imm=0x7FFF),\n")],
                          [["--notify-only"]]),
    # the base generator (processor main 22c139a4) against the head bench
    "base_generator": ("BASE", [["--notify-only"], []]),
    # ...the same, limited to the sections that hold the new checks (NP, AX)
    "base_generator_sections": ("BASE", [["--notify-only"], ["--aecp-dispatch-only"]]),
    # the range check back on the BAD_ARGUMENTS arm, full default run: the
    # updated W18d/W18d2 must fail beside SC1/SC2
    "range_bad_default": ([(UCODE, "      cnd=REL_LT, imm=E_SCFGNSD),\n",
                            "      cnd=REL_LT, imm=E_SCFGBAD),\n")],
                          [[]]),
    # the head as is, same harness: the probe positive control
    "control": ([], [["--notify-only"], ["--aecp-dispatch-only"]]),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--base-ucode", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    rc_all = 0
    for name, (edits, runs) in PROBES.items():
        if a.only and name not in a.only:
            continue
        tree = a.out / ("tree-" + name)
        if tree.exists():
            shutil.rmtree(tree)
        for parts in (("hdl",), ("tb", "common"), ("tb", "pp_top")):
            shutil.copytree(a.src.joinpath(*parts), tree.joinpath(*parts),
                            ignore=shutil.ignore_patterns("obj_*", "*.hex", "__pycache__"))
        if edits == "BASE":
            shutil.copyfile(a.base_ucode, tree / UCODE)
        else:
            for path, old, new in edits:
                f = tree / path
                text = f.read_text()
                assert text.count(old) == 1, f"{name}: edit text occurs {text.count(old)} times"
                f.write_text(text.replace(old, new))
        log = a.out / f"{name}.log"
        with log.open("w") as s:
            b = subprocess.run(["make", "-C", str(tree / "tb" / "pp_top"), "gsi-build",
                                "VERILATOR=" + a.verilator], stdout=s, stderr=subprocess.STDOUT)
            s.write(f"\n## build rc={b.returncode}\n")
            s.flush()
            for argv in runs:
                if b.returncode != 0:
                    break
                r = subprocess.run(["./obj_dir/Vpp_top_sim", *argv],
                                   cwd=tree / "tb" / "pp_top", stdout=s, stderr=subprocess.STDOUT)
                s.write(f"\n## run {' '.join(argv) or '(default)'} rc={r.returncode}\n")
                s.flush()
        fails = [l for l in log.read_text().splitlines() if l.startswith("FAIL")]
        tallies = [l for l in log.read_text().splitlines()
                   if l.startswith("[build") or l.startswith("## ")]
        print(f"== {name}")
        for l in tallies + fails:
            print("   " + l)
        shutil.rmtree(tree / "tb" / "pp_top" / "obj_dir", ignore_errors=True)
    return rc_all


if __name__ == "__main__":
    raise SystemExit(main())
