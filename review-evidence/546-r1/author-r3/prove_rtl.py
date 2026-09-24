import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

base = "d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
print("Base:", base)
print("Head:", head)

def git(*args):
    return subprocess.check_output(["git", *args], timeout=120)

def population(rev):
    return {path for path in git("ls-tree", "-r", "--name-only", rev, "hdl").decode().splitlines()
            if path.endswith((".sv", ".v"))}

# Preserve strings, escaped identifiers and all non-comment code spacing.
# Remove comments and blank-only lines, which comment edits can add.
lexer = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/|\\[^\s]+|\s+|.', re.S)
def normalized(source):
    pieces = []
    for match in lexer.finditer(source):
        token = match.group()
        if token.startswith(("//", "/*")):
            pieces.append("\n" * token.count("\n"))
        else:
            pieces.append(token)
    return "\n".join(line for line in "".join(pieces).splitlines() if line.strip()).encode()

paths = population(base)
assert paths == population(head), "HDL population changed"
changed = []
for path in sorted(paths):
    before = git("show", base + ":" + path)
    after = git("show", head + ":" + path)
    assert Path(path).read_bytes() == after, "Worktree differs from committed HDL"
    assert normalized(before.decode()) == normalized(after.decode()), path
    if before != after:
        changed.append(path)
    if path.endswith(("KL_crf_rx.sv", "KL_mmcm_drp_servo.sv")):
        print(path)
        print("  base normalized sha256:", hashlib.sha256(normalized(before.decode())).hexdigest())
        print("  head normalized sha256:", hashlib.sha256(normalized(after.decode())).hexdigest())
        print("  raw bytes equal:", before == after)
assert changed == ["hdl/ieee1722/crf/KL_crf_rx.sv"], changed
print("PASS: comment-free RTL unchanged across", len(paths), "tracked HDL files")
print("Changed HDL bytes:", ", ".join(changed))
with tempfile.TemporaryDirectory(prefix="546-a278-constant-", dir="/tmp") as tmp:
    for rev, label in [(base, "base"), (head, "head")]:
        work = Path(tmp) / label
        work.mkdir()
        source = work / "KL_crf_rx.sv"
        source.write_bytes(git("show", rev + ":hdl/ieee1722/crf/KL_crf_rx.sv"))
        ast = work / "constants.json"
        command = ["verilator", "--json-only", "-Wno-fatal", "--top-module", "KL_crf_rx",
                   "--Mdir", str(work / "obj"), "--json-only-output", str(ast), str(source)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        assert result.returncode == 0, result.stdout + result.stderr
        def variables(node):
            if isinstance(node, dict):
                if node.get("type") == "VAR":
                    yield node
                for child in node.values():
                    yield from variables(child)
            elif isinstance(node, list):
                for child in node:
                    yield from variables(child)
        params = list(variables(json.loads(ast.read_text())))
        for name, expected in [("RATE_DRIFT_NS_C", 601), ("TS_JUMP_NS_C", 2048)]:
            matches = [param for param in params if param.get("name") == name]
            assert len(matches) == 1, name
            value = matches[0]["valuep"][0]["name"]
            digits = value.split("'", 1)[1]
            if digits.startswith("s"):
                digits = digits[1:]
            number = int(digits[1:].replace("_", ""), {"h": 16, "d": 10, "b": 2, "o": 8}[digits[0]])
            assert number == expected, (label, name, value)
            print(label, name, "=", number, "(", value, ")")
print("PASS: both revisions elaborate TS_JUMP_NS_C to 2048 ns")
