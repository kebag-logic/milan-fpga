#!/usr/bin/env bash
# R354-3 replay of the round-1 guard-narrowing mutants at the reviewed head.
# Usage: mutants_round1_replay.sh <repo-root> <scratch-dir> <python-with-litex>
# S1-S4: the SoC clock guard exempts --no-milan, --full, --board arty or
#        --with-spiflash. B3: the builder clock guard applies only to
#        flashboot baremetal. My own implementations of the published
#        descriptions; each runs on a fresh copy (with .git) of the head tree.
set -u
repo=$1 scratch=$2 py=$3
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$scratch"

fresh() {
    rm -rf "$scratch/$1"
    rsync -a --exclude=__pycache__ "$repo/" "$scratch/$1/"
    printf '%s\n' "$scratch/$1"
}
patch_once() {  # patch_once <file> <old> <new>
    "$py" - "$@" <<'EOF'
import sys; p, o, n = sys.argv[1:]; s = open(p).read(); assert s.count(o) == 1, p; open(p, "w").write(s.replace(o, n))
EOF
}
run_arm() {  # run_arm <tree> <function>
    (cd "$1/sw/builder" && "$py" -c "
import sys; sys.path.insert(0, '.')
import test_clock_contract as m
getattr(m, sys.argv[1])()" "$2")
}
verdict() {
    local got=KILLED; [ "$2" -eq 0 ] && got=SURVIVED
    local ok=MATCH; [ "$got" = KILLED ] || ok=MISMATCH
    printf 'PROBE %-52s expected=KILLED got=%-8s %s\n' "$1" "$got" "$ok"
}

guard='    if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:'
for spec in "S1 not args.no_milan" "S2 not args.full" "S3 args.board != \"arty\"" "S4 not args.with_spiflash"; do
    id=${spec%% *} cond=${spec#* }
    t=$(fresh "$id")
    patch_once "$t/sw/litex/milan_soc.py" "$guard" \
        "    if $cond and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:"
    run_arm "$t" test_soc_clock_contract > "$scratch/$id.log" 2>&1
    verdict "$id SoC guard exempts: $cond" $?
done

t=$(fresh B3)
patch_once "$t/sw/builder/endstation_builder.py" \
    '        if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:' \
    '        if cons["flashboot"] == "baremetal" and cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:'
run_arm "$t" test_baremetal_clock_contract > "$scratch/B3.log" 2>&1
verdict "B3 builder guard only for flashboot baremetal" $?

t=$(fresh ctl)
run_arm "$t" test_soc_clock_contract > "$scratch/ctl_soc.log" 2>&1; rc1=$?
run_arm "$t" test_baremetal_clock_contract > "$scratch/ctl_builder.log" 2>&1; rc2=$?
[ $rc1 -eq 0 ] && [ $rc2 -eq 0 ] && echo "PROBE CTL unmutated SoC and builder arms pass                      MATCH" \
                                  || echo "PROBE CTL unmutated SoC and builder arms pass (rc $rc1/$rc2)       MISMATCH"
