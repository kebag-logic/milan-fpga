#!/usr/bin/env python3
"""Short compiling controls for comment and assertion-message boundaries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
work = packet / "scratch/independent-probes"
work.mkdir(parents=True, exist_ok=True)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
os.environ["TSN_CLANG"] = str(packet / "scratch/clang18/usr/lib/llvm-18/bin/clang")
os.environ["LD_LIBRARY_PATH"] = str(packet / "scratch/clang18/usr/lib/x86_64-linux-gnu")
sys.path.insert(0, str(root / "scripts"))
from check_comments import check
from check_conditionals import compile_file
from assertion_messages import inventory, instrument
from needle_audit import validate_needles
from mutation import execute, matches, MESSAGE_MARKERS

cross = shutil.which("riscv64-unknown-elf-gcc") or shutil.which("riscv64-elf-gcc")
rows = []
comments = {
    "assembly-direct": (".S", "nop # review probe prose\n"),
    "assembly-macro-hash": (".S", "#define REVIEW_HASH #\nnop REVIEW_HASH review probe prose\n"),
    "assembly-macro-hash-trace": (".S", "#define REVIEW_HASH #\nnop REVIEW_HASH REQ: PORT-01\n"),
    "c-trigraph-comment": (".c", "/??/\n/ review probe prose\nint value;\n"),
    "cpp-digit-comment": (".cpp", "int value = 1'000; // review probe prose\n"),
    "cpp-raw-plus-comment": (".cpp", "const char *value = R\"tag(// data)tag\"; /* review probe prose */\n"),
    "unlisted-conditional": (".c", "#ifdef REVIEW_UNUSED\nreview probe prose\n#endif\n"),
    "allowed-conditional": (".c", "#ifdef NDEBUG\nint value;\n#else\nlong value;\n#endif\n"),
}
for name, (suffix, text) in comments.items():
    path = work / (name + suffix)
    path.write_text(text)
    flags = [cross, "-march=rv32i", "-mabi=ilp32"] if suffix == ".S" else ["clang", "-std=c11" if suffix == ".c" else "-std=c++20", "-Wno-trigraphs"]
    cmd = [*flags, "-Wall", "-Wextra", "-Werror", *(["-Wno-trigraphs"] if suffix == ".c" else []), "-c", str(path), "-o", str(path.with_suffix(".o"))]
    result = subprocess.run(cmd, capture_output=True, text=True)
    errors = check(text, suffix == ".S", "c++" if suffix == ".cpp" else "c", "examples/rv32/control.S" if suffix == ".S" else "src/control.c")
    row = {"name": name, "source": text, "compile_rc": result.returncode, "compile_output": result.stdout + result.stderr, "comment_errors": errors}
    if suffix == ".S":
        pp = subprocess.run([cross, "-E", "-P", str(path)], capture_output=True, text=True)
        row["preprocessed"] = pp.stdout
        tree = work / name
        target = tree / "examples/rv32/control.S"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        try:
            row["conditional_matrix"] = compile_file(tree, "examples/rv32/control.S", tree / "matrix", 1)
        except Exception as error:
            row["conditional_error"] = str(error)
    rows.append(row)

source = """#include <gtest/gtest.h>
TEST(Review, Near) { EXPECT_NEAR(1.0, 2.0, 0.1) << "The difference between"; }
TEST(Review, NearUnrelated) { EXPECT_NEAR(1.0, 2.0, 0.1) << "specific different message"; }
"""
path = work / "needles.cpp"
path.write_text(instrument(source, MESSAGE_MARKERS))
result = subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Werror", str(path), "-lgtest_main", "-lgtest", "-pthread", "-o", str(work / "needles")], capture_output=True, text=True)
row = {"name": "default-near-template", "source": source, "compile_rc": result.returncode, "compile_output": result.stdout + result.stderr}
if result.returncode == 0:
    rc, failures, count = execute(work / "needles", work / "needles.xml", [])
    kill = {"test": "Review.Near", "needle": "The difference between"}
    row.update(run_rc=rc, count=count, failures=failures,
               audit_errors=validate_needles([{"name": "control", "kills": [kill]}], inventory(source)),
               streamed_match=matches(kill, failures),
               unrelated_default_match=matches(dict(kill, test="Review.NearUnrelated"), failures))
rows.append(row)
(packet / "receipts/independent-probes.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
