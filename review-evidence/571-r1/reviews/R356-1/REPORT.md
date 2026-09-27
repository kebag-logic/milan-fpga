[R356] POSITIVE - exact head f8a52f919bd309960046330a5af127b56731cb27

# R356-1 internal independent review: issue #571 / PR #597

- Exact head: `f8a52f919bd309960046330a5af127b56731cb27`, tree `f707dc8a91bbb708cd07c895bc2d744cdb6e8d83` (one commit on dev `2a2a7bb655e528edc3087c88033cd3a47546feb4`).
- Round: R356-1, first review of PR #597. Cleared context, detached clone, no author contact.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md; issue #571 body; assignment comment 5857833068 (decision: bind, no refusal); the correction comment 5858103665 (`docs/spec-refs.md` is not a repository file; the Milan v1.2 §5.3.3 citation plus construction evidence is accepted); the author's TAKEN and REVIEW READY comments; the PR body; processor pin `870ff88a` integrator section 2 (`docs/guides/integrator.md:68-70`); `git diff 2a2a7bb6..f8a52f91`; published evidence tree `ab3d66a7:review-evidence/571-r1`.
- Prior public review findings on this PR: **none exist**. The only PR comment is the manager's review-start notice (5858108931), so none are carried forward.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding. All five lenses are covered clean at this exact head. Two optional SUGGESTIONs follow; they do not affect coverage.

## What was verified (assigned checks 1-7)

**(1) One census, no literal at any hop.** `sw/builder/endstation_builder.py:2788-2790` emits `AEM_N_AUDIO_UNIT_C`, `AEM_N_CLKDOM_C` and the new `AEM_N_CONTROL_C` from the same `dc = overlay["descriptor_counts"]` (line 2783). That census is built in `_overlay_document` (`:5153-5159`, `"AUDIO_UNIT": 1 ... "CLOCK_DOMAIN": 1, "CONTROL": 1`). The CONTROL count matches what the model emits: `avdecc/aem_assemble.py:237` appends exactly one `(CONTROL, 0, d_control_identify(...))`, unconditionally. The served image (`_entity_model_image`, `:2297`) and the gate's ROM rendering (`:3139`) both use the same `build_model`. The gate ties census to constructor per kind (`scripts/check_entity_shape.py:575-576`). Reviewer mutant E-d (census literal `CONTROL: 2`) is killed by that arm (`generated ROM CONTROL descriptors: got 1, expected 2`). Emitter: `dc['CONTROL']` is used without a `.get(...,0)` fallback, so a missing census key fails loudly. That is stricter than the two existing lines and acceptable.

**(2) Two binding hops.** `hdl/milan/milan_datapath.sv:7426-7429` passes `AEM_N_AUDIO_UNIT_C`, `AEM_N_CLKDOM_C` and `AEM_N_CONTROL_C` to `pp_shadow`. `hdl/milan/KL_pp_shadow.sv:239` adds `N_CONTROL_P` (default 1). `KL_pp_shadow.sv:1060-1062` binds `u_pp` as `.N_AUDIO_UNIT_P (N_AUDIO_UNIT_P)`, `.N_CLK_DOMAIN_P (N_CLK_DOM_P)` and `.N_CONTROL_P (N_CONTROL_P)`. The parent name `N_CLK_DOM_P` is kept (line 237). No literal appears at either hop. The only `protocol_processor_top` instance in the parent is `u_pp`, and the only `KL_pp_shadow` instance is `pp_shadow`.

**(3) Zero is unreachable. The processor refuses zero if it ever arrived.**
- The constructors are unconditional: `_overlay_document` and `aem_assemble._entity_descriptors` (`:210`, `:235`, `:237`).
- `probe_zero_reach.py` wrote 12 hand-edited variants of `endstation_ax7101_1x1_tdm8.yaml` (`receipt-zero-reach.txt`). Variants V1-V6 and V9 add `descriptors: {CONTROL/AUDIO_UNIT/CLOCK_DOMAIN: 0}`, `descriptor_counts: {CONTROL: 0}`, `controls: []`, `audio_units: []`, `entity.controls: []`, `entity.identify: false` and `clocking.clock_domains: 0`. All of them load, and census, header and constructor all stay at 1/1/1.
- Four variants are refused with a named `ConfigError`: `names.control_identify: null` and `''` (V7, V8), `board.features.identify` (V10), and an empty `audio_unit_rates_hz` (V11).
- At the processor, forcing each count to 0 on `KL_pp_shadow` stops elaboration with a hard error. `KL_aecp_dyn_state.sv:164/172/177` reports "Size of range is '[0]', must be positive integer" (`receipt-elab-zero.txt`, `raw/elab-zero-*.log`).
- The gate also asserts `>= 1` per kind (`check_entity_shape.py:395-402`).

