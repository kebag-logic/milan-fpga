"""Stage bench-owned files outside the lane, with read-only source references."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path('$LANES/645-ring-slip')
w=Path(__file__).resolve().parent
name=sys.argv[1] if len(sys.argv)>1 else 'bench-inputs'
out=w/name
assert not out.exists()
out.mkdir()
# This is a build directory, with no Git checkout or branch. Bench generators
# own their files here; design inputs remain the verified lane's exact bytes.
for entry_name in ['hdl','protocol-processor','gptp-processor','third_party','configs','sw','scripts','avdecc','tools','syn','docs','tests']:
    (out/entry_name).symlink_to(root/entry_name,target_is_directory=True)
rows=[]
files=subprocess.check_output(['git','ls-files','-z','tb'],cwd=root).split(b'\0')
for entry in files:
    if not entry:continue
    rel=entry.decode();src=root/rel;dst=out/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes();dst.write_bytes(data);dst.chmod(src.stat().st_mode & 0o777)
    rows.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(w/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
print(len(rows),'tracked bench files staged')
