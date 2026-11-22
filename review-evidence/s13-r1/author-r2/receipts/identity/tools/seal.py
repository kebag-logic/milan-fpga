#!/usr/bin/env python3
"""seal.py DIR: write DIR/MANIFEST.sha256 over every file below DIR (sorted, sha256 and path), run DIR/tools/replay.py
over DIR into DIR/replay-output.txt, then write the manifest again so it lists that output too. Exit: replay's."""
import hashlib
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def seal():
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}"
            for p in sorted(root.rglob("*")) if p.is_file() and p.name != "MANIFEST.sha256"]
    (root / "MANIFEST.sha256").write_text("\n".join(rows) + "\n")
    return len(rows)


(root / "replay-output.txt").unlink(missing_ok=True)
n = seal()
run = subprocess.run([sys.executable, "-I", str(root / "tools/replay.py"), str(root)], capture_output=True, text=True)
header = (f"# python3 -I tools/replay.py . (run from this directory), over the {n} files MANIFEST.sha256 listed before "
          f"this output was added; exit {run.returncode}\n")
(root / "replay-output.txt").write_text(header + run.stdout + run.stderr)
print(f"sealed {seal()} files; replay exit {run.returncode}")
sys.exit(run.returncode)
