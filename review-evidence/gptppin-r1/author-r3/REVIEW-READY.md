[A835] REVIEW READY
Commit: fc6870cab13f74149864b80b6480ddb3641cb936 (branch 994-gptp-pin-1213ac5b; PR #995 against dev-soft-core; not pushed)

Delta from round 2's head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: two commits, six paths, all under tb/verilator/gptp_shadow or Markdown.
- 567eaa48ba782c9ad38c37a0c877f2e4ae33da72: sim_main.cpp, mutants.py, test_mutant_lifecycle.py (R916-2-F1, R915-2-F1, R915-2-R2 in the code comments).
- fc6870cab13f74149864b80b6480ddb3641cb936: tb/verilator/gptp_shadow/README.md, docs/reference/SUBMODULES.md, CHANGELOG.md (R915-2-R1, R2, R3, S1, and the F1 records).

Changed:
- sim_main.cpp, the race (R916-2-F1). "#106 race: one master Announce reaches the lane before the re-election" counts master Announces whose last beat is accepted on the lane (`txf_cyc`, the `tx_tvalid_o && tx_tready_i` clock) at or after the takeover and strictly before `fall`, the clock the published master bit fell. With no recorded fall nothing counts. The old bound, `rise + 2 * kSyncTicks`, is gone. An INFO line prints both clocks against the takeover: at the head the last beat is +285 and the re-election +1,281. The missing-Announce, cadence and credit assertions are unchanged.
- sim_main.cpp, phase 21 (R915-2-F1). Two arms, the reserve first:
  - Reserve (new): one Sync's launch record is held (rechold type 0), so no result returns. Sync and Pdelay_Req then wait on their owed claim (S_TXQ_TMR), and the master's own Announces fill the ticket: 5 frames outstanding, past TXTS_CAP_N_P - MAND_RSV_C = 8 - 4. GMID is then elected and its silence makes the takeover.
    - At the instant the arm checks: unsealed, outstanding still past the reserve, asCapable.
    - Over the next 250 ms it checks: no master Announce on the lane, no seal and no barrier.
    - Released, it checks: the results drain below the reserve, the withheld Announce leaves 1 s after the instant (2,000,103 clocks), and the cadence runs on.
    - Under an Announce leg without its credit gate, the Announce reaches the lane, because no fence backs the reserve.
  - Seal: the round-2 arm, renamed "#106 seal: ..." (it was "#106 credit: ..."). Its no-Announce check is now "no master Announce reaches the lane while sealed". Its comment says its fence also holds the lane, so it grades the retry and not the gate.
  - Order: under a leg that ignores the credit, the seal arm leaves a result owed and the reserve arm's quiet start would stop it. So the reserve arm runs first. At 8c8c1c36, an unpushed intermediate later amended, the control was caught only by "#106 reserve: the plane starts with no egress result owed".
  - The retry grading is one helper shared by both arms. The run has 424 checks: 408, plus 13 in the reserve arm, plus its 3 quiet-start checks.
- sim_main.cpp comments (R915-2-R2): the new phases are 19, 20 and 21 (the section header and the three function comments). The existing "18: the PHC trajectory" is untouched.
- mutants.py: two controls, 13 in all.
  - `announce_leg_ignores_the_credit` (generator): ANNTX's `e_credit_gate` removed, anchored on ANNTX's three gate lines, unique in the file. It must fail "#106 reserve: no master Announce reaches the lane without credit".
  - `master_announce_reaches_the_lane_after_the_re_election` (harness): R916-2's order_probe stall, `dut->tx_tready_i = 0` before and `= 1` after the race's queued Announce in `silence_gm_announces`. It must fail "#106 race: one master Announce reaches the lane before the re-election". The docstring says it plants in the harness, and why.
- test_mutant_lifecycle.py: 13 controls, "thirteen named defects".
- README.md (gptp_shadow): rows 19, 20 and 21. Row 20 gives the lane boundary and the re-election clock, and row 21 both arms. The campaign paragraph names the two new controls, with "phase 20's race" and "phase 19's settled rate". The last line says "all thirteen detections". Row 19 records the slewing arm's TLV sign (R915-2-S1).
- SUBMODULES.md, #994 record:
  - The selection rule follows R915-2-R1's exact order: "An image meeting the floor on the first directive ships." / "Otherwise all three are routed." / "The best worst-corner WNS ships (#818)." / "At 1x1 the first missed, as on the base." / "So all three were routed there."
  - The phase sentences are now phases 19 to 21. Phase 20 "sends an Announce in the deadline's own millisecond" (R915-2-S2's wording point). "The master Announce's last beat precedes its re-election clock." Phase 21 names the reserve and the seal.
  - The campaign is "four defects".
- CHANGELOG.md: "The cadence counts from that Announce (802.1AS-2011 Figure 10-15)." (R915-2-R3, exact). One line adds "It also grades the Announce credit through the ticket reserve."

Validation, at fc6870ca on clean shared clones, pinned Verilator 5.050. Every command ran in the foreground, in windows of at most 590 s, at host load 195 to 260 on 96 CPUs. Receipts are in receipts/INDEX.md.
- gptp_shadow `make run`: 424 checks: 424 PASS, 0 FAIL (rc 0, 238 s). `make lifecycle`: "mutant lifecycle: PASS (normal/repeat, thirteen named defects, ...)".
- gptp_shadow campaign: `mutants.py`'s own main() on slices of MUTATIONS (tools/mutants_slice.py), in nine slices across windows A to C: 13/13 controls, 0 failures.
  - The new controls are caught by their named checks: "#106 reserve: no master Announce reaches the lane without credit", and "#106 race: one master Announce reaches the lane before the re-election".
  - Three controls are caught by other checks than their names, exactly as at f97e49fe: both latency off-by-ones and credit_never_withheld.
  - Two slices (0-2, 6-8) hit the window after their first control. Their second controls (1-2, 7-8) ran in later windows.
- Reviewer probes at the head (tools/probes_r3.py; each a fresh clone, one edit, `make run`):
  - R916-2 order stall: rc 2, 423/424. FAIL "#106 race: one master Announce reaches the lane before the re-election". The last beat is at +4,659 and the re-election at +1,281.
  - R915-2 p106-nocredit: rc 2, 421/424. "#106 reserve: no master Announce reaches the lane without credit" (got 1), "two master Announces once the credit returns" (got 3), "the withheld Announce leaves 1 s after the instant".
  - R915-2 p106-beat: rc 2, 416/422. At once; the race; both arms' "two master Announces once the credit returns" and "the withheld Announce leaves 1 s after the instant".
  - R916-1 delayed-announce: rc 2, 416/422, the same six.
  - R916-1 retained-slave-rate: rc 2, 420/424. Rate 0 and the 8 ns advance at +100 ppm (0x345a) and at -100 ppm (0xffffcb86).
- gptp_plane: `make run` 31/31. phc-step (phc_step_slice.py, phc_step.py plus an arm filter): clean 62 checks, 0 failures, and all 8 arms PASS. The clean arm and two planted arms ran in window F, the other five one per process in window G.
- gptp_tables: limits rc 0, run 36 checks 0 failures, mutants 26/26 (nine slices of at most 3, window H).
- gptp_txts: `make` rc 0, 95 checks, controls 13, failures 0.
- milan_dp gptp and gptp-lat: NOT COMPLETED. Six attempts each (windows D, E, F, G, I and L, the later ones with the built binaries reused) ended at the window's timeout, rc 124. The simulations print only at exit.
  - receipts/rtl/milan_dp-inputs.txt: their recipes name 127 files, none changed after f97e49fe. The one name match is the product RTL `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, unchanged. No tracked file under tb/verilator/milan_dp names tb/verilator/gptp_shadow.
  - Round 2's 212/212 receipts at f97e49fe, [CA] 0xF822436A and 0xF8FE436A, therefore cover the same inputs.
- Docs workflow (tools/docs_steps.py, as round 2, em-dash base 2509db68): 48 distinct steps rc 0. They include the em-dash gate (0 findings over 211 added lines), the concise audience, gPTP, submodule and diagram gates, the test-evidence ratchet, and the SV, C/C++, Python and shell idiom gates. The cited-path, TOC and inventory gates pass too.
  - Not completed in a window: the Saved-state writer gate, and the CI event gate's selftest after "ci_events: OK".
  - Not run this round: the HDL reference build, the RV32 SDK install-verify (refuses on this host), both builder legs and the compiler-absent firmware controls. None reads a changed path.
- Images unchanged, by hash (receipts/ledger/images-unchanged.txt):
  - f97e49fe..fc6870ca changes six paths: four in tb/verilator/gptp_shadow, plus CHANGELOG.md and docs/reference/SUBMODULES.md.
  - plat_ledger at the head: PASS, 0 findings. Its 24 image sha256 (ELF, stripped and loadable at the 8 points) equal round 2's receipt, with 0 diff lines.
  - 291 png/svg/drawio blobs and gitlinks are identical (ls-tree, 0 diff lines). gptp-processor is at 1213ac5b.
  - docs/diagrams/submodule_boundaries.png is f5768392...ee66, and timesync_chain.png is d209354a...7655, R916-2's hashes.
  - The default gptp_ucode.hex regenerated from the pinned generator is 4eb21cef..., the rom_digests.tsv row.
- check_doc_style OK (25), check_gptp_docs OK (8 pages), check_submodule_docs OK (6 exact gitlinks), docs_inventory OK, `git diff --check` clean.
- S3, measured here. The simulation alone, run at once, takes 64 s at bbfdb674, 102 s at f97e49fe and 154 s at the head. The default target is 14 builds and runs; it was 10 at bbfdb674, whose hosted figure is the 393 s registered in scripts/suite_shards.py.
  - Hosted estimate: about 840 to 950 s, 47 to 53 % of the 1,800 s suite timeout.
  - The shard tool's balance and headroom gate at the head passes for any figure up to 1,200 s (worst regular worker 1,590 s against 1,620 s). It fails at 1,500 s (receipts/rtl/shard-projection.txt).
  - suite_shards.py is not edited: its table is measured data.

Acceptance criteria (#994, frozen): 1 MET (no pin site moved; 6 exact gitlinks; 8 current pages). 2 MET at the head for gptp_shadow, gptp_plane with phc-step, gptp_tables and gptp_txts. milan_dp gptp and gptp-lat are met at f97e49fe with unchanged inputs, and not re-completed at this head (above). 3 MET (round 1's routes; no synthesis input changed since 973f2f20).

Findings addressed:
- R916-2-F1 (MINOR): the race is graded against `fall` with the lane's last-beat clock. R916-2's stall fails that named check, at the head and as a campaign control.
- R915-2-F1 (MINOR): the reserve arm grades the credit gate with no fence behind it. R915-2's p106-nocredit fails "#106 reserve: no master Announce reaches the lane without credit", at the head and as a campaign control.
- R915-2-R1, R2, R3: exactly as stated.
- S1: the sign is recorded in the README row and the PR. The donor issue is left to the manager (no GitHub writes this round).
- S2: not taken. The reason is in the PR's known limitations, and the record's sentence no longer claims "at the instant".
- S3: measured and projected as above.
- S4 and S5 were not asked for. S5's control is still caught only by the quiet-start guards.

Open risks/questions:
- milan_dp gptp/gptp-lat at this head need a less loaded window, or the hosted or act run. Their inputs are unchanged since f97e49fe.
- The reserve arm adds about 50 s to each local simulation (the four-Announce fill is four simulated seconds). gptp_shadow's hosted figure needs measuring from this head's hosted window.
- The race's INFO line prints "+0" for the last beat when no master Announce follows the takeover (as under p106-beat). It is diagnostic only; the check itself counts nothing then.
