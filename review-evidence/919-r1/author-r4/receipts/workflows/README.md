Workflow jobs at 1a1e6665, step by step, each job on its own fresh clean clone of the head (run_wf.py, as in rounds
2 and 3). The step list is read from the workflow at the head.

- `verify-1a1e6665.md`: every `run:` step of rtl-fast.yml, elaborate.yml and docs.yml. 89 steps ran, each rc 0
  with a log naming the head; 159 not run, each with its stated reason; 0 bad.
- The reasons are the hosted-only reasons (GitHub's step context, artifacts and tokens) plus one per job rounds 3
  and 4 did not re-run (`not_run-rounds3-4.json.txt`, keys `rtl-fast.yml/<job>`): verilator-lint, bdd-conformance,
  yosys-tool, yosys-elaboration, publication-census and split-cdc, because afa3ea19 -> 1a1e6665 changes no RTL or
  RTL tooling; firmware-aecp-mutants and firmware-srp-mutants, because they plant AECP's and SRP's sources, which
  neither round changes (`../head/files-changed.txt`). Round 2 ran each at afa3ea19, rc 0. They are 29 steps.
- Jobs run: rtl-fast changes, firmware-unit (`test_ctrl_firmware: PASS`; the ratchet `ctrl_plat_phy.c 178/178
  164/164`, `firmware coverage: PASS (40 files)`), firmware-control-mutants (`mutants: 769 of 769 caught`,
  `test_ctrl_firmware: PASS`), firmware-verilator, firmware-boundary; elaborate-gates-0, elaborate-gates-1,
  elaborate; docs.yml's six jobs.
- Batches (`batch-*.log`): A docs, B rtl-fast's firmware jobs, C the control campaign on the session's own 8-CPU
  slices; D elaborate-gates-0 and E elaborate-gates-1 with the aggregate on ranges cpu_ranges.py picked.
  firmware-boundary and the elaborate jobs ran with the product LiteX venv.
- docs-check-no-git's three steps are rc 0 (`docs_check: 0 finding(s) across 219 md files`); its batch log ends in
  the runner's own traceback after the steps, because the job strips the clone's git metadata by design.
- One log over 200 KB is recorded by size and sha256 in `large-logs.sha256` (docs-gates-2 gate_41, rc 0).
- `logs/`: the step logs and rc files, host paths replaced by placeholders.
