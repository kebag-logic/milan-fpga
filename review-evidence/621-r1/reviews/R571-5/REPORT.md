[R571] POSITIVE - exact head 2cf985f3206dd519d80142fd2479afe24c3051f6

# R571-5: external review of PR #707 (issue #621)

- Exact head `2cf985f3206dd519d80142fd2479afe24c3051f6`, tree `cee526a44c9ecce9e5728cfec19d67828f22fdb0`.
- Source base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. The diff is 14 parent commits and 40 files, plus the `gptp-processor` gitlink `5dce647a` -> `7dda9c3b`.
- Clean, cleared-context external review. All five lenses were applied to the whole diff from the base, not only to the round-4 delta.

**Verdict basis.**
- No BLOCKER, MAJOR or MINOR is open at this head.
- This round adds one RESIDUE (R571-5-RES-1, the PR body's Status wording) and one SUGGESTION (R571-5-S1). Neither affects a lens.
- Every prior finding is resolved at this head (section 4), and every prior SUGGESTION is carried.
- All five lenses are CLEAN at this exact head.

## 1. Scope reconstructed from public state

Sources, in order: AGENTS.md, CONTRIBUTING.md, docs/README.md, then issue #621. The issue sources are its body, the assignment (comment 6084306147) and its donor correction (6084315762), and the rulings 6087415319, 6087498843, 6087655217, 6088189432 and the final 6089776382, which replaces the earlier receipt invariants. Then the runtime round (6101380300) and round 4 (6103886503).

- **Item 1.** Reproduce in simulation a +/-10 ms grandmaster-driven PHC step on a port that holds asCapable, show the 2 s loss, and find its cause. Cite 802.1AS-2020 11.2.2, 11.2.19 and 11.2.20.
- **Item 2.** Make a PHC step keep asCapable and a valid link delay, with a test that a planted defect fails. Here the fix is in the donor microcode, pinned by a parent gitlink.
- **Item 3 (effects).** Media is unaffected, and `tu`, GPTP_GM_CHANGED and CLOCK_DOMAIN are checked in simulation. Every suite and campaign that builds a changed file is run. The physical five-step repeat belongs to a later bench lane and is not part of this PR.
- **Rulings.** The capture-harness grading fix applies the production bound to `mutation none` arms only. The receipt refresh must keep the candidate's capture logs byte-identical to the base's, and must record that the old receipt was already stale at the base.
- **Runtime round.** `milan_dp` must finish within 60% of its 4800 s budget, with no coverage removed, no RTL or donor change, and no graded expectation changed. The GM-step leg moves to its own suite, which runs on every PR.
- **Round 4.** The runner tests describe the split recipe. The `dynmap` leg joins `LEGACY_LEGS`.

## 2. New findings at this head

### R571-5-RES-1 - RESIDUE - lens: Docs (wording only)

- **Artifact:** PR #707 body, Status section, line 17 (the live body as read during this review): "The round 4 head `2cf985f3` is local and unpushed."
- **Evidence:** the PR's `headRefOid` is `2cf985f3206dd519d80142fd2479afe24c3051f6`, and hosted contexts ran at that SHA (`receipts/hosted_checks_snapshot1.tsv`). The head is pushed.
- **Impact:** one stale status sentence. It changes no measurement, figure, verdict, test, code, generated artifact or clause claim.
- **Exact fix:** replace line 17 with "The round 4 head `2cf985f3` is pushed; hosted results at it are the manager's to confirm."
- **Verification:** read the live PR body.

### R571-5-S1 - SUGGESTION - lenses: Tests, Robustness

- **Artifacts:**
  - `tb/verilator/gptp_plane/sim_phc_step.cpp:187-188`: the peer LocalClock runs at exactly the DUT's true rate.
  - `sim_phc_step.cpp:124-127`: the delay tolerance is +/-125 ns.
  - Donor `docs/INTEGRATION.md`, "Peer delay across a phase step": "It retains the last valid ratio and link delay".
- **Relation:** R570-1-S1 raised this. That round could not place the plant, because SERVO has no free ROM word. This round executed it.
- **Evidence (executed):**
  - **The plant.** `zero-nrr-at-step` (`receipts/probe_generator_zero-nrr-at-step.py.diff`): a re-seeded rate window, which a step forces, also discards the retained ratio. Room was made by removing two paths that no step arm uses. That removal alone passes 62/0 on both harnesses as a positive control (`room-control`).
  - **Shipped harness:** the plant passes 62/0 (`receipts/probeE_shipped_zeronrr.log`). The regression cannot observe a lost ratio.
  - **Peer LocalClock at +400 ppm** (`receipts/probe_peer_ppm_harness.diff`): the same plant fails `no invalid link-delay publication` in 6 arms (`receipts/probeD_ppm400_zeronrr.log`).
  - **Head donor, same harness:** passes 62/0 at +100 ppm and at +400 ppm (`receipts/probeA_ppm100_head.log`, `probeB_ppm400_head.log`). The shipped behaviour is correct under a rate offset.
- **Why SUGGESTION:**
  - The code is correct, and the acceptance's failing arms exist.
  - A lost ratio would cost about (rate offset x turnaround / 2) for one interval. That is about 80 ns at 200 ppm and 800 us, so asCapable would hold in the modelled range.
- **Option:** give the step regression's peer a nonzero rate offset, with a turnaround or tolerance at which a lost ratio exceeds the tolerance, and plant the loss.

## 3. Lens results at this head

```text
[R571] PASS Conformance — gptp-processor hdl/ucode/gen_gptp_ucode.py:834-838,1298,1472-1497,1727-1738,1807-1829,1850-1880 (7dda9c3b); tb/verilator/gptp_plane/sim_phc_step.cpp:59-78,261-389; tb/verilator/milan_dp/sim_gmstep.cpp:952-1008; receipts/phc_step_basegen.log, phc_step_head.log, probeI_milandp_basegm.log, gm_steps_suite.log — the base donor reproduces the bench loss in both new tests; the head holds asCapable, a valid delay and single tu/GM_CHANGED/CLOCK_DOMAIN events, checked against issue #621 items 1-3, the assignment and the 802.1AS-2020 clause responsibilities the issue cites
[R571] PASS RTL — git diff 5603c353..2cf985f3 over hdl/, configs/, sw/ (empty); donor diff 5dce647a..7dda9c3b (hdl/ucode/gen_gptp_ucode.py and generated hex only); syn/yosys/rom_digests.tsv (+1 row); tb/verilator/gptp_plane/gptp_plane_wrap.sv:37,113; receipts/rom_fit_sweep.log — no RTL changes. Scratch cell 44 was unused. The ROM fits at 1016/1024 words in all 32 clock/option variants. The new digest row reproduces from the generator. The wrapper parameter defaults to the previous increment
[R571] PASS Robustness — sim_phc_step.cpp:70-76,315-389; gen_gptp_ucode.py:1286-1300,1397-1455,1756-1806; receipts/probeA_ppm100_head.log, probeB_ppm400_head.log, probeF_shipped_nopdstep.log; scripts/check_nvm_capture.py:55-62,131-159; tb/verilator/nvm_capture_cpu/run.py:78-79,116-126; receipts/check_nvm_capture*.log — covers steps across every exchange phase, real excessive delay, peer silence, answered and unanswered crossings, and 100/400 ppm peer offsets. The flag is cleared on every path that sends a request. The cease gate precedes the epoch leg. The capture gate fails closed
[R571] PASS Tests — receipts/phc_step_head.log (62/0, campaign 8/8), gm_steps_suite.log (190/0, 5/5 controls), gmstep_mutants_all_slice0-4.log (20/20 controls on the whole leg), gptp_plane_run.log (29/0), donor_engine.log (1613/0 plus 34/34 mutants), test_sim_pool_head.log (17/17), test_sim_pool_plant_gmstep_prereq.log (rc 1), phc_step_basegen.log (14 failures), probeI_milandp_basegm.log (40 failures) — every new test fails for the defect it targets, and every existing regression run is green
[R571] PASS Docs — docs/design/GPTP_PLANE.md:97-165; GM_LOSS_RECOVERY.md:230-239,275; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1711,1813-1817; docs/testing/TESTING.md:278,388-391,599; CI_WORKFLOWS.md:284-305; tb/verilator/README.md:62,64; tb/verilator/milan_dp/README.md:81,900-936,1384-1386; tb/verilator/milan_dp_gm_steps/README.md; donor docs/INTEGRATION.md; receipts/static_gates.log — every figure and count matches the receipt, campaign output or shard rule; 13 static gates exit 0. The only Docs item is RESIDUE R571-5-RES-1 (PR body)
```

### Conformance evidence

- **Mechanism, reproduced independently.**
  - I ran the head's step regression with the base donor generator (`5dce647a`) substituted (`receipts/phc_step_basegen.log`).
  - Every step arm loses asCapable for 2.000 s.
  - The forward and backward steps publish -3466 ns and +4545 ns, 0.10 s after the step. The bench saw 0 ns and 4,039 to 4,701 ns, and losses of 2.0 s.
  - Cause: the rate window that spans the step gives a neighbour rate ratio that is off by about 1%. The next delay is out of range, the ladder resets, and requalifying takes two clean exchanges at 1 s intervals.
- **Integration reproduction.**
  - I ran the head's `milan_dp` gmstep binary, all 190 checks, against a gPTP ROM generated from the base donor (`receipts/probeI_milandp_basegm.log`).
  - It fails 40 checks.
  - In the #621 phase, asCapable is lost for up to 6.0 M cycles. `tu` gives 2 or 3 episodes instead of 1, GPTP_GM_CHANGED gives 2 to 4 instead of 1, and CLOCK_DOMAIN gives 3 lock/unlock pairs instead of 1. These are the bench's effects.
- **Fix logic** (donor `gen_gptp_ucode.py`).
  - **Servo step (`:834-838`).** It clears `S_NR3`, which re-seeds the rate window and keeps `S_NRR`, and it sets `S_PDSTEP`.
  - **Request beat (`:1298`).** Each beat clears `S_PDSTEP` before the request is queued. Lost-response accounting (`:1472-1497`) is unchanged.
  - **Completion.** A complete exchange enters PDEPOCH (`:1727-1738`) after the pairing and cease gates.
    - A crossing exchange only marks `S_PDGOT`, for liveness. It publishes no delay, does not move the ladder and saves no rate window.
    - A clean exchange proceeds to PDPAIR unchanged.
  - **Clause reading.** The fix matches the responsibilities of the clauses the issue cites:
    - 11.2.2, capability from peer delay;
    - 11.2.19.3.3, rate ratio from successive t3/t4;
    - 11.2.19.3.4, delay from consistent differences;
    - 11.2.20, the responder's timestamps.
  - **Lost responses.** An answered crossing resets the lost count, so asCapable falls at the fourth unanswered request after it. An unanswered crossing earns no credit, so asCapable falls at the third. The prior rounds' SUGGESTION about this threshold reading stays carried.
- **Item 3 (effects).**
  - At the head, the #621 phase holds asCapable and a valid delay in every cycle.
  - Each step gives one `tu` episode and one GPTP_GM_CHANGED.
  - CLOCK_DOMAIN gives 1/1 at INTERNAL and 0/0 under CRF. The CRF servo is unlocked in this model, as documented.
  - `mr` and MEDIA_RESET do not change (`receipts/gm_steps_suite.log`).
- **Closure.** Item 3's physical repeat is not claimed. `closingIssuesReferences` is `[]`, and the body says "Relates to #621", so merging does not close #621.

### RTL evidence

- The parent `hdl/`, `configs/` and `sw/` diff is empty. The donor change is microcode only.
- **Microcode changes.**
  - One scratch cell, 44, which was previously unassigned. No numeric-index use of it exists.
  - One packed leg, PDEPOCH.
  - 3 more words in SERVO and 1 more in the timer program.
  - `S_NR4` is dropped from the boot-clear list. It is read only behind a nonzero `S_NR3` (`:1807-1829`).
- **ROM.** The ROM is 1016/1024 words; the base used 1008. All 32 variants generate (8 clocks, with the cease and seed options; `receipts/rom_fit_sweep.log`).
- **Digests.** The shipping image hashes to `a435fba6...`, equal to the new `rom_digests.tsv` row. The donor's checked-in `syn/ooc/work`, `tb/verilator/ucpu` and `tb/tsngen` hex files regenerate byte-identically.
- **Test wrapper.** `PHC_INCR_P` defaults to `32'h0800_0000`, the previous constant.

### Robustness evidence

- **Step positions.** Steps cross every exchange phase: t1 before the step, the response before the step, and a deferred t1 after it (`sim_phc_step.cpp:70-73`).
- **Real failures still fail.**
  - Real excessive delay and peer silence still clear asCapable (`:315-325`).
  - Answered and unanswered crossings under silence fall at the 4th and 3rd loss (`:358-389`).
  - A servo that never sets the step flag (`no-pdstep-set`) fails 10 checks (`receipts/probeF_shipped_nopdstep.log`).
- **Rate offset.** With a peer LocalClock at +100 ppm and at +400 ppm, the head passes 62/0.
- **Paths checked by reading.**
  - The cease `quiet` and credit `beat_off` paths end without sending a request, so a stale flag is never read for a fresh exchange.
  - The cease gate (`:1797-1806`) precedes PDEPOCH.
  - Warm reset clears the `S_T1V`/`S_PDWAIT` validity, so a response to a pre-reset request cannot complete.
- **Capture gate.**
  - `check_nvm_capture.py` exits 0.
  - Its `bytes`, `records`, `clock`, `ignore-off-timing` and `receipt-opt-out` mutations each exit 1.
  - `run.byte_only_controls()` passes, including the accepted 25 ms byte-only fixture and the production fixture that must be rejected.
  - A spec without a `mutation` key gets the production bound.

### Tests evidence

- **Toolchain.** All runs used Verilator 5.050 through the scoped wrapper, which reports "Verilator 5.050 2026-07-01 rev v5.050".
- **Exact bytes.** All runs used exact-head bytes: the run trees have no tracked modification (`receipts/clone_integrity.txt`).

| Run | Result | Receipt |
|---|---|---|
| `phc_step.py --mutants` | clean 62/0; cease-only positive control passes; 6/6 defects rejected by name; 8/8 | `phc_step_head.log` |
| `make -C tb/verilator/milan_dp_gm_steps` | leg 190/0; positive control (`--no-small-steps`) passes; 5/5 controls caught; rc 0; 627 s wall on a shared, loaded host | `gm_steps_suite.log` |
| `gmstep_mutants.py --all` (whole leg) | 20/20 controls caught; both positive controls pass. Five round-robin slices of the unmodified driver ran together, so every control ran exactly once (`scripts/gmstep_mutants_slice.py`) | `gmstep_mutants_all_slice0-4.log` |
| `make -C tb/verilator/gptp_plane run` | 29/0 | `gptp_plane_run.log` |
| donor `gptp-processor/tb/verilator/engine` (`make`) | `run` 1613/0; `mutants` 34/34 | `donor_engine.log` |
| `test_sim_pool.py` | 17/17. With `gmstep` put back into `run`'s prerequisites, the named arm fails (rc 1) | `test_sim_pool_head.log`, `test_sim_pool_plant_gmstep_prereq.log` |
| base donor ROM in both new tests | step regression: 14 failures; integration leg: 40 failures | `phc_step_basegen.log`, `probeI_milandp_basegm.log` |
| `suite_shards.py --selftest` | PASS. The `milan_dp_gm_steps` landmark is worker 3/5. There are 62 default suites, and the new one is not in the scheduled partition | listed in this report |

- **Suite independence.** The split leaves `milan_dp`'s `run` with no dependency on the GM-step leg.
- **One recipe.** The new suite rebuilds through `milan_dp`'s single recipe.
- **No concurrent writers.** The sweep (`scripts/run_all_suites.sh`) runs suites serially, so the two suites never write `milan_dp`'s generated images at the same time.

### Docs evidence

- **Capture page.** Every figure on `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` was re-derived from `measurements.json`: minimum, maximum, ratio and margin for all six arms.
  - The measured tree `a5d1a1b0` equals `034e2e30^{tree}`.
  - No RTL, firmware or config file changed between that tree and the head.
- **GPTP_PLANE.md.** Its counts match `phc_step.py`'s table: six plants, five distinct defects, and the cease-only positive control.
- **CI_WORKFLOWS.md.** Its worker 3/5 owner matches the shard rule.
- **Moved target.** TESTING.md, the READMEs and GM_LOSS_RECOVERY.md all reference the `gmstep-mutants` target by its new path.
- **Static gates.** 13 gates exit 0 (`receipts/static_gates.log`): docs_check, check_gptp_docs, check_submodule_docs, check_diagram_pngs, check_doc_paths, check_py_idiom, check_cpp_idiom, `measure_test_evidence --check`, `check_hygiene --check`, check_sweep_shape, check_doc_style, check_todo_ownership and `check_baremetal_only --check`.
- **Observed, not raised.** `tb/verilator/milan_dp/README.md:15` says "eleven ordinary simulations".
  - The text is identical at the base, and this lane did not touch it.
  - Under AGENTS.md section 4 it is new work, not a finding against this head.
  - The author has already disclosed it.

## 4. Prior findings at this head

| Finding | Severity | Status at `2cf985f3` | Evidence |
|---|---|---|---|
| R570-1-F1 = R571-1-F1 (test-evidence ratchet / hosted `docs-check`) | BLOCKER / MAJOR | RESOLVED | `measure_test_evidence.py --check` rc 0; hosted `docs-check` success at this head (`receipts/hosted_checks_snapshot1.tsv`) |
| R570-1-F2 (receipt arm escapes the production bound) | MINOR | RESOLVED | `production_spec` forces `mutation='none'`; `--mutation receipt-opt-out` exits 1 |
| R570-1-F3 = R571-1-F3 (design page figures) | MINOR | RESOLVED | All figures re-derived from `measurements.json` (Docs evidence) |
| R570-1-F4 = R571-1-F2 (answered crossing earns liveness credit) | MINOR | RESOLVED | `unanswered_at_drop=4` passes; `liveness-not-marked` and `r571-no-liveness` rejected by name |
| R570-1-F5 (auto-close of #621) | MINOR | RESOLVED | `closingIssuesReferences` is `[]`; the body says "Relates to #621" |
| R571-2-F1 (unanswered crossing earns no credit) | MINOR | RESOLVED | `unanswered_at_drop=3` passes; `credit-on-step` rejected by name |
| R570-4-F1 (runner tests encode the removed step) | MINOR | RESOLVED | `test_sim_pool.py` 17/17, and the `gmstep`-prerequisite plant fails it. `grep gmstep` shows only negative expectations and the never-run sentinel |
| R570-1-R1 / R571-1-R1, R570-4-R1 (Status wording) | RESIDUE | RESOLVED as written: line 16 carries R570-4-R1's exact fix. Line 17 has since gone stale; see R571-5-RES-1 | live PR body |
| R571-2-RES-1, R571-2-RES-2 | RESIDUE | RESOLVED | `GPTP_PLANE.md:141-147`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` |
| R570-1-S1 (ratio retention not observable) | SUGGESTION | carried, and now executed as R571-5-S1 | probes D and E |
| R570-1-S2 (no CHANGELOG entry for `7dda9c3b`) | SUGGESTION | carried, still open | `CHANGELOG.md` has no entry. Earlier pin advances are recorded inconsistently, so no binding rule applies |
| R570-1-S3 (ROM headroom of 8 words) | SUGGESTION | carried, still true | 1016/1024 words |
| R570-1-S4 (software settime does not set the step flag) | SUGGESTION | carried | See the note below this table |
| R570-1-S5 (TESTING.md `gptp_plane` row omits `phc-step`) | SUGGESTION | carried, still open | `docs/testing/TESTING.md:587` |
| R571-1-S1..S3, R570-2-S1 = R571-2-S1, R571-2-S2, R571-3-S1, R570-3-S1, R571-4-S1..S3, R570-4-S1 | SUGGESTION | carried, no lens effect | Not reopened |

**R570-1-S4, software settime.**
- `cfg_ptp_cmd_load` reaches the counter while the plane owns the PHC (`hdl/milan/milan_datapath.sv:2855-2858,2906`).
- The firmware console command `milan_settime` can issue it (`sw/firmware/milan_baremetal/milan_baremetal.c:1825-1842`).
- This is outside #621's grandmaster-driven scope. Whether to file a follow-up issue is the manager's call.

## 5. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | donor `gen_gptp_ucode.py` step, epoch, request and verdict legs; `sim_phc_step.cpp`; `sim_gmstep.cpp:952-1008`; base and head reproductions; issue items 1-3 and the rulings | R571-5 | `2cf985f3206dd519d80142fd2479afe24c3051f6` |
| RTL | CLEAN | parent hdl/configs/sw diff (empty); donor diff; ROM fit sweep; `rom_digests.tsv`; `gptp_plane_wrap.sv` | R571-5 | `2cf985f3206dd519d80142fd2479afe24c3051f6` |
| Robustness | CLEAN (SUGGESTION R571-5-S1 only) | crossing, silence and failure arms; peer-rate probes; step-flag plant; cease, beat-off and warm-reset paths; capture-gate controls | R571-5 | `2cf985f3206dd519d80142fd2479afe24c3051f6` |
| Tests | CLEAN (SUGGESTION R571-5-S1 only) | phc_step campaign; `milan_dp_gm_steps` suite; whole 20-control inventory; `gptp_plane` run; donor engine run and mutants; runner test and its plant; base-ROM failures | R571-5 | `2cf985f3206dd519d80142fd2479afe24c3051f6` |
| Docs | CLEAN (RESIDUE R571-5-RES-1 only) | GPTP_PLANE, GM_LOSS_RECOVERY, the capture page, TESTING, CI_WORKFLOWS, the READMEs, donor INTEGRATION.md, the PR body, 13 static gates | R571-5 | `2cf985f3206dd519d80142fd2479afe24c3051f6` |

## 6. Real limits

- **Hardware.** Physical calibration was NOT RUN. Simulation is not hardware proof. The bench repeat (issue item 3) belongs to the later lane.
- **Not run by this review:**
  - any full parent, protocol-processor, gPTP, Yosys or builder bank;
  - the vendor frontend, route or resource stages;
  - the act replica;
  - the capture campaign. The capture receipt was checked by its gate and controls, not re-measured.
- **Standard text.** The 802.1AS-2020 clause text was not re-read. The review used the clause citations in the issue and the published lost-response reading.
- **Shared host.** The `milan_dp_gm_steps` wall time (627 s) was measured on a shared host at load average 35-56. It is not a measurement of what the split costs.
- **Probe code.** The peer-rate and generator changes are disposable review probes. None of them ships.
- **Redaction.** In the published suite logs, the scoped simulator's install prefix is replaced by `<PINNED_VERILATOR_ROOT>` (`receipts/REDACTION.txt`). Nothing else in the logs was edited.
- **Clone integrity.** The review clone `$REVIEWS/r571-5-621` was never modified. After all runs (`receipts/clone_integrity.txt`):
  - HEAD and the tree are exact;
  - the index modes and blobs equal `ls-tree`;
  - re-hashing the worktree gives 0 blob mismatches;
  - the status is empty, including ignored files;
  - the gitlinks are gptp-processor `7dda9c3b`, protocol-processor `2ad2f845` and verilog-axis `48ff7a7e`, all clean.

## 7. Pending manager duties

- **Hosted.**
  - At the snapshot, these were success at this head: `docs-check`, `elaborate`, `rtl-fast`, `firmware-unit`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0/4 to 3/4, and Verilator shards 0/5 and 3/5. Shard 3/5 owns `milan_dp_gm_steps`.
  - Verilator shards 1/5, 2/5 and 4/5 were still in progress. Shard 4/5 owns `milan_dp`, so the runtime acceptance (within 60% of 4800 s) is still to be confirmed.
  - `Physical gPTP` was skipped by design, not executed.
- **Merge candidate.** The current-dev merge candidate (live dev `ac2c5e77`) and its builder and native banks.
- **Residue.** Carry R571-5-RES-1 and its exact fix to the residue checklist.
- **Donor.** The donor PR's own bar (FPGA-gPTP #77 at `7dda9c3b`).

R571-5 FINISHED
