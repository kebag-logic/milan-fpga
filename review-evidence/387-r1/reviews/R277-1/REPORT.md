[R277] NEGATIVE - exact head 44bf089108fec666d50873445720b51090ceede0

Round R277-1, external independent review of issue #387 / PR #540 (Relates to #387, partial).
Exact head `44bf089108fec666d50873445720b51090ceede0`, tree `48f1348f589dd7e75873df22dde4ab2f4eaf6f97`, source base `759da623072358afdb0e9d570a7b4b6a788492c9`.
The round ran from a cleared context. It used only public state: AGENTS.md, CONTRIBUTING.md, docs/README.md, and the issue body with its decisions and rulings (5606198212, 5794731090, 5800693336, 5802264260).
It also used FPGA-gPTP#68 with its owner decision (5794731372) and ruling (5798089412), the diff and history, and the public evidence tree at `50840b3e`.
The verdict, findings and ledger below were written before any other reviewer's report was read. The prior-findings section was added afterwards.

## Verdict

NEGATIVE. Three open MINOR findings of this round leave Conformance, Robustness, Tests and Docs unclean at this head. Three MINORs from the earlier round R276-1 (F2, F4, F5) are independently confirmed and retained under the same lenses. RTL is clean.

What holds, verified at this head:

- **The pin.** `gptp-processor` moves from `c1b61743` to `e5dcea6e`. That commit is donor `main` (compare: identical) and the merge of FPGA-gPTP PR #74. Its tree `5a02fa35` equals the reviewed head `ba926810`. The donor diff touches only the ROM generator, its tracked images, its tests and its docs; no donor `.sv` changes.
- **The ROM ledger.** `syn/yosys/rom_digests.tsv` gains exactly one row (line 33) and loses none. The pinned generator reproduces `4afe436d...` for `e5dcea6e`, and the old generator still reproduces the retained `83f14a7d...` row for `c1b61743`. The protocol-processor rows at `424c688f` are intact, and the body stays sorted and unique. The image is 1024 x 48 bits, matching `UPC_W_C = 10` and `UCODE_W_C = 48`.
- **No ROM consumer left stale.** The parent tracks no gPTP ROM image, and the ledger is the only tracked digest record. The builder regenerates the ROM per configuration from the pinned generator. All five configurations reproduce the author's per-configuration digests at the new pin.
- **Pin-bearing docs.** The donor deep links, the pin table and both pin-bearing diagrams follow the gitlink. The generators' `--check`, the PNG manifest check and the submodule and gPTP doc checks all pass. The remaining `c1b61743` mentions are dated "Source examined" statements in two proposed design pages, which is correct.
- **Consumer suites on the new ROM, re-run here** with Verilator 5.050 through the pinned wrapper (sha256 `905795b9...e92f`): `gptp_shadow` 309/309 with its mutant lifecycle PASS, and `milan_dp gptp` 181/181.
- **The gmstep leg at head:** 40 checks, 3 failures, exactly the three the PR names (two counted re-bases, no `mr` toggle, no MEDIA_RESET). The check lines are identical to the author's receipt.
- **The proposed datapath patch** (public evidence) applies cleanly and reproduces the published edited copy byte for byte. With it the leg reaches 40/40 at the shipped start phase. My own versions of the seven negative controls, plus two extras, were each caught by the named check.
- **The step policy text.** TIME_SYNC.md "Step policy" states the owner decision 5794731090 and the link-up ruling 5798089412 correctly and once, consistent with the donor's INTEGRATION.md at `e5dcea6e`.
- **Hot files untouched.** `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are not in the diff.
- **Static gates pass at head:** 18 focused doc, path, TOC, style, feature-status, source-list, C++ and hygiene gates, plus the module matrix, Python idiom and lint pragma gates.
- **Hosted checks at the exact head:** 21 executed jobs succeeded, including all five Verilator and four Yosys shards. The "Physical gPTP (nightly and manual)" job was skipped; it is not hardware evidence.

## Findings

```text
[R277] MINOR Conformance, Docs - docs/design/GM_LOSS_RECOVERY.md:119 - the "Decided reaction" for the grid aligner contradicts decision (b) without a public ruling
Requirement/evidence: #387 decision 5606198212 part (b) reads "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event"; 5794731090 restates part (b) as unchanged. The page's "Decided reaction to one step" column says for the grid aligner "Nothing to re-centre: neither reads the PHC". No ruling changes that part: 5802264260 rules on the render negative control, the mr merge and the CRF guard only. The technical observation is true of the tree (hdl/ieee1722/crf/KL_media_grid_align.sv:97-106 has no PHC or step input), but AGENTS.md section 2 requires a decision/implementation conflict to be published for a decision, not resolved in the page and attributed to the owner.
Impact: the authoritative page tells later lanes and the #117 bench that the owner decided the aligner needs nothing. Acceptance 2 ("state ... the media re-base") is therefore not faithfully met for that row.
Required change: either obtain and link a public ruling that the aligner's phase reference has nothing to re-centre, or restate that row as the decision records it and show the gap in the "This tree" column. When the decided column is next revised, it should also carry ruling 5802264260 item 2: a step inside a pending restart merges into exactly one restart and still counts its MEDIA_RESET.
Verification: the row matches the linked decision or ruling; scripts/docs_check.py, check_doc_style.py and check_em_dash.py pass.
```

```text
[R277] MINOR Docs, Tests - docs/design/GM_LOSS_RECOVERY.md:133 (also :163) - "The milan_dp gmstep leg measures all of this" overclaims what the leg grades
Requirement/evidence: The section's table has seven rows, and the leg does not measure three of them.
  - The CRF servo's window guard: the DRP responder answers 0 (tb/verilator/milan_dp/sim_gmstep.cpp:447-454), and none of the 40 checks reads the servo.
  - The grid aligner: the TDM clocks are held, so the aligner stays disengaged (tb/verilator/milan_dp/README.md:365).
  - Licensed streams: the talker is opened by the AAF_CTRL[1] escape, not by an lwSRP licence (README.md:366; sim_gmstep.cpp:30-32).
  The README states these limits; the design page does not.