**(4) Two-hop check kills omission, literal and swap at both hops.**
- The author's 24 self-test mutants all reject, and `--self-test` reports 219 checks with 0 failures (`receipt-entity-shape-selftest.log`). The plain gate reports 166 checks with 0 failures (`receipt-entity-shape.log`).
- The reviewer's own 32 verdicts are in `probe_gate_mutants.py` / `receipt-gate-mutants.txt`, and all 32 came out as expected.
  - Hop 0 (H0-a..h): wrong symbol, sized literal `32'd1`, 3-way rotation, binding commented out, local alias, `ifdef` alternate, duplicate value and renamed instance are all killed.
  - Hop 1 (H1-a..h): wrong symbol, `32'd1`, block-comment unbind, 3-way rotation, the undeclared `N_CLK_DOMAIN_P` name, an expression `N_CONTROL_P - 1`, all three unbound and a renamed instance are all killed.
  - Equivalent rewrites (H0-i, H0-j, H1-i: comment inside the value, line-wrapped values) are accepted, so the check does not raise false alarms on formatting.
  - Emitter mutants: a cross-wired CONTROL line (E-a), a hard-coded 1 (E-b) and a cross-wired AUDIO_UNIT line (E-e) pass the plain gate at shipping counts, as they must when every count is 1. The self-test's distinct 2/3/4 census oracle kills all three. That self-test runs in CI (`.github/workflows/docs.yml:449`).
  - Omitting the CONTROL line (E-c) is killed by both.
- Integration liveness at elaboration (`receipt-elab-columns.txt`): raising `N_AUDIO_UNIT_P` to 2 at the 1x1 shape changes the post-elaboration stages (PreOrder/Scoped/WroteAll/WroteFast) differently at head than at base. So `u_pp` really consumes the wrapper parameter at head. `N_CONTROL_P=3` and `N_CLK_DOM_P=2` at head also change those stages.

**(5) Five configurations: only the header line changes.** `probe_builds.sh` built all five tracked configurations with `--write-rtl` in disposable base and head tree copies (`receipt-builds.txt`, `receipt-tree-diff.txt`). All ten builds returned rc 0.
- Per configuration the output has 10 files. The only difference is `adp_shape_defaults.svh` gaining exactly `localparam int AEM_N_CONTROL_C    = 1;` after line 37.
- The other 9 out-dir artifacts per configuration are byte-identical, 45 of 45.
- A whole-tree diff after the builds shows the same result for the tree-side outputs: both sweep fragments and `hdl/common/csr/gen/*` are identical, and only the 5+1 headers and the six changed source files differ.
- `KL_pp_shadow` elaboration was compared at the AX 1x1 and 8x8 generated parameters with Verilator 5.050 (`receipt-elab-columns.txt`, `raw/stats-*.txt`). Base and head differ only in the pre-parameterisation `Link` column: +1 parameter VAR, +3 PINs and the literals and references that go with them. All post-elaboration stage columns (PreOrder, Scoped, WroteAll, WroteFast) are identical for both shapes.
- A `-Wall` lint of `KL_pp_shadow` gives 196 warnings at base and 196 at head, with no normalized delta (`receipt-lint-delta.txt`).

**(6) Tracked generated headers are builder output.** The regenerated headers for each of the five configurations are byte-identical to the committed `configs/generated/<cfg>/gen/adp_shape_defaults.svh` blobs at head. The committed `hdl/common/gen/adp_shape_defaults.svh` is byte-identical to the regenerated AX 1x1 header, which is its stated owner (`receipt-builds.txt`). The gate's arm D also agrees (`receipt-entity-shape.log`). No sign of hand edits.

