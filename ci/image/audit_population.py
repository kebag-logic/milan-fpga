#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Trace every reached docs, rtl-fast and elaboration step in the image, with networking disabled.

The reached step set is every `run` step of the docs workflow's gate legs and their
union job, of every job of the rtl-fast workflow, and of the elaboration legs and
their union job: the steps the inventory walks. The run-orchestration jobs call the
GitHub API by design; the reconciliation names their steps, untraced. Each runs
as the hosted runner runs a step: `bash -e` on the step text, in its working
directory, with the workflow, job and step environment, the runner context, and
the job's earlier GITHUB_PATH and GITHUB_ENV additions. Every job starts from a
clean checkout with a fresh home and temporary directory. The steps and needs
contexts hold each traced step's outcome and outputs, and a job's uploaded
artifacts are what a later job of the same workflow downloads.

A step the image replaces runs in its image form, recorded in the receipt:
installation and fetch lines that the image or the checkout supplies are removed,
and the documented adoption lines replace them. A cache-miss build step the
image replaces is not run; the reconciliation names it with its reason.

    python3 ci/image/audit_population.py --image DIGEST --base COMMIT --output RECEIPT --logs DIRECTORY

The receipt holds each step's exit status, invocation population and findings,
the source and image identity, and the reconciliation of traced and reached steps.
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
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
WORKFLOWS = (('.github/workflows/docs.yml', ('docs-gates-0', 'docs-gates-1', 'docs-gates-2', 'docs-check')),
             ('.github/workflows/rtl-fast.yml', None),
             ('.github/workflows/elaborate.yml', ('elaborate-gates-0', 'elaborate-gates-1', 'elaborate')))
#: Jobs that observe, collect and cancel workflow runs through the GitHub API: never traced offline.
ORCHESTRATION = ('ci-manifest', 'ci-fail-fast', 'ci-cancel-tail')
ORCHESTRATED = 'Run orchestration through the GitHub API, which needs the network by design'
#: A step of a job another run of a merge traces: the merge keeps that run's row.
UNSELECTED = 'not selected in this run'
#: Logical lines whose work the image or the checkout already supplies.
REMOVED = ('python3 -m pip install ', 'sudo apt-get update', 'sudo apt-get install ',
           'sudo apt-get -o Dir::Cache::archives=', 'python3 scripts/ci_install_cache.py ',
           'sudo ln -sf /opt/yosys/bin/yosys ')
#: Whole lines the documented adoption replaces (docs/testing/CI_IMAGE.md, "CI and act adoption").
ADOPTED = {'python3 scripts/ci_litex_env.py': 'python3 scripts/ci_litex_env.py --check'}
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
    'Install sbt': ("The checked sbt is the image's sbt layer", 'sbt --script-version\n'),
    'Put a job-private Python environment on PATH': ("The image's Python layer is the job's Python environment",
                                                     "python3 -c 'import litex, migen, yaml'\n"),
    'Build Verilator from source on cache miss': ("The image's Verilator layer replaces the cache and build", None),
    'Build Yosys from source on cache miss': ("The image's Yosys layer replaces the cache and build", None),
}
#: Fetch steps: the checkout supplies these submodules before the job; the image form proves it offline.
FETCH = re.compile(r'^git submodule update --init (.+)$')
#: Toolchain paths in the image carry a GNU packaging triplet. The committed receipt spells each as
#: `<triplet>` (its directory tells the host toolchain from the SDK); the step logs keep every path
#: exactly, and the receipt keeps their digests.
TRIPLET = re.compile(r'(?<![A-Za-z0-9])[a-z0-9_]+(?:-[a-z0-9]+){1,2}-gnu(?![A-Za-z0-9])')


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
    kept, removed, adopted = [], [], False
    for group in logical(run):
        # Only a top-level line is removed; an indented fallback keeps its block, which the image never takes.
        line = '\n'.join(group)
        if line in ADOPTED:
            line, adopted = ADOPTED[line], True
        (removed if group[0].startswith(REMOVED) else kept).append(line)
    if removed or adopted:
        reason = "Installation the image's layers supply is removed" if removed else 'The documented adoption form'
        return '\n'.join(kept) + '\n', reason, removed
    return run, 'verbatim', []


