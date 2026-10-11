#!/usr/bin/env python3
"""Check every pinned parent citation against downloaded exact parent blobs."""
import argparse
import re
import subprocess
from pathlib import Path

PIN='ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('repo',type=Path)
    ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
    a=ap.parse_args()
    files=['README.md','docs/MANAGER.md','docs/INTEGRATION.md','docs/SOURCE_EVIDENCE.md','docs/history/v1/PROJECT_STATUS.md']
    pattern=re.compile(r'https://github.com/kebag-logic/milan-fpga/blob/([0-9a-f]+)/([^#)\s]+)#L(\d+)(?:-L(\d+))?')
    total=0;unique=set()
    for name in files:
        text=(a.repo/name).read_text()
        for pin,path,first,last in pattern.findall(text):
            assert pin==PIN,(name,pin)
            lines=(a.packet/'authority'/path).read_text().splitlines()
            start,end=int(first),int(last or first)
            assert 1<=start<=end<=len(lines),(name,path,start,end)
            total+=1
            key=(path,start,end)
            if key not in unique:
                print(f'{path}:{start}-{end}: '+' / '.join(lines[start-1:end]))
                unique.add(key)
    print(f'PASS: {total} citation occurrences, {len(unique)} unique targets, all pinned to {PIN}')
    assert (total,len(unique))==(31,14)
    current=[a.repo/'README.md']+list((a.repo/'docs').glob('*.md'))
    bad=[]
    for f in current:
        for n,line in enumerate(f.read_text().splitlines(),1):
            if re.search(r'default[- ]off|defaults?\s+off',line,re.I):
                bad.append(f'{f.relative_to(a.repo)}:{n}: {line}')
    assert not bad,bad
    print('PASS: no current root/guide Markdown states default-off')
    for name in ['README.md','docs/MANAGER.md']:
        now=(a.repo/name).read_text()
        assert 'issues/35)' not in now
        for required in ['issues/58)','issues/117)','issues/64)','issues/488)']:
            assert required in now,(name,required)
    print('PASS: both conflict pages retain #58, #117, #64, #488 and omit fixed #35 risk entries')
    header=(a.repo/'hdl/wire/KL_gptp_rx_parser.sv').read_text()
    integration=(a.repo/'docs/INTEGRATION.md').read_text()
    for term in ['rx_valid_i high','exactly one','no event','including it','next accepted frame']:
        assert term in header,term
    for term in ['exactly one drop','no event','flagged byte\'s own edge','undefined','only its own frame','between valid bytes are ignored']:
        assert term in integration,term
    base=subprocess.check_output(['git','-C',str(a.repo),'show','5dce647a:tb/verilator/parser/sim_main.cpp'],text=True)
    start=base.index('void RxParserHarness::feed_gap(')
    end=base.index('// reset',start)
    assert 'dut->rx_err_i   = 0;' in base[start:end]
    print('PASS: feed_gap explicitly drove rx_err_i low already at the source base')

if __name__=='__main__':
    main()
