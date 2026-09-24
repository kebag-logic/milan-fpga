[R285] NEGATIVE - exact head 446e79b977640d13fa1e5dc0f9896d6c5a70391d

# R285-2: external re-review of PR #549 (Relates to #530), docs-only correction round 1

- Round: R285-2, external, cleared context.
- Head: `446e79b977640d13fa1e5dc0f9896d6c5a70391d`, tree `9f1c9511ca70d889ea2eb2b0a9a3f06d3b29f7fb`.
- Reviewed head of round 1: `c593cbeffaffa647cda70fb1a233455bf9c80d55`. This head adds five one-line commits on it. The commit bodies are empty, so there are no trailers.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06`. The gitlinks are unchanged: protocol processor `09f9bf38`, gPTP `c1b61743`, verilog-axis `48ff7a7e`.
- **Verdict: NEGATIVE, on one open MINOR (F1, lenses RTL and Docs).**
  - The round-1 findings are fixed as filed. Every claim that a shaper budgets or reads the raw verdict is gone. Every page that named the raw verdict as the stream gate now names ACTIVE.
  - The `hdl/` change is comments only. The silicon image built from `c593cbef` stays valid.
  - F1 is in the rewritten opening-edge corner text. Round 1's required outcome (R284-1 F1 and my own R285-1 F1) supplied this wording, and the author followed it. At this head it is wrong on two points:
    - The corner does not arise from "a Listener Ready already registered at the declaration". The processor clears the Listener registration at every declaration.
    - Status skew is not the corner's "whole" or "only" effect when the admission round refuses the stream.
  - This defect was carried in by the reviewers. I record it rather than bank the lens over it.

## Reconstruction (public state only)

1. Contract: AGENTS.md, CONTRIBUTING.md (sections 3 and 6), docs/README.md.
2. Issue #530:
   - The body. Its acceptance is: root cause for items 1 and 2, with a simulation reproduction and a fix; a silicon rerun; item 3 explained or fixed.
   - Every comment, including:
     - the A205 DECISION and BLOCKED;
     - the manager DECISIONs;
     - the A229 assignment and REVIEW READY;
     - the A236 assignment, which scopes a docs-only correction of R284-1 and R285-1 F1/F2 with no RTL change;
     - the SILICON RERUN note: the board runs `c593cbef`, and a physical rerun is pending;
     - A236 REVIEW READY.
3. Authorities, at the pin:
   - `protocol_processor_top.sv:497-506`: ACTIVE is "THE AVTP transmit gate", and the raw verdict lags it by up to three rounds.
   - `KL_srp_top.sv:445,746-748,772-781,849-862`: the optimistic window, and the gate handshake it shares with the talker FSM.
   - `KL_srp_talker_fsm.sv:432-441,635-638,686-710,800-803`: the admission swap, the talker-side Listener registrar, and ACTIVE.
   - `KL_srp_admission.sv:137-214`: the round, its latching and the published verdict.
   - In the parent: `REQUIREMENTS.md` section 5, `milan_datapath.sv` (`:635`, `:1640-1666`, `:1886-1916`, `:2020-2026`, `:2490-2510`, `:3055-3060`, `:3124-3160`, `:5262-5320`, `:6540-6625`), and `KL_talker_diag_ctx.sv:15-37`.
4. The round delta `git diff c593cbef..446e79b9` (six files) and its five commits. I also re-read the whole-PR diff `50e78097..446e79b9` for the pages this delta touches.
5. Public evidence tree `9d1b176c`, `review-evidence/530-r1`. It holds `author/`, `correction-a236/` and the two round-1 review packets.
   - I found no manager bank receipt there, and none in any issue or PR comment.
   - The manager's statement that the source static/builder and native banks passed at this head is recorded as the manager's. This round does not rely on it.

Prior public findings were read only after the independent pass below: the F1 analysis, the probes and the claim search.

## Findings

### F1 - MINOR - lenses: RTL, Docs - the corrected opening-edge corner states a false premise and overstates "status skew" as its only effect

**Where**

| file | lines | text |
|---|---|---|
| `hdl/milan/milan_datapath.sv` | 6585-6592 | "It can do so only when a Listener Ready is registered within those rounds, **which in practice means already registered at the declaration (a re-declaration the bridge's Listener outlived)** ... If the round then refuses it, **ACTIVE falls inside the window** and the declaration swaps to Talker Failed. **That status skew is the corner's whole effect here.**" |
| `CHANGELOG.md` | 41-42 | "That needs a Listener Ready registered at the declaration." / "That status skew is the corner's only effect." |
| `docs/reference/EGRESS_QUEUE_MAP.md` | 79-83 | "with a Listener Ready already registered at a fresh declaration ... In the shipping datapath the only effect is status skew" |
| `docs/reference/REGISTER_MAP.md` | 1112-1116 | "When a Listener Ready is already registered at a fresh declaration ... The only effect is that `LWSRP_STATUS[8]` can lead ..." |
| `docs/traceability/ieee8021q.md` | 58-59 | "The only effect here is that those status words can trail `LWSRP_STATUS[8]`". Row Q-9 (`:89`) adds that a refused stream "loses ACTIVE within the three-round optimistic window". |

**Authority and evidence.** All processor lines are at pin `09f9bf38`. Receipt `receipts/03-corner-evidence.txt` quotes each one.

1. **No Listener registration survives into a declaration.**
   - A declaration is one accept on the shared gate handshake (`KL_srp_top.sv:746-748`, driven into the talker FSM at `:489-492`).
   - On that accept, the top sets `opt_r` and the request (`KL_srp_top.sv:849-858`).
   - The same accept makes the talker FSM clear that source's Listener registrar: `reg_r <= R_MT_C; lstn_val_r <= 2'd0` (`KL_srp_talker_fsm.sv:705-710`, "gate re-open arms a fresh tracker").
   - So `lstn_out_w` reads 0 (`:638`), and ACTIVE, which needs Ready or Ready Failed (`:800-803`), is 0 after every declaration.
   - ACTIVE can rise inside the window only if a registering Listener event for that stream (New, JoinIn or JoinMt, `:686-692`) is decoded inside it. The window lasts at most three rounds of `N_SOURCES_P` cycles each, where `N_SOURCES_P` = `ACMP_SRC_C` (`milan_datapath.sv:7350`). That is 2 on the AX7101 1x1 shape, so the window is a few cycles.
   - The accept itself waits until no decoder event is in flight (`gate_ready_o = !evt_valid_i`, `KL_srp_talker_fsm.sv:432`).
   - "A re-declaration the bridge's Listener outlived" does not produce the corner. "Registered at the declaration" is never true.
   - Corroboration:
     - R284-1's early-Ready probe (Listener Ready before the Talker Advertise) did not trigger the corner.
     - My passive probe of the leg (`receipts/07-crflic-probe-instrumented.log`, instrumentation `receipts/09-probe-instrumentation.diff`) shows both sources' declaration edges with the Listener code 0 at the edge. ACTIVE first rises more than 404,000 cycles after declaration, and `sr_admitted` is already 1 when it does.
     - The leg has no re-declaration under a live Listener, so the reset itself rests on the lines quoted above. See Limits.
