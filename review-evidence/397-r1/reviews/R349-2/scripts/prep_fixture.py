#!/usr/bin/env python3
"""Write the populated KLJ2 fixture with the head harness's own fixture code.

Usage: prep_fixture.py <repo> <build-dir> <shape>
Writes <build>/slots.bin and <build>/commands.txt (plan 'all'), and the media
record to <build>/media_all.json. No simulation is run.
"""
import json, sys
from pathlib import Path
repo, build, shape = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(repo / 'tb/verilator/fw_service_budget'))
import run
media = run.fixtures(build, shape, True, 'all')
(build / 'media_all.json').write_text(json.dumps(media, indent=2) + '\n')
print(json.dumps(media))
