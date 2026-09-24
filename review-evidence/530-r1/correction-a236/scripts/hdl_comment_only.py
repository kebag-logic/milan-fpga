#!/usr/bin/env python3
"""Prove a commit range changes only // comment lines under hdl/.

Usage: hdl_comment_only.py <clone> <from-rev> [<to-rev>=HEAD]

Two checks, both must hold:
1. every added or removed line in `git diff -U0 <from> <to> -- hdl/` is a
   pure // comment line;
2. for every changed hdl/ file, the text with // comments and blank lines
   removed is byte-identical at both revisions (sha256 printed).
"""
import hashlib, re, subprocess, sys

clone, frm = sys.argv[1], sys.argv[2]
to = sys.argv[3] if len(sys.argv) > 3 else "HEAD"
git = lambda *a: subprocess.run(["git", "-C", clone, *a], capture_output=True,
                                text=True, check=True).stdout
print("range", git("rev-parse", frm).strip(), "..", git("rev-parse", to).strip())
diff = git("diff", "-U0", frm, to, "--", "hdl/")
changed = [l for l in diff.splitlines()
           if l[:1] in "+-" and not l.startswith(("+++", "---"))]
bad = [l for l in changed if not re.match(r"^[+-]\s*//", l)]
print("check 1: changed lines", len(changed), "non-comment", len(bad))
for l in bad:
    print("  NON-COMMENT:", l)

def strip(text):
    out = []
    for line in text.splitlines():
        k = line.find("//")
        line = (line[:k] if k >= 0 else line).rstrip()
        if line:
            out.append(line)
    return "\n".join(out)

files = git("diff", "--name-only", frm, to, "--", "hdl/").split()
ok2 = True
for f in files:
    a = strip(git("show", f"{frm}:{f}"))
    b = strip(git("show", f"{to}:{f}"))
    lit = len(re.findall(r'"[^"\n]*//[^"\n]*"', git("show", f"{to}:{f}")))
    same = a == b
    ok2 &= same and lit == 0
    print(f"check 2: {f} stripped-equal={same} "
          f"{hashlib.sha256(a.encode()).hexdigest()[:16]} "
          f"{hashlib.sha256(b.encode()).hexdigest()[:16]} "
          f"string-literals-with-//={lit}")
verdict = not bad and ok2
print("VERDICT:", "COMMENT-ONLY" if verdict else "LOGIC CHANGED")
sys.exit(0 if verdict else 1)
