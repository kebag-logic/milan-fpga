[R276] NEGATIVE - exact head 44bf089108fec666d50873445720b51090ceede0

Round R276-1, internal independent review of PR #540 (Relates to #387, partial), at exact head `44bf089108fec666d50873445720b51090ceede0`, tree `48f1348f589dd7e75873df22dde4ab2f4eaf6f97`. Source base `759da623072358afdb0e9d570a7b4b6a788492c9`; the head descends linearly from it (four one-line commits, no trailers), so the source candidate tree is the head tree. All five lenses were applied. Five MINOR findings are open, so the verdict is NEGATIVE. The RTL lens is clean.

Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md; the #387 body with its frozen acceptance; the decisions 5606198212 (part b) and 5794731090; the donor ruling FPGA-gPTP#68 5798089412; the manager rulings 5802264260; the assignment 5800693336; the PR body; the diff and history `759da623..44bf0891`; the donor diff `c1b61743..e5dcea6e`; and the public evidence tree `review-evidence/387-r1` at `50840b3e`. I did my own pass over the diff before reading any review thread. PR #540 had no earlier review findings (only two review-start notices), so none needed resolving or retaining.

## What holds at this head

- **The pin adoption is sound. Nothing was hand-edited.**
  - The gitlink `e5dcea6e` is the donor main tip. It is the merge of FPGA-gPTP PR #74, with parents `c1b61743` and `ba926810`, and its tree `5a02fa35` equals `ba926810`'s tree.
  - The donor delta touches no SystemVerilog: only the generator, the tracked images, the docs and the donor testbenches.
  - I regenerated the default image at the pin twice and got `4afe436d...` both times. That equals the new row `syn/yosys/rom_digests.tsv:33` and the donor's own tracked images.
  - The old row (`:30`, `83f14a7d...`) is kept on purpose, because the ledger is keyed by pin. It is the only place that old digest appears.
  - `ooc.sh tcam` accepts the new row (exit 0), and `ooc_harness._ledger_digests()` resolves it.
  - No gPTP ROM is tracked in the parent. The builder regenerates each configuration's image, and all five equal the published per-configuration table.
  - The builder's parsers of the generator still read the pinned generator.
  - `scripts/regen.sh`, named in acceptance 5, has never existed in the tree. Regeneration from the configuration is what actually happens.
- **The parent envelope matches the donor clamp to the unit.**
  - The donor clamp is `gen_gptp_ucode.py` `ppm_addend(200, clk_hz)`.
  - The parent envelope is `KL_gptp_txret.sv:303-305` `PHC_ADJ_MAX_C`, with `RECON_REL_PPM_P = 200`.
  - The builder passes `--clk-hz` = `milan_clk_hz` (`endstation_builder.py:5591-5595`), and the shadow passes the same clock to txret.
- **TIME_SYNC.md "Step policy" agrees with every source.** It matches 5794731090, ruling 5798089412 and the donor `INTEGRATION.md` "Step versus slew policy" at the pin, and it states the rule exactly once. The pin-following docs and both diagrams pass their generators' `--check`.
- **The gmstep leg reproduces exactly.**
  - It scores 37/40, and its run output is byte-identical to the author's `gmstep-tree.log`.
  - The three failures are the declared ones: render counted 2, `mr` toggles 0, MEDIA_RESET 0.
  - With the published proposed patch applied to a scratch copy, it scores 40/40.
  - Ruling 1's control (the step's re-centre removed, on the patched copy) fails "render: the GM change is one counted re-base event".
  - At the head, both `tu` arms can fail: `tu` four cycles late, and the step not re-arming holdover.
- **Consumer suites at the head:**
  - `gptp_shadow` `make run`: 309/309.
  - `milan_dp` `make gptp`: 181/181.
