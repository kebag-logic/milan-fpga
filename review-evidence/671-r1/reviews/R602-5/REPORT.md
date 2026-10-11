[R602] NEGATIVE - exact head 0c276b621d638c9a83e82f71fbf07bc153517bf7

# R602-5: internal cleared-context review of PR #715 (#671), round 5

- Head under review: `0c276b621d638c9a83e82f71fbf07bc153517bf7`, tree `85eb43d180dc240f5fa838e05dc6cbae6c7dd67a`. This is a delta review of five commits on `7bc7ceca` (`68f8a0364`, `af2165cb9`, `bd42818d3`, `de90ca768`, `0c276b621`), read with the full diff from the source base `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Assignment: [round 5](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6107082416), answering [R603-4-F1](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6107062972) and [R602-4](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6107063548).
- Order of reading: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #671 body and every manager comment; FASTCONNECT section 7, BAREMETAL_FIRMWARE (saved state), the host-suite README and SNAPSHOT_OWNERSHIP section 18; the diff and history; then the public evidence tree at `207a73a2` (`review-evidence/671-r1/author-r5`).
- Independence: I wrote my verdict and ledger (`receipts2/verdict_before_prior_findings.md`) before I read any prior review finding on this PR. I did not read the other reviewer's round-5 report on this head.

## Verdict

**NEGATIVE: one MAJOR is open (R602-5-F1, Tests and Robustness).**

The firmware answers R603-4-F1 correctly at this head:

- A refused read is now compared by its verdict, its byte count, a CRC-32 over all but its last four bytes, and those four bytes whole.
- Two different refused containers whose CRCs both close no longer collapse to the residue `0x2144df1c`.
- The three-read bound, validated-only generation, the fallback and the hold are textually unchanged.
- The sealed class runs in the standing suite, and the `r_digest_with_trailer` control fails by name on all three required shapes.
- The capture receipt binds the new firmware.

**The gap.** The fix depends on two comparisons, and the standing gate can fail for only one of them. Every fault the suite generates changes bytes before the trailer. None changes only the trailer, and none changes the bytes just before it.

**The evidence.** A one-line plant removes `a.tail == b.tail` from `nvm_reads_agree`. That brings back #671's loss: the cold boot acknowledges a commit and the clean reboot then loses 53 (1x1) or 163 (8x8) saved records. Checks 13 and 14, in full count, report 0 findings for that plant on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.

**Why it is open now.** The author's published handoff names this mechanism as load-bearing: "two views that differ only in their trailer also disagree. A digest over the prefix alone would have missed that case". [Round 2's ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6100704879) requires check 13 to be able to fail for every mechanism the fix depends on.

## Findings

### R602-5-F1 - MAJOR - Tests, Robustness - the trailer half of the refused-read comparison (and the bytes just before it) is pinned by no check that can fail

- **Artifact.**
  - Comparison: `sw/firmware/milan_baremetal/milan_baremetal.c:768-769` takes `digest` over `rd.bytes - KLJ2_TRAILER` and `tail` as the last four bytes. `:778-779` requires `a.tail == b.tail`.
  - Generator: `sw/firmware/nvm_hosttest/read_fault_cases.py:148-169` (`GROUPS`, `FLIPS`, `SEALED`) places byte faults only at offsets 0, 0x0B, 20 and the record area's middle byte.
  - Controls: `:21-119` (`READ_FAULT_MUTATIONS`) plant no defect in the tail comparison or in the digest's end bound.
- **Authority.**
  - [#671 round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6100704879), item 1: "the read-fault check must be able to fail for every mechanism the fix depends on". The [round-3 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6103025987) keeps that rule.
  - AGENTS.md section 6, Tests lens: "each new test can fail for the defect it claims to detect".
  - The round-5 design makes the trailer compare a separate mechanism, and the PR body states it: "A trailer-only difference is also told apart, which a prefix-only digest would miss". Before round 5 the whole-read CRC covered the trailer, so it needed no pin of its own.
- **Evidence.** All runs are at this head, through the tree's own `grade_fault_case`, `grade_read_faults` and `grade_refused_generation`:
  - `receipts2/probe_standing.log`: plant `no_tail` (the `&& a.tail == b.tail` term removed) gives `standing: findings=0 lost=0` on all three shapes. Plant `digest_short` (the CRC stops at `rd.bytes - 8`, so the four bytes before the trailer are compared by nothing) also gives `findings=0` on all three.
  - `receipts2/probe_sets.log`: my trailer set has 2,400 cases per shape. Each is a byte fault on the first trailer byte, the last trailer byte or the last byte before the trailer, for two or three reads, at every start in the 13-read cold and 12-read restart bound. Both orientations are covered, with the other slot blank or older, at every sequence the suite uses. Results:
    - head: 0 findings on every shape;
    - `no_tail`: 500 findings and 24 "was lost on the clean reboot" per shape;
    - `digest_short`: 250 findings and 12 losses per shape.
  - `trailer_in` (whole-read CRC with the tail compare kept): 0 findings, as expected. The tail and the whole-read CRC together determine the prefix CRC, so that plant is equivalent.
  - `receipts2/repro_no_tail.log` is a single case: slot A valid at 0x5A5A5, B blank, `--read-fault a:<img_len-4>:1:2:8`.
    - At the head, the boot reads A three times, accepts it, commits, and loses nothing.
    - With `no_tail` on a cold boot, the result is "slot A was taken as VD_CRC on reads that returned different bytes", "the boot read the flash 5 times, want exactly 7", then "53 other saved record(s) did not survive" (1x1) and "163" (8x8). On the restart path, A is taken as VD_CRC after four reads instead of six.
- **Impact.**
  - A natural simplification would pass every gate, including the hosted builder's writer gate: for a sealed container the tail equals the prefix CRC, so the tail term looks redundant.
  - That simplification reintroduces #671's lost commit for any transient fault confined to the CRC trailer.
  - The same holds for an off-by-four error in the digest's end bound.
- **Required outcome.**
  - The standing generated suite exercises reads that differ only in the trailer, and reads that differ only in the last bytes before it. This applies at least to the groups and windows that carry byte faults, on both entry paths and both orientations.
  - A named `--self-test` control that removes the tail comparison fails by its own words on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.
  - The host-suite README, the controls table and the counts follow.
  - The firmware itself needs no change.
- **Verification.**
  - `python3 -I scripts/probe_r602_5.py TREE WORK --mutants no_tail,digest_short --sets none --standing` must report findings on every shape, at minimum for `no_tail`.
  - `test_nvm_firmware.py --self-test` must stay green and list the new control on all three shapes.
- **Lenses.**
  - **Tests**: the gate cannot fail for this mechanism.
  - **Robustness**: the fault input class, a corrupted trailer or tail-adjacent bytes, is absent from the standing campaign. This is how R602-3-F1 was filed for the analogous window gap.
  - **Not Conformance or RTL**: the firmware behaves correctly on all 7,200 trailer cases and 4,800 extra sealed cases at the head, and the frozen acceptance items 1 to 3 are met by it.
  - **Not Docs**: no document or PR text claims the gate pins this mechanism, so no prose is false at this head.

### Retained SUGGESTIONs (optional, not blocking)

- **R602-4-S1** (Tests): the boot line's `read faults=` count is still graded by no check. `UNREAD_RE` group 1 is unused: `test_nvm_firmware.py` reads only group 2.
- **R602-4-S2** (Tests, Robustness): still no generated case faults both slots in one boot.

No RESIDUE is filed this round.

## Lens results

`[R602] PASS Conformance - sw/firmware/milan_baremetal/milan_baremetal.c:400-415,742-835 at 0c276b62 against #671 Required and Acceptance 1-3 and round-5 items 1-4; receipts2/selftest.log; receipts2/probe_sets.log (sealedalt: --read-sealed at offsets 28 (VD_SHAPE) and 36 (VD_REC), 1,600 cases per shape, 0 findings on 3 shapes); receipts2/check_claims.log`

