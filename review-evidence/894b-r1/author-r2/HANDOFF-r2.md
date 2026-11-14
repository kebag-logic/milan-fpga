# 894b-a781 round 2: HANDOFF (phase B on top, phase A below)

## PHASE B (started 07:24 CET 2026-11-14)

**Status: REVIEW READY at `184d47cacc0b4eccb923cfbd4f2df9c3a05f5638`** (comment text `REVIEW-READY-COMMENT.md`; posted
on #894 once, as issuecomment-6877989263). Start head `bc8acc76` (phase A). Authority: #894 issuecomment-6871343905 (the round 2
ruling), #902's bounds (issuecomment-6867990126: MRPDU 49 ms, paced R4L 238 ms, the harness join gate 181.0 to
239.0 ms), round 9's ruling issuecomment-6870437042 (the direct-index map table). #902 open at `5b264bf2`
(origin/894-tiers), not merged at the start.

### B0. Exit

- **Head `184d47ca`**, five commits and two sync merges on phase A's `bc8acc76`: `219ea7ed` (merge `5b264bf2`), `6122db33`
  (the key domain's single source), `15b36a9c` (a line wrap), `7e3daf54` (the restatement), `105e3aa9` (docs),
  `184d47ca` (merge `7398ec0a`, origin/894-tiers having moved). Nothing pushed; #902 still OPEN at `7398ec0a`.
- **No STOP trigger:** the platform image at 8x8/1if 56.0; no slice stated over 1,600 us (1,475); every 1x1 and 8x8/2if
  image byte-identical to `5b264bf2`'s and `7398ec0a`'s; every CPU-decided row within its bound; the load 0.709 of 0.75.
- **The measurement (once, B3):** RESULT PASS; the seven held-egress rows the only budget misses, each under round 1's
  figure; joins 186.687 to 190.705 ms; the first queued notice 2.259, the last 23.730, the largest command 2.442 ms.
- **Restated (B3):** `CTRL_LOOP_SRP_UNIT_US` 345 (unchanged); the 8x8/1if polls' base 235, walk 50, long notice 320 (the
  rest unchanged).
- **Left for a decision:** THE RETRY's cold cost at 8x8/1if (`AECP_ROUND_COLD_US` keyed on `MBX_N_IF`, 85 us stated,
  about 125 us measured; 1,654 STATED rounds in the `answering-every-port` arm, no row or slice affected). Keying it on
  the shape changes the 8x8/1if image and its rounds, outside the ruling's items. Also 1x1/1if's SRP unit, as before.
- **The full pass at `184d47ca`** (B6): the sweep 65 suites, 2,713,040 checks, 0 failures; every hosted job step 139
  run, 226 not run with a reason, 0 bad; the lane gates 49 at 0 and the 4 that exit 1 by design; the legs as #902's.
  Two host resets cut it (11:2x and 12:2x); B7 says what was run again.

### B1. Sync: the merge of origin/894-tiers at 5b264bf2

Merge commit `219ea7ed14c715b79007ba8cc748083ccadd06c4` (parents `bc8acc76`, `5b264bf2`), one merge. Merge base
`8a3791e4`; 16 commits on #902's side, 7 on this branch's; 17 files touched by both, 12 auto-merged, 5 conflicted:

| File | Conflict | Resolution |
|---|---|---|
| `tb/verilator/ctrl_service_budget/mrpdu_grade.py` | the import (`built_value` here, `tx_budget_ms` there) and the constants (`BUDGET_MS` + `LOOK_MS` here; `LATE_MS`, `OUTCOMES`, `FAILING` there) | one reader: `LATE_MS = tx_budget_ms(ctrl_loop.h)` (#902's), `BUDGET_MS = LATE_MS` (the row's budget, ruling (b)(i)), so the bound is read once, 49 ms; `OUTCOMES`, `FAILING` kept; `LOOK_MS` dropped (#902 removed the horizon, nothing else reads it). Both names stay because each has its own plant (`BUDGET_MS + 1`, `LATE_MS 10**6`) |
| `sw/firmware/ctrl/test/ctrl_configs.py` | the boundary gate's `OUTSIDE` entries | #902's three (`paced_rows.py`, `join_grade.py`, `mrpdu_grade.py`, its words) and this branch's `selftest_notice.py` |
| `docs/reference/FR_NFR.md` (3.4.1, the SRP/MRP row) | the row's text | #902's (49 ms, `T_egress`, 281 ms, 950 to 1050 ms) with this branch's sentence on the harness budget (`CTRL_LOOP_TX_BOUND_MS`, ruling (b)(i)) in place of "against T_svc's 20 ms" |
| `sw/firmware/ctrl/aecp/README.md` | the pending-notices paragraph | this branch's lead (each kept in its descriptor's event; the count by shape) and #902's bounds (130 ms at 1x1/1if with its amendment link, `queued_bound.py`) |
| `sw/firmware/ctrl/srp/README.md` | two lines | this branch's slice line (one build at every point, 1,475/1,795 at 8x8/1if, THE SHAPES) and #902's bound line (49 ms, `T_egress`) |

Auto-merged and checked: `ctrl_loop.h` (THE SHAPES with #902's `CTRL_LOOP_T_EGRESS_MS` and derived
`CTRL_LOOP_TX_BOUND_MS`), `selftest_notice.py` (`header_bound` expands `CTRL_LOOP_T_EGRESS_MS`), `notice_window.py`,
`run.py`, `selftest_mutants.py`, `load_grade.py`, `flip_grade.py`, `rows_tiers.py`, `aecp_arms.py`, `test_aecp.cpp`,
SPLIT_CONTROL_MEMORY.md, the harness README. Quick gates on the merged tree before the commit: `shape_costs.py --check
--selftest` PASS; flip at 1x1/1if rc 0, at 8x8/1if rc 0 (load 0.710 of 0.75), at 8x8/2if rc 1 as reported.

**The single source for round 9's direct-index table:** a follow-up commit (B4).

