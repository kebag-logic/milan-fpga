[A340] REVIEW READY

Commit: `104c8a54b183cd9215ed1e3a2e1be1634f48d33d` (local; not pushed).

Merged dev `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf` into `87e263fd1d71b1a7a04a2e9c9339220f35e4348f` with the assigned one-line subject. Processor `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` remains pinned; its history contains `0922e434`. Both changelog entries and both pins' ROM ledger rows are retained. SUBMODULES.md identifies the current pin and preserves the preceding adoption history. The repository generator regenerated the diagram and PNG manifest; they reproduce the implementation parent's bytes and passed visual and digest checks. Incoming CI and datapath documentation changes are preserved.

Validation on the merge (every required final command exited 0):

- `make -C tb/verilator/pp_shadow`: 520 + 520 + 520 + 159 checks. `pending-mutant`: clean control passes and the late-mark mutant fails both K10 and K12.
- `make -C tb/verilator/nvm_cosim`: 465 checks, all 39 named mutants killed. `make -C tb/verilator/nvm_backend`: 525 + 208 checks and four negative controls pass.
- `SUITE_TIMEOUT=10800 scripts/run_all_suites.sh <logs> --shard N/6`, all six chunks: 55 distinct suites, 2125050 checks, zero failures/timeouts. The full `milan_dp` default target passed 11206 checks.
- Full `sw/builder/test_builder.py` in both modes passes. SDK mode requires `--require-rv32` and audits 851 firmware compilations through the verified pinned compiler; absent mode hides all three cross candidates and compiles no firmware. The unchanged main program runs through an audited executable mapping. Both modes exclude the unavailable physical utilization report; only absent mode excludes the RV32 census.
- `syn/yosys/ooc.sh KL_pp_shadow`: 60766 LUT, 6136 LUTRAM, 30187 FF, 15 RAMB36, 4 RAMB18 and 6 DSP. This matches the preceding published post-fix LUT result: merge delta 0; the original correction remains -89 LUT against its published baseline. This round remeasured the merged head, not the historical baseline.
- Firmware self-test, capture and bare-metal gates pass. Firmware is unchanged, so no capture remeasurement was triggered.
- Both documentation CI modes pass. The [lane's complete documentation, CI-event, source-list, idiom, lint, port, naming and test-evidence gate set](https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5847390414) passes, including `check_em_dash --base 831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`. Front-end analysis and lint remain within their existing ratchets.
- `cd tests && behave --no-capture -f plain`: 344 scenarios and 1739 steps pass. Final diff and submodule checks: both worktree and base-to-head diff checks pass; parent and initialized submodules are clean.

Setup findings are recorded: the shared SDK had no provenance receipt, so a private copy was provisioned from the verified pinned archive; the default interpreter lacked the Markdown renderer dependency, so three refused gates were rerun with the prepared environment. No source or ratchet was changed to obtain a pass. Optional AAF/AVTP and gPTP field campaigns and their freshness checks were skipped because their generator is absent and contribute zero checks.

Acceptance: the assigned merge resolutions and local revalidation are complete. No new repository failure was found. No further RTL, firmware or test-source change was made. The original implementation's reporting-only limit remains: this adds no name/map materializer or flash-persistence claim.

HANDOFF.md records every conflict hunk with resolved file:line references, regeneration commands, full exits and logs. PR-BODY.md contains the complete proposed #502 body and merge-dev section. Independent review and hosted contexts remain outstanding. No push, PR operation, merge into dev, hardware operation, donor-source edit or other checkout was performed.
