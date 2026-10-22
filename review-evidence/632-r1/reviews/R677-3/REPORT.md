[R677] NEGATIVE - exact head ee5ece607816a1bfc834bd51734b703a8aab8e46

# R677-3: internal cleared-context review of PR #770, round 3 (Relates to #632, #764)

Head `ee5ece607816a1bfc834bd51734b703a8aab8e46`, tree `5505182fe6e444e736f1f10b4388621342b820d5`, source base `e26f1816`.
The delta reviewed is the 31 commits on the round-2 head `2ff30f0d`: the author's rounds 3, 3b, 4 and 5.

## Summary

- **Verdict: NEGATIVE.** Three MINOR findings are open.
  - **R677-3-F1 (MINOR).** A PDU whose timestamp falls before the latest domain event loses every event, including events whose frames are still ahead. This contradicts the stage's own stated rule, the design page and the harness's own reference model. A one-phase probe shows it on both harness shapes, and no current test reaches it.
  - **R677-3-F2 (MINOR, Docs).** Four stale statements: the design page's out-of-context figures for the queue, its planted-defect count, the test-evidence reader's count, and its "two frames past the queue" wording.
  - **R677-3-F3 (MINOR, Tests, Docs).** The full `tdm8render-mutants` campaign, which the PR's validation steps list, is red at the head.
    - The `ungated commit` control is still detected by T19, T21, T23 and T25, but its named check, T26, no longer fails.
    - The new stage presents silence for a flushed stream, so T26 cannot fail for its defect any more.
- One RESIDUE (review-round labels in three new source comments) and four SUGGESTIONS.
- **Everything else asked about holds at this head:**
  - the 33-bit CRF carry, graded at full width, with its planted truncation killed (R678-2-F1);
  - the hold-restart check, with `hold_keeps_ref` killed (R677-2-F2);
  - the R677-2-F3 figures;
  - the render queue at the pins on two interfaces with different out-leads, with its four required controls killed;
  - the long-PDU fix and its two controls;
  - the per-shape supported range and the 7.4.77.1 statement;
  - AAF offsets as set and the CRF output alone rounded, with GET_STREAM_INFO split per output;
  - inferred block RAM only, with the area and route figures as stated;
  - the 63/64 sweep, its one failure attributable only to the processor pin.
- **Campaigns I ran at the head:**
  - `render_queue` 22 of 22;
  - `gmstep-mutants --all` 20 of 20 (22 checks, 0 failures);
  - `tdm8render-mutants` 30 of 31 (F3).

## Reconstruction (public state only)

Read, in order:

1. `AGENTS.md` and `CONTRIBUTING.md`.
2. `docs/README.md`.
3. Issue #632 (title and scope).
4. These rulings and decisions:
   - the round-3 assignment, issuecomment-6306591168;
   - the option (b) processor ruling, issuecomment-6312625146;
   - the round-4 assignment, issuecomment-6316458183;
   - the owner decisions on #632, issuecomment-6309219099 (render queue now, option (a)) and issuecomment-6309313685 (block RAM);
   - the owner decision on #770, issuecomment-6320453361 (sized for the 2 ms default);
   - the AAF-exact ruling, issuecomment-6320617745.
5. The live PR body (45,669 bytes at review time).
6. The diff `2ff30f0d..ee5ece60` (79 files, +6,268 / -4,971) and its 31 commits.
7. The published evidence at `7aa121b3` `review-evidence/632-r1/author-r5`, mainly `receipts/round3`, `round4` and `round5` with their `INDEX.md`.
8. The author's REVIEW READY comment, issuecomment-6338815326.

The prior R677-2 and R678-2 reports were read only after my own pass and the draft verdict were written (`receipts/own/independent_verdict_draft.md`, timestamped).

The frozen scope this round is judged against:

- **Round 3.**
  - R678-2-F1: the full carry, full-width grading and a planted truncation.
  - R677-2-F2: `det afterhold` and `hold_keeps_ref`.
  - R677-2-F3: the figures.
  - R677-2-F1: the four-step `[NOTIFY]` case and its control. The processor half is ruled option (b), merged as processor PR #199 and consumed by the fourth pin adoption, so the case fails at this PR's pin by design.
