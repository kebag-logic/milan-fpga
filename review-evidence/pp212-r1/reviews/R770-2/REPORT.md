[R770] NEGATIVE - exact head a2fce4326ebdaf398a1920d79a664d44e6f1e5dd

# R770-2: external independent review of PR #213 (issue #212), round 2

- **Head:** `a2fce4326ebdaf398a1920d79a664d44e6f1e5dd`, tree `40d4bfd5d553663d3c21fa9f38862b57c77acb84`. The clone was verified at both before and after the probes.
- **Base:** main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Round-1 head `04856e48`.
- **Delta judged:** `04856e48..a2fce43`, six commits, added on top with no rebase. Round 1 is an ancestor of the head.
- **Scope rebuilt from:**
  - the issue body and its comments, including the round 2 assignment (issuecomment-6651608145);
  - the PR body and the PR thread, including the parent-route comment (issuecomment-6652128599);
  - `docs/README.md`;
  - the diff and its history;
  - the published packet `kebag-logic/milan-fpga@dbbbb05a…/review-evidence/pp212-r1/author-r2`.
- **Process files:** this repository has no `AGENTS.md` or `CONTRIBUTING.md`.
- **Round 1 reports:** I read them only after my own pass over the RTL and test delta: R770-1 (issuecomment-6651549338) and R769-1 (issuecomment-6651603962).

## Verdict

NEGATIVE, on one MINOR finding (F1).

What holds:
- Every round 1 finding is resolved at its cause, except one residual path of R770-1 F4 (F1 below).
- The 13-bit deadline keeps Milan Table 4.3 timing exactly, and it is wrap-safe.
- The area table matches the receipts. My own synthesis at 2x2 reproduces it bit for bit.
- Every new arm I ran is KILLED by its named check, with the README's failure count.

F1 is the residual path:
- A sink that stays settled through a link down/up keeps its pre-outage registration. That is a documented, pre-existing limit.
- Round 2's same-stream keep now also carries that registration through an A8 and a re-bind.
- At main, the re-bind cleared it.
- So a registration from before a link loss is applied at a settle after it. The architecture text, the integrator guide and the PR's design item 4 say this cannot happen, and no row grades it.

There is one RESIDUE (R1) and two SUGGESTIONs.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - a pre-outage registration survives a link change through a sink settled across it, then is kept at a same-stream re-bind

- **Where:**
  - `hdl/srp/KL_srp_listener_fsm.sv:1480-1487`: the link flush is `if (link_ev_w && !armed_r[s])`, so a settled sink's registrar is not flushed.
  - `hdl/srp/KL_srp_listener_fsm.sv:870-876`: `keep_v_w` keeps any non-MT registration on the same triple at the A15.
  - `docs/architecture/10_srp_engine.md:831-836`: "so no registration from before a link change is seeded or kept after it".
  - `docs/guides/integrator.md:630-632`: "A link down or up ends every registration a later settle could take, so after it each input waits for its talker's next declaration".
  - PR body, design item 4: "so nothing registered before a link loss is seeded or kept after it".
- **Evidence (reviewer probes, pinned Verilator 5.050, exact head):**
  - **XP2** (`receipts/probe-srp_stream_fsms.log`, `receipts/probe-summary.txt`). Sink 0 settles and registers V. The link goes down, then up. While settled it still reports V registered (as documented). After an A8 and an A15 on the same triple, the result is `reg 1 tk 1 state 1`: EVT_TK_REGISTERED and ADVERTISE for a registration made before the link loss.
  - **XPB at base `a9e84b66`** (`receipts/probe-rebind-base-a9e84b66.log`). The same settle, A8 and A15 with no link change gives `reg 0 tk 0`: at main, a re-bind ended the registration.
  - **XPB at head** (`receipts/probe-rebind-head-a2fce43.log`) gives `reg 1 tk 1`, the intended keep.
  - Together these show the new path: the round-2 keep extends the settled sink's stale, pre-outage registration across a re-bind. Main cleared it there.
  - XP3 covers an A8 on the LINK_DOWN clock. There the LINK_UP flush still ends the registration (`reg 0 tk 0`). The open path needs the sink settled at both edges.
