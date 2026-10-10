[R602] NEGATIVE - exact head 9112a0df27acc1381091845e94d8eaa1407f1bbb

# R602-2: internal cleared-context review of PR #715 (issue #671), round 2

- **Head:** `9112a0df27acc1381091845e94d8eaa1407f1bbb`, tree `7589415dd1c3ab6957686a6d7f20c47a62c45ba2`.
- **Source base:** `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- **Diff:** 11 commits, 12 files, +1,335 / -336. No `hdl/`, register-map, generator or record-layout file is touched.
- **Role:** internal independent reviewer `[R602]`, round R602-2, working in its own detached clone.
- **Lenses:** all five were applied independently at this head: Conformance, RTL, Robustness, Tests and Docs.

## Verdict

**NEGATIVE, on one MINOR (F1: Tests, Robustness).**

The firmware is correct on every path I read and drove. The #671 rule is applied as decided:
- one staged read per judgement;
- OK stands on one read;
- any other verdict, blank included, stands only on two byte-identical reads within three;
- the pick is re-staged under its own sequence, and the other slot is offered if the pick never reads back;
- no sequence is taken from refused bytes;
- an UNREAD slot holds the writer, with no capture, erase, program, acknowledgement or heartbeat.

Acceptance 1 to 3 hold for the cold boot, and every round-1 finding is resolved at this head.

The gap is in the tests. The hold has two call sites: the cold boot (`milan_baremetal.c:1734`) and the writer restart without a fabric reset, the re-attach path (`:1698`). No gate reaches the second one under a read fault. A plant that removes the hold from that path alone leaves both the writer gate and `nvm_cosim` green.

## Reconstruction

I read the following in order:
1. AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6).
2. docs/README.md.
3. The #671 body, with Required and Acceptance 1 to 3.
4. On #671:
   - assignment 6098494890, including its scope (record format, register map, A/B and boot budget unchanged) and STOP condition;
   - TAKEN 6098611315 and REVIEW READY 6100491164;
   - the round-2 assignment 6100704879, whose item 1 says "the read-fault check must be able to fail for every mechanism the fix depends on";
   - round-2 REVIEW READY 6102799749.
5. FASTCONNECT sections 6.1, 6.2 and 7, and `sw/firmware/ctrl_nvm/README.md` Boot items 2 to 4 and 9. The latter is the Mark II rule the assignment applies.
6. The full diff `e8454e27..9112a0df` and its history.
7. The firmware boot, judge, re-stage, fill, go-live, commit, heartbeat and console paths at the head, plus the SoC stage layout (`sw/litex/milan_soc.py:3014-3032`).
8. The host model, checks 13 and 14, and the plants.
9. Public evidence `25ad3f94:review-evidence/671-r1`. These are round-1 author receipts. I read the MANIFEST and the builder receipt tail. The round-2 builder receipts are not in that tree.

## Findings

### F1 - MINOR - Tests, Robustness - the #671 hold on the writer-restart (re-attach) path is reached by no gate

- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1695-1699`: the branch taken when load-pending is 0 and load-accepted is 1, which calls `nvm_go_live()` at `:1698`. This PR added that call. The other added call is `:1734`, on the cold boot.
  - `sw/firmware/nvm_hosttest/test_nvm_firmware.py:735-736`: every check-13 case boots with `--boot`, which is a cold boot.
  - `sw/firmware/nvm_hosttest/nvm_host.c:847-858`: `--boot-backend` reaches only the contract, over and live retire paths, not the re-attach path.
  - `tb/verilator/nvm_cosim/stubs/generated/mem.h:7`: `SPIFLASH_BASE` is a plain array, so `nvm_cosim` can plant no read fault, and `nvm_unread` is always 0 there.
  - `sw/firmware/nvm_hosttest/read_fault_cases.py:21-24`: `restart_at_zero` plants inside `nvm_go_live()` itself, which removes the hold on both paths at once, so no control tells the two paths apart.