- **Round 4.**
  - A block-RAM render queue per Stream Input that presents every sample at its AVTP presentation time at the pins.
  - Per-interface out-leads against the one domain event.
  - The late and too-early rules with counters and clauses.
  - Stream start, gPTP step and hold behaviour.
  - Four planted controls.
  - The #386 law re-graded in five suites.
  - Area within 2 RAMB18 per 8-channel stream with no LUTRAM.
  - The route-1x1 re-record.
- **Round 5.**
  - AAF offsets as set; the CRF output alone keeps Equation (14).
  - GET_STREAM_INFO word 3 split per output.
  - The re-graded offset cases.
  - The 33-bit CRF carry kept.
  - The notify column kept.
- **Owner decision 6320453361.** The queue is sized for the 2 ms default, with the supported range stated exactly and the 7.4.77.1 limit documented.

## Findings

### R677-3-F1 - MINOR - Conformance, RTL, Robustness, Tests, Docs - a PDU timestamped before the latest domain event loses its on-time events

**Where:**

- `hdl/ieee1722/aaf/KL_render_queue.sv:410-411`: `d_late_w = d_w[31]`.
- `:755-758`: a negative d sets `P_LATE_S` for the whole PDU.
- `:448`: `place_w` is false for every beat of that PDU.
- `:396`: the comment "the whole PDU is late".
- Blob `b91c2a2f9db6`.

**Authority:**

- The round-4 assignment requires that each sample reach its interface's pins at its AVTP presentation time (IEEE 1722-2016 4.4.4.9, 7.5: event k is presented k periods after the PDU's timestamp).
- The stage's own contract states the late rule **per event**:
  - the banner, `KL_render_queue.sv:68-77`: "THE RULES, per event of a PDU ... late F <= R ... the event is dropped";
  - the design page's rule table, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1883-1889`: "an event's frame is at or before R ... the event is dropped; the PDU counts once";
  - the PR body, Round 4: "those events dropped";
  - `docs/design/TIME_SYNC.md:390`: "an event at or before the frame every interface has read | dropped".
- The harness's reference model applies that rule to the signed difference: `tb/verilator/render_queue/sim_main.cpp:322-347`, per event `f <= m_.r`.

**Evidence:**

- When `hdr_ts - E_n` is negative, the RTL refuses the whole PDU at its header, even where F0 + k > R for later events k.
- A disposable probe adds one phase to the unmodified harness (`scripts/F1_partial_late_probe.patch`, `scripts/F1_partial_late_probe.sh`) with three PDUs:
  - a PDU with frame offset -1;
  - a PDU at phase -0.3 Ps;
  - a control at +0.3 Ps, which has the same late frames and d >= 0.
- Results (`receipts/F1_partial_late/`):
  - Head harness, unmodified: 36 checks, 0 failures (two interfaces) and 35 checks, 0 failures (one interface, 7 lanes).
  - Probe: `[latepart] ... (366 reads, 32 mismatched beats)` and `(183 reads, 20 mismatched beats)`.
  - On the 7-lane shape, 20 beats are exactly the five on-time events of the two d < 0 PDUs (2 + 3 events, 4 beats each). They are expected by the model and presented as silence by the DUT.
  - The d >= 0 control places its on-time events correctly.
  - The `[late]` count check fails only because the harness hard-codes `m_.late == 2`. DUT and model agree on 5.

**Contradicting statements in the tree.** They disagree with each other as well as with the RTL:

- `docs/reference/REGISTER_MAP.md:2048` (`RENDER_STAT[31:16]`): "PDUs refused as late (every event at or before the frame every interface has read)". The RTL counts a PDU with *any* late event, as the `[late]` phase's first PDU (two of six events late) shows.
- `hdl/milan/milan_datapath.sv:6939-6940`: "A PDU whose events are all presented already is late".

**Impact:**

- A PDU whose first sample's presentation time is already behind the latest domain event loses its still-on-time samples as well as its late ones: on the 1x1 shape (K = 2), events 3 to 5 for d in (-Ps/2, 0) and events 4 and 5 for d = -Ps. They are presented as silence.
- On the 1x1 shape some events are still on time while d >= -2.5 Ps. This is reachable for a PDU that arrives between about 21 us (the event latency) and 94 us after its first sample's presentation time: a short offset set by a controller, or a late network path.
- In the probe the DUT also counted two slips fewer than the model, since the frames it left silent were never presenting.
- The stage's documented law, the reference model "byte-exact against a model of the law" and the RTL disagree in a reachable input region that no phase exercises. The model therefore cannot detect a regression in either direction there.

