#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Fixture arms for yosys_bench.py: each plants the defect it guards and requires the refusal.

`yosys_bench.py --selftest` runs this file. It needs neither yosys, sv2v nor
an allocator library: the parsers run on captured text, the allocator arm on
malloc.sh with a missing file and an empty one, the record arms on a scratch
directory and the report arms on synthetic records. Every arm is a mutation
in the sense Rule 8 asks for - the input is broken on purpose and the harness
must notice - so a parser or a verdict that stops noticing turns the arm red.

Arms, by the defect each guards:

  1. EMIT RECORD - a `derived=` line is accepted and not used, an unknown key
     or a record with no `src=` is refused, and sv2v's argv is the record word
     for word.
  2. TIME SPENT TABLE - the `-d` table parses to exact rows, the one-line
     summary yosys prints WITHOUT `-d` parses to no rows, and the table ends
     at the first line that is not a row.
  3. TIME LINE - GNU time's four fields parse, the `Command exited with
     non-zero status` prefix is skipped, and anything else is refused.
  4. VERDICT - exit 0 with a complete log passes; a non-zero exit, an `ERROR:`
     line, a missing `End of script.`, a missing per-pass table, a hierarchy
     pass that is only synth's nested one, one issued BEFORE synth, or one the
     run died inside all refuse.
  5. NO NUMBER ON FAILURE - a record built from a failed run carries null in
     every timing field although a measurement existed; a missing design count
     or a requested-but-absent netlist fails the record; a good run publishes.
  6. DIGEST - equal bytes give one digest, one flipped byte another, and the
     report says MISMATCH when the trials of one cell disagree on the netlist.
  7. ALLOCATOR REFUSAL - an absent library, an existing file the loader will
     not preload, an unknown name and `glibc=...` are refused; `glibc` is no
     preload and actively drops an inherited LD_PRELOAD.
  8. REPORT ARITHMETIC - median, min and max over planted trials, the `vs
     glibc` percentage, a failed trial excluded from the numbers but counted,
     a different concurrency kept as its own row, and the below-3-trials mark.
  9. THE GATE'S PROGRAM - the program this harness times is run.sh's own
     line, read from run.sh and compared after path substitution, so a change
     to the gate's program turns this arm red until the harness follows.
 10. RECORDS - a written record loads back, a foreign schema and an empty
     directory are refused.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yosys_bench as yb  # after the sys.path insert above, on purpose

EMIT_TEXT = """top=T
define=SYNTHESIS
incdir=/i/one
incdir=/i/two
derived=/d/gen.sv
src=/d/gen.sv
src=/s/T.sv
"""

GOOD_LOG = """-- Running command `read_verilog T.v; synth -top T; hierarchy -check; stat -top T' --

1. Executing Verilog-2005 frontend: T.v

2. Executing SYNTH pass.

2.1. Executing HIERARCHY pass (managing design hierarchy).

2.2. Executing PROC pass (convert processes to netlists).

3. Executing HIERARCHY pass (managing design hierarchy).

4. Printing statistics.

5. Printing statistics.

End of script. Logfile hash: 7571950e1d, time: 0.08s, user: 0.04s, system: 0.01s, MEM: 29.38 MB peak
Yosys 0.66 (git sha1 86f2ddebc)
Time spent:
   55%     1 calls    0.039 sec abc
   15%     3 calls    0.011 sec read_verilog
    0%     3 calls    0.001 sec hierarchy
