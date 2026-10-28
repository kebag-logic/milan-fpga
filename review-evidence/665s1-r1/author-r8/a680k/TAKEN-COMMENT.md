[A680k] TAKEN
Branch: `665-s1-faces` (PR #795), on head `bdad673a7824d84c922d771ff5950e8f69083c27`
Authoritative references: ruling issuecomment-6463964028 (items 1 and 2); #791; #801
Interpreted scope: the harness's `as-built` control (`tb/verilator/ctrl_service_budget/run.py`) is caught by an access fault of cause 1 (instruction) or cause 5 (load), either being #791's decode defect; self-test checks (with planted mutants) that a trap of any other cause, or no trap, is still refused, and a real planted control: the `as-built` control on a build whose CPU decodes correctly (the clean image) must print ESCAPED. README updated to match. The PR body states arm B's 1x1 T_svc miss and 8x8 ceiling with #801 as the cause. No other change.
Validation plan: harness self-test; the `as-built` control at 1x1 (caught) and its planted clean-image control (ESCAPED); docs gates; the gates the harness change touches.
Blockers: none
