#!/usr/bin/env python3
"""Check published source-head totals and retain their exact published receipts."""
import json, re, shutil, sys
from pathlib import Path
packet = Path(sys.argv[1])
root = packet/'scratch/public/author-r3/receipts/round3'
head = '220b51f2eb50c32f830e0b5a8ee1ce138b218bb6'
selected, shards, suites = [], [], []
for n in range(4):
    sub = root/f'sweep-220b51f2/shard-{n}/spec'
    res = json.loads((sub/'results.json').read_text())
    end = json.loads((sub/'complete.json').read_text())
    assert res['head'] == end['head'] == head and end['exit_code'] == 0
    assert all(r['exit_code'] == 0 for r in res['results'])
    text = (sub/'01.log').read_text()
    names = re.findall(r'^PASS\s+(\S+)',text,re.M)
    counts = re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)',text)
    checks = re.search(r'checks: (\d+)\s+in-suite failures: (\d+)',text)
    assert counts and checks
    assert int(counts[1]) == int(counts[2]) == len(names)
    assert int(counts[3]) == int(counts[4]) == int(checks[2]) == 0
    suites += names
    shards.append({'shard':n,'suites':len(names),'checks':int(checks[1]),'rc':0,
                   'skips':[s.strip() for s in text.splitlines() if 'SKIPPED' in s]})
    selected += [sub/'01.log',sub/'results.json',sub/'complete.json']
assert len(suites) == len(set(suites)) == 64
assert sum(s['checks'] for s in shards) == 2189668
docs = json.loads((root/'docs-220b51f2/receipts.json').read_text())
assert docs['head'] == docs['head_after'] == head
executed = [s for s in docs['steps'] if s['rc'] is not None]
skipped = [s for s in docs['steps'] if s['rc'] is None]
assert len(executed)==42 and len(skipped)==2
assert all(s['rc']==0 and s['make']=='GNU Make 4.3' for s in executed)
static = (root/'static-220b51f2/gates.tsv').read_text().splitlines()
assert len(static)==30 and all(s.split('\t')[1]=='0' for s in static)
assert (root/'static-220b51f2/HEAD.txt').read_text().startswith('head '+head+' ')
behave=(root/'gates-220b51f2/behave.log').read_text()
assert '406 scenarios passed, 0 failed, 0 skipped' in behave
selected += [root/p for p in [
    'docs-220b51f2/receipts.json','suites-220b51f2/avtp_rxmon.log','suites-220b51f2/env.txt',
    'suites-220b51f2/rc.txt','sweep-220b51f2/avtp_rxmon-tally.txt',
    'sweep-220b51f2/shard-3/logs/avtp_rxmon.log','gates-220b51f2/behave.log',
    'gates-220b51f2/behave.rc','gates-220b51f2/behave.env.txt',
    'static-220b51f2/gates.tsv','static-220b51f2/HEAD.txt','static-220b51f2/lint_rtl.log',
    'rtl-comment-only/comment-only.txt','probe_sq_claims/SUMMARY.txt']]
selected += list((root/'static-220b51f2').glob('*.log'))
selected += list((root/'docs-220b51f2/logs').glob('*.log'))
for source in set(selected):
    dest = packet/'published-receipts'/source.relative_to(root)
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,dest)
summary={'head':head,'attribution':'author source-head executions; no manager source bank',
         'shards':shards,'suites_total':64,'checks_total':2189668,'failures':0,
         'docs_executed':42,'docs_skipped':skipped,'static_gates':30,
         'lint':'89 <= 89','behave':'14 features, 406 scenarios, 1977 steps; zero failures/skips',
         'avtp_rxmon':'97+218+116+119+14+13 = 577 checks; zero failures',
         'selected_published_receipts':len(set(selected))}
(packet/'public-gate-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
