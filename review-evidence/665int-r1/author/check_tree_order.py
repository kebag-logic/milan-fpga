"""The two files compare_same.py left DIFFERENT differ only in the order of LiteX's comment-only hierarchy tree.

Usage: check_tree_order.py <base-file> <head-file>
Prints the line counts and exits 0 when: every line that is neither a date line
nor a hierarchy-tree line is identical and in the same order, and the tree lines
are the same multiset once the last-child glyph is folded into the sibling glyph
(the order of two siblings moves which of them is drawn last).
"""
import collections
import re
import sys
from pathlib import Path

STAMP = re.compile(rb"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}")
BOX = ("│", "├", "└")


def split(path: Path):
    """The body lines in order, and the folded tree lines as a multiset."""
    body, tree = [], collections.Counter()
    for ln in path.read_bytes().split(b"\n"):
        if STAMP.search(ln):
            continue
        text = ln.decode("utf-8", errors="replace")
        if text.lstrip().lstrip("/ ").startswith(BOX) or text.lstrip().startswith(BOX):
            tree[text.replace("└", "├")] += 1
            continue
        body.append(ln)
    return body, tree


(bb, bt), (hb, ht) = split(Path(sys.argv[1])), split(Path(sys.argv[2]))
print(f"body lines {len(bb)} / {len(hb)} identical={bb == hb}; tree lines {sum(bt.values())} / {sum(ht.values())} same-multiset={bt == ht}")
sys.exit(0 if bb == hb and bt == ht else 1)
