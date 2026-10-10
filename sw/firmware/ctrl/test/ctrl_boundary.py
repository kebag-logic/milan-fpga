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
here or read from a builder's text: both are taken from the builders' compiler
invocations as they ran (ctrl_capture.py: every C and C++ compiler, the RV32
one, the Verilator builds' and the stack's CMake build's, through a recording
wrapper on PATH that runs the real compiler unchanged). The capture is given
(--capture, as the hosted firmware-unit job makes it around its firmware
steps), or, without one, made here by running every known builder
(ctrl_configs.BUILDERS) under it. Either way the stack's own gate and the
image builders run under it here (ctrl_runs.py). A missing or empty capture,
a known builder it holds no invocation of, a builder found by text that
compiled nothing in it and is listed nowhere, and a compiler a builder runs by
a path no wrapper stands on (one a Python builder starts, which the capture's
audit hook sees, or one a Makefile builder's recipe names, read from make's
own dry run under the capture's PATH) all refuse the gate by name; --without
verilator leaves out the builders that need Verilator, each named on the run.
- Language. Every firmware unit is judged as C, as every builder compiles the
  firmware's sources and their headers with them. A firmware unit is judged
  as C++ too, with the arms' test flags and include path (the stack's tests/
  on it), when a recorded C++ invocation reaches it: its source (the trees'
  file, or the text the capture kept of one the builder wrote) and every file
  it read first, every #include line followed as text in every branch alike,
  against the directories that invocation searched and every directory a
  builder searches, in the trees judged, and through the headers outside the
  checkout the capture kept beside it; one whose operand a macro computes,
  which text cannot follow, is refused.
- Build modes: every -D and -U flag of every recorded invocation, exactly as
  the compiler was given it, with each value the builds gave it. A macro the
  C implementation reserves (C11 7.1.3, a leading underscore and a capital or
  a second underscore, as the runtime's builder sets for Picolibc and
  compiler-rt) is not a firmware mode. The image's stream counts are taken at
  every shipped config (configs/*.yaml, each a shape the image builders take)
  from the image builder's own ctrl_image.shape_build; a recorded one that no
  shipped shape gives refuses the gate.
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

EACH PREPROCESSING ONCE (Memo). What a preprocessing reads is a function of
its arguments and of the files it reads, so the gate runs each one once per
run and reuses it where it would read the same: the same unit and the same
arguments, every file it read byte-identical (by digest), and every file the
trees gained or lost since named in none of those files and none of its
arguments, none of which computes an #include's operand (a header is looked
up by its name). A preprocessing that failed for any other reason than an
#error directive is never reused: what it read is not known. A unit's
configurations are preprocessed JOBS at a time, every side at once.

THE PIN (ctrl_pin.py). Every gate that builds the stack first runs the shared
pin check (ctrl_build.stack_pin): the submodule must be at its gitlink, and
every file of its sources, headers, tests, examples, scripts and CMake files
must hash to the gitlink's tree. This gate does too. Every target of a
Makefile builder whose recipe builds against the stack must have the pin check
as a prerequisite, read from make's own dry run.

--selftest first judges unplanted copies of the two trees, the base every
control shares, which must pass; then plants defects in the copies, each of
which must be refused by name (a control stops at the finding it names), and
controls each of which must pass; a control's planted builder runs through
the capture, and what it compiled joins the run's capture for that control
alone (ctrl_plants.py). Then the pin controls (ctrl_pin.pin_controls: the
check on edited clones, the gates that build the stack on an edited clone,
and every Makefile target that reaches the stack run for real on a poisoned
one). --require-rv32 refuses, rather than skips, the RV32 arm when no RV32
compiler is found.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture DIR --without verilator

Exit 0 = both sides hold; 1 = a finding or a control that misbehaved; 2 =
refused (no compiler, GoogleTest, cmake or clang, the stack's gate could not
run, or the capture is missing, empty or incomplete).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import os
import re
import shlex
import shutil
import stat
import sys
import tempfile
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import ctrl_capture  # noqa: E402
import fw_gtest  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import (C_FLAGS, CTRL, HARNESS, NVM_DIR, ROOT, RV32_FLAGS, STACK, STACK_INCLUDE,  # noqa: E402
                        STACK_PARTS, TB_COMMON, Refusal, Tree, includes, stack_pin)
from ctrl_capture import Capture, CaptureError  # noqa: E402
from ctrl_configs import (FLAG, FORCED, NEEDS, Read, Space, configurations, cxx_index, derive, held,  # noqa: E402
                          makefiles, mode_dims, run, spaces, variants)
from ctrl_pin import makefile_findings, named_compilers, pin_controls  # noqa: E402
from ctrl_plants import BASE, PLANTS, Plant  # noqa: E402
from ctrl_runs import captures, owned  # noqa: E402

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
#: Preprocessings run at once.
JOBS = 4
#: Units explored at once, each waiting on its preprocessings.
EXPLORERS = 32
#: How many configurations each judgement preprocessed a unit in, one entry per side judged.
PREPROCESSED: list[int] = []
#: A line splice, which the preprocessor joins before it reads anything else (??/ is a backslash where
#: trigraphs are on, as -std=c11 has them).
SPLICE = re.compile(r"(?:\\|\?\?/)[ \t]*\n")
#: An #include (or #include_next, #import, __has_include) whose operand a macro computes, in any spelling of #,
#: comments where blanks may be.
BLANK = r"(?:[ \t]|/\*.*?\*/)*"
COMPUTED_INCLUDE = re.compile(rf"(?:^{BLANK}(?:#|%:|\?\?=){BLANK}(?:include_next|include|import)(?!\w)|"
                              rf"__has_include(?:_next)?{BLANK}\(){BLANK}(?![\"<\s])", re.M | re.S)