**The second sync merge (origin/894-tiers moved past 5b264bf2 during the round).** At 10:05, after the measurement,
origin/894-tiers was `7398ec0a` (#902 still OPEN), three commits on `5b264bf2`: `55b8e621` (`aecp_maps.c`: the table's
declared slots held at compile time to every position `place()` forms, `MAP_DOMAIN`, `MAP_FLOOR`, the same
`MAP_SLOTS`; a build-row plant `map-table-each-direction-alone` in `aecp_map_mutants.py`/`aecp_mutants.py`), `947bd389`
and `7398ec0a` (docs, `aecp_arms.py`'s comment). Merged with one merge commit, `184d47cacc0b4eccb923cfbd4f2df9c3a05f5638`
(parents `105e3aa9`, `7398ec0a`), **no conflict**; every one of the AECP campaign's 275 plant anchors occurs exactly
once in the merged sources. The instruction is to merge again before measuring: the measurement had already run, so it
is carried by image identity instead: at `184d47ca` both 8x8/1if images (fixture and platform) are byte-identical to
the measured head `6122db33`'s, and the six fixed images to `7398ec0a`'s, which equal `5b264bf2`'s (B2).

### B2. Byte-identity against 5b264bf2

Base: qimg.sh on a clean clone of `5b264bf2` (`receipts/images/raw-b-902-5b264bf2.txt`). Checked with
`scripts/img_check_base.py` (phase A's `img_check.py` with the base named):

| When | Tree | Result | Receipt |
|---|---|---|---|
| after the merge and the key domain's single source | `6122db33` (the worktree, committed) | the six fixed images identical, ELF and loadable; platform-8x8-1if 56.0 (rom 129,200, sram 97,264, the same as 5b264bf2's 8x8/1if) | `img-b1-6122db33-vs-5b264bf2.txt` |
| restatement and docs | `105e3aa9` (clean clone) | the six fixed identical to 5b264bf2's; both 8x8/1if ELFs identical to the measured `6122db33`'s; 56.0 | `raw-b-105e3aa9.txt` |
| #902's new head | `7398ec0a` (clean clone) | its six fixed images identical to 5b264bf2's | `raw-b-902-7398ec0a.txt` |
| **the final head** | `184d47ca` (clean clone) | **the six fixed identical to 7398ec0a's (so to 5b264bf2's); both 8x8/1if ELFs identical to the measured 6122db33's; platform-8x8-1if 56.0** | `img-b2-184d47ca-vs-7398ec0a.txt`, `raw-b-184d47ca.txt` |

### B3. The measurement at 8x8/1if

At `6122db33` on clean clone `mB`, the built image at 1,475 us (its ELF identical to the worktree's, B2), the
contract-rate run: arm A every group (B-A0..B-A3, 95 groups), the `answering-every-port` arm (B-AE, 16 groups: the
queued notices), the `answering-ports` arm's `aecp-largest-notice` (B-AL: the largest legal command, the paced R4L row
as measured). Graded by `scripts/gate_b.py`; the figures restated by `scripts/restate.py`.

**Final (every leg done; `receipts/harness/gate-8x8-1if-6122db33.txt`): RESULT PASS.** 112 groups, 1,680 instances, all
measured. Each leg's exit: B-A0..B-A3 rc 0, B-AL rc 0, B-AE rc 1 (only the STATED round lines below).

| Row (bound, ms) | Worst, ms | Instance |
|---|---:|---|
| AECP (20) | 4.693 | `notice-every-7.held.aecp.if0` |
| ACMP (30) | 6.813 | `notice-every-6.held.acmp.if0` |
| ADP (30) | 5.522; ENTITY_AVAILABLE 4.413 | `notice-burst-6`; `backlog-adp@program-aged2-7` |
| MAAP (30) | 6.020 | `notice-every-0.held.maap.if0` |
| SRP (90) | 10.284 | `notice-every-6.held.srp.if0` |
| MRPDU (49) | 3.578 | `save-starved.mrpdu.periodic.if0` |
| AECP's notices (20) | 0.624 | `aecp-fanout`, SET_NAME |
| first queued notice (20) | 2.259 | `notice-burst-4` |
| last queued notice (130) | 23.730 | `notice-burst-1` (40 queued) |
| largest legal command, paced R4L (238) | 2.442 | `aecp_long.refused.collision_values.if0` |

- Budget misses: 7, exactly the seven held-egress rows, each under round 1's ledger figure (63.083 / 63.305 / 63.526 /
  63.747 / 63.969 / 62.025 / 61.680 ms against 63.24 ... 61.83); 0 new.
- Joins: 346 in 111 groups, 186.687 to 190.705 ms (gate 181.0 to 239.0); MRP run-outs 1,332 released, 979 empty, none
  late, absent or unresolved.
- Slices against 147,500: SRP's 146,052 (`backlog-adp@blank-aged2-1`), the build 137,924 (`srp`), THE RETRY's round
  109,745. Passes given whole: build-one 137,924 of 147,500, step 81,053 of 97,500. THE SHARE: only
  `aecp-largest-notice`'s two passes (213,816), reported at 8x8/1if as before.
- Load: 0.709 at the pin, 0.670 with tsn-c-stack#32 (0.75), with the restated polls (`receipts/model/load-8x8-1if-phaseB.txt`).
- Restated (`receipts/model/restate-8x8-1if-6122db33.txt`): `CTRL_LOOP_SRP_UNIT_US` 345 (heaviest `srp_mbx:receive`
  32,421 cycles: unchanged, so no image moves); EIGHT_ONE base 235 (21,995; was 240), withdraw 110 (10,317), rebuild 590
  (55,813), walk 50 (4,701; was 55), reclaim 30 (2,604), acmp 75 (6,813), acmp_declined 30 (2,542), aecp 140 (13,297,
  the every-port arm: the phase A concern did not materialise), aecp_long 320 (30,097; was 315), retained 345.
- Rows by every source, re-derived with 40 notices and the shape's polls (reported, owed to #872;
  `receipts/model/rows-8x8-1if-phaseB.txt`): R4 18.56, R5 113.87, R6 108.72, first 16.99, last 266.70, R4L 192.83,
  ACMP 45.48, ADP 44.77, MAAP 46.18, tx 58.53, txL 146.97 ms; the every-command-largest load 0.991.

**Interim notes (kept):**
- B-AL: rc 0, 0 budget misses (5 instances), joins 187.440 to 190.006 ms; the largest legal command's rows at most
  2.442 ms (238); the long notice's poll item 30,097 cycles (stated 315 us; restated 320). Two passes over THE SHARE
  (213,816 cycles; round 1 209,290), reported at 8x8/1if as before.
