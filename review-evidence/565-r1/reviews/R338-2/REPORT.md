[R338] POSITIVE - exact head 054e59b41471ffbb3b4999a60c4cb04abcfc895f

Round R338-2 is the internal independent review of issue #565 / PR #581.
Head `054e59b41471ffbb3b4999a60c4cb04abcfc895f`, tree `3a7593274d8872a75b2e28e2746ece9378e36706`: one commit on source base `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.
This round covered all five lenses: Conformance, RTL, Robustness, Tests and Docs. All five are CLEAN.
No BLOCKER, MAJOR or MINOR finding is open. Two SUGGESTIONs are recorded below. Both describe problems that existed before this PR and fall outside the frozen acceptance.

## Reconstruction

Sources, read in this order:
- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- Issue #565: the body and its three public comments (assignment 5848231174, TAKEN 5848248804, REVIEW READY 5848792439).
- PR #581: the body and its public comments.
- The build contract: `docs/integration/BAREMETAL_FIRMWARE.md:30-58`, with the timing history at `:1980-2002`.
- The capture harness README.
- `git diff 831f94f4..054e59b4` and the commit history.
- The public evidence packet at `8322c6de:review-evidence/565-r1`.

Frozen acceptance:
1. The 8x8 declares the clock its cacheless build is meant to close at, and every consumer of its `milan_clk_hz` is re-checked.
2. The note on that line says what it rests on.

Scope decision (assignment): change the value to 50 MHz with no closure claim, remeasure the capture gate, check the ROM ledger, and report on #231 without editing it.

Prior public findings on PR #581: none exist. R338-1 and R339-1 were voided before either reached a verdict (PR comment 5853095668), so there is nothing to carry forward or retain.

## Independent evidence (receipts under `receipts/`)

| Check | Method | Result |
|---|---|---|
| Config line | `configs/endstation_ax7101_8x8.yaml:55-56` | Reads `milan_clk_hz: 50000000  # BAREMETAL_FIRMWARE.md build contract (#565)`, with no closure claim. The `sys_clk_hz` note says "milan_soc.py default". The `audio_pll_hz` note (`:157-170`) states a contract, not closure. No other CLOSED claim appears in the file |
| Builder outputs, all five configs | Builder run at base and at head into scratch dirs (`builder-regen-rc.txt`, `builder-regen-sha256.txt`, `8x8-builder-before-after.diff`) | The other four configs: all 10 files byte-identical. 8x8: only these files change: `soc_params.json` (`--milan-clk-freq 100e6 -> 50e6`), `build_plan.md`, `lwsrp_table.json`/`.svh` (`CLK_FREQ_HZ_P`, `MILAN_CLK_FREQ_HZ`, `LWSRP_CLK_FREQ_C` 100000000 -> 50000000) and `gptp_ucode.hex` (`21e846a7...` -> `78c8418a...`, 13312 bytes each) |
| Sweep fragment (the 11th file) | `--write-fragment` for each config at base and at head, in a probe clone (`fragment-base-vs-head.txt`, `fragment-regen.txt`) | The other four configs are identical base vs head. The tracked `sweep_opts_arty.sh` and `sweep_opts_ax7101.sh` regenerate byte-identical from `arty_4x4` and `1x1_tdm8` |
| gPTP image | Generator arithmetic, `gptp-processor/hdl/ucode/gen_gptp_ucode.py:443-450` | Gain `round(2^24*512/clk)` goes 86 -> 172 and the limit 33554 -> 67109, as the PR states. The 8x8 head image equals the 1x1 image |
| LiteX gateware export, 8x8, base and head | `elaborate_8x8.sh` (no vendor tool, no software compile); `elab-8x8-file-compare.txt`, `elab-8x8-before-after.diff` | XDC byte-identical (21076 B). The only functional differences are `CLKOUT1_DIVIDE 16 -> 32`, `MILAN_CLK_FREQ_HZ 100000000 -> 50000000`, and the bridge watchdogs `12'd3072 -> 13'h1800` (6144), with counters widened from 12 to 13 bits. Every other difference is a timestamp or a path |
| Tree-wide consumer search | `consumer-search.txt` (141 lines, history excluded) | No consumer copies the 8x8 value as a hand-written literal. The suites include only `adp_shape_defaults.svh`, which is byte-identical. S2 covers two older hand-written AX literals that read no config |
| Capture input gate | `check_nvm_capture.py` and its four mutations (`capture-gate.log`) | PASS, rc 0; each mutation exits rc 1 |
| Gate fault probes | Probe clone (`capture-gate-probes.log`) | The pre-#565 receipt against the head config fails (rc 1). The head receipt with the 8x8 reverted to 100 MHz fails (rc 1). The restored copy passes. So the gate forced this remeasurement and now locks in the new clock |
| Harness edits are comment-only | AST comparison with docstrings masked (`code-edits-ast-compare.txt`) | `check_nvm_capture.py`, `recipe.py` and `soc.py` have ASTs identical to base |
| Receipt hashes | Recomputed at head | Harness hashes, `product_firmware_sha256`, per-arm `config_sha256` (8x8 `ede309aa...`, 1x1 `d2c757e2...`) and `processor_pins` all match the tree |
| Reproduced 8x8 arm | `run_capture_arm.sh`: 8x8 at 50 MHz, traffic ON, 16 captures, offline, Verilator 5.052, pinned SDK 14.3.0 installed from the pinned archive (`capture-8x8-50-on-*`) | rc 0. All 16 rows match the receipt cycle for cycle: minimum 24.29290 ms, maximum 24.30246 ms. Regraded, the maximum stays under 24.5 ms. The run consumed gPTP image `78c8418a...`, and its BIOS `f8aad0a0...` equals the receipt's |
| ROM ledger | The three default images regenerated at the pins (`rom-ledger-check.txt`) | `ltn_rom.hex`, `ucode.hex` and `gptp_ucode.hex` all match `syn/yosys/rom_digests.tsv`. `ooc.sh` uses generator defaults, so the config clock cannot reach the ledger. The PR leaves `rom_digests.tsv` unchanged |
| Bridge precedence at the new clock pair | The unmodified `test_precedence`, with (sys 100, milan 50) appended in memory (`probe-bridge-precedence.log`) | 20/20 checks pass. Bridge 61440 ns vs processor 81920 ns; the error beat lands at cycle 6147 of 8192 |
| Repository gates | `doc-gates.log`, `lint.log` | `docs_check`: 0 findings. `check_em_dash --base 831f94f4`: 0 findings over 18 added lines, arms 339/339. `check_doc_style` OK. `gen_toc --check` OK. `--verify-anchors`: 176 reproduced. `check_doc_paths` OK. `lint_rtl --check` PASS (90 <= 90). `git diff --check` rc 0 |
| Commit shape | `git log -1 --format=%B` | One line, no trailers, direct child of base |
| Clone integrity | `verify_clone_integrity.sh` (`clone-integrity.txt`) | HEAD, tree and index equal the reviewed head. All 908 tracked blobs and modes match. No hidden index flags. The three gitlinks are at their pins and clean. No untracked files |

