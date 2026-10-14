. /jobs/lib.sh
step "Yosys version proof" 'YOSYS_VERSION=v0.66; test -x /opt/yosys/bin/yosys-abc; echo "bundled ABC: $(cat /opt/yosys/ABC_REV)"; yosys -V; yosys -V | grep -F "Yosys ${YOSYS_VERSION#v}"'
step "sv2v version" 'sv2v --version'
step "Elaborate the integration-heavy tops" 'syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow'
step "OOC read sets" 'command -v tclsh >/dev/null
python3 syn/ooc/dp_srcs.py --selftest
python3 syn/ooc/ooc_tcl_selftest.py
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 syn/ooc/pp_baseline_reports_selftest.py
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null
python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null'
step "ooc.sh ROMs" 'python3 syn/yosys/ooc_selftest.py'
step "guard selftest" 'python3 syn/yosys/guard_selftest.py'
step "cache selftest" 'python3 syn/yosys/cache_selftest.py'
