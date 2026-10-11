#!/usr/bin/env python3
"""Check moved C tokens, first-party delta, inventories, and ratchet migration."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
a = ap.parse_args()
root = a.checkout.resolve()
base = "8b61b70902f3ebf118e56967277e2686731081bd"
merged = "aef7ac666"
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build
import ctrl_mutants
import ctrl_plants

def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])

# C preprocessing-token comparison keeps string/character literals intact.
lexer = re.compile(r'''(?P<skip>\s+|//[^\n]*|/\*[\s\S]*?\*/)|(?:u8|[uUL])?"(?:\\.|[^"\\])*"|(?:[uUL])?'(?:\\.|[^'\\])*'|[A-Za-z_]\w*|\d[\w.]*|>>=|<<=|\.\.\.|->|\+\+|--|&&|\|\||<=|>=|==|!=|<<|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|##|[^\s]''')
def tokens(data):
    text = data.decode().replace("\\\n", "")
    return [m.group() for m in lexer.finditer(text) if not m.group("skip")]

for new, old in ctrl_build.LEGACY.items():
    left = git("show", base + ":sw/firmware/ctrl/" + old)
    right = (root / "third_party/tsn-c-stack" / new).read_bytes()
    assert tokens(left) == tokens(right), (old, new)
    print(json.dumps({"old": old, "new": new, "tokens_equal": True,
                      "tokens": len(tokens(left)),
                      "token_sha256": hashlib.sha256(json.dumps(tokens(left)).encode()).hexdigest()}))
paths = git("diff", "--name-only", merged + "..HEAD").decode().splitlines()
production = [p for p in paths if p.startswith("sw/firmware/") and p.endswith((".c", ".h")) and
              "/test/" not in p and "/gtest/" not in p and (root/p).exists()]
print("Surviving first-party production C/H changes after inherited dev merge:", production)
assert production == ["sw/firmware/ctrl/mbx/mbx_wire.h"]
assert tokens(git("show", merged + ":" + production[0])) == tokens((root/production[0]).read_bytes())
print("Surviving production change is token-identical")
rtl = [p for p in paths if p.endswith((".sv", ".v")) or p in ("protocol-processor", "gptp-processor")]
assert not rtl
print("RTL and processor pin changes:", rtl)
for path in ("third_party/lwSRP", "protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    assert git("rev-parse", base + ":" + path) == git("rev-parse", "HEAD:" + path)
    print("unchanged gitlink:", path, git("rev-parse", "HEAD:" + path).decode().strip())
print("parent control mutants:", len(ctrl_mutants.MUTANTS))
print("boundary controls:", len(ctrl_plants.PLANTS),
      "defects:", sum(bool(p.needle) for p in ctrl_plants.PLANTS),
      "passing:", sum(not p.needle for p in ctrl_plants.PLANTS), "+ shared baseline")
ratchet = "sw/firmware/gtest/coverage.ratchet"
def rows(text):
    result = {}
    for line in text.splitlines():
        m = re.match(r"(\S+)  lines (\d+)/(\d+)  branches (\d+)/(\d+)", line)
        if m:
            name = m[1]
            for new, old in ctrl_build.LEGACY.items():
                if name == "sw/firmware/ctrl/" + old:
                    name = "third_party/tsn-c-stack/" + new
            result[name] = tuple(map(int, m.groups()[1:]))
    return result
old = rows(git("show", merged + ":" + ratchet).decode())
new = rows((root/ratchet).read_text())
for path in sorted(old.keys() | new.keys()):
    if old.get(path) != new.get(path):
        print("ratchet delta:", path, old.get(path), "->", new.get(path))
print("structural checks: PASS")
