command -v tclsh >/dev/null
python3 syn/ooc/dp_srcs.py --selftest
python3 syn/ooc/ooc_tcl_selftest.py
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 syn/ooc/pp_baseline_reports_selftest.py
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null
python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null
