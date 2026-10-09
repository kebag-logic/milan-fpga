#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the bare-metal saved-state store of #665 lane F1, on the host, per shape.

WHAT IT RUNS. sw/firmware/ctrl_nvm is portable C11 with no heap: the KLJ2
codec, the store (the boot restore and the write-back) and two flash ports.
For every shipped shape (configs/endstation_*.yaml) the builder fixes the
shape and the identity, the store is compiled against the same constants
sw/litex/milan_soc.py publishes for the shipping writer and at the shape's
own system clock (its config's sys_clk_hz: 83,333,000 Hz at the three Arty
shapes, 100 MHz at the two AX7101 ones), and its GoogleTest suite runs it
over the host flash model directly and over the on-chip LiteSPI port on a
model of the command master (sw/firmware/gtest/README.md). The tests
(test_nvm_boot.cpp, test_nvm_write.cpp) grade the boot path with valid,
absent, torn, corrupted and wrong-version slots, read faults at every boot
read, and the binding and D3 restore walks; the write path's commit, its A/B
atomicity and DR2a/DR2b/DR2c/DR5 rules, the console included; the writer held
while a read fault leaves the authority unknown, and reads that refuse a slot
alike on different bytes; a power cut inside every media effect of a commit;
the time base under PHC steps, at the shape's clock and across the counter's
wrap; a command master that stalls or slows every wait; and the service
bound. test_nvm_vector.cpp is the round trip against the recorded vectors of
tb/verilator/nvm_backend, under their identity. Every byte and every verdict
is compared with the fixture nvm_fixture.py writes from scripts/nvm_klj2.py,
the reference codec.

THE RV32 ARM (nvm_rv32.py) cross-compiles the store and the LiteSPI port
freestanding for RV32I and reports their static sizes per shape. Without a
compiler it is SKIPPED, visibly; --require-rv32 refuses instead.

COVERAGE. --coverage DIR builds every shape's suites with gcov's
instrumentation of the store into DIR and runs them (no RV32 arm, no
self-test); sw/firmware/gtest/fw_coverage.py reads DIR.

NEGATIVE CONTROLS. --self-test plants every defect of nvm_mutants.py into a
copy of the tree, one at a time, at the shipping 1x1 shape (or the shape a
defect names: a clock defect is graded at 83.333 MHz), and requires each
test the defect names to fail. Every test of the suite is named by at least
one defect.

Usage:
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 16
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --config configs/endstation_ax7101_8x8.yaml
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --coverage <dir>

Exit 0 = every test passed (and every planted defect reddened); 1 = a
finding; 2 = refused (the suite could not be built, or no RV32 compiler under
--require-rv32).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import nvm_mutants                                                      # noqa: E402
import nvm_rv32                                                         # noqa: E402
from nvm_bench import (ROOT, SUITE, TREE, UNITS, VECTOR, VECTOR_IDENT, Binary,  # noqa: E402
                       Refusal, ShapeInputs, build_suite, make_bench, run_suite, shape_inputs)
from nvm_fixture import table, write_fixture, write_vector_fixture     # noqa: E402

import fw_gtest                                                         # noqa: E402
import suite_tally                                                      # noqa: E402

SELF_TEST_SHAPE = "endstation_ax7101_1x1_tdm8"


@dataclass(frozen=True)
class Shape:
    """One shape's builder inputs and the fixtures written for it."""

    inputs: ShapeInputs
    fixture: Path
    vector_fixture: Path | None

    @property
    def stem(self) -> str:
        """The shape's config name."""
        return self.inputs.cfg.stem


def prepare(cfg: Path, work: Path) -> Shape:
    """Run the builder for `cfg` and write the shape's fixtures."""
    inputs = shape_inputs(cfg, work / "inputs")
    fixture = write_fixture(make_bench(inputs), work / "fixture")
    vector = None
    if table(cfg.stem) is not None:
        vector = write_vector_fixture(make_bench(inputs, VECTOR_IDENT), work / "vector-fixture")
    return Shape(inputs, fixture, vector)


def binaries(shape: Shape) -> tuple[Binary, ...]:
    """The binaries a shape runs: the suite, the recorded vector's where there
    is one, and at the shipping 1x1 shape the unit binaries too."""
    return (SUITE, *((VECTOR,) if shape.vector_fixture else ()), *(UNITS if shape.stem == SELF_TEST_SHAPE else ()))


