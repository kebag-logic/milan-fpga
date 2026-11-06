#!/usr/bin/env python3
"""stopped_probe.py CHECKOUT WORK: the boundary gate's own ctrl_plat_image.py runs (ctrl_runs.image_runs), judged by
its own stopped_at_link, with whether an ELF was left."""
import subprocess, sys
from pathlib import Path
ck, work = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(ck / 'sw/firmware/ctrl/test'), str(ck / 'sw/firmware/gtest')]
import ctrl_runs
for label, argv in ctrl_runs.image_runs(work):
    if 'ctrl_plat_image.py' in label:
        res = subprocess.run(argv, cwd=ck, capture_output=True, text=True, check=False)
        out = Path(argv[argv.index('--output') + 1])
        print(f'{label}: rc {res.returncode}; stopped_at_link {ctrl_runs.stopped_at_link(argv, res)}; ELF {(out / "ctrl_app.elf").exists()}')
