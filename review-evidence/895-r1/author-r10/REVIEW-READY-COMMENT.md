[A775] REVIEW READY — round 10, head `1215bd82` (local, not pushed)

Commit: `1215bd82` (`895-talker-redeclare` on the PR's `056d619d`, two commits; the manager pushes). It answers R835-4 (PR #901 issuecomment-6900107977) and R836-4 (issuecomment-6899966960). The roles name R835-5 and R836-5 next.

**For the merge candidate of `056d619d`:**
- **No image input changed after `056d619d`.** All 552 image files of every point (each ELF's loadable bytes and every linked object) are identical by sha256 at `1215bd82`, and `plat_ledger.py` passes at every point.
- **Non-markdown paths did change**, two of them, both test-side: `sw/firmware/ctrl/test/srp_talker.cpp` and `sw/firmware/ctrl/test/srp_talker_mutants.py`. The other five are markdown: `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md`, `sw/firmware/ctrl/aecp/README.md`, `sw/firmware/ctrl/plat/README.md` and `tb/verilator/ctrl_service_budget/README.md`.
- Every job that reads one of the seven paths ran again at `1215bd82` (below). The jobs that read none carry from round 9's full pass at `056d619d`.

**R836-4-F2 (MAJOR):**
- **The survey's two defects are fixed** (`round10/scripts/costs_vs_stated.py:145,185`):
  - the paced class is now read under its key, `classes.paced`;
  - `record_classes.held` now gets the record's command;
  - `record.aecp` is counted like every other statement.
- **The head's `record_classes.py` CLI over every preserved leg of rounds 8 and 9: RESULT PASS.** It ran in one pass over arm A merged, `answering-every-port`, `valid-destinations` and arm B, at 1x1/1if and 8x8/2if. The dearest record of each class, by the rule, against its statement:

| Point | Paced | Ordinary | Long |
|---|---|---|---|
| 1x1/1if | 28,288 cycles (accepted SET_CONFIGURATION): 300 of 300 us | 21,187: 225 of 235 us | 86,698: 915 of 975 us |
| 8x8/2if | 55,365 (accepted SET_CONFIGURATION): 585 of 595 us | 18,904: 200 of 265 us | 126,152: 1,325 of 1,650 us |

- **SET_STREAM_INFO** is 20,363 cycles at 1x1/1if (215 of 235 us) and at most 17,511 at 8x8/2if (185 of 265 us). It is held only when its command is passed.
- **No measurement exceeds its statement.** Nothing is restated, and the rows, load, pace and slice stand.
- **8x8/1if** is reported by class and never held (`record_classes.held`). This lane has no leg at that point and ran none.
- **The planted controls**, each on a copy of arm B's leg:
  - an accepted SET_CONFIGURATION raised to 40,000 cycles at 1x1/1if and 60,000 at 8x8/2if;
  - a SET_STREAM_INFO raised to 30,000 at each point.
  - Each is refused by the class grader over every leg, naming the record, and by the corrected survey (UNDER 1, rc 1). Round 8's survey passed all four.
  - Unplanted copies pass all three paths.
- **Coverage, corrected** (section 13, "The record classes graded (#895)"):
  - 63 statements a point: 57 measured, all within by the rule, and 6 derived and not staged.
  - The rounds 6, 7A and 8 claims are qualified where they stand.
  - `aecp_mbx.h`'s round costs are held by each leg's round check.

**R835-4-F1 (MINOR):**
- **The new test:** `Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriodsAfterTheLatestLeave` (`srp_talker.cpp`).
  - It requests the Leave on a centisecond and holds the loop `10 * CTRL_LOOP_JOIN_CS + CTRL_LOOP_TX_MS` after it.
  - It checks that the Leave leaves exactly then.
  - It requires the changed destination at least two LeaveAllTime periods after the Leave on the wire: 20,005 ms at two interfaces and 20,006 ms at one.
- **Three new plants** in `srp_talker_mutants.py`, each caught by name at 1x1/1if and 8x8/2if:
  - `talker-hold-off-drops-the-transmit-term` (the reviewer's m1: 19,895 / 19,966 ms);
  - `talker-hold-off-rounds-the-transmit-term-down` (19,995 / 19,996 ms);
  - `talker-hold-off-drops-the-join-and-transmit-terms` (m2).
- **The SRP campaign at the head:** 421 rows, 76 of them `talker-` (38 at each count), 0 escaped.

**R836-4-F1 and R835-4-F2 (MINOR):**
- Every listed passage (the reviews' line numbers, at `056d619d`) is restated as this head's, or given its subject: #894's head, or the round of this branch that measured it.
  - The two queued-notice and TX figures: `SPLIT_CONTROL_MEMORY.md:2266,2689`, `aecp/README.md:120`, `ctrl_service_budget/README.md:172`.
  - The earlier images and figures: `SPLIT_CONTROL_MEMORY.md:519-530,2551,2682,2688`, `FR_NFR.md:390`.
- Sections 5 and 13 gain provenance leads. Section 5 gains this head's own table: `ctrl_plat` 18,240 B; the platform 8x8/2if at 131,752 B with 1,368 B left; the arms with 60 and 200 B left.
- **The inventory** (`receipts/docs/superseded-inventory.md`) covers every tracked-text hit of each superseded figure: 178 hits, each classed, and none states a superseded figure as this head's.

**Residues and suggestions:**
- **RS1 (both reviews):** the roles are corrected.
- **R835-4-S1:** taken. The 18 us is the bounds' headroom; the flip check refuses `CTRL_LOOP_TX_MS` 34 from a 226 us base, at a tx row of 34.02 ms (reproduced).
- **R835-4-S2:** taken.
- **R835-4-S3:** retained.

**Validation** at `1215bd82`, each job on its own fresh clean clone:
- **The jobs that read a changed path**, each failed 0:
  - docs.yml's every job;
  - rtl-fast's `changes`, `bdd-conformance`, `firmware-unit` and the three mutant jobs;
  - rtl.yml's `full-ci-gate`.
- **Verify:** 86 steps ran at the head and 53 carried from `056d619d` (139, as there); 226 not run with a reason; 0 bad.
- **Campaigns:** control 716 of 716; AECP 299 rows; SRP 421 rows (76 `talker-`); 0 escaped. `fw_coverage.py --check` passes.
- **Lane gates a:** all rc 0 but the two 8x8/2if flip checks (by design). `harness_selftest`: 0 failures.
- **The 27 workflow check scripts:** rc 0.
- **Carried from round 9's full pass at `056d619d`** (they read no changed path, and the images are identical): rtl-fast's lint, Yosys, census, split CDC, boundary and Verilator jobs; rtl.yml's Yosys tool and shards; elaborate.yml; lane gates b and c; the 65-suite sweep.

**1x1/1if at the head (unchanged):**
- R4 13.25 of 20 ms;
- R5 75.84 of 90;
- R6 73.36 of 90;
- the first queued notice 14.72 of 20;
- the last queued notice 136.65 of 140;
- R4L 203.57 of 238;
- ACMP 29.63 of 30;
- ADP 27.86 of 30;
- MAAP 27.96 of 30;
- tx 34.00 of 49;
- txL 48.58 of 49.

A pass costs 260 us and every row holds up to 278 us, so the bounds' headroom is 18 us.

**Open risks/questions:**
- **The margins:** ACMP 0.37 ms and txL 0.42 ms, and the 1x1/1if paced record at its statement exactly.
- **8x8/1if's records are not reported** (no leg). Reporting them takes a new bank of every arm at that point.
- **Not run:** act and the hosted exact-head contexts, which follow the push.

Receipts: round 10's packet, with `INDEX.md` generated from the files present: classes, plants, the talker arms and plants, the inventory, identity, the ledger and gates. Nothing was pushed.
