#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: every module `milan_datapath` instantiates must be registered as a
Vivado source in `sw/litex/milan_soc.py`.

Why this exists. There are THREE independent file lists in this repo:

  * each `tb/verilator/<suite>/Makefile`  -> what Verilator compiles
  * `syn/yosys/run.sh`'s `tops=()` array  -> what Yosys synthesises
  * `milan_soc.py`'s curated source list  -> what VIVADO is given

A new module can be added, get a Verilator suite, get a Yosys top, pass every
gate in CI - and still be missing from the Vivado list. Nothing catches it,
because nothing in CI runs Vivado. It surfaces only as

    ERROR: [Synth 8-439] module 'X' not found

~40 minutes into a bitstream build, which is exactly when it is most expensive.
That happened on 2026-07-27 with `KL_i2s_feed_mux`: it had a suite, a Yosys
top, and 55/55 green - and three parallel Vivado runs all died on it.

This gate closes the gap in under a second, with no toolchain at all.

WHAT IT MEASURES, AND HOW IT READS. Both sides of the comparison are read the
way the tools that consume them read them, because the first version read
both as text and missed a real defect on each side:

  * The RTL side is `instantiations()`: every instantiation shape the front
    ends accept - at ANY indentation (the tree has one at column 0,
    `traffic_class_map` in `traffic_classifier.sv`, and a regex that needed
    two leading spaces walked past it), tab-indented, `X #(` with or without
    the space, and an arrayed instance `X u [1:0] (`. Comments are blanked
    first, so a commented-out instantiation is not one. Every
    `include`d body is spliced in the way the preprocessor does, so an
    instantiation living in a header is seen. This first hop is what
    `scripts/check_rtl_source_lists.py` imports and walks transitively; a
    hole here is a hole in the whole closure, which is why it lives here once.
  * The Vivado side is `vivado_sources()`: the `_MILAN_DATAPATH_SOURCES`
    literal and the source-path strings registered beside it, read through
    `ast` - the tree Python evaluates, in which a comment does not exist. A
    regex over the file's text counted a commented-out row as a registered
    source; three files left the list that way with this gate green.

Usage:
    python3 scripts/check_soc_sources.py             # gate (exit 1 on a miss)
    python3 scripts/check_soc_sources.py --list      # show the resolved sets
    python3 scripts/check_soc_sources.py --selftest  # fixture arms

Exit 0 = every instantiated module is registered and every registered file
         exists. Exit 1 = a finding. Exit 2 = a side could not be read.
