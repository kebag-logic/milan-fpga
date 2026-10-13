#!/usr/bin/env python3
"""Record before/after shipping-scope decisions on synthetic and historical Git trees."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import yaml

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'scripts'))
from ci_scope_history import execute, git, history, merge_checkout, scope_script

old = '33ac35b54648ef919227c5dd8b9abc97fa6bedbd'
rows = []
steps = [('rtl.yml', 'full-ci-gate', 'gate'), ('rtl-fast.yml', 'changes', 'scope'),
         ('elaborate.yml', 'elaborate', 'scope')]
old_scripts = {}
for wf, job, step in steps:
    source = subprocess.check_output(['git', '-C', str(repo), 'show',
                                      f'{old}:.github/workflows/{wf}'], text=True)
    doc = yaml.safe_load(source)
    body = next(s['run'] for s in doc['jobs'][job]['steps'] if s.get('id') == step)
    old_scripts[wf] = body.replace('python3 scripts/ci_scope.py --selftest', ':')
with tempfile.TemporaryDirectory(prefix='r3-table-') as raw:
    root = Path(raw)
    cases = history(root, repo)
    for wf, job, step in steps:
        body = scope_script(repo, wf, job, step)
        for case in cases:
            merge = merge_checkout(root, case)
            before_hosted = execute(root, old_scripts[wf], case.recorded, case.head, merge)
            after_hosted = execute(root, body, case.recorded, case.head, merge)
            git(root, 'checkout', '--quiet', '--detach', case.head)
            git(root, 'update-ref', 'refs/remotes/origin/dev', case.live)
            before_replay = execute(root, old_scripts[wf], case.recorded, case.head, case.head,
                                    inputs={'ACT': 'true'})
            after_replay = execute(root, body, case.recorded, case.head, case.head,
                                   inputs={'ACT': 'true'})
            assert after_hosted == after_replay == (case.paths, case.rtl)
            rows.append(dict(workflow=wf, case=case.label, before_hosted=before_hosted,
                             after_hosted=after_hosted, before_replay=before_replay,
                             after_replay=after_replay))
with tempfile.TemporaryDirectory(prefix='r3-b16-table-') as raw:
    wt = Path(raw) / 'b16'
    subprocess.run(['git', '-C', str(repo), 'worktree', 'add', '--quiet', '--detach',
                    str(wt), '6c810c45ac4ac7d5b45797430753020c9ea31d86'], check=True)
    try:
        recorded, head = '49da9fd9', 'f1b2489f'
        merge = git(wt, 'rev-parse', 'HEAD')
        live = git(wt, 'rev-parse', 'HEAD^1')
        # Keep replay refs in an isolated fixture, leaving shared refs alone.
        copy = Path(raw) / 'head-copy'
        subprocess.run(['git', 'clone', '--quiet', '--shared', '--no-checkout', str(repo), str(copy)], check=True)
        git(copy, 'checkout', '--quiet', '--detach', head)
        git(copy, 'update-ref', 'refs/remotes/origin/dev', live)
        for tree in (wt, copy):
            (tree / 'scripts/ci_scope.py').write_bytes((repo / 'scripts/ci_scope.py').read_bytes())
        for wf, job, step in steps:
            body = scope_script(repo, wf, job, step)
            before_hosted = execute(wt, old_scripts[wf], recorded, head, merge)
            after_hosted = execute(wt, body, recorded, head, merge)
            before_replay = execute(copy, old_scripts[wf], recorded, head, head,
                                    inputs={'ACT': 'true'})
            after_replay = execute(copy, body, recorded, head, head,
                                   inputs={'ACT': 'true'})
            assert after_hosted == after_replay
            assert after_hosted == (['docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md',
                                     'docs/findings/README.md'], 'false')
            rows.append(dict(workflow=wf, case='B16 actual', live=live, merge=merge,
                             before_hosted=before_hosted, after_hosted=after_hosted,
                             before_replay=before_replay, after_replay=after_replay))
    finally:
        subprocess.run(['git', '-C', str(repo), 'worktree', 'remove', '--force', str(wt)], check=True)
print(json.dumps(rows, indent=2))
