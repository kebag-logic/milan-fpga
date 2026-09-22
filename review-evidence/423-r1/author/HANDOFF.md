# A171 factual implementation handoff: issue 423

Author work is stopped at `fed4f63f33e6185e5c7e4735a27234db99651d24`. This is evidence, not approval.

## Identity and state

- Lane: `$CANDIDATE`.
- Branch: `423-retained-redundant-replay`.
- Starting dev: `88e9276b2a220c716f64a843f7e1eb8f9265e896`.
- Commit: `fed4f63f33e6185e5c7e4735a27234db99651d24`.
- Tree: `330afc6078441daf4d6a59d5dc760303a501477f`.
- One-line commit: `Prove retained replay across one exact redundant merge`.
- Working/index status: clean. No push or PR mutation performed.
- Manager A10; independent cleared internal R243 Codex and external R244 Opus reserved.
- Tools: Git 2.55.0; Python 3.14.7. Recorded gate processes inherited an eight-CPU affinity cap, OMP_NUM_THREADS=8 and MAKEFLAGS=-j8. Fixtures, history checks and mutations are serial within each command.
- `receipts/final-state.json` records branch, objects, submodule state and scoped sizes.

## Implemented contract

The new final arm is G1 + H + T from [the settled decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218).

G1 admits exactly one source-only merge. It must have two ordered parents, the second parent's only parent must be the first, and the merge tree must equal the second-parent tree. No distant-parent, octopus, additional-merge or resolution generalization was made.

H calls the existing `_linear_patches_contained` helper: distinct whitespace-exact patch matches plus touched-path postimage identity. Its matching algorithm and the pre-existing containment-arm order remain unchanged. The shared Git transport now decodes bytes with surrogateescape without universal-newline conversion, and feeds patch-id the encoded raw patch. This is needed for CRLF/literal/non-UTF-8 controls; it changes no historical-policy selection. All 145 prior assertions retain identical output and order. The old content and scratch test modules are byte-identical to the starting commit.

T requires one merge base. It enumerates source net-changed paths with renames unfolded, reads literal raw entries, and accepts exact tip/source mode/kind/OID identity, including absence. Otherwise tip/source must be regular blobs, the ancestor regular or absent, with the selected mode rule. Raw `git merge-file` must exit 0 and emit exactly the current tip bytes. No resolver choice, attribute, driver, textconv or normalization supplies proof. Failed measurements and unproved paths produce UNKNOWN/1 after successful historical proof. G1/H rejection falls through to the existing result.

The checker docstring, UNKNOWN footer and CONTRIBUTING now distinguish historical replay, current retention and unresolved overlap. #514 retains ownership of any change to the existing linear policy. No RTL, firmware, pins, hardware or workflow scheduling changed.

## Default self-test evidence

`rtk proxy python3 scripts/check_merge_containment.py --selftest`

Final head: exit 0, **326/326 assertions**, 17.479 seconds. Raw stdout/stderr/command/state are `receipts/final-selftest.*`.

| Population | Assertions | Scope |
|---|---:|---|
| Original | 145 | Exact same names, order and text; original content/scratch modules unchanged |
| Public matrix | 44 | 31 verdict/exit comparisons, two positive new-arm proof checks, eleven historical/unproved-path evidence checks |
| Mutations | 25 | Ten guards, all public killing cases; both verdict and exit asserted |
| Retention boundaries | 112 | Types, modes, absence, literal/non-UTF-8 paths/blobs, CRLF, repeated blocks, command/object errors, hostile config, SHA-256 |
| New total | 181 | All invoked by the existing default containment self-test owner |

`scripts/run_all_suites.sh` already owns the checker `--selftest`; no registration or workflow change is required. The full parent suite was not run by this author.

Boundary histories use actual Git trees and distinct original/replay commits. Every new accepted case also checks the new arm's retention proof text, preventing a pass through an unrelated pre-existing arm from covering it. The repeated-block set has sixteen real histories spanning 2/3/5/8 blocks, replacement/deletion, retained append and partial restoration. A separate raw merge probe exercised **11,256** two-deletion/one-restoration-plus-append combinations and found zero false no-op acceptances. The final probe includes a successful positive control, rejects command errors, and records 7,876 conflicting plus 3,380 clean changed-output negative merges. That probe is `scripts/probe_alignment.py`, with final raw output `receipts/final-alignment-probe.stdout` (plus the earlier `receipts/alignment-probe.log`); it is bounded support, not a general proof.

