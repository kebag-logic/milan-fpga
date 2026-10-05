"""Independent bounded controls using public receipts; no device operations.
Usage: python3 -B offline_probes.py PUBLIC_PACKET SCRATCH_DIRECTORY
"""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys

packet, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('wire', packet/'wire.py')
wire = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wire)
case = json.loads((packet/'wire-receipts-00.json').read_text())[0]
cmd,rsp,unlock = [bytes.fromhex(case[k]['raw']) for k in ('command','response','unlock')]
zero = bytearray(unlock)
zero[36:40] = bytes(4)
base = [bytes(zero), cmd, rsp, unlock]
checks=[]
def wire_case(name, order, expected, edit=None):
    frames = [bytearray(base[i]) for i in order]
    if edit: edit(frames)
    data = bytearray(struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1))
    for i, a in enumerate(frames):
        frame = bytes(12) + b'\x22\xf0' + a
        data.extend(struct.pack('<4I',10,i*100,len(frame),len(frame)))
        data.extend(frame)
    p=scratch/(name+'.pcap');p.write_bytes(data)
    w=wire.analyze([(p,False)],cmd[28:36].hex(),int.from_bytes(cmd[38:40],'big'),cmd[12:20].hex())['wire']
    actual=w['order'] if w else 'NO_MATCH'
    assert actual==expected,(name,actual)
    checks.append(dict(case=name,result=actual))

wire_case('response-first',[0,1,2,3],'RESPONSE_FIRST')
wire_case('reversed',[0,1,3,2],'COUNTERS_FIRST')
wire_case('missing-unlock',[0,1,2],'NO_UNLOCK_PUSH')
wire_case('prior-unlock',[0,3,1,2],'NO_UNLOCK_PUSH')
def flip(frames,frame,byte): frames[frame][byte]^=1
wire_case('wrong-controller',[0,1,2,3],'NO_UNLOCK_PUSH',lambda f:flip(f,3,19))
wire_case('wrong-input',[0,1,2,3],'NO_UNLOCK_PUSH',lambda f:flip(f,3,27))
wire_case('wrong-sequence',[0,1,2,3],'NO_MATCH',lambda f:flip(f,2,49))
wire_case('solicited-baseline',[0,1,2,3],'RESPONSE_FIRST',lambda f:f[0].__setitem__(22,f[0][22]&0x7f))

# Exercise the published startup test as a real failing process, without
# changing the published evidence or checkout.
mut=scratch/'startup';mut.mkdir(exist_ok=True)
for name in ['startup_decode.py','check_startup.py','startup-analysis.json','short-polls.csv']:
    shutil.copyfile(packet/name,mut/name)
for f in packet.glob('wire-receipts-*.json'):shutil.copyfile(f,mut/f.name)
original=json.loads((packet/'startup-headers.json').read_text())
for name,byte,mask in [('tv',1,1),('tu',3,1),('mr',1,8),('sp',22,16),('timestamp',12,1)]:
    doc=copy.deepcopy(original)
    h=bytearray.fromhex(doc['cycles'][0]['first_twelve_pdus'][0]['avtp_header']);h[byte]^=mask
    doc['cycles'][0]['first_twelve_pdus'][0]['avtp_header']=h.hex()
    (mut/'startup-headers.json').write_text(json.dumps(doc))
    r=subprocess.run([sys.executable,'-B',str(mut/'check_startup.py'),str(mut)],capture_output=True,timeout=15)
    assert r.returncode==1 and b'AssertionError' in r.stderr
    checks.append(dict(case='startup-'+name,rc=r.returncode,rejected=True))

source=(packet/'rule_controls.cpp').read_text()
for name,text,expected in [('normal',source,0),('inverted',source.replace('selected=(conn=="Connected")','selected=(conn!="Connected")'),1)]:
    p=scratch/('rule-'+name+'.cpp');p.write_text(text)
    binary=scratch/('rule-'+name)
    r=subprocess.run(['c++','-std=c++17','-O2','-pthread',str(p),'-o',str(binary)],capture_output=True,timeout=60)
    assert r.returncode==0,r.stderr.decode()
    r=subprocess.run([str(binary)],capture_output=True,timeout=15)
    assert r.returncode==expected
    checks.append(dict(case='rule-'+name,rc=r.returncode,stdout=r.stdout.decode().strip()))
print(json.dumps(dict(passed=True,checks=checks),indent=2))
