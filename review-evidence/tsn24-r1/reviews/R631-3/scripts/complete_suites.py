#!/usr/bin/env python3
import argparse,concurrent.futures,hashlib,json,os,pathlib,re,shutil,subprocess,xml.etree.ElementTree as ET
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--jobs',type=int,default=8);a=ap.parse_args();p=a.packet.resolve();w=p/'scratch';source=w/'source';env=json.loads((w/'environment.json').read_text());env={k:v for k,v in env.items() if not k.startswith('GTEST_')};out=w/'complete-suites';out.mkdir(exist_ok=True)
plants=[m for m in json.loads((source/'tests/mutations.json').read_text()) if m['name'].startswith(('dafresh-','g-expiry-')) or m['name']=='x-zero-never-expires']
bins=['adp_tests','acmp_tests','maap_tests','entity_tests','port_tests','adp_release','adp_debug','maap_debug']
def run_suite(b,d):
    d.mkdir(parents=True,exist_ok=True);cases={};rcs={};failures={}
    for name in bins:
        xml=d/(name+'.xml');xml.unlink(missing_ok=True)
        with (d/(name+'.log')).open('w') as log:r=subprocess.run([str(b/name),'--gtest_output=xml:'+str(xml)],env=env,stdout=log,stderr=subprocess.STDOUT)
        rcs[name]=r.returncode
        root=ET.parse(xml).getroot();nodes=root.findall('.//testcase');assert nodes,name
        assert int(root.get('tests'))==len(nodes)
        for c in nodes:
            test=c.get('classname')+'.'+c.get('name');key=name+'::'+test;assert key not in cases
            assert c.get('status')=='run' and c.get('result')=='completed',key
            assert not c.findall('skipped'),key
            cases[key]=True
            fs=c.findall('failure')
            if fs:failures[test]='\n'.join(f.get('message','')+' '+(f.text or '') for f in fs)
        assert (r.returncode!=0)==bool(int(root.get('failures'))),name
    return cases,failures,rcs

def one(m):
    name=m['name'];killer=m['kills'][0]['test'];row=out/name
    if name.startswith('g-expiry-'):full=w/'gap'/name;fb=full/'b';removed=w/'physical-gap'/name;rb=removed/'b'
    else:full=w/'escape'/name;fb=full/'build';removed=w/'physical-original'/name;rb=removed/'b'
    testfile='tests/test_entity.cpp' if killer.startswith('EntityYaml.') else 'tests/test_acmp.cpp'
    if killer.startswith('EntityYaml.'):
        removed=w/'physical-entity'/name;tree=removed/'tree';shutil.copytree(source,tree,dirs_exist_ok=True)
        f=tree/m['path'];text=f.read_text();assert text.count(m['old'])==1;f.write_text(text.replace(m['old'],m['new']))
        f=tree/testfile;t=f.read_text();suite,test=killer.split('.');start=t.index(f'TEST({suite}, {test})');start=t.rindex('// REQ:',0,start);end=re.compile(r'^}\n',re.M).search(t,start).end();f.write_text(t[:start]+t[end:]);rb=removed/'b'
        with (removed/'build.log').open('w') as log:
            subprocess.run(['cmake','-S',str(tree),'-B',str(rb),'-DCMAKE_BUILD_TYPE=Debug'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
            subprocess.run(['cmake','--build',str(rb),'-j16'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    # Verify copies differ only by the declared production plant and one physical test deletion.
    expected=(source/m['path']).read_text().replace(m['old'],m['new'])
    for copy,drop in [(full/'tree',False),(removed/'tree',True)]:
        assert (copy/m['path']).read_text()==expected,name
        for f in source.rglob('*'):
            if not f.is_file():continue
            rel=f.relative_to(source)
            if str(rel)==m['path'] or (drop and str(rel)==testfile):continue
            assert (copy/rel).read_bytes()==f.read_bytes(),str(rel)
    suite,test=killer.split('.');t=(source/testfile).read_text();kind='TEST' if killer.startswith('EntityYaml.') else 'TEST_F';start=t.index(f'{kind}({suite}, {test})');start=t.rindex('// REQ:',0,start);end=re.compile(r'^}\n',re.M).search(t,start).end();assert (removed/'tree'/testfile).read_text()==t[:start]+t[end:]
    fc,ff,fr=run_suite(fb,row/'full');rc,rf,rr=run_suite(rb,row/'removed')
    assert len(fc)==420 and len(rc)==419,(name,len(fc),len(rc))
    assert set(fc)-set(rc)=={('entity_tests' if killer.startswith('EntityYaml.') else 'acmp_tests')+'::'+killer} and set(rc)<=set(fc)
    assert set(ff)=={killer},(name,list(ff));assert m['kills'][0]['needle'] in ff[killer]
    assert not rf and all(v==0 for v in rr.values())
    return dict(plant=name,killer=killer,full_instances=len(fc),removed_instances=len(rc),full_failures=list(ff),removed_failures=list(rf),full_rc=fr,removed_rc=rr,escapes=True,source_and_deletion_verified=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:results=list(ex.map(one,plants))
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print('All',len(results),'plants: full 420 / removed 419, exact named catch, no skips, escape verified')
