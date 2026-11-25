#!/usr/bin/env python3
"""Test the physical buffer boundary and a disposable one-byte overread control."""
import os
from pathlib import Path
import resource
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
work = out / 'scratch' / 'boundary'
work.mkdir(exist_ok=True)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
pin = env.get('REVIEW_TEST_PREFIX', '$VALIDATION_TOOLS/gtest-1.14.0')
env.update(PKG_CONFIG_PATH=pin + '/lib/pkgconfig', LD_LIBRARY_PATH=pin + '/lib')
flags = subprocess.check_output(['pkg-config', '--cflags', '--libs', 'gtest', 'gmock'], env=env, text=True).split()
source = (root / 'src/adp.c').read_text()
anchor = '\tuint64_t target = wire_be64(frame + ADP_HEADER_BYTES + 4u);'
plant = '\tif ((wire_be16(frame + 16u) & 0x07FFu) > 56u) {\n\t\tvolatile uint8_t surplus = frame[82];\n\t\t(void)surplus;\n\t}\n'
assert source.count(anchor) == 1
(work / 'overread.c').write_text(source.replace(anchor, plant + anchor))
(out / 'overread-control.diff').write_text('Insert before target decode in src/adp.c:\n' + plant)
def run(name, cmd, expected=0):
    with (out / (name + '.log')).open('w') as log:
        log.write('COMMAND ' + ' '.join(cmd) + '\n')
        log.flush()
        rc = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=120).returncode
        log.write('RETURN ' + str(rc) + '\n')
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
    assert rc == expected if expected is not None else rc != 0
common = ['-g', '-O0', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
run('boundary-tests-build', ['clang++', '-std=c++20', *common, '-I' + str(root/'tests'), '-I' + str(root/'include'), '-I' + pin + '/include', '-c', str(out/'boundary_probe.cpp'), '-o', str(work/'tests.o')])
run('boundary-main-build', ['clang++', '-std=c++20', *common, '-I' + pin + '/include', '-c', str(root/'tests/main.cpp'), '-o', str(work/'main.o')])
for name, path in [('head', root/'src/adp.c'), ('overread', work/'overread.c')]:
    run(name + '-core-build', ['clang', '-std=c11', *common, '-DNDEBUG', '-I' + str(root/'include'), '-c', str(path), '-o', str(work/(name + '.o'))])
    run(name + '-link', ['clang++', *common, str(work/(name+'.o')), str(work/'tests.o'), str(work/'main.o'), *flags, '-o', str(work/name)])
run('physical-boundary', [str(work/'head'), '--gtest_filter=IndependentBoundary.*'])
run('overread-existing-suite', [str(work/'overread'), '--gtest_filter=-IndependentBoundary.*'])
run('overread-physical-boundary', [str(work/'overread'), '--gtest_filter=IndependentBoundary.*'], expected=None)
