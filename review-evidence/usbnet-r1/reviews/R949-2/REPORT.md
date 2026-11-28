[R949] NEGATIVE - exact head 701f294405d47a81eed1079d32b54e1eea4a4f31

# R949-2: internal independent re-review of PR #1020 (#1011, #1018)

- **Round.** R949-2, internal cleared-context reviewer.
- **Head.** `701f294405d47a81eed1079d32b54e1eea4a4f31`, tree `d3ea9ebf7db3d37e41629adb27ac9003060f33c5`. I verified both in the clone, and the clone was byte-clean when I finished (`receipts/restore_check.txt`).
- **Range judged.** The delta since R949-1's head, `cc49123d..701f2944` (rounds 3 to 8), including the merge of #1004's head `640699e6`.
  - The USB lane's own content is the 56 files that differ from `640699e6` (`receipts/delta_vs_1004head.txt`).
  - #1004's content was not re-reviewed; only its identity was checked.
- **Reconstructed from.**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - The #1011 body and its owner-side comments (7165838061, 7186353239, 7188062527), and the #1018 body.
  - The PR rulings 7213370880, 7216971645 and 7234489667.
  - The FX3 interface authority: kebag-logic/usb-audio PR #7 (merge `e3c87baf`), `docs/NETWORK.md`.
  - The diff and history, the published packet `review-evidence/usbnet-r1/author-r8` at `ab597339`, and the exact-head hosted check runs.
- **Reading order.** No private author material, lane scratchpad or management directory was read. Prior public reviews (R949-1, R950-1) were read only after my independent pass.
- **Verdict.** NEGATIVE.
  - Two MAJOR findings: two CI gate self-tests fail at this head, both introduced by this lane.
  - Three MINOR findings.
  - Two RESIDUE items and four SUGGESTIONs.
  - All ten prior public findings are closed at this head, except one optional suggestion I kept.

## What holds at this head (verified)

- **Merge of #1004.**
  - `91252ecf` recomputes cleanly except one conflict, `sw/firmware/ctrl/test/ctrl_mutants.py`. That conflict resolves to `640699e6`'s bytes exactly.
  - The thirteen named dependency files are byte-identical to `640699e6`, and all six gitlinks are identical (`receipts/identity_check.txt`).
  - No path under `sw/firmware`, `configs`, `sw/mailbox`, `sw/builder` or any submodule differs from `640699e6`.
  - The two ruled exceptions are `egress_ledger.py` (ruling 7234489667, item 3) and the inventory (item 4).
- **Firmware identity.**
  - The author measured the Arty ELF (`f17d1a9d...`), both ALINX ELFs and the map header (`5f0c6026...`) at `91252ecf` against `640699e6`.
  - The three later commits change no firmware, SoC, configuration or RTL input: `a4f00496` adds egress test tooling and documentation, `9da0ba5f` changes the ledger tool and USB_NET_PATH.md, and `701f2944` changes only the inventory.
  - I did not rebuild the ELFs.
- **Ledger point (`USB_NET_PATH.md` section 3).**
  - An independent derivation reproduces all seven figures under `60 + 1.05 * (max - 60)`, rounded up to 0.01 ms (`receipts/ledger_probe.log`).
  - The Arty column equals SPLIT_CONTROL_MEMORY.md's table.
  - Only the last-AECP figure moves, from 61.99 to 62.14 ms (unrounded 62.1381675).
  - One 80 MHz cycle over the figure is 62.1400125 ms, which the grade records as 62.14001.
  - The ledger self-test passes and catches 25 of 25 mutants.
  - My three disposable doc plants are all refused: a low USB figure, a dropped injected measurement and a raised unrelated row (`receipts/ledger_plants.log`).
- **Injected census and wire bound.**
  - The 159 published per-case receipts give a largest wait of 558.835 us, at `none/aecp-largest-notice`. Every case has `agree_ps` 0.
  - `(558.835 + 54.88) * 1.05 + 0.32 + 0.26 = 644.98075 us`, which is at most 1000 us. `tb/verilator/usbnet/egress_grade.py:40-43` computes the same expression.
  - The provisional baseline replay records 15 free-space changes. That is why ruling 7216971645 item 3 (the full live census) applied, and the live census was run.
