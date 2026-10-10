# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_configs.py - the configurations the firmware's builders compile it in, as their compilers were run (#697).

The boundary gate (ctrl_boundary.py) judges each unit in every configuration
its builders compile it in; this module reads them from a capture of the
builders' compiler invocations (ctrl_capture.py), and lists none of them.

THE BUILDERS. BUILDERS is the known set: every builder of the firmware that
compiles, each with the commands that run it when the gate makes the capture
itself. A capture judged must hold an invocation of each, unless the run says
it has none of what that builder needs (--without verilator); each one left
out is named on every run. The builders are found by text as well, as a
cross-check that cannot pass on its own: every Python module and Makefile of
the checkout, tracked or new and not ignored, that names the firmware's tree
(sw/firmware/ctrl, or its shared builder ctrl_build), the gate's own modules
excepted, must have compiled in the capture, be one of BUILDERS (or run only
under one the run leaves out, PART_OF), or be listed in OUTSIDE with the reason
its compiles, if any, are none of the firmware's. Any other refuses the gate
by name, and so does a compiler a builder runs by a path that is no wrapper.

THE BUILD MODES: the macros of every recorded invocation as the compiler's own
expansion of it reports them (ctrl_expand, THE EXPANSION), never as a reader
parses its arguments: each macro its translation unit has defined when its
source begins, other than by the C library's headers or a generated header
a dimension models, with its value (the driver's built-ins, the command line
in any spelling, a file of the checkout read first), and each the command
line or such a file leaves undefined, or the same driver predefines with no
argument and the invocation does not. A macro the C implementation reserves
(C11 7.1.3) is not a mode. The image's stream counts are their own dimension
(image_dim); a recorded value of theirs that no shipped shape gives refuses
the gate.

