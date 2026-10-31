[R747] POSITIVE - exact head 125ac68006d124dd149b9161539dfaa787166e62

# R747-5: composition review of PR #820 (#818) on the merge-train candidate

- **Candidate:** `125ac68006d124dd149b9161539dfaa787166e62`, tree `1aff472e57f4e4b08238e985e678f5d2a8780729`.
- **Parents:**
  - `7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c`: live dev `02ca829a` plus the queued predecessor PR for #814.
  - `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`: PR #820's source head, tree `afee23b5`.
- **Merge base of the two parents:** `02ca829ad821f4233ab66f59978c65d3c3c9de70`.
- **Source reviews at `81f78a81`:** R747-4 POSITIVE (issuecomment-6543583892) and R748-3 POSITIVE (issuecomment-6543597130).
- **Composition head reviewed last:** `ffe3a631`, by R747-3, which was NEGATIVE with F1 (MINOR).
- **Scope:** composition acceptance only.

**Verdict basis.**
- **The candidate is a pure file-disjoint union.** Each file the PR changes is byte-identical to the source head. Each file the predecessor changes is byte-identical to the first parent. The merge adds no bytes of its own.
- **R747-3 F1 is resolved.** The fix is at the source head and is carried into the candidate unchanged.
- **The shared-surface gates pass on the candidate.** That covers the docs, TOC and anchor, em dash, CI event contract, hygiene, Python idiom and evidence-pin gates.
- **The #818 gate passes on the candidate.** Its self-test, mutant campaign and baseline audit all pass.
- **The signed local-CI packet verifies.** It names this candidate and this head.
- **No new finding.**

## Composition identity (receipts/composition_identity.txt)

