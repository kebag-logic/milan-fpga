#!/usr/bin/env bash
# Scratch (M8a-1): the software gates the change touches, each unpiped, rc recorded.
set -u
L=$LANES/640-m8a
S=$VALIDATION_STORAGE/640m8a-a594/m81
G=$S/gates
P312=$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12
export TMPDIR=$S/tmpdir MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export MILAN_RV32_CC=$VALIDATION_STORAGE/502-a340-sdk/bin/riscv32-linux-gcc
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH VERILATOR_JOBS=2 MAKEFLAGS=-j8
cd "$L" || exit 9
run() {  # name, command...
  local n=$1; shift
  "$@" > "$G/$n.log" 2>&1
  echo $? > "$G/$n.rc"
  printf '%s\t%s\trc=%s\n' "$(date -Is)" "$n" "$(cat "$G/$n.rc")" >> "$G/summary.tsv"
}
git rev-parse HEAD > "$G/head.txt"
git status --porcelain > "$G/status-before.txt"
run test_ctrl_memory "$MILAN_LITEX_PYTHON" -B sw/litex/test_ctrl_memory.py
run litex_sims_selftest bash scripts/run_litex_sims.sh --selftest
run litex_sims bash scripts/run_litex_sims.sh "$G/litex-sim-logs"
run ctrl_memory_py312 "$P312" -I sw/litex/ctrl_memory.py plan "$S/fit/split-endstation_ax7101_8x8-if2/ctrl_app.elf" --stage-bytes 13264
run py_idiom "$P312" scripts/check_py_idiom.py
run py_idiom_selftest "$P312" scripts/check_py_idiom.py --selftest
run hygiene "$P312" scripts/check_hygiene.py --check
run hygiene_selftest "$P312" scripts/check_hygiene.py --selftest
run todo "$P312" scripts/check_todo_ownership.py
run fail_fast "$P312" scripts/measure_fail_fast.py --check
run test_evidence "$P312" scripts/measure_test_evidence.py --check
run soc_sources python3 scripts/check_soc_sources.py
run soc_sources_selftest python3 scripts/check_soc_sources.py --selftest
run iob_pack_selftest python3 sw/litex/iob_pack_selftest.py
run sweep_shape python3 scripts/check_sweep_shape.py --self-test
run deploy_shape python3 scripts/check_deploy_shape.py --self-test
run entity_shape python3 scripts/check_entity_shape.py --self-test
run ooc_selftests bash -c 'set -e; python3 syn/ooc/dp_srcs.py --selftest; python3 syn/ooc/ooc_tcl_selftest.py; python3 syn/ooc/pp_baseline.py --selftest; python3 syn/ooc/pp_baseline_mutants.py; python3 syn/ooc/pp_baseline_reports_selftest.py; python3 syn/ooc/pp_resource_gate.py --selftest; python3 syn/ooc/pp_resource_gate_mutants.py; python3 syn/ooc/pp_resource_gate.py check-baseline'
run ctrl_image_selftest python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
run test_builder_elab python3 sw/builder/test_builder.py --require-elaboration --require-rv32
run test_ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
git status --porcelain > "$G/status-after.txt"
echo done > "$G/sw.done"
