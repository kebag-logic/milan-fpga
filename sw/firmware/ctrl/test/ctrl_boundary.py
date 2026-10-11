#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_boundary.py - the TSN stack's boundary, held from both sides in the builders' own compiles (#697).

THE COMPILES DECIDE. The gate judges exactly the sources a capture of the
builders' compiler invocations recorded as compiled (ctrl_capture.py), and for
each, what it read is the compiler's own dependency output for that
invocation, made as it ran (ctrl_shim, THE DEPENDENCY PASS): the rule -M
writes with the invocation's own arguments, in its directory and environment
(every file it reads: the source, what the command line reads first, what the
source includes, system headers too), and the tree -H prints of what the
source's own #include lines read, each file under the one whose #include read
it. The gate builds no include path, lists no source and resolves no header.
It classifies each file a compile read by where it lives (WHERE A FILE LIVES)
and refuses, by name:
- THE FIRMWARE'S SIDE: a compile of a firmware source that reads a file of the
  stack outside its public headers (include/); and, in any compile, a firmware
  file whose #include line reads one (a firmware header that only a test
  compiles as C++ is held too).
- THE STACK'S SIDE: a compile of a stack source that reads, through the
  source's own #include lines, anything but the stack's files and the C
  implementation's headers (a source or header of the stack's tests/ may read
  the host's libraries outside the checkout as well: GoogleTest); and, in any
  compile, a stack file whose #include line reads anything else. What a
  compile reads first by its command line (-include, -imacros) is the
  builder's, not the source's: a file of the stack outside include/ read so,
  or a file of the checkout outside the stack read so into a compile of a
  stack source, refuses the gate (ctrl_configs, THE FILES READ FIRST), and
  what such a file reads in a compile of a stack source must be no file of the
  checkout outside the stack.
- A source a compile that passed compiled whose dependency output failed or
  is incomplete, and every fault of the capture ctrl_configs.held names (a
  missing or empty capture, a known builder it holds nothing of, an
  invocation the compiler could not expand, a compiler run by a path no
  wrapper stands on). A compile that failed compiled nothing: where its pass
  failed with it (the RV32 self-test's planted header defects), it is named
  on the run, not refused.
- A file under sw/firmware named as one of the stack's sources or public
  headers: a copy there would stand in for the stack's own.
Test equipment, and a builder's own files outside the checkout, are held by
the #include lines of the firmware and stack files they read, not by their
own: the arms use the stack's test fakes (tests/acmp_fake.hpp).

WHERE A FILE LIVES (Places), by its resolved path, in a checkout root judged
(the checkout's, and a control's copy of it) or outside every one:
- the stack's: under third_party/tsn-c-stack; public under its include/.
- the C implementation's: a file the compiler reads, or one in a directory it
  searches, when run with no argument (its baseline, from the expansion), and
  the freestanding C library headers the RV32 builds supply
  (sw/firmware/gtest/rv32_include, fw_rv32.includes), which -nostdinc leaves
  as the only C library there.
- the firmware's: under sw/firmware, but the test equipment (the harness
  sw/firmware/gtest, the host bench sw/firmware/nvm_hosttest, and every host/
  and test/ directory), and every file of the checkout an RV32 compile (one
  whose built-ins define __riscv) compiles or reads, wherever it lives: what
  the target build reads is the firmware (the images' own sources under
  test/, lwSRP).