**Files the PR changes** (merge base to `81f78a81`, 11 files):
- `CHANGELOG.md`
- `docs/design/{AREA_BUDGET,MARK_II_AREA_PLAN}.md`
- `docs/integration/BUILDING.md`
- `docs/reference/SUBMODULES.md`
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`
- `syn/ooc/pp_placement_selftest.py`
- `syn/ooc/pp_resource_gate{,_mutants,_selftest,_set_selftest}.py`

**Files the predecessor changes** (merge base to `7f4d7eea`, 6 files):
- `ci/image/exec-audit.json`
- `docs/litex/CLOCK_DOMAINS.md`
- `docs/testing/TESTING.md`
- `scripts/run_litex_sims.sh`
- `sw/litex/milan_soc.py`
- `sw/litex/test_soc_timing_cuts.py`

**Textual overlap: none.**
- `git diff 7f4d7eea..125ac680` lists exactly the 11 PR files.
- `git diff 81f78a81..125ac680` lists exactly the 6 predecessor files.
- Every blob equals its own side.

**Gitlinks.** The six submodule gitlinks are identical at the parent, the source and the candidate (receipts/gitlinks.txt, receipts/submodule_status.txt).

**Workflows.** The four workflow definitions hash the same at the head and at the candidate. The candidate hashes match the manifest's `definitions` (bdf72c62…, 4b6018fd…, 47656c6f…, 11c833ab…).

**Semantic interactions examined:**
- **`ci/image/exec-audit.json` (predecessor only).** The predecessor adds one generated-program entry from `scripts/run_litex_sims.sh`. It does not interact with the #818 generators, `pp_resource_gate_mutants.py` and `pp_placement_selftest.py`. L1 covers the inherited question of stale digests.
- **`docs/testing/TESTING.md` and `docs/litex/CLOCK_DOMAINS.md` (predecessor only).** These describe the SoC `sys`-path timing cuts. The #818 prose describes the processor resource gate's route-set rule. No #818 page links into the predecessor's new text, and the anchor check reproduces all 544 cross-page fragments.
- **Route-WNS wording.**
  - The predecessor's TESTING.md:722-723 refers to "the SoC's `sys` paths that set the route WNS".
  - `docs/design/AREA_BUDGET.md:149-150` names the bridge-to-PHY-counter path of the recorded route, and #814 restages that path. Neither side changed those lines (`git blame`: `ca39dc1b0`, 2026-10-28).
  - #818's own lines (`:144-146`) state the gate rule and the #806 fall. They do not contradict the predecessor's text.
  - Refreshing that critical-path sentence after a new route is measured belongs to the #814 line of work, not to this composition (see pending duties).
- **Gate inventories and CI event contract.** Neither side changes a workflow file, and `ci_events.py --check` and `--selftest` pass. The `scripts/run_litex_sims.sh` INVENTORY gains `test_soc_timing_cuts` on the predecessor side only.
- **`CHANGELOG.md`.** Only the PR changes it, so no section collides.

## Signed local CI packet (receipts/localci, receipts/signed_packet_verify.log, scripts/verify_signed_packet.sh)

- **`manifest.json`.** Its sha256 is `9433c3860a1f70bdbe815051af87a38d301938763f8526d7ebfb2f4596da6102`, as stated.
- **(1) Key.** `allowed_signers` holds one ED25519 key with fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. Its principal and namespace are both `milan-local-ci`. This is the required key.
- **(2) Signature.** `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` printed `Good "milan-local-ci" signature` and exited 0.
- **(3) Subject.**
  - Candidate `125ac680…`, tree `1aff472e…`, parent `7f4d7eea…`.
  - Head `81f78a81…`, tree `afee23b5…`.
  - PR 820, `result` success.
- **(3) Coverage.**
  - All 47 coverage entries are `ok: true`.
  - 46 entries are `by: act`.
  - One entry is `by: not-run`: `rtl/physical-gptp`. Its stated reason is that the job runs only on schedule or dispatch; act shows it skipped.
- **Act jobs.** Every act job is `success` except that skipped job.
- **Banks.** The `full-native` and `manager-builder` banks record exit 0.
- **What this packet is not.** It is the manager's local evidence for the candidate. It is not a manager source bank at this head, and this round infers none.

## Executed evidence at the candidate (receipts/SUMMARY.txt; scripts/composition_gates.sh)

Every gate below exited 0.

**Documentation gates:**
- `docs_check.py`: 0 findings over 210 Markdown files.
- `check_doc_style.py`: OK.
- `check_doc_paths.py`: OK, 1075 cited paths.
- `check_submodule_docs.py`: OK, 6 exact gitlinks.

**TOC gates** (run with the pinned Markdown renderer environment):
- `gen_toc.py --check`: 149 pages.
- `gen_toc.py --verify-anchors`: 544 fragments.
- `gen_toc.py --selftest`: 1501/1501 arms.

**Em dash gate:**
- `--base 7f4d7eea`: 0 findings over 73 added lines in 6 pages.
- `--base 02ca829a`: 0 findings over 114 added lines in 8 pages.

**CI contract and ratchets:**
- `ci_events.py --check`: 2199 items.
- `ci_events.py --selftest`: 5258 arms.
- `check_hygiene.py --check`, `check_py_idiom.py` and `generate_ci_evidence_pins.py --check`: pass.

**#818 gate:**
- `pp_resource_gate.py --selftest`: 312 arms and 500 generated cases PASS, and the placement gate passes (`gate_selftest_documented.log:391`). The issue's four planted cases each pass with their expected exit (`gate_selftest.log:232-235`).
- `pp_resource_gate_mutants.py`: the control passes and all 236 mutants fail.
- `pp_resource_gate.py check-baseline`: PASS on 3 endpoints.

**Harness note.** My first attempt ran these gates in the interpreter's isolated mode. That mode drops the script directory from the import path, so the imports failed. The fault was in my invocation, not in the candidate. The reruns above use the workflows' own form, `python3 <script>`. Three host-side inventory checkers need the CI image environment, so they do not apply on the host and their receipts were dropped: `ci_command_table.py`, `ci_tool_inventory.py` and `check_results_fresh.py`.

**Restore.**
- Interpreter caches were removed after the runs.
- `git status --short --ignored` is empty, and the index and worktree are clean.
- `git write-tree` gives `1aff472e…`, and HEAD is `125ac680…`.
- The gitlinks are as listed above.

## Findings

**No new finding at this head.**
- The composition adds no bytes, so it adds no source comment and no new RESIDUE.
- I scanned the PR's added lines for lane, round, reviewer and comment-ID labels. The scan is empty.

### L1 (a limit, not a finding): exec-audit digests for the #818 generators

The file is `ci/image/exec-audit.json`.

**What I found.** The candidate's reviewed list carries:
- 173 entries generated by `syn/ooc/pp_resource_gate_mutants.py`;
- 72 entries generated by `syn/ooc/pp_placement_selftest.py`.

#818 changes both generators and `pp_resource_gate.py`, and the campaign now runs 236 mutants. So these entries plausibly hold pre-#818 digests.

**Why it is not a finding.**
- The population audit is image-level and is not yet wired into PR replay (`docs/testing/CI_IMAGE.md:600`).
- The gap is inherited from the source head; the composition did not create it.
- The predecessor touches this file with one unrelated entry only.
- It is outside composition scope, and the audit needs Docker, so I did not run it.

**Routing.** It is listed under the pending manager duties.

## Prior public review findings (read after the independent pass)

| Prior finding | Status at `125ac680` | Evidence |
|---|---|---|
| R747-3 F1 MINOR (Docs, Conformance): the composed tree said the gate refuses the #806 route's 0.408 ns fall | **RESOLVED** | `docs/design/AREA_BUDGET.md:144-145`: "Before #818 the gate refused that fall; under #818 it prints a WARNING and passes". Also `docs/reference/SUBMODULES.md:421-425` and `CHANGELOG.md:75-76`. All three blobs are identical to `81f78a81`, which R747-4 and R748-3 reviewed. On the candidate the gate prints the WARNING and passes (`gate_selftest.log:234`). |
| R747-3 OBS-1 SUGGESTION (Tests, Docs): `ci/image/command-table.json:13944-13957` pins pre-#818 content | **RETAINED**, optional, not composition-introduced | The pins are still `425bfc9e…`, `71a4a2f2…` and `9e0ddcd0…`, the merge-base digests. The candidate's files are `2a056c60…`, `a6c1b4ee…` and `c7e6082f…`. `pp_resource_gate_set_selftest.py` has no declaration. |
| R748-1 F1, F2, F3 MINOR | **RESOLVED**, unchanged by composition | `MARK_II_AREA_PLAN.md` and `pp_resource_gate.py` are byte-identical to the source. The self-test arms and the 236-mutant run pass on the candidate. |
| R748-1 R1 RESIDUE (PR body mutant claim) | **RESOLVED** (per R747-2 and R748-2) | No change by composition. |
| R748-1 S1 SUGGESTION (`bound()` sub-conditions) | Ceiling part **RESOLVED**; `bound()` part **RETAINED**, optional | Gate bytes unchanged. |
| R747-1, three SUGGESTIONs: fuzz on marked routes only, selection by WNS only, stale comparison directory | **RETAINED**, optional | Gate, self-test and recipe bytes unchanged. |
| R747-2 RS1 RESIDUE: PR body "Round 2 mutants, each killed by the arm written for it" | **RETAINED** as RESIDUE | Still present at `receipts/pr820_body_at_review.md:89`. The exact fix is as stated in R747-2. |
| R748-2 R2 RESIDUE: the PR body's file table has stale arm and mutant counts | **RETAINED** as RESIDUE | `receipts/pr820_body_at_review.md:76` says "38 new mutants, 11 rewritten", while `:19` says "44 new and 11 rewritten". The exact fix is to make `:76` agree with `:19` and with the campaign's 236 (per R748-2). |

## Lens results (clean lenses in findings format)

- `[R747] PASS Conformance - docs/design/AREA_BUDGET.md:144-146, receipts/gate_selftest.log:232-235, receipts/gate_check_baseline.log, receipts/composition_identity.txt - the #818 frozen acceptance (four planted cases, docs gates) holds on the composed tree; the composition changes no #818-scope byte; the F1 prose agrees with the gate's WARNING-and-pass behaviour.` The predecessor did not touch the acceptance item that #814 round 1's recorded routes select ExtraPostPlacementOpt, which is a record-side claim. R747-4 and R748-3 covered it, and `check-baseline` passes here.
- `[R747] PASS RTL - receipts/gitlinks.txt, receipts/composition_identity.txt - neither side changes HDL; the six gitlinks are identical at parent, source and candidate; the predecessor's SoC Python (sw/litex/milan_soc.py) is disjoint from the PR's processor OOC gate.` The composition does not touch the RTL lens's scope. Source coverage is R747-4 and R748-3 at `81f78a81`.
- `[R747] PASS Robustness - syn/ooc/pp_resource_gate.py (blob identical to 81f78a81), receipts/gate_selftest.log (500 fuzz cases), receipts/gate_mutants.log - the gate's refusal, boundary and malformed-input paths are byte-unchanged and still pass on the composed population.` The composition does not touch the Robustness lens's scope. Source coverage is R747-4 and R748-3.
- `[R747] PASS Tests - receipts/gate_selftest_documented.log:391, receipts/gate_mutants.log (236/236 fail), receipts/gate_check_baseline.log, receipts/hygiene_check.log, receipts/py_idiom.log - the PR's documented validation commands give the PR body's stated results on the candidate; the shared ratchets pass on the composed population.` OBS-1 and L1 are outside the composition.
- `[R747] PASS Docs - receipts/{docs_check,gen_toc_check,gen_toc_anchors,gen_toc_selftest,em_dash_base_parent,em_dash_base_srcbase,doc_style,doc_paths,submodule_docs,ci_events_check}.log; docs/design/AREA_BUDGET.md:142-150, docs/reference/SUBMODULES.md:416-428, CHANGELOG.md:70-80 - both sides' Markdown composes with no TOC, anchor, style, path or em dash defect; F1 is resolved.` The PR-body RESIDUE items RS1 and R2 are retained and do not affect coverage.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #818 body acceptance; `AREA_BUDGET.md:144-146`; `gate_selftest.log:232-235`; `gate_check_baseline.log`; composition identity | R747-5 (composition); source: R747-4, R748-3 | `125ac68006d124dd149b9161539dfaa787166e62` (source `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`) |
| RTL | CLEAN (composition does not touch the scope) | gitlinks at three commits; file-disjointness | R747-5; source: R747-4, R748-3 | `125ac68006d124dd149b9161539dfaa787166e62` (source `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`) |
| Robustness | CLEAN (composition does not touch the scope) | gate blob identity; fuzz and mutant runs on the candidate | R747-5; source: R747-4, R748-3 | `125ac68006d124dd149b9161539dfaa787166e62` (source `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`) |
| Tests | CLEAN | self-test (312 arms, 500 cases); 236/236 mutants; baseline on 3 endpoints; ratchets | R747-5; source: R747-4, R748-3 | `125ac68006d124dd149b9161539dfaa787166e62` |
| Docs | CLEAN | docs, TOC, anchor, em dash, style, path, submodule and CI-event gates; F1 prose lines | R747-5; source: R747-4, R748-3 | `125ac68006d124dd149b9161539dfaa787166e62` |

