#!/usr/bin/env python3
"""docs_steps.py CLONE BASE OUT: every gate command of .github/workflows/docs.yml's jobs (wire-accountability,
docs-check-no-git, docs-gates-0/1/2) on CLONE, one after the other, each with its rc and last line, in OUT/steps.txt;
each command's whole output in OUT/logs/. Python runs from the hash-locked Markdown venv of the tree's own lock
(md_venv.provide). Skipped, by name: installs and downloads (pip, apt, sv2v, the SDK install; the pinned tools are on
PATH), the CI-only recorders (ci_runtime_evidence record/identify, ci_gate_receipts record, ci_install_cache), and the
candidate's act_ci.py (AGENTS.md: its offline self-test runs only inside the disposable CI job). The em-dash gate takes
BASE; the no-git docs gate runs on a `git archive` export of CLONE's HEAD; the two end-station builder legs
(ci_builder_legs.py run 0 and 1) run as their own units (builder_leg.sh). Exit 0 when every step's rc is 0."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

clone, base, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
sys.path.insert(0, '<mgmt>/2026-09-23')
import md_venv  # noqa: E402

(out / 'logs').mkdir(parents=True, exist_ok=True)
bindir = out / 'bin'
bindir.mkdir(exist_ok=True)
venv = md_venv.provide(str(clone), 'HEAD', bindir)
env = dict(os.environ, PATH=f'{bindir}:{os.environ["PATH"]}')
wf = yaml.safe_load((clone / '.github/workflows/docs.yml').read_text())
SKIP = re.compile(r'^sudo |^command -v |pip install|apt-get|ci_runtime_evidence\.py|ci_gate_receipts\.py|ci_install_cache\.py --packages|'
                  r'ci_rv32_sdk\.py --destination|act_ci\.py|install_dir|trap |^(set|case|esac|fi|if|then|else|done|'
                  r'for|ver=|sha256=|url=|mkdir|archive=|echo|unzip|chmod|ln |export|cpus=|test |campaign=|'
                  r'simulations=|tool_build=|printf|\{|\}|: #|git submodule|git fetch|git cat-file|base=|;;|pull_request|'
                  r'push\)|\*\))')
steps = []
for job in ('wire-accountability', 'docs-check-no-git', 'docs-gates-0', 'docs-gates-1', 'docs-gates-2'):
    for s in wf['jobs'][job]['steps']:
        run = s.get('run') or ''
        joined = re.sub(r'\\\n\s*', ' ', run)
        for line in joined.splitlines():
            line = line.strip()
            if not line or SKIP.search(line):
                continue
            if line.startswith('python3 scripts/check_em_dash.py'):
                line = f'python3 scripts/check_em_dash.py --base {base}'
            if 'ci_builder_legs.py run' in line:
                continue  # the two end-station builder legs run as their own units (builder_leg.sh)
            if '--output "$RUNNER_TEMP/milan-hdl-reference"' in line:
                line = line.replace('"$RUNNER_TEMP/milan-hdl-reference"', str(out / 'hdl-reference'))
            if '"$RUNNER_TEMP/rv32-absent.jsonl"' in line:
                line = line.replace('"$RUNNER_TEMP/rv32-absent.jsonl"', str(out / 'rv32-absent.jsonl'))
            steps.append((job, line))
seen, uniq = set(), []
for job, line in steps:
    key = (job == 'docs-check-no-git', line)
    if key not in seen:
        seen.add(key)
        uniq.append((job, line))
export = out / 'nogit'
if export.exists():
    shutil.rmtree(export)
export.mkdir()
subprocess.run(f'git -C {clone} archive HEAD | tar -x -C {export}', shell=True, check=True)
rows, bad = [], 0
for k, (job, line) in enumerate(uniq):
    cwd = export if job == 'docs-check-no-git' else clone
    tag = f'{k:02d}-' + re.sub(r'[^A-Za-z0-9]+', '_', line.split('python3 ')[-1])[:48]
    r = subprocess.run(line, shell=True, cwd=cwd, env=env, capture_output=True, text=True)
    text = (r.stdout + r.stderr)
    (out / 'logs' / f'{tag}.log').write_text(f'$ {line}\n(cwd {"export" if cwd == export else "clone"})\n{text}')
    last = next((l for l in reversed(text.strip().splitlines()) if l.strip()), '')
    rows.append(f'{tag:<58} rc={r.returncode}  {last[:150]}')
    bad += r.returncode != 0
    print(rows[-1], flush=True)
porcelain = subprocess.run(['git', '-C', str(clone), 'status', '--porcelain', '--untracked-files=no'],
                           capture_output=True, text=True).stdout
head = subprocess.run(['git', '-C', str(clone), 'rev-parse', '--short=8', 'HEAD'], capture_output=True, text=True).stdout
(out / 'steps.txt').write_text(f'# docs workflow steps on {head.strip()} (em-dash base {base[:8]}), {len(rows)} steps, '
                               f'{bad} with rc != 0\n' + '\n'.join(rows) +
                               f'\ntracked files changed after the steps: {len(porcelain.splitlines())}\n')
sys.exit(1 if bad else 0)
