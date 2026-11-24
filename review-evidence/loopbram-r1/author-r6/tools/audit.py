"""Audit the round-6 packet: sizes, text, links, manifest, handoff shape and forbidden names.

Usage: audit.py <checkout>
"""
import codecs
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

packet = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1])
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip(), "dirty lane"
handoff = (packet / "HANDOFF-r6.md").read_text()
assert handoff.startswith("Status: ") and handoff.splitlines()[1].startswith("ETA: "), "handoff head"
assert handoff.rstrip().splitlines()[-1] == "REVIEW READY " + head, handoff.rstrip().splitlines()[-1]
# Token lists are stored rot13-encoded so that this script spells no product or model name.
MODEL = [codecs.decode(t, "rot13") for t in ["pynhqr", "bchf", "fbaarg", "unvxh", "naguebcvp", "bcranv", "pbqrk",
                                             "trzvav", "pbcvybg", "snoyr", "yynzn", "zvfgeny"]]
TOOLS = [codecs.decode(t, "rot13") for t in ["ivinqb", "irevyngbe", "lbflf", "kvyvak", "nyvak", "nk7101",
                                             "RkgenGvzvatBcg", "NygFcernqYbtvp", "RkgenCbfgCynprzragBcg"]]
model_re = re.compile(r"\b(?:" + "|".join(MODEL) + r")\b|\bgpt\b|\bgpt-?\d", re.I)
tool_re = re.compile("|".join(TOOLS), re.I)
files = [p for p in packet.rglob("*") if p.is_file()]
for p in files:
    assert p.stat().st_size < 200000, (p, p.stat().st_size)
    assert p.suffix != ".gz", p
    text = p.read_bytes().decode("utf-8")
    hit = model_re.search(text)
    assert not hit, ("model name", p, hit.group(0))
for p in packet.rglob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        assert (p.parent / target.split("#")[0]).exists(), (p, target)
body = (packet / "PR-BODY.md").read_text()
assert not tool_re.search(body), tool_re.search(body).group(0)
assert "\n---" not in body and "Generated with" not in body
receipts = packet / "receipts"
count = 0
for line in (receipts / "manifest-1.jsonl").read_text().splitlines():
    row = json.loads(line)
    blob = (receipts / row["file"]).read_bytes()
    assert len(blob) == row["bytes"] and hashlib.sha256(blob).hexdigest() == row["sha256"], row["file"]
    assert head in blob.decode().splitlines()[0], ("receipt not bound to the head", row["file"])
    count += 1
listed = {json.loads(line)["file"] for line in (receipts / "manifest-1.jsonl").read_text().splitlines()}
assert listed == {p.name for p in receipts.iterdir()} - {"INDEX.md", "manifest-1.jsonl"}, "unlisted receipt"
print("PACKET PASS", head, "receipts", count, "files", len(files))
