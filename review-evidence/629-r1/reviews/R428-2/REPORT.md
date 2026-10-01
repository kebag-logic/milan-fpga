[R428] NEGATIVE - exact head c554ae51b1dcc2285863f0f0117cb025971a594c

# R428-2: internal cleared-context re-review of PR #631 (#629, lane M1, design only)

- **Head:** `c554ae51b1dcc2285863f0f0117cb025971a594c`, tree `20c142998c6802e6c6730adfb814ec2a001af7b4`. It is three docs commits on round 1's `78d4fef2`: `4845f158` (the round-2 answers), `49899572` (three tightened statements) and `c554ae51` (the shape-header glob fix). Source base and live dev are both `d4dd742679b902b2bc5eedf89d525066d59aafbb`.
- **Diff against base:** `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new, 884 lines) and its row in `docs/README.md`. No RTL, builder, model, configuration or processor change.
- **Read, in this order:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - #629's body and its comments: the lane M1 assignment 5935051587, the rulings 5935520588, the round-2 assignment 5935864862, the DECISION 5936327987, the round-2b assignment 5936355573 and REVIEW READY 5936429406;
  - the clause texts (Milan v1.2; IEEE 1722.1-2021; IEEE 1722-2016), read from local copies that are not republished;
  - the diff and its history, and the code at the head;
  - the author packets `review-evidence/629-r1/author-r2/` and `author-r2b/`;
  - the PR body and the hosted checks.
- **Prior public findings** (R428-1 and R429-1) were read only after my own pass over the diff. Each is resolved or retained below.

## Verdict in one paragraph

Round 2 answers every round-1 finding of both reviews; all eleven are resolved at this head. The input contract now holds:

- the 48 kHz base format only (Milan v1.2 6.2, Table 6.1);
- `stream_data_length` = 24 x `channels_per_frame`;
- groups of 16 by `sequence_num` modulo 16, which stay aligned across the 8-bit wrap;
- the group-mean pick and the 4,096 ns bound.

Re-run under the page's full rules, the bound gives zero history restarts at the 10.8-sized error (+/-1,042 and +/-1,426 ns) under every error shape tried, at 0 and 300 ppm. It also rejects a one-sample step at every group position. The `mr` re-seed, the rewritten (b) and (c), the up-to-date rulings, D1's new grounds and D5's options all hold.

Three MINOR findings remain open, all in the round-2 text that argues for the meter and for its tests:

- **F1:** the desk model behind the page's table omits the page's own within-group void rule. Under the stated rules, its +/-2,500 ns row is wrong.
- **F2:** the "group" error shape is presented as a bounding case. For the servo's 2 ppm lock test it is the best case, and 10.8-sized error that is correlated within a group still fails that test with the mean.
- **F3:** one named switch-test mutant cannot fail its row, because the restart engine's #387 merge absorbs it. The rationale sentence behind it is inaccurate in the same way.

## Judgments on the assigned items

**1. AAF meter input rules (round-1 F2 here, R429-1 F2/F3): hold.**
- Milan v1.2 6.2 fixes 32-bit PCM AAF with NS = 6 at 48 kHz in normal timestamp mode, and Table 6.1 and Table 6.2 confirm it. The page restricts the meter to exactly this (`:410-438`).
- `stream_data_length` = 6 x 4 x `channels_per_frame` is right for INT_32BIT. The meter checks it because the RX monitor's family compare does not check the sample count (`KL_avtp_rx_monitor_ctx.sv:486-491`, verified). Every advertised input format has 6 samples per PDU (`avdecc/aem_descriptors.py:133`; `0x0205022000806000` and `0x0215022002006000` decode to 6 samples per frame).
- 16 divides 256, so the groups by `sequence_num` modulo 16 stay aligned across the wrap. The probe ran 10 s continuous (312 wraps) with 0 restarts. A continuity check without the 8-bit wrap gave 313 restarts, so that mutant fails (`receipts_probe.out`, the `wrap` lines).
- The parser nets the page names exist (`milan_datapath.sv:5418-5446`). The `tu` trap is real: `KL_crf_rx` takes `avtprx_tv_bit` (`:5530-5534`), while the common-header `tu` is byte o+3 bit 0 (`avtp_stream_parser.sv:175`).

**2. The bound and the mean against the servo's 2 ppm lock test, and step rejection.**
- **The bound holds.** The probe implements every rule the page states, including the within-group void (`:457-459`) that the author model omits. Under each shape (independent, group-alternating, group random-sign, group-uniform, and 10 ms, 100 ms and 1 s sine wander), at +/-1,042 and +/-1,426 ns and at 0 and 300 ppm, the 4,096 ns bound gives 0 restarts and 0 voids. `rate_valid` reaches the run ceiling of 0.9957. The arithmetic agrees: two picks at 1,426 ns plus 601 ns of rate term is 3,453 ns. Within a group, 2 x 1,426 + 562 is 3,414 ns. Both are under 4,096 ns.
- **A real step is rejected.** A one-sample step (+/-20,833 ns) restarts the history once at each of the 16 group positions, and so does a half-sample step. It is caught either by the within-group void or by the pick spacing. Sub-bound steps of 2,000 to 4,000 ns, where not voided, enter the rate as one transient of up to about 5,000 ns per window, about 9.7 ppm with noise. That matches the page's "at most about 8 ppm" plus noise (`receipts_probe.out`, the `step` lines).
- **The mean passes the lock test for independent per-PDU error and for slow wander.** At +/-1,042 and +/-1,426 ns independent, P2 puts 1.000 of windows under 1,024 ns, against 0.57 to 0.75 for P1. This reproduces the page's numbers.
- **The mean does not pass it for 10.8-sized error that is correlated within a group but not across 512 ms (F2).** The page's +/-2,500 ns P2 row also does not survive the page's own void rule (F1).
- **The author model reproduces byte for byte** at the published evidence (`author_model_rerun.txt`: sha256 `2a20b767...3b19` for both the published and the re-run output, `cmp` rc 0). The page's table transcribes it faithfully.

**3. `mr` re-seed on a change of the followed input (R429-1 F4): holds.**
- An era starts at a change of the followed listener and at entry into AAF following. It clears the lock with no disruption trigger and seeds the received `mr` silently (`:540-546`, `:636-641`).
- `KL_crf_rx` keeps tracking its `mr` level on every accepted PDU whether or not CRF is selected (`KL_crf_rx.sv:380`, `:586-587`). A switch onto CRF therefore raises no stale echo.
- The meter row (`:816`) grades the no-re-seed mutant deterministically, and the root row (`:820`) drives opposite `mr` levels.
- The second mutant in `:820` is not graded (F3).

**4. Test-plan gaps (R428-1 F4, R429-1 F5): each named gap now has a row.**
- The rows cover W2 at the root (`:819`), the D5 counters (`:823`, and the lock-loss bench row), the CSR words (`:824`), and the true-ratio leg at +20 and -15 ppm with the mux-stuck mutant (`:818`).
- Decimation by 1 now "never validates" (`:808`). That is correct under the rules, since a 125 us spacing is outside 2 ms +/- 4,096 ns.
- The stale-decode-table AECP mutant (`:825`) is a real mutant: the last index is accepted, reads back and decodes as no source.
- `rate_valid` is asserted wherever a rate is compared (`:802-804`).
- The one exception is F3.

**5. Clause wording, (b) and (c): holds against the texts.**
- **(b)** now separates three things: what the clauses require (5.3.11.1, 5.4.2.15, 5.3.11.2 and Table 5.7, which leaves "locked" to the manufacturer), what they permit (5.3.11.1's dynamic change; the 10.6 free-wheel; the 4.4.4.7 NOTE), and this design's choice of no fallback. Each quotation matches the clause text. The 10.6 paraphrase drops "due to network packet loss" (S3).
- **(c):** 4.4.4.3 paragraphs one, three and last, 10.4.3, PICS F.7 AAF-5 and AAF-6, 10.8 Equations (15) and (16), and 4.3.5 are quoted and assigned correctly. The two "need not be seamless" quotations now sit with the received-toggle case only (`:129-132`, `:140-143`).

**6. The page against the rulings: current.**
- #632 and protocol-processor #141 are named and linked (`:20-28`, `:718`, `:767-770`).
- The Decisions table shows D1 and D5 re-opened, D2, D3 and D6 ruled, D4 with the owner and D7 filed.
- D2's ruled wording ("keeps one AAF timestamp in 16", 5935520588) differs from the mean of 16. The round-2 assignment authorised replacing the pick ("D2 ... stand, subject to the design fixes below"), and the page states the change inside D2 (`:379-380`, `:852`). The DECISION comment records the wording change for the manager. The page itself does not quote the superseded wording (S4).

**7. D1's new grounds: valid, and L1 stands on them.**
- The saved-state argument is withdrawn correctly. The source set is model shape (`endstation_builder.py:3412-3419`), and a model-id mismatch is refused whole: `milan_baremetal.c:634-636` returns `VD_SHAPE` (see also `SAVED_STATE_FASTCONNECT.md:638-640` and `SAVED_STATE_MATERIALIZATION.md:1153-1158`).
- L1's remaining merit is real: the CRF index is 1 wherever INTERNAL and CRF are both declared, independent of the listener count. The places that select CRF by index say exactly that: `test_builder.py:19588`, `milan_soc.py:872-874`, `tb/verilator/mmcm_servo/sim_main.cpp:197`, and B6's SET_CLOCK_SOURCE 1.
- The page states the shape caveat (CRF is 0 without INTERNAL, `endstation_builder.py:4262-4267`, `:5034`). No clause decides the order.
- I agree with L1. Ruling it is the manager's.

**8. D5's options: complete and fairly stated.**
- The history behind the recorded rule checks out:
  - the "one clock-validity authority" banner first appears in `c947acd8d` (2026-08-14, VERSION 0x0047);
  - its current wording was revised in `223d20184` (2026-08-24);
  - the stored source first reached the media plane in `c92159ac9` (2026-09-02).
- The options:
  - C0 keeps the rule.
  - C1 follows the servo's LOCKED. The servo drops from LOCKED to ACQUIRE on one window outside 2 ppm and needs four windows to re-qualify (`KL_mmcm_drp_servo.sv:232-233`, `:567-568`, `:689-694`), so the page's "one pair per about 2.5 s" upper bound holds.
  - C2 follows the reference lock.
  - C3 rightly reads 4.4.4.7 as being about gPTP discontinuities, so raising `tu` for media lock widens it.
- C1's counter churn depends on the timestamp error shape (F2).
- Recommending C1 is reasonable, and C2 is a sound alternative if counter churn matters. The ruling is the manager's or the owner's.

**9. Gates, link and privacy: met.**
- At the head:
  - `scripts/check_entity_shape.py` gives rc 0, with 166 checks and 0 failures;
  - `docs_check`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_em_dash --base d4dd7426`, `check_doc_paths`, `check_gptp_docs`, `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, and `git diff --check`, both base..head and on the worktree, all give rc 0 (`gates/`).
- The glob fix is load-bearing. In a probe clone, restoring the glob adds exactly one arm-I failure, the `MEDIA_CLOCK_FOLLOWING.md` line, against an unmodified control clone (`gates/mutant_glob_*`, `gates/control_scratchclone_*`). The control clone lacks submodules, so both fail on unrelated lines; only the difference is evidence.
- The page and the PR body say "Relates to #629", and nothing closes it.
- A scan of the diff, the commit messages and the PR body found no host, peer, switch, instrument, address or private path.

## Findings

```text
[R428] MINOR Tests, Robustness, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:510-529 (row :524) against :457-459; review-evidence/629-r1/author-r2/meter_rules_model.py - the desk model omits the page's within-group void rule, and its +/-2,500 ns row does not hold under the stated rules
```

**F1**
- **Requirement/evidence:**
  - The page voids a group on "any `|ts_i - ts_0 - i * 125,000|` above the jump bound" (`:457-459`), and a voided group restarts the history (`:533-534`).
  - The author model's `grade()` tests only the pick spacing. `picks()` never applies the within-group test.
  - With the void applied, independent +/-2,500 ns error at 0 ppm voids 14,448 groups in 120 s, and `rate_valid` is 0.0000 under both P1 and P2. With the void switched off, the probe reproduces the page's 0.9957 (`receipts_probe.out`: `white 2500 0 mean 4096 void=on` against `void=off`).
  - The void sets an effective independent per-timestamp tolerance of about (4,096 - 562) / 2, roughly 1,767 ns at 300 ppm. The page does not state this.
- **Impact:** the page shows the mean giving margin to +/-2,500 ns, which its own rules cannot deliver. An implementation lane that builds the void as written gets a meter that differs from the evidence. One that builds to the evidence drops a stated rule.
- **Required outcome:** the evidence models the rules the page states, or the page changes or justifies the rule. The table row and the sentence after it match the corrected run. The page states the per-timestamp tolerance the void imposes.
- **Verification:** a re-run of the corrected model, with its output matching the page's table at the next head.

```text
[R428] MINOR Robustness, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:510-529, :463-464 - "two error shapes bound the cases" is false for the servo lock test: 10.8-sized error correlated within a group is not removed by the mean
```

**F2**
- **Requirement/evidence:**
  - The page's "group" shape alternates sign per 16-PDU group and is called "the shape no averaging removes". The table and text then present the two shapes as bounding the cases (`:513-516`, `:526-529`).
  - The servo's window error is the difference of two picks 256 apart (`KL_mmcm_drp_servo.sv:609`, `:648`). 256 is even, so an alternating-per-group error cancels exactly. For the lock test this is the best case, not a bound.
  - The probe ran +/-1,042 ns, inside IEEE 1722-2016 10.8 Equation (15), with P2, the 4,096 ns bound and zero restarts in every case (`receipts_probe.out`):

    | Error shape | Windows under 1,024 ns | Lock4 |
    |---|---|---|
    | random sign per group | 0.607 (0 ppm), 0.598 (300 ppm) | 0.137 |
    | uniform per group | 0.838, 0.880 | 0.556, 0.654 |
    | 10 ms periodic | 0.598 | 0.000 |

    At +/-1,426 ns the random-sign case falls to 0.500. P1 is no better in these shapes.
  - The page's claim, that the mean "keeps independent error out of the servo's lock test", holds only for independent per-PDU error and slow wander. It does not cover all error of 10.8 size.
- **Impact:** the page asserts that a talker at the 10.8 limit locks under P2. A talker whose timestamp error is correlated over a 2 ms group but not over 512 ms would leave the servo cycling between ACQUIRE and LOCKED, and under D5/C1 would move the CLOCK_DOMAIN counters at the stated maximum rate. Nothing before the bench, which grades one peer, would show it. P2 is still never worse than P1, so the choice stands; the claim is what is overstated.
- **Required outcome:** the page states which error shapes the mean removes and which it does not, and corrects "bound the cases". The unfiltered class is recorded as a limit or a bench observation, or is graded in the test plan.
- **Verification:** the page text at the next head, and a model run that includes a within-group-correlated shape.

```text
[R428] MINOR Tests, RTL, Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md:820 (second mutant), :636-648 - the "disruption trigger unmasked at a switch" mutant cannot fail its row; #387's merge absorbs the era-start request
```

**F3**
- **Requirement/evidence:**
  - Row `:820` says that with the disruption trigger unmasked at a switch, "the era-start lock fall requests a second restart", which its "exactly one toggle per output" check would catch.
  - The era start clears the meter lock "in one cycle" at the change of the followed source (`:544-546`), a few cycles after the source-change edge (`milan_datapath.sv:1560-1570`, `KL_media_clock_restart.sv:213`).
  - `KL_media_clock_restart.sv:236-246` merges any request that lands while a talker's target is pending, or while its adopted level has not yet been carried by a reported PDU (`hold_r == 0`).
  - Probe `mcr_merge_probe/` drives the unmodified module in the pinned HDL simulator (5.050) with two streaming talkers. A request at +2, +3, +5 or +30 cycles after the source change gives one wire toggle per talker, the same as the design. Requests at +600 and +1,600 cycles give a second toggle (`mcr_merge_probe/receipt.out`).
  - The rationale at `:643-648`, that a second request "from a meter lock fall, would land after it", is true only of a delayed fall, such as 100 ms of silence without an era start. It is not true of the era-start fall the mask exists for.
- **Impact:** a named mutant that the plan cannot show failing. This is the class round-2 item 3 asked to close, and it is the AGENTS section 6 Tests rule.
- **Required outcome:** the mask is graded where it is observable, for example the number of restart requests per switch at the engine's input. Otherwise the page records the mask as defence in depth with no wire-level mutant. The rationale names which lock fall can land after the merge window.
- **Verification:** the row and the rationale at the next head.

### Suggestions (optional; they do not affect coverage)

- **S1 (Docs), `:433-438`.** "Under the 16-PDU pick below, 3, 12, 24, 48 and 96 ... would also survive the sequence wrap, because 96 divided by the count divides 256" describes a per-format 96/spf pick, not the 16-PDU pick. Under the 16-PDU pick every count aligns, but the spacing is not 2 ms. The conclusion, refusing them all, is unaffected.
- **S2 (Docs), `:455-456`.** "The truncation of the division is the same in every pick" is not exact. `floor(sum / 16)` varies by up to 1 ns between picks as the rounded deviations vary. That is well inside the `:808` 1-LSB tolerance, but the sentence should say so.
- **S3 (Conformance, Docs), `:104-105`.** IEEE 1722-2016 10.6 reads "If CRF timestamps are lost due to network packet loss". The paraphrase drops the qualifier. The page already frames 10.6 as a nearest case, so the outcome is unchanged.
- **S4 (Docs), `:852`.** The D2 row could name the ruled wording ("keeps one AAF timestamp in 16", 5935520588) and say that the round-2 assignment's pick fix replaces it with the mean of 16, as the DECISION comment does. A cold reader of the page alone would then see the change.

## Prior public findings at this head

| Finding | Status at `c554ae51` | Evidence |
|---|---|---|
| R428-1 F1, D1's saved-selection rationale | Resolved | withdrawn with the refusal path cited (`:339-357`); the D6 consequence appears in the Configuration row, Decisions and Limits |
| R428-1 F2, meter input contract | Resolved | base format only, `stream_data_length` rule, modulo-16 groups, the stated 10.8 + 384 ns assumption, B2, test rows. New issues in the round-2 evidence are F1 and F2 above |
| R428-1 F3, C1 reverses a recorded rule | Resolved | explicit reversal with options C0 to C3 (`:674-708`); the banner rewrite is listed in the root row (`:757`) |
| R428-1 F4, test-plan gaps (a) to (e) | Resolved | `:819`, `:823` and the lock-loss bench row, `:824`, `:808`, `:825` |
| R428-1 F5, (b) states a choice as an obligation | Resolved | `:83-132`; 10.6 and the 4.4.4.7 NOTE are cited (S3 is a wording nit) |
| R428-1 F6, page not current with the rulings | Resolved | `:20-28`; Decisions table; #632 and protocol-processor #141 |
| R428-1 S1 to S4, O1 | Taken | (d)5 softened; A2 conditioned on a live feed (`:654-660`); citations corrected (`KL_aecp_nvm_writer.sv:501-503`, `:3937`, 871/792, `_load_names`, harnesses, (d)2's three places); shapes without INTERNAL (`:359-364`); O1 recorded as (d)8 |
| R429-1 F1, clause statements too strong | Resolved | "at most one" removed (`:72-76`); (b) rewritten; 7.6.2's consequence restated (`:70`) |
| R429-1 F2, CRF-derived jump bound | Resolved | 4,096 ns derived from 10.8 (`:487-508`); test rows `:809-810`; B AAF records the restart count (`:837`) |
| R429-1 F3, accept and decimation at the wrap | Resolved | 48 kHz base only, with the spf source named (`:410-445`); refusal test with 8 and 12 spf (`:811`) |
| R429-1 F4, second toggle on an AAF-to-AAF switch | Resolved | era re-seed on a listener change and on entry; opposite-level tests with a no-re-seed mutant (`:816`, `:820`). A related ungraded mutant is F3 above |
| R429-1 F5, three untested behaviours, two wrong failure modes | Resolved | `:819`, `:818` (+20 and -15 ppm, mux-stuck), `:808`, `:825` |
| R429-1 S1 to S4 | Taken | `:3112` stale comment; `_load_names`; offsets; the `tu` trap (`:401`); the CSR read window (`:761`); the 7.6 row; C1 explicit; the shape caveat |

## Lens coverage at this head

```text
[R428] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:62-218, :371-529, :626-650, :674-708 at c554ae51 - clause findings (a)-(d), the meter's format and timing basis, the mr rules and D5's options, checked against Milan v1.2 5.3.3.6, 5.3.11.1, 5.3.11.2 (Table 5.7), 5.4.2.15/.16, 6.2 (Tables 6.1, 6.2), 7.2.2, 7.2.3 and IEEE 1722-2016 4.3.2, 4.3.5, 4.4.4.3, 4.4.4.7, 7.2.4, 7.3.3, 7.3.5, 7.5, 10.4.3, 10.6, 10.8 Eq. (15)/(16), PICS Table F.7 AAF-5/AAF-6; S3 only (non-blocking)
[R428] MINOR RTL - see F3 (KL_media_clock_restart.sv:236-246 merge behaviour against the page's switch rationale and row :820); every other cited RTL range re-read at the head (milan_datapath.sv, KL_crf_rx.sv, KL_mmcm_drp_servo.sv, KL_media_grid_align.sv, avtp_stream_parser.sv, KL_avtp_rx_monitor_ctx.sv, milan_csr.sv, KL_aecp_nvm_writer.sv) holds as cited
[R428] MINOR Robustness - see F1, F2 (meter_rules_probe.py; receipts_probe.out)
[R428] MINOR Tests - see F1, F3 (test plan :797-845; mcr_merge_probe/receipt.out)
[R428] MINOR Docs - see F1, F2, F3; gates all rc 0 (gates/*.rc), the index row docs/README.md, the PR body and the public-text scan are clean
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:62-218`, `:371-529`, `:626-650`, `:674-708` against the clause texts listed above | R428-2 | c554ae51b1dcc2285863f0f0117cb025971a594c |
| RTL | UNCLEAN (F3) | the page's current-state and design claims against the cited RTL at the head; `KL_media_clock_restart.sv` driven in `mcr_merge_probe/` | R428-2 | c554ae51b1dcc2285863f0f0117cb025971a594c |
| Robustness | UNCLEAN (F1, F2) | the meter's void, bound, pick and step behaviour under seven error shapes (`meter_rules_probe.py`); the switch, holdover and saved-state-at-update paths | R428-2 | c554ae51b1dcc2285863f0f0117cb025971a594c |
| Tests | UNCLEAN (F1, F3) | the simulation and bench tables `:797-845`, each mutant against its pass criterion; the author model | R428-2 | c554ae51b1dcc2285863f0f0117cb025971a594c |
| Docs | UNCLEAN (F1, F2, F3) | the whole of `docs/design/MEDIA_CLOCK_FOLLOWING.md`, the `docs/README.md` row, the docs gates and `check_entity_shape.py` (rc 0), the PR body, the public-text scan | R428-2 | c554ae51b1dcc2285863f0f0117cb025971a594c |

## Executed evidence (this round)

| Run | Result | Receipt |
|---|---|---|
| Author desk model re-run (`meter_rules_model.py` from the evidence branch, standard library) | rc 0; output byte-identical to the published `meter_rules_model.out` | `author_model_rerun.out`, `author_model_rerun.txt` |
| Reviewer meter-rules probe: the page's full rules, including the within-group void and integer modulo-2^32 picks; 7 error shapes x 3 amplitudes x 2 offsets; steps at 16 group positions; the wrap and its mutant (at most 8 workers) | rc 0 | `meter_rules_probe.py`, `receipts_probe.out`, `receipts_probe.rc` |
| Merge-window probe on the unmodified `KL_media_clock_restart.sv`, pinned HDL simulator 5.050 (launcher sha256 `905795b9...e92f`, reports `rev v5.050`) | build rc 0, run rc 0; early requests merge, late requests double-toggle | `mcr_merge_probe/sim_main.cpp`, `mcr_merge_probe/receipt.out`, `mcr_merge_probe/receipt.rc` |
| Docs gates and `check_entity_shape.py` at the head (pinned docs environment) | all 12 rc 0; `checks: 166 failures: 0` | `run_gates.sh`, `gates/*.out`, `gates/*.rc`, `gates/HEAD` |
| Glob-fix mutant: the glob restored in a probe clone, against an unmodified control clone | the mutant adds exactly the page's arm-I failure | `gates/mutant_glob_check_entity_shape.*`, `gates/control_scratchclone_check_entity_shape.*` |
| Hosted check runs at the head, read only (snapshot time in the file) | success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`; `docs-check` in progress; 7 skipped contexts, which are not evidence | `hosted_checks_at_head.txt` |
| Clone integrity after every probe | HEAD and index tree `20c14299`; 979 blobs byte- and mode-identical; status empty, including ignored entries; gitlinks external `efeb541a` (not initialised, as found), gptp-processor `5dce647a`, protocol-processor `b2db3a97`, verilog-axis `48ff7a7e`; submodules clean | `restore_check.txt` |

## Limits

- **Desk review of a design.** The proposed meter does not exist. Both models (the author's and this round's) model the page's rules, not any talker, and the error shapes are assumptions.
- **The lock column assumes perfect local following** (window error = remote ring noise), as the author model does. Servo dynamics were not simulated.
- **The clause texts were read from local copies** of Milan v1.2, IEEE 1722.1-2021 and IEEE 1722-2016.
- **Evidence pointer.** The assignment names evidence tree `0c17547b`, which holds only `review-evidence/629-r1/author/`. The round-2 packets `author-r2/` and `author-r2b/` were read from the evidence branch tip `02b4f38dd3202049b42c4f2f781d70865b61009a`.
- **Not re-run here.** The manager's source, static, builder and native banks, the full suites, and any hosted or local-replica job. Physical calibration was not run, and skipped hosted contexts are not hardware or exhaustive-gate proof.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Complete the hosted `docs-check` at this head, and the hosted and local-replica acceptance.
- Pin the round-2 evidence commit (`02b4f38d` or its successor) in the PR record.
- Obtain the external review's verdict at this head.
- Re-review F1 to F3 at a new head.
- Rule on D1 and D5, and obtain the owner's ruling on D4.
- Build and validate the candidate merge against live dev at the merge turn.
- The baseline PR #630 is still cited through the PR.

R428-2 FINISHED