- the checkout's: any other file of a root (test equipment, the benches).
- outside: anything else (a builder's own file, an installed tool's, the
  host's libraries).

THE CAPTURE. Without --capture the gate makes it, as the hosted
firmware-boundary and firmware-verilator jobs do, by running every known
builder the run judges (ctrl_configs.BUILDERS) under it, each by its builds
and not its suites: the suite builders by their --build-only, which builds
every binary and image the suites build and runs and plants nothing. A
capture given (--capture, made by ctrl_capture.py around any command) is
judged instead. Either way the stack's own gate and the image builders run
under it here (ctrl_runs.py). --without verilator leaves out the builders
that need Verilator, as the hosted firmware-boundary job does, and --only
verilator judges them alone, as the hosted firmware-verilator job does; each
builder and control left out is named on the run. The stack's own gate, its
scripts/check_boundary.py (the same rule under its own CMake build with gcc
and clang, and its objects' symbols), runs as well.

THE PIN (ctrl_pin.py). Every gate that builds the stack first runs the shared
pin check (ctrl_build.stack_pin): the submodule must be at its gitlink, and
its checkout the gitlink's whole tree (the same paths, types and modes, every
file hashing to the tree's blob), git reading the real objects only. This gate
does too, and holds the pin proof's census (ctrl_pin.census): the proof starts
git only through its helper. Every target of a Makefile builder whose recipe
builds against the stack must have the pin check as a prerequisite, read from
make's own dry run.

--selftest first judges an unplanted copy of the firmware and the stack, the
base every control shares, which must pass; then plants defects in copies,
each refused by name, and controls each of which must pass (ctrl_plants.py).
A control's planted builder compiles the copy, through a capture of its own,
as the builders do (the image builder's compile, the arms' flags and include
path) or in a spelling of its own; what it compiled is judged, with the run's
capture beside it for what a capture must hold. Then the pin controls
(ctrl_pin.pin_controls). Then the firmware's README must give the self-test's
own population (figures): its defects and passing controls in the firmware
builders' run, its defects in the Verilator builders' run and its pin
controls; a copy of the page with each figure one more is refused by name.
--require-rv32 refuses, rather than skips, the RV32 arm when no RV32 compiler
is found.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture DIR --without verilator

Exit 0 = both sides hold; 1 = a finding or a control that misbehaved; 2 =
refused (no compiler, cmake or clang, the stack's gate could not run, or the
capture is missing, empty or incomplete).
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import ctrl_capture  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import CTRL, NVM_DIR, ROOT, STACK, STACK_INCLUDE, STACK_PARTS, Refusal, stack_pin  # noqa: E402
from ctrl_capture import Capture, CaptureError, Deps, Invocation  # noqa: E402
from ctrl_configs import BUILDERS, COMPILED, NEEDS, Scope, command, failed, held, makefiles, once  # noqa: E402
from ctrl_pin import makefile_findings, named_compilers, pin_controls, proof_census  # noqa: E402
from ctrl_plants import BASE, PLANTS, Plant  # noqa: E402
from ctrl_runs import captures, control_capture, owned, stack_gate  # noqa: E402

#: Where the stack lives in a checkout root.
STACK_REL = STACK.relative_to(ROOT).as_posix()
#: The freestanding C library headers the RV32 builds supply (fw_rv32.includes): the C library there.
C_LIBRARY_REL = (Path(fw_rv32.__file__).resolve().parent / "rv32_include").relative_to(ROOT).as_posix()
#: The firmware's tree in a checkout root.
FIRMWARE_REL = "sw/firmware"
#: The parts of the firmware's tree that hold test equipment, and the directories that do inside any part.
EQUIPMENT_PARTS = ("gtest", "nvm_hosttest")
EQUIPMENT_DIRS = ("host", "test")
#: What a file is (Places.kind).
PUBLIC, STACK_FILE, IMPLEMENTATION, FIRMWARE, CHECKOUT, OUTSIDE = (
    "public", "stack", "implementation", "firmware", "checkout", "outside")
#: What a stack file reads that it may not.
NOT_OURS = "which is neither the stack's nor the C implementation's"
#: The builtin an RV32 compile's expansion defines.
TARGET = "__riscv"
#: Copies of the trees a control plants into, at once.
JOBS = 4
#: The firmware's page, which gives the self-test's population (figures). Its name is joined from stem and
#: suffix for the reason fw_coverage.README gives.
README = CTRL / ("README" + ".md")
#: Each figure the page gives of the self-test's population: what it counts, and the sentence it is in.
FIGURES = (("defects in the firmware builders' run", re.compile(r"It then plants (\d+) defects, each refused by name")),
           ("passing controls in the firmware builders' run",
            re.compile(r"each refused by name, and (\d+) passing controls, where the firmware builders' capture is")),
           ("defects in the Verilator builders' run",
            re.compile(r"Where the Verilator builders' capture is, it plants (\d+) more")),
           ("pin controls", re.compile(r"(\d+) pin controls follow the boundary controls")))


# ---- where a file lives -------------------------------------------------------------------


@dataclass
class Places:
    """The checkout roots judged (resolved; a control's copy before the checkout), and the files of the checkout,
    from a root, that an RV32 compile compiles or reads; each file's kind, worked out once per baseline."""

    roots: tuple[Path, ...]
    target: frozenset[str]
    known: dict[tuple[str, tuple[str, ...]], str] = field(default_factory=dict)

    def located(self, path: str) -> tuple[Path | None, str]:
        """The root a file lies in, and its path from there; (None, the path) outside every root."""
        for root in self.roots:
            top = str(root)
            if path.startswith(top + "/"):
                return root, path[len(top) + 1:]
        return None, path

    def kind(self, path: str, implementation: tuple[str, ...]) -> str:
        """Where a file lives (see WHERE A FILE LIVES); `implementation` is the compile's baseline (files read and
        directories searched)."""
        key = (path, implementation)
        if key not in self.known:
            self.known[key] = self.classify(path, implementation)
        return self.known[key]

    def classify(self, path: str, implementation: tuple[str, ...]) -> str:
        """kind, worked out."""
        root, rel = self.located(path)
        if root is not None and rel.startswith(STACK_REL + "/"):
            return PUBLIC if rel.startswith(f"{STACK_REL}/{STACK_INCLUDE}/") else STACK_FILE
        if root is not None and rel.startswith(C_LIBRARY_REL + "/"):
            return IMPLEMENTATION
        if any(path == own or path.startswith(own.rstrip("/") + "/") for own in implementation):
            return IMPLEMENTATION
        if root is None:
            return OUTSIDE
        parts = rel.split("/")
        firmware = rel.startswith(FIRMWARE_REL + "/") and len(parts) > 3 and parts[2] not in EQUIPMENT_PARTS and \
            not any(part in EQUIPMENT_DIRS for part in parts[3:-1])
        return FIRMWARE if firmware or rel in self.target else CHECKOUT

    def name(self, path: str) -> str:
        """A file, named by where it lives: the stack's from the stack (tsn-c-stack/...), the checkout's from its
        root, anything else in full."""
        root, rel = self.located(path)
        if root is None:
            return path
        return "tsn-c-stack/" + rel[len(STACK_REL) + 1:] if rel.startswith(STACK_REL + "/") else rel

    def tests(self, path: str) -> bool:
        """Whether a file is one of the stack's tests (its tests/), which may read the host's libraries."""
        return self.located(path)[1].startswith(f"{STACK_REL}/tests/")


def implementation(inv: Invocation) -> tuple[str, ...]:
    """What the compiler reads and searches on its own (its baseline in each language the invocation compiles)."""
    made = inv.expansion
    return tuple(sorted(frozenset().union(*(b.own for _, b in made.baseline)))) if made is not None else ()


def targets(capture: Capture, roots: tuple[Path, ...]) -> frozenset[str]:
    """Every file of a root, from that root, that an RV32 compile of the capture compiles or reads (its expansion's
    built-ins define __riscv)."""
    def of(leaf: Capture) -> frozenset[str]:
        """targets of one capture part."""
        places = Places(roots, frozenset())
        found: set[str] = set()
        for inv in leaf.invocations:
            if inv.expansion is None or not any(n == TARGET for u in inv.expansion.units for n, _, _ in u.builtins):
                continue
            for source in inv.sources:
                files = (source.path, *(source.deps.files if source.deps is not None else ()))
                found.update(rel for root, rel in map(places.located, files) if root is not None)
        return frozenset(found)
    return frozenset().union(*(once(f"targets {roots}", leaf, of) for leaf in capture.leaves))


# ---- the two sides ------------------------------------------------------------------------


def findings_of(source: str, deps: Deps, impl: tuple[str, ...], places: Places) -> list[str]:
    """Every finding one compiled source's dependency list shows (see THE FIRMWARE'S SIDE, THE STACK'S SIDE)."""
    name, kind = places.name, lambda path: places.kind(path, impl)
    edges = deps.edges(source)
    through = {path: includer for includer, path in reversed(edges)}
    found = []
    side = kind(source)
    if side == FIRMWARE:
        for path in deps.files:
            if kind(path) == STACK_FILE:
                via = f" (included by {name(through[path])})" if through.get(path, source) != source else ""
                found.append(f"firmware: {name(source)} reads {name(path)}{via}, not one of the stack's public "
                             "headers")
    if side in (PUBLIC, STACK_FILE):
        for path, includer in through.items():
            if kind(path) not in admitted(places, source):
                found.append(f"stack: {name(source)} reads {name(path)} (included by {name(includer)}), {NOT_OURS}")
        command_line = set(deps.files) - set(through)
        for path in sorted(command_line):
            if kind(path) in (FIRMWARE, CHECKOUT):
                found.append(f"stack: a compile of {name(source)} reads {name(path)}, which its command line reads "
                             "first: a file of the checkout outside the stack")
    for includer, path in edges:
        if kind(includer) == FIRMWARE and kind(path) == STACK_FILE:
            found.append(f"firmware: {name(includer)} includes {name(path)}, not one of the stack's public headers")
        if kind(includer) in (PUBLIC, STACK_FILE) and kind(path) not in admitted(places, includer):
            found.append(f"stack: {name(includer)} includes {name(path)}, {NOT_OURS}")
    return found


def admitted(places: Places, includer: str) -> tuple[str, ...]:
    """What a stack file's #include line may read: the stack's files and the C implementation's; for one of the
    stack's tests, the host's libraries outside the checkout too."""
    base = (PUBLIC, STACK_FILE, IMPLEMENTATION)
    return (*base, OUTSIDE) if places.tests(includer) else base


def judged(capture: Capture, places: Places) -> dict[str, frozenset[str]]:
    """Every finding the capture's compiles show, each with the builders of a compile that shows it (the fewest);
    one compiled source's findings are worked out once per dependency list, its kind and its baseline."""
    found: dict[str, frozenset[str]] = {}
    seen: dict[tuple[str, int, tuple[str, ...]], list[str]] = {}
    for inv in capture.invocations:
        impl = implementation(inv)
        for source in inv.sources:
            if source.lang not in COMPILED or source.deps is None:
                continue
            side = places.kind(source.path, impl)
            key = (source.path if side not in (OUTSIDE, CHECKOUT) else side, id(source.deps), impl)
            if key not in seen:
                seen[key] = findings_of(source.path, source.deps, impl, places)
            for core in seen[key]:
                if core not in found or len(inv.builders) < len(found[core]):
                    found[core] = inv.builders
    return found


def counted(capture: Capture, places: Places) -> dict[str, int]:
    """How many compiled sources each side's compiles compile: the firmware's, the stack's, and the rest."""
    counts = {FIRMWARE: 0, "stack": 0, "rest": 0}
    for inv in capture.invocations:
        impl = implementation(inv)
        for source in inv.sources:
            if source.lang in COMPILED:
                side = places.kind(source.path, impl)
                counts[side if side == FIRMWARE else "stack" if side in (PUBLIC, STACK_FILE) else "rest"] += 1
    return counts


def shadows(roots: tuple[Path, ...]) -> list[str]:
    """No file under sw/firmware is named as a source or public header of the stack."""
    found = []
    for root in roots:
        stack, firmware = root / STACK_REL, root / FIRMWARE_REL
        names = {p.name for part in STACK_PARTS for p in (stack / part).iterdir() if p.is_file()}
        found += [f"firmware: {p.relative_to(root).as_posix()} has the name of the stack's {p.name}"
                  for p in sorted(firmware.rglob("*")) if p.is_file() and p.name in names]
    return found


def judge(capture: Capture, roots: tuple[Path, ...], scope: Scope, target: frozenset[str] = frozenset(),
          control: Plant | None = None, own: Capture | None = None) -> list[str]:
    """Every finding on both sides of the boundary in the capture's compiles (in `own`'s alone, a control's, with
    the run's capture beside it for what a capture must hold), named with the builders of a compile that shows
    it; `target` adds files the run's RV32 compiles read."""
    texts = {HERE / name: text for name, text in control.texts} if control else None
    forgot = control.alter.removeprefix("forget ") if control and control.alter.startswith("forget ") else ""
    held(capture, scope, texts, roots, own, tuple(b for b in BUILDERS if b.path != forgot))
    judging = own if own is not None else capture
    places = Places(tuple(r.resolve() for r in roots), targets(judging, roots) | target)
    found = judged(judging, places)
    return [f"{core} [{', '.join(sorted(builders)) or 'a builder'}]" for core, builders in found.items()] + \
        shadows(roots)


# ---- the planted controls (ctrl_plants) -----------------------------------------------------


def mirror(plant: Plant, work: Path) -> Path:
    """A copy of the firmware's tree and the stack, laid out as in the checkout, with one plant written into it."""
    root = work / "root"
    shutil.rmtree(root, ignore_errors=True)
    for tree in (CTRL, NVM_DIR):
        shutil.copytree(tree, root / tree.relative_to(ROOT), ignore=shutil.ignore_patterns("__pycache__"))
    for part in ("src", STACK_INCLUDE, "tests", "examples"):
        shutil.copytree(STACK / part, root / STACK_REL / part)
    tops = {"ctrl": root / CTRL.relative_to(ROOT), "stack": root / STACK_REL, "nvm": root / NVM_DIR.relative_to(ROOT)}
    for file, old, new in ((plant.file, plant.old, plant.new), *plant.extra):
        if not file:
            continue
        top = tops[plant.side]
        if file.startswith("+"):
            target = top / file[1:]
            if target.exists():
                raise Refusal(f"control {plant.name!r}: {file[1:]} exists already")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new, encoding="utf-8")
            continue
        text = (top / file).read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"control {plant.name!r}: its anchor occurs {text.count(old)} times in {file}")
        (top / file).write_text(text.replace(old, new), encoding="utf-8")
    return root


