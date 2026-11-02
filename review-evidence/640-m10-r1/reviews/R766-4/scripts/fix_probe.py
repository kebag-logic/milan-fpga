"""Apply a proposed cell text to a copy of the plan in memory and report style findings near it.
Usage: python3 fix_probe.py <repo> <old> <new>"""
import sys
repo, old, new = sys.argv[1:4]
sys.path.insert(0, repo + "/scripts")
import check_doc_style as c
page = repo + "/docs/design/MARK_II_AREA_PLAN.md"
text = open(page).read()
assert text.count(old) == 1, "old text not unique"
line = text[: text.index(old)].count("\n") + 1
new_text = text.replace(old, new)
base = {(f.line, f.reason) for f in c.analyze(text)}
for f in c.analyze(new_text):
    if (f.line, f.reason) not in base:
        print("NEW", f.line, f.reason)
print("probed line", line, "done")
