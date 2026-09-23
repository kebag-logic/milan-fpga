#!/usr/bin/env python3
"""Reviewer mutation probes: each mutation edits ONE property in a disposable
copy of the head's scripts and runs `gen_toc.py --selftest` there.

Usage: mutate.py <head-scripts> <scratch-dir> <out.txt>
A mutation is KILLED when the self-test exits non-zero; the first failing
arm names are recorded. The copy is rebuilt from <head-scripts> for every
mutation, so no mutation leaks into the next.
"""
import shutil
import subprocess
import sys
from pathlib import Path

C, H, T = "gen_toc_containers.py", "gen_toc_html.py", "gen_toc.py"
MUTATIONS = [
    ("R01 item continues only past its column", C,
     "        if lead >= box.need:\n", "        if lead > box.need:\n"),
    ("R02 footnote continues at two columns", C,
     "    if lead >= TAB_STOP:\n        return at + TAB_STOP\n",
     "    if lead >= 2:\n        return at + 2\n"),
    ("R03 indented line is never lazy", C,
     "    if _lead(rem) >= TAB_STOP:\n        return True\n", ""),
    ("R04 any item interrupts a paragraph", C,
     "        elif item and not (interrupting and not (\n"
     "                item.group(2) and int(item.group(1) or 1) == 1)):\n",
     "        elif item:\n"),
    ("R05 four padding columns count as code", C,
     "padding > TAB_STOP else", "padding >= TAB_STOP else"),
    ("R06 footnote content is read", C,
     "    noted = any(box.kind == NOTE for box in walk.stack)\n",
     "    noted = False\n"),
    ("R07 <!---> does not close at once", H,
     'HTML_ABRUPT_END_RE = re.compile(r"-?>")', 'HTML_ABRUPT_END_RE = re.compile(r">")'),
    ("R08 --!> does not close", H,
     'HTML_COMMENT_END_RE = re.compile(r"--!?>")', 'HTML_COMMENT_END_RE = re.compile(r"-->")'),
    ("R09 tag filter ignored", H,
     "        elif HTML_FILTERED_RE.match(raw, mark.start()):\n            at = mark.start() + 1\n", ""),
    ("R10 backslash escape not read", H,
     'r"\\\\%(esc)s|(?P<ticks>', 'r"(?P<ticks>'),
    ("R11 code span not skipped", H,
     "            at = closer.end() if closer else at\n", "            at = at\n"),
    ("R12 Markdown text never closes", H,
     "inside, text = inside and not inline_closes(\"\\n\".join(text)), []",
     "inside, text = inside, []"),
    ("R13 no container ends a block", T,
     "owner not in scope.held_by or ", ""),
    ("R14 prose comment never ends early", T,
     " or (prose and not scope.plain)", ""),
    ("R15 rendered comment hides nothing", T,
     "        out[-1] = COMMENT if hidden and out[-1] == TEXT else out[-1]\n", ""),
    ("R16 <!--> is an open comment again", T,
     'scan, inside = scan[at + len("<!"):], True', 'scan, inside = scan[at + len(COMMENT_OPEN):], True'),
    ("R17 declarations take lowercase", T,
     '"declaration name": "A-Z",', '"declaration name": "A-Za-z",'),
    ("R18 indented comment in a paragraph is a block", C,
     "    if state == COMMENT and (label == TEXT or _lead(rem) > 3):\n",
     "    if state == COMMENT and label == TEXT:\n"),
    ("R19 lazy line gates as a paragraph", C,
     "return _scope(walk, HELD, (True, True), rem, TEXT)",
     "return _scope(walk, PARAGRAPH, (True, True), rem, TEXT)"),
    ("R20 quote takes no optional space", C,
     '    return at + 1 if text[at:at + 1] == " " else at\n', "    return at\n"),
    ("R21 empty item survives a blank line", C,
     "        return len(text) if box.filled and _blank(rest) else None\n",
     "        return len(text) if _blank(rest) else None\n"),
    ("R22 thematic break opens an item", C,
     "        elif THEMATIC_BREAK_RE.match(rem):\n            break\n", ""),
    ("R23 every item starts filled", C,
     "_push(walk, ITEM, need, bool(item.group(2)))", "_push(walk, ITEM, need, True)"),
    ("R24 quoted attribute values not read", H,
     r'''r"(?:\"[^\"]*(?:\"|\Z)|'[^']*(?:'|\Z)|(?:(?!%(s)s)[^>])*))?)*(?:>|\Z)"''',
     r'''r"(?:(?:(?!%(s)s)[^>])*))?)*(?:>|\Z)"'''),
    ("R25 bogus comment is not skipped", H,
     r'r"(?P<comment><!--)|<!(?!--)[^>]*(?:>|\Z)|<\?[^>]*(?:>|\Z)"',
     r'r"(?P<comment><!--)"'),
    ("R26 gate ignored (column-0 paragraph state)", T,
     "label, state, delim, tag = _opens(line, para, state, scope.gate)",
     "label, state, delim, tag = _opens(line, para, state)"),
    ("R27 types 3 to 5 not raw in the layer", C,
     "    raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None\n",
     "    raw = None\n"),
    ("R28 blank line does not end a quote", C,
     "        if lead > 3 or rest[lead:lead + 1] != \">\":\n            return None\n",
     "        if _blank(rest):\n            return len(text)\n"
     "        if lead > 3 or rest[lead:lead + 1] != \">\":\n            return None\n"),
    ("R29 two-digit ordinal widens nothing", C,
     "end = _lead(rem) + (len(item.group(1)) + 1 if item.group(1) else 1)",
     "end = _lead(rem) + (2 if item.group(1) else 1)"),
    ("R30 tabs not expanded in the layer", C,
     "    text = line.expandtabs(TAB_STOP)\n", "    text = line.replace('\\t', ' ')\n"),
]


def main() -> None:
    head, scratch, out_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    lines = []
    for name, module, old, new in MUTATIONS:
        work = scratch / "mut"
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(head, work)
        path = work / module
        src = path.read_text()
        if src.count(old) != 1:
            lines.append(f"{name}: NOT APPLIED (pattern occurs {src.count(old)} times)")
            continue
        path.write_text(src.replace(old, new))
        res = subprocess.run([sys.executable, "-B", "gen_toc.py", "--selftest"],
                             cwd=work, capture_output=True, text=True)
        out = (res.stdout + res.stderr).splitlines()
        failing = [l for l in out if l.startswith("[") or "FAIL" in l][:3]
        verdict = "KILLED" if res.returncode else "SURVIVED"
        lines.append(f"{name}: {verdict} exit={res.returncode} :: " + " || ".join(failing)[:400])
        print(lines[-1], flush=True)
    shutil.rmtree(scratch / "mut", ignore_errors=True)
    Path(out_path).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
