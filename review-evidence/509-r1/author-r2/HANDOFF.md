[A333] Round 2 handoff

Candidate: `04c9802d852befba3b5d854ba5f3faf3ddfc59a7`. Branch: `509-pp-descriptor-ownership`.
Starting head: `20423082f221a02f3de72952cec4e1ac0c839b1d`.
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.

Items 1-5 complete; all 30 recorded foreground gate invocations returned 0. No push, PR edit or merge performed.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/509#issuecomment-5845357621
Internal report: https://github.com/kebag-logic/milan-fpga/pull/568#issuecomment-5845348382
External report: https://github.com/kebag-logic/milan-fpga/pull/568#issuecomment-5845356060

## Change list

| File:line | Assignment and change |
|---|---|
| scripts/audit_pp_descriptors.py:319 | Item 1 / R330 M1: reload the configuration with both generator bindings patched, so model identity can change. |
| scripts/audit_pp_descriptors.py:343 | Item 1: every audit runs a simulated identity-coverage repair and refuses unchanged packed identity. |
| scripts/audit_pp_descriptors.py:35 | Item 4 / R331 S1: explicit AuditError refusals replace integrity assertions in decoder, builder comparison and packed-byte survival. These errors cannot be mislabeled as ordinary model refusals. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59 | Item 2 / R330 M2: L2 points body/key consistency to new F7, preserving PP60 acceptance. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:242 | Item 2: F7 requires a legal pair and independent mismatched-type and mismatched-index refusals. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:64 | Item 3 / R330 M3: L7 distinguishes enforced map bounds from recorded stream-channel width deviations. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:139 | Item 3: explicitly identifies the shipping arty_current image and its six deviations. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:243 | Item 3: new F8 owns the clause-backed static-map policy, matching validation and shipping model change; #464 stays closed. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:63 | Item 5 / R331 S2: complete L6 source/domain/identity-list/gPTP sub-rules and current reachability or failure dispositions. |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:210 | Describes re-derived identity, the discriminating control and optimization-safe integrity checks. |

No production builder, configuration, RTL, processor source or gitlink changed.
Other suggestions remain with #495 per the assignment.

## Reviewer probes and mutants

Public evidence source: `509-review-evidence` at `db0303e5fe715ca4dc8b4728762f426f081b85bc`, under `review-evidence/509-r1/reviews/`.
Fetched into a disposable bare repository under temporary storage; no evidence checkout was created.
Reviewer scripts were read from their public blobs. Their SHA-256 values are recorded in `reviewer-script-hashes.json`.

R330 scripts ran unchanged. R331 checker and embedded mutation bodies ran unchanged.
The R331 reproduction wrapper hardcodes the previous head and creates/restores checkouts. That wrapper was not executed because this assignment prohibits other checkouts. Its probe commands and mutation bodies were applied to disposable exports of this candidate and the pinned submodules instead. The changed expected result is M3 under optimization: it now refuses.

| Probe or mutant | Observed exit / verdict | Receipt |
|---|---|
| Pristine audit, normal and optimized | 0; five images and all original measurements identical; SHA-256 `8233f515e8e469570314fdfea9437db5d082a6441f04a75ff840efe5444f4779` | audit.json; audit-optimized.json |
| Fresh candidate export, without creating a checkout | 0; byte-identical pristine receipt | audit-export.json |
| R330 M1, normalize last body byte | 1; audit refuses altered packed bytes | r330-mutations.log |
| R330 M2, rates-offset refusal | 0; only offset 143 changes accepted -> refused | r330-mutations.log |
| R330 M3, include IDENTIFY in model_shape | 0; identity changes `0x001BC5F531E6A9DA` -> `0x001BC572445BE3EA` | r330-mutations.log; r330-m3-audit.json |
| R330 fresh-process CLI identity control | 0; all five image hashes match; pristine reset_time edit changes only byte 6741 with unchanged ID | r330-cli.json; r330-cli.log |
| R330 M3 fresh-process CLI | 0; same changed IDs as the repaired audit; changed offsets 303-307 and 6741 | r330-m3-fresh.json; r330-m3-fresh.log |
| R330 accepted-YAML reach probes | 0; buffer, CRF word, format count/family, CRF-only source and invalid IDs reach packed bytes | r330-probe-reach.log |
| R330 relocated YAML control | 0; all 32 rows equal tracked arty_current | loader-controls.json |
| R331 page/receipt checker | 0; zero mismatches | r331-page-receipt.log |
| R331 checker negative control | 1; planted image-size mismatch detected | r331-page-negative.log |
| R331 M1, L6/L10 semantic checks | 0; reversed list, ninth word, offset 143, count/extent mismatch and truncated word all flip to refused; eight-word control stays accepted | r331-mutations.json; r331-M1.json |
| R331 M2, raise loader bound to 9 | 0; ninth-rate loader becomes accepted; conversion still refuses unsupported rates | r331-mutations.json; r331-M2.json |
| R331 M3, normalize invalid model ID | 1; packed-byte integrity refusal | r331-M3.log |
| R331 M3 with -O | 1; same refusal with optimization | r331-M3-O.log |
| R331 missing gPTP authority | 1; named authority refusal | missing-gptp.log |
| R331 empty clock-source list | IndexError; no image produced; existing behavior retained | loader-controls.json |

