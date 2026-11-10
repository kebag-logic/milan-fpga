"""measured_diff.py OLD NEW: every leaf of two srptx reports' measured blocks that differs, by path. A receipt
header (lines before the first "{") is skipped."""
import json
import sys


def read(path):
    text = open(path).read()
    return json.loads(text[text.index("{"):])


def leaves(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, f"{path}/{k}")
    elif isinstance(x, list):
        for k, v in enumerate(x):
            yield from leaves(v, f"{path}[{k}]")
    else:
        yield path, x


old, new = read(sys.argv[1]), read(sys.argv[2])
a, b = dict(leaves(old.get("measured", old))), dict(leaves(new.get("measured", new)))
diff = [(k, a.get(k, "<absent>"), b.get(k, "<absent>")) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
print(f"{len(diff)} measured leaves differ; findings old {len(old.get('findings', []))} new {len(new.get('findings', []))}")
for k, x, y in diff:
    print(f"  {k}: {x} -> {y}")
