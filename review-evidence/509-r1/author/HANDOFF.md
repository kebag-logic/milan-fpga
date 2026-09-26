# Issue #509 author handoff

Role: [A327], author. Status: audit and documentation complete; all requested local commands returned 0; ready for independent review.

Branch: `509-pp-descriptor-ownership`.
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Remote confirmed: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/509#issuecomment-5844867005

Pinned processors are unchanged: protocol processor
`990f96526bb89356c963a260ebbdcf2a77e6623a`; gPTP processor
`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The axis pin is
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unrelated external
submodule remains uninitialized.

## Scope

Publish the descriptor ownership matrix and five-configuration evidence.
Reconcile identity bytes and document existing implementation gaps.
Keep processor changes and adjacent repairs with their assigned owners.
No push, pull request changes, merge, hardware, or donor edits.

## Change list

| File:line | Change |
|---|---|
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:21 | Parent/processor ownership and limits |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:46 | L1-L10 and ADP matrix with enforcing paths and open owners |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:82 | Five configurations decoded from packed bytes |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:144 | Legal structural controls, invalid changes and actual refusal causes |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:185 | Identity derivation, descriptor equality and #495 reproduction |
| docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:223 | Bounded follow-up allocation |
| scripts/audit_pp_descriptors.py:41 | Packed-image decoder and reproducible audit measurements |
| docs/ENDSTATION_BUILDER.md:64,231,439,713,1054 | Ownership link, corrected descriptor census and image size, qualified identity claims |
| docs/README.md:63 | Reference-page entry point |

## Evidence

| Evidence | Result |
|---|---|
| L1-L10 and ADP ownership | Matrix drafted; parent shipping semantics and processor generic format duties distinguished |
| Five shipping configurations | 32/64/96/41/116 descriptors; 5792/10112/15360/7352/18288 bytes, in reference-page order |
| AUDIO_UNIT | Rate offset 144; N=3 for arty_current, otherwise N=1; lengths 156/148 |
| CLOCK_DOMAIN | Source offset 76; count 2; length 80; list [0,1] in every image |
| Legal boundaries and invalid changes | descriptor-audit.json contains per-probe results, including accepted invalid models |
| Identity and generator-owned bytes | Changing reset_time to 3 changes arty_4x4 byte 6741, while ENTITY model ID remains 0x001BC557FC6ABBC8 |
| Multi-configuration behavior | NOT RUN: each tracked image has one configuration; no maximum-across-configurations proof |

### Five-image receipts

| Configuration | Descriptors / bytes | ENTITY model ID | Image SHA-256 |
|---|---|---|---|
| endstation_arty_4x4 | 64 / 10112 | `0x001BC557FC6ABBC8` | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| endstation_arty_8ch | 96 / 15360 | `0x001BC507C86F4172` | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| endstation_arty_current | 32 / 5792 | `0x001BC50AC1000005` | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| endstation_ax7101_1x1_tdm8 | 41 / 7352 | `0x001BC5C40236BA0E` | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| endstation_ax7101_8x8 | 116 / 18288 | `0x001BC572F79BC5D1` | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |

`descriptor-audit.json` contains 30 packer probes, 13 YAML probes and two
map probes, plus the generator-only identity mutation. Accepted YAML probes
include decoded rows from the resulting image, not just a successful exit.
The receipt SHA-256 is
`8233f515e8e469570314fdfea9437db5d082a6441f04a75ff840efe5444f4779`.

`generator-cli.json` independently records five matching image hashes after
running all three documented CLI boundaries per configuration. Its build trees
were temporary and outside this output directory; they have been removed.

## Gates

All commands ran in the foreground, without pipelines. The per-command
runner used a 7200-second timeout and preserved each exit status in
`gates.jsonl`. Logs below are relative to this handoff.

| Command or mode | Exit status | Evidence |
|---|---|---|
| `python3 "$RECEIPTS/builder-mode.py" sdk --audit "$RECEIPTS/compiler-sdk.jsonl"` | 0 | builder-sdk.log; 755.3 s |
| `python3 "$RECEIPTS/builder-mode.py" absent --audit "$RECEIPTS/compiler-absent.jsonl"` | 0 | builder-absent.log; 566.96 s |
| `python3 avdecc/gen_aem_store.py --self-test` | 0 | aem-selftest.log; 0.11 s |
| `python3 scripts/audit_pp_descriptors.py --output $RECEIPTS/descriptor-audit.json` | 0 | audit.log; 0.46 s |
| `python3 scripts/check_entity_shape.py --self-test` | 0 | entity-shape.log; 40.7 s |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | nvm-firmware.log; 39.29 s |
| `python3 scripts/check_nvm_capture.py` | 0 | nvm-capture.log; 0.72 s |
| `python3 scripts/check_baremetal_only.py --check` | 0 | baremetal.log; 14.64 s |
| `python3 -B scripts/docs_check.py` | 0 | docs-git.log; 4.17 s |
| `GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | docs-no-git.log; 4.22 s |
| `python3 scripts/ci_events.py --check` | 0 | ci-check.log; 0.21 s |
| `python3 scripts/ci_events.py --selftest` | 0 | ci-selftest.log; 14.56 s |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | em-dash.log; 3.02 s |
| `python3 scripts/check_doc_style.py` | 0 | doc-style.log; 0.06 s |
| `python3 scripts/gen_toc.py --check` | 0 | toc.log; 2.52 s |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | anchors.log; 1.62 s |
| `python3 scripts/check_doc_paths.py` | 0 | doc-paths.log; 0.06 s |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | module-matrix.log; 0.97 s |
| `python3 scripts/xvlog_gate.py --check` | 0 | xvlog.log; 138.76 s |
| `python3 scripts/check_rtl_source_lists.py` | 0 | rtl-lists.log; 1.47 s |
| `python3 scripts/check_sv_idiom.py` | 0 | sv-idiom.log; 0.41 s |
| `python3 scripts/lint_rtl.py --check` | 0 | rtl-lint.log; 6.06 s |
| `python3 scripts/check_cpp_idiom.py` | 0 | cpp-idiom.log; 1.22 s |
| `python3 scripts/check_py_idiom.py` | 0 | py-idiom.log; 3.32 s |
| `python3 scripts/check_port_contracts.py` | 0 | ports.log; 2.32 s |
| `python3 scripts/measure_naming.py --check` | 0 | naming.log; 0.46 s |
| `python3 scripts/measure_test_evidence.py --check` | 0 | test-evidence.log; 5.32 s |
| `cd tests && behave --no-capture -f plain` | 0 | behave.log; 1.17 s |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | diff.log; 0.03 s |
| Three generator CLIs for each of five configurations | 0 | generator-cli.log and generator-cli.json; all image hashes matched |

