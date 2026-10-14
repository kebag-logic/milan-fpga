#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Walk the censused shell syntax without executing candidate commands."""

from pathlib import Path
import re

from ci_command_table import Refusal, nodes, shell_tree


class Shell:
    """Keep variables, directories and function names in their actual scope."""

    def __init__(self, audit: object, where: str) -> None:
        self.audit = audit
        self.where = where
        self.functions = {}
        self.active = set()
        self.env = dict(audit.env)
        self.source = ''

    def location(self, node: dict) -> str:
        """Give every refusal and residue a source location."""
        return f"{self.where}:{node.get('Pos', {}).get('Line', 1)}"

    def value(self, node: dict, directory: Path) -> str:
        """Resolve literals and simple expansions; walk all nested execution."""
        kind = node.get('Type')
        if kind == 'Lit':
            return re.sub(r'\\(.)', r'\1', node.get('Value', ''))
        if kind == 'SglQuoted':
            return node.get('Value', '')
        if kind == 'ParamExp':
            name = node['Param']['Value']
            if name == 'BASH_SOURCE':
                return str(self.audit.root / self.where.split(':')[0])
            if name == '0' and self.where.split(':')[0].endswith('.sh'):
                return str(self.audit.root / self.where.split(':')[0])
            for child in nodes(node):
                if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst'):
                    self.value(child, directory)
            if set(node) - {'Type', 'Pos', 'End', 'Short', 'Dollar', 'Rbrace', 'Param'}:
                # Parameter operators are data; their nested substitutions were walked.
                return '${RUNTIME}'
            return self.env.get(name, '${' + name + '}')
        if kind in ('CmdSubst', 'ProcSubst'):
            saved = dict(self.env)
            end = self.statements(node.get('Stmts', []), directory)
            self.env = saved
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
            return '${RUNTIME}'
        if kind == 'ArithmExp':
            for child in nodes(node):
                if child is not node and child.get('Type') in ('CmdSubst', 'ProcSubst'):
                    self.value(child, directory)
            return '${RUNTIME}'
        if kind in ('DblQuoted', 'Word') or (kind is None and 'Parts' in node):
            return ''.join(self.value(part, directory) for part in node.get('Parts', []))
        raise Refusal(f'unsupported shell word {kind!r} at {self.location(node)}')

    def assignments(self, values: list[dict], directory: Path) -> None:
        """Resolve scalar assignments without inventing array contents."""
        for assignment in values:
            name = assignment.get('Name', {}).get('Value')
            if not name:
                continue
            if assignment.get('Value'):
                self.env[name] = self.value(assignment['Value'], directory)
            elif assignment.get('Array'):
                for item in assignment['Array'].get('Elems', []):
                    if item.get('Value'):
                        self.value(item['Value'], directory)
                self.env[name] = '${RUNTIME}'

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
        for redirect in statement.get('Redirs', []):
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
            if node.get('Variant', {}).get('Value') not in ('local', 'declare', 'export', 'readonly'):
                raise Refusal(f'unsupported shell declaration at {where}')
            for item in node.get('Args', []):
                if not item.get('Name') and item.get('Value'):
                    option = self.value(item['Value'], directory)
                    if option.startswith('-') and option not in ('-a', '-A', '-gA'):
                        raise Refusal(f'unsupported shell declaration option at {where}')
            self.assignments(node.get('Args', []), directory)
            return directory
        if kind == 'FuncDecl':
            name = node['Name']['Value']
            self.functions[name] = node['Body']
            return directory
        if kind in ('Block', 'Subshell'):
            saved = dict(self.env)
            result = self.statements(node.get('Stmts', []), directory)
            if kind == 'Subshell':
                self.env = saved
                return directory
            return result
        if kind == 'BinaryCmd':
            return self.binary(node, directory, where)
        if kind == 'IfClause' or (kind is None and 'Then' in node):
            self.statements(node.get('Cond', []), directory)
            before = dict(self.env)
            left = self.statements(node.get('Then', []), directory)
            left_env = dict(self.env)
            self.env = dict(before)
            right = self.statement(node['Else'], directory) if node.get('Else') else directory
            if left != right:
                raise Refusal(f'ambiguous shell directory after conditional at {where}')
            self.env = {k: v if self.env.get(k) == v else '${RUNTIME}' for k, v in left_env.items()}
            return directory
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
                if loop.get('Name') and values and all('$' not in value for value in values):
                    for value in values:
                        self.env[loop['Name']['Value']] = value
                        if self.statements(node.get('Do', []), directory) != directory:
                            raise Refusal(f'ambiguous shell directory after loop at {where}')
                    return directory
                if loop.get('Name'):
                    self.env[loop['Name']['Value']] = '${RUNTIME}'
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
            self.env = {k: v if self.env.get(k) == v else '${RUNTIME}' for k, v in before.items()}
            return directory
        raise Refusal(f'unsupported shell construct {kind!r} at {where}')

    def binary(self, node: dict, directory: Path, where: str) -> Path:
        """Keep fallback and pipeline directories separate from successful operands."""
        before = dict(self.env)
        left = self.statement(node['X'], directory)
        if node['Op'] == 10:  # The right side of && runs after left succeeds.
            return self.statement(node['Y'], left)
        left_env = dict(self.env)
        self.env = dict(before)
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
            self.env = {key: value if self.env.get(key) == value else '${RUNTIME}'
                        for key, value in left_env.items()}
            return left
        if node['Op'] in (12, 13):
            self.env = before
            return directory
        raise Refusal(f'unsupported shell operator at {where}')

    def call(self, node: dict, directory: Path, where: str, inline: str | None) -> Path:
        """Execute no commands; resolve the lexical effects of a simple call."""
        saved = dict(self.env)
        self.assignments(node.get('Assigns', []), directory)
        args = [self.value(arg, directory) for arg in node.get('Args', [])]
        if not args:
            return directory
        if inline is not None:
            if len(args) < 2 or args[1] != '-':
                raise Refusal(f'unclassified interpreter input arguments at {where}')
            return directory
        if args[0] in self.functions:
            if args[0] in self.active:
                raise Refusal(f'recursive shell function {args[0]!r} at {where}')
            self.active.add(args[0])
            before = dict(self.env)
            self.env.update({str(i): value for i, value in enumerate(args[1:], 1)})
            directory = self.statement(self.functions[args[0]], directory)
            self.env = before
            self.active.remove(args[0])
        elif args[0] == 'trap':
            if len(args) < 3:
                raise Refusal(f'unsupported shell trap at {where}')
            if args[1] != '-':
                saved_trap = dict(self.env)
                self.statements(shell_tree(args[1], self.audit.parser).get('Stmts', []), directory)
                self.env = saved_trap
        elif args[0] == 'cd':
            operands = args[1:]
            if operands[:1] == ['--']:
                operands = operands[1:]
            if len(operands) != 1:
                raise Refusal(f'unresolved shell cd at {where}')
            if '$' in operands[0] or '<dynamic>' in operands[0]:
                declaration = self.audit.table['scripts'].get(self.where.split(':')[0])
                if not declaration:
                    raise Refusal(f'unresolved shell cd at {where}')
                self.audit.residue.add(f'{where}: declared runtime shell directory')
            directory = (directory / operands[0]).resolve()
        elif args[0] in ('source', '.'):
            if len(args) != 2 or '$' in args[1]:
                raise Refusal(f'unfollowed source at {where}')
            path = (directory / args[1]).resolve()
            self.audit.script(args[1], where, directory)
            from ci_command_table import sha256
            relative = path.relative_to(self.audit.root).as_posix()
            declaration = self.audit.table['scripts'].get(relative)
            if declaration and declaration['sha256'] == sha256(path):
                parsed = shell_tree(path.read_text(), self.audit.parser)
                for item in nodes(parsed):
                    if item.get('Type') == 'FuncDecl':
                        self.functions[item['Name']['Value']] = item['Body']
        else:
            self.audit.env = dict(self.env)
            self.audit.command(args, where, directory)
        if node.get('Assigns'):
            self.env = saved
        return directory

    def run(self, source: str, directory: Path) -> None:
        """Parse one script and audit even functions absent from literal calls."""
        source = re.sub(r'\$\{\{.*?\}\}', '${RUNTIME}', source)
        tree = shell_tree(source, self.audit.parser)
        self.statements(tree.get('Stmts', []), directory)
        for name, body in list(self.functions.items()):
            if name in self.active:
                continue
            saved = dict(self.env)
            self.active.add(name)
            self.statement(body, directory)
            self.active.remove(name)
            self.env = saved
