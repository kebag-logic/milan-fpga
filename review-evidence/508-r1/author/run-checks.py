from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
checks=[
('pp-srcs',['python3','scripts/pp_srcs.py','--check','--selftest']),
('docs-git',['python3','scripts/docs_check.py']),
('docs-no-git',['env','GIT_DIR=/nonexistent-508-a295-git','python3','scripts/docs_check.py']),
('em-dash',['python3','scripts/check_em_dash.py','--base','c266432dcb0cdd464205823a3d82cad260eedde2']),
('doc-style',['python3','scripts/check_doc_style.py']),
('toc',['python3','scripts/gen_toc.py','--check']),
('doc-paths',['python3','scripts/check_doc_paths.py']),
('module-matrix',['python3','docs/traceability/gen_module_matrix.py','--check']),
('xvlog',['python3','scripts/xvlog_gate.py','--check']),
('rtl-lists',['python3','scripts/check_rtl_source_lists.py']),
('cpp-idiom',['python3','scripts/check_cpp_idiom.py']),
('py-idiom',['python3','scripts/check_py_idiom.py']),
('port-contracts',['python3','scripts/check_port_contracts.py']),
('naming',['python3','scripts/measure_naming.py','--check']),
('test-evidence',['python3','scripts/measure_test_evidence.py','--check']),
('test-evidence-selftest',['python3','scripts/measure_test_evidence.py','--selftest']),
('rtl-lint',['python3','scripts/lint_rtl.py','--check']),
('diff-check',['git','diff','--check']),
]
failed=[]
for name,args in checks:
 rc=subprocess.run(['python3',str(p/'run_gate.py'),name+('' if len(sys.argv)<2 else '-'+sys.argv[1]),*args]).returncode
 if rc:failed.append(name)
print('FAILED',failed,flush=True)
sys.exit(bool(failed))
