#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove each census shape against the real tool: the differential harness.

Every fixture in ci_differential_fixtures.py is resolved twice. The walker resolves
it statically, with the census gate off, and reports the observed commands it
would run, their directories and argument vectors. The real tool runs it inside
the image, offline: GNU Make 4.3, bash 5.2.21 or dash, and CPython 3.12.3, with
each observed command replaced by a stub that records its directory and
arguments. The outcomes are compared:

- `identical`: the walker resolved exactly the commands the real tool ran.
  A runtime slot matches one argument; an unquoted runtime expansion matches any.
- `residue`: every command the walker resolved ran, and what it did not resolve is
  covered by located residue in a declared script.
- `refused`: the walker refused by name, and the real tool ran the hidden command.

A census shape is accepted only through a focus fixture whose outcome equals its
expectation and that exercised the shape. The receipt binds the walker sources,
the fixtures and the census shapes; any change needs a new run in the image.

    python3 scripts/ci_differential.py --run --image DIGEST --receipt PATH   # in the image
    python3 scripts/ci_differential.py --write-census                       # from the tree
    python3 scripts/ci_differential.py --check
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

import ci_command_table
from ci_command_table import Audit, Refusal, Runtime, binding
from ci_differential_fixtures import FIXTURES
import ci_shell_walk
import ci_tool_inventory


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / 'ci/image/syntax-census.json'
RECEIPT = ROOT / 'ci/image/differential-receipt.json'
#: Reference tool identities the receipt must be measured with.
TOOLS = {'bash': ['bash', '--version'], 'make': ['make', '--version'], 'python3': ['python3', '-VV'],
         'dash': ['dpkg-query', '-W', '-f', '${Version}', 'dash']}
EXPECTED = {'bash': 'GNU bash, version 5.2.21(1)-release', 'make': 'GNU Make 4.3', 'python3': 'Python 3.12.3'}
OUTCOMES = ('identical', 'residue', 'refused')
STUB = '''#!/usr/bin/python3 -I
import json, os, sys
record = json.dumps({{'directory': os.getcwd(), 'argv': [os.path.basename(sys.argv[0]), *sys.argv[1:]]}})
descriptor = os.open({log!r}, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
os.write(descriptor, (record + '\\n').encode())
os.close(descriptor)
'''


def fixture_digest(fixture: dict) -> str:
    """Bind a receipt entry to the exact fixture definition."""
    return hashlib.sha256(json.dumps(fixture, sort_keys=True).encode()).hexdigest()


def encode(value: str) -> list:
    """Keep runtime provenance in the receipt: literal, runtime slot or any number of fields."""
    if isinstance(value, ci_shell_walk.Fields):
        return ['fields']
    if isinstance(value, Runtime):
        return ['runtime']
    return ['literal', value]


def matches(pattern: list, argv: list[str]) -> bool:
    """A runtime slot matches one argument; a fields slot matches any number."""
    if not pattern:
        return not argv
    head = pattern[0]
    if head[0] == 'fields':
        return any(matches(pattern[1:], argv[index:]) for index in range(len(argv) + 1))
    if not argv:
        return False
    return (head[0] == 'runtime' or head[1] == argv[0]) and matches(pattern[1:], argv[1:])


def same(walked: dict, ran: dict) -> bool:
    """One walker resolution and one real execution agree on directory and arguments."""
    return walked['directory'] in (None, ran['directory']) and matches(walked['argv'], ran['argv'])


