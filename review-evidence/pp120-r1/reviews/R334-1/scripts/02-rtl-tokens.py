#!/usr/bin/env python3
"""Compare HDL between commits after removing comments and whitespace.

Prints every non-comment token-line difference, so a reader sees the complete
functional RTL delta of the change (and that 691f1d2 -> head changed none)."""
import difflib, re, subprocess, sys

CLONE = sys.argv[1] if len(sys.argv) > 1 else "$REVIEWS/r334-1-pp120"
PAIRS = [("0922e43408f891fc0b84a84691df86b4fd0f1c0d", "a9b7874d415d935949becd7ccfd58799927efb08"),
         ("691f1d2b3a73705a50a8f827e2bb16837dc0dcdc", "a9b7874d415d935949becd7ccfd58799927efb08")]


def git(*args: str) -> str:
    """Return git stdout for the review clone."""
    return subprocess.run(["git", "-C", CLONE, *args], check=True,
                          capture_output=True, text=True).stdout


def strip(text: str) -> list[str]:
    """Remove // and /* */ comments, collapse whitespace, drop blank lines."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    return [" ".join(line.split()) for line in text.splitlines() if line.strip()]


for a, b in PAIRS:
    files = [f for f in git("diff", "--name-only", a, b, "--", "hdl").split() if f]
    print(f"== {a[:8]}..{b[:8]}: {len(files)} HDL file(s) changed")
    for f in files:
        old = strip(git("show", f"{a}:{f}")); new = strip(git("show", f"{b}:{f}"))
        d = [l for l in difflib.unified_diff(old, new, lineterm="", n=0)
             if not l.startswith(("---", "+++", "@@"))]
        print(f"-- {f}: {len(d)} non-comment line change(s)")
        for l in d:
            print("   " + l)
