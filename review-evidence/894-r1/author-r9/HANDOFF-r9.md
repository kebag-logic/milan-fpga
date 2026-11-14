# 894-a773: #894 round 9, HANDOFF

**Status: REVIEW READY at the final head `5b264bf26416108add32d7fe5abca5252ffde2cb`** (started 03:46 CET 2026-11-14). The full pass at the head is clean (section 7); every 1x1/1if row holds by every source; no STOP trigger fired. Posted 07:28 CET as #894 issuecomment-6872978311, the round's one comment (text: `REVIEW-READY-COMMENT.md`, identical); PR body for round 9: `PR-BODY.md` (not applied: no PR edits this round). Nothing pushed.

- Start head `dd01b0afef87037ec485cd49b40a26b542854bdd` (round 8's REVIEW READY, issuecomment-6870102413).
- Authority: the ruling #894 issuecomment-6870437042 (round 9). Read with it: R838-3 (PR #902 issuecomment-6870395150) and its probes `probe_maps.py`, `audit_hash_geometry.py`; R837-3 (issuecomment-6870427229).
- Nothing pushed. No TAKEN posted.

## 0. Exit (at `5b264bf2`)

1x1/1if, `flip_grade.py --check --point 1x1/1if`: RESULT PASS.

| Row | W, ms | Bound | Round 8 |
|---|---:|---:|---:|
| R4 | 12.85 | 20 | 12.82 |
| R4L (paced) | 188.39 | 238 | 173.37 |
| ACMP | 28.44 | 30 | 28.35 |
| ADP | 26.83 | 30 | 26.76 |
| MAAP | 26.95 | 30 | 26.88 |
| first | 14.51 | 20 | 14.50 |
| R5 | 72.91 | 90 | 72.71 |
| R6 | 68.80 | 90 | 68.62 |
| last | 126.46 | 130 | 125.84 |
| tx | 29.86 | 49 | 29.78 |
| txL | 48.09 | 49 | 47.98 |

- The rows move from round 8's only by AMAP_LIVE_WRITE's restatement (25 -> 30 us at 1x1/1if) and the pace that follows (7 -> 8 ms; at 7 txL is 49.69).
- Pace 8 ms (`paced_rows.choice`); slice 900 us (least margin +0.019); queued bound 130 (no statement); `tier_grid.py` 18 of 420, the built design chosen; load 0.513 / 0.509; every-command load 0.692.
- **No STOP trigger:** P 8 holds (STOP only if none up to 11); last 126.46 within 140; no image over its cap (each equal to round 8's or 8 B smaller); no map-command behaviour change (the definition test byte-identical and passing); the collision case's heaviest pass 93,813 cycles at 1x1/1if, under THE SHARE's 200,000.

## 1. Item 1: the map table as a direct index (`f0611e7f`)

- `sw/firmware/ctrl/aecp/aecp_shape.py:19` `descriptors(blob)` (each descriptor's bytes as aecp_image.c loads them) and `:32` `key_domain(blob)`: emits `AECP_ENTITY_KEY_STREAMS` (most STREAM_OUTPUT index + 1), `_STREAM_CHANNELS` (most AAF channels over each STREAM_OUTPUT's current and advertised formats), `_CLUSTERS` (most clusters of a STREAM_PORT_INPUT), `_CLUSTER_CHANNELS` (most channels of an input port's cluster), any configuration. Reason: the ruling's "sized from the build-time shape constants and the largest channels-per-stream (or per-cluster) value"; read from the image's own bytes.
- `aecp_shape.py:106` / `aecp_entity.py:44`: the generated tables (`aecp_map_defaults`, `aecp_entity_image`) behind `#ifndef AECP_ENTITY_SHAPE_ONLY`. Reason: `aecp_maps.c` includes the header for its constants alone; an unused static table is a `-Werror` warning in C.
- `sw/firmware/ctrl/aecp/aecp_maps.c:5-6` includes `aecp_entity_gen.h` shape-only; `:150-157` `MAP_FIRSTS` = max(streams, clusters), `MAP_CHANNELS` = max(stream channels, cluster channels), `MAP_SLOTS` = their product (at least 1); `_Static_assert` that each direction's domain (streams x stream channels, clusters x cluster channels) fits `MAP_SLOTS`, and that `AECP_MAP_PAGE < 256` (a slot holds index + 1).
- `aecp_maps.c:199` `place()`: the key's position `first * MAP_CHANNELS + channel`, or `MAP_SLOTS` outside the domain; one `VISIT()`. `:375` the decode: `legal()` first (the existing range refusal), then `place()`; a key outside the domain takes the same `ILLEGAL` turn (BAD_ARGUMENTS at its turn, before its port is read, the table ending there). `:216` `look()`: a map row outside the domain holds no mapping's key.
- One stride for both directions (the ruling's single formula). Domains: 1x1 (2 streams of 8, 8 clusters of 1) 8 x 8 = 64; 8x8 9 x 8 = 72; arty_4x4 5 x 4 = 20; arty_8ch 8 x 8 = 64; arty_current 8 x 2 = 16; 16x4 17 x 4 = 68; 16x32 17 x 32 = 544 (`receipts/item2/key-domain.txt`).
- `992e52a0`: `MAP_SLOTS` is the domain's size **at least 256**, the table's former size (`aecp_maps.c:149-160`). Reason (section 4): with the domain's 64 at 1x1/1if the edit's stack frame moves 192 B and the largest legal command's record goes 91,625 -> 98,720 cycles by the data cache alone; restated that is 1,040 us, the pace 9 ms and the every-command load 0.705, over 0.70, so `tier_grid.py` holds no design. At 256 the record is 91,625 (965 us by the rule; 975 kept). The index and its domain check are unchanged; 16x32's 544 is over the floor. The shared stride keeps the existing restore test's 2-channel cluster poke (`Core.MapsCompareEveryCoordinateAndBothDirectionsOnRestore`, cluster channel 1) inside the domain, so it passes unchanged.
- Behaviour: in every product state a legal key is in the domain (a format is set only where the integrator's verdict calls it supported, the builder's shapes; cluster counts are static), so the domain refusal never fires there. It fires only in fixture states that widen a current format or cluster past the build's (the round 8 slot-sharing test's 1023-channel stream; replaced, section 2). The definition test passes unchanged (byte-identical: `git diff dd01b0af -- test_aecp.cpp` touches no line of it).
- Images (`receipts/images/every-image-final.txt`, at the head): rom equal to round 8's or 8 B smaller, sram and tiles unchanged. So item 3's fallback is not needed: the direct index fits.

## 2. Item 2: the controls (`58e6b60f`)

- `test_aecp.cpp:178` fixture helpers `accepted_keys(type)` (port 0's keys from the loaded descriptors: each STREAM_OUTPUT's channels; each input cluster's channels), `edit_map`, `same_rows`.
- `:2632` `Core.EveryAcceptedMapKeyIsItsOwn`: every accepted key added in ADDs of 63 mappings (repeating its keys where fewer are left), each held as its own in order, then removed in REMOVEs of 63; in the work arm each edit within 2 (n + R).
- `:2673` `Core.EveryKeyOfTheDomainIsItsOwn`: input clusters and every STREAM_OUTPUT widened to `KEY_CHANNELS`, within the domain; every position one key's (catches a short stride at 1x1).
- `:2701` `Core.MapKeysOutsideTheDomainAreRefusedAtTheirTurn`: a key past the domain's channel, legal under a widened format or cluster, refused 7 at its turn, after the earlier mapping's port read (reads 1), map unchanged; the domain's last channel accepted; a held row outside the domain bars nothing.
- `:2736` `Core.MapEditWorkIsLinearInItsMappings`: stream input 0 still widened to 64 (values only, the input key (0,0)); the output keys drawn from `accepted_keys(15)`, repeated past the port's 8 at 1x1. The 8/16/32/63 counts and the n(n+1)/2 controls kept.
- `aecp_arms.py:19` `KEY_GEOMETRIES` (16 talkers x 4, R838-3's; one of 8 then 15 of 32, the builder's most: a 32-channel-only entity is refused by the image lint, no Base format), `:22` `key_geometry`, `:36` `key_arms` (KEYS in the work arm at every checked-in configuration and both geometries), `:161` in `all_arms`, `--keys`.
- Removed: `Core.MapKeysThatShareASlotAreTheirOwn` (a hash property; its keys are outside the domain now).

## 3. Item 3: fallback

Not taken: the direct index fits memory (every image smaller, no tile change; the table is on the stack and shrinks at every checked-in configuration).

## 4. Item 4: re-measure, restate, rows, images

- Legs at `58e6b60f` (the domain-sized table, 64 slots at 1x1), `receipts/item4/remeasure-legs.txt`: 1x1/1if REMOVE 98,720, ADD 92,801, refused 23,956 / 83,016 / 83,664 (round 8: 92,766, 86,504, 23,014 / 78,420 / 79,384), every pass within THE SHARE (0 of 102 over); 8x8 146,010 (1,535 us by the rule, 1,555 kept); 8x8-1if 155,625 (reported, lane 894b; the leg exits 1 on THE TRANSMIT's build over the one-interface slice, as in round 8).
- Experiment (scratch clone, not the lane): the same source with the table floored at 256 slots: REMOVE 91,625, ADD 83,716, refused 23,883 / 75,481 / 75,892. So the direct index is cheaper than round 8's table, and the 64-slot rise is the edit's stack frame moving 192 B across the 8 KiB direct-mapped data cache.
- Counterfactual at 1,040 us (`receipts/item4/counterfactual-1040us.txt`, `long-load-by-record.txt`): P 7 txL 52.90, P 8 49.28, P 9 47.63 / R4L 203.44 (holds); the every-command load 0.705 > 0.70 (it crosses 0.70 near 1,015 us), so `tier_grid.py --point 1x1/1if` exits 1 (0 of 420), at P 7 and at P 9.
- Taken: the floor (`992e52a0`). The record at the head's firmware is 91,625 cycles, 965 us by the rule; `LONG_RECORD_US['1x1/1if']` stays 975, the larger kept, as round 8 kept 8x8's 1,555 (comment `rows_tiers.py:126-131`, value `:132`).
- **8x8 (`88ed7082`):** the pre-check pass's H-L8L at `5cfa32c2` (the floored table) measured the 8x8 shape's record at 156,716 cycles, 1,650 us by the rule, over the stated 1,555 (round 8 142,634; the 72-slot table 146,010). The map command's frame is round 8's 2,528 B at both shapes (`mark`'s 80 -> 96); the heaviest 8x8 pass's rise is mostly `ctrl_mem` (memcpy/memset after the edit, 24,492 -> 35,971 cycles), so data-cache state again. Restated `LONG_RECORD_US['8x8/2if']` 1,555 -> 1,650, the larger kept (`rows_tiers.py:132`). 8x8/2if rows are reported: R4L 180.65 -> 180.74 (238), txL 488.98 -> 558.51 (49, over before and after); `flip_grade.py --check --point 8x8/2if` exits 1 as before; rows_tiers 971/971, flip 555/555 at 1,650.
- **The datapath events (`1f47c09c`).** `eventcost.py` (the take and every sink's work, the cut `DATAPATH_US` states; it reproduces the recorded 31.96 / 29.06 / 23.33 us exactly on the earlier heads' legs) gives AMAP_LIVE_WRITE 25.51 us at 1x1/1if at the head and 25.32 at round 8's head: 30 us by the rule, over the 25 stated, so `DATAPATH_US['1x1/1if']['AMAP_LIVE_WRITE']` is 30 (`rows_tiers.py:95-99`). AVB 30.55 and AS_PATH 31.57 stay within 35; 8x8 35.76, 32.79, 22.65 within 40, 40, 25 (`receipts/model/event-costs-final-pass.txt`).
- **The pace (`1f47c09c`).** At AMAP 30, txL is 49.69 ms at 7 ms; 8 ms is the smallest that holds: txL 48.09 / 49, R4L 188.39 / 238 (`AECP_PACE_MS 8u`, `aecp_mbx.h:54`, its comment `:44-53`). Every 1x1/1if row holds: R4 12.85, R5 72.91, R6 68.80, first 14.51, last 126.46 (130 by the next-5-ms rule, unchanged), ACMP 28.44, ADP 26.83, MAAP 26.95, tx 29.86. Slice 900 us (least margin +0.019); `tier_grid.py` 18 of 420, the built design chosen; loads 0.513 / 0.509, every-command 0.692. 8x8/2if reported: R4L 195.74, txL 446.92. rows_tiers 971/971, flip 555/555, load 25/25.
- Pre-checks at `5b264bf2` (units, clean clones): firmware suite PASS; harness self-test 0 failures, 246 mutants caught, 0 escaped; 1x1 `aecp-largest-notice` rc 0 (record 91,625, 0 of 106 passes over THE SHARE, joins 188.087 to 190.013); 1x1 `srp` rc 0 (joins 188.087 to 190.013, 8 released, 5 empty); every image equal to `5cfa32c2`'s.
- Every other input from the legs is within its stated cost at 1x1 and 8x8 (8x8-1if's base over, reported, as in round 8): `receipts/model/measured-inputs-final-pass.txt`, regenerated from the final pass.
- The final pass's legs re-measure every input at the head (section 7).

## 5. Item 5: docs (R838-3-F2, R838-3-F3, R837-3-2) (`5cfa32c2`, with the README parts in `992e52a0`)

| Finding | Fixed at | Now states |
|---|---|---|
| R837-3-2, R838-3-F2: harness README R4L | `tb/verilator/ctrl_service_budget/README.md:183` | R4L's paced bound 238 ms at the commit, 9.3.2.6's 240 ms at the wire less `T_ingress` and `T_egress` (`PACED_BOUNDS`, the egress ruling item 1); the 30 ms rows cite the ruling 6844175391 with the owner's confirmation 6844947317 |
| R837-3-2: the pace rule | `README.md:185` | the smallest whole ms at most 13 that holds txL within its 49 ms bound and R4L within 238 ms (the egress ruling, item 2), and `statements`' exact words |
| R837-3-2: SPLIT_CONTROL_MEMORY R4L | `docs/design/SPLIT_CONTROL_MEMORY.md:2355` | 238 ms at the commit, both allowances, both rulings cited |
| R838-3-F2: THE TIERS bullet | `SPLIT_CONTROL_MEMORY.md:2475` ("What is left") | THE TRANSMIT's 49 ms at 19 cs, 240 less the armed join time and `T_egress` |
| (same class) MRP budget paragraph | `SPLIT_CONTROL_MEMORY.md:2351` | 50 ms, and with `T_egress` 49 ms |
| (same class) THE PACE bullet | `SPLIT_CONTROL_MEMORY.md:2376` | "it found 6 ms" at 50 ms; with `T_egress` and 975 us it finds 7 ms, txL 47.98, R4L 173.37; the every-command load 0.692 (`tier_grid.py`) |
| R837-3-2: the loads | `SPLIT_CONTROL_MEMORY.md:2481` | 0.792 / 0.752 at 8x8/2if, 0.513 / 0.509 at 1x1/1if (`load_grade.py --check` at the head) |
| R838-3-F3: the fixture's +184 B | this round's PR body, REVIEW READY, `receipts/images/rom-layout-f3.txt` | round 8's rewrite grew `.text` by 180 B everywhere; `.rodata`'s 8-byte alignment made it +184 B of rom at the 1x1/1if fixture and +176 B at the other seven; both endpoints stand (no repo text carried the claim) |
| R837-3-R1 (residue): `long_notice.py:19-23` | the docstring | the reviewer's wording: collisions over distinct indices (refused at the first illegal one) and over the key's legal values, the row's own among them |
| R838-3-R1 (residue): "11 commits" | this round's PR body and REVIEW READY | "the delta from `dd01b0af` to `5b264bf2`" |
| Item 4's restatements (`88ed7082`, `1f47c09c`, `5b264bf2`) | `SPLIT_CONTROL_MEMORY.md:2340` (the datapath events), `:2367` (the rows' table, an 8 ms row), `:2376`, `:2453`, `:2462-2463` (the direct index: 8x8's 1,650 us, the datapath events and the pace); `FR_NFR.md:383` | AMAP_LIVE_WRITE 30 us at 1x1/1if, 8x8's record 1,650 us, THE PACE 8 ms with txL 48.09 and R4L 188.39 |
| Item 1's docs | `sw/firmware/ctrl/aecp/README.md:196-238`; SPLIT_CONTROL_MEMORY section 13 "The command, under #904" (`:2375`) and the new "The direct index" (`:2457`) | the index, the domain, the floor and its reason, the controls, the plants |

`docs_check.py` 0 findings; `check_em_dash.py` 0 over 26 changed pages.

## 6. New checks, planted mutants and failing words

| Check | Plant (`aecp_map_mutants.py`) | Failing words | Where caught |
|---|---|---|---|
| Every accepted key its own slot | `map-index-channel-dropped` (`first * MAP_CHANNELS`) | "an ADD of every key the port accepts holds each as its own" | `Core.EveryAcceptedMapKeyIsItsOwn` (output keys collide) |
| the same | `map-index-stream-or-cluster-dropped` (`channel`) | the same | the same (input keys collide) |
| Every position of the domain one key's | `map-index-stride-short` (`first * (MAP_CHANNELS - 1u) + channel`) | "an ADD of every key of the domain holds each as its own" | `Core.EveryKeyOfTheDomainIsItsOwn` (no accepted key collides at 1x1, the filled domain does) |
| No key outside the domain forms an index | `map-domain-a-channel-wide` (`channel <= MAP_CHANNELS`) | "a key outside the domain is refused at its turn, before its port is read" | `Core.MapKeysOutsideTheDomainAreRefusedAtTheirTurn` |
| A row outside the domain holds no key | `map-outside-row-looked-up` (slot 0 for it) | "a row outside the domain bars no mapping" | the same |
| Work linear (quadratic plant, re-anchored from `map-hash-the-stream-alone`) | `map-table-scanned` (each lookup visits every slot) | "past twice their sum" (8 mappings, 1 row: 593 visits at the 64-slot table) | `Core.MapEditWorkIsLinearInItsMappings` (work arm) |
| Work linear (quadratic plant, kept) | `map-remove-values-rewalked` | "not under n(n+1)/2"; "past twice their sum" (38, 138, ...) | the same |

Removed with the hash: `map-table-key-unchecked` (no key compare is left to drop) and `map-hash-the-stream-alone` (re-anchored above). All 32 plants on `aecp_maps.c` and THE PACE caught at the head's firmware (`receipts/item2/map-plants.txt`); the full table is 273 (269 in round 8, less 2, plus 6), and `controls()` holds every test claimed.

## 7. Gate table

The full pass at `5b264bf26416108add32d7fe5abca5252ffde2cb`, once, each part on its own clean clone and never piped (receipts `receipts/gates/`; tooling `scripts/`). Two earlier passes were stopped part-way (section 8) and are not this table.

| Gate | Result | Receipt |
|---|---|---|
| The sweep, 4 shards (`native-shards.py`, label 894-r9i, CPUs 0-7, 8-15, 16-23, 24-31) | exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures | `sweep-shard{0..3}.txt` |
| Every hosted job step of rtl-fast, rtl, elaborate and docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`) | 139 run, 226 not run with a reason, 0 bad | `workflows-verify.md` |
| Firmware jobs: unit, control, AECP and SRP campaigns, boundary, Verilator | every step 0; the AECP campaign 273 of 273 caught, the 32 on the map file and THE PACE among them | `workflows-verify.md`, `unit-rcs.txt` |
| Lane gates, parts a, b, c | 45 at 0; the 4 that exit 1 by design (8x8/2if reported, as-built): `rows_tiers --terms`, `flip --check`, `--point 8x8/2if`, `--design as-built` | `lane-summary.txt`, `lane-*.txt` |
| Harness self-test | 0 failures; 246 mutants caught, 0 escaped | `lane-harness_selftest.summary.txt` |
| `flip_grade.py --check --point 1x1/1if` | PASS (txL 48.09/49, R4L 188.39/238, last 126.46/130) | `lane-flip_check_1x1.txt` |
| rows_tiers, flip and load self-tests; `load_grade.py --check` | 971/971, 555/555, 25/25; 0.513 and 0.509 | `lane-*.txt` |
| `tier_grid.py --point 1x1/1if` | exit 0, 18 of 420, the built design | `lane-tier_grid.txt` |
| em-dash, idioms, docs, diff checks (11 bases incl. `dd01b0af`), `ctrl_hot` | 0 | `lane-*.txt` |
| BDD; `make twin`, `make twin-plants` | pass; 0 findings, every plant refused | `lane-behave.summary.txt`, `lane-twin*.summary.txt` |
| Lane parts b and c (builder tests, NVM self-test, boot 1x1, 8x8, native, plants) | 0 | `lane-*.summary.txt` |
| Harness legs at 1x1 (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`) | exit 0; the plant control C-R1 caught | `harness-head-builds.txt` |
| Harness legs at 8x8/2if | four groups exit 0; `srp` exits 1 on #910's build of one (138,054 and 147,814 against 121,500) | the same |
| Harness legs at 8x8-1if | exit 1, reported (lane 894b's point) | the same |
| Join intervals, every leg | 57 in 14 group runs (54 in 13 unplanted), 185.485 to 190.040 ms within 181.0 to 239.0; 195 run-outs, 126 released, 69 empty, 0 late, absent or unresolved | the same |
| Measured inputs from the pass's legs | the record 91,625 (965 us; 975 stated) at 1x1/1if, 156,716 (1,650) at 8x8; the long notice 34,370 (365); poll items within their stated costs at 1x1 and 8x8 | `receipts/model/measured-inputs-final-pass.txt` |
| Datapath events from the pass's `datapath-events` legs | 1x1/1if 30.55, 31.57, 25.51 us (35, 35, 30 stated); 8x8/2if 35.76, 32.79, 22.65 (40, 40, 25) | `receipts/model/event-costs-final-pass.txt` |
| Every image at the head (`qall.sh`) | within its caps; rom equal to round 8's or 8 B smaller; sram and tiles equal | `receipts/images/every-image-final.txt` |

## 8. Run history

- 03:46 CET: start; read the ruling, both reports.
- 03:46-03:58: item 1 (generator constants, direct index); core arm: only the old slot-sharing test fails (its key is outside the domain); the definition test passes.
- 03:58-04:10: item 2 tests and the KEYS arm; work arm 6/6; KEYS arm 7 of 7 geometries (147 s); R838-3's probe at the tree: rc 0.
- 04:11-04:13: the 32 plants on aecp_maps.c and THE PACE, two units (88-95, 72-79): all caught. Images at the working tree; F3 reconciled from round 8's ELFs.
- 04:14: commits `f0611e7f`, `58e6b60f`; 04:15: clone `r9/rgh`; legs L1L (88-95), L8L (72-79), 81L (64-71) launched.
- 04:18-04:19: L1L rc 0 but its record 98,720 (1,040 us by the rule); L8L 146,010; 81L rc 1 (reported). At 1,040 us P 9 is the smallest, the flip check passes, but `tier_grid.py` exits 1: the every-command load 0.705 > 0.70.
- 04:19-04:23: the layout experiment (scratch clone `r9/rgh-pad`, the table floored at 256, leg pad-L1L on 88-95): 91,625. Decision: the floor (the index unchanged), 975 kept; P 9 edits reverted.
- 04:23-04:44: floor rebuilt (core 13/13, work 4/4, KEYS 7/7, 32 plants caught, images); commit `992e52a0`; docs; commit `5cfa32c2`; docs check 0, em-dash 0; tier grid 2 of 420, flip check PASS.
- 04:42-04:45: firmware suite pre-check at `5cfa32c2` on a clean clone (unit, 88-95): PASS, the eight work arms among its arms.
- 04:45: #894, #908 and #902 had no comment after the ruling; `dev-soft-core` still `cec88385`; #810's branch gone from the remote (merged).
- 04:46: the full pass at `5cfa32c2`: sweep `894-r9g` shards on 0-7, 8-15, 16-23, 24-31 (taskset checked); dispatchers: 18 workflow and lane lines on 32-63 (MAX 4), 15 legs on 64-79,88-95 (MAX 6). Round 8's same-named unit files archived to `units-r8-final` first.
- 04:52: H-L1L at `5cfa32c2`: 91,625 / 83,716 / 75,892 / 75,481 / 23,883, as the experiment; no pass over THE SHARE (heaviest 149,490).
- 05:03-05:13: every leg ended at its expected exit (8x8 `srp`, 8x8-1if legs 1, reported); W-fw-aecp, W-fw-srp, W-fw-boundary rc 0. The measured inputs: H-L8L's record 156,716 cycles, 1,650 us by the rule, over 8x8's stated 1,555.
- 05:13: legs dispatcher done; the workflow dispatcher stopped and its 11 unstarted lines re-spread on 64-79,88-95 (MAX 4).
- 05:14-05:16: the 8x8 restatement; rows_tiers 971/971, flip 555/555, `--terms` exit 1 (8x8/2if); commit `88ed7082`; py idiom, docs check, em-dash 0 over 26 pages, diff check 0.
- 05:16-05:17: the pre-check pass at `5cfa32c2` stopped, its twelve units listed then stopped one by one (dispatcher first); outputs archived to `r9/precheck-5cfa32c2`, unit files to `units-r9-precheck`; its clones removed.
- 05:18: a pass at `88ed7082`: sweep `894-r9h` on 0-7, 8-15, 16-23, 24-31; workflow and lane lines on 32-63 (MAX 4); legs on 64-95 (MAX 6). 05:44: legs done (H-L1L 91,625 and H-L8L 156,716, as stated); unstarted workflow lines re-spread on 64-95.
- 05:46-05:53: the datapath events checked against `DATAPATH_US` with `eventcost.py`: AMAP_LIVE_WRITE over at 1x1/1if (25.51 us; 25.32 at round 8's head). Its provenance reproduced on the earlier heads' legs (23.33 exactly). At 30 us P 7 fails txL (49.69), P 8 holds; grid 18 of 420.
- 05:49: the pass at `88ed7082` stopped, its twelve units listed then stopped one by one, archived to `r9/stopped-88ed7082` and `units-r9-stopped` (W-fw-aecp, -srp, -boundary, -control and every leg had ended at their expected exits; lane part a's first 23 gates 0).
- 05:50-05:52: commits `1f47c09c` (AMAP 30 us, THE PACE 8 ms), `5b264bf2` (docs); docs check 0, em-dash 0 over 26 pages, idioms 0, diff check 0; model self-tests and checks as above.
- 05:52-06:01: pre-checks at `5b264bf2` (above). #894 had two new comments, lane 894b's STOP (6871307898) and its ruling (6871343905): none applies to this round's items; (c) has lane 894b take the shape header as the direct index's single source after #902 merges. `dev-soft-core` still `cec88385`.
- 06:02: **the final pass at `5b264bf2`**: sweep `894-r9i` on 0-7, 8-15, 16-23, 24-31 (taskset checked); 18 workflow and lane lines on 32-63 (MAX 4); 15 legs on 64-95 (MAX 6).
- 06:28: every leg at its expected exit (H-L1L 91,625, H-L8L 156,716; every input within its stated cost); unstarted workflow lines re-spread on 64-95; 06:39 split again (LiteX elaboration on 32-63, the rest on 64-95, MAX 2 each).
- 06:56-07:14: the sweep's four shards exit 0; the last unit (`W-fw-verilator`) rc 0 at 07:14.
- 07:15-07:27: `collect.sh` (verify: 139 run, 226 not run, 0 bad), receipts, PR body, comment, index; #894, #902 and #908 had no new comment, `dev-soft-core` still `cec88385`.
- 07:28: REVIEW READY posted (issuecomment-6872978311), the round's one comment.
