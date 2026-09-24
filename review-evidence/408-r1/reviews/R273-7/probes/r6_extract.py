#!/usr/bin/env python3
"""Load gate 1b's lexical subset S (with its round-four character allowlist),
its closure table and its directive/name readers out of a checkout's
sw/builder/test_builder.py, unmodified (R273-6). Extends the R273-5
extractor (subset_extract) with the round-four names; nothing is patched.

usage as a module: `load(repo_root)` -> (namespace, missing names)
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexer_extract_head as base  # noqa: E402
import subset_extract  # noqa: E402

ROUND_FOUR = {"c_identifier_re", "c_splice_re", "lexer_names",
              "assert_character_closure"}


def load(root):
    saved_prefixes = base.MODULE_PREFIXES
    saved = set(subset_extract.EXTRA)
    base.MODULE_PREFIXES = saved_prefixes + ("_CLOSURE", "_closure")
    subset_extract.EXTRA |= ROUND_FOUR
    try:
        ns, missing = subset_extract.load(root)
    finally:
        base.MODULE_PREFIXES = saved_prefixes
        subset_extract.EXTRA.clear()
        subset_extract.EXTRA |= saved
    # the gate's own registration, `lexer_readers["names"] = lexer_names`
    if "lexer_readers" in ns and "lexer_names" in ns:
        ns["lexer_readers"]["names"] = ns["lexer_names"]
    return ns, missing
