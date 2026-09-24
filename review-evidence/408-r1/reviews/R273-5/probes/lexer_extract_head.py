#!/usr/bin/env python3
"""Load gate 1b's own translation-phase and directive-reader code out of a
checkout's sw/builder/test_builder.py, unmodified, so a probe can ask it
what it reads and compare that with the pinned compiler.

Head layout (8e12d31f and later): the phases are module-level
(`_c_phases()` and its helpers, the generated corpus), and the readers are
nested in test_baremetal_profile_contract(). Both are picked by name out of
the AST and executed in one namespace; nothing is patched.

usage as a module: `load(repo_root)` -> (namespace, missing names)
"""
import ast
import os
from pathlib import Path
import re
import tempfile
import typing

MODULE_PREFIXES = ("_C_", "_c_", "_CPhases", "_LEXER_", "_lexer_")
NESTED = {
    "c_line", "blanked", "cpp_hash", "cpp_directive_re", "cpp_arms",
    "error_line_re", "conditional_groups", "blank_spans", "holds_error",
    "is_guard", "keyed_condition_re", "directive_re", "include_operand_re",
    "macro_definition_re", "macro_definitions", "lexer_corpus",
    "lexer_conditions", "lexer_keeps", "lexer_pastes", "lexer_readers",
    "firmware_includes", "firmware_directives", "MAX_ARM_SELECTIONS",
    "firmware_includes_third_party", "firmware_includes_own",
    "firmware_includes_generated",
}


def _name(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return node.name
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
            isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def load(root):
    path = Path(root) / "sw/builder/test_builder.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    top = [n for n in tree.body
           if (_name(n) or "").startswith(MODULE_PREFIXES)]
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "test_baremetal_profile_contract")
    nested = [n for n in func.body if _name(n) in NESTED]
    module = ast.Module(body=top + nested, type_ignores=[])
    ns = {"re": re, "Any": typing.Any, "Callable": typing.Callable,
          "NamedTuple": typing.NamedTuple, "Path": Path, "os": os,
          "tempfile": tempfile, "__name__": "r273_lexer_extract"}
    exec(compile(module, str(path), "exec"), ns)
    missing = {n for n in NESTED if n not in ns}
    return ns, missing
