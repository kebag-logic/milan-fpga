#!/bin/sh
# Verify an extracted review-evidence packet against the published evidence commit
# and against its own manifests. usage: verify_packet.sh <git-clone> <evidence-commit> <extract-root>
set -eu
REPO=$1; COMMIT=$2; ROOT=$(cd "$3" && pwd)
cd "$REPO"
n=0; bad=0
git ls-tree -r "$COMMIT" review-evidence/b2-r1 > /tmp/.vp.$$
while read -r mode type blob path; do
  n=$((n+1))
  f="$ROOT/$path"
  if [ ! -f "$f" ]; then echo "MISSING $path"; bad=$((bad+1)); continue; fi
  h=$(git hash-object "$f")
  [ "$h" = "$blob" ] || { echo "BLOBDIFF $path"; bad=$((bad+1)); }
done < /tmp/.vp.$$
rm -f /tmp/.vp.$$
echo "evidence-commit blobs checked: $n, mismatches: $bad"
cd "$ROOT/review-evidence/b2-r1"
python3 - <<'EOF'
import hashlib, json, os
m = json.load(open("MANIFEST.json"))
bad = [e["file"] for e in m if hashlib.sha256(open(e["file"], "rb").read()).hexdigest() != e["published_sha256"]]
red = [e["file"] for e in m if e["path_redacted"]]
files = {os.path.relpath(os.path.join(r, f), ".") for r, _, fs in os.walk(".") for f in fs}
print("outer MANIFEST.json entries:", len(m), "published-hash mismatches:", len(bad), "unlisted:", sorted(files - {e["file"] for e in m} - {"MANIFEST.json"}))
print("path-redacted entries (author hash differs by design):", red)
EOF
cd author
echo "author MANIFEST.sha256 failures (expected: exactly the redacted files):"
sha256sum -c MANIFEST.sha256 2>/dev/null | grep -v ': OK$' || true
