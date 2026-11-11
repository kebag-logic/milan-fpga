[R827] NEGATIVE - exact head a91fb27dd39483e4694e193504da1dbe06208807

# R827-1: internal cleared-context review of PR #889 (issue #870, Mark II split S9)

- Head reviewed: `a91fb27dd39483e4694e193504da1dbe06208807`, tree `29f1691c9d5b4fee0d316940754187bae737b137`, on `dev-soft-core` `1d6bf555` (fourteen commits: round 1's eight, round 2's four, round 3's two).
- Role: internal independent reviewer, cleared context, own detached clone. No source edit, commit, push or GitHub write. Disposable probes only, restored and verified (`receipts/restore_verification.txt`).
- Verdict: **NEGATIVE**. Two MINOR findings are open: F1 (Tests) and F2 (Tests, Docs). Nothing BLOCKER or MAJOR was found. The RTL timing cuts, the route, the identity gate's refusals, the all-fabric endpoint and the D7 (a) accounting all hold against the code and the receipts. Both MINORs are test or test-labelling gaps, each with a small fix.

## Authority reconstructed (in order)

1. `AGENTS.md` and `CONTRIBUTING.md` (the lens list, the severities, the comment rule given by the manager's brief).
2. Issue #870's body: scope, acceptance 1 to 6, out of scope.
3. The manager's rulings on #870. Round 2 is issuecomment-6779934014: option (a), logic cut, recipe unchanged, no pblocks, no floor exception; register the read path and the ring write; a head never before its data; a mutant per cut; STOP if the floor still misses. Round 3 is issuecomment-6788700325: cuts (a), (b) and (c); the verdict's cost per frame and a back-to-back proof; an AND-OR built by the generator with an overlap check; WNS and WHS >= +0.030 ns on one directive from one checkpoint; S2 recorded, not graded.
4. The authorities linked from those: `docs/design/MARK_II_AREA_PLAN.md` (Target and M8a-2), `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` section 4, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (the #818 best-of-three procedure), `sw/mailbox/mailbox.yaml`.
5. `git diff 1d6bf555..a91fb27d` and the per-commit history.
6. The public author packet at `2f0c3d52` (`review-evidence/665s9-r1/author/receipts`, mainly `r3/`), and the executor and manager comments on #870 and #889.

No private author material, lane scratchpad or other reviewer's report was read. **Prior public review findings: none.** PR #889 carries only the two review-start comments, and #870 carries only executor and manager comments. There is nothing to resolve or retain.

## Findings

### F1 - MINOR - Tests - `sw/builder/test_builder.py:23667-23704` (`_identity_file_plants`), `:23707-23750` (gate 23p); `sw/litex/check_image_identity.py:208-225`

- **Title.** The identity gate's bound-bitstream branch has no positive control. A gate that refuses every bound bitstream passes gate 23p.
- **Authority and evidence.**
  - Scope: the image manifest records the bitstream's hash. AGENTS Tests lens: positive, negative and boundary behaviour are covered, and each test can fail for the defect it claims to detect.
  - Both good images in 23p carry `"bitstream": null`. The split image is exported without `--build`, and the route's manifest `r3/route/split-image_manifest.json` is also null.
  - So `_bitstream_rules` returns before its comparison on every passing image.
  - The two bitstream plants are both negative: no bitstream bound, and another bitstream than the bound one.
  - Reviewer probe (`receipts/probe_bitstream_positive_23p.log`): `check_image_identity.py:224` `if have != bound:` was replaced by `if True:`, so every bound bitstream is refused. Gate 23p still reports `ALL GATES PASS`.
  - The comparison itself is correct by inspection. The binding survives the manifest's JSON round trip unchanged (`receipts/probe_bitstream_roundtrip.log`).
- **Impact.** `milan_soc.py:4964-4966` runs the gate on every split `--build`, with the bitstream bound. That is the shipping path, and no test covers it. A regression in the bound-and-matching branch would refuse every built split image, or a wrong binding would pass. The lane's suite would see neither. No split bitstream was built in this lane, so the branch has never run positively anywhere.
- **Required outcome.** Gate 23p grades a split image whose manifest binds a bitstream that the image's `gateware/*.bit` matches, and requires it to pass (exit 0). A fixture bitstream, as the existing plants use, is enough.
- **Verification.** Gate 23p passes at the fixed head. The `if True:` mutant above, or `have == bound`, fails 23p on the new control.

### F2 - MINOR - Tests, Docs - `tb/verilator/mbx/suite.hpp:153-154` against `:958-963`; `tb/verilator/mbx/README.md:155` and `:164`; `docs/design/MAILBOX_SPLIT.md:137`

- **Title.** Round 2 named its head-publication check `H0`, an ID the suite already uses for "an RX_TAIL ahead of RX_HEAD stores nothing".
- **Authority and evidence.**
  - `suite.hpp:958-963` (base `1d6bf555`) labels three checks `H0 ...`: the RX_TAIL guard. `suite.hpp:153-154` (commit `3ba76ae7`) adds two more `H0 ...` checks: no ring word written under the published head.
  - The README's check table now has two `H0` rows, `| H0 to H2 | a wrong host counter ...` and `| H0 | on the RTL only, last, ...`.
  - Its mutant table reads `rx-tail-unguarded` → "H0, nothing stored", and `rx-head-published-one-cycle-early` → "H0, no ring word written under the head".
  - `MAILBOX_SPLIT.md:137` cites "its check H0" for the head rule.
  - AGENTS Docs lens: the PR and the docs give a cold reviewer enough to find the evidence. Tests lens: each test is identifiable as the one that detects its defect.
- **Impact.** A reader following "check H0" from the design doc or the mutant table cannot tell which of two unrelated checks is meant. The ruling's own proof ("a test that fails when the head is published one cycle early") is named by an ambiguous ID. The mutant needles use full label text, so grading is not affected today. Any short-ID reference (docs, receipts, future needles) is ambiguous.
- **Required outcome.** Each check ID in the mailbox suite names one check. Rename the new check, or the old one, to a free ID, and use the same ID in `suite.hpp`, `mutants.py` (needles), `tb/verilator/mbx/README.md` and `MAILBOX_SPLIT.md`.
- **Verification.** No two different checks in `suite.hpp` and `suite_face.hpp` share an ID prefix. `make -C tb/verilator/mbx` and `make mutants` stay green with every arm caught.

### R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:971`; the REVIEW READY comment and PR body ("67,358 of 67,358 nets routed")

- **Wording only.** "Every routable net is routed in every round: ... then 67,358 of 67,358" gives the recipe directive's count as the round's.
- **Receipts.** `r3/route/split-*/alinx_ax7101_route_status.rpt` shows 67,358 of 67,358 (`ExtraPostPlacementOpt`), 67,354 of 67,354 (`ExtraTimingOpt`) and 67,333 of 67,333 (`AltSpreadLogic_high`), each with 0 routing errors. The claim that every net is routed is true on every directive.
- **Exact fix.** In `MARK_II_AREA_PLAN.md:971`, write "then 67,358 of 67,358 at the recipe's directive (67,354 and 67,333 at the other two)". In the PR text, write "every net routed on every directive (67,358 at the recipe's)".

### S1 - SUGGESTION - Docs - `docs/design/MARK_II_AREA_PLAN.md:1010`

"No path from the receive block, `KL_mbx/u_rx`, is among the 15 worst at the bus clock in any directive" rests on the signoff timing reports. The packet holds only their sha256. `r3/route/worst-paths.txt` gives one path per clock. Optional: publish the path headers of the 15 worst bus-clock paths per directive. The gate's own figures are published and do not depend on this sentence.

### S2 - SUGGESTION - RTL, Robustness - `hdl/milan/mailbox/KL_mbx_rx.sv:180`, `:665-668`

The frame FSM went from a full 2-bit encoding to `logic [2:0]` with five states. The three unused codes have no transition out, and `rx_ready_o` is 0 in them, so only a reset leaves them. That state is unreachable in correct operation, and the synchronous reset recovers it. Optional: a default transition to `RECV_S`, if the project wants upset recovery.

## Focus items, checked against code and receipts

### (1) The builder recipe and the identity gate

- **The recipe.** `endstation_builder.py:4450` `with_placement` sets only `control.placement`, and `build()` refuses `--write-rtl` and `--write-fragment` under `split`. I ran gate 23o: all 5 configs load to the file stating the key, the 8 shape artifacts are byte-identical, and no tracked file changes. The refusals and both planted recipes are caught. Gate 23n also passes (`receipts/builder_gates_23n_23o_23p.log`).
- **The ident and the manifest.** `milan_soc.py:2998-3023`: the ident ends in `split` for a split build, and the all-fabric ident is unchanged. `write_image_manifest` records the schema, placement, ident, VERSION, the mailbox major and minor (from the contract), the firmware ELF's sha256 and bytes, and the bitstream binding after `--build`. It then runs the gate on the image.
- **The gate.** `check_image_identity.py` cross-checks:
  - the manifest against `csr.csv`'s ident, the `milan_csr.sv` and `KL_mbx_pkg.sv` the Vivado script reads, and the firmware's sha256 and rom words against the rom bank init files;
  - the bitstream payload and part;
  - `CTRL_SPLIT_P` and the mailbox presence;
  - DDR3 (`main_ram`, `ddrphy` or `sdram`, `ddram` pads).
- **Gate 23p.** I ran it here: both good images pass, `--ctrl-mailbox --with-dram` is refused, and the 12 planted images each fail by their kind. That meets acceptance 6. F1 is the one gap.
- **All-fabric unchanged.**
  - Structurally, the mailbox sources are added only under `--ctrl-mailbox` (`milan_soc.py:2877-2893`, `:3198`). The DDR3 and memory-bridge removal is gated on `ctrl_mailbox`. VERSION, `mailbox.yaml`, `KL_mbx_pkg.sv`, firmware and configs are untouched by the diff.
  - Receipts: `r3/gates/endpoint-compare-*.log` show 21 of 21 export files identical at 1x1 and 8x8 after the normaliser (timestamps, roots, the comment-only hierarchy tree). The tracked builder outputs' byte identity is from round 1.

### (2) The KL_mbx timing cuts and the contract

**Registered read offset, +1 clock per register read.** `KL_mbx.sv:182-190`, `:1405-1437`.

- `rd_off_r` is captured only on `reg_rd_w`, and `ack_r <= (host_req_i && !reg_rd_w) || rd_q_r`. A write and a ring read still take 1 cycle; a register read takes 2.
- The only read side effect, the GM_HI and DOMAIN snapshot, moved to `rd_q_r` (`:898-903`). It is sampled in the cycle `reg_rdata_r` samples GM_LO.
- The bound-talker read-back is read at `hrk_r`, registered at the request, and the copier yields that cycle (`KL_mbx_rx.sv:270-314`).
- `KL_mbx_wb` holds `busy_r` until ACK, so the variable acknowledge needs no adapter change (Wishbone B4).

**Ring write port and published head.** `KL_mbx_rx.sv:488-530`, `:719-721`, `:736`.

- The port is registered, and `rx_head_words_o` is `head_pub_r`, which is `head_r` a cycle later. The HDR1 word decided at the commit lands at the next edge, and the core sees the head one cycle after that. The IRQ pending bit reads the published head.
- Free space still uses the internal `head_r`, which can only be ahead of the published head.
- Check H0 (see F2 on its ID) and the author's mutant hold. My extra probe `p12`, which publishes the head in the commit cycle itself, fails H0 with 169 words.

**Port address and word free of the write decision (round 3 (a)).** `wen_w` alone carries the channel, the free space and the maximum frame size; `waddr_w` and `wdata_w` follow `st_r` alone.

- W0 bites on the author's arm (both zeroed).
- It also bites on my two narrower probes: `p15` zeroes only the address (Wishbone), and `p16` only the word (AXI4-Lite).

**Verdict registered one clock before it acts (round 3 (b)).** `KL_mbx_rx.sv:532-572`, `:665-684`.

- The verdict is captured into `vd_*_r` at `fin_ready_w`. `VRD_S` acts on RX_DROP, RATE_DROP, FILTER_MISMATCH, the clean-up and HDR0. `rx_ready_o` is 1 only in `RECV_S`, so no byte is taken in either verdict cycle.
- Every term the verdict reads holds between FIN and VRD, because no byte is taken. Tokens can only refill in that cycle, and the commit decrements them at HDR1, after a nonzero sample. So the bucket cannot underflow.
- Cost: +1 mailbox clock per received frame, 6 clocks after a committed frame and 4 after any other, and none per host access.
- Throughput check (mine): a minimum 60-byte frame plus 6 clocks is 660 ns at 100 MHz, against 672 ns of line time per minimum 1 GbE frame, so one interface is still kept up with.
- V0 and V1 bite on the author's arm, and on my probes `p1` (a byte taken in `VRD_S`: V0 counts and records wrong, V1 3 against 6 and 4) and `p3` (clean-up moved to the verdict cycle: V0 records wrong, F1 LEN 0).
- `p17` re-reads the bucket in the acting cycle. It survives because it differs only when a refill tick falls in that one cycle, which no check targets. Both samplings are defensible and the RTL's is the documented one. This is not a finding.
- `p18` (verdict registers sampled every cycle) is equivalent by construction.

**AND-OR read multiplexer, generated (round 3 (c)).**

- `mailbox_skeleton.py:530-660`: `read_terms` computes each term's offsets from the contract, `check_read_onehot` refuses a shared offset by name, and `read_mux_findings` requires the AND-OR form in the tracked skeleton. `KL_mbx.sv:987-1227` holds 114 selects and a pure OR of ANDed words.
- I ran `gen_mailbox.py --check --crosscheck`: 0 findings. `--selftest`: 0 arms failed. Those include the priority-chain plant, the dropped-select plant and the three window-overlap arms, each naming two registers and an offset.
- S0 reads the whole window at 1 and 2 interfaces through both adapters. It bites on the author's two overlap arms.
- `p19` (BOUND_EID's select without `bnd_eid_vld_w`) is caught by Q17. `p20` (`rd_off_r` loaded every cycle) is equivalent, because `reg_rdata_r` samples it before the next load. It is not a defect.

**Contract unchanged.** `mailbox.yaml`, `KL_mbx_pkg.sv`, the register map, the minor, VERSION (`milan_csr.sv`), the firmware and the configs do not appear in `git diff --stat 1d6bf555..a91fb27d`. `gen_mailbox.py --check` reports 0 drift.

**Suite and mutants (run here, pinned Verilator 5.050; identity verified).**

- `make`: 546 / 591 / 553 / 598 checks, 0 failures; cosim 32; model 490; 12 of 12 quick arms caught (`receipts/mbx_make_all.log`).
- `mutants.py --jobs 3`: 4 positive controls, then **231 of 231 caught** (`receipts/mbx_mutants.log`).

### (3) The route

All three #818 directives open the same `alinx_ax7101_synth.dcp`. It is 60,113,078 bytes, sha256 `6ae97a5d...34d9`, written by the recipe session at its line 3311. The three scripts differ only in the `place_design -directive` line (`r3/route/split-*/baseline_implementation.tcl`).

From `signoff.txt` and `timing-summary-*`:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Nets routed, all of them, 0 errors |
|---|---|---|---|
| `ExtraPostPlacementOpt` | +0.274 / +0.102 | +1.636 / +0.036 | 67,358 |
| `ExtraTimingOpt` | +0.089 / +0.064 | +1.641 / +0.036 | 67,354 |
| `AltSpreadLogic_high` | +0.153 / +0.082 | +1.641 / +0.036 | 67,333 |

- Every corner of every directive is >= +0.030 ns on both WNS and WHS, and the 0 C and 85 C models read the same. Acceptance 1 and the round 3 ruling's gate are met.
- **Figures.** At `ExtraPostPlacementOpt`: 29,377 LUT, 39,235 FF, 12,671 slices, 56 RAMB36 and 32 RAMB18 (72 tiles), 5 DSP. That is 8,663 LUT under 38,040 and 49.5 tiles under 121.5. Block RAM is 53.3 % of the part, under 60 %. The rom and sram banks are 39 tiles, inside the 56-tile allocation.
- The resource gate exits 1 for RAMB18 +5 alone (`gate-check-shipping-view.log`). This is disclosed, and it is not an acceptance item.

**Is the recipe directive, routed from the checkpoint after the host reset, equivalent?** Procedurally yes.

- `prep_directives3.py` takes the recipe's own integrated script from `# Add pre-optimize commands` to its end, verbatim. That tail includes the clock constraints, `opt_design`, the timing grade, placement, `phys_opt`, routing, the full-split census and the reports.
- It opens the synthesis checkpoint the interrupted session had already written. That is exactly how `PP_SHADOW_BASELINE_RECIPE.md:142-180` routes the other two directives, so all three now come from one file, which is what the "one checkpoint" rule asks for.
- What a reopened checkpoint cannot carry is session state set before synthesis in the script's head. That head is only hashed in the packet, not published. So bit-for-bit identity with an uninterrupted session is not shown.
- It does not matter for the verdict: all three directives meet the floor, so the gate is met whichever run is taken as the recipe's.

### (4) S2's harness T_svc tallies

These are recorded, not graded; S2b (#810) owns the budget. The author receipts at `a2690e68` are `r3/gates/budget-*-delta-r2-to-r3.txt`:

- 1x1/1if: 36 misses (36/141 instances, 15/81 paths), the same probes as round 2, each within 0.001 ms.
- 8x8/2if: 63 (63/182, 31/129), equal to round 2.

Against round 1 and the base, 1x1 moved from 34 to 36: `acmp.entity_available` 8.723 → 10.434 ms and `acmp.get_tx_state` 9.454 → 11.185 ms. Round 2 disclosed this on #870. It is recorded here, not graded. The harness was not re-run by the reviewer: there is no RV32 or LiteX split build in this review.

### (5) M8a-2 and D7 (a)

- **M8a-2.** DDR3, main RAM and the three processor memory bridges are removed under `--ctrl-mailbox` only (`milan_soc.py`, the `if not ctrl_mailbox:` block and `:4599`). The route's census holds `KL_mbx` and `KL_gptp_shadow`, and none of the wrapper and the five engines (`baseline_placement.tsv`). The integrated route goes through the full-split recipe.
- **D7 (a), out of context, recomputed from `r3/ooc/*/util_hier.rpt`.**
  - 1 interface: 5,913/8,827 against 5,564/8,734, giving **349 LUT / 93 FF**.
  - 2 interfaces: 8,969/14,709 against 8,215/14,558, giving **754 / 151**.
  - The OOC sources' `KL_mbx_rx.sv` and `KL_mbx.sv` sha256 equal the reviewed head's.
- **The close-out row.** "49 LUTs over its 300 LUT target", accepted as measured. The route is 8,663 LUT under the M9 bar, far from the 300-LUT trigger for D7 (b).
- **Area-plan arithmetic** checked: 75 LUT, 6 FF and -228 slices against round 2; 8,282 under 37,659; 6,890 under 36,267; the percentages.

## Lens results (artifact-specific)

```text
[R827] PASS Conformance — #870 acceptance 1-6 and rulings issuecomment-6779934014 / -6788700325 against r3/route/signoff-all.txt, r3/route/split-*/{timing-summary-*,route_status.rpt,baseline_utilization.rpt}, r3/gates/endpoint-compare-*.log, r3/ooc/*/util_hier.rpt, MARK_II_AREA_PLAN.md:954-1135, and the gates 23n/23o/23p and gen_mailbox --check/--selftest runs here — every criterion and ruling item met; contract files untouched
[R827] PASS RTL — hdl/milan/mailbox/KL_mbx_rx.sv:180-314,488-572,580-742 and KL_mbx.sv:182-190,898-903,987-1227,1405-1437, KL_mbx_wb.sv busy/ack — clock/reset (all new state reset synchronously), FSM VRD_S path, widths, read-back port arbitration, ack timing, GM snapshot coherence, head-before-data ordering; no defect (S2 optional)
[R827] PASS Robustness — the same RTL under reviewer probes p1, p3, p12, p15-p20 (receipts/r827_probes_table.txt) and the suite's noise-on-port bench: back-to-back frames across both verdict cycles, overflow and oversize drains (W0), reset clear of the new registers, refill between FIN and VRD (p17, analysed), host-port noise between requests (p20, equivalent); no defect
[R827] MINOR Tests — sw/builder/test_builder.py:23667-23750 — F1, the bound-bitstream branch has no positive control (planted refusal survives 23p)
[R827] MINOR Tests — tb/verilator/mbx/suite.hpp:153-154 vs :958-963 — F2, check ID H0 names two checks
[R827] MINOR Docs — tb/verilator/mbx/README.md:155,164; docs/design/MAILBOX_SPLIT.md:137 — F2, "check H0" ambiguous
```

Otherwise in Tests: `make` and `make mutants` (231 of 231) were rerun here, and the planted undo of each round 3 cut bites its own check. Otherwise in Docs: `check_doc_paths.py` OK (1,086 paths), `check_doc_style.py` OK, `git diff --check` clean. The comment rule holds: no new lane, round, reviewer or comment-ID text in added source lines (`receipts/comment_rule_scan.txt`; the hits are byte lanes and one re-indented base comment). R1 is RESIDUE and S1 a SUGGESTION.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #870 body and the two rulings; r3 route, endpoint and OOC receipts; `MARK_II_AREA_PLAN.md` M8a-2; gates 23n, 23o, 23p and the gen_mailbox check and self-test run here | R827-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| RTL | CLEAN | `KL_mbx_rx.sv`, `KL_mbx.sv` (generated), `KL_mbx_wb.sv`, `mailbox_skeleton.py` and `mailbox_face.py` read-term generation | R827-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Robustness | CLEAN | the same RTL; 9 reviewer probes and 2 controls; the suite's noise and probe bench (`tb_mbx_top.sv` BENCH_P, `bench.hpp`) | R827-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Tests | UNCLEAN (F1, F2 open) | `tb/verilator/mbx/*` (suite, bench, mutants: 231 of 231 run here), `test_builder.py` gates 23n, 23o, 23p (run, plus the bitstream probe), `gen_mailbox.py --selftest`, `pp_baseline.py --selftest` and its mutants, `test_ctrl_memory.py` | R827-1 | a91fb27dd39483e4694e193504da1dbe06208807 |
| Docs | UNCLEAN (F2 open; R1 residue; S1 optional) | `MAILBOX_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `SPLIT_CONTROL_MEMORY.md`, `PP_SHADOW_BASELINE_RECIPE.md`, `TESTING.md`, `ENDSTATION_BUILDER.md`, the mbx and ctrl_service_budget READMEs, the PR body | R827-1 | a91fb27dd39483e4694e193504da1dbe06208807 |

## Real limits

- **Implementation.** No Vivado run by the reviewer. The route, the out-of-context term and the resource gate are graded from the author's published receipts at `a2690e68`. The last commit, `a91fb27d`, changes two design documents only (`git show --stat`). The checkpoint and timing `.rpt` binaries are hashed, not published. The integrated script's head (pre-synthesis session state) is not in the packet; see (3).
- **LiteX split runs.** No split boot and no S2 harness rerun by the reviewer. Their evidence is the author's receipts at `a2690e68` (`r3/gates/split-boot-*.log`, `budget-*`). The firmware runs on the head's RTL only through the mailbox co-simulation run here (32 checks).
- **Banks.** No full parent, PP, gPTP, Yosys or builder bank, sweep or workflow replay. Those are author receipts. No manager source bank exists at this head, and none is claimed or inferred.
- **Hosted checks.** Snapshot at review time, `receipts/hosted_checks_snapshot.txt`:
  - executed and succeeded: `full-ci-gate`, `elaborate-gates-0`, `bdd-conformance`;
  - skipped context: `Physical gPTP (nightly and manual)`;
  - most others still queued or in progress.
  - The manager owns hosted and act acceptance.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was touched.
- **Redaction.** Receipts redact the host's home directory as `<home>`.

## Pending manager duties

- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `46c971fa0a09e2c8ca21acb95769defdc06c3068`) with the builder and native banks at the merge turn, and link the receipts.
- Own hosted (exact-head `verilator-suites` and `yosys-portability` once ready) and act acceptance.
- Route F1 and F2 to the executor, and re-review the fixing head under Tests and Docs. Coverage of every lens is banked against a commit, so any lens whose scope the fix touches must be re-covered.
- Carry R1 to the residue checklist.
- Post-merge containment, and the second, external positive review.

R827-1 FINISHED
