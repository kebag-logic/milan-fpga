#!/usr/bin/env python3
"""Probe A (reviewer-owned, disposable): is SET_CONTROL's out-of-range
BAD_ARGUMENTS body graded?

At this head E_SCTRL answers an out-of-range value (neither 0 nor 255) with
BAD_ARGUMENTS through the shared refusal tail, which now carries the IDENTIFY
value in force (06 section 6.8, last sentence of the issue-#53 paragraph).
At the base it answered through the zero-bodied E_BADARG1 stub.

Variants, each in its own scratch copy of hdl/, tb/common and tb/pp_top:
  mutant-suite   the base's zero body restored (the out-of-range arm branches
                 to E_BADARG1 again), bench unmodified, FULL default run of
                 tb/pp_top (every section)  -> does anything turn red?
  head-check     head RTL, bench plus ONE added check: the holder, with
                 IDENTIFY at 255, sends SET_CONTROL(128) and demands
                 BAD_ARGUMENTS carrying 255, byte-exact (aecp-dispatch target)
  mutant-check   the mutant with the same added check
Usage: probe_sctrl_badarg.py <clone> <scratch-dir> <verilator> <variant>...
"""
import shutil
import subprocess
import sys
from pathlib import Path

clone, scratch, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
variants = sys.argv[4:]

MUT_OLD = ("    u('SET_STATUS', imm=ST_BADARG),              # neither: out of range,\n"
           "    u('BRANCH', imm=SCTRL_EMIT),                 # carrying the value in force\n")
MUT_NEW = ("    u('SET_STATUS', imm=ST_BADARG),              # neither: out of range,\n"
           "    u('BRANCH', imm=E_BADARG1),                  # PROBE: the base's zero body\n")

CHK_ANCHOR = ('          "LK3 ...and the IDENTIFY value is still 255, on GET and on the face");\n')
CHK_ADD = CHK_ANCHOR + (
    "    {  // PROBE: the out-of-range refusal carries the value in force (255)\n"
    "      lock(true, \"PROBE\");\n"
    "      ++seq;\n"
    "      const auto r = ask(AEM_SET_CONTROL, ctrl_body(0, 128));\n"
    "      const auto w = want(CTLR_MAC, CTLR_EID, AECP_BAD_ARGUMENTS, AEM_SET_CONTROL,\n"
    "                          ctrl_body(0, 255));\n"
    "      CHECK(r == w, \"PROBE SET_CONTROL(128) with IDENTIFY at 255: BAD_ARGUMENTS \"\n"
    "            \"carrying 255, byte-exact (status %d, cdl %d, body byte %d)\", st(r), cdl(r),\n"
    "            r.size() > 42 ? int(r[42]) : -1);\n"
    "    }\n")


def tree(name: str, mutate: bool, check: bool) -> Path:
    root = scratch / name
    if root.exists():
        shutil.rmtree(root)
    for parts in (("hdl",), ("tb", "common"), ("tb", "pp_top")):
        shutil.copytree(clone.joinpath(*parts), root.joinpath(*parts),
                        ignore=shutil.ignore_patterns("obj_*", "*.hex", "__pycache__"))
    if mutate:
        g = root / "hdl" / "aecp" / "ucode" / "gen_ucode.py"
        t = g.read_text()
        assert t.count(MUT_OLD) == 1
        g.write_text(t.replace(MUT_OLD, MUT_NEW))
    if check:
        s = root / "tb" / "pp_top" / "sim_main.cpp"
        t = s.read_text()
        assert t.count(CHK_ANCHOR) == 1
        s.write_text(t.replace(CHK_ANCHOR, CHK_ADD))
    return root


def run(root: Path, full: bool) -> None:
    bench = root / "tb" / "pp_top"
    r = subprocess.run(["make", "-C", str(bench), "gsi-build", "VERILATOR=" + verilator],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    (root / "build.log").write_text(r.stdout)
    if r.returncode != 0:
        print(f"{root.name}: build rc={r.returncode}")
        return
    args = [str(bench / "obj_dir" / "Vpp_top_sim")] + ([] if full else ["--aecp-dispatch-only"])
    r = subprocess.run(args, cwd=bench, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, check=False)
    (root / "run.log").write_text(r.stdout)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL:")]
    tallies = [ln for ln in r.stdout.splitlines()
               if ln.startswith("[build ") or ln.startswith("AX:") or ln.startswith("A5b+M9")]
    print(f"{root.name}: sim rc={r.returncode} failures={len(fails)}")
    for ln in tallies + fails[:10]:
        print("    " + ln)


for v in variants:
    if v == "mutant-suite":
        run(tree(v, True, False), True)
    elif v == "head-check":
        run(tree(v, False, True), False)
    elif v == "mutant-check":
        run(tree(v, True, True), False)
    else:
        raise SystemExit(f"unknown variant {v}")
