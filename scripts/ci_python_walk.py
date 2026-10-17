#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Follow Python programs: module search paths, imports, loaders, capabilities and literal calls.

The methods form a mixin of the command-table audit: each interpreter process has
its own modelled search path; imports follow every in-tree portion; execution or
network capability requires a reviewed declaration; literal calls are classified.
"""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass, replace
import hashlib
from pathlib import Path

from ci_command_table import TABLE, Refusal, Runtime, _dirname, _join, _normpath


NETWORK = {'urllib', 'http', 'requests', 'socket', 'ftplib', 'urllib3', 'ssl', 'pip', 'socketserver'}
CALLS = {'run', 'check_call', 'check_output', 'Popen', 'call', 'system', 'getoutput', 'getstatusoutput'}
#: Reflection that reaches module namespaces, code objects or builtins: execution capability.
REFLECTION = {'__dict__', '__globals__', '__builtins__', '__subclasses__', '__code__', '__closure__', '__func__',
              '__self__', '__getattribute__', '__getattr__', '__import__', '__loader__', '__spec__', '__reduce__',
              '__reduce_ex__', '__bases__', '__base__', '__mro__', '__kwdefaults__', '__defaults__', '__wrapped__'}
#: Builtins that evaluate, import or reach namespaces by name.
EXECUTING_BUILTINS = {'eval', 'exec', 'compile', '__import__', 'breakpoint', 'getattr', 'setattr', 'delattr',
                      'vars', 'globals', 'locals'}
# An unresolved sys.path entry makes every in-tree module portion reachable.
OPEN_SEARCH = Path('/\x00open-search-path')
# Module loaders execute located code; literal in-tree locations are followed.
LOADERS = {'runpy.run_path', 'runpy.run_module', 'importlib.util.spec_from_file_location',
           'importlib.util.module_from_spec', 'importlib.util.find_spec', 'importlib.machinery.PathFinder.find_spec',
           'importlib.machinery.SourceFileLoader', 'importlib.machinery.SourcelessFileLoader',
           'importlib.machinery.ExtensionFileLoader', 'imp.load_source', 'imp.load_module',
           'zipimport.zipimporter', 'pkgutil.get_loader', 'pkgutil.find_loader'}


@dataclass(frozen=True)
class Scope:
    """The literal-evaluation context of one Python file in one process."""

    assignments: dict
    qualified: Callable[[ast.AST], str]
    where: str
    directory: Path
    search: tuple | None = None


class PythonWalk:
    """Python analysis for the command-table audit; `self` is that audit."""

    def python_facts(self, source: str) -> tuple:
        """Parse once: imports, literal assignments and alias-qualified names."""
        if source in self.facts:
            return self.facts[source]
        tree = ast.parse(source)
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
        for name, expressions in assignments.items():
            if len(expressions) == 1 and isinstance(expressions[0], (ast.Name, ast.Attribute)):
                aliases[name] = qualified(expressions[0])
        self.facts[source] = (tree, imports, assignments, qualified)
        return self.facts[source]

    def python_program(self, path: Path, relative: str, working: Path, isolated: bool = False) -> None:
        """Walk one interpreter process with its own modelled module search path.

        The script's directory starts the path unless `-I` isolates the interpreter.
        """
        if self.python_context and self.python_context[1]:
            raise Refusal(f'child Python program {relative!r} under the unmodelled PYTHONPATH '
                          f'of {self.python_context[1]!r}')
        search, writer = self.python_search_path(relative, () if isolated else (path.resolve().parent,), working)
        previous = self.python_context
        self.python_context = (search, None)
        self.shape('py:program.isolated' if isolated else 'py:program', relative)
        try:
            for name in ('sitecustomize', 'usercustomize'):  # Imported at interpreter startup.
                for module in self.module_files(name, self.search_bases(name), relative):
                    self.shape('py:import.startup', relative)
                    self.script(str(module), relative, module.parent, working, kind='module')
            self.python_context = (search, writer)
            self.python(path.read_text(), relative, working)
        finally:
            self.python_context = previous

    def search_bases(self, name: str, search: tuple | None = None) -> list[Path]:
        """Search-path entries for an absolute import; an open path admits every portion."""
        search = search if search is not None else (self.python_context[0] if self.python_context else ())
        bases = [entry for entry in search if entry != OPEN_SEARCH]
        if OPEN_SEARCH in search:
            bases += [entry for entry in self.module_index().get(name.split('.')[0], []) if entry not in bases]
        return bases

    def python_search_path(self, main: str, initial: tuple[Path, ...], working: Path) -> tuple:
        """Grow the in-tree search path to a fixed point over the program's module closure."""
        search = list(initial)
        while True:
            closure, writer = self.python_closure(main, tuple(search), working)
            added = []
            for relative in sorted(closure):
                for entry in self.path_insertions(relative, working, tuple(search)):
                    if entry not in search and entry not in added:
                        added.append(entry)
            if not added:
                return tuple(search), writer
            search += added

    def python_closure(self, main: str, search: tuple, working: Path) -> tuple[set[str], str | None]:
        """Collect every in-tree module a program can import or load from this search path."""
        closure, queue, writer = set(), [main], None
        while queue:
            relative = queue.pop()
            if relative in closure:
                continue
            closure.add(relative)
            source = (self.root / relative).read_text()
            tree, imports, assignments, qualified = self.python_facts(source)
            if writer is None and any(isinstance(n, ast.Constant) and n.value == 'PYTHONPATH' or
                                      isinstance(n, ast.keyword) and n.arg == 'PYTHONPATH'
                                      for n in ast.walk(tree)):
                writer = relative
            origin = (self.root / relative).parent
            targets = []
            for name in imports:
                level = len(name) - len(name.lstrip('.'))
                dotted = name.lstrip('.')
                if dotted:
                    bases = [origin.parents[level - 2] if level > 1 else origin] if level else \
                        self.search_bases(dotted, search)
                    targets += self.module_files(dotted, bases, relative)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and qualified(node.func) in (
                        'runpy.run_path', 'importlib.util.spec_from_file_location'):
                    index = 0 if qualified(node.func) == 'runpy.run_path' else 1
                    if len(node.args) > index:
                        value = self.literal_path(node.args[index], Scope(assignments, qualified, relative,
                                                                          working, search))
                        if value is not None and (working / value).resolve().is_file():
                            targets.append((working / value).resolve())
                elif isinstance(node, ast.Call) and qualified(node.func) == 'runpy.run_module' and \
                        node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    targets += self.module_files(node.args[0].value, self.search_bases(
                        node.args[0].value, search), relative)
            for target in targets:
                if target.resolve().is_relative_to(self.root):
                    queue.append(target.resolve().relative_to(self.root).as_posix())
        return closure, writer

    def path_insertions(self, relative: str, working: Path, search: tuple) -> list[Path]:
        """Literal sys.path additions; any other search-path change is refused by name."""
        tree, _, assignments, qualified = self.python_facts((self.root / relative).read_text())
        result = []
        def evaluate(node: ast.AST, bindings: dict) -> None:
            """Record one resolved entry; an unresolved one may be any directory."""
            values = {**assignments, **{k: [v] for k, v in bindings.items()}}
            value = self.literal_path(node, Scope(values, qualified, relative, working, search))
            self.shape('py:search-path.open' if value is None else 'py:search-path.entry', f'{relative}:{node.lineno}')
            result.append(OPEN_SEARCH if value is None else (working / value).resolve())
        loops, functions = {}, {}
        for node in ast.walk(tree):
            if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and \
                    isinstance(node.iter, (ast.Tuple, ast.List)):
                for child in ast.walk(node):
                    if child is not node:
                        loops.setdefault(id(child), []).append(node)
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if child is not node:
                        functions[id(child)] = node  # Breadth-first: the innermost definition wins.
        def parameter_bindings(node: ast.AST, item: ast.AST) -> list[dict]:
            """Bind function parameters to the literal arguments of every same-module call."""
            function = functions.get(id(node))
            names = {n.id for n in ast.walk(item) if isinstance(n, ast.Name)}
            parameters = [a.arg for a in function.args.args] if function else []
            used = [name for name in parameters if name in names]
            if not used:
                return [{}]
            calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
                     isinstance(n.func, ast.Name) and n.func.id == function.name]
            references = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == function.name]
            if not calls or len(references) != len(calls):
                return []  # Passed as a value or called elsewhere: the argument is unknown.
            result = []
            for call in calls:
                binding = {}
                for name in used:
                    index = parameters.index(name)
                    keyword = [k.value for k in call.keywords if k.arg == name]
                    value = call.args[index] if index < len(call.args) else (keyword[0] if keyword else None)
                    if value is None:
                        return []
                    binding[name] = value
                result.append(binding)
            return result
        for node in ast.walk(tree):
            target = None
            if isinstance(node, ast.Call) and qualified(node.func) in (
                    'sys.path.insert', 'sys.path.append', 'sys.path.extend', 'site.addsitedir'):
                arguments = node.args[1:] if qualified(node.func) == 'sys.path.insert' else node.args
                if len(arguments) != 1:
                    raise Refusal(f'unmodelled sys.path modification at {relative}:{node.lineno}')
                target = arguments[0]
                if qualified(node.func) == 'sys.path.extend':
                    if not isinstance(target, (ast.List, ast.Tuple)):
                        raise Refusal(f'unmodelled sys.path modification at {relative}:{node.lineno}')
                    target = target.elts
            elif isinstance(node, (ast.Assign, ast.AugAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(qualified(t.value if isinstance(t, ast.Subscript) else t) == 'sys.path' for t in targets):
                    if not isinstance(node.value, (ast.List, ast.Tuple)):
                        raise Refusal(f'unmodelled sys.path modification at {relative}:{node.lineno}')
                    target = node.value.elts
            if target is None:
                continue
            for item in target if isinstance(target, list) else [target]:
                enclosing = loops.get(id(node), [])
                elements = [{enclosing[-1].target.id: e} for e in enclosing[-1].iter.elts] if enclosing else [{}]
                parameters = parameter_bindings(node, item)
                if not parameters:
                    self.shape('py:search-path.open', f'{relative}:{node.lineno}')
                    result.append(OPEN_SEARCH)
                for loop_binding in elements:
                    for binding in parameters:
                        evaluate(item, {**binding, **loop_binding})
        return result

    def python(self, source: str, where: str, directory: Path) -> None:
        """Detect capabilities independently of decoding, then classify literal calls."""
        tree, imports, assignments, qualified = self.python_facts(source)
        from ci_syntax import python_nodes
        python_nodes(self, tree, where)
        declaration = self.table['scripts'].get(where)
        capability = False
        for name in imports:
            if not self.python_import(name, where, directory):
                if self.allowed_import(name):
                    self.shape('py:import.external', where)
                else:
                    self.shape('py:capability.import', where)
                    capability = True
            if name.split('.')[0] in NETWORK | {
                    'subprocess', 'pty', 'asyncio', 'multiprocessing', 'ctypes', 'cffi'}:
                capability = True
        calls = []
        modules = {name.split('.')[0] for name in imports if not name.startswith('.')}
        for node in ast.walk(tree):
            symbol = qualified(node) if isinstance(node, (ast.Name, ast.Attribute)) else ''
            if symbol.startswith(('os.exec', 'os.spawn', 'os.posix_spawn', 'subprocess.', 'pty.',
                                  'asyncio.create_subprocess', 'ctypes.', 'cffi.')) or \
                    symbol in ('os.system', 'os.popen'):
                capability = True
            # Namespaces reached by reflection can hold any executing callable.
            if isinstance(node, ast.Attribute) and node.attr in REFLECTION:
                self.shape('py:capability.reflection', f'{where}:{node.lineno}')
                capability = True
            if symbol == 'sys.modules' or (symbol.startswith('builtins.') and
                                           symbol.split('.')[1] in EXECUTING_BUILTINS):
                self.shape('py:capability.namespace', f'{where}:{node.lineno}')
                capability = True
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                    qualified(node.func) in ('getattr', 'vars', 'setattr', 'delattr') and node.args and \
                    qualified(node.args[0]).split('.')[0] in modules:
                self.shape('py:capability.namespace', f'{where}:{node.lineno}')
                capability = True
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Call) and \
                    qualified(node.value.func) in ('globals', 'vars', 'locals'):
                self.shape('py:capability.namespace', f'{where}:{node.lineno}')
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
            if function in LOADERS or function.endswith(('.exec_module', '.load_module')):
                capability |= self.python_loader(function, node, Scope(assignments, qualified, where, directory))
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
            shell = keywords.get('shell')
            if function in ('os.system', 'os.popen') or (isinstance(shell, ast.Constant) and shell.value is True):
                mode = 'sh'  # The string runs under /bin/sh -c.
            elif shell is None or (isinstance(shell, ast.Constant) and shell.value is False):
                mode = 'argv'  # A string names one program; it is never split.
            else:
                mode = 'runtime'
            calls.append((node.lineno, argument, working, executable, mode))
        if capability:
            self.shape('py:capability.declared', where)
            if declaration is None:
                raise Refusal(f'undeclared executing or network script {where!r}')
            if declaration['sha256'] != hashlib.sha256(source.encode()).hexdigest():
                raise Refusal(f'changed declared script {where!r}')
            if declaration['class'] not in ('installer', 'reviewed non-installing') or not declaration.get('reason'):
                raise Refusal(f'invalid script classification {where!r}')
        self.python_calls(calls, assignments, where)

    def python_loader(self, function: str, node: ast.Call, scope: Scope) -> bool:
        """Follow literal in-tree code loaders; a runtime location is a declared capability."""
        where, directory = scope.where, scope.directory
        location = f'{where}:{node.lineno}'
        self.shape(f"py:loader.{function.rsplit('.', 1)[-1]}", location)
        if function == 'runpy.run_module':
            argument = node.args[0] if node.args else None
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                if self.python_import(argument.value, where, directory):
                    return False
                if not self.allowed_import(argument.value):
                    return True
                return False
        elif function in ('runpy.run_path', 'importlib.util.spec_from_file_location'):
            index = 0 if function == 'runpy.run_path' else 1
            argument = node.args[index] if len(node.args) > index else None
            value = self.literal_path(argument, scope) if argument else None
            if value is not None:
                path = Path(value) if Path(value).is_absolute() else directory / value
                if not path.resolve().is_relative_to(self.root) or not path.is_file():
                    raise Refusal(f'Python loader outside the source tree at {location}')
                self.script(str(path.resolve()), location, self.root, directory, kind='module')
                return False
        self.residue.add(f'{location}: runtime Python module loading')
        return True

    def literal_path(self, node: ast.AST, scope: Scope, seen: frozenset = frozenset()) -> str | None:
        """Evaluate only literal path arithmetic anchored at a constant or this file."""
        recurse = lambda child: self.literal_path(child, scope, seen)
        shape = lambda name: self.shape(f'py:path.{name}', f'{scope.where}:{getattr(node, "lineno", 0)}')
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            shape('constant')
            return node.value
        if isinstance(node, ast.Name):
            if node.id == '__file__':
                shape('file')
                return str(self.root / scope.where.split(':')[0])
            values = scope.assignments.get(node.id, [])
            if node.id in seen or len(values) > 1:
                return None
            if values:
                shape('name')
                return self.literal_path(values[0], scope, seen | {node.id})
            return self.imported_constant(scope.qualified(node), scope, seen | {node.id})
        if isinstance(node, ast.Attribute) and node.attr == 'parent':
            value = recurse(node.value)
            shape('parent')
            return None if value is None else str(Path(value).parent)
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) and \
                node.value.attr == 'parents' and isinstance(node.slice, ast.Constant) and \
                isinstance(node.slice.value, int):
            value = recurse(node.value.value)
            parents = Path(value).parents if value is not None else ()
            shape('parents')
            return str(parents[node.slice.value]) if 0 <= node.slice.value < len(parents) else None
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left, right = recurse(node.left), recurse(node.right)
            shape('join-operator')
            return None if left is None or right is None else str(Path(left) / right)
        if not isinstance(node, ast.Call) or node.keywords:
            return None
        function = scope.qualified(node.func)
        if isinstance(node.func, ast.Attribute) and node.func.attr in ('resolve', 'absolute') and not node.args:
            value = recurse(node.func.value)
            if value is None:
                return None
            # The process directory anchors relative paths, exactly as at run time.
            anchored = scope.directory / value
            shape(node.func.attr)
            return str(anchored.resolve() if node.func.attr == 'resolve' else anchored)
        values = [recurse(argument) for argument in node.args]
        if None in values or not values:
            return None
        if function in ('pathlib.Path', 'str', 'os.fspath') and len(values) == 1:
            shape(function)
            return str(Path(values[0])) if function == 'pathlib.Path' else values[0]
        if function in ('os.path.join', 'pathlib.Path'):
            shape(function)
            return _join(values) if function == 'os.path.join' else str(Path(*values))
        if function == 'os.path.dirname' and len(values) == 1:
            shape(function)
            return _dirname(values[0])
        if function in ('os.path.abspath', 'os.path.realpath') and len(values) == 1:
            shape(function)
            anchored = _join([str(scope.directory), values[0]])
            return _normpath(anchored) if function == 'os.path.abspath' else str(Path(anchored).resolve())
        return None

    def imported_constant(self, name: str, scope: Scope, seen: frozenset) -> str | None:
        """Evaluate a constant imported from exactly one in-tree module, in that module."""
        module, _, constant = name.rpartition('.')
        if not module or module.startswith('.'):
            return None
        files = self.module_files(module, self.search_bases(module, scope.search), scope.where)
        if len(files) != 1:
            return None
        self.shape('py:path.imported-constant', scope.where)
        relative = files[0].resolve().relative_to(self.root).as_posix()
        _, _, assignments, qualified = self.python_facts(files[0].read_text())
        values = assignments.get(constant, [])
        if len(values) != 1:
            return None
        return self.literal_path(values[0], replace(scope, assignments=assignments, qualified=qualified,
                                                    where=relative), seen)

    def allowed_import(self, name: str) -> bool:
        """External modules are accepted only by an explicit allowance."""
        return any(name == allowed or name.startswith(allowed + '.')
                   for allowed in self.table.get('python_imports', []))

    def module_index(self) -> dict[str, list[Path]]:
        """Every in-tree directory that holds a module, package or namespace portion of a name."""
        if self.modules is None:
            self.modules = {}
            for base, children, files in self.root.walk():
                children[:] = sorted(c for c in children if c not in ('.git', '__pycache__'))
                names = {f.split('.', 1)[0] for f in files
                         if f.endswith(('.py', '.pyc', '.so', '.pyd', '.pyw'))} | set(children)
                for name in sorted(n for n in names if n.isidentifier()):
                    self.modules.setdefault(name, []).append(base)
        return self.modules

    def module_files(self, name: str, bases: list[Path], where: str) -> list[Path]:
        """Return every in-tree file an import may execute from any search-path portion."""
        files = []
        for base in bases:
            cursor = base
            for part in name.split('.'):
                cursor = cursor / part
                compiled = [p for p in cursor.parent.glob(part + '.*')
                            if p.is_file() and p.suffix in ('.pyc', '.so', '.pyd', '.pyw')]
                if compiled:
                    raise Refusal(f'unreviewable in-tree Python module {compiled[0].name!r} for {name!r} at {where}')
                module = cursor.with_suffix('.py')
                if (cursor / '__init__.py').is_file():
                    files.append(cursor / '__init__.py')
                elif module.is_file():
                    files.append(module)
                    break
                elif not cursor.is_dir():
                    break
                # A namespace portion executes nothing itself but supplies the next part.
        return files

    def python_import(self, name: str, where: str, directory: Path) -> bool:
        """Follow every in-tree portion of an import; no allowance stands in for one."""
        level = len(name) - len(name.lstrip('.'))
        origin = (self.root / where).parent
        dotted = name.lstrip('.')
        if level:
            bases = [origin.parents[level - 2] if level > 1 else origin]
        else:
            # Every in-tree entry the program can place on sys.path is searched.
            bases = self.search_bases(dotted) if self.python_context else [origin]
        files = self.module_files(dotted, bases, where) if dotted else []
        if files or level:
            self.shape('py:import.relative' if level else 'py:import.module', where)
        # Python imports the first portion on its path; with several, which runs is not decided here.
        matched = [base for base in bases if self.module_files(dotted, [base], where)] if dotted else []
        alternatives = len(matched) > 1
        self.inspecting += alternatives
        try:
            for path in files:
                self.script(str(path), where, path.parent, directory, kind='module')
        finally:
            self.inspecting -= alternatives
        if level and dotted and not files:
            raise Refusal(f'unresolved relative Python import {name!r} at {where}')
        return bool(files) or bool(level)

    def check_import_allowances(self) -> None:
        """Table invariant: no external-import allowance names a module the checkout supplies."""
        for name in self.table.get('python_imports', []):
            files = self.module_files(name, self.module_index().get(name.split('.')[0], []), str(TABLE))
            if files:
                raise Refusal(f'external-import allowance {name!r} names in-tree module '
                              f'{files[0].relative_to(self.root).as_posix()!r}')

    def python_calls(self, calls: list[tuple], assignments: dict, where: str) -> None:
        """Classify decoded command and executable-override arguments."""
        for line, argument, working, executable, mode in calls:
            overrides = self.values(executable, assignments, where=f'{where}:{line}') if executable else []
            for value in self.values(argument, assignments, where=f'{where}:{line}'):
                if isinstance(value, str) and mode == 'sh':
                    self.shape('py:exec.shell', f'{where}:{line}')
                    self.shell(value, f'{where}:{line}', working, dialect='sh')
                elif isinstance(value, str) and mode == 'argv':
                    self.shape('py:exec.program', f'{where}:{line}')
                    self.command([value], f'{where}:{line}', working)
                elif mode == 'runtime':
                    self.residue.add(f'{where}:{line}: runtime Python shell selection')
                else:
                    self.shape('py:exec.argv', f'{where}:{line}')
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
