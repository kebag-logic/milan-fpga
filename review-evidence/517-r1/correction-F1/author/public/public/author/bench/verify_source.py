#!/usr/bin/env python3
"""Prove the source boundary against the assigned base; write a JSON receipt.
Usage: python3 verify_source.py LANE OUTPUT_JSON
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "483a133ed08867ea0d300d2b4a027b5b48a4282f"

def git(lane, *args):
    return subprocess.check_output(["rtk", "proxy", "git", "-C", str(lane), *args], text=True)

def tokens(text):
    lex = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|\d+(?:\.\d+)?|[^\s]', re.S)
    return [t for t in lex.findall(text) if not t.startswith(("//", "/*"))]

def main():
    lane, output = map(Path, sys.argv[1:])
    head = git(lane, "rev-parse", "HEAD").strip()
    status = git(lane, "status", "--porcelain")
    assert not status, "source must be clean"
    changed = git(lane, "diff", "--name-only", BASE, "HEAD").splitlines()
    prefix = "tb/verilator/milan_dp/"
    assert set(changed) == {prefix + p for p in ("Makefile", "README.md", "sim_nxn.cpp", "sim_pool.py", "test_sim_pool.py")}
    cpp = prefix + "sim_nxn.cpp"
    before = tokens(git(lane, "show", f"{BASE}:{cpp}"))
    after = tokens((lane / cpp).read_text())
    assert before == after, "behavioral C++ tokens changed"
    old = git(lane, "show", f"{BASE}:{prefix}Makefile")
    new = (lane / prefix / "Makefile").read_text()
    old = old.replace("VERILATOR_JOBS ?= 0\n", "VERILATOR_JOBS ?= 0\n# Ordinary simulations only; never derived from the make jobserver.\nSIM_JOBS ?= 2\n")
    a = old.index("\t./obj_dir/Vmilan_dp_sim\n", old.index("\nrun:"))
    b = old.index('\t@echo "---- #386 render law:', a)
    c = new.index("\t@exec python3 sim_pool.py")
    d = new.index('\t@echo "---- #386 render law:', c)
    assert old[:a] == new[:c] and old[b:] == new[d:], "build, prerequisites or render phase changed"
    inventory = [line.strip() for line in old[a:b].splitlines() if line.startswith("\t./")]
    assert len(inventory) == 10
    record = dict(base=BASE, head=head, tree=git(lane, "rev-parse", "HEAD^{tree}").strip(),
                  clean=True, changed=changed, cpp_executable_tokens_equal=True,
                  cpp_token_count=len(after), original_commands=inventory,
                  make_outside_sim_variable_and_ordinary_tail_equal=True,
                  submodule_pins=git(lane, "ls-tree", "HEAD", "protocol-processor", "gptp-processor", "third_party/verilog-axis"),
                  changed_file_sha256={f: hashlib.sha256((lane / f).read_bytes()).hexdigest() for f in changed})
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
