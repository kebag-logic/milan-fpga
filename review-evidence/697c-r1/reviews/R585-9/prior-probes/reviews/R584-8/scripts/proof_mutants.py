#!/usr/bin/env python3
"""Disposable mutants of the pin proof (ctrl_build.py / ctrl_pin.py) of a milan-fpga checkout.
Each mutant edits one anchor (which must occur exactly once), runs pin_suite.py, records which
controls escape and what the census says, then restores the exact original bytes.
Usage: proof_mutants.py <checkout> <scratch-dir> <receipt-dir>"""
import subprocess
import sys
from pathlib import Path

root, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
HERE = Path(__file__).resolve().parent
BUILD = "sw/firmware/ctrl/test/ctrl_build.py"
PIN = "sw/firmware/ctrl/test/ctrl_pin.py"

MUTANTS = {
    "M1-no-replace-env": (BUILD, '"GIT_NO_REPLACE_OBJECTS": "1", ', ''),
    "M2-no-graft-env": (BUILD, ', "GIT_GRAFT_FILE": NO_GRAFTS', ''),
    "M3-disk-hash-through-git-filters": (
        BUILD, "found[rel] = (\"100755\" if mode & stat.S_IXUSR else \"100644\", \"blob\", blob_id(path, algorithm))",
        "found[rel] = (\"100755\" if mode & stat.S_IXUSR else \"100644\", \"blob\", "
        "git(stack, \"hash-object\", \"--\", rel).stdout.strip())"),
    "M4-mode-not-compared": (BUILD, '("100755" if mode & stat.S_IXUSR else "100644", "blob"', '("100644", "blob"'),
    "M5-symlinks-followed": (BUILD, "data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()",
                             "data = path.read_bytes()"),
    "M5b-symlinks-followed-and-typed-by-target": (BUILD, "path.lstat().st_mode", "path.stat().st_mode",
                                                  "data = os.readlink(path).encode() if path.is_symlink() else "
                                                  "path.read_bytes()", "data = path.read_bytes()"),
    "M6-partial-tree": (BUILD, "found = on_disk(stack, algorithm)",
                        "found = on_disk(stack, algorithm)\n    keep = ('src', 'include', 'tests', 'examples', "
                        "'scripts', 'cmake', 'CMakeLists.txt')\n    want = {k: v for k, v in want.items() if "
                        "k.split('/')[0] in keep}\n    found = {k: v for k, v in found.items() if k.split('/')[0] in keep}"),
    "M7-extra-paths-ignored": (BUILD, "for name in want.keys() | found.keys()", "for name in want.keys()"),
    # a Git command outside the helper in its dashed form: the census must name it
    "M8-dashed-ls-tree-outside-helper": (
        BUILD, 'tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)',
        'tree = run(["/usr/lib/git-core/git-ls-tree", "-r", "-t", "-z", "--full-tree", pin], cwd=stack)'),
    "M9-dashed-rev-parse-outside-helper": (
        BUILD, 'head = git(stack, "rev-parse", "HEAD").stdout.strip()',
        'head = run(["/usr/lib/git-core/git-rev-parse", "HEAD"], cwd=stack).stdout.strip()'),
    # the gitlink read outside the helper in the dashed form, no control's anchor touched
    "M11-dashed-ls-files-outside-helper": (
        BUILD, 'entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()',
        'entry = run(["/usr/lib/git-core/git-ls-files", "--stage", "--", rel], cwd=root).stdout.split()'),
    "M10-plain-ls-tree-outside-helper": (
        BUILD, 'tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)',
        'tree = run(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])'),
}

summary = []
for name, (rel, *edits) in MUTANTS.items():
    if len(sys.argv) > 4 and name not in sys.argv[4:]:
        continue
    path = root / rel
    original = path.read_bytes()
    text = original.decode()
    pairs = list(zip(edits[::2], edits[1::2]))
    if any(text.count(old) != 1 for old, _ in pairs):
        summary.append(f"{name}: ANCHOR not unique, not run")
        continue
    for old, new in pairs:
        text = text.replace(old, new)
    try:
        path.write_text(text, encoding="utf-8")
        res = subprocess.run([sys.executable, "-I", str(HERE / "pin_suite.py"), str(root), str(scratch / name)],
                             capture_output=True, text=True, timeout=600)
    finally:
        path.write_bytes(original)
    log = res.stdout + res.stderr
    (out / f"{name}.log").write_text(log, encoding="utf-8")
    escaped = [ln.split("pin control, ", 1)[-1].split(":", 1)[0] for ln in log.splitlines()
               if ln.startswith("[ESCAPED]")]
    census = next((ln for ln in log.splitlines() if ln.startswith("census findings:")), "census: no line")
    summary.append(f"{name}: rc={res.returncode}; escaped={escaped}; {census[:220]}")
(out / "SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
print("\n".join(summary))
