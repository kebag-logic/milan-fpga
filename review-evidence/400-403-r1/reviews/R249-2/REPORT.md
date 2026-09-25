[R249] NEGATIVE - exact head 7463ab0889da9a95fce7c921e386d6035d69778e

# R249-2: internal independent review of PR #566 (issues #400 and #403)

- Round: R249-2 (cleared context, own clone). R249-1 and R250-1 were voided before any verdict, so no earlier public review finding exists on this PR to resolve or retain.
- Exact head: `7463ab0889da9a95fce7c921e386d6035d69778e`, tree `7741fe585b8de933e461cad62cf763976c30833a`. Reviewed range: `864b36f5..7463ab08`, which contains preserved author commit `17e2cf69`, merge `6cb11238`, and `4cfbb825`, `e7da6545`, `2d61e7ed`, `7463ab08`.
- Authority, in the order read: AGENTS.md, CONTRIBUTING.md (sections 1 to 3 and 6), docs/README.md, the #400 and #403 bodies and all comments on both, REQUIREMENTS.md (REQ-MAC-02, REQ-CLS-03, REQ-VER-01..04), the PR body, the diff and history, then the public evidence tree `5e060feb:review-evidence/400-403-r1`.
- Frozen acceptance applied: #400 5770922734 and 5781042070, #403 5770922898, and the 2026-09-23 owner decision (restored PTOF moves to #70). Acceptance also requires that the existing gates stay green: #403 original AC4 (Verilator and Yosys gates green) and "existing gates ... remain mandatory" in 5770922898.
- Verdict basis: one BLOCKER and three MINOR findings are open. Conformance, RTL, Tests and Docs are UNCLEAN. Robustness is CLEAN.

## Findings

### F1 - BLOCKER - Tests, Conformance
**Where:** `tb/verilator/nvm_cosim/run_cases.py:131` calls `sw/firmware/nvm_hosttest/test_nvm_firmware.py:166`. The saved-state co-simulation suite is broken at this head.

- **Evidence:** Round 2 changed the third parameter of `constants_header()` from `ident: Ident` to `boot_constants: dict[str, int]` and spread it with `**boot_constants`. Its only other consumer was not updated: `run_cases.py:131` still passes `ident`. At this head, `make -C tb/verilator/nvm_cosim quick` exits 2 with `TypeError: 'Ident' object is not a mapping`, before it builds or measures anything (receipt 25).
- **Base comparison:** the same command at base `864b36f5` passes with 315 of 315 checks (receipt 26).
- **Before round 2:** at `2d61e7ed` the suite already failed, one step later. Its host-compiled firmware had no `MILAN_MAC_CTRL_SET`, `MILAN_TCAM_CTRL_BOOT`, `MILAN_AAF_CTRL_BOOT` or `MILAN_MAAP_CTRL_BOOT` (receipts 27, 27b). So the bundle's firmware change (`17e2cf69`) introduced the defect, and round 2 fixed one consumer of the fixture but not the other.
- **Hosted confirmation:** at this exact head, `Verilator shard 1/5` reports `FAIL nvm_cosim`, "NOCOUNT nvm_cosim: printed no tally line at all", and the aggregate `verilator-suites` context is `failure` (receipts 80, 81).
- **Impact:**
  - The only suite that runs the shipping writer against `KL_nvm_backend` and the pinned donor producers no longer runs.
  - A required exact-head gate is red.
  - "Existing regressions remain green" (AGENTS section 6, Tests) and the retained acceptance that Verilator gates stay green are both unmet.
- **Required outcome:** every consumer of the host-test constants header uses the same derivation (`boot_policy.fabric_constants`), so that `nvm_cosim` builds and tallies again. Nothing is to be skipped or weakened.
- **Verification:**
  - `make -C tb/verilator/nvm_cosim quick` passes at the new head, and so do `run` (both shapes plus the mutants) and the hosted `verilator-suites` context.
  - A repository-wide search for callers of any signature changed in the fix finds no stale caller.

### F2 - MINOR - Tests, Docs
**Where:**
- `tb/verilator/pp_shadow/sim_main.cpp:625-636` and `:1564-1570`
- `tb/verilator/csr/sim_main.cpp:103-116` and `:750`
- `tb/verilator/pp_shadow/Makefile` and `tb/verilator/csr/Makefile` (both unchanged)

The in-tree runs cannot fail for the binding and reset defects they name. The runs that can fail exist only outside the repository.

