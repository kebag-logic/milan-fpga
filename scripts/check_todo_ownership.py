#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a marker in first-party code names the issue that owns it.

Why this exists. Rule 7 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a marker either names a concrete issue
or is resolved - it is not an untracked backlog. An unowned marker is worse
than no marker: it reads as a plan, nobody is accountable for it, and it
survives the change that made it wrong. `ptp_ts_top.sv` carried a marker
asking for DMA engine signals beside the three DMA streams the module already
declares (`s_axis_tx_*`, `m_axis_rx_*`, `ts_m_axis_*`), which Issue #53
records as present and only needing attachment.

WHAT IT MEASURES. Every tracked first-party file whose type has a comment
syntax registered in SYNTAX below is read, its comment text is extracted with
that syntax, and a comment carrying one of the marker words (WORDS, matched
without regard to case) immediately followed by `:`, `(` or `#` is a marker.
The one accepted owned form is the word followed by the owning issue in
parentheses - `TODO(#123)`; any other spelling (a bare colon, `#123` without
the parentheses, two issues in one pair, the issue after the colon) is
unowned. EVERY OCCURRENCE IS CLASSIFIED ON ITS OWN: the owner is the `(#N)`
immediately after ITS word, so a line carrying one owned marker and one bare
one is one owned marker and one unowned marker, not an owned line, and an
issue written BEFORE a word (`(#12) <word>: ...`) owns nothing - it is not
attached to the word by the contract's one form, and could as well close the
sentence before it. THE OWNER'S ISSUE NUMBER IS TAKEN ON TRUST: it is not
checked against the tracker, so a fabricated number passes, and `--list`
prints every owned marker under that caveat.

The word anywhere else is a NEAR-MISS, counted and printed by `--list` per
occurrence rather than silently dropped, so a reader can see what the
narrowing cost - a second word beside a marker on the same line is its own
near-miss, not part of the marker. The classes observed in this tree: a
citation of the historical task-list document; an IDENTIFIER in
`scripts/gen_toc.py` (the placeholder description that gate refuses) and every
comparison against it; prose about markers, this docstring and the CI step
name included. At the head this text was written against the gate printed
21 near-miss occurrences on 15 lines; the guide's Rule 7 and the CI step
comment carry the same numbers from the same run.

WHAT IS READ. The population is `code_quality_scope.tracked()`: the
superproject plus the two project-owned processor submodules, with the vendor
gitlinks (`third_party/`, `external/`) dropped, refusing an absent or off-pin
processor. Every file in it whose type is registered is read: RTL and its
headers, C/C++, Python, shell, Tcl with constraints and simulator scripts,
Makefiles, YAML, TOML, INI, Gherkin features, Verilator config and file lists,
and the git dotfiles.
Files in `scripts/lint_rtl.py`'s LINT_EXCLUDE are not: `hdl/milan/milan_top.sv`
is an archived Zynq top no build compiles, and its two markers (lines 329 and
751) are part of the archive, not of maintained code. Markdown is not scanned
at all - prose about a document whose name is one of these words is not a
marker - and `--list` prints the census of tracked types that are not read, so
the blind spots are visible instead of assumed away.

HOW COMMENTS ARE FOUND, and the one rule the extractor obeys: STRING STATE
NEVER CROSSES A LINE. The first version treated an apostrophe as a string
delimiter in SystemVerilog, so `1'b0` opened a "string" that swallowed every
comment up to the next apostrophe, however many lines later; a fifth of the
RTL comment surface was invisible and a hidden marker was printed as a
near-miss. Now only `"` delimits a SystemVerilog string; in C/C++ an
apostrophe opens a character literal only when it does not follow a word
character (`1'000` and `0x00A0'0000ull` are digit separators) and the literal
closes on its own line; in YAML, Makefiles and TOML an apostrophe inside a
word (`don't`) is prose; Tcl, .xdc and .do have no apostrophe quoting at all;
Python triple-quoted strings are tracked across lines so a marker-shaped
example inside a docstring is not a marker; Gherkin and INI comments are whole
lines. Block comments are the only other state carried across lines, so a
marker on a later line of `/* ... */` is caught. A misread quote can therefore
hide at most the rest of its own line, never the next one.

