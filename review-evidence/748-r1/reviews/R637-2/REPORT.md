[R637] POSITIVE - exact head 2e83841675e4e1439c413c9ca11b4a123898a60e

R637-2, external independent delta review of issue #748 / PR #749.
Tree: `4b1bed5825eae73757cb5368c71468c7d1d67d72`.
Source base: `9ef717727e6fdac11ee7f01672fefae948452343`.
Previously reviewed head: `c48bfe38b25f002d24898cec265520b9fc1a7111`.

All five lenses are CLEAN. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is recorded. All five named prior findings are resolved, including the accepted optional post-gate cache comparison. This approves the reviewed source delta; it is not approval of a future merge tree or a statement that manager acceptance duties are complete.

## Scope and independence

Reconstructed AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and frozen public assignments, REQ-VER-02/03/04, the Elaboration section of CI_WORKFLOWS.md, submodule ownership, the patch installer and interpreter-selection contracts. Then examined the complete five-file base/head change and the five-commit round-2 delta, followed by published execution evidence. The round-2 changes affect the control, its documentation and explanatory comments. Generated workflow bytes are unchanged from c48bfe38.

Authorities: [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/748#issuecomment-6200705849), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/748#issuecomment-6203340834), [author source-head receipt](https://github.com/kebag-logic/milan-fpga/issues/748#issuecomment-6205012196), and [public execution packet](https://github.com/kebag-logic/milan-fpga/tree/8ed1c7b682059c1a97c191a756eb8b536098750d/review-evidence/748-r1).

The independent verdict and ledger were written before reading prior public review findings. Those findings were then reconciled against their causes, not adopted as technical authority. No private handoff, author scratchpad, other checkout or management source directory was read. The public author HANDOFF.md was not read either. Unchanged workflow and product artifacts retain their prior coverage; this round independently checks whether the delta invalidates it.

## Findings and prior-finding dispositions

### R637-1-F01 - RESOLVED - original MAJOR - Conformance, Robustness, Tests, Docs

Artifact: `scripts/ci_toolcache_isolation.py:321`, `:350`; `sw/builder/test_builder.py:29272`; `docs/testing/CI_WORKFLOWS.md:1437`.

Authority and required outcome: round-2 item 1 requires both patch checks to execute and pass. Missing or skipped checks cannot supply isolation evidence.

Evidence: `verify()` supplies `--receipt` to the actual builder driver. `checks()` requires a pass row with an empty NOT RUN list for each named check and also rejects nonzero process status. Missing receipts produce a no-receipt status for both names; the CLI prints those names. Missing rows are refused by their check name. Unreadable JSON stops with a nonzero error; it cannot produce ISOLATED.

Verification: `probe-delta.json` tests each absent row and each NOT RUN row independently, a missing receipt, a nonzero exit despite complete passing rows, and malformed JSON. The reviewer also ran only the two actual builder checks in a dependency-incomplete environment: the builder returned zero with two NOT RUN rows, and the production reader refused both by name (`missing-dependency-driver.log`, `.json`). This local fixture lacks the dependency set; it does not claim to be the complete patched installation.

The published CLI fixtures supply that complementary execution evidence: complete patched installations pass; removing only litex-boards fails by both check names, with and without patches; an available unpatched installation fails and writes no receipt. Fixture mutation bases identify the reviewed head, and their diffs alter the intended setup step. The retained `--shared` and base-workflow controls both fail, including a concurrent placement failure and 9296 changed cache paths. The original false-acceptance impact is closed.

### R637-1-F02 - RESOLVED - original MINOR - Robustness, Tests

Artifact: `scripts/ci_toolcache_isolation.py:372`, particularly `:394`; CLI help and `docs/testing/CI_WORKFLOWS.md:1456`.

Authority and required outcome: round-2 item 2 requires normalization before state is derived, or explicit rejection of relative input, with consistent documentation.

Evidence: all five scalar path options and every repeated --tool-dir are resolved before work-root use, revision resolution, planting, or Leg construction. The CLI and documentation explicitly accept both forms. --rev is resolved once to a commit before setup.

Verification: published full CLI runs `fixtures/head-relative.json` and `head-absolute.json` bind the exact head, both return zero, execute both patch checks in both legs, and preserve all 6303 cache paths. The reviewer checked every path option at the argument boundary in both forms and exercised actual CLI bad-revision refusal with relative and absolute --work; neither created a work directory. The original relative child-script failure is closed.

### R637-1-F03 - RESOLVED - original RESIDUE - Docs

Artifact: `.github/ci-templates/elaborate.yml:156`, `scripts/ci_toolcache_isolation.py:13`, `scripts/ci_events.py:569` and `:7457`.

Authority and required outcome: round-2 item 3 and the owner comment rule require the specified issue/requirement citations without changing generated commands.

Verification: all four explanations now carry `(#748; REQ-VER-04)`. The added source explanations state behavior and reason, without new bench labels, lane names, reviewer IDs, review rounds or issue-comment IDs. Generated workflow bytes equal c48bfe38; `ci_gate_workflows.py --check` returns zero. The attribution residue is closed.

### R636-1-F1 - RESOLVED - original RESIDUE - Conformance, Docs

Artifact: PR #749 body, Inventory table, `docs, rtl-fast, rtl` pip-install row, retained in `public-scope.json`.

Authority and required outcome: the original finding requested adding the omitted LiteX package installation to that row, without changing its correct private destination classification.

Verification: the row now explicitly includes “the LiteX pins in rtl-fast firmware-boundary.” The requested wording correction is present. No measurement or destination claim changes.

### R636-1-F2 - RESOLVED - original SUGGESTION - Tests

Artifact: `scripts/ci_toolcache_isolation.py:133`, `:197`, `:431`; `public-evidence/author-r2/evidence/round2/gate-legs/`.

Authority and required outcome: accepted as round-2 item 4: optionally execute both gate legs before the final cache manifest and publish the byte-equality receipt.

Verification: --gate-legs uses registered source dependencies at the selected revision, applies the job-budget environment, runs both workflow gate scripts concurrently, and waits for their completion before `manifest(cache)`. The final comparison includes the netlist-preservation steps. Omitted tail steps are named with reasons; nontext executable tail steps are refused by name. No full bank was rerun by the reviewer.

The published exact-head control receipt reports both legs at rc 0 (939.6 s and 408.0 s), 6303 planted paths, zero changes, and identical planted/final SHA-256 `871f9aea2b89f393b82fcd49ecb9aa6797cd669a75e5b3d601d74a5aba678d36`. Both driver receipts bind the exact head and tree. The reviewer fed those receipts to the repository union checker: 103 gates exactly once, requirements judged on the union, rc 0 (`author-builder-union.*`). The one recorded gate-11 calibration arm remains NOT RUN, with no hardware proof inferred. The requested evidence gap is closed.

## Independent lens evidence and reviewer-owned ledger

[R637] PASS Conformance - issue #748 assignments; `scripts/ci_toolcache_isolation.py:321,372,410` - all four round-2 requirements satisfied by source inspection, published positive/negative fixtures and focused falsification. The job-private workflow decision remains intact.

[R637] PASS RTL - `reviewed-paths.txt`, `.github/workflows/elaborate.yml:111,346`, `sw/builder/test_builder.py:22634`, `sw/litex/patches/apply.sh:32` - no HDL, firmware, product configuration, source pin, gitlink, patch-content or hardware-interface change. Interpreter selection and consumer ordering are unchanged. No clock, reset, CDC, protocol-field or product test-semantics change results from this delta.

[R637] PASS Robustness - `scripts/ci_toolcache_isolation.py:108,133,302,321,372`; `probe-delta.json`; public shared/dev controls - named refusal of skipped or absent checks; nonzero and malformed receipts fail closed; both path forms normalize; invalid revisions refuse before setup; setup failures prevent optional gate execution. Required concurrency and cache-difference controls remain effective.

[R637] PASS Tests - builder receipt producer `sw/builder/test_builder.py:29272`; `probe-delta.json`; published fixture diffs, gate-23h receipts and builder-leg receipts; `author-builder-union.json` - the actual builder can exit zero on skipped checks and the revised consumer now detects it. Complete and defective installations are distinguished. Both missing-check cases and both NOT RUN cases were independently probed. The post-leg cache comparison has executable evidence.

[R637] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1437`, control docstring/help, four cited source explanations, current PR body and public receipt packet - pass criteria, path forms, optional gate prerequisites and omitted steps match code. The physical calibration limitation remains explicit. No new wording residue was found.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen assignments; control:321,372,410; seven CLI fixtures; post-leg receipt | R637-2 | 2e83841675e4e1439c413c9ca11b4a123898a60e |
| RTL | CLEAN | Full base/head path inventory; unchanged generated workflow; builder:22634; apply.sh:32; pinned source identities | R637-2, delta applied over prior clean coverage | 2e83841675e4e1439c413c9ca11b4a123898a60e |
| Robustness | CLEAN | control:108,133,302,321,372; probe-delta.json; shared/dev negative controls | R637-2 | 2e83841675e4e1439c413c9ca11b4a123898a60e |
| Tests | CLEAN | Builder receipt producer; fixture mutation diffs; gate-leg and patch receipts; 20 focused checks; author-builder-union.json | R637-2 | 2e83841675e4e1439c413c9ca11b4a123898a60e |
| Docs | CLEAN | CI_WORKFLOWS.md:1437; CLI/docstring; template:156; ci_events.py:569,7457; PR inventory; public receipts | R637-2 | 2e83841675e4e1439c413c9ca11b4a123898a60e |

## Evidence integrity and reproducibility

`fetch_evidence.py` downloaded 70 selected public execution files at immutable publication commit `8ed1c7b682059c1a97c191a756eb8b536098750d`; every file matches its published SHA-256 manifest entry. Original and published hashes are distinguished where the publisher redacted paths. The publication commit is unsigned according to its verification metadata; no detached signature was supplied. This review verifies hashes and public provenance, not a cryptographic signer identity.

`audit_evidence.py` verifies seven fixture outcomes, their revision or mutation-base binding, the post-gate comparison, both exact-head builder receipts, both per-leg patch-check receipts, and all 46 rc-zero documentation gate rows. The published contract self-test excerpt reports all three #748 mutation arms caught and 5233 arms passing. These are author execution receipts, not reviewer or manager executions. Existing workflow cost evidence remains applicable because generated commands are unchanged; native setup measured 2.6 s per leg in the final post-gate receipt. This is not a new hosted wall-time measurement.

Reviewer commands, all foreground:

```sh
python3 -B <packet>/fetch_evidence.py
python3 -B <packet>/probe_delta.py <checkout>
python3 -B <packet>/audit_evidence.py
python3 -B scripts/ci_gate_workflows.py --check
python3 -B scripts/ci_builder_legs.py union --workflow elaborate \
  --head 2e83841675e4e1439c413c9ca11b4a123898a60e \
  --tree 4b1bed5825eae73757cb5368c71468c7d1d67d72 \
  --output <packet>/author-builder-union.json \
  <packet>/public-evidence/author-r2/evidence/round2/gate-legs/builder-leg-0.json \
  <packet>/public-evidence/author-r2/evidence/round2/gate-legs/builder-leg-1.json
python3 -B <packet>/verify_checkout.py <checkout>
```

All completed successfully. The union command reads receipts and the driver inventory; it does not execute the builder bank. The reviewer probes execute only the two selected dependency checks. No heavy build, native full bank or hardware tool was needed. Generated bytecode was removed. `checkout-integrity.json` verifies 1371 superproject blobs, bytes, modes and exact index entries, plus the four required registered submodules and all their pinned blobs/modes/index entries. Head and tree match the assignment; final status is empty. No source fix, commit, push, GitHub write, hardware access, container execution or host replay orchestration occurred. Disposable data is confined to packet scratch, which is excluded from publication.

## Real limits and pending manager duties

The [manager replay receipt at c48bfe38](https://github.com/kebag-logic/milan-fpga/pull/749#issuecomment-6204715936) reports 63 successful jobs and one skipped nightly-only physical job. It is evidence for that earlier head, not an exact-head replay receipt for this review. The workflow is byte-identical, but manager acceptance still requires the announced final-head replay.

The exact-head hosted snapshot contains six successful completed jobs, one skipped job, 20 running and 18 queued jobs. It is a point-in-time snapshot, not final acceptance. Skipped contexts are not counted as execution. The manager owns final hosted/replay acceptance; this review does not wait for or certify unfinished jobs.

There is no manager source bank at this head, and none is inferred. The published author source-head receipts are distinct from the current-dev merge-candidate evidence. At merge time the manager must construct and validate the candidate against then-current dev (supplied live tip `973e681be51882840670b8bc566f02b8005b1996`), publish its builder/native receipts and required hosted/replay results, settle the review completion bar, obtain maintainer merge authorization, and perform post-merge containment and issue/project closure. This source review cannot approve that future candidate in advance.

Physical calibration NOT RUN and field skips supply no hardware or release-campaign proof. Native controls model the shared cache with a local interpreter; they are not execution inside the hosted image. No full parent, processor, gPTP, portability or builder bank was rerun by the reviewer. Publication is restricted to REPORT.md and the files listed in MANIFEST.sha256.

R637-2 FINISHED
