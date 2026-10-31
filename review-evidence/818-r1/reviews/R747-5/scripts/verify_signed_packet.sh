#!/usr/bin/env bash
# Verify the signed local-CI packet for PR #820 head 81f78a81 / candidate 125ac680.
# Usage: verify_signed_packet.sh <dir holding manifest.json, manifest.json.sig, allowed_signers>
set -eu
d=$1
sha256sum "$d/manifest.json"
awk '{print $3" "$4}' "$d/allowed_signers" > "$d/.key.pub"
ssh-keygen -lf "$d/.key.pub"
rm -f "$d/.key.pub"
ssh-keygen -Y verify -f "$d/allowed_signers" -I milan-local-ci -n milan-local-ci -s "$d/manifest.json.sig" < "$d/manifest.json"
python3 -I - "$d/manifest.json" <<'EOF'
import json, sys
m = json.load(open(sys.argv[1]))
s, cov = m["subject"], m["execution"]["coverage"]
print("subject", s["candidate"], s["candidate_tree"], s["candidate_parent"], s["head"], s["head_tree"], s["pr"])
print("result", m["result"], "coverage", len(cov), "not ok", [k for k, v in cov.items() if v.get("ok") is not True])
print("not act", {k: v.get("reason", "")[:80] for k, v in cov.items() if v["by"] != "act"})
print("act non-success", {k: v for k, v in m["execution"]["act"]["jobs"].items() if v != "success"})
EOF
