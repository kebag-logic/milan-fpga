# HANDOFF: #797 D0 round 5 (dev sync and inventory regeneration), executor [A706e]

Status: **REVIEW READY** at head `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63`, local branch `797-d0-audit`, not pushed. PR #815 still points at `8d8c2e36`.

- origin is `https://github.com/kebag-logic/milan-fpga.git`. The lane branched from dev `1e80128f` (`git merge-base --is-ancestor 1e80128f HEAD` rc 0).
- Round 5 adds two commits on top of `8d8c2e36`: one merge, one regeneration. No rebase, no amend, no force.
- `git merge-base --all origin/dev HEAD` gives one base, `e61a4afa`, in a clean clone and in the lane. `git ls-remote` read dev at `e61a4afa` during the gates (`receipts/gates/lane/ls_remote_dev.log`).
- No git command was run inside a submodule. Pins are unchanged: processor `a9e84b66`, gPTP `135afd04`.
- Round 4 handoff: `../797-a706d/HANDOFF.md`. Reviews: R741-4 and R742-4, both POSITIVE at `8d8c2e36`.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6580917076
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6581702893

## Commits (one-line subjects, no body, no trailers)

| Commit | Subject | Content |
|---|---|---|
| `b48b2fd5` | Merge dev e61a4afa into 797-d0-audit | `git merge --no-ff origin/dev`, with the dev SHA read by `git rev-parse --short=8 origin/dev`. Parents `8d8c2e36` and `e61a4afa`. 46 files from dev, auto-merged |
| `e8ec8d20` | Regenerate the documentation inventory on the merge of dev e61a4afa: 213 pages, 176 current and 16 stale (#797) | `docs/DOCUMENTATION_AUDIT.md` only: 43 insertions, 53 deletions, written by `python3 scripts/docs_inventory.py --write` |

## Conflicts

None. Git auto-merged `docs/README.md`, the one file both sides changed. Neither `scripts/docs_inventory.py`, `scripts/docs_inventory.json` nor `docs/DOCUMENTATION_AUDIT.md` changed on dev, so after the merge the three were byte-identical to `8d8c2e36` (`git diff --quiet HEAD^1 HEAD -- ...` rc 0).

## Each change, with file:line and its reason

Every line below was written by the generator. None was edited by hand. The compared rows come from `receipts/regen/compare-8d8c2e36-e8ec8d20.txt`, written by `tools/compare_audit.py`, which reads both pages with `git show`.

| Change at `e8ec8d20` | Reason (dev's change that caused it) |
|---|---|
| `docs/DOCUMENTATION_AUDIT.md:30-34` summary: 212 -> 213 pages; current 166 -> 176; stale 25 -> 16; obsolete 21 | One new page, and nine pages lost their only finding row (below) |
| `docs/DOCUMENTATION_AUDIT.md:36-45` lane table | Same counts per lane: design 1 stale (was 6), overview and guides 2 stale, reference 12 stale |
| `docs/DOCUMENTATION_AUDIT.md:168` new row `docs/design/MARK_II_STREAM_ENGINES.md`, 1288 lines, current, area lane | Added by PR #828 |
| Nine rows go from stale to current: `REQUIREMENTS.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAAP_FABRIC.md`, `docs/fpga/DATAPLANE_WALKTHROUGH.md`, `docs/litex/LITEX_SOC.md`, `docs/overview/ARCHITECTURE.md`, `docs/overview/FULL_FPGA_SOLUTION.md`, `docs/overview/SYSTEM_DOMAIN_MAP.md`, `docs/traceability/ieee8021q.md` | PR #828 reworded each page's "Mark II default" sentence, so D0-001's copy row left. Each page had no other finding |
| D0-001 copy rows also left `docs/fpga/FPGA_DESIGN.md` and `docs/reference/FR_NFR.md`. Both stay stale | Same rewording; both pages keep other findings |
| Line-count cells of pages dev changed, such as `README.md` 482 -> 488 and `docs/reference/FR_NFR.md` 630 -> 642 | Dev's edits |
| `:465` D0-001 `README.md`: line 60 -> "re-verify: quote not found" | PR #828 replaced `README.md:60`'s sentence |
| `:486` D0-033 `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md`: line 23 -> "re-verify: quote not found" | PR #828 replaced the sentence at line 23 |
| `:507` D0-056 `docs/reference/FR_NFR.md`: line 77 -> "re-verify: quote not found" | PR #828 replaced the sentence at line 77 |
| `README.md` D0-002 142 -> 148, D0-003 419 -> 425, D0-004 441 -> 447, D0-005 471 -> 477, D0-046 348 -> 354, D0-047 383 -> 389 | PR #828 added six lines above them in `README.md` |
| `docs/reference/FR_NFR.md` D0-019 173 -> 178, D0-020 277 -> 282 | PR #828 added lines above them |

No other finding row moved, and none changed its statement. No row was added. Finding rows: 87 (22 copies) -> 76 (11 copies). D0-001, D0-033 and D0-056 are marked by the generator's own rule ("re-verify: quote not found"). Their pages stay stale because the entries remain in the data file. Removing the entries would be a data change, which this round does not make.

**The "Mark II default" decision (round 4, open decision 2).** Dev's charter now records an owner decision for the Mark II end state (`docs/reference/FR_NFR.md` NFR-SCOUT-02, citing #665). A grep of `README.md`, `REQUIREMENTS.md`, `docs/reference/FR_NFR.md` and `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md` finds no sentence that calls firmware the default. Whether this settles D0-001, D0-033 and D0-056 is for the reviewers and the maintainer.

## Generator and freshness gate

- Generator: `python3 scripts/docs_inventory.py --write`, which writes only `docs/DOCUMENTATION_AUDIT.md` (`scripts/docs_inventory.py:990`). `--findings-dir` writes outside the tree. `scripts/docs_inventory.json` is the generator's input: no mode of the generator writes it, so it is unchanged here.
- Gate: `--check`. Self-test: `--selftest`, 50 controls.
- Before the write, on the merged tree: `--check` rc 1, "STALE (403 lines differ); first difference at line 30" (`receipts/regen/check-merged-before-write.log`, `.rc`). After: `--write` rc 0 and `--check` rc 0 (`write.log`, `check-after-write.log`).
- **Planted stale-page mutants on fresh clones of `e8ec8d20`** (`tools/stale_page_mutants.sh`, `receipts/probes/stale-page-mutants.txt`). In every arm the clean head gives `--check` rc 0, the planted tree gives `--check` rc 1, and `--write` then `--check` give rc 0:
  - `append-line`: one line appended to the new `docs/design/MARK_II_STREAM_ENGINES.md`. The diff is its line count and the totals.
  - `d0-001-copy`: the D0-001 statement put back on `REQUIREMENTS.md`. Its copy row returns and the page renders stale (current 176 -> 175, stale 16 -> 17). So the cross-page search still runs on the merged tree.
  - `d0-001-restored`: the statement put back on `README.md`. The D0-001 row is located again, at line 490.

## Findings per area

Generated by `python3 scripts/docs_inventory.py --findings-dir findings` from a clean clone of `e8ec8d20` (`receipts/regen/findings-dir.log`, rc 0). The notes are in `findings/README.md`.

| Area | Rows | Copy rows | Of which "re-verify" | File |
|---|---:|---:|---:|---|
| reference (with integration) | 54 (was 57) | 0 (was 3) | 2 (D0-033, D0-056) | `findings/reference.md` |
| overview and guides | 11 (was 14) | 0 (was 3) | 1 (D0-001) | `findings/overview-and-guides.md` |
| design | 1 (was 6) | 1 (was 6) | 0 | `findings/design.md` |
| testing and CI | 1 | 1 | 0 | `findings/testing-and-ci.md` |
| archive (recorded, not to be rewritten) | 9 | 9 | 0 | `findings/archive.md` |
| **total** | **76** (was 87) | **11** (was 22) | **3** | |

## Gates

All ran on clean clones of `e8ec8d20` and none was piped. The runner and verifier are in `receipts/gates/tools/`, copied from the assigned tools with this lane's paths. The rtl-fast counterparts and `collect.py` come from round 4. One `not_run.json` reason changed: `docs-gates-0/ci_step_55` now points to round 4's own log. `select_rtl_fast.py` on the head picks the same 45 steps as round 4. Neither workflow changed on dev.

| Gate | Result | Receipt |
|---|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 65 steps rc 0, 31 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/docs-yml-table.md`, `docs-yml-verify.rc`, `receipts/gates/docsyml/` |
| Of those: `docs_check.py` (gate_7, and with git stripped in `docs-check-no-git` ci_step_3), `check_doc_style.py` (gate_9), em-dash (gate_8, `[e61a4afa..HEAD]`), bare-metal scope (gate_21), cited paths (gate_43), TOC and anchors (gate_45), inventory `--check` and `--selftest` (gate_46) | rc 0 each | `receipts/gates/docsyml/docs-gates-0__gate_*.log` |
| Every step of `.github/workflows/rtl-fast.yml` that reads `scripts/` or `docs/` | 17 steps rc 0, 28 not run with a stated reason, 0 bad; verifier rc 0 | `receipts/gates/rtl-fast-table.md`, `rtl-fast-verify.rc`, `receipts/gates/rtl-fast/` |
| `python3 scripts/docs_inventory.py --check` | rc 0, "OK (540 lines ...is fresh)" | `receipts/gates/lane/inventory_check.log` |
| `python3 scripts/docs_inventory.py --selftest` | rc 0, 50 controls | `receipts/gates/lane/inventory_selftest.log` |
| `python3 scripts/pp_srcs.py --check` and `--check --selftest` | rc 0 each | `receipts/gates/lane/pp_srcs_check.log`, `pp_srcs.log`; also rtl-fast `verilator-lint__ci_step_8.log` |
| `git diff --check $(git merge-base origin/dev HEAD) HEAD` | rc 0 | `receipts/gates/lane/diffcheck.log` |
| `git merge-base --all origin/dev HEAD` is one commit | rc 0, `e61a4afa` in the clone and in the lane | `receipts/gates/lane/merge_base_all.log`, `merge_base_all_lane.log` |

Every job's clone was clean and at `e8ec8d20` after its steps (`*__tree-after.txt`). The exception is `docs-check-no-git`, whose step strips the git metadata. `docs-gates-2__gate_41.log` was over 200 KB, so it is a `.sha256.txt` record. No step failed and none was retried. To avoid round 4's SDK race, `docs-gates-1`, `docs-gates-2` and the firmware jobs started only after `docs-gates-0` had installed the RV32 SDK.

**Other differences from the hosted run** (as in round 4): the pinned Verilator's directory is substituted for `/opt/verilator/bin`; `changes/scope` runs in the replay form (`ACT=true`, base `origin/dev` at `e61a4afa`); Yosys and sv2v were already on `PATH`, so the install steps were not run; `firmware-boundary` ran with the LiteX interpreter first on `PATH`.

## Resources

All jobs ran in parallel inside this unit. The unit's `memory.peak` read **10.7 GB** at the end, over the 8 GB target and under the 12 GB cap. That figure includes page cache. Samples during the run read 7.6 GB total at the highest, and anonymous memory at 5.3 GB at the next sample. The peak itself was not sampled. Host MemAvailable read 42.7 to 46.1 GB at each sample. At the end, `uptime` read load averages of 51, 67 and 75, shared with other lanes. No Vivado, no sweep, no hardware.

## Open decisions and limits

1. **Hosted CI has not run on this head; it is not pushed.** The local replica (`act_ci.py`) was not run.
2. **D0-001, D0-033 and D0-056** now read "re-verify: quote not found" (above). Removing them is for the decision on "Mark II default".
3. **No statement or citation was re-verified this round.** The new page and dev's other new lines were not checked.
4. Round 4's other open items carry over unchanged: the owner additions of 2026-10-30, the two scope-addition statements, the `also` breadth, and the unextended sampling.

## Receipts

`receipts/INDEX.md` is generated from the files present by `python3 -I tools/receipt_index.py <output dir>`.

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
