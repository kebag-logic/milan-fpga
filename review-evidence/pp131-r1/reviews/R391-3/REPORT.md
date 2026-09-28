[R391] NEGATIVE - exact head cbbb5acc77e9e068c3313d78ed4c1e5e79299a71

# R391-3: independent external review of processor PR #132 (issue #131, D3 lane 1), round 3

- **Repository.** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-3.
- **Head.** Exact head `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71`, tree `63e8bbf1cb966049b4f405145f9e73fd2b03adc5`. The PR's live head reads the same sha. Base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Delta reviewed.** `2b38d68e..cbbb5acc`, five commits: `f8d1a83`, `9d66095`, `58c5fe9`, `e94bea8`, `cbbb5ac`. They touch 19 files (+801 / -103). Four are RTL: the writer, the engine pass-through, the binding manager's new `rs_agg_i` and the top wiring.
- **Authorities.**
  - Parent contract: milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md`. It is byte-identical at `7a7582f0` and at live dev `b5c0f69d`. I used §6.1-§6.3, §7.1-§7.2, §8.1, §8.8 and §18.1.
  - `docs/design/SAVED_STATE_FASTCONNECT.md` §9.3 and §16 (the saved-state durability page) at `b5c0f69d`.
  - Parent #70 rulings:
    - DR1a-DR6 (5862405632);
    - DR2c-carrier (5863247772) and its correction (5868716535);
    - the DR3a/DR4 ratification (5873060660).
  - Issue #131:
    - the hold-admission ruling (5873580386);
    - the DR3a clarification (5876655419: an aggregate expiry never closes a provable image);
    - the round-3 assignment (5876934804).
- **Reconstruction order.**
  1. Processor README, docs/README and hdl/README. The processor repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #131's body and every maintainer and manager comment, the PR body (rounds 1-3) and the manager's bank comments.
  3. The parent rulings and contract sections above.
  4. `git diff c951a9ff..cbbb5acc`, then the round-3 delta per commit.
  5. Public evidence: milan-fpga `b657a2de` `review-evidence/pp131-r1`. This is the round-1 archive; there is no later public archive. I also read the hosted check runs at the exact head.
- **My round-2 packet** (`pp131-r391-2-packet`) was read-only input for my own scripts and findings.
- **Other reviews.** No private material was read. The other reviewer's prior public findings were read only after my own pass over the diff (last section).

## Verdict

NEGATIVE.

**What holds at this head:**

- **The RTL implements the clarification, and I found no case where it misbehaves.** Before the proof the aggregate aborts nothing. A binding walk still reading takes its own per-wait path through `rs_agg_i`, fails whole and releases the listener. The D3 walk then proves the image, reads no record and ends DEFAULTS, cause 3. CLOSED needs an unprovable image (cause 7) or a pass-1 roll-back that cannot prove it again (the pass-1 cause).
  - Probe D1 at the top's own derived deadlines, five arms:
    - image present at reset: DEFAULTS 4 clocks after the bound;
    - image loaded after reset and proven by the writer's LOCATE: DEFAULTS +545, also +545 with a just-inside grant-slow device after the release;
    - image refused: CLOSED, cause 7, +44;
    - descriptor memory silent: CLOSED, cause 7 through the store's own watchdog, +4,105.
  - My P9 sweep: 17,406 runs with the expiry on every clock of both walks. There are 0 deviations.
- **Every named check passes, and every mutant from my round 2 is killed.**
  - Both guides now state every aggregate terminal and both causes of CLOSED, consistent with 07 §5.3.
  - D3R15, D3R16, D3R17 and D3O7 kill `agg_not_in_rollback`, `agg_not_stopped_at_terminal`, `agg_fires_with_event_in_hand` and `resident_never_returned`.
  - `d3_mutants.py` reports **69 of 69 KILLED, goldens PASS** in my run.
- **Parent consequence (item 4): no write is lost.** In a scratch parent at dev `b5c0f69d` I reproduce the 7 of 315 failures, and 315 of 315 at base. When B1-B4 run past the backoff, 315 of 315 pass with this head, under the top's own backoff derivation and under the module default alike. The later record persists and the power cycle restores it.

**Two new MINOR findings remain open:**

1. **F1 MINOR (Conformance, Tests, Docs): the parent-visible change list is incomplete and misattributes the nvm_cosim failures.**
   - The 7 failures do not come from "the ruled backoff outlasting the scenario window". They come from the parent's `cosim_top.sv` leaving the binding manager's `RETRY_BACKOFF_CYC_P` at its module default of 50,000,000 clocks. At the suite's 1 MHz clock that is 50 s, 100 times the ruled 500 ms.
   - The pin-adoption lane needs two edits the PR body does not list: bind that parameter as the top derives it, and extend B1-B4.
2. **F2 MINOR (Conformance, Tests): three variants of the pre-proof path are unguarded.** Three reviewer mutants each leave the aggregate unenforced on a clarified path, yet each passes all 7,855 checks of the default pp_top build:
   - the image proven by the writer's own LOCATE, the parent §8.1 product order;
   - the bound on the proof's own clock;
   - a binding byte in hand at the expiry.

   D3R14 grades only the image-present-at-reset path.

Three SUGGESTIONs (S1-S3) do not affect the verdict.

## Findings

### F1 - MINOR - Conformance, Tests, Docs - the PR body's parent-visible list omits the nvm_cosim backoff binding and misattributes the 7 of 315 failures

- **Where.**
  - PR #132 body, "Round 3 / Parent-visible changes in round 3". It declares only `.rs_agg_i (1'b0)` for `tb/verilator/nvm_cosim/cosim_top.sv`. The failures are left to "the pin-adoption lane reconciles those cases with DR2c", attributed to "the binding manager's DR2c backoff".
  - The round-1 list declares the top's `NVM_RETRY_BACKOFF_CYC_P` only.
  - Processor side:
    - `hdl/acmp/KL_acmp_nvm_shadow.sv:136`: `RETRY_BACKOFF_CYC_P = 50_000_000`, a constant referenced to 100 MHz;
    - the top binds it to `NVM_RETRY_BACKOFF_CYC_P = ceil(CLK_HZ_P / 2)` (`hdl/top/protocol_processor_top.sv:151`, `:2560`).
  - Parent side, dev `b5c0f69d`:
    - `tb/verilator/nvm_cosim/cosim_top.sv:253-257` instantiates the module directly at `CLK_HZ_P = 1_000_000`. It sets only `RS_TMO_CYC_P`, "derived the way it derives it", because the file transcribes the top's producer path;
    - `cosim_cases.cpp:488`: B1-B4 allow `idle(1500)` for "debounce, three attempts, give-up".
- **Authority.**
  - Issue #131 assignment 5868003073: "Any parent-visible change is declared in the PR body for the parent pin-adoption lane".
  - The round-3 assignment: "No interface change beyond the declared ones".
  - This review's item 5: the list must be complete.
  - DR2c: 3 attempts, 500 ms apart.
- **Evidence.** `scripts/nvm_cosim_variants.sh` builds scratch copies of the parent at dev `b5c0f69d`, which are never committed. Each variant runs `run_cases.py --shapes 1x1 --skip-mutants`, the `quick` target.

  | Variant | Processor | `cosim_top` / B1-B4 edits | Result |
  |---|---|---|---|
  | base | `c951a9ff` | none | **315 / 315** |
  | head | `cbbb5acc` | `rs_agg_i` tied 0 | **308 / 315**: the author's 7 (B1-B4 `later_record_persists@end:0x21`; `restores_last_verified` after B1, B2, B4) |
  | ruled | `cbbb5acc` | as head, plus `.RETRY_BACKOFF_CYC_P((CLK_HZ_P/2)+(CLK_HZ_P%2))` | **311 / 315**: a different four (B1/B4 `last_verified_kept@end:0x20` and their power-cycle restores) |
  | ruledlong | `cbbb5acc` | as ruled, plus B1-B4 `idle(2600)` | **315 / 315** |
  | headlong | `cbbb5acc` | as head (module default), plus B1-B4 `idle(102000)` | **315 / 315** |

  - **The timelines** are in `receipts/nvm_cosim-B1-B4-timelines.txt`, with port operation end cycles in µs at 1 MHz.
    - **Head.** Attempt 1 of record 0x20 errs at 2,730 ms, and the next would follow 50 s later. At `end` (6,730 ms) the status reads `pend 1`, `alarm 0`, `mgr_dirty 3`, so the change is reported as pending and nothing is lost. The later record 0x21 is simply queued behind the serial flush engine.
    - **Ruled.** The attempts land at 2,730, 3,230 and 3,730 ms, 500 ms apart. The case's fault window closes at about 3,730 ms, so B1's and B4's third attempt succeeds and the case premise (give-up) breaks.
    - **Ruledlong.** Three failed attempts are followed by the sticky alarm. Record 0x21 is written at 5,330 ms and restored after the power cycle.
    - **Headlong.** Attempts at 2,730, 52,730 and 102,730 ms. Record 0x21 is written at 104,730 ms and restored.
- **Answer to item 4.**
  - No write is lost: every later record persists and restores once the scenario outlasts the backoff.
  - The ruled contract admits a SET lost to a power cycle inside the backoff window, provided the loss was reported at the cut:
    - DR2a: "No unconditional durability promise";
    - D3 §7.1: durable only when a verified slot holds the change;
    - §7.2 K18a/b: `power_cut_loses_only_unsaved`;
    - FASTCONNECT §16: "The last verified snapshot survives; unsaved changes may be lost. Every lost change was reported at the cut. Its reporter was producer pending or `nvm_dirty`";
    - FASTCONNECT §9.3: durable needs `nvm_pend` 0.
  - At head the cut happens with `pend 1` and the durable claim is never made: `no_durable_claim@end` passes, and all 7 failures are persistence or restore checks.
  - The backoff also holds the binding manager's *other* records behind the failing one, for up to 2 × 500 ms at ruled values. No ruling forbids that for this producer.
- **Impact.** The manager's consumer bank now runs nvm_cosim `quick`. A pin-adoption lane that follows the PR body would tie `rs_agg_i` and still fail 7 checks. Or it would "reconcile" B1-B4 against a 50 s backoff that is not the ruled one, which leaves the suite no longer a transcription of the top. Two parent edits are needed and neither is declared.
- **Required outcome.**
  - The PR body's parent-visible list names both `cosim_top.sv` edits: `.rs_agg_i (1'b0)` and `.RETRY_BACKOFF_CYC_P` bound as the top derives it.
  - It names the B1-B4 window extension past the debounce and both backoffs. With 2,600 ms, 315 of 315 pass.
  - It corrects the attribution: the failures come from the 100 MHz module default at the suite's 1 MHz clock.
- **Verification.** Run `scripts/nvm_cosim_variants.sh ... ruledlong` and get 315 of 315; re-read the PR body's list.

### F2 - MINOR - Conformance, Tests - three pre-proof variants of the clarified aggregate are unguarded; each mutant passes every pp_top check

- **Where.**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:603-604`: `proof_w` has two branches, W_IMG with the store's level and W_IMGLOC with the writer's own LOCATE hit.
  - `:566`: `agg_past_w` tests the count, not the fired level.
  - `:567`: `agg_o = agg_fired_r`, "level ... until reset" per the port contract `:206-208`.
  - `:810`: the proof's DEFAULTS path.
  - `tb/pp_top/d3_phases.hpp:1702-1790`, D3R14: both arms power up with the image in memory at reset, so the valid arm always proves by W_IMG. My D1 "valid" arm confirms this (D3 walk longest wait 0).
  - The in-tree `proof_reads_records_past_bound` removes the whole `:810` branch, so it never separates the two proof branches.
