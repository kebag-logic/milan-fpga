[R770] POSITIVE - exact head 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1

# R770-3: external independent review of PR #213 (issue #212), round 3

- **Head:** `834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1`, tree `93bea04f1a5e4173ee43f4824c3419d774d8206f`, as the PR reports.
- **Delta judged:** `a2fce43..834cc88`, six commits, no rebase. `a2fce43` is an ancestor of the head. Code the delta does not touch keeps its R770-2 / R770-1 lens verdict, unless the delta changes something it depends on.
- **Read, in order:** the docs README conventions (the repository has no AGENTS.md or CONTRIBUTING.md); the issue body, the round 2 and round 3 assignments (issuecomment-6651608145, -6670001706); the PR body and the manager's evidence comments; the diff; the published packet `kebag-logic/milan-fpga@c5661216…/review-evidence/pp212-r1/author-r3`.
- **Other reviewer's report:** read only after this verdict and ledger were written, to check its residues and suggestion.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. R769-2 F1 = R770-2 F1 is resolved at its cause by option (a), as ruled:
- LINK_DOWN (Flush!) and LINK_UP (Begin!) now take every sink registrar to MT, settled sinks included, ahead of every other event of their clock.
- A settled sink's withdrawal is published as a leavetimer!'s is.
- My round 2 probe XP2, the falsifier of that finding, now gives `reg 0 tk 0 state 0`. It fails again (`reg 1 tk 1 state 1`) on the round-2 listener RTL and under the new arm `settled-link-flush-dropped`.

Two RESIDUE items (wording only) and four SUGGESTIONs are recorded below. None affects the verdict.

## Findings

### R1 - RESIDUE - Docs - an unclear back-reference in the arm table

- **Where:** `tb/srp_top/README.md:901`, row `settled-link-flush-dropped`: "a settled sink's registrar takes no link change (the exception before this row)".
- **Problem:** "before this row" reads as the table row above, which is `seed-deadline-rebuild-drops-now`. The meaning is the settled-sink exception the listener made before PS24's change.
- **Exact fix:** replace "(the exception before this row)" with "(the settled-sink exception the listener had before PS24)".
- **Why RESIDUE:** wording only. No count, named check or edit changes.

### R2 - RESIDUE - Docs (PR body) - "README cells re-recorded" for eight arms, where seven have a cell

- **Where:** PR body, Validation, the paragraph after the campaign table: "In SRP, against round 2: five new arms, and eight arms whose counts the new rows move (README cells re-recorded)."
- **Evidence:**
  - The author's `srp-vs-round2.txt` lists the eight MOVED arms. My re-run of all eight gives the same counts.
  - Seven of them have a failing-check count cell in `tb/srp_top/README.md` (`presettle-removed` 37, `seed-no-registered-strobe` 26, `rebind-same-not-kept` 5, `keep-declares-seed-type` 2, `pt-link-flush-dropped` 6, `listener-settle-compare-dropped` 45, `listener-teardown-keeps-declaring` 84). All seven are re-recorded correctly.
  - The eighth, `listener-reprobe-abandons-leave` (1 → 3 failures, now also on PS24), sits in the issue #188 table (`:792`). That table has no count column, so there is no cell to re-record. Its named check RB2 is still the one required.
- **Exact fix:** replace "(README cells re-recorded)" with "(the seven README cells that record a count re-recorded; the issue #188 table, which holds `listener-reprobe-abandons-leave`, records none)".
- **Why RESIDUE:** wording in the PR body only. No figure, receipt or test changes.

### S1 - SUGGESTION - Conformance, Docs - say that the LINK_UP strobe is a local choice

