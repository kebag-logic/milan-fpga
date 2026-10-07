#!/usr/bin/env python3
"""Report control statements on added C lines whose body is not braced.
Usage: braces.py SRC BASE HEAD"""
import re, subprocess, sys
src, base, head = sys.argv[1:4]
diff = subprocess.run(["git", "-C", src, "diff", "-U0", f"{base}..{head}", "--", "*.c", "*.h"],
                      capture_output=True, text=True, check=True).stdout
added, path, line = {}, None, 0
for l in diff.splitlines():
    if l.startswith("+++ b/"):
        path = l[6:]; added[path] = set()
    elif l.startswith("@@"):
        m = re.search(r"\+(\d+)(?:,(\d+))?", l); line = int(m.group(1))
    elif l.startswith("+") and path:
        added[path].add(line); line += 1
bad = 0
for p, lines in added.items():
    text = subprocess.run(["git", "-C", src, "show", f"{head}:{p}"], capture_output=True, text=True).stdout
    body = text.splitlines()
    for n in sorted(lines):
        s = body[n - 1]
        m = re.match(r"\s*(?:\}\s*)?(else\s+if|if|for|while|else)\b", s)
        if not m or re.match(r"\s*\}?\s*while\s*\(.*\)\s*;", s) and "do" in "".join(body[max(0,n-40):n]):
            continue
        # gather the full header: balance parentheses
        j, chunk = n - 1, s
        if m.group(1) != "else":
            depth = 0; k = chunk.find("(")
            while True:
                depth = chunk.count("(") - chunk.count(")")
                if depth <= 0 or j + 1 >= len(body):
                    break
                j += 1; chunk += " " + body[j].strip()
        tail = chunk[chunk.rfind(")") + 1:] if m.group(1) != "else" else chunk[chunk.find("else") + 4:]
        if not tail.strip().startswith("{") and not tail.strip().startswith("if"):
            print(f"{p}:{n}: {s.strip()}"); bad += 1
print(f"unbraced added control lines: {bad}")
