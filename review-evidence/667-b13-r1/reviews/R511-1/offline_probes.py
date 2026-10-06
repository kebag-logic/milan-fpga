#!/usr/bin/env python3
"""Run published adverse controls and independent synthetic capture probes.

Usage: python3 offline_probes.py PACKET_DIRECTORY
The only adaptation is relocating the published controls' temporary directory.
All inputs, generated captures and imports stay beneath packet/scratch/.
"""
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys

packet=Path(sys.argv[1]).resolve()
source=packet/'scratch/public/author'
work=packet/'scratch/controls'
work.mkdir(parents=True,exist_ok=True)
for name in ['check_receipts.py','run_b13.py','compare_restore.py','decode_capture.py','restore-start.jsonl']:
    shutil.copyfile(source/name,work/name)
(work/'scratch').mkdir(exist_ok=True)
s=(work/'check_receipts.py').read_text()
assert s.count("dir='/tmp'")==1
(work/'check_receipts.py').write_text(s.replace("dir='/tmp'","dir=str(p/'scratch')"))
print('Published controls: temporary directory relocated; all assertions unchanged.',flush=True)
subprocess.run([sys.executable,'-B',str(work/'check_receipts.py'),str(work)],check=True)
spec=importlib.util.spec_from_file_location('decoder',work/'decode_capture.py')
decoder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(decoder)

def pcap(path,tagged,stamps):
    data=bytearray(bytes.fromhex('d4c3b2a1')+struct.pack('<HHIIII',2,4,0,0,65535,1))
    for i,timestamp in enumerate(stamps):
        prefix=bytearray(28)
        tap=0x12345678abcdef00+125000*i
        prefix[8:20]=struct.pack('<III',3,tap>>32,tap&0xffffffff)
        ethernet=bytes(12)+(bytes.fromhex('8100000222f0') if tagged else bytes.fromhex('22f0'))
        aaf=bytearray(24)
        aaf[0]=2;aaf[1]=0x81;aaf[2]=(254+i)%256
        aaf[12:16]=timestamp.to_bytes(4,'big')
        frame=prefix+ethernet+aaf
        data+=struct.pack('<IIII',0,i,len(frame),len(frame))+frame
    path.write_bytes(data)

for tagged in (False,True):
    file=work/('tagged.pcap' if tagged else 'plain.pcap')
    stamps=[(0xffff0000+125000*i)&0xffffffff for i in range(20)]
    pcap(file,tagged,stamps)
    records=list(decoder.records(file))
    assert records[0][1]==0x12345678abcdef00 and records[0][2]==3
    s=decoder.analyze([file])['streams'][0]
    assert s['gaps']==0 and s['first_step_ns']==125000 and s['steady_period_ns']==125000
    assert [x['sequence'] for x in s['first']]==[(254+i)%256 for i in range(10)]
    assert [x['avtp_timestamp'] for x in s['first']]==stamps[:10]
    stamps[0]=(stamps[1]+400000000)&0xffffffff
    pcap(file,tagged,stamps)
    s=decoder.analyze([file])['streams'][0]
    assert s['first_step_ns']==-400000000 and s['first_offset_from_steady_ns']==400125000
    truncated=work/'truncated.pcap';truncated.write_bytes(file.read_bytes()[:-1])
    try:
        list(decoder.records(truncated))
    except ValueError:
        pass
    else:
        raise AssertionError('truncated packet accepted')
    print('PASS synthetic', 'tagged' if tagged else 'plain',': tap-word order, sequence and timestamp wrap, negative startup jump, packet truncation.')
print('PASS offline controls and independent synthetic capture probes.')