def fixture_of(shape: Shape, binary: Binary) -> Path:
    """The fixture a binary reads (the unit binaries ask it nothing)."""
    return shape.vector_fixture if binary.vector and shape.vector_fixture else shape.fixture


def build(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> dict[str, Path]:
    """Every binary of a shape from `tree`, by name."""
    return {binary.name: build_suite(shape.inputs, work / binary.name, b, binary, tree) for binary in binaries(shape)}


def evidence(log: str) -> list[str]:
    """The lines of a run worth printing: the tally, the figures and every failure."""
    keep = ("==", "RESULT", "  longest", "  [FAIL]", "  verdict")
    return [ln for ln in log.splitlines() if ln.startswith(keep)]


def run_shape(shape: Shape, work: Path, b: fw_gtest.Build, require_rv32: bool) -> tuple[list[str], int]:
    """Every binary of one shape, then its RV32 arm; (the findings, the tests run)."""
    exes = build(shape, work, b)
    findings: list[str] = []
    tests = 0
    print(f"{shape.stem:<28} clock={shape.inputs.clock_hz} Hz")
    for binary in binaries(shape):
        ok, log = run_suite(exes[binary.name], fixture_of(shape, binary))
        print("\n".join(f"  {ln.strip()}" for ln in evidence(log)))
        tests += suite_tally.scan(log)[0]
        if not ok:
            findings.append(f"{shape.stem}: {binary.name} failed")
    return findings + [f"{shape.stem}: {x}" for x in rv32_arm(shape.inputs, work, require_rv32)], tests


def rv32_arm(inputs: ShapeInputs, work: Path, require: bool) -> list[str]:
    """The RV32I freestanding build of one shape, and its sizes."""
    cc = nvm_rv32.compiler()
    if cc is None:
        if require:
            raise Refusal("no RV32 compiler (the pinned SDK's riscv32-linux-gcc or a bare-metal one)")
        print(f"  rv32: SKIPPED for {inputs.cfg.stem}: no RV32 compiler; --require-rv32 refuses")
        return []
    found, sizes = nvm_rv32.build(TREE, work / "rv32", work / SUITE.name / "gen", cc)
    if sizes:
        print(f"  rv32 at {inputs.clock_hz} Hz: text={sizes['text']} data={sizes['data']} "
              f"bss={sizes['bss']} "
              f"stage={sizes.get('nvm_stage')} payload={sizes.get('nvm_payload')} "
              f"chunk={sizes.get('nvm_chunk')} store={sizes.get('nvm')} "
              f"clock={sum(sizes.get(s, 0) for s in nvm_rv32.CLOCK)} (bytes)")
        print(f"  largest static frame: {sizes.get('stack_frame')} bytes (not a call-chain bound)")
    return found


def suite_tests(exes: dict[str, Path], shape: Shape) -> dict[str, str]:
    """Every check a shape's binaries hold: the check -> the binary holding it."""
    held: dict[str, str] = {}
    for binary in binaries(shape):
        res = fw_gtest.run([str(exes[binary.name]), "--gtest_list_tests"],
                           env={**os.environ, "NVM_FIXTURE": str(fixture_of(shape, binary))})
        held.update({check: binary.name for check in nvm_mutants.listed_checks(res.stdout)})
    return held


def plant_and_grade(m: nvm_mutants.Mutant, shape: Shape, held: dict[str, str], work: Path,
                    b: fw_gtest.Build) -> str:
    """Plant one defect and run the tests it names; '' when every one failed."""
    tree = work / m.name / "tree"
    nvm_mutants.plant(m, tree)
    try:
        exes = build(shape, work / m.name, b, tree)
    except Refusal as exc:
        return f"self-test: {m.name} at {shape.stem} does not build: {exc}"
    logs = ""
    for binary in binaries(shape):
        kills = [k for k in m.kills if held.get(k) == binary.name]
        if kills:
            logs += run_suite(exes[binary.name], fixture_of(shape, binary), kills)[1]
    shutil.rmtree(tree, ignore_errors=True)
    alive = nvm_mutants.survivors(m, logs)
    if alive:
        return f"self-test: {m.name} at {shape.stem} was NOT caught by {', '.join(alive)}"
    first = next((ln.strip() for ln in logs.splitlines() if "[FAIL]" in ln), "")
    at = f" at {shape.inputs.clock_hz} Hz" if m.shape else ""
    print(f"  self-test OK: {m.name:<26} caught by {', '.join(m.kills)}{at}; first: {first[:110]}")
    return ""


def self_test(shapes: dict[str, Shape], work: Path, jobs: int) -> list[str]:
    """Plant every defect; each test it names must fail, at the shipping 1x1
    shape unless the defect names another (one that shows only at a clock
    that is not a whole number of MHz)."""
    for m in nvm_mutants.MUTANTS:
        stem = m.shape or SELF_TEST_SHAPE
        if stem not in shapes:
            shapes[stem] = prepare(ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
    # each graded shape built once first: every planted copy then reuses its
    # test objects, which no defect changes (its seams are .c files)
    shared = fw_gtest.Build(jobs=1)
    graded = {m.shape or SELF_TEST_SHAPE for m in nvm_mutants.MUTANTS}
    listing = {stem: build(shapes[stem], work / "listing" / stem, fw_gtest.Build(jobs=jobs, cache=shared.cache))
               for stem in graded}
    held = {stem: suite_tests(listing[stem], shapes[stem]) for stem in graded}
    found = [f"self-test: no defect names the test {n}"
             for n in nvm_mutants.unnamed_checks(sorted(held[SELF_TEST_SHAPE]))]
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        verdicts = pool.map(lambda m: plant_and_grade(m, shapes[m.shape or SELF_TEST_SHAPE],
                                                      held[m.shape or SELF_TEST_SHAPE], work / "mutants", shared),
                            nvm_mutants.MUTANTS)
        found += [v for v in verdicts if v]
    return found


def coverage(cfgs: list[Path], out: Path, jobs: int) -> int:
    """Every shape's binaries, built for gcov into `out` and run; 0 when each passed."""
    b = fw_gtest.Build(coverage=True, jobs=jobs)
    failed = False
    try:
        for cfg in cfgs:
            shape = prepare(cfg, out / "shapes" / cfg.stem)
            exes = build(shape, out / "shapes" / cfg.stem, b)
            for binary in binaries(shape):
                ok, log = run_suite(exes[binary.name], fixture_of(shape, binary))
                print("\n".join(f"  {ln.strip()}" for ln in evidence(log) if not ln.startswith("  longest")))
                failed = failed or not ok
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(f"saved-state store coverage run: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main() -> int:
    """Grade every shipped shape; with --self-test, the planted defects too."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", action="append", type=Path,
                    help="configs to grade (default: every configs/endstation_*.yaml)")
    ap.add_argument("--self-test", action="store_true",
                    help="also plant every defect and require its named tests to fail")
    ap.add_argument("--require-rv32", action="store_true",
                    help="refuse, rather than skip, when no RV32 compiler is present")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4, help="parallel builds and planted defects")
    ap.add_argument("--coverage", type=Path, help="build for gcov into this directory and run every shape there")
    args = ap.parse_args()
    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    if args.coverage is not None:
        return coverage(cfgs, args.coverage.resolve(), args.jobs)
    findings: list[str] = []
    print(f"toolchain: {fw_gtest.toolchain()}")
    try:
        with tempfile.TemporaryDirectory(prefix="ctrl-nvm.") as tmp:
            shapes: dict[str, Shape] = {}
            b = fw_gtest.Build(jobs=args.jobs)
            tests = 0
            for cfg in cfgs:
                shapes[cfg.stem] = prepare(cfg, Path(tmp) / "shapes" / cfg.stem)
                got, ran = run_shape(shapes[cfg.stem], Path(tmp) / "shapes" / cfg.stem, b, args.require_rv32)
                findings += got
                tests += ran
            if args.self_test and not findings:
                findings += self_test(shapes, Path(tmp) / "self-test", args.jobs)
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    for x in findings:
        print(f"FINDING: {x}")
    if findings:
        return 1
    print(f"saved-state store gate (#665 F1): OK across {len(cfgs)} shape(s), {tests} tests"
          + (f", and all {len(nvm_mutants.MUTANTS)} planted defects reddened" if args.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
