[A537] REVIEW READY

Commit: `42f654478c11bd8f2b070969d83140587190f276`
Branch: `661-pp-pin-ead80360`, based on `506d91dbeeba585d72d2e80d92fca799c719f8ee`.

Changed: processor gitlink `631eeb34` -> `ead8036035affd53ef4b29979190f2f4f67084c0`; the four supplied adaptations, in order and with exact patch-tree equivalence; the P2 amendment, duplicate L6/L10 cleanup and ADP_STATUS note; every pin-derived record; resource baseline D and its per-block comparison with C. There are 21 one-line commits. The processor source, parent RTL, firmware and SoC interfaces are unchanged.

Capture: `python3 scripts/check_nvm_capture.py` returns 0. Census and firmware digest match the retained receipt; the 8x8 maximum is 13.86484 ms, below 24.5 ms. No re-measurement was required.

Resources: the route and both standalone endpoints completed under the shared lock and pass `pp_resource_gate.py check`. Policy fields are unchanged. The route fits at 50 MHz with WNS/WHS +0.108/+0.036 ns, 50,318 LUT, 54,214 FF and 15,789 slices (61 free); all 100,970 routable nets are fully routed, with zero routing errors. Against C: -449 LUT, -5,420 FF, -43 slices and -5 RAMB36s. Standalone 1x1 is 23,178 LUT / 19,776 FF; 8x8 is 29,853 / 27,370. The authoritative finding explains the processor PRs' measured deltas and distinguishes predecessor #653's contribution. This completes #639's re-baseline and #234 criterion 2; the manager's remaining-criteria record leaves only that criterion. The 60 percent LUT target remains #640.

Validation at this head:

| Command / campaign | Result |
|---|---|
| `scripts/run_all_suites.sh $VALIDATION_STORAGE/661-a537/parent-suite-logs` | rc 0; 59/59 suites, 2,149,002 checks, no failures or timeouts |
| `bash protocol-processor/scripts/run_suites.sh` | rc 0; 33/33 suites, 1,021,627 checks, no failures; processor-compatible sv2v 0.0.13 |
| `make -C gptp-processor -j16 contract tb lint` | rc 0, including the default mutation controls |
| `syn/yosys/run.sh --results $VALIDATION_STORAGE/661-a537/yosys-pinned-results` | rc 0; 55/55 tops, both structural checks, exact tally and fresh cache controls; required ABC revision `5d51a5e420f5de493d07bf61109a977248c86ffb` |
| Every shell step of `.github/workflows/docs.yml` | 49/49 rc 0, each under GNU Make 4.3; whole `test_builder.py --require-rv32` included |
| All 17 consumer commands | rc 0; exact commands and receipts in HANDOFF.md |
| Real `xvlog_gate.py --check` and `--selftest` | rc 0; 73 parent + 52 pinned-processor files, two existing budgeted processor findings; live planted control passes, no missing-tool skip |
| `pp_shadow`; full `nvm_cosim`; explicit NVM lint/quick | rc 0; shadow 2,169 checks; co-simulation 465 checks and all 39 mutants killed; quick 315 checks |
| BDD, LiteX and resource instruments | rc 0; 404 scenarios / 1,968 steps, 4/4 LiteX simulations plus controls, all 174 resource mutants killed |

Pinned Verilator 5.050 was used throughout. The parent lowering uses sv2v 0.0.12. Original environment/setup attempts and their successful replacements are separately recorded; none is silently counted as a pass.

The assigned exceptions reproduce exactly at base and head: #656's physical gPTP simulation returns rc 2 with 139 checks / 3 failures at both; #657's full render campaign returns rc 2 with the same 28 PASS / 4 FAIL outcomes across all 32 controls. The separate physical abort-accounting verifier passes at both. No test or threshold was changed.

Coverage limits: the parent sweep declares four `tsn_fuzz` skips (two optional-generator field campaigns and their freshness checks), contributing zero to its count. The whole builder declares two NOT RUN arms: the ineffective `MAKEFLAGS += -e` mutation under Make 4.3 and the absent historical calibration report. These are disclosed in the packet, not claimed as coverage.

Acceptance criteria: met within the assigned author scope, including the authorized #656/#657 exceptions. No STOP condition was reached. Both worktrees are clean. The only processor change is the gitlink.

Evidence packet: `2026-09-23/661-a537/HANDOFF.md`, `PR-BODY.md`, per-gate and per-suite receipts, the exact 49-step documentation ledger, resource deltas/digests, patch equivalence and exact base/head verdict comparisons. Raw logs and measurement checkpoints remain under `$VALIDATION_STORAGE/661-a537`; large artifacts are represented by size and SHA-256 in the packet. The PR body uses Closes #661, Closes #639, Closes #234, Relates to #629 and Relates to #229.

Reviewers: internal [R486], external [R487]. This is author evidence, not a review verdict. No push, PR operation, merge, hardware access or bench operation was performed.
