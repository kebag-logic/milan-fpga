#!/usr/bin/env python3
"""Run the output and map-read controls in four independent build directories."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
selected = 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly:Core.*Map*:Face.TheRunningCheckReadsOneWindowWordAStream'

def run(shape, interfaces):
    name = f'focused-{shape}-if{interfaces}'
    config = 'endstation_ax7101_1x1_tdm8.yaml' if shape == '1x1' else 'endstation_ax7101_8x8.yaml'
    cmd = [sys.executable, '-B', str(repo / 'sw/firmware/ctrl/test/aecp_arms.py'), '--app',
           '--config', str(repo / 'configs' / config), '--interfaces', str(interfaces),
           '--filter', selected, '--output', str(packet / 'scratch' / name)]
    with (packet / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + repr(cmd) + '\n'); log.flush()
        result = subprocess.run(cmd, cwd=repo, stdout=log, stderr=subprocess.STDOUT,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, result.returncode, flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(lambda args: run(*args), [(s, i) for s in ('1x1', '8x8') for i in (1, 2)]))
raise SystemExit(max(results))
