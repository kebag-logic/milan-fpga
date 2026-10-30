[R732] POSITIVE - exact head 667b9bbc02b99a08d71efab750f95e8702cbbe57

External cleared-context review of issue #787 / PR #822, round R732-1.
Head `667b9bbc02b99a08d71efab750f95e8702cbbe57`, tree `171ad200ca2fbc5ab6050a200ab023d3249801c1`, base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
Processor gitlink `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645` (processor PR #209's merge commit; tree `b0f66acb`, the same as the reviewed head `013ee63f`).

## Reconstruction

Read in order: AGENTS.md and CONTRIBUTING.md (completion bar, lenses, severity), docs/README.md, then the #787 issue body.
The issue requires a reset on `reboot_req_o` within a stated bound, a journal write completed or abandoned as at a cut, the #396 power-area checks, the bench smoke and the `power` area using REBOOT, a request-to-reset simulation, a mutant that ignores the request, and the pin carrying processor #203.
Also read: the manager's extension issuecomment-6518083444 (silicon pre-run: no ENTITY_DEPARTING; required: the PHY hold and the IPROG wait only after the egress path drains, a derived bound, the bound restated, a wire-side check covering both the advertising and non-advertising paths, and three planted mutants), and the review-start comment issuecomment-6529861618.
Then: IEEE 1722.1-2021 7.4.43, 6.2.4.1.3 and 6.2.5.2.2; Milan v1.2 5.6.3.3 and Table 5.51 as cited; IEEE 802.3-2022 3.2.1, 3.2.2 and Table 4-2; docs/design/REBOOT_RESET.md; `git diff 1e80128f..667b9bbc` (60 files, 14 commits); then the evidence tree at `2ae3b3b4` (`review-evidence/787-r1`).
PR data was fetched only through `gh pr view ... --json title,body,headRefOid,baseRefName,baseRefOid,files,commits`.
No PR or issue comment was listed before the verdict and ledger below were written to disk.

## What I executed (receipts under `receipts/`)

Host paths in the receipts are redacted to `<packet>`, `<clone>`, `<tools>`, `<home>` and `<tmp>`; nothing else in them was edited. All runs were in disposable clones of the exact head under this packet's `scratch/`, with Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, verified). The pinned LiteX venv was used for the builder gates.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/reboot_ctrl` (both legs + mutants) | default leg 221 checks 0 failures; 1 Gb/s leg 46/0; rc 0 | `reboot_ctrl_make.log/.rc` |
| `python3 -u mutants.py` (reboot_ctrl) | golden PASS, 30 of 30 controls killed, rc 0 | `reboot_ctrl_mutants.log/.rc` |
| `make -C tb/verilator/pp_shadow` (four legs) | 719, 719, 759 and 317 checks (2,514), 0 failures, all four `RESULT: PASS`; `[RB]` on the three full legs | `pp_shadow_make.log/.rc` |
| `python3 reboot_mutant.py` (pp_shadow) | clean control `[RB]` PASS; 6 of 6 arms killed by their named checks, including `hold-on-the-request-alone` (the pre-fix shape) on "ENTITY_DEPARTING leaves after the notification, before the PHY hold" | `pp_shadow_reboot_mutant.log/.rc` |
| builder gates 1d, 1f, 1f-bites, 23m, 23m-bites | ALL GATES PASS, rc 0 (10 s); 23m does 5 real `milan_soc.py` elaborations | `builder_subset5.log/.rc` |
| builder gate 1b (`test_baremetal_profile_contract`) alone | ALL GATES PASS, rc 0, 1,109 s; no arm NOT RUN on this host | `builder_gate1b.log/.rc` |
| the six-gate subset in one process | printed ALL GATES PASS, then hit my 590 s timeout (rc 124). Gate 1b alone needs 1,109 s, so this was my budget, not a gate failure | `builder_subset.log/.rc` |
| `submodule_boundaries.gen.py --check` and `--selftest`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `gen_mac_tx_model.py --check` | all OK, five rc 0 | `generators_check.log` |
| ROM ledger rows for `a9e84b66` against the images the head's build generated | `ucode.hex` 49a993be..., `ltn_rom.hex` 23cc67ee..., equal to the new `syn/yosys/rom_digests.tsv` rows | `rom_sha256_from_build.txt` |
| processor pin | `a9e84b66` parents `f65c8ff7` (old pin) and `013ee63f`; both trees `b0f66acb` | `processor_pin.txt` |
| reviewer leg: Arty statement 11,656 octets at 10 Mb/s with my own literal 11 ms (`--egress-only`) | 46/0 PASS; the same leg with literal 10 ms fails 4 checks, so the leg discriminates | `reviewer_arty_leg*.log/.rc` |
| reviewer probe: stray frame-end edge on the take's clock at count 0 | under-count shown (see S1); the same edge 10 clocks apart waits to the bound | `probe_coincide_at_zero.log`, `scripts/probe_coincide_at_zero.cpp` |
| #396 planner `torture_campaign.py --self-test`, `--coverage-by-area --areas power`, behave `torture_campaign_plan.feature` | 123 tests OK; power area `missing: {}`; 189 scenarios, 708 steps passed | `planner*.log`, `behave_torture_plan.log/.rc` |
| exact-head hosted check runs (read only) | rtl-fast, verilator-suites, yosys-portability, 19 Verilator shards, 4 Yosys shards, docs and firmware jobs: success. "Physical gPTP (nightly and manual)" skipped, which is not hardware proof | `hosted_check_runs_667b9bbc.txt` |
| author route-set receipts (`author-r3`) | all 617 published files match MANIFEST.json `published_sha256`. The 7 INDEX.md mismatches are exactly the 20 `path_redacted` files' pre-redaction hashes. `head-667b9bbc-set-check.log`: `directive ExtraPostPlacementOpt selected`, 0.165 ns, every corner at or above WNS 0.03 / WHS 0, `RESULT: PASS` rc 0. #607: three PASS. xvlog: 0 findings, rc 0. IOB pack 22 ports. Route status 0 routing errors. Toggle pair `eth_clocks0_rx -> milansoc_crg_clkout1` Max Delay Datapath Only 8.00 ns at +5.87 ns, 51 endpoints. CDC-3 17 -> 18 (the hold's ASYNC_REG MultiReg) | inspected in place |
| author sweep receipt `sweep-e12147d4/tally.log` | 2,192,196 checks, 0 in-suite failures, reboot_ctrl 298. `e12147d4..667b9bbc` touches no hdl/, sw/ or tb source except `reboot_mutant.py`; the gitlink moves `013ee63f` -> `a9e84b66`, same tree | inspected in place |
| comment-rule scan of every added source line (`git diff 1e80128f..667b9bbc -- hdl sw tb scripts syn tests`), corrected, run after the prior findings were read (see R2) | 1 hit, `tb/verilator/reboot_ctrl/mutants.py:113` | `comment_rule_scan.txt`, `scripts/comment_rule_scan.py` |
| clone integrity after all work | HEAD, tree, index (`git ls-files -s`), all six gitlinks byte-identical to the baseline; worktree == HEAD; 0 status entries | `clone_integrity.txt` |

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

