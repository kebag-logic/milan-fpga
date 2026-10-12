#!/usr/bin/env python3
import argparse,concurrent.futures,json,os,pathlib,shutil,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--gtest',required=True);ap.add_argument('--clang18',required=True);ap.add_argument('--sdk',type=pathlib.Path);a=ap.parse_args()
src=a.source.resolve();packet=a.packet.resolve();work=packet/'scratch';env={k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
binpath=work/'bin';binpath.mkdir(exist_ok=True)
commands={x:[shutil.which(x)] for x in ['gcc','g++','cc','c++','clang-tidy','cppcheck','riscv64-elf-gcc'] if shutil.which(x)}
commands.update({'clang':[a.clang18],'clang-18':[a.clang18],'clang++':[a.clang18,'--driver-mode=g++']})
if a.sdk:
    sdk=a.sdk.resolve();prefix=['env','LD_LIBRARY_PATH='+str(sdk/'usr/lib/x86_64-linux-gnu')+':'+a.gtest+'/lib']
    for name in ['clang','clang-18','clang++']:commands[name]=prefix+commands[name]
    commands['clang-tidy']=prefix+[str(sdk/'usr/bin/clang-tidy-18')]
    commands['clang++']+=['-nostdinc++']
    for rel in ['usr/include/c++/13','usr/include/x86_64-linux-gnu/c++/13','usr/include/c++/13/backward']:commands['clang++']+=['-isystem',str(sdk/rel)]
for name in commands:
    path=binpath/name
    if not path.exists():path.symlink_to(packet/'scripts/job_limiter.py')
(packet/'scripts/job_limiter.py').chmod(0o755)
cfg=work/'limit.json';cfg.write_text(json.dumps({'commands':commands,'locks':str(work/'locks'),'jobs':16}))
env.update(REVIEW_LIMIT_CONFIG=str(cfg),PATH=str(binpath)+':'+env['PATH'],PKG_CONFIG_PATH=a.gtest+'/lib/pkgconfig',CMAKE_PREFIX_PATH=a.gtest,LD_LIBRARY_PATH=a.gtest+'/lib',TSN_CLANG=str(binpath/'clang-18'))
(work/'environment.json').write_text(json.dumps(env,indent=2))
# Export tracked bytes only. All mutable copies remain in scratch.
for ref,name in [('HEAD','source'),('1ba2735','base')]:
    tree=work/name;tree.mkdir(exist_ok=True)
    archive=subprocess.check_output(['git','archive',ref],cwd=src)
    subprocess.run(['tar','-xf','-','-C',str(tree)],input=archive,check=True)
plants=json.loads((src/'tests/mutations.json').read_text())
core=','.join(m['name'] for m in plants if (m['name'].startswith('dafresh-') or m['name']=='x-zero-never-expires') and m['kills'][0]['test'].startswith('AcmpFresh.'))
py='python3';scripts=packet/'scripts';tree=str(work/'source')
tasks=[('validate',[py,'scripts/validate.py','--work',str(work/'validation'),'--jobs','16'],src),
('rv32',[py,'scripts/baremetal.py','--work',str(work/'rv32'),'--jobs','16'],src),
('rv32-base',[py,'scripts/baremetal.py','--work',str(work/'rv32-base'),'--jobs','16'],work/'base'),
('escape',[py,str(scripts/'R630-1/escape_probe.py'),'--tree',tree,'--work',str(work/'escape'),'--jobs','8'],src),
('physical-original',[py,str(scripts/'R630-1/physical_removal.py'),'--tree',tree,'--work',str(work/'physical-original'),'--plants',core],src),
('gap',[py,str(scripts/'R630-2/gap_mutants.py'),'--tree',tree,'--work',str(work/'gap'),'--jobs','6'],src),
('physical-gap',[py,str(scripts/'R630-2/physical_removal.py'),'--tree',tree,'--work',str(work/'physical-gap'),'--plants','g-expiry-skipped-with-listener,g-expiry-skipped-invalid-da'],src)]
def run(t):
    name,cmd,cwd=t;start=time.time()
    with (work/(name+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    (work/(name+'.rc')).write_text(str(r.returncode)+'\n')
    result=dict(name=name,command=cmd,rc=r.returncode,seconds=round(time.time()-start,2));print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as ex:results=list(ex.map(run,tasks))
(work/'run-results.json').write_text(json.dumps(results,indent=2)+'\n')
