[R729] NEGATIVE - exact head 9d509029de967c50de7527edf2b8869aa9db9074

# R729-1: independent internal review of FPGA-gPTP PR #95 (issue #94)

- Repository: Mister-M-alt/FPGA-gPTP, PR #95 "End the Pdelay_Req cease on a portEnabled toggle".
- Exact head `9d509029de967c50de7527edf2b8869aa9db9074`, tree `4d0c9d078cb2d575b100e23c6b34c2637c247594`. Source base `f97c1803`. Four commits.
- Review clone: detached at the exact head. It was never edited. Every probe ran in a disposable copy (see "Restoration").
- Inputs, in order:
  1. The repository guides. This repository has no AGENTS.md or CONTRIBUTING.md, so I read `README.md` and `docs/README.md` (truth order: RTL and generated microcode, then executable tests, then guides).
  2. The issue #94 body: clauses, Expected and Acceptance.
  3. The manager's assignment and the author's review-ready comment on #94, and the PR #95 body.
  4. `git diff f97c1803..9d509029` and its history.
  5. The published evidence `kebag-logic/milan-fpga@635234810f71ec72166d2ba226e483cfd247d2b1:review-evidence/gptp94-r1` (213 files).
  6. The parent sources at milan-fpga #805's head `e06ade31`, for the companion seam.
- No manager source bank exists at this head. None is claimed or inferred here. All execution evidence below is either this review's own runs (listed in MANIFEST.sha256) or the author's published receipts, and each item says which.

## Verdict

**NEGATIVE.** Two MINOR behavioural defects remain open. Both sit on the portEnabled paths this PR adds, both cite a clause, and both reproduce with a deterministic engine probe:

- **R729-F1.** After a warm reset during a cease, with the port low at reset release, the later rise does not end the Milan v1.2 4.2.6.2.5 cease. The port stays silent for the rest of the countdown, which is the issue's own symptom.
- **R729-F2.** A Pdelay_Resp_Follow_Up that arrives after the fall still pairs with the response armed before it. It publishes a new neighborPropDelay and commits while the port is NOT_ENABLED.

Apart from those two, the change does what the issue and the assignment ask:

- the port contract;
- the NOT_ENABLED leg on both edges;
- the transmit, credit and egress-claim gates;
- the rise's immediate request with lostResponses = 0;
- the two-exchange re-earn;
- the unchanged countdown exit;
- the ROM packing;
- the 15 new controls;
- the parent companion's wiring.

All of these are verified below. There is no RESIDUE. No prior public review finding exists on this PR.

## Findings

### R729-F1: a rise after a warm reset with the port low at release keeps the retained cease (MINOR)

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Location:**
  - `hdl/top/KL_gptp_engine.sv:1102` (`port_seen_r <= port_seen_r || port_en_r;`) and `:1107` (`if (port_seen_r && (port_enabled_i != port_en_r))`). Only an enabled sample arms edge detection, so the first rise after a release with the port low raises no event.
  - The design comment at `hdl/top/KL_gptp_engine.sv:154-160`.
  - The cease state is scratch that survives a warm reset, by design (`hdl/ucode/gen_gptp_ucode.py:364-378`). Issue #94 itself cites this as part of why the cease is stuck.
  - Docs: `docs/INTEGRATION.md:214-216` ("The first enable after reset raises nothing. The boot cadence already sends the first request.") and `docs/HDL_DEVELOPER.md:262`.
- **Authority:**
  - Milan v1.2 4.2.6.2.5: the cease ends when portEnabled toggles.
  - IEEE 802.1AS-2011 Figure 11-8 (Cor1, Cor2): `portEnabled && pttPortEnabled` leaves NOT_ENABLED only through INITIAL_SEND_PDELAY_REQ.
  - Issue #94 Expected: "Rising edge: INITIAL_SEND_PDELAY_REQ. One Pdelay_Req goes out on the next transmit opportunity".
