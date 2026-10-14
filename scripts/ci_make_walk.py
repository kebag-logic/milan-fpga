#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Resolve the censused Make subset without running make or shell commands."""

from pathlib import Path
import glob
import re

from ci_command_table import Refusal, Runtime, sha256
from ci_syntax import SENSITIVE


def dynamic(value: str) -> bool:
    """Only unresolved source values are runtime residue, never host locations."""
    return isinstance(value, Runtime)


def invocation(audit: object, words: list[str], where: str, directory: Path) -> None:
    """Parse complete option operands before selecting a file and targets."""
    filename = 'Makefile'
    file_selected = False
    targets = []
    overrides = dict(audit.make_overrides)
    runtime_directory = any(directory.is_relative_to(p) for p in audit.runtime_directories)
    rest = iter(words[1:])
    for token in rest:
        if token in ('-C', '--directory', '-f', '--file'):
            value = next(rest, None)
            if value is None:
                raise Refusal(f'missing make option operand at {where}')
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
        elif re.fullmatch(r'-j(?:[0-9]+|\$\{RUNTIME\})', token):
            pass
        elif token in ('-s', '--no-print-directory', '-n', '-B'):
            pass
        elif token.startswith('-'):
            raise Refusal(f'unsupported make option {token!r} at {where}')
        elif re.match(r'^\w+=', token):
            key, value = token.split('=', 1)
            if key in SENSITIVE:
                raise Refusal(f'uncensused Make override {key!r} at {where}')
            overrides[key] = Runtime(value) if dynamic(token) else value
        else:
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
    audit.makefile(path, targets, overrides, directory)


