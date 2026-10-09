#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Shared-stimulus MAAP wire differential: the C core and the parent fabric engine (#686)."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from ctrl_build import CTRL, ROOT, Outcome, Tree, compile_c, execute, sources
import fw_gtest


def differential(out: Path, ctrl: Path = CTRL, rtl: Path | None = None) -> Outcome:
    """Build the real parent RTL and C core; grade by the shared test tally."""
    out.mkdir(parents=True, exist_ok=True)
    tree = Tree(ctrl, out, out / "reuse", fw_gtest.Build(jobs=4))
    objs = compile_c(tree, sources(tree, ("maap/maap.c",)), "core")
    objs.append(fw_gtest.main_object(tree.build, out / "harness"))
    flags = ["-std=c++20", "-O1", "-Wall", "-Wextra", "-Werror",
             f"-I{CTRL / 'maap'}", f"-I{ROOT / 'tb/common'}", f"-I{ROOT / 'sw/firmware/gtest'}"]
    exe = out / "differential"
    argv = [os.environ.get("VERILATOR", "verilator"), "--cc", "--exe", "--build", "-j", "8",
            "--top-module", "KL_maap", "-GCLK_FREQ_HZ_P=10000", "-Wno-fatal",
            "--Mdir", str(out / "fabric"), "-CFLAGS", " ".join(flags),
            "-LDFLAGS", " ".join(fw_gtest.TEST_LIBS), "-o", str(exe),
            str(rtl or ROOT / "hdl/ieee1722/maap/KL_maap.sv"), str(ctrl / "test/test_maap_differential.cpp"),
            *map(str, objs)]
    result = fw_gtest.run(argv, timeout=570)
    (out / "build.log").write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode != 0:
        print(result.stdout + result.stderr)
        return Outcome("maap differential", 2, result.stdout + result.stderr)
    outcome = execute("maap differential", exe)
    (out / "run.log").write_text(outcome.log, encoding="utf-8")
    print(outcome.log)
    return outcome


def sensitivity(out: Path) -> int:
    """Require every differential case to reject its named planted defect."""
    from ctrl_mutants import MUTANTS, caught

    cells = [(m.name, "maap/maap.c", m.old, m.new, f"AllStates/DifferentialCell.SharedConflict/{k}")
             for k, key in enumerate((0, 1, 2, 6, 7, 8, 12, 13, 14))
             for m in MUTANTS if m.name == f"maap-table-b7-{key}"]
    cases = [("wire", "maap/maap.c", "f[17] = 16u;", "f[17] = 28u;", "MaapDifferential.ProbeSequenceWireAndCadence"),
             ("release", "maap/maap.c", "m->state = MAAP_INITIAL;\n\tm->queued = 0;",
              "m->state = MAAP_DEFEND;\n\tm->queued = 0;", "MaapDifferential.ReleaseAndRetry"), *cells]
    delay = "base + MAAP_SERVICE_MS + 1u + draw(m, variation - 2u * MAAP_SERVICE_MS - 1u)"
    timing = "MaapDifferential.ProbeTimingAndCount"
    # R529-1's 1 ms escape and both strict boundary controls.
    for ms in (1, 500, 600):
        cases.append((f"probe-{ms}ms", "maap/maap.c", delay,
                      f"announce ? {delay} : {ms}u", timing))
    cases.append(("parent-probe-bound", "test/test_maap_differential.cpp",
                  "kParentProbeMaxMs = 581", "kParentProbeMaxMs = 499", timing))
    cases.append(("parent-probe-count", "test/test_maap_differential.cpp",
                  'ASSERT_EQ(f.frames.size(), 5u) << "Table B.7 parent four',
                  'ASSERT_EQ(f.frames.size(), 4u) << "Table B.7 parent four', timing))
    cases.append(("parent-ignores-mac", "hdl/ieee1722/maap/KL_maap.sv",
                  "16'hACE1 ^ station_mac_i[15:0] ^ station_mac_i[31:16]",
                  "16'hAC61", timing))
    escaped = 0
    for name, path, old, new, test in cases:
        copy = out / name / "ctrl"
        shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
        is_rtl = path.startswith("hdl/")
        source = out / name / "KL_maap.sv" if is_rtl else copy / path
        original = (ROOT / path if is_rtl else source).read_text(encoding="utf-8")
        if original.count(old) != 1:
            raise ValueError(f"{name}: differential fixture is not unique")
        source.write_text(original.replace(old, new), encoding="utf-8")
        outcome = differential(out / name / "build", copy, source if is_rtl else None)
        needle = "MAC/phase sampling reaches the parent's highest draws" if is_rtl else ""
        ok = caught(test, needle, outcome)
        print(f"[{'ok' if ok else 'ESCAPED'}] differential mutant {name}: {test}", flush=True)
        escaped += not ok
    print(f"differential mutants: {len(cases) - escaped}/{len(cases)} caught")
    return int(escaped != 0)


def main() -> int:
    """Keep all generated files in caller-selected scratch storage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="maap-diff-") as scratch:
        out = args.keep.resolve() if args.keep else Path(scratch)
        out.mkdir(parents=True, exist_ok=True)
        outcome = differential(out)
        if outcome.rc != 0:
            return outcome.rc
        return sensitivity(out / "mutants") if args.self_test else 0


if __name__ == "__main__":
    sys.exit(main())
