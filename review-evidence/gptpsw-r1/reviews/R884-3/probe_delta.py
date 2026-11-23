#!/usr/bin/env python3
"""Independent cause controls, all mutations confined to packet scratch."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
source = (root/'sw/firmware/ctrl/gptp/gptp.c').read_text()
old = subprocess.check_output(['git','show','8167b70d:sw/firmware/ctrl/gptp/gptp.c'],cwd=root,text=True)
cases = {
    'old-port': (old, '*'),
    'without-local-clock': (source.replace('return phc_ns - p->local_off;', 'return phc_ns;'), 'Net.*Step*'),
    'without-immediate-clear': (source.replace('p->pd.multi = true;\n\tp->pd.good = 0;\n\tas_capable_set(p, false);',
                                             'p->pd.multi = true;'),
                              'Scripted.*Response*:Scripted.OneClockAnsweringTwice*'),
}
def run(case):
    name, (src, filt) = case
    work = out/'scratch'/name
    work.mkdir(exist_ok=True)
    (work/'gptp.c').write_text(src)
    flags = ['-fsanitize=undefined','-fno-sanitize-recover=undefined']
    commands = [
        ['gcc','-std=c11','-O2',*flags,'-I'+str(root/'sw/firmware/ctrl/gptp'),'-c',str(work/'gptp.c'),'-o',str(work/'core.o')],
        ['g++','-std=c++20','-O1',*flags,'-I'+str(root/'sw/firmware/ctrl/gptp'),'-I'+str(root/'sw/firmware/gtest'),
         str(root/'sw/firmware/ctrl/test/test_gptp.cpp'),str(work/'core.o'),'-lgtest_main','-lgtest','-lpthread','-o',str(work/'probe')],
    ]
    with (out/(name+'-build.log')).open('w') as log:
        for cmd in commands:
            subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
    result = subprocess.run([str(work/'probe'),'--gtest_filter='+filt],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/(name+'.log')).write_text(result.stdout)
    (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
    assert result.returncode == 1 and '[  FAILED  ]' in result.stdout and 'runtime error:' not in result.stdout
    return name + ': rejected by test assertion, rc=1'
with ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(run,cases.items()):
        print(result)
