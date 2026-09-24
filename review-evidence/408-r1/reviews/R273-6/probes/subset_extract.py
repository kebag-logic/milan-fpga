#!/usr/bin/env python3
"""Load gate 1b's lexical-subset check S and its directive readers out of a
checkout's sw/builder/test_builder.py, unmodified (R273-5). Extends the
round-four extractor with the S functions and every *_PIN constant."""
import ast
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexer_extract_head as base  # noqa: E402

EXTRA = {"c_line_end_re", "assert_lexes_as_compiled", "assert_spelled_without_digraphs",
         "include_directive_re", "assert_within_lexical_subset",
         "subset_refusal_corpus", "assert_subset_refuses"}


def load(root):
    path = Path(root) / "sw/builder/test_builder.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "test_baremetal_profile_contract")
    pins = {base._name(n) for n in func.body
            if (base._name(n) or "").endswith("_PIN")}
    saved = set(base.NESTED)
    base.NESTED |= EXTRA | pins
    try:
        ns, missing = base.load(root)
    finally:
        base.NESTED.clear()
        base.NESTED |= saved
    return ns, missing
