[R731] POSITIVE - exact head 667b9bbc02b99a08d71efab750f95e8702cbbe57

# R731-1: internal cleared-context review of PR #822 (#787)

- PR: kebag-logic/milan-fpga #822, `787-reboot-reset` -> `dev`.
- Exact head `667b9bbc02b99a08d71efab750f95e8702cbbe57`, tree `171ad200ca2fbc5ab6050a200ab023d3249801c1`.
- Source base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Processor gitlink `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Scope: the whole PR, `git diff 1e80128f..667b9bbc`, 14 commits and 63 paths (60 files plus the gitlink as GitHub counts them). Five lenses applied.
- Role: the lane's internal cleared-context reviewer. This is not the external review.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open under any lens at this head.

One RESIDUE (a source comment that breaks the comment rule) and two SUGGESTIONs are recorded below. None of them changes a behaviour, a figure, a verdict or a conformance claim.

## How the task was reconstructed

1. I read AGENTS.md, CONTRIBUTING.md (sections 1 to 3 and 6) and docs/README.md.
2. Issue #787's body (receipts/issue787_body.txt), fetched without comments. The decision record is `docs/design/REBOOT_RESET.md` at the head.
3. PR metadata, fetched only through `gh pr view ... --json title,body,headRefOid,baseRefName,baseRefOid,files,commits` and `gh api .../pulls/822` (receipts/pr822_view.json, pr822_api.json).
4. The diff and its history, the RTL first, then the SoC, the builder, the harnesses and the documents.
5. Public executable evidence: tree `2ae3b3b4` `review-evidence/787-r1` (`author/`, A700 and A700c; `author-r3/`, A700d) and the exact-head hosted check runs.
6. Authorities cited: IEEE 1722.1-2021 7.4.43, 6.2.4.1.3 and 6.2.5.2.2; Milan v1.2 5.6.3.3, 5.6.3.5.8, 5.6.3.5.11 and Table 5.51; IEEE 802.3-2022 3.2.1, 3.2.2 and Table 4-2.
7. Pinned sources read where they decide a claim: LiteEth `276c9e37` `mac/core.py` (the transmit pipeline), `phy/gmii.py` and `phy/mii.py` (the PHY reset pin).

I read prior review findings only after this verdict and the ledger below were on disk (section "Prior public findings").

## The seven focus checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | SUCCESS, the notification and ENTITY_DEPARTING are whole and in order on the wire-side MAC model before the PHY hold; the unfixed RTL fails it | met | `[RB]` passes on three full legs (receipts/pp_shadow_full.log, 2,514 checks, 0 failures) and alone (reboot-mutant clean control). `hold-on-the-request-alone`, the silicon shape, fails "ENTITY_DEPARTING leaves after the notification, before the PHY hold" (receipts/pp_shadow_reboot_mutant.log). The public receipt `author/receipts/confirm-0d4be94c` runs `[RB]` against the unfixed head `0d4be94c`: RESULT FAIL, on that same check and on "leaves none in the MAC" (5 frames) |
| 2 | The in/out account cannot under-count | met | Analysis below, plus U12 to U18 of `reboot_ctrl` (receipts/reboot_ctrl_all.log, 221 + 46 checks) and the reviewer probes (receipts/probe_reboot_ctrl.log, probe_rb_wiring.log) |
| 3 | The toggle crossing is CDC-safe and constrained; the counter cannot alias | met | `KL_reboot_ctrl.sv:236,248-252` (three flops, edge from `[2]^[1]`); `sw/litex/milan_soc.py:1760-1762` (reset-less source, `eth_tx`); `sw/litex/clock_constraints.tcl:65-71` (class-based 8 ns `-datapath_only` eth<->part bound); round-3 route receipt: the bounded pair has 51 endpoints against dev's 50, at +5.87 ns |
| 4 | The bound derives from the SoC's definitions (gate 23m), and the restated end-to-end bound is right | met | `endstation_builder.py` `reboot_mac_statement` evaluates the SoC's own names and function; gate 23m elaborates the 5 real configs (receipts/builder_subset.log). Arithmetic re-derived below |
| 5 | Removing the MAC-port gate keeps builder gate 1b and the gPTP direct path (#187) | met | `milan_datapath.sv:1608-1612` and `9073-9074`: the handshake assignments are unchanged and the account reads derived wires. The gate 1b census (`test_builder.py:11707-11742`, unchanged) passes (receipts/builder_subset.log) |
| 6 | The re-pin's ROM ledger and boundary records come from their generators | met | `ltn_rom.hex`/`ucode.hex` regenerated from the pinned submodule hash to the new `rom_digests.tsv` rows (`23cc67ee...`, `49a993be...`). The boundary generator `--check`, `check_submodule_docs.py`, `check_diagram_pngs.py` and `gen_mac_tx_model.py --check` all pass (receipts/records_checks.log). Processor `a9e84b66` is PR #209's merge commit and the processor's `main` tip, and its tree `b0f66acb` is `013ee63f`'s (receipts/processor_pin_on_main.json) |
| 7 | The full sweep, rtl-fast and the #396 planner pass | met (author and hosted evidence; planner re-run) | Sweep at `e12147d4`: tally 2,192,196 checks, 0 failures, `reboot_ctrl` 298 (public `author/receipts/sweep-e12147d4/tally.log`). From `e12147d4` to the head only docs, generated records, `reboot_mutant.py` and a gitlink move to an identical tree change (`git diff --stat e12147d4..667b9bbc`). Exact-head hosted: rtl-fast, verilator-suites (19 shards executed), yosys-portability (4 shards executed), elaborate, docs-check, docs-check-no-git and wire-accountability all succeeded; only "Physical gPTP (nightly and manual)" was skipped (receipts/hosted_check_runs.txt). Planner: behave `torture_campaign_plan.feature` 189 scenarios pass, `torture_campaign.py --self-test` 123 tests OK (receipts/behave_torture_plan.log, torture_selftest.log) |

Round-3 route set (A700d, no commit): the public receipt `author-r3/receipts/results/head-667b9bbc-set-check.log` reads `RESULT: PASS`, `directive ExtraPostPlacementOpt selected ... 0.165 ns`. Every signoff corner is at or above the floors (setup +0.165/+1.565 ns, hold +0.102/+0.036 ns). The fall from the record is a WARNING, as #818 specifies. `xvlog/xvlog.log`: 0 findings over 85 hdl/ files and 52 pinned-processor files, the three changed RTL files included (`census-changed.txt`). The #607 check passes on all three route logs, and its planted copy is refused (rc 1). The IOB-pack result is quoted by the author's review-ready note; I did not open a raw IOB-pack log. These receipts match the PR body's figures.

## Analysis behind checks 2 to 4

**One source into the MAC.** `MilanMAC` has one transmit path, `tx_dp` (`m_axis_mac_tx`) -> `mac_tx_cdc` -> `tx_sf` -> `LiteEthMACCore` -> `phy.sink` (`milan_soc.py:1806-1836, 1867, 1895-1931`). The gPTP plane, the control lane, AAF and CRF all merge inside the datapath, upstream of the counted port, through combinational `adp_tx_arbiter` and `tx_ifg_gasket` stages (`milan_datapath.sv:8769-8834, 8971-8984, 9021-9041`; `tx_ifg_gasket.sv:58-62`; `adp_tx_arbiter.sv:120-124`). So `phy.sink` carries no frame the port did not count in. The processor's last frame is therefore at the port, or partly past it, when the request rises; `[RB]` grades exactly that ("at the port: ENTITY_DEPARTING left before the request").

**Under-count.**
- A half-taken frame: `in_frame_r`, `KL_reboot_ctrl.sv:253`.
- Back-to-back frames, and a frame in every MAC stage: each counts in at its own `tlast` (`:259-260`), whatever stage it sits in.
- A take and an end on the same clock: net zero. That is arm `end-wins-over-a-take`.
- A spurious first edge after reset: saturates at 0 (`:261`). A frame cannot complete within the three clocks after reset (a minimum frame is 8 beats).
- Two ends inside one sampling window lose edges. That only over-counts, which lengthens the wait to its bound.
- Loopback, or a one-sided MAC reset: over-count only.
- The flush clears the count only while both link-guard resets are high. `KL_link_guard.sv:47-56, 293, 309` raises `eth_rst_o` only together with `reinit_o`, and every MAC buffer is reset in that window.

**Aliasing.** `phy.sink` ends are at least 84 octet times apart (LiteEth's gap and preamble stages sit upstream of the PHY, `mac/core.py:139-146`). That is 672 ns at 1 Gb/s, against a 20 ns datapath clock. `fly_r` saturates both ways at `FLY_MAX_C` = 139 for the AX7101 statement, above the 61 frames the MAC can hold.

**10/100 Mb/s (Arty).**
- `_PHY_MODEL_MIN_MBPS["mii"] = 10`, so T_EGRESS = ceil(93,248 / 10,000) + 1 = 11 ms.
- The Arty configs set `milan_clk_hz`, so `crossed` is true and the statement is 11,656 octets. With `crossed` false it would be 10,092.
- The quiet millisecond is far longer than the MII converter's two nibbles (800 ns at 10 Mb/s).

**Dead transmit clock.** The count holds, and EGRESS ends at `egress_exp_w` (`:243, 290`). `[RB]`: 2,845 clocks from the request, inside (2,800, 2,904]; arm `egress-without-a-bound` is killed.

**Octet statement.** It is 564 beats x 8 + 61 frames x 84 + 2,020 = 11,656 octets:

- beats: `mac_tx_cdc` 16 + 1, `tx_sf` 512 + 1, core crossing 32 + 2 stage beats;
- frames: 17 + 8 + 2 + 34.

LiteEth `276c9e37` builds its TX path as CDC (depth 32, unbuffered) -> 64:8 converter -> 8-bit last_be/padding/CRC/preamble/gap stages (`mac/core.py:94-180`). Those hold one 64-bit word and a few octets, inside the two stage beats. The statement over-counts every frame's framing, so it is an upper bound.

**End-to-end bound.** Each wait expires on the tick after its bound, so each lasts at most bound + 1 ms. Request to IPROG word = 10,000 + T_E + 3,500 + 3 ms + 8 clocks:

| Statement | T_E | Bound |
|---|---:|---:|
| AX7101 | 2 ms | 13,505 ms |
| Arty | 11 ms | 13,514 ms |
| Datapath default | 28 ms | 13,531 ms |

The figure before the egress wait was 13,502 ms. U17 measures 108,041 clocks against a stated 108,048.

**Gate 23m and the statement.**
- The builder sets `crossed = bool(milan_clk_hz)`, and the SoC sets `milan_cd = "milan" if milan_clk_freq else "sys"` (`milan_soc.py:3181`).
- Gate 23m compares the elaborated Instance of each real config against `eb.datapath_params()`. A mismatch fails there, not silently.
- Gate 1f holds the FIFO keywords to the named depths and the toggle to `phy.sink` in `eth_tx`; 9 of 9 cuts are refused.

**ICAPE2 words.** The sequence is dummy, sync, NOOP, write WBSTAR, 0, write CMD, IPROG, NOOP, each byte bit-reversed. It matches the 7-series IPROG sequence and the pinned LiteX ICAP encoding. CSIB is low for exactly the eight IPROG clocks (`:309-311, 321`), and `[RB]` checks the exact words and the retry.

## Reviewer probes (disposable, under scratch/; scripts/ are portable)

| Probe | Planted where | Result | Reading |
|---|---|---|---|
| `sat-at-one` | `KL_reboot_ctrl.sv:259`, the count saturates at 1 | killed (U12) | under-count with two frames in the MAC is caught |
| `in-frame-sticks` | `:253`, the half-taken flag never clears | killed (U12, U13) | |
| `bound-without-quiet-ms` | `:174`, T_EGRESS without its quiet ms | killed (U12, U14, both legs) | |
| `exit-tick-not-idle` | `:290`, quiet exit without idle on the tick | survived | moves the cut-off for a frame that starts after the REBOOT's frames by one clock (a first beat on the clock before the tick); the design already loses such a frame, so this is one clock inside the stated tolerance (SUGGESTION S2) |
| `quiet-set-when-busy` | `:296`, the tick sets quiet even when busy | survived | shortens the quiet window by at most one clock after a frame that ends on the tick; no owed frame is affected (S2) |
| `frame-wired-to-beat` | `milan_datapath.sv:9761`, every beat counted as a frame | killed by `[RB]` | |
| `beat-wired-to-frame-end` | `milan_datapath.sv:9760` | survived `[RB]` | see S1 |
| `flush-unwired` | `milan_datapath.sv:9763` | survived `[RB]` | see S1 |

## Findings

### F1: RESIDUE (Docs)
- **Artifact:** `tb/verilator/reboot_ctrl/mutants.py:113-114`, added in `157967548c`.
- **Authority:** the owner comment rule of 2026-10-15. Source comments state behaviour and reason with issue and requirement IDs. They never show lane labels, review rounds, reviewer IDs or issue-comment IDs.
- **Evidence:** the new comment reads `# the [A10] arms of issuecomment-6518083444: today's PHY hold on the request alone, a drain that ignores the MAC FIFO, a drain with no bound`. It carries a lane label and an issue-comment ID. It also calls the two egress arms "a drain".
- **Impact:** wording only. It changes no arm, check or figure.
- **Required outcome (exact fix):** `# the egress arms of the REBOOT silicon defect (#787): the PHY hold on the request alone, an egress wait that ignores the MAC FIFO, an egress wait with no bound`.
- **Verification:** `grep -n 'issuecomment\|\[A10\]' tb/verilator/reboot_ctrl/mutants.py` prints nothing, and `make -C tb/verilator/reboot_ctrl mutants` still kills 30 of 30.

