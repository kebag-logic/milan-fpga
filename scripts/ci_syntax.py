#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Refuse syntax outside the reviewed node, operator and exact-use census."""

import ast
import builtins
import hashlib
import json
import re

from ci_command_table import Refusal, Runtime, nodes


SENSITIVE = {
    'PATH', 'IFS', 'CDPATH', 'BASH_ENV', 'ENV', 'BASHOPTS', 'SHELLOPTS', 'BASH_CMDS',
    'PYTHONPATH', 'PYTHONHOME', 'LD_PRELOAD', 'LD_LIBRARY_PATH',
    'SHELL', 'MAKEFLAGS', 'GNUMAKEFLAGS', 'MAKEFILES', 'MAKEOVERRIDES', 'MAKE',
    '.SHELLFLAGS', '.RECIPEPREFIX',
}

#: Variables that make an interpreter or loader run code it was not given: refused by name in a
#: workflow `env:`, before the allowlist below is consulted.
HOOKS = {
    'PERL5OPT', 'PERL5LIB', 'PERLLIB', 'NODE_OPTIONS', 'NODE_PATH', 'GIT_EXEC_PATH', 'GIT_CONFIG',
    'GIT_CONFIG_COUNT', 'GIT_CONFIG_GLOBAL', 'GIT_CONFIG_SYSTEM', 'GIT_CONFIG_PARAMETERS', 'GIT_SSH',
    'GIT_SSH_COMMAND', 'GIT_ASKPASS', 'GIT_EDITOR', 'GIT_PAGER', 'GIT_EXTERNAL_DIFF', 'PYTHONUSERBASE',
    'PYTHONSTARTUP', 'PYTHONINSPECT', 'PYTHONSAFEPATH', 'PYTHONNOUSERSITE', 'PYTHONEXECUTABLE',
    'PYTHONPLATLIBDIR', 'PYTHONWARNINGS', 'PYTHONBREAKPOINT', 'LD_AUDIT', 'LD_LIBRARY_PATH', 'LD_PRELOAD',
    'HOME', 'XDG_CONFIG_HOME', 'TMPDIR', 'SHELL', 'POSIXLY_CORRECT', 'PROMPT_COMMAND', 'PS4', 'GLOBIGNORE',
    'BASH_XTRACEFD', 'BASH_LOADABLES_PATH', 'BASH_COMPAT', 'INPUTRC', 'MAKELEVEL', 'GCC_EXEC_PREFIX',
    'COMPILER_PATH', 'LIBRARY_PATH', 'CPATH', 'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'CC', 'CXX', 'CFLAGS',
    'CXXFLAGS', 'LDFLAGS', 'CPPFLAGS', 'VERILATOR_ROOT', 'JAVA_TOOL_OPTIONS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS',
}


def workflow_environment(census: dict, env: dict, where: str) -> None:
    """A workflow `env:` name is accepted only if the walker models it: the census's reviewed names.

    Exported shell functions (`BASH_FUNC_*`) and interpreter, loader and tool hooks
    are refused by name; any other name outside the allowlist is refused as unmodelled.
    """
    for name in sorted(env):
        if name.startswith('BASH_FUNC_'):
            raise Refusal(f'exported shell function in workflow environment {name!r} at {where}')
        if name in SENSITIVE or name in HOOKS or name.startswith(('GIT_CONFIG_', 'LD_')):
            raise Refusal(f'interpreter hook in workflow environment {name!r} at {where}')
        if name not in census.get('workflow_environment', {}):
            raise Refusal(f'unmodelled workflow environment name {name!r} at {where}')


#: Arithmetic operators that assign: `=`, `++` and `--`.
ARITHMETIC_ASSIGNMENTS = (74, 36, 37)


def semantic_node(value: object) -> object:
    """Keep semantic fields while removing parser locations and comments."""
    if isinstance(value, list):
        return [semantic_node(child) for child in value]
    if isinstance(value, dict):
        return {key: semantic_node(child) for key, child in value.items()
                if key not in ('Pos', 'End', 'Comments') and not (
                    isinstance(child, dict) and set(child) <= {'Offset', 'Line', 'Col'})}
    return value