2. **"ACTIVE falls inside the window" is not what the RTL does.**
   - ACTIVE takes `sr_adm_fsm = opt_r | adm_admitted` (`KL_srp_top.sv:445`, `KL_srp_talker_fsm.sv:803`).
   - A round that refuses inside the window does not lower it. `opt_r` clears only on the third round strobe (`KL_srp_top.sv:772-781`).
   - So ACTIVE falls when the window closes, and only if the round that closes it refuses.
3. **Status skew is not the only effect in the refusal branch.**
   - When the closing round refuses, the gates have opened and then closed on a declaration that was never admitted.
   - Those gates are the Table 5.4 streaming level `tkd_streaming_w` (`milan_datapath.sv:3055-3060`). Its edges count STREAM_START and STREAM_STOP, and a start resets MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX (`KL_talker_diag_ctx.sv:25-37`).
   - The same gates drive the media-clock-restart streaming input (`:3124`), `CRFT_CTRL[6]/[7]` (`:5318-5319`) and the `0x82C` lobs, and a PDU may start while they are open.
   - A refusal is reachable. It needs the running sum above 75 % of the port rate (`KL_srp_admission.sv:85-88,152-154`), and the port rate is 100 Mb/s whenever `cfg_mac_is_1g` is 0 (`milan_datapath.sv:7492`).
   - In the admitted branch, status skew is indeed the only effect.

