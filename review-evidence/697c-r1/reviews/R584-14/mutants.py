# Reviewer mutation driver (R584-14): one source mutant of the pin proof, on a disposable full copy of the clone.
# Usage: python3 -I mutants.py <clone-root> <scratch-dir> <mutant>
# Copies <clone-root> (its .git and the initialised tsn-c-stack submodule with it) to <scratch-dir>/<mutant>,
# applies the mutant to the copy's sw/firmware/ctrl/test/ctrl_build.py (refusing if its anchor is absent), then
# runs run_pin_controls.py (beside this script) on the copy and prints the ESCAPED controls. The clone is only read.
import shutil
import subprocess
import sys
from pathlib import Path

B = "sw/firmware/ctrl/test/ctrl_build.py"
MUTANTS = {
    "M0-none": [],
    "M1-no-object-hash": [("    if held != oid:\n", "    if False:\n")],
    "M2-stack-allowlist-not-called": [("    configured(stack)\n    head = git(", "    head = git(")],
    "M3-superproject-check-not-called": [("    superproject_configured(root)\n", "")],
    "M4-no-helper-fsmonitor": [('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"')],
    "M5-no-lazy-fetch-variable": [(', "GIT_NO_LAZY_FETCH": "1"}', "}")],
    "M6-superproject-local-scope-only": [("               if named in SUPERPROJECT_REFUSED and",
                                          "               if scope == 'local' and named in SUPERPROJECT_REFUSED and")],
    "M7-tree-walk-not-recursing": [('                trees.append((f"{prefix}{name}/", child))\n',
                                    "                pass\n")],
    "M8-stack-allowlist-after-object-reads": [
        ("    configured(stack)\n    head = git(", "    head = git("),
        ("    want = pinned_tree(stack, pin, algorithm)\n", "    want = pinned_tree(stack, pin, algorithm)\n"
                                                         "    configured(stack)\n")],
}

root, scratch, name = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
copy = scratch / name
if copy.exists():
    shutil.rmtree(copy)
shutil.copytree(root, copy, symlinks=True)
target = copy / B
text = target.read_text(encoding="utf-8")
for old, new in MUTANTS[name]:
    if text.count(old) != 1:
        sys.exit(f"{name}: anchor not found exactly once: {old!r}")
    text = text.replace(old, new)
target.write_text(text, encoding="utf-8")
work = scratch / f"{name}-work"
if work.exists():
    shutil.rmtree(work)
res = subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("run_pin_controls.py")), str(copy), str(work)],
                     capture_output=True, text=True)
lines = res.stdout.splitlines()
escaped = [ln for ln in lines if ln.startswith("[ESCAPED]") or ln.startswith("  [FAIL]")]
print(f"{name}: rc={res.returncode}; {lines[0] if lines else ''}")
for ln in escaped:
    print("  " + ln[:400])
print("  " + (lines[-1] if lines else res.stderr.strip()[-400:]))
shutil.rmtree(copy, ignore_errors=True)
shutil.rmtree(work, ignore_errors=True)
