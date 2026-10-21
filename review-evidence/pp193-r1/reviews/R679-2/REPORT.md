[R679] NEGATIVE - exact head 7b424cdfe111a426f00517ff471246b4b9650726

# R679-2: independent round-2 review of processor PR #198 (Closes #193)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #198, round R679-2.
- Exact head `7b424cdfe111a426f00517ff471246b4b9650726`, tree `4142dcfe858d04687f3f37847a67f7c69d6ae0ea`.
- Previously reviewed head `6ddfcda4` (R679-1, R680-1). Round-2 delta: five author commits `e38c535`, `acd65be`, `c7c8825`, `57fb7dd`, `7b424cd`. Source base `21601694`.

Round 2 closes both reviews' MAJOR finding. A parked Listener applicant is now in the group of the StreamID it holds, and a sink that declares that StreamID takes it over (LA + New! = VN). One value goes out per tick, with no Lv beside the declaration, and the peer registrar stays IN. This holds in every variant of both prior reviews' probes, in the new SH10-SH16 and SW4-SW7 checks, and under all five new controls, each KILLED as claimed. The area figures reproduce exactly from the receipts. The PR body states the 8x8 shape, and the citation and label fixes are applied.

The verdict is NEGATIVE for one reason. Item 4 of the assignment (R679-1-S2) required a probe of a handover to a slot the walk has already passed, and a fix with a case and a control if it misbehaves. The author's probe found no misbehaviour, but it covered only a holder in AN during a plain tx! walk. In an own-LeaveAll (txLA!) walk, a QA applicant handed to an already-walked slot loses its post-LeaveAll re-declaration. Nothing goes out for the stream until the next periodic!, where the one-applicant model sends JoinMt in the LeaveAll frame. This is F1 (MINOR). A second MINOR (F2) is a reachable round-2 guard that no check exercises. One RESIDUE and three SUGGESTIONS complete the report.

## Reconstruction (order followed)