def build(fixture: dict, tree: Path) -> None:
    """Write the fixture tree with the committed tables and a one-step workflow."""
    (tree / 'ci/image').mkdir(parents=True)
    for name in ('command-table.json', 'sources.lock.json', 'syntax-census.json', 'make-builtins.json'):
        shutil.copyfile(ROOT / 'ci/image' / name, tree / 'ci/image' / name)
    for name, text in fixture.get('files', {}).items():
        path = tree / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        if name in fixture.get('executable', []):
            path.chmod(0o755)
    for name, target in fixture.get('links', {}).items():
        (tree / name).parent.mkdir(parents=True, exist_ok=True)
        (tree / name).symlink_to(target)
    table = json.loads((tree / 'ci/image/command-table.json').read_text())
    for name in fixture.get('declare', []):
        table['scripts'][name] = {'class': 'reviewed non-installing', 'reason': 'Differential fixture.',
                                  'sha256': hashlib.sha256((tree / name).read_bytes()).hexdigest()}
    for name, patterns in fixture.get('patterns', {}).items():
        table['commands'][name]['patterns'].extend(patterns)
    for interpreter, programs in fixture.get('inline', {}).items():
        for program in programs:
            pin = hashlib.sha256(program.encode()).hexdigest()
            table['inline'][f'{interpreter}:{pin}'] = {'class': 'non-installing', 'reason': 'Differential fixture.'}
    (tree / 'ci/image/command-table.json').write_text(ci_tool_inventory.serialized(table))
    census = json.loads((tree / 'ci/image/syntax-census.json').read_text())
    for name in fixture.get('workflow_environment', []):
        census['workflow_environment'][name] = 'Differential fixture.'
    for kind, sources in fixture.get('exact_uses', {}).items():
        for text in sources:
            statement = ci_command_table.shell_tree(text, Path(os.environ['CI_IMAGE_SHFMT']))['Stmts'][0]
            node = statement['Cmd'] if kind != 'environment-file' else statement
            from ci_syntax import semantic_node
            raw = json.dumps(semantic_node(node), sort_keys=True, separators=(',', ':')).encode()
            entry = census['shell_exact_uses'].setdefault(hashlib.sha256(raw).hexdigest(), {'sources': [], 'kinds': []})
            source = fixture.get('exact_source', '.github/workflows/fixture.yml')
            entry['sources'] = sorted(set(entry['sources']) | {source})
            entry['kinds'] = sorted(set(entry['kinds']) | {kind})
    (tree / 'ci/image/syntax-census.json').write_text(ci_tool_inventory.serialized(census))
    step = {'run': fixture['run']}
    if fixture.get('env'):
        step['env'] = fixture['env']
    if fixture.get('working-directory'):
        step['working-directory'] = fixture['working-directory']
    workflow = tree / '.github/workflows/fixture.yml'
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [step]}}}))


def walk(fixture: dict, tree: Path) -> dict:
    """Resolve the fixture with the walker, recording observed commands, shapes and residue."""
    observed = set(fixture.get('observe', [])) | {'zz_probe'}
    resolved, inspected, shapes = [], [], set()
    command, shape = Audit.command, Audit.shape

    def observing(self: Audit, words: list[str], where: str, directory: Path | None = None) -> None:
        """Record an observed command's directory and arguments, as the walker resolved them."""
        if words and not isinstance(words[0], Runtime) and Path(words[0]).name in observed:
            directory = (directory or self.root).resolve()
            unknown = any(directory.is_relative_to(p) for p in self.runtime_directories)
            entry = {'directory': directory.relative_to(self.root).as_posix()
                     if directory.is_relative_to(self.root) and not unknown else None,
                     'argv': [encode(Path(words[0]).name)] + [encode(w) for w in words[1:]]}
            (inspected if self.inspecting else resolved).append(entry)
            if Path(words[0]).name == 'zz_probe':
                self.shape('cmd:table', where)
                return None  # The sentinel itself has no table row; every other observed name is classified.
        return command(self, words, where, directory)

    def recording(self: Audit, name: str, where: str) -> None:
        """Record every shape the fixture exercises."""
        shapes.add(name)
        return shape(self, name, where)

    Audit.command, Audit.shape = observing, recording
    ci_command_table.GATE = False
    try:
        result = ci_tool_inventory.derive(tree)
        refusal = None
    except (Refusal, OSError, KeyError, ValueError) as error:
        result, refusal = None, str(error).replace(str(tree), '<fixture>')
    finally:
        Audit.command, Audit.shape = command, shape
        ci_command_table.GATE = True
    return {'refusal': refusal, 'resolved': resolved, 'inspected': inspected, 'shapes': sorted(shapes),
            'residue': [r.replace(str(tree), '<fixture>') for r in (result or {}).get('residue', [])]}


