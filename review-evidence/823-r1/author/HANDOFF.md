# HANDOFF: [A753c] #823 round 3 (split record space and framing)

Status: DONE. REVIEW READY posted 2026-11-09 as issuecomment-6739484939, at f3e902f2.

- Lane: $LANES/823-name-cap, branch 823-nvm-format
- Start head: 61eec0c360 (round 1, [A753]); base origin/dev-soft-core a9d69c77 (verified)
- origin https://github.com/kebag-logic/milan-fpga.git (verified)
- Authority: #823 issuecomment-6730985093 ([A10] round 3 ruling), scoping decisions 1, 2, 6
  of issuecomment-6730773797 to the split placement.
- Scratch: $VALIDATION_STORAGE/823-a753c

## Progress
- [x] TAKEN posted (issuecomment-6731087521)
- [x] context read (design page, census, F1 store, builder split output, Python reference)
- [x] implementation (4 commits on 61eec0c3, head f3e902f2)
- [x] gates (all final rc 0; receipts/SUMMARY.md, receipts/gates/verify.md)
- [x] REVIEW READY posted (issuecomment-6739484939)

## TAKEN
- Posted issuecomment-6731087521 (text: TAKEN.md), 2026-11-09 ~04:00 CET.

## Plan (decided 04:05)
1. Declaration: sw/firmware/ctrl_nvm/nvm_layout3.h (NVM3_CAP_* per block, bases chained);
   reader scripts/nvm_layout3.py (exactly one decimal line per cap, path:line).
2. Python reference scripts/nvm_klj3.py: 10-byte layout-3 frame, KLJ3 container, decode
   (KLJ2 magic -> VD_VER), inventory3, split constants MILAN_NVM3_* (32 ports), stage bytes.
3. Flash map: FLASHBOOT_RESERVED gains journal_klj3 0xE4_0000 + 0xA_0000 (640 KiB, two
   320 KiB slots). Today's journal untouched; the split store reads its two headers only.
4. Builder: nvm_split_capacity() + emit_nvm_split(overlay) -> <stem>/nvm_split.json, refusal
   over any block citing the declaration line. New gate (split record space) + controls;
   gate 38 (all-fabric 128 names) unchanged.
5. F1 C: nvm_shape.h/nvm_klj2.[ch] (file names kept) -> KLJ3/layout 3; nvm_store.c: open
   bits with counts (decision 6), legacy KLJ2 headers read at boot -> st.legacy + VD_VER,
   erase every block the container spans; LiteSPI guard -> KLJ3 journal; fmodel protect
   span + alias across slots.
6. Tests: fixture/bench on KLJ3; KLJ2 at boot (legacy region and in-slot); NAME first/last/
   one past at a doctored at-capacity build (907 names) + compile refusal at 908; mutants.
7. VERSION: format chain (KLJ3 major 3, layout 3, KLJ2 recognised -> VD_VER). Gateware
   VERSION CSR NOT bumped: conflict with all-fabric-unchanged and ARCHITECTURE_HW_SW_SPLIT
   section 7 -> publish as an open question in REVIEW READY.
8. Docs: SAVED_STATE_FORMAT_32X32.md (split's format; all-fabric keeps KLJ2; A3 typical
   15 us, margin), ctrl_nvm README, split target README; drift gate green.

## Progress (05:00)
- Implemented (uncommitted yet): declaration + reader, KLJ3 reference + its gate (6 plants), journal_klj3
  in FLASHBOOT_RESERVED, builder emit_nvm_split + gate 39 (10 plants), F1 codec/store/port/model/rig/
  fixture/tests (capacity binary, KLJ2 tests, open_count), mutants re-anchored + 13 new, over-capacity
  compile control, split target harness (self-test 73/73), gen_flash_port (37/37), RV32 self-test (17),
  split SoC constants (milan_soc.py), ctrl_memory stage + LEDGERED 13,594, boundary OUTSIDE entries,
  docs (format page regenerated: 0 findings, 10/10 plants; split target README; memory page delta).
- Measured split memory (receipts/split-memory): +704..712 B rom, +352..576 B sram; tiles 37.5/41.0/
  51.0/57.5 (ledgered fits, 296 B rom left before 58.0). Base clone: $VALIDATION_STORAGE/823-a753c/base-wt.
- F1 suite: OK across 5 shapes (464 tests before the last tests were added). Self-test running in
  background (log $VALIDATION_STORAGE/823-a753c/st1.log).
- TODO: self-test result; coverage ratchet + exclusions (nvm_framed_as arcs); README sizes/counts;
  commit; clean-clone gates; REVIEW READY.
- Decision taken and to publish: gateware VERSION NOT bumped (open question).

## Committed (05:30)
- Head c1c9049bea70029756b84042f4bfd097092a2840 (3 commits on 61eec0c3):
  1076449a declaration + builder split output + gate 39; 755f8393 split store KLJ3 + reference + link;
  c1c9049b docs + page gate.
- Pre-commit on the working tree: F1 suite 5 shapes OK (474 tests); self-test 123/123 (before the
  legacy-check rewrite; rerun on the clean clone); coverage ratchet recorded (100% after exclusions);
  gate 39 + 38 pass; check_nvm_klj3 6/6; page gate 0 findings, 10/10 plants; idiom/docs gates pass;
  test_ctrl_memory PASS (LiteX venv); split target self-test 73/73; gen_flash_port 37/37; RV32 17.
