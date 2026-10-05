[R496] POSITIVE - exact head e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d

Round R496-4, internal independent review of issue #665 lane F0 / PR #668. Tree `ce7e90ddd1263ec89751eca6d836e451a87ecded`. Source base `fa450d301805881ad713b67521477bf042ddadfd`. The round-4 delta is `3ebd6ca3..e6420c0f`: four commits, with no dev merge.

## Summary

- **The round-4 assignment (5999248955) is met.** No BLOCKER, MAJOR, MINOR or RESIDUE is found in the delta. Two SUGGESTIONs are recorded (S1, S2); they do not affect coverage.
- **R497-3 F1 is RESOLVED.** Owed DEPARTINGs are capped at two by construction. A further SHUTDOWN is coalesced into the queued DEPARTING and counted. The wire-semantics argument holds:
  - against the repository's transcription of Milan v1.2 Table 5.54;
  - against a differential probe over 400 random seeds versus an unbounded-queue reference;
  - at 2^32 + 3 coalesced SHUTDOWNs.
- **R496-3 F1 is RESOLVED.** The k + 1 statement is consistent in `ctrl_loop.h` A3, `adp_mbx.h`, `MAILBOX_SPLIT.md` and the PR body. R496-3's own probe, unchanged, now gives pass 3 for k ≥ 2, where it gave up to pass 65.
- **R496-3 F2 is RESOLVED.** A18 to A20 guard the three legs. All 7 applicable R496-3 reviewer copies are killed by the head's own `adp` arm. The eighth is re-planted at its new site and caught by A16.
- **Ledger:** all five lenses are CLEAN at this head.

The independent pass over the diff, and my own probes, were completed before I read any prior finding text. I then read only my own round-3 report (R496-3). I did not read the other reviewer's reports. R497-3 F1 is graded from the round-4 assignment's statement of it.

## Findings

### S1 - SUGGESTION - RTL (architecture), Docs - A3's multi-frame figure counts from "the merge frees the room" without saying room for how many frames

- **Where:** `sw/firmware/ctrl/loop/ctrl_loop.h:43-50`; `sw/firmware/ctrl/adp/adp_mbx.h:69-82`; `docs/design/MAILBOX_SPLIT.md:354-360,374-384`.
- **Evidence:**
  - A poll sends one owed frame per pass. So "committed in pass k + 1 counted from the first pass that starts after the merge frees the room" holds when the ring has room for all k + 1 frames.
  - E5 (`test_adp.c:767-823`) releases the whole ring at once (`mbx_model_tx_pause(&model, false)`). So does R496-3's `probe_owed_bound.c`.
  - A merge that frees one record at a time, behind a slow sink, spreads the k + 1 frames over k + 1 room events.
  - A3's premise ("a response finds room in its transmit ring") reads naturally as room for the owed frames, so this is not a false claim. It is a precision gap that appeared when the figure went from one frame to k + 1.
- **Impact:** a later lane composing figures from A3 might read the bound as starting from the first freed record.
- **Suggested outcome:** say "room for its k + 1 frames" (or "the k + 1 frames each find room") in A3, the `adp_mbx.h` owed-frames paragraph and the design page.
- **Verification:** read-back of the three sentences.

### S2 - SUGGESTION - Tests - the stated owed-frame figures are not pinned by a check

- **Where:** `sw/firmware/ctrl/adp/adp_mbx.h:122-124`; `sw/firmware/ctrl/test/test_adp.c:811,813`.
- **Evidence:**
  - Reviewer mutant `rv-owed-passes-inflated` replaces `ADP_MBX_OWED_PASSES` with 9. It survives (`receipts/reviewer_mutants.log`). E5 compares `at <= ADP_MBX_OWED_PASSES` and `accesses <= ADP_MBX_OWED_ACCESSES`.
  - The behaviour itself is graded more strictly, by `at == k + 1u`. Killed mutants `departing-queue-unbounded`, `rv-loop-polls-twice` and `rv-poll-two-frames` show it.
  - The existing figures `ADP_MBX_EVT_ACCESSES` and `ADP_MBX_RX_ACCESSES` follow the same pattern, which earlier rounds accepted.
