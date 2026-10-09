#!/usr/bin/env python3
"""Replay the three assigned downstream guard controls from the repository root."""
from pathlib import Path
import json
import os
import re
import shlex
import subprocess
import sys
from unittest.mock import patch
ROOT = Path.cwd()
WORK = Path(os.environ['WORK']) / 'sweep-replay'
WORK.mkdir(exist_ok=True)
sys.path[:0] = [str(ROOT/'sw/builder'), str(ROOT/'syn/resmap')]
import endstation_builder as eb
import yosys_sweep as sweep
plan = sweep.load_plan(ROOT/'syn/resmap/sweep_plan.json')
base = (ROOT/'configs/endstation_ax7101_1x1_tdm8.yaml').read_text()
rows = []
for label in ('streams-8', 'streams-8-chans-2', 'pp-names-235'):
    point = next(p for p in plan['points'] if p['name'] == label)
    directory = WORK/label
    directory.mkdir(exist_ok=True)
    if 'shape' in point:
        cfg = WORK/'tree/configs'/('endstation_'+point['shape']+'.yaml')
        cfg.parent.mkdir(parents=True,exist_ok=True)
        cfg.write_text(sweep.variant_text(base,plan['variants'][point['shape']]))
        try:
            eb._derive_artifacts(str(cfg))
        except eb.ConfigError as error:
            assert '235 writable names' in str(error), str(error)
            (directory/'builder-refusal.log').write_text(str(error)+'\n')
        else:
            raise RuntimeError('expected builder refusal escaped')
        # Negative control only: use the generator, bypassing its earlier
        # capacity refusal in memory so the downstream guard is exercised.
        with patch.object(eb,'nvm_name_capacity',return_value=(1024,'planted capacity for downstream control')):
            art=eb._derive_artifacts(str(cfg))
            generated,_=eb._write_artifact_dir(art,str(WORK/'tree/configs/generated'))
            generated=Path(generated)
            (generated/'gen').mkdir(exist_ok=True)
            (generated/'gen/adp_shape_defaults.svh').write_text(art.adp_svh)
    record = sweep.prepare_sources(WORK,plan,point,directory)
    if point['top'] == 'KL_pp_shadow':
        source=sweep.find_declaring(record['src'],'module KL_pp_shadow')
        dst=directory/'shadow.sv'
        text = Path(source).read_text()
        for key,value in sweep.point_params(plan,point).items():
            pattern = r'(^\s*parameter\b[^=\n]*?\b'+key+r'\s*=\s*)([^,\n]+)'
            text,hits=re.subn(pattern,lambda m: m[1]+str(value),text,flags=re.M)
            assert hits==1,(key,hits)
        dst.write_text(text)
        record['src'][record['src'].index(source)]=str(dst)
    args=['sv2v','--top='+point['top'], *['-D'+v for v in record['define']],
          *['-I'+v for v in record['incdir']],*record['src']]
    for flow in ('run.sh','ooc.sh'):
        text=(ROOT/'syn/yosys'/flow).read_text()
        text=text.replace('R="$(cd "$(dirname "$0")/../.." && pwd)"','R='+shlex.quote(str(ROOT)))
        text=text.replace('. "$(dirname "$0")/malloc.sh"','. '+shlex.quote(str(ROOT/'syn/yosys/malloc.sh')))
        for call in ('sv2v --top="$top" $inc $srcs','sv2v --top="$top" $INC $srcs'):
            text=text.replace(call,shlex.join(args))
        script=directory/flow
        script.write_text(text)
        cli=['--top',point['top'],'--no-structural'] if flow=='run.sh' else [point['top']]
        env=dict(os.environ,TMPDIR=str(WORK),OOC_TMP=str(directory/'ooc'))
        run=subprocess.run(['bash',str(script),*cli],cwd=ROOT,env=env,capture_output=True,text=True)
        log=directory/(flow+'.log'); log.write_text(run.stdout+run.stderr)
        assert run.returncode!=0 and '$error' in run.stdout, (label,flow,run.returncode,run.stdout)
        rows.append(dict(point=label,flow=flow,rc=run.returncode,guard='active $error',log=str(log.relative_to(WORK))))
        print(rows[-1],flush=True)
(WORK/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
