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
or -U followed by one) names a macro whose value only the build knows. A flag
whose macro is computed too, which no reader could name, refuses the gate.

THE SHAPES: every shipped config (configs/*.yaml), each a shape the image
builders take. For each, the image builder's own ctrl_image.shape_build writes
the store's generated headers and gives the image's stream counts, and every
entity generator (*/*_entity.py) writes its header, as the arms and the image
builders run them. The SRP adapter's shape header is force-included by the
SRP builds, and not by the others.

THE MAILBOX CONTRACT: the tracked one, and the variant its generator writes
(gen_mailbox.py --variant-interfaces) for every interface count it admits,
counting up from one until it refuses.

THE C++ SOURCES: every C++ source a builder names, a test or a bench.

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
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import ctrl_image
from ctrl_build import CTRL, HERE, PP, ROOT, STACK, STACK_PREFIX, Refusal
from srp_arms import DEFAULT_ENTITY

sys.path.insert(0, str(ROOT / "sw/builder"))
from endstation_builder import ConfigError  # noqa: E402

#: The boundary gate's own modules: never a builder.
GATE = frozenset(HERE / name for name in ("ctrl_boundary.py", "ctrl_configs.py", "ctrl_pin.py"))
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
#: The macro a flag computed at run time names, read from its literal start.
COMPUTED = re.compile(r"([A-Za-z_]\w*)(?:=|$)")
#: A macro name the C implementation reserves (C11 7.1.3): never a firmware mode.
RESERVED = re.compile(r"_[A-Z_]")
#: A #define line, read as text: its macro and its definition.
DEFINE = re.compile(r"^\s*#\s*define\s+([A-Za-z_]\w*)(.*)$", re.M)
#: The suffixes of a C++ source.
CXX_SUFFIXES = (".cpp", ".cc", ".cxx")


@dataclass(frozen=True)
class Read:
    """What one preprocessing read: its dependencies and the macros that decided them (tested or expanded where a
    conditional or an #include of a file it read names them, or a definition of one does); its error
    when it does not preprocess, and whether that error is an #error directive's only."""

    deps: frozenset[Path]
    tested: frozenset[str]
    error: str = ""
    stopped: bool = False


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
        return bool(self.macros & read.tested or self.reads & {d.name for d in read.deps} or
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


def python_flags(path: Path, text: str) -> tuple[list[str], list[str]]:
    """A Python builder's flags (a string literal that is one, or a bare -D or -U followed, in a list, a tuple or
    a call's arguments, by a literal macro) and the macros of the flags it computes (an f-string, or a bare -D
    or -U followed by one)."""
    tree = ast.parse(text)
    parts = {id(part) for node in ast.walk(tree) if isinstance(node, ast.JoinedStr) for part in node.values}
    flags, values = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and id(node) not in parts and isinstance(node.value, str) and \
                FLAG.fullmatch(node.value):
            flags.append(node.value)
        elif isinstance(node, ast.JoinedStr) and literal_start(node)[:2] in BARE:
            values.append(computed_macro(path, literal_start(node)[2:]))
        sequence = node.elts if isinstance(node, (ast.List, ast.Tuple, ast.Set)) else \
            node.args if isinstance(node, ast.Call) else []
        for bare, then in zip(sequence, sequence[1:]):
            if not (isinstance(bare, ast.Constant) and bare.value in BARE):
                continue
            if isinstance(then, ast.Constant) and isinstance(then.value, str) and MACRO.fullmatch(then.value):
                flags.append(bare.value + then.value)
            elif isinstance(then, ast.JoinedStr):
                values.append(computed_macro(path, literal_start(then)))
            elif not isinstance(then, ast.Constant):
                raise Refusal(f"the builder {rel(path)} writes {bare.value} before a macro it computes: the "
                              "boundary cannot read it")
    return flags, values


def makefile_flags(text: str) -> list[str]:
    """A Makefile's flags: the words of its logical lines (comments aside) that are one, or a bare -D or -U
    followed by a macro."""
    flags = []
    for line in text.replace("\\\n", " ").splitlines():
        words = [word.strip("\"'") for word in line.split("#", 1)[0].split()]
        flags += [word for word in words if FLAG.fullmatch(word)]
        flags += [bare + then for bare, then in zip(words, words[1:]) if bare in BARE and MACRO.fullmatch(then)]
    return flags


def candidates() -> list[Path]:
    """Every Python module and Makefile of the checkout, tracked or new (and not ignored)."""
    res = run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
               "*.py", "*Makefile", "*.mk"])
    if res.returncode:
        raise Refusal(f"cannot list the checkout's files: {res.stderr.strip()}")
    return sorted({ROOT / name for name in res.stdout.split("\0") if name and (ROOT / name).is_file()})


def builders(texts: dict[Path, str]) -> list[Path]:
    """The firmware's builders among the files `texts` holds: each that names the firmware's tree, the boundary
    gate's own modules excepted (its controls' modes and its exploration's flags are not a builder's)."""
    return [path for path, text in texts.items()
            if path.resolve() not in GATE and any(n in text for n in BUILDER_NAMES)]


def builder_texts(planted: dict[Path, str] | None = None) -> dict[Path, str]:
    """The text of every builder the checkout holds, with `planted` replacing a file's text, or adding a new
    file, for the self-test."""
    texts = {path: path.read_text(encoding="utf-8", errors="replace") for path in candidates()}
    texts.update(planted or {})
    return {path: texts[path] for path in builders(texts)}


def derive(planted: dict[Path, str] | None = None) -> tuple[dict[str, tuple[str, ...]], dict[str, str]]:
    """Every macro the builders set or clear, with each flag they write for it; and every macro whose value a
    builder computes, with the first builder that does. A reserved name is the C implementation's."""
    found: dict[str, dict[str, None]] = {}
    computed: dict[str, str] = {}
    for path, text in builder_texts(planted).items():
        try:
            flags, values = python_flags(path, text) if path.suffix == ".py" else (makefile_flags(text), [])
        except SyntaxError as exc:
            raise Refusal(f"the builder {rel(path)} does not parse: {exc}") from exc
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


def cxx_sources() -> list[Path]:
    """Every C++ source a builder names (a string literal of a Python builder, or a word of a Makefile, ending in
    a C++ suffix), wherever it is found: beside the builder, among the firmware's tests, in the stack (named
    under tsn-c-stack/ or not), in the protocol processor or from the checkout's root."""
    found: dict[Path, None] = {}
    for path, text in builder_texts().items():
        if path.suffix == ".py":
            names = [n.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Constant) and
                     isinstance(n.value, str) and n.value.endswith(CXX_SUFFIXES) and not n.value.split()[1:]]
        else:
            names = [w for w in text.replace("\\\n", " ").split() if w.endswith(CXX_SUFFIXES)]
        for name in names:
            for base in (path.parent, HERE, STACK, ROOT, PP):
                hit = base / name.removeprefix(STACK_PREFIX) if base == STACK else base / name
                if hit.is_file():
                    found[hit.resolve()] = None
    return list(found)