An invalid `merge.conflictStyle` is validated by Git before the final override and makes merge-file exit 128. Its final control expects UNKNOWN even for otherwise retained bytes. The positive hostile-config control remains present with valid diff3 configuration. This implements the decision's unmeasurable-failure rule; no acceptance criterion was weakened. Development receipts showing the initially incorrect positive expectation are retained separately.

## Public fixture and history reproductions

Run from the lane:

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-author/scripts/reproduce_public.py $CANDIDATE
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-author/scripts/reproduce_history.py $CANDIDATE
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-author/scripts/audit_mutations.py $CANDIDATE
```

Use `scripts/run_receipt.py <receipt-name> <command...>` to capture outputs and enforce the CPU cap. The delivered packet includes immutable public fixture scripts and baseline checker copies. `reproduce_history.py` reads the disposable bare donor mirror at `donor.git`; recreate it if omitted from an archive with:

```sh
rtk proxy git -c maintenance.auto=false clone --mirror https://github.com/Mister-M-alt/FPGA-gPTP.git $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-author/donor.git
```

The public R242 scripts are from commit `badb350c0892fd5a6c771f24943463c9b1440c24`. All 12 selected downloaded blobs re-hash to their recorded Git object IDs; `receipts/public-input-verification.json` records them. The public fixture builder is unchanged; only its diagnostic helper-interface adapter is replaced by the production interface. It reproduces **31/31 outcomes and all 31 original head/tip OID pairs**. The author test builders are adapted from those public factual fixtures, while the production proof is a separate 158-line implementation, not the prototype copied unchanged.

Public original/replay pairs and raw diff SHA-256 values:

| Original | Replay | SHA-256 |
|---|---|---|
| `3db86812096830fada2f5f276fa5f4d9f37d1d14` | `5602e70bb4cf70c2e0e39e846e26925e27659e32` | `fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f` |
| `9790ac736e6d10301ad814ffdf73dbe37b59768b` | `20927af74752620b2ad0f973e8be3203994b5547` | `d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3` |

The reproduction hashes `git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>` output bytes. The pairs' raw patches and verbatim patch IDs agree.

| Public case | Baseline | Final production |
|---|---|---|
| PR62 at `f0f1c055ee5226f08e656c27cb1bf4c355be11ae` | STRANDED/1 | UNKNOWN/1 |
| PR62 at `c1b617435824929a790739ea8585c3fe1a328cc0` | STRANDED/1 | UNKNOWN/1 |
| PR61 at both targets | Existing historical policy | contained/0 |
| Published adjacent extension | Historical proof only | UNKNOWN/1 |
| Published replay then exact reversion | Historical proof only | UNKNOWN/1 |

Both PR62 results name `tb/tsngen/mutants.py` and `tb/verilator/gaskets/mutants.py`. The other three net-changed paths have identity/no-op retention. See `receipts/pr62-history.json`, `receipts/published-probe.json`, and `receipts/final-public-history.*`. This clears no donor sweep or processor-pin prerequisite.

## Per-guard mutation evidence

`receipts/final-guard-mutations.json`: exit 0, final head/tree, 35.689 seconds. `receipts/mutations-matrix.json` retains every output from **341 CLI runs**: baseline plus ten mutants, each across all 31 public histories. The changed-case set must equal the public expectation, not merely be nonempty. All ten guards were killed.

| Weakened guard | Changed public cases: verdict/exit |
|---|---|
| merge-count | 3: STRANDED/1 -> contained/0 |
| parent-count | 25: STRANDED/1 -> contained/0 |
| direct-parent | 28: STRANDED/1 -> contained/0 |
| merge-tree | 21: STRANDED/1 -> UNKNOWN/1; 22: STRANDED/1 -> contained/0 |
| historical-proof | 17: STRANDED/1 -> UNKNOWN/1; 18: STRANDED/1 -> UNKNOWN/1; 19: STRANDED/1 -> UNKNOWN/1; 20: STRANDED/1 -> UNKNOWN/1 |
| retention-proof | 6: UNKNOWN/1 -> contained/0; 7: UNKNOWN/1 -> contained/0; 8: UNKNOWN/1 -> contained/0; 9: UNKNOWN/1 -> contained/0; 10: UNKNOWN/1 -> contained/0; 11: UNKNOWN/1 -> contained/0; 12: UNKNOWN/1 -> contained/0; 13: UNKNOWN/1 -> contained/0; 14: UNKNOWN/1 -> contained/0; 15: UNKNOWN/1 -> contained/0; 16: UNKNOWN/1 -> contained/0 |
| exact-only | 1: contained/0 -> UNKNOWN/1; 2: contained/0 -> UNKNOWN/1 |
| mode-rule | 10: UNKNOWN/1 -> contained/0 |
| tip-byte-equality | 14: UNKNOWN/1 -> contained/0 |
| merge-error | 11: UNKNOWN/1 -> contained/0 |

## Selected repository gates

Run `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-author/scripts/run_gates.py` from the lane to repeat this bounded batch. Every row below exited 0 on staged tree `330afc6078441daf4d6a59d5dc760303a501477f`, subsequently committed unchanged as `fed4f63f33e6185e5c7e4735a27234db99651d24`. `receipts/final-state.json` independently checked the batch's recorded source-byte hashes against the final checkout.

| Command | Exit | Receipt prefix |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs-checked-tree` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc-checked-tree` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom-checked-tree` |
| `python3 scripts/check_hygiene.py --check` | 0 | `hygiene-checked-tree` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `fail-fast` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence` |
| `python3 scripts/check_todo_ownership.py` | 0 | `todo-ownership` |
| `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal` |
| `python3 scripts/check_feature_status.py --self-test` | 0 | `feature-status` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths` |
| `python3 scripts/check_archive.py` | 0 | `archive` |
| `python3 scripts/pp_srcs.py --check` | 0 | `pp-sources` |
| `python3 scripts/check_soc_sources.py` | 0 | `soc-sources` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `source-lists-checked-tree` |
| `python3 scripts/check_port_contracts.py` | 0 | `port-contracts` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom` |
| `python3 scripts/check_sh_idiom.py` | 0 | `sh-idiom` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint-rtl` |

