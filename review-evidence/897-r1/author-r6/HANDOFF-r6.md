# HANDOFF round 6: lane 897 (A776), R833-5's two MINORs and five residues

Status: **REVIEW READY** (2026-11-15, started 15:15 CET), posted once on #897, issuecomment-6896663632 (`REVIEW-READY-COMMENT.md`).
Assignment: the manager's round 6, on R833-5 (NEGATIVE at `eca1b9ca` on F1 and F2, both MINOR; the report and its receipts are on `897-review-evidence`, `review-evidence/897-r1/reviews/R833-5/`).
Base: round 5's head `eca1b9ca`, on #902's round-13 head `234bc149`. Nothing is pushed; the manager pushes.

## 1. F1: the GET_AS_PATH guard holds the answered read

R833-5: `record_classes.py:196-198` held a GET_AS_PATH answered SUCCESS. The port that answered before `arm_path.py` also answered SUCCESS, with an empty sequence, so the reviewer's probe passed with that stub in `build.py` (`probe_stub_path.sh`: `run.py --self-test` 0 failures, `record_classes.py --selftest` 13 of 13).

The change (`record_classes.py`, `selftest_mutants.py`, the harness README, section 13):
- **The guard reads the response.** `Record` carries the response's control_data_length. `read_leg` reads it from the frame it already parses: `(fr[16] << 8 | fr[17]) & 0x7FF`.
- **What a pass must hold.** `ANSWERED_LENGTH = 16 + 8 * arm_path.ENTRIES`, 80. It is the controller_entity_id, sequence_id, command_type, descriptor_index and count (16 B), and 8 B an entry (IEEE 1722.1-2021 7.4.41.2).
  - A pass is refused unless its answering-ports leg at 1x1/1if answered a GET_AS_PATH SUCCESS at that length.
  - Every GET_AS_PATH the answering-ports arm answers SUCCESS at another length is refused by name ("a GET_AS_PATH answered SUCCESS with control_data_length N, not the 80 of the 8 entries the arm's path port reads and answers").
- **The planted control.** "a GET_AS_PATH answered SUCCESS with no entries" (control_data_length 16) is refused by those words. `record_classes.py --selftest` refuses 14 of 14.
- **The port pinned.** `port_findings()` checks three things:
  - `build.VARIANTS['answering-ports']` defines `arm_path.B_PATH`;
  - that arm puts `b_path` in the face's `path` port;
  - `arm_path.B_PATH` reads through the window twice (the count, then each entry) and answers `arm_path.ENTRIES`.

  It is a check of the harness self-test ("the answering-ports arm's path port is arm_path.py's, which reads the window"), and `record_classes.py --selftest` fails on it.
- **The mutant.** "build: arm B's path port answers no entries at once, reading no window (earlier rule)" restores the earlier stub in `build.VARIANTS`. It is caught by that check.

Evidence:
- the real legs at `eca1b9ca`: arm B's GET_AS_PATH is SUCCESS at control_data_length 80, 1x1/1if 16,208 cycles and 8x8/2if 16,397 / 15,966. Arm A's is ENTITY_MISBEHAVING at 16. `record_classes.py` over every one-interface leg and the 8x8 legs: RESULT PASS;
- R833-5's probe on a clean clone of `b15da60a` (lane gate `stub_probe_refused`): both suites refuse it by name: `run.py --self-test` fails "the answering-ports arm's path port is arm_path.py's, which reads the window" ("the answering-ports arm's build does not define arm_path.py's path port"), `record_classes.py --selftest` exits 1 on the same finding, and `build.py` is restored;
- a scratch stub-port leg (arm B, 1x1/1if, `aecp`; `receipts/stub-leg/`, never committed): it answers SUCCESS at control_data_length 16, 10,019 cycles, and `record_classes.py` refuses it by name, beside every leg and in place of arm B's.

## 2. F2: the focus figures receipted

`receipts/records/`: every AECP record of the head's legs (`fB1`, `fA1`, `fB8`, `fA8` at `eca1b9ca`) and the measurement legs (`mB1`, `mA1` part 3, `m2B8`, `m2A8`). Each record has its group, start, CPU cycles, cost by the rule, command, status and response control_data_length. Then each GET_AS_PATH response frame is decoded: status, sequence_id, descriptor_index, count, control_data_length, frame length and the eight ClockIdentities. Then the most by command and status.

| Figure | Receipt line |
|---|---|
| 1x1/1if arm B, 16,208 cycles, 175 us | `fB1-results.txt`: `aecp ... 16,208 cycles 175 us command GET_AS_PATH status 0 control_data_length 80`; the response: `count 8, control_data_length 80 (16 + 8 x 8 = 80), frame 106 B, entries 001bc5fffe000000 ... 001bc5fffe000007` |
| 1x1/1if arm A refused, 10,948 cycles | `fA1-results.txt`: `10,948 cycles 115 us command GET_AS_PATH status 10 control_data_length 16`; `count 0` |
| 8x8/2if interface 1, 15,966 cycles | `fB8-results.txt`: `15,966 cycles 170 us command GET_AS_PATH status 0 control_data_length 80`; the response on port 1, `count 8` |
| 8x8/2if interface 0, 16,397; arm A 11,328 / 11,150 | `fB8-results.txt`, `fA8-results.txt` |

