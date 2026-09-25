[R313] NEGATIVE - exact head dd6a68e9063c3f7aa81536197254d187e9cb65ba

# R313-2: external independent delta review of issue #501 / PR #557

- Head: `dd6a68e9063c3f7aa81536197254d187e9cb65ba`, tree `255f99668325a7fc4c50eae661add6079f284789`.
- Round-1 head: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`. Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Delta: one commit, 6 files, +158/-102. It touches four saved-state and firmware pages, `scripts/check_nvm_record_space.py` and `scripts/nvm_map_checks.py`. No RTL, firmware C, donor source or pin changed.
- Role: external independent reviewer, cleared context, isolated detached clone. The review started publicly at PR #557 comment 5823943300.
- Authorities read:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the issue #501 body, the 2026-09-23 decision (5789750234) and scope items 1-6 (5821769708);
  - the round-2 assignment and capture-hold decision (issue #501 comment 5823589125);
  - the donor obligation (processor #61 comment 5823590638);
  - the executor's REVIEW READY (5823924470) and the PR body at this head;
  - the delta and full diffs, and the public evidence tree `d38b98fe.../review-evidence/501-r1` (author, author-r2, and the D3 driver).
- Verdict: **NEGATIVE**. All four round-1 findings are closed, and both suggestions were taken. One new MINOR finding is open under Conformance, RTL, Robustness and Docs. It is in the text written to close round-1 F3: the premise the capture-hold decision rests on is contradicted by the shipping firmware, the backend RTL and the page's own writer sequence. Tests is covered clean at this head.
- Amendment, disclosed: the Conformance attribution of F1 was added after the verdict and ledger were first written and the other reviewer's report was then read. The reason is given under "Prior public review findings". The verdict word did not change.

## Findings

### R313-2-F1: MINOR. Lenses: Conformance, RTL, Robustness, Docs

- **Where:**
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1600-1601` (section 18, Timing): "Today only BINDING is materialized; maps are not copied yet. No materialized map copy can overrun the hold today."
  - `:1699` (UNRESOLVED 6): "Only BINDING is materialized today; maps are not copied yet."
  - The decision premise is in issue #501 comment 5823589125, item 3: "because maps are not materialized yet (only BINDING is), so no map copy exists to overrun today". The donor obligation (processor #61 comment 5823590638) is triggered "When this issue's writer materializes the audio maps".
- **Title:** every capture already copies the grown 8x8 output-map records under the hold, so the exposure exists at this head, not only after donor adoption.
- **Authority and evidence:**
  - **The page's own writer sequence.** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1054` (section 7, step 3.4) says "Copy every CLOSED record from the live window into the stage". `:253` says the writer "copies only records whose open bit is clear".
  - **The RTL.** `hdl/milan/KL_nvm_backend.sv:1122-1133`: an accepted RELOAD "makes every record a completed one", so every allocated record's open bit clears after the boot load. A record the producer never writes, such as every map record today, stays closed and is therefore copied.
  - **The firmware.** `sw/firmware/milan_baremetal/milan_baremetal.c:1003-1017` (`nvm_capture`) walks every record of the shape (`nvm_rec_after`, `:508-531`) and copies each closed one, at its generated length, between ARM and ATTEST.
  - **Executed** (`scripts/capture_copy_probe.py`). The probe instruments the copy loop in memory, builds it on the tree's own firmware host bench, and runs one commit per shape.
    - At this head, one 8x8 capture copies **12,634 bytes over 156 records, of which 4,672 bytes are the eight 584-byte MAPS_OUT records** (`receipts/capture_copy_probe.log`).
    - At the base, the same probe copies 8,602 bytes, 640 of them MAPS_OUT (`receipts/capture_copy_probe_base.log`).
    - 1x1 copies 3,218 bytes at both.
    - So this PR adds 4,032 copied bytes to every 8x8 capture, and it does so today.
  - The page's own model, which the section 18 table applies correctly to that same 12,634-byte area, gives 31.9 ms nominal and 63.8 ms at doubled costs (`receipts/hold_margin.log`). Those figures describe the copy the shipping firmware performs at this head. Captures at this head are driven by BINDING changes.
  - AGENTS section 2: when the Issue or decision, the documentation and the implementation conflict, publish the conflict for a decision rather than choosing an interpretation.
