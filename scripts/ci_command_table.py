#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Classify literal CI commands against a closed, reviewed command table."""

from __future__ import annotations

from collections.abc import Iterator
import hashlib
import json
import os
import subprocess
from pathlib import Path
import re
import shlex


TABLE = Path('ci/image/command-table.json')
RECEIPT = Path('ci/image/differential-receipt.json')
#: The walker sources and fixtures a differential receipt is bound to.
BOUND = ('ci_command_table.py', 'ci_python_walk.py', 'ci_shell_walk.py', 'ci_make_walk.py', 'ci_syntax.py',
         'ci_tool_inventory.py',
         'ci_differential.py', 'ci_differential_fixtures.py')
#: Only the differential harness walks without the census gate, to measure each fixture.
GATE = True
class Refusal(ValueError):
    """A literal command has no reviewed classification."""


class Runtime(str):
    """Mark a value derived from an expression, never from literal dollar text."""

    def replace(self, old: str, new: str, count: int = -1) -> Runtime:
        """Retain provenance when normalizing checkout paths."""
        return type(self)(super().replace(old, new, count))


class Fields(Runtime):
    """An unquoted runtime expansion: any number of runtime fields, never a literal."""


def _join(values: list[str]) -> str:
    # The analysed program's os.path.join, reproduced exactly for POSIX paths.
    result = values[0]
    for value in values[1:]:
        result = value if value.startswith('/') else (
            result + value if not result or result.endswith('/') else result + '/' + value)
    return result


def _dirname(value: str) -> str:
    # The analysed program's os.path.dirname: trailing separators of the head are removed.
    head = value[:value.rfind('/') + 1]
    return head.rstrip('/') if head and head != '/' * len(head) else head


def _normpath(value: str) -> str:
    # The analysed program's os.path.normpath: purely textual, so '..' never follows a link.
    slashes = 2 if value.startswith('//') and not value.startswith('///') else int(value.startswith('/'))
    parts = []
    for part in value.split('/'):
        if part in ('', '.'):
            continue
        if part == '..' and (parts and parts[-1] != '..' or slashes):
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return '/' * slashes + '/'.join(parts) or '.'


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


def binding(census: dict) -> str:
    """Identify the walker, its fixtures and the census shapes a differential receipt measured."""
    here = Path(__file__).resolve().parent
    files = {name: hashlib.sha256((here / name).read_bytes()).hexdigest() for name in BOUND}
    return hashlib.sha256(json.dumps({'files': files, 'shapes': census.get('shapes', {})},
                                     sort_keys=True).encode()).hexdigest()


def shell_tree(source: str, parser: Path, dialect: str = 'bash') -> dict:
    """Parse Bash or POSIX shell syntax without executing any candidate command."""
    result = subprocess.run([str(parser), '-ln', 'bash' if dialect == 'bash' else 'posix', '--to-json'],
                            input=source, text=True, capture_output=True, check=False)
    if result.returncode:
        raise Refusal('shell parse failed: ' + result.stderr.strip())
    return json.loads(result.stdout)


from ci_python_walk import PythonWalk  # noqa: E402 - the mixin uses the helpers above


