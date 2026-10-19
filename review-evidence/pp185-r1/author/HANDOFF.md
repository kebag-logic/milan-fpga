# [A647] #185 + #186 handoff

Lane: processor branch `185-186-control-unlock`, from main `08ae0013`
(08ae00130f096f241463172c4781885934400ee4). Assignment: processor issue #185, comment
6249574548 (A10): one lane, two commits; round 1b (manager correction on #186, comment
6253571045) adds a third.

Head: `f42c886c9abf311af64152eda669cbb040460bd1` (round 1c). Round 1 ended at `c8261711`,
round 1b at `fcb6b513`.

| Commit | Subject |
|---|---|
| `198f1b1` | READ_DESCRIPTOR CONTROL: overlay the IDENTIFY current value from the dynamic store (#185) |
| `c826171` | LOCK_ENTITY: the notification a LOCK or UNLOCK causes echoes its flags; the timeout keeps 0 (#186) |
| `fcb6b51` | LOCK_ENTITY: the automatic unlock's notification carries UNLOCK, as the command-driven one does (#186) (round 1b) |
| `a2cf652` | Merge processor main 246cbc22 (#181 notify-queue cut, #184 MSRP Domain) into 185-186-control-unlock (round 1c) |
| `f42c886` | tb/aecp_notify README: the two occupancy controls that also fail section LF after the merge (round 1c) |

`c826171`'s subject records the round-1 instruction; `fcb6b51` reverses its timeout
half, as the correction asks.

Nothing was pushed. No PR was opened.

## Round 1c

Status: done. Head is `f42c886` (merge `a2cf652` and one README-record commit) on main
`246cbc22`. Every processor gate and all 13 campaigns are rc 0 at the merged base and
at the head. All 17 parent consumer gates are rc 0 at base and head on a committed local
scratch parent. Every record difference is listed below. REVIEW READY is posted on #185
with the head (see Posting).

Processor main had moved from `08ae0013` to `246cbc22`
(246cbc22df280db8fcc09708882bb40b2e964c0e: #181 notify-queue cut, PR #187; #184 MSRP
Domain, PR #191). `git merge origin/main` conflicted in the five files the round names.
The round-1b head `fcb6b513` was merged with one merge commit (no rebase, no amend):

| Commit | Subject |
|---|---|
| `a2cf652` | Merge processor main 246cbc22 (#181 notify-queue cut, #184 MSRP Domain) into 185-186-control-unlock |

Head: `a2cf652eb3de82a8a186d02e150c093d99c0fbbc` (parents `fcb6b513`, `246cbc22`).
Nothing was pushed, and TAKEN was not posted again.

### Round 1c conflict resolutions (file:line at a2cf652)

Both sides keep their behaviour:

- `hdl/aecp/KL_aecp_notify.sv:842-846`: the emission pick's lock arm keeps the lane's
  `pick_arg1_w = lockf_r[31:16]` / `pick_arg0_w = lockf_r[15:0]`. Its next arm reads
  main's registered occupancy, `else if (cmdq_nempty_r)`, instead of the lane's base
  `cmdq_count_r != 5'd0`. This was the only RTL conflict. Main's other occupancy
  writes merged cleanly and are unchanged: the declaration `:441`, `amap_busy_o`
  `:1179`, reset `:1210`, push `:1314`, claim `:1532`. So are the lane's flags latch:
  `:422-423`, reset `:1233`, the two timeouts latching `LOCKF_UNLOCK_C` `:1400,1405`,
  LOCK/UNLOCK latching `rgy_flags_i` `:1450,1466`.
- `tb/aecp_notify/sim_main.cpp:370-372`: the default run calls the lane's `lock_flags()`
  (section LF), then main's `command_queue()` (CQ), then main's
  `occupancy_held(...)` (OC1) last. LF therefore also runs under the OC1 monitor, which
  samples every clock edge.
- `tb/aecp_notify/README.md:12-17` (the section list names LF and CQ, then OC), `:27`
  (the default build runs LF 6, CQ 8 and OC1), `:38` (86 checks: 57 in the first run, 5
  in FT, 20 in PT/CK/PD/CA, 4 in SC; measured), `:359` section LF and `:389` sections
  CQ and OC, both kept in full.
- `tb/pp_top/notify_mutants.py:30-34` (docstring: #181's occupancy flop, then #186's
  flags), `:637` `LOCK_FLAGS` and `:728` `OCCUPANCY` both kept,
  `:770` `MUTANTS = ... + OCCUPANCY + LOCK_FLAGS`.
- `docs/architecture/09_verification.md:309` "ten of the notification block's" (base
  seven, plus the lane's LF and main's CQ and OC), `:330-332` the LF, CQ and OC rows.

Checks on the merge, before any gate:
- Every main-only file is identical to main. `git diff 246cbc22 a2cf652` is empty for
  `hdl/packet_engine` (the router scan), `hdl/srp`, `syn/ooc`, `tb/srp_*`,
  `tb/aecp_notify/{occupancy.vlt,Makefile,port_tuple.hpp}`.
- Every lane-only file is identical to the lane head. `git diff fcb6b513 a2cf652` is
  empty for the engine, the microcode generator and table, `hdl/top`, the pp_top,
  ucpu and aecp_cmds benches.
- `git diff --stat 246cbc22 a2cf652` has the same 28 files and per-file counts as
  `git diff --stat 08ae0013 fcb6b513`, except `tb/aecp_notify/README.md` (+34 → +40,
  the count lines).
- Every exact-edit anchor of the 16 campaign drivers and every mutation patch applies
  exactly once at `a2cf652` (622 edits, 0 failures).
- No generated record needed re-recording. Main changes no file a lane generator reads
  (the engine, `gen_ucode.py`, `aecp_commands.json`), and `make check` and
  `gen_matrix.py --check` pass on the merge.

### Round 1c: the merged notify campaign and the README record

The notify campaign at the merge (`a2cf652`) gives 125 of 125 KILLED, goldens PASS.
Base `246cbc22` gives 109 of 109. Every mutant present at both fails the same checks,
except two of #181's controls. They now also fail LF checks, because LF's SET_NAME
round goes through the command queue whose occupancy they break:

| Control | Base 246cbc22 | Head a2cf652 |
|---|---|---|
| `occupancy_push_unseen` | 7: DR2, DR2b, CQ1, CQ1b, CQ2, CQ2b, OC1 | 9: DR2, DR2b, **LF2, LF3**, CQ1, CQ1b, CQ2, CQ2b, OC1 |
| `occupancy_reset_set` | 14: TS1 ... DR3, CQ1 ... OC1 | 17: the same plus **LF1, LF2, LF3** |

Their named checks (OC1, CQ...) are among those failures, so both are still KILLED. The
16 lock controls fail exactly the checks they failed at round-1b head `fcb6b513`
(129 of the 129 mutants common to both runs are identical). The two
`tb/aecp_notify/README.md` mutation rows are corrected, with one sentence on why
(`tb/aecp_notify/README.md:441,445,453-454`), in a README-only commit:

| Commit | Subject |
|---|---|
| `f42c886` | tb/aecp_notify README: the two occupancy controls that also fail section LF after the merge |

Final head: `f42c886c9abf311af64152eda669cbb040460bd1`. `git diff a2cf652 f42c886` is that
README alone (+5 -2). No build, suite or campaign reads it. The only README references
in the Makefiles, drivers and scripts are comments, plus `make check`'s link, ID and
figure gates, and those were rerun at `f42c886`. The 13 campaigns ran on the
`a2cf652` tree. acmp and d3 were still running when the README was committed, and
their private trees copy only `hdl`, `tb/common` and `tb/pp_top`.

### Round 1c records: processor gates

Base is merged main `246cbc22`, in the scratch parent's protocol-processor checkout
(detached, ignored products cleaned first). Head is `a2cf652`, in the lane tree after
`git clean -fdX`. Both ran at the same time, each gate unpiped in the foreground of its
own detached job, with its own log, rc and duration. Pinned Verilator 5.050 came first
on PATH, then sv2v 0.0.12 and Yosys 0.33. The final head `f42c886` reran every gate
on a cleaned lane tree (table below).

| Gate | Base 246cbc22 | Head a2cf652 | Comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,029 checks, 0 failing (3,146 s) | rc 0, 1,030,123 checks, 0 failing (3,098 s) | 5 lines differ, the lane's own deltas as in rounds 1 and 1b: UPC map 61 → 62 constants / 90 → 91 entry points; aecp_notify 80 → 86 (LF); pp_top 10,519 → 10,599 (RDC, LN); ucpu 437 → 445 (RC, L3/L3b); the total (+94) |
| executed REQ-tag check | rc 0, 233 evidence lines | rc 0, 233 | log identical; evidence identical as sorted with source lines masked |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | links 1202 → 1204, aecp entries 84 → 85, ids 608 → 617 files: the lane's deltas, as in round 1 |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 (125 s) | rc 0 (126 s) | identical with all.v line numbers masked (six memory warnings) |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | rc 0 | the same |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | rc 0 | identical with source and all.v line numbers masked |

### Round 1c records: campaigns

These are all 13 campaigns that build a changed file, as in rounds 1 and 1b (the merge
changes no other file of the lane's set). Each ran with a fresh output directory
outside the trees and TMPDIR in scratch. Base ran in the submodule at `246cbc22` and
head in the lane at `a2cf652`, two streams each. `receipts/r1c/compare/` holds the
table, the sorted masked diffs and the per-mutant failing-check sets.

| Campaign | Base 246cbc22 | Head a2cf652 | Comparison |
|---|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 58 checks PASS (1,591 s) | rc 0, 67 checks PASS (1,732 s) | the 9 `rdc-*` arms added, each KILLED by name. `lk-sctrl-lock-nop` 12 → 13, `rd-tail-uncut` 9 → 16, `rd-str-short-guard-nop` 1 → 6 (README rows as recorded since round 1). The other 55 records fail the same checks. All 67 are identical to round-1b head |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 109 of 109 KILLED, goldens PASS (2,217 s) | rc 0, 125 of 125 KILLED, goldens PASS (3,289 s) | the 16 lock controls and their 2 goldens added. 120 records identical. `occupancy_push_unseen` 7 → 9 and `occupancy_reset_set` 14 → 17 (above). All 16 lock controls identical to round-1b head |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected | rc 0, same | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS | rc 0, same | one line: `td-lock-default-59s` still fails TD1, whose message names flags UNLOCK (as round 1b) |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS | rc 0, same | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected | rc 0, same | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS | rc 0, same | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED | rc 0, same | identical as sorted |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS | rc 0, same | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS | rc 0, same | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,392 s) | rc 0, same (2,216 s) | identical as sorted; all 57 records fail the same checks |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed | rc 0, same | identical with source and all.v line numbers masked |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (5,084 s) | rc 0, same (5,023 s) | identical as sorted; all 116 records fail the same checks |

Not run, as in rounds 1 and 1b, because they build no file this lane changes:
tb/srp_top and tb/srp_admission mutants (#184 changed their sources, but on main; the
lane changes none of them), tb/acmp_talker/retry_mutants.py, tb/desc_mem_guard/mutate.py,
tb/desc_store's lint mutations and `make -C tb/nvm_port figures`.

### Round 1c records: the final head f42c886

Every processor gate ran again at `f42c886` in the lane tree, after the head campaigns
and `git clean -fdX`. Each log is byte-identical to its `a2cf652` log:
run_suites (rc 0, 1,030,123 checks, 1,882 s), the REQ-tag check and its evidence,
lint_hdl, make check, gen_matrix, syn/yosys/run.sh under 0.33 and 0.66, and the
Yosys elab guards (`receipts/r1c/compare/head-vs-final-head.txt`). The exact-edit anchor
check at `f42c886` finds 622 edits, 0 failures. After the gates and the cleaning,
`git status --short --ignored` is empty.

### Round 1c scratch-parent consumer gates

The scratch parent is the same clone of kebag-logic/milan-fpga at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. This round it is committed, locally, on a
local branch `pp185-a647-r1c-scratch`, and it was never pushed:

| Parent commit | Subject |
|---|---|
| `40f12b103` | Scratch: parent-evidence-classification.patch (#180) |
| `63d7b6d9e` | Scratch: parent-adoption-milan_dp-67.patch (#176) |
| `e418e44bc` | Scratch: protocol-processor at merged main 246cbc22 (base pass) |
| `fbc999ff6` | Scratch: protocol-processor at lane head f42c886c (head pass) |

The two patch commits hold the patches verbatim: `git apply --check -R` of each passes
on the tree, sha256 76625170…495e and e142e2e7…66d3. `git diff --stat e9cbb676 HEAD`
is exactly their two files plus the gitlink. Each pass checked, before running, that
the gitlink was committed at the pass's SHA (`git rev-parse HEAD:protocol-processor`)
and the submodule was checked out there. Every git command was preceded by a
`rev-parse --show-toplevel` check. Both trees' ignored products were cleaned, and
`git status --short` in the parent is empty before and after each pass. The base pass
ran after the base processor streams, since it shares their checkout; the head pass
ran after the base pass.

| # | Parent consumer gate | Base (246cbc22) | Head (f42c886) | Comparison |
|---|---|---|---|---|
| 1 | check_cpp_idiom.py | rc 0 | rc 0 | identical |
| 2 | check_py_idiom.py | rc 0 | rc 0 | 258,874 → 259,068 lines (the lane's +194, as in round 1b) |
| 3 | check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | check_port_contracts.py | rc 0 | rc 0 | protocol-processor ports 1,763 → 1,765 (`rgy_flags_o`, `rgy_flags_i`, documented); undocumented 111 <= 111 |
| 6 | measure_naming.py --check | rc 0 | rc 0 | the same two ports (3,991 → 3,993 ports); candidates unchanged |
| 7 | measure_test_evidence.py --check (#180 patch) | rc 0 | rc 0 | identical |
| 8 | docs_check.py | rc 0 | rc 0 | identical |
| 9 | check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | sw/builder/test_builder.py | rc 0 (1,358 s) | rc 0 (1,442 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both (gate 11's external build tree). With the round-1 masking (the NVM writer self-test arms' timing-dependent finding counts and first findings; all 70 `self-test OK` at both), identical except two temp names |
| 11 | lint_rtl.py --check | rc 0 | rc 0 | identical |
| 12 | make -C tb/verilator/pp_shadow | rc 0 | rc 0 | RESULT: PASS; 2,188 PASS/FAIL lines identical as sorted; `ucode.hex` 90 → 91 programs; parallel-make output order |
| 13 | nvm_cosim lint | rc 0 | rc 0 | Verilator walltimes only |
| 14 | nvm_cosim quick | rc 0 | rc 0 | identical |
| 15 | make -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 (1,766 s) | rc 0 (1,731 s) | 13 RESULT: PASS; 1,143 PASS/FAIL lines identical as sorted; `ucode.hex` 90 → 91; phase timings, output order; 16 of 360 informational `timestamp` lines moved by a constant 5,120 ns (stamp and phc), residuals identical, as in round 1 |
| 16 | make -C tb/verilator/milan_dp_render | rc 0 | rc 0 | PASS/FAIL identical as sorted; `ucode.hex` 90 → 91; output order |
| 17 | flock $VIVADO_LOCK xvlog_gate.py --check | rc 0, 0 findings | rc 0, 0 findings (3,290 s, most of it waiting on another lane's exclusive lock) | the pin line only (246cbc22 → f42c886c) |

### Round 1c: accepted lengths, refusal cases and new checks

Round 1c changes no behaviour of either side, so the accepted lengths and refusal cases
are those of round 1 (READ_DESCRIPTOR) and the round-1b LOCK_ENTITY notification table
below. Round 1c adds no new check. Its only check-related change is the merge order
LF → CQ → OC1 in `tb/aecp_notify`'s default run. Every check of both sides keeps its
planted mutant, and each mutant is still KILLED by its named check at the head: the 9
`rdc-*` arms, the 16 lock controls, and #181's 11 occupancy controls (named failing
words in rounds 1 and 1b below, and in `tb/aecp_notify/README.md` for #181's).

### Round 1c acceptance

| Item | Met | Where |
|---|---|---|
| Merge origin/main into the branch, one merge commit, no rebase | yes | `a2cf652` (parents `fcb6b513`, `246cbc22`) |
| #181 kept: `cmdq_nempty_r == (count != 0)`, its in-tree checks, the router scan | yes | the pick reads `cmdq_nempty_r` (`KL_aecp_notify.sv:846`); OC1 in every run and CQ pass (86 checks); its 11 controls KILLED; `hdl/packet_engine` identical to main |
| The lane kept: LOCK_ENTITY flags (both unlocks UNLOCK) and the CONTROL overlay | yes | LF, LN, L5b, L6d, TD1, RN, L3/L3b, RDC pass; the 16 lock and 9 `rdc-*` arms KILLED, each record identical to round 1b |
| Generated records only through their generators | yes | none needed re-recording (no generator input changed); the README mutation record follows the campaign |
| Every processor gate at merged base and head, rc 0 | yes | tables above; final head byte-identical to the merge |
| Every campaign building a changed file, base and head, rc 0 | yes | the 13 above |
| Parent consumer gates, committed local scratch parent at dev e9cbb676 with the two patches | yes, 17 of 17 rc 0 at base and head | table above |
| Receipts under the output directory, with an index generated from the files present | yes | `receipts/r1c/`, `receipts/INDEX.md` |
| One-line commit subjects; no push; TAKEN not posted again | yes | |
| STOP conditions | none hit | `git diff fcb6b513 f42c886 -- hdl/top hdl/common hdl/aecp/ucpu_pkg.sv` is empty (main changed none of them either); against main `246cbc22` the only `hdl/top` lines are round 1's internal wire and its two connections (+3); no register-map, top-level port or parameter change |

## Round 1b

Manager correction on #186 (comment 6253571045, read exactly): the round-1 instruction
that the lock-timeout notification keeps flags 0 is withdrawn. Both unlock
notifications, the command-driven one and the automatic one after the one-minute
timeout (Milan v1.2 Table 5.22), carry flags UNLOCK with locked_id 0 (IEEE
1722.1-2021 7.5.2, 7.4.2.1 Table 7-143). I checked the clauses: Table 5.22's
LOCK_ENTITY row says only "Sent when the entity automatically unlocks itself after
the one (1) minute timeout"; Table 7-143 defines bit 31 (value 1) as UNLOCK and bits 0
to 30 as reserved.

New head: `fcb6b5138e17b33a3c51572594a1aa210aa0bef1`, one commit on `c8261711`:

| Commit | Subject |
|---|---|
| `fcb6b51` | LOCK_ENTITY: the automatic unlock's notification carries UNLOCK, as the command-driven one does (#186) |

Nothing was pushed, nothing was rebased or amended, and TAKEN was not posted again.

### Round 1b changes (file:line at fcb6b51)

- `hdl/aecp/KL_aecp_notify.sv:423`: `LOCKF_UNLOCK_C = 32'h0000_0001` (Table 7-143 UNLOCK).
  `:1393` (the timeout coalesced into a pending lock round) and `:1398` (the timeout
  with no round pending) latch `LOCKF_UNLOCK_C` where they latched 0. Comments at
  `:102-105` (banner), `:422`, `:1391`. A LOCK or UNLOCK still latches the command's
  whole word (`:1443`, `:1459`, unchanged), and the reset value stays 0.
- `hdl/aecp/KL_aecp_engine.sv:2971`, `hdl/aecp/ucode/gen_ucode.py:1175-1179`: comments
  only (the job's arguments are UNLOCK for the timeout). The microcode, `ucode.hex` and
  every ROM are unchanged: E_LOCKUNS still emits r14[31:0].
- `hdl/aecp/ucode/aecp_commands.json:69`: the notify doc string, "auto-unlock with flags
  UNLOCK", which renders F06.14's LOCK_ENTITY row (`06_aecp_engine.md:253`).
- `tb/pp_top/sim_main.cpp:12523` (`LN_AUTO_FLAGS = 1`), `:12567`: **LN2** now expects
  flags UNLOCK and locked_id 0 ("LN2 the auto-unlock after that LOCK (Milan Table 5.22)
  carries UNLOCK"). `:5279-5284`: **L6d** (main suite, the 400 ms wrap timeout) expects
  flags 1. Comments at `:12514-12515`.
- `tb/pp_top/notify_phases.hpp:2394`, `:2403-2404`: **TD1** (the sixth build, the top's
  60,000 ms default) expects flags UNLOCK. `:1655`: section **RN**'s independent lock
  model predicts UNLOCK on the automatic unlock's pushes. `:1603`: the same model's
  push after the holder's UNLOCK now predicts the UNLOCK's flags, 1. That line has been
  stale since round 1 (round 1 made the UNLOCK's notification echo its flags but left
  the model at 0). The fixed seed never reaches it: its 7 lock takes end in 6 automatic
  unlocks, and the lock is still held at the end. It is corrected here because it is
  the same "both unlocks carry UNLOCK" contract.
- `tb/aecp_notify/sim_main.cpp:389-391`: **LF2** (a timeout coalesced over a pending
  LOCK) expects job args 0000/0001, flags UNLOCK. Comment at `:332-339`.
- `tb/ucpu/sim_main.cpp:1354-1360`: **L3b** runs E_LOCKUNS with the auto-unlock job's
  r14 = 1 and expects flags UNLOCK, locked_id 0.
- `tb/pp_top/notify_mutants.py:623-633`, `:640-644`, `:662-667`, `:692-697`: LN2's new
  words, the two anchors `LOCKF_TIMEOUT` and `LOCKF_COALESCED`, the earlier two timeout
  controls re-anchored, and three new controls (below).
- Docs: `06_aecp_engine.md:253,806-819,1295` (§6.8's flags paragraph, F06.14, the
  opcode answers); `00_MILAN_COMPLIANCE_REVIEW.md:600` (decision row 16, its evidence
  adds L6d); `09_verification.md:330` (the LF row); `tb/pp_top/README.md` (TD1 at
  `:915`, LN at `:2326-2331`, RN at `:2573`, the #186 paragraph at `:2813` and its
  rows at `:2924-2937`); `tb/aecp_notify/README.md:360,370,378,382`;
  `tb/ucpu/README.md:80`.

### Round 1b: the LOCK_ENTITY notification table (coalesced changes included)

This supersedes the round-1 table under "Accepted lengths and refusal cases" below.
Command lengths and answers are unchanged from base (cdl 28; SUCCESS / ENTITY_LOCKED /
BAD_ARGUMENTS / NOT_SUPPORTED, flags echoed). The unsolicited LOCK_ENTITY goes to every
registered controller except the requester (an automatic unlock excludes nobody):

| Cause | Notification flags @24..@27 | locked_id | Round 1 (c826171) |
|---|---|---|---|
| a LOCK that took the lock | the LOCK's whole flags word (reserved bits included) | the new holder | same |
| an UNLOCK that released it | the UNLOCK's whole flags word (UNLOCK = 1, reserved bits included) | 0 | same |
| the lock timeout, no round pending (Milan Table 5.22 automatic unlock) | **UNLOCK (0x00000001)** | 0 | 0 |
| the lock timeout coalesced into a pending lock round | **UNLOCK (0x00000001)**, no exclusion | 0 | 0 |
| a LOCK coalesced over a pending timeout round | the LOCK's own word | the holder now | same |
| no change (already-unlocked query, refused LOCK, keep-alive) | no notification (unchanged) | - | same |

### Round 1b checks, planted mutants and failing words

Changed checks: LN2, L6d, TD1, RN (model), LF2, L3b. Each fails when the timeout is
planted back to 0, which is the round-1 behavior and what the qualification observed:

| Check | Planted mutant | Where measured | Failing words |
|---|---|---|---|
| LN2 (section AX, default build) | `lock_timeout_flags_zero`: the no-round timeout latches `32'd0` | notify campaign | `LN2 the auto-unlock after that LOCK (Milan Table 5.22) carries UNLOCK: flags 0x00000001, locked_id 0x0000000000000000, byte-exact` |
| L6d (main suite) | `lock_auto_unlock_flags_zero`: the same edit | notify campaign | `L6d: 60 s auto-unlock notifies (Milan Table 5.22), flags UNLOCK, locked_id 0, seq 3` |
| LF2 (tb/aecp_notify) | `lock_coalesced_timeout_flags_zero`: the coalesced timeout latches `32'd0` | notify campaign | `LF2: X's LOCK with flags 0x00040000 times out before its round leaves: the coalesced notification is the auto-unlock's, flags UNLOCK (job args 0000/0001)` |
| LN2 (line build), RN, TD1, L6d | both timeout latches `32'd0` (hand-planted, `receipts/r1b/hand/`) | `make` in tb/pp_top, then `make aecp-line` and `make timer-defaults` | default build `10057 checks, 3 failures`: L6d, LN2, `RN: ... zero divergence from the independent registry and lock model (6 of 2211 frame comparisons diverged)`; line build `279 checks, 1 failures`: LN2; defaults build `3 checks, 1 failures`: `TD1: T-LOCK-UNLOCK at its default: ... (LOCK_ENTITY, u = 1, flags UNLOCK, locked_id 0) ...` |
| L3b (tb/ucpu) | E_LOCKUNS flags from r12 = 0 (hand-planted) | `make` in tb/ucpu | `445 checks: 443 PASS, 2 FAIL`: `L3 the causing command's flags echoed at @24, got 00000000`, `L3b flags UNLOCK, locked_id 0 (00000000 00000000 00000000)` |

The tree was restored after each hand-planted run and checked clean (`git status`
empty), and `git clean -fdX` ran before the gates.

The notify campaign's lock controls, measured on their own (`--jobs 4 --only`, the 16)
and again in the full campaign, identical: goldens PASS, 16 of 16 KILLED.

| Control | Planted | Failing checks (round 1 → 1b) |
|---|---|---|
| `lock_unlock_notifies_flags_zero` | E_LOCKUNS flags from r12 (the #186 reproduction) | L5b → L5b, L6d |
| `lock_auto_unlock_flags_zero` (new) | the timeout latches 0 | L6d |
| `lock_notification_flags_zero` | the same E_LOCKUNS edit, section AX | LN1, LN4 → LN1, LN2, LN4 |
| `lock_flags_unlock_bit_only` | the latch takes `{31'd0, rgy_op_i[0]}` | LN1, LN4 (same) |
| `lock_timeout_keeps_flags` | the timeout no longer writes the latch (keeps the LOCK's word) | LN2 (same) |
| `lock_timeout_flags_zero` (new) | the timeout latches 0 | LN2 |
| `lock_flags_from_exclusion` | the job's arguments from the exclusion eid | LN1 to LN4 (same 4; LN2's words now "carries UNLOCK") |
| `lock_job_arguments_dropped` | the engine loads a LOCK job like any other | LN1, LN4 → LN1, LN2, LN4 |
| `lock_job_r14_unpacked` | `lockf_w = lockc_r` | LN1, LN4 → LN1, LN2, LN4 |
| `lock_notification_not_sent` | the LOCK job runs UPC_NOSEND_C (premise) | LN1 to LN4 (same) |
| `lock_response_flags_zero` | E_LOCKEN's response flags from r12 (premise) | LN1, LN4 responses (same) |
| `lock_coalesced_timeout_keeps_flags` | the coalesced timeout keeps the LOCK's word | LF2 (same) |
| `lock_coalesced_timeout_flags_zero` (new) | the coalesced timeout latches 0 | LF2 |
| `lock_take_keeps_old_flags` | a LOCK latches nothing | LF1, LF3 → LF1, LF3a, LF3 |
| `lock_release_keeps_old_flags` | an UNLOCK latches nothing | LF1b (same) |
| `register_refused` | the REGISTER answered NO_RESOURCES (premise) | LK0, LN0 (same) |

The new failures in the earlier controls come from the timeout's UNLOCK. A word of 0
or a stale LOCK word on the automatic unlock now differs from the expected 1 (LN2,
L6d), and LF3a's LOCK with flags 0 follows a timeout that latched 1.

### Round 1b records (head fcb6b51)

Base records are those of round 1 (`08ae0013`, unchanged). Head ran in the lane tree
after `git clean -fdX`, and each new record was compared with base and with the round-1
head `c8261711`. Pinned Verilator 5.050 first on PATH, then sv2v 0.0.12 and Yosys 0.33.
Each gate ran unpiped in the foreground of its own detached job, with its own log, rc
and duration.

| Gate | Head fcb6b51 | vs round-1 head c8261711 | vs base 08ae0013 |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,094 checks, 0 failing (2,183 s) | identical | as in round 1: UPC map 61 → 62 / 90 → 91, aecp_notify 67 → 73, pp_top 10,519 → 10,599, ucpu 437 → 445 |
| executed REQ-tag check | rc 0 | log identical; evidence identical with source lines masked (pp_top lines after L6d +1) | evidence identical as sorted with lines masked |
| scripts/lint_hdl.sh | rc 0 | identical | identical |
| make check | rc 0 | identical | as in round 1 (links 1196 → 1198, aecp entries 84 → 85, ids 592 → 601) |
| scripts/gen_matrix.py --check | rc 0 | identical | identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 | six memory warnings' all.v lines +1 (the new localparam) | as in round 1, those lines moved |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | the same six lines +1 | the same |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | inventory line of `KL_aecp_notify.g_rows_guard` +2 (the banner), all.v lines +1 | as in round 1, lines moved |

Campaigns at head `fcb6b513`: all 13 that build a changed file, as in round 1 (the
round-1b files are the notify block, the engine's and the generator's comments, the
command table, and the pp_top, aecp_notify and ucpu benches). Two streams in the lane
tree, each output directory fresh and outside the tree, TMPDIR scratch. Base records are
round 1's.

| Campaign | Head fcb6b513 | vs round-1 head c8261711 |
|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 67 checks PASS | identical, line for line (durations masked) |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 114 of 114 KILLED, goldens PASS (2,406 s) | the 3 new controls added; every non-lock control fails the same checks; the lock controls' changes are those in the table above |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected (695 s) | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS (1,382 s) | identical but for one failing-check line's text: `td-lock-default-59s` still fails TD1 (59,003 ms), whose message now names flags UNLOCK |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS (280 s) | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected (763 s) | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS (62 s) | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED (457 s) | identical as sorted lines |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS (208 s) | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS (681 s) | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,026 s) | summary identical; each mutant's failing checks identical except `armq_read_tail`'s L6d line, whose message now names flags UNLOCK (the same check) |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed (1,319 s) | identical with all.v line numbers masked (47 lines, +1) |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (4,546 s) | identical; each of the 117 records' failing checks identical |

Not run, as in round 1, because they build no changed file: tb/srp_top and
tb/srp_admission mutants, tb/acmp_talker/retry_mutants.py, tb/desc_mem_guard/mutate.py,
tb/desc_store's lint mutations and `make -C tb/nvm_port figures`.

### Round 1b scratch-parent consumer gates

Same scratch parent (dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, never committed or
pushed). In the submodule (`rev-parse --show-toplevel` checked before every git command)
the head was fetched from the lane and checked out detached at `fcb6b513`, its ignored
products cleaned, and the gitlink staged at
`fcb6b5138e17b33a3c51572594a1aa210aa0bef1`. The parent's ignored products were also
cleaned. The two parent patches are still applied verbatim, and `git apply --check -R`
of each passes (sha256 76625170…495e and e142e2e7…66d3). `git diff --stat` shows exactly
their two files.

| # | Parent consumer gate | Base (08ae0013) | Head (fcb6b513) | vs round-1 head (c8261711) |
|---|---|---|---|---|
| 1 | check_cpp_idiom.py | rc 0 | rc 0 | identical |
| 2 | check_py_idiom.py | rc 0 | rc 0 | 258,981 → 258,994 lines (the driver's +13) |
| 3 | check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | check_port_contracts.py | rc 0 | rc 0 | identical |
| 6 | measure_naming.py --check | rc 0 | rc 0 | identical |
| 7 | measure_test_evidence.py --check (#180 patch) | rc 0 | rc 0 | identical |
| 8 | docs_check.py | rc 0 | rc 0 | identical |
| 9 | check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | sw/builder/test_builder.py | rc 0 | rc 0 (1,912 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both (gate 11's external build tree). With the round-1 masking (the NVM writer self-test arms' timing-dependent first findings; all 70 `self-test OK` at both), identical except two temp names |
| 11 | lint_rtl.py --check | rc 0 | rc 0 | identical |
| 12 | make -C tb/verilator/pp_shadow | rc 0 | rc 0 | RESULT: PASS; 2,188 PASS/FAIL lines identical as sorted; Verilator build sizes |
| 13 | nvm_cosim lint | rc 0 | rc 0 | Verilator walltimes only |
| 14 | nvm_cosim quick | rc 0 | rc 0 | identical |
| 15 | make -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 | rc 0 | PASS/FAIL lines identical as sorted; otherwise Verilator build sizes and render-phase timings |
| 16 | make -C tb/verilator/milan_dp_render | rc 0 | rc 0 | records identical as sorted; build sizes |
| 17 | flock $VIVADO_LOCK xvlog_gate.py --check | rc 0, 0 findings | rc 0, 0 findings | the pin line (c8261711 → fcb6b513) |

### Round 1b acceptance

| Item | Met | Where |
|---|---|---|
| Correction: the automatic unlock after the timeout carries flags UNLOCK, locked_id 0 | yes | `KL_aecp_notify.sv:1393,1398`; LN2, L6d, TD1, RN, LF2, L3b |
| Correction: the command-driven unlock carries UNLOCK, locked_id 0 | yes (since round 1: it echoes the UNLOCK's word) | L5b, LN4, LF1b |
| LN2 updated, its planted mutant keeps 0 and fails | yes | `lock_timeout_flags_zero` → LN2; also `lock_auto_unlock_flags_zero` → L6d, `lock_coalesced_timeout_flags_zero` → LF2, and the hand-planted runs |
| Docs and the handoff's coalesced-change table | yes | above; 06 §6.8, F06.14, compliance row 16, 09, READMEs |
| Gates, campaigns, parent consumer gates rerun, rc 0 | yes | tables above |
| STOP conditions | none hit | no register-map, top-level port or parameter change (`git diff c826171 HEAD -- hdl/top hdl/common hdl/aecp/ucpu_pkg.sv` is empty) |

REVIEW READY with the new head was posted on #185 (comment 6257747212).

## Status (round 1)

Round 1 text below is kept as written at `c8261711`. Where it says the timeout keeps
flags 0, round 1b supersedes it.

- TAKEN was posted on #185 (comment 6249589802) in the first session. It was not posted again.
- Done. Both commits are on the lane branch at head `c826171`. Every processor gate and
  every campaign that builds a changed file is rc 0 at base and at head. All 17 parent
  consumer gates are rc 0 at base and at head. Every record difference is listed and
  explained below. REVIEW READY is posted on #185 with the head (comment 6255090417).

## Resume notes (second session)

- The first session was stopped by the manager at 14:3x. All of its edits were intact in the
  tree, uncommitted. I checked that no planted mutant had been left in it. Every
  `rdc-*.patch` still applies forward (`git apply --check`) and none applies in reverse. The
  campaign anchor check found every exact-edit anchor of the 16 drivers exactly once (594
  edits, 0 failures). Every tree file matched the intended change in the diff review.
- The base `run_suites.sh` had been cut off. It was re-run from the start in the scratch
  submodule at base.
- The tree was split into the two commits by hunk. Mixed hunks were applied by exact string
  edits, and the full state was kept in a stash and a scratch backup. At the #185 commit,
  `tb/aecp_cmds/decode.json` was re-swept (`make -C tb/aecp_cmds record`, 617,916 trials)
  and the ucpu README count was set to that commit's 442. After the #186 commit, the
  head's tracked files were byte-identical to the backup, and the re-swept record matched
  the first session's byte for byte.
- After measuring the new arms on their own, I added their mutation records to the suite
  READMEs and to 09. To keep two commits, the branch was reset to the #185 commit, that
  commit was amended, the #186 commit was cherry-picked and amended. There was no rebase,
  and nothing had been pushed. The superseded SHAs were `8b86d69` and `ccb8b6f`.
- The full dispatch campaign at `60da763` showed three earlier arms failing more checks
  than at base, because they also reach new RDC or LN checks (below). Their README rows
  were updated. Head campaigns were running in the lane tree at the time, so I rebuilt
  the two commits with `git commit-tree` from a temporary index, each being the earlier
  commit's tree with the new `tb/pp_top/README.md` blob. The branch was moved with
  `git update-ref`, and only the README was refreshed in the working tree.
  `git diff 60da763 ccd1b8b` touches `tb/pp_top/README.md` alone (+10 -4). The
  superseded SHAs were `722d585` and `60da763`. Nothing reads that README except
  `make check`'s link, ID and figure gates (a search of the campaign drivers, Makefiles
  and scripts finds only comments).
- The first parent consumer pass at `ccd1b8b` failed gate 1, `check_cpp_idiom.py`:
  "FAIL: multi-declarator declaration 2 > ratchet 0" (Rule 11 of the parent's
  CODE_QUALITY.md). Both findings were mine, in `tb/pp_top/sim_main.cpp`
  (`const uint8_t v0 = ..., v1 = ...;` and the same for `t0, t1`, in
  `rd_control_after_set`). I stopped that pass and the head campaigns that were running,
  split the two declarations in the #185 commit (and so in the #186 tree), and rebuilt
  both commits the same way (`198f1b1`, `c826171`; `ccd1b8b` and `37ef8c3` superseded).
  `git diff ccd1b8b c826171` is that file alone (+4 -2). The probe's gates 2-11 passed;
  its records are kept under the scratch records as `probe-parent-ccd1b8b` and are not
  counted. Every processor gate, every campaign that builds `tb/pp_top/sim_main.cpp`, and
  every parent consumer gate was then run again at `c826171`.
- `make check` passes at both commits (rc 0).

## Scope notes

- The session brief names "E_SCFG" as the allowed change scope and "Closes #179" for the PR
  body. #179 (SET_CONFIGURATION, closed and merged) and E_SCFG belong to another lane. This
  lane's assignment (A10, comment 6249574548) covers #185 (READ_DESCRIPTOR's CONTROL overlay)
  and #186 (the LOCK_ENTITY notification's flags). I did the assignment exactly: the
  changes are those two arms, their tests, the generators and records that must follow them,
  and the docs that record them. E_SCFG is untouched. The PR body closes #185 and #186, not
  #179.
- STOP check: there is no register-map, top-level port or parameter change.
  `git diff 08ae001 HEAD -- hdl/top` adds one internal wire (`aecp_rgy_flags_w`) and its two
  connections, and nothing in `protocol_processor_top`'s port or parameter list. The
  `hdl/common` package, `ucpu_pkg.sv` and every register map are unchanged. Two internal
  module ports were added, `KL_aecp_engine.rgy_flags_o` and `KL_aecp_notify.rgy_flags_i`
  (32 bits each). They are wired only inside `protocol_processor_top` and in the
  `tb/aecp_cmds` wrapper (left open). Nothing in the parent instantiates either module; a
  search of the scratch parent finds only comments and source lists.

## Changes (file:line at head c826171)

### #185 READ_DESCRIPTOR CONTROL current value (commit 198f1b1)

- `hdl/aecp/ucode/gen_ucode.py:257`: `E_RDESCCT = 600`, in the free 594..639 run in front
  of E_RDESC.
- `hdl/aecp/ucode/gen_ucode.py:1286-1344`: the clause comment, the layout constants
  (`CT_VTYPE_LANE` 80, `CT_VOFF_LANE` 88, `CT_VALUES` 104, `CT_LINEAR_INT16` 0x0002,
  `CT_CUR_OFF` 108, `CT_CUR_TAIL` 112), and the `E_RDESCCT` program at
  `gen_ucode.py:1308`. It runs the configuration check and the locate, then three layout
  guards to E_RDESC. Otherwise it copies image bytes 0..107, puts `current[0]` @108 from
  `RGN_DYN + SEL_IDENT` (GET_CONTROL's row, no image arm), rebuilds 109..111 from the
  image lane, and copies the TAIL from 112. Placement asserts: `E_RDESCCT + 12` and `+ 17`.
- `hdl/aecp/KL_aecp_engine.sv:904`: `UPC_RDESCCT_C = 11'd600`.
- `hdl/aecp/KL_aecp_engine.sv:3303-3314`: the re-dispatch at the @28 seam. It applies to
  AEM, message_type 0, READ_DESCRIPTOR, cdl >= 20, configuration 0 and descriptor_type
  CONTROL, and it sits beside issue #82's four.
- `hdl/aecp/ucode/aecp_commands.json:91`: READ_DESCRIPTOR's entries gain `RDESCCT`.
- `tb/aecp_cmds/decode.json:62`: `RDESCCT` floor 20, cdls 20 and 100, SUCCESS at 129. RDESC
  loses its 129 answer. The trial count and the engine and ROM digests were re-swept.
- `tb/ucpu/sim_main.cpp:46,205-221,288,861-899`: section RC (RC1, RC2) on a conformant
  113-byte IDENTIFY CONTROL. `tb/ucpu/README.md:6,70-76` record it.
- `tb/pp_top/sim_main.cpp`: AX fixture (CONTROL_LINEAR_UINT8, lane 0xA0..0xA7, image
  `current[0]` 0x5A); RDC0 at `:12383`; RDC1 to RDC3b at `:12029` (`rd_control_after_set`);
  RDC4 at `:12108`; RDC5 (before and after the power cycle) to `:12454`; RDC6 (a 111-byte
  CONTROL) to `:12505`; the helpers `rd_ctrl` and `rd_ctrl_image` at `:12353` and `:12358`.
- `tb/pp_top/aecp_dispatch_mutants.py:135-162` and the nine
  `tb/pp_top/aecp_dispatch_mutations/rdc-*.patch`.
- Docs: `docs/architecture/06_aecp_engine.md:306,315,336-354,1294` (§6.1 overlay table
  row, the CONTROL paragraph, the opcode answer row); `docs/00_MILAN_COMPLIANCE_REVIEW.md:599`
  (decision row 15); `docs/architecture/09_verification.md:185` (Identify row);
  `tb/pp_top/README.md` (section AX title, the RDC bullet, nine arm rows and their note,
  and the three earlier rows the RDC checks move: `lk-sctrl-lock-nop` 12 → 13,
  `rd-tail-uncut` 9 → 16, `rd-str-short-guard-nop` 1 → 5).

### #186 LOCK_ENTITY notification flags (commit c826171)

- `hdl/aecp/ucode/gen_ucode.py:1166-1186`: E_LOCKUNS builds flags @24 from r14[31:0], the
  causing command's word (`gen_ucode.py:1183`), where it used r12 = 0. The comment states
  the register contract.
- `hdl/aecp/KL_aecp_engine.sv:528`: output `rgy_flags_o`. At `:2273` it is
  `{cfg_ix_r, desc_ix_r}`, LOCK_ENTITY's @24..@27 as E_LOCKEN echoes it.
- `hdl/aecp/KL_aecp_engine.sv:1589-1598`: `lockf_w` packs r14[31:0] as LOCK_ENTITY's
  for the command and for the notification job routed to the rgy face (`uns_r && regun_r`).
- `hdl/aecp/KL_aecp_engine.sv:2970-2978`: a PP_UNS_LOCK_C job lands `uns_arg1_i` and
  `uns_arg0_i` in `cfg_ix_r` and `desc_ix_r`.
- `hdl/aecp/KL_aecp_notify.sv:94-103` (banner), `:271` (`rgy_flags_i`), `:420` (`lockf_r`),
  `:836-837` (the job's arguments), `:1224` (reset), `:1390` and `:1395` (the timeout,
  coalesced or not, latches 0), `:1440` and `:1456` (a LOCK or UNLOCK latches the command's
  word).
- `hdl/top/protocol_processor_top.sv:3451,3857,4065`: the internal wire and its two
  connections.
- `tb/aecp_cmds/aecp_cmds_wrap.sv:231`: `.rgy_flags_o ()`.
- `hdl/aecp/ucode/aecp_commands.json:69`: the notify doc string, which renders F06.14's
  LOCK_ENTITY row (`06_aecp_engine.md:253`).
- `tb/aecp_notify/sim_main.cpp:137` (`lock_op`), `:340-403` (section LF: LF1, LF1b, LF2,
  LF3a, LF3), and `tb/aecp_notify/README.md` (the build table, the count and section LF).
- `tb/ucpu/sim_main.cpp:1340-1359`: L3 (flags 0x80010001 echoed), L3b (auto-unlock 0).
- `tb/pp_top/sim_main.cpp:5231-5240`: L5b expects the UNLOCK's flags 1. `:12508-12572`:
  section LN (LN0 to LN4).
- `tb/pp_top/notify_mutants.py:622-704`: `LOCK_FLAGS`, 13 controls.
- Docs: `06_aecp_engine.md:253,800-816,1292`; `00_MILAN_COMPLIANCE_REVIEW.md:600` (decision
  row 16); `09_verification.md` §8.4 (LF row, "eight of the notification block's");
  `tb/pp_top/README.md` (the LN bullet, 13 notify rows and their note, and
  `rd-str-short-guard-nop` 5 → 6 for LN0); `tb/ucpu/README.md:78`.

## Accepted lengths and refusal cases

READ_DESCRIPTOR (AEM, message_type 0, opcode 0x0004). The recorded sweep is
`tb/aecp_cmds/decode.json`.

| Case | Program | Answer |
|---|---|---|
| cdl 12..19 | BADARG | BAD_ARGUMENTS, the command echoed (unchanged) |
| cdl >= 20, configuration 0, CONTROL, located, length >= 112, `values_offset` 104, `control_value_type` < 0x0002 (LINEAR_INT8 or LINEAR_UINT8) | E_RDESCCT | SUCCESS: image bytes, with `current[0]` @108 = what GET_CONTROL reads (0 after reset and power cycle, the value after every SET_CONTROL); cdl 16 + length (129 for the 113-byte fixture). Padded commands (cdl 100) answer the same |
| same, length < 112 (ends inside lane 104..111) | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| same, `values_offset` != 104 | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| same, `control_value_type` >= 0x0002 (wider or non-linear) | E_RDESCCT → E_RDESC | SUCCESS, the image whole |
| CONTROL index not in the image | E_RDESCCT → E_RDSTUB | NO_SUCH_DESCRIPTOR, §7.4.5 4-byte stub (as E_RDESC) |
| `configuration_index` >= configurations_count | E_RDESCCT → E_RDSTUB | BAD_ARGUMENTS stub (as E_RDESC; unreachable with configuration 0 and one or more configurations) |
| configuration != 0, or any other type | unchanged | as at base |

GET_CONTROL answers every located CONTROL index from the same IDENTIFY row (E_GCTRL), so
the overlay agrees with GET_CONTROL for any index it serves.

LOCK_ENTITY (opcode 0x0001) accepts the same lengths and returns the same answers as at
base: cdl 28, SUCCESS / ENTITY_LOCKED / BAD_ARGUMENTS / NOT_SUPPORTED, flags echoed. What
changes is the unsolicited LOCK_ENTITY sent to every registered controller except the
requester:

| Cause | Notification flags @24..@27 | locked_id |
|---|---|---|
| a LOCK that took the lock | the LOCK's whole flags word (reserved bits included) | the new holder |
| an UNLOCK that released it | the UNLOCK's whole flags word (UNLOCK = 1, reserved bits included) | 0 |
| the lock timeout (Milan Table 5.22 auto-unlock) | 0 (round 1; **UNLOCK since round 1b**) | 0 |
| coalesced changes (a round still pending) | the last cause's (a timeout's 0, **UNLOCK since round 1b**; a LOCK's own) | the holder now |
| no change (already-unlocked query, refused LOCK) | no notification (unchanged) | - |

## New checks, planted mutants and failing words

Every arm was killed by its named check. The dispatch arms were measured with
`aecp_dispatch_mutants.py --jobs 4 --only rdc-...` and the notify arms with
`notify_mutants.py --jobs 4 --only ...`, both on the head tree (142 s and about 10 min).
The full campaigns at head re-grade them (below).

### #185 (aecp_dispatch_mutants.py, target aecp-dispatch): control PASS, 9 of 9 KILLED

| Arm | Planted | Named failing words | Failing checks |
|---|---|---|---|
| `rdc-base-no-overlay` | the engine's #185 re-dispatch removed (the issue reproduction) | `RDC1 CONTROL 0 after SET_CONTROL(255) and three refused SET_CONTROLs: READ_DESCRIPTOR byte-exact` | 7 |
| `rdc-unset-image` | E_RDESCCT given an image arm for an unwritten row | `RDC0 CONTROL 0 before any SET_CONTROL: current[0] the reset 0, not the image's 0x5A: READ_DESCRIPTOR byte-exact` | 2 |
| `rdc-voffset-guard-nop` | the values_offset guard's BRANCH replaced with NOP | `RDC2 CONTROL 0 with values_offset 106, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-vtype-int16` | the value-type bound 0x0002 moved to 0x0003 | `RDC3 CONTROL 0 as a CONTROL_LINEAR_INT16, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-vtype-uint8-only` | only CONTROL_LINEAR_UINT8 overlaid | `RDC3b CONTROL 0 as a CONTROL_LINEAR_INT8, IDENTIFY 255: overlaid: READ_DESCRIPTOR byte-exact` | 1 |
| `rdc-short-floor-111` | the too-short floor 112 moved to 111 | `RDC6 CONTROL 0 of 111 bytes, IDENTIFY 255: its image whole: READ_DESCRIPTOR byte-exact` | 2 (with LN0) |
| `rdc-unit-shift-8` | @109 from a shift of 8, not 16 | `RDC1 CONTROL 0 after SET_CONTROL(255) and three refused SET_CONTROLs: READ_DESCRIPTOR byte-exact` | 7 |
| `rdc-ident-reset-255` | the IDENTIFY row resets to 255 (premise) | `RDC0 IDENTIFY unset: GET_CONTROL reads Milan 5.3.12's reset 0 (premise)` | 5 |
| `rdc-sctrl-no-write` | E_SCTRL's IDENTIFY write a NOP (premise) | `RDC1 GET_CONTROL reads 255 (premise)` | 11 |

`tb/ucpu` RC1 and RC2 grade the program in isolation: the 113-byte form, with a one-byte
TAIL, and a `values_offset` of 106 served whole.

### #186 (notify_mutants.py): goldens PASS, 13 of 13 KILLED

| Control | Planted | Named failing words |
|---|---|---|
| `lock_unlock_notifies_flags_zero` | E_LOCKUNS flags from r12 = 0 (the issue reproduction), main suite | `L5b: C2's second notification carries sequence_id 1 (Milan 5.4.5.1) and the UNLOCK's flags 1` |
| `lock_notification_flags_zero` | the same edit, section AX | `LN1 ...its notification echoes the LOCK's flags: flags`, `LN4 ...its notification echoes the UNLOCK's flags: flags` |
| `lock_flags_unlock_bit_only` | the latch takes `{31'd0, rgy_op_i[0]}` | LN1, LN4 (as above) |
| `lock_timeout_keeps_flags` | the timeout no longer clears the latch | `LN2 the auto-unlock after that LOCK (Milan Table 5.22) carries flags 0: flags` |
| `lock_flags_from_exclusion` | the job's arguments from the exclusion eid | `LN3 ...its notification carries flags 0: flags` (and LN1, LN2, LN4) |
| `lock_job_arguments_dropped` | the engine loads a LOCK job like any other | LN1, LN4 |
| `lock_job_r14_unpacked` | `lockf_w = lockc_r` (no notification packing) | LN1, LN4 |
| `lock_notification_not_sent` | the LOCK job runs UPC_NOSEND_C (premise) | `LN1..LN4 ...: the registered bench is notified` |
| `lock_response_flags_zero` | E_LOCKEN's response flags from r12 (premise) | `LN1 a second controller's LOCK: SUCCESS echoing flags 0x00010000`, `LN4 its UNLOCK: SUCCESS echoing flags 0x80020001` |
| `lock_coalesced_timeout_keeps_flags` | the coalesced timeout keeps the latch | `LF2:` (tb/aecp_notify) |
| `lock_take_keeps_old_flags` | a LOCK latches nothing | `LF1:`, `LF3:` |
| `lock_release_keeps_old_flags` | an UNLOCK latches nothing | `LF1b:` |
| `register_refused` | the REGISTER answered NO_RESOURCES (premise) | `LN0: the bench registers for unsolicited notifications again` (and LK0) |

`tb/ucpu` L3 and L3b grade E_LOCKUNS in isolation (flags 0x80010001 echoed whole; the
auto-unlock's 0).

## Base and head records

Base ran in the scratch parent's protocol-processor checkout at `08ae0013`; its ignored
products were cleaned after `run_suites.sh` and before the base campaigns. Head ran in the
lane tree after `git clean -fdX`, first at `60da763`, then again at the final head `c826171`.
Every final-head log is identical to the `60da763` log (Verilator walltimes masked), except
the executed REQ-tag evidence: 11 pp_top source lines moved by +2, from the two split
declarations. Every gate ran in the foreground of its own
detached job, with its own log, rc and duration, never piped. The pinned Verilator
5.050 came first on PATH, then sv2v 0.0.12 and Yosys 0.33.

| Gate | Base 08ae0013 | Head c826171 | Record comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,000 checks, 0 failing (1,632 s) | rc 0, 1,030,094 checks, 0 failing (2,155 s) | every suite line identical except: UPC map gate 61 → 62 engine constants and 90 → 91 entry points (`UPC_RDESCCT_C` / `E_RDESCCT`); aecp_notify 67 → 73 (section LF: 5 checks and its registration); pp_top 10,519 → 10,599 (section AX 239 → 279, RDC +28 and LN +12, in the default and the line build); ucpu 437 → 445 (RC +5, L3/L3b +3) |
| executed REQ-tag check (check-req-tags.py --suites/--evidence) | rc 0, 226 evidence lines, 14 suites | rc 0, 226, 14 | identical; the evidence file identical but for pp_top source line numbers |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | identical except `links: 1196 → 1198` (the two new decision rows' anchors), `aecp commands: 84 → 85 entries` (RDESCCT) and `ids: 592 → 601 files` (the nine new patch files); F06.14 41 rows at both |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | identical |
| syn/yosys/run.sh (sv2v 0.0.12, Yosys 0.33, the CI pin) | rc 0, 42 tops (82 s) | rc 0 (92 s) | identical except six memory warnings' all.v line numbers (+21, the engine's and notify block's added lines) |
| syn/yosys/run.sh with the host Yosys 0.66 (second record) | rc 0 | rc 0 | the same six line numbers |
| tb/elab_guards/guards.py --frontend yosys --jobs 4 (CI portability job) | rc 0 (80 s) | rc 0 (147 s) | identical except the guard inventory's source lines (engine +2, notify +7) and the all.v line of the engine's guards (+3) |

Campaigns at base and head: every one that builds a changed file, meaning the engine, the
notify block, the top, the microcode generator and its table, or the pp_top, aecp_notify,
ucpu or aecp_cmds benches. Base ran in the scratch submodule at `08ae0013` and head in the
lane tree, each output directory fresh and outside the tree, and TMPDIR scratch. The eight
campaigns that build `tb/pp_top/sim_main.cpp` ran at `c826171`. The other five (aecp_cmds,
name_state, maap, adp, elab_guards) ran at `c826171` too, and their `60da763` runs are
identical.

| Campaign | Base 08ae0013 | Head c826171 | Comparison |
|---|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py --jobs 2 | rc 0, 58 checks PASS (1,073 s) | rc 0, 67 checks PASS (1,098 s) | the 9 `rdc-*` arms added, each KILLED by name. Three earlier arms fail more checks, every base failure kept: `lk-sctrl-lock-nop` 12 → 13 (RDC1's premise), `rd-tail-uncut` 9 → 16 (the seven overlaid RDC reads), `rd-str-short-guard-nop` 1 → 6 (RDC6's four and LN0, after RD4's unanswered read). Their README rows were updated. Every other record is identical; the `60da763` run is identical to this one, line for line |
| tb/pp_top/notify_mutants.py --jobs 2 | rc 0, 98 of 98 KILLED, goldens PASS (1,631 s) | rc 0, 111 of 111 KILLED, goldens PASS (2,202 s) | the 13 lock controls added and two goldens for their new suite runs (`--aecp-dispatch-only`, `--arm-queue-only`); every earlier control fails the same number of checks |
| tb/aecp_cmds/mutants.py --jobs 2 | rc 0, 17 of 17 detected (738 s) | rc 0, same | identical |
| tb/pp_top/aecp_mutants.py --jobs 2 | rc 0, 67 checks PASS (1,293 s) | rc 0, same (1,272 s) | identical |
| tb/pp_top/ctr_mutants.py --jobs 2 | rc 0, 18 checks PASS (356 s) | rc 0, same (287 s) | identical |
| tb/pp_top/gsi_mutants.py --jobs 2 | rc 0, 20 detected (1,059 s) | rc 0, same (866 s) | identical |
| tb/pp_top/name_wr_mutant.py | rc 0, decode killed, golden and restored PASS (101 s) | rc 0, same (64 s) | identical |
| tb/name_state/mutants.py --jobs 2 | rc 0, 16 KILLED (413 s) | rc 0, same (399 s) | identical as sorted lines |
| tb/maap/mutants.py --jobs 2 | rc 0, 32 checks PASS (160 s) | rc 0, same (179 s) | identical |
| tb/adp_engine/mutants.py --jobs 2 | rc 0, 62 checks PASS (461 s) | rc 0, same (562 s) | identical |
| tb/pp_top/acmp_mutants.py --jobs 2 | rc 0, 51 of 51 KILLED, goldens PASS (2,399 s) | rc 0, same (2,002 s) | identical as sorted lines, each mutant's failing checks identical |
| tb/elab_guards/mutants.py --jobs 2 | rc 0, 160 of 160 killed (1,414 s) | rc 0, same (1,439 s) | identical with engine, notify and all.v line numbers masked (44 lines) |
| tb/pp_top/d3_mutants.py --jobs 3 | rc 0, 110 of 110 KILLED, goldens PASS (4,830 s) | rc 0, same (4,434 s) | identical as sorted lines (117), each mutant's failing checks identical |

Not run, as they build no changed file: tb/srp_top and tb/srp_admission mutants (SRP
sources only), tb/acmp_talker/retry_mutants.py (pp_pkg, srp_pkg, KL_acmp_talker),
tb/desc_mem_guard/mutate.py (the descriptor store and its guard), tb/desc_store's lint
mutations (the image generator) and `make -C tb/nvm_port figures` (KL_pp_nvm_port).

## Scratch-parent consumer gate table

The scratch parent is a clone of kebag-logic/milan-fpga at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` under the scratch root. It was never committed
or pushed. Its submodules sit at their pins (external efeb541a, gptp-processor e4869fd0,
lwSRP 08ee86e8, tsn-c-stack 70936b77, verilog-axis 48ff7a7e). The protocol-processor
gitlink was staged (`git add`, not committed) at base `08ae0013` for the base pass. For the
head pass the head was fetched from the lane, checked out detached, and the gitlink staged
at `c8261711e040db0d89c77980b198716974b4684b`, where it was left. Every git command in the
submodule and in the parent was preceded by a `rev-parse --show-toplevel` check. The
parent's and the submodule's ignored products were cleaned before each pass.

Two uncommitted scratch-only parent edits were applied before both passes, verbatim:
- `parent-evidence-classification.patch` (#180, from the pp178 lane; 2,689 bytes, sha256
  76625170…495e): the reader classifications of the processor's elab_guards drivers;
- `parent-adoption-milan_dp-67.patch` (#176, from the pp176 lane; sha256 e142e2e7…66d3): the
  milan_dp #67 case's 2013-length SET_STREAM_INFO expectation.

`git diff --stat` in the parent at both passes shows exactly these two files
(`scripts/measure_test_evidence_readers.py` +16, `tb/verilator/milan_dp/sim_nxn.cpp` +8 -4).

| # | Parent consumer gate | Base (08ae0013) | Head (c8261711) | Comparison |
|---|---|---|---|---|
| 1 | python3 scripts/check_cpp_idiom.py | rc 0 | rc 0 | identical. The first head pass, at `ccd1b8b`, failed here with my two multi-declarator lines (resume notes); fixed |
| 2 | python3 scripts/check_py_idiom.py | rc 0 | rc 0 | no findings; 258,800 → 258,981 lines, the Python this change adds to the campaign drivers |
| 3 | python3 scripts/check_rtl_source_lists.py | rc 0 | rc 0 | identical |
| 4 | python3 scripts/pp_srcs.py --check --selftest | rc 0 | rc 0 | identical |
| 5 | python3 scripts/check_port_contracts.py | rc 0 | rc 0 | protocol-processor ports 1,761 → 1,763 (`rgy_flags_o`, `rgy_flags_i`, both documented); undocumented 111 <= 111 unchanged |
| 6 | python3 scripts/measure_naming.py --check | rc 0 | rc 0 | the same two ports counted (3,989 → 3,991 ports scanned); 95 candidates, all recorded, unchanged |
| 7 | python3 scripts/measure_test_evidence.py --check (with the #180 patch) | rc 0 | rc 0 | identical |
| 8 | python3 scripts/docs_check.py | rc 0 | rc 0 | identical |
| 9 | python3 scripts/check_sh_idiom.py | rc 0 | rc 0 | identical |
| 10 | python3 sw/builder/test_builder.py | rc 0 (1,986 s) | rc 0 (1,751 s) | ALL GATES PASS EXCEPT 1 NOT RUN at both: gate 11's calibration report needs an external build tree absent here. With temp names, durations, and the finding counts and first findings of the firmware NVM writer's self-test arms masked (those arms grade on parallel threads and stop at the first named finding, so the counts depend on timing; every arm is `self-test OK` at both), base and head are identical except one more temp name. The `vivado.log` it mentions is a synthetic file written by its constraint-log test; Vivado is not started |
| 11 | python3 scripts/lint_rtl.py --check | rc 0 | rc 0 | identical: 90 violations within the ratchet of 90 |
| 12 | make -j8 -O -C tb/verilator/pp_shadow | rc 0 (393 s) | rc 0 (411 s) | RESULT: PASS at both; the 2,188 PASS/FAIL record lines identical as sorted; differences are `ucode.hex: 2048 words, 90 → 91 programs` (E_RDESCCT) and Verilator's build sizes |
| 13 | make -j8 -O -C tb/verilator/nvm_cosim lint | rc 0 | rc 0 | identical |
| 14 | make -j8 -O -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2 | rc 0 | rc 0 | identical |
| 15 | make -j8 -O -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 (2,251 s) | rc 0 (2,106 s) | the 1,143 PASS/FAIL record lines identical as sorted (parallel legs). The rest differs only in phase timings, Verilator sizes, the 90 → 91 programs line, and 16 of 360 informational `timestamp` lines whose absolute stamp and phc moved by a constant 5,120 ns of simulated time, residuals identical |
| 16 | make -j8 -O -C tb/verilator/milan_dp_render | rc 0 (877 s) | rc 0 (808 s) | records identical as sorted; the 90 → 91 programs line and build sizes |
| 17 | flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check (Vivado 2026.1 xvlog) | rc 0, 0 findings | rc 0, 0 findings | identical but for the line naming the processor pin (08ae0013 → c8261711) |

## Acceptance (issues #185 and #186 "Done when", assignment items 1-5)

| Item | Met | Where |
|---|---|---|
| #185: READ_DESCRIPTOR CONTROL returns the current value after every SET_CONTROL, as the four overlaid types of #82 do (IEEE 7.2.22, 7.3.6.2; Milan 5.3.12) | yes | E_RDESCCT and its re-dispatch; AX RDC0 to RDC6 byte-exact (reset 0, 255 after SET_CONTROL(255) and three refused, 0 after SET_CONTROL(0), either side of a power cycle); ucpu RC1, RC2 |
| #186: the notification a LOCK_ENTITY command drives echoes the command's flags, as the response does (IEEE 7.5.2, 7.4.2.1) | yes | the flags latch, the job's arguments, the r14 packing, E_LOCKUNS; L5b (UNLOCK, flags 1), LN1 and LN4 (reserved bits in both halves), aecp_notify LF1, LF1b, LF3; ucpu L3 |
| #186: the lock-timeout notification (Milan Table 5.22) keeps flags 0 | withdrawn by the correction; round 1b makes it UNLOCK | see Round 1b acceptance |
| Suite cases for each, each with a planted mutant that fails it | yes | 9 dispatch arms and 13 notify controls, all killed by their named checks (tables above) |
| docs/architecture/06_aecp_engine.md and the command records updated | yes | 06 §6.1, §6.8, F06.14, the opcode answers; `aecp_commands.json`; re-swept `decode.json`; compliance review rows 15, 16; 09; suite READMEs |
| Every processor gate at base and head, with the CI-pinned sv2v and Yosys | yes, all rc 0 | records above |
| Parent consumer gates on a scratch parent at dev e9cbb676, gitlink at the head, with the #180 and #176 parent patches | yes, all 17 rc 0 at base and head | table above |
| STOP on a register-map, top-level port or parameter change | none made; no STOP | `git diff 08ae001 HEAD -- hdl/common hdl/aecp/ucpu_pkg.sv` is empty; `hdl/top` gains one internal wire and two internal connections only |

PR-BODY.md therefore carries "Closes #185" and "Closes #186". The brief's "Closes #179" is
not used: #179 is SET_CONFIGURATION, already closed by another lane, and this assignment does
not touch it (Scope notes).

## Posting

Round 1: REVIEW READY was posted on processor issue #185 with the head (comment
6255090417), as the assignment ("Post REVIEW READY or STOP here") and the brief ask.
Round 1b: "[A647] REVIEW READY: branch 185-186-control-unlock, head
fcb6b5138e17b33a3c51572594a1aa210aa0bef1 (round 1b; three commits on main 08ae0013)."
was posted on #185 (comment 6257747212). TAKEN was not posted again. Nothing was posted
on #186 or elsewhere. No existing comment was edited.
Round 1c: "[A647] REVIEW READY: branch 185-186-control-unlock, head
f42c886c9abf311af64152eda669cbb040460bd1 (round 1c; main 246cbc22 merged in a2cf652)."
was posted on #185 (comment 6263866453). TAKEN was not posted again.

## Final state

- Lane: branch `185-186-control-unlock` at `f42c886c9abf311af64152eda669cbb040460bd1`.
  It is five commits on `08ae0013` plus the merge of main `246cbc22`: `198f1b1`,
  `c826171`, `fcb6b51`, the merge `a2cf652` and the README commit `f42c886`. The tree is
  clean (`git status --short --ignored` is empty after `git clean -fdX`). Nothing was
  pushed, nothing was rebased, and no PR exists.
- Scratch parent: dev `e9cbb676` plus the four local commits on the local branch
  `pp185-a647-r1c-scratch` (round 1c table), never pushed. HEAD is `fbc999ff6`, with the
  gitlink committed at `f42c886` and the submodule checked out there (detached). The
  working tree is clean. Rounds 1 and 1b used the same clone with the patches
  uncommitted, as their brief asked.
- All scratch work (records, scripts, backups, campaign outputs) is under the scratch root,
  outside both trees and outside this directory.

## Artifacts in this directory

- `HANDOFF.md`, `PR-BODY.md`.
- `receipts/r1c/` (round 1c): `base/gates` and `head/gates` (every processor gate at
  `246cbc22` and `a2cf652`, with `HEAD.txt`, the REQ-tag evidence and status),
  `base/campaigns` and `head/campaigns` (the 13 campaign summaries with rc and duration),
  `head-final/gates` (every gate at `f42c886`), `parent-base` and `parent-head` (the 17
  consumer gates, the parent's local commits, the committed gitlink, the submodule HEAD,
  the patch digests and their `apply --check -R`, and the parent status before and after),
  `compare` (the campaign table, sorted masked diffs, per-mutant failing-check sets base
  vs head and round-1b head vs round-1c head, the parent table and diffs, and head vs final
  head), `merge` (the lane log, the diff stats, the merge's combined diff, the conflicted
  files against each parent, the anchor check and the final status), `try` (the
  pre-commit aecp_notify run, make check and matrix on the merge), the streams' `.out`
  files and `scripts` (the scripts that ran them). Files over 200 KB (the parent
  pp_shadow and milan_dp logs, base and head, and the milan_dp diff) are listed in
  `OVER-200KB.sha256`.
- `receipts/`: the logs, rc and duration files of every gate and campaign summary, under
  `base`, `head` (`60da763`), `head-final` (`c826171`), `parent-base`, `parent-head`,
  `base-campaigns`, `head-campaigns`, `newarms` (the new arms on their own) and the per-commit
  checks `c185`, `c185b`, `c186`, `c186b`. Four logs over 200 KB are recorded by sha256 and
  size in `receipts/OVER-200KB.sha256`: pp_shadow and milan_dp, base and head. The per-mutant
  campaign logs stay in the scratch records.
- `receipts/r1b/` (round 1b): `head` (every processor gate at `fcb6b513`, with
  `HEAD.txt`, the REQ-tag evidence and `status-after.txt`), `head-campaigns` (the 13
  campaign summaries with rc and duration), `parent-head` (the 17 consumer gates, the
  gitlink, the submodule HEAD and the parent diff stat), `newarms` (the 16 lock controls
  on their own, with each control's log), `hand` (the hand-planted runs, their patches
  and the post-restore `git status`), `try` (the pre-commit suite runs and `make
  check`/lint/matrix), and `scripts` (the scripts that ran them). The two round-1b logs
  over 200 KB (parent pp_shadow and milan_dp) are listed in `OVER-200KB.sha256`.
- `receipts/INDEX.md`: generated from the files present by
  `receipts/r1c/scripts/receipts_index.py` (the round-1b script, unchanged), with each
  file's size and sha256: 897 files, 11 over 200 KB listed. Round 1b's index had 526
  files and 6 over 200 KB.
- `try/pp_top.log` is the second pre-commit pp_top run (rc 0). The first one failed RN
  (`6 of 2211 frame comparisons diverged`) because the model still predicted flags 0 on
  the automatic unlocks. That run led to the RN and TD1 updates, and its log was
  overwritten by the rerun.

## Tool identities

- Verilator 5.050 (`verilator --version`: "Verilator 5.050 2026-07-01 rev v5.050"), the pinned
  wrapper exported first on PATH. The host default, 5.052, was not used.
- sv2v 0.0.12 (`--numeric-version`), sha256 b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b.
- Yosys 0.33 (git sha1 2584903a060), CI's ubuntu apt build, sha256
  88c0a12bb814a1a8716b1ae10b482e35d3005ed558e1f5f626b3dc983ea3abd0, used for
  `syn/yosys/run.sh` and the elab-guard grading. The host Yosys 0.66 (sha256
  ec566d8f...b5b) was also run as a second record.
- Vivado 2026.1 xvlog, used only by the parent's `xvlog_gate.py`, under
  `flock $VIVADO_LOCK` (exclusive).
