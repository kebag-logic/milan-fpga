#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_boundary.py - the TSN stack's boundary, held from both sides (#697).

THE STACK'S SIDE. Every source and public header of the tsn-c-stack submodule
(src/*.c, include/*.h) is preprocessed with this firmware's own include path
and flags, as the host arms compile it (ctrl_build.includes, C_FLAGS) and as
the RV32 build does (RV32_FLAGS and the freestanding headers of fw_rv32), and
its dependencies are read from the compiler. Each must be one of the stack's
public headers, a header of the C library the compiler supplies, or the SRP
adapter's generated shape header where a configuration force-includes it, as
the SRP builds do. A dependency anywhere else (the mailbox driver or its HAL,
the generated register-map contract, the MMIO platform, the app, the loop,
the store, an image) is refused by name; one that does not resolve is refused
too. The stack's tests (tests/*.cpp, tests/*.hpp), which the arms compile with
the firmware's test include path (ctrl_build.compile_tests), are preprocessed
as C++ the same way: they may reach anything of the stack and the host's own
libraries (the C++ library, GoogleTest), and nothing of milan-fpga outside
the submodule. The stack's own gate, its scripts/check_boundary.py (the same
rule under its own CMake build with gcc and clang, and its objects' symbols),
runs as well.

THE FIRMWARE'S SIDE. Every firmware source and header under sw/firmware/ctrl
(every directory but host/ and test/, which hold test equipment) and the
measured images' own sources (every C source under test/; the tests are C++)
reach the stack through its public headers only. AECP is the firmware's, not
the stack's: its core and adapters are judged here like the rest. Each unit is
preprocessed on the host and with the RV32 compiler, with every firmware
directory on the include path, a shape's generated headers, and the stack's
other directories searched last, so a header only they hold resolves there;
any other generated header is named, not read; a dependency inside the stack
outside include/ is refused. No file under sw/firmware may be named as one of
the stack's sources or public headers: a copy there would shadow, or stand in
for, the stack's own.

AS ITS BUILDERS COMPILE IT. Each unit is judged in the language and in every
configuration its builders compile it in, and nothing about either is listed
here: both are read from the builders. The builders are found, never listed:
every Python module and Makefile of the checkout, tracked or new, that names
the firmware's tree (sw/firmware/ctrl, or its shared builder ctrl_build), this
gate excepted.
- Language. Every firmware unit is judged as C, as every builder compiles the
  firmware's sources and their headers with them. A firmware unit is judged
  as C++ too, with the arms' test flags and include path (the stack's tests/
  on it), when a C++ source a builder names (a test, a bench) reaches it:
  every #include line is followed as text, in every branch alike, and one
  whose operand a macro computes, which text cannot follow, is refused. A
  name resolves beside its builder, in the firmware's tree, its tests, the
  stack, the protocol processor, the checkout's root, or a directory of the
  checkout the builder names, in the trees judged; one the builder writes
  itself is followed through the builder's literals; one that resolves to no
  file, or that the builder computes, is refused by name (ctrl_configs).
- Build modes: every -D or -U flag written in a builder, as one argument or
  as two (-D NAME, -U NAME). A macro the C implementation reserves (C11 7.1.3,
  a leading underscore and a capital or a second underscore, as the runtime's
  builder sets for Picolibc and compiler-rt) is not a firmware mode.
- Values: a flag a builder computes at run time is a value, not a mode. The
  image's stream counts are taken at every shipped config (configs/*.yaml,
  each a shape the image builders take) from the image builder's own
  ctrl_image.shape_build. A unit that tests any other computed value is
  refused: the boundary has none of its values. A value is an f-string, its
  macro the literal before its "="; any other -D or -U a builder writes that
  is neither a literal nor an f-string refuses the gate by name.
- Shapes: the headers the builders generate for each shipped config, written
  by the builders' own generators (every entity generator, */*_entity.py, and
  the store's headers from ctrl_image.shape_build); and the SRP adapter's
  shape header force-included, as the SRP builds compile every unit, or not,
  as the others do.
- The mailbox contract: the tracked one, and the variant its generator writes
  (gen_mailbox.py --variant-interfaces) for every other interface count it
  admits, counting up from one until it refuses, as the two-interface builds
  compile the firmware.
The compiler reports each macro a unit's preprocessing tests or expands
(-dU). Of those, the ones that can decide which files it reads are the ones
the conditionals and #include lines of the files it read name, and those
their definitions name in turn; a macro only code expands cannot. Starting
with every alternative that defines a macro chosen, so that a test of it is
reported, the gate preprocesses each unit under every combination of the
alternatives of what decides its reads, until no new one appears: a mode, a
value, a shape or a contract none of them names cannot change what it
includes, and a shape or a contract matters only through the macros its
headers define differently (or a generated header whose own directives
differ). A configuration that stops on an #error directive is one
no builder compiles: what it reads is still judged, from the compiler's
dependency list, which it writes in full; only a unit that stops in every
configuration is refused for it. A finding names, beyond the unit's default
build, the smallest configuration that reaches it.

THE PIN (ctrl_pin.py). Every gate that builds the stack first runs the shared
pin check (ctrl_build.stack_pin): the submodule must be at its gitlink, and
every file of its sources, headers, tests, examples, scripts and CMake files
must hash to the gitlink's tree. This gate does too. Every target of a
Makefile builder whose recipe builds against the stack must have the pin check
as a prerequisite, read from make's own dry run.

--selftest first plants defects in copies of the two trees, each of which must
be refused by name, and controls each of which must pass; then the pin
controls (ctrl_pin.pin_controls: the check on edited clones, the gates that
build the stack on an edited clone, and every Makefile target that reaches the
stack run for real on a poisoned one); then the stack gate's own self-test.
--require-rv32 refuses, rather than skips, the RV32 arm when no RV32 compiler
is found.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest

Exit 0 = both sides hold; 1 = a finding or a control that misbehaved; 2 =
refused (no compiler, GoogleTest, cmake or clang, or the stack's gate could
not run).
"""

from __future__ import annotations

import argparse
import itertools
import os
import re
import shlex
import shutil
import sys
import tempfile
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import fw_gtest  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import (C_FLAGS, CTRL, HARNESS, NVM_DIR, ROOT, RV32_FLAGS, STACK, STACK_INCLUDE,  # noqa: E402
                        STACK_PARTS, TB_COMMON, Refusal, Tree, includes, stack_pin)
# modes stays importable from here: a caller judges in the modes a planted builder gives (judge's universe).
from ctrl_configs import (DEFAULT_ENTITY, FLAG, FORCED, Read, Space, cxx_sources, derive, image_dim,  # noqa: E402
                          makefiles, mode_dims, modes, run, spaces, variants)
from ctrl_pin import makefile_findings, pin_controls  # noqa: E402

#: The C library's headers (ISO C11, 7.1.2): what the stack may include beside its own.
C_HEADERS = ("assert complex ctype errno fenv float inttypes iso646 limits locale math stdalign stdarg stdatomic "
             "stdbool stddef stdint stdio stdlib stdnoreturn string tgmath uchar wchar wctype").split()
#: The stack's directories other than its public headers, searched last on the firmware's side.
STACK_PRIVATE = ("src", "tests", "examples")
#: The directories under sw/firmware/ctrl that hold test equipment; every other one is the firmware's.
TEST_EQUIPMENT = ("host", "test")
LWSRP = ROOT / "third_party/lwSRP/src"
#: The stack's own gate, from the submodule.
STACK_GATE = STACK / "scripts/check_boundary.py"
#: A line -dU writes for a macro the preprocessing tested or expanded.
TESTED = re.compile(r"^#(?:define|undef) ([A-Za-z_]\w*)", re.M)
#: The compiler's report of a header it could not find.
MISSING = re.compile(r"fatal error: (.+?): No such file or directory")
#: What an #error directive (or, under -Werror, a #warning) makes the compiler say: a configuration no
#: builder compiles.
STOPS = ("#error", "#warning")
#: An #include line, read as text: its operand in group 1.
INCLUDE = re.compile(r"^\s*#\s*include\s+(.*?)\s*$", re.M)
#: A directive that decides which files a preprocessing reads (a conditional or an #include): what it names in
#: group 1.
DECIDING = re.compile(r"^\s*#\s*(?:if|ifdef|ifndef|elif|elifdef|elifndef|include|include_next)\b(.*)$", re.M)
#: An identifier.
IDENT = re.compile(r"[A-Za-z_]\w*")
#: A definition -dU writes: its macro, then its replacement list.
DEFINED = re.compile(r"^#define ([A-Za-z_]\w*)(?:\([^)]*\))?(.*)$", re.M)
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
    """One unit preprocessed in one configuration: its words beyond the unit's default build, its flags, and what
    it read."""

    label: str
    flags: tuple[str, ...]
    read: Read


# ---- the exploration ------------------------------------------------------------------------


@lru_cache(maxsize=None)
def deciding_names(path: str, stamp: tuple[int, int]) -> frozenset[str]:
    """Every identifier a file's conditionals and #include lines hold, read as text (`stamp`, its modification
    time and size, keeps a file a control rewrote from being read from the cache)."""
    text = Path(path).read_text(encoding="utf-8", errors="replace").replace("\\\n", " ")
    return frozenset(name for m in DECIDING.finditer(text) for name in IDENT.findall(m[1]))


def deciding(out: str, deps: frozenset[Path]) -> frozenset[str]:
    """The macros a preprocessing tested or expanded (-dU's `out`) that can decide which files it reads: those
    the conditionals and #include lines of the files it read name, and those their definitions name in turn. A
    macro only code expands cannot change what is read."""
    names: set[str] = set()
    for dep in deps:
        try:
            stat = dep.stat()
        except OSError:
            continue
        names |= deciding_names(str(dep), (stat.st_mtime_ns, stat.st_size))
    bodies: dict[str, set[str]] = {}
    for m in DEFINED.finditer(out):
        bodies.setdefault(m[1], set()).update(IDENT.findall(m[2]))
    queue = list(names & bodies.keys())
    while queue:
        for name in bodies.get(queue.pop(), ()):
            if name not in names:
                names.add(name)
                queue.append(name)
    return frozenset(TESTED.findall(out)) & names


def preprocess(argv: list[str], unit: Path, work: Path, standins: Path | None) -> Read:
    """The files the compiler reads for `unit` under `argv`, and the macros its preprocessing tests or expands
    (-dU) that can decide which files it reads (deciding), or its error. With `standins`, a header nobody
    supplies by its plain name (a generated one) is named, not read: an empty stand-in of it is written there,
    searched last. A path through ".." or from the root that resolves nowhere is an error, never stood in for."""
    work.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=".d", dir=work)
    os.close(fd)
    dep = Path(name)
    extra = ["-idirafter", str(standins)] if standins else []
    try:
        for _ in range(64):
            res = run([*argv, *extra, "-E", "-dU", "-P", "-MD", "-MF", str(dep), "-MT", "boundary", str(unit)])
            missing = Path(found[1]) if standins and (found := MISSING.search(res.stderr)) else None
            if res.returncode == 0 or missing is None or missing.is_absolute() or ".." in missing.parts or \
                    (standins / missing).exists():
                break
            (standins / missing).parent.mkdir(parents=True, exist_ok=True)
            (standins / missing).write_text("", encoding="utf-8")
        said = [ln.split("error:", 1)[1].strip() for ln in res.stderr.splitlines() if "error:" in ln]
        stopped = res.returncode != 0 and bool(said) and all(s.startswith(STOPS) for s in said)
        if res.returncode != 0 and not stopped:
            return Read(frozenset(), frozenset(), said[0] if said else res.stderr.strip() or f"exit {res.returncode}")
        names = shlex.split(dep.read_text(encoding="utf-8").replace("\\\n", " ").split(":", 1)[1])
        deps = frozenset(Path(n) for n in names)
        return Read(deps, deciding(res.stdout, deps), said[0] if stopped else "", stopped)
    finally:
        dep.unlink(missing_ok=True)


def explore(argv: list[str], unit: Path, space: Space, work: Path, standins: Path | None = None) -> list[Seen]:
    """`unit` preprocessed in its default build, then under every combination of the alternatives of the modes
    and dimensions that decide what it reads, every other one at its seed, until no new one appears."""
    every = {**space.dims, **mode_dims(argv, space.modes)}
    seed = {n: d.seed for n, d in every.items()}
    tested: list[str] = []
    runs: dict[tuple[str, ...], tuple[dict[str, int], Read]] = {}

    def visit(config: dict[str, int]) -> bool:
        """Preprocess in one configuration; True when it showed a dependence not seen before."""
        flags = tuple(f for n, d in every.items() for f in d.alternatives[config[n]][1])
        if flags in runs:
            return False
        read = preprocess([*argv, *flags], unit, work, standins)
        runs[flags] = (config, read)
        new = [n for n, d in every.items() if n not in tested and d.shown(config[n], read)]
        tested.extend(new)
        return bool(new)

    visit({n: 0 for n in every})
    grew = True
    while grew:
        grew = False
        for pick in itertools.product(*(range(len(every[n].alternatives)) for n in tested)):
            grew = visit({**seed, **dict(zip(tested, pick))}) or grew
    seen = []
    for flags, (config, read) in runs.items():
        # a run that failed tested nothing it could report: its label is its whole configuration
        failed = bool(read.error) and not read.stopped
        label = " ".join(w for n, d in every.items() if (n in tested or failed) and (w := d.alternatives[config[n]][0]))
        deps = frozenset(d.resolve() for d in read.deps if d.is_absolute() or d.exists())
        seen.append(Seen(label, flags, Read(deps, read.tested, read.error, read.stopped)))
    return seen


def judged(units: list[Path], argv: list[str], space: Space, work: Path,
           standins: Path | None = None) -> list[tuple[Path, list[Seen]]]:
    """Every unit explored, a few at once."""
    with ThreadPoolExecutor(max_workers=JOBS) as pool:
        result = list(zip(units, pool.map(lambda u: explore(argv, u, space, work / "pp", standins), units)))
    PREPROCESSED.append(sum(len(seen) for _, seen in result))
    return result


def smallest(found: dict[tuple[str, str], list[str]]) -> list[str]:
    """Each finding once, named by the smallest configuration that reaches it."""
    return [f"{side}{f' [{min(labels, key=lambda s: (len(s.split()), s))}]' if labels and all(labels) else ''}: "
            f"{core}" for (side, core), labels in found.items()]


def common(found: dict[tuple[str, str], list[str]], side: str, name: str, seen: list[Seen], space: Space) -> None:
    """The findings every side shares: a unit that stops on an #error in every configuration, and one whose
    reads a value a builder computes decides, which the boundary has none of."""
    if seen and all(s.read.stopped for s in seen):
        found.setdefault((side, f"{name} stops on an #error in every configuration: {seen[0].read.error}"), [])
    for s in seen:
        for macro in sorted(s.read.tested & space.values.keys()):
            found.setdefault((side, f"{name} tests {macro}, a value {space.values[macro]} computes at run time, "
                                    "which the boundary has none of"), []).append(s.label)


# ---- the firmware's tree, as its builders give it -------------------------------------------

def firmware_dirs(ctrl: Path) -> list[Path]:
    """The firmware's directories: every directory under the ctrl tree but the test equipment's."""
    return sorted(d for d in ctrl.iterdir() if d.is_dir() and d.name not in TEST_EQUIPMENT and
                  not d.name.startswith((".", "__")))


def search(trees: Trees, work: Path) -> list[str]:
    """The firmware's include path from the tree judged: ctrl_build's, then every other firmware directory
    a builder adds (aecp/ for the AECP arms, srp/ for the SRP arms)."""
    given = includes(Tree(trees.ctrl, work, work, stack=trees.stack))
    return given + [flag for d in firmware_dirs(trees.ctrl) if (flag := f"-I{d}") not in given]


def tail(trees: Trees) -> list[str]:
    """The rest of the firmware's include path: the store's platform and RV32 headers, lwSRP's, and the stack's
    other directories, searched last."""
    return [f"-I{NVM_DIR / 'plat'}", f"-I{NVM_DIR / 'test/rv32'}", f"-I{LWSRP / 'include'}", f"-I{LWSRP}",
            *(f"-idirafter{trees.stack / d}" for d in STACK_PRIVATE)]


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
    flags = [f for word in label.split() if FLAG.fullmatch(word)
             for f in ((f"-U{FLAG.fullmatch(word)[1]}", word) if word.startswith("-D") else (word,))]
    return tuple(compiler + flags)


def forced_in(seen: Seen) -> frozenset[Path]:
    """The SRP adapter's shape header a configuration force-includes, wherever its shape put it."""
    if (FORCED not in seen.flags) or seen.flags[seen.flags.index(FORCED) - 1] != "-include":
        return frozenset()
    return frozenset(d for d in seen.read.deps if d.name == FORCED and
                     any(d.is_relative_to(gen.resolve()) for gen, _ in variants().shapes.values()))


def stack_side(trees: Trees, compiler: list[str], label: str, space: Space, work: Path) -> list[str]:
    """The stack's sources and public headers, preprocessed under the firmware's flags in every configuration:
    every dependency is the stack's public header, the C library's, or the shape header a configuration
    force-includes."""
    public = (trees.stack / STACK_INCLUDE).resolve()
    units = sorted((trees.stack / "src").glob("*.c")) + sorted((trees.stack / STACK_INCLUDE).glob("*.h"))
    argv = [*compiler, *search(trees, work), "-x", "c"]
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, argv, space, work / label):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault((label, f"the stack's {name} does not preprocess with the firmware's flags: "
                                         f"{s.read.error}"), []).append(s.label)
                continue
            allowed = c_library(library_flags(compiler, s.label)) | forced_in(s) | {unit.resolve()}
            for dep in sorted(s.read.deps - allowed):
                if not dep.is_relative_to(public):
                    found.setdefault((label, f"the stack's {name} includes {where(dep, trees)}"), []).append(s.label)
        common(found, label, f"the stack's {name}", seen, space)
    return smallest(found)


