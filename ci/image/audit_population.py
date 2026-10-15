#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Trace every reached docs-check and rtl-fast step in the image, with networking disabled.

The reached step set is every `run` step of the docs workflow's `docs-check` job
and of every job of the rtl-fast workflow: the steps the inventory walks. Each runs
as the hosted runner runs a step: `bash -e` on the step text, in its working
directory, with the workflow, job and step environment, the runner context, and
the job's earlier GITHUB_PATH and GITHUB_ENV additions. Every job starts from a
clean checkout with a fresh home and temporary directory.

A step the image replaces runs in its image form, recorded in the receipt:
installation and fetch lines that the image or the checkout supplies are removed,
and the documented adoption lines replace them. A cache-miss build step the
image replaces is not run; the reconciliation names it with its reason.

    python3 ci/image/audit_population.py --image DIGEST --output RECEIPT --logs DIRECTORY

The receipt holds each step's exit status, invocation population and findings,
the source and image identity, and the reconciliation of traced and reached steps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

import exec_audit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKFLOWS = (('.github/workflows/docs.yml', ('docs-check',)), ('.github/workflows/rtl-fast.yml', None))
#: Logical lines whose work the image or the checkout already supplies.
REMOVED = ('python3 -m pip install ', 'sudo apt-get update', 'sudo apt-get install ',
           'sudo ln -sf /opt/yosys/bin/yosys ')
#: The documented RV32 adoption form (docs/testing/CI_IMAGE.md, "CI and act adoption").
RV32 = ('set -euo pipefail\npython3 scripts/ci_rv32_sdk_selftest.py\n'
        'python3 scripts/ci_rv32_sdk.py --verify-only --destination /opt/rv32-sdk\n'
        'mkdir -p "$HOME/br-milan-rv32"\nln -s /opt/rv32-sdk "$HOME/br-milan-rv32/host"\n'
        '"$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc" --version\n')
#: Steps the image replaces whole: the image form proves what replaced them.
REPLACED = {
    'Install the python gate dependencies': ("PyYAML is in the image's Python layer", "python3 -c 'import yaml'\n"),
    'Install the pinned Markdown renderer': ("The locked renderer is in the image's Python layer",
                                             "python3 -c 'import cmarkgfm'\n"),
    'Install diagram gate dependencies': ('The SVG renderer and wavedrom are in the image',
                                          "rsvg-convert --version\npython3 -c 'import wavedrom'\n"),
    'Install behave': ("behave is in the image's Python layer", 'behave --version\n'),
    'Install the pinned sv2v release': ("The checked sv2v is the image's sv2v layer", 'sv2v --version\n'),
    'Install and verify the pinned RV32 SDK': ('The documented RV32 adoption form', RV32),
    'Build Verilator from source on cache miss': ("The image's Verilator layer replaces the cache and build", None),
    'Build Yosys from source on cache miss': ("The image's Yosys layer replaces the cache and build", None),
}
#: Fetch steps: the checkout supplies these submodules before the job; the image form proves it offline.
FETCH = re.compile(r'^git submodule update --init (.+)$')


def logical(text: str) -> list[list[str]]:
    """Group physical lines continued by a trailing backslash."""
    groups, current = [], []
    for line in text.splitlines():
        current.append(line)
        if not line.endswith('\\'):
            groups.append(current)
            current = []
    return groups + ([current] if current else [])


def image_form(name: str, run: str) -> tuple[str | None, str, list[str]]:
    """The text a step runs in the image, why, and the logical lines removed."""
    if name in REPLACED:
        reason, text = REPLACED[name]
        return text, reason, [run]
    fetch = FETCH.match(run.strip())
    if fetch:
        return (f'git submodule status {fetch[1]}\n', 'The checkout supplies these submodules before the job',
                [run])
    kept, removed = [], []
    for group in logical(run):
        # Only a top-level line is removed; an indented fallback keeps its block, which the image never takes.
        (removed if group[0].startswith(REMOVED) else kept).append('\n'.join(group))
    if removed:
        return '\n'.join(kept) + '\n', "Installation the image's layers supply is removed", removed
    return run, 'verbatim', []


