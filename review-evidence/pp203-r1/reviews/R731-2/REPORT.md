[R731] POSITIVE - exact head 013ee63fd42455987ddbbbeb3b66f5af106b5793

# R731-2 independent review: processor issue #203 / PR #209 (AECP REBOOT), round 3 delta

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #209
- Exact head: `013ee63fd42455987ddbbbeb3b66f5af106b5793`, tree `b0f66acb645e958b1c9212c9e4d842991154a9a8`
- Previously reviewed head: `ec1ff275a72d885f0908fd213d8009e9e4dda4d9` (R731-1, R732-2). Source base `f65c8ff7`.
- Delta reviewed: `git diff ec1ff27..013ee63` (2 commits, 20 files), read against the whole `f65c8ff7..013ee63` series.
- Reviewer: internal independent reviewer, cleared context, own detached clone
- Simulator for every executed receipt: the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), identity checked before use

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open at this head.

- R731-F1 = R732-F3 (MAJOR) is RESOLVED at its cause. `reboot_req_o` now also waits for the TX arbiter to be idle. That covers the last frame started on any lane, with or without a DEPARTING.
- R732-F4 (MINOR) is RESOLVED. The live PR body is this head's text, and its figures reproduce.
- My mid-frame probe passes in both paths at this head. It fails the non-advertising path at the round-2 head, which reproduces F1. It fails both paths with the new wait planted out.
- The round-2 reviewers' probes pass at this head:
  - R731's window probe;
  - R732's post-DEPARTING probe, at 156 checks;
  - R732's non-advertising probe, at 162 checks.
- All 31 REBOOT arms are KILLED by name, each with its README count. The early-request arm fails 32 checks.
- The parent consumer checks pass with `reboot_req_o` named open: the lint ratchet, and the `pp_shadow` suite at 2,310 checks.

One wording RESIDUE and two carried SUGGESTIONs are recorded below. None of them affects the verdict.

## Findings

### R731-R1 (RESIDUE): diagram 21's label says the request is held "from a REBOOT's SUCCESS"

- **Lenses:** Docs.
- **Where:** `docs/diagrams/21-integration-faces.svg:124`:
  `reboot_req_o: held from a REBOOT's SUCCESS to rst_n`. The label is hand-authored. It was added in
  `d7a24de` (round 1) and is untouched by this delta. R731-1 missed it.
- **Authority:** 02 F02.10 (`docs/architecture/02_interfaces.md:584`). The request rises only after
  the SUCCESS response, the notifications, any DEPARTING and the last frame started have each had
  their last byte taken.
- **Impact:** wording only. A reader of the figure could take the request to rise at the SUCCESS.
  F02.10, 06 §6.11 and both guides state the contract correctly, and no measurement, test or
  claim depends on the label.
- **Exact fix:** replace the text with
  `reboot_req_o: held, once a REBOOT's frames have left, to rst_n`. Keep the same element and
  coordinates; `scripts/check-integrator-params.py` reads this file, so re-run `make check`.

### R731-S1 (SUGGESTION, carried from R731-1): state the request's clock-domain contract at F02.10, or register it

- **Lenses:** RTL, Docs.
- **Where:** `hdl/top/protocol_processor_top.sv:4957`
  (`assign reboot_req_o = (rbt_st_r == RB_REQ);`), F02.10 and `docs/guides/integrator.md`.
- **Status at this head:** the PR body's open risks now say that the request is a `clk_i`-domain
  decode, to be synchronised by an asynchronous reset input. F02.10 and the integrator guide still
  cover it only through the general rule at `docs/guides/integrator.md:46`.
- **Detail:** the encoding argument is unchanged. RB_DOWN to RB_DEP is 011 to 100 and can decode
  as 101 for a moment in gates. RB_DEP to RB_REQ is 100 to 101, a single bit.
- **Suggested outcome:** one flop on the output, or one sentence at F02.10 and in the guide. Both
  are optional. milan-fpga #787 consumes the port.

### R731-S2 (SUGGESTION, carried from R731-1): the whole-frame RX discard has no observable test

- **Lenses:** Tests.
- **Status:** unchanged by this delta. My probe `p2-rx-gate-cuts-mid-frame` survived at the round-2
  head, and nothing after the acceptance is admitted, so no wire behaviour changes. The point is
  optional.

**Comment rule:** I scanned the delta's added lines in `hdl tb scripts syn Makefile` for bench
lane labels, reviewer IDs, review rounds and comment IDs (`receipts/comment_rule_scan.txt`). No
new instance was found.
- Every "round" hit is the protocol's notification round.
- Every "lane" hit is a TX arbiter lane, a hardware term.
- "The reviewers' two non-advertising cases" appears only in commit `cb73ff3`'s message and in the
  PR body, where the rule allows it.