#: A word a file's name can be.
WORD = re.compile(r"[\w.+-]+")


class Stopped(Exception):
    """A control's judgement found the finding it names: the rest of it need not run."""


@dataclass(frozen=True)
class Trees:
    """The ctrl tree and the stack being judged: the checkout's, or planted copies; and the judgement of them,
    which reuses the run's preprocessings."""

    ctrl: Path
    stack: Path
    memo: Judgement | None = field(default=None, compare=False)


@dataclass(frozen=True)
class Seen:
    """One unit preprocessed in one configuration: its words beyond the unit's default build, its flags, and what
    it read."""

    label: str
    flags: tuple[str, ...]
    read: Read


# ---- each preprocessing once ----------------------------------------------------------------


@dataclass(frozen=True)
class Facts:
    """What a file's text holds, its splices joined: every word a file's name can be, whether an #include of it
    computes its operand, and every identifier its conditionals and #include lines hold (those that can decide
    what else is read)."""

    words: frozenset[str]
    computes: bool
    directives: frozenset[str]


@dataclass(frozen=True)
class Entry:
    """One preprocessing: what it read, the digest of each file it read (its stand-ins aside), and the listing
    of the trees it ran in."""

    read: Read
    digests: tuple[tuple[str, str], ...]
    listing: frozenset[str]


class Judgement:
    """One judgement's view of the files: each file's digest, taken once, and the listing of the trees judged;
    what it preprocessed and reused; and `stop`, set once a control's finding is found."""

    def __init__(self, memo: Memo, listing: frozenset[str]) -> None:
        self.memo, self.listing = memo, listing
        self.digests: dict[str, str | None] = {}
        self.counts = {"ran": 0, "reused": 0}
        self.lock = threading.Lock()
        self.stop = threading.Event()

    def digest(self, path: str) -> str | None:
        """A file's digest, or None when there is no such file."""
        if path not in self.digests:
            try:
                self.digests[path] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            except OSError:
                self.digests[path] = None
        return self.digests[path]

    def facts(self, path: str, digest: str) -> Facts:
        """What a file holds, read once per content."""
        found = self.memo.facts.get(digest)
        if found is None:
            text = SPLICE.sub("", Path(path).read_bytes().decode("utf-8", "replace"))
            found = self.memo.facts[digest] = Facts(
                frozenset(WORD.findall(text)), bool(COMPUTED_INCLUDE.search(text)),
                frozenset(name for m in DECIDING.finditer(text) for name in IDENT.findall(m[1])))
        return found

    def count(self, what: str) -> None:
        """One more preprocessing run or reused."""
        with self.lock:
            self.counts[what] += 1

    def lookup(self, argv: list[str], unit: Path) -> Read | None:
        """A preprocessing of the run that reads what this one would (see Memo), or None."""
        for entry in self.memo.candidates(str(unit), tuple(argv)):
            if all(self.digest(path) == digest for path, digest in entry.digests) and self.unmoved(entry, argv):
                self.count("reused")
                return entry.read
        return None

    def unmoved(self, entry: Entry, argv: list[str]) -> bool:
        """Whether no file the trees gained or lost since the entry ran could be one it looks up: its name is in
        none of the files it read and none of its arguments, none of which computes an #include's operand."""
        if entry.listing is self.listing:
            return True
        names = {name.rpartition("/")[2] for name in entry.listing ^ self.listing}
        if not all(WORD.fullmatch(n) for n in names) or names & {w for a in argv for w in WORD.findall(a)}:
            return False
        return not any((f := self.facts(path, digest)).computes or names & f.words for path, digest in entry.digests)

    def store(self, argv: list[str], unit: Path, read: Read, standins: Path | None) -> None:
        """A preprocessing, for the run to reuse: never one that failed but on an #error directive."""
        if read.error and not read.stopped:
            return
        digests = []
        for dep in read.deps:
            if standins is not None and within(dep, resolved(str(standins))):
                continue
            if (digest := self.digest(str(dep))) is None:
                return
            digests.append((sys.intern(str(dep)), digest))
        self.memo.add(str(unit), tuple(argv), Entry(read, tuple(digests), self.listing))


