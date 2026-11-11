[R828] NEGATIVE - exact head a91fb27dd39483e4694e193504da1dbe06208807

# R828-1: external review of PR #889 (issue #870, Mark II split S9, with S10 closed by D7 (a))

- Head: `a91fb27dd39483e4694e193504da1dbe06208807`, tree `29f1691c9d5b4fee0d316940754187bae737b137`, on `dev-soft-core` `1d6bf555`. That is 14 commits over three rounds.
- RTL head of the route: `a2690e68`. `git diff a2690e68..a91fb27d` touches only `docs/design/MAILBOX_SPLIT.md` and `docs/design/MARK_II_AREA_PLAN.md`.
- Authority: the body of #870, plus the manager's rulings issuecomment-6779934014 (round 2) and issuecomment-6788700325 (round 3). The standing timing rule is: logic cut, recipe unchanged, no pblocks, no floor exception.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs, all five, each against the artifacts named below.
- Verdict: NEGATIVE, on two MINOR findings.
  - F1: one identity rule of the gate has no planted negative control, and acceptance 6 asks for one.
  - F2: the new check ID `H0` reuses an existing check ID in the same suite.
  - RTL and Robustness are clean. Every timing cut was re-executed with its planted undo, and four extra reviewer probes were run.

## Order of reconstruction

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The #870 body, then its eight public comments: the author's TAKEN, STOP and REVIEW READY, and the manager's two rulings.
4. The mailbox contract files.
5. `git diff 1d6bf555..a91fb27d`, plus the history per round.
6. The published author packet (archive `2f0c3d52e360c931471713f40bf76466cb2f358f`, `review-evidence/665s9-r1/author/receipts`), with route, gates, r2, r3 and m8a2 read against the code.
7. The exact-head hosted check list.

Prior public review findings on this PR: none existed at this head. The PR has no review and no review comment. Its two issue comments are review-start notices, and #870 carries no reviewer finding. So nothing is retained or resolved.

## Executed evidence (this round, at the exact head)

Receipts are listed in MANIFEST.sha256. The scoped Verilator 5.050 identity was checked: `--version` printed `Verilator 5.050 2026-07-01 rev v5.050`. The host load average was about 190 to 255 throughout, so the mutant runs used one compile job per arm.

| Run | Result | Receipt |
|---|---|---|
| `make run-wb run-axil run-cosim run-if2` (tb/verilator/mbx) | rc 0: 546 / 591 checks (1 if), cosim 32, 553 / 598 (2 if), host model 490, 0 failures; equal to the author's figures | `receipts/mbx_suites.log` |
| The 16 timing-cut arms of `mutants.py`, both adapters where defined | 16 of 16 caught by the named check: read mux on the bus (R0), register read answered early (R0), GM snapshot at the request (G1), copier ignoring the registered read (Q20), read-back at the request (R1), head published one cycle early (H0, 169 words), ring port zeroed by the decision (W0, 0 of 20), verdict unregistered (V0 11 of 22, V1), select overlapping another (S0), window overlapping another (S0) | `receipts/mbx_mutants_cut_arms.log` |
| 12 further arms new or changed in this delta (read-side decodes, re-anchored fixtures, `axil-rdata-follows-port`) | 12 of 12 caught | `receipts/mbx_mutants_changed_arms.log` |
| Reviewer probes, not in the tree: rx_ready high in the verdict cycle; clean-up on the stale verdict; verdict registers loaded in the act cycle; second header word never written | All four caught (V0, V1, F1, D0, T0 and others) | `receipts/mbx_probes.log`, `scripts/probes.json` |
| `gen_mailbox.py --check`, `--crosscheck`, `--selftest` | 0 findings / 0 findings / 0 arms failed; the priority-chain plant is named by the cross-check; the three overlap arms are refused naming both registers (DA_GATE/F_CTRL at 0x0800, BOUND_EID/RX_HEAD at 0x0100, GM_LO/RX_HEAD at 0x0040) | `receipts/gen_mailbox_*.log` |
| `check_doc_style.py`, `check_doc_paths.py`, `git diff --check 1d6bf555..a91fb27d`, no en/em dash in any added line | OK (23 documents; 1086 cited paths) / clean / 0 | `receipts/doc_checks.log` |
| Hosted check snapshot at the exact head (13:35 CET) | 11 completed success, 1 skipped (Physical gPTP, schedule-only), 20 in progress, 18 queued: not yet evidence | `receipts/hosted_checks_snapshot.txt` |

