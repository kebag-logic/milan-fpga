#!/usr/bin/env python3
"""usage: command_table_staleness.py <checkout> <rev>...
For each rev, count the files pinned in ci/image/command-table.json 'scripts'
(path -> sha256) whose blob at that rev differs from the pin, or is absent.
Reads git objects only; for a submodule path it reads the gitlink's tree."""
import hashlib, json, subprocess, sys
root = sys.argv[1]
def blob(rev, path):
    r = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True)
    if r.returncode == 0:
        return r.stdout
    # Inside a submodule: resolve its gitlink at rev and read from the submodule's objects.
    for sub in ("gptp-processor", "protocol-processor", "third_party/lwSRP", "third_party/tsn-c-stack", "third_party/verilog-axis"):
        if path.startswith(sub + "/"):
            ls = subprocess.run(["git", "-C", root, "ls-tree", rev, sub], capture_output=True, text=True).stdout.split()
            if len(ls) >= 3:
                r = subprocess.run(["git", "-C", f"{root}/{sub}", "show", f"{ls[2]}:{path[len(sub)+1:]}"], capture_output=True)
                if r.returncode == 0:
                    return r.stdout
    return None
for rev in sys.argv[2:]:
    pins = json.loads(blob(rev, "ci/image/command-table.json"))["scripts"]
    stale, absent, ours = [], [], []
    for path, entry in sorted(pins.items()):
        content = blob(rev, path)
        if content is None:
            absent.append(path); continue
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            stale.append(path)
    delta = [p for p in stale if p in ("scripts/owned_process.py", "scripts/process_test_support.py",
             "scripts/test_suite_cancellation.py", "tb/verilator/gptp_shadow/test_mutant_lifecycle.py")]
    print(rev, "pins", len(pins), "stale", len(stale), "absent", len(absent), "stale-from-this-delta", delta)
