#!/usr/bin/env bash
# The command sequence behind this packet's receipts, in execution order.
# REPO is the detached candidate clone, PKT this packet, TOOLBIN a directory
# holding the pinned-tool wrappers (python3 with the hash-pinned Markdown
# lock; Verilator 5.050). Every command ran in the foreground.
set -uo pipefail
REPO=${REPO:?candidate clone}; PKT=${PKT:?packet dir}; TOOLBIN=${TOOLBIN:?wrappers}
export PATH="$TOOLBIN:$PATH"
cd "$REPO"

# 1. Lineage, overlap and delta preservation (receipts/lineage.txt,
#    receipts/{pr,pred,dev,overlap}_files.txt).
B=$(git merge-base 5c78ce2e 0e26e0ac)
git diff --name-only 5c78ce2e ddf8151c | sort > "$PKT/receipts/pr_files.txt"
git diff --name-only "$B" 0e26e0ac | sort > "$PKT/receipts/pred_files.txt"
comm -12 "$PKT/receipts/pr_files.txt" "$PKT/receipts/pred_files.txt" > "$PKT/receipts/overlap_files.txt"
for f in $(cat "$PKT/receipts/pr_files.txt"); do
  a=$(git diff 5c78ce2e ddf8151c -- "$f" | grep '^[+-][^+-]' | sort | sha1sum)
  b=$(git diff 0e26e0ac 551e4b5d -- "$f" | grep '^[+-][^+-]' | sort | sha1sum)
  [ "$a" = "$b" ] || echo "PR DELTA DIFFERS: $f"
done
for f in $(git diff --name-only 5c78ce2e 0e26e0ac); do
  a=$(git diff 5c78ce2e 0e26e0ac -- "$f" | grep '^[+-][^+-]' | sort | sha1sum)
  b=$(git diff ddf8151c 551e4b5d -- "$f" | grep '^[+-][^+-]' | sort | sha1sum)
  [ "$a" = "$b" ] || echo "TRAIN DELTA DIFFERS: $f"
done

# 2. Static and documentation gates (receipts/static/).
PARENT=0e26e0ac07abf1043ac2712fe39f92de0b34f2dd DEV=5c78ce2e9d831e588e759b696ed549804327e4d8 \
  "$PKT/scripts/run_static_gates.sh" . "$PKT/receipts/static"
# no-git mode: a git-archive extraction with empty submodule directories
N="$PKT/scratch/nogit"; rm -rf "$N"; mkdir -p "$N"
git archive --format=tar HEAD | tar -x -C "$N"
for s in external gptp-processor protocol-processor third_party/verilog-axis; do mkdir -p "$N/$s"; done
( cd "$N" && python3 scripts/docs_check.py; echo "exit $?" ) > "$PKT/receipts/static/nogit_docs_check.log" 2>&1
( cd "$N" && python3 scripts/check_feature_status.py; echo "exit $?" ) > "$PKT/receipts/static/nogit_feature_status.log" 2>&1
git diff --check 0e26e0ac HEAD; git diff --check 5c78ce2e HEAD

# 3. ROM digest ledger (receipts/rom_digests.log).
"$PKT/scripts/check_rom_digests.sh" . "$PKT/scratch/rom"

# 4. Composed datapath front ends (receipts/sv2v_*, receipts/yosys_hierarchy*).
#    sv2v --top=milan_datapath over `syn/yosys/ooc.sh --emit-dp` with ooc.sh's
#    INC flags, then `yosys read_verilog -sv; hierarchy -check; stat`.

# 5. milan_dp legs on the candidate (receipts/dynamic/).
( cd tb/verilator/milan_dp && VERILATOR_JOBS=8 make -s gmstep-build \
  && ./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0 )
python3 "$PKT/scripts/run_one_control.py" . gmstep anchors
python3 "$PKT/scripts/run_one_control.py" . crflic anchors
# gmstep campaign: positives for both legs and all 14 controls, 4 at a time,
# VERILATOR_JOBS=2 each (8 jobs), each planted copy under $PKT/scratch.
{ echo "positive gmstep"; echo "positive option-off"; for i in $(seq 0 13); do echo "control $i"; done; } |
  VERILATOR_JOBS=2 xargs -P 4 -L 1 sh -c 'WORK='"$PKT"'/scratch/gm_$0_$1 python3 '"$PKT"'/scripts/run_one_control.py . gmstep "$0" "$1"'
( cd tb/verilator/milan_dp && VERILATOR_JOBS=8 make -s crflic-build \
  && ./obj_crflic/Vmilan_dp_crflic && ./obj_crflic/Vmilan_dp_crflic --unwarmed-refusal )
{ echo "positive x"; for i in 0 1 2 3 4 5; do echo "mutant $i"; done; } |
  VERILATOR_JOBS=2 xargs -P 4 -L 1 sh -c 'WORK='"$PKT"'/scratch/cl_$0_$1 python3 '"$PKT"'/scripts/run_one_control.py . crflic "$0" "$1"'
( cd tb/verilator/milan_dp && VERILATOR_JOBS=4 make -s gptp )
( cd tb/verilator/milan_dp && VERILATOR_JOBS=4 make -s gptp-lat )

# 6. Remove this run's ignored build products, then prove the restore.
"$PKT/scripts/verify_restore.sh" . 551e4b5dfa8ac7ec68a3161c95d4000eb6337396 bea28456ef036cb8cd8c94a800b1b6921ab6108c
