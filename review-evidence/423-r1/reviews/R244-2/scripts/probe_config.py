#!/usr/bin/env python3
"""Reviewer probe: hostile Git configuration and environment, whole CLI.

Builds the public matrix's positive replay (#1) and four lost-work histories
with the self-test's own builders, then runs the checker under each hostile
repository configuration or environment variable.  A lost-work history must
never read contained/0; a positive may fail closed (UNKNOWN) but must not
turn STRANDED into contained.

    probe_config.py <checker-src-dir> <scratch-dir> <out.json>
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HISTORIES = (("positive", "_s_positive", "contained"),
             ("revert-pr-commit", "_s_revert_c", "UNKNOWN"),
             ("partial-revert", "_s_revert_partial_hunk", "UNKNOWN"),
             ("omitted-linear", "_s_omit_linear", "STRANDED"),
             ("linear-missing-whitespace", "_s_whitespace", "STRANDED"))

HOSTILE = (
    ("baseline", {}, {}),
    ("color.ui=always", {"color.ui": "always"}, {}),
    ("color.diff=always", {"color.diff": "always"}, {}),
    ("diff.relative=true", {"diff.relative": "true"}, {}),
    ("diff.noprefix=true", {"diff.noprefix": "true"}, {}),
    ("diff.mnemonicPrefix=true", {"diff.mnemonicPrefix": "true"}, {}),
    ("diff.context=0", {"diff.context": "0"}, {}),
    ("diff.algorithm=histogram", {"diff.algorithm": "histogram"}, {}),
    ("diff.renames=copies", {"diff.renames": "copies"}, {}),
    ("diff.ignoreSubmodules=all", {"diff.ignoreSubmodules": "all"}, {}),
    ("core.quotePath=false", {"core.quotePath": "false"}, {}),
    ("i18n.logOutputEncoding=latin1", {"i18n.logOutputEncoding": "ISO-8859-1"}, {}),
    ("log.showSignature=true", {"log.showSignature": "true"}, {}),
    ("merge.conflictStyle=zdiff3", {"merge.conflictStyle": "zdiff3"}, {}),
    ("core.autocrlf=true", {"core.autocrlf": "true"}, {}),
    ("GIT_ICASE_PATHSPECS=1", {}, {"GIT_ICASE_PATHSPECS": "1"}),
    ("GIT_GLOB_PATHSPECS=1", {}, {"GIT_GLOB_PATHSPECS": "1"}),
    ("GIT_NOGLOB_PATHSPECS=1", {}, {"GIT_NOGLOB_PATHSPECS": "1"}),
    ("GIT_EXTERNAL_DIFF=false", {}, {"GIT_EXTERNAL_DIFF": "false"}),
    ("GIT_DIFF_OPTS=-u0", {}, {"GIT_DIFF_OPTS": "-u0"}),
    ("GIT_CONFIG_PARAMETERS color", {}, {"GIT_CONFIG_PARAMETERS": "'color.ui'='always'"}),
)


def main():
    src, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
    sys.path.insert(0, str(src))
    from merge_containment_selftest_replay import _History
    checker = src / "check_merge_containment.py"
    rows = []
    for label, builder, truth in HISTORIES:
        repo = scratch / label
        if repo.exists():
            shutil.rmtree(repo)
        repo.mkdir(parents=True)
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            getattr(_History(), builder)()
        finally:
            os.chdir(cwd)
        for name, config, env_extra in HOSTILE:
            for key, value in config.items():
                subprocess.run(("git", "-C", str(repo), "config", key, value), check=True)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **env_extra)
            p = subprocess.run((sys.executable, str(checker), "--no-fetch", "--base",
                                "main", "pr"), cwd=repo, env=env, capture_output=True)
            for key in config:
                subprocess.run(("git", "-C", str(repo), "config", "--unset", key), check=True)
            words = p.stdout.decode("utf-8", "replace").split()
            verdict = words[0] if words else "none"
            unsafe = truth != "contained" and (p.returncode == 0 or verdict == "contained")
            rows.append({"history": label, "truth": truth, "hostile": name,
                         "rc": p.returncode, "verdict": verdict, "unsafe": unsafe,
                         "note": p.stdout.decode("utf-8", "replace").splitlines()[:1],
                         "stderr": p.stderr.decode("utf-8", "replace")[-300:]})
    json.dump(rows, open(out, "w"), indent=1)
    for r in rows:
        flag = "UNSAFE" if r["unsafe"] else ("fail-closed" if r["verdict"] != r["truth"] else "")
        print(f"{r['history']:26} {r['hostile']:30} rc={r['rc']} {r['verdict']:10} {flag}")
    print("UNSAFE rows:", sum(r["unsafe"] for r in rows), "of", len(rows))


if __name__ == "__main__":
    main()
