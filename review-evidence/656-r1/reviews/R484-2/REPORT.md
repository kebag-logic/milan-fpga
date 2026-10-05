[R484] POSITIVE - exact head d0e29f6dda6f04f3ace1dbb395f57379e58cacaf

R484-2, internal independent delta review of issue #656 / PR #662. All five lenses are CLEAN. The sole previous MINOR, M1 = F2, is resolved by the PR-body correction. No new finding. This verdict covers the reviewed source and corrected body; it does not certify merge completion or hardware readiness.

Head: `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf`.
Tree: `289f09d8c7151617ffb019f49b5c972924e4fedd`.
Source base: `c0280fc008ef9c5c1650402a58bab3e47a92127b`.
Live dev observed: `e617275074e370cec342af99b929e2588fc8d43f`.

The review reconstructed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/656) and [frozen scope](https://github.com/kebag-logic/milan-fpga/issues/656#issuecomment-5985174558), requirements and interface authorities, then the complete source diff and two-commit history, then public executable evidence. The independent source pass preceded prior public findings. This round's own verdict and five-lens ledger were written before reading the external review report. No private author material or other checkout was read.

The four non-Docs lenses retain their CLEAN coverage from [R484-1 at this exact head](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986945006). Their scoped artifacts have not changed. This round checked that carry-forward independently against the diff, source and tree identity; it did not rerun the physical simulation leg.

The body comparison is exact, including whitespace. The [public original PR-BODY.md](https://github.com/kebag-logic/milan-fpga/blob/e5cae5f54a7efc54eb1b22095e310bb8324ace4e/review-evidence/656-r1/author/PR-BODY.md) is the published author artifact, without path redaction. Its SHA256 is `19d959618430f119f1313173309c578fee09efddd68597c808200014201b5c4d`; the live body is `2ab688eaaf2e8d06d22dfa90503fa1a337932d31e3254b1a8e4957fc29cf38a3`. Only the Known limitations bullet beginning "INTERNAL against an asynchronous talker" differs. The preceding 10,286 bytes and following 1,462 bytes are identical. See `receipts/body.diff` and `receipts/delta-check.json`.

The numerical correction agrees with the source model:

| Quantity | Recomputed result |
|---|---:|
| 48,000 events/s x 10 ppm | 0.48 events/s per fed pair |
| 48,000 events/s x 10.64 ppm | 0.51072 events/s per fed pair, approximately 0.51/s |
| Modeled FSYNC: 50,000,000 x 782 / 1591 / 512 | 47,999.4893148963 Hz |
| Actual modeled mismatch | 10.6392729939 ppm; 0.5106851037 events/s per fed pair |
| Actual modeled slip period | 1.9581538462 seconds |

`sim_ax1x1gptp.cpp:321` supplies the clock ratio and `:89` the 3,072-edge PDU cadence. `hdl/milan/milan_datapath.sv:5905` engages the aligner at INTERNAL; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:182` documents the per-pair queue, drop-oldest and repeat rules. `docs/reference/REGISTER_MAP.md:1994` distinguishes the two slip boundaries. The revised pre-A2-a clause now identifies this leg's old axis-paced talker. Before A2-a that talker matched the nominal packet grid, placing this modeled beat at the TDM junction. Other talker-rate mismatches could already produce loopback slips. The correction does not claim that A2-a introduced every asynchronous-talker slip.

Prior findings are disposed as follows. There is no open BLOCKER, MAJOR or MINOR.

- **M1 = R485-1 F2; MINOR; Docs; RESOLVED.** Artifact: PR #662, Known limitations, INTERNAL bullet, and [correction comment 5986948467](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986948467). Authority/evidence: the rate arithmetic and clock/queue contracts above. Impact of the former text: roughly 6% excessive rate scaling and an overbroad historical claim. Required outcome: 0.48 events/s per fed pair per 10 ppm, 0.51/s at 10.64 ppm, with the old TDM-junction clause limited to the old axis-paced talker. Verification: live-body byte comparison and independent arithmetic both PASS. The issue's immutable REVIEW READY comment retains its old coefficient; the public correction explicitly supersedes it.

- **S1 = R485-1 F1; SUGGESTION; Tests, Robustness; retained, optional and not taken.** Artifacts: `tb/verilator/milan_dp_gptp/verify_abort.py:76` and `tb/verilator/milan_dp/README.md:275`. Evidence: the exact 160-RX-PDU pin is unchanged; the new period is 6,250 + 26/391 axis cycles. R484-1 measured 159 completions for about 0.1702% of window phases and 160 at this head's deterministic phases. Impact: a later phase-moving change can cause a loud false failure, never a false pass. Optional outcome: document the phase dependence beside the pin, or accept the two legitimate RX counts while preserving exact zero TX/sample checks. Verification if adopted: 159/160 accepted, 158 and nonzero TX/samples refused, existing accounting still passes. No such change was made or required here.

- **R2 = R485-1 RES-1; RESIDUE; Docs; retained under the assigned prior disposition for #495 at merge.** Artifacts: `tb/verilator/milan_dp/README.md:287,297` and `tb/verilator/milan_dp_gptp/README.md:7,9`. These pre-existing prose summaries remain unchanged; the executable counts and measured transcripts are unchanged. Impact: stale summaries, with no consumer in the tests. Exact prose fixes: at `:297`, "The physical harness contributes 139 checks." At wrapper `:7`, "The normal total is 179 checks: 139 physical, 40 accounting." At wrapper `:9`, "Extended mode runs the physical harness alone, with 139 checks." Confirm the extended count when that mode is next run. At `:287`, "The trimmed scenario requires 16.992510280 simulated seconds over 849625514 cycles." Preserve the separate dated historical measurement at `:359`. Verification: compare the revised summaries with their measured transcripts and check the named lines. This round retains the explicitly assigned residue disposition; it does not generalize that disposition to new numerical or conformance defects.

The external [R485-1 findings](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986909374) were read after the independent verdict/ledger checkpoint. F2 is resolved; F1 and RES-1 are retained exactly as above. The formal-review and inline-review-comment lists were empty when inspected.

[R484] PASS Conformance - Issue #656 acceptance, scope comment 5985174558, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1133`, `REQUIREMENTS.md:235`, unchanged source diff - the test-model correction remains within frozen scope. Acceptance 1 and 2 and the local half of 3 retain R484-1 evidence. The hosted half of 3 remains pending and is not represented as passed.

[R484] PASS RTL - `hdl/milan/milan_datapath.sv:5905`, `hdl/ieee1722/aaf/KL_chan_map_capture.sv:182`, `receipts/source.diff` - the source diff still changes only the harness pacing and its documentation. No RTL, ports, registers, parameters or gitlinks changed; the clock and queue mechanism remains consistent.

[R484] PASS Robustness - `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:483,743`, `tb/verilator/milan_dp_gptp/verify_abort.py:76` - fixed-increment scheduling, the PTP reservation guard and reset re-anchoring are unchanged from the reviewed head. S1 stays optional and cannot cause false approval.

[R484] PASS Tests - `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:638,842`, public `head-driver-milan_dp_gptp.log`, `ctl-dev-noA2a.log`, `ctl-fix-noA2a.log` - no oracle, threshold, timer or comparison window changed. R484-1's H/C1/C2 coverage remains applicable. Public log hashes were independently checked against the immutable publication manifest.

[R484] PASS Docs - PR #662 corrected limitation bullet, comment 5986948467, `tb/verilator/milan_dp/README.md:173,200`, `docs/reference/REGISTER_MAP.md:1994`, `receipts/body.diff` - the coefficient and historical qualification are correct, the immutable earlier statement is publicly superseded, and M1 is closed.

Reviewer-owned coverage ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #656 acceptance and scope; `MEDIA_CLOCK_FOLLOWING.md:1133`; unchanged diff; R484-1 H/C1/C2; hosted physical skip | R484-1, preserved by R484-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| RTL | CLEAN | `milan_datapath.sv:5905`; `KL_chan_map_capture.sv:182`; exact tree, source diff and gitlinks | R484-1, preserved by R484-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Robustness | CLEAN | `sim_ax1x1gptp.cpp:483,743`; `verify_abort.py:76`; S1 optional | R484-1, preserved by R484-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Tests | CLEAN | `sim_ax1x1gptp.cpp:638,842`; R484-1 H/C1/C2; immutable public source logs and their hashes | R484-1, preserved by R484-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Docs | CLEAN | Live PR body; public original body; correction 5986948467; `REGISTER_MAP.md:1994`; body diff and arithmetic receipts | R484-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |

Evidence and limits:

- Eight selected immutable public logs matched their published hashes. The head source log records physical 139/0 and accounting 6/0, 20/0, 14/0; its driver and tally return 0. The first-bad parent/commit logs show 139/0 versus 139/3. Removing A2-a with old pacing passes; removing it with corrected pacing fails 139/5. These are inspected source receipts, not new simulation executions.
- Current hosted metadata records successful required contexts, five successful exhaustive simulation workers and four successful portability workers, including successful execution steps and aggregate reconciliation. "Physical gPTP (nightly and manual)" is explicitly SKIPPED, with no executed steps. See `receipts/hosted-checks.json` and [the exact-head run](https://github.com/kebag-logic/milan-fpga/actions/runs/37249252013).
- The manager's full source static/builder and native banks are supplied evidence, not rerun here. The selected public builder log explicitly says "ALL GATES PASS EXCEPT 1 NOT RUN"; its missing calibration-report arm is not covered. Source evidence at this head does not validate the final current-dev merge candidate.
- Physical calibration NOT RUN. No hardware, field run or licensed-streaming proof is supplied by this delta review. Field skips are not hardware proof. The ideal-following peer has no recovery jitter or wander; physical release obligations remain open.
- No simulation/compiler build, full bank, mutation campaign, container, local workflow replica, hardware action, source edit, commit, push, GitHub write, contact or delegation was performed. The pinned simulation executable was not invoked in this round.
- Byte/mode/index verification checked 1,009 superproject blobs and 790 required-submodule blobs. All index records match their commit trees at stage 0. Required pins: gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, protocol `631eeb342ca1e3fa80e734077a56a943aee76ff1`, stream library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Optional `external` remains uninitialized as on arrival. No tracked, untracked or ignored delta remains in the checked populations.

Pending manager duties:

1. Publish this report and obtain the external delta verdict; wait for every active review to finish.
2. Carry R2 to #495 at merge and preserve the public S1 optional/not-taken disposition.
3. Complete hosted physical acceptance 3 through an executed 139/0 run. Keep "Relates to #656" until the hosted obligation is met; then update closure state appropriately.
4. Own hosted/local workflow acceptance and validate the final candidate against current dev at the merge turn. The source base is `c0280fc008ef9c5c1650402a58bab3e47a92127b`; the observed live dev is `e617275074e370cec342af99b929e2588fc8d43f` and must be refreshed then.
5. Merge only with maintainer authorization, complete post-merge containment, then close/move the issue only when its completion requirements are satisfied.

Portable reproduction, all commands in the foreground:

```sh
python3 verify_delta.py <checkout> <packet>
python3 read_public_evidence.py <packet>
python3 verify_integrity.py <checkout>
```

These scripts and the raw receipts are enumerated in `MANIFEST.sha256`, relative to this packet. Full API responses and downloaded source logs stay under unpublished `scratch/`. Only manifest-listed files and REPORT.md are for publication.

R484-2 FINISHED
