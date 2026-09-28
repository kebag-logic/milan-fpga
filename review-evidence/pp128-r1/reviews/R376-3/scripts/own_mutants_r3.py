#!/usr/bin/env python3
"""R376-3 reviewer mutants at 66451539, run through own_mutants_r2.main().

n05 hands the command turn back only after an EVC_INIT dispatch, so other event
classes could keep preempting commands. Usage as own_mutants_r2.py.
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("om", Path(__file__).resolve().parent / "own_mutants_r2.py")
om = importlib.util.module_from_spec(spec)
spec.loader.exec_module(om)
om.MUTANTS.clear()
om.MUTANTS["n05_turn_only_on_init"] = [(
    "      if ((state_r == S_IDLE) && disp_kind_w == DK_EV) begin\n        txn_turn_r <= 1'b1;",
    "      if ((state_r == S_IDLE) && disp_kind_w == DK_EV) begin\n"
    "        if (disp_code_w == EVC_INIT) txn_turn_r <= 1'b1;")]
raise SystemExit(om.main())