- B-AE: 0 budget misses (728 instances); the queued notices: the first at most 2.259 ms (20), the last at most
  23.730 ms (130), 640 in 16 groups, 40 a group; joins 188.15 to 190.02 ms; slices within 147,500 (SRP's 122,906, the
  build 114,754, THE RETRY's round 109,745). **Exit 1 on 1,654 STATED lines of one kind: THE RETRY's rounds of no
  notice beside 1, 2 or 4 refused attempts over their stated cost** (11,900 / 15,300 / 22,100 cycles; the dearest
  12,547 / 19,326 / 23,343), i.e. the round's cold cost: `AECP_ROUND_COLD_US` and `AECP_ATTEMPT_US` are keyed on
  `MBX_N_IF` (`aecp_mbx.h:29`, `aecp.h:60`), so 8x8/1if takes the 1x1's 85 us; measured about 125 us (19,326 less two
  attempts' 6,800). At the 8x8 shape's two-interface cost (185 us) every one is within. No round with a notice is
  over. Round 1's arm A had none (the arm could not build at 8x8/1if before (iv)). See B0 for the disposition.
- The transmit-aged control at 8x8/1if (B-CTA): caught, 8 of 8 groups' timer-driven MRPDU over 49 ms (66.505 to
  67.015 ms), every group's joins past the gate, 15 run-outs late each (`receipts/harness/control-transmit-aged-8x8-1if-6122db33.txt`).

### B4. Changes after the merge, with file:line and reason

**`6122db33`: the shape header as the single source of round 9's direct-index table** (ruling (c); #902's REVIEW READY
issuecomment-6872978311 names it as this lane's at the merge). #902 sized the table from `AECP_ENTITY_KEY_*`, which
`aecp_shape.key_domain` writes into `aecp_entity_gen.h` from the image's descriptors; the shape header (`srp_entity_gen.h`)
already stated the build's shape (THE SHAPES' streams, the notice-bearing descriptors). Now:
- `sw/firmware/ctrl/srp/srp_entity.py:3-8` (docstring), `:16` (imports `aecp_shape`), `:24-41` (`emit`, the blob at `:32`, the lines at `:41`): the shape
  header states `AECP_ENTITY_KEY_STREAMS`, `_STREAM_CHANNELS`, `_CLUSTERS`, `_CLUSTER_CHANNELS`, by `aecp_shape.key_domain`
  of the builder's own AEM image (`_entity_model_image`, the bytes `aecp_entity.py` renders). Why: one derivation, one
  header in every unit an image compiles (the builders force-include it first).