- **Handshake (my run).**
  - The production MII chain reproduces it: 512 cases, maximum 257.5 ns, stated as 260 ns.
  - Both chain plants are caught (early release, long handshake), and the egress controls pass 18 of 18.
- **Suites and plants (my runs, Verilator 5.050).**
  - `make run` passes 92,755 checks with 0 failures. The sweep tally reads 92,759 checks and 0 failures.
  - All 72 named planted defects are caught by their named checks (`receipts/campaigns/`).
- **Gates (my runs).** These pass:
  - docs_check, docs_inventory `--check`, check_doc_paths, gen_toc `--check` and `--verify-anchors`, check_solution_docs;
  - measure_test_evidence, measure_naming, check_py_idiom, check_hygiene, check_em_dash (`cc49123d..HEAD`);
  - lint_rtl `--check` (89 against a ratchet of 89), check_port_contracts, ci_events `--check` and `--selftest`.
  - The failures are F1 and F2, plus the inherited baremetal-only failure under the limits.
- **Published packet.** All 1,246 published files match the publication manifest's `published_sha256`.
  - Of the round-7 and round-8 author `MANIFEST.sha256` entries, 1,031 match byte for byte.
  - 201 differ only by recorded path redaction: their `original_sha256` equals the author hash.
  - 577 are listed but deliberately not archived (raw traces, journals, ELFs) (`receipts/packet_verify.log`).
- **Station record against the FX3 authority.**
  - Length then kind (`0x4E01`/`0x4E02`, L = 16); MAC first octet first; flags bit 0 is MAC_VALID.
  - Freshness is a serial-number sequence comparison; expiry is at 3 × heartbeat.
  - LD1 = bus alive ∧ held ∧ fresh ∧ MAC_VALID ∧ CONFIGURED ∧ SUPERSPEED (`hdl/usbnet/KL_usbnet_tap.sv:194`), exactly as NETWORK.md states it.
  - The record limit is 1514 to the computer and the acceptance envelope is 1515 from it. Both are documented with their reason (`USB_NET_PATH.md:263-267`).
- **Comment rule.** Added source lines in the delta carry no lane label, review round, reviewer ID or comment ID. "#1020 ruling" cites a PR, not a comment.

## Findings

### F1 MAJOR - Tests, Docs - `scripts/ci_scope.py:70` (`GATE_READ_DOCS`) against `tb/verilator/ctrl_service_budget/egress_ledger.py:45` (`USB_DOC`) - the change classifier's self-test fails at this head
- **Evidence.**
  - `9da0ba5f` made the ledger gate read `docs/design/USB_NET_PATH.md` but did not register that page as gate-read.
  - `python3 scripts/ci_scope.py --selftest` returns rc 1 with `FAIL gate-read page docs/design/USB_NET_PATH.md (named at tb/verilator/ctrl_service_budget/egress_ledger.py:45) is relevant` (`receipts/gates/ci-scope-selftest.log`).
  - Bisect: it passes at `91252ecf` and at `a4f00496`, and fails at `9da0ba5f` (`receipts/gates/ci-scope-bisect.log`).
  - The hosted `changes` job (140877762401) fails at the same step, "Classify the change conservatively".
- **Impact.**
  - `rtl-fast` and `full-ci-gate` are red at this head, and every long gate behind them is skipped.
  - Without the registration, an edit to the ledger table alone would be filed docs-only. It would then skip the very gate that reads that table.
- **Required outcome.** The page is a registered gate-read page, and `ci_scope.py --selftest` passes.
- **Verification.** The self-test passes at the new head, and the hosted `changes` job succeeds.

### F2 MAJOR - Tests - `scripts/suite_shards.py:148,152` (usbnet, 300 s provisional) merged with #1004's inventory - the Verilator shard self-test fails at this head
- **Evidence.**
  - `python3 scripts/suite_shards.py --selftest` returns rc 1 with `FAIL head worker 25/27 predicted 1299 s (21.6 min), bound 1276 s` (`receipts/gates/suite-shards-selftest.log`).
  - Run on full-tree exports, it passes at both merge parents, `b4a1df4a` and `640699e6`. It fails at the merge `91252ecf` and at HEAD (`receipts/gates/suite-shards-bisect.log`).
  - The self-test runs in `.github/workflows/rtl.yml`'s `verilator-shards` job (line 344).
