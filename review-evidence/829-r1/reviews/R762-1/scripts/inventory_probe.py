#!/usr/bin/env python3
"""In a disposable checkout, re-pin only hashes of changed declared scripts and
report the first refusal that is about something else.
usage: inventory_probe.py <disposable checkout> <shfmt>"""
import hashlib, json, os, re, subprocess, sys
root, shfmt = sys.argv[1:3]
table_path = f"{root}/ci/image/command-table.json"
env = dict(os.environ, CI_IMAGE_SHFMT=shfmt, PYTHONPATH="scripts")
for step in range(12):
    done = subprocess.run(["python3", "scripts/ci_tool_inventory.py", "--check"], cwd=root, env=env,
                          capture_output=True, text=True, timeout=280)
    last = (done.stdout + done.stderr).strip().splitlines()[-1] if (done.stdout + done.stderr).strip() else ""
    print(f"step {step} rc {done.returncode}: {last[:600]}", flush=True)
    m = re.match(r"REFUSED: changed declared script '([^']+)'", last)
    if not m:
        break
    name = m.group(1)
    table = json.load(open(table_path))
    entry = table["scripts"][name]
    digest = hashlib.sha256(open(f"{root}/{name}", "rb").read()).hexdigest()
    def repin(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("sha256", "content_sha256") and isinstance(value, str):
                    node[key] = digest
                else:
                    repin(value)
    repin(entry)
    table["scripts"][name] = entry
    json.dump(table, open(table_path, "w"), indent=2, sort_keys=True)
    open(table_path, "a").write("\n")
