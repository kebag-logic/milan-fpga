import subprocess,os,json,shutil
from pathlib import Path
out=Path(__file__).parent;root=out/'scratch'/'supplemental';root.mkdir(exist_ok=True)
for name in ['avdecc','hdl/common/csr']:shutil.copytree(out/'scratch/head'/name,root/name,dirs_exist_ok=True)
paths=['avdecc/aem_maps.py','avdecc/gen_aem_store.py','avdecc/aem_assemble.py','avdecc/aem_descriptors.py'];original={n:(root/n).read_text() for n in paths}
M,S,A,D=paths;results=[]
no_count=(M,'if len(rows) > SMAP_MAX_ROWS:','if False:')
no_crf=(M,'if not chans:','if False:')
no_oracle=(S,'if cause in str(e):','if True:')
wide=(M,'for c in range(2, 8)','for c in range(2, 9)')
reverse=(S,'stale = sorted(set(KNOWN_MAP_DEVIATIONS) - set(got))','stale = []')
oldvector=(S,'1, [[0, c, c % 8, 0] for c in range(63)]),','0, [[0, c % 8, c, 0] for c in range(63)]),')
cases=[('pristine',[],0,'self-test: PASS'),('crf-without-oracle',[no_crf,no_oracle],0,'self-test: PASS'),('wide-without-reverse',[wide,reverse],0,'self-test: PASS'),('old-row-vector-without-oracle',[no_count,oldvector,no_oracle],0,'self-test: PASS'),('new-row-vector-without-oracle',[no_count,no_oracle],1,'has 63 mappings'),('old-row-vector-with-oracle',[no_count,oldvector],1,'refused, but not for'),('directory-all-three-disabled',[(A,'elif prev_t != t:','elif False:'),(A,'if i != runs[t][1]:','if False:'),(A,'if got != want:','if False:')],1,'[FAIL] a shuffled directory'),('formats-ut-lost',[(D,'FORMATS = [0x0205022000806000, 0x0215022002006000]','FORMATS = [0x0205022000806000]')],1,'[FAIL] FORMATS')]
for label,edits,rc,fragment in cases:
 for n,t in original.items():(root/n).write_text(t)
 for n,old,new in edits:
  t=(root/n).read_text();assert t.count(old)==1,(label,old);(root/n).write_text(t.replace(old,new))
 p=subprocess.run(['rtk','proxy','python3','-B','avdecc/gen_aem_store.py','--self-test'],cwd=root,capture_output=True,text=True);s=p.stdout+p.stderr
 # The count-removal message names the test, not the generator exception.
 if label=='new-row-vector-without-oracle':fragment='Table 7-32 allows (62): built without complaint'
 assert p.returncode==rc and fragment in s,(label,p.returncode,s)
 (out/'focused-logs'/('supplemental-'+label+'.log')).write_text(s)
 results.append({'label':label,'exit_code':p.returncode,'expected_fragment':fragment,'result':'PASS'})
for n,t in original.items():(root/n).write_text(t)
(out/'supplemental-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS',len(results),'causal controls')
