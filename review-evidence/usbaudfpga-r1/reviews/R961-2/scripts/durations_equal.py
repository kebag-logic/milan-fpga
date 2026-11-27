#!/usr/bin/env python3
"""Compare the suite-duration table and provisional set at the reviewed head
(now in scripts/suite_durations.py) with the pre-refactor table in the
audio side's scripts/suite_shards.py plus the network side's usbnet entry."""
import ast, subprocess, sys
REPO, OURS, HEAD = sys.argv[1:4]
def src(rev, p):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{p}"],
                          capture_output=True, text=True, check=True).stdout
def assigns(text):
    out = {}
    for node in ast.parse(text).body:
        tgt = node.targets[0] if isinstance(node, ast.Assign) else getattr(node, "target", None)
        if isinstance(tgt, ast.Name) and node.value is not None:
            try:
                out[tgt.id] = ast.literal_eval(node.value)
            except Exception:
                if isinstance(node.value, ast.Call) and node.value.args:
                    try:
                        out[tgt.id] = frozenset(ast.literal_eval(node.value.args[0]))
                    except Exception:
                        pass
    return out
old = assigns(src(OURS, "scripts/suite_shards.py"))
new = assigns(src(HEAD, "scripts/suite_durations.py"))
print("old keys", len(old["SUITE_SECONDS"]), "new keys", len(new["SUITE_SECONDS"]))
print("SUITE_SECONDS equal:", old["SUITE_SECONDS"] == new["SUITE_SECONDS"])
print("PROVISIONAL equal:", old["PROVISIONAL_SUITES"] == new["PROVISIONAL_SUITES"], sorted(new["PROVISIONAL_SUITES"]))
