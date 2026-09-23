#!/usr/bin/env python3
"""R237-2 reviewer mutation probe for the #437 walk changes.

Usage: mutate.py TREE [M<n> ...]
TREE is a disposable checkout of the exact head. With mutation IDs, only
those run; without, all run. For each mutation the
script rewrites TREE/scripts/gen_toc.py (one exact substring replacement,
refused unless the original occurs exactly once), runs
`gen_toc.py --selftest` and `check_em_dash.py --selftest`, records the exit
codes and the first failing arm names, then restores the original bytes and
verifies their SHA-256. A mutation is KILLED when either selftest exits
non-zero.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

MUTATIONS = [
    ("M1 no content-column continuation (opening_para override removed)",
     "                opening_para = PARAGRAPH\n",
     "                pass\n"),
    ("M2 no PARAGRAPH->HELD inside the item",
     "        return HELD if after == PARAGRAPH else after, (context[0], False)\n",
     "        return after, (context[0], False)\n"),
    ("M3 no rendered-comment hiding",
     "        hidden = rendered_comment and out[-1] == TEXT\n",
     "        hidden = False\n"),
    ("M4 abrupt empty comments not complete",
     '            scan, inside = scan[at + len("<!"):], True\n',
     "            scan, inside = scan[at + len(COMMENT_OPEN):], True\n"),
    ("M5 dedented quote/footnote keeps item context",
     "    if BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line):\n        return after, None\n",
     "    if False:\n        return after, None\n"),
    ("M6 empty item survives a blank",
     "        return after, None if context and context[1] else context\n",
     "        return after, context\n"),
    ("M7 wide padding keeps the padded column",
     "        if not item.group(2) or column - marker_end > 4:\n",
     "        if not item.group(2):\n"),
    ("M8 lazy line releases item",
     "    if para == HELD and after == HELD:\n        return after, context\n",
     "    if False:\n        return after, context\n"),
    ("M9 rendered comment ignores raw HTML lines",
     "        if out[-1] in (HTML, COMMENT) or (out[-1] == TEXT and COMMENT_OPEN in line):\n",
     "        if out[-1] == COMMENT or (out[-1] == TEXT and COMMENT_OPEN in line):\n"),
    ("M10 continuation also for empty-item context",
     "        if para == HELD and item_context and not item_context[1] \\\n",
     "        if para == HELD and item_context \\\n"),
    ("M11 strict column for the continuation",
     "                    and _indent_columns(line) >= item_context[0]:\n",
     "                    and _indent_columns(line) > item_context[0]:\n"),
    ("M12 strict column for item membership",
     "    if context and _indent_columns(line) >= context[0]:\n",
     "    if context and _indent_columns(line) > context[0]:\n"),
    ("M13 empty item keeps its padded column",
     "        if not item.group(2) or column - marker_end > 4:\n            column = marker_end + 1\n",
     "        if item.group(2) and column - marker_end > 4:\n            column = marker_end + 1\n"),
    ("M14 prose openers do not update the rendered comment",
     "        if out[-1] in (HTML, COMMENT) or (out[-1] == TEXT and COMMENT_OPEN in line):\n",
     "        if out[-1] in (HTML, COMMENT):\n"),
    ("M15 a non-interrupting ordinal seeds an item",
     "    item = LIST_ITEM_RE.match(line) if label == TEXT and after == HELD else None\n",
     "    item = LIST_ITEM_RE.match(line) if label == TEXT else None\n"),
    ("M16 a blank ends every item",
     "        return after, None if context and context[1] else context\n",
     "        return after, None\n"),
    ("M17 hidden prose also hides headings in fences only",
     "        hidden = rendered_comment and out[-1] == TEXT\n",
     "        hidden = rendered_comment and out[-1] == TEXT and not line.startswith(\"#\")\n"),
    ("M18 non-TEXT block content seeds item context (prior R237-r1 F3 mutation)",
     "    item = LIST_ITEM_RE.match(line) if label == TEXT and after == HELD else None\n",
     "    item = LIST_ITEM_RE.match(line) if label != TEXT or after == HELD else None\n"),
]


def run(tree: Path, script: str) -> tuple[int, list[str]]:
    r = subprocess.run([sys.executable, f"scripts/{script}", "--selftest"], cwd=tree,
                       capture_output=True, text=True)
    lines = (r.stdout + r.stderr).splitlines()
    fails = [ln for ln in lines if "FAIL" in ln or ln.startswith("[")][:4]
    return r.returncode, fails


def main() -> int:
    tree = Path(sys.argv[1])
    target = tree / "scripts" / "gen_toc.py"
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    survivors = 0
    for name, old, new in [m for m in MUTATIONS if m[0].split()[0] in sys.argv[2:]] or MUTATIONS:
        if text.count(old) != 1:
            print(f"REFUSED {name}: original occurs {text.count(old)} times")
            survivors += 1
            continue
        target.write_text(text.replace(old, new))
        try:
            toc, toc_fail = run(tree, "gen_toc.py")
            dash, dash_fail = run(tree, "check_em_dash.py")
        finally:
            target.write_bytes(original)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
        killed = toc != 0 or dash != 0
        survivors += not killed
        print(f"{'KILLED ' if killed else 'SURVIVED'} {name}: toc={toc} emdash={dash}")
        for ln in (toc_fail + dash_fail)[:4]:
            print(f"    {ln[:180]}")
    print(f"restored gen_toc.py sha256 {digest}; survivors {survivors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