def run(fixture: dict, tree: Path, scratch: Path) -> list[dict]:
    """Run the step with the real tools for every variant; collect what the stubs recorded."""
    log = scratch / 'observed.log'
    bin_directory = scratch / 'bin'
    bin_directory.mkdir()
    directories = [bin_directory] + ([tree / fixture['stub_directory']] if fixture.get('stub_directory') else [])
    for directory in directories:
        directory.mkdir(exist_ok=True)
        for name in set(fixture.get('observe', [])) | {'zz_probe'}:
            stub = directory / name
            stub.write_text(STUB.format(log=str(log)))
            stub.chmod(0o755)
    script = scratch / 'step.sh'
    script.write_text(fixture['run'])
    home = scratch / 'home'
    home.mkdir()
    statuses = []
    for variant in fixture.get('variants', [{}]):
        environment = {'PATH': f'{bin_directory}:{os.environ["PATH"]}', 'HOME': str(home),
                       'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', **fixture.get('env', {}), **variant}
        directory = tree / fixture.get('working-directory', '.')
        result = subprocess.run(['bash', '-e', str(script)], cwd=directory, env=environment, timeout=120,
                                capture_output=True, text=True, check=False)
        statuses.append(result.returncode)
    ran = []
    for line in log.read_text().splitlines() if log.is_file() else []:
        record = json.loads(line)
        path = Path(record['directory'])
        record['directory'] = path.relative_to(tree.resolve()).as_posix() if path.is_relative_to(tree.resolve()) \
            else None
        if record not in ran:
            ran.append(record)
    return ran, statuses


def outcome(fixture: dict, walker: dict, ran: list[dict]) -> str:
    """Compare the walker's resolution with the real executions."""
    if walker['refusal'] is not None:
        return 'refused' if ran or not fixture.get('executes') else 'refused-without-execution'
    unresolved = [x for x in ran if not any(same(w, x) for w in walker['resolved'])]
    unexecuted = [w for w in walker['resolved'] if not any(same(w, x) for x in ran)]
    if unexecuted:
        return 'mismatch'
    if unresolved:
        return 'residue' if walker['residue'] else 'mismatch'
    return 'identical'


def tool_versions() -> dict:
    """The reference tools this receipt was measured with, read inside the image."""
    versions = {}
    for name, command in TOOLS.items():
        text = subprocess.run(command, capture_output=True, text=True, check=True).stdout
        # The version alone: the build triple a tool appends names no product surface.
        versions[name] = text.splitlines()[0].split(' (x86_64')[0].strip() if text else ''
    for name, prefix in EXPECTED.items():
        if not versions[name].startswith(prefix):
            raise SystemExit(f'REFUSED: {name} is {versions[name]!r}, not the image reference {prefix!r}')
    return versions


def measure(only: list[str], image: str) -> dict:
    """Run every fixture through both resolutions."""
    census = json.loads(CENSUS.read_text())
    results = {}
    for fixture in FIXTURES:
        if only and fixture['id'] not in only:
            continue
        with tempfile.TemporaryDirectory(prefix='ci-differential-') as directory:
            scratch = Path(directory)
            tree = scratch / 'tree'
            tree.mkdir()
            build(fixture, tree)
            walker = walk(fixture, tree)
            ran, statuses = run(fixture, tree, scratch)
        result = outcome(fixture, walker, ran)
        # The receipt names disposable locations by role, never by their scratch path.
        names = ((str(scratch / 'home'), '<home>'), (str(tree), '<fixture>'), (str(scratch), '<scratch>'))
        def neutral(value: object) -> object:
            """Replace disposable paths throughout one recorded value."""
            if isinstance(value, str):
                for path, role in names:
                    value = value.replace(path, role)
                return value
            if isinstance(value, list):
                return [neutral(item) for item in value]
            if isinstance(value, dict):
                return {key: neutral(item) for key, item in value.items()}
            return value
        walker, ran = neutral(walker), neutral(ran)
        results[fixture['id']] = {
            'sha256': fixture_digest(fixture), 'expect': fixture['expect'], 'outcome': result,
            'shapes': walker['shapes'], 'walker': walker['resolved'], 'inspected': walker['inspected'],
            'residue': walker['residue'], 'refusal': walker['refusal'], 'real': ran, 'statuses': statuses}
        if fixture['expect'] == 'refused' and walker['refusal'] and fixture.get('refusal', '') not in walker['refusal']:
            results[fixture['id']]['outcome'] = 'refused-otherwise'
        mark = 'PASS' if results[fixture['id']]['outcome'] == fixture['expect'] else 'FAIL'
        print(f"{mark}: {fixture['id']}: {results[fixture['id']]['outcome']} (expect {fixture['expect']})")
    return {'schema': 1, 'binding': binding(census), 'image': image, 'tools': tool_versions(), 'fixtures': results}


