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

THE ELABORATION keeps the hierarchy. Every module but the datapath is read as
a blackbox, so each instance stays a cell whose ports have a direction and no
body. The datapath alone is elaborated, by ``hierarchy -check`` (an unknown
module or port fails), and its processes become cells through the passes
``proc`` runs, in its order. Two changes keep every read under the name the
source gave it, which is what the census keys a read by:

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

REPO = Path(__file__).resolve().parent.parent.parent
TOP = "milan_datapath"
RUN_SH = REPO / "syn/yosys/run.sh"
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


@functools.lru_cache(maxsize=1)
def recipe() -> Recipe:
    """The record ``syn/yosys/run.sh --emit milan_datapath`` prints, which is bash's own expansion of the gate's row."""
    out = run(["bash", str(RUN_SH), "--emit", TOP], REPO, "syn/yosys/run.sh --emit refused the recipe")
    rows = [line.split("=", 1) for line in out.splitlines() if "=" in line]
    pick = {k: [v for key, v in rows if key == k] for k in ("top", "define", "incdir", "src")}
    if pick["top"] != [TOP] or not pick["src"]:
        raise CensusError(f"syn/yosys/run.sh --emit {TOP} printed no recipe for {TOP}")
    return Recipe(tuple(pick["define"]), tuple(Path(d) for d in pick["incdir"]), tuple(Path(s) for s in pick["src"]))


def tool(name: str) -> str:
    """The sv2v or yosys to run: $SV2V or $YOSYS when set, else the one on PATH."""
    path = os.environ.get(name.upper()) or shutil.which(name)
    if not path:
        raise CensusError(f"missing tool: {name}; the census elaborates with the sv2v and Yosys "
                          f"syn/yosys/README.md pins")
    return path


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
    """The sv2v and Yosys versions the census elaborated with."""
    sv2v = run([tool("sv2v"), "--version"], REPO, "sv2v --version").strip()
    yosys = run([tool("yosys"), "-V"], REPO, "yosys -V").split("(")[0].strip()
    return f"{sv2v}, {yosys}"


def front_end_files(rcp: Recipe) -> set[Path]:
    """Every file sv2v can read for the datapath: each source, and every file under an
    include directory or under a source's own directory (sv2v searches that first)."""
    out = {p.resolve() for p in rcp.sources}
    for root in {*rcp.incdirs, *(p.parent for p in rcp.sources)}:
        out |= {p.resolve() for p in Path(root).rglob("*") if p.suffix in FRONT_END_SUFFIXES and p.is_file()}
    return out


@functools.lru_cache(maxsize=1)
def tracked_openers() -> dict[Path, tuple[int, str]]:
    """Each file the front end can read, as tracked, that holds an escaped name with a
    comment opener: its first such line and name."""
    out = {}
    for path in sorted(front_end_files(recipe())):
        hit = opener(path.read_text(encoding="utf-8", errors="replace"))
        if hit:
            out[path] = hit
    return out


def opener(text: str) -> tuple[int, str] | None:
    """(line, name) of the first escaped name in text holding // or /*, or None."""
    m = ESCAPED_OPENER.search(text)
    return (text.count("\n", 0, m.start()) + 1, m.group()) if m else None


def guard(overlay: dict[Path, str]) -> None:
    """Refuse an escaped name holding // or /* in any file the front end can read, planted copies included."""
    hits = {p: h for p, h in tracked_openers().items() if p not in overlay}
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
    """The census's scratch: one directory, the blackbox library Yosys read once, the ROM images."""

    def __init__(self) -> None:
        self.root: Path | None = None
        self.libs: dict[str, Path] = {}          # sha256 of the library's text -> its RTLIL
        self.baseline: dict[str, str] = {}       # the tracked sources' library modules

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
    the RTLIL of the tracked library when every module of it is unchanged (plus
    any module a plant adds), else the whole library afresh."""
    if WORK.baseline and all(mods.get(n) == t for n, t in WORK.baseline.items()):
        lib = WORK.libs[digest(WORK.baseline)]
        extra = {n: t for n, t in mods.items() if n not in WORK.baseline}
        if not extra:
            return [f"read_rtlil {lib}"]
        (arm / "extra.v").write_text("".join(extra.values()), encoding="utf-8")
        return [f"read_rtlil {lib}", f"read_verilog -lib {arm / 'extra.v'}"]
    key = digest(mods)
    if key not in WORK.libs:
        WORK.roms()
        (arm / "lib.v").write_text("".join(mods.values()), encoding="utf-8")
        lib = WORK.path() / f"lib-{key[:16]}.il"
        run([tool("yosys"), "-q", "-p", f"read_verilog -lib {arm / 'lib.v'}; write_rtlil {lib}"], WORK.path(),
            "the elaborator (Yosys) refused the other modules as blackboxes")
        WORK.libs[key] = lib
        if not WORK.baseline:
            WORK.baseline = dict(mods)
    return [f"read_rtlil {WORK.libs[key]}"]


def digest(mods: dict[str, str]) -> str:
    """The sha256 of a library's modules, in name order."""
    h = hashlib.sha256()
    for name in sorted(mods):
        h.update(name.encode() + b"\0" + mods[name].encode() + b"\0")
    return h.hexdigest()


def elaborate(overlay: dict[Path, str]) -> Netlist:
    """The datapath elaborated from the recipe, overlay's texts (absolute path ->
    text) in place of the files they name; a CensusError if any step refuses,
    its paths named as in the checkout."""
    rcp = recipe()
    overlay = {Path(p).resolve(): t for p, t in overlay.items()}
    guard(overlay)
    arm = Path(tempfile.mkdtemp(prefix="arm-", dir=WORK.path()))
    try:
        argv = shadow(rcp, overlay, arm / "tree")
        top, mods = split(run(argv, arm, "the front end (sv2v) refused the datapath"))
        script = library(mods, arm)
        (arm / "top.v").write_text(top, encoding="utf-8")
        script += [f"read_verilog {arm / 'top.v'}", f"hierarchy -check -top {TOP}", *PROC,
                   f"write_json {arm / 'net.json'}"]
        run([tool("yosys"), "-q", "-p", "; ".join(script)], WORK.path(), "the elaborator (Yosys) refused the datapath")
        with (arm / "net.json").open(encoding="utf-8") as handle:
            return netlist(json.load(handle))
    except CensusError as exc:
        raise CensusError(str(exc).replace(f"{arm / 'tree'}/", "").replace(f"{arm}/", "")) from exc
    finally:
        shutil.rmtree(arm, ignore_errors=True)