def tests_side(trees: Trees, space: Space, work: Path) -> list[str]:
    """The stack's tests, preprocessed as the arms compile them in every configuration: nothing of milan-fpga
    outside the stack."""
    argv = ["g++", *fw_gtest.CXX_FLAGS, *search(trees, work), f"-I{trees.stack / 'tests'}",
            f"-idirafter{trees.stack / 'examples'}"]
    probe = work / "gtest_probe.cpp"
    work.mkdir(parents=True, exist_ok=True)
    probe.write_text("#include <gtest/gtest.h>\n#include <gmock/gmock.h>\n", encoding="utf-8")
    if preprocess(argv, probe, work, None).error:
        raise Refusal("the stack's tests need GoogleTest's and GoogleMock's headers")
    units = sorted((trees.stack / "tests").glob("*.cpp")) + sorted((trees.stack / "tests").glob("*.hpp"))
    stack = trees.stack.resolve()
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, [*argv, "-x", "c++"], space, work):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault(("tests", f"the stack's {name} does not preprocess with the firmware's test "
                                           f"flags: {s.read.error}"), []).append(s.label)
                continue
            for dep in sorted(s.read.deps):
                if not dep.is_relative_to(stack) and (dep.is_relative_to(trees.ctrl.resolve()) or
                                                      dep.is_relative_to(ROOT.resolve())):
                    found.setdefault(("tests", f"the stack's {name} includes {where(dep, trees)}"),
                                     []).append(s.label)
        common(found, "tests", f"the stack's {name}", seen, space)
    return smallest(found)