def context(expression: str, values: dict[str, str]) -> str:
    """Resolve one runner expression for a push of the reviewed head onto its base."""
    expression = expression.strip()
    if expression in values:
        return values[expression]
    if expression.startswith('needs.') and expression.endswith('.result'):
        return 'success'
    if re.fullmatch(r'steps\.[\w-]+\.outputs\.[\w-]+', expression):
        return ''  # An output its step never wrote reads as empty, as on the runner.
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
    """Every step of the reached and orchestration jobs, in workflow order; only `run` steps are reached."""
    steps = []
    for workflow, jobs in WORKFLOWS:
        document = yaml.safe_load((root / workflow).read_text())
        for job, body in document['jobs'].items():
            if jobs is not None and job not in jobs and job not in ORCHESTRATION:
                continue
            for index, step in enumerate(body.get('steps', [])):
                steps.append({'workflow': workflow, 'job': job, 'index': index, 'id': step.get('id'),
                              'name': step.get('name', step.get('uses', str(index))), 'run': step.get('run'),
                              'uses': step.get('uses'), 'with': step.get('with', {}),
                              'env': {**document.get('env', {}), **body.get('env', {}), **step.get('env', {})},
                              'working-directory': step.get('working-directory', '.'),
                              'if': step.get('if'), 'orchestration': job in ORCHESTRATION,
                              'needs': body.get('needs', []), 'outputs': body.get('outputs', {})})
    return steps


def artifact_files(paths: str, values: dict[str, str]) -> tuple[Path | None, list[Path]]:
    """What actions/upload-artifact@v4 uploads: every matched file, relative to their common directory."""
    files = []
    for line in str(paths).splitlines():
        if line.strip():
            pattern = substitute(line.strip(), values)
            matched = sorted(glob.glob(pattern)) if glob.has_magic(pattern) else [pattern]
            files += [Path(name) for name in matched if Path(name).is_file()]
    if not files:
        return None, []
    base = files[0].parent
    while not all(f.is_relative_to(base) for f in files):
        base = base.parent
    return base, files


def transfer(step: dict, values: dict[str, str], store: dict[str, dict[str, bytes]]) -> dict:
    """Upload a job's files to, or download them from, the workflow run's artifact store."""
    options = {key: substitute(value, values) if key != 'path' else value for key, value in step['with'].items()}
    if step['uses'].startswith('actions/upload-artifact@'):
        base, files = artifact_files(options['path'], values)
        if not files and options.get('if-no-files-found', 'warn') == 'error':
            return {'artifact': options['name'], 'uploaded': [], 'outcome': 'failure'}
        store[options['name']] = {f.relative_to(base).as_posix(): f.read_bytes() for f in files}
        return {'artifact': options['name'], 'outcome': 'success',
                'uploaded': {name: hashlib.sha256(data).hexdigest() for name, data in store[options['name']].items()}}
    target = Path(substitute(options.get('path', '.'), values))
    if 'name' in options:
        names, nested = [options['name']], False
    else:
        names, nested = sorted(n for n in store if fnmatch.fnmatchcase(n, options.get('pattern', '*'))), True
    if options.get('merge-multiple') not in (None, 'false') or not names or any(n not in store for n in names):
        return {'artifact': options.get('name', options.get('pattern')), 'downloaded': names, 'outcome': 'failure'}
    for name in names:
        for relative, data in store[name].items():
            destination = (target / name if nested else target) / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
    return {'artifact': options.get('name', options.get('pattern')), 'downloaded': names, 'outcome': 'success'}


def git(root: Path, *args: str) -> str:
    """One read-only Git query of the traced checkout."""
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def listed_program(words: list[str]) -> tuple[str, str, list[str]]:
    """What a listed command runs, read as the audit reads an exec: kind, operand and arguments."""
    family = exec_audit.interpreter(Path(words[0]).name)
    if family is None:
        return ('script' if '/' in words[0] else 'name'), words[0], words[1:]
    read = exec_audit.operands(family, words)
    if read['kind'] == 'script':
        return 'script', read['rest'][0], read['rest'][1:]
    return read['kind'], read.get('module') or Path(words[0]).name, []


def placeholders(words: list[str]) -> list[str]:
    """Arguments with absolute paths as placeholders, since every run has its own temporary paths."""
    return ['<path>' if word.startswith('/') else word for word in words]


