[R532] POSITIVE - exact head fe1cd0679f5028c749af7242c903a82ca2b3d692

Round R532-14 is the internal independent delta review of issue #665, lane F4, PR #690. It covers the one commit `154722e1..fe1cd067` (tree `1452e3d48865f09739432b92608401371257dfb1`). The source base `99e4eb6c` and live dev `17f62ef6` carry byte-identical act runners (section 4). The round-13 POSITIVE verdicts at `154722e1` are the baseline for everything outside this delta.

All five lenses (Conformance, RTL, Robustness, Tests, Docs) were applied at this head and are CLEAN. No BLOCKER, MAJOR, MINOR or RESIDUE is open. Two optional SUGGESTIONs are recorded (R532-14-S1, R532-14-S2). Every prior public finding is resolved or retained unchanged (section 6). This verdict does not authorize merge and does not close issue #665.

## 1. Reconstruction

- **Contract.** AGENTS.md sections 3 to 8, CONTRIBUTING.md, docs/README.md, issue #665 body (F4 = SRP lane).
- **Round-14 assignment** (#665 comment 6055458854) has three items:
  1. Add the exact lwSRP tuple to `TRUSTED_SUBMODULES`, so that `REQUIRED_SUBMODULES` materialises it over public HTTPS.
  2. Update every act-runner contract and self-test that enumerates the trusted submodules. Add a check, with a planted control, that a candidate whose `.gitmodules` adds or drops lwSRP is refused.
  3. Run the runner self-tests, contract gate, docs gates, builder and ctrl suite.

  The manager will run this PR's act replay with dev's trusted runner plus exactly this manifest entry.
- **REVIEW READY** 6055933097 and review start 6055957026.
- **Authorities.**
  - `.gitmodules` at the head.
  - `docs/testing/CI_WORKFLOWS.md`: "Act-first local replication", covering the trust boundary and bootstrap (`:1385-1440`), and the manifest paragraph (`:1542-1552`).
  - AGENTS.md section 5: the trusted dev runner, and the candidate's self-test only inside the disposable CI job.
- **Delta** (`receipts/round14-delta.diff`): only `scripts/act_ci.py` (+78/-2) and `docs/testing/CI_WORKFLOWS.md` (+4/-4). Parent is `154722e1`; one-line message, no trailer, no merge/rebase/amend. All five gitlinks are unchanged (`receipts/clone-integrity.log`).
- **Public evidence.** The author's round-14 packet at evidence commit `2276e34a`:
  - Files read: `author-r14/ROUND14-GATES.md`, `ROUND14-MUTATIONS.json`, `ROUND14-SCOPE.JSON`, `round14-helpers/runner-mutants.py`, `runner-job.sh`, `round14-receipts/runner-final.log` and `runner-mutants.log`.
  - The `runner-final.log` (`455eca12…`) and `runner-mutants.log` (`6ad90fe0…`) digests match the gate table.
  - `ROUND14-SCOPE.JSON` binds the runner to sha256 `35890bea…`, which equals the head blob (`receipts/clone-integrity.log`).
  - The runner self-test ran inside a networkless, read-only container, as AGENTS.md section 5 allows. It reports 442 `ok` lines and `selftest: PASS`; the single `FAIL` substring is inside an arm label (`:256`).

## 2. Independent pass over the delta

**Manifest entry (`scripts/act_ci.py:229-233`).**
- The tuple `("third_party/lwSRP", "third_party/lwSRP", "https://github.com/kebag-logic/lwSRP.git")` equals `.gitmodules:13-15` byte for byte: name, path and URL, including `.git`.
- The subsection name keeps its case through `git config --list`.
- `REQUIRED_SUBMODULES` (`:235-237`) is unchanged code. It now yields verilog-axis, protocol-processor, gptp-processor and lwSRP, and still excludes `external`.

**The trust model is unchanged.**
- Apart from the tuple, the production code paths are byte-identical: `expected_submodule_config` (`:1662`), `validate_submodule_manifest` (`:1671-1733`), `initialize_required_submodules` (`:1736-1751`), `git_prefix` (`:1086-1100`) and the callers at `:1837` and `:5278`.
- `receipts/dev-plus-tuple-vs-head.diff` shows that dev's runner plus only the tuple differs from the head runner only inside `selftest_submodule_manifest` and `selftest_lwsrp_manifest` (head `:10590-10723`).
- The only new network destination is the one approved public HTTPS URL. There is no new credential, environment, path, process or Docker surface.
- `protocol.allow=never`, with only HTTPS enabled, is unchanged. The SSH-only `external` entry is still validated and never fetched.

**New self-test arms.**
- **Independent fixture** (`:10590-10601`). It hard-codes the five approved entries. This removes the circularity of the base version, which derived its fixture from `TRUSTED_SUBMODULES` (base `:10587,10592`).
- **Materialization arm** (`:10622-10629`). It pins the exact `git submodule update --init --` argv.
- **`selftest_lwsrp_manifest`** (`:10677-10723`). It has six variants: drops, duplicates, adds another, redirects, drops gitlink, adds gitlink.
- **Two candidate-trust plants.** They cover the config-only drop and add. They show that the refusal comes from the trusted manifest comparison, and that an unchanged gitlink set cannot mask it.

## 3. Executed evidence (this round, exact head bytes)

The runner was **not** executed as a program, and its `--selftest` was not run here. The probes work as follows:
- They read a byte copy of the head file (sha256 `35890bea…`).
- They AST-extract a fixed list of reviewed definitions into a fresh module: the manifest constants, `Refusal`, `SelftestTally`, `expect_refusal`, the git helpers, the three manifest functions and the two manifest self-test functions.
- The runner's tracked process launcher `capture()` is replaced by a reviewer-owned function with the same contract.
- Every fixture git command runs locally with `protocol.allow=never`.

| Run | Result | Receipt |
|---|---|---|
| Baseline: unmodified head definitions (`probe_manifest.py … none`) | 15/15 arms ok, failures 0 | `receipts/probe-none.log` |
| 21 defect mutations plus one no-defect control, at most 16 in parallel (`run_campaign.sh`) | 20 caught. V4 survives (S1). T6 (control, no defect) passes as expected | `receipts/campaign-summary.txt`, `receipts/probe-*.log/.rc` |
| Real commits through the extracted production validator (`probe_validate.py`) | See below | `receipts/validate-real-commits.log` |
| End-to-end materialization (`probe_materialize.py`) on a scratch clone of the head, using the runner's git prefix/environment and anonymous HTTPS | rc 0, 5.3 s. All four required trees are populated at their gitlinks, lwSRP at `9197193e` from `https://github.com/kebag-logic/lwSRP.git`. `external` is neither configured nor populated | `receipts/materialize-e2e.log` |
| Offline gates: `ci_events.py --check` (1741 items), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py`, `check_baremetal_only.py --check`, `measure_naming/fail_fast/test_evidence --check`, `check_todo_ownership.py` | All rc 0 | `receipts/gates/*` |
| `check_em_dash.py --base 154722e1` | rc 2: cannot judge, because the pinned renderer is not installed and no shared install is permitted. A manual check finds no em or en dash in the added lines. The author's receipt docs-03 is rc 0 | `receipts/gates/em-dash.*` |

Real-commit validation results:

| Runner | `fe1cd067` (head) | `154722e1` | `17f62ef6` (live dev) |
|---|---|---|---|
| Head runner | ACCEPT | ACCEPT | REFUSE (missing lwSRP) |
| Dev runner | REFUSE: `unexpected 'submodule.third_party/lwSRP.path'`, the exact message the manager reported | REFUSE (same message) | ACCEPT |
| Dev + tuple | ACCEPT | ACCEPT | REFUSE (missing lwSRP) |

Mutation catches (the claimed arm fails for its claimed defect):

| Mutation | Caught by |
|---|---|
| P1 manifest omits lwSRP / P2 wrong URL (`.git` dropped) / P3 wrong path | "five approved entries"; the exact-manifest acceptance aborts |
| P4 REQUIRED includes external / P5 omits lwSRP / P6 reorders | the materialization argv arm |
| V1 ignore extra config keys | "adds another lwSRP" (and the standing update-command arm) |
| V2 ignore missing config keys | "drops lwSRP" |
| V3 ignore URL values | "redirects lwSRP" (and the standing URL arm) |
| V5 no duplicate-key check | "duplicates lwSRP" |
| V6 no gitlink check / V7 subset-only / V8 superset-only | "drops/adds lwSRP gitlink" (and the standing gitlink arm), as applicable |
| V9 SSH protocol enabled | the HTTPS-only arm |
| T1 plant does nothing | both "control catches candidate-controlled trust" checks |
| T2 extra stanza also refused for an incidental key | the "adds another lwSRP" control |
| T3 drop variant also drops the gitlink (gitlink masks config) | the "drops lwSRP" control |
| T4 drop variant drops nothing / T5 redirect variant redirects nothing | the variant's own refusal arm |
| C1 pre-fix shape: manifest omits lwSRP **and** the fixture is derived from the manifest | the materialization arm and the "drops lwSRP" arm, then abort |

These results are consistent with the author's eight named mutation/needle pairs (`ROUND14-MUTATIONS.json`). Three of those pairs share one `if False` validator mutation with different needles. This campaign splits the extra, missing and value-change defects (V1, V2, V3) and also tests the two plants themselves (T1 to T3).

## 4. The manager's act replay procedure

- Source base `99e4eb6c` and live dev `17f62ef6` carry the same `scripts/act_ci.py` (sha256 `79579e6b…`).
- Applying exactly the five-line tuple (`receipts/dev-plus-tuple.diff`) gives a runner whose production code equals the head runner's. `receipts/dev-plus-tuple-vs-head.diff` shows differences only in the two self-test functions.
- The reviewer's reconstruction has sha256 `35d2cd4436a9beab31e59be1e67d7eadef28b8e448401ee7717c0af4836e67d4`. It accepts this head and refuses the dev tree (`receipts/validate-real-commits.log`).

Judgement: **sound and minimal.** It adds only the reviewed manifest entry to the trusted install, and it does not bring the candidate's new self-test code into the trust anchor. Conditions:
1. Run it through the documented audited-install bootstrap (`CI_WORKFLOWS.md:1398-1420`):
   - `install -m 0555` outside the candidate, and record the SHA-256;
   - `--selftest --worktree <candidate>`;
   - `--pr 690 --repo kebag-logic/milan-fpga --worktree <candidate> --trusted-install-sha256 <digest>`.

   A patched copy is not clean at the validation base, so the ordinary trusted-dev invocation would refuse it.
2. Publish the diff against the dev blob, and the installed digest, on the PR. The diff must show only the tuple hunk.
3. Re-derive the patch if dev's `scripts/act_ci.py` moves before the run.
4. Note that the patched install's self-test keeps dev's fixture, which is derived from `TRUSTED_SUBMODULES`, so it does not exercise the new lwSRP arms. Those arms are evidenced by the author's containerized head self-test and by section 3.

## 5. Findings

**R532-14-S1 | SUGGESTION | Tests | `scripts/act_ci.py:10677-10723` (`selftest_lwsrp_manifest`), `:1710`**
- Evidence: mutant V4 ignores `.path` value changes when it compares the parsed manifest. It survives with 0 failures (`receipts/probe-V4-ignore-path-values.log`). No arm, new or standing, changes a `.path` value while keeping the key set.
- Impact: none today. Production compares the full key/value map, and a path redirect would also meet the gitlink-set equality check or git's own path lookup. The gap concerns only a future regression of the validator.
- Optional outcome: add a variant that sets lwSRP's `path` to another value, with gitlinks unchanged.
- Verification: V4 then fails that arm.

**R532-14-S2 | SUGGESTION | Docs | `docs/testing/CI_WORKFLOWS.md:1398-1405`**
- Evidence: the bootstrap paragraph says later PRs, "including changes to this runner", are validated by the already-trusted base copy.
- That cannot hold for a PR that changes the trusted submodule set, because by design the base copy refuses it (`receipts/validate-real-commits.log`).
- After such a merge, in-flight PR heads that lack the new entry are refused until they merge dev.
- This text predates the delta and is outside the frozen round-14 assignment.
- Optional outcome, as a separate Issue if the owner wants it: name the manifest-change case and its audited-install procedure (section 4).
- Verification: a docs-only diff.

No BLOCKER, MAJOR, MINOR or RESIDUE.

## 6. Prior public findings at this head

These were read after the independent pass and the draft verdict (`receipts/independent-verdict-draft.txt`, 10:39:22+02:00). The round-13 verdicts at `154722e1` (R532-13 6052690604, R533-13 6052580165) leave no open BLOCKER, MAJOR, MINOR or RESIDUE.

| Finding | Disposition at `fe1cd067` |
|---|---|
| R532-12-F1 (MINOR, Tests) | Resolved at R532-13/R533-13. `srp_feedback.hpp` and `srp_mutants.py` are untouched by this delta. Retained resolved. |
| R533-12-R1 (RESIDUE, Docs) | Resolved. `docs/design/MAILBOX_SPLIT.md` is untouched. Retained resolved. |
| R532-12-S1 (SUGGESTION, RTL/Tests) | Optional, not taken. `srp_mbx.c` is untouched. Retained optional. |
| R532-8-F1, hosted half | Still a manager duty (section 8). |
| All earlier findings listed as resolved in R533-13's retention table | No artifact they name is in this two-file delta. Retained resolved. |

## 7. Lens ledger (reviewer-owned)

```text
[R532] PASS Conformance — scripts/act_ci.py:207-237, .gitmodules:13-15, receipts/validate-real-commits.log, receipts/materialize-e2e.log — the tuple equals .gitmodules exactly, REQUIRED_SUBMODULES materialises lwSRP over anonymous HTTPS, and assignment items 1-3 are met with the author's digest-verified receipts
[R532] PASS RTL — receipts/round14-delta.diff, receipts/clone-integrity.log — no HDL, register, mailbox contract, workflow or gitlink change in the delta; the runner's module contracts (validate/initialize signatures, callers :1837,:5278) are unchanged
[R532] PASS Robustness — scripts/act_ci.py:1671-1751, receipts/campaign-summary.txt, receipts/validate-real-commits.log — duplicate, extra, missing, redirected and gitlink-mismatched manifests are refused before fetch; external stays unfetched; post-merge refusal of pre-merge trees is the intended exact-manifest behaviour
[R532] PASS Tests — scripts/act_ci.py:10584-10723, receipts/probe-*.log — every new arm and both plants fail for their claimed defect (20 of 21 defect mutations caught; the V4 survivor is S1, optional)
[R532] PASS Docs — docs/testing/CI_WORKFLOWS.md:1542-1552, receipts/gates/* — five gitlinks, four allowlisted HTTPS pins and the lwSRP path match the code; docs gates pass; S2 optional
```

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `act_ci.py:207-237`, `.gitmodules`, assignment items 1-3, real-commit validation, end-to-end materialization, author receipts | R532-14 | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| RTL | CLEAN (no HDL in the delta; runner interface unchanged) | `round14-delta.diff`, gitlinks, `act_ci.py:1671-1751,1837,5278` | R532-14 | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Robustness | CLEAN | `act_ci.py:1671-1751`, mutation campaign, real-commit refusals, external exclusion | R532-14 | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Tests | CLEAN | `act_ci.py:10584-10723`, mutation campaign including the plant tests T1-T3, author `ROUND14-MUTATIONS.json` | R532-14 | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Docs | CLEAN | `CI_WORKFLOWS.md:1385-1440,1542-1552`, offline docs gates | R532-14 | fe1cd0679f5028c749af7242c903a82ca2b3d692 |

R532-13 and R533-13 cover the rest of the PR at its ancestor `154722e1`. Nothing in their lens scopes outside these two files has changed since.

## 8. Real limits and pending manager duties

Limits:
- The runner program and its `--selftest` were not executed. The probes ran extracted reviewed definitions with a reviewer-owned process launcher, so the runner's own `capture()` (unchanged) was not exercised.
- No Docker, act or slot run was performed.
- The end-to-end probe fetched the four public submodules read-only over the network into scratch.
- The em-dash gate could not run locally.
- No manager source bank runs at this head, and none is claimed.
- Physical calibration is NOT RUN, and the author's builder gate 11 calibration is NOT RUN. Field skips are not hardware proof.
- Hosted snapshot (`receipts/hosted-checks-snapshot.tsv`, 10:39:47+02:00):
  - Completed with success: changes, full-ci-gate, verilator-lint, wire-accountability, bdd-conformance, docs-check-no-git, Yosys shards 0 to 3.
  - Skipped: Physical gPTP.
  - Still in progress, with no conclusion drawn: docs-check, elaborate, firmware-unit, yosys-elaboration, Verilator shards 0 to 4.

Manager duties:
- The trusted act replay under the section 4 conditions, with the diff and digest published.
- Hosted acceptance at the exact head, including the in-progress contexts and the hosted half of R532-8-F1.
- The current-dev merge candidate (builder and native banks) at the merge turn, against live dev `17f62ef6`.
- The second, external positive review.
- Explicit maintainer merge authorization, and post-merge containment.
- After merge, tell in-flight PRs that their act replay needs current dev merged in, because the head runner refuses a tree without lwSRP.
- R532-14-S1 and S2 are optional.

R532-14 FINISHED
