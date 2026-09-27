"""Apply one single-site source mutation at a time to a disposable tree, run the
repository's declaration entry point, record the outcome, and restore the source.

Usage: python3 run_mutants.py <tree> <cases.json> [<cases.json> ...] > receipt.json
A case needs keys issue, name, old, new; `old` must occur exactly once.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

tree = Path(sys.argv[1]).resolve()
source = tree / "sw/builder/endstation_builder.py"
original = source.read_bytes()
digest = hashlib.sha256(original).hexdigest()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tree, text=True).strip()
rows = []
try:
    for cases_path in sys.argv[2:]:
        for case in json.loads(Path(cases_path).read_text()):
            text = original.decode()
            count = text.count(case["old"])
            if count != 1:
                rows.append(dict(case=case["name"], issue=case["issue"], applied=False,
                                 occurrences=count))
                continue
            source.write_text(text.replace(case["old"], case["new"]))
            run = subprocess.run(["python3", "-B", "sw/builder/test_declarations.py"],
                                 cwd=tree, capture_output=True, text=True, timeout=900)
            lines = (run.stdout + run.stderr).strip().splitlines()
            rows.append(dict(case=case["name"], issue=case["issue"], applied=True,
                             source=Path(cases_path).name, returncode=run.returncode,
                             verdict="KILLED" if run.returncode else "SURVIVED",
                             last_line=lines[-1] if lines else ""))
            source.write_bytes(original)
finally:
    source.write_bytes(original)
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
control = subprocess.run(["python3", "-B", "sw/builder/test_declarations.py"],
                         cwd=tree, capture_output=True, text=True, timeout=900)
print(json.dumps(dict(head=head, source_sha256=digest, cases=rows,
                      restored_control_returncode=control.returncode), indent=1))
