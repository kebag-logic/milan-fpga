#!/usr/bin/env python3
"""Reviewer probe: a four-target report through a real process stdout.

Usage: stdout_probe.py <scripts-dir> <work-dir> <locpath>

Targets, in order: aa-ok (contained), pr-lost (STRANDED, note names raw
paths), pr-merge (UNKNOWN, note names raw paths), zz-later (contained).  The
report must be complete: four verdict lines in order, both summaries, exit 1,
an empty stderr, ASCII-only stdout, and every raw name quoted as its ASCII
byte literal.  Fixtures are built with raw Git plumbing only.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from locale_probe import LOCALES, OLD, CHANGED, EXTENDED, git, tree, commit, child_env  # noqa: E402

NAMES = (b"\xa1\xfe.txt", b"\xa2\x7e.txt", b"\x84\x41.txt", b"\x87\x90.txt",
         b"\xc3\xa9.txt", b"raw-\xff", b"tab\tcr\r\nlf\n")


def main():
    scripts, work, locpath = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    checker = scripts / "check_merge_containment.py"
    work.mkdir(parents=True, exist_ok=True)
    os.chdir(work)
    git("init", "-q", "-b", "main")
    original = commit(tree({n: OLD for n in NAMES} | {b"control": OLD}), [], "original")
    src_tree = tree({n: CHANGED for n in NAMES} | {b"control": OLD})
    linear = commit(src_tree, [original], "linear source")
    merge = commit(src_tree, [original, linear], "redundant merge")
    fin = tree({n: CHANGED for n in NAMES} | {b"control": CHANGED})
    branch = commit(fin, [merge], "source control edit")
    r1 = commit(src_tree, [original], "replay 1")
    r2 = commit(fin, [r1], "replay 2")
    main_tip = commit(tree({n: OLD for n in NAMES} | {b"control": EXTENDED}), [r2],
                      "revert every named file")
    lost = commit(tree({n: CHANGED.replace(b"line 10", b"never landed") for n in NAMES}
                       | {b"control": OLD}), [original], "never landed")
    for ref, oid in (("main", main_tip), ("aa-ok", original), ("pr-lost", lost),
                     ("pr-merge", branch), ("zz-later", original)):
        git("update-ref", "refs/heads/" + ref, oid)
    labels = [repr(n)[1:].encode("ascii") for n in NAMES]
    for label, lc_all, utf8, _pair in LOCALES:
        env = child_env(lc_all, utf8, locpath)
        r = subprocess.run((sys.executable, "-B", str(checker), "--no-fetch", "--base", "main",
                            "aa-ok", "pr-lost", "pr-merge", "zz-later"),
                           env=env, capture_output=True)
        lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
        words = [ln.split()[0].decode("ascii", "replace") for ln in lines[:4]]
        linear_line = next((ln for ln in lines if b"pr-lost" in ln), b"")
        merge_line = next((ln for ln in lines if b"pr-merge" in ln), b"")
        result = {
            "locale": label, "rc": r.returncode, "verdicts": words,
            "stderr_empty": r.stderr == b"",
            "ascii_stdout": r.stdout.isascii(),
            "stranded_summary": b"branch tip(s) have work" in r.stdout,
            "unknown_summary": b"lack a containment proof" in r.stdout,
            "stranded_names": sum(lab in linear_line for lab in labels),
            "unknown_names": sum(lab in merge_line for lab in labels),
            "stderr_tail": r.stderr.decode("ascii", "backslashreplace")[-200:]}
        result["pass"] = (r.returncode == 1 and words == ["contained", "STRANDED", "UNKNOWN", "contained"]
                          and result["stderr_empty"] and result["ascii_stdout"]
                          and result["stranded_summary"] and result["unknown_summary"]
                          and result["stranded_names"] == sum(n in NAMES for n in sorted((*NAMES, b"control"))[:6])
                          and result["unknown_names"] == len(NAMES))
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
