#!/usr/bin/env python3
"""Reviewer replay of the #649 refused sweep points through syn/yosys/run.sh and ooc.sh.

Runs each point through the flow as committed at --flow-rev (the PR head or its
base) with an explicit sv2v binary, so the converted (sv2v 0.0.13) and native
(sv2v 0.0.12, the CI pin) lowerings are both exercised, before and after the
change. Also replays the rx_mac_filter override named in
docs/development/CODE_QUALITY.md. Writes one JSON row per run.

usage: sweep_replay.py --repo TREE --work DIR --sv2v BIN --flow-rev REV --label L
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--sv2v', required=True)
    ap.add_argument('--flow-rev', required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--run-mode', default='full', help='run.sh --mode; elaborate skips mapping')
    ap.add_argument('--flows', default='run.sh,ooc.sh', help='flows for the sweep points')
    ap.add_argument('--points', default='streams-8,streams-8-chans-2,pp-names-235,rx-tdata-52')
    args = ap.parse_args()
    root = args.repo.resolve()
    work = (args.work / args.label).resolve()
    work.mkdir(parents=True, exist_ok=True)
    sys.path[:0] = [str(root / 'sw/builder'), str(root / 'syn/resmap')]
    import endstation_builder as eb
    import yosys_sweep as sweep

    plan = sweep.load_plan(root / 'syn/resmap/sweep_plan.json')
    base = (root / 'configs/endstation_ax7101_1x1_tdm8.yaml').read_text()
    flows = {f: subprocess.run(['git', '-C', str(root), 'show', f'{args.flow_rev}:syn/yosys/{f}'],
                               check=True, capture_output=True, text=True).stdout
             for f in ('run.sh', 'ooc.sh')}
    jobs = []
    for label in args.points.split(','):
        directory = work / label
        directory.mkdir(exist_ok=True)
        if label == 'rx-tdata-52':
            # docs/development/CODE_QUALITY.md: OOC_CHPARAM="TDATA_WIDTH=52" ooc.sh rx_mac_filter
            jobs.append((label, 'ooc.sh', None, ['rx_mac_filter'], {'OOC_CHPARAM': 'TDATA_WIDTH=52'}, directory))
            jobs.append((label + '-legal64', 'ooc.sh', None, ['rx_mac_filter'], {'OOC_CHPARAM': 'TDATA_WIDTH=64'}, directory))
            continue
        point = next(p for p in plan['points'] if p['name'] == label)
        if 'shape' in point:
            cfg = work / 'tree/configs' / ('endstation_' + point['shape'] + '.yaml')
            cfg.parent.mkdir(parents=True, exist_ok=True)
            cfg.write_text(sweep.variant_text(base, plan['variants'][point['shape']]))
            refused = ''
            try:
                eb._derive_artifacts(str(cfg))
            except eb.ConfigError as error:
                refused = str(error)
            (directory / 'builder-refusal.log').write_text(refused + '\n')
            # Negative control only: the builder refuses first; bypass in memory to reach the RTL guard.
            with patch.object(eb, 'nvm_name_capacity', return_value=(1024, 'reviewer planted capacity')):
                art = eb._derive_artifacts(str(cfg))
                generated, _ = eb._write_artifact_dir(art, str(work / 'tree/configs/generated'))
                (Path(generated) / 'gen').mkdir(exist_ok=True)
                (Path(generated) / 'gen/adp_shape_defaults.svh').write_text(art.adp_svh)
        record = sweep.prepare_sources(work, plan, point, directory)
        if point['top'] == 'KL_pp_shadow':
            source = sweep.find_declaring(record['src'], 'module KL_pp_shadow')
            dst = directory / 'shadow.sv'
            text = Path(source).read_text()
            for key, value in sweep.point_params(plan, point).items():
                pattern = r'(^\s*parameter\b[^=\n]*?\b' + key + r'\s*=\s*)([^,\n]+)'
                text, hits = re.subn(pattern, lambda m, v=value: m[1] + str(v), text, flags=re.M)
                if hits != 1:
                    raise SystemExit(f'{key}: {hits} parameter defaults rewritten, expected 1')
            dst.write_text(text)
            record['src'][record['src'].index(source)] = str(dst)
        conv = [args.sv2v, '--top=' + point['top'], *['-D' + v for v in record['define']],
                *['-I' + v for v in record['incdir']], *record['src']]
        for flow in args.flows.split(','):
            cli = (['--top', point['top'], '--no-structural', '--mode', args.run_mode]
                   if flow == 'run.sh' else [point['top']])
            jobs.append((label, flow, conv, cli, {}, directory))

    def one(job):
        label, flow, conv, cli, extra, directory = job
        text = flows[flow]
        text = text.replace('R="$(cd "$(dirname "$0")/../.." && pwd)"', 'R=' + shlex.quote(str(root)))
        text = text.replace('. "$(dirname "$0")/malloc.sh"', '. ' + shlex.quote(str(root / 'syn/yosys/malloc.sh')))
        for call in ('sv2v --top="$top" $inc $srcs', 'sv2v --top="$top" $INC $srcs'):
            if conv is not None:
                text = text.replace(call, shlex.join(conv))
            else:
                text = text.replace(call, shlex.quote(args.sv2v) + call[len('sv2v'):])
        script = directory / f'{label}.{flow}'
        script.write_text(text)
        env = dict(os.environ, TMPDIR=str(work), OOC_TMP=str(directory / f'ooc-{label}'), **extra)
        run = subprocess.run(['bash', str(script), *cli], cwd=root, env=env, capture_output=True, text=True)
        log = directory / f'{label}.{flow}.log'
        log.write_text(run.stdout + run.stderr)
        err = re.findall(r'ERROR:[^\n]*', run.stdout + run.stderr)
        return dict(label=args.label, point=label, flow=flow, rc=run.returncode,
                    first_error=err[0][:200] if err else '', log=str(log.relative_to(work.parent)))

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(one, jobs))
    for row in rows:
        print(json.dumps(row), flush=True)
    (work / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