- **Authority:**
  - IEEE 802.1Q-2022 Table 10-4: Flush! and Begin! take a registrar to MT.
  - The round 2 ruling on R770-1 F4 ("fix, not a deviation").
  - R770-1 F4's stated impact: a pre-outage registration applied at a settle after the link returns, with Listener Ready, EVT_TK_REGISTERED and SETTLED_RSV_OK for an attribute the current link has not registered (example: a talker that rebooted during the outage).
  - The PR's own design item 4 and the 10 §6.4 text quoted above.
- **Impact:**
  - Unbind and re-bind is the operator's way to restart a stuck stream. After an outage it now re-applies the stale registration instead of clearing it.
  - The stale state lasts until the talker withdraws or this participant's LeaveAll ages it out: one T-MRP-LEAVEALL plus T-MRP-LEAVE.
  - Three texts say the opposite, and no PS/LK row covers the case. A change in this area would land green either way.
- **Required outcome:** one of the following (a maintainer scope choice):
  - (a) An A15 does not keep a registration that has lived through a link change. For example, a per-sink bit set by `link_ev_w` while armed and cleared by the sink's next registering event, which `keep_v_w` requires clear: about N flip-flops and a few LUT. Add a PS23 row (settled, registered, link down and up, A8, A15 on the same triple: nothing kept until the talker's next declaration) and an arm that fails it by name.
  - (b) Flush every sink registrar on a link change per Table 10-4, settled or not. This is wider: it changes what a settled sink reports across an outage. It needs its own rows and arms, and a ruling on the Lv indication and the class-C strobe.
  - (c) A recorded maintainer decision that this path is accepted. Then correct `10_srp_engine.md:831-836`, `integrator.md:630-632` and PR design item 4 / Limits to say that a sink settled through a link change keeps its registration, also across an A8 and a re-bind to the same stream.
- **Verification:** under (a) or (b), XP2 gives `reg 0 tk 0` and the new arm is KILLED by its named check. Under (c), the three texts carry the qualifier.

### R1 - RESIDUE - Docs - T-MRP-LEAVE's value copied outside F08.1 in the new text

- **Where:**
  - `docs/architecture/10_srp_engine.md:226`, storage row: "leave deadline 13 (`$clog2(LEAVE_MS_P + 1)` at 5000 ms)".
  - `docs/architecture/10_srp_engine.md:782`: "`$clog2(LEAVE_MS_P + 1)` bits of `now_ms_i`, 13 at 5000 ms".
  - Both were added in this delta.
- **Authority:** `docs/README.md:70-71` (single-source rules: timing values only in F08.1). This is the same class as round 1's F5, which this round fixed.
- **Exact fix:**
  - At `:226`, "at 5000 ms)" becomes "at the F08.1 `T-MRP-LEAVE`)".
  - At `:782`, "13 at 5000 ms:" becomes "13 at the F08.1 `T-MRP-LEAVE`:".
- **Why RESIDUE:** wording only. It changes no figure (13 bits is unchanged), test, code or claim.

### S1 - SUGGESTION - Tests

PS20 grades the Talker Failed same-stream re-bind only before tx! (`tb/srp_stream_fsms/sim_main.cpp:3220-3236`). The Advertise variant runs both before and after the old Lv. A Failed variant after the old Lv would cover the Asking Failed New on the keep path. No verdict effect: the keep path does not depend on the type (`keep-declares-seed-type` is already KILLED on PS20).

### S2 - SUGGESTION - Conformance (follow-up)

Apart from F1, a settled sink's registrar still has no Flush!/Begin!. This is pre-existing, documented at `10_srp_engine.md:835-836` and in the PR limits, and outside issue #212. Suggest a tracking issue against Table 10-4 if F1 is resolved by (a) or (c).