**[R732] SUGGESTION RTL, Robustness - hdl/milan/KL_reboot_ctrl.sv:257-262 - a stray end on the clock of a take at count 0 cancels the take (S1)**
Requirement/evidence: the banner (lines 77-78) and REBOOT_RESET.md section 3 say the count "can only make the wait longer, never shorter". When `fly_r == 0`, `took_w` and `txend_w` on the same clock hit neither branch. The end can only be stray, because no counted frame is in the MAC. So the frame taken on that clock is never counted. `receipts/probe_coincide_at_zero.log`: the PHY hold comes 1.8 ms after the request with that frame still in the MAC; with the edge 10 clocks earlier, it comes at the 28 ms bound.
Impact: none reachable on the shipping wiring. The datapath (`milan_cd`) and the MAC's sys side share the PLL reset (`sw/litex/milan_soc.py:853`, `ResetSignal(milan_cd)`). The flush clears the count only while both MAC sides are in reset, and the eth side then emits nothing. So a stray edge arises only in the first clocks after a reset, when no source can be taking a frame. This is a corner where the code contradicts its stated invariant, not an observed defect.
Required change (optional): count the take when `took_w && txend_w && fly_r == 0`, and add a mutant/check for it. Or state the exception in the banner.
Verification: the reviewer probe reports "waited to the bound" for the same-clock case.