def observed_arguments(instance: dict, program: tuple[str, str, list[str]], directory: str) -> list[str] | None:
    """The arguments of an exec instance that runs the listed program, or None when it runs another."""
    kind, operand, _ = program
    seen = exec_audit.invocation(instance)
    if kind == 'script' and seen['kind'] == 'script':
        # A listed absolute path is the listing run's own temporary copy: only its name is comparable.
        matched = seen['name'] == Path(operand).name if operand.startswith('/') else \
            seen['path'] == exec_audit.lexical(directory, operand)
    elif kind == 'name':
        matched = seen['kind'] in ('program', 'script') and seen['name'] == operand
    else:
        matched = seen['kind'] == kind and seen['path' if kind == 'module' else 'name'] == operand
    return list(seen.get('args', [])) if matched else None


def commands(listed: list[Path], logs: list[Path], steps: list[dict], checkout: str) -> list[dict]:
    """Find each listed (job, step, command) among the exec instances of its traced step.

    A listed step names a traced step, or extends that name with a qualifier for another
    command of the step. An instance matches when it runs the listed script, module or
    program. Arguments are compared with absolute paths as placeholders; when no matching
    instance has the listed arguments, the observed ones are kept beside the listed ones.
    """
    rows = []
    for path in listed:
        for entry in json.loads(path.read_text())['steps']:
            traced = sorted((s for s in steps if s['job'] == entry['job'] and
                             (s['label'] == entry['step'] or entry['step'].startswith(s['label'] + ' '))),
                            key=lambda s: -len(s['label']))[:1]
            program = listed_program(entry['command'])
            found: list[list[str]] = []
            for step in traced:
                directory = exec_audit.lexical(checkout, step['working-directory'])
                log = next((d / step['log'] for d in logs if (d / step['log']).is_file()), None)
                for line in log.read_text().splitlines() if log else []:
                    arguments = observed_arguments(json.loads(line), program, directory)
                    if arguments is not None:
                        found.append(arguments)
            row = {'job': entry['job'], 'step': entry['step'], 'command': entry['command'],
                   'traced_step': traced[0]['step'] if traced else None, 'instances': len(found),
                   'arguments': 'listed' if placeholders(program[2]) in map(placeholders, found) else 'observed'}
            if found and row['arguments'] == 'observed':
                row['observed'] = [list(variant) for variant in dict.fromkeys(map(tuple, found))][:3]
            rows.append(row)
    return rows


def untripled(value: object) -> object:
    """A receipt value with each toolchain triplet spelled `<triplet>`."""
    if isinstance(value, str):
        return TRIPLET.sub('<triplet>', value)
    if isinstance(value, list):
        return [untripled(item) for item in value]
    if isinstance(value, dict):
        return {key: untripled(item) for key, item in value.items()}
    return value


def untraced() -> set[str]:
    """The reasons a reached step may stay untraced: the image replaces it, or it orchestrates the run."""
    return {reason for reason, _ in REPLACED.values()} | {ORCHESTRATED}


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
            # The run that selected a step's job decides its row, traced or untraced with its reason.
            if row['traced'] or rows.get(row['step'], {}).get('why', UNSELECTED) == UNSELECTED:
                rows[row['step']] = {**row, 'user': receipt.get('user')}
    order = [row['step'] for row in first['reconciliation']]
    steps = sorted((step for receipt in receipts for step in receipt['steps']), key=lambda s: order.index(s['step']))
    reconciliation = [rows[key] for key in order]
    merged = {**first, 'users': [r.get('user') for r in receipts], 'reconciliation': reconciliation,
              'steps': steps, 'traced': sum(row['traced'] for row in reconciliation)}
    merged.pop('user', None)
    merged['artifacts'] = [moved for receipt in receipts for moved in receipt['artifacts']]
    merged['commands'] = commands(listed, logs, steps, first['source']['checkout'])
    merged['clean'] = all(step['clean'] for step in steps) and \
        all(row['traced'] or row['why'] in untraced() for row in reconciliation) and \
        all(row['instances'] for row in merged['commands']) and \
        all(moved['outcome'] == 'success' for moved in merged['artifacts'])
    output.write_text(json.dumps(untripled(merged), indent=1, sort_keys=True) + '\n')
    print(f"{merged['traced']} of {merged['reached']} reached steps traced; "
          f"{sum(not s['clean'] for s in steps)} with findings; "
          f"{sum(bool(r['instances']) for r in merged['commands'])} of {len(merged['commands'])} "
          f"listed commands observed, {sum(r['arguments'] == 'listed' for r in merged['commands'])} "
          "with the listed arguments")
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


