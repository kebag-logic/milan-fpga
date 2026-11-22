#!/usr/bin/env python3
"""seal.py DIR: write DIR/MANIFEST.content.sha256 (the decompressed content of every .xz/.gz file below DIR) and
DIR/MANIFEST.sha256 over every file below DIR (sha256sum format, the content manifest included), run
DIR/tools/replay.py over DIR into DIR/replay-output.txt, then write both manifests again so they list that output
too. Exit: replay's."""
import gzip
import hashlib
import lzma
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def content(path):
    data = path.read_bytes()
    return lzma.decompress(data) if path.suffix == ".xz" else gzip.decompress(data)


def seal():
    files = [p for p in sorted(root.rglob("*")) if p.is_file() and not p.name.startswith("MANIFEST.")]
    packed = [f"{hashlib.sha256(content(p)).hexdigest()}  {p.relative_to(root)}"
              for p in files if p.suffix in (".xz", ".gz")]
    (root / "MANIFEST.content.sha256").write_text("\n".join(packed) + "\n")
    files = sorted(files + [root / "MANIFEST.content.sha256"], key=lambda p: str(p.relative_to(root)))
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}" for p in files]
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
