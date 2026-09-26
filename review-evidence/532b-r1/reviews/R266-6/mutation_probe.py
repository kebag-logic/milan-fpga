"""Mutation probes for PR #570's require_tool change, run against a disposable copy.

Usage: python3 -I mutation_probe.py <copy-root> <result.json>
Each mutant replaces one exact source fragment in <copy-root>/scripts/act_ci.py,
runs `python3 -I scripts/act_ci.py --selftest`, records exit code and failing
arms, and restores the original bytes. "expect" is the reviewer's prediction.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
target = root / "scripts" / "act_ci.py"
original = target.read_bytes()
digest = hashlib.sha256(original).hexdigest()

LOOKUP = "    found = shutil.which(name, path=SAFE_PATH)\n"
KEEP = "    if name == \"pasta\":\n        return str(pathlib.Path(found).absolute())\n"
RESOLVE = "    return str(pathlib.Path(found).resolve())\n"
LAUNCH = "        require_tool(\"pasta\"),\n        \"--runas\",\n"

MUTANTS = [
    ("M01", "revert: resolve pasta like every other tool", KEEP, "", "killed"),
    ("M02", "re-resolve the path at the uplink launch site", LAUNCH,
     "        str(pathlib.Path(require_tool(\"pasta\")).resolve()),\n        \"--runas\",\n", "killed"),
    ("M03", "preserve the symlink name of every tool", KEEP + RESOLVE,
     KEEP + "    return str(pathlib.Path(found).absolute())\n", "killed"),
    ("M04", "look pasta up on the ambient PATH", LOOKUP,
     "    found = shutil.which(name) if name == \"pasta\" else shutil.which(name, path=SAFE_PATH)\n", "killed"),
    ("M05", "fall back to the ambient PATH when SAFE_PATH lacks pasta", LOOKUP,
     "    found = shutil.which(name, path=SAFE_PATH) or (shutil.which(name) if name == \"pasta\" else None)\n",
     "killed"),
    ("M06", "return the bare name so the launcher searches its own PATH", KEEP,
     "    if name == \"pasta\":\n        return name\n", "killed"),
    ("M07", "drop the executable-bit requirement for pasta", LOOKUP,
     "    found = shutil.which(name, mode=os.F_OK, path=SAFE_PATH) if name == \"pasta\" "
     "else shutil.which(name, path=SAFE_PATH)\n", "killed"),
    ("M08", "accept any directory entry named pasta, even a dangling link", LOOKUP,
     "    found = next((str(pathlib.Path(d) / name) for d in SAFE_PATH.split(':') "
     "if os.path.lexists(pathlib.Path(d) / name)), None) if name == \"pasta\" "
     "else shutil.which(name, path=SAFE_PATH)\n", "killed"),
    ("M09", "CONTROL: resolve the directory but keep the final name", KEEP,
     "    if name == \"pasta\":\n        return str(pathlib.Path(found).parent.resolve() / name)\n", "survives"),
    ("M10", "widen the preserved set to a non-slot tool (sudo)", KEEP,
     "    if name in (\"pasta\", \"sudo\"):\n        return str(pathlib.Path(found).absolute())\n", "survives"),
    ("M11", "widen the preserved set to a slot tool (ip)", KEEP,
     "    if name in (\"pasta\", \"ip\"):\n        return str(pathlib.Path(found).absolute())\n", "killed"),
    ("M12", "return a cwd-relative spelling of the SAFE_PATH hit", KEEP,
     "    if name == \"pasta\":\n        return os.path.relpath(found)\n", "killed"),
]

results = []
for ident, title, old, new, expect in MUTANTS:
    text = original.decode("utf-8")
    count = text.count(old)
    if count != 1:
        results.append({"id": ident, "title": title, "error": f"fragment count {count}"})
        continue
    target.write_bytes(text.replace(old, new).encode("utf-8"))
    try:
        run = subprocess.run(
            [sys.executable, "-I", "scripts/act_ci.py", "--selftest"],
            cwd=root, capture_output=True, text=True, timeout=600, check=False,
        )
    finally:
        target.write_bytes(original)
    failing = [line.strip() for line in (run.stdout + run.stderr).splitlines()
               if line.lstrip().startswith(("FAIL", "fail "))]
    observed = "survives" if run.returncode == 0 else "killed"
    results.append({
        "id": ident, "title": title, "expect": expect, "observed": observed,
        "returncode": run.returncode, "failing_arms": failing,
        "tail": (run.stdout + run.stderr).splitlines()[-3:],
    })
assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, "copy not restored"
pathlib.Path(sys.argv[2]).write_text(json.dumps({"sha256_act_ci": digest, "mutants": results}, indent=2) + "\n")
for item in results:
    print(item["id"], item.get("observed"), "expect", item.get("expect"), item.get("failing_arms", item.get("error")))
sys.exit(0 if all(r.get("observed") == r.get("expect") for r in results) else 1)
