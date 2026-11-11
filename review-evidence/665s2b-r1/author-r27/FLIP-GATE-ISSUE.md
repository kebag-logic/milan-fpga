Title: Mark II split: the flip at 8x8/2if waits on its long-window load (`flip_grade.py --check`)

The S2b lane (#665) splits its load gate (round 27 ruling, issuecomment-6788828284, item 4). `load_grade.py --check` holds 1x1/1if for merge. 8x8/2if moves to a flip check, `tb/verilator/ctrl_service_budget/flip_grade.py`, which the split placement's flip at 8x8/2if must pass. At S2b's round 27 head it exits 1.

**Evidence at the S2b head** (round 27 receipts; the figures are `load_grade.py`'s and `flip_grade.py`'s own output):
- 8x8/2if, read at this tree's TSN stack pin (the flip check's column, item 6): **0.815**, ceiling 0.70, 1.16x the compute for 0.70. Largest terms: SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070, the timers 0.068.
- 8x8/2if with tsn-c-stack#32 at the pin (the column graded for merge until round 27): 0.719, 1.03x.
- The baseline (#882's harness fix, re-measured on unchanged firmware) moved no stated cost.
- A cut of this tree's share of SRP's record was measured on a scratch image and not committed. Its heaviest record fell from 34,361 to 33,741 cycles, about 0.713 with tsn-c-stack#32 and 0.809 at the pin. It took arm A's image with tsn-c-stack#32 over the 8x8/2if ROM ledger (122,936 B in 122,880).
- On the same groups, one image to the next moved the heaviest work pass by -15,987 to +2,056 cycles.

**Acceptance**
1. `python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check` exits 0 at the flip's head: 8x8/2if at most 0.70, read at the pin of that head, every stated cost measured on that head's image.
2. `flip_grade.py --selftest` refuses all six of its controls at that head, the over-ceiling row among them.
3. The access cycles of #870's `KL_mbx` round, once it lands, are in the grade (round 27 ruling, item 7). Until then the harness's own access cycles are used, as S2b's round 27 used them.

**Options** (the round 27 ruling, item 5; the owner chooses): a flip ceiling other than 0.70; a per-source refill (from S2b's round 26: SRP's refill 2 to 2.19 ms closes 0.019 with tsn-c-stack#32, and more is needed at the pin); compute, #872 early (1.16x at the pin); or an lwSRP donor cut. 57 % of the heaviest SRP record's cycles are lwSRP's code. Its excess of some 11,000 cycles over the second heaviest is not in what the in-tree cut reaches.

**Dependencies:** #872 (the more-compute image); #870 (S9's `KL_mbx` timing round and its access cycles); the TSN stack pin move that carries tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32 (tsn-c-stack#34, merged on the stack's `main` at `715589c`; the move is its own lane under #859's round 4 ruling, item 1). That pin move owes the 8x8/2if `answering-every-port` arm 204 bytes of `rom`. Once it lands, the pin includes tsn-c-stack#32, and acceptance 1 needs the pin's column measured again on that pin's image: the committed `load_grade.STATED_US` is this head's pin, `70936b77`.

**Out of scope:** 1x1/1if, held for merge by `load_grade.py --check` (0.450 with tsn-c-stack#32, 0.463 at the pin), and 32x32/2if, reported as the more-compute image (#872).

Relates to #665.