Additional receipts: `toc-selftest` (0), `toc-anchors` (0), `py-idiom-selftest` (0), `hygiene-selftest` (0), and `em-dash` (0 at the final head against starting dev). `git diff --cached --check` also exited 0 before commit. The lint gate reports its existing 90 findings within the unchanged ratchet, not zero historical lint debt. No budget file changed.

| Module | Lines | Longest function |
|---|---:|---:|
| `scripts/check_merge_containment.py` | 996 | 74 |
| `scripts/merge_containment_replay.py` | 158 | 22 |
| `scripts/merge_containment_selftest.py` | 918 | 93 |
| `scripts/merge_containment_selftest_mutations.py` | 66 | 24 |
| `scripts/merge_containment_selftest_replay.py` | 592 | 25 |
| `scripts/merge_containment_selftest_retention.py` | 258 | 30 |

## Acceptance and limits

AC1-3 have local implementation evidence. AC4 is pending the manager's full bar and independent exact-head reviews. This handoff does not provide a reviewer verdict or bank any review lens.

Only Git 2.55.0/Python 3.14.7 were exercised here, including real SHA-1 and SHA-256 histories. The minimum-Git refusal remains covered by the original tests. No general xdiff alignment proof, arbitrary semantic-rewrite equivalence, large-file/resource ceiling or exhaustive platform/version matrix is claimed. The H scan retains its existing cost; T performs bounded-per-path subprocess operations but has no new global large-repository performance guarantee. Conflicting/overlapping edits, different special-file entries, invalid configuration and missing/error measurements remain nonzero. Binary identity can pass; differing binary content remains unresolved.

No control produced a false acceptance contradicting the selected criterion. Public PR62, the published adjacent extension, arbitrary overlapping rewrites and unrelated shape extensions remain unresolved. Existing linear historical semantics are deliberately asymmetric and remain #514's work.

## Manager-owned remaining work

Archive the factual packet and raw receipts; push the exact head and create/update the PR; run the complete native bar, trusted act replicas, mandatory hosted contexts and current candidate validation. Obtain cleared R243/R244 reviews and a reviewer-owned final lens ledger, resolve findings, obtain merge authorization, then perform post-merge containment and issue/project closure. No full parent Verilator/Yosys or processor/native-builder rerun, Docker/act, install, privilege, hardware, push, PR metadata action, merge or delegation was performed by A171.

`REVIEW-READY.md` is the factual issue comment. `PR-BODY.md` is a draft for the manager. Development receipts with earlier failed wording/formatting or invalid-configuration expectations are retained and are not counted as final gate passes. All material final commands carry their explicit exit and measured object context in the selected receipt JSON.
