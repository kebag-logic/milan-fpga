[R470] POSITIVE - exact head 03895b63a3e8197353c2483593927b92efb73092

# R470-2 internal cleared-context review: issue #653 / PR #655

- **Head:** `03895b63a3e8197353c2483593927b92efb73092`, tree `c43cabe5a60ee90e737e268e27532221f176c288`.
- **Source base:** `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. Live dev at review time is `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`, already merged into the head.
- **Pins:** processor `631eeb34`, gPTP `5dce647a`, verilog-axis `48ff7a7e`, `external` `efeb541a` (not initialized, as at the start). All are unchanged against the base.
- **Scope reconstructed from public state, in this order:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #653 body;
  - the lane comment (5980090994), the executor's STOP (5980272602), the re-scope ruling (5980290102), REVIEW READY (5982287900) and the bench-lane pointer (5983013751);
  - the PR #655 body, including its "Manager round 1b" note;
  - REQUIREMENTS.md REQ-VER-06 and the REGISTER_MAP CRF rows;
  - the diff `fea346e7..03895b63` and its history;
  - the published evidence tree `c4b00e84:review-evidence/653-r1`. Its logs are from round 1 at `77ea6cb4`, so I used them only as a cross-check.
- **Frozen scope (the ruling's four items):**
  1. Fix the CRF invariant, parent only, with no port, register or parameter change.
  2. Add standing `[UNB]` tests in the `milan_dp` notify leg for AAF and CRF, for both order and invariant. Each needs planted controls (order reversed, CRF unlock not counted, double count), recorded in the bench README.
  3. Report the OOC 1x1 area delta, with a STOP above 30 LUT or 60 FF.
  4. Correct the stale pointer in the PR body.

  The hardware order and acceptance 4 (20 controller connects) are manager bench items, so the PR says "Relates to #653".
- **Prior public findings:** I read them only after my own pass over the diff. All are resolved or retained below.
- **Lenses applied:** all five, each with its own artifacts.

## What changed since the last reviewed head (`77ea6cb4`)

- **Lane commit.** `b2098fd9` touches only `CHANGELOG.md` (one line) and `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+6/-3).
- **Merge of dev.** `03895b63` merges dev `6c22d3ca` (PR #650: `syn/resmap/*`, `docs/findings/649_*`, `docs/findings/README.md`) with no conflicts.
- **The merge preserves the lane diff.** `git diff fea346e7 b2098fd9` and `git diff 6c22d3ca 03895b63` are identical apart from `index` lines (MERGE_LANE_DIFF_IDENTICAL, `receipts/merge_and_pointer_checks.txt`).
- **RTL and test bytes are unchanged since round 1.** Every lens was nevertheless re-applied at this head, and its evidence re-run.

## Findings

No BLOCKER, MAJOR or MINOR is open. This round records two RESIDUE findings (wording only) and one new SUGGESTION, and retains three prior SUGGESTIONs.

### R470-2-F1 RESIDUE (Docs): PR #655 body, "Status", "How to get into the same state" and "Local gates": stale head references

- **Evidence.** Three places in the body still describe the round 1 head:
  - Status says "head `77ea6cb4`, four commits on dev `fea346e7`".
  - The checkout block comments `# head 77ea6cb4`.
  - The gate table is introduced as "Local gates at `77ea6cb4`".

  The PR head is `03895b63` (`b2098fd9` plus a merge of dev `6c22d3ca`). The closing "Manager round 1b" paragraph records this, but those three places do not.
- **Why RESIDUE.** The gate figures were measured at `77ea6cb4`, and the RTL and test bytes are unchanged since then (above). No measurement, figure, verdict, test or claim changes.
- **Exact fix:**
  - Status: "head `03895b63` (lane commits on dev `fea346e7`, merged with dev `6c22d3ca`)".
  - Checkout comment: `# head 03895b63`.
  - Gate heading: "Local gates at `77ea6cb4` (RTL and test bytes unchanged at `03895b63`)".
- **Verification:** read the PR body.

### R470-2-F2 RESIDUE (Docs): `tb/verilator/milan_dp/README.md:661-663`: registration is listed as a per-input step

- **Evidence.** The README reads "For each input it does the following: 1. registers controllers A and B; ...". But `sim_nxn.cpp:2614-2630` (`unbind_order_section()`) registers A and B once (`:2620-2623`), before the loop over the two inputs (`:2625`).
- **Why RESIDUE.** It describes the procedure, not a check, figure or verdict.
- **Exact fix:** replace the lead-in and step 1 with "It registers controllers A and B once. Then, for each input, it:", and renumber the remaining four steps from 1.
- **Verification:** compare the README with `sim_nxn.cpp:2614-2630`.

### R470-2-S1 SUGGESTION (Docs): `docs/design/MEDIA_CLOCK_FOLLOWING.md:1059-1063`: rule 1 states the general case before the CRF exception

- **Evidence.** The first sentence of rule 1 lists "was unbound" among the 100 ms causes. The added sentence then says a followed CRF input's lock falls at the unbind itself.
- **Assessment.** Read together, the contract is correct, so this is not a defect.
- **Optional rewording:** "falls after 100 ms with no accepted PDU: the stream stopped, was STOPPED or was rejected, or a followed AAF input was unbound."

### Retained SUGGESTIONs (optional, unchanged at this head)

- **R470-1-S1 = R471-S1 (Tests, RTL).** No root-level check grades a followed CRF input's unbind with CRF selected. Such a check would require one restart request at the unbind, none at the timeout after it, and HOLDOVER entered.
  - I re-ran `milan_dp_mclk`: 168 checks pass (55/0, 32/0, 50/0, and the 31/31 control campaign).
  - That suite does not unbind, so the suggestion stands.
- **R471-S2 (Tests).** `unb_mutants.py` has no `--jobs` option. This round ran the five selectors concurrently by hand: about 3.6 minutes of wall time.

## Prior public findings, resolved or retained at this head

| Finding | Severity | Status at `03895b63` | Evidence |
|---|---|---|---|
| R470-1-F1 (`MEDIA_CLOCK_FOLLOWING.md` sequence-gap pointer) | RESIDUE | **Resolved** | `:1502` now reads `(:405-407)`, and `KL_crf_rx.sv:405-406` is the `rate_break_w` sequence-gap term. |
| R470-1-S1 (followed-CRF consumer check) | SUGGESTION | Retained (optional) | Above. |
| R471-F1 (lock-loss rule omits the CRF unbind fall) | MINOR | **Resolved** | `MEDIA_CLOCK_FOLLOWING.md:1061-1063` now reads: "A followed CRF input's lock falls at the unbind itself, counting one MEDIA_UNLOCKED (#653); a followed AAF input's meter lock still falls at its own 100 ms timeout. HOLDOVER and the restart request follow either fall." Rules 2 to 4 (`:1064-1081`) still read true for both sources, because HOLDOVER and the restart key on the fall, not on its timing. The dated bench record `docs/findings/629_*:1647` is left as recorded, as R471-F1 itself required. |
| R471-F2 (changelog states the order as a device fact) | MINOR | **Resolved** | `CHANGELOG.md:50`: "Simulation shows the UNBIND_RX response leaving before the counters push. The hardware order in #653 awaits a bench capture." |
| R471-F3 (two pointers at `:964` and `:1499`) | RESIDUE | **Resolved** | `:964` reads `(:397-410)` and `:1502` reads `(:405-407)`. Every moved `KL_crf_rx` pointer on the design page was checked mechanically: 15 of the 16 address text byte-identical to their dev range. The 16th is the intended `:34-38`, which gains the unbind wording (`receipts/merge_and_pointer_checks.txt`). |
| R471-S1, R471-S2 | SUGGESTION | Retained (optional) | Above. |

## Lens results, one line per clean lens

```text
[R470] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:395,:627-631,:540-545,:641-696,:314; hdl/milan/milan_datapath.sv:5625-5626; receipts/J1_milan_dp_notify_head.log [UNB] U1-U4 at 03895b63 - against Milan v1.2 5.3.8.10 Table 5.6 and ruling items 1-4: a locked CRF input's unbind scores one MEDIA_UNLOCKED at the bind fall (+200), so the source pair reads 1/1 as the UNBIND_RX response leaves (+277), GET_COUNTERS after it reads 1/1/0, and past both 100 ms timeouts it still reads 1/1/0; STREAM_INTERRUPTED never counts the unbind; the response precedes every unlock push on AAF 0 and CRF 1 (+277 vs +2294/+3057); no port, register field or parameter change; area under the 30 LUT / 60 FF STOP; the PR body carries the item 4 pointer correction and "Relates to #653" as ruled
[R470] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:354,:393-395,:445-465,:536-565,:567-616,:627-631,:641-696; hdl/milan/milan_datapath.sv:2661,:3172-3232,:5596-5653,:5745-5746 - single clock domain, no CDC; the edge reuses the existing en_q (no new flop, no reset change); on the same edge as the timeout arm, both write the identical non-blocking cnt_unlocked_o+1; no accept or lock rise can share the fall cycle (w_hit is gated by en_i); the bind-rise wipe stays the last writer, and rise and fall are mutually exclusive; 32-bit wrap like the other tallies; the consumers (CRF_CTRL[31], the 4.4.4.3 restart edge, the servo ref lock) see one fall per unbind, earlier; Yosys OOC (AX 1x1 TDM8 shape) re-run at dev and head: 433->368 LUT, 544->544 FF, 1 RAMB18 (receipts/ooc_yosys_KL_crf_rx_{dev,head}.log); lint 90<=90 with pinned 5.050 (receipts/lint_rtl_check.log)
[R470] PASS Robustness - tb/verilator/crf_rx/sim_main.cpp [UNB-a..e], [5t-g2b], [5t-g3], [5t-g3b]; probes/crf_unit/SUMMARY.txt; probes/P1_aaf_no_bindfall_unlock.log - covered: an unbind of a locked input; an unbind of an unlocked, settling input (no count, no pulse); an unbind on the timeout's own edge (one count, one pulse); a stopped input still holding its lock (one count); the talker streaming, with gaps, into the unbound input (no STREAM_INTERRUPTED, no second count at the timeout); silence while bound (still unlocks); reset clears en_q (no spurious fall); a repeated UNBIND on an unbound input (no edge); the bind-rise wipe after an unbind. Reviewer fault probes (the dev RTL, the lock gate removed, the lock kept, no dirty pulse, a shared-edge double count) are each caught by named unit checks; the AAF bind-fall unlock removed is caught by AAF U3 in the notify leg
[R470] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:2293-2630,:2840; tb/verilator/milan_dp/unb_mutants.py; tb/verilator/milan_dp/Makefile CRFRX_SRC/unb-mutants; tb/verilator/crf_rx/sim_main.cpp:1010-1070,:1474-1601; scripts/measure_test_evidence.py:669-673 - notify leg 421/0 with 38 [UNB] checks (receipts/J1); all five unb mutants caught, with their named breaks failing and named holds passing (4, 2, 2, 2, 2 of 421; receipts/J4_*); the order mutant's kept leg output shows exactly the four U2 order checks failing, with the response at +6277 behind the pushes (probes/P7_*); crf_rx 16567/0 (receipts/J3); milan_dp_mclk 168/0 (receipts/J5); the [5t-g3] re-pin fails against the dev RTL together with [5t-g3b] and [UNB-a1,a2,a4,a5,b2,e1], so it tightens the check rather than weakening it; measure_test_evidence --check PASS with 0 unexplained DUT-source readers
[R470] PASS Docs - CHANGELOG.md:11,:41-58; docs/design/MEDIA_CLOCK_FOLLOWING.md:295-299,:494,:516,:531,:632,:759,:964,:973,:991-997,:1059-1081,:1499-1503; docs/reference/REGISTER_MAP.md:188,:851; docs/testing/TESTING.md:273,:311-313; tb/verilator/milan_dp/README.md:75,:93,:656-715,:1073; hdl/milan/milan_datapath.sv:3174-3176; KL_crf_rx.sv header :34-38,:138-142; PR #655 body - of the 16 moved KL_crf_rx pointers, 15 resolve to text byte-identical to their dev range and the 16th (:34-38) carries the intended unbind wording (receipts/merge_and_pointer_checks.txt); the trace and mutant tables equal the reproduced runs, including "exactly the four U2 order checks" (P7); the R471-F1/F2 fixes and both RESIDUE pointer fixes are present; em-dash gate 0 findings over 113 added lines, doc-path gate OK, doc-style OK, docs_check 0 findings; the open items are RESIDUE F1/F2 only, which under the 2026-10-02 owner rule leave the lens clean
```

## Examined, not findings

- **The CSR lever.** `en_i = cfg_crf_en | acmpl1_bound` and `sid_i = acmpl1_bound ? acmpl1_sid : cfg_crf_sid` (`milan_datapath.sv:5625-5626`). With the bench lever `CRF_CTRL[0]` held, an ACMP unbind is not a fall, so the unlock waits for the timeout or for the swapped `sid_i` to go silent. This predates the lane, `REGISTER_MAP.md:851` documents it ("enable and ACMP bind both low"), and the lever resets to 0.
- **Re-bind without unbind.** A BIND_RX that re-targets an already-bound CRF input to another talker is not a bind edge in `KL_crf_rx`. This predates the lane and is outside the ruling.
- **The silent return in `[UNB]`.** `unbind_order_section()` returns silently on a shape mismatch (`sim_nxn.cpp:2617`). `[GSI]`, earlier in the same leg, fails a named check on the same guard (`:2269-2271`), so the leg cannot pass silently.
- **Why the response leads.** The response is queued at +193, before the debounced bind level falls (+199) and before any unlock (+200/+204). ACMP also holds the top TX class on the processor's single TX stream. So the response leads by construction, and the order mutant proves that the check catches a reversal.
- **The 629 bench record.** Its "Declared" column ("Lock falls 100 ms after the last PDU") is a dated record of the earlier design, and stays as recorded.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_rx.sv:314,395,540-545,627-631,641-696`; `milan_datapath.sv:5625-5626`; notify `[UNB]` U1-U4 on AAF 0 and CRF 1 (421/0); ruling items 1-4; the PR body's relation and pointer correction | R470-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| RTL | CLEAN | `KL_crf_rx.sv:354,393-395,445-465,536-616,627-631,641-696`; `milan_datapath.sv:2661,3172-3232,5596-5653,5745-5746`; Yosys OOC at dev and head; lint (5.050) | R470-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Robustness | CLEAN | crf_rx `[UNB-a..e]` and `[5t-g2b/g3/g3b]`; probes P0 and P2-P6 (crf unit) and P1 (AAF notify); notify U4 with the talker streaming | R470-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Tests | CLEAN | `sim_nxn.cpp` `[UNB]`; `unb_mutants.py`, 5/5 caught with the clean control; the P7 order-mutant leg output; crf_rx 16567/0; milan_dp_mclk 168/0; `measure_test_evidence.py --check` | R470-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Docs | CLEAN (RESIDUE F1, F2 carried) | CHANGELOG; MEDIA_CLOCK_FOLLOWING (every `KL_crf_rx` pointer, the lock-loss rule); REGISTER_MAP; TESTING; the milan_dp README; the datapath comment; the PR body; the em-dash, doc-path, doc-style and docs_check gates | R470-2 | `03895b63a3e8197353c2483593927b92efb73092` |

## Executed here

Every run is at the exact head unless marked otherwise, with the pinned "Verilator 5.050 2026-07-01 rev v5.050". `receipts/runs_summary.txt` lists each run with its rc.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp notify` | rc 0, 421/0; both trace lines equal the README and PR table | `receipts/J1_milan_dp_notify_head.log` |
| `unb_mutants.py 1`..`5`, the `make unb-mutants` inventory, run concurrently | rc 0 each: clean control PASS, mutant caught (4, 2, 2, 2, 2 of 421) | `receipts/J4_unb_mutant_{1..5}.log` |
| `make -C tb/verilator/crf_rx` | rc 0: 14287/0, 2201/0, 69/0, mutants 10/0 | `receipts/J3_crf_rx_suite_head.log` |
| `make -C tb/verilator/milan_dp_mclk` | rc 0: 55/0, 32/0, 50/0, 31/31 | `receipts/J5_milan_dp_mclk_head.log` |
| `syn/yosys/ooc.sh KL_crf_rx` (AX 1x1 TDM8), dev and head RTL | 433 -> 368 LUT, 544 -> 544 FF, 1 RAMB18 | `receipts/ooc_yosys_KL_crf_rx_{dev,head}.log` |
| `scripts/lint_rtl.py --check` (5.050) | PASS, 90 <= 90 | `receipts/lint_rtl_check.log` |
| em-dash (base `6c22d3ca`), doc paths, doc style, docs_check | rc 0 each, 0 findings | `receipts/docs_*.log` |
| `scripts/measure_test_evidence.py --check` | PASS | `receipts/measure_test_evidence_check.log` |
| Probe P1: AAF bind-fall unlock removed (copy) | 421/2: AAF U3 at the response and right after it | `probes/P1_*` |
| Probes P0 and P2-P6: crf_rx unit against the clean, dev and four planted arms (copy) | clean has 0 failures; all five planted arms caught by named checks | `probes/crf_unit/*`, `probes/crf_unit_probes.py` |
| Probe P7: the order mutant with its leg output kept | exactly the four U2 order checks fail | `probes/P7_*`, `probes/order_mutant_full_log.py` |
| Hosted check runs at the head (read-only) | the executed jobs had succeeded; Verilator shards 0/1/2/4, docs-check and elaborate were in progress; Physical gPTP was skipped, not executed | `receipts/hosted_checks_at_head.txt` |
| Clone integrity after the probes | HEAD, tree and index exact; the `ls-files -s` digest equals the baseline; 0 status entries including ignored; gitlinks unchanged; submodule worktrees clean | `receipts/clone_state_final.txt` |

## Real limits

- **Vivado not re-run.** The ruling does not require it, and no Vivado run was allowed beside the other builds. The Vivado OOC figures (373 -> 352 LUT, 544 FF) are taken as published. The Yosys delta was reproduced.
- **Not re-run, covered by the manager's source banks at this head:**
  - the default `milan_dp` sweep (11877 checks);
  - the pp_shadow, milan_dp_render, capture_coherence, aaf_clock_meter and milan_dp_gptp suites;
  - the gsi, crflic, gmstep, render-csr and tdm8render campaigns;
  - `syn/yosys/run.sh`, xvlog, behave and the builder bank.
- **Two known failures not re-checked this round:** `milan_dp_gptp` 139/3 and `tdm8render-mutants` 28/32. Both fail identically at dev.
- **No spec text.** No Milan or IEEE text was available locally. Clause readings rest on the quotations in the RTL headers, the issue and the ruling.
- **Simulation only.** Physical calibration was NOT RUN, and no bench capture was taken. Field skips are not hardware proof. #653's reported hardware order is unconfirmed either way.
- **Hosted CI was read only.** Several jobs were still in progress at read time.
- **Redaction.** The pinned simulator's install path is redacted to `<pinned-5.050-root>` in the published logs. `MANIFEST.sha256` hashes the redacted files.

## Pending manager duties

- Carry RESIDUE R470-2-F1 (the PR body's head references) and R470-2-F2 (the README `:661-663` registration step) to the residue checklist with their exact fixes.
- Hosted and act acceptance at the exact head. That includes the in-progress Verilator shards, `docs-check`, `elaborate`, and the exact-head `verilator-suites` and `yosys-portability` contexts.
- Candidate-merge validation against live dev at the merge turn, then post-merge containment.
- File Issues for the two dev failures (`milan_dp_gptp` 139/3; `tdm8render-mutants` 28/32), unless already filed.
- Bench lane B10 (#629 comment 5983013590): a capture of one disconnect at the DUT's port with a reversed-order control, and acceptance 4 (20 controller connects). #653 stays open for these.
- The external review at this head. Merge authorization stays with the maintainer.

R470-2 FINISHED
