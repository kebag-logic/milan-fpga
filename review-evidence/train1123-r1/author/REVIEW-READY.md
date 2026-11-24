<!-- NOT POSTED. The lane STOPped (HANDOFF-r1.md, "The STOP"): two of #969's owner-ruled conditions break at 8x8/1if.
This is the comment to post on #665 once the owner has decided them and the same legs are re-graded. Everything below
"Open risks/questions" stands as measured. -->
[A828] REVIEW READY

Commit: `f5a1585e601cc627824b590c7f50351e3c8da18f` (branch `pf-train-1123`, for one PR -> `dev-soft-core`)

Changed: the one composition of the seven post-flip lab-fix PRs, each merged at its review-approved head with a merge
commit of its own:
- PR #958 (#956, #957) and PR #961 (#950, #954), already composed on `dev-soft-core` `854bd723` as `078c60fb`;
- PR #959 (#948) `64117b77`, PR #975 (#584) `3cda030c`, PR #971 (#969) `c113018d`, PR #978 (#973) `87b2fc0f` and
  PR #974 (#972) `77a74b2f`.

Every conflict keeps both sides:
- the four AECP plant tables;
- #950/#954's `Streams` and #969's `Early` sink fixtures (#969's two Python constants renamed apart);
- #969's and #973's SRP plants and campaign filters;
- every CHANGELOG entry;
- each PR's ledger history.

Combined figures are re-derived from measurement (`c2b2ba1a`):
- the 8x8 platform images at 59.5 and 64.5 RAMB36, `ctrl_plat` 19,136 and 21,888 B (S14 debt 3.5 and 8.5);
- the size fixture's 8x8/1if image at 57.5, its `declaring-outputs` arm 133,128 B of rom.

Two gate findings on the composed head are fixed:
- `ctrl_configs.OUTSIDE` now classifies #974's `sw/litex/mac_link_status.py`. #974's own head fails `ctrl_boundary`
  the same way.
- The firmware page's pin controls are 192, with #948's seven `milan_dp` targets.

The resolved texts are held to the idiom and docs gates. One CPU-budget statement is raised by the rule: 8x8/1if
`aecp_long` 320 -> 325 us, 30,948 CPU cycles, every owner bound held. No RTL, mailbox-contract or bound change by this
lane. The tsn-c-stack pin is unchanged at `715589c1`.

Validation (receipts: the lane's packet, `receipts/INDEX.md`):
- **Firmware gate**, 4 shards with plants: PASS at `c2b2ba1a`, with 2,003 live invocations and 0 escaped. Rerun at
  `f5a1585e`: **PASS** all four: 2,003 live invocations, shards 96/845/399/663; 96 + 844 + 398 + 664 `[ok]`, 0 escaped.
- **`ctrl_boundary --require-rv32 --selftest`**: PASS at `b6b2e603` (0 findings, 117 boundary, 192 pin, 4 figure
  controls). Rerun at `f5a1585e`: **PASS**: 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved.
- **Other firmware and builder gates** at `c2b2ba1a`: `fw_coverage` PASS (40 files); builder legs and union PASS (113
  gates).
- **Twin** (4 targets) at `c2b2ba1a`: PASS.
- **`plat_ledger`** at `c2b2ba1a` and `f5a1585e`: PASS with 0 findings, and the 24 image hashes are identical at the
  two heads. `test_ctrl_memory.py`: PASS.
- **Verilator suites** at `c2b2ba1a`, 0 failures in every one:
  - milan_dp, 14,379 checks;
  - milan_dp_render, tdm_render, avtp_rxmon, milan_dp_mclk and aaf_audio_loop, 3,626 checks;
  - nvm_backend and fw_service_budget;
  - the split boot (1x1, 8x8, 8x8/2if, controls, self-test), nvm_split_target (self-test, 1x1, 8x8) and
    `check_nvm_capture.py`.
- **Routes** at `c2b2ba1a` on the recipe (inputs equal to `f5a1585e`'s), #818's floor met at every corner:
  - 8x8/1if ExtraPostPlacementOpt: +0.105 / +0.036 ns;
  - 1x1/1if ExtraTimingOpt: +0.384 / +0.036 ns. Its ExtraPostPlacementOpt reached +0.019 on `KL_mbx` rx.
- **The formal CPU budget measurement** at 1x1/1if and 8x8/1if: every arm and every group, 490 groups.
  - Both statements the manager's ruling named are within: 1x1/1if paced 305 of 315 us, 8x8/1if long 900 of 1,720 us.
  - 1x1/1if: 0 statements exceeded.
  - 8x8/1if: `aecp_long` raised.
  - Owner bounds: loads 0.512 / 0.744, last notice 127.43 of 130 ms, ACMP 29.15, txL 47.98, THE TRANSMIT 76.86 of
    77 ms. THE SHARE is passed only by `srp-bound`'s passes, owed to #977.
  - Only the 7 known held-egress misses.
- **Harness tree checks and self-tests** at `f5a1585e`: **PASS**: load_grade, flip_grade (both points) and shape_costs `--check` PASS; the five `--selftest` rc 0; `run.py --self-test` 0 failures (360 MUTANT caught lines); test_ctrl_memory 0 failures.
- **Docs workflow steps** at `f5a1585e`: 56 steps rc 0, 24 SKIP (installs and hosted recorders); the 3 RV32 SDK install-verify steps refuse ("missing regular SDK provenance receipt", the environment, as on the bases); docs_check 0 findings, em-dash 0 over 801 added lines, every idiom gate PASS; tree clean after.

Acceptance criteria: each PR's own, carried unchanged by its approved head, and the composition's (manager [A10],
2026-11-23):
- (1) five merges, both sides kept, figures from measurement: met.
- (2) the statements by the rule: met for every statement (the two named are within). **#969's two conditions at
  8x8/1if: not met, see below.**
- (3) the formal measurement: met.
- (4) the gates: met.

Open risks/questions:
- **Two of #969's owner-ruled conditions break at 8x8/1if** on the composed image:
  - kept <= bound in arm A: kept Talker Failed 142,582 against bound 142,137 CPU cycles. At #969's head they were
    142,909 against 153,208; the bound path got cheaper.
  - A build pass in `answering-ports`: `srp-bound`'s build of one MRPDU, 171,645 against `CTRL_LOOP_BUILD_ONE_PASS_US`
    147,500.
  - The owner's decision is needed before review can clear.
- A scratch probe (not committed) shows the output map's 63-mapping edit at 1x1/1if: 176,099 cycles, 1,850 us, over
  the 975 that the input map's largest legal command states. The harness has never measured it there (#894's design).
  It is a candidate new Issue, not this composition's. At 8x8/1if the same edit is 1,435 us, within 1,720.
