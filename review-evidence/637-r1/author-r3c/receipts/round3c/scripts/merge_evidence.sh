#!/usr/bin/env bash
# the merge's evidence: parents, conflicted files, each side's diff into the merge for those files, and the
# datapath composition check (merge minus one parent equals the other parent's own change, both ways)
# usage: merge_evidence.sh <repo> <merge> <outdir>
set -u
cd "$1" || exit 2
m=$2; out=$3; mkdir -p "$out"
o=$(git rev-parse "$m^1"); t=$(git rev-parse "$m^2"); b=$(git merge-base "$o" "$t")
f=hdl/milan/milan_datapath.sv
{
  echo "merge $(git rev-parse "$m")"; echo "ours (lane) $o"; echo "theirs (dev) $t"; echo "merge-base $b"
  echo "subject: $(git log -1 --format=%s "$m")"
  echo "files both sides changed:"; comm -12 <(git diff --name-only "$b" "$o" | sort) <(git diff --name-only "$b" "$t" | sort)
  echo "gitlinks changed by dev: $(git diff --raw "$b" "$t" | grep -c ' 160000 ' || true)"
  echo "datapath: lines changed by dev ($b..$t) vs lines the merge adds over ours:"
  a=$(git diff "$b" "$t" -- $f | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
  c=$(git diff "$o" "$m" -- $f | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
  echo "  $a  $c  $([ "$a" = "$c" ] && echo EQUAL || echo DIFFER)"
  echo "datapath: lines changed by the lane ($b..$o) vs lines the merge adds over dev:"
  a=$(git diff "$b" "$o" -- $f | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
  c=$(git diff "$t" "$m" -- $f | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
  echo "  $a  $c  $([ "$a" = "$c" ] && echo EQUAL || echo DIFFER)"
  echo "stopped_i wiring at the merge:"; git grep -n 'stopped_i' "$m" -- $f
  echo "hdl/syn/constraints changed by the merge over ours:"; git diff --stat "$o" "$m" -- hdl syn constraints
  echo "hdl/syn/constraints changed by the merge over dev:"; git diff --stat "$t" "$m" -- hdl syn constraints
} > "$out/merge-check.txt" 2>&1
for p in sim_nxn.cpp dynmap_probes.vlt README.md; do
  git diff "$t" "$m" -- "tb/verilator/milan_dp/$p" > "$out/vs-dev-$p.diff"
  git diff "$o" "$m" -- "tb/verilator/milan_dp/$p" > "$out/vs-lane-$p.diff"
done
git show --cc --format='%H %s' "$m" -- tb/verilator/milan_dp > "$out/merge-cc.diff"