- The round-5 firmware diff touches only `struct nvm_read` (a `tail` field), its two initialisers, `nvm_read_slot`'s refusal branch and `nvm_reads_agree`. The judgement loop, the re-stage, the pick, the fallback and the hold are textually unchanged.
- For a CRC-clean container the round-4 key was the constant `0x2144df1c` (`check_claims.log`: one value over 100 random sealed containers). The new key distinguishes 100 of 100.
- Distinct CRC-clean refusals then a clean read: the change survives with every record on both product shapes, both orientations, both entry paths and at the sequence boundaries. This holds in the standing class (32 of 32 group, orientation, path and sequence combinations covered; `check_claims.log`) and in my alternative-offset sealed set.
- The comparison is at least as fine as round 4's. Equal (prefix CRC, tail) implies an equal whole-read CRC, so no agreement round 4 refused is now accepted.
- Round-5 item 2 (Mark II): reported with `file:line` in the PR body and handoff. `sw/firmware/ctrl_nvm/nvm_store.c:142-149,165-173,208-216` chains one CRC over the header read and the whole-container read, compared by `vd`, `digest` and `bytes`. CRC is affine in its start state, so for a CRC-clean container that value depends only on the header read and the length, which bears out the report. It is unchanged here, as ruled.

`[R602] PASS RTL - git diff --name-only e8454e27..0c276b62 -- hdl protocol-processor gptp-processor syn constraints (empty); receipts2/clone_integrity.log (gitlinks unchanged); milan_baremetal.c:415 (static assert: the slot fits the stage), :744-770; receipts2/capture_gate.log; receipts2/cosim.log`