- **Authority.**
  - The clarification (5876655419): after a WAIT-GO expiry, "the D3 walk then proves the image, with no further NVM record reads, and ends DEFAULTS".
  - Parent §6.2 IMAGE row and §8.1 steps 1, 2 and 6: `configure_fabric` precedes `load_aem_image`, and "if the descriptor store holds no validated image, a LOCATE of ENTITY 0 makes it walk the one the firmware loaded". In the product order the proof is therefore the writer's LOCATE.
  - The ratification: the aggregate is an enforced bound, with a negative control.
  - §18.1 Negative controls: "boundary ... and indefinitely delayed inputs"; "Each must fail a named ... assertion".
  - This round's own edges: expiry on the exact proof clock, and with an event in hand.
  - The same class as R391-2 F1, which the author resolved for the D3 writer with D3R16/D3R17.
- **Evidence.** `scripts/r391_3_mutants.py` plants each mutant. `receipts/mutants-r391-3-d3only.log` has the D3 section at 120 of 120 for each. `receipts/mutants-r391-3-survivors-fullsuite.log` has the whole default build at 7,855 of 7,855 for each.

  | Mutant | Edit | Observable defect |
  |---|---|---|
  | `proof_default_only_from_img` | the `:810` DEFAULTS taken only when `ws_r == W_IMG` | P9 scenario 3 (image loaded after reset): **1,974 of 5,802** runs prove by LOCATE after the bound, then read all 108 D3 records and end COMPLETE, cause 0, e.g. at clock 7,512 for a bound of 2,800. Full scale, D1 "lateslow" arm (`receipts/probe-D1-mutant-proof_default_only_from_img.log`): **COMPLETE 2,141,220 clocks (2.1 s) after the bound, 108 D3 record READs past it, firmware budget exceeded**. The golden ends DEFAULTS +545 with 0 READs. |
  | `proof_past_bound_needs_fired` | `agg_past_w = agg_fired_r` | P9 scenario 2, h 1467: the bound lands on the W_IMG proof clock. The expiry is registered one clock late, the walk leaves proven with the aggregate spent and reads 108 records: COMPLETE at 7,511 for a bound of 2,800. The golden sweep contains the same clock and ends DEFAULTS, 0 READs. |
  | `agg_o_pulse` | `agg_o = agg_expire_w`, one clock | P9 scenarios 2-3: **476 of 5,802** runs had a binding byte in hand on the expiry clock. The binding walk then reads on unfailed and restores bindings after the bound; the terminal lands up to 1,843 clocks past the bound, against 579 in the golden. With probe D1's device, the walk would run on to its natural end, about 3.3 M clocks. |

  - A fourth mutant is **equivalent in effect**: `bind_agg_ignores_byte_in_hand`, which fires in H_RS_STREAM even with a byte in hand. It gives 0 of 5,802 deviations, and every graded later SET persists. The walk fails whole either way, and a `done` in hand ends the drain.
  - A fifth is **KILLED** by D3R14: `bind_agg_only_between_records`.
