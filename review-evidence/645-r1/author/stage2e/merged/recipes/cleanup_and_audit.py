import hashlib, json, os, subprocess
from pathlib import Path
repo=Path(os.environ["REPO"]).resolve()
m=Path(__file__).parent.resolve()
e=Path(os.environ["EVIDENCE"])
assert int((m/"all-functional.rc").read_text())==0
assert int((m/"all-measurements.rc").read_text())==0
pairs={"sw/builder/out":m/"route/builder", "configs/generated/ltn_rom.hex":m/"route/roms/ltn_rom.hex", "configs/generated/ucode.hex":m/"route/roms/ucode.hex"}
removed=[]
for name,target in pairs.items():
    p=repo/name
    assert p.is_symlink(), name
    assert p.resolve()==target.resolve(), (name,str(p.resolve()))
for name in pairs:
    (repo/name).unlink()
    removed.append(name)
def git(*args):
    return subprocess.check_output(["git",*args],cwd=repo,text=True).strip()
submodules={}
# Submodule paths come from the repository's own .gitmodules.
paths=subprocess.check_output(["git","config","--file",".gitmodules","--get-regexp","path"],cwd=repo,text=True)
for row in paths.splitlines():
    rel=row.split(None,1)[1]
    d=repo/rel
    if not (d/".git").exists():
        submodules[rel]={"initialized":False,"checked":False}
        continue
    top=subprocess.check_output(["git","-C",str(d),"rev-parse","--show-toplevel"],text=True).strip()
    assert Path(top).resolve()==d.resolve(), rel
    status=subprocess.check_output(["git","-C",str(d),"status","--porcelain","--untracked-files=all","--ignored"],text=True)
    assert not status.strip(), (rel,status)
    top=subprocess.check_output(["git","-C",str(d),"rev-parse","--show-toplevel"],text=True).strip()
    assert Path(top).resolve()==d.resolve(), rel
    pin=subprocess.check_output(["git","-C",str(d),"rev-parse","HEAD"],text=True).strip()
    submodules[rel]={"head":pin,"clean_including_ignored":True}
status=git("status","--porcelain","--untracked-files=all","--ignored")
assert not status, status
result={"head":git("rev-parse","HEAD"),"branch":git("branch","--show-current"),"origin":git("remote","get-url","origin"),"removed_generated_symlinks":removed,"root_clean_including_ignored":True,"submodules":submodules}
assert result["branch"]=="645-ring-slip"
assert result["origin"]=="https://github.com/kebag-logic/milan-fpga.git"
(e/"final-clean-state.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
