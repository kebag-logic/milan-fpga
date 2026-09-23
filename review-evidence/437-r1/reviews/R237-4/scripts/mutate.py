#!/usr/bin/env python3
"""Reviewer mutation probes for #437's new walk properties.

Usage: mutate.py <head-scripts-dir> <scratch-dir> <out.json>

Each mutant copies the head `scripts/` directory into <scratch-dir>/<name>,
applies ONE exact text replacement (refused unless the old text occurs
exactly once), and runs both shipped self-tests from the copy:
`gen_toc.py --selftest` and `check_em_dash.py --selftest`. A mutant is
KILLED when either exits non-zero; the failing arm lines are kept. At most
8 mutants run at once. The head copy itself is run first as a control and
must pass both.
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

C, G = "gen_toc_containers.py", "gen_toc.py"
MUTANTS = [
    ("gate-ignored", G, "_opens(line, para, state, scope.gate)", "_opens(line, para, state)"),
    ("no-end-with-container", G, "if state in (FENCE, HTML) and owner not in scope.held_by:",
     "if False and state in (FENCE, HTML) and owner not in scope.held_by:"),
    ("comment-ends-with-container", G, "if state in (FENCE, HTML) and owner not in scope.held_by:",
     "if state in (FENCE, HTML, COMMENT) and owner not in scope.held_by:"),
    ("empty-comment-closes", G, "            scan, inside = scan[at + len(COMMENT_OPEN):], True\n",
     "            scan, inside = scan[at + len(COMMENT_OPEN):], True\n"
     "            if scan.startswith((\">\", \"->\")):\n"
     "                scan, inside = scan[1 if scan[0] == \">\" else 2:], False\n"),
    ("link-definition-ignored", C, "or not LINK_DEFINITION_RE.match(rem)):", "or True):"),
    ("holds-always", C, "holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)", "holds = True"),
    ("open-paragraph-not-held", C, "holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)",
     "holds = box.filled"),
    ("no-lazy", C, "if state == TEXT and para == PARAGRAPH and _lazy(rem):", "if False:"),
    ("blank-continues-quote", C, "            return None\n        return _quote_content(text, at + lead)",
     "            return len(text) if _blank(rest) else None\n        return _quote_content(text, at + lead)"),
    ("raw-3-5-never-ends", C, 'state, tag = (TEXT, "") if tag in rem else (HTML, tag)', "state, tag = (HTML, tag)"),
    ("raw-3-5-gate-not-none", C, "return _scope(walk, None if raw_3_5 else NO_PARAGRAPH)",
     "return _scope(walk, NO_PARAGRAPH)"),
    ("footnote-whitespace-continues", C, "return at if not text else None", "return at if not text.strip() else None"),
    ("any-ordinal-interrupts", C, "item.group(2) and int(item.group(1) or 1) == 1)):", "item.group(2))):"),
    ("wide-padding-is-content", C, "padding > TAB_STOP else end + padding", "padding > 99 else end + padding"),
    ("nested-container-no-fill", C, "    if walk.stack:\n        walk.stack[-1].filled = True\n    walk.serial += 1",
     "    walk.serial += 1"),
    ("inline-comment-opens-block", C, "if state == COMMENT and (label == TEXT or _lead(rem) > 3):", "if False:"),
    ("link-definition-title-any-quote", G, r'(?:%(b)s+\"(?:%(t)s|\\.)*\")?', r"(?:%(b)s+\S+)?"),
    ("footnote-needs-two", C, "    if lead >= TAB_STOP:\n        return at + TAB_STOP", "    if lead >= 2:\n        return at + 2"),
]


def run(copy: Path) -> dict:
    res = {}
    for key, script in (("toc", "gen_toc.py"), ("em", "check_em_dash.py")):
        p = subprocess.run([sys.executable, "-B", script, "--selftest"], cwd=copy,
                           capture_output=True, text=True, timeout=1800)
        lines = (p.stdout + p.stderr).splitlines()
        res[key] = {"exit": p.returncode, "tail": lines[-2:],
                    "failed_arms": [l for l in lines if "FAIL" in l or l.startswith("[I437") or "expected" in l][:6]}
    return res


def mutant(head: Path, scratch: Path, spec) -> dict:
    name, file, old, new = spec
    copy = scratch / name
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(head, copy)
    if name != "CONTROL":
        src = (copy / file).read_text()
        if src.count(old) != 1:
            return {"name": name, "error": f"old text occurs {src.count(old)} times"}
        (copy / file).write_text(src.replace(old, new))
    res = run(copy)
    killed = res["toc"]["exit"] != 0 or res["em"]["exit"] != 0
    return {"name": name, "file": file, "killed": killed, **res}


def main() -> int:
    head, scratch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    control = mutant(head, scratch, ("CONTROL", G, "", ""))
    print("CONTROL toc", control["toc"]["exit"], control["toc"]["tail"][-1:], "em", control["em"]["exit"], control["em"]["tail"][-1:])
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda s: mutant(head, scratch, s), MUTANTS))
    out.write_text(json.dumps({"control": control, "mutants": results}, indent=1))
    for r in results:
        if "error" in r:
            print(f"{r['name']:34} ERROR {r['error']}")
            continue
        print(f"{r['name']:34} {'KILLED' if r['killed'] else 'SURVIVED'} toc={r['toc']['exit']} em={r['em']['exit']} "
              f"| {(r['toc']['failed_arms'] or r['em']['failed_arms'] or [''])[0][:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