- **Impact.** The head's RTL is correct on every one of these paths. However, a regression on any of them would silently remove the enforced 1,000 ms bound, in two of the three cases on the product's own boot order. That reintroduces the multi-second dark entity the ratification exists to prevent, and no gate would notice.
- **Required outcome.** Named checks that fail on each mutant:
  - A D3R14 arm with no image at reset and the image loaded before `PP_CTRL[1]`, proven by the writer's LOCATE after the bound. It must end DEFAULTS, cause 3, within one per-wait deadline, with no D3 record READ.
  - The bound on the image proof's own clock, in W_IMG, and in W_IMGLOC with the answer in hand. The walk must end DEFAULTS with no D3 record READ.
  - A binding byte in hand on the expiry's clock. The walk must fail whole at its next waiting clock.

  The three mutants join `d3_mutants.py` with README rows, KILLED.
- **Verification.**
  - `scripts/run_r391_3.sh ... d3 <mutant>` fails for each of the three.
  - `d3_mutants.py` kills every mutant from the tree, and the goldens pass.

### S1 - SUGGESTION - Docs - the firmware wait is exactly 1,000 ms plus two per-wait deadlines

`docs/guides/integrator.md:430-432` says: "The terminal follows the bound within one per-wait deadline, or within two when a roll-back runs after it ... cover 1,000 ms plus 40 ms".

