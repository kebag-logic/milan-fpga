"""Probe P3: rebuild each reviewed inline variant from its tracked script and exact diff, and compare
the digest with the entry's key. Usage: python3 -I p3_variants.py <checkout>"""
import hashlib, json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
d = json.loads((root / "ci/image/exec-audit.json").read_text())
ok = bad = 0
for key, entry in d["inline_programs"].items():
    if "diff" not in entry:
        continue
    lines = (root / entry["variant_of"]).read_text().split("\n")
    out, pos = [], 0
    for hunk in re.split(r"(?m)^(?=@@ )", entry["diff"])[1:]:
        head, *body = hunk.split("\n")
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", head)
        start = int(m.group(1)) - (0 if m.group(2) == "0" else 1)
        out += lines[pos:start]; pos = start
        for b in body:
            if b.startswith("-"): pos += 1
            elif b.startswith("+"): out.append(b[1:])
            elif b.startswith(" "): out.append(lines[pos]); pos += 1
    out += lines[pos:]
    text = "\n".join(out)
    good = hashlib.sha256(text.encode()).hexdigest() == key
    ok += good; bad += not good
    if not good: print("MISMATCH", key, entry["variant_of"])
print(f"variants rebuilt: {ok} match, {bad} differ")
