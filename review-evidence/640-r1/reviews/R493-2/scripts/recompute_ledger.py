#!/usr/bin/env python3
"""Independent arithmetic audit, reading committed resource records and both pages."""
import json
import math
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
base = '5603c353137e90c1fa95429f6d00ef7a2298d9ee'
record_path = 'syn/ooc/pp_resource_baseline.json'
raw = (repo / record_path).read_bytes()
assert raw == subprocess.check_output(['git', 'show', base+':'+record_path], cwd=repo)
eps = json.loads(raw)['endpoints']
route = eps['route-1x1']['record']
ooc = eps['ooc-1x1']['record']
docs = {p: (repo / 'docs/design' / p).read_text() for p in ['MARK_II_AREA_PLAN.md','AREA_BUDGET.md']}
checks = 0

def equal(got, expected, label):
    global checks
    assert got == expected, (label, got, expected)
    checks += 1

def rows(text):
    return [[re.sub(r'[`*]', '', c.strip()) for c in line.strip().strip('|').split('|')]
            for line in text.splitlines() if line.startswith('|')]

def row(text, key):
    found = [r for r in rows(text) if r[0] == key]
    assert len(found) == 1, (key, len(found))
    return found[0]

def nums(cells):
    return [float(c.replace(',', '').replace('+','')) for c in cells]

plan = docs['MARK_II_AREA_PLAN.md']
for ep in eps:
    f = eps[ep]['record']['figures']
    r = row(plan.split('| Endpoint | LUT |')[1].split('\n\n')[0], ep)
    equal(nums(r[1:3]), [f['LUT'], f['FF']], ep)
    equal(nums(r[4:8]), [f['RAMB36'], f['RAMB18'], f['BRAM_TILE'], f['DSP']], ep+' primitives')
    equal(nums(r[8].split('/')), [f['WNS_ns'], f['WHS_ns']], ep+' timing')
    equal(f['BRAM_TILE'], f['RAMB36'] + f['RAMB18']/2, ep+' tiles')
    digest=row(plan.split('| Endpoint | Input SHA-256 |')[1].split('\n\n')[0],ep)[1]
    equal(digest,eps[ep]['record']['inputs_sha256'],ep+' input digest')
    print(ep, json.dumps(f, sort_keys=True))

inventory = plan.split('### Current processor inventory')[1].split('## Baseline at dev')[0]
for r in rows(inventory):
    if r[0] not in route['scopes']:
        continue
    equal(nums(r[1:4]), [eps[e]['record']['scopes'][r[0]]['LUT'] for e in eps], 'scope '+r[0])

keys = ['u_pp/u_adp','u_pp/u_listener','u_pp/u_lsn_admit','u_pp/u_talker',
        'u_pp/u_originator','u_pp/u_nvm_shadow','u_pp/u_srp','u_pp/u_aecp',
        'u_pp/u_notify','u_pp/u_nvm_port','u_pp/u_nvm_arb','u_nvm']
assert not any(y.startswith(x+'/') for x in keys for y in keys if x != y)
sub = sum(ooc['scopes'][k]['LUT'] for k in keys)
equal(sub,17678,'disjoint removable LUT')
equal(sum(ooc['scopes'][k]['RAMB36']+ooc['scopes'][k]['RAMB18']/2 for k in keys),6.5,'disjoint RAM')
maap = 429 # Historical #686 measurement explicitly named by the plan.
gross = sub + maap
partial_keys = ['u_pp/u_adp','u_pp/u_listener','u_pp/u_lsn_admit','u_pp/u_talker','u_pp/u_nvm_shadow','u_pp/u_srp']
partial_gross = sum(ooc['scopes'][k]['LUT'] for k in partial_keys)+maap
equal(gross,18107,'full gross')
equal(partial_gross,8012,'partial gross')
equal(gross-partial_gross,10095,'retained AECP and NVM')
mailbox = 3102 # MAILBOX_SPLIT.md, F3 round 3 measured skeleton.
full = [math.floor((gross-mailbox-i+m)/100)*100 for i,m in [(2000,-1500),(1000,0),(500,1500)]]
partial = [partial_gross-mailbox-i+m for i,m in [(2000,-1500),(1000,0),(500,1500)]]
equal(full,[11500,14000,16000],'split range')
equal(partial,[1410,3910,5910],'partial range')
m8a = [math.floor((1696*p-d)/100)*100 for p,d in [(0.5,400),(0.75,250),(1,100)]]
census=(repo/'docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md').read_text()
equal(float(row(census,'DDR3 controller')[3].replace(',',''))+float(row(census,'DDR3 PHY')[3].replace(',','')),1696,'named DDR prepacking cells')
equal(float(row(census,'Anonymous LUT')[3].replace(',','')),3231,'unowned cells')
equal(nums(row(census,'BIOS ROM and SRAM')[5:7]),[18,1],'historical reusable CPU memory')
equal(m8a,[400,1000,1500],'M8a prepacking estimate')
lanes = [[100,200,400],[400,600,1000],[400,600,900],[300,500,700],m8a,[1300,1700,2200]]
remaining = [sum(x[i] for x in lanes) for i in range(3)]
equal(remaining,[2900,4600,6700],'remaining M lanes')
fabric = [1500+900,2600+1200,3600+1500]
start = route['figures']['LUT']
images = {'Full split':[start-full[i]-remaining[i] for i in range(3)],
          'No split, including M3/M10':[start-remaining[i]-fabric[i] for i in range(3)],
          'Partial, F5 unqualified':[start-partial[i]-remaining[i]-fabric[i] for i in range(3)]}
