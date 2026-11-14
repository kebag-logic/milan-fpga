[A773] REVIEW READY
Commit: 5b264bf26416108add32d7fe5abca5252ffde2cb (the delta from `dd01b0af` to `5b264bf2`, seven commits; PR #902, `894-tiers` -> `dev-soft-core`, still `cec88385`)

Round 9, under #894's ruling of 2026-11-14 (issuecomment-6870437042), answering R838-3 (PR #902 issuecomment-6870395150) and R837-3 (issuecomment-6870427229).

Changed:
- **Item 1, the direct index** (`f0611e7f`). `aecp_maps.c` puts each map-edit key at its position in the port's key domain: stream or cluster x the most channels one has + channel. The domain comes from the build's shape constants, which `aecp_shape.key_domain` reads from the image's descriptors (`AECP_ENTITY_KEY_*`).
  - It is injective by construction, so the #904 bound holds at every geometry the builder accepts.
  - A `_Static_assert` holds the table to the whole domain.
  - The geometry's range refusal runs first. A key outside the domain takes the same turn, BAD_ARGUMENTS before its port is read, and never forms an index. No product state reaches it.
  - The definition test is byte-identical and passes.
- **Item 2, the controls** (`58e6b60f`).
  - `Core.EveryAcceptedMapKeyIsItsOwn` adds and removes every accepted key in 63-mapping commands. The work arm runs it at the five checked-in configurations, at R838-3's 16 x 4 and at the builder's widest (16 talkers, up to 32 channels), each edit within 2 (n + R).
  - `Core.EveryKeyOfTheDomainIsItsOwn` and `Core.MapKeysOutsideTheDomainAreRefusedAtTheirTurn` cover the whole domain and its edge.
  - The 8/16/32/63 counts and the quadratic plants are kept. New plants: colliding indices (`map-index-channel-dropped`, `-stream-or-cluster-dropped`, `-stride-short`), the domain's edge (`map-domain-a-channel-wide`, `map-outside-row-looked-up`) and a table scan (`map-table-scanned`). Each is caught by its words.
  - R838-3's `probe_maps.py`, unchanged, exits 0: the 63-mapping ADD is 63 visits of 126 (it found 714), the REMOVE 315 of 378 (2,268).
- **Item 3, the fallback:** not needed. The direct index fits, and no image grows.
- **Item 4, the record** (`992e52a0`). The table keeps at least its former 256 slots.
  - With only the domain's 64 at 1x1/1if, the edit's stack frame moves 192 B, and the data cache takes the REMOVE of 63 from 91,625 to 98,720 cycles with the same code.
  - Restated, that would be 1,040 us. At AMAP_LIVE_WRITE's earlier 25 us the pace would then be 9 ms (txL 47.63, R4L 203.44), but the 1x1/1if load with every command the largest legal one would be 0.705, over 0.70, and `tier_grid.py` would hold no design.
  - At 256 slots the record is 91,625 cycles, 965 us by the rule, so 975 us stays as the larger.
- **Item 4 at 8x8** (`88ed7082`): the floored table's 8x8 record is 156,716 cycles (memory copies after the edit, the data cache again), 1,650 us by the rule, over the 1,555 stated, so 8x8/2if's stated record is 1,650 us, the larger kept. Its reported rows at the head (8 ms): R4L 195.74 ms within 238, txL 446.92 ms, over 49 as before.
- **Item 4, the datapath events and the pace** (`1f47c09c`, `5b264bf2`): AMAP_LIVE_WRITE's take and sinks measure 25.51 us at 1x1/1if (`eventcost.py`, the cut `DATAPATH_US` states; it reproduces the table's recorded 23.33 us at #810's merge), 30 us by the rule, over the 25 stated. It was 25.32 at round 8's head already. Restated at 30 us, txL is 49.69 ms at 7 ms, so THE PACE is 8 ms (`AECP_PACE_MS 8u`), the smallest that holds.
- **Item 5, docs** (`5cfa32c2`, `5b264bf2`):
  - R837-3-2 and R838-3-F2: 238 and 49 ms in the harness README and section 13, the pace rule with its R4L condition, the head's loads (0.792 / 0.752 at 8x8/2if, 0.513 / 0.509 at 1x1/1if), and the 30 ms rows cited to the ruling 6844175391.
  - Section 13 gains "The direct index"; the AECP README describes it.
  - R837-3-R1 is fixed in `long_notice.py`.
- **R838-3-F3, reconciled:** round 8's rewrite grew `.text` by 180 B in every image. `.rodata`'s 8-byte alignment made that +184 B of rom at the 1x1/1if fixture, whose start-head `.text` ended on a boundary, and +176 B at the other seven. Both endpoints stand; "every image +176 B" was wrong for that image and for the code's growth (`rom_layout.py` over both heads' ELFs).
- **R838-3-R1:** this comment and the PR body say "the delta from `dd01b0af` to `5b264bf2`".

