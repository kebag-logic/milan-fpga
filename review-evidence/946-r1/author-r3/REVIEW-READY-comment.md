[A797] REVIEW READY (round 3)
Commit: `fe297847` on `946-ctx-fmt` (round 3 is `cbbd1ac0`, `fe297847` on round 2's `9f4f3de0`). Tests and docs only: no firmware behaviour changes, and the only production-source change is one comment in `sw/litex/ctrl_memory.py`. The composition onto the flip train (PR #945, `b1f1161b`) is made by round 2's recipe: scratch `f8694fdd`, round 2's `d98dd322` plus exactly this round's tests, plants and README.

Changed (answering R867-2 and R868-2):
- R867-2-F-1: `test_plat_sinks.cpp` S11 exercises the change gate at a bound input's own index. Input 7 is bound and its stream published. STREAM_OUTPUT 7's waiting SET_STREAM_FORMAT is acknowledged, answers SUCCESS and writes no context. SET_NAME of input 7 answers SUCCESS and writes no context. The reviewer's two plants are in `sink_mutants.py` (28 defects now): the type test dropped and the kind test dropped, each caught by S11 on its own words.
- R867-2-F-2, R867-2 RESIDUE-3 and R868-2-R2: the PR body's "Why it is race-free" now states the code's order.
  - The change port forwards the change to the face, whose publication makes its own mailbox accesses.
  - It then reads the applied state, unless the core is doing a waiting change again.
  - Then it writes the contexts.
  - All of this happens before the core answers and before control returns to the event loop, so no ACMP input is processed between the change, or the bound check, and the write.
  - Round 2's handoff and REVIEW READY used the "no mailbox access between" phrase too; this text supersedes them.
- R867-2 RESIDUE-1 and R868-2-R1: the `ctrl_memory.py` ledger comment names the debt's owner as "the hybrid XIP work, the cold-code and descriptor flash migration (#665 decision D3)". The diff is comment-only.
- R867-2 RESIDUE-2: Known limitations names #950.
- Suggestions:
  - S-2 is taken as a test-only check: S1 asserts that every format an input with a context advertises is AAF.
  - S-1 is not taken: the status is a core change, and #950 carries it.
  - S-3 is not taken: the line predates the PR, and that README takes the train's side at composition; left to #746.
  - R868-2-S1 is answered in Known limitations, which names the face copy and the channel clip as #950's to cover.

Validation (lane `fe297847` / composition `f8694fdd`):
- Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test`: PASS / PASS. Verdicts: 75 / 74, none failed. Control campaign: 745 of 745 / 825 of 825, the 28 sink defects among them. AECP and SRP campaigns: 729 / 875 defects caught, none escaped.
- `Sinks.S1` to `S11`: 11/11 at 8x8/1if and at 1x1/1if.
- `fw_coverage.py --check`: PASS / PASS, `ctrl_plat.c` and `ctrl_plat_csr.c` at 100 % lines and branches after exclusions.
- Docs workflow steps: lane, every step dev-soft-core has passes; composition, 97 of 97. `test_ctrl_memory.py`: 0 failures.
- `plat_ledger.py --self-test`: PASS with 8 of 8 controls / PASS with 9 of 9. The product image at all four ledger points is byte-identical to round 2's on both bases.
- CPU-budget images are hash-equal: the composition's to the train's recorded ones (1x1 `55484254e638ed7f`, 8x8/1if `175418f4b5b1a9d4`), and the lane's to dev-soft-core `cb96336d`'s (1x1 `554b04f717765a88`, 8x8/1if `112680a06b8983e6`).
- Carried from round 2, whose inputs round 3 does not change: the receive stack's suite, the split boot simulation, the twin, and the composition's sweep.

Acceptance criteria: unchanged from round 2. The bench's stream, power-cycle and soak items at 8x8/1if are not run here; there is no hardware in this lane.

Open risks/questions: unchanged from round 2 (#950 for input 0, the CRF input and STREAM_OUTPUTs, with the refused change's status and the face copy's exposure).
