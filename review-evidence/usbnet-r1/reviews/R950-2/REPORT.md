[R950] NEGATIVE - exact head 701f294405d47a81eed1079d32b54e1eea4a4f31

Round R950-2, external independent source review of PR #1020, relating to #1011 and #1018. Tree: `d3ea9ebf7db3d37e41629adb27ac9003060f33c5`.

All five lenses were applied. The three R950-1 findings are closed at their causes. R949-1 F1 remains blocking: registration and tallying were repaired, but the resulting CI assignment fails its mandatory budget self-test. One additional MINOR concerns an obsolete quantitative ACMP margin. One PR-body RESIDUE is recorded. No source fix or GitHub write was made.

## Scope and reconstruction

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, issue bodies and public decisions, relevant requirements/interface authorities, then the requested diff and history. The independent implementation pass preceded reading prior public finding comments. No other current review report, private author material or management source tree was read.

The requested source range is `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350..701f294405d47a81eed1079d32b54e1eea4a4f31`; the later-round comparison starts at `cc49123d2db1e01e80859efa10f8da43a01344ef`. The separately reviewed #1004 dependency is `640699e6866602b2a5de5d404c43f3bd4df8037c`. Its content was checked for identity, not re-reviewed. `source-range.txt`, `review-delta.txt`, `public-context.json` and `receipt-audit.json` record these boundaries.

Authorities applied:

