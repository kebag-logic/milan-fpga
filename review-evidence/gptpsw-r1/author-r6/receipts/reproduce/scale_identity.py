from pathlib import Path
import hashlib, json, subprocess, sys
root=Path('/data-2/milan/lanes/opt-hart2'); scratch=Path('/data-2/milan/tmp/opt-a837')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
built='368c2d1e9898e43849873bd242fba482924817f0'
head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
changed=subprocess.check_output(['git','-C',str(root),'diff','--name-only',built,head],text=True).splitlines()
observer='tb/verilator/ctrl_service_budget/harts_cost.hpp'
at_build=subprocess.check_output(['git','-C',str(root),'show',f'{built}:{observer}'])
assert at_build==(root/observer).read_bytes()
records=[]
for arm in ('32-d0','32-d8'):
 d=scratch/'scale'/arm;s=json.loads((d/'build.json').read_text());bad=[]
 for key,want in s['inputs'].items():
  if key=='tree:firmware':got=build.tree_digest([root/t for t in build.FIRMWARE_TREES])
  elif key=='tree:config':got=build.tree_digest([root/'configs'/(s['shape']+'.yaml')])
  else:got=hashlib.sha256(build.resolve(key,d).read_bytes()).hexdigest()
  if got!=want:bad.append(key)
 assert not bad,bad
 assert hashlib.sha256((d/'native/Vsim').read_bytes()).hexdigest()==s['executable_sha256']
 assert observer in (d/'native/sim_main.d').read_text()
 records.append(dict(arm=arm,recorded_inputs_match=True,executable_sha256=s['executable_sha256'],
   supplemental_observer_sha256=hashlib.sha256(at_build).hexdigest(),
   observer_same_as_build_commit=True,compiler_depfile_lists_observer=True,
   note='Original manifest omitted the new header; the later builder correctly refuses reuse without it. '
        'Original manifest is retained, not rewritten. This supplemental evidence ties the unmodified header '
        'to the recorded build commit and compiler dependency file.'))
r=dict(build_head=built,report_head=head,changed_since_build=changed,models=records,
  one_hart_before=json.loads((scratch/'scale/onehart32-before/identity.json').read_text()),
  one_hart_after=json.loads((scratch/'scale/onehart32-after/identity.json').read_text()))
assert r['one_hart_before']['sha256']==r['one_hart_after']['sha256']
(scratch/'scale-input-equivalence.json').write_text(json.dumps(r,indent=2)+'\n')
print('All recorded inputs and native executables match; observer header equals the build commit; one-hart ELF matches.')