- At LINK_UP the head publishes EVT_TK_UNREGISTERED for a settled sink whose registrar holds a value received while the link was down (my XP8 shows it). 10 §6.4 (`10_srp_engine.md:841-842`) says LINK_UP "ends it the same way".
- 802.1Q-2022 Table 10-4 gives Begin! no Lv indication; only Flush! carries one.
- Publishing the end of a registration the application was told of is the consistent local choice: otherwise `tk_reg_state` would drop to NONE with no class-C event. It is not a defect.
- §6.4 could make the point explicit, for example: "LINK_UP (Begin!, which Table 10-4 gives no indication) ends it the same way, so the application sees the end of every registration it was told of."

### S2 - SUGGESTION - Tests - adopt the cases the new probes cover

My probes XP7, XP9, XP10, XP12 and XP13 pass at the head and fail on the round-2 listener RTL. PS24 does not cover them:
- a link fall on the clock the seeded LV arm issues (arm, then cancel of the same slot; a stale expiry later is quiet);
- a parked re-bind seeded on a held Talker Failed, then a link change before the walk (only the owed Lv goes out);
- two sinks sharing one stream (both withdrawals published, one Lv, one New after the talker re-declares);
- a LeaveAll on the link-fall clock, and on the clock before it.

The RTL term under test is the same per-sink branch that PS24 and its five arms already grade, so there is no verdict effect. Adopting the cases would pin the timer-op order and the group behaviour against later edits.

### S3 - SUGGESTION - Tests - one end-to-end row for the settled-sink link change

- PS24 grades the publication at the listener.
- No `tb/pp_top` row takes a settled, registered sink through a link change and reads what the processor then reports: the ACMP listener leaving SETTLED_RSV_OK, GET_RX_STATE, and GET_STREAM_INFO's failure fields after a Talker Failed.
- The path is the one EVT_TK_UNREGISTERED already drives at a leavetimer!, which AS-phase rows exercise. So this is coverage depth, not a gap in the ruling's required row.

### S4 - SUGGESTION - Conformance (follow-up, outside issue #212)

- The talker FSM's Listener registrars take no Flush!/Begin! either. `KL_srp_talker_fsm` has no link input; `KL_srp_top.sv` wires `link_up_i` only to `u_domain` (`:374`) and the listener (`:622`).
- This predates the PR and is outside issue #212, which is about the Stream Input side.
- Now that the listener follows Table 10-4 on a link change, a tracking issue for the talker side would close the same class of gap.

## Round 3 focus items, judged at cause

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Every sink registrar to MT at LINK_DOWN/LINK_UP, settled included; a settled sink's withdrawal published as a leavetimer!'s; nothing from before a link change seeded or kept by any path | **Met** | See "Conformance and RTL" below |
| 2 | PS24 and its five arms caught by name; PS20 Talker Failed after the old Lv | **Met** | PS24 (`sim_main.cpp:3420-3519`): with and without a full port table, before and after the old Lv. Each check: the fall publishes one EVT_TK_UNREGISTERED, NONE, MT, declaration withdrawn, no timer op; the rise adds nothing; A8 and A15 on the same triple apply nothing; the two tx!s send only the owed Lv; LV at the fall cancels its slot; the next declaration registers again; a Talker on the link's clock registers nothing. All five arms are KILLED on their PS24 checks in my run, with the README counts (11, 5, 6, 1, 1). PS20 now runs the Failed case before tx! and after the Lv went out (`:3221-3246`); `keep-declares-seed-type` fails 2 (was 1) |
| 3 | The "settled sink across a link change" limit gone from 10 §6.4, the integrator guide and the PR limits | **Met** | 10 §6.4 (`:833-843`) now states the flush and its publication. The integrator guide (`integrator.md:630-633`) says "a settled input's too". The PR's Limits entry is replaced by "A settled sink at a link change", which states the new behaviour. Searching the docs, HDL and READMEs for "through a link", "across a link" and "no link input" finds only the historical sentence "Before issue #212 a settled sink's registrar had no link input" (`:842-843`) |
| 4 | The 13-bit note at `KL_srp_listener_fsm.sv:499` and its 4500-7500 ms range; the residue texts applied exactly | **Met** | `:500-502`: "(13 at the default T-MRP-LEAVE); the width stays 13 bits across F08.1's 4500-7500 ms range". F08.1 (`08_timing.md:40`) gives "5000 ms (4500–7500)". `$clog2(4501)` = `$clog2(7501)` = 13; `PT_SLACK_C` is 3691 and 691 at the ends, both below the initial LV age (3692, 692), so the wrap-safe compare holds across the range. The residue texts are below |
| 5 | The area table (2x2 13,030 LUT, -163 vs round 2) matches the receipts | **Met, and reproduced** | The author's `area/834cc88/srp_top_2x2.stat` sums to LUT1-6 = 13,030 and FD = 5,334, and the 8x8 file to 28,480 / 11,224. The 10 §5.1 deltas (+1,555 LUT, +170 INV, +522 FF; +5,434, +711, +1,988) are the stat-file differences against main. My own run (sv2v 0.0.13, yosys 0.66, the author's lowering) gives `KL_srp_top` 2x2 at **13,030 / 5,334** and the listener at N = 2 at **6,476 / 1,456**, identical to the author's |

