[R339] NEGATIVE - exact head 054e59b41471ffbb3b4999a60c4cb04abcfc895f

External independent review R339-2 of issue #565 / PR #581. Head `054e59b41471ffbb3b4999a60c4cb04abcfc895f`, tree `3a7593274d8872a75b2e28e2746ece9378e36706`, source base `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`. One commit, nine files.

Verdict basis: one open MINOR (F1, `Docs`). Everything else checked out. The frozen acceptance criteria are met. Every consumer of the 8x8 `milan_clk_hz` that I derived independently agrees with the published before/after table. The capture receipt reproduces row-for-row at the arms I could run.

## Reconstruction order

1. Read AGENTS.md, CONTRIBUTING.md (by reference), `docs/integration/BAREMETAL_FIRMWARE.md#build-contract`.
2. Read issue #565: the body, the assignment and decision in comment 5848231174, TAKEN, and REVIEW READY.
3. Read the PR #581 body and the manager comments. R338-1 and R339-1 are recorded as VOID.
4. Read `git diff 831f94f4..054e59b4` and the history.
5. Read the public evidence at `8322c6de:review-evidence/565-r1/author/`.
6. Checked prior public review findings on #581 only after my own pass. There are none: no `[R…]` comments, no reviews, no inline comments. Nothing needs to be resolved or retained.

## Findings

### F1 - MINOR - Docs - `docs/integration/BAREMETAL_FIRMWARE.md:33` with `:43` - the build contract claims tooling rejects a non-50 MHz bare-metal profile, and neither tool does

- **Authority/evidence:**
  - `:33` says: "The builder and `milan_soc.py` both reject a bare-metal profile unless all of these statements hold". One of those statements (`:43`) is "The cacheless CPU side and the 64-bit Milan plane run at 50 MHz."
  - Neither tool checks the clock:
    - The builder's bare-metal checks (`sw/builder/endstation_builder.py:4224-4230`) cover only CPU/XLEN/harts, L2/scala_args and flashboot.
    - The `milan_soc.py` checks (`sw/litex/milan_soc.py:3683-3688`) cover only CPU/XLEN/harts, FPU, L2 and scala_args.
  - The lane's own base proves it. At `831f94f4` the builder accepted the bare-metal 8x8 at `milan_clk_hz: 100000000` (rc 0, `receipts/builder-base-8x8.log`). My gateware export ran `milan_soc.py --software-profile baremetal --milan-clk-freq 100e6` with rc 0 (`receipts/board-export-diff.txt`).
  - `sw/builder` and `sw/litex` are unchanged between base and head, so the same is true at head.
  - The PR edits this section (`:55-57`) and cites it as the basis for the new yaml note. It still leaves the reader believing the clock is enforced. That missing check is exactly how #565's condition went unnoticed.
- **Impact:**
  - The authoritative contract misstates what the tooling guarantees.
  - A future bare-metal shape that declares a clock other than 50 MHz passes the builder and SoC generator silently.
  - For the two measured shapes the capture gate would catch such a change. For any other shape nothing would. A reader of the contract has no way to know this.
- **Required outcome:** the build contract separates the invariants the builder/`milan_soc.py` actually reject from the 50 MHz clock, which is a declared target that the tools do not check. Adding the check instead would be new work under a new Issue. That is a maintainer's call; the doc must not claim enforcement that does not exist.
- **Verification:** re-read `BAREMETAL_FIRMWARE.md#build-contract` at the new head against `endstation_builder.py:4224-4230` and `milan_soc.py:3683-3688`. Alternatively, if a check is added, run the builder on a bare-metal yaml probe with `milan_clk_hz: 100000000` and expect a refusal.

### F2 - SUGGESTION - Docs - `hdl/ieee1722/aaf/README-parameters.md:37` - "the 100 MHz AX build" wording

The PR made the sibling `CLK_FREQ_HZ` row shape-derived (`:29`). The derived-localparam row still says "the 100 MHz AX build needs it re-derived". No configured AX shape runs at 100 MHz any more. The only 100 MHz AX path left is the un-configured `milan_soc.py` default, the bring-up profile. Optional: state the rationale without naming a board clock. This does not affect coverage.

### F3 - SUGGESTION - Robustness - builder bare-metal validation (`sw/builder/endstation_builder.py:4224`)

Optional new Issue: have the builder refuse a bare-metal profile whose `milan_clk_hz` differs from the contract clock. That would turn F1's documentation into an executable guard. This PR does not require it.

