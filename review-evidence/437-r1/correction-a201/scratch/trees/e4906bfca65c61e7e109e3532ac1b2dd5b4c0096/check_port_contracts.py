#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a module boundary is reviewable without reading the implementation.

Why this exists. Rule 5 of the maintainability guide
(docs/development/CODE_QUALITY.md) says the module declaration and each
instantiation must make the boundary reviewable on their own.
`CONTRIBUTING.md` already states the half about declarations - "Ports
documented inline with `//!` - the port list IS the spec" - and nothing checked
it.

What is measured. Every tracked `.sv` and `.svh` under `hdl/` in the
superproject and both project-owned processor submodules: the shared
code-quality scope, minus the `LINT_EXCLUDE` list that `scripts/lint_rtl.py`
owns with a reason per entry (currently empty). Ports come from the ONE shared
header parser, `scripts/sv_ports.py`. The first version of this gate
carried a private one, and review found it ended a `module X import pkg::*;`
header at the import's `;`, so 23 modules - all three integration tops among
them - contributed no ports to the ratchet at all. One parser, both gates,
one population.

Five things are checked, and they are deliberately different kinds of check:

  1. WILDCARD BINDINGS (`.*`) are refused outright, by path:line. A `.*`
     connects by name at elaboration, so adding a port to a child silently
     rewires the parent with no diff at the instantiation site. The tree has
     none today, which is exactly why the arm that proves this check BITES
     matters more than the count: a gate whose population is empty is
     indistinguishable from a gate that does nothing.

  2. POSITIONAL BINDINGS are refused outright - port lists and parameter
     lists alike, instance arrays included - for the same reason with a
     sharper edge: reordering a child's ports or parameters silently rewires
     every positional parent and the widths often still fit. Only
     instantiations of modules THIS TREE declares are judged; a vendor
     primitive or generated wrapper keeps whatever form its tool requires.

  3. PRODUCTION HIERARCHICAL READS are refused: `inst.member` through any
     child instance declared in the file (first-party or foreign),
     `Module.inst.member` rooted in a module name this tree declares, and
     `$root.`. A child register is not a boundary; a dependency on it becomes
     a documented named port. Member access through an `interface` instance
     is a modport, not a backdoor, and is outside this population on purpose.

  4. UNDOCUMENTED PORTS are RATCHETED, per tree, not refused. There are
     hundreds, they are real debt, and a flag-day pass over them would be
     exactly the churn the governing rule forbids. Each tree's count may only
     fall, and a processor's debt is never traded against the superproject's.
     A port is documented when its own line carries `//!` or a standalone
     `//!` run documents the bundle it sits in; the bundle rule and its four
     boundaries are the parser's (see scripts/sv_ports.py). A header whose
     port list names ports with no direction keyword - the non-ANSI form - is
     refused by path:line rather than counted as zero, because the parser
     cannot see ports declared in the body and the rule requires ANSI ports.

  5. UNJUSTIFIED OPEN AND LITERAL-BOUND CONNECTIONS on first-party children
     are RATCHETED, by identity. An open status output and a tied-off input
     can each be the clearest boundary, so they are inventoried, not refused,
     but each owes a local rationale the way a lint waiver does. A connection
     is justified when a comment sits on its line, or a comment run sits
     directly above the contiguous run of open/literal connections it belongs
     to; a blank line, an ordinary connection or a sibling carrying its own
     comment ends that run. Whether the comment IS a rationale is review's
     job; that one exists is the gate's. No identity may be added; the budget
     lists every one that exists today so the debt is never hidden.

The population is REFUSED (exit 2, named) when it is empty, when any of
`hdl/`, `gptp-processor/hdl` or `protocol-processor/hdl` contributes no file
or no parsed port, or when a tracked HDL path is not present in the working
tree as a regular file (deleted, never checked out, or replaced by a symlink
or a directory): a pathspec or checkout problem must never read as green, and
dropping such a path from the population would be the under-count #186
forbids. An absent or off-pin processor is refused earlier, by the shared
scope.

Known limits, recorded here rather than left to be discovered:

  - the one `interface` header in the tree (hdl/common/axi_stream_if.sv: two
    ports, four parameters) is outside both gates' populations, because the
    shared parser reads `module` headers;
  - a hierarchical reference is recognised by its FIRST component: an instance
    declared in the same file, a module name this tree declares, or `$root`.
    A reference rooted in an instance that another file declares, or in a name
    a macro introduces, is not seen; a `.*` or positional form produced by a
    macro is seen only where the macro's own text is scanned (`.svh` files
    are, so a macro body carrying one is refused at its definition);
  - the inventories read RTL only: C++ harness access through Verilator's root
    (`__DOT__`) and the gPTP processor's board bench RTL under `bench/` are
    outside them, and the guide carries the counts.

Usage:
    python3 scripts/check_port_contracts.py                # gate
    python3 scripts/check_port_contracts.py --list         # per-file and per-connection detail
    python3 scripts/check_port_contracts.py --selftest     # fixture arms
    python3 scripts/check_port_contracts.py --write-budget # regenerate scripts/port_docs.budget

