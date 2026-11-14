# HANDOFF round 3 — lane 897 (A776): GET_AS_PATH composed with #902 (894-tiers)

Status: **DONE** (2026-11-14 11:17 CET): the full pass at `f098f893` is green, the 1x1/1if flip check composed with #902 passes, every cap and the load hold, and no STOP condition was met. `PR-BODY.md` is ready for the manager; REVIEW READY is posted on #897: issuecomment-6875785531 (`REVIEW-READY-COMMENT.md`).
Round 2 head: `3bebf03a1d25bcbde9c0ec48dfd711af7280131e` (REVIEW READY issuecomment-6863354920; R833-2 POSITIVE, PR #898 issuecomment-6864287713).
Composed with: `origin/894-tiers` at `5b264bf26416108add32d7fe5abca5252ffde2cb` (#902, not merged; `dev-soft-core` still `cec88385`). R838-4 posted NEGATIVE at `5b264bf2` (two MINOR docs findings), so `894-tiers` may move: re-fetched before the full pass (section 3.2).
Sync merges: `e45981f8eecf8cbbbd1cef1f0ff528c8b3241f52` (894-tiers at `5b264bf2`) and, after 894-tiers moved to `7398ec0a` at 09:30 (#902 round 10), `a3a509d79dd694845431d231466b51d63ae53033`; `417f44af` (the ratchet), `25ea917f` (the docs), `f098f893` (the module limit). **Final head: `f098f893d57e0fa3ec95a7e459313c5cfe4f4224`.** Nothing pushed.
Worktree: `$LANES/897-aspath`, branch `897-split-as-path`. PR #898 targets `dev-soft-core`.

Bound rulings read: #894 issuecomment-6867393730 item (d) (#898 must pass the 1x1/1if flip check composed with #902), issuecomment-6867990126 (MRPDU 49 ms, paced R4L 238 ms, harness join gate 181.0-239.0 ms), issuecomment-6870437042 (the map table as a direct index).

## 1. Sync (item 1)

- `git fetch origin`: `origin/894-tiers` = `5b264bf2`, `origin/dev-soft-core` = `cec88385` (the merge base of both branches). Submodule pins equal on all three (protocol-processor `a9e84b66`, gptp-processor `135afd04`, lwSRP `08ee86e8`, tsn-c-stack `715589c1`, verilog-axis `48ff7a7e`); #902 changes no gitlink, no `hdl/` file and no workflow.
- `git merge --no-ff --no-commit 5b264bf2`, then one merge commit `e45981f8` ("Merge 894-tiers 5b264bf2 (#902, not merged) into the split's GET_AS_PATH lane, each conflict kept from both sides"). 13 files changed on both sides: 4 conflicted, 9 merged without a conflict.

| File | How | Resolution |
|---|---|---|
| `sw/firmware/ctrl/plat/ctrl_plat.c` (`compose`) | conflict | #902's `#if AECP_MBX_OWED_SLOTS != 0u` block (owed slots, slot count, queue ops) kept, then this branch's `aecp_platform` with no `.path` (the stub this branch removed stays removed) |
| `sw/firmware/gtest/coverage.ratchet` (`ctrl_plat.c` row) | conflict | both sides 100 % (129/129 here, 133/133 there); the composed count is the measurement's, recorded from `fw_coverage.py --write` (section 4) |
| `sw/firmware/ctrl/plat/README.md:113` | conflict | both sides moved 59.5 to 60.0; this branch's line, which adds "refused at 60.5", kept (true at the composed head: 130,816 B in 131,072) |
| `docs/design/SPLIT_CONTROL_MEMORY.md` section 6 (the platform's override sentence) | conflict | both sides moved 59.5 to 60.0; this branch's line, which adds "half a tile more is refused under its override too", kept (true at the composed head) |
| `docs/design/MAILBOX_SPLIT.md`, `sw/firmware/ctrl/aecp/README.md`, `sw/firmware/ctrl/test/{aecp_mutants.py,ctrl_aecp_image.c,test_aecp.cpp}`, `tb/verilator/ctrl_service_budget/{README.md,build.py,run.py}` | merged, no conflict | checked below |
| `tb/verilator/ctrl_split_boot/README.md` | identical change on both sides | merged equal to both |

Check (`scripts/r3/merge_sides.py`, the `-U0` hunks' +/- lines as sorted multisets): for each of this branch's 17 files, the merge's diff from `5b264bf2` carries exactly this branch's diff from `cec88385`; for each of #902's 85 files, the merge's diff from `3bebf03a` carries exactly #902's diff from `cec88385`. The only lines not carried verbatim are the four rows above that both sides edited. No other file differs. No design decision was needed.

### 1.1 The second sync merge (894-tiers moved to `7398ec0a`)

At 09:30 `origin/894-tiers` moved from `5b264bf2` to `7398ec0aeea468d92ff642a03a06e291a0cd58d1`, #902's round 10 (#894 issuecomment-6873298790: `55b8e621` the map table's assertion and its campaign control, `947bd389` section 13's current rows from the flip check, `7398ec0a` a comment); `dev-soft-core` stayed `cec88385`, #902 not merged. So it was merged again before the full pass, as the assignment requires: one merge commit `a3a509d7` ("Merge 894-tiers 7398ec0a (#902 round 10, not merged) into the split's GET_AS_PATH lane, without a conflict"), parents `25ea917f` and `7398ec0a`. Six files changed on #902's side (`SPLIT_CONTROL_MEMORY.md`, the AECP README, `aecp_maps.c`, `aecp_arms.py`, `aecp_map_mutants.py`, `aecp_mutants.py`); three of them this branch changes too, and all merged without a conflict. `merge_sides.py 5b264bf2 25ea917f 7398ec0a`: every file of both sides carried exactly, 0 differ (`receipts/sync/merge_sides-second.txt`). The merge's staged tree equals the rehearsal's (section 3.1), whose eight images were byte-identical to `e45981f8`'s, so the harness measurements of section 2 stand for the final tree.

**The composition's own red, and its fix (`f098f893`).** At `a3a509d7` `check_py_idiom.py` refused "long module 11 > ratchet 10": `sw/firmware/ctrl/test/aecp_mutants.py` is 963 lines at `5b264bf2`, this branch's nine plants make it 999, #902's round 10 976, and the composition 1,012, past `LONG_MODULE_LINES` 1,000 (`receipts/probes/py_idiom_at_a3a509d7.txt`). `f098f893` moves the nine GET_AS_PATH face plants, their two anchors and the sink's into `sw/firmware/ctrl/test/aecp_face_mutants.py` as `ROWS`, the pattern of #902's `aecp_map_mutants.py` and `aecp_owed_mutants.py`, appended to `DEFECTS` with `defect(*row)`; `aecp_mutants.py` is 977 lines and the gate passes (`py_idiom_at_f098f893.txt`). The campaign's 283 defects are the same in every field (name, file, anchor, replacement, checks; compared against `a3a509d7`'s module), the nine at the end of the tuple instead of beside the other face plants. The AECP README's verification sentence names the new module.

## 2. Composed acceptance (item 2)

### 2.1 flip_grade.py --check --point 1x1/1if

At `e45981f8` (clean clone): **RESULT: PASS**, rc 0, every row by every source, figures identical to #902's at `5b264bf2`: R4 12.85/20, R5 72.91/90, R6 68.80/90, first 14.51/20, last 126.46/130, R4L 188.39/238, ACMP 28.44/30, ADP 26.83/30, MAAP 26.95/30, tx 29.86/49, txL 48.09/49. `load_grade.py --check` rc 0: 0.513 at the pin, 0.509 with tsn-c-stack#32 (ceiling 0.70). (Logs: `r3/early/`.)

### 2.2 GET_AS_PATH's cost in the rows

At `5b264bf2` the fixture's and the platform's `path` port was a stub answering false at once. Here it is the face's: GSI kind 2, the count and then each entry, each a bounded window read (`mbx_win_read`, `MBX_WIN_GSI_WAIT_CYCLES` 64). The shipped datapath serves at most 8 entries (`KL_gptp_engine.sv:780-785` clamps the pathTrace count to 8; `milan_datapath.sv` `asp_*`, entries 0..7), so a read is at most 9 words. It enters three of the rows' terms:

| Term the rows charge | Stated (1x1/1if) | GET_AS_PATH at the composed head | Source |
|---|---:|---|---|
| AS_PATH_CHANGED's take and sinks (`rows_tiers.DATAPATH_US`) | 35 us | 30.02 us measured (31.57 at `5b264bf2`); AVB_INFO_CHANGED 30.64 (30.55), AMAP_LIVE_WRITE 23.34 (25.51) | `datapath-events`, `eventcost.py` on `hA1`/`bA1` |
| its notice in THE RETRY's rounds (`AECP_ROUND_COLD_US` + n x `AECP_NOTICE_US` + k x `AECP_ATTEMPT_US`) | 85 + n x 255 + k x 34 us | unanswered: one GSI word an attempt, 378-796 CPU cycles (scratch span); answered with 8 entries (scratch arm: 9 GSI reads at the contract's whole bound, the count up to 877 cycles, the 8 entries 3,032): the round that built it 46,397 cycles against its stated 59,500; no round, notice or pass over its bound in either arm | `round_grade` in `hA1`, `hN1`; scratch `sA1`, `pN1` |
| a GET_AS_PATH command's record (`record.aecp`) | 235 us | no group sends one; bounded by GET_AVB_INFO's record in arm A (the same handler, `aecp_commands.c:460-500`, one unanswered word) 11,655 cycles + 8 words at 877 + 18 data-word reads at the most a mailbox read took (60) + the 64 B of entries: about 19,950 cycles, 200 us | `aecp` group frame spans, `SUMMARY mbx_read=.../7/60` |

So no stated cost moves, the rows and the load are #902's, and the flip check passes on them.

Data placement (#909): every writable symbol (`.data`, `.bss`, `.stack`) of every image, the fixture's and the platform's at the four points and the harness's formal arm at 1x1/1if, has the same address and size at `e45981f8` as at `5b264bf2` (`scripts/r3/sram_layout.py`, `r3/logs/sram-layout.txt`): GET_AS_PATH adds `rom` only. (The `answering-every-port` test arm swaps two of its own statics, `answering` and `image_face`.)

### 2.3 ROM ledger at every point, delta against 5b264bf2

`plat_ledger.py --self-test` (7 of 7 controls; `plat_ledger: PASS`) and `fixtures3.sh` at both heads, each on its own clean clone:

| Image, point | `5b264bf2` rom B | `e45981f8` rom B | Delta | sram B | RAMB36 base -> head | Cap | Verdict |
|---|---:|---:|---:|---|---|---:|---|
| fixture 1x1/1if | 110,576 | 110,904 | +328 | 55,152, unchanged | 40.5 -> 41.0 | 56 | holds |
| fixture 1x1/2if | 111,872 | 112,192 | +320 | 57,312, unchanged | 41.5 -> 41.5 | 56 | holds |
| fixture 8x8/1if | 124,104 | 124,424 | +320 | 96,240, unchanged | 54.0 -> 54.0 | 56 | holds |
| fixture 8x8/2if | 125,368 | 125,688 | +320 | 113,168, unchanged | 59.0 -> 59.0 | 59.0 (#902's entry) | holds, 1,288 B before 126,976 |
| platform 1x1/1if | 115,640 | 115,952 | +312 | 56,224, unchanged | 42.5 -> 42.5 | 56 | holds |
| platform 1x1/2if | 116,952 | 117,264 | +312 | 58,336, unchanged | 43.5 -> 43.5 | 56 | holds |
| platform 8x8/1if | 129,208 | 129,520 | +312 | 97,264, unchanged | 56.0 -> 56.0 | 56 | holds, 1,552 B before 131,072 |
| platform 8x8/2if | 130,504 | 130,816 | +312 | 114,160, unchanged | 60.0 -> 60.0 | 60.5 (entry 60.0) | holds, 256 B before 131,072 |
| harness arm A 1x1/1if | 110,576 | 110,904 | +328 | 55,152 | 40.5 -> 41.0 | 56 | holds |
| harness arm A 8x8/2if | 125,368 (`bA8`) | 125,688 (`hA8`) | +320 | 113,168 | 59.0 -> 59.0 | 59.0 | holds, 1,288 B under 126,976 |
| harness `answering-ports` 8x8/2if | 125,528 (`bB8`) | 125,872 (`hB8`) | +344 | 113,168 | 59.0 -> 59.0 | 59.0 | holds, 1,104 B under 126,976 |
| harness `answering-every-port` 8x8/2if | 125,676 (`bN8`) | 126,012 (`hN8`) | +336 | 113,232 | 59.0 -> 59.0 | 59.0 | holds, 964 B under 126,976 |
| harness `answering-ports` 1x1/1if | 110,744 (`bB1`) | 111,088 (`hB1`) | +344 | 55,152 | 41.0 -> 41.0 | 56 | holds |
| harness `answering-every-port` 1x1/1if | 110,884 (`bN1`) | 111,220 (`hN1`) | +336 | 55,152 | 41.0 -> 41.0 | 56 | holds |

## 3. Gates (item 3)

### 3.1 Round 2's gates at the composed head; round 1's plants by name

**The harness legs at both heads** (fresh builds of `5b264bf2` and `e45981f8`, #902 round 9's legs, `hs3.sh`; `receipts/harness/measure/`):

| Leg | `5b264bf2` | `e45981f8` | Note |
|---|---|---|---|
| 1x1 arm A: `datapath-events`, `aecp-largest-notice`, `backlog-owed`, `srp`, `aecp`, `aecp-fanout`, `acmp-cmd` | rc 0; 7 recorded budget misses; no STATED | rc 0; the same 7; no STATED | the 7 are `backlog-owed`'s egress-held paths (#902's, tsn-c-stack #26), 61.5-63.6 ms against 20; joins 187.958-190.027 ms in 181.0-239.0, none late or absent |
| 1x1 `answering-every-port`: `notice-every-0`, `notice-burst-0` | rc 0, 0 misses | rc 0, 0 misses | |
| 1x1 `answering-ports`: `aecp` | rc 0, 0 misses | rc 0, 0 misses | |
| 8x8 arm A: as 1x1 less `aecp-largest-notice` | rc 1: STATED `srp` build of one 138,054 and 147,814 > 121,500 | rc 1: STATED `srp` build of one 138,998 and 149,156 > 121,500 | #910's debt, 8x8/2if reported; the rise is instruction-cache placement (SRP's code and every data object unchanged) |
| 8x8 `answering-every-port` | rc 0 | rc 0 | |
| 8x8 `answering-ports`: `aecp`, `aecp-largest-notice` | rc 0; 2 passes over THE SHARE (254,919) | rc 0; the same 2 (255,281) | #902's reported 8x8 condition |

Measured inputs at the composed head against their stated costs: the largest legal record 91,231 cycles at 1x1/1if (975 us stated; 91,625 at base) and 156,972 at 8x8 (1,650 us; 156,716); the datapath events above; THE TRANSMIT's build of one 69,269 cycles at 1x1/1if (725 us stated; 68,937 at base), within it, 730 us by the stating rule: the rows at 730 us in a scratch tree (`cl-rows.diff`) still pass, each at most 0.01 ms more, txL 48.10 within 49.

**Pre-pass at `25ea917f`** (not the full pass: the firmware jobs and lane parts a and c, each a fresh clean clone, while #902's round 10 is outstanding; `r3/gates-out/pre-25ea917f/`):

| Job | Result |
|---|---|
| `firmware-aecp-mutants` | every step rc 0; 282 `[ok]`, 0 other; the nine `face-as-path-*` plants each `[ok]` by its named test |
| `firmware-control-mutants` | every step rc 0; "mutants: 717 of 717 caught"; `[ok] mutant plat-as-path-unavailable (platboot1, platboot2)` |
| `firmware-srp-mutants` | every step rc 0; 345 `[ok]`, 0 other |
| `firmware-unit` | every step rc 0; coverage PASS (39 files; `aecp_face.c` 179/179, 160/160; `ctrl_plat.c` 100 %) |
| lane part c | every gate rc 0: `plat_ledger`, `fixtures`, the five boots, `nvm_selftest` (526 tests, all 144 planted defects reddened) |
| lane part a | every gate rc 0 but the four that exit 1 by design (`rows_tiers_report_exits_1`, `flip_check_exits_1`, `flip_check_1x1_as_built_exits_1`, `flip_check_8x8_exits_1`), each with output identical to `5b264bf2`'s; `tier_grid` 0, `flip_check_1x1` 0, `load_check` 0, `fw_coverage_check` 0, `behave` 0, `twin` 0 findings, `twin_plants` each refused; 39 gates at 0 and the 4 by design at 1 |
| `firmware-boundary` | every step rc 0; "ctrl_boundary: PASS" |
| clones after | lane parts a and c: no tracked or untracked change |

**The second merge, rehearsed.** #902's round 10 is committed in its lane as `7398ec0a` (three commits on `5b264bf2`: `aecp_maps.c`'s assertion and its campaign control, section 13's current rows, a comment) and was not on `origin` yet. In a scratch clone (`r3/cl-trial`) `25ea917f` merges `7398ec0a` with no conflict; `docs_check` 0, the 1x1/1if flip check PASS, the nine `face-as-path` plants present; the eight images (fixture and platform at the four points) are byte-identical to `e45981f8`'s (`receipts/trial/trial-images.log`). So once `894-tiers` carries round 10, the harness measurements above stand for the composed tree.

### 3.2 Full pass once at the final head, clean clone

At `f098f893`, started 09:35 (`final_pass.sh`): 25 dispatched units (every workflow job a PR to dev-soft-core triggers, each on its own fresh clone by `run_wf.py`; lane parts a, b and c, each on its own clone; the harness legs at both points on a clean clone `r3/cl-final-f098f893`) and the four sweep shards, each on its own booked range (`launch_sweep3.sh`).

Launch log (`r3/logs/final-pass.txt`), each a fix to the launchers, none to a gate:
- 09:41: the dispatcher and sweep launcher restarted with `setsid`: the first instances were in the starting tool call's process group. The four units they had started ran on.
- 09:52: the dispatcher's pool limit raised from 3 to 6 (no range free for 16 minutes; the pool measured 3.7 of 32 CPUs busy), each start still gated on the pool's measured load under 16.
- 10:04: the dispatcher and the sweep launcher picked 32-39 in the same second (10:03:08), for `hs-fB1` and shard 0. `hs-fB1` was stopped within a minute and requeued; shard 0 kept 32-39. Both launchers now take one shared `flock` around pick-and-start and hold it 5 s after the start.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| every workflow step | `verify_wf.py f098f893 ... rtl-fast.yml docs.yml elaborate.yml rtl.yml --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4` | **139 steps ran, 226 not run with a reason, 0 bad**; 28 job clones at `f098f893` with no tracked change (four firmware jobs leave `test_ctrl_firmware_shards.py`'s untracked `dispatch-build/`, as at the pre-pass; `docs-check-no-git` removes `.git` by design) | `receipts/gates/verify-table.md`, `gates/job-clones-after.txt`, `gates/wf/` |
| AECP campaign | firmware-aecp-mutants step 9 | 283 `[ok]`, 0 other; the nine `face-as-path-*` plants each caught by name, now from `aecp_face_mutants.py` | `gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| control campaign | firmware-control-mutants step 9 | "mutants: 717 of 717 caught"; `[ok] mutant plat-as-path-unavailable (platboot1, platboot2)` | `gates/wf/rtl-fast__firmware-control-mutants__ci_step_9.log` |
| SRP campaign | firmware-srp-mutants step 9 | 345 `[ok]`, 0 other | |
| lane parts a, b, c | `lane_gates3.sh f098f893 ... a|b|c` | 40 gates at 0, the 4 by design at 1 (`rows_tiers_report_exits_1`, `flip_check_exits_1`, `flip_check_1x1_as_built_exits_1`, `flip_check_8x8_exits_1`); `flip_check_1x1` 0, `load_check` 0, `tier_grid` 0, `py_idiom` 0, `plat_ledger` and `fixtures` the same figures as at `e45981f8`; every clone clean after | `gates/lane/` |
| harness legs | `hs3.sh` on `r3/cl-final-f098f893`: fA1, fN1, fB1, fA8, fS8, fN8, fB8 | rc 0 each but `fS8` (8x8 `srp` alone): rc 1 on its build of one, 138,998 and 149,156 against 121,500, #910, the same figures as the measurement build; every image byte-identical to its measurement build at `e45981f8` | `harness/final-f098f893/` |
| full Verilator sweep | `scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0..3, each shard its own booked range (32-39, 80-87, 48-51 of 48-55, 0-7), picked at each launch | **65 suites (15, 17, 17, 16): 65 passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures**; every shard clone at the head with no tracked change but shard 3's two suite-written `TEST_RESULTS.md`, as in round 2 | `sweep/shard-*/summary.log`, `complete.json`, `suite-logs-sha256.txt`, `sweep/clones-after.txt` |

## 4. Changes this round (file:line, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `e45981f8` | the four conflicts above | both sides kept | item 1 |
| `417f44af` | `sw/firmware/gtest/coverage.ratchet:26` | `ctrl_plat.c` 131/131 (the merge's provisional value) to 132/132 lines, 42/42 branches | the composed tree's measurement (`fw_coverage.py --write` in a clean clone of `e45981f8`, `receipts/early/cov-write.diff`); `--check` passes either way (100 %). The same write shows #902's own `aecp.c`, `aecp_maps.c` and `aecp_mbx.c` rows behind their measurement (611 to 615, 223 to 267, 132 to 136 lines), at 100 %, left as #902's |
| `25ea917f` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (the paragraph after round 30's block) | round 2's paragraph and table (at `cec88385`) replaced by the composed head's, the change against `5b264bf2`; it opens "At the merge of #894's tiers", not "At this branch's head" (R833-2 F1) | the figures at the composed head |
| `25ea917f` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 5, the harness arm's table | a row: the composed head's `answering-every-port` arm at 8x8/2if, 126,012 B, 964 under 126,976 | the same |
| `25ea917f` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, the datapath-events paragraph and a new subsection "GET_AS_PATH through the face" before "What is left" | the three terms GET_AS_PATH enters, each measured or bounded against its stated cost; no stated cost moves | item 2: GET_AS_PATH's cost in the rows, stated |
| `a3a509d7` | (the second sync merge) | #902's round 10, no conflict | item 1, 894-tiers moved |
| `f098f893` | `sw/firmware/ctrl/test/aecp_face_mutants.py` (new), `aecp_mutants.py:15` (the import), `:874` (the rows appended; the constants at `a3a509d7`'s lines 39-41 and the nine `defect` calls at 668-699 removed), `sw/firmware/ctrl/aecp/README.md:275-277` | the nine face plants in their own module, the same rows; the README names it | the 1,000-line module limit at the composition (py idiom ratchet) |

## 5. New checks (planted mutant, failing words)

No new check: no behaviour changed. The composition's own red is the existing py idiom ratchet, planted by the composition itself: at `a3a509d7`'s tree it fails with "FAIL: long module 11 > ratchet 10. New Python complies immediately; see Rule 12 in docs/development/CODE_QUALITY.md." (`receipts/probes/py_idiom_at_a3a509d7.txt`), and at `f098f893` it passes, "long module: 10 <= 10". Round 1's ten plants are each caught by name at the final head (the AECP campaign's nine, now from `aecp_face_mutants.py`, and the control campaign's `plat-as-path-unavailable`).

## 7. Receipts

`receipts/INDEX.md` indexes every receipt (593 files, sizes and sha256, host paths scrubbed before indexing, none over 200 KB; the large logs are listed in `gates/large/` with their sha256 and kept as excerpts). Directories: `sync/` (both merges' side checks, the merge facts and gitlinks), `early/` (the flip, load, idiom and docs checks at `e45981f8`, the flip forms at both heads, coverage, the data-layout comparison), `rom/` (plat_ledger and fixtures at `5b264bf2` and `e45981f8`), `harness/measure/` (the legs at both heads, event costs, record spans, slices, comparisons), `harness/scratch/` (the two scratch arms' diffs and spans, the 730 us rows), `trial/` (the rehearsed second merge's images), `probes/` (the py idiom at `a3a509d7` and `f098f893`), `prepass-25ea917f/`, and the full pass: `gates/` (verify table, workflow logs, job clones, lane gates), `harness/final-f098f893/`, `sweep/`. The scripts are in `../scripts/` (round 3's, from `scratch/scripts/r3`).

## 6. Notes for the next session

- Scratch `/data-2/milan/tmp/897-a776`: round 2's `r2/`, round 1's `rom/`, the `units/` logs and `docs_check.log` deleted at the start (14 GB to 54 MB). Kept: `gates/` (run_wf.py, verify_wf.py, not_run.json, venv), `scripts/`, `bin/`, `std/`. Round 1 and 2 receipts stay in the output directory. Deleting round 2's sweep shard clones `$LANES/897-a776-r2-shard{0..3}` (outside scratch) was refused by the permission policy; they are left in place and round 3 uses the label `897-a776-r3`.
- Round 3's scripts: `scripts/r3/` (`hs3.sh`, `lane_gates3.sh`, `fixtures3.sh`, `launch3.sh`, `dispatch3.py`, `merge_sides.py`, `sram_layout.py`, `eventcost.py` copied from lane 894's tools). Clones: `r3/cl-base` (`5b264bf2`), `r3/cl-head` (`e45981f8`), scratch `r3/cl-span` and `r3/cl-path` (never committed: `build.py` edits that trace `mbx_win_read` and answer an 8-entry path through 9 GSI reads).
- Scratch at the end: 13 GB (`r3/`: the clones `cl-base`, `cl-head`, `cl-span`, `cl-path`, `cl-rows`, `cl-trial`, `cl-final-f098f893`, `sweep-src-f098f893`; the harness builds `r3/builds/`; the pass's outputs `r3/gates-out/`; the sweep `r3/sweep-f098f893/`). The sweep shard clones are `$LANES/897-a776-r3-shard{0..3}` (9.7 GB); round 2's `897-a776-r2-shard{0..3}` are still there (their deletion was refused at the start). No unit of this lane is left running, and no dispatcher or launcher.
- Nothing pushed, no PR opened or edited, no comment edited or deleted, no board touched.
- At posting (2026-11-14 10:17 UTC, 11:17 CET): `894-tiers` `7398ec0a` with R837-5 and R838-5 POSITIVE on PR #902; `dev-soft-core` still `cec88385`, so #902 had not merged and no `dev-soft-core` merge was due. When #902 merges, this branch will need `dev-soft-core` merged (the merge should be clean: it is `7398ec0a` plus #902's merge commit).
