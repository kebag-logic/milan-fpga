#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Classify literal CI commands against a closed, reviewed command table."""

from __future__ import annotations

import ast
from collections.abc import Iterator
import hashlib
import json
import os
import subprocess
from pathlib import Path
import re
import shlex


TABLE = Path('ci/image/command-table.json')
NETWORK = {'urllib', 'http', 'requests', 'socket', 'ftplib'}
CALLS = {'run', 'check_call', 'check_output', 'Popen', 'call', 'system', 'getoutput', 'getstatusoutput'}


class Refusal(ValueError):
    """A literal command has no reviewed classification."""


def sha256(path: Path) -> str:
    """Bind a declaration to exact source bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nodes(value: object) -> Iterator[dict]:
    """Walk the parser's structural JSON, including nested substitutions."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def word(value: dict) -> str:
    """Retain literal argv and mark shell expansion without evaluating it."""
    kind = value.get('Type')
    if kind == 'Lit':
        return re.sub(r'\\(.)', r'\1', value.get('Value', ''))
    if kind == 'SglQuoted':
        return value.get('Value', '')
    if kind == 'ParamExp':
        return '${' + value['Param']['Value'] + '}'
    if kind in ('CmdSubst', 'ProcSubst', 'ArithmExp', 'BraceExp'):
        return '${RUNTIME}'
    if 'Parts' in value or kind == 'DblQuoted':
        return ''.join(word(part) for part in value.get('Parts', []))
    raise Refusal(f'unsupported shell word node {kind!r}')


def shell_tree(source: str, parser: Path) -> dict:
    """Parse Bash syntax without executing any candidate command."""
    result = subprocess.run([str(parser), '-ln', 'bash', '--to-json'], input=source,
                            text=True, capture_output=True, check=False)
    if result.returncode:
        raise Refusal('shell parse failed: ' + result.stderr.strip())
    return json.loads(result.stdout)


