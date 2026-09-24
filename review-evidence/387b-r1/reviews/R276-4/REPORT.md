[R276] NEGATIVE - exact head e68c1b1ac08c8b1e12a28e281b266d06f881e402

Round R276-4, internal cleared-context review of issue #387 / PR #555 (acceptance 3, datapath half), tree `c8b28ac217337d5d5e12af41e9ece31e3e80e831`, diff `57456af96b3127b9d309a995bbbd35a6113ce52d..e68c1b1ac08c8b1e12a28e281b266d06f881e402` (18 files, +762/-90). All five lenses applied. One BLOCKER and three MINOR findings are open, so four lenses are unclean. Robustness is covered clean.

The PR head moved to `a9636e0f670f90f411da3024a141e93efa1872df` during this round. That commit is not reviewed here, and nothing below applies to it.

## Reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md (sections 1, 3, 5, 6), docs/README.md. Then the issue #387 body with its frozen acceptance, and comments 5606198212 (part b), 5794731090 (owner step policy), 5802264260 (rulings: item 1 replaces the drift control, item 2 merges a step into a pending restart), 5810378282 (aligner decision), 5814963103 (A256 assignment), 5816940740 (A256 REVIEW READY) and 5816975318 / 5817241898 (A268 merge round). Then the PR #555 body. Then the RTL, harness and docs diff, the dev-merge delta (`00d388d8..e68c1b1a`: #547's servo RTL, mmcm_servo suite and docs rows only), and the public evidence tree `review-evidence/387b-r1` at `964ac393` (author and author-merge packets). Finally the exact-head hosted runs.

## Findings

### F1 - BLOCKER - Tests, RTL, Conformance - `sw/builder/test_builder.py:8856-8867` and `:10287-10296` - the builder's PHC-consumer pin still names the pre-#387 render trigger, and two hosted contexts are red at this head

- Authority/evidence: gate 1b (`test_baremetal_profile_contract`) pins the exact term set of `render_recentre_p_w` as `gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load | src_recentre_p_r`. Its comment calls it "the one consumer the two census rows above admit beyond the PHC crossing".
  - The head rewrites that initializer to `media_rebase_p_w | src_recentre_p_r` (`hdl/milan/milan_datapath.sv:6026-6028`).
  - It also adds a second reader of the two PHC control strobes (`media_rebase_p_w`, `:3110`, feeding `mcr_restart_p_w`, `:3111-3113`).
  - The gate and its ADP-term mutant (`:10287-10296`) were not updated.
