#!/usr/bin/env bash
# Round-4 mutation probes of the census-sentence and table checks. All on
# disposable copies under <scratch>; nothing in the review clone is edited.
# Usage: mutate_r4.sh <packet> <clone> <archived author dir> <scratch>
set -u
P=$1; C=$2; A=$3; S=$4
PAGE=docs/findings/606_FIRST_BIND_MEASUREMENT.md
BODY=$P/receipts/pr_body_at_read_r4.md
rm -rf "$S/mut"; mkdir -p "$S/mut"
chk() { python3 -B "$P/scripts/census_sentence_r4.py" "$1" "$2" "$3" > "$S/mut/out.txt" 2>&1; echo $?; }
report() { name=$1; want=$2; got=$3; extra=$4
  if [ "$got" = "$want" ]; then v=KILLED-OR-EXPECTED; else v=SURVIVED-OR-UNEXPECTED; fi
  [ "$want" = 0 ] && v=$([ "$got" = 0 ] && echo PASSES-AS-EXPECTED || echo UNEXPECTED-FAIL)
  [ "$want" = 1 ] && v=$([ "$got" = 1 ] && echo KILLED || echo SURVIVED)
  echo "$name: rc=$got ($v) $extra"; }

git -C "$C" show HEAD:$PAGE > "$S/mut/page.md"
# control: unmodified page and live body; the one expected FAIL is F7
rc=$(chk "$A" "$S/mut/page.md" "$BODY"); report "C0 control, unmodified page + live body (expect rc 1 from F7 only)" 1 "$rc" "fails: $(grep -c '^FAIL' "$S/mut/out.txt") [$(grep '^FAIL' "$S/mut/out.txt" | cut -c6-60)]"
# positive control: body with only F7's phrase qualified
sed "s/210 ACMP commands all to the peer's input/210 state-changing ACMP commands, all to the peer's input/" "$BODY" > "$S/mut/body_f7.md"
rc=$(chk "$A" "$S/mut/page.md" "$S/mut/body_f7.md"); report "C1 body with F7's phrase qualified" 0 "$rc" ""
# page mutants, checked against the qualified body so only the page can fail
sed 's/^No state-changing command addressed a DUT stream input:.*/No command in the lane addressed a DUT stream input: every state-changing command went to the reference peer, and every AECP command was a GET_ or READ_./' "$S/mut/page.md" > "$S/mut/m1.md"
rc=$(chk "$A" "$S/mut/m1.md" "$S/mut/body_f7.md"); report "M1 page reverted to the round-3 F6 sentence" 1 "$rc" ""
sed 's/228 GET_COUNTERS and 4 READ_DESCRIPTOR/226 GET_COUNTERS and 4 READ_DESCRIPTOR/' "$S/mut/page.md" > "$S/mut/m2.md"
rc=$(chk "$A" "$S/mut/m2.md" "$S/mut/body_f7.md"); report "M2 page GET_COUNTERS 228 -> 226" 1 "$rc" ""
grep -v '^The commands that did address the DUT' "$S/mut/page.md" > "$S/mut/m3.md"
rc=$(chk "$A" "$S/mut/m3.md" "$S/mut/body_f7.md"); report "M3 page reads sentence removed" 1 "$rc" ""
sed 's/the 210 `CONNECT_RX`/the 200 `CONNECT_RX`/' "$S/mut/page.md" > "$S/mut/m4.md"
rc=$(chk "$A" "$S/mut/m4.md" "$S/mut/body_f7.md"); report "M4 page 210 -> 200" 1 "$rc" ""
# archive mutants
rm -rf "$S/mut/arch"; cp -a "$A" "$S/mut/arch"
f=$(ls "$S/mut/arch"/bind/bind-1/*.jsonl | grep -v snapshot | head -1)
echo '{"kind":"transaction","mt":6,"seq":1,"start":0,"end":0,"response":{"status":0,"listener_uid":1,"talker_uid":8,"conn_count":1}}' >> "$f"
rc=$(chk "$S/mut/arch" "$S/mut/page.md" "$S/mut/body_f7.md"); report "M5 archive + one CONNECT_RX to DUT Stream Input 1" 1 "$rc" ""
rm -rf "$S/mut/arch"; cp -a "$A" "$S/mut/arch"
f=$(ls "$S/mut/arch"/bind/bind-1/snapshot-before.jsonl)
echo '{"role":"dut","what":"x-5-1","response":{"cmd":"SET_STREAM_FORMAT","status":"SUCCESS"}}' >> "$f"
rc=$(chk "$S/mut/arch" "$S/mut/page.md" "$S/mut/body_f7.md"); report "M6 archive + one SET_STREAM_FORMAT to DUT Stream Input 1" 1 "$rc" ""
rm -rf "$S/mut/arch"
# table mutant: one per-bind cell changed in a shared scratch clone commit
rm -rf "$S/mut/clone"; git clone -q --shared --no-checkout "$C" "$S/mut/clone"
git -C "$S/mut/clone" checkout -q --detach 5c57927413e0dae279f06a75d2a58e3fec8a2bb0
python3 - "$S/mut/clone/$PAGE" <<'EOF'
import sys, re
p = sys.argv[1]; t = open(p).read().split("\n")
i = next(k for k, l in enumerate(t) if l.startswith("| Bind | Unbound before"))
row = t[i + 2]; cells = row.split("|"); cells[2] = cells[2] + "0"; t[i + 2] = "|".join(cells)
open(p, "w").write("\n".join(t))
EOF
git -C "$S/mut/clone" -c user.name=probe -c user.email=probe@invalid commit -q -am probe
python3 -B "$P/scripts/tables_r2.py" "$S/mut/clone" fb4a1b895 HEAD "$BODY" > "$S/mut/out.txt" 2>&1
n=$(grep -c '  CHANGED' "$S/mut/out.txt"); pb=$(grep 'Per-bind table' "$S/mut/out.txt" | sed 's/.*identical on: //')
if [ "$n" -ge 1 ] && [ "$pb" = "NO PAGE TABLE" ]; then echo "M7 one per-bind table cell changed: KILLED (CHANGED tables $n, PR body per-bind identical on $pb)"; else echo "M7 one per-bind table cell changed: SURVIVED ($n, $pb)"; fi
rm -rf "$S/mut"
