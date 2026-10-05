"""Check public packet text and structured protocol identity fields.
Usage: python3 -B packet_privacy.py CHECKOUT PUBLIC_PACKET
Print locations and counts, never identifying values.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

repo, packet = map(Path,sys.argv[1:])
sys.path.insert(0,str(repo/'scripts'))
from docs_check import SCRUB_RULES

files=[p for p in packet.iterdir() if p.is_file()]
files += [repo/'docs/findings/653_DISCONNECT_ORDER_BENCH.md']
hits=[]
for p in files:
    text=p.read_text()
    for regex,category,_ in SCRUB_RULES:
        if regex.search(text):hits.append(dict(file=p.name,category=category))
assert not hits,hits
dut=bytes.fromhex('020000fffe000001')
peer=(3).to_bytes(8,'big')
controller=(1).to_bytes(8,'big')
checked=0
for p in packet.glob('wire-receipts-*.json'):
    for row in json.loads(p.read_text()):
        for kind in ('command','response','unlock'):
            b=bytes.fromhex(row[kind]['raw'])
            assert b[12:20]==controller
            if b[0]==0xfc:
                assert b[20:28] in (dut,peer,bytes(8))
                assert b[28:36] in (dut,peer)
                assert b[4:10] in (bytes(6),bytes.fromhex('020000000001'),bytes.fromhex('000000000003'))
            else:assert b[4:12] in (dut,peer)
            checked+=1
for case in json.loads((packet/'startup-headers.json').read_text())['cycles']:
    for row in case['first_twelve_pdus']:
        assert bytes.fromhex(row['avtp_header'])[4:12]==bytes(8)
pattern=r'static std::string errorUpdate\(.*?\n\}'
functions=[re.search(pattern,(packet/f).read_text(),re.S).group() for f in ['probe.cpp','probe_phase.cpp','rule_controls.cpp']]
assert len(set(functions))==1
print(json.dumps(dict(passed=True,files_scanned=len(files),text_findings=hits,structured_headers=checked,peer_and_controller_fields_neutral=True,startup_stream_ids_zero=True,rule_function_equal_in_both_probes_and_controls=True,rule_function_sha256=hashlib.sha256(functions[0].encode()).hexdigest(),limit='Original peer descriptor names, serial and interface records are not public replay inputs. The operator eight-category audit is retained provenance, not independently rerun here.'),indent=2))