- **Evidence:** probe D (`scripts/run_probes.sh`, `receipts/probes-head.txt`). Setup: enter the cease with two responders, then 1.3 s into the 3 s countdown assert a warm reset, hold the port low through release, and raise it 200 ms later.
  - Result: `R729 D low-at-release: first request 3000 ms after the rise` and `FAIL R729 D low-at-release: the rise ends the cease within one interval`. The cease ran out its countdown.
  - Same probe with the fall 2 cycles after release: `first request 0 ms after the rise`.
  - With the disposable candidate change in `receipts/probe3-candidate-fix.diff` (`port_seen_r <= 1'b1`, so the first post-release sample is the reference level), the same probe gives 0 ms (`receipts/probes-candidate-fix.txt`). The unmodified engine suite still passes with that change: 2002/2002 (`receipts/probe3-fullsuite.log`).
- **Impact:**
  - Trigger: a warm reset with the fabric kept and scratch retained, during a cease, with the port low at release. For example, a board-level reset that also restarts the PHY. The parent's `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` (milan-fpga `e06ade31`, `hdl/milan/milan_datapath.sv:3194`) is then low at release, because `i_link_up` is low.
  - Consequence: when the link comes up, no Pdelay_Req, asCapable or Sync follows for the rest of the cease countdown, up to about 5 minutes at the shipping default.
  - The documented contract says the boot cadence serves the first enable. It does not serve it when a retained cease is quiet.
- **Required outcome:** one of the following.
  - A rise seen after reset release from a port that was low at release ends a retained cease and sends INITIAL_SEND_PDELAY_REQ at once. The integration and HDL guides state the rule. An engine check covers a warm reset in a cease with the port low at release followed by a rise, and a planted control fails that check.
  - Or the maintainer records an explicit scope decision on #94 that this path is out of scope, and the guides state the limitation.
- **Verification:** `scripts/run_probes.sh <fresh clone at the new head>` prints `R729 D low-at-release: first request` at 1000 ms or less and no `FAIL R729 D` line. The repository's own new check fails under its control.

### R729-F2: a Follow_Up heard after the fall completes the exchange, publishes the delay and commits while NOT_ENABLED (MINOR)

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Location:**
  - `hdl/ucode/gen_gptp_ucode.py:2180-2203` (`prog_leg_noten`). NOTEN sets `S_PDGOT`, which stops a NEW response from arming. It leaves an armed `S_RSPSEQ`, `S_RSPSRC` and a standing `S_T1V` in place.
  - `_pdpost_pairing_gates` (`hdl/ucode/gen_gptp_ucode.py:2021-2070`) refuses a Follow_Up only on port number, armed sequenceId, armed responder and `S_CEASE`. It runs the arithmetic tail (`PDEPOCH`/`PDPAIR`, `:2006-2018`), which writes publish word 3 and COMMITs.
  - Docs: `docs/TEST_DEVELOPER.md:140` ("Sends and commits nothing while the port is disabled"). The PR body also states the contract "nothing commits while the port is down".
- **Authority:**
  - IEEE 802.1AS-2011 Figure 11-8 (MDPdelayReq, Cor1/Cor2, required by 11.2.15.3). NOT_ENABLED has no transition on rcvdPdelayRespFollowUp. neighborPropDelay is computed only when leaving WAITING_FOR_PDELAY_RESP_FOLLOW_UP.
  - Issue #94 Expected/Acceptance: on the falling edge the port is NOT_ENABLED.
- **Evidence:** probe A (`receipts/probes-head.txt`). Setup: a capable master sends its Pdelay_Req and the peer's Pdelay_Resp arrives. The port falls, and NOTEN commits asCapable FALSE. Then the matching Follow_Up arrives, with t3 200 ns earlier so a pairing would move the delay.
  - Result: `R729 A: pdelay before 601 after 701; commits after the FU 1`, plus `FAIL ... commits nothing` and `FAIL ... leaves the delay`.
  - The re-earn checks after the rise pass. The rise's own NOTEN clears the transient `S_PDOK = 1`, so asCapable is not raised early.
  - With the candidate's one extra NOTEN word (`WRST S_RSPSEQ = 0`): `pdelay before 601 after 601; commits after the FU 0`. The ROM image grows from 1,021 to 1,022 words shipping and from 1,022 to 1,023 seeded.
- **Impact:**
  - A disabled port publishes a neighborPropDelay from an exchange its state machine must ignore. It commits a publication generation during NOT_ENABLED, and it advances the rate-ratio window (`S_NR3`/`S_NR4`).
  - Reachable when portEnabled falls while a Follow_Up still reaches the engine: the `LINK_CTRL[0]` administrative disable with the PHY still receiving, or a Follow_Up already inside the receive path when the link drops.
  - This is focus item 4, a toggle during an outstanding response. None of the four new phases covers this ordering: phase 46 covers a response *we* build, not one we receive.
