#!/usr/bin/env python3
"""Read-only parent and three-pin source/index/mode receipts."""
import ast,base64,hashlib,json,os,pathlib,stat,subprocess,sys
BASE="483a133ed08867ea0d300d2b4a027b5b48a4282f"
PINS=("gptp-processor","protocol-processor","third_party/verilog-axis")
ROOT=pathlib.Path.cwd()
OUT=pathlib.Path(__file__).resolve().parent

def git(root,*args):
    return subprocess.check_output(["git","--no-optional-locks","--no-replace-objects","-C",str(root),*args])

def tree(root):
    raw=git(root,"ls-files","--stage","-z")
    rows={}
    for entry in raw.split(b"\0"):
        if not entry: continue
        metadata,raw_name=entry.split(b"\t",1)
        mode,oid,stage=metadata.decode().split()
        name=os.fsdecode(raw_name)
        path=root/name
        item=dict(index_mode=mode,index_oid=oid,stage=stage)
        if mode=="160000":
            item["kind"]="gitlink"
        else:
            st=path.lstat()
            data=os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
            item.update(kind="symlink" if stat.S_ISLNK(st.st_mode) else "file",mode=oct(st.st_mode),
                        sha256=hashlib.sha256(data).hexdigest(),size=len(data),
                        actual_git_blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest())
            assert item["actual_git_blob"]==oid, (root,name,"tracked bytes differ from index")
            if not stat.S_ISLNK(st.st_mode):
                assert bool(st.st_mode & stat.S_IXUSR)==(mode=="100755"), (root,name,"executable mode")
        rows[name]=item
    return dict(head=git(root,"rev-parse","HEAD").decode().strip(),
                tree=git(root,"rev-parse","HEAD^{tree}").decode().strip(),
                index_base64=base64.b64encode(raw).decode(),
                index_flags_base64=base64.b64encode(git(root,"ls-files","-v","-z")).decode(),files=rows)
result=dict(base=BASE,parent=tree(ROOT),pins={})
for name in PINS:
    result["pins"][name]=tree(ROOT/name)
    assert result["pins"][name]["head"]==result["parent"]["files"][name]["index_oid"]
    assert git(ROOT,"ls-tree",BASE,"--",name)==git(ROOT,"ls-tree","HEAD","--",name)
path="tb/verilator/gptp_shadow/mutants.py"
def populations(text):
    return {n.targets[0].id:ast.dump(n.value,include_attributes=False) for n in ast.parse(text).body
            if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)
            and n.targets[0].id in ("MUTATIONS","NOT_SEPARATELY_OBSERVABLE")}
prior=populations(git(ROOT,"show",BASE+":"+path).decode())
current=populations((ROOT/path).read_text())
assert prior==current
result["mutation_populations"]=dict(unchanged=True,ast_sha256={k:hashlib.sha256(v.encode()).hexdigest() for k,v in current.items()})
for path in ("tb/verilator/gptp_shadow/sim_main.cpp","tb/verilator/gptp_shadow/gptp_shadow_wrap.sv",
             "scripts/suite_shards.py","scripts/suite_tally.py"):
    assert git(ROOT,"show",BASE+":"+path)==(ROOT/path).read_bytes(), path
assert not git(ROOT,"diff","--name-only",BASE,"HEAD","--","hdl","sw","tb/verilator/milan_dp")
result["unchanged_product_and_pool"]=True
result["status"]=git(ROOT,"status","--porcelain=v1").decode()
assert not result["status"], result["status"]
label=sys.argv[1]
(OUT/(label+".json")).write_text(json.dumps(result,indent=2)+"\n")
if len(sys.argv)>2:
    previous=json.loads((OUT/(sys.argv[2]+".json")).read_text())
    assert result==previous, "tracked source/index/pin integrity changed"
print(json.dumps(dict(label=label,head=result["parent"]["head"],tree=result["parent"]["tree"],base=BASE,
    parent_files=len(result["parent"]["files"]),pins={name:dict(head=p["head"],files=len(p["files"])) for name,p in result["pins"].items()},
    exact_comparison=len(sys.argv)>2,mutation_tables_unchanged=True)))