- Hosted results at this exact head:
  - `elaborate` job 107707833579 fails: `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, `AssertionError: render recentre pulse must read only the GM-change, adjtime, settime and settled clock-source discontinuities: unexpected render_recentre_p_w initializer 'media_rebase_p_w | src_recentre_p_r'`.
  - `docs` / `docs-check` job 107707833793 fails in its compiler-absent step with the same assertion.
- Local reproduction (`scripts/probe_builder_render_pin.sh`, receipts `receipts/builder-gate1b-{base,head,probe}.log`):
  - dev base `57456af9`: rc 0.
  - This head: rc 1, same assertion.
  - A disposable probe that re-points only the pin and its mutant anchor at `media_rebase_p_w`: rc 0 (`receipts/builder-probe.patch`). So the defect is confined to the gate not following the RTL.
  - That probe is not a proposed fix. It leaves the new `media_rebase_p_w` reader of the PHC strobes unpinned.
- Impact:
  - Two required contexts are red, so the PR cannot merge.
  - A PHC-net ownership contract that a gate enforces changed without its declaration.
  - Acceptance 5 ("Verilator gates green on the exact candidate") is not met, since `elaborate` is a Verilator elaboration gate.
  - The published author evidence did not run this gate: A256 lists `test_builder.py` gate 11 as not run, and the A268 merge round ran no builder gate. The PR's green-gate statements therefore do not cover it.
- Required outcome:
  - The builder contract states the post-#387 consumer set of `eff_ptp_adjust_w` and `cfg_ptp_cmd_load`, including the restart path through `media_rebase_p_w`.
  - Its mutation arm plants a spliced term that the pin refuses.
  - `elaborate` and `docs-check` are green on the exact candidate.
- Verification:
  - `python3 sw/builder/test_firmware_compiler.py --absent --audit <file>` exits 0 at the candidate.
  - Hosted `elaborate` and `docs-check` succeed on that exact head.
  - The gate's ADP-term mutant still fires, and so does a mutant spliced into `media_rebase_p_w`.

### F2 - MINOR - Conformance, Docs - `hdl/ieee1722/avtp/KL_media_clock_restart.sv:55-71`, PR #555 "Decisions this change rests on" item 1, `docs/design/GM_LOSS_RECOVERY.md:157` - the implemented "pending" boundary is adoption, not the wire, and the stated reason is false in the tested case

- Authority/evidence: ruling 5802264260 item 2 says a step that lands while an `mr` restart is pending merges with it (one restart, never a cancellation). The round asks reviewers to judge the reading "pending = requested but not on the wire".
  - The RTL (`:205`, `tgt_r <= ~mr_o`) ends the pending window when the stream adopts the new level into `mr_o`. That happens before any PDU carrying it has launched.
  - The banner justifies a new restart after that point because "that stream's listeners have already seen the earlier toggle" (`:68-71`), and PR decision 1 says the same.
  - T17's own scenario contradicts the justification. Talker 0 adopts the disruption (`tb/verilator/tkdiag/sim_main.cpp:681`) and the step arrives three cycles later (`:686`), with no PDU sent on talker 0 in between. T17 nevertheless requires two toggles and two MEDIA_RESET (`:701-704`).
- Probe (`scripts/probe_pending_boundary.sh`, receipt `receipts/probe-pending-wire-boundary.log`): an engine that also merges while the adopted level has not yet completed a PDU (`hold_r == 0`) fails exactly T17's two talker-0 checks (got 1, expected 2). So the head implements "not yet adopted", not "not on the wire".
- Impact:
  - For the ruling's own example (a CRF disruption plus a step), a stream in steady state emits two toggles and counts two MEDIA_RESET when the step lands after adoption but before the new level's first PDU: up to one PDU interval, 125 us for an AAF talker and 2 ms for the CRF output. The "not on the wire" reading gives one.
  - The authoritative text asserts a rationale the harness shows to be untrue, so a maintainer confirming "the reading" would confirm a different boundary from the one built.
- Required outcome:
  - The RTL banner, the PR decision and the GM_LOSS_RECOVERY row state the boundary as implemented (the adoption edge), without the "listeners have already seen" claim, and the conflict with the "not on the wire" reading is published on #387 for a maintainer decision.
  - Or the engine implements the wire boundary with a failing arm.
- Verification: the text matches `mcr_track`; T17 (or the probe above) grades whichever boundary is decided.

### F3 - MINOR - Docs, RTL - `hdl/ieee1722/aaf/KL_render_setpoint.sv:81-83` and `:167-170` - the render stage's banner and port spec still list a GM identity change as a re-centre trigger

- Authority/evidence: CONTRIBUTING.md section 1 says "the port list IS the spec".
  - The `recentre_p_i` port comment reads "one-cycle: GM identity change, PHC step or a settled clock-source change".
  - The banner reads "the integration's set: a GM identity change, a PHC step, a clock-source change once its grid settled".
  - Since this head, the integration drives the port with `media_rebase_p_w | src_recentre_p_r` only (`milan_datapath.sv:6026-6028`). `TIME_SYNC.md:197` and `GM_LOSS_RECOVERY.md:151` were updated; this file was not.
- Impact: the module's own spec contradicts the decided behaviour (a GM identity change alone is no trigger). A reader of the module is told the opposite of what #387 decided.
- Required outcome: both comments name the post-#387 trigger set.
- Verification: read both lines against `render_recentre_p_w`, and run the docs gates.

### F4 - MINOR - Tests, Docs - PR #555 "Known limitations / out of scope: Sweep time", `docs/testing/CI_WORKFLOWS.md:159`, `scripts/run_all_suites.sh:240-242` - the stated `milan_dp` margin rests on a stale figure, and the real margin after this change is about half of what the PR states

- Authority/evidence: the PR says the added ~182 s leaves "roughly 595 s of the 2700 s budget", starting from "the #444 hosted worst case of about 1815 s" that CI_WORKFLOWS.md and run_all_suites.sh still record (885 s, 49%).
  - Two exact hosted dev runs today measured the `milan_dp` suite at 2133.3 s (dev `57456af9`, this PR's base) and 2099.5 s (dev `59b81670`), from the shard's `shard: 4/5` line to `PASS milan_dp` (`receipts/hosted-evidence.txt`). So the margin is already about 570 s before this change.
  - Locally I measured the added cost at 175 s: gmstep build and leg 39 s (`receipts/gmstep-head.log`) plus the three sweep controls 136 s (`receipts/gmstep-mutants-default-head.log`). That agrees with the author's 182 s.
  - At the documented ~1.58x hosted ratio, the dev base plus this change projects to roughly 2380-2420 s, leaving roughly 280-320 s (about 11%).
  - The exact-head hosted run cannot confirm this. It was cancelled at 1745.7 s, still inside the suite, when the PR head moved.
- Impact: a hosted `milan_dp` timeout is a red required context. The change roughly halves the real margin, while the PR and the authoritative budget table both describe a margin that does not exist. That is the decision input a maintainer would use to accept the added cost.
- Required outcome:
  - An exact-head hosted `milan_dp` duration is recorded.
  - The margin the PR states (and, if the maintainer so decides, the budget basis in CI_WORKFLOWS.md and run_all_suites.sh) is derived from current measurements.
  - The maintainer decides, on that figure, whether the three sweep controls stay in `run`.
- Verification: the exact-head shard 4/5 log shows the suite window, and the stated margin equals 2700 s minus that window.

### S1 - SUGGESTION - Docs - PR #555 body "Status"

It still reports head `00d388d8` and base `59b81670`. The sweep figures (9775 checks) were taken at `1dc93828`, before the dev merge brought #547's servo RTL into the `milan_dp` source list. The "Dev merge" section records the merge, but no full sweep is recorded at the merge head. Updating the status line to the reviewed head and naming the evidence head would help a cold reader.

### S2 - SUGGESTION - Tests - `tb/verilator/milan_dp/gmstep_mutants.py:230-231`, `tb/verilator/tkdiag/mcr_mutants.py:148-149`

Both runners take an existing `obj_gmstep` / `obj_dir` binary as the positive control when one is present. Through `make` it is always fresh, but a direct `python3 gmstep_mutants.py` after a source edit grades a stale clean binary. Rebuilding the clean leg, or checking its age against the sources, would close that gap.

## Judgments the round asked for

- **IEEE 1722-2016 4.4.4.3 and Milan Table 5.4.** Conformant apart from F2.
  - A step is ORed into `restart_p_i` ungated by selection (`milan_datapath.sv:3110-3113`), so each step requests one toggle.
  - The >= 8-PDU hold logic is unchanged (`KL_media_clock_restart.sv:207-224`), and MEDIA_RESET counts the `mr` bit each transmitted PDU carried (`KL_talker_diag_ctx` on the shared PDU feed).
  - gmstep at this head: one toggle, first sent at step pulse +116 cycles; one counted re-base at +132; one MEDIA_RESET and none between commit and step. 48/48 (`receipts/gmstep-head.log`).
- **Reading "pending = requested but not on the wire".** Not what is built; see F2. The built boundary is adoption into the stamped level.
- **Reading "streams may end on opposite `mr` levels".** Acceptable.
  - 4.4.4.3 defines the toggle and its hold per stream, and 10.4.3 makes only the recovered stream's bit valid.
  - No in-tree reader compares levels across streams: `tgt_r` is referenced only by the engine, `sim_nxn.cpp:3108` (updated to flip every context) and `mcr_mutants.py`.
  - The `KL_crf_tx.sv` change is comment-only.
- **The changed legacy tv/mr check (`tb/verilator/milan_dp/sim_main.cpp:975-979`).** Not a weakening.
  - The byte check masks only bit 3 (`& 0xF7`, still `0x81`), and a new check grades `mr` against the parity of the PHC steps the harness itself issued (`:560`, `:1034`).
  - Clean main leg at head: 231/0 (`receipts/main-leg-clean-head.log`).
  - A planted mutant that gates the step's `mr` term by CRF selection is caught by exactly that check: 231 checks, 1 failure (`receipts/probe-step-gated-by-crf-main-leg.log`, `scripts/probe_step_gated_by_crf.sh`). So "whatever the clock source" is graded outside the CRF-selected gmstep leg.
- **Sweep time.** +175 s measured locally. The margin is F4.
- **The #387 part b aligner decision is untouched.**
  - `KL_media_grid_align.sv` is not in the diff.
  - The GM_LOSS_RECOVERY aligner row (`:152`) is context-only in `57456af9..e68c1b1a`, so the merge kept #547's wording byte for byte.
  - The suite README's aligner bullet (`:501`) is unchanged.

## Lens results (clean lines carry their evidence)

- `[R276] BLOCKER Conformance - sw/builder/test_builder.py:8856-8867 - F1` and `[R276] MINOR Conformance - hdl/ieee1722/avtp/KL_media_clock_restart.sv:55-71 - F2`. Also applied and found sound:
  - `milan_datapath.sv:3097-3113`, `:6014-6028`
  - `KL_media_clock_restart.sv:189-226` against 4.4.4.3 / Table 5.4 and rulings 5802264260 items 1-2
  - gmstep 48/48, the three sweep controls 4/4, tkdiag 90/90 (T17 7/7) and mcr mutants 3/3 at this head
- `[R276] BLOCKER RTL - sw/builder/test_builder.py:8856-8867 - F1` and `[R276] MINOR RTL - hdl/ieee1722/aaf/KL_render_setpoint.sv:81-83,167-170 - F3`. Also applied and found sound:
  - Widths of the per-stream `tgt_r`.
  - A request on the adoption cycle merges (it reads the pre-edge `mr_o`).
  - Clock domain: engine and step pulse are both `axis_clk` (`milan_datapath.sv:3141`, `:2750`, `ptp_csr_sync` aclk).
  - Reset of `tgt_r` to `'0`.
  - `KL_crf_tx.sv` comment-only.
  - Hosted `yosys-elaboration`, `verilator-lint` and Yosys shards 0-3 green at this head.
