R459-3 own independent pass, written before reading any prior review's findings (R458-1/2, R459-1/2).
Exact head b59e99cb928939f5c4089964dea8f4628d06ede7, tree 06d80d967d2c7baa550a66dd2572a787e8adead6.

Provisional per-lens result of the own pass: Conformance CLEAN, RTL CLEAN, Robustness CLEAN, Tests CLEAN, Docs CLEAN.
No BLOCKER/MAJOR/MINOR/RESIDUE found by the own pass.

Provisional SUGGESTIONS:
- S1 (Tests): probes wtsp-write-ignores-ready and wsid-ram-write-ignores-ready survive the committed walk arms;
  equivalent in the engine (KL_srp_top holds S_GATE/S_CTL with latched faces until accepted, so the last write lands
  on the accept cycle), but a walk arm that offers a gate/ctl op while the event bus holds ready low, with a different
  face before acceptance, would pin the module-level contract.
- S2 (Tests): the timer-arm FIFO builds (tb/srp_top storage) do not randomise unreset memories
  (no --x-initial unique / +verilator+rand+reset+2), unlike the walk-record builds; a FIFO word read before its push
  would read zero there.

Receipts at this point: suites/*.log (srp_top 4x15 + 2200; srp_stream_fsms 23/30/43/79 + 1219; srp_admission 5 shapes
to 991231), campaign/srp_top-campaign.log (126/126, 78/78), probes/SUMMARY.txt (9 caught, 3 equivalent), lockstep/
(28 runs x 400000 cycles, 7 new shapes, 0 mismatches; control caught), lint_focus.log (24/24), docs-*.log, marginal.txt.