- `sw/firmware/ctrl/aecp/aecp_shape.py:103-106`: `aecp_entity_gen.h` states the key domain only under
  `#ifndef CTRL_SRP_ENTITY_H`, for a compile given no shape header (the host arms: core, work, the key arms at the five
  configurations and the 16x4 and 16x32 geometries, which compose no SRP and would hit THE SHAPES' `#error` with one).
  Why: an image reads one source; a host arm reads the same derivation.
- `sw/firmware/ctrl/aecp/aecp_maps.c:5,142-146`: comments only (where the domain comes from). No image byte moved (B2).
- `tb/verilator/ctrl_service_budget/shape_costs.py`: `KEY_DOMAIN`, `KEY_GUARD` (`:64-66`), `aecp_header_of` (`:183`), `key_domain`
  (`:192`), `key_findings` (`:197`), called from `findings` (`:311`); `key_controls` (`:420`) and three `CONTROLS` (21 now). Why: the single source
  held by a check with plants (B5).
- `sw/firmware/ctrl/test/ctrl_configs.py:268-271`: `shape_costs.py`'s boundary entry names the two headers it reads.
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 "Where the shape is stated": the key domain and its single source.

### B5. New checks, planted mutants and failing words

| Check | Plant | Failing words |
|---|---|---|
| The shape header states the key domain (`shape_costs.key_findings`, in `--check`, `--selftest` and the harness self-test's table checks) | `the shape header not stating the map edits' key domain` (its four lines dropped) | "1x1/1if: the shape header does not state AECP_ENTITY_KEY_STREAMS, ..., the map edits' key domain" |
| `aecp_entity_gen.h` states it only with no shape header | `aecp_entity_gen.h stating the key domain beside the shape header` (the guard dropped) | "1x1/1if: aecp_entity_gen.h states AECP_ENTITY_KEY_STREAMS, ... outside #ifndef CTRL_SRP_ENTITY_H, beside the shape header" |
| The two are the same derivation | `the shape header's key domain not the image's` (8x8's streams 2) | "8x8/1if: the shape header states AECP_ENTITY_KEY_STREAMS 2, not the image's 9" |
| An image's table reads the shape header (firmware, ad hoc on a clone) | the shape header's `AECP_ENTITY_KEY_STREAMS` 64 with `aecp_entity_gen.h` unchanged | every image's ELF changes, 8 of 8 (`receipts/images/plant-key-domain-wider-6122db33.txt`) |

Receipts: `receipts/model/key-domain-plants-6122db33.txt` (each plant's findings); `shape_costs.py --check --selftest`
at `6122db33`: PASS, 21 of 21 controls refused.

### B6. Gate table (phase B)

The full pass at the final head `184d47ca`, once, each part on its own clean clone, never piped: the sweep as four shard
units (`native-shards.py`, label `894b-r2b`); every hosted job step of rtl-fast, rtl, elaborate and docs (`run_wf.py`,
then `verify_wf.py`); the lane gates' three parts (`lane_gates.sh`, phase B's bases added); the harness legs at 1x1 and
8x8/2if as #902's pass runs them (`mkqueueB.sh`; 8x8/1if is the measurement's, B3); every image. Launched by
`launchB.py` (a unit on this session's CPUs that only polls and launches): every unit on an 8-wide range of 0-95 free
by the shared picker's busy set at that moment, checked right before each launch; the sweep first.

| Gate | Where | Result |
|---|---|---|
| Harness self-test | `6122db33`, clean clone | 0 failures, 872 checks, 257 mutants caught, 0 escaped (`receipts/harness/harness-selftest-6122db33.txt`) |
| Quick gates (table, flip x3, load, rows_tiers, tier_grid, docs, em-dash, idioms, diff, ctrl_hot) | `6122db33`; `184d47ca`, clean clones | as expected at both but the Python idiom gate at `6122db33` (fixed in `15b36a9c`); all as expected at `184d47ca` (`receipts/gates/`) |
| Images | `5b264bf2`, `6122db33`, `105e3aa9`, `7398ec0a`, `184d47ca` | the six fixed identical throughout; 8x8/1if 56.0 and identical to the measured head's (B2) |
| The key-domain plant on the firmware | `6122db33` + plant | caught, 8 of 8 images changed |
| The 8x8/1if measurement and the transmit-aged control | `6122db33` | B3 |
| **The sweep, 4 shards** (`894b-r2b`; CPUs 8-15, 32-39, 40-47, 48-55) | `184d47ca` | exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures (`receipts/gates/sweep-shard{0..3}-184d47ca.txt`) |
| **Every hosted job step** of rtl-fast, rtl, elaborate, docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`) | `184d47ca` | 139 run, 226 not run with a reason, 0 bad (`receipts/gates/workflows-verify-184d47ca.md`) |
| Firmware jobs (unit, control, AECP, SRP campaigns, boundary, Verilator) | `184d47ca` | every step 0; campaigns 716, 275 and 345 caught, 0 escaped (`notice-dropped-with-its-descriptors-next`, `map-table-each-direction-alone` among them); boundary PASS; coverage 39 files (`receipts/firmware/firmware-jobs-184d47ca.txt`) |
| Lane gates, parts a, b, c | `184d47ca` | 49 at 0; `rows_tiers --terms`, `flip --check`, `--point 1x1/1if --design as-built`, `--point 8x8/2if` exit 1 by design. Harness self-test 0 failures, 872 checks, 257 caught, 0 escaped; rows_tiers 971/971, flip 578/578, load 25/25; load 0.513/0.509; tier_grid exit 0; table 21/21; flip 8x8/1if PASS (0.709), 1x1/1if PASS; 13 diff-check bases; em-dash, idioms, docs, ctrl_hot, BDD, twin and plants, builder, NVM, boot x4 (`receipts/gates/lane-gates-184d47ca.txt`) |
| Harness legs at 1x1 and 8x8/2if | `184d47ca` | exit 0 but `srp` at 8x8/2if (#910's build of one, 138,054 and 147,814 against 121,500, as #902 reports); C-R1 caught; 48 joins in 11 group runs, 185.485 to 190.040 ms; 172 run-outs, none late, absent or unresolved (`receipts/harness/legs-1x1-8x8-184d47ca.txt`) |
| Every image (the pass's Q-img) | `184d47ca` | identical to `7398ec0a`'s, 8x8/1if 56.0 (`receipts/images/img-b3-fullpass-184d47ca.txt`) |

Two environment notes, neither a code change: docs-gates-1's builder leg (`test_builder.py --require-rv32`) first failed
because `run_wf.py`'s sandbox HOME lacked the RV32 SDK the hosted job provisions at `~/br-milan-rv32` (#902's sandbox home
has that link); the link was added and the job run again whole on a fresh clone, failed 0. docs-check-no-git strips
`.git` by design, so the driver's post-run `git status` fails after its steps, every one rc 0, as in #902's pass.

### B7. Run history (phase B)

- 07:24 CET: start. Fetched: origin/894-tiers `5b264bf2`, #902 OPEN (not merged), origin/dev-soft-core `cec88385`.
  The round 2 ruling re-fetched, identical to `A10-RULING.md`. Merge base of the branch and 894-tiers `8a3791e4`;
  16 commits on #902's side, 7 on this branch's; 17 files touched by both.
- 07:26: baseline images at `5b264bf2` on a clean clone (unit on this session's CPUs). 07:31: the merge, 5 conflicts
  (B1), committed `219ea7ed`. Quick gates on the merged tree pass.
- 07:34: the key domain's single source (B4); images identical to 5b264bf2's but 8x8/1if (56.0); committed `6122db33`.
  origin/894-tiers rechecked: still `5b264bf2`, #902 OPEN.
- 07:37: measurement clone `mB` at `6122db33`. Units (each MemoryMax 10G), CPUs by `cpu_ranges.py pick` checked before
  each launch: B-A0 32-39, B-A1 24-31, B-A2 16-23, B-A3 8-15 (arm A, every group, 95 in four parts balanced by simulated
  time, `scripts/legB.py`), B-AE 0-7 (the answering-every-port arm, 16 groups); the picker then had no free range, so
  B-AL (the answering-ports arm's `aecp-largest-notice`, one job) runs on this session's CPUs 96-127. Each build took
  under a minute.
- 07:38: harness self-test (B-st) on clean clone `hB` at `6122db33` (session CPUs). The wider-key-domain plant built on
  clone `pK`: 8 of 8 images changed. 07:41: B-AL done, rc 0. Quick gates on clean clone `qB`: every gate as expected but
  the Python idiom gate (one line of 121 columns in `shape_costs.py`'s new plant); wrapped, committed `15b36a9c` (07:45).
- 07:55: B-st done: 0 failures, 872 checks, 257 mutants caught, 0 escaped. 07:47-07:59: B-CTA (the
  transmit-aged control, session CPUs), caught. 08:22: B-AE done, rc 1 (THE RETRY's rounds, STATED; B3).

- 09:21-10:03: arm A done (B-A1..A3 09:14-09:19, B-A0 10:02 with `save-second`, the longest group); 09:3x a regrade of
  B-A0's 21 finished groups gave `backlog-owed` early. 10:03: the gate PASS; restatement and derived rows (B3).
- 10:0x: commits `7e3daf54` (the restatement: `poll_grade.EIGHT_ONE`, comments in `ctrl_loop.h`, `load_grade.py`,
  `build.py`'s plant comment) and `105e3aa9` (docs). Images at `105e3aa9`: identical as above.
- 10:05: origin/894-tiers found at `7398ec0a` (#902 OPEN): merged, no conflict, `184d47ca`; images at `7398ec0a` and at
  `184d47ca` on clean clones: identical (B2). Quick gates at `184d47ca`: as expected.
- 10:08-10:47: the shared picker had no free 8-wide range in 0-95 (every range held by two other lanes' legs and shards);
  polled. 10:47: `launchB.py` started (B-launch) to take ranges as they free, the sweep first.
- 10:5x-11:10: a release hold for #894 collected 8-15, 40-47, 64-79, 88-95 (the picker hands out nothing meanwhile).
  11:10:36: the sweep launched (`894b-r2b`, shards on 8-15, 16-23, 24-31, 32-39; each unit's affinity checked), then
  W-fw-verilator 88-95, lane-a 72-79, W-fw-control 64-71, W-fw-aecp 56-63, W-fw-srp 48-55, W-fw-unit 40-47.
- **About 11:19-11:59: the host was reset (a RAM fault), killing every unit of that first attempt** (its last write
  11:19:17; the launch log kept as scratch `fullB-killed/launch-1110.txt`). No part of it is evidence. Nothing had been
  posted, pushed or merged. 12:03: resumed; the tree clean at `184d47ca`, every commit in place, origin/894-tiers still
  `7398ec0a`, #902 OPEN; #894's round 10 ruling (issuecomment-6873298790) is #902's, at `7398ec0a`, already merged here.
- 12:04: the killed attempt's outputs and the four shard clones removed; the full pass relaunched from fresh clones
  (B-launch): the sweep on 8-15, 32-39, 40-47, 48-55 (affinity checked), then the queue (W-fw-verilator 88-95, lane-a
  80-87, W-fw-control 72-79, W-fw-aecp 64-71, W-fw-srp 56-63, ...).
- 12:19-12:23: firmware-verilator, firmware-aecp-mutants and firmware-srp-mutants ended, each whole on its own fresh
  clone at `184d47ca`, every step rc 0 (the AECP campaign 275 of 275 caught, `notice-dropped-with-its-descriptors-next`
  and #902's `map-table-each-direction-alone` among them; the SRP campaign 345 caught, 0 escaped).
- **About 12:25-12:29: the host was reset a second time**, killing the rest of the second attempt. 12:33: resumed;
  tree clean at `184d47ca`. The three jobs above are kept as the pass's (each completed at the final head on its own
  clean clone); every other part is run again from fresh clones.
- 12:34: relaunched (B-launch, queue capped at 4 at once to ease the host's memory): the sweep on 8-15, 32-39, 40-47,
  48-55 (affinity checked); lane-a 88-95, W-fw-control 80-87, W-fw-unit 72-79, W-fw-boundary 64-71, then the rest.
- 12:34-14:26: the pass ran to the end: sweep shards 13:41 (0, 3), 13:50 (1), 14:06 (2), exit 0 each; the jobs and lanes
  13:04-13:57; docs-gates-1 failed its builder leg on the sandbox HOME's missing SDK link: link added 13:40, the job
  run again (W-docs-gates-1b, 8-15) 13:41-13:59, failed 0; the legs 13:48-14:26; Q-img 14:18.
- 14:27: `verify_wf.py`: 0 bad. Receipts written; #894 rechecked: a new ruling (issuecomment-6876349104, 11:06) is for
  #902's lane (1x1/1if's AECP record at `7398ec0a`), not this one; origin/894-tiers still `7398ec0a`.
- 14:29: REVIEW READY posted on #894, issuecomment-6877989263 (identical to `REVIEW-READY-COMMENT.md`), the round's one
  comment. Nothing pushed; no PR created or edited; the only merges are the two sync merges. No unit of mine left
  running.
---

## PHASE A (done)

**Status: phase A done; stopped as assigned (no STOP trigger).** Head
`bc8acc76fc524c167aa47613e54968e66ff02a17`, two commits on round 1's STOP head `c9226ff3` (unpushed):
`86c3cf23c68894d964a559712dff1d40cb67f495` (code and tests) and `bc8acc76` (docs). Authority: #894
issuecomment-6871343905 (the round 2 ruling, text in `A10-RULING.md`). Phase A posts nothing, pushes nothing, merges
nothing. Started 05:00 CET 2026-11-14, ended 06:25. No STOP trigger met (section 6), so no STOP-COMMENT.md.

### 0. Exit

- **Done:** (i), the keying of (ii) and (iii), (iv)'s derivation, its sizing by shape with its proof and plants, and
  both notice arms built at 8x8/1if with their groups constructed (none run). Committed `86c3cf23`, `bc8acc76`.
- **STOP triggers, none met:** the platform image at 8x8/1if is 56.0 RAMB36 after every change (same rom and sram);
  no slice is stated over 1,600 us (the largest 1,475); every 1x1 image (1if, 2if) and every 8x8/2if image is
  byte-identical to `8a3791e4`'s, ELF and loadable bytes, at the head on a clean clone.
- **Verification at the head:** harness self-test 0 failures, 863 checks, 250 mutants caught, 0 escaped; the five
  firmware jobs (unit, control, AECP and SRP mutant shards, boundary) every step rc 0, the new plant caught in the
  AECP shard; the model, table and style gates as expected.
- **Not run (phase A is build and unit tests only):** any simulation leg, the sweep, the hosted RTL jobs
  (verilator-lint, split-cdc, firmware-verilator, yosys), the act replica. Phase B runs them.
- **Phase B:** section 5. Every provisional figure: section 4.

### 1. Items

| Item | What | State |
|---|---|---|
| (i) | MRPDU row's harness budget from `CTRL_LOOP_TX_BOUND_MS`, plant one over | done: `mrpdu_grade.BUDGET_MS` (50 at this head, 49 after #902 through the same reader) |
| (ii) | `CTRL_LOOP_SRP_UNIT_US` per shape | done: THE SHAPES table, 8x8/1if 345 us provisional; 1x1 250, two interfaces 365 |
| (iii) | poll costs per shape, load recomputed | done: `poll_grade.STATED_US` by shape, 8x8/1if provisional; load 0.710 / 0.670 |
| (iv) | 8x8/1if's most pending notices from its descriptors via the shape header | done: 40 > 12; sized by shape, proven none dropped with plants; both notice arms build at 8x8-1if, groups constructed |
| check | platform image at 8x8/1if <= 56.0 after each change; 1x1 and 8x8/2if byte-identical | done: 56.0 at every step; the six fixed images identical (section 6) |

### 2. Changes, with file:line and reason

**`86c3cf23`, code and tests:**
- **(i)** `tb/verilator/ctrl_service_budget/mrpdu_grade.py:28` `BUDGET_MS`: `CTRL_LOOP_TX_BOUND_MS` read from
  `ctrl_loop.h` by `tier1_rows.built_value`, the reader #902 round 8 extends to its `- CTRL_LOOP_T_EGRESS_MS` form (so
  the budget becomes 49 at the merge with no edit here). `:70` `wait_ms()` is the row's normative wait W bringing the
  family's budget, min(T_svc, srp ceiling) = 20, to `BUDGET_MS` (the idiom `notice_window` uses for the queued notices);
  `:99` the probe carries it, `:101` the row records it. Why: ruling (b)(i).
  - `selftest_notice.py:68` `header_bound()`: the bound evaluated from `ctrl_loop.h`'s text apart from mrpdu_grade's
    reader (every name expanded, `rows_grade.arithmetic`), so the check is not the reader checking itself. `:81`
    `timer_checks`: a row at the bound within it, one 1 ms over it a miss (were 19 and 21 ms against 20).
  - `sw/firmware/ctrl/test/ctrl_configs.py:249,251`: `mrpdu_grade.py` (in #902's own words, so the merge is trivial)
    and `selftest_notice.py` registered in the boundary gate's `OUTSIDE`, since both now name the firmware tree.
- **(ii)** `sw/firmware/ctrl/loop/ctrl_loop.h:286-295` (comment), `:310,315,320,325`: `CTRL_LOOP_SRP_UNIT_US` in each
  shape's block, 250 / 345 / 365 / 365; the ternary define removed. Why: ruling (b)(ii); 345 = 32,401 cycles x 1.05,
  rounded up to 5 us.
  - `shape_costs.py:42` `NAMES` takes it; `:242` a rule, the unit within its slice (ctrl_loop.c's `_Static_assert`);
    the report and the controls' block carry it.
- **(iii)** `poll_grade.py:90-106` `ONE`, `TWO`, `EIGHT_ONE`, `STATED_US` keyed by `shape_costs.Shape`; `:133`
  `stated_us` takes the shape (an int is the shipping streams' shape) and refuses an unlisted one. Why: ruling (b)(iii).
  - `load_grade.py:317`: at a NEAREST point (8x8/1if) the polls' base and items are the point's own shape's, not the
    nearest point's table; `:110-118` the comment. Load recomputed (section 4).
  - `shape_costs.py:262`: a listed shape whose polls `poll_grade.STATED_US` does not state is a finding.
- **(iv)** `sw/firmware/ctrl/srp/srp_entity.py:16,24,32`: the shape header also states `CTRL_AEM_STREAM_INPUTS`,
  `_STREAM_OUTPUTS`, `_AVB_INTERFACES`, `_CLOCK_DOMAINS` from the builder's own AEM overlay (`descriptor_counts`).
  - `sw/firmware/ctrl/aecp/aecp.h:65-81`: `AECP_NOTICES_HELD` = 2 x streams + 3 x AVB interfaces + clock domains (the
    shipping 1x1's with no shape header); `AECP_NOTICES_MOST` = it at one interface, 40 at two (unchanged there).
  - `sw/firmware/ctrl/aecp/aecp_mbx.c:8`: `_Static_assert(AECP_NOTICES_HELD <= AECP_NOTICES_MOST)`.
  - **Firmware check first (the ruling's words):** pending notices are kept one event a descriptor
    (`aecp_config.events`, `aecp.c` `aecp_changed`/`scan`), so no storage is sized by `AECP_NOTICES_MOST` and none is
    dropped at 40; the constant caps a round's take (`aecp_mbx.c` `retry`, `AECP_ROUND_FIRM_NOTICES` at one interface)
    and is the queue length the rows model and the arm count. 8x8/1if's descriptors: 9 + 9 streams x 2, 1 AVB
    interface x 3, 1 clock domain x 1 = 40, over 12, so it is sized by shape.
  - `sw/firmware/ctrl/test/test_aecp.cpp:3100` `Mailbox.EveryNoticeTheDescriptorsHoldIsKeptAndSentOnce`: every notice
    the descriptors hold is pending at once, `== AECP_NOTICES_MOST` at one interface, and each sent exactly once.
  - `sw/firmware/ctrl/test/aecp_arms.py:123`: that test and the bound test run at the 8x8 configuration at one
    interface in `all_arms` (firmware-unit).
  - `sw/firmware/ctrl/test/aecp_retry_mutants.py:239`: the campaign's plant `notice-dropped-with-its-descriptors-next`.
  - `notice_window.py:56` `KINDS` (the per-kind notices, shared); `:145` `notices_most(build)` at the build's shape
    through `shape_costs.notices_most` (was a regex on the `12u : 40u` ternary), `:155` the arm's check.
  - `shape_costs.py:154` `header_of` (cached), `:174` `evaluated`, `:201` `notices_most`, `:208` `notices_held`,
    `:268` `notice_findings`, `:374` `notice_controls`.
  - `load_grade.py:109`: 8x8/1if's `counter_descriptors` 18 -> 20 (round 1's typo: 18 streams + 1 AVB + 1 clock),
    now held to the shape header by `notice_findings`.
- **Self-test wiring:** `selftest_round.py:138,160` `polls_at_shape`; `selftest_mutants.py:77,501,503,794,796`.

**`bc8acc76`, docs:** FR_NFR.md 3.4.1 (the MRPDU harness budget; the 8x8/1if gate: no budget miss beyond the rows the
egress decides, recorded misses, the restated trigger; THE SHAPES with the SRP record and polls, provisional; the
notices); SPLIT_CONTROL_MEMORY.md section 13 "THE SHAPES and 8x8/1if" rewritten (table with the SRP record, the
notices, the provisional SRP record and polls, the load, the MRPDU budget, the ledger of the seven egress rows by name,
1x1/1if's unit finding, what is owed after #902); the harness, AECP and SRP READMEs.

### 2b. Interpretations made (public in PR-BODY.md where they matter)

- **"The measurement" for `CTRL_LOOP_SRP_UNIT_US`** is the heaviest SRP record handler, `srp_mbx:receive`, as 8x8/2if's
  365 us was (34,361 cycles + 5 %, section 13's record-cut paragraph), not the slice overrun round 1 inferred (about
  337 us with the loop's take before the handler).
- **`rows_grade.py` is untouched** (the assignment allows only keying its slice and build costs, round 1's). Its
  `costs()` still reads the withdrawal, rebuild and notice items at the interface count, and its `header()` takes
  `AECP_NOTICES_MOST`'s no-shape-header default (12). Neither reaches a held row: its points are 1x1/1if and 8x8/2if,
  and 8x8/1if's rows by every source are reported, not computed by the flip check. Phase B's report of them must take
  40 notices and the shape's polls.
- **"The queued-notice and R4L harness arm"** is read as the `answering-every-port` arm (the queued notices; it was the
  one refused at 8x8/1if) and the `answering-ports` arm's `aecp-largest-notice` (R4L; it built in round 1). Both built.
- **The size by shape** keeps two interfaces at 40, so 1x1/2if's image is byte-identical; 40 is at least every
  two-interface shape's descriptors (1x1's 12, 8x8's 40), which the static assertion and `shape_costs` hold.
- **The 8x8/1if notice item (140 us)** is taken literally from round 1's measurement, though below 1x1/1if's 210 us,
  as the assignment says; it is flagged as the likeliest to rise in phase B.
- **CPUs:** the shared picker had no free range all phase; every unit ran on this session's own CPUs (96-127), none a
  new booking, each its own unit capped at 10 GB.

### 3. New checks, planted mutants and failing words

| Check | Plant | Failing words |
|---|---|---|
| THE TRANSMIT's row held to the derived bound (harness self-test) | `transmit: THE TRANSMIT's row held one over CTRL_LOOP_TX_BOUND_MS` (BUDGET_MS + 1) | "THE TRANSMIT's row is held to CTRL_LOOP_TX_BOUND_MS as ctrl_loop.h derives it, never a typed figure ..." and "one 1 ms over its bound, at 51 ms, misses it" |
| the same | `transmit: THE TRANSMIT's row held to T_svc's 20 ms (earlier rule)` (W = 0) | the same first check, and "a timer's MRPDU is timed from its TICK to its commit, at its bound, 50 ms, within it" |
| A pass's polls at 8x8/1if at its shape's costs | `shapes: 8x8/1if's polls held at the interface count's (earlier rule)` | "a pass's polls at 8x8/1if are held to its shape's stated costs, apart from the interface count's ..." |
| 8x8/1if's load reads its shape's polls in both columns | `load: 8x8/1if's polls at 8x8/2if's, the nearest point's (earlier rule)` | "8x8/1if's load takes its polls' base and items at its shape's stated costs in both columns ..." |
| Table rule: SRP record within its slice (`shape_costs --selftest`) | `an SRP record over its slice` | "the shape (1, 2, 2): an SRP record of 905 us, over its slice of 900 us" |
| Polls stated at every listed shape | `a listed shape whose polls are not stated` | "poll_grade.py states the polls at [...], not at the shapes ctrl_loop.h lists, [...]" |
| `AECP_NOTICES_MOST` at each point vs its descriptors | `the notices most typed at the 1x1's 12 at one interface (earlier rule)` | "8x8/1if: AECP_NOTICES_MOST is 12, under the 40 notices its descriptors hold" |
| the same | `an AVB interface's notices counted as two` | "1x1/1if: ... is 11, under the 12 ..." and "8x8/1if: ... is 39, under the 40 ..." |
| the same | `two interfaces' most under the 8x8's descriptors` | "8x8/2if: AECP_NOTICES_MOST is 12, under the 40 notices its descriptors hold" |
| the default | `the notices with no shape header not the shipping configuration's` | "aecp.h holds 11 notices with no shape header, not the shipping configuration's 12" |
| load counter descriptors = shape header | `a load point counting other descriptors with counters than the shape header states` | "8x8/1if: load_grade.py counts 18 descriptors with counters, not the 20 the shape header states" |
| Firmware: every notice kept and sent once | campaign row `notice-dropped-with-its-descriptors-next` (`e->pending = 0u` on a build) | "every notice the descriptors hold is sent, none dropped" (6 of 12 at 1x1/2if app; 20 of 40 at 8x8/1if) |
| Firmware build: descriptors over the most | ad hoc: aecp.h's earlier `(MBX_N_IF == 1u ? 12u : 40u)` at the 8x8 shape | `static assertion failed: "AECP_NOTICES_MOST: the descriptors hold more notices"` |

Receipts: `receipts/firmware/plant-*.txt`; the shape controls in `shape_costs.py --selftest` (18 of 18).

### 4. Provisional figures (phase B re-measures each after #902 merges)

All from round 1's graded legs at `93afe385` on the 8x8/1if image at 1,475 us (arm A, every group, A0-A3; and AL, the
answering-ports arm's `aecp-largest-notice`), each the most measured plus 5 %, rounded up to 5 us
(`receipts/r1-heaviest-8x8-1if.txt`):

| Figure | Where | Measured, CPU cycles | Stated, us | Was (one interface) |
|---|---|---:|---:|---:|
| `CTRL_LOOP_SRP_UNIT_US` | ctrl_loop.h (1, 9, 9) | 32,401 (`srp_mbx:receive`, backlog-adp@blank-aged2-7) | 345 | 250 |
| polls base | poll_grade EIGHT_ONE | 22,478 (save-held) | 240 | 205 |
| withdraw | | 10,238 (backlog) | 110 | 90 |
| rebuild | | 56,003 (fixture) | 590 | 290 |
| walk | | 4,829 (srp) | 55 | 35 |
| reclaim | | 2,460 (save-held) | 30 | 25 |
| retained (and an SRP record's own apply, up to 32,023) | | stated at the SRP record's | 345 | 280 |
| acmp | | 6,936 (backlog-owed) | 75 | 50 |
| acmp_declined | | 2,600 (backlog-owed) | 30 | 20 |
| aecp (a notice) | | 13,041 (aecp-fanout) | 140 | 210 |
| aecp_long | | 29,860 (aecp-largest-notice) | 315 | 365 |
| the load at 8x8/1if, pin / tsn-c-stack#32 | load_grade | (recomputed) | 0.710 / 0.670 | 0.706 / 0.672 |

- The slice at 345 us, predicted from round 1's logs (`receipts/r1-srp-slices-8x8-1if.txt`): the latest record start
  was 124,105 cycles into its pass (check at most 122,500 at 250 us), so at 345 us a slice ends by about
  113,000 + 1,605 + 32,401 = 147,006 cycles, under 147,500. A 494-cycle margin: phase B's slice check decides it.
- **The aecp item (140 us) is from arm A only;** the answering-every-port arm, which stages the heaviest notices at the
  other points (1x1/1if's 210 came from it), was not measurable at 8x8/1if before (iv). It is the likeliest figure to
  rise in phase B.
- 8x8/1if's records, events and THE STEP's pass in the load stay 8x8/2if's (NEAREST), owed to #872, as before.

### 5. What phase B must measure (after #902 merges, on the merged head)

1. Sync: merge `dev-soft-core` into this branch (the manager), resolving `mrpdu_grade.py` (#902's `LATE_MS`/`resolve`
   beside this `BUDGET_MS`/`wait_ms`; both derive `CTRL_LOOP_TX_BOUND_MS`, 49), `ctrl_configs.py` (the same
   `mrpdu_grade.py` entry), FR_NFR line 418 and the README lines both sides touch; take the shape header as the single
   source for #902 round 9's direct-index table (the ruling (c)); check 1x1 and 8x8/2if byte-identity against #902's
   merged head (qimg + `scripts/img_check.py` against the merged head's own images, not 8a3791e4's).
2. Measure at 8x8/1if (arm A every group, AL, and the answering-every-port arm): every row the CPU decides within its
   bound; no budget miss beyond the seven egress rows of section 13's ledger, none new or larger; MRPDU within 49;
   joins 181.0 to 239.0; the first queued notice within 20 ms, the last within 130 ms, the paced R4L within 238 ms.
3. Restate from that measurement plus 5 %: `CTRL_LOOP_SRP_UNIT_US` at (1, 9, 9) and every `EIGHT_ONE` poll figure;
   recompute the load (<= 0.75); STOP if a slice is over 1,600 us or the platform image over 56.0.
4. The `transmit-aged` control (`--variant answering-later --mutation transmit-aged`) at the derived budget: it holds
   an MRPDU 300 passes, so it must still put every group's row over 49 ms, not only over 20 ms.
5. The full pass once, then REVIEW READY (the manager's next assignment).

### 6. Gate table

| Gate | Where | Result |
|---|---|---|
| Images: six fixed identical to 8a3791e4, platform-8x8-1if <= 56.0 | start, after (ii), after (iv), head (clean clone) | PASS each (`receipts/images/img-0..3`); 8x8/1if 56.0, same rom/sram |
| `shape_costs.py --check --selftest` | working tree before commit | PASS, 18/18 controls |
| flip --point 1x1/1if; --point 8x8/1if; --point 8x8/2if | same | rc 0; rc 0 (0.710 of 0.75); rc 1 as reported |
| flip, load, rows_tiers self-tests; load --check; tier_grid 1x1/1if | same | rc 0 each |
| docs_check, em-dash, Python and C++ idiom, `git diff --check 8a3791e4`, ctrl_hot --check | same | rc 0 each |
| AECP notice tests at 1x1/1if, 1x1/2if and 8x8/1if (mailbox) | working tree | PASS (2 tests each) |
| Plant `notice-dropped-with-its-descriptors-next` (campaign form; 8x8/1if) | working tree | CAUGHT both |
| Plant earlier rule 12 at 8x8/1if | working tree | refused by the static assertion |
| Harness self-test (`run.py --self-test`) | head, clean clone | rc 0: 0 failures, 863 checks, 250 mutants caught, 0 escaped (`receipts/harness/harness-selftest-bc8acc76.txt`) |
| firmware-unit (suites incl. the 8x8/1if AECP arm, coverage 39 files) | head, fresh clone | every step rc 0 (`receipts/firmware/firmware-jobs-bc8acc76.txt`) |
| firmware-control-mutants, -aecp-mutants, -srp-mutants (the campaign's four shards with unit's) | head | every step rc 0, no ESCAPED; `notice-dropped-with-its-descriptors-next` [ok] |
| firmware-boundary | head | first run rc 2: the default venv lacks migen (environment); rerun with the LiteX venv, as round 1: every step rc 0, `ctrl_boundary: PASS` |
| answering-every-port arm built at 8x8-1if, 16 groups constructed | head | the model holds 40 notices, `AECP_NOTICES_MOST` at its shape 40; 40 queued-notice probes a group (`receipts/harness/arm-every-8x8-1if-bc8acc76.txt`) |
| answering-ports arm (R4L's `aecp-largest-notice`) built at 8x8-1if | head | 96 groups constructed (`arm-ports-8x8-1if-bc8acc76.txt`) |
| quick gates at the head | clean clone | as before commit (`receipts/gates/quick-gates-bc8acc76.txt`) |
| load at 8x8/1if | head | 0.710 / 0.670 of 0.75 (`receipts/model/load-8x8-1if-bc8acc76.txt`) |

### 7. Run history

- 05:00 CET: start; read the ruling (fetched, identical to `A10-RULING.md`) and round 1's HANDOFF.
- 05:0x: fetched #902's branch `894-tiers` (read only) to see round 8's form of `CTRL_LOOP_TX_BOUND_MS` (`dd01b0af`:
  `240 - 10 x JOIN_CS - T_EGRESS`, 49 ms, read by `tier1_rows.built_value`/`tx_budget_ms`), so (i) reads the bound
  through the same reader and takes 49 at the merge without an edit.
- 05:1x: round 1's measurements extracted from its graded legs (scratch, A0-A3 and AL at `93afe385`):
  `receipts/r1-heaviest-8x8-1if.txt` (`scripts/r1_heaviest.py`), `receipts/r1-srp-slices-8x8-1if.txt`
  (`scripts/srp_slices.py`). Also: 1x1/1if's heaviest SRP record in round 1's S1 (save groups) is 26,086 cycles,
  over its 250 us unit (a finding; 1x1 must not move).
- 05:16: images at the start head: identical to round 1's head receipt (`receipts/images/img-0-start-c9226ff3.txt`).
- 05:18: (ii) in the working tree; images: the six fixed identical, 8x8/1if 56.0 (`img-1-after-ii.txt`).
- 05:20: (iv)'s C side; images: the six fixed identical, 8x8/1if 56.0 (`img-2-after-iv.txt`).
- 05:2x-05:3x: (i), (iii), (iv)'s Python, the firmware test and plant, the docs. One slip, corrected before commit:
  the first section 13 rewrite took its end marker from an earlier "### What is left" heading and duplicated a span;
  the file was restored from HEAD and rewritten at the right span (diff checked: 39 insertions, 32 deletions).
- 05:3x: commits `86c3cf23`, `bc8acc76`; clean clone c2 at the head; images there identical to the working tree's.
- 05:37-05:39: units started on this session's own CPUs (96-127; the shared picker had no free range, so no new
  booking), each MemoryMax 10G: R2-st (harness self-test), R2-firmware-unit, -boundary, -aecp-mutants, R2-arm-every,
  R2-arm-ports; 05:42 R2-firmware-control-mutants and -srp-mutants.
- 05:40: both arms built at 8x8-1if (about a minute each), groups constructed.
- 06:01: unit, AECP and SRP shards done, every step 0; boundary step 9 rc 2 on the venv's missing migen; 06:03 rerun
  with the LiteX venv (R2-firmware-boundary-b), 06:22 PASS. 06:0x harness self-test done, 0 failures. 06:12 control
  shard done.
- 06:2x: quick gates on the clean clone at the head; receipts sanitized of host paths; INDEX.md generated. No unit of
  mine left running. Nothing posted, pushed or merged.
