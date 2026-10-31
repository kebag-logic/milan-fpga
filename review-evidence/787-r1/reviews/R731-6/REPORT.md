[R731] POSITIVE - exact head 808e64e39c1007e463cf20de892e6dca73bfa2a6

# R731-6: composition review of the #787 merge-train candidate (PR #822)

Cleared-context composition review of issue #787 / PR #822. The candidate is `808e64e39c1007e463cf20de892e6dca73bfa2a6`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. Its parents are `125ac680` (the #818 candidate, whose tree equals live dev `e5b8405d`) and the PR head `86a349d5`.

**Verdict: POSITIVE.** The composed tree adds no defect beyond the reviewed sources, and nothing MINOR or worse is open against it.

The candidate tree is **byte-identical** to the PR source head tree, which R731-5 and R732-5 reviewed POSITIVE at `86a349d5`. It is also byte-identical to `cbc7c604`, which R731-4 and R732-4 reviewed POSITIVE. A merge of live dev `e5b8405d` with `86a349d5` produces exactly this tree, without conflict. Every gate that reads the files shared with the predecessors passes on the candidate: 25 gates, all rc 0. The signed local-CI packet passes all three required checks.

Two **manager-owned merge conditions** are recorded below (MD-1, MD-2). They are not defects in the composed tree, so they do not change the verdict. But **MD-1 means GitHub cannot merge PR #822 at its current head**. Read them before the merge turn.

## 1. Reconstruction

- **Contract.** I read AGENTS.md, CONTRIBUTING.md and docs/README in that order. The issue #787 body has a frozen acceptance: a design-first reset choice; a reset bound on `reboot_req_o`; journal safety; recovery of the eight state items, ADP, gPTP with correct TX timestamps and stream rebind; REBOOT driving the `power` area's 50 soft resets; a request-to-reset simulation and a mutant that ignores the request; and the processor #203 pin landing in the same PR. I also read the round 4 and 5 assignments (issue comments 6541732410, 6543406776, 6544849367) and the round-6 and later manager comments on the PR.
- **Diff.** I read `git diff 125ac680..808e64e3`: 63 files, +3,326 / -73. History is in section 2.
- **Order.** I read the prior public review findings only after my own pass over the composition (section 6).

## 2. Composition facts (receipts: `receipts/composition.txt`, `receipts/overlap.txt`, `receipts/merge_bases.txt`, `receipts/probe_composition.txt`)