THE FILES READ FIRST: every file the expansion read before its source
(-include, -imacros, in any spelling, and what those include). The
implementation's (a file the baseline reads, or one in a directory it
searches) and a generated header a dimension models by content (a shipped
config's SRP shape header, a mailbox contract variant) are modeled. A file of
the checkout outside the stack is judged as a firmware unit, and a stack
public header is one; any other (a file of the stack that is not public, a
file outside the checkout) refuses the gate by name, and so does a file of
the checkout read first into a compile of the stack's own sources. An
invocation the compiler could not expand, or whose expansion is none
(ctrl_expand.refusal), refuses the gate by name.

THE SHAPES: every shipped config (configs/*.yaml), each a shape the image
builders take. For each, the image builder's own ctrl_image.shape_build writes
the store's generated headers and gives the image's stream counts, and every
entity generator (*/*_entity.py) writes its header, as the arms and the image
builders run them. The SRP adapter's shape header is force-included by the
SRP builds, and not by the others.

THE MAILBOX CONTRACT: the tracked one, and the variant its generator writes
(gen_mailbox.py --variant-interfaces) for every interface count it admits,
counting up from one until it refuses.

THE C++ SOURCES: the source of every invocation whose expansion compiles it as
C++, as the compiler read it: the trees' file where it is one, else the text
the capture kept, with the directories that invocation's expansion searched
and the headers outside the checkout the capture kept beside it; and every
file of the checkout it read first. A C++ compile of a source that was no
file, or of its standard input, refuses the gate by name.

Each way a builder varies a unit's build is a dimension (Dim): its
alternatives, the one the search holds it at, and what in a preprocessing
shows that the unit depends on it.
"""

from __future__ import annotations

import atexit
import hashlib
import itertools
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, lru_cache
from pathlib import Path

import ctrl_image
from ctrl_build import CTRL, HERE, ROOT, STACK, STACK_INCLUDE, Refusal
from ctrl_capture import Capture, Expansion, Invocation
from ctrl_expand import BUILTIN, COMMAND_LINE
from srp_arms import DEFAULT_ENTITY

sys.path.insert(0, str(ROOT / "sw/builder"))
from endstation_builder import ConfigError  # noqa: E402

#: The boundary gate's own modules: never a builder.
GATE = frozenset(HERE / name for name in ("ctrl_boundary.py", "ctrl_capture.py", "ctrl_configs.py", "ctrl_pin.py",
                                          "ctrl_plants.py", "ctrl_shim.py", "ctrl_expand.py",
                                          "ctrl_runs.py"))
#: The shipped configs: each a shape the image builders take (ctrl_image.py --shape, ctrl_srp_image.py --config).
CONFIGS = ROOT / "configs"
#: The mailbox contract's generator, which writes the contract for another interface count.
GEN_MAILBOX = ROOT / "sw/mailbox/gen_mailbox.py"
#: The mailbox contract, which a variant replaces.
CONTRACT = "mbx_contract.h"
#: The SRP adapter's generated shape header, which the SRP builds force-include and the others do not.
FORCED = "srp_entity_gen.h"
#: What a builder of the firmware names: its tree, or the shared builder the arms, campaigns and fixtures
#: are written on.
BUILDER_NAMES = ("sw/firmware/ctrl", "ctrl_build")
#: A -D or -U flag, its macro's name in group 1 (a function-like macro's parameters after it).
FLAG = re.compile(r"-[DU]([A-Za-z_]\w*)(?:\([^)]*\))?(?:=.*)?", re.S)
#: What a file an expansion read first is (read_first, kind_of).
IMPLEMENTATION, TOOL, MODELED, OWN = "the compiler's own", "an installed tool's", "a header a dimension models", \
    "the builders'"
#: The digest the recorder gives an installed tool's own C++ source, which is not followed (ctrl_shim.RECORDER).
INSTALLED = "installed"
#: A macro name the C implementation reserves (C11 7.1.3): never a firmware mode.
RESERVED = re.compile(r"_[A-Z_]")
#: A #define line, read as text: its macro and its definition.
DEFINE = re.compile(r"^\s*#\s*define\s+([A-Za-z_]\w*)(.*)$", re.M)


@dataclass(frozen=True)
class Builder:
    """One builder of the firmware that compiles: its file (a script, or a Makefile), from the checkout's root;
    the commands that run it when the gate makes the capture itself, from the root ({python} the interpreter,
    {work} a directory of the run's own, {verilator} the Verilator); and what it needs that a run may have none
    of ("verilator")."""

    path: str
    runs: tuple[tuple[str, ...], ...]
    needs: str = ""


#: The known set: every builder of the firmware that compiles. The hosted firmware-unit job runs the first four
#: under the capture (rtl-fast.yml); the gate runs the stack's gate and the image builders itself on every run
#: (ctrl_runs.owned); the last three need Verilator, which the hosted job has none of.
BUILDERS = (
    Builder("sw/firmware/gtest/fw_rv32_selftest.py",
            (("{python}", "sw/firmware/gtest/fw_rv32_selftest.py", "--require-rv32"),)),
    Builder("sw/firmware/ctrl/test/test_ctrl_firmware.py",
            (("{python}", "sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32", "--self-test", "--jobs",
              "4"),)),
    Builder("sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py",
            (("{python}", "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--jobs", "4"),)),
    Builder("sw/firmware/gtest/fw_coverage.py",
            (("{python}", "sw/firmware/gtest/fw_coverage.py", "--selftest"),
             ("{python}", "sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "4"))),
    Builder("third_party/tsn-c-stack/scripts/check_boundary.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_image.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_srp_image.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_image_selftest.py", ()),
    Builder("tb/verilator/mbx/Makefile",
            (("make", "-C", "tb/verilator/mbx", "VERILATOR={verilator}", "VBUILD_JOBS=4"),), "verilator"),
    Builder("sw/firmware/ctrl/test/maap_differential.py",
            (("{python}", "sw/firmware/ctrl/test/maap_differential.py", "--self-test"),), "verilator"),
    Builder("sw/firmware/ctrl/test/aecp_wire.py",
            (("{python}", "sw/firmware/ctrl/test/aecp_wire.py", "--reference", "protocol-processor", "--interfaces",
              "1", "--output", "{work}/aecp-wire", "--verilator", "{verilator}"),), "verilator"),
)
#: What a run may say it has none of: each builder that needs it is left out of the capture, and named.
NEEDS = {"verilator": "Verilator"}
#: The builders found by text that run only under another builder: left out where that one is.
PART_OF = {"tb/verilator/mbx/mutants.py": "tb/verilator/mbx/Makefile"}
#: The builders found by text whose compiles, if any, are none of the firmware's, each with the reason.
OUTSIDE = {
    "docs/diagrams/submodule_boundaries.gen.py": "draws the submodule diagram; it compiles nothing",
    "scripts/ci_events.py": "models the CI workflows; it compiles nothing",
    "scripts/ci_scope.py": "selects the CI scope from the paths a change touches; it compiles nothing",
    "sw/firmware/ctrl/adp/adp_entity.py": "writes the ADP shape header; it compiles nothing",
    "sw/firmware/ctrl/test/ctrl_mutant.py": "the campaign tables' record of one defect; it compiles nothing",
    "sw/firmware/ctrl_nvm/test/nvm_mutants.py": "the saved-state store campaign's planted defects, which "
                                                "test_ctrl_nvm.py compiles; it compiles nothing",
    "sw/firmware/ctrl/test/ctrl_reuse.py": "cuts the processor's sources into fragments the arms compile; it "
                                           "compiles nothing",
    "sw/firmware/ctrl/test/srp_reuse.py": "cuts the processor's SRP sources into fragments the SRP arms compile; it "
                                          "compiles nothing",
    "sw/firmware/ctrl/test/ctrl_image_runtime.py": "compiles the bare-metal runtime from picolibc's and "
                                                   "compiler-rt's sources outside the checkout, no firmware or stack "
                                                   "source, its macros all reserved names",
    "sw/mailbox/gen_mailbox.py": "writes the mailbox contract; it compiles nothing",
    "sw/mailbox/mailbox_emit.py": "writes the mailbox contract's text; it compiles nothing",
}


@dataclass(frozen=True)
class Read:
    """What one preprocessing read: its dependencies and the macros that decided them (tested or expanded where a
    conditional or an #include of a file it read names them, or a definition of one does); its error
    when it does not preprocess, and whether that error is an #error directive's only."""

    deps: frozenset[Path]
    tested: frozenset[str]
    error: str = ""
    stopped: bool = False

    @cached_property
    def names(self) -> frozenset[str]:
        """The name of every file it read."""
        return frozenset(dep.name for dep in self.deps)


@dataclass(frozen=True)
class Dim:
    """One way the builders vary a unit's build. Each alternative is the words a finding names it by and the
    flags it adds; the first is the unit's default build, `seed` the one the search holds it at until the unit
    is seen to depend on it: when one of `macros` decides what a preprocessing reads, when it reads a generated
    header named in `reads`, or, at the default, when one of `base_only` (a force-included header's own guard)
    decides it."""

    alternatives: tuple[tuple[str, tuple[str, ...]], ...]
    seed: int
    macros: frozenset[str]
    reads: frozenset[str] = frozenset()
    base_only: frozenset[str] = frozenset()

    def shown(self, at: int, read: Read) -> bool:
        """Whether one preprocessing, with this dimension at alternative `at`, depends on it."""
        return bool(self.macros & read.tested or self.reads and self.reads & read.names or
                    (at == 0 and self.base_only & read.tested))


@dataclass(frozen=True)
class Space:
    """What one side's units are explored over: the builders' modes and the dimensions the builders vary that
    side along."""

    modes: dict[str, tuple[str, ...]]
    dims: dict[str, Dim]


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One tool, its output captured, its messages in English."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False,
                          env={**os.environ, "LC_ALL": "C"})


def rel(path: Path) -> str:
    """A path of the checkout, named from its root."""
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


# ---- the builders ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def candidates() -> list[Path]:
    """Every Python module and Makefile of the checkout, tracked or new (and not ignored), listed once per run."""
    res = run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
               "*.py", "*Makefile", "*.mk"])
    if res.returncode:
        raise Refusal(f"cannot list the checkout's files: {res.stderr.strip()}")
    return sorted({ROOT / name for name in res.stdout.split("\0") if name and (ROOT / name).is_file()})


