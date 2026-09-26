[A333]

## Status

Round 2 complete; all 30 recorded local gate invocations returned 0, with existing skipped arms documented below. The candidate is local and unpushed. `509-pp-descriptor-ownership` -> `dev`.
Head: `04c9802d852befba3b5d854ba5f3faf3ddfc59a7`. Internal delta review and publication remain pending. R331-1 is the accepted ancestor external review.

## Linked Issue / roles

Closes #509
Relates to #478, #464 and #495.

Author: [A333] (round 2); [A327] (round 1). Internal reviewer: [R330]. External reviewer: [R331].

## Description

The processor contract assigned descriptor semantics to model lint without an
explicit allocation to the shipping builder. This change publishes the L1-L10
and ADP ownership matrix, measures all five packed shipping images, and separates
construction from demonstrated refusal. A reproducible audit records accepted
invalid inputs as findings. The builder reference now reflects the measured
census and the limits of model-ID derivation.

The allocation follows the public assignment decision. Generic packed-image
structure remains processor-owned; configuration-dependent shipping semantics
are parent-owned. The separate processor contract change has exact proposed
wording in processor-wording.md, linked from HANDOFF.md. Production validators, shipping inputs and donor pins
are unchanged.

## Authoritative references

- #509 and its assignment comment 5844867005; REQUIREMENTS REQ-VER-03/04.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` and `docs/ENDSTATION_BUILDER.md`.
- Processor memory-map section 3.1 at `990f96526bb89356c963a260ebbdcf2a77e6623a`.
- Processor issues 38, 39, 60, 82 and 89; existing parent owners #478/#464/#495.

## How to get into the same state

Use branch `509-pp-descriptor-ownership`, based on
`7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, with its initialized pinned submodules.
Install the repository-pinned Markdown requirements in a temporary environment:

```sh
python3 -m venv --system-site-packages /tmp/descriptor-audit-env
/tmp/descriptor-audit-env/bin/python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
. /tmp/descriptor-audit-env/bin/activate
```

The read-only RV32 SDK was verified with `scripts/ci_rv32_sdk.py --verify-only`.
The handoff includes `builder-mode.py`: SDK mode maps the native compiler
selection to that verified SDK; absent mode hides all three cross-compiler
candidates. Both execute the complete existing builder entry point.

## How to validate

```sh
python3 scripts/audit_pp_descriptors.py --output /tmp/pp-descriptor-audit.json
python3 sw/builder/test_builder.py --require-rv32
python3 sw/builder/test_builder.py
python3 avdecc/gen_aem_store.py --self-test
python3 scripts/check_entity_shape.py --self-test
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 scripts/check_nvm_capture.py
python3 scripts/check_baremetal_only.py --check
python3 -B scripts/docs_check.py
GIT_DIR=/dev/null python3 -B scripts/docs_check.py
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_sv_idiom.py
python3 scripts/lint_rtl.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
(cd tests && behave --no-capture -f plain)
git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
```

Select SDK and compiler-absent environments respectively for the two builder
commands. `GIT_DIR=/dev/null` exercises the CI filesystem-inventory path without
removing the checkout metadata. Full CLI regeneration through the builder,
store generator and image join matched all five audited image hashes.

Expected: every gate exits 0. Accepted invalid-input probes are documented
findings, not compliance passes. #464 is closed and its repaired generator
self-test passes all 20 checks at this base. ADP/entity-shape self-test: 136
checks, zero failures. SDK builder: one arm not run (missing calibration report). Compiler-absent
builder: two arms not run (compiler instruments and calibration).
The filesystem documentation mode skips inventory parity as expected.
Behavior tests pass 344 scenarios and 1739 steps. Existing xvlog/RTL lint
ratchets remain at 4/90 findings. Full results are in HANDOFF.md.

## Known limitations / out of scope

- Each tracked image contains one configuration. No maximum-across-configurations proof is claimed.
- Follow-ups F1-F4 cover invalid model IDs, buffer floors, format lists and required INTERNAL sources. The maintainer files these bounded parent repairs.
- F5 records the processor diagram's cluster-minimum discrepancy with zero-cluster input pools; it requires a public clause-backed decision under processor #60.
- F6 allocates parent image-boundary L6/L10 checks and separate processor #89 work. #478 is not expanded.
- F7 allocates processor body type/index consistency against the directory key, separately from processor #60.
- F8 owns the six shipping arty_current static-map stream-channel deviations and their clause-backed product-policy disposition. #464 remains closed.
- Generator-owned identity evolution, unused snapshots and the other round-1 suggestions remain #495.
- Processor #82 runtime overlays/response limits, hardware qualification and merge evidence remain separate work.

## Definition of Done

- [x] Ownership matrix, five-image measurements and identity reconciliation are documented
- [x] Audit probes use real generation and isolated mutations
- [x] Required local verification commands returned 0 with documented skips
- [ ] Evidence is posted in a PR comment
- [x] Parent contract is updated; exact separate processor wording is supplied
- [ ] Internal review is positive
- [x] External review R331-1 is positive at the ancestor head, retained by the round-2 assignment
- [ ] Every review lens is clean at the applicable head
- [ ] Blocking findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Hosted checks and candidate merge validation pass
- [x] Documentation is updated
- [ ] Post-merge containment is checked before Done


## Round 2

Re-derive identity with the generator mutation active and require a discriminating identity control. Preserve audit integrity under optimized Python. Allocate the body/directory mismatch to F7 and the six shipping arty_current static-map deviations to F8; qualify L7 and enumerate the remaining L6 sub-rules.

Exact local head: `04c9802d852befba3b5d854ba5f3faf3ddfc59a7`.

All required local gates returned 0. The original audit receipt is byte-identical under normal Python, optimized Python and a fresh candidate export. R330 M3 now rotates the model ID from `0x001BC5F531E6A9DA` to `0x001BC572445BE3EA`, matching the unchanged fresh-process CLI probe. R331 M3 now refuses normalization both normally and under `-O`. The other published mutants retain their expected discriminating outcomes. Ten explicit refusal controls and a legal control pass in both interpreter modes.

Reviewer probe/mutation bodies were preserved. The R331 wrapper itself pins the old head and creates checkouts, so its bodies were applied to disposable exports of this head under the assignment's no-other-checkouts restriction. All temporary exports were removed.

F7 and F8 remain bounded maintainer-filing records under #509. R330 delta re-review is pending; the assignment retains R331-1 as the ancestor external positive. No reviewer-owned completion ledger, hosted acceptance or merge approval is claimed.
