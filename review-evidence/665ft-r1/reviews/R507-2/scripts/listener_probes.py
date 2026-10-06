#!/usr/bin/env python3
"""Rerun the public skipped/setup/crash tally regressions through the full self-test."""
import contextlib
import io
import os
from pathlib import Path
import sys

root, packet = map(lambda p: Path(p).resolve(),sys.argv[1:3])
work=packet/'scratch/listener-probes'
work.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(packet/'scratch')
sys.path.insert(0,str(root/'sw/firmware/gtest'))
import fw_gtest
import tally_selftest as tally

source=fw_gtest.MAIN_SOURCE.read_text()
original_build=tally.build
for name,old,new in [
    ('skip', 'if (info.result()->Failed() || info.result()->Skipped()) {', 'if (info.result()->Failed()) {'),
    ('setup', 'suite->name());\n                failures++;', 'suite->name());'),
    ('crash', '        put_tally(state.checks + 1u, state.failures + 1u);',
              '        put_tally(state.checks + 1u, state.failures);'),
]:
    assert source.count(old)==1
    altered=work/f'{name}.cpp'
    altered.write_text(source.replace(old,new))
    tally.build=lambda out,b=None,main_source=altered: original_build(out,b,main_source)
    sys.argv=['tally_selftest.py']
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        rc=tally.main()
    log=output.getvalue()
    (packet/f'receipts/listener-{name}.log').write_text(log)
    (packet/f'receipts/listener-{name}.rc').write_text(str(rc)+'\n')
    print(f'{name}: self-test rc={rc}; expected 1')
    for line in log.splitlines():
        if '[FAIL]' in line or 'want checks' in line or 'RESULT lines' in line:
            print(line)
    assert rc==1 and 'want checks' in log, 'must fail on the tally itself'
tally.build=original_build
print('three prior listener regressions now rejected by their own tally lines: PASS')
