import io,json,os,re,subprocess,sys,tarfile,tempfile
from pathlib import Path
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
head="1496558d82cf35fc98dda0e781b2a1be643c301a"; old="d81a302760b84f32d2aa019643f57682bb6e052c"
def run(args,cwd=None): return subprocess.run(["rtk","proxy",*map(str,args)],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
def raw(*args): return subprocess.check_output(["rtk","proxy","git","-C",str(root),*args])
results=[]
with tempfile.TemporaryDirectory(prefix="r221-docs-") as td:
 scratch=Path(td)
 for rev in [head,old]:
  repo=scratch/rev[:8]
  r=run(["git","clone","--quiet","--no-hardlinks","--no-checkout",root,repo]);assert r.returncode==0,r.stdout
  r=run(["git","checkout","--quiet","--detach",rev],repo);assert r.returncode==0,r.stdout
  assert not (repo/"protocol-processor/docs/architecture/07_memory_maps.md").exists()
  for mode in ["git","no-git"]:
   if mode=="no-git": (repo/".git").rename(scratch/(rev[:8]+"-git-metadata"))
   r=run(["python3","-B","scripts/docs_check.py"],repo)
   log=f"{rev[:8]}-{mode}.log";(out/log).write_text(r.stdout)
   want=0 if rev==head else 1
   assert r.returncode==want,(rev,mode,r.stdout)
   if rev==old: assert "ENDSTATION_BUILDER.md:963" in r.stdout and "07_memory_maps.md" in r.stdout
   results.append(dict(head=rev,mode=mode,submodules_initialized=False,exit=r.returncode,expected_exit=want,log=log))
   if rev==head:
    r=run(["python3","-B","scripts/check_feature_status.py"],repo)
    log=f"{rev[:8]}-{mode}-feature-status.log";(out/log).write_text(r.stdout);assert r.returncode==0,r.stdout
    results.append(dict(head=rev,mode=mode,command="check_feature_status.py",exit=r.returncode,log=log))
    document=repo/"docs/ENDSTATION_BUILDER.md"
    pristine=document.read_text()
    target=re.search(r"\[processor section 3.1, L10\]\(([^)]+)\)",pristine).group(1)
    old_link="../protocol-processor/docs/architecture/07_memory_maps.md#31-descriptor-tree"
    document.write_text(pristine.replace(target,old_link))
    r=run(["python3","-B","scripts/docs_check.py"],repo)
    log=f"{rev[:8]}-{mode}-old-link-control.log";(out/log).write_text(r.stdout)
    assert r.returncode==1 and "ENDSTATION_BUILDER.md:963" in r.stdout and "07_memory_maps.md" in r.stdout,r.stdout
    results.append(dict(head=rev,mode=mode,mutation="only restore old local link",exit=r.returncode,expected_exit=1,log=log))
    document.write_text(pristine)
 text=raw("show",head+":docs/ENDSTATION_BUILDER.md").decode()
 url=re.search(r"\[processor section 3.1, L10\]\(([^)]+)\)",text).group(1)
 pin=raw("rev-parse",head+":protocol-processor").decode().strip()
 assert f"/blob/{pin}/docs/architecture/07_memory_maps.md#31-descriptor-tree" in url
 previous=raw("show",old+":docs/ENDSTATION_BUILDER.md").decode()
 previous_url=re.search(r"\[processor section 3.1, L10\]\(([^)]+)\)",previous).group(1)
 assert previous_url.split("#")[1]==url.split("#")[1]
 target=(root/"protocol-processor/docs/architecture/07_memory_maps.md").read_text()
 assert "### 3.1 Descriptor tree" in target and "| L10 |" in target
 # Read the public immutable file, independently of local initialization.
 r=run(["gh","api",f"repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/contents/docs/architecture/07_memory_maps.md?ref={pin}","--jq",".content"])
 assert r.returncode==0,r.stdout
 import base64,hashlib
 remote=base64.b64decode(r.stdout);assert remote==(root/"protocol-processor/docs/architecture/07_memory_maps.md").read_bytes()
 (out/"link-target.json").write_text(json.dumps(dict(url=url,previous_url=previous_url,pin=pin,fragment="31-descriptor-tree",heading="3.1 Descriptor tree",sha256=hashlib.sha256(remote).hexdigest(),public_bytes_equal_pinned_file=True),indent=2))
(out/"results.json").write_text(json.dumps(results,indent=2)); print(json.dumps(results,indent=2))