1. **Repository rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md` (conventions, single-source rules, `make check`).
2. **Issue #193.**
   - The frozen body ("Done when").
   - The assignment (issuecomment-6289596705), the STOP (6289991979), the STOP ruling (6290012163), the round-1b REVIEW READY (6299186889) and the manager's answers (6299223806).
   - The round-2 REVIEW READY (6310615005).
3. **PR #198.**
   - The body at this head.
   - The round-2 assignment (issuecomment-6300041102) and the manager's area ruling (issuecomment-6310654578), read exactly.
4. **Authorities.**
   - The design banner and full head text of `hdl/srp/KL_srp_listener_fsm.sv`, including the Table 10-3 functions.
   - `docs/architecture/10_srp_engine.md` §5.1 and §6.4.
   - The two test READMEs.
   - The IEEE/Milan texts are not in the repository. Clause numbers are checked against the frozen ruling and the repository's own usage.
5. **Diff and history.**
   - `git diff 21601694..7b424cdf`, with the round-2 delta `6ddfcda..7b424cdf` read hunk by hunk.
   - `57fb7dd..7b424cd` changes only `tb/srp_top/README.md` (3 lines).
6. **Public executable evidence.** `kebag-logic/milan-fpga@cbc4bd9f:review-evidence/pp193-r1/author-r2/`, read by section:
   - the HANDOFF (Round 2, R2.1-R2.8);
   - the round-2 receipts: campaigns, gates, consumers, ooc, area-listener, probes and scripts;
   - the R679-1 and R680-1 probe scripts.

The prior public findings (R679-1 issuecomment-6300027310, R680-1 issuecomment-6299632354) were read only after my own pass over the delta, the probes and the controls. Their resolution is below.

## Findings

### R679-2-F1 — MINOR — Conformance, RTL, Robustness, Tests, Docs: a handover into a slot the txLA! walk has passed loses the applicant's LeaveAll re-declaration (R679-1-S2 misbehaves)

**Where.**
- `hdl/srp/KL_srp_listener_fsm.sv:1054`: the taker gets `wdone_r <= (walk_r != W_IDLE) && wdone_r[src]`.
- `:700-704`: a taker slot that the walk has already passed is never walked again in that walk.
- `wtxla_r` is per walk, so the applicant's next transmit opportunity is a plain tx!.

**Claim text.**
- Banner `:111-112`: "one to a slot the walk has passed waits for the next tx!".
- `docs/architecture/10_srp_engine.md:644-645`: "its message goes at the next tx!, one T-MRP-JOIN later".
- PR body, Behaviour: "its message goes one T-MRP-JOIN later". Round 2, S2: "it is never lost and never sent twice".
- Author HANDOFF R2.2 item 4: "no misbehaviour, so no change".

**Reproduction.** Ordinary inputs only, through `probes/s2_probe.py`:
1. Sink 0 (VLAN 3) and sink 5 or 7 (VLAN 0) are settled on one StreamID.
2. The higher sink declares alone and is ticked to QA.
3. An own LeaveAll marks the next walk txLA!.
4. Clock 1, 2 or 3 into that walk, after the walk has passed sink 0 and before it reaches the holder, sink 0's talker registers. Sink 0 becomes the owner and takes the QA applicant (no sum change, so no New!).

**Evidence** (`receipts/s2_probe_head.log`):

| Walk | Handover | RTL sends | One-applicant model |
|---|---|---|---|
| txLA! | into a passed slot (6 cases) | `''` in the LeaveAll walk and `'' '' ''` in the next three ticks | `'3/2'`, JoinMt Ready, in the LeaveAll walk |
| txLA! | before the walk (control) | `'3/2'` | `'3/2'` |
| txLA! | none (control) | `'3/2'` | `'3/2'` |
| plain tx! | into a passed slot (all cases) | matches the model | as the author recorded: the QA case owes no message, and an AN/VN case is one tick late |

- Only the periodic! that follows (QA → AA) brings the JoinMt back.
- Base `6ddfcda4` gives the same words (`receipts/s2_probe_base.log`). The cause is the round-1 handover; round 2 did not change it.
- The author's S2 probe (HANDOFF R2.2 (a)) used a holder in AN. AN sends New on tx! and on txLA! alike, so it cannot show this.

**Authority.**
- IEEE 802.1Q-2018 Table 10-3: QA on txLA! is sJ, and QA on tx! sends nothing.
- 10.7.7: one Applicant per attribute value. A handed-over applicant must see the transmit opportunity the single applicant would have seen.
- 35.1.2.2: the stream is still wanted.
- The ruling (issuecomment-6290012163, item 2): "the declaration continues uninterrupted".
- The round-2 assignment, item 4: "If it misbehaves, fix it in this round with a case and a control."

**Impact.**
- The peer's registrar for the Listener value goes to LV on the DUT's own LeaveAll, and receives no re-join until the next periodic! and its tick.
- A peer whose LeaveTime expires first deregisters the stream while sinks still want it. That is the symptom class of #193.
- Likelihood is low. It needs a lower-index sink's first registration on a shared StreamID inside the few clocks of a txLA! walk. Control-plane handovers (A8 or A15 of the owner) go to a higher index and are not affected.
- The documentation and the PR describe the case as a one-tick delay.

**Severity.** MINOR. The window is narrow and periodic! recovers. It is still an open item of the round-2 assignment and a false behaviour claim.

**Required outcome.**
- A handed-over applicant gets exactly one transmit opportunity of the kind the walk carries (tx! or txLA!), whatever the taker's index. For example, a handover into a passed slot carries an owed txLA!, or the walk serves the taker at the giver's slot.
- Add a committed SH case: a txLA! walk, a handover into a passed slot, and the JoinMt expected in that LeaveAll walk or the next. Plant a named control that is KILLED.
- Correct the banner, §6.4 and the PR text.

**Verification.**
- `probes/s2_probe.py` (via `probes/run_reviewer_probes.sh`) gives MATCH in every row.
- The plain-tx! rows stay MATCH and both controls stay MATCH.
- SH1-SH16, SW1-SW7 and the srp_top campaign keep passing.

### R679-2-F2 — MINOR — Tests: the round-2 "a sink parked again keeps its own" guard has no check that fails without it

**Where.** `hdl/srp/KL_srp_listener_fsm.sv:944` and `:949`: `lv_take_w && !lvp_r[a]`.

**Evidence.**
- A disposable control, `probes/rv-repark-overwrites-pairs.patch`, drops `&& !lvp_r[a]`. It survives the whole stream-FSM suite (1,410 PASS) and srp_top `share` (9 PASS) (`receipts/campaign-reviewer-arms.out`).
- The guard does protect a reachable path. `probes/repark_probe.py` covers it with ordinary inputs:
  1. Sink 1 declares SIDP.
  2. Sink 0, alone on SID0 in QA, re-binds to SIDP, which parks SID0's Lv.
  3. Before any tx!, sink 0 re-binds again, to SIDQ.
- At the head the next tx! sends SID0 `'5/2'` (Lv) and nothing for SIDP, as the model expects (`receipts/repark_probe_head.log`, MATCH).
- Under the control, SID0's owed Lv is lost (`''`) and SIDP gets a spurious New (`'0/2'`) (`receipts/repark_probe_mut.log`, DIFF). Meanwhile all 1,410 suite checks still pass.
- The author's parked-pairs probe covers a re-park with a joiner on the parked value, which goes through `hand_w`. It does not cover this path.

**Authority.**
- The #188 obligation (the owed Lv) that the round-2 assignment requires unchanged when no sink declares the old value.
- IEEE 802.1Q-2018 10.7.7.
- The lane's own bar: each new behaviour carries a check with a planted KILLED control.

**Impact.** A later edit can silently drop a parked Lv and re-declare an unrelated stream.

**Required outcome.** A committed SH case for "parked, then re-bound again while another sink declares the interim stream", with a named control (this edit) that is KILLED.

**Verification.** Run the campaign with the new arm: KILLED on the new check.

### R679-2-R1 — RESIDUE — Docs: one srp_top README control row names fewer failing checks than fail

**Where.** `tb/srp_top/README.md:860`, the row for `listener-teardown-keeps-declaring`.

**Evidence.**
- The count (62) is right.
- The named list "SH3, SH10-SH16 and the Table 10-3 walks…" omits SH2, SH4-SH9, RB1, RB4 and RB7, which also fail. See the author's `campaigns/head/srp_top.log:187` and my `receipts/campaign-commit5-arms.out`.
- The base row had the same omission. Commit 5 extended it.

**Exact fix.** Replace "SH3, SH10-SH16 and the Table 10-3 walks that reach LA through an A8 (62)" with "SH2-SH16, RB1, RB4, RB7 and the Table 10-3 walks that reach LA through an A8 (62)".

### R679-2-S1 — SUGGESTION — Tests: the both-parked exclusion in `same_w` has no killing check

`probes/rv-both-parked-grouped.patch` drops `|| (lvp_r[s] && lvp_r[t])` at `KL_srp_listener_fsm.sv:599`. It survives the stream-FSM suite and srp_top `share`.

Without the exclusion the relation becomes asymmetric in SH16's state. The higher-index parked holder would see the lower one as a member and could go quiet while that one is still parked. SH16 hides this, because the lower sink's own Lv retires first in the same walk.

A case where the lower sink's park outlives the walk (for example, LO kept through txLA!) would pin it.

### R679-2-S2 — SUGGESTION — RTL (area): at two sinks `g_lcp_flops` duplicates `lsid_r`

The comment at `:821-825` says so. At N = 2, `lcp_w` could alias `g_wsid_flops.lsid_r` and save 128 flip-flops. The listener-alone receipts show 803 → 933 FF at two sinks.

### R679-2-S3 — SUGGESTION — Docs: state the measured listener-alone one-sink delta beside "no 1x1 figure"

The author's `area-listener/SUMMARY.txt` measured the listener alone at one sink: 2,729 → 2,798 LUT (+69), FF unchanged. The PR body's "No 1x1 figure was measured here" is true of `KL_pp_shadow`. Adding the listener-alone one-sink figure, labelled as such, would help the route-1x1 reader.

## Prior public findings on this PR, at this head

| Finding | Resolution at 7b424cdf | Evidence |
|---|---|---|
| R679-1-F1 / R680-1-F1, MAJOR: parked and live applicants for one value | **Resolved** | See the breakdown below this table. |
| R679-1-F2 / R680-1-F2, MINOR: area without its shape | **Resolved** | The PR body states "the module defaults (8 Stream Inputs and 8 Stream Outputs)" beside the figure, that no 1x1 figure was measured here, and that the 4th pin adoption's route-1x1 measures the shipped cost. The figures reproduce from the published OOC receipts: main 56,743 LUT / 26,331 FF, base 57,266 / 26,381, head 58,078 / 26,949. That is +1,335 / +618 against main and +812 / +568 for round 2. LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10 and CARRY4 2,392 are unchanged. The listener alone at 8 sinks is 9,428 → 9,750 (+322), against 11,679 at `c7c8825` (+2,251). The shifter fix of commit 4 is confirmed. |
| R680-1-F4, MINOR (and R679-1-S1): §35.2.2.8.7 cited for the type sum | **Resolved** | `tb/srp_stream_fsms/sim_main.cpp:1794` and `tb/srp_top/sim_main.cpp:3172` cite "§35.1.2.2; §35.2.4.4.3, Table 35-14", with §35.2.6 kept for the change in place. |
| R680-1-F3, RESIDUE: labels in new source comments | **Applied as written** | `tb/srp_top/sim_main.cpp:3000` is the given heading, and the `SW3: ` prefix is gone. |
| R679-1-S2, SUGGESTION: handover to a lower index after the walk passed it | **Not resolved: misbehaves in the txLA! form** | The plain tx! form behaves as recorded, but the txLA! form loses the LeaveAll re-declaration; see R679-2-F1. |

How R679-1-F1 / R680-1-F1 is resolved:
- **R679-1's `run_probes.sh`** (with the same one-line anchor adaptation the author made; identical bytes) on 7b424cdf, every variant:
  - no `FAIL: PR`/`FAIL: PW`;
  - one value per tick (`'0/2'`, `'0/2'`, `'3/2'`);
  - the wire frames carry the value once (35 B), with no Lv;
  - peer before 1, after 1, deregs 0, Lv 0;
  - 1,414 and 11 PASS (`receipts/prior-r679-1-*.log`).
- **R680-1's two probes** (revision guard set to the head): 2/2 PASS each, count 1, leaves 0, peer IN (`receipts/prior-r680-1-*.log`).
- **SH10-SH16 and SW4-SW7** pass (1,410 and 8,669 PASS).
- **The five new controls** are KILLED with the claimed tags, and `listener-settle-compare-dropped` (re-anchored, edit unchanged) is still KILLED (`receipts/campaign-round2-arms.out`).
- **The #188 obligations with no declarer:** SH14 and the RB checks pass.
- **The banner** (`:103-112`) and **10 §6.4** ("A parked Leave") describe the parked case.

## The assignment's checks

| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | A parked applicant joins the group of the StreamID another sink settles on or declares (LA + New! = VN); no stale Lv; #188 unchanged with no declarer | Holds | See R679-1-F1 above. RTL: `mbr_w = rec_valid_r` and `same_w` read `lq_r` while parked (`:587-608`); the takeover clears the giver's park (`:1037-1038`); the retirement marks the group's walk (`:989-996`). |
| 1 | SH/SW cases for both index orders and both re-bind forms, byte-exact frames and an uninterrupted peer registrar, each with a named KILLED control | Holds | SH10-SH13 and SW4-SW7 (orders 1/0 and 0/1, with A15 at once or A8 then A15). SW compares the whole frame (`f == exp`) and counts values over the next three frames. The peer model counts deregistrations and Lv. Controls: `listener-parked-outside-groups` (SH10-SH16; SW4-SW7), `listener-settle-skips-leave-copies` (SH10-SH15; SW4-SW7), `listener-merge-keeps-park` (SH10-SH13), `listener-retire-skips-group-mark` (SH15), `listener-park-drops-matcher-pairs` (SH16): all KILLED in my run. |
| 1 | The reviewers' probes, every variant: no FAIL PR/PW, one value per tick, no Lv while the joiner declares, peer IN with 0 deregistrations | Holds | See R679-1-F1 above. |
| 1 | Banner and 10 §6.4 describe the parked case | Holds | Banner `:103-112`; `10_srp_engine.md` §6.4 "A parked Leave" and the §5.1 rows. |
| 2 | PR body shape and area | Holds | See R679-1-F2 above. |
| 3 | F4 citations and F3 residue | Holds | See above. |
| 4 | S2 probe recorded, or a fix with a case and a control | **Not met** | R679-2-F1 |
| 5 | Every cited record from the clean runner restart (HANDOFF R2.6) | Consistent; no counter-evidence | See the notes below this table. |
| 6 | Consumer gates at dev 78ca9bdf with four adoption patches pass at this head; no port, parameter or register-map change | Author receipts consistent; scope verified | See the notes below this table. |

Notes on check 5 (the clean runner restart):
- The published head campaign record is complete and internally consistent. `campaigns/head/srp_top.{log,rc,sec}`: rc 0, 203/203, coverage 124/124, 18 controls PASS, 0 UNPROVEN, 3,456 s. A duplicate that was stopped within a minute cannot have produced it.
- `RUNNER.txt` names the head runners (`head-camps`, `head-camps2`).
- No published receipt refers to the set-aside `void-*` records.
- The `c7c8825f` rows in `area-listener/SUMMARY.txt` are the shifter diagnosis, not head records.
- Gate and consumer records are at 57fb7dd2, plus a final consumer run at 7b424cdf. Their `STATE.txt` files carry gitlinks 57fb7dd2 and 7b424cdf.
- My own re-runs of nine srp_top arms reproduce the head record's failing tags exactly.
- Limit: run times are not independently timestamped.

Notes on check 6 (consumer gates and scope):
- `consumers/{base,head,final}`: every gate rc 0 except `check_submodule_docs` rc 1, identical at base and head.
- `milan_dp` and the other head records are rc 0. `final` (gitlink 7b424cdf) runs the static gates: all rc 0 but `submodule_docs`.
- The parent base dev 78ca9bdf and the fourth patch (`parent-evidence-classification`) are stated by the author. Three of the four apply commits are visible in `STATE.txt`.
- Scope: the module headers of `KL_srp_listener_fsm`, `KL_srp_top` and `protocol_processor_top` are byte-identical at 21601694, 6ddfcda and the head (`receipts/scope-headers.txt`). Under `hdl/` the round 2 delta touches only the listener. Docs 02 and 07 are unchanged.

### Other round-2 RTL checks (reviewer's own)

- **Leave-copy compare write.** `g_lcp_flops` writes `lcp_r[s]` under the same enable as the leave copy, one enable per sink, and is unreset. It is read only through `lq_r`, and only while `lvp_r`. A park writes the row in the same clock that it writes `lcp_r`, so no unwritten value is ever read.
- **Disposable controls.** Each of these is KILLED:
  - `rv-leave-compare-copy-unwritten`: SH10-SH15, SW4-SW7;
  - `rv-parked-uses-matcher-pairs`: SH10-SH16, SW4-SW7;
  - `rv-take-forgets-walk-mark`: SH7.
- **The two-parked invariant** ("two parked applicants never hold one value") holds on every path I traced. A takeover or `hand_w` always clears the first park before a second could form. Its exclusion is untested (S1).
- **Comment rule.** The added source lines contain no lane label, lane name, review round, reviewer ID or issue-comment ID. The new test comment cites `RB`/`RB5`, which are suite check IDs (behaviour IDs under parent #746), so this is not residue.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Table 10-3 rows for LA/LO + New!, QA on tx!/txLA!; 10.7.7, the 35.2.6 NOTE, 35.1.2.2, Table 35-14, Milan 4.2.7.2.2 as cited by the ruling; wire frames from SW4-SW7 and the prior probes; S2 probe in both walk kinds at head and base | R679-2 | 7b424cdfe111a426f00517ff471246b4b9650726 |
| RTL | UNCLEAN (F1) | round-2 delta of `KL_srp_listener_fsm.sv` hunk by hunk (owner_map `same_w`/`lq_r`, settle pair writes, `g_lcp_flops`, walk retirement mark, takeover park clear) in the context of the full head file; module headers; lint rc 0 | R679-2 | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Robustness | UNCLEAN (F1) | prior probes (four FSM variants, two wire variants, two R680-1 probes); S2 handover at walk clocks 1-3 for two holder indices, tx! and txLA!, with controls; re-park while another sink declares the interim stream; five disposable mutants | R679-2 | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Tests | UNCLEAN (F1, F2) | stream-FSM suite 1,410 PASS and srp_top 8,669 PASS at head (1,403 and 8,665 at base); the six round-2 controls and three commit-5 re-counted controls re-run with tags; five reviewer controls (three KILLED, two surviving: F2, S1); SH10-SH16 and SW4-SW7 source read | R679-2 | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Docs | UNCLEAN (F1 claim text) | banner, `10_srp_engine.md` §5.1/§6.4, both test READMEs (counts verified; R1), PR body (shape, figures, S2 text), author HANDOFF Round 2 and its receipts; `make check` and `gen_matrix --check` rc 0 | R679-2 | 7b424cdfe111a426f00517ff471246b4b9650726 |

## Receipts

Every run below used an archived copy or a scratch clone under `scratch/` (never the review clone), with the pinned simulator 5.050 (it reports `rev v5.050`, the CI pin). At most 16 jobs ran at once. Host paths are replaced by `<PACKET>`, `<CLONE>`, `<REVIEWS>`, `<TOOLS>`, `<HOME>` and `<TMP>`.

| Receipt | What | rc |
|---|---|---|
| `receipts/suite-srp_stream_fsms-{head,base}.log` | `make` in tb/srp_stream_fsms at head and at 6ddfcda | 0, 1410 PASS / 0, 1403 PASS |
| `receipts/suite-srp_top-{head,base}.log` | `make` in tb/srp_top | 0, 8669 PASS / 0, 8665 PASS |
| `receipts/campaign-round2-arms.out`, `campaign-round2-arms/` | head `tb/srp_top/mutants.py --only` with the six round-2 controls (and the reviewer arms), `--jobs 16` | 124: the run hit the 585 s limit inside a full-srp_top reviewer arm. All six round-2 control lines printed before that, each KILLED. |
| `receipts/campaign-reviewer-arms.out`, `campaign-reviewer-arms/` | five reviewer arms on the stream suite and srp_top `share` | 1 (expected: two arms survive, F2 and S1) |
| `receipts/campaign-commit5-arms.out`, `campaign-commit5-arms/` | `listener-rider-not-quiet`, `-withdraw-ignores-riders`, `-teardown-keeps-declaring` | 0, 7/7 |
| `receipts/s2_probe_{head,base}.log` | `probes/s2_probe.py` | 0 (probe lines show DIFF in the txLA! rows) |
| `receipts/repark_probe_{head,mut}.log` | `probes/repark_probe.py` at head, and with `rv-repark-overwrites-pairs` | 0 / 0 (MATCH / DIFF) |
| `receipts/prior-r679-1-{fsm,wire}.log`, `prior-r679-1-run_probes.out` | R679-1 `run_probes.sh` at 7b424cdf (`probes/prior-r679-1/`, anchor adapted) | 0, 0 |
| `receipts/prior-r680-1-parked{,-wire}-probe.log` | R680-1 probes, guard set to 7b424cdf (`probes/prior-r680-1/`) | 0, 0 |
| `receipts/gate-{lint_hdl,gen_matrix,make_check}.log` | `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` at head | 0, 0, 0 |
| `receipts/scope-headers.txt` | module-header digests at 21601694, 6ddfcda and head; `hdl/` diff stat | n/a |
| `receipts/hosted-checks.txt` | exact-head check runs at 08:14Z | n/a |
| `receipts/source-integrity.txt` | `probes/verify_clone.sh` on the review clone | 0 |

`probes/run_reviewer_probes.sh <clone> <revision> <outdir>` re-runs the S2 probe, the re-park probe (plain and mutated) and the controls campaign on any candidate.

## Limits and pending manager duties

- **Not run.**
  - No full processor, parent, gPTP, Yosys or builder bank.
  - No `run_suites.sh`, no pp_top campaigns and no parent consumer gates.
  - No OOC synthesis and no full srp_top campaign: only nine of its control labels (the six round-2 controls and three commit-5 re-counts), plus the five reviewer arms.
  - For all of these I rely on the author's published round-2 receipts, with their recorded revisions (57fb7dd2 for the records, 7b424cdf for the README-reading gates and the final static consumer gates).
  - No manager source bank exists at this exact head, and none is claimed or inferred.
- **Contexts.** Source base `21601694`, review base `6ddfcda4`, and the live dev `d77a8afdbc960d70d1ceeee9af1163624f102b16` of the final candidate are distinct contexts.
- **Hosted CI at 08:14Z.**
  - Executed: `docs-gates` and `portability` succeeded in both workflow runs.
  - `suites`: still in progress in both runs, so not counted.
  - The manager owns hosted/act acceptance.
- **Physical calibration NOT RUN.** No hardware; field skips are not hardware proof.
- **Standards.** The IEEE 802.1Q-2018 and Milan v1.2 texts were not re-read. Table 10-3 behaviour is taken from the repository's transcription (`app_next_f`, `app_msg_f`) and the suite's independent model.
- **Manager duties.**
  - Obtain fixes for F1 and F2, then an independent re-review.
  - Carry R1 to the residue checklist.
  - Validate the current-dev merge candidate with the builder and native banks at the merge turn, and link those receipts on the PR.
  - Check the shipped cost with the route-1x1 measurement at the 4th pin adoption, per the area ruling.
- **Clone integrity.** The review clone was never modified. Verified:
  - HEAD `7b424cdf…`, tree `4142dcfe…`;
  - status clean, ignored files included;
  - index equal to HEAD;
  - the bytes and modes of all 697 tracked entries;
  - zero gitlinks, so there are no submodule pins to restore.

R679-2 FINISHED
