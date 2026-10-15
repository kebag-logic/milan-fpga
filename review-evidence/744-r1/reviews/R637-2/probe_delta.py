"""Focused falsification checks. No tracked source is written."""
import ast, hashlib, importlib.util, os, pathlib, subprocess, sys, tempfile
ROOT=pathlib.Path(sys.argv[1]).resolve()
PACKET=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"scripts"))
import ci_runtime_workflows as runtime
import check_baremetal_only as policy
print("Source head:",subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip())
print("act_ci.py SHA-256:",hashlib.sha256((ROOT/"scripts/act_ci.py").read_bytes()).hexdigest())
assert sum(map(len,policy.HOST_MEMORY_READS.values()))==14
for path,lines in policy.HOST_MEMORY_READS.items():
    source=(ROOT/path).read_text().splitlines()
    for line in lines: assert source.count(line)==1,(path,line)
print("All 14 declarations occur exactly once in their declared current file")
assert runtime.CENSUS_WORKER_BYTES==1213100*1024==1242214400
published=PACKET/"public/author-r2/evidence/r2/budget-step-head.sh"
assert published.read_text()==runtime.census_budget_step()["run"]
print("Published exact-head budget shell equals current generator output byte-for-byte")
with tempfile.TemporaryDirectory(dir=PACKET/"scratch",prefix="budget-") as td:
    top=pathlib.Path(td)
    cases=[("8GiB",{},"4"),("4GiB ancestor",{"ancestor":str(4*2**30)},"2"),
           ("absent controller",{"absent":True},"16"),
           ("unreadable leaf",{"deny":"leaf"},None),
           ("unreadable ancestor",{"deny":"ancestor"},None),
           ("unsearchable ancestor",{"deny":"directory"},None),
           ("leaf directory",{"nonfile":"leaf"},None),
           ("ancestor directory",{"nonfile":"ancestor"},None)]
    for n,(name,config,want) in enumerate(cases):
        root=top/str(n); root.mkdir(); hierarchy=root/"sys"; leaf=hierarchy/"a/b"; leaf.mkdir(parents=True)
        (root/"meminfo").write_text(f"MemTotal: {61*1024*1024} kB\n")
        (root/"self-cgroup").write_text("0::/a/b\n")
        (root/"nproc").write_text("#!/bin/sh\necho 16\n"); (root/"nproc").chmod(0o755)
        files={"leaf":leaf/"memory.max","ancestor":hierarchy/"a/memory.max"}
        if not config.get("absent"):
            files["leaf"].write_text(str(8*2**30)); files["ancestor"].write_text(config.get("ancestor","max"))
        if config.get("nonfile"):
            path=files[config["nonfile"]]; path.unlink(); path.mkdir()
        denied=None
        if config.get("deny"):
            denied=hierarchy/"a" if config["deny"]=="directory" else files[config["deny"]]
            denied.chmod(0)
            if os.geteuid()==0:
                print(name,"SKIP: effective uid zero bypasses permissions"); denied.chmod(0o755); continue
        envfile=root/"env"
        shell=runtime.census_budget_step()["run"]
        for old,new in [("/proc/meminfo",root/"meminfo"),("/proc/self/cgroup",root/"self-cgroup"),("/sys/fs/cgroup",hierarchy)]: shell=shell.replace(old,str(new))
        try:
            result=subprocess.run(["bash","-c",shell],env={**os.environ,"PATH":str(root)+":"+os.environ["PATH"],"GITHUB_ENV":str(envfile)},capture_output=True,text=True,timeout=5)
        finally:
            if denied: denied.chmod(0o755)
        content=envfile.read_text() if envfile.exists() else None
        if want is None: assert result.returncode!=0 and content is None,(name,result,content)
        else: assert result.returncode==0 and content==f"CI_CENSUS_JOBS={want}\n",(name,result,content)
        print(name,"rc",result.returncode,"export",repr(content),"PASS")
print("Focused delta probes PASS")
