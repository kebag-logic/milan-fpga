#!/usr/bin/env python3
"""Record source identities, case counts and unchanged production boundaries."""
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path.insert(0,str(root/'sw/firmware/nvm_hosttest'))
import read_fault_cases as c
def git(*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
fw = 'sw/firmware/milan_baremetal/milan_baremetal.c'
source = (root/fw).read_bytes()
assert source == git('show','0c276b62:'+fw)
assert source == git('show','bd42818d:'+fw)
print('Production firmware byte-identical to round 5 and measured commit')
print('Firmware sha256',hashlib.sha256(source).hexdigest())
paths = ['hdl','protocol-processor','gptp-processor','third_party/verilog-axis',
         'docs/reference/REGISTER_MAP.md','scripts/nvm_klj2.py']
assert not git('diff','--name-only','e8454e27','HEAD','--',*paths)
print('Source-base delta has no RTL, required gitlink, register-map or KLJ2 codec change')
cases = c.fault_cases(4096)
assert len(cases) == 3550
print('Generated cases',len(cases),'cold',sum(not x.restart for x in cases),
      'restart',sum(x.restart for x in cases))
counts=collections.Counter(c.term_of(x) for x in cases if c.term_of(x))
assert all(counts[t] == 32 for t,_,_ in c.COMPARISON)
print('Term classes',dict(counts))
assert not c.comparison_findings(source.decode(),cases)
assert not c.comparison_self_test(source.decode(),cases)
# Removing even one ruled combination must be detected, not just all of a class.
for term,_,_ in c.COMPARISON:
    one=next(x for x in cases if c.term_of(x)==term)
    got=c.comparison_findings(source.decode(),[x for x in cases if x!=one])
    assert any(f"the comparison's {term} has no fault class at 1 place(s)" in x for x in got)
    print('Single missing class combination refused:',term)
for bound in (12,13):
    assert set(c.windows(bound)) == {(0,64)} | {(start,n) for start in range(bound) for n in range(1,5)}
print('Full read-bound window sets intact')
writer=(packet/'receipts/writer.log').read_text()
for term,_,_ in c.COMPARISON:
    for shape in ('endstation_arty_4x4',*c.PRODUCT_SHAPES):
        assert any(c.control_of(term) in line and shape in line and c.alone_in(term) in line
                   for line in writer.splitlines())
print('All four removal controls rejected by own diagnostic on all three shapes')
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
assert receipt['product_firmware_sha256'] == hashlib.sha256(source).hexdigest()
assert git('rev-parse',receipt['base']+'^{tree}').decode().strip()==receipt['tree']
for name,digest in receipt['harness_sha256'].items():
    assert hashlib.sha256((root/'tb/verilator/nvm_capture_cpu'/name).read_bytes()).hexdigest()==digest
print('Capture receipt: firmware, measured tree and all harness input digests match')
print('Physical calibration NOT RUN; capture measurement not rerun')
print('PASS')
