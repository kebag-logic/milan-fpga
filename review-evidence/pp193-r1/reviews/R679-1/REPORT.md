[R679] NEGATIVE - exact head 6ddfcda4c3170b8f463c8623833f7541ca8c1faf

# R679-1: independent review of processor PR #198 (Closes #193)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #198, round R679-1.
- Exact head `6ddfcda4c3170b8f463c8623833f7541ca8c1faf`, tree `45faa5d3bd449cc0d8f8bee77f186d5e0c73022c`.
- Source base `21601694880efdfc4be3028afa3525fbc8f29c03`. The three author commits are `2b382b2`, `67b90c1` and `788425d`. The manager merge `6ddfcda` brings in processor main `08023123` (#192).
- The merge is exactly the clean merge. `git merge-tree --write-tree 788425d 0802312` gives tree `45faa5d3…`, which is the head tree. No conflict-resolution bytes are added.

The ordinary shared-stream behaviour is correct, byte-exact and well controlled: owner, quiet riders, both unbind orders, three sinks, rider rebind, the Ready + AskingFailed = ReadyFailed sum, mid-walk handover and consecutive-clock A8/A15 pairs. All 12 new controls and the 9 re-anchored #188 controls are KILLED.

The PR still leaves one path with two applicants for one StreamID:

- A sink alone on a StreamID re-binds away and parks its owed Leave (#188).
- Another sink then settles on that StreamID and declares it before the owed Leave is sent.
- One MRPDU then carries two Listener VectorAttributes for the value, New and Lv.
- The suite's own Milan v1.2 §4.2.7.2.2 peer Registrar model deregisters the stream while the new sink declares it.

That is finding F1 (MAJOR), so the verdict is NEGATIVE.

## Reconstruction

1. **Repository rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md` (conventions, single-source rules, citation rules).
2. **Issue #193.**
   - The frozen body and its "Done when" list.
   - The assignment (issuecomment-6289596705), the STOP (issuecomment-6289991979), the STOP ruling (issuecomment-6290012163) and the answers (issuecomment-6299223806), all in full.
   - The author's REVIEW READY report (issuecomment-6299186889) and the PR body.
3. **Authorities.**
   - `docs/architecture/10_srp_engine.md` §5.1 and §6.4.
   - The design banner of `hdl/srp/KL_srp_listener_fsm.sv`, its Table 10-3/10-4 transcription and the #188 park rules.
   - The `lstn_decl_state` consumers in `protocol_processor_top.sv` and `KL_srp_top.sv`.
   - Parent issue #746, for the comment rule.
   - The IEEE/Milan PDFs are not in the repository and were not re-read (see Limits).
4. **Diff and history.**
   - `git diff 21601694..6ddfcda`, split into the author delta (`0802312..6ddfcda`: one RTL file, docs 10, two suites, two campaign drivers and 21 patches) and the #192 content (already reviewed under PR #197).
   - The full head text of `KL_srp_listener_fsm.sv`, read line by line.
5. **Public executable evidence.**
   - `kebag-logic/milan-fpga@f4be7534:review-evidence/pp193-r1`: the OOC receipts (`author/receipts/round1b/ooc/{base,head}/ooc_pp_shadow.log`) and the tree listing.
   - Parent dev `e26f1816`: `hdl/milan/KL_pp_shadow.sv` and `syn/yosys/run.sh`, read for the measured shape.

## Findings

### F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs: a parked owed Leave and a new group's declaration of the same StreamID both transmit

**Where.**
- `hdl/srp/KL_srp_listener_fsm.sv:568`: `mbr_w = rec_valid_r && !lvp_r` puts every parked applicant outside every group.
- `:574`: `same_w` groups by the matcher stream_id only, never by the parked leave copy `lsid_r`.
- `:696`: `hand_w` merges only members that exist at the parking sink's own A15.
- `:640-641`: a new sink's request is held only by its own `lvp_r`.
- `:918-929`: both slots are pushed in the same walk.
- Claim text: the banner at `:84-106`, and `docs/architecture/10_srp_engine.md:616-650`, where §6.4 says the value has "one applicant" and "The value's single applicant lives in one of the sinks' … slots".

**Reproduction.** Ordinary control and receive faces only. No internal forcing, no RTL edit.
1. Sink P is alone on stream A, registered Ready, and its applicant is ticked to QA.
2. P re-binds to stream B, by a direct A15 or by A8 then A15. Its applicant goes LA, owes Lv for A and is parked (#188 rule).
3. Before the next tx!, sink J settles on A and the talker's next Advertise registers it. J reports Ready.
4. The next walk pushes both J's New for A and P's owed Lv for A.

**Evidence: interface level** (`receipts/probe-parked-leave-head.log`). All four variants fail: P above or below J, each with and without an A8 first.
- J below P: `0/2 5/2`, meaning New Ready then Lv Ready for one value in one tick.
- J above P: `5/2 0/2`.

**Evidence: wire level** (`receipts/probe-parked-leave-wire-head.log`). This runs through the real decoder, listener FSMs, encoder and slot pool, with the PR's own `PeerRegistrar` model fed every DUT MSRP frame. J = 0 and P = 1 give one 47-byte frame at 2403 ms:

```
01 80 c2 00 00 0e 0a 0b 0c 0d 0e 0f 22 ea 00 03 08 00 1a
00 01 11 22 33 44 55 66 00 01 00 80   <- FirstValue 1122334455660001, New, Ready
00 01 11 22 33 44 55 66 00 01 b4 80   <- same FirstValue, Lv, Ready
00 00 00 00
```

The peer Registrar ends that frame in MT (deregs 1, Lv 1) while sink 0 declares Ready. It re-registers only on the next frame, about 200 ms later. The reverse indices give `…b4 80 … 00 80`, which is a deregistration and re-registration inside one frame (deregs 1). Both cases fail the probe check `PW1`/`PW2`.

**Evidence: base comparison** (`receipts/probe-parked-leave-baseRTL.log`). With the base RTL and the head benches, the probe gives the same words. The parked case therefore predates these commits. This is not a regression; it is the part of #193's acceptance that the fix leaves open.

**Authority.**
- IEEE 802.1Q-2018 §10.7.7 (one Applicant per attribute value).
- The §35.2.6 NOTE (at most one Listener declaration per StreamID per port).
- §35.1.2.2 (Lv only for streams no longer wanted).
- Milan v1.2 §4.2.7.2.2 (the registrar deregisters at once on Lv).
- The frozen ruling (issuecomment-6290012163): "exactly one sink is the declaration owner … Only the owner's applicant transmits".
- The focus criteria: "exactly one VectorAttribute per value goes on the wire" and "a Milan 4.2.7.2.2 peer registrar never deregisters while a sink wants the stream".

**Impact.**
- A stream that one sink hands to another, for example a controller moving a stream between Stream Inputs, can lose its reservation at the peer. This is the symptom #193 reports.
- One MRPDU carries conflicting events for one attribute value.
- The window is from the re-bind to the next tx! (one T-MRP-JOIN), and needs a talker frame inside it. That is narrow, but it is reached by an ordinary ACMP sequence.

**Required outcome.**
- The value keeps one applicant across live and parked copies. When a sink settles on, or declares, a stream_id that another sink holds parked with an owed message, the parked applicant joins that stream's group. For example, the group takes the parked applicant over as the #188 same-stream re-probe rule does for one sink (LA + New! = VN), instead of letting a stale Lv go out beside the new declaration.
- The #188 obligations stay unchanged when no sink declares the old value.
- Committed SH/SW cases for both index orders and both re-bind forms, byte-exact single-value frames and an uninterrupted peer Registrar, each with a named KILLED control.
- Banner and §6.4 text that describe the parked case.
- Alternatively, a manager ruling that scopes this path out, with a tracking issue.

**Verification.** `scripts/run_probes.sh <clone> <candidate> <outdir>` must report, for every variant:
- no `FAIL: PR`/`FAIL: PW` lines;
- one value per tick;
- no Lv while the joiner declares;
- the peer IN with 0 deregistrations.

The existing SH1-SH9, SW1-SW3 and RB checks, and the 196-check campaign, must still pass.

### F2 — MINOR — Docs: the PR body's area figure does not state its measured sink count

**Where.** The PR #198 body, under Behaviour, in the sentence beginning "In the parent's out-of-context synthesis of `KL_pp_shadow` the election costs 1,037 LUTs…".

**Evidence.**
- The numbers are accurate. The public receipts `ooc/{base,head}/ooc_pp_shadow.log` give LUT 56,501 → 57,538 (+1,037) and FF 26,332 → 26,382 (+50). LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10 and CARRY4 2,392 are unchanged. The "about 1.8 %" is 1,037 / 56,501 = 1.84 %.
- The measured shape is not stated. The run is `synth_xilinx -family xc7 -flatten` over `KL_pp_shadow` with no parameter override in `syn/yosys/run.sh` at parent dev `e26f1816`, so it uses the module defaults `N_STREAM_IN_P = 8` and `N_STREAM_OUT_P = 8` (`hdl/milan/KL_pp_shadow.sv:195-196`).
- The manager's answer (issuecomment-6299223806, item 1) requires "the out-of-context figure with its sink count, and the 1x1 figure if one is measured".

**Impact.** A reader cannot tell the accepted 8-sink cost from the shipped 1x1 cost. This is measurement provenance, so it is MINOR rather than RESIDUE.

**Required outcome.** State the shape beside the figure, for example "(the module defaults, 8 Stream Inputs and 8 Stream Outputs)". Also say that no 1x1 figure was measured, and that the 4th pin adoption's route-1x1 measures the shipped cost.

**Verification.** Compare the edited PR body with the two OOC receipts and `KL_pp_shadow.sv:195-196`.

### S1 — SUGGESTION — Docs: the type-sum clause in two test comments

`tb/srp_stream_fsms/sim_main.cpp:1592` and `tb/srp_top/sim_main.cpp:3112` cite "§35.2.6, §35.2.2.8.7" for Ready + AskingFailed = ReadyFailed. Elsewhere this repository uses §35.2.2.8.7 for FailureInformation (`KL_srp_decoder.sv:96`, `KL_srp_talker_fsm.sv:36`). The type-sum authority used by the banner and by `10_srp_engine.md:631-632` is §35.1.2.2 with Table 35-14.

The two comments copy the frozen ruling's own citation (issuecomment-6290012163, item 3), so this is not counted against the author. Suggested fix: cite "§35.1.2.2, Table 35-14; §35.2.6" there, and let the manager decide whether to correct the ruling's citation.

### S2 — SUGGESTION — RTL (from reading the code; not probed): a handover to a lower index after the walk has passed it

`KL_srp_listener_fsm.sv:979` copies the giver's walk mark. Suppose the applicant moves by `op_mv_w` to an owner whose slot the current walk has already passed, and the giver has not been walked yet. Then the applicant gets no tx! in that walk, and its message goes one T-MRP-JOIN later.

This never causes two tx!, which is what the banner claims, and Table 10-3 allows it. A sentence in §6.4 noting the possible one-tick delay would complete the description.

## Prior public findings on this PR, resolved at this head

Before writing my verdict and ledger I had read no other review (`receipts/draft-verdict-before-prior-findings.txt`). The query afterwards (`receipts/prior-findings-audit.txt`) found two review-start notices, one concurrent public review (R680-1, issuecomment-6299632354, NEGATIVE), zero submitted reviews and zero inline comments.

| R680-1 finding | Resolution at 6ddfcda4 |
|---|---|
| F1 MAJOR, parked and live applicants for one value | **Retained.** It is the same defect as my F1, reached independently with my own probes and receipts. |
| F2 MINOR, area figure without its sink count | **Retained** as my F2, MINOR. My first draft had this as RESIDUE. I raised it because the manager's answer makes the sink count a condition of the accepted figure. |
| F3 RESIDUE, `SW.`/`SW3:` labels in new source comments | **Not retained.** Parent issue #746, which records the owner's 2026-10-15 rule, names the forbidden labels as bench lanes ("bench lane B17"), lane names, review rounds, reviewer IDs and issue-comment IDs. It also says that "identifiers such as `B10` to `B13` … are behaviour IDs, not bench lanes, and stay". `SW1-SW3` are the suite's check IDs: the campaign's named failing assertions in `tb/srp_top/mutants.py`. The `// ==== SW.` header follows the file's existing group headers (`A.` to `J.`, `DJ.` at `:2061-2951`). I scanned the author delta for lane, reviewer, round and comment-ID residue and found nothing. |
| F4 MINOR, §35.2.2.8.7 cited for the type sum | **Not retained at MINOR.** Recorded as S1 (SUGGESTION), because the comments reproduce the frozen ruling's own citation; see S1. |

## The focus checks

| Requirement | Result | Evidence |
|---|---|---|
| Several settled sinks on one StreamID give exactly one VectorAttribute per value, byte-exact | **Holds for settled sinks; fails when a parked Leave meets them (F1)** | srp_top `share` SW1 byte-exact against the independent builder, then three more frames with one value each (`receipts/suite-srp_top-head.log`, 8,665 PASS); probes for F1 |
| Owner is the lowest-index declaring sink; riders send nothing | Holds | `own_w`/`act_w`/`quiet_w` (`:600-603`); SH1, SH4; `listener-group-order-reversed` and `listener-rider-not-quiet` KILLED |
| Handover carries the state: no Lv!, no New! unless the sum changes; both orders, three sinks, rider rebind, mid-walk, consecutive-clock pairs | Holds | SH2, SH3, SH4, SH5, SH7, SH8, SH9 (`receipts/suite-srp_stream_fsms-head.log`, 1,403 PASS); seven controls KILLED (drops-state, teardown-applies-lv, withdraw-ignores-riders, forgets-walk-mark, settle-parks-shared-stream, rider-settle-hands-over, group-op-during-settle). An ACMP op and a decoder event cannot share a clock (`ctl_ready_o = !evt_valid_i`, `:626`). |
| Declared type is the sum (Ready + AskingFailed = ReadyFailed) | Holds | `cfp_w` OR of `dcl_r` (`:597`; codes 1/2/3); SH6 and SW3 byte-exact FourPacked 3; `listener-type-not-combined` KILLED in both suites |
| Last declarer keeps the #188 owed-Leave rules | **Holds for its own slot; the parked slot is not merged with later demand (F1)** | `op_lv_w` (`:610`); the settle arm still parks when `hand_w` is 0 (`:784-787`); RB1-RB9, WK and the Table 10-3 walks pass; the 9 re-anchored #188 controls are KILLED with unchanged edits (my diff of the edit lines: only the anchor context, plus the documented `listener-declaration-not-held` move to the grant term) |
| A Milan 4.2.7.2.2 peer registrar never deregisters while a sink wants the stream | **Holds in SW2; fails on the F1 path** | SW2 PASS; `receipts/probe-parked-leave-wire-head.log` deregs 1 |
| Registrar, EVT_TK_* and GET_RX_STATE stay per sink | Holds | The author delta does not touch `reg_plane`/`reg_ind`. `lstn_decl_state_o` is the sink's own `dcl_r` while its group declares (`:1178`); consumers: the top's status port and side-port snapshot only. SH6/SW3 check each sink's own type. |
| Every new check has a KILLED control; re-anchored #188 controls still KILLED | Holds | `receipts/campaign-head.log`: 196/196 PASS, coverage 113/113, 0 UNPROVEN; the changed gsi control `failure-change-redeclares` KILLED with golden and restored PASS (`receipts/gsi-head.log`, `gsi-head/results.json`) |
| No port, parameter or register-map change | Holds | `receipts/scope-ports.txt`: listener module header identical to main, top header identical to base; the author delta touches only `KL_srp_listener_fsm.sv` under `hdl/`; 07/02 unchanged |
| The area figure is recorded accurately | Numbers accurate; sink count missing (F2) | OOC receipts as quoted in F2 |
| Comment rule (no lane, round, reviewer or comment IDs in new source comments) | Holds | scan of the added lines of `21601694..6ddfcda`: no match |
| PR claims re-checked | Hold | base RTL with head benches fails exactly 26 SH checks (`probe-parked-leave-baseRTL.log`: 30 FAIL = 26 SH + 4 probe); suite tallies 1,403 and 8,665 equal the READMEs; lint, `gen_matrix --check` and `make check` rc 0 at head |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #193 body, assignment, STOP, ruling, answers; 802.1Q §10.7.7, §35.2.6 NOTE, §35.1.2.2, Table 35-14 and Milan §4.2.7.2.2 as cited by the ruling; wire frames from SW1/SW3 and from the F1 probe; peer Registrar outcomes | R679-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| RTL | UNCLEAN (F1) | the full head `KL_srp_listener_fsm.sv` (owner_map, app_arb, handover, settle_app, app_plane, walk, status_map); the merge-tree identity; the module headers of listener and top; the `lstn_decl_state` consumers; lint rc 0 | R679-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Robustness | UNCLEAN (F1) | both unbind orders, three sinks, rider rebind, mid-walk and consecutive-clock pairs (suite); four parked-Leave variants (interface level) and two (wire level), at head and at base RTL; same-clock grant/op/ctl interplay by code reading (S2) | R679-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Tests | UNCLEAN (F1: no case or control for a parked Leave meeting a new declarer of the value) | `srp_stream_fsms` 1,403 PASS; `srp_top` 8,665 PASS; the full srp_top campaign 196/196 with coverage 113/113; the gsi control; all 12 new and 9 re-anchored patches read | R679-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Docs | UNCLEAN (F1 claim text, F2) | banner, `10_srp_engine.md` §5.1/§6.4, `tb/srp_stream_fsms/README.md`, `tb/srp_top/README.md`, `tb/pp_top/README.md` (#193 paragraph), PR body, OOC receipts and the parent shape; `make check` rc 0 | R679-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |

## Receipts and how they were produced

All commands ran on disposable `git archive` exports or a scratch clone under `scratch/`, never in the review clone.

- **Simulator.** The scoped wrapper reports version 5.050 rev v5.050, which matches the CI pin `VERILATOR_VERSION: v5.050` in `.github/workflows/hdl.yml`.
- **Parallelism.** At most 14 jobs ran at once: the campaign with `--jobs 10`, two suites, the gsi run with `--jobs 3` and one probe.
- **Paths.** Local absolute paths in the logs are replaced by `<SIM_ROOT>`, `<PACKET>` and `<HOME>`.

| Receipt | What | rc |
|---|---|---|
| `receipts/suite-srp_stream_fsms-head.log` | `make` in tb/srp_stream_fsms (walk arms 1x1/2x2/3x5/9x9 and the suite) | 0, 1403 PASS |
| `receipts/suite-srp_top-head.log` | `make` in tb/srp_top (storage arms and every group) | 0, 8665 PASS |
| `receipts/campaign-head.log`, `receipts/campaign-head/` | `tb/srp_top/mutants.py --jobs 10` (full) | 0, 196/196, coverage 113/113 |
| `receipts/gsi-head.log`, `receipts/gsi-head/` | `tb/pp_top/gsi_mutants.py --only failure-change-redeclares --jobs 3` | 0, detected, golden and restored PASS |
| `receipts/lint_hdl-head.log`, `gen_matrix-head.log`, `make_check-head.log` | `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` (scratch clone at the head) | 0, 0, 0 |
| `receipts/probe-parked-leave-head.log` | `scripts/probe_parked_leave.py` then `make RUN_ARGS=suite` | 2 (expected: 4 PR failures, 1403 suite checks PASS) |
| `receipts/probe-parked-leave-wire-head.log` | `scripts/probe_parked_leave_wire.py` then `make RUN_ARGS=share` | 2 (expected: PW1, PW2 fail; SW1-SW3 PASS) |
| `receipts/probe-parked-leave-baseRTL.log` | the same FSM probe with base `hdl/` and head `tb/` | 2 (26 SH + 4 PR failures) |
| `receipts/scope-ports.txt` | module-header and scope comparison | n/a |
| `receipts/source-integrity.txt` | `scripts/verify_clone.py` on the review clone | 0 |
| `receipts/hosted-checks.txt` | exact-head check runs at 19:46Z | n/a |
| `receipts/draft-verdict-before-prior-findings.txt`, `receipts/prior-findings-audit.txt` | order of the independent verdict and the prior-findings read | n/a |

`scripts/run_probes.sh <clone> <revision> <outdir>` re-runs both probes on any candidate.

## Limits and pending manager duties

- **Not run.** No full processor, parent, gPTP, Yosys or builder bank. No pp_top suite. Only the one changed gsi control of the gsi campaign. No acmp, notify, aecp, d3 or elab campaigns. No parent consumer gates. No synthesis.
  - For those I rely on the author's published receipts, with their recorded revisions, and claim no manager source bank.
  - No manager source bank exists at this exact head.
  - The source base `21601694` and the live dev `78ca9bdf104819265588726bce4322696c38b8c2` of the final candidate are different contexts.
- **Physical calibration NOT RUN.** No hardware. Field skips are not hardware proof.
- **Hosted CI at 19:46Z.**
  - Executed: `docs-gates` and `portability` completed successfully in both workflow runs.
  - Still running: `suites` in both runs, so not counted.
  - The manager owns hosted/act acceptance.
- **Standards.** The IEEE 802.1Q-2018 and Milan v1.2 texts are not in the repository. Clause and table numbers are checked against the frozen ruling and the repository's own usage, not re-read from the standards.
- **S2** comes from reading the code and was not probed.
- **Manager duties.**
  - Obtain a fix for F1 and F2, then an independent re-review.
  - Validate the current-dev merge candidate with the builder and native banks at the merge turn, and link those receipts on the PR.
  - Check the shipped cost against the resource gate with the route-1x1 measurement at the 4th pin adoption.
- **Clone integrity.** The review clone was never modified. The exact HEAD and tree, a clean status (ignored files included), index equal to HEAD, and the bytes and executable bits of all 692 tracked files were all verified. The tree has zero gitlinks, so there are no submodule pins to restore.

R679-1 FINISHED