Exit 0 = no wildcard, positional or hierarchical production binding, every
tree's undocumented count at or under its ratchet, no unjustified connection
outside the budget. Exit 1 = a finding. Exit 2 = the population or the budget
is unusable (refused, named).
"""

import argparse
import re
import sys
from collections.abc import Collection, Iterable, Iterator
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "port_docs.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: which files are first-party gated surface is OWNED by lint_rtl.py, with a
#: recorded reason per exclusion. Importing it means the two gates can never
#: disagree about what this repository is responsible for.
from lint_rtl import LINT_EXCLUDE
from code_quality_scope import tracked
#: the ONE header parser: what ports a module declares, and which are documented
from sv_ports import declarations, module_headers

TREES = ("hdl", "gptp-processor", "protocol-processor")

STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')
COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
MODULE_DECL = re.compile(r"^\s*module\s+(\w+)", re.M)
INTERFACE_DECL = re.compile(r"^\s*interface\s+(\w+)", re.M)
WILDCARD = re.compile(r"\.\s*\*")
NAMED_CONNECTION = re.compile(r"\.\s*(?:\*|[A-Za-z_]\w*\s*\()")

#: SystemVerilog words that can precede a parenthesised or bracketed block and
#: would otherwise read as a module name in front of an instance name
NOT_A_MODULE = {
    "if", "else", "for", "while", "case", "casez", "casex", "repeat", "foreach",
    "assert", "assume", "cover", "always", "always_ff", "always_comb",
    "always_latch", "initial", "final", "return", "generate", "endgenerate",
    "begin", "end", "module", "endmodule", "function", "task", "posedge",
    "negedge", "wait", "disable", "$display", "$error", "$fatal", "bind",
    "unique", "priority", "property", "sequence", "assign", "force", "release",
    "typedef", "enum", "struct", "union", "packed", "parameter", "localparam",
    "input", "output", "inout", "wire", "logic", "reg", "var", "bit", "int",
    "integer", "byte", "shortint", "longint", "signed", "unsigned", "tri",
    "real", "time", "genvar", "automatic", "static", "virtual", "class",
    "import", "export", "default", "modport", "interface", "endinterface",
}


def blank_comments(text: str) -> str:
    """Blank string literals, block comments and line comments, keeping every
    newline so line numbers survive. Strings go first: `$display("u.hit")` is
    not a hierarchical read, and a `//` inside a string is not a comment."""
    def blank(m: re.Match[str]) -> str:
        """The match as spaces, its newlines kept so the line numbers hold."""
        return "".join(c if c == "\n" else " " for c in m.group(0))
    return COMMENT.sub(blank, STRING.sub(blank, text))


def tree_of(rel: str) -> str:
    """Which of the three trees owns a path, and so which ratchet judges it."""
    for sub in ("gptp-processor", "protocol-processor"):
        if rel.startswith(sub + "/"):
            return sub
    return "hdl"


def sources() -> list[str]:
    """The gated surface, taken from lint_rtl so the two gates cannot disagree."""
    return [p for p in tracked("hdl") if p.endswith((".sv", ".svh"))
            and p not in LINT_EXCLUDE]


def check_files(paths: Iterable[str], root: Path = REPO) -> str | None:
    """A refusal message naming every tracked HDL path the working tree does
    not hold as a regular file, or None. Such a path is refused, never dropped:
    a population quietly missing a file under-counts (#186), and a symlink is
    not the tracked blob either."""
    missing = [p for p in paths
               if (root / p).is_symlink() or not (root / p).is_file()]
    if missing:
        return (f"REFUSED: incomplete population - {len(missing)} tracked HDL "
                "path(s) not present as a regular file (deleted, never checked "
                "out, or replaced by a symlink or a directory): "
                + ", ".join(missing))
    return None


def declared_modules(paths: Iterable[str]) -> tuple[set[str], set[str]]:
    """(module names, interface names) this tree declares."""
    modules, ifaces = set(), set()
    for rel in paths:
        code = blank_comments((REPO / rel).read_text(errors="replace"))
        modules |= set(MODULE_DECL.findall(code))
        ifaces |= set(INTERFACE_DECL.findall(code))
    return modules, ifaces


# ---------------------------------------------------------------------------
# ports: the population and the undocumented count, through sv_ports
# ---------------------------------------------------------------------------
def scan_ports(text: str) -> tuple[int, list[str]]:
    """(total, undocumented_names) over the module headers in `text`."""
    total, undoc = 0, []
    for _module, name, doc, _multibit, kind in declarations(text):
        if kind == "param":
            continue
        total += 1
        if not doc.strip():
            undoc.append(name)
    return total, undoc


def non_ansi_headers(text: str) -> list[tuple[str, int]]:
    """[(module, line)] for every module whose port list names ports without a
    direction keyword: the non-ANSI form, whose directions live in the body
    where the parser does not look. Counting such a module as zero ports would
    let its whole boundary escape the ratchet, so it is refused instead."""
    with_ports = {m for m, _n, _d, _b, kind in declarations(text) if kind != "param"}
    out = []
    for module, header, line in module_headers(text):
        if module in with_ports:
            continue
        end = header.rfind(")")
        depth, start = 0, None
        for i in range(end, -1, -1):
            if header[i] == ")":
                depth += 1
            elif header[i] == "(":
                depth -= 1
                if depth == 0:
                    start = i
                    break
        if start is None or header[:start].rstrip().endswith("#"):
            continue                       # no port list, or only a parameter list
        body = re.sub(r"//![^\n]*", " ", header[start + 1:end])
        if re.search(r"[A-Za-z_]\w*", body):
            out.append((module, line))
    return out


# ---------------------------------------------------------------------------
# instantiations
# ---------------------------------------------------------------------------
def _close(code, opening, open_ch="(", close_ch=")"):
    """Index after the balanced closer beginning at `opening`, or None."""
    if opening >= len(code) or code[opening] != open_ch:
        return None
    depth = 0
    for pos in range(opening, len(code)):
        depth += 1 if code[pos] == open_ch else (-1 if code[pos] == close_ch else 0)
        if depth == 0:
            return pos + 1
    return None


def _skip_space(code, pos):
    while pos < len(code) and code[pos].isspace():
        pos += 1
    return pos


def _at_line_start(code, pos):
    return not code[code.rfind("\n", 0, pos) + 1:pos].strip()


def declared_instances(text: str, known: Collection[str], foreign: bool = False
                       ) -> Iterator[tuple[str, str, str, str, int, str]]:
    """Yield instances with their balanced connection text as
    (module, instance, params_text, conns_text, conns_start, code).

    A regex that jumps from `#(` to the instance name silently skips every
    parameterised instantiation because the parameter body lies between them.
    Walking the balanced lists makes parameterised and plain instances the
    same population, keeps module declarations out (they have no instance
    identifier after their optional parameter list), and steps over an
    instance array's `[range]`.

    Known modules are matched anywhere. With `foreign`, a module this tree does
    not declare is also matched, but only at the start of a line - where an
    instantiation lives and a function call, cast or declaration does not - so
    its instance names can root a hierarchical read.

    One head may declare several instances: `child u_a (.a(a)), u_b (.*);` is
    legal SystemVerilog (`module_instance { , module_instance } ;`). So after
    the first connection list the walk continues through every `, instance
    [range] ( ... )` of the tail, and each instance is yielded with the head's
    parameter text, its own connection list and its own position, so a
    wildcard, a positional list, an open or literal-bound connection or a
    hierarchical root on a later instance is judged like the first one's. The
    first version stopped after the first list, and review of PR #279 showed
    `u_bad(.*)` in that fixture passing the gate.
    """
    code = blank_comments(text)
    for module_match in re.finditer(r"\b[A-Za-z_]\w*\b", code):
        name = module_match.group(0)
        if name in NOT_A_MODULE:
            continue
        if name not in known and not (foreign and _at_line_start(code, module_match.start())):
            continue
        if module_match.start() and code[module_match.start() - 1] in ".:$`":
            continue
        pos = _skip_space(code, module_match.end())
        params = ""
        if pos < len(code) and code[pos] == "#":
            pos = _skip_space(code, pos + 1)
            end = _close(code, pos)
            if end is None:
                continue
            params = code[pos + 1:end - 1]
            pos = _skip_space(code, end)
        while True:                                         # every instance of the declaration
            inst_match = re.match(r"[A-Za-z_]\w*", code[pos:])
            if not inst_match or inst_match.group(0) in NOT_A_MODULE:
                break
            inst = inst_match.group(0)
            pos = _skip_space(code, pos + inst_match.end())
            if pos < len(code) and code[pos] == "[":        # instance array
                end = _close(code, pos, "[", "]")
                if end is None:
                    break
                pos = _skip_space(code, end)
            end = _close(code, pos)
            if end is None:
                break
            yield name, inst, params, code[pos + 1:end - 1], pos + 1, code
            pos = _skip_space(code, end)
            if pos >= len(code) or code[pos] != ",":        # `;` (or anything else) ends the tail
                break
            pos = _skip_space(code, pos + 1)


def _line(code, pos):
    return code[:pos].count("\n") + 1


def scan_bindings(text: str, known: Collection[str],
                  ifaces: Collection[str] = frozenset()
                  ) -> tuple[list[int], list[tuple[str, str, int, str]],
                             list[tuple[str, str, int]]]:
    """(wildcards, positional, hierarchical) for one source.

    wildcards:    [line]
    positional:   [(module, instance, line, what)]  what in {"ports", "parameters"}
    hierarchical: [(root, member, line)]
    `known` is the set of module names this tree declares; anything else is a
    vendor or generated boundary whose binding form its tool dictates, but
    whose instances still root a hierarchical read. `ifaces` are the interface
    names this tree declares; their instances are modports, not children."""
    code = blank_comments(text)
    wildcards, positional, instances = [], [], set()
    for name, inst, params, conns, start, _code in declared_instances(text, known, foreign=True):
        if name in ifaces:
            continue
        instances.add(inst)
        if name not in known:
            continue
        wildcards += [_line(code, start + m.start()) for m in WILDCARD.finditer(conns)]
        if conns.strip() and not NAMED_CONNECTION.search(conns):
            positional.append((name, inst, _line(code, start), "ports"))
        if params.strip() and not NAMED_CONNECTION.search(params):
            positional.append((name, inst, _line(code, start), "parameters"))
    hierarchical = []
    roots = sorted(instances | set(known))
    if roots:
        rooted = re.compile(r"(?<![.\w$:])(" + "|".join(map(re.escape, roots))
                            + r")\s*\.\s*([A-Za-z_]\w*)")
        for ref in rooted.finditer(code):
            hierarchical.append((ref.group(1), ref.group(2), _line(code, ref.start())))
    for ref in re.finditer(r"\$root\s*\.\s*([A-Za-z_]\w*)", code):
        hierarchical.append(("$root", ref.group(1), _line(code, ref.start())))
    return wildcards, sorted(positional, key=lambda p: p[2]), sorted(hierarchical, key=lambda h: h[2])


# ---------------------------------------------------------------------------
# open and literal-bound connections, and whether each carries a rationale
# ---------------------------------------------------------------------------
EMPTY_CONNECTION = re.compile(r"\.\s*([A-Za-z_]\w*)\s*\(\s*\)")
LITERAL_CONNECTION = re.compile(
    r"\.\s*([A-Za-z_]\w*)\s*\(\s*(?:\d+\s*)?'[sS]?[bBdDhHoO][0-9a-fA-F_xXzZ]+\s*\)"
    r"|\.\s*([A-Za-z_]\w*)\s*\(\s*'[01xXzZ]\s*\)"
    r"|\.\s*([A-Za-z_]\w*)\s*\(\s*[01]\s*\)")
COMMENT_ONLY = re.compile(r"^\s*//")
HAS_COMMENT = re.compile(r"//")


def scan_connection_dispositions(text: str, known: Collection[str]
                                 ) -> list[tuple[str, str, str, int, str, bool]]:
    """[(module, instance, port, line, kind, justified)] for every open
    (kind "OPEN") or literal-bound (kind "TIED") named port on a first-party
    child. Justification is the bundle rule of the docstring, read from the
    original text so the comments are still there."""
    lines = text.split("\n")
    found = []
    for name, inst, _params, conns, start, code in declared_instances(text, known):
        base = _line(code, start)
        hits = []
        for m in EMPTY_CONNECTION.finditer(conns):
            hits.append((m.group(1), base + conns[:m.start()].count("\n"), "OPEN"))
        for m in LITERAL_CONNECTION.finditer(conns):
            port = next(g for g in m.groups() if g is not None)
            hits.append((port, base + conns[:m.start()].count("\n"), "TIED"))
        hit_lines = {ln for _p, ln, _k in hits}
        for port, ln, kind in sorted(hits, key=lambda h: h[1]):
            found.append((name, inst, port, ln, kind, _justified(lines, ln, hit_lines)))
    return found


def _justified(lines, ln, hit_lines):
    """A comment on the connection's line, or a comment run directly above the
    contiguous run of open/literal connections (without comments of their own)
    that this connection belongs to."""
    if HAS_COMMENT.search(lines[ln - 1]):
        return True
    j = ln - 2                                    # 0-based index of the line above
    while j >= 0 and (j + 1) in hit_lines and not HAS_COMMENT.search(lines[j]):
        j -= 1                                    # a sibling without its own comment
    return j >= 0 and bool(COMMENT_ONLY.match(lines[j]))


def test_backdoors(known: Collection[str],
                   ifaces: Collection[str]) -> list[tuple[str, str, str, int]]:
    """Read-only inventory of hierarchical observation confined to test RTL."""
    found = []
    for rel in tracked("tb/**/*.sv"):
        text = (REPO / rel).read_text(errors="replace")
        _w, _p, hier = scan_bindings(text, known, ifaces)
        found += [(rel, root, member, line) for root, member, line in hier]
    return found


# ---------------------------------------------------------------------------
# the audit and its refusals
# ---------------------------------------------------------------------------
def check_population(files_per_tree: dict[str, int],
                     ports_per_tree: dict[str, int]) -> str | None:
    """A refusal message, or None. An empty or partial population must never
    establish a baseline or read as a pass."""
    if not any(files_per_tree.values()):
        return "REFUSED: empty population - no tracked .sv/.svh under hdl/ in any tree"
    for tree in TREES:
        if not files_per_tree.get(tree):
            return f"REFUSED: partial population - {tree} contributed no file"
        if not ports_per_tree.get(tree):
            return f"REFUSED: partial population - {tree} contributed no parsed port"
    return None


def audit() -> dict[str, object]:
    """One pass over the population: every finding, count and refusal at once.

    The refusal is carried in the result rather than raised, so a caller that
    wants the numbers and a caller that wants the verdict read the same scan.
    """
    paths = sources()
    files_per_tree = {t: 0 for t in TREES}
    ports_per_tree = {t: 0 for t in TREES}
    undoc_per_tree = {t: 0 for t in TREES}
    undoc, wild, pos, hier, dispositions, nonansi = {}, [], [], [], [], []
    refusal = check_files(paths)
    if refusal:
        # nothing is read: a scan of the files that ARE present is exactly
        # the under-count the refusal exists to prevent
        return {
            "files": files_per_tree, "ports": ports_per_tree,
            "undoc_per_tree": undoc_per_tree, "undoc": undoc, "wild": wild,
            "pos": pos, "hier": hier, "nonansi": nonansi,
            "dispositions": dispositions, "backdoors": [], "refusal": refusal,
        }
    known, ifaces = declared_modules(paths)
    for rel in paths:
        tree = tree_of(rel)
        text = (REPO / rel).read_text(errors="replace")
        n, u = scan_ports(text)
        nonansi += [(rel,) + t for t in non_ansi_headers(text)]
        files_per_tree[tree] += 1
        ports_per_tree[tree] += n
        undoc_per_tree[tree] += len(u)
        if u:
            undoc[rel] = u
        w, p, h = scan_bindings(text, known, ifaces)
        wild += [(rel, line) for line in w]
        pos += [(rel,) + t for t in p]
        hier += [(rel,) + t for t in h]
        dispositions += [(rel,) + d for d in scan_connection_dispositions(text, known)]
    return {
        "files": files_per_tree, "ports": ports_per_tree, "undoc_per_tree": undoc_per_tree,
        "undoc": undoc, "wild": wild, "pos": pos, "hier": hier, "nonansi": nonansi,
        "dispositions": dispositions, "backdoors": test_backdoors(known, ifaces),
        "refusal": check_population(files_per_tree, ports_per_tree),
    }


def identity(rel: str, inst: str, port: str) -> str:
    """`path:instance.port`. A processor path is spelled `<submodule>:<path>`,
    the form naming.budget and xvlog.budget use, so this generated file is
    never read as a hand-written list of submodule sources (pp_srcs --check
    refuses a literal `protocol-processor/hdl/.../x.sv` in any tracked file)."""
    tree = tree_of(rel)
    if tree != "hdl":
        rel = f"{tree}:{rel[len(tree) + 1:]}"
    return f"{rel}:{inst}.{port}"


# ---------------------------------------------------------------------------
# the budget: per-tree undocumented counts, unjustified connections by identity
# ---------------------------------------------------------------------------
def read_budget(path: Path = BUDGET) -> tuple[dict[str, int], set[str]] | None:
    """({tree: count}, {identity}) or None when missing or malformed."""
    if not path.is_file():
        return None
    counts, idents = {}, set()
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] == "undocumented" and len(parts) == 3 and parts[2].isdigit():
            counts[parts[1]] = int(parts[2])
        elif parts[0] == "unjustified" and len(parts) == 2:
            idents.add(parts[1])
        else:
            return None
    if any(t not in counts for t in TREES):
        return None
    return counts, idents


def ratchet(result: dict[str, object],
            budget: tuple[dict[str, int], set[str]]
            ) -> tuple[list[tuple[str, int, int]], list[str], list[str]]:
    """(over, new, left): trees over their count, unjustified identities not
    recorded, recorded identities no longer present."""
    counts, idents = budget
    over = [(t, result["undoc_per_tree"][t], counts[t]) for t in TREES
            if result["undoc_per_tree"][t] > counts[t]]
    current = {identity(rel, inst, port) for rel, _m, inst, port, _l, _k, ok
               in result["dispositions"] if not ok}
    return over, sorted(current - idents), sorted(idents - current)


def write_budget(result: dict[str, object], path: Path = BUDGET) -> None:
    """Re-record the ratchets from this tree, with the reasoning above them.

    Written only from the tool: a hand-edited number is a limit nobody
    measured, and the header says so where the next editor will read it.
    """
    rows = [(rel, inst, port) for rel, _m, inst, port, _l, _k, ok
            in result["dispositions"] if not ok]
    unjust = sorted(identity(*row) for row in rows)
    per_tree = {t: sum(1 for rel, _i, _p in rows if tree_of(rel) == t) for t in TREES}
    head = [
        "# GENERATED by scripts/check_port_contracts.py --write-budget - the Rule 5",
        "# ratchets. Regenerate only from the tool; every number is its measured",
        "# value at the head that commits it.",
        "#",
        "# undocumented: first-party module ports in each tree with no `//!`",
        "# contract, a standalone `//!` run counting for its bundle (the bundle",
        "# rule and its four boundaries are scripts/sv_ports.py's). EACH NUMBER",
        "# MAY ONLY GO DOWN, and a tree's debt is never traded against another's.",
        "# Re-measured on the corrected population after review: the private",
        "# scanner had dropped every port of the 23 `module X import pkg::*;`",
        "# headers, so 204 became a count over the whole population.",
        "#",
        "# unjustified: open or literal-bound named connections on first-party",
        "# children with no comment on the line and no comment run directly above",
        "# their run, as path:instance.port (a processor path is spelled",
        "# <submodule>:<path>, the naming.budget form). A LINE MAY ONLY LEAVE, by",
        "# adding the rationale or removing the port; none may be added. These",
        "# are the review inventory the guide classifies, not defects proven one",
        "# by one.",
        "#",
        "# ports per tree: " + ", ".join(f"{t} {result['ports'][t]}" for t in TREES),
        "# unjustified per tree: " + ", ".join(f"{t} {per_tree[t]}" for t in TREES),
    ]
    body = [f"undocumented {t} {result['undoc_per_tree'][t]}" for t in TREES]
    body += [f"unjustified {i}" for i in unjust]
    path.write_text("\n".join(head + body) + "\n")


# ---------------------------------------------------------------------------
# self-test: every answer known by construction; each arm fails when the
# defect it guards comes back
# ---------------------------------------------------------------------------
def _mod(body, head="module f ("):
    return f"{head}\n{body}\n);\nendmodule\n"


#: The names the self-test's fixtures declare: one child module and one
#: interface, so an arm reads without hunting for what "known" holds.
_SELFTEST_KNOWN = {"KL_child"}
_SELFTEST_IFACES = {"axi_stream_if"}


def _bindings(src):
    """`scan_bindings` over one fixture, with the self-test's declared names."""
    return scan_bindings(src, _SELFTEST_KNOWN, _SELFTEST_IFACES)


def _dispositions(src):
    """`scan_connection_dispositions` over one fixture."""
    return scan_connection_dispositions(src, _SELFTEST_KNOWN)


def _arm_binding_forms(ck):
    """Every binding form the gate refuses, and every one it accepts."""
    # -- the three refusals must BITE. Their live population is zero, so without
    # -- these arms the gate is indistinguishable from an inert one.
    w, p, h = _bindings("\n\n  KL_child u_c (.*);")
    ck("a wildcard binding is caught, with its line", w == [3], f"{w}")
    w, p, h = _bindings("  KL_child u_c (sig_a, sig_b);")
    ck("a positional binding is caught", [x[3] for x in p] == ["ports"], f"{p}")
    w, p, h = _bindings("  KL_child u_c (.a(sig_a), .b(sig_b));")
    ck("a named binding is accepted", not w and not p, f"{w} {p}")
    w, p, h = _bindings("  KL_child #(.W(8)) u_c (.a(sig_a));")
    ck("a parameterised named binding is accepted", not w and not p, f"{w} {p}")
    w, p, h = _bindings("  KL_child #(.W(8)) u_c (sig_a);")
    ck("a parameterised positional binding is caught", [x[3] for x in p] == ["ports"], f"{p}")
    w, p, h = _bindings("  KL_child #(8, 16) u_c (.a(sig_a));")
    ck("a positional PARAMETER list is caught", [x[3] for x in p] == ["parameters"], f"{p}")
    w, p, h = _bindings("  KL_child u_c [0:1] (.*);")
    ck("an instance array with a wildcard is caught", len(w) == 1, f"{w}")
    w, p, h = _bindings("  KL_child u_c [0:1] (sig_a, sig_b);")
    ck("an instance array bound by position is caught", len(p) == 1, f"{p}")
    w, p, h = _bindings("  KL_child u_c [0:1] (.a(sig_a));")
    ck("an instance array bound by name is accepted", not w and not p, f"{w} {p}")


def _arm_multi_instance(ck):
    """One head, several instances: each instance is judged on its own."""
    # -- one head, several instances: `module_instance { , module_instance } ;`.
    # -- The first version stopped after the first connection list, so the
    # -- reviewer's `u_bad(.*)` passed (PR #279).
    w, p, h = scan_bindings("child u_ok(.a(a)), u_bad(.*);", {"child"}, _SELFTEST_IFACES)
    ck("a wildcard on the second instance of a declaration is caught, with its line",
       w == [1], f"{w}")
    w, p, h = _bindings("  KL_child u_ok (.a(sig_a)), u_bad (sig_a, sig_b);")
    ck("a positional binding on the second instance is caught",
       [(x[1], x[3]) for x in p] == [("u_bad", "ports")], f"{p}")
    w, p, h = _bindings("  KL_child u_a (.a(sig_a)), u_b (.a(sig_b));")
    seen = [i for _m, i, *_ in declared_instances("  KL_child u_a (.a(sig_a)), u_b (.a(sig_b));", _SELFTEST_KNOWN)]
    ck("a clean two-instance declaration is accepted and both instances are seen",
       not w and not p and seen == ["u_a", "u_b"], f"{w} {p} {seen}")
    three = "  KL_child #(.W(8)) u_a (.a(sig_a)),\n    u_b [0:1] (.a(sig_b)),\n    u_c (.a(sig_c));"
    w, p, h = _bindings(three)
    seen = [(i, prm.strip()) for _m, i, prm, *_ in declared_instances(three, _SELFTEST_KNOWN)]
    ck("a three-instance declaration with an array and a parameterised head is accepted, every instance seen",
       not w and not p and seen == [("u_a", ".W(8)"), ("u_b", ".W(8)"), ("u_c", ".W(8)")], f"{w} {p} {seen}")
    w, p, h = _bindings(three.replace("(.a(sig_c))", "(.*)"))
    ck("a wildcard on the third instance is caught on its own line", w == [3], f"{w}")
    w, p, h = _bindings(three.replace("(.a(sig_b))", "(sig_b)"))
    ck("a positional array instance in the middle of a declaration is caught",
       [(x[1], x[2], x[3]) for x in p] == [("u_b", 2, "ports")], f"{p}")
    w, p, h = _bindings("  KL_child #(8) u_a (.a(sig_a)), u_b (.a(sig_b));")
    ck("a positional parameter list on a shared head is refused for every instance it configures",
       [(x[1], x[3]) for x in p] == [("u_a", "parameters"), ("u_b", "parameters")], f"{p}")
    w, p, h = _bindings("  KL_child u_a (.a(sig_a)), u_b (.a(sig_b));\n  assign leak = u_b.hidden_r;")
    ck("a read through the second instance is a hierarchical dependency",
       h == [("u_b", "hidden_r", 2)], f"{h}")
    w, p, h = _bindings("  VendorPrimitive u_a (sig_a), u_b (sig_b);\n  assign leak = u_b.q;")
    ck("a foreign head's later instance is not judged but still roots a read",
       not p and h == [("u_b", "q", 2)], f"{p} {h}")


def _arm_foreign_and_noise(ck):
    """A foreign module keeps its form, and comments and strings are not bindings."""
    # a module this tree does NOT declare keeps whatever form its tool needs
    w, p, h = _bindings("  VendorPrimitive u_v (sig_a, sig_b);")
    ck("a foreign module is not judged", not p, f"{p}")
    w, p, h = _bindings("  VendorPrimitive u_v (.*);")
    ck("a foreign wildcard keeps its boundary exception", not w, f"{w}")

    # control flow, comments and strings must not read as bindings
    w, p, h = _bindings("  if (cond) begin\n    x <= 1;\n  end")
    ck("control flow is not an instantiation", not p, f"{p}")
    w, p, h = _bindings("  // KL_child u_c (sig_a, sig_b);")
    ck("a commented-out binding is not counted", not p and not w, f"{p} {w}")
    w, p, h = _bindings('  KL_child u_c (.a(sig_a));\n  initial $display("u_c.hit");')
    ck("a string literal is not a hierarchical read", not h, f"{h}")


def _arm_hierarchical_reads(ck):
    """What counts as a read through a child, and what only looks like one."""
    # -- production hierarchical reads --
    w, p, h = _bindings("  KL_child u_c (.a(sig_a));\n  assign leak = u_c.hidden_r;")
    ck("a read through a first-party child is caught", h == [("u_c", "hidden_r", 2)], f"{h}")
    w, p, h = _bindings("  axis_fifo #(._dispositions(4)) u_f (.a(sig_a));\n  assign leak = u_f.rd_ptr_reg;")
    ck("a read through a FOREIGN child instance is caught", h == [("u_f", "rd_ptr_reg", 2)], f"{h}")
    w, p, h = _bindings("  assign leak = KL_child.u_x.pass_r;")
    ck("a reference rooted in a module name is caught", h == [("KL_child", "u_x", 1)], f"{h}")
    w, p, h = _bindings("  assign leak = $root.top.u_x.pass_r;")
    ck("a $root reference is caught", h == [("$root", "top", 1)], f"{h}")
    w, p, h = _bindings("  axi_stream_if s_axis ();\n  assign v = s_axis.tvalid;")
    ck("interface member access is a modport, not a backdoor", not h, f"{h}")
    w, p, h = _bindings("  assign v = pkt.KL_child.x;\n  assign q = my_pkg::KL_child.y;")
    ck("a struct member or package item named like a module is not a reference", not h, f"{h}")
    w, p, h = _bindings("  wire foo (a, b);\n  logic [7:0] arr [0:3];")
    ck("a declaration is not a foreign instantiation", not h and not p, f"{h} {p}")


def _arm_port_documentation(ck):
    """Which ports the shared parser sees, and which comment documents which."""
    # -- port documentation, through the shared parser --
    n, u = scan_ports(_mod("  input wire clk_i  //! the clock"))
    ck("a documented port is not counted", n == 1 and not u, f"{n} {u}")
    n, u = scan_ports(_mod("  input wire clk_i"))
    ck("an undocumented port is counted", n == 1 and u == ["clk_i"], f"{n} {u}")
    n, u = scan_ports(_mod("  //! the clock\n  input wire clk_i"))
    ck("documentation may sit on the line above", n == 1 and not u, f"{n} {u}")
    n, u = scan_ports(_mod("  //! the stream\n  input wire v_i,\n  input wire r_i,\n  input wire l_i"))
    ck("one comment documents a contiguous bundle", n == 3 and not u, f"{n} {u}")
    n, u = scan_ports(_mod("  //! the stream\n  input wire v_i,\n\n  input wire other_i"))
    ck("a blank line ends the bundle", n == 2 and u == ["other_i"], f"{n} {u}")
    n, u = scan_ports(_mod("  input wire a_i,  //! documents a_i and nothing else\n  input wire b_i"))
    ck("a sibling port's trailing comment does not document the next port",
       n == 2 and u == ["b_i"], f"{n} {u}")
    n, u = scan_ports(_mod("  // ---- a plain section banner ----\n  input wire a_i"))
    ck("a plain // banner is not a port contract", n == 1 and u == ["a_i"], f"{n} {u}")
    n, u = scan_ports("module m\n  import p_pkg::*;\n#(\n  parameter int N = 1\n) (\n"
                      "  input wire a_i,\n  output logic b_o //! b\n);\nendmodule\n")
    ck("a `module X import pkg::*;` header keeps its port list",
       n == 2 and u == ["a_i"], f"{n} {u}")
    n, u = scan_ports("module m #(\n  //! table depth\n  parameter int N = 16\n) (\n"
                      "  input wire clk_i,\n  input wire rst_n\n);\nendmodule\n")
    ck("a parameter's comment does not document the ports after `)(`",
       n == 2 and u == ["clk_i", "rst_n"], f"{n} {u}")
    n, u = scan_ports(_mod("  input wire a_i, b_i, c_i"))
    ck("names sharing one declaration are each a port", n == 3 and len(u) == 3, f"{n} {u}")
    n, u = scan_ports(_mod("  axi_stream_if.slave s_axis, //! ingress\n  input wire clk_i"))
    ck("an interface-modport port is in the population", n == 2 and u == ["clk_i"], f"{n} {u}")
    n, u = scan_ports(_mod("  input wire a_i, //! the output of the mux, one parameter\n  input wire b_i"))
    ck("a keyword inside `//!` prose is not a port", n == 2 and u == ["b_i"], f"{n} {u}")
    n, u = scan_ports("module f (\n  input wire clk_i //! clock\n);\n"
                      "  function automatic int g(input int x);\n    return x;\n  endfunction\nendmodule\n")
    ck("a function argument in the body is not a port", n == 1 and not u, f"{n} {u}")
    na = non_ansi_headers("module old_style (clk_i, a, b);\n  input clk_i;\n  input a;\n  output b;\nendmodule\n")
    ck("a non-ANSI port list is refused, with its line", na == [("old_style", 1)], f"{na}")
    for src, what in (("module m #(parameter int N = 1);\nendmodule\n", "a parameter list alone"),
                      ("module m ();\nendmodule\n", "an empty port list"),
                      ("module m;\nendmodule\n", "no port list"),
                      (_mod("  input wire clk_i //! clock"), "an ANSI port list")):
        na = non_ansi_headers(src)
        ck(f"{what} is not a non-ANSI header", not na, f"{na}")


def _arm_dispositions(ck):
    """Open and literal-bound connections, and the comment that justifies one."""
    # -- open and literal-bound connections and their rationale --
    d = _dispositions("  KL_child u_c (.unused_o(), .reset_i(1'b0), .data_i(sig));")
    ck("open and literal-bound ports are inventoried",
       [(x[2], x[4]) for x in d] == [("unused_o", "OPEN"), ("reset_i", "TIED")], f"{d}")
    d = _dispositions("  KL_child u_c (\n    .unused_o(), // never consumed here\n    .data_i(sig));")
    ck("a comment on the connection's line justifies it", [x[5] for x in d] == [True], f"{d}")
    d = _dispositions("  KL_child u_c (\n    //! the diagnostic is owned by software\n"
                      "    .unused_o(),\n    .data_i(sig));")
    ck("a comment directly above justifies it", [x[5] for x in d] == [True], f"{d}")
    d = _dispositions("  KL_child u_c (\n    //! P4 seam, unlanded at this pin\n"
                      "    .a_o(),\n    .b_i(1'b0),\n    .c_i('0),\n    .data_i(sig));")
    ck("a comment above a contiguous run justifies the whole run",
       [x[5] for x in d] == [True, True, True], f"{d}")
    d = _dispositions("  KL_child u_c (\n    //! a rationale\n\n    .unused_o(),\n    .data_i(sig));")
    ck("a blank line between the comment and the connection leaves it unjustified",
       [x[5] for x in d] == [False], f"{d}")
    d = _dispositions("  KL_child u_c (\n    .data_i(sig),\n    .unused_o());")
    ck("no comment is no rationale", [x[5] for x in d] == [False], f"{d}")
    d = _dispositions("  KL_child u_c (\n    //! only a\n    .a_o(),\n    .data_i(sig),\n    .b_o());")
    ck("an ordinary connection ends the run", [x[5] for x in d] == [True, False], f"{d}")
    d = _dispositions("  KL_child u_c (\n    .a_o(), //! a's own reason\n    .b_o());")
    ck("a sibling's own comment ends the run", [x[5] for x in d] == [True, False], f"{d}")
    d = _dispositions("  KL_child u_a (.a(sig)), u_b (\n    .x_o(),\n"
                      "    .y_i(1'b0), //! y is a feature disable here\n    .a(sig));")
    ck("open and literal-bound ports on the second instance are inventoried with their rationale",
       [(x[1], x[2], x[3], x[4], x[5]) for x in d]
       == [("u_b", "x_o", 2, "OPEN", False), ("u_b", "y_i", 3, "TIED", True)], f"{d}")


def _arm_ratchets(ck):
    """The ratchet verdicts, the identity spelling and the budget refusals."""
    # -- the ratchets, on synthetic results --
    res = {"undoc_per_tree": {"hdl": 5, "gptp-processor": 1, "protocol-processor": 2},
           "dispositions": [("x.sv", "KL_child", "u_c", "a_o", 3, "OPEN", False),
                            ("x.sv", "KL_child", "u_c", "b_i", 4, "TIED", True)]}
    budget = ({"hdl": 5, "gptp-processor": 1, "protocol-processor": 2}, {"x.sv:u_c.a_o"})
    ck("counts at the ratchet and recorded identities pass", ratchet(res, budget) == ([], [], []))
    res2 = dict(res, undoc_per_tree={"hdl": 4, "gptp-processor": 2, "protocol-processor": 2})
    over, new, left = ratchet(res2, budget)
    ck("a tree over its count is refused even when another fell",
       over == [("gptp-processor", 2, 1)], f"{over}")
    res3 = dict(res, dispositions=res["dispositions"] + [("y.sv", "KL_child", "u_d", "z_o", 9, "OPEN", False)])
    ck("a new unjustified identity is refused", ratchet(res3, budget)[1] == ["y.sv:u_d.z_o"])
    res4 = dict(res, dispositions=[])
    ck("a recorded identity that gained its rationale has left",
       ratchet(res4, budget) == ([], [], ["x.sv:u_c.a_o"]))
    # the literal is assembled so this file never spells a submodule source
    # path itself, the property pp_srcs --check holds over every tracked file
    pp_path = "/".join(("protocol-processor", "hdl", "srp", "KL_srp_top.sv"))
    ck("a processor identity is spelled <submodule>:<path>, never as a source path",
       identity(pp_path, "u_d", "p_i") == "protocol-processor:hdl/srp/KL_srp_top.sv:u_d.p_i"
       and identity("hdl/x.sv", "u", "p") == "hdl/x.sv:u.p")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bp = Path(td) / "b"
        bp.write_text("undocumented hdl 1\nundocumented gptp-processor 1\n")
        ck("a budget missing a tree is unusable", read_budget(bp) is None)
        bp.write_text("undocumented hdl 1\nundocumented gptp-processor 1\n"
                      "undocumented protocol-processor x\n")
        ck("a non-numeric count is unusable", read_budget(bp) is None)
        ck("a missing budget is unusable", read_budget(Path(td) / "none") is None)
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "a.sv").write_text("module a; endmodule\n")
        (root / "d.sv").mkdir()
        (root / "l.sv").symlink_to("a.sv")
        ck("a tracked HDL path present as a regular file is not refused",
           check_files(["a.sv"], root) is None)
        refusal = check_files(["a.sv", "gone.sv", "d.sv", "l.sv"], root) or ""
        ck("a tracked HDL path that is absent, a directory or a symlink is refused, by name",
           refusal.startswith("REFUSED: incomplete population")
           and all(name in refusal for name in ("gone.sv", "d.sv", "l.sv"))
           and "a.sv" not in refusal.split(": ")[-1], refusal)


