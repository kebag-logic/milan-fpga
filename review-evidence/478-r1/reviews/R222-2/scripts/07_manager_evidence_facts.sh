#!/usr/bin/env bash
# Identity and exit facts from the manager's round2 packet in the immutable
# evidence archive (3811227e), cross-checked against this review clone. Only
# round2/manager and round2/candidate.json are parsed. Read-only.
set -euo pipefail
E=${EVIDENCE:-/tmp/r222-478-r2-scratch/evidence}
C=3811227ee1af4ed96493528f1af17e852e2b7176
M=review-evidence/478-r1/round2/manager
R=$VALIDATION_STORAGE/reviews/r222-478-r2
blob() { git -C "$E" cat-file blob "$C:$1"; }

echo "## round2/candidate.json"; blob review-evidence/478-r1/round2/candidate.json
echo "## static/builder bank (manager-builder/results.json)"
blob $M/manager-builder/results.json | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("head", d["head"], "base", d["base"])
rs = d["results"]
print("commands", len(rs), "non-zero", sum(r["exit_code"] != 0 for r in rs))
for r in rs:
    if "test_builder" in " ".join(r["command"]) or "docs_check" in " ".join(r["command"]) or "check_em_dash" in " ".join(r["command"]):
        print("  exit", r["exit_code"], " ".join(r["command"]))'
blob $M/manager-builder/complete.json
echo "## builder log (40.log): gate 36a lines and verdict"
blob $M/manager-builder/40.log | grep -E 'gate 36a|ALL GATES|NOT RUN|\[gate 11\]'
echo "## full native (full-native/results.json)"
blob $M/full-native/results.json | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("head", d["head"], "base", d["base"])
for r in d["results"]:
    print("  exit", r["exit_code"], "%8.1fs" % r["seconds"], " ".join(r["command"]))'
blob $M/full-native/complete.json
echo "## parent sweep summary (full-native/01.log)"
blob $M/full-native/01.log | grep -E '^checks:|declared skips|SKIPPED|^PASS +pp_shadow|^FAIL' || true
echo "## Verilator version reported by the native logs"
for f in full-suite-logs/pp_shadow.log full-native/04.log; do
  printf '%s: %s\n' "$f" "$(blob $M/$f | grep -o -E 'Verilator [0-9]+\.[0-9]+' | sort -u | tr '\n' ' ')"
done
echo "## integrity records vs this review clone"
for f in builder-integrity.json builder-final-tree-integrity.json native-tree-integrity.json; do
  blob $M/$f | python3 -c '
import json, sys
d = json.load(sys.stdin); p = d["parent"]; s = d["required_submodules"]
print(sys.argv[1], d["result"], p["head"], p["tree"], p["files_verified"],
      {k: (v["head"][:12], v["tree"][:12], v["files_verified"]) for k, v in s.items()})' "$f"
done
echo "review clone: head=$(git -C "$R" rev-parse HEAD) tree=$(git -C "$R" rev-parse 'HEAD^{tree}') files=$(git -C "$R" ls-tree -r HEAD | awk '$2=="blob"' | wc -l)"
for p in third_party/verilog-axis protocol-processor gptp-processor; do
  echo "  $p head=$(git -C "$R/$p" rev-parse HEAD | cut -c1-12) tree=$(git -C "$R/$p" rev-parse 'HEAD^{tree}' | cut -c1-12) files=$(git -C "$R/$p" ls-tree -r HEAD | wc -l)"
done