The full 231-arm campaign was not re-run here. Under this host's load, one shard with controls exceeded the command time limit and was stopped after its four positive controls passed (`receipts/mbx_mutants_shard0of6.log`). The 28 arms re-run are the 43 the delta adds or changes, minus 15 fixture re-anchorings of existing checks. The author's 231-of-231 receipt is `r3/final/mbx-mutants.log`.

## The focus points

**(1) Recipe and identity gate.**
- `with_placement` (`sw/builder/endstation_builder.py:4450-4459`) sets `control: {placement}` and nothing else. That equals what `_load_control` returns for a file that states the key (`:4432-4442`).
- With `--write-rtl` or `--write-fragment`, the split recipe is refused (`:6095-6097`).
- The manifest (`sw/litex/check_image_identity.py:79-88`, written at `sw/litex/milan_soc.py:3006-3022`) binds: schema, placement, the ident (`soc._ident`, the same string SoCCore gets), VERSION from milan_csr.sv, the mailbox major and minor from the contract, the firmware path, sha256 and bytes, and the bitstream's `bitstream_binding` after a `--build`.
- In the routed image the bitstream is `null` (`r3/route/split-image_manifest.json`), because the route export does not `--build`. Gate 23p exercises the bound, unbound and other-bitstream rules on synthetic bitstreams only.
- All-fabric:
  - Its exports at `a2690e68` equal the base's, 21 of 21 files at 1x1 and 8x8, after normalising timestamps, the two tree roots and the lines of LiteX's comment-only hierarchy tree (`r3/gates/endpoint-compare-*.log`, script `r3/tools/endpoint_compare.py`).
  - The builder's outputs of the five shipped configs are byte-identical, 50 files (`endpoint/builder-all-fabric-{base,head}.sha256` agree).
  - Those outputs were taken at `ad2ed0e3`. `git diff ad2ed0e3..a91fb27d -- sw/builder configs sw/litex syn scripts` is empty.
  - No all-fabric build writes a manifest: the write is gated on `args.ctrl_mailbox` (`milan_soc.py:4963-4966`).
- The rule-by-plant map is `receipts/identity_gate_rule_coverage.md`, and finding F1 comes from it.

**(2) The KL_mbx cuts, against the mailbox contract.**
- `git diff --name-only 1d6bf555..a91fb27d` names none of `sw/mailbox/mailbox.yaml`, `KL_mbx_pkg.sv`, `VERSION`, `sw/firmware`, `KL_mbx_wb.sv` or `KL_mbx_axil.sv`. `gen_mailbox.py --check` is clean.
- **Registered read offset** (`hdl/milan/mailbox/KL_mbx.sv:1413-1430`):
  - `reg_rd_w` excludes the event ring and the receive rings.
  - A register read is acked at `rd_q_r`, two cycles after the request; a write or a ring read is acked in one.
  - `rsel_r` is 0 in the ack cycle because no request may come before the answer.
  - Both adapters hold `busy_r` until the ack (`KL_mbx_wb.sv:41-50`, `KL_mbx_axil.sv:72-150`), so they are latency-agnostic.
  - The two other direct drivers of the port (`tb/verilator/milan_dp/sim_split.cpp:93-197`, `twin_split.cpp:206-235`) wait on the ack.
  - The only read side effect, the GM snapshot, moved to the sampling cycle (`KL_mbx.sv:900`), and check G1 holds it.
  - Cost: +1 mailbox clock per register read, none per write or ring read.
- **Ring write port and published head** (`KL_mbx_rx.sv:495-530, 718-722, 736`):
  - The word decided in cycle t is written at the edge ending t+1. `head_pub_r` publishes `head_r` one cycle after the commit, so the HDR1 word is in the ring before the head covers it.
  - Free space still reads the unpublished `head_r`, which is conservative.
  - Check H0 counts every ring write under the published head on every clock; the early-publish undo fails it with 169 words.
