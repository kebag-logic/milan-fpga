#!/usr/bin/env python3
"""Load gate 1b's lexer, subset check S and directive readers out of a
checkout's sw/builder/test_builder.py, unmodified, into one namespace (the
reviewers' round-three extractor, extended with the round-four names).

Module-level: `_c_phases()` and its helpers, the corpora, the allowlist
(`_S_*`) and the closure table (`_CLOSURE_*`, `_closure_corpus()`).
Nested in test_baremetal_profile_contract(): picked by name, in AST order.

usage as a module: `load(repo_root, source=None)` -> (namespace, missing).
`source` replaces the file text (a disconnect patch applied in memory).
"""
import ast
import os
from pathlib import Path
import re
import tempfile
import typing

MODULE_PREFIXES = ("_C_", "_c_", "_CPhases", "_LEXER_", "_lexer_", "_S_",
                   "_CLOSURE_", "_closure_")
NESTED = {
    "c_line", "blanked", "cpp_hash", "cpp_directive_re", "cpp_arms",
    "c_splice_re", "c_line_end_re", "c_identifier_re",
    "error_line_re", "conditional_groups", "blank_spans", "holds_error",
    "is_guard", "keyed_condition_re", "directive_re", "include_operand_re",
    "macro_definition_re", "macro_definitions", "lexer_corpus",
    "lexer_conditions", "lexer_keeps", "lexer_pastes", "lexer_names",
    "lexer_readers", "MAX_ARM_SELECTIONS",
    "assert_lexes_as_compiled", "assert_spelled_without_digraphs",
    "include_directive_re",
    "assert_within_lexical_subset", "subset_refusal_corpus",
    "assert_subset_refuses",
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


def load(root, source=None):
    path = Path(root) / "sw/builder/test_builder.py"
    text = path.read_text(encoding="utf-8") if source is None else source
    tree = ast.parse(text)
    top = [n for n in tree.body
           if (_name(n) or "").startswith(MODULE_PREFIXES)]
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "test_baremetal_profile_contract")
    wanted = set(NESTED) | {_name(n) for n in func.body
                            if (_name(n) or "").endswith("_PIN")}
    nested = [n for n in func.body if _name(n) in wanted]
    module = ast.Module(body=top + nested, type_ignores=[])
    ns = {"re": re, "Any": typing.Any, "Callable": typing.Callable,
          "NamedTuple": typing.NamedTuple, "Path": Path, "os": os,
          "tempfile": tempfile, "__name__": "a254_gate_extract"}
    exec(compile(module, str(path), "exec"), ns)
    # the gate registers its closure identifier reader in a statement of its
    # own, after the `lexer_readers` literal, so this loader does the same
    if "lexer_names" in ns:
        ns["lexer_readers"].setdefault("names", ns["lexer_names"])
    missing = {n for n in wanted if n not in ns}
    return ns, missing
