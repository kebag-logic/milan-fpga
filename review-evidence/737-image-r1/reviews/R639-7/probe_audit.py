#!/usr/bin/env python3
"""Harmless offline audit controls, confined to packet/scratch; no shared installs."""
import json, os, shlex, sys, tempfile, zipfile
from pathlib import Path
root=Path(os.environ.get('CHECKOUT', os.getcwd())).resolve()
packet=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'ci/image'))
import exec_audit as a

def main():
 with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='audit-') as name:
  work=Path(name)
  env={'PATH':os.environ['PATH'],'HOME':str(work),'LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
  rows=[]
  def run(label,argv):
   result=a.trace(argv,work,env,a.Origin(work,a.checkout_files(work)))
   population,findings=a.judge(result,a.allowlist())
   rows.append({'label':label,**result,'population':population,'findings':findings})
  wheel=work/'zz_probe_pkg-0.1-py3-none-any.whl'
  with zipfile.ZipFile(wheel,'w') as z:
   z.writestr('zz_probe_pkg/__init__.py','')
   z.writestr('zz_probe_pkg-0.1.dist-info/METADATA','Metadata-Version: 2.1\nName: zz-probe-pkg\nVersion: 0.1\n')
   z.writestr('zz_probe_pkg-0.1.dist-info/WHEEL','Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
   z.writestr('zz_probe_pkg-0.1.dist-info/RECORD','')
  args=['install','--no-index','--no-deps','--no-compile','--disable-pip-version-check','--target',str(work/'installed'),str(wheel)]
  run('explicit-module-control',[sys.executable,'-m','pip',*args])
  args[-2]=str(work/'inline-installed')
  run('inline-local-wheel',[sys.executable,'-c','from pip._internal.cli.main import main; raise SystemExit(main('+repr(args)+'))'])
  rows[-1]['installed']=(work/'inline-installed/zz_probe_pkg/__init__.py').is_file()
  stub=work/'apt-get'
  stub.write_text('#!/bin/sh\nprintf observed > '+shlex.quote(str(work/'marker'))+'\n')
  stub.chmod(0o755)
  run('direct-installer-name-control',[str(stub),'--version'])
  (work/'marker').unlink()
  assembly='.section .data\nname: .asciz "'+str(stub)+'"\narg: .asciz "--version"\n.align 4\nargv: .long name, arg, 0\nenvp: .long 0\n.section .text\n.global _start\n_start:\nmov $11,%eax\nmov $name,%ebx\nmov $argv,%ecx\nmov $envp,%edx\nint $0x80\nmov $1,%eax\nmov $93,%ebx\nint $0x80\n'
  (work/'probe.s').write_text(assembly)
  run('compat-exec',['bash','-e','-c','as --32 -o probe.o probe.s; ld -m elf_i386 -o trampoline probe.o; ./trampoline'])
  rows[-1]['installer_stub_ran']=(work/'marker').is_file()
  run('copied-elf-control',['bash','-e','-c','cp /usr/bin/printenv unlisted; ./unlisted --version'])
  run('modified-copied-elf',['bash','-e','-c',"cp /usr/bin/printenv unlisted2; printf '\\0' >> unlisted2; ./unlisted2 --version"])
  text=json.dumps(rows,indent=2).replace(str(work),'<probe>').replace(str(root),'<checkout>').replace(str(Path(sys.executable).parent),'<python-bin>').replace(str(packet),'<packet>')
  (packet/'audit-probes.json').write_text(text+'\n')
  print(json.dumps([{'label':r['label'],'rc':r['exit_status'],'exec_count':len(r['instances']),'findings':[f['reason'] for f in r['findings']],'installed':r.get('installed'),'installer_stub_ran':r.get('installer_stub_ran')} for r in rows],indent=2))
if __name__=='__main__': main()
