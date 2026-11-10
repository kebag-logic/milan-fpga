# HANDOFF: [A753e] #823 round 5 (append-only save path + round 4 fixes)

Status: DONE (11:3x CET). REVIEW READY posted on #823: issuecomment-6764816430 (text REVIEW-READY.md), head
7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 (4 commits on 30ca4b21, not pushed; origin/dev-soft-core still 1d6bf555 at
posting). Receipts: receipts/ (SUMMARY.md, INDEX.md, 1,188 files). PR-BODY.md final. All my units have exited.
Open for the manager: the 8x8 two-interface ledger (59.5 vs 57.5 RAMB36) and #818's routed gate (needs Vivado).

- Lane: $LANES/823-name-cap, branch 823-nvm-format, start head 30ca4b21 (round 4, [A753d], pushed, PR #863)
- origin https://github.com/kebag-logic/milan-fpga.git (verified); origin/dev-soft-core 1d6bf555 (verified 01:15 CET)
- Authority: #823 issuecomment-6754858510 ([A10] round 5 ruling) on R805-4 (PR #863 issuecomment-6752573647)
  and R806-4 (issuecomment-6754770706). Reports read in full: 823-r805-4/REPORT.md, 823-r806-4/REPORT.md.
- Scratch: $VALIDATION_STORAGE/823-a753e. Output: this directory.
- Posting: the ruling says "post REVIEW READY on PR #863"; this session's assignment allows posting only
  TAKEN / REVIEW READY / STOP on issue #823, so REVIEW READY goes on #823.
- My unit: milan-823-a753e.service, CPUs 120-127, MemoryMax 20 GB. All 128 host CPUs were booked at 03:2x.

## Progress
- [x] TAKEN posted: issuecomment-6755119629 (text TAKEN.md), 01:2x CET
- [x] (1) append-only save path in the F1 store (code + tests + plants), see Design below
- [x] (1) 32x32 worst case: test_nvm_bound.cpp at 32x32/2if TDM8: 321.3 ms during the erase, 325.2 ms during
      a compaction (bound 500 ms); append 175.2 ms, twice 350.4 ms <= 500 ms (dev run, 1x1 suite run log run7.log)
- [x] (2) N1 SPLIT_CONTROL_MEMORY: c20ed894 run back to 3,344 against 13,264 bytes, a note pointing at section 5
- [x] (3) N2 QSPI_FLASHBOOT: who reads/writes each reserved range, per FASTCONNECT section 5; stale
      "nothing writes or reads them" and "blank-flash responder" sentences removed
- [x] (4) RS5, RS6 (FASTCONNECT contents + status row); RS-a (comments: nvm_klj2.c/h, nvm_shape.h,
      nvm_layout3.h, nvm_layout3.py, nvm_klj3.py x3, check_nvm_klj3.py, builder #: comment, test_builder
      docstring); RS-b (test_nvm_write.cpp rewritten; no nvm_klj2.py left there; nvm_rig.cpp/test_nvm_boot.cpp kept)
- [x] (5) SG3=S-a LINE_CITE_RE widened (range, list, unquoted, "line N", #L) + 4 plants; SG4=S-b at-width 255
      compile + off-by-one control; S-c #error unless NVM_HOST_SHAPE (bench header) + control
- [~] (6) area: #818 gate is Vivado (forbidden this round) -> not run. Split memory measured (mem/):
      fixture +5,280 B rom at every point; 1x1 37.5->39.0, 1x1if2 41.0->42.0, 8x8 51.0->52.5,
      8x8if2 (ledgered 57.5) -> 59.5 REFUSED by the ledger. Platform image not linked again. DECISION NEEDED.
- [x] commit b6a60fbdff92bf89552f1634e6890bd27d41b485 (one commit, one-line subject); origin/dev-soft-core
      still 1d6bf555 at 03:39 (fetched). Dev self-test (self3.log, working tree) stopped at 16/184 OK, no
      failure, in favour of the clean-clone run.
- [x] gates on a clean clone of the head (7c97e99f): 30 jobs, 152 steps rc 0, 198 not run with reasons (verify_wf rc 0);
      builder unions 107/107 (docs, elaborate); LiteX 8/8; ctrl_nvm self-test rc 0 (728 tests, 191 planted reddened);
      twin rc 0 (0 findings, 20 plants x2); drift gate, diff_check rc 0; sweep at b6a60fbd 65/65 (stands, SUMMARY.md)
- [x] REVIEW READY posted: issuecomment-6764816430 (11:3x CET)

## Design (for the PR body / REVIEW READY)
- Slot = base container at 0 + log of delta segments from NVM_LOG_START (page after the base); delta = KLJ3
  header + changed records (framed, ascending) + pad + CRC; <= NVM_SEG_PAGES 28 pages; seq strictly above.
- Save: capture (1 record/step) -> records whose staged bytes changed are in flight -> delta (cap: min(28 pages,
  room)) to the auth slot, page cycle assemble/seal/[suspend]/program/wait/verify. Failed delta after a program
  issued -> torn; nothing appends past torn.
- Compaction (force/console, torn, full, auth NONE + inflight, room < reserve = half log): base = stage at the
  auth slot's seq (first seq with no slot), page by page with a carry of the record a page cuts; each page yields
  to a save (appended to the old slot); after the base, the old log since copy_from copied page for page; move
  (auth = new, log_end mapped); over an old slot inflight stays (next delta ends the tie), with no old slot only
  records latched behind the front stay; old slot prepared.
- Background prep of the non-auth slot: read every page (256 B/step); a written page erases its block (once per
  prep), re-check; 3 failed preps -> FAILED until reset; erase timeout counts run time only.
- Erase suspend (PES 0x75/PER 0x7a, port calls suspend/resume): a delta's program during the erase suspends,
  times it (suspend_us_max; suspend_slow > NVM_SUSPEND_ROOM_US 95290), programs, verifies, resumes. A suspend not
  seen by the deadline -> resumed once the device answers. After a failed program, nothing until busy()==0.
- Deadline NVM_APPEND_TIMEOUT_MS 500 from due to read back (VD_ERASE in suspend wait, else VD_PROGRAM).
- Window NVM_WINDOW_MS 150 (decision 4) for this store; DR2c backoff 1000 ms kept.
- Boot: base judged as before; log walked (agreement of two walks, as a refusal); slot seq = last closing
  delta's; restage = base re-judged + replay to the judged end (limit), seq must match.
- Stage stays the whole container (+ page 256 B + carry); the proposal row's "one page and one record" stage
  alone is not built (would need compaction streaming from the owners).

## Gates on b6a60fbd (from 03:40)
- 03:4x found: round 3's SDK home $VALIDATION_STORAGE/823-a753c/gates/home is GONE (only its venv left). With HOME
  there the RV32 arm silently fell back to /usr/bin/riscv64-elf-gcc 16.2 (fw_rv32.CANDIDATES). Fix: the pinned
  SDK installed offline from $VALIDATION_TOOLS/bootlin-504-probe/<release>.tar.xz (digest checked) into
  $VALIDATION_STORAGE/823-a753e/gates<home-path>/host, verified ("SDK fresh installation: verified");
  run_wf.py and extra_gate.sh HOME repointed there. Runs made with the wrong compiler moved to
  gates/superseded-system-cc (self-test aborted, memory runs).
- Extras rc 0: diff_check, drift_gate (0 findings, self-test PASS). mem_head/mem_base (SDK) rc 0 / ledger refusal
  at 8x8if2 head only: figures identical to the doc's table (base reproduces the 57.5 ledger).
- Unit milan-823-a753e-ctrlnvm (120-127): test_ctrl_nvm.py --require-rv32 --self-test --jobs 8, relaunched 03:47.
- Waiter milan-823-a753e-waiter (tools/waiter4.py, waiter.log): holds four 4-CPU ranges for the sweep
  (native-shards.py label 823-a753e-sweep, out $VALIDATION_STORAGE/823-a753e/sweep), then drivers A (r4-a), B (r4-b)
  on 4 CPUs, C (r4-c) and twin on 8. Gate root $VALIDATION_STORAGE/823-a753e/gates/final. rtl-fast aggregate after.

- 03:49 sweep shards on 92-95, 20-23, 16-19 (shard 2), 84-87; every preflight PASS on all 4 shards (suite
  cancellation incl.). Driver A on 80-83 (03:49), driver B on 28-31 (03:59).
- 04:06 firmware-unit done, 0 bad: store gate "OK across 5 shape(s), 728 tests"; save bound 321274 us (erase) /
  325187 us (compaction), append 175187 us, twice 350374 us; coverage ratchet PASS (ctrl_nvm incl.).
- Drafts: REVIEW-READY.md (VALIDATION/ACCEPTANCE placeholders), PR-BODY.md (STATUS_BLOCK/HEAD_SHA/PLANTED).
  Receipts: tools/assemble.sh (round 5), placeholders.tsv in scratch.

- 04:25 FIRST-RUN FAILURE on b6a60fbd: firmware-boundary ci_step_9 (ctrl_boundary.py) rc 2: "REFUSED:
  scripts/check_nvm_format_32x32.py names the firmware's tree and is a program, and is neither a known builder ...
  (OUTSIDE)". Cause: the page gate now reads the store's constants (STORE_CONSTANTS). Fix commit
  d01c66ad8ab62f2c69cac504a9fcdb76d45fc173: ctrl_configs.OUTSIDE entry (compiles nothing). Census re-run in the
  working tree: no unregistered builder program left. test_ctrl_memory.py (LiteX venv) rc 0 on the working tree.
- 04:3x restart on d01c66ad: drivers A (80-83), B (28-31) relaunched on the same ranges (held by keep-* units across
  the switch), root gates/final fresh; waiter5.py books 8 CPUs for driver C; unit milan-823-a753e-mine (120-127):
  twin + twin-plants, then the ctrl_nvm self-test. Extras on d01c66ad rc 0: diff_check, drift_gate (0 findings,
  self-test PASS), mem_head (same figures). b6a60fbd outputs kept in gates/superseded-b6a60fbd.
- The sweep keeps running on b6a60fbd: b6a60fbd..d01c66ad is one dict entry in sw/firmware/ctrl/test/ctrl_configs.py,
  which no sweep suite reads (grep of tb/verilator Makefiles/.py/.sh: no ctrl_configs reader). State it in REVIEW READY.

- d01c66ad results so far: firmware-unit 0 bad (728 tests; same bound figures); twin rc 0 ("twin: 0 finding(s)",
  twin-plants rc 0, 40 refusal lines as round 4); sweep shard 3 (b6a60fbd) 16/16 PASS, 21,575 checks.
- 05:04 driver C on 84-91 by hand (8 contiguous free CPUs; waiter5 only took aligned ranges, stopped).

- 05:22 SWEEP DONE (b6a60fbd): 4 shards exit 0; 15+17+17+16 = 65/65 suites PASS, 0 timed out, 2,192,899 checks,
  0 in-suite failures; capture_coherence PASS (shard 2, 4 CPUs); every preflight PASS (no #833 symptom).
- firmware-boundary on d01c66ad: ci_step_9 rc 0 ("ctrl_boundary: PASS").

- SECOND-RUN FAILURES on d01c66ad (05:45-05:55):
  - firmware-control-mutants ci_step_9 rc 1: "mutants: 569 of 570 caught"; [ESCAPED]
    acmp-nvm-bindings-latched-by-the-others: 9 checks failed, none the named "N1 the binding parameters come back"
    (test_acmp_nvm.cpp N1 stopped at ASSERT "N1 the store commits it": the store finds nothing changed when the
    owner refuses the latch, and DR2b writes nothing). Fix: that check EXPECT, so the restore checks run.
  - ctrl_nvm self-test rc 1: 12 plants NOT caught (180 of 192 OK lines). Diagnosed with tools/grade_some.py
    (logs kept per plant): cases that broke a second rule (magic kept the old crc16; pad refused by CRC; cap
    refused by the pad rule at 1x1; room refused by magic), timings that missed the plant (carry, DR2b heal,
    attempts across moves, read during an over-deadline erase), a missing check (copied delta in the new slot), a
    power-cut sweep that hung on an unbounded wait (timeout = no named FAIL).
  - Fixes: commit a9c6391f (tests/fixture/rig; delta_count_unbounded and delta_overrun_unchecked dropped as
    verdict-equivalent, the README says why; delta_cap_unchecked graded at 8x8) and 7c97e99f (missing delta
    crc16 case + plant delta_crc16_unchecked). Grader: all 10 kept plants + the 4 delta record plants caught;
    suite 1x1/8x8 rc 0 (302 tests).
- Other d01c66ad results rc 0 (superseded, kept in gates/superseded-d01c66ad): firmware-unit, boundary, verilator,
  aecp/srp mutants, every docs and rtl-fast job, elaborate, rtl yosys; twin; docs builder union (107 gates).
- Sweep stays b6a60fbd: b6a60fbd..7c97e99f touches ctrl_configs.py, test_acmp_nvm.cpp, the ctrl_nvm README and
  test/ files; no tb/ suite reads any (grep; ctrl_service_budget not in the sweep; ctrl_srp_image's imports do not
  load ctrl_configs/nvm_fixture/nvm_mutants).
- 06:5x final run on 7c97e99f: waiter6.py (A, B: 4 CPUs; C: 8, or 4 after 15 min); unit mine (120-127): diff_check,
  drift_gate, mem_head, ctrl_nvm self-test, twin.

## Resume after the 07:49 host power-off (session [A753e] resumed 09:44 CET)
- Tree clean at 7c97e99f (4 commits on 30ca4b21, not pushed). origin/dev-soft-core still 1d6bf555 (fetched 09:5x).
  #823: TAKEN posted once (issuecomment-6755119629); no REVIEW READY yet.
- Done on 7c97e99f before the cut, all rc 0: diff_check, drift_gate, mem_head (8x8if2 ledger refusal, as expected),
  firmware-unit, firmware-boundary, firmware-verilator, docs wire-accountability, docs-check-no-git, docs-gates-0,
  elaborate-gates-0.
- Cut mid-job (partial logs moved to gates/interrupted-0749, never counted): firmware-control-mutants (after
  ci_step_8), docs-gates-1 (after ci_step_13), elaborate-gates-1 (after ci_step_23), ctrl_nvm self-test (header only).
- 09:5x relaunched on fresh clean clones of 7c97e99f (holders first, then units):
  gates-a 8-11 (tools/r5-a.txt: control/aecp/srp mutants, rtl-fast yosys-tool, yosys-elaboration, split-cdc),
  gates-b 12-15 (r5-b.txt: docs-gates-1, docs-gates-2, docs-check, changes, verilator-lint, bdd-conformance,
  publication-census, rtl-fast aggregate), gates-c 72-79 (r5-c.txt: elaborate-gates-1, elaborate, rtl full-ci-gate,
  yosys-tool, yosys-shards 0-3/4, yosys-portability), mine 64-71 (ctrl_nvm self-test --jobs 8, then twin+twin-plants).
  Logs: drive-{a,b,c}5.log in scratch; outputs in gates/final and gates/run/logs.
- Results: drivers C 10:45, B 11:02, A 11:05 list done, every job "failed 0"; control mutants 570/570; self-test rc 0
  11:03; twin rc 0 11:16. Builder unions run by hand (scripts/ci_builder_legs.py union, tree ffccc6f5) into
  gates/final/union, both rc 0. not_run.json's rtl/verilator-shards/* reason now names the sweep head.
  assemble.sh gained the interrupted-poweroff section; receipts/extra/twin-excerpt.txt written after it, index rerun.

## Notes
- 02:15 implementation first green at 1x1; 5 shapes 671 -> 728 tests after coverage tests.
- Coverage: nvm_store.c/nvm_klj2.c/litespi: every line and arc covered except the existing exclusion rows
  (nvm_framed_as, nvm_idle due arc, nvm_shape_consistent, ls_in_journal); the stale nvm_erase_start row removed
  from sw/firmware/gtest/README.md. Ratchet file not rewritten (fractions stay 1).
- Ledger conflict: see (6). No CI gate plans the linked image (ctrl_runs image runs stop at link).
- First self-test run killed (my nvm_shape.h edit landed mid-run; then tmpfs growth ~100 MB/mutant toward the
  20 GB cap). Fix: plant_and_grade now removes each mutant's work dir. Gate runs use TMPDIR on /data.
- Residue found, not changed (not in the ruling's list): nvm_rig.hpp:18 and nvm_suite.hpp:9 say the fixture
  comes from scripts/nvm_klj2.py (it is nvm_klj3.py).
- Gate tools copied to $VALIDATION_STORAGE/823-a753e/gates/tools (paths repointed); venv symlink to round 3's.
