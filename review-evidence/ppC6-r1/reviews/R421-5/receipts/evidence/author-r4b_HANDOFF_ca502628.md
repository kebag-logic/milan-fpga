# [A492] Lane C6 round 4b (merge only) handoff: notifications and Identify

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c6-notifications`
(PR #139). Round-4b start `651839e1ce9d3a36adfbfae0297dd091a02a2def` (round 4, unpushed; origin
URL and HEAD confirmed). Assignment: #80 comment 5944153047 (Round 4b, merge only).
Roles: executor [A492], manager [A10], reviewers [R420] (internal), [R421] (external).

## Status

Done; REVIEW READY: see the last line of this file. TAKEN posted on #80 (comment 5944159066).
Head `95a78c099ee5aa914521975355adc1dfef99d01c` (tree `d0be0f91665f4e6b8e16bfa3aa8f53bbeaff518f`),
one merge commit on `651839e1`, parents `651839e1` and `03c842a7`; no rebase, no other commit.

| Item | State |
|---|---|
| 1. Merge main `03c842a7` (`--no-ff`), keeping both sides; five builds; ROMs regenerated, overlaps checked | committed `95a78c09` |
| 2. Re-measure at the merge: every suite, every campaign, both reviewers' round-3 probes | done, all rc 0 (below): every arm kept, every count equal to its README record, every probe equal to the reviewer's own |
| 3. Parent consumer gates at milan-fpga dev `cdf49d1a` with the combined C4 + C6 patch | done, 16 of 16 rc 0 (below) |

No STOP condition was met: no port, parameter or parent-visible change by this round (list below).

## Merge resolution

`git fetch origin main` gave `03c842a780064048b0a1a3de29214174a1c13934` (PR #140, lane C5a, AECP
deadlines and hazard classes; it had itself merged `16ea10ac`, so the merge base with the lane is
`16ea10ac`). `git merge --no-ff --no-commit 03c842a7`, resolved, then the merge commit `95a78c09`.
`git merge-tree --write-tree 03c842a7 95a78c09` gives `d0be0f91`, the head's own tree.

Main touched 65 files. The six the assignment named conflicted; the rest merged textually
(docs 00, 03, 06, 08, integrator, operator; `KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`,
`gen_ucode.py`, `protocol_processor_top.sv`; `tb/ucpu/README.md`; `.gitattributes`,
`.github/workflows/hdl.yml`; the 42 new patches in `tb/pp_top/mutations/` and `aecp_mutants.py`). Each conflict, both sides kept:

| File | Conflict | Resolution |
|---|---|---|
| `tb/ucpu/sim_main.cpp` (`:553-555`, `:1722-1724`) | both sides appended checks: main's P19/P20 (`the_deadline_preempt_*`), the lane's N6/N7 | main's two first, then the lane's one (round 4's order rule) |
| `tb/pp_top/Makefile` | header; `run` (main's `$(MAKE) budget` and tally of 4 vs the lane's identify build and tally of 4); `clean`; `.PHONY` | five builds in `run`: default, fixture, identify (third), line (fourth), timebase (fifth, `$(MAKE) budget`); the awk tally requires 5 (`:149`); `clean` removes `obj_dir obj_vid obj_idn obj_line obj_tim`; `.PHONY` the union; header "Five builds" (`:4-14`); the budget comment "the fifth ... beside the other four" (`:152-154`) |
| `tb/pp_top/sim_main.cpp` | file header; main's sections DL, HZ, TB code vs the lane's `#include "notify_phases.hpp"`; `one_section`; the section calls; the tally comment | header says five builds (`:20-26`); main's DL/HZ/TB code, then the include (`:13562`); union of the flags (`dl_only`, `hz_only`, `ident_only`, `notify_only`); calls: main's AX, DL, HZ, then the lane's ID0, NP, ST, RN; "five builds" (`:13626-13629`); `PP_TOP_TIM_REAL` arm says fifth (`:13586`) |
| `tb/pp_top/pp_top_wrap.sv` | banner; port list (lane's three `dbg_ident_gap_*` vs main's DL/HZ taps); `dbg_*` assigns | both; the banner names the three re-built parameters and adds "The fifth build defines PP_TOP_TIM_REAL" (`:29-38`) |
| `tb/pp_top/README.md` | the `make` paragraph; section DV's build sentence and table row | "five times (sections DV, ID, AX and TB)" (`:20-22`); "the third build is section ID's identify build, the fourth section AX's line build, and the fifth section TB's timebase" (`:1417-1418`); default row lists DV, AX and DL and the lane's ID0, NP, ST, RN |
| `docs/architecture/09_verification.md` | both sides added a "### 8.3" | main's "8.3 The AECP deadline and the hazard classes" keeps its number (six links anchor `#83-the-aecp-deadline...`: 00, 03 twice, 06, 08 and 09 itself); the lane's notifications section follows as **8.4** (nothing links its anchor) |

