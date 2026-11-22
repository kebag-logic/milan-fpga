#!/usr/bin/env python3
"""Repeat G1-G4 for one source/one sink at the default one-interface mailbox."""
import concurrent.futures as cf,json,pathlib,subprocess,sys
parent=pathlib.Path(sys.argv[1]).resolve()
p=pathlib.Path(__file__).resolve().parent
sys.path[:0]=[str(parent/'sw/firmware/ctrl/test'),str(parent/'sw/firmware/gtest')]
import fw_gtest
from ctrl_build import Tree,PORTABLE,firmware,includes,link
from ctrl_reuse import cut_reuse
text=(parent/'sw/firmware/ctrl/test/test_adp.cpp').read_text()
for field in ('talker_stream_sources','listener_stream_sinks'):
    old='.'+field+' = 8u,'
    assert text.count(old)==1
    text=text.replace(old,'.'+field+' = 1u,')
source=p/'scratch/shape-one-test.cpp';source.write_text(text)
def run(side):
    work=p/'scratch'/('shape-one-'+side)
    stack=p/'scratch/base-stack' if side=='base' else parent/'third_party/tsn-c-stack'
    tree=Tree(parent/'sw/firmware/ctrl',work/'build',work/'reuse',fw_gtest.Build(jobs=4),stack)
    cut_reuse(tree.reuse)
    objs=firmware(tree,PORTABLE,'adp')+fw_gtest.compile_tests(tree.build,includes(tree),[source],work/'tests')
    exe=link(tree,'shape-one',objs)
    q=subprocess.run([str(exe),'--gtest_filter=AdpFirstAvailable.*'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (p/'receipts'/('shape-one-'+side+'.log')).write_text(q.stdout.replace(str(p),'$PACKET'))
    (p/'receipts'/('shape-one-'+side+'.rc')).write_text(str(q.returncode)+'\n')
    assert q.returncode==(1 if side=='base' else 0)
    assert '[==========] 4 tests from 1 test suite ran.' in q.stdout
    print('one source/one sink/one interface',side,q.returncode,flush=True)
with cf.ThreadPoolExecutor(2) as pool:list(pool.map(run,('base','head')))
