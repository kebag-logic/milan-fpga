[A781] REVIEW READY
Commit: 184d47cacc0b4eccb923cfbd4f2df9c3a05f5638 (`894-8x8-1if`, round 2 phase B; nothing pushed, the PR is opened on `dev-soft-core` after #902 merges)

Round 2 under #894's ruling issuecomment-6871343905, with #902's bounds (issuecomment-6867990126) and round 9's direct-index table (issuecomment-6870437042) merged in from `894-tiers`.

Changed:
- **The sync merges.**
  - `219ea7ed` merges #902's `5b264bf2`, with five conflicts resolved:
    - `mrpdu_grade.py`: THE TRANSMIT's bound read once, `BUDGET_MS = LATE_MS`, 49 ms;
    - `ctrl_configs.py`: both sides' boundary entries;
    - FR_NFR 3.4.1's SRP/MRP row: #902's figures with the harness-budget sentence;
    - the AECP and SRP READMEs.
  - `184d47ca` merges `7398ec0a`, which `894-tiers` moved to during the round, with no conflict.
- **The shape header is the single source of the direct-index table's key domain** (`6122db33`, item (c)).
  - `srp_entity.py` states `AECP_ENTITY_KEY_*` from `aecp_shape.key_domain` over the builder's AEM image.
  - `aecp_entity_gen.h` states them only under `#ifndef CTRL_SRP_ENTITY_H`, for the host arms.
  - `shape_costs.py` holds this, with three plants.
  - A firmware plant that widens the shape header's key streams changes all eight images.
- **8x8/1if's polls restated from the measurement plus 5 %** (`7e3daf54`): the base 235 us (was 240), the walk 50 (55), a long notice 320 (315); the rest unchanged. `CTRL_LOOP_SRP_UNIT_US` stays 345 us, from the heaviest record, 32,421 cycles, so no image moves.
- **The docs** (`105e3aa9`): FR_NFR 3.4.1 (the bounds 49, 238 and 181.0 to 239.0 ms; the record and the polls as measured), section 13 (the gate, the ledger, the finding below, the rows reported), and the READMEs.

Measured once at 8x8/1if (head `6122db33`, the built image at 1,475 us):
- **The run.** Every group of arm A, the `answering-every-port` arm and the `answering-ports` arm's `aecp-largest-notice`: 112 groups, 1,680 instances.
- **The image.** Both 8x8/1if images at `184d47ca` are byte-identical to the measured head's.
- **The worst rows:**

| Row (bound, ms) | Worst, ms |
|---|---:|
| AECP (20) | 4.693 |
| ACMP, ADP, MAAP (30) | 6.813, 5.522, 6.020 |
| SRP (90) | 10.284 |
| MRPDU (49) | 3.578 |
| The first queued notice (20) | 2.259 |
| The last queued notice (130), of 40 | 23.730 |
| The largest legal command, the paced R4L row (238) | 2.442 |

- **Budget misses.** The only ones are `backlog-owed`'s seven held-egress rows, 61.680 to 63.969 ms, each under its recorded figure. They are recorded misses in 1x1/1if's form, and none is new.
- **Joins and run-outs.** 346 joins, 186.687 to 190.705 ms, within 181.0 to 239.0. Of the 2,311 run-outs, none was late, absent or unresolved.
- **Slices.** Each is within the stated 147,500 cycles: SRP's 146,052, the build's 137,924 and THE RETRY's 109,745.
- **The load.** 0.709 at the pin and 0.670 with tsn-c-stack#32, within 0.75.
- **The image cap.** The platform image is 56.0 RAMB36.
- **The aged build's control.** `transmit-aged` is caught: 8 of 8 groups' timer-driven MRPDU are over the derived 49 ms.

Validation (the full pass at `184d47ca`, each part on its own clean clone, never piped; two host resets cut it, so parts ran again, as the open risks say):
- **The sweep, 4 shards** (`native-shards.py`, each on its own clone and CPU range): exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures.
- **Every hosted job step** of rtl-fast, rtl, elaborate and docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`): 139 run, 226 not run with a reason, 0 bad.
- **The firmware jobs:** every step 0. The control, AECP and SRP campaigns caught 716, 275 and 345, with 0 escaped; `notice-dropped-with-its-descriptors-next` and `map-table-each-direction-alone` are among them. The boundary gate PASS; coverage PASS on 39 files.
- **The lane gates:** 49 at 0. The four that exit 1 by design are `rows_tiers --terms`, `flip --check`, `--point 1x1/1if --design as-built` and `--point 8x8/2if`, all reported rows. They include:
  - the harness self-test: 0 failures, 872 checks, 257 mutants caught, 0 escaped;
  - rows_tiers 971/971, flip 578/578 and load 25/25; `load_grade.py --check` 0.513 and 0.509; `tier_grid.py --point 1x1/1if` exit 0; the table of shapes 21/21;
  - the flip check at 8x8/1if PASS (0.709) and at 1x1/1if PASS;
  - the diff checks against 13 bases (`5b264bf2`, `dd01b0af` and `bc8acc76` among them);
  - em-dash, the idioms, docs and `ctrl_hot`;
  - BDD, the twin and its plants, the builder tests, NVM, and boot 1x1, 8x8, native and plants.
- **The harness legs at 1x1 and 8x8/2if** (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`) exit 0, but `srp` at 8x8/2if exits 1 on #910's build of one, as #902 reports (138,054 and 147,814 against 121,500).
  - The plant control C-R1 is caught.
  - 48 joins in 11 group runs, 185.485 to 190.040 ms; of 172 run-outs, none was late, absent or unresolved.
