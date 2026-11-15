[A776] REVIEW READY
Commit: `eca1b9ca` (round 5, on #902's round-13 head `234bc149`; round 3's `f098f893` was POSITIVE from R833-4)

Round 5, under #897's ruling issuecomment-6890824581 on round 4's STOP. Not pushed; `dev-soft-core` is still `cec88385`.

Changed (since round 4's merge `b58a5430`):
- `2170b22e`, item 1: the platform's 8x8/2if entry is 60.5, #901's `8238156d`. It did not cherry-pick, so the identical text is applied where the two trees agree. The base lines differ: #895's `ctrl_plat` is 20,352 B, this tree's 20,288.
  - `ctrl_memory_ledger.py` (30 lines) and `test_ctrl_memory.py`'s control are byte-for-byte `8238156d`'s.
  - The entry moves 60.0 -> 60.5, its reason naming this tree's 168 B.
  - Section 5 states the plan: 1,880 B left in 133,120; a debt of 4.5 RAMB36; GET_AS_PATH uses 312 B of the half tile; graded against 133,120 B once #901 is composed.
  - At the #901 merge only that entry's reason, its `ctrl_plat` figure and two docs lines conflict.
- `3079bb1e`, item 4: GET_AS_PATH's record is tracked in arm B's `aecp` group. The arm's `path` port (`arm_path.py`) reads the count and the entries through the window, as the face's does, and answers 8. `record_classes.py` names the record, holds it as an ordinary record, and refuses a pass without it (2 planted controls).
- `6ef7a8ff`: the row sends GET_AS_PATH on AVB_INTERFACE 0 at every interface, as `get_avb_info`'s does. At `3079bb1e` both 8x8 legs were refused "aecp.get_as_path.if1: unexpected response: status NO_SUCH_DESCRIPTOR": each image holds one AVB_INTERFACE. 3 plants are caught by name. The 1x1 scripts are byte-identical.
- `eca1b9ca`: two class lines restated by the rule, each the same work with its fetches moved by the code's placement. It also restates section 13's "GET_AS_PATH through the face" on `234bc149` (R833-3 R1, R2), section 5's arm row, FR_NFR 3.4.1 and the harness README. No firmware header states either cost.
  - `record.aecp` at 1x1/1if: 235 -> 245 us. The answering-every-port arm's SET_NAME is 23,051 cycles in all 16 groups (22,236 at `234bc149`); at `b58a5430` it is the same ELF.
  - The paced class at 1x1/1if: 300 -> 305 us. Arm B's accepted SET_CONFIGURATION is 28,752 cycles (28,376 at `234bc149`, 28,357 at `b58a5430` with the earlier port).

Validation:
- **GET_AS_PATH's record, by the rule:**

  | Arm | 1x1/1if | 8x8/2if |
  |---|---|---|
  | arm B, SUCCESS, 8 entries (cdl 80) | 16,208 cycles, 175 us, within the ordinary 245 | 16,397 / 15,966, 175 / 170 us, within 265 |
  | arm A, ENTITY_MISBEHAVING | 10,948, 115 us | 11,328, 120 us |

  The 18 data-word reads an unanswered read skips would add about 1,080 cycles, about 185 us.
- **Record classes over every one-interface leg:** the full arm A at 1x1/1if (96 groups), the whole answering-every-port arm (16) and arm B (`aecp`, `aecp-fanout`, `aecp-largest-notice`), plus the 8x8 legs. Every leg exits 0, with the 7 known held-egress misses. **RESULT PASS** after the restatements.
- **Stated-table compare by the rule at 1x1/1if:** every other cost holds:
  - the build of one 730 of 735;
  - AECP's timer slot 70 of 70; LINK 150 of 155; TICK 50 of 55; an SRP record 280 of 280;
  - the largest legal notice 360 of 365; the largest legal command 925 of 975;
  - the datapath events 30.53, 29.18 and 24.24 us against 35, 35 and 30.
- **The rows, the pace and the slice:** `flip_grade.py --check --point 1x1/1if` PASS at the built design:
  - R4 13.25, R4L 188.48, ACMP 29.14, ADP 27.49, MAAP 27.61;
  - first 14.67, R5 74.32, R6 72.41, last 127.52 of 130;
  - tx 33.57, txL 48.61 of 49.

  The load is 0.518 and 0.514 against 0.70. The pace stays 8 ms by its rule. The slice rule holds 6 of 420 and chooses the built 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2 (+0.0080).
- **The answered notice** (a scratch arm, never committed; its diff and the round's inputs are published): 28,098 cycles against 34,000 (one notice) and 65,576 against 85,000 (three).
- **One full pass at `eca1b9ca`**, each part on its own fresh clean clone:
  - **Workflows:** every job a PR to `dev-soft-core` triggers, every `run:` step: 139 ran, 226 not run with a stated reason, 0 bad; the 28 job clones have no tracked change afterwards.
  - **Campaigns:** AECP 308 caught, none missed, the nine `face-as-path-*` plants by name. Control 717 of 717, `plat-as-path-unavailable` among them. SRP 345 caught. `fw_coverage.py --check` PASS (39 files), `ctrl_boundary` PASS.
  - **Lane gates:** 40 at 0, and the 4 that exit 1 by design. Each of those refuses the same rows as at `234bc149` (8x8/2if's, and as built at 1x1/1if R4, first and last).
    - the harness self-test: 0 failures, 249 of 249 mutants; `rows_tiers` 1,033 of 1,033; flip 585 of 585; load 26 of 26;
    - `plat_ledger` PASS, its 8x8-if2 at 131,240 B, 60.5;
    - `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets;
    - the split boot ready at 26.921, 66.545 and 68.766 ms;
    - the NVM gate, `behave`, the twin and the hooks self-test.
  - **CPU budget harness legs at the final head**, one a point and arm: every ELF is byte-identical to its measurement build, every leg exits 0, and the 1x1 group scripts are identical to `3079bb1e`'s.
  - **Verilator sweep:** 65 suites, four shards each on its own picked range. 64 passed and 0 failed. `milan_dp` timed out at its 4,800 s under host contention, "result UNKNOWN, not a failure" by the runner, with 0 failures in its partial log. Run again alone on its own booked range on a fresh clean clone, it PASSES in 2,548 s. That makes 2,713,040 checks, 0 in-suite failures, round 3's count.
- **#909:** every writable symbol of the 8 images has `234bc149`'s address and size. The 8 ELFs are byte-identical to `b58a5430`'s.

Acceptance criteria:
- #897 acceptance 1-4 are met (3 as amended, issuecomment-6828659285); acceptance 5 belongs to the bench lane.
- Ruling item 1 is met. In item 4: the record is tracked and held at both points; the classes, the compare, the pace and slice rules, R1 and R2, and one full pass are done. The delta review from `f098f893` is the reviewer's.
- No STOP condition holds: GET_AS_PATH's record is under the ordinary class; every 1x1/1if row and the load hold; the rule's slice is the built one; every image is within its cap; the response is unchanged on the wire.

Open risks/questions:
- **#902 moved during the round:** `894-tiers` is at `478ff78c` (six commits: docs and comment restatements, and `CTRL_LOOP_TX_MS` at two interfaces). This round stays on round 13's `234bc149`, as the ruling fixes. A scratch trial merge into `eca1b9ca`, never committed, conflicts only in FR_NFR 3.4.1's paced paragraph, which both sides edit.
- **8x8/2if, reported, not restated:** AVB_INFO_CHANGED and AMAP_LIVE_WRITE measure 38.64 and 23.88 us (37.40 and 23.19 at `234bc149`), 45 and 30 by the rule, against the 40 and 25 stated. Restated, the reported last queued notice would be 836.57 ms (806.60) and txL 469.52 (459.40). For #894's 8x8 lane and #890.
- **One AVB_INTERFACE at two interfaces:** each image's entity model holds one (`MBX_CTRCHG_AVB_INTERFACE_COUNT 1u`), so a command naming AVB_INTERFACE 1 finds no descriptor: GET_AS_PATH there answered NO_SUCH_DESCRIPTOR. Whether a two-interface entity must hold one an interface is outside #897's scope. Raised for a decision.
- **The composed #901 + #898 image** is graded against 133,120 B after #901's review head (ruling item 3). Over 60.5 goes to the owner.
- **The 64-entry path** (unchanged): a control_data_length of 528 is past IEEE 1722.1-2021 9.2.2.6's 524, so the largest legal count is 63. The shipped datapath serves at most 8.