- **Impact.** Exact-head `verilator-suites` cannot pass, so the AGENTS §7 ready-gate bullet cannot be met.
- **Required outcome.**
  - The merged inventory schedules within the 1276 s worker budget by the repository's own scheduling rule: re-measure or re-place `usbnet`, or rebalance.
  - The budget constant and the timeout bound are not raised.
- **Verification.** The self-test passes at the new head, and the hosted `verilator-suites` shards execute and pass.

### F3 MINOR - Docs, Conformance - `docs/design/USB_NET_PATH.md:78-79` - stale ACMP figure for the local-delivery wait
- **The page says.** "Adding the conservative bound to #1004's 29.77 ms ACMP row gives 29.808075 ms, below 30 ms by 191.925 us."
- **At this head.**
  - #1004's installed row is ACMP 29.84 ms (`docs/design/SPLIT_CONTROL_MEMORY.md:3579-3580`, byte-identical to `640699e6`). The author's round-8 handoff also uses 29.84.
  - The correct sum is 29.878075 ms, with a 121.925 us margin. The bound still holds.
  - The sentence was added in `5405864318`, before #1004's later row was merged, and was not updated.
- **Impact.** The authoritative page overstates the ACMP margin by 70 us. This is a figure claim, so it is not residue.
- **Required outcome.** The page states 29.84 ms, 29.878075 ms and 121.925 us, citing the installed row rather than a copied value.
- **Verification.** The doc diff, checked against SPLIT_CONTROL_MEMORY.md section 15.

### F4 MINOR - Tests, Conformance - `hdl/milan/milan_datapath.sv:4138-4144`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:217,386`, `tb/verilator/usbnet/test_clock.cpp:28-29` - the datapath sources of LD2 and LD3 are untested
- **Evidence.**
  - No file under `tb/` references `o_led_*` or `media_locked_all_o`. The usbnet suite never compiles `milan_datapath`.
  - The truth module is exhaustively tested and planted, and the attachment test covers `usbnet_soc`.
  - The clock-command test re-derives the source kind in the harness (`clock_internal_i = kind == 0`, `clock_stream_i = kind == 2`) and drives the truth module directly.
  - So the real decode never runs: `media_clk_table`/`media_clk_resolve` → `int_clk_selected_r`, `follow_sel_r`, and the indexed `avtprx_locked_all_w[aaf_follow_idx_r]`.
  - A defect in any of the six assigns would pass every test. Examples: a swapped selection level, the wrong lock index, or CRF dropped from LD2.
- **Authority.**
  - #1018 AC1: each input through each state, and each rule has a planted defect.
  - #1018 AC2: LD3 set over AECP SET_CLOCK_SOURCE.
  - Ruling 7213370880, item 5: STOP if a level is missing in fabric.
  - AGENTS §6 Tests: real integration wiring where practical; tests do not merely reproduce implementation assumptions.
- **Note.** I read the six assigns against the ruling and they are correct. The finding is the missing test, not the logic.
- **Required outcome.** Either:
  - a check drives the real datapath levels from a stored clock-source index and the stream lock and gate levels to `o_led_*`, with named plants for the selection decode, the indexed lock and the LD2 reduction; or
  - a public ruling states that the seam test discharges #1018 AC1 and AC2 for these sources.
- **Verification.** Each new plant fails its named check, and the unmodified head passes.

### F5 MINOR - Docs, Conformance - packet `review-evidence/usbnet-r1/author-r8/round5/HANDOFF-r5.md:45-51` - route and corner evidence for the current gateware is not public
- **Evidence.**
  - The handoff claims four routes passing Slow/Fast at 0/85 °C, a USB delta of +1,987 LUT, +1,685 FF and +4 BRAM tiles, and smallest setup/hold margins of 0.158/0.018 ns.
  - It links `receipts/ROUTES.md`, `CDC-FINDINGS.md`, `MAILBOX-WAIT.md`, `product-head-identity.json` and `source/pins.json`. None is published: the publication manifest lists only the three round-5 Markdown files, and no fetched ref carries them.
  - The route receipts that are published (`author/receipts/arty-route-*`) predate the fabric LEDs.
  - No `hdl/` or `sw/litex/` input changed after the round-5 routed head `ddda29e1`. The firmware ROM did change, from Arty ELF `f08cac5b` to `f17d1a9d`, and round 7 states that the earlier physical result is not promoted.
