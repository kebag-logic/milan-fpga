#!/usr/bin/env bash
# Round 6's term and #671 controls, re-run unchanged at the checked-out head
# (#671 round 7): the term census, the term matrix, the term views and all
# eighteen #671 controls in full on the three required shapes, one after
# another, at four jobs, under the scratch CPython 3.12.3.
# Usage: host_controls.sh <repo> <r6-scripts> <work> <logdir>
set -u
repo=$1; r6=$2; work=$3; logs=$4
export PATH="$VALIDATION_STORAGE/671-a592/venv312/bin:$PATH" TMPDIR=$VALIDATION_STORAGE/671-a592/r7/tmp
mkdir -p "$logs"
cd "$repo" || exit 2
run() {
  local name=$1; shift
  local start; start=$(date +%s.%N)
  "$@" > "$logs/$name.log" 2>&1
  local rc=$?
  echo "rc=$rc elapsed=$(python3 -c "print(round($(date +%s.%N) - $start, 2))") head=$(git rev-parse HEAD)" >> "$logs/$name.log"
  echo "$name rc=$rc $(date -Is)"
}
run term_census python3 "$r6/term_census.py" "$repo"
run term_matrix python3 "$r6/term_matrix.py" "$repo" "$work/term_matrix" --jobs 4
run term_views python3 "$r6/term_views.py" "$repo" "$work/term_views"
b1="r_omit_verdict r_omit_byte_count r_omit_prefix_crc r_omit_trailer r_digest_with_trailer r_digest_header_only"
b2="restart_at_zero unbounded_retry generation_from_refused_slot verdict_only_agreement r_fill_from_flash r_restage_fail_offers_none"
b3="restage_fail_not_unread r_restage_any_seq r_reattach_goes_live r_judge_four_tries p_restage_unbounded r_restage_four_tries"
for shape in endstation_arty_4x4 endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for b in 1 2 3; do
    eval "labels=\$b$b"
    # shellcheck disable=SC2086
    run "plants_b${b}_$shape" python3 "$r6/plants_full.py" "$repo" "$work/plants_b${b}_$shape" 4 "$shape" $labels
  done
done