"""

ONE_LINE_TAIL = "Time spent: 59% 1x abc (0 sec), 14% 3x read_verilog (0 sec), ...\n"
STAT_JSON = '{"creator": "Yosys", "design": {"num_wires": 36, "num_cells": 47}}'
MEASURE = yb.Measure(1.5, 1.2, 0.1, 40960)


def _expect(problems: list[str], condition: bool, message: str) -> None:
    if not condition:
        problems.append(message)


def _must_refuse(problems: list[str], call: Callable[[], object], what: str) -> str:
    """Require a BenchRefusal from `call` and return its message; acceptance or a crash is a finding.

    A crash is not a refusal: the command line prints `refused: ...` and exits 2
    on a BenchRefusal and a traceback on anything else, so a parser that dies
    on bad input instead of refusing it is the defect, reported by name.
    """
    try:
        call()
    except yb.BenchRefusal as exc:
        return str(exc)
    except Exception as exc:  # the crash IS the finding, reported by name
        problems.append(f"{what}: crashed with {type(exc).__name__} instead of refusing ({exc})")
        return ""
    problems.append(f"{what} was accepted")
    return ""


def arm_emit() -> list[str]:
    """Arm 1: the --emit record feeds sv2v word for word; anything unknown is refused."""
    problems: list[str] = []
    record = yb.parse_emit(EMIT_TEXT)
    _expect(problems, record == yb.EmitRecord("T", ("SYNTHESIS",), ("/i/one", "/i/two"), ("/d/gen.sv", "/s/T.sv")),
            f"emit record parsed as {record}")
    _expect(problems, yb.sv2v_argv("sv2v", record) == ["sv2v", "--top=T", "-DSYNTHESIS", "-I", "/i/one", "-I", "/i/two",
                                                       "/d/gen.sv", "/s/T.sv"],
            f"sv2v argv is {yb.sv2v_argv('sv2v', record)}")
    _must_refuse(problems, lambda: yb.parse_emit(EMIT_TEXT.replace("src=", "derived=")), "a record with no src= line")
    _must_refuse(problems, lambda: yb.parse_emit(EMIT_TEXT + "flag=-O2\n"), "an unknown --emit key")
    _must_refuse(problems, lambda: yb.parse_emit(EMIT_TEXT + "garbage\n"), "a line without =")
    return problems


def arm_time_spent() -> list[str]:
    """Arm 2: the -d table parses exactly; the no-d one-liner yields nothing."""
    problems: list[str] = []
    rows = yb.parse_time_spent(GOOD_LOG)
    expected = [yb.PassTime("abc", 55, 1, 0.039), yb.PassTime("read_verilog", 15, 3, 0.011),
                yb.PassTime("hierarchy", 0, 3, 0.001)]
    _expect(problems, rows == expected, f"table parsed as {rows}")
    _expect(problems, yb.parse_time_spent(GOOD_LOG.split("Time spent:")[0] + ONE_LINE_TAIL) == [],
            "the one-line summary (no -d) produced rows")
    truncated = GOOD_LOG.replace("   15%     3 calls    0.011 sec read_verilog\n", "junk\n")
    _expect(problems, yb.parse_time_spent(truncated) == expected[:1], "the table did not end at a non-row line")
    return problems


def arm_time_line() -> list[str]:
    """Arm 3: GNU time's line parses; the failure prefix is skipped; junk is refused."""
    problems: list[str] = []
    _expect(problems, yb.parse_time_line("0.08 0.06 0.01 35356\n") == yb.Measure(0.08, 0.06, 0.01, 35356),
            "a plain time line did not parse")
    prefixed = "Command exited with non-zero status 1\n0.01 0.00 0.00 20584\n"
    _expect(problems, yb.parse_time_line(prefixed) == yb.Measure(0.01, 0.0, 0.0, 20584),
            "the non-zero-status prefix was not skipped")
    for text in ("", "0.08 0.06 0.01", "a b c d", "0.08 0.06 0.01 1.5"):
        _must_refuse(problems, lambda t=text: yb.parse_time_line(t), f"time text {text!r}")
    return problems


def arm_verdict() -> list[str]:
    """Arm 4: every way a run proves nothing is a refusal; the complete log passes."""
    problems: list[str] = []
    rows = yb.parse_time_spent(GOOD_LOG)
    _expect(problems, yb.judge(GOOD_LOG, 0, rows).ok, "the complete log was refused")
    planted = {
        "non-zero exit": (GOOD_LOG, 1, rows),
        "ERROR line": (GOOD_LOG.replace("4. Printing statistics.", "ERROR: Module `\\x' is not part of the design."),
                       0, rows),
        "no End of script": (GOOD_LOG.replace("End of script.", "End of scrip"), 0, rows),
        "no per-pass table": (GOOD_LOG, 0, []),
        "only synth's nested hierarchy": (GOOD_LOG.replace("3. Executing HIERARCHY", "2.9. Executing HIERARCHY"),
                                          0, rows),
        "hierarchy before synth": (GOOD_LOG.replace("3. Executing HIERARCHY pass (managing design hierarchy).\n", "")
                                   .replace("1. Executing Verilog-2005 frontend: T.v",
                                            "1. Executing HIERARCHY pass (managing design hierarchy)."), 0, rows),
        "died inside hierarchy -check": (GOOD_LOG.replace("4. Printing statistics.\n", "")
                                         .replace("5. Printing statistics.\n", ""), 0, rows),
    }
    for name, (log, code, table) in planted.items():
        _expect(problems, not yb.judge(log, code, table).ok, f"planted defect passed: {name}")
    return problems


