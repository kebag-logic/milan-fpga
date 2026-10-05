#!/usr/bin/env python3
"""Run bounded receipt-reader and counter-rule controls without bench access.

Usage: python3 offline_controls.py EVIDENCE_ROOT SCRATCH_DIRECTORY
All generated data and executables remain in SCRATCH_DIRECTORY.
"""
import importlib.util
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

root, scratch = map(Path, sys.argv[1:])
src = root / 'author'
scratch.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('receipt_reader',src/'wire.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
rows = [r for f in src.glob('wire-receipts-*.json') for r in json.loads(f.read_text())]
sample = next(r for r in rows if r['cycle'] == 'A0300-1')
raw = {k:bytearray(bytes.fromhex(sample[k]['raw'].replace('<controller-host-id>','000000000000')))
       for k in ('command','response','unlock')}
raw['baseline'] = raw['unlock'].copy()
raw['baseline'][36:40] = bytes(4)
ctl = raw['command'][12:20].hex()
listener = raw['command'][28:36].hex()
idx = int.from_bytes(raw['command'][38:40],'big')


def capture(name, names, mutation=None):
    frames = [bytearray(raw[n]) for n in names]
    if mutation: mutation(frames)
    blob = struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1)
    for n, frame in enumerate(frames):
        ns = (7 << 32) + 0xfffffe00 + n*1000
        tap = bytearray(28)
        struct.pack_into('<III',tap,8,2,ns >> 32,ns & 0xffffffff)
        eth = bytes(12)+bytes.fromhex('22f0')
        packet = tap+eth+frame
        blob += struct.pack('<IIII',1,n,len(packet),len(packet))+packet
    path = scratch/(name+'.pcap');path.write_bytes(blob)
    return path


def check(name,names,expected,mutation=None):
    path=capture(name,names,mutation)
    result=reader.analyze([(path,True)],listener,idx,ctl)['wire']
    actual=result['order'] if result else 'NO_MATCH'
    assert actual==expected,(name,expected,actual)
    if result and result['unlock']:
        assert result['response_unlock_us'] == (1 if expected=='RESPONSE_FIRST' else -1)
    print(name+': '+actual)


base=['baseline','command','response','unlock']
check('response-first',base,'RESPONSE_FIRST')
check('reversed-order',['baseline','command','unlock','response'],'COUNTERS_FIRST')
check('missing-push',base[:-1],'NO_UNLOCK_PUSH')
check('prior-unlock',['baseline','unlock','command','response'],'NO_UNLOCK_PUSH')


def flip(frames,frame,offset):
    frames[frame][offset] ^= 1


check('foreign-controller',base,'NO_UNLOCK_PUSH',lambda fs:flip(fs,-1,12))
check('foreign-input',base,'NO_UNLOCK_PUSH',lambda fs:flip(fs,-1,27))
check('foreign-response-sequence',base,'NO_MATCH',lambda fs:flip(fs,2,49))
def solicited(frames):
    frames[0][22] &= 0x7f


check('solicited-baseline',base,'RESPONSE_FIRST',solicited)
first=capture('clock-a',base[:-1]);second=capture('clock-b',['unlock'])
assert reader.analyze([(first,True),(second,True)],listener,idx,ctl)['wire']['order']=='NO_UNLOCK_PUSH'
print('separate-capture-clocks: NO_UNLOCK_PUSH')

# Prove the extracted function is identical to both published probe variants.
control=(src/'rule_controls.cpp').read_text()
pattern=r'static std::string errorUpdate\(.*?\n\}'
function=re.search(pattern,control,re.S).group()
for name in ('probe.cpp','probe_phase.cpp'):
    assert re.search(pattern,(src/name).read_text(),re.S).group()==function
print('counter function equality: both published probes')
for name,source,expected in [('counter-clean',control,0),
                            ('counter-inverted',control.replace('conn=="Connected"','conn!="Connected"'),1)]:
    source_file=scratch/(name+'.cpp');source_file.write_text(source)
    binary=scratch/name
    build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(source_file),'-o',str(binary)],
                         capture_output=True,text=True,timeout=120)
    assert build.returncode==0, 'counter control build failed'
    run=subprocess.run([str(binary)],capture_output=True,text=True,timeout=30)
    assert run.returncode==expected,(name,run.returncode)
    print(name+': rc '+str(run.returncode))
print('PASS: nine capture controls and eight counter-rule controls; inverted predicate rejected')