- **From the writer's equations,** the worst case is: the bound, plus the first clock with no event in hand (at most 8 clocks in P9), plus the roll-back's two strobe clocks, plus a debt wait of up to `NVM_RS_TMO_CYC_P`, plus a re-LOCATE of up to `NVM_RS_TMO_CYC_P`.
- **So the bound can be exceeded by a few clocks,** before the firmware's own lead over the accepted start is counted.
- **The practical margin is about 20 ms,** because the store's 4,096-clock watchdog bounds a re-LOCATE fetch. Every terminal I observed is within the budget: D1 at most +4,105, P9 at most +15,561 at a 2,800-clock bound.
- **The firmware's wait decides nothing** (parent §8.8).

Consider saying "plus a few clocks", or recommending a small margin.

### S2 - SUGGESTION - Docs - two wording points in the terminal tables

- **The integrator's `NVM_RS_AGG_CYC_P` row** (`integrator.md:91`) says "CLOSED only if the image cannot be proven, or if the bound falls inside that roll-back".
  - A bound cannot fall inside a roll-back that it started itself. Step 3's own bullet says it right: "inside a roll-back that another fault had started".
  - A roll-back the bound started can still end CLOSED if its re-LOCATE fails.
- **07 §5.3's table** has no row for the image proof's own per-wait deadline. That path gives CLOSED with cause 3 and no roll-back, as the writer banner (`KL_aecp_nvm_writer.sv:72-73`) states. It is reachable only when `NVM_RS_TMO_CYC_P` is set below the store's image walk, which the guide forbids.

