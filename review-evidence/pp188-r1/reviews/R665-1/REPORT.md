[R665] NEGATIVE - exact head cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48

# R665-1: independent internal review of processor PR #195 (Closes #188, #189)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #195, branch `188-189-listener`.
- Exact head `cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48`, tree `a19fe4d05c3bfcab317780fe8e57f07f77c23469`. Verified in the isolated clone and in the scratch extraction used for every run.
- Reviewed delta: `git diff b48312e1..cb8bab04` (28 files, +679/-52). It holds the author commits `9c8859a` (#188) and `dc01aec` (#189) on main `5addf297`, and the manager merge `cb8bab0` of main `b48312e1` (#184 Domain re-join, #190 per-source TSpec).
- Round 1. PR #195 had no public review findings before this pass; it carries only the two review-start notices. There is nothing to resolve or retain.

## Verdict

NEGATIVE: two MINOR findings are open (F1, F2). One RESIDUE (F3) and one SUGGESTION (S1) are recorded.

What holds:
- The #188 and #189 changes do what the issues require in every case this reviewer drove.
- The merge is a correct union of both sides.
- Every gate and campaign this reviewer ran at the exact head passes.

What keeps it negative:
- **F1:** the new #188 settle logic has documented arms that no check reaches. Four non-equivalent reviewer mutants survive. One of them brings back the #188 symptom on a double rebind.
- **F2:** the frozen #189 acceptance ("on every change") is not met when the event router coalesces two type changes. The PR body states this, but the design documents do not, and no scope decision covers it.

## Reconstruction

- **Conventions.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` (checked with `git ls-files`). `docs/README.md` served as the author conventions: ID registries, single-source rules, and what `make check` enforces.
- **Frozen scope.**
  - The issue #188 and #189 bodies.
  - The assignment comment 6256482476 on #188, read in full. It adds:
    - keep Milan v1.2 4.2.7.2.2 intact;
    - update the banner at `KL_srp_listener_fsm.sv:67-71`;
    - for #189, the in-place swap in both directions, with no state transition added;
    - a suite case and a planted mutant for each;
    - processor gates and parent consumer gates;
    - STOP on any register-map, top-level port or parameter change.
  - No other maintainer or manager scope decision exists on #188, #189 or #195.
- **Authorities.** Each authority the delta cites was checked against the repository's own records:
  - IEEE 802.1Q-2018 10.7.7 and Table 10-3, against the module's own transcription (`app_next_f`, `app_msg_f`; the PR does not change either);
  - 802.1Q 35.2.6;
  - Milan v1.2 Tables 5.30 and 5.39;
  - Milan 4.2.7.2.2 (Δ13, `01_overview.md:148`);
  - Milan 5.5.3.5.43, .45 and .48 (F05.3 and F05.5 in `05_acmp_engine.md`).
- **Limit on authorities.** The 802.1Q and Milan texts themselves were not available to this reviewer. Clause and note numbers, in particular "Table 10-3 note 11", were checked for consistency with the repository's existing citations, not against the published standards.
- **Public evidence.**
  - Source: `kebag-logic/milan-fpga@5baa360e:review-evidence/pp188-r1`.
  - Fetched sparse into a scratch directory, used as data only, never executed.
  - Contents read: the author handoff, the PR body, and 499 receipts. All rc files were scanned.
  - The manager has posted no evidence comment on #188, #189 or #195 beyond the assignment and the review-start notices.

## Findings

### F1 - MINOR - Tests, Robustness - documented #188 settle arms reached by no check

**Where.**
- Untested logic in `hdl/srp/KL_srp_listener_fsm.sv`:
  - `:607`: LO counted as owing;
  - `:581-582`, `:592-593`: `csid_w`, the stream_id a parked applicant holds, which a settle while parked uses;
  - `:722-723`: a txLA! walk keeps the park ("txLA! keeps LO");
  - `:420`: received Listener values are not applied to a parked sink.
- Where these arms are documented:
  - the banner at `:67-82`;
  - `docs/architecture/10_srp_engine.md:585-603` (§6.4 "A settle while a Leave is still owed", rows "LA or LO");
  - the author handoff's settle table ("the rebind, or a third stream while one is parked"; "A rebind back to the parked stream_id is 'same'").
- What the existing checks drive: `tb/srp_stream_fsms/sim_main.cpp:1072-1150` (section M, RB1-RB3) and `walk_main.cpp` WK11. They cover only an LA applicant, one settle per park, and tx! walks.

**Evidence.** Receipts are `receipts/exec/probes.log` and `receipts/exec/rv-probes.log`. Scripts are `scripts/probes.py`, `scripts/rv_probes.py` and `scripts/rv_section.cpp`.
- Four reviewer edits survive the full `tb/srp_stream_fsms` `make` at the head. That run covers the walk arms at 1/1, 2/2, 3/5 and 9/9 (38/50/74/134 checks), then the suite (1352/1352 PASS). The survivors:
  - U1: LO not owed;
  - U2: the park retired on a txLA! walk;
  - U3: the parked rx mask removed;
  - U5: `csid_w` ignores the park.
- A reviewer-only section, RV1-RV5, was inserted into a scratch copy of the suite. It passes at the head (1358/1358), which confirms the head behaves as documented. Under each survivor it fails:

| Survivor | RV checks failed | Observed effect |
|---|---|---|
| U5 | RV1, RV2 | A second rebind before tx! sends a Lv for the middle, never-declared stream and drops the held stream's Lv. This is the #188 symptom on two rebinds within one T-MRP-JOIN. A rebind back to the parked stream sends a spurious Lv. |
| U1 | RV3, RV5 | An LO applicant's Empty for the old stream is never sent. |
| U2 | RV4 | After a txLA! walk, the Empty is sent for the new stream instead of the held one. |
| U3 | RV5 | An rMt on the new stream moves the parked LO applicant to VO, and the owed Empty is lost. |

- U6 (the retire keeps FourPacked) and U7 (`set_same_w` without `rec_valid_r`) survive both the suite and RV. They are recorded as likely equivalent.
- Harness controls:
  - both goldens PASS;
  - U4 (owed FourPacked cleared) is KILLED by WK11;
  - U9 (the author's `rf_swap_unlatched` edit) is KILLED by B4.

**Impact.** A regression in these arms would land with every processor gate and both campaigns green. U5 in particular re-opens #188 for a controller that rebinds twice in quick succession.

**Required outcome.** Add suite checks for these arms, each with a planted control in `tb/srp_top/mutants.py`:
- a settle while parked onto a third stream;
- a rebind back to the parked stream;
- an LO applicant settled onto another stream;
- a txLA! walk while parked;
- received Listener values while parked (an LO case: LA ignores every received event).

Then:
- add the new group to the campaign's assertion-coverage set;
- update the suite READMEs and tallies.

RV1-RV5 and U1/U2/U3/U5 are a ready template. Alternatively, remove any arm that is not intended and correct its documentation.

**Verification.** At the new head:
- `tb/srp_stream_fsms` passes;
- the srp_top campaign is rc 0 with the new arms KILLED;
- `scripts/probes.py <tree> <out> --only U1-lo-not-owed U2-park-retires-on-txla U3-parked-applies-rx U5-csid-ignores-park` reports every arm KILLED.

### F2 - MINOR - Conformance, Robustness, Docs - REGISTERING_FAILED misses a coalesced second type change

**Where.**
- `hdl/acmp/KL_pp_acmp_listener.sv:1169-1171`: the SOK bookkeeping takes the type from the event's payload bit.
- `hdl/top/protocol_processor_top.sv:3249-3250`: the payload is the registered type at strobe time.
- `hdl/packet_engine/KL_pp_event_router.sv:15-34`: "one sticky latch holds the event WITH ITS FIRST payload until the consumer acks it". A re-fire before the ack coalesces into that event, and its later payload is discarded.
- `docs/architecture/05_acmp_engine.md:314-320` claims, without condition, that REGISTERING_FAILED "follows the swap in both directions".

**Authority.**
- The frozen #189 Done-when (issue body and assignment): "GET_RX_STATE's REGISTERING_FAILED follows the registered declaration type on every change, including the in-place swap in both directions".
- Milan v1.2 Table 5.39: "1 if registering a Talker Failed attribute".

**Evidence.**
- Code reading of the three blocks above.
- The PR body records the gap itself: "A residual, not changed here: the event router keeps the first payload of a source that strobes again before the listener takes it".
- No maintainer or manager scope decision narrows the acceptance.
- The window is wider than "a few clocks". It lasts until the listener acknowledges the first TK_ATTR_REGISTERED:
  - the listener takes router events only in `X_IDLE`, behind transactions and timer work (`KL_pp_acmp_listener.sv:951-1047`);
  - `05_acmp_engine.md:189-191` adds that while a talker event is held, "a source strobing again coalesces".

**Impact.**
- Two type changes of one sink's registration, before the listener takes the first, leave GET_RX_STATE reporting the intermediate type.
- This persists until the next type change, because refreshes of the same type raise no new event.
- Meanwhile GET_STREAM_INFO and the Listener declaration follow the last type.
- It is the same observable inconsistency #189 reports, in a narrower corner.

**Required outcome.** One of:
- **(a) Close it.** For example, take the type from the SRP listener's registered-type level (`tk_reg_state_o`) at classification time, or re-read it when the event is presented with `evt_lost`. Add a case that coalesces two swaps, with a planted control. A top-level port change would be a STOP condition under the assignment.
- **(b) Accept it explicitly.** Obtain a manager or owner scope decision accepting it as a tracked residual, with a tracking issue. Record the limitation in `05_acmp_engine.md` §6.3 beside the cell note, and in the PR body.

**Verification.**
- For (a): the new case passes at the head and its control is KILLED.
- For (b): the scope-decision link, and the doc sentence at the new head.

### F3 - RESIDUE - Docs (prose only) - the "same stream" row describes only the LA case

**Where.**
- `docs/architecture/10_srp_engine.md:596`: "keeps the applicant: the next tx! sends the Lv, unless the talker registers again first, when New! takes LA to VN and the tx! sends New".
- The banner at `hdl/srp/KL_srp_listener_fsm.sv:69-72`: "(LA + New! is VN, so a re-probe that re-registers before tx! sends New, and one that does not sends the Lv)".
- The first row of the PR body's settle table, which uses the same words.

**Defect.** The row covers an LO applicant too (its own header says "an Empty owed"). For LO, the tx! sends the Empty (`app_msg_f` LO: `s`), and New! takes LO to VN. The code is correct; only the sentence is narrower than the row.

**Exact fix.**
- 10 §6.4 row: "keeps the applicant: the next tx! sends what it owes (the Lv from LA, the Empty from LO), unless the talker registers again first, when New! takes LA or LO to VN and the tx! sends New".
- Banner: "(LA or LO + New! is VN, so a re-probe that re-registers before tx! sends New, and one that does not sends the owed Lv or Empty)".
- PR body row: the same wording.

### S1 - SUGGESTION - Docs - one row of the pp_top ACMP-controls table mixes measurement dates

- **Where:** `tb/pp_top/README.md:2082`, the `st_ls_teardown_as_declare` row, now records "1 of 48", measured at this change.
- **Why it is inconsistent:** the table's lead-in still dates every row's count to the 2026-10-04 #639 re-run, on a "1 of 43" basis. The twelve other arms that now also fail the new checks keep their 2026-10-04 counts.
- **The new figure is right:** this reviewer's campaign shows `ACMP: 48 checks, 1 failures` for that arm.
- **Suggestion:** re-record the column at the head with a dated line, or date that one cell. The four new #188/#189 controls could also get the "Failing checks" column.

## Lenses

### Conformance - UNCLEAN (F2)

**#188.**
- The settle now applies Lv!, then does one of three things:
  - keeps the applicant (same stream);
  - parks the old stream_id until its owed message goes out at the next tx!;
  - starts VO.
- This matches 802.1Q-2018 10.7.7 (one applicant per value) and Table 10-3 (LA sends sL at tx!; LA + New! = VN).
- Driven at the head:
  - RB1, RB2, RB3 and WK11 (the author's checks, re-run);
  - RV1-RV5 (reviewer, scratch);
  - AS7, end to end: the MRPDU after a rebind carries the old stream's Lv and nothing for the new one, and the next MRPDU carries New Ready.
- The registrar plane (`KL_srp_listener_fsm.sv:784-874`, Δ13 / Milan 4.2.7.2.2) is untouched by the diff.
- Accepted deviation, latency only: compared with strict per-value semantics, the new value's New waits one T-MRP-JOIN, and its received values are not applied while parked. The banner and 10 §6.4 document this.

**#189.**
- In SETTLED_RSV_OK, TK_REG updates `f_srp_decl[1]` in both directions.
- `rf_w` stays gated to SOK (`:652`).
- The transition ROM and its generator are not in the diff, so no state transition is added.
- B4/B4b and AS5b/AS5c pass at the head. GET_RX_STATE is byte-exact: 0x0042 after the swap to Failed, 0x0002 after the swap back.

**Open:** F2. The frozen "every change" clause is not met under coalescing.

### RTL - CLEAN

- **Examined:** `KL_srp_listener_fsm.sv` (whole module); `KL_pp_acmp_listener.sv:1149-1187` and `:640-700`.
- **Arbitration and same-cycle writes:**
  - `ctl_acc_w` implies no decoder event (`ctl_ready_o = !evt_valid_i`), so a settle never meets an rx hit.
  - Settle, declaration grant and walk grant are mutually exclusive per sink in `app_arb`. The writes to `lvp_r`, `app_r` and `fourpack_r` therefore never collide on one index.
- **Park consistency:** while parked, the applicant can only stay LA or LO until a tx!:
  - the rx mask is in place;
  - Lv!, rLA! and periodic! leave LA and LO unchanged;
  - the declaration grant is masked.
  `lvp_r` therefore always agrees with the applicant state.
- **Leave copy:**
  - written only under `lv_take_w`, read only under `lvp_r`;
  - its distributed-RAM arm has one write port, a read at the write address (`csid_w`), and a read at `wsrc_r`. That is the shape of a dual-port LUTRAM.
- **Lint:**
  - `scripts/lint_hdl.sh` rc 0 (41 modules), pinned Verilator 5.050;
  - per-shape `--lint-only -Wall` of `KL_srp_listener_fsm` at N_SINKS_P = 1, 2, 3, 5, 9: rc 0, no warnings (`receipts/exec/lint-listener-shapes.log`).
- **Ports, parameters, register map:** no change. The `hdl/` diff has no port or parameter lines.
- **Comment rule:**
  - Every new source comment states behaviour and reason with issue and requirement IDs.
  - None of the added lines in `hdl/` or `tb/` sources carries a lane label, lane name, review round, reviewer ID or comment ID.
  - The one `R458-3` in an added line is a pre-existing provenance cell in `tb/srp_top/README.md:750`. The PR edited that README row for WK11; it is an existing instance, tracked by #746.

### Robustness - UNCLEAN (F1, F2)

- Nothing back-pressures ACMP (`ctl_ready_o` unchanged).
- A third settle, or a teardown while parked, keeps the owed message.
- RV1, RV2, RV4 and RV5 confirm the head handles:
  - a settle while parked;
  - a rebind back to the parked stream;
  - a txLA! walk while parked;
  - received values while parked.
- **Open:**
  - F1: no committed check guards these paths;
  - F2: the coalesced double type change.

### Tests - UNCLEAN (F1)

Every new check has a planted control. Each was KILLED by its named check at the exact head:
- **srp_top campaign:**
  - RB1: `listener-rebind-abandons-leave`, `listener-declaration-not-held`, `listener-park-never-retires`;
  - RB2: `listener-reprobe-abandons-leave`;
  - RB3: `listener-reprobe-parks-own-stream`;
  - WK11: `walk-ignores-leave-copy`, `lsid-ram-read-sink-0`, `lsid-flops-read-sink-0`, `lsid-ram-written-with-new-stream`, `wsid-write-ignores-ready`.
- **ACMP campaign:**
  - AS7: `rebind_abandons_leave`, `park_never_retires`;
  - B4/B4b in `tb/acmp_listener` and AS5b/AS5c in `tb/pp_top`: `rf_swap_unlatched`, `rf_swap_sticky`;
  - AS6 (VLAN release): the regraded `st_ls_teardown_as_declare`, and `st_ls_teardown_lost`.

The rebind and the re-probe are each covered (rebind: RB1, AS7; re-probe: RB2, RB3). The "Each new check has a planted mutant" clause is met.

**Open:** F1, documented arms that no check reaches.

### Docs - UNCLEAN (F2)

- **Examined:**
  - the banner `:67-82`, which replaces the old trade-off at `:67-71` as assigned;
  - `10_srp_engine.md` §5.1: the storage-table row and the cost-table note (the note states that the listener figures were "not measured again");
  - `10_srp_engine.md` §6.4: the owed-Leave subsection;
  - `05_acmp_engine.md` §6.3: the cell note;
  - the `tb/srp_stream_fsms`, `tb/srp_top`, `tb/acmp_listener` and `tb/pp_top` READMEs.
- **Tallies matching this reviewer's head runs:**
  - srp_stream_fsms: 1352 checks; walk arms 38/50/74/134;
  - acmp_listener: 3170;
  - pp_top ACMP phase: 48 checks, "about 23 s" (measured 22,621 ms);
  - `st_ls_teardown_as_declare`: "1 of 48".
- **Open:** F2 (the §6.3 note claims an unconditional follow). F3 is RESIDUE; S1 is a SUGGESTION.

## Merge verification (manager merge cb8bab0 of main b48312e1)

**Conflicts.** `git merge-tree --write-tree dc01aec b48312e1` conflicts in exactly two files, `tb/pp_top/acmp_mutants.py` and `tb/srp_top/mutants.py`. Its tree differs from the published merge tree only in those two files (`receipts/merge-replay.log`).

**Union check.** `scripts/check_mutant_union.py` imports both lists at each revision (`receipts/mutant-union.log`, rc 0).

`acmp_mutants.py`:
- 60 arms in the merge; 57 and 54 in the parents; 51 in the merge base.
- Every arm of either parent is present unchanged, except one handled correctly:
  - `st_ls_teardown_as_declare@tb/pp_top`: main keeps the base version, and the author side regrades it to AS6's VLAN check;
  - the merge carries the regrade, which is the correct one-sided resolution.
- No arm is new to the merge.
- Every planted edit's old text occurs exactly once in the merged sources (60 anchors).

`srp_top/mutants.py`:
- 150 arms in the merge; 129 and 141 in the parents.
- Every arm of both parents is present.
- Every arm's patch file passes `git apply --check` on the merged tree (150 of 150).
- The coverage set is the union (WK 11, RB 3, DJ 4).

**Executed at the merge head.**
- ACMP campaign: 60/60 KILLED, 7 goldens PASS, rc 0. This includes the #190 TSpec arms.
- srp_top campaign: rc 0, 168 checks (17 controls, 150 arms KILLED, assertion coverage 94/94 including DJ1-DJ4 from #184).

## Receipt index

`scripts/check_receipt_index.py` (`receipts/receipt-index-check.log`, rc 0):
- The author's `receipts/INDEX.md` has 499 rows, one for each of the 499 files besides itself.
- For every unredacted file, bytes and sha256 prefix match, and the first line matches the index's rendering.
- The two path-redacted files match through `MANIFEST.json`'s `original_sha256`.
- The publication `MANIFEST.json` lists all 500 files, and every `published_sha256` matches.

## Execution evidence at the exact head (reviewer-run; focused, not a bank)

- Every run used a scratch extraction of the exact head tree (`a19fe4d0`).
- Verilator 5.050, wrapper sha256 `905795b9...e92f` (`receipts/tool-identity.txt`). The host's 5.052 was not used.
- Each command's own exit status was written to an rc file, never through a pipe.

| Run | Result | Receipt |
|---|---|---|
| `tb/srp_stream_fsms` `make` (walk arms + suite) | rc 0; walk 38/50/74/134; suite 1352/1352 | `exec/suite-srp_stream_fsms.*` |
| `tb/acmp_listener` `make run` | rc 0; 3170/3170 | `exec/suite-acmp_listener.*` |
| `tb/pp_top` `make run` (full default run, 7 builds) | rc 0; 10533/10533 | `exec/suite-pp_top.*` |
| `tb/srp_top` `make run` | rc 0; 8660/8660 | `exec/suite-srp_top.*` |
| `tb/srp_encoder`, `tb/srp_decoder`, `tb/event_router` | rc 0; 593, 190 and 81 checks | `exec/suite-*.*` |
| `scripts/lint_hdl.sh` | rc 0 (41 modules) | `exec/lint_hdl.*` |
| listener lint at N_SINKS_P = 1/2/3/5/9 | rc 0 each, no warnings | `exec/lint-listener-shapes.log` |
| `tb/pp_top/acmp_mutants.py --jobs 3` | rc 0; 60/60 KILLED, goldens PASS | `exec/acmp-campaign.*` |
| `tb/srp_top/mutants.py --jobs 6` | rc 0; 168/168, coverage 94/94 | `exec/srp_top-campaign.*` |
| reviewer probes `scripts/probes.py --jobs 4` | rc 0; goldens pass; U4, U9 KILLED; U1, U2, U3, U5, U6, U7, U8 survive | `exec/probes.*` |
| reviewer RV section `scripts/rv_probes.py --jobs 4` | rc 0; head 1358/1358; U1, U2, U3, U5 fail RV checks; U6, U7 pass | `exec/rv-probes.*` |

**Hosted CI at the exact head** (read-only; `receipts/hosted-checks-cb8bab04.txt`, fetched 2026-10-19T09:32Z):
- `portability` and `docs-gates` completed with success on both the push and the pull_request runs;
- `suites` was still in progress on both.

The manager owns hosted and act acceptance; nothing here claims it.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #188/#189 bodies, assignment 6256482476; `KL_srp_listener_fsm.sv` settle/walk/registrar planes; `KL_pp_acmp_listener.sv` X_ROM; event router; F05.3/F05.5/F05.14; RB1-3, WK11, AS5b/c, AS7, B4/B4b, RV1-5 at head | R665-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| RTL | CLEAN | both changed modules in full context; arbitration and same-cycle write analysis; lint_hdl rc 0; per-shape lint N = 1/2/3/5/9; no port, parameter or register-map change; comment rule on all 670 added lines | R665-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Robustness | UNCLEAN (F1, F2) | park, re-settle, teardown-while-parked, txLA!-while-parked and rx-while-parked paths (RV1-5); router coalescing window | R665-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Tests | UNCLEAN (F1) | new checks and their controls in both campaigns (60/60, 150/150 KILLED at head); merged mutant union and anchors; reviewer probes U1-U9 and RV1-5 | R665-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Docs | UNCLEAN (F2) | banner; 10 §5.1 and §6.4; 05 §6.3; four suite READMEs and their tallies; PR body; receipt index vs files (499/499) and publication manifest (500/500) | R665-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |

## Real limits

- **No author or manager execution at this exact head.** The author's published gate, campaign and consumer receipts are at `dc01aec4`, before the merge. For the merged head `cb8bab04`, the only executions are this reviewer's focused runs above. No author or manager source bank exists at this exact head, and none is claimed or inferred.
- **Not run by this reviewer** (out of scope or not allowed):
  - `scripts/run_suites.sh`;
  - the other processor campaigns: srp_admission, maap, adp, aecp, aecp-dispatch, ctr, gsi, name_wr, notify, name_state, elab_guards, d3;
  - `make check` and Yosys;
  - every parent consumer gate.

  For these, the evidence is the author's at `dc01aec4`. All are rc 0 except two expected cases: the `check_submodule_docs` pin mismatch, and the in-pass `ooc_selftest` setup refusal, which was rerun with rc 0 in `consumers/ooc-*`. Hosted `docs-gates` passed at the exact head.
- **No implementation measurement.**
  - No Vivado synthesis, timing or resource measurement of the leave copy or its 64-bit comparator. The only area figure is the author's Yosys OOC pricing at `dc01aec4`.
  - Physical calibration NOT RUN. No hardware; field skips are not hardware proof.
- **Standards and F2 window.** The standards' texts were not available (see Reconstruction). F2's window comes from code reading, not from a simulated coalescing case.
- **Probe equivalence.** The reviewer probes are disposable scratch edits. U6, U7 and U8 are recorded as likely equivalent, not proven equivalent.

## Pending manager duties

- Route F1 and F2 to the author. If F2's residual is to be accepted rather than closed, it needs a scope decision.
- Carry F3 to the residue checklist.
- At the merge turn, build and validate the current-dev candidate with the builder and native banks, and link those receipts on the PR:
  - source base `b48312e1`;
  - live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`;
  - the processor-side full bank has not run at `cb8bab04`.
- Hosted and act acceptance at the final head. `suites` was still in progress when this report was written.
- Parent adoption of the new gitlink (`check_submodule_docs` pin and diagram), as for any moved pin.
- Merge still requires two independent positive reviews and the full completion bar.

## Packet

Published files are listed in `MANIFEST.sha256`:
- **`scripts/`:** portable. Each script resolves the packet root from its own location and expects the pinned Verilator at `scratch/bin/verilator`.
- **`receipts/`:** host paths are replaced by `<packet>`, `<clone>`, `<tools>`, `<home>` and `<container-layer>`.

Scratch trees under `scratch/` are not published.

**Clone integrity.** After all work, the isolated clone was verified byte-identical to the head (`receipts/clone-integrity.txt`):
- HEAD and tree as above;
- empty status, including untracked and ignored files;
- index equal to HEAD in mode, blob and path for all 657 entries;
- every working-tree blob hash and executable bit equal to the index;
- no gitlinks or `.gitmodules` in this repository, so there were no submodule pins to restore.

R665-1 FINISHED