class Memo:
    """Every preprocessing of the run (see EACH PREPROCESSING ONCE), by unit and arguments."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.entries: dict[tuple[str, tuple[str, ...]], list[Entry]] = {}
        self.facts: dict[str, Facts] = {}
        self.listings: dict[frozenset[str], frozenset[str]] = {}
        self.made: list[Judgement] = []

    def judgement(self, trees: Trees | None) -> Judgement:
        """A judgement of these trees, their files listed now (of no trees, for a preprocessing on its own)."""
        listing = frozenset(f"{side}/{path.relative_to(root).as_posix()}"
                            for side, root in (() if trees is None else (("ctrl", trees.ctrl), ("stack", trees.stack)))
                            for path in root.rglob("*") if path.is_file())
        with self.lock:
            self.made.append(Judgement(self, self.listings.setdefault(listing, listing)))
            return self.made[-1]

    def total(self, what: str) -> int:
        """How many preprocessings every judgement so far ran, or reused."""
        return sum(made.counts[what] for made in self.made)

    def candidates(self, unit: str, argv: tuple[str, ...]) -> list[Entry]:
        """The preprocessings of a unit with these arguments."""
        with self.lock:
            return list(self.entries.get((unit, argv), ()))

    def add(self, unit: str, argv: tuple[str, ...], entry: Entry) -> None:
        """One more preprocessing."""
        with self.lock:
            self.entries.setdefault((unit, argv), []).append(entry)


#: The run's preprocessings.
MEMO = Memo()


# ---- the exploration ------------------------------------------------------------------------


@lru_cache(maxsize=None)
def resolved(name: str) -> Path:
    """A path a compiler named, resolved once per run (the run makes no link)."""
    return Path(name).resolve()


def within(path: Path, root: Path) -> bool:
    """Whether a resolved path is under a resolved root (Path.is_relative_to, as a prefix of its text)."""
    text, top = str(path), str(root)
    return text == top or text.startswith(top.rstrip("/") + "/")


def deciding(out: str, deps: frozenset[Path], memo: Judgement) -> frozenset[str]:
    """The macros a preprocessing tested or expanded (-dU's `out`) that can decide which files it reads: those
    the conditionals and #include lines of the files it read name (read once per content), and those their
    definitions name in turn. A macro only code expands cannot change what is read."""
    names: set[str] = set()
    for dep in deps:
        if (digest := memo.digest(str(dep))) is not None:
            names |= memo.facts(str(dep), digest).directives
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


def preprocess(argv: list[str], unit: Path, work: Path, standins: Path | None,
               memo: Judgement | None = None) -> Read:
    """The files the compiler reads for `unit` under `argv`, and the macros its preprocessing tests or expands
    (-dU) that can decide which files it reads (deciding), or its error; one of the run's, where `memo` holds
    one that reads the same. With `standins`, a header nobody supplies by its plain name (a generated one) is
    named, not read: an empty stand-in of it is written in a directory of this preprocessing's own there,
    searched last. A path through ".." or from the root that resolves nowhere is an error, never stood in for."""
    if memo is not None:
        if memo.stop.is_set():
            raise Stopped
        if (read := memo.lookup(argv, unit)) is not None:
            return read
        memo.count("ran")
    work.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=".d", dir=work)
    os.close(fd)
    dep = Path(name)
    own = Path(tempfile.mkdtemp(prefix="standins-", dir=standins)) if standins else None
    extra = ["-idirafter", str(own)] if own else []
    try:
        for _ in range(64):
            res = run([*argv, *extra, "-E", "-dU", "-P", "-MD", "-MF", str(dep), "-MT", "boundary", str(unit)])
            missing = Path(found[1]) if own and (found := MISSING.search(res.stderr)) else None
            if res.returncode == 0 or missing is None or missing.is_absolute() or ".." in missing.parts or \
                    (own / missing).exists():
                break
            (own / missing).parent.mkdir(parents=True, exist_ok=True)
            (own / missing).write_text("", encoding="utf-8")
        said = [ln.split("error:", 1)[1].strip() for ln in res.stderr.splitlines() if "error:" in ln]
        stopped = res.returncode != 0 and bool(said) and all(s.startswith(STOPS) for s in said)
        if res.returncode != 0 and not stopped:
            return Read(frozenset(), frozenset(), said[0] if said else res.stderr.strip() or f"exit {res.returncode}")
        names = shlex.split(dep.read_text(encoding="utf-8").replace("\\\n", " ").split(":", 1)[1])
        deps = frozenset(resolved(n) for n in names if Path(n).is_absolute() or Path(n).exists())
        read = Read(deps, deciding(res.stdout, deps, memo or Memo().judgement(None)), said[0] if stopped else "",
                    stopped)
        if memo is not None:
            memo.store(argv, unit, read, own)
        return read
    finally:
        dep.unlink(missing_ok=True)
        if own:
            shutil.rmtree(own, ignore_errors=True)


def explore(argv: list[str], unit: Path, space: Space, work: Path, standins: Path | None = None,
            memo: Judgement | None = None) -> list[Seen]:
    """`unit` preprocessed in its default build, then under every combination of the alternatives of the modes
    and dimensions that decide what it reads, every other one at its seed, until no new one appears."""
    every = {**space.dims, **mode_dims(argv, space.modes)}
    seed = {n: d.seed for n, d in every.items()}
    tested: list[str] = []
    runs: dict[tuple[str, ...], tuple[dict[str, int], Read]] = {}

    def visit(configs: list[dict[str, int]]) -> bool:
        """Preprocess in every configuration not run yet, at once (one the run holds is reused at once, the rest
        go to the shared workers); True when one showed a dependence not seen before."""
        if memo is not None and memo.stop.is_set():
            raise Stopped
        fresh: dict[tuple[str, ...], dict[str, int]] = {}
        for config in configs:
            flags = tuple(f for n, d in every.items() for f in d.alternatives[config[n]][1])
            if flags not in runs:
                fresh.setdefault(flags, config)
        reads = {flags: (memo.lookup([*argv, *flags], unit) if memo is not None else None) for flags in fresh}
        pending = {flags: pool().submit(preprocess, [*argv, *flags], unit, work, standins, memo)
                   for flags, read in reads.items() if read is None}
        wait(pending.values())
        grew = False
        for flags, config in fresh.items():
            read = reads[flags] or pending[flags].result()
            runs[flags] = (config, read)
            new = [n for n, d in every.items() if n not in tested and d.shown(config[n], read)]
            tested.extend(new)
            grew = grew or bool(new)
        return grew

    visit([{n: 0 for n in every}])
    while visit([{**seed, **dict(zip(tested, pick))}
                 for pick in itertools.product(*(range(len(every[n].alternatives)) for n in tested))]):
        pass
    seen = []
    for flags, (config, read) in runs.items():
        # a run that failed tested nothing it could report: its label is its whole configuration
        failed = bool(read.error) and not read.stopped
        label = " ".join(w for n, d in every.items() if (n in tested or failed) and (w := d.alternatives[config[n]][0]))
        seen.append(Seen(label, flags, read))
    return seen


@lru_cache(maxsize=None)
def pool() -> ThreadPoolExecutor:
    """The run's preprocessing workers, which every unit explored shares: JOBS compilers at once."""
    return ThreadPoolExecutor(max_workers=JOBS, thread_name_prefix="ctrl-boundary-cc")


@lru_cache(maxsize=None)
def explorers() -> ThreadPoolExecutor:
    """The run's explorations, each waiting on its preprocessings (never the other way round)."""
    return ThreadPoolExecutor(max_workers=EXPLORERS, thread_name_prefix="ctrl-boundary-unit")


def judged(units: list[Path], argv: list[str], space: Space, work: Path, standins: Path | None = None,
           memo: Judgement | None = None) -> list[tuple[Path, list[Seen]]]:
    """Every unit explored, a few at once."""
    futures = [explorers().submit(explore, argv, unit, space, work / "pp", standins, memo) for unit in units]
    wait(futures)
    result = list(zip(units, (future.result() for future in futures)))
    PREPROCESSED.append(sum(len(seen) for _, seen in result))
    return result


def smallest(found: dict[tuple[str, str], list[str]]) -> list[str]:
    """Each finding once, named by the smallest configuration that reaches it."""
    return [f"{side}{f' [{min(labels, key=lambda s: (len(s.split()), s))}]' if labels and all(labels) else ''}: "
            f"{core}" for (side, core), labels in found.items()]


def common(found: dict[tuple[str, str], list[str]], side: str, name: str, seen: list[Seen]) -> None:
    """The finding every side shares: a unit that stops on an #error in every configuration."""
    if seen and all(s.read.stopped for s in seen):
        found.setdefault((side, f"{name} stops on an #error in every configuration: {seen[0].read.error}"), [])


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
    for unit, seen in judged(units, argv, space, work / label, None, trees.memo):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault((label, f"the stack's {name} does not preprocess with the firmware's flags: "
                                         f"{s.read.error}"), []).append(s.label)
                continue
            allowed = c_library(library_flags(compiler, s.label)) | forced_in(s) | {resolved(str(unit))}
            for dep in sorted(s.read.deps - allowed):
                if not within(dep, public):
                    found.setdefault((label, f"the stack's {name} includes {where(dep, trees)}"), []).append(s.label)
        common(found, label, f"the stack's {name}", seen)
    return smallest(found)


def tests_side(trees: Trees, space: Space, work: Path) -> list[str]:
    """The stack's tests, preprocessed as the arms compile them in every configuration: nothing of milan-fpga
    outside the stack."""
    argv = ["g++", *fw_gtest.CXX_FLAGS, *search(trees, work), f"-I{trees.stack / 'tests'}",
            f"-idirafter{trees.stack / 'examples'}"]
    probe = work / "gtest_probe.cpp"
    work.mkdir(parents=True, exist_ok=True)
    probe.write_text("#include <gtest/gtest.h>\n#include <gmock/gmock.h>\n", encoding="utf-8")
    if preprocess(argv, probe, work, None, trees.memo).error:
        raise Refusal("the stack's tests need GoogleTest's and GoogleMock's headers")
    units = sorted((trees.stack / "tests").glob("*.cpp")) + sorted((trees.stack / "tests").glob("*.hpp"))
    stack, ctrl, root = trees.stack.resolve(), trees.ctrl.resolve(), ROOT.resolve()
    found: dict[tuple[str, str], list[str]] = {}
    for unit, seen in judged(units, [*argv, "-x", "c++"], space, work, None, trees.memo):
        name = unit.relative_to(trees.stack).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault(("tests", f"the stack's {name} does not preprocess with the firmware's test "
                                           f"flags: {s.read.error}"), []).append(s.label)
                continue
            for dep in sorted(s.read.deps):
                if not within(dep, stack) and (within(dep, ctrl) or within(dep, root)):
                    found.setdefault(("tests", f"the stack's {name} includes {where(dep, trees)}"),
                                     []).append(s.label)
        common(found, "tests", f"the stack's {name}", seen)
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


def cxx_units(trees: Trees, work: Path, capture: Capture) -> tuple[list[Path], list[str]]:
    """The firmware units a recorded C++ invocation reaches (ctrl_configs.cxx_sources): its source, the trees'
    file where it is one and else the text the capture kept, and every file it read first; every #include line
    followed as text in every branch, against the including file's directory, every directory a recorded C++
    invocation searched that is one, and every directory a builder searches, in the trees judged; and through
    the headers outside the checkout the capture kept, by the name they were reached at. As findings, an
    #include whose operand a macro computes, which text cannot follow."""
    moved = view(trees) or (lambda path: path)
    index = cxx_index(capture)
    shapes = [gen for gen, _ in variants().shapes.values()]
    dirs = [Path(f[2:]) for f in search(trees, work)] + [trees.stack / d for d in (STACK_INCLUDE, *STACK_PRIVATE)]
    dirs += [NVM_DIR / d for d in ("host", "plat", "host/stubs", "test", "test/rv32")]
    dirs += [LWSRP / "include", LWSRP, HARNESS, moved(HERE), TB_COMMON, *shapes]
    searched = list(dict.fromkeys(str(d) for d in [*dirs, *map(moved, index.present)]))
    roots = [r.resolve() for r in (ROOT, trees.ctrl, trees.stack, *shapes)]
    kept, reached = index.kept, index.reached
    queue = [(moved(source.path), source.digest) for source in index.sources]
    read: set[Path] = set()
    findings: list[str] = []
    looked: dict[str, Path | None] = {}

    def hit(candidate: str) -> Path | None:
        """A file a name reaches in a directory, in the trees judged and inside the roots; looked up once."""
        if candidate not in looked:
            try:
                regular = stat.S_ISREG(os.stat(candidate).st_mode)
            except OSError:
                regular = False
            found = moved(Path(candidate).resolve()) if regular else None
            looked[candidate] = found if found is not None and any(found.is_relative_to(r) for r in roots) else None
        return looked[candidate]

    while queue:
        path, digest = queue.pop()
        if path in read:
            continue
        read.add(path)
        if (not digest or any(within(resolved(str(path)), r) for r in roots[:3])) and path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
        elif digest:
            text = capture.text(digest)
        else:
            continue
        for operand in operands(text):
            if operand[:1] not in ('"', "<"):
                findings.append(f"firmware c++: {where(path, trees)} includes {operand}, which text cannot follow")
                continue
            name = operand[1:].split('"' if operand[0] == '"' else ">", 1)[0]
            queue += [(found, "") for base in ([str(path.parent)] if operand[0] == '"' else []) + searched
                      if (found := hit(f"{base}/{name}")) is not None]
            beside = [(path.parent / name).resolve()] if operand[0] == '"' else []
            queue += [(held_at, kept[held_at]) for held_at in (*beside, *reached.get(name, ())) if held_at in kept]
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
    for unit, seen in judged(firmware_units(trees) if units is None else units, argv, space, work, standins,
                             trees.memo):
        name = unit.relative_to(trees.ctrl).as_posix()
        for s in seen:
            if s.read.error and not s.read.stopped:
                found.setdefault((label, f"{name} does not preprocess: {s.read.error}"), []).append(s.label)
                continue
            for dep in sorted(s.read.deps):
                if any(within(dep, stack) and not within(dep, public) for stack, public in stacks.items()):
                    found.setdefault((label, f"{name} includes {where(dep, trees)}, not one of the stack's public "
                                             "headers"), []).append(s.label)
        common(found, label, name, seen)
    return smallest(found)


def shadows(trees: Trees, firmware: Path) -> list[str]:
    """No file under sw/firmware is named as a source or public header of the stack."""
    names = {p.name for part in STACK_PARTS for p in (trees.stack / part).iterdir() if p.is_file()}
    roots = [trees.ctrl] + [p for p in firmware.iterdir() if p.is_dir() and p.resolve() != CTRL.resolve()]
    return [f"firmware: {p.relative_to(root.parent).as_posix()} has the name of the stack's {p.name}"
            for root in roots for p in sorted(root.rglob("*")) if p.is_file() and p.name in names]


def judge(trees: Trees, rv32: str | None, work: Path, capture: Capture, control: Plant | None = None,
          without: frozenset[str] = frozenset()) -> list[str]:
    """Every finding on both sides of the boundary for these trees, in every configuration and language the
    capture's invocations compile them in; each side judged at once, reusing the run's preprocessings. The
    capture must hold every known builder's invocations but those `without` leaves out (ctrl_configs.held,
    with a `control`'s builder texts added to the checkout's). A control that must be refused is judged until
    the finding it names is found."""
    texts, needle = ({HERE / name: text for name, text in control.texts}, control.needle) if control else (None, "")
    held(capture, without, texts)
    each = spaces(derive(capture))
    trees = replace(trees, memo=MEMO.judgement(trees))
    names = shadows(trees, ROOT / "sw/firmware")
    cxx, unfollowed = cxx_units(trees, work / "firmware-cxx", capture)
    if needle and any(needle in f for f in names + unfollowed):
        return unfollowed + names
    cross = [rv32, *RV32_FLAGS, *fw_rv32.includes(rv32)] if rv32 is not None else None
    sides: list[Callable[[], list[str]]] = [
        lambda: stack_side(trees, ["gcc", *C_FLAGS], "host", each["stack"], work / "stack"),
        lambda: stack_side(trees, cross, "rv32", each["stack"], work / "stack") if cross else [],
        lambda: tests_side(trees, each["tests"], work / "tests"),
        lambda: firmware_side(trees, ["gcc", "-std=c11"], "firmware", each["firmware"], work / "firmware"),
        lambda: unfollowed,
        lambda: firmware_side(trees, ["g++", *fw_gtest.CXX_FLAGS], "firmware c++", each["c++"],
                              work / "firmware-cxx", cxx),
        lambda: firmware_side(trees, cross, "firmware rv32", each["firmware"], work / "firmware-rv32")
        if cross else [],
        lambda: names]
    found: dict[int, list[str]] = {}
    with ThreadPoolExecutor(max_workers=len(sides), thread_name_prefix="ctrl-boundary-side") as runner:
        futures = {runner.submit(side): at for at, side in enumerate(sides)}
        for future in as_completed(futures):
            try:
                found[futures[future]] = future.result()
            except Stopped:
                continue
            except BaseException:
                trees.memo.stop.set()
                raise
            if needle and any(needle in f for f in found[futures[future]]):
                trees.memo.stop.set()
    return [f for at in sorted(found) for f in found[at]]


def stack_gate(selftest: bool, work: Path, capture: Path | None) -> tuple[list[str], list[str]]:
    """The stack's own boundary gate (and its self-test), from the submodule, its CMake builds under the capture
    where one is given: what it said, and its refusal as a finding."""
    for tool in ("cmake", "clang", "gcc", "nm"):
        if shutil.which(tool) is None:
            raise Refusal(f"the stack's gate needs {tool}")
    work.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, "-I", str(STACK_GATE), "--work", str(work), "--jobs", "4"]
    argv = [*argv, "--selftest"] if selftest else argv
    res = run(argv, cwd=work) if capture is None else \
        ctrl_capture.run(capture, argv, cwd=work, capture_output=True, text=True, env_extra={"LC_ALL": "C"})
    lines = [f"    {line}" for line in (res.stdout + res.stderr).strip().splitlines()]
    return lines, [] if res.returncode == 0 else [f"the stack's own gate {STACK_GATE.relative_to(ROOT)} refused: "
                                                  f"exit {res.returncode}"]


