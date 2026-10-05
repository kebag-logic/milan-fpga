#!/usr/bin/env python3
"""Gate-only fault probes in a disposable copy; the reviewed source is never edited."""
import pathlib,subprocess,shutil,sys,os,re,json
p=pathlib.Path(__file__).resolve().parents[1]; source=p/'scratch/tree'; root=p/'scratch/id-probe'
if root.exists():shutil.rmtree(root)
subprocess.run(['git','clone','--quiet','--no-hardlinks',str(source),str(root)],check=True)
os.environ['TMPDIR']=str(p/'scratch')
paths=subprocess.check_output(['git','-C',str(root),'ls-files','-z','--','docs','hdl','tb']).decode().split('\0')
original={x:(root/x).read_bytes() for x in paths if x}
forms=[
 ('braced-single','T-ACMP-CMD','T-ACMP-','T-ACMP-{CMD, DELAY}', 'docs/README.md'),
 ('braced-hyphenated','T-NVM-RS-AGGREGATE','T-NVM-','T-NVM-{RS-DEADLINE, RS-AGGREGATE}','docs/README.md'),
 ('line-broken','T-ADP-DELAY-START','T-ADP-','T-ADP-\n//                DELAY-START','tb/adp_engine/tb_adp_top.sv'),
 ('optional-base','T-ADP-DELAY','T-ADP-','T-ADP-DELAY(-START)','hdl/adp/KL_adp_engine.sv'),
 ('optional-tail','T-ADP-DELAY-START','T-ADP-','T-ADP-DELAY(-START)','hdl/adp/KL_adp_engine.sv'),
 ('optional-line-broken','T-ADP-DELAY-START','T-ADP-','T-ADP-DELAY(-\n//                START)','tb/pp_top/pp_top_wrap.sv'),
 ('minus-one','P-RX-SLOTS','P-RX-SLOTS','P-RX-SLOTS-1','hdl/common/pp_pkg.sv'),
 ('sibling','T-BUDGET-AECP-WC','T-BUDGET-AECP-','T-BUDGET-AECP-TYP / -WC','docs/architecture/08_timing.md'),
]
masters=['docs/architecture/01_overview.md','docs/architecture/08_timing.md']
def call(label,args):
 r=subprocess.run([sys.executable,str(root/'scripts/check-ids.py'),*args],text=True,capture_output=True)
 print(label,'rc',r.returncode);print(r.stdout,end='');print(r.stderr,end='')
 return r
for label,target,prefix,form,path in forms:
 assert form in original[path].decode(),(label,'form not in actual tree')
 for rel,data in original.items():
  if b'\0' not in data[:8192]:
   # Suppress competing references in copies, keeping every original registry row.
   text=data.decode('utf-8',errors='replace'); text=re.sub(r'(?<![A-Za-z0-9_-])'+re.escape(prefix),'Z'+prefix[1:],text)
   if rel in masters:
    oldlines=data.decode().splitlines(); newlines=text.splitlines()
    start=next(i for i,line in enumerate(oldlines) if ('## 7. Parameter master table (F01.5)' in line if rel==masters[0] else '<a id="fig-08-constants"></a>' in line))
    began=False
    for i in range(start+1,len(oldlines)):
     line=oldlines[i]
     if line.startswith('|'):
      began=True
      if prefix in line.split('|')[1]:
       cells=newlines[i].split('|');cells[1]=line.split('|')[1];newlines[i]='|'.join(cells)
     elif began:break
    text='\n'.join(newlines)+'\n'
   (root/rel).write_text(text)
 (root/path).write_text((root/path).read_text()+'\n'+form+'\n')
 good=call(label+' present',['--root',str(root)]); assert good.returncode==0
 master=masters[0] if target.startswith('P-') else masters[1]
 text=(root/master).read_text(); lines=text.splitlines(keepends=True); removed=[]
 for i,line in enumerate(lines):
  if line.startswith('|') and target in line.split('|')[1].split():removed.append(i)
 if target=='T-BUDGET-AECP-WC':
  removed=[i for i,line in enumerate(lines) if line.startswith('| T-BUDGET-AECP-TYP / -WC |')]
 assert len(removed)==1,(target,removed)
 i=removed[0]
 if target=='P-RX-SLOTS':lines[i]=lines[i].replace('P-RX-SLOTS × ', '')
 elif target=='T-BUDGET-AECP-WC':lines[i]=lines[i].replace(' / -WC', '')
 else:lines.pop(i)
 (root/master).write_text(''.join(lines))
 bad=call(label+' missing row',['--root',str(root)])
 assert bad.returncode==1 and path+':' in bad.stdout and target in bad.stdout
 failures=[x for x in bad.stdout.splitlines() if x.startswith('ID FAIL:')]
 assert all(x.startswith('ID FAIL: '+path+':') for x in failures),failures
for rel,data in original.items():(root/rel).write_bytes(data)
assert call('restored',['--root',str(root)]).returncode==0
# Inject a narrow defect in minus-one resolution, leaving every other branch intact.
script=root/'scripts/check-ids.py'; pristine=script.read_text()
old='(token.endswith("-1") and token[:-2] in rows)';new='token.endswith("-1")'
assert old in pristine;script.write_text(pristine.replace(old,new))
r=call('minus-one accepts nonexistent base: selftest',['--selftest'])
(root/'tb/reviewer-minus-one.txt').write_text('P-REVIEWER-MISSING-1\n')
a=call('minus-one accepts nonexistent base: real tree',['--root',str(root)])
script.write_text(pristine)
b=call('original rejects nonexistent base: real tree',['--root',str(root)])
assert r.returncode==0 and a.returncode==0 and b.returncode==1
print('CONFIRMED self-test survivor: unknown minus-one base')
(root/'tb/reviewer-minus-one.txt').unlink()
assert call('final exact tree',['--root',str(root)]).returncode==0
