[A767] STOP — PR #892, round 2 ([A10] ruling issuecomment-6807277620): the 8x8/2if flip check reads 0.767, over the owner's 0.75

Head: `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb`. Nothing is pushed. It is six commits on `50e2a722`:
- the ruling's fixes;
- the 8x8/2if override re-keyed at `ctrl_plat` 21,392 B, with `SPLIT_CONTROL_MEMORY.md` section 5 restated at 41.0;
- `scenario.py`'s comment shortened, so the module stays at the Python gate's 1,000-line limit.

**How it was measured.** `load_grade.py` and `flip_grade.py` are on S2b's branch, not on this base. I measured on a scratch tree: S2b's head `e7e2b744`, with this PR's firmware delta (`acmp_mbx.c`, `acmp_mbx.h`) and the pin at `715589c`.
- Two scratch-only adaptations: S2b's hot list drops `__lshrdi3`, which nothing links since tsn-c-stack#27; and S2b's 8x8/2if fixture ledger goes from 57.5 to 58.0, so its image builds (the ROM finding below).
- S2b's donor-leg groups: 19 at 1x1, 18 at 8x8.
- S2b's own parsers (`costs24.py`, `aecp_kinds.py`).
- S2b's round-27 rule for the donor column: each cost is the larger of this measurement and the committed columns.
- Built with the pinned RV32 SDK.

| Point | Load, committed pin column (`70936b77`) | Load, committed donor column (tsn-c-stack#32) | Load with `715589c` and the redelivery | Ceiling |
|---|---:|---:|---:|---|
| 1x1/1if | 0.463 | 0.450 | 0.483 | 0.70, within |
| 8x8/2if | 0.815 | 0.719 | **0.767** | 0.75, **over** |

**Cause.** ACMP's owed-frame item (`item.acmp`, the span of the adapter's poll that commits an ACMP frame) rises from 40 to 165 us at 8x8 (35 to 120 at 1x1). On a scratch build that also traces `acmp_poll` and `acmp_rx`, the heaviest 8x8 poll (15,550 CPU cycles, `backlog-owed`) breaks down as:
- the core's poll sending the owed frame: 3,990 cycles;
- two `acmp_rx` calls (the kept command offered again, and one waiting record): 9,248 cycles;
- the adapter's ring take: 2,312 cycles.

That command handling is already charged per record (`rec.acmp`). The grader charges it again at the owed frame's rate.
- With `item.acmp` as the poll less the commands it handled (6,302 cycles, 70 us), 8x8/2if reads 0.730.
- With the core's poll alone (45 us), it reads 0.721.
- SRP's term is unchanged at 0.219.

**Also measured on that tree.**
- At 1x1, S2b's harness fails `poll_grade.py`'s stated item: "STATED backlog-owed: a acmp item of 10,974 CPU cycles, over its stated 6,500" (four instances). 8x8 stays under its stated 185 us.
- Budget misses are 7 of 141 at 1x1 and 7 of 182 at 8x8; S2b's donor legs had 6.
  - The four commands behind the owed input are answered, at 62.9 to 64.6 ms; at the donor they were never answered.
  - The new miss is `backlog-owed.service.acmp.last`, at 62.1 / 62.5 ms: the acmp ring is held while a command is kept.
- ROM: S2b's 8x8/2if size fixture with this delta needs 122,984 B of `rom`. That takes a fifth bank (124,928 B) and plans 58.0 RAMB36, refused at S2b's ledgered 57.5. S2b's sync onto this pin owes that, and the hot-list entry.

**This lane's own figures**, on the pinned SDK, at `8ffcf2fc`. The only later commit changes one comment, and every gate is re-running on a clean clone of `bfe7a9d6`.
- S2 at both pins: T_svc misses 34 -> 34 of 141 at 1x1, 63 -> 59 of 182 at 8x8. The four commands behind the owed input go from never answered to all answered, the worst after 104.568 / 138.526 ms.
- The control campaign caught 585 of 585.
- Workflow steps: 150 rc 0 (the eleven SDK install-and-verify steps now among them), 215 not run with a stated reason, and 1 bad, the Python idiom gate, which `bfe7a9d6` fixes.

**Decision needed.**
- (a) S2b's grader charges a command handled inside the ACMP poll to its record only: the acmp item less its nested `acmp_rx`. 8x8/2if then reads 0.730, within 0.75, and the same accounting lowers the 1x1 poll item that S2b's harness now flags. That change is on S2b's line (#810, #890), not in this lane.
- (b) The owner accepts 0.767, or moves the flip ceiling.
- (c) A redelivery that takes a kept command's handling out of the poll. Only the poll runs between an accepting poll and the next timer service, so this needs the service loop changed (not this lane's) or the port contract's redelivery rule relaxed.

Recommendation: (a). The over comes from the measurement charging each command's handling twice; very little of it is new work. The redelivery moves a kept command's handling from the receive service into the poll that frees its slot.