# ---- the planted controls (ctrl_plants) -----------------------------------------------------

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
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new, encoding="utf-8")
            continue
        target = root / file
        text = target.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"control {plant.name!r}: its anchor occurs {text.count(old)} times in {file}")
        target.write_text(text.replace(old, new), encoding="utf-8")
    return trees


def planted_run(plant: Plant, trees: Trees, work: Path, capture: Path) -> list[dict]:
    """A plant's builder, run through `capture` in a directory of its own beside the copies, its files beside it
    there before the capture began (a tick of the file clock earlier); a planted Makefile's compilers named by a
    path, as bypass records (ctrl_pin.named_compilers)."""
    where = (work / "builder").resolve()
    shutil.rmtree(where, ignore_errors=True)
    where.mkdir(parents=True)
    (where / "planted.c").write_text("", encoding="utf-8")
    for name, text in plant.beside:
        (where / name).parent.mkdir(parents=True, exist_ok=True)
        (where / name).write_text(text, encoding="utf-8")
    if plant.beside:
        time.sleep(0.05)
    builder = where / ("planted.mk" if plant.make else "planted_builder.py")
    builder.write_text(plant.run, encoding="utf-8")
    argv = ["make", "-f", str(builder), "planted"] if plant.make else [sys.executable, str(builder)]
    given = {"PLANT_CTRL": str(trees.ctrl), "PLANT_STACK": str(trees.stack), "PLANT_WORK": str(where),
             "PLANT_GCC": shutil.which("gcc") or "gcc"}
    ctrl_capture.run(capture, argv, cwd=where, capture_output=True, text=True, env_extra=given)
    return named_compilers(builder, {**ctrl_capture.install(capture), **given}) if plant.make else []


