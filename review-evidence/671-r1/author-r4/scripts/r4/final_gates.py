"""Check the refreshed capture receipt and all final changed-document consumers."""
import concurrent.futures
import subprocess
import sys
from pathlib import Path

repo, logs = map(Path, sys.argv[1:])
logs.mkdir(parents=True, exist_ok=True)
commands = [
    ("capture", ["python3", "scripts/check_nvm_capture.py"], 0),
    *[(f"capture-{mutation}", ["python3", "scripts/check_nvm_capture.py", "--mutation", mutation], 1)
      for mutation in ("bytes", "records", "clock", "ignore-off-timing")],
    ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"], 0),
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"], 0),
    ("hygiene", ["python3", "scripts/check_hygiene.py", "--check"], 0),
    ("docs", ["python3", "scripts/docs_check.py"], 0),
    ("toc", ["python3", "scripts/gen_toc.py", "--check"], 0),
    ("doc-style", ["python3", "scripts/check_doc_style.py"], 0),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"], 0),
    ("diff", ["git", "diff", "--check"], 0),
    ("branch-diff", ["git", "diff", "--check", "e8454e27", "HEAD"], 0),
]

def run(item):
    name, command, expected = item
    with (logs / f"{name}.log").open("w") as log:
        result = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT)
    return name, command, expected, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands))
for name, command, expected, got in results:
    print(f"{name}: rc={got} expected={expected} " + " ".join(command))
assert all(got == expected for _, _, expected, got in results), "a final gate failed"
print("Final gates and four required negative controls: PASS")
