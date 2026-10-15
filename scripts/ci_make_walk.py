#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Resolve the censused Make subset without running make or shell commands."""

from pathlib import Path
import glob
import json
import re

from ci_command_table import Refusal, Runtime, sha256
from ci_syntax import SENSITIVE


BUILTINS = Path('ci/image/make-builtins.json')
#: File search and make-maintained state change selection; neither is modelled.
UNMODELLED = {'VPATH', 'GPATH', 'MAKEFILE_LIST', 'MAKE_RESTARTS', 'MAKE_TERMOUT', 'MAKE_TERMERR'}
#: The one censused MAKEFLAGS line: it removes the recorded built-in rules.
NO_BUILTIN_RULES = 'MAKEFLAGS += -r'
NAME = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
#: Flags make passes to a child through MAKEFLAGS that the walker reads: silent, dry run,
#: always remake, no built-in rules and print directory. Others refuse.
LETTERS = set('sBnrw')
#: Variables make itself sets in a recipe's environment.
MAKE_EXPORTS = {'MAKEFLAGS', 'MAKELEVEL', 'MFLAGS'}


class MakeFlags(str):
    """The MAKEFLAGS a make passes to its recipes, with the flags and variables it encodes."""

    def __new__(cls, letters: frozenset, overrides: dict) -> 'MakeFlags':
        variables = ' '.join(f'{key}={value}' for key, value in sorted(overrides.items()))
        text = ''.join(sorted(letters)) + (' -- ' + variables if variables else '')
        result = super().__new__(cls, text)
        result.letters, result.overrides = frozenset(letters), dict(overrides)
        return result


def inherited_flags(value: str | None, where: str) -> tuple[frozenset, dict]:
    """Read the MAKEFLAGS a child make receives: its flag letters and command-line variables."""
    if value is None:
        return frozenset(), {}
    if isinstance(value, MakeFlags):
        return value.letters, value.overrides
    if dynamic(value):
        raise Refusal(f'unmodelled runtime MAKEFLAGS at {where}')
    head, separator, tail = (' ' + value).partition(' -- ')
    words = head.split()
    letters = set(words[0]) if words and not words[0].startswith('-') else set()
    if letters - LETTERS or any(not re.fullmatch(r'--no-print-directory', w) for w in words[1 if letters else 0:]):
        raise Refusal(f'unmodelled MAKEFLAGS {value!r} at {where}')
    overrides = {}
    for word in tail.split():
        if '=' not in word or '\\' in word:
            raise Refusal(f'unmodelled MAKEFLAGS variable {word!r} at {where}')
        key, _, text = word.partition('=')
        overrides[key] = text
    return frozenset(letters), overrides


def dynamic(value: str) -> bool:
    """Only unresolved source values are runtime residue, never host locations."""
    return isinstance(value, Runtime)


def top_level(text: str, characters: str) -> int:
    """First character outside any reference, as make scans a line before expansion."""
    index = 0
    while index < len(text):
        if text.startswith('$$', index):
            index += 2
            continue
        if text.startswith(('$(', '${'), index):
            opening, closing = text[index + 1], ')' if text[index + 1] == '(' else '}'
            depth, index = 1, index + 2
            while index < len(text) and depth:
                depth += (text[index] == opening) - (text[index] == closing)
                index += 1
            continue
        if text[index] in characters:
            return index
        index += 1
    return -1


def logical_lines(text: str, where: str) -> list[tuple[int, list[str]]]:
    """Group physical lines joined by an odd number of trailing backslashes."""
    result, current, start = [], [], 0
    for number, line in enumerate(text.split('\n'), 1):
        if not current:
            start = number
        current.append(line)
        backslashes = len(line) - len(line.rstrip('\\'))
        if backslashes and backslashes % 2 == 0:
            raise Refusal(f'unmodelled escaped Make line end at {where}:{number}')
        if backslashes % 2 == 0:
            result.append((start, current))
            current = []
    if current:
        result.append((start, current))
    return result


def condensed(lines: list[str]) -> str:
    """Join a non-recipe line: each backslash-newline and its surrounding blanks become one space."""
    return re.sub(r'(?:[ \t]*\\\n)+[ \t]*', ' ', '\n'.join(lines))


def uncommented(text: str, where: str) -> str:
    """Drop a comment; escaped number signs are not modelled."""
    if '\\#' in text:
        raise Refusal(f'unmodelled escaped Make number sign at {where}')
    index = top_level(text, '#')
    return text if index < 0 else text[:index]


