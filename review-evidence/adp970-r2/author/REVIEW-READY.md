# #970 round 5: #1015 on the merged dependencies — handoff


**ETA:** nothing pending on this side.

## 1. What changed this round

Two commits on the local `4f6ee193`:

1. `77f2dc55` merges `dev-soft-core` `4df125b8` (#1016), as a merge commit with no rebase.
   - #1016 merged the same `a6864a49` this branch already carried through its earlier merge of `1013-pins`, plus its
     two later commits (`e5d8a71b`, `d3cb3cf1`: gPTP phase 22, test-bench and documentation only).
   - So the consumer change is in the tree once, and the merge had no conflicts.
   - Git kept this branch's tsn-c-stack gitlink, since `dev-soft-core` did not move it after `a6864a49`.
2. `f4833e16` pins tsn-c-stack `c3bff8f3`, #40's merge commit, not its branch head.
   - Its tree `4064709b` equals `95902060`'s, the head the stack review covered.
   - `SUBMODULES.md` row and links are updated, and the #970 entry is written in #1013's table form, naming PR #40.
   - The change log line, the submodule diagram and the documentation inventory come from their generators.

## 2. Validation at `f4833e16`

- ADP arms adp, portable, unit, walk, platboot1 and platboot2: rc 0. 28 of 28 draw plants caught; the full plant table
  names every host test.
- Firmware gate PASS, coverage PASS.
- Boot simulations at 1x1 and 8x8 PASS (`PYTHONHASHSEED=0`, as before).
- Ledger PASS at four points, `rom` unchanged from round 4 (127,832 / 129,624 / 141,944 / 143,688 B).
- Twin and its plants, co-simulation, reboot (unchanged: 92.325 ms to the first ENTITY_AVAILABLE), hooks, budget
  self-test (0 failures) and memory plan tests all PASS.
- The docs workflow's 37 local gates pass.
- CPU legs, against base `5de21ff3`, whose images and simulated hardware equal the merged base's:
  - 1x1: 75 paired, 0 misses on both, composed maximum 1.468 ms, 0 over the share.
  - 8x8/1if: 90 paired, the same 7 known misses, composed maximum 1.820 ms, 0 over the share. The egress ledger passes.
  - Against round 4's legs, no row at either point is apart by more than 0.1 ms.
  - The load and flip tables print exactly the base's output.

Logs: `receipts/r5/milan/`.

## 3. The one remaining loss in the direct run (desk only; `receipts/r5/attribution/`)

Run `direct-20261126-074411` covers 20 link-ups with the link partner's PHY on its interrupt.

**No ENTITY_AVAILABLE was lost.** The partner received 44 ENTITY_AVAILABLEs, `available_index` 1095 to 1138, every
step 1. In every link-up the first one arrived 0.16 to 3.88 s after the carrier.

**The analysis tool's one "lost" link-up is no. 7, and what it lost is a MAAP PROBE** (3 of 4 seen). The tool flags a
link-up as lost when either a PROBE or an advertisement index is missing.

- In the other 19 link-ups, the device's first PROBE arrives at its link event, -0.004 to +0.124 s from the
  partner's carrier, and its first MSRP frame follows it by 1.1 ms (1.1 to 1.2 ms in all 19).
- In link-up 7, the first MSRP and MVRP frames arrived 0.2 ms before the partner recorded its carrier. The PROBE sent
  1.1 ms before them, about 1.3 ms before that carrier, did not arrive. The next three did (+0.56, +1.12, +1.69 s, the
  last with the ANNOUNCE).

**So the device's link came up about 1.3 ms before the partner's, and its first frame went out before the partner's
receive path took frames.**

- That is the partner's side: a link that comes up a millisecond later at one end.
- It is not the device: it sends from its own link-up, as the 19 others show.
