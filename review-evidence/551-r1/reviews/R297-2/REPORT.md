[R297] NEGATIVE - exact head f219a5edaa191b33acc8b77abd22469f8f0db1f9

# R297-2 external independent review: issue #551 / PR #553

- Role: [R297], cleared-context external independent reviewer, round R297-2.
- Exact head: `f219a5edaa191b33acc8b77abd22469f8f0db1f9`, tree `aca067d42122d785d8319d4d0926484dd9351568`.
- History: merge `8dc98a429bd9918ad643fdb0051c2c9660395722` (parents `babb8925`, dev `864b36f5`), then content commit `f219a5ed`.
- Source base and live dev: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
- Gitlinks: `protocol-processor` `990f96526bb89356c963a260ebbdcf2a77e6623a` (contains the #112 fix, `a8f8ce81`), `gptp-processor` `e5dcea6e`, `third_party/verilog-axis` `48ff7a7e`. `external` is uninitialised, as at start.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md sections 1, 3 and 6, and docs/README.md;
  - the issue #551 body;
  - manager decisions 5813147847 and 5816014072;
  - assignments 5814963437, 5831903033 and 5832468673;
  - the TAKEN and REVIEW READY comments, and the PR body;
  - FR_NFR.md FR-SRP-03, and the processor interface (`protocol_processor_top.sv`, `KL_srp_top.sv`, `KL_srp_admission.sv`, `docs/guides/integrator.md`);
  - the diff `864b36f5..f219a5ed` with `git show --remerge-diff 8dc98a42`, and the exact-head hosted check runs.
- Verdict and ledger were written before I read any prior review. Prior findings are resolved in their own section below.

## Verdict summary

The implementation is right. `lwsrp_stream_gate` is ACTIVE AND the per-source real grant, and every licence consumer reads it. The processor pin now keeps the grant low until the current TSpec has been evaluated. At this head, a refused re-declaration opens no CRF or AAF licence, whatever the source's TSpec history. I confirmed this in simulation, including a pre-fix processor control that fails.

The merge is clean, and the mutants and the BDD pin behave as claimed. One open MINOR keeps Docs and Conformance unclean: the specification-facing licence scenario still tells the reader that the pre-#112 residual window is open and that its fix is pending. That contradicts round-3 acceptance item 3 and every other contract document.

## Findings

### F1 - MINOR - Docs, Conformance - `tests/features/milan_streaming_licence.feature:92-94` - the licence scenario still describes the pre-#112 residual window as open

- **Requirement/evidence:** the round-3 assignment (issue comment 5831903033, item 3) says: "the 'cannot open' claims are now true. Remove the residual-window text that described the pre-#112 round." At this head the scenario that pins the #551 composition still reads:

  > "Residual: a refused re-declaration with a different previous TSpec can still see about one round of licence: the first-round grant uses the previous slope. Processor issue #112 owns that pending fix."

  The file was last changed by `babb8925`. Neither the merge nor `f219a5ed` touches it (`receipts/feature_residual_evidence.txt`). My runs show the opposite of what the comment says:
  - the changed-TSpec refusal arm `[I]` passes for both sources and both phases (`receipts/head_clean.run.log`, 415 checks, 0 failures);
  - the same arm fails 28 checks only against the pre-#112 processor (`receipts/prefix_control.run.log`).
- **Impact:** the one specification-facing artifact for this contract tells a cold reader that the #551 defect is still open and that #112 is pending. That contradicts CHANGELOG, FR_NFR, REGISTER_MAP, EGRESS_QUEUE_MAP, ieee8021q, the compliance matrix and the shipped evidence. Round-3 acceptance item 3 is not met for this artifact.
- **Required outcome:** the scenario comment describes the current contract: ACTIVE AND the current-TSpec real grant, with changed-TSpec refusal graded by `obj_crflic` `[I]`. It no longer claims a residual window or a pending processor fix.
- **Verification:**
  - `git grep -n -i 'residual\|pending fix\|first-round grant' tests/features/milan_streaming_licence.feature` returns nothing.
  - `behave features/milan_streaming_licence.feature` still passes 5/5.
  - The three wrong-composition arms (`scripts/bdd_arms.sh`) still fail the gate scenario.
- **Lens attribution:** not filed under Tests. The executable step is exact, and all three failing arms work (`receipts/bdd/summary.txt`); only the comment is false. Not filed under RTL or Robustness, because no behaviour is involved.

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_crf_licence.cpp:1143` - "refused re-declaration emits no PDU" has no demonstrated failing arm

No arm I ran makes this check fail. The pre-#112 control fails 28 `[I]` checks but not this one, and the six missing-term mutants also open the licence for only a few cycles, with no media event inside that time. The licence, counter-pair and reset checks carry the acceptance. The PDU check follows structurally, but it has not been shown to fail. Optional fix: state this in the README failing-arms table, or stage a media event inside the window.

### S2 - SUGGESTION - Tests, Robustness - `sim_crf_licence.cpp` `grant_case` - no shipped case refuses a re-declaration made over a standing, admitted declaration

Every shipped case withdraws before it re-declares. So the fixture exercises the processor's invalidation only through the withdrawal path. My probe (`scripts/redeclare_probe.py`) covers the other path:

- **Staging:** a 224-byte declaration stays standing with its real grant high and no Listener. A 20,000-byte declaration is then made over it, with the same wire Listener Ready timing.
- **At the pin:** 181 checks pass, 0 fail (`receipts/redeclare/pin.run.log`). Across the four source/phase cases, four each of these PASS:
  - "preload holds its real grant";
  - "re-declaration retired the standing grant";
  - "optimistic window actually raised ACTIVE";
  - "refused ... never opened".
- **Against pre-#112 processor `7a47f578`:** 24 checks fail (`receipts/redeclare/prefix.run.log`). Every source/phase case opens the licence, adds a STREAM_START/STREAM_STOP pair, and resets all three seeded counters.

The behaviour is correct. A shipped arm would add regression protection for this path.

## Focus items

1. **Merge `8dc98a42`.**
   - `git show --remerge-diff` (`receipts/merge_remerge_diff.txt`) differs from Git's automatic merge only inside the five conflict blocks: REGISTER_MAP.md x2, milan_datapath.sv x2 and the milan_dp README x1. No other file or hunk changed.
   - In milan_datapath.sv, the resolution keeps dev's ACTIVE term (#530). Dev's #508 published-round paragraph just above the conflict is untouched auto-merge text. The resolution adds this PR's grant term: `assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] & pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];`.
   - Across the whole PR against dev, that assignment is the only non-comment RTL change. The `crft_stat_c[6]` line changes its comment only.
   - `8dc98a42..f219a5ed` changes RTL comments only.
   - The merge tree alone builds and passes the licence leg: 253 checks, 0 failures, with `[I]` still skipped at that commit (`receipts/merge_8dc98a42.*`).
2. **Unwarmed fixture.**
   - `[I]` preloads 224 bytes, withdraws, then re-declares 20,000 bytes. `[J]` runs the reverse. At this head, `receipts/head_clean.*` gives 415 checks and 0 failures.
   - I reproduced the pre-fix control myself, without touching the clone's submodule. I extracted the processor `hdl/` tree at `7a47f578` (the pre-fix parent of `a8f8ce81`; it has no `pend_acc_r`) with `git archive` into scratch and passed it as `PP_DIR`. The unchanged head harness and datapath then fail 34 checks (`receipts/prefix_control.*`):
     - 28 in `[I]`, 7 per source/phase: the grant rose, the licence opened, STREAM_START and STREAM_STOP were added, and MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX were reset;
     - 6 in `[J]`, on ACTIVE timing.
   - This matches the executor's reported control.
3. **Mutants.** My parallel driver ran the shipped `MUTATIONS` table and graded each arm with the shipped `verdict()`, which requires the named check (`receipts/mutants/`).
   - The three ACTIVE-removed (raw-grant-only) arms are caught with 23, 16 and 6 failures.
   - The three grant-removed (ACTIVE-only) arms are caught with 58, 29 and 29 failures, each on its named refused-source check.
   - My ACTIVE-OR-grant arm is caught with 79 failures.
   - My arm that drops the grant at AAF sources above 0 survives, as expected: the AX 1x1 shape has no such source (see Real limits).
   - BDD: the gate scenario passes clean, and fails for ACTIVE-only, grant-only and ACTIVE-OR-grant (`receipts/bdd/`).
4. **Docs.**
   - These no longer describe a residual window: CHANGELOG, FR_NFR, REGISTER_MAP, EGRESS_QUEUE_MAP, ieee8021q, the compliance matrix, the milan_dp README, and the `KL_pp_shadow.sv` and `milan_datapath.sv` comments.
   - Their "cannot open" claims hold at this head (focus item 2 and S2).
   - The one exception is F1.
   - The measured latency matches my run: AAF 5/5 and CRF 3/5 cycles for both TSpec histories, with ordinary Listener Ready adding 0 (`[B]` "opened on the cycle ACTIVE rose").
5. **Clauses.**
   - FR-SRP-03 as cited ("on failure the stream MUST NOT transmit") matches `docs/reference/FR_NFR.md:211`.
   - `docs/spec-refs.md` does not exist at this head, and `git log --all -- docs/spec-refs.md` is empty. I therefore checked the Milan v1.2 5.3.7.3 and 5.3.7.7 Table 5.4 citations, and the 802.1Q 34.3/34.4 citations, against the in-repo authorities: FR_NFR, the MILAN_COMPLIANCE_MATRIX 5.3.7.3 row, and ieee8021q Q-9/Q-10. They are consistent with each other and with the counters the fixture grades.
   - No standards text was available to check clause numbering at the source (Real limits).

## Lens results

```text
[R297] PASS RTL - hdl/milan/milan_datapath.sv:6623-6624 (gate), :1887 (lobs >0), :1917 (AAF 0), :2027 (AAF >0), :2506 (LWSRP_STATUS[8]), :3058 (Table 5.4 level), :5296-5323 (CRF licence, CRFT_CTRL[6]/[7]); hdl/milan/KL_pp_shadow.sv:635-642,1260-1261; protocol-processor 990f9652 KL_srp_admission.sv and KL_srp_top.sv (7a47f57..a8f8ce81) - checked against the #551 decision and the processor contract (protocol_processor_top.sv:517-526, integrator.md:284-285, which prescribe ACTIVE AND srp_sr_admitted_o). The per-source AND is SRP_TALKERS_C wide on both slices. Both terms come straight from one processor instance on one clock, with no added register and so no skew; both reset low. Status-only readers (LWSRP_STATUS[6]/[9], LWSRP_SLOPE) are unchanged and documented.
[R297] PASS Robustness - receipts/head_clean.run.log, receipts/prefix_control.run.log, receipts/redeclare/{pin,prefix}.run.log - refused changed and identical TSpecs, both sources, both round phases, withdraw-then-declare and declare-over-standing-declaration, reversed history, and the closing edge through either term. The pre-fix processor is detected on both declaration paths. The first declaration after reset is stated as outside the arm; by RTL reading of 990f9652, slope_valid_r resets to 0, so that round is discarded as pending rather than granted.
[R297] PASS Tests - tb/verilator/milan_dp/sim_crf_licence.cpp:1047-1200, crflic_mutants.py:52-80, crflic_probes.vlt, tests/steps/milan_streaming_licence_steps.py:174-186 - with the pinned 5.050 simulator: 415/0 at head; every shipped mutant caught on its named check; the pre-fix control fails; the exact-composition BDD step fails on three wrong-term arms; the legacy --unwarmed-refusal invocation produces identical output (receipts/head_flag.run.log). S1 and S2 are optional.
[R297] MINOR Docs - tests/features/milan_streaming_licence.feature:92-94 - F1. Everything else in the lens is correct: CHANGELOG, FR_NFR, REGISTER_MAP (0x750, 0x694, 0x698, 1105-1140), EGRESS_QUEUE_MAP, ieee8021q (35, 50-63, Q-9, Q-10, MRP-4), MILAN_COMPLIANCE_MATRIX:179, the milan_dp README, and the RTL comments match the RTL and runs. These gates return rc 0 (receipts/static/): docs_check, check_em_dash --base 864b36f5 (0 findings in 197 added lines, 339/339 arms), doc_style, gen_toc --check, doc_paths, gen_module_matrix --check.
[R297] MINOR Conformance - tests/features/milan_streaming_licence.feature:92-94 - F1 leaves round-3 acceptance item 3 unmet for this artifact. The rest of the conformance bar is met:
  - issue acceptance 1-3: the decision is recorded; the refused re-declaration shows no licence, counter pair, reset or PDU, with failing arms; the gates pass (exact-head hosted: 21 success, plus 1 skipped nightly physical context, receipts/hosted_checks_f219.txt);
  - assignment: the admitted case streams, latency is measured and stated, and the named documents are updated;
  - round 3: dev is merged, the arm is mandatory, the EXPECTED-FAIL skip is removed, the drop-grant mutants fail, and the pre-fix control fails.
