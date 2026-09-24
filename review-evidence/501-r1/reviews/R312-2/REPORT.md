[R312] NEGATIVE - exact head dd6a68e9063c3f7aa81536197254d187e9cb65ba

# R312-2: internal independent delta review of issue #501 / PR #557

- Reviewer: [R312], the internal reviewer, working from a cleared context.
- Round: R312-2, a delta review of round 2 by executor [A288].
- Head: `dd6a68e9063c3f7aa81536197254d187e9cb65ba`, tree `255f99668325a7fc4c50eae661add6079f284789`.
- Round-1 head: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`.
- Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Assignment: issue #501 comment 5823589125, items 1-5. It records the manager's capture-hold decision: option (b), no RTL change, with a measured obligation on processor #61 (comment 5823590638).

## Reconstruction

I read, in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. The issue #501 decision (5789750234) and frozen scope (5821769708).
3. The round-2 assignment (5823589125) and the author's REVIEW READY (5823924470).
4. The donor obligation on processor #61 (5823590638). Processor #61 and #83 are both OPEN.
5. `git diff b5ee412cd..dd6a68e9` across 6 files: 4 docs, `scripts/check_nvm_record_space.py` and `scripts/nvm_map_checks.py`.
6. The full `573f0052a..dd6a68e9` diff, 14 files.
7. The firmware capture path, `sw/firmware/milan_baremetal/milan_baremetal.c:937-1024`.

This round changes no RTL, firmware, donor source or gitlink.

I read the other reviewer's round-1 findings only after writing this verdict and ledger. They are resolved in the last section.

## Findings

### R312-2 F1: MAJOR. Lenses: Conformance, RTL, Robustness, Docs

**Title:** the new capture-hold text says no map copy happens today. The shipping firmware copies the full grown 8x8 record area at every capture.

**Where:**
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1600-1602` (section 18).
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1699-1700` (UNRESOLVED 6).
- The premise of the assignment item 3 decision (issue 501 comment 5823589125): "maps are not materialized yet (only BINDING is), so no map copy exists to overrun today".
- The same premise in the donor obligation (processor #61 comment 5823590638), whose measurement starts "when this issue's writer materializes the audio maps".

**What the page says at head:**
- "Today only BINDING is materialized; maps are not copied yet."
- "No materialized map copy can overrun the hold today."
- "Donor writer adoption through processor #61/#83 must measure the copy."

**What the code does:**
- `nvm_capture()` walks every record of the shape's generated table (`milan_baremetal.c:1003`, `nvm_rec_after()` at `:508-530` over `nvm_blocks`).
- It copies every record whose ownership bit is clear, byte by byte, under the grant hold (`:1005`, store at `:1012`).
- The copy extent is therefore set by the shape's record table, not by which records the producer materializes.
- `configs/endstation_ax7101_8x8.yaml:61` builds the bare-metal firmware.
- `KL_pp_shadow.sv:961` instantiates the backend unconditionally, with the default `T_HOLD_MS_P = 50` (`KL_nvm_backend.sv:145`).

**Executed evidence:** `scripts/capture_copy_probe.py`, receipt `receipts/capture_copy_probe.log`.
- The probe instruments the copy store in a scratch copy of the firmware and drives the committed host bench: a blank board, then one commit, with nothing materialized.
- At 8x8 the capture copied **12,634 bytes over 156 records, 4,672 of them in output-map ids 0x70-0x77**.
- The page's own model on the counted bytes gives 31.8816 ms nominal (1.57x) and **63.7632 ms doubled (0.78x)**.
- At 1x1 it copied 3,218 bytes over 53 records: 8.2532 / 16.5064 ms (6.06x / 3.03x).
- The model's figures in the new section 18 table are correct. The claim about what is copied today is not.

**Impact:**
- The 8x8 exposure that section 18 now describes exists at this head for every 8x8 build, whenever a BINDING (or any producer) write meets a capture. The page defers it to donor adoption and says it cannot happen today.
- The copy loop being timed is this repository's firmware, not the donor writer. A measurement obligation that starts only when the donor materializes maps is triggered by the wrong event.
- That obligation is also owned by a lane that does not own the copy.
- A recorded decision rests on a premise the implementation contradicts. AGENTS section 2 requires that conflict to be published for a decision, and section 8 forbids a hidden material assumption.
- Safety still holds: a lapsed hold voids the capture and it is retried.
- 1x1 is unaffected.

**Required outcome:**
- Section 18 and UNRESOLVED 6 state what the firmware copies today: every closed record of the shape, independent of materialization. So the 8x8 hold exposure is present at this head, not only after donor adoption.
- The manager re-records the capture-hold disposition on the corrected premise. Any of these would do:
  - keep (b) with a tracked public owner that covers the parent firmware's 8x8 copy;
  - change the hold;
  - another decided remedy.
- The measurement obligation's trigger and owner match the copy that exists today. The donor obligation comment is corrected or supplemented to match.
- No design is prescribed here.

**Verification:**
- Re-read section 18 (`:1589-1610`) and item 6 (`:1692-1707`) at the fixing head against `milan_baremetal.c:1003-1016`.
- Re-run `scripts/capture_copy_probe.py`.
- Check that the decision comment and the obligation cite the full-area copy. If `T_HOLD_MS_P` or the copy changes, re-run `tb/verilator/nvm_backend`, `tb/verilator/nvm_cosim` and the host bench.

### R312-2 S1: SUGGESTION. Lens: Docs

**Where:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1831`.