- **Authority:**
  - The round-2 assignment, item 1 (#671 comment 6100704879): "the read-fault check must be able to fail for every mechanism the fix depends on".
  - AGENTS.md section 6, `Tests` ("Each new test can fail for the defect it claims to detect"; "Real integration wiring is tested where practical").
  - AGENTS.md section 6, `Robustness` ("reset during activity").
  - The firmware page states that the hold applies to a writer that would go live on any path (`docs/integration/BAREMETAL_FIRMWARE.md:2015-2051`).
- **Evidence:**
  - Probe `p1_reattach_no_hold` (`probes/plant.py`) replaces only the re-attach branch's `nvm_go_live();` with the pre-#671 `nvm_ready = 1;`.
  - The shipping writer gate on `endstation_arty_4x4` stays green: "saved-state writer gate: OK across 1 shape(s)", rc 0 (`receipts/p1_reattach_no_hold.log`). That gate includes checks 1 to 14, the disabled-writer and boot-walk graders.
  - `nvm_cosim` stays green on the same plant: "465 checks: 465 PASS", "39 of 39 mutant(s) killed", rc 0 (`receipts/p1_cosim.log`).
  - On that path a read fault leaves `nvm_unread` set, but the planted writer goes live with `nvm_auth_slot = NONE` and `nvm_seq = 0` (`:1668-1675`). Its next commit targets A at sequence 1 (`:1383-1384`). That is #671's restart at zero on a CPU-only restart.
  - This last point is an inference from the source. The host model cannot drive a re-attach, which is the finding itself.
- **Impact:**
  - The head is correct (`:1698` calls `nvm_go_live()`).
  - A one-line regression on that call site would bring #671's loss back to every CPU-only writer restart that meets a boot read fault, and every gate would stay green.
- **Lens attribution:**
  - Tests: no check can fail for this mechanism.
  - Robustness: the uncovered path is a restart during activity.
  - Not Conformance. The frozen acceptance 1 and 2 are met at the cold boot, and the acceptance's planted control (`restart_at_zero`) fails as required. The gap is measured against the round-2 assignment's test bar and the Tests lens.
- **Required outcome:**
  - The host model can boot as a writer restart on a live backend (load accepted, load pending 0, window live) with a planted read fault.
  - Check 13 gains at least one such case where a slot is left unread, and requires all of:
    - the hold is named;
    - no heartbeat, erase, program or acknowledgement;
    - `backed` 0;
    - after a change and a clean reboot, every saved record survives.
  - A named `--self-test` control that reverts only the re-attach call (the `p1_reattach_no_hold` text) reddens on the first shape and both product shapes.
- **Verification:** at the new head, `probes/run_probe.sh <template> <work> p1_reattach_no_hold configs/endstation_arty_4x4.yaml 2 <logs>` exits 1 with a finding naming the case, and `--self-test` reports the new control "caught by N named finding(s)" on three shapes.

### S1 - SUGGESTION - Robustness, Docs - a slot that never reads cleanly holds the shipping writer on every boot, and the firmware page does not say so

- **Where:** `docs/integration/BAREMETAL_FIRMWARE.md:2044-2045` ("The next reset reads every slot again.").
- **Evidence and reasoning:**
  - Under #665 decision 2, a slot whose reads differ on every boot holds the writer on every boot. One way this happens: a power cut interrupts the erase of the non-authoritative slot and leaves marginal cells.
  - The only recovery is the operator's `milan_nvm wipe`, which also erases the good slot (`milan_baremetal.c:1989-2000`).
  - Before #671, a torn slot was refused and the next commit erased it. Now the writer never erases it.
  - The A/B guarantee is unchanged: one complete image survives and is loaded. Only the availability of persistence changes.
  - The Mark II page states the every-boot hold (`sw/firmware/ctrl_nvm/README.md` Boot item 9). The PR body states it under "Known limitations". The shipping firmware page does not.
  - This was not probed on hardware.
- **Suggestion:**
  - Add the Mark II sentence to the firmware page.
  - Consider a follow-up Issue for a non-destructive recovery, such as erasing only an unread slot that was not picked. That would need its own decision.

### S2 - SUGGESTION - Robustness - the runtime capture prefill still reads the authoritative slot freshly from flash

- **Where:** `milan_baremetal.c:1245-1255` (`nvm_prefill_stage`). This code is unchanged by the PR.
- **Reasoning (not probed):**
  - Open records keep these unvalidated bytes.
  - The stage is re-judged before any erase (`:1400-1408`). A record-area fault is therefore refused by the record crc16 or the erased-record rule, and the commit is deferred, not written.
  - This is outside #671, which concerns boot. It is noted because the PR's own principle, "what is loaded is what was judged", stops at the boot.

### R1 - RESIDUE - Docs - "the hold" names two different things in one sentence

- **Where:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1651`: "The firmware changed in its boot path and its console report of the hold only; `nvm_capture()`, the hold and the census are unchanged."
- **The problem:** the first "hold" is the #671 writer hold, and the second is the backend's capture grant hold. Wording only: no figure, measurement or claim changes.
- **Exact fix:** "The firmware changed in its boot path and its console report of the writer's hold only; `nvm_capture()`, the backend's capture hold and the census are unchanged."

## Prior public findings on this PR, resolved or retained at this head

I read these only after my independent pass. That pass had already produced F1, S1, S2 and R1. The p1 receipts are timestamped 00:35:42 and 00:44:51 +0200, and `VERDICT_FIXED_BEFORE_PRIOR_READ.md` records the verdict and the ledger.

**Disclosure.** At 00:45:06 +0200, a bulk fetch of the PR's comments, made to read the round-1 findings, also returned the other reviewer's round-2 report (comment 6102963708). It was already posted. I saw its opening lines and its first finding, and stopped reading it. That was after my p1 receipts and before the interim record. I did not read it further, and nothing in this report is taken from it.

| Prior finding | Status at 9112a0df | Evidence |
|---|---|---|
| R602-1 F1 (MINOR, Docs/Robustness): fault worst-case boot understated | Resolved | See details below the table. |
| R602-1 R1: FASTCONNECT 7's loss mode per store | Resolved | `SAVED_STATE_FASTCONNECT.md:781-800` carries the exact text. It matches `nvm_commit` targeting A when no slot is authoritative (`milan_baremetal.c:1384`). |
| R602-1 R2 / R603-1 R1: check numbering | Resolved | The README numbers checks 12, 13 and 14 (`nvm_hosttest/README.md:90-128`) and says "fourteen checks". No "thirteen" or "checks 12 and 13" remains. |
| R602-1 R3: SNAPSHOT_OWNERSHIP 18 names the console report | Resolved | Applied at `:1651`. The new wording ambiguity there is my R1. |
| R602-1 R4: all-0xFF reads walked at COUNT 1 only | Resolved | `nvm_hosttest/README.md:92-124` matches `fault_cases` (`--read-ff {slot}:{skip}:1`). |
| R602-1 S1: read-fault counter | Resolved | The counter is documented as a floor (`milan_baremetal.c:478-482`). |
| R602-1 S2 / R603-1 F1 (MAJOR, Tests): check 13 blind to record-area, both-valid and stage-fill mechanisms | Resolved | See details below the table. |
| R602-1 S3 / R603-1 S1: operator wipe while held | Resolved | Documented at `milan_baremetal.c:1576-1577` and `BAREMETAL_FIRMWARE.md`. Checked by `grade_hold_console` (`test_nvm_firmware.py:820-824`). |
| R603-1 F2 (MINOR, Docs/RTL): boot worst case | Resolved | Same as R602-1 F1. |
| R603-1 S2: console names the real retire cause | Resolved | `nvm_held` is set only in `nvm_go_live()` (`:1581-1591`). Checked for all four retire causes (`RETIRE_CAUSES`, `test_nvm_firmware.py:168-176, 825-830`). |
| R603-1 S3: re-stage sequence check exercised | Resolved | The `--read-other` mode (`nvm_host.c`) and control `r_restage_any_seq`, caught on three shapes. |

**Details for R602-1 F1 and R603-1 F2 (boot worst case):**
- The PR body now gives a fault worst case of about 16.4 s at 1x1 and 17.1 s at 8x8 from reset to entity enabled, labelled an ESTIMATE.
- It is summed from measured per-read costs: 1,611.6 ms per 64 KiB refused read, and 86 ms or 303 ms per container read.
- I checked the count: 2 refused judgement reads + 1 OK + 3 refused re-stages per slot gives 10 slot-length reads + 2 container reads, within the 12-read bound (`:788-825`, `:1656-1667`).
- 10 × 1,611.6 + 2 × 303 ≈ 16.7 s of slot reads. That is consistent with 17.1 s once the rest of the measured 1,247 ms both-valid 8x8 boot is added.
- The restart heartbeat note is in the PR body's limitations.

**Details for R602-1 S2 and R603-1 F1 (check 13 blind spots):**
- Check 13 now faults a record-area byte (`read_fault_cases.py:137-149`).
- It covers both slots valid in both orientations, including the wrap at sequence 0, and the older slot faulted for the whole boot (`:150-157`).
- It requires every other saved record to survive (`test_nvm_firmware.py:704-723`).
- `r_digest_header_only`, `r_fill_from_flash`, `r_restage_fail_offers_none` and `restage_fail_not_unread` are standing controls. Each was caught by its own words on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8` in my run (`receipts/base_selftest.log`).

**No prior finding is retained.** F1 above is new at this head.

## Answers from evidence

- **Sequence derivation is local to the firmware.**
  - The diff touches no HDL.
  - The sequence enters only through `nvm_read_slot` on VD_OK (`milan_baremetal.c:757-758`). It flows through `nvm_judge_slot`, `nvm_restage`, `nvm_pick_slot` and `nvm_boot` (`:1647-1675`), and `nvm_commit` uses `nvm_seq + 1` (`:1383`).
  - With no slot accepted, `nvm_seq = 0` (`:1672`), and only refused-by-content or blank verdicts reach that point without a hold.
  - Check 14 grades this, and the `generation_from_refused_slot` control reddens on three shapes.
- **Acceptance 1 (cold boot), met.**
  - My run of `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 6` at this head ends "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened", rc 0 (`receipts/base_selftest.log`).
  - It reports 34 "self-test OK" lines: all nine #671 controls on three shapes, plus the five writer controls, the PHY, disabled-writer and boot-walk controls.
  - Check 13 walks both orientations at sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF, and both-valid at 0x5A5A5 and across the wrap.
- **Acceptance 2, met.** `restart_at_zero` fails by name on three shapes. Six further independent probes of my own all redden the gate, each by a named finding (rc 1, no build error):

  | Probe | Defect planted | Findings |
  |---|---|---|
  | `p2_held_heartbeats` | held writer not retired | 81 findings, "the held writer persisted something or claimed backing", hb 7, backed 1 |
  | `p3_no_third_compare` | the third read may agree only with the first | "one faulty read held the writer" |
  | `p4_judge_no_unread_bit` | unread bit dropped | 151 findings |
  | `p5_blank_on_one_read` | BLANK stands on one read | "taken as VD_BLANK on reads that returned different bytes" and "87 other saved record(s) did not survive" |
  | `p6_tries_two` | `NVM_READ_TRIES` 2 | "one faulty read held the writer" |
  | `p7_restage_once` | one re-stage read | 26 findings |

- **Acceptance 3, met.**
  - `nvm_commit`, erase, program, verify, `nvm_capture` and `nvm_prefill_stage` have no hunk in the diff.
  - Checks 1 to 12 are unmodified. Their five controls now grade against `WRITER_GRADES`, the same checks as before.
  - `make -C tb/verilator/nvm_cosim run` with the pinned Verilator 5.050 (`--version`: "Verilator 5.050 2026-07-01 rev v5.050") gives "465 checks: 465 PASS, 0 FAIL" and "39 of 39 mutant(s) killed by their named check", rc 0 (`receipts/cosim_run.log`).
- **Closing #671.** I judge the code to satisfy #671's Required with the stated identical-fault limit. That limit is #665 round 4's accepted rule and is stated in FASTCONNECT 7 and both READMEs. "Closes #671" is supportable once F1 is answered.
- **Capture receipt.**
  - `python3 scripts/check_nvm_capture.py` gives "PASS: capture census, clocks, both timing arms and receipt agree", and its four controls fire, rc 0 (`receipts/capture.log`).
  - The receipt's tree `891f5d32` is the tree of `49d28e5a`. The firmware source blob `7f2d28f3` is identical at `49d28e5a` and at this head.
  - `9112a0df` changes only `measurements.json` and SNAPSHOT_OWNERSHIP 18.
  - The binary digest `33eaa0c3`, and the +1,712 B text delta under the pinned SDK, are author receipts. I did not reproduce them, because an RV32 build is outside this review's allowance.
- **Docs gates at this head:**
  - `scripts/docs_check.py`: 0 findings across 202 md files.
  - `check_doc_style.py`: OK.
  - `check_doc_paths.py`: OK, 957 cited paths resolve.
  - Added lines in the diff carry 0 U+2014 characters.
  - `check_em_dash.py` itself could not run, because the pinned Markdown renderer is not installed here (`receipts/em_dash.log`, rc 2).

## Clean-lens evidence

```text
[R602] PASS Conformance - sw/firmware/milan_baremetal/milan_baremetal.c:737-825,1581-1591,1647-1675,1383-1384 against #671 Required/Acceptance 1-3, assignment 6098494890, ctrl_nvm/README.md Boot 3,4,9, FASTCONNECT 6.2 and 7; receipts/base_selftest.log (5 shapes, 9 #671 controls on 3 shapes), receipts/cosim_run.log - one staged read per judgement, OK on one read, refusal/blank on two byte-identical reads within 3, re-stage under the picked sequence with fallback, no sequence from refused bytes, UNREAD holds; acceptance met at the cold boot; F1 is a test gap, not a conformance gap
[R602] PASS RTL - milan_baremetal.c:366,413-415 (stage holds a 64 KiB slot),737-761 (copy bounded by rule-3 length <= NVM_SLOT_BYTES, unsigned indices),788-825 (judge/re-stage bounded at 3),1536-1544 (window filled with NVM_IMG_LEN stage bytes, an accepted container being exactly that length by rules 10/12),1656-1667 (fallback loop ends within two passes),1084 (retired/held: no heartbeat strobe); sw/litex/milan_soc.py:3025-3032 (64 KiB stage below the live window); no hdl/ in the diff; nvm_cosim 465/465 - firmware-side widths, bounds, termination, writer state on every boot path and boot latency estimate (17.1 s at 8x8, arithmetic rechecked, inside #397's 20 s comparison)
[R602] PASS Docs - docs/design/SAVED_STATE_FASTCONNECT.md:781-800; docs/integration/BAREMETAL_FIRMWARE.md:2015-2051,2157-2164; sw/firmware/nvm_hosttest/README.md:43-55,89-163,203-215; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1811-1820 against measurements.json and the code; PR body; receipts/docs_check.log, doc_style.log, doc_paths.log - changed contracts reflected, figures match the receipt, limits stated; R1 is RESIDUE (wording only), S1 optional
```

Robustness and Tests are UNCLEAN under F1. Their examined scope was:
- **Robustness:** fault windows, the hold, both-valid and wrap layouts, the other-slot address fault, the held console and wipe, retire causes, the re-attach path (F1), torn-slot persistence (S1) and the runtime prefill (S2).
- **Tests:** checks 13 and 14, the host fault model, the nine controls, my seven probes (six caught, one not: F1), and `nvm_cosim` reach.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 body and assignments 6098494890 and 6100704879; #665 decision 2 via ctrl_nvm README Boot 3, 4 and 9; FASTCONNECT 6.2 and 7; `milan_baremetal.c` judge, re-stage, pick, go-live and commit; writer gate self-test; nvm_cosim | R602-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| RTL | CLEAN | `milan_baremetal.c` bounds, loop termination, stage and window sizes and writer state; `milan_soc.py` stage layout; no HDL in the diff; nvm_cosim 465/465 and 39/39; boot-latency estimate | R602-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Robustness | UNCLEAN (F1) | fault windows, hold, both-valid, wrap, other-slot fault, console and wipe while held, retire causes, re-attach path, torn-slot persistence, prefill | R602-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Tests | UNCLEAN (F1) | `test_nvm_firmware.py` checks 13 and 14; `read_fault_cases.py`; `nvm_host.c` fault model; nine controls on three shapes; probes p1 to p7; nvm_cosim with p1 | R602-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |
| Docs | CLEAN (R1 residue carried) | FASTCONNECT 7; BAREMETAL_FIRMWARE Boot and host suite; nvm_hosttest README; SNAPSHOT_OWNERSHIP 18 and 20 item 6 against `measurements.json`; PR body; docs gates | R602-2 | 9112a0df27acc1381091845e94d8eaa1407f1bbb |

## Real limits of this review

- **No hardware and no physical calibration (NOT RUN).** Every fault I drove is the host model's: a wrong-bytes view per mapped read. Skipped field contexts are not hardware proof.
- **The re-attach consequence in F1 is inferred from the source.** No harness here can drive a re-attach under a read fault, and that is the finding.
- **Probes ran on one shape (`endstation_arty_4x4`).** My baseline self-test covered all five shapes.
- **Not run by me:**
  - builder banks (`--require-rv32`, `--require-elaboration`);
  - the Mark II power-cut suite and the rtl-fast firmware-unit replica;
  - the capture CPU harness, so the receipt was regraded, not re-measured;
  - an RV32 build, so the size delta and the firmware digest are author receipts;
  - the act replica;
  - the pinned-renderer em-dash gate.
- **Python and timing.** Python here is 3.14.7; the author's is 3.12.3. The self-test ran at `--jobs 6` on a host shared with other load (load average about 50), and finished in about 3 minutes.
- **Hosted checks at this head** (snapshot at 2026-10-10T22:37Z, `receipts/hosted_checks_9112a0df.txt`):
  - succeeded: 12, including full-ci-gate, verilator-lint, yosys-elaboration, Yosys shards 0 to 3, Verilator shard 3/5, docs-check-no-git, bdd-conformance, wire-accountability and changes;
  - in progress: 7 (Verilator shards 0, 1, 2 and 4, firmware-unit, elaborate, docs-check);
  - skipped: 1 (Physical gPTP, nightly and manual; not hardware proof).
  - Acceptance of these belongs to the manager.
- **Clone state:** restored and verified (`receipts/restore_verify.log`, rc 0):
  - the index tree equals `7589415d`;
  - all 1,271 tracked files rehash to their index blobs, with matching modes;
  - there are no untracked or ignored entries;
  - gitlinks are at their pins: protocol-processor `2ad2f845`, gptp-processor `5dce647a` and third_party/verilog-axis `48ff7a7e`, each clean;
  - `external` and `third_party/lwSRP` were uninitialised, as at the start.
  - Session-created `__pycache__` and `nvm_cosim` build directories were removed first.

## Pending manager duties

- Carry F1 to the lane, and R1 to the residue checklist. S1 and S2 are optional, and S1 may become a follow-up Issue.
- Accept the exact-head hosted contexts and run the act replica.
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `1fb0ed9a`) with the builder and native banks.
- Re-review at the head that answers F1. Tests and Robustness must be covered again there, along with any lens whose scope that change touches.

## Receipts and scripts (listed in MANIFEST.sha256)

- `VERDICT_FIXED_BEFORE_PRIOR_READ.md`: the interim verdict and ledger, written before reading the round-1 findings.
- `probes/plant.py`, `probes/run_probe.sh` and `probes/verify_clone.sh`: portable probe and restore scripts. Probes are applied only to disposable copies.
- `receipts/base_selftest.log` and `.rc`; `receipts/cosim_run.log` and `.rc`; `receipts/capture.log` and `.rc`.
- `receipts/docs_check.log`, `doc_style.log`, `doc_paths.log`, `em_dash.log` and `docs_gates.summary`.
- `receipts/p1_reattach_no_hold.log` and `.rc`, and `receipts/p1_cosim.log` and `.rc` (F1).
- `receipts/p2_*` to `receipts/p7_*` (`.log` and `.rc`).
- `receipts/hosted_checks_9112a0df.txt` and `receipts/restore_verify.log`.
- Local workspace paths in the receipts are replaced by `<packet>` and `<review-clone>`.

R602-2 FINISHED