def _spec(work: Path, rtlil: bool) -> yb.RunSpec:
    staged = yb.Staged("T", work, "0" * 64, 10, 0.1, ("sv2v",))
    return yb.RunSpec(staged, yb.Variant("glibc", None, "glibc"), 1, "b", 1, rtlil, "synth")


def arm_no_number() -> list[str]:
    """Arm 5: a failed run's record has null numbers even though a measurement existed."""
    problems: list[str] = []
    ctx = yb.Context({"cpu": "c"}, {"yosys": "Y"})
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        spec = _spec(work, False)
        (work / f"{spec.stem}.yosys.log").write_text(GOOD_LOG)
        (work / f"{spec.stem}.stat.json").write_text(STAT_JSON)
        good = yb.build_record(spec, "p", yb.Outcome(0, MEASURE, "", 0.0), ctx)
        _expect(problems, good["status"] == "ok" and good["wall_s"] == 1.5 and good["cells"] == 47
                and good["wires"] == 36 and len(good["passes"]) == 3, f"a good run did not publish: {good['reason']}")
        failed = yb.build_record(spec, "p", yb.Outcome(1, MEASURE, "", 0.0), ctx)
        nulls = all(failed[k] is None for k in ("wall_s", "user_s", "sys_s", "max_rss_kib", "cells", "wires"))
        _expect(problems, failed["status"] == "failed" and nulls and failed["passes"] == [],
                "a failed run published a number")
        unmeasured = yb.build_record(spec, "p", yb.Outcome(0, None, "time output is empty", 0.0), ctx)
        _expect(problems, unmeasured["status"] == "failed" and unmeasured["wall_s"] is None,
                "a run with no resource measurement published")
        (work / f"{spec.stem}.stat.json").write_text('{"design": {"num_cells": "47"}}')
        _expect(problems, yb.build_record(spec, "p", yb.Outcome(0, MEASURE, "", 0.0), ctx)["status"] == "failed",
                "a non-numeric design count published")
        (work / f"{spec.stem}.stat.json").write_text(STAT_JSON)
        wanted = yb.build_record(_spec(work, True), "p", yb.Outcome(0, MEASURE, "", 0.0), ctx)
        _expect(problems, wanted["status"] == "failed", "a requested but absent netlist published")
    return problems


def _fake(variant: str, wall: float, conc: int = 4, rtlil: str | None = None, status: str = "ok") -> dict[str, object]:
    number = status == "ok"
    return {"schema": yb.SCHEMA, "top": "T", "variant": variant, "alloc_lib": None, "alloc_package": f"{variant} 1.0",
            "trial": 1, "batch_id": "b", "concurrency": conc, "load1_before": 0.0, "program": "p",
            "program_shape": "shape", "input": {"sha256": "d" * 64, "bytes": 1, "sv2v_s": 0.1, "sv2v_argv": []},
            "tools": {"yosys": "Y"}, "machine": {"cpu": "c", "vcpus": 1, "virt": "none", "mem_total_kib": 1048576,
                                                 "kernel": "k", "thp": "always"},
            "status": status, "reason": "" if number else "planted", "exit_code": 0 if number else 1,
            "wall_s": wall if number else None, "user_s": wall if number else None, "sys_s": 0.5 if number else None,
            "max_rss_kib": int(wall * 102400) if number else None, "cells": 47 if number else None,
            "wires": 36 if number else None, "passes": [], "recorded_at": "t",
            "rtlil": {"sha256": rtlil, "bytes": 1} if rtlil and number else None}