- **Impact:** a drift between the macro and the "3" and "1,628" stated in prose would not be caught. The behaviour would still be caught.
- **Suggested outcome:** a check or a static assertion tying `ADP_MBX_OWED_PASSES` to 3 and `ADP_MBX_OWED_ACCESSES` to 1,628, as the prose states.
- **Verification:** `rv-owed-passes-inflated` is killed.

## Clean lenses (same format as findings, with evidence)

```text
[R496] PASS Conformance - sw/firmware/ctrl/adp/adp.c:107-115,154-175,269-281; adp/adp.h:33-57,87; protocol-processor/tb/adp_engine/sim_main.cpp:261-320 (pinned ead80360, its Table 5.54 transcription: DEPARTING x TK_NOT_DISCOVERED is "Table 5.54 -", ignored, for both interface_index rows); protocol-processor/docs/architecture/04_adp_engine.md F04.7/F04.8 - the cap of two owed DEPARTINGs and the coalescing rule checked against round-4 item 1 option 1, Milan v1.2 5.6.3.5.8/5.6.3.5.11 and Table 5.54, IEEE 1722.1-2021 6.2.2.15 and Figure 6-3 per ruling 5994972330; while any DEPARTING is owed available_index stays 0 (advertise refuses at adp.c:124), so the queued and every coalesced DEPARTING carry 0 and nothing this interface sends leaves between them; MBX_N_IF is 1 (mbx_contract.h:27); differential probe: 400 of 400 seeds, states equal and wires equal to the unbounded reference after collapsing back-to-back identical DEPARTINGs, 3,721 reference-only frames, all such repeats; A19's Table 5.51 reading (GM_CHANGE and DISCOVER ignored in DELAY) matches F04.7
[R496] PASS RTL - git diff 3ebd6ca3..e6420c0f over hdl, tb, syn, configs, sw/litex, sw/builder, sw/mailbox, scripts and every gitlink is empty (gitlink listing sha256 identical at both heads); sw/firmware/ctrl/loop/ctrl_loop.c:130-148 (events, receive, then one poll per module per pass) against ctrl_loop.h:28-50 A1-A4; adp.h:147-171 widths (departing_owed 0..2, departing_coalesced modulo 2^32 as stated at :162); adp_mbx.h:122-124 unsigned macro arithmetic (3, 1,628); tb/verilator/mbx make -j16 from a clean export, both adapters and the co-simulation running the round-4 firmware: 134 + 179 + 13 checks, 0 failures, 0 Verilator warnings, quick mutants 4 of 4
[R496] PASS Robustness - adp.c shutdown/link_change/gm_change/timer_expired/rx/poll under a stalled port: free-mode probe of 400 seeds x 20,000 random inputs (enable, SHUTDOWN, link up/down, GM change, DISCOVER, expiry, room on/off, poll) holds I1 owed <= 2, I2 index 0 while owed and the queued one carries 0, I3 SHUTDOWNs acted on = sent + owed + coalesced, I4 no AVAILABLE while a DEPARTING is owed, I5 one frame per poll (300,103 SHUTDOWNs acted on, up to 236 coalesced in one seed); 2^32 + 3 coalesced pairs through the public API: two owed, index 1, the counter wraps to 3, then the wire carries DEPARTING 1, DEPARTING 0, AVAILABLE 0 and the machine is in WAITING (probe_wrap.log); R496-3 probe_owed_rules L1-L3 correct at the head
[R496] PASS Tests - sw/firmware/ctrl/test/test_adp.c:391-462 (A18-A20), 464-495 (A21), 767-823 and 982-986 (E5); ctrl_mutants.py:48-87; test_ctrl_firmware.py --self-test at the head: model 134, port 81, adp 163, walk 320, entity 45, rv32 1, 51 of 51 defects caught by their named checks; R496-3's 7 applicable reviewer copies killed by the head's adp arm, the eighth re-planted at its new site (ctrl_mutants.py:53) and caught by A16 (14 checks); 9 of 10 round-4 reviewer mutants killed by name, as expected, and the tenth (S2) survives, as expected; the differential probe's self-check fails all four planted coalescing defects
[R496] PASS Docs - docs/design/MAILBOX_SPLIT.md:287-323,354-384; sw/firmware/ctrl/README.md:45,72-79; the adp.h, ctrl_loop.h and adp_mbx.h comments; the PR body at review time (receipts/pr668_body_at_review.md:62-64,90-106) - each states the cap of two, the coalescing and counting, and the k + 1 / pass 3 / 1,628 figure consistently with the code and the measurements (63 to 99 accesses, reproduced by R496-3's probe: 63/69/93/99); docs_check 0 findings, doc style OK, check_em_dash --base fa450d30 0 findings over 2,304 added lines (and its selftest, 339 arms), gen_toc --check and --verify-anchors OK, git diff --check fa450d30 HEAD rc 0, and the bare-metal-only, hygiene, Python and C/C++ idiom gates and ci_scope --selftest all rc 0
```

