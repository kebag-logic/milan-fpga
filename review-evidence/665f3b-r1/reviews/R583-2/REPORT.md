[R583] NEGATIVE - exact head 651ccb5aea1bc4d99f356503c188947d39e0c9e4

External independent review, R583-2, issue #665 / PR #736.
Tree: `efe717466398cf59ad71dc436feb74c6d1fe9c9d`.

The per-source predicate and timing corrections pass the focused checks. One MAJOR remains: the new timing-page checker is missing from the CI classifier's document dependency table. This fails the exact-head hosted selector before either required firmware job executes. The earlier hosted-proof finding therefore remains open.

## Scope and independence

Reconstructed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue and public scope decisions, requirements and interface authorities, then source-base history/diff and public execution evidence. The source-base range is `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0..651ccb5aea1bc4d99f356503c188947d39e0c9e4`. The implementation reviewed is `d40e4e98..651ccb5a`, with particular attention to the three-commit round-2 delta `db29bdd0..651ccb5a`. Inherited #705 implementation was distinguished from this lane.

Scope authorities: [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151273346), [corrected pin/behavior scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151422598), [ruling item 4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6092086337), and [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6153927545).

The independent diff pass preceded reading prior findings. An independent verdict and five-lens ledger were written before opening the prior review bodies. No private author material, work-history document, or other checkout was read. Public evidence was fetched from immutable publication [e3af7960](https://github.com/kebag-logic/milan-fpga/tree/e3af796024d095e9f5cb9fa231e8efe34c501100/review-evidence/665f3b-r1). All 67 retained author artifacts were checked against their published Git blob IDs (`receipts/public-evidence-identity.json`).

## Open finding

### R583-2-F1 - MAJOR - Conformance, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/test/ctrl_service_bounds.py:13`, `scripts/ci_scope.py:68`, `.github/workflows/rtl-fast.yml:43`, and `docs/testing/CI_WORKFLOWS.md:202`.

**Authority/evidence:** Round-2 item 2 requires successful executed `firmware-boundary`, `firmware-verilator`, and `rtl-fast` at the new head. AGENTS.md section 7 requires a successful current-head verdict. The workflow policy requires the classifier's table to include documents consumed by gated checks.

The newly added `ctrl_service_bounds.py` reads `docs/design/MAILBOX_SPLIT.md`. `GATE_READ_DOCS` does not include that page. Both independent commands reproduce the omission:

```text
python3 scripts/ci_scope.py --selftest
  FAIL gate-read page docs/design/MAILBOX_SPLIT.md
       (named at sw/firmware/ctrl/test/ctrl_service_bounds.py:13) is relevant
selftest: 1 FAILURE(S)
exit 1

python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md
false
exit 0
```

Receipts: `receipts/ci-scope.log`, `receipts/ci-scope.rc`, and `receipts/ci-scope-classification.log`.

Directly read [hosted run 38464016325](https://github.com/kebag-logic/milan-fpga/actions/runs/38464016325), whose `head_sha` is the exact reviewed head. The `changes` job [115526169267](https://github.com/kebag-logic/milan-fpga/actions/runs/38464016325/job/115526169267) fails on the same selftest. `firmware-verilator` (115526474447) and `firmware-boundary` (115526475388) are **skipped**, and the `rtl-fast` aggregate fails. The same failure occurs in `elaborate` and `full-ci-gate`; the long-gate aggregates fail and their shards are skipped. Raw job metadata and logs are retained under `receipts/hosted-*`.

**Impact:** The current head cannot satisfy the assigned hosted validation. The timing document is also incorrectly classified as docs-only despite now supplying executable test input. This is a gate-integration and document-verification defect, not prose residue. The selftest catches it and prevents a false green.

**Required outcome:** Register the timing page as a relevant gate input, or provide an equivalent policy-compliant always-run check. Keep the selector selftest intact. Obtain successful execution of both firmware jobs and `rtl-fast` at the corrected head; satisfy the other required contexts through the manager's acceptance procedure.

**Verification:** The two commands above must return a passing selftest and `true` classification. The compiled service-bound check and its 38 controls must still pass. Read the corrected exact-head hosted job steps and conclusions; skipped jobs do not clear this requirement. Re-review the corrected head.

This finding retains the outstanding outcome of **R582-1-F1 (MAJOR; Tests, Conformance)**. Its scratch-maintenance source repair passes local checks, but its explicit hosted-execution requirement remains unmet for a new, independently reproduced reason.

## Prior finding dispositions

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R583-1-F1, MAJOR, all five lenses | Resolved | `maap_mbx.c:36` caches the complete `acmp_declaring` answer. `:52` retains interface, allocation count and range validity. The unchanged `probe_owner.cpp` passes; IF1/IF2 Listener and answered-probe composition tests pass. The source-validity mutant is caught by both demand arms at both interface counts. |
| R583-1-F2, MINOR, Conformance/Tests/Docs | Resolved | `MAILBOX_SPLIT.md:752` uses 3,523 / 4,429, with independently compiled header results and all four corrected products. Both event envelopes exceed 10 ms. `service-bounds.log` reports 38/38 controls caught. F1 above concerns integration of the new guard, not incorrect table values. |
| R582-1-F1, MAJOR, Tests/Conformance | Retained; source repair verified, hosted proof outstanding | Six lifecycle checks pass, including persisted and command-level maintenance settings, loose fetch, ENOENT tolerance, and EACCES/EIO propagation. Exact-head firmware jobs were skipped. |
| R582-1-F2, MINOR, Docs; R583-1-R1, RESIDUE, Docs | Resolved | `SUBMODULES.md:256` expressly states that the current pin includes #19's ADP refusals. Submodule and documentation checks pass. |
| R582-1-R1, RESIDUE, Docs | Resolved | The cited links in `sw/firmware/gtest/README.md` now use `70936b77`; the referenced ownership/reentry contract is preserved. |

The prior optional suggestions remain optional and do not prevent clean coverage:

- **R582-1-S1 - SUGGESTION - Tests - `maap_mbx.c:127,157`.** The prior receive/link refresh-removal probes had no dedicated killer. The later poll repairs the snapshot within the pass. Optional outcome: add a discriminating timing observation or explicitly document that redundancy. Verification: a named control must fail for a removed refresh. This review does not claim those two controls were added.
- **R582-1-S2 - SUGGESTION - Tests, RTL - `test_maap_mbx.cpp:529`, `maap_mbx.c:44`.** The maximum-source callback test uses Listener demand; it does not force all funded freshness reads. The current source limit is 16. Optional outcome: measure the all-answered-source case and guard the bitmap capacity. Verification: an overrun or capacity violation is rejected. No current supported-shape overflow was found.
- **R582-1-S3 - SUGGESTION - Docs - `maap/README.md:112`.** Poll/tick observation latency remains described in words. Optional outcome: state the bounded latency numerically, with its service assumptions. Verification: compare against the mailbox tick and poll order; physical timing remains unmeasured.
- **R582-1-S4 - SUGGESTION - Docs - PR #736 description.** The body names the three newly adopted changes; the public handoff additionally explains #23's integration of the old pin. Optional outcome: add that integration distinction to the body. Verification: preserve the distinction between new behavior and already adopted publication code.

## Acceptance evidence

**Pin provenance.** The move is `405dc68310a18f669049ffc10cc23eef7300dcff` to `70936b77dc41981e192438388cd0aced69954f18`. Merge metadata, verdict headers and local objects agree:

| Stack PR | Merge commit | Reviewed head | Positive dependency reviews |
|---|---|---|---|
| #19 | `51870377c5012766a8ea1d9798e3c499ca1060a3` | `66b3a757` | [R576](https://github.com/kebag-logic/tsn-c-stack/pull/19#issuecomment-6085778617), [R577](https://github.com/kebag-logic/tsn-c-stack/pull/19#issuecomment-6086078198) |
| #20 | `98dc9e3076714bebe113982ee18c3c1c496cf3c9` | `0c5ef532` | [R578](https://github.com/kebag-logic/tsn-c-stack/pull/20#issuecomment-6088675209), [R579](https://github.com/kebag-logic/tsn-c-stack/pull/20#issuecomment-6088680624) |
| #25 | `70936b77dc41981e192438388cd0aced69954f18` | `f13c9c16` | [R630](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6130759174), [R631](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6130754591) |

History also contains #23, merge `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475`, integrating the old pin's publication code into main. Its tree equals reviewed integration head `3c9ca52f`, with separate [R622](https://github.com/kebag-logic/tsn-c-stack/pull/22#issuecomment-6116467700) and [R623](https://github.com/kebag-logic/tsn-c-stack/pull/22#issuecomment-6116469528) integration verdicts. It is not an additional newly adopted behavior. Before F3b, the only changed production source/header versus the old pin is `src/adp.c`. All 45 net changed paths belong to the authorized PR file sets. The target tree equals #25's reviewed head. The public handoff lists each merge and review. See `receipts/evidence-audit.json` and `receipts/public-author/pin-proof.json`.

**Predicate and ordering.** Reviewed `acmp_mbx.c:102`, `ctrl_app.c:28,78`, `ctrl_app_srp.c:53`, `srp_mbx.c:580`, `maap_mbx.c:36,52,72,164`, and stack `acmp.c:1249`. They implement valid source DA AND (answered probe younger than 15,000 ms OR registered Listener), constrained by interface and allocation. MAAP callbacks use a snapshot and invoke no synchronous core query. Gate writes precede allocation reports; idle ticks retire expiry. A source becoming valid through its allocation callback opens on the following poll, as documented. Asking Failed counts as demand separately from media licence. No unrelated parent production behavior change was found.

**Executed focused checks.** Eight arms passed: ADP 54 checks; ACMP 130; two-interface ACMP 29; MAAP 37 core/allocation plus 21 mailbox; two-interface MAAP 22; SRP composition 60 at each interface count; SRP unit 59. The unchanged prior probe passed with both invalid-source demand arms closed and the valid-source control open. It is byte-identical to the published R583-1 probe (`receipts/probe-identity.json`).

The tests cover lengths 0..81, versions 1..7, wrong ADP control lengths and a valid mailbox discovery; fresh probe, Listener, neither, 14999/15000/15001 ms; source validity independent of MAAP; source/interface isolation; acquisition/loss ordering; idle wake; no reentry; and SRP Ignore, Asking Failed, Leave, rejoin and destruction. Nineteen focused F3b/ADP/publication mutants were caught at 24 designated test/arm checks, including the retained two-interface gate control. Raw failures are in `receipts/focused-controls/`.

**Published source-head evidence.** The original campaign contains 519/519 caught parent mutants. Round 2 adds the source-validity control: the live table, CSV, and four successful sliced logs contain exactly 520 distinct names, all caught. AECP reports 76 and SRP 278 caught; adjusted line/branch coverage is 100% across 30 files, with explicit exclusions. The unsliced control attempt timed out (124); the four successful exhaustive slices are the completion evidence. Host and RTL compiler-boundary receipts pass with 126 pin controls. These are author source-head receipts, not manager source-bank executions. Twenty changed-file digests in the published final-state record match this checkout.

**Images.** Audited the published 15 before/after rows across five shapes and three compositions. The first-round maximum Release load growth was 1,320 B; the corrected head reports 988 to 1,304 B, below the [2,048 B Release ceiling](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947). All before/after ELF digests and section sizes are retained in `receipts/public-author/round2/image-hashes.json` and `image-table.md`. These images were not independently rebuilt in this review.

The all-fabric load artifacts remain identical in the published receipts:

| Artifact | Bytes | Before / round 1 / round 2 SHA-256 |
|---|---:|---|
| BIOS binary | 52,988 | `5a2c937f40542238114c7bdd267d0eb2977a70a5cb0eb72889cc4ec3d1c0d4f3` |
| AEM descriptor | 7,512 | `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` |

No claim is made that every generated build artifact or routed bitstream is identical.

**Interfaces and documentation.** The assigned `KL_mbx_pkg.sv` and `mbx_contract.h` changes are comments only; register encoding and CDC/reset logic do not change. The generator's check/crosscheck/selftest, submodule-document check, diagram check and documentation check all passed locally. The contract states predicate equivalence, and the obsolete egress consequence is removed. Independent header compilation gives three-module bounds 1,783/1,879 and four-module bounds 3,523/4,429. The four-module products are 10,569/13,287; 38,753/48,719; 77,506/97,438; and 31,707/39,861 accesses. The numerical correction is sound; F1 prevents its CI integration from clearing.

## Hosted evidence

Direct observations at 2026-10-13 20:48 UTC are retained in `receipts/hosted-summary.json`.

| Head / run | Executed results | Skips / pending |
|---|---|---|
| `651ccb5a`, rtl-fast 38464016325 | Selector and aggregate fail; bdd-conformance succeeds | Both firmware boundary jobs, firmware unit/mutation jobs, lint, elaboration and census skipped |
| `651ccb5a`, rtl-full 38464016359 | full-ci-gate and both aggregates fail | Long-gate shards and physical context skipped |
| `651ccb5a`, elaborate 38464016332 | Fails the same selector selftest | No successful elaboration evidence from this run |
| `651ccb5a`, docs 38464016320 | docs-check-no-git and wire-accountability succeed | docs-check still in progress at observation |
| `db29bdd0`, rtl-fast 38451042997 | Both boundary jobs fail during scratch deletion; other firmware unit/mutation jobs succeed | Old-head failure is not corrected-head proof |
| `db29bdd0`, rtl-full 38451042883 | All five simulation shards and all four synthesis shards succeed; aggregates succeed | Physical context skipped; evidence belongs to the old head |

## Reviewer-owned lens ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1; retained R582-1-F1 | #665 frozen decisions; REQUIREMENTS.md section 1; processor 05_acmp_engine.md:405; stack acmp.c:1265; maap_mbx.c:36; image/pin audit; exact-head hosted run 38464016325 | R583-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| RTL | CLEAN | mailbox.yaml:324; KL_mbx_pkg.sv:303 comment-only delta; ctrl_app.c:28; ctrl_app_srp.c:53; maap_mbx.c:36,52,95,164; mailbox generator receipt and interface tests | R583-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Robustness | CLEAN | test_adp.cpp:543; test_maap_mbx.cpp:252; test_acmp_mbx.cpp:447,490; srp_feedback.hpp:4; unchanged probe_owner.cpp; ctrl_pin_lifecycle.py; focused controls | R583-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Tests | UNCLEAN - F1; retained R582-1-F1 | Eight executed arms; 19 mutants / 24 targeted checks; 520-name public audit; lifecycle/service controls; ci_scope.py:68 and hosted selector log | R583-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Docs | UNCLEAN - F1 | MAILBOX_CONTRACT.md:255; MAILBOX_SPLIT.md:725,752,1060; SUBMODULES.md:256; maap/README.md:112; gtest/README.md links; CI_WORKFLOWS.md:202 and omitted document dependency | R583-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |

## Reproduction, limits and manager duties

Portable runners in `scripts/` take `--repo` and `--packet`, or positional repository/packet arguments. `run_focused.py --jobs 3` runs three independent arms with four compilation jobs each; `run_probes_fixed.py` runs the unchanged probe and both header evaluations. `focused_controls.py --mode mutations --jobs 4`, `--mode lifecycle`, and `--mode bounds` reproduce the focused controls. `static_checks.py`, `audit_evidence.py` and `verify_tree.py` reproduce the remaining checks. Disposable output belongs under `scratch/`, which is excluded from publication.

All processes were kept under foreground parent commands and joined before completion. No source fixes, commits, pushes, GitHub writes, other-checkout edits, sub-agents, container execution, privileged installation, hardware action, or full parent/processor/synthesis/builder bank was performed. The specified simulator identity was checked before use; no full local simulation sweep is claimed.

Physical calibration was **NOT RUN**. Field skips are not hardware proof. Mailbox transaction bounds exclude CPU and external callback timing; no target 10 ms acceptance or complete physical release acceptance is inferred. Protocol interpretation followed the approved scope and repository/processor/stack authorities; the full Milan/IEEE publications were not independently re-audited.

There is **no manager source bank at this exact head**, and none is claimed. Source validation is distinct from the final current-dev merge candidate. The manager still owns hosted/act acceptance, the candidate built against current dev (the assignment records `0136de16291a127e0a34627c77ac09cd41efc08b`), builder/native bank receipts, independent corrected-head review, explicit merge authorization, and post-merge containment. No source-head result clears those duties.

Final verification hashes every tracked blob's raw bytes, checks executable/symlink modes, compares all stage-zero index entries with the recorded trees, and verifies all five required submodule gitlinks/heads. It passed: 1,311 superproject blobs and 1,043 submodule blobs, no untracked files. The unused external gitlink remains uninitialized. See `receipts/final-tree-verification.json`. No tracked source restoration was necessary because all probes used disposable copies.

`MANIFEST.sha256` lists the publishable scripts and receipts. Only those files and this report belong in the publication packet.

R583-2 FINISHED
