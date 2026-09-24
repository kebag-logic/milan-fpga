#!/usr/bin/env bash
# Re-derive, at the exact head and its gitlinks, every source fact the PR's
# documents assert about the pinned processors and the parent. Read-only.
# Usage: pin_claims.sh <clone>
set -u
cd "$1" || exit 2
x() { echo "\$ $*"; "$@" | cut -c1-240; echo "[exit=${PIPESTATUS[0]}]"; echo; }
echo "head=$(git rev-parse HEAD) gptp=$(git -C gptp-processor rev-parse HEAD) pp=$(git -C protocol-processor rev-parse HEAD)"; echo
echo "## #511: no asymmetry input or tuner in the pinned gPTP processor"
x git -C gptp-processor grep -n -I -i asym -- . ':!docs/history/**'
x git -C gptp-processor grep -n -I -i -E 'uart_tune|tuner' -- . ':!docs/history/**'
echo "## #511: no parent asymmetry control"
x git grep -n -I -i -E 'delay_?asym|asym_|cfg_asym|asymmetry_ns|delayasymmetry' -- hdl sw configs avdecc scripts
x git grep -n -E 'parameter int unsigned (INGRESS|EGRESS)_LAT_NS_P' -- hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv
x git grep -n -A4 '_known_gp = ' -- sw/builder/endstation_builder.py
echo "## #510: processor MVU decode, parameters and harness arms"
x git -C protocol-processor grep -n -E 'MVU_GET_MILAN_INFO_C|desc_ty_r  == MVU' -- hdl/aecp/KL_aecp_engine.sv
x git -C protocol-processor grep -n -I -E 'MVU_SUID|MVU_MCR|EN_MVU|EN-MVU' -- hdl tb
x git -C protocol-processor grep -n -E 'P-EN-MVU-SUID' -- docs/architecture/01_overview.md
x git -C protocol-processor grep -n -E 'mvu\(MVU_PID_LO, 0x000[1-4]' -- tb/pp_top/sim_main.cpp
echo "## #394: one interface, one port, flags zero"
x git -C protocol-processor grep -n -E '^MILAN_FEATURES_FLAGS' -- hdl/aecp/ucode/gen_ucode.py
x git -C protocol-processor grep -n -E 'CHECK\(ff == 0u' -- tb/pp_top/sim_main.cpp
x git -C protocol-processor grep -n -E '\.N_IF_P +\(1\)' -- hdl/top/protocol_processor_top.sv
x git grep -n -E 'add_argument\("--eth-port"' -- sw/litex/milan_soc.py
x git grep -n -E 'number_of_redundant_streams' -- avdecc/aem_descriptors.py