def builder(path: Path, text: str) -> bool:
    """Whether a file is one of the firmware's builders: it names the firmware's tree, and it is not one of the
    boundary gate's own modules (its controls' builders are not the checkout's)."""
    return path.resolve() not in GATE and any(n in text for n in BUILDER_NAMES)


@lru_cache(maxsize=None)
def checkout_builders() -> tuple[tuple[Path, str], ...]:
    """Every builder the checkout holds, with its text: read once per run, as the gate writes nothing there."""
    texts = ((path, path.read_text(encoding="utf-8", errors="replace")) for path in candidates())
    return tuple((path, text) for path, text in texts if builder(path, text))


def builder_texts(planted: dict[Path, str] | None = None) -> dict[Path, str]:
    """The text of every builder the checkout holds, with `planted` replacing a file's text, or adding a new
    file, for the self-test."""
    texts = dict(checkout_builders())
    for path, text in (planted or {}).items():
        texts.pop(path, None)
        if builder(path, text):
            texts[path] = text
    return dict(sorted(texts.items()))


def makefiles() -> list[Path]:
    """The Makefiles among the builders."""
    return [path for path in builder_texts() if path.suffix != ".py"]


def left_out(without: frozenset[str]) -> list[Builder]:
    """The known builders a run leaves out: those needing what it says it has none of."""
    return [b for b in BUILDERS if b.needs and b.needs in without]


def held(capture: Capture, without: frozenset[str], planted: dict[Path, str] | None = None,
         trees: tuple[Path, Path] = (CTRL, STACK)) -> None:
    """Refuse, by name, a known builder the capture holds no invocation of, a builder found by text that compiled
    nothing in it and is none of BUILDERS, PART_OF or OUTSIDE, a compiler a builder ran by a path that is no
    wrapper, and an invocation whose expansion is none or reads a file first that is not modeled (expanded; a
    file of the trees judged, the ctrl tree's and the stack's, is the checkout's)."""
    out = {b.path for b in left_out(without)}
    known = {b.path for b in BUILDERS}
    reasons = [f"the capture holds no invocation of {b.path}, a builder of the firmware that compiles"
               for b in BUILDERS if b.path not in out and b.path not in capture.builders]
    for path in builder_texts(planted):
        name = rel(path)
        if name in capture.builders or name in known or name in OUTSIDE or PART_OF.get(name) in out:
            continue
        reasons.append(f"{name} names the firmware's tree, compiled nothing in the capture, and is neither a known "
                       "builder (ctrl_configs.BUILDERS) nor one whose compiles are none of the firmware's (OUTSIDE)")
    for bypass in capture.bypassed:
        reasons.append(f"{', '.join(bypass['from']) or 'a builder'} ran {bypass['bypass']}, a compiler the capture "
                       "does not wrap, so it records none of that compiler's invocations")
    reasons += [reason for leaf in capture.leaves for reason in once("unkept", leaf, unkept)]
    where = places(trees)
    reasons += [reason for leaf in capture.leaves for reason in
                once(f"expanded {where}", leaf, lambda c: expanded(c, where))]
    if reasons:
        raise Refusal("; ".join(dict.fromkeys(reasons)))


