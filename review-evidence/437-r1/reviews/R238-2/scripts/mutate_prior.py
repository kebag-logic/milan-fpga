#!/usr/bin/env python3
"""Mutations that restore the root cause of each prior public finding, scored
by both shipped self-tests (same harness as mutate.py).
Usage: mutate_prior.py <head-root> <scratch-dir> <out.json> [jobs]"""
import concurrent.futures
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate  # noqa: E402

MUTATIONS = [
    ("P01 fence content opens containers (R237-r1 F3, fenced marker)", "gen_toc_containers.py",
     "if not closed and state in (FENCE, COMMENT, HTML):", "if not closed and state in (COMMENT, HTML):"),
    ("P02 comment content opens containers (R237-r1 F3, commented marker)", "gen_toc_containers.py",
     "if not closed and state in (FENCE, COMMENT, HTML):", "if not closed and state in (FENCE, HTML):"),
    ("P03 raw HTML content opens containers (R237-r1 F3, HTML marker)", "gen_toc_containers.py",
     "if not closed and state in (FENCE, COMMENT, HTML):", "if not closed and state in (FENCE, COMMENT):"),
    ("P04 a dedented quote is lazy (R238-r1 F2)", "gen_toc_containers.py",
     "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,", "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE,"),
    ("P05 a tag in any item continues a paragraph (R237-2 F1 root 1)", "gen_toc_containers.py",
     "return _scope(walk, para, (plain, plain and para == PARAGRAPH), rem, label)",
     "return _scope(walk, PARAGRAPH if walk.stack else para, (plain, plain and para == PARAGRAPH), rem, label)"),
    ("P06 the column-0 gate returns (R237-r1 F1, R238-r1 F1)", "gen_toc.py",
     "label, state, delim, tag = _opens(line, para, state, scope.gate)",
     "label, state, delim, tag = _opens(line, para, state)"),
    ("P07 in-item block outlives the item (R237-2 F1 root 2, R238-r1 F3)", "gen_toc.py",
     "owner not in scope.held_by or (prose and not scope.plain)):", "(prose and not scope.plain)):"),
    ("P08 every opener in raw HTML opens (R237-2 F2)", "gen_toc_html.py",
     "        mark = HTML_MARKUP_RE.search(raw, at)\n        if not mark:\n            return False\n",
     "        mark = re.compile(r\"(?P<comment><!--)\").search(raw, at)\n        if not mark:\n            return False\n"),
    ("P09 empty item holds a blank line (R237-2 F3 property)", "gen_toc_containers.py",
     "return len(text) if box.filled and _blank(rest) else None", "return len(text) if _blank(rest) else None"),
    ("P10 four-column opener in an item read as code (R237-2 S1)", "gen_toc_html.py",
     "        if scope.raw is not None:\n            raw.append(scope.raw)\n",
     "        if scope.raw is not None and not scope.raw.startswith('  '):\n            raw.append(scope.raw)\n"),
]
mutate.MUTATIONS = MUTATIONS
sys.argv = [sys.argv[0]] + sys.argv[1:]
mutate.main()