- **Focused static and docs checks at the head:** 24 of them, all exit 0. They include `docs_check`, `check_em_dash --base 759da623`, `check_gptp_docs` with and without the submodule, the diagram checks, `gen_module_matrix --check`, `measure_test_evidence --check`, the C++ and Python idiom checks, `gen_toc` and `check_feature_status`.
- **Scope held.**
  - The hot files `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are untouched.
  - The PR says "Relates to #387" and states that acceptance 3 is not met.
  - All seven required hosted contexts are `success` at the exact head. `Physical gPTP (nightly and manual)` is a skipped context.

## Findings

**F1: MINOR (Conformance, Docs). The "decided reaction" recorded for the grid aligner contradicts the owner decision.**

- **Where:** `docs/design/GM_LOSS_RECOVERY.md:119`.
- **Authority and evidence:**
  - Decision 5606198212 part (b) says "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event".
  - 5794731090 keeps part (b) "unchanged", and ruling 5802264260 rules on three other points, none of them the aligner.
  - Row 119 nevertheless puts "Nothing to re-centre: neither reads the PHC" in the *Decided* column.
  - That the aligner has no PHC input is true of the tree (`hdl/ieee1722/crf/KL_media_grid_align.sv:89-106`), but it is an observation, not the decision.
  - The published handoff (`review-evidence/387-r1/author/HANDOFF.md`) shows the author knew the decision names the aligner, and no question about it was published.
  - Under CRF selection the aligner follows the physical grid, and the CRF servo steers that grid against the PHC. A step can therefore reach the aligner indirectly (see #539), so "nothing to re-centre" is a design judgement.
  - The gmstep leg holds the TDM clocks, so the aligner stays disengaged and nothing measures its reaction.
  - AGENTS.md section 2 requires such a conflict to be published for a decision, not settled privately.
- **Impact:** the one authoritative record states an owner decision the owner did not make. The follow-up lane implements against this page.
- **Required outcome:** a recorded ruling on the aligner's re-base, with the Decided column quoting it. Until that ruling exists, the Decided column carries part (b)'s wording and the tree column carries the observation.
- **Verification:** row 119's decided text is traceable to a decision or ruling comment that says it.

**F2: MINOR (Conformance, Docs). The one place that records the media re-base omits ruling 5802264260 point 2.**

- **Where:** `docs/design/GM_LOSS_RECOVERY.md:109-137`.
- **Authority and evidence:**
  - Point 2 rules that a step landing while an `mr` restart is pending merges with it: exactly one restart, never a cancellation, and the step's MEDIA_RESET is still counted.
  - Acceptance 2 asks for the media re-base "in one place". The PR and the REVIEW READY comment claim acceptance 2 is "Met".
  - The section has no row or sentence for the merge rule.
  - At the head, `KL_media_clock_restart` flips one target per request (`hdl/ieee1722/avtp/KL_media_clock_restart.sv:167`), so two requests inside one hold cancel. The tree state for this rule is therefore "Not yet".
- **Impact:**
  - The rule the follow-up must implement, with a failing arm, lives only in an issue comment.
  - The `mr` and MEDIA_RESET rows read as the whole rule, but the case they omit is the one that cancels.
- **Required outcome:** the section states the merge rule as decided, with its tree state.
- **Verification:** a reader of the section alone can state the rule, and the docs gates stay green.

**F3: MINOR (Docs). The page claims the gmstep leg measures more than it does.**

- **Where:** `docs/design/GM_LOSS_RECOVERY.md:133`, "The `milan_dp` gmstep leg measures all of this."
- **Evidence:**
  - The leg holds the TDM clocks, so the aligner stays disengaged (`tb/verilator/milan_dp/sim_gmstep.cpp:34-35`; `tb/verilator/milan_dp/README.md` "The model's limits").
  - It answers the MMCM DRP with zero data and grades no servo behaviour (`sim_gmstep.cpp:447-454`; no check names the servo).
  - It opens the talker through `AAF_CTRL[1]`, not an lwSRP licence (`sim_gmstep.cpp:30-32`).
  - Of the seven rows, the "Grid aligner and packet NCO" and "CRF servo" rows are not measured.
- **Impact:** the PR claims coverage it does not deliver, on the page a cold reader trusts.
- **Required outcome:** the sentence names what the leg grades and what it does not, or points to the README limits.
- **Verification:** the text matches the check list in `receipts/gmstep-head.log`.

**F4: MINOR (Tests). The counted-event checks do not tie the event to the step.**

- **Where:** `tb/verilator/milan_dp/sim_gmstep.cpp:857` and `:873-882`.
- **Evidence:** the probe `edit-identity-keyed-rebase` (`receipts/gmstep-probes.txt`) passes 40/40, the same result as the correct edit.
  - The probe takes the published proposed patch and keys `media_rebase_p_w` to the grandmaster-identity change instead of the plane's step. The step itself then triggers no re-centre, no `mr` toggle and no MEDIA_RESET.
  - The identity trigger is not contrived: it is the existing task #22 detector that still drives the I2S element (`hdl/milan/milan_datapath.sv:5983`).
- **Authority:**
  - 5794731090 says "every step is one counted event".
  - The leg's banner (`sim_gmstep.cpp:4-10`) claims to grade exactly that.
  - AGENTS.md section 6, Tests lens: "each new test can fail for the defect it claims to detect".
- **Impact:** once the follow-up wires the leg as acceptance 3's grader, it will accept an identity-keyed re-base. Under the decided policy such an implementation fails in two directions: it re-bases nothing on a locked same-grandmaster jump above 100 us or on a link-up step, and it counts a MEDIA_RESET on a grandmaster change that only slews.
- **Required outcome:** the leg separates the two triggers. Either each counted event must follow the step, which timing can check because the step lands 160000 cycles after the commit in this model, or a case separates them: a step with no identity change, or an identity change with no step.
- **Verification:** `scripts/gmstep_probes.py --only edit-identity-keyed-rebase` fails with a named check.

**F5: MINOR (Tests, Robustness). The licence checks cannot see a talker that stops for good.**

- **Where:** `tb/verilator/milan_dp/sim_gmstep.cpp:823-849` and `:808-818`.
- **Evidence:**
  - `longest` and `span` are measured only between successive talker PDUs (`:830`, `:833`). So the silence from the last PDU to the end of the window is never graded.
  - The `tu` grading also accepts a window with no PDU after `tu` clears (`:813`).
  - The probe `edit-talker-silent-after-event` (the proposed edit, plus a latch that silences the AAF packetizer permanently once `tu` clears after the change, while the gate register still reads open) passes 40/40.
  - That run printed "600 PDUs over 385200 cycles", against 1286 over 825612 for the clean edit. About 670 talker intervals of trailing silence went ungraded.
- **Authority:** REQ-PTP-08 (a licensed stream is never stopped), acceptance 3's "the stream stays licensed", and the check's own name, "the talker never pauses beyond four of its intervals".
- **Impact:** a defect that stops streams after a grandmaster step passes the leg meant to grade acceptance 3. The published control set cannot expose this, because its "tu stops the talker" control resumes after `tu` clears.
- **Required outcome:** the pause measure includes the interval from the last PDU to the end of the graded window, or the leg requires PDUs after `tu` clears.
- **Verification:** the probe fails with a named licence check.

**S1: SUGGESTION (Docs).** The comments at `tb/verilator/milan_dp/Makefile:99` and `:277` say "gmstep_mutants.py" uses the overrides, but no such file is in the tree. It exists only in the published evidence packet. Say it is pending, or describe the override without naming the file.

**S2: SUGGESTION (Tests).** At `sim_gmstep.cpp:843-844`, the MEDIA_UNLOCKED delta has no `counters_valid` guard. If both Stream Input GET_COUNTERS calls return nothing, both reads are `0xDEADBEEF` and the delta passes. On the output side, `sout0` validity is never checked (only `sout1`, at `:879`). Check word 32 on `sin0`, `sin1` and `sout0`.

**S3: SUGGESTION (Docs).** The CRF-servo row at `GM_LOSS_RECOVERY.md:120` could cite #539. That issue records the roughly 108 to 524 us band between the legitimate bound and the 1024 ppm guard, which is reachable now that every locked step exceeds 100 us.

## Per-lens results

- `[R276] UNCLEAN Conformance - docs/design/GM_LOSS_RECOVERY.md:109-137; PR #540 body; #387 acceptance 1-5 - F1 and F2 open.` Also examined, with no further finding:
  - Acceptance 1 is recorded.
  - Acceptance 3 is truthfully declared not met.
  - Acceptance 5's ROM regeneration is from the configuration.
  - The PR claims "Relates", not "Closes".
  - TIME_SYNC.md matches 5794731090 and 5798089412.
