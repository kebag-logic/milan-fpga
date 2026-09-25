[R250] NEGATIVE - exact head 7463ab0889da9a95fce7c921e386d6035d69778e

# R250-2 external independent review: issues #400 and #403, PR #566, round 1

- Head: `7463ab0889da9a95fce7c921e386d6035d69778e`, tree `7741fe585b8de933e461cad62cf763976c30833a`.
- Diff reviewed whole: `864b36f5e9450ef64f75ca3f0d68c44330e447d7..7463ab08` (26 files), including the merge `6cb11238` by remerge-diff.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Result: Conformance, RTL and Robustness are clean. Tests is unclean with one BLOCKER and one MINOR. Docs is unclean with one MINOR.
- The BLOCKER is a regression in a required suite. The hosted `verilator-suites` context is also red at this head.

## Reconstruction

The review was rebuilt from public state only, in this order: AGENTS.md, CONTRIBUTING.md, docs/README.md, and REQUIREMENTS.md (REQ-MAC-02, REQ-CLS-03). Then the #400 and #403 issue bodies and every comment on them. The decisions used were 5770922734 (#400) and 5770922898 (#403), both pre-implementation. Also used: scope note 5729726367, assignment 5781042070, the 2026-09-23 owner decision 5789766951 (restored PTOF moves to #70), resume assignment 5831927176, and the round-2 order 5832912970. Next came the PR body and comments, the diff and its history, and the published evidence tree at `5e060feb.../review-evidence/400-403-r1`. No prior public review findings exist on the PR. Rounds R249-1 and R250-1 were voided before any verdict, so nothing had to be resolved or kept from them.

## Findings

### F1 - BLOCKER - Tests - `tb/verilator/nvm_cosim/run_cases.py:131` against `sw/firmware/nvm_hosttest/test_nvm_firmware.py:166`: the saved-state co-simulation suite crashes before running any case

- **Authority and evidence:** Round 2 (`7463ab08`) changed the third parameter of `constants_header()` from an `Ident` to a boot-constant mapping (`**boot_constants`). The only other caller was not updated. `run_cases.py:131` still passes `ident`.
  - At the exact head, `make -C tb/verilator/nvm_cosim quick` fails with `TypeError: 'Ident' object is not a mapping` and exit 2 (`receipts/nvm_cosim-quick-head.log`).
  - At base `864b36f5` the same command passes, `315 checks: 315 PASS` (`receipts/nvm_cosim-quick-base.log`).
  - Hosted run 36142747033, job `Verilator shard 1/5`, fails with `FAIL nvm_cosim`. Its suite-log artifact shows the same traceback, and the required aggregate `verilator-suites` concludes `failure` (`receipts/hosted-checks-7463ab08.txt`, `receipts/hosted-nvm_cosim-7463ab08.txt`).
  - AGENTS.md section 6, `Tests`: "Existing regressions remain green."
  - Section 7 requires exact-head `verilator-suites` evidence.
- **Impact:**
  - The only harness that grades the shipping saved-state writer and backend against the section 9 orderings measures nothing at this head.
  - A required merge-bar context is red.
  - The firmware itself is not implicated. A disposable probe gave the call `fabric_constants(overlay, lwsrp)` and passed 315/315 at 1x1 (`receipts/nvm_cosim-quick-head-adapted-probe.log`; reverted, never committed).
- **Required outcome:** every caller of the changed helper gets its boot constants from the same generated derivation, and `nvm_cosim` passes at the new head.
- **Verification:**
  - `make -C tb/verilator/nvm_cosim run` exits 0, covering both shapes and every named mutant killed.
  - Hosted `Verilator shard 1/5` and `verilator-suites` succeed on the new exact head.

### F2 - MINOR - Tests - `tb/verilator/pp_shadow/sim_main.cpp:624-654,1564-1569`, `tb/verilator/csr/sim_main.cpp:105-116`, `tb/verilator/pp_shadow/Makefile:134`: the new discriminating fixture legs have no committed recipe

