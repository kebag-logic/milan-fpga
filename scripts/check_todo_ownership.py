#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: a TODO in first-party code names the issue that owns it.

Why this exists. Rule 7 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a marker either names a concrete issue
or is resolved - it is not an untracked backlog. An unowned marker is worse
than no marker: it reads as a plan, nobody is accountable for it, and it
survives the change that made it wrong. `ptp_ts_top.sv` carried a
marker asking for DMA engine signals, next to the three DMA streams that
already exist, which Issue #53 records as present and only needing attachment.

WHAT COUNTS AS A MARKER, and why the definition is narrow. Across the
superproject and both project-owned processor submodules, the first of these
words appears fifteen times before the cleanup and fourteen are not markers. A
naive search finds:

  * a citation of the historical task-list document, which pages legitimately
    name;
  * an IDENTIFIER in `scripts/gen_toc.py` holding the placeholder description
    that gate refuses, and every comparison against it;
  * prose ABOUT markers - "as a placeholder", "it belongs in the roadmap, not
    here".

So a marker here is: the word, INSIDE A COMMENT, immediately followed by `:` or
`(`. That is the shape a real marker always has and none of the false positives
above do. The three classes are counted and printed rather than silently
dropped, so a reader can see what the narrowing cost.

Accepted form: the marker word followed immediately by the owning issue in
parentheses - `(#123)`. The issue number is the owner.

Files excluded from the RTL half come from `scripts/lint_rtl.py`'s
`LINT_EXCLUDE`, the same list Rules 5 and 6 use; `hdl/milan/milan_top.sv` is an
archived Zynq top that no build compiles, and its markers are part of the
archive, not of maintained code. Markdown is not scanned at all: prose about a
document whose name is one of these words is not a marker.

Usage:
    python3 scripts/check_todo_ownership.py            # gate
    python3 scripts/check_todo_ownership.py --list     # markers and near-misses
    python3 scripts/check_todo_ownership.py --selftest # fixture arms

Exit 0 = every marker in gated first-party code names an issue.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE
from code_quality_scope import tracked

WORDS = "TODO|FIXME|XXX|HACK"
#: the marker shape: the word, then optional space, then `:` or `(`
MARKER = re.compile(r"\b(%s)\b\s*(?=[:(])" % WORDS)
#: the owned form
OWNED = re.compile(r"\b(?:%s)\s*\(\s*#\d+\s*\)" % WORDS)
#: the word anywhere, for the near-miss inventory
ANY = re.compile(r"\b(%s)\b" % WORDS)

SLASH = (".sv", ".v", ".cpp", ".h", ".hpp", ".c")
HASH = (".py", ".sh", ".yml", ".yaml", ".tcl", ".mk")

SOURCE_PATTERNS = ("*.py", "*.sh", "*.tcl", "*.mk", "*.yml", "*.yaml",
                   ".github", "hdl", "sw", "scripts", "tb", "syn", "harness")


def comments_only(text, path):
    """Preserve comments/newlines and blank code plus quoted strings."""
    out = ["\n" if char == "\n" else " " for char in text]
    if path.endswith(SLASH):
        i, state, quote = 0, "code", ""
        while i < len(text):
            char = text[i]
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if state == "code":
                if char in ('"', "'"):
                    state, quote = "string", char
                elif char == "/" and nxt == "/":
                    state = "line"
                    out[i] = out[i + 1] = "/"
                    i += 1
                elif char == "/" and nxt == "*":
                    state = "block"
                    out[i], out[i + 1] = "/", "*"
                    i += 1
            elif state == "string":
                if char == "\\":
                    i += 1
                elif char == quote:
                    state = "code"
            elif state == "line":
                out[i] = char
                if char == "\n":
                    state = "code"
            else:  # block comment
                out[i] = char
                if char == "*" and nxt == "/":
                    out[i + 1] = "/"
                    i += 1
                    state = "code"
            i += 1
        return "".join(out)

    if path.endswith(HASH):
        for offset, line in _lines_with_offsets(text):
            quote, escaped = "", False
            for n, char in enumerate(line):
                if escaped:
                    escaped = False
                    continue
                if char == "\\" and quote:
                    escaped = True
                elif quote:
                    if char == quote:
                        quote = ""
                elif char in ('"', "'"):
                    quote = char
                elif char == "#":
                    out[offset + n:offset + len(line)] = line[n:]
                    break
        return "".join(out)
    return "".join(out)