### S3 - SUGGESTION - RTL, Robustness - the binding manager's backoff default only fits 100 MHz

`KL_acmp_nvm_shadow.sv:133-136` defaults `RETRY_BACKOFF_CYC_P` to 50,000,000, which is right only at 100 MHz. Every direct instantiator at another clock inherits a wrong DR2c spacing silently; F1 is one instance. Consider stating in the banner that direct instantiators must derive it from their clock, or deriving the default from a clock parameter.

## Items of this round

1. **`f8d1a83`, the clarification.** Met in RTL, as shown under Verdict. The edges I hunted:
   - **Exact proof clock.** The LOCATE hit and the refusal each land unfired on the bound's own clock. They give DEFAULTS cause 3 with 0 READs, and CLOSED cause 7. An expiry in W_IMG is handled by `agg_past_w`.
   - **During the proof.** There are 579 W_IMGLOC expiries in P9, all DEFAULTS, or CLOSED cause 7 when refused.
   - **Event in hand.** P9 has 648 binding walks with a byte in hand at `agg_o`'s rise. Each either ends its read on the event it holds or fails whole at its next waiting clock under the fired aggregate, at most 2 clocks later. D3R17 covers the writer's grant, and the golden sweep covers every D3 state with at most an 8-clock edge.
   - **Pre-proof expiry, then an unprovable image.** The restore reads cause 7. I agree with that reading: the aggregate aborted nothing, and §6.2's IMAGE row names the first abort.
   - **Firmware wait.** See S1.
   - **Coverage.** The coverage of three of these paths is F2.
2. **`9d66095`, both guides.**
   - Both guides list every terminal the aggregate can take, and both causes of CLOSED. They agree with 07 §5.3: the parameter row, bring-up step 3, the operator outcome table, the CLOSED paragraph, the troubleshooting row and diagram 23.
   - `make check` returns rc 0, including freshness and links.
   - Two wording nits are in S2.
3. **`58c5fe9`, `e94bea8`, `cbbb5ac`.**
   - The in-tree driver reports 69 of 69 KILLED, goldens PASS (`receipts/d3_mutants-intree*.*`).
   - My own copies of `agg_fires_with_event_in_hand`, `agg_not_stopped_at_terminal` and `resident_never_returned` are KILLED, by D3R17, D3R16 and D3O7.
   - The mutants I wrote against the pre-proof path are covered under F2.
4. **Parent consequence.** No write is lost, and the contract admits a pending, reported loss at a cut. The PR body's attribution and adoption list are F1.
5. **DR4 and the parent-visible list.**
   - DR4: +1,030 LUT / +559 FF / 0 BRAM / 0 DSP at 1x1 is in the PR body, within the 2,500 / 1,400 ceiling. I did not re-measure it (Limits).
   - The parent-visible list has the five round-1 ports, `NVM_RS_AGG_CYC_P`, the ceil per-wait default, snapshot word 37, the classifier line and the `rs_agg_i` tie.
   - It lacks the nvm_cosim backoff binding and the B1-B4 extension (F1).

