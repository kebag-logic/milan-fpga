#!/usr/bin/env python3
"""Snapshot public finding dispositions and independently recount exclusions."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("repo", type=Path)
args = parser.parse_args()
packet = Path(__file__).resolve().parent

def api(endpoint):
    return json.loads(subprocess.check_output(["gh","api",endpoint,"--paginate"]))

pr = api("repos/kebag-logic/milan-fpga/pulls/684")
assert pr["head"]["sha"] == "708e5634f28e6e5a19236a9b0a9a543c3622e52d"
body = pr["body"]
assert "Milan v1.2 section 5.6.3 (Advertise state machine) and IEEE 1722.1-2021 section 6.2 (ADPDU)" in body
snapshot = {"url":pr["html_url"],"head":pr["head"]["sha"],"body":body}
(packet/"pr-body.json").write_text(json.dumps(snapshot,indent=2)+"\n")
comments = api("repos/kebag-logic/milan-fpga/issues/677/comments")
original = next(x for x in comments if x["id"] == 6024328677)
correction = next(x for x in comments if x["id"] == 6024757146)
assert "15 rows" in original["body"]
assert "14 data rows" in correction["body"] and "five are ADP rows" in correction["body"]
assert original["created_at"] == original["updated_at"]
path = "sw/firmware/gtest/README.md"

def rows(text):
    lines = text.splitlines()
    start = lines.index("| File | Function | Statement | Uncovered | Why no input reaches it |")
    found = []
    for line in lines[start+2:]:
        if not line.startswith("|"):
            break
        found.append(tuple(x.strip() for x in line.strip("|").split("|")[:4]))
    return found

base = rows(subprocess.check_output(["git","-C",str(args.repo),"show","6714181d:"+path]).decode())
head = rows((args.repo/path).read_text())
assert base == head and len(head) == 14
assert sum(row[0] == "`sw/firmware/ctrl/adp/adp.c`" for row in head) == 5
conversation = api("repos/kebag-logic/milan-fpga/issues/684/comments")
reviews = api("repos/kebag-logic/milan-fpga/pulls/684/reviews")
inline = api("repos/kebag-logic/milan-fpga/pulls/684/comments")
index = [{"id":x["id"],"url":x["html_url"],"first_line":x["body"].splitlines()[0]} for x in conversation]
result = {"independent_verdict_sha256":hashlib.sha256((packet/"independent-pass.md").read_bytes()).hexdigest(),
          "pr_head":pr["head"]["sha"], "pr_citation_correct":True,
          "exclusions_base_and_head":14,"adp_exclusions":5,"identities_equal":True,
          "original_comment_preserved":True,
          "correction":{k:correction[k] for k in ("id","html_url","body")},
          "conversation_index":index,"submitted_reviews":len(reviews),"inline_comments":len(inline)}
(packet/"public-disposition.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS public head and corrected clause attribution")
print("PASS 14 unchanged exclusion identities, five ADP rows; original comment preserved; correction present")
print(f"Public index: {len(conversation)} conversation comments; {len(reviews)} submitted reviews; {len(inline)} inline comments")
for x in index:
    if x["first_line"].startswith("[R"):
        print(x["id"],x["first_line"])
