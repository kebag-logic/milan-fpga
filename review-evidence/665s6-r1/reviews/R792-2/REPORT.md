[R792] NEGATIVE - exact head 526f937cde45e3a591fb3b9484ffdcaddbdfa144

# R792-2: external review of PR #853 (#665 S6a, the placement switch), round 2

- Head: `526f937cde45e3a591fb3b9484ffdcaddbdfa144`, tree `e57b34a1f1d150cca37c2ffa8fb42001f05192ae`. Target: `dev-soft-core`. Source base: `a9d69c77`.
- Delta reviewed: `6584b7bf..526f937c`, eight commits and 23 files. This is judged against round 1 (R792-1 and R791-1, both at `6584b7bf`). Code the delta does not touch keeps its round 1 lens verdict.
- Evidence read: author round 2 receipts at `1f33e530:review-evidence/665s6-r1/author-r2`. All 1,122 manifest entries hash-match the published tree, with no unlisted file (`receipts/evidence-manifest-verify.txt`). Also read: the PR body, ruling issuecomment-6715535566, the S6 assignment issuecomment-6712890110, and both round 1 reports, which were opened only after this round's own pass over the diff.

## Verdict in one paragraph

Every finding of both round 1 reviews is fixed at its cause and verified by its own verification step. That includes the reviewers' probes, run unchanged at this head.
- The drop count now counts: the leg fails 3 checks on round 1's tap and passes 66 of 66 at the head.
- The CDC check refuses every raw crossing either reviewer planted. It also refuses the eight raw crossings among this round's eleven allowance probes and passes the three legal forms, so it makes no false refusal.
- The three `docs-gates-0` gates are green when re-run at the head, and the two reader classifications are sound.
- The all-fabric identity on six shapes and the placement figures match the receipts.

One MINOR stays open. Ruling 6715535566 item 5 ("say so where it is defined") is not carried. `syn/ooc/pp_placement.py` still defines `f0-f4` as a live placement, with no statement that it is dead until the flip. The verdict is NEGATIVE on that one item alone.

## Findings

### F-1 MINOR: the `f0-f4` placement is not marked dead where it is defined

`[R792] MINOR Conformance, Docs - syn/ooc/pp_placement.py:14,43; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192,212-220 - ruling 6715535566 item 5 not carried into the source`

- **Authority.** Ruling issuecomment-6715535566 item 5 says: "`pp_placement.py` `f0-f4` (item 6): ruled dead. Say so where it is defined. It is removed at the flip (S13), together with the all-fabric placement." The item names no other stage, unlike items 1, 2, 4 and 6. The S6 assignment (issuecomment-6712890110, item 6) gives `pp_placement.py` to this lane.
- **Evidence.**
  - `syn/ooc/pp_placement.py` is unchanged by the PR (it is not in `git diff --name-only a9d69c77..526f937c`).
  - `:14` still lists `PLACEMENTS = ("all-fabric", "f0-f4", "full-split")`, and `:43-48` give `f0-f4` live limits, with no statement of its status.
  - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192` and `:212-220` still present an `f0-f4` row and a runnable `--placement f0-f4` recipe.
  - The statement exists only in the PR body ("`pp_placement.py`'s `f0-f4` is ruled dead until the flip", Known limitations), and PR text is not where the placement is defined.
  - The author's handoff (section 5) and REVIEW READY (issuecomment-6717994137) say it was left out deliberately, because the round was held to the findings.
- **Impact.** The tree still offers a ruled-dead measurement population as a selectable placement, with live limits and a recipe. A later lane or integrator can measure it, or depend on it, with nothing at the definition to say the owner has retired it. The decision lives only in an issue comment and a PR body that are not durable repository knowledge (AGENTS.md section 2).
- **Required outcome.** Where `f0-f4` is defined in `pp_placement.py`, a comment states that the placement is ruled dead and is removed at the flip with the all-fabric placement. Per the owner's comment rule it cites `#665`, not the ruling's comment ID. The recipe page's `f0-f4` row does not present the placement as live without that status.
- **Verification.**
  - Re-read `pp_placement.py` at the new head, at the `PLACEMENTS` definition and the `f0-f4` branch of `limits`.
  - Re-read the recipe page's `f0-f4` row.
  - `python3 scripts/check_py_idiom.py` and `check_doc_style.py` stay green, and `syn/ooc/pp_placement_selftest.py` is unchanged and passes.

### Suggestions (optional, no lens effect)