### Observations outside this lane's scope (not findings)

- `docs/AAF_LATENCY_TAPS.md:15` says "100 MHz on the AX7101 ⇒ 10 ns/cycle". The only AX shape with latency taps is the 1x1 (`latency_taps: true`), which moved to 50 MHz before this lane. This is pre-existing, owned by the 1x1 history, and a candidate for its own Issue.
- The capture harness writes the ignored `configs/generated/ltn_rom.hex` and `ucode.hex` into the checkout. This is pre-existing harness behaviour, and those files are untracked. I removed them after my probes.

## Clean lens results (same evidence format)

```text
[R339] PASS Conformance — configs/endstation_ax7101_8x8.yaml:56; issue #565 acceptance 1-2 and assignment 5848231174 items 1-5 — value 50000000 matches BAREMETAL_FIRMWARE.md:43; the note cites the contract and #565 and makes no closure claim; sys_clk_hz (:55 "milan_soc.py default"), audio_pll_hz (:157 "24.576 MHz BY CONTRACT") and the datapath_probes history (:48-52) carry no CLOSED claim; the derived PHC reset increment is 20 ns/tick (Q8.24 335544320) and the gPTP ROM gain/limit words change 0x56→0xAC and 0x8312→0x10625, matching the published 86→172 and 33554→67109; the 8x8 gPTP image now equals the shipping 1x1 image (78c8418a…) because the station MAC, priority1 and clock are the same; the #231 report was checked against docs/findings/PP_SHADOW_BASELINE.md at ae729bbf lines 42-44, 60, 73, 97, 102 (8x8 timer 100 MHz, OOC 10 ns, 68,136 LUT / -11.331 ns, exceeds 63,400 by 4,736, no place/route) and is accurate.
[R339] PASS RTL — reviewer gateware export (no synthesis) of the 8x8 at base (100e6) and head (50e6), receipts/board-export-diff.txt — XDC byte-identical, sha256 28fae38e… (= author board-after), with sys/milan/audio/audio_tdm async clock groups retained and the milan clock derived from the PLL; only RTL deltas are PLLE2 CLKOUT1_DIVIDE 16→32 (VCO 1600 MHz → 50 MHz), MILAN_CLK_FREQ_HZ 100000000→50000000 and the PP bridge watchdogs 12'd3072→13'h1800; pp_mem_timeout_cycles(100e6, 50e6)=6144 (13 bits) clears its strict-first-in-time check (6144×50e6 < 4096×100e6) and exceeds the worst bus wait of 137; the datapath consumers (milan_datapath.sv:214,240,764,5481,5567,5647,5747,6053,6192,6886,7386) take MILAN_CLK_FREQ_HZ; the CBS, whose package constant is 100 MHz, is not instantiated (milan_csr.sv:21-27); no RTL file changed.
[R339] PASS Robustness — sw/litex/milan_soc.py:2164-2215; tb/verilator/nvm_capture_cpu/README.md:42-49; configs/endstation_ax7101_8x8.yaml — config-dependent behaviour is derived rather than mirrored (bridge watchdog, MCLK divider 3→2, latency-tap timeout 50000→25000 = MILAN_CLK_FREQ_HZ/2000, PPS width derived and disabled in this shape); the 100 MHz non-contract capture arm deliberately keeps the 50 MHz configuration ROM, and the README and receipt say so and make no gPTP claim; the bare-metal clock-enforcement gap is recorded as SUGGESTION F3 and does not affect this lens.
[R339] PASS Tests — scripts/check_nvm_capture.py (AST identical to base, receipts/ast-equal.txt), tb/verilator/nvm_capture_cpu/measurements.json, sw/builder/test_builder.py:19882-19884 — gate rc 0 at head, with all 7 named controls detected and the 4 README mutations each rc 1; fault probes: head config + base receipt → rc 1 "capture inputs changed", and base config + head receipt → rc 1, so the gate does bind configured_cpu_hz to the yaml; the builder self-test asserts CLK_FREQ_HZ_P == milan_clk_hz == MILAN_CLK_FREQ_HZ; capture reproduction: the 8x8 50 MHz ON arm (16-capture build) rows 0-2 are byte-equal to the receipt with identical netlist/firmware/BIOS/gPTP ROM/config hashes, and the 8x8 50 MHz OFF arm row 1 is equal (row 0 differs by 496 ticks under a 2-capture build whose BIOS image differs; see limits).
[R339] UNCLEAN Docs — F1 (MINOR) open; the rest of the Docs scope checked clean: SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1590 and :1737-1753 figures equal the receipt (min/max per arm, 49/max margins 2.0163/2.0197/7.4170/7.4371/2.5784/2.4760, 0.19754 ms headroom); BAREMETAL_FIRMWARE.md:55-57, the nvm_capture_cpu README :45-49/:137, recipe.py/soc.py/check_nvm_capture.py comments and README-parameters.md:29 are accurate; no stale "AX timing CLOSED"/"until #565" text remains (tree search); all docs gates rc 0.
```

