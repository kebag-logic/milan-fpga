#!/usr/bin/env python3
"""R368-3 probe: verify the round-3 kept native evidence and regrade it with head code.

Usage: python3 -B kept_evidence_regrade.py <repo-root at head> <author-r3 packet dir> <archive MANIFEST.json>
1. Every artifact in native-artifacts.json: each stored part's size and SHA-256,
   reassembly (gunzip for .gz), raw size and SHA-256. Files under
   native-evidence-raw/ must equal the manifest's raw bytes of the same name.
2. Every kept service run: receipt log_sha256 and raw_log equal the kept raw
   log; receipt input_hashes equal head inputs(); then the head grading code
   (grade, service_findings, report_verdict) is re-run on the raw log with the
   receipt's media, exactly as run.py --regrade does after its build-hash
   check (the native build directories are not published, so that one check
   cannot be repeated), and rows/findings must equal the stored receipt.
3. no-publish control: raw log carries the named simulation failure.
4. Capture arms: head nvm_capture_cpu grading of each raw capture log equals the
   kept measurement and the committed receipt; byte-only control re-graded.
"""
from pathlib import Path
import contextlib
import gzip
import hashlib
import io
import json
import re
import sys

root = Path(sys.argv[1]).resolve()
pkt = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/fw_service_budget'))
import run as svc  # noqa: E402
sys.path.pop(0)
sys.modules.pop('run')
sys.path.insert(0, str(root / 'tb/verilator/nvm_capture_cpu'))
import run as cap  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
arts = json.loads((pkt / 'native-artifacts.json').read_text())
cmds = {c['name']: c for c in json.loads((pkt / 'native-commands.json').read_text())}
# The archive redacted local paths after the author hashed; its MANIFEST.json
# (argv[3]) records original and published SHA-256 per published file.
arch = {e['file'].split('author-r3/', 1)[1]: e for e in json.loads(Path(sys.argv[3]).read_text())
        if 'author-r3/' in e['file']}
raw = {}
bad = 0
counts = dict(exact=0, redacted_chain=0, gz_via_raw=0)
for item in arts:
    name = item['name']
    gz = name.endswith('.gz')
    stem = name[:-3] if gz else name
    paths = [st['path'] for st in item['stored']]
    if all((pkt / q).exists() for q in paths):
        parts = []
        for st in item['stored']:
            b = (pkt / st['path']).read_bytes()
            e = arch.get(st['path'])
            if e is None or sha(b) != e['published_sha256']:
                print('NOT PUBLISHED AS RECORDED', st['path']); bad += 1
            elif e['path_redacted']:
                if e['original_sha256'] != st['sha256']:
                    print('REDACTION CHAIN BROKEN', st['path']); bad += 1
                else:
                    counts['redacted_chain'] += 1
            elif len(b) != st['size'] or sha(b) != st['sha256']:
                print('STORED MISMATCH', st['path']); bad += 1
            else:
                counts['exact'] += 1
            parts.append(b)
        body = b''.join(parts)
        if gz:
            body = gzip.decompress(body)
        redacted = any(arch.get(q, {}).get('path_redacted') for q in paths)
        if not redacted and (len(body) != item['raw_size'] or sha(body) != item['raw_sha256']):
            print('RAW MISMATCH', name); bad += 1
    else:
        q = 'native-evidence-raw/' + Path(stem).name
        body = (pkt / q).read_bytes()
        e = arch.get(q)
        if not gz or e is None or e['path_redacted'] or sha(body) != e['published_sha256'] \
                or len(body) != item['raw_size'] or sha(body) != item['raw_sha256']:
            print('GZ-REPLACEMENT MISMATCH', name); bad += 1
        else:
            counts['gz_via_raw'] += 1
    raw[stem] = body
print(f'manifest: {len(arts)} artifacts; {counts}; mismatches={bad}')
rawdir = pkt / 'native-evidence-raw'
for f in sorted(rawdir.iterdir()):
    same = f.name in raw and raw[f.name] == f.read_bytes()
    kind = 'manifest-equal' if same else ('NOT IN MANIFEST' if f.name not in raw else 'DIFFERS')
    print(f'raw-dir {f.name}: {kind}')
    bad += 0 if same or f.name not in raw else 1

