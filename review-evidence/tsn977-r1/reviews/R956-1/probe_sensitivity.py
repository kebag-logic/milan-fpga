#!/usr/bin/env python3
"""Compile isolated ACMP defects and run every shipped hosted test binary."""
import argparse, concurrent.futures, json, os, pathlib, shlex, subprocess, xml.etree.ElementTree as ET

p=argparse.ArgumentParser()
p.add_argument('source', type=pathlib.Path)
p.add_argument('packet', type=pathlib.Path)
a=p.parse_args()
src, out=a.source.resolve(), a.packet.resolve()
build=out/'scratch/gcc'
text=(src/'src/acmp.c').read_text()
plants={
    'omit-talker-top-octet': ('(p[4] ^ (th >> 24))', '0u'),
    'omit-controller-top-octet': ('(p[12] ^ (ch >> 24))', '0u'),
    'omit-unique-high-octet': ('(uint32_t)(p[2] ^ (unique >> 8))', '0u'),
    'admit-word-zero': ('static void admit(struct acmp *a)', ''),
    'finish-word-zero': ('static void finish(struct acmp *a)', ''),
}
flags=shlex.split(subprocess.check_output(['pkg-config','--cflags','--libs','gmock','gtest'],text=True))
bins=['adp_tests','acmp_tests','acmp_wide','acmp_walk','maap_tests','entity_tests','port_tests','adp_release','adp_debug','maap_debug']

def probe(name, edit):
    work=out/'scratch/probes'/name
    rec=out/'receipts/probes'/name
    work.mkdir(parents=True,exist_ok=True); rec.mkdir(parents=True,exist_ok=True)
    old,new=edit
    if name.endswith('word-zero'):
        start=text.index(old); end=text.index('\n}',start)+2
        changed=text[:start]+text[start:end].replace('bits = a->dirty[k / 32u];','bits = a->dirty[0];')+text[end:]
    else:
        assert text.count(old)==1
        changed=text.replace(old,new)
    (work/'acmp.c').write_text(changed)
    (rec/'plant.json').write_text(json.dumps(dict(name=name,old=old,new=new),indent=2)+'\n')
    with (rec/'build.log').open('w') as log:
        def command(argv):
            r=subprocess.run(list(map(str,argv)),stdout=log,stderr=subprocess.STDOUT,timeout=120)
            if r.returncode: raise RuntimeError(f'{name} compile/link failed')
        for wide in [False,True]:
            opts=['-DACMP_MAX_SINKS=33u','-fsanitize=shift,undefined','-fno-sanitize-recover=shift,undefined'] if wide else []
            obj=work/('wide.o' if wide else 'core.o')
            command(['gcc','-std=c11','-O0','-g','-Wall','-Wextra','-Werror','-DNDEBUG','-DCTRL_REENTRY_ASSERT',*opts,'-I'+str(src/'include'),'-c',work/'acmp.c','-o',obj])
            for binary in (['acmp_wide','acmp_walk'] if wide else ['acmp_tests','entity_tests']):
                test={'acmp_tests':'test_acmp.cpp','acmp_wide':'test_acmp_wide.cpp','acmp_walk':'test_acmp_walk.cpp','entity_tests':'test_entity.cpp'}[binary]
                objects=[build/f'CMakeFiles/{binary}.dir/tests/{test}.o',build/f'CMakeFiles/{binary}.dir/tests/main.cpp.o']
                libs=[build/'libentity_examples.a'] if binary=='entity_tests' else []
                command(['g++',*opts,obj,*objects,*libs,build/'libtsn_test.a',*flags,'--coverage','-o',work/binary])
    rows=[]
    for binary in bins:
        executable=work/binary if (work/binary).exists() else build/binary
        with (rec/(binary+'.log')).open('w') as log:
            r=subprocess.run([str(executable),'--gtest_output=xml:'+str(rec/(binary+'.xml'))],stdout=log,stderr=subprocess.STDOUT,timeout=120)
        doc=ET.parse(rec/(binary+'.xml')).getroot()
        cases=list(doc.iter('testcase'))
        rows.append(dict(binary=binary,rc=r.returncode,tests=int(doc.get('tests')),failures=int(doc.get('failures')),disabled=int(doc.get('disabled')),errors=int(doc.get('errors')),skipped=sum(bool(c.findall('skipped')) for c in cases),complete=all(c.get('status')=='run' and c.get('result')=='completed' for c in cases)))
    result=dict(plant=name,results=rows,survives=all(r['rc']==0 and r['complete'] and r['failures']==0 and r['disabled']==0 and r['errors']==0 and r['skipped']==0 for r in rows))
    (rec/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda pair:probe(*pair),plants.items()))
(out/'receipts/probes/results.json').write_text(json.dumps(results,indent=2)+'\n')