def _lines_with_offsets(text):
    offset = 0
    for line in text.splitlines(keepends=True):
        yield offset, line
        offset += len(line)


def comment_text(line, path):
    """The comment part of one line, retained for the fixture API."""
    return comments_only(line, path).strip()


def scannable():
    return [p for p in tracked(*SOURCE_PATTERNS)
            if p.endswith(SLASH + HASH)
            and p not in LINT_EXCLUDE]


def scan_line(line, path="x.py"):
    """(is_marker, is_owned) for one line."""
    body = comment_text(line, path)
    if not body:
        return False, False
    if not MARKER.search(body):
        return False, False
    return True, bool(OWNED.search(body))


def audit():
    unowned, owned, near = [], [], []
    for rel in scannable():
        text = (REPO / rel).read_text(errors="replace")
        comments = comments_only(text, rel).splitlines()
        lines = text.splitlines()
        for n, line in enumerate(lines, 1):
            body = comments[n - 1] if n <= len(comments) else ""
            is_marker = bool(MARKER.search(body))
            is_owned = is_marker and bool(OWNED.search(body))
            if is_marker:
                (owned if is_owned else unowned).append((rel, n, line.strip()[:92]))
            elif ANY.search(line):
                near.append((rel, n, line.strip()[:92]))
    return unowned, owned, near


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    # THE MARKER WORDS ARE ASSEMBLED, NOT WRITTEN OUT, exactly as
    # scripts/docs_check.py assembles its denied tokens. A fixture that spells
    # a marker turns this file into a finding of its own gate: `comment_text`
    # sees the `#` that opens the string, not the string. Assembling them keeps
    # the fixtures readable AND keeps the file clean, and the arm below proves
    # the assembled form still exercises the matcher.
    T = "TO" + "DO"
    F = "FIX" + "ME"
    ck("the assembled fixture words are the real markers", T == chr(84) + "ODO" and len(F) == 5)

    ck("an unowned marker is caught",
       scan_line(f"  //{T}: add DMA signals", "a.sv") == (True, False))
    ck("an owned marker is accepted",
       scan_line(f"  //{T}(#53): attach the DMA streams", "a.sv") == (True, True))
    ck(f"{F} is a marker too", scan_line(f"  # {F}: broken", "a.py") == (True, False))
    ck(f"an owned {F} is accepted",
       scan_line(f"  # {F}(#7): broken", "a.py") == (True, True))

    # -- the three false-positive classes, each observed in this tree --
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
    block = f"/*\n * {T}: inside a block comment\n */\n"
    view = comments_only(block, "a.sv")
    ck("a marker on a later line of a block comment is caught",
       any(MARKER.search(line) for line in view.splitlines()))

    # -- and this gate must not be a finding of itself --
    own = Path(__file__).read_text()
    ck("this checker carries no marker of its own",
       not any(scan_line(l, "scripts/check_todo_ownership.py")[0]
               for l in own.splitlines()),
       "a checker that flags its own fixtures or prose cannot be green")

    # -- and the live tree must be readable --
    unowned, owned, near = audit()
    ck("the live scan reads the tree", len(near) > 0,
       "no near-miss at all - the scan is not reaching the tree")
    ck("the scan skips markdown", not any(r.endswith(".md") for r, _n, _l in near + unowned))

    n = 15
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="markers and near-misses")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    unowned, owned, near = audit()

    if args.list:
        print(f"owned markers ({len(owned)}):")
        for rel, n, line in owned:
            print(f"   {rel}:{n}  {line}")
        print(f"\nnear-misses - the word, but not a marker ({len(near)}):")
        for rel, n, line in near:
            print(f"   {rel}:{n}  {line}")
        print()

    for rel, n, line in unowned:
        print(f"UNOWNED MARKER: {rel}:{n} — {line}\n"
              f"    A marker names the issue that owns it, as TODO(#N), or it is "
              f"resolved. An unowned marker reads as a plan nobody is accountable for.")

    if unowned:
        return 1
    print(f"TODO ownership gate: OK ({len(owned)} owned marker(s), 0 unowned; "
          f"{len(near)} near-miss(es) correctly not treated as markers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
