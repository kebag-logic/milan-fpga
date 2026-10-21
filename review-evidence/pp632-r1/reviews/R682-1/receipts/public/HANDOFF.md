# A659: milan-fpga #632 + #764 (phase-align the recovered media clock to the followed CRF)

## Round 3b (session 8, 2026-10-21 12:23 to 14:48) -- option (b) committed in the processor

**Status: REVIEW READY** posted on #632 with both heads: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6316365497 (text: `public-review-ready-r3b.txt`; URL also in
`public-review-ready-r3b.posted.txt`). Every item of the round 3b assignment done; every gate it touches rc 0.

Ruling: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6312625146 ([A10], option (b); the STOP
condition "more than the one gather change" waived for these five words; R677-2's four-step case stays as
specified). Scope of this round, and only this: (1) the processor commit with its test and planted defects, (2) the
milan_dp re-measure with the committed processor head applied uncommitted to the submodule, (3) docs/receipts in
milan-fpga. The listener render queue was NOT started (next round). TAKEN not re-posted. Nothing pushed.

**Heads.** milan-fpga `3fdaea3d2adee05c41629363bffbf32cff5b0656` on `32fb8fc2` (one docs commit). Processor `51f88c7e14e7e2527c09ff9a23b93dd6b857fd50` on
branch `632-sinfo-notify-stored` at processor main `08023123` (origin checked: the protocol-processor repository, the
same URL as the milan-fpga submodule's; branch base verified `08023123` before committing). The milan-fpga submodule
is at its pin `2cbed0a9`, status clean, after the measurement.

### Processor commits (on `08023123`, oldest first)

| Commit | Subject |
|---|---|
| `175a5a15` | Compare SET_STREAM_INFO's offset with the stored row once a controller set it and with the integrator's factory word before, so the push follows the offset as set (milan-fpga #632) |
| `0b097464` | Re-record tb/aecp_cmds' decode sweep against the ROM with SET_STREAM_INFO's stored-row compare |
| `51f88c7e` | Measure D3S5's SET_STREAM_INFO latency on a row already set, the arm its timed SET takes, since E_SINFO's two arms reach the store a cycle apart |

`0b097464` exists because `make check`'s AECP command gate refused `175a5a15` alone: `tb/aecp_cmds/decode.json`
records the ROM digest its sweep ran on. Re-recorded through its own target (`make -C tb/aecp_cmds record`, 617,916
trials, 176 checks pass): the digest line alone moved. No amend.

### D9: D3S5's premise took the never-set arm's latency (found by the sweep at `0b097464`, fixed)

`tb/pp_top` D3S5 places an NVM WRITE's done on the store's accepting cycle of a SET_STREAM_INFO, using the latency
of an earlier SET measured on the same row. With option (b) that earlier SET ran on a row never set (the GSI(3)
arm) and the timed SET on a set row (the stored arm), which reaches the store one cycle later: "D3S5 premise: the
change accepted at 315227, the WRITE's done at 315228" (the only failure of the first build; `make run` then ran
none of pp_top's six later builds). `51f88c7e` sets the row first and measures on the arm the timed SET takes; the
premise is graded as before (`primed` added to it). The D3 control graded by D3S5 (`clear_wins_same_edge`) is still
killed, and the other eleven D3 controls graded by section S were re-run at the head (gate table). Receipts of the
superseded run: `receipts/round3/processor_0b097464_superseded/`. The E_SINFO block and the ROM are identical at
`0b097464` and `51f88c7e` (`hdl/` unchanged), so the milan-fpga measurement holds for the head.

### milan-fpga commit (on `32fb8fc2`)

| Commit | Subject |
|---|---|
| `3fdaea3d` | Record that SET_STREAM_INFO's push compares with the stored offset once set and with the factory offset in force before, as the processor gate ruled for #632 |

`docs/design/MEDIA_CLOCK_FOLLOWING.md:1694-1705`: the design doc said only "a processor whose gate reads the offset
as set"; the ruled form compares with GET_STREAM_INFO's word on an output never set, so the doc now states both
arms, the SET of 0 on a never-set output, and the factory-row residue. Docs gates 49/49 at `3fdaea3d`.

### Changes (file:line at the processor head; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/aecp/ucode/gen_ucode.py:2434-2466` | E_SINFO: `READ_ST RGN_DYNV + SEL_PTOFF`, COMPARE, `BR_STATUS` -> the unset arm; set arm `READ_ST RGN_DYN + SEL_PTOFF` (the anchor of milan-fpga's mutant 9, kept byte-exact), `BRANCH`; unset arm `GATHER_EXT GSI(3)`; skip target `E_SINFO + 17`; three asserts on the branch targets and END. 13 -> 18 words of a 32-word slot; ROM words 1859..1873 alone differ from main's | Milan v1.2 5.4.5.2, 5.4.2.9, 5.4.2.10.2; IEEE 1722.1-2021 7.5.2 |
| `tb/pp_top/sim_main.cpp:1286-1299`, `:2018-2021` | `gsi_ptoff_applied`: the face answers a Stream Output's GSI(3) as milan-fpga's integrator does (row rounded up to whole 48 kHz periods once set, factory 2,000,000 ns before); off everywhere but NS | 5.4.2.10.2; IEEE 1722-2016 10.7 Eq. (14) |
| `tb/pp_top/notify_phases.hpp:1131-1201`, `:2349-2352` | section NS, run by `run_pushes` after NP on its own model | 5.4.5.2 |
| `tb/pp_top/notify_mutants.py:228-243` | two planted defects | -- |
| `tb/pp_top/README.md:69-73`, `:2484`, `:2661-2698`, `:2997-3003`, `:3029-3036` | D3S5's measurement, NS in the run list, section NS (with the residue), the mutation record (137 controls; four rows' counts moved) | -- |
| `tb/pp_top/d3_phases.hpp:640-682` (`51f88c7e`) | D3S5 sets the row first and measures the latency on the arm its timed SET takes (`primed` in the premise) | -- |
| `docs/architecture/06_aecp_engine.md:522`, `09_verification.md:184`, `:318` | the chain names the compare and the residue; NS on both arms of the A/B row; the 8.4 evidence row | -- |
| `tb/aecp_cmds/decode.json` | the ROM digest (`0b097464`) | -- |

### New checks (planted mutant, failing words)

pp_top section NS (`--notify-only`): A and B registered (NS0); NS0b premise (no row set, GET 2,000,000 on both);
NS1 output 1 SET 2,000,000 on a never-set row: nothing; NS2 output 0 SET 0 on a never-set row: one push, byte-exact;
NS3 2,010,000: one push, NS3b GET reads 2,020,834 (premise); NS4 2,010,000 again: nothing; NS5 2,020,834: one push.
20 checks. The ruled four: identical SET pushes nothing (NS4), changed SET pushes once (NS3, NS5), SET 0 on a
never-set row pushes once (NS2), first SET equal to the factory value pushes nothing (NS1).

| Mutant | Planted | Failing words (all named checks fail, nothing else) |
|---|---|---|
| `stream_info_compare_applied` (the planted defect: the GSI(3) compare restored) | set arm's stored read -> `GATHER_EXT GSI(3)` | "NS4 ... again: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller and 0 at the requester"; "NS5 ..., the value GET read, a change: exactly one unsolicited response of this command at the other registered controller, got 0" |
| `stream_info_unset_arm_dropped` (the never-set arm control) | the unset arm's `BR_STATUS` a NOP: option (a) | "NS1 ... on a row never set: an unchanged offset pushes nothing (Milan 5.4.5.2), got 1 at the other controller"; "NS2 ... on a row never set: exactly one unsolicited response of this command at the other registered controller, got 0" |

Moved by NS (re-measured, README updated): `enq_dropped_stream_info` 1 -> 4 (NP3, NS2, NS3, NS5),
`stream_info_get_body` 1 -> 4 (same), `requester_not_excluded` 12 -> 15, `entry_seq_not_advanced` 13 -> 15. The
other eighteen `--notify-only` controls fail exactly their recorded checks.

### The consumer re-measure (milan-fpga, `receipts/round3/notify_sinfo_pp_0b097464/`)

The processor head is 50 commits past the pin. Its gen_ucode.py diff does not apply at the pin with three lines of
context (a later comment differs), and with one line its third hunk lands on another `])` 33 lines away (it would
have put the asserts in the wrong block). So `scripts/round3b/splice_sinfo.py` replaced the pin's E_SINFO block (and
nothing else) with the head's, each found exactly once; `submodule_applied.diff` is exactly the committed hunk. The
ROM it emits is `f9954a76...`, byte-identical to round 3's option (b) ROM, words 1859..1873 alone differing from the
pin's `518b900c...`, and those words equal the processor head's own ROM.

