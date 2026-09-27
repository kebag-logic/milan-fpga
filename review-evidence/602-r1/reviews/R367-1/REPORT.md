[R367] NEGATIVE - exact head 49012143b335ea48d6a71c441a05d0c1796887ff

# R367-1: external review of PR #603 (issue #602, deliverable 2)

- **Round:** R367-1, external independent reviewer, cleared context.
- **Head:** `49012143b335ea48d6a71c441a05d0c1796887ff`, tree `8b45256c51568c953830ae49e6e24139152ee70d`.
- **Base:** `6d5ebd7357c1e468e446f18a61527c5be6118a04`, an ancestor of the head.
- **Commits:** three, each one line with no trailers.
  - `f7660247e`: RTL, simulation and docs.
  - `81893de43`: one engine port comment.
  - `49012143b`: `test_builder.py` only.
- **Authorities read:** AGENTS.md, CONTRIBUTING.md and docs/README.md. From #602: the issue body, ruling 5859297355, assignment 5859299480 and scope correction 5859621253. From #387: decisions 5606198212, 5794731090 and 5802264260.
- **Material reviewed:** the diff and its history. From the public evidence tree `1dab2e7c:review-evidence/602-r1`, only the OOC and artifact-identity files.
- **Verdict basis:** two MINOR documentation findings are open, F1 and F2. The functional change, its simulation and its mutation evidence are correct. Nothing found blocks the RTL.

## The six assigned checks

### 1. The only functional RTL change: confirmed

`hdl/milan/milan_datapath.sv:3133-3134` is now `mcr_restart_p_w = crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)`. The `| media_rebase_p_w` term is gone. Every other `hdl/` hunk is comment text. `receipts/hdl_noncomment_diff.txt` shows this, and the engine hunks sit inside its block comment at lines 6-148.

These paths are untouched:

- `media_rebase_p_w` (`:3132`) still feeds `render_recentre_p_w` (`:6053-6055`).
- `cfg_ptp_cmd_load` still feeds `KL_ptp_clock_validity.phc_load_p_i` (`:1951`) for `tu`.
- The source-change trigger `src_change_w` is still inside `KL_media_clock_restart`, from `clk_src_i = media_clk_src_r`.
- The CRF-disruption and received-`mr` terms keep their `crf_clk_selected_r` gate.
- The engine's hold and merge logic have no code change.

### 2. The gmstep leg is real and can fail

At the head, the leg passes 64/64 at feed delay 0, and 64/64 at each of the 42 feed delays. The counted render re-base lands at step pulse +132 in all 42.

The leg asserts:

- no outgoing `mr` transition across the event;
- no MEDIA_RESET increment, both between commit and step and across the whole event;
- `tu` set, then held at least 0.25 s, then cleared;
- licence and continuity;
- one counted render re-base.

Both controls pass. The source-change control toggles `mr` once. The selected-CRF control toggles `mr` once; the sink stays locked, and no PHC step occurs meanwhile.

**Lane mutants: 16 of 16 caught by their named checks.** The three #602 arms fail these checks:

| Mutant | Check it fails |
|---|---|
| Re-base term restored | `restart: a PHC-only step leaves outgoing mr unchanged` |
| Source-change term removed | `source control: a real source change toggles mr once` |
| CRF propagation removed | `CRF control: selected CRF mr propagates exactly once` |

The retained negative control disables the render re-base. It fails `render: the GM change is one counted re-base event`.

**Reviewer mutants:**

- Five are caught:
  - the restored term, gated by CRF;
  - adjtime alone restored;
  - the GM identity requesting a restart;
  - the `tu` level requesting a restart;
  - the full restore graded on the option-off leg.
- RV5 survives simulation. It lets a coincident re-base suppress genuine restarts. Builder gate 1b's exact-RHS pin rejects it statically (F3, a SUGGESTION).

### 3. The test_builder.py edits are exactly what the ruling forces

Every edit follows from the ruling:

