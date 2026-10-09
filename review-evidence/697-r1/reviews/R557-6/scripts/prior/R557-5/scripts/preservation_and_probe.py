#!/usr/bin/env python3
"""Check production preservation and reproduce assembly gaps in disposable copies."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
work = packet / "scratch/preservation"
work.mkdir(parents=True, exist_ok=True)
os.environ["TSN_CLANG"] = str(packet / "scratch/clang18/usr/lib/llvm-18/bin/clang")
os.environ["LD_LIBRARY_PATH"] = str(packet / "scratch/clang18/usr/lib/x86_64-linux-gnu")
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
from compiler_tokens import raw_tokens
from check_comments import check
from check_conditionals import compile_file

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

paths = ["src/adp.c", "src/acmp.c", "src/maap.c", "include/adp.h", "include/acmp.h", "include/maap.h", "include/wire.h"]
rows = []
for path in paths:
    base = git("show", "ae982af:" + path)
    prior = git("show", "625b0011:" + path)
    head = (root / path).read_bytes()
    code = lambda data: [(kind, value) for kind, value, *_ in raw_tokens(data.decode(), "c") if kind != "comment" and not value.isspace()]
    rows.append({"path": path, "round6_bytes_equal": prior == head,
                 "base_noncomment_tokens_equal": code(base) == code(head),
                 "head_sha256": hashlib.sha256(head).hexdigest()})
(packet / "receipts/production-preservation.json").write_text(json.dumps(rows, indent=2) + "\n")
assert all(row["round6_bytes_equal"] and row["base_noncomment_tokens_equal"] for row in rows)

tree = work / "probe-tree"
tree.mkdir(exist_ok=True)
for name in git("ls-files", "-z").decode().split("\0"):
    if name:
        target = tree / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
path = tree / "examples/rv32/start.S"
path.write_text(path.read_text() + "\n#define REVIEW_HASH #\nnop REVIEW_HASH review probe prose\n")

def run(item):
    name, args = item
    result = subprocess.run([sys.executable, *args], cwd=tree, capture_output=True, text=True)
    (packet / "receipts" / (name + ".log")).write_text(result.stdout + result.stderr)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    return {"name": name, "rc": result.returncode}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    gates = list(pool.map(run, [
        ("assembly-probe-comment-gate", ["scripts/check_comments.py"]),
        ("assembly-probe-rv32", ["scripts/baremetal.py", "--work", str(work / "probe-rv32"), "--jobs", "2"]),
    ]))
gates.append({"name": "assembly-probe-conditional-matrix", "result": compile_file(tree, "examples/rv32/start.S", work / "matrix", 1)})

source = "#define REVIEW_SKIP .i##f 0\nREVIEW_SKIP\nreview probe prose\n.endif\n"
control = work / "conditional.S"
control.write_text(source)
cc = shutil.which("riscv64-unknown-elf-gcc") or shutil.which("riscv64-elf-gcc")
result = subprocess.run([cc, "-march=rv32i", "-mabi=ilp32", "-Wall", "-Wextra", "-Werror", "-c", str(control), "-o", str(work / "conditional.o")], capture_output=True, text=True)
pp = subprocess.run([cc, "-E", "-P", str(control)], capture_output=True, text=True)
gates.append({"name": "macro-produced-assembler-conditional", "source": source,
              "compile_rc": result.returncode, "compile_output": result.stdout + result.stderr,
              "preprocessed": pp.stdout, "comment_errors": check(source, True, "c", "examples/rv32/control.S")})
(packet / "receipts/assembly-full-tree-probe.json").write_text(json.dumps(gates, indent=2) + "\n")
print(json.dumps(gates, indent=2))
