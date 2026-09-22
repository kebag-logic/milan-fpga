from pathlib import Path
import json,subprocess,sys
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
commands=[('policy-check', ['scripts/check_baremetal_only.py', '--check']), ('policy-selftest', ['scripts/check_baremetal_only.py', '--selftest']), ('python-selftest', ['scripts/check_py_idiom.py', '--selftest']), ('shell-selftest', ['scripts/check_sh_idiom.py', '--selftest']), ('evidence-selftest', ['scripts/measure_test_evidence.py', '--selftest']), ('fail-fast-selftest', ['scripts/measure_fail_fast.py', '--selftest']), ('docs-selftest', ['scripts/docs_check.py', '--selftest']), ('em-dash-selftest', ['scripts/check_em_dash.py', '--selftest']), ('contents-selftest', ['scripts/gen_toc.py', '--selftest']), ('hygiene-selftest', ['scripts/check_hygiene.py', '--selftest']), ('todo-selftest', ['scripts/check_todo_ownership.py', '--selftest'])]
rows=[]
for name,args in commands:
 cmd=['rtk','proxy','python3',*args]
 p=subprocess.run(['rtk','proxy','python3',str(out.parent/'scripts/record.py'),str(out/name),*cmd])
 rows.append({'name':name,'argv':cmd,'exit':p.returncode})
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(int(any(r['exit'] for r in rows)))