- `[R276] PASS Robustness - hdl/ieee1722/avtp/KL_media_clock_restart.sv:189-226, tb/verilator/tkdiag/sim_main.cpp:639-705, receipts/probe-pending-wire-boundary.log, receipts/probe-step-gated-by-crf-main-leg.log - repeated and back-to-back requests (merge while pending, no cancellation: mutant caught), a request on the adoption cycle, a stream stopping or starting while pending (the non-streaming branch adopts the target and re-satisfies the hold), reset, feature/config dependence (INTERNAL selection graded by the main leg; plane-off adjtime and software settime are both steps, milan_datapath.sv:2750-2751; firmware settime is operator-invoked only, sw/firmware/milan_baremetal/milan_baremetal.c:99-104)`.
- `[R276] BLOCKER Tests - sw/builder/test_builder.py:8856-8867 - F1` and `[R276] MINOR Tests - docs/testing/CI_WORKFLOWS.md:159 - F4`. Also applied and found sound:
  - Each named control fails its named check: `receipts/gmstep-mutants-default-head.log`, `receipts/tkdiag-head.log`.
  - The CRF-gating mutant is caught by the changed legacy check.
  - The `run` wiring (`tb/verilator/milan_dp/Makefile:429`, `:526`) and `measure_test_evidence --check` exit 0.
