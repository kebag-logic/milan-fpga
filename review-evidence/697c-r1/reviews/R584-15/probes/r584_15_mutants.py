# Reviewer mutation driver (R584-15): one source mutant of the pin proof, on a disposable full copy of the clone.
# Usage: python3 -I r584_15_mutants.py <clone-root> <scratch-dir> <mutant>
# Copies <clone-root> (its .git and the initialised tsn-c-stack submodule with it) to <scratch-dir>/<mutant>,
# applies the mutant to the copy's sw/firmware/ctrl/test/ctrl_build.py (refusing if an anchor is not found exactly
# once), then runs R584-14's run_pin_controls.py (its published copy, prior-R584-14/ beside this script) on the
# copy and prints every ESCAPED control and FAIL line. The Git is the first `git` on PATH. The clone is only read.
import shutil
import subprocess
import sys
from pathlib import Path

B = "sw/firmware/ctrl/test/ctrl_build.py"
SUPER_IF = '               if f"{section}.{variable}" in SUPERPROJECT_REFUSED and\n'
SUPER_FOR = '    refused = [f"{key} ({scope})" for scope, section, _, variable, key, value in configuration(root)\n'
SUPER_FOR_NAMED = '    refused = [f"{key} ({scope})" for scope, section, subsection, variable, key, value in configuration(root)\n'
MUTANTS = {
    "M00-none": [],
    # Round 16's match: a remote's key refused only with a named subsection.
    "M01-remote-named-subsection-only": [
        (SUPER_FOR, SUPER_FOR_NAMED),
        (SUPER_IF, '               if f"{section}.{variable}" in SUPERPROJECT_REFUSED and '
                   '(section != "remote" or bool(subsection)) and\n')],
    # A remote's key refused with a named or empty subsection, not with none.
    "M02-remote-subsection-required": [
        (SUPER_FOR, SUPER_FOR_NAMED),
        (SUPER_IF, '               if f"{section}.{variable}" in SUPERPROJECT_REFUSED and '
                   '(section != "remote" or subsection is not None) and\n')],
    # A remote's key refused with a named subsection or none, not with an empty one.
    "M03-remote-empty-subsection-passes": [
        (SUPER_FOR, SUPER_FOR_NAMED),
        (SUPER_IF, '               if f"{section}.{variable}" in SUPERPROJECT_REFUSED and '
                   '(section != "remote" or subsection != "") and\n')],
    # The parser reads an empty subsection as none.
    "M04-parser-empty-as-none": [("    return section, subsection if dot else None, variable\n",
                                  "    return section, subsection if dot and subsection else None, variable\n")],
    # The stack's family reads an empty subsection as named.
    "M05-family-empty-as-named": [("    named = \"*\" if subsection else '\"\"'\n", "    named = \"*\"\n")],
    "M06-superproject-check-not-called": [("    superproject_configured(root)\n", "")],
    "M07-superproject-check-after-index-read": [
        ("    superproject_configured(root)\n    entry = git(root, \"ls-files\", \"--stage\", \"--\", rel).stdout.split()\n",
         "    entry = git(root, \"ls-files\", \"--stage\", \"--\", rel).stdout.split()\n    superproject_configured(root)\n")],
    "M08-no-object-hash": [("    if held != oid:\n", "    if False:\n")],
    "M09-stack-allowlist-not-called": [("    configured(stack)\n    head = git(", "    head = git(")],
    "M10-no-helper-fsmonitor": [('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"')],
    "M11-no-lazy-fetch-variable": [(', "GIT_NO_LAZY_FETCH": "1"}', "}")],
    "M12-tree-walk-not-recursing": [('                trees.append((f"{prefix}{name}/", child))\n', "                pass\n")],
    # The superproject's worktree scope left out.
    "M13-superproject-local-scope-only": [(SUPER_IF, '               if scope != "worktree" and '
                                                     'f"{section}.{variable}" in SUPERPROJECT_REFUSED and\n')],
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
runner = Path(__file__).resolve().parent / "prior-R584-14" / "run_pin_controls.py"
res = subprocess.run([sys.executable, "-I", str(runner), str(copy), str(work)], capture_output=True, text=True)
lines = res.stdout.splitlines()
escaped = [ln for ln in lines if ln.startswith("[ESCAPED]") or ln.startswith("  [FAIL]")]
print(f"{name}: rc={res.returncode}; {lines[0] if lines else ''}")
print(f"  ESCAPED/FAIL lines: {len(escaped)}")
for ln in escaped:
    print("  " + ln[:600])
print("  " + (lines[-1] if lines else res.stderr.strip()[-600:]))
shutil.rmtree(copy, ignore_errors=True)
shutil.rmtree(work, ignore_errors=True)
