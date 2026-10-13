"""Scratch (round 17): mutants of the pin proof's configuration checks (ctrl_build.py), each applied alone to a
disposable clone, then every pin control with the census and the figure check run (R584-14's run_pin_controls.py,
unchanged); prints each mutant's escaped controls and the run's summary. Restores the file.

usage: super_mutants17.py <disposable clone> <work dir> <driver.py> [mutant prefix ...]
"""
import shutil
import subprocess
import sys
from pathlib import Path

top, work, driver = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
target = top / "sw/firmware/ctrl/test/ctrl_build.py"
original = target.read_text(encoding="utf-8")
CALL = "    superproject_configured(root)\n"
READ = '    entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()\n'
LAZY = (', "GIT_NO_LAZY_FETCH": "1"}', "}")
SUPER_EXCEPT = ' and\n               not (scope == "command" and f"{key}={value}" == HELPER_CONFIG)]'
STACK_EXCEPT = '                       scope == "command" and f"{key}={value}" == HELPER_CONFIG)]'
HELPER = [('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"'),
          (SUPER_EXCEPT, ' and\n               not scope == "command"]'),
          (STACK_EXCEPT, '                       scope == "command")]')]
KEYS = ('("extensions.partialclone", "remote.promisor", "remote.partialclonefilter", "remote.uploadpack",\n'
        '                        "core.sshcommand", "core.fsmonitor")')
BOUND = "for scope, section, _, variable, key, value in configuration(root)\n"
MATCH = 'if f"{section}.{variable}" in SUPERPROJECT_REFUSED and\n'
ROUND16 = ('("extensions.partialclone", "remote.*.promisor", "remote.*.partialclonefilter", "remote.*.uploadpack", '
           '"core.sshcommand", "core.fsmonitor")')
PARSE = "return section, subsection if dot else None, variable"


def remote_only(condition: str) -> list[tuple[str, str]]:
    """The superproject's check refusing a remote key only where `condition` holds of its subsection."""
    bound = BOUND.replace(", _,", ", subsection,")
    return [(BOUND + "               " + MATCH,
             bound + "               " + MATCH.replace(" and\n", f' and (section != "remote" or {condition}) and\n'))]


MUTANTS = {"N0 none": []}
MUTANTS["N1 the superproject check not called"] = [(CALL, "")]
MUTANTS["N2 the superproject check after the index is read"] = [(CALL, ""), (READ, READ + CALL)]
MUTANTS["N3 the superproject's local scope only"] = [(MATCH, MATCH.replace("if ", 'if scope == "local" and ', 1))]
for key in ("extensions.partialclone", "remote.promisor", "remote.partialclonefilter", "remote.uploadpack",
            "core.sshcommand", "core.fsmonitor"):
    MUTANTS[f"N4 {key} not refused"] = [(KEYS, KEYS.replace(f'"{key}"', '"pin-control.none"'))]
MUTANTS["N5 the helper's own command-line setting refused in the superproject"] = [(SUPER_EXCEPT, "]")]
MUTANTS["N6 no HELPER_CONFIG"] = HELPER
MUTANTS["N7 no GIT_NO_LAZY_FETCH"] = [LAZY]
MUTANTS["N8 neither the superproject check nor GIT_NO_LAZY_FETCH"] = [(CALL, ""), LAZY]
MUTANTS["N9 neither the superproject check nor HELPER_CONFIG"] = [(CALL, ""), *HELPER]
MUTANTS["P1 round 16's match: a remote key with a named subsection only"] = [
    (BOUND, BOUND.replace(", _,", ", subsection,")),
    ('if f"{section}.{variable}" in SUPERPROJECT_REFUSED and',
     f"if family(section, subsection, variable) in {ROUND16} and")]
MUTANTS["P2 a remote key with a subsection, named or empty, only"] = remote_only("subsection is not None")
MUTANTS["P3 a remote key with a named subsection or none only"] = remote_only('subsection != ""')
MUTANTS["P4 the stack's `*` family holding an empty subsection too"] = [("named = \"*\" if subsection else '\"\"'",
                                                                         'named = "*"')]
MUTANTS["P5 parsed_key reading an empty subsection as none"] = [(PARSE, "return section, subsection or None, variable")]
MUTANTS["P6 parsed_key reading no subsection as an empty one"] = [(PARSE, "return section, subsection, variable")]
wanted = sys.argv[4:]
try:
    for name, edits in MUTANTS.items():
        if wanted and not any(name.startswith(w) for w in wanted):
            continue
        text = original
        for old, new in edits:
            assert text.count(old) == 1, (name, old)
            text = text.replace(old, new)
        assert text != original or not edits, name
        target.write_text(text, encoding="utf-8")
        try:
            own = work / f"{list(MUTANTS).index(name):02d}-{name[:2]}"
            shutil.rmtree(own, ignore_errors=True)
            res = subprocess.run([sys.executable, "-I", "-B", driver, str(top), str(own)],
                                 capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            print(f"== {name}: TIMEOUT after 300 s", flush=True)
            continue
        lines = res.stdout.splitlines()
        total = [ln for ln in lines if ln.startswith("run_pin_controls:")]
        escaped = [ln for ln in lines if ln.startswith("[ESCAPED]") or ln.startswith("  [FAIL]")]
        stopped = res.stderr.strip().splitlines()[-1:] if not total else []
        print(f"== {name}: rc={res.returncode} {total[-1] if total else 'stopped: ' + ' '.join(stopped)[:400]}; "
              f"escaped {len(escaped)}", flush=True)
        for ln in escaped:
            print("    " + ln[:400], flush=True)
finally:
    target.write_text(original, encoding="utf-8")
print("restored:", target.read_text(encoding="utf-8") == original)
