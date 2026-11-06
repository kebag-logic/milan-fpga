[R769] POSITIVE - exact head 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1

# Internal independent review R769-3: processor PR #213 (issue #212), round 3

- **Head**: `834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1`, tree `93bea04f1a5e4173ee43f4824c3419d774d8206f`. I checked
  both in the detached clone (`git rev-parse HEAD`, `git write-tree`).
- **Base**: `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Live dev at assignment: `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- **Round 3 delta reviewed**: `a2fce43..834cc88`, six commits: `154680f`, `d7b32c5`, `56bf44c`, `49fbdbf`, `ae8d582`,
  `834cc88`. Files: `hdl/srp/KL_srp_listener_fsm.sv`, `tb/srp_stream_fsms/{sim_main.cpp,README.md}`,
  `tb/srp_top/{mutants.py,README.md,mutations/*}` (5 new patches, 8 re-cut), `docs/architecture/{02_interfaces,10_srp_engine}.md`,
  `docs/guides/integrator.md`, and the PR body.
- **Code the delta does not touch** keeps its round 2 lens verdict (R769-2). The one exception is code whose
  behaviour depends on the reordered link branch (PS20 to PS23, LK1, AS7 to AS9). I re-ran it below.
- **Authorities**:
  - IEEE 802.1Q-2022 §10.7 and Table 10-4 (registrar: Begin!, Flush!, leavetimer!).
  - Milan v1.2 §5.3.8.5 and §5.5.3.5.18.
  - Issue #212: the acceptance in its body, the round 2 assignment (issuecomment-6651608145) and the round 3
    assignment (issuecomment-6670001706, option (a)).
  - `docs/README.md` §2, the single-source rules.
  - F08.1, where T-MRP-LEAVE is 5000 ms, range 4500 to 7500.
- **Published evidence**: kebag-logic/milan-fpga `c5661216625cf760ce182d480482141853d0d144`,
  `review-evidence/pp212-r1/author-r3/`.
- **Process**: I made my own pass over the diff and ran my own campaign subset first. Only then did I read
  the prior public findings (R769-2, R770-2) and my round 2 probe block.

## Verdict

POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head. All five lenses are clean.

- **R769-2 F1 = R770-2 F1 is resolved at its cause.**
  - What changed in the RTL: LINK_DOWN and LINK_UP now take every sink registrar to MT, settled or not. The
    link branch is the first of the clock's registrar events (`hdl/srp/KL_srp_listener_fsm.sv:1434-1444`).
  - How a settled sink's withdrawal is published, the same way as at a leavetimer!:
    - EVT_TK_UNREGISTERED;
    - the declaration withdrawn (`ind_unreg_w`, `:592`);
    - an LV registrar's leave slot cancelled.
  - Why nothing from before a link change comes back after it:
    - The keep path is blocked by `!link_ev_w` (`:884`).
    - The seed path reads the port registrars' next state, which is MT on a link clock (`:706-707`, `:751-752`).
    - A decoder value on the link's own clock registers nothing (`:584`).
- **My round 2 probe P1, re-run unchanged at this head** (`receipts/probe-srp_stream_fsms.log`):
  - Both runs end with `reg 0 tk 0 state 0`.
  - After the old Lv, P1 passes.
  - Before the old Lv, P1 fails only its "no push" clause. That clause was wrong in my probe. The link-down
    withdrawal correctly owes one Lv, and my probe Q1 shows that this Lv is the only push.
  - So the PR body's account of P1 is correct, and P1 does not falsify the fix.
  - P8 now reads `tk 0 state 0 unreg 1`.
- **PS24 and the PS20 Failed variant**:
  - Both match the ruling: settled and registered, the port table full and not full, link down and up, then A8
    and A15 on the same triple, before and after the old Lv.
  - Each of the five new arms is KILLED by its named check. The failure counts are 11, 5, 6, 1 and 1, the same
    as the author's receipt and the README cells.
- **The retired limit** is gone from 10 §6.4, the integrator guide and the PR's Limits.
- **The 13-bit comment and both residues** are applied in the exact text.
- **The area table** matches the receipts. I reproduced both shapes' stat files byte for byte: 2x2 is 13,030 LUT
  and 5,334 FF, −163 LUT against round 2.