## Round 1 findings at this head (judged at cause)

| Finding | Ruling | At this head | Evidence |
|---|---|---|---|
| R769-1 F1, re-bind to the same stream loses its registration when the table is full | option (a) | **Resolved.** The A8 leaves the registrar running on the record's triple, unpublished. An A15 on the same {stream_id, DA, VLAN} keeps it whatever the table holds. PS20 runs before and after the old Lv. Another DA or VLAN is another value. No stale registration survives a re-bind to a different stream (PS20 misses; my XP4 binds away and back; XP6 cancels the slot of an LV registration re-bound elsewhere) or a withdrawal while unbound (PS21) | `rebind-same-not-kept` KILLED (PS20, PS21, 4 failures), plus `keep-ignores-da`, `keep-ignores-vlan`, `keep-declares-seed-type`, `keep-latency-strobe-dropped`, `keep-ignores-expiry` and `unarmed-registrar-deaf`, all KILLED by name. XP5: a kept LV registration keeps its own slot and ends at its deadline |
| R770-1 F4, no Flush!/Begin! on the port registrars | fix | **Resolved for the port registrars and the unbound sinks** (`pt_next` `link_ev_w` first; `:1484`). The input is internal: `KL_srp_top`'s port list is byte-identical to main (sha256 of the module header at both commits is `3e55ab87…`), and `protocol_processor_top.sv` and the register map are unchanged. **Residual path open: F1** | PS23 (5 checks) and LK1 pass. `pt-link-flush-dropped`, `link-begin-dropped`, `unarmed-link-flush-dropped`, `keep-on-link-clock` and `top-listener-link-unwired` are each KILLED by name |
| R770-1 F1, rLv/rIn/rMt of an unheld value | test | **Resolved.** PS16 covers all three events for both types, plus the refused-then-freed case | `pt-alloc-any-event` KILLED (PS16, 9 failures) |
| R770-1 F2, FailureInformation and latency changed before the settle | test | **Resolved.** PS17 covers code, bridge and latency, Advertise latency with one strobe, and Advertise turned Failed | `pt-fcode-first-only` (1), `pt-lat-on-alloc-only` (3) and `pt-type-on-alloc-only` (1), each KILLED on its PS17 check |
| R770-1 F3, A8 on a held value; rLv on LV | test | **Resolved.** PS18 checks no EVT_TK_REGISTERED, unregistered or latency strobe, NONE, latency 0 and no timer op. PS19 checks LV kept with the LeaveAll's deadline, ending at it | `seed-on-teardown` KILLED (PS18), `pt-rlv-on-lv-ends` KILLED (PS19) |
| R770-1 F5 (RESIDUE), `10:759`, `:805` | reviewer text | **Applied exactly**: "one `T-MRP-LEAVEALL` later" (`:767`) and "after a random `T-MRP-LEAVEALL` draw" (`:845`) | doc read |
| R769-1 R1 (RESIDUE), `10:222` | reviewer text | **Applied exactly** (`:226`): "the value, type and payloads written with a registration, the leave deadline at the LeaveAll that starts LV; all read only while it is not MT" | doc read |
| R769-1 S1, practical reach | taken | **Done.** Integrator §8 (`integrator.md:618-632`) and 10 §6.4 state it with the shipping N = 2, which I confirmed in the parent's generated shape (`ADP_LISTENER_SINK_C = 2`, `endstation_ax7101_1x1_tdm8`). The link sentence there is part of F1 | doc read |
| R769-1 S3, stale-expiry guard | keep the guard, correct §6.4 | **Done.** `10:807-817` now says the guard ends when the arm is issued, describes the window across the `KL_srp_top` and processor-top queues, and gives the cost of an exact guard. The PR limits match. The decision is within the ruling | doc read; PS15 still passes |
| R769-1 S2 / R770-1 S1, 13-bit deadline | only if smaller at 2x2 and 8x8 | **Taken and correct**: see the next section | `pt-expiry-sign-bit` (6) and `seed-deadline-rebuild-drops-now` (4) KILLED |

