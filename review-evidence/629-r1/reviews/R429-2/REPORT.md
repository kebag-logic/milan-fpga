[R429] NEGATIVE - exact head c554ae51b1dcc2285863f0f0117cb025971a594c

# R429-2: external re-review of PR #631 (issue #629, lane M1, design only)

- **Head under review:** `c554ae51b1dcc2285863f0f0117cb025971a594c`, tree `20c142998c6802e6c6730adfb814ec2a001af7b4`. Four commits on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`: round 1's `78d4fef2`, then `4845f158` (the round-2 answers), `49899572` (three tightened statements) and `c554ae51` (the shape-header glob fix).
- **Diff:** `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new, 884 lines) and its design-index row in `docs/README.md` (+1). No RTL, builder, model, configuration or processor change.
- **Reconstructed from**, in this order:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - #629's body; the lane M1 assignment (5935051587); the rulings on round 1 (5935520588); the round-2 assignment (5935864862); the round-2 DECISION (5936327987); the round-2b assignment (5936355573); and the REVIEW READY (5936429406).
  - The clause texts: Milan v1.2, IEEE 1722.1-2021 and IEEE 1722-2016, from the same local copies as round 1, with identical hashes.
  - The code at `d4dd7426` and the processor pin `b2db3a97`.
  - The diff and its history.
  - The public evidence on branch `629-review-evidence` at `02b4f38d`: `review-evidence/629-r1/author-r2` (with `meter_rules_model.py` and its output) and `author-r2b`. The pinned tree `0c17547b` holds only round 1's `author/` packet; the round-2 packets are at the branch tip.
