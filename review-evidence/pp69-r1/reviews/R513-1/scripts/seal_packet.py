#!/usr/bin/env python3
"""Hash the publication set and verify all listed bytes; exclude scratch."""
import hashlib, pathlib, subprocess
packet=pathlib.Path(__file__).resolve().parents[1]
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R513] POSITIVE - exact head cb730a2f9dd7e4f60a03a38d4b47b569e68da8df'
assert report.splitlines()[-1]=='R513-1 FINISHED'
assert 'SKELETON' not in report
files=[packet/'REPORT.md']
files += [f for root in ['scripts','receipts'] for f in (packet/root).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
paths=sorted(set(files))
(packet/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(packet).as_posix()+'\n' for f in paths))
r=subprocess.run(['sha256sum','-c','MANIFEST.sha256'],cwd=packet,capture_output=True,text=True)
assert r.returncode==0,r.stdout+r.stderr
print(f'Publication manifest verified: {len(paths)} files; scratch excluded.')
print('Report first line:',report.splitlines()[0]); print('Report last line:',report.splitlines()[-1])
