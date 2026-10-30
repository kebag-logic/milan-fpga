#!/usr/bin/env bash
# Run the parent consumer gates with the gptp-processor gitlink set to one SHA.
# Usage: parent_gates.sh <parent-clone> <gitlink-sha> <log-dir> [repin]
# With "repin", parent docs pinning f97c1803 are rewritten to the gitlink for
# the gPTP-docs gate only, then restored. Nothing is committed or pushed.
set -u
PARENT=$1; SHA=$2; LOG=$3; REPIN=${4:-}
SUB=$PARENT/gptp-processor
OLD=f97c18035be6ef5345e5af27db2124c5697c1b40
mkdir -p "$LOG"
[ "$(git -C "$PARENT" rev-parse --show-toplevel)" = "$PARENT" ] || { echo "parent toplevel mismatch"; exit 2; }
[ "$(git -C "$SUB" rev-parse --show-toplevel)" = "$SUB" ] || { echo "submodule toplevel mismatch"; exit 2; }
git -C "$SUB" checkout -q --detach "$SHA" || exit 2
git -C "$PARENT" update-index --cacheinfo "160000,$SHA,gptp-processor" || exit 2
echo "gitlink $(git -C "$PARENT" ls-files --stage -- gptp-processor | cut -c8-47) checkout $(git -C "$SUB" rev-parse HEAD)"
gate() { # name command...
  local name=$1; shift
  ( cd "$PARENT" && "$@" ) > "$LOG/$name.log" 2>&1
  echo "$name rc=$?"
}
if [ "$REPIN" = repin ]; then
  files=$(cd "$PARENT" && grep -rl "$OLD\|${OLD:0:8}" docs README.md 2>/dev/null)
  ( cd "$PARENT" && sed -i "s/$OLD/$SHA/g; s/${OLD:0:8}/${SHA:0:8}/g" $files )
  echo "repinned $(echo "$files" | wc -w) files"
  gate check_gptp_docs_with_submodule_repinned python3 scripts/check_gptp_docs.py --with-submodule
  ( cd "$PARENT" && git checkout -q -- $files )
  exit 0
fi
gate check_gptp_docs python3 scripts/check_gptp_docs.py
gate check_gptp_docs_with_submodule python3 scripts/check_gptp_docs.py --with-submodule
gate check_gptp_docs_selftest python3 scripts/check_gptp_docs.py --selftest
gate make_gptp_processor_docs make -C gptp-processor docs
gate check_submodule_docs python3 scripts/check_submodule_docs.py
gate check_submodule_docs_selftest python3 scripts/check_submodule_docs.py --selftest
gate measure_naming python3 scripts/measure_naming.py --check
gate measure_fail_fast python3 scripts/measure_fail_fast.py --check
gate measure_test_evidence python3 scripts/measure_test_evidence.py --check
gate check_hygiene python3 scripts/check_hygiene.py --check
