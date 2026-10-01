[R428] NEGATIVE - exact head 78d4fef220c0ad4873a89b138828c0543c2bcad0

# R428-1: internal cleared-context review of PR #631 (#629, lane M1, design only)

- Head `78d4fef220c0ad4873a89b138828c0543c2bcad0`, tree `3fba1fdc1c8f172d7d744d18da1e4d4c4afadf55`, one commit on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb` (also the live dev tip when this round read it).
- Diff: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new, 577 lines) and its row in `docs/README.md:72`. No RTL, builder, model, config or processor change.
- Read in order: AGENTS.md, CONTRIBUTING.md, docs/README.md; #629's body, the lane M1 assignment (5935051587), the TAKEN (5935072991), the DECISION (5935490330) and the rulings (5935520588); the clause texts; the diff and history; the code at `d4dd7426` and the processor at its pin `b2db3a97`; the published evidence at `0c17547b` `review-evidence/629-r1/` (the hashes match its MANIFEST).
- Prior public review findings on PR #631: none. At this round's start the PR held only the two INDEPENDENT REVIEW STARTED notices, so nothing carries over to resolve or retain.

## Verdict in one paragraph

Most of the page holds up. The clause reading in (a) is right, the code map is accurate (one citation points at a banner rather than the logic), the A2 analysis is right, W2 and the holdover rules agree with the servo's state machine, and the area basis reproduces exactly. Six MINOR findings are open, and they leave all five lenses unclean:

- D1's main rationale rests on a saved-state restore that this repository refuses across the very `entity_model_id` change the design makes (F1).
- The meter's input contract is not established: the decimation rule disagrees with the accept rule, and the AAF timestamp-quality assumption has no basis (F2).
- D5/C1 reverses a recorded rule without saying so (F3).
- The test plan misses a check the page itself promises, and has no D5 case (F4).
- Part (b) states a design choice as a clause obligation (F5).
- The page is not current with the rulings already made on it (F6).

## Clause judgments (asked items a to d)

- **(a) Agreed.** Milan v1.2 5.3.3.6 sets a minimum: exactly one INPUT_STREAM source per CRF input, or one for the single AAF input when no CRF input exists, and INTERNAL when outputs exist. It neither lists nor forbids a source on an AAF input beside the CRF input's. IEEE 1722.1-2021 7.2.9 (Table 7-17, "sourced from the media clock of an Input Stream") permits the location. 7.2.32 (Table 7-61) caps `clock_sources_count` at 216, which is (508 - 76) / 2, and sets no order. The identity-permutation order rule is the processor's own.
- **(b) The outcome is sound, but the classification is overstated.** Indefinite holdover with the index kept is permitted. Free-wheel is supported by 1722-2016 4.4.4.7 NOTE and by 10.6 for a lost CRF stream, which the page does not cite. But "must keep the selection" is a clause obligation only while a controller holds the entity lock (Milan 5.4.2.15). The "need not be seamless / any appropriate action" quotations in 4.4.4.3 and 10.4.3 describe the reaction to a signalled `mr` restart, not a stopped stream. See F5.
- **(c) Agreed on the literal text.** The 4.4.4.3 third paragraph and 10.4.3 name CRF only. The source-change toggle and the 8-PDU hold are mandatory for AAF (PICS F.7 AAF-5, AAF-6). Only the stream used for recovery counts (4.4.4.3 last paragraph, 10.4.3 last paragraph). The 10.8 phase limit of +/-5 % (+/-1,041.7 ns at 48 kHz) is quoted correctly. Applying the disruption and echo triggers to a followed AAF stream is a reasonable design choice. An alternative reading is worth recording (S1).
- **(d) Items 1, 3, 4, 6 and 7 are verified as stated. Item 2's corrected basis is right, and item 5 is defensible.**
  - The BAD_ARGUMENTS refusal follows from 7.2.32's list together with Table 7-141. 7.4.23.1 adds only the "current value on failure" rule.
  - Milan 7.2.2 requires a CRF input and restricts no source.
  - Milan 7.2.3 requires only that the output exists. The A2 basis on 7.2.32 ("a source of a common clock signal") with Table 7-8 (7.2.6: "the Clock Domain providing the media clock for the Stream") is correct, and both outputs name CLOCK_DOMAIN 0 (`avdecc/aem_descriptors.py`, `d_stream`).
  - Item 2's list is incomplete: two more places credit 7.4.23.1 with the membership test (S3).

## Code map

Every citation was re-read at `d4dd7426`. The full table is in `receipts/citation_check.md`. All are accurate except these precision points (S3):

- The restore check is cited at the `KL_aecp_nvm_writer.sv:86-90` banner; the compare itself is at `:501-503`.
- The Limits citation `endstation_builder.py:3936-3955` starts one line early.
- The servo's "814 LUT / 789 FF" comes from a shape-unknown record. It reprices at 871 LUT / 792 FF at this head.

## Design judgments

- **D2 meter: right units, unproven input.**
  - At spf 6, one PDU in 16 gives the 96-sample, 2 ms spacing.
  - The 256-entry ring difference has `KL_crf_rx`'s units (ns per 512 ms), so the servo needs no change.
  - The 32-bit ring arithmetic is exact modulo 2^32.
  - Not established: the accept and decimation rules, and the jitter tolerance the meter inherits (F2).
- **D3 W2: matches the servo.** HOLDOVER is entered on any reference lock fall (`KL_mmcm_drp_servo.sv:562-564`). It leaves for ACQUIRE with a two-window skip and the lock count cleared, the integrator kept (`:571-579`). PI and lock are held while the rate is invalid (`:611-615`). The one-cycle unlocked presentation is needed and correct, but no test grades it (F4).
- **Lock loss, holdover and `mr`.** These agree with the servo (no timeout, trim frozen), with `KL_crf_rx`'s 8-in/100 ms-out lock, and with `KL_media_clock_restart`'s merge of a request landing on a pending one, so each disruption and each switch gives one toggle. "Under following this fixes A2" holds while the TDM feed is live (S2).
- **D4, the A2 options.** The analysis is correct. A2-a reverses the recorded INTERNAL free-run rule (`milan_datapath.sv:5713-5718`, `KL_media_grid_align.sv:38-41`), and the page says so.
- **D5 / C1.** The edges of one level keep Milan 5.3.11.2's invariant structural. But C1 reverses the recorded LOCKED-equals-tu rule without saying so (F3).
- **Area.** The basis reproduces exactly: `ooc.sh KL_crf_rx` at the 1x1 TDM8 shape gives 433 LUT, 544 FF, 1 RAMB18, 147 CARRY4. The meter's 250-350 LUT / 200-300 FF is a plausible scaling once the ten 32-bit Table 5.6 counters and the interval logic are removed. Both are out-of-context synthesis estimates, as the page says.
- **Bench plan.**
  - B AAF grades AAF following correctly: the tone is captured in the DUT's clock domain and sent to a peer on its own clock, so any following error shows as slips.
  - B6's THD+N method resolves single-frame slips. At 0.1 ppm over 10 min it would see about 3 frames.
  - B INTERNAL and the synthetic controls are present.
  - The lock-loss row does not read the CLOCK_DOMAIN counters D5 changes (F4).

## Findings

```text
[R428] MINOR Conformance, Robustness, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:267-268, :552 - D1's saved-selection rationale does not hold
```

**F1**

- **Requirement/evidence:** The page recommends L1 because "a unit whose saved selection (Milan v1.2 5.3.11.1) is CRF restores onto CRF after the update". It argues against L2 because "a saved CRF selection, index 1, would restore onto AAF input 0". But the same design moves `entity_model_id` on every regenerated image (`:470`, `:557`; all five shipping configs are `entity_model_id: hash-derived`). The saved-state container is refused whole when its model id differs:
  - `sw/firmware/milan_baremetal/milan_baremetal.c:634-636` returns `VD_SHAPE`;
  - `docs/design/SAVED_STATE_FASTCONNECT.md:638-640`: "an image from a different shape is refused by identity";
  - `docs/design/SAVED_STATE_MATERIALIZATION.md:1153-1158`: the clock-source restore rule is defence in depth "for a configuration that pins its id; no shipped configuration does".

  So no saved selection crosses the update under either order.
- **Impact:** D1 was ruled (#629 5935520588) on a benefit that does not exist. The page also omits the real consequence of D6: at this update every unit drops its saved clock source and returns to the image default (INTERNAL), along with every other saved record. The FR and bench text written from this page would carry the wrong expectation. L1 may still be right on its other ground (index 1 keeps meaning CRF for controllers across images).
- **Required change:** Restate D1's basis without the restore claim, or confine that claim to a pinned-id configuration. Record that the source-set change discards saved state across the update: Milan 5.3.11.1 persistence holds within one image, not across a model change. Let D1 and D6 be re-confirmed on that basis.
- **Verification:** The page text at the next head, checked against the three sites above.

```text
[R428] MINOR RTL, Robustness, Tests - docs/design/MEDIA_CLOCK_FOLLOWING.md:281-282, :297-311, :518-521 - the AAF meter's input contract is not established
```

**F2**

- **Requirement/evidence:**
  - **(i) Accept and decimation disagree.** The accept rule admits any `spf` dividing 96, and decimation picks by `sequence_num` modulo 96/spf. `sequence_num` wraps at 256 (IEEE 1722-2016 4.4.4.6). For spf 1, 2, 4, 8, 16 and 32, 256 is not a multiple of 96/spf. Picks across the wrap are then 32 or 64 samples apart, the 2 ms spacing rule restarts the history on every wrap, and the rate never becomes valid (`receipts/meter_model.out`, part 1). This is latent today, because shipping listeners advertise only spf 6 (`avdecc/aem_descriptors.py:133`; Milan v1.2 6.2 Table 6.1). But the stated contract is self-inconsistent.
  - **(ii) Timestamp quality is assumed.** The page asserts that one AAF timestamp in 16 "is therefore the same measurement a CRF PDU carries". It reuses `KL_crf_rx`'s adjacent-spacing jump bound of 2,048 ns, which that module derives for a CRF talker with "Arrival/network jitter is absent here" and remote quantisation under 384 ns (`KL_crf_rx.sv:279-294`). No basis is given for AAF talkers. IEEE 1722-2016 4.3.2 and 4.3.3 bound transmit timing, not presentation-time jitter. A desk model with independent uniform per-timestamp jitter (`receipts/meter_model.out`, part 2) gives these rate_valid fractions:
    - 99.9 % up to +/-750 ns;
    - 49 % at +/-1,000 ns with a 100 ppm offset;
    - 0.08 % at +/-1,250 ns.

    A talker past that cliff is never followed: the servo stays in ACQUIRE with PI held while GET_CLOCK_SOURCE reads the AAF source.
  - **(iii) The test plan checks neither.** The meter suite (`:518-521`) uses ideal synthetic timestamps only.
- **Impact:** AAF following could fail on real talkers that a CRF-grade bound rejects, and nothing planned before the bench would show it. The bench grades one peer.
- **Required change:**
  - State the AAF timestamp-quality assumption with a basis (a clause, or a measurement of the reference peer's AAF stream).
  - Choose and justify the meter's spacing bound or break rule for AAF.
  - Make accept and decimation agree: accept only spf with 256 mod (96/spf) = 0 (spf 6 at 48 kHz), or decimate by an accepted-PDU count.
  - Add meter-suite cases with jitter at and beyond the bound, and a refused non-6 spf, each with a failing mutant.
- **Verification:** The page and its test-plan rows at the next head.

```text
[R428] MINOR RTL, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:415-428, :556 - D5/C1 reverses a recorded rule without saying so
```

**F3**

- **Requirement/evidence:** `hdl/milan/milan_datapath.sv:3469-3475` records CLOCK_DOMAIN LOCKED = ~tu as a deliberate rule: "One clock-validity authority, two views; a LOCKED count that disagreed with the tu bit on the wire would be two answers to one question." Under C1, a followed source in HOLDOVER counts UNLOCKED while every outgoing AVTPDU still carries tu = 0. That is the disagreement the rule forbids. The page cites these lines (`:224`) and says the current definition "is not wrong". It does not say that C1 reverses the rule, whereas it does flag D4's reversal (`:408`, `:555`).
- **Impact:** D5 was accepted (#629 5935520588) without that being visible, and the parent-visible change list omits the banner rewrite.
- **Required change:** State the reversal and why it is acceptable, or give an option that keeps one authority. List the `:3469-3475` rewrite among the root changes.
- **Verification:** The page text at the next head.

```text
[R428] MINOR Tests - docs/design/MEDIA_CLOCK_FOLLOWING.md:351, :477, :509-546 - test-plan gaps against the design's own promises
```

**F4**

- **Requirement/evidence:**
  - **(a) The W2 promise has no test.** For W2 the page says "the one-cycle presentation is what prevents it, so a test grades it" (`:351`). No row grades it at the root:
    - the `mmcm_servo` row drives the servo directly, so the testbench supplies the unlock;
    - the `milan_dp` switch row grades `mr`, the recentre, the aligner and `SLIP_TDM`, not HOLDOVER then ACQUIRE on a switch onto an already-locked CRF;
    - no mutant removes the presentation.
  - **(b) D5/C1 is untested.** It was accepted, yet nothing grades the domain LOCKED/UNLOCKED counters across holdover, return and switch, or Milan 5.3.11.2's LOCKED = UNLOCKED (+1) invariant. The lock-loss bench row (`:545`) does not read them either.
  - **(c) The registers are untested.** The two new read-only CSR words (`:477`) have no case.
  - **(d) One mutant's symptom is wrong.** The "decimation by 1: the rate is off by the decimation ratio" mutant (`:518`) misstates its failure. Under the page's spacing rule (`:307-309`), 125 µs picks restart the history at every pick, so rate_valid never rises.
  - **(e) One "mutant" is not a mutant.** The AECP model-walk row's mutant (`:527`) is a builder refusal, not a mutant of the graded SET acceptance and BAD_ARGUMENTS check.
- **Impact:** These are checks named by the design, or by an accepted decision, that the plan cannot show failing.
- **Required change:** Add cases with named failing mutants for (a), (b) and (c). Correct (d). Give (e) a real mutant, for example a regenerated list whose RTL decode table is stale.
- **Verification:** The page's test-plan table at the next head.

```text
[R428] MINOR Conformance, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:71-99 - (b) states a design choice as a clause obligation
```

**F5**

- **Requirement/evidence:**
  - Milan v1.2 5.4.2.15 forbids a non-ATDECC clock-source change only "If the PAAD-AE is locked by a controller".
  - 5.3.11.1 requires that a listed source is in use and that the current source is saved, and states that "The PAAD-AE is able to dynamically change the clock source". Neither clause forbids an autonomous fallback while the entity is unlocked.
  - The "Recover any way it sees fit" bullet (`:94-96`) quotes 4.4.4.3 and 10.4.3. Both describe a listener's reaction to a talker-signalled media clock restart, not a stopped stream.
  - The text that does cover a lost CRF stream is 1722-2016 10.6: "the media clock free-wheels until the CRF stream resumes".
- **Impact:** The page is the stated basis for the FR-CLK-03/04 amendments (`:467`). An over-read "must" would enter normative text as a clause obligation, which is the defect class (d) exists to remove.
- **Required change:**
  - Separate what the clauses require from what this design chooses. The clauses require: a listed source is in use, the selection is persisted, and nothing changes it by non-ATDECC means while locked. The design chooses: no fallback at any time.
  - Cite 10.6 and the 4.4.4.7 NOTE for free-wheel.
- **Verification:** The page text at the next head.

```text
[R428] MINOR Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:6, :437, :482-484, :548-562 - the page is not current with the rulings on it
```

**F6**

- **Requirement/evidence:** After this head, #629 comment 5935520588 ruled on the page:
  - accepted D1-D3, D5 and D6;
  - filed D7 as #632;
  - filed the processor part as protocol-processor #141;
  - sent D4 to the owner.

  The page still says the processor issue "is to be filed with the decision" (`:482-484`) and that D7 "should be a new issue" (`:437`), and it lists all seven decisions as requested. AGENTS.md section 7 requires authoritative documentation to be current at merge.
- **Impact:** The merged page would tell the implementation lanes it governs that settled questions are open and existing issues are still to be filed.
- **Required change:** Before merge, record each ruling with its link, keep D4 marked as pending the owner, and name #632 and protocol-processor #141 where the page proposes them.
- **Verification:** The page at the next head; the links resolve.

### Suggestions (optional, do not affect coverage)

- **S1 (Conformance), `:115-118`, `:157-160`.** PICS F.7 AAF-5 ("mr toggled when the device's media clock source has changed", 4.4.4.3 first paragraph) can be read to cover a followed AAF stream's loss when the entity falls into holdover. On that reading, #629's "applies to AAF and CRF alike" is defensible rather than wrong. The design outcome is the same; consider softening (d)5.
- **S2 (RTL, Docs), `:398-402`.** "Under following, this design fixes A2" holds while the TDM feed is live. The aligner's feed watchdog (`KL_media_grid_align.sv:95-100`) disengages on a dead feed, and the packet grid free-runs. State the condition, as the A2-a row already does.
- **S3 (Docs), citation precision and completeness:**
  - restore compare at `KL_aecp_nvm_writer.sv:501-503`, not the `:86-90` banner;
  - Limits rule at `endstation_builder.py:3937`;
  - servo 871 LUT / 792 FF at this head (`receipts/ooc_KL_mmcm_drp_servo.log`);
  - the builder change list omits `_load_names`' refusal of `names.clock_sources.stream` (`endstation_builder.py:3784-3790`), which the restored stream name needs;
  - the servo port rename also touches the `tb/verilator/mmcm_servo/` harnesses;
  - (d)2 omits L6's "IEEE 7.4.23.1" in `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`, and the processor's `07_memory_maps.md:135` and `gen_ucode.py:1414`, all of which credit 7.4.23.1 with the membership test.
- **S4 (Docs), `:267`, `:552`.** "Index 1 keeps meaning CRF on every shape" holds where both INTERNAL and a CRF sink are declared, which is all five shipping shapes. A listener-only shape without INTERNAL puts CRF at 0 (`endstation_builder.py:5034-5044`).

### Observation outside this diff (for the manager)

- **O1.** `avdecc/aem_descriptors.py:456` emits `clock_source_flags = 0x0002` with the comment "(STREAM_ID)". IEEE 1722.1 Table 7-16 gives STREAM_ID = 0x0001 and LOCAL_ID = 0x0002 (the field values are legible in the 2013 text, and the 2021 table has the same bits). Milan v1.2 5.3.3.6 leaves the value unimposed, so this is not a conformance defect. But the label is wrong, and the per-AAF sources this design adds would inherit it. Candidate for its own issue, or a decision in the model lane.

## Lens coverage at this head

| Lens | Applied to (artifacts) | Result |
|---|---|---|
| Conformance | Page `:51-168` and `:263-273` against Milan v1.2 5.3.3.6, 5.3.11.1-2 (Tables 5.7, 5.15), 5.4.2.15-16, Tables 5.4/5.6, 6.2, 7.1-7.4, 7.6.2, Annex B; IEEE 1722.1-2021 6.2.2.8, 7.2.6 (Table 7-8), 7.2.9-7.2.9.2, 7.2.32 (Table 7-61), 7.4.23-7.4.24, Table 7-141; IEEE 1722-2016 4.3.2-4.3.3, 4.4.4.3, 4.4.4.6, 4.4.4.7, 10.4.3, 10.6, 10.8, PICS F.7 | UNCLEAN: F1, F5 |
| RTL | Page `:200-461` against `milan_datapath.sv` (every cited range), `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv`, `KL_media_grid_align.sv`, `KL_crf_tx.sv`, `KL_aaf_packetizer.sv`, `KL_media_clock_restart.sv`, processor `gen_ucode.py`, `KL_aecp_nvm_writer.sv`, `KL_aecp_dyn_state.sv`, firmware KLJ2 verification | UNCLEAN: F2, F3 |
| Robustness | Lock loss, holdover, return, switch and update/restore paths; spf and sequence wrap; timestamp jitter (`receipts/meter_model.out`) | UNCLEAN: F1, F2 |
| Tests | Page `:509-546`, simulation and bench tables, against the design's own promises and the accepted decisions | UNCLEAN: F2, F4 |
| Docs | The whole page, `docs/README.md:72`, the gates (all rc 0, `receipts/gates.rc`), the privacy scan (no host, peer, switch or instrument named) | UNCLEAN: F1, F3, F5, F6 |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | the page's clause findings against the clause texts listed above | R428-1 | 78d4fef220c0ad4873a89b138828c0543c2bcad0 |
| RTL | UNCLEAN | the page's current state and design against the cited RTL, the processor at b2db3a97, and the firmware | R428-1 | 78d4fef220c0ad4873a89b138828c0543c2bcad0 |
| Robustness | UNCLEAN | holdover, switch, restore and meter-input paths; the desk model | R428-1 | 78d4fef220c0ad4873a89b138828c0543c2bcad0 |
| Tests | UNCLEAN | the page's test plan (simulation and bench) | R428-1 | 78d4fef220c0ad4873a89b138828c0543c2bcad0 |
| Docs | UNCLEAN | `docs/design/MEDIA_CLOCK_FOLLOWING.md`, `docs/README.md`, docs gates | R428-1 | 78d4fef220c0ad4873a89b138828c0543c2bcad0 |

## Executed evidence (this round)

- **Docs gates, rc 0 each** (`receipts/gate_*.log`, `receipts/gates.rc`). They ran in a fresh environment pinned from `tools/markdown/requirements.txt` with hashes:
  - `docs_check.py`: 0 findings over 184 md + 955 scrubbed files;
  - `check_doc_style.py`;
  - `gen_toc.py --check`;
  - `gen_toc.py --verify-anchors`: 292 links;
  - `check_em_dash.py --base d4dd7426...`: 0 findings over 578 added lines;
  - `check_doc_paths.py`: 871 paths;
  - `check_feature_status.py --self-test` and `check_feature_status.py`;
  - `git diff --check d4dd7426 HEAD`.
- **Area:** `ooc.sh KL_crf_rx` and `ooc.sh KL_mmcm_drp_servo` at the 1x1 TDM8 shape, rc 0, single tops only (`receipts/ooc_*.log`).
- **Desk model:** `scripts/meter_model.py` (standard library only, deterministic seed), rc 0 (`receipts/meter_model.out`).
- **Clone integrity:** after every probe, the clone was verified at the exact head (`receipts/restore_check.txt`). HEAD, tree and index tree are `3fba1fdc`; worktree and index are identical to HEAD; the status is empty with no untracked files. The submodule gitlinks are external `efeb541a`, gptp-processor `5dce647a` and protocol-processor `b2db3a97`, with both checked-out submodules clean. No file in the clone is newer than this round's start.
- **Hosted, snapshot 2026-10-01T16:27Z** (`receipts/hosted_checks_at_head.txt`):
  - success: `rtl-fast`, `changes`, `elaborate`, `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`;
  - in progress: `docs-check`;
  - skipped contexts, which are not evidence: `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, shards, physical gPTP.

## Limits

- This is a desk review of a design. The proposed RTL does not exist, so nothing proposed was simulated.
- `meter_model.py` is a model of the page's stated rules with an assumed jitter shape. It is not a measurement of any talker.
- The clause texts were read from text extractions of the standards. Table field values in 1722.1-2021 Table 7-16 were confirmed against the 2013 text.
- The processor was read only at the pin `b2db3a97`.
- No bench, hardware, container or local CI replica was used. Physical calibration was not run, and skipped hosted contexts are not hardware or exhaustive-gate proof.
- The manager's full source, static, builder and native banks at this head are the manager's evidence, as stated in the assignment. They were not rerun here.

## Pending manager duties

- Completion of the hosted `docs-check` at this head, and the hosted and local-replica acceptance.
- The candidate merge result on current dev at the merge turn.
- The second, external review (R429-1) and its verdict.
- Re-review of F1-F6 at a new head.
- The owner's D4 decision.
- Whether to file O1.
- The baseline PR #630 is still open; the page cites it through the PR.

R428-1 FINISHED
