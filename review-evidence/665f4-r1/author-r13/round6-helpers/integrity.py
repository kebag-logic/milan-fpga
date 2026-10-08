import os
import hashlib,json,os,subprocess,shutil
from pathlib import Path
r=Path(os.environ["SCRATCH"])
root=Path.cwd().resolve()
env=os.environ.copy(); env["GIT_NO_REPLACE_OBJECTS"]="1"
def git(where,*args):
    top=subprocess.check_output(["git","-C",str(where),"rev-parse","--show-toplevel"],env=env,text=True).strip()
    assert Path(top).resolve()==where.resolve(),(where,top)
    return subprocess.check_output(["git","-C",str(where),*args],env=env)
def inspect(where):
    head=git(where,"rev-parse","HEAD").decode().strip()
    entries=git(where,"ls-tree","-rz",head).split(b"\0")
    records=[]
    for entry in filter(None,entries):
        meta,name=entry.split(b"\t",1); mode,kind,oid=meta.split()
        if kind==b"commit": continue
        path=where/os.fsdecode(name)
        data=os.readlink(path).encode() if mode==b"120000" else path.read_bytes()
        assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==oid.decode(),name
        records.append(dict(path=os.fsdecode(name),size=len(data),sha256=hashlib.sha256(data).hexdigest()))
    assert not git(where,"status","--porcelain","--untracked-files=all").strip()
    assert not git(where,"ls-files","--others","--ignored","--exclude-standard").strip()
    flags=git(where,"ls-files","-v").decode().splitlines()
    assert all(x[0] not in "hSs" for x in flags)
    return dict(head=head,verified_files=len(records),source_sha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest()),records
report={}; records={}
for key,path in [("parent",root),("lwSRP",root/"third_party/lwSRP"),("processor",root/"protocol-processor"),("gptp",root/"gptp-processor"),("axis",root/"third_party/verilog-axis"),("dependency_tests",Path(os.environ["LWSRP"]))]:
    report[key],records[key]=inspect(path)
public_src = root / "third_party/lwSRP/src"
local_src = Path(os.environ["LWSRP"])/"src"
public_files = {p.relative_to(public_src): p.read_bytes() for p in public_src.rglob("*") if p.is_file()}
local_files = {p.relative_to(local_src): p.read_bytes() for p in local_src.rglob("*") if p.is_file()}
assert public_files == local_files
report["dependency_tests"]["production_equals_public_pin"]=True
report["dependency_tests"]["branch"]=git(Path(os.environ["LWSRP"]),"branch","--show-current").decode().strip()
report["parent"]["tree"]=git(root,"rev-parse","HEAD^{tree}").decode().strip()
report["parent"]["diff_paths"]=git(root,"diff","--name-only","500b8f64443777685e6a54049d933476710d26f0","HEAD").decode().splitlines()
assert not git(root,"diff","500b8f64443777685e6a54049d933476710d26f0","HEAD","--","hdl","configs","sw/litex","sw/firmware/milan_baremetal","sw/mailbox","docs/reference/REGISTER_MAP.md").strip()
report["unchanged_default_image_rtl_and_register_map"]=True
cg=Path("/sys/fs/cgroup")/Path('/proc/self/cgroup').read_text().strip().split('::')[1].lstrip('/')
report["memory_current"]=int((cg/"memory.current").read_text())
report["memory_peak"]=int((cg/"memory.peak").read_text())
report["free_data_bytes"]=shutil.disk_usage(root).free
assert report["memory_peak"]<9000000000
assert report["free_data_bytes"]>30000000000
(r/"integrity-report.json").write_text(json.dumps(report,indent=2)+"\n")
selected=[x for x in records['parent'] if x['path'] in report['parent']['diff_paths'] or x['path'].startswith('sw/firmware/ctrl/') or x['path'].startswith('sw/firmware/gtest/')]
(r/'source.json').write_text(json.dumps(selected,indent=2)+'\n')
print(json.dumps(report,indent=2))
