[R652] POSITIVE - exact head e11fb36b366587b5e2403c5d47452c16aae6ec31

# R652-1: independent review of PR #191 (issue #184), MSRP Domain re-join encoding

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR / issue | #191 / #184 |
| Exact head | `e11fb36b366587b5e2403c5d47452c16aae6ec31`, tree `cb3672c5ab26692249e8bacae5dfaf6d07c659a2` (verified in the isolated clone, index tree equal) |
| Source base | processor main `08ae00130f096f241463172c4781885934400ee4` |
| Diff reviewed | `git diff 08ae0013..e11fb36b`, 25 files, +676 / -49, one commit |
| Public evidence | kebag-logic/milan-fpga `8551207c21d0a3c127c251327fd3c323a12f6f60`, `review-evidence/pp184-r1/` (author receipts) |
| Reviewer role | internal independent reviewer, cleared context, own clone |

**Verdict: POSITIVE.** The fix does what the issue asks. The Domain re-declaration (periodic and LeaveAll) is now JoinIn only while the Registrar of the declared value is IN, and JoinMt otherwise (IEEE 802.1Q-2018 10.7.6.3 sJ; Milan v1.2 4.2.7.1). A peer's Lv takes that Registrar from IN to MT at once (Milan v1.2 4.2.7.2.2, Δ13). The single New at link rise is unchanged, and so are SR class priority and VID adoption (4.2.7.2.1). The RTL change stays in `KL_srp_domain.sv`, plus the wiring it needs in `KL_srp_top.sv`. All three required scenarios have suite cases, and each case fails under a planted mutant. I reproduced every reviewer-run gate and campaign on this head. The open items are one SUGGESTION and two RESIDUE wording items. None of them makes a lens unclean.

