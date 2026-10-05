"""Portable offline probes: python3 -B focused_probes.py PACKET SCRATCH.

Synthetic captures derive from published role-safe headers. No device access.
"""
import copy
import importlib.util
import json
import struct
import subprocess
import sys
from pathlib import Path

packet, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(packet))
from wire import analyze

rows = [r for f in sorted(packet.glob('wire-receipts-*.json')) for r in json.loads(f.read_text())]
case = next(r for r in rows if r['cycle']=='A0300-1')
command, response, unlock = [bytearray.fromhex(case[k]['raw']) for k in ('command','response','unlock')]
zero = unlock.copy(); zero[36:40] = bytes(4)
ctl, listener, idx = command[12:20].hex(),command[28:36].hex(),int.from_bytes(command[38:40],'big')

def capture(name, frames):
    data = struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1)
    for n, f in enumerate(frames):
        tap = bytearray(28)
        t = 10**10+n*1000
        struct.pack_into('<III',tap,8,3,t>>32,t&0xffffffff)
        eth = bytes(12)+bytes.fromhex('22f0')
        payload = tap+eth+f
        data += struct.pack('<4I',10,n,len(payload),len(payload))+payload
    path = scratch/(name+'.pcap');path.write_bytes(data)
    return analyze([(path,True)],listener,idx,ctl)['wire']

wire_results = []
tests = [('response_first',[zero,command,response,unlock],'RESPONSE_FIRST'),('reversed',[zero,command,unlock,response],'COUNTERS_FIRST'),('missing_push',[zero,command,response],'NO_UNLOCK_PUSH'),('prior_unlock',[zero,unlock,command,response],'NO_UNLOCK_PUSH')]
for name, offset, target in [('foreign_controller',12,'unlock'),('foreign_input',27,'unlock'),('foreign_sequence',49,'response')]:
    fs = [x.copy() for x in (zero,command,response,unlock)]
    fs[3 if target=='unlock' else 2][offset] ^= 1
    tests.append((name,fs,'NO_UNLOCK_PUSH' if target=='unlock' else None))
solicited = zero.copy();solicited[22] &= 0x7f;solicited[12:20] = bytes.fromhex('0000000000000004')
tests.append(('solicited_auxiliary_baseline',[solicited,command,response,unlock],'RESPONSE_FIRST'))
for name,fs,expected in tests:
    result=capture(name,fs); actual=result['order'] if result else None
    assert actual==expected,(name,actual,expected)
    wire_results.append(dict(case=name,expected=expected,actual=actual,passed=True))
bad=response.copy();bad[2] = 8
r=capture('non_success_status',[zero,command,bad,unlock]);assert r['status']==1
wire_results.append(dict(case='non_success_status',actual=r['status'],expected=1,passed=True))

# Build the extracted rule and kill the inverse Connected predicate in a copy.
rule_results=[]
for tag, source in [('clean',(packet/'rule_controls.cpp').read_text()),('inverted',(packet/'rule_controls.cpp').read_text().replace('conn=="Connected"','conn!="Connected"'))]:
    cpp=scratch/(tag+'.cpp');cpp.write_text(source);exe=scratch/tag
    build=subprocess.run(['g++','-std=c++17','-O0','-pthread',str(cpp),'-o',str(exe)],capture_output=True,text=True,timeout=60)
    assert build.returncode==0,build.stderr
    run=subprocess.run([str(exe)],capture_output=True,text=True,timeout=10)
    assert run.returncode==(0 if tag=='clean' else 1)
    rule_results.append(dict(case=tag,compile_rc=build.returncode,run_rc=run.returncode,stdout=run.stdout))

start=json.loads((packet/'restore-start.json').read_text());end=json.loads((packet/'restore-end.json').read_text())
restore_results=[]
for tag in ['changed_mapping','matching_aem_failure','matching_binding_failure','boolean_status','wrong_endpoint','reordered_inventory']:
    a,b=copy.deepcopy(start),copy.deepcopy(end)
    if tag=='changed_mapping':
        r=next(r for r in b['observations'] if r['category']=='maps' and r['value']['mappings'])
        r['value']['mappings'][0][0]^=1
    elif tag=='matching_aem_failure':
        for d in (a,b):next(r for r in d['observations'] if r['category']=='clocks')['status']='NO_SUCH_DESCRIPTOR'
    elif tag=='matching_binding_failure':
        for d in (a,b):next(r for r in d['observations'] if r['category']=='bindings')['status']=1
    elif tag=='boolean_status':
        for d in (a,b):next(r for r in d['observations'] if r['category']=='bindings')['status']=False
    elif tag=='wrong_endpoint':b['endpoint']='start'
    else:b['observations'].reverse()
    ap,bp=scratch/(tag+'-start.json'),scratch/(tag+'-end.json')
    ap.write_text(json.dumps(a));bp.write_text(json.dumps(b))
    run=subprocess.run([sys.executable,'-B',str(packet/'restore_compare.py'),str(ap),str(bp)],capture_output=True,text=True,timeout=10)
    expected=0 if tag=='reordered_inventory' else 1
    assert run.returncode==expected and not run.stderr
    reply=json.loads(run.stdout);assert reply['pass_restore']==(expected==0)
    restore_results.append(dict(case=tag,rc=run.returncode,reason=reply.get('reason','equal successful inventory')))
print(json.dumps(dict(passed=True,wire=wire_results,rule=rule_results,restore=restore_results),indent=2))