### Environment and evidence limits

`RECEIPTS` is this output directory. The gate interpreter is
`$VALIDATION_STORAGE/509-a327-python/bin/python3`, a temporary environment outside
the output directory. Its Markdown packages came from the repository hash-pinned
`tools/markdown/requirements.txt`. The initial contents check failed on missing
`html5lib`; setup resolved that dependency, then all contents/anchor checks passed.

SDK mode first verified the read-only installation at
`$VALIDATION_STORAGE/504-manager-r1/sdk-install`. `builder-mode.py` maps only the
native compiler executable to that SDK and invokes the complete builder through
`runpy`, with `--require-rv32`. `compiler-sdk.jsonl` records each requested and
executed command. Compiler-absent mode hides the three cross-compiler candidates
and lets the existing host compiler probe take its normal stand-down path.

Evidence limits:

- SDK builder: `ALL GATES PASS EXCEPT 1 NOT RUN`; gate 11 resource calibration needs the unavailable mf48 placement report. The RV32 instruments did run (232 census compiles declared RV32, zero unstated).
- Compiler-absent builder: `ALL GATES PASS EXCEPT 2 NOT RUN`; gate 1b compiled census/resolver/preprocessor/include instruments and gate 11 calibration are not run. The three cross-compiler candidates were deliberately absent. These exclusions are not counted as passing.
- `gen_aem_store.py --self-test`: 20 checks pass at the #464-repaired base. Six declared compatibility-map deviations are preserved and reported, not repaired.
- `check_entity_shape.py --self-test`: 136 checks, zero failures.
- Documentation filesystem mode: zero findings; inventory parity is the one expected skip because Git is deliberately unavailable.
- Behavior tests: 14 features, 344 scenarios and 1739 steps pass; zero failed or skipped.
- xvlog: 0 parent findings; 4 existing processor findings equal the recorded ratchet.
- RTL lint: 90 findings equal the ratchet; 17 waived. Naming: 96 recorded candidates. Test-evidence ratchets pass. No budget or waiver changed.
- No hosted evidence, hardware run, publication or merge is claimed.

## Processor contract wording

Separate processor change after this parent review; no donor file changed.
Replace the section 3.1 introduction beginning "Structural rules enforced"
with the following text, preserving the L1-L10 clause table:

> The consuming product owns its shipping model semantics. For the parent
> end-station, the allocation and measured enforcement are recorded in
> `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` of kebag-logic/milan-fpga.
> That contract distinguishes construction from discriminating refusal.
> The processor owns generic packed-image structure and validation:
> image extents, directory well-formedness, dense indices, name binding,
> line-buffer bounds and descriptor type/index consistency. An ownership
> assignment is not evidence that every check is implemented. At processor
> commit 990f96526bb89356c963a260ebbdcf2a77e6623a, the packer checks density,
> duplicate keys, names and line-buffer bounds but does not compare the
> descriptor body's type/index with its directory key.
>
> Parent shipping checks are authoritative for configuration-dependent
> semantics: model identity and evolution, AUDIO_UNIT rate-list offset,
> count and length, clock-source construction and list shape, and ADP
> stream-count maxima across supported configurations. Processor checks
> retained for the same semantic constraints are defence in depth.
> Neither construction nor byte-exact serving substitutes for a negative
> validation case. Open obligations remain under processor issues 38,
> 39, 60 and 89 and the parent matrix's linked follow-ups.

