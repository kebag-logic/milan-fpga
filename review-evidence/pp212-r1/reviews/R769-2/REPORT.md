[R769] NEGATIVE - exact head a2fce4326ebdaf398a1920d79a664d44e6f1e5dd

# Internal independent review R769-2: processor PR #213 (issue #212), round 2

- **Head**: `a2fce4326ebdaf398a1920d79a664d44e6f1e5dd`, tree `40d4bfd5d553663d3c21fa9f38862b57c77acb84`. I checked
  both in a detached, cleared-context clone.
- **Base**: `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- **Round-2 delta reviewed**: `04856e48..a2fce43`, six commits (`76d1055`, `ead9bc0`, `2fcd9d1`, `b08368d`,
  `9849bdf`, `a2fce43`).
- **Code the delta does not touch** keeps its round-1 lens verdict (R769-1). That covers `tb/pp_top` and
  its ACMP arms, which the delta does not change.
- **Authorities**:
  - issue #212 body: the frozen acceptance 1-5;
  - the round-2 assignment on issue #212: rulings, tests, suggestions, residue, gates;
  - the manager's parent-route comment on PR #213;
  - IEEE 802.1Q-2022 §10.7, §10.7.8, Table 10-4;
  - Milan v1.2 §5.3.8.5, §5.5.3.5.18 and Table 4.3 (through F08.1);
  - `docs/README.md` §2, the single-source rules.
- **Published evidence**: kebag-logic/milan-fpga `dbbbb05a7c7cc260b85b1a769126335515fa31c4`,
  `review-evidence/pp212-r1`.
- **Process**: I read the prior public findings (R769-1, R770-1) only after my own pass over the diff.

## Verdict

**NEGATIVE.** One MINOR finding is open: R769-2 F1.

At this head, the round-2 changes do what the rulings asked, with one exception:

- **R769-1 F1 is fixed.** A re-bind to the same {stream_id, DA, VLAN} keeps its registration whatever the
  port table holds.
- **R770-1 F1, F2 and F3** each have a row and an arm that fails it by name.
- **The 13-bit leave deadline** is wrap-safe and keeps T-MRP-LEAVE exact, including the seeded arm's rebuilt
  absolute deadline.
- **The area figures** match the receipts. I reproduced the 2x2 figure byte for byte.
- **Both residues** are applied in the reviewers' exact text.
- **The exception**: R770-1 F4's cause is fixed for the port registrars and for unbound sinks. The new
  same-stream keep path opens it again for a sink that was settled through the link change. Such a sink
  keeps its pre-outage registration through an unbind and a re-bind to the same stream after the link
  returns.
  - The texts claim the opposite: 10 §6.4, the integrator guide, the PS23 README sentence and PR design
    item 4.
  - No row grades it.

Two RESIDUE items and two SUGGESTIONs are below. They do not affect the verdict.

## Findings

### F1 — MINOR — Conformance, RTL, Robustness, Tests, Docs
**A registration that a sink held through a link change is kept by its re-bind to the same stream after
the link returns.**

- **Where**:
  - `hdl/srp/KL_srp_listener_fsm.sv:1480-1487`. LINK_DOWN/LINK_UP flush a sink registrar only
    `if (link_ev_w && !armed_r[s])`: "A settled sink's registrar has no link input, as before".
  - `:868-878` (`settle_keep`). An A15 on the record's triple keeps any registrar state that is not MT.
  - `:1458-1471`. Since `76d1055` the A8 no longer clears the sink registrar.
- **Texts this falsifies**:
  - `docs/architecture/10_srp_engine.md:833`: "so no registration from before a link change is seeded or
    kept after it".
  - `docs/guides/integrator.md:630-632`: "A link down or up ends every registration a later settle could
    take, so after it each input waits for its talker's next declaration".
  - `tb/srp_stream_fsms/README.md:264-265`, PS23: "end every registration a settle could take".
  - PR design item 4: "so nothing registered before a link loss is seeded or kept after it".
- **Authority**:
  - IEEE 802.1Q-2022 Table 10-4: Flush! and Begin! take a registrar to MT.
  - The round-2 ruling on R770-1 F4: "fix, not a deviation … every port registrar goes to MT".
  - R770-1 F4's impact: a pre-outage registration applied at a settle after the link returns. Its example
    is a talker that rebooted during the outage, answers PROBE_TX, but has not declared its stream again.
- **Evidence** (reviewer probe P1, `receipts/probe-srp_stream_fsms.log`, `receipts/probe-srp_stream_fsms.diff`,
  `probes/r769_2_probe_block.cpp`):
  1. Fill the port registrars.
  2. Settle sink 0 on V, and the talker sends a JoinIn for V (IN).
  3. Take `link_up_i` down for 3 clocks, then up for 3 clocks. Probe P8 shows the sink stays IN with no
     EVT_TK_UNREGISTERED, which is the documented limit.
  4. A8 on sink 0. In the second run a tx! then sends the old Lv.
  5. A15 on V.
  - Both runs fail the "nothing applied" expectation: `reg 1 tk 1 state 1`. EVT_TK_REGISTERED, ADVERTISE
    and IN appear at the settle, and the next tx! declares New Ready.
  - The 1,500 suite checks all pass alongside the probe (1,539 checks, 1,537 PASS, 2 FAIL, both P1).
  - At the round-1 head the A8 cleared the registrar, so this registration ended at the unbind. The
    round-2 keep path now carries it across.
  - PS23's "a sink's kept registration" case covers only a sink that was already unbound at the link
    change.
- **Impact**:
  - Controllers commonly unbind and re-bind the same stream after a device's link returns.
  - That re-bind now raises EVT_TK_REGISTERED, `tk_reg_state` ADVERTISE/FAILED, SETTLED_RSV_OK and Listener
    Ready New from a registration the current link never made.
  - This lasts until this participant's own LeaveAll ages it (T-MRP-LEAVEALL plus T-MRP-LEAVE). It is
    R770-1 F4's impact on this path.
  - The integrator guide tells integrators that this cannot happen.
- **Required outcome**: one of the following.
  - (a) Apply LINK_DOWN (Flush!) and LINK_UP (Begin!) to every sink registrar, settled ones too, per Table
    10-4.
    - A settled sink's withdrawal would then be published as a leavetimer!'s is.
    - This also removes the PR's "A settled sink across a link change" limit.
  - (b) Keep the settled-sink exception, but make a link change end what a later A15 can keep. For
    example, use one flag per sink, set by a link change while the sink is settled and cleared at its A15,
    so that its next A15 starts afresh.
  - (c) A recorded maintainer scope decision accepting this case. 10 §6.4, the integrator guide, the PS23
    README sentence and PR item 4 must then say that a sink settled through a link change keeps that
    registration through a re-bind to the same stream.
  - Under (a) or (b), add a PS row: settled, registered, link down and up, A8, A15 on the same triple,
    before and after the old Lv, nothing applied. Add an arm that fails it by name.
- **Verification**:
  - Probe P1, or the new row, passes at the fixed head.
  - The new arm is KILLED by name.
  - The SRP campaign and the stream-FSM, srp_top and pp_top suites stay green.
  - The area at 2x2 and 8x8 is recorded, given the parent route constraint below.

### R1 — RESIDUE — Docs (PR body)
**The SRP-campaign split in the PR body's Validation table is wrong.**

- **Where**: PR #213 body, Validation, row "SRP (`tb/srp_top/mutants.py`)": "275 of 275 (5 controls, 269 arm
  entries)".
- **Evidence**:
  - `MUTANTS` holds 255 entries (230 labels) over 19 suite/group pairs.
  - The author's receipt `campaigns/srp-a2fce43/camp-srp.log` has 19 `control` lines and 255 KILLED
    entries, plus the coverage check, for 275.
  - The total, the coverage figure and every receipt are correct. Only the parenthesis is wrong.
- **Exact fix**: replace "(5 controls, 269 arm entries)" with "(19 controls, 255 arm entries and the coverage
  check)".

### R2 — RESIDUE — Docs
**The T-MRP-LEAVE value is copied outside F08.1.** This is the same class as R770-1 F5.

- **Where**:
  - `docs/architecture/10_srp_engine.md:226`, the storage row: "leave deadline 13 (`$clog2(LEAVE_MS_P + 1)`
    at 5000 ms)".
  - `:782`: "13 at 5000 ms".
- **Authority**: `docs/README.md` §2. Timing values live only in F08.1. A value copied outside its table is
  a review finding.
- **Exact fix**:
  - At `:226`, replace "(`$clog2(LEAVE_MS_P + 1)` at 5000 ms)" with "(`$clog2(LEAVE_MS_P + 1)`, at the
    default `T-MRP-LEAVE`)".
  - At `:782`, replace "13 at 5000 ms" with "13 at the default `T-MRP-LEAVE` (F08.1)".
- This is wording only. No figure, test or code changes.

### S1 — SUGGESTION — Docs
- The RTL comment `hdl/srp/KL_srp_listener_fsm.sv:499` ("enough for T-MRP-LEAVE (13 at 5000 ms)") carries
  the same copied value. It could read "(13 at the default T-MRP-LEAVE)".
- F08.1 gives T-MRP-LEAVE a 4500-7500 ms range, so it is also worth stating that the width stays 13 bits
  across that range (`$clog2(7501)` = 13, `PT_SLACK_C` = 691).

### S2 — SUGGESTION — Robustness (note only)
- After an A8 of a Talker Failed, `msrp_fail_bridge_o` (`:1644`, ungated by contract) keeps reading the kept
  FailureInformation's system id. Probe P5 shows `0x0011223344556677` with `tk_reg_state` NONE. Before
  round 2 it read 0.
- Its only consumer, `protocol_processor_top.sv:3605-3607` (GET_STREAM_INFO), gates it on
  `tk_reg_state == FAILED`, and `KL_srp_top.sv:230` documents "valid only with tk_reg_state == FAILED". So
  nothing leaks.
- The 10 §5.1 storage row could add "`msrp_fail_bridge` keeps the kept value, valid only while FAILED"
  beside "`acc_latency` reading 0 meanwhile".

## Prior public review findings at this head

| Finding | Status at `a2fce43` | Evidence |
|---|---|---|
| R769-1 F1: a same-stream re-bind loses its registration when the table is full | **RESOLVED** at its cause | (1) My round-1 probe, re-run unchanged: 1,502 of 1,502 (`receipts/r769-1-probe-at-a2fce43.log`). (2) PS20 covers the table full, before and after the old Lv, Advertise and Failed, with another DA or VLAN counting as another value. `rebind-same-not-kept` is KILLED by name (4), as are `keep-ignores-da`, `keep-ignores-vlan`, `keep-declares-seed-type` and `keep-latency-strobe-dropped`. (3) No stale registration survives a re-bind to another stream: probe P6 (re-bind away, then back: nothing) and PS5. (4) Nor does one survive a withdrawal: PS21 (rLv, an unanswered LeaveAll, a re-bind on the leavetimer!'s clock) and `unarmed-registrar-deaf` and `keep-ignores-expiry` KILLED. (5) The latest FailureInformation and latency are applied at the re-bind: probe P7 |
| R769-1 R1: `10_srp_engine.md:222` | **RESOLVED**, exact text | `:226` now reads "the value, type and payloads written with a registration, the leave deadline at the LeaveAll that starts LV; all read only while it is not MT" |
| R769-1 S1: the path's reach | taken | integrator §8 and 10 §6.4 state it with the shipping N = 2. Its last sentence is falsified by F1 |
| R769-1 S2: the 13-bit deadline | taken, measured | see focus item 4 below |
| R769-1 S3: the stale-expiry guard | §6.4 corrected per the ruling | `10_srp_engine.md:807-817` now says the guard ends at the arm's issue, that the queues' latency is unseen, and why an exact guard costs more than a few LUT. The guard is unchanged (`seed-lv-unguarded` and PS15 still graded) |
| R770-1 F1: rLv/rIn/rMt of an unheld value | **RESOLVED** | PS16; `pt-alloc-any-event` KILLED (9 failures, tag PS16) |
| R770-1 F2: FailureInformation and latency changed before the settle | **RESOLVED** | PS17; `pt-fcode-first-only` (1), `pt-lat-on-alloc-only` (3) and `pt-type-on-alloc-only` (1), each KILLED by its PS17 check |
| R770-1 F3: A8 on a held value; rLv on LV | **RESOLVED** | PS18 with `seed-on-teardown` KILLED (2); PS19 with `pt-rlv-on-lv-ends` KILLED (2) |
| R770-1 F4: no Flush!/Begin! on the port registrars | **RESOLVED for the port registrars and unbound sinks; cause RETAINED, narrowed, as R769-2 F1** | `link_up_i` is wired internally only: the `KL_srp_top` diff from main is one connection line, its port list is byte-identical, and `hdl/top` and the register map are unchanged. PS23 and LK1 are graded, with `pt-link-flush-dropped`, `link-begin-dropped`, `unarmed-link-flush-dropped`, `keep-on-link-clock` and `top-listener-link-unwired` all KILLED by name. The same-stream keep path carries a settled-through registration across a re-bind (F1) |
| R770-1 F5: `:759`, `:805` timing copies | **RESOLVED**, exact text | `:767` "one `T-MRP-LEAVEALL` later"; `:845` "after a random `T-MRP-LEAVEALL` draw" |
| R770-1 S1: area | taken | below |

## Focus items

1. **Same-stream re-bind**: met, as R769-1 F1 above.
   - PS20 and its arm are caught by name.
   - A different stream (P6, PS5) or a withdrawal (PS21) leaves no stale registration.
   - Exception: a registration held through a link change (F1).
2. **Link change**:
   - Every port registrar goes to MT on either edge of `link_up_i` (`pt_next`: `link_ev_w` has the highest
     priority).
   - So does every unbound sink registrar.
   - Neither a seed nor a keep happens on the link's clock: `seed_reg_w` is built from `pt_nreg_w`, and
     `keep_v_w` requires `!link_ev_w`.
   - The wiring is internal only. LK1 and its arm are graded.
   - The settled-sink exclusion leaves F1.
3. **PS16-PS23 and their arms**: all four named arms are KILLED by their named checks, with counts equal to
   the README cells and the author's receipt: `pt-fcode-first-only` 1, `pt-lat-on-alloc-only` 3,
   `seed-on-teardown` 2, `pt-rlv-on-lv-ends` 2.
4. **The 13-bit leave deadline** (`:497-501`, `:680-684`, `:741`, `:1518`):
   - `PT_DW_C = $clog2(5001) = 13`, `PT_SLACK_C = 8191 - 5000 = 3191`.
   - The age reads 3192 (-5000) when LV starts and is not expired. It reaches 0 on the deadline's
     millisecond. `now_ms_i` is the timer service's free-running +1 counter (`KL_pp_timer_service.sv:96`).
   - The seeded arm's deadline is rebuilt as `now + (dl13 - now13)`. The remaining time is 1-5000, so this
     equals the original 32-bit absolute deadline exactly.
   - Probe P3 covers 8 bases across 13-bit and 32-bit wraps (`0xFFFFFFFF`, `0xFFFFFFFF - 2500`,
     `0xFFFFE000 + 4000`, `8192·k - 1`, and others), with settles at +0, +1, +4999 and +5000. In every case
     the arm deadline equals base + 5000 (mod 2^32), and nothing is seeded at +5000.
   - Probe P4 steps `now_ms_i` one ms at a time across the 13-bit wrap: LV at deadline - 1, MT at the
     deadline.
   - `pt-expiry-sign-bit` and `seed-deadline-rebuild-drops-now` are KILLED.
   - The decision rule, smaller at 2x2 and 8x8, is met on the `KL_srp_top` receipts: -67 LUT and -38 FF;
     -83 LUT and -152 FF.
5. **The stale-expiry guard decision**:
   - The guard is kept, and §6.4's sentence is corrected as ruled.
   - The integrator text on the path's reach, with the shipping N = 2, is in `integrator.md:618-632`. The
     1x1 product binds two Stream Inputs, its stream and CRF, per 10 §5.1.
   - That text's last sentence is F1.
6. **Area**:
   - I recomputed the published stat files of `a9e84b66`, `04856e48` and `a2fce43`.
     - 2x2: 11,475, 12,690 and 13,193 LUT; 4,812, 5,372 and 5,334 FF. That is +503 LUT and -38 FF against
       round 1.
     - 8x8: 23,046, 27,399 and 28,193 LUT; 9,236, 11,376 and 11,224 FF.
     - INV: 2,811, 2,944 and 2,875 at 2x2; 3,483, 4,411 and 4,037 at 8x8.
   - These match the PR table and 10 §5.1's "1,718 LUT, 64 inverters and 522 flip-flops" and "5,147 LUT,
     554 inverters and 1,988 flip-flops".
   - I re-ran `srp_top_2x2` at the head with the same flow. The stat file is byte-identical to the
     author's (`receipts/area-head-a2fce43/srp_top_2x2.stat`).
   - The FF formula N x 244 + (1 + log2 N + 32) + 1 matches the listener's -37 (2x2) and -151 (8x8)
     against round 1. The link FF merges at `KL_srp_top`: -38 and -152.
7. **Residue texts**: both are applied exactly (table above).

## Lens evidence

### Conformance — UNCLEAN (F1)
- Table 10-4 on the port registrars:
  - registering events go to IN;
  - leavetimer! takes LV to MT;
  - rLv takes IN to MT (Δ13) and is `-x-` in LV;
  - rLA!/txLA! take IN to LV;
  - Flush! and Begin! go to MT.
  These are in `pt_next`, with the sink registrar's priority, graded by PS6-PS9, PS16, PS19 and PS23.
- The kept registration follows Table 10-4 while unbound (PS21, PS22) and raises nothing, per F10.5
  (PS22).
- §10.7 and §10.7.8 (state independent of application interest) hold for the same-stream re-bind (PS20).
- Milan §5.3.8.9 exact triple: PS20's DA and VLAN misses.
- Acceptance 4: no top-level port, parameter or register-map change. `hdl/top` is unchanged against main,
  and `KL_srp_top`'s port list is unchanged.
- Open: a sink registrar settled through a link change is not flushed, and the keep path now carries it
  across a re-bind (F1).

### RTL — UNCLEAN (F1)
- I read the round-2 RTL diff in full (`KL_srp_listener_fsm.sv` +148/-58, `KL_srp_top.sv` +1).
- The keep compare reuses `cset_w` plus one {DA, VLAN} compare per sink.
- `keep_v_w` excludes:
  - the sink's own leavetimer! on the settle's clock (`kexp_w`, with the stale-arm guard);
  - a link change.
- On the A15 of another value, the A8's teardown is unchanged (cancel when LV, clear the data). The seed's
  `T_ARM_C` overrides the cancel later in the block, as at round 1.
- `acc_latency_o` and `dbg_reg_state_o` are gated on `armed_r`. `msrp_fail_bridge_o` stays ungated by
  contract (S2).
- `link_q_r` resets to 0, so the first clock after reset with the link up is a Begin! on registrars that
  are already MT. That is harmless.
- Lint at the head, pinned Verilator 5.050: 41 of 41 `LINT OK`, rc 0 (`receipts/lint_hdl_5050.log`).
- The comment rule holds: no lane label, round, reviewer ID or comment ID in any added hdl/ or tb/ line.
  The only match was `la_rx_lanes`, the MRP LeaveAll lanes.

### Robustness — UNCLEAN (F1)
- The deadline is wrap-safe across 13-bit and 32-bit wraps (P3, P4).
- No stale registration survives another-stream re-binds (P6) or withdrawals (PS21).
- The latest FailureInformation is applied at a keep (P7).
- The unbound sink's ungated fail-bridge level is gated at its only consumer (S2).
- F1's stale-after-outage path is open.

### Tests — UNCLEAN (F1)
- My SRP-campaign run, `--only` the 46 labels whose named check is a PS or LK row (48 entries, `--jobs 8`,
  pinned 5.050):
  - 50 of 50 PASS: controls `srp_stream_fsms suite` (1,500 of 1,500) and `srp_top link` (2 of 2), plus
    48 entries KILLED by their named checks.
  - Every label's failure count and tags equal the author's full-run receipt (46 of 46 SAME,
    `receipts/campaign-compare-vs-author.txt`).
- The README count cells for the new arms equal those counts.
- `presettle-removed` (36, named PS3) and `pt-seed-dropped` (26, named PS5) are correctly renamed for
  acceptance 5.
- Open: no row grades a sink settled through a link change and then re-bound to the same stream (F1).
  PS23's kept case starts from an unbound sink.

### Docs — UNCLEAN (F1)
- 10 §6.4, the integrator guide, the stream-FSM README PS23 sentence and PR item 4 carry the falsified link
  claim (F1).
- Otherwise:
  - F10.5 arcs, §5.1 storage rows and measured cost, REQ-ACMP-018, 02 §4 and 05 A15 are consistent with
    the RTL;
  - the residues are applied exactly;
  - R1 and R2 are wording residue.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `KL_srp_listener_fsm.sv` pt_match/pt_next/pt_seed/settle_keep/reg_plane/status_map; `KL_srp_top.sv:622`; Table 10-4 rows vs PS6-PS9, PS16-PS23, LK1; probes P1, P6-P8 | R769-2 (delta 04856e48..a2fce43; rest R769-1) | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| RTL | UNCLEAN (F1) | full round-2 RTL diff; `hdl/top` and the `KL_srp_top` port list vs main; lint 41/41 at pinned 5.050; comment-rule scan | R769-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Robustness | UNCLEAN (F1) | probes P1-P8; timer-service ms counter; GET_STREAM_INFO gating | R769-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Tests | UNCLEAN (F1) | PS16-PS23 and LK1 code; 46-label campaign run (50/50) vs the author's receipt; round-1 probe 1,502/1,502; mutants.py coverage list (PS 23, LK 1) | R769-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Docs | UNCLEAN (F1) | `10_srp_engine.md`, `integrator.md`, `02_interfaces.md`, `05_acmp_engine.md`, `00_MILAN_COMPLIANCE_REVIEW.md`, both bench READMEs, PR body; residue texts | R769-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |

## Published evidence checked

- **Integrity**: 1,534 files under `author-r2/` and `reviews/R769-1/` of `review-evidence/pp212-r1` equal
  their `published_sha256` in `MANIFEST.json`, with 0 bad and 0 missing
  (`receipts/evidence-manifest-check.txt`).
- **Commit signature**: the evidence commit shows no signature status locally. Integrity rests on the
  manifest digests.
- **Sweep receipt** (`processor/head-a2fce43`): every rc is 0. 36 suites, 1,030,993 checks, 0 failing;
  srp_stream_fsms 1,500, srp_top 8,671, pp_top 11,064. My controls reproduce the srp_stream_fsms and
  srp_top `link` figures.
- **SRP campaign receipt**: 275 of 275, coverage 166 of 166, rc 0. The control/arm split stated in the PR
  body is wrong (R1).
- **Area receipts**: consistent and reproduced (focus item 6).
- **Spot-checked only**: the parent-consumer-gate receipts. I did not re-run them.

## Real limits

- **Banks not run here**: I ran no full processor sweep, no other campaigns (ACMP, AECP, GSI, CTR, name
  write, dispatch, notification, D3), no 8x8 area run and no parent gates. For those I relied on the
  author's published receipts, verified by digest. The delta does not touch `tb/pp_top` or its arms.
- **Probes are disposable bench code**: they ran only in `tb/srp_stream_fsms` at the listener level. F1 is
  shown at the listener face, not end to end through `tb/pp_top` and an ACMP re-bind.
- **No hardware**: physical calibration is NOT RUN. No hardware, Vivado route or hosted/act job was
  executed by this review, and field skips are not hardware proof.
- **No manager source bank** runs at this exact head, and I claim none.
- **Clone restored**: after the probes the clone is at the exact head, with:
  - a clean worktree and index;
  - the index equal to the tree (modes, blobs and paths);
  - every tracked file's blob equal to its index entry;
  - no gitlinks (none are required).

  One ignored `tb/common/__pycache__/` that the campaign driver's import created was removed.

## Pending manager duties

- **Parent route**: the parent-route comment says "Round 2 must not grow it beyond this without a new
  route". This head's `KL_srp_top` yosys LUT figure is +503 (2x2) over round 1, at 99.94 % slice packing
  on dev. A Vivado place-and-route of this head, or of the fixed head, at the shipping shape is still owed
  and is the manager's.
- **Merge candidate**: the current-dev merge candidate (builder and native banks) at the merge turn, from
  base `a9e84b66`, live dev `604899c0`.
- **Pin bump**: the parent's ROM-digest rows and documented-pin update for the bump.
- **Acceptance**: hosted/act acceptance.
- **Merge rule**: two independent POSITIVE reviews before merge.
- **Residue checklist**: carry R1 and R2.

## Receipts

Every file below is listed in `MANIFEST.sha256`:

- `receipts/srp-campaign-issue212-arms.log`, `.rc`
- `receipts/campaign-compare-vs-author.txt`
- `receipts/campaign-control-srp_stream_fsms-suite.log`
- `receipts/probe-srp_stream_fsms.log`, `.rc`, `.diff`
- `receipts/r769-1-probe-at-a2fce43.log`, `.rc`
- `receipts/area-head-a2fce43/srp_top_2x2.stat`
- `receipts/area-head-a2fce43.out`, `.rc`
- `receipts/lint_hdl_5050.log`, `.rc`
- `receipts/evidence-manifest-check.txt`
- `receipts/tool-identity.txt`

Scripts:

- `probes/r769_2_probe_block.cpp`
- `probes/make_probe_tree.sh`
- `probes/r769_1_probe_rebind_same_full_table.py`
- `probes/area_some.sh`
- `probes/compare_campaign.py`
- `probes/verify_evidence_manifest.py`
- `probes/RUN.md`

R769-2 FINISHED