## Assignment focus items

1. **Config line and note:** correct, with no closure claim. The other 8x8 clocks carry no stale CLOSED claim.
2. **Consumers:** re-derived with before/after values, as the builder, fragment, gPTP, gateware and consumer-search rows show. The other four configs' generated artifacts are byte-identical, 11 files each.
3. **Capture gate:**
   - The receipt's rows, maxima and digests are refreshed, and so is section 18.
   - The gate logic is unchanged, and the rerun passes.
   - One 8x8 arm was reproduced identically.
   - The 8x8 peak at 50 MHz is 24.30246 ms, 0.19754 ms under the 24.5 ms bar.
   - The gate still requires the labelled 100 MHz point (`scripts/check_nvm_capture.py:68-69`).
4. **ROM ledger:** the statement "no re-recording needed; images use generator defaults" is correct.
5. **#231 report:** accurate. At `ae729bbf`, `docs/findings/PP_SHADOW_BASELINE.md` records the following. All of it describes the 100 MHz recipe, and none of it is required here.
   - `:45`: the 8x8 timer at 100 MHz.
   - `:97`: the integrated 8x8 runs at 100 MHz.
   - `:73`: 68,136 LUT and -11.331 ns.
   - `:60`: a separate 10 ns standalone constraint.
   - `:102-104`: no placement result.
