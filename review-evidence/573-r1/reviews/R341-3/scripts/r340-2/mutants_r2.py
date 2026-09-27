"""Round-2 single-site mutants against sw/builder/test_declarations.py.

Usage: python3 mutants_r2.py <disposable tree root> <cases json> <output json>
Each case: {"id", "file", "old", "new", "expect"}; `old` must occur exactly once
in `file` (relative to the tree). expect is KILLED for a check that must be
detected, or PROBE for a test-adequacy question whose answer is recorded.
Every mutated file is restored after each case and compared byte-for-byte.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
CASES = json.loads(Path(sys.argv[2]).read_text())
FILES = sorted({case["file"] for case in CASES})
ORIGINAL = {name: (ROOT / name).read_bytes() for name in FILES}


def run_tests():
    return subprocess.run([sys.executable, "-B", "sw/builder/test_declarations.py"],
                          cwd=ROOT, capture_output=True, text=True, timeout=1800)


def restore():
    for name, blob in ORIGINAL.items():
        (ROOT / name).write_bytes(blob)


def main() -> None:
    rows = []
    try:
        for case in CASES:
            text = ORIGINAL[case["file"]].decode()
            count = text.count(case["old"])
            if count != 1:
                rows.append(dict(id=case["id"], file=case["file"], applied=False, occurrences=count))
                print(f"NOT-APPLIED {case['id']} ({count})", flush=True)
                continue
            (ROOT / case["file"]).write_text(text.replace(case["old"], case["new"]))
            result = run_tests()
            lines = (result.stdout + result.stderr).strip().splitlines()
            verdict = "KILLED" if result.returncode else "SURVIVED"
            rows.append(dict(id=case["id"], file=case["file"], expect=case["expect"],
                             applied=True, returncode=result.returncode, verdict=verdict,
                             last_line=lines[-1] if lines else ""))
            restore()
            print(f"{verdict:8} [{case['expect']}] {case['id']}: {rows[-1]['last_line'][:170]}",
                  flush=True)
    finally:
        restore()
    control = run_tests()
    rows.append(dict(id="unmutated control", returncode=control.returncode,
                     verdict="PASS" if control.returncode == 0 else "FAIL",
                     last_line=(control.stdout.strip().splitlines() or [""])[-1]))
    rows.append(dict(id="sources restored",
                     sha256={n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in FILES},
                     identical=all((ROOT / n).read_bytes() == b for n, b in ORIGINAL.items())))
    print(rows[-2], rows[-1])
    Path(sys.argv[3]).write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