def recipe_lines(text: str) -> list[str]:
    """Split an expanded recipe at newlines that no odd run of backslashes continues."""
    lines, current = [], ''
    for part in text.split('\n'):
        current += part
        if (len(current) - len(current.rstrip('\\'))) % 2:
            current += '\n'
            continue
        lines.append(current)
        current = ''
    return [*lines, current] if current else lines


def split_order(dependencies: list[str]) -> tuple[list[str], list[str]]:
    """Separate normal prerequisites from order-only ones after the bar."""
    if '|' not in dependencies:
        return list(dependencies), []
    index = dependencies.index('|')
    return dependencies[:index], [d for d in dependencies[index + 1:] if d != '|']


def make_abspath(name: str, start: str) -> str:
    """GNU Make 4.3's `abspath`: lexical, so `..` never follows a link, and separators collapse."""
    parts = [] if name.startswith('/') else [p for p in start.split('/') if p]
    for part in name.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return '/' + '/'.join(parts)


def builtin_database(audit: object) -> dict:
    """Load the recorded built-in rules and defaults once per derivation."""
    if audit.make_builtins is None:
        audit.make_builtins = json.loads((audit.root / BUILTINS).read_text())
        audit.inputs[BUILTINS.as_posix()] = sha256(audit.root / BUILTINS)
    return audit.make_builtins


def invocation(audit: object, words: list[str], where: str, directory: Path) -> None:
    """Parse complete option operands before selecting a file and targets."""
    filename = 'Makefile'
    file_selected = False
    targets = []
    letters, inherited = inherited_flags(audit.exported_env.get('MAKEFLAGS'), where)
    letters, overrides = set(letters), dict(inherited)
    level = audit.exported_env.get('MAKELEVEL', '0')
    if dynamic(level) or not level.isdigit():
        raise Refusal(f'unmodelled MAKELEVEL {level!r} at {where}')
    runtime_directory = any(directory.is_relative_to(p) for p in audit.runtime_directories)
    rest = iter(words[1:])
    for token in rest:
        if token in ('-C', '--directory', '-f', '--file'):
            value = next(rest, None)
            if value is None:
                raise Refusal(f'missing make option operand at {where}')
            audit.shape('make:option.' + ('directory' if token in ('-C', '--directory') else 'file'), where)
            if token in ('-C', '--directory'):
                runtime_directory |= dynamic(value)
                directory = directory / value
            else:
                if file_selected:
                    raise Refusal(f'multiple Makefile selection at {where}')
                filename = value
                file_selected = True
        elif token.startswith(('--file=', '--directory=')) or token.startswith(('-C', '-f')):
            value = token.split('=', 1)[1] if '=' in token else token[2:]
            audit.shape('make:option.' + ('directory' if token.startswith(('-C', '--directory=')) else 'file'), where)
            if token.startswith(('-C', '--directory=')):
                runtime_directory |= dynamic(value)
                directory = directory / value
            else:
                if file_selected:
                    raise Refusal(f'multiple Makefile selection at {where}')
                filename = value
                file_selected = True
        elif token in ('-j', '--jobs'):
            value = next(rest, None)
            if value is None or not (value.isdigit() or dynamic(value)):
                raise Refusal(f'unsupported make jobs at {where}')
            audit.shape('make:option.jobs', where)
        elif re.fullmatch(r'-j(?:[0-9]+|\$\{RUNTIME\})', token):
            audit.shape('make:option.jobs', where)
        elif token in ('-s', '--no-print-directory', '-n', '-B'):
            audit.shape(f'make:option.{token.lstrip("-")}', where)
            letters |= {token[1]} if len(token) == 2 else set()
        elif token.startswith('-'):
            raise Refusal(f'unsupported make option {token!r} at {where}')
        elif re.match(r'^\w+=', token):
            key, value = token.split('=', 1)
            if key in SENSITIVE or key in UNMODELLED:
                raise Refusal(f'uncensused Make override {key!r} at {where}')
            if not dynamic(token) and re.search(r'[$\\\s]', value):
                raise Refusal(f'unmodelled Make command-line value for {key!r} at {where}')
            audit.shape('make:option.variable', where)
            overrides[key] = Runtime(value) if dynamic(token) else value
        else:
            audit.shape('make:option.goal', where)
            targets.append(token)
    if runtime_directory or dynamic(filename) or any(dynamic(t) for t in targets):
        audit.residue.add(f'{where}: runtime Makefile selection')
        return
    directory = directory.resolve()
    if directory in audit.external_builds:
        return  # Already recorded by the checksum-pinned workflow installer.
    if not file_selected and any((directory / name).is_file() for name in ('GNUmakefile', 'makefile')):
        raise Refusal(f'unsupported alternate default Makefile at {where}')
    path = directory / filename
    if not path.is_file():
        raise Refusal(f'unresolved Makefile {filename!r} at {where}')
    if not path.resolve().is_relative_to(audit.root):
        raise Refusal(f'Makefile outside source tree at {where}')
    audit.shape('make:invocation' + ('.inherited-flags' if 'MAKEFLAGS' in audit.exported_env else ''), where)
    audit.makefile(path, targets, overrides, directory, (frozenset(letters), int(level)))


