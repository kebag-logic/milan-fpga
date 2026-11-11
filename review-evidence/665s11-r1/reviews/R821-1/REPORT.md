[R821] NEGATIVE - exact head b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702

Internal cleared-context review, round R821-1, of PR #881 (issue #871, Mark II split stage S11, AECP REBOOT on the CPU). Head `b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702`, tree `d8f59879fc1cd1fbf2553155fd89b05ca32b63f5`. That is six commits on `dev-soft-core` `1d6bf555`. I reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, the #871 body and its two public comments, plan decision D9 and the S6 and S11 rulings on #665, and `docs/design/REBOOT_RESET.md` (#787, PR #822). I read the clauses in IEEE 1722.1-2021 and Milan v1.2 myself, then the diff and history, then the public author packet (`5cbba57e`, `review-evidence/665s11-r1`). I read no private author material and no other reviewer's report.

All five lenses were applied. Three MINOR findings are open. One of them (F1) is attributable to all five lenses, so no lens is clean at this head and the verdict is NEGATIVE. Acceptance items 2 to 5 are met on executable evidence. Item 1 is honestly partial, and the PR correctly says "Relates to #871".

## Findings

### F1 MINOR - Conformance, RTL (architecture), Robustness, Tests, Docs - non-AECP commands are taken after the REBOOT's SUCCESS, and their frames can leave after ENTITY_DEPARTING

- **Where:** `sw/firmware/ctrl/aecp/aecp.c:195` (`aecp_ready` closes AECP only), `sw/firmware/ctrl/plat/ctrl_plat.c:180-201` (`reboot_step`), `sw/firmware/ctrl/plat/ctrl_plat.c:348` (`ctrl_plat_step`: the loop runs every protocol until the port fires). The claims are `docs/design/REBOOT_RESET.md:264` ("Only the request's source differs"), `:270` ("No command is taken after it"), `sw/firmware/ctrl/aecp/README.md:162`, the PR body's AECP-owner row ("No command after it") and the #871 REVIEW READY comment ("No command is taken after it").
- **Authority:** The processor this placement replaces "takes no command from its queue until reset ... and the top discards, whole, every frame that starts on `rx_*` after it, so no ACMP, ADP or AECP command reaches an engine". It also sends "no frame ... after the final ENTITY_DEPARTING until the reset", and raises the request only after "the last frame started, of any lane". See `protocol-processor/docs/architecture/06_aecp_engine.md` section 6.11 and REQ-FWX-001 (`protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md:557`). `REBOOT_RESET.md` section 6 states that the processor serves no command after the response. The lane's TAKEN scope says it answers REBOOT "as 7.4.43 and the processor do".
- **Evidence (executed):** I added two host tests to a disposable clone (`scripts/fw_probes.py`, probe `behaviour-acmp-after-success`, receipts `fw_probe_behaviour.log` and `fw_probe_behaviour.json`).
  - In the first test, a BIND_RX reaches the mailbox after the REBOOT's SUCCESS has left and before the reset port fires. The bind is **applied** (`sink_bound=1`) and **answered** (2 ACMP frames).
  - In the second test, ENTITY_DEPARTING has already left the mailbox and the port has not yet fired. The same BIND_RX makes **2 ACMP frames leave the mailbox after ENTITY_DEPARTING**, and the port then fires.
  - The simulation's ORDER grade probes only an AECP command before the port (`after-success`); it probes ACMP only after the port. No test covers the window.
- **Impact:** Between the SUCCESS and the port (4.457 ms in the CPU simulation, and unbounded while a ring is held) the entity keeps accepting, applying and answering ACMP and other non-AECP traffic. A controller can receive a successful bind response from an entity that has already announced its departure. A change accepted this way is then committed by the drain. The design document says no command is taken and that only the request's source differs. Neither is true for these commands.
- **Required outcome:** One of the following:
  - (a) Processor parity: from the SUCCESS, no received frame of any channel is taken, and after ENTITY_DEPARTING no other channel starts a transmission until the port fires. Add a host test and a planted defect for each.
  - (b) A public decision that records the split's difference from REQ-FWX-001. Then `REBOOT_RESET.md` section 8, both READMEs and the PR text must state exactly which commands are refused and which frames may follow ENTITY_DEPARTING, with a test that pins the chosen behaviour.

  The choice is the manager's.
- **Verification:** For (a), rerun `fw_probes.py ... behaviour-acmp-after-success`; its EXPECTs encode (a) and must pass. For (b), the new test and the corrected text.

