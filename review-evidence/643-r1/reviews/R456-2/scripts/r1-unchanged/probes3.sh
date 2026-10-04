#!/bin/bash
# R456-1 probe campaign part 3: the tie boundary. Usage: probes3.sh PACKET VERILATOR_WRAPPER
#   tie36   - the published diagnostic's phase list, +2010..+2045 (36 phases)
#   tietr18 - this review's +2018..+2035 scan with a per-PDU trace of the
#             pop nearest each PDU end (the run whose +2025 failed)
#   tietr36 - the same trace on the +2010..+2045 list
set -u
P=$1; VL=$2; R=$P/receipts/probes; mkdir -p $R
D="$P/scripts/run_probe.py"; HP=$P/scratch/hp
PH_FROM='constexpr std::array<long, 18> kLawPhases = {\n    0, 130, 260, 391, 521, 651, 781, 911, 927, 1042, 1156, 1172, 1302, 1432,\n    1562, 1693, 1823, 1953};'
PH18='constexpr std::array<long, 18> kLawPhases = {\n    2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,\n    2030, 2031, 2032, 2033, 2034, 2035};'
PH36='constexpr std::array<long, 36> kLawPhases = {\n    2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045};'
T1_FROM='    std::array<int, kIdSpace> tie_pop{};'
T1_TO='    std::array<int, kIdSpace> tie_pop{};\n    std::array<long, kIdSpace> dbg_prev{};\n    std::array<long, kIdSpace> dbg_next{};\n    long dbg_last_pop = -1;'
T2_FROM='            end_fill_due = last_accept_id;\n            last_end_id = last_accept_id;'
T2_TO='            end_fill_due = last_accept_id;\n            last_end_id = last_accept_id;\n            dbg_prev[static_cast<size_t>(last_accept_id)] = axis_cycle - dbg_last_pop;\n            dbg_next[static_cast<size_t>(last_accept_id)] = -1;'
T3_FROM='        if ((dut->rootp->milan_datapath__DOT__rsp_pop_p_w & 1) && last_end_id >= 0) {\n            const size_t i = static_cast<size_t>(last_end_id);'
T3_TO='        if (dut->rootp->milan_datapath__DOT__rsp_pop_p_w & 1) {\n            if (last_end_id >= 0 && dbg_next[static_cast<size_t>(last_end_id)] < 0)\n                dbg_next[static_cast<size_t>(last_end_id)] = axis_cycle - end_at[static_cast<size_t>(last_end_id)];\n            dbg_last_pop = axis_cycle;\n        }\n        if ((dut->rootp->milan_datapath__DOT__rsp_pop_p_w & 1) && last_end_id >= 0) {\n            const size_t i = static_cast<size_t>(last_end_id);'
T4_FROM='        if (tie_pop[i] != 0) ++ties;'
T4_TO='        if (tie_pop[i] != 0) ++ties;\n        if (f != kPrefillTargetEvt || tie_pop[i] != 0 || dbg_next[i] <= 4 || dbg_prev[i] <= 4)\n            std::printf("  [dbg] %s id %ld fill %d tie %d ok %d prev_pop_seen_before_end %ld next_pop_seen_after_end %ld d %ld\\n", tag, id, f, tie_pop[i], (f == kPrefillTargetEvt || tie_ok) ? 1 : 0, dbg_prev[i], dbg_next[i], d);'
b() { echo "== build $*"; python3 $D build "$@" --verilator $VL || echo "BUILD FAILED $*"; }
b $HP tie36 --tb-edit "$PH_FROM" "$PH36"
b $HP tietr18 --tb-edit "$PH_FROM" "$PH18" --tb-edit "$T1_FROM" "$T1_TO" --tb-edit "$T2_FROM" "$T2_TO" --tb-edit "$T3_FROM" "$T3_TO" --tb-edit "$T4_FROM" "$T4_TO"
b $HP tietr36 --tb-edit "$PH_FROM" "$PH36" --tb-edit "$T1_FROM" "$T1_TO" --tb-edit "$T2_FROM" "$T2_TO" --tb-edit "$T3_FROM" "$T3_TO" --tb-edit "$T4_FROM" "$T4_TO"
echo "== builds done $(date +%T)"
r() { python3 $D run "$1" "$2" --mode="$3" --log "$R/$4.log" & }
r $HP tie36 --law-only hp-tie36-law
r $HP tietr18 --law-only hp-tietr18-law
r $HP tietr36 --law-only hp-tietr36-law
wait
echo "== runs done $(date +%T)"
