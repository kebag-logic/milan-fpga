#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run ctrl_image_runtime.py unchanged, with -fno-stack-protector on its compiles (#723).

The pinned RV32 SDK enables the stack protector by default and the runtime
recipe does not turn it off, so its archives reference __stack_chk_guard
and the image does not link. #723 owns the fix; until then this adds the
one flag to each compiler call of the recipe and changes nothing else.
"""
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECIPE = ROOT / 'sw/firmware/ctrl/test/ctrl_image_runtime.py'
ORIGINAL = subprocess.run


def run(argv: object, *args: object, **kwargs: object) -> subprocess.CompletedProcess:
    """Insert the flag into compiles only; archive and other calls pass unchanged."""
    if isinstance(argv, list) and str(argv[0]).endswith('gcc') and '-c' in argv:
        argv = [argv[0], '-fno-stack-protector', *argv[1:]]
    return ORIGINAL(argv, *args, **kwargs)


if __name__ == '__main__':
    sys.path[:0] = [str(RECIPE.parent), str(ROOT / 'sw/firmware/gtest')]
    subprocess.run = run
    sys.argv = [str(RECIPE), *sys.argv[1:]]
    runpy.run_path(str(RECIPE), run_name='__main__')
