#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a module boundary is reviewable without reading the implementation.

Why this exists. Rule 5 of the maintainability guide
(docs/development/CODE_QUALITY.md) says the module declaration and each
instantiation must make the boundary reviewable on their own.
`CONTRIBUTING.md` already states the half about declarations — "Ports
documented inline with `//!` — the port list IS the spec" — and nothing checked
it. Across the superproject and both project-owned processor submodules, 222
of 2,003 module/interface ports carried no documentation before the
representative cleanup below.

Four things are checked, and they are deliberately different kinds of check:

  1. WILDCARD BINDINGS (`.*`) are refused outright. A `.*` connects by name at
     elaboration, so adding a port to a child silently rewires the parent with
     no diff at the instantiation site. The tree has none today, which is
     exactly why the arm that proves this check BITES matters more than the
     count: a gate whose population is empty is indistinguishable from a gate
     that does nothing.

  2. POSITIONAL BINDINGS are refused outright, for the same reason with a
     sharper edge: reordering a child's ports silently rewires every positional
     parent and the types often still fit. Only instantiations of modules THIS
     TREE declares are judged - a vendor primitive or generated wrapper keeps
     whatever form its tool requires.

  3. PRODUCTION HIERARCHICAL READS through a declared child instance are
     refused. A child register is not a boundary; a dependency on it becomes a
     documented named port instead.

  4. UNDOCUMENTED PORTS are RATCHETED, not refused. There are hundreds, they
     are real debt, and a flag-day pass over them would be exactly the churn
     the governing rule forbids. The count may not rise.

The project-owned processor submodules come from the shared code-quality scope.
The individual excluded-file list is NOT written again here: it is imported
from `scripts/lint_rtl.py`, which records why for each exception.
`hdl/milan/milan_top.sv` is in it — a Zynq top that no build compiles and that
cannot elaborate here — and documenting its ports would decorate a file every
gate already ignores.

Usage:
    python3 scripts/check_port_contracts.py            # gate
    python3 scripts/check_port_contracts.py --list     # per-file counts
    python3 scripts/check_port_contracts.py --selftest # mutation arms

Exit 0 = no wildcard/positional/hierarchical production binding, and
undocumented ports at or under the ratchet in scripts/port_docs.budget.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "port_docs.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: which files are first-party gated surface is OWNED by lint_rtl.py, with a
#: recorded reason per exclusion. Importing it means the two gates can never
#: disagree about what this repository is responsible for.
from lint_rtl import LINT_EXCLUDE
from code_quality_scope import tracked

PORT = re.compile(
    r"^\s*(input|output|inout)\s+(?:wire|logic|var)?\s*(?:signed\s+)?"
    r"(?:\[[^\]]*\]\s*)?(\w+)")
COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
MODULE_DECL = re.compile(r"^\s*module\s+(\w+)", re.M)
BOUNDARY_DECL = re.compile(r"^\s*(?:module|interface)\s+(\w+)", re.M)
WILDCARD = re.compile(r"\.\s*\*\s*\)")

#: SystemVerilog keywords that can open a parenthesised block and would
#: otherwise read as a module instantiation
NOT_A_MODULE = {
    "if", "else", "for", "while", "case", "casez", "casex", "repeat", "foreach",
    "assert", "assume", "cover", "always", "always_ff", "always_comb",
    "always_latch", "initial", "final", "return", "generate", "endgenerate",
    "begin", "end", "module", "endmodule", "function", "task", "posedge",
    "negedge", "wait", "disable", "$display", "$error", "$fatal",
}


def blank_comments(text):
    def blank(m):
        return "".join(c if c == "\n" else " " for c in m.group(0))
    return COMMENT.sub(blank, text)


def sources():
    return [p for p in tracked("hdl") if p.endswith(".sv") and p not in LINT_EXCLUDE]


def declared_modules(paths):
    names = set()
    for rel in paths:
        names |= set(MODULE_DECL.findall(blank_comments((REPO / rel).read_text(errors="replace"))))
    return names


def module_headers(text):
    """Yield module declarations through the semicolon after their port list."""
    code = blank_comments(text)
    for match in BOUNDARY_DECL.finditer(code):
        depth = 0
        for pos in range(match.end(), len(code)):
            char = code[pos]
            depth += 1 if char == "(" else (-1 if char == ")" else 0)
            if char == ";" and depth == 0:
                yield text[match.start():pos + 1]
                break