"""
import ast
import re
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATAPATH = REPO / "hdl/milan/milan_datapath.sv"
SOC = REPO / "sw/litex/milan_soc.py"
#: the list literal in milan_soc.py that `add_source` walks
SOC_LIST = "_MILAN_DATAPATH_SOURCES"

#: Trees a source list may legitimately draw from, and where a `include is
#: looked up. The vendored AXI-stream RTL is here because every consumer must
#: carry it too. check_rtl_source_lists.py imports this rather than keeping a
#: second copy.
SEARCH_ROOTS = ("hdl", "protocol-processor/hdl", "gptp-processor/hdl",
                "third_party/verilog-axis/rtl")

#: instantiation names we care about - project RTL, not language keywords or
#: generate-block labels. Anything matching a project prefix must be a real
#: module we own, so a typo in a prefix fails loudly rather than silently
#: shrinking the checked set.
PREFIXES = ("KL_", "avtp_", "adp_", "acmp_", "aaf_", "traffic_", "ptp_",
            "cdc_", "tcam", "rx_", "tx_", "axis_", "timestamp_",
            "ethernet_", "event_", "milan_")

#: The instantiation shapes a front end accepts: `X #(`, `X u (`, `X u [N:0] (`
#: at ANY indentation. Keywords that share the shape (`else if (`, `module X (`)
#: are matched too and discarded by the callers, which only keep names a
#: source declares or a project prefix claims; a shape the regex does not see
#: is a module no consumer is told about, so the net is wide on purpose.
INST_RE = re.compile(
    r"^[ \t]*([A-Za-z_]\w*)"                         # the module, any indent
    r"(?:\s*#\s*\("                                   # `X #(`  (space optional)
    r"|\s+[A-Za-z_]\w*\s*(?:\[[^\]]*\]\s*)*\()",      # `X u (`, `X u [1:0] (`
    re.M)
INCLUDE_RE = re.compile(r'^[ \t]*`include\s+"([^"]+)"', re.M)
_COMMENT_OR_STRING_RE = re.compile(
    r'"(?:\\.|[^"\\\n])*"|//[^\n]*|/\*.*?\*/', re.S)
#: a whole string that is a repository-relative source path
_SOURCE_PATH_RE = re.compile(r"^(?:[\w.-]+/)+[\w.-]+\.(?:sv|v)$")


def strip_comments(text):
    """Blank every comment, keeping the line structure so line-anchored
    patterns still see the same lines. String literals are stepped over, not
    blanked: a `//` inside one is not a comment, and an `include names its
    file in one."""
    def blank(match):
        token = match.group(0)
        if token.startswith('"'):
            return token
        return re.sub(r"[^\n]", " ", token)
    return _COMMENT_OR_STRING_RE.sub(blank, text)


@lru_cache(maxsize=None)
def _under_roots(name):
    """The first file under SEARCH_ROOTS whose path ends with `name`, so an
    include with a directory part (`gen/x.svh`) finds a `gen/` directory."""
    for root in SEARCH_ROOTS:
        base = REPO / root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob(Path(name).name)):
            if path.is_file() and path.as_posix().endswith("/" + name):
                return path
    return None


def resolve_include(name, includer):
    """The file `include "name"` opens: beside the includer first, then the
    search roots. None when no file answers."""
    beside = includer.parent / name
    if beside.is_file():
        return beside
    return _under_roots(name)


def spliced(path, _seen=None):
    """(text, included, unresolved): the unit's text as the front end sees it.

    Every `include body is spliced in at its line, recursively, each file at
    most once (a guarded header including itself ends); comments and strings
    are blanked. `included` lists the files spliced, `unresolved` the include
    names no file answered to - the caller decides what that means.
    """
    seen = set() if _seen is None else _seen
    seen.add(path.resolve())
    included, unresolved = [], []

    def splice(match):
        name = match.group(1)
        target = resolve_include(name, path)
        if target is None:
            unresolved.append(name)
            return ""
        if target.resolve() in seen:
            return ""
        included.append(target)
        body, inc, bad = spliced(target, seen)
        included.extend(inc)
        unresolved.extend(bad)
        return body

    text = INCLUDE_RE.sub(splice, strip_comments(path.read_text(errors="replace")))
    return text, included, unresolved


def instantiations(path):
    """Module names instantiated by the unit in `path` - includes followed,
    comments ignored. The FIRST HOP; check_rtl_source_lists.py walks it."""
    text, _included, _unresolved = spliced(Path(path))
    return set(INST_RE.findall(text))


def instantiated(datapath=DATAPATH):
    return {m for m in instantiations(datapath) if m.startswith(PREFIXES)}


def vivado_sources(soc=SOC):
    """(paths, derived, why): the source paths milan_soc.py registers, read the
    way Python reads the file.

    `paths` are the string constants that are repository-relative source
    paths: the rows of the `_MILAN_DATAPATH_SOURCES` literal and source paths
    returned by its derived helper calls.
    A comment is not in the tree Python evaluates, so a commented-out row is
    not a row. `derived` names the starred calls inside the literal
    (`*_pp_sources()`); their expansion belongs to the caller. `why` is set,
    and the others None, when the file or the list cannot be read.
    """
    soc = Path(soc)
    try:
        tree = ast.parse(soc.read_text(), filename=str(soc))
    except (OSError, SyntaxError) as exc:
        return None, None, f"{soc.name}: {exc}"
    literal = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == SOC_LIST for t in node.targets):
            literal = node.value
    if not isinstance(literal, ast.List):
        return None, None, f"{soc.name}: no `{SOC_LIST} = [...]` list literal"
    derived = []
    for elt in literal.elts:
        if isinstance(elt, ast.Starred) and isinstance(elt.value, ast.Call):
            derived.append(ast.unparse(elt.value.func))
        elif not (isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                  and _SOURCE_PATH_RE.match(elt.value)):
            return None, None, (f"{soc.name}:{elt.lineno}: {SOC_LIST} holds an "
                                f"entry that is neither a source path nor a "
                                f"derived expansion")
    paths = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and _SOURCE_PATH_RE.match(node.value) and node.value not in paths):
            paths.append(node.value)
    return paths, derived, None


def registered(soc=SOC):
    """({module-name-by-stem: path}, None), or (None, why)."""
    paths, _derived, why = vivado_sources(soc)
    if paths is None:
        return None, why
    return {Path(p).stem: p for p in paths}, None


def audit(datapath=DATAPATH, soc=SOC):
    """(inst, reg, missing, gone, why) - the whole comparison, injectable so
    the self-test grades copies rather than editing the tree."""
    inst = instantiated(datapath)
    reg, why = registered(soc)
    if reg is None:
        return inst, {}, [], [], why
    missing = sorted(inst - set(reg))
    # A source file that no longer exists is the mirror-image defect: Vivado
    # would fail on a missing file rather than a missing module.
    gone = sorted(p for p in reg.values() if not (REPO / p).is_file())
    return inst, reg, missing, gone, None


def selftest():
    """Fixture arms, each known by construction and each red when the defect
    it guards is put back (the two-space regex, the text-regex list reader)."""
    failures = checks = 0

    def ck(name, ok, detail=""):
        nonlocal failures, checks
        checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        # 1. the instantiation shapes the front ends accept, and the lines
        #    that share the shape without being one
        (d / "shapes.sv").write_text(
            "module KL_top #(parameter W = 1) (\n  input logic clk\n);\n"
            "  KL_two u_two (.clk(clk));\n"
            "KL_col0 u_col0 (.clk(clk));\n"
            "\tKL_tab u_tab (.clk(clk));\n"
            "  KL_param #(.W(W)) u_p (.clk(clk));\n"
            "  KL_tight#(.W(W)) u_t (.clk(clk));\n"
            "  KL_arr u_arr [1:0] (.clk(clk));\n"
            "  KL_arr2 u_arr2[3:0](.clk(clk));\n"
            "  KL_split\n    #(.W(W)) u_s (.clk(clk));\n"
            "  // KL_ghost u_g (.clk(clk));\n"
            "  /* KL_ghost2 u_g2 (.clk(clk)); */\n"
            "  /*\n  KL_ghost3 u_g3 (.clk(clk));\n  */\n"
            "  assign x = KL_func(clk);\n"
            "  KL_task(clk);\n"
            "  initial $display(\"KL_str u_s (\");\n"
            "endmodule\n")
        got = instantiations(d / "shapes.sv")
        ck("a two-space instantiation is seen", "KL_two" in got, f"got {sorted(got)}")
        ck("a column-0 instantiation is seen", "KL_col0" in got, f"got {sorted(got)}")
        ck("a tab-indented instantiation is seen", "KL_tab" in got, f"got {sorted(got)}")
        ck("a parameterised instantiation is seen with or without the space before #",
           {"KL_param", "KL_tight"} <= got, f"got {sorted(got)}")
        ck("an arrayed instance is seen", {"KL_arr", "KL_arr2"} <= got, f"got {sorted(got)}")
        ck("an instantiation whose #( starts on the next line is seen", "KL_split" in got,
           f"got {sorted(got)}")
        ck("a commented-out instantiation is not one",
           not {"KL_ghost", "KL_ghost2", "KL_ghost3"} & got, f"got {sorted(got)}")
        ck("a function call, a task call and a string are not instantiations",
           not {"KL_func", "KL_task", "KL_str", "KL_top"} & got, f"got {sorted(got)}")

        # 2. `include: the body is part of the unit, recursively, once
        (d / "gen").mkdir()
        (d / "top.sv").write_text(
            "module KL_t;\n`include \"body.svh\"\n`include \"gen/shape.svh\"\n"
            "`include \"missing.svh\"\nendmodule\n")
        (d / "body.svh").write_text(
            "`include \"nested.svh\"\nKL_inc u_inc (.a(a));\n")
        (d / "nested.svh").write_text(
            "`include \"body.svh\"\n  KL_nested u_n (.a(a));\n")
        (d / "gen" / "shape.svh").write_text("  KL_gen u_g (.a(a));\n")
        got = instantiations(d / "top.sv")
        _text, included, unresolved = spliced(d / "top.sv")
        ck("an instantiation inside an included body is seen", "KL_inc" in got,
           f"got {sorted(got)}")
        ck("a nested include is followed and a header including itself ends",
           "KL_nested" in got and len(included) == 3,
           f"got {sorted(got)}, spliced {[p.name for p in included]}")
        ck("an include with a directory part resolves beside the includer",
           "KL_gen" in got, f"got {sorted(got)}")
        ck("an include no file answers to is reported by name",
           unresolved == ["missing.svh"], f"got {unresolved}")
        ck("a header under the search roots resolves from anywhere",
           resolve_include("gen/adp_shape_defaults.svh", d / "top.sv") is not None
           and resolve_include("ethernet_events.svh", d / "top.sv") is not None)

        # 3. the Vivado list is read as Python reads it
        (d / "soc.py").write_text(
            '"""Not a list: hdl/a/KL_doc.sv is prose."""\n'
            "def _pp_sources():\n    return []\n"
            f"{SOC_LIST} = [\n"
            "    *_pp_sources(),\n"
            '    "hdl/a/KL_live.sv",  # "hdl/a/KL_trailing.sv"\n'
            '    # "hdl/a/KL_dead.sv",\n'
            '    "third_party/verilog-axis/rtl/axis_fifo.v",\n'
            "]\n"
            "def add(platform, cond):\n"
            f"    srcs = list({SOC_LIST})\n"
            "    if cond:\n"
            '        srcs.append("hdl/a/KL_cond.sv")\n'
            '    print("see hdl/a/KL_msg.sv for details")\n'
            "    return srcs\n")
        paths, derived, why = vivado_sources(d / "soc.py")
        ck("a live row is a row", paths is not None and "hdl/a/KL_live.sv" in paths, f"{paths} {why}")
        ck("a commented-out row is not a row",
           paths is not None and "hdl/a/KL_dead.sv" not in paths, f"{paths}")
        ck("a path in a trailing comment or a docstring is not a row",
           paths is not None and not {"hdl/a/KL_trailing.sv", "hdl/a/KL_doc.sv"} & set(paths),
           f"{paths}")
        ck("a conditional registration beside the list is read",
           paths is not None and "hdl/a/KL_cond.sv" in paths, f"{paths}")
        ck("a path inside a message string is not a registration",
           paths is not None and not any("KL_msg" in p for p in paths), f"{paths}")
        ck("the derived half is reported as the starred call, not guessed from syntax",
           derived == ["_pp_sources"], f"{derived}")
        ck("a vendored .v entry counts as a source", paths is not None
           and "third_party/verilog-axis/rtl/axis_fifo.v" in paths, f"{paths}")
        (d / "nolist.py").write_text("x = 1\n")
        ck("a file without the list is refused, not read as empty",
           vivado_sources(d / "nolist.py")[0] is None)
        (d / "badrow.py").write_text(f"{SOC_LIST} = ['hdl/a/b.sv', 42]\n")
        ck("a row that is neither a path nor a derived expansion is refused",
           vivado_sources(d / "badrow.py")[0] is None)

        # 4. the live tree, then the two mutations the round-2 review ran
        inst, reg, missing, gone, why = audit()
        ck("the live datapath's first hop is registered and present",
           why is None and not missing and not gone and len(inst) >= 30,
           f"missing {missing} gone {gone} why {why} ({len(inst)} modules)")
        soc_text = SOC.read_text()
        row = next((l for l in soc_text.splitlines()
                    if '"hdl/common/cdc_pulse.sv"' in l), None)
        mutated = soc_text.replace(row, "#" + row, 1) if row else soc_text
        (d / "milan_soc.py").write_text(mutated)
        _i, _r, m2, _g, w2 = audit(soc=d / "milan_soc.py")
        ck("commenting out the live row that carries cdc_pulse.sv is a MISSING SOURCE",
           row is not None and w2 is None and "cdc_pulse" in m2,
           f"row {row!r} missing {m2} why {w2}")
        dp = DATAPATH.read_text()
        end = dp.rfind("endmodule")
        (d / "milan_datapath.sv").write_text(
            dp[:end] + "\nKL_zz_col0 u_zz_col0 ();\n" + dp[end:])
        ck("a column-0 instantiation added to the live datapath reaches the first hop",
           "KL_zz_col0" in instantiated(d / "milan_datapath.sv"))

    print(f"\n{checks} checks: {checks - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    inst, reg, missing, gone, why = audit()
    if why is not None:
        print(f"CANNOT READ THE VIVADO LIST: {why}")
        return 2
    if not inst:
        print("CANNOT READ milan_datapath: no instantiation found, and an empty "
              "first hop would prove nothing")
        return 2

    if "--list" in args:
        print(f"instantiated by milan_datapath ({len(inst)}):")
        for m in sorted(inst):
            print(f"   {'ok ' if m in reg else 'MISS'}  {m}")
        print(f"\nregistered for Vivado ({len(reg)})")

    if missing or gone:
        for m in missing:
            print(f"MISSING SOURCE: milan_datapath instantiates '{m}' but "
                  f"sw/litex/milan_soc.py does not register it -> Vivado "
                  f"synthesis WILL fail with [Synth 8-439] module not found")
        for p in gone:
            print(f"STALE SOURCE: milan_soc.py registers '{p}' which does not exist")
        return 1

    print(f"SoC source gate: OK ({len(inst)} instantiated modules all registered, "
          f"{len(reg)} sources all present)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
