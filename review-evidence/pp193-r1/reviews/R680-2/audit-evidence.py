#!/usr/bin/env python3
"""Recompute area and audit public return codes; requires fetch-evidence.py first."""
from pathlib import Path
import hashlib, json, re, shutil
root=Path(__file__).resolve().parent
p=root/'scratch/evidence/author-r2/receipts/round2'
lines=[]
areas={}
for rev in ['main','base','head']:
    line=next(s for s in (p/f'ooc/{rev}/ooc_pp_shadow.log').read_text().splitlines() if s.startswith('KL_pp_shadow'))
    areas[rev]=list(map(int,line.split()[1:]));lines.append(rev+': '+line)
assert areas['head'][0]-areas['main'][0]==1335
assert areas['head'][3]-areas['main'][3]==618
assert areas['head'][0]-areas['base'][0]==812
assert areas['head'][3]-areas['base'][3]==568
assert all(areas['main'][i]==areas['base'][i]==areas['head'][i] for i in [1,4,5,6,7])
lines.append('PASS main->head +1335 LUT +618 FF; base->head +812 LUT +568 FF; LUTRAM/RAMB36/RAMB18/DSP/CARRY4 unchanged')
stats={}
for rev in ['6ddfcda4','c7c8825f','57fb7dd2']:
    txt=(p/f'area-listener/w-{rev}-8/stat.txt').read_text()
    lut=sum(int(n) for n in re.findall(r'^\s*(\d+)\s+LUT[1-6]\s*$',txt,re.M))
    ff=sum(int(n) for n in re.findall(r'^\s*(\d+)\s+FDRE\s*$',txt,re.M))
    stats[rev]=(lut,ff);lines.append(f'Listener 8 sinks {rev}: LUT={lut} FF={ff}')
assert stats['c7c8825f'][0]-stats['6ddfcda4'][0]==2251
assert stats['57fb7dd2'][0]-stats['6ddfcda4'][0]==322
lines.append('PASS commit-4 listener cost reduction: 2251 -> 322 incremental LUT (1929 removed); historical pre-fix characterization, not a passing head gate')
for area in ['gates','campaigns','consumers','ooc']:
    for f in sorted((p/area).glob('*/*.rc')):
        rc=int(f.read_text());expected=1 if f.name=='submodule_docs.rc' else 0
        assert rc==expected,str(f)
        lines.append(f'rc={rc} {f.relative_to(p)}'+(' (known baseline pin-doc mismatch)' if expected else ''))
campaign=(p/'campaigns/head/srp_top.log').read_text()
for name,tags in [('listener-parked-outside-groups',['SH10','SH11','SH12','SH13','SH14','SH15','SH16','SW4','SW5','SW6','SW7']),('listener-settle-skips-leave-copies',['SH10','SH11','SH12','SH13','SH14','SH15','SW4','SW5','SW6','SW7']),('listener-merge-keeps-park',['SH10','SH11','SH12','SH13']),('listener-retire-skips-group-mark',['SH15']),('listener-park-drops-matcher-pairs',['SH16'])]:
    found=[s for s in campaign.splitlines() if s.startswith(name+':')]
    assert found and all(' KILLED ' in s for s in found)
    alltags=set(','.join(s.split('tags=')[1] for s in found).split(','))
    assert set(tags)<=alltags
    lines.extend(found)
assert '203 checks: 203 PASS, 0 FAIL' in campaign
assert 'assertion coverage: 124/124; missing=[]' in campaign
lines.append('PASS named controls cover every SH10-SH16 and SW4-SW7 check; 203/203, coverage 124/124')
out=root/'public-receipts';out.mkdir(exist_ok=True)
selected=[]
for pat in ['gates/*/*.rc','gates/*/tools.txt','gates/*/run_suites.log','gates/final/*.log','campaigns/head/*.log','campaigns/*/*.rc','campaigns/head/RUNNER.txt','head-extra/*.log','head-extra/*.rc','consumers/*/*.rc','consumers/*/STATE.txt','consumers/head/submodule_docs.log','consumers/head/test_builder.log','compare/**/*.txt','compare/**/*.csv','ooc/*/ooc_pp_shadow.log','ooc/*/rom_digests.rows.diff','area-listener/w-*-8/stat.txt','scripts/chain_h*.sh','scripts/chain_cons2.sh','scripts/chain_final.sh','scripts/run_camps.sh','scripts/run_extra.sh','scripts/run_ooc.sh','repo-record.txt','scope-ports.txt','EXTERNAL-RECORDS.csv']:
    selected.extend(p.glob(pat))
selected.extend((p/'campaigns/head/work/srp_top').glob('listener-*park*.log'))
for f in sorted(set(selected)):
    if not f.is_file():continue
    rel=f.relative_to(p);dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
(root/'evidence-audit.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[:8]));print('Return codes, controls and area verified; selected raw receipts copied.')