6. **Repository gates:** every gate this round ran passes (see the repository-gates row).
   - Hosted exact-head check runs are in `hosted-check-runs.tsv`. Every executed job concluded success.
   - `Physical gPTP (nightly and manual)` was skipped and counts as no evidence.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

**S1** (SUGGESTION; lenses Docs and Conformance)

```text
[R338] SUGGESTION Docs, Conformance - docs/integration/BAREMETAL_FIRMWARE.md:33,43 - build contract claims enforcement of the 50 MHz clock that no gate performs
Requirement/evidence: :33 says the builder and milan_soc.py "both reject a bare-metal profile unless all of these statements hold", and :43 lists the 50 MHz Milan/CPU clock. The builder checks only milan_clk_hz <= sys_clk_hz (sw/builder/endstation_builder.py:3772-3773). At base, the bare-metal 8x8 at 100e6 built with rc 0 in both the builder and the milan_soc.py export (builder-regen-rc.txt, elab-8x8 base run). sw/builder/test_builder.py:17109-17110 builds a bare-metal variant at 80 MHz. The claim predates this PR (a33c78f3/1e80a106), and the PR's own consumer table describes the loader correctly.
Impact: configuration-time checks do not refuse the #565 class of drift. For the two AX shapes, the hosted capture input gate now catches a revert (capture-gate-probes.log, probe B). Another bare-metal shape would not be caught.
Required change: none for this PR. Recommend a new Issue that decides between enforcing the contract clock in the builder and rewording :33.
Verification: a planted non-50 MHz bare-metal config is refused, or the paragraph no longer claims refusal.
```

**S2** (SUGGESTION; lenses Tests and Docs)

```text
[R338] SUGGESTION Tests, Docs - sw/litex/test_pp_mem_bridge.py:382-392; sw/litex/sweep_extra.sh:13 - hand-written AX clock pairs match no tracked configuration
Requirement/evidence: the precedence test says it covers "Every shape this tree actually builds". It lists AX sys/milan 100/100 as "shipping" and omits 100/50, the pair both AX configurations declare at this head. sweep_extra.sh hard-codes --milan-clk-freq 100e6 for ax7101. Both predate this PR: the shipping 1x1 moved to 50 MHz in 1e80a106. Neither reads the 8x8 configuration. A probe running the unmodified precedence test with 100/50 appended passes 20/20 (probe-bridge-precedence.log). milan_soc.pp_mem_timeout_cycles refuses a violating pair at elaboration.
Impact: none observed. The race is untested at the pair the AX shapes actually build, and an extra-directive sweep would build a clock that no configuration declares.
Required change: none for this PR. Recommend a new Issue to derive both lists from the configurations.
Verification: the precedence test enumerates the configured pairs, and sweep_extra.sh sources the generated fragment.
```

## Clean-lens results

