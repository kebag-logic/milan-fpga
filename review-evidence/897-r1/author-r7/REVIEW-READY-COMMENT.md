[A776] REVIEW READY
Commit: `59c934c6` (round 7, the sync onto `dev-soft-core` `70f4056f`; round 6's `b15da60a` met the bar, R833-6 POSITIVE)

Round 7, the manager's assignment: the sync, and nothing else. #902 merged as `659d7687` and #901 as `70f4056f`. Not pushed.

Changed:
- **`d0355a45`, the merge.** One `--no-ff` merge of `dev-soft-core` `70f4056f`, parents `b15da60a` and `70f4056f`, merge base `234bc149`. Eight files conflicted, and each keeps both sides' behaviour:
  - `build.py`'s arms comment: both arms. The module docstring's second paragraph is rewrapped, the same words, so the composition stays within the 1,000-line module limit (1,001 otherwise).
  - `run.py`'s `--variant` help: both arms.
  - `load_grade.py`'s two stated columns: #901's tables, with `record.aecp` at 1x1/1if this branch's 245. Each cost is the one of the side that moved it from `234bc149`, the larger where both did (#895's composition ruling, item 2). Only that cell differs from `70f4056f`'s.
  - `ctrl_memory.py`: the platform's 8x8/2if entry carries `ctrl_plat` 20,352 B, as `plat_ledger.py` measures the composed image, and both rulings' reasons.
  - `coverage.ratchet`: by `fw_coverage.py --write` on the composed tree, as CI checks it. `ctrl_plat.c` measures 132/132, and four more rows are recorded at their measured totals, each 100 %.
  - The plat README, FR_NFR 3.4.1 and `SPLIT_CONTROL_MEMORY.md` (12 hunks): the current lines at the composed figures, and both lanes' history in their merge order.

  Every other file carries each side's own diff exactly (`merge_sides.py`).
- **`4b9dc6ce`, by the rule.** `CTRL_LOOP_TX_MS` at 1x1/1if goes 34 -> 35 ms for the composed tx row's 34.20 (#895 issuecomment-6895331865, item 1). The hold-off stays 2,023 cs, and all 12 images are byte-identical at either figure. The self-tests' plants move with the figure.
- **`4b9dc6ce`, by the owner's decision of 2026-11-15** (#665 issuecomment-6892332745). The size fixture's 8x8/2if entry goes 59.0 -> 59.5: the three harness arms on it need 127,096 to 127,416 B, past 59.0's 126,976. That is S14 debt, not a stop. `test_ctrl_memory.py` holds 59.5 and refuses 60.0.
- **`59c934c6`.** Section 13's "GET_AS_PATH on SRP's Talker declarations", as the composed image measures it.

