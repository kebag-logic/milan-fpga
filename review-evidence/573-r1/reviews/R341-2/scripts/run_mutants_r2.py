"""Round-2 single-site mutants against the repository's declaration entry point.

Usage: python3 run_mutants_r2.py <tree> <cases.json> > receipt.json
A case needs keys id, file (tree-relative), old, new; `old` must occur exactly
once in `file`. Every touched file is restored and re-hashed at the end.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

tree = Path(sys.argv[1]).resolve()
cases = json.loads(Path(sys.argv[2]).read_text())
originals = {c["file"]: (tree / c["file"]).read_bytes() for c in cases}
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tree, text=True).strip()


def run():
    return subprocess.run(["python3", "-B", "sw/builder/test_declarations.py"],
                          cwd=tree, capture_output=True, text=True, timeout=900)


rows = []
try:
    for case in cases:
        path = tree / case["file"]
        text = originals[case["file"]].decode()
        count = text.count(case["old"])
        if count != 1:
            rows.append(dict(id=case["id"], applied=False, occurrences=count))
            continue
        path.write_text(text.replace(case["old"], case["new"]))
        result = run()
        lines = (result.stdout + result.stderr).strip().splitlines()
        rows.append(dict(id=case["id"], file=case["file"], applied=True,
                         returncode=result.returncode,
                         verdict="KILLED" if result.returncode else "SURVIVED",
                         last_line=lines[-1] if lines else ""))
        path.write_bytes(originals[case["file"]])
finally:
    for name, data in originals.items():
        (tree / name).write_bytes(data)
restored = {name: hashlib.sha256((tree / name).read_bytes()).hexdigest() == hashlib.sha256(data).hexdigest()
            for name, data in originals.items()}
control = run()
print(json.dumps(dict(head=head, cases=rows, restored=restored,
                      restored_control_returncode=control.returncode), indent=1))