## Prior public findings at this head

I wrote my own verdict and ledger first (`receipts/verdict_before_prior_reviews.md`, 04:52Z).
Only then did I read R732-2's report and the public comment list. I did not open R732-3.

- **R731-F1 = R732-F3 (MAJOR): RESOLVED.**
  - **Cause, before:** RB_DEP waited only for ADP's build, ADP's queue and ADP's flight. With no
    advertise machine up, a frame from another lane, selected before the gate closed, overlapped
    the rise.
  - **Cause, now:** RB_DEP also requires `!arb_busy_w` (`hdl/top/protocol_processor_top.sv:4946`,
    `:4947`). The new arbiter output is `busy_o = (arb_st_r != A_IDLE)`
    (`hdl/packet_engine/KL_pp_tx_arbiter.sv:301`). It is high from a selection, through A_START and
    A_STREAM, to the clock the downstream takes the last byte.
  - **Why idle means "the last byte has left":**
    - The arbiter's byte lane is a pass-through.
    - The ACMP header shim between the arbiter and `tx_*` is combinational. It gives the arbiter
      `tx_ready_i` only in pass-through and SH_BODY (`protocol_processor_top.sv`, `shim_stream`).
    - So the arbiter's `eof_w` is the MAC's `tx_valid_o && tx_eof_o && tx_ready_i`.
  - **Why no new frame starts after the exit:**
    - The exit clock has `rbt_quiet_w` high (RB_DEP with ADP not busy, `:4928`), which masks every
      lane except ADP's (`:4692`).
    - ADP's lane request is `laneq_adp_cnt_r != 0`, which the exit requires to be 0.
    - So `select_w` is 0 in the exit clock, and RB_REQ keeps the gate closed until reset.
  - **Advertising path:** the DEPARTING is the last frame the arbiter starts, so the same wait
    covers it. This replaces the retired `tx_fly_adp_r`.
  - **Executed evidence:** my mid-frame probe (`PRM-*`), my window probe (`PRB-*`), R732's
    non-advertising probe, and RBT12/RBT13 with arms `rbt-last-frame-unwatched` and
    `rbt-last-byte-offered` (see "Executed evidence").
  - **The manager's round-3 required outcomes are all met:**
    - the request follows the last frame's EOF handshake, in both paths;
    - no frame starts after it;
    - SUCCESS and the notifications stay first;
    - each reviewer's probe is a permanent row with EOF backpressure: RBT12 is R731's lock-expiry
      case, and RBT13 is R732's eight-sink, slots-full case;
    - each row has an early-request plant that it kills.
- **R732-F4 (MINOR): RESOLVED.** The live body (`gh pr view` at this head) is byte-identical to the
  published `author-r3/PR-BODY.md`. Its manifest hash matches. Its figures agree with this head:
  - RBT has 155 checks; I reproduced it.
  - There are 31 REBOOT arms, 18 sequence plus 13 gate; I reproduced them, with each count equal
    to its README cell.
  - `tb/tx_arbiter` has 67 checks, and the two `busy_o` plants fail 9 of 67; I reproduced both.
  - OOC is −385 LUT, +7 FF and +4 CARRY4. I recomputed this from the manifest-verified
    `ooc-head.log` and `ooc-base-dev-1e80128f-from-round1.log`.
  - pp_top 11,060 = 11,032 + 28 new RBT checks.
  - Sweep 1,030,922 = 1,030,893 + 28 + 1.
  - Requirement evidence: 264. The 262 + 2 new tags agree with `make check`'s 264 tags.
  - Earlier rounds' figures are labelled as superseded under "Review history".
- **R732-F1 (MAJOR, round 1): stays RESOLVED.**
  - R732's post-DEPARTING probe, unchanged, gives 156 checks and 0 failures at this head.
  - The 13 gate arms are KILLED.
  - RBT9 to RBT11 pass inside RBT's 155 checks.
- **R732-F2 (RESIDUE, round 1): stays RESOLVED.** Line 824's heading is unchanged.
- **R731-S1 and R731-S2:** carried as SUGGESTIONs (above).

## Five lenses on the delta

