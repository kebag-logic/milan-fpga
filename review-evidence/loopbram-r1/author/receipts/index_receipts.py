import json,hashlib,gzip,sys
from pathlib import Path
out=Path('<home-path>/milan-fpga-management/2026-09-23/loopbram-a826/round2/receipts')
sys.path.insert(0,'<home-path>/milan-fpga-management/2026-09-23');import privacy
manifest=json.loads((out/'manifest.json').read_text())
for p in out.rglob('*.gz'):
 b=p.read_bytes();assert privacy.scrub_redact(b)==b
 data=gzip.decompress(b);assert privacy.scrub_redact(data)==data
lines=['# Round 2 receipts','',f"Candidate: `{manifest['head']}`. Local author evidence; no push or independent review verdict.",'','All compressed receipts and their decompressed payloads are unchanged by `privacy.scrub_redact`. Local roots are replaced by `$CHECKOUT` and `$SCRATCH`. Restore those placeholders before replaying archived Python or Tcl scripts. `manifest.json` records the compressed, redacted-payload and original-file SHA-256 values. Timing-report hashes inside `route-summary.json` refer to original files and match that manifest field. The manifest also records the gzip level: an alternate level may avoid an incidental binary-rule match in compressed bytes while preserving the independently scrubbed payload.','', '## Evidence map','', '| Evidence | Receipt |','|---|---|', '| Initial nine-cluster and 64/65-key probe | [topology_probe.json](topology_probe.json), [reproducer](topology_probe.py) |','| Current source and unchanged-input proof | [source identity](source_identity.json.gz), [head compatibility](head-compatibility.json.gz) |','| Disabled identity | [builder/image hashes](identity.json.gz), [SoC and initialization comparison](gateware-identity.json.gz) |','| Audio and controls | [regression summary](regression-summary.json.gz), [planted defects](wire-controls-summary.json.gz), [actual plant commands](mutants-head--results.json.gz) |','| Complete builder union | [union](builder-union--union.json.gz), [union log](builder-union--union.log.gz) |','| Physical sweep | [route summary](route-summary.json.gz), per-recipe Tcl, logs, utilization and corner reports below |','| Leaf comparison | [queue](leaf-queue-summary.json.gz), [capture and totals](leaf-capture-summary.json.gz) |','| S14 debt and unchanged allocator | [firmware memory](firmware-memory.json.gz), [measurement export](measure_soc.py.gz) |','| Portability | [run result](yosys--run.json.gz), [log](yosys--run.log.gz) |','', 'The complete builder union records one existing unrun row: historical Arty mf48 placement calibration, whose external report is absent. Mandatory elaboration and RV32 requirements pass. Earlier failing union attempts are preserved as history, not current-head verdicts. The initial receipt archive is [history/INDEX-initial.md](history/INDEX-initial.md); its hashes belong to its own retained files.','', '## Compressed files','', '| File | Role | Bytes | SHA-256 |','|---|---|---:|---|']
for r in manifest['receipts']:
 p=out/r['file'];b=p.read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 role='Earlier attempt' if 'builder-union-attempt' in r['file'] else 'Current packet'
 lines.append(f"| [{r['file']}]({r['file']}) | {role} | {r['bytes']} | `{r['sha256']}` |")
lines+=['','## Plain metadata','', '| File | SHA-256 |','|---|---|']
for name in ['manifest.json','topology_probe.py','topology_probe.json','issue-comment.json']:
 p=out/name
 if p.exists():lines.append(f"| [{name}]({name}) | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |")
p=out/'issue-comment.json'
if p.exists():
 d=json.loads(p.read_text())
 if d.get('url'):lines+=['',f"Public evidence: [issue #979 review-ready comment]({d['url']})."]
(out/'INDEX.md').write_text('\n'.join(lines)+'\n')
print('Indexed',len(manifest['receipts']),'compressed files; recursive privacy checks passed.')
