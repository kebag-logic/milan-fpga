#!/usr/bin/env python3
"""Reviewer-owned mutation probes for #437's new properties.

Usage: mutate.py <pristine-scripts-dir> <scratch-dir> <out-json> [jobs]

Each mutant is one exact text replacement that must apply exactly once; the
mutated tree is a copy under <scratch-dir>/<id>/scripts. A mutant is KILLED
when `gen_toc.py --selftest` or `check_em_dash.py --selftest` exits non-zero.
The failing arm names are kept so a kill can be attributed to the property.
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

C, G = "gen_toc_containers.py", "gen_toc.py"
MUTANTS = [
    ("M01 fence/HTML no longer end with their container", G,
     "        if state in (FENCE, HTML) and owner not in scope.held_by:\n",
     "        if False and state in (FENCE, HTML) and owner not in scope.held_by:\n"),
    ("M02 only a fence ends with its container", G,
     "        if state in (FENCE, HTML) and owner not in scope.held_by:\n",
     "        if state in (FENCE,) and owner not in scope.held_by:\n"),
    ("M03 only raw HTML ends with its container", G,
     "        if state in (FENCE, HTML) and owner not in scope.held_by:\n",
     "        if state in (HTML,) and owner not in scope.held_by:\n"),
    ("M04 comments also end with their container (emulation re-added)", G,
     "        if state in (FENCE, HTML) and owner not in scope.held_by:\n",
     "        if state in (FENCE, HTML, COMMENT) and owner not in scope.held_by:\n"),
    ("M05 type-7 ignores the container gate", G,
     "            label, state, delim, tag = _opens(line, para, state, scope.gate)\n",
     "            label, state, delim, tag = _opens(line, para, state, None)\n"),
    ("M06 empty comment <!--> closes (closure re-added)", G,
     "            scan, inside = scan[at + len(COMMENT_OPEN):], True\n",
     "            scan, inside = scan[at + len(\"<!\"):], True\n"),
    ("M07 blank continues an item only when filled (open paragraph ignored)", C,
     "        holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)\n",
     "        holds = box.filled\n"),
    ("M08 blank continues any item", C,
     "        return len(text) if holds and _blank(rest) else None\n",
     "        return len(text) if _blank(rest) else None\n"),
    ("M09 link definition fills its item", C,
     "            or not LINK_DEFINITION_RE.match(rem)):\n",
     "            or True):\n"),
    ("M10 a nested container does not fill its parent", C,
     "    if walk.stack:\n        walk.stack[-1].filled = True\n    walk.serial += 1\n",
     "    walk.serial += 1\n"),
    ("M11 no lazy continuation", C,
     "        if state == TEXT and para == PARAGRAPH and _lazy(rem):\n",
     "        if False and state == TEXT and para == PARAGRAPH and _lazy(rem):\n"),
    ("M12 lazy line may start a list item", C,
     "              FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)\n",
     "              FOOTNOTE_DEFINITION_RE, RAW_3_5_RE)\n"),
    ("M13 footnote continues on a whitespace-only line", C,
     "    return at if not text else None\n",
     "    return at if _blank(rest) else None\n"),
    ("M14 quote takes no optional space", C,
     "    return at + 1 if text[at:at + 1] == \" \" else at\n",
     "    return at\n"),
    ("M15 wide padding keeps its width (no indented-code rule)", C,
     "    return end + 1 if not item.group(2) or padding > TAB_STOP else end + padding\n",
     "    return end + 1 if not item.group(2) else end + padding\n"),
    ("M16 any list item interrupts a paragraph", C,
     "        elif item and not (interrupting and not (\n"
     "                item.group(2) and int(item.group(1) or 1) == 1)):\n",
     "        elif item:\n"),
    ("M17 thematic break read as a list item", C,
     "        elif THEMATIC_BREAK_RE.match(rem):\n            break\n",
     "        elif False:\n            break\n"),
    ("M18 types 3-5 gate is the layer's NO_PARAGRAPH (R238-2 F1(d) reverted)", C,
     "    return _scope(walk, None if raw_3_5 else NO_PARAGRAPH)\n",
     "    return _scope(walk, NO_PARAGRAPH)\n"),
    ("M19 types 3-5 never end", C,
     "        state, tag = (TEXT, \"\") if tag in rem else (HTML, tag)\n",
     "        state, tag = (HTML, tag)\n"),
    ("M20 types 3-5 not opened by the layer", C,
     "    raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None\n",
     "    raw = None\n"),
    ("M21 layer treats an inline comment as a block", C,
     "    if state == COMMENT and (label == TEXT or _lead(rem) > 3):\n",
     "    if False:\n"),
    ("M22 quote continues on a blank line (R237-3 F4)", C,
     "        if lead > 3 or rest[lead:lead + 1] != \">\":\n            return None\n",
     "        if _blank(rest):\n            return len(text)\n"
     "        if lead > 3 or rest[lead:lead + 1] != \">\":\n            return None\n"),
    ("M23 item content column ignores the marker's own indentation", C,
     "    end = _lead(rem) + (len(item.group(1)) + 1 if item.group(1) else 1)\n",
     "    end = (len(item.group(1)) + 1 if item.group(1) else 1)\n"),
    ("M24 tabs counted as one column in the layer", C,
     "    text = line.expandtabs(TAB_STOP)\n",
     "    text = line.replace(\"\\t\", \" \")\n"),
    ("M25 definition title may be single-quoted", G,
     "    r\"(?:%(b)s+\\\"(?:%(t)s|\\\\.)*\\\")?%(b)s*$\"",
     "    r\"(?:%(b)s+[\\\"'](?:%(t)s|\\\\.)*[\\\"'])?%(b)s*$\""),
    ("M26 an open paragraph holds every box, not only the innermost", C,
     "        holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)\n",
     "        holds = box.filled or para == PARAGRAPH\n"),
]


def run_one(pristine: Path, scratch: Path, mutant: tuple) -> dict:
    ident, target, old, new = mutant
    root = scratch / ident.split()[0]
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(pristine, root / "scripts")
    path = root / "scripts" / target
    text = path.read_text()
    count = text.count(old)
    row = {"id": ident, "file": target, "applies": count}
    if count != 1:
        row["verdict"] = "NOT APPLIED"
        return row
    path.write_text(text.replace(old, new))
    for gate in (["gen_toc.py", "--selftest"], ["check_em_dash.py", "--selftest"]):
        proc = subprocess.run([sys.executable, "-B", *gate], cwd=root / "scripts",
                              capture_output=True, text=True, timeout=900)
        out = proc.stdout + proc.stderr
        fails = [l for l in out.splitlines() if "FAIL" in l or l.startswith("[")][:12]
        row[gate[0]] = {"exit": proc.returncode, "tail": out.strip().splitlines()[-1:] if out.strip() else [],
                        "failing_lines": fails}
    killed = row["gen_toc.py"]["exit"] != 0 or row["check_em_dash.py"]["exit"] != 0
    row["verdict"] = "KILLED" if killed else "SURVIVED"
    return row


def main() -> int:
    pristine, scratch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    scratch.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=min(jobs, 8)) as pool:
        rows = list(pool.map(lambda m: run_one(pristine, scratch, m), MUTANTS))
    out.write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(f"{r['verdict']:11} {r['id']}"
              + (f"  [gen_toc exit {r['gen_toc.py']['exit']}: {r['gen_toc.py']['tail']}; "
                 f"em_dash exit {r['check_em_dash.py']['exit']}]" if "gen_toc.py" in r else f" (applies {r['applies']})"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
