#!/usr/bin/env bash
# Reproduce the focused review in a fresh packet directory.
# Arguments: REPO PACKET SDK_CACHE BASE_PYTHON SCOPED_SIMULATOR VIVADO VIVADO_LOCK
set -euo pipefail
repo=$(realpath "$1")
packet=$(realpath "$2")
sdk_cache=$(realpath "$3")
base_python=$(realpath "$4")
export REAL_VERILATOR=$(realpath "$5")
vivado=$(realpath "$6")
vivado_lock=$7
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$packet/scratch"
python3 "$here/prepare_sdk.py" "$repo" "$packet" "$sdk_cache" "$base_python"
python3 "$here/clone_probe.py" "$repo" "$packet"
export MILAN_LITEX_PYTHON="$packet/scratch/sdk-python"
export VERILATOR="$here/bounded_verilator.py"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
export TMPDIR="$packet/scratch"
"$REAL_VERILATOR" --version
run() { python3 "$here/run_receipt.py" "$packet" "$@"; }
run model "$repo" "$MILAN_LITEX_PYTHON" sw/litex/gen_mac_tx_model.py --check
run model-control "$repo" "$MILAN_LITEX_PYTHON" "$here/probe_model.py" "$repo" "$packet"
run capture "$repo" "$MILAN_LITEX_PYTHON" sw/litex/test_gmii_rx_capture.py --emit-dir "$packet/scratch/capture"
run gptp-txts "$packet/scratch/probe" make -j16 -C tb/verilator/gptp_txts
run iob-selftest "$repo" python3 sw/litex/iob_pack_selftest.py
run runner-selftest "$repo" bash scripts/run_litex_sims.sh --selftest
# Exclusively held, after the compilation/mutation campaign has ended.
run placement "$packet/scratch/capture" flock -w 600 "$vivado_lock" "$vivado" -mode batch -nojournal -source "$repo/sw/litex/gmii_rx_capture_check.tcl" -tclargs "$packet/scratch/capture"
run restored-review-tree "$repo" python3 "$here/audit_tree.py" "$repo" ba080007a402dced74fa74656338710e0b6cb880
run restored-probe-tree "$packet/scratch/probe" python3 "$here/audit_tree.py" "$packet/scratch/probe" ba080007a402dced74fa74656338710e0b6cb880
