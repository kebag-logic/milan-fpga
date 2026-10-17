#!/usr/bin/env python3
"""Read-only exact-head, index, worktree and documentation-delta audit."""
import hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])
head = "befe50d11df208676a28a748e5a74b5845400e95"
previous = "6aaec5dfc45e84c8842f3f31f76910bfa91a96e1"
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == "72f13f55b8617b16bdc54b0ec1e2bc88a3d1599b"
assert git("show", "-s", "--format=%P", "HEAD").decode().strip() == previous
assert not git("diff", "--cached", "HEAD", "--")
changes=git("diff", "--name-only", previous, head).decode().splitlines()
assert changes == ["docs/architecture/06_aecp_engine.md", "tb/pp_top/README.md"]
assert git("diff", "--name-status", previous, head).decode().splitlines() == ["M\t"+x for x in changes]
rows=[]; gitlinks=[]
for row in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not row: continue
    meta, name = row.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    path = name.decode()
    if mode == "160000":
        gitlinks.append({"path":path,"commit":oid}); continue
    f=root/path
    content=os.readlink(f).encode() if mode == "120000" else f.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
    actualmode="120000" if f.is_symlink() else ("100755" if f.stat().st_mode & stat.S_IXUSR else "100644")
    assert blob == oid and actualmode == mode, path
    rows.append({"path":path,"mode":mode,"blob":oid})
assert not gitlinks, "Inspect any newly discovered required gitlinks"
engine=(root/"hdl/aecp/KL_aecp_engine.sv").read_text()
assert "if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;" in engine
architecture=" ".join((root/changes[0]).read_text().split())
assert "a command under cdl 16 lacks the complete descriptor_type/descriptor_index pair and answers `BAD_ARGUMENTS`" in architecture
cpp=(root/"tb/pp_top/sim_main.cpp").read_text()
body=cpp.split("static const Row kRows[] = {",1)[1].split("};",1)[0]
cases=[(int(a,16),int(b),int(c)) for a,b,c in re.findall(r"\{0x([0-9A-F]+), (\d+), (\d+),",body)]
short=[x for x in cases if x[2]==4]
assert len(short)==12 and len({x[0] for x in short})==11
low=[x[0] for x in short if x[0] != 9 and (x[0]&255)==9]
assert low == [0x0109,0x8009]
assert len(cases)==13 and cases[-1]==(0x24,0,8)
print(json.dumps({"head":head,"tree":git("rev-parse","HEAD^{tree}").decode().strip(),"parent":previous,"changed_files":changes,"tracked_files_verified":len(rows),"index_matches_head":True,"gitlinks":gitlinks,"cdl_16_rows":len(short),"distinct_types":len({x[0] for x in short}),"low_byte_aliases":[hex(x) for x in low],"tracked_files":rows},indent=2))