**Required outcome:**

- One late rule for a PDU timestamped before the latest event, stated once and implemented as stated.
  - Either place the later events per event, as the banner, design page and model say;
  - or rule that such a PDU is refused whole and say so in the banner, the design page's rule table, `TIME_SYNC.md`, the PR body and the model.
- Make `REGISTER_MAP.md:2048` and `milan_datapath.sv:6939-6940` say what the RTL counts.
- Add a `render_queue` phase with a partly late PDU timestamped before the latest event, on both shapes, and a planted defect that it kills: the other rule.

**Verification:**

- `make -C tb/verilator/render_queue` passes both shapes with the new phase.
- `mutants.py` catches the new control by its named check.
- The probe above, re-run, agrees with whichever rule is chosen.
- The six texts (banner, design page, `TIME_SYNC.md`, `REGISTER_MAP.md`, the datapath comment, the PR body) and the model say the same rule.

### R677-3-F2 - MINOR - Docs - stale figures and one wrong rule statement for the queue

**Where, evidence and fix:**

- **`docs/design/MEDIA_CLOCK_FOLLOWING.md:1939-1941` (blob `902f7af95b78`).**
  - The page reads "2 RAMB18, 594 LUT, 231 FF ... 6 RAMB36, 945 LUT, 395 FF". Those are the first form's figures (`round4/ooc/q1x1.rpt`, `q8x8.rpt`).
  - The cut stage measured 553 LUT / 228 FF and 890 LUT / 387 FF (`round4/ooc_bb9a9200/q1x1.rpt`, `q8x8.rpt`; HEAD `bb9a9200`).
  - `KL_render_queue.sv` is unchanged from `bb9a9200` to the head (`git diff --stat bb9a9200..ee5ece60 -- hdl/ieee1722/aaf/KL_render_queue.sv` is empty), and the PR body states 553/228 and 890/387.
  - Fix: 553 LUT, 228 FF; 890 LUT, 387 FF.
- **`docs/design/MEDIA_CLOCK_FOLLOWING.md:1950`.**
  - The page reads "18 planted defects". `tb/verilator/render_queue/mutants.py` plants 22, `docs/testing/TESTING.md:662` says twenty-two, and my run caught 22 of 22 (`receipts/own/rq_mutants.log`).
  - Fix: 22.
- **`scripts/measure_test_evidence_readers.py:208`.**
  - It reads "plants one of eighteen presentation-stage defects". Fix: twenty-two.
- **`docs/design/MEDIA_CLOCK_FOLLOWING.md:1895-1896`.**
  - It reads "once an event lies two frames past the queue the PDU's later events are refused with it".
  - The RTL refuses the later events once any event is past the queue, at F >= R + ROWS (`KL_render_queue.sv:459-464`, `far_in_w`), as the banner (`:81-84`) and PR body say.
  - Fix: "once an event lies past the queue".

**Impact:** a reader's area figures, campaign bar and long-PDU rule disagree with the evidence and the RTL. These are figures and a behaviour claim, so they are not RESIDUE.

**Verification:** the four places read as fixed, and the docs workflow's gates pass.

### R677-3-F3 - MINOR - Tests, Docs - the full tdm8render campaign is red at the head: T26 no longer discriminates its control

**Where:**

- `tb/verilator/milan_dp_render/tdm8_render_mutants.py:210-217`: the control "ungated commit: a closed epoch admits frames anyway", named check T26.
- `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3035-3056` (blob `c47465a6a3ff`): T26, "MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value never reaches a slot".
- The PR body's "How to validate": `make -C tb/verilator/milan_dp_render tdm8render-mutants`, expected "their campaigns catch every planted control".

**Evidence:**

- My full run at the head is `receipts/own/tdm8m.log`, rc 2:
  - "31 checks: 30 PASS, 1 FAIL";
  - "[FAIL] mutant 'ungated commit: a closed epoch admits frames anyway' failed, but not the named check ('T26 ...')".
