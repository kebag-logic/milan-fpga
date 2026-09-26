import subprocess,os,time,json
from pathlib import Path
root=Path('$VALIDATION_STORAGE/565-a344')
commands=[
('docs-git',['python3','-B','scripts/docs_check.py'],{}),
('docs-no-git',['python3','-B','scripts/docs_check.py'],{'GIT_DIR':'/dev/null'}),
('em-dash',['python3','-B','scripts/check_em_dash.py','--base','831f94f4'],{}),
('doc-style',['python3','-B','scripts/check_doc_style.py'],{}),
('toc',['python3','-B','scripts/gen_toc.py','--check'],{}),
('anchors',['python3','-B','scripts/gen_toc.py','--verify-anchors'],{}),
('doc-paths',['python3','-B','scripts/check_doc_paths.py'],{}),
('capture-gate',['python3','-B','scripts/check_nvm_capture.py'],{}),
('diff-check',['git','diff','--check'],{})]
for name,argv,extra in commands:
    env=os.environ.copy();env.update(extra)
    start=time.monotonic()
    with (root/(name+'.log')).open('w') as log:
        r=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=7200)
    result=dict(argv=argv,env=extra,rc=r.returncode,seconds=time.monotonic()-start)
    (root/(name+'-result.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(name,result,flush=True)
    print((root/(name+'.log')).read_text()[-2500:],flush=True)
    if r.returncode:raise SystemExit(r.returncode)