def control(plant: Plant, base: Capture, work: Path, scope: Scope, target: frozenset[str]) -> tuple[bool, str]:
    """One control: its copy planted, its builder run, and its verdict against what it names."""
    try:
        root = mirror(plant, work)
        capture, own = control_capture(plant, root, base, work / "run")
        findings = judge(capture, (root, ROOT), scope, target, plant, own)
    except (Refusal, CaptureError) as exc:
        findings = [f"REFUSED: {exc}"]
    shutil.rmtree(work, ignore_errors=True)
    ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
    shown = next((f for f in findings if plant.needle and plant.needle in f), findings[0] if findings else "")
    return ok, f"[{'ok' if ok else 'ESCAPED'}] boundary control {plant.name}: {shown or 'passes'}"


def controls(work: Path, run: Capture, scope: Scope) -> tuple[int, int]:
    """The base the controls share passing, every plant of the run's scope refused by the finding it names, every
    pass control passing, each other plant named as left out; the misbehaving count and the controls run."""
    plants = [plant for plant in PLANTS if scope.judges(plant.needs)]
    for plant in PLANTS:
        if not scope.judges(plant.needs):
            print(f"  LEFT OUT: boundary control {plant.name}, judged where its builders' capture is (needs "
                  f"{plant.needs or 'the firmware builders'})")
    target = targets(run, (ROOT,))
    bad = 0
    with ThreadPoolExecutor(max_workers=JOBS, thread_name_prefix="ctrl-boundary-plant") as runner:
        futures = [runner.submit(control, plant, run, work / str(at), scope, target)
                   for at, plant in enumerate((BASE, *plants))]
        for future in futures:
            ok, line = future.result()
            print(line, flush=True)
            bad += not ok
    return bad, 1 + len(plants)


