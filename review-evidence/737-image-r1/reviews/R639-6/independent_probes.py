#!/usr/bin/env python3
"""Safe literal probes; no installation, network, or original-tree mutation."""
import contextlib,io,json,os,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT']=str(out/'scratch/shfmt'); os.environ['TMPDIR']=str(out/'scratch')
sys.path[:0]=[str(root/'scripts'),str(root/'ci/image')]
import ci_tool_inventory as inventory
from ci_inventory_patterns_selftest import Fixture
import exec_audit
results=[]
def probe(name,command,files,actual=None):
 with tempfile.TemporaryDirectory(dir=out/'scratch',prefix=name+'-') as tmp:
  f=Fixture(pathlib.Path(tmp)); f.run(command)
  for path,text in files.items(): f.file(path,text)
  result={'name':name,'workflow':command,'files':files,'modes':[]}
  for mode in ['--write','--check']:
   buf=io.StringIO();sys.argv=['inventory','--root',str(f.root),mode]
   with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf): rc=inventory.main()
   result['modes'].append({'mode':mode,'rc':rc,'output':buf.getvalue()})
  if actual:
   # Replace the unknown command with a harmless observable marker only after derivation.
   for path,text in files.items(): f.file(path,text.replace('r639_unlisted_command','echo R639_REACHED_UNLISTED'))
   r=subprocess.run(actual,cwd=f.root,capture_output=True,text=True,timeout=15)
   result['real']={'argv':actual,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
  results.append(result)
probe('make-explicit-stem','make',{'Makefile':'all: probe.c\nprobe.c: ; bash $*bootstrap.sh\n','bootstrap.sh':'echo SAFE\n','probebootstrap.sh':'r639_unlisted_command\n'},[str(out/'scratch/reference/root/usr/bin/make'),'--no-print-directory'])
probe('shell-short-circuit','X=evil.sh; [ -e missing ] && X=benign.sh; bash "$X"',{'evil.sh':'r639_unlisted_command\n','benign.sh':'echo SAFE\n'},[str(out/'scratch/reference/root/usr/bin/bash'),'-c','X=evil.sh; [ -e missing ] && X=benign.sh; bash "$X"'])
probe('make-unlisted','make',{'Makefile':'override X = echo\nall: ; $(X) okay\n'})
probe('shell-unlisted','select x in a; do echo "$x"; done',{})
probe('python-unlisted','python3 probe.py',{'probe.py':'async def probe():\n pass\n'})
probe('python-network','python3 probe.py',{'probe.py':'import urllib.request\n'})
probe('shell-pwd-shadow','pwd() { echo evil; }; cd "$(cd safe && pwd)"; bash bootstrap.sh',{'safe/bootstrap.sh':'echo SAFE\n','evil/bootstrap.sh':'r639_unlisted_command\n'},[str(out/'scratch/reference/root/usr/bin/bash'),'-c','pwd() { echo evil; }; cd "$(cd safe && pwd)"; bash bootstrap.sh'])
with tempfile.TemporaryDirectory(dir=out/'scratch',prefix='audit-') as tmp:
 base=pathlib.Path(tmp);env={'PATH':'/usr/bin:/bin','LC_ALL':'C.UTF-8'}; names=exec_audit.allowlist()
 for name in ('apt-get','r639_unlisted_program'):
  path=base/name;shutil.copyfile('/bin/true',path);path.chmod(0o755)
  r=exec_audit.audit_step('ELF '+name,[str(path)],base,env,names);results.append({'name':'audit-elf-'+name,'result':r})
  path.write_text('#!/bin/sh\nprintf "harmless script control\\n"\n');path.chmod(0o755)
  r=exec_audit.audit_step('script '+name,[str(path)],base,env,names);results.append({'name':'audit-script-'+name,'result':r})
 source=base/'static.c';source.write_text('int main(void) {return 0;}\n');binary=base/'r639_static_probe'
 compile=subprocess.run(['cc','-static',str(source),'-o',str(binary)],capture_output=True,text=True,timeout=30)
 if compile.returncode==0:
  r=exec_audit.audit_step('static binary',[str(binary)],base,env,names);results.append({'name':'audit-static','result':r,'file':subprocess.check_output(['file',str(binary)],text=True)})
 else: results.append({'name':'audit-static','not_run':compile.stderr})
text=json.dumps(results,indent=2).replace(str(out),'$PACKET').replace(str(root),'$ROOT')+'\n'
(out/'independent-probes.json').write_text(text)
print(text)
