#!/usr/bin/env bash
# R502-2 (PR #164, issue #42): the reviewer's commands, as run. Portable:
#   REPO   = a clone of the processor repository at the exact head
#   PACKET = an output directory (receipts/, scratch/)
#   VL     = the pinned Verilator 5.050 front end
# Independent jobs run concurrently, each with its own log and rc file; the
# caller waits on the rc files. At most 16 compiler jobs together.
set -euo pipefail
REPO=${REPO:?}; PACKET=${PACKET:?}; VL=${VL:?}
HEAD=ad670a71b4d2f38f59672d51d8309d59ffed0808
S=$PACKET/scratch; L=$S/logs; W=$PACKET/scripts/vl_jcap.sh
mkdir -p "$S/head" "$S/probe" "$S/plant" "$S/tmp" "$L"
for t in head probe plant; do git -C "$REPO" archive "$HEAD" | tar -x -C "$S/$t"; done
export VL_REAL=$VL

# print-only probe of section DN's clocks
python3 "$PACKET/scripts/probe_dn_clocks.py" "$S/probe"
(cd "$S/probe/tb/pp_top" && VL_J=4 make gsi-build VERILATOR="$W" && ./obj_dir/Vpp_top_sim --domain-notify-only) \
  > "$L/probe.log" 2>&1; echo $? > "$L/probe.rc"

launch() { local name=$1 dir=$2; shift 2
  setsid nohup bash -c "cd '$dir' && /usr/bin/time -v $* > '$L/$name.log' 2>&1; echo \$? > '$L/$name.rc'" \
    >/dev/null 2>&1 </dev/null & }
# suites fed by the two merges (#134: srp_top, srp_stream_fsms; #22: originator, rx_validator)
for s in srp_stream_fsms srp_top originator rx_validator; do
  launch "$s" "$S/head/tb/$s" env VL_J=2 make VERILATOR="$W"; done
# the full pp_top suite (six builds) and the notify campaign
launch pp_top "$S/head/tb/pp_top" env VL_J=3 make VERILATOR="$W"
launch notify_mutants "$S/head" env TMPDIR="$S/tmp" VL_J=3 python3 tb/pp_top/notify_mutants.py \
  --output "$S/nm_out" --verilator "$W" --jobs 4
# reviewer-owned controls (after srp_top frees its slots)
launch extra_dn "$S" env VL_J=2 python3 "$PACKET/scripts/extra_dn_mutants.py" "$S/plant" "$S/xm_out" "$W" 2

# static and docs checks (foreground)
python3 "$PACKET/scripts/plant_check.py" "$S/plant"
git clone -q --no-hardlinks "$REPO" "$S/docsclone"; git -C "$S/docsclone" checkout -q --detach "$HEAD"
(cd "$S/docsclone" && for t in links matrix modmatrix params ids figures stale; do make "$t"; done \
  && python3 scripts/gen_matrix.py --check)
git -C "$REPO" diff --check e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8 "$HEAD"
# after the campaign: README record vs observed failing sets
# python3 "$PACKET/scripts/record_vs_results.py" "$REPO/tb/pp_top/README.md" "$S/nm_out/results.json"