- **Required outcome:** in NOT_ENABLED no received Pdelay_Resp_Follow_Up pairs, publishes or commits. For example, NOTEN disarms the outstanding exchange, or PDPOST refuses while the port is disabled. An engine check covers a Pdelay_Resp before the fall and its Follow_Up after it, and a planted control fails that check. The test guide's statement then holds.
- **Verification:** `scripts/run_probes.sh <fresh clone at the new head>` prints `commits after the FU 0` with an unchanged delay and no `FAIL R729 A` line. The new repository check fails under its control.

No RESIDUE. In the reviewed delta, no source comment shows a bench lane label, lane name, review round, reviewer ID or issue-comment ID (checked by a pattern search over every added line of `hdl`, `tb`, `bench`, `syn`, `scripts` and `docs`).

### Not a finding (recorded)

- **Cor2 reset of the rate ratio and sequence counter.** INITIAL_SEND_PDELAY_REQ's `neighborRateRatio = 1.0` and `pdelayReqSequenceId = random()` (Cor2) are not done. The PR records this openly. The assignment and the issue's acceptance do not ask for it. The ratio stays a valid measurement across a short outage, and the existing stale-window guard covers a long one.
- **Slot 7 now runs NOTEN.** The slot dispatch's default branch now sends slot 7 to NOTEN as well as slot 6. No code arms timer slot 6 or 7 (the ROM arms slots 0-5, and the RTL arms slots 0 and 2), so this path is unreachable.

## Lens evidence

### Conformance (UNCLEAN: R729-F1, R729-F2)

- **Port.** `port_enabled_i` stands for 802.1AS-2011 10.2.4.11 portEnabled. The parent drives `eff_link_w`, so a link loss or an administrative disable is a portEnabled fall.
- **Falling edge.**
  - NOTEN clears `S_CEASE`, `S_CEASECNT`, `S_MULTI`, `S_IVMULTI` and `S_RSP1`. It sets `S_PDGOT`, so the next judgement computes `S_PDLOST = 0`: lostResponses restarts at zero.
  - Through PDPAIR's `bad` tail it clears `S_PDOK` and asCapable and commits.
  - The RTL asCapable hook then expires the Announce receipt watch, as for any asCapable fall.
  - Phase 45 shows asCapable falling with a commit within 2 ms. The issue's own estimate before the change was about 4 s.
- **Rising edge.**
  - NOTEN runs again, then the queued slot-0 beat. One Pdelay_Req goes out at once: phase 44, and probes B1/B3 measured 286-288 cycles at 2 MHz.
  - The cadence restarts from that request. The cease is not resumed.
  - Unanswered, only the fifth loss after the rise commits asCapable FALSE (Figure 11-8 RESET with Cor2).
  - Answered, asCapable needs two exchanges (Milan v1.2 4.2.6.2.4), in phases 44 and 45 and in probes A, B1 and B3.
- **Countdown exit.**
  - The cease entry now ends in NOTEN's tail. Its effects equal the old block's: `S_PDOK` 0, flags without asCapable, COMMIT, `S_IVMULTI` and `S_RSP1` 0.
  - `S_CEASE` is written from RB, which holds `S_IVMULTI == 1` on that path. So `S_CEASE` still has one setter, and the invariant at `gen_gptp_ucode.py:364-378` holds.
  - Phase 47 measures 5 s with the 3 s image. With the 5-minute default the formula is `max(1, 300000 // 1000)` = 300 beats plus two, giving 302 s, the figure the issue saw on hardware.
- **Transmission while disabled.** A disabled port sends no Sync, Announce or Pdelay frame (10.3 DisabledPort). The initiating beats read no credit, every SEND is dropped, and both egress claims read empty (phases 44-46).
- **Open:** F1 (a rise after a warm reset with the port low at release) and F2 (receive-side pairing in NOT_ENABLED).

### RTL (UNCLEAN: R729-F1, R729-F2)