My round 1 probes, re-run at this head as campaign arms, now each fail by name:
- `pt-alloc-any-event`, `pt-fcode-first-only`, `pt-lat-on-alloc-only` and `seed-on-teardown`;
- `pt-rlv-on-lv-ends`;
- `pt-type-on-alloc-only` (`receipts/campaign-r2-arms.summary.txt`).

## The 13-bit leave deadline (focus 4)

`PT_DW_C = $clog2(5001) = 13` and `PT_SLACK_C = 8191 - 5000 = 3191`. An entry enters LV only from IN at a LeaveAll, with `dl = now + 5000 (mod 8192)`. Its age `now - dl` therefore starts at 3192. It stays above the slack until `now = t0 + 5000`, where it is 0 and the entry expires.

That is exact T-MRP-LEAVE. It also holds because:
- `now_ms_i` is `KL_pp_timer_service`'s free-running `+1` counter (`hdl/common/KL_pp_timer_service.sv:96`);
- expiry is outranked only by events that leave LV, so the age can never wrap past the window.

The seeded arm is `now + (seed_dl - now[12:0])`, which is the entry's absolute deadline.

**XP1** checks this directly. It covers t0 in {100000, 5192, 8191, 8192, 3191, 3192, 54151, 2^32-2501, 2^32-1, 0}, crossing both the 13-bit and the 32-bit wrap, and settle offsets {0, 1, 2000, 3191, 3192, 4999, 5000, 5001, 8191}.
- Every offset below 5000 seeds LV with an arm deadline of exactly `t0 + 5000`.
- Every offset from 5000 up finds the entry expired.
- 90 of 90 checks pass.

## Area (focus 6)

The packet's `area/head-a2fce43` stat files sum to the PR table:
- `KL_srp_top` 2x2: LUT1-6 = 13,193 and FF = 5,334, which is +503 LUT and -38 FF against round 1's 12,690 / 5,372;
- 8x8: 28,193 / 11,224;
- the 13-bit decision: `r2` 13,260 / 5,372 against `r2dl13` 13,193 / 5,334 at 2x2, and 28,276 / 11,376 against 28,193 / 11,224 at 8x8, so smaller at both shapes.

My own run (`scripts/area_2x2.sh`: sv2v 0.0.13, yosys 0.66, the author's lowering) reproduces `KL_srp_top` 2x2 at 13,193 LUT / 5,334 FF and the listener at N = 2 at 5,892 / 1,456 exactly (`receipts/area-head-2x2/`).

The FF arithmetic checks out:
- N × 244, where 244 = 2 + 124 + 1 + 32 + 72 + 13;
- -19 FF per entry, plus 1 link flip-flop in the listener, which merges with the Domain FSM's in `KL_srp_top`.

The manager's parent-route comment says that round 2 must not grow beyond the round-1 route "without a new route". The head's yosys LUT figure is +503 over round 1. That is a pending manager duty, below.

## Executed evidence

All runs used pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, identity checked) on fresh local clones of the exact head under the packet's scratch directory.

