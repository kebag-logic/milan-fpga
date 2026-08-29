#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mechanical hygiene: the objective checks, measured before any was adopted.

Why this exists. Rule 9 of the maintainability guide
(docs/development/CODE_QUALITY.md) says let pinned tools enforce objective,
mechanical rules - and measure signal and false positives BEFORE gating, so a
new baseline does not bury real findings or start a fight with the house style.

WHAT IS MEASURED. Five adopted checks and one rejected candidate, over the
first-party files of this superproject and both project-owned processor
submodules: every tracked file with a suffix in SCANNED_SUFFIXES or a name in
SCANNED_NAMES, outside EXCLUDED_PREFIXES, minus the generated files (below).
Markdown is deliberately outside the population: a Markdown hard line break IS
two trailing spaces, so the check would fight the format. `--measure` prints
the table for the tree it runs on; this is its output at the head that carries
this docstring, after the repair commits - 646 files (487 in this repository,
130 in protocol-processor, 29 in gptp-processor), 15 generated files skipped,
about 0.4 s, so runtime rejected nothing:

  | Candidate | Findings | Files | Verdict |
  |---|---:|---:|---|
  | Line over 100 columns | 1204 | 179 | rejected |
  | Trailing whitespace | 1 | 1 | adopted |
  | Missing EOF newline | 0 | 0 | adopted |
  | CRLF line ending | 0 | 0 | adopted at zero |
  | UTF-8 BOM | 0 | 0 | adopted at zero |
  | Tab in SystemVerilog | 0 | 0 | adopted at zero |

Before the repair commits the same scanner counted 44 trailing-whitespace lines
in 17 files (43 in 16 files of this repository, 1 in protocol-processor) and 15
files without a final newline. Every one in this repository was repaired; the
one that remains is protocol-processor/tb/nvm_port/measure_figures.py:206, and
it is that repository's to fix.

WHY THE LINE-LENGTH CHECK IS REJECTED, on the record. It is the highest-volume
candidate and it fights two deliberate house rules. `$error` takes later
arguments as VALUES, so an elaboration message MUST be one string literal -
hdl/milan/milan_datapath.sv:808 and hdl/ieee8021q/filtering/rx_mac_filter.sv:120
carry the note saying so, and every one of those messages is over 100 columns
by construction. The curated source lists in `syn/yosys/run.sh` and
`syn/yosys/ooc.sh` are single lines by design, because a line continuation is
what let a shell comment silently shrink one of them (recorded in
`syn/ooc/dp_srcs.py`). Wrapping either would trade a real property for a
cosmetic one. Rejected, not deferred - and still measured by `--measure`, so the
number above can be regenerated: a line counts when its text, without its line
ending, is longer than LINE_LENGTH_LIMIT characters after UTF-8 decoding (a tab
counts as one character).

The three zero-population checks are adopted BECAUSE they are at zero: holding
a clean property at zero costs nothing, and each carries an arm proving it
bites, so it cannot be an empty gate nobody notices. Makefiles and `.xdc`
constraints are in the population for the four byte checks; the tab check
looks only at .sv/.svh, because in a makefile a tab IS the syntax.

TRAILING WHITESPACE is a NON-BLANK line ending in spaces or tabs. A line that is
only spaces or tabs is an indented blank line - layout, not debt - so it is
neither counted nor repaired; this count and `git diff --check`, whose
blank-at-eol rule flags those lines too, disagree by exactly that class.

GENERATED AND VENDORED SOURCES ARE EXCLUDED. The phrases and the line window are
imported from `scripts/gen_toc.py`, which owns what "generated" means. One
tightening applies to code and not to Markdown: here the banner must be a
COMMENT line that leads with the phrase (see BANNER_RE). A Markdown page
announces its banner as visible prose (**GENERATED**), so gen_toc must match
prose; a code file's prose is its docstring, and a docstring that quotes another
file's banner is not a banner - scripts/check_results_fresh.py was silently
exempt from this gate by exactly that sentence until the R2 review of #283
found it. The skipped list is printed in full, so an exemption is never
invisible.