- `[R276] PASS RTL - gptp-processor gitlink e5dcea6e; donor diff c1b61743..e5dcea6e (no SystemVerilog); syn/yosys/rom_digests.tsv:33; gen_gptp_ucode.py ppm_addend vs hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:303-305,434-436; hdl/milan/milan_datapath.sv:1935-1936,2741-2744,3091-3092,5965-5967 (phc_step_we consumers unchanged); ooc.sh tcam; gptp_shadow 309/309; milan_dp gptp 181/181; gmstep elaboration - the imported ROM, its shape, its digest and its envelope agree with the parent consumer contracts, and no parent RTL changed.`
- `[R276] UNCLEAN Robustness - tb/verilator/milan_dp/sim_gmstep.cpp:808-849 - F5 open.` Also examined, with no further finding:
  - The leg's transport bounds: AXI throws after 2048 cycles, and AECP gives up after 400000.
  - The counter failure path (S2).
  - The donor's timeout, failover, asCapable-bounce and reset coverage, from the donor record; not re-run.
- `[R276] UNCLEAN Tests - tb/verilator/milan_dp/sim_gmstep.cpp:857,873-882,823-849; receipts/gmstep-head.log; receipts/gmstep-probes.txt - F4 and F5 open.` Also examined, with no further finding:
  - The reproduction.
  - The three declared failures.
  - Ruling 1's control.
  - The two tu arms.
  - Makefile `CLKV_SRC` and `GMSTEP_MDIR` work as overrides.