- **Two test gaps and two notes**, none of which changes the verdict: S1 to S4 below.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1 — SUGGESTION — Tests
**A settled sink's LINK_UP (Begin!) is not graded on its own.**

- **Where**: `tb/srp_stream_fsms/sim_main.cpp:3420` onwards (PS24).
- **Claim this concerns**: `docs/architecture/10_srp_engine.md:833-843`: "LINK_UP finds a registrar registered only
  by a value received while the link was down, and ends it the same way". PR design item 4 says LINK_UP takes
  every sink registrar to MT, settled or not.
- **Why PS24 misses it**: in PS24 the registrar is already MT when the link comes back. Its "LINK_UP adds nothing"
  check therefore passes whether or not LINK_UP takes a settled sink's registrar to MT.
- **What already covers each part**:
  - PS23 and `link-begin-dropped` grade the rising edge of the shared `link_ev_w`, but for port registrars and
    unbound sinks only.
  - PS24 and `settled-link-flush-dropped` grade settled sinks, but at the fall only.
- **Evidence**:
  - The behaviour is correct at this head: reviewer probe Q5 passes.
  - A disposable arm makes a settled sink take LINK_DOWN but not LINK_UP
    (`receipts/arm-settled-begin-dropped.diff`, planted by `scripts/plant_settled_begin_dropped.py`). All 1,512
    suite checks still pass under it, PS24 included. Only my Q5 fails, together with P1's known clause
    (`receipts/arm-settled-begin-dropped.log`: 1,560 checks, 2 FAIL).
- **Impact**:
  - The real-world reach is small. It needs a Talker value decoded after the fall: a frame already in the
    receive pipeline, or a link level that lags the MAC.
  - A later edit that splits the flush by edge for settled sinks would land green.
- **Suggested outcome**: add a PS24 case and plant the arm above as a named mutant:
  - settled sink, link down, a JoinIn while the link is down (it registers), then link up;
  - expected: one EVT_TK_UNREGISTERED, NONE, MT, the declaration withdrawn.

### S2 — SUGGESTION — Tests
**PS24 runs only a Talker Advertise.**

- **Gap**: there is no Talker Failed variant of the link change.
- **Evidence**: my probe Q2 covers the Failed case, before and after the old Lv, and passes:
  - at LINK_DOWN, Asking Failed is withdrawn, `tk_reg_state` leaves FAILED, and there is one EVT_TK_UNREGISTERED;
  - the same-triple re-bind applies nothing.
- **Why it is only a suggestion**: the link branch does not depend on the type. This would mirror PS20's Failed
  variant.

### S3 — SUGGESTION — Conformance (note, outside issue #212)
**The listener's Lv goes out after the link returns.**

- **What happens**: the Listener applicant has no Begin! at LINK_UP. So the Lv owed from the link-down withdrawal
  is sent at the first tx! after the link returns. PS24 grades this ("the two tx!s send only the owed Lv").
- **Why it is harmless**: a peer registrar that is MT ignores an rLv, and the ruling scopes registrars only.
- **Related**: on the Begin! edge, the implementation publishes the end of a registration (EVT_TK_UNREGISTERED)
  as it does at Flush!. That keeps the application consistent with the registrar, as the ruling's "published
  the way a leavetimer!'s is" asks.
- **Suggested outcome**: if applicant Begin! at LINK_UP is ever wanted, track it in its own issue.

### S4 — SUGGESTION — Docs (R769-2 S2, carried, not taken)
**`msrp_fail_bridge_o` keeps the kept value.**

- **What happens**: the port stays ungated (`hdl/srp/KL_srp_listener_fsm.sv:1655`). It keeps the kept or
  withdrawn FailureInformation's system id while `tk_reg_state` is not FAILED. After a link change it keeps it too.
- **Why nothing leaks**: its only consumer, GET_STREAM_INFO, gates it on FAILED, and `KL_srp_top` documents that
  gate.
- **Suggested outcome**: the 10 §5.1 storage row could say "`msrp_fail_bridge` keeps its last value, valid only
  while FAILED".

## Prior public review findings at this head