- **S-1 (Tests).** The bench's own names still drop the units that the DUT boundary now carries.
  - The port `p_pt_offset0` (`tb/verilator/milan_dp/tb_split_top.sv:78`), and the nets `pub_idle_slope`, `fw_pt_offset`, `d_idle_slope` and `d_pt_offset` (`:102`, `:117`, `:194`, `:202`).
  - These are not DUT boundaries, and the naming ratchet passes (`receipts/gates/measure_naming.log`). Renaming them to `_ns` and `_bps` would keep the bench consistent with R791-F1's fix.
- **S-2 (Tests).** A refused clock pin is labelled with a Yosys internal net that carries the temporary path. For example, `flop fw_r's CLK reads $and$/tmp/split-cdc-se76b2el/top.v:523$106.Y` (`receipts/cdc-allowance-probes.log`, last probe).
  - The refusal is correct, but the words vary run to run. Naming the driving cell's type would make the message stable enough to anchor a plant.
- **S-3 (Tests, carried from R792-1 S-1).** The split leg still does not exercise the `EDIT` window, the counter-change and face events or the GM event.
  - R791's seven mutants of those paths (E1-E3, G1, G2, C1, W1) still survive with `checks: 66 failures: 0` (`receipts/r791-split-reviewer-mutants.log`).
  - The ruling assigns this to S6b's two-placement comparison, and the PR body and the suite README say so.
- **S-4 (Robustness, carried from R792-1 S-3).** `KL_mbx_cdc_window.sv` still drops a request edge that rises while the previous transfer waits for its handshake. This is unchanged by the delta and reachable only past the window's wait bound.
- **S-5 (RTL, measurement).** The split image places with WNS -0.021 ns over 22 endpoints (post-placement estimate, not routed).
  - The worst path is on the 100 MHz system clock inside `KL_mbx`'s event block: `u_evt/gm_pend_r` to `rec_r`, 18 logic levels.
  - The delta does not cause it, since `KL_mbx` is not in the delta. S9's routed image should watch that path.
- **S-6 (Tests).** `split_mutants.py:139` no longer bounds a run by wall clock.
  - The leg's waits are cycle-bounded (`wait_for(..., 8000)` and `20000`), and the hosted job carries its own timeout. A hung mutant therefore needs an unbounded loop in the model.
  - I accept the change, which brings the file under the ratchet's three wall-clock files. It is noted only so a later reader knows it was weighed.

No RESIDUE item is raised in this round. The delta's new source comments carry no lane label, review round, reviewer ID or issue-comment ID: a scan of every added non-Markdown line in `a9d69c77..526f937c` finds only the algorithmic "round" of the identity tool and the bench's `round` loop variable.

## Prior findings, each resolved or retained at this head