Usage:
    python3 scripts/check_todo_ownership.py            # gate
    python3 scripts/check_todo_ownership.py --list     # markers, near-misses, types read and not
    python3 scripts/check_todo_ownership.py --selftest # fixture arms

Exit 0 = every marker in gated first-party code names an issue.
Exit 1 = an unowned marker, printed as path:line:word, one per occurrence.
Exit 2 = REFUSED before any verdict: git is missing, a processor submodule is
         absent or off-pin, or the population has nothing from the
         superproject or from a processor. A partial population is never a pass.
"""

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE
from code_quality_scope import PROJECT_SUBMODULES, first_party, tracked

WORDS = "TODO|FIXME|XXX|HACK"
#: the marker shape: the word, then optional space, then `:`, `(` or `#`
MARKER = re.compile(r"\b(%s)\b\s*(?=[:(#])" % WORDS, re.IGNORECASE)
#: the one owned form: the word, then exactly one issue number in parentheses
OWNED = re.compile(r"\b(?:%s)\s*\(\s*#\d+\s*\)" % WORDS, re.IGNORECASE)
#: the word anywhere, for the near-miss inventory
ANY = re.compile(r"\b(%s)\b" % WORDS, re.IGNORECASE)


class Syntax(NamedTuple):
    """How one file type spells a comment, and what can hide one."""
    line: tuple        #: line-comment openers, to end of line
    block: tuple       #: (open, close) of a block comment carried across lines, or ()
    quotes: str        #: characters that always open a string, closed on the same line
    soft_quotes: str   #: characters that open a string only after a non-word character
    triple: tuple      #: multi-line string delimiters carried across lines (Python)
    whole_line: bool   #: a comment is a whole line whose first non-blank text is an opener


SV = Syntax(("//",), ("/*", "*/"), '"', "", (), False)
C = Syntax(("//",), ("/*", "*/"), '"', "'", (), False)
PY = Syntax(("#",), (), "\"'", "", ('"""', "'''"), False)
SHELL = Syntax(("#",), (), "\"'", "", (), False)
PROSE_HASH = Syntax(("#",), (), '"', "'", (), False)
TCL = Syntax(("#",), (), '"', "", (), False)
GHERKIN = Syntax(("#",), (), "", "", (), True)
INI = Syntax(("#", ";"), (), "", "", (), True)
FLIST = Syntax(("//", "#"), ("/*", "*/"), "", "", (), False)

#: comment syntax by suffix; a type absent here is not read, and `--list` says so
SYNTAX = {
    ".sv": SV, ".svh": SV, ".v": SV, ".vh": SV, ".vlt": SV,
    ".cpp": C, ".cc": C, ".cxx": C, ".c": C, ".h": C, ".hpp": C, ".hh": C,
    ".py": PY,
    ".sh": SHELL,
    ".yml": PROSE_HASH, ".yaml": PROSE_HASH, ".mk": PROSE_HASH,
    ".toml": PROSE_HASH, ".budget": PROSE_HASH,
    ".gitignore": PROSE_HASH, ".gitattributes": PROSE_HASH,
    ".tcl": TCL, ".xdc": TCL, ".do": TCL,
    ".feature": GHERKIN, ".ini": INI, ".gitmodules": INI,
    ".f": FLIST,
}
#: comment syntax by basename; `Containerfile.<flavour>` matches by its stem
NAMED = {"Makefile": PROSE_HASH, "Containerfile": SHELL}


def type_key(path):
    """The census key of `path`: a registered basename, else its suffix, else its name."""
    name = Path(path).name
    stem = name.split(".")[0]
    if stem in NAMED and (name == stem or name.startswith(stem + ".")):
        return stem
    if name.endswith(".example"):
        return Path(name[:-len(".example")]).suffix + ".example"
    return Path(name).suffix or name


def syntax_for(path):
    """The comment syntax of `path`, or None when its type is not read."""
    key = type_key(path)
    if key in NAMED:
        return NAMED[key]
    if key.endswith(".example"):
        key = key[:-len(".example")]
    return SYNTAX.get(key)


