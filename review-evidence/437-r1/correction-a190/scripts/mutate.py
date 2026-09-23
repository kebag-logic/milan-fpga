#!/usr/bin/env python3
"""Named one-line mutations of the committed walk, each in a disposable copy.

Usage: mutate.py REV OUT.json [ID...]
Every mutation replaces exactly one span of one file in `git archive REV
scripts`, then runs `gen_toc.py --selftest` and `check_em_dash.py --selftest`
in that copy. A mutation is KILLED for its property when both self-tests exit
nonzero and at least one failing arm of each names the property (`expect`).
The checkout itself is never modified.
"""
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = "$LANES/437-container-paragraph-scopes"
C, H, G = "gen_toc_containers.py", "gen_toc_html.py", "gen_toc.py"
# (id, property, file, old, new, expected arm-name fragments)
MUTATIONS = [
    ("M01", "type-7 gate read from the container layer", G,
     "_opens(line, para, state, scope.gate)", "_opens(line, para, state)",
     ["two spaces", "bullet at column, inline tag outside", "labels live bullet paragraph"]),
    ("M02", "a tag under a nested block opens raw HTML (no gate from item liveness)", C,
     "return _scope(walk, para, (plain, plain and para == PARAGRAPH), rem, label)",
     "return _scope(walk, PARAGRAPH if walk.stack and not _blank(rem) else para, "
     "(plain, plain and para == PARAGRAPH), rem, label)",
     ["labels nested quote", "labels nested bullet"], ("toc",)),
    ("M03", "a block opened in a container ends with it", G,
     "owner not in scope.held_by or (prose", "False or (prose",
     ["would escape", "P02"]),
    ("M04", "lazy continuation keeps containers open", C,
     "    if _blank(rem):\n        return False\n    if _lead(rem) >= TAB_STOP:",
     "    if True:\n        return False\n    if _lead(rem) >= TAB_STOP:",
     ["lazy"]),
    ("M05", "an indented lazy line continues the paragraph", C,
     "    if _lead(rem) >= TAB_STOP:\n        return True\n",
     "    if _lead(rem) >= TAB_STOP:\n        return False\n",
     ["lazy indented"]),
    ("M06", "an empty item ends at a blank line", C,
     "_push(walk, ITEM, need, bool(item.group(2)))", "_push(walk, ITEM, need, True)",
     ["empty item ends at blank", "empty padded item ends at blank"]),
    ("M07", "a blank line of the item's column keeps an empty item", C,
     "        if lead >= box.need:\n", "        if lead >= box.need and not _blank(rest):\n",
     ["empty item kept by a blank of its column"]),
    ("M08", "an empty item's first line meets no paragraph (R237-2 F3)", C,
     "    if not _blank(rem):\n        for box in walk.stack:\n            box.filled = True\n",
     "    first = any(not box.filled for box in walk.stack)\n"
     "    if not _blank(rem):\n        for box in walk.stack:\n            box.filled = True\n"
     "    para = PARAGRAPH if first and not _blank(rem) and walk.stack else para\n",
     ["labels empty item, tag opens HTML"], ("toc",)),
    ("M09", "a quote consumes one optional space", C,
     'return at + 1 if text[at:at + 1] == " " else at', "return at",
     ["a quote's optional space leaves a raw opener",
      "a continued quote's optional space leaves a raw opener"]),
    ("M10", "a footnote definition continues at four columns", C,
     "    if lead >= TAB_STOP:\n        return at + TAB_STOP\n",
     "    if lead >= 2:\n        return at + 2\n",
     ["footnote"]),
    ("M11", "padding over four columns makes the content column marker plus one", C,
     "padding > TAB_STOP else end + padding", "padding > TAB_STOP + 1 else end + padding",
     ["code padding uses one"]),
    ("M12", "a list item interrupts a paragraph only with content and ordinal 1", C,
     "item.group(2) and int(item.group(1) or 1) == 1)):", "True)):",
     ["noninterrupting ordinal", "empty"]),
    ("M13", "a thematic break is no list item", C,
     "        elif THEMATIC_BREAK_RE.match(rem):\n            break\n", "",
     ["thematic break is no item"]),
    ("M14", "raw HTML blocks of types 3 to 5 are raw", C,
     "raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None", "raw = None",
     ["type-3 block", "type-4 block", "type-5 block"]),
    ("M15", "footnote content is not read in place", C,
     "noted = any(box.kind == NOTE for box in walk.stack)", "noted = False",
     ["footnote content is read at the page end"]),
    ("M16", "tab stops of four", C,
     "text = line.expandtabs(TAB_STOP)", "text = line.replace(\"\\t\", \" \")",
     ["tab"]),
    ("M17", "a comment opens only in HTML's data state (not on any substring)", H,
     "        mark = HTML_MARKUP_RE.search(raw, at)\n",
     "        mark = re.compile(r\"(?P<comment><!--)\").search(raw, at)\n",
     ["double-quoted attribute", "CDATA is a bogus comment"]),
    ("M18", "--!> closes a comment", H,
     'HTML_COMMENT_END_RE = re.compile(r"--!?>")', 'HTML_COMMENT_END_RE = re.compile(r"-->")',
     ["--!> closes"]),
    ("M19", "<!--> and <!---> close at once", H,
     "abrupt = HTML_ABRUPT_END_RE.match(raw, mark.end())", "abrupt = None",
     ["abrupt"]),
    ("M20", "GFM's tag filter escapes the tag", H,
     "elif HTML_FILTERED_RE.match(raw, mark.start()):", "elif False:",
     ["tag filter leaves the attribute as text"]),
    ("M21", "a bogus comment ends at the next >", H,
     r'r"(?P<comment><!--)|<!(?!--)[^>]*(?:>|\Z)|<\?[^>]*(?:>|\Z)"',
     r'r"(?P<comment><!--)|<\?[^>]*(?:>|\Z)"',
     ["CDATA is a bogus comment"]),
    ("M22", "a quoted attribute value hides an opener", H,
     "r\"(?:\\\"[^\\\"]*(?:\\\"|\\Z)|'[^']*(?:'|\\Z)|(?:(?!%(s)s)[^>])*))?)*(?:>|\\Z)\"",
     "r\"(?:(?:(?!%(s)s)[^>])*))?)*(?:>|\\Z)\"",
     ["a quoted value hides a greater-than"]),
    ("M23", "inline raw HTML in Markdown text closes a comment", H,
     "        if mark.group(\"html\") and HTML_COMMENT_END_RE.search(mark.group(\"html\")):\n"
     "            return True\n",
     "        if False:\n            return True\n",
     ["closed by an inline comment", "inline tag closes after the block"]),
    ("M24", "a closer in plain prose or a code span closes nothing", H,
     "    at = 0\n    while True:\n        mark = INLINE_HTML_RE.search(text, at)",
     "    return bool(HTML_COMMENT_END_RE.search(text))\n    at = 0\n    while True:\n"
     "        mark = INLINE_HTML_RE.search(text, at)",
     ["prose arrow closes nothing", "code span hides the tag"]),
    ("M25", "a code span hides inline HTML", H,
     "        if mark.group(\"ticks\"):\n", "        if False:\n",
     ["code span hides the tag"]),
    ("M26", "an inline declaration takes an uppercase name", H,
     '"decl": _cc("declaration name")', '"decl": _cc("tag name")',
     ["lowercase declaration is text"]),
    ("M27", "a paragraph's text is read whole", H,
     "if text and not (scope.text is not None and scope.cont):",
     "if text and not (scope.text is not None and False):",
     ["tag across lines closes"]),
    ("M28", "a comment opened in prose ends with its paragraph", G,
     "prose = state == COMMENT and (label == TEXT or scope.plain)", "prose = False",
     ["heading after a prose opener", "item block ends before a code span"]),
    ("M29", "an opener indented into a paragraph is prose", G,
     "prose = state == COMMENT and (label == TEXT or scope.plain)",
     "prose = state == COMMENT and label == TEXT",
     ["indented comment opener continues a paragraph"]),
    ("M30", "an inline comment starts no block in the container layer", C,
     "    if state == COMMENT and (label == TEXT or _lead(rem) > 3):\n        label, state = TEXT, TEXT\n",
     "",
     ["type-3 block", "leaves that line alone"]),
    ("M31", "a hidden line is labelled commented", G,
     "out[-1] = COMMENT if hidden and out[-1] == TEXT else out[-1]", "pass",
     ["#516", "raw HTML in an item"]),
    ("M32", "a marker inside a fence, comment or raw HTML block opens nothing (R237-r1 F3)", C,
     "    if not closed and state in (FENCE, COMMENT, HTML):\n        return _inside(walk, rem)\n",
     "    if False:\n        return _inside(walk, rem)\n",
     ["marker-indented-closer", "marker is inert"]),
    ("M33", "a dedented quote or footnote definition ends the item (R238-r1 F2)", C,
     "    starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,\n"
     "              FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)\n",
     "    starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, LIST_ITEM_RE, RAW_3_5_RE)\n",
     ["R238 D0", "releases iff dedented"]),
]


