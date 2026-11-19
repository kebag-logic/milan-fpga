# 943 A800 round 2 — handoff

STATUS: DONE (19:45 CET 2026-11-19). REVIEW READY (round 2) posted on #943: issuecomment-7018504570. Head
`a16899b1` on branch 943-out-status, committed, NOT pushed (the manager pushes). ETA: none, the round is finished.

Answers R872-1 (NEGATIVE at 502b041c: F1 MAJOR, F2 MINOR, R1) and R871-1 (NEGATIVE at 502b041c: F1 MINOR; S1, S2).
The table is RESOLUTIONS.md; the PR body for #953 is PR-BODY.md, built from the published body (the manager applies
it); the receipts are receipts/ (INDEX.md, 44 files).

## Commits (round 2)

- `106c7203` Pin a declaring STREAM_OUTPUT's whole flags word under each Listener declaration and refuse another
  interface's Listener in AppOutputs, each defect planted (#943)
- `a16899b1` Grade a declaring STREAM_OUTPUT's completion in the CPU budget harness's declaring-outputs arm, its
  records held by class and its plants caught (#943)

## Gates at a16899b1

| Gate | Result | Receipt |
|---|---|---|
| declaring-outputs arm, 1x1/1if and 8x8/1if (clean clones) | 0 refusals, 0 budget misses; 6 and 13 completions in records, 1 in a round each; share: 0, and 2 in aecp-largest-notice at 8x8/1if (as arm B) | budget/declaring-outputs-* |
| the three plants, both points (a16899b1's tree but its design-doc paragraph) | each CONTROL caught, 0 refusals | budget/plant-* |
| record_classes (A, B, every-port, declaring) | PASS at both; FAIL without the declaring legs | budget/record-classes-* |
| flip_grade --check | PASS at both, unchanged | budget/flip-grade-* |
| run.py --self-test | 0 failures | budget/harness-selftest.txt |
| bridge probe (F2) | brief: brief=1, 0 source calls; whole: 1 call, 91e0f0000100 | budget/brief-probe.txt |
| AppOutputs at 1x1/2if; 17 rows planted at 1x1/2if, 1x1/1if, 8x8/1if | PASS; 17/17 at 1x1/2if, 15/17 at one interface (two equivalents) | tests/, firmware/plants-* |
| firmware gate, 4 shards | PASS (1,806 invocations; control 825/825; AECP 383; 0 escaped) | firmware/firmware-gate-* |
| fw_coverage --check | PASS, 40 files | firmware/fw-coverage-a16899b1.txt |
| docs.yml gate steps | every step rc 0 but the 3 RV32 SDK verify steps (host SDK, as in round 1) | docs/ |
| ctrl_boundary --without verilator | refuses the same two pre-existing files; declaring_outputs.py not refused | firmware/boundary-* |
| py idiom gate, docs_check, docs inventory | pass; the inventory fresh | (lane runs) |

Carried from round 1, the firmware unchanged (`git diff 502b041c..a16899b1 -- sw/firmware` = the two test files):
twin and plants, plat_ledger, memory test, release image, arm A, answering-ports/every-port/talker-notices arms.

## For the manager

- The open risk, the owner's (R871-S1's second half): on the declaring arm's image the records with no completion
  measure 320 us (paced, 1x1/1if) and 1,760 us (long, 8x8/1if), reported, not held; the held declaring SET_STREAM_INFO
  is 3 cycles inside 245 us at 1x1/1if. Not a STOP: no held figure is over its statement and no bound moved.
- R871-S2: in the round-1 author packet, label receipts/firmware/plants-*.txt as an intermediate row set.
- Units of this lane: all finished (no milan-943-a800-* unit left running).