def where(path: Path, trees: Trees) -> str:
    """A dependency, named by where it lives."""
    for root, label in ((trees.ctrl, "sw/firmware/ctrl/"), (trees.stack, "tsn-c-stack/"), (ROOT, "")):
        if path.is_relative_to(root.resolve()):
            return label + path.relative_to(root.resolve()).as_posix()
    return str(path)


# ---- the firmware's side ------------------------------------------------------------------

def firmware_units(trees: Trees) -> list[Path]:
    """The firmware's sources and headers, and the measured images' own sources: every C source under test/
    (the tests are C++)."""
    units = [p for d in firmware_dirs(trees.ctrl) for p in sorted(d.glob("*.[ch]"))]
    return units + sorted((trees.ctrl / "test").rglob("*.c"))


def view(trees: Trees) -> Callable[[Path], Path] | None:
    """A file of the checkout as the trees judged hold it: under the ctrl tree or the stack, their copy's."""
    if (trees.ctrl.resolve(), trees.stack.resolve()) == (CTRL.resolve(), STACK.resolve()):
        return None
    moves = ((CTRL.resolve(), trees.ctrl), (STACK.resolve(), trees.stack))
    return lambda path: next((into / path.relative_to(root) for root, into in moves if path.is_relative_to(root)),
                             path)