class Makefile:
    """Select explicit or unique pattern rules and expand their known variables."""

    def __init__(self, audit: object, path: Path, overrides: dict[str, str], directory: Path | None = None,
                 flags: tuple = (frozenset(), 0)) -> None:
        letters, level = flags
        self.audit = audit
        self.path = path.resolve()
        self.relative = self.path.relative_to(audit.root).as_posix()
        self.directory = directory.resolve() if directory is not None else self.path.parent
        builtins = builtin_database(audit)
        self.builtin_rules = builtins['rules']
        defaults = builtins['variables']
        # Precedence, lowest first: make's defaults, the environment, the command line.
        self.variables = {name: row['value'] for name, row in defaults.items()}
        self.simple = {name for name, row in defaults.items() if row['flavor'] == 'simple'}
        self.environment = set(audit.exported_env) - MAKE_EXPORTS
        for name, value in audit.exported_env.items():
            if name not in MAKE_EXPORTS and not dynamic(value) and '$' in value:
                raise Refusal(f'unmodelled Make reference in environment value {name!r} for {self.relative}')
        # Environment and command-line values are recursive variables, as in make.
        self.variables.update({name: audit.exported_env[name] for name in self.environment})
        self.simple.difference_update(self.environment)
        # GNU Make 4.3 runs $(shell) in the environment make itself received.
        self.startup = dict(audit.exported_env)
        self.level, self.letters = level, letters
        self.variables.update({'MAKE': 'make', 'CURDIR': str(self.directory), 'MAKELEVEL': str(level)})
        self.simple.update(('MAKE', 'CURDIR', 'MAKELEVEL'))
        self.overrides = overrides
        self.variables.update(overrides)
        self.simple.difference_update(overrides)
        self.call_arguments = 0
        self.stem = None
        self.no_builtin_rules = 'r' in letters
        self.rules = {}
        self.target_variables = {}
        self.phony = set()
        self.mentioned = set()
        self.default = None
        self.first = None
        self.line = 0
        self.visited = set()
        self.audit.inputs[self.relative] = sha256(self.path)

    @property
    def where(self) -> str:
        """Report the source line that owns expansion or selection."""
        return f'{self.relative}:{self.line}'

    def shape(self, name: str) -> None:
        """Every rule applied below is a census shape with a differential fixture."""
        self.audit.shape(f'make:{name}', self.where)

    def variable(self, name: str, seen: frozenset[str]) -> str:
        """Apply recursive versus immediate assignment semantics."""
        if name in seen:
            raise Refusal(f'recursive make variable {name!r} at {self.where}')
        if name in UNMODELLED or name in ('MAKEFLAGS', 'MAKEOVERRIDES') or (
                name.startswith('.') and name not in self.audit.census['make']['special_variables']):
            raise Refusal(f'unmodelled Make variable {name!r} at {self.where}')
        if name == '.SHELLSTATUS':
            self.shape('variable.shell-status')
            return Runtime('${RUNTIME}')  # The status of the last parse-time shell.
        if name == '*' and self.stem is None:
            raise Refusal(f'unmodelled Make explicit-rule stem $* at {self.where}')
        if name in ('@', '<', '^', '*'):
            self.shape(f'automatic.{name}')
        elif name in ('MAKE', 'CURDIR', 'MAKELEVEL', 'MAKECMDGOALS'):
            self.shape(f'variable.{name}')
        elif name.isdigit():
            self.shape('call.argument')
        elif name in self.overrides:
            self.shape('variable.command-line')
        elif name in self.environment:
            self.shape('variable.environment')
        else:
            self.shape('variable.reference')
        value = self.variables.get(name, '')
        return value if name in self.simple else self.expand(value, seen | {name})

    def expand(self, text: str, seen: frozenset[str] = frozenset()) -> str:
        """Expand balanced Make references, preserving escaped shell dollars."""
        output = []
        index = 0
        while index < len(text):
            if text.startswith('$$', index):
                output.append('\x01')
                index += 2
            elif text.startswith('$(', index) or text.startswith('${', index):
                close = ')' if text[index + 1] == '(' else '}'
                opening = text[index + 1]
                end = index + 2
                depth = 1
                while end < len(text) and depth:
                    depth += (text[end] == opening) - (text[end] == close)
                    end += 1
                if depth:
                    raise Refusal(f'unclosed Make expansion at {self.where}')
                expression = text[index + 2:end - 1]
                match = re.match(r'([\w-]+)\s+(.*)', expression, re.S)
                if match:
                    output.append(self.function(match[1], match[2], seen))
                elif re.fullmatch(r'[\w.@<>^*?+%-]+', expression):
                    if re.fullmatch(r'[@<>^*?+%][DF]', expression):
                        raise Refusal(f'unsupported Make automatic variable {expression!r} at {self.where}')
                    if expression in ('?', '+', '%'):
                        raise Refusal(f'unsupported Make automatic variable {expression!r} at {self.where}')
                    output.append(self.variable(expression, seen))
                else:
                    raise Refusal(f'unsupported Make reference {expression!r} at {self.where}')
                index = end
            elif text[index] == '$':
                if index + 1 == len(text):
                    raise Refusal(f'trailing Make dollar at {self.where}')
                name = text[index + 1]
                if name not in '@<^*':
                    raise Refusal(f'unsupported Make automatic variable {name!r} at {self.where}')
                output.append(self.variable(name, seen))
                index += 2
            else:
                output.append(text[index])
                index += 1
        result = ''.join(output)
        return Runtime(result) if any(dynamic(item) for item in output) else result

    @staticmethod
    def arguments(text: str) -> list[str]:
        """Split only top-level commas in nested Make function arguments."""
        result = []
        start = depth = 0
        for index, char in enumerate(text):
            depth += (char in '({') - (char in ')}')
            if char == ',' and depth == 0:
                result.append(text[start:index])
                start = index + 1
        return [*result, text[start:]]

    @staticmethod
    def match(pattern: str, value: str) -> str | None:
        """Return the sole stem for a Make percent pattern."""
        if '%' not in pattern:
            return '' if pattern == value else None
        if pattern.count('%') != 1:
            raise Refusal(f'unsupported Make pattern {pattern!r}')
        before, after = pattern.split('%')
        if value.startswith(before) and value.endswith(after) and len(value) >= len(before) + len(after):
            return value[len(before):len(value) - len(after) if after else None]
        return None

    @classmethod
    def implicit(cls, pattern: str, value: str, prerequisites: list[str]) -> tuple[str, list[str]] | None:
        """Make's implicit match: a slash-free pattern matches the file name, keeping its directory."""
        directory, name = ('', value) if '/' in pattern else (value.rpartition('/')[0], value.rpartition('/')[2])
        stem = cls.match(pattern, name)
        if stem is None:
            return None
        prefix = directory + '/' if directory else ''
        return prefix + stem, [prefix + p.replace('%', stem) if '%' in p else p for p in prerequisites]

    def function(self, name: str, text: str, seen: frozenset[str]) -> str:
        """Implement only the functions present in the reached-source census."""
        if name not in self.audit.census['make']['functions']:
            raise Refusal(f'unsupported Make function {name!r} at {self.where}')
        raw = self.arguments(text)
        self.shape(f'function.{name}')
        if name == 'call':
            # GNU Make 4.3 func_call: $(0) is the name; arguments an outer call bound
            # beyond this call's count are blank; the body is the variable's own value.
            names = self.expand(raw[0], seen).split()
            if len(names) != 1 or names[0] in self.audit.census['make']['functions'] or names[0] not in self.variables:
                raise Refusal(f'undefined or unmodelled Make macro {raw[0]!r} at {self.where}')
            bindings = {'0': names[0], **{str(i): self.expand(v, seen) for i, v in enumerate(raw[1:], 1)}}
            bindings.update({str(i): '' for i in range(len(raw), self.call_arguments)})
            saved, simple, outer = dict(self.variables), set(self.simple), self.call_arguments
            self.variables.update(bindings)
            self.simple.update(bindings)
            self.call_arguments = max(len(raw), outer)
            try:
                return self.variable(names[0], seen)
            finally:
                self.variables, self.simple, self.call_arguments = saved, simple, outer
        if name == 'foreach':
            if len(raw) != 3 or not re.fullmatch(r'\w+', raw[0]):
                raise Refusal(f'unsupported Make foreach at {self.where}')
            saved, simple = dict(self.variables), set(self.simple)
            result = []
            for value in self.expand(raw[1], seen).split():
                self.variables[raw[0]] = value
                self.simple.add(raw[0])
                result.append(self.expand(raw[2], seen))
            self.variables, self.simple = saved, simple
            return ' '.join(result)
        if name == 'if' and len(raw) not in (2, 3):
            raise Refusal(f'unsupported Make if arguments at {self.where}')
        if name in ('if', 'and'):
            return self.lazy(name, raw, seen)
        args = [self.expand(arg, seen) for arg in raw]
        if name == 'shell':
            command = ','.join(args).replace('\x01', '$')
            # Literal command structure is mandatory; runtime data remains data.
            if re.match(r'\s*(?:\$|<dynamic>)', command):
                raise Refusal(f'computed Make shell command at {self.where}')
            self.recipe_shell(command, dict(self.startup))
            return Runtime('${RUNTIME}')
        if name == 'error':
            return ''  # Error paths execute no command; conditions are audited both ways.
        if name == 'strip':
            return ' '.join(','.join(args).split())
        if name == 'firstword':
            return next(iter(','.join(args).split()), '')
        if name == 'abspath':
            return ' '.join(make_abspath(p, str(self.directory)) for p in ','.join(args).split())
        if name == 'wildcard':
            return ' '.join(p for pattern in ','.join(args).split()
                            for p in sorted(glob.glob(pattern, root_dir=self.directory)))
        if any('\\' in arg for arg in args[:2]) and name in ('subst', 'patsubst', 'filter', 'filter-out'):
            raise Refusal(f'unmodelled escaped Make pattern at {self.where}')
        if name == 'subst' and len(args) == 3 and args[0]:
            return args[2].replace(args[0], args[1])
        if name == 'patsubst' and len(args) == 3 and args[1].count('%') <= args[0].count('%') <= 1:
            return ' '.join(args[1].replace('%', stem) if (stem := self.match(args[0], item)) is not None
                            else item for item in args[2].split())
        if name in ('filter', 'filter-out') and len(args) == 2:
            return ' '.join(item for item in args[1].split()
                            if any(self.match(p, item) is not None for p in args[0].split()) == (name == 'filter'))
        if name == 'addprefix' and len(args) == 2:
            return ' '.join(args[0] + item for item in args[1].split())
        raise Refusal(f'unsupported Make function {name!r} at {self.where}')

    def lazy(self, name: str, raw: list[str], seen: frozenset[str]) -> str:
        """`$(if)` and `$(and)` expand arguments in order and stop where make stops.

        A runtime condition selects at run time: every branch is walked and the value is runtime.
        """
        if name == 'if':
            condition = self.expand(raw[0], seen)
            branches = raw[1:]
            if dynamic(condition):
                for branch in branches:
                    self.expand(branch, seen)
                return Runtime('${RUNTIME}')
            selected = branches[0] if condition.strip() else (branches[1] if len(branches) > 1 else '')
            return self.expand(selected, seen)
        value = ''
        for argument in raw:
            value = self.expand(argument, seen)
            if dynamic(value):
                for rest in raw[raw.index(argument) + 1:]:
                    self.expand(rest, seen)
                return Runtime('${RUNTIME}')
            if not value.strip():
                return ''
        return value

    def recipe_environment(self) -> dict[str, str]:
        """A recipe inherits environment and command-line names at their current values, and make's own flags."""
        names = sorted(self.environment | set(self.overrides))
        environment = {name: self.variable(name, frozenset()) for name in names}
        letters = set(self.letters) | ({'r'} if self.no_builtin_rules else set())
        environment['MAKEFLAGS'] = MakeFlags(frozenset(letters), self.overrides)
        environment['MAKELEVEL'] = str(self.level + 1)
        return environment

    def recipe_shell(self, command: str, environment: dict | None = None) -> None:
        """Walk a recipe or parse-time shell under /bin/sh in make's exact child environment."""
        saved = self.audit.env, self.audit.exported_env
        environment = self.recipe_environment() if environment is None else environment
        self.audit.env, self.audit.exported_env = dict(environment), dict(environment)
        try:
            self.audit.shell(command, self.where, self.directory, dialect='sh')
        finally:
            self.audit.env, self.audit.exported_env = saved

    def assignment(self, name: str, operator: str, value: str) -> None:
        """Preserve environment/default/override precedence for supported assignments."""
        if name in SENSITIVE or name in UNMODELLED:
            raise Refusal(f'uncensused Make assignment {name!r} at {self.where}')
        if operator not in self.audit.census['make']['assignment_operators']:
            raise Refusal(f'uncensused Make assignment operator {operator!r} at {self.where}')
        if name == '.DEFAULT_GOAL':
            value = value.strip()
            if operator != ':=' or not re.fullmatch(r'[\w./-]+', value):
                raise Refusal(f'computed .DEFAULT_GOAL at {self.where}')
            self.shape('default-goal')
            self.default = value
        elif name.startswith('.'):
            raise Refusal(f'unsupported Make special variable {name!r} at {self.where}')
        self.shape(f'assignment.{operator}')
        if name in self.overrides or (operator == '?=' and name in self.variables):
            return
        if operator == ':=' or (operator == '+=' and name in self.simple):
            value = self.expand(value)
            self.simple.add(name)
        elif operator != '+=':
            self.simple.discard(name)
        if operator == '+=' and name in self.variables:
            value = self.variables[name] + ' ' + value
        self.variables[name] = value

    def classify(self, line: str) -> tuple[str, str, str] | None:
        """Return (name, operator, value) when make itself reads this line as an assignment."""
        index = top_level(line, ':=')
        if index < 0:
            return None
        if line[index] == ':':
            if line.startswith('::', index):
                raise Refusal(f'uncensused Make double-colon form at {self.where}')
            if not line.startswith(':=', index):
                return None  # A rule: its first colon precedes any assignment.
            operator, start, end = ':=', index, index + 2
        else:
            operator, start = (line[index - 1] + '=', index - 1) if index and line[index - 1] in '+?!' else ('=', index)
            end = index + 1
        name = line[:start].strip(' \t')
        if not (NAME.fullmatch(name) or re.fullmatch(r'\.[A-Z_]+', name)):  # Special names refuse by name.
            raise Refusal(f'non-canonical Make assignment {line.strip()!r} at {self.where}')
        return name, operator, line[end:].lstrip(' \t')

    def rule(self, line: str) -> list[str]:
        """Record one canonical rule; target-specific values must be literal and plain."""
        colon = top_level(line, ':')
        names, rest = line[:colon], line[colon + 1:]
        semicolon = top_level(rest, ';')
        if top_level(rest if semicolon < 0 else rest[:semicolon], ':') >= 0:
            raise Refusal(f'unsupported Make rule at {self.where}')
        equals = top_level(rest, '=')
        if equals >= 0 and (semicolon < 0 or equals < semicolon):
            self.shape('target-specific')
            self.target_specific(names, rest, equals)
            return []
        dependencies, separator, inline = rest.partition(';') if semicolon >= 0 else (rest, '', '')
        names = self.expand(names)
        if dynamic(names) or '$' in names:
            raise Refusal(f'unresolved Make target at {self.where}')
        current = names.split()
        patterns = [name for name in current if '%' in name]
        if patterns and len(current) > 1:
            raise Refusal(f'unsupported multiple-target pattern rule at {self.where}')
        for name in current:
            if name.startswith('.') and name != '.PHONY':
                raise Refusal(f'unsupported Make special or suffix rule {name!r} at {self.where}')
            if any(c in name for c in '&()'):
                raise Refusal(f'unsupported Make grouped or archive target {name!r} at {self.where}')
            if self.first is None and name != '.PHONY' and '%' not in name:
                self.first = name
            resolved = self.expand(dependencies).split()
            if name == '.PHONY':
                self.shape('phony')
                self.phony.update(resolved)
            self.mentioned.update(n for n in [name, *resolved] if '%' not in n and n != '|')
            self.rules.setdefault(name, ([], []))[0].extend(resolved)
            if separator:
                self.shape('inline-recipe')
                self.rules[name][1].append((self.line, inline))
        return current

    def target_specific(self, names: str, rest: str, equals: int) -> None:
        """Only `target: NAME = literal` and `:=` are modelled, for exact targets."""
        before = rest[equals - 1:equals]
        operator = before + '=' if before and before in '+?!:' else '='
        name = rest[:equals - (len(operator) - 1)].strip(' \t')
        value = rest[equals + 1:].strip(' \t')
        if operator not in ('=', ':=') or not NAME.fullmatch(name):
            raise Refusal(f'unsupported Make target-specific form {rest.strip()!r} at {self.where}')
        if name in SENSITIVE or name in UNMODELLED:
            raise Refusal(f'uncensused Make target override {name!r} at {self.where}')
        if '$' in value or top_level(value, ';') >= 0:
            raise Refusal(f'computed target-specific Make variable at {self.where}')
        targets = self.expand(names).split()
        if any('%' in target for target in targets):
            raise Refusal(f'unsupported pattern-specific Make variable at {self.where}')
        for target in targets:
            self.target_variables.setdefault(target, {})[name] = value

    def parse(self) -> None:
        """Classify every logical line by make's own reading; refuse non-canonical spellings."""
        current = []
        definition = None
        condition_depth = 0
        body = []
        text = self.path.read_text()
        for self.line, physical in logical_lines(text, self.relative):
            first = physical[0]
            if definition is not None:
                if first.strip().startswith('define '):
                    raise Refusal(f'unmodelled nested Make definition at {self.where}')
                if len(physical) == 1 and first.strip() == 'endef':
                    self.variables[definition] = '\n'.join(body)
                    self.simple.discard(definition)
                    definition = None
                else:
                    body.extend(physical)  # A definition keeps its text, continuations included.
                continue
            if first.startswith('\t') and current:
                self.shape('recipe-line')
                # Make expands every tab-led line of a rule, comments included.
                recipe = '\n'.join([physical[0][1:], *(p.removeprefix('\t') for p in physical[1:])])
                for target in current:
                    self.rules[target][1].append((self.line, recipe.lstrip(' \t@+-')))
                continue
            joined = condensed(physical)
            line = uncommented(joined, self.where)
            stripped = line.strip()
            if not stripped:
                continue
            if first.startswith('\t'):
                raise Refusal(f'unowned Make recipe at {self.where}')
            if first[0] in ' \t':
                raise Refusal(f'non-canonical indented Make line {stripped!r} at {self.where}')
            if condition_depth and not (stripped in ('else', 'endif') or
                                        stripped.startswith(('$(error ', 'ifeq ', 'ifneq '))):
                raise Refusal(f'unsupported conditional Make body at {self.where}')
            if line == NO_BUILTIN_RULES:
                self.shape('no-builtin-rules')
                self.no_builtin_rules = True
                current = []
                continue
            if stripped.startswith('define '):
                self.shape('define')
                current = []
                definition = stripped[7:].strip()
                if definition in SENSITIVE or definition in UNMODELLED:
                    raise Refusal(f'uncensused Make definition {definition!r} at {self.where}')
                if not re.fullmatch(r'\w+', definition):
                    raise Refusal(f'unsupported Make definition at {self.where}')
                body = []
                continue
            if stripped.startswith(('ifeq ', 'ifneq ')):
                self.shape('conditional')
                condition_depth += 1
                self.expand(stripped)
                continue
            if stripped in ('else', 'endif'):
                if not condition_depth:
                    raise Refusal(f'unmatched Make conditional at {self.where}')
                condition_depth -= stripped == 'endif'
                continue
            if stripped.startswith('$(error '):
                self.expand(stripped)
                continue
            words = stripped.split()
            if words[0] in ('include', '-include', 'sinclude', 'override', 'export', 'unexport', 'undefine',
                            'private', 'vpath', 'load', '-load', 'endef'):
                raise Refusal(f'unsupported Make construct {stripped!r} at {self.where}')
            assignment = self.classify(line)
            if assignment:
                current = []
                self.assignment(*assignment)
                continue
            if top_level(line, ':') >= 0:
                self.shape('rule')
                # A rule's text after its first unquoted ';' is a recipe line: make passes it on, '#' included.
                cut = top_level(joined, '#;')
                if cut >= 0 and joined[cut] == ';' and len(physical) > 1:
                    raise Refusal(f'unmodelled continued inline Make recipe at {self.where}')
                current = self.rule(joined if cut >= 0 and joined[cut] == ';' else line)
                continue
            raise Refusal(f'unsupported Make construct {stripped!r} at {self.where}')
        if condition_depth:
            raise Refusal(f'unclosed Make conditional at {self.where}')
        if definition is not None:
            raise Refusal(f'unclosed Make definition at {self.where}')
        for name, (_, recipes) in self.rules.items():
            if '%' in name and not recipes:
                raise Refusal(f'unsupported recipe-less Make pattern rule {name!r} in {self.relative}')
        # Make remakes its makefile only through terminal rules, never through match-anything ones.
        for row in self.builtin_rules if not self.no_builtin_rules else []:
            matched = self.implicit(row['target'], self.path.name, row['prerequisites']) if row['terminal'] else None
            if matched and all((self.path.parent / p).exists() for p in matched[1]):
                raise Refusal(f'built-in rule {row["target"]!r} may remake {self.relative}')

    def builtin_rule(self, name: str, depth: int = 0) -> str | None:
        """The built-in rule make would apply: existing prerequisites first, then chains."""
        if self.no_builtin_rules or depth > 3:
            return None
        for chained in (False, True):
            for row in self.builtin_rules:
                if not row['recipe'] or (row['target'] == '%' and not row['terminal'] and depth):
                    continue  # Non-terminal match-anything rules never make intermediates.
                matched = self.implicit(row['target'], name, row['prerequisites'])
                if matched is None:
                    continue
                if all((self.directory / p).exists() or p in self.mentioned or (
                        chained and not row['terminal'] and self.builtin_rule(p, depth + 1)) for p in matched[1]):
                    return row['target'] + (':: ' if row['terminal'] else ': ') + ' '.join(row['prerequisites'])
        return None

    def target(self, target: str, prerequisite: bool = False) -> None:
        """Visit a target and bind automatic variables to that exact rule."""
        if dynamic(target):
            self.audit.residue.add(f'{self.where}: runtime Make prerequisite')
            return
        if target in self.visited:
            return
        self.visited.add(target)
        stem = None  # An explicit rule's $* depends on the suffix list: not modelled.
        rule = self.rules.get(target)
        if rule is None or (not rule[1] and target not in self.phony):
            builtin = self.builtin_rule(target)
            if builtin:
                raise Refusal(f'built-in implicit rule {builtin!r} may apply to {target!r} in {self.relative}')
            explicit = rule
            matches = []
            for pattern, (prerequisites, _) in self.rules.items():
                if '%' in pattern and (found := self.implicit(pattern, target, prerequisites)) is not None:
                    matches.append((pattern, found))
            if len(matches) > 1:
                raise Refusal(f'ambiguous Make pattern for {target!r} at {self.where}')
            if matches:
                self.shape('pattern-rule')
                pattern, (stem, implicit) = matches[0]
                # An implicit rule's prerequisites come first in $< and $^, as in make.
                normal, order = split_order(implicit)
                extra, extra_order = split_order(explicit[0] if explicit else [])
                rule = ([*normal, *extra, '|', *order, *extra_order], self.rules[pattern][1])
            elif explicit is not None:
                rule = explicit
            elif prerequisite and (self.directory / target).exists():
                self.shape('prerequisite-file')
                return
            else:
                raise Refusal(f'unresolved Make target {target!r} at {self.where}')
        saved, simple = dict(self.variables), set(self.simple)
        specific = self.target_variables.get(target, {})
        for name in specific:
            if name in self.overrides:
                raise Refusal(f'target-specific {name!r} for {target!r} is overridden by a command-line '
                              f'value in {self.relative}')
        self.variables.update(specific)
        self.simple.update(specific)
        dependencies, recipes = rule
        if '|' in dependencies:
            self.shape('order-only')
        normal = dependencies[:dependencies.index('|')] if '|' in dependencies else dependencies
        dependencies = [d for d in dependencies if d != '|']
        for child in dependencies:
            self.target(child, True)
        self.variables.update({'@': target, '<': next(iter(normal), ''),
                               '^': ' '.join(dict.fromkeys(normal)), '*': stem or ''})
        self.simple.update(('@', '<', '^', '*'))
        saved_stem, self.stem = self.stem, stem
        try:
            for self.line, recipe in recipes:
                # Make runs each unescaped line of an expanded recipe in its own shell.
                lines = recipe_lines(self.expand(recipe).replace('\x01', '$'))
                if len(lines) > 1:
                    self.shape('recipe-lines')
                # Under -n make prints a line instead of running it, unless it names $(MAKE) or starts with +.
                runs = 'n' not in self.letters or re.search(r'\$[({]MAKE[)}]', recipe) or \
                    recipe.lstrip(' \t@-').startswith('+')
                for command in lines:
                    self.shape('recipe' if runs else 'recipe.dry-run')
                    self.audit.inspecting += not runs
                    try:
                        self.recipe_shell(command.lstrip(' \t@+-'))
                    finally:
                        self.audit.inspecting -= not runs
        finally:
            self.stem = saved_stem
        self.variables, self.simple = saved, simple

    def walk(self, targets: list[str] | None) -> None:
        """Audit all suite recipes or the requested target closure."""
        key = (self.relative, str(self.directory), tuple(targets or []), targets is None,
               tuple(sorted((k, v, dynamic(v)) for k, v in self.overrides.items())), self.audit.incoming_state())
        if key in self.audit.seen:
            return
        self.audit.seen.add(key)
        self.variables['MAKECMDGOALS'] = ' '.join(targets or [])
        self.simple.add('MAKECMDGOALS')
        self.parse()
        selected = [t for t in self.rules if t != '.PHONY' and '%' not in t] if targets is None else targets
        if targets is not None:
            self.shape('goal.' + ('command-line' if targets else 'default' if self.default else 'first'))
        for target in selected or [self.default or self.first or '']:
            self.target(target)