def unkept(capture: Capture) -> list[str]:
    """Each C++ compile of a source the capture could not keep: one that was no file, or standard input."""
    reasons = []
    for inv in capture.invocations:
        for path, lang, digest in inv.sources:
            if lang == "c++" and not digest:
                where = "its standard input" if path == "-" else f"{path}, which was no file when it ran"
                reasons.append(f"{', '.join(sorted(inv.builders)) or 'a builder'} compiled C++ from {where}")
    return reasons


#: What is read from each capture, once per capture: a control's capture is joined from the run's and its own.
READ: dict[tuple[str, int], tuple[Capture, object]] = {}


def once(kind: str, capture: Capture, read: Callable[[Capture], object]) -> object:
    """What `read` gives for a capture, read once (by kind and identity)."""
    known = READ.get((kind, id(capture)))
    if known is None or known[0] is not capture:
        READ[(kind, id(capture))] = known = (capture, read(capture))
    return known[1]


def command(inv: Invocation) -> str:
    """An invocation, named: who ran it and how (its arguments cut short)."""
    words = " ".join([inv.tool, *inv.args])
    return f"{', '.join(sorted(inv.builders)) or 'a builder'} ran {words[:200]}{' ...' if len(words) > 200 else ''}"


@lru_cache(maxsize=None)
def modeled() -> frozenset[str]:
    """The digests of the generated headers a dimension models when a build reads one first: every shipped
    config's SRP shape header (the forced dimension, at each shape) and every mailbox contract variant."""
    found = variants()
    headers = [gen / FORCED for gen, _ in found.shapes.values()] + list(found.contracts.values())
    return frozenset(hashlib.sha256(h.read_bytes()).hexdigest() for h in headers if h.is_file())


def expansions(inv: Invocation) -> list[Expansion]:
    """An invocation's expansion, then those of the compiles that made each precompiled header it read first."""
    return [inv.expansion, *inv.first] if inv.expansion is not None else []


def read_first(inv: Invocation) -> list[tuple[str, str]]:
    """Every file an invocation read before its source, resolved, with what it is: the implementation's (its
    baseline read it, or it lies in a directory its baseline searches), an installed tool's (as the recorder
    judges a C++ source), a header a dimension models (by content), or the builders' own. A precompiled header's
    header and what it read are read first by every compile that reads the precompiled header."""
    return once_read_first(tuple(expansions(inv)))


@lru_cache(maxsize=None)
def once_read_first(made: tuple[Expansion, ...]) -> list[tuple[str, str]]:
    """read_first of a tuple of expansions, made once."""
    own = frozenset().union(*(b.own for e in made for _, b in e.baseline))
    found: dict[str, str] = {}
    for exp in made:
        for _, where, digest, tool in (*exp.entered, *(exp.mains if exp is not made[0] else ())):
            if where in own or any(where.startswith(d.rstrip("/") + "/") for d in own):
                found[where] = IMPLEMENTATION
            else:
                found[where] = TOOL if tool else MODELED if digest in modeled() else OWN
    return list(found.items())


def places(trees: tuple[Path, Path]) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    """The checkout's places for the trees judged (the ctrl tree's and the stack's, the checkout's or copies):
    every root of the checkout, and every stack."""
    ctrl, stack = (t.resolve() for t in trees)
    return tuple(dict.fromkeys((ROOT.resolve(), ctrl, stack))), tuple(dict.fromkeys((STACK.resolve(), stack)))


def kind_of(where: str, places_of: tuple[tuple[Path, ...], tuple[Path, ...]]) -> str:
    """Where a file read first lies: "public" (a stack's public header), "stack" (another file of a stack),
    "checkout" (another file of the checkout, tracked, or of the trees judged), or "outside" (a build's own)."""
    path, (tops, stacks) = Path(where), places_of
    for stack in stacks:
        if path.is_relative_to(stack):
            return "public" if path.is_relative_to(stack / STACK_INCLUDE) else "stack"
    return "checkout" if any(path.is_relative_to(top) for top in tops) and tracked(path) else "outside"


