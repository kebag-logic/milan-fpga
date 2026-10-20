[R665] POSITIVE - exact head 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e

# R665-2: independent internal review of processor PR #195 (Closes #188, #189), round 2

Exact head `7f56fc4d7f5102cac6dacb9c00f372d20d3b379e`, tree `34af6de87215cc90a774757debc8af90073aaa87`.
The head is the manager merge of processor main `24c7f853` (#185/#186) into the author head `cca12e3c`.
Previously reviewed head: `cb8bab04`. Reviewed delta:
- six author commits `114f16a`, `51df2b6`, `66785d2`, `0f9a4f2`, `518b365`, `cca12e3` on `cb8bab04`;
- the merge `7f56fc4` (parents `cca12e3c`, `24c7f853`).

## Verdict

POSITIVE. Every named prior finding is resolved at its cause:
- R666-001 and R665-1-F2 (the coalesced REGISTERING_FAILED);
- R665-1-F1 (the settle arms with no checks);
- R665-1-F3 and R666-002 (wording).

The merge is the conflict-free automatic merge, and it composes additively. No top-level port, parameter or register-map change.

Two new wording-only items are recorded as RESIDUE, with their exact fixes. R665-1-S1, which was not assigned, stays a SUGGESTION. One new SUGGESTION is added. None of these leaves a lens unclean.

## Reconstruction

- **Repository guides.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`. I followed `docs/README.md`: the conventions, the single-source rules, and the source-comment rule as the owner set it.
- **Frozen scope:**
  - #188 body: the Leave of the old Listener declaration goes out at the next tx! even after a re-settle. Rebind and re-probe each have a check and a planted mutant. Authority: IEEE 802.1Q-2018 10.7.7 and Table 10-3, and Milan v1.2 5.5.3.5.
  - #189 body: GET_RX_STATE REGISTERING_FAILED follows the registered type on every change, both swap directions, with no transition added. Authority: Milan v1.2 5.5.3.5.44 Table 5.39, Table 5.23, and 802.1Q-2018 35.2.6.
  - Assignment on #188: keep Milan v1.2 4.2.7.2.2, and STOP on any port, parameter or register-map change.
- **Round-2 assignment (PR issuecomment-6264243047):**
  1. Item 1, option (a) for R666-001 and R665-1-F2. It needs both coalesced directions with the listener held busy, a planted control, no new transition, the 05 §6.3 correction, and the removal of the "residual" sentence.
  2. Item 2, R665-1-F1. It needs five settle arms, each with a KILLED control, the coverage set, and the READMEs. U6 and U7 are accepted as likely equivalent.
  3. Item 3, R665-1-F3 and R666-002, applied as written.
  4. Item 4: S1 is not assigned.
- **Interface authorities read at the head:**
  - the router contract: `docs/architecture/02_interfaces.md` §5 and `hdl/packet_engine/KL_pp_event_router.sv:14-34, 80, 166-172` (FIRST payload; a re-fire coalesces);
  - F05.3 / Table 5.30 cell `EVT_TK_REGISTERED` × SOK (`docs/architecture/05_acmp_engine.md:313-326`);
  - the SRP listener status map (`hdl/srp/KL_srp_listener_fsm.sv:950-957`, `tk_reg_state_o`).
- **Order of work.** I made my own pass over the delta first. Only then did I read the R666-1 and R665-1 findings (PR issuecomment-6263408703 and issuecomment-6264221765), to resolve them below.

## Findings (new at this head)

### R665-2-R1 - RESIDUE - Tests, Docs - a new source comment names a check label

- **Where:** `tb/srp_top/mutants.py:184`, added by `518b365`: `# WK12's own counts and its precondition, at every shape`.
- **Authority:** the owner's comment rule of 2026-10-15. Source comments must not show bench labels, and a new instance in the reviewed delta is RESIDUE. The round-2 assignment also removed the same kind of label from this file: `(walk_main.cpp WK11)`, R666-002.
- **Impact:** wording only. The selector strings in the tuples below the comment are executable and stay as they are.
- **Exact fix:** `# the leave-copy walk check's own counts and its precondition, at every shape`.
- **Verification:** `grep -nE '^\s*#.*\bWK[0-9]+' tb/srp_top/mutants.py` prints nothing.

### R665-2-R2 - RESIDUE - Docs - 05 §5 says a coalesced event "carries" the registered type

- **Where:** `docs/architecture/05_acmp_engine.md:191-192`, added by `114f16a`: "A coalesced `EVT_TK_REGISTERED` still carries the type registered when it is taken (§6.3)."
- **Defect:** the event's payload carries the type of the FIRST strobe. That is the 02 §5 router contract, and §6.3 says so. The listener's Failed input is the SRP listener's level, read when the event is taken (`hdl/top/protocol_processor_top.sv:3300-3313`). The sentence reads as though the payload changed. The code and §6.3 are right.
- **Impact:** wording only. No figure, check or behaviour depends on it.
- **Exact fix:** "A coalesced `EVT_TK_REGISTERED` is still taken with the type the sink registers at that moment: the top reads it from the SRP listener's level, not from the event's first payload (§6.3)."
- **Verification:** the sentence at the new head.

### R665-2-S2 - SUGGESTION - Docs (PR text) - the PR body's records and one table row

- **Head composition.** The PR body records "Base cb8bab04 ... and head cca12e3c". The PR head is now `7f56fc4`, the manager's merge of main `24c7f853`. Consider one sentence: the records were taken at the author head `cca12e3c`, and `7f56fc4` composes main `24c7f853`. On the merged head, this reviewer measured `tb/pp_top` at 10,649 checks: 10,528 at `b48312e1`, plus +106 from main (#185/#186), plus +15 from this branch.
- **The WK12 row.** The row of the PR body's checks table lists two controls. Three more grade WK12's counts and its precondition: `listener-rebind-abandons-leave`, `listener-park-never-retires` and `listener-aa-tx-stays-aa`. `tb/srp_top/README.md:806-812` already records them, so the PR row could name them too.

## Prior findings at this head

| ID | Severity then | Status at 7f56fc4 | Evidence |
|---|---|---|---|
| R666-001 | MAJOR | **RESOLVED** | Cause removed: `hdl/top/protocol_processor_top.sv:3300-3313` drives `lstn_evt_tk_failed_w` from `srp_tk_reg_state_w[k] == 2'd2` of the presented TKREG source, not `evr_pay_w[15]`. The listener latches it into `tkfail_r` when it takes the event (`KL_pp_acmp_listener.sv:1024-1030`), and SOK applies it (`:1167-1173`). The level is the registered `rtype_r`, written in the same clock as the strobe (`KL_srp_listener_fsm.sv:829-845`, `:950-954`), so the uncoalesced timing is unchanged. The F05.3 SOK cell and the transition ROM are untouched: the listener diff is comment-only. AS5d (Advertise→Failed→Advertise) and AS5e (Failed→Advertise→Failed) hold the listener busy across both strobes: MAC TX held, six requests, TX free = 1. They prove from the trace that the listener took one coalesced event, then require only the six answers (no arc), GET_RX_STATE byte-exact, and the same after an unchanged refresh. The author's receipts at `cca12e3` and this reviewer's run at the exact merged head both show the golden PASS (ACMP 58/58) and `tk_failed_first_payload`, `tk_failed_or_payload`, `tk_failed_and_payload`, `router_coalesce_unflagged` and `tk_type_unlatched` all KILLED by their named checks (`receipts/acmpmut.log`, `receipts/acmpmut-coalesce-results.json`). |
| R665-1-F2 | MINOR | **RESOLVED** | Same cause and evidence as R666-001. `05_acmp_engine.md:315-325` now states that the top reads the level and why: the router keeps the first payload. "Residual" and "not changed here" appear in neither 05 nor the PR body. |
| R665-1-F1 | MINOR | **RESOLVED** | Suite checks, each with a planted control in `tb/srp_top/mutants.py:172-187` (see the next table). Coverage set `("WK", 12), ("RB", 9)` (`mutants.py:303`). READMEs: `tb/srp_stream_fsms/README.md:73-98, 229, 247`; `tb/srp_top/README.md:707, 777-821`. The F1 verification step itself, re-run at the head with the published R665-1 `probes.py` (hash-verified against its MANIFEST): U1, U2, U3 and U5 now **KILLED**. U6 and U7 survive, accepted as likely equivalent and recorded in `tb/srp_top/README.md:816-821`. U4 and U9 stay KILLED, and both goldens PASS (`receipts/r665-1-probes-head.log`). |
| R665-1-F3 | RESIDUE | **RESOLVED** | The exact wording is applied: 10 §6.4 row `docs/architecture/10_srp_engine.md:596`, the banner `hdl/srp/KL_srp_listener_fsm.sv:70-73`, and the PR body's first settle row. |
| R666-002 | RESIDUE | **RESOLVED** | All nine listed locations are applied (`tb/acmp_listener/sim_main.cpp:1178`; `tb/pp_top/sim_main.cpp` both headings; `tb/srp_stream_fsms/sim_main.cpp` the section heading and the RB1-RB3 prefixes; `walk_main.cpp:36`, `:464` and `:532`; `tb/srp_top/mutants.py:162`). One new instance was introduced later: R665-2-R1. |
| R665-1-S1 | SUGGESTION | **RETAINED** (not assigned) | `tb/pp_top/README.md:2130`: `st_ls_teardown_as_declare` now reads "1 of 58" while the table's lead-in and the other rows date to the 2026-10-04 "of 43" run. This reviewer confirmed the figure at the head: `ACMP: 58 checks, 1 failures`, the named check `AS6: the sink's VLAN membership is released` (`receipts/acmpmut-teardown.log`). |

How each R665-1-F1 settle arm is covered at `7f56fc4`. All controls were re-run at the exact head (`receipts/srpmut.log`: 18 checks, 18 PASS, both goldens PASS).

| Settle arm | Check | Control (KILLED at head) |
|---|---|---|
| a settle while parked onto a third stream | RB4 (suite); WK12 (walk, all four shapes) | `listener-csid-ram-ignores-park` (RB4; WK12, 14 failures = 5 + 9 at 3/5 and 9/9), `listener-csid-flops-ignores-park` (WK12, 3 = 1 + 2 at 1/1 and 2/2) |
| a rebind back to the parked stream | RB5 | `listener-rebind-back-keeps-park` |
| an LO applicant settled onto another stream | RB6 | `listener-lo-not-owed` |
| a txLA! walk while parked | RB7 | `listener-park-retires-on-txla` |
| received Listener values while parked (LO) | RB8 | `listener-parked-applies-rx` |
| the no-record sink, the new RB9 behaviour | RB9 | `listener-unrecorded-applicant-owes` |
| WK12's own counts and precondition | WK12 | `listener-rebind-abandons-leave`, `listener-park-never-retires`, `listener-aa-tx-stays-aa` |

## Lenses

### Conformance - CLEAN

- **#189.** Milan v1.2 Table 5.39: REGISTERING_FAILED is "1 if registering a Talker Failed attribute". It is now the registered type at the time the event is taken, and a coalesced pair of swaps cannot leave it on the intermediate type. Table 5.30 marks `EVT_TK_REGISTERED` in SETTLED_RSV_OK as `x`: still no arc, action, frame or notification. That is the AS5d/AS5e "six answers and nothing else" check plus the unchanged ROM. IEEE 802.1Q-2018 35.2.6 (a type change is the new declaration alone) is unchanged in the registrar.
- **#188.** 802.1Q-2018 10.7.7 and Table 10-3. The settle applies Lv! and keeps an applicant that owes a message (LA sL, LO s) on its own value. The parked arms checked are: a third stream, a rebind back, LO, txLA! (LA→LO, no message), and received values. The new no-record term (`KL_srp_listener_fsm.sv:609-610`) makes a sink with no record hold no value. So a LeaveAll-driven VO→LO no longer makes its first settle send an Empty for a stream_id it never declared, or delay its New by one T-MRP-JOIN (RB9). The Δ13 registrar (Milan v1.2 4.2.7.2.2) is untouched: the registrar block is not in the delta.
- **Interface.** No port, parameter or register-map change: `receipts/integrity-final.txt`, 0 port or parameter lines changed in the top since `cb8bab04`, and the top's merge-side lines are three internal wires of #186.

### RTL - CLEAN

- **`evt_tk_failed_live`** (`protocol_processor_top.sv:3306-3313`) is an N-way compare of the registered `evr_src_w` against constants, muxing a 2-bit status level from flops. It is small, and it adds no state and no latency. It indexes the same sink `k` as the payload it replaces (`evr_payload_w[EVR_TKREG_BASE_C + k]`, `:3251`). TKUNR and other sources drive 0, as the payload did.
- **The payload** still carries the strobe-time type to the trace ring (`:3332-3333`).
- **The settle change** (`KL_srp_listener_fsm.sv:608-613`) gates only the Lv! image on `rec_valid_r`. `set_same_w` was already gated, and `lvp_r` (`:698`) follows `set_owes_w`. The walk's message gate (`:732`) already required `rec_valid_r`.
- **`lint_hdl.sh` at the head** passes, all modules LINT OK, with the pinned simulator (`receipts/lint_hdl-head.log`).

### Robustness - CLEAN

- **Coalescing.** The window is bounded by the listener's idle take. Within it, any number of swaps collapses to the level at take time, and a swap after the take re-strobes a fresh event. Both directions are exercised under a held MAC TX with full TX slots, and the coalescing is proven by the trace's coalesced bit, which `router_coalesce_unflagged` KILLS.
- **The settle arms.** Two rebinds within one T-MRP-JOIN, a rebind back, LO, txLA! and rx-while-parked each fail under their control. The U5 effect R665-1 reported (a Lv for the middle, never-declared stream) is now killed by RB4 and WK12 at every shape.
- **Residual corners.** None of these is introduced by this delta:
  - a stale TK_REGISTERED taken after the listener's own A15/A8 on that sink reads level 0;
  - the router does not order one sink's REG and UNREG events. That is the router's existing contract (02 §5).

### Tests - CLEAN

Exact-head execution, all in disposable copies of `git archive 7f56fc4d`, with pinned Verilator 5.050 (wrapper sha256 `905795b99e0a…`, the same as the author's record):

| Run | Result | Receipt |
|---|---|---|
| `tb/pp_top` `make run` (seven builds) | rc 0, **10,649 checks: 10,649 PASS, 0 FAIL** | `receipts/pptop.log`, `.rc` |
| `tb/srp_stream_fsms` `make` (walk at 1/1, 2/2, 3/5, 9/9, then suite) | rc 0, suite 1,361/1,361 | `receipts/fsms.log`, `.rc` |
| `tb/acmp_listener` `make run` | rc 0, 3,170/3,170 | `receipts/acmpl.log`, `.rc` |
| `tb/srp_top/mutants.py --only` (13 #188 arms, 16 grades) | rc 0, 18/18 PASS, all KILLED | `receipts/srpmut.log`, `.rc` |
| `tb/pp_top/acmp_mutants.py --only` (5 coalescing controls) | rc 0, golden PASS (ACMP 58/58), 5 of 5 KILLED | `receipts/acmpmut.log`, `receipts/acmpmut-coalesce-results.json` |
| `acmp_mutants.py --only st_ls_teardown_as_declare` | KILLED, 1 of 58 (the README figure) | `receipts/acmpmut-teardown.log` |
| R665-1 `probes.py` (G0, U1-U9) | U1/U2/U3/U4/U5/U9 KILLED; U6/U7/U8 survive (U6/U7 accepted as equivalent; U8 recorded in R665-1 as a candidate equivalent) | `receipts/r665-1-probes-head.log` |

- **Author receipts at `cca12e3`** were verified against the published manifest: 1,171/1,171 entries hash-match, none missing, none unlisted (`receipts/evidence-manifest-check.txt`). They show:
  - every processor gate rc 0 at base `cb8bab04` and at head;
  - `run_suites` 1,030,051 → 1,030,070;
  - the srp_top campaign at 179 checks, all PASS, with assertion coverage 101/101;
  - ACMP 65 of 65 KILLED;
  - every other campaign rc 0, and the listed ones identical.
- **Spot checks** against the head counts: the PR's +19 suite checks (pp_top +10, srp_stream_fsms +9); the srp_top 168 → 179 (+11 tuples); and the coverage 94 → 101 (WK12 plus RB4-RB9).

### Docs - CLEAN (two RESIDUE items, one retained and one new SUGGESTION)

- **The architecture deltas are accurate:** 05 §6.3 (`:315-325`), 10 §6.4 (`:596-606`), and the banner (`:67-80`). They match the code and checks above. R665-2-R2 is the one imprecise sentence, in 05 §5.
- **The READMEs** record every new check, control, count and the two equivalents: `tb/srp_stream_fsms/README.md`, `tb/srp_top/README.md` and `tb/pp_top/README.md` (`:2077-2086`, `:2142-2154`).
- **Doc gates at the head** all report OK: `lint`, `links` (1,218), `matrix` (115 REQ rows, 17 GAP), `params`, `aecpcmd`, `modmatrix`, `stale`, `reqtags`, `ids` and `figures`, plus `gen_matrix.py --check` (94 rows, 0 untested). The git-index-dependent targets ran in the review clone, which stayed clean (`receipts/make-check-head.log`, `receipts/make-check-gitneeded-head.log`, `receipts/gen_matrix-head.log`). `wavedrom-check` and the diagram render were not run.
- **The comment rule** holds for the delta's new source comments, except R665-2-R1.

## Merge verification (`7f56fc4` = `cca12e3c` + main `24c7f853`)

- **Automatic merge.** `git merge-tree --write-tree cca12e3c 24c7f853` reproduces tree `34af6de8…` exactly, so the merge is the conflict-free automatic merge with no manual resolution (`receipts/integrity-final.txt`).
- **Auto-merged files:**
  - `hdl/top/protocol_processor_top.sv`: main adds three lines (the `aecp_rgy_flags_w` wire and two connections), disjoint from `evt_tk_failed_live`. `lint_hdl` passes at the head.
  - `tb/pp_top/sim_main.cpp`: both sides' sections run in the merged bench. 10,649 equals the sum of 10,528 (`b48312e1`), +106 from main (10,634 at `4865184`, PR #196's record), and +15 from this branch (10,543 at `cca12e3`). Nothing was lost or duplicated.
  - `tb/pp_top/README.md`: the sections are disjoint. Main's notify-campaign and dispatch totals and this branch's ACMP rows ("nine controls"; `st_ls_teardown_as_declare` 1 of 58, re-measured here) are each consistent with the head.
- **Totals.** No README states an overall pp_top total. The `ACMP: 58 checks` golden at the head matches the README's "of 58".

## Integrity after probes

`receipts/integrity-final.txt`:
- HEAD and tree are the exact ones, and `git status` is empty;
- the worktree and the index equal HEAD;
- all 680 tracked paths match their blob bytes and modes, and the index entries equal the HEAD tree;
- the processor repository has **0 gitlinks**, so no submodule pin applies here.

Every probe ran in an archive copy under the packet's scratch directory. The review clone only ran read-only doc checks.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #188/#189 frozen bodies and assignments; round-2 assignment; Milan v1.2 Tables 5.30/5.39, 4.2.7.2.2; 802.1Q-2018 10.7.7, Table 10-3, 35.2.6; F05.3 SOK cell; router contract 02 §5 | R665-2 | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| RTL | CLEAN | `protocol_processor_top.sv:3246-3313`; `KL_pp_acmp_listener.sv:1024-1030, 1160-1173`; `KL_srp_listener_fsm.sv:67-80, 412-430, 598-613, 692-735, 826-875, 950-957`; `KL_pp_event_router.sv:14-34, 150-195`; merge-side top lines; lint at head | R665-2 | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Robustness | CLEAN | busy-listener coalescing in both directions, with its preconditions; settle arms under five controls plus the no-record arm; R665-1 U-probes at head | R665-2 | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Tests | CLEAN | exact-head pp_top full suite, srp_stream_fsms, acmp_listener; 13 srp_top arms; 6 pp_top ACMP controls; R665-1 probes; author packet (1,171 hashes) and its campaign and gate logs | R665-2 | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Docs | CLEAN (RESIDUE R665-2-R1, R665-2-R2; SUGGESTION R665-1-S1, R665-2-S2) | 05 §5 and §6.3; 10 §6.4; listener banner; three suite READMEs; PR body; doc gates at head | R665-2 | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |

## Real limits

- **No manager source bank** runs at this head, and I neither claim nor infer one.
- **Author receipts.** The author's gate and campaign receipts are at the source head `cca12e3c`, not at `7f56fc4`. My exact-head execution was focused: the suites and controls listed above. It did not include:
  - the full `run_suites.sh`;
  - the notify, aecp, dispatch and d3 campaigns, or the other campaigns, at the merged head;
  - Yosys or the elaboration guards;
  - `wavedrom-check` or the diagram render;
  - the parent consumer gates.
- **The evidence commit** `61e4bb57` is unsigned: GitHub verification reports "unsigned". Its integrity rests on its `MANIFEST.json` hashes, which all match.
- **Hosted contexts** at the exact head, read when this report was written (`receipts/hosted-check-runs-head.tsv`): `docs-gates` and `portability` completed with success (two of each); `suites` was still in progress (two). The manager owns hosted/act acceptance.
- **No hardware.** Physical calibration was NOT RUN, and nothing here is hardware proof.

## Pending manager duties

- **Merge-turn validation.** Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Source validation is distinct from that candidate: source base `b48312e1`, live dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`.
- **Hosted and parent gates.** Complete hosted/act acceptance (the `suites` contexts were in progress) and the parent consumer gates for the candidate.
- **Residue checklist.** Carry R665-2-R1 and R665-2-R2 to the residue checklist with their exact fixes. R665-1-S1 and R665-2-S2 are optional.
- **Second review.** Obtain the second independent review at this head. Merge needs two independent positive reviews and the full completion bar.

## Packet

`MANIFEST.sha256` lists every publishable receipt and script (sha256sum format, relative paths).
- **Scripts:**
  - `scripts/run_probes.sh`: exact-head suites and controls;
  - `scripts/verify_integrity.sh`: head and tree, blobs and modes, index, gitlinks, the re-merge, and the port/parameter scan;
  - `scripts/verify_evidence.py`: the author packet against its manifest.
- **Receipts** are under `receipts/`. Host paths are replaced by `<packet>`, `<clone>`, `<tools>` and `<container layer>`.

R665-2 FINISHED