**[R732] SUGGESTION Tests - tb/verilator/reboot_ctrl/mutants.py - no control for the count's upper saturation (S2)**
Requirement/evidence: `FLY_MAX_C` (KL_reboot_ctrl.sv:177) must be at least the most frames the MAC can hold, or a saturated count under-counts. No mutant lowers it. U12's three frames would catch only a ceiling below 3.
Impact: none at the head. `FLY_MAX_C` is 139 for the SoC statement against at most 61 framed beats plus one frame on the line.
Required change (optional): a mutant setting the ceiling to the U12 depth, killed by U12, or a check at a statement whose ceiling is reachable.
Verification: mutants.py lists the control as killed.

**[R732] RESIDUE Docs - tb/tools/torture_campaign.py:3135-3139 - the link-down comment omits the egress wait**
Requirement/evidence: the comment on `RELEASE_REBOOT_LINK_DOWN_S` says the end station holds its PHY in reset "once its saved state drains, within 10,000 ms and one tick of the request". Since `15796754`, the hold also waits for the egress (at most 2 ms on the AX7101 and 11 ms on the Arty, plus a tick). REBOOT_RESET.md section 6 states it correctly: "within 11 s of T0, the drain and egress bounds rounded up". The value 11 stays right (at most 10,013 ms on the Arty). No measurement, figure, verdict, test or code changes, so this is purely wording.
Exact fix: replace "holds its PHY in reset once its saved state drains, within 10,000 ms and one tick of the request" with "holds its PHY in reset once its saved state drains and the MAC has sent every frame, within 10,000 ms, the egress bound (11 ms at most) and two ticks of the request".

**[R732] RESIDUE Docs - tb/verilator/reboot_ctrl/mutants.py:113-114 - a source comment shows a lane label and an issue-comment ID (R2; retained from R731-1 F1)**
Requirement/evidence: the owner comment rule (2026-10-15) says source comments never show lane labels or issue-comment IDs. The comment added in `157967548c` reads `# the [A10] arms of issuecomment-6518083444: today's PHY hold on the request alone, a drain that ignores the MAC FIFO, a drain with no bound`. It also calls the two egress arms "a drain".
My first-pass comment-rule scan missed this: the case-insensitive pattern also matched `1'b0`, and the output was cut at 30 lines. After reading the prior findings I re-ran a corrected scan over every added line of the source delta. It finds exactly this one instance (`receipts/comment_rule_scan.txt`, `hits: 1`).
Impact: wording only; it changes no arm, check or figure.
Exact fix: `# the egress arms of the REBOOT silicon defect (#787): the PHY hold on the request alone, an egress wait that ignores the MAC FIFO, an egress wait with no bound`.
Verification: the corrected scan reports `hits: 0`, and `make -C tb/verilator/reboot_ctrl mutants` still kills 30 of 30.

## Per-lens results

