"""SCRATCH ONLY: bounded historical proof and deliberately strict tip retention.

Not a proposed production replacement. Exit 0 proves the selected condition;
1 means not proved; 2 means an input/plumbing failure. --historical intentionally
omits retention, reproducing the unsafe shortcut for comparison.
"""
import argparse, importlib.util, json, os, pathlib, subprocess, sys
TRUSTED=pathlib.Path('$VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py')
spec=importlib.util.spec_from_file_location('trusted_containment',TRUSTED)
mc=importlib.util.module_from_spec(spec);spec.loader.exec_module(mc)
class Refused(Exception): pass
class Unmeasurable(Exception): pass
def git(*args):
 p=subprocess.run(['rtk','proxy','git','--no-replace-objects',*args],capture_output=True)
 if p.returncode: raise Unmeasurable('Git failed: '+repr(args)+' '+p.stderr.decode(errors='replace'))
 return p.stdout
def parents(oid): return git('show','-s','--format=%P',oid).decode().split()
def tree(oid): return git('rev-parse',oid+'^{tree}').decode().strip()
def entries(oid):
 result={}
 for record in git('ls-tree','-r','-t','-z',oid).split(b'\0'):
  if record:
   metadata,path=record.split(b'\t',1); result[path]=metadata
 return result
def require(value,reason):
 if not value: raise Refused(reason)
def proof(branch,target,historical=False):
 record={'scope':'SCRATCH ONLY; one A/M/C source shape','branch':branch,'target':target,'historical_only':historical}
 try:
  require(mc.is_full_oid(branch) and mc.is_full_oid(target),'full object IDs required')
  err=mc.active_graft_error()
  if err: raise Unmeasurable(err)
  if git('rev-parse','--is-shallow-repository').strip()!=b'false': raise Unmeasurable('incomplete history')
  require(mc.exact_ref_syntax(branch) and mc.exact_ref_syntax(target),'unreadable exact commit')
  cp=parents(branch);require(len(cp)==1,'source tip must have one parent')
  merge=cp[0];mp=parents(merge);require(len(mp)==2,'source parent must be exactly a two-parent merge')
  origin,incoming=mp
  require(parents(incoming)==[origin],'first parent must be the incoming parent sole immediate parent')
  require(tree(merge)==tree(incoming),'merge adds or removes tree content relative to incoming parent')
  unique=set(git('rev-list',target+'..'+branch).decode().split())
  require(unique=={branch,merge,incoming},'only the exact two-linear/one-merge source scope is supported')
  r=subprocess.run(['rtk','proxy','git','--no-replace-objects','merge-base','--is-ancestor',origin,target],capture_output=True)
  if r.returncode not in (0,1): raise Unmeasurable('common-origin query failed')
  require(r.returncode==0,'target lacks the exact common origin')
  record.update({'origin':origin,'incoming':incoming,'merge':merge})
  ok,err=mc._linear_patches_contained(branch,target)
  if err: raise Unmeasurable(err)
  require(ok,'not every source linear commit has a distinct exact replay with identical touched-path postimages')
  record['historical_replay']=True
  if historical:
   record['result']='HISTORICAL ONLY: NOT current retention';return 0,record
  protected=set()
  for commit in (incoming,branch):
   paths,err=mc._commit_paths(commit)
   if err: raise Unmeasurable(err)
   protected.update(os.fsencode(p) for p in paths)
  require(bool(protected),'empty protected set')
  source_entries,target_entries=entries(branch),entries(target)
  different=[os.fsdecode(p) for p in sorted(protected) if source_entries.get(p)!=target_entries.get(p)]
  record['protected_paths']=[os.fsdecode(p) for p in sorted(protected)]
  record['different_at_tip']=different
  require(not different,'current protected entries differ; retention not proved')
  record['result']='exact current protected entries retained';return 0,record
 except Refused as exc:
  record['result']='NOT PROVED: '+str(exc);return 1,record
 except (Unmeasurable,OSError,ValueError) as exc:
  record['result']='UNKNOWN: '+str(exc);return 2,record
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('repo');p.add_argument('branch');p.add_argument('target');p.add_argument('--historical',action='store_true')
 a=p.parse_args();os.chdir(a.repo);rc,result=proof(a.branch,a.target,a.historical);print(json.dumps(result,indent=2));sys.exit(rc)
