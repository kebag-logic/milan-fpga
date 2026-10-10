"""Compare two firmware gate logs (test_ctrl_firmware.py --self-test) verdict by verdict.
Every "[ok]"/"[ESCAPED]"/"[FAIL]"-style line is keyed on the plant name (text before the first ':');
the verdict word and the named test must match. Usage: python3 -I compare_verdicts.py DEV_LOG HEAD_LOG"""
import re
import sys

LINE = re.compile(r"^\s*\[(?P<v>[A-Za-z ]+)\]\s+(?P<rest>.*)$")


def verdicts(path):
    rows = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        m = LINE.match(line.rstrip("\n"))
        if not m:
            continue
        key = m["rest"].split(":", 1)[0]
        rows.setdefault(key, []).append((m["v"], m["rest"]))
    return rows


a, b = verdicts(sys.argv[1]), verdicts(sys.argv[2])
na, nb = sum(map(len, a.values())), sum(map(len, b.values()))
print(f"verdict lines: dev {na}, head {nb}")
for name, rows in (("dev", a), ("head", b)):
    words = {}
    for rs in rows.values():
        for v, _ in rs:
            words[v] = words.get(v, 0) + 1
    print(f"  {name} verdict words: {words}")
only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
print(f"only at dev: {len(only_a)}", *only_a, sep="\n  ")
print(f"only at head: {len(only_b)}", *only_b, sep="\n  ")
diff_v, diff_text = [], []
for k in sorted(set(a) & set(b)):
    if [v for v, _ in a[k]] != [v for v, _ in b[k]]:
        diff_v.append(k)
    elif [t for _, t in a[k]] != [t for _, t in b[k]]:
        diff_text.append((k, a[k], b[k]))
print(f"verdict word differs: {len(diff_v)}", *diff_v, sep="\n  ")
print(f"same verdict, different text: {len(diff_text)}")
for k, x, y in diff_text:
    print(f"  {k}\n    dev : {x}\n    head: {y}")
sys.exit(1 if diff_v or only_a or only_b else 0)