- **Address and word without the decision** (round 3 (a)): only `wen_w` carries the hit, overflow, oversize and free-space terms (`:499-500`). The undo fails W0 (0 of 20 unwritten words seen at their slots).
- **Registered verdict** (round 3 (b), `:553-570, 665-668`):
  - The verdict registers load only at `fin_ready_w`. It acts in `VRD_S`, where `rx_ready_o` is low (`:221`).
  - `tokens_r` is decremented only at the commit and can only refill in between, so the verdict taken at FIN stays valid.
  - Cost: one mailbox clock per frame. The gap after a committed frame's last byte becomes 6 clocks, and 4 after any other frame (V1).
  - The undo fails V0 and V1.
  - My probes show V0 and V1 also catch a byte taken in the verdict cycle, a clean-up keyed on the stale verdict, and a verdict loaded one cycle late.
- **AND-OR read multiplexer** (round 3 (c)):
  - The skeleton generator emits 114 selects and one OR (`sw/mailbox/mailbox_skeleton.py:530-640`).
  - `check_read_onehot` refuses a byte offset that two terms share, naming both terms.
  - `read_mux_findings` requires the AND-OR form in the tracked skeleton.
  - The suite's S0 check reads every word of the window and counts any read in which two selects are set.
  - The priority-chain undo is functionally equivalent while the selects are one-hot, so it is caught structurally by the cross-check. A real select overlap fails S0, on the RTL and in the generator.

**(3) The route** (from the published receipts; read-out in `receipts/route_readout.txt`).
- One synthesis checkpoint, `alinx_ax7101_synth.dcp`, sha256 `6ae97a5d...334d9`: all three implementation scripts open the same path.
- Each script is the integrated script's tail from `# Add pre-optimize commands`, verbatim, with only the placement directive substituted. The recipe's own directive is untouched.
- All three meet WNS and WHS >= +0.030 ns at every corner:

| Directive | Slow WNS / WHS | Fast WNS / WHS |
|---|---|---|
| `ExtraPostPlacementOpt` | +0.274 / +0.102 | +1.636 / +0.036 |
| `ExtraTimingOpt` | +0.089 / +0.064 | +1.641 / +0.036 |
| `AltSpreadLogic_high` | +0.153 / +0.082 | +1.641 / +0.036 |

- Nets routed, with 0 routing errors in each:
  - `ExtraPostPlacementOpt`: 67,358 of 67,358;
  - `ExtraTimingOpt`: 67,354 of 67,354;
  - `AltSpreadLogic_high`: 67,333 of 67,333.
- The recipe directive's image: 29,377 LUT, 39,235 FF, 12,671 slices, 56 RAMB36 / 32 RAMB18 (72 tiles), 5 DSP.
- **On the reset and the recipe directive.** I judge routing the recipe directive from the checkpoint equivalent for this gate.
  - The checkpoint is the recipe session's own: `synth_design completed successfully`, then `write_checkpoint -force alinx_ax7101_synth.dcp`, both before the reset (`r3/route/split-synthesis-checkpoint-lines.txt`).
  - The post-synthesis commands are the recipe's, byte for byte: constraints re-sourced, `opt_design ExploreArea`, `place_design ExtraPostPlacementOpt`, `phys_opt`/`route_design`/`phys_opt AggressiveExplore`. Only `open_checkpoint` and the same 32-thread parameter are prefixed.
  - The result is not guaranteed bit-identical to an uninterrupted session. It is a genuine route of the unchanged recipe, though, and it is the only arrangement in the three rounds where all three directives share one checkpoint, which is what #818 and ruling item 5 ask for.
  - There is no in-session versus from-checkpoint pair on one netlist to compare against.
- The resource gate on the selected route exits 1 for RAMB18 +5 (27 to 32) against the all-fabric record. Its timing figures pass. This is published in `MARK_II_AREA_PLAN.md`; see "Pending manager duties".

**(4) S2's harness, recorded and not graded:**

| Point | T_svc misses, round 1 | Round 2 | Round 3 |
|---|---:|---:|---:|
| 1x1/1if | 34 | 36 | 36 |
| 8x8/2if | 63 | 63 | 63 |