- This row is in the response table for the re-review at `53b2026e`. It still reads "about 22 ms and 44 ms at 8x8, a margin of 1.1 to 2.3" and points at "18, 20 (item 6)", which now carry 31.9/63.8 ms.
- The row is historical by its table, so this is optional.
- A note such as "superseded at #501, see section 18" would stop a cold reader from following the pointer to different numbers.

## Round-1 findings (mine) at this head

| Finding | Status | Evidence at `dd6a68e9` |
|---|---|---|
| F1 MAJOR: writer framing by cluster count, stale "BLOCKED on #501" | **Closed** | See below |
| F2 MAJOR: capture-hold margin not re-derived | **Figures closed; exposure part superseded by R312-2 F1 (open)** | See below |
| F3 MINOR: stale 8x8 figures | **Closed** | See below |
| S1 SUGGESTION: firmware table not graded | **Taken (documented instrument), verified** | See below |
| S2 SUGGESTION: vacuous cleared-first check | **Partly taken** | See below |
| S3 SUGGESTION: silent 1x1 digest skip; formula restated | **Not taken; stays optional** | See below |

**F1, closed:**
- `SAVED_STATE_MATERIALIZATION.md:940-946`: padding runs through the "derived capacity". Inputs keep the cluster count and outputs follow section 4.2.
- `:444`: the parameter row names "output entry capacities from section 4.2".
- `:1631-1649` and the stage-3 row at `:1661` drop "BLOCKED on #501". Stage 3 now requires donor adoption, #502 and silicon proof.
- `:1635-1638` derives 72 entries, 576 B payload and 584 B framed at 8x8, and `max(17, 2*8)` at 1x1. These match the 8x8 fixture and `receipts/shape_dump.log`.
- `git grep` finds no saved-state page sizing an output record by cluster count.

