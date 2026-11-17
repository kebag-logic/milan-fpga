"""Apply check_doc_style.analyze to pages outside its DOCUMENTS list and
report only findings on lines added since <base>.  usage: <repo> <base> <page>..."""
import subprocess, sys, re
from pathlib import Path
repo, base, pages = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as c
total = 0
for p in pages:
    diff = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "--", p], capture_output=True, text=True, check=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        s, n = int(m.group(1)), int(m.group(2) or 1)
        added |= set(range(s, s + n))
    found = [f for f in c.analyze((repo / p).read_text()) if f.line in added]
    total += len(found)
    print(f"{p}: {len(added)} added line(s), {len(found)} finding(s) on them")
    for f in found:
        print(f"  {p}:{f.line}: {f.reason}")
print(f"limits: sentence {c.MAX_SENTENCE_WORDS} words, paragraph {c.MAX_PARAGRAPH_WORDS} words / {c.MAX_PARAGRAPH_SENTENCES} sentences; total {total}")
