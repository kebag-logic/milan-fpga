#!/usr/bin/env python3
"""Regrade committed receipts' raw logs with a given run.py; compare to committed rows.

Usage: regrade_check.py <harness-dir-containing-run.py> <repo-root>
Prints per-receipt: log digest check, row equality, differing fields, budget findings.
Exit 0 if every receipt regrades to identical rows and findings, else 1.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

harness, repo = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location('run_under_test', harness / 'run.py')
mod = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(harness))
spec.loader.exec_module(mod)
ok = True
for shape in ('1X1', '8X8'):
    rec = json.loads((repo / f'docs/findings/397_SERVICE_BUDGET_{shape}.json').read_text())
    raw = rec['raw_log']
    digest_ok = hashlib.sha256(raw.encode()).hexdigest() == rec['log_sha256']
    try:
        res = mod.grade(raw, rec['media'])
    except Exception as exc:  # a mutation may break grading outright
        print(f'{shape}: digest_ok={digest_ok} GRADE-ERROR {type(exc).__name__}: {exc}')
        ok = False
        continue
    same = res['rows'] == rec['rows'] and res['budget_findings'] == rec['budget_findings']
    ok &= same and digest_ok
    print(f'{shape}: digest_ok={digest_ok} rows_identical={res["rows"] == rec["rows"]} '
          f'findings_identical={res["budget_findings"] == rec["budget_findings"]} findings={res["budget_findings"]}')
    if not same:
        for a, b in zip(res['rows'], rec['rows']):
            d = {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)}
            if d:
                print(f'   {b["duty"]}: ' + ', '.join(f'{k}: got {v[0]} committed {v[1]}' for k, v in sorted(d.items())))
        if len(res['rows']) != len(rec['rows']):
            print(f'   row count got {len(res["rows"])} committed {len(rec["rows"])}')
sys.exit(0 if ok else 1)