### Conformance and RTL (focus 1)

Paths checked in `hdl/srp/KL_srp_listener_fsm.sv`:
- **Link branch (`reg_plane`, `:1434-1445`).** It is now first among the sink registrar's events, for every sink. LV cancels the slot (`tpend_r <= T_CANCEL_C`), the registrar goes to MT, and EVT_TK_UNREGISTERED is raised when it was not MT. The `!armed_r` gate (`:1495-1498`, after the link branch) still silences unbound sinks, so PS22's "raises nothing" holds.
- **`reg_ind` (`:575-594`).** `ind_reg_w` is gated by `!link_ev_w`, so a decoder value on the link's clock requests no declaration. `ind_unreg_w` gains `link_ev_w && reg_r != MT`, so the declaration is withdrawn (Lv at the next tx!), as at a leavetimer!. `ind_fchg_w` is not gated, but its only use is inside the registering branch, which the link branch pre-empts.
- **Seed.** `seed_v_w` (`:751-752`) reads `pt_nreg_w`, which is MT on the link's clock (`pt_next` `:706-707`). On any later clock the entries are MT too.
- **Keep.** `keep_v_w` (`:883-884`) requires `reg_r != MT` and `!link_ev_w`, so neither a same-clock nor a later A15 keeps anything.
- **A15 on another value.** It starts MT from the port registrars, which the link change emptied.
- **Timer ops.**
  - A seeded arm issuing on the link's clock is followed by a cancel of that slot on the next clock: in the block, the per-sink `tpend_r <= T_CANCEL_C` lands after the `sdl_v_r` clear (XP7).
  - A LeaveAll on the link's clock arms nothing (XP12). A LeaveAll on the clock before it ends in a cancel (XP13).
- **Status.** `tk_reg_state` reads NONE and `msrp_fail_code` 0. `acc_latency` keeps the last latched value while the sink stays settled, exactly as after its leavetimer! (XP11: 888 in both). That is the existing "latches on each registering event" contract (10 `:630`) and matches "published as at its leavetimer!".
- **Flush! vs Begin!.** Table 10-4 gives Flush! an Lv indication from IN and LV; the head publishes it at the fall. Begin! carries none; the head's strobe at LINK_UP for a registration made while the link was down is a local consistency choice (S1).
- **Ports and comments.**
  - `KL_srp_top`'s port list is unchanged: the author's sha256 of its module header is equal at main and head. `protocol_processor_top.sv` is unchanged.
  - Round 3 adds no state (FF unchanged at both shapes).
  - **Comment rule:** I scanned every added line of `.sv`, `.cpp`, `.py` and `.patch` in the delta for lane labels, round names, reviewer IDs and comment IDs. There are none; the only hits are the protocol term "LeaveAll lanes". The comments state behaviour with 802.1Q-2022 Table 10-4 and issue #212.

## Prior findings at this head

