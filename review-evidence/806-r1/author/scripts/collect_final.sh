#!/usr/bin/env bash
# collect_final.sh: copy the final-head receipts (sweep, rtl-fast, docs, static, Yosys at f99405af; the physical leg
# at cf3ef596, whose inputs equal the head's) into receipts/final-f99405af/, host paths redacted, large logs by digest.
set -u
S=$(cd "$(dirname "$0")" && pwd); X=$VALIDATION_STORAGE/scratch/806-a701; R=$X/r; H=f99405af
O=$(dirname "$S")/receipts/final-$H
mkdir -p "$O"/sweep "$O"/rtl-fast "$O"/docs "$O"/static "$O"/yosys "$O"/physical-cf3ef596
for k in 0 1 2 3; do
  cp "$X/sweep-$H/shard-$k/spec/complete.json" "$O/sweep/shard-$k-complete.json"
  python3 "$S/copy_receipts.py" "$O/sweep" "$X/sweep-$H/shard-$k/spec/01.log"
  mv "$O/sweep/01.log" "$O/sweep/shard-$k-driver.log"
done
python3 "$S/copy_receipts.py" "$O/sweep" "$X/sweep-$H/tally-quiet.out" "$X/sweep-$H/tally-per-suite.txt" --digest "$X/sweep-$H/union"
python3 "$S/copy_receipts.py" "$O/rtl-fast" "$R/rtlfast-$H/run.out" "$R/rtlfast-$H/table.txt" "$R/rtlfast-$H/base.txt" \
  "$R/rtlfast-$H/run/receipts.json" --digest "$R/rtlfast-$H/run/logs"
D=$X/docs/docs-$H
python3 "$S/copy_receipts.py" "$O/docs" "$D/all.out" "$D/all.rc" "$D/leg1-litex.out" "$D/leg1-litex.rc" "$D/md312.out" \
  "$D/md312.rc" "$D/nogit_summary.txt" "$D/dev-ref.txt"
python3 "$S/copy_receipts.py" "$O/static" "$R/static-$H/table.txt" "$R/static-$H/head.txt" "$R/static-$H/submodules.txt" \
  "$R/static-$H/clone-status-after.txt" "$R/static-$H/builder_bank.log" "$R/static-$H/lint.log" "$R/static-$H/xvlog.log" \
  "$R/static-$H/cpp_idiom.log" "$R/static-$H/py_idiom.log" "$R/static-$H/port_contracts.log" "$R/static-$H/gptp_docs.log" \
  "$R/static-$H/submodule_docs.log" "$R/static-$H/rom_digests_record.log" "$R/static-$H/docs_check.log"
python3 "$S/copy_receipts.py" "$O/yosys" "$R/yosys-$H/head.txt" "$R/yosys-$H/versions.txt" "$R/yosys-$H/seconds.txt" \
  "$R/yosys-$H/run.rc" "$R/yosys-$H/clone-status-after.txt" "$R/yosys-$H/run.log"
P=$R/gptp-cf3ef596
python3 "$S/copy_receipts.py" "$O/physical-cf3ef596" "$P/table.txt" "$P/tally.out" "$P/head.txt" "$P/selection.txt" \
  "$P/deadline.txt" "$P/clone-status-after.txt" "$P/logs/milan_dp_gptp.log"
du -sh "$O"