- **Impact.** A cold reviewer cannot check #1011 AC2 or #1018 AC3 (routing at every corner, and the cost band) for the gateware under review.
- **Note.** The PR body already says physical-route qualification remains open, so no false completion claim stands.
- **Required outcome.** Either the round-5 route receipts are published with their head and their equivalence to this head, or the PR and packet state that route evidence for this gateware is pending.
  - This needs no source change. Publication is the manager's.
- **Verification.** The linked receipts resolve in the published packet, and the per-corner slacks and utilisation agree with the handoff.

### R1 RESIDUE - Docs - `docs/design/USB_NET_PATH.md:13-14` - the build-scope sentence is too broad
- **The page says.** "It is built for the Arty only (`milan_soc.py --usb-net`, ...). No other board's build carries a line of it."
- **At this head.**
  - The status LEDs are built on every Arty build with the MAC, not only with `--usb-net` (`sw/litex/milan_soc.py:4153`, `:4447`). Without the tap, LD1 is held at 0.
  - The datapath's `o_led_*` level outputs exist on every board, unconnected.
- **Exact fix.** "The USB network path is built for the Arty only (`milan_soc.py --usb-net`, `sw/litex/usbnet_soc.py`). The status LEDs are on every Arty build with the MAC; without `--usb-net`, LD1 stays dark. Other boards carry only the datapath's unconnected `o_led_*` level outputs."

### R2 RESIDUE - Docs - `docs/design/USB_NET_PATH.md:146` - the injected-frame time is given without its rounding
- **The page says.** "1539 octets on the wire, 123.2 us." But 1539 × 80 ns is 123.12 us, and `tb/verilator/usbnet/egress_usb.py:24` charges 123.2 us rounded up.
- **Exact fix.** "1539 octets on the wire, 123.12 us, charged as 123.2 us (rounded up)."

### S1 SUGGESTION - Docs - `sw/litex/usbnet_soc.py:153-155`, `:8`, `:21`
- **Blank lines.** Three blank lines precede `@dataclass`, added in this delta. Commit `011aaa6f` removed the same pattern elsewhere.
- **Stale docstrings.** The module docstring's `add_usb_net(mac, platform, sys_clk_freq)` and `add_status_leds(soc, platform, sys_clk_freq, mac)` omit `repo_root`, `rx_dp_sys` and `inject_en`. This predates the delta.

### S2 SUGGESTION - Docs - packet `round8/receipts/DERIVATION.md` - "USB margin" is the margin over the injected measurement
- For six rows the figure derives from the Arty measurement, so the point's binding margin is smaller than stated. For `backlog.owed.if0` it is 0.14761 ms, not 0.22019 ms.
- Relabel the column, or add the binding margin (`receipts/ledger_probe.log`).

### S3 SUGGESTION - Conformance - #1011 AC1d (kept from R949-1 S1, optional)
- Record publicly how AC1d ("shaping unchanged in the existing harness with injection at its rate limit") is discharged: the tap harness's datapath-wait and priority checks, together with the unchanged CBS, shaper_core and queues suites.

### S4 SUGGESTION - Tests - the executor's final-head gate list
- The fourteen recorded final-head gates omit `scripts/ci_scope.py --selftest` and `scripts/suite_shards.py --selftest`, which would have caught F1 and F2.
- Add both whenever an edit touches a gate's read set or the suite inventory.

## Prior public findings at this head (read after my independent pass)

