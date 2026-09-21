"""Delete only configuration replay, then run the whole original 1x1 plan."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

SCRATCH = Path('/data/milan/reviews/r218-503-scratch')
PE = Path('/data/milan/reviews/r218-503-evidence/design-evidence/500-materialization/proposal-evidence')
os.environ['D3_OUT'] = str(SCRATCH / 'config-probe')
os.environ['OOC_OUT'] = str(SCRATCH / 'ooc')
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')
spec = importlib.util.spec_from_file_location('d3_config', PE / 'run.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
m.HERE = SCRATCH / 'report-config'
m.HERE.mkdir(exist_ok=True)
m.PROTO = SCRATCH / 'prototype-config'
shutil.copytree(PE / 'prototype', m.PROTO)
p = m.PROTO / 'KL_aecp_nvm_writer.proto.sv'
old = "          if (sub_r != 4'd15) begin"
new = "          if (cg_r == 4'(G_CFG)) st_r <= R_ADV;\n          else if (sub_r != 4'd15) begin"
t = p.read_text()
assert t.count(old) == 1
p.write_text(t.replace(old, new))
(m.HERE / 'injection.txt').write_text(old + '\nBECOMES\n' + new + '\n')
s = m.prep_shape('1x1')
b = m.do_build(m.Build('base-config-replay-deleted', '1x1'), s, 8)
res = m.execute(b, s)
m.report({b.name: res})
for r, g in res:
    if r.case == 'V1b_restore_everything' and not r.variant:
        print('CONFIG BEFORE', g.ans('pre.cfg.valid'))
        print('CONFIG AFTER', g.ans('post.cfg.valid'))
        print('CONFIG SLOT', g.slots(*r.slots_in).get(0))
