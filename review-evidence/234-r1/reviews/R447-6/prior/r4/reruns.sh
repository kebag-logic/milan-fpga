#!/usr/bin/env bash
# Rerun this reviewer's round-1 to round-3 probes, unchanged (copies under prior/), at the checkout's head.
# Usage: reruns.sh <repo checkout> <validation storage root holding A/ and B/> <evidence dir> <scratch> <out> <light|heavy>
# light: the single-process probes, run one after another; heavy: the three mutant campaigns, one after another.
set -u
repo=$1 store=$2 ev=$3 scratch=$4 out=$5 mode=$6
here=$(cd "$(dirname "$0")" && pwd)
p=$here/prior
mkdir -p "$out" "$scratch"
run() { local name=$1; shift; ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ); }
if [ "$mode" = light ]; then
  run r1_check_tables python3 -B "$p/r1/check_tables.py" "$repo" "$ev"
  run r1_partition_check python3 -B "$p/r1/partition_check.py" "$ev"
  run r1_probe_cli python3 -B "$p/r1/probe_cli.py" "$repo" "$scratch/r1_cli"
  run r1_probe_route_status python3 -B "$p/r1/probe_route_status.py" "$repo" "$scratch/r1_route_status"
  run r1_replay_records python3 -B "$p/r1/replay_records.py" "$repo" "$ev"
  run r2_partition_r2 python3 -B "$p/r2/partition_r2.py" "$ev"
  run r2_probe_contract python3 -B "$p/r2/probe_contract.py" "$repo" "$store/A/work/ax7101/gateware" "$scratch/r2_contract"
  run r2_probe_policy python3 -B "$p/r2/probe_policy.py" "$repo" "$scratch/r2_policy"
  run r2_probe_route_real_A python3 -B "$p/r2/probe_route_real.py" "$repo" "$store/A/work/ax7101/gateware" "$scratch/r2_route_A"
  run r2_probe_route_real_B python3 -B "$p/r2/probe_route_real.py" "$repo" "$store/B/work/ax7101/gateware" "$scratch/r2_route_B"
  run r3_armq_count python3 -B "$p/r3/armq_count.py" "A-1x1=$store/A/work/ax7101-ooc/baseline_cells.tsv" \
    "B-1x1=$store/B/work/ax7101-ooc/baseline_cells.tsv" "A-8x8=$store/A/work/ax8x8-ooc/baseline_cells.tsv"
  git -C "$repo" show b5894838d6c47180ac4169e7d52dd746f461af21:syn/ooc/pp_baseline_rank.py > "$scratch/rank_b5894838.py"
  ( cd "$store" && run r3_hier_compare python3 -B "$p/r3/hier_compare.py" "$scratch/rank_b5894838.py" \
      "$repo/syn/ooc/pp_baseline_rank.py" A/work/ax7101/gateware/baseline_hierarchy.rpt \
      A/work/ax7101-ooc10/baseline_hierarchy.rpt A/work/ax7101-ooc/baseline_hierarchy.rpt \
      A/work/ax8x8-ooc/baseline_hierarchy.rpt B/work/ax7101/gateware/baseline_hierarchy.rpt \
      B/work/ax7101-ooc/baseline_hierarchy.rpt B/work/ax8x8-ooc/baseline_hierarchy.rpt )
  run r3_probe_bigint_B python3 -B "$p/r3/probe_bigint.py" "$repo" "$store/B/work/ax7101/gateware" "$scratch/r3_bigint_B"
  run r3_probe_bigint_A python3 -B "$p/r3/probe_bigint.py" "$repo" "$store/A/work/ax7101/gateware" "$scratch/r3_bigint_A"
  run r3_probe_gaps python3 -B "$p/r3/probe_gaps.py" "$repo" "$store/A/work/ax7101/gateware" "$scratch/r3_gaps"
  run r3_probe_text python3 -B "$p/r3/probe_text.py" "$repo" "$store/A/work/ax7101/gateware" "$scratch/r3_text"
else
  run r1_extra_mutants python3 -B "$p/r1/extra_mutants.py" "$repo" "$scratch/r1_mutants"
  run r2_classify_mutants python3 -B "$p/r2/classify_mutants.py" "$repo" "$scratch/r2_classify" 16
  run r3_extra_mutants_r3 python3 -B "$p/r3/extra_mutants_r3.py" "$repo" "$scratch/r3_mutants"
fi
echo done > "$out/$mode.done"
