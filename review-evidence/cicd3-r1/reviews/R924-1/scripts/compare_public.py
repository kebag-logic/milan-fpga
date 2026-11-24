#!/usr/bin/env python3
"""Recheck the published A/B receipt identities with the published host-text normalization."""
import importlib.util,json,pathlib,re,sys
p=pathlib.Path(sys.argv[1]); receipts=p/'receipts'
spec=importlib.util.spec_from_file_location('published_logcmp',receipts/'tools/logcmp.py');lc=importlib.util.module_from_spec(spec);spec.loader.exec_module(lc)
stage=[(re.compile(r'<TMP>/[A-Za-z0-9_.-]+'),'<STAGE>'),(re.compile(r'milan-mutant-stage-\d+/[A-Za-z0-9_.-]+'),'<STAGE>'),(re.compile(r'<TMP>/<STAGE>'),'<STAGE>')]
def norm(path,mutant=False):
 lines=lc.norm(path)
 if mutant:
  for pat,replacement in stage: lines=[pat.sub(replacement,line) for line in lines]
 return lines
for folder,names in [('mut3',['crf_rx-mutants','avtp_rxmon-depkt_mutants']),('mut2',['tcam-mutants','rx_filter-binding_mutant'])]:
 for name in names:
  base=norm(receipts/'mutants'/folder/'m3b-cold'/(name+'.log'),True)
  for arm in ('m3b-warm','m3h-cold','m3h-warm','m3x-warm'):
   actual=norm(receipts/'mutants'/folder/arm/(name+'.log'),True)
   assert actual==base,(name,arm)
   print(json.dumps(dict(driver=name,arm=arm,identical=True,lines=len(base))))
  for arm in ('m3b-warm','m3h-warm'):
   stats=dict(line.split() for line in (receipts/'mutants'/folder/arm/(name+'.stats')).read_text().splitlines())
   print(json.dumps(dict(driver=name,arm=arm,direct_hits=stats['direct_cache_hit'],misses=stats['cache_miss'])))
for group,a,b,file in [('piece','p0-listorder','p0-longestfirst','milan_dp__0.json'),('preflight','s9-pre','s9-nopre','maap__2.json')]:
 left=json.loads((receipts/group/a/file).read_text());right=json.loads((receipts/group/b/file).read_text())
 for name in ('head','tree'):left.pop(name);right.pop(name)
 assert left==right,(group,'receipt difference')
 print(json.dumps(dict(group=group,receipt_identical_except_head_tree=True,cases=len(left['results']))))
 if group=='piece':
  assert norm(receipts/group/a/'log')==norm(receipts/group/b/'log')
  print(json.dumps(dict(group=group,published_excerpt_identical=True,lines=len(norm(receipts/group/a/'log')),full_transcript_recomputed=False)))
 else:
  for file in ('maap__2.log','aaf_clock_meter.log'):
   assert norm(receipts/group/a/'logs'/file)==norm(receipts/group/b/'logs'/file)
   print(json.dumps(dict(group=group,file=file,transcript_identical=True)))
print('Coverage limit: four completed mutation-driver A/B comparisons; mmcm_servo is incomplete, not identical evidence.')