The exit-1 rows are expected mutant or negative-control results, not failed gates.
The published R330 M3 summary looks up `changed_offsets`; the audit field is `changed_image_offsets`. Its null summary field is retained unchanged. The fresh-process receipt and underlying audit record establish the actual changed offsets.

## Added integrity controls

Run `python3 -B audit-controls.py "$CANDIDATE"` and repeat with `-O`.
Both control runners exit 0. Every case below is checked with explicit exceptions.

| Probe | Normal | Optimized |
|---|---|---|
| legal image and identity control | accepted | accepted |
| bad magic | refused | refused |
| bad version | refused | refused |
| wrong image length | refused | refused |
| bad header checksum | refused | refused |
| body type mismatch | refused | refused |
| body index mismatch | refused | refused |
| descriptor outside image | refused | refused |
| builder image disagreement | refused | refused |
| packer normalizes body bytes | refused | refused |
| identity derivation ignores changed field | refused | refused |

Receipts: `audit-controls-normal.json`, `audit-controls-optimized.json`.

## Individual audit verdicts

These are measured acceptances/refusals, not product-conformance passes.

| Layer | Probe | Verdict |
|---|---|---|
| Processor packer | pristine shipping document | accepted |
| Processor packer | output port shares input cluster block | accepted |
| Processor packer | metadata index gap | refused |
| Processor packer | duplicate row | refused |
| Processor packer | ENTITY name differs from name table | refused |
| Processor packer | wire index differs from metadata | accepted |
| Processor packer | wire type differs from metadata | accepted |
| Processor packer | buffer at 2126000 ns | accepted |
| Processor packer | buffer one ns below floor | accepted |
| Processor packer | CLASS_A cleared | accepted |
| Processor packer | current format outside list | accepted |
| Processor packer | mixed AAF and CRF formats | accepted |
| Processor packer | 47 formats at Table 7-8 cap | accepted |
| Processor packer | 48 formats below line-buffer cap | accepted |
| Processor packer | source list reversed | accepted |
| Processor packer | input port declares a static map | accepted |
| Processor packer | cluster channel_count two | accepted |
| Processor packer | duplicate output stream channel | accepted |
| Processor packer | CONTROL is not IDENTIFY | accepted |
| Processor packer | zero model ID | accepted |
| Processor packer | all-ones model ID | accepted |
| Processor packer | eight full rate words | accepted |
| Processor packer | nine full rate words | accepted |
| Processor packer | offset 143 | accepted |
| Processor packer | count disagrees with extent | accepted |
| Processor packer | one byte short | accepted |
| Processor packer | ENTITY talker count disagrees | accepted |
| Processor packer | ENTITY listener count disagrees | accepted |
| Processor packer | opaque 576-byte row | accepted |
| Processor packer | opaque 577-byte row | refused |
| Parent YAML | unchanged YAML | loader accepted; image accepted |
| Parent YAML | empty listener list | loader refused |
| Parent YAML | buffer one ns below floor | loader accepted; image accepted |
| Parent YAML | non-Milan CRF word | loader accepted; image accepted |
| Parent YAML | 48 AAF output formats | loader accepted; image accepted |
| Parent YAML | mixed output format families | loader accepted; image accepted |
| Parent YAML | outputs without INTERNAL | loader accepted; image accepted |
| Parent YAML | static input map | loader refused |
| Parent YAML | zero model ID pin | loader accepted; image accepted |
| Parent YAML | all-ones model ID pin | loader accepted; image accepted |
| Parent YAML | eight distinct rates | loader accepted; image refused |
| Parent YAML | nine distinct rates | loader refused |
| Parent YAML | duplicate rates | loader refused |
| Parent map | legal output fanout | accepted |
| Parent map | duplicate output stream channel | refused |

## Gates

All gate commands run in the foreground without pipelines, with a 7200-second timeout per command. `run-gate.py` preserves exit statuses in `gates.jsonl` and full logs beside this handoff.

The full builder runs through `builder-mode.py`. SDK mode verifies the read-only pinned installation, redirects the selected native compiler to it, and requires the RV32 instruments. Absent mode hides the three cross-compiler candidates and retains the normal host-compiler stand-down behavior. `compiler-sdk.jsonl` and `compiler-absent.jsonl` record every intercepted compiler invocation.

The Markdown interpreter uses the repository hash-pinned requirements in temporary storage outside this output directory. `GIT_DIR=/dev/null` selects the filesystem CI mode without removing metadata.

