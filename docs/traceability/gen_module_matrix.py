#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Generate the per-module spec-traceability matrix from repo ground truth.

Roadmap item-3 subtask (per-module spec-test traceability), item-4 (README-
tests merged with the matrix, "one doc, no drift") and item-10 (the
peer-validation substrate) all want the SAME artifact: for every RTL module,
which spec family/clause it implements and which test exercises it — with
coverage gaps visible. Hand-authored, that drifts the moment a module or a
testbench moves; so it is GENERATED here from four ground-truth sources:

  1. the RTL tree            hdl/**/*.sv  ->  module name + spec family (path)
  2. the testbench tree      tb/verilator/*/Makefile  ->  which .sv it compiles
  3. the field campaign      tb/verilator/tsn_fuzz     ->  which families it fuzzes
  4. the clause matrices     docs/traceability/*.md    ->  clause refs per module

Outputs (regenerate on any tree change; that is the no-drift contract):

  * docs/traceability/MODULE_MATRIX.md      the rolled-up top index
  * hdl/<family>/<leaf>/README-tests.md     per spec-family-leaf index

Run:  python3 docs/traceability/gen_module_matrix.py [--check]
      --check exits non-zero if the generated files are stale (for CI).
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HDL = os.path.join(ROOT, "hdl")
TBDIR = os.path.join(ROOT, "tb", "verilator")
TRACE = os.path.join(ROOT, "docs", "traceability")

#: spec family (first path component under hdl/) -> human name + standard
FAMILY = {
    "ieee17221": ("IEEE 1722.1 (ATDECC)", "ADP / ACMP / AECP-AEM-MVU"),
    "ieee1722": ("IEEE 1722 (AVTP)", "AAF / CRF / MAAP / AVTP common"),
    "ieee8021q": ("IEEE 802.1Q", "TS/CBS shaping · SRP/MRP · VLAN/TCAM filtering"),
    "ieee8021as": ("IEEE 802.1AS", "gPTP timestamping / pdelay / sync"),
    "common": ("Common / integration", "CSR, CDC, RMON, utilities"),
    "milan": ("Milan (Avnu) integration", "datapath + top wrappers"),
}
#: tsn_fuzz field campaigns by the leaf dir they principally cover
FUZZ_LEAF = {"aecp": "make aecp", "acmp": "make acmp", "adp": "make adp",
             "avtp": "make aaf", "aaf": "make aaf"}


def rtl_modules():
    """[(family, leaf, relpath, module_or_pkg, is_pkg)] for every hdl .sv."""
    out = []
    for dirpath, _dirs, files in os.walk(HDL):
        for fn in sorted(files):
            if not fn.endswith(".sv"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            parts = os.path.relpath(path, HDL).split(os.sep)
            family = parts[0]
            leaf = parts[1] if len(parts) > 2 else parts[0]
            txt = open(path, errors="ignore").read()
            m = re.search(r"^\s*module\s+(\w+)", txt, re.M)
            p = re.search(r"^\s*package\s+(\w+)", txt, re.M)
            if m:
                out.append((family, leaf, rel, m.group(1), False))
            elif p:
                out.append((family, leaf, rel, p.group(1), True))
    return out


def tb_index():
    """basename(.sv) -> sorted set of tb/verilator dirs that compile it."""
    idx = {}
    if not os.path.isdir(TBDIR):
        return idx
    for tb in sorted(os.listdir(TBDIR)):
        mk = os.path.join(TBDIR, tb, "Makefile")
        if not os.path.isfile(mk):
            continue
        txt = open(mk, errors="ignore").read()
        for base in re.findall(r"([A-Za-z0-9_]+\.sv)", txt):
            idx.setdefault(base, set()).add(tb)
    return idx


def instantiation_edges(mods):
    """module -> set(known modules it instantiates or includes).

    Uses the KNOWN module-name set as the candidate list so a plain
    `\\bNAME #(` / `\\bNAME inst (` match cannot false-positive on a keyword
    or a function call — SV module names here are all specific (KL_*, adp_*,
    ...). Include directives (`include "x.sv"`) are followed too.
    """
    known = {name for _f, _l, _r, name, is_pkg in mods if not is_pkg}
    file_of = {}
    for _f, _l, rel, name, is_pkg in mods:
        if not is_pkg:
            file_of[name] = rel
    edges = {}
    inst_re = {m: re.compile(r"\b%s\s*(?:#\s*\(|\w+\s*\()" % re.escape(m)) for m in known}
    for name, rel in file_of.items():
        txt = open(os.path.join(ROOT, rel), errors="ignore").read()
        # strip line comments so a mention in a banner is not counted
        body = re.sub(r"//.*", "", txt)
        hit = set()
        for m in known:
            if m == name:
                continue
            if inst_re[m].search(body):
                hit.add(m)
        # `include "child.sv"` -> the module(s) that file defines
        for inc in re.findall(r'`include\s+"([^"]+\.sv)"', txt):
            base = os.path.basename(inc)
            for m2, r2 in file_of.items():
                if os.path.basename(r2) == base:
                    hit.add(m2)
        edges[name] = hit
    return edges


def coverage(mods, tbi):
    """Return (direct, exercised): module -> set(tb dirs).

    direct    = the module's own file is listed by that TB (focused coverage).
    exercised = reachable transitively from a direct module through the
                instantiation graph (compiled + simulated in that TB's design).
    """
    direct = {}
    for _f, _l, rel, name, is_pkg in mods:
        if is_pkg:
            continue
        tbs = tbi.get(os.path.basename(rel), set())
        if tbs:
            direct[name] = set(tbs)
    edges = instantiation_edges(mods)
    exercised = {k: set(v) for k, v in direct.items()}
    # propagate each TB down through what its directly-listed modules instantiate
    for root, tbs in direct.items():
        stack = [root]
        seen = {root}
        while stack:
            cur = stack.pop()
            for child in edges.get(cur, ()):
                exercised.setdefault(child, set()).update(tbs)
                if child not in seen:
                    seen.add(child)
                    stack.append(child)
    return direct, exercised


def clause_refs():
    """basename-token -> set of clause ids mentioned in the same matrix row."""
    refs = {}
    clause_re = re.compile(r"M-[A-Z]+-\d+|§?\d+\.\d+(?:\.\d+)*|7\.4\.\d+")
    for fn in os.listdir(TRACE):
        if not fn.endswith(".md") or fn == "MODULE_MATRIX.md":
            continue  # skip our own generated output (avoid self-pollution)
        for line in open(os.path.join(TRACE, fn), errors="ignore"):
            if not line.startswith("|"):
                continue
            mods = re.findall(r"`([A-Za-z0-9_]+)`", line)
            cls = clause_re.findall(line)
            if not mods or not cls:
                continue
            for mod in mods:
                refs.setdefault(mod, set()).update(cls[:3])
    return refs


def build():
    mods = rtl_modules()
    tbi = tb_index()
    refs = clause_refs()
    direct, exercised = coverage(mods, tbi)
    rows = []
    for family, leaf, rel, name, is_pkg in mods:
        base = os.path.basename(rel)
        dtbs = sorted(direct.get(name, set()))
        xtbs = sorted(exercised.get(name, set()) - direct.get(name, set()))
        fuzz = FUZZ_LEAF.get(leaf)
        cl = sorted(refs.get(name, set()) | refs.get(base.replace(".sv", ""), set()))
        if is_pkg:
            status = "pkg"
        elif dtbs:
            status = "direct"          # focused, dedicated testbench
        elif xtbs:
            status = "exercised"       # compiled+simulated in a broader TB only
        elif fuzz:
            status = "fuzz"
        else:
            status = "UNTESTED"
        rows.append(dict(family=family, leaf=leaf, rel=rel, name=name,
                         is_pkg=is_pkg, dtbs=dtbs, xtbs=xtbs, fuzz=fuzz,
                         clauses=cl, status=status))
    return rows


STATUS_GLYPH = {"direct": "✅", "exercised": "➰", "fuzz": "🔬",
                "pkg": "📦", "UNTESTED": "⚪"}


def _test_cell(r):
    parts = ["`%s`" % t for t in r["dtbs"]]
    if r["xtbs"]:
        parts.append("➰" + ",".join(r["xtbs"][:3]))
    if r["fuzz"]:
        parts.append("🔬`%s`" % r["fuzz"])
    return " · ".join(parts) or "—"


def render_top(rows):
    direct = sum(1 for r in rows if r["dtbs"])
    exok = sum(1 for r in rows if r["status"] == "exercised")
    fuzz = sum(1 for r in rows if r["fuzz"])
    unt = [r for r in rows if r["status"] == "UNTESTED"]
    mods = [r for r in rows if not r["is_pkg"]]
    out = ["<!--", "SPDX-FileCopyrightText: 2026 Kebag Logic",
           "SPDX-License-Identifier: CERN-OHL-W-2.0", "-->",
           "# Module ↔ spec ↔ test traceability matrix", "",
           "**GENERATED — do not hand-edit.** `python3 docs/traceability/gen_module_matrix.py`",
           "(regenerate on any RTL/TB tree change; `--check` gates staleness in CI).",
           "",
           "Every module in `hdl/` mapped to its spec family, the clause(s) it",
           "appears against in the clause matrices, and the testbench(es) that",
           "compile it. A module with no testbench is an **⚪ UNTESTED** row —",
           "that is the coverage gap this matrix exists to make visible.", "",
           "Legend: ✅ dedicated Verilator TB · ➰ exercised transitively in a "
           "broader TB's design · 🔬 in the tsn_fuzz field campaign · 📦 package "
           "· ⚪ not compiled by any TB.", "",
           "**Totals:** %d modules · %d with a dedicated TB · %d exercised-only · "
           "%d field-fuzzed · **%d not in any TB**"
           % (len(mods), direct, exok, fuzz, len(unt)), ""]
    if unt:
        out += ["## ⚪ Untested modules (the backlog)", ""]
        for r in sorted(unt, key=lambda r: r["rel"]):
            out.append("* `%s` — `%s`" % (r["name"], r["rel"]))
        out.append("")
    for fam in ["ieee17221", "ieee1722", "ieee8021q", "ieee8021as", "common", "milan"]:
        frows = [r for r in rows if r["family"] == fam]
        if not frows:
            continue
        title, blurb = FAMILY.get(fam, (fam, ""))
        out += ["## %s" % title, "", "_%s_" % blurb, "",
                "| module | file | test | clauses |", "|---|---|---|---|"]
        for r in sorted(frows, key=lambda r: (r["leaf"], r["rel"])):
            cl = ", ".join(r["clauses"][:4]) or "—"
            out.append("| %s `%s` | `%s` | %s | %s |"
                       % (STATUS_GLYPH[r["status"]], r["name"],
                          r["rel"].replace("hdl/", ""), _test_cell(r), cl))
        out.append("")
    return "\n".join(out) + "\n"


def render_leaf(fam, leaf, frows):
    title, _ = FAMILY.get(fam, (fam, ""))
    out = ["<!--", "SPDX-FileCopyrightText: 2026 Kebag Logic",
           "SPDX-License-Identifier: CERN-OHL-W-2.0", "-->",
           "# `%s/%s` — modules & test coverage" % (fam, leaf), "",
           "**GENERATED** by `docs/traceability/gen_module_matrix.py` — do not",
           "hand-edit. Part of the %s family; rolled up in" % title,
           "[`docs/traceability/MODULE_MATRIX.md`](../../../docs/traceability/MODULE_MATRIX.md).",
           "", "| module | file | test | clauses |", "|---|---|---|---|"]
    for r in sorted(frows, key=lambda r: r["rel"]):
        cl = ", ".join(r["clauses"][:4]) or "—"
        out.append("| %s `%s` | `%s` | %s | %s |"
                   % (STATUS_GLYPH[r["status"]], r["name"],
                      os.path.basename(r["rel"]), _test_cell(r), cl))
    out.append("")
    return "\n".join(out) + "\n"


def leaf_files(rows):
    """{abs_path: content} for every per-leaf README-tests.md."""
    groups = {}
    for r in rows:
        groups.setdefault((r["family"], r["leaf"]), []).append(r)
    files = {}
    for (fam, leaf), frows in groups.items():
        # leaf dir: hdl/<fam>/<leaf> unless leaf==fam (flat family like common/milan)
        d = os.path.join(HDL, fam) if leaf == fam else os.path.join(HDL, fam, leaf)
        files[os.path.join(d, "README-tests.md")] = render_leaf(fam, leaf, frows)
    return files


def main():
    check = "--check" in sys.argv
    rows = build()
    artifacts = {os.path.join(TRACE, "MODULE_MATRIX.md"): render_top(rows)}
    artifacts.update(leaf_files(rows))
    stale = []
    for path, content in artifacts.items():
        cur = open(path).read() if os.path.exists(path) else None
        if cur != content:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, "w").write(content)
    mods = [r for r in rows if not r["is_pkg"]]
    unt = [r for r in mods if r["status"] == "UNTESTED"]
    if check:
        if stale:
            print("STALE (run gen_module_matrix.py):")
            for s in stale:
                print("  " + s)
            return 1
        print("traceability matrix up to date (%d modules, %d untested)"
              % (len(mods), len(unt)))
        return 0
    print("wrote %d files · %d modules · %d untested: %s"
          % (len(artifacts), len(mods), len(unt),
             ", ".join(r["name"] for r in unt) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
