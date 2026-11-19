import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
head="a16899b1fb2a0c731ebf18476d1a38627254ea4e"
required=("gptp-processor","protocol-processor","third_party/verilog-axis","third_party/tsn-c-stack","third_party/lwSRP")
def git(where,*args):return subprocess.check_output(["git","-C",str(where),*args])
def verify(where,expected,label):
 actual=git(where,"rev-parse","HEAD").decode().strip();assert actual==expected,(label,actual)
 tree=git(where,"rev-parse","HEAD^{tree}").decode().strip()
 assert git(where,"write-tree").decode().strip()==tree,label+" index"
 entries=git(where,"ls-tree","-rz","HEAD").split(b"\0")
 count=0;links={}
 for entry in entries:
  if not entry:continue
  info,name=entry.split(b"\t",1);mode,kind,oid=info.decode().split();p=where/os.fsdecode(name)
  if kind=="commit":links[os.fsdecode(name)]=oid;continue
  m=p.lstat().st_mode
  if mode=="120000":assert stat.S_ISLNK(m);data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(m),(label,name,"not regular")
   assert bool(m&stat.S_IXUSR)==(mode=="100755"),(label,name,"mode")
   data=p.read_bytes()
  actual_blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual_blob==oid,(label,name,"bytes")
  count+=1
 print(label,expected,"tree",tree,"PASS",count,"tracked blobs and modes; index matches HEAD")
 return links
links=verify(root,head,"parent")
for name in required:verify(root/name,links[name],name)
for name,oid in sorted(links.items()):print("gitlink",name,oid)
assert not git(root,"status","--porcelain").strip(),"dirty parent"
print("Parent status clean; required initialized submodules match their gitlinks, index, tracked bytes and modes.")
print("Round-two changed paths:")
print(git(root,"diff","--name-status","502b041c..HEAD").decode(),end="")
print("Firmware production, HDL, mailbox contract, pins and cost tables unchanged in round two:")
paths=["hdl","sw/mailbox","sw/firmware/ctrl/app","sw/firmware/ctrl/aecp","sw/firmware/ctrl/loop","tb/verilator/ctrl_service_budget/rows_tiers.py","tb/verilator/ctrl_service_budget/edit_rows.py","tb/verilator/ctrl_service_budget/load_grade.py",*required]
assert not git(root,"diff","502b041c..HEAD","--",*paths).strip()
print("PASS")
