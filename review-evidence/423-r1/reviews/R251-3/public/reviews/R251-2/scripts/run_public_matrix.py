"""Use unchanged public fixture builders and frozen expectations on this source."""
import argparse
import importlib.util
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
root=Path(__file__).resolve().parents[1]
a.output.mkdir(parents=True,exist_ok=True)
checker=a.checkout.resolve()/'scripts/check_merge_containment.py'
sys.path.insert(0,str(checker.parent))
import check_merge_containment as mc
import merge_containment_replay as proof
from merge_containment_selftest_scratch import quiet_git

def components(unused,branch):
    unproved=proof._retained_at_tip(branch,'main',mc._git)
    return {'G_shape':proof._redundant_merge_shape(branch,'main',mc._git),
            'H_replay':mc._linear_patches_contained(branch,'main')[0],
            'T_retained':not unproved,'T_detail':unproved}

with tempfile.TemporaryDirectory(prefix='r251-public-matrix-') as td:
    work=Path(td)
    baseline=work/'baseline'
    baseline.mkdir()
    names=['check_merge_containment.py','merge_containment_selftest.py',
           'merge_containment_selftest_content.py','merge_containment_selftest_scratch.py']
    for name in names:
        data=subprocess.run(['rtk','proxy','git','-C',str(a.checkout),'show',
                             '52711029f374650dc93830d5ea28e81cb5c8f410:scripts/'+name],
                            capture_output=True,check=True).stdout
        (baseline/name).write_bytes(data)
    r=subprocess.run(['rtk','proxy','python3','-B',str(baseline/'check_merge_containment.py'),'--selftest'],capture_output=True)
    (a.output/'baseline-selftest.stdout').write_bytes(r.stdout)
    (a.output/'baseline-selftest.stderr').write_bytes(r.stderr)
    assert r.returncode==0,r.stderr
    original_ids=[line.split()[1] for line in r.stdout.decode().splitlines() if line.startswith('  ok')]
    current_ids=[line.split()[1] for line in (root/'raw/selftest.stdout').read_text().splitlines() if line.startswith('  ok')]
    assert len(original_ids)==145
    assert current_ids[:145]==original_ids
    (a.output/'existing-arm-preservation.json').write_text(json.dumps({'baseline_exit':r.returncode,
        'baseline_assertions':len(original_ids),'current_assertions':len(current_ids),
        'original_145_names_and_order_preserved':True,'names':original_ids},indent=2)+'\n')
    sys.argv=['fixtures.py',str(baseline/'check_merge_containment.py'),str(checker),
              str(work/'fixtures'),str(a.output.resolve()/'matrix.json')]
    spec=importlib.util.spec_from_file_location('public_fixtures',root/'public/author/public/scripts/fixtures.py')
    fixtures=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixtures)
    fixtures.components=components
    cwd=os.getcwd()
    try:
        with quiet_git():
            result=fixtures.main()
    finally:os.chdir(cwd)
    assert result==0,result
    measured=json.loads((a.output/'matrix.json').read_bytes())['rows']
    published=json.loads((root/'public/author/public/rawlogs/fixture-matrix.json').read_bytes())['rows']
    assert len(measured)==len(published)==31
    for actual,expected in zip(measured,published):
        for key in ['scenario','branch_head','base_tip','expected']:
            assert actual[key]==expected[key],(key,actual,expected)
    print('PASS: 31 exact public head/tip pairs and expectations reproduced; original 145 assertions preserved.')
