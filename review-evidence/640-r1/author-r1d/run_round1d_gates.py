import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--jobs', type=int, default=8)
args = parser.parse_args()

root = Path('$LANES/640-mark2-plan')
out = Path('$VALIDATION_STORAGE/640-a540/round1d/gates-7387bb6f6')
out.mkdir(parents=True, exist_ok=True)
py = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3'
base = '5603c353137e90c1fa95429f6d00ef7a2298d9ee'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', VERILATOR='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
env['PATH'] = '$VALIDATION_TOOLS/pinned-verilator-5.050:' + str(Path(py).parent) + ':' + env['PATH']
env['TMPDIR'] = str(out / 'tmp')
Path(env['TMPDIR']).mkdir(exist_ok=True)
commands = [
('docs_check','scripts/docs_check.py'),
('docs_self','scripts/docs_check.py --selftest'),
('feature_status','scripts/check_feature_status.py'),
('feature_self','scripts/check_feature_status.py --self-test'),
('em_dash',f'scripts/check_em_dash.py --base {base}'),
('em_dash_self','scripts/check_em_dash.py --selftest'),
('doc_style','scripts/check_doc_style.py'),
('doc_style_self','scripts/check_doc_style.py --selftest'),
('gptp_docs','scripts/check_gptp_docs.py --with-submodule'),
('gptp_docs_self','scripts/check_gptp_docs.py --selftest'),
('doc_map','docs/DOC_MAP.gen.py --check'),
('doc_map_self','docs/DOC_MAP.gen.py --selftest'),
('timesync','docs/diagrams/timesync_chain.gen.py --check'),
('timesync_self','docs/diagrams/timesync_chain.gen.py --selftest'),
('solution','scripts/check_solution_docs.py'),
('solution_self','scripts/check_solution_docs.py --selftest'),
('submodule_diagram','docs/diagrams/submodule_boundaries.gen.py --check'),
('submodule_diagram_self','docs/diagrams/submodule_boundaries.gen.py --selftest'),
('submodule_docs','scripts/check_submodule_docs.py'),
('submodule_docs_self','scripts/check_submodule_docs.py --selftest'),
('diagram_pngs','scripts/check_diagram_pngs.py'),
('diagram_pngs_self','scripts/check_diagram_pngs.py --selftest'),
('module_matrix','docs/traceability/gen_module_matrix.py --check'),
('baremetal','scripts/check_baremetal_only.py --check'),
('baremetal_self','scripts/check_baremetal_only.py --selftest'),
('doc_paths','scripts/check_doc_paths.py'),
('archive','scripts/check_archive.py'),
('archive_self','scripts/check_archive.py --selftest'),
('toc_self','scripts/gen_toc.py --selftest'),
('toc_anchors','scripts/gen_toc.py --verify-anchors'),
('toc_check','scripts/gen_toc.py --check'),
('todo','scripts/check_todo_ownership.py'),
('hygiene','scripts/check_hygiene.py --check'),
('wire','scripts/check_wire_accountability.py --self-test'),
('resource_baseline','syn/ooc/pp_resource_gate.py check-baseline'),
('resource_self','syn/ooc/pp_resource_gate.py --selftest'),
('resource_mutants','syn/ooc/pp_resource_gate_mutants.py'),
('ci_scope','scripts/ci_scope.py --selftest'),
('ci_events','scripts/ci_events.py --check'),
('wavedrom_self','scripts/gen_wavedrom.py --selftest'),
('wavedrom_axis','scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check'),
('wavedrom_cdc','scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check'),
('wavedrom_gptp','scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check'),
('pp_sources','scripts/pp_srcs.py --check --selftest'),
]
jobs = [(name,[py,*shlex.split(cmd)],env) for name,cmd in commands]
jobs += [('docs_nogit',[py,'scripts/docs_check.py'],dict(env,GIT_DIR='/dev/null')),
         ('gptp_make',['make','-j16','-C','gptp-processor','docs'],env),
         ('diff_base',['git','diff','--check',base,'HEAD'],env),
         ('diff_tree',['git','diff','--check'],env)]
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
 subroot = root / sub
 actual = subprocess.check_output(['rtk','proxy','git','-C',str(subroot),'rev-parse','--show-toplevel'], text=True).strip()
 if Path(actual).resolve() != subroot.resolve():
  raise SystemExit('Submodule root mismatch: ' + sub)
for name in ('recompute_ledger','verify_round1c','verify_round1d'):
 jobs.append((name,[py,'$MANAGEMENT/2026-09-23/640-a540/'+name+'.py',str(root)],env))
(out / 'head.txt').write_text(subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],cwd=root,text=True))
def run(job):
 name,cmd,jobenv=job
 start=time.monotonic()
 with (out / (name+'.log')).open('w') as log:
  result=subprocess.run(['rtk','proxy',*cmd],cwd=root,env=jobenv,stdout=log,stderr=subprocess.STDOUT,timeout=550)
 row={'gate':name,'command':shlex.join(cmd),'rc':result.returncode,'seconds':round(time.monotonic()-start,2)}
 (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
 print(name,result.returncode,flush=True)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
 rows=list(pool.map(run,jobs))
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
failed=[r for r in rows if r['rc']]
print('RESULT',len(rows),'gates;',len(failed),'nonzero',flush=True)
sys.exit(bool(failed))
