# Lane 637 (author [A656]) — HANDOFF

## Round 3 (REVIEW READY at `1e914414`, posted on #637 as comment 6298458163; rounds 2 and 1 below are kept as they were, except round 2's campaign rows, now split)

Answers R669-2 (PR #768 comment 6295588258) and R670-2 (comment 6295076402) under the round-3 assignment
(comment 6295599722). New commits on `8000520c`, no rebase, no amend, not pushed.

- Head: `1e914414557874648ac5041aff88b96908e0e053`. Every gate this round lists is rc 0 at the head, or at
  `600565b4` for the campaign (only the milan_dp README and a Makefile comment differ). Board cold cycle not done.
- Commits on `8000520c`: `dc7dd727` (docs: the cause fields), `600565b4` (the lone-record cases and three
  controls, TESTING.md's count), `1e914414` (the milan_dp README table and Makefile count, from the campaign).
- No RTL change: `git diff 8000520c HEAD -- hdl syn constraints` is empty, so round 2's route-1x1, ooc-1x1,
  ooc-8x8, xvlog and Yosys records (at `887b6bf2` and `af5eefc6`, equal in those trees) carry to this head; no
  Vivado run was owed or made.

### Assignment work items

| Item | Met | Evidence |
|---|---|---|
| 1. R669-2-F1: `[MAPREC]` grades blank 1, fail 0, done 1 on a lone framed map record failing the validated test, a crc case and a layout-or-id case; controls removing the crc and layout/id terms caught | yes, plus a layout case beside the id case and the optional magic/length control | `maprec_lone_record_section`; rows 61, 62, 63 |
| 2. R669-2-F2: REGISTER_MAP paragraph and PP_STAT `[3]`, D3 8.7 state what holds when the binding walk also failed | yes | `dc7dd727` |
| 3. R670-2-F1: PR body, HANDOFF and issue separate the full campaign (rc 2, 63/65), the listener rerun (rc 0, 2/2) and the aggregate; synthesis rc 0 kept apart; both receipts linked | yes | PR body round-2 account rows; Round 2 Gates table below; the round-3 REVIEW READY |
| 4. Residue to the merge checklist, applied only inside an edit already made | yes: only R670-2-R3 (the PR body's role lines, which this round rewrites) | PR body roles |

### Changes (file:line at the head, clause)

- `tb/verilator/milan_dp/sim_nxn.cpp:5496-5529` `maprec_lone_record_case` and `maprec_lone_record_section`
  (D3 3 rule 7, 8.7): a window holding one framed map record, edited at one byte (payload under the old crc16;
  layout, id or magic re-sealed); every port graded on its reset set (GET_AUDIO_MAP, both RAMs), then PP_STAT done
  1, busy 0, fail 0, blank 1. `:5553` the section runs last; `:5557` the vacuity guard counts 59 pages (51 + 8).
- `tb/verilator/milan_dp/dynmap_mutants.py` rows 61 to 63 and a docstring paragraph for them.
- `docs/reference/REGISTER_MAP.md:2378-2380` and the PP_STAT row `[3]` (`:2403`); `docs/design/SAVED_STATE_MATERIALIZATION.md`
  8.7 (`:1499-1502`): the map restore adds no cause of its own; `[20:18]` reads 0 because its start gate
  (`milan_datapath.sv:5347-5348`) needs a D3 walk that ended with no cause; `[22:21]` keeps the binding walk's.
- `docs/testing/TESTING.md:277` 63 controls, 43 `[MAPREC]` arms; `tb/verilator/milan_dp/Makefile:569-570` 63 and 54;
  `tb/verilator/milan_dp/README.md` the lone-record bullet, PP_STAT bullet, campaign line and table.

### New checks and their planted mutants (round 3)

The four new cases in the dynmap leg (`maprec_lone_record_section`), each a window holding one framed map record
and nothing else, after a planted power cycle: GET_AUDIO_MAP on both ports and both crossbar RAMs read the reset
sets, then PP_STAT done 1, busy 0, fail 0, blank 1 (`5b000484`). At the head the leg is 649 checks, 0 failures
(589 at round 2: +60, fifteen per case).

| Case | Edit | Term that fails |
|---|---|---|
| `lone crc-bad input record` | record `0x60`, payload byte 5 (the first mapping's cluster) 0 to 4, crc16 left | crc16 |
| `lone wrong-layout input record` | record `0x60`, header byte 2 (layout) to `0x03`, re-sealed | layout and id |
| `lone wrong-id output record` | record `0x70`, header byte 3 (id) to `0x71`, re-sealed | layout and id |
| `lone wrong-magic output record` | record `0x70`, header byte 0 (magic) `0x17` to `0x18`, re-sealed | magic and length |

| # | Leg | Mutant (planted in `milan_datapath.sv`, AS_RJDG's `amr_rs_valid_r` condition) | Named check(s) that fail | Failures |
|---:|---|---|---|---|
| 61 | dynmap | the validated-record test ignores the crc16 | `[MAPREC] lone crc-bad input record: PP_STAT blank 1` | 1 of 649 |
| 62 | dynmap | the validated-record test ignores the layout and the id | `[MAPREC] lone wrong-layout input record: PP_STAT blank 1`; `[MAPREC] lone wrong-id output record: PP_STAT blank 1` | 2 of 649 |
| 63 | dynmap | the validated-record test ignores the magic and the length | `[MAPREC] lone wrong-magic output record: PP_STAT blank 1` | 1 of 649 |

Each mutant touches only the validated test; the well-formed test beside it is unchanged, so the record is still
refused and only blank can tell. Before this round, R669-2's probe showed each of these mutants passing the leg at
589/0. Rows 1 to 60 keep their meaning. Their dynmap tallies move to 649, and their failure counts are re-measured
in the milan_dp README table (row 1, for example, 142 to 166 of 649, since the four new cases expect the power-on
map).

**The campaign, one command.** `make -C tb/verilator/milan_dp_render tdm8render-build` (rc 0), then
`make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` from a clean clone at `600565b4`:
`68 checks: 68 PASS, 0 FAIL`, `CAMPAIGN rc=0`. That is five clean legs passing (dynmap, maprec8, maprec4, listener,
talker) and 63 of 63 controls caught, in one execution
(`receipts/round3/campaign/campaign-600565b4.verdicts.txt`, `.log.excerpt`, `render-build.log`). `600565b4`
differs from the head only in the milan_dp README and a Makefile comment.

### Gates (round 3)

From clean clones at the head `1e914414`, unpiped, one log and one rc per command (`receipts/round3/scripts/`).
Python gates under CPython 3.12.3 with the workflows' pins; the campaign driver under the host's CPython 3.14.8, as
in round 2. Verilator 5.050.

| Gate | Head | rc / result | Receipt (`receipts/round3/`) |
|---|---|---|---|
| `make -C tb/verilator/milan_dp dynmap`, `maprec8`, `maprec4` | `1e914414` | 0, 0, 0: 649/0, 219/0, 137/0 | `legs/` |
| `make -C tb/verilator/milan_dp_render tdm8render-build`, then `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` (one full command) | `600565b4` (tb, hdl equal to the head) | 0, then 0: 68 checks, 68 PASS; 63 of 63 caught, five clean legs pass | `campaign/` |
| docs.yml: docs-gates-0 steps 4, 12 to 21, 23, 24, 27, 29 to 52 and 54; docs-check-no-git; wire-accountability; docs-gates-2 16 and 17 (95 commands; em-dash against `e26f1816`) | `1e914414` | all 95 rc 0 | `docs/rc.tsv` |
| docs.yml: builder legs 0 and 1 (docs-gates-1 and -2 step 15) | `1e914414` | 0 and 0 (leg 1: 102 of 103 gates; gate 11, the calibration gate, declared NOT RUN by the builder: it reads a place report from a local LiteX build tree this host does not hold) | `builder/` |

The healthy map-restore hold at the head stays 598 to 672 clocks (dynmap leg; the four new cases hold 672), so
D3 18.4 and the README keep their figure.

Not rerun this round, with the reason: route-1x1, ooc-1x1, ooc-8x8, xvlog and the full Yosys run (no file under
`hdl`, `syn` or `constraints` changed since `887b6bf2`/`af5eefc6`); the rtl-fast firmware and boundary steps (no
firmware, Makefile target or `ctrl` README change; the Makefile edit is a comment); the full sweep (not in the
round-3 list; the only suite source changed is `milan_dp`'s dynmap leg, rerun above, and its campaign driver).
Skipped as in round 2: hosted provisioning, hosted-result steps, builder gate 11 (declared NOT RUN by the builder),
the act replica (no push), the hosted exhaustive gates, and the board cold cycle.

Cancelled or superseded, not cited: a first builder-bank launch at the head refused in 1 s in both legs ("source
dependency origin differs: third_party/tsn-c-stack"), because the scratch clone's submodule origins pointed at the
lane's own checkouts. `git submodule sync` restored the `.gitmodules` URLs, as a clone of the canonical repository
has them, and the bank was rerun from the start (`builder-refused/`). Before the full campaign, the three new rows
ran through the driver in the lane during development (all caught); only the full campaign is cited.

## Round 2 (REVIEW READY at `8000520c`, posted on #637 as comment 6294768287; round 1 below is kept as it was)

Answers R669-1 (PR #768 comment 6268811441) and R670-1 (comment 6269970193) under the round-2 assignment
(comment 6269988820), whose rulings accept the one-pass map transaction and require the cross-port fix.

- Base: dev `e26f1816` merged with a merge commit, `8a7e6beb` (no conflict: #763's change is `sw/firmware/ctrl`
  only, and `git diff e9cbb676 e26f1816 -- hdl` is empty, so round 1's base area and timing records still hold).
- Commits after the merge: `df284d1d` (RTL and tests), `02271047` (sweep order), `a48c6a16` (docs), `887b6bf2`
  (layout/id both directions, legal maximum), `1ff152ee` (the named checks of campaign rows 58 and 59), `556959bd`
  (the milan_dp README's campaign table), `af5eefc6` (the measured hold, 598 to 672 clocks, in 18.4 and the README).
- Head: `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`. `8000520c` changes one line of `sw/firmware/ctrl/README.md`
  (the firmware boundary's pin-control count, 161 to 165; see Gates). `git diff 887b6bf2 8000520c -- hdl` is empty,
  so the routed and synthesized `887b6bf2` carries the head's RTL; `git diff 1ff152ee 8000520c -- tb scripts`
  touches only the milan_dp README.
- Three host resets (hardware memory errors, not gate failures) cut round-2 sessions: the first while ooc-8x8 and
  the sweep were running, the second while the boundary legs and the sweep were running at `8000520c`, the third
  while the sweep at `8000520c` was in `milan_dp`. Each cut run was rerun from the start in a later session, and no
  partial result is cited. After the third, the sweep ran as the runner's own four shards, one after another, each
  a complete run with its own log and rc, so a reset could cost only the shard it cut.

### Rulings applied

- One-pass restore accepted: D3 section 3 rule 7 now carries the amendment for the map records, and 18.4 states
  the transaction, its map-only boundary, and its validation obligation for one pass and its deadlines.
- Cross-port ownership fixed, not documented: the restore takes every reset set down first (below).

### Assignment work items

| Item | Met | Evidence |
|---|---|---|
| 1. PP_STAT `[1]`, `[3]`, `[7]` composed; public-register assertions with a control each | yes | `pp_stat_*_w`; `maprec_grade_stat` after every case; rows 38 to 44, 56 |
| 2. Cross-port fix; both port orders and a cyclic swap; GET, ownership, routing; a control restoring the old order | yes | AS_RNEXT stages; `mp_out_section` (`maprec8`); row 54 |
| 3. Restore arms with killing controls: put-back, holes, layout/id, ranges, conflicting keys, pass-0 defaults, directions, port boundaries | yes | `maprec_value_arms_section`, `maprec_pass0_abort_section`, `mp_in_section` (`maprec4`); rows 45 to 53, 57 to 60 |
| 4. Every docs-workflow gate and self-test at the head, no ratchet loosened; the literal-bound port justified; executed, skipped and cancelled separated | yes | Gates (round 2) below; `milan_datapath.sv:9152` |
| 5. PP_STAT `[4]` names the parent map writer | yes | `REGISTER_MAP.md` PP_STAT `[4]` |
| 6. R669-R1 to R3; S1 as one sentence in 18.4 | yes | Changes below |
| Merge dev `e26f1816` (merge commit); rerun the gate list, dynmap, dynmap-mutants, route-1x1 and ooc | yes | `8a7e6beb`; Gates (round 2) |
| STOP on a processor register-map, top-level port or parameter change | none made | `git diff 63a187e1 8000520c -- hdl` adds or removes no `input`, `output` or `parameter` line; the processor pin stays `2cbed0a9`; `milan_csr.sv` takes the same four inputs, composed |

### Changes (file:line at `887b6bf2`, clause)

`hdl/milan/milan_datapath.sv`
- `:2333`, `:2837-2841`, `:5756-5773` PP_STAT's restore bits composed with the map restore (`pp_stat_*_w`):
  busy covers it, done waits for its end, fail adds its roll-back, blank needs it to have validated no record and
  failed nowhere (D3 3 rule 7, 5.2, 8.7; R670-F1, R669-F1, R669-S2). The processor's interface is unchanged.
- `:4906-4929` the restore's contract comment; `:5222-5224` stage and put-back marks; `:5240` `amr_rs_valid_r`.
- `:5363-5395` AS_RNEXT: stage 0 REMOVEs every dynamic port's reset set, stage 1 reads each record once, stage 2
  ADDs back the marked ports' reset sets (Milan v1.2 5.3.10.1; R670-F2, R669-F5; the ruling).
- `:5484-5503` AS_RJDG: a framed, crc-clean record sets `amr_rs_valid_r` (the processor's `framed_any_r` test);
  erased, unframed or refused marks the port. `:5595-5605` AS_EEND: a refused saved set marks its port; a refused
  take-down or put-back rolls back (D3 6.2, 8.6).
- `:9152` the `mrec_offset_i` literal's rationale (R669-F3); `:4938` "check 15" (R669-R1).

`hdl/milan/KL_pp_shadow.sv:966` lane label removed (R669-R2); `:1621-1624` pointer to the composition.
`hdl/common/csr/milan_csr.sv:650-651` the four inputs arrive composed.

`tb/verilator/milan_dp/sim_nxn.cpp` `[MAPREC]` split into functions under 100 lines (R669-F4, cpp-idiom);
`want_r`/`want_k` single declarators; the alarm check renamed so no `alarm (` reaches the wall-clock detector
(R669-F4); `start_the_boot_restore_walk` holds `tready` low while it polls (an answer the release sends is kept
whole for the caller's await); `(lane 3)` removed (R669-R3). New: PP_STAT after every case and inside the saved
case's map restore; first-record device error; the value arms (hole, ranges, conflicting keys, layout, id, each
in both directions where the direction has the field); legal maximum; put-back under a restored 4-channel format;
D3 pass-0 abort; the multi-port half `maprec_multiport_section` (8x8 outputs, 4x4 inputs).
`tb/verilator/milan_dp/Makefile` legs `maprec8`, `maprec4` (appended last to the ordinary list, so the round-robin
CI pieces keep the heaviest piece's membership); `dynmap_probes.vlt` opens `amap_out_owner_r`;
`dynmap_mutants.py` 23 new rows, multi-check rows, `--jobs` (at most two builds); `test_sim_pool.py` fourteen legs.

Docs: `SAVED_STATE_MATERIALIZATION.md` 3 rule 7 (amendment), 5.2, 8.7, 18.4 (implementation record rewritten: three
stages, roll-back, the transaction, its validation obligation, status, holds, S1 sentence, evidence),
`REGISTER_MAP.md` PP_STAT `[1]`, `[2]`, `[3]`, `[4]` (the parent map writer, R670-F5, R669-F6), `[7]` and a
paragraph, `TESTING.md`, the milan_dp README.

### New checks and their planted mutants (round 2)

Campaign: `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4` from a clean clone at `887b6bf2`:
65 checks, 64 PASS, 1 FAIL (`receipts/round2/campaign/campaign-887b6bf2.log`). The one FAIL was row 59's named
check, not the mutant: with every input port's record id at `0x60`, every port also WRITES region `0x60`, the last
writer was port 3, and port 3 then restores correctly while ports 0 to 2 fail (8 of 137, reproduced by hand,
`receipts/round2/campaign/row59-by-hand.log`). `1ff152ee` names the checks that catch it; rows 58 and 59 rerun at
`1ff152ee` through the driver: both caught, each clean leg passing (`campaign-rows58-59-1ff152ee.log`). So 60 of
60 caught; rows 1 to 37 keep their round-1 meaning with the leg's new tally (589 checks).

**Rerun at the head** (`af5eefc6`, whose `tb/` and `hdl/` equal `8000520c`'s), the same command from a fresh
clone: 65 checks, 63 PASS, 2 FAIL (`campaign-af5eefc6.log.excerpt`, `.verdicts.txt`). Both FAILs are the
listener leg, its clean run and row 36, and neither is a mutant result. The listener leg runs in
`tb/verilator/milan_dp_render` and keeps that suite's generated inputs (`ltn_rom.hex`, `ucode.hex`,
`tdm8r_aemi.bin`) unmade, taking them from the suite's clean build, as the driver's docstring says. A fresh clone
has none, and the `dynmap-mutants` target builds only `milan_dp`'s legs. This is dev's arrangement (`e26f1816`'s
driver has the same listener entry and its target the same prerequisites), and `887b6bf2`'s run passed only because
its tree had been swept. After `make -C tb/verilator/milan_dp_render tdm8render-build`, row 36 through the driver:
the clean listener leg passes, and the mutant is caught by its named check, 8 failures of 264
(`campaign-row36-af5eefc6.log`). So at the head: 60 of 60 caught, all five clean legs pass. The PR body's
validation steps now build the render suite before the campaign. Making the target do so itself is left as a
proposal for the manager; this lane did not change it.

| # | Leg | Mutant (planted in `milan_datapath.sv`) | Named check(s) that fail | Failures |
|---:|---|---|---|---|
| 38 | dynmap | the map restore's roll-back is not composed into PP_STAT fail | `[MAPREC] roll-back: PP_STAT fail 1`; `[MAPREC] first-record device error: PP_STAT fail 1`; `[MAPREC] slow memory: PP_STAT fail 1`; `[MAPREC] silent memory: PP_STAT fail 1` | 4 of 589 |
| 39 | dynmap | PP_STAT blank ignores a validated map record | `[MAPREC] saved, after the power cycle: PP_STAT blank 0`; `[MAPREC] empty, after the power cycle: PP_STAT blank 0` | 16 of 589 |
| 40 | dynmap | PP_STAT blank ignores the map restore's failure | `[MAPREC] first-record device error: PP_STAT blank 0` | 1 of 589 |
| 41 | dynmap | PP_STAT busy does not cover the map restore | `[MAPREC] saved: PP_STAT reads busy, not done, not blank, while the map restore holds` | 1 of 589 |
| 42 | dynmap | PP_STAT done does not wait for the map restore | `[MAPREC] saved: PP_STAT reads busy, not done, not blank, while the map restore holds` | 1 of 589 |
| 43 | dynmap | PP_STAT blank is published before the map restore ends | `[MAPREC] saved: PP_STAT reads busy, not done, not blank, while the map restore holds` | 1 of 589 |
| 44 | dynmap | the map restore takes every record it reads for a validated one | `[MAPREC] first boot: PP_STAT blank 1` | 1 of 589 |
| 45 | dynmap | a saved set the ADD rule refuses is never put back | `[MAPREC] put-back: SPI 0: number_of_mappings` | 3 of 589 |
| 46 | dynmap | an erased or refused record's port is never put back | `[MAPREC] first boot: SPI 0: number_of_mappings` | 88 of 589 |
| 47 | dynmap | no hole rule: a mapping after an UNUSED entry is not refused | `[MAPREC] hole, input: SPI 0: number_of_mappings`; `[MAPREC] hole, output: SPO 0: number_of_mappings` | 6 of 589 |
| 48 | dynmap | the layout version is not judged | `[MAPREC] wrong layout, input: SPI 0: number_of_mappings`; `[MAPREC] wrong layout, output: SPO 0: number_of_mappings` | 6 of 589 |
| 49 | dynmap | the record id is not judged | `[MAPREC] wrong id, input: SPI 0: number_of_mappings`; `[MAPREC] wrong id, output: SPO 0: number_of_mappings` | 6 of 589 |
| 50 | dynmap | a field outside every ADD range is dropped, not refused | `[MAPREC] range, input stream channel: SPI 0: number_of_mappings`; `[MAPREC] range, input cluster: SPI 0: number_of_mappings`; `[MAPREC] range, output stream: SPO 0: number_of_mappings`; `[MAPREC] range, output cluster: SPO 0: number_of_mappings` | 12 of 589 |
| 51 | dynmap | one input cluster, two mappings: not refused | `[MAPREC] conflicting keys, input: SPI 0: number_of_mappings` | 3 of 589 |
| 52 | dynmap | one output stream channel, two clusters: not refused | `[MAPREC] conflicting keys, output: SPO 0: number_of_mappings` | 3 of 589 |
| 53 | dynmap | the map restore runs over a D3 abort in pass 0 | `[MAPREC] D3 pass-0 abort: SPI 0: number_of_mappings` | 6 of 589 |
| 54 | maprec8 | the round-1 ordering: a port's reset set comes down just before its saved set | `[MAPREC] transfers, after the power cycle: port 0: the mappings are the expected list` | 12 of 219 |
| 55 | maprec8 | a refused put-back does not roll back | `[MAPREC] refused put-back: port 7: number_of_mappings` | 7 of 219 |
| 56 | maprec8 | the map restore's roll-back is not composed into PP_STAT fail, 8x8 | `[MAPREC] refused put-back: PP_STAT fail 1` | 1 of 219 |
| 57 | maprec8 | an output port refused a key another port holds is never put back | `[MAPREC] conflicting keys across ports: port 7: number_of_mappings` | 4 of 219 |
| 58 | maprec8 | every output port writes and reads output port 0's record | `[MAPREC] transfers, after the power cycle: port 7: the mappings are the expected list` | 12 of 219 |
| 59 | maprec4 | every input port writes and reads input port 0's record | `[MAPREC] inputs: the window holds the codec's records and the pend has fallen`; `[MAPREC] inputs, after the power cycle: port 0: the mappings are the expected list` | 8 of 137 |
| 60 | maprec4 | the last input port's refused saved set is never put back | `[MAPREC] put-back, last port: port 3: number_of_mappings` | 3 of 137 |

The checks these rows name (all in `tb/verilator/milan_dp/sim_nxn.cpp`, `[MAPREC]`): `maprec_grade_stat` after
every case (PP_STAT done 1 busy 0, then fail and blank), the mid-restore read in `maprec_saved_section`,
`maprec_torn_and_roll_back_section` (first-record device error), `maprec_value_arms_section` (holes, ranges,
conflicting keys, layout and id in both directions, legal maximum, put-back), `maprec_pass0_abort_section`, and
the multi-port `mp_out_section` (8x8) and `mp_in_section` (4x4).

### Resource and timing (round 2)

Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `--single-thread-synthesis`, Vivado 2026.1 under the
exclusive lock), round 1's drivers unchanged (`receipts/route-1x1/route.sh`, `receipts/ooc/ooc1x1.sh`,
`receipts/ooc/ooc8x8.sh`), run on a clean clone at `887b6bf2`, whose `hdl/` equals every later commit's. The base
is round 1's record at `e9cbb676`; `git diff e9cbb676 e26f1816 -- hdl` is empty, so it is the merged base's too.

| Route-1x1 | LUT | FF | SLICE | RAMB36 | RAMB18 | DSP | WNS ns | WHS ns | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| base `e9cbb676` (= `e26f1816` in `hdl/`) | 49,613 | 52,353 | 15,725 | 74 | 25 | 14 | +0.215 | +0.036 | rc 0 |
| round 1 `90b15366` | 49,902 (+289) | 52,615 (+262) | 15,801 | 74 | 25 | 14 | +0.316 | +0.015 | rc 0 |
| round 2 `887b6bf2` | 49,873 (+260) | 52,611 (+258) | 15,764 (+39) | 74 | 25 | 14 | +0.065 | +0.036 | rc 0 |

- Route complete, no unrouted net, no routing error. WNS stays positive; its move from round 1 is placement, not
  this path set (the gate's sub-block report moves only `u_nvm`, the wrapper and processor blocks by tens of LUTs).
- `milan_datapath`'s own logic in the routed hierarchy: 663 LUT at the base, 988 at round 1, 1,025 now (+37 over
  round 1 for the stages, the put-back marks, the validated flag and the PP_STAT composition).
- DR4's maps-stage ceiling is 1,250 LUT / 600 FF incremental at 1x1 TDM8; round 2 uses +260 / +258.

| Endpoint | base LUT / FF | round 2 LUT / FF | delta | gate |
|---|---|---|---|---|
| ooc-1x1 (standalone `KL_pp_shadow`) | 23,314 / 19,821 | 23,366 / 19,823 | +52 / +2 | rc 0 |
| ooc-8x8 | 30,211 / 27,451 | 30,282 / 27,451 | +71 / +0 (equal to round 1) | rc 0 |

- RAMB36, RAMB18 and DSP unchanged at both endpoints. ooc-8x8 synthesizes `KL_pp_shadow` alone, which holds the
  arbiter but not the datapath, so round 2's RTL leaves it where round 1 left it.
- `scripts/xvlog_gate.py --check` (under the exclusive lock) and `--selftest` at `887b6bf2`: rc 0 and rc 0, 0
  findings (`receipts/round2/route-ooc/xvlog-*.log`).
- Receipts: `receipts/round2/route-ooc/` (reports, logs), drivers `receipts/round2/scripts/vivado-chain.sh` (route,
  ooc-1x1) and `chain-r2b.sh` (the ooc-8x8 and xvlog rerun after the host reset).

### The reviewers' probes, rerun at the head

Both reviews' probe scripts were copied from their packets into scratch (the packets untouched) and run against a
clean clone at `af5eefc6`. Where the round-1 source line a probe anchors on no longer exists, the copy re-anchors
it to the head's line doing the same job, and the diff is published beside it (`receipts/round2/review-probes/`).
The build jobs were lowered to this host's bound; nothing else changed.

| Probe (review) | Round 1 result | At `af5eefc6` |
|---|---|---|
| `probe_maps.py` (R670): public PP_STAT after saved maps and after a map-only device error; hole, range, duplicate and refused-ADD put-back oracles | 131 checks, 3 failures (the F1 status defect) | 131 checks, 0 failures |
| `probe_controls.py` (R670): hole rule off; put-back off (re-anchored to the stage-2 mark) | each 6 failures (3 of them F1) | each 3 failures, exactly the three targeted value/RAM checks |
| `maprec_probes.py` (R669): clean leg | 331 checks, 0 failures | 589 checks, 0 failures |
| `maprec_probes.py` (R669): `no_putback` (re-anchored), `no_hole_rule`, `no_layout_id` (re-anchored), `no_range_refuse`, `no_dup_cluster`, `restore_on_pass0_defaults` | all six SURVIVED (0 failures) | all six CAUGHT: 3, 6, 12, 12, 3, 6 failures of 589 |
| `ppstat_probe.sh` (R669): PP_STAT printed after every planted power cycle (no check added) | fail and blank followed the processor only | fail 1 with the map roll-back in every roll-back, deadline and first-record-error case; blank 0 wherever a record validated; the leg 589/0 |

One harness note: the R669 driver builds with `-o ltn_rom.hex -o ucode.hex`, so in a fresh clone the first runs
crashed (rc -11, the clean leg too) on missing processor ROM images. Generating them with the suite's own targets
(`make -C tb/verilator/milan_dp ltn_rom.hex ucode.hex`) fixed it; no rebuild was needed, and only the runs after
that are cited.

### Gates (round 2)

Every runnable step of `.github/workflows/docs.yml` and `rtl-fast.yml`, one log and one rc per command, no pipes,
from clean clones (`receipts/round2/scripts/gates.sh`, `gates-ci.sh`, `gates-boundary.sh`). Python gates under
CPython 3.12.3 with the workflows' pins, except the two firmware-boundary legs (below) and the sweep (its
process-ownership preflight needs `os.pidfd_open`, which that 3.12.3 build lacks), which ran under CPython 3.14.8.
Verilator 5.050, Yosys 0.66, sv2v v0.0.12, the pinned RV32 SDK.

| Gate (workflow job and step) | Head | rc / result | Receipt (`receipts/round2/`) |
|---|---|---|---|
| docs-gates-0 steps 4, 12 to 21, 23, 24, 27, 29 to 52 and 54; docs-check-no-git 4; wire-accountability 5; docs-gates-2 16 and 17 (95 commands; em-dash against the merged base `e26f1816`) | `8000520c` | all 95 rc 0 | `gates-head/docs-ci/rc.tsv` |
| docs-gates-1 and docs-gates-2 step 15, builder legs 0 and 1 | `8000520c` | 0 and 0 (leg 1: gate 11 declared NOT RUN by the gate, below) | `gates-head/builder/` |
| rtl-fast firmware-boundary step 10 (`ctrl_boundary.py --without verilator`) | `8000520c` | 0: 0 findings, 112 boundary, 165 pin, 4 figure controls | `gates-head/boundary/` |
| rtl-fast firmware-verilator step 15 (`ctrl_boundary.py --only verilator`) | `8000520c` | 0: 0 findings, 6 boundary, 165 pin, 4 figure controls | `gates-head/boundary/` |
| rtl-fast verilator-lint 8, 9; bdd-conformance 6; yosys-elaboration 11 to 15; publication-census 13; firmware-unit 8, 11, 12, 13; firmware-control-, aecp- and srp-mutants 10; `changes` 3's `ci_scope.py --selftest` (28 commands) | `af5eefc6` | all 28 rc 0 | `gates-af5eefc6/rc.tsv` |
| `syn/yosys/run.sh` (the full run) | `af5eefc6` | 0, tap purity PASS | `gates-af5eefc6/yosys-af5eefc6.log` |
| `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4`, the full campaign from a fresh clone (clean legs dynmap 589/0, maprec8 219/0, maprec4 137/0, talker pass; the listener leg's clean run and row 36 FAIL, its suite unbuilt) | `af5eefc6` | **rc 2**: 65 checks, 63 PASS, 2 FAIL | `campaign/campaign-af5eefc6.log.excerpt` |
| `make -C tb/verilator/milan_dp_render tdm8render-build`, then `python3 dynmap_mutants.py --jobs 2 36` (the listener leg rerun) | `af5eefc6` | rc 0: 2 checks, 2 PASS | `campaign/campaign-row36-af5eefc6.log` |
| aggregate of the two rows above (two executions, not one command) | `af5eefc6` | 60 of 60 caught and five clean legs passed across them; the full campaign command's own exit was 2 | both |
| `scripts/xvlog_gate.py --check`, `--selftest` | `887b6bf2` | 0, 0 | `route-ooc/xvlog-*.log` |
| route-1x1, ooc-1x1, ooc-8x8 | `887b6bf2` | 0, 0, 0 | `route-ooc/` |
| `scripts/run_all_suites.sh "$out" --shard <i>/4`, i = 0 to 3 (the full sweep as the runner's four shards) | `8000520c` | rc 0 each: 63 suites (16, 17, 15, 15), 63 passed, 0 failed, 0 timed out; 2,187,192 checks, 0 in-suite failures; the four declared `tsn_fuzz` skips. `milan_dp` inside it: dynmap 589/0, maprec8 219/0, maprec4 137/0 | `sweep/` (`shard-<i>.log`, the per-suite logs' sha256) |

What carries the older heads to the head: `git diff af5eefc6 8000520c` is one line of `sw/firmware/ctrl/README.md`,
and of the gates in this table only `ctrl_boundary.py` reads that page (both of its legs rerun at the head);
`git diff 887b6bf2 8000520c -- hdl syn constraints` is empty.

**Executed, skipped, cancelled.**

- Executed: every row of the table, each from a clean clone, with its log and rc.
- Skipped, with the reason:
  - the workflows' provisioning steps (pip and apt installs, package-download resolution, submodule fetches, the
    sv2v, SDK, Verilator and Yosys install or build-on-miss steps): hosted provisioning. Their local equivalents are
    the pinned tools above, and the SDK's own verification (docs-gates-0 step 29) ran.
  - the steps that read hosted job results and run only on GitHub: docs-gates-0 55, docs-gates-1 16, docs-gates-2 18
    (record outcomes), docs-check 7, the ci-manifest, ci-fail-fast and ci-cancel-tail jobs, the classification of
    the PR's changed files in rtl-fast's `changes` job (its `ci_scope.py --selftest` ran) and the `rtl-fast`
    aggregate.
  - builder gate 11 (the calibration gate), which the builder itself declares NOT RUN: it reads a place report from
    a local LiteX build tree this host does not hold.
  - the act-first local replica (`act_ci.py --pr`): this lane does not push, so there is no remote PR head for it
    to record and recheck.
  - the hosted exhaustive `verilator-suites` and `yosys-portability` gates: they start on the hosted runner when the
    PR is marked ready. The full sweep and the full Yosys run above are their local counterparts.
  - the sweep's four `tsn_fuzz` steps, which the sweep declares skipped (the external generator is absent).
  - the on-board cold cycle (no bench access).
- Cancelled or superseded, none of them cited as a result:
  - at `af5eefc6`: both builder legs refused to start (a receipt file from an earlier run was in their path), and
    both boundary legs failed, one on `migen` being absent from the 3.12.3 interpreter, the other on the README's
    pin-control count (161 against the self-test's 165). `8000520c` fixes the count. All four reran at the head
    under the LiteX environment's interpreter, which holds `migen` as the hosted job's installed pins do, and pass.
  - runs cut by host resets: ooc-8x8 and a sweep in the first, the boundary leg without Verilator and a sweep at
    `8000520c` in the second, a sweep at `8000520c` (cut in `milan_dp`, the 40th of 63 suites, every earlier suite
    PASS) in the third. All were rerun from the start; none of the cut sweeps' suite results is cited.
  - one sweep start at `8000520c` aborted in the sweep's own cancellation preflight (rc 2: its hard-HUP control
    timed out), because the launcher had set SIGHUP to ignored, which the control's child inherited. It was
    relaunched without that and is the sweep in the table. One launch of the builder and boundary legs with
    relative log paths ran no gate and wrote nothing.

## Round 1 (as handed off)

Status: REVIEW READY at `63a187e1579474bca562d85304b9a91466877c33` (local, not pushed). Every gate rc 0 at the head
or at a commit whose `hdl` equals it. The on-board cold cycle is not done (no bench access in this lane).

- Branch `637-map-records` from dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` (processor pin `2cbed0a9`), not pushed.
- Commits on `e9cbb676`: `6ab04441` (RTL and the leg), `bbc6690b` (check 15, campaign arms), `bdff750c` (docs,
  READMEs, RTL comments), `5537211f` (more scenarios), `4cf7f4b9` (pending composition in the docs), `90b15366`
  (area cut and the aggregate scenario), `e3105d21` (deadline arms), `79f8aa89` (the held SET's premise), `edbd11a0`
  (README campaign table), `cf5c0c23` (pp_shadow P2), `63a187e1` (REGISTER_MAP PP_NVM_STAT[4]).
- `git diff 90b15366 HEAD -- hdl` is empty: the routed and standalone-measured commit carries the head's RTL.
- TAKEN: issue #637 comment 6257357939. REVIEW READY: issue #637 comment 6267367417 (text in `receipts/review-ready.md`).

## Step 0: dependencies (MATERIALIZATION 18.4, lane 4)

- Lane 1: done. Processor PR #132 (`d352bbaa`) is an ancestor of the pin.
- Lane 2: done. PR #623 (merge `e4b771f9`, processor `b2db3a97`) is in dev.
- Lane 3: NOT done in the parent (MATERIALIZATION.md:15-16 at base, MILAN_COMPLIANCE_MATRIX.md:182 at base). It
  does not block: the name records (`0x80..`) are disjoint, and this lane changes no name path. The name half of
  the sticky pending stays.
- DR3a: ratified (#70 comment 5873060660). DR4: ruled (#70 comment 5862405632). The maps ceiling is 1,250 LUT /
  600 FF incremental at 1x1 TDM8 (MATERIALIZATION.md:2380 at base).

## Design

- The processor never writes or reads maps (`KL_aecp_nvm_writer.sv:119-121`; processor `07_memory_maps.md:584-610`, 5.1, at
  the pin). The parent writes and restores them, with no processor change.
- The parent reaches `KL_nvm_backend` through a 2:1 device-face arbiter in `KL_pp_shadow.sv`, beside the
  processor's NVM port.
- The writer and the restore live in `milan_datapath.sv`, where the map stores and the edit server are.
- The restore applies a saved set through the existing ADD/REMOVE transaction server, so its value rule is the
  ADD rule itself (D3 15 item 7, parity by reuse).
- One deliberate deviation, published: one read pass, not two. The parent's roll-back reaches every map, so a
  second pass ends in the same states and only lengthens the faces' hold. That hold is bounded by the
  processor's 4,096-clock gather watchdog (`DESC_MEM_TMO_CYC_P`).

## Changes (file:line at the head, clause)

`hdl/milan/KL_pp_shadow.sv`
- `:402-433` the record face `mrec_*`, `amap_unflushed_i`, `amap_alarm_i` (07 5.1; D3 15 item 2, amended).
- `:1009-1020` the sticky source takes names only; `pend_i` adds `amap_unflushed_i`; the map pulse stays for the
  accepting edge (D3 5.2, 7.1; #502).
- `:1022-1099` the device-face arbiter: selection, drain, routing (D3 6.4, the drain; 15 item 4, amended).
- `:1165`, `:1180` the backend's `alarm_i` and `nvm_alarm_o` OR in the map alarm (DR2c; FASTCONNECT 9.2).
- `:1376-1391` the processor's port through the arbiter.

`hdl/milan/milan_datapath.sv`
- `:317-335` parameters `AMR_MS_CYC_P` (derived from the processor's timebase), `AMR_RS_TMO_MS_P` (20),
  `AMR_RS_AGG_MS_P` (1,000), `AMR_MEM_TMO_MS_P` (1,000) (DR2a, DR2c, DR3a; the port's T-NVM-PORT-DEADLINE).
- `:3154-3207` the edit face's processor nets renamed `ppo_*` and muxed with the restore's beats (`amr_own_r`).
- `:4166` GET_AUDIO_MAP waits while the map restore holds (07 5.1).
- `:4463` a restore beat is never a live write (D3 3.1).
- `:4641-4647` `amap_boot_busy_w` adds the map restore's hold (the edit face, the four CSR sites).
- `:4661`, `:4858` the roll-back: the stores take the clipped image and the RAMs are swept again (D3 8.6).
- `:4867-5727` the writer and the restore (`amr_*`): banner, record shape, source slot, payload generator, crc16,
  latch, set decode, the ms tick, deadlines and the FSM (Milan v1.2 5.3.9.1, 5.3.10.1; D3 3, 6.1, 7.1, 8.3, 8.4,
  8.6, 8.8; FASTCONNECT 4.2, 6.1; DR2a to DR2c, DR3a).
- `:6174` the format judge waits while the map restore runs (D3 8.4).
- `:9100-9118` the record face connected; `:9181` the entity enable waits for the map restore (07 5.1).

Comments only: `hdl/milan/KL_nvm_backend.sv:198-204`, `hdl/common/csr/milan_csr.sv:182-196`.

`scripts/check_nvm_record_space.py` check 15 and `scripts/nvm_contract.py` seam `PARENT_LAYOUT_EDIT`.

Tests: `tb/verilator/milan_dp/sim_nxn.cpp` `[MAPREC]` section and the window model's planted faults (read error,
silence, slow reads and writes, write errors); `dynmap_probes.vlt`; `Makefile` (`DYNMAP_MS_CYC`, `DYNMAP_AGG_MS`,
`SHADOW_SRC`); `dynmap_mutants.py` (24 arms, planting in `KL_pp_shadow.sv` too); `tb/verilator/pp_shadow/sim_main.cpp`
P2 (the bounded wait for the map restore's blank reads).

Docs: SAVED_STATE_MATERIALIZATION.md (status, 1, rule 9, 5.2, 8.4, 8.6, 10, 13, 15 items 2 and 3, 18.4
implementation record), SAVED_STATE_FASTCONNECT.md (1, 4.2, 12.2, 13), SAVED_STATE_SNAPSHOT_OWNERSHIP.md (status,
6.1, 11), MILAN_COMPLIANCE_MATRIX.md, REGISTER_MAP.md (CHMAP hold, PP_STAT[11]), FPGA_DESIGN.md,
BAREMETAL_FIRMWARE.md, MILAN_V12_ROADMAP.md, TESTING.md, the milan_dp and pp_shadow READMEs.

## New checks and planted mutants

`tb/verilator/milan_dp` dynmap leg, `[MAPREC]` section (`sim_nxn.cpp`, `dynmap_map_records_section`): 331 checks in
the leg, 0 failures (`receipts/gates/dynmap-run10.log`). Every planted control below was caught by its named check;
each clean leg passes (`receipts/mutants/`). Rows 12 to 35 are this lane's.

- Empty list, both directions: `empty: ...` and `empty, after the power cycle: ...` (rows 12, 13, 14, 34).
- Non-empty non-default list: `saved: ...`, `saved, after the power cycle: ...` (rows 15, 25).
- Torn-record control (a payload byte changed under its crc16, to a list the ADD rule would take): `torn input
  record: ...` (row 16).
- The parent's roll-back on a read error after the input was applied: `roll-back: ...` (rows 17, 18, 19).
- The D3 walk's roll-back (planted `rb_r`): `D3 roll-back: ...` (row 20).
- Held GET at the terminal and the entity enable: `held GET: ...` (rows 21, 23).
- Held SET_STREAM_FORMAT judged on the restored list: `held SET_STREAM_FORMAT: ...` (row 22).
- DR2b, an unchanged ADD writes nothing: `unchanged: ...` (row 24).
- Taint, a change during the slowed record write: `taint: ...` (row 26).
- DR2c, a record whose writes always fail: `failing writes: ...` (rows 27, 28, 29, 35).
- Per-wait deadline, silent memory: `silent memory: ...`, and the drain on a late answer (rows 30, 32).
- Aggregate deadline, slow memory: `slow memory: ...` (row 31; the leg compiles the aggregate to 300 ms, a test value).
- One device face, two initiators: `shared face: ...` (row 33).
- The parent layout literal: `scripts/check_nvm_record_space.py` check 15, control `--mutate=parent_layout`, caught
  ("the parent map writer frames layout_version 0x03 ... the donor's LAYOUT_VER_P is 0x02").

| # | Leg | Planted in | Mutant | Named check that fails | Failures |
|---:|---|---|---|---|---|
| 1 | dynmap | `milan_datapath.sv` | an empty reset: the power-on image holds no mapping | `[DYNMAP] power-on SPI 0: number_of_mappings` | 91 of 331 |
| 2 | dynmap | `milan_datapath.sv` | no clip after the restore: the window ignores a restored input format | `[DYNMAP] restored SPI 0: number_of_mappings` | 6 of 331 |
| 3 | dynmap | `milan_datapath.sv` | no output clip: the window ignores a STREAM_OUTPUT row | `[DYNMAP] window, output row staged at 4 ch: capture RAM keys 0..7 hold the output map` | 2 of 331 |
| 4 | dynmap | `milan_datapath.sv` | the boot writer never fills the crossbar RAMs | `[DYNMAP] power-on: render RAM keys 2..9 hold the input map` | 70 of 331 |
| 5 | dynmap | `milan_datapath.sv` | the CSR writer is not held while the boot writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 6 | dynmap | `milan_datapath.sv` | the input store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 2 of 331 |
| 7 | dynmap | `milan_datapath.sv` | the output store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, output: no CSR write splits the store from the RAM` | 2 of 331 |
| 8 | dynmap | `milan_datapath.sv` | the boot window ignores the CLOSED terminal | `[DYNMAP] CSR hold, input: CSR lands in both once the sweep after CLOSED has ended` | 2 of 331 |
| 9 | dynmap | `milan_datapath.sv` | no sweep after the restore's terminal | `[DYNMAP] CLOSED on the roll-back's clock: render RAM keys 2..9 hold the input map` | 6 of 331 |
| 10 | dynmap | `milan_datapath.sv` | no drain clock: busy ends while the last boot write is in flight | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 11 | dynmap | `milan_datapath.sv` | the edit face never waits for the boot writer | `[DYNMAP] edit meets the sweep: the ADD is answered only after the sweep ends` | 2 of 331 |
| 12 | dynmap | `milan_datapath.sv` | the map writer never marks a record dirty | `[MAPREC] empty: the window holds the codec's records and the pend has fallen` | 30 of 331 |
| 13 | dynmap | `milan_datapath.sv` | an empty saved list reads as an erased record (#763) | `[MAPREC] empty, after the power cycle: SPI 0: number_of_mappings` | 17 of 331 |
| 14 | dynmap | `milan_datapath.sv` | no first-dirty window: the change is written at the next tick | `[MAPREC] empty: the write waited out the 500 ms first-dirty window` | 2 of 331 |
| 15 | dynmap | `milan_datapath.sv` | the restore refuses every framed record | `[MAPREC] saved, after the power cycle: SPI 0: number_of_mappings` | 42 of 331 |
| 16 | dynmap | `milan_datapath.sv` | the restore ignores the record's crc16 | `[MAPREC] torn input record: SPI 0: number_of_mappings` | 3 of 331 |
| 17 | dynmap | `milan_datapath.sv` | a failed walk rolls nothing back | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 18 | dynmap | `milan_datapath.sv` | the roll-back sweeps the RAMs and leaves the stores | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 19 | dynmap | `milan_datapath.sv` | the roll-back puts the stores back and never sweeps the RAMs | `[MAPREC] roll-back: render RAM keys 2..9 hold the input list` | 3 of 331 |
| 20 | dynmap | `milan_datapath.sv` | the map restore runs over the D3 walk's roll-back | `[MAPREC] D3 roll-back: SPI 0: number_of_mappings` | 6 of 331 |
| 21 | dynmap | `milan_datapath.sv` | GET_AUDIO_MAP does not wait for the map restore | `[MAPREC] held GET: answered with the restored list` | 1 of 331 |
| 22 | dynmap | `milan_datapath.sv` | the format judge does not wait for the map restore | `[MAPREC] held SET_STREAM_FORMAT: SUCCESS against the restored list` | 2 of 331 |
| 23 | dynmap | `milan_datapath.sv` | the entity enable does not wait for the map restore | `[MAPREC] held GET: the entity enable waits for the map restore` | 1 of 331 |
| 24 | dynmap | `milan_datapath.sv` | every phase-5 beat marks its record, changed or not (DR2b) | `[MAPREC] unchanged: no record write follows an unchanged edit` | 3 of 331 |
| 25 | dynmap | `milan_datapath.sv` | a restore write counts as a change | `[MAPREC] saved: the restore itself writes no record` | 2 of 331 |
| 26 | dynmap | `milan_datapath.sv` | a change after the latch does not taint the write | `[MAPREC] taint: the window ends on the final list` | 5 of 331 |
| 27 | dynmap | `milan_datapath.sv` | a fourth attempt follows the third failure | `[MAPREC] failing writes: three attempts, then no more` | 1 of 331 |
| 28 | dynmap | `milan_datapath.sv` | no backoff between attempts | `[MAPREC] failing writes: the attempts are at least 500 ms apart` | 1 of 331 |
| 29 | dynmap | `milan_datapath.sv` | the last failed attempt raises no alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 30 | dynmap | `milan_datapath.sv` | the map restore has no per-wait deadline | `[MAPREC] silent memory: the walk ends at its per-wait deadline` | 1 of 331 |
| 31 | dynmap | `milan_datapath.sv` | the map restore has no aggregate deadline | `[MAPREC] slow memory: SPI 0: number_of_mappings` | 8 of 331 |
| 32 | dynmap | `KL_pp_shadow.sv` | the arbiter does not drain a read the map writer abandoned | `[MAPREC] silent memory, late answer: a later change reaches the window` | 1 of 331 |
| 33 | dynmap | `KL_pp_shadow.sv` | the arbiter's selection moves while the backend serves a command | `[MAPREC] shared face: both writers' records are in the window` | 1 of 331 |
| 34 | dynmap | `KL_pp_shadow.sv` | the map writer's pending is not reported | `[MAPREC] empty: PP_STAT pend rises with the accepted change` | 1 of 331 |
| 35 | dynmap | `KL_pp_shadow.sv` | the map writer's alarm does not reach nvm_alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 36 | listener | `milan_datapath.sv` | an empty reset, under the listener's end-to-end check | `T18 POWER-ON: with no map command since the reset, the lane renders injected events` | 8 of 264 |
| 37 | talker | `milan_datapath.sv` | an empty reset, under the talker's end-to-end check | `[V] every requested column was decoded` | 20 of 134 |

One arm survived the first full run: row 22, the format judge. The held SET_STREAM_FORMAT reached its judge after the
input port was already restored, so the hold made no difference. The scenario now slows the input record's lanes by
250 clocks (the whole hold stays inside the 4,096-clock gather watchdog) and adds the premise "...while the input port
still held its reset set"; the row was then caught (`receipts/mutants/mutant-22.log`) and caught again in the final
run.

## Resource / timing

Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `--single-thread-synthesis`, Vivado 2026.1 under
the exclusive lock, `pp_resource_gate.py check --endpoint route-1x1`); driver `receipts/route-1x1/route.sh`, each run
on a clean clone.

| Route-1x1 | LUT | FF | SLICE | RAMB36 | RAMB18 | DSP | WNS ns | WHS ns | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| base `e9cbb676` | 49,613 | 52,353 | 15,725 | 74 | 25 | 14 | +0.215 | +0.036 | rc 0 (equals the accepted record) |
| first head `6ab04441` | 50,203 (+590) | 52,699 (+346) | 15,720 | 74 | 25 | 14 | +0.479 | +0.036 | rc 1: LUT grew by more than 500 |
| head `90b15366` (logic of the final head) | 49,902 (+289) | 52,615 (+262) | 15,801 (+76) | 74 | 25 | 14 | +0.316 | +0.015 | rc 0 |

- The first head's +590 LUT was +525 in `milan_datapath`'s own logic. `90b15366` cut it: the deadlines count
  milliseconds (11-bit counters), one crc16 step is shared, the byte counter is 11 bits, the header is judged as it
  streams, the owner compares use the bits an owner can differ in, and REMOVE reads the clip instead of the live
  store (equal at restore time, by the holds). Post-synthesis: +619 to +445.
- `u_nvm` grows by +153 to +164 in every head, from the arbiter's muxes on the backend's request inputs. The rest of
  the movement is the optimizer's in unrelated blocks (gPTP shadow about -285, CSR +100).
- DR4's maps-stage ceiling is 1,250 LUT / 600 FF incremental; the head uses +289 / +262.
- Route complete at every head, no unrouted net. WHS stays positive (+0.015 ns).
- `git diff 90b15366 HEAD -- hdl` is empty (only tests and docs after it).

Standalone `KL_pp_shadow` (the recipe's standalone measurements, `--integrated-clock`; the 8x8 parameter block from
the recipe's RTL-only elaboration of the 8x8 export), `pp_resource_gate.py check`:

| Endpoint | base LUT / FF | head LUT / FF | delta | gate (base, head) |
|---|---|---|---|---|
| ooc-1x1 | 23,314 / 19,821 | 23,366 / 19,823 | +52 / +2 | rc 0, rc 0 |
| ooc-8x8 | 30,211 / 27,451 | 30,282 / 27,451 | +71 / 0 | rc 0, rc 0 |

Both bases equal the accepted records. RAMB36, RAMB18 and DSP are unchanged at every endpoint. The head of these
runs is the routed head `90b15366`.

## Gates

All commands unpiped, one log and rc each; logs in `receipts/gates/` and `receipts/final/`. Python gates ran under
CPython 3.12.3 (the hosted runner's) with the hash-locked Markdown, HDL-reference and PyYAML pins, except the suite
sweep: its process-ownership preflight needs `os.pidfd_open`, which that 3.12.3 build lacks, so the sweep ran under
the host's CPython 3.14.8 (PyYAML 6.0.3). Verilator 5.050 (pinned), Yosys 0.66 (the workflow's sha), sv2v v0.0.12.

| Gate | Head | rc |
|---|---|---|
| `scripts/lint_rtl.py --check --self-test` | `79f8aa89` (hdl = final) | 0 (`hdl/milan` 2 of ratchet 2) |
| `scripts/pp_srcs.py --check --selftest` | `79f8aa89` | 0 |
| `scripts/xvlog_gate.py --check`, `--selftest` (under the Vivado lock) | `79f8aa89` (hdl = final) | 0, 0 (0 findings) |
| `syn/yosys/run.sh` | `e3105d21` (hdl = final) | 0 (58 of 58 tops; tap purity PASS) |
| `syn/ooc` and `syn/yosys` self-tests (12, as `rtl-fast` runs them) and `pp_resource_gate_mutants.py` | `79f8aa89` | all 0 |
| `scripts/check_nvm_record_space.py`, `--self-test` | `79f8aa89` | 0, 0 (22 controls, `parent_layout` among them) |
| `scripts/check_nvm_capture.py` (its controls included) | `79f8aa89` | 0: census, clocks, both timing arms and receipt agree, so no re-measure is owed |
| docs: `docs_check`, `check_doc_paths`, `check_doc_style` (+selftest), `gen_toc --check`, `check_em_dash --base e9cbb676` (+selftest), `check_feature_status`, `check_gptp_docs` (+selftest), `check_solution_docs` (+selftest), `check_submodule_docs` (+selftest), `check_wire_accountability --self-test`, `ci_scope --selftest`, `check_baremetal_only --check`, `gen_hdl_reference --selftest` and build | final | all 0 |
| `make -C tb/verilator/milan_dp dynmap` | `79f8aa89` (leg unchanged since) | 0, 331 checks, 0 failures |
| `make -C tb/verilator/milan_dp dynmap-mutants` | `79f8aa89` | 0, 37 of 37 caught |
| `make -C tb/verilator/pp_shadow` | `cf5c0c23` | 0 (610, 610, 650, 317 checks) |
| `scripts/run_all_suites.sh`, first run | `79f8aa89` | 1: 62 of 63 suites; `pp_shadow` P2 failed (see below) |
| `scripts/run_all_suites.sh`, final | `63a187e1` | 0: 63 of 63 suites, 2,186,578 checks, 0 failures, 0 timed out (4 declared `tsn_fuzz` skips: the external generator is absent) |
| docs, lint, `pp_srcs`, record-space, capture, HDL reference at the head | `63a187e1` | all 0 (`receipts/final/`) |
| route-1x1, ooc-1x1, ooc-8x8 | see Resource / timing | 0 |

**The first sweep's one failure, and its fix.** `pp_shadow` P2 read `PP_NVM_STAT[4]` (`dev_busy`) right after the
restore walk and found an operation in flight. It was the map restore's blank read of record `0x60`: a probe showed
the bit clear 20 idle clocks later. Since #637 that read follows the D3 terminal by design. The check now waits up to
2,000 clocks for the device face to go idle, graded as its own check, and then asserts the original condition
unchanged (`cf5c0c23`).

**Its planted control** (`receipts/ppshadow-control/`). A map restore that never takes its read bytes and has no
per-wait deadline (`hold-control.diff`) fails the new check, "PP_NVM_STAT[4]: the map restore's blank reads end
within 2,000 clocks", and the original one: 610 checks, 2 failures. Never taking the bytes alone is healed by
design: the 20 ms per-wait deadline fires and the arbiter's drain completes the read, so the face still goes idle in
bound (`rready-only-healed.log`). Reproduce from `tb/verilator/pp_shadow`, with the two edits applied to a copy at
`<dir>/hdl/milan/milan_datapath.sv` (the suite's waivers match that path):

```sh
SRCS=$(MAKEFLAGS= make -s --no-print-directory -C ../milan_dp print-srcs | tr ' ' '\n' | sed "s|.*/hdl/milan/milan_datapath.sv$|$DIR/hdl/milan/milan_datapath.sv|" | tr '\n' ' ')
make run-base BUILD_DIR="$DIR/obj" "DP_SRCS=$SRCS"
```

## Acceptance (issue #637 and the #763 additions)

| Item | Met | Evidence |
|---|---|---|
| 1. Restore at boot under the D3 rules (well-formed only; torn or corrupt keeps the default) and reset on a roll-back | yes, with one stated deviation (one read pass) | `[MAPREC]` saved, torn, roll-back, D3 roll-back, silent and slow memory; rows 15 to 20, 30, 31 |
| 2. The contract and design pages state the ownership; the processor's amended D3 contract matches | yes | D3 page status, 1, 5.2, 8.4, 15 item 2, 18.4; FASTCONNECT 1, 4.2, 12.2, 13; snapshot page 6.1, 11; processor `07_memory_maps.md` 5.1 and `KL_aecp_nvm_writer.sv:93-97,119-121` and `07_memory_maps.md:584-610` at the pin |
| 3. A parent check plants a power cycle after a map change and the maps return; a torn-record control keeps the default | yes | `[MAPREC]` empty, saved, torn |
| 4. Capture timing and census unchanged, or re-measured | unchanged | `scripts/check_nvm_capture.py` rc 0 at the head (census, clocks, both arms and the receipt agree) |
| #763: an EMPTY list in both directions and a non-empty non-default list survive a planted power cycle | yes | `[MAPREC]` empty and saved, GET_AUDIO_MAP and both crossbar RAMs |
| #763: the record format is kept (FASTCONNECT 6.1, D3 8.3 V3g) | yes | the window equals the repository codec's framing byte for byte; the empty list is a framed record of UNUSED entries |
| #763: checked on the board with a cold cycle | NOT done | no bench access in this lane |

## Open risks and questions

- The deviation: one read pass instead of the processor's two (D3 18.4, implementation record). A reviewer may want it ruled.
- The faces' hold (553 to 635 clocks here) is measured against a zero-latency window model; DDR latency adds to it, against the 4,096-clock gather watchdog.
- The entity enable now reaches the processor after the map restore, so the side port's image-window lock, which follows the requested enable, engages that much later.
- The sweep ran under CPython 3.14.8, because the CI-matching 3.12.3 build lacks `os.pidfd_open`; the other Python gates ran under 3.12.3.
- Multi-port ordering at 8x8, and the name stage (lane 3), as in the PR body's limitations.
