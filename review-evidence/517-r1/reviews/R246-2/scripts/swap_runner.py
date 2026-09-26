#!/usr/bin/env python3
"""R246-2: run the HEAD pool tests against a substituted file, then restore.

Usage: python3 swap_runner.py <probe-tree> <receipt-dir> <label> <relpath> <source> \
           <test-file> <runs> <default|ignored> [<test-file> <runs> <disp> ...]

<source> is either `blob:<sha>` (read with git cat-file from the probe tree) or
`sed:<old>=><new>` applied once to the current bytes (anchor asserted unique).
The original bytes of <relpath> are restored and verified afterwards.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    tree, out, label, rel, source = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                     sys.argv[3], sys.argv[4], sys.argv[5])
    target = tree / rel
    original = target.read_bytes()
    if source.startswith("blob:"):
        new = subprocess.run(["git", "-C", str(tree), "cat-file", "blob", source[5:]],
                             capture_output=True, check=True).stdout
    else:
        old, repl = source[4:].split("=>", 1)
        old, repl = old.encode().decode("unicode_escape"), repl.encode().decode("unicode_escape")
        text = original.decode()
        assert text.count(old) == 1, f"anchor count {text.count(old)}"
        new = text.replace(old, repl).encode()
    try:
        target.write_bytes(new)
        print(f"{label}: {rel} sha256 {hashlib.sha256(new).hexdigest()}", flush=True)
        rest = sys.argv[6:]
        for k in range(0, len(rest), 3):
            test, runs, disp = rest[k:k + 3]
            subprocess.run([sys.executable, str(HERE / "repeat_disposition.py"), str(target.parent)
                            if rel.startswith("tb/") else str(tree / "tb/verilator/milan_dp"),
                            str(out / label), test, runs, disp, os.environ.get("PAR", "1")], check=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    print(f"restored {rel} sha256 {hashlib.sha256(original).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