def archive(rev: str, dest: Path) -> None:
    data = subprocess.run(["git", "-C", REPO, "archive", rev, "scripts"],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest, filter="data")


def failing(out: str) -> list[str]:
    names = re.findall(r"FAIL \[([^\]]*)\]", out)
    names += re.findall(r"^\s*- \[([^\]]*)\]", out, re.M)
    names += re.findall(r"GUARD (.*)", out)
    return names


def run(copy: Path) -> dict:
    res = {}
    for key, script in (("toc", "gen_toc.py"), ("emdash", "check_em_dash.py")):
        try:
            r = subprocess.run([sys.executable, "-B", script, "--selftest"], cwd=copy,
                               capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            res[key] = {"exit": "timeout", "failing": [], "tail": "no verdict in 120 s"}
            continue
        out = r.stdout + r.stderr
        res[key] = {"exit": r.returncode, "failing": failing(out),
                    "tail": out.strip().splitlines()[-1] if out.strip() else ""}
    return res


def main() -> int:
    rev, out = sys.argv[1], Path(sys.argv[2])
    only = set(sys.argv[3:])
    results = []
    with tempfile.TemporaryDirectory(prefix="a190-mutants.") as tmp:
        base = Path(tmp) / "clean"
        archive(rev, base)
        results.append({"id": "M00", "property": "unmutated control",
                        **run(base / "scripts")})
        for mid, prop, name, old, new, expect, *rest in MUTATIONS:
            consumers = rest[0] if rest else ("toc", "emdash")
            if only and mid not in only:
                continue
            copy = Path(tmp) / mid
            archive(rev, copy)
            path = copy / "scripts" / name
            src = path.read_text()
            count = src.count(old)
            if count != 1:
                results.append({"id": mid, "property": prop, "error": f"{count} matches"})
                print(f"{mid} ERROR: {count} matches for its span", flush=True)
                continue
            path.write_text(src.replace(old, new))
            res = run(copy / "scripts")
            hit = {k: [f for f in v["failing"] if any(e in f for e in expect)]
                   for k, v in res.items()}
            killed = all(res[k]["exit"] not in (0, "timeout") and hit[k] for k in consumers)
            results.append({"id": mid, "property": prop, "file": name, "old": old, "new": new,
                            "expect": expect, "consumers": consumers, "killed": killed, **res,
                            "named_hits": hit})
            print(f"{mid} {'KILLED' if killed else 'SURVIVED'} toc={res['toc']['exit']}"
                  f"({len(res['toc']['failing'])} arms, {len(hit['toc'])} named) "
                  f"emdash={res['emdash']['exit']}({len(res['emdash']['failing'])} arms, "
                  f"{len(hit['emdash'])} named) :: {prop}", flush=True)
    out.write_text(json.dumps({"rev": rev, "results": results}, indent=1) + "\n")
    print(f"control: toc={results[0]['toc']['exit']} emdash={results[0]['emdash']['exit']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