- **Port level.** `port_en_r` registers `port_enabled_i` once. No synchroniser is needed: in the parent, `eff_link_w` is combinational from axis_clk registers and the SoC-synchronised `i_link_up`, and the shadow and engine run on `axis_clk` (`milan_datapath.sv:8851`). The existing `eff_link_w` consumers (link counters, ADP) already treat it as that domain.
- **Edge logic.** It matches the stated intent:
  - a fall withdraws an owed beat, and a later edge re-raises NOTEN;
  - a same-cycle push and edge resolves to the edge, because the edge assignment comes later;
  - the portEnabled events take the lowest push priority, behind the parser and the timer, and wait while the queue is full.
- **Gates.**
  - Credit: `tx_credit_i && port_en_r`, `KL_gptp_engine.sv:799`.
  - SEND: `resp_send_w && port_en_r`, `:1138`.
  - Claims: cleared after the micro-code writes in the same block, so the clear wins (`:1079-1082`). The held-Pdelay_Req guard (`pdreq_block_w`) reads the cleared claim, so it cannot deadlock while the port is disabled.
- **Dispatch and ROM.** Slot 6 is dispatched to NOTEN (`gen_gptp_ucode.py:1523-1524`). No code arms timer slots 6 or 7. All four tracked ROM images regenerate byte-identical from the generator:
  - engine `--clk-hz 2000000 --cease-ms 3000`;
  - tsngen `--clk-hz 2000000`;
  - ucpu default;
  - ooc default.

  Usage is 1,021 words shipping and 1,022 seeded, the same as at base. Only RESUME and PDPAIR move in the packing.
- **Lint.** `make lint` rc 0 with no `%Warning` (pinned Verilator 5.050). `syn/ooc/check_ooc_clock.py --selftest` PASS (30 arms).
- **Area:** author receipts only, since no Vivado is available here. Placed figures: 4,874 LUTs, 3,459 FFs and 1,659 slices at head, against 4,943 / 3,455 / 1,663 at base, with WNS +0.513 ns (`author/receipts/area/*`). They match the PR table.
- **Open:** F1 (the `port_seen_r` reference level) and F2 (NOTEN leaves the armed exchange).

### Robustness (UNCLEAN: R729-F1, R729-F2)

- Toggles shorter than one beat, low for 1 and 3 cycles inside a cease (probes B1 and B3):
  - two commits (fall and rise);
  - a request at once;
  - then one per interval;
  - re-earn in two exchanges.
- A rise swept over [-400, +200] cycles around the cadence timer's expiry, in 4-cycle steps (probe C, `receipts/probes-sweep-head.txt`): 151 offsets, never two requests and never none.
- A frame built across the fall is dropped, and its claim does not hold the next request (phase 46).
- A fall 2 cycles after a warm-reset release ends the cease (probe D, second variant).
- **Open:** a warm reset with the port low at release (F1), and a Follow_Up in flight across the fall (F2).

### Tests (UNCLEAN: R729-F1, R729-F2, missing gates)

Executed here at the exact head, every suite with its own log and rc in `receipts/head`, using pinned Verilator 5.050:

| Gate | Head | Base `f97c1803` |
|---|---|---|
| `make contract` | rc 0 | not re-run |
| `make lint` | rc 0, 0 warnings | not re-run |
| `make docs` | rc 0 (diagrams check, docs, source evidence "20 exact, 0 findings", both selftests) | not re-run |
| `make -C tb/verilator/engine run` | 2002 ×3 + 60, rc 0 | 1977 ×3 + 60, rc 0 |
| engine mutation arm (repository `run_mutant` verdicts, 8 workers) | 128/128, rc 0 | not re-run (see below) |
| `make -C tb/verilator/ucpu` | 768/768 | not re-run |
| `make -C tb/verilator/parser` | 378/378, arm 16/16 | not re-run |
| `make -C tb/verilator/gaskets` | 81/81, arm 5/5 | not re-run |
| `make -C tb/tsngen` | 288/288, arm 4/4 | not re-run |
| `make -C bench/arty test` | PASS | not re-run |
| tracked bytes after the runs | `git diff --exit-code` clean | clean |