head_inputs = svc.inputs()
heads = sorted({c['head'] for c in cmds.values()})
print('native command heads:', heads)
for name in sorted(n for n in raw if n.startswith('service-') and n.endswith('-receipt.json')):
    stem = name[:-len('-receipt.json')]
    rec = json.loads(raw[name])
    log = raw[stem + '-raw.log']
    args = cmds[stem]['command']
    mutation = args[args.index('--mutation') + 1] if '--mutation' in args else 'none'
    enforce = '--enforce-service' in args
    rbf = '--record-budget-findings' in args
    ok_bind = rec['log_sha256'] == sha(log) and rec['raw_log'] == log.decode()
    ok_inputs = rec['input_hashes'] == head_inputs
    result = dict(media=rec['media'], shape=rec['shape'], raw_log=log.decode())
    result.update(svc.grade(log.decode(), rec['media']))
    findings_key = 'service_findings' if enforce else 'budget_findings'
    if enforce:
        result['service_findings'] = svc.service_findings(result, log.decode())
    same_rows = result['rows'] == rec['rows']
    same_find = result.get(findings_key) == rec.get(findings_key)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            svc.report_verdict(mutation, result.get(findings_key), rbf)
        verdict = 'PASS ' + buf.getvalue().strip().splitlines()[-1] if buf.getvalue().strip() else 'PASS'
    except Exception as exc:  # noqa: BLE001
        verdict = f'FAIL {exc}'
    fl = result.get(findings_key) or []
    per_line = sum(1 for x in fl if x.startswith('console line lacks a dispatch opportunity: '))
    lines = sum(1 for r in result['rows'] if 'command_index' in r)
    ticked = sum(1 for r in result['rows'] if 'command_index' in r and r.get('tick_calls', 0) > 0)
    gaps = [x for x in fl if 'gap' in x or 'backing' in x][:2]
    print(f'{stem}: mutation={mutation} plan={rec["media"]["plan"]} bind={ok_bind} inputs_eq_head={ok_inputs} '
          f'rows_eq={same_rows} findings_eq={same_find} findings={len(fl)} per_line={per_line} '
          f'lines={lines} ticked={ticked} verdict={verdict}')
    for g in gaps:
        print('    ', g)
    bad += 0 if (ok_bind and ok_inputs and same_rows and same_find and verdict.startswith('PASS')) else 1
np = raw['service-no-publish-all-raw.log'].decode()
print('no-publish named failure present:', 'missing MDIO/publication evidence' in np)

committed = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
n = 0
for short, mhz in (('1x1', 50), ('8x8', 50), ('8x8', 100)):
    for traffic in ('on', 'off'):
        nm = f'capture-{short}-{mhz}-{traffic}'
        spec = json.loads(raw[nm + '-sources.json'])
        text = raw[nm + '-raw.log'].decode()
        rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', ln))
                for ln in text.splitlines() if ln.startswith('CAPTURE index=')]
        m = cap.grade_rows(rows, spec)
        kept = json.loads(raw[nm + '.json'])
        match = [e for e in committed['measurements'] if (e['shape'], e['cpu_hz'], e['traffic']) == (m['shape'], m['cpu_hz'], m['traffic'])]
        eq = m == kept and len(match) == 1 and all(match[0][k] == v for k, v in m.items())
        n += len(rows)
        print(f'{nm}: captures={len(rows)} max_ms={m["maximum_ms"]} regrade_eq_kept_and_receipt={eq}')
        bad += 0 if eq else 1
text = raw['capture-byte-only-capture.log'].decode()
rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', ln)) for ln in text.splitlines() if ln.startswith('CAPTURE index=')]
bm = cap.grade_rows(rows, json.loads(raw['capture-byte-only-sources.json']))
base = json.loads(raw['capture-8x8-50-on.json'])
cap.grade_byte_only(bm, base)
print(f'byte-only: captures={len(rows)} min_ms={bm["minimum_ms"]} max_ms={bm["maximum_ms"]} '
      f'ratio={bm["minimum_ms"] / base["maximum_ms"]:.5f} (>1.5 required; grade_byte_only passed)')
for ctl in ('capture-skip-copy', 'capture-no-traffic'):
    ks = sorted(k for k in raw if k.startswith(ctl))
    print(ctl, 'artifacts:', ks)
print(f'total captures regraded={n}; overall problems={bad}')
