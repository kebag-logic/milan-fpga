#!/usr/bin/env python3
"""regen_patches.py <repo> <scratch> <patch>...: rewrite each one-file patch against the
repo's working file: its old comment text is updated, it is applied with git apply in a
scratch copy, and the hunk is re-emitted with difflib (a/ b/ headers, no index line)."""
import difflib, shutil, subprocess, sys
from pathlib import Path
OLD_C = "// periodic!, or the own sLA on its tx!"
NEW_C = "// periodic!, or a LeaveAll on a tx! clock (own sLA)"
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
for p in map(Path, sys.argv[3:]):
    text = p.read_text().replace(OLD_C, NEW_C)
    rel = next(l[6:] for l in text.splitlines() if l.startswith("+++ b/"))
    work = scratch / p.stem
    shutil.rmtree(work, ignore_errors=True)
    (work / rel).parent.mkdir(parents=True)
    shutil.copy(repo / rel, work / rel)
    tmp = scratch / (p.stem + ".in.patch")
    tmp.write_text(text)
    subprocess.run(["git", "apply", "--check", str(tmp)], cwd=work, check=True)
    subprocess.run(["git", "apply", str(tmp)], cwd=work, check=True)
    src = (repo / rel).read_text().splitlines(True)
    dst = (work / rel).read_text().splitlines(True)
    out = "".join(difflib.unified_diff(src, dst, f"a/{rel}", f"b/{rel}", n=3))
    p.write_text(out)
    print(f"rewrote {p.name}")