def expanded(capture: Capture, where_of: tuple[tuple[Path, ...], tuple[Path, ...]]) -> list[str]:
    """Each invocation the capture could not have expanded, whose expansion is none, or whose expansion read a file
    first that is neither the implementation's, nor modeled, nor a file of the checkout outside the stack (or a
    public header of it) read into a compile that is not of the stack's own sources."""
    stacks = where_of[1]
    reasons = []
    for inv in capture.invocations:
        made = inv.expansion
        if inv.failed or made is not None and made.error:
            reasons.append(f"{command(inv)}, which the compiler could not expand: {inv.failed or made.error}")
            continue
        if made is None:
            continue
        ours = [(where, kind_of(where, where_of)) for where, what in read_first(inv) if what == OWN]
        inputs = [Path(path) for path, _, _ in inv.sources if path != "-"]
        stack_own = any(path.is_relative_to(s) for path in inputs for s in stacks)
        for where, kind in ours:
            if kind == "stack":
                reasons.append(f"{command(inv)}, which reads {where} first, a file of the stack that is not one of "
                               "its public headers")
            elif kind != "public" and stack_own:
                reasons.append(f"{command(inv)}, which reads {where} first into a compile of the stack's own "
                               "sources: not one of the stack's public headers")
    return reasons


def read_first_units(capture: Capture, trees: tuple[Path, Path]) -> list[Path]:
    """The files of the checkout outside the stack that an invocation read first: each judged as a firmware unit."""
    where_of = places(trees)
    found: dict[Path, None] = {}
    for leaf in capture.leaves:
        for inv in once("by expansions", leaf, lambda c: list({(i.expansion.digest, *(e.digest for e in i.first)): i
                                                               for i in c.invocations
                                                               if i.expansion is not None}.values())):
            for where, what in read_first(inv):
                if what == OWN and kind_of(where, where_of) == "checkout" and tracked(Path(where)):
                    found[Path(where)] = None
    return list(found)


def tracked(path: Path) -> bool:
    """Whether a file is one the checkout tracks, or one of a copy of the trees a control judges (outside the
    checkout): a build's own file under the checkout (a generated header in an object directory) is not."""
    if not path.is_relative_to(ROOT.resolve()):
        return path.is_file()
    return path.relative_to(ROOT.resolve()).as_posix() in tracked_files()


@lru_cache(maxsize=None)
def tracked_files() -> frozenset[str]:
    """Every file the checkout tracks, its submodules' included, listed once per run."""
    res = run(["git", "-C", str(ROOT), "ls-files", "-z", "--recurse-submodules"])
    if res.returncode:
        raise Refusal(f"cannot list the checkout's files: {res.stderr.strip()}")
    return frozenset(name for name in res.stdout.split("\0") if name)


# ---- the build modes ------------------------------------------------------------------------


def derive(capture: Capture) -> dict[str, tuple[str, ...]]:
    """Every macro the recorded invocations set or clear, with each flag they give it (but the image's stream
    counts, a dimension of their own); a reserved name is the C implementation's. Read once per capture part."""
    def joined(whole: Capture) -> dict[str, tuple[str, ...]]:
        """The modes of each part, in order."""
        found: dict[str, dict[str, None]] = {}
        for leaf in whole.leaves:
            for name, flags in once("modes", leaf, modes_of).items():
                found.setdefault(name, {}).update(dict.fromkeys(flags))
        return {name: tuple(flags) for name, flags in sorted(found.items())}
    return once("joined modes", capture, joined)


def rendered(name: str, params: str, value: str | None) -> str:
    """A macro's state as the flag that gives it: -DNAME when it is 1, -DNAME(params)=value, or -UNAME."""
    if value is None:
        return f"-U{name}"
    return f"-D{name}" if not params and value == "1" else f"-D{name}{params}={value}"


def flags_of(inv: Invocation) -> tuple[str, ...]:
    """The build modes an invocation's expansion reports (THE BUILD MODES): for each unit (its own, and those of
    the compiles that made each precompiled header it read first), every macro defined when its source begins,
    as a flag, but those the implementation's files, an installed tool's or a modeled header last set; every one
    the command line or a file of the builders' own last undefined; and every one the baseline predefines that it
    lacks. Reserved names are left to the callers."""
    return once_flags(tuple(expansions(inv)))


@lru_cache(maxsize=None)
def once_flags(made: tuple[Expansion, ...]) -> tuple[str, ...]:
    """flags_of of a tuple of expansions, made once."""
    ours = {where for where, what in once_read_first(made) if what == OWN}
    flags: dict[str, None] = {}
    for exp in made:
        printed = {name: where for name, where, _, _ in (*exp.entered, *exp.mains)}
        flags.update(dict.fromkeys(unit_flags(exp, printed, ours)))
    return tuple(flags)


