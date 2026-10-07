#!/usr/bin/env python3
"""Reproduce sixteen source-base exports, then the candidate option bank."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = 'e21c1ca024d37ea188ad15b5c8f9c2dae18628df'
def one(args):
    from unittest.mock import patch
    root = Path(args.root)
    cpu_data = Path(args.data)
    import pythondata_cpu_naxriscv as nax
    import pythondata_cpu_vexiiriscv as vex
    nax.data_location = str(cpu_data / 'naxriscv')
    vex.data_location = str(cpu_data / 'vexiiriscv')
    sys.path.insert(0, str(root / 'sw/litex'))
    source = subprocess.check_output(['git', '-C', str(root), 'show', BASE + ':sw/litex/milan_soc.py'])
    scope = {'__name__': 'baseline_soc', '__file__': str(root / 'sw/litex/milan_soc.py')}
    exec(compile(source, scope['__file__'], 'exec'), scope)
    from litex.soc.cores.cpu.naxriscv import NaxRiscv
    from litex.soc.integration.builder import Builder
    read_args = NaxRiscv.args_read
    def frozen(args):
        read_args(args)
        NaxRiscv.update_repo = 'no'
    options = {'none': {}, 'zero': {'l2_bytes': 0}, 'l2': {'l2_bytes': 8192}, 'fpu': {'with_fpu': True}}[args.option]
    with patch.object(NaxRiscv, 'args_read', side_effect=frozen):
        soc = scope['MilanSoC'](scope['alinx_ax7101'].Platform(), 50000000,
                               cpu=args.cpu, xlen=args.xlen, with_milan=False, **options)
        Builder(soc, output_dir=args.out, compile_software=False).build(run=False)
    name = soc.cpu.netlist_name
    raw = (cpu_data / args.cpu / (name + '.v')).read_bytes()
    rtl = re.sub(rb'//[^\n]*', b'', raw).replace(name.encode(), b'CPU')
    row = {'label': f'{args.cpu}-{args.xlen}-{args.option}', 'cpu': args.cpu,
           'xlen': args.xlen, 'option': args.option, 'netlist': name + '.v',
           'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
           'rtl_sha256': hashlib.sha256(rtl).hexdigest(), 'rc': 0}
    Path(args.result).write_text(json.dumps(row, indent=2) + '\n')

def main(args):
    scratch = Path(args.out)
    scratch.mkdir(parents=True, exist_ok=True)
    expected = json.loads(Path(args.expected).read_text())
    # Remove only the ten measured cached variants in the disposable copies.
    # Their first use must regenerate; repeated zero/FPU-no-effect cases reuse them.
    for row in expected:
        (Path(args.data) / row['cpu'] / row['netlist']).unlink(missing_ok=True)
    rows = []
    for cpu in ('vexiiriscv', 'naxriscv'):
        for xlen in (32, 64):
            for option in ('none', 'fpu', 'l2', 'zero'):
                label = f'{cpu}-{xlen}-{option}'
                result = scratch / (label + '.json')
                command = [sys.executable, __file__, '--one', '--root', args.root,
                           '--data', args.data, '--cpu', cpu, '--xlen', str(xlen),
                           '--option', option, '--out', str(scratch / label),
                           '--result', str(result), '--jobs', str(args.jobs)]
                with (scratch / (label + '.log')).open('w') as log:
                    completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
                (scratch / (label + '.rc')).write_text(str(completed.returncode) + '\n')
                assert completed.returncode == 0, label
                rows.append(json.loads(result.read_text()))
                print(json.dumps(rows[-1]), flush=True)
    by_label = {row['label']: row for row in expected}
    for row in rows:
        assert row['sha256'] == by_label[row['label']]['sha256'], row['label']
        assert row['rtl_sha256'] == by_label[row['label']]['rtl_sha256'], row['label']
        assert row['size'] == by_label[row['label']]['size'], row['label']
    Path(args.result).write_text(json.dumps(rows, indent=2) + '\n')
    print('PASS: 16 exports; all raw and normalized digests and byte counts reproduce public measurements', flush=True)
    command = [sys.executable, str(Path(args.root) / 'sw/builder/test_soc_options.py'),
               '--netlists', '--nax-data-dir', str(Path(args.data) / 'naxriscv')]
    subprocess.run(command, check=True)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', required=True)
parser.add_argument('--data', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--result', required=True)
parser.add_argument('--jobs', type=int, default=4)
parser.add_argument('--expected')
parser.add_argument('--one', action='store_true')
parser.add_argument('--cpu')
parser.add_argument('--xlen', type=int)
parser.add_argument('--option')
args = parser.parse_args()
os.environ['JAVA_TOOL_OPTIONS'] = f'-XX:ActiveProcessorCount={args.jobs} -Xmx2g'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
if args.one:
    one(args)
else:
    main(args)