@lru_cache(maxsize=None)
def operands(text: str) -> tuple[str, ...]:
    """The operand of every #include line of a text."""
    return tuple(INCLUDE.findall(text))


def cxx_units(trees: Trees, work: Path, planted: dict[Path, str] | None = None) -> tuple[list[Path], list[str]]:
    """The firmware units a C++ source a builder names reaches, every #include line followed as text in every
    branch, against every directory a builder searches, in the trees judged; a source a builder writes itself
    followed through the builder's literals; and as findings, an #include whose operand a macro computes,
    which text cannot follow, and every C++ name of a builder that resolves to no file or that it computes."""
    moved = view(trees) or (lambda path: path)
    sources = cxx_sources(planted, view(trees))
    shapes = [gen for gen, _ in variants().shapes.values()]
    dirs = [Path(f[2:]) for f in search(trees, work)] + [trees.stack / d for d in (STACK_INCLUDE, *STACK_PRIVATE)]
    dirs += [NVM_DIR / d for d in ("host", "plat", "host/stubs", "test", "test/rv32")]
    dirs += [LWSRP / "include", LWSRP, HARNESS, moved(HERE), TB_COMMON, *shapes]
    roots = [r.resolve() for r in (ROOT, trees.ctrl, trees.stack, *shapes)]
    queue, read, findings = list(sources.files), set(), list(sources.findings)
    texts = [(None, text) for text in sources.written.values()]
    while queue or texts:
        path, text = texts.pop() if texts else (queue.pop(), None)
        if path in read:
            continue
        if path is not None:
            read.add(path)
            text = path.read_text(encoding="utf-8", errors="replace")
        for operand in operands(text):
            if operand[:1] not in ('"', "<"):
                findings.append(f"firmware c++: {where(path, trees) if path else 'a source a builder writes'} "
                                f"includes {operand}, which text cannot follow")
                continue
            name = operand[1:].split('"' if operand[0] == '"' else ">", 1)[0]
            for base in ([path.parent] if path and operand[0] == '"' else []) + dirs:
                if (base / name).is_file() and \
                        any((hit := moved((base / name).resolve())).is_relative_to(r) for r in roots):
                    queue.append(hit)
    ctrl = trees.ctrl.resolve()
    units = {trees.ctrl / path.relative_to(ctrl): None for path in read
             if path.is_relative_to(ctrl) and len(part := path.relative_to(ctrl).parts) > 1 and
             part[0] not in TEST_EQUIPMENT}
    return sorted(units), findings


