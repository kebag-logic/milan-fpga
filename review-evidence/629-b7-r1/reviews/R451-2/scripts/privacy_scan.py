#!/usr/bin/env python3
"""Scan for the two capture values that the evidence commit d36de704 masked, without printing them.

The values are recovered from d36de704's own diff: each removed line is paired with its added
line, and the text that the placeholders <capture-channels> and <capture-format> replaced is
taken as the value. The scan then counts, per file, the format value and the channel count in
its file-name form (<N>ch) and prose form (<N> channels), and prints only counts and the
values' SHA-256.

usage: privacy_scan.py <evidence git dir> <mask commit> <commit to scan>... -- <file>...
"""
import difflib, hashlib, re, subprocess, sys
args = sys.argv[1:]
sep = args.index("--")
gd, mask, scan, files = args[0], args[1], args[2:sep], args[sep + 1:]
git = lambda *a: subprocess.run(["git", "--git-dir", gd, *a], capture_output=True, check=True).stdout.decode("utf-8", "replace")
diff = git("diff", "-U0", f"{mask}^", mask, "--", "review-evidence/629-b7-r1/author/tools")
minus = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
plus = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
vals = {}
for a, b in zip(minus, plus):
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "replace":
            for ph in ("<capture-channels>", "<capture-format>"):
                if b[j1:j2] == ph or ph in b[j1:j2]:
                    v = a[i1:i2].strip().strip('"')
                    vals.setdefault(ph, set()).add(v)
assert all(len(v) == 1 for v in vals.values()) and len(vals) == 2, "could not recover exactly two values"
fmt = vals["<capture-format>"].pop(); nch = vals["<capture-channels>"].pop()
print("format value sha256", hashlib.sha256(fmt.encode()).hexdigest()[:16], "| channel value sha256", hashlib.sha256(nch.encode()).hexdigest()[:16])
pats = {"format": re.compile(re.escape(fmt)), "channels-filename": re.compile(rf"\b{re.escape(nch)}ch\b"),
        "channels-prose": re.compile(rf"\b{re.escape(nch)} (?:capture )?channels\b")}
def report(label, text):
    c = {k: len(p.findall(text)) for k, p in pats.items()}
    if any(c.values()):
        lines = [str(i) for i, l in enumerate(text.splitlines(), 1) if any(p.search(l) for p in pats.values())]
        print(f"{label}: {c} lines {','.join(lines[:12])}{' ...' if len(lines) > 12 else ''}")
    return sum(c.values())
for f in files:
    print(f"file {f}: total {report(f, open(f, encoding='utf-8', errors='replace').read())}")
for c in scan:
    names = git("ls-tree", "-r", "--name-only", c, "review-evidence/629-b7-r1").split()
    tot = nf = 0
    for n in names:
        t = git("show", f"{c}:{n}")
        k = report(f"{c[:8]}:{n.replace('review-evidence/629-b7-r1/', '')}", t) if n.endswith(("json", "jsonl", "txt", "md", "py", "log", "sh", "csv")) else 0
        tot += k; nf += bool(k)
    print(f"commit {c[:8]}: {nf} files, {tot} matches")