- The census count for `media_rebase_p_w` drops from 3 to 2.
- The pinned exact initializer loses the term. This makes the pin stricter.
- Two mutant anchors move to the expression's new last line, with the same mutant meaning.
- One diagnostic string, one expected-count message, the comments and the prose summary change to match.

Nothing is weakened:

- No mutant was deleted.
- Lines naming either net fall from 38 to 32; the hunks account for all six.
- The `eff_ptp_adjust_w: 3` census still holds.

### 4. Docs: the named files are right, the others are stale

These files state the ruling, cite #602 and keep "render re-base" distinct from "media-clock restart":

- GM_LOSS_RECOVERY.md;
- TIME_SYNC.md;
- the compliance matrix;
- the module comments;
- the milan_dp README.

Other current documents at the same head still state the old contract (F1). So do the TESTING.md routing row and a tkdiag header comment (F2).

### 5. Area: bounded and not functional

The whole changed cone synthesises to 38-42 LUT at 2 contexts and 155-156 LUT at 9 contexts. The edit's local effect is -4 and -1 LUT. The reported +182 and +1,606 LUT are larger than the entire engine, so they come from whole-design technology mapping, not from logic the edit touches. The section "Area delta" below gives the detail.

### 6. Generated artifacts: byte-identical

The reviewer regenerated all five configurations, each with its own tree's builder:

- all 50 artifacts are byte-identical between base and head;
- every generated `adp_shape_defaults.svh` equals the tracked copy.

## Findings

### F1 - MINOR - Docs - current authoritative documents still state the superseded contract

**Location** (all at the exact head):

- `docs/fpga/FPGA_DESIGN.md:178-179`: "A PHC step toggles `mr` whatever the clock-source selection. Every running Stream Output counts that toggle in MEDIA_RESET."
- `docs/reference/REGISTER_MAP.md:128-130`: "A PHC step toggles `mr` on every running Stream Output whatever the selection, and that output's Table 5.4 MEDIA_RESET counts the toggle it transmits (#387)."
- `docs/MILAN_V12_ROADMAP.md:360-361`: the same two sentences.
- `CHANGELOG.md:16` and `:116-135`: the "Unreleased - one media event per PHC step" entry still says "Every step now toggles `mr` once" and "Each talker's MEDIA_RESET counts the toggle it sends". No entry records the #602 reversal.

**Authority/evidence:**

- AGENTS.md section 6, `Docs`: "Changed contracts are reflected in authoritative docs."
- docs/README.md lists the FPGA design and the register map as current authorities, and the changelog as the record of measured changes.
- Ruling 5859297355 changes the contract, and this PR implements it. At the same head, GM_LOSS_RECOVERY.md, TIME_SYNC.md and the compliance matrix say the opposite of these files. `receipts/stale_doc_scan.txt` lists every hit.

**Impact:**

- An integrator or firmware author who reads the register map or FPGA design expects MEDIA_RESET to increment on every PHC step.
- A release or soak reviewer who reads the Unreleased changelog expects the pre-#602 behaviour. That is the conflict #602 was opened to remove.

**Required outcome:**

- At the merge head, no current document says that a PHC-only step or re-base toggles `mr` or counts MEDIA_RESET.
- The CHANGELOG records the #602 change. Editing the #387 entry or adding a #602 entry are both acceptable.
- Moving this to another Issue does not clear the lens (AGENTS.md section 7).

**Verification:** repeat the scan in `scripts/README-probes.md` at the new head. No hit outside `docs/history/**` may assert a PHC-step `mr` toggle or a step-only MEDIA_RESET.

### F2 - MINOR - Docs, Tests - campaign routing and a test header still describe the #387 integration

**Location:**

- `docs/testing/TESTING.md:273`, the `gmstep-mutants` explicit-campaign row:
  - It says "twelve gmstep controls and two option-off controls". At this head there are sixteen: fourteen gmstep and two option-off. `tb/verilator/milan_dp/README.md:707` says sixteen.
  - It says "The default sweep runs the three controls #387's acceptance names". Five now run with `acceptance=True`.
  - It still routes on "the option-off leg's PHC-step `mr` checks".
  - Its trigger list omits `hdl/ieee1722/avtp/KL_media_clock_restart.sv`. This PR adds a control that plants into that file, through `MCR_SRC`.