for name,values in images.items():
    for case,value in zip(['Conservative','Central','Optimistic'],values):
        for path,text in docs.items():
            r = [r for r in rows(text) if r[:2] == [name,case]]
            equal(len(r),1,path+' scenario row')
            equal(nums(r[0][2:]),[value,38040-value,37659-value],path+' '+name+' '+case)
        print(name,case,value,'headroom',38040-value,37659-value)

cumulative=[start]*3
table=plan.split('### Cumulative default-image estimates')[1].split('### No-split')[0]
for index,savings in enumerate([full,*lanes,[0,0,0]],1):
    cumulative=[v-s for v,s in zip(cumulative,savings)]
    r=row(table,str(index))
    equal(nums(r[3:]),[cumulative[1],cumulative[0],cumulative[2]],'cumulative '+str(index))
equal(images['Full split'][0]+1300,37167,'full without core')
equal(images['Partial, F5 unqualified'][1]+1700,39657,'partial without core')
m3=ooc['scopes']
own=m3['u_pp/u_aecp']['LUT']-sum(m3['u_pp/u_aecp/'+x]['LUT'] for x in ['u_d3','u_dyn','u_store','u_ucpu','u_resp'])
equal(own,1302,'M3 AECP own scope')
equal(m3['u_pp/u_dispatch/u_aecp_q']['LUT'],421,'M3 dispatch queue')
weighted=m3['u_pp/u_notify']['LUT']*.6+(m3['u_pp/u_aecp/u_d3']['LUT']+m3['u_pp/u_aecp/u_dyn']['LUT'])*.7+own*.5+421*.4
equal(round(weighted,1),3380.3,'M3 weighted displacement')

released=['u_pp/g_rx_pool['+str(i)+'].u_rx_slots' for i in [0,1,2,4,5]]
released += ['u_pp/u_mrp_strip','u_pp/u_tx_slots','u_pp/u_timer','u_pp/u_trace','u_pp/u_rx_validator','ctl_fifo']
storage=[sum(route['scopes'][k][kind] for k in released) for kind in ['RAMB36','RAMB18']]
equal(storage,[10,2],'conditional remaining wrapper release')
equal([route['scopes']['wrapper'][k] for k in ['RAMB36','RAMB18']], [storage[0]+6,storage[1]+1], 'whole wrapper disjoint partition')
memory = [[74,27,87.5,87.5],[-6,-1,-6.5,81],[1,10,6,87],[-18,-1,-18.5,68.5],[50,0,50,118.5],[2,0,2,120.5],[-10,-2,-11,109.5]]
for path,text in docs.items():
    block=text.split('| Item | RAMB36 delta |')[1].split('\n\n')[0]
    actual=[nums(r[1:]) for r in rows(block) if len(r)==5 and re.match(r'[+\-]?\d',r[1])]
    equal(actual,memory,path+' memory table')
    total=0
    for r in actual:
        equal(r[0]+r[1]/2,r[2],path+' tile conversion')
        total+=r[2]
        equal(total,r[3],path+' memory cumulative')
equal(135*.9,121.5,'reserve ceiling')
equal(sum([56948,3458,0,78744,8192])+18,147360,'preflight linked span')
pre=sum(r[2] for r in memory[:-1])
post=pre+memory[-1][2]
scenarios=[('pre-release',pre,120.5),('post-release',post,109.5),
           ('56 firmware tiles',post-50+224*1024/4096,115.5),
           ('no reuse pre',pre+18.5,139),('no reuse post',post+18.5,128),
           ('partial pre-release',pre+6,126.5)]
for label,value,expected in scenarios:
    equal(value,expected,label)
    print(label,'tiles',value,'allowance',121.5-value)
print('PASS',checks,'independent comparisons; estimates remain conditional, no physical measurement performed')
