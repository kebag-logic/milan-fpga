"""Resolve docs/findings/README.md: dev's 234 row, the branch's 649 row, each verbatim."""
import subprocess, sys
P = "docs/findings/README.md"
def show(rev):
    return subprocess.run(["git", "show", f"{rev}:{P}"], check=True, capture_output=True, text=True).stdout.splitlines(keepends=True)
base, ours, theirs = show("0a75aa77"), show("72816d26"), show("origin/dev")
assert len(base) == len(ours) == len(theirs)
diff_o = [i for i in range(len(base)) if base[i] != ours[i]]
diff_t = [i for i in range(len(base)) if base[i] != theirs[i]]
assert len(diff_o) == 1 and ours[diff_o[0]].startswith("| [649_"), diff_o
assert len(diff_t) == 1 and theirs[diff_t[0]].startswith("| [234_"), diff_t
out = list(base)
out[diff_o[0]] = ours[diff_o[0]]
out[diff_t[0]] = theirs[diff_t[0]]
open(P, "w").write("".join(out))
print(f"resolved: line {diff_t[0]+1} from origin/dev (234 row), line {diff_o[0]+1} from 72816d26 (649 row)")