def unit_flags(made: Expansion, printed: dict[str, str], ours: set[str]) -> list[str]:
    """The flags of one expansion's units (once_flags), its files read by the name they were printed at."""
    flags: dict[str, None] = {}
    for unit in made.units:
        table: dict[str, tuple[str, str | None]] = {n: (p, v) for n, p, v in unit.builtins}
        last = dict.fromkeys(table, BUILTIN)
        for where, name, params, value in unit.ops:
            table[name], last[name] = (params, value), where
        for name, where in last.items():
            if where in (BUILTIN, *COMMAND_LINE) or printed.get(where) in ours:
                flags[rendered(name, *table[name])] = None
        base = made.base(unit.language)
        for name, _, _ in base.builtins if base else ():
            if table.get(name, ("", None))[1] is None:
                flags[f"-U{name}"] = None
    return list(flags)


def modes_of(capture: Capture) -> dict[str, tuple[str, ...]]:
    """The build modes of one capture part."""
    image = image_dim()
    given = {state(f) for _, flags in image.alternatives for f in flags}
    found: dict[str, dict[str, None]] = {}
    for inv in {(i.expansion.digest, *(e.digest for e in i.first)): i for i in capture.invocations
                if i.expansion is not None and not i.expansion.error and not i.failed}.values():
        for flag in flags_of(inv):
            name = FLAG.fullmatch(flag)[1]
            if RESERVED.match(name):
                continue
            if name in image.macros:
                if state(flag) not in given:
                    raise Refusal(f"{command(inv)}, which compiles with {flag}, a stream count no shipped shape "
                                  "gives (ctrl_image.shape_build)")
                continue
            found.setdefault(name, {})[flag] = None
    return {name: tuple(flags) for name, flags in sorted(found.items())}


@dataclass(frozen=True)
class Variants:
    """What the builders generate per configuration: each shipped config's generated headers and the image's
    stream-count flags; and the mailbox contract written for each interface count but the tracked one's."""

    shapes: dict[str, tuple[Path, tuple[str, ...]]]
    contracts: dict[int, Path]


@lru_cache(maxsize=None)
def variants() -> Variants:
    """Every shipped config's generated headers, by the builders' own generators, and every contract variant the
    mailbox generator admits; written once per run."""
    work = Path(tempfile.mkdtemp(prefix="ctrl-boundary-variants-"))
    atexit.register(shutil.rmtree, work, True)
    shapes = {}
    for config in sorted(CONFIGS.glob("*.yaml")):
        try:
            gen, flags = ctrl_image.shape_build(config, work / config.stem)
        except (ConfigError, subprocess.CalledProcessError) as exc:
            raise Refusal(f"the end-station builder refused {config.name}, whose shape the image builders "
                          f"take: {exc}") from exc
        for generator in sorted(CTRL.glob("*/*_entity.py")):
            res = run([sys.executable, "-B", str(generator), str(config), "-o", str(gen / f"{generator.stem}_gen.h")])
            if res.returncode:
                raise Refusal(f"{generator.name} refused {config.name}: {res.stderr.strip()}")
        shapes[config.stem] = (gen, tuple(flags))
    if DEFAULT_ENTITY.stem not in shapes:
        raise Refusal(f"the arms' default entity {DEFAULT_ENTITY.name} is not a shipped config")
    tracked = (CTRL / "mbx" / CONTRACT).read_text(encoding="utf-8")
    contracts = {}
    for count in itertools.count(1):
        out = work / f"interfaces-{count}"
        res = run([sys.executable, "-B", str(GEN_MAILBOX), "--variant-interfaces", str(count), "--out", str(out)])
        if res.returncode == 2 and res.stdout.startswith("REFUSED") and count > 1:
            break
        if res.returncode:
            raise Refusal(f"{GEN_MAILBOX.name} failed for {count} interfaces: {(res.stdout + res.stderr).strip()}")
        if (out / CONTRACT).read_text(encoding="utf-8") != tracked:
            contracts[count] = out / CONTRACT
    return Variants(shapes, contracts)


def definitions(path: Path) -> dict[str, str]:
    """The macros a header defines, each with its definition, read as text."""
    text = path.read_text(encoding="utf-8", errors="replace").replace("\\\n", " ")
    return {m[1]: m[2].strip() for m in DEFINE.finditer(text)}


def skeleton(path: Path) -> tuple[str, ...]:
    """A header's directives other than its definitions: what decides what else it reads."""
    text = path.read_text(encoding="utf-8", errors="replace").replace("\\\n", " ")
    return tuple(ln.strip() for ln in text.splitlines() if ln.lstrip().startswith("#") and not DEFINE.match(ln))


def varying(tables: list[dict[str, str]]) -> frozenset[str]:
    """The macros the tables do not all define alike."""
    return frozenset(n for n in set().union(*tables) if len({t.get(n) for t in tables}) > 1)