| Finding | Round 1 severity, lens | Status at `526f937c` | Evidence (this round's own runs unless stated) |
|---|---|---|---|
| R791-F1 units in two boundaries | MAJOR RTL, Tests | **Resolved** | The ports are `i_ctl_pub_idle_slope_bps` and `i_ctl_pt_offset_ns` (`milan_datapath.sv:714,731`). Four `KL_mbx_cdc` ports carry the same units (`:64,80,152,166`), as do every SoC table and instance keyword (`receipts/split-port-names.log`: 80 split ports, 16 instance keywords, 0 misses) and the bench bindings. `measure_naming.py --check` PASS, 95 recorded (`receipts/gates/measure_naming.log`). No naming-ratchet file is in the PR's diff, so there is no exclusion. The split leg passes, and hosted `docs-gates-0` succeeded at this head (`receipts/hosted-check-runs.tsv`). Gate 23m: author receipt `gates/test-builder-require-rv32.log`, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, as in round 1). |
| R791-F2 firmware boundary | MAJOR Tests, Docs | **Resolved** | R791's `ctrl_boundary_probe.py`, unchanged: "0 unclassified", and "the self-test's 175 (misbehaved 0); the README states 175" (`receipts/r791-ctrl-boundary-probe.log`). The one edit under `sw/firmware/ctrl/` is `README.md:255`, and the PR body states it. Hosted `firmware-boundary` and `firmware-verilator` were still queued at review time. |
| R791-F3 tap tuples and declaration encoding | MINOR Tests | **Resolved** | R791's `split_reviewer_mutants.py`, unchanged: T1, T2 and D1 CAUGHT by named checks (`receipts/r791-split-reviewer-mutants.log`). The leg's `check_tap` (`sim_split.cpp:522`) covers six accepted classes and five refusals. I checked them against IEEE 1722.1-2021 and IEEE 1722-2016 Annex B: 0x22F0 with 0xFA, 0xFB, 0xFC and 0xFE; MAAP at 91-E0-F0-00-FF-00. I checked the group addresses against IEEE 802.1Q: MSRP 0x22EA at 01-80-C2-00-00-0E, MVRP 0x88F5 at 01-80-C2-00-00-21. |
| R791-F4 drop counter cannot count | MINOR RTL, Robustness, Tests | **Resolved in the split.** The wrapper's Issue is a manager duty. | RTL: `KL_ctrl_split.sv:176-191,232`. I read it against `third_party/verilog-axis/rtl/axis_fifo.v:261-300`: `overflow_reg` pulses for one cycle after the last beat of a frame dropped for full, oversize or ongoing drop, and `last_kept_r` is written on that same edge from that same beat, so the two align. A runt (HEAD0 with last) and a refused frame (HEAD1 marked bad) record 0. A frame kept at HEAD1 or in BODY records 1. Saturation is at `:342`. Leg on round 1's tap: 3 FAIL, `65 handed out, 0 counted lost` (`receipts/split-leg-old-tap.log`). At the head: `108 offered, 65 handed out, 43 counted lost`, 66 checks, 0 failures (`receipts/split-leg.log`). R791's drop probe: `100 offered, 64 handed out, rx_drops_o 36` (`receipts/r791-drop-probe.log`). Mutants: 22 of 22 caught, the four drop-count arms among them (`receipts/split-mutants.log`). The `KL_pp_shadow` twin is untouched and has no Issue yet (see Pending manager duties). |
| R791-F5 = R792 T-1 CDC check exemption | MINOR Conformance, Tests, Docs | **Resolved** | `split_cdc_check.py:72-85,146-149,212-240`. The self-test passes: 253 sinks, 12 of 12 plants refused (`receipts/split-cdc-selftest.log`). R791's `cdc_plants.py`: "raw crossings the check let through: 0". My round 1 `cdc_check_probes.py`: "departures: 0" (both receipts here). This round's 11 allowance probes are 0 departures, listed below. The docstring (`:4-49`), `MAILBOX_SPLIT.md:1428-1440` and the suite README claim no more than the check does. |
| R792 D-1 stale pages | MINOR Docs | **Resolved** | Re-read at the head: `MAILBOX_SPLIT.md:826-832` (the split reads the block through `KL_mbx_cdc`), `MARK_II_AREA_PLAN.md:423-425` (the SoC builds the split datapath, and there is no `KL_pp_shadow` or `KL_maap` at `CTRL_SPLIT_P = 1`), and `CLOCK_DOMAINS.md:244-245` (both crossings, with their primitives and FIFOs). Doc style is OK, and the em dash gate finds 0 over 202 added lines (`receipts/gates/`). `sw/firmware/ctrl/plat/README.md:137` stays S2b's, as round 1 routed it. |
| R791-F6 / R792 R-1 labels and comment IDs | RESIDUE | **Resolved** | No "F-INT" remains in any file the PR changes. The remaining hits are in files the PR does not touch (`scripts/ci_events.py`, `sw/firmware/ctrl/test/*`), which belong to #746. `milan_datapath.sv:380` and `:5641` now read "(#665)". |
| R791-F7 / R792 R-2 REBOOT item and PR body | RESIDUE | **Resolved** | `MAILBOX_SPLIT.md:1751-1756` names S11 and the 0 tie, and `milan_datapath.sv:10143` ties `pp_reboot_req_w` to 0. The PR body gives each ruling's outcome (S9, S11, S13). |
| R792 R-3 counter word | RESIDUE | **Resolved** | `sim_split.cpp:382` reads "its STREAM_START counter". |
| R791-S1 SoC tables against the bench | SUGGESTION | Still holds | R791's `soc_vs_tb_wiring.py`, unchanged: 138 bindings, 0 disagreements (`receipts/r791-soc-vs-tb-wiring.log`). The 16 inline bindings, the renamed `m_pub_idle_slope_bps_i` among them, are covered by `split_port_names.py` and by the Vivado placement's clean elaboration. |
| R792 S-1, S-3 | SUGGESTION | Retained as S-3 and S-4 above | Unchanged by the delta. |
| R792 S-2 | SUGGESTION | Became R791-F4; resolved | See above. |
| R792 S-4, S-5 | SUGGESTION | Unchanged, optional | The all-fabric QoR is not re-measured after the `g_af_pp` rename. `split_population.py` keeps its MIT header. |

### This round's probes of the new CDC allowance (`scripts/cdc_allowance_probes.py`, `receipts/cdc-allowance-probes.log`)

Each probe edits a copy of `KL_mbx_cdc.sv` and runs the check's own `run()` on it. All 11 behave as the docstring's rule requires:

- **Clean, as they must be:**
  - the tracked text;
  - the hold written out as an `else`;
  - the taken bus mixed with a datapath flop.
- **Refused:**
  - the held bus on the gated mux's untaken input;
  - the taken bus mixed with a sys flop (`reads fw_send_q_r`);
  - an output reading the bus through the gated mux;
  - the capture selected by the acknowledgement's pulse;
  - the capture selected by a one-cycle-late copy of the pulse;
  - the capture selected by the pulse AND a datapath level;
  - another datapath flop taking the bus on the gate (`ev_dom_r reads m_fw_identify_i`);
  - a flop clocked by a gated datapath clock (`a clock that is not a clock input`).

## The three gates round 1 left red, and the two reader classifications

Re-run at the head, unpiped, on this clean clone (`receipts/gates/`):

- `check_port_contracts.py`: OK, with hdl 217 <= 217 undocumented.
- `check_py_idiom.py`: every ratchet at or under its budget (long function 9 <= 9, long module 10 <= 10, too many parameters 7 <= 7, undocumented 0, over-long line 0).
- `measure_test_evidence.py --check`: PASS, with 0 <= 0 unexplained DUT-source readers and 3 <= 3 wall-clock files.
- Also re-run: `measure_naming.py --check` PASS and `check_doc_style.py` OK. `check_em_dash.py --base a9d69c77` finds 0 over 202 added lines, run in the pinned renderer venv.

**Reader classifications** (`scripts/measure_test_evidence_readers.py:245-252`): **accepted**.
- `split_mutants.py` reads the RTL only to find each arm's anchor and plant it into a copy. Its verdict is the leg's named check failing in a completed run, as with the table's other mutation campaigns (for example `tb/verilator/mbx/mutants.py`).
- `split_cdc_check.py` reads the RTL through sv2v and Yosys, and judges domains by clock connectivity and port prefixes. Its one allowance (`fw_r`, `u_fw_req.dest_pulse`) is a named rule of its own table, not an expected value derived from the text.
- Both dispositions say what the tools do.

The refactors for the idiom ratchet keep their behaviour.
- Placement identity: the six digests of the round 2 head dump equal those of seven receipts (`receipts/identity-digests-compare.txt`). Those receipts are round 1's author dumps, R791-1's and R792-1's, all computed with round 1's tool, and round 2's base dump. So the refactored canonical form is byte-identical on every shape. The self-test passes 6 of 6 arms (author receipt).
- Population: 6 shapes and a 3-of-3 self-test (author receipts).
- `resmap_map.py` and `check_solution_docs.py`: the changes are line wrapping only.

## Identity and placement figures

- **All-fabric identity.** All six digests are the same in every receipt (`receipts/identity-digests-compare.txt`):
  - arty_4x4 `a69cdde2...`, arty_8ch `1a21d006...`, arty_current `96cabfad...`;
  - ax7101_1x1_tdm8 `b57dd8d2...`, ax7101_8x8 `a8ac6fe8...`, recipe `72214352...`.
  - This equals `a9d69c77` on all six shapes.
- **Placement** (a measurement, not a gate). Figures from `author-r2/receipts/vivado/`:
  - `utilization_place.rpt`, design state "Physopt postPlace", xc7a100tfgg484-2: Slice 14,383 of 15,850 (90.74 %); Slice LUTs 34,228 (53.99 %); registers 45,234; BRAM tiles 93 (75 RAMB36, 36 RAMB18); 5 DSP.
  - `timing_place-summary.rpt`: WNS -0.021 ns over 22 failing endpoints; WHS -0.248 ns over 431.
  - Synthesis: 35,982 LUT.
  - The hierarchy shows `milan_datapath` 18,584 LUT, `KL_ctrl_split` 226, `KL_mbx_cdc` 1,397, and no `KL_pp_shadow` or `KL_maap` row.
  - `run.txt` gives clone `526f937c`, Vivado rc 0, 0 ERROR and 0 CRITICAL WARNING.
  - All of these match the handoff and the PR body. The run is the author's. I did not re-run Vivado.

## Clean lenses, with evidence

- `[R792] PASS RTL - hdl/milan/KL_ctrl_split.sv:38-43,176-191,232,338-342 against third_party/verilog-axis/rtl/axis_fifo.v:217,261-300; KL_mbx_cdc.sv:56-90,144-215,231-282; KL_mbx_cdc_window.sv:32-45; milan_datapath.sv:373-385,711-781,9964-10021,10143; author vivado hierarchy - drop-count timing alignment, reset, saturation, the renames' widths and bindings, comment-only port docs, REBOOT tie`
  - The drop flag and its count are synchronous-reset, single-domain (`clk_i`) logic with no new crossing. Each rename keeps its width (32, and `S_C*32` / `CTRL_ENTRIES_P*32`).
  - Every SoC name resolves to a port (`receipts/split-port-names.log`). The placed block grew by 2 LUT and 9 FF.
  - The round 1 RTL verdict on everything else stands, since the delta changes only comments there.
- `[R792] PASS Robustness - KL_ctrl_split.sv:149-191 (runt at HEAD0, refused at HEAD1, kept at HEAD1 with last, BODY, oversize via DROP_OVERSIZE_FRAME, back-to-back last beats, reset); sim_split.cpp:565-606 - malformed and boundary frames under a full FIFO`
  - A refused or runt frame dropped for full is never counted: the refused-frame mutant is caught.
  - A two-beat kept frame is counted: the HEAD1 mutant is caught.
  - The count saturates at 255: the wrap mutant is caught, with 320 more frames offered.
  - Every kept frame is handed out or counted exactly once (108 = 65 + 43).
- `[R792] PASS Tests - sim_split.cpp:522-606, tb_split_top.sv:83-93,367-375, split_mutants.py:93-128, split_cdc_check.py:252-297, measure_test_evidence_readers.py:245-252 - each new test fails for the defect it names`
  - Leg: 66/0 at the head, and 3 failures on round 1's tap.
  - Mutants: 22/22, re-run here (`receipts/split-mutants.log`, 268 s).
  - CDC: 12/12 plants, plus 11 new probes and both reviewers' probe sets at 0 departures.
  - R791's mutants T1, T2 and D1 are caught. The seven that survive (S-3) are S6b's by ruling.

UNCLEAN at this head: Conformance (F-1) and Docs (F-1). The rest of each of those lenses was applied clean at this head:
- **Conformance:** R791-F1 to F5 and T-1 meet their verification steps; identity is unchanged on six shapes; the REBOOT tie and S11/S6b/S9 deferrals follow the ruling.
- **Docs:** D-1's three pages; `MAILBOX_SPLIT.md:1388-1398,1424-1442,1748-1758`; the suite README; the PR body's figures; the docs gates.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1) | ruling issuecomment-6715535566 items 1-7; assignment issuecomment-6712890110; each prior finding's verification step; identity receipts (7 files, all equal); `pp_placement.py`; PR body | R792-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| RTL | CLEAN | `KL_ctrl_split.sv` drop count against `axis_fifo.v`; the `KL_mbx_cdc` and `milan_datapath` renames; `KL_mbx_cdc_window.sv` port docs; `milan_soc.py` bindings (`split_port_names.py`, `soc_vs_tb_wiring.py`); Vivado hierarchy | R792-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Robustness | CLEAN | `KL_ctrl_split` tap and FIFO drop paths (runt, refused, HEAD1-kept, oversize, saturation, reset); the leg's burst checks; leg on round 1's tap; R791's drop probe | R792-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Tests | CLEAN | split leg (66/0), `split_mutants.py` (22/22), `split_cdc_check.py --selftest` (12/12), 11 allowance probes, R791 and R792-1 probes, R791 mutants, reader dispositions, the docs-gates-0 gates re-run | R792-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Docs | UNCLEAN (F-1) | `MAILBOX_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `CLOCK_DOMAINS.md`, `tb/verilator/milan_dp/README.md`, `sw/firmware/ctrl/README.md:255`, `PP_SHADOW_BASELINE_RECIPE.md:192-220`, `pp_placement.py`, the PR body; doc style, em dash | R792-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |

## What was executed (all at the exact head, on this review's isolated clone)

Tools: Verilator 5.050 (scoped pinned build, `--version` checked), sv2v 0.0.12 (pinned, `--numeric-version` checked), Yosys 0.66 (system). The commands are in `scripts/run_probes.sh`, with pins in `scripts/env.sh`. The prior reviewers' scripts were run unchanged from `1f33e530:review-evidence/665s6-r1/reviews/*/scripts/`.

| Run | rc | Result | Receipt |
|---|---|---|---|
| `split_cdc_check.py --selftest` | 0 | 253 sinks clean; 12 of 12 plants refused | `receipts/split-cdc-selftest.log` |
| `cdc_allowance_probes.py` (this round) | 0 | 11 probes, 0 departures | `receipts/cdc-allowance-probes.log` |
| R791 `cdc_plants.py`, unchanged | 0 | R1, R2 and R3 refused; 0 let through | `receipts/r791-cdc-plants.log` |
| R792-1 `cdc_check_probes.py`, unchanged | 0 | 5 probes, 0 departures | `receipts/r792-1-cdc-check-probes.log` |
| split leg (`build-split`, then the binary) | 0 | 66 checks, 0 failures; burst 108 / 65 / 43 | `receipts/split-leg.log` |
| split leg with round 1's `KL_ctrl_split.sv` | fails (as required) | 3 FAIL, 0 counted lost | `receipts/split-leg-old-tap.log` |
| `make split-mutants` | 0 | control passes; 22 of 22 caught | `receipts/split-mutants.log` |
| R791 `split_reviewer_mutants.py --jobs 8` | 0 | T1, T2 and D1 caught; 7 survive (S6b's) | `receipts/r791-split-reviewer-mutants.log` |
| R791 `ctrl_split_drop_probe.cpp` | 0 | 36 lost, 36 counted | `receipts/r791-drop-probe.log` |
| R791 `ctrl_boundary_probe.py` | 0 | 0 unclassified; 175 = 175 | `receipts/r791-ctrl-boundary-probe.log` |
| R791 `soc_vs_tb_wiring.py` | 0 | 138 bindings, 0 disagreements | `receipts/r791-soc-vs-tb-wiring.log` |
| `split_port_names.py` (this round) | 0 | 0 misses | `receipts/split-port-names.log` |
| docs-gates-0 gates (6) | 0 each | as listed above | `receipts/gates/*` |
| identity digest cross-check | - | 7 receipts, all equal | `receipts/identity-digests-compare.txt` |
| evidence manifest check | - | 1,122 entries, 0 mismatches, 0 unlisted | `receipts/evidence-manifest-verify.txt` |
| restore check | - | status empty (with ignored files); diff-index 0; index tree = HEAD tree; 6 gitlinks at HEAD; submodules clean | `receipts/restore-check.txt` |

## Hosted evidence at review time (read-only, not a verdict)

`receipts/hosted-check-runs.tsv`, read at the end of this round: 20 succeeded, `docs-gates-0` among them; 1 skipped (`Physical gPTP`, nightly and manual only); 31 queued or in progress (among them `firmware-boundary`, `firmware-verilator`, the Verilator and Yosys shards and `publication-census`); 0 failed. The manager owns hosted acceptance.

## Real limits

- I did not re-run the full sweep, the identity dump, the population check, the builder bank, the export compare, the hosted-job replay or the Vivado placement. I relied on the author's round 2 receipts for them. Their hashes match the evidence manifest, and the identity digests are also cross-checked against two independent round 1 reviewers' receipts.
- The Vivado figures are a post-placement estimate and were not routed. Timing closure is not known.
- Physical calibration was NOT RUN. Field skips are not hardware proof, and no hardware was used.
- No manager source bank exists at this head, and none is claimed. The current-dev merge candidate (source base `a9d69c77`, live dev `1eb5289d`) is the manager's, at the merge turn.
- The PR targets `dev-soft-core`, so no act run applies.

## Pending manager duties

- **Open the Issue R791-F4 required for `KL_pp_shadow`'s identical uncounted drop.** It is `drop_p_w = fw_valid_w & ~fw_ready_w` under `FRAME_FIFO`/`DROP_WHEN_FULL`, so the all-fabric `PP_DIAG[15:8]` reads 0 under a burst. No such Issue exists at review time: a search for "PP_DIAG drop" and "KL_pp_shadow drop count" returned none. AGENTS.md section 4 asks for it before merge.
- Route `sw/firmware/ctrl/plat/README.md:137` (the SoC described as idle) to S2b or S6b, as round 1 noted.
- Name the lane that carries F-1, if not this one.
- Confirm the exact-head hosted run completes, in particular `firmware-boundary`, `firmware-verilator`, `rtl-fast` and, after ready, `verilator-suites` and `yosys-portability`.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- S6b's CI job for `make split-cdc` (ruling item 6), so that the 12 plants run hosted.

R792-2 FINISHED