def arm_digest() -> list[str]:
    """Arm 6: bytes decide the digest, and disagreeing trials are reported as MISMATCH."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        one, two = Path(tmp) / "a.il", Path(tmp) / "b.il"
        one.write_bytes(b"autoidx 1\nmodule \\T\nend\n")
        two.write_bytes(one.read_bytes())
        _expect(problems, yb.sha256_of(one) == yb.sha256_of(two), "identical files digest differently")
        two.write_bytes(one.read_bytes().replace(b"1", b"2"))
        _expect(problems, yb.sha256_of(one) != yb.sha256_of(two), "a flipped byte kept the digest")
    same = yb.summarise([_fake("glibc", 1, rtlil="a" * 64), _fake("glibc", 1, rtlil="a" * 64)])
    _expect(problems, same.netlist == "a" * 16, f"agreeing netlists reported as {same.netlist!r}")
    mixed = yb.summarise([_fake("glibc", 1, rtlil="a" * 64), _fake("glibc", 1, rtlil="b" * 64)])
    _expect(problems, mixed.netlist.startswith("MISMATCH"), f"disagreeing netlists reported as {mixed.netlist!r}")
    _expect(problems, yb.summarise([_fake("glibc", 1)]).netlist == "-", "no netlist did not read as a dash")
    return problems


def arm_allocator() -> list[str]:
    """Arm 7: a named allocator that is absent or unloadable is refused; glibc is no preload."""
    problems: list[str] = []
    _must_refuse(problems, lambda: yb.resolve_variant("jemalloc=/nonexistent/libjemalloc.so.2"), "an absent library")
    with tempfile.NamedTemporaryFile(suffix=".so") as probe:
        message = _must_refuse(problems, lambda: yb.resolve_variant(f"custom={probe.name}"), "an empty file")
        _expect(problems, not message or "preload" in message,
                f"the empty-file refusal does not name the loader ({message!r})")
    _must_refuse(problems, lambda: yb.resolve_variant("bogus"), "an unknown allocator")
    _must_refuse(problems, lambda: yb.resolve_variant("glibc=/usr/lib/libc.so.6"), "glibc with a library path")
    glibc = yb.resolve_variant("glibc")
    _expect(problems, glibc.lib is None and glibc.name == "glibc", f"glibc resolved to {glibc}")
    saved = os.environ.get("LD_PRELOAD")
    os.environ["LD_PRELOAD"] = "/inherited/from/the/caller.so"
    try:
        _expect(problems, "LD_PRELOAD" not in yb.child_env(None), "glibc inherited the caller's LD_PRELOAD")
        _expect(problems, yb.child_env("/x/y.so").get("LD_PRELOAD") == "/x/y.so", "the library did not reach the env")
    finally:
        if saved is None:
            del os.environ["LD_PRELOAD"]
        else:
            os.environ["LD_PRELOAD"] = saved
    return problems


def arm_report() -> list[str]:
    """Arm 8: median/min/max, the glibc comparison, exclusion of failed trials, rows per concurrency."""
    problems: list[str] = []
    # 1, 2, 9: the median is 2 and the mean is 4, so a mean cannot pass as a median.
    recs = [_fake("glibc", 9.0), _fake("glibc", 1.0), _fake("glibc", 2.0), _fake("glibc", 4.0, status="failed"),
            _fake("jemalloc", 1.0), _fake("jemalloc", 1.0), _fake("jemalloc", 1.0), _fake("jemalloc", 5.0, conc=1)]
    glibc = yb.summarise(recs[:4])
    _expect(problems, glibc.wall == yb.Spread(2.0, 1.0, 9.0) and glibc.ok == 3 and glibc.trials == 4,
            f"glibc cell summarised as {glibc}")
    _expect(problems, glibc.cpu == yb.Spread(2.5, 1.5, 9.5), f"CPU spread is {glibc.cpu}")
    _expect(problems, glibc.rss_mib is not None and abs(glibc.rss_mib.hi - 900.0) < 1e-9,
            f"RSS spread is {glibc.rss_mib}")
    _expect(problems, yb.spread([5.0]) == yb.Spread(5.0, 5.0, 5.0), "a single value is not its own spread")
    _expect(problems, yb.summarise(recs[3:4]).wall is None, "a cell with no OK trial produced a number")
    text = yb.render_report(recs)
    rows = [line for line in text.splitlines() if line.startswith("| glibc") or line.startswith("| jemalloc")]
    _expect(problems, len(rows) == 3, f"expected 3 cell rows, got {len(rows)}")
    _expect(problems, any("| 3/4 | 4 | 2.00 (1.00-9.00) | 2.50 (1.50-9.50) |" in row for row in rows),
            "the glibc row does not carry median (min-max)")
    _expect(problems, any(row.startswith("| jemalloc | 3/3 | 4 |") and "| -50.0% |" in row for row in rows),
            "the jemalloc row is not -50.0% against glibc at the same concurrency")
    _expect(problems, any(row.startswith("| jemalloc | 1/1* | 1 |") and "| - | 47 |" in row for row in rows),
            "the lone-concurrency row is not its own, starred, uncompared row")
    _expect(problems, "## Machine and tools" in text and "- jemalloc: jemalloc 1.0" in text, "the header lacks context")
    return problems


def arm_gate_program() -> list[str]:
    """Arm 9: the timed program is run.sh's own, read from run.sh and compared after substitution."""
    problems: list[str] = []
    text = yb.RUN_SH.read_text()
    head = re.search(r'^\s*program="(read_verilog \$TMP/\$top\.v; [^"]*)"$', text, re.M)
    tail = re.search(r'^\s*program="\$program; (tee -q -o \$TMP/\$top\.stat\.json [^"]*)"$', text, re.M)
    if not head or not tail:
        return ["run.sh no longer spells its full-mode program the way this arm reads it"]
    gate = f"{head.group(1)}; {tail.group(1)}"
    substitutions = (("$TMP/$top.stat.json", "S.stat.json"), ("$TMP/$top.v", "T.v"), ("$SYNTH", "synth"), ("$top", "T"))
    for old, new in substitutions:
        gate = gate.replace(old, new)
    ours = yb.program_for("T", "S", False)
    _expect(problems, gate == ours, f"gate program {gate!r} differs from harness program {ours!r}")
    _expect(problems, yb.program_for("T", "S", True) == ours + "; write_rtlil S.il",
            "--rtlil does not append write_rtlil")
    return problems


