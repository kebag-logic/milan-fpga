"""Freeze focused CPU receipts and normalize host paths. Arguments: packet checkout."""
import gzip,hashlib,json,re,shutil,sys
from pathlib import Path
packet,checkout=map(lambda s:Path(s).resolve(),sys.argv[1:3])
scratch=packet/"scratch";build=scratch/"cpu-build";cpu=packet/"cpu";cpu.mkdir(exist_ok=True)
raw=scratch/"raw-review-receipts";raw.mkdir(exist_ok=True)
records=[]
def digest(b):return hashlib.sha256(b).hexdigest()
def normalize(text):
 for a,b in ((str(scratch/"cpu"),"$CHECKOUT"),(str(scratch/"base"),"$BASE_CHECKOUT"),(str(checkout),"$CHECKOUT"),(str(packet),"$PACKET")):
  text=text.replace(a + chr(47),b + chr(47))
 text=re.sub(r"/home/[^/\s]+/", "$WORKSPACE_HOME/", text)
 text=text.replace("$VALIDATION_TOOLS/","$VALIDATION_TOOLS/")
 return text
for name in ("cpu.log","host.log","base-host.log","notice-fault.log"):
 path=packet/name;data=(raw/name).read_bytes() if (raw/name).exists() else path.read_bytes();(raw/name).write_bytes(data)
 public=normalize(data.decode()).encode();path.write_bytes(public)
 records.append(dict(file=name,original_sha256=digest(data),published_sha256=digest(public),path_normalized=data!=public))
for path in sorted((build/"results").glob("notice-burst-*")):
 if path.suffix==".log":
  data=path.read_bytes();published=gzip.compress(data,mtime=0);target=cpu/(path.name+".gz")
  target.write_bytes(published)
  records.append(dict(file=str(target.relative_to(packet)),raw_sha256=digest(data),published_sha256=digest(published),compression="gzip",path_normalized=False))
 elif path.suffix in (".json",".txt"):
  shutil.copy2(path,cpu/path.name)
path=build/"build.json";data=path.read_bytes();public=normalize(data.decode()).encode();(cpu/"build.json").write_bytes(public)
records.append(dict(file="cpu/build.json",original_sha256=digest(data),published_sha256=digest(public),path_normalized=True))
(packet/"receipt-provenance.json").write_text(json.dumps(records,indent=2)+"\n")
print("Packaged",len(list(cpu.iterdir())),"CPU receipts; normalized paths only in four logs and build metadata")
