#!/usr/bin/env bash
# Disposable mutation probes on a throwaway clone of the candidate: each plants
# one composition-shaped defect in a file this PR or its predecessor touched,
# commits it locally, and records which gate sees it. Usage:
#   probes.sh <probe-clone> <python-with-markdown-lock> <receipt-dir>
set -u
P=$1; PY=$2; OUT=$3; mkdir -p "$OUT"; : > "$OUT/probes.txt"
HEAD=86726d5e60ced4f7baad6a042890b44abf7d76ed
DEV=ea3fb38877842f223afea97e3bd72a10500455c9
cd "$P" || exit 2
G() { git -c user.name=probe -c user.email=probe@invalid "$@"; }
probe() { id=$1; desc=$2; edit=$3; shift 3
  G checkout -q --detach "$HEAD"; G reset -q --hard "$HEAD"
  eval "$edit"; G commit -qam "probe $id" >/dev/null 2>&1
  n=0; for gate in "$@"; do n=$((n+1))
    eval "$gate" > "$OUT/$id.g$n.log" 2>&1; rc=$?
    printf '%s | %s | rc=%s | %s\n' "$id" "$desc" "$rc" "$gate" | tee -a "$OUT/probes.txt"
  done; }
R=docs/findings/README.md; F=docs/findings/117_AUDIO_CONTINUITY.md
EM=$(printf '\xe2\x80\x94')
probe P0 "control: unmodified candidate" "true" \
  "$PY scripts/check_em_dash.py --base $DEV" "$PY scripts/docs_check.py" "$PY scripts/check_doc_paths.py" "$PY scripts/gen_toc.py --verify-anchors"
probe P1 "em dash planted in the composed 117 index row" \
  "sed -i '/117_AUDIO_CONTINUITY.md/s/Integrity PASS/Integrity $EM PASS/' $R" \
  "$PY scripts/check_em_dash.py --base $DEV"
probe P2 "117 index row link target renamed to a missing file" \
  "sed -i 's/(117_AUDIO_CONTINUITY.md)/(117_AUDIO_CONTINUITY_X.md)/' $R" \
  "$PY scripts/docs_check.py" "$PY scripts/check_doc_paths.py" "$PY scripts/gen_toc.py --verify-anchors"
probe P3 "117 page cross-page anchor to 451_TDM8_FIRST_LIGHT broken" \
  "sed -i 's/451_TDM8_FIRST_LIGHT.md#method/451_TDM8_FIRST_LIGHT.md#no-such-anchor/' $F" \
  "$PY scripts/docs_check.py" "$PY scripts/check_doc_paths.py" "$PY scripts/gen_toc.py --verify-anchors"
probe P4 "bad resolution: predecessor 451 timing row dropped from index" \
  "sed -i '/451_TDM8_TIMING_SOC_BOARD.md/d' $R" \
  "$PY scripts/docs_check.py" "$PY scripts/check_doc_paths.py" "$PY scripts/gen_toc.py --check"
probe P5 "bad resolution: 117 row duplicated" \
  "sed -i '/117_AUDIO_CONTINUITY.md/p' $R" \
  "$PY scripts/docs_check.py" "$PY scripts/check_doc_style.py"
G checkout -q --detach "$HEAD"; G reset -q --hard "$HEAD"
echo "restored $(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" | tee -a "$OUT/probes.txt"