| Finding | Status | Evidence at `701f2944` |
|---|---|---|
| R949-1 F1 BLOCKER, suite not in the sweep | CLOSED | `scripts/suite_shards.py:148,152`; `scripts/run_all_suites.sh:302`; the tally reads usbnet at 92,759 checks and 0 failures. F2 is a new budget regression in the same area. |
| R949-1 F2 MAJOR, injection stops after a system-side reset | CLOSED | Four-phase flush, `hdl/usbnet/KL_usbnet_tx_arb.sv:94-121`; `tx_reset_domains` "one-sided reset resumes injection" (`sim_main.cpp:721-750`); plant `reset_flush_not_requested` caught |
| R949-1 F3 MINOR and R950-1-03 MINOR, RX length against the contract | CLOSED | `KL_usbnet_rx_copy.sv:45` = 1514; TX envelope 1515 with reason (`USB_NET_PATH.md:263-267`); boundaries 1513/1514/1515 RX and 1514/1515/1516 TX with recovery; plant `rx_maximum_ignored` caught |
| R949-1 F4 MINOR (a)(b)(c), untested rules | CLOSED | Plants `rx_header_length_ignored`, `tx_header_length_ignored` and `ld3_external_requires_stream` caught |
| R949-1 F5 MINOR, REBOOT page | CLOSED | `docs/design/REBOOT_RESET.md:110-113` |
| R949-1 R1 RESIDUE, LED clock comment | CLOSED | `hdl/usbnet/KL_status_leds.sv:37` "the SoC system clock" |
| R949-1 S1 SUGGESTION, AC1d mapping | KEPT (optional) | S3 |
| R949-1 S2 SUGGESTION, station record behind a waiting frame | CLOSED | Documented, `USB_NET_PATH.md:448-450` |
| R950-1-01 MAJOR, burst over the envelope after a hold | CLOSED | Reserved credit outside the refill ceiling (`KL_usbnet_tx_inject.sv`, `refill_cap_w`); `tx_held_envelope`; plant `pending_credit_refilled` caught |
| R950-1-02 MINOR, record terminator ungraded | CLOSED | Plants `record_terminator_missing` and `record_terminator_early` caught by "exactly one record terminator" |

## Lenses applied

- **Conformance (UNCLEAN: F3, F4, F5).**
  - Checked the rulings item by item: 7213370880 (LED predicates, identity), 7216971645 ((a)/(b) with the injected term) and 7234489667 (rule, figures, controls, inventory).
  - Checked the station record, LD1 and length limits against NETWORK.md.
  - Checked #1011 AC1a-c through the plants, and #1018 AC1 and AC2 (F4).
- **RTL (CLEAN).**
  - Read the delta of `KL_usbnet_local_rx`, `KL_usbnet_rx_copy`, `KL_usbnet_tx_inject`, `KL_usbnet_tx_arb`, `KL_usbnet_tap`, `KL_status_led_truth` and `KL_status_leds`; `milan_datapath.sv:4138-4144` with `media_clk_resolve`; `usbnet_soc.py`, `usbnet_local_soc.py` and the `milan_soc.py` hooks.
  - What I checked in that code:
    - merger lock through bubbles and the last byte;
    - discard rollback that keeps committed records;
    - serial-number freshness and the 18-bit expiry;
    - oversize records consumed with framing kept;
    - four-phase flush state machine and reset-less toggle;
    - reserved-credit ceiling;
    - LED predicates registered before two `MultiReg` stages;
    - `macsys` being a renamed `sys`.
  - lint_rtl and check_port_contracts pass. No finding.
- **Robustness (CLEAN).**
  - Malformed, short and oversize records; repeated, stale and wrapped sequences; zero heartbeat; MAC_VALID clear.
  - Full buffers, odd lengths and stalls; one-sided resets and abort.
  - Rate envelope after a hold; network priority at boundaries. These are covered by the passing suite and by caught plants. No finding.
- **Tests (UNCLEAN: F1, F2, F4).** My suite, plant, egress-plant, ledger and gate runs, listed above.
- **Docs (UNCLEAN: F1, F3, F5; R1 and R2 are residue).**
  - Read USB_NET_PATH.md sections 1, 3, 6 and 8, and the REBOOT_RESET, SYSTEM_INTEGRATOR, INTEGRATION_GUIDE, TESTING, MODULE_MATRIX and README-tests deltas.
  - Inventory freshness passes. The history is as ruled: `a4f00496` holds #1004's inventory byte for byte, and `701f2944` regenerates it with the generator.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3, F4, F5) | Rulings 7213370880 / 7216971645 / 7234489667; usb-audio `e3c87baf` `docs/NETWORK.md`; `KL_usbnet_tap.sv:194`; `KL_usbnet_tx_inject.sv` station parser; `USB_NET_PATH.md` sections 3 and 6; 159 `egress-cases` receipts; `egress_grade.py:40-43` | R949-2 | `701f294405d47a81eed1079d32b54e1eea4a4f31` |
