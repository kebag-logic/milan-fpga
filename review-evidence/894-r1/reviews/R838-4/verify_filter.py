#!/usr/bin/env python3
"""Run the thirteen-test selection on the binary produced by run_focused.py."""
from pathlib import Path
import subprocess

packet=Path(__file__).resolve().parent
binary=next((packet/'scratch/map-core').glob('*/suite'))
with (packet/'map-core-wide.log').open('w') as log:
    result=subprocess.run([str(binary),'--gtest_filter=Core.*Map*:Core.Every*'],stdout=log,stderr=subprocess.STDOUT)
(packet/'map-core-wide.rc').write_text(str(result.returncode)+'\n')
raise SystemExit(result.returncode)
