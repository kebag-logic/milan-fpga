[A767] STOP — PR #892, round 2 ([A10] ruling issuecomment-6806698193): R830-1 F1's redelivery moves a split point's RAMB36 plan

Head: `50e2a722ef2671b3f5b017f97b1c7d41705c4f32`, unchanged. The ruling's fixes are in the lane's working tree, uncommitted, until this is decided. Nothing is pushed.

**What moves.** This is the round-1 assignment's STOP condition: a moved RAMB36 plan is a design decision. The measurement used the pinned RV32 SDK (`scripts/ci_rv32_sdk.py --verify-only` rc 0), one runtime and `ctrl_memory.plan`. The point is the size fixture (`ctrl_srp_image.py --with-aecp --layout split`) at 1x1 with two interfaces:

| | `70936b77` | `50e2a722` | with the redelivery |
|---|---:|---:|---:|
| `rom` need B | 106,040 | 106,408 | 106,552 |
| `rom` banks | [65536, 32768, 8192] | same | [65536, 32768, 8192, 2048] |
| RAMB36 | 40.5 | 40.5 | **41.0** |

The need is 56 B over the 106,496 B granule.

**What holds.**
- Every other fixture point keeps its plan, with this much `rom` left:
  - 1x1/1if: 37.5, 1,512 B left
  - 8x8/1if: 50.5, 88 B left
  - 8x8/2if: 57.5 (ledgered), 480 B left
- The target platform keeps its plan at all four points: 39.0 / 42.0 / 52.0 / 59.0.
- `struct ctrl_plat` grows 8 B at the two-interface points (20,072 → 20,080 and 21,384 → 21,392), so the 8x8/2if override must be re-keyed. Re-keyed in a scratch copy, it plans 59.0.

**Cause.** `on_poll`, with the inlined redelivery, grows from 128 to 244 B. Smaller changes: `acmp_mbx_attach` +12 B, `request` +12 B, `image_app` +8 B. A narrower variant without the loop's `rx_records`/`rx_bad` counts still moves the plan: 106,504 B, 8 B over.

**Ruling items in the tree.**
- R829-1 F1: E3 pins the poll's return at one owed frame. Plant `acmp-poll-owes-nothing-at-one`.
- R829-1 F2: on the pinned SDK, round 1's fixture and platform tables come out byte-identical at `1d6bf555` and `50e2a722`.
- R830-1 F1:
  - The redelivery: the kept record, then up to a full ring (19) of waiting records in arrival order, until a decline.
  - K4 is R830's P1: the second command leaves in pass 10. K5 to K7 cover the rest; five new plants and four re-anchored. A scratch subset campaign caught 15 of 15.
  - `ACMP_MBX_PASS_MAX` goes from 1,030 to 2,754, restated in `MAILBOX_SPLIT.md` and the READMEs. `service_bounds`: 0 failures.
  - Coverage of `acmp_mbx.c`: 106/106 lines, 42/42 branches.
- R830-1 F2 and F3: done. No change inside tsn-c-stack is needed.

**Decision needed.**
- (a) Accept 41.0 for the fixture's 1x1/2if. The lane then re-keys the ledger, restates `SPLIT_CONTROL_MEMORY.md` section 5, commits, runs S2 and the ruling's gates on a clean clone, and posts REVIEW READY.
- (b) Keep 40.5. That needs at least 56 B removed from the image somewhere outside this ruling's list; name where.

Recommendation: (a). The point is neither the shipping point nor ledgered, and the platform image keeps 42.0 there. Its margin was 88 B before this ruling, so any later change would cross it.
