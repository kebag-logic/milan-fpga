#!/usr/bin/env python3
"""Run the sweep self-test on in-memory mutations; no checkout writes.
Usage: wiring_probes.py REPO
"""
import contextlib
import io
import os
from pathlib import Path
import sys
import types

repo=Path(sys.argv[1]).resolve()
path=repo/'syn/resmap/soc_sweep.py'
source=path.read_text()
sys.path.insert(0,str(path.parent))
changes=[
 ('control','','','soc_sweep self-test: PASS'),
 ('builder placement omitted','"-o", str(out), str(config),\n                    "--placement", placement], cwd=tree','"-o", str(out), str(config)], cwd=tree','prepare(all-fabric) did not ask the builder'),
 ('missing image refusal bypassed','    if missing:\n','    if False:\n','prepare(split) returned an argument list naming an absent platform image'),
 ('export placement forced','base = prepare(work, plan_placement(plan))','base = prepare(work, "split")','command_export asked prepare() for split'),
 ('wrong image root','if not (tree / path).is_file()]','if not (Path("/nonexistent") / path).is_file()]','a platform image present in the tree was reported missing'),
 ('include flag omitted','return [*params["argv"], "--entity-gen-dir", str(tree / "configs/generated" / yosys_sweep.BASE_CONFIG)]','return params["argv"]','prepare(all-fabric) returned'),
]
for label,old,new,marker in changes:
    assert not old or source.count(old)==1
    module=types.ModuleType('review_sweep')
    module.__file__=str(path)
    sys.modules[module.__name__]=module
    exec(compile(source.replace(old,new) if old else source,str(path),'exec'),module.__dict__)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): rc=module.selftest()
    output=buf.getvalue()
    assert rc==(0 if not old else 1) and marker in output,(label,rc,output)
    print('PASS',label,'rc',rc)
    print(output,end='')
print('PASS 1 unplanted control and 5 named wiring probes')
