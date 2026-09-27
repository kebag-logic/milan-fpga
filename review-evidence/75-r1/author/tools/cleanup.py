"""Remove only this run's temporary files and verify no capture process remains."""
import hashlib,json,subprocess,sys
from pathlib import Path
role=sys.argv[1]
if role=='controller':
 names=['/tmp/a386_avdecc_ro.py','/tmp/a386_controller.py','/tmp/a386_reconnect.py']
elif role=='capture':
 names=['/tmp/a386_capture.py']
else:raise SystemExit('unknown role')
for name in names:
 p=Path(name)
 if p.exists():
  b=p.read_bytes();print(p.name,len(b),hashlib.sha256(b).hexdigest());p.unlink()
# Process scan is read-only; do not touch unrelated work.
r=subprocess.run(['timeout','3s','ps','-eo','pid,args'],capture_output=True,text=True,timeout=4)
assert r.returncode==0
hits=[s for s in r.stdout.splitlines() if any(n in s for n in names) and 'ps -eo' not in s]
assert not hits,'run process remains'
print(role,'temporary scripts removed; no matching process remains')
