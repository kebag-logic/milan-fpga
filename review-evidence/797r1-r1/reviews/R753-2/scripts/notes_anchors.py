#!/usr/bin/env python3
"""Check the page's links into the design notes and count one-column Note tables.
Usage: notes_anchors.py <page> <notes>"""
import re, sys
page = open(sys.argv[1], encoding="utf-8").read()
notes = open(sys.argv[2], encoding="utf-8").read()
links = set(re.findall(r"CSR_REGISTER_NOTES\.md#([^)\s]+)\)", page))
def anchor(h):
    h = re.sub(r"[`*]", "", h).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h, flags=re.U)
    return h.replace(" ", "-")
heads = {anchor(m) for m in re.findall(r"^#{1,6} (.*)$", notes, re.M)}
miss = [l for l in links if l not in heads]
print("links", len(links), "heads", len(heads), "unresolved", len(miss))
for m in miss[:10]:
    print(" ", m)
print("Note tables on page:", len(re.findall(r"^\| Note \|", page, re.M)))
