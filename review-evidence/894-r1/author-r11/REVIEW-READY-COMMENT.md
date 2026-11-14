[A773] REVIEW READY
Commit: 9606b3a915de284c71d3063c2e8d94b097f18241 (ten commits on `7398ec0a`; PR #902, `894-tiers` -> `dev-soft-core`)

Round 11, under #894's assignment (issuecomment-6878230332) as amended (issuecomment-6878532871). The measurement that opened it (issuecomment-6878200592) found `aecp-fanout`'s one-row REMOVE_AUDIO_MAPPINGS at 27,851 CPU cycles (295 us by the rule) and its ADD at 22,932 (245), against `record.aecp`'s 235 us at 1x1/1if.

Changed:
- **The attribution.** Commit-by-commit traces of each record at `9d7167bd`, `1b70cedd` and `7398ec0a` reproduce every span.
  - #904's one-pass check (`1b70cedd`) added 1,643 commits. `look`'s copy of each row and the REMOVE pass's copy of each kept row were each an 8 B call of `memcpy`, about 120 cycles. The edit also cleared 960 B of its table whatever its size.
  - The commits after it add 2,495 cycles at the same commit count: lines cached before that are cold at the later layouts.
  - At the head the REMOVE is 4,321 commits, 10,397 cycles of short stalls, 10,349 of instruction-fetch stalls (143 refills of 64 B) and 2,784 of data stalls.
  - The 17,932 the assignment names is `9d7167bd`'s figure; `8cc3e5d3`'s image is 19,008.
- **The cut** (`bc971054`, `aecp_maps.c`). The REMOVE is now 22,728 cycles (240 us by the rule; 2,863 commits, 148 refills), the ADD 20,595 (within 235) and the largest legal command 86,978 (915 us; 975 kept). The direct index, the 2 (n + R) bound and every refusal with its precedence stand, and the definition test passes unchanged.
  - A mapping is copied a coordinate at a time and a row's words are composed in registers.
  - The edit clears only the domain's slots, and each mapping's link, marks and occurrences at its turn.
  - A REMOVE looks up only the reach its FOUND pass holds.
  - The descriptor and page are echoed inline.
  - Two new tests: `Core.MapEditWorkReadsOnlyWhatItCleared`, in the work arm, where each edit starts from a stale table; and `Core.MapCommandsEchoTheirDescriptorAndPage`, an echo no test checked before.
  - Twelve new campaign rows, each caught by name. All 286 rows are caught at the head.
- **The edits as a class of their own** (`895f8906`, `dd788ed5`; amendment step 2, since the REMOVE is still 348 cycles over 22,380).
  - Of the k AECP records a row counts in w ms, `min(k, ceil((w + 1) / P))` are edits, at `EDIT_RECORD_US`: 260 us at 1x1/1if (a one-row output REMOVE in the answering-ports arm, 24,360 cycles; arm A's input REMOVE is 240) and 325 at 8x8/2if.
  - Every other AECP record is charged 235 and 265 us. LONG_ROWS are unchanged.
  - The planted control, an unpaced edit charged at the non-edit record, is refused by name.
- **Costs restated** from the final pass's measurements:
  - **A TICK at 50 us** (`0a474c6f`). AECP's sink sends an owed frame inside it: 4,617 cycles at `7398ec0a`, and 4,612 in another group under the cut.
  - **ACMP's owed frame at 55 us** (`6ec12ad7`): 4,890 cycles, moved from 4,723 by the cut's layout.
  - **`CTRL_LOOP_TX_MS` at 34 ms** (`6ec12ad7`), over the tx row's 33.01. Only a static assertion reads the figure.
  - **At 8x8/2if, from that point's legs** (`9606b3a9`; issuecomment-6881287231): a pass's events' fixed part at 35 us (2,859 cycles; 2,093 at round 9's head) and ACMP's owed frame at 70 (6,193; already 6,239 at round 9's head).
- **The gap** (`record_classes.py`). A final pass's AECP records are held by class: a paced edit to the edit class, every other record and an unpaced edit to `record.aecp`, and the long group to `LONG_RECORD_US`. A pass whose arm A at 1x1/1if missed a group is refused. Six planted controls run in the harness self-test.
- **What the final pass refused, and the fixes.**
  - `check_cpp_idiom.py` refused three multi-declarator lines at `9fda93a1`; each is now a line of its own (`3e0ca737`).
  - The flip check's planted TRANSMIT figure looked for its old words (`9106a980`).
  - `fw_coverage.py --check` found one unreachable arc of the reach's kept-row test, now named in the coverage exclusions with the reason (`2d579e89`).
  - None of these changes a compiled file. Every image is byte-identical across `9fda93a1`, `3e0ca737` and `6ec12ad7` (332 of 332 files; a one-constant control differs in 24).
- **The documents:** section 13 (the rows, a subsection *The one-row edit*), FR_NFR 3.4.1, and both READMEs.

