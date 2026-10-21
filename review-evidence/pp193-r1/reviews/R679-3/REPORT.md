[R679] NEGATIVE - exact head 474346357043218c4e6b728f4ab4b83a2a8579e1

# R679-3: independent round-3 review of processor PR #198 (Closes #193)

- Exact head `474346357043218c4e6b728f4ab4b83a2a8579e1`, tree `5ad76c02f6cfd8dbfa0b8d09e34b1cd22acec312`. The clone was verified byte-exact after all probes (`receipts/verify_clone.txt`: 702 tracked entries, 0 byte or mode mismatches, index equal to HEAD, no gitlinks in this repository).
- Round-3 delta reviewed: six author commits on `7b424cdf` (`70dd531`, `2f95efe`, `8f16338`, `1969f94`, `65d39b0`, `324ac9a`), plus the manager merge of processor main `859b537b` (#199).
- Summary:
  - The walk fix is correct and conformant at the head. My own S2 probe gives MATCH in 20 of 20 rows. A new two-handover sweep gives MATCH in 626 of 626 rows. All five new controls are KILLED on their named checks.
  - The extra fix (SH21) is a real defect at the base and is conformant.
  - Area is inside the accepted bound. The merge composes, and no port, parameter or register-map change is made.
- One MINOR remains, in the Tests lens: R679-3-F1. The round-3 term that holds the walk's done strobe until the second pass has served its slot has no check that fails without it. A mutant that strobes at the end of the first pass passes all 1,418 stream-FSM checks and all 8,669 srp_top checks. Under that mutant the second pass's message falls into the next tick, beside that tick's own message for the same StreamID.

## Reconstruction (order followed)

1. **Contributor rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. I read `docs/README.md` (conventions, single-source rules, what `make check` enforces). The comment rule comes from the owner text in the assignment.
2. **Frozen scope.** Issue #193 body; the A10 assignment (issuecomment-6289596705); the A661 STOP (…6289991979); the ownership ruling (…6290012163: owner election, handover "continues uninterrupted", combined type, suite cases); the area answers (…6299223806); the round-2 assignment (…6300041102); the round-2 area ruling (…6310654578: +1,335 LUT / +618 FF accepted); the round-3 assignment, read exactly (…6311435371); the author's round-3 REVIEW READY (…6319348032); the review start (…6319730921).
3. **Authorities.**
   - IEEE 802.1Q-2018 Table 10-3, as transcribed independently in `tb/srp_stream_fsms/sim_main.cpp:28-112`: QA on txLA! is sJ; QA on tx! sends nothing; LA on tx! is sL then VO; LA on txLA! is LO with no message; LO on tx! is s; New! takes VO to VN.
   - IEEE 802.1Q-2018 10.7.7 (one Applicant per attribute value), the 35.2.6 NOTE, 35.1.2.2 (Lv only for a stream no longer wanted), Milan v1.2 4.2.7.2.2 (a peer registrar deregisters at once on Lv).
   - The `txop_done_o` port contract, `hdl/srp/KL_srp_listener_fsm.sv:172`: "one-cycle strobe: tick walk finished, pushes accepted".
   - The `KL_srp_top` drain contract, `hdl/srp/KL_srp_top.sv:46-50` and `:1164-1169`.
4. **Diff and history.** `git diff 21601694..4743463`, `git diff 7b424cdf..324ac9a` (RTL, docs, tests, READMEs, mutants and patches, read in full), and `git diff 859b537..4743463`.
5. **Public evidence.** The milan-fpga evidence packet `d530fd82…/review-evidence/pp193-r1/author-r3` was sparse-cloned at the pinned commit. All 2,547 files match `MANIFEST.json` `published_sha256`: 0 missing, 0 mismatched, 0 unlisted (`receipts/evidence-manifest-check.txt`). The GitHub API reports the commit as unsigned, so integrity rests on the manifest, not on a signature. From that packet I read the round-3 `INDEX.md` header, `area/SUMMARY.txt` with the `ooc-final` and `ooc-main` logs and STATE, `scope-ports.txt`, `gates/head/run_suites.log`, every gate and campaign `.rc` (21 of 21 are 0), `campaigns/RUNNER.txt` and `campaigns/final/srp_top.log`.
6. **Prior findings.** Read only after my own pass over the diff and my probes: R679-2 (issuecomment-6311425623) and R680-2 (issuecomment-6310901034). I did not read the concurrent round-3 external review.

## Findings

### R679-3-F1 — MINOR — Tests: the done strobe's wait for the second pass has no killing check

**Where.**
- `hdl/srp/KL_srp_listener_fsm.sv:1036-1042`, W_DONE: `walk_r <= (&wdone_r) ? W_IDLE : W_EVAL; txop_done_o <= &wdone_r;`. This is a round-3 term: the strobe now waits until every slot holds the walk mark.
- The new checks drive and grade the walk through `tick_with_input_at` (`tb/srp_stream_fsms/sim_main.cpp:1853`).
  - That helper stops at the first `l_txop_done_o`, then idles 2 clocks.
  - Every SH16 and SH18-SH20 taker is sink 0, so the second pass pushes within those 2 clocks.
  - No check requires that a walk's pushes come before its strobe.

**Evidence** (reviewer probes; disposable arm `rv3-done-before-rewalk` in `probes/make_r3_mutants.py` changes only `txop_done_o <= &wdone_r` to `txop_done_o <= 1'b1`, keeping the second pass):

| Run | Result | Receipt |
|---|---|---|
| stream-FSM suite with the arm | 1,418 PASS, 0 FAIL | `receipts/phase1/rv3-done-before-rewalk.log` |
| srp_top suite (every group, real encoder and slot pool) with the arm | 8,669 PASS, 0 FAIL (head: 8,669 PASS) | `receipts/phase3/top-mut.log`, `top-head.log` |
| `probes/order_probe.py` at head: takers 0, 2, 4; tx! and txLA!; handover at clocks 1-12 | 72 rows, 0 pushes after the strobe | `receipts/phase2/order-head.log` |
| the same with the arm | 32 of 72 rows push after the strobe, e.g. "taker=0 walk=tx! inject@1: done at clock 9, pushes before 0, after 1" | `receipts/phase2/order-mut.log` |
| `probes/chain_probe.py` with the arm | 50 of 626 rows DIFF, e.g. "walk=tx! A=2: walk '' (model '0/2'); next '0/2 3/2'" | `receipts/phase2/chain-mut.log` |

In the chain row above, the second pass's New, pushed after the strobe, lands in the next tick together with that tick's JoinMt. That is two messages for one StreamID in one tick, the #193 symptom class.

**Authority.**
- The port contract at `:172` ("tick walk finished, pushes accepted").
- `KL_srp_top` drains the encoder on the two strobes (`KL_srp_top.sv:1164-1169`, "the cadence's messages ride its MRPDU"), and the encoder snapshots its pending count when a drain starts (`KL_srp_encoder.sv:561`, `drain_n_r`). A push after the strobe therefore misses that cadence's MRPDU. I infer this from the RTL; no srp_top bench exercises a handover behind the walk, which is why the arm survives there too.
- The round-3 assignment item 1 and the ruling's item 2 ("the declaration continues uninterrupted"). The banner, §6.4 and the PR all claim "the walk's tx! or txLA! in that walk".
- The lane's bar, which R679-2-F2 applied in the previous round: each new behaviour carries a check with a planted control that is KILLED.

**Impact.**
- The head RTL behaves correctly: 0 late pushes in 72 rows, and 626 of 626 chain rows MATCH.
- But a later edit that strobes before the second pass would reintroduce R679-2-F1 on the wire, undetected. The txLA! JoinMt would leave the LeaveAll MRPDU, and a tx! New would ride beside the next walk's message for the same value.

**Required outcome.**
- Add a committed check that grades a walk's Listener pushes against its done strobe. Either form works:
  - make `tick_with_input_at` (or a new SH case) count any Listener push between the strobe and the next join tick and require none, with a taker above sink 0 (for example sink 4 with holder 7) so that the second pass takes more than 2 clocks;
  - or add an srp_top case that requires the second pass's message in that cadence's MRPDU.
- Add the named control `txop_done_o <= 1'b1` in W_DONE, with the second pass kept. It must be KILLED on the new check.

**Verification.**
- The campaign reports the new control KILLED on its named check.
- `probes/order_probe.py` still reports LATE 0 at head, and LATE above 0 with the control planted.

### R679-3-R1 — RESIDUE — Docs: a review round named in repository prose

- **Where.** `tb/srp_top/README.md:884`, the `listener-walk-marks-group-only-on-retire` row: "the walk marks a group only when a park retires (round 2's form)". This is new in `8f16338`/`324ac9a`. Repository documentation describes behaviour and should not name review rounds.
- **Exact fix.** Replace "(round 2's form)" with "(the form before this change)".

### R679-3-R2 — RESIDUE — PR text: the S2 bullet credits the wrong finder

- **Where.** PR #198 body, section Round 2, bullet "A handover to a slot the walk has passed (S2)": "Round 3 found that in a txLA! walk the LeaveAll re-declaration was lost instead". R679-2 found it (R679-2-F1), and round 3 fixed it.
- **Exact fix.** Replace "Round 3 found that" with "R679-2 (F1) found that".

### R679-3-S1 — SUGGESTION — Docs/RTL: state the LA/LO exception of the group mark where the mechanism is described

- `KL_srp_listener_fsm.sv:1004` skips the group mark when the transmit leaves the applicant LA or LO. The in-code comment at `:996-1002` says so.
- The banner (`:110-120`), §6.4 (`docs/architecture/10_srp_engine.md:645`) and the PR body describe the group mark without the exception.
- My arm `rv3-group-mark-on-lo` drops the exception and passes all 1,418 checks (`receipts/phase1/rv3-group-mark-on-lo.log`).
  - That fits my reading: the LA/LO applicant stays in its slot, which the walk has marked, and a handover from there carries the mark.
  - The author's `area/SUMMARY.txt` shows that the exception is the cheaper form: W2, 58,046 LUTs, against W, 58,555.
- Suggestion: add a short clause to the banner and §6.4, for example "unless the transmit leaves it LA or LO, where a handover carries the mark instead".

### R679-3-S2 — SUGGESTION — Tests: SH1 no longer sees a rider that is not quiet

- With `listener-rider-not-quiet`, SH1's rider above the owner still goes to LO on the received LeaveAll. The group mark now holds its Empty to the next walk, which SH1 does not tick (`tb/srp_top/README.md:899-904`). The control is still KILLED (12 checks, SH14 named), so no coverage is lost.
- Suggestion: extend SH1's received-LeaveAll check by one tick, so that it again grades the rule with the rider above the owner.

## Prior public findings on this PR, at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R679-2-F1, MINOR: a handover into a slot the txLA! walk passed loses the LeaveAll re-declaration | **Resolved** (cause fixed); the strobe-order test gap of the new mechanism is new: R679-3-F1 | `probes/s2_probe.py`: 20/20 MATCH at head (both holders, tx! and txLA!, clocks 1-3, both controls); at `7b424cdf` the six txLA! handover rows read DIFF (`receipts/phase1/s2-head.log`, `s2-base.log`). Chain sweep 626/626 MATCH at head, 326 DIFF at `7b424cdf`. SH16, SH18 (x2), SH19 and SH20 fail on the `7b424cdf` RTL (`tests-on-base.log`); `listener-walk-ends-owing-a-transmit` KILLED on SH16, SH18-SH20. Banner `:106-120`, §6.4 `:643-651` and the PR text no longer claim a delay. |
| R679-2-F2, MINOR: no check fails without the re-park guard | **Resolved** | SH17 (`sim_main.cpp:1799`). Its control `listener-repark-takes-matcher-pairs` is byte-for-byte the edit I named (`rv-repark-overwrites-pairs`) and is KILLED on SH17 (`receipts/phase1/ctl-listener-repark-takes-matcher-pairs.log`, `phase2/camp-out`). `repark_probe.py`: MATCH at head, DIFF with the edit. |
| R679-2-R1, RESIDUE: README row names fewer failing checks | **Applied**, then extended | `tb/srp_top/README.md:868`: "SH2-SH17, SH21, SH23, RB1, RB4, RB7 … (65); SW2, SW4, SW6 (3)". This matches `campaigns/final/srp_top.log:187-188` tag for tag. The other six re-counted rows (`settle-compare-dropped` 32, `rider-not-quiet` 12, `handover-drops-state` 12, `withdraw-ignores-riders` 15, `group-order-reversed` 10, `settle-parks-shared-stream` 2) and `retire-skips-group-mark` 2 also match that log. |
| R679-2-S1, SUGGESTION: no killing check for the both-parked exclusion | **Applied** | SH23 (`sim_main.cpp:2047`). Its control `listener-two-parks-grouped` is the `rv-both-parked-grouped` edit and is KILLED on SH23. |
| R679-2-S2, SUGGESTION: two-sink `lcp` aliasing | **Measured, not kept**, as the assignment allowed | +99 LUT / -128 FF at 2 Stream Inputs (`area/SUMMARY.txt` item 2). It is not area-neutral, so commit 5 removed it. RTL at 8 sinks unchanged. |
| R679-2-S3, SUGGESTION: state the listener-alone one-sink delta | **Applied** | The PR body, beside "No 1x1 figure", gives main 2,898 LUT / 454 FF and head 2,786 / 455. That matches `area/SUMMARY.txt` item 3. |
| R680-2-S1, SUGGESTION: two check IDs in a test comment | **Applied** | The "(RB)" and "(RB5)" parentheticals are gone (`sim_main.cpp`, SH10-SH13 comment). |
| R679-1 / R680-1 findings | Resolved at round 2 (per R679-2) and **still resolved** | The delta leaves the parked-group terms unchanged apart from the walk marks. SH10-SH16 and SW4-SW7 pass at head, and their controls stay KILLED (`campaigns/final/srp_top.log`, my spot-check `receipts/phase2/camp.log`). |

## The round-3 assignment's checks

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | F1 mechanism, against Table 10-3, 10.7.7 and ruling item 2 | **Met** (RTL, Conformance); test gap R679-3-F1 | See "Mechanism review" below. s2 20/20 MATCH with both controls. SH18-SH20 pass, and `listener-walk-ends-owing-a-transmit` is KILLED. |
| 2 | Extra fix: New beside the last declarer's Lv in one walk | **Real at base, conformant, covered** | On the `7b424cdf` RTL, SH21 fails with "this walk '5/2 0/2'": Lv and New for one StreamID in one walk (`tests-on-base.log`). At head the New waits for the next tx!, as one applicant's New! after sL must (Table 10-3: LA, tx!, sL, VO; New! gives VN, sent at the next tx!; 10.7.7). `listener-walk-marks-group-only-on-retire` is KILLED on SH21. |
| 3 | F2 (SH17 with the named edit), R1, S1 (SH23 and control), S3, R680-2-S1 | **Met** | See the table above. |
| 4 | Area within +1,335 LUT / +618 FF plus 64 LUT | **Met** (on receipts) | `ooc-main` 56,743 / 26,331; `ooc-final` at `65d39b0c` 58,046 / 26,949; so +1,303 / +618. LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10 and CARRY4 2,392 are unchanged. The `65d39b0c` listener blob equals the head's (`f61843cf…`). Pins are checked in each STATE.txt. The receipts are manifest-verified; I did not re-synthesize. |
| 5 | The manager merge of main composes | **Met** | Every main-side file of #199 is byte-identical to `859b537` at the head, `hdl/aecp` tree included (`0237e79f…`), and `gen_ucode.py`, `decode.json`, the notify, d3 and sim sources and docs 06/09 are equal. Only `tb/pp_top/README.md` touches both sides, in disjoint hunks, and its merge delta equals main's delta line for line (`receipts/scope-and-merge.txt`). At the merged head: `tb/pp_top` 10,741 PASS, `tb/aecp_cmds` 176 PASS (617,916 trials) (`receipts/phase4`). The `gsi_mutants.py` anchor of the PR still occurs once in the RTL. |
| 6 | No top-level port, parameter or register-map change | **Met** | Against main `859b537` the only HDL change is `KL_srp_listener_fsm.sv`. Its module header hashes identically at 21601694, 7b424cdf, 859b537 and the head. `protocol_processor_top.sv` equals main's. Docs 01, 02 and 07 are unchanged against main. |

### Mechanism review (RTL, Conformance, Robustness)

- **One transmit, never two.**
  - `wdone_r[t]` means "the walk passed this slot or served the applicant in it" (`:1003`), and every member of a served group is marked (`:1004-1008`).
  - A handover copies the giver's mark onto the taker, after every other assignment (`:1072`).
  - A taker that the walk passed and whose giver it had not reached is the only kind of slot left unmarked at W_DONE. The second pass serves it in the same walk, with the walk's `wtxla_r`.
  - A taker of an already served applicant inherits the mark, so it is not served again.
  - My arm `rv3-take-keeps-taker-mark` (the taker keeps its own mark) fails SH16, SH18 (x2), SH19 and SH20. `rv3-rewalk-keeps-wsrc` (the second pass does not restart at slot 0) fails the same five.
- **No delay for other applicants.**
  - A walk with no unmarked slot ends exactly as before.
  - In a second pass, marked slots pass in one clock each and push nothing. Slots already served are never sent again.
  - The pass lengthens the walk by at most about N clocks per handover, with `join_tick_i` latched into `tick_pend_r`. Every applicant's transmit stays in the same walk.
- **Termination.**
  - Every slot passed is marked, quiet riders included (`walk_grant_w`). The author's control `listener-walk-marks-only-served-slots` shows that without this a walk never ends (SH22).
  - My chain sweep puts a second handover into the second pass: walks of 29-30 clocks, 3 passes. Every one of its 626 rows ends, with exactly the one-applicant message.
  - Further passes need further external handovers, so a walk always ends once its inputs stop.
- **Group mark on a VO or parked group.**
  - A later New! on a member of a group whose (VO) transmit already passed waits for the next tx!. That is one applicant's behaviour.
  - Parked applicants stay in the group of their held value, and two parks are never grouped (SH23). A retired park's slot that later takes another group's applicant from an unreached slot gets that slot's unmarked state and is served (SH16).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 10-3 transcription against the RTL walk; SH16-SH23 expectations; s2 (20 rows) and chain (626 rows) against the one-applicant model; SH21 at base; 10.7.7, the 35.2.6 NOTE, 35.1.2.2, ruling item 2 | R679-3 (delta); unchanged terms keep R679-2's verdict | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| RTL | CLEAN | `KL_srp_listener_fsm.sv` round-3 delta (`:106-120`, `:420-424`, `:996-1008`, `:1032-1043`, `:1072`) in the context of `owner_map`, `app_arb`, `handover` and `walk_msg`; four reviewer arms; module-header and scope diff; area receipts | R679-3 | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Robustness | CLEAN | Walk termination (SH22 control, chain walks of 3 passes); second-pass bound; handover in the W_DONE and W_IDLE cycles (`(walk_r != W_IDLE)` guard); strobe order at head (order probe, 0 late) | R679-3 | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Tests | **UNCLEAN** (R679-3-F1) | SH16-SH23 source; five new controls KILLED (own runs and campaign spot-check of 10 arms); suite at head 1,418 PASS, walk arms PASS; head tests on base RTL (6 named failures); srp_top 8,669 PASS; surviving arm `rv3-done-before-rewalk`; `rv3-group-mark-on-lo` equivalent | R679-3 | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Docs | CLEAN (residue R679-3-R1, R2 carried) | Banner, 10 §6.4, both READMEs (counts checked against the final campaign), PR body; comment-rule scan of the delta's added lines (no lane, reviewer, round or comment ID in source comments; one round name in a README, R1) | R679-3 | 474346357043218c4e6b728f4ab4b83a2a8579e1 |

## Receipts (all under this packet; listed in MANIFEST.sha256)

- `probes/`:
  - `s2_probe.py` and `repark_probe.py` (round-2 reviewer probes, unchanged), plus the `rv-repark-overwrites-pairs.patch` they use;
  - `chain_probe.py`, `order_probe.py` and `make_r3_mutants.py` (four arms);
  - `run_r3_probes.sh`, `run_r3_phase2.sh`, `run_r3_phase3.sh` and `run_r3_phase4.sh`;
  - `verify_clone.sh` and `verify_evidence.py`.
- `receipts/phase1/`: head full stream-FSM `make` (walk arms and suite); s2, repark and chain at head and base; head tests on base RTL; four reviewer arms; five author controls applied with `git apply`. `SUMMARY.txt` is the run table.
- `receipts/phase2/`: order probe at head and with the arm; chain probe with the arm; srp_top `mutants.py --only` (10 round-3 arms, `camp-out/`).
- `receipts/phase3/`: srp_top `make` at head and with `rv3-done-before-rewalk`.
- `receipts/phase4/`: `tb/pp_top` and `tb/aecp_cmds` at the merged head.
- `receipts/gates/`: `scripts/lint_hdl.sh` and `make check` at head (rc 0 both).
- `receipts/scope-and-merge.txt`, `receipts/evidence-manifest-check.txt`, `receipts/verify_clone.txt`, `receipts/tools.txt` (Verilator 5.050 through the pinned wrapper, with its sha256).
- In the build logs, the local install root of the pinned Verilator is redacted to `<pinned-verilator-5.050>`. Nothing else in the logs is edited.

## Real limits

- No area re-synthesis by this review. Item 4 rests on the manifest-verified author receipts (`area/`). That measurement is at `65d39b0c` against main `08023123` on a scratch parent. No figure exists at the merged head; the merge changes only main-side AECP files, so the PR's delta is the listener blob, which is identical.
- The wire-level impact in R679-3-F1 is inferred from `KL_srp_top` and `KL_srp_encoder` RTL (drain on the strobes, pending-count snapshot). It is shown executed at the FSM interface (late pushes, a two-message tick), not through an srp_top frame.
- The evidence commit `d530fd82` is unsigned according to the GitHub API. Integrity was checked against `MANIFEST.json` only.
- Not run here: the full processor and parent banks, the consumer gates, the gPTP and Yosys banks, hosted or act CI, and hardware. Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank runs at this exact head, and none is claimed or inferred here.

## Pending manager duties

- Validate the current-dev merge candidate (source base 21601694; live dev d77a8afdbc960d70d1ceeee9af1163624f102b16) with the builder and native banks, and link the receipts.
- Re-run the consumer gates, as the round-3 assignment assigns.
- Own hosted/act acceptance and the 4th pin adoption's route-1x1 resource gate.
- Carry R679-3-R1 and R679-3-R2 to the residue checklist.

R679-3 FINISHED
