#!/usr/bin/env python3
"""Issue #113: prove retained stop, generator-signal and print-failure checks."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('packet', type=Path)
    args = ap.parse_args()
    packet = args.packet.resolve()
    os.environ.update(MAKEFLAGS='', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch/tmp'))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    source = packet / 'scratch/head'
    edits = [
        ('stop', '    (STATE / f"{n}.stop").touch()\n    for later', '    return\n    for later'),
        ('generator', '        reraise(record["gen_signal"], record.get("gen_core", False))', '        return 0'),
        ('print', '        print(f"engine pass {n}: its transcript could not be printed ({exc})", file=sys.stderr)\n        (STATE / f"{n}.stop").touch()\n        return 1', '        return 0'),
    ]
    for name, old, new in edits:
        for mutated in (False, True):
            work = packet / 'scratch' / ('fault-' + name + '-' + str(mutated))
            if work.exists():
                shutil.rmtree(work)
            engine = work / 'tb/verilator/engine'
            engine.mkdir(parents=True, exist_ok=True)
            for rel in ('tb/verilator/engine/Makefile', 'tb/verilator/engine/pass_run.py', 'tb/engine_passes_test.py'):
                shutil.copy(source / rel, work / rel)
            runner = engine / 'pass_run.py'
            text = runner.read_text()
            assert text.count(old) == 1
            if mutated:
                runner.write_text(text.replace(old, new))
            spec = importlib.util.spec_from_file_location('scheduling_test', work / 'tb/engine_passes_test.py')
            test = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test)
            trial = work / 'trial'
            trial.mkdir()
            trees = test.tree(trial)
            if name == 'stop':
                plan = {'0': {'sleep': 0.2}, '1': {'sleep': 0.1, 'exit': 7},
                        '2': {'sleep': 2}, '3': {'sleep': 2}}
                done = test.make(trees['parallel'], ['-j16'], plan, trial / 'events.jsonl')
                state = trees['parallel'] / 'obj_dir/engine-passes'
                records = [json.loads((state / (str(i) + '.json')).read_text()) for i in range(4)]
                caught = not (done.returncode == 2 and all(records[i].get('stopped') for i in (2, 3)))
                print('stop records:', json.dumps(records, sort_keys=True), 'make status:', done.returncode)
            elif name == 'generator':
                caught = bool(test.gen_signal(trees, trial))
            else:
                caught = bool(test.unprintable(trees, trial))
            assert caught == mutated, (name, mutated, caught)
            print('PASS', name, 'mutation rejected' if mutated else 'control accepted', flush=True)
    print('PASS 3 controls and 3 targeted mutations')


if __name__ == '__main__':
    main()