### S1: SUGGESTION (Tests, Robustness)
- **Artifact:** `hdl/milan/milan_datapath.sv:9760` (`.mac_tx_beat_i`) and `:9763` (`.mac_flush_i`).
- **Evidence:** both wirings survive `[RB]` when planted (receipts/probe_rb_wiring.log), and no other integration gate reads them. The unit suite grades the ports' behaviour (U13, U15).
- **Impact:** none on any owed frame.
  - The REBOOT's own frames are wholly past the port before the request, and they are counted in `fly_r`.
  - A wrong beat term exposes only a later frame, from another source, that stalls for more than a millisecond at the port. Such a frame is dropped inside `tx_sf` (store-and-forward, so no runt), which the design already accepts for late frames.
  - An unwired flush leaves the count high after a link-guard episode, so the wait ends at its 2 ms bound.
- **Optional outcome:**
  - an `[RB]` arm that stalls a non-owed frame mid-port across the exit tick;
  - one that runs a link-guard episode with frames in the MAC model before the REBOOT;
  - or both as `reboot-mutant` arms.

### S2: SUGGESTION (Tests)
- **Artifact:** `hdl/milan/KL_reboot_ctrl.sv:290, 296`.
- **Evidence:** the two survivors above. Each changes the quiet window's edge by one clock.
- **Optional outcome:** a U18 variant whose first beat lands on the clock before a tick, and one whose frame ends on the tick, each graded to the clock.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `pp_shadow` `[RB]` wire-side order and completeness of SUCCESS, the notification and ENTITY_DEPARTING against IEEE 1722.1-2021 7.4.43 and Milan v1.2 5.6.3.3 / Table 5.51 (`sim_main.cpp` `grade_reboot_on_the_wire`); IPROG words and bound against `REBOOT_RESET.md` 3; issue #787's acceptance (the bench items stay with #787, which the PR leaves open with "Relates to"); `torture_campaign.py` `check_release_reboot`/`check_release_gptp_relock` | R731-1 | `667b9bbc02b99a08d71efab750f95e8702cbbe57` |
| RTL | CLEAN | `hdl/milan/KL_reboot_ctrl.sv` (whole file), `milan_datapath.sv` diff and its TX arbitration chain, `KL_pp_shadow.sv` diff, `milan_soc.py` MilanMAC TX chain, toggle, MultiReg and ICAPE2, `clock_constraints.tcl`, `KL_link_guard.sv` reset sequencing, LiteEth `276c9e37` `mac/core.py`, `phy/gmii.py`, `phy/mii.py`; lint ratchet with pinned Verilator 5.050 passes (receipts/lint_rtl.log); round-3 xvlog/route receipts | R731-1 | `667b9bbc02b99a08d71efab750f95e8702cbbe57` |
| Robustness | CLEAN | under-count and alias cases above (half frame, back-to-back, every MAC stage, coincident take and end, reset edge, flush, loopback, 10/100 Mb/s, dead clock); reset during hold and words (U9, U10); one-clock request (U8); the no-MAC stub (gate 1f); probes in receipts/probe_*.log; S1 and S2 are optional and leave no open defect | R731-1 | `667b9bbc02b99a08d71efab750f95e8702cbbe57` |
| Tests | CLEAN | `reboot_ctrl` 221 + 46 checks and 30 of 30 mutants (receipts/reboot_ctrl_all.log); `pp_shadow` four legs, 2,514 checks (receipts/pp_shadow_full.log); `reboot-mutant` 6 of 6 (receipts/pp_shadow_reboot_mutant.log); builder gates 1b, 1d, 1f (+9 cuts), 23m (+3 cuts) with the LiteX interpreter (receipts/builder_subset.log); planner behave and self-test; 8 reviewer probes; hosted exact-head check runs | R731-1 | `667b9bbc02b99a08d71efab750f95e8702cbbe57` |
| Docs | CLEAN (one RESIDUE, F1) | `docs/design/REBOOT_RESET.md` (whole), `CLOCK_DOMAINS.md`, `INTEGRATION_GUIDE.md`, `TESTING.md`, `SUBMODULES.md`, `CHANGELOG.md`, `AREA_BUDGET.md`, `MODULE_MATRIX.md`, both suite READMEs, `BAREMETAL_FIRMWARE.md`; every bound figure re-derived; comment-rule scan of every added source line (one instance, F1) | R731-1 | `667b9bbc02b99a08d71efab750f95e8702cbbe57` |