- **Authority and evidence:** The check `#400 generated parent/wrapper/top/child startup VID` compares against `DECLARATION_VID`, which defaults to 2. That is also the default of every donor parameter. No committed recipe defines `DECLARATION_VID`, `DECLARATION_OUTPUTS`, `CSR_DECL_TALK/LIST` or `CSR_SRP_RESET_BITS` (repository-wide search). The VID-73, CRF-on and 20-case CSR matrix runs exist only as ad hoc commands in the evidence tree (`author/fixture-vid73.svh`, `author-r2/csr-matrix.py`). Measured here:
  - **R1:** removing `.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)` from `milan_datapath.sv:7411` survives the committed `make` (402 checks, 0 failures).
  - **R7a/R7b:** replacing the child hop `KL_srp_top.sv:341` `.DEF_VID_P (DOM_DEF_VID_P)` with `16'd2` survives both gate 40 and the committed `make`.
  - **R2:** the same fixture built with a generated VID of 73 passes at head.
  - **R3/R7c:** under that fixture, both mutants are detected (3 failures each).
  - AGENTS.md section 6, `Tests`: "Each new test can fail for the defect it claims to detect". The #400 decision requires proof of "each generated-VID binding hop".
- **Impact:** The hop proof is one-off evidence at this head, not a regression. A later processor pin that drops the child binding stays green in every committed gate. The same applies to the CRF-on output-count leg and to the non-default reset-bit CSR legs.
- **Required outcome:** at least the distinct-VID leg, and preferably the CRF-on and shape/reset legs, run from a committed recipe that the suite runner executes. Otherwise the default check's label must stop claiming the hop.
- **Verification:** R1 and R7b are detected by the committed recipe.

### F3 - MINOR - Docs - current-tree text contradicts contracts this PR changed

- **Authority and evidence:** AGENTS.md section 6, `Docs`: "Changed contracts are reflected in authoritative docs." CONTRIBUTING section 5: leave touched code at least as clear as it was. Each item below became false with this diff:
  1. `hdl/common/csr/milan_csr.sv:1542-1543`: the comment directly above `aaf_ctrl <= AAF_CTRL_RST_C` still says "enable=0, bypass=1 ... VID=2". The reset is now 0. `:1549`, "VID/DMAC mirror the AAF defaults", no longer holds, because LWSRP_VID resets to 2 and AAF_CTRL VID resets to 0.
  2. `docs/design/MAAP_FABRIC.md:83-84` says `MAAP_CTRL` resets to `0x0800` with block count "default 8", and claims to mirror REGISTER_MAP. `:151` still records "count = 8 like the reference" as the settled decision. The #403 decision now sets reset 0 and a count of exactly the declared outputs.
  3. `docs/design/AREA_BUDGET.md:41` and `sw/litex/milan_soc.py:3464-3469` (`--no-maap` help) say MAAP may be absent "when stream destination addresses are statically provisioned". `hdl/milan/milan_datapath.sv:274-275` says the builder gate keys on `stream_dmac_base: maap`. The builder now refuses MAAP removal for every config (`endstation_builder.py:3210`), and numeric bases are legacy scratch.
  4. `hdl/milan/milan_datapath.sv:301-302` says the RX filter prune "builder gate keys on platform.rx_address_filter being declared 'promiscuous'". This PR deletes that gate (`validate_features`, former rule 4).
  5. `tb/verilator/milan_dp/README.md:683` and `tb/verilator/milan_dp/sim_main.cpp:1330` name `PRES_DFLT_C`, which this PR removes in favor of `ADP_STROUT_PRES_NS_C`.
- **Impact:** A cold reader following the as-built MAAP page, the area-lever table or the RTL banners will believe a 0x0800 reset, a static-address MAAP prune and a filter-declaration gate, none of which exist. That is the kind of declaration drift #400 and #403 exist to remove.
- **Required outcome:** each statement above matches the shipped contract, or is removed.
- **Verification:** reread the cited lines at the new head. `docs_check`, `check_em_dash` and `gen_toc --check` pass.

### S1 - SUGGESTION - Tests, Conformance - `sw/builder/test_declarations.py:162-166`: timer profile read from defaults only

Gate 40 asserts the `KL_srp_top` parameter defaults and the PRNG bounds. It does not check the `u_srp` instance in `protocol_processor_top`. Adding `.LEAVE_MS_P (600)` there survives gate 40 (`receipts/mutant-S1.log`). No override exists at this pin, so this is optional hardening for later pin moves.