Ordinals beyond the conflict hunks, so every place says the same five builds:
`tb/pp_top/sim_main.cpp:12376` (TB banner "fifth"), `tb/pp_top/pp_top_wrap.sv:483` ("the
Makefile's fifth"), `tb/pp_top/README.md:706` (section TB "fifth build"), `:729` ("`make` runs
all five"; main's text said "all three", already stale on main), `:1736` (the lane's build table
gains the `obj_tim` row), `docs/architecture/08_timing.md:167` and `09_verification.md:258`
("fifth build"), `tb/pp_top/aecp_mutants.py:57` (comment "the fifth build"). The lane's "third
build" for section ID stands everywhere (docs 00, 06, 09; README; `notify_phases.hpp`;
`notify_mutants.py`; Makefile `identify-build`). Every `tb/pp_top` binary still prints the same
build-line shape, so `notify_mutants.py`'s `TALLY` pattern needs no change.

**ROM words, beyond the text.** Regenerated from each side's generator: main `03c842a7` 87
programs, lane `651839e1` 88, merge 89 (2048 words each; `place()` asserts on any overlap and
passed). C5a adds one program, `E_DLKILL` at words 6..7 (falls into `E_FAILSAFE` at 8), and
changes no other word. The merged ROM equals main's except words 464..469 and 480..500 (the lane's
`E_IDNOTIF` and `E_SINFOUNS`, equal to the lane's word for word), and the lane's except words 6..7
(main's `E_DLKILL`). So C5a's microcode does not use 464 or 480, and nothing moved
(`receipts/ucode-merge-compare.txt`). `check_upc_map.py`: PASS (61 engine constants, 89 entry
points). Graded byte-exact at 464/480 as before: `tb/ucpu` N6/N7, `tb/pp_top` ID1 and NP3.

**RTL.** The resolution edits no RTL: `git diff 651839e1 95a78c09 -- hdl` has the same patch-id as
main's own `git diff 16ea10ac 03c842a7 -- hdl` (`685619ce…`), and `git diff 03c842a7 95a78c09 --
hdl` the same as the lane's `16ea10ac..651839e1` (`28d62c91…`).

**Interactions read, no change needed.** C5a's deadline kill and µCPU preempt never touch an
unsolicited job: `dl_kill_r` and `dl_queued_o` are gated by `!uns_r` (`KL_aecp_engine.sv`, the
DEADLINE KILL block), and the job start loads `cmd_r.protocol = PP_PROTO_AEM`, `msg_type = 0`,
so C5a's `st_echo_w` (NOT_IMPLEMENTED echo for non-AEM types) is 0 for every unsolicited frame,
including `E_IDNOTIF`/`E_SINFOUNS`. C5a's classifier (`protocol_processor_top.sv` `hz_classify`)
gives a command-form IDENTIFY_NOTIFICATION (0x0026, refused BAD_ARGUMENTS by the lane) the default
RO_SNAPSHOT/NONE key, which is right for a state-free refusal.

**Anchors and patches on the merged tree (no build):** `notify_mutants.py` 40 mutants / 43
anchors, `d3_mutants.py` 83 / 92, `acmp_mutants.py` 19 / 19, each exactly once; `gsi_mutants.py`
20 at their stated counts; `name_wr_mutant.py` 1 and 1. `git apply --check` clean for every patch:
`tb/pp_top/mutations` 42 (C5a's 55 arms), `tb/pp_top/aecp_dispatch_mutations` 35,
`tb/adp_engine/mutations` 28, `tb/maap/mutations` 27, `tb/srp_top/mutations` 73.

## Round-4b items

Merge only: no new test, no new mutant, no RTL edit (the merge's `hdl/` is exactly each side's
change on the other, by patch-id). Failing arms and mutants: every campaign was re-run at the merge
(below); every lane, C5a and other control is KILLED with the failing-check count its README
records. Clauses the merged ROM touches: IEEE 1722.1-2021 §7.4.39.1 (Figure 7-61) and §7.4.15.1
(Figure 7-40) for the lane's `E_IDNOTIF`/`E_SINFOUNS`, unmoved at 464/480; C5a's `E_DLKILL` (03 §6
rule (e), into `E_FAILSAFE`, §9.3.2.6) at 6..7.

## Parent-visible list, round 4b

Read against the parent at milan-fpga dev `cdf49d1a` (processor pin there `b2db3a97`, as at
`7f0927bb`). Round 4b adds no top port, no top parameter, no register: `git diff 651839e1 95a78c09
-- hdl/top` declares no port or parameter (its one `input` line is an argument of C5a's `hz_key`
function). Nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0).
`parent-adoption-c4c6-ea3fb388.patch` is unchanged (sha256
`67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`).

| # | Change | Parent effect | Parent disposition |
|---|---|---|---|
| 1 | `tb/pp_top` builds five times (identify third, line fourth, timebase fifth) | test code in the processor's suite; `make -C tb/pp_top identify`, `--identify-only`, `--notify-only` and the build line `notify_mutants.py` reads are unchanged | none |
| 2 | the lane's 09 section renumbered §8.3 -> §8.4 | the parent cites no 09 anchor (grep of its docs: none) | none |
| 3 | main's C5a arrives with the merge: `KL_aecp_engine` `dl_kill_i`/`dl_queued_o`, `KL_aecp_ucpu` `preempt_i`/`preempt_upc_i`/`preempted_o` (internal, documented), the classifier, `E_DLKILL`, the non-AEM NOT_IMPLEMENTED echo, `aecp_mutants.py` + CI step | #140's, not this lane's. Port-contract gate: protocol-processor 1,757 ports (1,752 at round 4; these five), undocumented 111 <= 111. Evidence gate: `aecp_mutants.py` is not flagged as a DUT reader; 72 <= 77, 0 unexplained | none needed by this lane |

## Gates

Verilator 5.050 (the CI pin, `$VALIDATION_TOOLS/verilator-v5.050`) behind a scratch shim capping
`-j 0` at 8; one heavy command at a time; campaigns with `--jobs 1`; `TMPDIR` on disk. Yosys 0.66,
sv2v. Every processor command ran on a `git archive 95a78c09` export
(`$VALIDATION_STORAGE/c6r4b/head`), except `make -C tb/nvm_port figures` (a scratch shared clone at
`95a78c09`, clean after) and `make stale` (the lane tree, read-only). The lane tree's `git status`
stayed empty. Long commands ran detached (nohup) and were waited on in the foreground; each
finished rc 0, and nothing heavy of mine ran beside another. Receipts: `receipts/`.

### Processor, at the merge `95a78c09` (all rc 0)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map PASS (61 engine constants, 89 entry points); M9 selftest 9/9 and PASS (30 opcodes); 33 suites, 1,019,110 checks, 0 failing (round 4: 1,018,785; +296 pp_top, +29 ucpu). `pp_top` 9,151 (default 8,679, fixture 20, identify 178, line 218, timebase 56), `ucpu` 437, `aecp_notify` 14, `originator` 107; 13 min 25 s (`receipts/run_suites-95a78c0.log`) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK; `KL_aecp_notify`, `KL_aecp_engine`, `protocol_processor_top` 0 findings at `-GEN_IDENTIFY_NOTIF_P=1` |
| `make lint wavedrom-check links matrix modmatrix params` (export); `make stale` (lane tree) | 0, 0 | 41 mermaid + 18 wavedrom, links 1,035, 115 REQ / 17 GAP, 94 rows 0 untested, parameters 27 = 27 = 27; stale clean |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops YOSYS OK and the Xilinx memory-map check; 114 s |
| `git diff --check` `651839e1..`, `03c842a7..`, `16ea10ac..95a78c09` | 0, 0, 0 | |

**No arm lost** (`receipts/pp_top-sections-main-lane-merge.txt`; `tb/pp_top` at main `03c842a7`
(scratch export), the lane head `651839e1` (round 4's receipt) and the merge's tree `d0be0f91`):
every section line of main's and of the lane head's is in the merge's, unchanged; the merge has none
of its own.

| Build | main `03c842a7` | lane `651839e1` | merge `95a78c09` |
|---|---:|---:|---:|
| default | 8,607 | 8,439 | 8,679 = 8,607 + ID0 3 + NP 47 + ST 18 + RN 4 |
| fixture | 20 | 20 | 20 |
| identify (ID) | - | 178 | 178 |
| line (AX) | 218 | 218 | 218 |
| timebase (TB) | 56 | - | 56 |
| total | 8,901 | 8,855 | 9,151 |

`tb/ucpu`: `16ea10ac` 398, main 427 (+29, P19/P20), lane 408 (+10, N6/N7), merge 437.

### Mutation campaigns at `95a78c09` (all rc 0, one run each, `--jobs 1`)

| Campaign | Result |
|---|---|
| `notify_mutants.py` | five goldens PASS; **40 of 40 KILLED**; every failing-check count equals the README record mutant by mutant (one message differs only in a measured value inside the same check: `counter_limit_500ms` ST3b worst 434,030 -> 433,753 clocks) (`receipts/notify-mutants-95a78c0.json`); 14.8 min |
| `aecp_mutants.py` (C5a) | 5 controls PASS (pp_top budget, d3, deadline, hazards; ucpu run); **55 of 55 KILLED**; every failure count equals the README record arm by arm; 14.3 min |
| `aecp_dispatch_mutants.py` | controls `aecp-dispatch`, `aecp-line`, `line-guards` PASS; **35 of 35 KILLED**; counts equal round 4's and the record; 8.6 min |
| `acmp_mutants.py` | 3 goldens PASS; 19 of 19 KILLED; the 14 recorded pp_top counts unchanged; 5.8 min |
| `d3_mutants.py` (whole set) | 3 goldens PASS; **83 of 83 KILLED**; all 71 counts of the README table equal (including C5a's 17 and 6); 89.6 min |
| `make -C tb/adp_engine mutants` | 2 controls PASS; 30 of 30 KILLED; verdict lines identical to round 4; 6.6 min |
| `make -C tb/maap mutants` | 3 controls PASS; 29 of 29 KILLED; identical to round 4; 4.1 min |
| `make -C tb/srp_top mutants` | 11 controls PASS; 78 of 78 KILLED; assertion coverage 65/65; identical to round 4; 32 min |
| `gsi_mutants.py` | 20 of 20 detected; golden and restored PASS; all 22 records identical to round 4; 14.5 min |
| `tb/acmp_talker/retry_mutants.py` | 62 KILLED; 7 equivalence and 1 performance controls retained; identical to round 4; 6.9 min |
| `tb/srp_admission/mutants.py` | 3 controls PASS; 3 defects x 3 suites PASS (12/12); identical; 12.9 min |
| `tb/pp_top/name_wr_mutant.py` | decode killed; golden and restored PASS |
| `make -C tb/nvm_port figures` (clone) | every figure agrees; 2 waivers with reasons; output identical to round 4; 4.8 min |

### Both reviewers' round-3 probes, re-run unchanged at `95a78c09`

Scripts read from the review packets, run on copies of the merge export; each result equals the
reviewer's own receipt at `9624ef4` once the build line's `, DESC_LINE_BYTES_P 576` is removed
(`receipts/reviewer-probes/`).

- R420-3 `run_probes.sh` (RP3a-RP3j): 600 checks, 0 failures; log identical.
- R420-3 `boundary_control.sh` (S1): section ID 178/0 under the control; the probes fail RP3j
  w=1 k=-2 only (597 checks, 1 failure); log identical.
- R420-3 `r420_2_probes_unchanged.py`: the six records equal the reviewer's JSON (RP1 15,301; RP2
  3 frames; RS1/RS2 smallest gap 15,232; `hold_ignores_gap` 4 failures ID3f, ID8q, ID8r, ID7r;
  `burst_deadline_one_tick_short` passes ID; `wait_ignores_gap` x2 REFUSED).
- R421-3 `r421_arms.py`: 188 checks, 0 failures; log identical.
- R421-3 random-press probe (`r421_3_random.py`, `run_random.sh`, 16 campaigns x 200 steps, run
  from the bench directory): all rc 0; all 16 logs identical.
- R421-3 `r421_3_probes.py` (latch mutants; `--jobs 2`, `VJOBS=4`): the same 9 records as the
  reviewer's, as a set (`p_wait_latch_always` SURVIVES, equivalent; `c_press_not_latched` KILLED
  by section ID only).
- R421-3 `r421_3_ft_sweep.sh`: nine phases, both lower bounds hold; output identical.

### Parent consumer set at milan-fpga dev `cdf49d1a`

Scratch copy `$VALIDATION_STORAGE/c6r4b-parent/src`; the trusted checkout was not touched (HEAD
`cdf49d1a`, status empty before and after). Commits:
1. `7c4e7fc`: `git archive cdf49d1a` of the trusted checkout; `external` (`efeb541`),
   `gptp-processor` (`5dce647`) and `third_party/verilog-axis` (`48ff7a7`) cloned at their recorded
   pins from round 4's scratch clones (origin URLs reset to the `.gitmodules` URLs);
   `protocol-processor` a shared clone of this lane at `95a78c09`. `git submodule init` registers
   them, with no fetch. Its 984-entry index equals the trusted tree's except the processor gitlink
   (`b2db3a97` there, `95a78c09` here).
2. `a00664b`: `git apply parent-adoption-c4c6-ea3fb388.patch` (unchanged; `git apply --check`
   clean). The scratch tree was clean after every gate.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | multi-declarator 0 <= 0, long function 0 <= 0, build without warnings 0 <= 0 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | long function 9 <= 9, too many parameters 7 <= 7, global statement 0 <= 0, over-long line 0 <= 0 |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files, 4 of 4 consumer lists; protocol-processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | 3,798 first-party ports (protocol-processor 1,757: +5, C5a's engine/µCPU ports); undocumented protocol-processor 111 <= 111 |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | PASS: 96 candidates, all recorded |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 72 <= 77 without a mutation arm, 10 <= 10, 0 <= 0 unexplained DUT-source readers, 3 <= 3; the 30 readers listed equal round 4's |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings across 185 md + 956 scrubbed files; scrub self-test 23/23; routing 4/4 |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet (hdl/ 0, pinned processors 4), the same four as round 4 (one line number moved, 915 -> 922); 2.5 min |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the calibration report needs a local mf48 build tree, as in rounds 1-4); 18 min |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 <= 90 (17 waived, 0 justified lint_off) |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures; RESULT: PASS; 3.8 min |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint passes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 RESULT: PASS, 0 FAIL (182 + 182; milan_datapath 235, 235, 232; media_aclk 191); the 6 + 6 mutant arms pass; 26 min |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65 and 152 checks, 0 failures; 5 of 5 leg-defect arms caught; 6 min |

Logs over 200 KB, not copied:

| Log | Bytes | sha256 |
|---|---:|---|
| parent `pp_shadow` (gate 12) | 311,431 | `66f5b0b9a92fff33db8d2bf156319b878196fe51f95d6fb34d65fbc9128d8129` |
| parent `milan_dp` (gate 15) | 2,005,807 | `ca80c942c39884055ee1712d138e0404ba55c13dc878d813ae89740c1b441c7b` |

Receipts for the other gates: `receipts/parent-gates/` (with `gates.status` and the index diff).

## PR-BODY.md

`PR-BODY.md` in this directory keeps the `[A463]` first line and the four `Closes` lines, gains a
one-line pointer to rounds 4 and 4b under the round summaries, and a "Round 4b" section (the merge
with clause references, the parent-visible list, validation, what remains). To stay under GitHub's
65,536-character body limit, the older rounds' validation tables became paragraphs carrying the
same figures (round 1: processor and parent tables; round 2: processor, campaign and parent
tables; round 3: the same; round 4: processor, campaign, probe and parent tables); the rounds'
design text, findings, cost tables and parent-visible lists are unchanged. The full tables for
round 4b are in the Round 4b section. Length: see the last line of this file.

## What remains

- Hosted CI on the PR, and the one delta review covering rounds 4 and 4b.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged) when it moves its processor
  pin past this head.
- Retained, unchanged: R420-1 S1 and R420-1 S4 (`tb/pp_top/README.md`). Round 3's SUGGESTIONs
  R420-3 S1 and R421-3 S1 are not taken in this merge-only round; both reviewers' probes still
  show the behaviour they cover.
- The lane tree carries ignored build products from earlier rounds (`tb/*/obj_dir`); untouched,
  untracked and not part of any commit.
- No hardware was used. Simulation only; the parent keeps the parameter at 0.

## Scratch (for a resume)

`$VALIDATION_STORAGE/c6r4b`: `bin/verilator` (pinned 5.050, `-j 0` capped at 8), `head/` (export of
95a78c09), `side-03c842a7/` (main export), `campaigns.sh` (chain; status in
`receipts/campaigns.status`), `receipts/`, `parent-gates/`. Parent scratch:
`$VALIDATION_STORAGE/c6r4b-parent/src` (commits `7c4e7fc` archive + submodules, `a00664b` patch).

PR-BODY.md: 64,316 characters (64,395 bytes), 1,220 under the 65,536 limit.

REVIEW READY posted once on #80 (comment 5947318179) at `95a78c099ee5aa914521975355adc1dfef99d01c`,
after this file and PR-BODY.md were final. Nothing pushed (the branch on origin is still `9624ef4c`).
