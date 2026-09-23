#!/usr/bin/env python3
"""Mutation, restoration and parent-locale probes against one source tree.

Adapted from the R244-1 reviewer's probes/mutate.py (copied unchanged in
r244-probes/).  Each probe copies <source-root>/scripts into its own scratch
directory, applies literal single-occurrence edits, and runs that copy's
unmodified default owner (check_merge_containment.py --selftest) from the lane
checkout, which is only read.  A mutant is killed when the self-test fails.

Usage: mutate_head.py <source-root> <label> [probe-name ...]
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
SCRATCH = PACKET / "scratch"
LOCALES = SCRATCH / "locales"
LANE = Path("$LANES/423-retained-redundant-replay")

LATIN1 = {"LC_ALL": "en_US.ISO-8859-1", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
          "LOCPATH": str(LOCALES)}
BIG5 = {"LC_ALL": "zh_TW.BIG5", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
        "LOCPATH": str(LOCALES)}
ASCII = {"LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
UTF8_STRICT = {"LC_ALL": "en_US.UTF-8", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
UTF8_MODE = {"PYTHONUTF8": "1"}

R = "merge_containment_replay.py"
C = "check_merge_containment.py"
G = "merge_containment_git.py"

PROBES = {
    # Unmutated source under six parent environments: all must pass.
    "control-default": ([], {}),
    "control-utf8-mode-parent": ([], UTF8_MODE),
    "control-utf8-strict-parent": ([], UTF8_STRICT),
    "control-ascii-parent": ([], ASCII),
    "control-latin1-parent": ([], LATIN1),
    "control-big5-parent": ([], BIG5),
    # R244-A: filename or patch bytes pass through the filesystem codec again.
    "lossy-git-bytes": ([
        (G, "    return p.returncode, p.stdout\n",
            "    return p.returncode, os.fsencode(os.fsdecode(p.stdout))\n"),
    ], {}),
    "restore-4671-replay-transport": ([
        (R, "import tempfile\n", "import os\nimport tempfile\n"),
        (R, "if (terminator or name != path", "if (terminator or name != os.fsencode(path)"),
        (R, "        try:\n            entries = [_tree_entry(commit, name)",
            "        path = os.fsdecode(name)\n        try:\n"
            "            entries = [_tree_entry(commit, path)"),
    ], {}),
    "restore-4671-patch-transport": ([
        (C, "import subprocess\nimport sys\n", "import os\nimport subprocess\nimport sys\n"),
        (C, 'rc, patch = _git_raw("show"', 'rc, patch = _git("show"'),
        (C, 'input=patch.rstrip(b"\\n")', "input=os.fsencode(patch)"),
    ], {}),
    "drop-lossy-output-guard": ([
        (G, "    if os.fsencode(text) != out:\n", "    if False:\n"),
    ], {}),
    # R244-D: diagnostics print decoded names again.
    "restore-raw-differing-names": ([
        (C, "import subprocess\nimport sys\n", "import os\nimport subprocess\nimport sys\n"),
        (C, "[path_label(n) for n in names.split(b\"\\0\") if n][:6]",
            "[os.fsdecode(n) for n in names.split(b\"\\0\") if n][:6]"),
    ], {}),
    "restore-decoded-unknown-labels": ([
        (R, "import tempfile\n", "import os\nimport tempfile\n"),
        (R, "unproved.append(path_label(name))", "unproved.append(repr(os.fsdecode(name)))"),
    ], {}),
    # R244-B: text copies of the sources under an ASCII parent.
    "restore-text-source-copies": ([
        ("merge_containment_selftest_mutations.py",
         '(source_dir / "check_merge_containment.py").read_bytes()',
         '(source_dir / "check_merge_containment.py").read_text()'),
        ("merge_containment_selftest_mutations.py",
         '(source_dir / "merge_containment_replay.py").read_bytes()',
         '(source_dir / "merge_containment_replay.py").read_text()'),
        ("merge_containment_selftest_mutations.py",
         '            before, after = before.encode("ascii"), after.encode("ascii")\n', ""),
        ("merge_containment_selftest_mutations.py",
         '(target / "checker.py").write_bytes(checker)',
         '(target / "checker.py").write_text(checker)'),
        ("merge_containment_selftest_mutations.py",
         '(target / "merge_containment_replay.py").write_bytes(mutated)',
         '(target / "merge_containment_replay.py").write_text(mutated)'),
    ], ASCII),
    # R244-C: the named T guards and replay distinctness.
    "single-base-dropped": ([(R, "if len(bases) != 1:", "if not bases:")], {}),
    "retention-renames-folded": ([
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
            '"--ignore-submodules=none", "--name-only",'),
    ], {}),
    "retention-submodules-default": ([
        (R, '"--ignore-submodules=none", "--name-only", "--no-renames",',
            '"--name-only", "--no-renames",'),
    ], {}),
    "ancestor-regular-guard": ([
        (R, "for entry in (original, tip, branch)):", "for entry in (tip, branch)):"),
    ], {}),
    "distinct-replay-dropped": ([
        (C, "        candidates.remove(match)\n", "        pass\n"),
    ], {}),
    # R244 survivors it did not raise; reported, not claimed killed.
    "entry-name-check": ([(R, "if (terminator or name != path", "if (terminator")], {}),
    "entry-full-tree": ([
        (R, '"ls-tree", "-z",\n                   "--full-tree", commit',
            '"ls-tree", "-z",\n                   commit'),
    ], {}),
    "conflict-style-override-dropped": ([
        (R, '_git_bytes("-c", "merge.conflictStyle=merge", "merge-file",',
            '_git_bytes("merge-file",'),
    ], {}),
}

#! A host without localedef: Latin-1 and Big5 children report NOT RUN, so only
#! the in-process Big5 codec control can kill the transport restorations.
NO_LOCALEDEF = {"PATH": str(SCRATCH / "nolocaledef-bin")}
for _name in ("control-default", "lossy-git-bytes", "restore-4671-replay-transport",
              "restore-4671-patch-transport", "drop-lossy-output-guard",
              "restore-raw-differing-names", "restore-decoded-unknown-labels"):
    PROBES[_name + "-no-localedef"] = (PROBES[_name][0], {**PROBES[_name][1], **NO_LOCALEDEF})


def run(name, root, outdir):
    edits, env_extra = PROBES[name]
    work = SCRATCH / ("mut-" + outdir.name) / name
    shutil.rmtree(work, ignore_errors=True)
    (work / "tmp").mkdir(parents=True)
    shutil.copytree(root / "scripts", work / "scripts")
    for rel, before, after in edits:
        target = work / "scripts" / rel
        data = target.read_bytes()
        if data.count(before.encode()) != 1:
            return name, {"error": f"edit not unique in {rel}: {before[:60]!r} "
                                   f"x{data.count(before.encode())}"}
        target.write_bytes(data.replace(before.encode(), after.encode()))
    env = dict(os.environ, TMPDIR=str(work / "tmp"), **env_extra)
    env.pop("PYTHONIOENCODING", None)
    if "LOCPATH" not in env_extra:
        env.pop("LOCPATH", None)
    proc = subprocess.run((sys.executable, "-B", str(work / "scripts" / C), "--selftest"),
                          cwd=LANE, env=env, capture_output=True, timeout=1800)
    (outdir / (name + ".out")).write_bytes(proc.stdout + b"\n--stderr--\n" + proc.stderr)
    out = proc.stdout.decode("utf-8", "backslashreplace")
    fails = [line.split()[1] for line in out.splitlines() if line.startswith("  FAIL")]
    oks = sum(1 for line in out.splitlines() if line.startswith("  ok"))
    not_run = [line.strip() for line in out.splitlines() if "NOT RUN" in line]
    shutil.rmtree(work, ignore_errors=True)
    return name, {"rc": proc.returncode, "ok": oks, "fail_count": len(fails),
                  "fails_first": fails[:12], "not_run": not_run,
                  "last": out.strip().splitlines()[-1:] if out.strip() else [],
                  "stderr_tail": proc.stderr.decode("utf-8", "backslashreplace")[-300:]}


def main():
    root, label = Path(sys.argv[1]).resolve(), sys.argv[2]
    names = sys.argv[3:] or list(PROBES)
    outdir = PACKET / "receipts" / ("mutations-" + label)
    outdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(pool.map(lambda n: run(n, root, outdir), names))
    (outdir / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=True) + "\n")
    for name, value in results.items():
        verdict = ("error" if "error" in value else
                   "PASS" if value["rc"] == 0 else "FAILS")
        print(f"{name:34} {verdict:5} rc={value.get('rc')} ok={value.get('ok')} "
              f"fail={value.get('fail_count')} {value.get('fails_first', [])[:3]} "
              f"{value.get('not_run') or ''} {value.get('error', '')}")


if __name__ == "__main__":
    main()
