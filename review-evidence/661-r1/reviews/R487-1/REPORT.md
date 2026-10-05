[R487] NEGATIVE - exact head 42f654478c11bd8f2b070969d83140587190f276

# R487-1: external review of issue #661 / PR #663

- Head `42f654478c11bd8f2b070969d83140587190f276`, tree `1772c37de75f39a15a5491d0ecfe9ba045c929b9`, branch `661-pp-pin-ead80360`.
- Source base: dev `506d91dbeeba585d72d2e80d92fca799c719f8ee`. Live dev at review time: `fa450d301805881ad713b67521477bf042ddadfd`.
- Processor gitlink: `631eeb342ca1e3fa80e734077a56a943aee76ff1` -> `ead8036035affd53ef4b29979190f2f4f67084c0`.
- Role: external cleared-context reviewer. I reconstructed the review from public state only: AGENTS.md, CONTRIBUTING.md, the issue body and manager comments, the linked issues, the diff, and the public evidence tree at `0010a410`. I applied all five lenses.

## Verdict

NEGATIVE. There is no BLOCKER or MAJOR finding.

- **What passed:** the gitlink, the four adaptations, every pin-derived record, resource baseline D, the closing claims and the #656/#657 exception handling all hold, and I re-verified them independently.
- **Why NEGATIVE:** one MINOR finding remains open, and that alone forces a NEGATIVE verdict.
  - **F1 (open):** the adopted `available_index` rule has not been carried into four other parent statements. One of them is a parent test check that now fails a conformant sequence.
  - **F2 (resolved):** the PR body published local host paths and a local account name. A manager edit of the PR body at the unchanged head (2026-10-05T09:20:55Z) fixed this, and I verified the fix (see F2).
- **Unclean lenses:** Conformance, Tests and Docs, all under F1. RTL and Robustness are clean.

## Answers to the six review questions

1. **The four adaptations: equivalent.**
   - I applied each supplied patch in the assigned order (c8, p2-p1, c10, 232) to the gitlink commit `4a2f8ae4`, in a private index.
   - Every cumulative tree equals its committed tree: `6298dd24` = `dbd9e246`, `e7afc773` = `eefffe50`, `dd9ff6fb` = `880a40fc`, `35a2525f` = `42c63ebc`. Receipt: `receipts/patch_equivalence.log`.
   - **P2 amendment:** `SAVED_STATE_MATERIALIZATION.md` section 8.8, W13 and section 15 item 4, and the FASTCONNECT page, match the processor RTL and docs at the pin:
     - `NVM_MEM_TMO_CYC_P = CLK_HZ_P`, described as 20 x the 50 ms grant hold;
     - 1 + `RETRY_MAX_P` = 3 attempts, then `nvm_alarm`;
     - `restore_rb_o` exists at the top and is already exported by `KL_pp_shadow`.
   - **L6/L10 cleanup:** the processor lint (`model_rules.py` L6/L10/L1) covers every refusal the deleted `aem_image_checks.py` made. Six mutation probes are each killed by the PR's own gate 36b tests (`receipts/mutate_gate36b.summary`):
     - each emitter with the lint off (two probes);
     - each waiver pass-through dropped (three probes);
     - the waiver narrowed to ports 0..6.
2. **Pin-derived records: correct at the new pin.**
   - **ROM digests:** I regenerated both ROMs outside the tree. They match the new `ead80360` rows, which equal the `631eeb34` rows (`receipts/rom_digests_check.log`).
   - **Generated records and gates:** source lists (42/42 tops, 0 recorded), the port ratchet (1,759 processor ports), naming, test-evidence dispositions, the submodule page and the boundary diagram all pass their generators' `--check` at head.
   - **Capture:** `check_nvm_capture.py` passes. Census, clocks and firmware are unchanged, so no re-measurement was owed.
   - **xvlog budget:** the line numbers (`vd_push_w` at 383, `cancel_hit_w` at 194) match the pin.
   - **SUBMODULES table:** each "`main` after merge" SHA matches processor `main`'s first-parent history. Public processor `main` is identical to `ead80360`.
