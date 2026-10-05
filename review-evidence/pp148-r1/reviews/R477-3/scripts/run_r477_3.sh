#!/bin/sh
# R477-3 reviewer probes, as run. Usage: run_r477_3.sh CLONE PACKET PINNED_VERILATOR
# CLONE is a clone holding 07b1469d, 356c1bba and 80b3c1b2; nothing is written to it.
# Every tree is a `git archive` extraction under PACKET/scratch.
set -eu
CLONE=$1 PACKET=$2 PINNED=$3
S=$PACKET/scratch R=$PACKET/receipts
mkdir -p "$S/bin" "$S/tmp" "$R"
ln -sf "$PINNED" "$S/bin/verilator"
PATH=$S/bin:$PATH; export PATH
verilator --version

for pair in head:80b3c1b223aaad05f428164cd56595a4c1187509 \
            base356:356c1bbad2e9838659b433736040acf0cc4abf3e \
            base07:07b1469ddf1e2a54e4a42cac06c41f084ecffd6c; do
  t=${pair%%:*} rev=${pair#*:}
  rm -rf "${S:?}/$t"; mkdir -p "$S/$t"
  git -C "$CLONE" archive "$rev" | tar -x -C "$S/$t"
  # plant check: every .patch arm and every inline text arm
  rc=0; python3 "$PACKET/scripts/plant_check.py" "$S/$t" > "$R/plant_check-$t.log" 2>&1 || rc=$?
  echo "$t rc=$rc" > "$R/plant_check-$t.rc"
done

# the refreshed arm alone, at head and at base, concurrently
for t in head base07; do
  ( cd "$S/$t/tb/pp_top" && rc=0 && TMPDIR=$S/tmp python3 ctr_mutants.py \
      --output "$R/ctr-one-window-$t" --only ctr-notify-one-window --jobs 2 \
      > "$R/ctr-one-window-$t.log" 2>&1 || rc=$?; echo "$rc" > "$R/ctr-one-window-$t.rc" ) &
done
wait

# the whole ctr campaign at head
rc=0; (cd "$S/head/tb/pp_top" && TMPDIR=$S/tmp python3 ctr_mutants.py \
    --output "$R/ctr-full-head" --jobs 9 > "$R/ctr-full-head.log" 2>&1) || rc=$?
echo "$rc" > "$R/ctr-full-head.rc"

# documentation gate at head
rc=0; make -C "$S/head" check > "$R/make-check-head.log" 2>&1 || rc=$?
echo "$rc" > "$R/make-check-head.rc"

# compare with the published records (fetched beforehand into scratch)
for t in head base; do
  [ -f "$S/pub-r1c-$t-camp-ctr.log" ] || continue
  echo "== $t"; diff "$S/pub-r1c-$t-camp-ctr.log" "$R/ctr-full-head.log" >/dev/null 2>&1 \
    && echo "full log identical" || echo "full log differs (expected for base)"
done
