# HANDOFF: #797 D0 round 6 (dev sync and inventory regeneration), executor [A706f]

Status: **STOP** at head `430a077c0e9a5a42062103742a8f3f1b8bacc6b8`, local branch `797-d0-audit`, not pushed. PR #815 still points at `e8ec8d20`. The merge and the regeneration are committed and every assigned gate but one is rc 0. The image command-table checker, `python3 scripts/ci_tool_inventory.py --check`, exits 2 on the head. It exits 2 with the same refusal on dev `604899c0` itself, on round 5's head and on the old merge base, and regeneration cannot fix it. The assignment's rule for a gate that fails for a reason the regeneration cannot fix is STOP with the log, so this round stops there ([STOP](#stop-the-image-command-table-checker)).

- origin is `https://github.com/kebag-logic/milan-fpga.git`. The lane branched from dev `1e80128f` (`git merge-base --is-ancestor 1e80128f HEAD` rc 0).
- Round 6 adds two commits on top of `e8ec8d20`: one merge, one regeneration. No rebase, no amend, no force.
- `git merge-base --all origin/dev HEAD` gives one base, `604899c0`, in a clean clone and in the lane. `git ls-remote` read dev at `604899c0` during the gates (`receipts/gates/lane/ls_remote_dev.log`).
- No git command was run inside a submodule. Pins are unchanged: processor `a9e84b66`, gPTP `135afd04`.
- Round 5 handoff: `../797-a706e/HANDOFF.md`. Reviews: R741-5 and R742-5 POSITIVE at `e8ec8d20`; the composition on dev `297b642f` POSITIVE (R741-6).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6634824794
- STOP: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6635537751

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject | Content |
|---|---|---|
| `626d367f` | Merge dev 604899c0 into 797-d0-audit | `git merge --no-ff origin/dev`, with the dev SHA read by `git rev-parse --short=8 origin/dev`. Parents `e8ec8d20` and `604899c0`. 15 files from dev (PR #836), auto-merged |
| `430a077c` | Regenerate the documentation inventory on the merge of dev 604899c0: 213 pages, 176 current and 16 stale (#797) | `docs/DOCUMENTATION_AUDIT.md` only: 6 insertions, 6 deletions, written by `python3 scripts/docs_inventory.py --write` |

## Conflicts

None. One file changed on both sides, `ci/image/command-table.json`, and git auto-merged it ("Auto-merging ci/image/command-table.json", no conflict markers):

| Side | Rows in `ci/image/command-table.json` |
|---|---|
| Lane (since `e61a4afa`) | the `git -C <runtime> ls-files -z` pattern; the `scripts/docs_inventory.py --check` and `--selftest` patterns; the `scripts/docs_inventory.py` declaration with its sha256 |
| Dev (PR #836) | re-pinned `scripts/ci_gate_workflows_selftest.py`, `scripts/ci_scope_history.py` and `scripts/run_litex_sims.sh`; new declaration `scripts/ci_litex_legs.py` |
| Merged (`626d367f`) | every row of both. `git diff 604899c0 HEAD -- ci/image/command-table.json` is the lane's 19 added lines only, and `git diff e8ec8d20 HEAD --` the same file is dev's 11-line change only |

Nothing was re-pinned by hand. At the head, all five digests named above equal their file bytes (`receipts/command-table/probe.log`, written by `tools/command_table_probe.sh` with `tools/table_digests.py`). Neither `scripts/docs_inventory.py`, `scripts/docs_inventory.json` nor `docs/DOCUMENTATION_AUDIT.md` changed on dev, so after the merge the three were byte-identical to `e8ec8d20` (`receipts/regen/inventory-files-unchanged-by-merge.txt`).

## Each change, with file:line and its reason

Every line below was written by the generator. None was edited by hand. The compared rows come from `receipts/regen/compare-e8ec8d20-430a077c.txt`, written by `tools/compare_audit.py`, which reads both pages with `git show`.

| Change at `430a077c` | Reason (dev's change that caused it) |
|---|---|
| `docs/DOCUMENTATION_AUDIT.md:30` current lines 73,277 -> 73,487 (pages 176, unchanged) | PR #836 added 210 lines to `docs/testing/CI_WORKFLOWS.md`, a current page |
| `docs/DOCUMENTATION_AUDIT.md:31` stale lines 10,630 -> 10,638 (pages 16, unchanged) | PR #836 added 8 lines to `docs/testing/TESTING.md`, a stale page |
| `docs/DOCUMENTATION_AUDIT.md:34` total lines 91,909 -> 92,127 (pages 213, unchanged) | The sum of the two |
| `docs/DOCUMENTATION_AUDIT.md:332` `docs/testing/CI_WORKFLOWS.md` 3414 -> 3624 lines, still current | PR #836's three-leg `elaborate` section |
| `docs/DOCUMENTATION_AUDIT.md:337` `docs/testing/TESTING.md` 1927 -> 1935 lines, still stale with D0-057 | PR #836's `--only` line and leg paragraph |
| `docs/DOCUMENTATION_AUDIT.md:540` D0-057 on `docs/testing/TESTING.md`: line 1810 -> 1818 | The same eight lines are above it; the statement is unchanged |

The assignment's "words" are the page's Lines column: the audit counts lines, not words. No page was added or removed, and no page changed status. No finding row was added, removed, or newly marked "re-verify"; no statement cell changed. Finding rows stay 76 (11 copies). Dev's merge fixed or removed no finding. D0-001, D0-033 and D0-056 still read "re-verify: quote not found", as in round 5.

## Generator and freshness gate

- Generator: `python3 scripts/docs_inventory.py --write`, which writes only `docs/DOCUMENTATION_AUDIT.md`. `--findings-dir` writes outside the tree. `scripts/docs_inventory.json` is the generator's input: no mode of the generator writes it, so it is unchanged here.
- Gate: `--check`. Self-test: `--selftest`, 50 controls.
- Before the write, on the merged tree: `--check` rc 1, "STALE (6 lines differ); first difference at line 30", committed `| current | 176 | 73,277 |` against generated `| current | 176 | 73,487 |` (`receipts/regen/check-merged-before-write.log`, `.rc`). After: `--write` rc 0 and `--check` rc 0 (`write.log`, `check-after-write.log`).
- **Planted stale-page mutants on fresh clones of `430a077c`** (`tools/stale_page_mutants.sh`, `receipts/probes/stale-page-mutants.txt`, rc 0). In every arm the clean head gives `--check` rc 0, the planted tree gives `--check` rc 1, and `--write` then `--check` give rc 0:
  - `append-line`: one line appended to `docs/testing/CI_WORKFLOWS.md`, the page PR #836 grew. The diff is its line count (3624 -> 3625) and the totals.
  - `d0-057-copy-removed`: the D0-057 copy on `docs/testing/TESTING.md:1818` reworded ("is pinned at the Milan 2 ms DEFAULT" -> "defaults to the Milan 2 ms"). The copy row leaves and the page renders current (current 176 -> 177, stale 16 -> 15). So the moved row is the one the search finds on the merged tree.
  - `d0-001-copy`: the D0-001 statement put back on `REQUIREMENTS.md`. Its copy row returns and the page renders stale (current 176 -> 175, stale 16 -> 17). So the cross-page search still runs on the merged tree.

## Findings per area

Generated by `python3 scripts/docs_inventory.py --findings-dir findings` from a clean clone of `430a077c` (`receipts/regen/findings-dir.log`, rc 0). The notes are in `findings/README.md`. Only `findings/testing-and-ci.md` differs from round 5's, in the D0-057 line (1810 -> 1818).

| Area | Rows | Copy rows | Of which "re-verify" | File |
|---|---:|---:|---:|---|
| reference (with integration) | 54 | 0 | 2 (D0-033, D0-056) | `findings/reference.md` |
| overview and guides | 11 | 0 | 1 (D0-001) | `findings/overview-and-guides.md` |
| design | 1 | 1 | 0 | `findings/design.md` |
| testing and CI | 1 | 1 | 0 | `findings/testing-and-ci.md` |
| archive (recorded, not to be rewritten) | 9 | 9 | 0 | `findings/archive.md` |
| **total** | **76** (unchanged) | **11** (unchanged) | **3** | |

## STOP: the image command-table checker

`receipts/command-table/probe.log` (rc of the probe script 0; the rcs below are each run's own), from `tools/command_table_probe.sh` with the pinned parser that `ci/image/prepare_parser.py` fetched and authenticated (shfmt v3.11.0, kept outside the tree and the output directory). Each run is on a fresh clean clone with its submodules:

| Tree | `python3 scripts/ci_tool_inventory.py --check` | Declared script digests that do not match the bytes, or whose file is missing |
|---|---|---:|
| `430a077c` (head) | rc 2, `REFUSED: changed declared script 'sw/builder/endstation_builder.py'` | 35 |
| `626d367f` (merge) | rc 2, same refusal | 35 |
| `604899c0` (dev) | rc 2, same refusal | 35 |
| `e8ec8d20` (round 5 head) | rc 2, same refusal | 37 |
| `e61a4afa` (round 5 merge base) | rc 2, same refusal | 37 |

- The 35 at the head are dev's 35, entry for entry: 34 stale digests and the missing `tb/verilator/render_setpoint/mutants.py`. The lane's declaration (`scripts/docs_inventory.py`) and dev's four PR #836 rows all match their bytes at the head. The merge added no mismatch.
- The refused digest has been stale on dev since before the lane branched: `sw/builder/endstation_builder.py` is declared `84878e53...` at `1e80128f`, `e61a4afa` and `604899c0`, and its bytes hash to `025882ac...` at `e61a4afa` and later.
- In a disposable copy of the head only, re-pinning that one digest to the file's bytes moves the refusal to `REFUSED: uncensused Python builtin 'exec' at sw/builder/endstation_builder.py` (rc 2). So the fix is more than a digest: the builder uses a construct the walker's census does not hold. Regeneration of the audit page cannot reach it, and changing the table or the census is outside this round's scope.
- What does pass at the head: the docs workflow's own inventory step walked alone through the command-table walker (`tools/walk_inventory_step.py`, round 4's tool): `walked: ['scripts/docs_inventory.py']`, `residue: []`, `OK`, rc 0.
- No PR workflow runs `ci_tool_inventory.py --check` (a search of `.github/workflows/` and `.github/ci-templates/` finds none), so no hosted context reads this.

**Decision needed (manager):** accept the checker as dev's pre-existing failure, with the lane's rows shown consistent above, or send the stale table and the census gap to their own Issue first. This lane did not post REVIEW READY.

## Gates

All ran on clean clones of `430a077c` and none was piped. The runner and verifier are in `receipts/gates/tools/`, round 5's copies with this round's scratch paths; `not_run.json` and `rtl_fast_not_run.json` are unchanged. `select_rtl_fast.py` on the head picks the same 45 steps as round 5. Neither workflow changed on dev. Both tables below have the same rows, rcs and reasons as round 5's.

| Gate | Result | Receipt |
|---|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 65 steps rc 0, 31 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/docs-yml-table.md`, `docs-yml-verify.rc`, `receipts/gates/docsyml/` |
| Of those: `docs_check.py` (gate_7, 0 findings across 213 pages; and with git stripped in `docs-check-no-git` ci_step_3), `check_doc_style.py` (gate_9), em-dash (gate_8, `[604899c0..HEAD]`, 0 findings over 534 added lines), bare-metal scope (gate_21), cited paths (gate_43), TOC and anchors (gate_45), inventory `--check` and `--selftest` (gate_46) | rc 0 each | `receipts/gates/docsyml/docs-gates-0__gate_*.log` |
| Every step of `.github/workflows/rtl-fast.yml` that reads `scripts/` or `docs/` | 17 steps rc 0, 28 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/rtl-fast-table.md`, `rtl-fast-verify.rc`, `receipts/gates/rtl-fast/` |
| `python3 scripts/docs_inventory.py --check` | rc 0, "OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)" | `receipts/gates/lane/inventory_check.log` |
| `python3 scripts/docs_inventory.py --selftest` | rc 0, 50 controls | `receipts/gates/lane/inventory_selftest.log` |
| `python3 scripts/pp_srcs.py --check` and `--check --selftest` | rc 0 each | `receipts/gates/lane/pp_srcs_check.log`, `pp_srcs.log`; also rtl-fast `verilator-lint__ci_step_8.log` |
| Image command-table checker, `python3 scripts/ci_tool_inventory.py --check` | **rc 2** on the head and on dev (above) | `receipts/command-table/probe.log` |
| `git diff --check $(git merge-base origin/dev HEAD) HEAD` | rc 0 | `receipts/gates/lane/diffcheck.log` |
| `git merge-base --all origin/dev HEAD` is one commit | rc 0, `604899c0` in the clone and in the lane | `receipts/gates/lane/merge_base_all.log`, `merge_base_all_lane.log` |

Every job's clone was clean and at `430a077c` after its steps (`*__tree-after.txt`, `receipts/gates/lane/tree-after.txt`). The exception is `docs-check-no-git`, whose step strips the git metadata. `docs-gates-2__gate_41.log` was over 200 KB, so it is a `.sha256.txt` record. No step failed and none was retried. `docs-gates-1`, `docs-gates-2` and the rtl-fast jobs started only after `docs-gates-0` had installed the RV32 SDK (its `ci_step_28` rc 0).

**Other differences from the hosted run** (as in round 5): the pinned Verilator's directory is substituted for `/opt/verilator/bin`; `changes/scope` runs in the replay form (`ACT=true`, base `origin/dev` at `604899c0`); Yosys and sv2v were already on `PATH`, so the install steps were not run; `firmware-boundary` ran with a LiteX interpreter first on `PATH` (a scratch virtualenv of another lane that imports `litex` and `migen`).

## Resources

The docs jobs and lane gates ran first, then `docs-gates-1`, `docs-gates-2` and nine rtl-fast jobs in parallel, all inside this unit. The unit's `memory.peak` read **10.8 GB** at the end, over the 8 GB target and under the 12 GB cap. That figure includes page cache from the clones: `memory.stat` read anonymous memory at 0.3, 3.0 and 0.7 GB at the three samples, and file cache at 9.8 GB at the first. Host MemAvailable read 56.8 to 60.1 GB at each sample. No Vivado, no sweep, no hardware.

## Open decisions and limits

1. **The STOP above.**
2. **Hosted CI has not run on this head; it is not pushed.** The local replica (`act_ci.py`) was not run.
3. **No statement or citation was re-verified this round.** Dev's new lines in `docs/testing/CI_WORKFLOWS.md` and `docs/testing/TESTING.md` were not checked.
4. Round 5's other open items carry over unchanged: D0-001, D0-033 and D0-056 and the "Mark II default" decision; the owner additions of 2026-10-30; the two scope-addition statements; the `also` breadth; the unextended sampling.

## Receipts

`receipts/INDEX.md` is generated from the files present by `python3 -I tools/receipt_index.py <output dir>`. Tools added this round: `tools/command_table_probe.sh`, `tools/table_digests.py`, and round 4's `tools/walk_inventory_step.py`; `tools/stale_page_mutants.sh` has round 6's three arms.

## Docs workflow gate table

| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | `wire-accountability__ci_step_1.log` |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | `wire-accountability__ci_step_3.log` |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | `wire-accountability__ci_step_4.log` |
| wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | `docs-check-no-git__ci_step_1.log` |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | `docs-check-no-git__ci_step_2.log` |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | `docs-check-no-git__ci_step_3.log` |
| docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-0__ci_step_1.log` |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | `docs-gates-0__gate_1.log` |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | `docs-gates-0__ci_step_5.log` |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | `docs-gates-0__ci_step_7.log` |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | `docs-gates-0__gate_7.log` |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | `docs-gates-0__gate_8.log` |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | `docs-gates-0__gate_9.log` |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | `docs-gates-0__gate_10.log` |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | `docs-gates-0__gate_11.log` |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | `docs-gates-0__gate_12.log` |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | `docs-gates-0__gate_13.log` |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | `docs-gates-0__gate_14.log` |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | `docs-gates-0__gate_15.log` |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | `docs-gates-0__gate_16.log` |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | `docs-gates-0__ci_step_21.log` |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | `docs-gates-0__gate_18.log` |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | `docs-gates-0__gate_19.log` |
| docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | `docs-gates-0__gate_21.log` |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-0__ci_step_28.log` |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | `docs-gates-0__gate_24.log` |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | `docs-gates-0__gate_26.log` |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | `docs-gates-0__gate_27.log` |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | `docs-gates-0__gate_28.log` |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | `docs-gates-0__gate_29.log` |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | `docs-gates-0__gate_30.log` |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | `docs-gates-0__gate_31.log` |
| docs-gates-0 | gate_32 | Port contract gate | 0 | `docs-gates-0__gate_32.log` |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | `docs-gates-0__gate_33.log` |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | `docs-gates-0__gate_34.log` |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | `docs-gates-0__gate_35.log` |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | `docs-gates-0__gate_36.log` |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | `docs-gates-0__gate_37.log` |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | `docs-gates-0__gate_38.log` |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | `docs-gates-0__gate_39.log` |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | `docs-gates-0__gate_40.log` |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | `docs-gates-0__gate_43.log` |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | `docs-gates-0__gate_44.log` |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | `docs-gates-0__gate_45.log` |
| docs-gates-0 | gate_46 | Documentation inventory freshness gate | 0 | `docs-gates-0__gate_46.log` |
| docs-gates-0 | gate_47 | AEM store generator self-test | 0 | `docs-gates-0__gate_47.log` |
| docs-gates-0 | gate_48 | Sweep/build shape gate | 0 | `docs-gates-0__gate_48.log` |
| docs-gates-0 | gate_49 | Deploy shape gate | 0 | `docs-gates-0__gate_49.log` |
| docs-gates-0 | gate_50 | Entity shape gate | 0 | `docs-gates-0__gate_50.log` |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 | `docs-gates-0__ci_step_53.log` |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | `docs-gates-0__gate_51.log` |
| docs-gates-0 | ci_step_55 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context; this workflow's id for the step the assigned list names ci_step_54. Round 4 tried it once: it refuses on the runner's local submodule origin (../797-a706d/receipts/gates/env-first-attempts/docs-gates-0__ci_step_55.log) |
| docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-1__ci_step_1.log` |
| docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-1__ci_step_3.log` |
| docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-1__ci_step_5.log` |
| docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-1__ci_step_9.log` |
| docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-1__ci_step_13.log` |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | `docs-gates-1__gate_25_0.log` |
| docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-2__ci_step_1.log` |
| docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-2__ci_step_3.log` |
| docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-2__ci_step_5.log` |
| docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-2__ci_step_9.log` |
| docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-2__ci_step_13.log` |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | `docs-gates-2__gate_25_1.log` |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | `docs-gates-2__gate_41.log` |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | `docs-gates-2__gate_42.log` |
| docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check | ci_step_1 | Set CPU-derived job budgets | NOT RUN | this job has no local gate |
| docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only docs-check's hosted verify uses |
| docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies uploaded hosted receipts; this job's gates ran above |
| docs-check | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration, no local gate |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | cancels a hosted run |

65 steps ran, 31 not run with a reason, 0 bad

## rtl-fast gate table

| Job | Step | Name | Reads | rc | Log |
|---|---|---|---|---:|---|
| changes | scope | Classify the change conservatively | direct | 0 | `changes__scope.log` |
| changes | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | direct | 0 | `verilator-lint__ci_step_7.log` |
| verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | direct | 0 | `verilator-lint__ci_step_8.log` |
| verilator-lint | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| bdd-conformance | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| yosys-tool | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | through syn/yosys/run.sh | 0 | `yosys-elaboration__ci_step_7.log` |
| yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | through syn/ooc/dp_srcs.py, syn/ooc/pp_resource_gate.py | 0 | `yosys-elaboration__ci_step_8.log` |
| yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | through syn/yosys/ooc_selftest.py | 0 | `yosys-elaboration__ci_step_9.log` |
| yosys-elaboration | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| publication-census | ci_packages_3 | Resolve exact package downloads 3 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| publication-census | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | through sw/firmware/gtest/tally_selftest.py | 0 | `firmware-unit__ci_step_7.log` |
| firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-unit__ci_step_9.log` |
| firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | through sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py | 0 | `firmware-unit__ci_step_11.log` |
| firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | through sw/firmware/gtest/fw_coverage.py | 0 | `firmware-unit__ci_step_12.log` |
| firmware-unit | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-control-mutants__ci_step_8.log` |
| firmware-control-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-aecp-mutants__ci_step_8.log` |
| firmware-aecp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-srp-mutants__ci_step_8.log` |
| firmware-srp-mutants | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-boundary__ci_step_8.log` |
| firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-boundary__ci_step_9.log` |
| firmware-boundary | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | direct | NOT RUN | ci_install_cache resolves apt package downloads; this host has no apt, and the packages are installed |
| firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | direct | 0 | `firmware-verilator__ci_step_13.log` |
| firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | through sw/firmware/ctrl/test/ctrl_boundary.py | 0 | `firmware-verilator__ci_step_14.log` |
| firmware-verilator | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | ci_collect | Collect actual runtime evidence | direct | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_observe | Observe the first failed job | direct | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | direct | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | direct | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | direct | NOT RUN | cancels a hosted run |

17 steps ran, 28 not run with a reason, 0 bad
