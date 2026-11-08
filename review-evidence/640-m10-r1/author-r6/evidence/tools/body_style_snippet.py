import re, subprocess, sys
sys.path.insert(0, "scripts"); import check_doc_style as c
for page in ["docs/design/MARK_II_AREA_PLAN.md", "docs/design/AREA_BUDGET.md",
             "docs/design/MAILBOX_SPLIT.md", "docs/findings/README.md"]:
    diff = subprocess.run(["git", "diff", "-U0", "0a75aa77", "--", page], capture_output=True, text=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        added.update(range(int(m.group(1)), int(m.group(1)) + int(m.group(2) or 1)))
    text = open(page).read(); lines = text.splitlines()
    for f in c.analyze(text):
        end = f.line
        while end < len(lines) and lines[end].strip() and not lines[end].lstrip().startswith(("#", "|", "-", "```")):
            end += 1
        if any(f.line <= n <= end for n in added):
            print(page, f.line, f.reason)