| Finding | Ruling | At this head |
|---|---|---|
| R769-2 F1 = R770-2 F1: a pre-outage registration survives a link change through a settled sink, then is kept at a same-stream re-bind | option (a) | **Resolved at cause.** See focus 1. XP2 and XP3 now pass as CHECKs. PS24 grades the ruled sequence; `settled-link-flush-dropped` restores the round-2 exception and fails 11 PS24 checks |
| R770-2 S1: PS20 Talker Failed same-stream re-bind after the old Lv | test | **Resolved.** PS20 runs it before tx! and after the Lv went out |
| R770-2 S2: retire the settled-sink link limit | taken | **Resolved** (focus 3) |
| R770-2 R1 = R769-2 R2: `10_srp_engine.md:226`, `:782` | reviewers' text | **Applied exactly, R769-2 R2's text** (now `:227`, `:783`): "(`$clog2(LEAVE_MS_P + 1)`, at the default `T-MRP-LEAVE`)" and "13 at the default `T-MRP-LEAVE` (F08.1)". My R1 text differed in wording only. The single-source rule is met either way |
| R769-2 R1: the PR body's SRP-campaign split | reviewer's text | **Applied.** The Validation row reads "280 of 280 (19 controls, 260 arm entries and the coverage check)". I checked it against the author's log (19 `control` lines, 260 KILLED, 0 UNPROVEN, coverage 167/167) and against `MUTANTS` (260 entries, 235 labels, 19 suite/group pairs) |
| R769-2 S1: the RTL width comment and the range | taken | **Resolved** (focus 4) |
| R769-2 S2: `msrp_fail_bridge_o` keeps a kept Failed's system id after an A8 (note only) | not taken in the round 3 assignment | **Retained as a note.** It is unchanged by the delta, and it also holds after a link change while settled. Its consumer gates it on FAILED (as R769-2 found), so nothing leaks |
| R770-1 F1-F5, R769-1 F1/R1/S1-S3 | round 2 | **Still resolved.** The delta moves the link branch, but PS16-PS23 still pass and their arms are KILLED by name in my run (`pt-link-flush-dropped`, `link-begin-dropped`, `unarmed-link-flush-dropped`, `keep-on-link-clock`, `top-listener-link-unwired`, `rebind-same-not-kept`, `keep-declares-seed-type`, and the PS22 arms) |

## Executed evidence (reviewer runs at the exact head)

All runs used pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, identity checked; `receipts/tool-versions.txt`) on fresh local clones of `834cc88`, each verified at head and tree with a clean status.

| Run | Result | Receipt |
|---|---|---|
| `tb/srp_stream_fsms` `make` (walk arms at four shapes, then the suite) | rc 0; **1,512 / 1,512**, equal to the PR | `receipts/suite-srp_stream_fsms.log` |
| `tb/srp_top` `make` | rc 0; **8,671 / 8,671**, equal to the PR | `receipts/suite-srp_top.tail40.log` (the full log is listed in `receipts/NOT-COPIED.txt`) |
| SRP campaign `--only` 22 arms: the 5 new, the 8 MOVED, the 7 whose patches were re-cut, `keep-on-link-clock` and `top-listener-link-unwired`; `--jobs 10` | rc 0; **30 / 30** (5 controls, 25 entries); every arm KILLED by its named check. **22 of 22 labels give the author's exact failure counts and tags** | `receipts/campaign-r3-arms.{log,rc,compare.txt}`, `receipts/campaign-r3-arms/*.log` |
| Reviewer probes XP1-XP13 in a scratch copy of the suite | rc 0; **1,614 / 1,614** (1,512 plus 102) | `receipts/probe-srp_stream_fsms.log`, `scripts/r770_probes_r3.inc`, `scripts/make_probe_tree.sh` |
| The same probes on the round-2 listener RTL (control) | rc 2; 19 FAIL: XP2, XP7-XP13 and 11 PS checks | `receipts/probe-on-round2-listener.log`, `scripts/probe_controls.sh` |
| The same probes under `settled-link-flush-dropped` (control) | rc 2; the same 19 FAIL | `receipts/probe-under-settled-link-flush-dropped.log` |
| yosys area, `KL_srp_top` 2x2 and listener N = 2 | 13,030 / 5,334 and 6,476 / 1,456, identical to the author's | `receipts/area-head-2x2/*.stat`, `scripts/area_2x2.sh` |
| Published packet integrity | 1,239 / 1,239 `author-r3/` files match `MANIFEST.json` `published_sha256`; none missing or unlisted; 2 are path-redacted | `receipts/evidence-manifest-check.txt`, `scripts/verify_evidence_manifest.py` |

