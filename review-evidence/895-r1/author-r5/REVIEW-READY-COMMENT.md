[A775] REVIEW READY — round 5, head `62298ab5cbfeb7056e4567f70e69d578201c75e0` (local, not pushed)

Commit: `62298ab5cbfeb7056e4567f70e69d578201c75e0` (`895-talker-redeclare` on `91c3fc0e`, six commits; the manager pushes). `894-tiers` stayed at `7398ec0a` all round and #902 is open, so no sync merge.

**Changed** (the ruling issuecomment-6876349305, each a derived restatement; no bound, ceiling, the every-source rule, RTL, lwSRP or donor changed):
- `0d2662c0` (item 2): `load_grade.py` states AECP's timer slot and the TICK at 1x1/1if at their measurement on the merge plus 5 %: 65 -> 75 and 45 -> 50 µs, both columns. At 8x8/2if its four: AECP's slot 105 -> 115, the TICK 40 -> 55, a pass's events' fixed part 30 -> 35, MAAP's record 150 -> 155. The AECP record stays #902's 235 (item 3). #909 is named in section 13 for the placement the merge moves, not chased.
- `c2622f79` (item 1): `AECP_PACE_MS` 8 -> 9 ms, `paced_rows.choice` at the tree's tables, with FR_NFR 3.4.1's and section 13's rows.
- `b3a5ed99` (item 1): `CTRL_LOOP_TX_MS` at 1x1/1if 30 -> 34 ms, the tx row 33.20 by every source rounded up.
  - Its two controls plant 33 (were 29).
  - `SRP_REDECLARE_CS` is 2,023 cs at one interface (2,022 before; 2,029 at two).
  - The Talker tests' hold-off horizon is derived from the same headers (it was 20,220 ms typed).
- `8238156d` (item 4): the platform's 8x8/2if entry 60.0 -> 60.5 RAMB36, the owner's cap (#665 issuecomment-6824896581, as issuecomment-6831583372 raised the fixture's), refused at 61.0, with its planted ledgers. S14's debt is 4.5 RAMB36, the cap fully used.
- `10cd5472`: three files of the merged tree held to the idiom ratchets, behaviour-preserving. `check_py_idiom.py`/`check_cpp_idiom.py` failed already at `91c3fc0e` (round 4 ran no gates) and pass at #902's head.
  - `srp_gate.hpp`: one declarator a line.
  - The Talker plant table: split in two functions, the 34 plants identical tuple by tuple.
  - `build.py`: comments reflowed, 1,003 -> 1,000 lines.
- `62298ab5`: section 13's closing load, ROM and summary.

The order is costs, pace, tx: at pace 9 with #894's two costs the slice rule takes 950 µs, not the built 900; at the restated costs it takes 900 again (least margin +0.0225).

**Validation**, at the head:
- `flip_grade.py --check --point 1x1/1if` **PASS**:
  - txL 47.86 of 49; tx 33.20 (`CTRL_LOOP_TX_MS` 34) of 49; R4L 203.48 of 238;
  - last queued notice 127.08 of 130; ACMP / ADP / MAAP 28.85 / 27.20 / 27.29 of 30;
  - R4 12.96, first 14.59 of 20; R5 / R6 73.46 / 69.35 of 90.
- The pace rule gives 9 ms (txL 49.46 at 8, 47.86 at 9).
- `tier_grid.py --point 1x1/1if`: 18 of 420 designs hold, **CHOSEN the built design** (900 µs).
- `load_grade.py --check` PASS: **0.515** at the pin, 0.511 with tsn-c-stack#32, and 0.694 with every notice the largest legal one. The ruling's 0.528 included the AECP record at 300.
- Self-tests: the flip check refuses 555 of 555 plants, the load gate 25 of 25.
- **The CPU budget harness**, every group of every arm at 1x1/1if and 8x8/2if (clean clone of `b3a5ed99`, the head's firmware):
  - 0 refusals and 0 `STATED` lines in any leg; every leg rc 0;
  - arm A 7 of 950 and 7 of 994 misses (the `backlog-owed` held-egress rows, ruling 6871343905 (a)); every other arm 0;
  - 0 passes over the share (134,749 and 230,855 in arm A).
  - **Join intervals: 1,091 in 227 group runs, 185.905 to 190.192 ms, all within 181 to 239.**
  - At the head (`harness_final.sh` + `compare_builds.py`, all eight point-arms): the images' loadable bytes are identical, the samples byte-identical, and every group regrades rc 0.
  - Measured costs equal round 4's cycle for cycle, each within the restated tables. The largest legal command's record is 970 µs, within its 975.
- **ROM** (`plat_ledger.py` PASS; `test_ctrl_memory.py` PASS):
  - platform 8x8/2if **60.5** (131,256 B, 1,864 B left);
  - fixture and both 8x8/2if harness arms 59.0 (864 / 556 / 696 B left);
  - every other point at most 56: platform 43.0, 43.5, 56.0; fixture 41.0, 42.5, 54.5.
- **The full pass, once, at the head**, each job on its own clean clone, never piped:
  - every `run:` step of the four workflows: 139 rc 0, 226 not run with a stated reason, 0 bad (`verify_wf.py`). The campaigns catch control 716 of 716, AECP 274, SRP 413, 0 escaped.
  - **Verilator sweep, 4 shards on their own booked ranges: 65 suites, 0 failed, 2,712,199 checks.** `tsn_fuzz` with the pinned tsn-gen passes.
  - Lane gates: all rc 0, but the two flip checks that hold 8x8/2if (rc 1 by design). `test_builder.py --require-rv32`, the split boot and its plants, behave 511 scenarios.
- Receipts: lane 895's management output `round5/receipts` (`INDEX.md` generated from the files present).

**Acceptance criteria:** acceptance 4 composed holds by the ruling at the head: every 1x1/1if row by every source within its bound, the load within 0.70, `tier_grid.py` holding the built design, every join interval within 181-239 ms, each image within its entry. Acceptance 1-3 and 5 stand from earlier rounds, re-checked by the Talker tests and the 34 plants at both interface counts. Acceptance 6 is the bench run, not done here.

**Open risks/questions:**
- **The AECP record:** 28,173 cycles (300 µs) here, 235 stated by the ruling. #902's round 11 (#894 issuecomment-6878230332, 6878532871) answers it with a cut or a class split. When `894-tiers` moves, #901 merges it again and recomputes.
- **Not this lane's, for #894:** `firmware-unit` and the mutant jobs leave an untracked `dispatch-build/keys/` in their checkout. #902's `aecp_arms.key_arms` (`58e6b60f`) writes two key-geometry YAMLs while the shard-dispatch self-test builds its arm list.
- **Not run:** act and the hosted exact-head contexts (they follow the push). A note on #909, which this lane does not post on, is the manager's. `[TIME]` (#906) and the hold `[TX]` (#907) stay pre-existing.
