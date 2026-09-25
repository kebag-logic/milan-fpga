#!/bin/sh
# R307-1 reproduction of the reviewer's executable checks for PR #560 at
# 6a9828c172aa4d5d8ee49725e357a10bae2caa52. Run from a DISPOSABLE full copy
# of the checkout (submodules initialised at their pins), never the reviewed
# clone itself. VERILATOR must name Verilator 5.050.
#   usage: VERILATOR=/path/to/verilator PACKET=/path/to/packet sh reproduce.sh <copy>
set -eu
T="$1"; : "${VERILATOR:?}"; : "${PACKET:?}"
export PATH="$(dirname "$VERILATOR"):$PATH" VERILATOR_JOBS=8
cd "$T"
test "$(git rev-parse HEAD)" = 6a9828c172aa4d5d8ee49725e357a10bae2caa52

# static gates (the renderer-dependent ones need tools/markdown/requirements.txt)
for c in "scripts/check_port_contracts.py" "scripts/measure_naming.py --check" \
         "scripts/measure_test_evidence.py --check" "scripts/measure_test_evidence.py --selftest" \
         "scripts/pp_srcs.py --check" "scripts/docs_check.py" "scripts/check_doc_paths.py" \
         "scripts/gen_toc.py --check" "scripts/check_rtl_source_lists.py" \
         "scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2" \
         "scripts/check_doc_style.py" "docs/traceability/gen_module_matrix.py --check" \
         "scripts/check_cpp_idiom.py" "scripts/check_py_idiom.py" \
         "scripts/check_submodule_docs.py" "scripts/check_diagram_pngs.py" \
         "docs/diagrams/submodule_boundaries.gen.py --check" "scripts/lint_rtl.py --check"; do
  python3 -B $c >/dev/null 2>&1 && echo "rc=0 $c" || echo "rc=$? $c"
done

# ROM digests at the pin, recomputed with the generators ooc.sh runs
python3 protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o /tmp/r307_ltn.hex >/dev/null
python3 protocol-processor/hdl/aecp/ucode/gen_ucode.py -o /tmp/r307_ucode.hex >/dev/null
sha256sum /tmp/r307_ltn.hex /tmp/r307_ucode.hex
grep 990f96526bb89356c963a260ebbdcf2a77e6623a syn/yosys/rom_digests.tsv

# the timed [GSI] leg, its mutation campaign, reviewer mutants and probe
make -C tb/verilator/milan_dp notify-build VERILATOR="$VERILATOR"
(cd tb/verilator/milan_dp && ./obj_notify/Vmilan_dp_notify | tail -n 3)
make -C tb/verilator/milan_dp gsi-mutants
python3 "$PACKET/scripts/reviewer_mutants.py" "$T/tb/verilator/milan_dp"
cp tb/verilator/milan_dp/sim_nxn.cpp /tmp/r307_sim_nxn.orig
python3 "$PACKET/scripts/probe_gsi_latency_and_g8.py" tb/verilator/milan_dp/sim_nxn.cpp
make -C tb/verilator/milan_dp notify-build VERILATOR="$VERILATOR" NOTIFY_MDIR=obj_probe
(cd tb/verilator/milan_dp && ./obj_probe/Vmilan_dp_notify | grep -E 'PROBE|^checks:|^RESULT')
cp /tmp/r307_sim_nxn.orig tb/verilator/milan_dp/sim_nxn.cpp

# consuming suites
make -C tb/verilator/pp_shadow VERILATOR="$VERILATOR"
make -C tb/verilator/nvm_cosim run JOBS=8 POOL=8