| Measure (lane `32fb8fc2`, submodule pin + head's E_SINFO, uncommitted) | Result |
|---|---|
| `make notify` (the timed leg, 1x1) | rc 0, 441 checks, 0 failures; pushes 0, 1, 0, 1 at steps 1..4; GET 2,000,000 / 2,020,834 / 2,020,834 / 2,041,667 |
| `python3 gsi_mutants.py 9` (the planted control) | rc 0: clean leg PASS; mutant caught at "[NOTIFY] SET_STREAM_INFO step 3: 2,010,000 ns again modifies nothing" (3 failures of 441) |
| never-set probe (disposable, scratch clone at `32fb8fc2`, `scripts/round3b/sinfo_never_set_probe.py`) | rc 0, 444 checks, 0 failures: SET 0 on the CRF output's never-set row pushes once; GET then 0; SET 2,000,000 back pushes once |
| submodule after | `2cbed0a9`, status empty; milan_dp's ignored `ucode.hex` regenerated from the pin (`518b900c...`) |

The docs commit `3fdaea3d` touches no simulated input, so the measurement at `32fb8fc2` stands at the head.

### The residue (recorded by ruling, not a finding)

Before a row's first SET the compare reads the integrator's GSI(3), the offset as applied: a factory row that is
not whole periods compares with its applied value, so a SET of exactly that factory value would push. No shipping
configuration has such a row (every factory row is 2 ms, whole periods). Recorded in the processor README section
NS, 06's chain, the milan-fpga design doc, PP-PR-BODY.md and PR-BODY.md.

### Resources

No gateware structure changes this round: milan-fpga's commit is docs only, and the processor change is ROM content
(the 2048-word ROM keeps its size; five more words placed in E_SINFO's existing 32-word slot). Route not re-run; the
round 3 route at `62ee1a8c` stands. The pin adoption that brings the new ROM is a later round's.

### Gate table (round 3b)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| processor docs gates | `make check` | `51f88c7e` (and `0b097464`) | rc 0: lint, wavedrom, links, matrix, req-tags (231 tags), modmatrix, params, aecpcmd (selftest 231 of 231; 31 commands), ids, figures, stale. At `175a5a15` alone: aecpcmd refused (decode.json's ROM digest), fixed by `0b097464` | `receipts/round3/processor_51f88c7e/make_check.log` |
| processor HDL lint | `./scripts/lint_hdl.sh` | `51f88c7e` | rc 0 | `processor_51f88c7e/lint_hdl.log` |
| processor suites | `REQ_TAG_LOG=... ./scripts/run_suites.sh` (CI's step) | `51f88c7e` | rc 0: every suite PASS, 1,030,329 checks, 0 failing; `pp_top` 10,741 over its seven builds; `ucpu` 447; `aecp_cmds` 176; `aecp_notify` 131. At `0b097464`: `pp_top` failed D3S5's premise (D9) | `processor_51f88c7e/suites.txt`; `processor_0b097464_superseded/` |
| processor traceability, executed half | `python3 scripts/check-req-tags.py --suites ... --evidence ...` | `51f88c7e` | rc 0: 231 evidence lines, 14 suites | `processor_51f88c7e/req_tags_executed.log` |
| notify controls (`--notify-only`) | `notify_mutants.py --jobs 1 --only` the 22 | `51f88c7e` (and `0b097464`) | rc 0: goldens PASS, 22 of 22 KILLED by their named checks; the two new ones fail NS4+NS5 and NS1+NS2 | `processor_51f88c7e/campaigns/notify.*` |
| D3 controls graded by section S | `d3_mutants.py --jobs 1 --only` the 12 | `51f88c7e` | rc 0: goldens PASS, 12 of 12 KILLED, each failing exactly its recorded count (3, 2, 1, 18, 14, 2, 5, 2, 2, 1, 2, 1) | `processor_51f88c7e/campaigns/d3.*` |
| AECP command decode controls (CI) | `python3 -B tb/aecp_cmds/mutants.py --jobs 1` | `51f88c7e` | rc 0: 17 of 17 detected by their named failures; golden and restored PASS | `processor_51f88c7e/campaigns/aecp_cmds.*` |
| AECP dispatch controls (CI) | `aecp_dispatch_mutants.py --jobs 1` | `51f88c7e` | rc 0: the four controls (aecp-dispatch, aecp-line, d3, line-guards) PASS, then 69 of 69 planted defects KILLED by their named checks; 73 checks, 0 failures | `processor_51f88c7e/campaigns/aecp_dispatch.*` |
| AECP deadline and hazard controls (CI) | `aecp_mutants.py --jobs 1` | `51f88c7e` | rc 0: six controls (pp_top budget, d3, deadline, hazards, timer-defaults; ucpu) PASS, then 61 of 61 planted defects KILLED; 67 checks, 0 failures | `processor_51f88c7e/campaigns/aecp.*` |
| ucode generator | `python3 hdl/aecp/ucode/gen_ucode.py` (also inside every suite's build) | `51f88c7e` | 2048 words, 92 programs; ROM differs from main's at 1859..1873 alone | `notify_sinfo_pp_0b097464/digests.sha256` |
| milan_dp notify leg, the processor head's E_SINFO applied | `make -C tb/verilator/milan_dp notify` | lane `32fb8fc2` + processor `0b097464` = `51f88c7e` E_SINFO | rc 0: 441 checks, 0 failures | `receipts/round3/notify_sinfo_pp_0b097464/` |
| its planted control | `python3 gsi_mutants.py 9` | same | rc 0: clean PASS; caught at step 3 (3 of 441) | same |
| never-set probe (disposable) | `make notify` with the probe, scratch clone | same | rc 0: 444 checks, 0 failures; SET 0 pushes once | same |
| milan-fpga docs gates (49) | `scripts/docs_gates.sh` (round-3 runner) | `3fdaea3d` | 49 of 49 rc 0 | `receipts/round3/docs-gates-3fdaea3d/` |

Not run this round, with reason: the milan-fpga sweep, media_phase, route, Yosys, lint and builder (no input changed
since `32fb8fc2`: `3fdaea3d` is one design document); the processor's SRP, MAAP and ADP campaigns, Yosys and
elaboration guards (no input changed: the processor change is ROM content and tb/pp_top); the full D3 campaign's
other 98 controls (graded by sections the change does not touch; the D3S5 setup change is equivalent for them).

### Environment notes (round 3b)

- One exploratory run of all 22 `--notify-only` mutants (before the receipts) used `--jobs 3`, three builds at once,
  against the two-build cap; memory stayed under 1 GB. Every receipt run used `--jobs 1` beside at most one other
  build. A first slot-2 launch at the head would have run tb/aecp_cmds' `make mutants` at its default four jobs; it
  was stopped seconds in (during the notify golden) and relaunched with `--jobs 1`.
- The probe of round 3 anchored on the call before `28510858`; the round 3b copy anchors on the timed-leg call.
- Processor gates ran in clean clones at the head under scratch; no build product in either checkout.

## Round 3 (session 7, 2026-10-21 04:36 to 12:40) -- STOP on the processor gate (STOP condition 2)

STOP posted: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6313646784 (text: `public-stop-r3.txt`),
head `32fb8fc2`, no processor commit. TAKEN not re-posted. Not pushed.

Assignment: https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306591168, answering R678-2
(issuecomment-6306376430) and R677-2 (issuecomment-6306520485). Base `2ff30f0d`, new commits on it (no rebase, no
amend). Processor clone `$LANES/632-pp` (private path), branch `632-sinfo-notify-stored` at processor main
`08023123` (origin checked: the same repository URL as the milan-fpga submodule's). **No processor commit**: see the
STOP below. The milan-fpga submodule stays at its pin `2cbed0a9`, clean (`git -C protocol-processor status` empty);
the processor change was applied to it uncommitted only for the milan_dp measurements, then restored.

### The STOP: the one-read processor fix does not meet the ruled case

The ruling's fix is one word in E_SINFO: `READ_ST rd=6, RGN_DYN + SEL_PTOFF` in place of `GATHER_EXT rd=6, GSI(3)`
(option (a), `receipts/round3/notify_sinfo/option_a.diff`). Measured on the real datapath and processor (the
committed `milan_dp` `[NOTIFY]` case, the notify leg, 1x1), with the microcode applied uncommitted to the
submodule at its pin:

| Processor | step 1 (2,000,000, held) | step 2 (2,010,000) | step 3 (2,010,000 again) | step 4 (2,020,834) | never-set CRF row: SET 0 (probe) | leg |
|---|---|---|---|---|---|---|
| pin `2cbed0a9` (GSI(3) gate) | 0 | 1 | **1** (exp 0) | **0** (exp 1) | 1 | 444 checks, 3 failures |
| option (a): the one read, as ruled | **1** (exp 0) | 1 | 0 | 1 | **0** (exp 1) | 444 checks, 2 failures |
| option (b): stored row once a controller set it, the integrator's word before | 0 | 1 | 0 | 1 | 1 | 444 checks, 0 failures |

Cause: the processor's dynamic store reads a row no controller has written as 0 with its valid bit clear
(`KL_aecp_dyn_state.sv`, `ptoff_r` reset 0, `ptoff_v_r` 0; the integrator serves the factory 2 ms meanwhile). In
the notify leg no SET has touched output 0 before `[NOTIFY]`, so option (a) compares 2,000,000 with 0 and pushes
at step 1, and a SET of 0 on a never-set row compares 0 with 0 and pushes nothing although the offset in force
moves from 2 ms to 0 (a missed 5.4.5.2 notification the base and the pin both send). Option (b) is the store's own
idiom for this, as E_SCFG does for #178 (`RGN_DYNV` valid read, COMPARE, BR_STATUS; the stored row if set, else the
integrator's GSI(3)): five more words (`option_b.diff`), the gather kept on the never-set arm. Its residue: before
the first SET a factory row that is not whole periods compares with its applied value (no shipping config has one;
every factory row is 2 ms). Decision needed: (a) as ruled, with R677-2's step 1 re-specified and the never-set SET
0 recorded as a follow-up, or (b). Either way the processor PR, its test and its planted defect follow the ruling.

Measured with option (b) uncommitted at `fe3ff999` (`receipts/round3/notify_sinfo/`): notify leg 441 checks, 0
failures; `gsi_mutants.py 9` (the planted control restoring the applied-readback compare) caught at "[NOTIFY]
SET_STREAM_INFO step 3" (3 failures of 441). At the pin: the clean leg fails steps 3 and 4 and the control reports
its pattern absent (0 PASS, 2 FAIL), as designed. Recorded: the committed case fails at the current pin.

### Round 3 commits (on `2ff30f0d`, oldest first)

| Commit | Subject |
|---|---|
| `81f09d06f` | Carry each rounded offset's bit 32 into the CRF output's 64-bit timestamp, and read a row past 32 bits back through GET_STREAM_INFO as 0xFFFFFFFF |
| `f36177f9b` | Grade every offset row on all 33 bits and every CRF timestamp on 64 at the 2^32 boundary, in reset and at run time, and the detector after a hold onto the fold, each with a planted defect |
| `fe3ff9999` | Grade SET_STREAM_INFO's push against the offset as set in four steps on the wire, with the microcode gate's applied-readback compare planted |
| `45633bd1c` | Drop review labels from the #632 source comments |
| `d790dd442` | Document the offsets' carry past 2^32 and GET_STREAM_INFO's saturated word, the SET echo against the applied readback, the push judged on the value set, and the listener out of this PR (#632) |
| `cf85a578b` | Document the rounder's readback row without a unit and hold the #632 changelog and render-latency lines to the style limits |
| `aea19ce73` | Record media_phase's default target at 553 s and its thirty-three-mutant campaign at 1,396 s on two jobs |
| `62ee1a8cc` | Write each rounded row's low word and carry as two indexed writes, its reset value from an elaboration table, since Yosys drops an indexed concatenation target and kept no cell of the rounder |
| `28510858b` | Run the SET_STREAM_INFO push case on the timed leg alone, the one leg whose output 0 still holds its factory offset when the section starts |
| `32fb8fc26` | Record that milan_dp's pool starts no leg after the notify leg while the processor pin's SET_STREAM_INFO gate reads the applied word |

**Head: `32fb8fc26acf7dedc507512d7a455898a26afd84`** (not pushed; no rebase, no amend). Processor: no commit.

### D8: the case's premise held on one leg only (found by the sweep, fixed)

`fe3ff999` ran the four steps in every `[NOTIFY]` (the timed leg and the nxn legs). The nxn legs' whole-model walk
leaves output 0 at 750,000 ns (#67) before `[NOTIFY]`, so step 1's "the offset held" was false there and its push
was right: the sweep's N=4 leg failed step 1 (`receipts/round3/sweep_62ee1a8c/shard0/milan_dp_failures_extract.txt`).
`28510858` runs the case on the timed leg alone, R677-2's leg, where nothing sets the row first. The same sweep
showed that `sim_pool.py` starts no leg after a failure, so at this pin the designed notify failure hides seven later
legs; `32fb8fc2` documents it, and the legs were run on their own at the head (gate table).

### D7: the rounder synthesized to nothing in Yosys (found this round, fixed)

`81f09d06` wrote each row as `{ofs_c_o[row_r], ofs_ns_o[32*row_r +: 32]} <= dv_quot_r[32:0];` (and the reset loop
likewise). Verilator and Vivado take it (the route at `81f09d06` kept `pres_round` at 149 LUT / 193 FF), but Yosys
0.66 through sv2v v0.0.12 drops a concatenation target with an indexed part: every output undriven, and
`KL_mtt_round` synthesized to **0 cells** (round 2: 1,084). `syn/yosys/run.sh` still printed `[PASS] KL_mtt_round
cells=0` (`receipts/round3/yosys_small_tops_aea19ce7_zero_cells/`). Fix `62ee1a8c`: two indexed writes, the reset
values from an elaboration-time table `RESET_RND_C`; Yosys 1,215 cells. The three mutants anchored on those lines
were re-anchored and re-killed (`receipts/round3/media_phase_ofs_62ee1a8c/`). Follow-up for the manager (new work,
not this lane's): the Yosys gate accepts a top whose synthesis kept zero cells; a floor (cells > 0, or a per-top
recorded minimum) would have caught this.

### Outcome per item

| Item | Status |
|---|---|
| R678-2-F1 (MAJOR) CRF carry | done: `81f09d06` (portable form `62ee1a8c`, D7), graded `f36177f9` |
| R677-2-F1 (MAJOR) processor gate | **STOP** (above); milan_dp case and planted control committed (`fe3ff999`, on the timed leg alone `28510858`), measured with every form at `fe3ff999` and form (b) again at `32fb8fc2`; docs scoped (`d790dd44`, `32fb8fc2`); follow-up recorded below |
| R677-2-F2 (MINOR) hold restarts the reference | done: `f36177f9` (`det afterhold`, `hold_keeps_ref`) |
| R677-2-F3 (MINOR) PR body figures | done in PR-BODY.md (404 LUTs and 8 slices; twenty-eight, now thirty-three) |
| R677-2-R1, R678-2-R1 comment labels | done: `45633bd1` and the files of `81f09d06`/`f36177f9`/`fe3ff999` (no `R67x-n-Fn` left in any source comment) |
| R677-2-R2 datapath fold comment | done (`81f09d06`, the R677-2 wording) |
| R677-2-R3..R5, R678-2-R2 listener scope | done: design doc, TIME_SYNC, CHANGELOG (`d790dd44`, `cf85a578`), PR body |
| S1..S4 (optional) | not taken: S2's guard would restrict factory rows, which the carry now serves in full |

### Changes (file:line at `cf85a578`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mtt_round.sv:99` | `ofs_c_o`: each row's bit 32 | IEEE 1722-2016 10.7 Eq. (14), 10.4.13.1 Eq. (13) |
| `KL_mtt_round.sv:101-103`, `:217-219` | `rb_row_i`/`rb_ns_o`: GET_STREAM_INFO's readback of a row, saturated at 0xFFFFFFFF past 32 bits | Milan v1.2 5.4.2.10.2 |
| `KL_mtt_round.sv:129-138`, `:177`, `:210` | `g_carry` guard (33 bits hold the largest rounding); `round_c` 33 bits; reset and conversion load the carry | 10.7 Eq. (14) |
| `hdl/ieee1722/crf/KL_crf_tx.sv:160`, `:401` | `transit_c_i` (defaulted 0), added into the 64-bit sum at `ROUND_MTT_P = 0`; `:308` unused with the converter | 10.4.13.1 Eq. (13), 10.7 Eq. (14) |
| `hdl/milan/milan_datapath.sv:3452-3475`, `:5001`, `:5255`, `:6395` | carry vector, readback index, GSI word 3 from `rb_ns_o`, CRF output's carry | 5.4.2.10.2, 10.4.13.1 |
| `milan_datapath.sv:3418-3420`, `:3429-3444` | R677-2-R2 fold comment; the SET echo against the readback, the gate on the value set | 5.4.2.9, 5.4.2.10.2, 5.4.5.2 |

No top-level port, no register-map change. Module ports added: `KL_mtt_round` `ofs_c_o`, `rb_row_i`, `rb_ns_o`;
`KL_crf_tx` `transit_c_i` (defaulted, so every other instance is unchanged).

### New checks (planted mutant, failing words)

media_phase campaign, 28 -> 33 mutants:

| Mutant | Harness / case | Required failing check |
|---|---|---|
| mtt_carry_dropped | ofs | `[ofs C] every row reads back as applied, rounded up to whole periods, all 33 bits` |
| mtt_reset_carry_dropped | ofs | `[ofs A] in reset every row reads its factory value rounded up to whole periods, all 33 bits` |
| readback_saturation_dropped | ofs | `[ofs C] GET_STREAM_INFO reads every row as applied, 0xFFFFFFFF past 32 bits` |
| crf_carry_dropped (the planted truncation) | ofs | `[ofs C] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14` |
| hold_keeps_ref (R677-2-F2) | det afterhold | `[det afterhold] after a hold, samples either side of +/-Ps/2 read the half-period phase` |
| offset_rounding_bypassed (anchor follows the 33-bit load) | ofs | unchanged |

`ofs` cases: A, B (CRF row 4,294,958,333, the largest that rounds under 2^32), C (run time: CRF 4,294,958,334, the
first past it; talker 3 0xFFFFFFFF), D (CRF 0xFFFFFFFF), E (factory rows at the boundary, graded in reset), F (run
time: CRF back to 2 ms, the carry clears). The old grader's 32-bit cast and its skip of CRF rows past 2^31 are gone;
the AAF phase against the CRF is graded on 64 bits for AAF rows under 2^31. 46 checks.

`det afterhold`: settle on +/-100 ns, an mr hold mid-window, then +/-10,416 ns: theta -31,250, committed correction
-32,768/256 (the slew limit), settled low. With `hold_keeps_ref`: theta 0.

milan_dp `[NOTIFY]` (N6), `sim_nxn.cpp:1445`: four steps from A counted at B, with SUCCESS, none to A, the push's
latency = the value set (5.4.5.1) and GET's applied value per step. Planted control: `gsi_mutants.py` mutant 9
("uc" kind, `UC_SINFO_STORED` -> `UC_SINFO_APPLIED`), the clean build run with the mutated ROM.

### Resources and route (round 3)

The carry moves the CRF offset by one bit, so route-1x1 was re-run at `81f09d06`, and again at `62ee1a8c` after D7's
rewrite, each on a clean clone under the round-1 recipe (`receipts/round3/route_81f09d06/`,
`receipts/round3/route_62ee1a8c/`, `scripts/round3/route.sh`, Vivado under the exclusive lock only). The two routes
give the same figures and the same per-block utilization:

| Figure | Record | Round 2 `f1643214` | Round 3 `81f09d06` = `62ee1a8c` | Delta to record | Tolerance |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,709 | 49,733 | +120 | +500 |
| FF | 52,353 | 52,760 | 52,765 | +412 | +600 |
| SLICE | 15,725 | 15,797 | 15,804 | +79 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 13 | 13 | -1 | +0 (re-baseline recommended) |
| WNS / WHS | +0.215 / +0.036 | +0.305 / +0.036 | +0.282 / +0.016 | | floor +0.030 / 0 |

Route complete, gate exit 0 (`RESULT: PASS`), 42 and 39 minutes. Worst setup path: the Ethernet MAC's TX CRC counter
into `KL_gptp_gmii_launch`, outside the lane. The STOP-condition-1 measure (the carry's own cost)
against the round-2 route, per block (`hier_delta_vs_f1643214.txt`): `pres_round` +1 LUT / +3 FF, `crf_tx` +1 / +1,
the datapath's own logic (GSI word 3 from `rb_ns_o`) +8 / +1: about +10 LUT, no RAMB, against the 64-LUT bar. The
rest of the movement is placement in unchanged RTL (`csr` +59, `pp_shadow` -37, the top +17). Headroom left: LUT 380,
FF 188, **SLICE 1**.

### Gate table (round 3)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep, four shards in sequence, one runner, builds capped at two | `scripts/round3/sweep.sh` -> `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.13, tsn-gen `deca300`) | `62ee1a8c` | shard 0 14/15, 45,415 checks, `milan_dp` FAIL (7: the 3 designed pin failures in the timed leg, 4 of D8's premise in the N=4 leg; 7 legs not started); shard 1 16/16, 331,638; shard 2 17/17, 262,057 (`capture_coherence` 20,832 / dp 447 / campaign 35 of 35); shard 3 16/16, 1,540,268; 0 failures outside `milan_dp` | `receipts/round3/sweep_62ee1a8c/` |
| milan_dp, every leg | `scripts/round3/mdp_run.sh`: `make run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"`, then `make run-notify` | `32fb8fc2` | rc 0: 14 tallies, 11,629 checks, 0 failures, 2,415 s; notify leg rc 2: 441 checks, 3 failures (steps 3, 4 at the pin, by design) | `receipts/round3/milan_dp_32fb8fc2/` |
| notify leg and planted control with the gate fix (form (b), uncommitted in the submodule) | `make notify`; `python3 gsi_mutants.py 9` | `fe3ff999`, `32fb8fc2` | 441 checks, 0 failures; control caught at step 3 (3 of 441); at the pin the control reports its anchor absent | `receipts/round3/notify_sinfo/` |
| the three processor forms against the case and the never-set probe | one build, three ROMs | `fe3ff999` | pin 3 failures, (a) 2, (b) 0 (table above) | `receipts/round3/notify_sinfo/` |
| media_phase default target | `make -C tb/verilator/media_phase` | `cf85a578` (`ofs` again at `62ee1a8c`; suite in the sweep at `62ee1a8c`) | rc 0: 27 tallies, 326 checks, 553 s at three case jobs, five builds | `receipts/round3/media_phase_default_cf85a578/`, `media_phase_ofs_62ee1a8c/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=2` | `cf85a578`; the six `ofs` mutants again at `62ee1a8c` | rc 0: 19 clean, 33/33 killed, 52 checks, 1,396 s | `receipts/round3/media_phase_mutants_cf85a578/`, `media_phase_ofs_62ee1a8c/` |
| route-1x1 resource gate | `scripts/round3/route.sh` (round-1 recipe, clean clone), `pp_resource_gate.py check --endpoint route-1x1` | `81f09d06`, `62ee1a8c` | exit 0 both: LUT +120, FF +412, SLICE +79, RAMB +0, DSP -1, WNS +0.282, WHS +0.016 | `receipts/round3/route_81f09d06/`, `route_62ee1a8c/` |
| Yosys, the changed tops | `syn/yosys/run.sh --top KL_crf_tx --top KL_mtt_round --top KL_aaf_capture_i2s --top milan_datapath` (sv2v v0.0.12, CI's pin) | `32fb8fc2` | rc 0, 4/4 PASS (`KL_mtt_round` 1,215 cells; `milan_datapath` 1,712,703), tied-input and tap-purity PASS. At `aea19ce7`: `KL_mtt_round` 0 cells (D7) | `receipts/round3/yosys_changed_tops_32fb8fc2/`, `yosys_small_tops*/` |
| lint | `python3 scripts/lint_rtl.py --check` | `32fb8fc2` | PASS 89 <= 89 | `receipts/round3/lint_32fb8fc2/` |
| docs gates (49) | `scripts/docs_gates.sh` | `32fb8fc2` (and `62ee1a8c`) | 49/49 rc 0. At `d790dd44`: 47/49 (doc style, naming), fixed in `cf85a578` | `receipts/round3/docs-gates-*/` |
| builder bank | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `32fb8fc2` | rc 0, all gates pass except gate 11 not run (needs the separate Arty build tree), as round 2 | `receipts/round3/builder_bank_32fb8fc2/` |
| crf_tx | `make -C tb/verilator/crf_tx` | working tree before `81f09d06`; in the sweep at `62ee1a8c` | 129/129 | sweep receipts |
| comment audit (R678-2-R1) | `git diff e26f1816..HEAD` added source lines, review labels | `62ee1a8c` (no source comment since) | 0 matches | `receipts/round3/comment_audit.txt` |

Superseded this round: the sweep at `aea19ce7`, cancelled with TERM after D7 was found (`CANCELLED: TERM`).

### Environment notes (round 3)

- The round-2 `bin/python3` symlink pointed at a deleted interpreter; round 3 uses a wrapper that execs the round-2
  CPython 3.12.13 venv (a symlink to a venv's python loses its site-packages, so the image generator found no YAML).
- sv2v: CI pins v0.0.12; the host's default is v0.0.13, so the Yosys runs put v0.0.12 first on PATH.
- The Vivado route ran inside this unit's 12 GB cap (peak about 8.8 GB); no Verilator build beside it except one
  small harness. `memory.events` shows reclaim at the cap and no OOM kill.

### Follow-up recorded (not implemented, by ruling)

An applied value that changes without a SET (a media clock rate change with the same row as set) changes what
GET_STREAM_INFO reads and what every output stamps, with no SET_STREAM_INFO behind it: IEEE 1722.1-2021 7.5.2's
change in normal operation, for which an unsolicited notification would be due. Out of #770's scope; a new Issue.

## Round 2 (session 6, 2026-10-20 21:50 to 2026-10-21 04:10) -- STOP posted on F1

**Status: STOP at `2ff30f0d` on R678-1-F1 (the decision below); every other round 2 item done and every gate
green.** Not pushed; dev `78ca9bdf` not merged. TAKEN not re-posted. STOP:
https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6306168406 (text: `public-stop.txt`).

### Round 2 commits (on `f1fda3f1`, oldest first)

| Commit | Subject |
|---|---|
| `b23e9e31e` | Aggregate the phase circularly against a tracking reference, settle only with every sample of four full windows in band, and drop a correction whose hold lands on its own snapshot edge |
| `1c58fd9d6` | Apply every stream output's presentation offset in whole media clock periods by the CRF transmitter's Equation 14 rule, and read the applied rows back through GET_STREAM_INFO |
| `920e7e93b` | Grade the detector's fold boundary, settled flag, range guard and snapshot holds alone, engagements at the fold and a local PHC step in the loop, and four AAF offsets against the CRF timing points, with a planted defect for each |
| `07f774252` | Close the I2S blend's frame on its I2S pair, the last of the frame to arrive, back-dated by the I2S front end's latency, and present each I2S pair on its own strobe instead of the next |
| `07c7eeaf4` | Grade the in-tree I2S and TDM8 blend at both interfaces' pins through the capture crossbar's frame bank, with the old closing pair and the late I2S pop planted |
| `133d1a1e0` | Convert the offset rows round and round with one divider and no per-row copy, name the rounder's ports for their unit, and hold the new harnesses to the C++ rules |
| `dd2563439` | Document the tracking fold, the every-sample settle, the snapshot hold, offsets in whole periods, the blend's I2S close and the listener decision with its measured cost, and record media_phase's fresh timing (#632, #764) |
| `61c2b468e` | Record the media_phase campaign's measured 837 s at four jobs |
| `814695e3a` | Name the factory-row loop for its row, so the fold's own default binding stays the one the builder's binding controls plant |
| `44508dd89` | Round every output's offset in one multiplier-free rounder, the CRF output stamping its applied row with its own converter no longer elaborated, and plant its raw row |
| `f16432140` | Unwrap each phase sample with one compare and one whole period on the reference's side, the same representative the difference form chose, in about half its logic |
| `2ff30f0dc` | Record the campaign's 751 s at the head and the route-1x1 headroom the listener decision is measured against |

### Outcome per item

| Item | Ruling | Status |
|---|---|---|
| R678-1-F1 | listener presents each sample at the pin at its presentation time | **STOP: decision needed** (below). Not implemented: every form of it exceeds the route-1x1 gate the same ruling holds, and it replaces the #386 render law six suites grade |
| R678-1-F2 | AAF offsets in whole periods, Eq. 14's rule; readback applied | done: `1c58fd9d`, `920e7e93`, `133d1a1e`; one multiplier-free rounder for every row with the CRF output on it (`44508dd8`) |
| R678-1-F3 | circular aggregation; settled needs every sample in band; detector and closed-loop cases | done: `b23e9e31`, `920e7e93`; cheaper identical unwrap `f1643214` |
| R678-1-F4 | a hold on the snapshot edge drops the correction | done: `b23e9e31`, `920e7e93` |
| R677-1-F1 | in-tree blend gets its constants, graded at its pins | done: `07f77425`, `07c7eeaf`; found D6 on the way |
| R677-1-F2 | PHC step hold case and mutant | done: `920e7e93` |
| R677-1-F3 | settled-flag and fold-range checks and mutants | done: `920e7e93` |
| R677-1-F4 | media_phase budget basis | done in the docs commit (fresh timing below) |
| R677-1-F5, R678-1-R1 | stale divider texts; PR body reviewer lines | done (docs commit; PR-BODY.md) |

### F1: the decision needed (published with STOP)

Measured before designing (`receipts/round2/ooc_render_setpoint/`): presenting at the timestamp holds each sample for
the offset less its arrival lead, about 1.9 ms at 2 ms, about 96 events: 128 rows per 8-channel stream where the
stage keeps 32. Vivado OOC of `KL_render_setpoint` at the 1x1 parameters: depth 5 = 456 LUT (128 LUTRAM), depth 7 =
1,006 LUT (512 LUTRAM). +550 LUT for storage alone against 469 LUT and 20 SLICE of route-1x1 headroom
(round-1 head: +31 LUT, +60 SLICE of +500/+80). Block RAM: two or three RAMB18 (the parity-split rows need a write
port each) against a RAMB tolerance of 0. The depacketizer frame FIFO is 2,048 bytes (`FIFO_DEPTH_BYTES`), about 8
PDUs of the shipping stream, under the 14 a 2 ms hold needs. Every option replaces the #386 fill law graded by
`render_setpoint`, `milan_dp` (render law, settle recentre, aclk), `follow_ring`, `milan_dp_gm_steps`,
`milan_dp_render`. One pop per stream cannot land two interfaces whose post-grid delays differ by a frame on one
presentation time without a per-interface frame delay; the Arty DAC path (`KL_i2s_playback`) has its own fill law and
elastic FIFO, fed by the raw render tap by default. Options for the decision: (a) a timestamp-snapped setpoint queue
in LUTRAM (+~550 LUT storage + logic) or BRAM (+2..3 RAMB18), (b) a presentation gate at a deepened depacketizer FIFO
(+1 RAMB36; delays the loopback ring and the DAC tap too). Either needs the route-1x1 record re-written by an accepted
growth decision, the supported offset range (queue depth), and the late/early PDU policy.

### Defects found this round

- **D6, the I2S pair one pop late (found by the blend grade with sample values at the pins).** `KL_aaf_capture_i2s`
  (and the flat golden `aaf_talker_i2s` it was split from) copied `cdc_pair_fifo`'s registered `rdata_o` on the pop
  edge, so every strobe carried the PREVIOUS pair: the I2S data lagged its strobe by a frame. With the round-1 blend
  close on the TDM pair the banked I2S pair was two periods older than the stamp (R677's probe counted strobes, not
  samples, so it saw one). The TDM front ends alias `rdata_o`; both I2S front ends now do too (`07f77425`). Affects
  the I2S-only and blend shapes (Arty, retired); the AX7101 shapes have no I2S capture.
- **The detector's arithmetic mean across the fold (R678-1-F3)**, reproduced on `f1fda3f1` by the new det cases
  (`receipts/round2/det_vs_f1fda3f1/`): balanced, 129:127, 160:96 and jittered half-period samples read theta 0 / 244 /
  7,812 / 10,678 units instead of about 31,250; meanin settled; snap on the edge committed 3000/256 for mr, the term
  disabled and not-LOCKED (broken history, PHC step and slew squash the rate commit and so passed).

### Changes (file:line at the docs commit; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:482` | `PH_UW_C` (unwrapped sample width) | 10.8 |
| `KL_mmcm_drp_servo.sv:521` | `g_refold_guard`: one re-fold brings the window phase into 16 bits | 10.8 |
| `KL_mmcm_drp_servo.sv:740-747` | tracking reference `ph_ref_r`/`ph_ref_v_r`, `ph_allin_r` | 10.8 Eq. 15 |
| `KL_mmcm_drp_servo.sv:778-806` | per-sample band, tracking unwrap, window re-fold, settled needs every sample | 10.8 Eq. 15 |
| `KL_mmcm_drp_servo.sv:856-895` | reference update per counted window, seeded by an era's first sample, cleared by a hold | 10.8 |
| `KL_mmcm_drp_servo.sv:1017` | snapshot reads `ph_hold_w` on its own edge (R678-1-F4) | 10.8 |
| `hdl/ieee1722/crf/KL_mtt_round.sv` (new) | every output row rounded up to whole periods, KL_crf_tx's Eq. 14 rule, one round-robin divider, no multiplier (pass 2's numerator is pass 1's less its remainder) | 10.7 Eq. 14, 4.3.5, 10.8 Eq. 15 |
| `hdl/ieee1722/crf/KL_crf_tx.sv` | `ROUND_MTT_P` (default 1, its converter); 0 takes the rounded row, no converter elaborated (the datapath's instance) | 10.7 Eq. 14 |
| `KL_mmcm_drp_servo.sv:787-797` (at `f1643214`) | the unwrap as one compare and one period on the reference's side (identical mapping, receipts/round2/unwrap_equivalence) | 10.8 |
| `hdl/milan/milan_datapath.sv:3439-3462` | `pres_round` over the ACMP_SRC_C rows; `aecp_pres_applied_w` | 4.3.5 |
| `milan_datapath.sv:1447`, `:5238` | talkers stamp the applied rows; GET_STREAM_INFO reads them | 4.3.5; IEEE 1722.1 GET_STREAM_INFO |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:98-113` | `close_pair()` (TDM only), `close_slot()`, `close_is_i2s()` | 4.3.5, 10.8 |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv:386`, `:643`, `:661` | `TDM_CLOSE_SLOT_P`: the frame closes on its last pair to arrive | 4.3.5 |
| `milan_datapath.sv:1246`, `:1260`, `:6106-6125` | the blend closes on its I2S pair, back-dated by the I2S front end's latency | 4.3.5, 10.8 |
| `hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv:153`, `aaf_talker_i2s.sv:178` | pair data alias the FIFO's registered read (D6) | 4.3.5 |
| `milan_datapath.sv:6307`, `sw/builder/endstation_builder.py:4748`, `sw/builder/test_builder.py:21628` | R677-1-F5 stale divider texts, as written | -- |
| `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile` | source lists: `KL_mtt_round.sv` | -- |

No top-level port, no register-map layout change (MCSRV_STAT[9]'s meaning tightened, read only). Module parameter
added: `KL_chan_map_capture.TDM_CLOSE_SLOT_P` (defaulted to the old behaviour). `close_pair()` lost its blend
argument (callers updated).

### New checks (planted mutant, failing words)

media_phase campaign, 28 mutants (17 kept; `fold_not_centred` retargeted because the window re-fold now gives the
short way, so its observable is the per-sample band):

| Mutant | Harness / case | Required failing check |
|---|---|---|
| tracking_fold_removed | det balanced | `[det balanced] the window phase reads the half-period phase` |
| window_refold_removed | det cross | `[det cross] past +Ps/2 the window phase re-folds to the short way` |
| settled_on_mean_only | det meanin | `[det meanin] settled never asserts with every sample outside the band` |
| snapshot_hold_ignored | det snap | `[det snap] mr on the closing edge` |
| settled_is_engaged (R677 P2) | det inband | `[det inband] settled first reads 1 at the close of the fourth full in-band window` |
| fold_range_guard_removed (R677 P3) | det range | `[det range] a timestamp 2^25 ns from the domain event is not sampled` |
| fold_not_centred (retargeted) | det inband | same as settled_is_engaged |
| step_hold_removed (R677 P1) | phcstep | `[phcstep] the phase term let go at the PHC step` |
| offset_rounding_bypassed | ofs | `[ofs A] every AAF output stamps whole periods from the CRF timing points` |
| blend_closed_on_tdm_pair | blend | `[blend 0] the I2S pair of every banked frame started at its pins inside +/-5 % of Ps` |
| i2s_pair_one_pop_late | blend | same |
| crf_row_raw (ofs_wrap) | ofs | `[ofs A] every CRF timing point is a frame instant plus the CRF row as read back` |

capture_coherence: three anchors moved to the renamed close-rule text (same mutants, same expected checks).
milan_dp nxn: `#632 GET_STREAM_INFO reads the offset applied, whole periods` (2,010,000 ns set, 2,020,834 read) on
an AAF row and the CRF row, then the existing #403 timestamp grade at those offsets.

### Area work this round (receipts/round2/ooc_blocks/)

Vivado OOC per block, LUT / FF / DSP:

| Block | f1fda3f1 | this round |
|---|---|---|
| `KL_mmcm_drp_servo` | 1,233 / 1,006 / 0 | 1,384 / 1,026 / 0 with the difference-form unwrap (`b23e9e31`); 1,342 / 1,026 / 0 with the sign-selected unwrap (`f1643214`, identical mapping: `receipts/round2/unwrap_equivalence/`, 558 M pairs, 0 mismatches) |
| `KL_mtt_round` (new) | -- | 122 / 155 / **1** with multiplies (`1c58fd9d`), 182 / 190 / 0 multiplier-free (`44508dd8`): pass 1's numerator is shifted adds of DEN, pass 2's is pass 1's less its remainder |
| `KL_crf_tx` | 404 / 298 / 1 (its own converter) | 246 / 169 / 0 at `ROUND_MTT_P = 0` (the datapath's instance): the CRF row comes rounded from `KL_mtt_round` |

The first rounder would have added a DSP against a DSP tolerance of 0; the routed `KL_crf_tx` held one DSP for its
own x 62,500. One multiplier-free rounder for every row and `KL_crf_tx` at `ROUND_MTT_P = 0` gives the image one DSP
fewer. Expected route movement against the round-1 head: about +130 LUT, +80 FF, -1 DSP; slices the open risk
(+60 of +80 used at round 1).

### Resources and route (round 2)

route-1x1 at `f1643214` on a clean clone under the round-1 recipe (`receipts/round2/route_f1643214/`):

| Figure | Record | Round 1 `a6ae20f9` | Round 2 `f1643214` | Delta | Tolerance |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | 49,709 | +96 | +500 |
| FF | 52,353 | 52,641 | 52,760 | +407 | +600 |
| SLICE | 15,725 | 15,785 | 15,797 | +72 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 14 | 13 | -1 | +0 (re-baseline recommended) |
| WNS / WHS | +0.215 / +0.036 | +0.276 / +0.032 | +0.305 / +0.036 | | floor +0.030 / 0 |

Route complete, gate exit 0, 40 minutes. Per block against the reference route (`hier_delta_vs_ref.txt`): servo
+382 LUT / +200 FF, `pres_round` (KL_mtt_round) +148 / +190, `crf_tx` -109 / -142, domain event +6 / +79,
crossbar -15 / +64, crf_rx +24 / +33; outside the lane the gPTP shadow -209 LUT (placement). Worst setup path: the
SoC's write-beat counter into a RAMB18 enable, outside the lane.

### Gate table (round 2)

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| full sweep, four shards, two runners on two clean clones | `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.13, tsn-gen `deca300`) | `2ff30f0d` | 64/64 suites, 2,187,770 checks, 0 failures: shard 0 15/15 53,842 (tsn_fuzz 164 + 677 pass), shard 1 16/16 331,603 (media_phase 291 checks, ~533 s), shard 2 17/17 262,057 (capture_coherence inside its 2,400 s window, campaign 35/35), shard 3 16/16 1,540,268 | `receipts/round2/sweep_2ff30f0d/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` | `f1643214` (`2ff30f0d`: a Makefile comment and a doc paragraph) | rc 0: 18 clean, 28/28 killed, 46 checks, 751 s | `receipts/round2/media_phase_mutants/` |
| media_phase suite timing (R677-1-F4) | `make` at the default CASE_JOBS | working tree before `dd256343` | rc 0, 578 s with five builds | `receipts/round2/media_phase_suite/` |
| route-1x1 resource gate | round-1 recipe on a clean clone, `pp_resource_gate.py check --endpoint route-1x1` | `f1643214` (no RTL or build input changed since) | exit 0: LUT +96, FF +407, SLICE +72, RAMB +0, DSP -1, WNS +0.305, WHS +0.036, route complete | `receipts/round2/route_f1643214/` |
| lint | `python3 scripts/lint_rtl.py --check` | `2ff30f0d` | PASS 89 <= 89 | `receipts/round2/lint/` |
| docs gates (49) | `scripts/docs_gates.sh` | `2ff30f0d` | 49/49 rc 0 | `receipts/round2/docs-gates/` |
| Yosys | `syn/yosys/run.sh` (all tops); `--top` the six changed tops | `dd256343`; `f1643214` | 60/60 PASS, tap-purity PASS; the six changed tops PASS, tied-input PASS | `receipts/round2/yosys_all_tops_dd256343/`, `yosys_changed_tops_f1643214/` |
| builder bank | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `f1643214` (it reads none of `2ff30f0d`'s changes) | rc 0, all gates pass except one not run for its recorded reason (needs a separate Arty build tree) | `receipts/round2/builder_bank_f1643214/` |
| aaf, crf_tx | `make -C tb/verilator/aaf`, `make -C tb/verilator/crf_tx` | working tree (in the sweep at `2ff30f0d`) | pass; crf_tx 129/129 | sweep receipts |
| detector vs f1fda3f1 | det cases on the round-1 servo | `f1fda3f1` servo | the cancellation and snapshot defects reproduced | `receipts/round2/det_vs_f1fda3f1/` |

### Environment notes (round 2)

- The sweep runner refuses an interpreter without `os.pidfd_open`; the standalone CPython 3.12.3 build on this host
  lacks it, so the sweep ran on CPython 3.12.13 (same CI constraint pins); the docs gates and lint ran on 3.12.3.
- Two clean clones, because concurrent sweeps in one tree share build directories (the runner refuses).
- MemoryCurrent reached 10-11 GB during the sweep, almost all page cache (anon under 1 GB, 8 GB inactive file).
- A Vivado OOC batch inherits `-generic` values between `synth_design` calls in one session; that run's third
  report was discarded (`receipts/round2/ooc_blocks/README.txt`).

### Loop design (unchanged gains; what changed)

Gains, poles and bandwidths as round 1 (phase pole 0.944, rate 0.70; ~0.018 / 0.11 Hz; clamp 256 ns per window).
The detector: each folded sample unwrapped against a tracking reference (the last counted window's re-folded phase,
or the era's first sample), summed, the window phase re-folded once. At +/-Ps/2 the estimate is the half-period
phase, so the pull is at the clamp and the fold is left within a window or two: closed-loop at +Ps/2 (2 ns inside)
and -Ps/2 with 8 ns truncation and +/-48 ns jitter, re-engaged at -0.49 Ps, in band 26.4 / 26.6 s, settled never
read outside the band.

## Round 1

**Status: REVIEW READY at `f1fda3f1` (2026-10-20, session 5).** Every gate passes at the head (gate table below):
the sweep (64 of 64 suites), the 17 phase mutants, route-1x1 within the resource gate and timing floor (at
`a6ae20f9`, RTL identical), lint, Yosys and the docs gates. route-1x1 had failed at `e96f3928` (R1); the servo
shrink passed it at `5537cc41` (R2) and again with the window cap at `a6ae20f9` (R3). The sweep found two fixture
timings that assumed the retired CRF divider (D5), fixed in `33a460db` and `f1fda3f1`. REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112 (head `f1fda3f1`).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284510903
- Addendum 1 (in/out latencies at the pins): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284578201
- Addendum 2 (one reference per media clock domain; replaces addendum 1 item 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284659263
- #764 report: https://github.com/kebag-logic/milan-fpga/issues/764#issuecomment-6283948176
- Lane: branch `632-764-media-phase` from dev `e26f1816` (checked: `git merge-base HEAD origin/dev` = e26f1816;
  origin = https://github.com/kebag-logic/milan-fpga.git). Not pushed (pushing is outside this lane).
- TAKEN (session 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284564768. Not re-posted.
- REVIEW READY (session 5, head `f1fda3f1`): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112

## Session history

| Session | What happened |
|---|---|
| 1 | TAKEN posted; stopped by the manager for addendum 1. No commit. |
| 2 | Stopped by the manager for addendum 2. No commit. |
| 3 | Four commits: `cd39fea0` servo phase loop; `b7d3ad20` domain event, phased CRF output, AAF time base; `5081c7b2` media_phase bench and two-interface pins; `dac4ce37` capture_coherence `[PIN]` leg. Cut by a host reset (memory error) at 10:00 with an uncommitted media_phase Makefile/suite-budget change. |
| 4 | Resumed 12:07. Found and fixed two defects in session 3's design (D1, D2 below) and one robustness gap (D3); committed the session-3 leftovers; wrote the docs; ran the gates. route-1x1 at `e96f3928` failed the resource gate (R1 below); began shrinking the servo, uncommitted, when the host reset at 14:01. |
| 5 | Resumed 14:10. Validated the shrink (all media_phase cases pass, OOC 1168 LUT / 982 FF), fixed six stale comments and the clamp mutant's removed anchor, added the HOLDOVER and INTERNAL let-go mutants, committed `6f4a2b46` + `5537cc41`; route-1x1 at `5537cc41` PASSED (R2). Found a window-phase wrap under a talker sending faster than it declares (D4) and capped the window (`e887d937`, `a6ae20f9`); route-1x1 passed at `a6ae20f9` (R3). One mutant survived the 16-bit phase (fixed, `e85df091`). The sweep found D5 (two `milan_dp` fixture timings, `33a460db`, `f1fda3f1`); every gate then passed at `f1fda3f1`; REVIEW READY posted. |

## Commits (base `e26f1816`)

| Commit | Subject |
|---|---|
| `cd39fea0` | Phase the media servo to the followed CRF stream: an exact fold, a type-2 term under a slew limit, and an integrator that carries its odd errors |
| `b7d3ad20` | Stamp the CRF output and the AAF talkers from the clock domain's media event, back-dated by each interface's derived latency |
| `5081c7b2` | Grade the phase loop at the silicon window and two interfaces at their pins, with a planted defect per loop term |
| `dac4ce37` | Grade the shipping talker's timestamps against its TDM pins in the coherence datapath leg |
| `9ca025c9` | Carry each frame's instant through the capture crossbar, count the marker latency to the frame's closing pair, re-fold the phase on a PHC slew, and grade three interfaces at their pins |
| `e96f3928` | Document the phase contract per source, the domain event and per-interface constants, the listener decision and the -0.46 Ps accounting (#632, #764) |
| `0ee46622` | Name the new event ports by their unit, split the phase harness's multi-declarators, and register the media_phase budget and mutation reader with the test-evidence gate |
| `f49851da` | Regenerate the module matrix and the CDC census for the domain event and the retired CRF divider crossing, and record the media_phase budget |
| `974f17df` | Follow the domain event's renamed PHC port in the phase campaign's back-dating anchor |
| `6f4a2b46` | Fold each phase sample to its own nearest period, take the window phase as its sum over the nominal PDU count on the low 32 bits of each instant, and grade the phase term's let-go at every hold |
| `5537cc41` | Document the per-sample fold, the window sum and the hold conditions with their let-go mutants (#632) |
| `e887d937` | Cap the phase window at the nominal count plus 1/32 so a talker sending faster than it declares cannot wrap the window phase, and grade the cap with a burst case |
| `a6ae20f9` | Document the phase window's sample cap and its burst case (#632) |
| `e85df091` | Give the uncentred-fold mutant the one phase bit its range needs, so it plants a fold into [0, Ps) rather than one that wraps back to the centred reading |
| `33a460db` | Size the #726 TX wrap run in TDM frames: the CRF talker now stamps every 96th domain event, and the counters fixture clocks the TDM bus with axis_clk |
| `f1fda3f1` | Wait out the CRF talker's slower cadence in the nxn legs: with no audio frame running it stamps every 96th media tick, 200,000 clocks at 100 MHz |

## R1: the resource gate at `e96f3928`, and the shrink

route-1x1 at `e96f3928` (`receipts/route_e96f3928/`): LUT 50,329 (+716 against the 49,613 record; tolerance +500),
FF 53,072 (+719; +600), SLICE 15,802 (+77; +80), DSP 14 (+0), WNS 0.048 ns (floor 0.030), WHS 0.033. Gate exit 1.
Per block against a route of the recorded baseline's RTL (another lane's route of dev `e9cbb676`, which equals the
record in every figure; `e26f1816` differs from it only in firmware tests and docs): servo +581 LUT / +381 FF, domain
event +6 / +79, CRF rx -11 / +65, CRF tx -22 / +51, capture crossbar -19 / +64; outside this lane's logic the
processor wrapper moved +384 LUT and the gPTP shadow -233 (no RTL change there: optimisation movement). The worst
setup path is in the soft CPU's DMA bridge (20 levels, 100 MHz), not in this lane's logic.

The shrink (`6f4a2b46`), each step measured with `syn/yosys/ooc.sh KL_mmcm_drp_servo` (`receipts/ooc/`):
base 865 LUT / 792 FF; `974f17df` 1,457 / 1,183; now 1,168 / 982.
- the PDU-to-PDU unwrap and its runaway re-fold removed: each sample folds to its own nearest whole period, so every
  pull is the short way by construction (the slew case's 27 us re-acquired as its 6.2 us fold, as before);
- the window mean's division removed: Theta is the window sum over the nominal 256 PDUs, a shift (a short window
  only pulls less; it reads settled only when full); the divider is now by the constant Ps alone;
- the detector takes the low 32 bits of the domain event and of the CRF timestamp (their difference is exact within
  2^31 ns; the fold range is 2^25 ns, 33.5 ms, against a 2 ms default Max Transit Time);
- the PI operand 48 -> 40 bits; `KL_crf_tx`'s registered event instant dropped (the engine takes `ev_ns_i` on the
  event's cycle);
- the hold replaces the re-fold: every hold condition lets the term go and spoils the open window. Each case now
  grades the let-go (`phase_o[20]` low within 5 to 200 ms of its event), with a mutant per hold condition.

## R2: route-1x1 at `5537cc41` passes

`receipts/route_5537cc41/`: LUT 49,643 (+30), FF 52,662 (+309), SLICE 15,782 (+57 of +80), RAMB36 74, RAMB18 25,
DSP 14, WNS +0.418 ns, WHS +0.013 ns, route complete; gate exit 0. Per block against the reference route
(`hier_delta_vs_ref.txt`): servo +274 LUT / +180 FF, domain event +6 / +79, CRF rx +8 / +33, CRF tx -17 / -14,
capture crossbar -60 / +63; outside the lane the processor wrapper -106 LUT and the gPTP shadow -238. Comparing the
two routes, the processor wrapper's movement alone swung by 490 LUTs (+384 at `e96f3928`, -106 here) with no
processor RTL change: the route's LUT figure carries a few hundred LUTs of placement-dependent movement that this
lane does not control. The worst setup path is the SoC's AXI-Lite-to-Wishbone bridge, outside the lane.

## R3: route-1x1 at `a6ae20f9` (the head) passes

`receipts/route_a6ae20f9/`: LUT 49,644 (+31 of +500), FF 52,641 (+288 of +600), SLICE 15,785 (+60 of +80), RAMB36 74
(+0), RAMB18 25 (+0), DSP 14 (+0), WNS +0.276 ns (floor +0.030; fall -0.061 is a rise), WHS +0.032 ns (floor 0),
route complete; gate exit 0. Per block against the reference route: servo +264 LUT / +180 FF, domain event +6 / +79,
CRF rx -1 / +33, CRF tx -15 / -14, capture crossbar -5 / +64; processor wrapper -44 LUT, gPTP shadow -232. The
worst setup path is the existing reset synchroniser into the servo's 200 MHz phase-shift domain (`psrst_sync_r`, one
LUT, 3.8 ns of routing, unchanged RTL): placement-dependent, above the floor. Not re-recorded (see the decision).

## D4: the window phase could wrap (found in session 5, fixed)

The window phase is the window sum over 256 in 16 bits; 268 samples near Ps/2 overflow it. `KL_crf_rx` checks
the declared interval (96) and the 2 ms timestamp spacing, but not the arrival rate, and it consumes EARLY PDUs, so
a talker sending faster than it declares puts more than 256 samples in a window while its timestamps stay within the
33.5 ms fold range (about 15 extra). With samples within 0.0015 Ps of Ps/2 that window's phase wrapped sign: one
window's pull, at the slew limit, the wrong way. Fix (`e887d937`): a window keeps at most `PH_CAP_C` = 264 samples
(256 + 1/32); an elaboration guard proves 264 x Ps/2 / 256 inside 16 bits. New `burst` case: the talker sends every
1.92 ms for 0.6 s from a servo window boundary (267 PDUs in 512 ms); the window keeps exactly 264, the phase holds.
Mutant `window_cap_removed` fails `[burst] the window the burst filled kept exactly 264 samples, the cap` (max 267).
OOC unchanged (1,168 / 982).

## Defects found in session 4 (and fixed)

- **D1, the AAF time base latched at the tick (found by the new `[PIN]` check).** `capture_coherence` dp leg,
  engagement DP-band-true+0 (one cycle before the walk's crossing): stamps exactly 20,833 ns off their frame. When a
  frame closes ON the tick's cycle with none pending, the crossbar's walk takes the closing frame (#74 item 2
  coincidence law) but `aaf_tbase_r` latched the domain event of the frame before. Fix: the frame's instant is banked
  in `KL_chan_map_capture` beside the frame and loaded into the walk with it (`tdm_close_ns_i` -> `tdm_frame_ns_r` ->
  `tdm_walk_ns_o`), fed by `KL_media_domain_event.mark_ns_o`. After the fix: max 15 ns at that engagement.
- **D2, the marker latency counted to the frame's end (found by reviewing every shipping shape).** The crossbar closes a
  frame on the last pair it KEEPS (at most four), so on the 8x8 TDM32 shape the marker is pair 3 of 16 (a quarter
  of the frame in) and on the Arty I2S blend it is TDM pair 2; session 3 derived the latency as one whole frame.
  Those shapes' events would have been 0.75 Ps and 0.25 Ps off. Fix: `close_pair()` and `pair_end_bits()` in
  `KL_media_if_latency_pkg`; the datapath derives from `CMAP_TDM_FRAME_PAIRS_C`. The 1x1 value is unchanged
  (20,964 ns). New interface C in the synthetic shape: the 8x8's own TDM32 front end on 98.304 MHz, graded at
  every slot's pin, max 30.6 ns; its planted control (C counted to the frame's end) fails.
- **D3, a PHC policy slew did not re-fold (found by review against #545).** A slew below the unwrap's runaway bound
  (87 us) accumulated in the unwrapped phase and the loop pulled it back the long way. Fix: `phc_slew_q_r` in
  `ph_hold_w`. New `slew` case (27 us at 200 ppm): re-acquired in 20.0 s from +0.30 Ps, the short way; its
  planted control fails (phase out of band, 10,325 ns). Superseded in session 5: no unwrap remains, so the slew
  now holds the term (graded by the let-go check and `slew_hold_removed`) and the short way is the fold's.

## Changes (file:line at `f1fda3f1`, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:46-92` | banner: the phase term, its per-sample fold, window sum, cap, gains, poles, slew limit, hold conditions | Milan v1.2 7.6.1; IEEE 1722-2016 10.7 Eq. 14, 10.8 Eq. 15, 4.3.5 |
| `KL_mmcm_drp_servo.sv:323-333` | parameters `FS_HZ_P`, `PH_GAIN_LSH_P`, `PH_SLEW_NS_P`, `PH_MIN_PDU_P`, `PH_SETTLE_WIN_P` | 10.8 |
| `KL_mmcm_drp_servo.sv:438` | `IF_C = 8` integrator fractional bits (#764 floor) | 7.6.1 |
| `KL_mmcm_drp_servo.sv:444-507` | Ps as 62,500/3 exactly; fold range 2^25 ns; nominal 256 PDUs per window; `PH_CAP_C` 264 with its guard; slew clamp | 10.8, Milan 7.3.2 |
| `KL_mmcm_drp_servo.sv:703` | `ph_hold_w`: outside LOCKED, term off, mr toggle, broken history, PHC step or slew | 10.8 |
| `KL_mmcm_drp_servo.sv:763-831` | `phase_det`: per-PDU exact fold in 1/3 ns (restoring divider by Ps), window sum capped at 264, Theta = sum >> 8, verdicts | 10.7, 10.8 |
| `KL_mmcm_drp_servo.sv:836` | `pi_isum_x_w`: integ + e/2 + phase term in fixed point | 7.6.1 |
| `KL_mmcm_drp_servo.sv:948` | the phase term clamped to the slew limit, one window late | 10.8 |
| `KL_mmcm_drp_servo.sv:1308-1318` | `ph_settled_o`, `phase_o`; `MCSRV_STAT[9]` | 10.8 |
| `hdl/ieee1722/crf/KL_media_domain_event.sv` (new) | the domain media event: marker back-dated, `mark_ns_o`, liveness, alt tick | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:78-118` (new) | `cyc_ns`, `half_cyc_ns`, `close_pair`, `pair_end_bits`, `mark_lat_ns`, `slot_msb_ns` | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:388-394`, `:480-483` | event grid = every 96th domain event; ts = its instant + Eq. 14 offset; /512 divider and its cdc_pulse retired | 10.7 Eq. 14, 4.3.5 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:488` | `ts_p_o`/`ts_o`: the consumed timing point | 10.8 |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv:451`, `:654`, `:1284` | the frame instant banked with the frame and loaded into the walk (D1) | 4.3.5, 10.8 |
| `hdl/milan/milan_datapath.sv:6078-6108` | domain event, closing-pair latency (D2), AAF time base from the walk (the packetizer reads its low 32 bits) | 4.3.5, 10.8 |
| `milan_datapath.sv:6150-6155`, `:6320`, `:5948` | servo phase operands (low 32 bits); CRF output events; CRF rx timing point | 10.8 |
| `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile` | source lists for the two new files | -- |
| `scripts/lint.budget` | crf 4 -> 3 (one SYNCASYNCNET fewer with `KL_crf_tx`'s cdc_pulse gone) | -- |
| `scripts/run_all_suites.sh`, `scripts/suite_shards.py`, `scripts/measure_test_evidence.py`, `scripts/measure_test_evidence_readers.py` | media_phase budget 900 s (provisional), its reader disposition | -- |
| `tb/verilator/milan_dp/stream_counters.py:180-189`, `stream_counters.hpp:300-304`, `sim_nxn.cpp:5046-5052`, `:7757-7760` | fixture waits sized for the CRF talker's domain-event cadence (D5) | -- |
| docs: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Phase alignment), `docs/design/TIME_SYNC.md`, `docs/testing/TESTING.md`, `CHANGELOG.md`, generated module matrix and CDC census, `hdl/*/README-tests.md` | contract, constants, decision, accounting, proof table | -- |

No top-level port, no register-map layout change: one reserved read-only bit, `MCSRV_STAT[9]`, now reads the phase
settled (STOP condition 1 allows new read-only status fields). Module ports changed: `KL_mmcm_drp_servo` (phase
inputs, `phase_o`, `ph_settled_o`), `KL_crf_tx` (`clk_audio_i`/`ptp_ns_i` -> `ev_p_i`/`ev_ns_i`), `KL_crf_rx`
(`ts_p_o`/`ts_o`), `KL_chan_map_capture` (`tdm_close_ns_i` defaulted, `tdm_walk_ns_o`).

## New checks (planted mutant, failing words)

media_phase campaign (`make -C tb/verilator/media_phase mutants`), 17 mutants (`tb/verilator/media_phase/phase_mutants.py`):

| Mutant | Case | Required failing check |
|---|---|---|
| phase_term_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| phase_sign_flipped | engage | `[engage] phase held inside +/-5 % of Ps to the end` |
| rate_damping_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| integrator_floored | carry | `[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)` |
| slew_clamp_removed (clamp at Ps/2) | engage | `[engage] the pull is slew-limited` |
| fold_not_centred | engage2 | `[engage2] the pull went the short way` |
| history_hold_removed | step | `[step] the phase term let go at the reference's history restart` |
| mr_hold_removed | mr | `[mr] the phase term let go at the mr toggle` |
| holdover_hold_removed (state and history terms; either alone suffices, so one alone survives, measured) | holdover | `[holdover] the phase term let go at HOLDOVER` |
| idle_hold_removed (state term and the IDLE reset) | internal | `[internal] the phase term let go at INTERNAL` |
| window_cap_removed (D4) | burst | `[burst] the window the burst filled kept exactly 264 samples, the cap` |
| slew_hold_removed | slew | `[slew] the phase term let go at the slew level` |
| domain_event_not_backdated | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| crf_output_off_grid | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| pins_b_constant_dropped | pins | `[pins B] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |
| pins_constants_swapped | pins | `[pins A] ...and inside the derivation` |
| pins_c_closed_at_frame_end (D2) | pins | `[pins C] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |

The let-go checks are new in session 5 (`sim_main.cpp` `watch_letgo`/`check_letgo`): the engaged bit `phase_o[20]`
must read low on some datapath cycle within 10 ms (step), 5 ms (mr, INTERNAL, slew) or 200 ms (HOLDOVER) of the
event. The session-4 mutants `refold_removed` and `slew_refold_removed` targeted the unwrap, which no longer exists.

capture_coherence (`mutants.py`, default target), the five #632 mutants of 25:

| Mutant | Leg | Required failing check |
|---|---|---|
| the live PHC at the walk | dp | `[PIN] every slot's MSB pin instant, less its slot offset, is its AAF timestamp less the presentation offset, inside +/-5 % of Ps` |
| the time base latched at the tick (D1) | dp-band | same |
| the marker latency's frame term dropped | dp | same |
| the marker latency's write term dropped | dp | `[PIN] ...and inside the marker latency's derivation` |
| the walk's instant latched at the snapshot (D1) | chmap | `F: tick-cycle: col 1 walk instant is frame 2's` |

Positive controls: `[PIN] control: the same stamps graded without the per-slot constant are refused`; the
clean builds of every leg pass first.

## Loop design (gains, bandwidths, why)

- Units: 1 trim unit = 1 ns per 512 ms window of rate = 1/512 ppm; the plant moves the rate one unit per unit.
- PI per window: `integ += e/2 + 3/128 x Theta_ns` (Theta: last window's phase, its sample sum over the nominal 256,
  clamped), `u = integ + e/4`.
- Linear model (desk, `receipts/loop/poles.py`, output `poles.log`, the g = 3/128 row): poles 0.944 (phase; time constant 17
  windows = 8.9 s), 0.70 (rate; 2.8 windows = 1.4 s), -0.40, 0. Phase bandwidth about 0.018 Hz, rate about 0.11 Hz:
  six times apart, so the rate loop has settled before the phase moves, and the phase term never fights it.
- Slew limit: Theta clamped at +/-5,461 ns, which makes the integrator settle at e = -256 ns per window: the phase
  moves at most 256 ns a window = 0.5 ppm. Inside the 2 ppm lock test (no LOCKED drop, no CLOCK_DOMAIN count) and
  glitch-free through the MMCM fine phase shift (no slip; TDM frames continuous).
- Pull-in from Ps/2: ~41 windows at the clamp, then the pole: 23-28 s measured.
- Fold exact: Ps = 62,500/3 ns, worked in 1/3 ns (3d mod 62,500 by a restoring divider by the constant Ps, 29
  cycles; PDUs are 2 ms apart). Each sample folds to its own nearest period; Theta = window sum >> 8 (nominal 256).

## Latency constants (per interface, derivation)

Marker latency = closing pair's last bit (2(k+1) word_bits + d - 1 bit periods) + FIFO write + 4.5 datapath cycles
(`receipts/latency/` evaluates the package): 1x1 TDM8 master 20,964 ns; 8x8 TDM32 master 5,308 ns; Arty TDM8+I2S
blend 15,756 ns; Arty I2S 21,126 ns; TDM8 slave 21,004 ns; synthetic TDM4 d=0 20,802 ns. Slot k pin offset:
(k x word_bits + d) bit periods. Listener post-grid: crossbar (streams x 4 + 2 cycles) + bank walk 9 cycles + adopt
wait phi (0.229..21.059 us, per lock) + slot offset: NOT compensated (see the open decision).

## -0.46 Ps accounting (addendum item 4)

`receipts/acct/`: base KL_crf_tx beside the TDM8 master, one audio clock and reset, three reset phases: the old CRF
divider event sits +40.4..+59.9 ns (+0.002..+0.003 Ps) after the frame sync at the pins. So the constant is the old
AAF stamp's distance from its own frame: marker latency (+0.006 Ps folded) + capture age. -0.46 Ps folds to +0.54;
less 0.006, plus 0.0025: 0.536 Ps = 11.2 us = ~559 axis cycles, unique in the recorded 256..785 band.

## Open decision (published with REVIEW READY)

The listener's post-grid pin delay cannot be "counted against the presentation time offset": the render path
(`KL_render_setpoint`) presents by fill, 8 events after accept, not at the avtp_timestamp. A timestamp-driven render
is a listener-datapath change outside the media-clock chain (STOP condition 3). Constants derived and documented.

## Stale text left outside the scope (follow-up)

`configs/endstation_ax7101_8x8.yaml:159` comment, `sw/builder/endstation_builder.py:4009-4011` comment and `:4748`
build-plan text, `sw/builder/test_builder.py:21628` comment, all "KL_crf_tx /512". The builder and configs are
outside the media-clock chain; build plans are untracked.

## Resource before/after, route timing

| Measure | Base (record, `e26f1816` inputs) | `e96f3928` | Head (`a6ae20f9` = `e85df091` RTL) |
|---|---:|---:|---:|
| route-1x1 LUT | 49,613 | 50,329 (+716, fail) | 49,644 (+31) |
| route-1x1 FF | 52,353 | 53,072 (+719, fail) | 52,641 (+288) |
| route-1x1 SLICE | 15,725 | 15,802 (+77) | 15,785 (+60) |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 |
| WNS / WHS | +0.215 / +0.036 ns | +0.048 / +0.033 ns | +0.276 / +0.032 ns |
| servo, routed hierarchy | 897 LUT / 814 FF | 1,478 / 1,195 | 1,161 / 994 |
| servo, Yosys OOC | 865 / 792 | 1,457 / 1,183 | 1,168 / 982 |

Details and per-block movements: R1, R2, R3 above.

## Gate table (head `f1fda3f1`; the RTL is identical since `a6ae20f9`, where the route ran)

| Gate | Command | Result | Receipt |
|---|---|---|---|
| route-1x1 resource gate | `syn/ooc/pp_resource_gate.py check <gateware> --endpoint route-1x1` after the recipe route | exit 0: LUT +31, FF +288, SLICE +60, DSP/BRAM +0, WNS +0.276, WHS +0.032, route complete | `receipts/route_a6ae20f9/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` at `e85df091` (no media_phase or RTL file changed since) | rc 0: 10 clean cases, 17 of 17 mutants fail their named checks (27 checks, 0 failures) | `receipts/media_phase_e85df091/mutants.log` |
| full sweep, shards 0-3 | `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.3, tsn-gen `deca300`) | shard 0 at `f1fda3f1`: 15/15, 52,903 checks, 0 failures (`milan_dp` included); its `tsn_fuzz` campaigns re-run with tsn-gen at `f1fda3f1`: 164 + 677 pass, all campaigns passed. Shard 1 at `e85df091`: 16/16, 331,441 checks, 0 failures (`media_phase` included; the diff to `f1fda3f1` is three `milan_dp` fixture files, which no shard-1 suite compiles). Shard 2 at `f1fda3f1`: 16/17 under the runner, 262,022 checks, 0 failures, and `capture_coherence` killed by the 2,400 s wall clock on two CPUs (result unknown), re-run alone at `f1fda3f1` inside the same budget: PASS in 21 min (run 20,832 checks, dp 447, campaign 35 of 35 with all 25 mutants caught; the runner's `suite_tally.py --verdict` rc 0). Shard 3 at `f1fda3f1`: 16/16, 1,540,268 checks, 0 failures | `receipts/sweep_f1fda3f1/` (with `shard2_capture_coherence_uncontended/`), `receipts/sweep_e85df091/shard1/` |
| lint | `python3 scripts/lint_rtl.py --check` | rc 0: 89 <= ratchet 89 | `receipts/lint_f1fda3f1.log` |
| Yosys synthesis gate | `syn/yosys/run.sh` (serial, every top) at `e85df091` (RTL identical) | rc 0: 59 of 59 tops PASS; tap-purity PASS | `receipts/yosys_e85df091/` |
| docs gates (49, the docs workflow's) | `scripts/docs_gates.sh` in the output dir | all 49 rc 0 at `f1fda3f1` | `receipts/docs-gates/` |
| servo OOC (Yosys) | `syn/yosys/ooc.sh KL_mmcm_drp_servo` | 1,168 LUT / 982 FF / 3 DSP (Vivado maps none) | `receipts/ooc/` |

Earlier, superseded: route-1x1 at `e96f3928` exit 1 (R1); at `5537cc41` exit 0 (R2); the mutant campaign at
`a6ae20f9` had one survivor, `fold_not_centred`, fixed in `e85df091` (`receipts/media_phase_a6ae20f9/`).

## Sweep launch note (session 5)

The first launch at 16:36 named shards `1 2 3 4` (they are 0-indexed, 0..3) and pinned them to CPUs 0-5 (session
4's script; this session is booked on 112-127). It was cancelled with TERM after 5 minutes (`CANCELLED: TERM`),
`sweep.sh` now derives its CPUs from the session's affinity, and the sweep was re-run as shards 0..3.

## D5: milan_dp counters-8 failed in the sweep (session 5, fixed in the fixture)

Sweep shard 0 at `e85df091`: `milan_dp` FAIL, `[726 TX] restart/wrap emitted enough got=0x0 exp=0x1` (both
phases) in `stream_counters.py --shape 8`; reproduced (`TX_RUN,0,8,0,2,2`: the CRF talker emitted 2 PDUs; base
`e26f1816` emits 8, AAF 64 in both). Cause: a fixture artifact the lane exposes. The nxn fixture toggles
`clk_audio_i` and `clk_tdm_i` 1:1 with `axis_clk`; the base CRF talker divided `clk_audio_i` (/512 /96: a PDU every
49,152 cycles on both shapes), the lane's counts 96 domain events, one per TDM frame: 2 x 8 x 32 = 512 cycles on
TDM8 (49,152 per PDU, as before) but 2 x 32 x 32 = 2,048 on the 8x8's TDM32 (196,608 per PDU). In hardware
`clk_tdm_i` is 98.304 MHz on that shape, so both are 48 kHz. make stopped there, so the cases after `counters-8`
(counters-*-frames, base, notify, crflic, dynmap, nxn*, nolpf, prune, ax1x1, aclk, render-mutants) never ran:
Fix (`33a460db`, test only): `stream_counters.py` passes the bus's slot count (`-DTDM_SLOTS_TB`, the same value as
`AUDIO_IF_SLOTS_P`) and `stream_counters.hpp` runs the TX wrap leg `400000 x TDM_SLOTS_TB / 8` cycles, so every
talker still crosses the six-PDU wrap seed: shape 8 now emits 9 and 8 CRF PDUs (base 8 and 8), shape 1 is
unchanged (same cycle count). The checks are untouched (`>6` emitted, counter follows the wire exactly). Then the
cases after `counters-8` were run at `33a460db` with `make -k` (`receipts/milan_dp_d5/`): all pass except `nxn4c`,
the Arty shape (TDM8 master with the I2S pair blended), three checks: `[CTRS-OUT] real q3/q4 stimuli reach every
AAF and CRF index`, `[CTRS-OUT] every real FRAMES_TX source raises dirty` (0xf of 0x1f), `class A off: a CRF PDU
still reaches the MAC`. Same cause: the nxn fixture leaves `clk_tdm_i` at 0 outside the counters build (the
fixture's own note: only `ax1x1` clocks the TDM master), so on nxn4c no audio frame runs, the domain event falls back
to the 48 kHz media tick (the designed liveness fallback) and a CRF PDU comes every 96 x 2083.3 = 200,000 clocks at
100 MHz, while the waits were sized for the old 49,152 (`RealPduWait` 52,000, `CRF_BUDGET` 160,000). The I2S-only legs
(nxn, nxndv, nxn8) keep 49,152 (I2S frame = clk_audio/512). Fix (`f1fda3f1`, test only): `CRF_PDU_MAX_CLK` = 200,000,
`RealPduWait` = it + 5,000, `CRF_BUDGET` = 2 x it + 10,000; nxn4c then passes with 0 failures. No other suite
compiles `sim_nxn.cpp` or the counters files (checked), so shard 1's pass at `e85df091` stands for the head.

## tsn-gen note (session 5)

The final shard 0 (`f1fda3f1`) passed 15 of 15 but `tsn_fuzz` declared its two field campaigns SKIPPED: the
tsn-gen checkout the sweep pointed at (another lane's temporary directory) was deleted between 16:38 and 18:07.
tsn-gen was rebuilt in this lane's scratch at CI's `TSN_GEN_REV` `deca300` (`packet_gen`, Release, as the rtl
workflow builds it) and `tsn_fuzz` re-run alone at `f1fda3f1` with it. At `e85df091` the campaigns had run (shard 0
of the superseded sweep).

## capture_coherence wall clock (session 5)

Shard 2 at `f1fda3f1` ran on two CPUs (its campaign sizes itself by affinity, and two keeps it at two builds):
`capture_coherence` hit the runner's 2,400 s wall clock with 24 of 25 mutants caught and the last in flight
(`TIMEOUT ... result UNKNOWN, not a failure`). Per the runner's contract it was re-run uncontended, alone, with the
campaign pinned to two units (`python3 mutants.py --jobs 2`, the same two builds at once) on more CPUs.

## Decision for the merge: the resource re-baseline

`docs/design/AREA_BUDGET.md` asks a merge that moves the shipping image to re-record its endpoints on the merge
result (`record --write`) with the budget and #234 findings text. That is outside the media-clock chain (STOP
condition 3), so it is not in this lane; the head's route passes the gate against the existing record. The
standalone endpoints' source list includes this lane's files (the OOC script keeps the integrated read set), so
their digests would change too; their figures should not, since the processor RTL is unchanged.

## Receipts

`receipts/INDEX.md` (generated from the files present).