def _arm_population(ck):
    """The population refusals: an empty, fileless or portless tree."""
    # -- the population refusals --
    ck("an empty population is refused",
       (check_population({}, {}) or "").startswith("REFUSED: empty"))
    ck("a tree with no file is refused, by name",
       "gptp-processor" in (check_population({"hdl": 3, "gptp-processor": 0, "protocol-processor": 3},
                                             {"hdl": 9, "gptp-processor": 0, "protocol-processor": 9}) or ""))
    ck("a tree with files but no parsed port is refused, by name",
       "protocol-processor" in (check_population({"hdl": 3, "gptp-processor": 3, "protocol-processor": 3},
                                                 {"hdl": 9, "gptp-processor": 9, "protocol-processor": 0}) or ""))
    ck("a whole population is accepted",
       check_population({"hdl": 3, "gptp-processor": 3, "protocol-processor": 3},
                        {"hdl": 9, "gptp-processor": 9, "protocol-processor": 9}) is None)


def _arm_live_scan(ck):
    """The live tree: the scan must actually reach and read every tree."""
    # -- and the live scan must actually read the tree --
    result = audit()
    ck("the live population is whole", result["refusal"] is None, f"{result['refusal']}")
    total = sum(result["ports"].values())
    ck("the live scan reads the tree", total > 3000, f"{total} ports")
    for tree in TREES:
        ck(f"the live scan reaches {tree}", result["ports"][tree] > 0, f"{result['ports']}")
    ck("lint_rtl's exclusion list is empty today, so every tracked .sv/.svh is in the population",
       not LINT_EXCLUDE)
    paths = sources()
    known_live, _ = declared_modules(paths)
    for rel, least in (("hdl/milan/milan_datapath.sv", 100),
                       ("/".join(("gptp-processor", "hdl", "top", "KL_gptp_engine.sv")), 30),
                       ("/".join(("protocol-processor", "hdl", "top", "protocol_processor_top.sv")), 100)):
        n, _u = scan_ports((REPO / rel).read_text(errors="replace"))
        ck(f"the `import` header of {rel.split('/')[-1]} contributes its ports",
           n >= least, f"{n} ports, expected at least {least}")
    ck("the .svh files are in the binding population", any(p.endswith(".svh") for p in paths))
    ck("the tree's interface is not a hierarchical root", "axi_stream_if" not in known_live)


