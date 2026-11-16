#!/usr/bin/env python3
"""Record the exact review delta, history, new tests and coverage thresholds."""
from pathlib import Path
import re
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True)
print(git("log", "--format=%H %s", "16ba667d..70c100da"))
names = git("diff", "--name-only", "16ba667d..70c100da").splitlines()
print("Changed files", len(names))
print("\n".join(names))
assert len(names) == 33
assert not any(p.startswith("hdl/") or p == "docs/reference/MAILBOX_CONTRACT.md" for p in names)
print("PASS no RTL or mailbox-contract delta")
diff = git("diff", "--unified=0", "16ba667d..70c100da", "--", "sw/firmware/ctrl/test/test_aecp.cpp")
tests = [line[1:] for line in diff.splitlines() if line.startswith("+TEST_F(")]
assert len(tests) == 14
print("New tests", len(tests), *tests, sep="\n")
diff = git("diff", "--unified=0", "16ba667d..70c100da", "--", "sw/firmware/gtest/coverage.ratchet")
rows = [line[1:] for line in diff.splitlines() if line.startswith("+sw/")]
assert len(rows) == 6
for row in rows:
    assert all(a == b for a,b in re.findall(r"(\d+)/(\d+)", row))
print("Six changed files retain 100% line and branch thresholds:", *rows, sep="\n")
print("Threshold audit only; not a new coverage measurement.")