| Run | Result | Receipt |
|---|---|---|
| `tb/srp_stream_fsms` (walk arms at 4 shapes plus the suite) | rc 0; suite **1,500 / 1,500** (equals the PR) | `receipts/suite-srp_stream_fsms.log` |
| `tb/srp_top` | rc 0; **8,671 / 8,671**, LK1 included (equals the PR) | `receipts/suite-srp_top.log` |
| SRP campaign, `--only` the 38 issue-#212 arms (new and re-cut), `--jobs 8` | rc 0; 41 / 41 (2 controls plus 39 entries); every arm KILLED by its named check; all 38 failure counts equal the `tb/srp_top/README.md` cells | `receipts/campaign-r2-arms.{log,summary.txt,readme-compare.txt}`, `receipts/campaign-r2-arms/*.log` |
| Reviewer probes XP1-XP6 added to a scratch copy of the suite | 1,593 / 1,593 (1,500 plus 93), with info lines XP2 and XP3 | `receipts/probe-srp_stream_fsms.log`, `scripts/r770_probes.inc`, `scripts/make_probe_tree.sh` |
| XPB at base and head | base `reg 0 tk 0` (1,435 / 1,435); head `reg 1 tk 1` (1,500 / 1,500) | `receipts/probe-rebind-{base-a9e84b66,head-a2fce43}.log` |
| `tb/pp_top` `--acmp-only` (the AS phase: AS7, AS8, AS9) | rc 0; 62 checks, 0 failures | `receipts/suite-pp_top-acmp-only.log` |
| `tb/pp_top` full `make run` | **NOT COMPLETED**: stopped by my own 590 s limit after the build, during the run (rc 124). The author's sweep receipt shows 11,064 / 11,064 | `receipts/suite-pp_top.log` |
| yosys area, 2x2 | as above | `receipts/area-head-2x2/` |
| Published packet integrity | all 1,466 `author-r2/` files match `MANIFEST.json` `published_sha256`; none missing or unlisted | `receipts/evidence-manifest-check.txt` |

On the packet's integrity: it is a sha256 manifest, not a cryptographic signature. The evidence commit `dbbbb05a` is unsigned (git `%G?` = N). 92 entries are path-redacted, with differing original and published digests.

Spot-checked from the author's receipts (`processor/head-a2fce43`, bound to head and tree in `records/processor-records.txt`):
- `make check`, lint under 5.050 and 5.052, `syn/yosys/run.sh`, the elaboration guards and the REQ-tag checks: all rc 0;
- `run_suites.sh`: 36 suites, 1,030,993 checks, 0 failing;
- the full SRP campaign: 275 / 275, coverage 166 / 166;
- the scratch-parent consumer gate at pin `a2fce43` on dev `604899c0`: 27 job rc files, all 0, with ROM digests equal to main's.

Hosted at the exact head (read-only): `docs-gates` and `portability` were executed and succeeded (two runs each). `suites` was still in progress when read. The manager owns hosted and act acceptance.

## Lens notes (delta only; code the delta does not touch keeps its round 1 verdict)

- **Conformance:**
  - Table 10-4 on the port registrars: the link event first, then registering, then leavetimer!, then rLv (IN only; LV `-x-`), then LeaveAll.
  - Δ13 is kept, and an unbound registrar follows its value.
  - The F10.5 teardown edges carry no class-C strobe (armed-gated `ind_reg_w`/`ind_fchg_w`, cleared unregistered and latency strobes).
  - `tk_reg_state`, `acc_latency` and `dbg_reg_state` are armed-gated. `msrp_fail_bridge` stays ungated, but the top gates it by `tk_reg_state == FAILED` (`protocol_processor_top.sv:3605`).
  - Open: F1.
- **RTL:**
  - `keep_v_w` excludes a same-clock leavetimer! (`kexp_w`) and a link change.
  - A seeded LV arm overrides the settle's cancel (T_ARM after T_CANCEL in block order).
  - The unbound sink's `ind_unreg_w` withdraw request only clears `dcl_r`, which is already 0 (`:902`, `:1156-1160`).
  - `link_q_r` resets to 0, so the first clock after reset is a harmless Begin!.
  - Comment rule: a scan of every added line in `hdl/`, `tb/` and the drivers found no lane labels, lane names, rounds, reviewer IDs or comment IDs.
- **Robustness:**
  - The 13-bit wrap-safety relies on a +1 ms timebase, and that holds (XP1).
  - The stale-expiry window is documented as a limit.
  - Open: F1.
