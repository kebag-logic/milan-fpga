#!/usr/bin/env python3
"""Inject read outages through production entry points without network or writes."""
import copy
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
from urllib.error import HTTPError

def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / 'scripts'))
    import ci_runtime_evidence as runtime
    import ci_fail_fast as fast
    from ci_manifest import compare
    from ci_workflow_plan import committed_plan, workflow
    source = committed_plan(root, '84ee9ea119b548b4982d2c0988d8753a2ce4d0cf')
    graph = workflow((root / '.github/workflows/rtl.yml').read_text())['jobs']
    assert graph['ci-manifest']['timeout-minutes'] * 60 > fast.RETRY_BUDGET_SECONDS
    assert graph['ci-cancel-tail']['needs'] == ['ci-fail-fast', 'ci-manifest']
    observe_step = next(s for s in graph['ci-fail-fast']['steps'] if s.get('id') == 'ci_observe')
    expected = set(json.loads(observe_step['env']['EXPECTED_JOBS']))
    skipped = json.loads(observe_step['env']['SKIPPED_MATRICES'])
    work = out / 'scratch' / 'observer-probe'
    work.mkdir(exist_ok=True)
    event = {'repository': {'full_name': 'fixture/project'}}
    (work / 'event.json').write_text(json.dumps(event))
    env = {'GITHUB_EVENT_NAME': 'push', 'GITHUB_EVENT_PATH': str(work / 'event.json'),
           'GITHUB_REPOSITORY': 'fixture/project', 'GITHUB_RUN_ID': '1', 'GITHUB_SHA': source['head'],
           'GH_TOKEN': 'fixture', 'GITHUB_OUTPUT': str(work / 'outputs'), 'ACT': 'false',
           'EXPECTED_JOBS': observe_step['env']['EXPECTED_JOBS'],
           'SKIPPED_MATRICES': observe_step['env']['SKIPPED_MATRICES']}
    outcomes = []
    for kind in (403, 429, 500, 502, 503, 'timeout', 'exhaustion'):
        error = (TimeoutError('injected timeout') if kind == 'timeout' else
                 HTTPError('fixture', 429 if kind == 'exhaustion' else kind, 'injected',
                           {'Retry-After': '601' if kind == 'exhaustion' else '240'}, None))
        for role in ('collector', 'watcher'):
            clock = [1000.0]
            (work / 'outputs').unlink(missing_ok=True)
            def sleep(seconds):
                clock[0] += seconds
            argv = (['reader', 'collect', '--run', '1', '--artifacts', str(work / 'absent'),
                     '--output', str(work / 'manifest.json')] if role == 'collector' else ['observer', 'watch'])
            with patch.dict(os.environ, env), patch.object(sys, 'argv', argv), \
                    patch('ci_fail_fast.urlopen', side_effect=error) as requests, \
                    patch('ci_fail_fast.time.monotonic', side_effect=lambda: clock[0]), \
                    patch('ci_fail_fast.time.time', side_effect=lambda: clock[0]), \
                    patch('ci_fail_fast.time.sleep', side_effect=sleep):
                rc = runtime.main() if role == 'collector' else fast.main()
            assert rc == 0
            assert (work / 'outputs').read_text() == 'observer_error=true\n'
            assert all(c.args[0].method == 'GET' for c in requests.call_args_list)
            job = 'ci-manifest' if role == 'collector' else 'ci-fail-fast'
            assert not fast.tail_failed({job: {'result': 'success', 'outputs': {'observer_only_error': 'true'}}})
            if role == 'collector':
                document = json.loads((work / 'manifest.json').read_text())
                assert not document['complete']
                assert set(document['payload']['results'].values()) == {'unknown'}
                try:
                    compare(document, document)
                except ValueError:
                    pass
                else:
                    raise AssertionError('observer outage accepted as equivalent')
            outcomes.append({'role': role, 'injection': kind, 'rc': rc, 'virtual_seconds': clock[0] - 1000,
                             'requests': requests.call_count, 'writes': 0})
    # An observer's successful job conclusion cannot erase its explicit gap.
    artifacts = work / 'watcher-artifacts'
    artifacts.mkdir(exist_ok=True)
    key = '.github/workflows/rtl.yml:ci-fail-fast'
    receipt = {'head': source['head'], 'tree': source['tree'], 'workflow': '.github/workflows/rtl.yml',
               'job': 'ci-fail-fast', 'matrix': {}, 'result': 'success', 'tools': {},
               'steps': {'ci_observe': {'outcome': 'success', 'conclusion': 'success',
                                        'outputs': {'observer_error': 'true'}}}}
    (artifacts / 'job-evidence.json').write_text(json.dumps(receipt))
    with patch.dict(os.environ, env), patch.object(runtime, 'collect_api', return_value=({}, {key: 'success'})):
        document = runtime.collect(artifacts, work / 'watcher-manifest.json', [1])
    assert document['payload']['results'][key] == 'unknown' and not document['complete']
    # Each terminal evidence failure still takes the actual cancellation path.
    for job in ('ci-manifest', 'ci-fail-fast'):
        for result in fast.FAILURES:
            needs = {job: {'result': result, 'outputs': {'observer_only_error': 'false'}}}
            posted = []
            def request(path, method='GET'):
                posted.append((path, method))
                return {}
            siblings = [{'id': 2, 'head_sha': source['head'], 'path': '.github/workflows/docs.yml',
                         'head_repository': {'full_name': 'fixture/project'}, 'status': 'in_progress'}]
            with patch.dict(os.environ, {**env, 'CI_TAIL_NEEDS': json.dumps(needs)}), \
                    patch.object(sys, 'argv', ['tail', 'tail']), \
                    patch.object(fast.API, 'pages', return_value=siblings), \
                    patch.object(fast.API, 'request', side_effect=request):
                assert fast.main() == 0
            assert posted == [('runs/2/cancel', 'POST'), ('runs/1/cancel', 'POST')]
    raw = [{'name': name, 'status': 'completed', 'conclusion': 'skipped', 'steps': []} for name in skipped]
    path = '.github/workflows/rtl.yml'
    execution, results = runtime.api_evidence(source, raw, path)
    assert set(results.values()) == {'skipped'}
    assert all(s['outcome'] == 'skipped' for steps in execution.values() for s in steps)
    for field, value in [('name', 'unknown'), ('status', 'in_progress'), ('conclusion', 'failure'),
                         ('conclusion', 'success'), ('steps', [{'name': 'invented'}])]:
        changed = copy.deepcopy(raw)
        changed[0][field] = value
        for reader in (lambda: runtime.api_evidence(source, changed, path),
                       lambda: fast.observe(changed, expected, skipped)):
            try:
                reader()
            except ValueError:
                pass
            else:
                raise AssertionError('malformed raw observation accepted')
    for order in (False, True):
        expanded = {'name': skipped[raw[0]['name']][0], 'status': 'completed', 'conclusion': 'skipped', 'steps': []}
        changed = [expanded, *raw] if order else [*raw, expanded]
        for reader in (lambda: runtime.api_evidence(source, changed, path), lambda: fast.observe(changed, expected, skipped)):
            try:
                reader()
            except ValueError:
                pass
            else:
                raise AssertionError('overlap accepted')
    (out / 'observer-results.json').write_text(json.dumps({'outages': outcomes, 'genuine_tail_failures': 8,
                'raw_matrix_negative_forms': 7, 'raw_expanded_legs': len(results)}, indent=2) + '\n')
    print('PASS: 14 observer outages, 8 genuine tail failures, malformed/overlap controls')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