Validation:
- **The composed images** (`plat_ledger.py` 7 of 7 controls, PASS at every point):
  - platform: 117,800, 119,384, 130,504 and 132,064 B (43.0, 44.0, 56.0, 60.5; 1,056 B left in 133,120 at 8x8/2if, within ruling item 3's 133,120);
  - fixture: 112,744, 114,304, 125,408 and 126,928 B (41.5, 42.5, 55.0, 59.0).
  - Each is #901's plus GET_AS_PATH's 304 to 320 B. `sram` and `ctrl_plat` are #901's, and no writable symbol moves (#909).
- **The rows at the composed tables** (`flip_grade.py --check --point 1x1/1if` PASS at the built design, 900 us):
  - R4 13.40, R4L 203.57, ACMP 29.82, ADP 28.05, MAAP 28.15;
  - first 14.73, R5 76.10, R6 73.61, the last queued notice 136.99 of 140;
  - tx 34.20, txL 48.77 of 49.

  The load is 0.519 at the pin and 0.516 with tsn-c-stack #32. The pace stays 9 ms. The slice rule holds 6 of 420 and chooses the built 900 us.
- **Measured again on the composed image:** every group of every arm at both points, arm A (96 / 94), the every-port arm (16), `valid-destinations` (2) and arm B's three groups.
  - Every leg exits 0 with no refusal. The misses are the seven held-egress `backlog-owed` paths at each point (#26). The joins are 185.525 to 190.193 ms.
  - **Every stated 1x1/1if cost holds by the rule.** The nearest is AECP's timer slot at 75 of 75 us. The only exceedances are the two class lines, each held by its class: the long notice at 360 of 365, the paced SET_CONFIGURATION at 295 of 305. **No cost is restated.**
  - **`record_classes.py` over every leg at both points: PASS.** At 1x1/1if: long 910 of 975, ordinary 220 of 245, paced 295 of 305. At 8x8/2if: 1,335 of 1,650, 200 of 265, 580 of 595.
  - **GET_AS_PATH's answered read:** 16,500 cycles, 175 us, at 1x1/1if; 14,521 and 14,318, 155 us, at 8x8/2if. Each is SUCCESS with eight entries at control_data_length 80. Arm A's refused response is 11,308 cycles.
- **Gates at `59c934c6`**, each part on its own fresh clean clone:

  - **Firmware:** the unit suites PASS; `fw_coverage --check` PASS (39 files); AECP 308 caught, the nine GET_AS_PATH plants by name; control 717 of 717; SRP 421 caught; `ctrl_boundary` PASS.
  - **Workflows:** every `rtl-fast` and docs job and `run:` step: 108 ran, 94 not run with a stated reason, 0 bad. `publication-census` timed out once on the shared pool (sv2v's 900 s) and passes alone on a booked range.
  - **The split-firmware Verilator suites**, each alone: `milan_dp` PASS (4,083 s of 4,800), `mbx` PASS, `milan_dp_gm_steps` PASS.
  - **Lane gates:** 45 gates.
    - 39 at 0, among them the harness self-test (0 failures, 250 of 250 mutants), `record_classes --selftest` (14 of 14 and the port check), `plat_ledger`, `test_ctrl_memory`, `docs_check` 0 findings, the em-dash gate against `70f4056f` and `234bc149`, and both idiom ratchets.
    - The 4 that exit 1 by design refuse round 6's rows.
    - The `milan_dp` twin and its plants: a red `dev-soft-core` already carries (below).
  - **Harness legs, one a point and arm:** 8 of 8 rc 0, each ELF byte-identical to its measurement build.

Acceptance criteria (the round-7 assignment):
- **Item 1 met.** One `--no-ff` merge with a resolution table. The ratchet is from its tool, and no generated file was hand-edited.
- **Item 2 met.** Every split image is built and its ROM reported; the one entry an image passed is raised as S14 debt. The 1x1/1if legs and the class grader at both points are re-measured on the composed image. A statement is restated only by the rule, and the rows, pace and slice are recomputed under the existing rulings.
- **Item 3 met** (above).
- **No STOP condition holds:** the last queued notice is 136.99 ms within 140, every 1x1/1if row is within its bound, and the load is 0.519 against 0.70.

Open risks/questions:
- **8x8/2if, reported:** AMAP_LIVE_WRITE measures 28.82 us, 35 by the rule, against the 30 stated there. It is not restated: an 8x8/2if cost moves that point's tx row, and so `CTRL_LOOP_TX_MS` and the hold-off at two interfaces, a firmware change outside this sync. For #894's 8x8 lane and #890.
- **The harness arms on the 8x8/2if fixture** now plan 59.5, and the fixture itself 126,928 B, 48 B before its next granule. Both are S14 debt.
- **A red already on `dev-soft-core`:** the `milan_dp` twin and its plants exit 2. The twin is a lane gate no workflow runs. Its owed row `split-talker-failed` still expects the split's behaviour before #895. The finding and the plant verdicts are identical on a clean clone of `70f4056f`, so the composition does not cause it. For #895's lane (#901).
- **Carried:** one AVB_INTERFACE an image at two interfaces (raised for a decision); the 64-entry path's control_data_length.