def arm_records() -> list[str]:
    """Arm 10: a written record loads back; a foreign schema and an empty directory are refused."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        _must_refuse(problems, lambda: yb.load_records(out), "an empty records directory")
        path = yb.write_record(out, _fake("glibc", 1.0))
        loaded = yb.load_records(out)
        _expect(problems, path.is_file() and len(loaded) == 1 and loaded[0]["wall_s"] == 1.0,
                "the record did not round-trip")
        foreign = dict(_fake("glibc", 1.0), schema=yb.SCHEMA + 1, trial=2)
        yb.write_record(out, foreign)
        _must_refuse(problems, lambda: yb.load_records(out), "a foreign schema")
    return problems


ARMS: tuple[tuple[str, Callable[[], list[str]]], ...] = (
    ("emit record", arm_emit), ("time-spent table", arm_time_spent), ("time line", arm_time_line),
    ("verdict", arm_verdict), ("no number on failure", arm_no_number), ("digest", arm_digest),
    ("allocator refusal", arm_allocator), ("report arithmetic", arm_report), ("gate program", arm_gate_program),
    ("records", arm_records),
)


def main() -> int:
    """Run every arm; exit 1 when any planted defect went unnoticed."""
    failed = 0
    for name, arm in ARMS:
        try:
            problems = arm()
        except Exception as exc:  # a crashing arm is a red arm, not a stopped suite
            problems = [f"crashed: {type(exc).__name__}: {exc}"]
        print(f"  [{'FAIL' if problems else 'PASS'}] {name}")
        for problem in problems:
            print(f"         {problem}")
        failed += bool(problems)
    print(f"bench self-test: {len(ARMS)} arms, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