- **Conformance.**
  - The status table, lock refusal and response-first order are untouched by the delta and keep
    R731-1's CLEAN disposition (IEEE 1722.1-2021 §7.4.43; §7.4.43.2 with §7.4.1/§7.4.2).
  - The notification still reaches every other registered controller before the DEPARTING (IEEE
    §7.5.2; Milan v1.2 §5.4.5.2). The DEPARTING still goes where advertising (Milan §5.6.3.5.8 and
    §5.6.3.5.11; IEEE §6.2.4 and §6.2.5.2.2). It is now proven again by `PRM-ADV`'s order check
    (SUCCESS, then notification, then the held frame whole, then one DEPARTING, then the request)
    and by RBT6.
  - REQ-FWX-001's row (`docs/00_MILAN_COMPLIANCE_REVIEW.md:557`) now names the arbiter's `busy_o`
    and "the request after the last frame started, of any lane". This is the frozen acceptance's
    "the request follows the transmit-done".
  - CLEAN.
- **RTL.**
  - The new wait is correct by construction (see R731-F1 above) and adds one port to
    `KL_pp_tx_arbiter` (`hdl/packet_engine/KL_pp_tx_arbiter.sv:85`).
  - `tx_fly_uns_r` is still needed: RB_NTF uses it to decide when the gate may close.
  - No top-level port, parameter or register-map change. The issue's one allowed top change is
    still `reboot_req_o` alone.
  - Lint: 41 modules LINT OK at 5.050.
  - CLEAN.
- **Robustness.**
  - **Mid-frame backpressure:** the MAC holds another lane's frame at its 30th byte for 500 ms,
    then takes it. In both paths the request stays 0 throughout and rises two clocks after that
    frame's last byte (`PRM-NA` rise 155516 after 155514; `PRM-ADV` rise 627203 after the DEPARTING
    at 627201, which itself follows the held frame).
  - **Integrity:** no torn byte, and no offer after the rise.
  - **Slot exhaustion:** RBT13 and R732's probe, with no standard TX slot free.
  - **Withheld reset:** 5 s in RBT12/RBT13, 75 s and 65 s in RBT9/RBT10.
  - **Liveness:** finite. The gate stops new non-ADP selections, ADP builds nothing after its
    enable falls, and a MAC that never takes a byte holds the request back, as documented.
  - CLEAN.
- **Tests.**
  - RBT12 and RBT13 (`tb/pp_top/sim_main.cpp:13081`, `:13093`) check every byte offered from the
    rise through a 5 s withheld reset (`tx_offer_t == t_last`).
  - RBT7's new open-gate check (`:12718`) names `rbt-response-unwatched`. RBT12's open-gate check
    names `rbt-notification-flight-unwatched`.
  - The re-targeted names are honest: with the arbiter wait holding the request, those two losses
    now show only as an early gate close.
  - `tb/tx_arbiter` compares `busy_o` with the model every clock. Its M6 and M7 plants fail as
    recorded.
  - CLEAN.
- **Docs.** The following all match the RTL and the executed counts:
  - 00 (GAP-13 text, REQ-FWX-001);
  - 02 (reset rule 6, F02.10);
  - 03 F03.5 (REBOOT gate row, `docs/architecture/03_packet_engine.md:494`);
  - 04 (enable row, `docs/architecture/04_adp_engine.md:166`);
  - 06 §6.11 (step 4 at `docs/architecture/06_aecp_engine.md:1104`, the RBT12/13 paragraph) and
    the F06.14 REBOOT row;
  - both guides;
  - `tb/pp_top/README.md` (arm table, RBT12/13 rows);
  - `tb/tx_arbiter/README.md` (67 checks, M6/M7, re-plant counts).

  No stale reference to `tx_fly_adp_r`, "build, queue or send" or "granted in those two clocks"
  remains (`git grep`). `make check` rc 0. CLEAN, with RESIDUE R731-R1 carried to the checklist.

## Executed evidence (this review, exact head unless stated, Verilator 5.050)

Every build ran in a copy under the packet's `scratch/`. The copies came from `git archive` of the
exact head, which `receipts/scratch_head_vs_archive.txt` confirms (0 differences after all runs).

