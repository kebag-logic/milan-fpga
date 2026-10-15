#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Walk the censused shell syntax without executing candidate commands.

The walker keeps the state the shell keeps: variables, exported names, functions,
local scopes and the working directory. Where a construct leaves that state
undecided, every reachable alternative is joined: a value that differs between
paths is a runtime value, never a literal, and a directory that differs refuses.
`exit`, `return`, `break` and `continue` end their path, and its state joins
where the shell resumes. Words expand as the shell expands them, including field
splitting and pathname expansion. Each modelled rule is a census shape.
"""

from dataclasses import dataclass, field
from pathlib import Path
import re

from ci_command_table import Fields, Refusal, Runtime, _normpath, nodes, shell_tree, sha256
from ci_syntax import SENSITIVE, exact_use, shell_nodes


RUNTIME = Runtime('${RUNTIME}')
PLAIN = {'Cmd', 'Pos', 'End', 'Position', 'Semicolon'}
#: Names whose exact command-substitution shapes the walker evaluates.
SUBSTITUTIONS = ('cd', 'pwd', 'dirname', 'realpath')
#: Builtins handled by the walker itself rather than the command table.
WALKER_BUILTINS = {'cd', 'source', '.', 'trap', 'read', 'unset', 'shift', 'exit', 'return', 'break', 'continue'}
#: Parser node fields that carry no value of their own.
PARAMETER_PLAIN = {'Type', 'Pos', 'End', 'Short', 'Dollar', 'Rbrace', 'Param'}
#: Arithmetic operators that assign: `=`, `++` and `--`.
ARITHMETIC_ASSIGNMENTS = (74, 36, 37)
IFS = ' \t\n'
MISSING = object()


def posix_dirname(value: str) -> str:
    """The image's coreutils dirname of one operand; its self-test holds the reference outputs."""
    stripped = value.rstrip('/')
    if not value or '/' not in stripped:
        return '/' if value and not stripped else '.'
    return stripped.rpartition('/')[0].rstrip('/') or '/'


def glob_pattern(text: str) -> bool:
    """Whether unquoted text is a pathname pattern: `*`, `?` or a closed bracket expression."""
    return bool(re.search(r'[*?]|\[[^]]*\]', text))


def function_names(tree: object) -> set[str]:
    """Every function a parsed program can define, wherever the definition stands."""
    return {node['Name']['Value'] for node in nodes(tree) if node.get('Type') == 'FuncDecl'}


def assigned_names(tree: object) -> set[str]:
    """Every variable a construct can assign, including loop, read and arithmetic targets."""
    names = set()
    for node in nodes(tree):
        kind = node.get('Type')
        if kind in ('CallExpr', 'DeclClause'):
            for item in node.get('Assigns', []) + (node.get('Args', []) if kind == 'DeclClause' else []):
                if item.get('Name'):
                    names.add(item['Name']['Value'])
        if kind == 'CallExpr':
            words = [part.get('Value') for arg in node.get('Args', []) for part in arg.get('Parts', [])[:1]]
            if words[:1] == ['read']:
                names.update(word for word in words[1:] if word and re.fullmatch(r'[A-Za-z_]\w*', word))
        if kind == 'WordIter' and node.get('Name'):
            names.add(node['Name']['Value'])
        if kind in ('BinaryArithm', 'UnaryArithm') and node.get('Op') in ARITHMETIC_ASSIGNMENTS:
            for part in nodes(node.get('X', {})):
                if part.get('Type') == 'Lit' and re.fullmatch(r'[A-Za-z_]\w*', part.get('Value', '')):
                    names.add(part['Value'])
                    break
    return names


@dataclass
class Frame:
    """Collect the states with which paths leave one construct."""

    kind: str  # 'function', 'source', 'loop', 'subshell' or 'process'
    states: list = field(default_factory=list)
    resumes: list = field(default_factory=list)