## Judgement per section 18.1 sentence (delta only)

| Sentence | Judgement at cbbb5acc | Evidence |
|---|---|---|
| Measure its 1,000 ms aggregate ...; include both walks and roll-back to COMPLETE, DEFAULTS or CLOSED | met, now with the clarified pre-proof path | D1 arms, P9 golden, D3R13-D3R17 |
| Exercise zero, boundary, corrupt, refused and indefinitely delayed inputs | met in RTL; three pre-proof boundary variants are ungraded | F2 |
| Each must fail a named ... assertion | met for the in-tree 69; not for F2's three | `receipts/d3_mutants-intree.log`, F2 |
| Release AECP/ADP early (negative control) | met | D1: 0 early enable cycles in every arm, AECP released only at DEFAULTS |
| Re-run the processor's full required gates | the author's claim; I re-ran the delta's suites only | `suite-*.log`, Limits |

## IEEE 1722.1 / Milan behaviour relied on

- Milan §5.6.1 (via F07.9): ADP may start only once the restore is done. It holds in every D1 arm (`adp_enable` only at DEFAULTS, 0 early cycles).
- IEEE 1722.1-2021 AECP command timeout: a dropped held AECP command is retried by its controller. It is unchanged from round 2: P1/P2 at head match round 2 exactly.

## Round-2 findings of this reviewer, at this head

| R391-2 item | Disposition at cbbb5acc | Evidence |
|---|---|---|
| F1 MINOR, post-terminal inertness and no-event-in-hand firing unguarded | **Resolved** | D3R16 and D3R17 kill my `agg_not_stopped_at_terminal` (3 checks) and `agg_fires_with_event_in_hand` (2 checks), plus the in-tree copies |
| F2 MINOR, a WAIT-GO expiry ends CLOSED | **Resolved** per the clarification | RTL `:544, :810`, `rs_agg_i`. D1 arms. The P9 golden reproduces the author's count: 452 pre-proof expiries in scenarios 0-1, all now DEFAULTS. Docs updated. F2 of this round is a new coverage finding on the clarified path, not a retention. |
| S1, the resident count never decremented | **Taken** | D3O7 kills `resident_never_returned` |

My round-1 findings F1-F4 stay resolved. D3O5 and D3O6 pass. My P1/P1b/P1c/P2 admission probes and P3-P5 restore probes give the same readings at head as at round 2 (`receipts/probe-R391-2-P1-P6-at-head.log`). The round-2 P6 wrap anchor moved, and P9 supersedes it.

## Hosted evidence (read-only)

Workflow `hdl` ran at the exact head on `push` (run 36489797787) and on `pull_request` (run 36489801151). Both completed with success. Six jobs executed and none were skipped: `docs-gates`, `portability` and `suites`, twice each (`receipts/hosted-check-runs-head.txt`). The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | clarification 5876655419, the round-3 assignment and the ratification clause by clause; parent §6.2, §6.3, §7.1, §8.1, §8.8, §18.1 and FASTCONNECT §9.3/§16 against the writer (`KL_aecp_nvm_writer.sv:56-80, 520-620, 650-816`), the binding manager (`KL_acmp_nvm_shadow.sv:69-80, 150-155, 536-562`) and the top wiring (`protocol_processor_top.sv:2553-2566, 3621-3625`); the PR body's parent-visible lists against the parent's direct instantiation (`cosim_top.sv:253-257`) | R391-3 | cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 |
| RTL | CLEAN | full read of the round-3 HDL delta; `expire_w` gating by `proven_r`; `agg_past_w` by count; `proof_w` both branches; `rs_tmo_w` in H_RS_REQ and H_RS_STREAM with its drain; zero-tolerance lint of the four touched modules (0 findings); P9 golden, 0 deviations | R391-3 | cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 |
| Robustness | CLEAN | D1 (5 arms, derived deadlines); P9 (17,406 runs, 6 scenarios: erased or saved bindings, per-byte-slow device, late image, refused image, a pass-1 disagreement, owed descriptor debt; the device face re-proven after it, ACMP in CLOSED); the parent nvm_cosim variants (no loss, no durable claim over a pending change) | R391-3 | cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 |
| Tests | UNCLEAN (F2, F1) | `d3_phases.hpp` D3R14-D3R17, D3O7; `d3_mutants.py` (69/69 from the tree); my 20 mutants (16 KILLED, 1 equivalent in effect, 3 surviving the whole default build); pp_top `make run` 7,875/7,875, acmp_nvm 353/353, rx_validator 437/437; the parent nvm_cosim quick loop in five variants | R391-3 | cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 |
| Docs | UNCLEAN (F1) | 01 F01.5, 03 rule (e), 07 §5.3 (both tables), 08 F08.1, 09 §7, integrator (parameter row, §4.1, bring-up step 3), operator (outcome table, CLOSED paragraph, troubleshooting row), diagram 23 SVG, the pp_top/acmp_nvm README mutation rows; `make check` and `gen_matrix.py --check` rc 0; the PR body (rounds 1-3) | R391-3 | cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 |

