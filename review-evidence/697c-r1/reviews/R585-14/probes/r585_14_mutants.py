"""R585-14: mutants of the pin proof (ctrl_build.py), each applied alone to a disposable copy of the superproject,
then the pin controls run (r585_14_pin_controls.py); prints each mutant's escaped controls. Restores the file.
usage: python3 -I r585_14_mutants.py <disposable-superproject-copy> <work-dir> <driver.py> [MUTANT ...]"""
import subprocess
import sys
from pathlib import Path

top, work, driver = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
target = top / "sw/firmware/ctrl/test/ctrl_build.py"
original = target.read_bytes()
MUTANTS = {
    "MA-allowlist-not-checked": [("    configured(stack)\n    head = git(", "    head = git(")],
    "MB-hash-not-compared": [("    if held != oid:\n", "    if False:\n")],
    "MC-allowlist-after-object-reads": [("    configured(stack)\n    head = git(", "    head = git("),
                                        ("    found = on_disk(stack, algorithm)\n",
                                         "    configured(stack)\n    found = on_disk(stack, algorithm)\n")],
    "MD-no-helper-fsmonitor-setting": [('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"'),
                                       ('scope == "command" and f"{key}={value}" == HELPER_CONFIG',
                                        'scope == "command"')],
    "ME-no-lazy-fetch-variable-removed": [(', "GIT_NO_LAZY_FETCH": "1"}', '}')],
    "MF-any-local-key-accepted": [('scope in ("local", "worktree") and named in STACK_CONFIG',
                                   'scope in ("local", "worktree")')],
    "MG-trees-below-root-unchecked": [('        data = stored(stack, "tree", oid, algorithm, f"the pinned {prefix} tree" if '
                                       'prefix else "the pinned root tree")',
                                       '        data = stored(stack, "tree", oid, algorithm, "the pinned root tree") '
                                       'if not prefix else git(stack, "cat-file", "tree", oid).raw')],
    "MH-commit-unchecked": [('    head, _, _ = stored(stack, "commit", pin, algorithm, "the pinned commit").partition(b"\\n")',
                             '    head, _, _ = git(stack, "cat-file", "commit", pin).raw.partition(b"\\n")')],
    "MI-command-scope-any-key": [('scope == "command" and f"{key}={value}" == HELPER_CONFIG', 'scope == "command"')],
}
try:
    for name, edits in MUTANTS.items():
        if sys.argv[4:] and name not in sys.argv[4:]:
            continue
        text = original.decode()
        for old, new in edits:
            if text.count(old) != 1:
                print(f"{name}: NOT APPLIED ({old[:60]!r} found {text.count(old)} times)", flush=True)
                break
            text = text.replace(old, new)
        else:
            target.write_text(text)
            try:
                res = subprocess.run([sys.executable, "-I", driver, str(top), str(work / name)], capture_output=True,
                                     text=True, timeout=240)
            except subprocess.TimeoutExpired as exc:
                out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                print(f"{name}: TIMEOUT after 240 s (a control hung); last line: {out.splitlines()[-1:]}", flush=True)
                target.write_bytes(original)
                continue
            lines = res.stdout.splitlines()
            escaped = [ln for ln in lines if ln.startswith("[ESCAPED]")]
            total = [ln for ln in lines if ln.startswith("PIN CONTROLS")]
            print(f"{name}: rc={res.returncode} {total[-1] if total else res.stderr.strip()[-300:]}; "
                  f"escaped {len(escaped)}", flush=True)
            for ln in escaped:
                print("    " + ln[:230], flush=True)
        target.write_bytes(original)
finally:
    target.write_bytes(original)