Impact: the authoritative page claims executable evidence for the CRF guard's reaction to a step, which does not exist. That guard is exactly where #539 records an open gap.
Required change: say which rows the leg grades and which it does not, and name where each ungraded row is covered or left open (#539 for the guard, the #117 bench, the licence limit).
Verification: every row the page says the leg measures maps to a named check in sim_gmstep.cpp.
```

```text
[R277] MINOR Tests, Robustness, Docs - tb/verilator/milan_dp/sim_gmstep.cpp:94-95, 734-737, 868 (banner :37-41; README.md:367) - the render-law arms depend on the leg's start phase and fail a correct datapath
Requirement/evidence: AGENTS.md section 6 Tests ("each new test can fail for the defect it claims to detect", and it must not fail without one). The arms grade the fill at avtprx_accept_p against a band of setpoint..setpoint+1. That sample is upstream of the render stage's push, where the #386 law is defined (hdl/ieee1722/aaf/KL_render_setpoint.sv:54-59).
  Probe (scripts/phase_probe.sh): add 0..41 idle cycles before the peer's media feed starts. One media tick is 41.67 cycles; the probe changes no RTL.
  - At head, offsets 6-12 (7 of 42) fail the baseline band arm with the fill at accept at 10.
  - Offset 12 also fails "one constant" and "holds its constant across the event".
  - With the proposed datapath edit (40/40 at the shipped phase), the same 7 offsets fail 1 or 3 checks.
  - The law quantity, the fill right after the push (TARGET = 14), is 14 in all 84 runs, so the RTL keeps its law. The arm, not the stage, moves.
  - An unrelated mutant hit the same window: lengthening the clock-validity holdover (H8) shifted acquisition by 8 cycles and failed the band arm.
  README.md:367 and the banner state "the fill constant is the band's upper edge, 9 events" as a fixed property of the 2 MHz model.
Impact: the PR plans to wire this leg into the sweep. Any change that moves acquisition by a few cycles (poll count, ROM timing, holdover) can then fail a correct datapath. A negative control can also be caught for the wrong reason.
Required change: grade the render law at its own reference point, or fix the feed's phase to the media tick with the reason recorded, so the leg with the edit passes at every start phase. Then correct the banner and README statement.
Verification: scripts/phase_probe.sh passes all 42 offsets with the edit, and the negative controls are still caught by their named checks.
```

```text
[R277] SUGGESTION Docs, Tests - tb/verilator/milan_dp/Makefile:99, :277 - the comments name gmstep_mutants.py, which is not in the tree
Requirement/evidence: git ls-files lists only sim_gmstep.cpp for gmstep. The runner exists only in the public review evidence (author/work/gmstep_mutants.py). README.md:361 correctly says it joins later.
Impact: a reader looking for the runner the comment describes will not find it.
Required change: land the runner or say it joins with the datapath edit.
Verification: the comment names a tracked file, or none.
```

```text
[R277] SUGGESTION Tests, Robustness - tb/verilator/milan_dp/sim_gmstep.cpp:843-844 - the Stream Input GET_COUNTERS answers are never checked for validity
Requirement/evidence: the Stream Output answer is checked (word 32 == 0x1F); the Stream Input answers are not. Probe H9 forces the datapath's Stream Input counter select to 0. "The listener stays locked (MEDIA_UNLOCKED unchanged)" still passes (0 - 0), and FRAMES_RX +0 is printed but not graded.
Impact: low, because a real lock loss comes with silence or an unbind, which the render arms catch. But the named arm itself can pass vacuously.
Required change: check counters_valid for both Stream Input answers, and check that FRAMES_RX advances.
Verification: probe H9 fails the leg.
```

```text
[R277] SUGGESTION Docs - docs/design/TIME_SYNC.md:95 - "The bound is PHC_ADJ_MAX_C, which KL_gptp_txret enforces"
Requirement/evidence: KL_gptp_txret.sv:434-436 does not clamp the trim. It refuses egress timestamps while the applied addend exceeds the envelope. The clamp itself is the donor microcode's (ppm_addend, gen_gptp_ucode.py:428).
Required change: say the plane clamps to the bound, and that KL_gptp_txret refuses egress timestamps outside it.
```

Observations, not findings:

- **The render count arm at head.** Removing either the step trigger (H3) or the identity trigger (H4) gives exactly one counted re-base, so the arm passes. With the datapath edit it discriminates the count (E2 and E3 are caught), but not the trigger source: see the retained R276-1 F4, confirmed by probe E8.
- **The commit discontinuity.** Unplugging it into the clock-validity block (H5) does not fail "tu set in the first cycle the bank names GM B". The sync verdict clears on the same commit, so `tu` still rises there, and the acceptance wording is met by either path.

## Per-lens results

```text
[R277] PASS RTL - gptp-processor gitlink e5dcea6e (donor diff c1b61743..e5dcea6e: gen_gptp_ucode.py and images only, no .sv); syn/yosys/rom_digests.tsv:33; hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:303-305 vs gen_gptp_ucode.py:428 ppm_addend; tb/verilator/milan_dp/Makefile:101,146 (CLKV_SRC resolves to the same file); KL_render_setpoint law held in all 84 phase-probe runs - ROM geometry, envelope derivation and consumer behaviour checked against the parent contracts; gptp_shadow 309/309, milan_dp gptp 181/181; no parent RTL in the diff
[R277] UNCLEAN Conformance - docs/design/GM_LOSS_RECOVERY.md:115-123 against 5606198212(b), 5794731090, 5802264260; docs/design/TIME_SYNC.md:75-105 against 5794731090, 5798089412 and donor INTEGRATION.md "Step versus slew policy" - the step policy is stated correctly and once; the re-base row for the aligner is not (finding 1)
[R277] UNCLEAN Robustness - sim_gmstep.cpp render-law arms under 42 start phases x 2 datapaths (finding 3); licence arms against a permanently silenced talker (retained R276-1 F5, probe E9); counter-transport vacuity (suggestion); waits are cycle-bounded (AXI 2048, AECP 400000 cycles)
[R277] UNCLEAN Tests - sim_gmstep.cpp 40 checks re-run at head (37/40) and with the edit (40/40); 20 fault probes (receipts 20-25); phase sweep (receipts 30-34) - findings 2 and 3, and retained R276-1 F4 and F5
[R277] UNCLEAN Docs - TIME_SYNC.md step policy, GM_LOSS_RECOVERY.md re-base section and verification row, milan_dp README gmstep section, Makefile comments - findings 1, 2 and 3
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (finding 1; retained R276-1 F2) | TIME_SYNC.md step policy; GM_LOSS_RECOVERY.md re-base table; decisions 5606198212, 5794731090; rulings 5798089412, 5802264260; donor INTEGRATION.md at e5dcea6e; REQ-PTP-05/07/08/09 | R277-1 | 44bf089108fec666d50873445720b51090ceede0 |
| RTL | CLEAN | gitlink e5dcea6e and donor diff; ROM digest ledger; ROM geometry; KL_gptp_txret envelope; clock-validity and render wiring in milan_datapath.sv (unchanged); Makefile source list | R277-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Robustness | UNCLEAN (finding 3; retained R276-1 F5) | sim_gmstep.cpp under the phase sweep and 20 fault probes | R277-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Tests | UNCLEAN (findings 2, 3; retained R276-1 F4, F5) | gmstep leg at head and with the proposed edit; negative controls; probes E8 and E9; consumer suites gptp_shadow and milan_dp gptp | R277-1 | 44bf089108fec666d50873445720b51090ceede0 |
| Docs | UNCLEAN (findings 1, 2, 3; retained R276-1 F2) | TIME_SYNC.md, GM_LOSS_RECOVERY.md, GPTP_PLANE.md, SUBMODULES.md, guides/gptp/*, traceability/ieee8021as.md, both diagrams, milan_dp README and Makefile | R277-1 | 44bf089108fec666d50873445720b51090ceede0 |

## Prior public review findings

The only earlier review on PR #540 is R276-1 (internal, NEGATIVE, same exact head, PR comment 5804105668). I read it after the verdict, findings and ledger above were written. Each of its findings is disposed of below at this head. "Retained" means still open, independently checked here.

| R276-1 item | Disposition at 44bf0891 | Independent evidence |
|---|---|---|
| F1 MINOR Conformance, Docs: aligner row contradicts decision (b) | RETAINED | Same defect as R277 finding 1, found independently. |
| F2 MINOR Conformance, Docs: the one-place re-base record omits ruling 5802264260 item 2 (a step during a pending restart merges into one restart and still counts MEDIA_RESET) | RETAINED | GM_LOSS_RECOVERY.md:109-137 has no merge rule. `KL_media_clock_restart.sv:167` flips `tgt_r` once per request, so two requests inside one hold cancel; the tree state is "Not yet". I had carried this only inside finding 1's required change. As a gap in the record acceptance 2 names, it stands as its own MINOR. |
| F3 MINOR Docs: "measures all of this" overclaims | RETAINED | Same defect as R277 finding 2, which also adds the Tests lens. |
| F4 MINOR Tests: the counted-event arms do not tie the event to the step | RETAINED | Probe E8 (receipt 25) keys `media_rebase_p_w` to the grandmaster-identity pulse instead of the step, on the proposed edit, and passes 40/40. One identity change coincides with one step in this scenario, so the render, `mr` and MEDIA_RESET counts cannot tell the two triggers apart. My observation above ("it only discriminates with the datapath edit") covers the count, not the trigger. This is a real gap in my own pass. |
| F5 MINOR Tests, Robustness: the licence arms cannot see a talker that stops for good | RETAINED | Probe E9 (receipt 25) silences the AAF packetizer permanently once `tu` clears after the change, with the admission gate untouched, on the proposed edit. It passes 40/40 and prints "600 PDUs over 385200 cycles", against 1286 over 825612 clean. `longest` and `span` (sim_gmstep.cpp:828-835) never include the trailing silence. |
| S1 SUGGESTION: Makefile names a runner not in the tree | RETAINED | Same as R277 suggestion 1. |
| S2 SUGGESTION: no counters_valid guard on the Stream Input answers (and on `sout0`) | RETAINED | Same as R277 suggestion 2; probe H9 shows the vacuous pass. |
| S3 SUGGESTION: cite #539 on the CRF servo row | RETAINED | Consistent with R277 finding 2's required change. |

Effect on this round: R276-1 F2, F4 and F5 are additional open MINORs at this head. They fall under Conformance and Docs (F2) and Tests and Robustness (F4, F5), all already unclean here, so the verdict and the ledger states do not change. The open MINOR set at this head is R277 findings 1-3 plus R276-1 F2, F4 and F5.

## Limits

- **Not run by this reviewer:** the full parent, protocol-processor, gPTP, Yosys and builder banks; the full `milan_dp` `run` recipe; `tsn_fuzz`; the physical `milan_dp_gptp` leg; act; hardware. Source-bank results are the manager's public evidence, not re-derived here.
- **The phase probe** changes only the harness copy's start offset and adds a print. It proves the arms' phase dependence at 2 MHz and says nothing about 100 MHz legs.
- **Why the fill at accept reaches 10** (accept-to-push latency at the compressed clock) is inferred from the measured sawtooth, not traced cycle by cycle.
- **Probe coverage.** The probes are single mutations on private copies. They do not cover the proposed edit's merge rule (ruling 5802264260 item 2), which is not implemented yet.
- **Not hardware evidence.** Physical calibration was NOT RUN, and skipped hosted contexts are not hardware proof.
- **Clone restored.** The review clone was restored and re-verified: head, tree and index, every tracked blob and mode, no untracked or ignored files, and the three required submodules at their gitlinks with byte-exact blobs (receipt 90).

## Pending manager duties

- Route findings 1-3 and the retained R276-1 F2, F4 and F5 to the author lane. Finding 1 needs a public ruling, or a page correction, on the grid aligner row.
- Build and gate the final current-dev candidate: source base `759da623`, live dev `26d855a9` at the start of this round.
- Keep hosted and act acceptance, and bank a lens only at a head that includes the fixes.
- Track the deferred items on #387:
  - the `milan_datapath.sv` edit, with ruling 2's merge arm;
  - wiring `gmstep` and its negative-control runner into the sweep;
  - the CHANGELOG entry for this pin's behaviour change, held with the hot file;
  - #539;
  - the #117 bench step (acceptance 4);
  - the unruled talker-licence model limit (the author's open question 5).

## Receipts

Listed in `MANIFEST.sha256`; scripts are under `scripts/`, receipts under `receipts/`.

- `00` / `90`: clone baseline and final verification.
- `01`: ROM digest reproduction.
- `02`: static gates.
- `03`: scratch-copy verification.
- `10`: gmstep leg at head.
- `20`-`25`: fault probes, one JSON line each (25 is the two probes checking the earlier round's F4 and F5).
- `30`-`34`: phase sweep, sawtooth and full script sweep with its summary.
- `40`: hosted check runs.
- `41`: per-configuration ROM digests.
- `50` / `51`: consumer suites.
- `raw/`: selected full logs.

R277-1 FINISHED
