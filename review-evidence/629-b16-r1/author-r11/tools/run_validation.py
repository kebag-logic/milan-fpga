#!/usr/bin/env python3
"""Round 11 foreground validation dispatcher; inherited runners and probes retain their bytes.
Usage: run_validation.py MODE PREVIOUS_PACKET CANDIDATE_FIXTURE SOURCE_REPO SCRATCH
Run under the pinned parser. MODE: controls-N, self, parser, reader, layers, probes-N.
The fixture contains the candidate page, index, design reference and renderer; historical
Git reads use SOURCE_REPO. No repository or bench state is written.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
mode, previous, candidate, repository, scratch = sys.argv[1:]
p, c, repo, work = map(Path, (previous, candidate, repository, scratch))
o = Path(__file__).resolve().parents[1]
work.mkdir(parents=True, exist_ok=True)
gitdir = subprocess.run(["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
                       capture_output=True, text=True, check=True, timeout=15).stdout.strip()
os.environ["GIT_DIR"] = gitdir
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
page = c / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
check = o / "tools/check_b16_figures.py"
out = work / (mode + ".json")
if mode.startswith("probes-"):
    selection = mode[len("probes-"):]
    overlay = work.parent / "packet"
    sys.argv = [str(o / "tools/r11_probe_reruns.py"), str(c), str(overlay),
                str(p / "tools/review-probes"), str(work / mode),
                "ada26e56ac42ee5de311aef84cb86c8435b97cee"]
    ns = runpy.run_path(sys.argv[0])
    main = ns["main"]
    if selection.isdigit():
        group = int(selection)
        selected = dict(list(ns["PROBE"].items())[group * 5:(group + 1) * 5])
    else:
        selected = {selection: ns["PROBE"][selection]}
    main.__globals__["PROBE"] = selected
    raise SystemExit(main())
if mode.startswith("controls-"):
    n = mode.split("-")[1]
    script = p / ("tools/r" + n + "_check_controls.py")
    args = [check, page, p, work / mode, out]
elif mode in ("self", "layers"):
    script = p / ("tools/r10_self_probes.py" if mode == "self" else "tools/r10_layers.py")
    args = [check, page, p, work / mode, out]
elif mode in ("parser", "reader"):
    script = p / ("tools/r10_parser_extents.py" if mode == "parser" else "tools/r10_reader_controls.py")
    args = [check, c, work / mode, out]
else:
    raise SystemExit("unknown mode " + mode)
cmd = [sys.executable, "-I", str(script), *map(str, args)]
with (work / (mode + ".stdout")).open("w") as log:
    result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=570)
(work / (mode + ".rc")).write_text(str(result.returncode) + "\n")
print(json.dumps(dict(mode=mode, rc=result.returncode, receipt=out.name)), flush=True)
raise SystemExit(result.returncode)