| Command / mode | Exit | Evidence |
|---|---|---|
| `python3 $RECEIPTS/builder-mode.py sdk --audit $RECEIPTS/compiler-sdk.jsonl` | 0 | builder-sdk.log; 774.72 s |
| `python3 $RECEIPTS/builder-mode.py absent --audit $RECEIPTS/compiler-absent.jsonl` | 0 | builder-absent.log; 561.97 s |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | nvm-firmware.log; 38.84 s |
| `python3 scripts/check_nvm_capture.py` | 0 | nvm-capture.log; 0.72 s |
| `python3 scripts/check_baremetal_only.py --check` | 0 | baremetal.log; 14.74 s |
| `python3 -B scripts/docs_check.py` | 0 | docs-git.log; 4.17 s |
| `GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | docs-no-git.log; 4.17 s |
| `python3 scripts/ci_events.py --check` | 0 | ci-check.log; 0.21 s |
| `python3 scripts/ci_events.py --selftest` | 0 | ci-selftest.log; 14.59 s |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | em-dash.log; 3.02 s |
| `python3 scripts/check_doc_style.py` | 0 | doc-style.log; 0.06 s |
| `python3 scripts/gen_toc.py --check` | 0 | toc.log; 2.47 s |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | anchors.log; 1.62 s |
| `python3 scripts/check_doc_paths.py` | 0 | doc-paths.log; 0.06 s |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | module-matrix.log; 0.97 s |
| `python3 scripts/xvlog_gate.py --check` | 0 | xvlog.log; 138.84 s |
| `python3 scripts/check_rtl_source_lists.py` | 0 | rtl-lists.log; 1.42 s |
| `python3 scripts/check_sv_idiom.py` | 0 | sv-idiom.log; 0.46 s |
| `python3 scripts/lint_rtl.py --check` | 0 | rtl-lint.log; 6.96 s |
| `python3 scripts/check_cpp_idiom.py` | 0 | cpp-idiom.log; 1.22 s |
| `python3 scripts/check_py_idiom.py` | 0 | py-idiom.log; 3.37 s |
| `python3 scripts/check_port_contracts.py` | 0 | ports.log; 2.32 s |
| `python3 scripts/measure_naming.py --check` | 0 | naming.log; 0.46 s |
| `python3 scripts/measure_test_evidence.py --check` | 0 | test-evidence.log; 5.72 s |
| `cd tests && behave --no-capture -f plain` | 0 | behave.log; 1.17 s |
| `git diff --check` | 0 | diff.log; 0.03 s |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | diff-base.log; 0.02 s |
| `python3 avdecc/gen_aem_store.py --self-test` | 0 | aem-selftest.log; 0.11 s |
| `python3 scripts/check_entity_shape.py --self-test` | 0 | entity-shape.log; 40.92 s |
| `python3 scripts/audit_pp_descriptors.py --output $RECEIPTS/descriptor-audit.json` | 0 | audit.log; 0.46 s |

### Evidence limits

- SDK builder: one arm not run, resource calibration without the placement report. All RV32 instruments ran; 856 compiler invocations are recorded.
- Compiler-absent builder: two arms not run, compiler-dependent census/resolution/preprocessor/include instruments and resource calibration. The existing stand-down behavior is explicit in the log.
- Documentation filesystem mode: zero findings; inventory parity is the expected Git-dependent skip. Git mode: zero findings.
- Behavior: 14 features, 344 scenarios, 1739 steps pass; none failed or skipped.
- Entity-shape self-test: 136 checks, zero failures.
- Generator self-test passes all 20 checks and still reports the same six static-map deviations. F8 owns the remaining shipping-policy disposition.
- Parser gate: zero parent findings; four existing processor findings equal its ratchet. RTL lint: 90 existing findings equal its ratchet, with 17 waivers. No budget or waiver changed.
- No hardware, physical calibration, multi-configuration proof, hosted exact-head result or merge result is claimed.

## Processor follow-up and review boundary

Exact proposed separate processor wording is in [processor-wording.md](processor-wording.md). It preserves the original proposed contract and routes the body/key gap to F7, separately from PP60.

The maintainer files F1-F8 from the reference page. F7 owns generic body/key consistency; F8 owns the shipping static-map policy. Existing #478/#464 acceptance remains unchanged and closed. Other review suggestions go to #495.

The round-2 assignment retains R331-1 as the ancestor external positive and requests an internal delta review. This handoff is author evidence, not a reviewer-owned clean-lens ledger or merge approval.
Publication, exact-head hosted/local workflow evidence, candidate-merge validation, merge authorization, containment and board state remain with the maintainer.

Temporary review artifacts, exports and the temporary interpreter are deleted after validation; no toolchain or tree export is kept in this output directory. No hardware run or multi-configuration proof is claimed.

## Final state

Head: `04c9802d852befba3b5d854ba5f3faf3ddfc59a7`. The worktree is clean and all four gitlinks are unchanged. The commit has a one-line subject, no body and no trailers.

`REVIEW-READY.md` contains the issue comment submitted as the final action. Internal delta review and maintainer publication remain pending. No push, PR edit or merge was performed.