### F2 MINOR - Tests, Docs - the simulation's item-2 plant `reset-before-the-response` does not fire the reset before the response

- **Where:** `tb/verilator/ctrl_reboot/run.py:650` (the plant, commented "the reset port fired at the REBOOT's acceptance, before its frames leave") and `run.py:730` (`plant_point` accepts any finding of the grade). The PR body cites this plant as item-2 evidence ("a mutant firing the reset before the response leaves fails").
- **Evidence (executed):** I ran the self-test myself (`reboot_selftest.log`), and `scripts/grader_probe.py` read the planted run's own log (`grader_probe.log`):
  - REBOOT in at bus cycle 11,900,127;
  - SUCCESS left at 12,130,525;
  - notification left at 12,144,497;
  - the reset port fired at 12,180,730.

  So the port fired **after** the response and the notification had left. The plant is caught only by "ORDER: ENTITY_DEPARTING did not leave between the notification and the reset port" and by "a frame given after the reset port fired was taken". It is never caught by the response clause. `plant_point` checks only `startswith('ORDER:')`, not the plant's own words.
- **Impact:** The CPU simulation never shows item 2's "a mutant that fires the reset before the response leaves fails", although the PR presents it as doing so. Item 2 itself still holds on other evidence:
  - the host defect `plat-reboot-before-the-response` (B12, response held in the ring), which I reran and which is caught by its own words;
  - the grader control `response-after-the-port`.

  So the evidence claim and the plant's comment are wrong; item 2 is not unmet.
- **Required outcome:** One of the following:
  - The plant fires the port before the SUCCESS leaves, and the self-test requires the "SUCCESS left the mailbox after the reset port fired" finding.
  - The plant, its comment, the README row and the PR row are redescribed as what the plant is (a reset before ENTITY_DEPARTING).

  In either case, `plant_point` should require each plant's own finding words.
- **Verification:** The self-test line for this plant names the response clause, or the renamed plant's own clause.

### F3 MINOR - Conformance, Docs - a single measurement is presented as "the bound", and the held-ring case is missing from the authoritative document

- **Where:** `docs/design/REBOOT_RESET.md:288` ("**The bound.** In the CPU simulation the reset port rises 222,853 CPU cycles ..."), and the PR's "Request to reset" measurement. #871 asks for "The request-to-reset bound in cycles".
- **Evidence:** The firmware stage has no deadline. It waits on `aecp_reboot_due` (every AECP completion), on `departing_owed` and on ADP's ring draining (`ctrl_plat.c:180-201`). The PR body itself says "A datapath that never drains the mailbox's rings holds the reset back". Section 8 omits this, and gives one run's figure under the heading "The bound". Section 6's 11 s link-drop grade assumes the request follows T0 promptly.
- **Impact:** A reader of the authoritative document has no stated worst case for the firmware stage, and may take one scenario's 445,707 bus cycles for a bound.
- **Required outcome:** Section 8 and the PR state the figure as a measurement of that scenario. They also state the firmware stage's bound, or that it has none while a ring is held (as the processor documents for its MAC: "A MAC that never takes a frame holds the request back").
- **Verification:** Read the text. Fixing it changes a claim about a figure, so I file it as MINOR, not RESIDUE.

### Suggestions (do not affect coverage)

- **S1 Tests:** `aecp_commands.c:547-569` claims "the routes run in the processor's order", but no test pins index-before-lock. My planted swap (`lock-before-the-index`) passes every test. Neither standard orders these routes, so this is optional. A test would be ENTITY 1 under another controller's lock, expecting NO_SUCH_DESCRIPTOR.
- **S2 Tests:** `ctrl_plat.c:332` `quiet()` retries a held face block through `aecp_face_poll`, but no test can fail without it. My planted removal (`quiet-without-the-face-poll`) passes, because the host model acknowledges a face commit at once.
- **S3 Tests:** `run.py` `grade_cut`'s "never a mix" has no shipped control. My reviewer control (`grader_probe.py`) shows it refuses a mixed replay: "a write half applied". Adding it to `CONTROLS` would bank that.
- **S4 RTL:** The all-fabric `milan_datapath` instances in `sw/litex/milan_soc.py` (the no-MAC stub near :891 and `MilanMAC`) leave `i_i_reboot_req` unconnected, while the port's own comment says "tie 0". It is harmless (the port is unread at `CTRL_SPLIT_P = 0`). Tying it 0 would match the port contract and the integrator tables.