ONE RATCHET PER POPULATION. scripts/hygiene.budget carries a section for this
repository and one per processor, and --check compares each against its own.
A pinned processor's debt is held in its own section, so it can never free a
slot for a new finding here (R2 of #283); neither processor runs a hygiene
check of its own, so new processor debt is first seen here, at the pin bump
that brings it. The pin refusal in code_quality_scope looks at a submodule's
HEAD only: a working-tree edit inside a pinned checkout is scanned as-is.

THE FIXER operates on bytes. A byte that is not UTF-8 comes out exactly as it
went in, and a file is written only when a finding in it was repaired. It
refuses processor-submodule paths (their repair is upstream), and it REPORTS
every repaired line that lies inside a string literal (a Python triple-quoted
string, or a line whose double quotes do not balance) or in a make variable's
value, as far as a simple scan can tell: whitespace there is a value, so
stripping it is a content change the reviewer must read as one.

Usage:
    python3 scripts/check_hygiene.py            # the findings, per population
    python3 scripts/check_hygiene.py --check    # the ratchets CI runs
    python3 scripts/check_hygiene.py --fix      # repair the mechanical ones
    python3 scripts/check_hygiene.py --measure  # the six-candidate table
    python3 scripts/check_hygiene.py --selftest # fixture arms

Exit 0 = every population at or under its ratchets in scripts/hygiene.budget.
Exit 1 = a finding over its ratchet, a missing ratchet, or a repair that only
the owning repository can make. Exit 2 = an unusable population: a processor
submodule off its pin, or a population with no file in it.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "hygiene.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: what "generated" means is OWNED by gen_toc.py; a second definition here
#: would be exactly the drift Rule 3 forbids
from gen_toc import GENERATED_RE, GENERATED_SCAN_LINES
from code_quality_scope import PROJECT_SUBMODULES, tracked

SCANNED_SUFFIXES = (".sv", ".svh", ".v", ".py", ".cpp", ".h", ".hpp", ".c",
                    ".sh", ".tcl", ".mk", ".xdc", ".yml", ".yaml")
#: scanned by name, not suffix; a makefile is judged by the four byte checks
#: and never by the tab check
SCANNED_NAMES = ("Makefile",)
EXCLUDED_PREFIXES = ("third_party/", "external/", "gen/", "build/")
#: the budget sections, in report order: this repository, then each processor
POPULATIONS = ("superproject",) + PROJECT_SUBMODULES
LINE_LENGTH_LIMIT = 100
BOM = b"\xef\xbb\xbf"

#: name -> (fixable, description). Order is the report order.
CHECKS = (
    ("trailing whitespace", True, "a non-blank line ending in spaces or tabs"),
    ("missing EOF newline", True, "a file whose last line has no newline"),
    ("CRLF line ending", True, "a carriage return before a newline"),
    ("UTF-8 BOM", True, "a byte-order mark at the start of a source file"),
    ("tab in SystemVerilog", False, "a tab character in .sv/.svh (house style is 2 spaces)"),
)
CHECK_NAMES = tuple(name for name, _f, _d in CHECKS)

#: The six candidates in the order the guide's table quotes them, with the
#: verdict recorded when they were measured. Three were at zero before any
#: repair; the line-length candidate is measured but not gated.
CANDIDATES = (
    ("Line over 100 columns", "rejected"),
    ("trailing whitespace", "adopted"),
    ("missing EOF newline", "adopted"),
    ("CRLF line ending", "adopted at zero"),
    ("UTF-8 BOM", "adopted at zero"),
    ("tab in SystemVerilog", "adopted at zero"),
)

#: A banner is a COMMENT line - shebang, `#`, `//`, `--`, `*`, `/*`, `<!--`,
#: `;` - and the phrase LEADS it: at most BANNER_LEAD_WORDS words may stand
#: before it. Measured on this tree: every real banner leads with no word at
#: all except the Vivado block design's `# This is a generated script based on
#: design` (3), and the one comment that mentions generation mid-sentence,
#: bd/milan-dma.tcl line 5, leads with 6. The docstring sentence that exempted
#: scripts/check_results_fresh.py is not a comment line at all.
COMMENT_LEAD_RE = re.compile(r"^\s*(?:#!?|//!?|--|/\*+|\*|<!--|;)\s*")
BANNER_LEAD_WORDS = 3
BANNER_RE = re.compile(
    r"^(?:\S+\s+){0,%d}(?:%s)" % (BANNER_LEAD_WORDS, GENERATED_RE.pattern), re.I)

#: What `--fix` reports as a content change rather than formatting: the
#: whitespace it stripped was part of a value. Double quotes only - an
#: apostrophe in a comment would report every contraction - counted after
#: Python's triple quotes are removed; a shell `"..."` may run on to the next
#: line, so there the state is carried across lines. A make variable keeps its
#: trailing whitespace in GNU make (`dir := /foo/bar   ` is the manual's own
#: warning). A shell heredoc is not recognised.
TRIPLE_RE = re.compile(rb'"""|\'\'\'')
DQUOTE_RE = re.compile(rb'(?<!\\)"')
MAKE_ASSIGN_RE = re.compile(rb"^ *[^#\s=:][^=]*?[:+?!]?=")

SECTION_RE = re.compile(r"^#\s*---\s*section\s+(\S+)")


def is_generated(raw):
    """A generated file announces itself in a comment banner within the first lines."""
    for line in raw.decode("latin-1").splitlines()[:GENERATED_SCAN_LINES]:
        lead = COMMENT_LEAD_RE.match(line)
        if lead and BANNER_RE.match(line[lead.end():]):
            return True
    return False


def in_scope(rel):
    name = rel.rsplit("/", 1)[-1]
    return ((rel.endswith(SCANNED_SUFFIXES) or name in SCANNED_NAMES)
            and not rel.startswith(EXCLUDED_PREFIXES))


def sources():
    patterns = [f"*{s}" for s in SCANNED_SUFFIXES] + [f"*{n}" for n in SCANNED_NAMES]
    return [p for p in tracked(*patterns) if in_scope(p)]


def read_tree(lister=sources):
    """[(path, bytes)] for the whole population; refuses an off-pin processor."""
    return [(rel, (REPO / rel).read_bytes()) for rel in lister()]


def load_tree(lister=sources):
    """The tree, or the refusal message when a processor is not at its pin."""
    try:
        return read_tree(lister), None
    except RuntimeError as exc:                # code_quality_scope's pin refusal
        return None, str(exc)


def is_project_submodule_path(rel):
    """Whether a finding must be repaired in the owning submodule repository."""
    return rel.startswith(tuple(f"{name}/" for name in PROJECT_SUBMODULES))


def population_of(rel):
    """The budget section a path is judged against."""
    return rel.split("/", 1)[0] if is_project_submodule_path(rel) else "superproject"


def has_trailing_ws(line):
    """`line` is one `\\n`-split segment; a CRLF file's segments end in `\\r`."""
    body = line.rstrip(b"\r")
    return bool(body.strip(b" \t")) and body != body.rstrip(b" \t")


def judges_tabs(path):
    return path.endswith((".sv", ".svh"))


def scan_bytes(raw, path="x.sv"):
    """Return {check_name: count} for one file's bytes."""
    found = dict.fromkeys(CHECK_NAMES, 0)
    if not raw or is_generated(raw):
        return found
    found["UTF-8 BOM"] = int(raw.startswith(BOM))
    found["CRLF line ending"] = int(b"\r\n" in raw)
    found["missing EOF newline"] = int(not raw.endswith(b"\n"))
    lines = raw.split(b"\n")
    found["trailing whitespace"] = sum(1 for l in lines if has_trailing_ws(l))
    if judges_tabs(path):
        found["tab in SystemVerilog"] = sum(1 for l in lines if b"\t" in l)
    return found


def line_length_findings(raw):
    """The rejected candidate: lines longer than LINE_LENGTH_LIMIT characters."""
    text = raw.decode("utf-8", "replace")
    return sum(1 for l in text.split("\n") if len(l.rstrip("\r")) > LINE_LENGTH_LIMIT)


def fix_bytes(raw):
    """Repair the four fixable findings on the bytes themselves.

    Nothing is decoded: a byte that is not UTF-8 is not this gate's business
    and comes out exactly as it went in. With nothing to repair the bytes come
    back equal, which is how the caller knows not to write.
    """
    if raw.startswith(BOM):
        raw = raw[len(BOM):]
    raw = raw.replace(b"\r\n", b"\n")
    raw = b"\n".join(l.rstrip(b" \t") if l.strip(b" \t") else l
                     for l in raw.split(b"\n"))
    if raw and not raw.endswith(b"\n"):
        raw += b"\n"
    return raw


def content_risks(rel, old, new):
    """[(line, reason)] for each repaired line whose whitespace was a value."""
    name = rel.rsplit("/", 1)[-1]
    is_py = rel.endswith(".py")
    quote_spans_lines = rel.endswith(".sh")
    is_make = name in SCANNED_NAMES or rel.endswith(".mk")
    before = old[len(BOM):] if old.startswith(BOM) else old
    risks, in_triple, in_quote = [], False, False
    for n, (a, b) in enumerate(zip(before.replace(b"\r\n", b"\n").split(b"\n"),
                                   new.split(b"\n")), 1):
        if is_py and len(TRIPLE_RE.findall(a)) % 2:
            in_triple = not in_triple
        odd = len(DQUOTE_RE.findall(TRIPLE_RE.sub(b"", a))) % 2
        if quote_spans_lines and odd:
            in_quote = not in_quote
        if a == b:
            continue
        if in_triple:
            risks.append((n, "inside a triple-quoted string"))
        elif in_quote or (odd and not quote_spans_lines):
            risks.append((n, "inside a string literal"))
        elif is_make and MAKE_ASSIGN_RE.match(a):
            risks.append((n, "the value of a make variable"))
    return risks


def fix_tree(files, write):
    """Repair every (path, bytes) that has a fixable finding.

    `write(path, bytes)` is called only for a repaired file of this repository;
    a processor path is returned for an upstream fix instead. Returns
    (repaired paths, upstream paths, [(path, line, reason)] content risks).
    """
    repaired, upstream, risks = [], [], []
    for rel, raw in files:
        if not raw or is_generated(raw):
            continue
        new = fix_bytes(raw)
        if new == raw:
            continue
        if is_project_submodule_path(rel):
            upstream.append(rel)
            continue
        risks.extend((rel, n, why) for n, why in content_risks(rel, raw, new))
        write(rel, new)
        repaired.append(rel)
    return repaired, upstream, risks


def audit_files(files):
    """(totals by population, per-file findings, skipped paths, files by population)."""
    totals = {pop: dict.fromkeys(CHECK_NAMES, 0) for pop in POPULATIONS}
    sizes = dict.fromkeys(POPULATIONS, 0)
    per_file, skipped = {}, []
    for rel, raw in files:
        sizes[population_of(rel)] += 1
        if raw and is_generated(raw):
            skipped.append(rel)
            continue
        found = scan_bytes(raw, rel)
        if any(found.values()):
            per_file[rel] = found
        for name, count in found.items():
            totals[population_of(rel)][name] += count
    return totals, per_file, skipped, sizes


def measure(files):
    """{candidate: [findings, files]} - the table Rule 9 quotes."""
    rows = {name: [0, 0] for name, _verdict in CANDIDATES}
    for rel, raw in files:
        if not raw or is_generated(raw):
            continue
        found = scan_bytes(raw, rel)
        found["Line over 100 columns"] = line_length_findings(raw)
        for name, count in found.items():
            if count:
                rows[name][0] += count
                rows[name][1] += 1
    return rows


def read_budget(text=None):
    """{population: {check: limit}} from the sectioned budget file."""
    if text is None:
        if not BUDGET.is_file():
            return {}
        text = BUDGET.read_text()
    out, section = {}, None
    for line in text.splitlines():
        header = SECTION_RE.match(line)
        if header:
            section = out.setdefault(header.group(1), {})
            continue
        line = line.split("#", 1)[0].strip()
        if "=" in line and section is not None:
            k, v = line.split("=", 1)
            if v.strip().isdigit():
                section[k.strip()] = int(v.strip())
    return out


def compare(totals, budget):
    """The --check verdicts: empty when every population is within its own section."""
    bad = []
    for pop in POPULATIONS:
        section = budget.get(pop, {})
        for name in CHECK_NAMES:
            limit = section.get(name)
            if limit is None:
                bad.append(f"NO RATCHET for {name!r} in section {pop} of "
                           f"{BUDGET.relative_to(REPO)}")
            elif totals[pop][name] > limit:
                bad.append(f"FAIL: {pop}: {name} {totals[pop][name]} > ratchet {limit}")
    return bad


def partial(sizes):
    """The refusal for a population with no file in it; None when all are populated."""
    empty = [pop for pop in POPULATIONS if not sizes[pop]]
    if empty:
        return (f"REFUSED: no first-party file in {', '.join(empty)} - a partial "
                "population must never establish a baseline")
    return None


def selftest():
    failures = run = 0

    def ck(name, ok, detail=""):
        nonlocal failures, run
        run += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    zeros = dict.fromkeys(CHECK_NAMES, 0)

    # -- the scanner ---------------------------------------------------------
    ck("trailing whitespace is caught",
       scan_bytes(b"int x;   \n")["trailing whitespace"] == 1)
    ck("a trailing tab is trailing whitespace too",
       scan_bytes(b"int x;\t\n")["trailing whitespace"] == 1)
    ck("a whitespace-only line is not trailing whitespace",
       scan_bytes(b"a\n   \nb\n")["trailing whitespace"] == 0,
       "an indented blank line is layout, not a finding")
    ck("a missing EOF newline is caught",
       scan_bytes(b"int x;")["missing EOF newline"] == 1)
    ck("a present EOF newline is not", scan_bytes(b"int x;\n")["missing EOF newline"] == 0)
    ck("CRLF is caught", scan_bytes(b"a\r\nb\n")["CRLF line ending"] == 1)
    ck("a BOM is caught", scan_bytes(b"\xef\xbb\xbfa\n")["UTF-8 BOM"] == 1)
    ck("a tab in SystemVerilog is caught",
       scan_bytes(b"\tx <= 1;\n", "a.sv")["tab in SystemVerilog"] == 1)
    ck("the line-length candidate counts the 101st character, not a tab's width",
       line_length_findings(b"x" * 101 + b"\n" + b"x" * 100 + b"\n" + b"\t" * 50 + b"\n") == 1)

    # -- generated means a comment banner, not a sentence about one ----------
    ck("a Vivado block-design banner marks a generated file",
       scan_bytes(b"# This is a generated script based on design: x\nint y;   ") == zeros)
    ck("a docstring that quotes a banner is not a banner",
       scan_bytes(b'"""Gate: freshness.\n\nThe file says "GENERATED by x - do not '
                  b'hand-edit" because it is generated.\n"""\ny = 1   \n',
                  "a.py")["trailing whitespace"] == 1,
       "prose about another file's banner exempted scripts/check_results_fresh.py")
    ck("a comment that reaches the phrase mid-sentence is prose",
       scan_bytes(b"# Though there are limitations about the generated script,\n"
                  b"int y;   \n", "a.tcl")["trailing whitespace"] == 1)

    # -- the fixer repairs exactly what the scanner reports, on bytes --------
    dirty = b"\xef\xbb\xbfint x;   \r\nint y;\t \r\nint z;"
    clean = fix_bytes(dirty)
    ck("the fixer clears every mechanical finding",
       all(v == 0 for v in scan_bytes(clean).values()), f"{scan_bytes(clean)}")
    ck("the fixer preserves the content",
       clean == b"int x;\nint y;\nint z;\n", f"{clean!r}")
    ck("the fixer is idempotent", fix_bytes(clean) == clean)
    latin1 = b"// caf\xe9 au lait   \nint x;\n"
    ck("a byte that is not UTF-8 comes out exactly as it went in",
       fix_bytes(latin1) == b"// caf\xe9 au lait\nint x;\n", f"{fix_bytes(latin1)!r}")
    writes = []
    fix_tree([("hdl/a.sv", b"// caf\xe9\nint x;\n")], lambda rel, new: writes.append((rel, new)))
    ck("a file with no finding is not rewritten", writes == [], f"{writes}")
    writes = []
    repaired, upstream, risks = fix_tree(
        [("protocol-processor/hdl/a.sv", b"int x;   \n")],
        lambda rel, new: writes.append((rel, new)))
    ck("a project-submodule file is reported upstream and never written",
       writes == [] and upstream == ["protocol-processor/hdl/a.sv"] and not repaired,
       f"{writes} {upstream} {repaired}")
    writes = []
    repaired, upstream, risks = fix_tree(
        [("sw/a.py", b's = """line one  \nline two"""\n')],
        lambda rel, new: writes.append((rel, new)))
    ck("a repaired line inside a triple-quoted string is reported as content",
       writes == [("sw/a.py", b's = """line one\nline two"""\n')]
       and risks == [("sw/a.py", 1, "inside a triple-quoted string")], f"{writes} {risks}")
    ck("whitespace after a closing quote is formatting",
       content_risks("sw/a.py", b's = "done"   \nt = """a\nb"""  \n',
                     b's = "done"\nt = """a\nb"""\n') == [])
    ck("a repaired line whose quotes do not balance is reported",
       content_risks("hdl/a.sv", b'$display("a  \n', b'$display("a\n')
       == [(1, "inside a string literal")])
    ck("a make variable's value is reported, a make comment is not",
       content_risks("tb/x/Makefile", b"FOO = bar   \n# note   \n", b"FOO = bar\n# note\n")
       == [(1, "the value of a make variable")])

    # -- one ratchet per population ------------------------------------------
    budget = {pop: dict(zeros) for pop in POPULATIONS}
    budget["protocol-processor"]["trailing whitespace"] = 1
    totals, _pf, _sk, _sz = audit_files([("hdl/a.sv", b"int x;   \n"),
                                         ("protocol-processor/hdl/b.sv", b"int y;\n"),
                                         ("gptp-processor/hdl/c.sv", b"int z;\n")])
    ck("a superproject finding does not ride in a processor's free slot",
       compare(totals, budget) == ["FAIL: superproject: trailing whitespace 1 > ratchet 0"],
       f"{compare(totals, budget)}")
    totals, _pf, _sk, _sz = audit_files([("hdl/a.sv", b"int x;\n"),
                                         ("protocol-processor/hdl/b.sv", b"int y;   \n"),
                                         ("gptp-processor/hdl/c.sv", b"int z;\n")])
    ck("a processor finding at its own ratchet passes", compare(totals, budget) == [])
    ck("a budget without a population's section is a missing ratchet",
       any(v.startswith("NO RATCHET") and "gptp-processor" in v
           for v in compare(totals, {p: b for p, b in budget.items() if p != "gptp-processor"})))
    ck("a population with no file is refused",
       partial({"superproject": 3, "protocol-processor": 0, "gptp-processor": 1}) is not None
       and partial({pop: 1 for pop in POPULATIONS}) is None)
    def off_pin():
        raise RuntimeError("off pin")
    tree, why = load_tree(off_pin)
    ck("a processor off its pin is refused before anything is read",
       tree is None and why == "off pin", f"{tree!r} {why!r}")

    # -- the live tree ---------------------------------------------------------
    tree = read_tree()
    totals, per_file, skipped, sizes = audit_files(tree)
    ck("the live scan reads the tree", len(tree) > 100, f"{len(tree)} files")
    ck("the live scan reaches both project processor submodules",
       all(sizes[pop] > 0 for pop in PROJECT_SUBMODULES), f"{sizes}")
    ck("generated files are actually being skipped", bool(skipped),
       "nothing was skipped - the generated predicate is not firing")
    ck("the hand-written gate the R2 review found exempt is scanned",
       "scripts/check_results_fresh.py" in dict(tree)
       and "scripts/check_results_fresh.py" not in skipped)
    makefile = next((rel for rel, _raw in tree if rel.rsplit("/", 1)[-1] == "Makefile"), None)
    ck("a tab in a tracked makefile is not judged",
       makefile is not None and scan_bytes(b"\tx <= 1;\n", makefile)["tab in SystemVerilog"] == 0,
       "a tab IS the syntax there")
    ck("a CRLF in that makefile is",
       makefile is not None and scan_bytes(b"x\r\n", makefile)["CRLF line ending"] == 1)
    xdc = next((rel for rel, _raw in tree if rel.endswith(".xdc")), None)
    ck("trailing whitespace in a tracked .xdc is caught",
       xdc is not None and scan_bytes(b"# x   \n", xdc)["trailing whitespace"] == 1,
       "the constraints are in the population")
    ck("the budget carries every population",
       all(set(read_budget().get(pop, {})) >= set(CHECK_NAMES) for pop in POPULATIONS),
       f"{sorted(read_budget())}")

    print(f"\n{run} checks: {run - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet every check, per population")
    ap.add_argument("--fix", action="store_true", help="repair the mechanical findings")
    ap.add_argument("--measure", action="store_true",
                    help="the six-candidate table, the rejected line-length one included")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    tree, why = load_tree()
    if tree is None:
        print(f"REFUSED: {why}")
        return 2
    totals, per_file, skipped, sizes = audit_files(tree)
    refusal = partial(sizes)
    if refusal:
        print(refusal)
        return 2

    if args.fix:
        repaired, upstream, risks = fix_tree(
            tree, lambda rel, new: (REPO / rel).write_bytes(new))
        for rel in repaired:
            print(f"fixed {rel}")
        for rel in upstream:
            print(f"needs upstream fix in project submodule: {rel}")
        for rel, line, reason in risks:
            print(f"content change, not formatting: {rel}:{line} ({reason})")
        print(f"\n{len(repaired)} file(s) repaired. A tab in SystemVerilog is NOT fixed "
              "automatically: re-indenting is a judgement about layout.")
        if risks:
            print(f"{len(risks)} repaired line(s) sit inside a string literal or a make "
                  "variable's value; review each as a content change, not formatting.")
        if upstream:
            print(f"{len(upstream)} project-submodule file(s) were not rewritten; "
                  "repair them in their owning repository and update the pin.")
        return 1 if upstream else 0

    if args.measure:
        rows = measure(tree)
        print(f"{len(tree)} first-party file(s): "
              + ", ".join(f"{pop} {sizes[pop]}" for pop in POPULATIONS)
              + f"; {len(skipped)} generated file(s) skipped. A line is over "
              f"{LINE_LENGTH_LIMIT} columns when its text, without its line ending, "
              f"is longer than {LINE_LENGTH_LIMIT} characters after UTF-8 decoding.\n")
        print("| Candidate | Findings | Files | Verdict |")
        print("|---|---:|---:|---|")
        for name, verdict in CANDIDATES:
            print(f"| {name[0].upper() + name[1:]} | {rows[name][0]} | {rows[name][1]} | {verdict} |")
        return 0

    for rel in sorted(per_file):
        bits = ", ".join(f"{k} x{v}" for k, v in per_file[rel].items() if v)
        print(f"{rel}: {bits}")

    print(f"\n{len(tree)} first-party file(s) scanned: "
          + ", ".join(f"{pop} {sizes[pop]}" for pop in POPULATIONS))
    print(f"{len(skipped)} generated file(s) skipped, their fix is in their generator:")
    for rel in skipped:
        print(f"  {rel}")
    width = max(len(pop) for pop in POPULATIONS)
    print("\n  " + " " * 24 + "  ".join(f"{pop:>{width}}" for pop in POPULATIONS))
    for name in CHECK_NAMES:
        print(f"  {name:<24}" + "  ".join(f"{totals[pop][name]:>{width}}" for pop in POPULATIONS))

    if not args.check:
        return 0

    verdicts = compare(totals, read_budget())
    if verdicts:
        print()
        for line in verdicts:
            print(line)
        return 1
    budget = read_budget()
    print()
    for pop in POPULATIONS:
        print(f"  {pop}: " + ", ".join(
            f"{name} {totals[pop][name]}<={budget[pop][name]}" for name in CHECK_NAMES))
    print(f"HYGIENE RATCHET: PASS ({len(POPULATIONS)} population(s), {len(tree)} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
