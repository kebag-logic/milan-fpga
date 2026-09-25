[A311] REVIEW READY

Commit: `b376f6113b388929fe82e883d400e5361319b966` (local `545-crf-servo-slew`). Parents: reviewed lane `92ad1687d84ff077f872719b4f1df601f82064d2` and requested dev `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.

Merged the assigned dev head. Both changelog sections and all applicable campaign rows remain. The gPTP pin is `5dce647a`, the processor pin is `990f9652`, and initialized submodules match the gitlinks. The repository generator rebuilt the submodule master, SVG, PNG and manifest; direct and A4 renders were visually checked. ROM digest re-recording reproduced the merged ledger. No product code was manually changed during resolution.

Validation:

- Clean `taskset -c 8,9 make -C tb/verilator/mmcm_servo`: rc 0, 944.14 seconds; 100 unit, 8 rail, 113 step and 90 slew checks. Local margin: 855.86 seconds (47.5%) of the unchanged 1800-second budget.
- `make -C tb/verilator/crf_rx`: rc 0; 13,836 unit, 1,658 discontinuity and 69 connected checks; mutation campaign 8/8.
- `make -C tb/verilator/gptp_shadow -j8`: rc 0; 309 checks, nine mutation controls and lifecycle gate.
- Connected gmstep leg: 58/58. `make -C tb/verilator/milan_dp gmstep-mutants`: rc 0, 16/16.
- `make -C tb/verilator/mmcm_servo slew-mutants`: rc 0, 10/10; both positive controls pass and all eight defects fail their named checks.
- Default `milan_dp` run sweep: all 34 expanded commands returned 0 in foreground chunks 0-9, 10-20, 21-26 and 27-33. The clock-ratio leg passes 144/144; default render and gmstep campaigns pass 6/6 and 4/4.
- `python3 sw/builder/test_builder.py`: rc 0. NOT RUN: gate 11 real placement-report calibration, because its required report is absent. No compiler arm was skipped.
- Both docs-check CI modes, `check_em_dash --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7`, doc style, TOC/anchors, doc paths, traceability, diagram/pin checks, frontend analysis, source lists, SV/C++/Python idioms, RTL lint, port contracts, naming and test-evidence checks: all rc 0. Existing ratchets unchanged.
- `cd tests && behave --no-capture -f plain`: rc 0; 344 scenarios / 1,739 steps. `git diff --check`, dev-to-head whitespace check and final root/submodule cleanliness checks: rc 0.

Repository OOC recipe reproduces 864 -> 871 LUT / 790 -> 792 FF for the servo, plus 1 LUT / 4 FF for isolated release alignment. These blocks are unchanged by the merge, so their merge-round delta is zero. The combined isolated parent addition remains +8 LUT / +6 FF; this is not a whole-datapath measurement.

The assigned A311 packet contains HANDOFF.md with every conflict resolution and file:line reference, exact gate receipts and chunked sweep commands, plus the full locally updated PR-BODY.md. No new validation failure was found. The local merge head awaits the assigned delta review; no independent-review or hosted-CI verdict is claimed. No push, PR edit, dev merge, other lane, submodule edit, delegation or hardware action was performed.
