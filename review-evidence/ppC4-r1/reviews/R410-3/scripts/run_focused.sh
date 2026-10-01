#!/usr/bin/env bash
# R410-3 focused executable checks at the exact head. Portable: pass the tree
# (a clean checkout of the head), the Verilator wrapper and the receipt dir.
#   run_focused.sh TREE VERILATOR_BIN_DIR RECEIPTS STAGE
# Every command runs in the foreground, pinned to 8 CPUs (taskset -c 0-7), so
# Verilator's "-j 0" build make and any driver pool stay within 8 jobs.
set -uo pipefail
tree=$1; vbin=$2; out=$3; stage=$4
export PATH="$vbin:$PATH"
mkdir -p "$out"
cd "$tree" || exit 2
pin() { taskset -c 0-7 "$@"; }
rec() {  # rec NAME CMD... : log stdout+stderr, record rc and wall time
  local name=$1; shift
  local t0=$(date +%s)
  ( pin "$@" ) >"$out/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc wall=$(( $(date +%s) - t0 ))s cmd=$*" | tee -a "$out/rc-summary.txt"
  return 0
}
case $stage in
  suites)
    verilator --version | tee -a "$out/rc-summary.txt"
    for s in rx_validator acmp_listener acmp_nvm maap adp_engine; do
      rec "suite-$s" make -C "tb/$s"
      grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/suite-$s.log" | tail -1 | sed "s/^/  $s tally: /" | tee -a "$out/rc-summary.txt"
    done
    rec suite-pp_top make -C tb/pp_top
    grep -E '^[A-Z0-9]+: [0-9]+ checks|checks, [0-9]+ failures|[0-9]+ checks: [0-9]+ PASS' "$out/suite-pp_top.log" | sed 's/^/  pp_top: /' | tee -a "$out/rc-summary.txt"
    ;;
  entry)
    # the one-section selectors, each on the default build, run from
    # tb/pp_top as the Makefile does (the ROM images and the tally file are
    # cwd-relative)
    cd tb/pp_top || exit 2
    for f in --acmp-only --adp-only --maap-internal-only --gsi-internal-only --name-writes-only --d3-only; do
      rm -f obj_dir/build_tally.txt
      rec "pp_top-entry$f" ./obj_dir/Vpp_top_sim "$f"
      tail -2 "$out/pp_top-entry$f.log" | sed "s/^/  $f: /" | tee -a "$out/rc-summary.txt"
    done
    ;;
  gates)
    rec lint_hdl ./scripts/lint_hdl.sh
    rec make_check make check
    rec gen_matrix python3 scripts/gen_matrix.py --check
    rec diff_check_d5 git diff --check d5f73bac158276a9fcf549185bad5c65c0498dae 4e558491c608dc88efc7963a77cb6b49bce2a46e
    rec diff_check_lane git diff --check b2db3a970cedbbff2f8ba813acb96122c442bc58 4e558491c608dc88efc7963a77cb6b49bce2a46e
    rec check_upc_map python3 scripts/check_upc_map.py
    ;;
  acmp_mutants_A|acmp_mutants_B|acmp_mutants_C)
    # the 19 controls in three groups (each with its own goldens), so every
    # foreground call stays bounded; the driver's temp copies go to scratch
    case $stage in
      acmp_mutants_A) only="msg_ok_forced guard_ctlr_dropped guard_talker_eid_dropped guard_talker_uid_dropped cdl_not_44_rejected" ;;
      acmp_mutants_B) only="st_ls_settle_as_withdraw st_ls_teardown_as_declare st_ls_sid_da_swapped st_ls_state_none st_ls_vid_dropped st_ls_index_zero st_ls_teardown_lost" ;;
      acmp_mutants_C) only="bound_view_not_latched bound_dmac_from_sid bound_view_not_cleared matcher_da_ignored matcher_vid_ignored" ;;
    esac
    export TMPDIR="${R410_TMP:?set R410_TMP to a scratch dir}"; mkdir -p "$TMPDIR"
    # shellcheck disable=SC2086
    rec "$stage" python3 tb/pp_top/acmp_mutants.py --output "$out/$stage" --verilator "$vbin/verilator" --jobs 8 --only $only
    tail -25 "$out/$stage.log" | tee -a "$out/rc-summary.txt"
    ;;
  maap_mutants)
    export TMPDIR="${R410_TMP:?set R410_TMP to a scratch dir}"; mkdir -p "$TMPDIR"
    rec maap_mutants make -C tb/maap mutants "MUTANT_OUTPUT=$out/maap_mutants" "VERILATOR=$vbin/verilator"
    tail -40 "$out/maap_mutants.log" | tee -a "$out/rc-summary.txt"
    ;;
  adp_mutants)
    export TMPDIR="${R410_TMP:?set R410_TMP to a scratch dir}"; mkdir -p "$TMPDIR"
    rec adp_mutants make -C tb/adp_engine mutants "MUTANT_OUTPUT=$out/adp_mutants" "VERILATOR=$vbin/verilator"
    tail -40 "$out/adp_mutants.log" | tee -a "$out/rc-summary.txt"
    ;;
  *) echo "unknown stage $stage"; exit 2 ;;
esac