## Real limits

- **Simulator.** The simulator path named in the brief, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`, does not exist on this host.
  - I used a copy of the byte-identical sibling wrapper (sha256 `905795b9...`, identical across all 175 sibling wrappers on the host).
  - It executes a binary with sha256 `fb2cc573...` that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator-identity.txt`).
  - This is the same identity as rounds 1 and 2.
- **What I did not run:**
  - the full processor bank: `run_suites.sh` over all 33 suites, full `lint_hdl.sh`, srp_top mutants, nvm_port figures;
  - any Yosys or builder bank;
  - xvlog and the evidence classifier;
  - the full parent consumer set: only nvm_cosim `quick`, in scratch copies.
- **DR4 not re-measured.** The instrument is Vivado out-of-context, which is not available on this host. The 8x8 diagnostic moves between rounds (+1,270, +795, then +1,067 LUT) with no matching RTL change. DR4 acceptance is 1x1 only (DR4 ruling), so this does not bear on the ceiling, but the manager may want the instrument's baseline recorded per round.
- **Parent copies.** The parent copies are local clones at dev `b5c0f69d`. `protocol-processor` is at the named sha. `gptp-processor` and `third_party/verilog-axis` are at the parent's gitlinks, from their public remotes. The only edits are the ones named in F1's table.
- **Simulation only.** The bench compresses its protocol timebase; the NVM deadlines derive from a nominal 1,000,001 Hz clock.
  - P9 overrides `NVM_RS_AGG_CYC_P` to 2,800 in disposable copies.
  - D1 runs at the top's own derivations.
  - Physical calibration was NOT RUN, field skips are not hardware proof, and nothing here is hardware proof.
- **Probe grader.** My first P9 grader flagged three kinds of run as deviations that were correct behaviour:
  - a read that ended on the event in hand at `agg_o`'s rise;
  - a proof on the bound's own clock;
  - a refusal on the bound's own clock.

  The published grader keys on a waiting clock under the fired aggregate and accepts both on-clock paths. The published golden receipt comes from it.
- **Clone hygiene.** Every build, probe and mutant ran on exported copies or local clones under this packet's `scratch/`. At the end the clone was re-verified (`receipts/clone-integrity.txt`):
  - HEAD, the tree and the index agree;
  - all 312 work-tree blobs rehash to their tree blobs, and the modes match;
  - status, ignored files included, is empty;
  - there are no gitlinks and no `.gitmodules`, so no submodule gitlinks are required.

## Pending manager duties

- Adjudicate F1 and F2 into the next round:
  - F1 is a PR-body correction with evidence;
  - F2 needs named checks and three in-tree mutants.
- Carry into the pin-adoption lane:
  - the `cosim_top.sv` edits (`rs_agg_i`, and `RETRY_BACKOFF_CYC_P` derived as the top does);
  - the B1-B4 window extension;
  - the five round-1 ports and `NVM_RS_AGG_CYC_P`;
  - the snapshot word 37;
  - the classifier disposition for `d3_mutants.py`.
