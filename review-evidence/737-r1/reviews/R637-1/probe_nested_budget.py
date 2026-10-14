#!/usr/bin/env python3
"""Inspect real child Makefile commands reached by the capture campaign."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
spec = importlib.util.spec_from_file_location('capture_budget_probe', root / 'tb/verilator/capture_coherence/mutants.py')
driver = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = driver
spec.loader.exec_module(driver)
packet = Path(__file__).resolve().parent
work = packet / 'scratch' / 'budget-probe'
work.mkdir(parents=True, exist_ok=True)
units = driver.arm_units(work, True)
for cpus in (4, 12, 16):
    budget = cpus // min(4, cpus)
    for leg in ('junction', 'chmap', 'nco'):
        suite, target, source_var, directory_var, rtl, _, _ = driver.LEGS[leg]
        command = ['make', '-n', '-s', '--no-print-directory', '-C', str(suite), target,
                   source_var + '=' + str(rtl.resolve()), directory_var + '=' + str(work / ('obj_' + leg))]
        result = subprocess.run(command, cwd=root, text=True, capture_output=True,
                                env=dict(os.environ, MAKEFLAGS=driver.BUILD_MAKEFLAGS,
                                         VERILATOR_JOBS=str(budget)))
        assert result.returncode == 0, result.stderr
        lines = [line for line in result.stdout.splitlines() if '--cc --exe --build' in line]
        assert len(lines) == 1, lines
        selected = int(re.search(r'(?:^|\s)-j\s+(\d+)', lines[0])[1])
        if leg == 'nco':
            assert selected == 0
        else:
            assert selected == budget
        print(json.dumps({'job_cpus': cpus, 'campaign_workers': min(4, cpus),
                          'exported_compiler_budget': budget, 'child_leg': leg,
                          'actual_make_recipe_j': selected,
                          'zero_selects_full_process_affinity': selected == 0}, sort_keys=True))
for index, unit in enumerate(units):
    if 'nco' in unit.name:
        print(json.dumps({'case': unit.name, 'owning_leg': str(index % 4) + '/4',
                          'scheduled_in_four_worker_pool': True}, sort_keys=True))
