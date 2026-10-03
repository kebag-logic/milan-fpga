# [A507] Round 3 of lane P2 (PR #145): handoff

- Assignment: #15 comment 5961238126. It answers R436-2 (5961230273, one MINOR) and R437-2 (5960887168, three MINOR), both NEGATIVE.
- Branch `p2-nvm-port-robustness`. Start head `c0715410418b47ffaccf5feed55b71617fcfaf82` (pushed). Commits were added; nothing was amended.
- Final head: `527662d659b4ead97675744d12a43af1ea92b9b3`, local and not pushed. Seven commits:

  | Commit | Item |
  |---|---|
  | `593f291` | item 1 |
  | `ae1cb85` | item 2 |
  | `355e7d3` | item 3 |
  | `6fb74ad` | the parent's Python idiom gate: a docstring on item 2's nested helper |
  | `f4519fe` | item 4 |
  | `46796bf` | item 5: `git merge --no-ff` of main `88969246` (#144, lane C8) |
  | `527662d` | item 5: `git merge --no-ff` of main `c74711d4` (#146, campaign drivers' `--jobs N`); no conflict |

- TAKEN: #15 comment 5961243270 (2026-10-02 20:48Z). REVIEW READY: #15 comment 5963684192 (2026-10-03 00:35Z), head `527662d`.
- **Item 5, main moved.** At 22:43Z `origin/main` was `88969246`: PR #144 (C8) had merged at 21:50Z.
  - **Merged** with `--no-ff`. The one conflict was 09: both sides appended an §8.5. Both are kept: C8's §8.5 first, then this lane's section as §8.6, and §8.2's pointer now reads §8.6.
  - **Auto-merged:** 01, 07 and the integrator guide, with every hunk of both sides intact. Every one-sided file equals its own side.
  - **Main moved again.** At 00:00Z main was `c74711d4` (#146, merged 23:58Z). It changes only eight mutation drivers, their READMEs and the new `tb/common/mutant_pool.py`. It was merged `--no-ff` as `527662d` with no conflict, and `hdl`, `docs`, `tb/nvm_port` and `tb/acmp_nvm` are unchanged by it.
  - **Last fetch** before posting: main is still `c74711d4`, contained in the head.
- Scratch, outside the tree: `$VALIDATION_STORAGE/ppP2-a507`.
  - Helpers: `wt.sh`, `plants.py`, `models.py`, `fastfig.py`, `checkclaims.py`, `ooc/`, `status.sh`.
  - Logs: `gates/`, `pgates/`, `logs/`.
  - Reviewer re-runs: `rev/`.

## Per finding

### R436-2 F1 (MINOR): Q1 and Q9 passed all 343 checks

- **The change.** T30, `a_paused_or_latched_cycle_is_never_charged` (`tb/nvm_port/sim_main.cpp:2187-2272`; called at `:2764`). Each arm starts from a reset of its own.
  - (a) An ERASE answered on its own grant, then the WRITE granted `TMO` cycles late: served.
  - (b) The header READ answered on its eighth byte, then the payload grant `TMO` cycles late: served.
  - (c) and (d) A byte `TMO` cycles late on the one cycle the manager drops `rready` (c) or `wvalid` (d), the count at its bound: served. The drop is placed by `mgr_drop_gap`, `sim_main.cpp:312`, `:696-713`.
  - (e) The control, one owed cycle later: DEADLINE at `TMO` + 3 cycles, the held cycle counted.
- **The contract it serves.** The banner (`KL_pp_nvm_port.sv:69-83`) and 02 §8: a terminal already latched is not owed, and a paused cycle neither counts nor ends the operation (`:260-261`, `:277`).
- **Now failing without it.**
  - Q1 fails T30a and RW4.
  - Q9 fails T30c, T30d, T30e and RW4.
  - Both fail under all four models in R436-2's own `plant.py`, run unchanged (`rev/plant-out/plants.md`).
  - Both also fail R436-2's own `directed.py` R436d/e beside T30 (`rev/directed-out/SUMMARY.txt`).
- **The reviewers' fuzz modes, folded in as a standing check.**
  - `tb/nvm_port/fuzz_main.cpp` has modes FZ1-FZ9: legal, silent, resume and babble.
  - It is built by `make` (`tb/nvm_port/Makefile:35-48`) at `FUZZ_TMOS = 1 2 3 37`.
  - Q1 and Q9 at bound 3 fail FZ2, FZ3, FZ6 and FZ7 (gate rows Q1/fuzz and Q9/fuzz).

### R437-2 F1 (MINOR): a paused cycle at the bound is never a verdict

- **The change.** T30c, T30d and T30e (as above).
- **Now failing without it.**
  - Y11 fails T30c-e and RW4, and so does Y16.
  - R437-2's own Z1a and Z1b, injected unchanged by its `spec_z2_directed.py`, pass at the head under all seven legal models at 100 and 37. They fail on Y11 and Y16 (`rev/r437-out/spec_z2_directed.txt`).

### R437-2 F2 (MINOR): the latched-done term in `S_WEWAIT`

- **The change.** T30a, plus T30b for `S_RHWAIT` under the pristine model.
- **Now failing without it.** Y1 fails T30a and RW4, and Y2 fails T30b and RW4, under every legal model at 100 and 37 (`rev/r437-out/spec_y_pause.txt`).
- **Equivalence.** Y3 and Y4 (Q3 and Q4) are measured equivalent and argued in the README: a latched done takes `S_WWAIT` and `S_RPWAIT` to `S_FIN` and then `S_IDLE`, which zeroes the count.
- **Docs.** The README and 09 §8.5 now say which wait states are pinned.

### R437-2 F3 (MINOR): the TMO-derived harness at every legal bound

- **The change.** T6's poke is named on the bus. It comes once the backend has taken the ERASE (`sim_main.cpp:1021-1049`).
- **A third suite build at 20,** the suite's smallest legal bound (`Makefile:15-18`, `:42-48`). The suite's `static_assert` keeps it at 20 and up; the port's bounds 1, 2 and 3 are graded by the randomized harness.
- **Contract.** Round 2's assignment item 5, and #21 item 4: coincident completion is a freedom the port must take.
- **Now failing without it.** Round 2's T6 under the coincident model fails 16 of 356 at 4096 (gate row `T6-timed/coincident/4096`). In the scratch calibration it failed 15 at 500 and 16 at 1000.
- **Evidence.**
  - Scratch, every model at the head at 20, 37, 100, 1000, 4096 and 100000 (`mdH.txt`): the seven legal models are 356/0, and short read (273/83) and silent (115/241) give the same figures at every bound with every RW check passing.
  - R437-2's `spec_bounds.py` and `spec_bounds2.py` at the head: all 0 FAIL from 20 to 100000.
  - Its `spec_t6stage.py` cannot apply, because its anchor is the old staging.

### R436-2 S1 = R437-2 S1 (taken as item 2): the owed READ's drain

See item 2.

### R437-2 S2 (taken as item 3): a late grant that carries err

See item 3.

### R436-2 R1, R2 (RESIDUE, item 4)

- **R1.** `tb/nvm_port/README.md:479` reads "T24, T28 and T29 grade all of it at `TMO` = 100, …".
- **R2.** `:545-546` now name the 11th and the 21st bytes. The same two ordinals are corrected in the PR body's Round 2 item 4.

## Per item

1. **Device models and mutations.**
   - No model was added to the gate's MODELS table.
   - The harness gained these armings:
     - `mgr_drop_gap`, a strobe dropped on the bound cycle;
     - `gnt_err_with_grant` (item 3);
     - the babbling READ, by setting the abandoned command's length past its end, as R437-2's BABBLE probe does.
   - The randomized harness has its own device and manager.
   - **Mutations:** every R436-2 Q-plant and R437-2 Y-plant is a gate row, with edit text compared byte-identical by script (26 rows, `deadline_rows.py`). Each reddens:

     | Plant | Checks failed |
     |---|---|
     | Q1, Y1 | T30a, RW4 |
     | Q2, Y2 | T30b, RW4 |
     | Q5, Y5 | T24, T29a-b, T30a-b, RW4 |
     | Q6, Y13 | T29a, T30e, RW1 |
     | Q7, Y14 | T29b, RW1 |
     | Q9, Y16, Y11 | T30c-e, RW4 |
     | Y6 | T24, T30b, RW4 |
     | Y7 | T24, RW4 |
     | Y8 | T24, T28c, T28f, RW1 |
     | Y9 | T24, T29b, RW1 |
     | Y10 | T24, T28a, T28d, T28f, T29a, T30e, RW1 |
     | Y15 | T24, T28, T29, T30e, RW1, RW3 |

     Q3, Q4, Q8, Q10, Y3, Y4 and Y12 are measured equivalent, at 0.
   - **Bound rows:** `coincident/4096` 0, and `T6-timed/coincident/4096` 16.
   - **No RTL change.**
2. **Device models and mutations.**
   - **Armed:** T28f's babbling READ, and the fuzz's babble mode FZ9.
   - **Mutations:** D27 (round 2's unbounded drain) 3; D28 (the whole length) 1; D29 (no decrement) 3; D30 (retaken at a later deadline) 3; D27/fuzz FZ9.
   - **RTL change.** It serves the banner (`KL_pp_nvm_port.sv:85-99`) and 02 §8: a READ owes at most its length, and bytes past it are not progress.
     - `KL_pp_nvm_port.sv:222`: `owed_left_r`.
     - `:285-296`: `left_w` and `drain_w`.
     - `:323-327`: the `nvm_port_owed_left` block.
     - `:610`: the drain.
     - The banner rewrite at `:85-99` keeps its line count.
   - **Lines moved.** The in-tree citations moved: `:233-244` to `:234-245`, `:319-323` to `:340-344`, `:415-418` to `:436-439`, M1's `:345`/`:359` to `:366`/`:380`. The ARMS table is now 376…529.
3. **Device models and mutations.**
   - **Armed:** `gnt_err_with_grant`, graded in `late_grants_that_leave_nothing_owed` (`sim_main.cpp:1936-1972`).
   - **Mutations:** X20 as D31 fails 2 (the T24 arm). D11 now fails 4.
   - **No RTL change.**
4. **No RTL change.** README wording only, plus the PR body ordinals.
5. **Merge** `46796bf` (see Status). No RTL of this lane changed in the merge; main's `KL_aecp_desc_store.sv`, descriptor generator, `tb/desc_store` and docs came in.

## Parent-visible list

1. No port or parameter change. `KL_pp_shadow` needs no edit, and the port-contract count is unchanged (1,757 processor ports).
2. One device-face behaviour change. After a deadline, an abandoned READ's bytes past its length are not taken, and the next request ends DEADLINE until the backend ends the READ or a reset. `KL_nvm_backend` and the responder never present more than a READ's length.
3. **The parent patches are unchanged.**

   | Patch | sha256 | Size |
   |---|---|---|
   | `parent-adoption-p2-cdf49d1a.patch` | `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b` | 9,728 bytes |
   | `parent-adoption-c4c6-ea3fb388.patch` | `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c` | 2,687 bytes |

   The banner text the p2 patch paraphrases is unchanged.
4. Processor documents the parent reads: 02 §8, and 09 §8.6 (renumbered from §8.5 by the merge).

## Gates (at `f4519fe`, pinned Verilator 5.050)

**Processor gates.** Logs are in `$VALIDATION_STORAGE/ppP2-a507`:
- wave 1 in `r1/`, at `f4519fe`;
- wave 2 in `r2/`, at `46796bf`;
- wave 3 in `gates/` and `pgates*/`, at `527662d`.

Wave 3 ran only what #146's files feed:
- the eight changed campaigns, at their default `--jobs`, all identical to the earlier waves;
- `srp_admission` 12 of 12, and `retry_mutants` 62 killed with 7 equivalence controls;
- the docs gates;
- the parent light gates 1-11 for both patch sets.

| Gate | `f4519fe` | `46796bf` | Result |
|---|---|---|---|
| `run_suites.sh` | rc 0 | rc 0 | 33 suites, 1,020,123 checks, 0 failing; `nvm_port` 1,104 |
| `make -C tb/nvm_port figures` | rc 0 | inputs unchanged | 129 builds, all agree, 1,203 s |
| docs (CI docs job, `make check`, `gen_matrix --check`) | rc 0 | rc 0 | links 1,045, and 1,060 after the merge |
| `lint_hdl.sh`, `syn/yosys/run.sh` | rc 0, 0 | rc 0, 0 | 41 modules; 36 tops and the memory-map check |
| d3 (`--jobs 3`) | rc 0 | rc 0 | 87 of 87 |
| aecp | rc 0 | rc 0 | 55 of 55 |
| aecp-dispatch | rc 0 | rc 0 | 37 of 37 |
| maap | rc 0 | rc 0 | 29 of 29 |
| adp | rc 0 | rc 0 | 30 of 30 |
| acmp | rc 0 | rc 0 | 19 of 19 |
| notify | rc 0 | rc 0 | 40 of 40 |
| gsi | rc 0 | rc 0 | 20 detected |
| name_wr | rc 0 | rc 0 | killed |
| srp_top | rc 0 | inputs unchanged | 78 of 78, coverage 65/65 |

Every campaign's verdict lines are identical across both waves and round 2b.

**Mutation tables.** These are the gate rows (fails of 356). Per-plant names are in the README's table and in `ff3.json`.
- The reviewer plants: Q1 2, Q2 2, Q5 17, Q6 3, Q7 2, Q9 4; Y1 2, Y2 2, Y5 17, Y6 7, Y7 10, Y8 12, Y9 9, Y10 15, Y11 4, Y13 3, Y14 2, Y15 68, Y16 4.
- The equivalents: Q3, Q4, Q8, Q10, Y3, Y4 and Y12 are 0.
- Item 2: D27 3, D28 1, D29 3, D30 3.
- Item 3: D31 2, D11 4.
- On the randomized harness at bound 3 (fails of 9): Q1/fuzz 4, Q9/fuzz 4, D27/fuzz 1.
- At bound 4096: coincident/4096 0, and T6-timed/coincident/4096 16.

**Parent consumer set (16), at dev `cdf49d1a`.** At `527662d` the light gates 1-11 were re-run. Set A again fails only gate 10, and set B passes all eleven; the heavy gates 12-16 read nothing #146 changed.
- At `f4519fe`, with c4c6 then p2: all 16 rc 0 (`r1/pgates/`).
- At `46796bf`, with c4c6 then p2 (`pgates/`): 14 of 16 rc 0.
  - Gate 10 (`test_builder`, rc 1) and gate 15 (`milan_dp`, rc 2) fail on main's C8 default descriptor lint ("L1 port-cluster-minimum" on the parent's 8x8 model).
  - Plain main `88969246` with c4c6 + p2 fails gate 10 identically (`pgatesC/`).
- At `46796bf`, with c4c6 then C8's `parent-adoption-c8-cdf49d1a.patch` then p2 (`pgatesB/`): all 16 rc 0, with results equal to `f4519fe`'s. `test_builder` passes, and `milan_dp` gives 9 RESULT: PASS with no FAIL lines.
  - The patch came read-only from milan-fpga branch `ppC8-review-evidence`, at `review-evidence/ppC8-r1/author-r4/` (sha256 `aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209`, 8,482 bytes).

**Reviewer scripts** (`rev/`): see the PR body's Round 3 validation. The only one that cannot apply is R437-2's `spec_t6stage.py`, whose anchor is the old T6 staging.

**Peak memory:** 8.7 GB anon, during the first wave.

## Out-of-context cost

The recipe is sv2v, then Yosys `synth_xilinx -family xc7 -flatten` (`$VALIDATION_STORAGE/ppP2-a507/ooc/ooc.sh`). Main `631eeb34` is 197 LUT, 118 FF and 14 CARRY4.

| Setting | Round 2 | Round 3 | Delta |
|---|---|---|---|
| default | 245/148/21 | 296/164/30 | +51 LUT, +16 FF, +9 CARRY4 |
| 1 | 248/122/14 | 287/138/23 | +39 LUT, +16 FF, +9 CARRY4 |
| 2^31-1 | 266/152/22 | 301/168/31 | +35 LUT, +16 FF, +9 CARRY4 |
| 125M | 261/148/21 | 309/164/30 | +48 LUT, +16 FF, +9 CARRY4 |

## Notes for a continuation

- **The figures gate** takes about 20 minutes under load (1,203 s, 129 builds). `measure_figures.py` is 989 lines, against the parent's 1,000-line module ratchet, so new rows go in `deadline_rows.py`.
- **Reviewer anchors kept intact on purpose.** The reviewers' scripts must keep applying, so these anchors were left exactly as they were:
  - in `sim_main.cpp`, the `held_since_evt` line, the `drop` line, and the call pairs `a_manager_strobe…/reset_mid_commit…` and `a_short_command…/every_operation…`;
  - every RTL line the plants edit.
- `scripts/__pycache__` in the trusted checkout predates this round (07:35), and was left alone.

## REVIEW READY

#15 comment 5963684192, posted 2026-10-03 00:35Z, for head `527662d659b4ead97675744d12a43af1ea92b9b3`. Main was `c74711d4` at the last fetch, seconds before. A continuation waits for the re-reviews and must not re-post.
