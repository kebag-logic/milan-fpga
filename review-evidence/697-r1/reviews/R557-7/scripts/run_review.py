#!/usr/bin/env python3
"""Run bounded, concurrent source-head verification; retain each log and status."""
import concurrent.futures,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(sys.argv[2]).resolve()
work=packet/"scratch/local";work.mkdir(parents=True,exist_ok=True)
sdk=packet/"scratch/sdk";env=dict(os.environ)
env.update(PYTHONDONTWRITEBYTECODE="1",TSN_CLANG=str(sdk/"root/usr/bin/clang-18"),LD_LIBRARY_PATH=str(sdk/"root/usr/lib/x86_64-linux-gnu"),CMAKE_PREFIX_PATH=str(sdk/"gtest"),PKG_CONFIG_PATH=str(sdk/"gtest/lib/pkgconfig"),CPLUS_INCLUDE_PATH=str(sdk/"gtest/include"),LIBRARY_PATH=str(sdk/"gtest/lib"),ASAN_OPTIONS="detect_leaks=1:halt_on_error=1",UBSAN_OPTIONS="halt_on_error=1",TMPDIR=str(work/"tmp"))
(work/"tmp").mkdir(exist_ok=True)
for k in list(env):
 if k.startswith("GTEST_"):del env[k]
(packet/"scratch/environment.json").write_text(json.dumps({k:env[k] for k in ["TSN_CLANG","LD_LIBRARY_PATH","CMAKE_PREFIX_PATH","PKG_CONFIG_PATH","CPLUS_INCLUDE_PATH","LIBRARY_PATH","ASAN_OPTIONS","UBSAN_OPTIONS","TMPDIR","PYTHONDONTWRITEBYTECODE"]},indent=2))
rows=[]
def command(name,args):
 start=time.monotonic()
 with (work/(name+".log")).open("w") as f:
  rc=subprocess.run(args,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (work/(name+".rc")).write_text(str(rc)+"\n")
 row={"gate":name,"rc":rc,"seconds":round(time.monotonic()-start,2)};rows.append(row)
 print(json.dumps(row),flush=True);return rc

def build(name,cc,cxx,option):
 directory=work/name
 if command(name+"-configure",["cmake","-S",str(root),"-B",str(directory),"-DCMAKE_BUILD_TYPE=Debug","-DCMAKE_C_COMPILER="+cc,"-DCMAKE_CXX_COMPILER="+cxx,option]):return
 if command(name+"-build",["cmake","--build",str(directory),"-j2"]):return
 if command(name+"-test",["ctest","--test-dir",str(directory),"--output-on-failure","-j2"]):return
 if name=="gcc":command("coverage",[sys.executable,"scripts/coverage.py",str(directory)])

def py(name,script,extra=()):return command(name,[sys.executable,"scripts/"+script,*extra])
def controls():
 cases=[("comments","check_comments.py",["--selftest","--work",str(work/"comment-controls")]),("assertion-templates","assertion_templates.py",["--check","--selftest","--work",str(work/"templates")]),("dependencies","dependency_selftest.py",["--work",str(work/"dependencies"),"--jobs","2"]),("needles","needle_audit.py",["--selftest"]),("boundary","check_boundary.py",["--selftest","--work",str(work/"boundary"),"--jobs","2"]),("conditionals","check_conditionals.py",["--selftest","--work",str(work/"conditionals"),"--jobs","2"]),("port-contracts","check_port_contracts.py",["--selftest"]),("report-controls","mutation_selftest.py",["--work",str(work/"reports"),"--jobs","2"]),("registration","registration_selftest.py",["--work",str(work/"registration-controls")]),("license","check_license.py",["--selftest"]),("traceability","traceability.py",["--selftest","--build",str(work/"gcc"),"--jobs","2"]),("inventory","test_inventory.py",["--build",str(work/"gcc"),"--jobs","2"]),("coverage-controls","coverage_selftest.py",[]),("privacy","check_privacy.py",[])]
 for name,script,args in cases:py(name,script,args)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 futures=[pool.submit(build,"gcc","gcc","g++","-DTSN_COVERAGE=ON"),pool.submit(build,"clang","clang","clang++","-DTSN_SANITIZERS=ON"),pool.submit(py,"mutation","mutation.py",["--work",str(work/"mutations"),"--jobs","4"]),pool.submit(py,"rv32","baremetal.py",["--work",str(work/"rv32"),"--jobs","2"]),pool.submit(controls)]
 for f in futures:f.result()
(work/"gates.json").write_text(json.dumps(rows,indent=2)+"\n")
sys.exit(any(x["rc"] for x in rows))
