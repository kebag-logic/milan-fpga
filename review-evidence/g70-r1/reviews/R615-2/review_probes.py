#!/usr/bin/env python3
"""Focused, disposable review probes. No synthesis, network access or source edits.

Usage: python3 review_probes.py --repo /path/to/clone --packet /path/to/packet --jobs 4
All fixtures and copies live below packet/scratch; receipts below packet/receipts/probes.
The fixture logs are synthetic and cannot establish measured resource or timing results.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HEAD = "169073fe9751b873d140b46d4363e02ad4f56b88"
LOG = """# read_xdc $SPEC/syn/ooc/ooc_clock.xdc
Command: synth_design -mode out_of_context -top KL_gptp_ucpu -part xc7a100tfgg484-2
Starting synth_design
Processing XDC Constraints
Parsing XDC File [@XDC@]
Start Technology Mapping
39 Infos, 65 Warnings, 0 Critical Warnings and 0 Errors encountered.
synth_design completed successfully
# report_timing_summary -delay_type max -max_paths 3 -file ucpu_timing.rpt
# report_clocks -append -file ucpu_timing.rpt
"""
RPT = """Synthetic review fixture; no measurement
1. checking no_clock (0)

Clock  Waveform(ns)  Period(ns)  Frequency(MHz)
-----  ------------ ---------- --------------
clk    {0.000 5.000} 10.000     100.000

Clock  Period(ns)  Waveform(ns)  Attributes  Sources
clk    10.000      {0.000 5.000} P           {clk_i}

