#!/usr/bin/env bash
# Plant real constant copies and non-copies in a disposable archive copy of a
# commit, run the docs checker, and compare with what a copy gate must do.
# Usage: copy_probes_r4.sh <clone> <commit> <scratch-dir> <out-file> [jobs]
# Each line: probe, kind (copy = a real restatement that must fail;
# noncopy = text that is not a restatement; table = a drifted table row),
# checker rc, verdict, first finding. "ESCAPES" marks a real copy that passed.
set -u
SRC=$(cd "$1" && pwd); REV=$2; WORK=$3; OUT=$4; JOBS=${5:-16}
mkdir -p "$WORK"
SELF=$(readlink -f "$0")

if [ "${PROBE:-}" != "" ]; then
  name=$PROBE; kind=$KIND; t="$WORK/p-$name"
  rm -rf "$t"; mkdir -p "$t"; git -C "$SRC" archive "$REV" | tar -x -C "$t"
  I=$t/docs/INTEGRATION.md; H=$t/docs/HDL_DEVELOPER.md; M=$t/docs/MANAGER.md
  add() { printf '\n%s\n' "$1" >> "$H"; }
  addraw() { printf '\n%b' "$1" >> "$H"; }
  case $name in
    control) ;;
    t_drift) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 |/' "$I" ;;
    t_generator_changed) sed -i 's/^SYNC_RTO_MS_C = 375\b/SYNC_RTO_MS_C = 400/' "$t/hdl/ucode/gen_gptp_ucode.py" ;;
    t_missing) sed -i '/^| `CEASE_MS_C` |/d' "$I" ;;
    t_duplicate) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |.*$/&\n&/' "$I" ;;
    t_formatted) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | **375** |/' "$I" ;;
    t_rom_drift) sed -i 's/^| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,021 of 1,024 | 3 |/' "$M" ;;
    c_sync_ms) add "The Sync watch is 375 ms." ;;
    c_sync_nospace) add "The Sync watch is 375ms." ;;
    c_sync_inline_code) add 'The Sync watch is `375 ms`.' ;;
    c_sync_table_cell) add '| Sync watch | 375 ms |' ;;
    c_sync_underscore) add 'The Sync watch is _375 ms_.' ;;
    c_cease_grouped) add "A 300,000 ms countdown." ;;
    c_cease_seconds) add "A 300 s countdown." ;;
    c_cease_5_min) add "A 5 min countdown." ;;
    c_cease_5min) add "A 5min countdown." ;;
    c_cease_5_mins) add "A 5 mins countdown." ;;
    c_cease_5_minutes) add "A 5 minutes countdown." ;;
    c_cease_5_minute_hyph) add "A 5-minute countdown." ;;
    c_cease_5_MIN_caps) add "A 5 MIN countdown." ;;
    c_cease_paren) add "The countdown (5 min) runs." ;;
    c_cease_five_minutes) add "After five minutes it ceases." ;;
    c_cease_Five_minutes) add "Five minutes later it ceases." ;;
    c_cease_five_minute_hyph) add "The five-minute countdown." ;;
    c_cease_five_min) add "A five min countdown." ;;
    c_cease_bold_word) add "After **five minutes** it ceases." ;;
    c_cease_underscore_digit) add "After _5 minutes_ it ceases." ;;
    c_cease_underscore_word) add "After _five minutes_ it ceases." ;;
    c_cease_dash_list) add "- 5 min: cease countdown" ;;
    c_cease_after_comma) add "It retries, then after 1, 5 min it ceases." ;;
    c_step_us) add "A 20 us step threshold." ;;
    c_rate_ppm) add "Inside 200 ppm." ;;
    c_meaning_in_ms) sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout in ms |/' "$I"; add "The Sync watch is 375 ms." ;;
    c_meaning_paren) sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout (ms) |/' "$I"; add "The Sync watch is 375 ms." ;;
    c_meaning_bare) sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout ms |/' "$I"; add "The Sync watch is 375 ms." ;;
    c_after_tilde_fence) addraw '~~~\nsleep 1 s\n~~~\n\nThe Sync watch is 375 ms.\n' ;;
    c_after_mixed_fence) addraw '~~~\n```\n~~~\n\nThe Sync watch is 375 ms.\n' ;;
    c_after_long_tilde_fence) addraw '~~~~\n~~~\n~~~~\n\nThe Sync watch is 375 ms.\n' ;;
    c_after_tilde_info_close) addraw '~~~text\nliteral\n~~~ not a close\nmore\n~~~\n\nThe Sync watch is 375 ms.\n' ;;
    c_after_long_backtick_fence) addraw '````\n```\n````\n\nThe Sync watch is 375 ms.\n' ;;
    c_integration_elsewhere) printf '\nThe Sync watch is 375 ms.\n' >> "$I" ;;
    c_tb_readme) printf '\nThe Sync watch is 375 ms.\n' >> "$t/tb/tsngen/README.md" ;;
    c_decimal_s) add "A 0.375 s Sync watch." ;;
    c_word_ms) add "A 375 milliseconds Sync watch." ;;
    n_decimal_min) add "A 2.5 min hold." ;;
    n_decimal_minutes) add "Wait 0.5 minutes." ;;
    n_twenty_five_minutes) add "A twenty-five minutes soak." ;;
    n_five_minimum) add "At least 5 minimum samples." ;;
    n_25_min) add "A 25 min soak." ;;
    n_fenced_backtick) addraw '```\nsleep 375 ms\n```\n' ;;
    n_fenced_tilde) addraw '~~~\nsleep 375 ms\n~~~\n' ;;
    n_fenced_tilde_info) addraw '~~~sh\nsleep 375 ms\n~~~\n' ;;
    n_history_page) printf '\nThe Sync watch is 375 ms.\n' >> "$t/docs/history/v1/RESOURCE_DELTAS_2026_10.md" ;;
    n_home_section) sed -i 's/^This table is the single home of protocol values\.$/&\n\nThe watch is 375 ms./' "$I" ;;
    n_linked) add 'The [`SYNC_RTO_MS_C`](INTEGRATION.md#protocol-constants) Sync watch.' ;;
    *) echo "unknown probe $name"; exit 2 ;;
  esac
  if [ "$name" != control ] && diff -rq "$t" <(true) >/dev/null 2>&1; then :; fi
  out=$(cd "$t" && python3 -I scripts/check_docs.py 2>&1); rc=$?
  first=$(printf '%s\n' "$out" | grep -m1 -E 'restates|generator|duplicate|not a plain|no protocol|ROM|Shipping|Seeded' | sed 's/^ *//')
  [ -n "$first" ] || first=$(printf '%s\n' "$out" | tail -1)
  case $kind in
    copy|table) if [ $rc -ne 0 ]; then v=caught; else v=ESCAPES; fi ;;
    noncopy) if [ $rc -eq 0 ]; then v=passes; else v=FALSE-FAIL; fi ;;
    *) v=info ;;
  esac
  printf '%-28s %-7s rc=%s %-10s | %s\n' "$name" "$kind" "$rc" "$v" "$first"
  rm -rf "$t"
  exit 0
