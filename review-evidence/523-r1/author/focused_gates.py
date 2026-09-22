"""Run only the author-owned focused bank, retaining each exact receipt."""
import pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parent
checks=[
 ("python-idiom",["python3","scripts/check_py_idiom.py"]),
 ("python-idiom-selftest",["python3","scripts/check_py_idiom.py","--selftest"]),
 ("shell-idiom",["python3","scripts/check_sh_idiom.py"]),
 ("shell-idiom-selftest",["python3","scripts/check_sh_idiom.py","--selftest"]),
 ("evidence",["python3","scripts/measure_test_evidence.py","--check"]),
 ("evidence-selftest",["python3","scripts/measure_test_evidence.py","--selftest"]),
 ("fail-fast",["python3","scripts/measure_fail_fast.py","--check"]),
 ("fail-fast-selftest",["python3","scripts/measure_fail_fast.py","--selftest"]),
 ("baremetal",["python3","scripts/check_baremetal_only.py","--check"]),
 ("baremetal-selftest",["python3","scripts/check_baremetal_only.py","--selftest"]),
 ("docs",["python3","scripts/docs_check.py"]),
 ("doc-style",["python3","scripts/check_doc_style.py"]),
 ("doc-style-selftest",["python3","scripts/check_doc_style.py","--selftest"]),
 ("gptp-docs",["python3","scripts/check_gptp_docs.py","--with-submodule"]),
 ("gptp-docs-selftest",["python3","scripts/check_gptp_docs.py","--selftest"]),
 ("em-dash",["python3","scripts/check_em_dash.py","--base","483a133ed08867ea0d300d2b4a027b5b48a4282f"]),
 ("doc-paths",["python3","scripts/check_doc_paths.py"]),
 ("contents",["python3","scripts/gen_toc.py","--check"]),
 ("contents-anchors",["python3","scripts/gen_toc.py","--verify-anchors"]),
 ("tally-selftest",["python3","scripts/suite_tally.py","--selftest"]),
 ("shards-selftest",["python3","scripts/suite_shards.py","--selftest"]),
 ("shell-syntax",["bash","-n","scripts/run_all_suites.sh"]),
 ("sweep-cancellation",["python3","scripts/test_suite_cancellation.py"]),
 ("mutation-lifecycle",["python3","tb/verilator/gptp_shadow/test_mutant_lifecycle.py"]),
]
failed=[]
for name,argv in checks:
    label=sys.argv[1]+"-"+name
    result=subprocess.run([sys.executable,str(root/"run_receipt.py"),label,*argv],capture_output=True,text=True,check=False)
    print(name, "exit", result.returncode,flush=True)
    if result.returncode:
        print(result.stdout,result.stderr,flush=True)
        failed.append(name)
print("Failed:",failed,flush=True)
sys.exit(bool(failed))