3. **Resource baseline D: consistent and policy-preserving.**
   - **Policy unchanged:** the policy fields (tolerances, floors, ceiling) are byte-identical between base and head. Only figures, scopes, `measured` notes and `inputs_sha256` moved (`receipts/baseline_policy_diff.log`).
   - **Figures reproduce:** every endpoint figure and every D-minus-C sub-block cell in the finding recomputes exactly from the JSON at base and head (`receipts/area_table_check.log`):
     - route 50,318 LUT / 54,214 FF / 15,789 slices / 74 RAMB36;
     - WNS +0.108 ns, WHS +0.036 ns;
     - standalone 23,178 and 29,853 LUT.
   - **Derived arithmetic checks out:** 79.37 %, 12,278 over, 61 slices free, 10,608 = 22,886 - 12,278, the 0.078 ns margin, and the outside-wrapper split (+569 / +90 = +475 / +83 plus +94 / +7).
   - **Gate checks:** `pp_resource_gate.py check-baseline` passes (3 endpoints). `--selftest` passes 260 arms plus 500 fuzz cases.
   - **Standalone WNS:** it fell (8x8 -1.947 -> -4.095 ns), but WNS is not a gated field for standalone endpoints, and the finding correctly calls it an internal estimate.
4. **Closing claims: supported.**
   - **#639:** its acceptance requires the gate baseline to be re-recorded, and D does that.
   - **#234:** the manager's remaining-criteria record leaves only criterion 2. Each flop array in the A storage table is addressed in D: the registry, SRP FIFOs and arm queues map to RAM32M, and the counter-stamp bank stays in flops by design.
   - **60 % target:** every page and the PR body keep it unmet (12,278 LUT over) and assigned to #640.
5. **#656 / #657.**
   - **Base vs head:** the published comparison shows identical verdict lists at base and head (139/3 rc 2; 28 PASS / 4 FAIL rc 2).
   - **After merge:** nothing in this PR touches `tb/verilator/milan_dp*`. I built the merge candidate (head plus live dev `fa450d30`, tree `57cc8b8a`, never committed) and ran `make -C tb/verilator/milan_dp_gptp`. It returned **rc 0**: physical 139 checks / 0 failures, and accounting 6 / 20 / 14 with 0 failures. The three #656 audio-order checks pass.
   - So nothing in this PR stops `milan_dp_gptp` passing once merged (`receipts/cand_milan_dp_gptp.log`).
6. **Scope.**
   - No parent RTL, firmware, constraint or SoC interface file changed. `KL_pp_shadow.sv` is identical.
   - `milan_soc.py` changes only inside `build_desc_image` (the retired checker).
   - The processor top gains only `parameter NVM_MEM_TMO_CYC_P = CLK_HZ_P`, with no port line changed (`receipts/scope_check.log`).
   - P1's name records match the parent backend's NAME allocation: id `0x80` + ordinal, 8-byte header plus 64 bytes, and one `DESC_NAME_ENTRIES_P` feeding both sides. So a name write cannot be refused as unallocated.

## Findings

### F1 - MINOR - Conformance, Tests, Docs

**Where:** the parent still states the superseded `available_index` rule after adopting processor PR #152:

