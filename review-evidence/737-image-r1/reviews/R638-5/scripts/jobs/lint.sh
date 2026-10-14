. /jobs/lib.sh
step "Verilator version proof" 'VERILATOR_VERSION=v5.050; /opt/verilator/bin/verilator --version; /opt/verilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"'
step "Ratcheted whole-tree lint gate" 'PATH="/opt/verilator/bin:$PATH" python3 scripts/lint_rtl.py --check --self-test'
step "Prove protocol-processor source lists are derived" 'python3 scripts/pp_srcs.py --check --selftest'