_TOKENS = {}


def _tokens(syn):
    """The regex that finds the next character sequence that matters in code."""
    if syn not in _TOKENS:
        parts = list(syn.line) + list(syn.block[:1]) + list(syn.triple)
        parts += list(syn.quotes) + list(syn.soft_quotes)
        parts = sorted(set(parts), key=len, reverse=True)
        _TOKENS[syn] = re.compile("|".join(re.escape(p) for p in parts))
    return _TOKENS[syn]


def _string_end(line, at, quote):
    """Index just past the string opened by `quote` at `at`, or the end of the line."""
    j = at + 1
    while j < len(line):
        if line[j] == "\\":
            j += 2
        elif line[j] == quote:
            return j + 1
        else:
            j += 1
    return len(line)


def _scan(line, syn, carried, spans):
    """Collect the comment spans of one line; return the state carried into the next.

    `carried` is None, "block" inside a block comment, or the delimiter of an
    open triple-quoted string. Nothing else survives the end of a line.
    """
    regex = _tokens(syn)
    i = 0
    while i < len(line):
        if carried == "block":
            close = syn.block[1]
            at = line.find(close, i)
            if at < 0:
                spans.append((i, len(line)))
                return "block"
            spans.append((i, at + len(close)))
            i, carried = at + len(close), None
            continue
        if carried:
            at = line.find(carried, i)
            if at < 0:
                return carried
            i, carried = at + len(carried), None
            continue
        found = regex.search(line, i)
        if not found:
            return None
        tok, at = found.group(0), found.start()
        if tok in syn.triple:
            i, carried = at + len(tok), tok
        elif tok in syn.line:
            spans.append((at, len(line)))
            return None
        elif syn.block and tok == syn.block[0]:
            spans.append((at, at + len(tok)))
            i, carried = at + len(tok), "block"
        elif (tok in syn.soft_quotes and at > 0
              and (line[at - 1].isalnum() or line[at - 1] == "_")):
            i = at + 1  # a digit separator or an apostrophe inside a word: code
        else:
            i = _string_end(line, at, tok)
    return carried


def comment_views(text, path):
    """The comment part of every line of `text`, split on newline, blanked elsewhere.

    Line N of the result is the comment text of line N of the file, character
    for character, so a match maps straight back to its source line.
    """
    syn = syntax_for(path)
    lines = text.split("\n")
    if syn is None:
        return [" " * len(line) for line in lines]
    views, carried = [], None
    for line in lines:
        spans = []
        if syn.whole_line:
            body = line.lstrip()
            if body.startswith(syn.line):
                spans.append((len(line) - len(body), len(line)))
        else:
            carried = _scan(line, syn, carried, spans)
        view = [" "] * len(line)
        for start, end in spans:
            view[start:end] = line[start:end]
        views.append("".join(view))
    return views


class Hit(NamedTuple):
    """One occurrence of a marker word, classified on its own."""
    line: int    #: 1-based line number
    kind: str    #: "owned", "unowned" or "near"
    word: str    #: the word as written
    text: str    #: the source line, stripped and clipped


def scan_text(text, path):
    """Every occurrence of a marker word in `text`, each classified on its own.

    A marker is owned by what follows ITS word - `(#N)` immediately after it -
    never by what appears elsewhere on the line. So one owned marker and one
    bare marker on a line are one owned and one unowned occurrence, and an
    issue written before a word owns nothing. The kind is read off the
    comment view at the word's own position; the view is character-aligned
    with the line, so a word in code is a near-miss and a word in a comment
    is judged by what the comment says right after it.
    """
    lines = text.split("\n")
    for n, (line, view) in enumerate(zip(lines, comment_views(text, path)), 1):
        for found in ANY.finditer(line):
            at = found.start()
            if MARKER.match(view, at):
                kind = "owned" if OWNED.match(view, at) else "unowned"
            else:
                kind = "near"
            yield Hit(n, kind, found.group(1), line.strip()[:92])


def scan_line(line, path="x.py"):
    """(is_marker, is_owned) for one line: is_owned only when EVERY marker on it is."""
    markers = [h for h in scan_text(line, path) if h.kind != "near"]
    if not markers:
        return False, False
    return True, all(h.kind == "owned" for h in markers)