**[R732] PASS Conformance - tb/verilator/pp_shadow/sim_main.cpp grade_reboot_resets_the_end_station / grade_reboot_on_the_wire, pp_shadow_make.log lines 742-818 - SUCCESS, the REBOOT notification and ENTITY_DEPARTING checked whole and in order at the MAC model's wire side before the PHY hold**
Clauses checked: IEEE 1722.1-2021 7.4.43; Milan v1.2 5.6.3.3 and Table 5.51.
- Advertising: request at 43,904,460; last frame off the wire at 43,904,843; hold at 43,905,006, more than 1 ms (100 clocks) and at most two ticks after it. No frame is cut or left in the MAC.
- Not advertising: no DEPARTING at the port or on the wire, and the hold waits for the last frame the port started.
- Dead transmit clock: the hold at 2,845 clocks, inside (2,800, 2,904].
- A refused REBOOT (ENTITY 1, NO_SUCH_DESCRIPTOR) resets nothing.
- The unfixed shape (`hold-on-the-request-alone`) fails the DEPARTING check.
Issue acceptance:
- The bound is stated and graded: U17, 108,041 clocks against 108,048. The restated 13,505, 13,514 and 13,531 ms equal 10,000 + {2, 11, 28} + 3,500 + 3 from the module's own arithmetic. My Arty leg confirms 11 ms.
- The drain completes or abandons as at a cut: U2-U8.
- The `power` area and the UART smoke use REBOOT: planner tests, `--after-reboot`.
- A request-to-reset simulation and a request-ignored mutant exist in both suites.
- The pin carrying #203 is in this PR.
The four post-reset #396 checks are the bench's by the issue's own design, and are open (limits).

**[R732] PASS RTL - hdl/milan/KL_reboot_ctrl.sv:155-325, hdl/milan/milan_datapath.sv:9068-9075 and 9737-9767, sw/litex/milan_soc.py:1754-1762 and 2111-2166 - FSM, widths, reset, CDC and the gPTP path against the banner and CLOCK_DOMAINS.md**
- FSM: every state exits, and the default returns to IDLE. `quiet_r` is cleared on DRAIN exit and on any non-idle clock between ticks, and is sampled at ticks.
- Widths: `MS_W_C` 14 bits covers 10,000; `FLY_W_C` 8 bits covers 139. The count saturates at both ends. The `idx_r` wrap is intended.
- Toggle crossing: a reset-less source in `eth_tx` on `phy.sink` valid, ready and last. In LiteEth at the pinned `276c9e37`, `phy.sink` is after the CRC, preamble and gap stages, one frame-last per frame. The toggle feeds a three-flop synchroniser with edge detect on bits [2] and [1], the same as `KL_link_guard`. Edges are at least 672 ns apart against a 20 ns clock, so no edge is lost or merged. The pair is constrained by the existing 8 ns datapath-only bound (+5.87 ns at the head); MII keeps its asynchronous groups like the guard's toggles.
- The hold reaches `sys` through a MultiReg with ASYNC_REG (CDC-3 +1). ICAPE2 runs on the 50 MHz `milan_cd`.
- The MAC handshake assignments and the gate 1b reference census are unchanged: `tx_mac_beat_w` takes the one tvalid & tready reference `tx_mac_good_w` had. Gate 1b passes.
- No other transmit source enters `tx_sf` or `core.sink` (`milan_soc.py:1836`, `1894-1931`), so frames in equal frames out. Loopback and one-sided resets only over-count.
- Upstream of the port, the control chain (`ctl_tx_mux`, the 512-cycle `ctl_ifg` gasket, the MAC-boundary arbiter) holds nothing for anywhere near a quiet millisecond.
- S1 is a SUGGESTION, not reachable.

