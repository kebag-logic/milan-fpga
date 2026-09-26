[A339] Round 3 handoff

Issue: [#231](https://github.com/kebag-logic/milan-fpga/issues/231).
PR: [#572](https://github.com/kebag-logic/milan-fpga/pull/572).
Assignment: [items 1-2](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5847401184).
Reviews: [R332-3](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5847397455), [R333-2](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5846837830).

Branch: `231-pp-shadow-baseline`.
Starting head: `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4`.
Completed head: `3a1477c528bdf71b7cecadf86383b7579c9197d6`.
Commit subject: `test: cover baseline export geometry and ambiguity refusals`.
Verified origin: `https://github.com/kebag-logic/milan-fpga.git`.

## Changes

| File:line | Change |
|---|---|
| `syn/ooc/pp_baseline.py:241` | Require the intended exception and diagnostic for each new negative case. Unrelated failures do not satisfy a refusal. |
| `syn/ooc/pp_baseline.py:298` | Exercise duplicate/empty parameter blocks, undeclared parameters and missing/duplicate template markers. |
| `syn/ooc/pp_baseline.py:314` | Exercise 40 inventory refusals through real preparation: missing/duplicate image bindings and geometry packages for all three ROM families; missing/duplicate depth and width declarations; generated ROM short/long and narrow/wide inputs; parameter ROM short and narrow/wide inputs. Restore each fixture and pass a clean inventory afterward. |
| `syn/ooc/pp_baseline.py:380` | Exercise integrated-directory, attribution-endpoint, missing/duplicate synthesis command and invalid pathname refusals. Pass a valid string-path control. Check both CLI endpoint exclusions. |
| `syn/ooc/pp_baseline.py:421` | Connect the new export tests and require zero-threshold hierarchy reporting in all three default emitted scripts. Retain attribution and output-containment controls. |
| `syn/ooc/pp_baseline_mutants.py:23` | Add generated and parameter ROM geometry mutants. |
| `syn/ooc/pp_baseline_mutants.py:32` | Add combined and independent image/package ambiguity guards, geometry-declaration uniqueness and address-depth conversion mutants. |
| `syn/ooc/pp_baseline_mutants.py:59` | Maintain the additional parameter, endpoint, pathname, template and report mutations exercised by the public probes. |

Assignment item 1 is met by the named synthetic export refusals.
Item 2 is met by 28 maintained kills and 32 public-probe kills.
All three pristine controls pass.
The refusal claims were not narrowed.
Production functions and constants compare identically with the starting head.
The committed delta contains only these two test-bearing Python files.
No baseline measurement, page, RTL or gitlink changed.

## Public probe provenance

Read-only evidence revision: `1202ce2f09f92729d4cc1fda4d05284a3d8a5cc0` on `231-review-evidence`.
The evidence was fetched into a temporary bare repository, without another checkout.
Both scripts and their original receipts were read there.
Script bytes were compared with their fetched blobs before and after execution.
The scratch repository, scripts, original receipts and validation environment were deleted afterward.
`$SCRATCH` below denotes that disposable directory.

| Reviewer | Public script | SHA-256 |
|---|---|---|
| R332-3 | [review-evidence/231-r1/reviews/R332-3/scripts/extra_mutants.py](https://github.com/kebag-logic/milan-fpga/blob/1202ce2f09f92729d4cc1fda4d05284a3d8a5cc0/review-evidence/231-r1/reviews/R332-3/scripts/extra_mutants.py) | `7a12dd2a7c385af0670429b17530ba248d82e0b2bc3057cc6341aaef3934735a` |
| R333-2 | [review-evidence/231-r1/reviews/R333-2/probe_selftest/mutate2.py](https://github.com/kebag-logic/milan-fpga/blob/1202ce2f09f92729d4cc1fda4d05284a3d8a5cc0/review-evidence/231-r1/reviews/R333-2/probe_selftest/mutate2.py) | `7846af5f35340876e31ab9c4e956d2db090d7592e4a4c551ca032ba680efeb79` |

## Mutant verdicts

All entries ran against `3a1477c528bdf71b7cecadf86383b7579c9197d6`.
Maintained: 28 killed; R332-3: 15 killed; R333-2: 17 killed.
There are no survivors, unapplied mutations or failing controls.
The unchanged R333-2 script reports nonzero exits without printing their numeric value.
Original command output is retained in the linked gate receipts.

| Suite | Case | Verdict |
|---|---|---|
| Maintained | `control` | CONTROL PASS |
| Maintained | `ROM error promotion` | KILLED (rc 1) |
| Maintained | `readmemh inventory equality` | KILLED (rc 1) |
| Maintained | `empty SRAM requirement` | KILLED (rc 1) |
| Maintained | `parameter ROM depth` | KILLED (rc 1) |
| Maintained | `generated ROM depth` | KILLED (rc 1) |
| Maintained | `generated ROM width` | KILLED (rc 1) |
| Maintained | `parameter ROM width` | KILLED (rc 1) |
| Maintained | `image and geometry ambiguity` | KILLED (rc 1) |
| Maintained | `image binding uniqueness` | KILLED (rc 1) |
| Maintained | `geometry package uniqueness` | KILLED (rc 1) |
| Maintained | `geometry declaration uniqueness` | KILLED (rc 1) |
| Maintained | `microcode address depth` | KILLED (rc 1) |
| Maintained | `outside repository guard` | KILLED (rc 1) |
| Maintained | `image depth` | KILLED (rc 1) |
| Maintained | `image width` | KILLED (rc 1) |
| Maintained | `hexadecimal image words` | KILLED (rc 1) |
| Maintained | `attribution constraint loading` | KILLED (rc 1) |
| Maintained | `attribution boundary preservation` | KILLED (rc 1) |
| Maintained | `wrapper declaration equality` | KILLED (rc 1) |
| Maintained | `empty parameter block` | KILLED (rc 1) |
| Maintained | `duplicate parameter` | KILLED (rc 1) |
| Maintained | `integrated output directory` | KILLED (rc 1) |
| Maintained | `attribution integrated endpoint` | KILLED (rc 1) |
| Maintained | `CLI integrated endpoint` | KILLED (rc 1) |
| Maintained | `single synthesis command` | KILLED (rc 1) |
| Maintained | `image pathname characters` | KILLED (rc 1) |
| Maintained | `template marker uniqueness` | KILLED (rc 1) |
| Maintained | `unfiltered hierarchy report` | KILLED (rc 1) |
| R332-3 | `control` | CONTROL PASS |
| R332-3 | `inventory image/geometry ambiguity guard` | KILLED (rc 1) |
| R332-3 | `package geometry declaration uniqueness` | KILLED (rc 1) |
| R332-3 | `microcode depth 1<<UPC_W_C` | KILLED (rc 1) |
| R332-3 | `wrapper declaration equality` | KILLED (rc 1) |
| R332-3 | `empty parameter block` | KILLED (rc 1) |
| R332-3 | `integrated output directory guard` | KILLED (rc 1) |
| R332-3 | `attribution requires integrated build` | KILLED (rc 1) |
| R332-3 | `CLI integrated-endpoint exclusivity` | KILLED (rc 1) |
| R332-3 | `single synth_design command` | KILLED (rc 1) |
| R332-3 | `image pathname character guard` | KILLED (rc 1) |
| R332-3 | `split_once uniqueness` | KILLED (rc 1) |
| R332-3 | `ROM_ERROR severity text` | KILLED (rc 1) |
| R332-3 | `ROM_ERROR placed after synthesis` | KILLED (rc 1) |
| R332-3 | `KEEP_HIERARCHY on wrong cell` | KILLED (rc 1) |
| R332-3 | `hexadecimal-only ROM check scoped to non-empty` | KILLED (rc 1) |
| R333-2 | `pristine` | CONTROL PASS |
| R333-2 | `R1-drop_rom_error_promotion` | KILLED (nonzero) |
| R333-2 | `R1-drop_readmemh_set_check` | KILLED (nonzero) |
| R333-2 | `R1-skip_param_rom_geometry` | KILLED (nonzero) |
| R333-2 | `R1-drop_output_outside_repo_check` | KILLED (nonzero) |
| R333-2 | `R1-control_width_check_removed` | KILLED (nonzero) |
| R333-2 | `R2-generated_rom_depth_dropped` | KILLED (nonzero) |
| R333-2 | `R2-generated_rom_width_dropped` | KILLED (nonzero) |
| R333-2 | `R2-param_rom_width_dropped` | KILLED (nonzero) |
| R333-2 | `R2-param_rom_ambiguity_refusal_dropped` | KILLED (nonzero) |
| R333-2 | `R2-package_declaration_ambiguity_dropped` | KILLED (nonzero) |
| R333-2 | `R2-integrated_directory_guard_dropped` | KILLED (nonzero) |
| R333-2 | `R2-attribution_requires_integrated_dropped` | KILLED (nonzero) |
| R333-2 | `R2-cli_attribution_endpoint_guard_dropped` | KILLED (nonzero) |
| R333-2 | `R2-unfiltered_hierarchy_report_dropped` | KILLED (nonzero) |
| R333-2 | `R2-wrapper_parameter_set_equality_dropped` | KILLED (nonzero) |
| R333-2 | `R2-duplicate_parameter_refusal_dropped` | KILLED (nonzero) |
| R333-2 | `R2-ooc_single_synth_command_dropped` | KILLED (nonzero) |

## Gates

Every command ran in the foreground, without a pipeline.
Each subprocess had a 1,800-second deadline.
Gate dependencies used the hash-locked `tools/markdown/requirements.txt` in a disposable environment.
The validation interpreter's directory was prepended to `PATH`.

The no-Git run used an absent `GIT_DIR` in the same worktree.
This selects the CI filesystem inventory without removing repository metadata.
Both modes scanned 168 Markdown files and 894 text files with zero findings.
Git mode passed 23/23 scrub controls; filesystem mode passed 22/22.
Filesystem mode skipped only inventory parity, which requires Git metadata.
Both modes passed 4/4 routing controls.

| Gate command | rc | Receipt |
|---|---:|---|
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 | [selftest.log](selftest.log) |
| `python3 syn/ooc/pp_baseline_mutants.py` | 0 | [maintained-mutants.log](maintained-mutants.log) |
| `python3 "$SCRATCH/R332-3/scripts/extra_mutants.py" syn/ooc/pp_baseline.py` | 0 | [R332-3-mutants.log](R332-3-mutants.log) |
| `python3 "$SCRATCH/R333-2/probe_selftest/mutate2.py" syn/ooc/pp_baseline.py "$SCRATCH/final-mutants"` | 0 | [R333-2-mutants.log](R333-2-mutants.log) |
| `python3 -B scripts/docs_check.py` | 0 | [docs-git.log](docs-git.log) |
| `GIT_DIR="$SCRATCH/absent-git" python3 -B scripts/docs_check.py` | 0 | [docs-no-git.log](docs-no-git.log) |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc.log](toc.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | [anchors.log](anchors.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths.log](doc-paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [py-idiom.log](py-idiom.log) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | [test-evidence.log](test-evidence.log) |
| `git diff --check` | 0 | [diff-check.log](diff-check.log) |
| `git diff --check 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 HEAD` | 0 | [committed-diff-check.log](committed-diff-check.log) |

Machine-readable command records: [gate-results.json](gate-results.json).
Probe hashes: [probe-provenance.json](probe-provenance.json).
Prepared full PR body: [PR-BODY.md](PR-BODY.md).

## Handoff state

The commit is local and unpushed; the working tree is clean.
The full current PR body was fetched with `gh pr view 572 --json body`, updated locally, and retained in PR-BODY.md.
The prepared body starts with `[A339]`, includes Round 3, and retains `Closes #231`.
The stale Round 2 publication sentence was removed.
No PR edit, push, merge, synthesis or hardware run was performed.
The required review-ready comment is the final publication action for this assignment.
Independent re-review, publication and final-head acceptance remain pending.
