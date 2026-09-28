"""Verify every stored native byte and replay capture oracles without simulation."""
from pathlib import Path
import gzip
import hashlib
import json
import re
import sys

out=Path(__file__).parent
root=Path('$LANES/590-592-599-firmware')
sys.path.insert(0,str(root/'tb/verilator/nvm_capture_cpu'))
import run

artifacts=json.loads((out/'native-artifacts.json').read_text())
raw_by_name={}
for item in artifacts:
    parts=[]
    for stored in item['stored']:
        path=out/stored['path'];raw=path.read_bytes()
        assert len(raw)==stored['size'] and hashlib.sha256(raw).hexdigest()==stored['sha256'],path
        assert len(raw)<=200000,path
        parts.append(raw)
    body=b''.join(parts)
    name=item['name']
    if name.endswith('.gz'):
        body=gzip.decompress(body);name=name[:-3]
    assert len(body)==item['raw_size'] and hashlib.sha256(body).hexdigest()==item['raw_sha256'],name
    assert name not in raw_by_name,name
    raw_by_name[name]=body

capture_count=0
committed=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
for short,mhz in [('1x1',50),('8x8',50),('8x8',100)]:
    for traffic in ('on','off'):
        name=f'capture-{short}-{mhz}-{traffic}'
        spec=json.loads(raw_by_name[name+'-sources.json'])
        raw=raw_by_name[name+'-raw.log'].decode()
        rows=[dict((key,int(value)) for key,value in re.findall(r'(\w+)=(\d+)',line))
              for line in raw.splitlines() if line.startswith('CAPTURE index=')]
        measured=run.grade_rows(rows,spec)
        assert measured==json.loads(raw_by_name[name+'.json']),name
        matches=[entry for entry in committed['measurements']
                 if (entry['shape'],entry['cpu_hz'],entry['traffic'])
                 == (measured['shape'],measured['cpu_hz'],measured['traffic'])]
        assert len(matches)==1,name
        assert all(matches[0][key]==value for key,value in measured.items()),name
        assert 'CAPTURE_DONE' in raw
        capture_count+=len(rows)
byte=json.loads(raw_by_name['capture-byte-only-measurement.json'])
base=json.loads(raw_by_name['capture-8x8-50-on.json'])
spec=json.loads(raw_by_name['capture-byte-only-sources.json'])
raw=raw_by_name['capture-byte-only-capture.log'].decode()
rows=[dict((key,int(value)) for key,value in re.findall(r'(\w+)=(\d+)',line))
      for line in raw.splitlines() if line.startswith('CAPTURE index=')]
measured=run.grade_rows(rows,spec)
run.grade_byte_only(measured,base)
assert all(byte[key]==value for key,value in measured.items())
assert byte['baseline_sha256']==hashlib.sha256(raw_by_name['capture-8x8-50-on.json']).hexdigest()
assert byte['minimum_slowdown']==byte['minimum_ms']/base['maximum_ms']
for path in out.rglob('*'):
    if path.is_file():
        assert path.stat().st_size<=200000,path
print(f'PASS: {len(artifacts)} retained native artifacts; {capture_count} captures; byte-only control')
