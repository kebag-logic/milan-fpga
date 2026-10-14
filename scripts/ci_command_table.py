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
NETWORK = {'urllib', 'http', 'requests', 'socket', 'ftplib', 'urllib3', 'ssl', 'pip', 'socketserver'}
CALLS = {'run', 'check_call', 'check_output', 'Popen', 'call', 'system', 'getoutput', 'getstatusoutput'}


class Refusal(ValueError):
    """A literal command has no reviewed classification."""


class Runtime(str):
    """Mark a value derived from an expression, never from literal dollar text."""

    def replace(self, old: str, new: str, count: int = -1) -> Runtime:
        """Retain provenance when normalizing checkout paths."""
        return Runtime(super().replace(old, new, count))


def normalize(value: str, root: Path) -> str:
    """Replace leading path components, including compiler include operands."""
    pattern = r'(^|(?<=\s)|(?<=-I)|(?<=\+incdir\+))' + re.escape(str(root)) + r'(?=/|$)'
    result = re.sub(pattern, lambda match: match[1] + '${CHECKOUT}', value)
    return Runtime(result) if isinstance(value, Runtime) else result


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
        census = root / 'ci/image/syntax-census.json'
        self.census = json.loads(census.read_text())
        self.inputs['ci/image/syntax-census.json'] = sha256(census)
        self.exported_env = {}
        self.make_overrides = {}
        self.runtime_directories = set()
        self.seen: set[str] = set()
        self.external_builds: set[Path] = set()
        self.installed_scripts: dict[str, str] = {}
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

    def script(self, name: str, where: str, directory: Path | None = None,
               working: Path | None = None) -> None:
        """Follow resolved scripts, refusing absent literal paths."""
        if name in self.installed_scripts:
            self.script(self.installed_scripts[name], where, self.root)
            return
        if isinstance(name, Runtime):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'unclassified runtime command name {name!r} at {where}')
            self.residue.add(f'{where}: runtime script path')
            return
        if directory and any(directory.is_relative_to(p) for p in self.runtime_directories):
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
        working = working or directory or self.root
        key = (relative, str(working))
        if key in self.seen:
            return
        self.seen.add(key)
        self.inputs[relative] = sha256(path)
        if path.suffix == '.py':
            self.python(path.read_text(), relative, working)
        elif path.suffix == '.sh':
            self.shell(path.read_text(), relative, directory or self.root)
        elif path.name == 'Makefile' or path.suffix == '.mk':
            self.makefile(path)
        else:
            raise Refusal(f'unsupported script language {relative!r} at {where}')

    def python(self, source: str, where: str, directory: Path) -> None:
        """Detect capabilities independently of decoding, then classify literal calls."""
        tree = ast.parse(source)
        from ci_syntax import python_nodes
        python_nodes(self, tree, where)
        declaration = self.table['scripts'].get(where)
        aliases = {}
        assignments = {}
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    bound = alias.asname or alias.name.split('.')[0]
                    aliases[bound] = alias.name if alias.asname else bound
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append('.' * node.level + (node.module or ''))
                for alias in node.names:
                    if alias.name != '*':
                        imports.append('.' * node.level + (node.module + '.' if node.module else '') + alias.name)
                for alias in node.names:
                    aliases[alias.asname or alias.name] = (node.module or '') + '.' + alias.name
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments.setdefault(target.id, []).append(node.value)
        def qualified(node: ast.AST) -> str:
            """Resolve imported aliases without evaluating expressions."""
            if isinstance(node, ast.Name):
                return aliases.get(node.id, node.id)
            if isinstance(node, ast.Attribute):
                return qualified(node.value) + '.' + node.attr
            return ''
        capability = False
        for name in imports:
            local = self.python_import(name, where, directory)
            if not local and not any(name == allowed or name.startswith(allowed + '.')
                                     for allowed in self.table.get('python_imports', [])):
                capability = True
            if name.split('.')[0] in NETWORK | {
                    'subprocess', 'pty', 'asyncio', 'multiprocessing', 'ctypes', 'cffi'}:
                capability = True
        for name, expressions in assignments.items():
            if len(expressions) == 1 and isinstance(expressions[0], (ast.Name, ast.Attribute)):
                aliases[name] = qualified(expressions[0])
        calls = []
        for node in ast.walk(tree):
            symbol = qualified(node) if isinstance(node, (ast.Name, ast.Attribute)) else ''
            if symbol.startswith(('os.exec', 'os.spawn', 'os.posix_spawn', 'subprocess.', 'pty.',
                                  'asyncio.create_subprocess', 'ctypes.', 'cffi.')) or \
                    symbol in ('os.system', 'os.popen'):
                capability = True
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function = qualified(node.func)
            executor = ((function.startswith('subprocess.') and function.split('.')[-1] in CALLS) or
                        function.startswith(('pty.', 'asyncio.create_subprocess',
                                             'os.exec', 'os.spawn', 'os.posix_spawn')) or
                        function in ('os.system', 'os.popen'))
            if function in ('eval', 'exec', 'getattr', '__import__', 'importlib.import_module'):
                capability |= function != 'getattr'
                self.residue.add(f'{where}:{node.lineno}: runtime Python execution or lookup')
            if not executor:
                continue
            capability = True
            keywords = {}
            for keyword in node.keywords:
                if keyword.arg is not None:
                    keywords[keyword.arg] = keyword.value
                elif isinstance(keyword.value, ast.Dict):
                    for key, value in zip(keyword.value.keys, keyword.value.values):
                        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                            raise Refusal(f'unsupported Python keyword unpacking at {where}:{node.lineno}')
                        keywords[key.value] = value
                else:
                    self.residue.add(f'{where}:{node.lineno}: runtime Python keyword unpacking')
            argument = keywords.get('args', node.args[0] if node.args else None)
            if function.startswith(('os.exec', 'os.spawn', 'os.posix_spawn', 'pty.', 'asyncio.')):
                raise Refusal(f'unclassified Python execution {function!r} at {where}:{node.lineno}')
            working = directory
            cwd = keywords.get('cwd')
            if cwd is not None:
                working = directory / (cwd.value if isinstance(cwd, ast.Constant) and
                                       isinstance(cwd.value, str) else '${RUNTIME}')
                if not isinstance(cwd, ast.Constant) or not isinstance(cwd.value, str):
                    self.runtime_directories.add(working)
            executable = keywords.get('executable')
            calls.append((node.lineno, argument, working, executable))
        if capability:
            if declaration is None:
                raise Refusal(f'undeclared executing or network script {where!r}')
            if declaration['sha256'] != hashlib.sha256(source.encode()).hexdigest():
                raise Refusal(f'changed declared script {where!r}')
            if declaration['class'] not in ('installer', 'reviewed non-installing') or not declaration.get('reason'):
                raise Refusal(f'invalid script classification {where!r}')
        self.python_calls(calls, assignments, where)

    def python_import(self, name: str, where: str, directory: Path) -> bool:
        """Follow package initializers and members before considering external imports."""
        level = len(name) - len(name.lstrip('.'))
        origin = (self.root / where).parent
        bases = [origin.parents[level - 2] if level > 1 else origin] if level else [
            origin, self.root, self.root / 'scripts']
        parts = name.lstrip('.').split('.')
        for base in bases:
            local = False
            cursor = base
            for part in parts:
                cursor = cursor / part
                module = cursor.with_suffix('.py')
                initializer = cursor / '__init__.py'
                if initializer.is_file():
                    self.script(str(initializer), where, base, directory)
                    local = True
                elif module.is_file():
                    self.script(str(module), where, base, directory)
                    return True
                elif cursor.is_dir():
                    raise Refusal(f'unsupported Python namespace package {name!r} at {where}')
                else:
                    break
            if local:
                return True
        if level:
            raise Refusal(f'unresolved relative Python import {name!r} at {where}')
        return False

    def python_calls(self, calls: list[tuple], assignments: dict, where: str) -> None:
        """Classify decoded command and executable-override arguments."""
        for line, argument, working, executable in calls:
            overrides = self.values(executable, assignments, where=f'{where}:{line}') if executable else []
            for value in self.values(argument, assignments, where=f'{where}:{line}'):
                if isinstance(value, str):
                    self.shell(value, f'{where}:{line}', working)
                else:
                    self.command(value, f'{where}:{line}', working)
                for override in overrides:
                    if not isinstance(override, str):
                        raise Refusal(f'unsupported executable override at {where}:{line}')
                    argv = [override, *value[1:]] if isinstance(value, list) else [override, value]
                    self.command(argv, f'{where}:{line}', working)

    def values(self, node: ast.AST, assignments: dict, seen: frozenset = frozenset(), where: str = '') -> list:
        """Resolve literal command data; locate every unresolved assembly."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return [node.value]
        if isinstance(node, (ast.List, ast.Tuple)):
            return [[n.value if isinstance(n, ast.Constant) and isinstance(n.value, str) else Runtime('<dynamic>')
                     for n in node.elts]]
        if isinstance(node, ast.Name) and node.id not in seen and node.id in assignments:
            return [value for expr in assignments[node.id]
                    for value in self.values(expr, assignments, seen | {node.id}, where)]
        self.residue.add(f'{where}: Python command assembled at runtime')
        return []

    def shell(self, source: str, where: str, directory: Path | None = None) -> None:
        """Walk the supported syntax with lexical directory and function scope."""
        from ci_shell_walk import Shell
        Shell(self, where).run(source, directory or self.root)

    def installation(self, words: list[str], where: str, directory: Path | None = None) -> None:
        """Record supported workflow installers; refuse unreviewed script installers."""
        if not where.startswith('.github/workflows/') or self.install_reader is None:
            raise Refusal(f'installer needs an explicit pin reader at {where}: {shlex.join(words)}')
        self.requests.extend(self.install_reader(shlex.join(words), self.env, directory or self.root))

    def command(self, words: list[str], where: str, directory: Path | None = None) -> None:
        """Dispatch only the finite handlers declared in the table."""
        if not words:
            return
        name = words[0]
        if name in self.functions:
            return
        if isinstance(name, Runtime):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'unclassified runtime command name {name!r} at {where}')
            self.residue.add(f'{where}: runtime command name')
            return
        if name.endswith(('.py', '.sh')):
            self.script(name, where, directory)
            return
        key = name if name == "." else Path(name).name
        row = self.table['commands'].get(key)
        if row is None or normalize(name, self.root) not in row.get('executables', [key]):
            raise Refusal(f'unclassified command {name!r} at {where}')
        patterns = row.get('patterns', row.get('prefixes', []))
        normalized = [normalize(w, self.root) for w in words[1:]]
        if not row.get('handler') and not any(self.matches(normalized, pattern) for pattern in patterns):
            raise Refusal(f'unclassified command {shlex.join(words)!r} at {where}')
        handler = row.get('handler')
        if row['class'] not in ('installer', 'non-installing'):
            raise Refusal(f'invalid command classification for {name!r}')
        if row['class'] == 'installer':
            if row.get('pin_reader') == 'copy':
                if len(words) > 2 and words[-2] in row.get('local_sources', []):
                    self.script(words[-2], where, directory)
                    self.installed_scripts[words[-1]] = words[-2]
                    return
                tool = row.get('destinations', {}).get(words[-1])
                if not tool or not any(r['tool'] == tool for r in self.requests):
                    raise Refusal(f'unbound installed tool at {where}')
            else:
                self.installation(words, where, directory)
        if handler == 'data':
            self.data_command(words, where)
        elif handler == 'residue':
            raise Refusal(f'unclassified evaluation command at {where}')
        elif handler == 'source':
            raise Refusal(f'unfollowed source command at {where}')
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
            if not any(self.matches(normalized, p) for p in row['patterns']):
                raise Refusal(f'unclassified find argument form at {where}')
        elif handler == 'python':
            self.python_command(words, where, directory, row)
        elif handler == 'shell':
            self.shell_command(words, where, directory, row)
        elif handler == 'git':
            self.git_command(words, where, directory, row)
        elif handler == 'make':
            self.make_command(words, where, directory, row)
    def data_command(self, words: list[str], where: str) -> None:
        """Data builtins cannot acquire variable-writing or evaluation options."""
        name, args = words[0], words[1:]
        if name == 'printf':
            delimited = args[:1] == ['--']
            if delimited:
                args = args[1:]
            if (not args or (not delimited and args[0].startswith('-')) or
                    re.search(r'%[-+ #0]*[0-9*]*(?:\.[0-9*]+)?n', args[0])):
                raise Refusal(f'uncensused printf option or variable write at {where}')
        elif name in ('test', '['):
            allowed = self.census['shell_test_operators']
            for argument in args:
                if (not isinstance(argument, Runtime) and argument.startswith('-') and
                        argument not in allowed):
                    raise Refusal(f'uncensused test operator {argument!r} at {where}')
        elif name in ('exit', 'return', 'break', 'continue'):
            if len(args) > 1 or (args and not isinstance(args[0], Runtime) and not args[0].isdigit()):
                raise Refusal(f'uncensused {name} operand at {where}')
        elif name not in ('echo', 'shift', ':', 'true', 'false'):
            raise Refusal(f'uncensused data builtin {name!r} at {where}')

    @staticmethod
    def matches(args: list[str], pattern: list[str]) -> bool:
        """Match complete argv; runtime slots cannot authorize literal options."""
        if not pattern:
            return not args
        expected = pattern[0]
        if isinstance(expected, dict) and set(expected) == {'data_paths'}:
            # A recipe owns its source population; the table never copies it.
            for count in range(1, len(args) + 1):
                if not Audit.matches([args[count - 1]], [{'data_path': expected['data_paths']}]):
                    break
                if Audit.matches(args[count:], pattern[1:]):
                    return True
            return False
        if not args:
            return False
        argument = args[0]
        if isinstance(expected, dict):
            suffix = expected.get('data_path')
            accepted = (set(expected) == {'data_path'} and suffix in ('.sv', '.svh') and
                        not isinstance(argument, Runtime) and not argument.startswith('-') and
                        argument.endswith(suffix))
        elif expected == '<runtime>':
            accepted = isinstance(argument, Runtime)
        else:
            accepted = argument == expected
        return accepted and Audit.matches(args[1:], pattern[1:])

    def wrapper_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Classify the declared wrapper command form and its executed children."""
        key = Path(words[0]).name
        rest = words[1:]
        if key == 'xargs' and not any(self.matches(rest, p) for p in row['patterns']):
            raise Refusal(f'uncensused xargs child form at {where}')
        if key == 'command' and rest[:1] in (['-v'], ['-V']):
            return
        while rest:
            if re.match(r'^\w+=', rest[0]):
                from ci_syntax import SENSITIVE
                variable, value = rest[0].split('=', 1)
                if variable in SENSITIVE:
                    raise Refusal(f'uncensused wrapper environment {variable!r} at {where}')
                self.exported_env[variable] = Runtime(value) if isinstance(rest[0], Runtime) else value
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
                if key == 'env':
                    if option in ('-i', '--ignore-environment'):
                        self.exported_env = {}
                    elif option in ('-u', '--unset'):
                        variable = rest[0].split('=', 1)[1] if '=' in rest[0] else rest[1]
                        self.exported_env.pop(variable, None)
                rest = rest[1 + (count if '=' not in rest[0] and not attached else 0):]
            else:
                break
        rest = rest[row.get('operands', 0):]
        if not rest and key not in ('exec', 'flock'):
            raise Refusal(f'missing wrapper command at {where}')
        self.command(rest, where, directory)

    def python_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Follow files or match an exact, reviewed inline program."""
        rest = words[1:]
        while rest and rest[0] in ('-I', '-B', '-u'):
            rest = rest[1:]
        if rest in (['--version'], ['-V']):
            return
        for form in row.get('installer_forms', []):
            prefix = form['prefix']
            if rest[:len(prefix)] == prefix:
                self.installation(['python3', *rest], where, directory)
                return
        if rest[:1] == ['-c'] and len(rest) >= 2:
            pin = hashlib.sha256(rest[1].encode()).hexdigest()
            entry = self.table.get('inline', {}).get(words[0] + ':' + pin)
            if not entry or not entry.get('reason'):
                raise Refusal(f'unclassified inline interpreter text at {where}')
            for index in entry.get('follow_args', []):
                if len(rest) <= index + 2:
                    raise Refusal(f'missing inline file argument at {where}')
                self.script(rest[index + 2], where, directory)
            if entry['class'] == 'installer':
                self.requests.extend(entry['tools'])
            elif entry['class'] != 'non-installing':
                raise Refusal(f'invalid inline classification at {where}')
            return
        if not rest or rest[0].startswith('-'):
            raise Refusal(f'unclassified Python invocation at {where}: {shlex.join(words)}')
        self.script(rest[0], where, directory)

    def shell_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Refuse literal interpreter text; retain declared runtime execution."""
        rest = words[1:]
        if len(rest) == 2 and rest[0] == '-n':
            return
        if rest[:2] == ['-euo', 'pipefail']:
            rest = rest[2:]
        if rest[:1] == ['-c'] and len(rest) == 2 and isinstance(rest[1], Runtime):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'undeclared runtime shell program at {where}')
            self.residue.add(f'{where}: declared runtime shell program')
            return
        if rest[:1] == ['-c'] and len(rest) >= 2:
            self.python_command([words[0], *rest[:2]], where, directory, {})
            self.shell(rest[1], where, directory)
            return
        if not rest or rest[0].startswith('-'):
            raise Refusal(f'unclassified shell invocation at {where}: {shlex.join(words)}')
        self.script(rest[0], where, directory)

    def git_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Require a complete positively classified Git argument form."""
        normalized = [normalize(w, self.root) for w in words[1:]]
        if not any(self.matches(normalized, p) for p in row['patterns']):
            raise Refusal(f'unclassified git command at {where}: {shlex.join(words)}')
        rest = words[1:]
        while rest and rest[0] in ('-C', '-c', '--no-optional-locks'):
            rest = rest[1:] if rest[0] == '--no-optional-locks' else rest[2:]
        if not rest or '$' in rest[0] or '<dynamic>' in rest[0]:
            self.residue.add(f'{where}: declared runtime git subcommand')
        elif rest[0] == 'clone':
            self.installation(['git', *rest], where, directory)
            destination = rest[-1]
            if '$' not in destination:
                self.external_builds.add(((directory or self.root) / destination).resolve())

    def make_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Resolve selected Makefiles before inspecting their recipes."""
        from ci_make_walk import invocation
        normalized = [normalize(w, self.root) for w in words[1:]]
        if '<dynamic>' in ' '.join(words) and any(self.matches(normalized, p) for p in row['patterns']):
            self.residue.add(f'{where}: declared runtime Make invocation')
            return
        invocation(self, words, where, directory or self.root)

    def makefile(self, path: Path, targets: list[str] | None = None, overrides: dict | None = None,
                 directory: Path | None = None) -> None:
        """Classify reachable rules using the supported Make semantics."""
        from ci_make_walk import Makefile
        Makefile(self, path, overrides or {}, directory).walk(targets)