- Re-planted alone through the driver's own `plant`, `build` and `run_leg` (`scripts/tdm8_one_mutant.py`, `receipts/own/ungated/head.log`):
  - the leg fails T21 (got 8, exp 0), T19 (got 8), T23 (got 1) and T25 (got 1);
  - T26 passes.
- The T26 scenario is byte-identical to round 2's (`2ff30f0d` lines 3059-3080 against head 3035-3056).
- What changed is upstream. `KL_render_queue` reads a flushed stream as silence and hands the crossbar zero lanes, so the "re-seeded crossbar value" a map write in the closed epoch could leak is zero whether or not the epoch gates commits. T26 therefore no longer tests what it states.
- The published evidence never shows this campaign run whole after the round-4 rewrite. Round 4 ran four mutants and three leg defects as a subset (`round4/milan_dp_render_632_bb9a9200/tdm8_subset.log`), and the sweep runs only `--leg-defects`. A run at `2ff30f0d` was not attempted here: its submodule copies lack git metadata, and creating it was declined.

**Impact:**

- A validation command the PR lists, with a stated pass criterion, fails at the head.
- A check named as the detector of a closed-epoch leak can no longer fail for that defect.
- The defect itself is still caught, by four other checks.

**Required outcome:**

- T26 again able to fail for a closed-epoch commit (for example, a non-zero value that reaches the crossbar while the epoch is closed). Or name the control's checks that do discriminate it and state why T26 is kept.
- A full `tdm8render-mutants` receipt at the corrected head.

**Verification:** `make -C tb/verilator/milan_dp_render tdm8render-mutants` exits 0, with every control caught by its named check.

### RESIDUE (wording only, carried to the residue checklist)

