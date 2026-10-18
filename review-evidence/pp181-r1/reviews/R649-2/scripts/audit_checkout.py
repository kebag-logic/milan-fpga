#!/usr/bin/env python3
"""Verify source tree, index, modes and inherited merge content without modifying them."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*args):return subprocess.check_output(["git","-C",str(root),*args])
head=git("rev-parse","HEAD").decode().strip();tree=git("rev-parse","HEAD^{tree}").decode().strip()
assert head=="c5afc0a42f200af01dd83e67b579dc3badc42601"
assert tree=="90ca8e745ab0842df12e7a98b3f99e002c50bab6"
index={}
for row in git("ls-files","--stage","-z").split(b"\0"):
 if not row:continue
 meta,path=row.split(b"\t",1);mode,sha,stage=meta.decode().split();assert stage=="0";index[os.fsdecode(path)]=(mode,sha)
blobs=0;gitlinks=[]
for row in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not row:continue
 meta,path=row.split(b"\t",1);mode,typ,sha=meta.decode().split();name=os.fsdecode(path)
 assert index.pop(name)==(mode,sha),name
 if mode=="160000":gitlinks.append([name,sha]);continue
 f=root/name
 if mode=="120000":b=os.fsencode(os.readlink(f));assert f.is_symlink()
 else:
  b=f.read_bytes();actual="100755" if f.stat().st_mode & stat.S_IXUSR else "100644";assert actual==mode,name
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==sha,name
 blobs+=1
assert not index
status=git("status","--porcelain=v1").decode();assert not status,status
merged=git("merge-tree","--write-tree","42eb9aef","08ae0013").decode().strip()
assert merged==git("rev-parse","2cacc92^{tree}").decode().strip()
main_files=["hdl/aecp/KL_aecp_engine.sv","hdl/aecp/ucode/gen_ucode.py","hdl/aecp/ucode/aecp_commands.json","hdl/aecp/ucode/aecp_fields.json","tb/pp_top/sim_main.cpp","tb/aecp_cmds","scripts/check_aecp_commands.py"]
assert not git("diff","08ae0013","HEAD","--",*main_files)
assert not git("diff","08ae0013","HEAD","--","hdl/protocol_processor_top.sv","docs/architecture/07_memory_maps.md")
print(json.dumps({"head":head,"tree":tree,"tracked_blobs_bytes_modes_index_verified":blobs,"gitlinks":gitlinks,"status":status,"reconstructed_merge_tree":merged,"inherited_176_files_equal_main":main_files,"result":"PASS"},indent=2))