## Clean-lens evidence

- **Conformance, CLEAN:**
  - `sw/builder/endstation_builder.py:1363-1372,1459-1463,1934-1972,2912-2922,3210-3215,3262-3268,3836-3837,4905-4913`, `sw/litex/boot_policy.py:50-65` and `sw/firmware/milan_baremetal/milan_baremetal.c:1375-1385` were checked against decisions 5770922734 and 5770922898 and the 2026-09-23 owner decision. Every declaration is derived, not mirrored:
    - `srp.vid` feeds `LWSRP_VID_RST_C`, `MILAN_SR_VID`, `MILAN_AAF_CTRL_BOOT` and `ADP_SRP_DOM_DEF_VID_C`. That constant is bound at `milan_datapath.sv:7411`, then `KL_pp_shadow.sv:1056`, then the processor top `:2226` (pin `990f9652`), then `KL_srp_top :341`.
    - Timer, TSpec, bandwidth, VID and offset refusals carry their reasons.
    - Presentation-offset rows exist per declared output, CRF included, in STREAM_OUTPUT order, and `ADP_TALKER_SRC_C` equals the row count for all five configs.
    - The promiscuous posture is `TCAM_CTRL=1` plus allmulti, the same as the unchanged reset.
    - The MAAP claim is exact: gate 35 transcript for shipping `ax7101_1x1_tdm8` shows `6cc=0x201 654=0x20001 700=1 100|=8 680=0x13 750=3`, and CRF-off shows `6cc=0x101`.
    - `entity_model_id` is unchanged for all five configs, base against head (`receipts/model-ids-*.txt`).
    - Out-of-scope items are untouched. No RX filter RTL changed. The listener `pres_ofs_i` still reads row 0, as it did before, and it gates diagnostics, not payload acceptance. Restored PTOF is correctly deferred to #70.
  - REQ-MAC-02's "filters station unicast" sits in tension with a shipping promiscuous posture. That tension predates this PR and is recorded in the #403 decision, which leaves restrictive policy out of scope, so it is not a finding here.
- **RTL, CLEAN:**
  - `hdl/common/csr/milan_csr.sv:1207-1208,1544,1552,1975,1986`, `hdl/milan/KL_pp_shadow.sv:189,1056`, `hdl/milan/milan_datapath.sv:1424-1427,2036,3261-3268,5747-5748,7411`:
    - Array indexing `k < ACMP_SRC_C == ADP_TALKER_SRC_C` stays in bounds.
    - Rows `k >= ACMP_SRC_C` keep 2 ms.
    - The new wires are observation-only.
    - The AAF and MAAP reset change is effect-neutral before boot: enable is 0 in both old and new, the CRF tag uses `LWSRP_VID`, `KL_maap` idles when disabled, and `cfg_maap_internal_i` is tied 0.
  - Area was measured with the repository OOC recipe, base against head, for `milan_csr`, `KL_pp_shadow` and `milan_datapath`. It reproduces delta 0 in every column: 4236/66991/96819 LUT_TOT, 3573/30187/43424 FF (`receipts/ooc-base.log`, `receipts/ooc-head.log`).
  - NxN mutants N1 (CRF transit reads row 0) and N2 (fold data from row 0) are detected, with 4 and 13 failures. The head leg passes 1844 checks.
