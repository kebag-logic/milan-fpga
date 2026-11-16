[A787] REVIEW READY

Commit: 9715a30ac4f43f58ca96fcc6d29314fad09bf8ae (`sync-dev-6b66f66d-into-dev-soft-core`, local; nothing pushed; the manager pushes)

Changed: round 2 of the dev sync (#665 issuecomment-6907491626).
- `10b2fe21`: one `--no-ff` merge of dev-soft-core `70f4056f` (#901) onto round 1's `d2da3159`. Two documentation conflicts, both sides kept; no code conflicted; no pin moved.
- `30c5d3d6`: section 5's sync sentence restated at the merge (32 to 40 B of `rom`, no tile moved).
- `4cb7d7ab`: the documentation audit regenerated.
- `9715a30a`: a semantic conflict of the dev merge, found by the sweep. dev's newer reads in the `pp_shadow` and bootsa benches address KL_pp_shadow at dev's flat path. On this line it sits in dev-soft-core's `g_af_pp` block, so both benches failed to compile. They now take that path, as the bench's other reads already did.

Validation (clean clones of `9715a30a` unless stated):
- **All four workflows:** 154 steps rc 0, 256 not run with a reason, 0 bad. This includes:
  - mutation campaigns: control 716 of 716, AECP 299, SRP 421, no escapes;
  - elaborate;
  - the Yosys shards;
  - the publication census: 6 shapes, 0 of 163 arms failed.
- **4-shard sweep: all 65 suites pass.** 62 passed at `4cb7d7ab`. `pp_shadow`, `milan_dp` and `milan_dp_gm_steps` were re-run at `9715a30a` and pass: the first two are fixed by it, and the third timed out under load at `4cb7d7ab`. No other suite reads the two changed files.
- **The split leg and its plants:** `split` 84 of 84; `split-mutants` 28 of 28.
- **Images:** each grows 32 to 40 B of `rom` over `70f4056f`, and no tile moves. The 8x8/1if platform plans 56.0 with 848 B spare, so the BRAM rule (#923) adds no debt.
- **The CPU budget harness at 1x1/1if:** arm A has 0, 0, 0 and 7 misses (the ruled held-egress rows). The answering-every-port and answering-ports legs pass. The flip check passes, and the load is 0.517 against 0.70. All 13 legs regrade byte-identical at `9715a30a`.
- **Routes**, at `10b2fe21`, whose RTL, firmware and build inputs are the head's:
  - split 1x1/1if meets on all three directives, best ExtraTimingOpt at +0.196 / +0.036 ns;
  - split 8x8/1if meets on AltSpreadLogic_high only, at +0.140 / +0.036 ns. That is round 1's figure; #810 had +0.292 on ExtraTimingOpt, and #927 takes the thin margin;
  - release AX7101 1x1 meets setup on all three, best +0.209 ns. Its gateware export equals round 1's, file for file.

Acceptance criteria:
- met: one merge, both sides kept; pins; the gates and the sweep; the images and the ledger; the routes and the release export; the 1000BASE-T-only advertisement recorded as #919's.
- **not met:** the three items below, each listed open as the ruling allows.

Open risks/questions (each blocks the merge, not the review):
1. **The open miss, and its cause: THE TRANSMIT's MRPDU rows wait for lwSRP's join timer, not the CPU** (ruling items 1 to 3).
   - At 8x8/1if across eleven LeaveAll phases (ten harness-only MAC seeds and the product MAC):
     - the sync alone misses at 9 of 11 phases (row budget 20 ms), worst `mrpdu.leaveall.if0` 160.6 ms, the product MAC 160.6 ms;
     - the local trial merge with #914's `d539f162` misses at 7 of 11 (budget 49 ms), worst 160.6 ms. **It still misses**, and its rows equal the sync's within 0.4 ms at every phase;
     - two phases miss on `mrpdu.periodic.if0` (100.6 and 140.8 ms) the same way.
   - In all 36 delayed run-outs, the frame leaves 0.44 to 1.56 ms after its participant's next join-timer run-out. That run-out is 189.1 to 189.6 ms, one JoinTime, after the participant's previous build. The CPU is busy for 12 to 22 % of the wait (97 to 99 % under the grandmaster flood), and THE TRANSMIT's build (about 31,500 cycles) is inside the slice.
   - lwSRP's `mrp_transmit` sends nothing while `join_wait` is set (`mrp_mad.c:1421`), and each transmission sets it for 19 cs (`:1539-1540`). So the remedy in ruling item 3 already holds at the merge, and the rows still miss.
   - The same wait fails #901's valid-destinations arm at 1x1/1if: a LeaveAll at 14,054 ms is sent 160.5 ms late. The same code passes with the pre-#840 MAC (an experiment).
   - **Question:** does THE TRANSMIT's row (FR_NFR.md 3.4.1) time the wait lwSRP's join timer imposes, and who owns it?
2. **The paced record at 1x1/1if**, a gate (`record_classes.py`, RESULT FAIL).
   - The merge's accepted SET_CONFIGURATION is 28,700 cycles, 305 us by the rule, against `edit_rows.PACED`'s 300 us. #901's head measured 28,288, and round 1 28,452.
   - Restating it to 305 us keeps every row within its bound (an experiment). But it takes the model's tx row past `CTRL_LOOP_TX_MS` (34 ms), so the flip check fails: the restatement reaches a firmware constant.
   - **Question:** restate both by the rule, and in which lane; or recover the 129 cycles.
3. **The release AX7101 1x1 route's fast-corner hold** is +0.014 to +0.016 ns at every directive: over the build gate's 0, under the round's +0.030. The worst paths are inside the LiteX CPU, and the image is dev's, file for file.
   - **Question:** does the +0.030 hold floor apply to the release image?

Found, not fixed:
- twin and twin-plants fail identically on `70f4056f`: the owed row `split-talker-failed`, which is #929, and plant `srp-plus-k`, which names the same retired Talker Failed;
- srptx fails as at `70f4056f` (#916);
- #840's 1000BASE-T-only advertisement is not on the split (#919, issuecomment-6907491954).

The host restarted three times during the round. Each cut unit's half-written output was removed and the unit run again, and no result above comes from a cut run. Receipts, the handoff and the PR body are in the lane's round-2 output.
