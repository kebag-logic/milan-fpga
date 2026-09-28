"""Foreground gate receipts at one committed head; build artifacts stay under data."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path('$LANES/607-xdc-clock-names')
out = Path(__file__).resolve().parent
work = Path('$VALIDATION_STORAGE/607-a408-work')
logs = work / 'gates'
logs.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(work), PYTHONPATH=str(work / 'docdeps'),
           MILAN_LITEX_PYTHON='$WORKSPACE_HOME/litex-milan/venv/bin/python', PYTHONHASHSEED='0',
           GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.commitGraph', GIT_CONFIG_VALUE_0='false')
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
base = '54ce877371ee6e8878cf67294e86c2a8481b62f6'
commands = []
if sys.argv[1] == 'builder':
    commands = [
        ('builder-present', ['python3','-B','sw/builder/test_builder.py','--require-rv32','--require-elaboration']),
        ('builder-absent', ['python3','-B',str(out / 'run_builder_absent.py')]),
    ]
else:
    rows = [
        ('scripts/ci_scope.py', '--selftest'),
        ('scripts/gen_hdl_reference.py', '--selftest'),
        ('scripts/gen_hdl_reference.py', '--output $VALIDATION_STORAGE/607-a408-work/hdl-reference-' + head[:9]),
        ('scripts/gen_wavedrom.py', '--selftest'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_axis_backpressure.json --background=white --check'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_cdc_handshake.json --background=white --check'),
        ('scripts/gen_wavedrom.py', 'docs/diagrams/wd_gptp_pdelay.json --background=white --check'),
        ('scripts/measure_control_flow.py', '--selftest'),
        ('scripts/measure_cohesion.py', '--selftest'),
        ('sw/builder/test_firmware_compiler.py', '--selftest'),
        ('sw/builder/test_firmware_compiler.py', '--absent --audit $VALIDATION_STORAGE/607-a408-work/firmware-absent.jsonl'),
        ('scripts/check_nvm_record_space.py', ''),
        ('scripts/check_nvm_record_space.py', '--self-test'),
        ('scripts/check_nvm_capture.py', ''),
        ('scripts/check_soc_sources.py', ''),
        ('scripts/check_soc_sources.py', '--selftest'),
        ('sw/litex/iob_pack_selftest.py', ''),
        ('scripts/check_rtl_source_lists.py', ''),
        ('scripts/check_rtl_source_lists.py', '--selftest'),
        ('scripts/measure_naming.py', '--check'),
        ('scripts/measure_naming.py', '--selftest'),
        ('scripts/check_port_contracts.py', ''),
        ('scripts/check_port_contracts.py', '--selftest'),
        ('scripts/measure_fail_fast.py', '--check'),
        ('scripts/measure_fail_fast.py', '--selftest'),
        ('scripts/check_todo_ownership.py', ''),
        ('scripts/check_todo_ownership.py', '--selftest'),
        ('scripts/measure_test_evidence.py', '--check'),
        ('scripts/measure_test_evidence.py', '--selftest'),
        ('scripts/check_hygiene.py', '--check'),
        ('scripts/check_hygiene.py', '--selftest'),
        ('scripts/check_sv_idiom.py', ''),
        ('scripts/check_sv_idiom.py', '--selftest'),
        ('scripts/check_cpp_idiom.py', ''),
        ('scripts/check_cpp_idiom.py', '--selftest'),
        ('scripts/check_sh_idiom.py', ''),
        ('scripts/check_sh_idiom.py', '--selftest'),
        ('scripts/ci_events.py', '--check'),
        ('scripts/ci_events.py', '--selftest'),
        ('avdecc/gen_aem_store.py', '--self-test'),
        ('scripts/check_entity_shape.py', '--self-test'),
        ('scripts/check_wire_accountability.py', '--self-test'),
        ('scripts/docs_check.py', ''),
        ('scripts/check_doc_paths.py', ''),
        ('scripts/gen_toc.py', '--check'),
        ('scripts/gen_toc.py', '--selftest'),
        ('scripts/gen_toc.py', '--verify-anchors'),
        ('scripts/check_em_dash.py', '--base ' + base),
        ('scripts/check_em_dash.py', '--selftest'),
        ('scripts/check_feature_status.py', '--self-test'),
        ('scripts/check_doc_style.py', ''),
        ('scripts/check_doc_style.py', '--selftest'),
        ('scripts/check_solution_docs.py', ''),
        ('scripts/check_solution_docs.py', '--selftest'),
        ('scripts/check_baremetal_only.py', '--check'),
        ('scripts/check_baremetal_only.py', '--selftest'),
        ('scripts/check_py_idiom.py', ''),
        ('scripts/check_py_idiom.py', '--selftest'),
        ('scripts/check_gptp_docs.py', '--with-submodule'),
        ('scripts/check_gptp_docs.py', '--selftest'),
        ('scripts/check_submodule_docs.py', ''),
        ('scripts/check_submodule_docs.py', '--selftest'),
        ('scripts/check_archive.py', ''),
        ('scripts/check_archive.py', '--selftest'),
        ('docs/traceability/gen_module_matrix.py', '--check'),
        ('docs/DOC_MAP.gen.py', '--check'),
        ('docs/DOC_MAP.gen.py', '--selftest'),
        ('docs/diagrams/timesync_chain.gen.py', '--check'),
        ('docs/diagrams/timesync_chain.gen.py', '--selftest'),
        ('docs/diagrams/submodule_boundaries.gen.py', '--check'),
        ('docs/diagrams/submodule_boundaries.gen.py', '--selftest'),
        ('scripts/check_diagram_pngs.py', ''),
        ('scripts/check_diagram_pngs.py', '--selftest'),
        ('scripts/check_sweep_shape.py', '--self-test'),
        ('scripts/check_deploy_shape.py', '--selftest'),
    ]
    commands = [(Path(path).stem + ('-' + Path(args.split()[0]).name.lstrip('-') if args else ''),
                 ['python3','-B',path,*args.split()]) for path,args in rows]
    commands += [('gptp-docs', ['make','-C','gptp-processor','docs']),
                 ('git-diff-worktree',['git','diff','--check']),
                 ('git-diff-committed',['git','diff','--check',base,'HEAD'])]
receipt = out / 'gate-results.json'
results = json.loads(receipt.read_text()) if receipt.exists() else []
failed = False
for label, command in commands:
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip() == head
    log = logs / (label + '.log')
    start = time.monotonic()
    print('START', label, flush=True)
    with log.open('w') as stream:
        result = subprocess.run(command,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=7200)
    row = dict(name=label,head=head,command=command,rc=result.returncode,
               elapsed_s=round(time.monotonic()-start,2),log=str(log),size=log.stat().st_size,
               sha256=hashlib.sha256(log.read_bytes()).hexdigest())
    results.append(row)
    receipt.write_text(json.dumps(results,indent=2)+'\n')
    print('FINISH',label,'rc='+str(result.returncode),'seconds='+str(row['elapsed_s']),flush=True)
    failed |= result.returncode != 0
sys.exit(int(failed))