### Comment rule

I checked every added source comment and docstring in the delta. None shows a lane label, review round, reviewer ID or issue-comment ID.

The `B11`-`B18` names in `test_plat_boot.cpp` and `plat_mutants.py` continue that file's own test-ID scheme (`B1`-`B10` at the base, as in `Boot.B10...`). They are not bench lane labels, so I record no RESIDUE for them. `S11` and `S12` appear only in prose (`tb/verilator/ctrl_reboot/README.md`, `MAILBOX_SPLIT.md`), not in source comments.

### Prior public review findings

PR #881 carries only the manager's four "review started" comments at this head. There are no prior findings to resolve or retain.

## The seven focus questions

1. **Statuses at their clauses.**
   - BAD_ARGUMENTS for fewer than Figure 7-68's 4 bytes.
   - NOT_SUPPORTED for any type but ENTITY; no MEMORY_OBJECT firmware image exists, 7.4.43.1.
   - NO_SUCH_DESCRIPTOR for ENTITY index ≠ 0.
   - ENTITY_LOCKED under another controller's lock (7.4.43.2). ENTITY_ACQUIRED cannot arise, because this entity is never acquired.
   - ENTITY_MISBEHAVING while a change waits for the platform: the #665 refusal rule, which the PR discloses.
   - Otherwise SUCCESS echoing `{type, index}` at cdl 16 (status and control_data_length per 1722.1-2021 9.2.2.5-9.2.2.6, 1722.1-2013 9.2.1.1). That code is `aecp_commands.c:547-569`, and the dispatch is `aecp_command`, which zero-fills the response and pre-sets the body length.
   - The SUCCESS notifies every other registered controller, with u=1 and each controller's own ID and sequence_id (1722.1-2021 7.5.2 lists REBOOT; Milan 5.4.5.1-5.4.5.2). That is `transmit()` in `aecp.c`.
   - Without a reset port the answer is NOT_IMPLEMENTED.

   The host tests `Core.Reboot*`, B11, B13 and B14 and the simulation's REFUSE grade cover each route. All 11 AECP REBOOT defects are caught by their own words (rerun).
2. **Order.** The simulation reproduces the order: SUCCESS 2.166 ms, notification 2.309 ms, ENTITY_DEPARTING 3.799 ms, port 4.457 ms. The release requires every AECP completion up to the last cookie handed to send, which comes through one in-order AECP ring (`aecp_mbx.c` poll). Then DEPARTING is sent on each advertising interface, and ADP's ring drains. B12 and B18 hold and fill the rings. No AECP command is taken after the SUCCESS. ACMP commands are taken, and their frames can follow DEPARTING (**F1**). The simulation's plant for this item does not do what it says (**F2**).
3. **CSR and crossing.**
   - `milan_soc.CtrlReboot` (`:3171`) is one `CSRStorage(1)`, in a bank pinned at `n_locs - 3` below the mailbox's.
   - `MultiReg` (`:3216`) crosses `sys` → `milan_cd` onto `i_reboot_req`.
   - In the split branch only, `milan_datapath.sv:10147-10149` drives `pp_reboot_req_w`, and so `reboot_ctrl.reboot_req_i`. `KL_reboot_ctrl` is unchanged; its level start is at `KL_reboot_ctrl.sv:277`, so a later 0 cancels nothing.
   - The MultiReg falls under the generic class exceptions (`clock_constraints.tcl:71-100`).
   - The CDC census diagram counts MultiReg ×4, and `CLOCK_DOMAINS.md` has the new row.
   - `G_CARRIED` (`census_split.py:249`): the census `--check` passes over 6 shapes at the head. Both author plants are refused by their own words ("driven by i_ctl_lock_held ...", "driven by a constant ..."). My third plant, `i_reboot_req | i_ctl_lock_held`, is refused too.
   - The mailbox contract is unchanged: no `mailbox.yaml` or `KL_mbx*` path is in the diff.
   - The all-fabric images are unchanged in logic: the only RTL change outside the split branch is one unread input, and the LiteX all-fabric path does not call `add_ctrl_mailbox`. Lint ratchet: 89 ≤ 89. Source-list gates: OK.
4. **Journal.** Reproduced in the simulation:
   - the write's erase came 62 bus cycles before the REBOOT, with 14 page programs after it;
   - the drain ended durable, and every item read back after the reset (completed);
   - the cut's replay read the saved snapshot whole (abandoned).

   Plant `write-torn` is caught: the drain hits its cap. Host defects `plat-reboot-stops-the-store` and `plat-reboot-hides-the-drain` (B16) are caught by their own words. The saved-state format is untouched (no `ctrl_nvm` path in the diff).