class Shell:
    """Keep variables, directories and function names in their actual scope."""

    def __init__(self, audit: object, where: str, argv0: str | None = None, dialect: str = 'bash') -> None:
        self.audit = audit
        self.where = where
        self.dialect = dialect
        self.invocation_source = where.split(':')[0]
        # $0 and BASH_SOURCE are the exact words that named each executed or sourced file.
        self.argv0 = argv0
        self.words = {self.invocation_source: argv0} if argv0 is not None else {}
        self.functions = {}
        self.names = set()
        self.commands = set()
        self.active = set()
        # A new shell process starts from its exported environment alone.
        self.env = dict(audit.exported_env)
        self.exported = set(audit.exported_env)
        self.locals = []
        self.frames = []

    def location(self, node: dict) -> str:
        """Give every refusal and residue a source location."""
        return f"{self.where}:{node.get('Pos', {}).get('Line', 1)}"

    def shape(self, name: str, node: dict | None = None) -> None:
        """Every rule applied below is a census shape with a differential fixture."""
        self.audit.shape(f'{self.dialect}:{name}', self.location(node) if node else self.where)

    # State

    def capture(self) -> tuple:
        """Copy the state one path carries."""
        return (dict(self.env), set(self.exported), {k: list(v) for k, v in self.functions.items()},
                [dict(scope) for scope in self.locals])

    def restore(self, state: tuple) -> None:
        """Continue from a captured state."""
        env, exported, functions, scopes = state
        self.env, self.exported = dict(env), set(exported)
        self.functions = {k: list(v) for k, v in functions.items()}
        self.locals = [dict(scope) for scope in scopes]

    def join(self, paths: list[tuple], construct: str, where: str) -> Path | None:
        """Continue from every reachable path: differing values are runtime, differing directories refuse."""
        live = [(state, directory) for state, directory in paths if directory is not None]
        if not live:
            if paths:
                self.restore(paths[0][0])
            return None
        if len({directory for _, directory in live}) > 1:
            raise Refusal(f'ambiguous shell directory after {construct} at {where}')
        states = [state for state, _ in live]
        env = {}
        for key in set().union(*(state[0] for state in states)):
            values = [state[0].get(key, MISSING) for state in states]
            same = all(v is not MISSING and v == values[0] and type(v) is type(values[0]) for v in values)
            env[key] = values[0] if same else RUNTIME
        exported = set().union(*(state[1] for state in states))
        for name in exported - set.intersection(*(state[1] for state in states)):
            env[name] = RUNTIME  # Exported on some paths only: a child may or may not see it.
        functions = {}
        for name in set().union(*(state[2] for state in states)):
            alternatives = []
            for state in states:
                for alternative in state[2].get(name, [None]):
                    if alternative not in alternatives:
                        alternatives.append(alternative)
            functions[name] = alternatives
        scopes = []
        for index in range(len(states[0][3])):
            frames = [state[3][index] for state in states]
            merged = {}
            for key in set().union(*frames):
                values = [frame.get(key, MISSING) for frame in frames]
                same = all(v is not MISSING and v == values[0] and type(v) is type(values[0]) for v in values)
                merged[key] = values[0] if same else RUNTIME  # Local on some paths only.
            scopes.append(merged)
        self.restore((env, exported, functions, scopes))
        return live[0][1]

    def escape(self, kind: str, directory: Path, where: str) -> None:
        """Record the state with which a path leaves its construct; the path then ends."""
        targets = {'return': ('function', 'source'), 'break': ('loop',), 'continue': ('loop',)}
        for frame in reversed(self.frames):
            if frame.kind == 'subshell' or (frame.kind == 'process' and kind == 'exit'):
                return  # The path ends with its subshell or process.
            if kind == 'exit':
                continue
            if frame.kind in targets[kind]:
                (frame.resumes if kind == 'continue' else frame.states).append((self.capture(), directory))
                return
            if frame.kind != 'loop':
                break
        if kind != 'exit':
            raise Refusal(f'uncensused shell {kind} outside its construct at {where}')

    def framed(self, kind: str, walk: object) -> tuple[Frame, Path | None]:
        """Walk one construct, collecting the paths that leave it early."""
        frame = Frame(kind)
        self.frames.append(frame)
        try:
            result = walk()
        finally:
            self.frames.pop()
        return frame, result

    def isolated(self, walk: object) -> None:
        """A subshell: its state and early exits never reach the parent."""
        saved = self.capture()
        try:
            self.framed('subshell', walk)
        finally:
            self.restore(saved)

    # Words

    def value(self, node: dict, directory: Path, quoted: bool = False) -> str:
        """Expand one word without field splitting or pathname expansion."""
        kind = node.get('Type')
        if kind == 'Lit':
            self.shape('word.literal' if not quoted else 'word.double-quoted', node)
            pattern = r'\\([$`"\\\n])' if quoted else r'\\(.)'
            return re.sub(pattern, r'\1', node.get('Value', '')).replace('\\\n', '')
        if kind == 'SglQuoted':
            self.shape('word.single-quoted', node)
            return node.get('Value', '')
        if kind == 'ParamExp':
            return self.parameter(node, directory)
        if kind in ('CmdSubst', 'ProcSubst'):
            end = None
            def walk() -> None:
                """The substitution's statements, in a subshell."""
                nonlocal end
                end = self.statements(node.get('Stmts', []), directory)
            self.isolated(walk)
            if kind == 'ProcSubst':
                self.shape('word.process-substitution', node)
                return RUNTIME
            return self.exact_substitution(node, directory, end)
        if kind == 'ArithmExp':
            self.shape('word.arithmetic', node)
            self.arithmetic(node, directory)
            return Runtime('${RUNTIME}')
        if kind in ('DblQuoted', 'Word') or (kind is None and 'Parts' in node):
            if kind == 'DblQuoted':
                self.shape('word.double-quoted', node)
            parts = [self.value(part, directory, quoted or kind == 'DblQuoted') for part in node.get('Parts', [])]
            value = ''.join(parts)
            return Runtime(value) if any(isinstance(part, Runtime) for part in parts) else value
        raise Refusal(f'unsupported shell word {kind!r} at {self.location(node)}')

    def parameter(self, node: dict, directory: Path) -> str:
        """A parameter: plain names resolve; operators and specials are runtime values."""
        name = node['Param']['Value']
        if name in ('0', 'BASH_SOURCE'):
            index = node.get('Index')
            parts = index.get('Parts', []) if index else []
            zero = index is None or (name == 'BASH_SOURCE' and len(parts) == 1 and
                                     parts[0].get('Type') == 'Lit' and parts[0].get('Value') == '0')
            plain = not set(node) - PARAMETER_PLAIN - {'Index'}
            word = self.argv0 if name == '0' else self.words.get(self.where.split(':')[0])
            self.shape('word.argv0' if name == '0' else 'word.bash-source', node)
            return word if word is not None and plain and zero else RUNTIME
        for child in nodes(node):
            if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst', 'ArithmExp'):
                self.value(child, directory)
        if set(node) - PARAMETER_PLAIN:
            # Parameter operators are data; their nested substitutions were walked.
            self.shape('word.parameter-operator', node)
            return Runtime('${RUNTIME}')
        if not re.fullmatch(r'[A-Za-z_]\w*', name):
            self.shape('word.special-parameter', node)
            return self.env.get(name, Runtime('${' + name + '}')) if name.isdigit() else Runtime('${' + name + '}')
        self.shape('word.parameter', node)
        return self.env.get(name, Runtime('${' + name + '}'))

    def arithmetic(self, node: dict, directory: Path) -> None:
        """Arithmetic data is runtime; its assignments make their targets runtime."""
        for child in nodes(node):
            if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst'):
                self.value(child, directory)
        for name in assigned_names(node):
            self.env[name] = RUNTIME

    def fields(self, word: dict, directory: Path) -> list[str]:
        """A command or loop word after expansion, field splitting and pathname expansion.

        Each segment carries its text and a pattern view in which quoted characters
        cannot act as pattern characters. Unquoted expansion results split at blanks.
        """
        segments = []  # (text, view, unquoted expansion)
        parts = word.get('Parts', [])
        brace = ''.join(part.get('Value', '') if part.get('Type') == 'Lit' else '\x00' for part in parts)
        if re.search(r'\{[^{}]*(,|\.\.)[^{}]*\}', brace):
            raise Refusal(f'uncensused shell brace expansion at {self.location(word)}')
        for index, part in enumerate(parts):
            kind = part.get('Type')
            if kind == 'Lit':
                raw = part.get('Value', '')
                text = self.value(part, directory)
                if index == 0 and raw.startswith('~'):
                    self.shape('word.tilde', part)
                    segments.append((Fields(text), '', True))
                    continue
                view = re.sub(r'\\(.)', lambda match: 'x' * len(match[1]), raw).replace('\\\n', '')
                segments.append((text, view, False))
            elif kind in ('ParamExp', 'CmdSubst', 'ArithmExp'):
                text = self.value(part, directory)
                segments.append((text, text, True))
            else:
                text = self.value(part, directory)
                # "$@" and "${name[@]}" expand to any number of fields, even quoted.
                every = kind == 'DblQuoted' and any(
                    child.get('Type') == 'ParamExp' and (child['Param']['Value'] == '@' or any(
                        index.get('Type') == 'Lit' and index.get('Value') in ('@', '*')
                        for index in (child.get('Index') or {}).get('Parts', [child.get('Index') or {}])))
                    for child in nodes(part))
                segments.append((Fields(text) if every else text, 'x' * len(text), every))
        if any(isinstance(text, Runtime) and unquoted for text, _, unquoted in segments):
            self.shape('word.split-runtime', word)
            return [Fields(''.join(text for text, _, _ in segments))]
        result, current, view, started = [], '', '', False
        for text, mask, unquoted in segments:
            if not unquoted:
                current, view, started = current + text, view + mask, True
                continue
            if any(c in IFS for c in text):
                self.shape('word.split', word)
            for number, piece in enumerate(re.split(r'[ \t\n]+', text)):
                if number:
                    if started:
                        result.append((current, view))
                    current, view, started = '', '', False
                if piece:
                    current, view, started = current + piece, view + piece, True
        if started:
            result.append((current, view))
        runtime = any(isinstance(text, Runtime) for text, _, _ in segments)
        expanded = []
        for text, mask in result:
            if glob_pattern(mask):
                self.shape('word.pathname-expansion', word)
                expanded.append(Fields(text))
            else:
                expanded.append(Runtime(text) if runtime else text)
        return expanded

    def assignment_value(self, word: dict, directory: Path) -> str:
        """An assignment value: no splitting or pathname expansion; tilde prefixes expand."""
        value = self.value(word, directory)
        parts = word.get('Parts', [])
        if any(part.get('Type') == 'Lit' and (index == 0 and part.get('Value', '').startswith('~') or
                                             ':~' in part.get('Value', '')) for index, part in enumerate(parts)):
            self.shape('word.tilde', word)
            return RUNTIME
        return value

    def plain_call(self, statement: dict, words: int, directory: Path) -> list[str] | None:
        """Fields of one unredirected, unassigned simple command of an exact arity."""
        call = statement.get('Cmd', {})
        if set(statement) - PLAIN or call.get('Type') != 'CallExpr' or call.get('Assigns'):
            return None
        values = [value for word in call.get('Args', []) for value in self.fields(word, directory)]
        if len(values) != words or any(isinstance(value, Runtime) for value in values):
            return None
        return values

    def exact_substitution(self, node: dict, directory: Path, end: Path | None) -> str:
        """Exact shapes only; any other substitution output is a runtime value.

        `$(cd <literal> && pwd)` is the one shape that yields a directory. `$(dirname
        <literal>)` and `$(realpath <literal>)` are exact functions of their operand.
        None applies when a function of the same name is defined anywhere in scope.
        """
        statements = node.get('Stmts', [])
        if len(statements) != 1 or set(statements[0]) - PLAIN or self.names & set(SUBSTITUTIONS):
            self.shape('word.command-substitution', node)
            return RUNTIME
        command = statements[0]['Cmd']
        if command.get('Type') == 'CallExpr':
            words = self.plain_call(statements[0], 2, directory)
            if not words or words[1].startswith('-') or words[0] not in ('dirname', 'realpath'):
                self.shape('word.command-substitution', node)
                return RUNTIME
            target = directory / words[1]
            if words[0] == 'dirname':
                self.shape('word.dirname', node)
                return posix_dirname(words[1])
            if target.exists():
                self.shape('word.realpath', node)
                return str(target.resolve())
            self.shape('word.command-substitution', node)
            return RUNTIME
        change = self.plain_call(command['X'], 2, directory) if command.get('Type') == 'BinaryCmd' and \
            command.get('Op') == 10 else None
        report = self.plain_call(command['Y'], 1, directory) if change else None
        if not change or report != ['pwd'] or change[0] != 'cd' or change[1].startswith('-'):
            self.shape('word.command-substitution', node)
            return RUNTIME
        logical = Path(_normpath(str(directory / change[1])))
        if not logical.is_dir() or logical != logical.resolve() or end != logical:
            self.shape('word.command-substitution', node)
            return RUNTIME  # A missing or symlinked directory is not modelled.
        self.shape('word.cd-pwd', node)
        return str(logical)

    # Statements

    def assignments(self, values: list[dict], directory: Path) -> None:
        """Resolve scalar assignments without inventing array contents."""
        for assignment in values:
            name = assignment.get('Name', {}).get('Value')
            if not name:
                continue
            if assignment.get('Value'):
                value = self.assignment_value(assignment['Value'], directory)
                if assignment.get('Index'):
                    self.shape('assignment.index', assignment)
                    self.value(assignment['Index'], directory) if assignment['Index'].get('Parts') else None
                    value = Runtime('${RUNTIME}')
                elif assignment.get('Append'):
                    self.shape('assignment.append', assignment)
                    previous = self.env.get(name, Runtime('${' + name + '}'))
                    joined = previous + value
                    value = Runtime(joined) if isinstance(previous, Runtime) or isinstance(value, Runtime) else joined
                else:
                    self.shape('assignment', assignment)
                self.env[name] = value
                if name == 'LD_PRELOAD':
                    self.audit.residue.add(f'{self.location(assignment)}: declared runtime loader selection')
            elif assignment.get('Array'):
                self.shape('assignment.array', assignment)
                for item in assignment['Array'].get('Elems', []):
                    if item.get('Value'):
                        self.value(item['Value'], directory)
                self.env[name] = Runtime('${RUNTIME}')
            elif not assignment.get('Naked'):
                self.shape('assignment', assignment)
                self.env[name] = ''  # `NAME=` assigns the empty string.

    def statements(self, statements: list[dict], directory: Path | None) -> Path | None:
        """Sequence statements; statements after an ended path are inspected, never continued."""
        last = directory
        for statement in statements:
            if directory is None:
                # Unreachable: inspected for its commands, never claimed to run.
                saved = self.capture()
                self.audit.inspecting += 1
                try:
                    self.framed('subshell', lambda: self.statement(statement, last))
                finally:
                    self.audit.inspecting -= 1
                    self.restore(saved)
                continue
            last = directory
            directory = self.statement(statement, directory)
        return directory

    def certain(self, statement: dict, directory: Path) -> bool:
        """Whether a statement always succeeds.

        That is a plain assignment, `true` or `:`, or `cd` into an existing directory.
        """
        node = statement.get('Cmd', {})
        if set(statement) - PLAIN or node.get('Type') != 'CallExpr':
            return False
        if any(child.get('Type') in ('CmdSubst', 'ProcSubst', 'ArithmExp') for child in nodes(node)):
            return False
        args = node.get('Args', [])
        if not args:
            return True
        if any(part.get('Type') not in ('Lit', 'SglQuoted') for word in args for part in word.get('Parts', [])):
            return False
        words = [self.value(word, directory) for word in args]
        if words[0] in self.names or node.get('Assigns'):
            return False
        if words in (['true'], [':']):
            return True
        target = Path(_normpath(str(directory / words[1]))) if words[0] == 'cd' and len(words) == 2 and \
            not words[1].startswith('-') else None
        return target is not None and target.is_dir() and target == target.resolve()

    def statement(self, statement: dict, directory: Path) -> Path | None:
        """Classify each supported compound form, refusing unknown nodes."""
        node = statement.get('Cmd', statement)
        kind = node.get('Type')
        where = self.location(node)
        inline = None
        if statement.get('Background'):
            raise Refusal(f'uncensused shell background operator at {where}')
        if statement.get('Negated'):
            self.shape('negation', node)
        for redirect in statement.get('Redirs', []):
            self.shape('redirect', redirect)
            if any(n.get('Type') == 'ParamExp' and n['Param']['Value'] in ('GITHUB_PATH', 'GITHUB_ENV')
                   for n in nodes(redirect)):
                exact_use(self.audit, statement, self.where, 'environment-file')
            if redirect.get('Word'):
                self.value(redirect['Word'], directory)
            if redirect.get('Hdoc'):
                self.shape('heredoc', redirect)
                self.value(redirect['Hdoc'], directory)
            if redirect.get('Hdoc') and node.get('Type') == 'CallExpr':
                args = node.get('Args', [])
                name = self.value(args[0], directory) if args else ''
                if name in ('python', 'python3'):
                    self.shape('heredoc.python', redirect)
                    inline = self.value(redirect['Hdoc'], directory)
                    self.audit.python_command([name, '-c', inline], where, directory, {})
                elif name in ('bash', 'sh'):
                    raise Refusal(f'unclassified interpreter input at {where}')
        if kind == 'CallExpr':
            return self.call(node, directory, where, inline)
        if kind == 'DeclClause':
            return self.declaration(node, directory, where)
        if kind == 'FuncDecl':
            self.shape('function.definition', node)
            self.functions[node['Name']['Value']] = [(node['Body'], self.where)]
            return directory
        if kind == 'Block':
            self.shape('block', node)
            return self.statements(node.get('Stmts', []), directory)
        if kind == 'Subshell':
            self.shape('subshell', node)
            self.isolated(lambda: self.statements(node.get('Stmts', []), directory))
            return directory
        if kind == 'BinaryCmd':
            return self.binary(node, directory, where)
        if kind == 'IfClause' or (kind is None and 'Then' in node):
            return self.conditional(node, directory, where)
        if kind in ('ForClause', 'WhileClause'):
            return self.loop(node, directory, where)
        if kind == 'CaseClause':
            self.shape('case', node)
            self.value(node['Word'], directory)
            for item in node.get('Items', []):
                for pattern in item.get('Patterns', []):
                    self.value(pattern, directory)
            before = self.capture()
            paths = [(before, directory)]  # No pattern matches.
            for item in node.get('Items', []):
                self.restore(before)
                result = self.statements(item.get('Stmts', []), directory)
                paths.append((self.capture(), result))
            return self.join(paths, 'case', where)
        raise Refusal(f'unsupported shell construct {kind!r} at {where}')

    def declaration(self, node: dict, directory: Path, where: str) -> Path:
        """`local`, `declare` and `export`; inside a function `declare` is local, as in bash."""
        variant = node.get('Variant', {}).get('Value')
        if any(a.get('Name', {}).get('Value') in SENSITIVE for a in node.get('Args', [])):
            exact_use(self.audit, node, self.where, 'assignment')
        if variant not in ('local', 'declare', 'export'):
            raise Refusal(f'unsupported shell declaration at {where}')
        options = []
        for item in node.get('Args', []):
            if not item.get('Name') and item.get('Value'):
                option = self.value(item['Value'], directory)
                if option not in ('-a', '-A', '-gA'):
                    raise Refusal(f'unsupported shell declaration option at {where}')
                options.append(option)
        scoped = variant == 'local' or (variant == 'declare' and '-gA' not in options)
        if scoped and not self.locals:
            if variant == 'local':
                raise Refusal(f'uncensused shell local outside a function at {where}')
            scoped = False
        self.shape(f'declaration.{variant}' + ('-global' if variant == 'declare' and not scoped else ''), node)
        for item in node.get('Args', []):
            name = item.get('Name', {}).get('Value')
            if name and variant == 'export':
                self.exported.add(name)
            if name and scoped:
                self.locals[-1].setdefault(name, self.env.get(name, MISSING))
                self.env[name] = ''  # A new local is empty until assigned.
        self.assignments(node.get('Args', []), directory)
        return directory

    def conditional(self, node: dict, directory: Path, where: str) -> Path | None:
        """Join both branches; a missing branch continues from the test."""
        if not node.get('Cond'):
            return self.statements(node.get('Then', []), directory)
        self.shape('if', node)
        condition = node.get('Cond', [])
        certain = len(condition) == 1 and self.certain(condition[0], directory)
        tested = self.statements(condition, directory)
        if tested is None:
            return None
        after = self.capture()
        then = self.statements(node.get('Then', []), tested)
        paths = [(self.capture(), then)]
        self.restore(after)
        if certain:  # The test always succeeds: the other branch is inspected, never taken.
            if node.get('Else'):
                self.audit.inspecting += 1
                try:
                    self.statement(node['Else'], tested)
                finally:
                    self.audit.inspecting -= 1
            self.restore(paths[0][0])
            return then
        otherwise = self.statement(node['Else'], tested) if node.get('Else') else tested
        paths.append((self.capture(), otherwise))
        return self.join(paths, 'conditional', where)

    def loop(self, node: dict, directory: Path, where: str) -> Path | None:
        """A body runs any number of times: what any iteration changes is runtime at every iteration and after.

        The body is walked to a fixed point: each value an iteration can change is
        runtime on entry, so a later iteration never reads an earlier literal.
        """
        start = self.capture()
        loop = node.get('Loop', {})
        kind = node.get('Type')
        if kind == 'ForClause' and loop.get('Type') == 'CStyleLoop':
            self.shape('for.arithmetic', node)
            for part in ('Init', 'Cond', 'Post'):
                if loop.get(part):
                    self.arithmetic(loop[part], directory)
            items = None
        elif kind == 'ForClause' and loop.get('Type') == 'WordIter':
            self.shape('for.words', node)
            items = [value for item in loop.get('Items', []) for value in self.fields(item, directory)]
        elif kind == 'ForClause':
            raise Refusal(f'unsupported shell loop at {where}')
        else:
            self.shape('while', node)
            items = None
        entry = self.capture()
        literal = bool(items) and not any(isinstance(item, Runtime) for item in items)
        values = items if literal else ([RUNTIME] if items is not None else [None])
        while True:
            ends, leaving = [], []
            for value in values:
                self.restore(entry)
                if value is not None:
                    self.env[loop['Name']['Value']] = value
                def body() -> Path | None:
                    """One iteration: the test of a while loop, then the body."""
                    if kind == 'WhileClause':
                        tested = self.statements(node.get('Cond', []), directory)
                        leaving.append((self.capture(), tested))
                        if tested is None:
                            return None
                    return self.statements(node.get('Do', []), directory)
                frame, result = self.framed('loop', body)
                ends.append((self.capture(), result))
                ends.extend(frame.resumes)  # `continue` starts the next iteration.
                leaving.extend(frame.states)  # `break` leaves the loop.
            changed = set()
            for state, result in ends:
                if result is None:
                    continue
                for key in set(state[0]) | set(entry[0]):
                    if state[0].get(key, MISSING) != entry[0].get(key, MISSING) and entry[0].get(key) is not RUNTIME:
                        changed.add(key)
                for key in state[1] - entry[1]:
                    changed.add(key)
            if not changed:
                break
            env, exported, functions, scopes = entry
            entry = ({**env, **{key: RUNTIME for key in changed}}, exported | {k for s, _ in ends for k in s[1]},
                     functions, scopes)
        paths = list(leaving)
        if kind != 'WhileClause':
            paths += ends
            if not literal and (items is None or any(isinstance(item, Fields) for item in items) or not items):
                paths.append((start if items is not None else entry, directory))
        result = self.join(paths, 'loop', where)
        if result is not None and result != directory:
            raise Refusal(f'ambiguous shell directory after loop at {where}')
        return result

    def binary(self, node: dict, directory: Path, where: str) -> Path | None:
        """`&&` and `||` join the paths where the right side does and does not run; pipelines are subshells."""
        if node['Op'] in (12, 13):
            self.shape('pipe' if node['Op'] == 12 else 'pipe-all', node)
            self.isolated(lambda: self.statement(node['X'], directory))
            self.isolated(lambda: self.statement(node['Y'], directory))
            return directory
        if node['Op'] not in (10, 11):
            raise Refusal(f'unsupported shell operator at {where}')
        certain = self.certain(node['X'], directory)
        left = self.statement(node['X'], directory)
        if left is None:
            return None
        after = self.capture()
        right = self.statement(node['Y'], left)
        if node['Op'] == 10:
            self.shape('and', node)
            if certain:
                return right
            paths = [(after, left), (self.capture(), right)]
            return self.join(paths, '&&', where)
        self.shape('or', node)
        if certain:
            self.restore(after)
            return left
        return self.join([(after, left), (self.capture(), right)], '||', where)

    def call(self, node: dict, directory: Path, where: str, inline: str | None) -> Path | None:
        """Execute no commands; resolve the lexical effects of a simple call."""
        assigns = node.get('Assigns', [])
        if any(a.get('Name', {}).get('Value') in SENSITIVE for a in assigns):
            exact_use(self.audit, node, self.where, 'assignment')
        # Words expand before the command's own assignments take effect, as in the shell.
        args = [value for word in node.get('Args', []) for value in self.fields(word, directory)]
        if not args:
            self.assignments(assigns, directory)
            return directory
        if inline is not None:
            if len(args) < 2 or args[1] != '-':
                raise Refusal(f'unclassified interpreter input arguments at {where}')
            return directory
        name = args[0]
        if assigns and self.dialect == 'sh' and not isinstance(name, Runtime) and \
                name in WALKER_BUILTINS | {'set', 'export', ':', 'exec', 'eval', 'readonly', 'times', 'umask'}:
            raise Refusal(f'uncensused assignment prefix on a POSIX special builtin at {where}')
        saved = self.capture()
        prefix = {a.get('Name', {}).get('Value') for a in assigns} - {None}
        if assigns:
            # The assignments last for this command only, exported to what it runs.
            self.shape('call.prefix-assignment', node)
            self.assignments(assigns, directory)
            self.exported |= prefix
        if not isinstance(name, Runtime) and name in self.names:
            result = self.function(args, directory, where)
        else:
            if not isinstance(name, Runtime):
                self.commands.add(name)
            result = self.builtin(args, node, directory, where, prefix)
        for key in prefix:
            if key in saved[0]:
                self.env[key] = saved[0][key]
            else:
                self.env.pop(key, None)
            self.exported = (self.exported - {key}) | ({key} & saved[1])
        return result

    def builtin(self, args: list[str], node: dict, directory: Path, where: str, prefix: set) -> Path | None:
        """The walker's own builtins, then the command table."""
        name = args[0]
        if name == 'trap':
            self.trap(args, where)
        elif name == 'cd':
            return self.change_directory(args, directory, where)
        elif name in ('source', '.'):
            if self.dialect == 'sh' and name == 'source':
                raise Refusal(f'uncensused POSIX shell source at {where}')
            return self.source_file(args, directory, where, node)
        elif name == 'read':
            exact_use(self.audit, node, self.where, 'read')
            self.shape('read', node)
            for operand in args[1:]:
                if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', operand):
                    self.env[operand] = Runtime('${RUNTIME}')
        elif name == 'printf' and '-v' in args[1:]:
            raise Refusal(f'uncensused printf -v at {where}')
        elif name == 'unset':
            if any(operand in SENSITIVE for operand in args[1:]):
                exact_use(self.audit, node, self.where, 'unset')
            self.shape('unset', node)
            for operand in args[1:]:
                if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', operand):
                    raise Refusal(f'uncensused unset operand at {where}')
                self.env.pop(operand, None)
                self.exported.discard(operand)
        elif name == 'shift':
            if len(args) > 2 or (len(args) == 2 and not args[1].isdigit()):
                raise Refusal(f'uncensused shift operand at {where}')
            self.shape('shift', node)
            count = int(args[1]) if len(args) == 2 else 1
            positional = {int(k): v for k, v in self.env.items() if k.isdigit() and k != '0'}
            for key in positional:
                self.env.pop(str(key))
            self.env.update({str(k - count): v for k, v in positional.items() if k > count})
        elif name in ('exit', 'return', 'break', 'continue'):
            self.audit.command(args, where, directory)  # Operand forms are table data.
            if name in ('break', 'continue') and args[1:] not in ([], ['1']):
                raise Refusal(f'uncensused multi-level {name} at {where}')
            self.shape(f'escape.{name}', node)
            self.escape(name, directory, where)
            return None
        else:
            if name == 'xargs':
                exact_use(self.audit, node, self.where, name)
            self.shape('call.command', node)
            self.audit.env = dict(self.env)
            self.audit.exported_env = {k: v for k, v in self.env.items() if k in self.exported}
            self.audit.command(args, where, directory)
            if name == 'exec' and len(args) > 1:
                return None  # The shell is replaced by the command.
        return directory

    def change_directory(self, args: list[str], directory: Path, where: str) -> Path:
        """`cd` to one literal operand, followed lexically; options, `-` and links refuse."""
        operands = args[1:]
        if operands[:1] == ['--']:
            operands = operands[1:]
        if len(operands) != 1 or (not isinstance(operands[0], Runtime) and operands[0].startswith('-')):
            raise Refusal(f'unresolved shell cd at {where}')
        operand = operands[0]
        if isinstance(operand, Runtime):
            declaration = self.audit.table['scripts'].get(self.where.split(':')[0])
            if not declaration:
                raise Refusal(f'unresolved shell cd at {where}')
            self.shape('cd.runtime')
            self.audit.residue.add(f'{where}: declared runtime shell directory')
            target = (directory / operand).resolve()
            self.audit.runtime_directories.add(target)
            return target
        self.shape('cd')
        logical = Path(_normpath(str(directory / operand)))
        if logical.exists() and logical != logical.resolve():
            raise Refusal(f'unmodelled shell cd through a symbolic link at {where}')
        return logical

    def trap(self, args: list[str], where: str) -> None:
        """A handler runs later, at a signal, return or exit: its variables and directory are unknown here."""
        if len(args) < 3:
            raise Refusal(f'unsupported shell trap at {where}')
        if args[1] in ('-', ''):
            self.shape('trap.reset')
            return
        if isinstance(args[1], Runtime):
            # Handler text assembled at run time is parsed by the shell later: declared residue only.
            if not self.audit.table['scripts'].get(self.where.split(':')[0]):
                raise Refusal(f'unclassified runtime trap handler at {where}')
            self.shape('trap.runtime')
            self.audit.residue.add(f'{where}: declared runtime trap handler')
            return
        self.shape('trap')
        parsed = shell_tree(args[1], self.audit.parser, self.dialect)
        shell_nodes(self.audit, parsed, self.where)
        unknown = Path('/${TRAP_DIRECTORY}')  # Outside the tree; nothing resolves under it.
        self.audit.runtime_directories.add(unknown)
        def handler() -> None:
            """The handler's statements, with every variable unknown."""
            self.env = {key: RUNTIME for key in self.env}
            self.statements(parsed.get('Stmts', []), unknown)
        self.isolated(handler)

    def source_file(self, args: list[str], directory: Path, where: str, node: dict) -> Path | None:
        """Source into the caller's directory, variables and function namespace."""
        if len(args) != 2 or isinstance(args[1], Runtime):
            raise Refusal(f'unfollowed source at {where}')
        if '/' not in args[1]:
            raise Refusal(f'uncensused shell source path search for {args[1]!r} at {where}')
        path = (directory / args[1]).resolve()
        if not path.is_file() or not path.is_relative_to(self.audit.root):
            raise Refusal(f'unresolved script {args[1]!r} at {where}')
        relative = path.relative_to(self.audit.root).as_posix()
        declaration = self.audit.table['scripts'].get(relative)
        if declaration and declaration['sha256'] != sha256(path):
            raise Refusal(f'changed declared script {relative!r}')
        exact_use(self.audit, node, self.where, 'source')
        if relative in self.active:
            raise Refusal(f'recursive source {relative!r} at {where}')
        self.shape('source', node)
        self.audit.inputs[relative] = sha256(path)
        parsed = shell_tree(path.read_text(), self.audit.parser, self.dialect)
        shell_nodes(self.audit, parsed, relative)
        defined = function_names(parsed)
        if defined & self.commands:
            raise Refusal(f'sourced function {sorted(defined & self.commands)[0]!r} shadows a command '
                          f'already resolved at {where}')
        self.names |= defined
        self.active.add(relative)
        self.words[relative] = args[1]
        previous = self.where
        self.where = relative
        try:
            frame, result = self.framed('source', lambda: self.statements(parsed.get('Stmts', []), directory))
        finally:
            self.where = previous
            self.active.remove(relative)
        return self.join([(self.capture(), result), *frame.states], 'source', where)

    def function(self, args: list[str], directory: Path, where: str) -> Path | None:
        """Apply every reachable definition from the same incoming state."""
        alternatives = self.functions.get(args[0], [None])
        if None in alternatives:
            # Where the definition did not run the shell searches PATH: a runtime command
            # name, never a resolved builtin or program, so only declared residue.
            if not self.audit.table['scripts'].get(self.where.split(':')[0]) or alternatives == [None]:
                raise Refusal(f'shell function {args[0]!r} is not defined on every path at {where}')
            self.shape('function.call-partly-defined')
            self.audit.residue.add(f'{where}: declared runtime command name where {args[0]!r} is undefined')
        else:
            self.shape('function.call')
        before = self.capture()
        paths = [(before, directory)] if None in alternatives else []
        for body, origin in [alternative for alternative in alternatives if alternative is not None]:
            self.restore(before)
            result = self.function_body(body, origin, args, directory, where)
            paths.append((self.capture(), result))
        return self.join(paths, 'function call', where)

    def function_body(self, body: dict, origin: str, args: list[str], directory: Path, where: str) -> Path | None:
        """Preserve global assignments while restoring positional and local values on every exit."""
        name = args[0]
        if name in self.active:
            raise Refusal(f'recursive shell function {name!r} at {where}')
        self.active.add(name)
        scoped = {key: value for key, value in self.env.items() if key.isdigit() and key != '0'}
        for key in scoped:
            self.env.pop(key)
        for index, value in enumerate(args[1:], 1):
            scoped.setdefault(str(index), MISSING)
            self.env[str(index)] = value
        self.locals.append(scoped)
        previous = self.where
        self.where = origin
        try:
            frame, result = self.framed('function', lambda: self.statement(body, directory))
            result = self.join([(self.capture(), result), *frame.states], 'function', where)
        finally:
            self.where = previous
        for key, value in self.locals.pop().items():
            if value is MISSING:
                self.env.pop(key, None)
            else:
                self.env[key] = value
        self.active.remove(name)
        return result

    def run(self, source: str, directory: Path) -> None:
        """Parse one program and audit even functions absent from literal calls."""
        source = re.sub(r'\$\{\{.*?\}\}', '${RUNTIME}', source)
        tree = shell_tree(source, self.audit.parser, self.dialect)
        shell_nodes(self.audit, tree, self.where)
        self.names = function_names(tree)
        self.frames.append(Frame('process'))
        try:
            end = self.statements(tree.get('Stmts', []), directory)
            # Every definition is inspected, called or not; this walk resolves nothing that runs.
            for name in sorted(self.functions):
                for alternative in self.functions[name]:
                    if alternative is None or name in self.active:
                        continue
                    saved = self.capture()
                    self.audit.inspecting += 1
                    try:
                        self.function_body(alternative[0], alternative[1], [name], end or directory, self.where)
                    finally:
                        self.audit.inspecting -= 1
                        self.restore(saved)
        finally:
            self.frames.pop()
