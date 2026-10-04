#!/bin/bash
# R456-2 probe BUILDS for #643 / PR #648 at 6b96391d. Usage: r2_builds.sh PACKET LANE
# Every edit string below is copied verbatim from R456-1's probes.sh/probes2.sh/
# probes3.sh (scripts/r1-unchanged/, byte-identical to the R456-1 packet), except
# the R456-2 additions marked NEW. run_probe.py plants harness edits IN PLACE, so
# builds that share a tree are serialised; lanes use separate copies of the tree
# (scratch/hp, hp2, hp3 = exact head at processor 631eeb34; scratch/pc4c, c4b =
# exact head + processor c4cb84ff + both adoption patches, never committed).
set -u
P=$1; LANE=$2; S=$P/scratch; L=$P/receipts/builds; mkdir -p $L
D="$P/scripts/r1-unchanged/run_probe.py"
export VL_REAL=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VL_JOBS=${VL_JOBS:-3}
VL="$P/scripts/r1-unchanged/vl_jobs.sh"
A2A_FROM='  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;'
A2A_TO='  wire        mga_sel_w = follow_sel_r;'
SP='  localparam int RENDER_SETPOINT_EVT_C = RENDER_PDU_EVT_C + RENDER_ALLOW_EVT_C;'
PH_FROM='    0, 130, 260, 391, 521, 651, 781, 911, 927, 1042, 1156, 1172, 1302, 1432,\n    1562, 1693, 1823, 1953};'
PH_TO='    2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,\n    2030, 2031, 2032, 2033, 2034, 2035};'
TIE_FROM='        if (f == kPrefillTargetEvt || tie_ok) ++fill_ok;'
TIE_TO='        if (f == kPrefillTargetEvt || (tie_ok && false)) ++fill_ok;'
TR_FROM='            settle_run = 0;\n            ++unsettled_ticks;\n        }\n    }'
TR_TO='            if (settle_run >= kSettleTicks) std::printf("  [probe] report LAPSED at tick %ld after a run of %ld (err %d)\\n", media_ticks, settle_run, err);\n            settle_run = 0;\n            ++unsettled_ticks;\n        }\n        if (settle_run == kSettleTicks) std::printf("  [probe] report MET at tick %ld (err %d)\\n", media_ticks, err);\n        if (media_ticks <= 24000 && media_ticks % 100 == 0) std::printf("  [probe] tick %ld engaged %d err %d run %ld\\n", media_ticks, static_cast<int>(dut->rootp->milan_datapath__DOT__mga_engaged_w), err, settle_run);\n    }'
ND_FROM='        run_fed(kBootPullInCycles);\n        phase_internal_law();'
ND_TO='        run_fed(0);\n        phase_internal_law();'
PH3_FROM='constexpr std::array<long, 18> kLawPhases = {\n    0, 130, 260, 391, 521, 651, 781, 911, 927, 1042, 1156, 1172, 1302, 1432,\n    1562, 1693, 1823, 1953};'
PH18='constexpr std::array<long, 18> kLawPhases = {\n    2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,\n    2030, 2031, 2032, 2033, 2034, 2035};'
PH36='constexpr std::array<long, 36> kLawPhases = {\n    2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045};'
T1_FROM='    std::array<int, kIdSpace> tie_pop{};'
T1_TO='    std::array<int, kIdSpace> tie_pop{};\n    std::array<long, kIdSpace> dbg_prev{};\n    std::array<long, kIdSpace> dbg_next{};\n    long dbg_last_pop = -1;'
# NEW (R456-2): the ambiguity window's guard removed (W = 4) and the window
# removed (W = 0), to show whether W is load-bearing at the boundary
G_FROM='constexpr long kLawGuardCycles = 4;'
G0_TO='constexpr long kLawGuardCycles = 0;'
GM4_TO='constexpr long kLawGuardCycles = -4;'
b() { local n=$2; echo "== build $n start $(date +%T)"; python3 $D build "$@" --verilator $VL > $L/$n.out 2>&1; echo "rc=$?" > $L/$n.rc; echo "== build $n $(cat $L/$n.rc) $(date +%T)"; }
case $LANE in
L1) T=$S/hp
    b $T clean
    b $T a2a --dp-edit "$A2A_FROM" "$A2A_TO"
    b $T spp1 --dp-edit "$SP" "${SP/;/ + 1;}"
    b $T spm1 --dp-edit "$SP" "${SP/;/ - 1;}"
    b $T w4 --tb-edit "$G_FROM" "$G0_TO" ;;