**(7) PP_DESCRIPTOR_OWNERSHIP.md addition (this PR's text only).** Lines 49-70 were checked sentence by sentence against the code above.
- The flow description matches the code: census → `gen/adp_shape_defaults.svh` → `milan_datapath.pp_shadow` → `KL_pp_shadow.u_pp`.
- The four-column table matches the code, including `N_CLK_DOM_P` → `N_CLK_DOMAIN_P`.
- The unconditional-construction claims match the code.
- "zero is unreachable" matches probe (3).
- The gate and self-test description matches `check_entity_shape.py` and `entity_shape_selftest.py:598-649`.
- The processor link is pinned to the current gitlink `870ff88a`, and its `#integration-parameters` anchor exists (`protocol-processor/docs/guides/integrator.md:48`).
- The Milan citation "Section 5.3.3" is the one the manager accepted in the correction comment. The repository's own clause map puts the per-descriptor mandates under §5.3.3.x, with IDENTIFY at §5.3.3.10 (`docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:146-152`).
- No other parent document lists unbound processor parameters, so the new section is the only inventory note needed.
- The docs gates pass: docs_check, doc_paths, gen_toc `--check`, feature_status, doc_style and em_dash `--base` (`receipt-gates.txt`).

**Scope.** No processor source changed. The gitlinks equal the base: `protocol-processor` `870ff88a`, `gptp-processor` `5dce647a`, `external` `efeb541a` and `third_party/verilog-axis` `48ff7a7e` (`git ls-tree` base vs head, `receipt-restore.txt`). The diff touches only the 12 files listed in the PR, and none is outside the assigned scope.

**Assigned gates re-run by the reviewer at head, all rc 0** (`receipt-gates.txt`): `sw/builder/test_declarations.py`, `scripts/check_entity_shape.py` with and without `--self-test`, `scripts/check_nvm_capture.py`, the docs gates above, `scripts/check_py_idiom.py`, and `git diff --check 2a2a7bb6 f8a52f91`.

## Findings

No BLOCKER, MAJOR or MINOR finding.

```text
[R356] SUGGESTION Docs — docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:62-63,70 — forward-referenced abbreviations and a mid-page link definition
Requirement/evidence: the new text uses `B._overlay_document` / `A._entity_descriptors` in "Ownership boundary", but the page defines the B/A source abbreviations later (":79 Source abbreviations below", table rows :98/:100); the new `[integration-parameters]` definition sits at :70 while every other reference definition of the page is collected at :316-328.
Impact: readability only; every gate passes and the statements are accurate.
Required change: optional — spell out the file paths (or point at the abbreviation table) and move the link definition to the page's reference block.
Verification: docs gates stay rc 0; text reads without a forward reference.
```

```text
[R356] SUGGESTION Docs, RTL — hdl/milan/KL_pp_shadow.sv:227-239 — parameter group comment predates the processor binding
Requirement/evidence: the group comment still titles these parameters "saved-state record allocation shape". N_CONTROL_P now sits in that group but sizes no saved-state record: KL_nvm_backend takes no CONTROL count (:980-981). N_AUDIO_UNIT_P/N_CLK_DOM_P now also size the processor's dynamic-state rows (:1060-1061). The new parameter's own line (:238) is accurate.
Impact: an in-source reader may think N_CONTROL_P feeds the NVM record allocation. No functional effect.
Required change: optional — widen the group comment to name both consumers. The generated-header comment block (builder :2784-2787) cannot gain a line without breaking the frozen "only the CONTROL line changes" acceptance, so it should stay as is for this lane.
Verification: comment-only diff; elaboration statistics unchanged.
```

Observations, not findings against this PR:
- The configuration loader silently accepts unknown top-level and `entity.*` / `clocking.*` keys (probe V1-V6, V9). No such key can change the three counts, so #571's claim holds. Whether unknown keys should be refused is pre-existing schema behaviour outside this lane. The manager may triage it as separate work if wanted.
- Reviewer mutant R-a removes the IDENTIFY constructor entirely. It is rejected, but the rejection is a `StopIteration` in model generation before the new ROM-count arm runs. The new arm's discriminating power is shown by E-d instead.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #571 acceptance 1-3 and assignment scope vs `endstation_builder.py:2783-2790,5153-5159`, `aem_assemble.py:198-242`, `milan_datapath.sv:7426-7429`, `KL_pp_shadow.sv:237-239,1060-1062`; processor `integrator.md:68-70`, `KL_aecp_dyn_state.sv:164-198`; five-config build comparison `receipt-builds.txt` | R356-1 | f8a52f919bd309960046330a5af127b56731cb27 |
| RTL | CLEAN (one SUGGESTION, comment wording) | Both instance maps and parameter declarations; types `int`→`int unsigned`; single-instance census; `KL_pp_shadow` elaboration base vs head at AX 1x1 and 8x8 (`receipt-elab-columns.txt`, `raw/stats-*.txt`); liveness legs au2/ctl3/cd2; `-Wall` lint delta (`receipt-lint-delta.txt`); gitlinks unchanged | R356-1 | f8a52f919bd309960046330a5af127b56731cb27 |
| Robustness | CLEAN | Zero-count reachability, 12 hand-written configurations (`receipt-zero-reach.txt`); processor behaviour at 0 for each count (`receipt-elab-zero.txt`); gate `>= 1` assertion `check_entity_shape.py:395-402`; missing-census-key behaviour `endstation_builder.py:2790` | R356-1 | f8a52f919bd309960046330a5af127b56731cb27 |
| Tests | CLEAN | `check_entity_shape.py:171-176,372-402,558,575-576`; `entity_shape_selftest.py:598-649,664`; author self-test log (219/0) and plain gate (166/0) rerun; 32 reviewer-owned mutants incl. emitter and ROM-side (`receipt-gate-mutants.txt`); CI wiring `.github/workflows/docs.yml:449`; `test_declarations.py`, `check_nvm_capture.py` rc 0 | R356-1 | f8a52f919bd309960046330a5af127b56731cb27 |
| Docs | CLEAN (two SUGGESTIONs) | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49-70` against the code and processor pin; the builder comment `:2780-2783`; parent-wide search for other unbound-parameter inventories (none); docs gates rc 0 (`receipt-gates.txt`); PR/issue evidence sufficiency | R356-1 | f8a52f919bd309960046330a5af127b56731cb27 |

## Real limits

- **Assigned Verilator path was absent.** `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. The reviewer copied the byte-identical wrapper from `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` (sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, same content at `396-manager-r2`) into scratch and confirmed `Verilator 5.050 2026-07-01 rev v5.050` before use. The author's figures were produced with 5.052, and the reviewer's were produced independently with 5.050.
- **Elaboration scope.** Elaboration was `KL_pp_shadow` as top, `--lint-only --stats`. It was not the full `milan_datapath`. No Yosys run was made by the reviewer.
- **Builder and CI coverage.** The full builder bank (both compiler modes) was not re-run, as that is not allowed. The five-configuration builds used the builder CLI only, with the local environment's toolchain state.
- **Docs gate interpreter.** `gen_toc --check` and `check_em_dash` needed the existing docs virtual environment interpreter (`$VALIDATION_TOOLS/md-venv-40cdefe08ebd`), because the system interpreter lacks the pinned renderer. Nothing was installed.
- **Milan text.** The Milan v1.2 specification text is not in the repository. The §5.3.3 citation was checked against the repository's own clause map and the manager's accepted correction, not against the standard itself.
- **Hardware.** Physical calibration was NOT RUN. Field and hardware behaviour is not proven by any of this.
- **Hosted checks.** The snapshot at review time is in `receipt-hosted-snapshot.txt`: several hosted contexts were still in progress. `Physical gPTP` shows `skipped`, and a skip is not an executed job. The reviewer did not accept or rely on hosted results.
- **Clone state after probes.** HEAD, tree, index-tree, blob modes and gitlinks equal the exact head, and the worktree matches the index (`receipt-restore.txt`). Only git-ignored outputs were added by the gates (`__pycache__`, `sw/litex/platforms`, `tb/verilator/nvm_capture_cpu`).

## Pending manager duties

- Final current-dev candidate merge build and validation at the merge turn (source base `2a2a7bb6`; live dev was `2a2a7bb6` at assignment). #580 also edits `PP_DESCRIPTOR_OWNERSHIP.md` and moves the processor pin, so the candidate should re-run the shape gate, docs gates and the `u_pp` binding check against whichever lands second.
- Exact-head hosted and act acceptance, including `verilator-suites` / `yosys-portability` completion.
- The external review ([R357]) and the second positive required by CONTRIBUTING.
- Merge authorization and post-merge containment.

R356-1 FINISHED