def selftest() -> int:
    """Prove each refusal BITES on a fixture whose answer is known by hand.

    The live population of the three refused forms is zero, so without these
    arms a working gate and an inert one report exactly the same thing.
    """
    failures, n_checks = 0, 0

    def ck(name: str, ok: bool, detail: str = "") -> None:
        """Score one arm; `detail` is printed only when the arm went red."""
        nonlocal failures, n_checks
        n_checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    for arm in (_arm_binding_forms, _arm_multi_instance, _arm_foreign_and_noise,
                _arm_hierarchical_reads, _arm_port_documentation,
                _arm_dispositions, _arm_ratchets, _arm_population,
                _arm_live_scan):
        arm(ck)

    print(f"\n{n_checks} checks: {n_checks - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


# ---------------------------------------------------------------------------
def main() -> int:
    """The gate's exit status: 0 clean, 1 a finding, 2 an unusable population."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="per-file and per-connection detail")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    ap.add_argument("--write-budget", action="store_true",
                    help="regenerate scripts/port_docs.budget from this tree")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    result = audit()
    if result["refusal"]:
        print(result["refusal"])
        return 2

    if args.write_budget:
        write_budget(result)
        print(f"wrote {BUDGET.relative_to(REPO)}")
        return 0

    bad = 0
    for rel, line in result["wild"]:
        bad += 1
        print(f"WILDCARD BINDING: {rel}:{line} uses `.*`. Adding a port to the child "
              f"would rewire this instance with no diff here.")
    for rel, name, inst, line, what in result["pos"]:
        bad += 1
        print(f"POSITIONAL BINDING: {rel}:{line} instantiates {name} as {inst} with a "
              f"positional {what[:-1]} list. Reordering the child's {what} would rewire it silently.")
    for rel, root, member, line in result["hier"]:
        bad += 1
        print(f"HIERARCHICAL DEPENDENCY: {rel}:{line} reads `{root}.{member}`. "
              f"Production dependencies cross the module boundary through a named port.")
    for rel, module, line in result["nonansi"]:
        bad += 1
        print(f"NON-ANSI PORT LIST: {rel}:{line} declares {module}'s ports without a "
              f"direction in the header. The gate cannot count them; Rule 5 requires ANSI ports.")

    unjustified = [d for d in result["dispositions"] if not d[6]]
    if args.list:
        for tree in TREES:
            files = sorted((r for r in result["undoc"] if tree_of(r) == tree),
                           key=lambda r: -len(result["undoc"][r]))
            print(f"  {tree}: {result['ports'][tree]} port(s) in {result['files'][tree]} file(s), "
                  f"{result['undoc_per_tree'][tree]} undocumented in {len(files)} file(s)")
            for rel in files:
                print(f"  {len(result['undoc'][rel]):>4} undocumented  {rel}: "
                      + " ".join(result["undoc"][rel]))
        for rel, name, inst, port, line, kind, ok in result["dispositions"]:
            print(f"  {kind}  {'justified  ' if ok else 'UNJUSTIFIED'}  {rel}:{line} {name} {inst}.{port}")
        for rel, root, member, line in result["backdoors"]:
            print(f"  TEST-XMR  {rel}:{line} {root}.{member}")
        print()

    budget = read_budget()
    if budget is None:
        print(f"NO RATCHET: {BUDGET.relative_to(REPO)} is missing or malformed "
              f"(regenerate with --write-budget)")
        return 2
    over, new, left = ratchet(result, budget)
    for tree, count, limit in over:
        bad += 1
        print(f"PORT-DOC RATCHET: FAIL ({tree}: {count} undocumented > ratchet {limit}). "
              f"A new port carries its `//!` contract.")
    for ident in new:
        bad += 1
        print(f"UNJUSTIFIED CONNECTION: {ident} is open or literal-bound with no rationale "
              f"comment on its line or directly above its run, and is not in the budget.")
    if bad:
        return 1

    total = sum(result["ports"].values())
    undoc = sum(result["undoc_per_tree"].values())
    print(f"port contract gate: OK ({total} first-party port(s): "
          + ", ".join(f"{t} {result['ports'][t]}" for t in TREES)
          + f"; {undoc} undocumented: "
          + ", ".join(f"{t} {result['undoc_per_tree'][t]} <= {budget[0][t]}" for t in TREES)
          + "; 0 wildcard, 0 positional, 0 hierarchical binding)")
    opens = sum(1 for d in result["dispositions"] if d[5] == "OPEN")
    tied = sum(1 for d in result["dispositions"] if d[5] == "TIED")
    print(f"  review inventory: {opens} open and {tied} literal-bound named connection(s), "
          f"{len(unjustified)} without a local rationale (all recorded; none may be added); "
          f"{len(result['backdoors'])} test-only hierarchical observation(s)")
    lowerable = [t for t in TREES if result["undoc_per_tree"][t] < budget[0][t]]
    if lowerable or left:
        print("  the ratchet can be lowered - regenerate with --write-budget"
              + (f" ({', '.join(f'{t} {result['undoc_per_tree'][t]}' for t in lowerable)})" if lowerable else "")
              + (f"; {len(left)} recorded connection(s) gained a rationale or left" if left else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