L2) T=$S/hp2
    b $T tieon --tb-edit "$PH_FROM" "$PH_TO"
    b $T tiespp1 --tb-edit "$PH_FROM" "$PH_TO" --dp-edit "$SP" "${SP/;/ + 1;}"
    b $T tiespm1 --tb-edit "$PH_FROM" "$PH_TO" --dp-edit "$SP" "${SP/;/ - 1;}"
    b $T tie36 --tb-edit "$PH3_FROM" "$PH36"
    b $T tieoff --tb-edit "$PH_FROM" "$PH_TO" --tb-edit "$TIE_FROM" "$TIE_TO"
    b $T tietr18 --tb-edit "$PH3_FROM" "$PH18" --tb-edit "$T1_FROM" "$T1_TO"
    b $T tietr36 --tb-edit "$PH3_FROM" "$PH36" --tb-edit "$T1_FROM" "$T1_TO" ;;
L3) T=$S/hp3
    b $T boottrace --tb-edit "$TR_FROM" "$TR_TO"
    b $T bootnodwell --tb-edit "$TR_FROM" "$TR_TO" --tb-edit "$ND_FROM" "$ND_TO"
    b $T w0 --tb-edit "$G_FROM" "$GM4_TO"
    b $T spm1w0 --tb-edit "$G_FROM" "$GM4_TO" --dp-edit "$SP" "${SP/;/ - 1;}"
    b $T spp1w0 --tb-edit "$G_FROM" "$GM4_TO" --dp-edit "$SP" "${SP/;/ + 1;}"
    b $T basep631 --tb-file $S/base_sim_tdm8_render.cpp ;;
L4) T=$S/pc4c
    b $T clean
    b $T spp1 --dp-edit "$SP" "${SP/;/ + 1;}"
    b $T spm1 --dp-edit "$SP" "${SP/;/ - 1;}" ;;
L5) T=$S/c4b
    b $T a2a --dp-edit "$A2A_FROM" "$A2A_TO"
    b $T tieon --tb-edit "$PH_FROM" "$PH_TO"
    b $T basec4c --tb-file $S/base_sim_tdm8_render.cpp ;;
esac
echo "== lane $LANE done $(date +%T)"
# NEW (R456-2), lane L6: the ambiguity window widened past the CRF window's
# margin (guard 1100, W = 1104, beyond any clearance, half a tick), to show the T30 CRF LAW standing gradable check
# fails by name and its law checks are then neither passed nor failed
if [ "$LANE" = L6 ]; then
    b $S/hp2 crfw1104 --tb-edit "$G_FROM" 'constexpr long kLawGuardCycles = 1100;'
fi
# NEW (R456-2), lane L7: print the per-offset histogram for EVERY window, the
# T30 CRF LAW window included (it is otherwise printed only under
# --law-boundary), so the CRF window's nearest-pop spread can be read in the
# full leg at both processors. Grading is unchanged.
if [ "$LANE" = L7 ]; then
    H_FROM='    if (law_boundary) print_the_offset_histogram(span_first, last_id, tag);'
    H_TO='    print_the_offset_histogram(span_first, last_id, tag);'
    b $S/hp2 crfhist --tb-edit "$H_FROM" "$H_TO"
    b $S/c4b crfhist --tb-edit "$H_FROM" "$H_TO"
fi