class Audit(PythonWalk):
    """Bind every literal command and followed script to one committed table."""

    def __init__(self, root: Path, inputs: dict[str, str]) -> None:
        self.root = root.resolve()
        self.inputs = inputs
        self.table = json.loads((root / TABLE).read_text())
        self.inputs[str(TABLE)] = sha256(root / TABLE)
        census = root / 'ci/image/syntax-census.json'
        self.census = json.loads(census.read_text())
        self.inputs['ci/image/syntax-census.json'] = sha256(census)
        self.shapes_used: dict[str, str] = {}
        self.inspecting = 0
        self.accepted = self.accepted_shapes(root) if GATE else None
        self.exported_env = {}
        self.make_builtins = None
        self.runtime_directories = set()
        self.seen: set[str] = set()
        self.external_builds: set[Path] = set()
        self.installed_scripts: dict[str, str] = {}
        self.residue: set[str] = set()
        self.modules: dict[str, list[Path]] | None = None
        self.facts: dict[str, tuple] = {}
        self.python_context: tuple | None = None
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

    def accepted_shapes(self, root: Path) -> set[str]:
        """Census shapes whose differential fixture resolved as the real tool did, at this walker."""
        receipt_path = root / RECEIPT
        receipt = json.loads(receipt_path.read_text())
        self.inputs[str(RECEIPT)] = sha256(receipt_path)
        if receipt.get('binding') != binding(self.census):
            raise Refusal('differential receipt does not match the walker, fixtures and census shapes; '
                          'run the differential harness in the image')
        results = receipt.get('fixtures', {})
        # Resolution shapes resolve identically or as located residue; detection shapes refuse
        # an undeclared program the real tool shows executing.
        return {shape for shape, fixture in self.census.get('shapes', {}).items()
                if results.get(fixture, {}).get('outcome') in ('identical', 'residue', 'refused') and
                results[fixture]['outcome'] == results[fixture].get('expect') and
                shape in results[fixture].get('shapes', [])}

    def shape(self, name: str, where: str) -> None:
        """Every rule the walker applies is a census shape with a passing differential fixture."""
        self.shapes_used.setdefault(name, where)
        if self.accepted is not None and name not in self.accepted:
            raise Refusal(f'uncensused construct shape {name!r} at {where}')

    def script(self, name: str, where: str, directory: Path | None = None,
               working: Path | None = None, kind: str = '') -> None:
        """Follow resolved scripts, refusing absent literal paths.

        `kind` is `module` for an imported module, `bash` or `sh` for the shell that
        reads a script, and `isolated` for a `python3 -I` program.
        """
        module, isolated = kind == 'module', kind == 'isolated'
        dialect = kind if kind in ('bash', 'sh') else 'bash'
        if name in self.installed_scripts:
            self.script(self.installed_scripts[name], where, self.root)
            return
        if isinstance(name, Runtime):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'unclassified runtime command name {name!r} at {where}')
            self.shape('cmd:runtime-script', where)
            self.residue.add(f'{where}: runtime script path')
            return
        if directory and any(directory.is_relative_to(p) for p in self.runtime_directories):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'script {name!r} in an unknown directory at {where}')
            self.shape('cmd:runtime-directory', where)
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
        program = path.suffix == '.py' and not module
        search = self.python_context[0] if module and self.python_context else None
        key = (relative, str(working), program, search, self.incoming_state(), dialect, isolated)
        if key in self.seen:
            return
        self.seen.add(key)
        self.inputs[relative] = sha256(path)
        if program:
            self.python_program(path, relative, working, isolated)
        elif path.suffix == '.py':
            self.python(path.read_text(), relative, working)
        elif path.suffix == '.sh':
            self.shell(path.read_text(), relative, directory or self.root, str(name), dialect)
        elif path.name == 'Makefile' or path.suffix == '.mk':
            self.makefile(path)
        else:
            raise Refusal(f'unsupported script language {relative!r} at {where}')

    def incoming_state(self) -> tuple:
        """Everything a child process inherits that changes its command population."""
        def frozen(values: dict) -> tuple:
            """Order values and keep runtime provenance distinct from equal literal text."""
            return tuple(sorted((k, v, isinstance(v, Runtime)) for k, v in values.items()))
        return frozen(self.exported_env)

    def shell(self, source: str, where: str, directory: Path | None = None, argv0: str | None = None,
              dialect: str = 'bash') -> None:
        """Walk the supported syntax with lexical directory and function scope."""
        from ci_shell_walk import Shell
        Shell(self, where, argv0, dialect).run(source, directory or self.root)

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
            # A file run directly is read by the interpreter its first line names.
            path = (directory or self.root) / name
            first = path.read_text().split('\n', 1)[0] if path.is_file() else ''
            interpreter = {'#!/bin/bash': 'bash', '#!/usr/bin/env bash': 'bash', '#!/bin/sh': 'sh',
                           '#!/usr/bin/env python3': 'python'}.get(first.strip())
            if interpreter is None or (interpreter == 'python') != name.endswith('.py'):
                raise Refusal(f'unmodelled interpreter line {first.strip()!r} for {name!r} at {where}')
            self.shape(f'cmd:direct.{interpreter}', where)
            self.script(name, where, directory, kind='' if interpreter == 'python' else interpreter)
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
        if handler not in ('python', 'shell', 'make'):  # Those record their own exact forms.
            self.shape(f'cmd:{handler or "table"}' + (f'.{key}' if handler == 'wrapper' else ''), where)
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
                    # find replaces {} with each found path at run time.
                    self.command([Runtime(w) if '{}' in w else w for w in rest[:end]], where, directory)
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
        if isinstance(expected, dict) and expected == {'data_file': True}:
            # A fixed program's input file is data; the table never copies a host path.
            accepted = not isinstance(argument, Runtime) and not argument.startswith('-') and argument != ''
        elif isinstance(expected, dict):
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
        replace = None
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
                if key == 'xargs' and option == '-I':
                    replace = rest[0][2:] if attached else rest[1]
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
        if key == 'xargs':
            # Input items replace the -I string, or are appended as further arguments.
            rest = [Runtime(w) if replace and replace in w else w for w in rest] + \
                ([] if replace else [Fields('xargs input')])
        self.command(rest, where, directory)

    def python_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Follow files or match an exact, reviewed inline program."""
        rest = words[1:]
        flags = set()
        while rest and rest[0] in ('-I', '-B', '-u'):
            flags.add(rest[0])
            rest = rest[1:]
        if rest in (['--version'], ['-V']):
            self.shape('cmd:python.version', where)
            return
        for form in row.get('installer_forms', []):
            prefix = form['prefix']
            if rest[:len(prefix)] == prefix:
                self.shape('cmd:python.installer', where)
                self.installation(['python3', *rest], where, directory)
                return
        if rest[:1] == ['-c'] and len(rest) >= 2:
            pin = hashlib.sha256(rest[1].encode()).hexdigest()
            entry = self.table.get('inline', {}).get(words[0] + ':' + pin)
            if not entry or not entry.get('reason'):
                raise Refusal(f'unclassified inline interpreter text at {where}')
            if Path(words[0]).name.startswith('python'):
                self.shape('cmd:python.inline', where)
                # A reviewed program is pinned by digest, not walked: what it runs is declared residue.
                self.residue.add(f'{where}: declared inline interpreter program')
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
        if not isinstance(rest[0], Runtime) and not str(rest[0]).endswith('.py'):
            raise Refusal(f'unsupported script language {rest[0]!r} at {where}')
        self.shape('cmd:python.isolated-script' if '-I' in flags else 'cmd:python.script', where)
        self.script(rest[0], where, directory, kind='isolated' if '-I' in flags else '')

    def shell_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Refuse literal interpreter text; retain declared runtime execution."""
        rest = words[1:]
        if len(rest) == 2 and rest[0] == '-n':
            self.shape('cmd:shell.syntax-check', where)
            return
        if rest[:2] == ['-euo', 'pipefail']:
            rest = rest[2:]
        if rest[:1] == ['-c'] and len(rest) == 2 and isinstance(rest[1], Runtime):
            if not self.table['scripts'].get(where.split(':')[0]):
                raise Refusal(f'undeclared runtime shell program at {where}')
            self.shape('cmd:shell.runtime-inline', where)
            self.residue.add(f'{where}: declared runtime shell program')
            return
        dialect = 'bash' if Path(words[0]).name == 'bash' else 'sh'
        if rest[:1] == ['-c'] and len(rest) >= 2:
            self.shape(f'cmd:shell.inline.{dialect}', where)
            self.python_command([words[0], *rest[:2]], where, directory, {})
            self.shell(rest[1], where, directory, dialect=dialect)
            return
        if not rest or rest[0].startswith('-'):
            raise Refusal(f'unclassified shell invocation at {where}: {shlex.join(words)}')
        if not str(rest[0]).endswith('.sh') and not isinstance(rest[0], Runtime):
            raise Refusal(f'unsupported script language {rest[0]!r} at {where}')
        self.shape(f'cmd:shell.script.{dialect}', where)
        self.script(rest[0], where, directory, kind=dialect)

    def git_command(self, words: list[str], where: str, directory: Path | None, row: dict) -> None:
        """Require a complete positively classified Git argument form."""
        normalized = [normalize(w, self.root) for w in words[1:]]
        if not any(self.matches(normalized, p) for p in row['patterns']):
            raise Refusal(f'unclassified git command at {where}: {shlex.join(words)}')
        rest = words[1:]
        while rest and rest[0] in ('-C', '-c', '--no-optional-locks'):
            rest = rest[1:] if rest[0] == '--no-optional-locks' else rest[2:]
        if not rest or isinstance(rest[0], Runtime):
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
        if any(isinstance(w, Runtime) and w == '<dynamic>' for w in words) and any(
                self.matches(normalized, p) for p in row['patterns']):
            self.residue.add(f'{where}: declared runtime Make invocation')
            return
        invocation(self, words, where, directory or self.root)

    def makefile(self, path: Path, targets: list[str] | None = None, overrides: dict | None = None,
                 directory: Path | None = None, flags: tuple = (frozenset(), 0)) -> None:
        """Classify reachable rules using the supported Make semantics; `flags` are letters and level."""
        from ci_make_walk import Makefile
        Makefile(self, path, overrides or {}, directory, flags).walk(targets)
