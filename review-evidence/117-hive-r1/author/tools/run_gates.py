"""Run the eight assigned gates in the physical worktree, preserving return codes."""
from pathlib import Path
import json
import subprocess
import sys
p = Path(__file__).resolve().parent.parent
repo = Path("$LANES/117-la-avdecc-enum")
commands = [
 [sys.executable, "scripts/docs_check.py"],
 [sys.executable, "scripts/check_doc_style.py"],
 [sys.executable, "scripts/gen_toc.py", "--check"],
 [sys.executable, "scripts/check_em_dash.py", "--base", "2a2a7bb6"],
 [sys.executable, "scripts/check_doc_paths.py"],
 [sys.executable, "scripts/ci_scope.py", "--selftest"],
 [sys.executable, "scripts/check_baremetal_only.py", "--check"],
 ["git", "diff", "--check"],
]
results = []
for i,cmd in enumerate(commands,1):
 r = subprocess.run(["timeout", "90s", *cmd], cwd=repo, capture_output=True, text=True, timeout=95)
 text = "COMMAND " + " ".join(cmd) + "\nCWD " + str(repo) + "\n" + r.stdout + r.stderr + "\nRC " + str(r.returncode) + "\n"
 assert len(text.encode()) <= 200000
 (p / f"gate-{i}.txt").write_text(text)
 results.append({"command":cmd, "rc":r.returncode})
 print(text, flush=True)
(p / "gates.json").write_text(json.dumps(results, indent=2)+"\n")
raise SystemExit(any(r["rc"] != 0 for r in results))