| Receipt | Command | Result |
|---|---|---|
| `receipts/golden_reboot.log` | `make -C tb/pp_top reboot` | RBT: 155 checks, 0 failures (0.50 GB RSS) |
| `receipts/tx_arbiter.log` | `make -C tb/tx_arbiter` | 67 checks: 67 PASS |
| `receipts/arb_busy_plants.log` | `scripts/arb_busy_plants.sh` (README M6, M7) | M6 fails 9 of 67 (`G busy_o ...` 3084 off); M7 fails 9 of 67 (1491 off): equal to the README |
| `receipts/camp_disp_rbt.log`, `receipts/camp-out/` | `aecp_dispatch_mutants.py --only <31 rbt arms> --jobs 7` | control PASS, 31 of 31 KILLED by name (32 checks, 0 FAIL) |
| `receipts/camp_disp_rbt_readme_cells.txt` | each arm's failure count against its `tb/pp_top/README.md` cell | 31 of 31 equal; `rbt-request-at-acceptance` (the early-request plant) fails 32 |
| `receipts/prm_head.out` | `scripts/probe_mid.py` (my probe: another lane's frame held mid-frame 500 ms at the round's end) | PRM-NA and PRM-ADV pass: 25 checks, 0 failures |
| `receipts/prm_old.out` | the same probe on round-2 head `ec1ff27` | PRM-NA FAILS (rise 105454 while the frame is held mid-frame; it ends at 155514); PRM-ADV passes |
| `receipts/prm_lastframe.out` | the same probe with `rbt-last-frame-unwatched` planted | PRM-NA and PRM-ADV both FAIL (ADV: rise 627089, DEPARTING ends 627169) |
| `receipts/probe_window.log` | `scripts/run_window_probe.sh` (R731-1's probe, unchanged; hunk applies at offset 9) | PRB-NA rise 105515 after the unlock notification's last byte at 105513; PRB-ADV rise 332234 after the DEPARTING at 332232; 11 checks, 0 failures |
| `receipts/r732_post_departure.log` | R732-2's `post-departure-probe.patch`, unchanged (`scripts/run_patch_probe.sh`, no fuzz, offset 58) | 156 checks, 0 failures |
| `receipts/r732_nonadvertising_old.log` | R732-2's `nonadvertising-probe.patch`, unchanged, on `ec1ff27` | 134 checks, 1 failure: request 16184473, ACMP frame ends 16184542 (reproduces R732-F3) |
| `receipts/r732_nonadvertising_nofuzz.log` | the same patch at this head, applied textually | hunk 1 cannot apply (the head appended RBT12/13 to `run()`), so the probe is not called: 155 checks; not counted as a probe run |
| `receipts/r732_nonadvertising.log` | `scripts/run_r732_nonadv.sh`: the patch's method hunk plus the call inserted by R732-2's own generator rule (`run-probes.py`, first-occurrence replace) | 162 checks, 0 failures; request 16184544 with `in_frame=0` after the 70-byte ACMP frame |
| `receipts/lint_hdl_5050.log` | `scripts/lint_hdl.sh`, pinned simulator first on PATH | 41 modules LINT OK |
| `receipts/make_check.log` | `make check` in a scratch clone at the head | rc 0; AECP command gate 32 commands, F06.14 42 rows, self-test 231 of 231; req-tags 264 tags |
| `receipts/parent_lint_pin_absent.log` | milan-fpga dev `1e80128f` (shallow scratch clone), processor = this head, `scripts/lint_rtl.py --check` | rc 1: `NEW ... PINMISSING ... 'reboot_req_o'`, as the PR body states |
| `receipts/parent_consumer_edit.diff`, `receipts/parent_lint_pin_open.log` | the same with `.reboot_req_o ()` named open at `u_pp` | `LINT GATE: PASS (89 violation(s) <= ratchet 89)` |
| `receipts/parent_pp_shadow.log` | `make -C tb/verilator/pp_shadow` in that scratch parent | 4 runs, 651 + 651 + 691 + 317 = 2,310 checks, 0 failures, every `RESULT: PASS` (equal to the author's `pp_shadow 2310`) |
| `receipts/evidence_manifest_check.txt` | `scripts/verify_manifest.py` against the published `MANIFEST.json` (milan-fpga `08802d05`) | 14 of 14 downloaded author-r3 files match |
| `receipts/hosted_check_runs.txt` | read-only check-run listing at the head | `docs-gates` and `portability` success in runs 41002318569 and 41002322002; both `suites` jobs in progress |
| `receipts/comment_rule_scan.txt` | added-line scan of the delta | no new comment-rule instance |

**Clone integrity** (`receipts/clone_integrity_after.txt`, `receipts/clone_index_after.txt`):
- HEAD is still the exact head, and the index writes tree `b0f66acb...`.
- All 750 tracked blobs re-hash to their index entries, with modes intact.
- `git status --porcelain --ignored` is empty.
- There are 0 gitlinks: the processor has no submodules.

**Scratch parent:** its processor directory is a clone at `013ee63` / `b0f66acb`
(`receipts/parent_pp_gitlink_content.txt`). Its own index entry for the gitlink was not re-staged.

**Redaction:** in the published logs, the simulator's install root and the user's home are
redacted to `<verilator-5.050-root>` and `<home>`.

**Probe sources:** R732-2's patches and runner are copied unchanged under `probes/r732-2/`, from
milan-fpga `95ef1fda641e7fd17e5b75643f1d1941b08af413`, `review-evidence/pp203-r1/reviews/R732-2/`.
R731-1's window patch is under `probes/`.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | §7.4.43 status and response-first order (unchanged since R731-1); §7.5.2 / Milan §5.4.5.2 notification before the DEPARTING; Milan §5.6.3.5.8/.11 and IEEE §6.2.4/§6.2.5.2.2 DEPARTING; REQ-FWX-001 row; issue #203 frozen acceptance and the round-3 required outcomes; PRM-ADV / RBT6 order | R731-2 (delta); R731-1 (unchanged status paths) | 013ee63fd42455987ddbbbeb3b66f5af106b5793 |
| RTL | CLEAN | `KL_pp_tx_arbiter.sv` FSM and `busy_o`; top `rbt_sequence`, `rbt_quiet_w`, `rbt_tx_gate`, `arb_req_w`, ACMP shim, `rbt_tx_flight`; lint at 5.050 | R731-2 | 013ee63fd42455987ddbbbeb3b66f5af106b5793 |
| Robustness | CLEAN | mid-frame and EOF backpressure in both paths; slots full; lock expiry at the round's end; withheld reset 5 s to 75 s; liveness of the new wait; parent consumer with the pin open | R731-2 | 013ee63fd42455987ddbbbeb3b66f5af106b5793 |
| Tests | CLEAN | RBT7 open-gate, RBT12, RBT13 and helpers in `tb/pp_top/sim_main.cpp`; `pp_top_wrap.sv` tap; 31 arms and 4 changed patches; `tb/tx_arbiter` check and M6/M7; README cells; R731 and R732 probes | R731-2 | 013ee63fd42455987ddbbbeb3b66f5af106b5793 |
| Docs | CLEAN (RESIDUE R731-R1 carried) | 00 GAP-13/REQ-FWX-001, 02 reset rule and F02.10, 03 F03.5, 04, 06 §6.11 and F06.14, integrator and operator guides, diagram 21, both bench READMEs, port and sequence comments, live PR body; `make check` | R731-2 | 013ee63fd42455987ddbbbeb3b66f5af106b5793 |

## Real limits

- No IEEE 1722.1-2021 or Milan v1.2 text was available here. Clause readings are those cited by the
  issue and the documents, checked for consistency, not quoted from the standards.
- No full bank was run: no `run_suites.sh`, Yosys or elaboration-guard bank, OOC synthesis, or the
  other campaigns. The sweep total (1,030,922) and the other campaign totals in the PR body are the
  author's published receipts. I checked them for consistency with the counts I reproduced, not by
  re-running them.
- **The parent consumer check was focused.** I ran the lint ratchet with the pin absent and with
  it open, and the `pp_shadow` suite, in a shallow scratch clone of dev `1e80128f`. I did not run:
  - the author's 64-suite sweep;
  - behave;
  - the static-docs gates;
  - the three other parent adoption edits (behave SERVED list, feature status, pin docs). The PR
    body lists them as required for adoption.
- The `external` and other non-processor parent submodules were not fetched beyond `gptp-processor`
  and `third_party/verilog-axis`, which the lint and `pp_shadow` need.
- The evidence commit `08802d05` is not cryptographically signed (`verification.reason: unsigned`).
  What I verified is the published `MANIFEST.json` hashes, for 14 spot-checked files.
- R732-2's non-advertising patch no longer applies textually at this head. I ran it as its own
  generator builds it, with the method unchanged and the call by its first-occurrence rule.
- Gate-level behaviour of `reboot_req_o` (R731-S1) is reasoned from the encoding, not simulated.
- Physical calibration NOT RUN. No hardware, Vivado run or field test. Hosted `suites` jobs were
  still in progress when read, so no hosted suite result is claimed.

## Pending manager duties

- Carry RESIDUE R731-R1 (diagram 21 label, exact fix above) to the residue checklist.
- Hosted and act acceptance at this head: both `suites` jobs were in progress.
- The current-dev merge candidate (builder and native banks) at the merge turn, against live dev
  `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- The parent adoption edits listed in the PR body (pin named at `u_pp`, behave SERVED, feature
  status, pin docs), and milan-fpga #787's use of the port. R731-S1 is relevant there.

R731-2 FINISHED
