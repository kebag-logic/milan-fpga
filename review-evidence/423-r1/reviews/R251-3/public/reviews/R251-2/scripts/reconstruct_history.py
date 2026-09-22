"""Read public donor commit objects; reproduce hashes, G/H/T and CLI results."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
a.checkout=a.checkout.resolve()
a.output=a.output.resolve()
a.output.mkdir(parents=True,exist_ok=True)
donor=a.checkout/'gptp-processor'
sys.path.insert(0,str(a.checkout/'scripts'))
import check_merge_containment as mc
import merge_containment_replay as proof
os.chdir(donor)
os.environ.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)

def git(*args):
    return subprocess.run(['rtk','proxy','git','--no-replace-objects',*args],capture_output=True,check=True).stdout

source_a='9790ac736e6d10301ad814ffdf73dbe37b59768b'
source_m='f27b45500cb02a5277b5cb32cef408658c1f914e'
source_c='3db86812096830fada2f5f276fa5f4d9f37d1d14'
replay_a='20927af74752620b2ad0f973e8be3203994b5547'
replay_c='5602e70bb4cf70c2e0e39e846e26925e27659e32'
targets=['f0f1c055ee5226f08e656c27cb1bf4c355be11ae','c1b617435824929a790739ea8585c3fe1a328cc0']
records={'commits':{},'patch_pairs':[],'targets':[]}
for oid in [source_a,source_m,source_c,replay_a,replay_c,*targets]:
    record=git('cat-file','commit',oid)
    (a.output/(oid+'.commit')).write_bytes(record)
    records['commits'][oid]={'parents':[line[7:].decode() for line in record.splitlines() if line.startswith(b'parent ')],
                            'tree':record.splitlines()[0][5:].decode()}
assert records['commits'][source_m]['parents']==['7fa64e99490b4648797374d3fdb1fedf08145e91',source_a]
assert records['commits'][source_a]['parents']==[records['commits'][source_m]['parents'][0]]
assert records['commits'][source_m]['tree']==records['commits'][source_a]['tree']
for source,replay,expected in [(source_a,replay_a,'d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3'),
                               (source_c,replay_c,'fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f')]:
    patches=[]
    for oid in [source,replay]:
        patch_bytes=git('diff','--no-ext-diff','--no-textconv','--no-renames',oid+'^',oid)
        (a.output/(oid+'.diff')).write_bytes(patch_bytes)
        patches.append(patch_bytes)
    assert patches[0]==patches[1]
    assert hashlib.sha256(patches[0]).hexdigest()==expected
    assert mc._same_patch_postimage(source,replay)==(True,None)
    records['patch_pairs'].append({'source':source,'replay':replay,'sha256':expected,
                                   'byte_identical':True,'postimages_equal':True})
with tempfile.TemporaryDirectory(prefix='r251-history-baseline-') as td:
    baseline=Path(td)/'check_merge_containment.py'
    baseline.write_bytes(subprocess.run(['rtk','proxy','git','-C',str(a.checkout),'show',
                        '52711029f374650dc93830d5ea28e81cb5c8f410:scripts/check_merge_containment.py'],
                        capture_output=True,check=True).stdout)
    for target in targets:
        g=proof._redundant_merge_shape(source_c,target,mc._git)
        h=mc._linear_patches_contained(source_c,target)
        paths=proof._retained_at_tip(source_c,target,mc._git)
        assert g and h==(True,None)
        assert paths==[repr('tb/tsngen/mutants.py'),repr('tb/verilator/gaskets/mutants.py')],paths
        row={'target':target,'G':g,'H':h,'T_unproved':paths,'commands':[]}
        for label,checker,source,want in [('source-pr62',a.checkout/'scripts/check_merge_containment.py',source_c,(1,b'UNKNOWN')),
                                        ('base-pr62',baseline,source_c,(1,b'STRANDED')),
                                        ('source-pr61',a.checkout/'scripts/check_merge_containment.py',source_a,(0,b'contained')),
                                        ('base-pr61',baseline,source_a,(0,b'contained'))]:
            cmd=['rtk','proxy','python3','-B',str(checker),'--no-fetch','--base',target,source]
            r=subprocess.run(cmd,capture_output=True)
            key=target[:8]+'-'+label
            (a.output/(key+'.stdout')).write_bytes(r.stdout)
            (a.output/(key+'.stderr')).write_bytes(r.stderr)
            assert (r.returncode,r.stdout.split()[0])==want,(key,r.stdout,r.stderr)
            row['commands'].append({'label':label,'argv':cmd,'exit':r.returncode,'stdout':r.stdout.decode()})
            print(key,r.returncode,r.stdout.splitlines()[0].decode())
        ancestor=git('merge-base',target,source_c).strip().decode()
        touched=git('diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',ancestor,source_c).split(b'\0')[:-1]
        row['entries']={}
        for name in touched:
            path=os.fsdecode(name)
            entries=[proof._tree_entry(oid,path) for oid in [ancestor,target,source_c]]
            row['entries'][path]={'ancestor_tip_source':entries,'retained':proof._entry_retained(*entries)}
        records['targets'].append(row)
(a.output/'history.json').write_text(json.dumps(records,indent=2)+'\n')
print('PASS: public hashes, ordered parents, matching postimages, both PR62 refusals and existing PR61 historical positives.')
