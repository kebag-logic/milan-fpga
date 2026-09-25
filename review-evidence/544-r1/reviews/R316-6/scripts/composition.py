#!/usr/bin/env python3
"""Prove path overlap, source retention and raw shared-file composition."""
import argparse
import ast
import hashlib
from pathlib import Path
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("scratch", type=Path)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(["git", "-C", str(a.root), *args])
base, source, parent = "ffcbd33d", "8383e929", "59e7f5fd"
paths = git("diff", "--name-only", base, source).decode().splitlines()
print("Source paths:", paths)
assert paths == ["docs/integration/BAREMETAL_FIRMWARE.md", "sw/builder/test_builder.py"]
print(git("log", "-6", "--first-parent", "--format=%H %P %s", "HEAD").decode())
for label, head in (("dev(387b)", "e1333a14"), ("548", "0b81fdc9"),
                    ("501", "2ab66c9d"), ("546", parent)):
    changed = git("diff", "--name-only", head + "^", head).decode().splitlines()
    print(label, "overlap:", sorted(set(paths) & set(changed)))
for path in paths:
    blobs = [git("show", rev + ":" + path) for rev in (base, source, parent, "HEAD")]
    with tempfile.TemporaryDirectory(dir=a.scratch) as tmp:
        files = [Path(tmp) / str(n) for n in range(3)]
        for f, data in zip(files, (blobs[2], blobs[0], blobs[1])):
            f.write_bytes(data)
        merged = subprocess.run(["git", "merge-file", "-p", *map(str, files)],
                                capture_output=True)
        assert merged.returncode == 0, path
        assert merged.stdout == blobs[3], path
    print("Raw three-way merge equals candidate:", path,
          "sha256", hashlib.sha256(blobs[3]).hexdigest())
def functions(data):
    return {n.name: ast.dump(n, include_attributes=False)
            for n in ast.walk(ast.parse(data)) if isinstance(n, ast.FunctionDef)}
left = functions(git("show", source + ":sw/builder/test_builder.py"))
right = functions(git("show", "HEAD:sw/builder/test_builder.py"))
for name in ("assert_identity_macro_free", "assert_identity_interval",
             "assert_preprocessed_identity_sample", "assert_preprocessed_asm_allowlist"):
    assert left[name] == right[name]
    print("Unchanged source identity function AST:", name)
changed = git("diff", "--name-only", parent, "HEAD").decode().splitlines()
assert changed == paths
print("No candidate-local changes to RTL, firmware, workflows, registries or gitlinks.")
print("Source-to-candidate firmware changes:")
print(git("diff", "--stat", source, "HEAD", "--", "sw/firmware").decode())
print("PASS: source delta retained, predecessor delta retained, no conflict resolution delta.")
