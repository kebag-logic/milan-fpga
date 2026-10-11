#!/usr/bin/env python3
"""Independently measure severity and placement on a one-guard module."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('packet', type=Path)
    p.add_argument('--verilator', default='verilator')
    args = p.parse_args()
    packet = args.packet.resolve()
    scratch = packet / 'scratch/forms'
    receipts = packet / 'receipts/forms'
    scratch.mkdir(exist_ok=True)
    receipts.mkdir(exist_ok=True)
    def one(task, placement, value):
        name = f'{task}-{placement}-{value}'
        work = scratch / name
        work.mkdir(exist_ok=True)
        call = '$fatal(1, "guard value %0d", P);' if task == 'fatal' else f'${task}("guard value %0d", P);'
        scope = 'initial ' if placement == 'initial' else ''
        src = ('module guard_probe #(parameter integer P=0)(output wire alive);\n'
               f'  {scope}if (P == 0) begin : parameter_guard\n    {call}\n  end\n'
               '  assign alive = 1\'b1;\nendmodule\n')
        (work / 'probe.sv').write_text(src)
        results = []
        commands = [('lint', [args.verilator, '--lint-only', '-Wall', '-Wno-DECLFILENAME',
                              '-Wno-UNUSEDSIGNAL', '-Wno-UNUSEDPARAM', '--top-module',
                              'guard_probe', f'-GP={value}', 'probe.sv'])]
        lowered = subprocess.run(['sv2v', 'probe.sv'], cwd=work, capture_output=True, text=True, check=True)
        (work / 'probe.v').write_text(lowered.stdout)
        commands.append(('synthesis', ['yosys', '-Q', '-q', '-p',
                         f'read_verilog -defer probe.v; chparam -set P {value} guard_probe; '
                         'hierarchy -check -top guard_probe; proc; opt_clean']))
        for frontend, cmd in commands:
            run = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
            log = run.stdout + run.stderr
            stem = receipts / f'{name}-{frontend}'
            stem.with_suffix('.log').write_text(log)
            stem.with_suffix('.rc').write_text(str(run.returncode) + '\n')
            if frontend == 'lint':
                refused = value == 0 and placement == 'module' and task != 'info'
            else:
                refused = value == 0 and task == 'fatal'
            documented = placement == 'module' or task == 'fatal'
            ok = (run.returncode != 0) == refused if documented else None
            results.append({'case': name, 'frontend': frontend, 'expected_refusal': refused,
                            'rc': run.returncode, 'documented_form': documented, 'pass': ok})
        return results
    with ThreadPoolExecutor(4) as pool:
        futures = [pool.submit(one, task, place, value)
                   for task in ('fatal', 'error', 'warning', 'info')
                   for place in ('module', 'initial') for value in (0, 1)]
        results = [row for f in futures for row in f.result()]
    (receipts / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')
    graded = [x for x in results if x['documented_form']]
    print(f'{sum(x["pass"] for x in graded)}/{len(graded)} documented outcomes agree with coding rule; '
          f'{len(results)-len(graded)} additional outcomes recorded without a documentation claim')
    return int(not all(x['pass'] for x in graded))


if __name__ == '__main__':
    raise SystemExit(main())
