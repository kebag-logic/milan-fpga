#!/usr/bin/env python3
"""Reviewer mutation sweep over the containment checker's production guards.

Each mutant copies the exact-head scripts directory into a disposable tree,
applies exact byte edits (each `before` must occur exactly once), and runs
the unmodified default self-test (`check_merge_containment.py --selftest`)
from that copy.  KILLED means the self-test exited non-zero.

    probe_mutants.py <head-scripts-dir> <scratch-dir> <out.json> [jobs] [PATH-override]
"""
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPLAY = "merge_containment_replay.py"
GIT = "merge_containment_git.py"
CHECKER = "check_merge_containment.py"

MUTANTS = (
    ("control-unmodified", None, ()),
    # R244-C guards the author says are now killed
    ("single-merge-base", REPLAY, (("if len(bases) != 1:", "if not bases:"),)),
    ("t-ignore-submodules", REPLAY, (('"--ignore-submodules=none", "--name-only", "--no-renames",',
                                      '"--name-only", "--no-renames",'),)),
    ("t-no-renames", REPLAY, (('"--ignore-submodules=none", "--name-only", "--no-renames",',
                               '"--ignore-submodules=none", "--name-only",'),)),
    ("ancestor-type-rule", REPLAY, (("for entry in (original, tip, branch))",
                                     "for entry in (tip, branch))"),)),
    ("replay-distinctness", CHECKER, (("        candidates.remove(match)\n", "        pass\n"),)),
    # survivors the author lists
    ("tree-entry-name-check", REPLAY, (("if (terminator or name != path", "if (terminator"),)),
    ("tree-entry-full-tree", REPLAY, (('"--full-tree", commit', "commit"),)),
    ("merge-file-style-override", REPLAY, (('"-c", "merge.conflictStyle=merge", "merge-file"',
                                            '"merge-file"'),)),
    ("t-no-ext-diff-textconv", REPLAY, (('"diff", "--no-ext-diff", "--no-textconv",\n',
                                         '"diff",\n'),)),
    # reviewer-selected guards
    ("merge-file-argument-order", REPLAY, (("for entry in (tip, original, branch)]",
                                            "for entry in (branch, original, tip)]"),)),
    ("absence-asymmetry", REPLAY, (("    if tip is None or branch is None:\n        return False\n", ""),)),
    ("historical-error-to-decline", REPLAY, (("        if historical is None:\n"
                                              "            raise _MeasurementError(error)\n", ""),)),
    ("merge-error-range", REPLAY, (("if rc < 0 or rc > 127:", "if rc < 0:"),)),
    ("g1-parent-read-check", REPLAY, (("    if not parents or parents[0] != second:\n"
                                       '        raise _MeasurementError(f"could not read parents of {second}")\n', ""),)),
    ("lossy-guard-removed", GIT, (("    if os.fsencode(text) != out:\n        return RC_LOSSY_OUTPUT, \"\"\n", ""),)),
    ("lossy-status-zero", GIT, (("RC_LOSSY_OUTPUT = 256", "RC_LOSSY_OUTPUT = 0"),)),
    ("labels-decoded", GIT, (('    return repr(name)[1:]', '    return os.fsdecode(name)'),)),
    # restorations of the R244-1 lossy transports, one site at a time
    ("argv-bytes-lossy", GIT, (('    p = subprocess.run(("git", "--no-replace-objects", *args),',
                                '    args = [os.fsencode(os.fsdecode(a)) if isinstance(a, bytes) else a\n'
                                '            for a in args]\n'
                                '    p = subprocess.run(("git", "--no-replace-objects", *args),'),)),
    ("t-lookup-lossy", REPLAY, (("import tempfile\n", "import os\nimport tempfile\n"),
                                ("entries = [_tree_entry(commit, name)",
                                 "entries = [_tree_entry(commit, os.fsencode(os.fsdecode(name)))"))),
    ("patch-transport-lossy", CHECKER, (("import subprocess\n", "import os\nimport subprocess\n"),
                                        ('input=patch.rstrip(b"\\n"),',
                                         'input=os.fsencode(os.fsdecode(patch.rstrip(b"\\n"))),'))),
    ("path-arm-lossy", CHECKER, (("import subprocess\n", "import os\nimport subprocess\n"),
                                 ('    paths = [n for n in names.split(b"\\0") if n]\n    if not paths:',
                                  '    paths = [os.fsencode(os.fsdecode(n)) for n in names.split(b"\\0") if n]\n    if not paths:'))),
    # R244-B restoration: text-mode source copies in the mutation harness
    ("text-source-copies", "merge_containment_selftest_mutations.py", (
        ('checker = (source_dir / "check_merge_containment.py").read_bytes()',
         'checker = (source_dir / "check_merge_containment.py").read_text()'),
        ('transport = (source_dir / "merge_containment_git.py").read_bytes()',
         'transport = (source_dir / "merge_containment_git.py").read_text()'),
        ('(target / "checker.py").write_bytes(checker)',
         '(target / "checker.py").write_text(checker)'),
        ('(target / "merge_containment_git.py").write_bytes(transport)',
         '(target / "merge_containment_git.py").write_text(transport)'))),
    ("postimage-paths-lossy", CHECKER, (("import subprocess\n", "import os\nimport subprocess\n"),
                                        ('    return ([name for name in names.split(b"\\0") if name], None)',
                                         '    return ([os.fsencode(os.fsdecode(name)) for name in names.split(b"\\0") if name], None)'))),
)


