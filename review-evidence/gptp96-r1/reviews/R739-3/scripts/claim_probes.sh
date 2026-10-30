#!/usr/bin/env bash
# Plant one defect per documented gate claim in a disposable archive copy of
# the reviewed tree and run the docs checker on it.
# Usage: claim_probes.sh <clone> <scratch-dir> <out-file> [jobs]
# Each output line: probe, what the documentation predicts, checker rc,
# first finding. "doc=fail" means the page says make docs rejects the plant;
# "doc=pass" means the page says it passes; "doc=-" means the page is silent.
set -u
SRC=$(cd "$1" && pwd); WORK=$2; OUT=$3; JOBS=${4:-16}
mkdir -p "$WORK"
SELF=$(readlink -f "$0")

if [ "${PROBE:-}" != "" ]; then
  name=$PROBE; doc=$DOC; t="$WORK/p-$name"
  rm -rf "$t"; mkdir -p "$t"; git -C "$SRC" archive HEAD | tar -x -C "$t"
  I=$t/docs/INTEGRATION.md; H=$t/docs/HDL_DEVELOPER.md; M=$t/docs/MANAGER.md
  add() { printf '\n%s\n' "$1" >> "$H"; }
  case $name in
    control) ;;
    k_drift) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 |/' "$I" ;;
    k_missing) sed -i '/^| `P1_C` | 248 |/d' "$I" ;;
    k_duplicate) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |.*$/&\n&/' "$I" ;;
    k_formatted) sed -i 's/^| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | **375** |/' "$I" ;;
    k_generator_changed) sed -i 's/^NPD_HI_C = 800 /NPD_HI_C = 900 /' "$t/hdl/ucode/gen_gptp_ucode.py" ;;
    u_meaning_comma_control) add "The watch is 375 ms." ;;
    u_meaning_ends_in_ms) sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout in ms |/' "$I"; add "The watch is 375 ms." ;;
    u_meaning_paren) sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout (ms) |/' "$I"; add "The watch is 375 ms." ;;
    u_unitless_ordinal) add "The fifth consecutive loss clears asCapable." ;;
    u_unitless_depth) add "The ROM holds 1,024 words." ;;
    i_space) add "The watch is 375 ms." ;;
    i_nospace) add "The watch is 375ms." ;;
    i_hyphen) add "A 375-ms watch." ;;
    i_grouped) add "A 300,000 ms countdown." ;;
    i_ungrouped_ns) add "A 20000 ns step." ;;
    i_ppm) add "Inside 200 ppm." ;;
    s_seconds) add "A 300 s countdown." ;;
    s_us) add "A 20 us step." ;;
    s_micro_sign) add "A 100 µs step." ;;
    s_greek_mu) add "A 100 μs step." ;;
    m_digits) add "A 5 min countdown." ;;
    m_digits_minutes) add "A 5 minutes countdown." ;;
    m_word) add "After five minutes it ceases." ;;
    m_word_hyphen) add "The five-minute countdown." ;;
    m_nospace) add "A 5min countdown." ;;
    m_word_min) add "A five min countdown." ;;
    x_fenced_backtick) printf '\n```\nsleep 375 ms\n```\n' >> "$H" ;;
    x_fenced_tilde) printf '\n~~~\nsleep 375 ms\n~~~\n' >> "$H" ;;
    x_home_section) sed -i 's/^This table is the single home of protocol values\.$/&\n\nThe watch is 375 ms./' "$I" ;;
    x_integration_elsewhere) printf '\nThe watch is 375 ms.\n' >> "$I" ;;
    x_history_page) printf '\nThe watch is 375 ms.\n' >> "$t/docs/history/v1/RESOURCE_DELTAS_2026_10.md" ;;
    x_tb_readme) printf '\nThe watch is 375 ms.\n' >> "$t/tb/tsngen/README.md" ;;
    x_inline_code) add 'The watch is `375 ms`.' ;;
    x_html_comment) add '<!-- The watch is 375 ms. -->' ;;
    d_decimal_s) add "A 0.375 s watch." ;;
    d_decimal_ms) add "A 375.0 ms watch." ;;
    d_word_ms) add "A 375 milliseconds watch." ;;
    d_word_us) add "A 20 microseconds step." ;;
    d_decimal_min) add "A 2.5 min hold." ;;
    d_decimal_minutes) add "A 7.5 minutes hold." ;;
    f_twenty_five_minutes) add "A twenty-five minutes soak." ;;
    f_five_minimum) add "At least 5 minimum samples." ;;
    f_twenty_five_min) add "A 25 min soak." ;;
    r_shipping_drift) sed -i 's/^| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,021 of 1,024 | 3 |/' "$M" ;;
    r_seeded_drift) sed -i 's/^| Seeded regression | 1,023 of 1,024 | 1 |/| Seeded regression | 1,022 of 1,024 | 2 |/' "$M" ;;
    r_seeded_duplicate) sed -i 's/^| Seeded regression | 1,023 of 1,024 | 1 |/&\n&/' "$M" ;;
    *) echo "unknown probe $name"; exit 2 ;;
  esac
  if [ "$name" != control ] && diff -rq -x .git "$SRC" "$t" > /dev/null 2>&1; then
    printf '%-26s doc=%-4s PLANT MISSED\n' "$name" "$doc"; exit 0
  fi
  out=$(cd "$t" && python3 scripts/check_docs.py 2>&1); rc=$?
  first=$(printf '%s\n' "$out" | sed -n 2p | sed 's/^ *//'); [ -n "$first" ] || first=$(printf '%s\n' "$out" | head -1)
  if [ "$doc" = fail ] && [ $rc -ne 1 ]; then v=CONTRADICTS; elif [ "$doc" = pass ] && [ $rc -ne 0 ]; then v=CONTRADICTS; else v=agrees; fi
  [ "$doc" = - ] && v=info
  printf '%-26s doc=%-4s rc=%s %-11s | %s\n' "$name" "$doc" "$rc" "$v" "$first"
  rm -rf "$t"
  exit 0
fi

cat > "$WORK/probe_list" <<'EOF'
control pass
k_drift fail
k_missing fail
k_duplicate fail
k_formatted fail
k_generator_changed fail
u_meaning_comma_control fail
u_meaning_ends_in_ms fail
u_meaning_paren pass
u_unitless_ordinal pass
u_unitless_depth pass
i_space fail
i_nospace fail
i_hyphen fail
i_grouped fail
i_ungrouped_ns fail
i_ppm fail
s_seconds fail
s_us fail
s_micro_sign fail
s_greek_mu fail
m_digits fail
m_digits_minutes fail
m_word fail
m_word_hyphen fail
m_nospace -
m_word_min -
x_fenced_backtick pass
x_fenced_tilde pass
x_home_section pass
x_integration_elsewhere fail
x_history_page pass
x_tb_readme fail
x_inline_code fail
x_html_comment -
d_decimal_s pass
d_decimal_ms pass
d_word_ms pass
d_word_us pass
d_decimal_min pass
d_decimal_minutes pass
f_twenty_five_minutes -
f_five_minimum -
f_twenty_five_min -
r_shipping_drift fail
r_seeded_drift fail
r_seeded_duplicate fail
EOF
xargs -P "$JOBS" -L 1 sh -c 'PROBE=$0 DOC=$1 bash "$2" "$3" "$4" /dev/null' < <(sed "s|\$| $SELF $SRC $WORK|" "$WORK/probe_list") | sort > "$OUT"
cat "$OUT"
