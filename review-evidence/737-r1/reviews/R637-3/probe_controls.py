#!/usr/bin/env python3
"""Exercise guard removal in memory without modifying the reviewed checkout."""
import concurrent.futures
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

MUTATIONS = {
    'S1': ('ci_case_receipts', 'ci_case_receipts_selftest',
           'outcome not in ("pass", "caught")', 'outcome not in ("pass", "caught", "failed")',
           'receipt control accepted: changed result outcome'),
    'S2': ('ci_manifest', 'ci_manifest_selftest',
           'observed["outcome"] != "success" or observed["skip_reason"] is not None',
           'observed["outcome"] not in ("success", "skipped") or observed["skip_reason"] is not None',
           'skipped-step collections accepted'),
    'S4': ('ci_gate_receipts', 'ci_gate_workflows_selftest',
           'len(scopes) != 1 or ', '', 'accepted individually valid mixed execution scopes'),
}

def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    if len(sys.argv) > 2:
        sys.path.insert(0, str(root / 'scripts'))
        module, test, old, new, expected = MUTATIONS[sys.argv[2]]
        loaded = importlib.import_module(module)
        source = (root / 'scripts' / (module + '.py')).read_text()
        assert source.count(old) == 1
        exec(compile(source.replace(old, new), '<guard-removal-' + sys.argv[2] + '>', 'exec'), loaded.__dict__)
        return importlib.import_module(test).main()
    def run(name):
        env = {**os.environ, 'TMPDIR': str(out / 'scratch'), 'PYTHONDONTWRITEBYTECODE': '1'}
        result = subprocess.run([sys.executable, __file__, str(root), name], cwd=root,
                                env=env, capture_output=True, text=True, timeout=120)
        (out / ('mutation-' + name + '.log')).write_text(result.stdout + result.stderr)
        caught = result.returncode != 0 and MUTATIONS[name][4] in result.stderr
        return name, {'rc': result.returncode, 'caught_at_expected_assertion': caught,
                      'removed': MUTATIONS[name][2], 'replacement': MUTATIONS[name][3]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = dict(pool.map(run, MUTATIONS))
    print(json.dumps(results, indent=2))
    (out / 'mutation-results.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(not all(row['caught_at_expected_assertion'] for row in results.values()))

if __name__ == '__main__':
    raise SystemExit(main())
