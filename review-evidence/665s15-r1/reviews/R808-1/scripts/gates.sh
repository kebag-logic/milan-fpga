#!/bin/bash
# Focused head gates, each with its own log and rc, run from a clean clone.
# usage: gates.sh CLONE OUTDIR [PARALLEL]
set -u
C=$1 O=$2 PAR=${3:-3}; export O
mkdir -p "$O"
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l)" > "$O/head.txt"
run() { local name=$1; shift; ( "$@" > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc" ) ; }
export -f run
cat > "$O/cmds.txt" <<'EOF'
builder_subset python3 sw/builder/test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged
py_idiom python3 scripts/check_py_idiom.py
soc_options python3 sw/builder/test_soc_options.py
gen_mailbox_check python3 sw/mailbox/gen_mailbox.py --check --crosscheck
gen_mailbox_selftest python3 sw/mailbox/gen_mailbox.py --selftest
ctrl_memory python3 sw/litex/test_ctrl_memory.py
harness_selftest python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
target_32x32 python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir $REVIEWS/665s15-r808-1-packet/scratch/nvm-target-32x32
docs_check python3 scripts/docs_check.py
record_space python3 scripts/check_nvm_record_space.py
baremetal python3 scripts/check_baremetal_only.py --check
builder_32x32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o $REVIEWS/665s15-r808-1-packet/scratch/shape32
entity_shape python3 scripts/check_entity_shape.py
EOF
while read -r name cmd; do
  printf '%s\0%s\0' "$name" "$cmd"
done < "$O/cmds.txt" | xargs -0 -n 2 -P "$PAR" bash -c 'run "$0" bash -c "$1"'
git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD > "$O/diff_check.log" 2>&1; echo $? > "$O/diff_check.rc"
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O/head.txt"
git status --porcelain --untracked-files=all >> "$O/head.txt"
for f in "$O"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done > "$O/summary.txt"
cat "$O/summary.txt"