# ---- the README's figures of the self-test -------------------------------------------------------


def population(pins: int) -> dict[str, int]:
    """The self-test's own population, counted from its controls, for each figure the page gives."""
    firmware = [plant for plant in PLANTS if not plant.needs]
    return dict(zip((what for what, _ in FIGURES),
                    (sum(bool(p.needle) for p in firmware), sum(not p.needle for p in firmware),
                     sum(plant.needs == "verilator" for plant in PLANTS), pins), strict=True))


def figures(text: str, counts: dict[str, int]) -> list[str]:
    """Each figure the page (`text`) gives that is not the self-test's own count, or that it gives not once."""
    findings = []
    for what, sentence in FIGURES:
        said = [int(n) for n in sentence.findall(text)]
        if said != [counts[what]]:
            findings.append(f"{README.relative_to(ROOT)} gives the {what} as "
                            f"{', '.join(map(str, said)) or 'nothing'}, where the self-test has {counts[what]}")
    return findings


def figure_controls(text: str, counts: dict[str, int]) -> tuple[int, int]:
    """The page with each figure one more, which must be refused naming that figure; the misbehaving count and
    the controls run."""
    bad = 0
    for what, sentence in FIGURES:
        found = sentence.search(text)
        planted = text[:found.start(1)] + str(int(found[1]) + 1) + text[found.end(1):] if found else text
        named = [f for f in figures(planted, counts) if what in f]
        ok = found is not None and len(named) == 1
        print(f"[{'ok' if ok else 'ESCAPED'}] figure control, the page's {what} one more: "
              f"{named[0] if named else 'no finding'}", flush=True)
        bad += not ok
    return bad, len(FIGURES)