**F2, figures closed; exposure part superseded:**
- The table at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1580-1585` equals `receipts/hold_margin.log` and the counted-byte probe exactly: 12,634 / 156, 83,604 instructions, 25,268 DDR accesses, 1,594,080 cycles, 31.9 / 63.8 ms, 1.57x / 0.78x.
- The 1x1 raw area is corrected from the base page's stale 3,220 to the gate's 3,218 (`receipts/figures_check.log`, 266 + 72 + 144 + 2,736).
- UNRESOLVED 6 carries the figures, 1x1 unchanged and the obligation link.
- What is not closed is the claim that no copy can overrun the hold today; see R312-2 F1.

**F3, closed.** Each figure below was recomputed from the gate output in `receipts/record_space.log` and `receipts/figures_check.log`.

| Location | Figure at head |
|---|---|
| `SAVED_STATE_FASTCONNECT.md:188-190` | 3,264 / 12,680 B, 19% |
| `SAVED_STATE_FASTCONNECT.md:788-790` | `40,000 + 4,096 + 12,680` = 56,776 |
| `SAVED_STATE_FASTCONNECT.md:793-795` | `ceil(12,680/4,096)` = 4 BRAM36 |
| `SAVED_STATE_FASTCONNECT.md:1231-1232` (9.4 table) | 13 / 50 pages, 65 / 250 ms, 2.1 / 8.1 ms, 3.07 / 3.26 s |
| `SAVED_STATE_FASTCONNECT.md:1235-1236` | 3,067.08896 / 3,258.1152 ms, 92% erase |
| `SAVED_STATE_FASTCONNECT.md:1239` | 2.46x / 2.61x |
| `SAVED_STATE_FASTCONNECT.md:1313-1314` | "every registered negative control" |
| `SAVED_STATE_MATERIALIZATION.md:1799-1803` | 3.07 / 3.26 s; 4.6 / 4.8 s, which is 500 + 1,000 + commit |
| `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1417` | 3.07 / 3.26 s |
| `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1456-1457` | 12,680, citing 4.2 |
| `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1553-1555` | 12,680, citing 4.2 |
| `BAREMETAL_FIRMWARE.md:1375` | names `MILAN_NVM_MAP{IN,OUT}_ENTRIES_k` |

- `git grep` for `8,648|8648|3.18 s|2.52x|52,744|3.06 s|2,624|8,604|1.1 to 2.3` leaves only two rows: `FASTCONNECT.md:453`, an explicitly PRE-#389 historical table, and `SNAPSHOT_OWNERSHIP.md:1831` (R312-2 S1).

**S1, taken and verified:**
- `SAVED_STATE_FASTCONNECT.md:364-366` names `tb/verilator/nvm_cosim` as the instrument.
- My probe `scripts/cosim_table_plant.sh` (`receipts/cosim_table_plant.log`) ran the 8x8 cosim builds. At the head: 150/150 PASS, rc 0.
- With only the firmware table write planted with the old 9-entry output length: RESULT FAIL, 2 FAIL (`W4_all_records_rewritten_after_refused_fill`), rc 1.
- The host bench still gives 0 findings for the same plant (`receipts/firmware_map_probe.log`), as the page now says.

**S2, partly taken:** the unreachable guard is removed (`nvm_map_checks.py:86-88`). The cleared-first store is still cleared by the probe's own statement; seeding it with a stale set remains optional.

**S3, not taken; stays optional:** `check_1x1_digest` still returns silently on an absent stem.

## Delta items 1-5, checked

**Item 1 (framing, parameter row, stale status):** met. See F1 above.

**Item 2 (figures):** met. See F3 above.

**Item 3 (hold):**
- Figures met.
- 1x1 is recorded unchanged.
- The obligation is linked from UNRESOLVED 6 and from MATERIALIZATION `:1647-1649`.
- The exposure statement is incorrect: R312-2 F1.

**Item 4 (self-test):**
- `check_nvm_record_space.py:292-314` registers a required substring per control.
- `:779-796` requires rc 1, a `FINDING:` line containing it, and no traceback on stdout or stderr.
- At head, `--self-test` rc 0: 18/18 controls print their named finding (`receipts/record_space_selftest.log`).
- My crash probe (`scripts/selftest_crash_probe.sh`, `receipts/selftest_crash_probe.log`) makes `--self-test` fail (rc 1) in all four head arms, each naming the failed control:
  - a control that raises before any finding (`traceback=True`);
  - a control that prints its named finding and then a traceback at exit;
  - a control that yields a real but unrelated finding;
  - a control that does nothing (exit 0).
- The same raise-before-finding plant in the round-1 file passes `--self-test` (rc 0, "(no FINDING line)"). So the probe detects exactly the change.
- The direct `--mutate=collide` run of the plant gives rc 1 with a traceback.
- `SAVED_STATE_FASTCONNECT.md:512-514` describes the rule accurately.

**Item 5 (the other reviewer's S1 and S2):** taken; see S1 and S2 above.

## Per-lens results

```text
[R312] PASS Tests — scripts/check_nvm_record_space.py:292-314,779-796, receipts/record_space_selftest.log, receipts/selftest_crash_probe.log — 18/18 controls rc 1 with their registered named FINDING; --self-test fails on crash-before-finding, finding-then-traceback, unrelated finding and vacuous control, each naming the control; the round-1 rule accepted the crash plant (rc 0), so the new rule is what kills it
[R312] PASS Tests — tb/verilator/nvm_cosim (8x8, suite's own cases), receipts/cosim_table_plant.log, receipts/firmware_map_probe.log — the page's new claim that nvm_cosim, not the host bench, kills a wrong firmware output-length table holds: head 150/150 PASS; table-only 9-entry plant 2 FAIL; host bench 0 findings for the same plant
[R312] PASS Tests — receipts/record_space.log, receipts/nvm_backend.log, receipts/firmware_hosttest.log, receipts/backend_mutants.log, receipts/d3_replay_head_summary.log, receipts/d3_replay_fw_rebase_old_len.log — round-1 probes re-run unchanged at head: gate rc 0 over 5 shapes; nvm_backend 525/0 (8x8) and 208/0 (1x1), 4 controls RED; host bench --self-test rc 0 with 4 controls; the three RTL mutants and the firmware plants reproduce round-1 outcomes byte for byte; D3 replay K16 17/17, boundary_audio 23/23, boundary_storage 72 keys 23/23; D3 firmware-table mutant fails (no 0x70 record reaches the journal)
[R312] PASS Conformance (partial; R312-2 F1 keeps Conformance unclean) — receipts/emit_head.log, receipts/emit_base.log, receipts/figures_check.log — every non-8x8 shape byte-identical base->head, 1x1 SHA-256 103ce107…3aea; 8x8 only ids 0x70..0x77 grow 72 -> 576 B; area 12634, image 12680, commit 3258.1152 ms, 2x < 8000 ms; the fixture equals the head emit; all identical to round 1
[R312] PASS Docs (partial; R312-2 F1 keeps Docs unclean) — SAVED_STATE_MATERIALIZATION.md:444,940-946,1631-1661,1799-1803; SAVED_STATE_FASTCONNECT.md:188-190,364-366,512-514,788-795,1231-1239,1313; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1417,1456,1553-1585,1692-1707; BAREMETAL_FIRMWARE.md:1375 — every figure recomputed against the gate and the model; anchors #42-… and #20-unresolved resolve to existing headings; docs_check, check_doc_style, check_doc_paths, gen_module_matrix --check, check_py_idiom, check_cpp_idiom, check_rtl_source_lists and git diff --check all rc 0
```

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R312-2 F1) | assignment items 1-5 and the item-3 premise; MATERIALIZATION framing and parameter row; section 4.2; base/head emits (5 shapes); 8x8 fixture; donor obligation comment; firmware capture walk | R312-2 | dd6a68e9063c3f7aa81536197254d187e9cb65ba |
| RTL | UNCLEAN (R312-2 F1) | `KL_nvm_backend.sv:145,297` hold parameter and refusal; `KL_pp_shadow.sv:961` default instance; firmware `nvm_capture()` copy extent under the hold; section 18 model; no HDL in the delta; round-1 RTL results otherwise stand | R312-2 | dd6a68e9063c3f7aa81536197254d187e9cb65ba |
| Robustness | UNCLEAN (R312-2 F1) | hold-lapse void and retry path at 8x8 today; over-capacity refusal (gate, nvm_backend); self-test crash and vacuous-control paths | R312-2 | dd6a68e9063c3f7aa81536197254d187e9cb65ba |
| Tests | CLEAN (suggestions only) | record-space gate and `--self-test` with 4 crash-probe arms; `nvm_map_checks.py` guard removal; nvm_backend with 3 RTL mutants; host bench `--self-test` and firmware plants; nvm_cosim 8x8 control and table plant; D3 replay and its firmware mutant | R312-2 | dd6a68e9063c3f7aa81536197254d187e9cb65ba |
| Docs | UNCLEAN (R312-2 F1) | FASTCONNECT 4.2/4.3/4.4/8.1/9.4/G0b; MATERIALIZATION 5/10/12/13/15/18; SNAPSHOT_OWNERSHIP 16/17/18/20; BAREMETAL_FIRMWARE:1375 | R312-2 | dd6a68e9063c3f7aa81536197254d187e9cb65ba |

## The other reviewer's round-1 findings at this head

I read these only after the verdict and ledger above were written. They are R313-1, PR comment 5823585783.

| Finding | Status at `dd6a68e9` |
|---|---|
| R313-1-F1 MAJOR (Conformance, Docs): framing rule and parameter row by cluster count | **Closed.** Same defect as my round-1 F1; evidence above. |
| R313-1-F2 MINOR (Conformance, Docs): stale 8x8 figures, including `BAREMETAL_FIRMWARE.md:1375` | **Closed.** Same set as my round-1 F3, plus the firmware constant wording, now at `:1375`. |
| R313-1-F3 MINOR (RTL, Robustness, Docs): hold budget not re-derived | **Figures closed; disposition retained as open** under R312-2 F1 (see below). |
| R313-1-F4 MINOR (Tests, Docs): `--self-test` accepted a crashing control | **Closed.** Evidence is under item 4: my own crash probe, four arms, each makes `--self-test` fail. |
| R313-1-S1 (Tests): name `nvm_cosim` for the firmware table | **Taken and verified**; see S1 above. |
| R313-1-S2 (Tests): unreachable guard | **Taken**; the guard is removed. |

On R313-1-F3:
- The re-derived figures match.
- That finding's own evidence already says `nvm_capture()` copies the whole record area under the hold.
- The disposition published at this head says instead that no map copy happens today. That is the open part, recorded here as R312-2 F1 under RTL, Robustness, Docs and Conformance.

## Real limits

**Renderer gates not run locally:**
- `scripts/gen_toc.py --check` and `scripts/check_em_dash.py` returned rc 2 because the pinned Markdown renderer (html5lib) is not installed. Shared installs are forbidden.
- The author's evidence reports both green.
- The hosted `docs-check` was still in progress when I sampled (`receipts/hosted_check_runs.tsv`).

**Hosted runs at the exact head, when sampled:**
- 14 completed `success`, including `rtl-fast`, `yosys-elaboration`, the Yosys shards 0-3, and Verilator shards 2 and 3.
- 5 were in progress: `docs-check`, `elaborate`, and Verilator shards 0, 1 and 4.
- 1 was skipped: `Physical gPTP (nightly and manual)`. It is not evidence.
- Hosted and act acceptance belong to the manager.

**Not run, per the round's rules:**
- the full parent, processor, gPTP, Yosys and builder banks;
- the full `nvm_cosim` sweep with mutants (only its 8x8 builds without the mutant sweep ran, twice);
- act or Docker;
- hardware.

**Physical calibration:** NOT RUN. No hardware persistence or hold timing was measured.

**R312-2 F1 evidence:**
- It counts bytes the firmware copies in the host bench, then applies the design page's cost model.
- It is not a timing measurement on the product CPU.
- The finding concerns what is copied, which the probe measures directly. It does not claim what the hardware time is.

**D3 replay:** it remains an uncommitted, scratch-adapted replay of immutable #500 sources (driver sha256 `d937a166…19bf1`, unchanged). The 72-key case substitutes an audio format for the CRF row, as disclosed in round 1.

**Where probes ran:**
- In scratch.
- As transient in-clone plants that were each restored from HEAD: the record-space gate file for the crash probe, and the firmware table line for the cosim and D3 plants.
- `receipts/restore_verification.log` records the checks after all probes:
  - the index equals the HEAD tree (mode, blob, path);
  - all 883 tracked non-gitlink files re-hash to their index blobs with no mode drift;
  - the four gitlinks are unchanged (`external` is uninitialized, as it was at start);
  - there are no untracked files, and every ignored build and cache directory created by this round was removed.

**Everything else:** my round-1 ledger stands, as assigned.

## Pending manager duties

- A decision on R312-2 F1: the corrected premise, and the owner and trigger of the hold measurement. Also a matching correction to processor #61 comment 5823590638.
- Then a fix round and a delta re-review at the fixing head.
- Hosted and act acceptance at the exact head, including the five runs still in progress.
- The candidate merge build at live `dev` `ffcbd33de70278ae34b533dcbadde0b36c8cba13` (source base `573f0052a`).
- Post-merge containment.
- Publication of this packet.
- Optional: R312-2 S1, and my round-1 S2 and S3.

R312-2 FINISHED