```text
[R338] PASS Conformance - configs/endstation_ax7101_8x8.yaml:55-56; tb/verilator/nvm_capture_cpu/measurements.json; receipts/capture-8x8-50-on-compare.txt; receipts/8x8-builder-before-after.diff - acceptance 1-2 and assignment items 1-5 checked against issue #565 and comment 5848231174: 50 MHz declared with a basis and no closure claim, consumers re-derived, capture maximum 24.30246 ms <= 24.5 ms reproduced, ROM-ledger and #231 statements accurate
[R338] PASS RTL - receipts/elab-8x8-before-after.diff; sw/litex/milan_soc.py:238-251,2164-2213; receipts/capture-8x8-50-on-run.log - no RTL source changed; derived elaboration at 50 MHz gives PLL divide 32, MILAN_CLK_FREQ_HZ 50000000 and watchdog 6144 in 13-bit counters, with the XDC unchanged; the milan-domain CDC structure matches the shipping 1x1; the full 8x8 SoC at a 50 MHz Milan clock elaborates and builds under Verilator 5.052 with USERERROR fatal
[R338] PASS Robustness - receipts/probe-bridge-precedence.log; receipts/capture-gate-probes.log; receipts/capture-8x8-50-on-compare.txt - bridge-before-processor precedence and the bus-wait floor hold at 100/50; a reverted or stale clock input fails the gate; both traffic arms stay under the half-floor; no PPS flag is generated for this shape and latency taps are pruned; a lower clock only lengthens cycle-derived intervals
[R338] PASS Tests - scripts/check_nvm_capture.py (rerun, four mutations, three fault probes); receipts/code-edits-ast-compare.txt; receipts/capture-8x8-50-on-measurement.json - the gate fails on the defects it guards against (stale receipt, reverted clock); harness and gate logic unchanged; the reproduced arm matches the receipt row for row; shape-reading suites consume only the byte-identical adp_shape_defaults.svh
[R338] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:55-57; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1600,1737-1750; tb/verilator/nvm_capture_cpu/README.md:40-49,137; hdl/ieee1722/aaf/README-parameters.md:29; receipts/doc-gates.log - every changed statement checked against the receipt and the generated artifacts; no current document still places the 8x8 at 100 MHz outside the labelled non-contract comparison; all documentation gates pass
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | config line, issue acceptance and assignment, builder outputs before/after, receipt, reproduced arm, ROM ledger, #231 baseline at `ae729bbf` | R338-2 | `054e59b41471ffbb3b4999a60c4cb04abcfc895f` |
| RTL | CLEAN | 8x8 gateware export base vs head, `milan_soc.py` clock and watchdog derivation, Verilator elaboration of the 8x8 SoC at 50 MHz | R338-2 | `054e59b41471ffbb3b4999a60c4cb04abcfc895f` |
| Robustness | CLEAN | bridge precedence probe at 100/50, gate fault probes, both-arm half-floor bound, feature-dependent PPS/latency-tap pruning | R338-2 | `054e59b41471ffbb3b4999a60c4cb04abcfc895f` |
| Tests | CLEAN | capture gate, mutations and fault probes, harness AST identity, reproduced 8x8 50 MHz ON arm, suite shape inputs | R338-2 | `054e59b41471ffbb3b4999a60c4cb04abcfc895f` |
| Docs | CLEAN | five changed Markdown/comment files, tree-wide clock-statement search, documentation gates | R338-2 | `054e59b41471ffbb3b4999a60c4cb04abcfc895f` |

The SUGGESTIONs do not affect coverage.

## Real limits

- Only one of the six capture arms was reproduced: 8x8, 50 MHz, traffic ON, the published peak. The other five rest on the public receipt and packet.
- The pinned Verilator 5.050 was not at its named path on this host. The capture used Verilator 5.052, the version the receipt records, and lint used the installed 5.052.
- One capture arm takes longer than a single command may run. It therefore ran as a detached process while this round blocked in the foreground until it exited. It finished (rc 0) before any verdict, and nothing from this round is still running.
- The Markdown renderer gates ran under an existing interpreter that carries the pinned `cmarkgfm` release. The scripts refuse any other release.
- Out of this round's scope, and not run: the full builder bank, the sweep shards, Yosys, the source bank, act and the hosted jobs. Their evidence belongs to the manager.
- Physical calibration and placement were NOT RUN. Simulation timing is not silicon timing, and no closure claim exists for the 8x8 at 50 MHz.

## Pending manager duties

- Build and validate the final candidate on live dev `8c8e7bb05aa50d840a84394e44659dc9c46b9639`. The source base was `831f94f4`.
- Own hosted and act acceptance at the exact head, keeping executed jobs separate from skipped contexts.
- Record the source-bank result at this head.
- Track the #231 re-run follow-up at 50 MHz.
- Decide whether to open Issues for S1 and S2.
- Obtain the external review. A merge needs explicit maintainer authorization.

R338-2 FINISHED
