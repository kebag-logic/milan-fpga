[R902] POSITIVE - exact head 58f7673b8c57a80230e716bc1774ff9cc2f71ddc

Internal cleared-context delta review R902-3 of issue #983 / PR #986. Head `58f7673b8c57a80230e716bc1774ff9cc2f71ddc`, tree `6dbb2ebaa80cf656a39b93c10c46e98fa6b92d2a`. The delta is one commit on `66b4def34dcbc0d371ce4eb339d3d0226875befa`, the head R902-1 reviewed NEGATIVE (https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7101347692). It touches 4 files: `ctrl_loop.h` (the guard), the new `host/ctrl_loop_host.h`, `test_builder.py` (gate 41) and `ENDSTATION_BUILDER.md`. Source base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`.

I applied all five lenses to the delta, and each is CLEAN at this head:

- R902-1-F1 (BLOCKER) is resolved at its cause.
- R902-1-R1 and R902-1-R2 (RESIDUE) are resolved.
- R902-1-S1 was adopted.
- No new BLOCKER, MAJOR, MINOR or RESIDUE was found. Two SUGGESTIONs are recorded, one new and one retained.

## How I reconstructed the task

- I read AGENTS.md, issue #983 (body: scope and frozen acceptance) and the author's three `[A830] REVIEW READY` comments on #983.
- I read `git diff 854bd723..58f7673b` and `66b4def3..58f7673b`, then the shape-table reader `tb/verilator/ctrl_service_budget/shape_costs.py` and the other text readers of `ctrl_loop.h`.
- I read the public evidence commit `ad3798bc641ff3f9d1f3827c5acf6a30fab0ac4b`, `review-evidence/linuxprof-r1/author-r3`, and verified it:
  - all 237 `MANIFEST.json` entries match their `published_sha256` (0 bad);
  - all 40 author-r3 files are listed;
  - R902-1's own `MANIFEST.sha256` verifies.
  - The evidence commit itself is unsigned. Its integrity rests on the manifest hashes.
- I read prior review findings (R900-1, R900-2, R902-1) only after my own pass over the diff. I did not read the concurrent R900-3 round.

Every probe ran in a disposable tree: `git archive` of base, `66b4def3` ("r2") and head, with the five initialized submodules extracted at their (identical) gitlinks, or a shared clone for the mutants. The review clone was not modified. `receipts/integrity.txt` records exact head bytes, a clean index and worktree, 0 untracked or ignored entries, and the gitlinks.

## Delta checks requested for this round