- `docs/design/SAVED_STATE_MATERIALIZATION.md:1037`;
- `tb/tools/avtp_wire_truth_checks.py:553-559` and `:586-589` (the check's docstring and verdict text);
- `avdecc/gen_aemi_image.py:105-106`;
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:154`.

**Authority and evidence:**

- At `ead80360`, `KL_adp_engine.sv:703-719` increments only after ENTITY_AVAILABLE and resets to 0 after ENTITY_DEPARTING (IEEE 1722.1-2021 Section 6.2.2.15). This PR's own `REGISTER_MAP.md:1032-1037` now says so.
- The four places above still say the index "increments on every transmitted ADPDU", citing 6.2.2.10 / 6.2.1.14.
- The compliance matrix says the increment-policy divergence "stays recorded in the processor's docs", but PR #152 removed that divergence.
- The wire-truth check's repeat rule encodes the old behaviour. A conformant sequence under the adopted rule is graded FAIL: an entity disabled during its first TMR_DELAY sends DEPARTING carrying 0 (processor `04_adp_engine.md` DELAY/SHUTDOWN row), then ENTITY_AVAILABLE carrying 0.
- Probe (`receipts/wire_truth_adp_probe.log`): DEP 0, AVAIL 0, 1 grades `wt.adp.available-index-advances` **FAIL**. The ordinary DEP N, AVAIL 0 sequence passes. At the base pin the old processor never produced that repeat.

**Impact:**

- A parent conformance tool can report a false FAIL on the adopted DUT.
- The saved-state contract and the compliance matrix contradict the register map within the same tree.

**Required outcome:**

- State the adopted rule in all four places, citing Section 6.2.2.15.
- Make the wire-truth check accept a reset to 0 after ENTITY_DEPARTING, while still refusing a repeat between consecutive ENTITY_AVAILABLEs.
- Add a self-test arm for each case.
- Alternatively, the manager publicly records a decision that defers this and names the owning issue.

**Verification:**

- `python3 tb/tools/avtp_wire_truth_selftest.py` with the new arms;
- the probe above grades PASS for the conformant sequence;
- `docs_check.py` passes;
- a grep finds no remaining "every transmitted ADPDU" statement outside history.

### F2 - MINOR - Docs - RESOLVED at the current PR body

**Status:** the body as fetched at review start had this defect. The manager's body edit at the unchanged head (comment 5991634080, 2026-10-05T09:20:55Z) removed it. `receipts/pr_body_scan.log` shows the current body (sha256 `b42523a0...`, head still `42f65447`) with:

- no `/data/`, `/home/`, `/tmp/`, `sudo` or `-u <account>`;
- no "is local" or "not been pushed".

The finding does not hold at the current body. The original text follows for the record.

**Where:** the PR #663 body as fetched at review start, sections "How to get into the same state" and "How to validate".

**Authority and evidence:**

- CONTRIBUTING.md section 6: "No bench-identifying information: hostnames, home paths ... Use placeholders".
- The live body publishes local absolute paths under the validation storage tree, and a local account name in `sudo -n -u <account>`.
- The manager's published copy of the same body (`review-evidence/661-r1/author/PR-BODY.md`, `path_redacted: true` in its MANIFEST) replaces exactly these with `$VALIDATION_TOOLS` / `$VALIDATION_STORAGE`. So the live body is the unredacted form the evidence policy removes.
- The same section also says the branch "is local and has not been pushed", but the PR's branch is on the remote.

**Impact:** host-identifying details appear in a public review object, and the replay commands point at paths a cold reviewer cannot use.

**Required outcome:**

- Edit the PR body to the placeholder form already used in the published packet copy, with no account name.
- Replace the "local branch" setup with fetching the PR head.

**Verification:** the live PR body contains no host path or account name, and the setup steps resolve from a fresh clone.

### Suggestions (non-blocking)

- **S1 - Tests:** the parent `nvm_cosim` harness includes the processor port, arbiter and binding manager, but not `KL_aecp_nvm_writer`. P1's name records reach `KL_nvm_backend` only in the full build. I found them compatible by static comparison only. A co-simulated name-record write, restore and rollback belongs with #637 / lane 3.
- **S2 - Robustness:** the retired parent checker derived its L10 bounds from the consumer (`gen_ucode.py` `SSR_LIST_OFF`/`SSR_WALK_MAX`). The processor lint uses its own literals (`RATES_OFFSET = 144`, `RATES_MAX = 8`). They agree today. A processor-side tie between the two would restore the lost cross-derivation.

## Other public review findings on this PR

- **At review start:** PR #663 carried no findings, only the two review-start notices.
- **Concurrent round:** after I had written my own verdict and ledger, a concurrent internal round published NEGATIVE (comment 5991604022). I read it then. Its items at this head:

| Item | Disposition here | Evidence |
|---|---|---|
| R486 F1 (host paths and account name in the body) | RESOLVED, same defect as my F2 | `receipts/pr_body_scan.log` |
| R486 F2 (body said "213 ports") | RESOLVED. The body now says 212, and the repository's `scripts/sv_ports.py` counts 212 ports at both pins (parameters 41 -> 42) | `receipts/top_port_count.log` |
| R486 R1 (stale "local branch" setup) | RESOLVED in the current body | `receipts/pr_body_scan.log` |
| R486 R2 (`SUBMODULES.md:148`, "A parent lane transfers names to `d3_unflushed_o`" reads as done) | RETAINED as RESIDUE; the line is unchanged at head. Fix as R486 states | `docs/reference/SUBMODULES.md:148` |
| R486 R3 (`PP_DESCRIPTOR_OWNERSHIP.md:333`, F5 row silent on the 8x8 waiver) | RETAINED as RESIDUE; the line is unchanged at head. Fix as R486 states | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:333` |
| R486 S1 (note the standalone 8x8 WNS fall) | Agree, SUGGESTION. It matches my question 3 observation | `receipts/area_table_check.log` |

That round did not report my F1.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `REGISTER_MAP.md:1025-1039` against `KL_adp_engine.sv:703-719`; P2/P1 amendments in `SAVED_STATE_MATERIALIZATION.md` (sections 8.8, 15 items 2/4, W13) against `protocol_processor_top.sv:160-175`, `KL_aecp_nvm_writer.sv:148,195,1063` and `08_timing.md:46`; L6/L10 rows in `PP_DESCRIPTOR_OWNERSHIP.md` against `model_rules.py:171-202,673-860`; closure claims against #234, #639 and #640 | R487-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| RTL | CLEAN | `scope_check.log` (no parent RTL/firmware/SoC change; one new top parameter, no port); `KL_pp_shadow.sv:997-1007` name count shared with the writer; `KL_nvm_backend.sv:227-255,408-409` against `KL_aecp_nvm_writer.sv:110-118,187-215`; deadline against `T_HOLD_MS_P = 50`; xvlog budget lines; ROM regeneration; `pp_shadow` 2,169/0; `nvm_cosim` 465/0 with all mutants killed; merge-candidate `milan_dp_gptp` rc 0 | R487-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Robustness | CLEAN | Silent-device path (DEADLINE, 3 attempts, `nvm_alarm`, quarantine never released by time); stale and narrowed waiver refusal (probe M6); emitter lint-off refusal (M1/M2); resource gate fail-closed self-test and fuzz; `check-baseline`; dev #652 backend guard against this PR (no interaction); merge candidate against live dev | R487-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Tests | UNCLEAN (F1) | gate 36b at head (`gate36b_head.log`) and 6/6 mutants killed; C10 self-test 50/50 and 4/4 mutants killed (`mutate_c10_selftest.summary`); `measure_test_evidence` dispositions against `acmp_mutants.py` and `test_gen_desc_image.py`; wire-truth ADP check probe (F1) | R487-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Docs | UNCLEAN (F1; F2 resolved) | `CHANGELOG.md`, `SUBMODULES.md`, `AREA_BUDGET.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `findings/README.md`, `PP_DESCRIPTOR_OWNERSHIP.md`, `ENDSTATION_BUILDER.md`, `CODE_QUALITY.md`, `pp_shadow/README.md`; `docs_check.py` 0 findings; the PR #663 body at review start and as edited (body sha256 `b42523a0...`) | R487-1 | `42f654478c11bd8f2b070969d83140587190f276` |

## Real limits

- **Vivado not rerun:** I did not rerun the route or standalone builds. I checked D against the recorded JSON, C, the policy and the gate's own checks. The raw reports and checkpoints are published only as digests, so I did not inspect them.
- **Full banks not run:** I did not run the parent sweep, processor sweep, Yosys, whole builder, docs workflow, or the #657 render campaign; they were not authorised here. For those I rely on the published author and manager evidence.
- **Patch provenance:** I compared the patches using the packet copies (MANIFEST original = published digests), not copies taken from the processor lanes.
- **W13:** the amended W13 behaviour is evidenced only by processor suites. The parent page says so ("not re-executed here").
- **Hosted checks at my read:** 18 contexts succeeded at the exact head, `Verilator shard 1/5` was in progress, and `Physical gPTP (nightly and manual)` was skipped (`receipts/hosted_check_runs.tsv`). A skipped context is not executed evidence.
- **Hardware:** no hardware, flashing or physical calibration was run. Field skips are not hardware proof.

## Pending manager duties

- Dispose of F1 (fix, or record a decision), then have the corrected head re-reviewed.
- Carry R486's R2 and R3 to the residue checklist.
- Build and validate the final candidate at the merge turn on live dev. My candidate tree `57cc8b8a` is evidence only.
- Accept the hosted and act results, including `Verilator shard 1/5`.
- After merge: flash, run the soak, and check post-merge containment.

R487-1 FINISHED
