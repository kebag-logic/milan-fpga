#!/usr/bin/env python3
"""R226-2: compare two arm-population files as multisets.

Usage: python3 -B compare_population.py <old.json> <new.json>
Keys: (family, name, page_sha256, expected_kind) for TOC arms, and the full
row tuple for the I440-E label rows. Prints removed/added/retained counts and
lists every added or removed item.
"""
import json
import sys
from collections import Counter

old, new = (json.load(open(p)) for p in sys.argv[1:3])


def key(a):
    return (a["family"], a["name"], a["page_sha256"], a["expected_kind"])


ko, kn = Counter(map(key, old["arms"])), Counter(map(key, new["arms"]))
removed, added = ko - kn, kn - ko
print(f"TOC arms: old {sum(ko.values())}, new {sum(kn.values())}, "
      f"retained {sum((ko & kn).values())}, removed {sum(removed.values())}, "
      f"added {sum(added.values())}")
print(f"duplicate keys: old {sum(v - 1 for v in ko.values() if v > 1)}, "
      f"new {sum(v - 1 for v in kn.values() if v > 1)}")
for k in sorted(removed):
    print("  REMOVED", k)
for k in sorted(added):
    page = next(a["page"] for a in new["arms"] if key(a) == k)
    print("  ADDED  ", k[0], repr(k[1]), "expects", k[3], "page", repr(page))
lo = Counter(tuple(r) for r in old["label_rows"])
ln = Counter(tuple(r) for r in new["label_rows"])
print(f"I440-E label rows: old {sum(lo.values())}, new {sum(ln.values())}, "
      f"retained {sum((lo & ln).values())}, removed {sum((lo - ln).values())}, "
      f"added {sum((ln - lo).values())}")
for r in sorted(lo - ln):
    print("  REMOVED", r)
for r in sorted(ln - lo):
    print("  ADDED  ", r)
# order: old rows keep their relative order in the new list
new_rows = [tuple(r) for r in new["label_rows"]]
old_rows = [tuple(r) for r in old["label_rows"]]
print("old label rows keep relative order:",
      [r for r in new_rows if r in set(old_rows)] == old_rows)
new_names = [a["name"] for a in new["arms"]]
old_names = [a["name"] for a in old["arms"]]
print("old TOC arms keep relative order:",
      [n for n in new_names if n in set(old_names)] == old_names)
print("MIN_ARMS:", old["MIN_ARMS"], "->", new["MIN_ARMS"],
      "| RAW_HTML_TAGS:", old["RAW_HTML_TAGS"], "->", new["RAW_HTML_TAGS"],
      "| ARM_FAMILIES equal:", old["ARM_FAMILIES"] == new["ARM_FAMILIES"])
