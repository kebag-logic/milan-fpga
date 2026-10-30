#!/usr/bin/env python3
"""Record source identities, documented constants and generated-image equality."""
import hashlib,importlib.util,json,os,pathlib,re,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"]="1";sys.dont_write_bytecode=True
head="8607347675743fe8d1ccaa370c63905c5ca1ccd5"
def git(*args):return subprocess.check_output(["git",*args],cwd=root)
spec=importlib.util.spec_from_file_location("generator",root/"hdl/ucode/gen_gptp_ucode.py");g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
log=[]
for name,value in re.findall(r"^\| `([A-Z][A-Z0-9_]*)` \| ([0-9,]+) \|",(root/"docs/INTEGRATION.md").read_text(),re.M):
 actual=getattr(g,name);assert int(value.replace(",",""))==actual
 log.append(f"CONSTANT {name} docs={value} source={actual} MATCH")
images={"syn/ooc/work/gptp_ucode.hex":[],"tb/verilator/ucpu/gptp_ucode.hex":[],"tb/verilator/engine/gptp_ucode.hex":["--clk-hz","2000000","--cease-ms","3000"],"tb/tsngen/gptp_ucode.hex":["--clk-hz","2000000"]}
for rel,args in images.items():
 target=out/"scratch"/(rel.replace("/","_")+".hex")
 p=subprocess.run([sys.executable,str(root/"hdl/ucode/gen_gptp_ucode.py"),*args,"-o",str(target)],capture_output=True,text=True,check=True)
 log.append("GENERATE "+rel+" "+p.stdout.replace(str(target),"generated-image").strip())
 equal=target.read_bytes()==(root/rel).read_bytes();log.append(f"IMAGE {rel} byte_equal={equal} sha256={hashlib.sha256(target.read_bytes()).hexdigest()}");assert equal
for kind,args in [("request-seeded",["--seq-seed","0x200000"]),("sync-seeded",["--sync-seq-seed","0x10000"]),("documented-cli",["--mac","0x02A1B2C3D4E5","--p1","248","--clk-hz","100000000"])]:
 target=out/"scratch"/(kind+".hex")
 p=subprocess.run([sys.executable,str(root/"hdl/ucode/gen_gptp_ucode.py"),*args,"-o",str(target)],capture_output=True,text=True,check=True)
 log.append(kind+" "+p.stdout.replace(str(target),"generated-image").strip())
log.append("HEAD "+git("rev-parse","HEAD").decode().strip());log.append("TREE "+git("rev-parse","HEAD^{tree}").decode().strip())
entries=git("ls-tree","-rz",head).split(b"\0");count=0;gitlinks=[]
for entry in entries:
 if not entry:continue
 meta,path=entry.split(b"\t",1);mode,typ,oid=meta.decode().split();p=root/os.fsdecode(path)
 if mode=="160000":gitlinks.append((os.fsdecode(path),oid));continue
 data=os.readlink(p).encode() if mode=="120000" else p.read_bytes()
 blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert blob==oid,os.fsdecode(path)
 if mode in ("100644","100755"):assert bool(p.stat().st_mode&0o111)==(mode=="100755"),str(p)
 count+=1
assert git("diff","--cached","--name-only",head)==b""
assert git("diff","--name-only",head)==b""
log.append(f"All {count} tracked blobs and executable modes match HEAD; index matches HEAD; gitlinks={gitlinks}")
log.append("Changed paths:\n"+git("diff","--name-status","135afd04",head).decode())
log.append("Whitespace check rc="+str(subprocess.run(["git","diff","--check","135afd04",head],cwd=root,capture_output=True).returncode))
(out/"source-audit.log").write_text("\n".join(log)+"\n")
print("\n".join(log))
