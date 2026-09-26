#!/usr/bin/env python3
"""Mutation probe for PR #570 (issue #532) at an exact head.

Usage: mutation_probe.py <repo-clone> <head-sha> <scratch-dir>

Exports <head-sha> with `git archive` into <scratch-dir>/tree-<name> per mutant,
applies one exact-string mutation to scripts/act_ci.py, runs the offline
`python3 -I scripts/act_ci.py --selftest` and records exit status, the arm
count and each failing arm. The clone itself is never modified.
"""
import pathlib
import shutil
import subprocess
import sys

REQ_OLD = '''    if name == "pasta":
        return str(pathlib.Path(found).absolute())
    return str(pathlib.Path(found).resolve())
'''
MUTANTS = {
    "M0-control-unchanged": [],
    "M1-require_tool-resolves-pasta-again": [
        (REQ_OLD, '''    return str(pathlib.Path(found).resolve())
'''),
    ],
    "M2-uplink-re-resolves-at-launch": [
        ('''        "--",
        require_tool("pasta"),''', '''        "--",
        str(pathlib.Path(require_tool("pasta")).resolve()),'''),
    ],
    "M3-every-tool-keeps-its-symlink": [
        (REQ_OLD, '''    return str(pathlib.Path(found).absolute())
'''),
    ],
    "M4-ambient-PATH-lookup": [
        ("    found = shutil.which(name, path=SAFE_PATH)\n",
         "    found = shutil.which(name)\n"),
    ],
    "M5-pasta-only-ambient-PATH": [
        (REQ_OLD, '''    if name == "pasta":
        return str(pathlib.Path(shutil.which(name) or found).absolute())
    return str(pathlib.Path(found).resolve())
'''),
    ],
    "M6-pasta-realpath": [
        (REQ_OLD, '''    if name == "pasta":
        return os.path.realpath(found)
    return str(pathlib.Path(found).resolve())
'''),
    ],
    "M8-also-preserve-non-slot-tool-sudo": [
        ('    if name == "pasta":\n        return str(pathlib.Path(found).absolute())\n',
         '    if name in ("pasta", "sudo"):\n        return str(pathlib.Path(found).absolute())\n'),
    ],
    "M7-pasta-resolves-only-parent-dir": [
        (REQ_OLD, '''    if name == "pasta":
        return str(pathlib.Path(found).parent.resolve() / "passt")
    return str(pathlib.Path(found).resolve())
'''),
    ],
}


def main() -> int:
    clone, head, scratch = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    results = []
    for name, edits in MUTANTS.items():
        tree = scratch / f"tree-{name}"
        if tree.exists():
            shutil.rmtree(tree)
        tree.mkdir()
        archive = subprocess.run(["git", "-C", clone, "archive", head], check=True, capture_output=True)
        subprocess.run(["tar", "-x", "-C", str(tree)], input=archive.stdout, check=True)
        target = tree / "scripts" / "act_ci.py"
        text = target.read_text(encoding="utf-8")
        for old, new in edits:
            if text.count(old) != 1:
                print(f"{name}: mutation anchor not unique ({text.count(old)})")
                return 2
            text = text.replace(old, new)
        target.write_text(text, encoding="utf-8")
        run = subprocess.run(
            [sys.executable, "-I", "scripts/act_ci.py", "--selftest"],
            cwd=tree, capture_output=True, text=True, timeout=1800,
        )
        lines = run.stdout.splitlines() + run.stderr.splitlines()
        oks = sum(1 for line in lines if line.startswith("  ok "))
        fails = [line.strip() for line in lines if line.startswith("  FAIL") or line.startswith("  fail")]
        verdict = "SURVIVED" if (edits and run.returncode == 0) else ("KILLED" if edits else ("PASS" if run.returncode == 0 else "CONTROL-FAILED"))
        results.append((name, run.returncode, oks, fails, verdict))
        (scratch / f"{name}.log").write_text(run.stdout + run.stderr, encoding="utf-8")
        shutil.rmtree(tree)
    for name, code, oks, fails, verdict in results:
        print(f"{name}: exit={code} ok_arms={oks} failing_arms={len(fails)} -> {verdict}")
        for line in fails:
            print(f"    {line}")
    bad = [r for r in results if r[4] in ("SURVIVED", "CONTROL-FAILED")]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
