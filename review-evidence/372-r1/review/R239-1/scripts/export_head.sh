#!/bin/sh
# R239: export the exact reviewed head into a scratch tree (read-only on the
# review clone), plus the verilog-axis submodule bytes the ptp_ts `run` leg
# needs, then prove every exported file hashes to the blob the head records.
set -eu
CLONE=$VALIDATION_STORAGE/reviews/r239-372-r1
HEAD_SHA=60c5225fe5f93209bf313c51b7a722f25f9aaa7d
WORK=$VALIDATION_STORAGE/r239-372-r1-work
DEST="$WORK/src"
rm -rf "$DEST"
mkdir -p "$DEST"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$DEST"
AXIS_PIN=$(git -C "$CLONE" ls-tree "$HEAD_SHA" third_party/verilog-axis | awk '{print $3}')
mkdir -p "$DEST/third_party/verilog-axis"
git -C "$CLONE/third_party/verilog-axis" archive "$AXIS_PIN" | tar -x -C "$DEST/third_party/verilog-axis"
echo "exported $HEAD_SHA (tree $(git -C "$CLONE" rev-parse "$HEAD_SHA^{tree}")) and verilog-axis $AXIS_PIN into $DEST"
# Blob-level proof over the parent tree (regular files and symlinks; gitlinks skipped).
python3 - "$CLONE" "$HEAD_SHA" "$DEST" <<'EOF'
import subprocess, sys, os
clone, head, dest = sys.argv[1:]
out = subprocess.run(["git", "-C", clone, "ls-tree", "-r", "-z", head], capture_output=True, check=True).stdout
ok = bad = skipped = 0
for rec in out.split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, kind, oid = meta.split()
    p = os.path.join(dest, path.decode())
    if kind != b"blob":
        skipped += 1
        continue
    if mode == b"120000":
        data = os.readlink(p).encode()
    else:
        with open(p, "rb") as fh:
            data = fh.read()
    h = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.strip()
    if h == oid:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", path.decode())
print(f"export blob proof: match={ok} mismatch={bad} gitlinks-skipped={skipped}")
sys.exit(1 if bad else 0)
EOF