**Impact**
- This paragraph is the lane's own correction. A later credit-shaping lane is told to rely on it (`milan_datapath.sv:6602-6605`, `EGRESS_QUEUE_MAP.md:84-85`).
- It gives that lane:
  - a trigger that cannot occur, a registration carried across a declaration;
  - a refusal timing that is off by up to the whole window;
  - no mention of a Table 5.4 START/STOP pair and a possible PDU on a declaration that was never admitted.
- The behaviour itself is the processor's documented optimistic-window contract, and I judge it benign. The finding is about the text only.

**Required outcome.** Change comments and docs only; the RTL does not change. In the five places above:
- Drop or correct the "registered at the declaration / re-declaration outlived" premise. The corner needs a registering Listener event decoded within the window, because every declaration clears the talker-side registrar.
- State that ACTIVE drops when the window closes, and only if the closing round refuses.
- Either state the refusal branch's effect or restrict "only/whole effect is status skew" to the admitted branch. The refusal branch's effect is a licence pulse of at most three rounds on a declaration that was never admitted: one STREAM_START/STREAM_STOP pair, the Table 5.4 interval counters reset, possibly a PDU, and `CRFT_CTRL[6]/[7]` and the lobs pulse.
- If the round-1 required-outcome wording still stands in the PR body and the A236 comment, correct it there too.

**Verification**
- Read the revised text against `KL_srp_talker_fsm.sv:705-710,800-803` and `KL_srp_top.sv:445,772-781`.
- The comment-free `milan_datapath.sv` stays identical to `c593cbef` (`scripts/sv_comment_free_compare.py`).
- `check_em_dash --base 50e78097`, `docs_check` and `gen_toc --check/--verify-anchors` stay green.

### Suggestions (do not affect coverage)

- **S1 (RTL, Docs).** `hdl/milan/milan_datapath.sv:5294-5296`, in the CRF LICENCE comment, still says the CRF emission "rides the same bw-gate the AAF talkers use".
  - The bw-gate is deleted. The shared gate is ACTIVE (`:5281`, `:6606`).
  - This text predates the PR, and the PR edits lines next to it. Optionally reword it with F1.
- **Carried from round 1, not taken by this correction, still optional:**
  - R284-1 S1 / R285-1 S3: the mutant campaign time (139 s against about 168 s), and an absolute `CRFLIC_MDIR` breaking `make crflic`;
  - R284-1 S2: the old-pin arm runs by hand only;
  - R285-1 S1: the t>0 AAF gates are guarded only by the source text;
  - R285-1 S2, third point: the adopted processor PRs are not named in CHANGELOG or SUBMODULES.

### Observation outside scope (not a finding against this PR)

These predate the PR and sit outside this lane. I note them for triage as a possible new Issue:
- `sw/builder/endstation_builder.py:332` says "milan_datapath gates the slope MUX on qidx < NUM_QUEUES". No slope mux has existed since VERSION `0x0056`.
- `sw/builder/test_builder.py:16811-16813` asserts `KL_lwsrp_bw_gate` parameters with the message "the bw-gate must budget the CRF stream's slope too".
- The dated bench warning at `REGISTER_MAP.md:1658` is a historical observation, as the author notes.

## Independent evidence at this head

The simulator is the scoped 5.050 build: wrapper sha256 `905795b9...`, `--version` "5.050 2026-07-01 rev v5.050". Builds used 8 jobs. Probes ran only in a disposable copy under `scratch/`. Local paths in the receipts are redacted to placeholders.