def select(paths):
    """The paths this gate reads: a registered comment syntax, and not LINT_EXCLUDE."""
    return [p for p in paths if syntax_for(p) is not None and p not in LINT_EXCLUDE]


def scannable():
    return select(tracked())


def population_problem(paths):
    """Why `paths` is not a population this gate may judge, or None."""
    if not paths:
        return "the population is empty"
    for sub in PROJECT_SUBMODULES:
        if not any(p.startswith(sub + "/") for p in paths):
            return f"the population has nothing under {sub}/"
    if all(p.split("/", 1)[0] in PROJECT_SUBMODULES for p in paths):
        return "the population has nothing from the superproject"
    return None


def audit(paths=None):
    """(unowned, owned, near) as (path, line, word, text), one entry per occurrence."""
    unowned, owned, near = [], [], []
    for rel in (scannable() if paths is None else paths):
        text = (REPO / rel).read_text(errors="replace")
        for hit in scan_text(text, rel):
            {"unowned": unowned, "owned": owned, "near": near}[hit.kind].append(
                (rel, hit.line, hit.word, hit.text))
    return unowned, owned, near


def lines_of(hits):
    """How many distinct file lines the occurrences in `hits` fall on."""
    return len({(rel, n) for rel, n, _word, _text in hits})


def selftest():
    failures, total = 0, 0

    def ck(name, ok, detail=""):
        nonlocal failures, total
        total += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    def hits(text, path):
        """(line, kind, WORD) per occurrence, in file order."""
        return [(h.line, h.kind, h.word.upper()) for h in scan_text(text, path)]

    def kinds(text, path):
        """Line number -> kind, for fixtures with one occurrence per line."""
        found = hits(text, path)
        assert len({n for n, _k, _w in found}) == len(found), found
        return {n: kind for n, kind, _w in found}

    # THE MARKER WORDS ARE ASSEMBLED, NOT WRITTEN OUT. Not because the gate
    # would flag a spelled fixture - a fixture is a string literal, and the
    # extractor sees its quotes - but because the near-miss inventory counts
    # the word ANYWHERE in a scanned line and this file is scanned. Spelled
    # out, every fixture below would land in the inventory the gate prints
    # for the tree, and that inventory is about the tree. The first arm
    # proves the assembled words are the ones the matcher looks for.
    T = "TO" + "DO"
    F = "FIX" + "ME"
    ck("the assembled fixture words are the real marker words",
       all(MARKER.search(f"{w}:") and ANY.search(w) for w in (T, F)))

    ck("an unowned marker is caught",
       scan_line(f"  //{T}: add DMA signals", "a.sv") == (True, False))
    ck("an owned marker is accepted",
       scan_line(f"  //{T}(#53): attach the DMA streams", "a.sv") == (True, True))
    ck(f"{F} is a marker too", scan_line(f"  # {F}: broken", "a.py") == (True, False))
    ck(f"an owned {F} is accepted",
       scan_line(f"  # {F}(#7): broken", "a.py") == (True, True))
    ck("case does not matter",
       scan_line(f"  // {T.lower()}: injected", "a.sv") == (True, False)
       and scan_line(f"  // {F.capitalize()}(#7): x", "a.sv") == (True, True))
    ck("the word then #N is a marker, and not the owned form",
       scan_line(f"  // {T} #12 injected", "a.sv") == (True, False))
    ck("two issues in one pair, or the issue after the colon, is not the owned form",
       scan_line(f"  // {T}(#12, #13): x", "a.sv") == (True, False)
       and scan_line(f"  // {T}: (#12) x", "a.sv") == (True, False))
    ck("the owner issue number is taken on trust, not checked against the tracker",
       scan_line(f"  // {T}(#999999): x", "a.sv") == (True, True))

    # -- every occurrence on a line is classified on its own: an owner belongs
    # to the word it follows, and one owned marker does not launder its
    # neighbour (the P2 review finding on this gate) --
    mixed = f"// {T}(#123): first; {F}: second"
    ck("an owned marker beside an unowned one does not own it",
       hits(mixed, "a.sv") == [(1, "owned", T), (1, "unowned", F)]
       and scan_line(mixed, "a.sv") == (True, False), str(hits(mixed, "a.sv")))
    ck("nor in the other order",
       hits(f"// {F}: second; {T}(#123): first", "a.sv")
       == [(1, "unowned", F), (1, "owned", T)])
    ck("two owned markers on one line are both owned",
       hits(f"// {T}(#1): a; {F}(#2): b", "a.sv") == [(1, "owned", T), (1, "owned", F)]
       and scan_line(f"// {T}(#1): a; {F}(#2): b", "a.sv") == (True, True))
    ck("an issue written before its word owns nothing: the owner follows the word",
       hits(f"// (#123) {T}: x", "a.sv") == [(1, "unowned", T)]
       and hits(f"// #123 {T}: x", "a.sv") == [(1, "unowned", T)]
       and hits(f"// fixed in #123. {T}: x", "a.sv") == [(1, "unowned", T)])
    ck("a second word beside a marker is its own near-miss",
       hits(f"// {T}(#7): see the historical {T}.md", "a.sv")
       == [(1, "owned", T), (1, "near", T)])
    ck("an owned marker in a comment beside the word in code",
       hits(f'{T} = "x"  # {T}(#7): rename', "a.py") == [(1, "near", T), (1, "owned", T)])

    # -- the near-miss classes, each observed in this tree --
    ck("a filename reference is not a marker",
       scan_line(f"  # see the historical {T}.md for the original plan", "a.py")[0] is False,
       "no colon or paren follows the word")
    ck("an identifier named for the word is not a marker",
       scan_line(f'{T} = "{T} describe this section"', "a.py")[0] is False,
       "an assignment is not a comment")
    ck("a comparison against that identifier is not a marker",
       scan_line(f"    if d == {T} or not d:", "a.py")[0] is False)
    ck("prose about markers is not a marker",
       scan_line(f"  #     yet - a {T} belongs in the roadmap, not here", "a.sh")[0] is False)
    ck("a marker word in a trailing parenthetical is not a marker",
       scan_line(f"  //! still tied high today (REQ-MAC-03 {T}) so the pulse fires",
                 "a.sv")[0] is False)

    # -- a marker in CODE, not a comment, is not a marker --
    ck("a string literal is not a comment",
       scan_line(f'    msg = "{T}: fill this in"', "a.py")[0] is False)
    ck("a marker on a later line of a block comment is caught",
       kinds(f"/*\n * {T}: inside a block comment\n */\n", "a.sv") == {2: "unowned"})

    # -- the apostrophe is not a string delimiter in SystemVerilog --
    ck("a sized literal before a marker on the same line",
       scan_line(f"wire t = 1'b0; // {T}: x", "a.sv") == (True, False))
    ck("a sized literal on the line before a marker",
       kinds(f"wire a = 1'b0;\n// {T}: on the next line\n", "a.sv") == {2: "unowned"})
    ck("an aggregate literal before a marker",
       scan_line(f"q = '{{default:0}}; // {T}: x", "a.sv") == (True, False))
    sv = (f"wire a = 1'b0; // {T}: beside a sized literal\n"
          f"assign q = 8'hFF; // {T}(#53): beside a hex literal\n"
          f'$display("//{T}: inside a string, not a comment");\n'
          f"// it's a comment with an apostrophe\n"
          f"// {T}: the line after that apostrophe\n")
    ck("no SystemVerilog comment is hidden by a literal, a string or an apostrophe",
       kinds(sv, "a.sv") == {1: "unowned", 2: "owned", 3: "near", 5: "unowned"},
       str(kinds(sv, "a.sv")))

    # -- and C++ has literals of its own --
    cpp = (f"int n = 1'000; // {T}: beside a digit separator\n"
           f"auto m = 0x00A0'0000'0000'0000ull; // {T}: beside hex digit separators\n"
           f"size_t q = doc.find('\"', 8); // {T}: beside a quote character literal\n"
           f"char c = '\\''; // {T}: beside an escaped apostrophe literal\n"
           f"// {T}: the line after them all\n")
    ck("digit separators and character literals hide no C++ comment",
       kinds(cpp, "a.cpp") == {n: "unowned" for n in range(1, 6)}, str(kinds(cpp, "a.cpp")))

    # -- string state never crosses a line, except a Python docstring --
    py = (f'"""Module doc.\n'
          f"    # {T}: an example inside a docstring, not a comment\n"
          f'"""\n'
          f"# {T}: a real comment\n"
          f"x = 1  # {T}(#7): a trailing owned one\n")
    ck("a marker-shaped example inside a Python docstring is not a marker, the comment after it is",
       kinds(py, "a.py") == {2: "near", 4: "unowned", 5: "owned"}, str(kinds(py, "a.py")))
    ck("a heredoc apostrophe does not carry into the next shell line",
       kinds(f"cat <<EOF\nit's\nEOF\n# {T}: after the heredoc\n", "a.sh") == {4: "unowned"})
    ck("Tcl has no apostrophe quoting",
       scan_line(f"puts it's ;# {T}: x", "a.tcl") == (True, False))
    ck("an apostrophe inside a YAML word is prose",
       scan_line(f"- name: don't  # {T}: x", "a.yml") == (True, False))

    # -- every registered type is read with its own comment syntax --
    typed = [("# ", "Makefile"), ("# ", "a.mk"), ("// ", "a.svh"), ("// ", "a.vh"),
             ("// ", "a.vlt"), ("# ", "a.xdc"), ("# ", "a.do"), ("# ", "a.feature"),
             ("# ", "a.ini"), ("; ", "a.ini"), ("# ", "a.toml"), ("// ", "a.f"),
             ("# ", "a.f"), ("# ", "Containerfile.dev"), ("# ", "a.budget"),
             ("# ", "boards.local.sh.example"), ("# ", "a.yml"), ("# ", "a.tcl"),
             ("// ", "a.h"), ("// ", "a.c"), ("# ", "a.sh"), ("// ", "a.v"),
             ("# ", ".gitignore"), ("# ", ".gitattributes"), ("; ", ".gitmodules")]
    missed = [path for opener, path in typed
              if scan_line(f"{opener}{T}: injected", path) != (True, False)]
    ck("every registered type is read with its own comment syntax", not missed, ", ".join(missed))
    ck("a Gherkin step is not a comment; a Gherkin comment line is",
       scan_line(f"  Given a step # {T}: x", "a.feature")[0] is False
       and scan_line(f"  # {T}: x", "a.feature") == (True, False))
    ck("markdown and images are not read", syntax_for("docs/x.md") is None
       and syntax_for("x.svg") is None)

    # -- the population: first-party types, no vendor tree, no archived top --
    sample = ["hdl/a.sv", "tb/x/Makefile", "hdl/common/parameters.svh",
              "third_party/verilog-axis/rtl/a.py", "external/b.sv",
              "gptp-processor/bench/arty/bench_phc.sv", "protocol-processor/Makefile",
              "hdl/milan/milan_top.sv", "docs/a.md", "x.svg"]
    links = ["external", "third_party/verilog-axis", "protocol-processor", "gptp-processor"]
    ck("a vendor gitlink is dropped and a project processor is kept",
       first_party(sample, links) == [p for p in sample
                                      if not p.startswith(("third_party/", "external/"))])
    ck("every registered first-party type is read and the rest is not",
       select(first_party(sample, links)) == ["hdl/a.sv", "tb/x/Makefile",
                                              "hdl/common/parameters.svh",
                                              "gptp-processor/bench/arty/bench_phc.sv",
                                              "protocol-processor/Makefile"])
    ck("an empty population is refused", population_problem([]) is not None)
    ck("a population missing a processor is refused",
       "gptp-processor" in (population_problem(["hdl/a.sv", "protocol-processor/hdl/a.sv"]) or ""))
    ck("a population without the superproject is refused",
       population_problem(["protocol-processor/hdl/a.sv", "gptp-processor/hdl/a.sv"]) is not None)
    ck("a complete population is judged",
       population_problem(["hdl/a.sv", "protocol-processor/hdl/a.sv",
                           "gptp-processor/hdl/a.sv"]) is None)

    # -- and this gate must not be a finding of itself --
    own = Path(__file__).read_text()
    ck("this checker carries no marker of its own",
       not any(h.kind != "near" for h in scan_text(own, "scripts/check_todo_ownership.py")),
       "a checker that flags its own fixtures or prose cannot be green")

    # -- the live tree: what is reached, independent of how much debt it holds --
    paths = scannable()
    ck("the live population reaches both processors, the gptp bench, RTL headers, "
       "Makefiles and this gate, and no vendor tree",
       any(p.startswith("gptp-processor/bench/") for p in paths)
       and any(p.startswith("protocol-processor/hdl/") for p in paths)
       and any(p.endswith(".svh") for p in paths)
       and any(type_key(p) == "Makefile" for p in paths)
       and "scripts/check_todo_ownership.py" in paths
       and not any(p.startswith(("third_party/", "external/")) for p in paths)
       and population_problem(paths) is None)
    unowned, owned, near = audit(paths)
    ck("every reported occurrence is a real line of its file that carries the word reported",
       all(re.search(r"\b%s\b" % word, (REPO / rel).read_text(errors="replace").split("\n")[n - 1])
           for rel, n, word, _text in unowned + owned + near))
    ck("the scan skips markdown", not any(r.endswith(".md") for r, _n, _w, _t in near + unowned))
    run = subprocess.run([sys.executable, __file__], env={"PATH": "/nonexistent"},
                         capture_output=True, text=True, cwd=REPO)
    ck("a host without git is refused by name, never passed",
       run.returncode == 2 and run.stdout.startswith("REFUSED: git is not available"),
       f"rc={run.returncode} stdout={run.stdout[:80]!r} stderr={run.stderr[-160:]!r}")

    print(f"\n{total} checks: {total - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true",
                    help="markers, near-misses, and the types read and not read")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    try:
        everything = tracked()
    except FileNotFoundError as exc:
        print(f"REFUSED: git is not available ({exc.filename}); "
              "the population cannot be enumerated")
        return 2
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"REFUSED: {exc}")
        return 2
    paths = select(everything)
    problem = population_problem(paths)
    if problem:
        print(f"REFUSED: {problem}; a partial population is never read as a pass")
        return 2

    unowned, owned, near = audit(paths)

    if args.list:
        print(f"owned markers ({len(owned)}) - the owner issue number is taken on trust, "
              "not checked against the tracker:")
        for rel, n, word, line in owned:
            print(f"   {rel}:{n}:{word}  {line}")
        print(f"\nnear-misses - the word, but not a marker "
              f"({len(near)} occurrence(s) on {lines_of(near)} line(s)):")
        for rel, n, word, line in near:
            print(f"   {rel}:{n}:{word}  {line}")
        read = Counter(type_key(p) for p in paths)
        chosen = set(paths)
        unread = Counter(type_key(p) for p in everything
                         if p not in chosen and p not in LINT_EXCLUDE)
        excluded = [p for p in everything if p in LINT_EXCLUDE]
        print(f"\nread: {len(paths)} first-party file(s) in {len(read)} type(s): "
              + ", ".join(f"{k} {v}" for k, v in read.most_common()))
        print(f"not read - no comment syntax registered ({sum(unread.values())} file(s)): "
              + ", ".join(f"{k} {v}" for k, v in unread.most_common()))
        print("not read - scripts/lint_rtl.py LINT_EXCLUDE: " + ", ".join(excluded))
        print()

    for rel, n, word, line in unowned:
        print(f"UNOWNED MARKER: {rel}:{n}:{word} — {line}\n"
              f"    A marker names the issue that owns it, as TODO(#N), or it is "
              f"resolved. An unowned marker reads as a plan nobody is accountable for.")

    if unowned:
        return 1
    print(f"TODO ownership gate: OK ({len(owned)} owned marker(s), 0 unowned; "
          f"{len(near)} near-miss occurrence(s) on {lines_of(near)} line(s) "
          f"correctly not treated as markers; {len(paths)} first-party file(s) read)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
