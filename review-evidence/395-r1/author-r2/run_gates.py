"""Run assigned gates serially in the foreground and retain exact exit codes."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import time

root = Path('$LANES/395-timing-grade')
work = Path('$VALIDATION_STORAGE/395-a390-work')
out = Path('$MANAGEMENT/2026-09-23/395-a390')
head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=root, text=True).strip()
base = '8bc97021f28fb7f729418d3a00851c84ea0b50fd'
md = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python'
checkpoint = '$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp'
reports = work / ('final-' + head[:9])
reports.mkdir(exist_ok=True)
logs = work / ('gates-' + head[:9])
logs.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONUNBUFFERED='1', PYTHONDONTWRITEBYTECODE='1',
           PYTHONHASHSEED='0', TMPDIR=str(work/'tmp'), MAKEFLAGS='-j16',
           JAVA_TOOL_OPTIONS='-XX:ActiveProcessorCount=16')
gates = [
 ('timing-script',300,['python3','-B','sw/litex/report_timing_grade.py',checkpoint,str(reports)],root),
 ('timing',1800,['$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado','-mode','batch','-nojournal','-notrace',
                 '-log',str(reports/'vivado.log'),'-source',str(reports/'report.tcl')],reports),
 ('crossings',1800,['$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado','-mode','batch','-nojournal','-notrace','-log',str(reports/'crossings.log'),'-source',str(work/'crossings.tcl'),'-tclargs',checkpoint,str(reports)],reports),
 ('mutations',1800,['python3','-B',str(work/'run_mutations.py')],root),
 ('builder-present',14400,['python3','-B','sw/builder/test_builder.py','--require-rv32','--require-elaboration'],root),
 ('builder-absent',14400,['python3','-B',str(work/'run_builder_absent.py')],root),
 ('ci-scope-selftest',300,['python3','-B','scripts/ci_scope.py','--selftest'],root),
 ('docs',300,['python3','-B','scripts/docs_check.py'],root),
 ('doc-paths',300,['python3','-B','scripts/check_doc_paths.py'],root),
 ('toc',300,[md,'-B','scripts/gen_toc.py','--check'],root),
 ('em-dash',300,[md,'-B','scripts/check_em_dash.py','--base',base],root),
 ('feature-status',300,['python3','-B','scripts/check_feature_status.py','--self-test'],root),
 ('doc-style',300,['python3','-B','scripts/check_doc_style.py'],root),
 ('doc-style-selftest',300,['python3','-B','scripts/check_doc_style.py','--selftest'],root),
 ('solution-docs',300,['python3','-B','scripts/check_solution_docs.py'],root),
 ('python-idiom',300,['python3','-B','scripts/check_py_idiom.py'],root),
 ('python-idiom-selftest',300,['python3','-B','scripts/check_py_idiom.py','--selftest'],root),
 ('diff-committed',300,['git','diff','--check',base,'HEAD'],root),
 ('diff-worktree',300,['git','diff','--check'],root),
]
results=[]
for name, seconds, argv, cwd in gates:
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip() != head:
        raise RuntimeError('HEAD moved during gates')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f'START {name} {started}',flush=True)
    log=logs/(name+'.log')
    command=['timeout','--foreground',str(seconds),*argv]
    now=time.monotonic()
    with log.open('w') as stream:
        result=subprocess.run(command,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,check=False)
    with log.open('rb') as stream:
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    row=dict(gate=name,head=head,command=command,cwd=str(cwd),started=started,
             seconds=round(time.monotonic()-now,2),returncode=result.returncode,
             log=str(log),bytes=log.stat().st_size,sha256=digest)
    results.append(row)
    (out/'gate-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(f'END {name} rc={result.returncode} seconds={row["seconds"]} log={log}',flush=True)
    if result.returncode:
        print(log.read_text(errors='replace')[-6000:],flush=True)
        raise SystemExit(result.returncode)
print(f'ALL {len(results)} GATES RC 0 at {head}',flush=True)