@lru_cache(maxsize=None)
def shape_dim() -> Dim:
    """The shapes: each shipped config's generated headers, searched first for a quoted include as the image
    builder puts them; the arms' default config is the unit's default build."""
    shapes = variants().shapes
    order = [DEFAULT_ENTITY.stem, *sorted(s for s in shapes if s != DEFAULT_ENTITY.stem)]
    headers = [{p.relative_to(shapes[s][0]).as_posix(): p for p in shapes[s][0].rglob("*.h")} for s in order]
    tables = [{m: d for p in held.values() for m, d in definitions(p).items()} for held in headers]
    names = set().union(*headers)
    reads = frozenset(Path(n).name for n in names if len({skeleton(h[n]) if n in h else None for h in headers}) > 1)
    alternatives = tuple((f"shape={s}" if i else "", ("-iquote", str(shapes[s][0]), "-I", str(shapes[s][0])))
                         for i, s in enumerate(order))
    return Dim(alternatives, 0, varying(tables), reads)


@lru_cache(maxsize=None)
def forced_dim() -> Dim:
    """The SRP adapter's shape header: left out, as most builds compile, or force-included, as the SRP builds
    compile every unit. Its own include guard shows a dependence only where it is left out."""
    header = variants().shapes[DEFAULT_ENTITY.stem][0] / FORCED
    defined = set(definitions(header))
    guard = set(re.findall(r"^\s*#\s*ifndef\s+(\w+)", header.read_text(encoding="utf-8"), re.M)) & defined
    return Dim((("", ()), (f"-include {FORCED}", ("-include", FORCED))), 1, frozenset(defined - guard),
               base_only=frozenset(guard))


@lru_cache(maxsize=None)
def contract_dim() -> Dim:
    """The mailbox contract: the tracked one, or a variant force-included ahead of it, as the two-interface
    builds compile the firmware (the variant's include guard keeps the tracked one out)."""
    contracts = variants().contracts
    tracked = CTRL / "mbx" / CONTRACT
    tables = [definitions(tracked), *(definitions(p) for p in contracts.values())]
    differ = len({skeleton(tracked), *(skeleton(p) for p in contracts.values())}) > 1
    alternatives = (("", ()), *((f"interfaces={n}", ("-include", str(p))) for n, p in contracts.items()))
    return Dim(alternatives, 0, varying(tables), frozenset({CONTRACT}) if differ else frozenset())


@lru_cache(maxsize=None)
def image_dim() -> Dim:
    """The image's stream counts: undefined, as every builder but the image's compiles, or a shape's, as
    ctrl_image.shape_build gives them."""
    counts = dict.fromkeys(flags for _, flags in variants().shapes.values())
    names = frozenset(FLAG.fullmatch(flag)[1] for flags in counts for flag in flags)
    return Dim((("", ()), *((" ".join(flags), flags) for flags in counts)), 1, names)


def spaces(universe: dict[str, tuple[str, ...]]) -> dict[str, Space]:
    """What each side is explored over."""
    image, shape, forced, contract = image_dim(), shape_dim(), forced_dim(), contract_dim()
    return {"stack": Space(universe, {"<shape>": shape, "<forced>": forced, "<image>": image}),
            "tests": Space(universe, {}),
            "firmware": Space(universe, {"<shape>": shape, "<contract>": contract, "<forced>": forced,
                                         "<image>": image}),
            "c++": Space(universe, {"<shape>": shape, "<contract>": contract, "<forced>": forced})}


def state(flag: str | None) -> tuple[str, ...]:
    """What a -D or -U flag leaves its macro as: defined with a value, or undefined."""
    if flag is None or flag.startswith("-U"):
        return ("undefined",)
    return ("defined", flag[2:].partition("=")[2] or "1")


def default(argv: list[str], name: str) -> tuple[str, ...]:
    """What the unit's own flags leave `name` as; the last flag for it wins."""
    return state(next((a for a in reversed(argv) if (m := FLAG.fullmatch(a)) and m[1] == name), None))


def mode_dims(argv: list[str], universe: dict[str, tuple[str, ...]]) -> dict[str, Dim]:
    """Each build mode as a dimension: the unit's own state of its macro, then every other one a builder
    compiled with (an -U first, so a mode's value replaces the default's without a redefinition warning); held
    defined until the unit is seen to test it."""
    dims = {}
    for name, flags in universe.items():
        base = default(argv, name)
        other = list(dict.fromkeys(f for f in flags if state(f) != base))
        if other:
            alternatives = (("", ()), *((f, (f"-U{name}", f) if f.startswith("-D") else (f,)) for f in other))
            seed = 0 if base[0] == "defined" else next(i for i, (f, _) in enumerate(alternatives) if f[:2] == "-D")
            dims[name] = Dim(alternatives, seed, frozenset({name}))
    return dims


# ---- the C++ sources ------------------------------------------------------------------------


