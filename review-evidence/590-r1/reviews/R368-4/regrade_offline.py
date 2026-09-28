#!/usr/bin/env python3
"""Regrade every published merge-dev service log with the exact head's grader.

Usage: regrade_offline.py <evidence 590-r1 dir> <repo at exact head> <out.json>
Build-free: it cannot check build binding (no build directory is published),
but it applies the head's run.grade / run.service_findings / run.report_verdict
to the published raw logs, checks the log bytes against the receipt's
log_sha256 and the published service log, and compares every graded field
(rows, heartbeat, liveness, phy, service_findings) with the receipt.
It also grades the no-publish control's named simulation finding.
"""
import contextlib, gzip, hashlib, io, json, sys
from pathlib import Path

base, repo, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo / 'tb/verilator/fw_service_budget'))
import run  # the head's grader

PK = base / 'author-mergedev'
ARTS = {a['name'].removesuffix('.gz'): a for a in json.loads((PK / 'native-artifacts.json').read_text())}

def load(name):
    a = ARTS[name]
    for s in a['stored']:
        p = PK / s['path']
        if p.is_file():
            d = p.read_bytes()
            d = gzip.decompress(d) if p.suffix == '.gz' else d
            break
        rel = s['path'].removesuffix('.gz')
        d = next((c.read_bytes() for c in (PK / 'raw' / rel,) if c.is_file()), None)
        if d is not None:
            break
    assert hashlib.sha256(d).hexdigest() == a['raw_sha256'], name
    return d

MUT = {'remove-dispatch': 'remove-dispatch', 'late-sample': 'late-sample'}
report, fails = {}, []
for name in sorted(n for n in ARTS if n.endswith('-receipt.json')):
    stem = name.removesuffix('-receipt.json').removeprefix('service-')
    mutation = next((m for m in MUT if stem.startswith(m)), 'none')
    rec = json.loads(load(name))
    raw = rec['raw_log']
    log = load('service-' + stem + '-raw.log').decode()
    wrapper = load('service-' + stem + '.log').decode()
    checks = dict(log_sha=hashlib.sha256(raw.encode()).hexdigest() == rec['log_sha256'],
                  published_log_equal=(log == raw))
    checks['wrapper_pass_line'] = any(l.startswith('PASS: ') for l in wrapper.splitlines())
    res = dict(rec)
    for k in ('rows', 'events', 'heartbeat_max_gap_ms', 'heartbeat_500ms_met', 'budget_findings',
              'heartbeat', 'liveness', 'service_findings', 'phy'):
        res.pop(k, None)
    graded = run.grade(raw, rec['media'])
    res.update(graded)
    res['service_findings'] = run.service_findings(res, raw)
    for k in ('rows', 'heartbeat_max_gap_ms', 'heartbeat_500ms_met', 'budget_findings',
              'heartbeat', 'liveness', 'service_findings', 'phy'):
        checks['equal_' + k] = res.get(k) == rec.get(k)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            run.report_verdict(mutation, res['service_findings'], False)
        verdict = 'rc0'
    except RuntimeError as e:
        verdict = 'REFUSED: ' + str(e)
    checks['verdict_rc0'] = verdict == 'rc0'
    f = res['service_findings']
    summary = dict(mutation=mutation, plan=rec['media']['plan'], shape=rec['shape'], verdict=verdict,
                   verdict_text=buf.getvalue().strip().splitlines()[-1] if buf.getvalue().strip() else '',
                   n_findings=len(f), per_line=sum(x.startswith('console line lacks') for x in f),
                   backing_lost='continuous backing lost' in f,
                   heartbeat_max_gap_ms=res['heartbeat_max_gap_ms'],
                   max_transaction_ms=res['phy']['max_transaction_sys_cycles'] / 100_000,
                   max_poll_ms=res['phy']['max_poll_sys_cycles'] / 100_000,
                   edges=(res['phy']['down_edges'], res['phy']['up_edges']),
                   worst_phy_bound_ms=max(r.get('phy_publication_bound_ms', 0) for r in res['rows']),
                   checks=checks)
    report[stem] = summary
    ok = all(checks.values())
    if not ok:
        fails.append(stem)
    print(f"{stem:40s} {'OK ' if ok else 'BAD'} {verdict:6s} findings={len(f):5d} per_line={summary['per_line']:5d} "
          f"gap={summary['heartbeat_max_gap_ms']:.5f} mdio={summary['max_transaction_ms']:.5f} "
          f"poll={summary['max_poll_ms']:.5f} edges={summary['edges']} phybound={summary['worst_phy_bound_ms']:.5f}")
# no-publish control: the native simulation itself must name the missing publication.
np_log = load('service-no-publish-all-raw.log').decode()
np_wrap = load('service-no-publish-all.log').decode()
np_ok = ('missing MDIO/publication evidence' in np_log
         and 'PASS: missing publication caught by target simulation' in np_wrap)
report['no-publish-all'] = dict(named_finding_present=np_ok)
print('no-publish-all named simulation finding present:', np_ok)
if not np_ok:
    fails.append('no-publish-all')
positives = [v for k, v in report.items() if v.get('mutation') == 'none']
agg = dict(positive_runs=len(positives),
           positive_findings=sum(v['n_findings'] for v in positives),
           largest_gap_ms=max(v['heartbeat_max_gap_ms'] for v in positives),
           largest_mdio_ms=max(v['max_transaction_ms'] for v in positives),
           largest_poll_ms=max(v['max_poll_ms'] for v in positives))
report['_aggregate'] = agg
print('AGGREGATE', agg)
json.dump(report, open(out, 'w'), indent=1)
print('RESULT', 'FAIL ' + ' '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
