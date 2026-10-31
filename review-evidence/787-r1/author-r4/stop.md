[A700e] STOP
Commit: `3e67de9c1d42557f222edd2b079d23265bf1b726`, local and not pushed. It is the merge `5640e4d7` of dev `02ca829a` into `4aa5666e`, plus one commit re-recording the port census. The pushed head stays `4aa5666e`.
STOP condition met: **the route misses the floor.** Route-1x1 on the three placement directives, judged by the #818 gate (PR #820's file at `50e5d08d`, used from scratch): rc 1, `RESULT: MATERIAL REGRESSION`.
- Worst-corner setup WNS, both slow corners:
  - ExtraPostPlacementOpt **+0.018 ns** (selected, the best)
  - ExtraTimingOpt **+0.017 ns**
  - AltSpreadLogic_high **+0.000 ns**
  - Every directive is under the +0.030 ns floor. TNS is 0 everywhere.
- Hold meets 0 ns at every corner: +0.033, +0.013 and +0.030 ns at the worst corners.
- Resources are inside every tolerance and ceiling. The selected route has LUT 52,291 (+279 against the record), FF 53,833 (+126) and slices 15,837 (+57; 13 free). RAM and DSP are unchanged, and 87.5 Block RAM tiles are used.
- Every route completes with no routing error.
- Worst path of each directive: the 100 MHz `sys` clock, in LiteDRAM's controller, from `milansoc_sdram_zqcs_timer_count1_reg[*]` to a bank machine's state or level CE, 16 to 18 levels, 74 to 79 % routing. Neither this PR nor dev's merges change that logic.
- Against each side's own set (one seed per directive each):
  - This branch before the merge (`667b9bbc`): +0.165 / +0.151 / +0.120 ns.
  - #806, as PR #813 records it: +0.032 / +0.235 / +0.218 ns.
  - The merge: +0.018 / +0.000 / +0.017 ns.
  - Each side's best met the floor; the merged image's does not. This measurement cannot separate a design effect from placement.
- This issue's bench comment reports an integration image that also carries #814 routed at +0.246 ns. #814 is not in dev yet.
The merge itself is clean (no other STOP condition):
- Exactly the six assigned files conflicted: two documents' prose, the pin table and the boundary-diagram records. None needed a behaviour choice. Both sides' CHANGELOG entries, pin rows, adoption records and area notes are kept. In #787's record, "FPGA-gPTP stays at" now names `135afd04`.
- Regenerated through their generators, each equal to the union of the two sides:
  - the boundary diagram, SVG/drawio/PNG and its manifest entry: against this branch only the gPTP pin differs, against dev only the processor pin;
  - the ROM ledger: re-recorded byte-identical to the textual merge;
  - the port census in `scripts/port_docs.budget` (its own commit): hdl 2181 / gPTP 127 / processor 1771, exactly base plus both sides' per-file additions, ratchets unchanged.
- `git diff --check $(git merge-base FETCH_HEAD HEAD) HEAD` against dev: rc 0.
Validation at the head:
- Static and pin-record bank 32 of 32 rc 0.
- Builder bank `ALL GATES PASS EXCEPT 2 NOT RUN`, round 2's two. Gate 1f 9/9, gate 23m on 5 configs, and #817's servo reset cut and refusal controls pass.
- xvlog 0 findings.
- milan_dp suites: 14,516 checks, 0 failures. milan_dp 13,796 = this branch's 13,757 + 16 (#806's gPTP legs, 202 -> 210 each) + 23 (#70's `[VOLATILE]` block).
- Campaigns whose inputs the merge changed:
  - `[RB]` 68 checks;
  - `reboot-mutant` 6 of 6, with round 2's failing counts;
  - LiteX simulations 7 of 7;
  - the MAC model check, OK;
  - #70's service budget, 69 checks;
  - #70's `dynmap-mutants`: 66 of 66 arms caught, among them its three processor-copy arms on this branch's pin, and every clean leg passes. From a clean clone, the full run caught 64, and its two end-to-end legs' controls failed. The listener leg is built with `make -o` over inputs only its own suite makes. The talker leg's build under the outer make spliced make's directory lines into its source list. With those inputs made and the script run directly, arms 36 and 37 and both controls pass. These are pre-existing harness preconditions; neither side changed those legs.
- rtl-fast: `success; failed jobs: none`, 12 of 12 jobs, behave 14 features / 508 scenarios / 2,330 steps.
- Docs workflow: 44 steps, 0 failed (2 skipped by rule), the concise-documentation and submodule-documentation gates included. Builder leg 1 with LiteX passes. Markdown gates 5 of 5. The no-git step's gates pass.
- On each route log: the #607 log check is clean and IOB packing is OK (22 ports).
Found, pre-existing, not changed in a merge-only round: `docs/diagrams/cdc_census.{svg,drawio}` is stale on this branch since round 2. Its generator counts three SoC MultiReg call sites, the PHY hold being the third; the committed file says two. The merge does not change it, and no gate reads it.
Decision needed (owner): how route-1x1 is to be met for this branch now that dev carries #806, #817 and #70 but not yet #814. Nothing is pushed.