| RTL | CLEAN | `hdl/usbnet/*.sv` delta; `milan_datapath.sv:815-820,1961-1997,4138-4144`; `KL_avtp_rx_monitor_ctx.sv:217,386`; `sw/litex/usbnet_soc.py:80-210`; `sw/litex/usbnet_local_soc.py`; `milan_soc.py` hooks; `receipts/gates/lint-rtl.log`, `port-contracts.log` | R949-2 | `701f294405d47a81eed1079d32b54e1eea4a4f31` |
| Robustness | CLEAN | `tb/verilator/usbnet/sim_main.cpp` (`rx_boundaries`, `tx_held_envelope`, `tx_reset_domains`, `local_tx_copy`), `sim_local.cpp`, `sim_wait.cpp`; `receipts/campaigns/usbnet-suite.log`, `mutants-72.log` | R949-2 | `701f294405d47a81eed1079d32b54e1eea4a4f31` |
| Tests | UNCLEAN (F1, F2, F4) | `receipts/campaigns/*`; `receipts/gates/*`; `receipts/ledger_plants.log`; `test_clock.cpp`; `scripts/ci_scope.py:70`; `scripts/suite_shards.py:57,148,152` | R949-2 | `701f294405d47a81eed1079d32b54e1eea4a4f31` |
| Docs | UNCLEAN (F1, F3, F5) | `USB_NET_PATH.md:13-14,55-79,146,198-216`; `SPLIT_CONTROL_MEMORY.md:3579-3580`; `REBOOT_RESET.md:110-113`; packet round 5 to round 8 handoffs; publication `MANIFEST.json`; `receipts/packet_verify.log` | R949-2 | `701f294405d47a81eed1079d32b54e1eea4a4f31` |

## Real limits

- No manager source bank exists at this head. I neither claim nor infer one.
  - I ran no full parent, PP, gPTP, Yosys or builder bank, no Docker or act, and no Vivado.
  - I did not rebuild the control ELFs. Identity rests on the author's rehashed builds, plus my check that every firmware and configuration input is unchanged.
- The census was not re-run.
  - The raw traces are hash-listed, not archived; ask the manager for them.
  - I re-derived the maximum wait and the wire expression from the 159 published per-case receipts only.
- **Hosted runs at the exact head.**
  - Executed: `changes`, which fails (F1); `docs-gates-0`, where `baremetal-only` fails and the job is then cancelled; and the aggregators, which fail.
  - Every Verilator, Yosys, firmware and union shard is SKIPPED, so no exact-head long-gate evidence exists (`receipts/hosted_checks.txt`). The manager owns hosted and act acceptance.
- **Inherited, #1004-owned.** `scripts/check_baremetal_only.py --check` fails here with five findings: `SPLIT_CONTROL_MEMORY.md:3501`, `ctrl_loop.h:355`, `ctrl_service_budget/README.md:49`, `arty_grade.py:52` and `egress_ledger.py:97`.
  - All five lines are byte-identical to `640699e6`, which fails identically (`receipts/gates/baremetal-only-1004head.log`).
  - They are out of this lane's scope, but the merge candidate stays red on them until #1004 resolves them.
- Physical calibration was NOT RUN. No bench, flash or route was run, and field skips are not hardware proof.

## Pending manager duties

- Publish the round-5 route receipts, or record route status as pending (F5).
- Validate the current-dev merge candidate. The source base is `c34e7d8b` and live dev is `e275d795`. Run the builder and native banks, and link their receipts.
- Accept hosted and act runs at a corrected head.
- Route the inherited `baremetal-only` findings to #1004.
- Carry R1 and R2 to the residue checklist.

R949-2 FINISHED