"""
TCL = r"""# This harness traces commands; it performs no synthesis.
proc read_xdc {path} {
    set ::constraint [file normalize $path]
    puts "READ $::constraint"
}
proc read_verilog {args} {}
proc get_ports {name} {return $name}
proc create_clock {args} {
    if {$args ne "-period 10.000 -name clk clk_i"} {error "wrong clock $args"}
    set ::clock $args
    puts "CLOCK $args"
}
proc synth_design {args} {
    if {![info exists ::constraint]} {error "synthesis before constraint read"}
    source $::constraint
    if {![info exists ::clock]} {error "clock absent"}
    puts "SYNTH $args"
}
proc report_utilization {args} {puts "REPORT utilization $args"}
proc report_timing_summary {args} {puts "REPORT timing $args"}
proc report_clocks {args} {puts "REPORT clocks $args"}
source [lindex $argv 0]
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    assert 1 <= args.jobs <= 16
    repo, packet = args.repo.resolve(), args.packet.resolve()
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip() == HEAD
    work = packet / "scratch" / "probes"
    receipts = packet / "receipts" / "probes"
    work.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(work))
    source = repo / "syn/ooc/check_ooc_clock.py"
    spec = importlib.util.spec_from_file_location("reviewed_checker", source)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    rows = []

    def record(name, command, cwd, expected_rc=None, must=(), absent=()):
        result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, timeout=120)
        (receipts / (name + ".log")).write_text(result.stdout)
        (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
        ok = (expected_rc is None or result.returncode == expected_rc)
        ok &= all(word in result.stdout for word in must)
        ok &= all(word not in result.stdout for word in absent)
        row = dict(name=name, rc=result.returncode, pass_expected=bool(ok),
                   required=list(must), forbidden=list(absent))
        return row

    # Interpret the actual Tcl scripts with independent command stubs.
    trace = work / "trace.tcl"
    trace.write_text(TCL)
    for top in ("ucpu", "engine"):
        row = record("trace_" + top,
                     ["tclsh", str(trace), str(repo / "syn/ooc" / (top + "_ooc.tcl"))], work, 0,
                     ("CLOCK -period 10.000 -name clk clk_i", "SYNTH -mode out_of_context",
                      "REPORT utilization -hierarchical -file " + top + "_util_hier.rpt",
                      "REPORT utilization -file " + top + "_util.rpt",
                      "REPORT timing -delay_type max -max_paths 3 -file " + top + "_timing.rpt",
                      "REPORT clocks -append -file " + top + "_timing.rpt"))
        rows.append(row)

    # Exercise the actual make target, substituting only the synthesis executable.
    # The positive control must reach the sentinel (exit 37); failures must stop first.
    base = work / "base"
    base.mkdir(exist_ok=True)
    for relative in ("Makefile", "syn/ooc/check_ooc_clock.py", "syn/ooc/run.sh",
                     "syn/ooc/ucpu_ooc.tcl", "syn/ooc/engine_ooc.tcl", "syn/ooc/ooc_clock.xdc",
                     "hdl/ucode/gen_gptp_ucode.py"):
        target = base / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / relative, target)
    settings = work / "settings.sh"
    settings.write_text("vivado() { echo REVIEW_SYNTHESIS_SENTINEL; return 37; }\n")
    env["VIVADO_SETTINGS"] = str(settings)
    read = "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\n"
    cases = [("make_clean", None, None, ("REVIEW_SYNTHESIS_SENTINEL",), ())]
    for top in ("ucpu", "engine"):
        path = "syn/ooc/" + top + "_ooc.tcl"
        old = (base / path).read_text()
        moved = old.replace(read, "").replace("report_utilization -hierarchical", read + "report_utilization -hierarchical")
        cases.append(("make_late_" + top, path, moved,
                      (top + "_ooc.tcl", "read_xdc after synth_design"), ("REVIEW_SYNTHESIS_SENTINEL",)))
        foreign = old.replace(read, "read_xdc /nonexistent/ooc_clock.xdc\n")
        cases.append(("make_foreign_" + top, path, foreign,
                      (top + "_ooc.tcl", "is not read before"), ("REVIEW_SYNTHESIS_SENTINEL",)))
    xdc = (base / "syn/ooc/ooc_clock.xdc").read_text()
    cases.extend([
        ("make_8ns", "syn/ooc/ooc_clock.xdc", xdc.replace("10.000", "8.000"),
         ("clock is 8.000 ns",), ("REVIEW_SYNTHESIS_SENTINEL",)),
        ("make_two_clocks", "syn/ooc/ooc_clock.xdc", xdc + "create_clock -period 10.000 -name extra [get_ports clk_i]\n",
         ("expected one create_clock",), ("REVIEW_SYNTHESIS_SENTINEL",)),
    ])

    def make_case(case):
        name, path, text, must, absent = case
        copy = work / name
        shutil.copytree(base, copy, dirs_exist_ok=True)
        if path:
            (copy / path).write_text(text)
        return record(name, ["make", "-j16", "ooc"], copy, 2, must, absent)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows.extend(pool.map(make_case, cases))

    # Independent report/log fixtures test each observable post-synthesis failure.
    post_cases = [("post_clean", LOG, RPT, ())]
    post_cases.extend([
        ("post_critical_line", LOG + "CRITICAL WARNING: [Review 1] planted\n", RPT, ("CRITICAL WARNING:",)),
        ("post_critical_count", LOG.replace("0 Critical", "2 Critical"), RPT, ("session ends with 2 critical warnings",)),
        ("post_missing_count", "\n".join(x for x in LOG.splitlines() if "Infos," not in x), RPT, ("no session message count",)),
        ("post_foreign_path", LOG.replace("@XDC@", "/foreign/syn/ooc/ooc_clock.xdc"), RPT, ("did not parse",)),
        ("post_late_parse", LOG.replace("Parsing XDC File [@XDC@]\n", "").replace("Start Technology Mapping", "Start Technology Mapping\nParsing XDC File [@XDC@]"), RPT, ("did not parse",)),
        ("post_late_clock", LOG + "# create_clock -period 10.000 -name clk [get_ports clk_i]\n", RPT, ("create_clock after synth_design",)),
        ("post_8ns", LOG, RPT.replace("10.000", "8.000").replace("5.000", "4.000").replace("100.000", "125.000"), ("Clock Summary is",)),
        ("post_wrong_port", LOG, RPT.replace("{clk_i}", "{other_i}"), ("not bound to clk_i",)),
        ("post_second_clock", LOG, RPT.replace("clk    {0.000 5.000} 10.000     100.000", "clk    {0.000 5.000} 10.000     100.000\nextra {0.000 5.000} 10.000 100.000"), ("Clock Summary is",)),
        ("post_unclocked", LOG, RPT.replace("no_clock (0)", "no_clock (1003)"), ("checking no_clock reports",)),
        ("post_missing_report", LOG, None, ("ucpu_timing.rpt: missing",)),
        ("post_unfinished", LOG.replace("synth_design completed successfully", "synthesis stopped"), RPT, ("did not complete",)),
        ("post_missing_log", None, RPT, ("ucpu_ooc.log: missing",)),
    ])
    for name, logtext, reporttext, must in post_cases:
        directory = work / name
        directory.mkdir(exist_ok=True)
        log, report = directory / "ucpu_ooc.log", directory / "ucpu_timing.rpt"
        for path, text in ((log, logtext), (report, reporttext)):
            if text is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(text.replace("@XDC@", str(source.parent / "ooc_clock.xdc")))
        rows.append(record(name, [sys.executable, str(source), "--log", str(log)], work,
                           0 if not must else 1, must))

    # Mutate distinct checker rules and require a diagnostic from its own selftest.
    mutations = [
        ("duplicate_xdc", "if len(clocks) != 1 or clocks[0] is None:", "if not clocks or clocks[0] is None:", "XDC with two create_clock lines escaped"),
        ("script_foreign", 'words == ["read_xdc", XDC_READ]', 'words[0] == "read_xdc" and words[-1].endswith(XDC)', "foreign ooc_clock.xdc of the same basename escaped"),
        ("log_foreign", 're.escape(str(xdc))', 'r".*/" + re.escape(xdc.name)', "foreign ooc_clock.xdc of the same basename read and parsed escaped"),
        ("critical_line", "if LOG_CRITICAL_RE.match(line):", "if False:", "critical warning after the session count escaped"),
        ("critical_count", 'elif (critical := LOG_COUNT_RE.match(lines[counts[-1]]).group(1)) != "0":', 'elif False:', "critical-warning count above zero escaped"),
        ("summary_period", "if summary != [CLOCK_SUMMARY]:", "if len(summary) != 1:", "wrong period escaped"),
        ("summary_duplicate", "if summary != [CLOCK_SUMMARY]:", "if summary[:1] != [CLOCK_SUMMARY]:", "second clock escaped"),
        ("clock_source", "if sources != [[CLOCK_PORT]]:", "if not sources:", "clock bound to another port escaped"),
        ("no_clock", 'if no_clock[:1] != ["0"]:', "if False:", "unclocked registers escaped"),
        ("read_before", 'if not any(words == ["read_xdc", XDC_READ] for _line, words in before):', "if False:", "no read_xdc escaped"),
    ]
    original = source.read_text()

    def mutate(case):
        name, old, new, expected = case
        assert original.count(old) == 1, name
        path = work / ("mutant_" + name + ".py")
        path.write_text(original.replace(old, new))
        return record("mutant_" + name, [sys.executable, str(path), "--selftest"], work,
                      1, (expected,), ("Traceback",))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows.extend(pool.map(mutate, mutations))
    rows.append(record("selftest_clean", [sys.executable, str(source), "--selftest"], work, 0,
                       ("PASS (30 arms)",)))
    (receipts / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
    for row in rows:
        print(f"{'PASS' if row['pass_expected'] else 'FAIL'} {row['name']} rc={row['rc']}")
    print(f"TOTAL {sum(row['pass_expected'] for row in rows)}/{len(rows)} expected outcomes")
    return int(not all(row["pass_expected"] for row in rows))


if __name__ == "__main__":
    sys.exit(main())
