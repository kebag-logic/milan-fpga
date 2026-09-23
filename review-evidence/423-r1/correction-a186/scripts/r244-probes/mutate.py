"""Disposable mutation / restoration probes against copied scripts.

Each probe copies the exact-head scripts/ directory into its own scratch
directory, applies literal single-occurrence edits, and runs the unmodified
default self-test owner (check_merge_containment.py --selftest) from the review
clone. The review clone itself is never edited.

Usage: mutate.py <clone> <outdir> [probe-name ...]
"""
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
LATIN1 = {"LC_ALL": "en_US.ISO-8859-1", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
ASCII = {"LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}

R = "merge_containment_replay.py"
C = "check_merge_containment.py"
RET = "merge_containment_selftest_retention.py"

PROBES = {
    # --- controls: unmutated head under three parent locales ---
    "control-default": ([], {}),
    "control-latin1-parent": ([], LATIN1),
    "control-ascii-parent": ([], ASCII),
    # --- restoration of earlier corrections (expect a failing self-test) ---
    "restore-pre-b911-all": ([
        (C, 'return p.returncode, os.fsdecode(p.stdout).rstrip("\\n")',
            'return p.returncode, p.stdout.decode("utf-8", "surrogateescape").rstrip("\\n")'),
        (C, 'input=os.fsencode(patch)', 'input=patch.encode("utf-8", "surrogateescape")'),
        (R, 'name != os.fsencode(path)', 'name != path.encode("utf-8", "surrogateescape")'),
        (R, 'path = os.fsdecode(name)', 'path = name.decode("utf-8", "surrogateescape")'),
    ], {}),
    "restore-git-utf8-only": ([
        (C, 'return p.returncode, os.fsdecode(p.stdout).rstrip("\\n")',
            'return p.returncode, p.stdout.decode("utf-8", "surrogateescape").rstrip("\\n")'),
        (C, 'input=os.fsencode(patch)', 'input=patch.encode("utf-8", "surrogateescape")'),
    ], {}),
    "restore-replay-utf8-only": ([
        (R, 'name != os.fsencode(path)', 'name != path.encode("utf-8", "surrogateescape")'),
        (R, 'path = os.fsdecode(name)', 'path = name.decode("utf-8", "surrogateescape")'),
    ], {}),
    "restore-base-text-git": ([
        (C, 'capture_output=True)\n    return p.returncode, os.fsdecode(p.stdout).rstrip("\\n")',
            'capture_output=True, text=True)\n    return p.returncode, p.stdout.rstrip("\\n")'),
        (C, 'input=os.fsencode(patch),\n                       capture_output=True)\n    fields = p.stdout.decode("ascii").strip().split()',
            'input=patch, capture_output=True,\n                       text=True)\n    fields = p.stdout.strip().split()'),
    ], {}),
    "restore-pre-4671-latin1-parent": ([
        (RET, 'repr(literal_path) in output', 'repr(path) in output'),
    ], LATIN1),
    "restore-pre-4671-default-parent": ([
        (RET, 'repr(literal_path) in output', 'repr(path) in output'),
    ], {}),
    # --- guard mutations beyond the ten public ones ---
    "ancestor-regular-guard": ([
        (R, 'for entry in (original, tip, branch)):', 'for entry in (tip, branch)):'),
    ], {}),
    "retention-renames-folded": ([
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
            '"--ignore-submodules=none", "--name-only",'),
    ], {}),
    "retention-submodules-default": ([
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
            '"--name-only", "--no-renames",'),
    ], {}),
    "entry-name-check": ([
        (R, 'if (terminator or name != os.fsencode(path)', 'if (terminator'),
    ], {}),
    "entry-full-tree": ([
        (R, '"ls-tree", "-z",\n                   "--full-tree", commit', '"ls-tree", "-z",\n                   commit'),
    ], {}),
    "identity-oid-only": ([
        (R, '    if tip == branch:\n        return True',
            '    if tip == branch or (tip and branch and tip[2] == branch[2]):\n        return True'),
    ], {}),
    "merge-order-swapped": ([
        (R, 'for entry in (tip, original, branch)]', 'for entry in (branch, original, tip)]'),
    ], {}),
    "single-base-dropped": ([
        (R, 'if len(bases) != 1:', 'if not bases:'),
    ], {}),
    "distinct-replay-dropped": ([
        (C, '        candidates.remove(match)\n', '        pass\n'),
    ], {}),
    "conflict-style-override-dropped": ([
        (R, '_git_bytes("-c", "merge.conflictStyle=merge", "merge-file",', '_git_bytes("merge-file",'),
    ], {}),
}


def run(name, clone, outdir):
    edits, env_extra = PROBES[name]
    work = Path(outdir) / "mut" / name
    shutil.rmtree(work, ignore_errors=True)
    (work / "tmp").mkdir(parents=True)
    shutil.copytree(Path(clone) / "scripts", work / "scripts")
    for rel, before, after in edits:
        target = work / "scripts" / rel
        text = target.read_text()
        if text.count(before) != 1:
            return name, {"error": f"edit not unique in {rel}: {before[:60]!r} x{text.count(before)}"}
        target.write_text(text.replace(before, after))
    env = dict(os.environ, TMPDIR=str(work / "tmp"), **env_extra)
    if env_extra.get("LC_ALL") == "en_US.ISO-8859-1":
        env["LOCPATH"] = str(Path(outdir) / "tmp" / "locales")
    proc = subprocess.run((sys.executable, str(work / "scripts" / C), "--selftest"),
                          cwd=clone, env=env, capture_output=True, timeout=900)
    out = proc.stdout.decode("utf-8", "backslashreplace")
    (work / "selftest.out").write_bytes(proc.stdout + b"\n--stderr--\n" + proc.stderr)
    fails = [line.split()[1] for line in out.splitlines()
             if line.startswith("  FAIL") or line.startswith("  fail")]
    oks = sum(1 for line in out.splitlines() if line.startswith("  ok"))
    return name, {"rc": proc.returncode, "ok": oks, "fail_count": len(fails),
                  "fails_first": fails[:12], "last": out.strip().splitlines()[-1:] if out.strip() else [],
                  "stderr_tail": proc.stderr.decode("utf-8", "backslashreplace")[-300:]}


def main():
    clone, outdir = sys.argv[1], sys.argv[2]
    names = sys.argv[3:] or list(PROBES)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(pool.map(lambda n: run(n, clone, outdir), names))
    print(json.dumps(results, indent=1, ensure_ascii=True))


if __name__ == "__main__":
    main()
