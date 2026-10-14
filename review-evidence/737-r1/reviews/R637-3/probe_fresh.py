#!/usr/bin/env python3
"""Reproduce fresh inventory preparation and synthetic-union collection only."""
import json
import os
from pathlib import Path
import subprocess
import sys

HEAD = '84ee9ea119b548b4982d2c0988d8753a2ce4d0cf'

def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    work = out / 'scratch' / 'fresh-checkout'
    env = {**os.environ, 'TMPDIR': str(out / 'scratch'), 'PYTHONDONTWRITEBYTECODE': '1'}
    def run(args, cwd=work):
        return subprocess.check_output(args, cwd=cwd, env=env, text=True, stderr=subprocess.STDOUT)
    print(run(['git', 'clone', '--shared', '--no-checkout', str(root), str(work)], out), flush=True)
    print(run(['git', 'checkout', '--detach', HEAD]), flush=True)
    initial = run(['git', 'submodule', 'status'])
    assert all(line.startswith('-') for line in initial.splitlines())
    print('All submodules initially absent', flush=True)
    sys.path.insert(0, str(work / 'scripts'))
    from ci_suite_workflows import inventory_dependencies
    preparation = inventory_dependencies()['run']
    print(run(['bash', '-eu', '-c', preparation]), flush=True)
    from ci_suite_pieces import inventory, PIECE_SECONDS
    from ci_runtime_evidence import collect
    from ci_manifest import compare
    tree = run(['git', 'rev-parse', 'HEAD^{tree}']).strip()
    artifacts = out / 'scratch' / 'fresh-artifacts'
    artifacts.mkdir()
    counts = {}
    for suite in PIECE_SECONDS:
        names = inventory(suite, work)
        counts[suite] = len(names)
        directory = artifacts / suite
        directory.mkdir()
        # These are schema fixtures, never records of suite execution.
        receipt = {'suite': suite, 'head': HEAD, 'tree': tree, 'inventory': names,
                   'legs': [{'shard': '0/1', 'cases': names}], 'union': 'pass',
                   'verdicts_sha256': 'a' * 64}
        (directory / 'union.json').write_text(json.dumps(receipt))
    event = out / 'scratch' / 'fresh-event.json'
    event.write_text(json.dumps({'repository': {'full_name': 'fixture/project'}}))
    os.environ.update(GITHUB_EVENT_PATH=str(event), GITHUB_EVENT_NAME='push',
                      GITHUB_REPOSITORY='fixture/project', ACT='true')
    document = collect(artifacts, out / 'scratch' / 'fresh-manifest.json', [])
    assert set(document['payload']['inventories']) == set(PIECE_SECONDS)
    assert not document['complete']
    try:
        compare(document, document)
    except ValueError:
        pass
    else:
        raise AssertionError('synthetic collection authenticated')
    result = {'head': HEAD, 'tree': tree, 'initial_submodules': initial.splitlines(),
              'prepared_submodules': run(['git', 'submodule', 'status']).splitlines(),
              'preparation': preparation, 'inventories': counts, 'complete': document['complete'],
              'scope': 'Fresh dependency preparation and synthetic union transport; no suite execution claim.'}
    (out / 'fresh-result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
