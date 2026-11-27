#!/usr/bin/env python3
"""Demonstrate surviving defects using ordinary BIND_RX commands only."""
import argparse, json, pathlib, shlex, subprocess, xml.etree.ElementTree as ET
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('packet',type=pathlib.Path); a=p.parse_args()
src,out=a.source.resolve(),a.packet.resolve()
work=out/'scratch/witness'; work.mkdir(exist_ok=True)
rec=out/'receipts/witness'; rec.mkdir(parents=True,exist_ok=True)
build=out/'scratch/gcc'
addition='''
namespace {
TEST_F(AcmpCore, IndependentTalkerTopOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA ^ 0x0200000000000000ull);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "talker-only top octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[4], 2u) << "saved talker top octet must follow the new binding";
}
TEST_F(AcmpCore, IndependentControllerTopOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA, 1u, kCtl1 ^ 0x0200000000000000ull);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "controller-only top octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[12], 2u) << "saved controller top octet must follow the new binding";
}
TEST_F(AcmpCore, IndependentUniqueHighOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA, 0x0101u);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "unique-id-only high octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[2], 1u) << "saved unique-id high octet must follow the new binding";
}
}
'''
(rec/'added-tests.cpp').write_text(addition)
(work/'test_acmp.cpp').write_text((src/'tests/test_acmp.cpp').read_text()+addition)
flags=shlex.split(subprocess.check_output(['pkg-config','--cflags','--libs','gmock','gtest'],text=True))
rows=[]
with (rec/'build.log').open('w') as log:
    def command(argv):
        subprocess.run(list(map(str,argv)),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
    command(['g++','-std=c++20','-O0','-g','-Wall','-Wextra','-Werror','-I'+str(src/'tests'),'-I'+str(src/'include'),*flags,'-c',work/'test_acmp.cpp','-o',work/'test.o'])
    for name in ['head','omit-talker-top-octet','omit-controller-top-octet','omit-unique-high-octet']:
        objects=[] if name=='head' else [out/'scratch/probes'/name/'core.o']
        command(['g++',*objects,work/'test.o',build/'CMakeFiles/acmp_tests.dir/tests/main.cpp.o',build/'libtsn_test.a',*flags,'--coverage','-o',work/name])
        with (rec/(name+'.log')).open('w') as testlog:
            r=subprocess.run([str(work/name),'--gtest_filter=AcmpCore.Independent*','--gtest_output=xml:'+str(rec/(name+'.xml'))],stdout=testlog,stderr=subprocess.STDOUT,timeout=120)
        doc=ET.parse(rec/(name+'.xml')).getroot()
        rows.append(dict(variant=name,rc=r.returncode,tests=int(doc.get('tests')),failures=int(doc.get('failures'))))
(rec/'results.json').write_text(json.dumps(rows,indent=2)+'\n'); print(json.dumps(rows,indent=2))
assert rows[0]['rc']==0 and all(r['rc']==1 and r['failures']==1 for r in rows[1:])
