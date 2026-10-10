# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_elab.py - milan_datapath as the pinned elaborator builds it, read back as a netlist.

publication_census.py classifies the processor's class-D values by where they
flow in the datapath. This module produces that flow from a real elaborator,
never from the source text (#665, comment 6097292237), so the form a read is
written in stops mattering: the census sees what the elaborator built.

THE RECIPE is CI's. ``syn/yosys/run.sh --emit milan_datapath`` prints the
defines, include directories and sources the Yosys gate elaborates the
datapath with, the all-fabric shape's header directory among them, and the
census takes them from there, never from a list of its own. sv2v lowers the
SystemVerilog as it does in that gate, and Yosys reads what sv2v writes.

THE SHAPES are every shape the builder builds (#665, comment 6100024293).
``shapes()`` is the recipe's own (run.sh's row: the module's default
parameters, define ``SYNTHESIS``, the all-fabric header), then one per
``configs/*.yaml`` in name order, each taken from sw/builder alone:

  header      the configuration's generated directory
              ``configs/generated/<name>``, and its ``gen/``, in place of the
              recipe's header slot, as milan_soc.py's ``--entity-gen-dir``
              puts both ahead of the tracked include directories
              (scripts/check_entity_shape.py arm D holds the header to what
              the builder generates)
  parameters  ``endstation_builder.datapath_params()``: every integer
              parameter the build binds on milan_datapath (test_builder gate
              23m compares it with the Instance milan_soc.py builds for each
              configuration); the three ROM image paths, which only the
              processor and gPTP wrappers read, stay at their defaults
  defines     ``SYNTHESIS`` alone: milan_soc.py adds no define, and Vivado's
              synthesis defines that one, as run.sh's recipe does

A configuration added to configs/ is elaborated with no edit here.

THE ELABORATION keeps the hierarchy. Every module but the datapath is read as
a blackbox, so each instance stays a cell whose ports have a direction and no
body. The datapath alone is elaborated, read deferred and bound to the shape's
parameters by ``hierarchy -check -chparam`` (an unknown module or port
fails), and its processes become cells through the passes ``proc`` runs, in
its order. Two changes keep every read under the name the source gave it,
which is what the census keys a read by:

  ``insbuf``        turns every connection into a buffer cell before
                    proc_prune, before proc_dff and after the last pass;
                    those two passes otherwise rewrite a read to the name of
                    its net's driver
  no ``opt_expr``   proc's closing pass is not run: it folds away a read
                    that a constant of this shape masks, and the census keeps
                    every cell the elaborator produced

Yosys writes the result as JSON: every cell with its type, its ports'
directions and the bits each port connects, and every net's name. With no
connection left, each bit has exactly one name, and the census checks that.

ONE FORM IS REFUSED BEFORE ELABORATION. sv2v reads ``//`` or ``/*`` inside a
backslash-escaped name (IEEE 1800-2017 5.6.1) as a comment and can drop the
rest of the line, a read among it, without an error. No file the front end
can read (each source, and every file under an include directory or under a
source's own directory) may hold an escaped name containing either.

Anything else the front end or the elaborator refuses is the census's refusal
too: an undefined module, port or macro, a hierarchical reference (the
datapath sets ``default_nettype none``), or a form sv2v does not parse, such
as ``alias`` or an ``iff`` event qualifier.

THE TOOLS are the pinned ones. ``toolchain()`` refuses an sv2v or a Yosys
other than the versions .github/workflows/rtl-fast.yml installs (its
``YOSYS_VERSION`` and the release its sv2v step fetches), with a message
naming both pins and both versions found.
"""

from __future__ import annotations

import atexit
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from census_rules import live

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "sw/builder"))
import endstation_builder as eb  # noqa: E402

TOP = "milan_datapath"
RUN_SH = REPO / "syn/yosys/run.sh"
#: The workflow whose census job installs the pinned sv2v and Yosys.
WORKFLOW = REPO / ".github/workflows/rtl-fast.yml"
SV2V_STEP = "Install the pinned sv2v release"
#: Where the builder writes each configuration's generated header directory.
GENERATED = REPO / eb.GEN_CONFIG_DIR
#: The ROM images a blackbox read needs in its working directory: a module
#: without parameters is elaborated as it is read, $readmemh included.
ROMS = (("protocol-processor/hdl/acmp/rom/gen_ltn_rom.py", "ltn_rom.hex"),
        ("protocol-processor/hdl/aecp/ucode/gen_ucode.py", "ucode.hex"),
        ("gptp-processor/hdl/ucode/gen_gptp_ucode.py", "gptp_ucode.hex"))
#: proc's passes in the order ``proc`` runs them (Yosys ``help proc``), with
#: insbuf before each pass that maps a read to its net's driver, and without
#: proc's closing opt_expr.
PROC = ("insbuf", "proc_clean", "proc_rmdead", "proc_prune", "proc_init", "proc_arst", "proc_rom", "proc_mux",
        "proc_dlatch", "insbuf", "proc_dff", "proc_memwr", "proc_clean", "insbuf")
#: A backslash-escaped name holding a comment opener, which sv2v lexes as a comment.
ESCAPED_OPENER = re.compile(r"\\[!-~]*?(//|/\*)")
FRONT_END_SUFFIXES = frozenset({".sv", ".svh", ".v", ".vh"})
MODULE = re.compile(r"^module\s+(\\\S+|[A-Za-z_][\w$]*)", re.M)
END = re.compile(r"^endmodule\b[^\n]*\n?", re.M)
#: The directives sv2v writes between modules: the net type in force, and its reset to ``wire``.
DIRECTIVE = re.compile(r"^`(?:default_nettype\s+(\w+)|resetall)[ \t]*$", re.M)
#: A tool gets this long before its silence counts as a refusal.
TOOL_SECONDS = 900


class CensusError(Exception):
    """The census cannot read the datapath; the message says why."""


@dataclass(frozen=True)
class Recipe:
    """What CI's Yosys gate elaborates milan_datapath from."""

    defines: tuple[str, ...]
    incdirs: tuple[Path, ...]
    sources: tuple[Path, ...]


@dataclass(frozen=True)
class Shape:
    """One shape the datapath is elaborated in."""

    name: str                               # "recipe", or the configuration's name
    header: Path | None                     # its generated header directory; None keeps the recipe's
    params: tuple[tuple[str, int], ...]     # the datapath parameters it binds, by name

    def binds(self, param: str, least: int) -> bool:
        """Whether this shape binds param to least or more."""
        return dict(self.params).get(param, least - 1) >= least


#: run.sh's own row: the module's default parameters and the recipe's header.
RECIPE = Shape("recipe", None, ())


@functools.lru_cache(maxsize=1)
def recipe() -> Recipe:
    """The record ``syn/yosys/run.sh --emit milan_datapath`` prints, which is bash's own expansion of the gate's row."""
    out = run(["bash", str(RUN_SH), "--emit", TOP], REPO, "syn/yosys/run.sh --emit refused the recipe")
    rows = [line.split("=", 1) for line in out.splitlines() if "=" in line]
    pick = {k: [v for key, v in rows if key == k] for k in ("top", "define", "incdir", "src")}
    if pick["top"] != [TOP] or not pick["src"]:
        raise CensusError(f"syn/yosys/run.sh --emit {TOP} printed no recipe for {TOP}")
    return Recipe(tuple(pick["define"]), tuple(Path(d) for d in pick["incdir"]), tuple(Path(s) for s in pick["src"]))


def shapes() -> tuple[Shape, ...]:
    """The recipe's shape, then one per configs/*.yaml in name order: the builder's
    generated header directory for it and the parameters the builder states."""
    out = [RECIPE]
    for path in sorted((REPO / "configs").glob("*.yaml")) if live("shapes") else ():
        try:
            cfg = eb.load_config(str(path))
            params = eb.datapath_params(cfg)
        except (eb.ConfigError, OSError, KeyError, ValueError) as exc:
            raise CensusError(f"the builder cannot state the shape of {rel(path)}: {exc}") from exc
        out.append(Shape(cfg["name"], GENERATED / cfg["name"], tuple(sorted(params.items()))))
    return tuple(out)


def shaped(rcp: Recipe, shape: Shape) -> Recipe:
    """rcp with the shape's header directory, then its gen/, in place of the recipe's
    header slot (the one include directory under configs/generated)."""
    if shape.header is None or not live("shape-header"):
        return rcp
    slot = [d for d in rcp.incdirs if Path(d).resolve().parent == GENERATED.resolve()]
    if len(slot) != 1:
        raise CensusError(f"the recipe has {len(slot)} include directories under {rel(GENERATED)}, not the one "
                          f"header slot a shape replaces")
    want = {p.relative_to(slot[0]) for p in Path(slot[0]).rglob("*") if p.is_file()}
    have = {p.relative_to(shape.header) for p in shape.header.rglob("*") if p.is_file()}
    if want - have:
        raise CensusError(f"{rel(shape.header)} lacks {', '.join(sorted(map(str, want - have)))}: run the builder "
                          f"for {shape.name}, or the front end reads another shape's header")
    at = rcp.incdirs.index(slot[0])
    return Recipe(rcp.defines, (*rcp.incdirs[:at], shape.header, shape.header / "gen", *rcp.incdirs[at + 1:]),
                  rcp.sources)


def tool(name: str) -> str:
    """The sv2v or yosys to run: $SV2V or $YOSYS when set, else the one on PATH."""
    path = os.environ.get(name.upper()) or shutil.which(name)
    if not path:
        raise CensusError(f"missing tool: {name}; the census elaborates with the sv2v and Yosys "
                          f"{rel(WORKFLOW)} pins")
    return path


@functools.lru_cache(maxsize=1)
def pins() -> tuple[str, str]:
    """(sv2v, Yosys) as rtl-fast.yml pins them: the release its sv2v steps fetch, and its YOSYS_VERSION."""
    try:
        doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CensusError(f"cannot read the pins from {rel(WORKFLOW)}: {exc}") from exc
    sv2v = {v for job in doc.get("jobs", {}).values() for step in job.get("steps", ())
            if step.get("name") == SV2V_STEP for v in re.findall(r"^ver=(\S+)$", step.get("run", ""), re.M)}
    yosys = str(doc.get("env", {}).get("YOSYS_VERSION", ""))
    if len(sv2v) != 1 or not yosys:
        raise CensusError(f"{rel(WORKFLOW)} pins sv2v {sorted(sv2v) or 'nowhere'} and Yosys {yosys or 'nowhere'}; "
                          f"the census needs one of each")
    return sv2v.pop(), yosys


def run(argv: list[str], cwd: Path, what: str) -> str:
    """argv's standard output; a CensusError saying ``what refused it`` with the tool's
    own words (Yosys's ERROR line, else the first line sv2v or a generator printed)."""
    try:
        done = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=TOOL_SECONDS, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CensusError(f"{what} did not run: {exc}") from exc
    if done.returncode:
        why = re.search(r"ERROR:[^\n]*", done.stdout + done.stderr) or re.search(r"\S[^\n]*", done.stderr + done.stdout)
        raise CensusError(f"{what}: {' '.join(why.group().split()) if why else f'exit {done.returncode}'}")
    return done.stdout


def toolchain() -> str:
    """The sv2v and Yosys versions the census elaborates with; a CensusError for any but the pinned ones."""
    sv2v = run([tool("sv2v"), "--version"], REPO, "sv2v --version").strip()
    yosys = run([tool("yosys"), "-V"], REPO, "yosys -V").split("(")[0].strip()
    want_sv2v, want_yosys = pins()
    if live("pins") and (sv2v.split()[-1:] != [want_sv2v] or yosys.split()[1:2] != [want_yosys.lstrip("v")]):
        raise CensusError(f"the census elaborates with the pinned sv2v {want_sv2v} and Yosys {want_yosys} "
                          f"({rel(WORKFLOW)}), not `{sv2v}` and `{yosys}`: set SV2V and YOSYS to the pinned tools")
    return f"{sv2v}, {yosys}"


def front_end_files(rcp: Recipe) -> set[Path]:
    """Every file sv2v can read for the datapath: each source, and every file under an
    include directory or under a source's own directory (sv2v searches that first)."""
    out = {p.resolve() for p in rcp.sources}
    for root in {*rcp.incdirs, *(p.parent for p in rcp.sources)}:
        out |= {p.resolve() for p in Path(root).rglob("*") if p.suffix in FRONT_END_SUFFIXES and p.is_file()}
    return out


@functools.lru_cache(maxsize=8)
def tracked_openers(rcp: Recipe | None = None) -> dict[Path, tuple[int, str]]:
    """Each file the front end can read for rcp (the recipe's shape when None, as the
    reviewers' probes call it), as tracked, that holds an escaped name with a comment
    opener: its first such line and name."""
    out = {}
    for path in sorted(front_end_files(rcp or recipe())):
        hit = opener(path.read_text(encoding="utf-8", errors="replace"))
        if hit:
            out[path] = hit
    return out


def opener(text: str) -> tuple[int, str] | None:
    """(line, name) of the first escaped name in text holding // or /*, or None."""
    m = ESCAPED_OPENER.search(text)
    return (text.count("\n", 0, m.start()) + 1, m.group()) if m else None


def guard(overlay: dict[Path, str], rcp: Recipe) -> None:
    """Refuse an escaped name holding // or /* in any file the front end can read, planted copies included."""
    hits = {p: h for p, h in tracked_openers(rcp).items() if p not in overlay}
    hits |= {p: h for p, h in ((p, opener(t)) for p, t in overlay.items()) if h}
    if hits:
        path, (line, name) = min(hits.items())
        raise CensusError(f"{rel(path)}:{line}: an escaped name holds a comment opener, `{name}`; the front "
                          f"end (sv2v) reads the rest of its line as a comment, a read among it")


def rel(path: Path) -> str:
    """path relative to the checkout when it lies inside it."""
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


@dataclass(frozen=True)
class Cell:
    """One cell of the elaborated datapath."""

    kind: str                             # a Yosys internal type ($and, $_BUF_, ...) or a module name
    dirs: dict[str, str]                  # port -> input, output or inout
    conns: dict[str, tuple]               # port -> its bits (an int per net bit, a str per constant bit)
    memid: str                            # the memory a $mem* cell reads or writes, or ""


@dataclass
class Netlist:
    """The elaborated datapath: its cells, its nets' names, and its ports."""

    cells: dict[str, Cell]
    names: dict[str, tuple]               # net name -> its bits
    hidden: frozenset[str]                # the names Yosys made: each holds a `$` (a function's locals too)
    ports: dict[str, tuple[str, tuple]]   # port -> (direction, bits)
    modules: dict[str, dict[str, str]]    # each blackbox module -> {port: direction}
    bit_name: dict[int, tuple[str, int]] = field(default_factory=dict)


def netlist(doc: dict) -> Netlist:
    """The Netlist of Yosys's JSON; a CensusError when a bit has two names or none."""
    top = doc["modules"].get(TOP)
    if top is None:
        raise CensusError(f"the elaborated design holds no module {TOP}")
    cells = {}
    for name, c in top["cells"].items():
        memid = str(c.get("parameters", {}).get("MEMID", ""))
        cells[name] = Cell(c["type"], dict(c.get("port_directions", {})),
                           {p: tuple(b) for p, b in c["connections"].items()}, memid)
    names = {n: tuple(v["bits"]) for n, v in top["netnames"].items()}
    hidden = frozenset(n for n, v in top["netnames"].items() if v.get("hide_name") or "$" in n)
    ports = {p: (v["direction"], tuple(v["bits"])) for p, v in top["ports"].items()}
    modules = {m: {p: v["direction"] for p, v in d.get("ports", {}).items()}
               for m, d in doc["modules"].items() if m != TOP}
    net = Netlist(cells, names, hidden, ports, modules)
    for n, bits in names.items():
        for i, b in enumerate(bits):
            if isinstance(b, int):
                if b in net.bit_name:
                    raise CensusError(f"the netlist names one net {net.bit_name[b][0]} and {n}: a connection "
                                      f"was left after the last insbuf")
                net.bit_name[b] = (n, i)
    used = {b for c in cells.values() for bits in c.conns.values() for b in bits if isinstance(b, int)}
    used |= {b for _, bits in ports.values() for b in bits if isinstance(b, int)}
    if used - set(net.bit_name):
        raise CensusError(f"the netlist connects {len(used - set(net.bit_name))} bit(s) no net names")
    return net


class Work:
    """The census's scratch: one directory, each blackbox library Yosys read once, the ROM images."""

    def __init__(self) -> None:
        self.root: Path | None = None
        # sha256 of a library's text -> its RTLIL and its modules (one per shape's header, and per changed module)
        self.libs: dict[str, tuple[Path, dict[str, str]]] = {}

    def path(self) -> Path:
        """The scratch directory, made on first use and removed at exit by the process that made it."""
        if self.root is None:
            self.root = Path(tempfile.mkdtemp(prefix="publication-census-"))
            atexit.register(remove, os.getpid(), self.root)
        return self.root

    def roms(self) -> None:
        """Generate the ROM images into the scratch directory once."""
        for gen, image in ROMS:
            target = self.path() / image
            if not target.exists():
                run([sys.executable, str(REPO / gen), "-o", str(target)], self.path(),
                    f"the ROM generator {gen} failed")
                if not target.stat().st_size:
                    raise CensusError(f"{gen} wrote an empty {image}")


def remove(pid: int, path: Path) -> None:
    """Remove path, only from the process that made it (a forked self-test worker leaves it)."""
    if os.getpid() == pid:
        shutil.rmtree(path, ignore_errors=True)


WORK = Work()


def split(text: str) -> tuple[str, dict[str, str]]:
    """sv2v's output cut into the datapath's module and every other module, each
    under the ``default_nettype`` in force where it starts (``resetall`` resets it
    to ``wire``); any other text outside a module is refused."""
    mods, at, nettype, outside = {}, 0, "wire", []
    for m in MODULE.finditer(text):
        between = text[at:m.start()]
        for d in DIRECTIVE.finditer(between):
            nettype = d.group(1) or "wire"
        outside.append(DIRECTIVE.sub("", between))
        e = END.search(text, m.end())
        if not e or m.group(1) in mods:
            raise CensusError(f"sv2v's output holds module {m.group(1)} unclosed or twice")
        mods[m.group(1)] = f"`default_nettype {nettype}\n" + text[m.start():e.end()]
        at = e.end()
    outside.append(DIRECTIVE.sub("", text[at:]))
    if "".join(outside).strip():
        raise CensusError(f"sv2v wrote text outside any module: `{' '.join(''.join(outside).split())[:120]}`")
    if TOP not in mods:
        raise CensusError(f"sv2v's output holds no module {TOP}")
    return mods.pop(TOP), mods


def shadow(rcp: Recipe, overlay: dict[Path, str], tree: Path) -> list[str]:
    """sv2v's arguments over a shadow of every file the front end can read: a link
    to each tracked file, a planted text written in its place. sv2v then reads a
    planted file wherever it would read the tracked one, from its own directory
    or from an include directory alike."""
    files = front_end_files(rcp)
    if set(overlay) - files:
        raise CensusError(f"cannot plant {', '.join(sorted(map(rel, set(overlay) - files)))}: the front end "
                          f"does not read it")
    if any(not f.is_relative_to(REPO) for f in files) or any(not Path(d).resolve().is_relative_to(REPO)
                                                             for d in rcp.incdirs):
        raise CensusError("a file or include directory the front end reads lies outside the checkout")
    for f in files:
        target = tree / f.relative_to(REPO)
        target.parent.mkdir(parents=True, exist_ok=True)
        if f in overlay:
            target.write_text(overlay[f], encoding="utf-8")
        else:
            target.symlink_to(f)
    incdirs = [tree / Path(d).resolve().relative_to(REPO) for d in rcp.incdirs]
    for d in incdirs:
        d.mkdir(parents=True, exist_ok=True)
    return [tool("sv2v"), f"--top={TOP}", *(f"-D{d}" for d in rcp.defines),
            *(a for d in incdirs for a in ("-I", str(d))),
            *(str(tree / Path(s).resolve().relative_to(REPO)) for s in rcp.sources)]


def library(mods: dict[str, str], arm: Path) -> list[str]:
    """The Yosys commands that read every module but the datapath as a blackbox:
    the RTLIL of a library already read whose every module is unchanged (plus
    any module a plant adds), else the whole library afresh."""
    for lib, base in WORK.libs.values():
        if all(mods.get(n) == t for n, t in base.items()):
            extra = {n: t for n, t in mods.items() if n not in base}
            if not extra:
                return [f"read_rtlil {lib}"]
            (arm / "extra.v").write_text("".join(extra.values()), encoding="utf-8")
            return [f"read_rtlil {lib}", f"read_verilog -lib {arm / 'extra.v'}"]
    key = digest(mods)
    WORK.roms()
    (arm / "lib.v").write_text("".join(mods.values()), encoding="utf-8")
    # per process: two workers of one pool may read the same library at once
    lib = WORK.path() / f"lib-{key[:16]}-{os.getpid()}.il"
    run([tool("yosys"), "-q", "-p", f"read_verilog -lib {arm / 'lib.v'}; write_rtlil {lib}"], WORK.path(),
        "the elaborator (Yosys) refused the other modules as blackboxes")
    WORK.libs[key] = (lib, dict(mods))
    return [f"read_rtlil {lib}"]


def digest(mods: dict[str, str]) -> str:
    """The sha256 of a library's modules, in name order."""
    h = hashlib.sha256()
    for name in sorted(mods):
        h.update(name.encode() + b"\0" + mods[name].encode() + b"\0")
    return h.hexdigest()


def elaborate(overlay: dict[Path, str], shape: Shape = RECIPE) -> Netlist:
    """The datapath elaborated from the recipe in shape, overlay's texts (absolute
    path -> text) in place of the files they name; a CensusError if any step
    refuses, its paths named as in the checkout."""
    rcp = shaped(recipe(), shape)
    overlay = {Path(p).resolve(): t for p, t in overlay.items()}
    if live("opener-guard"):
        guard(overlay, rcp)
    arm = Path(tempfile.mkdtemp(prefix="arm-", dir=WORK.path()))
    try:
        argv = shadow(rcp, overlay, arm / "tree")
        top, mods = split(run(argv, arm, "the front end (sv2v) refused the datapath"))
        script = library(mods, arm)
        (arm / "top.v").write_text(top, encoding="utf-8")
        bind = "".join(f" -chparam {k} {v}" for k, v in shape.params) if live("shape-params") else ""
        # deferred, so the module is elaborated once, at the shape's parameters;
        # hierarchy names a bound top $paramod$..., and rename gives it its name back
        script += [f"read_verilog -defer {arm / 'top.v'}", f"hierarchy -check -top {TOP}{bind}", f"rename -top {TOP}",
                   *(PROC if live("keep-names") else ("proc",)), f"write_json {arm / 'net.json'}"]
        run([tool("yosys"), "-q", "-p", "; ".join(script)], WORK.path(), "the elaborator (Yosys) refused the datapath")
        with (arm / "net.json").open(encoding="utf-8") as handle:
            return netlist(json.load(handle))
    except CensusError as exc:
        raise CensusError(str(exc).replace(f"{arm / 'tree'}/", "").replace(f"{arm}/", "")) from exc
    finally:
        shutil.rmtree(arm, ignore_errors=True)
