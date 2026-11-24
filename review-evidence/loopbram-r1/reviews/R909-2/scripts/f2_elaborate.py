#!/usr/bin/env python3
"""Elaborate each exported disabled release top (synth_design -rtl, write_verilog)
and hash its canonical text, sequentially (one Vivado at a time).

Canonicalization is the author's: drop (* attributes *), // and /* */ comments,
strip whitespace per line, drop empty lines. Identifiers, widths, cells,
parameters, connections and module order remain.

usage: f2_elaborate.py <vivado> <work-root> <out-json> side=<tree>:<export-dir> ...
"""
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

SHAPES = ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')


def canonical(raw: str) -> str:
    text = re.sub(r'\(\*.*?\*\)', '', raw, flags=re.S)
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return '\n'.join(line.strip() for line in text.splitlines() if line.strip()) + '\n'


def main() -> int:
    vivado, work, out_json = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    sides = dict(a.split('=', 1) for a in sys.argv[4:])
    results = []
    for name in SHAPES:
        for side, spec in sides.items():
            export = Path(spec) / name / 'gateware'
            run = work / side / name
            run.mkdir(parents=True, exist_ok=True)
            text = (export / 'alinx_ax7101.tcl').read_text()
            text = text[:text.index('# Synthesis report')]
            assert text.count('synth_design -directive AreaOptimized_high') == 1
            text = text.replace('synth_design -directive AreaOptimized_high', 'synth_design -rtl')
            text = text.replace('read_xdc alinx_ax7101.xdc', f'read_xdc {{{export}/alinx_ax7101.xdc}}')
            text = text.replace('[get_files alinx_ax7101.xdc]', f'[get_files {{{export}/alinx_ax7101.xdc}}]')
            text += '\nwrite_verilog -force rtl.v\nquit\n'
            (run / 'elaborate.tcl').write_text(text)
            t = time.time()
            with (run / 'run.log').open('w') as log:
                rc = subprocess.run([vivado, '-mode', 'batch', '-nojournal', '-nolog', '-source',
                                     str(run / 'elaborate.tcl')], cwd=export, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=5400).returncode
            entry = dict(shape=name, side=side, exit=rc, seconds=round(time.time() - t, 1))
            rtl = export / 'rtl.v'
            if rc == 0 and rtl.is_file():
                raw = rtl.read_text()
                canon = canonical(raw)
                (run / 'canonical.v').write_text(canon)
                entry.update(raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                             canonical_sha256=hashlib.sha256(canon.encode()).hexdigest(),
                             canonical_bytes=len(canon))
                rtl.rename(run / 'rtl.v')
            results.append(entry)
            print(json.dumps(entry), flush=True)
            out_json.write_text(json.dumps(results, indent=2) + '\n')
            if rc:
                return rc
    for name in SHAPES:
        hashes = {r['side']: r.get('canonical_sha256') for r in results if r['shape'] == name}
        print(name, 'IDENTICAL' if len(set(hashes.values())) == 1 else 'DIFFERENT', hashes, flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