def control_capture(plant: Plant, trees: Trees, base: Capture, work: Path) -> Capture:
    """The capture a control is judged against: the base the controls share, altered as the plant says, or with
    what its planted builder compiled, run through the capture beside the copies (a shared one ran before the
    base: its invocations are the base's)."""
    if plant.alter == "missing":
        return ctrl_capture.load(work / "no-capture")
    if plant.alter == "empty":
        (work / "empty").mkdir(parents=True, exist_ok=True)
        for name in ("records.jsonl", "manifest.jsonl"):
            (work / "empty" / name).write_text("", encoding="utf-8")
        return ctrl_capture.load(work / "empty")
    if plant.alter.startswith("drop "):
        lost = plant.alter.removeprefix("drop ")
        return replace(base, invocations=tuple(inv for inv in base.invocations if lost not in inv.builders),
                       parts=())
    if not plant.run or plant.shared:
        return base
    capture = (work / "capture").resolve()
    shutil.rmtree(capture, ignore_errors=True)
    named = planted_run(plant, trees, work, capture)
    return base + ctrl_capture.load(capture, required=False) + Capture((), (), (), tuple(named))


def controls(rv32: str | None, work: Path, run: Capture, without: frozenset[str]) -> int:
    """The base the controls share passing (the run's capture, with what every shared planted builder compiled),
    every plant refused by the finding it names (judged until it is found), every pass control passing; the
    misbehaving count."""
    shared = (work / "shared-capture").resolve()
    with ThreadPoolExecutor(max_workers=JOBS, thread_name_prefix="ctrl-boundary-plant") as runner:
        runs = [runner.submit(planted_run, plant, Trees(CTRL, STACK), work / "shared" / str(at), shared)
                for at, plant in enumerate(PLANTS) if plant.shared]
        named = [record for done in runs for record in done.result()]
    base = (run + ctrl_capture.load(shared) if shared.is_dir() else run) + Capture((), (), (), tuple(named))
    bad = 0
    for plant in (BASE, *PLANTS):
        trees = planted(plant, work / "plants")
        try:
            capture = control_capture(plant, trees, base, work / "plant-run")
            findings = judge(trees, rv32, work / "plants-build", capture, control=plant, without=without)
        except (Refusal, CaptureError) as exc:
            findings = [f"REFUSED: {exc}"]
        shutil.rmtree(work / "plants-build", ignore_errors=True)
        ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
        shown = next((f for f in findings if plant.needle and plant.needle in f), findings[0] if findings else "")
        print(f"[{'ok' if ok else 'ESCAPED'}] boundary control {plant.name}: {shown or 'passes'}", flush=True)
        bad += not ok
    shutil.rmtree(work / "plants", ignore_errors=True)
    return bad


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
    args = ap.parse_args(argv)
    without = frozenset(args.without)
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
            given = captures(args.capture, work, without)
            ran = owned(mine, work / "images")
            said, refused = build.result()
            # the stack's own self-test runs beside the controls; its build is the one the capture holds
            own = beside.submit(stack_gate, True, work / "stack-gate", None) if args.selftest else None
            env = ctrl_capture.install(mine)
            named = [record for makefile in makefiles() for record in named_compilers(makefile, env)]
            capture = sum(given[1:], given[0]) + ctrl_capture.load(mine) + Capture((), (), (), tuple(named))
            held(capture, without)
            universe = derive(capture)
            configurations(universe, capture, without, ran)
            bad = pins = 0
            if args.selftest:
                bad = controls(rv32, work / "controls", capture, without)
                print(f"boundary controls: {MEMO.total('ran')} preprocessings run, {MEMO.total('reused')} reused",
                      flush=True)
                (work / "pins").mkdir()
                misbehaved, pins = pin_controls(work / "pins", makefiles())
                bad += misbehaved
            PREPROCESSED.clear()
            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout", capture, without=without)
            runs, checkout = sum(PREPROCESSED), MEMO.made[-1].counts
            cxx = len(cxx_units(Trees(CTRL, STACK), work / "count", capture)[0])
            findings += makefile_findings(makefiles(), work / "makefiles")
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
    found = variants()
    tested = f", {1 + len(PLANTS)} boundary and {pins} pin controls, {bad} misbehaved" if args.selftest else ""
    print(f"ctrl_boundary: {len(firmware_units(Trees(CTRL, STACK)))} firmware units ({cxx} also as C++) and the "
          f"stack's sources, headers and tests, host{' and RV32' if rv32 else ''}, in every configuration of "
          f"{len(universe)} build modes from {len(capture.invocations)} recorded invocations, "
          f"{len(found.shapes)} shapes and {1 + len(found.contracts)} mailbox contracts ({runs} configurations, "
          f"{checkout['ran']} preprocessed), and every Makefile builder's pin prerequisites; {len(findings)} "
          f"finding(s){tested}")
    print(f"ctrl_boundary: {'FAIL' if findings or bad else 'PASS'}")
    return 1 if findings or bad else 0


if __name__ == "__main__":
    sys.exit(main())