- **New controls.** All 15 new #94 controls are caught, each on every check it names; the named-check rule covers the `#94 ` prefix.
- **Old controls.** The 112 earlier mutants are byte-identical between base and head (`MUTATIONS` compared entry by entry) and all are caught at head. So the BMCA, Announce, Sync and Pdelay checks they guard still bite. The base arm's 113/113 is the author's receipt (`author/receipts/repo-base-arm/01.log`). It was not re-run here: its mutant set is the unchanged subset above.
- **Coverage.** The author's coverage table (`author/receipts/coverage/coverage.md`) gives every one of the 25 new checks at least one failing control. Across the other suites I agree with it.
- **Missing gates:** no check covers a warm reset in a cease with the port low at release (F1), or a Pdelay_Resp_Follow_Up received after the fall (F2). The reviewer probes show that each would fail today.

### Docs (UNCLEAN: R729-F1, R729-F2)

- The new "Port enable" sections in `docs/INTEGRATION.md` and `docs/HDL_DEVELOPER.md`, the six `docs/TEST_DEVELOPER.md` lines and the integration checklist line describe the implementation accurately, with two exceptions:
  - `docs/INTEGRATION.md:214-216` and `docs/HDL_DEVELOPER.md:262` (F1). The boot cadence does not send the first request while a retained cease is quiet.
  - `docs/TEST_DEVELOPER.md:140` (F2). A Follow_Up heard while disabled commits.
- The re-pointed source-evidence anchors land on their constructs; I spot-checked 13 engine anchors and the generator anchor, and `check_source_evidence.py` reports 20 exact.
- The comment rule holds: no new lane, round, reviewer or comment ID.

## Parent companion (milan-fpga, lands with the adoption)

- **Applies.** `author/milan-fpga-companion.patch` applies cleanly (`git apply --check`, rc 0) to milan-fpga #805's head `e06ade31`. Its gitlink moves `gptp-processor` from `f97c1803` to `9d509029`.
- **Wiring.** `KL_gptp_shadow` passes `port_enabled_i` to its engine. `milan_datapath` drives it from `eff_link_w`. Every engine and shadow instantiation site in the parent `.sv` tree is covered: the shadow and `gptp_plane_wrap` for the engine; `milan_datapath`, `gptp_shadow_wrap` and `gptp_txts_wrap` for the shadow. The three wrappers tie the port high.
- **Reset values.** `LINK_CTRL` resets to 1 and the guard's `rx_alive_r` resets to 1, so `eff_link_w` at reset release follows `i_link_up`.
- **No contract change.** No register-map or contract change was found.
- **milan_dp checks.** The three new `milan_dp` gptp checks are: asCapable falls at a link loss; a link loss inside the cease ends it within one interval; and the countdown exit is unchanged.
  - The author's receipts show `milan_dp` `gptp` and `gptp-lat` at 205/205 on the head snapshot `f64eba22`, against 202/202 on base `e06ade31` (`author/receipts/parent-head-A/12.log`, `13.log`).
  - Four parent-side controls are each caught on their named checks (`author/receipts/parent-controls/results.json`).
  - The physical leg's Pdelay and verdict lines are identical to base (empty `parent-head-B/verdict-and-pdelay-lines-vs-base.diff`).