| Fact | Evidence |
|---|---|
| Candidate tree = PR head tree | `43d18533` for both. `git diff 86a349d5 808e64e3` is empty |
| Candidate parent tree = live dev tree | `125ac680^{tree}` = `e5b8405d^{tree}` = `1aff472e` |
| Live dev plus the PR head gives this tree | `git merge-tree --write-tree e5b8405d 86a349d5` returns `43d18533` with rc 0 and no conflict messages |
| Predecessors in the candidate | PR #826 (#814), merged to dev as `8adf5c99`, and PR #820 (#818), merged as `e5b8405d`. The PR branch already carries both: `f7d5fc3c` merged `4ee2aa96`, `6ffadb07` merged `81f78a81`, and `86a349d5` merged `8adf5c99` |
| PR files that #826 also changed | `docs/litex/CLOCK_DOMAINS.md`, `docs/testing/TESTING.md`, `sw/litex/milan_soc.py` |
| PR files that #820 also changed | `CHANGELOG.md`, `docs/design/AREA_BUDGET.md`, `docs/integration/BUILDING.md`, `docs/reference/SUBMODULES.md` |
| Predecessor facts kept | `receipts/overlap_removed_lines.txt` lists the 13 dev lines the candidate replaces in those seven files. Each is this PR's own rewording or extension of the same fact: the PP pin row, the soft-reset T0 paragraph, the pp_shadow row, the IPROG note, three `milan_soc.py` literals named as constants, and AREA_BUDGET's "this change" reworded to "#806's route". That last sentence comes from dev's #806 paragraph, so its referent is correct. No #826 or #820 line is dropped. CHANGELOG removes 0 lines |
| Gitlinks | `protocol-processor` `a9e84b66` (the PR's #203 re-pin). `gptp-processor` `135afd04` is the same as dev. No predecessor moves either one |
| Delta since the last reviewed heads | None in bytes: `git diff --name-only cbc7c604 808e64e3` is empty (`receipts/delta_since_reviewed.txt`). The only change is commit ancestry |

**Semantic interaction with #826 in `sw/litex/milan_soc.py`.** #826 adds `AXIReadyStage` on the CPU memory port, `RegisteredRefresher` and `add_staged_sdram`. These sit in the SDRAM and CPU memory path. #787 adds the REBOOT attachments inside `MilanMAC`: the `ethtxend_tgl` toggle, the egress-octet parameters, the PHY-hold `MultiReg` into `sys`, and `ICAPE2`. #826 adds no timing constraint at all: no false-path, max-delay, clock-group or platform command anywhere in its diff, so nothing can catch the new cells. The two changes share no signal and no registry. The census rows for the new crossing (CLOCK_DOMAINS, and the CDC census at x3 SoC `MultiReg` sites) were regenerated earlier and are byte-unchanged. The author's LiteX aggregate rerun shows 8/8 passing (`test_soc_timing_cuts` 23 arms, `RESULT: PASS`) at `f7d5fc3c` (author-r5 `campaigns-f7d5fc3c/litex-sims-rerun.log`). `milan_soc.py` and `test_soc_timing_cuts.py` are byte-identical between `f7d5fc3c` and the candidate.

**Semantic interaction with #820.** #820's gate sources (`syn/ooc/pp_resource_gate*.py`) are byte-equal to dev in the candidate, and this PR does not change them. The AREA_BUDGET and SUBMODULES route records state the re-pin route under the #818 gate, which composes with #820's paragraph. R731-4 and R732-4 reviewed that at the tree-identical `cbc7c604`.

## 3. Gates run on the candidate (`run_gates.sh`; receipts `receipts/gates/*.log|.rc`, `receipts/gates_summary.txt`)

All 25 gates exit 0. The Markdown gates ran with the pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1), which the gates verify themselves.

