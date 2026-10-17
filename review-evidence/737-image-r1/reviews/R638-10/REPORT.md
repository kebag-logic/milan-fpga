[R638] POSITIVE - exact head d7cb1f90af1b8c2f115f58281991f1c9626447f9

# R638-10: merge-and-regeneration review of PR #738 (issue #737, image lane)

- **Head:** `d7cb1f90af1b8c2f115f58281991f1c9626447f9`, tree `c32f2994d5c93cd01fe6d812701432808632657a`. The PR's `headRefOid` equals it.
- **Delta reviewed:** `6f86eee6..d7cb1f90`, which is POSITIVE at `6f86eee6` in R638-9 and R639-9. It has 11 first-parent commits: the merge `03dcd0c36` of `dev` `4a9b5a2a`, then `e19dd3542` through `d7cb1f90a`.
- **Assignment:** PR #738 comment 6208056999. The round-8 class ruling (6196923564) governs classification: an open guard is MAJOR, and a new trick against a closed guard is RESIDUE.
- **Method:**
  - I reconstructed the task cold from AGENTS.md and CONTRIBUTING.md, the issue body and the manager's comments, the diff, and the author's published packet at `f308bf87`.
  - I re-ran the generators' `--check` modes and the self-tests at the head, under CPython 3.12.3 with the pinned parser.
  - I ran differential probes of the new Make walker forms against GNU Make.
  - I built the live-`dev` merge candidate in a disposable copy.
- **Ordering:** I read prior review findings only after my own pass over the delta.

## Verdict summary

- No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN at this head.
- There are four RESIDUE items:
  - one under the class ruling (code);
  - three wording items (two in the guide, one in a source comment).
- There are four SUGGESTIONs. One of them records a merge-turn consequence for the manager: the live-`dev` candidate refuses `ci_tool_inventory.py --check` (see S1 and the pending duties).

## What was checked, against the assignment's four items

### (1) The merge `03dcd0c36`

- **True merge.** The parents are `6f86eee604729b80684526fc5b9be720d94f179a` and `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`, and the merge base is `fa7347fc`. `4a9b5a2a` is an ancestor of live `dev` `1f6f2f57`.
- **Replay.** `git merge-tree --write-tree 6f86eee6 4a9b5a2a` reports exactly one conflict, in `scripts/check_baremetal_only.py` (`receipts/merge-tree-6f86-4a9b.txt`).
- **Resolution.** The committed merge tree differs from the replayed tree only in that file: it drops the three conflict markers and adds one separating blank line.
  - Both arm functions are kept whole: `_arms_image_host_masks` (`scripts/check_baremetal_only.py:1384`) and `_arms_host_memory_reads` (`:1417`).
  - Both are still called, at `:1303` and `:1861`.
  - The self-test reports 867 arms (`receipts/head-checks/baremetal-selftest.log`), and the scan finds 0 findings across 1,395 files.
- **Gitlinks.** Every submodule gitlink at the head equals `4a9b5a2a`'s: gptp-processor `e4869fd0` and tsn-c-stack `70936b77` from `dev`, the others unchanged. The lane had not changed any gitlink since `fa7347fc`.
- **Workflows.** `git diff --name-only 4a9b5a2a HEAD -- .github` is empty: the PR changes no workflow. No `.sv`/`.v` file, and nothing under `hdl/`, `tb/`, `syn/`, `sw/` or the submodules, differs from merged `dev` (`receipts/pr-vs-merged-dev-files.txt`, 52 files, all CI/image/docs).

### (2) Regenerated records and guard closure

**Regenerated records, re-checked at the head:**