Each receipt names its image's sha256. The head legs' ELFs are the measurement builds' (round 5's `harness/final-eca1b9ca/images.txt`).

## 3. Residue RES1-RES5 (R833-5's exact fixes)

- RES1 (`SPLIT_CONTROL_MEMORY.md:2557`): "R4 13.25 ms (13.10 at the final pass's restatements)".
- RES2 (`:2526`): "At 950 us every 1x1/1if row held by every source ... the load was 0.516 and 0.512 (with GET_AS_PATH's restatements, below)".
- RES3 (`:2532`): "within the 245 us of an ordinary record (235 before the restatements below)".
- RES4 (the PR body's round-5 line): `PR-BODY.md` names R833-5 NEGATIVE at `eca1b9ca`.
- RES5 (round 5's REVIEW READY, issuecomment-6894799910, "Lane gates"): edited in place, as assigned. Only that phrase changed, to "as built at 1x1/1if R4 and last (the first queued notice at its 20 ms bound)" (`receipts/res5-edit.diff`). The as-built log shows first 20.00 of 20, +0.00.

## 4. Gates

One pass at `b15da60a` (`final_pass6.sh`, `gate_queue6.sh`, `lane_gates6.sh`), each part on its own fresh clean clone: 12 dispatched units, all rc 0 (`receipts/gates/dispatch-final-b15da60a.log`). No sweep: there is no firmware or RTL change.

| Gate | Result |
|---|---|
| the docs workflow, every job and `run:` step (`wire-accountability`, `docs-check-no-git`, `docs-check`, `docs-gates-0` to `-2`) | 61 steps ran, 34 not run with a stated reason, 0 bad; the job clones have no tracked change afterwards |
| lane gates (24) | 20 at 0, and the 4 that exit 1 by design, each output byte-identical to `eca1b9ca`'s. Among the 20: the harness self-test (0 failures, 250 of 250 mutants), `record_classes.py --selftest` (14 of 14 and the port check), `rows_tiers`, `load_grade.py --selftest` and `--check` (0.518 / 0.514), `flip_grade.py --selftest` and `--check --point 1x1/1if` (output identical to `eca1b9ca`'s), `tier_grid.py` (950 us), `plat_ledger`, the fixtures and `test_ctrl_memory`, `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets, and R833-5's probe refused by name |
| CPU budget harness legs, one a point and arm | every leg rc 0; `record_classes.py` at this head over them and round 5's one-interface legs: RESULT PASS |
| the images | all 14 byte-identical to `eca1b9ca`'s: the six harness arms, and the size fixture and the platform at the four points |

## 5. Changes (file, reason)

| Commit | File | Change | Reason |
|---|---|---|---|
| `b15da60a` | `tb/verilator/ctrl_service_budget/record_classes.py` | `Record.length`; `ANSWERED_LENGTH`; `answered_path`; the 1x1/1if guard and the every-leg length check; `port_findings`; the control "a GET_AS_PATH answered SUCCESS with no entries"; `checks()` and `--selftest` run the port check | F1 |
| `b15da60a` | `tb/verilator/ctrl_service_budget/selftest_mutants.py` | the mutant "build: arm B's path port answers no entries at once, reading no window (earlier rule)" | F1, the check can fail |
| `b15da60a` | `tb/verilator/ctrl_service_budget/README.md` | the record-classes paragraph and the mutant table's row | F1 |
| `b15da60a` | `docs/design/SPLIT_CONTROL_MEMORY.md` | RES1-RES3; section 13's statement of what the guard refuses | RES1-RES3, F1 |

## 6. Notes

- **#902 moved again**, to `41ca9f87` (11 commits past `234bc149`). It is not merged. A scratch trial merge into `b15da60a`, aborted, conflicts in `SPLIT_CONTROL_MEMORY.md` and FR_NFR 3.4.1 (`receipts/sync/894-tiers-41ca9f87-trial-merge.txt`). #902's section 13 states the paced class at 300 us; this branch's `edit_rows.PACED` is 305 at 1x1/1if.
- **R833-5's suggestions are retained:** S1 (`arm_path.B_PATH`'s stand-in), S3 (the answering-every-port arm's `a_path`) and S4 (`build.py`'s wrapping). S2 is applied: this round's INDEX is generated after sanitizing.
- **No unit of this lane is left running.** The scratch clones `cl-stub` and `cl-final-b15da60a` stay.
- **Nothing is pushed and no PR is edited.** The only comment edit is RES5's phrase, as assigned.
