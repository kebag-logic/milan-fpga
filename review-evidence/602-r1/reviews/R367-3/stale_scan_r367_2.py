#!/usr/bin/env python3
"""R367-2 stale-claim scan: every tracked text file outside docs/history and the
submodules, lines where a PHC step / re-base / settime / adjtime / clock step
co-occurs (same line or +-2 lines) with an mr / MEDIA_RESET / restart term.

Usage: python3 stale_scan_r367_2.py <repo> > hits.txt
Each hit is printed with 2 lines of context for manual classification.
"""
import re
import subprocess
import sys
from pathlib import Path

STEP = re.compile(r"PHC[- ]step|PHC[- ]only|re-?base|settime|adjtime|clock step|gm ?step|"
                  r"media_rebase_p_w|a step\b|the step\b|every step\b|each step\b", re.I)
MR = re.compile(r"`mr`|\bmr\b|MEDIA_RESET|restart|mcr_restart_p_w|restart_p_i", re.I)
SKIP = ("docs/history/", "external/", "gptp-processor/", "protocol-processor/", "third_party/")
EXT = (".md", ".sv", ".svh", ".v", ".cpp", ".h", ".hpp", ".py", ".c", ".txt", ".yml", ".yaml",
       ".json", ".toml", ".sh", ".tcl", ".xdc", "Makefile", ".mk", ".rst")


def main():
    repo = Path(sys.argv[1])
    files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True,
                           text=True, check=True).stdout.split()
    n = 0
    for rel in files:
        if rel.startswith(SKIP) or not rel.endswith(EXT):
            continue
        try:
            lines = (repo / rel).read_text(errors="replace").splitlines()
        except (IsADirectoryError, FileNotFoundError):
            continue
        for i, line in enumerate(lines):
            if not STEP.search(line):
                continue
            window = " ".join(lines[max(0, i - 2): i + 3])
            if MR.search(window):
                n += 1
                print(f"== {rel}:{i + 1}")
                for j in range(max(0, i - 2), min(len(lines), i + 3)):
                    print(f"   {j + 1:5d}| {lines[j]}")
    print(f"TOTAL {n}")


if __name__ == "__main__":
    main()
