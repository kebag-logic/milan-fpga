#!/usr/bin/env python3
"""refusal_edges.py CHECKOUT BOOT WORK: ctrl_plat_image.py's no-map refusal at its edges, on a finished split boot's
inputs, then the page's fence as written. One line per case: rc, ELF left or not, the last line said."""
import os, re, subprocess, sys
from pathlib import Path

checkout, boot, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)
libc, rt = boot / 'runtime/libc.a', boot / 'runtime/libcompiler_rt.a'
base = [sys.executable, '-B', 'sw/firmware/ctrl/test/ctrl_plat_image.py', '--config',
        'configs/endstation_ax7101_1x1_tdm8.yaml', '--csr-csv', str(boot / 'split-soc/mapped/soc/csr.csv')]


def case(name: str, *extra: str, cwd: Path = checkout) -> None:
    out = work / name
    done = subprocess.run([*base, '--output', str(out), *extra], cwd=cwd, capture_output=True, text=True, check=False)
    said = (done.stdout + done.stderr).strip().rsplit('\n', 1)[-1]
    print(f'{name}: rc {done.returncode}; ELF {"LEFT" if (out / "ctrl_app.elf").exists() else "none"}; {said[:170]}')


dangling = work / 'dangling.a'
dangling.unlink(missing_ok=True)
dangling.symlink_to(work / 'nothing.a')
(work / 'adir').mkdir(exist_ok=True)
(work / 'emptymap').mkdir(exist_ok=True)
case('no-map-real-archives', '--libc', str(libc), '--compiler-runtime', str(rt))
case('no-map-libc-only', '--libc', str(libc), '--compiler-runtime', str(work / 'absent.a'))
case('no-map-rt-only', '--libc', str(work / 'absent.a'), '--compiler-runtime', str(rt))
case('no-map-both-absent', '--libc', str(work / 'absent.a'), '--compiler-runtime', str(work / 'absent2.a'))
case('no-map-dangling-links', '--libc', str(dangling), '--compiler-runtime', str(dangling))
case('no-map-directory-archive', '--libc', str(work / 'adir'), '--compiler-runtime', str(work / 'absent.a'))
case('map-absent-dir', '--flash-map', str(work / 'nomap'), '--libc', str(libc), '--compiler-runtime', str(rt))
case('map-empty-dir', '--flash-map', str(work / 'emptymap'), '--libc', str(libc), '--compiler-runtime', str(rt))
case('map-true', '--flash-map', str(boot / 'split-soc/flash-map'), '--libc', str(libc), '--compiler-runtime', str(rt))
