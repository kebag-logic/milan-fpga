#!/bin/bash
# Read-only gate batch at the exact head; each job its own log and rc file.
# Usage: batch1.sh <clone> <outdir> <pinned-verilator-dir>
set -u
C=$1; O=$2; V=$3
mkdir -p "$O"
export PATH="$V:$PATH"
cd "$C"
run() { local n=$1; shift; ( "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc" ) & }
run lint_rtl         python3 scripts/lint_rtl.py --check
run pp_shadow        make -C tb/verilator/pp_shadow -j16
run port_contracts   python3 scripts/check_port_contracts.py
run naming           python3 scripts/measure_naming.py --check
run test_evidence    python3 scripts/measure_test_evidence.py --check
run nvm_capture      python3 scripts/check_nvm_capture.py
run submodule_docs   python3 scripts/check_submodule_docs.py
run boundary_check   python3 docs/diagrams/submodule_boundaries.gen.py --check
run docs_check       python3 scripts/docs_check.py
run pp_srcs          python3 scripts/pp_srcs.py --check --selftest
run rtl_src_lists    python3 scripts/check_rtl_source_lists.py
mkdir -p "$O/roms"
run rom_ltn          python3 protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o "$O/roms/ltn_rom.hex"
run rom_ucode        python3 protocol-processor/hdl/aecp/ucode/gen_ucode.py -o "$O/roms/ucode.hex"
wait
