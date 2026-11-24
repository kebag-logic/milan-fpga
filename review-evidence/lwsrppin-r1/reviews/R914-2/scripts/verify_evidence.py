"""Verify published evidence bytes and mechanically recount the reviewed receipts.

Usage: python3 -I -B scripts/verify_evidence.py <candidate-root> <extracted-packet>
The packet must be from a2a3c4d0cc3dc2b27aa74f1dddcaa3fe428742c4.
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, evidence = map(Path, sys.argv[1:])
head = "ed7df79c6f87a4172c885f268ad67629bd56c4eb"
base = "dbba60e68a6e4a46f80e381c30ff823ee4ff7484"
packet = "a2a3c4d0cc3dc2b27aa74f1dddcaa3fe428742c4"

def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])

manifest = json.loads((evidence / "MANIFEST.json").read_text())
checked = 0
for item in manifest:
    if not item["file"].startswith(("author/", "author-r2/", "author-route/")):
        continue
    digest = hashlib.sha256((evidence / item["file"]).read_bytes()).hexdigest()
    assert digest == item["published_sha256"], item["file"]
    checked += 1
print(f"Published author receipt manifest: {checked} entries verified, 0 mismatches")
print("Packet commit:", packet)
print("Packet tree:", git("rev-parse", packet + "^{tree}").decode().strip())
print("Commit signature present:", b"\ngpgsig " in git("cat-file", "commit", packet))
print("Verification establishes pinned content integrity; no cryptographic signer claim.")

names = git("diff", "--name-only", base, head).decode().splitlines()
assert set(names) == {"tb/verilator/milan_dp/twin_mrp.py", "tb/verilator/milan_dp/README.md",
                      "sw/firmware/ctrl/test/test_ctrl_firmware.py"}
print("Delta commits:", len(git("rev-list", base + ".." + head).splitlines()))
print("Delta paths:", ", ".join(names))
for path in (names[0], "tb/verilator/milan_dp/twin_mrp.py"):
    old = ast.parse(git("show", base + ":" + path))
    new = ast.parse((root / path).read_bytes())
    if path.endswith("test_ctrl_firmware.py"):
        old.body.pop(0)
        new.body.pop(0)
        assert ast.dump(old) == ast.dump(new)
        print(path + ": identical executable AST after module docstring removal")
    else:
        old_defs = {n.name: ast.dump(n) for n in old.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        new_defs = {n.name: ast.dump(n) for n in new.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        changed = [k for k in old_defs if old_defs[k] != new_defs[k]]
        assert changed == ["selftest"]
        print(path + ": only selftest changed among functions/classes")

r2 = evidence / "author-r2/receipts"
hash_lines = (r2 / "images/elf-hashes.txt").read_text().splitlines()
images = [line.split(maxsplit=2) for line in hash_lines if line.startswith("IDENTICAL ")]
assert len(images) == 28 and len({x[2] for x in images}) == 28
assert not any(line.startswith("DIFFERENT ") for line in hash_lines)
print("Published rebuild receipt: 28 unique identical ELF/bin/hex paths, 0 differences")
for path in ("images/plat_ledger-dbba60e6.log", "images/plat_ledger-ed7df79c.log"):
    text = (r2 / path).read_text()
    print(path, "last line:", text.strip().splitlines()[-1])

text = (r2 / "twin/twin.log").read_text()
assert "twin: 0 finding(s)" in text and "OK (11 checks)" in text
print("Published twin receipt: selftest 11; 0 findings")
plants = Counter(re.findall(r"^plant ([^:]+): REFUSED by", (r2 / "twin/plants-full.log").read_text(), re.M))
assert len(plants) == 16 and set(plants.values()) == {2}
print("Published plants receipt:", len(plants), "unique plants;", sum(plants.values()), "refusals")
for name, n in sorted(plants.items()):
    print(f"  {name}: {n}")
steps = (r2 / "docs/summary.txt").read_text().splitlines()
assert len(steps) == 44 and all("\trc=0\t" in line for line in steps)
print("Published docs receipts: 44 steps, all rc 0")
for p in ("twin/times.txt", "images/times.txt", "docs/head", "selftest/head"):
    print(p + ":")
    print((r2 / p).read_text().strip())
for side in ("base", "head"):
    summary = evidence / f"author-route/receipts/{side}/summary.txt"
    print(summary.relative_to(evidence))
    print(summary.read_text().strip())
print("PASS: receipt integrity, delta scope and published counts agree")
