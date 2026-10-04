#!/bin/bash
# R456-1 probe campaign part 2 (the three harness probes whose edit strings
# needed a plain '&&'). Usage: probes2.sh PACKET VERILATOR_WRAPPER
set -u
P=$1; VL=$2; R=$P/receipts/probes; mkdir -p $R
D="$P/scripts/run_probe.py"; HP=$P/scratch/hp
PH_FROM='    0, 130, 260, 391, 521, 651, 781, 911, 927, 1042, 1156, 1172, 1302, 1432,\n    1562, 1693, 1823, 1953};'
PH_TO='    2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,\n    2030, 2031, 2032, 2033, 2034, 2035};'
TIE_FROM='        if (f == kPrefillTargetEvt || tie_ok) ++fill_ok;'
TIE_TO='        if (f == kPrefillTargetEvt || (tie_ok && false)) ++fill_ok;'
TR_FROM='            settle_run = 0;\n            ++unsettled_ticks;\n        }\n    }'
TR_TO='            if (settle_run >= kSettleTicks) std::printf("  [probe] report LAPSED at tick %ld after a run of %ld (err %d)\\n", media_ticks, settle_run, err);\n            settle_run = 0;\n            ++unsettled_ticks;\n        }\n        if (settle_run == kSettleTicks) std::printf("  [probe] report MET at tick %ld (err %d)\\n", media_ticks, err);\n        if (media_ticks <= 24000 && media_ticks % 100 == 0) std::printf("  [probe] tick %ld engaged %d err %d run %ld\\n", media_ticks, static_cast<int>(dut->rootp->milan_datapath__DOT__mga_engaged_w), err, settle_run);\n    }'
ND_FROM='        run_fed(kBootPullInCycles);\n        phase_internal_law();'
ND_TO='        run_fed(0);\n        phase_internal_law();'
b() { echo "== build $*"; python3 $D build "$@" --verilator $VL || echo "BUILD FAILED $*"; }
b $HP tieoff --tb-edit "$PH_FROM" "$PH_TO" --tb-edit "$TIE_FROM" "$TIE_TO"
b $HP boottrace --tb-edit "$TR_FROM" "$TR_TO"
b $HP bootnodwell --tb-edit "$TR_FROM" "$TR_TO" --tb-edit "$ND_FROM" "$ND_TO"
echo "== builds done $(date +%T)"
r() { python3 $D run "$1" "$2" --mode="$3" --log "$R/$4.log" & }
r $HP tieoff --law-only hp-tieoff-law
r $HP boottrace --law-only hp-boottrace-law
r $HP bootnodwell --law-only hp-bootnodwell-law
wait
echo "== runs done $(date +%T)"