- Gate tools: receipts/gates/tools/run_wf.py, verify_wf.py, not_run.json (137 entries).

## Dry run on c1c9049b (05:27-07:30), superseded
- Found: Python idiom gate (2 undocumented nested helpers, 1 long line in the new KLJ3 modules; the lane
  run had them untracked) -> fixed in f3e902f2. Runner gaps (GITHUB_PATH, working-directory) fixed in
  run_wf.py. Everything else that ran passed: firmware-unit (coverage PASS), firmware-boundary PASS,
  firmware-verilator boundary PASS, builder legs 0 and 1 (EXCEPT 1 / 16 NOT RUN), elaborate legs 0 and 1
  (EXCEPT 1 NOT RUN each), docs-gates-0 all but the idiom gate, docs-gates-2, wire, no-git, changes.
- The dry-run sweep (stopped at about half, on purpose) showed no failure.
- Background commands die at 2 h: the final runs are systemd user units instead.

## Final runs on f3e902f2a96bb27eac6ed7780c70905af34f389e (from 07:31)
- Sweep: units milan-823-a753c-shard0..3 (CPUs 96-97/98-99/100-101/102-103: no free range from
  cpu_ranges.py pick, busy 124-128 of 128; MemAvailable 30.8 GB at launch), out $VALIDATION_STORAGE/823-a753c/sweep-final
- Drivers: milan-823-a753c-gates-a/b/c (lists receipts/gates/tools/final-*.txt), root
  $VALIDATION_STORAGE/823-a753c/gates/final; logs $VALIDATION_STORAGE/823-a753c/final-drive-*.log
- Self-test: milan-823-a753c-gates-selftest -> gates/run/logs/extra.ctrl_nvm_selftest_final.*
- Verify: python3 receipts/gates/tools/verify_wf.py f3e902f2... $VALIDATION_STORAGE/823-a753c/gates/final rtl/yosys-shards=4

## Host reboot 10:34; resumed 11:36 (lane at f3e902f2, tree clean)
State of the final runs at the reboot (read from $VALIDATION_STORAGE/823-a753c):
- Drivers: everything in final-c and final-b ran, all rc 0, except: elaborate-gates-1 gate_19 (LiteX aggregate)
  exit 92 = 2 simulations TIMEOUT under contention (test_retained_cdc_storage, test_soc_timing_cuts), 6 PASS;
  full-ci-gate target rc 1 at first run, re-run rc 0 (first run kept as *.first-run.*); publication-census killed
  at step 12; firmware-control-mutants killed at step 9; aecp/srp mutants and the rtl-fast aggregate not started.
- Self-test (test_ctrl_nvm.py --require-rv32 --self-test) on the clean clone: rc 0.
- Sweep (4 shards, 2 CPUs each beside the drivers): 0 failures, 11 suites TIMEOUT (unknown): milan_dp,
  milan_dp_gm_steps, milan_dp_mclk, aaf_clock_meter, capture_coherence, gptp_plane, maap, follow_ring,
  media_phase, mmcm_servo, reboot_ctrl. Reruns started 10:13-10:27 were killed by the reboot (kept in rerun/).
Plan: re-run the 11 suites uncontended on picked CPU ranges (rerun_suites.sh via extra_gate.sh, fresh clones);
re-run gate_19 alone; run the three mutant jobs, the census and the aggregate fresh; then verify, receipts, post.

## Re-runs after the reboot (11:39-, all on fresh clean clones of f3e902f2)
- Units milan-823-a753c-rr1..4 (CPUs 40-43, 44-47, 72-75, 76-79 from cpu_ranges.py pick; capture_coherence on 4),
  out $VALIDATION_STORAGE/823-a753c/rerun2/rrN, rc in gates/run/logs/extra.rrN.rc. Results so far: milan_dp,
  milan_dp_mclk, capture_coherence, aaf_clock_meter, gptp_plane, follow_ring, media_phase, mmcm_servo rc 0.
- Units gx (56-59) and gy (60-63): control/aecp/srp mutants, publication census, rtl-fast aggregate, all rc 0;
  elaborate-gates-1 gate_19 re-run alone, 8/8 LiteX simulations PASS, rc 0 (first run kept as *.first-run.*).
- verify_wf.py: 149 steps ran, 193 not run with a reason, 0 bad (rc 0).
- Receipts: receipts/gates/tools/assemble.sh (collect, verify table, INDEX.md).

## Final (13:3x)
- All 11 re-run suites rc 0 (rr1..rr4 rc 0, trees clean): table in receipts/SUMMARY.md.
- verify_wf.py: 149 ran, 193 not run with a reason, 0 bad. Receipts assembled (assemble.sh), INDEX.md regenerated.
- Corrected a figure from the earlier draft: the page gate has 9 plants plus a clean-tree control (not 10 plants).
- REVIEW-READY.md (text posted) and PR-BODY.md (status filled) written. Gateware VERSION left as an open question.
- No push, no PR, no merge/rebase/force/amend. Lane tree clean at f3e902f2.
- Posted REVIEW READY: issuecomment-6739484939 (text: REVIEW-READY.md). Round complete; stopping.