## Focus items

1. **Config line and note.** `configs/endstation_ax7101_8x8.yaml:56` reads `milan_clk_hz: 50000000  # BAREMETAL_FIRMWARE.md build contract (#565)`. It makes no closure claim. BAREMETAL_FIRMWARE.md:56-57 says so explicitly: "without claiming timing closure. No cacheless 8x8 placement or routing record exists." No other 8x8 clock carries a CLOSED claim.
2. **Consumers.** I ran the builder on all five configurations at base and head in scratch copies, with `--write-fragment` so the per-config sweep fragment is captured (`scripts/compare_artifacts.py`, `receipts/artifacts-compare.json`).
   - The four other configurations are byte-identical: 11 files each.
   - Six 8x8 files change, which matches the author's list: `soc_params.json`, `lwsrp_table.json`, `lwsrp_table.svh`, `build_plan.md`, `gptp_ucode.hex` and the sweep fragment (`receipts/8x8-artifact-diffs.txt`).
   - All 110 of my per-file hashes equal the author's `artifacts-before.json` / `artifacts-after.json`.
   - Before/after values:
     - `--milan-clk-freq` 100e6→50e6
     - `KL_lwsrp_top.CLK_FREQ_HZ_P` and `milan_datapath.MILAN_CLK_FREQ_HZ` 100000000→50000000
     - `LWSRP_CLK_FREQ_C` 100000000→50000000. This is informational only; nothing in the RTL reads it.
     - `build_plan.md` milan 100e6→50e6
     - `gptp_ucode.hex` sha256 21e846a7…→78c8418a…, 13312 bytes each, 6 words differ
   - Generated constraints: see RTL.
   - Simulation suites that read the shape:
     - csr, milan_dp and nvm_backend take descriptor geometry only.
     - nvm_cosim reads `lwsrp_table.json` only for `reset_words` (`sw/litex/boot_policy.py:35-65`), so it is clock-independent.
     - sim_nxn and sim_gptp run the builder for descriptor/AEM images and use their own model clocks.
   - The firmware reads no Milan-clock constant.
   - The tracked `configs/generated/sweep_opts_ax7101.sh` is owned by the 1x1, so it is correctly unchanged.
   - Docs: see the Docs line and F1/F2.
3. **Capture gate.**
   - `check_nvm_capture.py` returns rc 0, and the edits to it, `recipe.py` and `soc.py` leave the executable AST identical.
   - `receipts/receipt-delta.json` shows:
     - all six arms are present, each with 16 rows, all ok, 0 mismatches and 0 open
     - `configured_cpu_hz` is now 50000000 on every 8x8 arm
     - the maxima are unchanged: 8x8 50 MHz 24.30246 ms (row index 13, ON arm), below 24.5; 1x1 6.60642 ms; labelled 8x8 100 MHz point 19.79024 ms, still required by the gate
     - harness, firmware and config hashes and the processor pins match the head files and gitlinks
   - All 96 rows are equal to the base rows. The only per-arm changes are the command, `configured_cpu_hz`, and the new `gptp_ucode_sha256`/`config_sha256` fields.
   - The simulation is deterministic, so equal rows are expected. My reproduction (Tests line) shows that equal inputs reproduce the rows exactly.
4. **ROM ledger.**
   - `syn/yosys/ooc.sh timestamp_counter` returns rc 0 with a scratch `OOC_TMP`. Its mandatory preflight is fatal on a digest mismatch.
   - Direct regeneration with default arguments gives ltn_rom 23cc67ee…, ucode 23605682… (pin 0922e434) and gptp_ucode c496ed8a… (pin 5dce647a). All equal `syn/yosys/rom_digests.tsv`, which is unchanged in this lane (`receipts/rom-ledger.txt`).
   - The PR statement is correct: the configuration-specific gPTP image is not a ledger input, and nothing needed re-recording.