**[R732] PASS Robustness - reboot_ctrl U9-U18 and [RB], reboot_ctrl_make.log, reviewer_arty_leg.log, probe_coincide_at_zero.log - the account under ordering, rate and failure paths**
Every case in check (2) was covered:
- a frame half taken across ticks (U13);
- back-to-back frames and three frames in the MAC (U12, [RB] with KL_maap probing);
- a take on the clock of an end (U12 coincide);
- each MAC stage: the account is stage-agnostic, and the bound counts every named FIFO;
- 10 Mb/s (default leg, my Arty leg) and 1 Gb/s (1g leg);
- a dead transmit clock (U14, [RB]);
- a link-guard flush (U15);
- stray ends (U16);
- a reset during the hold and the words (U9, U10);
- a one-clock request (U7).
Streaming traffic that never goes quiet ends the wait at the bound. The bound is measured from EGRESS entry over buffers whose content precedes any later frame, so owed frames still leave at least 1 ms before it. S1 is the one corner found, and it is unreachable.

**[R732] PASS Tests - tb/verilator/reboot_ctrl/{sim_main.cpp,mutants.py}, tb/verilator/pp_shadow/{sim_main.cpp,reboot_mutant.py}, sw/builder/test_builder.py gates 1f/23m/1d - each new check fails for its defect**
- 30 of 30 and 6 of 6 mutants are killed by their named checks; the three the manager required (hold on the request alone, an egress that ignores the MAC FIFO, an egress with no bound) are among them.
- Gate 1f's 9 cuts are each refused by name, and gate 23m's 3 cuts likewise.
- The bounds are independent literals (Makefile `EGRESS_MS`, `RB_EGRESS_MS`, gate 1f's `564*8 + 61*84 + 2020`), and my wrong-literal leg fails.
- The bound is derived, not mirrored: `reboot_mac_statement` evaluates the SoC's own definitions with a node whitelist, and gate 23m holds 5 real elaborations to it.
- Existing regressions: pp_shadow's four legs, the author's sweep at e12147d4 (2,192,196 checks, sources unchanged since), and exact-head hosted rtl-fast and verilator-suites.
- S2 is optional.

**[R732] PASS Docs - docs/design/REBOOT_RESET.md, docs/litex/CLOCK_DOMAINS.md, docs/integration/INTEGRATION_GUIDE.md, docs/reference/SUBMODULES.md, syn/yosys/rom_digests.tsv, docs/diagrams/submodule_boundaries.*, docs/testing/TESTING.md, tb READMEs, CHANGELOG.md - changed contracts reflected and checked against the code and receipts**
- REBOOT_RESET.md: the bound arithmetic, the 11,656-octet decomposition (564 beats, 61 frames), and 2, 11 and 28 ms all agree with the code and my legs.
- The ROM ledger rows match the generated images. The boundary diagram, the pin table and the PNG checks pass their generators.
- The suite counts in TESTING.md and the READMEs match my runs (221, 46, 30).
- The comment rule: a corrected scan of every added source line finds one instance, `tb/verilator/reboot_ctrl/mutants.py:113` (RESIDUE R2, `receipts/comment_rule_scan.txt`).
- RESIDUE R1 and R2 are wording only.
- AREA_BUDGET.md and SUBMODULES.md still carry the `1be824fc` route and its old-gate verdict. Under the manager's record rule (the area record is re-recorded once on dev after the last release merge) this is not a finding.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | pp_shadow `[RB]` (sim_main.cpp, the four-leg log), reboot_ctrl U17, REBOOT_RESET.md sections 3 and 6, issue acceptance and extension | R732-1 | 667b9bbc02b99a08d71efab750f95e8702cbbe57 |
| RTL | CLEAN | KL_reboot_ctrl.sv, milan_datapath.sv delta, milan_soc.py MilanMAC delta, pinned LiteEth core.py, route clock_interaction and CDC receipts, gate 1b | R732-1 | 667b9bbc02b99a08d71efab750f95e8702cbbe57 |
| Robustness | CLEAN | reboot_ctrl U7-U18, [RB] dead-clock and non-advertising, reviewer Arty leg, reviewer coincide probe | R732-1 | 667b9bbc02b99a08d71efab750f95e8702cbbe57 |
| Tests | CLEAN | both mutant drivers (36 arms), gates 1f/23m/1d/1b, reviewer wrong-literal leg, planner self-test and behave, hosted exact-head contexts | R732-1 | 667b9bbc02b99a08d71efab750f95e8702cbbe57 |
| Docs | CLEAN (RESIDUE R1 and R2 carried) | REBOOT_RESET.md, CLOCK_DOMAINS.md, INTEGRATION_GUIDE.md, TESTING.md, SUBMODULES.md, rom_digests.tsv, boundary diagram, READMEs, CHANGELOG.md | R732-1 | 667b9bbc02b99a08d71efab750f95e8702cbbe57 |

## Real limits

- I did not run the full parent, PP, gPTP, Yosys or builder banks, Docker/act, or Vivado. The sweep, Yosys 61/61, docs and route figures are the author's published receipts, which I inspected. The route set's numbers were read from the published reports, not reproduced.
- The [RB] MAC is a model: its toggle flips at frame end in the same clock domain. The real crossing, the PHY's own transmit stage, and LiteEth's `phy.sink.last` behaviour are argued from the source and the route, not simulated.
- Physical calibration was NOT RUN. The hosted "Physical gPTP" context was skipped. No hardware proof exists: ENTITY_DEPARTING on silicon and the #396 power area's 50 soft resets (state restored, ADP valid time, gPTP relock with correct TX timestamps, rebind) are the bench's.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- The current-dev merge-candidate validation (builder and native banks) and its receipts; hosted/act acceptance.
- The bench re-run on the rebuilt pre-run image: DEPARTING on the wire, then the 50 soft resets. #787 stays open until then.
- The area and record re-recording on dev under the record rule.
- Carry RESIDUE R1 and R2 to the residue checklist.
- The internal cleared-context review and the second positive.

## Prior public findings at this head

I read these only after the verdict and ledger above were on disk: PR #822's issue comments (3), its reviews (0) and issue #787's comments (13).
The only prior review is R731-1, `[R731] POSITIVE` at this same head (issuecomment-6530610061). Its findings at this head:

| Prior finding | Lens | Status at 667b9bbc | Basis |
|---|---|---|---|
| R731 F1, RESIDUE, mutants.py:113-114 comment with `[A10]` and an issue-comment ID | Docs | **Retained** as my R2 | Confirmed independently by the corrected scan; still in the tree |
| R731 S1, SUGGESTION, `.mac_tx_beat_i` and `.mac_flush_i` wirings in milan_datapath.sv survive `[RB]` | Tests, Robustness | **Retained** (optional) | Agrees with my analysis: no owed frame depends on them; unit U13/U15 grade the ports |
| R731 S2, SUGGESTION, one-clock edges of the quiet window (`KL_reboot_ctrl.sv:290, 296`) survive | Tests | **Retained** (optional) | Not re-probed by me; it moves only late, non-owed frames by one clock |

My S1 (the same-clock stray end at count 0) and S2 (no saturation-top control) are not among R731's findings. R731's `sat-at-one` probe is a different plant (a ceiling of 1, killed by U12) and supports S2's reading that only small ceilings are caught.

Manager comments read for context:
- the extension issuecomment-6518083444, already used in the reconstruction;
- the route ruling issuecomment-6514731566 (the round-1 WNS refusal under #708 and #814), consistent with my non-finding on the `1be824fc` route text;
- the round-3 scope issuecomment-6525242660, matching the receipts I checked;
- the bench note issuecomment-6529314868.

The bench note records, on a local integration image (dev + #806 + #787 + #70 + #817 + #814, not the exact head or the release image), six accepted REBOOTs, each with ENTITY_DEPARTING as the last frame on the wire, ENTITY_AVAILABLE back in 13.3 to 14.1 s, and none from the previous image in 3 of 3. That supports the Conformance result but is not counted as exact-head evidence.

Nothing here changes the verdict or the ledger. The Docs row gains R2, which is RESIDUE and leaves the lens clean.

R732-1 FINISHED