| Record | Check run at the head | Result |
|---|---|---|
| `ci/image/tool-inventory.json` (46 records) | `ci_tool_inventory.py --check` | rc 0, "matches" |
| `ci/image/differential-receipt.json`, `syntax-census.json` | `ci_differential.py --check` | rc 0, 224 fixtures, 185 shapes, image `sha256:68331c79…` |
| `ci/image/image.lock.json` | `build.py --check-lock` (offline) | rc 0, recipe consistent; `recipe_digest()` = lock `712f7b38fde7d2c1…` |
| `ci/image/sources.lock.json` | PyYAML row vs `ci/constraints-ci.txt` | 6.0.2 wheel, sha256 `80bab7bf…`, size 767,542; I downloaded and hashed the same wheel |
| `ci/image/exec-audit-receipt.json` | structure and cross-checks (item 3) | sha256 `b8c28953…`, clean, source `54fbcba6a`, whose tree `5bac5727` is the head minus the receipt |

**Inventory change.** Between `6f86eee6` and the head, the inventory changed in four ways:
- `behave` and `pyyaml` were unpinned and now take the constraints file's pins (1.3.3 and 6.0.2).
- The evidence reader's hashed `pyyaml==6.0.2` request is the 46th record.
- Provenance follows the merged workflows.
- No other pin changed.

**Image identity.** I cannot rebuild the image. The two-cold-build evidence is the author's: `round10-cold-chain-2.log` shows recipe `712f7b38` with builds A and B (353,518 and 386,192 ms), the same image digest `68331c79…` and id `772f24ce…`, `--record-lock` on A and `--check-lock --verify-archive` on B. `54fbcba6a` changes only `image.lock.json`, and `git diff --name-only f1c041bce HEAD` lists only the lock and the receipt, so the recipe the builds used is the head's recipe.

**Guards extended for merged forms.** Each guard is judged closed by construction: an allowlist or an exact form, with anything else refused by name.

- **`PIP_CONSTRAINT`**
  - It is accepted only because it is on the workflow `env:` allowlist (`ci/image/syntax-census.json:1306`, enforced by `scripts/ci_syntax.py:36`). Any other `PIP_*` name is refused as unmodelled.
  - The value must fullmatch `${{ github.workspace }}/<path>` and name a file (`scripts/ci_tool_inventory.py:75`).
  - Every non-comment line must fullmatch `name @ https://files.pythonhosted.org/packages/…/<file>#sha256=<64 hex>`, and the name must agree with the archive's file name. Duplicates are refused (`:86`).
  - An unpinned request takes the constraint's pin, and a pinned one must agree with it (`:109`).
  - The constraints file's digest is an inventory input (`derive`), so changing it fails `--check`.
  - Indented comments, inline comments, markers, nested `-r`/`-c` and `pip -c` all refuse. Closed.
- **`apt-get -o`**
  - Only `apt-get -o Dir::Cache::archives=${RUNNER_TEMP}/<word> install …` is rewritten (`:166-170`).
  - A second `-o`, a glued `-oX`, `-o … update` and any other option fall through to "unsupported installation command" or "unsupported apt option". Closed.
- **`python3 -m venv DIR`.** Exactly four words, with no option (`:179-182`). Closed.
- **`ci_install_cache.py`.** It downloads without installing, so its own step requests nothing; the next step's `apt-get` request names the packages. In the trace it is a `REMOVED` line (`ci/image/audit_population.py`). Closed.
- **Shell `[[ ]]`** (`scripts/ci_syntax.py:55`)
  - The census admits only `BinaryTest.Op` 40, the `==` match (`syntax-census.json:1223`). `UnaryTest` and `ParenTest` have no census fields, so they refuse.
  - The arithmetic set `:52` is a second line of defence.
  - Both branches continue, and substitutions in the words are walked. Closed.
- **Make forms** (`scripts/ci_make_walk.py`)
  - A single `\#` is unescaped; longer runs and in-reference forms refuse (`:119`).
  - `$(eval)` is allowed only in a whole-line parse-time expansion, as one literal assignment that is not sensitive or unmodelled and contains no `$`; elsewhere it refuses (`:503`, `:513`).
  - Static pattern rules must have literal targets, one `%` and a matching stem, and must not redefine a target (`:664`).
  - A computed name must expand to a static `NAME` (`:362`), and the `UNMODELLED` and `MAKEFLAGS` refusal in `variable()` still applies.
  - A quoted runtime `-j` is one argument (`:220`).
  - Each form has a differential fixture: `scripts/ci_differential_fixtures.py:274-288`, plus the `bash-test-clause` fixtures at `:141`.
  - My probes (`receipts/probe-make-walker.json`) reproduce 8 of 10 extra forms identically against GNU Make: the command-line override of an eval'd value, `-` in names, `\#` in both recipe forms, a two-`%` static prerequisite, a nested computed name, and `$(or)` with whitespace.
  - The other two diverge: R638-10-R1.