- **Tests:**
  - PS16-PS23 and LK1 match the rulings.
  - `presettle-removed` disables the seed, the keep and the one-walk declaration, and fails PS3 by name.
  - `pt-seed-dropped` now names PS5.
  - Open: F1 has no row. S1 is a suggestion.
- **Docs:**
  - Residues applied exactly.
  - §6.4, the integrator guide, 02 §4, 05 A15 and REQ-ACMP-018 are consistent with the code, except F1's sentence.
  - R1 is new residue.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | listener `pt_next`, `settle_keep`, `reg_plane`, `status_map`; `KL_srp_top` wiring; 802.1Q-2022 Table 10-4; Milan Table 4.3; probes XP1-XP6 and XPB | R770-2 (delta); R770-1 for untouched code | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| RTL | CLEAN | listener delta (+148 −58), `KL_srp_top` +1; port list hash; area reproduction | R770-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Robustness | UNCLEAN (F1) | link-change paths, kept LV slot (XP5), re-bind to another stream (XP4, XP6), 13-bit wrap (XP1) | R770-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Tests | UNCLEAN (F1) | PS16-PS23, LK1, `mutants.py` and 38 arms re-run, README counts, suites | R770-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |
| Docs | UNCLEAN (F1; R1 is residue only) | `10_srp_engine.md` delta, `integrator.md` §8, `02_interfaces.md`, `05_acmp_engine.md`, compliance review REQ-ACMP-018, the srp READMEs, PR body | R770-2 | a2fce4326ebdaf398a1920d79a664d44e6f1e5dd |

## Real limits

- No manager source bank ran at this head, and I claim none.
- I did not run:
  - the full `run_suites.sh` sweep, the full SRP campaign or the other campaigns (ACMP, AECP, GSI, CTR, name write, dispatch, notification, D3): for these I rely on the author's published, manifest-verified receipts;
  - the area figures at 8x8.
- My full `tb/pp_top` run did not complete within my time limit. Only its AS (ACMP) phase ran.
- Physical calibration was NOT RUN. Skipped field checks are not hardware proof.
- No Vivado route of this head exists.
- The published packet is digest-checked but not signed.
- The shipping N = 2 was read from the parent's tracked generated shape at the evidence commit, not from dev `604899c0`.

## Pending manager duties

- Rule on F1's option, (a), (b) or (c), and carry R1 to the residue checklist.
- Make a new Vivado route of the shipping shape with this head as the gitlink. The yosys LUT figure is +503 over the round-1 route that the manager published, and the manager's own condition requires a route.
- Run the current-dev merge-candidate builder and native banks at the merge turn: source base `a9e84b66`, live dev `604899c0`.
- Accept the hosted results (`suites` was in progress when read).
- Bump the parent pin with its ROM-digest rows and documented-pin update.

## Clone integrity after the probes

The review clone was never written; all probes ran in scratch copies.

At the end:
- `HEAD` is `a2fce43`; `git write-tree` gives `40d4bfd5…`, equal to the HEAD tree;
- the working tree equals the index, and the index equals HEAD; `git status --porcelain --ignored` is empty;
- the repository has no submodule gitlinks.

Receipt: `receipts/clone-integrity.txt`, which also carries the `ls-files -s`, content and `ls-tree` digests.

## Packet

- `scripts/` holds everything needed to reproduce: `run_all.sh`, `make_probe_tree.sh`, `r770_probes.inc`, `make_base_probe_tree.sh`, `r770_probe_rebind_base.inc`, `area_2x2.sh` and `verify_evidence_manifest.py`.
- `run_all.sh` expects clean clones named `clean`, `clean2` and `clean3`, plus the probe tree, under `scratch/`, and `VERILATOR` set to the pinned 5.050.
- Host paths in the receipts are redacted to `<home>`, `<scratch>` and `<tools>`.
- `MANIFEST.sha256` lists every published receipt.

R770-2 FINISHED