- **Not executed here.** The parent banks were not executed in this review (out of scope for a reviewer run; the author's `milan_dp_gptp` alone took 5,347 s). Neither new parent check exercises F1 or F2.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R729-F1, R729-F2) | Issue #94 clauses, Expected and Acceptance; Milan v1.2 4.2.6.2.4/4.2.6.2.5; 802.1AS-2011 10.2.4.11, 11.2.15.3, Figure 11-8 (Cor1/Cor2); NOTEN, cease, PDREQ and PDPOST legs; phases 44-47; probes A, B, C, D | R729-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| RTL | UNCLEAN (R729-F1, R729-F2) | `KL_gptp_engine.sv` (port, port_enable block, push arbitration, credit/SEND/claim gates, pdreq hold); `gen_gptp_ucode.py` (slot dispatch, NOTEN, cease entry, pairing gates); four regenerated ROM images; lint; ooc clock selftest; author area receipts | R729-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Robustness | UNCLEAN (R729-F1, R729-F2) | 1- and 3-cycle glitches; 151-offset rise/cadence sweep; frame built across the fall; fall after warm-reset release; warm reset with the port low at release; Follow_Up across the fall | R729-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Tests | UNCLEAN (R729-F1, R729-F2) | Engine suite at head and base; 128-entry arm with 15 #94 controls and 112 unchanged earlier mutants; ucpu, parser, gaskets, tsngen, arty suites; author coverage table; missing gates for F1 and F2 | R729-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Docs | UNCLEAN (R729-F1, R729-F2) | `docs/INTEGRATION.md`, `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md`, `docs/SOURCE_EVIDENCE.md` anchors, `make docs`, comment-rule search of the delta, PR body | R729-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |

## Real limits

- **Area.** No Vivado on this host. `make ooc` was not run, and the area and timing figures are the author's receipts.
- **Parent.** No parent bank and no `milan_dp` leg was executed. The parent assessment rests on source reading at `e06ade31`, a clean `git apply --check`, and the author's published receipts.
- **Base arm.** The base mutation arm (113/113) was not re-run. Its mutants are byte-identical to the head arm's earlier 112, all of which are caught here.
- **Probe harness.** Probes C and D use the engine harness's own peer model. Its egress-stamp return (PHC + 200 ns, offered on the next cycle) is idealised, and probe C's grid is 4 cycles.
- **Hosted CI.** No hosted check-runs exist at this head: 0 check-runs, and the combined status is pending with no contexts. Nothing hosted is claimed.
- **Hardware.** Physical calibration was NOT RUN. No hardware was touched, and field skips are not hardware proof. The in-house link-toggle scenario the issue promises has not been posted.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `f97c1803`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks, and link the receipts on the PR. That is distinct from this source-head review.
- Hosted and act acceptance.
- Route R729-F1 and R729-F2 to the author, or record a maintainer scope decision for F1 on #94.
- Parent adoption: kebag-logic/milan-fpga#806, which the assignment names, does not resolve as a pull request. The adoption still owes the companion on a real branch, the parent area re-measure (route-1x1, ooc-1x1, ooc-8x8) and the in-house link-toggle scenario on the built image.

## Restoration

- **Review clone.** The clone at `$REVIEWS/r729-1-gptp94` was never edited; every build and probe ran in disposable clones under the packet's `scratch/`. Verified after the runs:
  - HEAD `9d509029de967c50de7527edf2b8869aa9db9074` and tree `4d0c9d078cb2d575b100e23c6b34c2637c247594`;
  - `git diff` and `git diff --cached` are empty, and `git status --ignored` is empty;
  - the index's (mode, blob, path) list equals `git ls-tree -r HEAD`: sha256 `64db7726…5288` for both.
- **Gitlinks.** The repository has no submodule gitlinks (0 entries of mode 160000). The parent's `gptp-processor` gitlink is the companion's concern, and it was checked by `git apply --check` only.
- **Suite clones.** The head and base work clones show no tracked change after their suites.

## Receipts

`MANIFEST.sha256` lists every published file. Host paths in the receipts are replaced by `<packet>`, `<review-clone>`, `<home>` and `<pinned-simulator…>` placeholders.

- `receipts/env.txt`: identities (head, tree, base, simulator, evidence tree, apply-check base, hosted state).
- `receipts/head/*.log`, `*.rc`: every head gate above. `receipts/base/engine-run.*`: the base engine suite.
- `receipts/head/engine-mutants-par.log`: the 128-entry arm, with every named failing line of every caught #94 control.
- `receipts/probes-head.txt`, `receipts/probes-candidate-fix.txt`, `receipts/probes-sweep-head.txt`: probes A, B1, B3 and D at head, the same probes under the disposable candidate change, and sweep C.
- `receipts/probe2-run.log`, `receipts/probe2-sim_main.diff`: the first probe run and its harness insertion.
- `receipts/probe3-candidate-fix.diff`, `receipts/probe3-run.log`, `receipts/probe3-fullsuite.log`: the candidate change (not proposed as the fix), its probe run, and the unmodified suite passing against it.
- `scripts/run_probes.sh` (`[fix|sweep]`), `scripts/probe_phases.cpp`, `scripts/probe_phases2.cpp`: portable probe reproduction against any fresh clone.
- `scripts/par_mutants.py`: the parallel driver around the repository's own `mutants.run_mutant`.
- `scripts/run_suites.sh`: the per-gate runner.

R729-1 FINISHED