- **Prior public findings** (R428-1 and my own R429-1) were read only after my own pass over the diff. Each is resolved or retained [below](#prior-findings-resolved-or-retained).

**Verdict: NEGATIVE, on three open MINOR findings (N1 to N3).** Every round-1 finding is answered in substance:

- The meter's input contract is now right: the 48 kHz base format, samples per PDU from `stream_data_length`, groups of 16 by `sequence_num` modulo 16, and a 4,096 ns bound that validates a 10.8 talker and still rejects a real step.
- The `mr` re-seed rule is right.
- The clause wording in (b) and (c) matches the texts.
- The page is current with #632 and protocol-processor #141.
- The gates pass, including `check_entity_shape.py`.

What remains is the evidence offered for the meter and for the switch test:

- **N1:** the desk model's "group" error shape alternates per group, and the 256-pick ring cancels any period-2 pattern exactly. So "the two shapes bound the cases" is false. Correlated 10.8-sized error fails the servo's 2 ppm lock test in 25 to 77 % of windows, and the mean does not help.
- **N2:** the model omits the page's own in-group void rule, so the +/-2,500 ns row is wrong.
- **N3:** one of the switch row's named mutants cannot fail its on-wire check, and the other fails only for about half of the switch phases.

## Contents

- [Focus questions](#focus-questions)
- [Findings](#findings)
- [Suggestions](#suggestions)
- [Prior findings resolved or retained](#prior-findings-resolved-or-retained)
- [Executed evidence](#executed-evidence)
- [Ledger](#ledger)
- [Limits](#limits)
- [Pending manager duties](#pending-manager-duties)

## Focus questions

### The AAF meter's input rules (page `:389-459`)

- **48 kHz base format only.** Milan v1.2 6.2 and Table 6.1 fix PCM, 32-bit depth, and NS = 6 samples per PDU at 48 kHz, with one timestamp per PDU in normal mode. The page's `format` INT_32BIT, `nsr` 48 kHz and `sp` clear (`:412-414`) match. They also match the advertised format `0x0205022000806000` (`avdecc/aem_descriptors.py:133`), which decodes to subtype AAF, `nsr` 5, format 2, depth 32, 2 channels and 6 samples per frame.
- **`stream_data_length` = 24 x channels.** This is correct for 4-octet containers: IEEE 1722-2016 7.3.5 requires the same number of samples in every AVTPDU of a stream. The field is in the parser's `fsh` word (`avtp_stream_parser.sv:176-177`). The RX monitor indeed does no sample-count check (`KL_avtp_rx_monitor_ctx.sv:486-491`).
- **The sparse-mode refusal** matches 7.2.4 and 7.5 (a timestamp in every eighth PDU).
- **Groups by `sequence_num` modulo 16.** `sequence_num` is 8 bits (4.4.4.6), and 16 divides 256, so the groups stay aligned across the wrap.
- **The group mean.** The formula at `:451` is exact modulo 2^32. Truncation is common to every pick. The in-group worst case at the design point is 2 x 1,426 + 15 x 125,000 x 300e-6 = 3,414.5 ns, inside the 4,096 ns void bound (`receipts/probe_meter_rules.out` section C), so the void rule never fires on the stated design error.
- **The 4,096 ns bound.** It is derived as `KL_crf_rx` derives its own (`KL_crf_rx.sv:279-294`: 601 ns drift plus 2 x 384 ns). 10.8 Equation (15) bounds the offset to the CRF timing points to +/-5.0 % of a sample period, and the CRF quantisation adds 384 ns. 2 x 1,426 + 601 = 3,453 ns, rounded up to 4,096.

### Do the bound and the mean pass the servo's 2 ppm lock test under 10.8-sized error, and still reject a real step?

**Step rejection: yes.** My probe applies the page's rules, including the void rule, with +/-1,426 ns independent error at 300 ppm and 64 step positions per size (`receipts/probe_meter_rules.out` section D):

| Step | Steps caught |
|---|---|
| 1,024 and 2,048 ns | 0 of 64 each |
| 3,000 ns | 1 of 64 |
| 4,096 ns | 63 of 64 |
| 6,000, 10,417 and +/-20,833 ns | 64 of 64 each |

A one-sample step is always caught: a step inside a group voids it, and a step at a group boundary breaks the spacing. The page's "a sub-bound phase step is followed as a transient" is accurate.

**Rate validity: yes.** For every error shape within +/-1,426 ns, `rate_valid` reaches the run's ceiling of 0.9957.

**The lock test: only for error that is independent per PDU, or that wanders slowly.**

- I re-ran the author's desk model, and it reproduces its published output byte for byte (`receipts/author_model_rerun.out`).
- Its "group" shape gives every group a sign that alternates group by group. The servo's error is `pick[k] - pick[k-256]`, and 256 is even, so the shape cancels exactly and reports 1.000 whatever its amplitude.
- 10.8 Equation (15) bounds the magnitude of the offset only; it sets no spectrum. With the rules as stated (B = 4,096 ns, P2, void on), the fraction of 512 ms windows inside 1,024 ns is:

| Error shape, peak J per timestamp | J = 1,042 ns | J = 1,426 ns |
|---|---|---|
| independent per PDU | 1.000 (P1: 0.748) | 1.000 (P1: 0.615) |
| alternating per group (the page's "group") | 1.000 | 1.000 |
| one uniform draw per group | 0.752 | 0.607 |
| one random sign per group | 0.483 | 0.483 |
| sinusoidal wander, 1 s period | 0.321 | 0.226 |
| sinusoidal wander, 2 s period | 0.483 | 0.342 |
| sinusoidal wander, 5 s and 20 s periods | 1.000 | 1.000 |

P1 and P2 give the same figures for every correlated shape. With a closed loop at the servo's gains (KI 1/2, KP 1/4; `KL_mmcm_drp_servo.sv:227-228`), even independent +/-1,426 ns error leaves 0.953 of windows inside, not 1.000. That is a simplified loop on an ideal plant. See N1.

### `mr` on a followed-input change (page `:540-546`, `:626-650`)

**The design is right.**

- An era starts at a change of the followed listener and at entry into AAF following.
- The lock clears in one cycle with no disruption trigger, and the received `mr` is seeded silently, as `KL_crf_rx` seeds its own (`KL_crf_rx.sv:380`).
- The switch is then declared by the source-change edge alone (`KL_media_clock_restart.sv:211-213`, `:230`), so it raises exactly one request.
- The decode, the restart module and the servo all run on `axis_clk` (`milan_datapath.sv:1560`, `:5596`), so the one-cycle unlocked presentation of W2 is seen by the servo FSM, which evaluates every cycle (`KL_mmcm_drp_servo.sv:564-568`).

**The switch test is not dependable** (see N3). I probed `KL_media_clock_restart` on the pinned simulator 5.050 with one AAF-rate output and one CRF-rate output, and a second request after a switch (`receipts/probe_mcr.out`):

- **No second request** (the design): exactly 1 toggle per output in 229 of 229 phases.
- **A second request 1 to 4 cycles after the edge** (the "disruption trigger unmasked" mutant, because the era-start lock fall is immediate): a second toggle in 8 of 916 trials. Those 8 needed a PDU report inside the gap, and the probe's period is 100 cycles; at the real 100 MHz fabric clock and 125 us period the gap is a few cycles out of 12,500.
- **A second request 0 to one PDU period after the edge** (the "no re-seed" mutant, the new input's first PDU): a second toggle in 1,355 of 2,748 trials.

### The test-plan gaps named in round 1

All are closed except the switch-row mutants (N3):

- **Decimation by 1** now fails as stated (`:808`): 125 us spacings restart the history at every pick, and every rate row asserts `rate_valid` (`:802-804`).
- **The AECP-walk mutant** is now a real fault (`:825`): a stale decode table leaves an accepted index decoding as no source, so the "servo leaves IDLE" check fails.
- **The W2 root presentation** (`:819`), **the D5 counters** (`:823`) and **the CSR words** (`:824`) each have a row and a mutant.
- **The true-ratio leg** (`:818`) has distinct offsets (+20 and -15 ppm) and a mux-stuck mutant.

### Clause wording in (b) and (c) (page `:81-162`)

The wording matches the texts:

- **5.3.11.1.** Milan v1.2 5.3.11.1 reads "At any given time, a Clock Domain must be using one of the associated CLOCK_SOURCE descriptors. The PAAD-AE is able to dynamically change the clock source ... The current clock source shall be saved".
- **5.4.2.15.** Its prohibition applies only "If the PAAD-AE is locked by a controller", and covers changes "by non-ATDECC means".
- **The 1722-2016 phrases.** "Need not be seamless" and "any appropriate action to minimize the disruption" (4.4.4.3 first paragraph, 10.4.3) now sit under the received-toggle case only (`:129-132`, `:140-143`).
- **Free-wheel.** 10.6 and the 4.4.4.7 NOTE are cited for it.
- **PICS AAF-5 and AAF-6** read "Is the mr field toggled when the device's media clock source has changed?" and "a minimum of eight (8) AAF AVTPDUs", both AAF:M.
- **No fallback** is now stated as this design's choice (`:111-127`, `:613-616`, `:859-862`).
- **(d) item 8 is correct.** IEEE 1722.1-2021 Table 7-16 puts STREAM_ID at bit 15 and LOCAL_ID at bit 14.

One reading is weaker than it needs to be (S1).

### The page and the rulings

- **#632 and protocol-processor #141** are named and linked at `:20-28`, `:718` and `:767-770`, and both resolve. #632 is "Phase-align the recovered media clock ...", OPEN; protocol-processor #141 is "SET/GET_CLOCK_SOURCE over INTERNAL, CRF and one source per AAF input (milan-fpga #629)", OPEN.
- **The Decisions table** (`:847-857`) gives each decision its state: D1 and D5 re-opened, D4 with the owner, D2, D3 and D6 ruled, and D7 filed.
- **D2's ruled wording** "keeps one AAF timestamp in 16" is changed by P2 to "keeps the mean of each 16". The DECISION comment records this "for the record". The page says only "Round 2 fixes the meter's input contract inside it" (`:379-380`) and does not quote the ruling's words (S2).

### D1 and D5 on their merits

- **D1 (L1, CRF at index 1).** The saved-state reason is rightly withdrawn:
  - `milan_baremetal.c:634-636` returns `VD_SHAPE` on a model-id mismatch;
  - `SAVED_STATE_MATERIALIZATION.md:1153-1158` says the clock-source restore rule is defence in depth "for a configuration that pins its id; no shipped configuration does";
  - `endstation_builder.py:3414-3419` puts the source set in the model shape.

  The remaining ground holds: the CRF index stays 1 independent of the listener count. The procedures and checks the page names do pin index 1 (`test_builder.py:19588`, `milan_soc.py:872-874`, `mmcm_servo/sim_main.cpp:197`). The case against L1 is stated fairly, and no clause orders the list. L1 is supportable.
- **D5.** The options are presented fairly, and the reversal of the recorded rule is explicit. Its provenance is verified: commit `c947acd8d` (2026-08-14, VERSION 0x0047) wrote the banner, and `c92159ac9` (2026-09-02) first let the stored source reach the media plane.

  On the merits, C1's stated cost, "at most one pair per about 2.5 s" on a servo excursion, assumes excursions are rare. Under N1, a conformant talker whose error is correlated on sub-3 s scales makes them routine, and C2 does not count them. The C1/C2 choice should be made on corrected evidence. This is part of N1's required outcome, not a separate finding.
- **D4** stays with the owner and is not judged.

### Gates

All are rc 0 at the head in this clone:

- `python3 scripts/check_entity_shape.py`: `RESULT: PASS`, arm I included (`receipts/gates/check_entity_shape.out`).
- The Markdown gates in the pinned environment: `docs_check` (0 findings), `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors` (292 links), `check_em_dash --base d4dd7426` (0 over 885 added lines) and `check_doc_paths` (874 paths).
- `git diff --check d4dd7426 c554ae51`.

**The glob fix discriminates.** In detached worktrees, arm I lists the design page's line (`/gen/adp_shape_defaults.svh ... outside the tracked tree`) at `49899572`, and does not list it at `c554ae51` (`receipts/gates/check_entity_shape_at_49899572.out`, `..._head_in_worktree.out`). Those worktree runs have no submodules checked out, so both stop with the builder's submodule error after arm I and carry the same Makefile resolution entries. Only the differential on the page's line is used.

The five named copies are exactly what `git ls-files 'configs/generated/*/gen/adp_shape_defaults.svh'` lists.

### Linkage and privacy

- "Relates to #629" is on the page (`:6`) and in the PR body. Nothing says Closes or Fixes.
- The public-text scan of the added lines finds no hit (`receipts/public_text_scan.out`, with a planted-address positive control). The page names only "the reference peer".

## Findings

### N1: MINOR (Robustness, Tests, Docs). The desk model's "group" shape is cancelled by the ring, so the page's lock-test claim is unsupported for correlated error

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md`:
  - `:510-516`: "Two error shapes bound the cases: 'group' gives every PDU of a group the same sign, alternating per group, the shape no averaging removes";
  - the table at `:518-524`, group rows, windows 1.000;
  - `:526-529`: "the mean keeps independent error out of the servo's lock test";
  - the D5 C1 cost at `:694`;
  - bench B AAF's "Servo LOCKED" at `:837`.
- **Authority and evidence:**
  - The servo samples `pick[k] - pick[k-256]` once per 512 ms. One window outside 1,024 ns zeroes `lock_cnt_r`, and LOCKED falls to ACQUIRE (`KL_mmcm_drp_servo.sv:232`, `:648`, `:567-568`, `:689-694`).
  - The model's group shape alternates sign per group (`author-r2/meter_rules_model.py`, `picks()`: `jit if (n // GROUP) % 2 == 0 else -jit`). A lag of 256 groups is even, so the pattern cancels exactly. The same holds for its "alt" shape under P1, because every pick is at an even PDU.
  - IEEE 1722-2016 10.8 Equation (15) bounds only the magnitude of the offset to the CRF timing points, not its spectrum.
  - With the page's rules, correlated error at the 10.8 amplitude leaves 0.226 to 0.752 of windows inside the lock threshold, with P1 and P2 identical (`receipts/probe_meter_rules.out` section A). The shapes tried are: one draw per group, one random sign per group, and 1 s and 2 s wander. Wander of 5 s or longer passes.
  - Separately, a closed loop at the servo's gains gives 0.953, not 1.000, for independent +/-1,426 ns. The page's 1.000 assumes the local clock follows exactly, as the model's docstring states.
- **Impact:**
  - The page presents B2 + P2 as passing the lock test for a talker at the 10.8 limit. It does so only when that talker's error is independent per PDU or wanders slower than a few seconds.
  - For a conformant talker whose phase error is correlated over 2 ms to about 3 s, the servo would leave LOCKED in a quarter to three quarters of windows.
  - Under the recommended C1, each exit moves the CLOCK_DOMAIN counters, and bench B AAF's "Servo LOCKED" could fail on a conformant peer.
  - D5's C1/C2 comparison and the bench pass criterion rest on the unsupported claim.
- **Required outcome:**
  - The desk evidence includes correlated shapes that are not period-2, such as one draw per group and wander between 0.5 and 5 s.
  - The page states what holds: the mean removes per-PDU independent error, and does nothing for error correlated across a group or wandering on sub-3 s scales.
  - The consequence is carried into D5's C1 cost and comparison, and into B AAF's pass criterion. That may be by stating it as a limit or by a design change; the choice is the lane's.
- **Verification:** the revised model output and page text at the next head. Correlated rows must not read 1.000 without an explanation that holds under a random-sign shape.

### N2: MINOR (Robustness, Tests, Docs). The desk model omits the page's in-group void rule, so the +/-2,500 ns row is wrong

- **Where:**
  - `:524`: "independent, +/-2,500 ns, 0 ppm: ... B2 + P2 valid 0.996, windows 0.987";
  - the void rule at `:457-459` ("so does any `|ts_i - ts_0 - i * 125,000|` above the jump bound").
- **Authority and evidence:**
  - `meter_rules_model.py` never voids a group; it applies only the adjacent-spacing test.
  - With independent +/-2,500 ns error, `|ts_i - ts_0|` reaches 5,000 ns. Many groups then exceed 4,096 ns and are voided.
  - Under the page's rules the history never validates: valid 0.0000, with 122 restarts/s at 0 ppm and 130/s at 300 ppm. With the void rule off, the probe reproduces the model's kind of result: valid 0.9957 (`receipts/probe_meter_rules.out` section B).
  - The +/-1,426 ns rows are unaffected, because the in-group worst case is 3,414.5 ns (section C).
- **Impact:**
  - The page reports headroom that its own rules do not have. Independent error well under the 4,096 ns spacing bound, from about +/-2,050 ns, already voids groups.
  - The implementation lane and the bench would read the row as the meter's tolerance margin.
- **Required outcome:**
  - The model implements the void rule and the row is corrected.
  - Alternatively, the page states the effective independent-error ceiling the void rule imposes.
- **Verification:** the revised model output and table row.

### N3: MINOR (RTL, Tests, Docs). One switch-row mutant cannot fail its on-wire check, and the other fails for only about half the switch phases

- **Where:**
  - test row `:820`, with its mutants "No re-seed on a change of the followed listener: a second toggle on outputs" and "the disruption trigger unmasked at a switch: the era-start lock fall requests a second restart";
  - `:643-648` ("A second request from the new input's first PDU, or from a meter lock fall, would land after it on about half the outputs").
- **Authority and evidence:**
  - `KL_media_clock_restart.sv:236-246` merges a second request while an output's adopted level has not yet been reported on a PDU (`hold_r == 0`).
  - The era-start lock fall comes within a few cycles of the source-change request, inside every output's merge window. In the probe, a second request 1 to 4 cycles after the edge reached the wire in 8 of 916 trials, at a 100-cycle period; at the real clock the gap is a few cycles out of 12,500 (`receipts/probe_mcr.out`). So the "disruption trigger unmasked" mutant passes "exactly one toggle per output per switch" almost always.
  - The no-re-seed mutant's second request comes at the new input's first accepted PDU. It reaches the wire in 1,355 of 2,748 phase and arrival combinations.
  - The default `milan_dp` leg is the 1x1 shape, with one AAF output and a CRF output whose window is up to 2 ms (`tb/verilator/milan_dp/Makefile:51`, `:60`). So one switch can pass with the defect present.
  - AGENTS.md section 6 requires that each new test can fail for the defect it claims to detect.
- **Impact:** a lane that implements the row as written can show both "failing mutants" passing, or keep a mutant that never fails. The one-request rule, which the page argues is what keeps the wire clean, would then be ungraded. The statement at `:645-648` also attributes a post-window landing to "a meter lock fall", which at an era start lands inside the window.
- **Required outcome:**
  - The row grades the property where each mutant is visible: for example, exactly one restart request per switch at the restart module's inputs (`restart_p_i` pulses plus source-change edges), or a stimulus whose switch phase is pinned or swept so that each named mutant is shown failing.
  - `:643-648` says which second request lands after the window and which lands inside it.
- **Verification:** the revised row and text. In the implementation lane, both mutants are shown failing.

## Suggestions

These are optional and do not affect lens coverage.

- **S1 (Conformance, Docs), `:100-103`.** The permission for an entity-initiated change rests on 5.3.11.1's "is able to dynamically change". The same clause continues "the user is expected to correctly set the clock source", which reads as capability for a controller-driven change. The permission stands more firmly on the absence of any prohibition outside 5.4.2.15's locked scope. The design chooses no fallback, so there is no impact.
- **S2 (Docs), `:379-380`, `:852`.** State on the page that P2 replaces the ruled wording "keeps one AAF timestamp in 16", and whether that needs confirmation. The DECISION comment already says so.
- **S3 (Docs), `:643-645`.** "At most 125 us" holds for the AAF outputs; the CRF output's window is up to 2 ms. Say "per output".
- **S4 (Docs), `:755`.** The Generated row's text names "the tracked `hdl/common/gen` copy", but its Where cell omits `hdl/common/gen/adp_shape_defaults.svh`.

## Prior findings resolved or retained

| Finding | State at `c554ae51` | Evidence |
|---|---|---|
| R429-1 F1 (clauses stronger than the text) | Resolved | (a) "one source per AAF Stream Input is this design's choice" `:74-75`; (b) split into required, permitted and chosen `:83-127`; 7.6.2's consequence restated `:70`; holdover `:613-616` |
| R429-1 F2 (CRF jump bound) | Resolved as asked: assumption with basis `:466-485`; bound re-derived `:487-508`; at- and beyond-bound rows with mutants `:809-810`; B AAF records the restart count and deviation `:837`. The evidence offered for the lock test is new finding N1. | probe sections A and D |
| R429-1 F3 (sequence wrap) | Resolved: base format only, samples per PDU from `stream_data_length`, groups by modulo 16 `:410-445`; refusal rows `:811-812` | Milan v1.2 6.2 Table 6.1; 1722-2016 7.3.5 |
| R429-1 F4 (`mr` re-seed) | Design resolved `:540-546`, `:636-648`. Its test row is retained in part as N3: opposite levels are driven, but the mutant fails only phase-dependently. | `receipts/probe_mcr.out` |
| R429-1 F5 (test-plan gaps) | Resolved: W2 root `:819`; true-ratio offsets and mux-stuck mutant `:818`; decimation-by-1 `:808`; AECP stale-table mutant `:825`; `rate_valid` asserted `:802-804` | page |
| R429-1 S1 to S4 | Taken: `:3112` in (d)6 `:204-207`; `_load_names` `:230`, `:753`; offsets `:230`, `:878`; `tu` trap `:401`; read-window trap `:761`; 7.6 `:70`; C1 reversal `:678-708`; shapes without INTERNAL `:359-364` | page |
| R428-1 F1 (D1's saved-state basis) | Resolved: withdrawn and re-argued `:339-364`; the D6 consequence recorded `:352-357`, `:752`, `:881-882` | `milan_baremetal.c:634-636` |
| R428-1 F2 (meter input contract) | Resolved as for R429-1 F2 and F3. The desk-model limits are N1 and N2. | as above |
| R428-1 F3 (D5 reverses a recorded rule) | Resolved: `:678-708`; banner rewrite listed `:757` | `milan_datapath.sv:3469-3475` |
| R428-1 F4 (test gaps a to e) | Resolved: `:819`, `:823`, `:824`, `:808`, `:825` | page |
| R428-1 F5 ((b) as a choice; 10.6) | Resolved: `:104-132` | clause texts |
| R428-1 F6 (rulings currency) | Resolved: `:20-28`, `:847-857`; the links resolve | issue reads |
| R428-1 S1 to S4, O1 | Taken: (d)5 `:200-203`; dead-feed condition `:654-660`; citations `:251`, `:738`, `:753`, `:758`, `:181-186`; shapes `:359-364`; O1 as (d)8 `:213-218` | page |

## Executed evidence

Every command ran in the foreground. Receipts are listed in `MANIFEST.sha256`.

| Run | Result | Receipt |
|---|---|---|
| The author's `meter_rules_model.py` (sha256 `a264f267...9fcd`), re-run from the published packet | rc 0, byte-identical to the published `meter_rules_model.out` | `receipts/author_model_rerun.out` |
| `probe_meter_rules.py` (standard library only, deterministic seed): the page's rules with the void rule, correlated shapes, a closed loop and a step sweep | rc 0 | `probe_meter_rules.py`, `receipts/probe_meter_rules.out` |
| `KL_media_clock_restart` merge-window probe on the pinned simulator 5.050 (identity in `receipts/simulator_identity.txt`), `N_TALKERS_P=2`, built in scratch | rc 0; 229/229 single toggles; 8/916 and 1,355/2,748 second toggles | `probe_mcr/sim_mcr.cpp`, `receipts/probe_mcr.out` |
| `python3 scripts/check_entity_shape.py` at the head in this clone | rc 0, `RESULT: PASS` | `receipts/gates/check_entity_shape.*` |
| The same in detached worktrees at `49899572` and `c554ae51` (no submodules; differential on arm I only) | rc 1 both; the page's line is listed only at `49899572` | `receipts/gates/check_entity_shape_at_49899572.*`, `..._head_in_worktree.*` |
| Markdown gates in the pinned environment, and `git diff --check d4dd7426 c554ae51` | all rc 0 | `receipts/gates/*.out`, `*.rc` |
| Hosted checks at the head, read only (17:19 UTC) | success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`; in progress: `docs-check`; skipped, not executed: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the shards and the physical gPTP job | `receipts/hosted_checks_read.tsv` |
| Public-text scan of the added lines | 0 hits; positive control 1 hit | `public_text_scan.sh`, `receipts/public_text_scan.out` |
| Restore check after all probes | exact head; index tree equals the HEAD tree; 979 tracked blobs and modes match; 0 status and 0 ignored entries (16 bytecode files from this round's gate runs removed); gitlinks unchanged (external `efeb541a` uninitialised as found, gptp-processor `5dce647a`, protocol-processor `b2db3a97`, verilog-axis `48ff7a7e`); no extra worktree | `restore_check.sh`, `receipts/restore_check.out` |

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MEDIA_CLOCK_FOLLOWING.md:60-218`, `:410-438`, `:466-486`, `:674-708` against Milan v1.2 5.3.3.6, 5.3.11.1, 5.3.11.2, 5.4.2.15 and 6.2 (Table 6.1); IEEE 1722-2016 4.4.4.3, 4.4.4.5 to 4.4.4.7, 7.2.4, 7.3.5, 7.5, 10.6, 10.8 Equations (15) and (16), and PICS AAF-5/6; IEEE 1722.1-2021 Table 7-16; `aem_descriptors.py:133` | R429-2 | `c554ae51b1dcc2285863f0f0117cb025971a594c` |
| RTL | UNCLEAN (N3) | design `:389-650` against `KL_crf_rx.sv:275-403`, `KL_mmcm_drp_servo.sv:225-236`, `:505-700`, `KL_media_clock_restart.sv:200-265`, `milan_datapath.sv:1554-1570`, `:3466-3494` and `:5594-5615`, `avtp_stream_parser.sv:160-180`, `KL_avtp_rx_monitor_ctx.sv:460-492`; the restart-merge probe | R429-2 | `c554ae51b1dcc2285863f0f0117cb025971a594c` |
| Robustness | UNCLEAN (N1, N2) | meter pick, void, bound and history rules `:440-553`; lock loss and switch `:584-650`; `receipts/probe_meter_rules.out` sections A to D; `receipts/author_model_rerun.out` | R429-2 | `c554ae51b1dcc2285863f0f0117cb025971a594c` |
| Tests | UNCLEAN (N1, N2, N3) | simulation table `:797-826` and bench `:828-845`, each named mutant against the cited RTL; `author-r2/meter_rules_model.py`; `receipts/probe_mcr.out` | R429-2 | `c554ae51b1dcc2285863f0f0117cb025971a594c` |
| Docs | UNCLEAN (N1, N2, N3) | the whole page; `docs/README.md` index row; the gates (`receipts/gates/`, all rc 0 at the head); the `check_entity_shape` differential; PR body linkage; `receipts/public_text_scan.out` | R429-2 | `c554ae51b1dcc2285863f0f0117cb025971a594c` |

## Limits

- **Design review only.** No meter or decode RTL exists. The probes model the page's stated rules, and drive today's `KL_media_clock_restart` standing in for the switch path.
- **The closed-loop figure is a simplified model:** ideal plant, the servo's KI and KP, with no slew limit, guard or plant gain error. It indicates direction, not the servo's exact rate.
- **The restart-merge probe** uses a scaled PDU period (100 cycles) and a report latency of zero. Real-clock visibility of the immediate second request is lower than the 8 of 916 measured.
- **Clause texts** were read from local copies (same hashes as round 1) and are not republished.
- **No hardware.** No bench run or physical calibration was done, and field skips are not hardware proof.
- **Hosted state.** `docs-check` was in progress when read. The long suites were skipped by path scope, not executed.
- **Out of scope.** D4 (with the owner), #632 and protocol-processor #141 were not reviewed.

## Pending manager duties

- Publish this report and the manifest-listed receipts, and post the verdict.
- Hosted and local-replica acceptance at the head, including the in-progress `docs-check`.
- After N1 to N3 are answered:
  - a re-review at the new head;
  - the internal review's verdict;
  - the decisions on D1 and D5 (and D4 by the owner);
  - the candidate merge against live dev (base `d4dd7426`);
  - post-merge containment.

R429-2 FINISHED