@dataclass(frozen=True)
class CxxSource:
    """The source of recorded C++ invocations: where the compiler read it, the text the capture kept of it, the
    directories those invocations searched, and the headers outside the checkout kept beside it."""

    path: Path
    digest: str
    dirs: tuple[Path, ...]
    kept: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class CxxIndex:
    """The C++ sources of a capture; every directory its C++ invocations searched, and those that were
    directories when it was read; the headers it kept beside them, with their texts; and each kept header by every
    name it can be reached at under a searched one."""

    sources: tuple[CxxSource, ...]
    dirs: tuple[Path, ...]
    present: tuple[Path, ...]
    kept: dict[Path, str]
    reached: dict[str, tuple[Path, ...]]


def cxx_index(capture: Capture) -> CxxIndex:
    """A capture's C++ index (CxxIndex), made once."""
    return once("index", capture, indexed)


def indexed(capture: Capture) -> CxxIndex:
    """The C++ index of cxx_index."""
    sources = tuple(cxx_sources(capture))
    dirs = tuple(dict.fromkeys(d for source in sources for d in source.dirs))
    kept = {Path(p): digest for source in sources for p, digest in source.kept}
    searched = set(dirs)
    reached: dict[str, list[Path]] = {}
    for path in kept:
        for up in path.parents:
            if up in searched:
                reached.setdefault(path.relative_to(up).as_posix(), []).append(path)
    return CxxIndex(sources, dirs, tuple(d for d in dirs if d.is_dir()), kept,
                    {name: tuple(paths) for name, paths in reached.items()})


def cxx_sources(capture: Capture) -> list[CxxSource]:
    """Every source a recorded invocation compiled as C++, and every file such an invocation read first
    (-include), once per path and text; read once per capture part."""
    found: dict[tuple[str, str], tuple[dict[str, None], dict[str, str]]] = {}
    for leaf in capture.leaves:
        for key, (dirs, kept) in once("sources", leaf, sources_of).items():
            held_dirs, held_kept = found.setdefault(key, ({}, {}))
            held_dirs.update(dirs)
            held_kept.update(kept)
    return [CxxSource(Path(path), digest, tuple(Path(d) for d in dirs), tuple(sorted(kept.items())))
            for (path, digest), (dirs, kept) in sorted(found.items())]


def sources_of(capture: Capture) -> dict[tuple[str, str], tuple[dict[str, None], dict[str, str]]]:
    """The C++ sources of one capture part: each (path, digest) with the directories searched and the headers
    kept beside it."""
    found: dict[tuple[str, str], tuple[dict[str, None], dict[str, str]]] = {}
    for inv in capture.invocations:
        if not any(lang == "c++" for _, lang, _ in inv.sources) or inv.expansion is None:
            continue
        kept = dict(inv.kept)
        starts = [(path, digest) for path, lang, digest in inv.sources
                  if lang == "c++" and digest and digest != INSTALLED]
        forced = [(where, "") for where, what in read_first(inv) if what == OWN]
        for key in [*starts, *forced]:
            dirs, beside = found.setdefault(key, ({}, {}))
            dirs.update(dict.fromkeys(d for e in expansions(inv) for d in e.dirs))
            beside.update(kept)
    return found


def configurations(universe: dict[str, tuple[str, ...]], capture: Capture, without: frozenset[str],
                   ran: list[str]) -> None:
    """What the configurations are drawn from: the capture's invocations, and the builders' generators."""
    found = variants()
    image = image_dim()
    known = [b.path for b in BUILDERS if b.path in capture.builders]
    print(f"capture: {len(capture.invocations)} compiler invocations from {len(capture.commands)} builder runs; "
          f"every known builder held: {', '.join(known)}")
    for b in left_out(without):
        print(f"  LEFT OUT: {b.path}, which needs {NEEDS[b.needs]}, which this run has none of (--without {b.needs})")
    print("\n".join(ran))
    print("build modes, from the recorded invocations: " +
          "; ".join(f"{name} ({' '.join(flags)})" for name, flags in universe.items()))
    print(f"shapes, the shipped configs: {', '.join(found.shapes)} (default {DEFAULT_ENTITY.stem}); the image's "
          f"stream counts (ctrl_image.shape_build): {'; '.join(w for w, _ in image.alternatives[1:])}; mailbox "
          f"contracts: the tracked one and {', '.join(f'{n} interfaces' for n in found.contracts) or 'no variant'}")
    sources = cxx_sources(capture)
    inside = [s for s in sources if s.path.is_relative_to(ROOT)]
    tools = {Path(path).name for inv in capture.invocations for path, lang, digest in inv.sources
             if digest == INSTALLED}
    print(f"C++ sources the recorded invocations compile, and the files they read first: "
          f"{len({s.path for s in sources})} ({len({s.path for s in inside})} in the checkout, the rest as the "
          f"capture kept them); installed tools' own, not followed: {', '.join(sorted(tools)) or 'none'}", flush=True)