| Finding | Status at `834cc88` | Evidence |
|---|---|---|
| R769-2 F1 = R770-2 F1: a registration kept through a link change by a settled sink and a same-stream re-bind | **RESOLVED** at its cause (option (a)) | RTL: the link branch is first for every sink (`:1434-1444`), `ind_unreg_w` (`:592`), keep `!link_ev_w` (`:884`), seed from `pt_nreg_w` (MT on a link clock). P1 re-run: `reg 0 tk 0 state 0` in both runs; its one failing clause is the owed Lv, the only push (Q1). P8: `tk 0 state 0 unreg 1`. PS24 covers IN and LV at the fall, the table full and not full, A8 and A15 before and after the old Lv, re-registration after the link returns, and a Talker on the link's clock. Five arms KILLED by name. Q2 to Q7 cover other paths (below) and pass |
| R769-2 R1: the SRP-campaign split in the PR body | **RESOLVED**, exact text | The PR's round 3 table quotes "(19 controls, 255 arm entries and the coverage check)" for `a2fce43`. Validation reads "280 of 280 (19 controls, 260 arm entries and the coverage check)", consistent with 255 + 5 entries over the same 19 pairs and with `camp-srp.log` (19 control lines, 260 KILLED, coverage 167/167) |
| R769-2 R2 = R770-2 R1: `10_srp_engine.md:226`, `:782` | **RESOLVED**, the R769-2 exact text | `:227` "(`$clog2(LEAVE_MS_P + 1)`, at the default `T-MRP-LEAVE`)"; `:783` "13 at the default `T-MRP-LEAVE` (F08.1)". No "5000 ms" remains in 10 |
| R769-2 S1: the 13-bit comment | taken | `KL_srp_listener_fsm.sv:501-502`: "(13 at the default T-MRP-LEAVE); the width stays 13 bits across F08.1's 4500-7500 ms range". This is correct: `$clog2(4501)` = `$clog2(7501)` = 13 |
| R769-2 S2: `msrp_fail_bridge_o` note | not taken (suggestion) | carried as S4 |
| R770-2 S1: Talker Failed same-stream re-bind after the old Lv | taken | PS20 `sim_main.cpp:3221` loops `lv_out`; `keep-declares-seed-type` KILLED, 2 failures (was 1) |
| R770-2 S2: the "settled sink across a link change" limit | retired | removed from 10 §6.4 (`:833-843` now states the flush and its publication), the integrator guide (`integrator.md:630-633`) and the PR's Limits (now a behaviour-change note) |
| Round 1 findings (R769-1 F1, R770-1 F1 to F5) | stay **RESOLVED** | The delta moves the link branch ahead of the other events. The rows and arms that depend on it still pass and kill: PS20 to PS23 and LK1 pass in my control (1,512/1,512 and LK1 2/2). `keep-on-link-clock`, `unarmed-link-flush-dropped`, `link-begin-dropped`, `pt-link-flush-dropped` (6, now also PS24), `top-listener-link-unwired`, `keep-declares-seed-type` and the re-cut `unarmed-indicates`, `unarmed-unregistered`, `unarmed-latency-strobe`, `lv-expiry-masked` and `r-sink-receive-priority-lost` are KILLED with the author's counts. pp_top's ACMP section (AS1 to AS9) passes |

## Focus items

1. **Flush!/Begin! for every sink registrar, and the publication.** Read in `reg_plane`, `reg_ind`,
   `settle_keep`, `pt_next` and `pt_seed`.
   - The link branch is the first event per sink. From LV it cancels the leave slot, sets MT, and strobes
     EVT_TK_UNREGISTERED when the registrar was not MT.
   - An unbound sink's strobe is still cleared by the `!armed_r` gate (F10.5).
   - On a link clock:
     - `ind_reg_w` is 0;
     - `ind_unreg_w` covers the declaration;
     - `keep_v_w` is 0;
     - `seed_v_w` is 0, because `pt_nreg_w` is MT.
   - So through settle, re-bind to the same or another stream, and either A8/A15 order, nothing from before a
     link change is seeded or kept.
   - My probes cover the remaining corners, all passing:
     - **Q1**: P1 with the exact expected pushes.
     - **Q2**: a settled Talker Failed through a link change.
     - **Q3**: an A15 on the same triple on the LINK_UP clock, with a registration made while the link was down.
     - **Q4**: a settle seeded LV, then link down on the very next clock, the clock on which the seeded arm
       issues. Arm, then cancel; MT; one unregistration; a late expiry is silent.
     - **Q5**: registered while the link is down, then LINK_UP ends it.
     - **Q6**: link down on the leavetimer!'s own clock. There is exactly one unregistration.
     - **Q7**: two settled sinks on one stream. Each publishes its own withdrawal.