- **Impact:**
  - Authoritative pages state as fact that no map bytes are copied under the hold today, and that no copy can overrun it today. The implementation copies them on every capture.
  - The recorded decision to keep the 50 ms hold, and to defer the measurement to a future donor event, rests on that statement.
  - From merge, the reduced margin (0.78x under the page's pessimistic model) applies to every 8x8 capture. A BINDING write during the copy is deferred past the lapse and voids the capture.
  - The page itself names the consequence of sustained activity: repeated void and retry, a liveness risk. That consequence is present at this head.
  - The only measurement obligation is attached to a later trigger, so no owner is named for the exposure that exists now.
  - Safety is kept: a lapsed hold voids the capture, which is released and retried. Nothing reaches flash unattested. That is why this is MINOR, as round-1 F3 was.
- **Required outcome:**
  - The decision owner confirms or revises the capture-hold decision on the corrected premise.
  - Section 18 and UNRESOLVED 6 then state what the implementation does: each 8x8 capture copies the full 12,634-byte record area, output-map records included, whether or not a writer materializes them. The modelled margins therefore apply from this head.
  - The measurement obligation, and its trigger, cover the exposure that exists now. How that is met (measurement, a hold change, or a copy that skips unmaterialized records) is the decision owner's and executor's choice.
- **Verification:**
  - A reviewer re-reads section 18, UNRESOLVED 6 and the donor obligation against `scripts/capture_copy_probe.py` output at the corrected head.
  - No sentence may claim that a record the firmware copies is not copied. If the copy scope itself changes, the probe's copied-byte count must match the page.

No other finding. No suggestion is raised this round.

## Round-1 findings: closure at this head

- **R313-1-F1 (MAJOR): CLOSED.**
  - `SAVED_STATE_MATERIALIZATION.md:940-946`: the framing rule pads "through its derived capacity"; input capacity remains the cluster count; output capacity follows section 4.2.
  - `:444`: the parameter row lists "per-port input cluster counts and output entry capacities from section 4.2".
  - The stale "Not before #501" text is replaced at `:1645-1649`, and the stage-3 row's "BLOCKED on #501" at `:1661`.
  - A search of the saved-state and firmware pages finds no sentence sizing an output record by cluster count.
- **R313-1-F2 (MINOR): CLOSED.** Every listed figure now carries the head value or cites section 4.2, and each was re-derived from the shape:
  - `SAVED_STATE_FASTCONNECT.md:188-190`: 3,264 B and 12,680 B, 19 percent (12,680/65,536 = 19.3 percent).
  - `:788-790`: `40,000 + 4,096 + 12,680 = 56,776`.
  - `:792-795`: `ceil(12,680/4,096) = 4` BRAM36.
  - `:1231-1232`: the section 9.4 rows. 1x1: 13 pages, 65 ms, 2.1 ms, 3.07 s. 8x8: 50 pages, 250 ms, 8.1 ms, 3.26 s. These are 3,067.08896 ms and 3,258.1152 ms, matching `receipts/compare_figures.log`.
  - `:1239-1240`: 2.46x and 2.61x (8,000/3,258.1 and 8,000/3,067.1). The erase share is 92 percent.
  - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1417` and `:1456-1457`: 3.07/3.26 s and a 12,680-byte stage. `:1553-1555`: 12,680 at 8x8.
  - `SAVED_STATE_MATERIALIZATION.md:1799-1803`: 3.07/3.26 s; durable 4.6/4.8 s (0.5 + 1.0 + commit bound).
  - `BAREMETAL_FIRMWARE.md:1375`: `MILAN_NVM_MAP{IN,OUT}_ENTRIES_k`, which are the generated names (`receipts/figures_head.json`).
  - The remaining 3.18 s and 22-44 ms figures are in tables that say they are historical: the PRE-#389 table at `SAVED_STATE_FASTCONNECT.md:440-453` and the re-review history at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1831`. The assignment keeps those.
- **R313-1-F3 (MINOR): CLOSED for the figures; the exposure statement is carried forward as R313-2-F1.**
  - The section 18 table at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1583` and UNRESOLVED 6 at `:1692-1698` match my unchanged `hold_margin.py` exactly: 21,958/83,604 instructions, 6,436/25,268 DDR, 412,660/1,594,080 cycles, 8.3/31.9 ms, 16.5/63.8 ms, and 6.06x/3.03x and 1.57x/0.78x.
  - 1x1 is unchanged (3,218 B, 53 records at base and head).
  - The page and the parameter agree: `T_HOLD_MS_P` is 50 and unchanged, per the recorded decision.
  - What does not hold is the sentence scoping the exposure to a future donor event (R313-2-F1).
- **R313-1-F4 (MINOR): CLOSED.**
  - `check_nvm_record_space.py:293-313` registers a required finding per control. `:779-796` requires rc 1, a `FINDING:` line containing it, and no traceback.
  - My unchanged crash probe now gives "--self-test with a crashing control: rc=1 ... RESULT: crash refused" (`receipts/selftest_crash_probe.log`).
  - A wider probe matrix (`scripts/selftest_probe_matrix.py`, `receipts/selftest_probe_matrix.log`) makes `--self-test` fail with its named line for each of six defective controls: a crash before the finding, a traceback after the correct finding, an unrelated finding, a silent `SystemExit(1)`, a no-op, and the required text printed outside a `FINDING:` line. The unmodified control passes.
  - All 18 controls print their named finding (`receipts/gate_selftest.log`), and the page's sentence at `SAVED_STATE_FASTCONNECT.md:512-514` now states what the loop enforces.
- **R313-1-S1: TAKEN.** `SAVED_STATE_FASTCONNECT.md:364-366` names `tb/verilator/nvm_cosim` and says the host test alone does not detect the defect. That is exactly what my unchanged mutant shows: `fw_out_table_uses_in_entries` passes the host test and is killed by `nvm_cosim` (`receipts/source_mutants.log`).
- **R313-1-S2: TAKEN.** The unreachable guard is removed from `scripts/nvm_map_checks.py:86-87`. The load-bearing `live.clear()` stays, and mutant `restore_nothing` is still caught.

## What was checked, per lens (this round)

### Conformance: UNCLEAN (R313-2-F1, attribution amended as disclosed above)

- The frozen scope items 1-6 and the round-2 assignment items 1, 2, 4 and 5 are met at this head, as the closures above show.
- Assignment item 3 requires "State the 8x8 exposure". The head states that exposure as future-only, which the implementation contradicts (R313-2-F1). So that criterion is not accurately met.
- `receipts/compare_figures.log`: 0 failures. This is my unchanged probe re-run at this head. The figures are derived from the shape, not copied from the PR:
  - 72 entries, 576 B and 584 B framed on every dynamic output port;
  - a decoded journal of 576 B per port, and the firmware constant 72;
  - growth of 4,032 B, and 156 records with top id 0xE2;
  - a worst commit of 3,258.1152 ms;
  - the backend decode rule hits every record offset;
  - the fixture matches.
- The head figures JSON is byte-identical to round 1's, except for the tree path, which confirms the delta changed no derivation. The 1x1 image SHA-256 is `103ce107...a3aea` at both base and head.
- The D3 replay was re-run unchanged from the public driver (`d38b98fe:review-evidence/501-r1/author/replay_d3.py`, sha256 `d937a166...19bf1`): K16 17/17 with 10 keys, `boundary_audio` 23/23 with 64 keys, `boundary_storage` 23/23 with 72 keys. Every port is empty before the restore boot and matches the decoded journal after it (`receipts/d3_replay.log`, `receipts/d3_replay_results.json`).
- As first written, this section said item 3 was "satisfied as written". It is corrected above.

### RTL: UNCLEAN (R313-2-F1)

- `hdl/` and every gitlink are unchanged from round 1 and from the base.
- `KL_nvm_backend.sv:1117-1138`: the open-vector semantics behind F1.
- `milan_baremetal.c:937-1027`, `:508-531`: the capture copy scope.
- `make -C tb/verilator/nvm_backend` with pinned Verilator 5.050 (`-j 8`): 525/525 at 8x8, 208/208 at 1x1, and all four existing controls RED (`receipts/nvm_backend_head.log`).
- RTL mutants re-run unchanged (`receipts/backend_mutants.log`): `one_over`, `nine_bit` and `stale_prefix` are all killed, the first by "output WRITE beyond capacity accepted".
- `tb/verilator/nvm_cosim` at 8x8: 150/150 (`receipts/nvm_cosim_8x8.log`).

### Robustness: UNCLEAN (R313-2-F1)

- The hold-lapse path: a lapsed grant voids the capture, which is released and retried (C2, C2e, C2r). It is still the safety argument, and it holds. What F1 disputes is the liveness scope.
- Over-capacity refusal is re-graded by the unchanged mutants: `gate_accept_oversize` is caught with its named message. The one-byte-over RTL checks are shown non-vacuous by `one_over`.
- Static ports keep their cluster allocation, as in round 1.

### Tests: CLEAN

- The gate returns rc 0 (`receipts/gate_default.log`). `--self-test` returns rc 0, with 18/18 named findings (`receipts/gate_selftest.log`).
- `--mutate old_output_length` returns rc 1 with "output-record capacity". `--mutate changed_1x1_image` returns rc 1 with "1x1 image digest changed" (`receipts/ctl_*.log`).
- The crash probe and the six-arm matrix are described under R313-1-F4.
- The source mutants were re-run unchanged. Their verdicts are identical to round 1's (`receipts/source_mutants.log`): `shape_one_short`, `restore_drops_last`, `restore_nothing` and `gate_accept_oversize` are caught, `fw_out_plen_old_nine` is caught by the host test, and `fw_out_table_uses_in_entries` is caught by `nvm_cosim` only, as the page now says.
- The firmware host test `--self-test` returns rc 0: five shapes, 8x8 image 12,680 B, four controls (`receipts/fw_hosttest_selftest.log`).
- The builder fixture test `test_baremetal_profile_contract` passes (`receipts/builder_profile_contract.log`).
- `gate_verbose` is rc 2 at both rounds, because `--verbose` is not a gate option. It is kept only because the probe list is unchanged.

### Docs: UNCLEAN (R313-2-F1)

- The four changed pages were read in full around every hunk. The figures, the section 4.2 anchors and `#20-unresolved` resolve, and section 18 is the section holding the Timing text.
- Local gates:
  - `docs_check.py` (0 findings, scrub 23/23, routing 4/4), `check_doc_style.py`, `check_doc_paths.py` (843 paths), `gen_module_matrix.py --check`, `check_py_idiom.py` and `check_cpp_idiom.py`: all rc 0.
  - The delta and the full diff add no U+2014, and `git diff --check` is clean (`receipts/diff_hygiene.log`).
- Not run locally, as in round 1: `check_em_dash.py` and `gen_toc.py --check` need the pinned Markdown renderer, which this host lacks, and shared installs are not allowed (`receipts/em_dash.log`, `receipts/gen_toc_check.log`).
- The PR body states the round-2 change set and limits. It does not restate the F1 premise beyond "assigns measured sizing to processor #61/#83 adoption".

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R313-2-F1 MINOR; attribution amended, see above) | scope items 1-6, decision 5789750234, assignment 5823589125 items 1-5; `SAVED_STATE_FASTCONNECT.md` s4.2, `:188-190,:440-453,:788-795,:1231-1240`; `SAVED_STATE_MATERIALIZATION.md:444,:940-946,:1636-1661,:1799-1803`; `compare_figures.log`; `figures_head.json`; D3 replay | R313-2 | `dd6a68e9063c3f7aa81536197254d187e9cb65ba` |
| RTL | UNCLEAN (R313-2-F1 MINOR) | `KL_nvm_backend.sv:145,1117-1138`; `milan_baremetal.c:508-531,937-1027`; nvm_backend suite and RTL mutants; nvm_cosim 8x8; capture copy probe at base and head | R313-2 | `dd6a68e9063c3f7aa81536197254d187e9cb65ba` |
| Robustness | UNCLEAN (R313-2-F1 MINOR) | hold-lapse void and retry path; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1054,1593-1612,1692-1707`; over-capacity mutants; `hold_margin.log` | R313-2 | `dd6a68e9063c3f7aa81536197254d187e9cb65ba` |
| Tests | CLEAN | `check_nvm_record_space.py:290-313,777-797,862-866`; `nvm_map_checks.py:70-100`; gate, self-test, named controls; crash probe and six-arm matrix; source mutants; fw host test self-test; builder fixture test | R313-2 | `dd6a68e9063c3f7aa81536197254d187e9cb65ba` |
| Docs | UNCLEAN (R313-2-F1 MINOR) | the four changed pages at every hunk; historical tables; static doc gates; PR body at head | R313-2 | `dd6a68e9063c3f7aa81536197254d187e9cb65ba` |

Only Tests is banked clean at this head. Its scope changed in this delta (the self-test loop and the guard), so it was re-applied at this head, not carried from round 1. Every lens was applied at this head.

## Prior public review findings on this PR

This section was written after the verdict and ledger above. The prior public findings are R312-1 (PR #557 comment 5823344017) and my own R313-1 (5823585783, closed above). The internal review R312-2 (5824109822) was published during this round, and I read it only at this point.

**R312-1 at this head:**

- **R312-1 F1 (MAJOR; Conformance, Docs): CLOSED.** This is the same defect as R313-1-F1, including its extra locations: `SAVED_STATE_MATERIALIZATION.md:1645-1649` no longer says "Not before #501", and the stage table row at `:1661` no longer reads "BLOCKED on #501".
- **R312-1 F2 (MAJOR; RTL, Robustness, Docs): figures CLOSED; exposure RETAINED as R313-2-F1.** UNRESOLVED 6 at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1692-1698` now carries 31.9/63.8 ms and 1.57x/0.78x.
- **R312-1 F3 (MINOR; Docs): CLOSED.** Its extra rows now read 3.07/3.26 s and 4.6/4.8 s at `SAVED_STATE_MATERIALIZATION.md:1799-1803`, and 3.07/3.26 s at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1417`.
- **R312-1 S1 and S2 (SUGGESTION; Tests): TAKEN**, as R313-1-S1 and S2 above.
- **R312-1 S3 (SUGGESTION; Tests): not taken; it stays optional.** My round-1 view stands: a renamed 1x1 stem reddens `--self-test` through the `changed_1x1_image` control's required finding. That is now enforced for every control (`receipts/gate_selftest.log`).

**R312-2 (concurrent, read after my verdict):**

- **R312-2 F1 (MAJOR; Conformance, RTL, Robustness, Docs): CONCUR. Same defect as R313-2-F1.**
  - It was found independently, with the same locations, the same probe result (12,634 B, of which 4,672 B MAPS_OUT at 8x8) and the same required outcome.
  - **Lens attribution:** I accept its Conformance attribution on the merits. Assignment item 3's "State the 8x8 exposure" is not accurately met when the stated exposure is scoped to a future event the implementation does not wait for. I amended my F1 lenses and my Conformance ledger row to match, disclosed at the top.
  - **Severity differs:** I grade it MINOR, because safety is kept and the hardware time is unmeasured. The other review grades it MAJOR. Both grades leave the same four lenses unclean and the verdict negative. The decision owner may settle the severity.
- **R312-2 S1 (SUGGESTION; Docs): CONCUR as optional.** The row at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1831` is historical by its table, and I did not treat it as a finding. A "superseded at #501" note would help a cold reader.

