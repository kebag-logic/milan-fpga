#!/bin/bash
# Round 8 gates at the head: documentation and idiom gates, standalone self-tests, and fixture identity.
R=$VALIDATION_STORAGE/r8; V=$VALIDATION_STORAGE/docs-venv/bin/python
cd $SOURCE
run(){ n=$1; shift; "$@" > $R/gate-$n.log 2>&1; echo "$n $?" | tee -a $R/gates8.rc; }
: > $R/gates8.rc
echo "HEAD $(git rev-parse HEAD)" | tee -a $R/gates8.rc
run docs-check python3 -B scripts/docs_check.py
run doc-style python3 -B scripts/check_doc_style.py
run doc-paths python3 -B scripts/check_doc_paths.py
run gptp-docs python3 -B scripts/check_gptp_docs.py
run inventory python3 -B scripts/docs_inventory.py --check
run idiom python3 -B scripts/check_py_idiom.py
run cpp-idiom python3 -B scripts/check_cpp_idiom.py
run em-dash $V -B scripts/check_em_dash.py --base c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350
run toc-check $V -B scripts/gen_toc.py --check
run toc-verify-anchors $V -B scripts/gen_toc.py --verify-anchors
for t in rows_tiers load_grade egress_ledger record_classes arty_grade kept_grade; do
  run standalone-$t python3 -I -B tb/verilator/ctrl_service_budget/$t.py --selftest
done
run arty-grade python3 -I -B tb/verilator/ctrl_service_budget/arty_grade.py
run fixtures python3 -I -B -c "
import subprocess,sys,types
src={r:subprocess.check_output(['git','show',r+':sw/firmware/ctrl/test/ctrl_mutant_fixtures.py']).decode() for r in ('4adfa9dc8','HEAD')}
vals=[]
for r,s in src.items():
    m=types.ModuleType('f'); exec(compile(s,'f','exec'),m.__dict__); vals.append({k:v for k,v in vars(m).items() if not k.startswith('__')})
print('fixture values identical:',vals[0]==vals[1],len(vals[0]),'names'); sys.exit(vals[0]!=vals[1])"
