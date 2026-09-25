import hashlib
import json
from pathlib import Path
import sys

out = Path(__file__).resolve().parent
sys.path.insert(0,str(Path.cwd()/'scripts'))
from suite_tally import scan

names = ['sequential-cold','sequential-warm','pooled-cold','pooled-warm']
results = {name:json.loads((out/name/'result.json').read_text()) for name in names}
reference = results[names[0]]
reference_scan = scan((out/names[0]/'milan_dp.log').read_text())
report = {'runs':{},'pairs':{},'equivalence':{}}
for name, row in results.items():
    assert row['exit_code']==0, name
    assert row['head']==reference['head'], name
    assert row['cpus']==reference['cpus'], name
    assert row['headers_before']==row['headers_after']==reference['headers_before'], name
    assert row['runtime_inputs']==reference['runtime_inputs'], (name,'inputs')
    assert row['binaries']==reference['binaries'], (name,'executables')
    checks, failures, matched, unparsed, skipped = scan((out/name/'milan_dp.log').read_text())
    assert failures==0 and not unparsed, (name,failures,unparsed)
    assert checks==reference_scan[0] and len(matched)==len(reference_scan[2]), (name,'full tally')
    assert row['seconds'] < 3600, (name,'budget')
    assert (out/name/'replay.log').read_bytes()==(out/names[0]/'replay.log').read_bytes(), (name,'replay')
    captures = {}
    for capture in sorted((out/name).glob('[0-9][0-9]-*.log')):
        data = capture.read_bytes()
        assert data==(out/names[0]/capture.name).read_bytes(), (name,capture.name)
        leg_checks,leg_failures,leg_matched,leg_unparsed,leg_skipped = scan(data.decode())
        assert leg_failures==0 and not leg_unparsed
        captures[capture.name]=dict(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),checks=leg_checks,failures=leg_failures)
    assert len(captures)==11
    report['runs'][name]=dict(seconds=row['seconds'],checks=checks,failures=failures,tallies=len(matched),
                             skipped=skipped,peak_rss_kib=row['peak_rss_kib'],peak_ordinary=row['peak_ordinary'],
                             peak_exclusive=row['peak_exclusive'],captures=captures,
                             budget_seconds=3600,margin_seconds=3600-row['seconds'])
for temperature in ['cold','warm']:
    before=results['sequential-'+temperature]['seconds']
    after=results['pooled-'+temperature]['seconds']
    report['pairs'][temperature]=dict(before=before,after=after,saved_seconds=before-after,saved_percent=100*(before-after)/before)
report['equivalence']=dict(head=reference['head'],cpus=reference['cpus'],all_captures_identical=True,all_replays_identical=True,
                           all_inputs_identical=True,all_executables_identical=True,all_headers_unchanged=True)
(out/'benchmark-equivalence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pairs':report['pairs'],'equivalence':report['equivalence'],
                  'counts':{name:{k:v for k,v in row.items() if k!='captures'} for name,row in report['runs'].items()}},indent=2))
