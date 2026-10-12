#!/usr/bin/env bash
# Composition probes: in a disposable copy of the candidate, remove one
# side's entry from each file both sides changed and require the gate that
# reads it to fail; restore exact bytes after each probe.
# Usage: probes.sh <candidate-repo> <scratch-copy> <outdir>
set -u
src=$1; copy=$2; out=$3
mkdir -p "$out"
rm -rf "$copy"; cp -a "$src" "$copy"; cd "$copy" || exit 2
probe() { # name, file, python-edit, gate...
  local name=$1 file=$2 edit=$3; shift 3
  cp -p "$file" "$out/.orig"
  python3 -c "$edit" "$file" >"$out/$name.edit" 2>&1
  if cmp -s "$file" "$out/.orig"; then echo "PROBE-NOT-APPLIED $name" | tee -a "$out/SUMMARY.txt"; return; fi
  "$@" >"$out/$name.log" 2>&1; rc=$?
  cp -p "$out/.orig" "$file"
  printf '%s rc=%s %s\n' "$([ $rc -ne 0 ] && echo CAUGHT || echo MISSED)" "$rc" "$name" | tee -a "$out/SUMMARY.txt"
}
: >"$out/SUMMARY.txt"
cut_entry='import re,sys
p=sys.argv[1]; key=sys.argv[2]; s=open(p).read()
i=s.index("    \""+key+"\":"); j=s.index("\n    \"",i+1) if "\n    \"" in s[i+1:] else s.index("\n}",i)
k=s.find("\n}",i); j=min(j,k) if j>0 else k
open(p,"w").write(s[:i]+s[j+1:])'
for key in tb/verilator/csr/lock_mutants.py tb/verilator/gptp_plane/phc_step.py \
           tb/verilator/milan_dp_gm_steps/gmstep_mutants.py; do
  name="readers-drop-$(echo "$key" | tr / _)"
  cp -p scripts/measure_test_evidence_readers.py "$out/.orig"
  python3 -c "$cut_entry" scripts/measure_test_evidence_readers.py "$key" >"$out/$name.edit" 2>&1
  if cmp -s scripts/measure_test_evidence_readers.py "$out/.orig"; then echo "PROBE-NOT-APPLIED $name" | tee -a "$out/SUMMARY.txt"; continue; fi
  python3 scripts/measure_test_evidence.py --check >"$out/$name.log" 2>&1; rc=$?
  cp -p "$out/.orig" scripts/measure_test_evidence_readers.py
  printf '%s rc=%s %s\n' "$([ $rc -ne 0 ] && echo CAUGHT || echo MISSED)" "$rc" "$name" | tee -a "$out/SUMMARY.txt"
done
# F-INT's publication-census job named in the merged CI page's job list.
probe ci-page-drop-publication-census docs/testing/CI_WORKFLOWS.md \
  'import sys;p=sys.argv[1];s=open(p).read();t="- the mailbox publication census, `publication-census` (#665), when RTL or\n  its tooling changes (below);\n";assert t in s;open(p,"w").write(s.replace(t,""))' \
  python3 scripts/ci_events.py --check
# The new suite moved off worker 3: the landmark must fail the selector selftest.
probe shards-landmark-wrong-owner scripts/suite_shards.py \
  'import sys;p=sys.argv[1];s=open(p).read();t="\"milan_dp_gm_steps\": 3,";assert t in s;open(p,"w").write(s.replace(t,"\"milan_dp_gm_steps\": 2,"))' \
  python3 scripts/suite_shards.py --selftest
git status --porcelain >"$out/final-status.txt"
git diff --stat >>"$out/final-status.txt"
echo "final status lines: $(wc -l <"$out/final-status.txt")" | tee -a "$out/SUMMARY.txt"