def exact_use(audit: object, node: dict, where: str, kind: str) -> None:
    """Require an exact semantic node at its reviewed source, never a substring."""
    raw = json.dumps(semantic_node(node), sort_keys=True, separators=(',', ':')).encode()
    entry = audit.census['shell_exact_uses'].get(hashlib.sha256(raw).hexdigest(), {})
    if where.split(':')[0] not in entry.get('sources', []) or kind not in entry.get('kinds', []):
        raise Refusal(f'uncensused shell {kind} at {where}')


def shell_nodes(audit: object, value: object, where: str, context: str = 'File',
                conditional: bool = False) -> None:
    """Validate every parsed node, including fields the semantic walker ignores."""
    if isinstance(value, list):
        for child in value:
            shell_nodes(audit, child, where, context, conditional)
        return
    if not isinstance(value, dict) or set(value) <= {'Offset', 'Line', 'Col'}:
        return
    kind = value.get('Type', context)
    fields = audit.census['shell_fields'].get(kind)
    if fields is None:
        raise Refusal(f'uncensused shell node {kind!r} at {where}')
    for key, child in value.items():
        if key not in fields:
            raise Refusal(f'uncensused shell {kind}.{key} at {where}')
        if key == 'Op' and child not in audit.census['shell_operators'].get(kind + '.Op', []):
            raise Refusal(f'uncensused shell operator {kind}.{child} at {where}')
        if isinstance(child, bool) and child not in audit.census['shell_flags'].get(kind + '.' + key, []):
            raise Refusal(f'uncensused shell flag {kind}.{key} at {where}')
    if kind == 'FuncDecl' and conditional:
        exact_use(audit, value, where, 'conditional-function')
    if kind == 'ParamExp':
        name = value['Param']['Value']
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name) and name not in audit.census['shell_special']:
            raise Refusal(f'uncensused shell special variable {name!r} at {where}')
    for key, child in value.items():
        if key not in ('Pos', 'End', 'Comments'):
            shell_nodes(audit, child, where, key, conditional or kind in (
                'IfClause', 'CaseClause', 'ForClause', 'WhileClause'))


def python_nodes(audit: object, tree: ast.AST, where: str) -> None:
    """Operators and expression nodes have the same closed boundary as statements."""
    for node in ast.walk(tree):
        if type(node).__name__ not in audit.census['python_nodes']:
            raise Refusal(f'uncensused Python node {type(node).__name__!r} at {where}')

        if isinstance(node, ast.Name):
            if node.id in vars(builtins) and node.id not in audit.census['python_builtins']:
                raise Refusal(f'uncensused Python builtin {node.id!r} at {where}')
            if node.id.startswith('__') and node.id not in audit.census['python_special_names']:
                raise Refusal(f'uncensused Python special name {node.id!r} at {where}')


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


def posix_dirname(value: str) -> str:
    """The image's coreutils dirname of one operand; its self-test holds the reference outputs."""
    stripped = value.rstrip('/')
    if not value or '/' not in stripped:
        return '/' if value and not stripped else '.'
    return stripped.rpartition('/')[0].rstrip('/') or '/'


def errexit_option(args: list[str]) -> bool | None:
    """The errexit setting `set` leaves, read as the shell reads its options; None when it names none.

    A runtime operand may set anything, so errexit is then not known to hold.
    """
    result, words = None, iter(args[1:])
    for word in words:
        if isinstance(word, Runtime):
            return False
        if word == '--' or word[:1] not in ('-', '+') or len(word) < 2:
            break
        for letter in word[1:]:
            option = 'errexit' if letter == 'e' else next(words, None) if letter == 'o' else None
            if isinstance(option, Runtime):
                return False
            if option == 'errexit':
                result = word[0] == '-'
    return result


def top_substitutions(word: dict | None) -> list[dict]:
    """The command substitutions a word performs itself, not those nested inside them."""
    found, pending = [], list((word or {}).get('Parts', []))
    while pending:
        part = pending.pop()
        if part.get('Type') == 'CmdSubst':
            found.append(part)
        elif part.get('Type') == 'DblQuoted':
            pending.extend(part.get('Parts', []))
        elif part.get('Type') in ('ParamExp', 'ArithmExp', 'ProcSubst'):
            found.extend(n for n in nodes(part) if n.get('Type') == 'CmdSubst')
    return found


def glob_pattern(text: str) -> bool:
    """Whether unquoted text is a pathname pattern: `*`, `?` or a closed bracket expression."""
    return bool(re.search(r'[*?]|\[[^]]*\]', text))