```

## Prior public review findings on PR #553, resolved at this head

Round 1 of this review ([R297-1](https://github.com/kebag-logic/milan-fpga/pull/553#issuecomment-5815993078), head `4eca4540`):

| ID | Severity | State at f219a5ed | Evidence |
|---|---|---|---|
| R297-1 F1 | MAJOR: a cold slope pipeline let a refused declaration open the licence | **CLOSED** | Processor pin `990f9652` contains `a8f8ce81`. `[I]` (the cold case: previous TSpec 224, refused 20,000) is a required default pass: 415/0. The pre-fix control fails it with 28 checks. `[J]` re-measures changed-TSpec latency. Beyond the round-1 probes, declare-over-declare passes at the pin and fails pre-fix (S2). First declaration after reset: RTL reading only (see RTL line above); README states it as outside the arm. |
| R297-1 F2 | MAJOR: the BDD scenario pinned the superseded gate; `rtl-fast` red | **CLOSED** | `milan_streaming_licence_steps.py:174-186` pins the exact AND. Clean 5/5; ACTIVE-only, grant-only and OR arms fail. Hosted `bdd-conformance` and `rtl-fast` succeed at `f219a5ed`. The scenario's comment is the new F1. |
| R297-1 F3 | MINOR: generated traceability stale; Q-9/Q-10 lost their module citation | **CLOSED** | `gen_module_matrix.py --check` rc 0 ("69 modules"). `MODULE_MATRIX.md:160` and `hdl/milan/README-tests.md:15` list `KL_pp_shadow` against 34.3 and 34.4. Q-9/Q-10 name `KL_srp_admission` (behind `KL_pp_shadow`) with the PROCESSOR status. |
| R297-1 F4 | MINOR: remaining ACTIVE-only descriptions, including the interface contract | **CLOSED** | Updated: `milan_datapath.sv:1642-1645`, `:5293-5295` and `:5334`; `ieee8021q.md:35`; milan_dp `README.md:27`; `MILAN_COMPLIANCE_MATRIX.md:179`. `KL_pp_shadow.sv:635-641` records the decided qualification of ACTIVE. The processor side now states it as well (`protocol_processor_top.sv:517-519`). A repository search finds no remaining ACTIVE-only licence description. |

The other round-1 review ([R296-1](https://github.com/kebag-logic/milan-fpga/pull/553#issuecomment-5815951481), head `4eca4540`):

| ID | Severity | State at f219a5ed | Evidence |
|---|---|---|---|
| R296-1 F1 | MAJOR: the first-round grant was stale | **CLOSED** | Same evidence as R297-1 F1. Its P1 staging equals the shipped `[I]`, and its P2 equals `[J]`. The latency statement covers changed TSpecs (5/5, 3/5). |
| R296-1 F2 | BLOCKER: BDD scenario failing; `bdd-conformance` red | **CLOSED** | Same evidence as R297-1 F2. The two stale rows it named (compliance matrix 179, milan_dp README 27) are updated. |
| R296-1 F3 | MAJOR: generated traceability stale | **CLOSED** | `gen_module_matrix.py --check` rc 0 at this head (`receipts/static/module_matrix.log`). |
| R296-1 F4 | MINOR: Q-9/Q-10 dropped the mapping, status, caveat and rationale, and over-claimed the 75% check | **CLOSED** | Q-9/Q-10 restore `KL_srp_admission` behind `KL_pp_shadow`, the PROCESSOR status, the "went with the deleted `lwsrp` suite" caveat and the 34.3/34.4 rationale. Q-9 now says the fixture "does not test the 75 % boundary". `ieee8021q.md:35` is corrected. `milan_datapath.sv:6573-6576` now says licences read the raw grant per source. |

None of the round-1 findings is retained. F1 of this round is new.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #551 body; decisions 5813147847/5816014072; assignments 5814963437/5831903033/5832468673; PR body; `FR_NFR.md:211-230`; feature scenario; `receipts/head_clean.*`, `prefix_control.*`, `hosted_checks_f219.txt` | R297-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| RTL | CLEAN | `milan_datapath.sv` gate and all consumers; `KL_pp_shadow.sv` ports; processor `990f9652` admission, top and interface docs; `receipts/merge_remerge_diff.txt` | R297-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Robustness | CLEAN | licence leg `[G]`-`[J]` at the pin and pre-fix; declare-over-declare probe at the pin and pre-fix; closing edges | R297-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Tests | CLEAN (S1, S2 optional) | `sim_crf_licence.cpp`, `crflic_probes.vlt`, `crflic_mutants.py` (6 shipped + 2 reviewer arms), BDD gate scenario (clean + 3 arms), merge-only leg, legacy flag run | R297-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |
| Docs | UNCLEAN (F1) | CHANGELOG, FR_NFR, REGISTER_MAP, EGRESS_QUEUE_MAP, ieee8021q, MILAN_COMPLIANCE_MATRIX, MODULE_MATRIX, milan_dp README, RTL comments, feature file; `receipts/static/*` | R297-2 | f219a5edaa191b33acc8b77abd22469f8f0db1f9 |

## Real limits

- All simulation ran on the AX 1x1 TDM8 two-source shape, on the leg's compressed millisecond grid. No other geometry was run.
- AAF sources above index 0 read the same pinned `lwsrp_stream_gate` vector. No shipped or reviewer arm simulates them: my mutant for them survives because this shape has none.
- The fixture stages the processor's S_GATE service tuple through `public_flat_rw` rather than issuing a controller request. As its README states, it is boundary staging and makes no end-to-end controller timing claim.
- The first declaration after reset is covered by RTL reading only.
- `docs/spec-refs.md` does not exist, and no standards text was available. Clause numbers were checked for consistency across in-repo authorities, not against the standards.
- The markdown gates ran in an existing environment whose requirements hash matches `tools/markdown/requirements.txt` (`40cdefe0`). Nothing was installed.
- The simulator is the scoped 5.050 wrapper (`receipts/tool_identity.txt`).
- Not run, per round rules: full parent/PP/gPTP/Yosys/builder banks, `xvlog_gate` (no Vivado), act/Docker, and host act_ci. `lint_rtl.py --check` and the idiom and source-list checks did run (rc 0).
- Physical calibration NOT RUN. Simulation and field skips are not hardware proof.
- I recorded hosted exact-head contexts only (21 executed success; the physical gPTP context skipped). Hosted and act acceptance belong to the manager.

## Pending manager duties

- Route F1 to the executor. A comment-only change to the feature file un-covers Docs and Conformance only; RTL, Robustness and Tests stay banked here unless their artifacts change.
- Re-review at the fixed head for Docs and Conformance, including that the BDD scenario still passes and its three wrong-term arms still fail.
- Hosted/act acceptance at the final exact head, and the final current-dev candidate build (source base `864b36f5`, live dev `864b36f5` at review start).
- A second independent positive review, and explicit maintainer authorisation before any merge.
- Optional: S1 and S2.

## Receipts and restoration

- Portable scripts are in `scripts/`:
  - `leg.sh`: builds and runs the leg in a disposable build directory.
  - `prefix_control.sh`: pre-fix processor via `git archive` plus `PP_DIR`.
  - `mutants.py`: parallel mutation driver using the shipped verdict.
  - `bdd_arms.sh`: BDD arms in scratch tree copies.
  - `redeclare_probe.py`: S2 probe.
  - `static_gates.sh`: focused static and documentation gates.
- Raw logs are in `receipts/`, with hashes in `MANIFEST.sha256`. Home-directory paths are redacted to `$HOME`.
- The clone was never edited. Probes used scratch copies, `git archive` extractions, or overridden `DP_SRC`, `PP_DIR` and `CRFLIC_MDIR`. `receipts/clone_state_after_probes.txt` records the final state:
  - HEAD and write-tree equal `f219a5ed` / `aca067d4`;
  - all 892 tracked files rehashed with 0 mismatches;
  - index equals the HEAD tree in mode, blob and path, and every `ls-files -v` flag is `H`;
  - all four gitlinks and the three initialised checkouts are unchanged and clean.
- Only ignored build by-products remain: the milan_dp ROM hex files and two `__pycache__` directories.

R297-2 FINISHED
