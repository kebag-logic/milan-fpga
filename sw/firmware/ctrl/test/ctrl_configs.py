# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_configs.py - the configurations the firmware's builders compile it in, read from the builders (#697).

The boundary gate (ctrl_boundary.py) judges each unit in every configuration
its builders compile it in; this module reads them, and lists none of them.

THE BUILDERS: every Python module and Makefile of the checkout, tracked or new
and not ignored, that names the firmware's tree (sw/firmware/ctrl, or its
shared builder ctrl_build), the gate's own modules excepted.

THE BUILD MODES: every -D or -U flag a builder writes, as one argument
("-DNAME", "-UNAME=1") or as two ("-D", "NAME": adjacent in a list, a tuple
or a call's arguments, or two words of a Makefile recipe). A macro the C
implementation reserves (C11 7.1.3) is not a mode.

THE VALUES: a flag a builder computes at run time (an f-string, or a bare -D
or -U followed by one) names a macro whose value only the build knows: the
macro is the f-string's literal up to its "=". A flag whose macro is computed
too, which no reader could name, refuses the gate, and so does every other
-D or -U a builder writes that is neither a literal nor an f-string (a
literal joined to a value by +, % or str.format, a bare one alone or before a
name it computes, one make computes: -D$(NAME), -DNAME=$(VALUE) or
$(addprefix -D,...)): each by name.

THE SHAPES: every shipped config (configs/*.yaml), each a shape the image
builders take. For each, the image builder's own ctrl_image.shape_build writes
the store's generated headers and gives the image's stream counts, and every
entity generator (*/*_entity.py) writes its header, as the arms and the image
builders run them. The SRP adapter's shape header is force-included by the
SRP builds, and not by the others.

THE MAILBOX CONTRACT: the tracked one, and the variant its generator writes
(gen_mailbox.py --variant-interfaces) for every interface count it admits,
counting up from one until it refuses.

THE C++ SOURCES: every C++ source a builder names, a test or a bench. A name
resolves beside the builder, among the firmware's tests, in the firmware's
tree, in the stack, in the protocol processor, from the checkout's root, and
in every directory of the checkout the builder names; every file it resolves
to is a source. A name the builder writes itself (write_text, write_bytes,
touch, open for writing, a copy's destination) is generated: it is followed
through the text the builder writes it from, its own literals. A name that
resolves to no file and that the builder does not write fails the gate by
name, and so does a name the builder computes, unless NOT_SOURCES lists it:
a path a self-test writes into a planted report, never a file; each of those
is checked to be held by its builder, unresolved and unwritten.

Each way a builder varies a unit's build is a dimension (Dim): its
alternatives, the one the search holds it at, and what in a preprocessing
shows that the unit depends on it.
"""

from __future__ import annotations

import ast
import atexit
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
from ctrl_build import CTRL, HERE, PP, ROOT, STACK, STACK_PREFIX, Refusal
from srp_arms import DEFAULT_ENTITY

sys.path.insert(0, str(ROOT / "sw/builder"))
from endstation_builder import ConfigError  # noqa: E402

#: The boundary gate's own modules: never a builder.
GATE = frozenset(HERE / name for name in ("ctrl_boundary.py", "ctrl_configs.py", "ctrl_pin.py", "ctrl_plants.py"))
#: The shipped configs: each a shape the image builders take (ctrl_image.py --shape, ctrl_srp_image.py --config).
CONFIGS = ROOT / "configs"
#: The mailbox contract's generator, which writes the contract for another interface count.
GEN_MAILBOX = ROOT / "sw/mailbox/gen_mailbox.py"
#: The mailbox contract, which a variant replaces.
CONTRACT = "mbx_contract.h"
#: The SRP adapter's generated shape header, which the SRP builds force-include and the others do not.
FORCED = "srp_entity_gen.h"
#: What a builder of the firmware names: its tree, or the shared builder the arms, campaigns and fixtures
#: are written on. Every -D or -U flag written in a builder is a build mode the boundary is judged in.
BUILDER_NAMES = ("sw/firmware/ctrl", "ctrl_build")
#: A -D or -U flag, its macro's name in group 1.
FLAG = re.compile(r"-[DU]([A-Za-z_]\w*)(?:=.*)?", re.S)
#: A flag written as two arguments: the bare -D or -U, then its macro (and value).
BARE = ("-D", "-U")
MACRO = re.compile(r"[A-Za-z_]\w*(?:=.*)?", re.S)
#: The macro a flag computed at run time names, read from its literal start: the name, then the "=" its
#: computed value follows.
COMPUTED = re.compile(r"([A-Za-z_]\w*)=")
#: A macro name the C implementation reserves (C11 7.1.3): never a firmware mode.
RESERVED = re.compile(r"_[A-Z_]")
#: A #define line, read as text: its macro and its definition.
DEFINE = re.compile(r"^\s*#\s*define\s+([A-Za-z_]\w*)(.*)$", re.M)
#: The suffixes of a C++ source.
CXX_SUFFIXES = (".cpp", ".cc", ".cxx")
#: The calls that write the file their receiver names (a Path's), and the shutil calls whose second argument is
#: the file they write.
WRITES = frozenset({"write_text", "write_bytes", "touch"})
COPIES = frozenset({"copy", "copy2", "copyfile", "move"})
#: The C++ names a builder holds that are no source it builds from: a path a self-test writes into a planted
#: report, never a file. Each is checked: its builder holds it, it resolves to no file, and the builder does not
#: write it; a file at its name would be followed like any other.
NOT_SOURCES = {
    ("sw/firmware/gtest/fw_coverage_selftest.py", "sw/firmware/ctrl/test/t.cpp"):
        "a firmware test's path in a planted coverage report",
    ("sw/firmware/gtest/fw_coverage_selftest.py", "tests/t.cpp"):
        "a stack test's path in a planted coverage report",
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
    """What one side's units are explored over: the builders' modes, the dimensions the builders vary that side
    along, and the values builders compute that the boundary has none of, each with its builder."""

    modes: dict[str, tuple[str, ...]]
    dims: dict[str, Dim]
    values: dict[str, str]


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One tool, its output captured, its messages in English."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False,
                          env={**os.environ, "LC_ALL": "C"})


def rel(path: Path) -> str:
    """A path of the checkout, named from its root."""
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def literal_start(node: ast.JoinedStr) -> str:
    """The literal text an f-string starts with."""
    first = node.values[0] if node.values else None
    return first.value if isinstance(first, ast.Constant) and isinstance(first.value, str) else ""


def computed_macro(path: Path, start: str) -> str:
    """The macro of a flag a builder computes, from its literal start; a macro it computes too is refused."""
    if m := COMPUTED.match(start):
        return m[1]
    raise Refusal(f"the builder {rel(path)} computes a -D or -U flag's macro: the boundary cannot read it")


def unreadable(path: Path, flag: str) -> Refusal:
    """The refusal of a -D or -U a builder writes in a form the boundary cannot read."""
    return Refusal(f"the builder {rel(path)} writes {flag!r}, a -D or -U flag the boundary cannot read (it reads "
                   "a literal flag, or an f-string that computes only the value)")


def joined(node: ast.AST, parent: dict[int, ast.AST]) -> bool:
    """Whether a literal is one a builder computes a string from: the left of + or %, or str.format's receiver."""
    up = parent.get(id(node))
    return (isinstance(up, ast.BinOp) and isinstance(up.op, (ast.Add, ast.Mod)) and up.left is node) or \
        (isinstance(up, ast.Attribute) and up.attr == "format")


def python_flags(path: Path, text: str) -> tuple[list[str], list[str]]:
    """A Python builder's flags (a string literal that is one, or a bare -D or -U followed, in a list, a tuple or
    a call's arguments, by a literal macro) and the macros of the flags it computes (an f-string, or a bare -D
    or -U followed by one). Any other literal starting -D or -U, a literal joined to a value among them, is
    refused by name."""
    tree = ast.parse(text)
    parts = {id(part) for node in ast.walk(tree) if isinstance(node, ast.JoinedStr) for part in node.values}
    parent = {id(child): node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    flags, values, paired = [], [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr) and literal_start(node)[:2] in BARE:
            values.append(computed_macro(path, literal_start(node)[2:]))
        sequence = node.elts if isinstance(node, (ast.List, ast.Tuple, ast.Set)) else \
            node.args if isinstance(node, ast.Call) else []
        for bare, then in zip(sequence, sequence[1:]):
            if not (isinstance(bare, ast.Constant) and bare.value in BARE):
                continue
            paired.add(id(bare))
            if isinstance(then, ast.Constant) and isinstance(then.value, str) and MACRO.fullmatch(then.value):
                flags.append(bare.value + then.value)
            elif isinstance(then, ast.JoinedStr):
                values.append(computed_macro(path, literal_start(then)))
            else:
                raise Refusal(f"the builder {rel(path)} writes {bare.value} before a macro it computes: the "
                              "boundary cannot read it")
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value[:2] in BARE) or \
                id(node) in parts or id(node) in paired:
            continue
        if FLAG.fullmatch(node.value) and not joined(node, parent):
            flags.append(node.value)
        else:
            raise unreadable(path, node.value)
    return flags, values


def makefile_flags(path: Path, text: str) -> list[str]:
    """A Makefile's flags: the words of its logical lines (comments aside) that are one, or a bare -D or -U
    followed by a macro. Any other word starting -D or -U, or a flag make computes ($ in it), is refused by
    name."""
    flags = []
    for line in text.replace("\\\n", " ").splitlines():
        words = [word.strip("\"'") for word in line.split("#", 1)[0].split()]
        for at, word in enumerate(words):
            if word[:2] not in BARE:
                continue
            flag = word + words[at + 1] if word in BARE and at + 1 < len(words) else word
            if not FLAG.fullmatch(flag) or "$" in flag:
                raise unreadable(path, flag)
            flags.append(flag)
    return flags


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
    boundary gate's own modules (its controls' modes and its exploration's flags are not a builder's)."""
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


@lru_cache(maxsize=None)
def builder_flags(path: Path, text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """One builder's flags and the macros of the flags it computes, read once per text."""
    try:
        flags, values = python_flags(path, text) if path.suffix == ".py" else (makefile_flags(path, text), [])
    except SyntaxError as exc:
        raise Refusal(f"the builder {rel(path)} does not parse: {exc}") from exc
    return tuple(flags), tuple(values)


def derive(planted: dict[Path, str] | None = None) -> tuple[dict[str, tuple[str, ...]], dict[str, str]]:
    """Every macro the builders set or clear, with each flag they write for it; and every macro whose value a
    builder computes, with the first builder that does. A reserved name is the C implementation's."""
    found: dict[str, dict[str, None]] = {}
    computed: dict[str, str] = {}
    for path, text in builder_texts(planted).items():
        flags, values = builder_flags(path, text)
        for flag in flags:
            if not RESERVED.match(name := FLAG.fullmatch(flag)[1]):
                found.setdefault(name, {})[flag] = None
        for name in values:
            computed.setdefault(name, rel(path))
    return {name: tuple(flags) for name, flags in sorted(found.items())}, dict(sorted(computed.items()))


def modes(planted: dict[Path, str] | None = None) -> dict[str, tuple[str, ...]]:
    """Every macro the builders set or clear, with each flag they write for it."""
    return derive(planted)[0]


def makefiles() -> list[Path]:
    """The Makefiles among the builders."""
    return [path for path in builder_texts() if path.suffix != ".py"]


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


def forced_dim() -> Dim:
    """The SRP adapter's shape header: left out, as most builds compile, or force-included, as the SRP builds
    compile every unit. Its own include guard shows a dependence only where it is left out."""
    header = variants().shapes[DEFAULT_ENTITY.stem][0] / FORCED
    defined = set(definitions(header))
    guard = set(re.findall(r"^\s*#\s*ifndef\s+(\w+)", header.read_text(encoding="utf-8"), re.M)) & defined
    return Dim((("", ()), (f"-include {FORCED}", ("-include", FORCED))), 1, frozenset(defined - guard),
               base_only=frozenset(guard))


def contract_dim() -> Dim:
    """The mailbox contract: the tracked one, or a variant force-included ahead of it, as the two-interface
    builds compile the firmware (the variant's include guard keeps the tracked one out)."""
    contracts = variants().contracts
    tracked = CTRL / "mbx" / CONTRACT
    tables = [definitions(tracked), *(definitions(p) for p in contracts.values())]
    differ = len({skeleton(tracked), *(skeleton(p) for p in contracts.values())}) > 1
    alternatives = (("", ()), *((f"interfaces={n}", ("-include", str(p))) for n, p in contracts.items()))
    return Dim(alternatives, 0, varying(tables), frozenset({CONTRACT}) if differ else frozenset())


def image_dim() -> Dim:
    """The image's stream counts: undefined, as every builder but the image's compiles, or a shape's, as
    ctrl_image.shape_build gives them."""
    counts = dict.fromkeys(flags for _, flags in variants().shapes.values())
    names = frozenset(FLAG.fullmatch(flag)[1] for flags in counts for flag in flags)
    return Dim((("", ()), *((" ".join(flags), flags) for flags in counts)), 1, names)


def spaces(universe: dict[str, tuple[str, ...]], computed: dict[str, str]) -> dict[str, Space]:
    """What each side is explored over. A value the builders compute that the image's are not is a dimension of
    its own, defined or not, so that a unit testing it is seen to, and refused."""
    image = image_dim()
    unknown = {name: where for name, where in computed.items() if name not in image.macros}
    guards = {f"<value {name}>": Dim((("", ()), (f"-D{name}", (f"-D{name}",))), 1, frozenset({name}))
              for name in unknown}
    shape, forced, contract = shape_dim(), forced_dim(), contract_dim()
    return {"stack": Space(universe, {"<shape>": shape, "<forced>": forced, "<image>": image, **guards}, unknown),
            "tests": Space(universe, guards, unknown),
            "firmware": Space(universe, {"<shape>": shape, "<contract>": contract, "<forced>": forced,
                                         "<image>": image, **guards}, unknown),
            "c++": Space(universe, {"<shape>": shape, "<contract>": contract, "<forced>": forced, **guards},
                         unknown)}


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
    writes (an -U first, so a mode's value replaces the default's without a redefinition warning); held defined
    until the unit is seen to test it."""
    dims = {}
    for name, flags in universe.items():
        base = default(argv, name)
        other = list(dict.fromkeys(f for f in flags if state(f) != base))
        if other:
            alternatives = (("", ()), *((f, (f"-U{name}", f) if f.startswith("-D") else (f,)) for f in other))
            seed = 0 if base[0] == "defined" else next(i for i, (f, _) in enumerate(alternatives) if f[:2] == "-D")
            dims[name] = Dim(alternatives, seed, frozenset({name}))
    return dims


@dataclass(frozen=True)
class Sources:
    """The C++ sources the builders name: the files each resolves to; for each name a builder writes itself, the
    text it writes it from (its literals); the names that are no source (NOT_SOURCES); and every name that
    resolves to nothing, or that a builder computes, as a finding."""

    files: tuple[Path, ...]
    written: dict[str, str]
    data: tuple[str, ...]
    findings: tuple[str, ...]


def write_target(call: ast.Call) -> ast.AST | None:
    """The expression naming the file a call writes: a Path's write_text, write_bytes or touch receiver, a
    shutil copy's destination, or what open opens for writing (its mode holds w, a, x or +)."""
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr in WRITES:
        return func.value
    if isinstance(func, ast.Attribute) and func.attr in COPIES and len(call.args) > 1:
        return call.args[1]
    builtin = isinstance(func, ast.Name) and func.id == "open"
    if not (builtin or isinstance(func, ast.Attribute) and func.attr == "open"):
        return None
    modes = [*call.args[1 if builtin else 0:], *(k.value for k in call.keywords if k.arg == "mode")]
    if not any(isinstance(m, ast.Constant) and isinstance(m.value, str) and set(m.value) & set("wax+")
               for m in modes):
        return None
    return (call.args[0] if call.args else None) if builtin else func.value


@dataclass(frozen=True)
class Names:
    """What one builder's text names: its C++ names (a literal ending in a C++ suffix; a bare suffix is none),
    the names it computes, the names it writes itself, the checkout's directories it names, and its literals."""

    names: tuple[str, ...]
    computed: tuple[str, ...]
    written: frozenset[str]
    dirs: tuple[Path, ...]
    literals: str


def python_names(text: str) -> tuple[list[str], list[str], set[str], list[str]]:
    """A Python builder's C++ names, the names it computes (an f-string ending in a C++ suffix, a suffix a value
    is joined to, or with_suffix's), the names it writes itself, and every other one-word literal."""
    tree = ast.parse(text)
    parts = {id(part) for node in ast.walk(tree) if isinstance(node, ast.JoinedStr) for part in node.values}
    parent = {id(child): node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    names, computed, written, literals = [], [], set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            tail = node.values[-1] if node.values else None
            if isinstance(tail, ast.Constant) and isinstance(tail.value, str) and tail.value.endswith(CXX_SUFFIXES):
                computed.append(ast.unparse(node))
            continue
        if isinstance(node, ast.Call) and (target := write_target(node)) is not None:
            written |= {n.value for n in ast.walk(target) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)) or id(node) in parts:
            continue
        up = parent.get(id(node))
        if node.value.endswith(CXX_SUFFIXES) and not node.value.split()[1:]:
            if not node.value.rsplit("/", 1)[-1].startswith("."):
                names.append(node.value)
            elif isinstance(up, ast.BinOp) and isinstance(up.op, (ast.Add, ast.Mod)) and up.right is node or \
                    isinstance(up, ast.Call) and isinstance(up.func, ast.Attribute) and up.func.attr == "with_suffix":
                computed.append(ast.unparse(up))
        elif node.value and not node.value.split()[1:]:
            literals.append(node.value)
    return names, computed, written, literals


def makefile_names(text: str) -> tuple[list[str], list[str], list[str]]:
    """A Makefile's C++ names (a word ending in a C++ suffix), the ones make computes (a variable or a pattern in
    it), and every other word."""
    words = [w.strip("\"'") for ln in text.replace("\\\n", " ").splitlines() for w in ln.split("#", 1)[0].split()]
    cxx = [w for w in words if w.endswith(CXX_SUFFIXES) and not w.rsplit("/", 1)[-1].startswith(".")]
    return ([w for w in cxx if "$" not in w and "%" not in w], [w for w in cxx if "$" in w or "%" in w],
            [w for w in words if not w.endswith(CXX_SUFFIXES)])


def joins(name: str, bases: list[Path]) -> list[Path]:
    """A name joined to each base (to the stack's root without its tsn-c-stack/ prefix)."""
    return [STACK / name.removeprefix(STACK_PREFIX) if base == STACK else base / name for base in bases]


@lru_cache(maxsize=None)
def names_of(path: Path, text: str) -> Names:
    """What a builder names, read once per text: a directory is a literal (or a Makefile word) that, joined
    beside the builder, to the firmware's tests or tree, the stack, the checkout's root or the protocol
    processor, is a directory of the checkout."""
    if path.suffix == ".py":
        names, computed, written, words = python_names(text)
        literals = "\n".join(n.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Constant) and
                              isinstance(n.value, str))
    else:
        (names, computed, words), written, literals = makefile_names(text), set(), ""
    bases = [path.parent, HERE, CTRL, STACK, ROOT, PP]
    dirs = {hit.resolve(): None for word in dict.fromkeys(words) if word not in (".", "..") and word[:1] != "-"
            for hit in joins(word, bases) if hit.is_dir() and hit.resolve().is_relative_to(ROOT)}
    return Names(tuple(dict.fromkeys(names)), tuple(dict.fromkeys(computed)), frozenset(written), tuple(dirs),
                 literals)