def summary(capture: Capture, scope: Scope, ran: list[str]) -> None:
    """What the run judges: the capture's invocations and builders, those left out, and the gate's own runs."""
    known = [b.path for b in BUILDERS if b.path in capture.builders]
    print(f"capture: {len(capture.invocations)} compiler invocations from {len(capture.commands)} builder runs; "
          f"every known builder held: {', '.join(known)}")
    for b in scope.left_out():
        print(f"  LEFT OUT: {b.path}, which needs {NEEDS[b.needs]}, which this run has none of (--without {b.needs})"
              if b.needs else f"  LEFT OUT: {b.path}, which the run that holds the firmware builders judges (--only "
              f"{scope.only})")
    if scope.only:
        print("  the builders found by text are cross-checked by the run that holds the firmware builders")
    nothing = failed(capture)
    if nothing:
        print(f"  {len(nothing)} compile(s) failed, each with its dependency pass, and compiled nothing: "
              f"{'; '.join(command(inv) for inv in nothing[:3])}{' ...' if len(nothing) > 3 else ''}")
    print("\n".join(ran), flush=True)


def main(argv: list[str] | None = None) -> int:
    """Hold both sides and every Makefile builder's pin prerequisites, with the stack's own gate beside them; with
    --selftest, the controls first."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--selftest", action="store_true", help="also plant every control and require its verdict")
    ap.add_argument("--require-rv32", action="store_true", help="refuse, not skip, without an RV32 compiler")
    ap.add_argument("--capture", type=Path, action="append",
                    help="a capture of the builders' invocations (ctrl_capture.py), repeatable; without one, the "
                         "gate runs every known builder under its own")
    ap.add_argument("--without", action="append", choices=sorted(NEEDS), default=[],
                    help="leave out the builders that need this, which the run has none of (each is named)")
    ap.add_argument("--only", choices=sorted(NEEDS), default="",
                    help="judge only the builders that need this, and the controls that need them (each other one "
                         "is named)")
    args = ap.parse_args(argv)
    if args.only in args.without:
        ap.error("--only and --without name the same builders")
    scope = Scope(frozenset(args.without), args.only)
    rv32 = fw_rv32.compiler()
    if rv32 is None and args.require_rv32:
        print("REFUSED: no RV32 compiler (the pinned SDK's riscv32-linux-gcc or MILAN_RV32_CC)")
        return 2
    if rv32 is None:
        print("  SKIPPED: the RV32 arm, no RV32 compiler; --require-rv32 refuses instead")
    try:
        with tempfile.TemporaryDirectory(prefix="ctrl-boundary-") as tmp, ThreadPoolExecutor(1) as beside:
            work = Path(tmp)
            print(f"tsn-c-stack at {stack_pin()}", flush=True)
            mine = work / "capture"
            build = beside.submit(stack_gate, False, work / "stack-gate-build", mine)
            given = captures(args.capture, work, scope)
            ran = owned(mine, work / "images")
            said, refused = build.result()
            # the stack's own self-test runs beside the controls; its build is the one the capture holds
            own = beside.submit(stack_gate, True, work / "stack-gate", None) if args.selftest else None
            env = ctrl_capture.install(mine)
            named = [record for makefile in makefiles() for record in named_compilers(makefile, env)]
            capture = sum(given[1:], given[0]) + ctrl_capture.load(mine) + Capture((), (), (), tuple(named))
            held(capture, scope)
            summary(capture, scope, ran)
            bad = pins = planted_count = figure_count = 0
            stated = []
            if args.selftest:
                bad, planted_count = controls(work / "controls", capture, scope)
                (work / "pins").mkdir()
                misbehaved, pins = pin_controls(work / "pins", makefiles())
                bad += misbehaved
                page = README.read_text(encoding="utf-8")
                stated = figures(page, population(pins))
                misbehaved, figure_count = figure_controls(page, population(pins))
                bad += misbehaved
            findings = judge(capture, (ROOT,), scope)
            counts = counted(capture, Places((ROOT.resolve(),), targets(capture, (ROOT,))))
            findings += makefile_findings(makefiles(), work / "makefiles") + proof_census() + stated
            if own is not None:
                said, tested = own.result()
                refused += tested
            print("\n".join(said), flush=True)
            findings += refused
    except (Refusal, CaptureError) as exc:
        print(f"REFUSED: {exc}")
        return 2
    for finding in findings:
        print(f"  [FAIL] {finding}")
    tested = (f", {planted_count} boundary, {pins} pin and {figure_count} figure controls, {bad} misbehaved"
              if args.selftest else "")
    print(f"ctrl_boundary: {sum(counts.values())} compiled sources of {len(capture.invocations)} recorded invocations "
          f"({counts[FIRMWARE]} the firmware's, {counts['stack']} the stack's, {counts['rest']} test equipment's "
          f"and builders' own), each judged by what its dependency output lists, host{' and RV32' if rv32 else ''}, "
          f"every Makefile builder's pin prerequisites and the pin proof's census; {len(findings)} finding(s)"
          f"{tested}")
    print(f"ctrl_boundary: {'FAIL' if findings or bad else 'PASS'}")
    return 1 if findings or bad else 0


if __name__ == "__main__":
    sys.exit(main())