**Probe P1 re-run.** My round 2 probe set is XP1-XP6, plus XPB. At this head:
- **XP1** (the 13-bit deadline across both wraps, 90 cases) passes unchanged.
- **XP2** is the falsifier of round 2's F1. It now passes as a CHECK: one EVT_TK_UNREGISTERED at the fall, NONE, nothing at the rise, and after A8 + A15 on the same triple `reg 0 tk 0 state 0`.
- **XP3-XP6** pass.
- **New probes.** XP7-XP13 target the claims "no registration from before a link change is seeded or kept after it, through any path" and "published as at its leavetimer!".
- **Result.** None falsifies a claim at this head. Each fails on the round-2 RTL, so each discriminates.

**The packet's integrity.** It is a sha256 manifest, not a cryptographic signature. The evidence commit `c5661216` is unsigned (git `%G?` = N).

**Spot-checks of the author's receipts** (`processor/head-834cc88`, bound to head and tree by `records/processor-records.txt`):
- every gate rc is 0: `make check`, lint under 5.050 and 5.052, `syn/yosys/run.sh`, elaboration guards, the REQ-tag checks (266 evidence lines, 14 suites), `run_suites.sh`;
- the sweep summary sums to **36 suites, 1,031,005 checks**, 0 failing;
- every campaign rc is 0, and the last lines equal the PR table (ACMP 103/103, AECP 67, AECP dispatch 105, CTR 18, D3 110/110, GSI 30, name write, notification 137/137, SRP 280/280);
- the scratch-parent gate at pin `834cc88` on dev `604899c0`: 28 rc files, all 0; behave 14 features, 508 scenarios; ROM digests equal to main's (`records/parent-records.txt`).

**Hosted, at the exact head (read-only, `receipts/hosted-checks-at-head.txt`):**
- `docs-gates` and `portability` were executed and succeeded, two runs each;
- `suites` was still `in_progress` when read at 02:08 UTC.

The manager owns hosted and act acceptance.

## Lens notes

- **Conformance - CLEAN.** The ruled Table 10-4 behaviour holds on every path I could build: settle, keep, seed, A8/A15 order, the link's own clock, parked re-bind, shared stream, Talker Failed. The PR's acceptance mapping for items 2 and 3 now includes PS24. S1 and S4 are suggestions.
- **RTL - CLEAN.** It is a small, uniform per-sink branch with no new state and no port change, and the comments follow the rule. The FF figures are unchanged, and the LUT figures reproduce.
- **Robustness - CLEAN.**
  - Ordering against the seeded arm, the pend queue and a LeaveAll is correct (XP7, XP12, XP13).
  - A stale expiry after the cancel is quiet (XP7).
  - The pre-existing stale-expiry window that the PR limits name is unchanged.