- `[R276] MINOR Docs - F2, F3, F4`. Also applied and found sound:
  - CHANGELOG, REGISTER_MAP, TIME_SYNC:197, the TESTING rows, the suite README control table and the GM_LOSS_RECOVERY rows match the code.
  - The cycle figures (+132, +116) reproduce.
  - No U+2014 added.
  - `docs_check`, `check_doc_style`, `check_em_dash --base 57456af9` and `gen_toc --check` (pinned renderer in an isolated environment), `check_gptp_docs`, `check_doc_paths`, `check_py_idiom` and `check_cpp_idiom` all exit 0 (`receipts/gates-summary.txt`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #387 acceptance 3 and 5 with rulings; `milan_datapath.sv:3097-3113,6014-6028`; `KL_media_clock_restart.sv`; gmstep and tkdiag logs; hosted `elaborate` | R276-4 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| RTL | UNCLEAN (F1, F3) | `KL_media_clock_restart.sv`, `milan_datapath.sv` hunks, `KL_crf_tx.sv`, `KL_render_setpoint.sv` banner and ports, `test_builder.py` PHC census pin; hosted Yosys and lint | R276-4 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Robustness | CLEAN | `KL_media_clock_restart.sv:189-226`; T17; the wire-boundary and CRF-gating probes; plane-off adjtime and settime paths | R276-4 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Tests | UNCLEAN (F1, F4) | `sim_gmstep.cpp`, `gmstep_mutants.py`, `mcr_mutants.py`, tkdiag `sim_main.cpp`, milan_dp `sim_main.cpp` and `sim_nxn.cpp`, both Makefiles, builder gate 1b, hosted shard timing | R276-4 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Docs | UNCLEAN (F2, F3, F4) | CHANGELOG, GM_LOSS_RECOVERY, TIME_SYNC, REGISTER_MAP, TESTING, milan_dp README, RTL banners, PR body, CI_WORKFLOWS budget table | R276-4 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |

## Prior public review findings on this PR

Read only after the verdict, findings and ledger above were written.

- **None exist, so nothing is resolved or retained.** PR #555 has 0 review objects and 0 inline comments. Its only two comments are the manager's start notices for R276-4 and R277-3. Issue #387 carries no reviewer finding against this head.
- **Corroboration of F1, read after the verdict.** The manager's own assignment [A269] on #387 (comment 5817362105, 15:45 UTC) records that the manager's SDK builder run fails gate 1b at `e68c1b1a`, on the same pin (`assert_boot_contract`, around `test_builder.py:8861`).
- **Not reviewed.** [A269] reports a builder-only change at `a9636e0f`. F1 stays open at the head under review.

## Real limits

- The full `milan_dp` sweep was not run at this head (it is longer than one foreground command here). Run here at this head: the gmstep leg, its three sweep controls, the clean main 1x1 leg (`obj_dir` recipe) and tkdiag with its arm. The author's full sweep ran at `1dc93828`, before the dev merge. The exact-head hosted run was cancelled mid-suite by a later push. Hosted Verilator shards 0-3 passed at this head.
- The full builder bank was not run (outside this round's allowance). Only gate 1b was run, compiler-absent. Builder gates behind the failing one in hosted `elaborate` are unobserved at this head.
- The round brief says the manager's native and builder bank evidence passed at this head. That evidence is not in the named evidence tree (`review-evidence/387b-r1` at `964ac393` holds only the author and author-merge packets). The manager's later public assignment 5817362105 states that the builder run fails gate 1b at this head, which agrees with F1.
- The IEEE 1722-2016 and Milan clause texts were read as quoted in the tree, not from the standards.
- No Yosys, hardware, physical calibration or act run. Field skips are not hardware proof.
- The review clone was left byte-exact at the head: worktree and index equal HEAD, no rehash mismatch, required gitlinks at their pins (`receipts/review-clone-integrity.txt`). All probes ran in disposable shared clones under the packet's scratch directory, which is not published. Host paths in the receipts are redacted to `$HOME` and `$DATA`. The Verilator used is 5.050, identity in `receipts/verilator-identity.txt`, with at most 8 build jobs.

## Pending manager duties

- Correct the brief's "builder banks passed at this head" in the published record. The manager's own 5817362105, F1 and the red hosted `elaborate` / `docs-check` all show gate 1b failing at `e68c1b1a`.
- Obtain an exact-head hosted `milan_dp` duration for F4.
- Take F2's boundary question to the maintainer.
- The candidate merge build on current dev, hosted and act acceptance, and acceptance 4 (the #117 bench) remain with the manager.
- Any later head, including `a9636e0f`, needs its own review.

R276-4 FINISHED