def firmware_side(trees: Trees, compiler: list[str], label: str, space: Space, work: Path,
                  units: list[Path] | None = None) -> list[str]:
    """Every firmware unit reaches the stack through its public headers only, in every configuration: the
    stack judged, and the checkout's submodule when the stack judged is a copy. With `units`, those are
    judged as C++, as the arms compile their tests (the stack's tests on the include path)."""
    cxx = units is not None
    argv = [*compiler, *search(trees, work), *([f"-I{trees.stack / 'tests'}"] if cxx else []), *tail(trees),
            "-x", "c++" if cxx else "c"]
    stacks = {s.resolve(): (s / STACK_INCLUDE).resolve() for s in (trees.stack, STACK)}
    standins = work / "standins"
    standins.mkdir(parents=True, exist_ok=True)
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(firmware_units(trees) if units is None else units, argv, space, work, standins):
        name = unit.relative_to(trees.ctrl).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault((label, f"{name} does not preprocess: {s.read.error}"), []).append(s.label)
                continue
            for dep in sorted(s.read.deps):
                if any(dep.is_relative_to(stack) and not dep.is_relative_to(public)
                       for stack, public in stacks.items()):
                    found.setdefault((label, f"{name} includes {where(dep, trees)}, not one of the stack's public "
                                             "headers"), []).append(s.label)
        common(found, label, name, seen, space)
    return smallest(found)


def shadows(trees: Trees, firmware: Path) -> list[str]:
    """No file under sw/firmware is named as a source or public header of the stack."""
    names = {p.name for part in STACK_PARTS for p in (trees.stack / part).iterdir() if p.is_file()}
    roots = [trees.ctrl] + [p for p in firmware.iterdir() if p.is_dir() and p.resolve() != CTRL.resolve()]
    return [f"firmware: {p.relative_to(root.parent).as_posix()} has the name of the stack's {p.name}"
            for root in roots for p in sorted(root.rglob("*")) if p.is_file() and p.name in names]