def _scan_port_lines(text):
    """(total, undocumented_names) for one source, comments intact.

    A port is documented when it carries `//!` on its own line, or when a `//!`
    line appears in the contiguous block above it - the run of lines back to
    the nearest blank line. That second form is how the house style actually
    reads a bundle: one comment over an AXIS valid/ready/last triple states the
    contract for all three, and demanding "//! valid" on the valid pin would
    add noise, not meaning. A blank line ends the group, so a comment cannot
    reach across an unrelated one.
    """
    lines = text.splitlines()
    total, undoc = 0, []
    for i, line in enumerate(lines):
        m = PORT.match(line)
        if not m:
            continue
        total += 1
        if "//!" in line:
            continue
        j, documented = i - 1, False
        while j >= 0 and lines[j].strip():
            above = lines[j].strip()
            if above.startswith("//!"):
                documented = True
                break
            if PORT.match(lines[j]) and "//!" in lines[j]:
                break          # a sibling that carries its OWN trailing `//!`
                               # ends the bundle: the comment above it belongs
                               # to that port, not to this one. An undocumented
                               # sibling is part of the same bundle, so the walk
                               # continues past it to the group comment.
            j -= 1
        if not documented:
            undoc.append(m.group(2))
    return total, undoc


def scan_ports(text, require_header=False):
    """(total, undocumented_names) for module ports only.

    Task/function arguments also use the `input` and `output` keywords. They
    are not module boundary ports and must not consume or hide ratchet budget.
    Header extraction keeps those later declarations out of the population.
    Bare snippets remain supported for the fixture arms.
    """
    headers = list(module_headers(text))
    if require_header and not headers:
        return 0, []
    targets = headers if headers else [text]
    total, undoc = 0, []
    for header in targets:
        n, names = _scan_port_lines(header)
        total += n
        undoc.extend(names)
    return total, undoc


