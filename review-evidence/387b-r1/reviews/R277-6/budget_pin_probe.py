#!/usr/bin/env python3
"""Check that the runner-contract pin accepts the live 3600 s milan_dp budget
and rejects a reversion to the historical 2700 s value.
Usage: budget_pin_probe.py <repo>"""
import pathlib, sys
repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
sys.dont_write_bytecode = True
from measure_test_evidence import runner_contract
live = (repo / "scripts/run_all_suites.sh").read_text()
ok_live = runner_contract(live) == []
rev = runner_contract(live.replace("SUITE_TIMEOUT:-3600", "SUITE_TIMEOUT:-2700"))
print("live_runner_accepted", ok_live)
print("reverted_2700_rejected", bool(rev), rev)
sys.exit(0 if ok_live and rev else 1)
