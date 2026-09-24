#!/usr/bin/env bash
# R286-1 probe library. Usage: source this file, then call `variant`.
#   TB   : the milan_dp bench directory of a scratch checkout at the head
#   RCPT : receipt directory
#   VERILATOR : pinned Verilator 5.050 (identity recorded in receipts/tool_identity.txt)
set -u
: "${TB:?}" "${RCPT:?}" "${VERILATOR:=verilator}" "${VJOBS:=8}"
# one leg's build line exactly as `make run` issues it, joined onto one line
recipe() { (cd "$TB" && make -n VERILATOR="$VERILATOR" VERILATOR_JOBS="$VJOBS" run 2>/dev/null) \
             | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -E -- "-o Vmilan_dp_$1\$"; }
# variant LEG TAG SRC EXTRA : build leg LEG from bench source SRC (a file in TB)
# into obj_LEG_TAG with extra Verilator arguments EXTRA, run it, keep the log
variant() {
  local leg=$1 tag=$2 src=$3 extra=$4 c
  c=$(recipe "$leg") || { echo "no recipe for $leg"; return 2; }
  if [ "$leg" = sim ]; then c=${c/ -o Vmilan_dp_sim/ --Mdir obj_sim_$tag -o Vmilan_dp_sim}
  else c=${c/--Mdir obj_$leg /--Mdir obj_${leg}_$tag }; fi
  c=${c/ sim_nxn.cpp / $src }
  c=${c/ -o Vmilan_dp_$leg/ $extra -o Vmilan_dp_$leg}
  printf '%s\n' "$c" > "$RCPT/build_${leg}_$tag.cmd"
  (cd "$TB" && eval "$c") > "$RCPT/build_${leg}_$tag.log" 2>&1
  local brc=$?; echo "build $leg $tag rc=$brc" | tee -a "$RCPT/status.txt"
  [ $brc -eq 0 ] || return $brc
  (cd "$TB" && "./obj_${leg}_$tag/Vmilan_dp_$leg") > "$RCPT/run_${leg}_$tag.log" 2>&1
  local rrc=$?; echo "run $leg $tag rc=$rrc $(grep -E 'checks:|checks,' "$RCPT/run_${leg}_$tag.log" | tail -1)" | tee -a "$RCPT/status.txt"
}
LEVER='-CFLAGS -DNOTIFY_REALLOC_TB=1'
ASAN='-CFLAGS "-fsanitize=address -fsanitize-recover=address -fno-omit-frame-pointer -g" -LDFLAGS "-fsanitize=address -fsanitize-recover=address"'
export ASAN_OPTIONS=halt_on_error=0:suppress_equal_pcs=0:detect_leaks=0