## Prior findings, graded against the round-4 assignment (5999248955) after the independent pass

| Prior item | Disposition at e6420c0f | Evidence |
|---|---|---|
| R497-3 F1: a SHUTDOWN silently dropped when the owed-DEPARTING counter is full | **RESOLVED** (option 1: bounded by construction, coalesced and counted) | See "R497-3 F1 in detail" below. |
| R496-3 F1 (MINOR): the stated bound said the first pass, but the AVAILABLE left in pass k + 1 | **RESOLVED** | The restatement is consistent across the four places named, with k ≤ 2: `ctrl_loop.h:43-50`, `adp_mbx.h:69-82,122-124`, `MAILBOX_SPLIT.md:354-360,374-384` and the PR body at lines 63 and 96-98. R496-3's `probe_owed_bound.c`, unchanged (sha256 in `receipts/r496-3_probe_copies.sha256`), against the head gives: k = 0, 1, 2 → passes 1, 2, 3; k = 3, 16, 64 → pass 3 at 93/99 accesses (round 3: passes 4, 17, 65, up to 1,959). E5 grades k = 1, 2, 64 with the expiry before and after the room. `departing-queue-unbounded` fails E5 by name. My `rv-loop-polls-twice` also fails E5, so E5's equality sees an early commit as well as a late one. Precision remainder: S1. |
| R496-3 F2 (MINOR): three legs of the owed-frame rule unguarded | **RESOLVED** | A18 covers a link loss and its return during the restart, before and after the expiry. A19 covers a GM change, a DISCOVER and a stray expiry in DELAY. A20 covers a link loss with no poll between. R496-3's copies `link-loss-drops-owed-departing`, `gm-change-drops-owed-available` and `link-loss-keeps-owed-available` fail A18, A19 and A20 (`receipts/r496-3_probes_at_head.log`). `queued-departing-keeps-first-index`, `poll-forgets-owed-available`, `blocked-available-not-owed` and `poll-sends-two-frames` are also killed. `second-shutdown-overwrites-index` reports "PATCH SITE NOT UNIQUE (0)" because its line was replaced. Its semantic equivalent is planted at `ctrl_mutants.py:53` and caught by A16. My `rv-link-loss-while-disabled-drops-departing`, the link-change leg while disabled, is killed by A8. |
| R496-2 R1 (RESIDUE): `CI_WORKFLOWS.md` wording (= R497-3 R1) | **RETAINED as RESIDUE** | The file is unchanged in round 4. The exact fix from R496-2 stands, and the manager carries it on the residue checklist. |
| R496-2 S1 to S5 | retained as suggestions | Not taken. They do not affect coverage. |
| R496-3's verdicts on the earlier items (R497-2 F1, R497-2 F2 = R496-2 N3, R496-2 N1, R496-2 N2) | stand | The delta touches none of their artifacts, except `adp.c`'s queue rule. A15 to A17 and E4 still pass, and the named defects for them are still caught. |

### R497-3 F1 in detail

- **Construction:**
  - `adp.c:166-174`: the first SHUTDOWN owes its DEPARTING with its index. The second queues one behind it, with `departing_owed` at 2. Any later SHUTDOWN only increments `departing_coalesced`.
  - `depart()` (`adp.c:108-115`) sends the oldest and zeroes the index the next one carries.
  - The SHUTDOWN still stops the timer, zeroes `available_index`, drops the run's owed AVAILABLE and enters DOWN on every branch (`adp.c:159-165`).