def run_step(step: dict, text: str, environment: dict[str, str], audit: tuple,
             log: Path) -> tuple[dict, dict[str, Path]]:
    """Run one step's image form under the audit, with fresh runner file-command files."""
    commands = Path(tempfile.mkdtemp(dir=environment['RUNNER_TEMP'], prefix='step-'))
    files = {name: commands / name.lower() for name in
             ('GITHUB_PATH', 'GITHUB_ENV', 'GITHUB_OUTPUT', 'GITHUB_STEP_SUMMARY')}
    for path in files.values():
        path.touch()
    script = commands / 'step.sh'
    script.write_text(text)
    entry = {'job': step['job'], 'label': step['name'], 'argv': ['bash', '-e', str(script)],
             'working-directory': step['working-directory'], 'text': text}
    names, root, origin = audit
    environment = {**environment, **{name: str(path) for name, path in files.items()}}
    return exec_audit.audit_step(entry, names, root, environment, log, origin), files


def job_values(step: dict, jobs: dict[tuple[str, str], dict], values: dict[str, str]) -> dict[str, str]:
    """The runner values a job starts with: its matrix, and the result and outputs of each job it needs."""
    needs = [step['needs']] if isinstance(step['needs'], str) else list(step['needs'])
    if any((step['workflow'], need) not in jobs for need in needs):
        raise ValueError(f"{step['job']} needs a job this run did not trace: {needs}")
    needed = {need: jobs[(step['workflow'], need)] for need in needs}
    return {**values, 'toJSON(matrix)': 'null', 'strategy.job-index': '0',
            'toJSON(needs)': json.dumps(needed, indent=2),
            **{f'needs.{n}.result': r['result'] for n, r in needed.items()},
            **{f'needs.{n}.outputs.{k}': v for n, r in needed.items() for k, v in r['outputs'].items()}}


def record_step(contexts: dict, values: dict[str, str], identifier: str | None, outcome: str,
                outputs: dict[str, str]) -> None:
    """The steps context a later step reads: each identified step's outcome and outputs."""
    contexts['ok'] = contexts['ok'] and outcome == 'success'
    if identifier:
        contexts['steps'][identifier] = {'outputs': outputs, 'outcome': outcome, 'conclusion': outcome}
        values.update({f'steps.{identifier}.outputs.{name}': value for name, value in outputs.items()})


