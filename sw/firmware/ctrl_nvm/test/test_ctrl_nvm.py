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
(test_nvm_boot.cpp, test_nvm_write.cpp, test_nvm_journal.cpp) grade the boot
path with valid, absent, torn, corrupted and wrong-version slots, read faults
at every boot read, and the binding and D3 restore walks; the append-only
journal of #823 (the log's replay, a torn delta, compaction, the background
erase and its suspend, the reserve, the append's deadline); the write path's
DR2b/DR2c/DR5 rules, the console included; the writer held while a read
fault leaves the authority unknown, and reads that refuse a slot alike on
different bytes; a power cut inside every media effect of a save and of a
compaction;
the time base under PHC steps, at the shape's clock and across the counter's
wrap; a command master that stalls or slows every wait; and the service
bound. test_nvm_vector.cpp is the round trip against the recorded vectors of
tb/verilator/nvm_backend, under their identity. Every byte and every verdict
is compared with the fixture nvm_fixture.py writes from scripts/nvm_klj3.py,
the reference codec of the split placement's KLJ3 and layout 3 (#823).

THE NAME CAPACITY (#823 scope item 4). At the shipping 1x1 shape the store is
also built with its names raised to the layout 3 NAME block's capacity
(test_nvm_capacity.cpp: the block's first, last and one-past id, and a commit
at capacity), and one name past it must not compile: nvm_shape.h refuses it,
and this gate requires the refusal and its words. So must a map entry count
the codec's table cannot hold: 256 for an input port, 65,536 for an output;
255 for an input port must compile. So must the doctored input-width build
outside the host test, and a journal that does not fit (#823 test plan T15).

THE BOUND SHAPE (#823 test plan T11 and T13). With the 1x1 shape the store is
also built at 32x32/2if TDM8, as scripts/nvm_format_32x32.py builds it with
the builder's three 32x32 limits lifted in memory (test_nvm_bound.cpp): the
save bound at the datasheet maxima, and the commit deadline.

THE RV32 ARM (nvm_rv32.py) cross-compiles the store and the LiteSPI port
freestanding for RV32I and reports their static sizes per shape. Without a
compiler it is SKIPPED, visibly; --require-rv32 refuses instead.

COVERAGE. --coverage DIR builds every shape's suites with gcov's
instrumentation of the store into DIR and runs them (no RV32 arm, no
self-test); sw/firmware/gtest/fw_coverage.py reads DIR.

BUILD ONLY. --build-only builds and links every shape's binaries (with
--coverage, the coverage builds) and its RV32 arm, and runs no binary; it
plants nothing and ends BUILT, never OK. The TSN stack boundary gate's builds
are such runs (sw/firmware/ctrl/test/ctrl_configs.py, BUILDERS): the boundary
needs the compiles, not the tests (#697).

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
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only

Exit 0 = every test passed (and every planted defect reddened; with
--build-only, every binary built); 1 = a
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
from nvm_bench import (CFLAGS, NAME_CAPACITY, ROOT, SUITE, TREE, UNITS, VECTOR,  # noqa: E402
                       VECTOR_IDENT, Binary, Refusal, ShapeInputs, bound_inputs, build_suite, doctor, includes,
                       make_bench, run_suite, shape_header, shape_inputs, write_headers)
from nvm_fixture import (table, write_bound_fixture, write_capacity_fixture, write_fixture,  # noqa: E402
                         write_vector_fixture)

import fw_gtest                                                         # noqa: E402
import suite_tally                                                      # noqa: E402

SELF_TEST_SHAPE = "endstation_ax7101_1x1_tdm8"
#: What nvm_shape.h says when the names outgrow the layout 3 NAME block, and
#: the assert that says it (the over-capacity control removes it).
NAME_REFUSAL = "the names outgrow their id block"
NAME_ASSERT = f'_Static_assert(MILAN_NVM3_N_NAME <= NVM3_CAP_NAME, "{NAME_REFUSAL}");\n'
#: The map tables' width refusals (#823): (the doctored constant, the count
#: one past its table, the words, and the assert the control removes).
MAPIN_REFUSAL = "an input map's entries outgrow the codec's byte table"
MAPOUT_REFUSAL = "an output map's entries outgrow the codec's 16-bit table"
#: The input table's own limit, which must compile (the accept side of WIDTHS).
AT_WIDTH = ("MILAN_NVM3_MAPIN_ENTRIES_0", 255)
#: The doctored input-width build refused outside the host test (nvm_shape.h).
DOCTORED_REFUSAL = "NVM_DOCTORED_MAPIN is the host test's doctored build alone"
DOCTORED_ERROR = f'#if defined(NVM_DOCTORED_MAPIN) && !defined(NVM_HOST_SHAPE)\n#error "{DOCTORED_REFUSAL}"\n#endif\n'
#: The journal's fit at the bound shape (#823 decision 3, test plan T15): a
#: slot of two erase blocks, one of three, and at the shipping shape one
#: output map larger than a delta segment, each refused in nvm_shape.h's
#: words, at its assert (the control removes it).
FITS = (
    ("bound", "MILAN_FLASH_JOURNAL_KLJ3_SIZE", 4 * 0x10000, "the container outgrows one slot",
     '_Static_assert(NVM_IMG_LEN <= NVM_SLOT_BYTES, "the container outgrows one slot");\n'),
    ("bound", "MILAN_FLASH_JOURNAL_KLJ3_SIZE", 6 * 0x10000, "a slot holds a base and an append log at least as large",
     '_Static_assert(NVM_LOG_START + NVM_IMG_LEN <= NVM_SLOT_BYTES,\n'
     '\t       "a slot holds a base and an append log at least as large");\n'),
    ("shape", "MILAN_NVM3_MAPOUT_ENTRIES_0", 900, "the largest record outgrows a delta segment",
     '_Static_assert(NVM_KLJ_MIN + ((NVM_SZ(NVM_PAYLOAD_MAX) + 3u) & ~3u) <= NVM_SEG_MAX,\n'
     '\t       "the largest record outgrows a delta segment");\n'),
)
WIDTHS = (
    ("MILAN_NVM3_MAPIN_ENTRIES_0", 256, MAPIN_REFUSAL,
     f'_Static_assert(NVM_SUM32(NVM_MAPI_WIDE) == 0u, "{MAPIN_REFUSAL}");\n'),
    ("MILAN_NVM3_MAPOUT_ENTRIES_0", 65536, MAPOUT_REFUSAL,
     f'_Static_assert(NVM_SUM32(NVM_MAPO_WIDE) == 0u, "{MAPOUT_REFUSAL}");\n'),
)


@dataclass(frozen=True)
class Shape:
    """One shape's builder inputs and the fixtures written for it."""

    inputs: ShapeInputs
    fixture: Path
    vector_fixture: Path | None
    capacity_fixture: Path | None
    #: the bound shape's inputs and fixture, prepared with the shipping 1x1
    bound: ShapeInputs | None = None
    bound_fixture: Path | None = None

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
    capacity = bound = bound_fixture = None
    if cfg.stem == SELF_TEST_SHAPE:
        capacity = write_capacity_fixture(make_bench(inputs, names=NAME_CAPACITY), work / "capacity-fixture")
        bound = bound_inputs(work / "bound")
        bound_fixture = write_bound_fixture(make_bench(bound), work / "bound-fixture")
    return Shape(inputs, fixture, vector, capacity, bound, bound_fixture)


def binaries(shape: Shape) -> tuple[Binary, ...]:
    """The binaries a shape runs: the suite, the recorded vector's where there
    is one, and at the shipping 1x1 shape the unit binaries too."""
    return (SUITE, *((VECTOR,) if shape.vector_fixture else ()), *(UNITS if shape.stem == SELF_TEST_SHAPE else ()))


def fixture_of(shape: Shape, binary: Binary) -> Path:
    """The fixture a binary reads (the unit binaries ask it nothing)."""
    if binary.capacity and shape.capacity_fixture:
        return shape.capacity_fixture
    if binary.bound and shape.bound_fixture:
        return shape.bound_fixture
    return shape.vector_fixture if binary.vector and shape.vector_fixture else shape.fixture


def over_capacity(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> list[str]:
    """One name past the layout 3 NAME block must not compile: the codec built
    against the shape header with its names at the capacity plus one is
    refused by nvm_shape.h, in its words. '' findings when it is."""
    gen = work / "over-capacity" / "gen"
    header = doctor(shape_header(shape.inputs), (("MILAN_NVM3_N_NAME", NAME_CAPACITY + 1),))
    write_headers(gen, header, shape.inputs.clock_hz)
    try:
        fw_gtest.compile_c(b, CFLAGS, includes(tree, gen), [tree / "nvm_klj2.c"], work / "over-capacity" / "obj")
    except fw_gtest.BuildError as exc:
        if NAME_REFUSAL in str(exc):
            print(f"  over capacity: {NAME_CAPACITY + 1} names refused at compile time ({NAME_REFUSAL!r})")
            return []
        return [f"{NAME_CAPACITY + 1} names refused for another reason: {str(exc)[-300:]}"]
    return [f"{NAME_CAPACITY + 1} names, one past the layout 3 NAME block, compiled"]


def over_width(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> list[str]:
    """A map entry count one past its table's width must not compile: the
    codec built against the shape header with one port's count there is
    refused by nvm_shape.h, in its words. Only the overflow a too-wide table
    initialiser raises is let pass, so the refusal is the assert's. ''
    findings when both are."""
    found = []
    for name, count, words, _assert in WIDTHS:
        gen = work / "over-width" / name / "gen"
        write_headers(gen, doctor(shape_header(shape.inputs), ((name, count),)), shape.inputs.clock_hz)
        try:
            fw_gtest.compile_c(b, (*CFLAGS, "-Wno-overflow"), includes(tree, gen), [tree / "nvm_klj2.c"],
                               work / "over-width" / name / "obj")
        except fw_gtest.BuildError as exc:
            if words in str(exc):
                print(f"  over width: {name} = {count} refused at compile time ({words!r})")
                continue
            found.append(f"{name} = {count} refused for another reason: {str(exc)[-300:]}")
            continue
        found.append(f"{name} = {count}, past its table's width, compiled")
    name, count = AT_WIDTH
    gen = work / "at-width" / "gen"
    write_headers(gen, doctor(shape_header(shape.inputs), ((name, count),)), shape.inputs.clock_hz)
    try:
        fw_gtest.compile_c(b, CFLAGS, includes(tree, gen), [tree / "nvm_klj2.c"], work / "at-width" / "obj")
        print(f"  at width: {name} = {count}, its table's limit, compiles")
    except fw_gtest.BuildError as exc:
        found.append(f"{name} = {count}, its table's limit, does not compile: {str(exc)[-300:]}")
    return found


def doctored_outside(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> list[str]:
    """NVM_DOCTORED_MAPIN under a shape header that is not the host test's
    (no NVM_HOST_SHAPE, as on a target) must not compile, in nvm_shape.h's
    words. '' findings when it does not."""
    gen = work / "doctored-outside" / "gen"
    header = "\n".join(ln for ln in shape_header(shape.inputs).splitlines() if "NVM_HOST_SHAPE" not in ln) + "\n"
    write_headers(gen, header, shape.inputs.clock_hz)
    try:
        fw_gtest.compile_c(b, (*CFLAGS, "-DNVM_DOCTORED_MAPIN"), includes(tree, gen), [tree / "nvm_klj2.c"],
                           work / "doctored-outside" / "obj")
    except fw_gtest.BuildError as exc:
        if DOCTORED_REFUSAL in str(exc):
            print(f"  doctored outside the host test: refused at compile time ({DOCTORED_REFUSAL!r})")
            return []
        return [f"NVM_DOCTORED_MAPIN outside the host test refused for another reason: {str(exc)[-300:]}"]
    return ["NVM_DOCTORED_MAPIN outside the host test compiled"]


def over_fit(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> list[str]:
    """Each journal that does not fit (FITS) must not compile, in its
    assert's words. '' findings when none does."""
    found = []
    for n, (where, name, value, words, _assert) in enumerate(FITS):
        inputs = shape.bound if where == "bound" else shape.inputs
        where = "the bound shape" if where == "bound" else shape.stem
        gen = work / "over-fit" / str(n) / "gen"
        write_headers(gen, doctor(shape_header(inputs), ((name, value),)), inputs.clock_hz)
        try:
            fw_gtest.compile_c(b, CFLAGS, includes(tree, gen), [tree / "nvm_klj2.c"],
                               work / "over-fit" / str(n) / "obj")
        except fw_gtest.BuildError as exc:
            if words in str(exc):
                print(f"  over fit: {name} = {value} at {where} refused at compile time ({words!r})")
                continue
            found.append(f"{name} = {value} at {where} refused for another reason: {str(exc)[-300:]}")
            continue
        found.append(f"{name} = {value} at {where}, a journal that does not fit, compiled")
    return found


def build(shape: Shape, work: Path, b: fw_gtest.Build, tree: Path = TREE) -> dict[str, Path]:
    """Every binary of a shape from `tree`, by name; the bound binary at the bound shape."""
    return {binary.name: build_suite(shape.bound if binary.bound else shape.inputs, work / binary.name, b, binary,
                                     tree)
            for binary in binaries(shape)}


def evidence(log: str) -> list[str]:
    """The lines of a run worth printing: the tally, the figures and every failure (in a build-only run, that the
    binary was not run)."""
    keep = ("==", "RESULT", "  longest", "  [FAIL]", "  verdict", "  save bound", "  append")
    return [ln for ln in log.splitlines() if ln.startswith(keep) or ln.endswith(fw_gtest.NOT_RUN)]


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
    if shape.stem == SELF_TEST_SHAPE and fw_gtest.EXECUTION.run:
        findings += [f"{shape.stem}: {x}" for x in over_capacity(shape, work, b)]
        findings += [f"{shape.stem}: {x}" for x in over_width(shape, work, b)]
        findings += [f"{shape.stem}: {x}" for x in doctored_outside(shape, work, b)]
        findings += [f"{shape.stem}: {x}" for x in over_fit(shape, work, b)]
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
              f"chunk={sizes.get('nvm_chunk')} page={sizes.get('nvm_page')} carry={sizes.get('nvm_carry')} "
              f"store={sizes.get('nvm')} "
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
    # the planted tree and its builds, about 100 MB a defect, are not kept
    shutil.rmtree(work / m.name, ignore_errors=True)
    alive = nvm_mutants.survivors(m, logs)
    if alive:
        return f"self-test: {m.name} at {shape.stem} was NOT caught by {', '.join(alive)}"
    first = next((ln.strip() for ln in logs.splitlines() if "[FAIL]" in ln), "")
    at = f" at {shape.inputs.clock_hz} Hz" if m.shape else ""
    print(f"  self-test OK: {m.name:<26} caught by {', '.join(m.kills)}{at}; first: {first[:110]}")
    return ""


def over_capacity_control(shape: Shape, work: Path, b: fw_gtest.Build) -> list[str]:
    """The compile-time refusal's own control: with nvm_shape.h's NAME assert
    removed, one name past the block compiles, and over_capacity says so."""
    m = nvm_mutants.Mutant("name_assert_removed", (("nvm_shape.h", NAME_ASSERT, ""),), ())
    tree = work / "tree"
    nvm_mutants.plant(m, tree)
    found = over_capacity(shape, work, b, tree)
    shutil.rmtree(tree, ignore_errors=True)
    if not any("compiled" in x for x in found):
        return ["self-test: name_assert_removed was NOT caught: over_capacity found " + repr(found)]
    print("  self-test OK: name_assert_removed        caught by over_capacity")
    return []


def over_width_control(shape: Shape, work: Path, b: fw_gtest.Build) -> list[str]:
    """The width refusals' own controls: with one of nvm_shape.h's two width
    asserts removed, over_width no longer finds that refusal in its words (an
    input count past its byte table compiles; an output count past 16 bits is
    still refused, by the slot's size and by the table type's range, but in
    other words)."""
    found = []
    for name, _count, words, line in WIDTHS:
        label = ("mapin" if "MAPIN" in name else "mapout") + "_width_assert_removed"
        m = nvm_mutants.Mutant(label, (("nvm_shape.h", line, ""),), ())
        tree = work / label / "tree"
        nvm_mutants.plant(m, tree)
        got = over_width(shape, work / label, b, tree)
        shutil.rmtree(tree, ignore_errors=True)
        if not any(x.startswith(name) for x in got):
            found.append(f"self-test: {label} was NOT caught: over_width found {got!r}")
            continue
        print(f"  self-test OK: {label:<26} caught by over_width; first: {got[0][:110]}")
    # the input table's limit refused one entry early
    m = nvm_mutants.Mutant("mapin_width_off_by_one", (("nvm_shape.h", "(MILAN_NVM3_MAPIN_ENTRIES_##k > 255u)",
                                                       "(MILAN_NVM3_MAPIN_ENTRIES_##k >= 255u)"),), ())
    tree = work / m.name / "tree"
    nvm_mutants.plant(m, tree)
    got = over_width(shape, work / m.name, b, tree)
    shutil.rmtree(tree, ignore_errors=True)
    if any("its table's limit, does not compile" in x for x in got):
        print(f"  self-test OK: {m.name:<26} caught by over_width")
    else:
        found.append(f"self-test: {m.name} was NOT caught: over_width found {got!r}")
    return found


def doctored_control(shape: Shape, work: Path, b: fw_gtest.Build) -> list[str]:
    """The refusal's own control: with nvm_shape.h's #error removed, the
    doctored build compiles outside the host test, and doctored_outside says so."""
    m = nvm_mutants.Mutant("doctored_error_removed", (("nvm_shape.h", DOCTORED_ERROR, ""),), ())
    tree = work / "tree"
    nvm_mutants.plant(m, tree)
    found = doctored_outside(shape, work, b, tree)
    shutil.rmtree(tree, ignore_errors=True)
    if not any("compiled" in x for x in found):
        return ["self-test: doctored_error_removed was NOT caught: doctored_outside found " + repr(found)]
    print("  self-test OK: doctored_error_removed     caught by doctored_outside")
    return []


def fit_control(shape: Shape, work: Path, b: fw_gtest.Build) -> list[str]:
    """Each fit assert's own control: removed, its journal is no longer
    refused in its words."""
    found = []
    for n, (_where, name, value, words, line) in enumerate(FITS):
        m = nvm_mutants.Mutant(f"fit_assert_removed_{n}", (("nvm_shape.h", line, ""),), ())
        tree = work / m.name / "tree"
        nvm_mutants.plant(m, tree)
        got = over_fit(shape, work / m.name, b, tree)
        shutil.rmtree(tree, ignore_errors=True)
        if not any(x.startswith(f"{name} = {value}") for x in got):
            found.append(f"self-test: {m.name} was NOT caught: over_fit found {got!r}")
            continue
        print(f"  self-test OK: {m.name:<26} caught by over_fit; first: {got[0][:110]}")
    return found


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
    found += over_capacity_control(shapes[SELF_TEST_SHAPE], work / "over-capacity-control", shared)
    found += over_width_control(shapes[SELF_TEST_SHAPE], work / "over-width-control", shared)
    found += doctored_control(shapes[SELF_TEST_SHAPE], work / "doctored-control", shared)
    found += fit_control(shapes[SELF_TEST_SHAPE], work / "fit-control", shared)
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
    print(f"saved-state store coverage run: {'FAIL' if failed else 'PASS' if fw_gtest.EXECUTION.run else 'BUILT'}")
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
    ap.add_argument("--build-only", action="store_true",
                    help="build and link every binary and run none (the TSN stack boundary gate's builds)")
    args = ap.parse_args()
    if args.build_only and args.self_test:
        ap.error("--build-only runs no test, so it plants no defect: drop --self-test")
    fw_gtest.EXECUTION.run = not args.build_only
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
    if args.build_only:
        print(f"saved-state store gate (#665 F1): BUILT across {len(cfgs)} shape(s), nothing run (--build-only)")
        return 0
    print(f"saved-state store gate (#665 F1): OK across {len(cfgs)} shape(s), {tests} tests"
          + (f", and all {len(nvm_mutants.MUTANTS) + 1 + len(WIDTHS) + 1 + 1 + len(FITS)} planted defects reddened"
             if args.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