- **Why the dropped frame is only a back-to-back repeat:**
  - `advertise()` refuses to send while any DEPARTING is owed (`adp.c:124`). So `available_index` stays 0, and no AVAILABLE can leave between the queued DEPARTING and a coalesced one.
  - Both would carry 0 and are built at send time from the same entity model.
  - With `MBX_N_IF` at 1, no other interface's frame shares the channel.
  - The differential probe confirms this mechanically. Over 400 seeds, with full drains whenever there is room, the head and the unbounded reference end every step in the same state. Their wires are equal once back-to-back identical DEPARTINGs are collapsed. The reference sent 3,721 frames the head did not, every one such a repeat.
  - The probe is not vacuous. Its self-check fails four planted defects: dropping the queued DEPARTING, overwriting the oldest index, a cap of one, and an uncounted coalesce.
- **Receiver side:**
  - The pinned processor's transcription of Milan v1.2 Table 5.54 (`protocol-processor/tb/adp_engine/sim_main.cpp:314-317`) has DEPARTING × TK_NOT_DISCOVERED as `-`, ignored, for both interface_index rows.
  - DEPARTING with a different interface_index × TK_DISCOVERED is also ignored (5.6.4.5.3 step 1).
  - So a listener that took the earlier DEPARTING does not act on the repeat.
  - For IEEE 1722.1-2021, a removal finds nothing left to remove. Clause number: see Real limits.
- **Mutants:**
  - `coalesced-departing-uncounted`, `coalesce-drops-queued-departing` and `coalesce-overwrites-oldest-index` are caught by A21 by name.
  - `departing-queue-unbounded` is caught by E5.
  - My `rv-cap-three`, `rv-cap-le`, `rv-queue-counts-as-coalesced`, `rv-coalesce-drops-both` and `rv-coalesce-keeps-available-owed` are killed by A21. `rv-depart-keeps-oldest-index` is killed by A16, A21 and E5.
- **Scale:**
  - A21 runs 100,001 coalesced SHUTDOWNs.
  - My `probe_wrap.c` runs 2^32 + 3 through the public API. Two DEPARTINGs stay owed, index 1 is kept, and the counter wraps modulo 2^32 as `adp.h:162` states. The wire then carries DEPARTING 1, DEPARTING 0, AVAILABLE 0.
- **Risk the executor already states:** a coalesced SHUTDOWN loses the extra copy that would have been one more chance against frame loss. ADP recovers from loss through valid_time. This is the trade the assignment's option 1 accepts.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-4 items 1-3 against `adp.c:107-281` and `adp.h:33-57,87`. Milan v1.2 5.6.3.5.x, Table 5.51 (F04.7) and Table 5.54 (pinned `sim_main.cpp:261-320`, 04 F04.8). IEEE 1722.1-2021 6.2.2.15 and Figure 6-3 per ruling 5994972330. Differential probe, 400 seeds, against the unbounded reference. | R496-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| RTL | CLEAN | Empty delta over HDL, tb, syn, configs, SoC/LiteX/builder, scripts and gitlinks. `ctrl_loop.c:130-148` pass order against A1-A4. Widths in `adp.h:147-171`. `adp_mbx.h:122-124` arithmetic. `tb/verilator/mbx` (Verilator 5.050, identity in `receipts/verilator_identity.txt`): 134/179/13 checks, 0 warnings, 4 of 4 quick mutants. S1 (SUGGESTION) only. | R496-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Robustness | CLEAN | Free-mode invariants I1-I5 over 400 × 20,000 random inputs. 2^32 + 3 coalesced SHUTDOWNs. R496-3 L1-L3 at the head. Link loss while disabled (A8). | R496-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Tests | CLEAN | `test_adp.c` A18-A21 and E5. `ctrl_mutants.py` (51 of 51 by name). R496-3's 8 copies (7 killed; 1 re-planted and caught). 10 round-4 reviewer mutants (9 killed by name; 1 survivor expected, S2). The probe self-check. S2 (SUGGESTION) only. | R496-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Docs | CLEAN | `MAILBOX_SPLIT.md:287-323,354-384`. `sw/firmware/ctrl/README.md:45,72-79`. The `adp.h`, `ctrl_loop.h` and `adp_mbx.h` comments. The PR body (consistent). docs_check, doc style, em-dash (`--base fa450d30`) and its selftest, gen_toc check and anchors, `git diff --check`, bare-metal-only, hygiene and idiom gates, all rc 0. R496-2 R1 residue retained for the manager's checklist. S1 (SUGGESTION) only. | R496-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |

## Executed (receipts under `receipts/`, sources under `probes/`)

- **Firmware gate:** `test_ctrl_firmware.py --self-test` (`fw_selftest.log`, rc 0). The RV32 arm ran and passed with the compiler present. `--require-rv32` and `--lwsrp` were not passed.
- **Mailbox suite:** `make -C tb/verilator/mbx -j16 VERILATOR=<pinned 5.050>` from a clean `git archive` export of the head (`mbx_suite.log`, rc 0).
- **My probes** (`probes/run_probes.sh`, `probe_coalesce_diff.c`, `compare_traces.py`, `probe_selfcheck.sh`, `probe_wrap.c`, `reviewer_mutants.py`):
  - `probe_diff.log` and `probe_free.log` (`probes.rc` 0);
  - `probe_selfcheck.log` (rc 0);
  - `probe_wrap.log` (rc 0);
  - `reviewer_mutants.log` (rc 0, 10 of 10 as expected).
- **R496-3's probes**, copied unchanged under `probes/r496-3/` and run against the head export: `r496-3_probes_at_head.log` (rc 0).
- **Gates:** `gate_*.log` and `.rc`, all rc 0. `check_em_dash` and `gen_toc` ran with the pinned renderer from `tools/markdown/requirements.txt`, installed in a disposable environment under scratch.
- **Hosted snapshot:** `hosted_checks_at_head.tsv`.
- **Restore:** `restore_check.txt`.
  - The clone was never edited. Probes and the suite ran on exported copies.
  - The Python cache directories my runs created were removed.
  - Afterwards:
    - HEAD and tree equal the head;
    - status, including ignored and untracked files, is empty;
    - the worktree and index equal HEAD;
    - every tracked blob was rehashed and every mode checked, with no mismatch;
    - the four gitlinks equal the head (`external` uninitialised, as at the start).
  - Host paths in two receipts are normalized to placeholders.

## Real limits

- **Not run by me:**
  - the builder bank and the parent, PP, gPTP and Yosys banks;
  - `xvlog_gate`, `lint_rtl`, the default-build export comparison and a switch-on OOC area;
  - the full RTL mutation campaign (`mutants.py`, 46);
  - the lwSRP arm.

  The round-4 delta touches no HDL, SoC, LiteX, builder, `syn`, config, script, gitlink or port-layer file (empty diff). So R496-3's RTL and default-build evidence carries forward by file identity. It was not re-executed here. The manager reports these banks passed at this head.
- **Clause numbers:**
  - Milan v1.2 Table 5.54 was checked against the pinned processor's transcription, not against the standard's text.
  - The IEEE 1722.1-2021 clause number 6.2.6.3.5 for `removeEntity` could not be checked from repository sources. The argument does not depend on it: removing an absent record is a no-op under any numbering.
- **Measurement scope:**
  - The co-simulation runs its fixed scenario.
  - E5 and both bound probes release the whole ring at once (S1).
  - Time per mailbox access (A4) is not measured. The figures are access and pass counts on the host model.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Publish this packet.
- Carry R496-2 R1 (= R497-3 R1) to the residue checklist. S1 and S2 are optional.
- Hosted acceptance at the exact head. At my snapshot: 11 contexts succeeded, 7 were in progress (Verilator shards 0, 1, 2 and 4, `yosys-elaboration`, `docs-check`, `elaborate`) and 1 was skipped ("Physical gPTP (nightly and manual)", not executed). The `act` replica is also the manager's.
- Build the final current-dev candidate (source base `fa450d30`, live dev `28f9666f`) at the merge turn.
- The second independent positive review, and acceptance of the completion ledger.
- Merge authorization and post-merge containment.

R496-4 FINISHED