5. **Item 1 is honestly partial.** At the shipping shape the builder ships one configuration and one AUDIO_UNIT rate (`RTL_TODAY` `sampling_rates={48000}`). Those two items read back unchanged and are reported NOT RUN, and the other six items and the binding pass the #396 grader. The PR says "Relates to #871 (not closed ...)", and no commit message carries a closing keyword (6 one-line subjects, no bodies or trailers).
6. **Plants and mutants.**
   - AECP: 11 of 11, by own words.
   - Platform: 11 of 11, by own words (the 10 REBOOT defects plus the re-anchored `plat-loop-before-ready`).
   - Census: 2 of 2, by own words, plus my third.
   - Simulation: 9 of 9 by grade, but judged by grade alone, and one plant is caught for the wrong reason (**F2**).
   - Of my 8 reviewer mutants, 6 are caught and 2 escape (S1, S2).
7. **S2 harness.** The PR records the change and does not grade it. The author's `s2-base/s2-compare.txt` matches the PR text:
   - 1x1/1if: 13 of 81 paths over T_svc at both base and head.
   - 8x8/2if: 31 over at the base and 29 at the head.
   - `acmp.probe_tx.if1` went from 5.416 ms at the base to 13.602 ms at the head, newly over.

   The PR leaves the budget to S2b (#810). I did not rerun the harness.

## Lens coverage (this round)

```text
[R821] UNCLEAN Conformance - aecp_commands.c:547-569, aecp.c:195-202/400/453/635, ctrl_plat.c:171-209/332-357 against IEEE 1722.1-2021 7.4.43 (Fig 7-68, 7.4.43.1-2), 7.5.2, 9.2.2.5-6 (2013 9.2.1.1), Milan v1.2 5.4.5.1-2, 5.6.2, 5.6.3.3/Table 5.50, processor 06 6.11 / REQ-FWX-001; #871 items 1-5 and Measurements - F1, F3 open
[R821] UNCLEAN RTL - milan_datapath.sv:611-619,10147-10149; milan_soc.py:1377-1384,3171-3216; KL_reboot_ctrl.sv:277; clock_constraints.tcl:71-100; census_split.py:249,574-597 with census --check (6 shapes) and 3 plants; lint ratchet - no RTL-artifact defect; F1 open as architecture (the processor's receive discard and transmit gate have no split replacement)
[R821] UNCLEAN Robustness - refusals, repeated REBOOT (busy_drops), refusing state, no-port composition, held/full rings (B12/B18), two interfaces (platboot if2 18/18), journal write in progress, nothing after the port (B17), commands between SUCCESS and port (probe) - F1 open
[R821] UNCLEAN Tests - test_aecp.cpp Core.Reboot* (3), test_plat_boot.cpp B11-B18, aecp_mutants.py 11, plat_mutants.py 10+1, census plants 2, tb/verilator/ctrl_reboot plants 4 + controls 5, all rerun; 8 reviewer mutants - F1, F2 open; S1-S3
[R821] UNCLEAN Docs - REBOOT_RESET.md section 8, MAILBOX_SPLIT.md, CLOCK_DOMAINS.md row, integrator tables, aecp/plat READMEs, ctrl_reboot README, PR body and #871 comments; em-dash, docs_check, solution-docs, TOC gates rerun PASS - F1, F2, F3 open
```

### Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | AECP REBOOT routes and notification, platform sequence, clauses above, #871 acceptance | R821-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| RTL | UNCLEAN (F1, architecture) | `i_reboot_req` port and split assign, `CtrlReboot` and MultiReg, constraints, census `G_CARRIED` | R821-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Robustness | UNCLEAN (F1) | refusals, repetition, refusing state, rings held or full, if2, journal write, post-port quiet | R821-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Tests | UNCLEAN (F1, F2) | host tests, both mutant tables, census plants, CPU-simulation plants and controls, reviewer mutants | R821-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |
| Docs | UNCLEAN (F1, F2, F3) | REBOOT_RESET section 8, MAILBOX_SPLIT, CLOCK_DOMAINS, integrator tables, READMEs, PR and issue text | R821-1 | b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 |

## What I executed at the exact head

These are focused runs only, each a receipt in `MANIFEST.sha256`.

- `tb/verilator/ctrl_reboot/run.py --self-test --jobs 3`, with the pinned Verilator 5.050 and the product LiteX tree. Result: rc 0, `ctrl_reboot: PASS (0 finding(s))`, 9 of 9. The author's figures are reproduced exactly: 445,707 bus and 222,853 CPU cycles, 582.094 ms, 4,590.218 ms, 62 cycles and 14 programs (`reboot_selftest.log`).
- `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` (the arms, no self-test): PASS. platboot is 18/18 at if1 and if2, and every aecp, plat and rv32 arm is ok (`test_ctrl_firmware_arms.log`).
- The author's REBOOT defects, through the shipped campaign code (`scripts/reboot_mutants.py`): AECP 11/11 and platform 11/11, each `[ok]`. The "no defect names the test" lines in `reboot_mutants_plat.log` are the full-table completeness check, which a subset cannot satisfy. They are not escapes.
- Reviewer probes (`scripts/fw_probes.py`): 6 mutants caught by their expected tests; 2 escape (S1, S2); the behaviour probe gives F1.
- `sw/mailbox/publication_census.py --check` with the pinned sv2v v0.0.12 and Yosys 0.66: PASS over 6 shapes. Its `--selftest` timed out under my 10-minute foreground limit (rc 124, `publication_census.log`). I therefore ran the 2 REBOOT plants and a third of my own on planted datapaths (`census_plant_*.log`), each refused by its words.
- `scripts/lint_rtl.py --check`: PASS (89 ≤ 89). The SoC and RTL source-list gates: OK. `check_em_dash.py --base 1d6bf555`: 0 findings over 206 added lines. `docs_check.py`, `check_solution_docs.py` and `gen_toc.py --check`: all OK.
- Hosted contexts at the exact head (snapshot `hosted_checks_snapshot.txt`): 30 success, 24 pending, 1 skipped. That is an observation only; hosted acceptance is the manager's.

After the probes, the review clone is at `b29f94d7`. `git diff --quiet HEAD` returns 0. The index equals the HEAD tree, and no entries are flagged assume-unchanged or skip-worktree. The six gitlinks match HEAD (`efeb541a` external not initialised, `135afd04`, `a9e84b66`, `08ee86e8`, `70936b77`, `48ff7a7e`), and the submodule trees are clean. All probe edits were made in a separate disposable clone, which was restored too. Builds left ignored, untracked outputs in the review clone (`configs/generated/*.hex`, `sw/builder/out/`, `__pycache__`). No tracked byte changed.

## Real limits

- I did not run these, and I claim no manager source bank:
  - the full firmware self-test campaigns (580 control, 150 AECP, SRP, 109 saved-state);
  - the full census self-test;
  - the full Verilator sweep, the builder bank, Yosys shards and Vivado;
  - the S2 harness, and the linked-size and RAMB36 measurements.

  The PR's figures for those rest on the author's published receipts.
- The CPU simulation builds no datapath. "On the wire" means the mailbox's transmit face. The PHY hold is modelled for 50 of 3,500 ms, and the IPROG word and the configuration load are not modelled. Physical calibration was NOT RUN. Field skips and desk results are not hardware proof.
- The host probes use the host compiler and the host mailbox model. F1's window is shown on that model. I did not plant it into the CPU simulation.

## Pending manager duties

- A ruling on F1, option (a) or (b), and re-review of the fix commit across every lens the fix touches.
- Exact-head hosted acceptance: 24 contexts were pending at my snapshot.
- The current-dev merge candidate (source base `1d6bf555`, live dev `46c971fa0a09e2c8ca21acb95769defdc06c3068`) with its builder and native banks, at the merge turn.
- The independent external review.
- Accept or rule on the retired census acceptance item. Ruling 6554243203 named a face-block level as the expected carrier and required the census to pass without the REBOOT exclusion. This lane chose the CSR carrier, keeps the exclusion and replaces the item with `G_CARRIED`. The choice was delegated to the lane and is published in the PR and `MAILBOX_SPLIT.md`, but the item's retirement should be acknowledged.
- The S6 round 1 ruling sent "the AECP-owned items" (S6a's item 4: the maps on the datapath and the undone-value window) to S11 with the REBOOT carrier. #871's frozen body does not carry them. Confirm where they are owed.
- The S12 bench REBOOT cycles, and REQ-VER-06's "each item set away from its default", which configuration and sampling rate cannot meet at the shipping shape.

R821-1 FINISHED
