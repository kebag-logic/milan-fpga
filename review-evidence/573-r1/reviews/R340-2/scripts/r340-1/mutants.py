"""Removed/altered-check mutants against sw/builder/test_declarations.py.

Usage: python3 mutants.py <disposable tree root> <cases json> <output json>
Each case: {"id", "origin", "old", "new"}; `old` must occur exactly once in
sw/builder/endstation_builder.py. The source is restored after every case and
compared byte-for-byte with its original at the end.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
CASES = json.loads(Path(sys.argv[2]).read_text())
SOURCE = ROOT / "sw/builder/endstation_builder.py"
ORIGINAL = SOURCE.read_bytes()


def run_tests():
    return subprocess.run([sys.executable, "-B", "sw/builder/test_declarations.py"],
                          cwd=ROOT, capture_output=True, text=True, timeout=900)


def main() -> None:
    rows = []
    try:
        for case in CASES:
            text = ORIGINAL.decode()
            assert text.count(case["old"]) == 1, case["id"]
            SOURCE.write_text(text.replace(case["old"], case["new"]))
            result = run_tests()
            lines = (result.stdout + result.stderr).strip().splitlines()
            rows.append(dict(id=case["id"], origin=case["origin"], returncode=result.returncode,
                             verdict="KILLED" if result.returncode else "SURVIVED",
                             last_line=lines[-1] if lines else ""))
            SOURCE.write_bytes(ORIGINAL)
            print(f"{rows[-1]['verdict']:8} {case['id']}: {rows[-1]['last_line'][:160]}", flush=True)
    finally:
        SOURCE.write_bytes(ORIGINAL)
    control = run_tests()
    rows.append(dict(id="unmutated control", origin="reviewer", returncode=control.returncode,
                     verdict="PASS" if control.returncode == 0 else "FAIL",
                     last_line=(control.stdout.strip().splitlines() or [""])[-1]))
    rows.append(dict(id="source restored", sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                     identical=SOURCE.read_bytes() == ORIGINAL))
    print(rows[-2], rows[-1])
    Path(sys.argv[3]).write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