- **Robustness, CLEAN:**
  - `sw/builder/test_declarations.py` refusal cases cover bool, float and out-of-range values. They cover listener offsets, CRF offsets with the output disabled, `hardware` filter, MAAP prune, and bandwidth at 0, 76 and 100.
  - Reset and boot posture was graded on the post-filter fabric: station unicast, foreign unicast, broadcast and unregistered multicast (`pp_shadow` #403 lines). TCAM-reset mutant R4 was detected.
  - MAAP boundaries were graded: the highest valid source gets `base + index`, and the first invalid source gets status 2 with no allocator request.
  - No in-tree software read-modify-writes `AAF_CTRL` or `MAAP_CTRL`.
  - CRF off and on differ by exactly one claimed address (gate 35).
  - Link-cycle restore and network adoption stay live.
- **Tests:** UNCLEAN (F1, F2).
  - Tests that passed or were detected here:
    - declarations gate: 26 refusals, header and binding mutants;
    - gate 35: 8/8 plants;
    - firmware host self-test: 5 shapes, 4 plants;
    - the round-2 control reproduces the four undeclared constants at `2d61e7ed`;
    - 16/16 builder and boot-policy mutants detected for the rule each breaks;
    - csr: 391/110/44/391 checks;
    - pp_shadow: 402 checks;
    - R4-R6 and R8 detected.
- **Docs:** UNCLEAN (F3).
  - Otherwise correct: ENDSTATION_BUILDER rows 22a/22b/28/30/35-44, REGISTER_MAP `0x654/0x680/0x684/0x6CC/0x75C/0x788`, README-parameters, and the SUBMODULES disclosures. The submodule diagram passes `--check` with 4 exact gitlinks. `docs_check` passes, and no added line carries U+2014.

## Merge and history checks

- The remerge-diff of `6cb11238` touches only `PNG_MANIFEST.json`, `submodule_boundaries.{drawio,png,svg}`, `REGISTER_MAP.md`, `SUBMODULES.md` and the `protocol-processor` gitlink.
- The gitlink equals dev's `990f9652`. The bundle's `8452f564` bump and its pin text were dropped.
- The SUBMODULES and REGISTER_MAP resolutions keep dev's rows and pins. Only the author's `0x680`/`0x684` rows replace dev's text, and they are accurate: `LWSRP_CTRL[5]` is unconnected at `milan_datapath.sv:2499`.
- `gptp-processor` and `verilog-axis` gitlinks equal base.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | builder/boot_policy/firmware lines above; generated headers x6; decisions 5770922734, 5770922898, 5789766951; gate 35 transcripts; model ids | R250-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| RTL | CLEAN | milan_csr.sv, KL_pp_shadow.sv, milan_datapath.sv lines above; processor pin 990f9652 top/srp; OOC base/head; NxN N0-N2 | R250-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Robustness | CLEAN | test_declarations refusals; pp_shadow reset/boot RX and MAAP boundary legs; R4; gate 35 CRF delta; software RMW census | R250-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Tests | UNCLEAN (F1 BLOCKER, F2 MINOR) | nvm_cosim head/base/probe; hosted shard 1/5; pp_shadow/csr recipes; mutants R1-R8, N1-N2, MB1-MB11, MP x5, S1 | R250-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Docs | UNCLEAN (F3 MINOR) | ENDSTATION_BUILDER, REGISTER_MAP, README-parameters, SUBMODULES, MAAP_FABRIC, AREA_BUDGET, milan_soc help, RTL banners, milan_dp README | R250-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |

## Limits

- Not run here, per the brief:
  - the complete builder, parent, PP, gPTP and Yosys banks, and `act`;
  - the `nvm_cosim run` target (both shapes plus mutants); only `quick` (1x1) ran;
  - NxN legs other than `obj_nxn` 4x4 (divergent, 8x8, 4c, ax1x1, aclk);
  - behave;
  - `check_em_dash` and `gen_toc --check`, whose pinned renderer is not installed and was not installed, since shared installs are not allowed. An added-line U+2014 scan was done instead.
- Area comes from a local Yosys 0.66. Both arms used the same tool, and the absolute figures match the published evidence.
- Physical calibration was not run. Field skips are not hardware proof.
- Deviations:
  - The first csr and pp_shadow runs used the recipes' hard-coded `--build -j 0` (all cores) for about 20 seconds before the job cap was applied. Every later build was capped at 8 jobs or fewer.
  - One file copy was briefly written outside the packet and deleted at once.
  - The first R2/R3 attempt failed on a runner quoting error and was rerun. It is kept under `receipts/invocation-error/`.
- Review clone integrity: the before and after records are identical (blob bytes, modes, index, clean worktree, gitlinks `990f9652`, `e5dcea6e`, `48ff7a7e`).

## Pending manager duties

- Hosted `verilator-suites` is red at this head (F1). `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability` and `yosys-portability` succeeded. `Physical gPTP` was skipped (nightly), which is not a result.
- Still owed: the final current-dev candidate (live dev `fd9e0ebf`), trusted `act`, merge authorization and containment.
- A re-review is needed at the corrected head, covering Tests and Docs, plus any lens whose scope the fixes touch.

R250-2 FINISHED
