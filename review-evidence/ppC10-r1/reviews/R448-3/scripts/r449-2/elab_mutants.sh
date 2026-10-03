#!/usr/bin/env bash
# R449-2: mutants of KL_pp_nvm_port's MAX_PAYLOAD_P guard against
# tb/nvm_port/elab_bounds.sh, in scratch copies (hdl/ and tb/nvm_port/ only).
# Usage: VERILATOR=<pinned 5.050> elab_mutants.sh <head-tree> <work-dir>
# A case suffixed -noyosys runs with sv2v and yosys removed from PATH.
# Writes <work-dir>/<case>.{diff,log,rc} and one summary line per case.
set -u
src=$1 w=$2; V=${VERILATOR:?set VERILATOR to the pinned 5.050 binary}
F=hdl/packet_engine/KL_pp_nvm_port.sv
[ -n "${CASES-}" ] || rm -rf "$w"; mkdir -p "$w"
# PATH without sv2v and yosys: a directory that holds either is replaced by a
# farm of symlinks to everything else in it.
NOYOSYS_PATH=""; i=0
while IFS= read -r d; do
  [ -n "$d" ] || continue
  if [ -x "$d/sv2v" ] || [ -x "$d/yosys" ]; then
    i=$((i + 1)); farm="$w/.nopath$i"; mkdir -p "$farm"
    for e in "$d"/*; do
      case "${e##*/}" in sv2v|yosys|yosys-*) ;; *) ln -s "$e" "$farm/" ;; esac
    done
    d="$farm"
  fi
  NOYOSYS_PATH="$NOYOSYS_PATH${NOYOSYS_PATH:+:}$d"
done < <(printf '%s\n' "$PATH" | tr ':' '\n')
sub() { # file, old, new: exact, must occur once
  python3 - "$1" "$2" "$3" <<'PY'
import sys
f, old, new = sys.argv[1:4]
s = open(f).read()
assert s.count(old) == 1, (old, s.count(old))
open(f, 'w').write(s.replace(old, new))
PY
}
GUARD_IF='  if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin : g_maxp_check'
BOUND='(1 << $bits(dev_len_o)) - 1 - int'"'"'(HDR_LEN_C)'
FATAL='    $fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",'
run_case() {
  local c=$1 t="$w/$1/tree" p="$PATH"
  mkdir -p "$t/tb"; cp -a "$src/hdl" "$t/"; cp -a "$src/tb/nvm_port" "$t/tb/"
  case "${c%-noyosys}" in
    pristine) ;;
    deleted)  sub "$t/$F" "$GUARD_IF" '  if (0) begin : g_maxp_check' ;;
    bound+1)  sub "$t/$F" "$BOUND" '(1 << $bits(dev_len_o)) - int'"'"'(HDR_LEN_C)' ;;
    ge)       sub "$t/$F" "$GUARD_IF" '  if (MAX_PAYLOAD_P >= MAXP_BOUND_C) begin : g_maxp_check' ;;
    gt-plus8) sub "$t/$F" "$GUARD_IF" '  if (MAX_PAYLOAD_P > MAXP_BOUND_C + 8) begin : g_maxp_check' ;;
    nobound)  sub "$t/$F" 'is above %0d: %0d + it' 'is above the bound: %0d + it'
              sub "$t/$F" '           MAX_PAYLOAD_P, MAXP_BOUND_C, HDR_LEN_C);' '           MAX_PAYLOAD_P, HDR_LEN_C);' ;;
    initial)  sub "$t/$F" "$GUARD_IF" '  initial if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin : g_maxp_check' ;;
    error)    sub "$t/$F" "$FATAL" '    $error("KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",' ;;
    warning)  sub "$t/$F" "$FATAL" '    $warning("KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",' ;;
    info)     sub "$t/$F" "$FATAL" '    $info("KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",' ;;
    fatal0)   sub "$t/$F" "$FATAL" '    $fatal(0, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: %0d + it overflows dev_len_o",' ;;
    hdr10)    sub "$t/$F" "localparam logic [15:0] HDR_LEN_C  = 16'd8;" "localparam logic [15:0] HDR_LEN_C  = 16'd10;" ;;
    *) echo "unknown case $c" >&2; return 2 ;;
  esac
  [ "$c" != "${c%-noyosys}" ] && p="$NOYOSYS_PATH"
  diff -u "$src/$F" "$t/$F" > "$w/$c.diff"
  ( cd "$t/tb/nvm_port" && PATH="$p" VERILATOR=$V ./elab_bounds.sh ) > "$w/$c.log" 2>&1
  echo $? > "$w/$c.rc"
  echo "$c rc=$(cat "$w/$c.rc") $(grep -cE '^(GUARD|ELAB|YOSYS) FAIL' "$w/$c.log") FAIL line(s); $(grep -m1 -E '^(GUARD|ELAB|YOSYS) FAIL' "$w/$c.log" | cut -c1-120)"
  rm -rf "$w/$c"
}
for c in ${CASES:-pristine pristine-noyosys deleted bound+1 ge gt-plus8 nobound initial \
         error error-noyosys warning warning-noyosys info info-noyosys fatal0 hdr10}; do
  run_case "$c" &
done
wait
