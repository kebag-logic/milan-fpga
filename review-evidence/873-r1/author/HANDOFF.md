# HANDOFF — [A763] issue #873 (act replay: 8 jobs on narrower CPU ranges)

Status: REVIEW READY at `88e1041c`. Items 1, 2, 3 and 5 met; item 4 is the manager's (`CALIBRATION.md`). Every gate rc 0 on a clean clone.

- Remote: `https://github.com/kebag-logic/milan-fpga.git` (confirmed with `git remote get-url origin`).
- Lane: branch `873-act-eight-jobs`, from dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`. Confirmed: merge base == `45c0b56c` == the live remote `dev` tip (`git ls-remote`, 10:10).
- Head: `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` (3 commits, one-line subjects, no body, no trailers):
  - `cf4898e3` Make the act replay's job count, per-job CPU width and memory cap one validated geometry that accepts 8 jobs on 6- or 8-CPU ranges and refuses memory or CPU over-subscription (#873)
  - `3a22125a` Document the act replay's job geometry, its measured basis from PR #835's replay and the unchanged 4 x 16 default (#873)
  - `88e1041c` Stub the nested self-test in the geometry usage-error arms so a missing usage error fails them instead of recursing (#873)
- Assignment: #873 Required items 1, 2, 3 and 5. Item 4 (the calibration replay) is the manager's: see `CALIBRATION.md`.
- TAKEN was posted on #873 at 2026-11-10T06:40:23Z, by the session cut at 07:49. It was not reposted.
- REVIEW READY posted on #873 at 2026-11-10T10:09:07Z (issuecomment-6764609397), naming head `88e1041c`.
- Nothing pushed. No PR, no act replay, no `--dry-run`, no Docker, no slot, no sudo, no workflow change.

## Resume note

The 07:49 power-off left the geometry refactor uncommitted in the worktree. I kept it, read it, and
checked it against its scratch selftest log. That log passed with the base's 621 isolated arms, the
same labels, and only embedded line numbers moved. This session added the new arms, the docs, one
robustness fix to the new arms (third commit), the mutants and the gates.

## Changes (file:line at `88e1041c`, reason)

`scripts/act_ci.py`:

| Line | Change | Reason |
|---|---|---|
| 107-120 | `JOB_CPU_WIDTHS = {16: (16, 12), 8: (8,), 6: (6,)}`, `MAX_CONCURRENT_JOBS = 8`, `REPLAY_CPU_LIMIT = 64` replace `CONTAINER_CPU_LIMIT = 16`, `FALLBACK_CPU_LIMIT = 12` | Item 1: the width is a parameter. 16 keeps its 12-CPU fallback (#737's one named setting). 8 and 6 have none. 64 is what one replay booked before (4 x 16). |
| 123-126 | `MAX_CONTAINER_MEMORY_GIB = 8` replaces `CONTAINER_MEMORY = "8g"`, `CONCURRENT_JOB_LIMIT = 4` and `SLOT_JOB_RANGES` | Item 1: the job count and memory cap are parameters. 8 GiB stays the default and the maximum. |
| 165-180 | `SLOT_MEMORY_GIB = 36`, `SLOT_SERVICE_MEMORY_GIB = 4`, `SLOT_MEMORY_MAX = f"{SLOT_MEMORY_GIB}G"` (still `"36G"`) | Item 2: the slot cap and the 4 GiB overhead the old comment named become numbers the bound can use. |
| 2145 | `replay_container_concurrency` caps at the geometry's jobs | Item 1: admission follows `--jobs`. |
| 4592, 4622 | `SlotMemory` docstring and refusal text name the geometry's cap | The OOM refusal names the cap that actually ran. |
| 4742-4815 | `JobGeometry` (frozen dataclass): type and range checks; memory bound at 4775; CPU bound at 4782; `range_widths`, `fallback_cpus`, `container_memory`; `DEFAULT_JOB_GEOMETRY = JobGeometry()` (4, 16, 8); `JOB_GEOMETRY` ContextVar; `job_geometry_arguments` | Items 1 and 2: one validated geometry. An over-subscribed one cannot exist. A Refusal, never a smaller replay. The default is today's geometry, so an unchanged command line runs and is refused as before. |
| 4838-4848 | `parse_cpu_ranges` accepts only the geometry's widths | Item 1: 6/8-CPU ranges only when chosen. The aligned, distinct and within-host refusals are unchanged. |
| 4861-4866 | `job_cpu_ranges` bounds concurrency by, and selects, the geometry's jobs | Item 1. |
| 4903-4952 | `build_act_command` takes `--concurrent-jobs`, `MILAN_CI_FALLBACK_CPUS` and `--memory`/`--memory-swap` from the geometry | Item 1. At the default the command is byte-identical to before (existing arms). |
| 17357-17370 | `--jobs`, `--job-cpus`, `--job-memory` | Item 1: the operator's choice. |
| 17472-17474 | `--selftest` refuses the three options as PR-run arguments | Same rule as `--cpu-ranges`. |
| 17480 | `main` sets the geometry before it parses `--cpu-ranges` | Ranges are read against the chosen width; a bad geometry refuses before any collaborator. |

Existing arms whose expected value moved from a removed constant to the geometry (same labels, same
values under the default, all pass): `selftest_validation_transcript` 6778-6783,
`selftest_runner_label_replay` 6905-6914, `selftest_act_command` 7634-7682,
`selftest_container_cpu_bound` 7724, `selftest_container_memory_bound` 7732-7757,
`selftest_job_concurrency` 7810 (`JobGeometry(limit)` in place of patching `CONCURRENT_JOB_LIMIT`),
`selftest_job_cpu_ranges` 7857 ("fallback has one named setting" now reads `JOB_CPU_WIDTHS[16]` and
the default's fallback), `selftest_slot_act_command` 14506. Because those values now follow the
geometry, the new default arm pins the default. Mutant M13 shows that only that arm, and a CLI arm,
catch a changed default memory cap.

`docs/testing/CI_WORKFLOWS.md` (item 5):

| Line | Change | Reason |
|---|---|---|
| 2272-2283 | Range width is `--job-cpus`. 16 keeps the 12 fallback; 8 and 6 have none. The refusals are kept at every width. Without `--job-cpus`, 6/8 ranges stay refused as #737 set them. | Replaces "`FALLBACK_CPU_LIMIT=12`" and "Eight-CPU ranges remain refused under the current owner ruling". States the conflict openly (below). |
| 2339-2340 | Admission bound is `--jobs`, 4 by default, at most 8 | Replaces `CONCURRENT_JOB_LIMIT=4`. |
| 2355-2406 | Job geometry: its two bounds, a table of accepted and refused shapes, an 8 x 6 example, the 16-CPU straddle note, #835's measured basis, the unchanged default, the 4 GiB caveat, and what the calibration decides | Item 5: measured basis and chosen default. Replaces "The current runner deliberately keeps four as its maximum". |
| 2831-2833 | `floor((36 - 4) / 8) = 4` stays true at the default, generalised to the cap | Keeps the resource-bounds record true. |

No change to `ci/act/*.go`. The pinned dispatcher already accepts width 16 or
`MILAN_CI_FALLBACK_CPUS` (1-16, `ci/act/cpu_ranges.go:20,37`) and as many jobs as there are ranges
(`:64`).

## New selftest arms (34): planted defect and failing words

Count: base `45c0b56c` 623 `ok` (non-isolated) / 621 (isolated); head 657 / 655. None removed
(normalised label diff: 0 base-only lines), 34 added. Mutants are one text replacement each in a copy
of the committed `act_ci.py` at `88e1041c`, run as `python3 -I <copy> --selftest --worktree <clean
clone>`. All 22 fail; none survives. Record: `receipts/mutants.json` (sha256 `8cca76a5...`) and
`receipts/mutants.py`.

| New arm (label, abridged) | Planted defect | Failing words |
|---|---|---|
| the default geometry is the runner's before #873, 4 jobs of 16 CPUs (12 fallback) at 8g ... | M13: default `memory_gib` 8 -> 4 | `FAIL the default geometry is the runner's before #873, ...` |
| the default geometry still refuses 6- and 8-CPU ranges by their width | M9: `parse_cpu_ranges` widths fixed to (16, 12, 8, 6) | `FAIL the default geometry still refuses 6- and 8-CPU ranges by their width` |
| 8 jobs on 6-CPU ranges: the 8 booked ranges parse, admit 8 concurrent jobs and are all selected (and the 8-CPU twin) | M8: `job_cpu_ranges` returns `ranges[:4]` | `FAIL 8 jobs on 6-CPU ranges: the 8 booked ranges parse, ...` and the 8-CPU one |
| 8 jobs on 6-CPU ranges: act starts 8 jobs at once, stated once, the dispatcher gets every range and fallback width 6, and each container is held to 4g ... (and twin) | M5: `--concurrent-jobs` from `min(4, ...)`; M6: fallback fixed at 12; M7: memory fixed at 8g | `FAIL 8 jobs on 6-CPU ranges: act starts 8 jobs at once, ...` and the 8-CPU one, for each |
| 8 jobs on 6-CPU ranges: a ninth concurrent job is refused (and twin) | M14: `job_cpu_ranges` drops the upper bound | `FAIL 8 jobs on 6-CPU ranges: a ninth concurrent job is refused` and twin |
| 8 jobs on 6-CPU ranges: seven booked ranges for 8 concurrent jobs are refused (and twin) | M15: range-count check removed | both, plus existing `FAIL too few booked ranges for concurrent jobs` |
| 8 jobs on 6-CPU ranges keep the --cpu-ranges refusals: an unaligned, a repeated and a beyond-the-host range ... (and twin) | M16: alignment check removed | both, plus existing `FAIL invalid or missing CPU ranges '1-16'` |
| 8 jobs on 6-CPU ranges refuse any other width: 0-15, 0-11, 0-7 (and 8-CPU: 0-15, 0-11, 0-5) | M9 | both `FAIL 8 jobs on ... refuse any other width` |
| memory over-subscription is refused: 8 jobs of 8 GiB ... 68 GiB / 8 of 5, 44 / 6 of 6, 40 / 5 of 7, 39 (4 arms) | M1: memory check removed; M2: service share dropped (6 x 6 and 5 x 7 then fit) | all four `FAIL memory over-subscription is refused: ...`, for each |
| CPU over-subscription is refused: 8 x 16 at 4 GiB / 5 x 16 at 6 / 8 x 16 at 1 (3 arms) | M3: CPU check removed; M4: `REPLAY_CPU_LIMIT` 128 | all three `FAIL CPU over-subscription is refused: ...`, for each |
| a geometry exactly at both bounds is accepted: 8 x 6 and 8 x 8 at 4 GiB, and 4 x 16 at 8 GiB, ... | M17: memory minimum 1 -> 2 | `FAIL a geometry exactly at both bounds is accepted: ...` (and the 8 x 16 at 1 GiB CPU arm, now refused for memory first). M18 (`>` -> `>=` at the memory cap) refuses the default itself at import, `Refusal: memory over-subscribed: 4 jobs of 8 GiB ... need 36 GiB`, so no run passes. |
| a job count, CPU width or memory cap out of range, or not an integer, is refused by name: (10 shapes) | M11: `MAX_CONCURRENT_JOBS` 16 | `FAIL a job count, CPU width or memory cap out of range, ...` |
| an 8-job geometry admits 8 legs of a 9-wide nested matrix, and all selected workflows share that 8-job limit in every order | M22: `replay_container_concurrency` caps at 4 | `FAIL an 8-job geometry admits 8 legs ...` (with 4 existing limit arms) |
| under an 8-job geometry every shipping workflow derives 1 to 8 concurrent containers, and rtl-full more than the default 4 | M22 | `FAIL under an 8-job geometry every shipping workflow ...` |
| --selftest with --jobs / --job-cpus / --job-memory is a usage error (3 arms) | M19, M20, M21: each option dropped from main's `--selftest` guard | `FAIL --selftest with --jobs is a usage error` (and each twin). Before `88e1041c` this defect recursed into the self-test; the stub makes it fail. |
| 8 jobs at the default 8 GiB are refused for memory before any collaborator | M1 (also M10, M13) | `FAIL 8 jobs at the default 8 GiB are refused for memory before any collaborator` |
| 8 jobs at the default 16 CPUs are refused for CPU before any collaborator | M3, M4 | `FAIL 8 jobs at the default 16 CPUs are refused for CPU before any collaborator` |
| a ninth job is refused before any collaborator | M11 (also M10) | `FAIL a ninth job is refused before any collaborator` |
| --cpu-ranges is read against the chosen width: 16-CPU ranges under --job-cpus 6 are refused | M9; M10 (`main` parses ranges before the geometry) | `FAIL --cpu-ranges is read against the chosen width: ...` |
| --jobs 8 --job-cpus 6 --job-memory 4 on 8 ranges of 6 reaches its first collaborator with that geometry, which does not outlive the run (and 8-CPU twin) | M10 | both `FAIL --jobs 8 --job-cpus ... reaches its first collaborator ...` |

Other mutants: M12 (default width 16 -> 8) fails five existing arms, then the self-test stops on
`Refusal: CPU range 0-15 has unsupported width 16; need 8`.

## Gate table (clean clone of committed head `88e1041c`)

Each gate ran on a fresh clean clone of `88e1041c` (tree clean before and after), its log and rc
written by the gate's own run, never piped. Python: a scratch venv with the recent gate pins
(PyYAML 6.0.3, behave 1.3.3, cmarkgfm, pyslang, wavedrom 2.0.3.post3). HOME was a scratch
directory. The pinned RV32 SDK was freshly installed into it once by the head's own
`scripts/ci_rv32_sdk.py`: `SDK fresh installation: verified`, archive sha256 `d42680e9...`. Each
job's SDK step then took its verified cache-hit path, so three jobs could not race one extract.

| Gate | Command | rc | Result |
|---|---|---:|---|
| act_ci self-test | `python3 scripts/act_ci.py --selftest` | 0 | `selftest: PASS`, 657 ok, 0 FAIL |
| act_ci flat isolated self-test (docs.yml gate_42's second call) | `install -m 0555 scripts/act_ci.py $d/act_ci.py; python3 -I $d/act_ci.py --selftest --worktree <clone>` | 0 | `selftest: PASS`, 655 ok |
| small-host control | `python3 -I scripts/act_ci_small_host_selftest.py` | 0 | `small-host runner control: PASS` |
| docs inventory | `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK (533 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` |
| behave | `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed |
| diff check | `git diff --check 45c0b56c 88e1041c` | 0 | no output |
| mutants | `mutants.py` (22 planted defects) | 0 | survivors: none |
| base reference (for the arm count) | `python3 scripts/act_ci.py --selftest` on a clean clone of `45c0b56c` | 0 (printed) | `selftest: PASS`, 623 ok; `receipts/gates/base_act_ci_selftest.log` |
| docs.yml, every `run:` step | `run_docs_yml.py <head> <job> <root>` per job, then `verify_docs_yml.py <head> <root>` | 0 | 66 steps ran, 31 not run with a reason, 0 bad (`verify_docs_yml.py` rc 0); every job's tree clean after |

The verifier's own output (`receipts/docsyml/docs-yml-table.md`; logs beside it, one log and one rc per step, `gate_8` run as a `pull_request` against live `dev`; the one log over 200 KB, `docs-gates-2__gate_41.log`, is in `receipts/docsyml/LARGE-LOGS.txt` with its sha256, size and tail):

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
| docs-gates-0 | gate_51 | Register reference freshness gate | 0 | `docs-gates-0__gate_51.log` |
| docs-gates-0 | ci_step_54 | Fetch inventory dependencies | 0 | `docs-gates-0__ci_step_54.log` |
| docs-gates-0 | gate_52 | CI scheduling and evidence controls | 0 | `docs-gates-0__gate_52.log` |
| docs-gates-0 | ci_step_56 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
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

66 steps ran, 31 not run with a reason, 0 bad

Runner and verifier: the copies in `829-a725c/receipts/gates/tools/` changed only in paths (lane,
venv, HOME); the diff is in `receipts/tools-diff.txt`. Their not-run list is that round's, with one
correction for this head's step ids. `docs-gates-0/ci_step_54` is now "Fetch inventory dependencies"
and runs. The hosted receipts-record step it named moved to `docs-gates-0/ci_step_56`, which is not
run, for the same reason.

## Open risks / questions

1. **Eight jobs fit only at 4 GiB each** (36G slot cap, 4 GiB service share). Measured peaks above
   that: capture 5.632 GiB, Yosys source builds 5.26 GiB, census 5.34-5.46 GiB (memory-derived; 2
   workers at 4 GiB), and #835's container maximum of 7.8 GiB. A peak includes reclaimable page
   cache, so this is a risk, not a prediction. But an OOM refuses the replay, so the 8 x 6
   calibration may end refused for memory. Raising 36G is a host decision outside #873.
2. **Owner ruling on eight-CPU ranges.** The docs said "Eight-CPU ranges remain refused under the
   current owner ruling" (#737: fallback stays 12, "one named setting, so it can change to 8 if the
   owner decides that"). #873, filed by the manager, asks to accept 6- and 8-CPU ranges. I kept them
   refused under the default geometry and accepted them only through an explicit `--job-cpus`. The
   docs now say so. If the owner's ruling should also bind the explicit option, the manager decides.
3. The calibration needs this PR's runner, so it runs from an independently audited install (the
   documented bootstrap), not from the trusted `dev` copy.
4. `ci/image/tool-inventory.json` pins `scripts/act_ci.py` at `b8a786ce...`. The base already hashes
   `3f91c996...`: stale since 2026-10-16, and checked only by the CI image build, not by docs.yml.
   Not touched.
5. A 6-CPU range aligned to 6 can straddle a 16-CPU die boundary (`12-17`). Booking is the manager's.
   `CALIBRATION.md` gives a non-straddling set.
6. The new code has had no live run in this lane (no replay, dry run or Docker). Its effect on act
   is proved offline on the generated act command, as the existing arms prove the default.
