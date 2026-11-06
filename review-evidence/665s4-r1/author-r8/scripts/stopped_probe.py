#!/usr/bin/env python3
"""The boundary gate's own verdict on its own ctrl_plat_image.py run: its argv from ctrl_runs.image_runs, judged by
ctrl_runs.stopped_at_link. usage: stopped_probe.py <clone> <work>. Exit 0 when it stopped at its link with no ELF."""
import subprocess
import sys
from pathlib import Path

clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(clone / 'sw/firmware/ctrl/test'), str(clone / 'sw/firmware/gtest')]
import ctrl_runs  # noqa: E402

label, argv = next(r for r in ctrl_runs.image_runs(work) if 'ctrl_plat_image.py' in r[0])
res = subprocess.run(argv, cwd=clone, capture_output=True, text=True, check=False)
out = Path(argv[argv.index('--output') + 1])
ok = ctrl_runs.stopped_at_link(argv, res)
print(f'{label}: exit {res.returncode}; ELF present {(out / "ctrl_app.elf").exists()}; stopped_at_link {ok}')
print((res.stdout + res.stderr).strip().splitlines()[-1][:220])
sys.exit(0 if ok and not (out / 'ctrl_app.elf').exists() else 1)