| check | result | receipt |
|---|---|---|
| `hdl/` delta `c593cbef..446e79b9` is comments only | 83 changed lines, 0 not a `//` comment. `milan_datapath.sv` with `//` and `/* */` stripped (string-aware, whitespace-normalised) is identical at both heads (sha256 `327d63f9...`) | `receipts/01-hdl-comment-only-and-scope.txt`, `scripts/sv_comment_free_compare.py` |
| scope of the delta | only `CHANGELOG.md`, four `docs/` pages and `milan_datapath.sv` change. 0 files under `tb/ tests/ scripts/ syn/ sw/`; gitlinks unchanged; one-line commits with empty bodies | same receipt |
| stale gate or shaper claims | no current-tense claim that `sr_admitted` is the stream gate. No claim that a shaper reads the verdict or the sum outside the retained-chain past tense. Remaining hits are historical ("until #530"), status-only, the leg or the mutants, or the out-of-scope builder remnants above | `receipts/02-claim-search.txt` |
| status wiring | `LWSRP_STATUS` packs `[1:0]` listener_decl, `[2]` reg, `[3]` ready, `[4]` declared, `[5]` domain, `[6]` res_active, `[7]` over_limit, `[8]` `lwsrp_stream_gate[0]`, `[9]` `lwsrp_slope_en`, `[10]` tfail_valid, `[11]` ctx_oor (`milan_datapath.sv:2502-2508`, widths at `:1646-1666`). `lwsrp_idle_slope` goes only to `LWSRP_SLOPE` (`:2509`). The raw verdict and the sum have no other reader in `hdl/` or `sw/litex` | read at head |
| F1 authority excerpts | quoted with line numbers | `receipts/03-corner-evidence.txt` |
| docs gates on the head bytes | `check_em_dash --base 50e78097`: 0 findings over 203 added lines, arms 57/57. `docs_check` 0 findings. `gen_toc --check` OK. `--verify-anchors` 150 links. `check_doc_paths` and `check_doc_style` rc 0. `git diff --check` clean | `receipts/04-docs-gates.txt` |
| hosted check runs at exact head (read only, 05:57 UTC) | success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `full-ci-gate`, Verilator shards 0/5 to 3/5, Yosys shards 0/4 to 3/4. Verilator shard 4/5 (`milan_dp`) still in progress. Physical gPTP skipped, which is not execution evidence. Combined status pending; aggregates not yet emitted. PR ready (not draft) | `receipts/05-hosted-check-runs.tsv` |
| `obj_crflic` leg at head, unmodified | 85 checks, 0 failures, RESULT PASS | `receipts/08-crflic-pristine-head.log` |
| passive probe of the same leg | leg still 85/0. Per source: 1 declaration edge, Listener code 0 in the cycle before and at the edge. Every ACTIVE rise happens with `sr_admitted` = 1, the first more than 404,000 cycles after declaration. The corner is not reached | `receipts/07-crflic-probe-instrumented.log`, `receipts/09-probe-instrumentation.diff`, `scripts/instrument_crflic_probe.py` |
| clone integrity after all work | HEAD, tree and index equal to head; 874 tracked files byte- and mode-exact; 0 hide or skip flags; 0 untracked or ignored leftovers; gitlinks `protocol-processor 09f9bf38`, `gptp-processor c1b61743` and `third_party/verilog-axis 48ff7a7e` at their pins and clean (`external` not initialised, as in the clone) | `receipts/06-verify-clone.txt`, `scripts/verify_clone.py` |

## Per-lens results (R285-2, exact head `446e79b9`)