- **Every image:** each 1x1 and 8x8/2if image is byte-identical to `7398ec0a`'s, whose six equal `5b264bf2`'s. 8x8/1if is within 56.0.
- **Before the pass:**
  - the harness self-test at `6122db33`: 0 failures, 257 mutants caught, 0 escaped;
  - the table of shapes: 21 of 21 controls refused;
  - the quick model and style gates at `184d47ca`: as expected.

Acceptance criteria (the round 2 ruling):
- (i) met: the MRPDU row is held to `CTRL_LOOP_TX_BOUND_MS`, 49 ms, with its plant.
- (ii) met: 345 us at 8x8/1if from its measurement, and the 1x1 and 8x8/2if images are unchanged.
- (iii) met: the polls are restated from the measurement and the load recomputed.
- (iv) met: 40 notices are derived from the descriptors and sized by shape, with plants that prove none dropped. The queued-notice and R4L arms are measured: first 2.259, last 23.730 and R4L 2.442 ms.
- (v): the full pass above.
- (a): the egress rows are recorded misses.
- (c): the merges, and the shape header as the single source.
- No STOP trigger fired.

Open risks/questions:
- **THE RETRY's cold cost at 8x8/1if is stated below its measurement. This is left for a decision.**
  - **What fails.** The `answering-every-port` arm exits 1 on 1,654 STATED lines. Every one is a round with no notice beside 1, 2 or 4 refused attempts: up to 12,547, 19,326 and 23,343 cycles, against 11,900, 15,300 and 22,100.
  - **Why.** `AECP_ROUND_COLD_US` and `AECP_ATTEMPT_US` are keyed on `MBX_N_IF`, so 8x8/1if takes the 1x1's 85 us cold cost. It measures about 125 us. The 8x8 shape's two-interface 185 us holds every round.
  - **What it does not affect.** No row misses and no slice runs past its length.
  - **Why it is not fixed here.** Keying the cold cost on the shape would change the 8x8/1if image and its rounds. That is outside the ruling's items, so it needs a ruling and a new measurement.
- **1x1/1if's SRP record** measured 26,086 cycles in round 1, over its 250 us. Its slices hold and its image is byte-identical; this stays left for a decision.
- **Reported, not held (#872):** 8x8/1if's rows by every source, derived with 40 notices and its own polls. R5, R6, the last queued notice, ACMP, ADP, MAAP, tx and txL are over their bounds there, as before; the every-command-largest load is 0.991. Figures are in section 13.
- **#902 is still OPEN at `7398ec0a`.** issuecomment-6876349104 asks #902's lane to check 1x1/1if's AECP record before it merges. A #902 round 11 would reach this branch through the manager's merge of `dev-soft-core` after #902 merges.
- **The pass ran three times because the host was reset twice** (a RAM fault, about 11:2x and 12:2x CET). Nothing from a cut attempt is counted, except three jobs that had finished whole, each on its own clean clone at this head: firmware-verilator and the AECP and SRP campaigns. Everything else ran again from fresh clones.
- **Environment, not code:**
  - docs-gates-1's builder leg first failed because the local runner's sandbox HOME lacked the RV32 SDK that the hosted job provisions at `~/br-milan-rv32`. With that link added, the job ran again whole and failed 0.
  - docs-check-no-git strips `.git` by design. Its steps are all rc 0, and only the local driver's post-run `git status` fails, as in #902's pass.