Validation (the full pass at the head, once, each part on a clean clone, never piped):
- **The sweep** (4 shards, each its own clone and unit): exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures.
- **Every hosted job step** of rtl-fast, rtl, elaborate and docs, run locally (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`): 139 run, 226 not run with a reason, 0 bad. The firmware jobs: every step 0, the AECP campaign 273 of 273 caught (the 32 on the map file and THE PACE among them).
- **Lane gates:** 45 at 0; the four that exit 1 are the reported 8x8/2if and as-built checks, by design. They include the diff checks against eleven bases (`dd01b0af` among them), em-dash (0 over 26 pages), Python and C++ idioms, docs, `ctrl_hot`, `tier_grid.py --point 1x1/1if` (0), the self-tests (rows_tiers 971/971, flip 555/555, load 25/25, harness 0 failures with 246 mutants caught and 0 escaped), `load_grade.py --check` (0.513 / 0.509), builder tests, NVM, boot 1x1 / 8x8 / native / plants, BDD, the twin and its plants.
- **Harness legs at 1x1** (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`): exit 0, and the planted control C-R1 is caught.
  - `aecp-largest-notice`: the REMOVE of 63 is 91,625 cycles and the ADD 83,716; the refused edits 23,883 to 75,892; the heaviest pass 149,490, none over THE SHARE.
  - 8x8/2if: four groups exit 0, and `srp` exits 1 on #910's build of one (138,054 and 147,814 against 121,500). The 8x8-1if legs exit 1 (reported, lane 894b).
- **The join intervals, every leg:** 57 in 14 group runs (54 in the 13 unplanted), 185.485 to 190.040 ms within 181.0 to 239.0. Of 195 run-outs, 126 were released and 69 empty; none was late, absent or unresolved.
- **The measured inputs** from the pass's legs: the record 91,625 cycles at 1x1/1if (965 us, 975 stated) and 156,716 at 8x8 (1,650 stated). AMAP_LIVE_WRITE is 25.51 us (30 stated), and every other datapath event and poll item is within its stated cost at 1x1/1if and 8x8/2if.
- **Every image** within its cap (`qall.sh` at the head).
- **Before the pass** (units, clean clones at the head): the firmware suite PASS, the harness self-test 0 failures, and the 1x1 `aecp-largest-notice` and `srp` legs exit 0. Two earlier passes, at `5cfa32c2` and `88ed7082`, were stopped when their legs showed a stated input under its measurement (8x8's record; then AMAP_LIVE_WRITE). Their outputs are kept and their findings are restated above.

Acceptance criteria (1x1/1if, `flip_grade.py --check --point 1x1/1if`: RESULT PASS, every row by every source):
- **The rows:** R4 12.85 / 20; R4L 188.39 / 238; ACMP 28.44, ADP 26.83, MAAP 26.95 / 30; first 14.51 / 20; R5 72.91, R6 68.80 / 90; last 126.46 / 130; tx 29.86, txL 48.09 / 49.
- **The design:** the pace 8 ms, the smallest (7 ms gives txL 49.69); the slice 900 us (least margin +0.019); `tier_grid.py --point 1x1/1if` chooses the built design, 18 of 420 holding.
- **The loads:** 0.513 at the pin, 0.509 with tsn-c-stack#32 (0.70), and 0.692 with every command the largest legal one.
- **The images:** every one within its cap. Rom is round 8's or 8 B smaller; sram and tiles are equal. The 1x1/1if fixture has 16 B left in its block, and the 8x8/1if platform 1,872 B inside its 56.0.
- **No STOP trigger:** 8 ms holds; last 126.46 is within 140; no image is over its cap; the map commands' behaviour is unchanged (definition test byte-identical and passing); the collision case's pass is within THE SHARE at 1x1/1if (the refused collision and conflict edits' passes at most 93,813 of 200,000 cycles; the accepted REMOVE's 149,490).

Open risks/questions:
- **Round 8's 7 ms pace rested on an understated input** (AMAP_LIVE_WRITE, above), now restated. Every measured input from the final pass's legs is within its stated cost at 1x1/1if and 8x8/2if.
- **The direct index's constants come from the entity generator.** When lane 894b merges #902, its shape header becomes their single source (ruling 6871343905, (c)).
- **The table's floor is a layout choice backed by measurement**, as above: the 64-slot table measured 98,720 cycles and the floored one 91,625, the same code. A later change to the edit's frame or the data near it can move the record. Each full pass's `aecp-largest-notice` legs re-measure it.
- **Unchanged duties:** 8x8/1if is lane 894b's; 8x8/2if stays reported (#910); #908 stays open by its own terms; S12b's wire capture is owed.