2. **PS24, its five arms, and the PS20 Failed variant.**
   - My run and the author's agree line for line (`receipts/arms-vs-author.txt`, 17 of 17):
     - `settled-link-flush-dropped` 11;
     - `settled-link-unpublished` 5;
     - `link-withdraw-dropped` 6;
     - `link-clock-indicates` 1;
     - `settled-link-keeps-lv-slot` 1.
   - Each is caught by the PS24 check named in `mutants.py`.
   - The PS24 checks verify the publication at the fall: one EVT_TK_UNREGISTERED, NONE, MT, the declaration
     withdrawn, and no timer op from IN or a cancel from LV.
   - The PS20 Failed variant passes before and after the old Lv. Gap: S1.
3. **The retired limit.** It is gone from:
   - `10_srp_engine.md:833-843`;
   - `integrator.md:630-633`;
   - the PR's Limits.

   A repository search finds no other text claiming that a settled sink keeps its registration through a link
   change. Two texts remain, and both are correct:
   - 10's "Before issue #212 a settled sink's registrar had no link input" is historical.
   - PS23's README sentence "every registration a settle could take" is now true.

   02 §4.1, the event catalog and F02.10 now name the listener's registrars.
4. **The 13-bit note and the residues**: applied exactly (table above). The delta adds no new single-source
   breach in 10. No source comment in the delta names a bench lane, lane name, review round, reviewer ID or
   issue-comment ID. I searched every added line.
5. **Area.** Measured with sv2v and yosys 0.66 `synth_xilinx -family xc7 -flatten`, using the author's
   `area_some.sh`. My `srp_top_2x2.stat` and `srp_top_8x8.stat` are byte-identical to
   `author-r3/receipts/area/834cc88/`:

   | Shape | LUT | FF | INV |
   |---|---|---|---|
   | 2x2 | 13,030 | 5,334 | 2,981 |
   | 8x8 | 28,480 | 11,224 | 4,194 |

   - Against round 2's 13,193 / 5,334 and 28,193 / 11,224, that is −163 and +287 LUT, with 0 FF at both shapes.
   - Against main, +1,555 LUT, +170 INV and +522 FF at 2x2; +5,434 LUT, +711 INV and +1,988 FF at 8x8.
   - These match the PR table, `AREA.md` and the 10 §5.1 text.

## Lens evidence

### Conformance — CLEAN
- **Table 10-4, Flush! and Begin!**: both take IN and LV to MT for every sink registrar, settled sinks included.
  That is ruling (1).
- **The ruling's publication requirement**: a settled sink's withdrawal is published as at a leavetimer! (Lv
  indication, EVT_TK_UNREGISTERED, NONE, Listener declaration withdrawn).
- **Re-registration**: Milan v1.2 §5.3.8.5 holds after the link returns. PS24 "again", and Q5.
- **Note**: S3. It is outside the issue's scope and has no verdict effect.

### RTL — CLEAN
- **Delta read in full**:
  - 29 RTL lines added and 18 removed in one module.
  - No new state: the FF count is unchanged at both shapes.
  - No port or register-map change.
- **Same-clock interactions checked**:
  - the seeded arm in flight (Q4);
  - the leavetimer! on the link clock (Q6);
  - an A15 on either link edge (PS23, Q3);
  - a decoder value on the link clock (PS24).
- **Lint**: the pinned 5.050 run passes for 41 modules (`receipts/spot/lint.log`).

### Robustness — CLEAN
- **Probes**: Q1 to Q7 and P1 to P8 (`receipts/probe-srp_stream_fsms.log`): 1,560 checks, of which 1,559 pass.
  The one failure is P1's known wrong clause.
- **Wide failure-bridge level**: unchanged in kind (S4).
- **Stale-expiry window**: the seeded-arm window is unchanged and already in the PR's Limits.

### Tests — CLEAN
- **Delta arms**: 17 arm entries and 4 controls, 21 of 21 (`receipts/arms.out`).
- **srp_stream_fsms**: 1,512/1,512 under the campaign and on its own (suite and walk).
- **srp_top**: 8,671/8,671, plus its storage tallies, in my own run.
- **pp_top**: the ACMP section passes 62/62 (AS1 to AS9), and the main suite section with AQ passes 1,713/1,713.
- **Author's receipts** (manifest-verified): sweep of 1,031,005 checks with 0 failing over 36 suites; SRP campaign
  280/280 with coverage 167/167. The coverage set computes to 167 with PS24.
