[R843] NEGATIVE - exact head af2c4d7a4a1930aba712792a7facd8e9cb88e7c7

# R843-3: internal independent delta review of PR #914 (issue #894, also #872), rounds 5 and 6

- **Head:** `af2c4d7a4a1930aba712792a7facd8e9cb88e7c7`, tree `63cae1575a884c869dd92698c8d4a9bb685f6aba`, on a detached clean clone. Source base `7398ec0a` is an ancestor.
- **Delta:** round 4's `98c0b62b` (R843-2 and R844-2 both POSITIVE) to `af2c4d7a`. That is two merges of #902 (`647d5c4a` = 234bc149, `5aadbc8c` = 4ae887a1) and nine lane commits (`b2737ba5` through `af2c4d7a`).
- **Authority:**
  - the round-5 assignment (sync onto #902's 234bc149, re-measure 8x8/1if);
  - #894's round-6 ruling, issuecomment-6892938049, items 1 to 6;
  - the owner's direction of 2026-11-15 (#665 issuecomment-6892332745);
  - REVIEW READY, #894 issuecomment-6895387328.
- **Evidence:** archive `d0318d2a`, review-evidence/894b-r1, author-r5 and author-r6. I fetched it by exact commit and verified it (`receipts/packet-verify.txt`).
- **Result: NEGATIVE, with two MINOR findings.**
  - **F1** (Docs, Conformance): section 13 still states 8x8/1if's gate, load and every-source rows from round 3's superseded image.
  - **F2** (Tests, Robustness): the lane's change to `record_classes.py` lets a mixed-point pass skip 1x1/1if's completeness guard.
  - Everything the round-6 ruling asked for in the tree is otherwise met and checked: the sync keying, the drain limit, the ledger by rule with its controls, the own ADP record with its controls, R843-2-S1, the image carry and the final pass.
  - There are also two RESIDUE items and two SUGGESTIONs.

## Context reconstructed

I read, in this order:
1. AGENTS.md;
2. the ruling and REVIEW READY comments;
3. the round-5 STOP (the packet's `STOP-COMMENT.md`, which matches issuecomment-6892905117);
4. `git log` and `git show --cc` for both merges;
5. the lane's own diffs `647d5c4a..0700f09e` and `5aadbc8c..af2c4d7a`;
6. the affected harness modules at the head: `egress_ledger.py`, `load_grade.py`, `record_classes.py`, `edit_rows.py`, `poll_grade.py`, `rows_tiers.py` and `ctrl_loop.h`;
7. section 13 and FR_NFR 3.4.1 at the head;
8. the author receipts, by section.

I read the round-4 reviews' findings only after this pass.

## Findings

### F1: MINOR. Lenses: Docs, Conformance.

**Where:**
- `docs/design/SPLIT_CONTROL_MEMORY.md:2547` (the load bullet);
- `:2550-2568` (the "gate at 8x8/1if" paragraph, its table, and the load, joins, slices and rounds bullets);
- `:2594-2595` (the every-source rows reported to #872, and the load with every AECP command the largest legal one).

**Evidence:** `receipts/doc-vs-receipts.txt` sets each line beside the author's own receipts of the head's image.
- **Why the old figures no longer apply.** The 8x8/1if image moved in round 5: `b2737ba5` raised `CTRL_LOOP_SRP_UNIT_US` to 365, and the 234bc149 merge brought #902's code. The author-r6 image receipts show 8x8/1if "moved from the start". Round 5 measured that image at `a15345f7`, and the head carries it byte-identical.
- **What section 13 still says.**
  - It describes the gate as "Measured once more on round 3's image ... (`d8629751`)". Its worst rows are AECP 4.693, the last queued notice 26.195, joins 186.687-190.705 ms and 2,455,411 rounds.
  - At :2547 and :2565 it gives the load as "0.711 at the pin and 0.671 with tsn-c-stack#32". The ADP bullet just above (:2546) says 0.673, and so does the head's `load_grade.py --check` (`receipts/load-grade-check.txt`).
  - The every-source rows at :2594 are round 3's: R5 113.95, the last 274.91, txL 147.06, and "its record 154,850 cycles, 1,630 us". The load at :2595 is 0.993.
- **What the head's own receipts say.**
  - `author-r6/receipts/model/rows-8x8-1if-af2c4d7a.txt`: R4 19.82, R5 126.36, R6 118.28, first 17.83, last 325.90, R4L 192.81, ACMP 48.37, ADP 48.33, MAAP 49.03, tx 67.24 and txL 134.96 ms, derived at `record.aecp.long` 1,510 us. The load with every command the largest is 0.969.
  - Two paragraphs above (:2591), section 13 itself states the largest command's record as 143,648 cycles, 1,510 us.
- **Where round 5's measurement does appear.** Its figures (114 groups, 1,717 instances, AECP 4.860, ACMP 7.231, ADP 6.014, MAAP 6.255, SRP 10.474, MRPDU 4.114, the first 2.812, the last 26.636, the largest command 2.547, joins 187.397-190.147, 2,453,084 rounds) are in the PR body and REVIEW READY only. The authoritative document records only the ledger rows and the restated items.
- **Why this is not RESIDUE.** These are stated measurements and derived figures in the document FR_NFR 3.4.1 cites for 8x8/1if's flip. The ruling's item 1 has the every-source rows reported, and its item 4 has the load recomputed. Fixing it changes figures.

**Impact:**
- A cold reader of the authoritative document gets the flip gate's evidence from an image the head no longer builds.
- They also get two contradictory loads for the trigger.
- They get every-source rows for #872 that understate R5, R6, the last queued notice, ACMP, ADP, MAAP and tx by 4 to 51 ms (for example the last queued notice is 274.91 against 325.90).

**Required outcome:** section 13 states 8x8/1if's gate as measured on the head's image:
- the round-5 measurement of `a15345f7`, carried by byte identity, with round 3's kept as history where useful;
- the load as 0.711 and 0.673 everywhere it is stated;
- the every-source rows, and the load with every command the largest, as the head derives them, with the largest command's record at 1,510 us.

**Verification:** every figure on those lines equals `rows-8x8-1if-af2c4d7a.txt`, `gate-8x8-1if-regraded-af2c4d7a.txt` and `load_grade.py --check` at the corrected head, and no line in section 13 states 0.671 or 154,850 as current.

### F2: MINOR. Lenses: Tests, Robustness.

**Where:**
- `tb/verilator/ctrl_service_budget/record_classes.py:26`, `:185`, `:334` and `:338`;
- `tb/verilator/ctrl_service_budget/README.md:217` (the contract sentence "At each point it is held at ... where it runs arm A").

**Evidence:**
- **The change.** #902's `record_classes.py`, as merged at `647d5c4a`, always required 1x1/1if's arm A and 1x1/1if's answering-ports SET_CONFIGURATION and SET_STREAM_INFO. The lane's `1a0fedad` made completeness apply only at a COMPLETE point "where it runs arm A". `main()` puts a point in the completeness map only when an arm A leg exists there.
- **The probe.** `scripts/record_classes_mixed_probe.py` (`receipts/record-classes-mixed-probe.txt`) builds a pass from:
  - 8x8/1if's complete synthetic legs;
  - plus 1x1/1if's answering-ports leg alone, with its accepted SET_CONFIGURATION removed and no 1x1/1if arm A.
- **The result.**
  - At the head that pass has 0 findings, so it passes.
  - The same 1x1/1if legs beside an 8x8/1if arm A leg, graded by `647d5c4a`'s module, are refused twice: "the pass runs no arm A leg at 1x1/1if" and "missing arm B's SET_CONFIGURATION" (`receipts/record-classes-mixed-probe-647d5c4a.txt`).
  - No planted control covers a mixed-point pass. The two new controls are 8x8/1if-only.

**Impact:**
- This is the guard #902 added after "the one-row map edit's record grew past `record.aecp` unseen in `aecp-fanout`".
- A final pass that carries 1x1/1if legs but is missing 1x1/1if's arm A or its arm-B accepted paths now passes whenever 8x8/1if's legs are complete. 1x1/1if's held records are then reported as passing over an incomplete arm.
- The change was needed to let an 8x8/1if-only pass run, but it also loosened 1x1/1if without a stated reason.

**Required outcome:**
- completeness is held at every COMPLETE point the pass has any leg at, not only where arm A runs, so a point with legs but no arm A is refused by name;
- an 8x8/1if-only pass still runs;
- a planted control holds the mixed-point case.

**Verification:** the probe above gives at least the two 1x1/1if findings, `record_classes.py --selftest` refuses the new control, and the 8x8/1if receipt (`record-classes-8x8-1if-a15345f7.txt`) still passes.

### R1: RESIDUE. Lens: Docs.

**Where:** `docs/design/MAILBOX_SPLIT.md:390`, a line #902's merge changed in this delta.

**Problem:** it reads "`CTRL_LOOP_SLICE_US`: the slice rule's choice at one interface, 0.95 ms, and 1.3 ms at two". In this tree 8x8/1if is one interface at 1.475 ms (THE SHAPES), so this keys the slice on the interface count. The authoritative statements are correct: `ctrl_loop.h:327/334` and section 13's table.

**Exact fix:** "`CTRL_LOOP_SLICE_US`, stated for each shape (THE SHAPES): the slice rule's choice at 1x1/1if, 0.95 ms, 1.475 ms at 8x8/1if, and 1.3 ms at two interfaces".

### R2: RESIDUE. Lens: Docs.

**Where:** `docs/reference/FR_NFR.md:394`, in the ledger sentence the lane added.

**Problem:** "(#894's round-6 ruling, item 2)" is the only ruling citation in that paragraph without a link.

**Exact fix:** "([#894's ledger ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), item 2)". That also matches section 13's naming at :2515.

### S1: SUGGESTION. Lenses: Docs, Robustness.

**Where:** `poll_grade.py:106` and section 13 :2544.

**Evidence:**
- `poll_grade.py:71-72`'s rule says a retained record's retry is "stated at the SRP record's cost". 1x1/1if follows its unit (280).
- 8x8/1if keeps `retained=345`, its measured record, while its unit is now 365.
- Section 13 says so ("the measured record stays the retained retry's cost"). That is stricter for the harness's apply check and 0.0x lighter in the load, and the survey shows it held (316.40 us measured, 335 by the rule).

**Optional:** state in `poll_grade.py`'s rule comment that 8x8/1if's retained cost is its measured record rather than the unit, and why. Or move it to 365 with the load recomputed.

### S2: SUGGESTION (R843-2-S2, retained). Lenses: RTL, Robustness.

The debug arm and the wire comparison still compile the core at the tracked one-interface contract at two interfaces. The delta does not touch them, and the author gives a reason for not taking it. Nothing more to do.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R843-2-S1 (SUGGESTION): results-directory mode cannot see a refused group | **RESOLVED** (`25c782a4`) | `egress_ledger.py:143` `run_refusals`, read at `:159`; two controls and a mutant. My probe P5 (refusals read under another key) fails the self-test (`receipts/ledger-probes.txt`). |
| R843-2-S2 (SUGGESTION) | Retained, optional | S2 above |
| R843-2-S3 (SUGGESTION): packet INDEX mismatches | **RESOLVED** for rounds 5 and 6 | Every mismatch is a path-redacted file whose MANIFEST.json `original_sha256` is the indexed one (`receipts/packet-verify.txt`). |
| R843-2-RES1: history wording at `egress_ledger.py:42`, `:318` | **RESOLVED** (`a15345f7`) | That comment has since been replaced by the derivation's, and the mutant's name is fixed. |
| R843-2-RES2, RES3; R844-2-R2: PR and packet prose | **RESOLVED** | PR body rows 48 and 49 (the live body equals the packet's but for a trailing newline). |
| R844-2-R1: `aecp.h` guard sentence | **RESOLVED** (`a15345f7`) | `aecp.h:63-64` reads "Most units include this header before the table and charge nothing". |

## The focus checks

1. **The sync merges.** **Met.**
   - In `ctrl_loop.h`, THE SHAPES block (1, 2, 2) at :326-332 carries #902's 950/735/280, and (1, 9, 9) at :333-339 keeps 1,475/1,795/1,475/365/165/25.
   - No 8x8/1if figure is keyed on the interface count. `CTRL_LOOP_TX_MS` and `CTRL_LOOP_STEP_PASS_US` stay `MBX_N_IF`-keyed. The first is a static assertion only, and the second is held by the survey (850 of 975 us).
   - The merge resolutions in `load_grade.py` (`srp_unit` via `shape_costs.at`, `unit_planted`), `poll_grade.py`, `rows_tiers.py`, `selftest_round.py` and the harness README key by shape.
   - The drain limit is 365 at 8x8/1if (`b2737ba5`), held by `load_grade.srp_unit` at :291, with a planted control at the measured 345.
   - `shape_costs.py --check` and `--selftest` (24 of 24) pass at the head.
2. **The ledger restatement.** **Met in the tool.**
   - The figures `figure`/`LEDGER` derive at :71-80 are all correct by the rule. I recomputed each by hand: 63.40, 63.64, 63.93, 64.16, 64.41, 62.30 and 61.94.
   - The hold is read from `scenario.py:844` once.
   - The self-test (`receipts/egress-ledger-selftest.txt`) passes 13 of 13 mutants.
   - My five probes each fail it (`receipts/ledger-probes.txt`): rounding to the nearest 0.01, 4 %, a hold of 61, a section-13 measurement digit, and the refusals key.
   - Section 13 :2572-2583 shows both measurements and the attribution.
   - The bare-merge proof is in `author-r5/receipts/harness/attribution-backlog-owed-647d5c4a.txt`: all seven rows identical to the microsecond.
3. **8x8/1if's own ADP record.** **Met in the tool.**
   - `load_grade.OWN`/`OWN_MEASURED` at :125-126: 12,210 cycles is 130 us by the rule.
   - `--check` passes, and `--selftest` passes 28 of 28.
   - My in-process probes (`receipts/own-adp-probe.txt`): a dearer measurement (12,500 cycles, 135 us) is refused, and the own statement unmerged is refused at 125.
   - The load is 0.711 and 0.673 (`receipts/load-grade-check.txt`).
   - 8x8/1if's own statements, by the rule from their cycles:
     - paced 635 (60,027) and one-row 320 (30,277) at `edit_rows.py:41`;
     - long 1,510 (143,648) at `rows_tiers.py:134`;
     - walk 55 (4,905) and notice 145 (13,572) at `poll_grade.py:106`.
   - `author-r5/receipts/model/record-classes-8x8-1if-a15345f7.txt` holds them on the measured legs.
   - The document's load and rows lag behind: see F1.
4. **R843-2-S1.** Resolved; see the table.
5. **The carry.**
   - The author-r6 image receipts: all eight images at `af2c4d7a` are byte-identical to `5aadbc8c`'s, and those are identical to round 5's measured `a15345f7`.
   - The six fixed images are identical to #902's `4ae887a1`.
   - The only firmware change after `a15345f7` is `CTRL_LOOP_TX_MS` 98→99 at two interfaces (I checked `git diff a15345f7 af2c4d7a -- sw`), which only a static assertion reads.
   - The regrade at the head's graders: 114 groups, 1,717 measured, joins 187.397-190.147, rounds within their statements, the held-egress rows 0.094-0.219 ms under, and the transmit-aged control caught 8 of 8.
6. **The full pass.** I spot-verified the author's receipts. They are the author's evidence, not a manager bank.
   - lane gates 65 of 65 with clean clones;
   - 139 local hosted-step replicas run, 226 not run with a reason;
   - firmware campaigns 716/302/345 caught, 0 escaped, boundary and firmware-verilator PASS;
   - the sweep's four shards: 15+17+17+16 = 65 suites and 361,003 + 2,046,229 + 284,233 + 21,575 = 2,713,040 checks, 0 failures, 0 SKIPPED;
   - plat_ledger 7 of 7 controls, and 8x8-if1 56 RAMB36 within its 56 budget.

**Comment rule:** I scanned the delta's added source lines (`*.py`, `*.c`, `*.h`, `*.cpp`, `*.sh`) for review rounds, lane or bench labels, reviewer IDs and issue-comment IDs. None is found.

## Lens results (artifact evidence)

| Lens | Result | Artifact | What was checked, against what |
|---|---|---|---|
| Conformance | **UNCLEAN** (F1) | `ctrl_loop.h:326-339`, `egress_ledger.py:55-80`, `load_grade.py:117-126,291,319-345`, section 13 :2546-2595, FR_NFR 3.4.1 :393-396 | Ruling items 1 to 4 and 6 and the round-5 keying, against the tool and the receipts. The tool meets each item, but the document's measured and derived 8x8/1if figures are round 3's (F1). |
| RTL | **CLEAN** | `sw/firmware/ctrl/loop/ctrl_loop.h:298-339,405-448`, `git show --cc 647d5c4a 5aadbc8c` for `ctrl_loop.h`, `git diff a15345f7 af2c4d7a -- sw` | THE SHAPES blocks and `#error`, `CTRL_LOOP_BUILD_MOST` 1 at 8x8/1if (1,475 < 1,795), and the 365 us unit's effect on the slice (SRP slices 142,809 of 147,500 measured). The static assertion on `CTRL_LOOP_TX_MS`. The firmware delta after the measured image is a constant only an assertion reads. No HDL is in the delta. |
| Robustness | **UNCLEAN** (F2) | `record_classes.py:26,65,185,334,338`, `egress_ledger.py:143-151`, `load_grade.py:327-345` | Refusals, a missing `results.json`, a dearer measurement and an unmerged own statement are each refused. A mixed-point pass escapes 1x1/1if's completeness (F2, probe). |
| Tests | **UNCLEAN** (F2) | `egress_ledger.py --selftest` (13/13), `load_grade.py --selftest` (28/28), `record_classes.py --selftest` (13/13), `shape_costs.py --selftest` (24/24); my probes P1-P8 and the mixed-point probe | Each new control can fail. My five ledger probes and two ADP probes are caught. No control covers the mixed-point completeness case, and that case passes (F2). |
| Docs | **UNCLEAN** (F1; R1, R2 residue) | `docs/design/SPLIT_CONTROL_MEMORY.md:2515,2546-2595`, `docs/reference/FR_NFR.md:393-396`, `docs/design/MAILBOX_SPLIT.md:390`, `tb/verilator/ctrl_service_budget/README.md:156-166,217` | The ledger, attribution, ADP and drain-limit text is current. The gate, load and every-source figures are stale (F1). |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | ruling 6892938049; `ctrl_loop.h`; `egress_ledger.py`; `load_grade.py`; section 13; FR_NFR 3.4.1; author-r5/r6 receipts | R843-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| RTL | CLEAN | `ctrl_loop.h` THE SHAPES and both merge resolutions; the firmware diff after `a15345f7`; image receipts | R843-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Robustness | UNCLEAN (F2) | `record_classes.py`; `egress_ledger.py`; `load_grade.py`; probes | R843-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Tests | UNCLEAN (F2) | the four self-tests at the head; probes P1-P8 and the mixed-point probes | R843-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |
| Docs | UNCLEAN (F1) | section 13; FR_NFR 3.4.1; MAILBOX_SPLIT.md; the harness README; PR body | R843-3 | af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 |

Code outside the delta keeps its round-4 lens verdicts (R843-2 at `98c0b62b`) unless the delta changes what it depends on.

## Real limits

- **No source bank.** I ran no manager bank, no Verilator, no image build and no harness measurement. Source-head execution evidence is the author's published receipts, which I spot-checked rather than re-ran.
- **What I did run** at the head: the four self-tests, `load_grade.py --check`, `shape_costs.py --check`, and disposable probes on a copy or in process.
- **Hosted runs.** The API lists no hosted check run or status for the exact head: 0 check runs, combined status pending with 0 contexts, 0 workflow runs. The author's 139 "hosted steps" are local replicas. I make no claim about hosted acceptance.
- **The mixed-point probe** uses the module's synthetic legs, not measured results.
- **Not exercised here:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone state.** It is restored: worktree and index equal HEAD, no status lines, and the six gitlinks unchanged (`receipts/clone-state.txt`). I removed this review's bytecode caches.

## Pending manager duties

- Carry F1 and F2 to the author. Re-review the corrected head on Conformance, Docs, Tests and Robustness, plus RTL if the fix touches firmware.
- Carry R1 and R2 to the residue checklist.
- Hosted and act acceptance at the exact head, which the manager owns.
- Build and validate the current-dev merge candidate at the merge turn (source base `7398ec0a`, live dev `6b66f66d`), and link its receipts.
- The next sync onto #902 (41ca9f87 or later, and #901): keep `AECP_QUEUED_MS` 130 at 8x8/1if by shape, and keep THE SHAPES' 8x8/1if block.

## Receipts and scripts (MANIFEST.sha256)

- **Scripts:**
  - `scripts/ledger_probes.sh`
  - `scripts/own_adp_probe.py`
  - `scripts/record_classes_mixed_probe.py`
  - `scripts/record_classes_mixed_probe_base.py`
  - `scripts/packet_verify.py`
  - `scripts/doc_vs_receipts.sh`
- **Receipts:**
  - `receipts/egress-ledger-selftest.txt`
  - `receipts/ledger-probes.txt`
  - `receipts/load-grade-check.txt`
  - `receipts/load-grade-selftest.txt`
  - `receipts/own-adp-probe.txt`
  - `receipts/record-classes-selftest.txt`
  - `receipts/record-classes-mixed-probe.txt`
  - `receipts/record-classes-mixed-probe-647d5c4a.txt`
  - `receipts/shape-costs-check.txt`
  - `receipts/shape-costs-selftest.txt`
  - `receipts/packet-verify.txt`
  - `receipts/doc-vs-receipts.txt`
  - `receipts/clone-state.txt`

R843-3 FINISHED