- [#1011](https://github.com/kebag-logic/milan-fpga/issues/1011), its station amendment and local-forwarding rulings: both local directions, control-only filters, checked source identity, reserved destinations, PCP 0/1, best-effort priority and rate limiting.
- [#1018](https://github.com/kebag-logic/milan-fpga/issues/1018), amended by the [fabric LED ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880): LD2 input media lock or output transmit permission; LD3 internal selection or the appropriate selected-source lock. No firmware LED work.
- [100 Mb/s ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645): preserve free-space outcomes or rerun the census at link rate; include injection, fixed path and handshake within 1000 us.
- [USB held-egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667): a separate USB point using per-row maxima; only the last AECP figure becomes 62.14 ms. Existing points and owner bounds remain unchanged.
- REQUIREMENTS.md sections 5/6/8, especially shipping-CBS scope, REQ-CLS-03/06/09 and REQ-VER-*; FR_NFR.md 3.4.1; USB_NET_PATH.md; REBOOT_RESET.md; SPLIT_CONTROL_MEMORY.md section 15; [usb-audio NETWORK.md at da91f599](https://github.com/kebag-logic/usb-audio/blob/da91f5999a31d0965872ff153194ee817d1106d1/docs/NETWORK.md).

The owner-approved fabric LED semantics govern this review. GPIF attachment, board operation and physical acceptance remain open. This verdict is not issue completion or merge acceptance.

## Findings

### R950-2-01 - BLOCKER - Tests, Docs

**Artifact:** `scripts/suite_shards.py:148`, `:874`; `scripts/run_all_suites.sh:343`; `.github/workflows/rtl.yml:344` and `:624`; `suite-registration.log`, `shard-budget-differential.json`.

**Title:** Mandatory shard self-test still fails after USB registration. This retains R949-1 F1's unresolved sweep-integration obligation.

**Authority/evidence:** CONTRIBUTING.md requires the local sweep and exact-head verification. R949-1 F1 explicitly required the registration fix to preserve the shard budget. At this exact head, `python3 -B scripts/suite_shards.py --selftest` exits 1:

```text
FAIL head worker 25/27 predicted 1299 s (21.6 min), bound 1276 s
selftest: 1 FAILURE(S)
```

The independent differential uses the dependency's own scheduling code/workflow and inventory, then the head's. The dependency has no scheduling problem and predicts worker 25 at 1275 s. The head predicts 1299 s, 23 s over the unchanged absolute cap. Its worker 25 contains `capture_coherence__5`, `pp_shadow__1`, and `avtp_rxmon`. USB is on worker 12, but adding it changes the overall assignment. This is deterministic scheduling arithmetic, not an execution-speed measurement or environmental failure. `probe_shard_budget.py` reproduces it without running any bank.

**Impact:** the mandatory sweep aborts at preflight with exit 2 before executing suites. Workflow preflight also invokes the failing check. The table entry, suite indexes and tally shapes are fixed, but they do not close F1 while this gate remains red.

**Required outcome:** integrate USB with a complete, disjoint assignment meeting existing absolute and timeout budgets and preserving special owners. Do not weaken the cap or omit suites. Keep generated workflow/contract artifacts consistent.

**Verification:** exact-head self-test exits 0, every worker meets its applicable bound, and selection/ownership controls pass. The manager then obtains required full local and hosted evidence. No full sweep was run here.

### R950-2-02 - MINOR - Conformance, Docs

**Artifact:** `docs/design/USB_NET_PATH.md:78`; `docs/design/SPLIT_CONTROL_MEMORY.md:3580`; public `author-r8/round8/receipts/owner-model.json`; `receipt-audit.json` (`acmp_composition`).

**Title:** Local-receiver ACMP composition uses a superseded service row and overstates its margin by 70 us.

**Authority/evidence:** USB_NET_PATH.md adds 38.075 us to “#1004's 29.77 ms” and claims 29.808075 ms, leaving 191.925 us. The merged dependency's current authoritative row is 29.84 ms, also used by the final owner model. Its receipt already states `acmp_with_local_mailbox_ms: 29.878075`. Independent arithmetic gives:

```text
29.84 ms + 3046 / 80,000 ms = 29.878075 ms
30 ms - 29.878075 ms = 121.925 us
```

The measured mailbox wait remains 1707 cycles and its conservative allowance remains 3046 cycles.

**Impact:** the current design page's composition and remaining numerical margin are false. The corrected composition still fits 30 ms; no deadline violation is alleged. This is MINOR, not wording-only RESIDUE, because correction changes a quantitative conformance claim.

**Required outcome:** replace 29.77, 29.808075 and 191.925 with 29.84, 29.878075 and 121.925 respectively, tied to the current qualified row. Preserve the wait measurement and all bounds.

**Verification:** compare the amended paragraph against section 15 and the final owner model, then recompute the sum and margin. This documentation correction alone requires no native census rerun.

### R950-2-R1 - RESIDUE - Docs

**Artifact:** current PR #1020 body, first paragraph, captured in `public-context.json`.

**Authority/evidence:** CONTRIBUTING.md section 2.1 requires role prefixes on PR bodies and comments. This body begins “The USB network path copies...” without one.

**Impact:** attribution convention only; no measurement, code, test, clause claim or privacy rule changes.

**Exact fix:** prefix the manager-maintained body with `[A10] `, matching the manager's public identity. If the executor republishes it, use that executor's established `[A<n>]` prefix instead.

**Verification:** inspect the first line. The manager may carry this residue on the residue checklist; it affects neither verdict nor coverage.

## Prior public findings

Read after the independent diff pass: [R950-1](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7188465679) and [R949-1](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7188657186). Dispositions are based on causes and executable evidence.

| Prior ID | Disposition | Evidence at this head |
|---|---|---|
| R950-1-01 | CLOSED | `KL_usbnet_tx_inject.sv:327` onward reserves pending cost outside the refill ceiling until PHY retirement; the tap connects retirement/abort. `sim_main.cpp:617` checks every departure interval after disabled injection, arbitration delay and MAC stalls with short/maximum sizes. Fresh baseline passes; published `pending_credit_refilled` fails its named envelope assertion. |
| R950-1-02 | CLOSED | `sim_main.cpp:329` grades exactly one accepted final-word terminator; the observer checks stalled stability. Missing/early-marker plants fail their named checks; fresh baseline passes. |
| R950-1-03 | CLOSED | `KL_usbnet_rx_copy.sv:45` defaults to 1514; `KL_usbnet_local_rx.sv:62` permits 1515 locally; injection's envelope is 1515. USB_NET_PATH.md sections 2/4 match the adopted direction-specific contract. Boundary/recovery checks pass; maximum-removal plant is caught. |
| R949-1 F1 | OPEN: R950-2-01 | Inventory registration, indexes, recognised tallies and `--ci-pieces --shard 0/27` work. The mandatory scheduling self-test still fails its head budget. |
| R949-1 F2 | CLOSED | `KL_usbnet_tx_arb.sv:94` onward adds four-phase cross-domain flush and preserves the reset-less end toggle. `sim_main.cpp:721` covers either domain alone, both request parities, active/idle operation. Fresh baseline passes; flush-removal plant fails the intended recovery assertion. |
| R949-1 F3 | CLOSED | Same direction-specific limit and boundary evidence as R950-1-03. |
| R949-1 F4(a,b) | CLOSED | Short Ethernet/AVTP/C-tag/S-tag cases exercise header-length refusal. RX/TX header-length-removal plants fail their named assertions. |
| R949-1 F4(c) | CLOSED by approved replacement | Firmware LED observer removed. `KL_status_led_truth.sv:26` gates external selection on clock lock; all 64 input combinations are tested. `test_clock.cpp:57` exercises an external descriptor through the real command fixture with explicit lock levels. Lock-removal plant is caught. |
| R949-1 F5 | CLOSED | `REBOOT_RESET.md:110` names the USB arbiter's ownership and exclusion of injected frame ends. |
| R949-1 R1 | CLOSED | `KL_status_leds.sv:37` now says “the SoC system clock.” |
| R949-1 S1 | Retained optional acceptance mapping | REQUIREMENTS.md section 5, USB_NET_PATH.md sections 3/8 and unchanged shaper receipts distinguish the unshaped product trunk from retained CBS blocks. A public manager statement mapping this evidence to AC1d remains useful. |
| R949-1 S2 | CLOSED by documentation | USB_NET_PATH.md's final paragraph states that a frame waiting for space delays station records while freshness continues to expire. |

The former local-path and station-format open scope is implemented. GPIF attachment and physical operation remain open, as the PR body states.

## Applied lenses

**Conformance:** applied adopted record framing, station fields, sequence/freshness/detach, directional size limits, filter ordering, local delivery and injection rules to `KL_usbnet_pkg.sv`, `KL_usbnet_tx_inject.sv`, `KL_usbnet_tap.sv`, `KL_usbnet_local_rx.sv` and USB_NET_PATH.md. Fabric LED predicates implement the approved replacement semantics. Applied the wire allowance and held-egress ruling; seven ledger misses remain misses of original budgets. R950-2-02 leaves this lens unclean.

[R950] PASS RTL - `hdl/usbnet/KL_usbnet_tx_arb.sv:94`, `KL_usbnet_tx_inject.sv:327`, `KL_usbnet_local_rx.sv:62`, `hdl/milan/milan_datapath.sv:4138`, `sw/litex/usbnet_soc.py:165`, `sw/litex/usbnet_local_soc.py:19` - checked reset flushing, reserved credit, speculative rollback, whole-frame arbitration, coherent station-address crossing and registered LED predicates against interfaces/rulings. Local copies observe accepted injections without feeding MAC backpressure; the mailbox merge grants whole frames with network priority. Six status outputs read existing fabric levels; completed predicates cross independently through two synchronizer stages. Control firmware/configuration and gitlinks equal #1004. No source correctness defect found; physical-route limitations remain below.

[R950] PASS Robustness - `tb/verilator/usbnet/sim_main.cpp:358`, `:482`, `:617`, `:721`; `sim_local.cpp`; `sim_wait.cpp`; `sim_truth.cpp`; `KL_usbnet_tx_inject.sv:211` - checked malformed/maximum records, stale/duplicate/older station sequences, detach/expiry, oversize recovery, either reset domain and request parity, FIFO pressure, stalled records, cancelled local fragments, preserved completed copies and mailbox arbitration. Fresh focused execution passes 92,497 checks. The actual mailbox harness observes 1707 cycles against 3046. Physical clock-loss/restart and an attached GPIF master were not exercised.

**Tests:** `receipt-audit.json` checks all 72 published plant logs for the intended failure and unique current source anchor. RTL, baseline tests and mutation table are byte-identical from measured merge `91252ecf7457287079d5d2f794b8544f0d9d34c4` to this head (`retained-inputs.json`). Fresh `tap`, `leds`, `truth`, `local` and `wait` runs pass with verified scoped compiler version 5.050. `focused-tally.json`: 92,497 checks, zero failures, no unparsed tally or NOCOUNT. Retained production attachment contributes 258 checks and real SET_CLOCK_SOURCE fixture four cases; inspected, not rerun. The fixture supplies lock levels explicitly and is not a complete processor/MMIO simulation. Fresh ledger self-test passes 218 control executions and catches 25 mutations; all 18 injection controls pass freshly. The 72-plant campaign was checked from individual receipts, not rerun. R950-2-01 leaves this lens unclean.

**Docs:** compared USB design, reset, clock-domain and integration-port contracts against the implementation and public scope. Contents/fragment repair and `MAX_LEN_OCTETS_P` rename retain approved limits. Inventory regeneration is its own commit; fresh `docs_inventory.py --check` passes. Final-head public receipts cover locked Contents controls, anchors and naming gates. No new prohibited bench-lane/review identifier was found in scoped source comments. R950-2-01 retains the earlier documentation/integration obligation; R950-2-02 is a quantitative documentation defect.

## Census, identity and publication audit

Evidence source: [ab597339 / review-evidence/usbnet-r1](https://github.com/kebag-logic/milan-fpga/tree/ab5973396472f63221353992cf287b03b01222a8/review-evidence/usbnet-r1), principally `author-r8/round7/receipts` and `author-r8/round8/receipts`. All 1293 extracted author artifacts covered by the publication manifest match their published SHA-256. No review directory was extracted. Redacted files are judged against published, not pre-redaction, digests.

This verifies a content-addressed/hash-bound publication, not a signature: the commit has no signature header and no detached signature was supplied. `publication-integrity.json` records that distinction.

`receipt-audit.json` independently verifies:

- Thirteen protected dependency files match #1004 and receipt hashes. Firmware/configuration paths and every gitlink have no delta against #1004. Inventory is the authorised generated exception; the separately authorised ledger extension is reviewed above.
- All six retained map-header artifacts rehash correctly. Receipts report equal baseline/candidate ELF hashes at the same pins: Arty `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf`; ALINX 1x1 `6e0a54124483adfadd04e8e6f62d296bdf884794b197d0ed9dc24c71de49fd56`; ALINX 8x8 `0f1450acefdd7fa0173d1de3221f8c5a6456e59d96fc99611b5121b1c26a2c3f`. Binaries are omitted from the publication: these are checked receipt claims supported by unchanged inputs, not independently rehashed ELF pairs or new builds.
- All 159 per-case replay receipts match hashes, trace identities, completion entries and source/parameter bindings across eight images. Every reported native departure disagreement is zero. Recomputing the aggregate gives `(558.835 + 54.88) * 1.05 + 0.32 + 0.26 = 644.98075 us`, within 1000 us.
- The 512 raw shipping-chain handshake rows contain the full eight-length/eight-by-eight-phase population. Maximum 257500 ps rounds up to 260 ns. Generated chain and its ten source hashes match. Fixed path remains the inherited 320 ns; the dependency's implementation was not re-reviewed.
- Retained results pass at `arty-usbnet-1x1` and still fail at `arty-1x1` for 62.03635 ms against 61.99 ms. Fresh controls accept exactly 62.14 ms and reject one 80 MHz cycle over it. Existing ledger points remain unchanged.

The live injected census supersedes the failed carry attempt: published replay identifies changed free-space outcomes, followed by the complete injected queue census with new firmware-visible tails. Instant-egress results are not treated as equivalent. Final owner model: load 0.501397114035, ACMP 29.84 ms, txL 48.90 ms, last notice 117.58 ms and longest pass 1.7923875 ms, within unchanged 0.70 / 30 / 49 / 140 / 2 limits. These are desk/model results, not physical calibration.

Raw traces are hash-listed but absent. The manager was asked for an approved scratch copy for a focused spot-check; none was supplied during review. No fresh trace replay, native census or raw-trace rehash is claimed. The source logic, complete bound receipt population, aggregate arithmetic and negative controls were checked instead.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R950-2-02) | #1011/#1018 rulings; NETWORK.md; USB_NET_PATH.md; FR_NFR.md 3.4.1; scoped USB RTL; receipt-audit.json | R950-2 applied; no clean coverage | 701f294405d47a81eed1079d32b54e1eea4a4f31 |
| RTL | CLEAN | hdl/usbnet/*.sv; datapath/status exports; usbnet_soc.py; usbnet_local_soc.py; REBOOT_RESET.md; dependency/source identities | R950-2 | 701f294405d47a81eed1079d32b54e1eea4a4f31 |
| Robustness | CLEAN | sim_main.cpp held/reset/boundary cases; sim_local.cpp; sim_wait.cpp; sim_truth.cpp; rtl-focused.log; named plant receipts; injection-controls.log | R950-2 | 701f294405d47a81eed1079d32b54e1eea4a4f31 |
| Tests | UNCLEAN (R950-2-01) | suite_shards.py; run_all_suites.sh; rtl.yml; focused-tally.json; ledger-controls.log; receipt-audit.json; shard-budget-differential.json | R950-2 applied; no clean coverage | 701f294405d47a81eed1079d32b54e1eea4a4f31 |
| Docs | UNCLEAN (R950-2-01, R950-2-02) | USB_NET_PATH.md; SPLIT_CONTROL_MEMORY.md; reset/clock/integration documents; inventory; PR body; public receipts | R950-2 applied; no clean coverage | 701f294405d47a81eed1079d32b54e1eea4a4f31 |

## Limits and pending manager duties

The round-5 public handoff reports four Arty routes, three USB-enabled and a matched disabled comparison, passing Slow/Fast at 0/85 C. It reports +1987 LUT, +1685 registers, +4 block-RAM tiles, zero added DSP, minimum setup/hold 0.158/0.018 ns, and whole-image CDC/external-I/O limitations. Underlying route receipts are absent under `author-r8/round5` in this publication. They were requested but not supplied. The older root `author` routes concern the previous implementation and cannot establish the later routes. Thus this is inspected author testimony, not independently verified four-corner raw evidence or a final-head route. The current PR explicitly keeps physical-route qualification open. The manager must supply current input binding and adjudicate cost against the original approximate band at that gate.

Physical calibration NOT RUN. Field skips and desk evidence are not hardware proof. The terminated bus still holds LD1 down. GPIF scheduling/wiring, saturated bidirectional networking with clean audio counters, controller operation and each LED observed on the board remain open.

Read-only hosted snapshot: 58 contexts, comprising 11 success, 12 failure, 26 skipped and 9 cancelled. Required `rtl-fast`, `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability` report failure; `wire-accountability` and `docs-check-no-git` report success. The Verilator preflight and matrix execution context are skipped. Failed aggregates and skipped jobs are not executed-bank evidence. `hosted-contexts.json` preserves job links. No hosted failure cause is inferred from the local shard finding.

No manager source bank exists at this head and none is claimed. The manager owns hosted/local workflow acceptance and the final current-dev merge candidate's builder/native banks. Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`; supplied live-dev reference: `e275d7950ef3385753e6a15d2e191ba855b171ed`, to be refreshed at merge turn. Candidate validation, fix re-review, two positive independent verdicts, reviewer-accepted completion ledger, authorised merge and containment remain pending.

No full parent/processor/synthesis/builder banks, physical builds, hardware, container workflow replicas, shared installs, author contact or sub-agents were used. All invoked checks terminated. Foreground orchestration awaited bounded concurrent checks, with at most ten compilation jobs and no detached background campaign.

`tree-verification.json` proves all 2041 parent tracked blobs, modes and index entries against the exact head, plus tracked bytes/modes/index entries of five populated dependencies at required gitlinks. Unused external remains unpopulated. No tracked source was modified. Disposable artifacts are under `scratch/`, excluded from publication. `MANIFEST.sha256` lists publishable scripts and receipts. Public diagnostics use role placeholders for execution paths.

R950-2 FINISHED