def scan_bindings(text, known):
    """(wildcards, positionals, hierarchical) for one source. `known` is the set of module
    names this tree declares; anything else is a vendor or generated boundary
    whose form its tool dictates."""
    code = blank_comments(text)
    wildcards = [m.start() for m in WILDCARD.finditer(code)]
    positional, instances = [], set()
    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*(#\s*\(|\s)\s*([A-Za-z_]\w*)\s*\(", code):
        name, inst = m.group(1), m.group(3)
        if name in NOT_A_MODULE or name not in known:
            continue
        instances.add(inst)
        start = m.end()
        depth, j = 1, start
        while j < len(code) and depth:
            depth += 1 if code[j] == "(" else (-1 if code[j] == ")" else 0)
            j += 1
        conns = code[start:j - 1]
        if conns.strip() and "." not in conns:
            positional.append((name, inst, code[:m.start()].count("\n") + 1))
    hierarchical = []
    for inst in sorted(instances):
        for ref in re.finditer(r"\b" + re.escape(inst) + r"\s*\.\s*([A-Za-z_]\w*)", code):
            hierarchical.append((inst, ref.group(1), code[:ref.start()].count("\n") + 1))
    for ref in re.finditer(r"\$root\s*\.\s*([A-Za-z_]\w*)", code):
        hierarchical.append(("$root", ref.group(1), code[:ref.start()].count("\n") + 1))
    return wildcards, positional, hierarchical


def audit():
    paths = sources()
    known = declared_modules(paths)
    total, undoc, wild, pos, hier = 0, {}, [], [], []
    for rel in paths:
        text = (REPO / rel).read_text(errors="replace")
        n, u = scan_ports(text, require_header=True)
        total += n
        if u:
            undoc[rel] = u
        w, p, h = scan_bindings(text, known)
        wild += [(rel, off) for off in w]
        pos += [(rel,) + t for t in p]
        hier += [(rel,) + t for t in h]
    return total, undoc, wild, pos, hier


def read_budget():
    if not BUDGET.is_file():
        return None
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line.isdigit():
            return int(line)
    return None


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    known = {"KL_child"}

    # -- the three refusals must BITE. Their live population is zero, so without
    # -- these arms the gate is indistinguishable from an inert one.
    w, p, h = scan_bindings("  KL_child u_c (.*);", known)
    ck("a wildcard binding is caught", len(w) == 1, f"{w}")
    w, p, h = scan_bindings("  KL_child u_c (sig_a, sig_b);", known)
    ck("a positional binding is caught", len(p) == 1, f"{p}")
    w, p, h = scan_bindings("  KL_child u_c (.a(sig_a), .b(sig_b));", known)
    ck("a named binding is accepted", not w and not p, f"{w} {p}")
    w, p, h = scan_bindings("  KL_child #(.W(8)) u_c (.a(sig_a));", known)
    ck("a parameterised named binding is accepted", not w and not p, f"{w} {p}")

    # a module this tree does NOT declare keeps whatever form its tool needs
    w, p, h = scan_bindings("  VendorPrimitive u_v (sig_a, sig_b);", known)
    ck("a foreign module is not judged", not p, f"{p}")

    # control flow must not read as an instantiation
    w, p, h = scan_bindings("  if (cond) begin\n    x <= 1;\n  end", known)
    ck("control flow is not an instantiation", not p, f"{p}")

    # a binding inside a comment is not a binding
    w, p, h = scan_bindings("  // KL_child u_c (sig_a, sig_b);", known)
    ck("a commented-out binding is not counted", not p and not w, f"{p} {w}")
    w, p, h = scan_bindings(
        "  KL_child u_c (.a(sig_a));\n  assign leak = u_c.hidden_r;", known)
    ck("a production hierarchical dependency is caught",
       h == [("u_c", "hidden_r", 2)], f"{h}")

    # -- port documentation --
    n, u = scan_ports("  input wire clk_i,  //! the clock")
    ck("a documented port is not counted", n == 1 and not u, f"{n} {u}")
    n, u = scan_ports("  input wire clk_i,")
    ck("an undocumented port is counted", n == 1 and u == ["clk_i"], f"{n} {u}")
    n, u = scan_ports("  //! the clock\n  input wire clk_i,")
    ck("documentation may sit on the line above", n == 1 and not u, f"{n} {u}")
    n, u = scan_ports("  //! the stream\n  input wire v_i,\n  input wire r_i,\n"
                      "  input wire l_i,")
    ck("one comment documents a contiguous bundle", n == 3 and not u, f"{n} {u}")
    n, u = scan_ports("  //! the stream\n  input wire v_i,\n\n  input wire other_i,")
    ck("a blank line ends the bundle", n == 2 and u == ["other_i"], f"{n} {u}")
    n, u = scan_ports("  input wire a_i,  //! documents a_i and nothing else\n"
                      "  input wire b_i,")
    ck("a sibling port's trailing comment does not document the next port",
       n == 2 and u == ["b_i"], f"{n} {u}")
    n, u = scan_ports("  // ---- a plain section banner ----\n  input wire a_i,")
    ck("a plain // banner is not a port contract", n == 1 and u == ["a_i"], f"{n} {u}")

    # -- and the live scan must actually read the tree --
    total, undoc, wild, pos, hier = audit()
    ck("the live scan reads the tree", total > 500, f"{total} ports")
    ck("the exclusion list is shared with lint_rtl", "hdl/milan/milan_top.sv" in LINT_EXCLUDE)

    n = 17
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="per-file undocumented counts")
    ap.add_argument("--selftest", action="store_true", help="run the mutation arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    total, undoc, wild, pos, hier = audit()
    count = sum(len(v) for v in undoc.values())
    bad = 0

    for rel, _off in wild:
        bad += 1
        print(f"WILDCARD BINDING: {rel} uses `.*`. Adding a port to the child "
              f"would rewire this instance with no diff here.")
    for rel, name, inst, line in pos:
        bad += 1
        print(f"POSITIONAL BINDING: {rel}:{line} instantiates {name} as {inst} "
              f"by position. Reordering the child's ports would rewire it silently.")
    for rel, inst, member, line in hier:
        bad += 1
        print(f"HIERARCHICAL DEPENDENCY: {rel}:{line} reads `{inst}.{member}`. "
              f"Production dependencies cross the module boundary through a named port.")

    if args.list:
        for rel in sorted(undoc, key=lambda r: -len(undoc[r])):
            print(f"  {len(undoc[rel]):>4} undocumented  {rel}")
        print()

    budget = read_budget()
    if budget is None:
        print(f"NO RATCHET: {BUDGET.relative_to(REPO)} is missing or unreadable")
        return 1
    if count > budget:
        print(f"PORT-DOC RATCHET: FAIL ({count} undocumented > ratchet {budget}). "
              f"A new port carries its `//!` contract.")
        bad += 1
    if bad:
        return 1

    print(f"port contract gate: OK ({total} first-party port(s), {count} "
          f"undocumented <= ratchet {budget}; 0 wildcard, 0 positional, "
          f"0 hierarchical binding)")
    if count < budget:
        print(f"  the ratchet can be lowered to {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
