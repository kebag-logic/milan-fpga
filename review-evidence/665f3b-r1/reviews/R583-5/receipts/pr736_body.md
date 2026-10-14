[A612]

## Contents

- **[Status](#status)** -- Local results and outstanding hosted proof.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent review.
- **[Description](#description)** -- Final F3b behavior and pin scope.
- **[Authoritative references](#authoritative-references)** -- Requirements and decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Candidate and dependencies.
- **[How to validate](#how-to-validate)** -- Reproducible checks.
- **[Round 2](#round-2)** -- Review corrections and controls.
- **[Round 3](#round-3)** -- CI document dependency and review corrections.
- **[Round 4](#round-4)** -- Stale gate-read page count.
- **[Round 5](#round-5)** -- Merge of current dev for the CI definitions.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Evidence boundaries.
- **[Definition of Done](#definition-of-done)** -- Remaining review and merge requirements.

## Status

REVIEW READY: affected local gates pass under the round 5 assignment.
Hosted acceptance remains manager-owned.
`665-f3b-parent` -> `dev`.
Candidate: `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`, the merge of dev
`fa7347fc59173f90e4feec2df207692e6e6e72ec` into `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5`.
Its tree is `f1c1f47cb4fefb8a6c68418d03dc762f72cbee15`, the tree `git merge-tree` predicts.
The merge changes nothing else.
Original base: `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Round 2 resumes `db29bdd07529fbc697b7956827092f64b1241714`;
`7032bca5a51d8d97fcb73d7fc106ca4af21de38e` is the head to publish on PR #736.

Parent campaigns caught 520 control, 76 AECP and 278 SRP mutations, with no
escapes. Coverage is adjusted 100% lines and branches across 30 files.
Both local compiler-boundary gates pass, including all 126 pin controls.
Round 5 local checks pass; exact-head hosted acceptance follows the manager's push.

## Linked Issue / roles

Relates to #665.

Executor: `[A612]`.
Independent reviews: R582-4 and R583-4 are positive at `6b4feeca`.
Review of the merge head `7032bca5`, including the reviewer-owned lens
ledger, remains pending. The author supplies validation evidence, no verdict.

## Description

`DA_GATE` publishes each source's `acmp_declaring` result: valid source
destination and either an answered probe younger than 15000 ms or a registered
Listener. The source must also belong to the interface and have an allocation.
MAAP allocation alone leaves the gate closed. The adapter snapshots the core
predicate outside MAAP callbacks and preserves gate-before-allocation-report
ordering. Idle service observes probe expiry.

Listener presence remains separate from the media licence. Asking Failed
provides declaration demand while leaving that licence closed. Mailbox and SRP
composition tests cover both interfaces, validity changes, withdrawal and expiry.

The full F3b lane moves the stack from `405dc683` to reviewed merge `70936b77`,
adopting #19, #20 and #25 under the corrected scope. Round 2 does not move it
again. Parent tests cover the adopted ADP malformed-discovery refusals.
The range also includes #23, integrating the old pin's publication code;
it adds no newly adopted behavior. Rounds 3 to 5 preserve the pin and firmware.

The default fabric BIOS and AEM descriptor remain byte-identical to the original
baseline. Across five shapes and three compositions, Release load growth is
988 to 1304 bytes, below the unchanged 2048-byte ceiling. Every linked image
passes its RV32I/ILP32 audit. HANDOFF.md records all before/after digests and sizes.

## Authoritative references

- #665 initial assignment, comment 6151273346; corrected scope, comment 6151422598.
- #665 round 2 assignment, comment 6153927545.
- #665 round 3 assignment, comment 6155487551; round 4 assignment, comment 6156987825.
- #665 round 5 assignment, comment 6158656140.
- #736 R582-4, comment 6157464972; R583-4, comment 6157466128.
- #736 R582-3, comment 6156867741; R583-3, comment 6156980716.
- #736 R582-2, comment 6155478463; R583-2, comment 6154961424.
- #736 R582-1, comment 6153917004; R583-1, comment 6153315844.
- Milan v1.2 4.3.3.1 and T-SRP-DAFRESH; IEEE 1722.1 ADP reception.
- `protocol-processor/docs/architecture/05_acmp_engine.md:405`.
- `sw/mailbox/mailbox.yaml`, `docs/reference/MAILBOX_CONTRACT.md`, `docs/design/MAILBOX_SPLIT.md`.
- Stack #24 Release-ceiling decision, comment 6126295947; reviewed stack #25.

## How to get into the same state

After the integration owner publishes the candidate, check out the recorded
commit and initialize only the dependencies required by the selected gates.
Verify each submodule's root before further Git operations, then its own origin.

```sh
git switch 665-f3b-parent
git checkout 7032bca5a51d8d97fcb73d7fc106ca4af21de38e
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
for submodule in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    test "$(git -C "$submodule" rev-parse --show-toplevel)" = "$PWD/$submodule" || exit 1
    git -C "$submodule" remote get-url origin
done
```

Use CPython 3.12.3, pinned Verilator 5.050 and the recorded RV32 compiler/runtime.
Set `TMPDIR` and `WORK` to disk-backed scratch, `MILAN_RV32_CC` and `VERILATOR`
to the selected executables, and keep outputs outside the checkout.
Use at most four campaign jobs and two Verilator builds.

## How to validate

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 --build-dir "$WORK/normal"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 --build-dir "$WORK/control"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 --build-dir "$WORK/aecp"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 --build-dir "$WORK/srp"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$WORK/coverage"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out "$WORK/image-controls"
python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/lint_rtl.py --check --self-test --jobs 2
python3 scripts/docs_check.py
python3 scripts/check_submodule_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
```

Expected: zero exit status, no escaped mutation, and adjusted 100% firmware
coverage. For sessions limited to ten-minute commands, HANDOFF.md supplies
the bounded campaign schedule and complete builder captures used for the
successful local runs. Those batches retain the exact live mutation tables
and the boundary gate checks their full capture union.

The handoff also records all 15 image pairs, the all-fabric identity check,
the unchanged review probe, six harness mutations, and each gate's planted controls.

## Round 2

- R583-1-F1: use the core's source-validity predicate. New Listener and probe
  composition tests compare core and published bits at IF1 and IF2, including
  valid-source positive controls. The unchanged `probe_owner.cpp` passes.
- R582-1-F1: persist `gc.auto=0` and `maintenance.auto=false` in every scratch
  repository and supply both on every helper Git command. Removal ignores
  disappearing files; permission and I/O errors still fail. Local boundary
  runs pass with 126 pin controls and six additional harness mutations killed.
  Hosted proof remains required after publication.
- R583-1-F2: recompute all dependent paths from 3523/4429 accesses per pass.
  Event envelopes at one microsecond per access are 10.569/13.287 ms; neither
  meets 10 ms. The compiled-header document check catches 38 planted errors.
- R582-1-F2/R1: document the adopted #19 ADP change and update five old stack
  permalinks. The pin, binary-identity requirement and Release ceiling remain fixed.

## Round 3

- R582-2-F1 / R583-2-F1: register `docs/design/MAILBOX_SPLIT.md` in
  `GATE_READ_DOCS`, identify `ctrl_service_bounds.py` as its reader, and add
  the classification case that catches removal of the registration.
  `CI_WORKFLOWS.md` now lists the dependency and its firmware job.
- The whole-branch inventory covers 330 gated files and 185 documentation
  candidates. All eight gate-read pages are registered and relevant;
  none is missing or stale. Reader-spelling and removal controls pass.
- R582-2-S1: document that receive/link refreshes keep callback snapshots
  current within the service pass; that pass's poll refreshes and republishes
  changed gates. This is documentation only. The optional deferred-ANNOUNCE
  and out-of-allocation demand tests remain future suggestions.
- R582-2-R1: correct round 2's published-head wording and remove the two
  stale limitation bullets. No image, predicate, coverage or mutation input changes.
- The service-bound check passes 47 checks, including 38 planted controls.
  The CI workflow contract passes 2169 items and 3064 control arms.
  Source-list, evidence-reader, documentation and Python checks pass.

```sh
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md
python3 "$EVIDENCE/round3/gate_read_inventory.py" --repo .
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 "$EVIDENCE/round3/service_bounds.py" --repo . --out "$WORK/service-bounds"
```

Set `EVIDENCE` to the published evidence packet.
Expected: all commands return zero; the page classification prints `true`.
The handoff records each affected gate and its controls.
Round 2's complete image, coverage and firmware mutation tables remain the
recorded measurements; round 3 does not rebuild unchanged firmware inputs.

The round 3 assignment accepts local validation for REVIEW READY.
The manager still owns the push, exact-head `changes`, `firmware-boundary`,
`firmware-verilator`, `rtl-fast`, `verilator-suites`, and `yosys-portability`
acceptance, independent re-review, and the final merge bar.

## Round 4

- R582-3-F1 / R583-3-F1: `docs/testing/CI_WORKFLOWS.md:179` said "Seven
  pages" after round 3 registered an eighth. It now reads "These pages", so
  the sentence cannot go stale when `GATE_READ_DOCS` changes. The paragraph
  still links all eight registered pages.
- R582-3-R1 / R583-3-R1: this body names the new head as the published head.
- Nothing else changes: one line in one file. Firmware, scripts, tests,
  generated files and the pin are untouched. R583-3-S1's optional count
  check is not added, because the count no longer exists.

```sh
python3 scripts/ci_events.py --check
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
python3 scripts/ci_scope.py --selftest
python3 -I "$EVIDENCE/round4/gate_read_paragraph.py" --repo .
```

Expected: all commands return zero. The paragraph check finds eight linked
and eight registered pages, and its six planted controls are refused,
including a restored "Seven" and a stated "Eight". On the `532ab871` page it
returns 1. Every other affected documentation and CI gate also passes with
its self-test; the handoff records each one and its controls. The 30 retained
image digests still match, so round 2's image, coverage and mutation tables stand.

## Round 5

- Merge: dev `fa7347fc` (#696 `ebac072b` and #734) into `6b4feeca` with a merge
  commit, no rebase. The merge tree is `f1c1f47cb4fefb8a6c68418d03dc762f72cbee15`,
  equal to the `git merge-tree` prediction and the manager's candidate tree.
  Nothing else changes: every path keeps one side's bytes, the gitlinks keep the
  lane's, and the diff against dev is the lane's 46 paths.
- Three files changed on both sides and merged without overlap:
  `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` and
  `sw/firmware/ctrl/maap/README.md`. `docs/design/MAILBOX_SPLIT.md` is still in
  `GATE_READ_DOCS` after #734's rewrite; #734 changed only the classifier's self-test.
- Dev changes no firmware image input. The stack pin stays `70936b77`.

```sh
python3 scripts/act_ci.py --selftest
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
python3 -I "$EVIDENCE/round5/mailbox_split_registration.py" --repo .
python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/maap-differential"
python3 -I "$EVIDENCE/round5/integrity.py" --repo .
```

Expected: all commands return zero. The act self-test passes 570 arms, and the
flat isolated install that the docs job runs passes too. The scope self-test passes 202 arms,
including refusal of each gate-read page filed as documentation only. The CI contract holds 2174 items.
The registration check refuses four planted edits of the entry and returns 1
on dev's own `ci_scope.py`. The MAAP differential, where #696's test change
meets this lane's adapter and pin, passes 12 checks and catches 17/17 mutants.
The documentation, idiom, evidence-reader and source-list gates and their
self-tests also pass at the merge; the handoff records each one with its controls.

## Known limitations / out of scope

- No placement switch, hardware access, flashing, synthesis or bitstream build.
- Experimental images establish link/ABI and growth evidence, not shipping RAM fit or physical timing.
- Independent re-review, candidate-merge validation and post-merge containment remain open.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including new-head hosted proof
- [x] New or changed behavior has self-checking tests
- [x] Affected local verification gates pass
- [ ] Full repository merge verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