- No HDL, gitlink, register-map or record-format change.
- `rd.bytes - KLJ2_TRAILER` cannot underflow: `rd.bytes` is 40 on a header refusal and 44 to 65,536 otherwise. The `tail` load at `rd.bytes - 4` lies inside the bytes the read staged.
- The CRC is four bytes shorter and the tail is one word load, so boot time does not grow.
- **Capture receipt.** It binds the head firmware: SHA-256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed` is the file at this head. The measured commit `bd42818d` has tree `39e2b51cb67bc69bc7914116006d8d4076bf7792`, and only `measurements.json` changed after it in the firmware, harness and config paths. `scripts/check_nvm_capture.py` exits 0, and its four `--mutation` arms exit 1 (`capture_gate.log`).
- Co-simulation (`make -C tb/verilator/nvm_cosim run`, Verilator 5.050 verified): "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check".

`[R602] PASS Docs - docs/design/SAVED_STATE_FASTCONNECT.md:128,793-803; docs/integration/BAREMETAL_FIRMWARE.md:2021-2036,2179-2192; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626-1679,1831; sw/firmware/nvm_hosttest/README.md:9-12,47-55,109-150,194-216,261-270 at 0c276b62; receipts2/check_claims.log; receipts2/capture_gate.log; receipts2/docs_subset.log`

Each claim was checked against the code or recomputed:

- the comparison is described exactly as coded;
- the residue claim was recomputed;
- "always tells apart one or two bits or only within 32 consecutive bits" held in 12,000 sampled differences over a 64 KiB read, with 0 missed;
- 3,422 of 3,508 cases per shape (1,647 restarts, 1,775 cold boots) was recomputed from the tree's generator for all three shapes;
- nineteen and fourteen controls match the self-test transcript (49 "self-test OK" lines);
- the measured commit and tree, the firmware SHA-256 and the 10.42973 ms figure match the receipt.

Other docs checks:

- `docs_check.py`, `check_doc_style.py`, `check_feature_status.py --self-test`, `check_hygiene.py --check`, `check_nvm_record_space.py`, `check_baremetal_only.py --check` and `measure_test_evidence.py --check` exit 0.
- The em-dash gate could not run here because its pinned renderer is not installed (rc 2, recorded). No added line in the diff contains U+2014, and the hosted `docs-check` at this head succeeded.
- F1's required outcome will need README and table updates when the control lands, but no text at this head is false.

`[R602] MAJOR Tests - sw/firmware/nvm_hosttest/read_fault_cases.py:21-119,148-169; test_nvm_firmware.py:893-948 - R602-5-F1`

Otherwise examined:

- `nvm_host.c` `seal_slot` (`:543-556`): it reseals at the faulted view's length word and leaves impossible lengths alone. Each sealed read is distinct, because the XOR differs per read.
- `sealed_class` and `Expect.judgement`: the "ffc" window is taken from the model and not typed in.
- `settle()` (`nvm_host.c:515-529`) skips the walk only when `memcmp` finds every word equal, which is exactly when the walk would call nothing. It is equivalent by construction.
- The `r_digest_with_trailer` control plants both lines, and its anchors are unique.
- `receipts2/selftest.log`: rc 0, "OK across 5 shape(s), and every planted defect reddened", 49 controls, all 14 #671 controls on three shapes, `r_digest_with_trailer` caught by "on reads that returned different bytes". The run took 3 min 49.6 s at `--jobs 8`.

`[R602] MAJOR Robustness - read_fault_cases.py:148-169 (no trailer or tail-adjacent fault in the standing campaign) - R602-5-F1`

Otherwise examined:

- `receipts2/probe_sets.log`: the head is clean on 2,400 trailer and pre-trailer cases and 1,600 alternative sealed cases per shape, on three shapes. Every case runs a change, its commit and a clean reboot on both entry paths.
- A header refusal (40 bytes) keys on a 36-byte CRC plus the last header word.
- A length-word fault changes `bytes` and so disagrees.
- The hold, wipe and retire paths are unchanged in this delta.

## Completion ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_baremetal.c:400-415,742-835`; #671 acceptance 1-3; round-5 items 1-4; `selftest.log`; `probe_sets.log` (sealedalt); `check_claims.log`; `ctrl_nvm/nvm_store.c:142-216` (item 2 report) | R602-5 | `0c276b621d638c9a83e82f71fbf07bc153517bf7` |
| RTL | CLEAN | `git diff --name-only` over `hdl`, the submodules, `syn` and `constraints` (empty); `clone_integrity.log`; `milan_baremetal.c:415,744-770`; `capture_gate.log`; `cosim.log` | R602-5 | `0c276b621d638c9a83e82f71fbf07bc153517bf7` |
| Robustness | UNCLEAN (R602-5-F1) | `read_fault_cases.py`; `nvm_host.c` fault model; `probe_sets.log`; `repro_no_tail.log` | R602-5 | `0c276b621d638c9a83e82f71fbf07bc153517bf7` |
| Tests | UNCLEAN (R602-5-F1) | `read_fault_cases.py`; `test_nvm_firmware.py`; `nvm_host.c`; `selftest.log`; `probe_standing.log`; `repro_no_tail.log`; `cosim.log` | R602-5 | `0c276b621d638c9a83e82f71fbf07bc153517bf7` |
| Docs | CLEAN | FASTCONNECT 7 and table; BAREMETAL_FIRMWARE saved-state and host-suite text; SNAPSHOT_OWNERSHIP 18; host-suite README; `check_claims.log`; `docs_subset.log`; hosted `docs-check` | R602-5 | `0c276b621d638c9a83e82f71fbf07bc153517bf7` |