- `[R276] UNCLEAN Docs - docs/design/GM_LOSS_RECOVERY.md:109-137,163; docs/design/TIME_SYNC.md:66,75-105; tb/verilator/milan_dp/README.md:39,340-372; the pin-following guides, SUBMODULES.md, the traceability page and the diagrams - F1, F2 and F3 open.` Everything else in that set is consistent with the decisions and the tree, and the gates listed above pass.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #387 acceptance, decisions and rulings; PR body; GM_LOSS_RECOVERY.md and TIME_SYNC.md; exact-head hosted contexts | R276-1 | 44bf089108fec666d50873445720b51090ceede0 |
| RTL | CLEAN | gitlink and donor delta; ROM ledger row, regeneration and OOC validation; envelope derivation; datapath step consumers; gptp_shadow and milan_dp gptp suites | R276-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Robustness | UNCLEAN (F5) | gmstep licence and tu grading; transport bounds; counter failure path; probe `edit-talker-silent-after-event` | R276-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Tests | UNCLEAN (F4, F5) | sim_gmstep.cpp; Makefile gmstep recipe; head run 37/40; 7 probes | R276-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Docs | UNCLEAN (F1, F2, F3) | GM_LOSS_RECOVERY.md; TIME_SYNC.md; milan_dp README and Makefile comments; pin-following docs and diagrams; 24 docs and static checks | R276-1 | 44bf089108fec666d50873445720b51090ceede0 |

## Limits

- **Banks not run.** No full parent, protocol-processor, gPTP, Yosys or builder bank was run. Also not run here:
  - the `milan_dp` `run` recipe;
  - `gptp_shadow` lifecycle and mutants;
  - `gptp_plane`, `gptp_txts`, `clkvalid`, `media_grid_align` and `tsn_fuzz`;
  - `test_builder.py`, `lint_rtl`, `xvlog_gate` and the donor suites.

  The manager's source banks are the evidence for those.
- **No physical evidence.** Physical calibration was NOT RUN, and acceptance 4 (the #117 bench) was not attempted. The skipped physical nightly context is not hardware proof.
- **The probes judge the harness, not this PR's RTL.** They apply the published proposed patch to scratch copies. The patch itself belongs to the follow-up lane, and its design (for example, the restart no longer gated by the clock source) was not reviewed here.
- **The gmstep model is limited.** It runs a 2 MHz compressed fabric with the TDM clocks held and the DRP stubbed, and the talker is opened by the escape bit.
- **One interaction is unexamined in simulation.** No parent leg drives a 20 to 100 us locked slew, which runs the PHC rate at up to 200 ppm for 0.5 s or more. So its effect on the CRF servo is not exercised, nor its effect on `tu`, whose 0.25 s holdover can end before such a slew does. The donor records the slew publication. This is noted for the bench, not raised as a finding.
- **The live-dev candidate was not built.** Live dev is `26d855a9176d63625e6635a029a0c44e3d57ce9a`.
- **Scratch trees were not published.** They include the ROM regenerations, the builder outputs, the scratch datapath copies and the probe logs. The published receipts carry the results.

## Pending manager duties

- Route F1 to F5 to the author, and obtain the ruling F1 needs.
- Build and gate the current-dev candidate at the merge turn.
- Own hosted and act acceptance.
- Obtain the external review.
- In the follow-up after #529: apply the patch, wire gmstep and its runner into the sweep, and add the CHANGELOG entry. Then run the #117 bench measurement (acceptance 4).

## Clone state after the probes

`receipts/clone-integrity.txt` is a PASS:

- HEAD, the tree and the index tree all equal the exact head.
- All 873 tracked blobs match HEAD's bytes and modes, and no index entry carries a hide flag.
- `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are clean at their gitlinks. `external` is uninitialised by design.
- `git status --ignored` is empty. Every build output this session created was removed.

## Receipts

Every file below is listed in `MANIFEST.sha256`.

- `receipts/tool-identity.txt`
- `receipts/rom-regeneration.txt`
- `receipts/builder-per-config.txt`
- `receipts/ooc-tcam.txt`
- `receipts/static-docs-gates.txt`
- `receipts/gptp_shadow-run.txt`
- `receipts/milan_dp-gptp.txt`
- `receipts/gmstep-head.log`
- `receipts/gmstep-probes.txt`
- `receipts/clone-integrity.txt`
- `scripts/gmstep_probes.py`
- `scripts/verify_clone.sh`

R276-1 FINISHED
