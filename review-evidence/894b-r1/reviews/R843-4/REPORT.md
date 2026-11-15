[R843] POSITIVE - exact head d539f162994fe671bb804d8e8c93088535bf65cd

Internal independent narrow-delta review R843-4 of issue #894 / PR #914 (lane 894b, 8x8/1if), round 7.

- **Head:** `d539f162994fe671bb804d8e8c93088535bf65cd`, tree `300e32073497b68c547deed82ae82ef7aa8e6efd`.
- **Delta reviewed:** `af2c4d7a..d539f162`, three commits (`d2fd8975`, `d0fea5f0`, `d539f162`). `af2c4d7a` is the head where R844-3 is POSITIVE.
- **Files changed:** `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md`, `tb/verilator/ctrl_service_budget/README.md` and `tb/verilator/ctrl_service_budget/record_classes.py`.
- **Not changed:** no firmware, RTL, build input or submodule gitlink. `git diff --raw` shows no `160000` entries.

**Result: POSITIVE.**
- All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR is open.
- Both R843-3 MINORs are resolved at their cause:
  - **F1:** section 13 now states 8x8/1if's gate as measured on the head's image.
  - **F2:** completeness is held at every point the pass runs any leg at.
- All residues from R843-3 and R844-3 are fixed with the reports' exact wording.
- This round records one new RESIDUE (FR_NFR history wording) and one SUGGESTION (the author's F1 check script).

This verdict is about the source head. It does not authorize a merge and it does not validate the current-dev candidate.

## Authority and scope

I reconstructed the task in this order:
1. AGENTS.md and CONTRIBUTING.md (lenses, verdict format, ledger rule).
2. Issue #894's rulings as cited in the changed text: the shape ruling, the round 2 ruling, the egress ruling, the round 3 ruling and the ledger ruling.
3. REQUIREMENTS / FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY.md section 13.
4. The delta and its history.
5. The author packet `review-evidence/894b-r1/author-r7` (archive `ef79ca12`) and REVIEW READY (issuecomment-6897705681), which names head `d539f162`.

I read prior public findings (R843-3, issuecomment-6895954911; R844-3, issuecomment-6895790018) only after my own pass over the diff.

Code outside the delta keeps its prior lens verdicts. The delta changes none of what that code depends on, because no image or grader input moved; see the evidence for byte identity under Conformance. The KNOWN items (#902 at `07ed787e`, `AECP_QUEUED_MS` keyed per shape at the #901 sync) are not findings.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R843-3-F1 (MINOR; Docs, Conformance): section 13 stated 8x8/1if's gate, load and every-source rows from round 3's image | **RESOLVED** | `SPLIT_CONTROL_MEMORY.md:2547-2595`. Every current figure matches its receipt, row by row and instance by instance (`receipts/section13-vs-receipts.txt`). Round 3's figures appear only as labelled history or in brackets. 0.673 is stated consistently, and 0.671 only as round 3's. FR_NFR 3.4.1 (`FR_NFR.md:393`) cites section 13's gate and states 0.711 and 0.673. |
| R843-3-F2 (MINOR; Tests, Robustness): a mixed-point pass skipped 1x1/1if's completeness | **RESOLVED** | `record_classes.py:190` now builds the completeness points from every COMPLETE point that has a leg, together with the map. At the head the R843-3 probe refuses the pass by name with both 1x1/1if findings; on `af2c4d7a`'s module it gives 0 findings (`receipts/mixed-probe-head-and-base.txt`). New planted control `record_classes.py:64`. Self-test: 14 of 14 at the head, 13 of 13 at the base. 8x8/1if-only passes still run (see Tests). |
| R843-3-R1 (RESIDUE): MAILBOX_SPLIT slice keyed by interface count | **RESOLVED**, exact fix plus a THE SHAPES link | `MAILBOX_SPLIT.md:390` |
| R843-3-R2 (RESIDUE): FR_NFR ledger ruling unlinked | **RESOLVED**, exact fix | `FR_NFR.md:394` links issuecomment-6892938049 as "#894's ledger ruling" |
| R843-3-S1 (SUGGESTION): 8x8/1if retained retry cost | Retained, optional | `poll_grade.py` is not in the delta |
| R843-3-S2 / R843-2-S2 (SUGGESTION): debug/wire arms at the tracked contract | Retained, optional | Not in the delta |
| R844-3-R1 (RESIDUE): `point_name` docstring "reported" | **RESOLVED**, exact fix | `record_classes.py:98` now reads "#894's 8x8/1if shape" |
| R844-3-R2 (RESIDUE): MAILBOX_SPLIT "at one interface" | **RESOLVED** | Same line as R843-3-R1 |
| R844-3-R3 (RESIDUE): round-3 load and rows unlabelled | **RESOLVED**, exact fix | `SPLIT_CONTROL_MEMORY.md:2547` reads "The round-3 load record, ..."; `:2595` reads "Round-3 reported rows, owed to #872"; `:2594` links the rows receipt at `d0318d2a`. That blob is `34a6136f`, the same as in `ef79ca12`. |
| R844-3-R4 (RESIDUE): PR body survey bullet reversed | **RESOLVED** | The current PR body reads "The survey over every leg finds every measurement within its statement by the rule." |

## New items at this head

### R843-4-R1: RESIDUE. Lens: Docs.

**Where:** `docs/reference/FR_NFR.md:393`, the words "as on each image before it (the image whose THE RETRY's round costs are its shape's, ..., among them), each holds: ... and the load 0.711 at the pin and 0.673 with tsn-c-stack#32".

**Problem:**
- Read literally, the list that follows, including the load 0.673, held "on each image before it".
- Section 13, which this clause cites, states otherwise:
  - round 3's image had load 0.671 (`SPLIT_CONTROL_MEMORY.md:2547`);
  - round 2's costs left the answering-every-port arm exiting 1 on 1,654 rounds (`:2568`).
- The head's own claim is correct, and so are the history figures in section 13. Only the attribution qualifier is too broad.

**Exact fix:** replace "as on each image before it (the image whose THE RETRY's round costs are its shape's, [#894's round 3 ruling](...), among them), each holds:" with "and as on round 3's image, the one whose THE RETRY's round costs are its shape's ([#894's round 3 ruling](...)), with its own load figures there, each holds:".

**Verification:** a wording-only diff. No figure, bound or verdict changes.

### R843-4-S1: SUGGESTION. Lenses: Tests, Docs.

**Where:** the author's `review-evidence/894b-r1/author-r7/scripts/f1_check.py`. This is packet tooling, not repository code.

**Problem:** the check tests each figure for substring presence somewhere in section 13 and somewhere in a receipt. A figure stated on the wrong row, or against the wrong instance, would still pass. I did the row-bound check by hand (`receipts/section13-vs-receipts.txt`) and found every row correct, so nothing at this head depends on the weakness.

**Optional:** in later packets, key each figure to its row name and instance.

## Lens results

```text
[R843] PASS Conformance — docs/design/SPLIT_CONTROL_MEMORY.md:2547-2595, docs/reference/FR_NFR.md:393-394 against gate-8x8-1if-regraded-af2c4d7a.txt, rows-8x8-1if-af2c4d7a.txt, survey-compare-ordinary-af2c4d7a.txt, control-transmit-aged-8x8-1if-a15345f7.txt and load_grade.py --check at d539f162 — section 13 states round 5's measurement as the head's gate
[R843] PASS RTL — git diff --raw af2c4d7a..d539f162 (5 paths, none under hdl/ or sw/, no gitlink) and img-d539f162-against-af2c4d7a.txt — no RTL or firmware change in the delta
[R843] PASS Robustness — tb/verilator/ctrl_service_budget/record_classes.py:181-212 — completeness refusals checked at mixed, reverse-mixed, single-point, uncomplete-point and empty passes
[R843] PASS Tests — record_classes.py:64 and :299-321 (new control), record_classes.py --selftest, run.py --self-test, four disposable mutants — the new control and the probes catch every mutant
[R843] PASS Docs — SPLIT_CONTROL_MEMORY.md:2547-2595, FR_NFR.md:393-394, MAILBOX_SPLIT.md:390, tb/verilator/ctrl_service_budget/README.md:217, record_classes.py:23-30,98,183-186 — prose matches code and receipts; R843-4-R1 residue only
```

**Conformance (CLEAN):**
- **Row-by-row check.** I checked section 13 (`:2547-2595`) row by row against the published receipts (`receipts/section13-vs-receipts.txt`).
  - Every worst row and its instance match the round-6 regrade of round 5's measurement: AECP 4.860, ACMP 7.231, ADP 6.014 and ENTITY_AVAILABLE 4.629, MAAP 6.255, SRP 10.474, MRPDU 4.114, the notices 2.168, the first and last queued notice 2.812 and 26.636, and R4L 2.547.
  - So do the gate totals: 114 groups and 1,717 instances, joins 352 in 113 groups from 187.397 to 190.147 ms, slices 142,809, 138,906 and 92,744, and 2,453,084 rounds with none over.
  - So do the rest: one SHARE pass at 202,546, the eleven every-source rows and 0.969, the heaviest SRP record 32,047 cycles (340 us, within 365), and transmit-aged 66.976 to 67.606 ms with 8 of 8 caught.
- **Load.** 0.711 and 0.673 match `load_grade.py --check` at the head (`receipts/gates/load_check.log`).
- **Byte identity carries the measurement.**
  - The delta touches no build input.
  - The author's chain `a15345f7 = 5aadbc8c = af2c4d7a = d539f162` is all-8-images identical (author-r6 and author-r7 image receipts).
  - `a15345f7` descends from `647d5c4a`, the merge of #902's `234bc149`, so "the image the tree that merges #902's `234bc149` builds" holds.
- **FR_NFR 3.4.1.**
  - Its bounds are unchanged.
  - It cites section 13's gate and states the head's figures.
  - The ledger ruling is linked by subject.
  - The history qualifier is R843-4-R1, a residue.

**RTL (CLEAN):**
- The delta has no HDL or firmware.
- All eight images are byte-identical to `af2c4d7a`'s (`img-d539f162-against-af2c4d7a.txt`).
- The submodule gitlinks are unchanged (`receipts/restore-check.txt`).
- R844-3's RTL coverage at `af2c4d7a` is an ancestor whose RTL scope nothing since has touched.

**Robustness (CLEAN):** my probe `scripts/completeness_probe.py` (`receipts/completeness-probe-d539f162.txt`) gives 9 of 9 cases as expected at the head:
- Three passes are accepted: 1x1/1if complete alone, as #902 held it; 8x8/1if complete alone, the lane's own requirement; and both points complete.
- These are refused by name:
  - the F2 mixed pass, with both 1x1/1if findings;
  - the reverse mixed pass (1x1/1if complete plus an 8x8/1if ports leg): "no arm A leg at 8x8/1if";
  - 8x8/1if complete plus an intact 1x1/1if ports leg;
  - an 8x8/1if ports leg alone.
- Passes with only uncomplete points (8x8/2if) and the empty pass are refused with the generic line.

On `af2c4d7a`'s module, 5 of 9 cases are as expected (`receipts/completeness-probe-af2c4d7a.txt`):
- Three mixed cases pass with 0 findings, which is the F2 defect.
- The ports-alone case is still refused there, but by the generic line rather than by name.

When `groups_of_arm` names a point with no legs, that point is still refused ("no arm A leg at X").

**Tests (CLEAN):**
- **Self-tests.** `record_classes.py --selftest` refuses 14 of 14 at the head and 13 of 13 at the base (`receipts/record-classes-selftest.txt`). `run.py --self-test` reports 0 failures and includes "PASS: the record classes refuse a mixed-point pass missing 1x1/1if's arm A and its arm B's SET_CONFIGURATION" (`receipts/gates/harness_selftest.log`).
- **Mutants.** Four disposable mutants, run in scratch copies only (`receipts/record-classes-mutants.txt`):
  - M1: points from the map only.
  - M2: points from arm A legs only.
  - M3: the named "no arm A leg" refusal dropped.
  - M4: the arm B check reading every point's ports legs at unmapped points.
- **Mutant results.** Each mutant makes the new control ESCAPE (selftest rc 1), and my probe fails on each. The new control can fail for the defect it claims to detect.
- **Real-data check.** The author's 8x8/1if-only receipt on round 5's measurement still passes (`author-r7/receipts/model/record-classes-8x8-1if-d539f162.txt`, RESULT: PASS).

**Docs (CLEAN, with R843-4-R1 residue):**
- **Prose matches code.**
  - The README (`:217`) and the module docstring (`:23-30`, `:183-186`) state the rule the code implements: any leg, arm A there, every group, arm B's accepted paths, and "no leg at either is refused".
  - The control list names the new control.
  - Section 13's added sentence at `:2591` matches.
- **Links and comments.**
  - The section 13 receipt link resolves to the identical blob.
  - `docs_check` reports 0 findings.
  - The comment rule holds: the added non-Markdown lines in `record_classes.py` carry only issue IDs (#894, #902), with no lane label, round, reviewer ID or comment ID. My scan matches nothing, and the author's comment scans and source-comment audit are empty.

## Gates for what changed

**My spot-checks at d539f162** (`receipts/gates/*.log`, each rc 0):
- `run.py --self-test`: 0 failures.
- `load_grade.py --selftest`: 28 of 28.
- `load_grade.py --check`: PASS, 8x8/1if 0.711 and 0.673.
- `shape_costs.py --check --selftest`: PASS.
- `flip_grade.py --check --point 8x8/1if`: PASS.
- `docs_check.py`: 0 findings.
- `check_py_idiom.py`: 0.
- `git diff --check af2c4d7a HEAD`: clean.

**The author's published receipts, verified by reading:**
- 45 lane gates, 0 bad (`lane-gates-r-d539f162.txt`), including the exits-1 gates exiting 1.
- The docs workflow: 61 steps run, 34 not run with a reason, 0 bad (`workflows-verify-docs-d539f162.md`).
- The harness self-test at the head differs from the base only by the new control line.

**Regrade:** I verified round 5's measurement regraded at `af2c4d7a` against its receipt. The head's graders differ from `af2c4d7a`'s only in `record_classes.py`, which the gate regrade does not read, so the regrade carries over. I did not rerun the regrade.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Section 13 `:2547-2595`; FR_NFR 3.4.1 `:393-394`; gate/rows/survey/transmit-aged receipts; `load_grade.py --check`; image-identity chain | R843-4 | d539f162994fe671bb804d8e8c93088535bf65cd |
| RTL | CLEAN | `git diff --raw af2c4d7a..d539f162` (no HDL/firmware/gitlink); all-8 image identity receipt; submodule status | R843-4 (delta); R844-3 at ancestor af2c4d7a for unchanged RTL scope | d539f162994fe671bb804d8e8c93088535bf65cd |
| Robustness | CLEAN | `record_classes.py:181-212`; completeness probe (9 cases) at head and base; R843-3 mixed probe | R843-4 | d539f162994fe671bb804d8e8c93088535bf65cd |
| Tests | CLEAN | `record_classes.py --selftest` 14/14; new control `:64,:299-321`; 4 mutants; `run.py --self-test`; author 8x8/1if-only receipt | R843-4 | d539f162994fe671bb804d8e8c93088535bf65cd |
| Docs | CLEAN (R843-4-R1 residue) | Section 13; FR_NFR 3.4.1; MAILBOX_SPLIT `:390`; harness README `:217`; `record_classes.py` docstrings; PR body; `docs_check` | R843-4 | d539f162994fe671bb804d8e8c93088535bf65cd |

## Limits

**What I did not run:**
- No Verilator, contract-rate or measurement leg. Round 5's measurement is carried by the published byte-identity receipts and the delta's scope; I did not rebuild any image.
- The author's lane gates that read private build directories (`record_classes_8x8_1if`); I verified them by their published receipt only.
- No parent/PP/gPTP/Yosys/builder bank, Docker or act.
- Physical calibration is NOT RUN, and field skips are not hardware proof.

**Hosted checks:** no hosted check context was visible on the PR at this head when I looked. I make no claim about hosted or act results.

**Clone state:** probes ran in place (in-process imports) or in scratch copies. After the probes, the clone is at the exact head: worktree and index clean, and the index matches the tree in mode and blob (`receipts/restore-check.txt`). I removed the `__pycache__` directories that the probe imports created.

## Pending manager duties

- Carry R843-4-R1 (and any still-open residue) to the residue checklist. R843-3-S1 and S2 remain optional.
- Validate the current-dev merge candidate (source base `7398ec0a`, live dev `6b66f66d`) with the builder and native banks at the merge turn, and link the receipts.
- Hosted and act acceptance of the exact head after it is marked ready.
- Maintainer authorization for any merge.

R843-4 FINISHED
