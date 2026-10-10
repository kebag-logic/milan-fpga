#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_boundary.py - the TSN stack's boundary, held from both sides (#697).

THE STACK'S SIDE. Every source and public header of the tsn-c-stack submodule
(src/*.c, include/*.h) is preprocessed with this firmware's own include path
and flags, as the host arms compile it (ctrl_build.includes, C_FLAGS) and as
the RV32 build does (RV32_FLAGS and the freestanding headers of fw_rv32), and
its dependencies are read from the compiler. Each must be one of the stack's
public headers or a header of the C library the compiler supplies. A
dependency anywhere else (the mailbox driver or its HAL, the generated
register-map contract, the MMIO platform, the app, the loop, the store, an
image) is refused by name; one that does not resolve is refused too. The
stack's tests (tests/*.cpp, tests/*.hpp), which the arms compile with the
firmware's test include path (ctrl_build.compile_tests), are preprocessed as
C++ the same way: they may reach anything of the stack and the host's own
libraries (the C++ library, GoogleTest), and nothing of milan-fpga outside
the submodule. The stack's own gate, its scripts/check_boundary.py (the same
rule under its own CMake build with gcc and clang, and its objects' symbols),
runs as well.

THE FIRMWARE'S SIDE. Every firmware source and header under sw/firmware/ctrl
(not the host model or the tests) and the measured images' own sources reach
the stack through its public headers only. Each is preprocessed on the host
and with the RV32 compiler, with the firmware's include path and the stack's
other directories searched last, so a header only they hold resolves there; a
generated header nobody has generated is named, not read; a dependency inside
the stack outside include/ is refused. No file under sw/firmware may be named
as one of the stack's sources or public headers: a copy there would shadow, or
stand in for, the stack's own.

EVERY CONFIGURATION. Both sides are judged in every configuration the
firmware's builders compile them in. The build modes are read from the
builders themselves (every -D or -U flag written in ctrl_build.py,
ctrl_arms.py, srp_arms.py, the two image fixtures, the MAAP differential and
the mailbox bench's Makefile), never restated here. The compiler reports each
macro a unit's preprocessing tests or expands (-dU). Starting with every other
mode's macro defined, so that a test of any of them is reported, the gate
preprocesses each unit under every combination of the modes of the macros it
tests, until no new one appears: a mode the unit never tests cannot change
what it includes. A finding names the mode flags, beyond the unit's default
build, of the smallest configuration that reaches it.

Every gate that builds the stack first runs the shared pin check
(ctrl_build.stack_pin): the submodule must be at its gitlink, and every file of
its sources, headers, tests, examples, scripts and CMake files must hash to the
gitlink's tree. This gate does too.

--selftest first plants defects in copies of the two trees, each of which must
be refused by name, and controls each of which must pass; then the pin
check's controls (a clone of the stack at its gitlink passes; the clone with a
source, a test, a script or a CMake file edited, with an edit hidden from git
status, with a file the tree does not hold, or at another revision, is
refused; the mailbox bench and the MAAP differential, in both its modes,
refuse the edited clone before building it); then runs the stack gate's own
self-test. --require-rv32 refuses, rather than skips, the RV32 arm when no RV32
compiler is found.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest

Exit 0 = both sides hold; 1 = a finding or a control that misbehaved; 2 =
refused (no compiler, GoogleTest, cmake or clang, or the stack's gate could
not run).
"""

from __future__ import annotations

import argparse
import ast
import itertools
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import fw_gtest  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import (C_FLAGS, CTRL, NVM_DIR, ROOT, RV32_FLAGS, STACK, STACK_INCLUDE, STACK_PARTS,  # noqa: E402
                        TB_MBX, Refusal, Tree, includes, stack_gitlink, stack_pin)

#: The C library's headers (ISO C11, 7.1.2): what the stack may include beside its own.
C_HEADERS = ("assert complex ctype errno fenv float inttypes iso646 limits locale math stdalign stdarg stdatomic "
             "stdbool stddef stdint stdio stdlib stdnoreturn string tgmath uchar wchar wctype").split()
#: The stack's directories other than its public headers, searched last on the firmware's side.
STACK_PRIVATE = ("src", "tests", "examples")
#: The firmware's directories under sw/firmware/ctrl; host/ and test/ are test equipment.
FIRMWARE_DIRS = ("mbx", "port", "loop", "adp", "maap", "acmp", "app", "plat", "srp")
#: The measured images' own sources (ctrl_image.py, ctrl_srp_image.py).
IMAGE_SOURCES = ("test/rv32_image/image_main.c", "test/rv32_image/image_arith.c", "test/rv32_image/image_rt.c",
                 "test/ctrl_image.c")
#: The firmware side's default build, the release the images ship (NDEBUG), and what its sources need
#: defined to preprocess at all: the window's address (plat/), a shape's stream counts (the image) and
#: lwSRP's Milan profile (srp/). The builders' modes, the SRP image's among them, vary on top of it.
FIRMWARE_DEFINES = ("-DNDEBUG", "-DCTRL_MBX_BASE=0x80000000u", "-DIMAGE_SINKS=1u", "-DIMAGE_SOURCES=1u",
                    "-DLWSRP_MILAN=1")
LWSRP = ROOT / "third_party/lwSRP/src"
#: The entity the SRP adapter's generated shape is taken from, as the SRP arms take it by default.
SRP_ENTITY = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
#: The stack's own gate, from the submodule.
STACK_GATE = STACK / "scripts/check_boundary.py"
#: The firmware's builders: every -D or -U flag written in one is a build mode the boundary is judged in.
BUILDERS = (HERE / "ctrl_build.py", HERE / "ctrl_arms.py", HERE / "srp_arms.py", HERE / "ctrl_image.py",
            HERE / "ctrl_srp_image.py", HERE / "maap_differential.py", TB_MBX / "Makefile")
#: A -D or -U flag, its macro's name in group 1.
FLAG = re.compile(r"-[DU]([A-Za-z_]\w*)(?:=.*)?", re.S)
#: A line -dU writes for a macro the preprocessing tested or expanded.
TESTED = re.compile(r"^#(?:define|undef) ([A-Za-z_]\w*)", re.M)
#: The compiler's report of a header it could not find.
MISSING = re.compile(r"fatal error: (.+?): No such file or directory")
#: Units preprocessed at once.
JOBS = 4
#: How many times each judgement preprocessed a unit, one entry per side judged.
PREPROCESSED: list[int] = []


@dataclass(frozen=True)
class Trees:
    """The ctrl tree and the stack being judged: the checkout's, or planted copies."""

    ctrl: Path
    stack: Path


@dataclass(frozen=True)
class Seen:
    """One unit preprocessed in one configuration: the mode flags beyond its default build, and its
    dependencies, or its error."""

    label: str
    deps: frozenset[Path]
    error: str


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One tool, its output captured, its messages in English."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False,
                          env={**os.environ, "LC_ALL": "C"})


# ---- the build modes, from the builders -----------------------------------------------------

def mode_flags(path: Path, text: str) -> list[str]:
    """The -D and -U flags written in one builder: its string literals (a Python builder) or the words of its
    recipes (a Makefile). A flag computed at run time (a shape's stream count, a test's expectation) is a
    value the build supplies, not a mode."""
    if path.suffix == ".py":
        tree = ast.parse(text)
        computed = {id(part) for node in ast.walk(tree) if isinstance(node, ast.JoinedStr) for part in node.values}
        return [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and id(node) not in computed
                and isinstance(node.value, str) and FLAG.fullmatch(node.value)]
    words = (word.strip("\"'") for line in text.splitlines() for word in line.split("#", 1)[0].split())
    return [word for word in words if FLAG.fullmatch(word)]


def modes(planted: dict[Path, str] | None = None) -> dict[str, tuple[str, ...]]:
    """Every macro the builders set or clear, with each flag they write for it, read from the builders (with
    `planted` replacing a builder's text, for the self-test)."""
    found: dict[str, dict[str, None]] = {}
    for path in BUILDERS:
        text = (planted or {}).get(path) or path.read_text(encoding="utf-8")
        for flag in mode_flags(path, text):
            found.setdefault(FLAG.fullmatch(flag)[1], {})[flag] = None
    return {name: tuple(flags) for name, flags in sorted(found.items())}


def state(flag: str | None) -> tuple[str, ...]:
    """What a -D or -U flag leaves its macro as: defined with a value, or undefined."""
    if flag is None or flag.startswith("-U"):
        return ("undefined",)
    return ("defined", flag[2:].partition("=")[2] or "1")


def default(argv: list[str], name: str) -> tuple[str, ...]:
    """What the unit's own flags leave `name` as; the last flag for it wins."""
    return state(next((a for a in reversed(argv) if (m := FLAG.fullmatch(a)) and m[1] == name), None))


def preprocess(argv: list[str], unit: Path, work: Path, standins: Path | None) -> tuple[set[Path], set[str]] | str:
    """The files the compiler reads for `unit` under `argv`, and the macros its preprocessing tests or expands
    (-dU), or its error. With `standins`, a header nobody supplies by its plain name (a generated one) is
    named, not read: an empty stand-in of it is written there, searched last. A path through ".." or from
    the root that resolves nowhere is an error, never stood in for."""
    work.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=".i", dir=work)
    os.close(fd)
    out = Path(name)
    dep = out.with_suffix(".d")
    extra = ["-idirafter", str(standins)] if standins else []
    try:
        for _ in range(64):
            res = run([*argv, *extra, "-E", "-dU", "-P", "-MD", "-MF", str(dep), "-MT", "boundary", "-o", str(out),
                       str(unit)])
            missing = Path(found[1]) if standins and (found := MISSING.search(res.stderr)) else None
            if res.returncode == 0 or missing is None or missing.is_absolute() or ".." in missing.parts or \
                    (standins / missing).exists():
                break
            (standins / missing).parent.mkdir(parents=True, exist_ok=True)
            (standins / missing).write_text("", encoding="utf-8")
        if res.returncode != 0:
            said = [ln.split("error:", 1)[1].strip() for ln in res.stderr.splitlines() if "error:" in ln]
            return said[0] if said else res.stderr.strip() or f"exit {res.returncode}"
        names = shlex.split(dep.read_text(encoding="utf-8").replace("\\\n", " ").split(":", 1)[1])
        return {Path(n) for n in names}, set(TESTED.findall(out.read_text(encoding="utf-8", errors="replace")))
    finally:
        out.unlink(missing_ok=True)
        dep.unlink(missing_ok=True)


def explore(argv: list[str], unit: Path, universe: dict[str, tuple[str, ...]], work: Path,
            standins: Path | None = None) -> list[Seen]:
    """`unit` preprocessed in its default build, then under every combination of the modes of the macros it
    tests, every other mode's macro defined, until no new one appears."""
    choices = {}
    for name, flags in universe.items():
        base = default(argv, name)
        other = list(dict.fromkeys((f,) for f in flags if state(f) != base))
        if other:
            choices[name] = [(), *other]
    seed = {n: () if default(argv, n)[0] == "defined" else next(c for c in cs if c and c[0].startswith("-D"))
            for n, cs in choices.items()}
    tested: list[str] = []
    runs: dict[tuple[str, ...], tuple[dict[str, tuple[str, ...]], tuple[set[Path], set[str]] | str]] = {}

    def visit(config: dict[str, tuple[str, ...]]) -> bool:
        """Preprocess in one configuration; True when it tested a mode's macro not seen tested before."""
        # an -U first, so a mode's value replaces the default's without a redefinition warning
        flags = tuple(f for n in choices for flag in config[n]
                      for f in ((f"-U{n}", flag) if flag.startswith("-D") else (flag,)))
        if flags in runs:
            return False
        result = preprocess([*argv, *flags], unit, work, standins)
        runs[flags] = (config, result)
        new = [] if isinstance(result, str) else [n for n in choices if n in result[1] and n not in tested]
        tested.extend(new)
        return bool(new)

    visit({n: () for n in choices})
    grew = True
    while grew:
        grew = False
        for pick in itertools.product(*(choices[n] for n in tested)):
            grew = visit({**seed, **dict(zip(tested, pick))}) or grew
    seen = []
    for config, result in runs.values():
        # a run that failed tested nothing it could report: its label is its whole configuration
        named = [n for n in choices if n in tested or isinstance(result, str)]
        label = " ".join(flag for n in named for flag in config[n])
        seen.append(Seen(label, frozenset(), result) if isinstance(result, str) else
                    Seen(label, frozenset(d.resolve() for d in result[0] if d.is_absolute() or d.exists()), ""))
    return seen


def judged(units: list[Path], argv: list[str], universe: dict[str, tuple[str, ...]], work: Path,
           standins: Path | None = None) -> list[tuple[Path, list[Seen]]]:
    """Every unit explored, a few at once."""
    with ThreadPoolExecutor(max_workers=JOBS) as pool:
        result = list(zip(units, pool.map(lambda u: explore(argv, u, universe, work / "pp", standins), units)))
    PREPROCESSED.append(sum(len(seen) for _, seen in result))
    return result


def smallest(found: dict[tuple[str, str], list[str]]) -> list[str]:
    """Each finding once, named by the smallest configuration that reaches it."""
    return [f"{side}{f' [{min(labels, key=lambda s: (len(s.split()), s))}]' if all(labels) else ''}: {core}"
            for (side, core), labels in found.items()]


# ---- the stack's side ---------------------------------------------------------------------

@lru_cache(maxsize=None)
def c_library(argv: tuple[str, ...]) -> frozenset[Path]:
    """The C library headers the compiler supplies under `argv` without the firmware's paths: the closure of
    every standard header it has."""
    work = Path(tempfile.mkdtemp(prefix="c-library-"))
    found: set[Path] = set()
    for header in C_HEADERS:
        probe = work / f"probe_{header}.c"
        probe.write_text(f"#include <{header}.h>\n", encoding="utf-8")
        res = run([*argv, "-M", "-MT", "boundary", str(probe)])
        if res.returncode == 0:
            names = shlex.split(res.stdout.replace("\\\n", " ").split(":", 1)[1])
            found |= {Path(n).resolve() for n in names if Path(n).resolve() != probe.resolve()}
    shutil.rmtree(work)
    if not found:
        raise Refusal(f"{argv[0]} supplies no C library header")
    return frozenset(found)


def library_flags(compiler: list[str], label: str) -> tuple[str, ...]:
    """The compiler's own flags and a configuration's mode flags, for the C library it supplies there."""
    flags = [f for word in label.split() for f in ((f"-U{FLAG.fullmatch(word)[1]}", word)
                                                    if word.startswith("-D") else (word,))]
    return tuple(compiler + flags)


def stack_side(trees: Trees, compiler: list[str], label: str, universe: dict[str, tuple[str, ...]],
               work: Path) -> list[str]:
    """The stack's sources and public headers, preprocessed under the firmware's flags in every configuration:
    every dependency is the stack's public header or the C library's."""
    public = (trees.stack / STACK_INCLUDE).resolve()
    units = sorted((trees.stack / "src").glob("*.c")) + sorted((trees.stack / STACK_INCLUDE).glob("*.h"))
    argv = [*compiler, *includes(Tree(trees.ctrl, work, work, stack=trees.stack)), "-x", "c"]
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, argv, universe, work / label):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.error:
                found.setdefault((label, f"the stack's {name} does not preprocess with the firmware's flags: "
                                         f"{s.error}"), []).append(s.label)
                continue
            library = c_library(library_flags(compiler, s.label))
            for dep in sorted(s.deps):
                if dep != unit.resolve() and not dep.is_relative_to(public) and dep not in library:
                    found.setdefault((label, f"the stack's {name} includes {where(dep, trees)}"), []).append(s.label)
    return smallest(found)


def tests_side(trees: Trees, universe: dict[str, tuple[str, ...]], work: Path) -> list[str]:
    """The stack's tests, preprocessed as the arms compile them in every configuration: nothing of milan-fpga
    outside the stack."""
    argv = ["g++", *fw_gtest.CXX_FLAGS, *includes(Tree(trees.ctrl, work, work, stack=trees.stack)),
            f"-I{trees.stack / 'tests'}", f"-idirafter{trees.stack / 'examples'}"]
    probe = work / "gtest_probe.cpp"
    work.mkdir(parents=True, exist_ok=True)
    probe.write_text("#include <gtest/gtest.h>\n#include <gmock/gmock.h>\n", encoding="utf-8")
    if isinstance(preprocess(argv, probe, work, None), str):
        raise Refusal("the stack's tests need GoogleTest's and GoogleMock's headers")
    units = sorted((trees.stack / "tests").glob("*.cpp")) + sorted((trees.stack / "tests").glob("*.hpp"))
    stack = trees.stack.resolve()
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, [*argv, "-x", "c++"], universe, work):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.error:
                found.setdefault(("tests", f"the stack's {name} does not preprocess with the firmware's test "
                                           f"flags: {s.error}"), []).append(s.label)
                continue
            for dep in sorted(s.deps):
                if not dep.is_relative_to(stack) and (dep.is_relative_to(trees.ctrl.resolve()) or
                                                      dep.is_relative_to(ROOT.resolve())):
                    found.setdefault(("tests", f"the stack's {name} includes {where(dep, trees)}"),
                                     []).append(s.label)
    return smallest(found)


def where(path: Path, trees: Trees) -> str:
    """A dependency, named by where it lives."""
    for root, label in ((trees.ctrl, "sw/firmware/ctrl/"), (trees.stack, "tsn-c-stack/"), (ROOT, "")):
        if path.is_relative_to(root.resolve()):
            return label + path.relative_to(root.resolve()).as_posix()
    return str(path)


# ---- the firmware's side ------------------------------------------------------------------

def firmware_units(trees: Trees) -> list[Path]:
    """The firmware's sources and headers, and the measured images' own sources."""
    units = [p for d in FIRMWARE_DIRS for p in sorted((trees.ctrl / d).glob("*.[ch]"))]
    return units + [trees.ctrl / s for s in IMAGE_SOURCES]


def firmware_flags(trees: Trees, compiler: list[str], work: Path) -> list[str]:
    """The firmware's include path as its builds give it, with the stack's other directories last, and the
    SRP adapter's generated shape force-included as the SRP builds include it."""
    tree = Tree(trees.ctrl, trees.ctrl, trees.ctrl, stack=trees.stack)
    paths = [*includes(tree), f"-I{trees.ctrl / 'srp'}", f"-I{NVM_DIR / 'plat'}", f"-I{NVM_DIR / 'test/rv32'}",
             f"-I{LWSRP / 'include'}", f"-I{LWSRP}"]
    last = [f"-idirafter{trees.stack / d}" for d in STACK_PRIVATE]
    shape = work / "srp_entity_gen.h"
    work.mkdir(parents=True, exist_ok=True)
    res = run([sys.executable, "-B", str(CTRL / "srp/srp_entity.py"), str(SRP_ENTITY), "-o", str(shape)])
    if res.returncode != 0:
        raise Refusal(f"srp_entity.py refused {SRP_ENTITY.name}: {res.stderr.strip()}")
    return [*compiler, *FIRMWARE_DEFINES, *paths, *last, "-include", str(shape)]


def firmware_side(trees: Trees, compiler: list[str], label: str, universe: dict[str, tuple[str, ...]],
                  work: Path) -> list[str]:
    """Every firmware unit reaches the stack through its public headers only, in every configuration: the
    stack judged, and the checkout's submodule when the stack judged is a copy."""
    argv = firmware_flags(trees, compiler, work)
    stacks = {s.resolve(): (s / STACK_INCLUDE).resolve() for s in (trees.stack, STACK)}
    standins = work / "standins"
    standins.mkdir(parents=True, exist_ok=True)
    units = firmware_units(trees)
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, [*argv, "-x", "c"], universe, work, standins):
        name = unit.relative_to(trees.ctrl).as_posix()
        for s in seen:
            if s.error:
                found.setdefault((label, f"{name} does not preprocess: {s.error}"), []).append(s.label)
                continue
            for dep in sorted(s.deps):
                if any(dep.is_relative_to(stack) and not dep.is_relative_to(public)
                       for stack, public in stacks.items()):
                    found.setdefault((label, f"{name} includes {where(dep, trees)}, not one of the stack's public "
                                             "headers"), []).append(s.label)
    return smallest(found)


def shadows(trees: Trees, firmware: Path) -> list[str]:
    """No file under sw/firmware is named as a source or public header of the stack."""
    names = {p.name for part in STACK_PARTS for p in (trees.stack / part).iterdir() if p.is_file()}
    roots = [trees.ctrl] + [p for p in firmware.iterdir() if p.is_dir() and p.resolve() != CTRL.resolve()]
    return [f"firmware: {p.relative_to(root.parent).as_posix()} has the name of the stack's {p.name}"
            for root in roots for p in sorted(root.rglob("*")) if p.is_file() and p.name in names]


def judge(trees: Trees, rv32: str | None, work: Path, universe: dict[str, tuple[str, ...]] | None = None) -> list[str]:
    """Every finding on both sides of the boundary for these trees, in every configuration."""
    universe = modes() if universe is None else universe
    host = ["gcc", *C_FLAGS]
    findings = stack_side(trees, host, "host", universe, work / "stack")
    firmware = firmware_side(trees, ["gcc", "-std=c11"], "firmware", universe, work / "firmware")
    if rv32 is not None:
        cross = [rv32, *RV32_FLAGS, *fw_rv32.includes(rv32)]
        findings += stack_side(trees, cross, "rv32", universe, work / "stack")
        firmware += firmware_side(trees, cross, "firmware rv32", universe, work / "firmware-rv32")
    findings += tests_side(trees, universe, work / "tests")
    findings += firmware
    findings += shadows(trees, ROOT / "sw/firmware")
    return findings


def stack_gate(selftest: bool, work: Path) -> list[str]:
    """The stack's own boundary gate (and its self-test), from the submodule; its refusal is a finding."""
    for tool in ("cmake", "clang", "gcc", "nm"):
        if shutil.which(tool) is None:
            raise Refusal(f"the stack's gate needs {tool}")
    argv = [sys.executable, "-I", str(STACK_GATE), "--work", str(work), "--jobs", "4"]
    res = run([*argv, "--selftest"] if selftest else argv, cwd=work)
    lines = (res.stdout + res.stderr).strip().splitlines()
    for line in lines:
        print(f"    {line}")
    return [] if res.returncode == 0 else [f"the stack's own gate {STACK_GATE.relative_to(ROOT)} refused: exit "
                                           f"{res.returncode}"]


# ---- the planted controls -------------------------------------------------------------------

@dataclass(frozen=True)
class Plant:
    """One control: written into the stack's copy or the ctrl tree's copy, side by side, so a relative path
    from one reaches the other (a "+" file is written whole as a new file); refused by a finding holding
    `needle`, or passing when `needle` is "". `mode` is a flag planted into a copy of ctrl_arms.py's text,
    which the boundary must then explore without being told."""

    name: str
    side: str
    file: str
    old: str
    new: str
    needle: str
    mode: str = ""


PLANTS = (
    Plant("stack source includes the mailbox HAL", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"mbx_hal.h\"\n",
          "the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("stack source includes the register-map contract", "stack", "src/acmp.c", "#include \"acmp.h\"\n",
          "#include \"acmp.h\"\n#include \"mbx_contract.h\"\n", "includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    Plant("stack source includes the composition", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"ctrl_app.h\"\n", "includes sw/firmware/ctrl/app/ctrl_app.h"),
    Plant("stack source includes the store's port", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"nvm_state.h\"\n", "includes sw/firmware/ctrl_nvm/nvm_state.h"),
    Plant("stack source includes the loop through a macro", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#define TSN_LOOP \"ctrl_loop.h\"\n#include TSN_LOOP\n",
          "includes sw/firmware/ctrl/loop/ctrl_loop.h"),
    Plant("stack public header includes the platform's header", "stack", "include/wire.h", "#include <stdint.h>\n",
          "#include <stdint.h>\n#include \"ctrl_debug.h\"\n", "the stack's include/wire.h includes"),
    Plant("stack source includes a header nobody supplies", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"image_layout.h\"\n", "does not preprocess with the firmware's flags"),
    Plant("stack source includes an OS header", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include <unistd.h>\n", "includes "),
    Plant("firmware reaches a stack example's header", "ctrl", "adp/adp_mbx.c", "#include \"adp_mbx.h\"\n",
          "#include \"adp_mbx.h\"\n#include \"adp_port.h\"\n",
          "adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("firmware header reaches a stack source by a relative path", "ctrl", "maap/maap_mbx.h",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"../../tsn-c-stack/src/maap.c\"\n",
          "includes tsn-c-stack/src/maap.c, not one of the stack's public headers"),
    Plant("image source reaches a stack test's header", "ctrl", "test/rv32_image/image_main.c",
          "#include \"ctrl_app.h\"\n",
          "#include \"ctrl_app.h\"\n#include \"../../../tsn-c-stack/tests/acmp_fake.hpp\"\n",
          "test/rv32_image/image_main.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    Plant("a copy of the stack's wire.h in the firmware", "ctrl", "+mbx/wire.h", "", "#include <stdint.h>\n",
          "mbx/wire.h has the name of the stack's wire.h"),
    Plant("a copy of the stack's adp.c in the firmware", "ctrl", "+adp/adp.c", "", "int adp_copy;\n",
          "adp/adp.c has the name of the stack's adp.c"),
    Plant("stack source includes the mailbox HAL under the re-entry assertion", "stack", "src/acmp.c",
          "#ifdef CTRL_REENTRY_ASSERT\n", "#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_hal.h\"\n",
          "host [-DCTRL_REENTRY_ASSERT]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("stack source includes the platform's header in a debug build", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n", "#ifndef NDEBUG\n#include <assert.h>\n#include \"ctrl_debug.h\"\n",
          "host [-UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/port/ctrl_debug.h"),
    Plant("stack source includes the contract in a debug build with the re-entry assertion", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n",
          "#ifndef NDEBUG\n#include <assert.h>\n#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_contract.h\"\n#endif\n",
          "host [-DCTRL_REENTRY_ASSERT -UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    Plant("firmware adapter reaches a stack test's fake under the re-entry assertion", "ctrl", "acmp/acmp_mbx.c",
          "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n#include \"../../tsn-c-stack/tests/acmp_fake.hpp\"\n"
          "#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    Plant("firmware adapter reaches the stack's test fake by its checkout path under the re-entry assertion",
          "ctrl", "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n"
          "#include \"../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp\"\n#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes third_party/tsn-c-stack/tests/acmp_fake.hpp, "
          "not one of the stack's public headers"),
    Plant("firmware tests a mode by its value", "ctrl", "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#if CTRL_REENTRY_ASSERT\n#include \"../../tsn-c-stack/src/maap.c\"\n#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c"),
    Plant("the SRP image's composition reaches a stack source", "ctrl", "test/ctrl_image.c",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n#include \"../../tsn-c-stack/src/acmp.c\"\n",
          "firmware [-DCTRL_IMAGE_SRP]: test/ctrl_image.c includes tsn-c-stack/src/acmp.c"),
    Plant("a stack test includes the mailbox HAL", "stack", "tests/test_maap_debug.cpp", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"mbx_hal.h\"\n",
          "tests: the stack's tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a stack test includes the firmware's harness", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"fw_gtest.hpp\"\n",
          "tests: the stack's tests/test_adp.cpp includes sw/firmware/gtest/fw_gtest.hpp"),
    Plant("a stack test includes the platform's pool in its release build", "stack", "tests/test_adp_reentry.cpp",
          "#include \"adp.h\"\n", "#include \"adp.h\"\n#ifdef ADP_TEST_RELEASE\n#include \"ctrl_pool.h\"\n#endif\n",
          "tests [-DADP_TEST_RELEASE]: the stack's tests/test_adp_reentry.cpp includes "
          "sw/firmware/ctrl/port/ctrl_pool.h"),
    Plant("a stack public header includes the mailbox HAL for C++ only", "stack", "include/acmp.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"mbx_hal.h\"\nextern \"C\" {\n",
          "tests: the stack's tests/test_acmp.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a mode an arm writes is explored without being named here", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_PLANTED_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          "-DCTRL_PLANTED_MODE"),
    Plant("pass: the firmware includes a public header", "ctrl", "port/ctrl_debug.c", "#include \"ctrl_debug.h\"\n",
          "#include \"ctrl_debug.h\"\n#include \"wire.h\"\n", ""),
    Plant("pass: the stack includes only its own header and the C library", "stack", "src/maap.c",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"wire.h\"\n#include <stdint.h>\n", ""),
    Plant("pass: a stack test reaches the stack's example", "stack", "tests/test_maap_debug.cpp",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"adp_port.h\"\n", ""),
)


def planted(plant: Plant, work: Path) -> Trees:
    """Copies of the trees with one plant written into them."""
    trees = Trees(work / "ctrl", work / "tsn-c-stack")
    for path in trees.ctrl, trees.stack:
        if path.exists():
            shutil.rmtree(path)
    shutil.copytree(CTRL, trees.ctrl, ignore=shutil.ignore_patterns("__pycache__"))
    for part in dict.fromkeys((*STACK_PARTS, *STACK_PRIVATE)):
        shutil.copytree(STACK / part, trees.stack / part)
    root = trees.stack if plant.side == "stack" else trees.ctrl
    if plant.file.startswith("+"):
        target = root / plant.file[1:]
        if target.exists():
            raise Refusal(f"control {plant.name!r}: {plant.file[1:]} exists already")
        target.write_text(plant.new, encoding="utf-8")
        return trees
    target = root / plant.file
    text = target.read_text(encoding="utf-8")
    if text.count(plant.old) != 1:
        raise Refusal(f"control {plant.name!r}: its anchor occurs {text.count(plant.old)} times in {plant.file}")
    target.write_text(text.replace(plant.old, plant.new), encoding="utf-8")
    return trees


def controls(rv32: str | None, work: Path) -> int:
    """Every plant refused by the finding it names, every pass control passing; the misbehaving count."""
    bad = 0
    arms = HERE / "ctrl_arms.py"
    for plant in PLANTS:
        trees = planted(plant, work / "plants")
        written = {arms: f"{arms.read_text(encoding='utf-8')}\nPLANTED = (\"{plant.mode}\",)\n"} if plant.mode else None
        findings = judge(trees, rv32, work / "plants-build", modes(written))
        shutil.rmtree(work / "plants-build", ignore_errors=True)
        ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
        shown = next((f for f in findings if plant.needle and plant.needle in f), findings[0] if findings else "")
        print(f"[{'ok' if ok else 'ESCAPED'}] boundary control {plant.name}: {shown or 'passes'}", flush=True)
        bad += not ok
    shutil.rmtree(work / "plants", ignore_errors=True)
    return bad


def pin_controls(work: Path) -> tuple[int, int]:
    """The shared pin check (ctrl_build.stack_pin) passes a clone of the stack at its gitlink and refuses, by
    name, the clone with a source, a test, a script or a CMake file edited, with an edit hidden from git
    status, with a header the gitlink's tree does not hold, and at another revision; the mailbox bench passes
    the pinned clone, and the bench and the MAAP differential (both modes) refuse an edited one before
    building it. Returns the misbehaving count and the number of controls."""
    pin = stack_gitlink()
    clone = work / "pin-clone"
    edited = f"differs from the pinned {pin[:8]}: "

    def fresh() -> None:
        """A new clone of the stack at its gitlink, for the next control."""
        if clone.exists():
            shutil.rmtree(clone)
        if run(["git", "clone", "--quiet", "--no-hardlinks", str(STACK), str(clone)]).returncode or \
                run(["git", "-C", str(clone), "-c", "advice.detachedHead=false", "checkout", "--quiet",
                     pin]).returncode:
            raise Refusal(f"cannot clone {STACK.relative_to(ROOT)} at {pin} for the pin controls")

    def append(rel: str) -> None:
        """One line added to a file of the clone."""
        (clone / rel).write_text((clone / rel).read_text(encoding="utf-8") + "\n", encoding="utf-8")

    def hidden() -> None:
        """A source edited and hidden from git status by the index's assume-unchanged flag."""
        append("src/adp.c")
        if run(["git", "-C", str(clone), "update-index", "--assume-unchanged", "src/adp.c"]).returncode:
            raise Refusal("cannot hide the pin control's edit from git status")

    def direct() -> tuple[bool, str]:
        """The pin check itself on the clone: accepted, and what it said."""
        try:
            return True, f"accepted {stack_pin(clone, pin)}"
        except Refusal as exc:
            return False, str(exc)

    def tool(argv: list[str], env: dict[str, str] | None = None) -> tuple[bool, str]:
        """A gate run on the clone: accepted (exit 0), and its last line about the stack."""
        res = subprocess.run(argv, capture_output=True, text=True, check=False, env={**os.environ, **(env or {})})
        said = [ln for ln in (res.stdout + res.stderr).splitlines() if "tsn-c-stack" in ln]
        return res.returncode == 0, f"exit {res.returncode}: {said[-1].strip() if said else 'no pin verdict'}"

    def bench(target: str) -> tuple[bool, str]:
        """The mailbox bench's `target` with the clone as its stack, and a compiler that always fails, so a
        bench that skipped the check could build nothing."""
        return tool(["make", "--no-print-directory", "-C", str(TB_MBX), f"STACK_DIR={clone}", "CC=false", target])

    def differential(*extra: str) -> tuple[bool, str]:
        """The MAAP differential on the clone, with a simulator that always fails."""
        return tool([sys.executable, "-B", str(HERE / "maap_differential.py"), "--stack", str(clone), *extra],
                    {"VERILATOR": "false"})

    arms = (("the pinned clone, unmodified", lambda: None, direct, ""),
            ("a core source edited", lambda: append("src/adp.c"), direct, edited + "src/adp.c"),
            ("a core test edited", lambda: append("tests/test_adp.cpp"), direct, edited + "tests/test_adp.cpp"),
            ("a stack script edited", lambda: append("scripts/check_boundary.py"), direct,
             edited + "scripts/check_boundary.py"),
            ("a CMake file edited", lambda: append("CMakeLists.txt"), direct, edited + "CMakeLists.txt"),
            ("an edit hidden from git status (assume-unchanged)", hidden, direct, edited + "src/adp.c"),
            ("a header the pinned tree does not hold", lambda: (clone / "include/stdint.h").write_text(""), direct,
             edited + "include/stdint.h"),
            ("another revision checked out",
             lambda: run(["git", "-C", str(clone), "checkout", "--quiet", "HEAD~1"]), direct, "is not the pinned"),
            ("the mailbox bench, the pinned clone", lambda: None, lambda: bench("stack-pin"), ""),
            ("the mailbox bench, a core source edited", lambda: append("src/maap.c"),
             lambda: bench("obj_fw/libctrlfw.a"), edited + "src/maap.c"),
            ("the MAAP differential, a core source edited", lambda: append("src/maap.c"), differential,
             edited + "src/maap.c"),
            ("the MAAP differential's self-test, a core source edited", lambda: append("src/maap.c"),
             lambda: differential("--self-test"), edited + "src/maap.c"))
    bad = 0
    for what, spoil, check, needle in arms:
        fresh()
        spoil()
        accepted, detail = check()
        ok = accepted if not needle else (not accepted and needle in detail)
        print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}", flush=True)
        bad += not ok
    shutil.rmtree(clone)
    return bad, len(arms)


def main(argv: list[str] | None = None) -> int:
    """Hold both sides, then the stack's own gate; with --selftest, the controls first."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--selftest", action="store_true", help="also plant every control and require its verdict")
    ap.add_argument("--require-rv32", action="store_true", help="refuse, not skip, without an RV32 compiler")
    args = ap.parse_args(argv)
    rv32 = fw_rv32.compiler()
    if rv32 is None and args.require_rv32:
        print("REFUSED: no RV32 compiler (the pinned SDK's riscv32-linux-gcc or MILAN_RV32_CC)")
        return 2
    if rv32 is None:
        print("  SKIPPED: the RV32 arm, no RV32 compiler; --require-rv32 refuses instead")
    universe = modes()
    print("build modes read from the builders: " +
          "; ".join(f"{name} ({' '.join(flags)})" for name, flags in universe.items()))
    try:
        with tempfile.TemporaryDirectory(prefix="ctrl-boundary-") as tmp:
            work = Path(tmp)
            print(f"tsn-c-stack at {stack_pin()}", flush=True)
            bad = pins = 0
            if args.selftest:
                bad = controls(rv32, work)
                misbehaved, pins = pin_controls(work)
                bad += misbehaved
            PREPROCESSED.clear()
            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout", universe)
            runs = sum(PREPROCESSED)
            findings += stack_gate(args.selftest, work)
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    for finding in findings:
        print(f"  [FAIL] {finding}")
    units = len(firmware_units(Trees(CTRL, STACK)))
    print(f"ctrl_boundary: {units} firmware units and the stack's sources, headers and tests, host"
          f"{' and RV32' if rv32 else ''}, in every configuration of {len(universe)} build modes "
          f"({runs} preprocessings); "
          f"{len(findings)} finding(s)"
          f"{f', {len(PLANTS)} boundary and {pins} pin controls, {bad} misbehaved' if args.selftest else ''}")
    print(f"ctrl_boundary: {'FAIL' if findings or bad else 'PASS'}")
    return 1 if findings or bad else 0


if __name__ == "__main__":
    sys.exit(main())