class Audit:
    """Bind every literal command and followed script to one committed table."""

    def __init__(self, root: Path, inputs: dict[str, str]) -> None:
        self.root = root.resolve()
        self.inputs = inputs
        self.table = json.loads((root / TABLE).read_text())
        self.inputs[str(TABLE)] = sha256(root / TABLE)
        self.seen: set[str] = set()
        self.residue: set[str] = set()
        self.functions: set[str] = set()
        self.requests: list[dict] = []
        self.env: dict[str, str] = {}
        self.install_reader = None
        self.parser = Path(os.environ.get('CI_IMAGE_SHFMT', 'shfmt'))
        parser_lock = root / self.table['parser']['source_lock']
        self.inputs[self.table['parser']['source_lock']] = sha256(parser_lock)
        parser_pin = json.loads(parser_lock.read_text())['host_tools'][self.table['parser']['tool']]
        if not self.parser.is_file() or sha256(self.parser) != parser_pin['sha256']:
            raise Refusal('CI_IMAGE_SHFMT must name the checksum-pinned Bash parser')

    def script(self, name: str, where: str, directory: Path | None = None) -> None:
        """Follow resolved scripts, refusing absent literal paths."""
        if name.startswith(('${ROOT}/', '$ROOT/', '$R/')):
            directory = self.root
        name = name.replace('${ROOT}/', '').replace('$ROOT/', '').replace('$R/', '')
        if '$' in name or '<dynamic>' in name:
            self.residue.add(f'{where}: runtime script path')
            return
        if directory and '$' in str(directory):
            self.residue.add(f'{where}: runtime working directory')
            return
        path = (directory or self.root) / name
        if not path.is_file():
            raise Refusal(f'unresolved script {name!r} at {where}')
        if not path.resolve().is_relative_to(self.root):
            raise Refusal(f'script outside source tree {name!r} at {where}')
        relative = path.resolve().relative_to(self.root).as_posix()
        declaration = self.table['scripts'].get(relative)
        if declaration:
            if declaration['sha256'] != sha256(path):
                raise Refusal(f'changed declared script {relative!r}')
            if declaration['class'] == 'installer':
                self.requests.extend(declaration['tools'])
                self.inputs[relative] = sha256(path)
                return
        if relative in self.seen:
            return
        self.seen.add(relative)
        self.inputs[relative] = sha256(path)
        if path.suffix == '.py':
            self.python(path.read_text(), relative, path.parent)
        elif path.suffix == '.sh':
            self.shell(path.read_text(), relative, directory or self.root)
        elif path.name == 'Makefile' or path.suffix == '.mk':
            self.makefile(path)
        else:
            raise Refusal(f'unsupported script language {relative!r} at {where}')

    def python(self, source: str, where: str, directory: Path) -> None:
        """Check imports and positional/keyword subprocess arguments without execution."""
        tree = ast.parse(source)
        network = False
        modules = {'subprocess', 'os'}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(a.asname or a.name for a in node.names if a.name in ('subprocess', 'os'))
            elif isinstance(node, ast.ImportFrom) and node.module in ('subprocess', 'os'):
                imported.update(a.asname or a.name for a in node.names if a.name in CALLS)
        calls = []
        assignments = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments.setdefault(target.id, []).append(node.value)
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or '']
                network |= any(n.split('.')[0] in NETWORK for n in names)
                for name in names:
                    stem = name.replace('.', '/') + '.py'
                    for base in (directory, self.root, self.root / 'scripts'):
                        if (base / stem).is_file():
                            self.script(stem, where, base)
                            break
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec', 'getattr', '__import__'):
                    self.residue.add(f'{where}:{node.lineno}: runtime Python execution or lookup')
                function = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, 'id', '')
                executor = (isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                            and node.func.value.id in modules and function in CALLS)
                if executor or (isinstance(node.func, ast.Name) and function in imported):
                    argument = next((k.value for k in node.keywords if k.arg == 'args'), None)
                    argument = argument if argument is not None else (node.args[0] if node.args else None)
                    if argument is not None:
                        cwd = next((k.value for k in node.keywords if k.arg == 'cwd'), None)
                        working = self.root
                        if cwd is not None:
                            working = (self.root / cwd.value if isinstance(cwd, ast.Constant) and
                                       isinstance(cwd.value, str) else self.root / '${RUNTIME}')
                        calls.append((node.lineno, argument, working))
        declaration = self.table['scripts'].get(where)
        if network or calls:
            if declaration is None:
                raise Refusal(f'undeclared executing or network script {where!r}')
            if declaration['sha256'] != hashlib.sha256(source.encode()).hexdigest():
                raise Refusal(f'changed declared script {where!r}')
            if declaration['class'] not in ('installer', 'reviewed non-installing') or not declaration.get('reason'):
                raise Refusal(f'invalid script classification {where!r}')
            if declaration['class'] == 'installer':
                if not declaration.get('tools'):
                    raise Refusal(f'installer has no tool pins: {where}')
                return
        for line, argument, working in calls:
            for value in self.values(argument, assignments):
                if isinstance(value, str):
                    self.shell(value, f'{where}:{line}', working)
                else:
                    self.command(value, f'{where}:{line}', working)

    def values(self, node: ast.AST, assignments: dict, seen: frozenset = frozenset()) -> list:
        """Resolve literals and simple command aliases; record dynamic assembly."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return [node.value]
        if isinstance(node, (ast.List, ast.Tuple)):
            return [[n.value if isinstance(n, ast.Constant) and isinstance(n.value, str) else '<dynamic>'
                     for n in node.elts]]
        if isinstance(node, ast.Name) and node.id not in seen and node.id in assignments:
            return [value for expr in assignments[node.id]
                    for value in self.values(expr, assignments, seen | {node.id})]
        self.residue.add('Python command assembled at runtime')
        return []

    def shell(self, source: str, where: str, directory: Path | None = None) -> None:
        """Classify calls in the complete Bash AST, including function bodies."""
        script = self.root / where.split(':', 1)[0]
        if script.is_file() and script.suffix == '.sh':
            source = source.replace('$(dirname "$0")', str(script.parent))
        source = re.sub(r'\$\{\{.*?\}\}', '${RUNTIME}', source)
        try:
            tree = shell_tree(source, self.parser)
        except Refusal as error:
            raise Refusal(f'{where}: {error}') from error
        saved = self.functions
        self.functions = saved | {n['Name']['Value'] for n in nodes(tree) if n.get('Type') == 'FuncDecl'}
        try:
            for node in nodes(tree):
                if node.get('Type') != 'CallExpr':
                    continue
                for assignment in node.get('Assigns', []):
                    if assignment.get('Value'):
                        value = word(assignment['Value'])
                        for key, replacement in self.env.items():
                            value = value.replace('${' + key + '}', str(replacement))
                        self.env[assignment['Name']['Value']] = value
                if not node.get('Args'):
                    continue
                words = [word(arg) for arg in node['Args']]
                line = node['Pos']['Line']
                self.command(words, f'{where}:{line}', directory)
                if words[0] == 'cd' and len(words) > 1:
                    directory = (directory or self.root) / words[1]
            for node in nodes(tree):
                if 'Redirs' not in node or node.get('Cmd', {}).get('Type') != 'CallExpr':
                    continue
                words = [word(arg) for arg in node['Cmd'].get('Args', [])]
                for redirect in node['Redirs']:
                    if 'Hdoc' not in redirect:
                        continue
                    if words[:2] in (['python3', '-'], ['python', '-']):
                        self.python(word(redirect['Hdoc']), where + ':heredoc', directory or self.root)
                    elif words and words[0] in ('bash', 'sh'):
                        self.shell(word(redirect['Hdoc']), where + ':heredoc', directory)
        finally:
            self.functions = saved

    def installation(self, words: list[str], where: str) -> None:
        """Record supported workflow installers; refuse unreviewed script installers."""
        if not where.startswith('.github/workflows/') or self.install_reader is None:
            raise Refusal(f'installer needs an explicit pin reader at {where}: {shlex.join(words)}')
        self.requests.extend(self.install_reader(shlex.join(words), self.env, self.root))

    def command(self, words: list[str], where: str, directory: Path | None = None) -> None:
        """Dispatch only the finite handlers declared in the table."""
        if not words:
            return
        words = [re.sub(r'\$\{(\w+)\}', lambda m: str(self.env.get(m[1], m[0])), w) for w in words]
        name = words[0]
        if name in self.functions:
            return
        if '$' in name or '<dynamic>' in name:
            self.residue.add(f'{where}: runtime command name')
            return
        if name.endswith(('.py', '.sh')):
            self.script(name, where, directory)
            return
        key = name if name == "." else Path(name).name
        row = self.table['commands'].get(key)
        if row is None:
            raise Refusal(f'unclassified command {name!r} at {where}')
        prefixes = row.get('prefixes')
        if prefixes is not None and not any(words[1:1 + len(p)] == p for p in prefixes):
            raise Refusal(f'unclassified command {shlex.join(words)!r} at {where}')
        handler = row.get('handler')
        if row['class'] not in ('installer', 'non-installing'):
            raise Refusal(f'invalid command classification for {name!r}')
        if row['class'] == 'installer':
            if row.get('pin_reader') == 'copy':
                if len(words) > 2 and words[-2] in row.get('local_sources', []):
                    self.script(words[-2], where, directory)
                    return
                tool = row.get('destinations', {}).get(words[-1])
                if not tool or not any(r['tool'] == tool for r in self.requests):
                    raise Refusal(f'unbound installed tool at {where}')
            else:
                self.installation(words, where)
        if handler == 'residue':
            self.residue.add(f'{where}: runtime command evaluation')
        elif handler == 'source':
            if len(words) != 2:
                raise Refusal(f'unsupported source command at {where}')
            path = (directory or self.root) / words[1]
            self.script(words[1], where, directory)
            if path.is_file():
                tree = shell_tree(path.read_text(), self.parser)
                self.functions.update(n['Name']['Value'] for n in nodes(tree) if n.get('Type') == 'FuncDecl')
        elif handler == 'trap':
            if len(words) > 1 and words[1] != '-':
                self.shell(words[1], where, directory)
        elif handler == 'wrapper':
            self.wrapper_command(words, where, directory, row)
        elif handler == 'find':
            for index, arg in enumerate(words):
                if arg in ('-exec', '-execdir'):
                    rest = words[index + 1:]
                    end = next((i for i, token in enumerate(rest) if token in (';', '+')), None)
                    if end is None:
                        raise Refusal(f'unterminated find execution at {where}')
                    self.command(rest[:end], where, directory)
        elif handler == 'python':
            self.python_command(words, where, directory, row)
        elif handler == 'shell':
            self.shell_command(words, where, directory, row)
        elif handler == 'git':
            self.git_command(words, where, directory, row)
        elif handler == 'make':
            self.make_command(words, where, directory, row)
    def wrapper_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared wrapper command form and its executed children."""
        key = Path(words[0]).name
        rest = words[1:]
        if key == 'command' and rest[:1] in (['-v'], ['-V']):
            return
        while rest:
            if re.match(r'^\w+=', rest[0]):
                rest = rest[1:]
            elif rest[0] == '--':
                rest = rest[1:]
                break
            elif rest[0].startswith('-'):
                option = rest[0].split('=', 1)[0]
                attached = len(option) > 2 and row.get('options', {}).get(option[:2]) == 1
                if attached:
                    option = option[:2]
                if option not in row.get('options', {}):
                    raise Refusal(f'unclassified {key} option {option!r} at {where}')
                count = row['options'][option]
                rest = rest[1 + (count if '=' not in rest[0] and not attached else 0):]
            else:
                break
        rest = rest[row.get('operands', 0):]
        self.command(rest, where, directory)

    def python_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared python command form and its executed children."""
        rest = words[1:]
        while rest and rest[0] in ('-I', '-B', '-u'):
            rest.pop(0)
        if not rest or rest[0] in ('--version', '-V'):
            return
        if rest[:3] == ['-m', 'pip', 'install']:
            self.installation(['python3', *rest], where)
            return
        if rest[0] == '-c' and len(rest) > 1:
            self.python(rest[1], where, directory or self.root)
        elif rest[0] == '-m':
            raise Refusal(f'unclassified Python module at {where}')
        elif rest[0] != '-':
            self.script(rest[0], where, directory)

    def shell_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared shell command form and its executed children."""
        if '-c' in words:
            self.residue.add(f'{where}: indirect shell')
        else:
            rest = [w for w in words[1:] if not w.startswith('-')]
            if rest:
                self.script(rest[0], where, directory)

    def git_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared git command form and its executed children."""
        rest = words[1:]
        while rest and (rest[0] in ('-C', '-c', '--git-dir', '--work-tree', '--no-optional-locks')):
            rest = rest[1:] if rest[0] == '--no-optional-locks' else rest[2:]
        if rest and ('<dynamic>' in rest[0] or '$' in rest[0]):
            self.residue.add(f'{where}: runtime git subcommand')
            return
        if not rest or rest[0] not in row['subcommands']:
            raise Refusal(f'unclassified git command at {where}: {shlex.join(words)}')
        if rest[0] == 'clone':
            if '--no-hardlinks' not in rest or any('://' in arg for arg in rest):
                self.installation(['git', *rest], where)
        if rest[0] == 'fetch':
            args = [w for w in rest[1:] if not w.startswith('-')]
            if not args or args[0] != 'origin':
                raise Refusal(f'unclassified git fetch source at {where}')

    def make_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared make command form and its executed children."""
        target = directory or self.root
        if '$' in str(target) or str(target).startswith('/tmp/'):
            self.residue.add(f'{where}: runtime Makefile directory')
            return
        if '-C' in words:
            value = words[words.index('-C') + 1]
            if '$' in value or value.startswith('/tmp/') or '<dynamic>' in value:
                self.residue.add(f'{where}: external or runtime Makefile')
                return
            target = target / value
        name = words[words.index('-f') + 1] if '-f' in words else 'Makefile'
        if '$' in name or '<dynamic>' in name:
            self.residue.add(f'{where}: runtime Makefile path')
            return
        path = target / name
        if not path.is_file():
            raise Refusal(f'unresolved Makefile {path} at {where}')
        targets = []
        skip = False
        for word in words[1:]:
            if skip:
                skip = False
            elif word in ('-C', '-f', '-j', '--jobs'):
                skip = True
            elif not word.startswith('-') and '=' not in word:
                targets.append(word)
        self.makefile(path, targets)

    def make_expansions(self, source: str, where: str, directory: Path) -> str:
        """Separate make expansion from shell syntax and inspect shell functions."""
        output = []
        index = 0
        while index < len(source):
            if source.startswith('$(', index):
                start = index + 2
                end = start
                depth = 1
                while end < len(source) and depth:
                    depth += (source[end] == '(') - (source[end] == ')')
                    end += 1
                if depth:
                    raise Refusal(f'unclosed make expansion at {where}')
                value = self.make_expansions(source[start:end - 1], where, directory)
                if value.startswith('shell '):
                    self.shell(value[6:], where, directory)
                output.append('make' if value == 'MAKE' else '${RUNTIME}')
                self.residue.add(f'{where}: make expansion')
                index = end
            elif source[index:index + 1] == '$' and source[index + 1:index + 2] in ('@', '<', '^', '?', '*', '%', '+'):
                output.append('${RUNTIME}')
                index += 2
            elif source.startswith('$$', index):
                output.append('$')
                index += 2
            else:
                output.append(source[index])
                index += 1
        return ''.join(output)

    def makefile(self, path: Path, targets: list[str] | None = None) -> None:
        """Classify selected targets and dependencies, or the owned suite population."""
        relative = path.resolve().relative_to(self.root).as_posix()
        self.inputs[relative] = sha256(path)
        rules = {}
        current = []
        for number, line in enumerate(path.read_text().replace('\\\n', ' ').splitlines(), 1):
            if line.startswith('.RECIPEPREFIX'):
                raise Refusal(f'unsupported Makefile recipe prefix at {relative}:{number}')
            if not line.lstrip().startswith('#') and '$(shell ' in line and not line.startswith('\t'):
                self.make_expansions(line, f'{relative}:{number}', path.parent)
            if line.startswith('\t'):
                for target in current:
                    rules[target][1].append((number, line))
            elif line.startswith(('include ', '-include ')):
                for name in line.split()[1:]:
                    if '$' in name:
                        self.residue.add(f'{relative}:{number}: runtime Makefile include')
                    else:
                        self.script(name, relative, path.parent)
            elif ':' in line and not line.lstrip().startswith('#') and not re.match(r'^\w+\s*[:?+]?=', line):
                names, dependencies = line.split(':', 1)
                dependencies, separator, inline = dependencies.partition(';')
                current = names.split()
                for target in current:
                    rules.setdefault(target, (dependencies.split(), []))
                    if separator:
                        rules[target][1].append((number, inline))
        pending = list(rules) if targets is None else (targets or [next(iter(rules), '')])
        while pending:
            target = pending.pop()
            key = f'{relative}:{target}'
            if key in self.seen:
                continue
            self.seen.add(key)
            if target not in rules:
                continue
            dependencies, recipes = rules[target]
            pending.extend(d for d in dependencies if d in rules)
            for number, line in recipes:
                recipe = self.make_expansions(line.lstrip('\t@+-'), f'{relative}:{number}', path.parent)
                self.shell(recipe, f'{relative}:{number}', path.parent)
