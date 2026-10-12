"""The head's pinned_tree against ls-tree -r -t's listing (the round-13 reading) for the stack's pin."""
import os
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_build  # noqa: E402

stack, pin = ctrl_build.STACK, ctrl_build.stack_gitlink(root)
env = {"PATH": os.environ["PATH"], **ctrl_build.GIT_ENVIRONMENT}
out = subprocess.run(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin], capture_output=True,
                     env=env, check=True).stdout.decode()
old = {}
for entry in filter(None, out.split("\0")):
    meta, name = entry.split("\t", 1)
    mode, kind, oid = meta.split()
    old[name] = (mode, kind, "" if kind == "tree" else oid)
new = ctrl_build.pinned_tree(stack, pin, "sha1")
print(f"pin {pin}: ls-tree entries {len(old)}, pinned_tree entries {len(new)}, trees "
      f"{sum(v[1] == 'tree' for v in new.values())}, equal {old == new}")
sys.exit(0 if old == new else 1)
