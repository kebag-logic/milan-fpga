#!/usr/bin/env python3
"""Run independent, read-only review spot checks; logs and status per command."""
import concurrent.futures, os, pathlib, subprocess, sys
repo=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True)
cases=[("ports",["scripts/check_port_contracts.py"]),("ports-selftest",["scripts/check_port_contracts.py","--selftest"]),("cpp",["scripts/check_cpp_idiom.py"]),("cpp-selftest",["scripts/check_cpp_idiom.py","--selftest"]),("test-evidence",["scripts/measure_test_evidence.py","--check"]),("capture",["scripts/check_nvm_capture.py"]),("record-space",["scripts/check_nvm_record_space.py"])]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
def run(case):
    name,args=case
    with (out/(name+".log")).open("w") as log:
        rc=subprocess.run([sys.executable,*args],cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    (out/(name+".rc")).write_text(str(rc)+"\n")
    return name,rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,cases))
for name,rc in results: print(name,rc)
sys.exit(any(rc for _,rc in results))
