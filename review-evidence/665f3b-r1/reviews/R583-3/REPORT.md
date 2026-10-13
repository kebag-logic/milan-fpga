[R583] NEGATIVE - exact head 532ab871272597d83fa08506bcb05298fbe87806

# R583-3: external independent delta review, issue #665 / PR #736

- Reviewed head: `532ab871272597d83fa08506bcb05298fbe87806`, tree `c298ac5e6a61242d1de452ec24c9991b78881148`.
- Delta: `651ccb5a..532ab871`, one commit: "fix(ci): classify mailbox service bounds as a gated input".
- Branch range for the inventory: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0..532ab871`.
- Scope: the round-3 assignment, issue #665 comment 6155487551. Earlier rounds stand for anything this commit does not touch.

## Verdict

The verdict is NEGATIVE because of one new MINOR, R583-3-F1 (Docs). The commit adds an eighth entry to `GATE_READ_DOCS`. The CI policy page now enumerates eight gate-read pages but still says "Seven pages". That is a stale count, which is a figure, so it is not residue.

Everything else in the round-3 assignment is met at this exact head:

- **Registration.** `docs/design/MAILBOX_SPLIT.md` is in `GATE_READ_DOCS`, and its reader is named.
- **Classifier.** The self-test passes, and its negative controls fail as they should.
- **Inventory.** An independent inventory over the whole branch finds no other unregistered gate-read page.
- **MAAP README.** The new sentences are accurate against the code.
- **PR body.** The R582-2-R1 fix was applied as prescribed.
- **Nothing else changed.** The commit touches three files, and all six gitlinks are unchanged.
- **Hosted CI.** Every required context ran and succeeded at the exact head.

The open BLOCKER and MAJORs from earlier rounds (R582-2-F1, R583-2-F1, R582-1-F1) are resolved at this head.

## Findings

### R583-3-F1 - MINOR - Docs

- **Artifact:** `docs/testing/CI_WORKFLOWS.md:179`, "Seven pages under `docs/` are relevant because Python in a classifier-gated job names them." Compare it with `scripts/ci_scope.py:69-78`, where `GATE_READ_DOCS` now has 8 entries.
- **Authority/evidence:**
  - At the parent `651ccb5a`, `GATE_READ_DOCS` had 7 entries, so the sentence was true there.
  - This commit adds `docs/design/MAILBOX_SPLIT.md` (`scripts/ci_scope.py:72`) and appends its reader at `CI_WORKFLOWS.md:201-204`.
  - The paragraph introduced by that sentence (`:179-204`) now names eight pages: REGISTER_MAP, MILAN_V12_AUDIT, TRACE_EVENTS, AAF_LATENCY_TAPS, AREA_BUDGET, MAILBOX_CONTRACT, SPLIT_CONTROL_MEMORY and MAILBOX_SPLIT.
  - The PR body's own Round 3 section says "All eight gate-read pages are registered".
  - `scripts/ci_events.py --check` returns 0 at this head, so no gate catches the stale count.
  - Receipt: `receipts/gate_read_count_wording.txt`.
- **Impact:** the authoritative CI policy page gives a wrong count for the table the round was assigned to update. A reader comparing the page with the classifier gets two answers. Correcting the count changes a stated figure, so under the owner rule of 2026-10-02 this is not RESIDUE.
- **Required outcome:** `CI_WORKFLOWS.md:179` gives the count that matches `GATE_READ_DOCS` ("Eight pages"), or drops the number.
- **Verification:**
  - Re-read `:179` against the `GATE_READ_DOCS` list.
  - `python3 scripts/ci_events.py --check` and `python3 scripts/ci_scope.py --selftest` still return 0.

### R583-3-R1 - RESIDUE - Docs (PR body only)

- **Artifact:** the PR #736 body, section "Status".
- **Evidence:** the R582-2-R1 fix was applied with the text that round prescribed: "Round 2 resumes `db29bdd0…`; `651ccb5aea1bc4d99f356503c188947d39e0c9e4` is the published head of PR #736." The PR's published head is now `532ab871`, so this sentence is stale again. Also stale: "Round 3 local checks pass; exact-head hosted acceptance follows the manager's push." The push has happened, and the hosted runs at `532ab871` have completed. This is pure wording. It changes no figure, test, code or verdict.
- **Exact fix:**
  - Replace "`651ccb5aea1bc4d99f356503c188947d39e0c9e4` is the published head of PR #736." with "`532ab871272597d83fa08506bcb05298fbe87806` is the published head of PR #736."
  - Replace "exact-head hosted acceptance follows the manager's push." with "exact-head hosted acceptance is the manager's."

### R583-3-S1 - SUGGESTION - Tests, Docs

- **Artifact:** `docs/testing/CI_WORKFLOWS.md:179` against `scripts/ci_events.py`.
- **Observation:** the gate-read count on the policy page is free prose that no check reads. That is why F1 escaped.
- **Optional outcome:** have `ci_events.py --check`, or the `ci_scope.py` self-test, compare the stated count with `len(GATE_READ_DOCS)`, or drop the number from the prose.

## Assignment items, judged

| Item | Result | Evidence |
|---|---|---|
| `MAILBOX_SPLIT.md` in `GATE_READ_DOCS`, naming its reader | Met | The `scripts/ci_scope.py:67-68` comment names `ctrl_service_bounds.py (firmware-unit)`. The entry is at `:72` and the classification case at `:292-293`. |
| Stated in `CI_WORKFLOWS.md` gate-read list | Met, with F1 | `CI_WORKFLOWS.md:201-204` names the reader, its job and the page link, which resolves to `docs/design/MAILBOX_SPLIT.md`. It also says "No `docs-check` step runs this check". `.github/workflows/*.yml` confirms the reader runs only through `test_ctrl_firmware.py` (`rtl-fast.yml:356`, firmware-unit). The count at `:179` was not updated (F1). |
| `ci_scope.py --selftest` passes | Met | Local rc 0 (`receipts/ci_scope_selftest_head.{log,rc}`). Negative controls: at parent `651ccb5a`, rc 1 with the identical FAIL line (`receipts/ci_scope_selftest_parent_651ccb5a.*`). At head with only the new entry deleted, rc 1 with 2 failures (`receipts/mutation_drop_entry.diff`, `receipts/ci_scope_selftest_mut_drop_entry.*`). `ci_scope.py docs/design/MAILBOX_SPLIT.md` prints `true`; the control `docs/design/MAAP_FABRIC.md` prints `false` (`receipts/ci_scope_classification.log`). |
| No other unregistered gate-read page over the whole branch | Met | Independent reviewer inventory (`gate_read_inventory.py`; `receipts/gate_read_inventory.tsv`): 90 branch-changed non-doc files and 251 name hits, each judged below. |
| maap README change (R582-2-S1) accurate | Met | See below. |
| R582-2-R1 applied to the PR body | Met as prescribed; now stale again (R583-3-R1) | The PR body's "Status" section has the prescribed sentence. The two limitation bullets ("cannot be proven under the no-push instruction", "prepared for later publication") are gone. |
| Nothing else changed | Met | `git diff --name-only 651ccb5a 532ab871` lists exactly `docs/testing/CI_WORKFLOWS.md`, `scripts/ci_scope.py` and `sw/firmware/ctrl/maap/README.md`. The parent of `532ab871` is `651ccb5a`. The six gitlinks are identical at both commits: `external`, `gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack` (`70936b77`) and `third_party/verilog-axis`. |
| Hosted runs at `532ab871` green | Met | See "Hosted evidence". |

### Gate-read inventory judgement

The reviewer's script lists every line in a branch-changed non-documentation file that names a documentation-classified page under `docs/`, either by path or by bare file name. Most of the 251 hits are bare-name `README.md` matches with no `docs/` reader. Each substantive hit is judged below.

- **Pages in `GATE_READ_DOCS`.** `ctrl_service_bounds.py:13` (MAILBOX_SPLIT) and `sw/litex/test_ctrl_memory.py:94` (SPLIT_CONTROL_MEMORY) are registered.
- **Readers outside the self-test's six roots.** These are the blind spot stated on the policy page.
  - `scripts/check_submodule_docs.py:20-22` reads `docs/reference/SUBMODULES.md` and `submodule_boundaries.drawio`.
  - `docs/diagrams/submodule_boundaries.gen.py:41-48` reads the drawio and png.
  - `docs.yml:121-124`, in the always-run `docs-check` job, runs both scripts.
  - `grep` over `.github/workflows` finds no gated job that runs them. `sw/firmware/ctrl/test/ctrl_configs.py:159` lists the generator only as an OUTSIDE builder that "compiles nothing", not as a step.
  - These pages correctly stay documentation-only.
- **`scripts/ci_events.py:259`** reads `CI_WORKFLOWS.md`. The policy table at `CI_WORKFLOWS.md:216` records that `docs-check` also runs this check.
- **Comments only.**
  - `tb/verilator/milan_dp/Makefile:340,489` mention `docs/testing/TESTING.md`.
  - `sw/firmware/ctrl/acmp/acmp_mbx.h:41` and `sw/firmware/ctrl/test/test_acmp_mbx.cpp:15` mention `FR_NFR.md`.
  - The MAILBOX_SPLIT mentions in `acmp_mbx.h` and the READMEs are comments too.
- **Self-test fixtures.** `scripts/ci_scope.py:365` (`EGRESS_QUEUE_MAP.md`) is the self-test's planted reader page, and the `cdc_census.*` hits are self-test cases.

The self-test's own whole-tree derivation passes, both locally and in the hosted `changes` log.

### MAAP README (`sw/firmware/ctrl/maap/README.md:135-137`)

The claim is: "Receive and link refreshes keep callback snapshots current. They provide freshness within the service pass. The same pass's MAAP poll refreshes and republishes changed gates." Checked against the code:

- `maap_mbx.c:127`: `receive()` calls `refresh_demand` before `maap_rx`.
- `maap_mbx.c:157`: the link event calls `refresh_demand` before `maap_port_operational`, on a link change only.
- `maap_mbx.c:145`: timer expiry also refreshes. The README does not claim the list is exhaustive.
- `maap_mbx.c:163-178`: `poll()` calls `refresh_demand` (`:167`), then `maap_poll`, then recomputes each interface's gate and calls `mbx_pub_da_gate` (`:174`) only when the gate differs from `published_gate`.
- `ctrl_loop.c:143-160`: `ctrl_loop_service` runs events, then RX, then every poll in the same pass. That supports "the same pass's MAAP poll".

The statement is accurate. It is documentation only and changes no code. R582-2-S1's test options remain optional.

## Hosted evidence at `532ab871` (read by the reviewer)

All runs are `pull_request` runs for head `532ab871272597d83fa08506bcb05298fbe87806`, and every job's `head_sha` is that head. Receipts: `receipts/hosted_runs_532ab871.json` and `receipts/hosted_jobs_*.tsv`.

| Run | Workflow | Jobs (conclusion) |
|---|---|---|
| 38471631742 | rtl-fast | changes, bdd-conformance, yosys-elaboration, firmware-control-mutants, firmware-srp-mutants, firmware-aecp-mutants, firmware-boundary, firmware-verilator, publication-census, firmware-unit, verilator-lint and rtl-fast: all **success**. Every job executed; none was skipped. |
| 38471631680 | rtl-full | full-ci-gate, Verilator shards 0-4/5, Yosys shards 0-3/4, verilator-suites and yosys-portability: **success**. "Physical gPTP (nightly and manual)" was **skipped**; it is a nightly/manual context, not hardware proof. |
| 38471632015 | elaborate | elaborate: **success** |
| 38471631560 | docs | docs-check, docs-check-no-git, wire-accountability: **success** |

Log excerpts (`receipts/hosted_rtlfast_excerpts.txt`) come from the run's log archive. The archive's sha256 is recorded there, and the archive itself is unpublished, under scratch.

- `changes` runs `python3 scripts/ci_scope.py --selftest`. It reports these lines as `ok`: "gate-read page docs/design/MAILBOX_SPLIT.md (named at sw/firmware/ctrl/test/ctrl_service_bounds.py:13) is relevant", the two mutation lines for the page, and "selftest: PASS".
- `firmware-unit` prints "== ctrl service bounds: checks: 47 failures: 0 ==".
- `firmware-boundary` and `firmware-verilator` each print the six "scratch lifecycle" controls `[ok]` and end with "ctrl_boundary: PASS".

## Local execution at this head

| Command | Result | Receipt |
|---|---|---|
| `python3 scripts/ci_scope.py --selftest` | rc 0, "selftest: PASS" | `receipts/ci_scope_selftest_head.*` |
| Same, at parent `651ccb5a` (archived tree) | rc 1, with the MAILBOX_SPLIT FAIL line | `receipts/ci_scope_selftest_parent_651ccb5a.*` |
| Same, with only the new entry removed | rc 1, 2 failures | `receipts/ci_scope_selftest_mut_drop_entry.*`, `receipts/mutation_drop_entry.diff` |
| `python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md` / `docs/design/MAAP_FABRIC.md` | `true` / `false` | `receipts/ci_scope_classification.log` |
| `python3 scripts/ci_events.py --check` | rc 0, 2169 contract items | `receipts/ci_events_check_head.*` |
| Service-bounds arm only (`run_service_bounds_arm.py`) | rc 0: 38/38 planted controls caught, 47 checks, 0 failures, matching the hosted run | `receipts/service_bounds_arm_local.*` |
| Independent gate-read inventory (`gate_read_inventory.py`) | 90 files, 251 hits, judged above | `receipts/gate_read_inventory.tsv`, `.stderr` |

The probes ran on archived copies under the unpublished scratch directory, or read the clone without changing it. Interpreter caches the runs created in the clone were removed. Final state (`receipts/clone_integrity_final.txt`):

- HEAD and tree are as stated.
- The worktree and index match HEAD.
- Index blob, mode and path equal the tree.
- The six gitlinks are as stated.

## Prior public findings on this PR, at this head

These were read after the independent pass above.

| Finding | Disposition at `532ab871` | Evidence |
|---|---|---|
| R582-2-F1 (BLOCKER; Conformance, Tests): `MAILBOX_SPLIT.md` unregistered, self-test fails, firmware jobs skipped | **Resolved** | The self-test returns rc 0 locally and passes hosted. firmware-boundary and firmware-verilator executed and succeeded. elaborate, rtl-full, verilator-suites and yosys-portability succeeded. |
| R583-2-F1 (MAJOR; Conformance, Tests, Docs): same omission; classification printed `false` | **Resolved** | Classification now prints `true`. Service bounds pass 47 checks and 38 controls, locally and hosted. The hosted jobs executed. |
| R582-1-F1 (MAJOR; Tests, Conformance): hosted firmware-boundary and firmware-verilator crashed in `Clone.fresh`; retained for missing hosted proof | **Resolved** | Both jobs executed and succeeded at this exact head. Each shows the six scratch-lifecycle controls `[ok]` and "ctrl_boundary: PASS". |
| R582-2-S1 / R582-1-S1 (SUGGESTION) | Addressed by the documentation option; the test options remain optional | README `:135-137` is accurate (see above). |
| R582-2-R1 (RESIDUE, PR body) | Applied as prescribed, but the prescribed sentence is stale again at the new head | Carried as R583-3-R1. |
| R582-1-S2, S3, S4 (SUGGESTION) | Untouched by this delta; still optional | No change in `maap_mbx.c`, `test_maap_mbx.cpp` or the PR scope. |
| R583-1-F1, R583-1-F2, R583-1-R1, R582-1-F2, R582-1-R1 | Resolved at `651ccb5a` by both prior rounds; the delta does not touch their artifacts | `git diff 651ccb5a 532ab871` touches none of them. |

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 assignment items 1-4 against `scripts/ci_scope.py:67-78,292-293` and `CI_WORKFLOWS.md:201-204`. AGENTS.md section 7 hosted contexts against runs 38471631742, 38471631680, 38471632015 and 38471631560: every executed job succeeded. Classification prints `true`. | R583-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| RTL | CLEAN | The three-file diff `651ccb5a..532ab871` contains no HDL, RTL harness or synthesis file, and the gitlinks are unchanged. Firmware composition claims were checked against `maap_mbx.c:36-60,127,145,157,163-178` and `ctrl_loop.c:143-160`. | R583-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Robustness | CLEAN | Classifier failure paths: the parent returns rc 1, the removal mutation returns rc 1, and the docs-only control prints `false`. Inventory blind spots (readers outside the six roots: `check_submodule_docs.py`, `submodule_boundaries.gen.py`, `ci_events.py`) were judged against `docs.yml:121-124` and `CI_WORKFLOWS.md:216`. | R583-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Tests | CLEAN | The new self-test case `ci_scope.py:292-293` fails on removal. The self-test derivation was run over the tree. The service-bounds arm gives 47 checks, 0 failures, 38/38 controls, locally and hosted. Hosted firmware-unit, firmware-boundary and firmware-verilator logs were read. | R583-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Docs | UNCLEAN (R583-3-F1, MINOR; R583-3-R1 RESIDUE carried) | `CI_WORKFLOWS.md:179-204`; the `ci_scope.py:57-68` comment; `maap/README.md:118-139`; the PR #736 body, "Status" and "Round 3" sections. | R583-3 | `532ab871272597d83fa08506bcb05298fbe87806` |

## Real limits

- **Delta only.** This round judges the round-3 delta and the whole-branch gate-read inventory. Lenses and artifacts the delta does not touch rest on earlier rounds, as assigned. The full parent, processor, gPTP, Yosys and builder banks were not run.
- **Hosted results were read, not re-run.** No Docker or act replica was run. The hosted log archive is retained only in scratch.
- **The inventory is a text net.** Like the self-test, it cannot see a page name computed at run time or a reader in a form it does not scan. It was checked against the workflow files by hand.
- **No hardware proof.** Physical calibration was NOT RUN, and the skipped "Physical gPTP" context is not hardware proof. No manager source bank exists for this head, and none is claimed.

## Pending manager duties

- Disposition and repair of R583-3-F1 (one word on `CI_WORKFLOWS.md:179`), then re-review of the new head.
- Carry R583-3-R1 to the residue checklist.
- Current-dev merge-candidate validation (source base `a0f39ad4`, live dev `0136de16`): builder and native banks at the merge turn, with receipts linked on the PR.
- Hosted and act acceptance at the final head.
- Candidate-merge validation and post-merge containment.

R583-3 FINISHED
