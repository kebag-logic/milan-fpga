[A773] REVIEW READY
Commit: 7398ec0aeea468d92ff642a03a06e291a0cd58d1 (the delta from `5b264bf2` to `7398ec0a`, three commits; PR #902, `894-tiers` -> `dev-soft-core`, still `cec88385`)

Round 10, under #894's assignment (issuecomment-6873298790), answering R837-4 (PR #902 issuecomment-6873294087) and R838-4 (issuecomment-6873195590). There is no behaviour change, and every image is byte-identical to `5b264bf2`'s.

Changed:
- **R837-4-1, the map table's static assertion** (`55b8e621`).
  - `aecp_maps.c` keeps the domain and the floor as separate macros. `MAP_DOMAIN` is `MAP_FIRSTS * MAP_CHANNELS`, the positions `place()` forms. `MAP_FLOOR` is `256u`. `MAP_SLOTS` is the larger of the two, the same expansion and type as before.
  - After `struct edit`, `_Static_assert(sizeof ((struct edit *)0)->slot / sizeof ((struct edit *)0)->slot[0] >= (size_t)MAP_DOMAIN, "the table holds every position place() forms")` bounds the declared array itself. Round 9's assertion was true by definition, so it could never fire. It is removed.
  - **The compile-time control** is AECP campaign row `map-table-each-direction-alone`. It plants `MAP_SLOTS` as the larger direction's own product: 16 slots at 1x1/1if, where an input key's index reaches 56. It is caught only by `aecp_maps.c`'s own compile refusal with the words `static assertion failed: "the table holds every position place() forms"` (`aecp_map_mutants.BUILD`, `aecp_mutants.refused`).
  - `controls()` keeps the build row out of the claimed test set. It holds `refused()` to three reader controls: other words, another file's refusal, and a row that is not a build row. Any other compile failure is still an escape.
  - The two document sentences, in SPLIT_CONTROL_MEMORY section 13 and the AECP README, now say what the assertion holds. Separately, they say the 256-slot floor is a layout choice (#909).
- **R838-4-F1, the current rows** (`947bd389`). Section 13's current table names its tool and head, and gives `flip_grade.py --check`'s figures:
  - 1x1/1if: R4 12.85, R5 72.91, R6 68.80, first 14.51 and last 126.46 ms. The summary's R4 is 12.85.
  - 8x8/2if: 42.09, 189.14, 177.28, 20.24 and 626.87 ms. This row of the same table was that tool's output at `a07de012`, so it was stale in the same way.
  - The progression table and the historical sentences keep their named states.
- **R838-4-F2:** the PR body's core command is `--core --filter 'Core.*Map*:Core.Every*'`. At the head it passes 13 tests; round 9's filter passed 8.
- **RESIDUE, each with the report's exact fix:**
  - R837-4-R1: `aecp_arms.py:17-19` (`7398ec0a`).
  - R837-4-R2: `SPLIT_CONTROL_MEMORY.md:2314` and `:2322`, with the same paragraph's two other "at this head" read the same way. No figure changes.
  - R838-4-R1: the PR body's "the first REMOVE is 1,165 visits against 2,078".
- **Suggestions:**
  - R838-4-S10: the PR body's share bullet now states only what the leg's receipt carries, the heaviest work pass, 149,490 of 200,000 cycles.
  - R837-4 S5 / R838-4-S7: the packet index is generated from the published bytes.
  - The others are not taken this round.

Validation (on clean clones at the head, never piped):
- **Every image is byte-identical to `5b264bf2`'s.** I hashed 332 files: 8 ELFs, their 8 binaries and 316 objects, built on one clone path at both heads. A second `5b264bf2` build reproduces them, and a `MAP_FLOOR` of 264 planted as a control changes 24 of them.
  - By the assignment's rule, the sweep is not run.
  - Round 9's measurements stand: the record, the datapath events, the harness legs and the join intervals.
- **Every hosted job step** of rtl-fast, rtl, elaborate and docs, run locally (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`): 139 run, 226 not run with a reason, 0 bad. The sweep's steps are among those not run, and their reason says so for this round.
- **The firmware jobs:** every step is 0.
  - The firmware suite: `test_ctrl_firmware: PASS`.
  - `fw_coverage.py --check`: PASS over 39 files.
  - The AECP campaign: 274 of 274 caught, `map-table-each-direction-alone` among them.
  - The control, SRP and boundary campaigns, and the firmware Verilator job.
- **The assertion's own controls:**
  - The build row alone (`aecp_mutants.py --shard 257 274`) prints `[ok]`.
  - With round 9's assertion planted back, the same row escapes: the plant compiles, no test runs, exit 1.
  - The probe compiles `aecp_maps.c` with the arms' flags at the five checked-in configurations, 16x4 and 16x32. The source as committed compiles at all seven. Each direction's own product is refused at the three configurations where it is smaller than the domain. The floor alone, or the array declared at the floor, is refused at 16x32 (544 positions).
- **Lane gates:** 46 at 0. The four that exit 1 are the reported 8x8/2if and as-built checks, by design. They include:
  - the diff checks against twelve bases, `5b264bf2` among them;
  - em-dash, 0 findings over 26 pages;
  - the Python and C++ idioms, docs, and `ctrl_hot`;
  - `tier_grid.py --point 1x1/1if`, 18 of 420;
  - the self-tests: rows_tiers 971/971, flip 555/555, load 25/25, and the harness's 0 failures with 246 mutants caught and 0 escaped;
  - `load_grade.py --check`, 0.513 / 0.509;
  - the builder, NVM, boot (1x1, 8x8, native, plants), BDD, and the twin with its plants.
- **The core filters at the head:** `'Core.*Map*:Core.Every*'` passes 13 tests and `'Core.Map*:Core.Every*'` 8.

Acceptance criteria (1x1/1if, `flip_grade.py --check --point 1x1/1if`: RESULT PASS, every row by every source):
- **The rows:**
  - R4 12.85 / 20; R4L 188.39 / 238;
  - ACMP 28.44, ADP 26.83, MAAP 26.95 / 30;
  - first 14.51 / 20; R5 72.91 and R6 68.80 / 90; last 126.46 / 130;
  - tx 29.86 and txL 48.09 / 49.

  Section 13's current table and summary give the same figures, cell for cell.
- **The design:** the pace is 8 ms, the slice 900 us, and `tier_grid.py` chooses the built design.
- **The loads:** 0.513 at the pin and 0.509 with tsn-c-stack#32 (0.70).
- **The images:** byte-identical to `5b264bf2`'s, each within its cap.
- **No STOP trigger:** no image changes, and no behaviour change is needed.

Open risks/questions:
- **The floor is a layout choice backed by measurement** (#909). The assertion bounds the table's size, not its timing. A later change to the edit's frame, or to the data near it, can move the record. Each full pass's `aecp-largest-notice` legs re-measure it.
- **The compile-time row runs at the campaign's configuration, 1x1/1if.** The probe receipt covers the other six geometries, and the assertion compiles into every build.
- **Unchanged duties:** 8x8/1if is lane 894b's; 8x8/2if stays reported (#910); #908 stays open by its own terms; S12b's wire capture is owed.
