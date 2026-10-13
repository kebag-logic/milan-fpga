#!/usr/bin/env bash
# R624-12: re-run every earlier control runner, self-probe set, parser/reader/layer audit and review probe
# against the regenerated check and the candidate page, through the packet's own dispatcher, concurrently.
# usage: run_validation_all.sh R11_PACKET PREV_PACKET_COPY CAND_FIXTURE SOURCE_REPO VAL_DIR PARSER_PY
set -uo pipefail
R11=$1 PREV=$2 CAND=$3 SRC=$4 VAL=$5 PY=$6
F=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
export PYTHONDONTWRITEBYTECODE=1
export GIT_DIR
GIT_DIR=$(git -C "$SRC" rev-parse --absolute-git-dir)
mkdir -p "$VAL/logs"
for m in controls-3 controls-4 controls-5 controls-6 controls-7 controls-8 controls-9 controls-10 \
         self parser reader layers probes-0 probes-1 probes-2; do
  ( rc=0; timeout 590s "$PY" -I -B "$R11/tools/run_validation.py" "$m" "$PREV" "$CAND" "$SRC" "$VAL/$m" \
      >"$VAL/logs/$m.log" 2>&1 || rc=$?; echo "$rc" >"$VAL/logs/$m.rc" ) &
done
# the three relocated probe copies, with the argv their originals take in r11_probe_reruns.py
CHK=$VAL/packet/tools/check_b16_figures.py PACK=$VAL/packet
rel() { # name script args...
  local n=$1 s=$2; shift 2
  mkdir -p "$VAL/rel-$n/scratch" "$VAL/rel-$n/work"
  ( rc=0; timeout 590s "$PY" -I -B "$R11/tools/relocated/$s" "$@" >"$VAL/logs/rel-$n.log" 2>&1 || rc=$?
    echo "$rc" >"$VAL/logs/rel-$n.rc" ) &
}
rel r624-5-row3200 probe_row3200.py "$CAND" "$PACK" "$VAL/rel-r624-5-row3200/scratch" "$VAL/rel-r624-5-row3200/out.json"
rel r624-6-row3200-polls probe_row3200_polls.py "$CHK" "$CAND/$F" "$PACK" "$CAND" "$VAL/rel-r624-6-row3200-polls/work" "$VAL/rel-r624-6-row3200-polls/out.json"
rel r624-6-escapes probe_r624_6_escapes.py "$CHK" "$CAND/$F" "$PACK" "$CAND" "$VAL/rel-r624-6-escapes/scratch" "$VAL/rel-r624-6-escapes/out.json"
wait
for f in "$VAL"/logs/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