- **Exact version queries** (`ci/image/exec_operands.py:245`, `:277`). Only the argv `--version`/`-V` (python) and `--version`/`-v` (node) skip program judgment. `python3 --version -c …` is still judged, and the self-test control covers it (`ci/image/exec_audit_selftest.py:288-292`; the author's image run shows 76/76). Closed.
- **Fixed-program data slot** (`scripts/ci_command_table.py:379`). It accepts one literal, non-option, non-runtime operand. The program text is pinned exactly, so the operand cannot change what runs. Controls: `scripts/ci_inventory_patterns_selftest.py:126-133` covers an option, a runtime word and a second file. Closed.

**Changed self-test control.** `scripts/ci_inventory_exact_selftest.py:43` changed its escaped-`#` control from `a\#b` to `a\\#b`. This is not a weakening: the single-backslash form is now modelled and proven identical by `make-escaped-number-sign`, and the two-backslash form still refuses by the same name.

### (3) The re-trace

**Coverage.**
- `reconciliation` has 230 rows: 97 rtl-fast, 87 docs and 46 elaborate. 195 are traced and 35 are not: 30 rows from `ci-manifest`, `ci-fail-fast` and `ci-cancel-tail`, and 5 cache-miss Verilator and Yosys builds.
- All 195 steps exit 0 and are clean, with 0 findings and 320,983 instances.
- I enumerated the population independently from the workflow YAML. Every `run` step of the docs gate legs and `docs-check`, of every rtl-fast job, and of the elaboration legs and `elaborate`, plus the orchestration jobs, is in the reconciliation, and there are no extras.

**Out of the population, unchanged from the positive `6f86eee6`:** docs `wire-accountability` and `docs-check-no-git`, and every `rtl.yml` job. At `6f86eee6`, `WORKFLOWS` already listed only `docs-check` from docs. The inventory walks every workflow.

**#745's budget step.** "Set CPU-derived job budgets" is untraced in the 9 orchestration rows. Its text (`text_sha256` `ca8fbe7d…`) is byte-identical to the 19 traced instances, so the step text itself is traced.

**Listed commands.** 115 listed, all observed; 111 with the listed arguments. The other 4 are runner values:
- `--base` full SHA;
- builder leg selection;
- `--jobs "$CI_CAMPAIGN_JOBS"`;
- `--jobs "$CI_CENSUS_JOBS"` (observed 7).

The list carries a stand-in `1` for the last one, as at `6f86eee6`.

**Reviewed lists.**
- Inline and streamed: the set of `(inline|stream, pinned)` digests in the receipt equals the 108 keys of `inline_programs` exactly, with 0 unused and 0 unlisted (`receipts/reviewed-lists-usage.txt`).
- Generated (461): exact use cannot be recomputed from the committed receipt, because generated rows carry no digest. This is retained as R639-9-S1 (see the limits).

**Decision point 1 (scope-text entries name the generated workflow).** Accepted. `scripts/ci_scope_history.py:146` reads `.github/workflows/<workflow>`, so `source: .github/workflows/<x>.yml` names what the self-test actually runs. No entry still says "historical revision".

**Decision point 2 (`--base fa7347fc` superset trace).** Accepted.
- The diff-scoped gates in the trace see `fa7347fc..54fbcba6a`, a superset of the PR's diff against `4a9b5a2a`.
- The added-line gates are monotone in that set, and no reached step was skipped.
- The final check re-ran `check_em_dash.py --base 4a9b5a2a` (0 findings, 909 added lines), and I reproduced it (`receipts/head-checks/em-dash.log`).

### (4) Prior residue

- **R638-9-R2: applied verbatim.** It is `docs/testing/CI_IMAGE.md:107-108`, placed after the exec-target line.
- **R638-9-R3: applied verbatim.**
  - The PR body's Round 9 row "Accepted sources (N3)" (body line 333) carries the reviewer's exact text.
  - The Round 8 row reads "Inline and streamed programs (superseded in Round 9)" (body line 291).
- **Not taken here, as the assignment directs (to #495):** R638-9-R1 and R638-9-S1 to S4. They are retained, not resolved.
- **R639-9-S1 to S3: retained.** They are optional, and the delta does not address them.

## Findings

### R638-10-R1 RESIDUE (class ruling; code): an `$(eval)` in a `$(foreach)` body that assigns the loop variable is modelled wrongly

- **Lenses:** Robustness, Tests, Conformance.
- **Where:** `scripts/ci_make_walk.py:450-462` (the `foreach` bind and restore) and `:513` (`evaluate`).
- **Evidence:** `receipts/probe-make-walker.json`, using the harness's own `build`/`walk`/`run`/`outcome`, against GNU Make on the host.
  - `X = outer` / `$(foreach X,a b,$(eval X := z$(X)))` / `all: ; zz_probe "$(X)"`
    - The walker resolves `outer`; make runs `zb`.
    - In make, the loop variable lives in a pushed scope and `eval` defines globally. The walker restores the saved value over the eval'd one.
  - `$(foreach X,a,$(eval X := q)$(eval Y := $(X)))` / `all: ; zz_probe "$(Y)"`
    - The walker resolves `q`; make runs `a`. Inside the iteration, the loop scope shadows the eval'd global.
  - Both outcomes are `mismatch`.
  - The comment at `:450` says "as in make", which is not true for this sub-form.
- **Why RESIDUE and not MAJOR:**
  - The form is accepted only inside the censused `make:expansion-line` and `make:function.eval` shapes, with a focus fixture, which the round-8 ruling treats as closed by construction ("implements … semantics with differential fixtures").
  - The divergence needs an `$(eval)` that reassigns the very loop variable, a contrived form that no tree Makefile uses. The tree's only use is `tb/verilator/milan_dp/Makefile:561`, which assigns `RECEIPT_$(case)`.
  - At runtime, the exec audit judges what actually runs.
- **Exact fix (optional code):** in `evaluate`, refuse by name an assignment whose name is a currently bound `foreach` variable. Track the bound names in a set pushed and popped around the loop at `:450`. Add a `refused` differential fixture with the first probe above.
- **Verification:** that fixture refuses with the new name, and `ci_differential.py --check` re-measures in the image.

### R638-10-R2 RESIDUE (wording, guide): "as the documented adoption has it" cites a section that does not say it

- **Lenses:** Docs.
- **Where:**
  - `docs/testing/CI_IMAGE.md:562`, "The job-private Python environment is the image's Python layer, as the documented adoption has it."
  - The adoption section (`:861-911`) mentions only `ci_litex_env.py --check`, the patches and RV32. It never mentions the job-private venv step.
- **Impact:** none on any measurement or artifact; the sentence's cross-reference is untrue.
- **Exact fix:** replace the sentence with:

  ```text
  The job-private Python environment step runs as an import check of the image's Python layer.
  ```

- **Verification:** doc-style, the em-dash check with `--base 4a9b5a2a`, and the TOC gate pass.

### R638-10-R3 RESIDUE (wording, guide): the receipt's untraced rule is stated as "replaced" only

- **Lenses:** Docs.
- **Where:** `docs/testing/CI_IMAGE.md:596`, "Every untraced step must also be one the image replaces."
  - As built, `untraced()` (`ci/image/audit_population.py:314`) also accepts the orchestration reason.
  - The guide's own `:553-554` says those steps are named, untraced.
- **Exact fix:** replace the sentence with:

  ```text
  Every untraced step must be one the image replaces or a run-orchestration step.
  ```

- **Verification:** as for R2.

### R638-10-R4 RESIDUE (wording, source comment): a fixture comment sits above the wrong fixture

- **Lenses:** Docs, Tests.
- **Where:** `scripts/ci_differential_fixtures.py:284`.
  - "# One backslash quotes a number sign in a makefile line, and is removed." precedes `make-eval-in-recipe` (`:285`).
  - It describes `make-escaped-number-sign` (`:287`).
- **Exact fix:** move that comment line to directly above `:287`. Optionally, put `# An $(eval) inside a recipe refuses by name.` above `:285`.
- **Verification:** the change is comment-only, but `binding()` (`scripts/ci_command_table.py:20-22`, `:110`) hashes this file's bytes. Moving the comment therefore needs a re-measured differential receipt in the image. Through `ci/image/differential-receipt.json`, which is an inventory input, it also needs the inventory, recipe and lock to be regenerated. Batch it with the next re-measure (for example R1's), not on its own.

### Suggestions (non-blocking)

- **R638-10-S1 (Docs; manager merge turn).** The author's open risk 5 says live `dev` `1f6f2f57` "touch[es] none of this PR's files". That is literally true, but `scripts/check_doc_style.py` is an inventory input: its digest is in `tool-inventory.json` `inputs`.
  - In a disposable copy of the head plus `dev` `4a9b5a2a..1f6f2f57`, `ci_tool_inventory.py --check` returns rc 2, "REFUSED: tool inventory differs from workflow installation requests" (`receipts/candidate-1f6f2f57-inventory-check.log`).
  - Regenerating changes only that one digest (`receipts/candidate-1f6f2f57-inventory-regenerated.diff`). It also moves the recipe to `f4309171c5044b47…`, so `--check-lock` then refuses the lock (`receipts/candidate-1f6f2f57-check-lock.log`).
  - Suggested outcome: state this in the risk. Any `dev` change to any of the 378 inventory inputs needs a regeneration, two cold builds, the lock and a re-trace before merge.
  - This is not a defect at this head, which validates against its assigned base `4a9b5a2a`.
- **R638-10-S2 (Tests, Robustness).** The escaped-`#` and `-`-in-name forms record no census shape: `make-escaped-number-sign` and `make-runtime-jobs` have `shapes: []`.
  - Every other modelled form names where the tree uses it through its shape.
  - Recording `make:escaped-number-sign` and `make:name.dash` (or similar) would put them under the same focus-fixture gate.
- **R638-10-S3 (Docs).** The adoption section does not say what the switch lane does with the job-private venv step or with "Install sbt", both of which the trace replaces: `REPLACED` gives `python3 -c 'import litex, migen, yaml'` and `sbt --script-version`.
  - A line for each in `## CI and act adoption` would let the switch lane reproduce the traced form exactly, as it does for RV32 and `ci_litex_env.py`.
  - In an adopted job container, `python3 -m venv` without system site-packages would hide the image's Python layer.
- **R638-10-S4 (Tests; retained R639-9-S1).** Generated-program use (461) cannot be recomputed from the committed receipt. Keeping the matched digest in generated population rows would make "used exactly" checkable from the public receipt, as it already is for the 108 inline entries.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merge `03dcd0c36` against the `merge-tree` replay. `scripts/check_baremetal_only.py:1303,1384,1417,1861`. Gitlinks. Regenerated inventory, sources lock, recipe and lock (`--check`, `--check-lock`). `ci/image/exec-audit-receipt.json` reconciliation and 115 commands. Decision points 1 and 2 (`scripts/ci_scope_history.py:146`). R638-9-R2 at `docs/testing/CI_IMAGE.md:107-108`, R638-9-R3 in the PR body at lines 291 and 333. | R638-10 | `d7cb1f90af1b8c2f115f58281991f1c9626447f9` |
| RTL | CLEAN (scope inapplicable) | `receipts/pr-vs-merged-dev-files.txt`: no HDL, `tb/`, `syn/`, `sw/` or submodule file differs from merged `dev` `4a9b5a2a`. The delta's own files are CI, image and docs only. Gitlinks equal `dev`'s. | R638-10 | `d7cb1f90af1b8c2f115f58281991f1c9626447f9` |
| Robustness | CLEAN (R1 is RESIDUE by class ruling) | `scripts/ci_tool_inventory.py:75,86,109,166-182`. `scripts/ci_syntax.py:36,52,55` with `ci/image/syntax-census.json:1223,1306`. `scripts/ci_make_walk.py:119,220,362,450,503,513,664`. `ci/image/exec_operands.py:245,277`. `scripts/ci_command_table.py:379`. `ci/image/audit_population.py:53,62,314,333`. 10 walker probes. | R638-10 | `d7cb1f90af1b8c2f115f58281991f1c9626447f9` |
| Tests | CLEAN (R1 and R4 are RESIDUE) | `scripts/ci_differential_fixtures.py:62-66,141-146,264-288`. `scripts/ci_inventory_patterns_selftest.py:126-133,282-288`. `scripts/ci_inventory_exact_selftest.py:43`. `ci/image/exec_audit_selftest.py:288-292`. 20 head checks at rc 0 under CPython 3.12.3 (`receipts/head-checks/`), plus em-dash and TOC at rc 0 under the renderer environment. | R638-10 | `d7cb1f90af1b8c2f115f58281991f1c9626447f9` |
| Docs | CLEAN (R2, R3 and R4 are RESIDUE) | `docs/testing/CI_IMAGE.md` delta (`:30-36`, `:104-108`, `:114-119`, `:133-160`, `:169-170`, `:460`, `:548-583`, `:596`, `:861-911`). The PR #738 body Status and Round 10 sections. Comment-rule scan of the added lines: no lane labels, review rounds, reviewer IDs or comment IDs. | R638-10 | `d7cb1f90af1b8c2f115f58281991f1c9626447f9` |

Every row is banked at the exact head under review.

## Real limits

- **No image rebuild or trace.** I did not rebuild the image or re-run the traced population; that needs Docker. Image identity, the two cold builds, the 76 image controls and the 195-step trace rest on the author's published receipts at `f308bf87` `author-r10/`. I cross-checked them for internal consistency against the committed receipt and the head's recipe digest.
- **Different tool versions for the walker probes.** They ran against GNU Make 4.4.1 on the host, not the image's 4.3. The divergence in R1 is the long-standing `foreach` scope and global `eval` semantics, but I did not re-measure it in the image. The host `/bin/sh` is not `dash`; the probes avoid shell-specific recipe syntax.
- **Interpreter for the renderer gates.** `check_em_dash.py` and `gen_toc.py --check` ran under a CPython 3.14 environment holding the pinned renderer, not under 3.12.3.
- **Generated-list use.** Use of the 461 generated entries is not recomputable from public artifacts (S4); the inline list is verified exactly.
- **Hosted CI.** At snapshot time (`receipts/hosted-checkruns-snapshot.tsv`), 23 contexts had succeeded, 25 were queued or in progress, and 1 was skipped. Hosted and act acceptance is the manager's.
- **No physical evidence.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **No manager source bank.** None runs at this head, and none is claimed.

## Pending manager duties

- **Merge turn.** Against live `dev` `1f6f2f57`, the inventory refuses (S1). The candidate needs `ci_tool_inventory.py --write`, a recipe change to `f4309171…`, two cold builds with `--record-lock` and `--check-lock --verify-archive`, and a re-trace receipt at the candidate. The alternative is to merge only once `dev` changes no inventory input.
- **Hosted and act acceptance.** Exact-head hosted contexts and the act replay of the merge candidate.
- **Residue checklist.** Carry R638-10-R1 to R4 to the residue checklist. Optional code in R1 and S2/S3 is the manager's call. R638-9-R1 and S1 to S4, and R639-9-S1 to S3, go to #495 as assigned.
- **Not done here.** No registry login or push is part of this PR, and none was done.

## Receipts

- Every published file is listed in `MANIFEST.sha256`.
- `reproduce.sh` and `probe_make_walker.py` are portable.
- The clone was restored to the exact head: worktree, index and tree `c32f2994…` equal HEAD, there are 0 status lines, and the six gitlinks match (`receipts/clone-restore-check.txt`).

R638-10 FINISHED