def context(expression: str, values: dict[str, str]) -> str:
    """Resolve one runner expression for a push of the reviewed head onto its base."""
    expression = expression.strip()
    if expression in values:
        return values[expression]
    if expression.startswith('needs.') and expression.endswith('.result'):
        return 'success'
    raise ValueError(f'unresolved runner expression {expression!r}')


def substitute(value: object, values: dict[str, str]) -> str:
    """Replace every runner expression in an environment value."""
    return re.sub(r'\$\{\{(.*?)\}\}', lambda match: context(match[1], values), str(value))


def file_commands(path: Path) -> list[str]:
    """Read one runner file-command file."""
    return path.read_text().splitlines() if path.is_file() else []


def environment_file(lines: list[str]) -> dict[str, str]:
    """GITHUB_ENV: NAME=value lines and NAME<<DELIMITER blocks."""
    result, index = {}, 0
    while index < len(lines):
        line = lines[index]
        if '<<' in line and ('=' not in line or line.index('<<') < line.index('=')):
            name, delimiter = line.split('<<', 1)
            block = []
            index += 1
            while index < len(lines) and lines[index] != delimiter:
                block.append(lines[index])
                index += 1
            result[name] = '\n'.join(block)
        elif '=' in line:
            name, value = line.split('=', 1)
            result[name] = value
        index += 1
    return result


def reset(root: Path) -> None:
    """Return the checkout and its initialized submodules to their committed state."""
    subprocess.run(['git', '-C', str(root), 'checkout', '--quiet', '--', '.'], check=True)
    subprocess.run(['git', '-C', str(root), 'clean', '-xdffq'], check=True)
    subprocess.run(['git', '-C', str(root), 'submodule', 'foreach', '--quiet', '--recursive',
                    'git checkout --quiet -- . && git clean -xdffq'], check=True)


def reached_steps(root: Path) -> list[dict[str, object]]:
    """Every run step of the reached jobs, in workflow order."""
    steps = []
    for workflow, jobs in WORKFLOWS:
        document = yaml.safe_load((root / workflow).read_text())
        for job, body in document['jobs'].items():
            if jobs is not None and job not in jobs:
                continue
            for index, step in enumerate(body.get('steps', [])):
                if 'run' in step:
                    steps.append({'workflow': workflow, 'job': job, 'index': index,
                                  'name': step.get('name', str(index)), 'run': step['run'],
                                  'env': {**document.get('env', {}), **body.get('env', {}), **step.get('env', {})},
                                  'working-directory': step.get('working-directory', '.'),
                                  'if': step.get('if')})
    return steps


def git(root: Path, *args: str) -> str:
    """One read-only Git query of the traced checkout."""
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def shape(words: list[str]) -> list[str]:
    """An argument vector compared by program name, with absolute paths as placeholders."""
    return [Path(words[0]).name if words else ''] + ['<path>' if w.startswith('/') else w for w in words[1:]]


def commands(listed: list[Path], logs: list[Path], steps: list[dict]) -> list[dict]:
    """Find each listed (job, step, command) among the exec instances of its traced step."""
    rows = []
    for path in listed:
        for entry in json.loads(path.read_text())['steps']:
            traced = [s for s in steps if s['job'] == entry['job'] and s['label'] == entry['step']]
            seen = 0
            for step in traced:
                for directory in logs:
                    log = directory / step.get('log', '')
                    if log.is_file():
                        seen += sum(shape(json.loads(line)['argv']) == shape(entry['command'])
                                    for line in log.read_text().splitlines())
            rows.append({'job': entry['job'], 'step': entry['step'], 'command': entry['command'],
                         'traced_step': traced[0]['step'] if traced else None, 'instances': seen})
    return rows