| Check | Result | Receipt |
|---|---|---|
| THE SHAPES chain byte-identical to base | **Yes.** 39 lines from `#if CTRL_LOOP_SHAPE(1u, 2u, 2u)` to its `#endif`, sha256 `f1bbae92…9d89` at both base and head. `ctrl_loop.h` base..head is +9/−0: the guard comment, the `#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)` / `#include "../host/ctrl_loop_host.h"` / `#else` lines (`ctrl_loop.h:360-367`) and the closing `#endif` (`:407`). | `receipts/integrity.txt` |
| Host shape selected before the chain, only under `CTRL_HOST_PLATFORM` at (1,1,2) | **Yes.** Guard at `ctrl_loop.h:365`. `host/ctrl_loop_host.h:29-33` refuses direct inclusion without the macro, without `CTRL_LOOP_SHAPE`, or at any shape but (1,1,2), and passes at (1,1,2). `CTRL_HOST_PLATFORM` is named only in the 4 files gate 41 allows. | `receipts/host_header_direct.txt`, `receipts/integrity.txt` |
| Why the header sits in `host/` | **Confirmed.** `ctrl_plants.py:600-602` (BASE) builds a C++ probe of every `*.h` in `acmp adp maap mbx port loop app`. In `loop/`, the header's own `#error` would fire in that probe. `host/` is not in that list. `ctrl_arms.py:47` scans every `.h` (host/ included) for compiler extensions, and the header uses none. `check_baremetal_only --check` covers it (0 findings over 1910 files). | `receipts/docs_gates_spot.txt` |
| Gate 41's new reader checks (`_check_shapes_text`, `_shapes_as_read`, `_shapes_reader`, `_check_fpga_rows`) | **Pass at head.** The output equals the author's receipt line for line: 4 FPGA rows read, no host row, both plants refused, 1if and 2if points as stated, `arty_current/1if` reported at the host shape. Gates 32, 41 and 42 and `test_bad_configs_rejected`: rc 0. | `receipts/gates_head.txt` |
| Mutant m1 (66b4def3's `ctrl_loop.h` restored) caught | **Yes.** "gate 41: shape_costs.py does not read THE SHAPES: ctrl_loop.h states "// THE HOST PLATFORM's shape (#983), …" for the shape (2, 9, 9)", rc 1. | `receipts/gate41_mutant_m1.txt` |
| My own mutants | **Each caught, in its own words, rc 1.** mA: guard without its shape test, with the gate's guard text and the header's shape `#error` following it → "the host shape's streams at two interfaces were not refused". mB: host `CTRL_LOOP_TX_MS` 36 → "not the 1x1/1if row's". mC: a host figure dropped → "states 7 figures". mD: the host row restated as a plain `#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)` in the chain → "THE SHAPES list the host shape (1, 1, 2) as an FPGA row". | `receipts/gate41_mutant_m{A,B,C,D}.txt`, `scripts/mutate.py` |
| R902-1's `probe_shape_costs.py` (unmodified copy) | **Same at base and head**, raises at r2. `listed()` gives `[(1,2,2),(1,9,9),(2,2,2),(2,9,9)]` with identical `at(1)` and `at(2)` at base and head, and ValueError at `66b4def3`. | `receipts/probe_shape_costs.txt` |
| `shape_costs --check` / `--selftest`, `load_grade --check`, `flip_grade --check [--point 1x1/1if]` | **Head output byte-identical to base** for all five commands (rc 0, 0, 0, 1, 0). `--selftest` refuses 25 of 25. `flip_grade --check` all points FAILs 8x8/2if at base and head alike, which is the documented base state. r2 raises ValueError in each. Each head output also equals the author's head receipt. | `receipts/budget_*_{base,r2,head}.txt` |
| FPGA `ctrl_loop.o` byte-identical at the 6 compiling points | **Yes, and stronger.** I preprocessed (`-E -P`) all 30 firmware `.c` outside `test/` and `host/` at 12 points: no shape header plus the 5 FPGA shape headers, each with its generated `aecp_entity_gen.h`, at `MBX_N_IF` 1 and 2. That gives 360 base/head pairs, all SAME (token streams and diagnostics). The 6 Arty points stop at THE SHAPES' `#error` in both trees. All 6 compiling `ctrl_loop.o` pairs are identical. The 5 sources that need `nvm_shape_gen.h` stop at that include in both trees, with identical diagnostics. They are still covered: the guard is false wherever `CTRL_HOST_PLATFORM` is undefined, and its `#else` branch is the base chain byte for byte. | `receipts/fw_preproc_all.txt`, `scripts/fw_preproc_all.sh` |
| Board host build 35/35 objects and binary identical (ti-sitara-am65x-bsp `afc35064`) | **Receipt verified by hash, and corroborated.** I did not rebuild the board repository. At the host profile's own shape header with `-DCTRL_HOST_PLATFORM`, r2 and head give the same `ctrl_loop.h` macro set (1483 macros, excluding the new include guard), the same `ctrl_loop.c` token stream and the same `-O2` object. The figures are 950/1010/735/285/85/34/130/35 with `MBX_N_IF 1u`. Without the macro, the shape is refused by THE SHAPES at both. | `receipts/host_shape_r2_vs_head.txt`; author `board_host_build.txt` (hash-verified) |
| The 245 FPGA artifacts' identity | **Receipt verified.** `identity-854bd723.json` and `identity-58f7673b.json` have 245 equal leaves, and `identity_fulltree.txt` shows 240/240. Independently, no builder, generator or config source changed in `66b4def3..58f7673b`: only the 4 files above changed, and the identity artifacts include no firmware object. | author receipts (hash-verified), `receipts/integrity.txt` |
| Other text readers of `ctrl_loop.h` | **No anchor changes meaning.** Every string literal of 4 or more characters in `tb/verilator/ctrl_service_budget/*.py`, `sw/firmware/ctrl/test/*.py`, `sw/builder/*.py` and `scripts/*.py` was counted in base and head `ctrl_loop.h`. Those whose count moved are prose fragments or generic tokens (`#if `, `#else`, `#endif`, `CTRL_LOOP_SHAPE(`). I inspected their users: `shape_costs.listed` (the gate passes), `load_grade.unit_planted:397` and `shape_costs` self-test `:492` (both anchor on a full FPGA `CTRL_LOOP_SHAPE(n, s, k)` head, which the guard's (1,1,2) never matches), `srp_arms.py:173` and `selftest_round.py:47` (regex `^#(?:el)?if CTRL_LOOP_SHAPE\(`, which does not match `#if defined(`), and the remaining test_builder/ctrl_plants hits (other files' text). Moving the host figures out of `ctrl_loop.h` also keeps `rows_tiers.py:882`'s `text.replace('#define CTRL_LOOP_SLICE_US 950u\n', …)` acting on the FPGA row alone, as at base. | `receipts/anchor_scan.txt`, `scripts/anchor_scan.py` |
| R1 / R2 | Resolved; see below. | |

### `run.py --self-test` and its 580 s bound: not blocking

- The bound is a base-state property of a loaded host, not something this PR introduced. R902-1's base run reached the same bound (rc 124, still grading controls), and so did the author's base run.
- At head the self-test grades rather than raises, which is R902-1-F1's required outcome. The author's base and head receipts are byte-identical (modulo the tree tag) over all 1944 lines, with no traceback, and both end rc 124 at 580 s.
- Every input the self-test reads from the tree is shown identical as read:
  - `tb/` is untouched;
  - THE SHAPES read identically through `shape_costs`;
  - the FPGA-visible preprocessed firmware is identical;
  - no text anchor in the harness changes meaning.
- No hosted workflow or bank runs `ctrl_service_budget`: no reference in `.github`, `ci`, `scripts` or any Makefile.
- The self-test's full verdict is therefore established at neither base nor head. I list that as a limit and as a manager duty, not a finding. I did not re-run it, because the host load average was about 127 on 32 CPUs.

## Prior public findings at this head

| Prior ID | Severity; lenses | Disposition at 58f7673b |
|---|---|---|
| R902-1-F1 | BLOCKER; Conformance, RTL, Tests | **RESOLVED at its cause**, with every required outcome met. (1) The five commands reach the base verdicts, with the four FPGA rows read unchanged. `flip_grade --check` grades as at base, and `run.py --self-test` grades rather than raises. (2) The host figures are selectable only under `CTRL_HOST_PLATFORM` at (1,1,2), and no reader takes them as an FPGA shape. (3) Gate 41 now fails on the defect (m1) and on four variants of it (author m2–m4 and m3b, plus my mA–mD). (4) The reader was not changed (`tb/` untouched), so no scope decision was needed. |
| R902-1-R1 | RESIDUE; Docs | **RESOLVED.** Section 6 rows are `H1`–`H9` (`ENDSTATION_BUILDER.md:1233-1241`), and row 5d cites "section 6, row H2" (`:1031`). `grep '^\| 6[a-i] \|'` matches only section 3's row 6a (`:1033`), which row 3's "row 6a's MAC" correctly cites. The gate 32 and gate 41 key maps pass. Gate 41's planted row is now labelled `H0`. |
| R902-1-R2 (retains R900-2-R1, R900-1-R1) | RESIDUE; Docs (PR body) | **RESOLVED.** The live PR body's Status reads "Published head: `58f7673b…`. The evidence below is local source-head evidence; hosted acceptance is tracked separately." The checkout comment reads "# head 58f7673b…", with no "once pushed". The live PR head is `58f7673b`. |
| R902-1-S1 | SUGGESTION; Tests | **ADOPTED.** `_contract_at` and `_shape_figures(n_if)` at `test_builder.py:30643-30678` force-include the contract at 1 and 2 interfaces and assert the printed `MBX_N_IF`. `_check_fpga_rows` (`:30751`) runs every config at both counts. |
| R902-1-S2 | SUGGESTION; Robustness | **RETAINED as a SUGGESTION.** `gptp.clock_accuracy: 'x'` raises ValueError rather than ConfigError. This is base behaviour on FPGA configs too, and the delta does not touch the builder. |
| R900-1-F1, R900-1-F2 | MINOR | Resolved at `66b4def3` (R900-2, R902-1). The delta touches no builder source and no TSpec prose, so the dispositions stand. |

## Findings of this round

### R902-3-S1 SUGGESTION - Tests, Robustness

- **Where:** `tb/verilator/ctrl_service_budget/` (`shape_costs.py --check/--selftest`, `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if`). No hosted workflow or bank runs them.
- **Point:** This PR's gate 41 now holds the specific defect class: the host shape inside, or beside, THE SHAPES as read by `shape_costs.listed`. The harness's own checks still run nowhere automatically, though. A later edit to THE SHAPES that keeps gate 41 green but breaks another harness rule (for example a figure layout `listed()` refuses for another reason) would again be silent in hosted CI.
- **Option:** A separate Issue could add the harness's fast checks (seconds each here) to a hosted job. This is outside #983's scope and does not affect this verdict.

### R902-1-S2 SUGGESTION - Robustness (retained)

As above: open a separate Issue for the `gptp.clock_accuracy` ValueError, beside the disclosed `board: null` / integer TypeError follow-up.

No RESIDUE was found in the delta. I scanned the new source comments (`ctrl_loop.h:360-364`, `host/ctrl_loop_host.h:1-24`, the new test_builder docstrings and comments) for lane labels, round or reviewer IDs and comment IDs, and found none. They cite only #983 and file names.

## Per-lens results

```text
[R902] PASS Conformance — sw/firmware/ctrl/loop/ctrl_loop.h:360-407 (chain sha256 f1bbae92 = base, 39 lines); receipts/budget_*_{base,head}.txt; author identity-{854bd723,58f7673b}.json — issue #983 scope "the FPGA scheduler-shape guard and its rows are untouched" (chain byte-identical, read identically by shape_costs.listed), "FPGA profile validation is unchanged" (five budget checks byte-identical to base), "every FPGA generated artifact stays byte-identical" (245/245 and 240/240 receipts; no builder or generator source in the delta), host entry for the Linux build only (guard at :365, macro named in 4 allowed files); acceptance 1 (gate 41 line 1 at head: three generators agree with the 5784-byte image)
[R902] PASS RTL — git diff --raw 66b4def3..58f7673b (no hdl/ or RTL file); receipts/fw_preproc_all.txt; receipts/host_shape_r2_vs_head.txt; receipts/host_header_direct.txt — no RTL in the delta. Firmware build architecture: 360 FPGA preprocessed source pairs and 6 ctrl_loop.o pairs identical base vs head at MBX_N_IF 1 and 2; the host build's macro set, tokens and object identical r2 vs head; the header's guards refuse every use but a CTRL_HOST_PLATFORM build at (1,1,2); placement in host/ keeps it out of ctrl_plants BASE's loop/*.h probe (ctrl_plants.py:600-602)
[R902] PASS Robustness — host/ctrl_loop_host.h:29-33; test_builder.py:30751-30823; receipts/host_header_direct.txt; receipts/gates_head.txt — direct inclusion without the macro, without CTRL_LOOP_SHAPE, or at (1,2,2) is refused; the host shape is refused without the macro and at two interfaces with it; arty_current/1if (an FPGA config at (1,1,2)) takes the host figures only under the macro, which no build input defines, and gate 41 reports that point separately; R902-1-S2 retained as a SUGGESTION (base behaviour)
[R902] PASS Tests — test_builder.py:30643-30823, 30923; receipts/gates_head.txt; receipts/gate41_mutant_{m1,mA,mB,mC,mD}.txt; receipts/probe_shape_costs.txt; receipts/anchor_scan.txt — gate 41 passes at head with output equal to the author's; it fails on R902-1-F1's own defect (m1) and on four independent mutants of mine, each in its own words; it reads ctrl_loop.h through the tree's reader, not a copy of its rules; R902-1-S1 adopted (n_if 1 and 2, MBX_N_IF asserted); no tb/ or firmware-test text anchor changes meaning
[R902] PASS Docs — docs/ENDSTATION_BUILDER.md:84, 1031, 1233-1241, 1272-1286; receipts/docs_gates_spot.txt; live PR #986 body — section 6's firmware-shape paragraph matches the code (host header, guard before the chain, refused without the macro or at 2 interfaces, arty_current named, gate 41's cases); H1-H9 labels and row 5d's H2 are consistent; TOC line updated; docs_check, check_baremetal_only --check, check_py_idiom and check_doc_paths rc 0 at head; PR body Status names the published head; no comment-rule residue in the delta
```

## Reviewer-owned completion ledger (lenses this round covered)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #983 scope and acceptance; `ctrl_loop.h:360-407`; budget receipts base/r2/head; identity receipts | R902-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| RTL | CLEAN | delta raw diff (no RTL); `fw_preproc_all.txt` (12 points, 360 pairs, 6 objects); `host_shape_r2_vs_head.txt`; `ctrl_loop_host.h:29-33`; `ctrl_plants.py:600-602` | R902-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Robustness | CLEAN (S1, S2 are SUGGESTIONs) | `host_header_direct.txt`; gate 41 refusal paths at `test_builder.py:30751-30823`; arty_current/1if point | R902-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Tests | CLEAN (S1 is a SUGGESTION) | `gates_head.txt`; mutants m1, mA–mD; `probe_shape_costs.txt`; `anchor_scan.txt`; author m1–m4 and m3b receipts | R902-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Docs | CLEAN | `ENDSTATION_BUILDER.md:84,1031,1233-1241,1272-1286`; `docs_gates_spot.txt`; live PR body; source comments in the delta | R902-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |

The delta's own artifacts were covered at the exact head. Code the delta does not touch keeps its prior lens verdicts:

- `endstation_builder.py` and the host example config (R900-2 and R902-1 at `66b4def3`; nothing in their scope has changed since).
- R902-1's Robustness and Docs coverage of the builder path.

## Limits

- I did not run, and claim nothing from:
  - the full builder suite, gate 1b, the firmware shards and mutation campaigns;
  - any RV32 cross build (the FPGA object comparison used the host compiler at `-O2`);
  - the board repository's own build, for which I rely on the author's hash-verified receipt, corroborated by the r2-vs-head macro, token and object identity of `ctrl_loop.c`;
  - Yosys, Verilator banks, act or Docker.
- `run.py --self-test` was not re-run. Its full verdict is established at neither base nor head, because both reach the 580 s bound on a loaded host.
- I did not rebuild the 245 identity artifacts. I hash-verified the receipts and confirmed that no generator or builder source changed in the delta.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank exists at this head, and I claim or infer none.
- The hosted runs at `58f7673b` were in flight when I looked (`receipts/hosted_checks_58f7673b.tsv`: 5 success, 1 skipped (physical gPTP nightly/manual), 42 queued or in progress). I recorded them as observed. They are not acceptance evidence from this round.

## Pending manager duties

- Validate the current-dev merge candidate (source base `854bd723`, live dev `e275d795`) with the builder and native banks, and link the receipts on the PR.
- Because the service-budget harness is in no bank, run `shape_costs.py --check/--selftest`, `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if` and `run.py --self-test` on the candidate. Give the self-test a bound long enough to finish on a quiet host.
- Own hosted and act acceptance at the exact PR head. Most required contexts were still queued.
- Re-pin the board repository (ti-sitara-am65x-bsp, which pins `66b4def3`) after merge.
- Merge only with explicit maintainer authorization.

R902-3 FINISHED