Validation (clean clones, never piped):
- **The full arm A at 1x1/1if** (every group, on `bc971054`'s firmware, regraded with the head's graders on its own clone):
  - 96 groups, 0 refusals.
  - 7 misses, `backlog-owed`'s held-egress rows as before.
  - 0 of 139,557 passes over THE SHARE.
  - Joins 188.002 to 190.022 ms; every save within its stated worst case.
- **Round 9's legs at every other point, H-L1N, C-R1, and the answering-ports `aecp-fanout` at 1x1 and 8x8:** 8 exit 0. H-81L, H-81A, H-81N, H-J8 and H-J81 exit 1 on round 9's own STATED lines and error.
- **`record_classes.py` over every leg, at the head:** RESULT PASS.
- **Every stated table by the rule, at both points** (`load_grade`, `poll_grade.STATED_US`, `whole_grade` i.e. `ctrl_loop.h`'s pass costs, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`):
  - Within at 1x1/1if but for the two class lines, the edit and the largest legal notice, each held to its own record. The polls' base is 18,843 cycles, 200 by the rule against 205.
  - At 8x8/2if the two restated; #910's build of one remains, as before.
- **Lane gates:**
  - Part a (46) at `9fda93a1` and `6ec12ad7`, and the 33 that read the model or the text at `9106a980` and the head: rc 0 but the four that exit 1 by design, and the three gates fixed above.
  - Parts b and c: rc 0.
- **Workflows** (`verify_wf.py`, every step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` at `9fda93a1` and `6ec12ad7`): 139 steps ran and 226 are not run with a reason. 2 and 1 are bad, the idiom and coverage gates, both fixed.
  - firmware-unit at `2d579e89`: every step rc 0, `fw_coverage.py --check` PASS (39 files).
  - The AECP campaign: 286 of 286 rows caught.
  - The docs jobs at the head: 61 steps, every one rc 0.
- **The four-shard sweep** at `9fda93a1`, each on its own picked range: every shard's command rc 0.

Acceptance criteria:
- **Item 1** is met: the record split by function, pass and stall (`receipts/attribution`).
- **Item 2:** the ADD holds 235 us. The REMOVE does not (240 by the rule), so item 3 applies as amended.
- **Item 3:** the class split, with every CPU-decided row at 1x1/1if within its bound by every source:
  - R4 12.93 (20), R4L 188.41 (238), ACMP 28.64, ADP 27.01, MAAP 27.13 (30).
  - First queued notice 14.56 (20), R5 73.39, R6 69.24 (90), last queued notice 127.22 (130).
  - tx 33.01 and txL 48.23 (49).
  - The load 0.515 and 0.511 (0.70); every join interval 186.492 to 190.044 ms over every leg (181.0 to 239.0); the pace 8 ms; `tier_grid.py` choosing the built design (18 of 420 hold).
- **Item 4** is met: the TICK is attributed and restated.
- **Item 5** is met: the check refuses a pass missing any group of arm A. The final pass ran the full arm A (96 groups, 0 refusals, 0 of 139,557 passes over THE SHARE, the 7 held-egress misses of `backlog-owed` as before), round 9's legs at every other point and the answering-ports `aecp-fanout` at both. `record_classes.py` over all of it: RESULT PASS.
- **Item 6** is met.

Open risks/questions:
- **For the owner: the answering-ports arm's SET_CONFIGURATION.** It is 33,724 cycles at 1x1/1if (355 us by the rule) and 78,332 on the 8x8 shape (825 us), against `record.aecp`'s 235 and 265.
  - Arm A's fixture refuses the command, because its stream observation does not answer. The labelled arm, whose ports answer as the product's do, takes it.
  - The harness README says that arm is never the formal measurement, so no stated cost covers it. The pass check reports it and does not hold it.
  - Charged as an ordinary record it would put ACMP at 35.60 ms, ADP at 33.78, MAAP at 34.01, the last queued notice at 141.49 and txL at 57.06, each over its bound.
  - It predates this lane: 33,533 cycles at round 4's head `12180198`. It meets none of round 11's STOP conditions as written, so I publish it rather than choose an interpretation.
- **The REMOVE stays over 235.** What remains of it is instruction-fetch stalls, mostly in code every command shares. Each further change I measured moved every other record by its layout.
- 8x8/2if's rows are reported, not held, as before: R4 42.62 ms, the last queued notice 665.47 and txL 459.40, the load 0.794. 8x8-1if's legs and the 8x8 `srp` legs exit 1, on the same STATED lines as in round 9.
- **issuecomment-6881004362:** the firmware campaigns' shard-dispatch self-test leaves `?? dispatch-build/` in the job's checkout. I reproduce it at every head this round ran: `aecp_arms.key_arms`, from `58e6b60f`. It fails no step. It is not changed this round, to keep the delta to round 11's items.