- Round 2's two new 1x1 misses (`acmp.entity_available`, `acmp.get_tx_state`) are explained in the round 2 STOP comment.
- From round 2 to round 3 the same probes miss, and none moves by more than 0.001 ms (`r3/gates/budget-*-delta-r2-to-r3.txt`). The budget is owned by S2b (#810).

**(5) M8a-2 and D7 (a).**
- DDR3, main RAM and the three processor bridges are built only when `ctrl_mailbox` is off (`milan_soc.py:3449-3452, 3825-3828, 4718`). `--ctrl-mailbox --with-dram` is refused.
- 29,377 LUT is 8,663 below 38,040. 72 tiles is 49.5 below 121.5. The route is far from 300 LUT of the M9 bar, so D7's (b) is not triggered.
- The term, out of context, is 349 LUT / 93 FF at one interface (49 LUT over its 300 target, within 120 FF) and 754 / 151 at two. The close-out row is at `MARK_II_AREA_PLAN.md:1123`.
- The ledger rows asked by acceptance 3 are in the "M8a-2: the integrated split route" section of the same file.

## Findings

**F1 - MINOR - Tests, Conformance - `sw/builder/test_builder.py:23618-23705` (gate 23p) against `sw/litex/check_image_identity.py:175-176` - the manifest's ident versus the image's ident has no planted negative control.**
- Requirement/evidence:
  - #870 scope: "The identity gate refuses an image whose manifest, ident, firmware hash or placement disagree."
  - Acceptance 6: "Each identity mismatch ... ha[s] a planted negative control that makes the gate fail."
  - The rule that binds the manifest to the image it ships with is `claimed["ident"] != got["ident"]`, comparing against csr.csv's `config_identifier`. No plant fires it. The "split ident names no placement" plant edits `soc_ident`, whose one result feeds both the SoC and the manifest (`milan_soc.py:3014`), so the two still agree and only the last-word rule fires. No file plant edits the manifest's `ident`. No other test runs the gate.
  - The map is in `receipts/identity_gate_rule_coverage.md`. The schema-fields rule (`:168-170`) is likewise uncontrolled.
  - I could not re-execute gate 23p: no interpreter here imports migen, litex and litex_boards. This finding is therefore by reading, from the fixtures as written.
- Impact: deleting or inverting the manifest-ident comparison leaves every gate green. A manifest copied from another image with a different ident would then be accepted on its hashes.
- Required outcome: a plant that leaves the image's ident alone and changes the manifest's `ident`, which must fail the gate with `FINDING manifest:`. Optionally, also one for the fields rule.
- Verification: gate 23p lists the new plant, and a copy of the gate with lines 175-176 removed fails gate 23p.

**F2 - MINOR - Tests, Docs - `tb/verilator/mbx/suite.hpp:153-154` against `:958-963`; `tb/verilator/mbx/README.md:155,164`; `docs/design/MAILBOX_SPLIT.md:137` - the new check ID `H0` already names another check of the same suite.**
- Requirement/evidence:
  - Before this delta, `H0` was "an RX_TAIL ahead of RX_HEAD stores nothing" (base `suite.hpp:929-934`, README row "H0 to H2").
  - The delta adds a second, unrelated `H0`: "no receive ring word is written under the head the core sees".
  - The README's check table now has two `H0` rows. MAILBOX_SPLIT.md cites "its check H0", and the issue and its rulings refer to "the H0 check", which is now ambiguous.
  - Both appear as `[FAIL] H0 ...` in one run (`receipts/mbx_probes.log`). `receipts/check_label_h0.txt` has the evidence.
  - The mutant needles happen to use full labels, so grading is not wrong today.
- Impact: a failure, a mutant needle or a document cited by ID cannot be told apart. A short needle such as `"H0"` would be satisfied by the wrong check.
- Required outcome: one ID per check in the suite, with the new check under an unused ID, and the README, MAILBOX_SPLIT.md and the mutant needle following it.
- Verification: the labels grep shows each ID prefix used by one check family; `make` and `make mutants` stay green.

**S1 - SUGGESTION - Tests - `tb/verilator/mbx/mutants.py:167-170` - A5 no longer detects AXI4-Lite RDATA following the host port.**
- Because a register read's word is now held in `reg_rdata_r` until the next register read, the arm `axil-rdata-follows-port` is caught by F1's record LEN (a stale ring word), not by A5 "RDATA and RRESP hold with it".
- The defect is still caught. Stalling RREADY across a ring read inside A5 would restore that check's own power.

**R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:971` - net counts.**
- "Every routable net is routed in every round: 66,578 of 66,578, then 66,913 of 66,913, then 67,358 of 67,358" gives the recipe directive's counts. In round 3, `ExtraTimingOpt` and `AltSpreadLogic_high` route 67,354 and 67,333, all of them.
- Exact fix: "Every routable net is routed in every directive of every round, none with an error; at the recipe's directive, 66,578 of 66,578, then 66,913 of 66,913, then 67,358 of 67,358."

Comment rule: in the reviewed delta, no source comment shows a lane label, a lane name, a review round, a reviewer ID or an issue-comment ID. The `#665 S9` and `S13` plan-stage citations and the check IDs are not lane labels. Docs name rounds and rulings, which the rule allows.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #870 acceptance 1-6 and both rulings against `KL_mbx.sv:1413-1430`, `KL_mbx_rx.sv:495-570`, `mailbox_skeleton.py:530-640`, `check_image_identity.py`, `endstation_builder.py:4450-4459, 6095-6097`, `milan_soc.py:3006-3022, 3449-3452, 4718`; contract files unchanged; route, endpoint and S2 receipts of `r3/` | R828-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| RTL | CLEAN | `KL_mbx.sv` answer block, read decodes, GM snapshot and AND-OR mux; `KL_mbx_rx.sv` host read register, ring write port, `head_pub_r`, verdict registers, FSM and buckets; adapters `KL_mbx_wb.sv`, `KL_mbx_axil.sv`; route paths `r3/route/worst-paths.txt`, `signoff-all.txt` | R828-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Robustness | CLEAN | Back-to-back frames across every verdict (V0/V1 and four reviewer probes, all caught); reset values of every new register; the free space on the unpublished head; the host port's noise outside requests (BENCH_P); a request before the answer excluded by both adapters and both split benches; `--ctrl-mailbox --with-dram` and split `--write-rtl` refused | R828-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Tests | UNCLEAN (F1, F2) | `suite.hpp` G1/W0/V0/V1/S0/H0, `bench.hpp`, `tb_mbx_top.sv`, `suite_face.hpp` (refusals graded in the second request, nothing removed), `mutants.py` (28 arms re-run, all caught), `gen_mailbox.py --selftest`, gate 23p fixtures by reading | R828-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Docs | UNCLEAN (F2) | `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md` (figures checked against `r3/route` utilization, signoff and route-status), `tb/verilator/mbx/README.md`, `docs/ENDSTATION_BUILDER.md` row 34a, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`; doc style and doc path gates OK | R828-1 | a91fb27dd39483e4694e193504da1dbe06208807 |

## Real limits

- The route, endpoint, S2, split-boot, sweep and workflow results are the author's published receipts, read against the code. They were not re-run here: no Vivado, LiteX, builder or native bank ran in this round, and there is no manager source bank at this head.
- Gate 23p was not executed, because no LiteX interpreter was available. F1 is by reading.
- 28 of 231 mutant arms were re-executed, chosen as every timing-cut arm plus the changed read-side arms. The other 203 rely on the author's receipt.
- The M8a-2 runs that include the mailbox but are not the split boot were recorded before the round 2 and 3 cuts, and the rulings did not ask for them again:
  - `nvm_split_target --point 8x8` at `e16c1343`;
  - `check_nvm_capture` at `e16c1343`;
  - `nvm_capture_cpu` at `0f3c4756`.

  `nvm_cosim` is in the final-head sweep, and the split boots re-ran at `a2690e68`.
- "Byte-identical" for the all-fabric exports means equal after normalising timestamps, roots and comment-only tree lines. The builder's tracked outputs are raw-identical.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- Process disclosure. Early in the round I started a detached full `mutants.py --jobs 12` campaign. It used the driver's default of four compile jobs per arm, so while it ran this round exceeded its 16-job cap.
  - Its rc file later read 0, but its log was deleted unread during receipt clean-up. It is not claimed as evidence, and its rc file is not published.
  - It also added to the host load that slowed the other runs. No campaign of this round is still running.

## Pending manager duties

- Hosted exact-head contexts: at the snapshot, 20 were in progress and 18 queued. The physical gPTP job is skipped by schedule.
- The current-dev merge candidate (source base `1d6bf555`, live dev `46c971fa`), with the builder and native banks, at the merge turn.
- A decision on the resource gate's RAMB18 +5 exit 1 on the selected split route, whose re-baseline the area plan leaves to M9.
- Whether the M8a-2 NVM runs need re-running on the cut RTL.
- Carrying R1 to the residue checklist.
- Merge needs two independent positive reviews and the full completion bar. This round is NEGATIVE on F1 and F2.

R828-1 FINISHED