None of the above changes the verdict word.

## Real limits

- No hardware ran. Physical calibration was NOT RUN, and the hosted "Physical gPTP" context was skipped at this head. Neither is hardware proof.
- The copy times in F1 and in section 18 come from the page's model, not from a measurement. F1 does not rest on a time: it rests on which bytes are copied, which the probe measured on the tree's own host bench.
- The host bench has no producer. With a producer, records open during a write are skipped, so a copy can only be shorter than the full area while something is being written.
- The K16 and boundary restores are model-level, as in round 1, and the product donor writer does not exist yet.
- Not run, by instruction: the full parent, PP, gPTP, Yosys and builder banks, act, and host `act_ci` and its selftest.
- Hosted contexts at this head were listed read-only (`receipts/hosted_checks.txt`): 17 success, 1 skipped (Physical gPTP) and 2 Verilator shards still in progress at listing time. The manager owns hosted and act acceptance.
- Where the receipts ran:
  - The gate, controls, figures, firmware host test, builder fixture test and doc gates ran from the review clone.
  - Mutants, the crash probes, the capture probe, nvm_backend, nvm_cosim and the D3 replay ran on disposable clones of head and base under `scratch/`, with every submodule cloned at its pin. The two public evidence commits were fetched into the scratch clone only.
- Clone restoration:
  - The builder fixture test left an ignored `sw/builder/out/` of 56 entries, all created during this round. It was removed (`receipts/clone_cleanup.log`).
  - After that, HEAD, tree and index match, all 883 tracked files have exact bytes and modes, the three initialised gitlinks are at their pins and clean, `external` is uninitialised as at start, and nothing untracked or ignored remains (`receipts/verify_clone.log`).
  - Nothing was fetched into the review clone this round.
- Redaction: the local home prefix and the inherited PATH were redacted from receipts (`receipts/sanitize.log`).

## Pending manager duties

- Publish this report and the manifest.
- Route R313-2-F1 to the decision owner, who confirms or revises the capture-hold decision on the corrected premise, and then to the executor. Re-review the corrected head.
- Candidate-merge validation against live `dev` `ffcbd33de70278ae34b533dcbadde0b36c8cba13` (source base `573f0052a0e4412e81f0845438fcec2086ce5d55`).
- Hosted and act acceptance at the final head, including the two Verilator shards in progress at listing time.
- Merge authorization and post-merge containment.

R313-2 FINISHED
