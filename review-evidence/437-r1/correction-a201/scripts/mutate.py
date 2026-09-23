#!/usr/bin/env python3
"""Named mutations of the A201 head, each applied to a disposable copy of
scripts/ and scored by both shipped self-tests. A mutation is killed when a
self-test fails; the failing arm names are recorded."""
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
CLONE = Path("$LANES/437-container-paragraph-scopes")
C, G = "gen_toc_containers.py", "gen_toc.py"
MUTATIONS = [
    ("M01", "R237-3 F2: a link reference definition fills its item", C,
     """    if walk.stack and not _blank(rem) and (
            walk.stack[-1].filled or label != TEXT
            or not LINK_DEFINITION_RE.match(rem)):""",
     """    if walk.stack and not _blank(rem):"""),
    ("M02", "R237-3 F2: an open paragraph of definitions does not hold its item", C,
     "holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)", "holds = box.filled"),
    ("M03", "R237-3 F2: a lazy line does not fill its item", C,
     """            walk.stack[-1].filled = True
            return _scope(walk, HELD)""", """            return _scope(walk, HELD)"""),
    ("M04", "a nested container does not fill its parent", C,
     """    if walk.stack:
        walk.stack[-1].filled = True
    walk.serial += 1""", """    walk.serial += 1"""),
    ("M05", "R237-3 F4: a blank line continues a block quote", C,
     """    if box.kind == QUOTE:
        if lead > 3""", """    if box.kind == QUOTE:
        if _blank(rest):
            return len(text)
        if lead > 3"""),
    ("M06", "R238-2 F2 C17: a type 3-5 block never ends", C,
     """state, tag = (TEXT, "") if tag in rem else (HTML, tag)""", """state, tag = (HTML, tag)"""),
    ("M07", "a type 3-5 opener counts as a lazy line", C,
     "FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)", "FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE)"),
    ("M08", "R238-2 F1(d): inside types 3 to 5 the gate is NO_PARAGRAPH", C,
     "return _scope(walk, None if raw_3_5 else NO_PARAGRAPH)", "return _scope(walk, NO_PARAGRAPH)"),
    ("M09", "a comment ends with the container it opened in", G,
     "if state in (FENCE, HTML) and owner not in scope.held_by:",
     "if state in (FENCE, COMMENT, HTML) and owner not in scope.held_by:"),
    ("M10", "a comment opened in prose ends at a blank line", G,
     """        if state in (FENCE, COMMENT, HTML):
            out.append(state)""", """        if state == COMMENT and not line.strip(CLASSES["blank"]):
            state = TEXT
        if state in (FENCE, COMMENT, HTML):
            out.append(state)"""),
    ("M11", "`<!-->` closes the comment it opens", G,
     "scan, inside = scan[at + len(COMMENT_OPEN):], True", 'scan, inside = scan[at + len("<!"):], True'),
    ("M12", "a fence or raw HTML block outlives its container", G,
     "if state in (FENCE, HTML) and owner not in scope.held_by:",
     "if False and state in (FENCE, HTML) and owner not in scope.held_by:"),
    ("M13", "a titled link reference definition is not one", G,
     r'''r"(?:%(b)s+\"(?:%(t)s|\\.)*\")?%(b)s*$"''', r'''r"%(b)s*$"'''),
    ("M14", "the title stop class loses the backslash", G,
     """    "title stop": '"\\\\\\\\',""", """    "title stop": '"',"""),
]


def score(mut):
    mid, prop, path, old, new = mut
    work = PACKET / "scratch" / "mut" / mid
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(CLONE / "scripts", work, ignore=shutil.ignore_patterns("__pycache__"))
    src = (work / path).read_text()
    assert src.count(old) == 1, (mid, src.count(old))
    (work / path).write_text(src.replace(old, new))
    out = {"id": mid, "property": prop, "file": path}
    for tool in ("gen_toc.py", "check_em_dash.py"):
        res = subprocess.run([sys.executable, "-B", str(work / tool), "--selftest"], cwd=CLONE,
                             capture_output=True, text=True)
        text = res.stdout + res.stderr
        failed = sorted(set(re.findall(r"FAIL \[([^\]]+)\]", text) + re.findall(r"^  - \[([^\]]+)\]", text, re.M)))
        guard = re.findall(r"GUARD (.*)", text)
        out[tool] = {"exit": res.returncode, "summary": (text.strip().splitlines() or [""])[-1],
                     "failed_arms": failed, "guards": guard}
    out["killed"] = any(out[t]["exit"] != 0 for t in ("gen_toc.py", "check_em_dash.py"))
    shutil.rmtree(work)
    return out


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(score, MUTATIONS))
    Path(sys.argv[1]).write_text(json.dumps(results, indent=1) + "\n")
    for r in results:
        arms = r["gen_toc.py"]["failed_arms"]
        print(f'{r["id"]} {"KILLED" if r["killed"] else "SURVIVED"} | {r["property"]} | TOC {r["gen_toc.py"]["summary"]} | '
              f'em-dash {r["check_em_dash.py"]["summary"]} | TOC arms: {arms[:4]}{" +%d" % (len(arms) - 4) if len(arms) > 4 else ""}')


if __name__ == "__main__":
    main()
