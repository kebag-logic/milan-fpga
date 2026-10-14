#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Refuse syntax outside the reviewed node, operator and exact-use census."""

import ast
import builtins
import hashlib
import json
import re

from ci_command_table import Refusal


SENSITIVE = {'PATH', 'IFS', 'BASH_ENV', 'ENV', 'SHELL', 'MAKEFLAGS', 'MAKE', '.SHELLFLAGS'}


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