- **Evidence, binding:** Every hop defaults to VID 2 (`KL_pp_shadow`, `protocol_processor_top`, `KL_srp_top`), and the harness's `DECLARATION_VID` default is also 2. So the check labelled "#400 generated parent/wrapper/top/child startup VID", as run by `make`, cannot fail for a broken hop:
  - With the `KL_pp_shadow` hop removed, `make` still passes, 402 of 402 checks (receipt 41).
  - With the `milan_datapath` hop removed, `make` still passes (receipt 43).
  - With a distinct generated VID (reviewer VID73 fixture), the head passes (receipt 40), and both mutants fail three checks (receipts 42, 44).
- **Evidence, reset bits:** In-tree CSR legs only run with generated reset bits 0. Masking `LWSRP_CTRL[1:0]` out of the real reset passes `make` (receipt 35) and fails with a reset-bits-3 fixture (receipt 36).
- **Out-of-tree only:** The `DECLARATION_OUTPUTS=2` CRF-on leg (receipt 45 is the reviewer's run) is likewise not in any recipe. The fixtures that make these checks non-vacuous exist only as scripts in the published author evidence (`author-r2/run-pp-fixtures.py`, `author-r2/csr-matrix.py`, which use private paths).
- **Misleading comments:** Two harness comments describe builds that the repository does not contain: "The second build supplies a distinct generated VID" and "the declaration matrix supplies each YAML shape explicitly".
- **Mitigation, noted:** the source-text gate 40 (`sw/builder/test_declarations.py`) does detect the removed bindings and reset symbols (receipt 10).
- **Impact:** after merge, the executable proof required by #400 5770922734 has no durable regression. That proof covers each generated-VID binding hop and the live reset bits as distinct from the firmware boot policy. A future broken hop stays green in every Verilator suite. The harness comments tell a cold reader that coverage exists when it does not.
- **Required outcome:** Either of these:
  - The distinct-VID, CRF-on and nonzero-reset-bit legs become repository recipes that the suite's default target (and therefore the hosted Verilator shards) runs, with their headers generated rather than hand-edited.
  - Or the comments and check labels state plainly that `make` covers only the VID-2, one-output, reset-bits-0 case, and name where the other cases are gated.
- **Verification:** mutants 41, 43 and 35, rerun against the suites' default targets, turn red.

### F3 - MINOR - Docs, RTL
**Where:**
- `hdl/common/csr/milan_csr.sv:1542-1543` and `:1549`
- `hdl/milan/milan_datapath.sv:302` (a `//!` parameter contract)

The contract text inside the RTL contradicts the changed behaviour.

- **Evidence:**
  - The comment directly above `aaf_ctrl <= AAF_CTRL_RST_C;` still reads "enable=0, bypass=1 ..., VID=2". The reset is now 0, which means bypass 0 and VID 0.
  - Line 1549 says the lwSRP "VID/DMAC mirror the AAF defaults". The lwSRP VID resets to 2 and AAF to 0.
  - `RXFILT_P`'s `//!` documentation says "the builder gate keys on platform.rx_address_filter being declared 'promiscuous'". This PR removed that gate: `sw/builder/endstation_builder.py:3225` says "Hardware presence is independent", and `validate_features` no longer reads the key.
  - House style makes the inline `//!` port and parameter documentation the spec (CONTRIBUTING section 1). CONTRIBUTING section 5 asks that touched code be left at least as clear as it was.
- **Impact:** a reader of the RTL gets the old reset contract and a gate that no longer exists.
- **Required outcome:** these comments state the neutral resets and the independent prune rule, or are removed.
- **Verification:** read the three sites at the new head. A search for `bypass=1` and `rx_address_filter` in `hdl/` finds no contradicting text.

### F4 - MINOR - Docs
**Where:**
- `docs/design/MAAP_FABRIC.md:83-84` and `:151`
- `tb/verilator/milan_dp/README.md:683` and `tb/verilator/milan_dp/sim_main.cpp:1330`
- `docs/ENDSTATION_BUILDER.md:1018`

Documents still mirror the old contracts.

- **Evidence:**
  - `MAAP_FABRIC.md` is an "AS-BUILT" spec that says its CSR block "mirrors" `REGISTER_MAP.md`. It still gives `MAAP_CTRL` "reset `0x0800` ... block count (default 8)" and "count = 8 like the reference". REGISTER_MAP (updated by this PR) now says neutral reset 0, with the firmware claiming exactly the declared outputs.
  - The milan_dp README and a harness comment explain the format fold "exactly as `aecp_pres_offset` folds set offsets over `PRES_DFLT_C`". This PR deletes `PRES_DFLT_C` in favour of `ADP_STROUT_PRES_NS_C`.
  - ENDSTATION_BUILDER section 3 goes from "66 rows" to "69 rows" after this PR adds four rows (22a, 22b, 43a, 43b). There are 71 numbered rows at head, against 67 at base.
- **Impact:** the as-built MAAP spec and the test documentation contradict the authoritative register map and the RTL, and the row count is wrong.
- **Required outcome:** the three places describe the neutral reset, the exact allocation and the generated per-output default row, and the count matches the table.
- **Verification:** read the sites at the new head. `git grep PRES_DFLT_C` returns nothing outside history. The row count equals the number of rows under the convention the base used.

### S1 - SUGGESTION - Conformance
**Where:** `sw/litex/boot_policy.py:58-59`

`MILAN_MAC_CTRL_SET = 1 << 3` and `MILAN_TCAM_CTRL_BOOT = 1` are literals. Nothing ties them to `platform.rx_address_filter`, which is not carried in the overlay. With one legal value this is correct today. Deriving them from the declared posture, or asserting it, would stop a future second value from silently keeping the bypass. This does not affect coverage.

## Per-lens results (the same three fields as a finding)

- **[R249] UNCLEAN Conformance** - F1 (#403 AC4 and the retained existing-gate criterion). The following were checked and found correct:
  - Declarations: every `srp:` leaf is classified (ENDSTATION rows 35 to 44, 43a, 43b), and unsupported values are refused by name (26 refusals, receipt 10).
  - VID: the single source `srp.vid` reaches `LWSRP_VID_RST_C`, `MILAN_SR_VID`, `MILAN_AAF_CTRL_BOOT` and `ADP_SRP_DOM_DEF_VID_C`, and on through `milan_datapath` -> `KL_pp_shadow` -> `protocol_processor_top` -> `KL_srp_top.DOM_DEF_VID_P` at 16 bits (VID73 end to end: receipt 40).
  - Domain adoption and link-cycle restore stay live (receipt 21).
  - Timers are asserted against the donor constants and the PRNG bounds (receipt 10).
  - Presentation offset: the 2 ms factory row for every output including CRF, and a runtime 1 ms that moves only its own GET and wire timestamp, on the 4x4 (1844 checks) and 8x8 (3524 checks) legs (receipts 22, 23).
  - RX posture: promiscuous is declared and defaulted, and `hardware` is refused with migration text. Station unicast, foreign unicast, broadcast and unregistered multicast all reach the post-filter fabric at reset and at boot (receipt 21).
  - Listener acceptance is unchanged: `pres_ofs_i` still takes row 0, which is 2 ms.
  - Reset and allocation: AAF and MAAP reset to 0 in both the real flop and the readback. The firmware transcript on all five shapes, plus CRF off, is correct: the shipping 1x1 claims 2 (unchanged), arty_current claims 1, and CRF on minus off equals 256 (receipt 11). The MAAP highest-valid and first-invalid boundaries hold at 1 and 2 outputs (receipts 21, 45).
  - No new receive-filter policy is implemented.
- **[R249] UNCLEAN RTL** - F3.
  - Behaviour is clean. `hdl/common/csr/milan_csr.sv`, `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv` at head are behaviour-neutral except where the decisions require change: the neutral resets, the generated VID parameter, and the header-driven factory row.
  - `ADP_STROUT_PRES_NS_C` length equals `ADP_TALKER_SRC_C` in all six tracked headers, and the generated headers equal the builder's emission (receipt 14).
  - Area delta is 0 on all six counters for milan_csr (4236), KL_pp_shadow (66991) and milan_datapath (96819 LUT_TOT), using the repository `syn/yosys/ooc.sh` at base and head (receipts 60, 61).
  - Lint ratchet and SV idiom gates pass (receipts 70, 74). The `TCAM_CTRL` write is a plain RW store equal to its reset value.
- **[R249] CLEAN Robustness** - `sw/builder/endstation_builder.py:1363-1372,1921-1972,3262-3266`; receipts 10, 15, 21, 34, 45.
  - Boolean, float, string and `None` values for the VID, timers, TSpec, budget and offsets are all refused. So are listener offsets, a CRF offset with the output disabled, and a case-variant filter value.
  - The MAAP boundaries at 1 and 2 outputs, the CRF on/off difference, a MAAP prune with talkers (refused), and a filter prune under promiscuous (accepted) all behave as the decisions require.
  - Reset readback and outputs are neutral on the 1x1, 4x4 and 8x8 CSR legs.
  - No open finding.
- **[R249] UNCLEAN Tests** - F1, F2.
  - The new checks otherwise detect their defects. The CSR reset and readback mutants are detected (receipts 30 to 33). The fold mutants (runtime ignored, all rows follow row 0, valid bit taken from row 0) are detected (receipts 50 to 52). A restrictive boot-filter mutant is detected (receipt 46). Gate 35 refuses 8 of 8 planted defects, and gate 40 its 9 binding mutants and 15 header mutants (receipts 10, 11).
  - The firmware self-test passes on 5 shapes (receipt 12).
- **[R249] UNCLEAN Docs** - F2, F3, F4.
  - REGISTER_MAP rows 0x654, 0x680, 0x684, 0x6CC, 0x75C and 0x788, ENDSTATION rows 22a, 22b, 30 and 35 to 44, and README-parameters match the RTL consumers (for example, `LWSRP_CTRL[5]` is unconnected at `milan_datapath.sv:2499`, so the row's "scratch" is true).
  - docs_check passes, and there is no em dash on any added line (receipts 73, 72b).

## Merge `6cb11238` (focus item 4)

- The remerge-diff is confined to the conflict files: `PNG_MANIFEST.json`, `submodule_boundaries.{drawio,png,svg}`, `REGISTER_MAP.md`, `SUBMODULES.md` and `protocol-processor` (receipt 01).
- The processor gitlink is dev's `990f9652`, and gPTP is dev's `e5dcea6e`. `git diff 864b36f5..7463ab08` touches no gitlink and no diagram file.
- The 0x680 and 0x684 rows took the bundle side. The bundle's `[5]` "legacy scratch" is accurate, because `o_lwsrp_decl_bypass` is unconnected.
- The 8452f564 adoption text was dropped as the assignment required, and the donor disclosure lines were kept.
- Also verified:
  - `check_cpp_idiom.py` passes at dev's pin (receipt 77), so the original author blocker is resolved by that pin.
  - Gates 18a to 18d and 20a pass (receipt 16).

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #400/#403 decisions vs builder, headers, RTL, firmware; receipts 10-16, 21-23, 40, 45 | R249-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| RTL | UNCLEAN (F3) | milan_csr.sv, KL_pp_shadow.sv, milan_datapath.sv diffs; donor top/child params; OOC base/head; lint | R249-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Robustness | CLEAN | builder validators; receipts 10, 15, 21, 34, 45 | R249-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Tests | UNCLEAN (F1, F2) | test_declarations.py, test_builder gates 35/40/23c/32/18/20a, csr, pp_shadow, sim_nxn, nvm_hosttest, nvm_cosim; 14 mutant runs | R249-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |
| Docs | UNCLEAN (F2, F3, F4) | ENDSTATION_BUILDER.md, REGISTER_MAP.md, SUBMODULES.md, README-parameters.md, MAAP_FABRIC.md, RTL/TB comments | R249-2 | 7463ab0889da9a95fce7c921e386d6035d69778e |

## Limits

- **Not run:**
  - The RV32 census (`test_baremetal_profile_contract`) did not run: no cross compiler was available.
  - `check_em_dash.py` could not run because its pinned renderer was absent. An equivalent byte probe with a positive control ran instead (receipt 72b).
  - No full builder, parent, PP, gPTP or Yosys bank, no act, no candidate merge, no hardware. Physical calibration was NOT RUN. Hosted skipped contexts (for example physical gPTP) are not evidence.
- **Partial coverage:**
  - Datapath legs run: nxn 4x4, nxn8 and ax1x1. Not rerun: nxndv, nxn4c, nolpf, prune, aclk, notify, crflic, and the render and gmstep mutant campaigns.
  - `nvm_cosim` ran only `quick` (1x1). Its `run` (8x8 plus mutants) did not run.
- **Tools and fixtures:**
  - Area was measured with the host's Yosys, the same binary at base and head.
  - The VID73, CRF-on and reset-bits-3 fixtures were built by the reviewer and are test-only. Their generators are in `scripts/`.
- **Clone state:**
  - The review clone was not modified. Tracked bytes, modes, index and gitlinks were re-verified (receipt 90).
  - Reading the public evidence tree fetched its commit into the clone's object store; no tracked content changed.

## Pending manager duties

- Hosted `verilator-suites` is red at this head (F1).
- Exact-head act and hosted acceptance, the final current-dev candidate (source base `864b36f5`, live dev `fd9e0ebf`), merge authorization and containment remain with the manager.
- R250 remains the external reviewer.

R249-2 FINISHED
