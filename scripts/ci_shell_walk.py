#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Walk the censused shell syntax without executing candidate commands."""

from pathlib import Path
import re

from ci_command_table import Refusal, Runtime, nodes, shell_tree, sha256
from ci_syntax import SENSITIVE, exact_use, shell_nodes


class Shell:
    """Keep variables, directories and function names in their actual scope."""

    def __init__(self, audit: object, where: str) -> None:
        self.audit = audit
        self.where = where
        self.invocation_source = where.split(':')[0]
        self.functions = {}
        self.active = set()
        self.env = dict(audit.env)
        self.exported = set(audit.exported_env)
        self.locals = []
        self.source = ''

    def location(self, node: dict) -> str:
        """Give every refusal and residue a source location."""
        return f"{self.where}:{node.get('Pos', {}).get('Line', 1)}"

    def value(self, node: dict, directory: Path, quoted: bool = False) -> str:
        """Resolve literals and simple expansions; walk all nested execution."""
        kind = node.get('Type')
        if kind == 'Lit':
            pattern = r'\\([$`"\\\n])' if quoted else r'\\(.)'
            return re.sub(pattern, r'\1', node.get('Value', '')).replace('\\\n', '')
        if kind == 'SglQuoted':
            return node.get('Value', '')
        if kind == 'ParamExp':
            name = node['Param']['Value']
            if name == 'BASH_SOURCE':
                return str(self.audit.root / self.where.split(':')[0])
            if name == '0' and self.invocation_source.endswith('.sh'):
                return str(self.audit.root / self.invocation_source)
            for child in nodes(node):
                if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst'):
                    self.value(child, directory)
            if set(node) - {'Type', 'Pos', 'End', 'Short', 'Dollar', 'Rbrace', 'Param'}:
                # Parameter operators are data; their nested substitutions were walked.
                return Runtime('${RUNTIME}')
            return self.env.get(name, Runtime('${' + name + '}'))
        if kind in ('CmdSubst', 'ProcSubst'):
            saved = dict(self.env)
            functions = dict(self.functions)
            end = self.statements(node.get('Stmts', []), directory)
            self.env = saved
            self.functions = functions
            calls = [n for n in nodes(node.get('Stmts', [])) if n.get('Type') == 'CallExpr']
            if kind == 'CmdSubst' and calls:
                last = calls[-1]
                args = last.get('Args', [])
                if len(args) == 1 and args[0].get('Parts') == [{'Type': 'Lit', 'Value': 'pwd'}]:
                    return str(end)
                # Use parsed words rather than source-text replacement for path idioms.
                first = args[0].get('Parts', []) if args else []
                if first and first[0].get('Value') == 'pwd' and len(args) == 1:
                    return str(end)
                if first and first[0].get('Value') in ('dirname', 'realpath') and len(args) == 2:
                    value = Path(self.value(args[1], directory))
                    return str(value.parent if first[0]['Value'] == 'dirname' else (directory / value).resolve())
            return Runtime('${RUNTIME}')
        if kind == 'ArithmExp':
            for child in nodes(node):
                if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst'):
                    self.value(child, directory)
            return Runtime('${RUNTIME}')
        if kind in ('DblQuoted', 'Word') or (kind is None and 'Parts' in node):
            parts = [self.value(part, directory, quoted or kind == 'DblQuoted') for part in node.get('Parts', [])]
            value = ''.join(parts)
            return Runtime(value) if any(isinstance(part, Runtime) for part in parts) else value
        raise Refusal(f'unsupported shell word {kind!r} at {self.location(node)}')

    def assignments(self, values: list[dict], directory: Path) -> None:
        """Resolve scalar assignments without inventing array contents."""
        for assignment in values:
            name = assignment.get('Name', {}).get('Value')
            if not name:
                continue
            if assignment.get('Value'):
                value = self.value(assignment['Value'], directory)
                if assignment.get('Index'):
                    value = Runtime('${RUNTIME}')
                elif assignment.get('Append'):
                    previous = self.env.get(name, '')
                    joined = previous + value
                    value = Runtime(joined) if isinstance(previous, Runtime) or isinstance(value, Runtime) else joined
                self.env[name] = value
            elif assignment.get('Array'):
                for item in assignment['Array'].get('Elems', []):
                    if item.get('Value'):
                        self.value(item['Value'], directory)
                self.env[name] = Runtime('${RUNTIME}')

    def statements(self, statements: list[dict], directory: Path) -> Path:
        """Sequence statements; a subshell returns the parent's directory."""
        for statement in statements:
            directory = self.statement(statement, directory)
        return directory

    def statement(self, statement: dict, directory: Path) -> Path:
        """Classify each supported compound form, refusing unknown nodes."""
        node = statement.get('Cmd', statement)
        kind = node.get('Type')
        where = self.location(node)
        inline = None
        if statement.get('Background'):
            raise Refusal(f'uncensused shell background operator at {where}')
        for redirect in statement.get('Redirs', []):
            if any(n.get('Type') == 'ParamExp' and n['Param']['Value'] in ('GITHUB_PATH', 'GITHUB_ENV')
                   for n in nodes(redirect)):
                exact_use(self.audit, statement, self.where, 'environment-file')
            if redirect.get('Word'):
                self.value(redirect['Word'], directory)
            if redirect.get('Hdoc'):
                self.value(redirect['Hdoc'], directory)
            if redirect.get('Hdoc') and node.get('Type') == 'CallExpr':
                args = node.get('Args', [])
                name = self.value(args[0], directory) if args else ''
                if name in ('python', 'python3'):
                    inline = self.value(redirect['Hdoc'], directory)
                    self.audit.python_command([name, '-c', inline], where, directory, {})
                elif name in ('bash', 'sh'):
                    raise Refusal(f'unclassified interpreter input at {where}')
        if kind == 'CallExpr':
            return self.call(node, directory, where, inline)
        if kind == 'DeclClause':
            if any(a.get('Name', {}).get('Value') in SENSITIVE for a in node.get('Args', [])):
                exact_use(self.audit, node, self.where, 'assignment')
            if node.get('Variant', {}).get('Value') not in ('local', 'declare', 'export', 'readonly'):
                raise Refusal(f'unsupported shell declaration at {where}')
            for item in node.get('Args', []):
                if not item.get('Name') and item.get('Value'):
                    option = self.value(item['Value'], directory)
                    if option.startswith('-') and option not in ('-a', '-A', '-gA'):
                        raise Refusal(f'unsupported shell declaration option at {where}')
                name = item.get('Name', {}).get('Value')
                if name and node['Variant']['Value'] == 'export':
                    self.exported.add(name)
                if name and self.locals and node['Variant']['Value'] == 'local':
                    self.locals[-1].setdefault(name, self.env.get(name))
            self.assignments(node.get('Args', []), directory)
            return directory
        if kind == 'FuncDecl':
            name = node['Name']['Value']
            self.functions[name] = [(node['Body'], self.where)]
            return directory
        if kind in ('Block', 'Subshell'):
            saved = dict(self.env)
            functions = dict(self.functions)
            result = self.statements(node.get('Stmts', []), directory)
            if kind == 'Subshell':
                self.env = saved
                self.functions = functions
                return directory
            return result
        if kind == 'BinaryCmd':
            return self.binary(node, directory, where)
        if kind == 'IfClause' or (kind is None and 'Then' in node):
            return self.conditional(node, directory, where)
        if kind in ('ForClause', 'WhileClause', 'CaseClause'):
            before = dict(self.env)
            if kind == 'ForClause':
                loop = node['Loop']
                if loop.get('Type') not in ('WordIter', 'CStyleLoop'):
                    raise Refusal(f'unsupported shell loop at {where}')
                for child in nodes(loop):
                    if child.get('Type') in ('CmdSubst', 'ProcSubst'):
                        self.value(child, directory)
                values = [self.value(item, directory) for item in loop.get('Items', [])]
                if loop.get('Name') and values and all(not isinstance(value, Runtime) for value in values):
                    for value in values:
                        self.env[loop['Name']['Value']] = value
                        if self.statements(node.get('Do', []), directory) != directory:
                            raise Refusal(f'ambiguous shell directory after loop at {where}')
                    return directory
                if loop.get('Name'):
                    self.env[loop['Name']['Value']] = Runtime('${RUNTIME}')
                bodies = [node.get('Do', [])]
            elif kind == 'WhileClause':
                self.statements(node.get('Cond', []), directory)
                bodies = [node.get('Do', [])]
            else:
                self.value(node['Word'], directory)
                bodies = [item.get('Stmts', []) for item in node.get('Items', [])]
            for body in bodies:
                if self.statements(body, directory) != directory:
                    raise Refusal(f'ambiguous shell directory after loop or case at {where}')
            self.env = {k: v if self.env.get(k) == v else Runtime('${RUNTIME}') for k, v in before.items()}
            return directory
        raise Refusal(f'unsupported shell construct {kind!r} at {where}')

    def conditional(self, node: dict, directory: Path, where: str) -> Path:
        """Join branch effects without overwriting reachable function alternatives."""
        if not node.get('Cond'):
            return self.statements(node.get('Then', []), directory)
        if self.statements(node.get('Cond', []), directory) != directory:
            raise Refusal(f'ambiguous shell directory in conditional test at {where}')
        before = dict(self.env)
        before_functions = dict(self.functions)
        left = self.statements(node.get('Then', []), directory)
        left_functions = dict(self.functions)
        left_env = dict(self.env)
        self.env = dict(before)
        self.functions = before_functions
        right = self.statement(node['Else'], directory) if node.get('Else') else directory
        for name in left_functions.keys() | self.functions.keys():
            alternatives = [*left_functions.get(name, []), *self.functions.get(name, [])]
            self.functions[name] = [v for i, v in enumerate(alternatives) if v not in alternatives[:i]]
        if left != right:
            raise Refusal(f'ambiguous shell directory after conditional at {where}')
        self.env = {k: v if self.env.get(k) == v else Runtime('${RUNTIME}') for k, v in left_env.items()}
        return left

    def binary(self, node: dict, directory: Path, where: str) -> Path:
        """Keep fallback and pipeline directories separate from successful operands."""
        before = dict(self.env)
        functions = dict(self.functions)
        left = self.statement(node['X'], directory)
        if node['Op'] == 10:  # The right side of && runs after left succeeds.
            return self.statement(node['Y'], left)
        left_env = dict(self.env)
        self.env = dict(before)
        if node['Op'] in (12, 13):
            self.functions = dict(functions)
        right = self.statement(node['Y'], directory)
        if node['Op'] == 11:
            command = node['Y'].get('Cmd', {})
            args = command.get('Args', [])
            terminating = (command.get('Type') == 'CallExpr' and args and
                           self.value(args[0], directory) in ('exit', 'return'))
            if terminating:
                self.env = left_env
                return left
            if left != right:
                raise Refusal(f'ambiguous shell directory after fallback at {where}')
            self.env = {key: value if self.env.get(key) == value else Runtime('${RUNTIME}')
                        for key, value in left_env.items()}
            return left
        if node['Op'] in (12, 13):
            self.env = before
            self.functions = functions
            return directory
        raise Refusal(f'unsupported shell operator at {where}')

    def call(self, node: dict, directory: Path, where: str, inline: str | None) -> Path:
        """Execute no commands; resolve the lexical effects of a simple call."""
        saved = dict(self.env)
        if any(a.get('Name', {}).get('Value') in SENSITIVE for a in node.get('Assigns', [])):
            exact_use(self.audit, node, self.where, 'assignment')
        self.assignments(node.get('Assigns', []), directory)
        args = [self.value(arg, directory) for arg in node.get('Args', [])]
        if not args:
            return directory
        if inline is not None:
            if len(args) < 2 or args[1] != '-':
                raise Refusal(f'unclassified interpreter input arguments at {where}')
            return directory
        if args[0] in self.functions:
            directory = self.function(args, directory, where)
        elif args[0] == 'trap':
            if len(args) < 3:
                raise Refusal(f'unsupported shell trap at {where}')
            if args[1] != '-':
                saved_trap = dict(self.env)
                parsed = shell_tree(args[1], self.audit.parser)
                shell_nodes(self.audit, parsed, self.where)
                self.statements(parsed.get('Stmts', []), directory)
                self.env = saved_trap
        elif args[0] == 'cd':
            operands = args[1:]
            if operands[:1] == ['--']:
                operands = operands[1:]
            if len(operands) != 1:
                raise Refusal(f'unresolved shell cd at {where}')
            if isinstance(operands[0], Runtime):
                declaration = self.audit.table['scripts'].get(self.where.split(':')[0])
                if not declaration:
                    raise Refusal(f'unresolved shell cd at {where}')
                self.audit.residue.add(f'{where}: declared runtime shell directory')
            directory = (directory / operands[0]).resolve()
            if isinstance(operands[0], Runtime):
                self.audit.runtime_directories.add(directory)
        elif args[0] in ('source', '.'):
            directory = self.source_file(args, directory, where, node)
        elif args[0] == 'read':
            exact_use(self.audit, node, self.where, 'read')
            for name in args[1:]:
                if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name):
                    self.env[name] = Runtime('${RUNTIME}')
        elif args[0] == 'printf' and '-v' in args[1:]:
            raise Refusal(f'uncensused printf -v at {where}')
        elif args[0] == 'unset':
            if any(name in SENSITIVE for name in args[1:]):
                raise Refusal(f'uncensused special-variable unset at {where}')
            for name in args[1:]:
                if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name):
                    raise Refusal(f'uncensused unset operand at {where}')
                self.env.pop(name, None)
                self.exported.discard(name)
        elif args[0] == 'shift':
            if len(args) > 2 or (len(args) == 2 and not args[1].isdigit()):
                raise Refusal(f'uncensused shift operand at {where}')
            count = int(args[1]) if len(args) == 2 else 1
            positional = {int(k): v for k, v in self.env.items() if k.isdigit() and k != '0'}
            for key in positional:
                self.env.pop(str(key))
            self.env.update({str(k - count): v for k, v in positional.items() if k > count})
        else:
            if args[0] == 'xargs':
                exact_use(self.audit, node, self.where, args[0])
            self.audit.env = dict(self.env)
            prefix = {a.get('Name', {}).get('Value') for a in node.get('Assigns', [])}
            self.audit.exported_env = {k: v for k, v in self.env.items() if k in self.exported | prefix}
            self.audit.command(args, where, directory)
        if node.get('Assigns'):
            self.env = saved
        return directory

    def source_file(self, args: list[str], directory: Path, where: str, node: dict) -> Path:
        """Source into the caller's directory, variables and function namespace."""
        if len(args) != 2 or isinstance(args[1], Runtime):
            raise Refusal(f'unfollowed source at {where}')
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
        self.audit.inputs[relative] = sha256(path)
        self.active.add(relative)
        previous = self.where
        self.where = relative
        try:
            parsed = shell_tree(path.read_text(), self.audit.parser)
            shell_nodes(self.audit, parsed, relative)
            return self.statements(parsed.get('Stmts', []), directory)
        finally:
            self.where = previous
            self.active.remove(relative)

    def function(self, args: list[str], directory: Path, where: str) -> Path:
        """Apply every reachable definition from the same incoming state."""
        before = dict(self.env)
        results = []
        environments = []
        for body, origin in self.functions[args[0]]:
            self.env = dict(before)
            results.append(self.function_body(body, origin, args, directory, where))
            environments.append(dict(self.env))
        if len(set(results)) != 1:
            raise Refusal(f'ambiguous function directory at {where}')
        keys = set().union(*environments)
        self.env = {key: environments[0].get(key, Runtime('${RUNTIME}'))
                    if all(e.get(key) == environments[0].get(key) for e in environments)
                    else Runtime('${RUNTIME}') for key in keys}
        return results[0]

    def function_body(self, body: dict, origin: str, args: list[str], directory: Path, where: str) -> Path:
        """Preserve global assignments while restoring positional and local values."""
        name = args[0]
        if name in self.active:
            raise Refusal(f'recursive shell function {name!r} at {where}')
        self.active.add(name)
        scoped = {key: value for key, value in self.env.items() if key.isdigit()}
        for key in scoped:
            self.env.pop(key)
        for index, value in enumerate(args[1:], 1):
            key = str(index)
            scoped.setdefault(key, None)
            self.env[key] = value
        self.locals.append(scoped)
        previous = self.where
        self.where = origin
        try:
            result = self.statement(body, directory)
        finally:
            self.where = previous
        for key, value in self.locals.pop().items():
            if value is None:
                self.env.pop(key, None)
            else:
                self.env[key] = value
        self.active.remove(name)
        return result

    def run(self, source: str, directory: Path) -> None:
        """Parse one script and audit even functions absent from literal calls."""
        source = re.sub(r'\$\{\{.*?\}\}', '${RUNTIME}', source)
        tree = shell_tree(source, self.audit.parser)
        shell_nodes(self.audit, tree, self.where)
        self.statements(tree.get('Stmts', []), directory)
        for name, body in list(self.functions.items()):
            if name in self.active:
                continue
            saved = dict(self.env)
            self.function([name], directory, self.where)
            self.env = saved
