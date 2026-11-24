#!/usr/bin/env python3
"""Reproduce suite outputs from isolated base/head trees; all children joined."""
import concurrent.futures, hashlib, json, os, pathlib, subprocess, sys, time
P=pathlib.Path(__file__).resolve().parents[1]
S=P/'scratch'
V=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
REVS={'base':'300da99beed5bb1c77e4b04af0bb4f9369856e0d','head':'fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f'}
def prep(repo):
    for label,rev in REVS.items():
        tree=S/label
        if not tree.exists():
            subprocess.run(['git','clone','--quiet','--shared','--no-checkout',repo,str(tree)],check=True)
            subprocess.run(['git','-C',str(tree),'checkout','--quiet','--detach',rev],check=True)
            subprocess.run(['git','-C',str(tree),'submodule','update','--init','third_party/verilog-axis','protocol-processor','gptp-processor','third_party/tsn-c-stack'],check=True)
    w=S/'simulator'
    w.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\ni=0\nwhile i<len(a):\n if a[i]=="-j": a[i+1]="2"; i+=1\n i+=1\nos.execv('+repr(V)+', ['+repr(V)+']+a)\n')
    w.chmod(0o755)
def task(label,suite):
    cwd=S/label/'tb/verilator'/suite
    name=label+'.'+suite
    env=os.environ.copy(); env.update(VERILATOR=str(S/'simulator'),VERILATOR_JOBS='2',MAKEFLAGS='--no-print-directory',OBJCACHE='',TMPDIR=str(S/'tmp'),PYTHONUNBUFFERED='1')
    (S/'tmp').mkdir(exist_ok=True)
    build=open(P/'receipts'/f'{name}.build.log','w'); out=open(P/'receipts'/f'{name}.output.log','w')
    cmds=[]
    def run(args,simulation=False):
        start=time.monotonic()
        proc=subprocess.run(args,cwd=cwd,env=env,stdout=out if simulation else build,stderr=subprocess.STDOUT)
        cmds.append({'argv':args,'rc':proc.returncode,'wall_seconds':round(time.monotonic()-start,3)})
        if proc.returncode: raise RuntimeError(f'{name}: {args} rc {proc.returncode}')
    def make(target):run(['make','-j16',target,'VERILATOR='+str(S/'simulator'),'VERILATOR_JOBS=2'])
    try:
        if suite=='crf_rx':
            make('unit-build');run(['./obj_dir/Vcrf_rx_sim'],True)
            make('discontinuity-build');run(['./obj_discontinuity/Vdiscontinuity'],True)
            # Separate simulation from its build for literal comparison without filtering.
            cmd=subprocess.check_output(['make','-n','talker_step','VERILATOR='+str(S/'simulator')],cwd=cwd,text=True)
            first=cmd.rsplit('./obj_talker/Vtalker_step',1)[0]
            run(['bash','-c',first]);run(['./obj_talker/Vtalker_step'],True)
            run(['python3','mutants.py'],True)
        elif suite=='maap':
            make('build');run(['./obj_dir/VKL_maap_sim'],True)
            run(['python3','mutants.py'],True)
        elif suite=='aaf_clock_meter':
            make('build');run(['./obj_dir/Vmeter_sim'],True)
            make('servo-build');run(['./obj_servo/Vservo_sim'],True)
            run(['python3','mutants.py'],True)
        elif suite=='mmcm_servo':
            make('unit-build');run(['./obj_dir/Vservo_sim'],True)
            cmd=subprocess.check_output(['make','-n','run','VERILATOR='+str(S/'simulator')],cwd=cwd,text=True)
            # The rails command is one continued command between the first run and second separator.
            lines=cmd.splitlines(); k=next(i for i,x in enumerate(lines) if '--top-module rails_wrap' in x)
            start=k
            while start>0 and lines[start-1].endswith('\\'):start-=1
            end=k
            while lines[end].endswith('\\'):end+=1
            run(['bash','-c','\n'.join(lines[start:end+1])]);run(['./obj_rails/Vrails_sim'],True)
            make('phc_step_build');run(['./obj_phc/Vphc_step'],True);run(['./obj_phc/Vphc_step','+slew_suite'],True)
        status='PASS'
    except Exception as e: status=str(e)
    finally:
        build.close();out.close()
        (P/'receipts'/f'{name}.commands.json').write_text(json.dumps({'revision':REVS[label],'status':status,'commands':cmds},indent=2)+'\n')
        (P/'receipts'/f'{name}.rc').write_text(('0' if status=='PASS' else '1')+'\n')
    return name,status
if __name__=='__main__':
    prep(sys.argv[1])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        tasks=[pool.submit(task,label,suite) for label in REVS for suite in ('crf_rx','maap','mmcm_servo','aaf_clock_meter')]
        for f in concurrent.futures.as_completed(tasks):print(*f.result(),flush=True)