- Run the donor full bank and the parent consumer bank (with nvm_cosim lint and quick, milan_dp, milan_dp_render) at dev `b5c0f69d`.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`).
- Own hosted and act acceptance, and record that physical calibration is NOT RUN.

## Prior public findings of the other reviewer, resolved or retained at this head

These were read after the verdict, findings and ledger above were written.

| Finding | Status at cbbb5acc | Evidence |
|---|---|---|
| R390-1 F1-F4, S1, S2 | stay **resolved** (as R390-2 recorded) | D3O5/D3O6 pass; the in-tree driver kills its 69; `09_verification.md:197-199` |
| R390-2 F1 MAJOR, a pre-walk expiry ends CLOSED with a valid image | **Resolved** | the clarification is implemented (D1 arms, P9 golden); D3R14 with `agg_closes_before_proof` KILLED; F2 of this report extends its coverage |
| R390-2 F2 MINOR, the guides misstate the terminals | **Resolved** | item 2 above; S2 nits only |
| R390-2 F3 MINOR, roll-back span ungraded | **Resolved** | D3R15; in-tree `agg_not_in_rollback` KILLED by both arms |
| R390-2 S1, `RX_SLOTS_P` floor | not taken (not assigned) | no check or statement added |
| R390-2 S2, `agg_ignores_in_hand` | **Taken in effect** | D3R17 grades a grant on the bound's own clock; `agg_fires_with_event_in_hand` KILLED |

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`. Scripts take a processor checkout, a scratch directory and a directory holding a Verilator 5.050 `verilator`. None of them writes into the checkout.

**Scripts.**

- `scripts/run_r391_3.sh <checkout> <rev> <scratch> <verilator dir> <probe> [args]` runs these probes:
  - `d1 [MUTANT]`: the D1 arms (`scripts/r391_3_d1.hpp`);
  - `sweep AGG STEP SCENS [MUTANT]`: the P9 sweep (`scripts/r391_3_sweep.hpp`);
  - `d3 [MUTANT]` and `full [MUTANT]`: the D3 section or the whole default build, with an optional planted mutant from `scripts/r391_3_mutants.py`.
- `scripts/nvm_cosim_variants.sh <parent clone> <parent rev> <checkout> <scratch> <verilator dir> <variant> [jobs]` runs the parent nvm_cosim quick loop in a scratch parent. It needs `GPTP` and `VAXIS` (local clones of those public remotes). The variants are `base`, `head`, `ruled`, `ruledlong` and `headlong`.
- `scripts/cosim_b_timeline.py <scratch> <variant>...` produces the B1-B4 timelines.
- The round-2 probes were re-run with the R391-2 packet's `scripts/run_probes2.sh`, with build parallelism capped at 4.

**Receipts.**

- **Gates and suites at head:**
  - `receipts/make-check-head.log`, `gen-matrix-check-head.log`, `lint-touched-head.log`;
  - `suite-pp_top-head.log` (7,875/7,875), `suite-acmp_nvm-head.log`, `suite-rx_validator-head.log`;
  - `pp_top-d3-only-head.log` (120/120).
- **Mutants:**
  - `receipts/d3_mutants-intree.log` and `d3_mutants-intree-results.json` (69/69 KILLED, goldens PASS);
  - `mutants-r391-3-d3only.log` (my 20);
  - `mutants-r391-3-survivors-fullsuite.log`.
- **Probes:**
  - `receipts/probe-D1-head.log` and `probe-D1-mutant-proof_default_only_from_img.log`;
  - `probe-P9-aggsweep-golden.log` and `probe-P9-aggsweep-mutant-*.log` (4);
  - `probe-R391-2-P1-P6-at-head.log`.
- **Parent:** `receipts/nvm_cosim-quick-{base,head,ruled,ruledlong,headlong}.log` and `nvm_cosim-B1-B4-timelines.txt`.
- **Environment:** `receipts/hosted-check-runs-head.txt`, `clone-integrity.txt`, `verilator-identity.txt`.

R391-3 FINISHED
