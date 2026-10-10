"""Documentation and static gate set from .github/workflows/docs.yml (docs-check, wire-accountability,
docs-check-no-git) plus the fast-workflow self-tests, run at one exact head in a clean worktree.

The candidate's own act runner self-test is not run on the host (AGENTS.md section 5).
"""
import concurrent.futures,json,os,shutil,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
repo=Path(sys.argv[1]).resolve(); tag=sys.argv[2]
out=w/('docs-'+tag);out.mkdir(exist_ok=True)
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
base=subprocess.check_output(['git','-C',str(repo),'merge-base','origin/dev','HEAD'],text=True).strip()
md='<doc-env>'
hdl='<scratch>/venv-hdl/bin/python3'
sdk='<sdk>'
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1',MILAN_RV32_CC=sdk+'/bin/riscv32-linux-gcc',VERILATOR='<pinned-compiler>/verilator',VERILATOR_JOBS='2')
env['PATH']=md+os.pathsep+sdk+'/bin'+os.pathsep+env['PATH']
P='python3'
C=[
 ('hdl-reference-selftest',[hdl,'scripts/gen_hdl_reference.py','--selftest']),
 ('hdl-reference',[hdl,'scripts/gen_hdl_reference.py','--output',str(out/'hdl-reference')]),
 ('docs-check',[P,'scripts/docs_check.py']),
 ('em-dash',[P,'scripts/check_em_dash.py','--base',base]),
 ('em-dash-selftest',[P,'scripts/check_em_dash.py','--selftest']),
 ('doc-style',[P,'scripts/check_doc_style.py']),('doc-style-selftest',[P,'scripts/check_doc_style.py','--selftest']),
 ('gptp-docs',[P,'scripts/check_gptp_docs.py']),('gptp-docs-selftest',[P,'scripts/check_gptp_docs.py','--selftest']),
 ('doc-map',[P,'docs/DOC_MAP.gen.py','--check']),('doc-map-selftest',[P,'docs/DOC_MAP.gen.py','--selftest']),
 ('timesync-chain',[P,'docs/diagrams/timesync_chain.gen.py','--check']),('timesync-chain-selftest',[P,'docs/diagrams/timesync_chain.gen.py','--selftest']),
 ('solution-docs',[P,'scripts/check_solution_docs.py']),('solution-docs-selftest',[P,'scripts/check_solution_docs.py','--selftest']),
 ('submodule-boundaries',[P,'docs/diagrams/submodule_boundaries.gen.py','--check']),('submodule-boundaries-selftest',[P,'docs/diagrams/submodule_boundaries.gen.py','--selftest']),
 ('submodule-docs',[P,'scripts/check_submodule_docs.py']),('submodule-docs-selftest',[P,'scripts/check_submodule_docs.py','--selftest']),
 ('wavedrom-selftest',[P,'scripts/gen_wavedrom.py','--selftest']),
 ('wavedrom-axis',[P,'scripts/gen_wavedrom.py','docs/diagrams/wd_axis_backpressure.json','--background=white','--check']),
 ('wavedrom-cdc',[P,'scripts/gen_wavedrom.py','docs/diagrams/wd_cdc_handshake.json','--background=white','--check']),
 ('wavedrom-pdelay',[P,'scripts/gen_wavedrom.py','docs/diagrams/wd_gptp_pdelay.json','--background=white','--check']),
 ('diagram-pngs',[P,'scripts/check_diagram_pngs.py']),('diagram-pngs-selftest',[P,'scripts/check_diagram_pngs.py','--selftest']),
 ('feature-status',[P,'scripts/check_feature_status.py','--self-test']),
 ('module-matrix',[P,'docs/traceability/gen_module_matrix.py','--check']),
 ('gptp-docs-submodule',[P,'scripts/check_gptp_docs.py','--with-submodule']),
 ('gptp-processor-docs',['make','-C','gptp-processor','docs']),
 ('control-flow-selftest',[P,'scripts/measure_control_flow.py','--selftest']),('cohesion-selftest',[P,'scripts/measure_cohesion.py','--selftest']),
 ('baremetal',[P,'scripts/check_baremetal_only.py','--check']),('baremetal-selftest',[P,'scripts/check_baremetal_only.py','--selftest']),
 ('rv32-sdk-selftest',[P,'scripts/ci_rv32_sdk_selftest.py']),('rv32-sdk-verify',[P,'scripts/ci_rv32_sdk.py','--destination',sdk,'--verify-only']),
 ('firmware-compiler-selftest',[P,'sw/builder/test_firmware_compiler.py','--selftest']),
 ('firmware-compiler-absent',[P,'sw/builder/test_firmware_compiler.py','--absent','--audit',str(out/'rv32-absent.jsonl')]),
 ('builder',[P,'sw/builder/test_builder.py','--require-rv32']),
 ('nvm-record-space',[P,'scripts/check_nvm_record_space.py']),('nvm-record-space-selftest',[P,'scripts/check_nvm_record_space.py','--self-test']),
 ('nvm-capture',[P,'scripts/check_nvm_capture.py']),
 ('nvm-firmware-selftest',[P,'sw/firmware/nvm_hosttest/test_nvm_firmware.py','--self-test']),
 ('soc-sources',[P,'scripts/check_soc_sources.py']),('soc-sources-selftest',[P,'scripts/check_soc_sources.py','--selftest']),
 ('iob-pack-selftest',[P,'sw/litex/iob_pack_selftest.py']),
 ('rtl-source-lists',[P,'scripts/check_rtl_source_lists.py']),('rtl-source-lists-selftest',[P,'scripts/check_rtl_source_lists.py','--selftest']),
 ('naming',[P,'scripts/measure_naming.py','--check']),('naming-selftest',[P,'scripts/measure_naming.py','--selftest']),
 ('ports',[P,'scripts/check_port_contracts.py']),('ports-selftest',[P,'scripts/check_port_contracts.py','--selftest']),
 ('fail-fast',[P,'scripts/measure_fail_fast.py','--check']),('fail-fast-selftest',[P,'scripts/measure_fail_fast.py','--selftest']),
 ('todo-ownership',[P,'scripts/check_todo_ownership.py']),('todo-ownership-selftest',[P,'scripts/check_todo_ownership.py','--selftest']),
 ('test-evidence',[P,'scripts/measure_test_evidence.py','--check']),('test-evidence-selftest',[P,'scripts/measure_test_evidence.py','--selftest']),
 ('hygiene',[P,'scripts/check_hygiene.py','--check']),('hygiene-selftest',[P,'scripts/check_hygiene.py','--selftest']),
 ('sv-idiom',[P,'scripts/check_sv_idiom.py']),('sv-idiom-selftest',[P,'scripts/check_sv_idiom.py','--selftest']),
 ('cpp-idiom',[P,'scripts/check_cpp_idiom.py']),('cpp-idiom-selftest',[P,'scripts/check_cpp_idiom.py','--selftest']),
 ('py-idiom',[P,'scripts/check_py_idiom.py']),('py-idiom-selftest',[P,'scripts/check_py_idiom.py','--selftest']),
 ('sh-idiom',[P,'scripts/check_sh_idiom.py']),('sh-idiom-selftest',[P,'scripts/check_sh_idiom.py','--selftest']),
 ('ci-events',[P,'scripts/ci_events.py','--check']),('ci-events-selftest',[P,'scripts/ci_events.py','--selftest']),
 ('doc-paths',[P,'scripts/check_doc_paths.py']),
 ('archive',[P,'scripts/check_archive.py']),('archive-selftest',[P,'scripts/check_archive.py','--selftest']),
 ('toc-selftest',[P,'scripts/gen_toc.py','--selftest']),('toc-anchors',[P,'scripts/gen_toc.py','--verify-anchors']),('toc',[P,'scripts/gen_toc.py','--check']),
 ('aem-store-selftest',[P,'avdecc/gen_aem_store.py','--self-test']),
 ('sweep-shape-selftest',[P,'scripts/check_sweep_shape.py','--self-test']),
 ('deploy-shape-selftest',[P,'scripts/check_deploy_shape.py','--self-test']),
 ('entity-shape-selftest',[P,'scripts/check_entity_shape.py','--self-test']),
 ('wire-accountability-selftest',[P,'scripts/check_wire_accountability.py','--self-test']),
 ('pp-srcs',[P,'scripts/pp_srcs.py','--check','--selftest']),
 ('ooc-dp-srcs-selftest',[P,'syn/ooc/dp_srcs.py','--selftest']),
 ('ooc-tcl-selftest',[P,'syn/ooc/ooc_tcl_selftest.py']),
 ('recipe-selftest',[P,'syn/ooc/pp_baseline.py','--selftest']),
 ('recipe-mutants',[P,'syn/ooc/pp_baseline_mutants.py']),
 ('recipe-reports-selftest',[P,'syn/ooc/pp_baseline_reports_selftest.py']),
 ('resource-gate-selftest',[P,'syn/ooc/pp_resource_gate.py','--selftest']),
 ('resource-gate-mutants',[P,'syn/ooc/pp_resource_gate_mutants.py']),
 ('resource-check-baseline',[P,'syn/ooc/pp_resource_gate.py','check-baseline']),
 ('yosys-ooc-selftest',[P,'syn/yosys/ooc_selftest.py']),
 ('yosys-guard-selftest',[P,'syn/yosys/guard_selftest.py']),
 ('yosys-cache-selftest',[P,'syn/yosys/cache_selftest.py']),
]
(w/'tmp').mkdir(exist_ok=True)
rows=[]
def run(entry,cwd=repo):
 name,argv=entry;start=time.time()
 with (out/(name+'.log')).open('w') as log:
  rc=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,rc,flush=True)
 return dict(name=name,argv=[str(a) for a in argv],cwd=str(cwd),rc=rc,seconds=round(time.time()-start,1))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 rows=list(pool.map(run,C))
# docs-check-no-git: the same docs gate on an exported tree without git metadata.
nogit=out/'nogit'
if nogit.exists():shutil.rmtree(nogit)
nogit.mkdir()
archive=subprocess.run(['git','-C',str(repo),'archive','--format=tar','HEAD'],check=True,capture_output=True).stdout
subprocess.run(['tar','-x','-C',str(nogit)],input=archive,check=True)
rows.append(run(('nogit-docs-check',[P,'scripts/docs_check.py']),nogit))
rows.append(run(('nogit-feature-status',[P,'scripts/check_feature_status.py']),nogit))
shutil.rmtree(nogit)
status=subprocess.run(['git','-C',str(repo),'status','--short'],capture_output=True,text=True).stdout
sub=subprocess.run(['git','-C',str(repo/'gptp-processor'),'status','--short'],capture_output=True,text=True).stdout
result=dict(head=head,em_dash_base=base,rows=rows,tree_status=status,gptp_processor_status=sub)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
bad=[r['name'] for r in rows if r['rc']]
print('FAILED:',bad) if bad else print('all',len(rows),'rc 0')
raise SystemExit(1 if bad or status or sub else 0)