Add after L10:

> The AUDIO_UNIT descriptor extent must equal 144 + 4 times its rate count.
> The parent currently emits one configuration per image, with one or
> three rate words. Its loader permits at most eight distinct entries,
> but its image conversion currently supports only 48000, 96000 and
> 192000 Hz. These are separate limits. The processor packer at the pin
> above does not enforce the L10 semantic offset/count/length checks or
> the L6 identity clock-source list; issue 89 remains open.

Add to integrator guide section 6:

> Drive entity_model_id_i from the same identity used in ENTITY bytes.
> Zero and all ones are invalid. A static-model change requires a new
> model identity, subject to IEEE 1722.1 section 6.2.2.8's exclusions.
> Drive talker_sources_i and listener_sinks_i with the maximum respective
> STREAM_OUTPUT and STREAM_INPUT counts over every supported configuration.
> The ENTITY descriptor must carry those same values. Drive identify_index_i
> with the primary IDENTIFY CONTROL index present in every configuration.
> These are integrator obligations, not properties proved by ADP transport.

Further precise processor documentation dispositions:

- F07.2's STREAM_PORT_INPUT-to-cluster `1..*` edge conflicts with the
  parent's documented zero-cluster 8x8 input pools. Resolve against the
  actual governing clause under PP60; this audit makes no waiver.
- L3 must preserve the distinct Milan 6.3 talker and 6.4 listener
  obligations. The parent's rate-family gate does not establish a
  universal per-stream, per-configuration Base-format rule.
- Section 3.2/3.3 must credit the parent constructor for Table 7-8 bytes.
  The packer preserves bytes; it does not synthesize the redundancy tail.
  PP82's runtime overlays and response ceiling remain separate work.
- The generic metadata/body consistency gap stays processor-owned under
  PP60. Publishing allocation does not close it.

## Follow-ups

| Record | Maintainer action | Reproducible evidence |
|---|---|---|
| F1 | File bounded parent invalid-model-ID refusal; coordinate PP38; do not add evolution to this new task | zero and all-ones model_id_pin each load and produce an image |
| F2 | File parent listener-buffer-floor refusal; coordinate PP60 L4 | 2125999 ns loads and packs; 2126000 is the legal boundary |
| F3 | File parent format-family/count/CRF-word validation; coordinate PP60 L3/L4 | mixed AAF/CRF list, 48-entry list, and CRF word ending BB81 each produce an image |
| F4 | File parent INTERNAL-source requirement for output models; coordinate PP60 L6 | sources [crf] with outputs retained produce an image |
| F5 | Resolve processor diagram/parent D8 cardinality discrepancy under PP60 | all eight 8x8 input ports decode to zero clusters |
| F6 | Schedule parent L6/L10 image validation and separate PP89 disposition | reversed [1,0], offset 143, ninth rate, count/length mismatch and truncation all pack |
| Existing | Keep #478 and #464 closed; preserve #495 identity/snapshot scope; leave PP82 runtime work and parent #76 qualification outside this lane | Public issue contracts and exact-pin measurements |

These are author observations and implementation dependencies, not review
verdicts. No production validator, shipping configuration, RTL or donor
pin was changed.

## Acceptance and handoff boundary

| Criterion | Author evidence | Remaining publication/dependency |
|---|---|---|
| 1: matrix | L1-L10/ADP rows include clauses, paths, consumers, boundaries and owners | Independent review and maintainer publication |
| 2: five configurations and discriminating probes | Decoded receipt, measurements, 45 probes and 15 CLI invocations | No multi-configuration proof claimed |
| 3: identity and contract ownership | Generator-only mutation reproduced; parent text updated | Exact processor wording above, for a separate reviewed change; no implementation relies on it |
| 4: bounded follow-ups | F1-F6 with cause-specific evidence; existing owner scopes preserved | Maintainer filing and the F07.2 clause-backed decision |

These are completion claims for the assigned audit delivery, not independent
review verdicts or a declaration that the Issue is ready to merge.
Both plain and base-relative `git diff --check` passed after the commit.
The worktree remained clean after the final builder run.

## Final state

Head: `20423082f221a02f3de72952cec4e1ac0c839b1d`. Worktree clean after commit.
Review-ready comment: https://github.com/kebag-logic/milan-fpga/issues/509#issuecomment-5845228758
Commit subject: `Document processor descriptor ownership and audit evidence`.
No body or trailers.
Independent review and publication remain with the assigned maintainers.