def tree_shapes() -> dict[str, str]:
    """The shapes the current tree's derivation applies, with a first location each."""
    used = {}
    shape = Audit.shape

    def recording(self: Audit, name: str, where: str) -> None:
        """Record every shape the tree uses, with its first location."""
        used.setdefault(name, where)
    Audit.shape = recording
    ci_command_table.GATE = False
    try:
        ci_tool_inventory.derive(ROOT)
    finally:
        Audit.shape = shape
        ci_command_table.GATE = True
    return used


def write_census() -> None:
    """Regenerate the census shapes: exactly the tree's shapes, each with its focus fixture."""
    focus = {}
    for fixture in FIXTURES:
        for shape in fixture.get('shapes', []):
            if shape in focus:
                raise SystemExit(f'REFUSED: shape {shape!r} has two focus fixtures')
            focus[shape] = fixture['id']
    used = tree_shapes()
    missing = sorted(set(used) - set(focus))
    if missing:
        raise SystemExit('REFUSED: tree shapes without a focus fixture: ' +
                         ', '.join(f'{name} ({used[name]})' for name in missing))
    census = json.loads(CENSUS.read_text())
    census['shapes'] = {name: focus[name] for name in sorted(used)}
    CENSUS.write_text(ci_tool_inventory.serialized(census))
    print(f'census shapes: {len(used)} tree shapes, each with a focus fixture')


def check() -> int:
    """The receipt is current and every census shape and fixture met its expectation."""
    census = json.loads(CENSUS.read_text())
    receipt = json.loads(RECEIPT.read_text())
    failures = []
    if receipt.get('binding') != binding(census):
        failures.append('receipt binding differs from the walker, fixtures and census shapes')
    for fixture in FIXTURES:
        entry = receipt['fixtures'].get(fixture['id'])
        if entry is None or entry['sha256'] != fixture_digest(fixture):
            failures.append(f"fixture {fixture['id']} is not measured at its current definition")
        elif entry['outcome'] != fixture['expect']:
            failures.append(f"fixture {fixture['id']}: {entry['outcome']}, expected {fixture['expect']}")
        elif not set(fixture.get('shapes', [])) <= set(entry['shapes']):
            missing = sorted(set(fixture['shapes']) - set(entry['shapes']))
            failures.append(f"fixture {fixture['id']} did not exercise {missing}")
    for shape, fixture in census.get('shapes', {}).items():
        if shape not in next((f.get('shapes', []) for f in FIXTURES if f['id'] == fixture), []):
            failures.append(f'census shape {shape!r} is not a focus of fixture {fixture!r}')
    for failure in failures:
        print(f'FAIL: {failure}')
    if failures:
        return 1
    print(f"PASS: {len(FIXTURES)} differential fixtures meet their expectations; "
          f"{len(census['shapes'])} census shapes proven at image {receipt['image']}")
    return 0


def main() -> int:
    """Measure in the image, regenerate the census shapes, or check the committed receipt."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--run', action='store_true')
    modes.add_argument('--write-census', action='store_true')
    modes.add_argument('--check', action='store_true')
    parser.add_argument('--image', default='')
    parser.add_argument('--receipt', type=Path, default=RECEIPT)
    parser.add_argument('--only', nargs='*', default=[])
    args = parser.parse_args()
    if args.write_census:
        write_census()
        return 0
    if args.check:
        return check()
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', args.image):
        print('REFUSED: --image must name the image manifest digest the harness runs in', file=sys.stderr)
        return 2
    receipt = measure(args.only, args.image)
    args.receipt.write_text(json.dumps(receipt, sort_keys=True, indent=1) + '\n')
    failed = [k for k, v in receipt['fixtures'].items() if v['outcome'] != v['expect']]
    print(f'{len(receipt["fixtures"]) - len(failed)} of {len(receipt["fixtures"])} fixtures met their expectation')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