## Real limits

- **Not run here, so I relied on the signed packet:**
  - the full parent, PP, gPTP, Yosys and builder banks;
  - Docker and act;
  - the image-level population audit (L1);
  - the image-form `ci_command_table` and `ci_tool_inventory`;
  - the hosted contexts.
- **Physical calibration was NOT RUN.** Field skips and the not-run physical gPTP job are not hardware proof.
- **This candidate sits on parent `7f4d7eea`.** The final current-dev candidate (live dev `8adf5c99`) is the manager's build at the merge turn, and this round did not examine it.
- **No new route was measured.** The #814 round-1 routes are judged only through the committed record and `check-baseline`.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) and link its receipts on the PR. Re-run composition if dev has moved beyond `7f4d7eea`'s content.
- Own hosted and act acceptance on the exact PR head.
- Route these to the image-maintenance follow-up or to this lane:
  - L1: the exec-audit generated-program digests.
  - OBS-1: the command-table content pins, and a declaration for `pp_resource_gate_set_selftest.py`.
- Once the #814 line of work measures a new route, refresh `docs/design/AREA_BUDGET.md:149-150`, the recorded route's critical-path sentence. Neither side touches it, so it is not a composition defect.
- Carry RESIDUE RS1 and R2 (PR body) to the residue checklist.
- Merge only with explicit maintainer authorization.

R747-5 FINISHED
