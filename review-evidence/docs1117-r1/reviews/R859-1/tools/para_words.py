"""Count words per paragraph/bullet for every block that the diff base..head adds or changes.
usage: para_words.py <repo> <base> <head> <file>...   (prints block, words, start line)"""
import re, subprocess, sys
repo, base, head, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout
worst = 0
for f in files:
    text = git("show", f"{head}:{f}").splitlines()
    added = set()
    for h in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", git("diff", "-U0", base, head, "--", f), re.M):
        s, n = int(h.group(1)), int(h.group(2) or 1)
        added.update(range(s, s + n))
    # split into blocks: blank-line paragraphs; each list item its own block; fenced code skipped
    blocks, cur, fence = [], [], False
    for i, line in enumerate(text, 1):
        if line.lstrip().startswith("```"):
            if cur: blocks.append(cur); cur = []
            fence = not fence; continue
        if fence or not line.strip() or line.lstrip().startswith("|"):
            if cur: blocks.append(cur); cur = []
            continue
        if re.match(r"\s*(?:[-*]|\d+\.)\s", line) and cur:
            blocks.append(cur); cur = []
        cur.append((i, line))
    if cur: blocks.append(cur)
    for b in blocks:
        if not any(i in added for i, _ in b): continue
        words = re.sub(r"\]\([^)]*\)", "]", " ".join(l for _, l in b))   # link targets are not words
        words = re.sub(r"^\s*(?:[-*]|\d+\.)\s", "", words)
        n = len([w for w in words.split() if re.search(r"\w", w)])
        kind = "bullet" if re.match(r"\s*(?:[-*]|\d+\.)\s", b[0][1]) else "para"
        new = all(i in added for i, _ in b)
        worst = max(worst, n) if new else worst
        print(f"{f}:{b[0][0]}\t{kind}\t{'new' if new else 'touched'}\t{n}\t{b[0][1].strip()[:70]}")
print("max words in a wholly new block:", worst)
