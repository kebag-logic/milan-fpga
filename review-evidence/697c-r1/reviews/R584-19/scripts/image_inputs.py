#!/usr/bin/env python3
"""Reviewer probe: which image-input paths differ between revisions.

For the pairs (dev d5858bbe -> dev e81ce82f) and (PR 97e71316 -> PR d40e4e98), list every changed path
under the trees the RV32 image builders read (sw/, configs/, the third_party gitlinks, gptp-processor and
protocol-processor gitlinks) and every changed path elsewhere. Then compare the PR's own patch over sw/,
configs/ and third_party/ against each dev base: identical patches over identical bases mean identical
image inputs. Usage: python3 -I image_inputs.py <checkout>"""
import subprocess
import sys

root = sys.argv[1]
IMAGE_TREES = ("sw/", "configs/", "third_party/", "gptp-processor", "protocol-processor")


def git(*a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


def changed(a, b):
    return [ln for ln in git("diff", "--name-only", "--no-renames", a, b).splitlines() if ln]


for a, b, label in (("d5858bbee328cf8d2c39a99ec14203f5d0ddd123", "e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c",
                     "dev d5858bbe -> dev e81ce82f"),
                    ("97e713168470bfae2685521fa557dc462b782b32", "d40e4e9827be2516f8f34b9d65f0a483fff2194c",
                     "PR 97e71316 -> PR d40e4e98")):
    paths = changed(a, b)
    image = [p for p in paths if p.startswith(IMAGE_TREES)]
    print(f"{label}: {len(paths)} paths changed, {len(image)} under image-builder trees")
    for p in image:
        print(f"  {p}")

# The PR's patch over the image trees, against each dev base it was merged with.
spec = ["--", "sw", "configs", "third_party", "gptp-processor", "protocol-processor"]
old = git("diff", "--no-renames", "--full-index", "d5858bbee328cf8d2c39a99ec14203f5d0ddd123",
          "97e713168470bfae2685521fa557dc462b782b32", *spec)
new = git("diff", "--no-renames", "--full-index", "e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c",
          "d40e4e9827be2516f8f34b9d65f0a483fff2194c", *spec)


def files(patch):
    out, cur = {}, None
    for ln in patch.splitlines(keepends=True):
        if ln.startswith("diff --git "):
            cur = ln.split(" b/", 1)[1].strip()
            out[cur] = ""
        out[cur] += ln
    return out


fo, fn = files(old), files(new)
same = sorted(k for k in fo.keys() & fn.keys() if fo[k] == fn[k])
diff = sorted(k for k in fo.keys() | fn.keys() if fo.get(k) != fn.get(k))
print(f"PR patch over image trees: {len(fo)} files vs d5858bbe, {len(fn)} files vs e81ce82f; "
      f"{len(same)} byte-identical file patches, {len(diff)} differ")
for k in diff:
    print(f"  differs: {k}")