def run(head, scratch, mutant, path_override):
    name, target, edits = mutant
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(head, tree / "scripts")
    if target:
        path = tree / "scripts" / target
        data = path.read_bytes()
        for before, after in edits:
            b, a = before.encode(), after.encode()
            if data.count(b) != 1:
                return {"mutant": name, "error": f"edit not unique: {before[:60]!r}"}
            data = data.replace(b, a)
        path.write_bytes(data)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LC_ALL="en_US.UTF-8",
               PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    env.pop("LOCPATH", None)
    if os.environ.get("PARENT") == "ascii":
        env["LC_ALL"] = "C"
    if path_override:
        env["PATH"] = path_override
    #! main() checks for grafts before --selftest, so it needs a repository
    #! as its working directory; an empty disposable one serves.
    subprocess.run(("git", "init", "-q", str(tree / "cwd")), check=True)
    subprocess.run(("git", "-C", str(tree / "cwd"), "-c", "user.name=Probe", "-c",
                    "user.email=probe@example.invalid", "-c", "commit.gpgsign=false",
                    "commit", "-q", "--allow-empty", "-m", "probe root"), check=True)
    p = subprocess.run((sys.executable, str(tree / "scripts" / CHECKER), "--selftest"),
                       capture_output=True, env=env, cwd=tree / "cwd")
    out = p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    fails = [ln.strip() for ln in out.splitlines() if re.match(r"\s+FAIL", ln)]
    return {"mutant": name, "file": target, "rc": p.returncode,
            "ok": len(re.findall(r"(?m)^\s+ok ", out)), "fail_count": len(fails),
            "not_run": [ln.strip() for ln in out.splitlines() if "NOT RUN" in ln],
            "first_fails": fails[:6],
            "tail": out.strip().splitlines()[-2:] if p.returncode and not fails else [],
            "verdict": ("CONTROL-PASS" if not target and p.returncode == 0 else
                        "CONTROL-FAIL" if not target else
                        "KILLED" if p.returncode else "SURVIVED")}


def main():
    head, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    path_override = sys.argv[5] if len(sys.argv) > 5 else None
    only = os.environ.get("ONLY")
    mutants = [m for m in MUTANTS if not only or m[0] in only.split(",")]
    scratch.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda m: run(head, scratch, m, path_override), mutants))
    json.dump(results, open(out, "w"), indent=1)
    for r in results:
        print(f"{r['mutant']:28} {r.get('verdict', 'ERROR'):13} rc={r.get('rc')} "
              f"ok={r.get('ok')} FAIL={r.get('fail_count')} notrun={len(r.get('not_run', []))}"
              f" {r.get('error', '')}")
        for f in r.get("first_fails", [])[:3]:
            print(f"      {f[:150]}")
        for t in r.get("tail", []):
            print(f"      tail: {t[:150]}")


if __name__ == "__main__":
    main()