**R677-3-R1 - Docs - comment rule.** Three new source comments in the delta name review rounds (`receipts/own/comment_rule_scan.txt`; existing instances are tracked by #746):

- `tb/verilator/media_phase/phase_mutants.py:206`: "(round 2's binding, every row through the rounder)". Exact fix: "(the former binding, every row through the rounder)".
- `tb/verilator/media_phase/sim_ofs.cpp:35`: "(round 2's binding)". Exact fix: "(the former every-row binding)".
- `tb/verilator/milan_dp/gsi_mutants.py:125`: "round 4's binding:". Exact fix: "the former binding:".

The README's issue-comment link at `tb/verilator/milan_dp/README.md:999` is a reworded existing line in documentation, not a source comment, so it is not counted.

### SUGGESTIONS (optional)

- **S1. A declared buffer the queue does not back.**
  - The builder accepts `buffer_length_ns` above 2,126,000 (`sw/builder/endstation_builder.py:1423-1431`). The datapath binds `MAX_HOLD_NS_P (2_126_000)` as a literal (`milan_datapath.sv:6994`).
  - So a configuration could declare, under IEEE 1722.1-2021 7.4.77.1, a buffer the queue does not hold.
  - Both texts record it and no shipped shape declares more, so it is not a finding. A builder bound at the queue's backed hold would close it, or a shared constant feeding both.
- **S2. Stale CI image command table.**
  - `ci/image/command-table.json` still names `KL_render_setpoint.sv` and `VKL_render_setpoint_sim` in about thirty places, and has no `render_queue` entry.
  - No workflow runs it (`docs/testing/CI_IMAGE.md:4`: the #737 lane supplies the image without changing workflows), and its `--check` needs the image's own tools here (`receipts/own/ci_tool_inventory_check.log`).
  - Flag it to the #737 lane, or regenerate it at adoption.
- **S3. Hard-coded harness counts.**
  - `tb/verilator/render_queue/sim_main.cpp`'s `[late]` and `[early]` checks hard-code the model's counts (`m_.late == 2`, `m_.early == 4`).
  - A new refusal phase must edit them. Deriving the expected counts from the phases' own PDUs would keep the check self-consistent.
- **S4. Full-campaign receipts.** Publish full-campaign receipts with the merge-candidate evidence. The author ran `gmstep-mutants` as a two-control subset after the rewrite (`round4/gm_steps_bb9a9200/gmstep_subset.log`). My full run at the head catches 20 of 20, so this is only a receipt gap there.

## Prior findings at this head

| Finding | Status at `ee5ece60` | Evidence |
|---|---|---|
| R678-2-F1 (MAJOR) CRF carry | **Resolved** | `KL_mtt_round` `ofs_c_o` and `rb_ns_o` saturating at 0xFFFFFFFF (`KL_mtt_round.sv`); `KL_crf_tx.sv:404` adds `{transit_c_i, transit_ns_i}` into the DIVW_C-wide offset; `milan_datapath.sv:3454-3473`, `:6398-6401`. `sim_ofs.cpp:315-340` grades every CRF timestamp on 64 bits against an independent Equation (14) and the frame grid; the 32-bit cast and the 2^31 skip are gone from the CRF grade (the AAF phase grade alone skips rows from 2^31, documented at `:342-346`). My `ofs` run: 0 failures (`receipts/own/mp_ofs.log`). `crf_carry_dropped`, `mtt_carry_dropped`, `mtt_reset_carry_dropped` and `readback_saturation_dropped` are each killed at the head (`round5/media_phase_mutants_ee5ece60/chunk3a.log`). Banner, design page and PR body corrected |
| R677-2-F1 (MAJOR) SET_STREAM_INFO change gate | **Resolved as ruled**, merge-gated on the pin | Option (b) in processor PR #199 (`51f88c7e`). At the pin `2cbed0a9` the case fails CRF steps 3 and 4 by design (`round5/sweep_ee5ece60/shard0/milan_dp_tallies.txt`: 459 checks, 3 failures, those steps only). With E_SINFO spliced in: 459 checks, 0 failures, and `gsi_mutants.py` 11 of 11, including the gate control caught at CRF step 3 (`round5/notify_fix_d5b516f6/`, test sources identical to the head). The AAF steps pass at either pin, as stated |
| R677-2-F2 (MINOR) hold restart | **Resolved** | My `det` run: `[det afterhold]` 3 ok (theta -31,250; committed -32,768/256) (`receipts/own/mp_det.log`); `hold_keeps_ref` killed at `[det afterhold]` at the head (`round5/media_phase_mutants_ee5ece60/chunk1.log`) |
| R677-2-F3 (MINOR) figures | **Resolved** | The "469 LUTs and 20 slices" text left the body with the R678-1-F1 decision section; "twenty-seven" now reads "forty", matching the campaign's 40 of 40 at the head |
| R677-2-R1, R678-2-R1 reviewer IDs | **Resolved** | No `R67x` token in any listed file or in the delta's added source lines (`receipts/own/comment_rule_scan.txt`); new instance of the rule: R677-3-R1 |
| R677-2-R2 fold comment | **Resolved** | `milan_datapath.sv:3423-3426` rewritten for the as-set rows |
| R677-2-R3 to R5, R678-2-R2 listener scope prose | **Superseded** | Round 4 built the listener; the design page says R678-1-F1 is done by it (`MEDIA_CLOCK_FOLLOWING.md:1807-1808`) |
| R678-1-F1 listener at the pin | **Implemented**; one residual defect | R677-3-F1 |
| R678-1-F2 non-period offsets | **Revised by ruling 6320617745, implemented** | AAF rows as set (`milan_datapath.sv:1447`), CRF row rounded alone (`g_pres_crf`), GET_STREAM_INFO split (`:5256-5259`); `ofs` 93 checks pass; nxn exact-stamp plants caught (`round5/nxn_plants_d5b516f6/`) |
| R677-2-S1 monitor EARLY threshold | **Dissolved** | Row 0 is an AAF row, now applied as set |
| R677-2-S2 modulo-2^32 rows | **Superseded** | By the 33-bit carry |
| R677-2-S3, S4 | Retained, unchanged | `KL_mmcm_drp_servo.sv` untouched by the delta; the data-delay literal `.DATA_DELAY_P (1'b1)` still at `milan_datapath.sv:1028`, `:1073`, `:1108` |

## Per-lens results

[R677] UNCLEAN Conformance - `KL_render_queue.sv:410-411,:755-758` against `MEDIA_CLOCK_FOLLOWING.md:1883-1889`, the round-4 requirement and IEEE 1722-2016 4.4.4.9 / 7.5 - R677-3-F1: the on-time samples of a PDU timestamped before the latest event are not presented. Everything else applied is met:
- round 5's split, from `milan_datapath.sv:1447`, `:3454-3473`, `:5256-5259` against Milan v1.2 5.4.2.9 and 5.4.2.10.2, with the CRF output alone by 10.7 Equation (14) and the carry per 10.4.13.1;
- the supported range, recomputed from the depth formula: (2 + 0.5) Ps - 20,964 = 31,119 ns and (2 + 128 - 1.5) Ps - 20,964 = 2,656,119 ns at 1x1; 1.5 Ps - 5,308 = 25,942 ns and 127.5 Ps - 5,308 = 2,650,942 ns at 8x8;
- ROWS = 2^ceil(log2(ceil(3 x 2,146,964 / 62,500) + 2)) = 128;
- the 7.4.77.1 statement (`:1875-1881`);
- the notify column, and the gate's failure at the pin attributable to the pin alone.

[R677] UNCLEAN RTL - `KL_render_queue.sv` (blob `b91c2a2f9db6`), `KL_aaf_rx_depacketizer.sv`, `KL_mtt_round.sv`, `KL_crf_tx.sv`, `KL_media_if_latency_pkg.sv`, `milan_datapath.sv` at the head - R677-3-F1. Checked clean:
- the divider's bounds (the remainder region below Ps x 2^QW; `g_chk_div`) and its rounding at half up;
- the frame-number width check;
- the scrub against the window: the newest writable row is R - 1 mod ROWS, already scrubbed;
- the read schedule's single port, with no port contention on reads;
- the flush walker's re-arm;
- the bank parity rule;
- the depacketizer's serial read FSM: no header of the next PDU while a payload is in flight, so `f0_r` is never overwritten mid-walk;
- tv and timestamp byte lanes, tagged and untagged;
- the CRF 33-bit sum and the saturating readback;
- the shape without a CRF output.

[R677] UNCLEAN Robustness - `KL_render_queue.sv` late, early, untimed, long-PDU, flush, step and hold paths - R677-3-F1 (a partly late PDU timestamped before the latest event). The long-PDU fix is otherwise clean: `[long]` with 40 and 300 events, and both controls killed in my run.

[R677] UNCLEAN Tests - `tb/verilator/render_queue/sim_main.cpp:322-347` against the RTL; `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3035-3056` - R677-3-F1 (the reference model and the RTL diverge in a reachable region no phase drives) and R677-3-F3. The rest is clean:
- `media_phase` `render`, `ofs` and `det` reproduce at the head (13/0; 93 checks; every det case);
- `render_queue` 22 of 22;
- the media_phase campaign 40 of 40 at the head (author);
- every pattern of the tdm8render, gmstep, follow_ring and mclk campaigns still applies at the head;
- my full `gmstep-mutants --all` at the head: 20 of 20, 22 checks, 0 failures.

R677-3-F3 also leaves this lens unclean: `tdm8render-mutants` 30 of 31 at the head, its T26 control not killed by name.

[R677] UNCLEAN Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md` (blob `902f7af95b78`), `docs/reference/REGISTER_MAP.md` (blob `9236e311a913`), `scripts/measure_test_evidence_readers.py`, `milan_datapath.sv:6939-6940`, PR body - R677-3-F1 (the late rule stated three ways), R677-3-F2, and R677-3-F3 (the PR body's "their campaigns catch every planted control"). Clean:
- the 5.4.2.10.2 split;
- the CRF-only write-back text;
- the supported-range table;
- the 7.4.77.1 paragraph;
- TIME_SYNC.md's other new rows (out-leads, depth, supported range, offsets) and the compliance-matrix rows;
- `RENDER_STAT` bits [9:0] and the reset value 0x100.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R677-3-F1) | rulings 6306591168, 6312625146, 6316458183, 6320617745; owner decisions 6309219099, 6309313685, 6320453361; `KL_render_queue.sv`, `milan_datapath.sv` offset and GSI paths, `KL_mtt_round.sv`, `KL_crf_tx.sv`; `MEDIA_CLOCK_FOLLOWING.md:1653-1955` | R677-3 | `ee5ece607816a1bfc834bd51734b703a8aab8e46` |
| RTL | UNCLEAN (R677-3-F1) | `KL_render_queue.sv`, `KL_aaf_rx_depacketizer.sv`, `KL_media_if_latency_pkg.sv`, `KL_mtt_round.sv`, `KL_crf_tx.sv`, `KL_media_domain_event.sv`, `milan_datapath.sv` diff | R677-3 | `ee5ece60...` |
| Robustness | UNCLEAN (R677-3-F1) | the stage's rule paths; probe `receipts/F1_partial_late/` | R677-3 | `ee5ece60...` |
| Tests | UNCLEAN (R677-3-F1, R677-3-F3) | `render_queue` harness and campaign, `media_phase` `render`/`ofs`/`det`, the campaign tables and receipts; own runs under `receipts/own/` | R677-3 | `ee5ece60...` |
| Docs | UNCLEAN (R677-3-F1, R677-3-F2, R677-3-F3) | `MEDIA_CLOCK_FOLLOWING.md`, `REGISTER_MAP.md`, `TIME_SYNC.md` late row, `TESTING.md`, `TIME_SYNC.md`, `MILAN_COMPLIANCE_MATRIX.md`, `measure_test_evidence_readers.py`, PR body | R677-3 | `ee5ece60...` |

No lens is covered clean at this head. After the fixes:

- Conformance, RTL and Robustness need re-cover at a head carrying the F1 change.
- Tests needs re-cover at a head carrying F1's phase and F3's repair.
- Docs needs re-cover at a head carrying the F1, F2 and F3 text.

## Evidence used

**Evidence packet.** The evidence packet `7aa121b3` `review-evidence/632-r1` was verified (`receipts/own/evidence_manifest_check.txt`):

- 2,788 manifest entries, 0 mismatched, 0 missing, 0 unlisted, 69 path-redacted.
- The commit is not signed (`%G?` = N), so its integrity rests on the manifest alone.

**The author's receipts relied on.** Each carries a HEAD file where noted:

- **Full sweep at `ee5ece60`.** `round5/sweep_ee5ece60/shard{0..3}/summary.txt`: 14/15, 16/16, 17/17, 16/16 suites; 47,447 + 331,516 + 262,062 + 1,540,265 checks; in-suite failures 3, all in shard 0's `milan_dp` notify leg, CRF steps 3 and 4 (`milan_dp_tallies.txt:6162-6168`). Its pool then started no later `milan_dp` leg.
- **Every `milan_dp` leg at `d5b516f6`.** `round5/milan_dp_legs_d5b516f6/summary.txt`: eleven legs, 0 failures; `render_mutants` 4 of 4. `d5b516f6..ee5ece60` changes docs and `tb/verilator/milan_dp/README.md` only.
- **media_phase campaign at `ee5ece60`.** `round5/media_phase_mutants_ee5ece60/chunk*.log`: 40 distinct planted defects killed. Chunk 2 hit its time limit (`rc=124`) on `mr_hold_removed` and `holdover_hold_removed` (killed by signal, counted as FAIL there); chunk 2b re-ran both and caught each.
- **route-1x1 at `5b502a05`.** `round5/route_1x1_5b502a05/route-1x1-check.log`: LUT +309, FF +343, SLICE +68, RAMB18 +2, DSP -1, WNS 0.108, WHS 0.015, route complete; gate exit 1 on RAMB18 alone. `5b502a05..ee5ece60` changes no RTL, synthesis or submodule path.
- **Out-of-context synthesis at `bb9a9200`.** `round4/ooc_bb9a9200/q1x1.rpt`, `q8x8.rpt`: 2 RAMB18 / 0 LUTRAM / 553 LUT / 228 FF, and 6 RAMB36 / 0 LUTRAM / 890 LUT / 387 FF. `q1x1.rpt.ram` shows 100 % inferred block RAM and 0 distributed RAM. No device primitive appears in `KL_render_queue.sv`.
- **Yosys and lint.** `round4/yosys_queue_bb9a9200/yosys_rq2.log`: `KL_render_queue` PASS with a non-zero cell count. `round5/yosys_changed_tops_d5b516f6/yosys_tops.log`: `KL_mtt_round` 1,215 cells, `KL_crf_tx` 2,687, `milan_datapath` 1,770,334. `round5/lint_5b502a05/lint2.log`: 89 <= 89.

**My own runs at the head, with the pinned Verilator 5.050 (identity verified):**

- `media_phase` `render`: 13 checks, 0 failures; A max 833.5 ns over 3,208 samples, B max 874.2 ns over 2,112; 4,072 of 4,072 and 2,688 of 2,688 samples reach the pins.
- `media_phase` `ofs`: 0 failures.
- `media_phase` `det`: every case passes.
- `render_queue` `mutants.py`: 22 of 22 caught, with its clean shapes passing.
- The F1 probe.
- The campaign pattern and named-check probes.
- `gmstep-mutants --all`: 20 of 20, 22 checks, 0 failures, 13:18 to 14:27.
- `tdm8render-mutants`: 30 of 31, rc 2, 13:18 to 14:51 (R677-3-F3).
- The single-mutant replay of `ungated commit`.

## Real limits of this round

- **No hosted check runs exist at this head.** The GitHub checks API lists none for `ee5ece60`. No hosted or act result is claimed; the manager owns that acceptance.
- **No manager source bank runs at this head**, and none is inferred. Source-head execution evidence is the author's receipts plus my focused runs.
- **Not re-run by me:**
  - the full sweep;
  - the `milan_dp` legs;
  - the spliced-processor notify leg and `gsi_mutants`;
  - route, out-of-context synthesis and Yosys.

  For those I verified the receipts and their head ancestry.
- **Not run by me as full campaigns:** the follow_ring, mclk and RENDER_STAT CSR control campaigns. The author's latest runs are follow_ring 16 of 16 and render-csr-controls 3 of 3 at `bb9a9200`, and mclk 31 of 31 in round 4. Their patterns apply at the head, and their latest receipts predate only the round-5 offset change, which does not touch what they plant.
- **The F1 probe is disposable** and was never committed. The fix's form is the author's to choose.
- **Physical calibration NOT RUN.** The bench proof (#764 method) follows merge. Field skips are not hardware proof.

## Pending manager and owner duties

- Assign R677-3-F1, R677-3-F2 and R677-3-F3. If the owner rules the whole-PDU refusal for a PDU timestamped before the latest event, record the ruling. The texts and the model still have to agree with the RTL.
- Carry R677-3-R1 to the residue checklist.
- At the merge turn:
  - adopt the processor pin carrying PR #199 (`51f88c7e`), then confirm `milan_dp` (notify leg and every later leg) and `gsi-mutants` at the current-dev candidate;
  - re-record the resource gate's RAMB18 baseline (+2, owner-budgeted);
  - build and validate the candidate (source base `e26f1816`, live dev `d77a8afd`);
  - publish the hosted and act receipts.
- Re-review the corrected head on every lens.

## Receipts and scripts (each listed in MANIFEST.sha256)

- `receipts/F1_partial_late/{base,probe}.{run,odd}.{log,rc}`: the F1 probe and its unmodified baseline.
- `receipts/own/`:
  - `mp_render`, `mp_ofs`, `mp_det` logs and rcs;
  - `rq_mutants`;
  - `campaign_patterns`, `campaign_patterns_mclk`, `campaign_names`;
  - `comment_rule_scan.txt`;
  - `evidence_manifest_check.txt`;
  - `ci_tool_inventory_check`;
  - `independent_verdict_draft.md`;
  - `gmsm.{log,rc,start,end}` and `tdm8m.{log,rc,start,end}`;
  - `ungated/head.{log,rc}`;
  - `restore_check.txt`: the clone restored to the head's bytes, index, modes and gitlinks after the probes;
  - `HEAD.txt`, start and end stamps.
- Host paths in my run logs are redacted to `<host path>`, `<clone>`, `<packet>` and `<tools>`.
- `scripts/`:
  - `F1_partial_late_probe.{sh,patch}`;
  - `campaign_patterns.py`, `campaign_patterns_mclk.py`, `campaign_names.py`, `tdm8_one_mutant.py`;
  - `comment_rule_scan.sh`;
  - `verify_evidence_manifest.py`.

R677-3 FINISHED