## Real limits

- I did not run the full Verilator sweep, the full builder bank or Yosys, because the assignment does not allow it. The sweep figure is the author's receipt at `e12147d4`, plus the exact-head hosted `verilator-suites` and `yosys-portability`. The manager owns hosted and act acceptance.
- No route, Vivado, xvlog or IOB-pack run is mine. Those are the author's round-3 receipts, checked for consistency with the PR body.
- `[RB]` runs with `GPTP_PLANE_EN_P=0`. The account does not depend on the frame source at the port, and the plane-on datapath elaborates in `milan_dp` and the hosted shards. No simulation sends a REBOOT with the plane on.
- The MAC model in `[RB]` is a model. The real MilanMAC's toggle behaviour is held only structurally (gate 1f) until the bench.
- Physical calibration was NOT RUN. Desk results are not hardware proof. The DEPARTING on the wire and the #396 power area's 50 soft resets are the bench's.
- The route records: `docs/reference/SUBMODULES.md:433-455` and `docs/design/AREA_BUDGET.md:144-146` still describe the round-1 route at processor `1be824fc` ("The gate refuses its 0.333 ns fall"). Under the manager's record rule (10-30), the area record is re-recorded once on dev, so this is not a finding here. It is listed for the manager's re-record step.
- Cleanup: probe build outputs were removed with `git clean -fdX` (ignored files only), including pre-existing ignored `configs/generated/*.hex` and `sw/builder/out/`. After that, all 1,456 tracked files rehash to their index blobs, with no flagged index entries and no mode change. The index tree equals the head tree, and every checkout sits at its gitlink, clean (receipts/clone_integrity.txt).

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts. No manager source bank runs at this head, and none is claimed here.
- Carry F1 to the residue checklist.
- Re-record the area and route records on dev under the record rule.
- Run the bench: the DEPARTING on the wire, then the #396 power area's 50 soft resets on the rebuilt image. #787 stays open until then.
- The external review is still owed.