def finished(contexts: dict, values: dict[str, str]) -> dict:
    """The needs context a later job reads: this job's result and its declared outputs."""
    return {'result': 'success' if contexts['ok'] else 'failure',
            'outputs': {name: substitute(value, values) for name, value in contexts['outputs'].items()}}


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
    every = reached_steps(root)
    reached = [step for step in every if step['run'] is not None]
    receipt_steps, reconciliation, artifacts = [], [], []
    job, origin = None, None
    stores: dict[str, dict[str, dict[str, bytes]]] = {}
    jobs: dict[tuple[str, str], dict] = {}
    # Each job starts from the image as built: the image's own files are snapshotted once, before any job.
    image = exec_audit.Image(exec_audit.SYSTEM_ROOTS)
    number = -1
    for step in every:
        key = f"{step['workflow']}#{step['job']}#{step['index']}"
        selected = not args.only or step['job'] in args.only
        if step['run'] is not None:
            number += 1
            text, reason, removed = image_form(step['name'], step['run'])
            row = {'step': key, 'name': step['name'], 'image_form': reason,
                   'removed': removed, 'text_sha256': hashlib.sha256((text or '').encode()).hexdigest()}
            if step['orchestration']:
                reconciliation.append({**row, 'traced': False, 'why': ORCHESTRATED})
                continue
            if not selected:
                reconciliation.append({**row, 'traced': False, 'why': UNSELECTED})
                continue
        elif step['orchestration'] or not selected:
            continue
        if (step['workflow'], step['job']) != job:
            if job is not None:
                jobs[job] = finished(contexts, step_values)
                origin.close()
            job = (step['workflow'], step['job'])
            reset(root)
            scratch = Path(tempfile.mkdtemp(prefix=f"job-{step['job']}-"))
            home, temp = scratch / 'user', scratch / 'temp'
            home.mkdir()
            temp.mkdir()
            job_path, job_env, contexts = [], {}, {'steps': {}, 'ok': True, 'outputs': step['outputs']}
            origin = exec_audit.Origin(root, names, scratch=(str(scratch),), image=image)
            step_values = job_values(step, jobs, {**values, 'github.workspace': str(root), 'runner.temp': str(temp)})
        step_values['toJSON(steps)'] = json.dumps(contexts['steps'], indent=2)
        step_values['job.status'] = 'success' if contexts['ok'] else 'failure'
        if step['run'] is None:
            outcome, outputs = 'success', {}
            if step['uses'] and step['uses'].startswith(('actions/upload-artifact@', 'actions/download-artifact@')):
                moved = transfer(step, step_values, stores.setdefault(step['workflow'], {}))
                artifacts.append({'step': key, **moved})
                outcome = moved['outcome']
            record_step(contexts, step_values, step['id'], outcome, outputs)
            continue
        if text is None:
            reconciliation.append({**row, 'traced': False, 'why': reason})
            record_step(contexts, step_values, step['id'], 'success', {})
            continue
        environment = {**inherited, 'PATH': ':'.join([*reversed(job_path), base_path]), 'HOME': str(home),
                       'CI': 'true', 'GITHUB_ACTIONS': 'true', 'GITHUB_WORKSPACE': str(root), 'GITHUB_SHA': head,
                       'GITHUB_EVENT_NAME': 'push', 'RUNNER_TEMP': str(temp),
                       'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', **job_env,
                       **{name: substitute(value, step_values) for name, value in step['env'].items()}}
        result, files = run_step(step, text, environment, (names, root, origin),
                                 args.logs / f'step-{number:03d}.jsonl')
        result.update({'step': key, 'image_form': reason, 'text_sha256': row['text_sha256'],
                       'log': f'step-{number:03d}.jsonl'})
        receipt_steps.append(result)
        reconciliation.append({**row, 'traced': True, 'why': reason})
        job_path += [line for line in file_commands(files['GITHUB_PATH']) if line]
        job_env.update(environment_file(file_commands(files['GITHUB_ENV'])))
        record_step(contexts, step_values, step['id'], 'success' if result['exit_status'] == 0 else 'failure',
                    environment_file(file_commands(files['GITHUB_OUTPUT'])))
        print(f"{'CLEAN' if result['clean'] else 'FINDINGS'}: {key} {step['name']} "
              f"(exit {result['exit_status']}, {result['instances']} execs)", flush=True)
    if origin is not None:
        origin.close()
    reset(root)
    return write_receipt(args, root, len(reached), (reconciliation, receipt_steps, artifacts))


def write_receipt(args: argparse.Namespace, root: Path, reached: int, rows: tuple[list, list, list]) -> int:
    """Write the receipt: source and image identity, each step's result, and the reconciliation."""
    reconciliation, receipt_steps, artifacts = rows
    traced = {row['step'] for row in reconciliation if row['traced']}
    receipt = {
        'schema': 1,
        'source': {'commit': git(root, 'rev-parse', 'HEAD'), 'tree': git(root, 'rev-parse', 'HEAD^{tree}'),
                   'base': args.base, 'checkout': str(root),
                   'submodules': git(root, 'submodule', 'status').splitlines()},
        'image': args.image, 'user': os.getuid(),
        'tools': {'python3': sys.version.split()[0]},
        'reached': reached, 'traced': len(traced),
        'reconciliation': reconciliation,
        'steps': receipt_steps,
        'artifacts': artifacts,
        'clean': all(step['clean'] for step in receipt_steps) and
        all(row['traced'] or row['why'] in untraced() for row in reconciliation) and
        all(moved['outcome'] == 'success' for moved in artifacts),
    }
    args.output.write_text(json.dumps(receipt, indent=1, sort_keys=True) + '\n')
    print(f"{len(traced)} of {reached} reached steps traced; "
          f"{sum(not s['clean'] for s in receipt_steps)} with findings")
    return 0 if receipt['clean'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