```text
[R285] PASS Conformance - receipts/01-hdl-comment-only-and-scope.txt (comment-free milan_datapath.sv identical to c593cbef; 0 files under tb/ tests/ scripts/ syn/ sw/; gitlinks unchanged), receipts/08-crflic-pristine-head.log (85/0), milan_datapath.sv:1913-1916,2020-2026,5278-5307,6606 against KL_srp_talker_fsm.sv:800-803 and Milan v1.2 5.3.7.3 - the behaviour R285-1 covered at c593cbef is byte-for-byte the behaviour here; the changed pages restate the 5.3.7.3 licence correctly (FR_NFR FR-SRP-01/02/03, ieee8021q Q-9, REGISTER_MAP 0x694[8])
[R285] UNCLEAN RTL - F1 open - milan_datapath.sv:6540-6613 comment block read against KL_srp_top.sv:445,746-748,772-781,849-862, KL_srp_talker_fsm.sv:432,635-638,686-710,800-803, KL_srp_admission.sv:137-214; also checked and correct: the "no shaper reads the slope or the verdict" claim (consumers only at :2502-2509), the CLOSING EDGE paragraph (sr_admitted_o = grant_r & req, KL_srp_admission.sv:206-211; sum_r round-latched), the markers cited at :635 and :6764, the :1995 and :1620-1622 rewordings; logic unchanged (receipt 01)
[R285] PASS Robustness - receipts/01 (no logic, harness or step change since c593cbef), receipts/07 and 08 (leg phases [A]..[E], [INV] at head), KL_srp_top.sv:772-781 and KL_srp_talker_fsm.sv:705-710 - the optimistic-window corner re-derived: narrower than recorded (needs a registering Listener event inside a window of a few cycles) and benign in both branches; escape-hatch terms at milan_datapath.sv:1913-1916,5305-5307 unchanged
[R285] PASS Tests - receipts/01 (sim_crf_licence.cpp, crflic_mutants.py, Makefile, tests/features and tests/steps untouched since c593cbef), receipts/08-crflic-pristine-head.log (85 checks, 0 failures at head) - round-1 coverage (three mutants caught, gate-reverted arm 23/85, old-pin arm 17/85, BDD pin fails on a planted gate) applies unchanged
[R285] UNCLEAN Docs - F1 open (CHANGELOG.md:41-42, EGRESS_QUEUE_MAP.md:79-83, REGISTER_MAP.md:1112-1116, ieee8021q.md:58-59,89) - also checked and correct at head: EGRESS_QUEUE_MAP "Credit-based shaping" scoped to the retained chain in past tense with its new Contents entry; ieee8021q.md :35-36, consequence 2 and Q-9/Q-10 name ACTIVE as the gate and the raw verdict and sum as status; FR_NFR FR-SRP-01/02/03 and FR-CONN-01/02 with the FR-SRP-03 scope note (FR_NFR.md:209); REGISTER_MAP LIVE list, slope-ordering paragraph, 0x680[4:2], 0x694[7]/[8]/[9], 0x698 against milan_datapath.sv:2502-2509; CHANGELOG lines 38-40; receipts/04 docs gates green
```

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:1913-1916,2020-2026,5278-5307,6606`; processor `KL_srp_talker_fsm.sv:800-803`; Milan v1.2 5.3.7.3 and 5.3.7.7 (from round 1); receipts 01 and 08 | R285-1, re-applied R285-2 | `c593cbeffaffa647cda70fb1a233455bf9c80d55`, an ancestor whose Conformance scope is byte-identical at `446e79b977640d13fa1e5dc0f9896d6c5a70391d` (receipt 01) |
| RTL | UNCLEAN (F1) | `milan_datapath.sv:635,1640-1666,1886-1916,2020-2026,2490-2510,3055-3060,3124,5262-5320,6540-6625,7350,7492`; processor `KL_srp_top.sv:415-445,742-862`, `KL_srp_talker_fsm.sv:430-560,635-710,792-807`, `KL_srp_admission.sv:1-217`, `protocol_processor_top.sv:485-510`; receipts 01, 03, 07 | R285-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| Robustness | CLEAN | `sim_crf_licence.cpp` phases `[A]`..`[E]`, `[INV]`; escape hatches `milan_datapath.sv:1913-1916,5305-5307`; the optimistic window re-derived from the processor sources; receipts 07 and 08 | R285-1, re-applied R285-2 | `c593cbeffaffa647cda70fb1a233455bf9c80d55`, an ancestor with no logic or harness change since (receipt 01) |
| Tests | CLEAN | `sim_crf_licence.cpp`, `crflic_mutants.py`, `Makefile`, the BDD feature and steps (untouched since `c593cbef`); receipt 08 at head | R285-1, re-applied R285-2 | `c593cbeffaffa647cda70fb1a233455bf9c80d55`, an ancestor whose Tests scope is untouched at `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| Docs | UNCLEAN (F1) | `CHANGELOG.md`, `EGRESS_QUEUE_MAP.md`, `FR_NFR.md`, `REGISTER_MAP.md`, `ieee8021q.md`, the in-RTL comments of `milan_datapath.sv`, `REQUIREMENTS.md` section 5; receipts 02 and 04 | R285-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |

For RTL and Docs to become clean, a comments-and-docs-only fix of F1 must be re-reviewed under those two lenses at its head. Conformance, Robustness and Tests stay banked at `c593cbef` only while the logic, the leg, the mutants, the Makefile and the BDD step stay untouched.

## Prior public findings on this PR, resolved or retained at this head

These were read after the verdict analysis above.

| item | disposition at `446e79b9` | basis |
|---|---|---|
| R284-1 F1 / R285-1 F1, MINOR (RTL, Docs): text said a shaper budgets or keeps the raw verdict | **RESOLVED as filed.** No text claims a shaper consumes the raw verdict or the sum in the shipping datapath. The real consumers (`LWSRP_STATUS[9]`, `0x698`) are named, and the bw-gate invariant is scoped to the retained, uninstantiated chain. The corner wording this item's required outcome prescribed is superseded by **R285-2 F1** above | `milan_datapath.sv:6549-6565,6607-6613`; `CHANGELOG.md:38-39`; receipt 02 |
| R284-1 F2 / R285-1 F2, MINOR (Docs): Q-9 and EGRESS_QUEUE_MAP named or implied the raw verdict as the gate | **RESOLVED.** Q-9 names `srp_active_o`; `sr_admitted_o` appears as "the gate until #530". EGRESS_QUEUE_MAP "Credit-based shaping" is past tense for the retained chain and gives the ACTIVE caveat. FR_NFR and REGISTER_MAP carry the same correction. The caveat's wording shares F1 | `ieee8021q.md:89`; `EGRESS_QUEUE_MAP.md:64-85`; `FR_NFR.md:144,147`; receipt 02 |
| R285-1 S2 (Docs): `milan_datapath.sv:1994` "bandwidth gate"; `ieee8021q.md:35` "idleSlope" | **RESOLVED**: now "the processor's per-stream ACTIVE (#530)" and "read back as `LWSRP_SLOPE` status with no shaper to program". The pin-scope naming part was not taken and remains optional | `milan_datapath.sv:1995`; `ieee8021q.md:35-36` |
| R284-1 S1, R284-1 S2, R285-1 S1, R285-1 S3 | not taken; they remain SUGGESTIONS in the Tests and Docs scopes, with no coverage effect | unchanged files (receipt 01) |
| R284-1 observation (t>0 gates without the engine-off escape) | not a finding against this PR; unchanged and documented at `milan_datapath.sv:1995-2010` | read at head |

## Limits

- Physical calibration and silicon: NOT RUN. Simulation passes are not hardware proof. The #530 silicon rerun (board on `c593cbef`) is the manager's and is pending.
- F1 point 1 rests on the processor RTL lines quoted in receipt 03. My probe confirms that declaration edges carry Listener code 0 in the leg. The leg has no re-declaration under a live Listener, and I built no bench that drives one. F1 point 3's refusal branch is derived from RTL. It is not exercised by any bench this round ran.
- Not run, per scope: the full parent, processor, gPTP, Yosys and builder banks; the other `milan_dp` legs; `pp_shadow`; the mutant campaign; the failing arms (unchanged since round 1); lint and `xvlog`; act or Docker.
- I found no manager bank receipt in the public evidence tree or in the comments. The manager's bank result is the manager's statement.
- Hosted Verilator shard 4/5 and the `verilator-suites` and `yosys-portability` aggregates were not complete when I read them.
- Specification text was not re-read this round. The Milan and 802.1Q readings are those of round 1.

## Pending manager duties

- Route F1 to a docs-only correction, then have RTL and Docs re-reviewed at the new head.
- Hosted: exact-head `verilator-suites` (shard 4/5 carries the new leg), `yosys-portability`, and act acceptance.
- Candidate merge validation against live dev `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f` (source base `50e78097`), post-merge containment.
- The #530 silicon rerun, which is the issue's closing acceptance.
- Optional: triage the out-of-scope builder remnants as a new Issue.

Publishable receipts and scripts are listed in `MANIFEST.sha256`. The disposable probe tree lives only under `scratch/`.

R285-2 FINISHED
