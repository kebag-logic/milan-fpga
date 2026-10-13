#!/usr/bin/env python3
"""Build disposable tests against unchanged candidate firmware."""
import argparse
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
args = p.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_reuse
import fw_gtest
out = packet/'scratch/owner-probe'
out.mkdir(parents=True,exist_ok=True)
ctrl_reuse.cut_reuse(out/'reuse')
b.stack_pin()
tree = b.Tree(b.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=4))
original=(b.HERE/'test_acmp_mbx.cpp').read_text()
extra=(packet/'probe_owner.cpp').read_text()
source=out/'test_owner.cpp'
source.write_text(original+'\nnamespace {\n'+extra+'\n}\n')
objs=b.firmware(tree,b.PORTABLE,'fw')
objs+=fw_gtest.compile_tests(tree.build,[*b.includes(tree),f'-I{b.STACK_TESTS}',f'-I{tree.reuse}'],[source],out/'test')
exe=b.link(tree,'probe_owner',objs+[b.label(tree,'R583 source-owner contract')])
result=subprocess.run([str(exe),'--gtest_filter=AcmpMailbox.R583SourceOwnerInvalidityClosesThePublishedGate'],capture_output=True,text=True)
(packet/'owner-probe.log').write_text(result.stdout+result.stderr)
(packet/'owner-probe.rc').write_text(str(result.returncode)+'\n')
print(result.stdout,flush=True)
# Header-derived access counts are independently compiled for both interfaces.
for interface in [1,2]:
    gen=out/f'if{interface}'
    subprocess.run([sys.executable,str(repo/'sw/mailbox/gen_mailbox.py'),'--variant-interfaces',str(interface),'--out',str(gen)],check=True,capture_output=True)
    count=gen/'counts.c'
    count.write_text('#include <stdio.h>\n#include "ctrl_app.h"\nint main(void) { printf("IF=%u ACMP=%u MAAP=%u SRP=%u THREE=%u FOUR=%u\\n", MBX_N_IF, ACMP_MBX_PASS_MAX, MAAP_MBX_PASS_MAX, SRP_MBX_PASS_MAX, CTRL_APP_THREE_PASS_MAX, CTRL_APP_PASS_MAX); return 0; }\n')
    binary=gen/'counts'
    subprocess.run(['gcc',*b.includes(tree),'-include',str(gen/'mbx_contract.h'),str(count),'-o',str(binary)],check=True)
    text=subprocess.check_output([str(binary)],text=True)
    (packet/f'bounds-if{interface}.log').write_text(text)
    print(text,end='')
# The probe intentionally fails when the reviewed defect exists.
sys.exit(0 if result.returncode==1 and 'core predicate=0 DA_GATE=1' in result.stdout else 1)