def merge(parts: list[Path], output: Path, listed: list[Path], logs: list[Path]) -> int:
    """Combine receipts traced as different users at one source and image into one receipt."""
    receipts = [json.loads(part.read_text()) for part in parts]
    first = receipts[0]
    if any(r['source'] != first['source'] or r['image'] != first['image'] for r in receipts):
        print('REFUSED: the receipts name different sources or images', file=sys.stderr)
        return 2
    rows: dict[str, dict] = {}
    for receipt in receipts:
        for row in receipt['reconciliation']:
            if row['traced'] and rows.get(row['step'], {}).get('traced'):
                print(f"REFUSED: {row['step']} traced twice", file=sys.stderr)
                return 2
            if row['traced'] or row['step'] not in rows:
                rows[row['step']] = {**row, 'user': receipt.get('user')}
    order = [row['step'] for row in first['reconciliation']]
    steps = sorted((step for receipt in receipts for step in receipt['steps']), key=lambda s: order.index(s['step']))
    reconciliation = [rows[key] for key in order]
    merged = {**first, 'users': [r.get('user') for r in receipts], 'reconciliation': reconciliation,
              'steps': steps, 'traced': sum(row['traced'] for row in reconciliation)}
    merged.pop('user', None)
    replaced = {reason for reason, _ in REPLACED.values()}
    merged['commands'] = commands(listed, logs, steps)
    merged['clean'] = all(step['clean'] for step in steps) and \
        all(row['traced'] or row['why'] in replaced for row in reconciliation) and \
        all(row['instances'] for row in merged['commands'])
    output.write_text(json.dumps(merged, indent=1, sort_keys=True) + '\n')
    print(f"{merged['traced']} of {merged['reached']} reached steps traced; "
          f"{sum(not s['clean'] for s in steps)} with findings; "
          f"{sum(bool(r['instances']) for r in merged['commands'])} of {len(merged['commands'])} "
          "listed commands observed")
    return 0 if merged['clean'] else 1