class Makefile:
    """Select explicit or unique pattern rules and expand their known variables."""

    def __init__(self, audit: object, path: Path, overrides: dict[str, str], directory: Path | None = None) -> None:
        self.audit = audit
        self.path = path.resolve()
        self.relative = self.path.relative_to(audit.root).as_posix()
        self.directory = directory.resolve() if directory is not None else self.path.parent
        self.variables = {**audit.exported_env, 'MAKE': 'make', 'CURDIR': str(self.directory)}
        self.simple = set(self.variables)
        self.overrides = overrides
        self.variables.update(overrides)
        self.simple.update(overrides)
        self.rules = {}
        self.target_variables = {}
        self.phony = set()
        self.default = None
        self.first = None
        self.line = 0
        self.visited = set()
        self.audit.inputs[self.relative] = sha256(self.path)

    @property
    def where(self) -> str:
        """Report the source line that owns expansion or selection."""
        return f'{self.relative}:{self.line}'

    def variable(self, name: str, seen: frozenset[str]) -> str:
        """Apply recursive versus immediate assignment semantics."""
        if name in seen:
            raise Refusal(f'recursive make variable {name!r} at {self.where}')
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

    def function(self, name: str, text: str, seen: frozenset[str]) -> str:
        """Implement only the functions present in the reached-source census."""
        if name not in self.audit.census['make']['functions']:
            raise Refusal(f'unsupported Make function {name!r} at {self.where}')
        raw = self.arguments(text)
        if name in ('call', 'foreach'):
            if name == 'call':
                macro = self.expand(raw[0], seen)
                if macro not in self.variables:
                    raise Refusal(f'undefined Make macro {macro!r} at {self.where}')
                bindings = {str(i): self.expand(v, seen) for i, v in enumerate(raw[1:], 1)}
                body = self.variables[macro]
                values = [bindings]
            else:
                if len(raw) != 3 or not re.fullmatch(r'\w+', raw[0]):
                    raise Refusal(f'unsupported Make foreach at {self.where}')
                values = [{raw[0]: v} for v in self.expand(raw[1], seen).split()]
                body = raw[2]
            saved, simple = dict(self.variables), set(self.simple)
            result = []
            for bindings in values:
                self.variables.update(bindings)
                self.simple.update(bindings)
                result.append(self.expand(body, seen))
            self.variables, self.simple = saved, simple
            return ' '.join(result)
        if name == 'if' and len(raw) not in (2, 3):
            raise Refusal(f'unsupported Make if arguments at {self.where}')
        args = [self.expand(arg, seen) for arg in raw]
        if name == 'shell':
            command = ','.join(args).replace('\x01', '$')
            # Literal command structure is mandatory; runtime data remains data.
            if re.match(r'\s*(?:\$|<dynamic>)', command):
                raise Refusal(f'computed Make shell command at {self.where}')
            self.audit.shell(command, self.where, self.directory)
            return Runtime('${RUNTIME}')
        if name == 'error':
            return ''  # Error paths execute no command; conditions are audited both ways.
        if name == 'strip':
            return ' '.join(','.join(args).split())
        if name == 'firstword':
            return next(iter(','.join(args).split()), '')
        if name == 'abspath':
            return ' '.join(str((self.directory / p).resolve()) for p in ','.join(args).split())
        if name == 'wildcard':
            return ' '.join(p if Path(pattern).is_absolute() else str(Path(p).relative_to(self.directory, walk_up=True))
                            for pattern in ','.join(args).split()
                            for p in sorted(glob.glob(str(self.directory / pattern))))
        if name in ('if', 'and'):
            if any(dynamic(a) for a in args):
                return Runtime('${RUNTIME}')
            if name == 'if':
                return args[1] if args[0].strip() else (args[2] if len(args) > 2 else '')
            return args[-1] if all(a.strip() for a in args) else ''
        if name == 'subst' and len(args) == 3:
            return args[2].replace(args[0], args[1])
        if name == 'patsubst' and len(args) == 3:
            return ' '.join(args[1].replace('%', stem) if (stem := self.match(args[0], item)) is not None
                            else item for item in args[2].split())
        if name in ('filter', 'filter-out') and len(args) == 2:
            return ' '.join(item for item in args[1].split()
                            if any(self.match(p, item) is not None for p in args[0].split()) == (name == 'filter'))
        if name == 'addprefix' and len(args) == 2:
            return ' '.join(args[0] + item for item in args[1].split())
        raise Refusal(f'unsupported Make function {name!r} at {self.where}')

    def assignment(self, assignment: re.Match) -> None:
        """Preserve environment/default/override precedence for supported assignments."""
        name, operator, value = assignment.groups()
        if name in SENSITIVE:
            raise Refusal(f'uncensused Make assignment {name!r} at {self.where}')
        value = re.split(r'(?<!\\)#', value, 1)[0].rstrip()
        if name == '.DEFAULT_GOAL':
            if operator != ':=' or not re.fullmatch(r'[\w./-]+', value):
                raise Refusal(f'computed .DEFAULT_GOAL at {self.where}')
            self.default = value
        elif name.startswith('.'):
            raise Refusal(f'unsupported Make special variable {name!r} at {self.where}')
        if name in self.overrides or (operator == '?=' and name in self.variables):
            return
        if operator == ':=' or (operator == '+=' and name in self.simple):
            value = self.expand(value)
            self.simple.add(name)
        elif operator != '+=':
            self.simple.discard(name)
        self.variables[name] = self.variables.get(name, '') + ' ' + value if operator == '+=' else value

    def parse(self) -> None:
        """Read declarations before selecting targets; refuse unsupported directives."""
        current = []
        definition = None
        condition_depth = 0
        body = []
        for self.line, line in enumerate(self.path.read_text().replace('\\\n', ' ').splitlines(), 1):
            stripped = line.strip()
            if definition is not None:
                if stripped == 'endef':
                    self.variables[definition] = '\n'.join(body)
                    definition = None
                else:
                    body.append(line)
                continue
            if not stripped or stripped.startswith('#'):
                continue
            if condition_depth and not stripped.startswith(('$(error ', 'ifeq ', 'ifneq ', 'endif', 'else')):
                raise Refusal(f'unsupported conditional Make body at {self.where}')
            if line.startswith('\t'):
                if not current:
                    raise Refusal(f'unowned Make recipe at {self.where}')
                for target in current:
                    self.rules[target][1].append((self.line, line.lstrip('\t@+-')))
                continue
            current = []
            assignment = re.fullmatch(r'([\w.]+)\s*(:=|\?=|\+=|=)\s*(.*)', line)
            if assignment:
                self.assignment(assignment)
                continue
            if stripped.startswith('define '):
                definition = stripped[7:].strip()
                if definition in SENSITIVE:
                    raise Refusal(f'uncensused Make definition {definition!r} at {self.where}')
                if not re.fullmatch(r'\w+', definition):
                    raise Refusal(f'unsupported Make definition at {self.where}')
                body = []
                continue
            if stripped.startswith(('ifeq ', 'ifneq ')):
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
            if stripped.startswith(('include ', '-include ', 'sinclude ', 'override ', 'export ', 'undefine ')):
                raise Refusal(f'unsupported Make construct {stripped!r} at {self.where}')
            if ':' in line:
                names, dependencies = line.split(':', 1)
                if ':' in dependencies:
                    raise Refusal(f'unsupported Make rule at {self.where}')
                specific = re.fullmatch(r'\s*(\w+)\s*=\s*(.*)', dependencies)
                if specific:
                    if specific[1] in SENSITIVE:
                        raise Refusal(f'uncensused Make target override {specific[1]!r} at {self.where}')
                    if '$' in specific[2]:
                        raise Refusal(f'computed target-specific Make variable at {self.where}')
                    for name in self.expand(names).split():
                        self.target_variables.setdefault(name, {})[specific[1]] = specific[2]
                    continue
                dependencies, separator, inline = dependencies.partition(';')
                names = self.expand(names)
                if dynamic(names) or '$' in names:
                    raise Refusal(f'unresolved Make target at {self.where}')
                current = names.split()
                for name in current:
                    if name.startswith('.') and name != '.PHONY':
                        raise Refusal(f'unsupported Make special or suffix rule {name!r} at {self.where}')
                    if self.first is None and name != '.PHONY' and '%' not in name:
                        self.first = name
                    resolved = self.expand(dependencies).split()
                    if name == '.PHONY':
                        self.phony.update(resolved)
                    self.rules.setdefault(name, ([], []))[0].extend(resolved)
                    if separator:
                        self.rules[name][1].append((self.line, inline))
                continue
            raise Refusal(f'unsupported Make construct {stripped!r} at {self.where}')
        if condition_depth:
            raise Refusal(f'unclosed Make conditional at {self.where}')
        if definition is not None:
            raise Refusal(f'unclosed Make definition at {self.where}')

    def target(self, target: str, prerequisite: bool = False) -> None:
        """Visit a target and bind automatic variables to that exact rule."""
        if dynamic(target):
            self.audit.residue.add(f'{self.where}: runtime Make prerequisite')
            return
        if target in self.visited:
            return
        self.visited.add(target)
        stem = ''
        rule = self.rules.get(target)
        if rule is None or (not rule[1] and target not in self.phony):
            explicit = rule
            matches = [(pattern, self.match(pattern, target)) for pattern in self.rules if '%' in pattern]
            matches = [(p, s) for p, s in matches if s is not None]
            if len(matches) > 1:
                raise Refusal(f'ambiguous Make pattern for {target!r} at {self.where}')
            if matches:
                pattern, stem = matches[0]
                implicit = self.rules[pattern]
                rule = ([*(explicit[0] if explicit else []), *implicit[0]], implicit[1])
            elif explicit is not None:
                rule = explicit
            elif prerequisite and (self.directory / target).exists():
                return
            else:
                raise Refusal(f'unresolved Make target {target!r} at {self.where}')
        saved, simple = dict(self.variables), set(self.simple)
        self.variables.update(self.target_variables.get(target, {}))
        self.simple.update(self.target_variables.get(target, {}))
        dependencies, recipes = rule
        normal = dependencies[:dependencies.index('|')] if '|' in dependencies else dependencies
        normal = [d.replace('%', stem) for d in normal]
        dependencies = [d.replace('%', stem) for d in dependencies if d != '|']
        for child in dependencies:
            self.target(child, True)
        self.variables.update({'@': target, '<': next(iter(normal), ''),
                               '^': ' '.join(dict.fromkeys(normal)), '*': stem})
        self.simple.update(('@', '<', '^', '*'))
        for self.line, recipe in recipes:
            command = self.expand(recipe).replace('\x01', '$')
            self.audit.shell(command, self.where, self.directory)
        self.variables, self.simple = saved, simple

    def walk(self, targets: list[str] | None) -> None:
        """Audit all suite recipes or the requested target closure."""
        key = (self.relative, str(self.directory), tuple(targets or []),
               tuple(sorted(self.overrides.items())), targets is None)
        if key in self.audit.seen:
            return
        self.audit.seen.add(key)
        previous = self.audit.make_overrides
        self.audit.make_overrides = self.overrides
        self.parse()
        selected = [t for t in self.rules if t != '.PHONY' and '%' not in t] if targets is None else targets
        for target in selected or [self.default or self.first or '']:
            self.target(target)
        self.audit.make_overrides = previous
