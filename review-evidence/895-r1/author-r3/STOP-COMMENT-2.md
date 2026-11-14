[A775] STOP — round 3 after the ruling issuecomment-6857334948, head `9e30c2c383ced58b0b2b87e774ea3b63d6389514` (local, not pushed; its firmware is `cf5b1441`'s, the last commit docs only)

**Why: a stated pass cost cannot be held at 1x1/1if.** In this lane's `valid-destinations` arm (its `srp-talker` and `srp-talker-loss` groups), a pass given whole to a build of one MRPDU takes up to **46,489 CPU cycles**. That is over the **43,000 (430 µs)** that `CTRL_LOOP_BUILD_ONE_PASS_US` states at 1x1/1if (`ctrl_loop.h`). `whole_grade.py` prints it as `STATED`, so the leg fails (four passes over). No bound, cap or ceiling was changed.

- **It comes from the sync merge, not round 3's firmware.** The same first build-one pass of `srp-talker-loss` (sys 327.5 M), from the same script:

| Commit | Build-one pass, CPU cycles |
|---|---:|
| round 2 `17ac263f` (old base) | 35,270 |
| the sync merge `cd6d79b6` (no round 3 firmware) | **45,339** |
| `f1f21546` (#905) | 46,528 |
| `a9fd4415` (names patch) | 45,566 |
| this head | 45,452 |

- **The cause is a data-cache layout move.** Committed-PC traces of that pass at round 2 and on this round's 8 B firmware (its first form, 45,204 cycles) show 6,798 and 6,795 instructions and 130 and 129 instruction refills. Load/store waits are 28,468 and 38,405 cycles. The extra waits are spread over `mrp_transmit`, `forward`, `declare_sources`, `transmit`, `deliver_event_changed` and `reg_event`, several of them at stack loads and stores.
  - The split stack is the 8 KiB after `.bss`, the data cache's own size.
  - #810 grows `nvm_stage` by 110 B and adds the saved-state store's 552 B `nvm`. That moves the 1x1/1if stack 368 B (about 6 sets) against SRP's objects, which stay at the same addresses (`image_arena`, `image_srp`, `image_app`).
- **Why it was not caught before.** #810 stated 430 µs as "the heaviest over every group plus 5 %" of its own arms. This arm is #895's and was not in that set. Round 2's legs ran before the merge.
- **To go on, one of these needs a decision; none is this lane's to take:**
  - (a) restate `CTRL_LOOP_BUILD_ONE_PASS_US` at 1x1/1if with this arm measured. With the rule's +5 % and 5 µs rounding that is 490 µs. THE RETRY's search reads it (`ctrl_retry_search.py`), so the search's figures move with it.
  - (b) a stack placement that does not move with `.bss`, for its own issue. It would also remove the fragility below: at this head the 8x8/2if `valid-destinations` image still has a per-source conflict of the kind #905's 24 B gave every 8x8/2if image (its polls' base at most 29,093 of 32,500).
  - (c) leave this arm's build-one passes out of the stated cost.

  Almost all the extra cycles are in donor and SRP-core code. The one #895 function among them, `declare_sources`, accounts for about 1,900 of the 10,000.

**Fixed this round, found on the way to the legs:**
- **#905's state set the 8x8/2if polls' base over (`cd863d40`).** At `a9fd4415`, `answering-every-port` read `STATED notice-burst-1/-4: a pass's polls base of 32,594 / 32,597 CPU cycles, over its stated 32,500`.
  - Every MAAP poll cost a constant ~2,300 cycles more than #810's.
  - A trace pinned it on the data cache. `refresh_demand` asks `acmp_declaring` of every source, and its saved registers had landed on the set of the size fixture's `image_aecp_bridge.acmp_owner`, which the source port loads: two refills a source.
  - This came from #905's 24 B in `struct maap_mbx` and its poll's larger frame. All three 8x8/2if images at `a9fd4415` had it; #810's had none.
  - #905's state is now 8 B: one source's SRC_SID words in flight at a time, the high word only on its source's own interface. The frame keeps #810's set.
  - **At this head the polls' heaviest base is 31,030 (S-N8 rc 0; #810's leg 30,659).** `MAAP_MBX_*_MAX` are unchanged.
  - The five SID plants are caught at both points. A first form that let either interface write the high word let `talker-sid-opens-before-its-high-word` escape at 2if, so it was not used.
- **The names patch dropped coverage (`cf5b1441`).** At `a9fd4415`, `fw_coverage.py --check` refused `aecp_nvm.c` with branches 89/90. The arc not taken was a name change of a run's type past its count.
  - A test now changes a type-5 name just past its last run and requires that nothing is queued.
  - A planted defect (the count check dropped) is caught by that test's words. The ratchet now reads `aecp_nvm.c` 113/113 lines and 90/90 branches.
  - The patch itself is carried unchanged (`a9fd4415`).

**The ruling's items:**
- (a) **C4-names.patch** is applied unchanged as `a9fd4415`. The full firmware suite passed on it; at this head it passes on a clean clone too (79 results PASS, 0 FAIL, the tree clean after).
- (b) **Every 8x8/2if image is at most 58.5**, with no fallback:
  - fixture 124,568 / 113,216 B, 360 B of rom left;
  - `answering-every-port` 124,876 / 113,280 B, 52 B left;
  - `valid-destinations` 124,728 / 113,232 B, 200 B left.

  Platform 60.0; every other point at most 56 (`plat_ledger.py` PASS, `ctrl_plat` unchanged at every point; the platform's largest 129,728 B of 131,072).
- (c) srptx `[SID]` is graded on its own words: at this head 119 stream frames, all `0200000000010000`, no `[SID]` finding; the #905 code arm is refused by `[SID]` (stream_id 0). `[TIME]` is recorded as #906, the hold `[TX]` path as #907, and neither is fixed.
- (d) Legs at this head (clean clone, every group of every arm, both points):

| Point | Arm | Result |
|---|---|---|
| 1x1/1if | A (4 parts, merged) | rc 0: 94 groups, 0 refusals, 7 of 945 budget misses (tsn-c-stack #26's seven), no STATED |
| 8x8/2if | A (8 parts, merged) | rc 0: 93 groups, 0 refusals, 7 of 996 (the same seven), no STATED |
| 1x1/1if | `answering-every-port` | rc 0: 0 of 280, no STATED |
| 8x8/2if | `answering-every-port` | rc 0: 0 of 736, polls' base at most 31,030 of 32,500 |
| 1x1/1if | `valid-destinations` | **rc 1: 0 of 5, the four build-one STATED lines above** |
| 8x8/2if | `valid-destinations` | rc 0: 0 of 20, polls' base at most 29,093 |
| 1x1/1if, 8x8/2if | B (`aecp`) | rc 0: 0 of 25, 0 of 39 |

No pass over the share anywhere. Least margins: 9.147 / 9.223 ms (arm A), 7.317 / 6.114 (`answering-every-port`), 20.691 / 20.912 (`valid-destinations`), 19.647 / 19.666 (arm B).

Acceptance 4 at this head's legs: the legs' measured costs fed into `load_grade.py`'s two tables by section 13's rule (in a scratch copy, not committed). The 1x1/1if long-window load is **0.503** at the pin and **0.502** with tsn-c-stack#32 (base `084cf7a8`: 0.501 / 0.499), held under 0.70 (`--check` rc 0). The 8x8/2if load is 0.825 / 0.773 (+0.003 / +0.003). 1x1/1if R4 / R5 / R6 are +0.68 / +0.29 / +0.28 ms; 8x8/2if +1.80 / +0.81 / +0.74 ms. Queued notices are unchanged. `flip_grade.py --check` exits 1 with the same OVER set as at the base. The tables move only measured costs (`event.AECP`, `event.MAAP`, `record.maap`; the tsn-c-stack#32 column's `base` at 8x8/2if, and `build_one` 430 -> 490 at 1x1/1if, which is the STOP's figure).

Commits since the first STOP:
- `a9fd4415`: the names patch.
- `cd863d40`: #905's state in 8 B, with the plants' anchors and the srptx arm's line.
- `cf5b1441`: the names-runs test and the ratchet.
- `9e30c2c3`: docs. `SPLIT_CONTROL_MEMORY.md` section 5 at this head, and section 9's new "Where the stack falls in it" with both moves measured. The milan_dp README gains #906 and #907.

Section 13 keeps #810's figures until this decision. Split boot at this head: ready at 26.299, 65.016 and 67.085 ms (1x1/1if, 8x8/1if, 8x8/2if), each PASS.

Not run: the clean-clone gate pass (workflows, sweep, full campaigns), which waits on this decision.
