#!/usr/bin/env bash
# make_receipts.sh: every receipt of round 3 from its log, through receipt.py (head and command first, host paths
# replaced), then receipts/INDEX.md from the files present
set -uo pipefail
S=/data-2/milan/tmp/665s7-a757c; T=$MANAGEMENT/2026-09-23/665s7-a757c/tools
R=$MANAGEMENT/2026-09-23/665s7-a757c/receipts; H=2128daad26b932feeed1ef2bde8f2774e8a51a31; G=$S/gates
r() { [ -f "$1" ] && python3 $T/receipt.py "$@"; }
M="make --no-print-directory -C tb/verilator/milan_dp"
r $G/make-srptx.log $R/srptx/make-srptx.txt $H $M srptx
r $G/make-srptx-plants.log $R/srptx/make-srptx-plants.txt $H $M srptx-plants
r $G/make-srptx-mutants.log $R/srptx/make-srptx-mutants.txt $H $M srptx-mutants
r $G/make-twin.log $R/srptx/make-twin.txt $H $M twin
r $G/make-twin-plants.log $R/srptx/make-twin-plants.txt $H $M twin-plants
r $G/srptx-clean.log $R/srptx/gate-clone-clean.txt $H "git status --porcelain --ignored=no (the srptx gate clone, after every srptx gate and the request probe)"
r $G/request-probe.log $R/probes/request-probe.txt $H "python3 -I request_probe.py tb/verilator/milan_dp <scratch>/req 280 240 (R813-2's script, sha256 baa576da6c8c1ca726161a70727d364aaeb53e3934863740871ae52622e24a3c, unchanged)"
r $G/code-probe.log $R/probes/r814-1-code-probe.txt $H "python3 -I code_probe.py <gate clone> <scratch>/cprobe 2 join-10cs join-15cs (R814-1's script, sha256 0e5d16ae03f1881427af18eb1528f602e788de3f98ff4f549e7898faf50e736c, unchanged)"
r $G/code-probe-clean.log $R/probes/code-probe-clone-clean.txt $H "git status --porcelain --ignored=no (the same clone, after the code probe)"
r $S/rcpt/ablate.txt $R/probes/ablate.txt $H "python3 -B ablate.py <gate clone>/tb/verilator/milan_dp <the grade at 2131eff4> <gate clone>/tb/verilator/milan_dp/obj_srptx"
r $S/rcpt/attrib.txt $R/probes/attribution-compare.txt $H "python3 -B attrib_compare.py <the grade at 2131eff4> <gate clone> obj_srptx/{wire,hold,licence,licence-16280,licence-16240}.json"
r $S/rcpt/join-figures.txt $R/srptx/join-figures.txt $H "python3 -B join_figures.py <gate clone>/tb/verilator/milan_dp obj_srptx/*.json (wire, hold, licence, licence-16280, licence-16240)"
r $S/rcpt/measured-diff.txt $R/srptx/measured-diff-vs-round2.txt $H "python3 -I measured_diff.py <round 2 report receipt> <this head's report>, per scenario"
r $S/rcpt/captures-sha256.txt $R/srptx/captures-sha256.txt $H "sha256sum obj_srptx/*.json in the gate clone"
r $S/rcpt/twin-split.txt $R/srptx/twin-split-capture.txt $H "sha256sum obj_twin/split.json (make twin in the gate clone) against round 1's receipt"
for n in wire hold licence licence-16280 licence-16240; do
  r $G/srptx/tb/verilator/milan_dp/obj_srptx/$n-report.json $R/srptx/$n-report.json.txt $H "$M srptx (its report, $n)"
done
g() { r $G/$1.log $R/gates/$1.txt $H "$2 (tools/gates.sh, on its own clean clone)"; }
g rv32-sdk "python3 scripts/ci_rv32_sdk.py --destination <scratch><home-path>/host --archive <tools>/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz"
g rv32-sdk-verify "python3 scripts/ci_rv32_sdk.py --destination <scratch><home-path>/host --verify-only"
g diff-check "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 $H"
g diff-check-r2 "git diff --check 2131eff48066da1e3bbeb6b417ea0655fa7c7741 $H"
g test-builder "python3 sw/builder/test_builder.py --require-rv32 (the LiteX venv first on PATH)"
g budget-selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test (the LiteX venv)"
g budget-1x1 "python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <scratch>/tmp/budget-1x1 --record-budget-findings (1 interface)"
g budget-8x8 "python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <scratch>/tmp/budget-8x8 --record-budget-findings (2 interfaces)"
g budget-clean "git status --porcelain --ignored=no (the budget clone, after its three runs)"
g budget8x8-clean "git status --porcelain --ignored=no (the budget-8x8 clone, after its run; budget-8x8 re-ran alone on it after the host restart)"
r $G/litex-sims-diag.log $R/gates/litex-sims-diag.txt $H "tools/litex_sims_diag.sh: elaborate-gates-1's gate_19, scripts/run_litex_sims.sh, in that job's worktree and environment with LITEX_SIM_TIMEOUT=7200 (diagnostic)"
r $S/ci/attempts.txt $R/ci/attempts.txt $H "every gate attempt before the kept one, with its cause"
g make-split "$M split"
g make-split-mutants "$M split-mutants"
g make-split-cdc "$M split-cdc"
g split-parallel "python3 tb/verilator/milan_dp/split_parallel.py --selftest"
g split-clean "git status --porcelain --ignored=no (the split clone, after its four gates)"
r $S/ci/ci-replay-table.md $R/ci/ci-replay-table.md $H "python3 ci_replay.py table (every run: step of every job a ready pull_request to dev-soft-core runs: docs, elaborate, rtl-fast, rtl; each job on its own clean clone)"
r $S/ci/not_run.json $R/ci/not_run.json.txt $H "python3 ci_replay.py table: each step that did not run, with its reason"
r $S/rcpt/key-verdicts.txt $R/ci/key-verdicts.txt $H "grep of the verdict lines in the replay's job logs (firmware self-test shards, mutant campaigns, fw_coverage, ctrl_boundary, behave, LiteX simulations, suite unions)"
r $S/rcpt/replay-results.txt $R/ci/replay-results.txt $H "each job instance's result.json result"
for k in 0 1 2 3; do
  r $S/sweep/shard-$k/spec/01.log $R/sweep/shard-$k.txt $H "run_all_suites.sh <out>/shard-$k/logs --wait --shard $k/4 (native-shards.py, its own clone and unit, MemoryMax 10G, MAKEFLAGS -j4 --no-print-directory)"
  r $S/sweep/shard-$k/spec/complete.json $R/sweep/shard-$k-complete.json.txt $H "the shard's run-recorded-gates.py completion record"
done
r $S/sweep-launch-record.txt $R/sweep/launch.txt $H "how the four shards were launched, and on which CPUs"
r $S/native-spec.json $R/sweep/native-spec.json.txt $H "the sweep spec native-shards.py and sweep-shard.py read"
python3 $T/index.py $R