- `tb/verilator/tkdiag/sim_main.cpp:650-652`: "The ruling's example is a CRF disruption plus a PHC step; milan_datapath ORs both onto restart_p_i". That is false at this head. The stimulus comments at `:696` and `:754` also call the second request "the PHC step".

**Authority/evidence:**

- AGENTS.md section 6, `Tests`: real integration wiring is tested where practical, and tests must not merely reproduce implementation assumptions.
- AGENTS.md section 6, `Docs`: changed contracts must be reflected in authoritative docs.
- TESTING.md is the authority that tells a reviewer which explicit campaign a change must run.

**Impact:**

- A later change to `KL_media_clock_restart.sv` is not routed to the campaign that now holds its source-change control.
- tkdiag tells its reader that the datapath can present a PHC step and a CRF disruption to `restart_p_i` together. This PR removes that scenario.
- The engine tests themselves remain valid. At the head they pass 96/0, and 4 of 4 mutants are caught.

**Required outcome:**

- The TESTING.md row matches the inventory: the total count, the default-sweep count, no stale option-off wording, and `KL_media_clock_restart.sv` among its triggers.
- The tkdiag header describes the second request as a genuine restart request, not an integrated PHC step.

**Verification:**

- Read the row against `gmstep_mutants.py` `CONTROLS`: 16 in total, 5 of them `acceptance=True`.
- If check names change, re-run `make -C tb/verilator/tkdiag` and expect 96/0 with 4 of 4 mutants caught.

### F3 - SUGGESTION - Tests, Robustness - the coincident-step guarantee is structural, not simulated

**Location:** three sources make the claim:

- `docs/design/GM_LOSS_RECOVERY.md`: "A simultaneous PHC step neither adds nor suppresses those restarts."
- `docs/design/TIME_SYNC.md`: "A coincident step never suppresses a required media-clock restart."
- `hdl/ieee1722/avtp/KL_media_clock_restart.sv:105-109`.

**Evidence:**

- Reviewer mutant RV5 (`... | crf_mr_toggle_p_w) & ~media_rebase_p_w;`) passes the clean gmstep leg; see `receipts/mutants/reviewer4.log`. No leg drives a genuine cause inside a PHC-step window.
- The property does hold at this head, because `mcr_restart_p_w` has no PHC input.
- Builder gate 1b's exact-RHS pin rejects RV5 and every restore mutant. The pin is at `sw/builder/test_builder.py:10572-10586` and `:10774-10780`; the result is in `receipts/pin_probe.txt`.

**Optional outcome:** do one of these:

- add a coincident case, for example a received CRF `mr` toggle inside the step window;
- or state in the docs that gate 1b enforces this half of the ruling.

### F4 - SUGGESTION - RTL - the rename control shows determinism, not insensitivity

**Location:** the "neutral" rows of the public evidence file `ooc-comparison.json`.

**Evidence:** a local rename gives the same netlist before mapping. A delta of 0 therefore proves only that the flow is deterministic. It cannot show how far a one-gate structural change moves the mapped LUT count.

**Optional outcome:** when this flow is used as area evidence, record a cone bound as well, or a structurally different but functionally trivial control.

## Area delta (check 5)

**The before and after runs differ only in the datapath.** In the public evidence:

- The three ROM images have identical hashes before and after.
- The shaped `milan_datapath.sv` copies differ by -176 bytes. That is exactly the base-to-head source difference, 424195 to 424019 bytes.
- The staged `ooc.sh` copies are 43510, 43509 and 43511 bytes for before, after and neutral. That matches the length of each phase's directory name.
- `syn/yosys/ooc.sh` itself is identical at base and head.

**Cone bound.** This is the reviewer's own measurement, in `receipts/cone/`. The edited expression feeds only `KL_media_clock_restart.restart_p_i`; the census pins `mcr_restart_p_w` to two references. The engine outputs are register levels, so downstream structure does not depend on the edit. The reviewer synthesised the whole cone with the exact before and after expressions, using `synth_xilinx -family xc7 -flatten`:

