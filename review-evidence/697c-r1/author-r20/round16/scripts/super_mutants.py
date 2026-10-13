"""Scratch (round 16): mutants of the superproject's configuration check (ctrl_build.py), each applied alone to a
disposable clone, then every pin control run (R585-14's r585_14_pin_controls.py, unchanged); prints each mutant's
escaped controls and whether Git ran a program. Restores the file.

usage: super_mutants.py <disposable clone> <work dir> <driver.py> [mutant prefix ...]
"""
import subprocess
import sys
from pathlib import Path

top, work, driver = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
target = top / "sw/firmware/ctrl/test/ctrl_build.py"
original = target.read_text(encoding="utf-8")
CALL = "    superproject_configured(root)\n"
READ = '    entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()\n'
LAZY = (', "GIT_NO_LAZY_FETCH": "1"}', "}")
HELPER = [('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"'),
          ('named in SUPERPROJECT_REFUSED and not (scope == "command" and f"{key}={value}" == HELPER_CONFIG)',
           'named in SUPERPROJECT_REFUSED and not scope == "command"'),
          ('scope == "command" and f"{key}={value}" == HELPER_CONFIG)]', 'scope == "command")]')]
KEYS = ('"extensions.partialclone", "remote.*.promisor", "remote.*.partialclonefilter",\n'
        '                        "remote.*.uploadpack", "core.sshcommand", "core.fsmonitor")')
MUTANTS = {"N0 none": []}
MUTANTS["N1 the superproject check not called"] = [(CALL, "")]
MUTANTS["N2 the superproject check after the index is read"] = [(CALL, ""), (READ, READ + CALL)]
MUTANTS["N3 the superproject's local scope only"] = [
    ("if named in SUPERPROJECT_REFUSED and not", 'if scope == "local" and named in SUPERPROJECT_REFUSED and not')]
for key in ("extensions.partialclone", "remote.*.promisor", "remote.*.partialclonefilter", "remote.*.uploadpack",
            "core.sshcommand", "core.fsmonitor"):
    MUTANTS[f"N4 {key} not refused"] = [(KEYS, KEYS.replace(f'"{key}"', '"pin-control.none"'))]
MUTANTS["N5 the helper's own command-line setting refused in the superproject"] = [
    (' and not (scope == "command" and f"{key}={value}" == HELPER_CONFIG)]', "]")]
MUTANTS["N6 no HELPER_CONFIG"] = HELPER
MUTANTS["N7 no GIT_NO_LAZY_FETCH"] = [LAZY]
MUTANTS["N8 neither the superproject check nor GIT_NO_LAZY_FETCH"] = [(CALL, ""), LAZY]
MUTANTS["N9 neither the superproject check nor HELPER_CONFIG"] = [(CALL, ""), *HELPER]
wanted = sys.argv[4:]
try:
    for name, edits in MUTANTS.items():
        if wanted and not any(name.startswith(w) for w in wanted):
            continue
        text = original
        for old, new in edits:
            assert text.count(old) == 1, (name, old)
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
        try:
            res = subprocess.run([sys.executable, "-I", "-B", driver, str(top), str(work / name[:2])],
                                 capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            print(f"== {name}: TIMEOUT after 300 s", flush=True)
            continue
        lines = res.stdout.splitlines()
        total = [ln for ln in lines if ln.startswith("PIN CONTROLS")]
        escaped = [ln for ln in lines if ln.startswith("[ESCAPED]")]
        print(f"== {name}: rc={res.returncode} {total[-1] if total else res.stderr.strip()[-300:]}; "
              f"escaped {len(escaped)}", flush=True)
        for ln in escaped:
            print("    " + ln[:400], flush=True)
finally:
    target.write_text(original, encoding="utf-8")
print("restored:", target.read_text(encoding="utf-8") == original)
