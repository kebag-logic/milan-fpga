#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index, gitlinks and interface preservation."""
import hashlib,json,os,pathlib,re,stat,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
C=pathlib.Path(sys.argv[1]).resolve()
def git(*args):return subprocess.check_output(["git","-C",str(C),*args])
HEAD="4865184c9ba88dd85aba3fc8036a6b74bcdb7073"
TREE="2f850bcae69e2361992a32e5f91ac97e4a81f979"
assert git("rev-parse","HEAD").decode().strip()==HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip()==TREE
entries=git("ls-tree","-rz","HEAD").split(b"\0")
fail=[];links=[];checked=[]
for entry in entries:
    if not entry:continue
    meta,path=entry.split(b"\t",1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(path)
    f=C/rel
    if mode=="160000":
        links.append({"path":rel,"gitlink":oid});continue
    data=os.fsencode(os.readlink(f)) if mode=="120000" else f.read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    realmode="120000" if f.is_symlink() else "100755" if f.stat().st_mode&0o111 else "100644"
    if actual!=oid or realmode!=mode:fail.append(rel)
    checked.append({"path":rel,"blob":oid,"mode":mode})
assert not fail
assert git("write-tree").decode().strip()==TREE
assert not git("status","--porcelain=v1","--untracked-files=all")
def blob(rev,path):return git("show",f"{rev}:{path}")
def sig(b):
    t=b.decode();i=t.index("module protocol_processor_top");return t[i:t.index(");",i)+2]
top="hdl/top/protocol_processor_top.sv"
assert sig(blob("b48312e1",top))==sig(blob(HEAD,top))
notify="hdl/aecp/KL_aecp_notify.sv"
queue=lambda b:[l.strip() for l in b.decode().splitlines() if "cmdq_" in l]
assert queue(blob("b48312e1",notify))==queue(blob(HEAD,notify))
router=git("ls-files","*event_router*").decode().splitlines()
for f in router:assert blob("b0f6f9c3",f)==blob(HEAD,f)
assert not git("diff","b0f6f9c3..HEAD","--","hdl/top","hdl/common","docs/architecture/02_interfaces.md","docs/architecture/07_memory_maps.md")
summary={"head":HEAD,"tree":TREE,"index_tree":TREE,"tracked_entries_verified":len(checked),"tracked_bytes_modes_match":True,"status_empty":True,"gitlinks":links,"top_signature_matches_b48312e1":True,"queue_lines_match_b48312e1":True,"router_files_unchanged":router,"round2_top_common_interface_map_unchanged":True,"entries":checked}
(P/"final-integrity.json").write_text(json.dumps(summary,indent=2)+"\n")
print(f"PASS: {len(checked)} tracked blobs/modes; index tree; clean status; {len(links)} gitlinks; interfaces, queue and router preserved")