## 1. What I reconstructed (in order)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`, tracked or untracked. I read `README.md` (gates: `run_suites.sh`, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`), `docs/README.md` (single-source rules, citation rules, `make check` before commit) and `.github/workflows/hdl.yml` (docs-gates, suites with the SRP campaign, portability). The repository has no submodules: `git ls-files -s` shows zero `160000` gitlinks.
2. **Frozen acceptance (issue #184 body).**
   - The re-declaration is JoinMt when no Domain registration is IN, and JoinIn when one is.
   - A suite case covers each, each with a planted mutant.
   - The processor suites and the parent consumer gates pass.
3. **Assignment (issue comment 6249574916), read exactly.**
   - (1) Use 10.7.6.3 for periodic and LeaveAll, and keep the single New.
   - (2) The 4.2.7.2.2 instantaneous IN→MT on rLv must hold for the Domain registrar, and both transitions must be tested.
   - (3) Add no-peer, peer-declaring and peer-withdrawal cases, each with a mutant, and update `10_srp_engine.md`.
   - (4) Run every processor gate and the parent consumer gates as in the #185/#186 assignment (comment 6249574548): base and head, the CI-pinned sv2v/Yosys, a scratch parent at milan-fpga dev `e9cbb676`, the `parent-evidence-classification.patch` (#180) and the milan_dp section #67 patch (#176).
   - (5) STOP on any register-map, top-level port or parameter change.
   - No maintainer or manager scope decision narrows or widens this.
4. **Authorities used.**
   - 802.1Q-2018 10.7.6.3, as the issue states it and as `10_srp_engine.md` 6.1 quotes it: IN gives JoinIn, MT or LV gives JoinMt.
   - Table 10-4 Registrar events.
   - Milan v1.2 4.2.7.2.1 (Domain adoption) and 4.2.7.2.2 (Δ13 in F01.4, REQ-SRP-005 in the compliance matrix).
   - Internal interfaces: `KL_srp_decoder` (the LeaveAll lane strobes at the VectorHeader, before that vector's values; `evt_class_a_o = is_domain && SRclassID == 6`), and the `KL_srp_encoder` own-LeaveAll handshake (`la_tx_o` is a subset of `la_prepare_done_o`, so the own sLA always coincides with `join_fsm_w`).
5. **Diff and history.** Single commit `e11fb36` on `08ae0013`. I read every hunk (sections 3 to 7).
6. **Public executable evidence.** I read the author receipts under `author-receipts/` and verified all 6,504 entries of the evidence `MANIFEST.json`: every file is present, and every published sha256 matches. I also read the hosted check runs at the exact head. Per instruction I did not read the author's `HANDOFF.md`.
7. **Prior public findings on PR #191.** I read them only after this pass, and there are none. The PR has no review objects, and its only comments are the two review-start notices (R652-1, R653-1). Nothing to resolve or retain.

## 2. Findings

| ID | Severity | Lenses | Location | Status |
|---|---|---|---|---|
| R652-1-S1 | SUGGESTION | Tests | `tb/srp_encoder/sim_main.cpp:1191-1197` (DR7) | open (non-blocking) |
| R652-1-RS1 | RESIDUE | Docs | `docs/architecture/10_srp_engine.md:296-298`; `hdl/srp/KL_srp_domain.sv:38-42`, `:206` | open, for the residue checklist |
| R652-1-RS2 | RESIDUE | Docs | evidence branch `review-evidence/pp184-r1/author-receipts/RECEIPTS.md` (the `synthdom/` line) | open, for the residue checklist |

### R652-1-S1: the value match is only half pinned (SUGGESTION, Tests)

- **Evidence.** `rx_is_decl_w` (`KL_srp_domain.sv:142-143`) compares the full surfaced `{priority, VID}` pair with the declared value. DR7, the only "another value" Lv case, uses `{6, 4, 9}`, which differs from `{6, 3, 2}` in both fields. I planted two comparator mutants (`receipts/probes/`):
  - match on priority only: srp_encoder 593/593 PASS, srp_top domjoin 4/4 PASS;
  - match on VID only: srp_encoder 593/593 PASS, srp_top domjoin 4/4 PASS.

  The suites do not kill either mutant. The reviewer bench kills both, through P7 (Lv `{6,3,9}`) and P8 (Lv `{6,4,2}`).
- **Impact.** None at this head: the RTL is correct, and my bench passes 17/17. A future edit that dropped one field of the comparison would still pass the suites.
- **Suggested outcome.** Add two DR7 variants to `tb/srp_encoder`: an Lv of `{6, 3, 9}` and an Lv of `{6, 4, 2}`, each leaving the registration IN. Give each a planted mutant in `mutants.py`.
- **Verification.** `scripts/probe_campaign.sh` with `rv-match-prio-only` and `rv-match-vid-only` must report a FAIL in `srp_encoder`.

### R652-1-RS1: a timing sentence states a common-case ordering as absolute (RESIDUE, Docs)

- **Evidence.** The reviewer bench's OBS-a and OBS-b (`receipts/domprobe-head.log`) show two cases where the re-join is JoinMt even though the peer re-declares later in the same MRPDU:
  - a tx! falls between a received Domain-lane LeaveAll and the peer's Domain value in the same MRPDU;
  - a received LeaveAll falls on a tx! clock, so `(leaveall_tick_i && tx_tick_i)` treats it like the own sLA and hands it over at once.

  That result is the sJ outcome for the LV Registrar at that tx!, so 10.7.6.3 conformance holds and no test, figure or verdict changes. Both windows are a few core clocks wide, within a T-MRP-JOIN period. Separately, a received LeaveAll that arrives inside a join round now reaches the next drain, not the current one. That is also conformant, because the re-join waits for a tx!, but it is not "the drain it would have reached anyway".

  The prose, however, states the ordering as unconditional:
  - doc 6.1: "Its re-join waits for the next tx! (the next T-MRP-JOIN round), the drain it would have reached anyway, so a declaration later in the peer's MRPDU registers first."
  - RTL header (lines 38-42) says the same, and the comment at `:206` calls every LeaveAll-plus-tx! clock "the own sLA on its tx!".
- **Exact fix.** In `docs/architecture/10_srp_engine.md:296-298`, replace "Its re-join waits for the next tx! (the next T-MRP-JOIN round), the drain it would have reached anyway, so a declaration later in the peer's MRPDU registers first." with:

  > "Its re-join waits for the next tx! (the next T-MRP-JOIN round), so a declaration later in the peer's MRPDU normally registers first. A received LeaveAll that falls on a tx! clock is handed over at once, as the own one is, and a tx! inside the peer's MRPDU hands the re-join over before the declaration registers. Either re-join is JoinMt, as sJ gives for the LV Registrar at that tx!."

  Optionally, in `KL_srp_domain.sv:206`, change "periodic!, or the own sLA on its tx!" to "periodic!, or a LeaveAll on a tx! clock (the own sLA)".

### R652-1-RS2: the receipt index names a directory that is not published (RESIDUE, Docs)

- **Evidence.** `author-receipts/RECEIPTS.md` lists "`synthdom/`: the Domain synthesis checks". No `synthdom` path exists in the evidence tree or in its `MANIFEST.json`. The figure that directory would back is the PR's "KL_srp_domain alone grows by 3 flip-flops and 1 LUT". I reproduced it independently (`receipts/domain-area.txt`, sv2v + Yosys 0.66 `synth_xilinx -family xc7 -flatten`, module only):
  - FF 113 → 116 (+3);
  - LUT 130 → 131 (+1).

  So no measurement is wrong. Only the index line is.
- **Exact fix.** On the evidence branch, delete the line "- `synthdom/`: the Domain synthesis checks." from `RECEIPTS.md`, or publish the directory it names.

## 3. Lens results

### Conformance (CLEAN)

- **sJ (802.1Q-2018 10.7.6.3).** `KL_srp_domain.sv:257`: `q0_ev_r <= reg_in_r ? EV_JOININ_C : EV_JOINMT_C`. This is used for the periodic, own-LeaveAll and received-LeaveAll re-joins. LV folds into MT, which is allowed because sJ encodes the two alike. The doc gives the reason: nothing else reads the Domain registration, and 802.1Q 35.2.4 gives the Domain no MAP.
- **Registrar (Table 10-4 with Milan 4.2.7.2.2).** `registrar_next`, lines 149-160:
  - rNew, rJoinIn and rJoinMt of the declared value set IN;
  - rLv of that value clears IN at once (Δ13);
  - rLA! and txLA! clear IN (to LV);
  - a received event wins over a LeaveAll in the same clock, as the stream registrars do (10 §6.5);
  - Flush! (LINK_DOWN) and Begin! (LINK_UP) clear IN.

  The top admits only New, JoinIn and JoinMt as registering events (`dom_rx_reg_w`, unchanged), so rIn and rMt never register.
- **Single New at link rise** is unchanged (`:231-238`). Covered by P1 and P16 on the reviewer bench, and by DR11 in the suite.
- **SR class priority and VID (4.2.7.2.1).**
  - The capture and adoption arithmetic, the comparison with the declared value, the Lv-then-New pair, DOMAIN_CHANGE, the class-D levels and the LINK_DOWN-only revert are unchanged from the base (base and head domain SM compared line by line). The only additions are `pend_in_r` and `reg_in_r <= pend_in_nx_w`.
  - Reviewer bench P13 to P16: a differing `{6,5,7}` gives Lv old, New adopted, priority 5, VID 7 and one DOMAIN_CHANGE. It then re-joins JoinIn, re-joins JoinMt after its Lv with the adoption kept, and reverts to the defaults on LINK_DOWN.
  - The existing D1 to D9 and the pp_top notify Domain arms pass (the author's notify campaign: 98/98 at base and head).
- **Range rule (10 §3)** still governs which value is "declared". P9 and P10: the two-class `{5,2,2}` NumberOfValues-2 vector registers, and its Lv withdraws `{6,3,2}`. P11: a class-B-only vector changes nothing.
- **Own LeaveAll.** The LeaveAll MRPDU's own re-join is JoinMt, because txLA! has already taken the Registrar to LV at that tx!. DR4, F1 and P12 cover it, and the doc states it.
- **Requirement traceability.** REQ-SRP-005 gains a DR6 tag (`tb/srp_encoder/sim_main.cpp:1187`). It is emitted at run time (`receipts/reqtag-srp_encoder-DR6.txt`), and the static req-tags gate passes with 227 tags.

### RTL (CLEAN)

- **Synthesizable, single clock, synchronous reset.** All three new flops (`rxla_pend_r`, `reg_in_r`, `pend_in_r`) are reset at `:179-181`. `registrar_next` assigns every output by default, so it infers no latch.
- **Last-assignment precedence in `domain_sm`** is deliberate and correct:
  - capture sets `pend_in_r` after the comb default;
  - LINK_DOWN and LINK_UP override everything;
  - adoption takes `pend_in_nx_w`, so a LeaveAll or Lv in the adoption clock is honoured.
- **Interface.** `KL_srp_domain` gains two inputs (`rxdom_lv_i`, `tx_tick_i`). Its only instantiations are `KL_srp_top` and the `tb/srp_encoder` wrapper; `syn/yosys/run.sh` elaborates it standalone.
  - `KL_srp_top` derives `dom_rx_lv_w` from the decoder's Domain or Class A Lv, and `tx_tick_i` from `join_fsm_w = p_join_fsm_r || la_done_w`.
  - Its ports and parameters are unchanged, and so are those of `protocol_processor_top`.
  - No register map changes, so the STOP condition is not met.
- **Own-sLA coincidence holds by construction:** `la_tx_o` is `la_prepare_done_o && ... && !la_cancel_i` (`KL_srp_encoder.sv:346-348`).
- **Lint.** `scripts/lint_hdl.sh` with the pinned Verilator 5.050 gives rc 0 (`receipts/lint-head.log`). The author's base and head lint receipts are identical.
- **Area.** +3 FF and +1 LUT for the module, reproduced (RS2).

### Robustness (CLEAN)

- **Reset, LINK_DOWN and LINK_UP** clear every new state bit (DR11, P16).
- **Queue backpressure.** The encoding is chosen at hand-over, when the queue is empty. A pending adoption withdrawn before it applies re-joins JoinMt (DR10).
- **Encoding fixed at hand-over.** A received LeaveAll waits for the next tx! (DR3a). A `periodic!` re-join that is already handed over keeps its encoding for at most one T-MRP-JOIN before the drain, which doc 6.1 discloses. The two few-clock races (RS1) yield the sJ result for the Registrar state at that tx!, recover at the next re-join, and are wording-only.
- **Probe mutants that survived.**
  - `rv-top-lv-any-type` and `rv-top-lv-no-class-a` are equivalent mutants: the decoder's `evt_class_a_o` already implies the Domain attribute type and SRclassID 6 (`KL_srp_decoder.sv:542`).
  - `rv-rx-leaveall-keeps-in` (a received LeaveAll does not age the Registrar) is killed by the suite's D8 and by my P5 and P5b.

### Tests (CLEAN; S1 is a suggestion)

- **Required cases, each with a planted mutant that fails it:**
  - no peer gives JoinMt: DR1 and DJ1 (`domain-rejoin-always-joinin`, which is the base encoding);
  - peer declaring gives JoinIn: DR2 and DJ2 (`domain-rejoin-always-joinmt`);
  - peer withdrawal gives JoinMt on the very next re-join: DR6 and DJ4 (`domain-lv-ignored`, `top-domain-lv-unwired`).

  The other new checks each have their own arm: DR3a, DR3, DR4, DR5 and DR7 to DR11, plus DJ3 with `top-domain-tx-every-clock` and `top-domain-tx-unwired`.
- **Reviewer runs at the exact head** (pinned Verilator 5.050, identity in `receipts/verilator-identity.txt`):
  - `tb/srp_encoder`: 593/593 PASS. That is 581 at base plus 12, as the README states.
  - `tb/srp_top` full default run: 8,660/8,660 PASS, 210,707,652 clocks. That is 8,656 at base plus 4. The `domjoin` group alone gives 4/4 PASS.
  - **Full `tb/srp_top/mutants.py --jobs 8`:** 159 checks, 159 PASS, assertion coverage 90/90, rc 0.
    - Every control line and every arm line (rc, failure count, KILLED and its tags) is identical to the author's head receipt (`receipts/campaign-head-srp_top.vs-author.diff` is empty).
    - The author's base and head receipts agree on all 135 pre-existing lines.
    - Every failing set in the `tb/srp_encoder` and `tb/srp_top` README mutation tables matches the campaign tags.
  - Independent `KL_srp_domain` bench (`scripts/domprobe/`), with expected values taken from the clauses rather than the RTL: 17/17 PASS.
- **Gap.** The value comparator is only half pinned (S1).

### Docs (CLEAN; RS1 and RS2 are residue)

- **`docs/architecture/10_srp_engine.md`** is updated: section 5 singleton state, F10.2 with both self-loops annotated, the new 6.1 "Re-join encoding" paragraph and Registrar table, and the 6.5 lane-table Domain row. Each statement matches the RTL and the bench results, apart from the RS1 sentence. The quoted 10.7.6.3 text matches the issue.
- **Suite READMEs.**
  - `tb/srp_encoder` and `tb/srp_top`: counts, DR and DJ definitions, and mutation tables all verified against the runs.
  - `tb/pp_top/README.md:2578-2581`: the moved citations `KL_srp_domain.sv:252` (adoption DOMAIN_CHANGE) and `:219` (revert) point at the right lines.
  - No other line citation into the changed RTL exists.
- **Comment rule (owner, 2026-10-15).** No added source or doc line names a bench lane label, lane name, review round, reviewer ID or issue-comment ID. "Domain lane" in the added lines means the decoder's per-attribute-type LeaveAll lane (`SRP_LA_DOMAIN_C`).
- **`make check` targets at head:** lint, links (1,202), matrix, reqtags (227 tags), modmatrix, params, aecpcmd, ids (607 files), figures and stale all give rc 0. `gen_matrix.py --check` also gives rc 0. These match the author's head log.
  - I did not run `wavedrom-check` locally, because the renderer is not installed here. The delta changes no WaveDrom block (0 matches in the diff), and the hosted docs-gates job, which runs the full `make check`, succeeded at this head.
- **PR text.** The Records-table figures I could check (suite counts, req-tag counts, links +6, ID files +15, campaign 137 → 159 and 86/86 → 90/90, area) all agree with the receipts or with my runs.

## 4. Author receipts and hosted evidence (source-head execution evidence)

- **Processor gates, base and head, all rc 0:**
  - `run_suites.sh`: 1,030,000 → 1,030,016 checks;
  - `check-req-tags.py` executed half: 226 → 227 evidence lines;
  - `lint_hdl.sh`: identical;
  - `make check` and `gen_matrix.py --check`;
  - `syn/yosys/run.sh`;
  - elaboration guards: 93/93.
- **Campaigns, base and head, all rc 0:** srp_top, srp_admission, adp, maap, name_state, elab_mutants, and the pp_top aecp, aecp-dispatch, ctr, notify, gsi, name-write, acmp and d3 campaigns.
- **Parent consumer gates** on a scratch parent at milan-fpga `e9cbb676`, with gitlink `08ae0013` (base) and `e11fb36b` (head) staged. The state files show both parent patches applied: `scripts/measure_test_evidence_readers.py` and `tb/verilator/milan_dp/sim_nxn.cpp`.
  - BDD: 14 features, 406 scenarios at both.
  - milan_dp tallies: byte-identical at base and head.
  - pp_shadow, nvm_cosim, milan_dp_render, test_builder and xvlog: rc 0 at both.
  - OOC `KL_pp_shadow`: 55,878 LUT and 26,284 FF at head.
  - ROM digests recorded for the new pin equal the base pin's (`ucode.hex` `a3b62cab…`, `ltn_rom.hex` `23cc67ee…`).
  - Expected failures: `check_submodule_docs` gives rc 1 identically at both (a moved pin before adoption). `test_evidence` unpatched gives rc 1 at both, and patched gives rc 0 at both.
- **Hosted checks at the exact head** (`receipts/hosted-checks-e11fb36b.txt`): docs-gates and portability completed with success, in both the push and pull_request contexts. The suites job was still in progress at query time. I claim no hosted suites result.
- **No manager source bank runs at this exact head**, and I neither claim nor infer one.

## 5. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_domain.sv` (all), `KL_srp_top.sv:340-395`, decoder LeaveAll and class-A derivation, encoder sLA handshake; 10.7.6.3 / Table 10-4 / Milan 4.2.7.1, 4.2.7.2.1, 4.2.7.2.2 (Δ13, REQ-SRP-005); reviewer bench P1-P16 | R652-1 | e11fb36b366587b5e2403c5d47452c16aae6ec31 |
| RTL | CLEAN | RTL diff, reset and precedence analysis, port and parameter inventory, `lint_hdl.sh` rc 0, module area at base and head | R652-1 | e11fb36b366587b5e2403c5d47452c16aae6ec31 |
| Robustness | CLEAN | link, reset, backpressure and adoption-withdrawal paths; same-clock and race observations OBS-a and OBS-b; five reviewer probe mutants (3 killed by bench or suite, 2 equivalent) | R652-1 | e11fb36b366587b5e2403c5d47452c16aae6ec31 |
| Tests | CLEAN (S1 suggestion) | `tb/srp_encoder` 593/593, `tb/srp_top` 8,660/8,660 and domjoin 4/4, full srp_top campaign 159/159 with coverage 90/90 matching the author's receipt, 15 author patches, reviewer bench 17/17, req-tag emission | R652-1 | e11fb36b366587b5e2403c5d47452c16aae6ec31 |
| Docs | CLEAN (RS1, RS2 residue) | `10_srp_engine.md` diff, three suite READMEs, `pp_top` citations, comment rule over all added lines, `make check` targets except wavedrom-check (hosted success), `gen_matrix`, PR text figures, evidence `RECEIPTS.md` | R652-1 | e11fb36b366587b5e2403c5d47452c16aae6ec31 |

## 6. Real limits

- The IEEE and AVnu PDFs are not available to me. Clause content is taken from the issue's frozen statement, the clause text quoted in `10_srp_engine.md` 6.1, F01.4 Δ13 and the compliance matrix. I did not compare it with the standards themselves.
- **Not run by me, by scope rule; I relied on the author's receipts:**
  - the full `run_suites.sh` bank;
  - every campaign other than srp_top;
  - `syn/yosys/run.sh` and the elaboration guards with the CI-pinned sv2v 0.0.12;
  - all parent consumer gates.

  My area probe used sv2v 0.0.13 and covers the single module only.
- `wavedrom-check` was not run locally (no renderer here). The delta changes no WaveDrom source.
- **Hosted suites job:** in progress at query time, with no result claimed.
- **Parent run marker:** the author's `parent-gates-head.out` marker is empty. The individual `head-par-*` receipts and the state file are present and were read.
- **Hardware:** none used. Physical calibration NOT RUN. No field result counts as hardware proof here.
- **Clone hygiene:**
  - The yosys ABC pass of my area probe wrote an empty untracked `abc.history` into the clone's working directory. I removed it and fixed the probe script to run in its own work directory.
  - Final state (`receipts/clone-integrity.txt`): HEAD and tree as above, index tree equal, `git status --porcelain --ignored` empty, 647 tracked files (630 × 100644, 17 × 100755), worktree-bytes digest equal to a fresh checkout's, no gitlinks.

## 7. Pending manager duties

- Build and validate the current-dev merge candidate (source base `08ae0013` on live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Own hosted and act acceptance, including the hosted suites job at this head (in progress when queried).
- Carry R652-1-RS1 and R652-1-RS2 to the residue checklist with their exact fixes. R652-1-S1 is left to the author's or manager's discretion.
- Merge needs the second independent review (R653-1) and the full completion bar.

## 8. Packet contents

- `scripts/`: portable reviewer scripts.
  - `vl-capped.sh`: Verilator wrapper capping `--build` jobs.
  - `domprobe/`: independent `KL_srp_domain` bench and its runner.
  - `probe_campaign.sh` and `mutations/`: five reviewer probe mutants.
  - `domain_area.sh`: module-only area.
- `receipts/`: raw logs and rc files for every run cited above. Host paths are redacted as `<packet>`, `<review-clone>` and `<home-path>`.
- `MANIFEST.sha256` lists every published file except this report.

R652-1 FINISHED