- **`docs_check.py`**: 0 findings across 212 md files and 1,435 scrubbed text files.
- **`gen_toc.py --check`, `--verify-anchors` and `--selftest`**: 552 cross-page fragment links reproduced.
- **`check_em_dash.py --base 125ac680`** (the candidate's parent) **and `--base e5b8405d`** (live dev): each reports 0 findings over 588 added lines in 25 pages, arms 339/339.
- **`ci_events.py --check` and `--selftest`**: OK on 2,199 contract items. **`ci_gate_workflows.py --check`**: OK.
- **Doc, submodule, diagram and SoC checkers**: `check_doc_paths`, `check_doc_style`, `check_submodule_docs` (6 exact gitlinks), `check_gptp_docs` with and without `--with-submodule`, `check_soc_sources`, `check_solution_docs`, `check_diagram_pngs` (6 decoded, source-bound), `check_feature_status`, `check_port_contracts`.
- **Hygiene and idiom ratchets**: `check_hygiene --check`, `check_py_idiom`, `check_rtl_source_lists`, `check_todo_ownership`.
- **`git diff --check`** against both `125ac680` and `e5b8405d`: rc 0.

The workflow hashes in the manifest's `definitions` (docs, elaborate, rtl-fast, rtl) match the candidate's `.github/workflows/*.yml` byte for byte (`receipts/sig/manifest_summary.txt`).

## 4. Signed local CI (`receipts/sig/`)

1. `allowed_signers` holds exactly one key. Its fingerprint is `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k` (ED25519) and its principal is `milan-local-ci`. **PASS.**
2. `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` reports a good signature, rc 0. The negative control with the wrong namespace returns rc 255. `manifest.json` sha256 is `ceb7a2f8…e2f4`, as stated. **PASS.**
3. The subject names candidate `808e64e3…`, its parent `125ac680…`, candidate tree and head tree both `43d18533…`, head `86a349d5…`, PR 822. The result is `success`. All 47 coverage entries have `ok: true`: 46 by act, plus `rtl/physical-gptp` as not-run with its reason. Act ran 68 jobs (67 success, and the schedule-only physical gPTP job skipped), exit 0. Bank `full-native` ran 5/5 commands with rc 0, and bank `manager-builder` 48/48. **PASS.** See MD-2 for one field that cannot be reconciled.

**Hosted checks at `86a349d5`** (`receipts/hosted_checks_86a349d5.tsv`): 67 success, 1 skipped (Physical gPTP, schedule only). They ran from 17:15Z to 18:36Z, against dev `8adf5c99`, before #820 merged at 20:12Z. Hosted and act acceptance is the manager's.

## 5. Findings

No BLOCKER, MAJOR or MINOR finding is open against the composed tree.

### Manager-owned merge conditions (not composed-tree defects)

#### MD-1 - merge readiness - PR #822 head `86a349d5` against live dev `e5b8405d` - criss-cross history: GitHub reports DIRTY and the act classifier refuses

- **Lenses affected if it is left:** Robustness and Tests (merge mechanics and evidence). The tree is unaffected.
- **Evidence:**
  - Since #820 merged, `git merge-base --all e5b8405d 86a349d5` returns two bases, `8adf5c99` and `81f78a81`.
  - `gh pr view 822` at 23:10Z reports `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY` (`receipts/github_pr_state.txt`).
  - A merge on base `8adf5c99` alone conflicts in `docs/design/AREA_BUDGET.md`. On `81f78a81`, or recursively, it is clean and gives `43d18533` (`receipts/probe_composition.txt`).
  - I extracted the act-path step of rtl-fast's `changes` job (`.github/workflows/rtl-fast.yml:53-54`; `receipts/classify_step.sh`) and ran it with `origin/dev = e5b8405d`. It exits 128 (`fatal: Not a valid object name`). With `origin/dev = 8adf5c99` it passes with `rtl=true` (`receipts/classify_origin-dev-*.log`).
  - R732-5 S1 predicted this class. The manager's comment 6546588633 describes the same refusal at `cbc7c604`.
- **Impact:** GitHub cannot merge the PR at this head. A new act replay of `86a349d5` against live dev refuses in `rtl-fast/changes`. The candidate itself cannot be pushed as dev's next commit, because its first parent is `125ac680`, not `e5b8405d`.
- **Required outcome:** before the merge turn, the PR head must have a single merge base with live dev. For example, a merge of `e5b8405d` into `787-reboot-reset`: I verified that `merge-tree` gives the same tree `43d18533`. That new head then needs its own exact-head evidence: hosted checks, and an act replay against live dev.
- **Verification:** `git merge-base --all origin/dev <new head>` prints one line. `mergeStateStatus` is not DIRTY. The new head's tree is `43d18533`.

#### MD-2 - evidence provenance - signed `manifest.json` `environment.act_runner` - the act result cannot come from the recorded runner

- **Lens affected:** Tests (evidence). The tree is unaffected.
- **Evidence:**
  - The manifest records `act_runner: e5b8405d` and `rtl-fast/changes: success` for PR head `86a349d5`.
  - The runner refuses unless its own commit equals the live dev tip (`scripts/act_ci.py` `validate_trusted_runner`, at `e5b8405d`). It fetches dev with full history (`materialize_remote_head`), and it has no option to override the base.
  - So a run from runner `e5b8405d` validates against `e5b8405d`, where the `changes` step must exit 128 (MD-1 probe).
  - The recorded success can only be reproduced with dev at `8adf5c99`. The manager's comment says the replay started at 18:16 local time, before #820 merged. The evidence commit that publishes the packet, `9399c5dc`, is dated 23:58 local time, after #820 merged.
- **Impact:** the packet misstates which runner and validation base produced the act result. The substance holds: act ran the PR head tree, which is the candidate tree, classified `rtl=true` either way, and all jobs passed. The banks ran the candidate itself. No coverage is lost. Only the label is wrong.
- **Required outcome:** the manager states the replay's actual runner and validation base in the packet, or re-signs after a replay that matches the label. That replay is only possible once MD-1 is cleared.
- **Verification:** the `act_runner` field equals the dev tip that the runner validated against, and that tip has a single merge base with the replayed head.

### RESIDUE (wording only; carried to the residue checklist)

#### RES-1 - RESIDUE - Docs (PR body) - PR #822 body lines 5, 16-17, 34, 68 and 202-203 (`receipts/pr822_body_at_review.md`) - the body predates both predecessor merges

This updates R731-5 RES-1 and R732-5 F1, which overlap R731-4 RES-B and RES-C and R732-4 R1.

- **Evidence:**
  - Line 16 still reads "REVIEW READY at `cbc7c604` … -> `dev` (`02ca829a`)".
  - Lines 17 and 68 say the PR "merges after" #826 and #820. Both are now in dev (`8adf5c99`, `e5b8405d`).
  - Line 34 reads "**Gates at the head pass.**".
  - R731-4 RES-A ("that file is not part of this PR") is **still present**. It wraps across lines 202-203, which is why R731-5's single-line probe recorded it as resolved. R732-5 retained it correctly.
- **Exact fix:**
  - Line 16: "**REVIEW READY** at `<new head>` (tree `43d18533`, identical to `cbc7c604`). `787-reboot-reset` -> `dev` (`e5b8405d`)."
  - Lines 17 and 68: "PR #826 (#814) and PR #820 (#818) are merged into dev (`8adf5c99`, `e5b8405d`); this PR carried their commits."
  - Line 34: "**Gates at `f7d5fc3c` pass, and carry to `<new head>`** (tree identical to `cbc7c604`)."
  - Line 5: "carrying PR #826's and PR #820's commits".
  - Lines 202-203: delete "; that file is not part of this PR". #820's gate is in dev now.
  - Do not reuse R731-5's proposed sentence "gives the branch one merge base with dev". It stopped being true when #820 merged (MD-1).

#### Carried unchanged (bytes unchanged, so each item keeps its prior status)

- **R731-1 F1 = R732-1 R2.** `tb/verilator/reboot_ctrl/mutants.py:113-114` (blob `2528a927`) still reads `# the [A10] arms of issuecomment-6518083444: …`. Fix as given in R731-1. Tracked by #746.
- **R732-1 R1.** `tb/tools/torture_campaign.py:3135-3139` (blob `43b1fc40`).
- **R732-4 R2.** `docs/reference/SUBMODULES.md:503`, "this change". **R731-4 RES-D and RES-E = R732-4 R3.** The re-pin route's record pointer.

### SUGGESTION (optional; all retained, bytes unchanged)

R731-4 SUG-1 = R732-4 S1 (`cdc_census.gen.py:122-123` note; no `--check` arm, R731-3 S2), R731-4 SUG-2, R732-4 S2, R732-4 S3, R731-3 S3, R731-1 S1 (`milan_datapath.sv` blob `443c2085`), R731-1 S2 and R732-1 S1 (`KL_reboot_ctrl.sv` blob `d2c74f47`), R732-1 S2, and R732-5 S1. R732-5 S1 asks that the classifier's criss-cross refusal print a reason instead of `fatal: Not a valid object name`. MD-1 shows why that would help.

**Comment rule.** The candidate changes no source byte relative to the reviewed heads, so no new comment instance is possible. The existing instance is carried above under #746.

## 6. Prior public findings at this head (read after the independent pass)

- **Earlier MINORs.** R731-3 F1 = R732-3 F1 (CDC census) and R732-3 F2 (re-pin route record) are **resolved**. R731-4 and R732-4 verified both at `cbc7c604`, and the candidate tree is identical.
- **No prior MINOR or worse is open.**
- **RESIDUE and SUGGESTION items** are dispositioned in section 5. Correction: R731-4 RES-A is still present (RES-1).

## 7. Lens results

| Lens | Result | Artifact | Checked |
|---|---|---|---|
| Conformance | PASS | issue #787 acceptance; `git diff 86a349d5 808e64e3` (empty); `REQUIREMENTS.md` unchanged between the reviewed heads and the candidate | The composition changes no acceptance artifact, requirement, protocol code or test relative to the source tree reviewed POSITIVE by R731-5 and R732-5 |
| RTL | PASS | `sw/litex/milan_soc.py` (the #826 overlap); `hdl/milan/*.sv` blobs; gitlinks `a9e84b66` / `135afd04` | #826's SDRAM and CPU memory-port cuts and #787's MilanMAC REBOOT attachments share no signal, constraint or registry. HDL is byte-unchanged. LiteX 8/8 at a byte-equal `milan_soc.py` (author-r5) |
| Robustness | PASS (MD-1 is manager-owned) | merge bases; `rtl-fast.yml:53-54` classifier probe; single-base merge probe | The composed tree is the recursive merge with no conflict. The criss-cross refusal is a merge-mechanics condition, not tree behaviour |
| Tests | PASS (MD-2 is manager-owned) | signed manifest (key, signature, subject, 47 coverage entries, banks); hosted checks at `86a349d5`; `ci_events --check/--selftest`; `ci_gate_workflows --check`; suite inventories (`run_all_suites.sh`, `suite_shards.py`, #826's `exec-audit.json`) | Every workflow job is mapped and ok. Workflow definitions match the candidate. #826's exec-audit entry is a LiteX stand-in that this PR does not touch |
| Docs | PASS (RESIDUE carried) | the seven overlap files; docs gates (section 3); PR body | Every predecessor fact is kept (0 dropped lines). TOC, anchors and em-dash pass against both bases. The PR body is stale in wording only (RES-1) |

## 8. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition: tree identity and the empty source delta. The source content is covered by R731-5 and R732-5 at `86a349d5` (tree `43d18533`); R731-3 and R732-3 covered it at `f7d5fc3c`, and no later byte touched its scope | R731-6 (composition); R731-5 / R732-5 (source) | 808e64e39c1007e463cf20de892e6dca73bfa2a6 |
| RTL | CLEAN | `milan_soc.py` overlap with #826; HDL blobs; gitlinks | R731-6 (composition); R731-5 / R732-5 (source) | 808e64e39c1007e463cf20de892e6dca73bfa2a6 |
| Robustness | CLEAN | merge-base and merge-tree probes; act classifier probe (MD-1 is manager-owned) | R731-6 (composition); R731-5 / R732-5 (source) | 808e64e39c1007e463cf20de892e6dca73bfa2a6 |
| Tests | CLEAN | signed packet; hosted checks; CI registries; suite inventories (MD-2 is manager-owned) | R731-6 (composition); R731-5 / R732-5 (source) | 808e64e39c1007e463cf20de892e6dca73bfa2a6 |
| Docs | CLEAN (RESIDUE RES-1 and the carried items go to the checklist) | overlap docs; 25 gates; PR body | R731-6 (composition); R731-4 / R732-4 at the tree-identical `cbc7c604`, and R731-5 / R732-5 (source) | 808e64e39c1007e463cf20de892e6dca73bfa2a6 |

## 9. Real limits

- **No source bank runs.** I ran no manager source bank, no full parent, PP, gPTP, Yosys or builder bank, no Vivado and no act. Execution evidence is the signed packet (candidate banks and act of the PR head), the hosted checks at `86a349d5`, and the author receipts.
- **No RTL or simulation probes.** I ran none, because no byte in their scope differs from the reviewed source tree. The only probes were git composition, the extracted classifier step and the docs and registry gates.
- **ROM digests.** The digest ledger needs the Yosys-backed `ooc.sh` path, which I did not run. Its bytes are this PR's own, no predecessor touches them, and the author's round-5 re-record was byte-identical.
- **Hardware.** Physical calibration is NOT RUN, and field skips are not hardware proof.
- **GitHub state.** The mergeability state was read at 23:10Z and can change.

## 10. Pending manager duties

1. **Clear MD-1 before the merge.** Give the branch a single merge base with live dev; the tree must stay `43d18533`. Then take exact-head hosted evidence, and an act replay against live dev that the classifier accepts.
2. **Fix the act label (MD-2).** State the real runner and validation base of the signed replay, or re-sign after a matching replay.
3. **Build and validate the final current-dev candidate at the merge turn.** Link its receipts on the PR.
4. **Carry RES-1 and the retained RESIDUE items to the residue checklist.** Apply RES-1's corrected line-202 fix.
5. **Run post-merge containment, and close #787 / move it to Done**, per CONTRIBUTING.

Receipts are listed in `MANIFEST.sha256`. The clone was restored and verified at exact head (`receipts/restore_check.txt`): HEAD and index tree are `43d18533`, the worktree is clean, the ls-files modes and blobs equal ls-tree, and the gitlinks are as committed.

R731-6 FINISHED
