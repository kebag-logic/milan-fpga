[A554]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)
- [Round 1](#round-1)

## Status

**REVIEW READY** at `5428b044176f95248e6916dc00dd89c0df154078`; `682-pp-pin-2ad2f845` -> `dev`. Retained locally; not pushed.

At final committed head `5428b044176f95248e6916dc00dd89c0df154078`, all affected validation returned **rc 0**: **49/49 literal documentation steps under GNU Make 4.3**; the complete control-firmware campaign with native/release/debug RV32 checks and **196/196 mutants caught**; SDK, object and tally controls; combined coverage **PASS for 17 files** (100% after documented exclusions); the mailbox suite and verdict reader; builder elaboration with required RV32; six resource/capture checks; and four Markdown gates using the specified interpreter. Port and naming generators reproduce the committed records twice under GNU Make 4.3. All 54 private tracked inputs match the final commit byte for byte.

The uninterrupted full parent sweep completed at ancestor `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`: **60/60 suites, driver rc 0, tally rc 0, 2,184,926 counted checks, zero in-suite failures**. Its four explicit tsn-gen field/freshness skips remain in that original log. They are covered by the separate final-head full field rerun: **899 checks, zero failures, zero skips**, including 164 AAF checks, 677 gPTP checks, grader/traceability controls and both report-freshness checks. The changed mailbox suite also passes again at the final head. `round2-refresh-source-closure.json` proves that the remaining suite inputs are unchanged; the earlier sweep is not relabelled as a run at the later head.

Retained exact-input evidence at `591a5752` includes 58/58 Yosys units, two structural gates, three top elaborations and their controls; BDD 14 features / 404 scenarios / 1,968 steps; native NVM **435 tests across five shapes and 109/109 mutants caught**; and vendor syntax **zero findings across 81 parent and 52 pinned-processor sources**, rc 0. The two integration audits bind retained processor, gPTP, physical-cadence, NVM quick/lint, LiteX, render and image results to unchanged final inputs. All three resource input digests and the capture source digest still match exactly. The selected bitstream and manifest pass the complete offline image preflight, and all 185 retained image/resource artifacts still match their recorded hashes (`round2-artifact-retention.json`).

The host builder's two documented NOTRUN arms remain outside its verdict: the ineffective MAKEFLAGS mutation under Make 4.3 and the absent historical calibration report. The earlier 59/60 sweep and its unresolved lifecycle cause remain disclosed as historical failed evidence; the accepted complete repeat passed. The render exception is exactly **"unchanged from dev; #657"**, supported by the manager ruling and completed differential. Hardware acceptance 5, publication, hosted checks and independent reviews remain pending; no push or hardware action was performed.

The render differential passed under the manager ruling. All three routes pass timing, and the selected ExtraPostPlacementOpt route has an accepted bitstream and bound manifest. Earlier failed results remain in HANDOFF.md and are not counted as passing final evidence. This is author evidence; independent reviews and hosted checks remain pending.

## Linked Issue / roles

Closes #682
Closes Mister-M-alt/protocol-processor-control-plane-avb-milan#22
Relates to #608
Relates to #658

Executor: `[A554]`
Internal cleared-context reviewer: `[R520]`
External reviewer: `[R521]`

## Description

Adopts processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` from `ead8036035affd53ef4b29979190f2f4f67084c0`, covering PRs 156, 159, 160, 161, 162 and 164. Only its gitlink changes; the processor top-level interface is byte-identical between pins. HANDOFF.md maps every parent-visible item and patch hunk.

The supplied notification patch lets the harness finish a frame already in progress for at most 2,048 cycles beyond the observation window. The second patch removes two fixed declaration-order findings from the processor syntax budget. Pin-derived ROM, submodule, boundary-diagram and port-contract records are regenerated; naming remains identical. The resource flow has an opt-in synthesis worker cap with unchanged default output and passing controls.

Dev `79b086d44eb62d007d38e18f5618b98e8e2a33e6` was merged with `--no-ff` and its changed resource inputs remeasured as combination F. A later `--no-ff` merge takes dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`; the next commit refreshes the generated parent port census to 2,079, with unchanged ratchets. Final input checks retain the same resource, capture, image and render dependencies. Changed mailbox and firmware consumers receive fresh validation.

The final authorized `--no-ff` merge takes dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` as `5428b044176f95248e6916dc00dd89c0df154078`. It is conflict-free and exactly matches an independent merge-tree calculation. `round2-refresh-merge.json` records the merge; `round2-refresh-source-closure.json` names its 24 changed paths and eleven unchanged dependency scopes. These are imported MAAP control-firmware changes, their documentation, and the mailbox build recipe. No processor source or parent/processor interface was changed by this lane.

The completed 60-suite sweep remains evidence at its actual head `591a5752`; the changed mailbox suite, complete control-firmware campaign, combined coverage, builder and documentation gates passed fresh runs at the final merge head. Resource and capture provenance passed again there. The field campaigns passed a separate complete rerun with 899 checks and no skips after their external tsn-gen directory disappeared during the sweep. The old Make/SDK temporary prefixes and the cited Make recipe later disappeared as well: `round2-tool-prefix-recovery.json` records a real GNU Make 4.3 source build and the repository-verified pinned SDK under this lane's scratch directory. No documentation gate ran with the fallback Make 4.4.1; that version appears only on the Python-only record-repeatability receipt before restoration, followed by another identical repeated generation under the restored GNU Make 4.3.

Combination F: 49,957 LUTs, 54,274 FFs, 15,734 slices, 87.5 BRAM tiles and 14 DSPs. Standalone 1x1 and 8x8 figures match combination E. All three synthesis logs report zero processor Synth 8-6901 warnings across 46 directly read sources; each retains one known parent warning. Policies are unchanged. Capture checking passes with unchanged firmware source digest; the retained 8x8 maximum is 13.86484 ms against 24.5 ms.

Acceptance 4 render result: **"unchanged from dev; #657"**, under the [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028334443). Both complete campaigns report 28/32, all 32 leg outcomes match, and the four failed cases have identical assertions and counts. Both actual clean-epoch outputs are 3,746 bytes with SHA-256 `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b`. `round2-render-differential.json` contains the proof and fresh-build corroboration; `round2-final-merge-closure.json` proves that the final merge did not change its dependency set. The adopted tree was restored exactly.

| Directive | Minimum WNS, ns | Minimum WHS, ns |
|---|---:|---:|
| ExtraPostPlacementOpt, selected | +0.124 | +0.031 |
| AltSpreadLogic_high | +0.090 | +0.011 |
| ExtraTimingOpt | +0.055 | +0.020 |

All corners meet WNS >= +0.03 ns and WHS >= 0. The selected bitstream is 3,825,992 bytes, SHA-256 `613a670a15dc7dce29c9cce0a1fc75527229575f7b43968dce6a444ffc80a8bc`. Its manifest regenerates byte-identically, binds that bitstream and the 7,512-byte AEM, and passes complete offline target-image preflight. The evidence includes all four slack metrics, worst paths, clock interactions, CDC and unconstrained-path reports. `round2-complete-image-evidence.json` records the artifact bindings. Only the selected route is claimed as a complete image.

## Authoritative references

- [Issue 682 assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147) and [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028334443).
- Processor PRs [156](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156), [159](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/159), [160](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160), [161](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/161), [162](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162) and [164](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164): their parent-visible lists define the adopted changes.
- [Issue 638](https://github.com/kebag-logic/milan-fpga/issues/638), `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: resource inputs, recording and re-baseline rule.
- [Issue 661](https://github.com/kebag-logic/milan-fpga/issues/661) and [PR 663](https://github.com/kebag-logic/milan-fpga/pull/663): adoption method.
- `REQUIREMENTS.md`, `CONTRIBUTING.md`, `docs/development/CODE_QUALITY.md`, `docs/reference/SUBMODULES.md`, and `docs/integration/BUILDING.md` section 5.

## How to get into the same state

Use the local candidate and initialized submodules. Before any command within the processor, verify its physical top-level directory.

```sh
cd $LANES/682-pp-pin3
git remote get-url origin
git rev-parse HEAD
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
git -C protocol-processor rev-parse HEAD
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export PYTHON_CPU_COUNT=4
export MILAN_RV32_CC=$VALIDATION_STORAGE/682-a554/round2/tool-prefixes/rv32-sdk/bin/riscv32-linux-gcc
export TSN_GEN_ROOT=$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen
export PYTHONHASHSEED=0
export PATH=$VALIDATION_STORAGE/682-a554/round2/tool-prefixes/make43/bin:$PATH
make --version
"$VERILATOR" --version
```

Expected origin: `https://github.com/kebag-logic/milan-fpga.git`; parent head `5428b044176f95248e6916dc00dd89c0df154078`; processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`; GNU Make 4.3; Verilator 5.050. Markdown gates use `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Environment and external dependency digests are retained in the packet.

## How to validate

`ROUND2-GATE-COMMANDS.md`, `round2-gate-table.md` and `round2-gate-receipts.json` contain every executed gate command, physical working directory, head, Make version, raw return code, log size and SHA-256. The 49 hosted documentation steps are reproduced literally under GNU Make 4.3. Final-head reruns are distinguished from evidence retained for unchanged inputs.

```sh
python3 scripts/check_nvm_capture.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
bash scripts/run_all_suites.sh $VALIDATION_STORAGE/682-a554/round2/final/parent-suite-logs
python3 scripts/suite_tally.py $VALIDATION_STORAGE/682-a554/round2/final/parent-suite-logs --quiet --expect-suite-root tb/verilator
make -C tb/verilator/milan_dp_render tdm8render-mutants
```

Ordinary gates require rc 0 and the uninterrupted full sweep requires 60/60. Under the manager ruling, each full render campaign reports 28/32 (raw make rc 2), while the differential verifier must return zero. The comparison changes only the gitlink and reverses both patches at the same parent tree, then restores the candidate exactly. Assertions, counts and actual clean-epoch bytes must match; any difference is a STOP.

The selected route must meet the section-5 timing thresholds at every corner and retain an unquarantined bitstream, bound manifest, required reports and successful complete-image preflight. It passes these checks. No hardware setup or flashing is part of the offline preflight.

## Known limitations / out of scope

- The complete sweep at `591a5752` records four field-campaign/freshness skips after the external tsn-gen directory disappeared. The pinned source and recursive dependencies were restored as verified exports; `round2-field-oracle-recovery.json` records the separate full field rerun. Skips remain disclosed in the original log.
- The original round-2 sweep completed 59/60 with a gPTP-shadow nested-cancellation cleanup failure; its cause remains unknown. The failed result and both focused diagnostics are retained. No test expectation was changed. The final full sweep is separate evidence.
- The initial NVM quick result shared scenario outputs with the original sweep and is qualified; the accepted replacement isolates both build and scenario outputs. The final sweep has no concurrent quick campaign. Startup-only render and lock-waiter errors remain recorded separately.
- To bound temporary-storage memory, 6.14 GB of completed NVM mutation ELF artifacts were moved to disk with verified byte-identical links. Active cases, source files, expectations and logs were unchanged; `round2-final-nvm-storage.json` records the operation. After the NVM campaign passed, every copied hash was rechecked and the temporary copies were removed. No campaign was interrupted.
- The host builder retains two NOTRUN arms: the ineffective MAKEFLAGS mutation under Make 4.3 and the absent historical calibration report. Environment-restricted workflow controls retain their own explicit dispositions.
- Positive timing does not clear missing I/O-delay coverage or CDC diagnostics: the selected image retains 46 no-input-delay and 87 no-output-delay entries and ten CDC-10 critical diagnostics. The selected implementation emits no CRITICAL WARNING or rejected-constraint diagnostic. Alternative route logs retain their pre-final Route 35-39 warnings.
- Processor 148 retains the disclosed MAC-stall limitation after grant. The separate 60% LUT area objective remains unmet.
- Acceptance 5 remains the manager's post-merge #608 withdrawal cycles, #658 default-map check and stream/counter soak. No hardware work is performed in this lane.
- Publication, protected hosted checks, independent review coverage, candidate-merge validation and post-merge containment remain pending.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 1

Head `1e99ad217f0747c33e03238f7d1c633c07ce572c` stopped at the full render campaign's 28/32 result, before the manager's exception existed. Fresh builds reproduced all four failed cases. The parent sweep was cancelled after 10/60; rc 143 was explicitly not a completed gate result. The remaining parent bank and complete-image work were not run.

Round 1 passed all 49 documentation workflow steps under Make 4.3, the 33-suite processor sweep with 1,028,250 checks, gPTP, BDD, the focused 421-check notification target, the resource/capture gates and corrected fresh synthesis evidence. Its resource combination E and three route-only results are historical: default +0.101/+0.031 ns, AltSpreadLogic_high -0.857/+0.008 ns, ExtraTimingOpt +0.334/+0.021 ns. None was claimed as a complete image.

The original description is retained as `ROUND1-PR-BODY.md`; full evidence remains in HANDOFF.md's Round 1 section and the original gate/evidence files. [Public round-1 STOP](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028310880). Round-2 evidence supersedes its current-state claims.
