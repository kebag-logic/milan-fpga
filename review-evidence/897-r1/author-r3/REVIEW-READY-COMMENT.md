[A776] REVIEW READY
Commit: f098f893d57e0fa3ec95a7e459313c5cfe4f4224 (round 3; round 2's head 3bebf03a was POSITIVE from R833-2)

Composed with #902 (`894-tiers`, not merged; `dev-soft-core` still `cec88385`), as #894's ruling issuecomment-6867393730 item (d) requires.

Changed:
- `e45981f8`: one merge commit of `894-tiers` at `5b264bf2`. Four conflicts, each kept from both sides:
  - `ctrl_plat.c`: #902's owed-notice slots, and this branch's `aecp_platform` with no `.path` stub;
  - `coverage.ratchet`: `ctrl_plat.c`'s row, recorded as measured in `417f44af` (132/132);
  - `plat/README.md` and `SPLIT_CONTROL_MEMORY.md` section 6: both sides moved 59.5 to 60.0, and this branch's line was kept.
  For each of this branch's 17 files and #902's 85, the merge carries that side's own diff exactly.
- `25ea917f`: `SPLIT_CONTROL_MEMORY.md` section 5 (the images at the composed head; the paragraph no longer opens "At this branch's head", R833-2 F1) and section 13's "GET_AS_PATH through the face" (its cost in the rows).
- `a3a509d7`: `894-tiers` moved to `7398ec0a` (#902 round 10) during the round, so it was merged again before the full pass. There was no conflict, and the images are byte-identical.
- `f098f893`: the composition took `aecp_mutants.py` to 1,012 lines, past the 1,000-line limit ("long module 11 > ratchet 10"). The nine GET_AS_PATH face plants move unchanged into `aecp_face_mutants.py`, so the campaign's 283 defects are the same in every field.

Validation:
One full pass at this head, each part on its own fresh clean clone:
- **Workflows:** every job a PR to dev-soft-core triggers, every `run:` step. 139 ran, 226 were not run (each with its stated reason), 0 bad. The 28 job clones have no tracked change afterwards.
- **Verilator sweep:** four shards, each on its own booked CPU range. 65 suites, 65 passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures.
- **Campaigns:** AECP 283 of 283 (the nine `face-as-path-*` plants each caught by name), control 717 of 717 (`plat-as-path-unavailable` among them), SRP 345 caught, none escaped. The firmware self-test passes in its four shards, `fw_coverage.py --check` passes (`aecp_face.c` 100 %), and `ctrl_boundary` passes.
- **Lane gates:** 40 at 0, and the 4 that exit 1 by design, with output identical to `5b264bf2`'s (the flip check over both points, at 8x8/2if and as built; the tier model's report). Among them:
  - the 1x1/1if flip check, `load_grade.py --check` and `tier_grid.py --point 1x1/1if`;
  - the py and cpp idiom ratchets, `docs_check` with 0 findings, the em-dash gate;
  - `plat_ledger` (7 of 7 controls); the split boot ready at 26.911, 66.436 and 68.576 ms, with its native controls, placement controls and plants;
  - `test_builder.py --require-rv32`, the NVM gate (526 tests, 144 plants), `behave` (511 scenarios), the twin.
- **CPU budget harness legs at both points:** fresh builds at this head, and the same legs at `5b264bf2` for the deltas. Every image is byte-identical to its measurement build. Every leg exits 0 except 8x8 `srp`, on #910's build of one, as at `5b264bf2`.

Acceptance criteria:
- #897 acceptance 1-4 are met (acceptance 3 as amended, issuecomment-6828659285); acceptance 5 belongs to the bench lane.
- **1x1/1if flip check, composed: PASS**, every row by every source, #902's figures unchanged: R4 12.85/20, R4L 188.39/238, ACMP 28.44, ADP 26.83, MAAP 26.95/30, first 14.51/20, R5 72.91 and R6 68.80/90, last 126.46/130, tx 29.86/49, txL 48.09/49.
- **Load:** 0.513 at the pin, 0.509 with tsn-c-stack#32 (ceiling 0.70), unchanged.
- **GET_AS_PATH's cost in the rows.** A read is at most nine GSI words (the shipped datapath serves at most eight entries). It enters three terms, each within its stated cost at 1x1/1if:
  - AS_PATH_CHANGED's sink: 30.02 us measured, against 35 stated;
  - its notice in THE RETRY's rounds: answered with eight entries in a scratch arm, the round is 46,397 cycles against the 59,500 it is admitted at;
  - a GET_AS_PATH record: bounded at about 200 us, against `record.aecp`'s 235.
  No stated cost moves.
- **Data placement (#909):** every writable symbol of every image has the same address and size as at `5b264bf2`.
- **ROM, against `5b264bf2`:**
  - fixture: 41.0 (was 40.5), 41.5, 54.0, and 59.0 at 8x8/2if (125,688 B, 1,288 B before its granule, #902's entry 59.0);
  - platform: 42.5, 43.5, 56.0 at 8x8/1if (1,552 B before its next granule), and 60.0 at 8x8/2if (130,816 B, 256 B before the half tile, entry 60.0, cap 60.5);
  - harness arms at 8x8/2if: 59.0 each, the nearest 964 B under;
  - every point +312 to +344 B of `rom`, `sram` unchanged; nothing over its cap.

Open risks/questions:
- **No harness group answers a datapath window**, and the answering arms' stand-ins read none. So no stated notice or record cost includes an answered window read for any observation: GET_STREAM_INFO is 6 words, GET_AVB_INFO 3, GET_COUNTERS 33, and GET_AS_PATH at most 9, each up to about 880 CPU cycles a word. GET_AS_PATH's read was measured in a scratch arm and fits. GET_COUNTERS' is the largest; it is #894's model as it stands, outside this lane. Whether to measure answered reads is a decision for #894.
- **The 64-entry path.** The face carries up to `AECP_PATH_ITEMS` (64) entries, the core's capacity since `a008ea92`. At 64 entries the response's control_data_length is 528, past IEEE 1722.1-2021 9.2.2.6's 524, so the largest legal count is 63. The shipped datapath serves at most 8, so no image reaches it.
- **THE TRANSMIT's build of one** at 1x1/1if measures 69,269 cycles here (68,937 at `5b264bf2`), within its stated 725 us; by the stating rule it would be 730 us. The rows solved at 730 us still pass, and nothing is restated. At 8x8/2if it is 0.7 to 0.9 % above `5b264bf2`'s, already over its bound (#910, reported).
- **Left to #902:** two stale figures. Section 13 still says the 1x1/1if fixture is 110,400 B at 40.5 RAMB36. The ratchet rows for `aecp.c`, `aecp_maps.c` and `aecp_mbx.c` are behind their measurement (all at 100 %).
- **ROM margins now:** the fixture's 8x8/2if has 1,288 B before its next granule; the platform's 8x8/2if 256 B before the half tile its entry refuses; the platform's 8x8/1if 1,552 B inside its 56.0.