## Prior public findings

(Written after the verdict and the ledger above.)

I read PR #822's issue comments, reviews and review comments, and issue #787's comments, only after the verdict and the ledger were on disk.

- **No prior reviewer finding exists to resolve or retain.** PR #822 carries two review-start notices (this round's and R732-1's) and no review. Issue #787 carries only manager and executor comments: assignments, TAKEN, REVIEW READY, a route ruling and bench evidence.
- **The defect report** (`issuecomment-6518083444`) is the silicon defect this round fixes. Focus check 1 closes it at the desk: the wire-side `[RB]` passes, and the unfixed shape fails.
- **The route ruling** (`issuecomment-6514731566`) places the round-1 WNS refusal under #708 and #814. That matches the limit noted above on the stale round-1 route text in `SUBMODULES.md` and `AREA_BUDGET.md`.
- **The manager's bench note** (`issuecomment-6529314868`) agrees with this review. It covers a local integration image, not the release image. In 6 of 6 accepted REBOOTs, ENTITY_DEPARTING is the DUT's last frame on the wire, and the previous image sent none in 3 of 3.
- **The 0.78 to 0.97 s from DEPARTING to link silence** fits the drain waiting on pending saved-state work, inside the 11 s `power.reboot-reset` bound. The design allows it (`REBOOT_RESET.md` 4), but I did not grade it.
- **Verdict:** none of this changes the verdict or the ledger.

R731-1 FINISHED