def judge(trees: Trees, rv32: str | None, work: Path, universe: dict[str, tuple[str, ...]] | None = None,
          computed: dict[str, str] | None = None, control: Plant | None = None) -> list[str]:
    """Every finding on both sides of the boundary for these trees, in every configuration and language, as the
    builders compile them (with a `control`'s builder text replacing or adding one's), or in `universe`'s modes
    and with `computed`'s values where given."""
    planted = builder_plant(control) if control else None
    derived = derive(planted)
    each = spaces(derived[0] if universe is None else universe, derived[1] if computed is None else computed)
    findings = stack_side(trees, ["gcc", *C_FLAGS], "host", each["stack"], work / "stack")
    firmware = firmware_side(trees, ["gcc", "-std=c11"], "firmware", each["firmware"], work / "firmware")
    cxx, unfollowed = cxx_units(trees, work / "firmware-cxx", planted)
    firmware += unfollowed + firmware_side(trees, ["g++", *fw_gtest.CXX_FLAGS], "firmware c++", each["c++"],
                                           work / "firmware-cxx", cxx)
    if rv32 is not None:
        cross = [rv32, *RV32_FLAGS, *fw_rv32.includes(rv32)]
        findings += stack_side(trees, cross, "rv32", each["stack"], work / "stack")
        firmware += firmware_side(trees, cross, "firmware rv32", each["firmware"], work / "firmware-rv32")
    findings += tests_side(trees, each["tests"], work / "tests")
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
    from one reaches the other (a "+" file is written whole as a new file; no file, none), with `extra` edits
    of the same kind in the same copy; refused by a finding (or a refusal) holding `needle`, or passing when
    `needle` is "". `words` are a builder's arguments (flags, or a source's name), planted into a copy of the
    text of `builder` (a file of test/, or one relative to it; a new one when it holds none; a Makefile's
    recipe when it is one), which the boundary must then read without being told; `raw` is text added to that
    copy as it is, and `swap` an (old, new) edit of it."""

    name: str
    side: str
    file: str
    old: str
    new: str
    needle: str
    words: tuple[str, ...] = ()
    builder: str = "ctrl_arms.py"
    raw: str = ""
    swap: tuple[str, str] | tuple[()] = ()
    extra: tuple[tuple[str, str, str], ...] = ()


#: A builder the checkout does not hold: it names the firmware's shared builder, as every builder does.
NEW_BUILDER = '"""A builder of the firmware that nobody lists."""\nfrom ctrl_build import Tree\n'
#: A Makefile builder the checkout does not hold, of the firmware's tree.
NEW_MAKEFILE = "# A builder of sw/firmware/ctrl that nobody lists.\n"


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
          ("-DCTRL_PLANTED_MODE",)),
    Plant("a mode an AECP arm writes is explored without being named here", "stack", "src/acmp.c",
          "#include \"acmp.h\"\n", "#include \"acmp.h\"\n#ifdef AECP_TEST_APP\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DAECP_TEST_APP]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a mode written in a new builder nobody lists is explored", "stack", "src/maap.c",
          "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_PLANTED_BUILDER\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_BUILDER]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          ("-DCTRL_PLANTED_BUILDER",), "planted_arms.py"),
    Plant("stack source includes the AECP core's header", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"aecp.h\"\n", "the stack's src/adp.c includes sw/firmware/ctrl/aecp/aecp.h"),
    Plant("a stack test includes the AECP adapter", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"aecp_mbx.h\"\n",
          "tests: the stack's tests/test_adp.cpp includes sw/firmware/ctrl/aecp/aecp_mbx.h"),
    Plant("the AECP core reaches a stack source", "ctrl", "aecp/aecp.c", "#include \"aecp_internal.h\"\n",
          "#include \"aecp_internal.h\"\n#include \"../../tsn-c-stack/src/acmp.c\"\n",
          "aecp/aecp.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers"),
    Plant("the AECP application bridge reaches a stack example's header", "ctrl", "app/ctrl_app_aecp.c",
          "#include \"ctrl_app_aecp.h\"\n", "#include \"ctrl_app_aecp.h\"\n#include \"adp_port.h\"\n",
          "app/ctrl_app_aecp.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("the AECP image's SRP composition reaches a stack source", "ctrl", "test/ctrl_aecp_image.c",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n#include \"../../tsn-c-stack/src/maap.c\"\n",
          "firmware [-DCTRL_IMAGE_SRP]: test/ctrl_aecp_image.c includes tsn-c-stack/src/maap.c"),
    Plant("a copy of the stack's acmp.h in the AECP directory", "ctrl", "+aecp/acmp.h", "", "#include <stdint.h>\n",
          "aecp/acmp.h has the name of the stack's acmp.h"),
    Plant("the image reaches a stack example's header under a shape's stream count", "ctrl",
          "test/rv32_image/image_main.c", "#include <stdbool.h>\n",
          "#include <stdbool.h>\n#if IMAGE_SINKS > 1u\n#include \"../../../tsn-c-stack/examples/adp_port.h\"\n"
          "#error PROBE-REACHED\n#endif\n",
          "firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes "
          "tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("a firmware header reaches a stack test's fake in C++ only", "ctrl", "acmp/acmp_mbx.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\nextern \"C\" {\n",
          "firmware c++: acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers"),
    Plant("the AECP image reaches a stack source at a shape its generated header gives many maps", "ctrl",
          "test/ctrl_aecp_image.c", "#include \"aecp_entity_gen.h\"\n",
          "#include \"aecp_entity_gen.h\"\n#if AECP_ENTITY_MAPS > 8u\n#include \"../../tsn-c-stack/src/acmp.c\"\n"
          "#endif\n",
          "firmware [shape=endstation_ax7101_8x8]: test/ctrl_aecp_image.c includes tsn-c-stack/src/acmp.c"),
    Plant("an adapter reaches a stack source where the SRP shape header is force-included", "ctrl",
          "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#ifdef CTRL_SRP_SOURCES\n#include \"../../tsn-c-stack/src/maap.c\"\n#endif\n",
          "firmware [-include srp_entity_gen.h]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c"),
    Plant("an adapter reaches a stack source on the two-interface contract", "ctrl", "adp/adp_mbx.c",
          "#include \"adp_mbx.h\"\n",
          "#include \"adp_mbx.h\"\n#if MBX_N_IF > 1u\n#include \"../../tsn-c-stack/src/adp.c\"\n#endif\n",
          "firmware [interfaces=2]: adp/adp_mbx.c includes tsn-c-stack/src/adp.c"),
    Plant("an adapter reaches a stack source where a build leaves lwSRP's profile undefined", "ctrl",
          "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifndef LWSRP_MILAN\n#include \"../../tsn-c-stack/src/acmp.c\"\n#endif\n",
          "firmware: acmp/acmp_mbx.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers"),
    Plant("the AECP core tests a value only its arms compute", "ctrl", "aecp/aecp.c",
          "#include \"aecp_internal.h\"\n", "#include \"aecp_internal.h\"\n#if AECP_TEST_INTERFACES > 1\n#endif\n",
          "aecp/aecp.c tests AECP_TEST_INTERFACES, a value sw/firmware/ctrl/test/aecp_arms.py computes at run time"),
    Plant("a mode an arm writes as two arguments is explored", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          ("-D", "CTRL_SPLIT_MODE")),
    Plant("a mode a new Makefile writes as two words is explored", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_SPLIT_MAKE\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MAKE]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          ("-D", "CTRL_SPLIT_MAKE"), "planted.mk"),
    Plant("a header only the MAAP differential's C++ source reaches includes a stack test's fake in C++ only",
          "ctrl", "+maap/maap_r584.h", "", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n",
          "firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers",
          extra=(("test/test_maap_differential.cpp", "#include \"maap.h\"\n",
                  "#include \"maap.h\"\n#include \"maap_r584.h\"\n"),)),
    Plant("a builder names a C++ source that is no file", "ctrl", "", "", "",
          "firmware c++: sw/firmware/ctrl/test/planted_arms.py names planted_r4.cpp, a C++ source that resolves to "
          "no file", ("planted_r4.cpp",), "planted_arms.py"),
    Plant("a builder computes a C++ source's name", "ctrl", "", "", "",
          "firmware c++: sw/firmware/ctrl/test/planted_arms.py computes the name of a C++ source",
          builder="planted_arms.py", raw='STEM = "planted_r4"\nPLANTED = STEM + ".cpp"\n'),
    Plant("a C++ source a builder writes reaches a header that includes a stack example in C++ only", "ctrl",
          "+adp/adp_r4.h", "", "#ifdef __cplusplus\n#include \"adp_port.h\"\n#endif\n",
          "firmware c++: adp/adp_r4.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public "
          "headers", builder="planted_arms.py",
          raw='from pathlib import Path\nPath("planted_r4.cpp").write_text("#include \\"adp_r4.h\\"\\n")\n'),
    Plant("a name NOT_SOURCES lists is followed once it is a file", "ctrl", "+test/t.cpp", "",
          "#include \"maap_r4.h\"\n",
          "firmware c++: maap/maap_r4.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers", extra=(("+maap/maap_r4.h", "", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n"),)),
    Plant("NOT_SOURCES lists a name its builder no longer holds", "ctrl", "", "", "",
          "firmware c++: NOT_SOURCES lists tests/t.cpp for sw/firmware/gtest/fw_coverage_selftest.py, which no "
          "longer names it", builder="../../gtest/fw_coverage_selftest.py", swap=('"tests/t.cpp", ', "")),
    Plant("a builder joins -D to a macro it computes", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D', a -D or -U flag the boundary cannot read",
          builder="planted_arms.py", raw='MODE = "CTRL_R4_JOINED"\nPLANTED = ["-D" + MODE]\n'),
    Plant("a builder formats a -D flag's macro", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D%s', a -D or -U flag the boundary cannot "
          "read", builder="planted_arms.py", raw='PLANTED = ["-D%s" % "CTRL_R4_FORMAT"]\n'),
    Plant("a builder joins a value to a -D flag", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-DCTRL_R4_VALUE=', a -D or -U flag the "
          "boundary cannot read", builder="planted_arms.py", raw='N = 2\nPLANTED = ["-DCTRL_R4_VALUE=" + str(N)]\n'),
    Plant("a builder's f-string computes a -D flag's macro name", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py computes a -D or -U flag's macro",
          builder="planted_arms.py", raw='SUFFIX = "MODE"\nPLANTED = [f"-DCTRL_R4_{SUFFIX}"]\n'),
    Plant("a builder writes a bare -D alone", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D', a -D or -U flag the boundary cannot read",
          builder="planted_arms.py", raw='NAMES = ["CTRL_R4_BARE"]\nPLANTED = ["cc", "-D"] + NAMES\n'),
    Plant("a Makefile computes a -D flag's macro", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-D$(MODE)', a -D or -U flag the boundary cannot read",
          builder="planted.mk", raw="planted:\n\tcc -D$(MODE) -c planted.c\n"),
    Plant("a Makefile computes a -D flag's value", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-DCTRL_R4_MAKE=$(VALUE)', a -D or -U flag the "
          "boundary cannot read", builder="planted.mk", raw="planted:\n\tcc -DCTRL_R4_MAKE=$(VALUE) -c planted.c\n"),
    Plant("a Makefile prefixes -D to the macros it lists", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-D,$(MODES))', a -D or -U flag the boundary cannot "
          "read", builder="planted.mk", raw="planted:\n\tcc $(addprefix -D,$(MODES)) -c planted.c\n"),
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
    for file, old, new in ((plant.file, plant.old, plant.new), *plant.extra):
        if not file:
            continue
        if file.startswith("+"):
            target = root / file[1:]
            if target.exists():
                raise Refusal(f"control {plant.name!r}: {file[1:]} exists already")
            target.write_text(new, encoding="utf-8")
            continue
        target = root / file
        text = target.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"control {plant.name!r}: its anchor occurs {text.count(old)} times in {file}")
        target.write_text(text.replace(old, new), encoding="utf-8")
    return trees



def builder_plant(plant: Plant) -> dict[Path, str] | None:
    """The builder text a plant is written into: a Python builder's tuple of arguments, or a Makefile recipe's
    words; then its raw text, after its swap."""
    if not (plant.words or plant.raw or plant.swap):
        return None
    builder = (HERE / plant.builder).resolve()
    text = builder.read_text(encoding="utf-8") if builder.exists() else \
        NEW_BUILDER if builder.suffix == ".py" else NEW_MAKEFILE
    if plant.swap:
        old, new = plant.swap
        if text.count(old) != 1:
            raise Refusal(f"control {plant.name!r}: its builder anchor occurs {text.count(old)} times")
        text = text.replace(old, new)
    if plant.words:
        text += f"\nPLANTED = {plant.words!r}\n" if builder.suffix == ".py" else \
            f"\nplanted:\n\tcc {' '.join(plant.words)} -c planted.c\n"
    return {builder: text + plant.raw}


def controls(rv32: str | None, work: Path) -> int:
    """Every plant refused by the finding (or the refusal) it names, every pass control passing; the misbehaving
    count."""
    bad = 0
    for plant in PLANTS:
        trees = planted(plant, work / "plants")
        try:
            findings = judge(trees, rv32, work / "plants-build", control=plant)
        except Refusal as exc:
            findings = [f"REFUSED: {exc}"]
        shutil.rmtree(work / "plants-build", ignore_errors=True)
        ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
        shown = next((f for f in findings if plant.needle and plant.needle in f), findings[0] if findings else "")
        print(f"[{'ok' if ok else 'ESCAPED'}] boundary control {plant.name}: {shown or 'passes'}", flush=True)
        bad += not ok
    shutil.rmtree(work / "plants", ignore_errors=True)
    return bad


def configurations(universe: dict[str, tuple[str, ...]], computed: dict[str, str]) -> None:
    """What the configurations are drawn from, as read from the builders."""
    found = variants()
    image = image_dim()
    print("build modes read from the builders: " +
          "; ".join(f"{name} ({' '.join(flags)})" for name, flags in universe.items()))
    print(f"shapes, the shipped configs: {', '.join(found.shapes)} (default {DEFAULT_ENTITY.stem}); the image's "
          f"stream counts (ctrl_image.shape_build): {'; '.join(w for w, _ in image.alternatives[1:])}; mailbox "
          f"contracts: the tracked one and {', '.join(f'{n} interfaces' for n in found.contracts) or 'no variant'}")
    print("values the builders compute, which no judged unit may test: " +
          "; ".join(f"{name} ({where})" for name, where in computed.items() if name not in image.macros))
    sources = cxx_sources()
    print(f"C++ sources the builders name: {len(sources.files)} files; written by a builder: "
          f"{', '.join(sources.written) or 'none'}; named, but no source (NOT_SOURCES): "
          f"{'; '.join(sources.data) or 'none'}")


def main(argv: list[str] | None = None) -> int:
    """Hold both sides, every Makefile builder's pin prerequisites, then the stack's own gate; with --selftest,
    the controls first."""
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
    try:
        universe, computed = derive()
        configurations(universe, computed)
        with tempfile.TemporaryDirectory(prefix="ctrl-boundary-") as tmp:
            work = Path(tmp)
            print(f"tsn-c-stack at {stack_pin()}", flush=True)
            bad = pins = 0
            if args.selftest:
                bad = controls(rv32, work)
                misbehaved, pins = pin_controls(work, makefiles())
                bad += misbehaved
            PREPROCESSED.clear()
            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout")
            runs = sum(PREPROCESSED)
            cxx = len(cxx_units(Trees(CTRL, STACK), work / "count")[0])
            findings += makefile_findings(makefiles(), work / "makefiles")
            findings += stack_gate(args.selftest, work)
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    for finding in findings:
        print(f"  [FAIL] {finding}")
    found = variants()
    print(f"ctrl_boundary: {len(firmware_units(Trees(CTRL, STACK)))} firmware units ({cxx} also as C++) and the "
          f"stack's sources, headers and tests, host{' and RV32' if rv32 else ''}, in every configuration of "
          f"{len(universe)} build modes, {len(found.shapes)} shapes and {1 + len(found.contracts)} mailbox "
          f"contracts ({runs} preprocessings), and every Makefile builder's pin prerequisites; "
          f"{len(findings)} finding(s)"
          f"{f', {len(PLANTS)} boundary and {pins} pin controls, {bad} misbehaved' if args.selftest else ''}")
    print(f"ctrl_boundary: {'FAIL' if findings or bad else 'PASS'}")
    return 1 if findings or bad else 0


if __name__ == "__main__":
    sys.exit(main())
