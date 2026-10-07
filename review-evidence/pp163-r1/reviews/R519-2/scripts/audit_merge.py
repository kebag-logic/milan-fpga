#!/usr/bin/env python3
"""Check merged controls, check-body preservation, patches and exact tracked bytes."""
import hashlib, importlib.util, json, os, pathlib, re, subprocess, sys
src=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'
def git(*args): return subprocess.check_output(['git','-C',str(src),*args])
def blob(ref,path): return git('show',ref+':'+path).decode()
def module(ref):
    m=type(sys)('notify_'+ref);m.__file__=str(src/'tb/pp_top/notify_mutants.py');sys.modules[m.__name__]=m
    exec(compile(blob(ref,'tb/pp_top/notify_mutants.py'),m.__file__,'exec'),m.__dict__)
    return m
heads={r:module(r) for r in ['cd9825c9','2ad2f845','ff581556','c9f74b68','HEAD']}
now={m.name:m for m in heads['HEAD'].MUTANTS};out={}
for r,m in heads.items():
    old={x.name:x for x in m.MUTANTS};missing=sorted(set(old)-set(now))
    changed_checks=[n for n in old.keys() & now.keys() if old[n].checks!=now[n].checks]
    changed_edits=[n for n in old.keys() & now.keys() if old[n].edits!=now[n].edits]
    out[r]={'arms':len(old),'missing':missing,'changed_named_checks':changed_checks,'changed_edits':changed_edits}
    assert not missing and not changed_checks
    assert set(changed_edits) == ({'cancel_one_clock_late','dereg_lost_at_round_end'} if r in ['cd9825c9','ff581556'] else {'dereg_lost_at_round_end'} if r == '2ad2f845' else set())
assert len(now)==89
plant=[]
for m in now.values():
    texts={}
    for path,old,new in m.edits:
        text=texts.get(path,blob('HEAD',path));assert text.count(old)==1,(m.name,path,text.count(old))
        texts[path]=text.replace(old,new,1)
    plant.append({'mutant':m.name,'edits':len(m.edits),'checks':list(m.checks),'planted':True})
out['notify_plants']=plant
patch_tree=scratch/'suites'
patches=[]
for rel in git('ls-files','tb/**/*.patch').decode().splitlines():
    r=subprocess.run(['git','apply','--check',str(src/rel)],cwd=patch_tree,capture_output=True,text=True)
    patches.append({'path':rel,'rc':r.returncode,'output':r.stdout+r.stderr})
assert all(p['rc']==0 for p in patches)
out['patches']=patches
# Donor code and interaction checks preserved byte-for-byte.
identities=['hdl/aecp/KL_aecp_notify.sv','tb/aecp_notify/port_tuple.hpp','tb/pp_top/interface_phases.hpp','tb/adp_engine/sim_if2.cpp']
out['donor_blobs']={p:git('rev-parse','HEAD:'+p).decode().strip() for p in identities}
assert all(blob('c9f74b68',p)==blob('HEAD',p) for p in identities)
def section(ref,path,start,end):return blob(ref,path).split(start,1)[1].split(end,1)[0]
assert section('cd9825c9','tb/pp_top/notify_phases.hpp','struct WithdrawStagePhase', '[[maybe_unused]]')==section('HEAD','tb/pp_top/notify_phases.hpp','struct WithdrawStagePhase','[[maybe_unused]]')
assert section('c9f74b68','tb/pp_top/notify_phases.hpp','struct DomainNotifyPhase','[[maybe_unused]]').strip()==section('HEAD','tb/pp_top/notify_phases.hpp','struct DomainNotifyPhase','// ==== WD.').strip()
out['WD_DN_body_identity']=True
# Only the final reporting block moves in c4539ff1.
p='tb/pp_top/sim_main.cpp';old=blob('HEAD^',p);new=blob('HEAD',p)
marker='  //! NOT the canonical tally shape:'
body=old[old.index(marker,old.index('int main(')):old.rindex('}')]
helper=new[new.index(marker,new.index('static int report_build')):new.index('\n}\n\nint main')+1]
assert body==helper
before=old[old.index('int main('):old.index(marker,old.index('int main('))]
after=new[new.index('int main('):new.index('  return report_build(h, build);')]
assert before==after
out['tally_extraction']={'same_reporting_body':True,'same_main_prefix':True,'old_main_lines':len(old[old.index('int main('):].splitlines()),'new_main_lines':len(new[new.index('int main('):].splitlines())}
(receipts/'merge-plant-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'parent_arms':{r:out[r]['arms'] for r in heads},'notify_arms':len(plant),'notify_edits':sum(x['edits'] for x in plant),'patches':len(patches),'tally':out['tally_extraction']}))