- **Tests - CLEAN.** PS24 covers the ruled sequence and the publication. The five arms fail it by name, and the re-cut arms keep their edits. Counts reproduce exactly. S2 and S3 are suggestions.
- **Docs - CLEAN.** The texts cover the settled sink: 10 §2, F10.5, §6.4, §5.1, 02 §4.1, the event catalog, F02.10 and the integrator guide. The limit is retired, and the residue texts are exact. R1 and R2 are wording residue.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | listener `reg_plane` link branch, `reg_ind`, `settle_keep`, `pt_next`, `pt_seed`, `status_map`; 802.1Q-2022 Table 10-4 Flush!/Begin!; Milan v1.2 §5.3.8.5; probes XP2, XP3, XP7-XP13 | R770-3 (delta); R770-2 and R770-1 for code the delta does not touch | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| RTL | CLEAN | `hdl/srp/KL_srp_listener_fsm.sv` delta (+29/-18): event priority, timer-op order, the comment rule; `KL_srp_top` header unchanged; area 2x2 re-measured | R770-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Robustness | CLEAN | a link change on the settle clock, the seeded-arm clock, the LeaveAll clock and the clock after it; parked re-bind; shared stream; Talker Failed; stale expiry after a cancel | R770-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Tests | CLEAN | PS24, the PS20 Failed variant, the five new arms, the re-cut and MOVED arms (22 re-run, identical counts), suites re-run, probe controls | R770-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Docs | CLEAN (R1, R2 RESIDUE) | 10 §2, §5.1, storage rows `:227`, F10.5, §6.4 `:783`, `:833-843`; 02 §4.1, event catalog, F02.10; integrator guide `:618-633`; both READMEs; PR body | R770-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |

## Real limits

- **Not run by me:** the full processor sweep (36 suites), `tb/pp_top`, the non-SRP campaigns, the full SRP campaign, lint, the yosys tops, the elaboration guards and the parent consumer gate. For these I rely on the author's published receipts, spot-checked as above. No manager source bank runs at this head, and none is claimed or inferred.
- **8x8 area:** not re-measured. The 2x2 shipping shape reproduced exactly.
- **Only the 5000 ms default exercised:** the probes run at `T-MRP-LEAVE`'s default. The 4500-7500 ms width statement was checked by arithmetic, not by an elaborated run at the ends.
- **Simulation only:** the evidence is simulation. Physical calibration was NOT RUN. Field skips are not hardware proof. No Vivado route of this head was run here.
- **Hosted `suites`:** still in progress when read.

## Pending manager duties

- **New Vivado route:** the shipping image needs a new route of this head. The parent-route comment (issuecomment-6652128599) set the round-1 route as the bound "without a new route". The yosys 2x2 LUT figure is +340 over round 1's 12,690 (13,030), with FF −38.
- **Merge-turn validation:** validate the current-dev merge candidate (builder and native banks; source base `a9e84b66`, live dev `cc204c6f`) at the merge turn, and link its receipts on the PR.
- **Hosted and act acceptance:** including the hosted `suites` result at this head.
- **Residue checklist:** carry R1 and R2.
- **Parent pin bump:** the ROM-digest rows (recorded, unchanged values) and the documented-pin update.

## Clone integrity after the probes

The review clone was only read. Every build and probe ran in separate clones and copies under the packet's `scratch/`. At the end (`receipts/clone-integrity.txt`):
- HEAD `834cc889…`, tree `93bea04f…`, and `git write-tree` equals the tree;
- `git status --porcelain --ignored` is empty, and `git diff --quiet HEAD` gives rc 0;
- the index (mode, blob, path) hashes the same as `git ls-tree -r HEAD`, and every working-tree file's blob equals its index blob;
- the repository has no submodule gitlinks (0 entries of mode 160000), so there are none to verify.

## Packet

- `REPORT.md` (this file).
- `MANIFEST.sha256`: every publishable receipt and script, with paths relative to the packet.
- `scripts/`: `run_all.sh`, `make_probe_tree.sh`, `probe_controls.sh`, `r770_probes_r3.inc`, `area_2x2.sh`, `verify_evidence_manifest.py`.
- `receipts/`: the logs and rc files above. Local paths are redacted to `<packet>`, `<home>`, `<scratch>` and `<verilator-5.050-root>`. Logs over 200 KB are listed with size and sha256 in `receipts/NOT-COPIED.txt` and `receipts/campaign-r3-arms/NOT-COPIED.txt`.

R770-3 FINISHED