def cxx_sources(planted: dict[Path, str] | None = None, view: Callable[[Path], Path] | None = None) -> Sources:
    """Every C++ source a builder names (named_sources); the checkout's, as its builders are, gathered once."""
    return checkout_sources() if planted is None and view is None else named_sources(planted, view)


@lru_cache(maxsize=None)
def checkout_sources() -> Sources:
    """Every C++ source the checkout's builders name, in the checkout."""
    return named_sources()


def named_sources(planted: dict[Path, str] | None = None, view: Callable[[Path], Path] | None = None) -> Sources:
    """Every C++ source a builder names (a string literal of a Python builder, or a word of a Makefile, ending in
    a C++ suffix), wherever it is found: beside the builder, among the firmware's tests, in the firmware's tree,
    in the stack (named under tsn-c-stack/ or not), in the protocol processor, from the checkout's root, or in a
    directory of the checkout the builder names; each as `view` gives the checkout's file (the ctrl tree and
    the stack being judged, which may be planted copies). A name the builder writes is followed through its
    literals; a name that is none of these, or that it computes, is a finding unless NOT_SOURCES lists it."""
    view = view or (lambda path: path)
    files: dict[Path, None] = {}
    written: dict[str, str] = {}
    data, findings = [], []
    texts = builder_texts(planted)
    for (where, name), why in NOT_SOURCES.items():
        if ROOT / where not in texts or name not in texts[ROOT / where]:
            findings.append(f"firmware c++: NOT_SOURCES lists {name} for {where}, which no longer names it")
    for path, text in texts.items():
        held = names_of(path, text)
        bases = [path.parent, HERE, CTRL, STACK, ROOT, PP, *held.dirs]
        for name in held.names:
            hits = [hit for join in joins(name, bases) if (hit := view(join.resolve())).is_file()]
            files.update(dict.fromkeys(hits))
            if hits:
                continue
            if name in held.written:
                written[f"{rel(path)} writes {name}"] = held.literals
            elif (rel(path), name) in NOT_SOURCES:
                data.append(f"{name} ({rel(path)}: {NOT_SOURCES[rel(path), name]})")
            else:
                findings.append(f"firmware c++: {rel(path)} names {name}, a C++ source that resolves to no file")
        findings += [f"firmware c++: {rel(path)} computes the name of a C++ source, {name}, which the boundary "
                     "cannot follow" for name in held.computed]
    return Sources(tuple(files), written, tuple(data), tuple(findings))
