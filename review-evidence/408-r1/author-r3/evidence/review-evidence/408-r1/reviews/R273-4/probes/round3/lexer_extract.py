#!/usr/bin/env python3
"""Load gate 1b's own nested lexer/reader functions out of a checkout's
sw/builder/test_builder.py, unmodified, so a probe can ask them what they
read and compare that with the pinned compiler.

Usage as a module: `load(repo_root)` returns a namespace dict holding
c_lexed, blanked, spliced, conditional_groups, lexer_keeps, macro_definitions,
lexer_corpus, cpp_hash, directive_re, arm_selections-free helpers.
"""
import ast
from pathlib import Path
import re
import typing

WANTED = {
    "c_splice_re", "c_split_name_re", "c_lex_stop_re", "c_line_end_re",
    "c_line", "c_raw_prefixes", "c_logical", "c_before", "c_spliced_end",
    "c_comment_end", "c_literal_end", "c_raw_prefixed", "c_raw_end",
    "c_lexed", "blanked", "cpp_hash", "cpp_directive_re", "error_line_re",
    "conditional_groups", "blank_spans", "keyed_condition_re",
    "directive_re", "include_operand_re", "line_spliced", "spliced",
    "closed_splices", "macro_definition_re", "macro_definitions",
    "lexer_corpus", "lexer_conditions", "lexer_keeps", "firmware_includes",
    "firmware_directives", "MAX_ARM_SELECTIONS", "firmware_includes_third_party", "firmware_includes_own", "firmware_includes_generated",
}


def _name(node):
    if isinstance(node, ast.FunctionDef):
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
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "test_baremetal_profile_contract")
    picked = [n for n in func.body if _name(n) in WANTED]
    module = ast.Module(body=picked, type_ignores=[])
    ns = {"re": re, "Any": typing.Any, "Callable": typing.Callable,
          "Path": Path}
    exec(compile(module, str(path), "exec"), ns)
    missing = WANTED - set(ns)
    return ns, missing
