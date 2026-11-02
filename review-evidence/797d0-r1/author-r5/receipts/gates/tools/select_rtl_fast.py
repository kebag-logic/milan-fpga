#!/usr/bin/env python3
"""List the steps of rtl-fast.yml that read scripts/ or docs/: named in the step's own text, or in a tracked file it runs.

usage: select_rtl_fast.py <tree>
This is how rtl_fast_selection.json and the NOT RUN list were read off the workflow; verify_rtl_fast.py fails
on any step listed here with neither an rc of 0 nor a stated reason.
"""
import re, subprocess, sys
from pathlib import Path
import yaml


def selected(tree: Path):
    wf = yaml.safe_load((tree / ".github/workflows/rtl-fast.yml").read_text())
    tracked = set(subprocess.run(["git", "-C", str(tree), "ls-files"], capture_output=True, text=True).stdout.split())
    words = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+)")
    for job, body in wf["jobs"].items():
        for n, step in enumerate(body["steps"]):
            run = step.get("run")
            if not run:
                continue
            direct = "scripts/" in run or "docs/" in run
            hops = sorted({w for w in words.findall(run) if w in tracked and (tree / w).is_file()
                           and not w.endswith((".txt", ".json"))
                           and re.search(r"\bscripts/|\bdocs/", (tree / w).read_text(errors="replace"))})
            if direct or hops:
                yield job, step.get("id") or f"step{n}", step.get("name", ""), "direct" if direct else "through " + ", ".join(hops)


if __name__ == "__main__":
    for row in selected(Path(sys.argv[1])):
        print("\t".join(row))