| Contexts | Before LUT | After LUT | FF before/after |
|---:|---:|---:|---:|
| 2 (AX 1x1: N_STREAMS + 1) | 42 | 38 | 28 / 28 |
| 9 (AX 8x8) | 156 | 155 | 98 / 98 |

**Reading:**

- The removed term's local effect is -4 and -1 LUT.
- The reported +182 and +1,606 LUT are 4.3x and 10.3x the size of the whole engine.
- FF, LUTRAM, block RAM, DSP and CARRY4 counts are unchanged, so no register, FSM, memory or arithmetic inference changed.
- The 1x1 delta is a pure mapping trade:
  - wires are identical and total cells fall by 29;
  - LUT2 and LUT3 rise by 350 while LUT4 and LUT5 fall by 227;
  - MUXF7/8 fall by 153 and INV by 58.
- At 8x8 the mapper reaches a different whole-design cover: LUT +1,606, MUXF +136, wires +1,171.
- Removing the term does not defeat any restart-path optimisation; the cone shrinks.

**Conclusion:** the growth is mapping variation in an unplaced, flattened, whole-design flow. It does not signal a functional change. Release area is judged on the placed build.

**Limit:** the full-datapath OOC was not re-run. The public 8x8 log shows 816 s per run, which exceeds this round's per-command budget.

## Evidence

The reviewer ran every probe at the exact head, on disposable copies only:

- **Probe tree:** a local clone detached at `49012143`, with its submodules at their gitlinks:
  - `gptp-processor` at `5dce647a`;
  - `protocol-processor` at `870ff88a`;
  - `third_party/verilog-axis` at `48ff7a7e`.
- **Simulator:** Verilator 5.050 (rev v5.050). The assigned wrapper path did not exist. The reviewer used the identical wrapper from this issue's manager tool directory and confirmed its version with `--version`.
- **Synthesis:** Yosys 0.66.

| Probe | Command (see `scripts/`) | Result |
|---|---|---|
| gmstep, delay 0 | `make -C tb/verilator/milan_dp gmstep` | rc 0, 64/64 (`receipts/gmstep_clean_delay0.log`) |
| gmstep, 42 delays | `Vmilan_dp_gmstep aemi.bin D`, D = 0..41 | 42/42 rc 0, each 64/64, re-base at step +132 (`receipts/delays/`) |
| clean positive controls | `run_mutants.py --clean` | gmstep pass; option-off 234 checks, 0 failures |
| lane inventory | `run_mutants.py --set author` | 16/16 caught by their named checks (`receipts/mutants/results.tsv`) |
| reviewer mutants | `run_mutants.py --set reviewer` | 5 caught; RV5 survived (F3); RV7 survived (see note) |
| static pin probe | `pin_probe.py` | head accepted; RV5, the restored term, the adjtime restore and the full restore rejected |
| tkdiag | `make -C tb/verilator/tkdiag` | rc 0, 96/0, 4/4 mutants caught |
| RTL lint gate | `scripts/lint_rtl.py --check --jobs 8` | PASS, 90 of ratchet 90, none in the touched lines |
| cone synthesis | `cone_synth.sh` | table above |
| five configurations | `artifact_identity.py` | 5 x 10 artifacts, base == head, tracked headers equal |
| diff hygiene | `git diff --check 6d5ebd73 49012143` | clean |
| hosted snapshot | read-only PR status query | see note (`receipts/hosted_snapshot.json`) |
| review-checkout integrity | after all probes | HEAD, index and worktree equal the exact head; 930 tracked files match blob and mode; gitlinks at their pins (`receipts/clone_integrity.txt`) |

Notes on the table:

- **RV7** removes the pre-existing clock-source gate, which is outside the #602 scope. Builder gate 1b's pin also rejects it.
- **Hosted snapshot** at query time:
  - `rtl-fast`: SUCCESS.
  - Yosys shards 0-3: SUCCESS.
  - Verilator shards 0 and 3: SUCCESS. Shards 1, 2 and 4: still in progress.
  - Physical gPTP: skipped.