5. **#231 report.** Accurate; see the Conformance line. The 8x8 integrated-synthesis figures describe the 100 MHz build. The re-run follow-up is the manager's, as recorded, and is not required here.
6. **Repository gates** (`receipts/gates-summary.txt`). All rc 0:
   - `docs_check.py`
   - `check_em_dash.py --base 831f94f4…`
   - `check_doc_style.py`
   - `gen_toc.py --check`
   - `gen_toc.py --verify-anchors`
   - `check_doc_paths.py`
   - `lint_rtl.py --check`
   - `git diff --check base..head`
   - `check_nvm_capture.py`, including the controls and mutations

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 8x8 yaml:55-56,157; BAREMETAL_FIRMWARE.md:33-57; issue #565 acceptance + assignment; derived gPTP ROM / PHC values; PP_SHADOW_BASELINE.md@ae729bbf | R339-2 | 054e59b41471ffbb3b4999a60c4cb04abcfc895f |
| RTL | CLEAN | Base/head 8x8 gateware export (XDC, PLL, watchdogs, datapath parameter); milan_soc.py:2164-2215; milan_datapath.sv clock plumbing | R339-2 | 054e59b41471ffbb3b4999a60c4cb04abcfc895f |
| Robustness | CLEAN | Derived clock-dependent constants; capture README comparison-arm limits; bridge watchdog refusals (F3 SUGGESTION only) | R339-2 | 054e59b41471ffbb3b4999a60c4cb04abcfc895f |
| Tests | CLEAN | check_nvm_capture.py controls, mutations and fault probes; receipt regrade; capture reproduction; test_builder.py:19882-19884 | R339-2 | 054e59b41471ffbb3b4999a60c4cb04abcfc895f |
| Docs | UNCLEAN (F1 MINOR open) | BAREMETAL_FIRMWARE.md; SAVED_STATE_SNAPSHOT_OWNERSHIP.md §18/§20.6; nvm_capture_cpu README; README-parameters.md; tree-wide clock-text search; docs gates | R339-2 | 054e59b41471ffbb3b4999a60c4cb04abcfc895f |

To clear: a head that resolves F1 needs `Docs` re-covered. If the fix changes only documentation, the other four lenses stay banked at this head, because nothing in their scope moves.

## Real limits

- **Capture reproduction is partial.** Each command has a wall-clock limit of about 10 minutes, and 16 captures need about 50 minutes, so a full 16-capture arm did not fit.
  - The 8x8 50 MHz ON run was stopped after 3 of 16 captures. Those 3 rows equal the receipt.
  - The 8x8 50 MHz OFF arm ran with `--captures 2`. That build has a different BIOS image (9f8b72f5… against the receipt's 4c4bd59b…), and its row 0 differs by 496 ticks (2,425,514 against 2,426,010). Row 1 is equal (2,426,154, the receipt's OFF maximum).
  - I did not reproduce the peak ON row (index 13, 24.30246 ms), any 1x1 arm, or the 100 MHz arms.
- **Simulator.** The scoped Verilator 5.050 path named in the assignment does not exist on this host. I used the system Verilator 5.052 (sha256 098b09b1…), which is the version the receipt records. SDK archive d42680e9… and CPU netlist c208df0b… match the receipt.
- **Not run by me:** the full builder bank, suite shards, PP/gPTP/Yosys banks, synthesis, place/route, Docker/act and any hardware. Physical timing and closure remain unmeasured, and the lane claims neither.
- **Board export.** It needed builder outputs under the checkout's ignored `sw/builder/out/`. I staged them there and removed them afterward. The ignored files my probes created have been removed. The clone is verified at the exact head tree, with a clean index and worktree, the recorded modes and the gitlinks (`receipts/restore-verification.txt`).

## Pending manager duties

- Hosted evidence at the exact head is not reviewer acceptance: 21 check runs succeeded and "Physical gPTP" was skipped (`receipts/hosted-check-runs.tsv`). Hosted and act acceptance, and the source bank, remain with the manager.
- Build and validate the final candidate merge result against live dev `8c8e7bb0…`.
- Carry the recorded #231 8x8 re-run follow-up.
- Route F1 to the executor. Consider new Issues for F3 and the AAF_LATENCY_TAPS.md:15 observation.

R339-2 FINISHED
