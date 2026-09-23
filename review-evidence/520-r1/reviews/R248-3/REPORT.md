[R248] POSITIVE - exact head 2a77ace7d98cda18ece9f7aba9c4a408850eb926

Round R248-3: cleared-context composition review of issue #520 / PR #522 on the
merge-train candidate. Candidate `2a77ace7d98cda18ece9f7aba9c4a408850eb926`,
tree `7ea541fba2bab5f30708a2e62fa77b548a70c92f`, parents
`9912748d9c30f33a85056fcd1d836d3a4449cc69` (live dev + #439) and
`d253f86e410e301d146d4bd4e74d027f00cfb462` (this PR's published head).

The composed tree introduces no defect beyond the reviewed sources. No new
BLOCKER, MAJOR, MINOR or SUGGESTION. All five lenses are CLEAN. Prior findings
are dispositioned in section 6.

## 1. Reconstruction

Read in this order: `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`; the
issue #520 body (frozen acceptance 1-5, settled scope) and every issue comment;
the PR #522 body and the manager's comments; the #350/#520 contract in
`docs/testing/CI_WORKFLOWS.md`, `scripts/ci_events.py` and `syn/yosys/`. Then
`git diff 9912748d..2a77ace7` and the train history. Then the public merge-order
record on issue #415 and the PR #521/#525 file lists. Prior review reports
(R247-1, R248-1, R248-2) were read only after this round's verdict and ledger
were written.

## 2. Composition map (verified)

| Step | Commit | Content | Evidence |
|---|---|---|---|
| live dev | `776bc77d` | #372 merged (PR #518) | tree `1c2f365f` |
| train step 1 | `794e4834` | same tree as live dev | tree `1c2f365f` (equal) |
| train step 2 | `9912748d` | + #439 (PR #525, head `f01f237d`) | fresh `merge-tree` = `bcddb6c8`, recorded tree equal |
| candidate | `2a77ace7` | + this PR (head `d253f86e`) | fresh `merge-tree` = `7ea541fb`, recorded tree equal |

- The same tree reproduces from the actual live dev commit: `776bc77d` + `f01f237d` gives
  `bcddb6c8`, then + `d253f86e` over base `483a133e` gives `7ea541fb`
  (`receipts/merge-reproduction.txt`).
- The candidate changes 8 files against live dev, exactly the union of #439 (2 files) and
  this PR (7 files).
- **The one shared file is `docs/testing/CI_WORKFLOWS.md`, shared with #439.** No other PR
  in the candidate touches this PR's files.
- This PR's patch `9912748d..2a77ace7` has the same `patch-id --verbatim` as its source
  patch `483a133e..d253f86e`, per file and in total.
  - #439's step patch equals its source patch.
  - #439's `CI_WORKFLOWS.md` hunk equals `d253f86e..2a77ace7` on that page.
  - The two PRs edit disjoint hunks of the page (candidate lines, zero-context diff):
    #520 at 225-226 and 245-258, #439 at 783-809 and 942-946.
- Six of this PR's seven files are blob-identical to `d253f86e`, all but `CI_WORKFLOWS.md`.
  `scripts/ci_events.py` is blob-identical to `f01f237d`.
- `hdl/`, the three required gitlinks, `scripts/yosys_shards.py`,
  `scripts/processor_yosys_tops.budget` and `scripts/pp_srcs.py` are unchanged from
  `483a133e` to the candidate.
- **Brief label correction.** The overlap brief names "504". The candidate does not
  contain #504 (PR #521, head `5081a25a`). The predecessor sharing the page is #439.
  - This matches the public order on issue #415 (comment 5789520611): "#520 composes
    CI_WORKFLOWS.md with #439".
  - PR #521 changes `CI_WORKFLOWS.md`, `ci_events.py`, `docs.yml` and `elaborate.yml`
    (`receipts/pr521-files.tsv`). It is ordered after this PR, so its composition with
    #520 is its own review's duty. It is not covered here.

## 3. Semantic interactions examined

1. **#439 run-body content pins vs this PR's `rtl.yml` edit.** #439 pins every recognized
   run script in the seven RTL jobs, comment lines included. This PR's `rtl.yml` change
   (`rtl.yml:538-548`) is a YAML comment between steps, outside any `run:` body.
   - Probe P1 places the same kind of comment inside the `yosys-shards` run body.
     `ci_events --check` refuses it, naming `yosys-shards` step 9 and its canonical line.
   - Control P2 adds a between-step comment. It is accepted (1589 items).
   - So the interaction is real and the actual placement composes.
2. **The #350 policy marks on the paragraph this PR edited.** Probe P3 removes
   `` `syn/yosys/result_cache.py` `` from the composed paragraph. `ci_events --check`
   refuses it by the #350 mark.
3. **Contract and self-test populations.** `ci_events --check` reports 1589 items and
   `--selftest` reports 2135 arms at the candidate.
   - These equal #439's published source figures. `d253f86e` alone reports 1513 items
     (`receipts/differential/`).
   - So this PR adds no contract item and removes none. The #439 arms derived from live
     RTL steps see no changed step.
4. **Shared ratchets over the union of changed Python, shell and workflow files.** All pass
   at the candidate: Python idiom, shell idiom, hygiene, fail-fast (82<=84, 4<=4, 0<=0),
   test evidence (74<=77), TODO ownership.
   - The slack is in HDL-module and suite populations, which neither PR touches.
   - The per-side differential of these ratchets refuses in submodule-less scratch
     trees. That refusal is correct fail-closed behaviour, so per-PR attribution was not
     possible (section 8).
5. **Navigation and wording on the composed page.** `gen_toc --check`, `--verify-anchors`
   and `--selftest`, `docs_check` and `--selftest`, `check_doc_style`, `check_doc_paths`,
   `DOC_MAP.gen.py --check` and `check_baremetal_only` (whose regex covers
   `CI_WORKFLOWS.md`) all pass.
   - `check_em_dash` passes against the candidate parent (57 added lines), the source base
     (394) and live dev (88). One mirrored label is exempt.
6. **Prose consistency.** #439's text (step-list and content pins, "Action steps retain
   their recorded keys and `with` bindings") and #520's text (the ROM bundle in the cache
   key) describe different mechanisms. Neither restates the other.
   - The `rtl.yml` comment points to `syn/yosys/README.md` "The result cache". That heading
     exists at `README.md:90`.
7. **Classification.** `ci_scope.py` classifies the candidate's change set as RTL/tooling
   relevant against both live dev and `9912748d` (`receipts/ci_scope-candidate.txt`). The
   exhaustive aggregates must therefore execute on it, not skip.
8. **Merge-model probes P4-P6 (informational).** Replacing the shared page with either
   side's version, which drops the other PR's prose, passes `ci_events`, `docs_check`,
   `gen_toc` and `check_doc_style`.
   - No gate holds either PR's prose on this page.
   - Its composed correctness rests on the merge evidence in section 2, which is exact.

## 4. Gates run on the candidate (all exit 0)

The runner is `scripts/run_gates.sh`. Raw logs and `summary.tsv` are in `receipts/gates/`.
The scoped Verilator 5.050 was first on `PATH` (receipt 02). No command in this set
invokes RTL simulation or lint.

| # | Command | Result |
|---|---|---|
| 03-04 | `docs_check.py`, `--selftest` | 0 findings / 164 md + 834 files; 23+4 arms |
| 05-07 | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 707/707 arms; 144 links; 106 pages OK |
| 08-11 | `check_em_dash.py --base 9912748d` / `483a133e` / `776bc77d`, `--selftest` | 0 findings over 57 / 394 / 88 added lines; 57 arms |
| 12-13 | `check_doc_style.py`, `--selftest` | OK |
| 14-15 | `ci_events.py --check`, `--selftest` | 1589 items; 2135 arms PASS |
| 16 | `ci_scope.py --selftest` | PASS |
| 17-18 | `measure_fail_fast.py --check`, `--selftest` | PASS; 106/106 |
| 19-20 | `check_hygiene.py --check`, `--selftest` | PASS (712 files); 35/35 |
| 21-22 | `check_py_idiom.py`, `--selftest` | within budget; 54/54 |
| 23-24 | `check_sh_idiom.py`, `--selftest` | within budget; 48/48 |
| 25-26 | `check_todo_ownership.py`, `--selftest` | OK (762 files); 45/45 |
| 27-28 | `measure_test_evidence.py --check`, `--selftest` | PASS; 101/101 |
| 29 | `check_doc_paths.py` | 833 cited paths resolve |
| 30-31 | `check_baremetal_only.py --check`, `--selftest` | 0 findings; 342 arms |
| 32 | `docs/DOC_MAP.gen.py --check` | OK |
| 33-35 | `check_archive.py`, `check_feature_status.py`, `--self-test` | OK; 0 findings |
| 36-37 | `pp_srcs.py --check`, `--selftest` | 42 derived sources; self-test passed |
| 38-39 | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 45/45; 18/18 |
| 40 | `syn/yosys/result_cache.py --selftest` | OK (key, hit-rule/trust, ROM bundle and schema controls) |
| 41 | `syn/yosys/rom_cache_selftest.py` | import check only: a library with no entry point, called at `cache_selftest.py:136` |
| 42 | `syn/yosys/cache_selftest.py` | OK: 5 original live arms + ROM controls (3 images, 2 modes, 2 tops, head/seed, generation and schema refusals), real `run.sh`, 53 s |
| 43-44 | `git diff --check 9912748d HEAD`, `483a133e HEAD` | clean |

## 5. Probes

The probes are in `scripts/probes.py`, with results in `receipts/probes/`. They ran on a
disposable clone of the candidate. Each probe was restored and proved clean before the
next. No commit was made.

| Probe | Mutation | Gate | Expected | Exit |
|---|---|---|---|---|
| P0 | none | `ci_events --check` | accept | 0 |
| P1 | comment inside the `yosys-shards` run body | `ci_events --check` | refuse | 1 (content pin, step 9) |
| P2 | extra comment between steps | `ci_events --check` | accept | 0 |
| P3 | drop the `result_cache.py` mark from the composed paragraph | `ci_events --check` | refuse | 1 (#350 mark) |
| P4 | shared page from `d253f86e` (no #439 prose) | `ci_events --check` | info | 0 |
| P5 | shared page from `f01f237d` (no #520 prose) | `ci_events --check` | info | 0 |
| P6 | as P5 | `docs_check`, `gen_toc --check`, `check_doc_style` | info | 0 |

## 6. Findings

No new finding at this head.

Prior public findings, read after sections 1-5 and the ledger were written:

| Finding | Round, severity, lens | Disposition at `2a77ace7` | Evidence |
|---|---|---|---|
| F1: two cache-key summaries state the pre-#520 key as enough for a skip | R248-1, MINOR, Docs | **RESOLVED** (unchanged from R248-2) | `README.md:27` and `rtl.yml:538-541` name the ROM bundle and point to the key definition. Both files are blob-identical to `d253f86e`. `gen_toc --check`, `docs_check`, `check_em_dash` and `ci_events` pass at the candidate. |
| SG1: message-less asserts; a non-AssertionError escapes `run_arms` | R248-1, SUGGESTION, Tests | RETAINED (optional) | `rom_cache_selftest.py` and `cache_selftest.py` are blob-identical to the source |
| SG2: no control pins the schema advance | R248-1, SUGGESTION, Tests | RETAINED (optional) | `result_cache.py:52` still reads `SCHEMA = "milan-yosys-result-cache/2"` |
| SG3: rtl-fast step comment lists only the original arms | R248-1, SUGGESTION, Docs | RETAINED (optional) | `rtl-fast.yml:219-222` is unchanged (blob-identical to the source) |
| S1: empty-image arm cannot tell run.sh's refusal from the digest helper's | R248-2, SUGGESTION, Tests | RETAINED (optional) | `rom_cache_selftest.py:212-214` is unchanged |
| none | R247-1, POSITIVE | nothing to resolve | - |

The out-of-scope notes of R248-1 and R248-2 are untouched by the composition:
48-top prose against the 54-top inventory, the Yosys techlib data outside the key,
and forgery inside a writable tier. Line citations are in
`receipts/prior-findings-at-head.txt`.

## 7. Lens results and reviewer-owned ledger

```text
[R248] PASS Conformance - docs/testing/CI_WORKFLOWS.md:225-226,245-258,783-809,942-946; .github/workflows/rtl.yml:538-559; scripts/ci_events.py (f01f237d blob); receipts/gates/14,15,40,42; receipts/probes/P1-P3 - the #439 CI contract (1589 items) holds this PR's workflow and policy edits at the candidate; #520 acceptance-5 commands pass on the composed tree; syn/yosys byte-identical to the reviewed source
[R248] PASS RTL - receipts/merge-reproduction.txt; git diff 483a133e..2a77ace7 over hdl/, gitlinks, yosys_shards.py, processor_yosys_tops.budget, pp_srcs.py (empty); syn/yosys/run.sh blob = d253f86e - the composition touches no RTL-scope artifact; coverage stands on the source rounds
[R248] PASS Robustness - syn/yosys/{run.sh,result_cache.py,rom_cache_selftest.py} blobs = d253f86e; receipts/gates/42 (generation-failure, missing/empty image, legacy/malformed entry arms on the real run.sh at the candidate) - the composition touches no Robustness-scope artifact; controls re-executed green
[R248] PASS Tests - receipts/gates/15,40,42,18,20,22,24,26,28; receipts/probes/P1,P3; receipts/differential/summary.tsv - the self-test populations the two PRs share (ci_events arms derived from live RTL steps) are unchanged by composition (2135 = #439 source); shared ratchets pass; interaction points proved able to fail
[R248] PASS Docs - docs/testing/CI_WORKFLOWS.md (both hunks, patch-id equal to their sources); syn/yosys/README.md:27,90; rtl.yml:538-541; receipts/gates/03-13,29,32; receipts/probes/P4-P6 - composed page carries both PRs' prose verbatim, consistent, navigable and wording-clean
```

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | shared policy page and #439 contract vs this PR's `rtl.yml`/page edits; acceptance-5 commands; probes P1-P3 | R248-3 | `2a77ace7d98cda18ece9f7aba9c4a408850eb926` |
| RTL | CLEAN | composition touches no RTL-scope artifact (HDL, gitlinks, inventory inputs and `run.sh` unchanged or blob-identical) | source rounds R248-2 and R247-1 (`28e350b9`, scope unchanged through `d253f86e`); scope confirmed untouched by R248-3 | `d253f86e410e301d146d4bd4e74d027f00cfb462` (ancestor of the candidate; lens scope byte-identical at `2a77ace7`) |
| Robustness | CLEAN | composition touches no Robustness-scope artifact; refusal arms re-executed on the candidate | source rounds R248-2 and R247-1; re-exercised by R248-3 | `d253f86e410e301d146d4bd4e74d027f00cfb462` (ancestor; scope byte-identical at `2a77ace7`) |
| Tests | CLEAN (SG1, SG2, S1 are suggestions) | shared `ci_events` populations; cache self-tests; shared ratchets; probes | R248-3 | `2a77ace7d98cda18ece9f7aba9c4a408850eb926` |
| Docs | CLEAN (SG3 is a suggestion) | `CI_WORKFLOWS.md` composition; README and `rtl.yml` pointers; docs, TOC, anchor, em-dash, style and path gates | R248-3 | `2a77ace7d98cda18ece9f7aba9c4a408850eb926` |

## 8. Real limits and pending manager duties

- **No hosted evidence exists at the candidate.** `2a77ace7` is not on the remote: the
  check-runs query returns 422.
  - At the PR head `d253f86e` (run 35822881606, `pull_request`), all seven required
    contexts are SUCCESS, with 5 Verilator and 4 Yosys workers executed. The nightly and
    manual physical gPTP leg is skipped.
  - Those Yosys workers served all 54 tops from the result cache (1+1+26+26, no refusals).
    The cache was restored from key `...-4d2246ba`, the merge ref of this PR's earlier
    head `28e350b9` onto `483a133e`. That is valid reuse under #350, but it is not live
    synthesis. That run's merge ref did not contain #439.
  - The manager owns exact-head hosted and act acceptance for the final candidate.
- **The manager's full source static/builder and native banks for this head are not
  claimed or inferred here.** No full parent, PP, gPTP, Yosys or builder bank was run.
  No trusted replica or its self-test was run.
- **Local tools differ from CI.** This host has Yosys 0.66 (distribution build) and sv2v
  v0.0.13; CI pins sv2v v0.0.12. `cache_selftest.py` compares runs only within this host.
- **Ratchet attribution.** The per-side differential of the submodule-dependent ratchets
  refused, correctly, in scratch trees without submodules. Only candidate-level passes are
  claimed.
- **The shared page's prose is not machine-held (P4-P6).** If the tree built at the merge
  turn differs from `7ea541fb`, the shared page must be re-verified.
  - The candidate's first-parent chain uses `794e4834`, which is tree-equal to live dev
    `776bc77d` but is not that commit. The tree reproduces from the real live dev commit.
- **Later composition is not covered.** #504 (PR #521) is ordered after this PR and
  touches `CI_WORKFLOWS.md` and `ci_events.py`.
- **Pending manager duties:** the final current-dev candidate at the merge turn; its
  exact-head hosted and act evidence; the two-positive bar; authorized merge; post-merge
  containment; Closed/Done.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- **Clone integrity.** After all runs, the clone holds the exact head bytes:
  `receipts/integrity-final.txt` shows HEAD, tree and index; 858 tracked files by bytes
  and mode; three stage-0 gitlinks at their pins with clean checkouts; nothing untracked
  or ignored.
  - A bytecode cache created by one gate during the run was removed. That gate ran an
    isolated interpreter, which ignores the no-bytecode setting.

R248-3 FINISHED
