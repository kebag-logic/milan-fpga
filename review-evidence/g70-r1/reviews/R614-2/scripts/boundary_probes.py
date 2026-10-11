#!/usr/bin/env python3
"""Exercise the production checker using real successful receipts and scratch mutations.

Usage: boundary_probes.py REPO PACKET
Every mutation is disposable. No source in REPO is edited.
"""
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
work = packet / "scratch" / "boundary"
work.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("checker", repo / "syn/ooc/check_ooc_clock.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
logs = packet / "scratch" / "viv_head"
xdc = packet / "scratch" / "head" / "syn/ooc/ooc_clock.xdc"
failures = []
def result(label, found, expected):
    ok = not found if expected is None else all(any(word in f for f in found) for word in expected)
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
    for f in found:
        print("  " + f)
    if not ok:
        failures.append(label)

for top in ("ucpu", "engine"):
    text = (logs / (top + "_ooc.log")).read_text()
    rpt = (logs / (top + "_timing.rpt")).read_text()
    parse = f"Parsing XDC File [{xdc}]\n"
    # Only the first parse is before mapping; the second is post-mapping.
    cases = [
        ("real-clean", text, rpt, None),
        ("late-parse-only", text.replace(parse, "", 1), rpt, ["did not parse"]),
        ("foreign-full-path", text.replace(str(xdc), "/elsewhere/syn/ooc/ooc_clock.xdc"), rpt, ["did not parse"]),
        ("critical-after-summary", text + "\nCRITICAL WARNING: [Timing 38-1] planted\n", rpt, ["CRITICAL WARNING"]),
        ("last-count-nonzero", text + "\n1 Infos, 0 Warnings, 1 Critical Warnings and 0 Errors encountered.\n", rpt, ["session ends with 1"]),
        ("absent-no-clock", text, re.sub(r"^.*checking no_clock.*\n", "", rpt, flags=re.M), ["checking no_clock reports"]),
        ("unclocked-register", text, rpt.replace("no_clock (0)", "no_clock (1)"), ["checking no_clock reports"]),
        ("wrong-period", text, rpt.replace("{0.000 5.000}      10.000", "{0.000 4.000}      8.000"), ["Clock Summary is"]),
        ("wrong-port", text, rpt.replace("{clk_i}", "{clock_renamed}"), ["not bound to clk_i"]),
        ("multiple-sources", text, rpt.replace("{clk_i}", "{clk_i rst_n}"), ["not bound to clk_i"]),
        ("post-synth-source", text + "\n# source late.tcl\n", rpt, ["source after synth_design"]),
        ("post-synth-generated-clock", text + "\n# create_generated_clock -name late\n", rpt, ["create_generated_clock after synth_design"]),
    ]
    for label, log_text, report_text, expected in cases:
        case = work / (top + "-" + label)
        case.mkdir(exist_ok=True)
        log = case / (top + "_ooc.log")
        log.write_text(log_text)
        log.with_name(top + "_timing.rpt").write_text(report_text)
        result(top + "-" + label, checker.post_findings(log, xdc), expected)

# Reachability through make ooc; the stub makes every accepted preflight visible.
base_files = ["Makefile", "syn/ooc/run.sh", "syn/ooc/check_ooc_clock.py", "syn/ooc/ucpu_ooc.tcl", "syn/ooc/engine_ooc.tcl", "syn/ooc/ooc_clock.xdc", "hdl/ucode/gen_gptp_ucode.py"]
cases = ["clean", "engine-late", "ucpu-late", "foreign-xdc", "double-clock", "wrong-period", "source-after", "generated-after"]
for label in cases:
    case = work / ("make-" + label)
    for name in base_files:
        target = case / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / name, target)
    read = "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\n"
    ucpu = case / "syn/ooc/ucpu_ooc.tcl"
    engine = case / "syn/ooc/engine_ooc.tcl"
    clock = case / "syn/ooc/ooc_clock.xdc"
    expected = None
    if label.endswith("-late"):
        script = engine if label.startswith("engine") else ucpu
        script.write_text(script.read_text().replace(read, "") + read)
        expected = ["read_xdc after synth_design"]
    elif label == "foreign-xdc":
        ucpu.write_text(ucpu.read_text().replace(read, "read_xdc /elsewhere/ooc_clock.xdc\n"))
        expected = ["is not read before"]
    elif label == "double-clock":
        clock.write_text(clock.read_text() + "create_clock -period 10.000 -name clk [get_ports clk_i]\n")
        expected = ["expected one create_clock"]
    elif label == "wrong-period":
        clock.write_text(clock.read_text().replace("10.000", "8.000"))
        expected = ["clock is 8.000 ns"]
    elif label == "source-after":
        ucpu.write_text(ucpu.read_text() + "source late.tcl\n")
        expected = ["source after synth_design"]
    elif label == "generated-after":
        ucpu.write_text(ucpu.read_text() + "create_generated_clock -name late\n")
        expected = ["create_generated_clock after synth_design"]
    settings = case / "stub-settings.sh"
    settings.write_text("vivado() { echo REVIEW_STUB_REACHED; return 7; }\n")
    env = dict(os.environ, VIVADO_SETTINGS=str(settings), TMPDIR=str(work), PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(["make", "-j16", "ooc"], cwd=case, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    (case / "make.log").write_text(proc.stdout)
    reached = "REVIEW_STUB_REACHED" in proc.stdout
    ok = proc.returncode != 0 and (reached if expected is None else not reached and all(w in proc.stdout for w in expected))
    print(f"make-{label}: {'PASS' if ok else 'FAIL'} rc={proc.returncode} stub_reached={reached}")
    print(proc.stdout)
    if not ok:
        failures.append("make-" + label)
print(f"SUMMARY 24 report/log probes + 8 make-flow probes; failures={failures}")
sys.exit(bool(failures))