- **Gaps**: S1 and S2. Neither leaves the ruled sequence untested.

### Docs — CLEAN
These texts all agree with the RTL and the probes:
- 10 §2, §5.1 (measured cost), F10.5 arcs, and §6.4;
- 02 §4.1, the event catalog and F02.10;
- the integrator guide §8;
- the bench READMEs, with cells equal to `camp-srp.log`;
- the PR body.

## Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_listener_fsm.sv` reg_plane/reg_ind/settle_keep/pt_next/pt_seed/status_map against Table 10-4 Flush!/Begin!/leavetimer!; the ruling texts; PS23, PS24; probes P1, P8, Q1-Q7 | R769-3 (delta a2fce43..834cc88; rest R769-2/R769-1) | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| RTL | CLEAN | RTL delta (`:36-41`, `:163-165`, `:501-502`, `:511-516`, `:576-593`, `:1434-1444`), same-clock paths, lint 5.050 (41 modules), area 2x2/8x8 stat byte-identity | R769-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Robustness | CLEAN | probes Q1-Q7, P1-P8; disposable arm (settled sink without Begin!); status gating | R769-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Tests | CLEAN | PS24, PS20 delta; `mutants.py` delta and 13 patches; 21-entry campaign subset; srp_stream_fsms, srp_top and pp_top (ACMP and suite sections) runs; author sweep and campaign receipts | R769-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |
| Docs | CLEAN | `10_srp_engine.md` §2/§5.1/F10.5/§6.4, `02_interfaces.md`, `integrator.md`, both bench READMEs, PR body; residue texts | R769-3 | 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 |

## Published evidence checked

- **Integrity**: all 1,239 files under `author-r3/` equal `MANIFEST.json`'s published sha256. None is missing or
  unlisted, and two are rewritten as the manifest records (`receipts/evidence-manifest-check.txt`).
- **Commit signature**: the evidence commit `c5661216` carries no git signature (GitHub reports "unsigned"). Its
  integrity rests on that manifest.
- **Spot-checked receipts**:
  - processor gates: every `.rc` is 0;
  - `sweep-summary.txt`;
  - `camp-srp.log` (rc 0, 280/280) and its per-arm lines for every delta arm;
  - `area/` (`AREA.md` and the stat files);
  - parent `pin-834cc88`: all 28 `.rc` files are 0, including `record_rom_digests`.

## Real limits

- **Not run by me**:
  - the full pp_top suite: one run exceeded the 10-minute foreground bound (`receipts/spot/pp_top-full.rc` = 124,
    no output). I ran its ACMP and main-suite sections instead;
  - the full processor sweep;
  - the full SRP campaign (I ran 17 delta-relevant arm entries);
  - the other campaigns;
  - the scratch-parent gates.

  For all of these I rely on the author's manifest-verified receipts.
- **No manager source bank** runs at this exact head, and I claim none.
- **Hosted checks at the exact head**, at review time (`receipts/hosted-check-runs-834cc88.txt`):
  - `portability` and `docs-gates` completed with success;
  - both `suites` runs were still in progress.

  The manager owns hosted and act acceptance.
- **Not proved**: physical calibration was NOT RUN, and field skips are not hardware proof. No Vivado route of
  this head was run. The parent route on PR #213 is for `04856e48`.
- **Clone after probes**: HEAD and the tree are unchanged, and the worktree and index are clean. Modes equal the
  tree (`git write-tree` = `93bea04f`). The repository has no gitlinks. One untracked `tb/common/__pycache__/`,
  which the campaign driver wrote, was removed.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its
  receipts on the PR.
- Accept the hosted runs at this head, `suites` included.
- Decide on a new Vivado route. Round 3 adds no flip-flops, and its yosys LUT moves −163 at 2x2, within the
  flow's noise. The round 1 route note asked that round 2 not grow beyond it without a new route.
- Merge the parent's pin and ROM-digest rows and update its documented pin.
- Carry S1 to S4 to the author as optional work.

R769-3 FINISHED