## Prior public findings: disposition at this head

| Prior IDs | Disposition | Evidence at this head |
|---|---|---|
| R603-4-F1 (MAJOR) | RESOLVED | The comparison no longer collapses CRC-clean refusals: residue recomputed, 100 of 100 keys distinct. The class is in the standing suite: 32 of 32 combinations, 64 class cases per shape. `r_digest_with_trailer` is caught by name on 3 shapes (`selftest.log`). My independent sealed probe at offsets the suite does not use is clean at the head. R603-4's own probe script was not run by me. The author reports it fails its own defect assertion, so that statement is author evidence only. The gap in the fix's other half is the new R602-5-F1, not a reopening. |
| R602-4-S1, R602-4-S2 (SUGGESTION) | RETAINED, optional | Not taken up, as the PR body states. |
| R602-3-F1 / R603-3-F1, R602-3-F2, R603-3-S1, R602-3-S1; R603-2-F1 / R602-2-F1, R603-2-S1, R603-2-S2, R603-2-R1, R602-2-S1, R602-2-R1; R603-1-F1, R603-1-F2, R603-1-S1 to S3, R603-1-R1; R602-1-F1, R602-1-S1 to S3, R602-1-R1 to R4 | RESOLVED (unchanged since the round-4 dispositions) | Round 5 touches none of their artifacts except the controls' anchors, which follow the new text. In my run, all 14 #671 controls are caught by name on all three shapes: `restart_at_zero`, `unbounded_retry`, `generation_from_refused_slot`, `verdict_only_agreement`, `r_digest_header_only`, `r_fill_from_flash`, `r_restage_fail_offers_none`, `restage_fail_not_unread`, `r_restage_any_seq`, `r_reattach_goes_live`, `r_judge_four_tries`, `p_restage_unbounded`, `r_restage_four_tries` and `r_digest_with_trailer`. |
| R603-2-OBS-1 / R602-2-S2 (prefill) | RETAINED OUTSIDE SCOPE | It is #717. |

## Limits

- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof. All execution here is on the host model and the co-simulation.
- **Host toolchain.** The host model ran under CPython 3.14.7 and host GCC 16.2.1, not the author's 3.12.3. Wall times were taken on a shared, heavily loaded host and are not comparable to the hosted limit.
- **Not reproduced here:**
  - the capture measurement itself; I re-graded the receipt only;
  - the firmware size delta (+96 B text), because I did no pinned RV32 SDK build;
  - the builder bank, the firmware-unit and Mark II suites, and the 10,581-run `settle()` twin campaign. I judge `settle()` equivalent by construction.
- No manager source bank exists at this head, and I claim none. Source-head execution evidence is the author's published receipts plus this packet's focused runs.
- Hosted checks at this head (`receipts2/hosted_checks.tsv`): 22 executed contexts completed `success`, including `docs-check`, `rtl-fast`, `firmware-unit`, `verilator-suites` and `yosys-portability`. `Physical gPTP (nightly and manual)` was skipped. The manager owns hosted and act acceptance.

## Pending manager duties

- Carry R602-5-F1 to the lane.
- File the Mark II (`ctrl_nvm`) refusal-digest collapse as its own Issue, as round 5 item 2 ruled. My read-only search found no such Issue filed yet.
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `6bfeeb13`) with the builder and native banks at the merge turn, and link its receipts.
- Accept the hosted and act evidence.

## Receipts

Everything listed in `MANIFEST.sha256` is under `receipts2/` and `scripts/`. The scripts take the tree and a work directory as arguments and run against any checkout of this head:

- `scripts/probe_r602_5.py`: trailer, sealed-alternative and standing-suite runs under three plants;
- `scripts/repro_no_tail_r602_5.py`: the single-case reproduction;
- `scripts/check_claims_r602_5.py`: the residue, detection-claim and case-count arithmetic.

R602-5 FINISHED