def main() -> int:
    """Trace the reached population and write the receipt."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--image', help='the image manifest digest this runs in')
    parser.add_argument('--base', help='the commit the push is judged against')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--logs', type=Path)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--only', nargs='*', default=[], help='jobs to trace (all when empty)')
    parser.add_argument('--merge', nargs='+', type=Path, help='receipts to combine into --output')
    parser.add_argument('--commands', nargs='*', type=Path, default=[],
                        help='command lists, each {"steps": [{"job", "step", "command"}]}, to find when merging')
    parser.add_argument('--merge-logs', nargs='*', type=Path, default=[], help='the merged receipts\' log directories')
    args = parser.parse_args()
    if args.merge:
        return merge(args.merge, args.output, args.commands, args.merge_logs)
    if not (args.image and args.base and args.logs):
        parser.error('--image, --base and --logs are required to trace')
    return trace_population(args)


def trace_population(args: argparse.Namespace) -> int:
    """Trace every selected reached step in order and write the receipt."""
    root = args.root.resolve()
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        print('REFUSED: the traced checkout must be clean', file=sys.stderr)
        return 2
    head = git(root, 'rev-parse', 'HEAD')
    names = exec_audit.allowlist()
    values = {'github.event_name': 'push', 'github.event.before': args.base, 'github.sha': head,
              'github.event.pull_request.base.ref': '', 'github.event.pull_request.head.sha': ''}
    base_path = os.environ['PATH']
    # A job container inherits the image's environment; the harness's own settings are not passed on.
    inherited = {key: value for key, value in os.environ.items()
                 if key not in ('TMPDIR', 'PYTHONDONTWRITEBYTECODE', 'HOSTNAME', 'HOME', 'PATH')}
    args.logs.mkdir(parents=True, exist_ok=True)
    reached = reached_steps(root)
    receipt_steps, reconciliation = [], []
    job = None
    for number, step in enumerate(reached):
        key = f"{step['workflow']}#{step['job']}#{step['index']}"
        text, reason, removed = image_form(step['name'], step['run'])
        row = {'step': key, 'name': step['name'], 'image_form': reason,
               'removed': removed, 'text_sha256': hashlib.sha256((text or '').encode()).hexdigest()}
        if args.only and step['job'] not in args.only:
            reconciliation.append({**row, 'traced': False, 'why': 'not selected in this run'})
            continue
        if text is None:
            reconciliation.append({**row, 'traced': False, 'why': reason})
            continue
        if step['job'] != job:
            job = step['job']
            reset(root)
            scratch = Path(tempfile.mkdtemp(prefix=f'job-{job}-'))
            home, temp = scratch / 'user', scratch / 'temp'
            home.mkdir()
            temp.mkdir()
            job_path, job_env = [], {}
            origin = exec_audit.Origin(root, exec_audit.checkout_files(root))
        commands = Path(tempfile.mkdtemp(dir=temp, prefix='step-'))
        files = {name: commands / name.lower() for name in
                 ('GITHUB_PATH', 'GITHUB_ENV', 'GITHUB_OUTPUT', 'GITHUB_STEP_SUMMARY')}
        for path in files.values():
            path.touch()
        script = commands / 'step.sh'
        script.write_text(text)
        environment = {**inherited, 'PATH': ':'.join([*reversed(job_path), base_path]), 'HOME': str(home),
                       'CI': 'true',
                       'GITHUB_ACTIONS': 'true', 'GITHUB_WORKSPACE': str(root), 'GITHUB_SHA': head,
                       'GITHUB_EVENT_NAME': 'push', 'RUNNER_TEMP': str(temp),
                       'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', **job_env,
                       **{name: str(path) for name, path in files.items()},
                       **{name: substitute(value, values) for name, value in step['env'].items()}}
        entry = {'job': step['job'], 'label': step['name'], 'argv': ['bash', '-e', str(script)],
                 'working-directory': step['working-directory']}
        result = exec_audit.audit_step(entry, names, root, environment, args.logs / f'step-{number:03d}.jsonl',
                                       origin)
        result.update({'step': key, 'image_form': reason, 'text_sha256': row['text_sha256'],
                       'log': f'step-{number:03d}.jsonl'})
        receipt_steps.append(result)
        reconciliation.append({**row, 'traced': True, 'why': reason})
        job_path += [line for line in file_commands(files['GITHUB_PATH']) if line]
        job_env.update(environment_file(file_commands(files['GITHUB_ENV'])))
        for line in file_commands(files['GITHUB_OUTPUT']):
            if '=' in line and step['job'] == 'changes':
                values[f"needs.changes.outputs.{line.split('=', 1)[0]}"] = line.split('=', 1)[1]
        print(f"{'CLEAN' if result['clean'] else 'FINDINGS'}: {key} {step['name']} "
              f"(exit {result['exit_status']}, {result['instances']} execs)", flush=True)
    reset(root)
    traced = {row['step'] for row in reconciliation if row['traced']}
    receipt = {
        'schema': 1,
        'source': {'commit': head, 'tree': git(root, 'rev-parse', 'HEAD^{tree}'), 'base': args.base,
                   'submodules': git(root, 'submodule', 'status').splitlines()},
        'image': args.image, 'user': os.getuid(),
        'tools': {'python3': sys.version.split()[0]},
        'reached': len(reached), 'traced': len(traced),
        'reconciliation': reconciliation,
        'steps': receipt_steps,
        'clean': all(step['clean'] for step in receipt_steps) and
        all(row['traced'] or row['why'] in [r for r, _ in REPLACED.values()] for row in reconciliation),
    }
    args.output.write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
    print(f"{len(traced)} of {len(reached)} reached steps traced; "
          f"{sum(not s['clean'] for s in receipt_steps)} with findings")
    return 0 if receipt['clean'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
