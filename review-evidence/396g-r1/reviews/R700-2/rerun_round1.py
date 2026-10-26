#!/usr/bin/env python3
"""Rerun retained public probes unchanged, then explicitly port only layout/anchor."""
import concurrent.futures, contextlib, hashlib, io, json, os, pathlib, shutil, subprocess, sys, tarfile, traceback
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent;scratch=out/'scratch'
public=scratch/'public';original=out/'round1-probes.py';text=original.read_text()
results=[]
namespace={'__name__':'__main__','__file__':str(original)}
args=sys.argv;sys.argv=[str(original),str(root)]
with (out/'round1-unmodified.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
 try:exec(compile(text,str(original),'exec'),namespace);rc=0
 except Exception as exc:
  traceback.print_exc();rc=1
  results.append(dict(name='unchanged-round1',rc=rc,exception=repr(exc),count_mutant_anchor_occurrences=namespace['text'].count(namespace['old'])))
sys.argv=args
(out/'round1-unmodified.rc').write_text(str(rc)+'\n')
(out/'round1-unmodified-partial.json').write_text(json.dumps(namespace.get('rows',[]),indent=2)+'\n')
portdir=scratch/'own-layout-port';portdir.mkdir(exist_ok=True)
old='values = [((c+1)*4096 + ((i+shift)%4096))*256 for c in range(C)]'
new='n = i + shift\n        code = ((n // 2048) * 0x9E3779B1) % 2**32\n        values = [(((c+1) << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)) << 8 for c in range(C)]'
assert text.count(old)==1
ported=text.replace(old,new).replace("old='words, n=abs(shift),'","old='\"n\": abs(shift),'").replace("new='words, n=abs(shift) + 1,'","new='\"n\": abs(shift) + 1,'")
(portdir/'probes.py').write_text(ported)
(out/'round1-port.patch').write_text(''.join(__import__('difflib').unified_diff(text.splitlines(True),ported.splitlines(True),fromfile='round1-probes.py',tofile='layout-port/probes.py')))
export=scratch/'mutant-export';export.mkdir(exist_ok=True)
raw=subprocess.check_output(['git','archive','HEAD','tb/tools','tests'],cwd=root)
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(export,filter='data')
def run(name,cmd,cwd):
 with (out/(name+'.log')).open('w') as log:
  r=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,TMPDIR=str(scratch)),timeout=550)
 (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return dict(name=name,rc=r.returncode)
commands=[('round1-layout-port',[sys.executable,'-B',str(portdir/'probes.py'),str(root)],root),
 ('prior-reviewer-mutants',[sys.executable,'-B',str(out/'prior-reviewer-mutants.py'),str(export),str(scratch/'prior-mutants'),'8'],root)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results+=list(pool.map(lambda j:run(*j),commands))
for filename in ('probes.json','grader_mutant.log','grader_mutant.rc'):
 shutil.copy2(portdir/filename,out/('round1-port-'+filename))
(out/'round1-rerun.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
