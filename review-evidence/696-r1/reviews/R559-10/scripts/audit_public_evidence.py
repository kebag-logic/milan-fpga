#!/usr/bin/env python3
"""Audit selected published author receipts, without running the author's banks."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
revision = 'dd8350f0d648656904188e490ecff933024bff0c'
prefix = 'review-evidence/696-r1/author-r13/merge-dev-e81ce82f-receipts/'
def read(name):
    return subprocess.check_output(['git', 'show', revision+':'+prefix+name], cwd=source)
manifest = dict((line.split('  ',1)[1], line.split('  ',1)[0])
                for line in read('MANIFEST-01.sha256').decode().splitlines())
names = ['final-provenance.json', 'native/final-results.json', 'sharding-result.json',
         'maap-ceiling.json', 'maap-campaign-result.json', 'resource-comparison.json',
         'resource-results.json', 'candidate-route-check.log', 'dev-route-check.log',
         'builder-limitation.json', 'source-inputs.json', 'shard-provenance.json',
         'native/shards/1/logs/maap.log', 'native/maap-integration.log',
         'native/maap-coverage.log', 'maap-ooc-candidate/util_hier_base.rpt',
         'shipping-candidate/ax7101/gateware/baseline_utilization.rpt',
         'shipping-candidate/ax7101/gateware/alinx_ax7101_route_status.rpt',
         'candidate-ooc-1x1-check.log', 'candidate-ooc-8x8-check.log']
for name in names:
    data = read(name)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == manifest[name], name
    target = packet/'receipts/public-author'/name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print('PASS published manifest', name, digest)
provenance = json.loads(read('final-provenance.json'))
assert provenance['head'] == '313616d1a18549d41907db389d378f0beb9bc543'
assert provenance['tree'] == '8eb5d868bfac1973ba1d82b0665aabae07d9494c'
matched, dev_matched, generated = 0, 0, []
for shape in json.loads(read('source-inputs.json')):
    for item in shape['files']:
        path = item['path']
        if path.startswith('$WORK/candidate/'):
            relative = path.removeprefix('$WORK/candidate/')
            f = source / relative
            if f.is_file():
                data = f.read_bytes()
                assert hashlib.sha256(data).hexdigest() == item['sha256'], relative
                assert len(data) == item['size'], relative
                matched += 1
            else:
                generated.append(path)
        elif path.startswith('$WORK/dev/'):
            relative = path.removeprefix('$WORK/dev/')
            repo, ref, leaf = source, 'e81ce82f', relative
            for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
                if relative.startswith(sub+'/'):
                    ref = subprocess.check_output(['git','rev-parse','e81ce82f:'+sub], cwd=source).decode().strip()
                    repo, leaf = source/sub, relative.removeprefix(sub+'/')
                    break
            result = subprocess.run(['git','show',ref+':'+leaf], cwd=repo, capture_output=True)
            if result.returncode:
                generated.append(path)
            else:
                assert hashlib.sha256(result.stdout).hexdigest() == item['sha256'], relative
                assert len(result.stdout) == item['size'], relative
                dev_matched += 1
        else:
            generated.append(path)
print('PASS source receipts identify requested head/tree')
print('PASS measured input file hashes compared with candidate checkout:', matched)
print('PASS measured dev input hashes compared with git objects:', dev_matched)
print('Generated/external inputs not reproduced by reviewer:', len(generated))
for path in generated:
    print('NOT REGENERATED', path)
log = read('native/shards/1/logs/maap.log')
campaign = json.loads(read('maap-campaign-result.json'))
publication = json.loads(subprocess.check_output(['git','show',revision+':review-evidence/696-r1/MANIFEST.json'], cwd=source))
entry = next(row for row in publication if row['file'] == 'author-r13/merge-dev-e81ce82f-receipts/native/shards/1/logs/maap.log')
assert hashlib.sha256(log).hexdigest() == entry['published_sha256']
if campaign['log_sha256'] != entry['original_sha256']:
    print('LIMIT: campaign summary digest does not identify the published MAAP log')
    print('Summary log_sha256:', campaign['log_sha256'], 'log_bytes:', campaign['log_bytes'])
    print('Published log_sha256:', entry['published_sha256'], 'log_bytes:', len(log))
    print('Use the two matching publication manifests for published bytes; no raw-log identity inferred.')
else:
    print('PASS campaign summary and published log hash agree')
assert b'KL_maap: 186 checks, 0 failures' in log
assert log.count(b'named rejection:') == 63
assert b'checks: 65   failures: 0' in log
print('PASS author MAAP log: 186 clean checks, 63 named defects, 2 controls')
raw = read('maap-ooc-candidate/util_hier_base.rpt').decode()
row = next(line for line in raw.splitlines() if '|   g_maap.maap_engine ' in line)
print('AUTHOR MEASUREMENT', row.strip())
print('Author source execution only; no manager source bank is asserted.')