fi

cat > "$WORK/probe_list" <<'LIST'
control noncopy
t_drift table
t_generator_changed table
t_missing table
t_duplicate table
t_formatted table
t_rom_drift table
c_sync_ms copy
c_sync_nospace copy
c_sync_inline_code copy
c_sync_table_cell copy
c_sync_underscore copy
c_cease_grouped copy
c_cease_seconds copy
c_cease_5_min copy
c_cease_5min copy
c_cease_5_mins copy
c_cease_5_minutes copy
c_cease_5_minute_hyph copy
c_cease_5_MIN_caps copy
c_cease_paren copy
c_cease_five_minutes copy
c_cease_Five_minutes copy
c_cease_five_minute_hyph copy
c_cease_five_min copy
c_cease_bold_word copy
c_cease_underscore_digit copy
c_cease_underscore_word copy
c_cease_dash_list copy
c_cease_after_comma copy
c_step_us copy
c_rate_ppm copy
c_meaning_in_ms copy
c_meaning_paren copy
c_meaning_bare copy
c_after_tilde_fence copy
c_after_mixed_fence copy
c_after_long_tilde_fence copy
c_after_tilde_info_close copy
c_after_long_backtick_fence copy
c_integration_elsewhere copy
c_tb_readme copy
c_decimal_s copy
c_word_ms copy
n_decimal_min noncopy
n_decimal_minutes noncopy
n_twenty_five_minutes noncopy
n_five_minimum noncopy
n_25_min noncopy
n_fenced_backtick noncopy
n_fenced_tilde noncopy
n_fenced_tilde_info noncopy
n_history_page noncopy
n_home_section noncopy
n_linked noncopy
LIST
xargs -P "$JOBS" -L 1 sh -c 'PROBE=$0 KIND=$1 bash "$2" "$3" "$4" "$5" /dev/null' < <(sed "s|\$| $SELF $SRC $REV $WORK|" "$WORK/probe_list") | sort > "$OUT"
cat "$OUT"
