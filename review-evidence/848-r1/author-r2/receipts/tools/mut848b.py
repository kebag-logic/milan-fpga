#!/usr/bin/env python3
"""Mutants aimed at the round-2 change: each is one exact, unique text replacement, graded by --selftest.

usage: mut848b.py <script> <work dir>
`want` is the expected verdict. Three SURVIVED rows are deliberate: two put the old grading back beside a mutant, to
show the new grading is what kills it, and one is S9, answered as equivalent. Any missed expectation fails this script.
"""
import subprocess
import sys
from pathlib import Path

GRADE = 'if text not in (listed if text.startswith("## D0-") else rendered):'
SOURCE = 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")'
ROW = 'for p in pages if p.area == area]'
GROUP = 'grouped.setdefault(lanes[finding.page], []).append((finding, line))'
LOCATED = 'where = "on page" if line else "re-verify: quote not found"'
OLD_GRADE = 'if text not in rendered + listed:'
GATE = 'if actual == expected and not broken:'
RULE = 'if page_findings and state == "current":'
M = [
    # the findings, one mutant per required outcome
    ("R787-F1/R788-F1 page row loses the recording page", [(SOURCE, 'f"| {cell(finding.source)} | {cell(finding.correction)} |")')], "killed"),
    ("R787-F2 own Inventory row dropped while counted", [(ROW, 'for p in pages if p.area == area and p.path != OUTPUT]')], "killed"),
    ("R787-F3 lane keeps only its first finding", [(GROUP, 'grouped.setdefault(lanes[finding.page], [(finding, line)])')], "killed"),
    ("R787-F3 lane keeps only its last finding", [(GROUP, 'grouped[lanes[finding.page]] = [(finding, line)]')], "killed"),
    ("R787-F3 lane file drops the statement", [('f"- Statement: {finding.quote}", ', '')], "killed"),
    ("R788-F2 lane file drops the source", [('f"- Contradicted by: {source_of(finding)}",', '')], "killed"),
    ("R788-F2 lane file drops the correction", [('f"- Correction: {finding.correction}", ""]', '""]')], "killed"),
    ("R787-F4 page loses the Located sentence", [('"`Located` says whether the quote is still on its page.",\n', '\n')], "killed"),
    ("R787-F4 page loses the route to a line", [('"`python3 scripts/docs_inventory.py --findings-dir DIR` writes each finding\'s line, one file per lane.", "",\n', '"",\n')], "killed"),
    ("R787-F4 page loses the way to a row a search misses", [('"A text search misses a wrapped or marked-up copy.", "That command still names its line.", "",\n', '')], "killed"),
    # the needle grading selects the right output in both directions
    ("harness: every needle graded on the page alone", [(GRADE, 'if text not in rendered:')], "killed"),
    ("harness: every needle graded on the lane files alone", [(GRADE, 'if text not in listed:')], "killed"),
    ("harness: the two outputs swapped", [(GRADE, 'if text not in (rendered if text.startswith("## D0-") else listed):')], "killed"),
    # attribution: with the old grading back, the page mutant survives
    ("attribution: old grading + page row mutant", [(GRADE, OLD_GRADE), (SOURCE, 'f"| {cell(finding.source)} | {cell(finding.correction)} |")')], "SURVIVED"),
    ("attribution: old grading alone is otherwise green", [(GRADE, OLD_GRADE)], "SURVIVED"),
    # the new prose must not satisfy a needle that means a cell
    ("vacuity: Located always says on page", [(LOCATED, 'where = "on page"')], "killed"),
    ("vacuity: Located always says re-verify", [(LOCATED, 'where = "re-verify: quote not found"')], "killed"),
    ("vacuity: lost quote cell blank", [(LOCATED, 'where = "on page" if line else "--"')], "killed"),
    # the reviewers' survivors at 212b7d6e that were not findings, one by one
    ("survivor R787 S6: banner window grows past the rule", [('BANNER_SCAN_LINES = 15', 'BANNER_SCAN_LINES = 10000')], "killed"),
    ("survivor R788: page drops the verified baseline", [('f"Statements on D0 pages were checked at dev `{verified_at}`."', '"Statements on D0 pages were checked."')], "killed"),
    ("survivor R788: page correction cell blank", [('| {cell(source_of(finding))} | {cell(finding.correction)} |', '| {cell(source_of(finding))} | -- |')], "killed"),
    ("survivor R788: line count reaches a heading-less page's purpose", [('return cell(PurePosixPath(path).name)\n', 'return cell(PurePosixPath(path).name) + str(text.count(chr(10)))\n')], "killed"),
    # the one survivor answered rather than killed: S9 = R788 'check ignores the status rule'
    ("survivor S9: gate ignores the rule, generator intact (equivalent)", [(GATE, 'if actual == expected:')], "SURVIVED"),
    ("S9 paired: generator loses the rule", [(RULE, 'if False:')], "killed"),
    ("S9 paired: generator loses the rule and the gate ignores it", [(RULE, 'if False:'), (GATE, 'if actual == expected:')], "killed"),
]


def main() -> int:
    """Grade every mutant; 1 when any row misses its expected verdict."""
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    work = Path(sys.argv[2])
    work.mkdir(parents=True, exist_ok=True)
    missed = 0
    for index, (name, edits, want) in enumerate(M):
        text = source
        for old, new in edits:
            assert text.count(old) == 1, (name, old, text.count(old))
            text = text.replace(old, new)
        target = work / f"m{index:02d}" / "scripts" / "docs_inventory.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True, timeout=120)
        verdict = "killed" if done.returncode else "SURVIVED"
        lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
        ok = verdict == want
        missed += not ok
        print(f"{'ok ' if ok else 'BAD'} {verdict:8} want {want:8} rc={done.returncode} :: {name} :: {lines[0][:110] if lines else ''}", flush=True)
    print(f"{len(M)} mutants, {missed} missed their expectation")
    return 1 if missed else 0


raise SystemExit(main())