## Reviewer-owned completion ledger (R367-1)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5859297355 and assignment items 1-4 against `milan_datapath.sv:3121-3134` and `KL_media_clock_restart.sv` (`src_change_w`, `restart_p_i`). The gmstep `restart:`, `source control:`, `CRF control:`, `tu:`, `licence:` and `render:` checks (64/64 at 42 delays). The option-off `CLKV: ... (#602)` checks | R367-1 | 49012143b335ea48d6a71c441a05d0c1796887ff |
| RTL | CLEAN | `milan_datapath.sv:1951`, `:2761`, `:3094-3134`, `:3163`, `:6044-6055`. The engine diff (comment-only). Lint gate. Cone synthesis at 2 and 9 contexts. OOC stat blocks before, after and neutral | R367-1 | 49012143b335ea48d6a71c441a05d0c1796887ff |
| Robustness | CLEAN | INTERNAL with the plane off (adjtime and settime), CRF with the plane on, 42 accept phases, repeated steps. The coincident path by structure and by the gate 1b pin (F3 is a SUGGESTION) | R367-1 | 49012143b335ea48d6a71c441a05d0c1796887ff |
| Tests | UNCLEAN (F2) | `sim_gmstep.cpp`, `sim_main.cpp`, `gmstep_mutants.py`, Makefile `MCR_SRC`. 16 lane and 7 reviewer mutants. `test_builder.py` hunks at 10714-10791, 12478-12505, 15100-15115 and 16651-16660. tkdiag. TESTING.md:273 | R367-1 | 49012143b335ea48d6a71c441a05d0c1796887ff |
| Docs | UNCLEAN (F1, F2) | Correct: GM_LOSS_RECOVERY.md, TIME_SYNC.md, the compliance matrix, the milan_dp README, the module comments. Stale: FPGA_DESIGN.md:178, REGISTER_MAP.md:128, MILAN_V12_ROADMAP.md:360, CHANGELOG.md:16 and :116-135, TESTING.md:273, tkdiag `sim_main.cpp:650` | R367-1 | 49012143b335ea48d6a71c441a05d0c1796887ff |

## Prior public review findings on PR #603

This section was read after the verdict and ledger above were written.

- **On PR #603:** no prior findings. The only public items are the two review-start notices, 5859885900 (R366-1) and 5859888993 (R367-1). There are no PR reviews and no inline review comments.
- **Origin of #602:** R362-1 F4 on PR #601. This round knows it only from the #602 issue body and did not read that report. It raised the conflict between the owner `mr` rule and the #387 PHC-step toggle. At this head the RTL side of that conflict is resolved, because a PHC-only step produces no `mr` toggle and no MEDIA_RESET. The documentation side stays open in the files named in F1.

## Real limits

- **Area:** the full-datapath OOC was not re-run. The area conclusions rest on the public stat blocks and the reviewer's cone synthesis.
- **Banks not run:** the full parent, PP, gPTP, Yosys and builder banks, the `milan_dp run` sweep, the docs gates, act and the hosted replica. This round was not permitted to run them.
- **Builder gate 1b:** reasoned from source, and replicated only for the pinned expression.
- **Hardware:** no physical calibration and no hardware. Field skips are not hardware proof.
- **gmstep model:** the leg runs in compressed time, the CRF servo DRP answers zero, and the escape bit licenses the talker.
- **Overlap:** the overlap with PR #601/#593 in GM_LOSS_RECOVERY.md and TESTING.md is not judged here.

## Pending manager duties

- Hosted exact-head acceptance. Verilator shards 1, 2 and 4 were still in progress at the snapshot.
- The act/local replica for this head.
- The current-dev candidate at the merge turn: source base `6d5ebd73`, live dev `8bc97021`.
- Resolve F1 and F2, then re-review the Tests and Docs lenses at the new head.
- The composition review of the overlap with PR #601.

R367-1 FINISHED
