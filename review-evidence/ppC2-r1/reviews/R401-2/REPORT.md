[R401] POSITIVE - exact head 053f979b9cfc84871ff2e107d43d20bf0e950db4

# R401-2: independent external delta review of processor PR #135 (lane C2, MAAP; issues #66, #67, #68)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `053f979b9cfc84871ff2e107d43d20bf0e950db4`, tree `33087148b197340778ee033f3f2210ac0f629059`
- Base: `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. Round-1 head: `b03d36f2`. This round adds nine commits: `4de2c60`, `8ae76ee`, `fa21c58`, `2c11d6f`, `8382cf6`, `ea79d8b`, `d0acc9b`, `4f6affc`, `053f979`.
- Round: R401-2. The review ran in a cleared context, in an isolated detached clone.
- Verdict: **POSITIVE**. No MINOR, MAJOR or BLOCKER is open. My round-1 MINOR (R401-1-F1) and suggestions F2 to F4 are resolved at this head. R400-1 F1 meets the manager's three-point ruling, and R400-1 F2 to F4 are resolved. I record three new SUGGESTIONs (S1 to S3). None of them blocks.

## 1. What was reconstructed, in order

1. The repository still has no AGENTS.md or CONTRIBUTING.md. The conventions come from `README.md` and `docs/README.md`: the single-source rules, and citations as plain clause references.
2. The frozen acceptance and scope decisions on #66:
   - the issue body (items 1 to 3);
   - the lane assignment (comment 5884446021);
   - the round-2 assignment (5887951933);
   - the author's STOP (5890736650);
   - the manager's ruling (5890772857): option 2. A frame whose TX slot was requested before the fall may drain. There is no cancel path and no module port change. R400-1 F1 is graded as three points.
3. The engine's authorities:
   - `docs/architecture/11_maap_engine.md` section 6;
   - the `KL_pp_maap.sv` banner;
   - REQ-MAAP-007 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`;
   - the top's TX pool-access arbiter (`hdl/top/protocol_processor_top.sv:3663-3760`) and `KL_pp_tx_slots`, which the drain rule rests on.

   IEEE 1722-2016 Annex B is cited through the clauses the ruling and the engine quote (Table B.7 Release! row, B.3.1 c) and e), B.3.2, B.3.5.2, footnotes a and c). The standard's text is not distributed with the repository.
4. The diff `c951a9ff..053f979b` (37 files) and the round-2 delta `b03d36f..053f979b` (18 files). I read the whole walker at the head, and each commit on its own.
5. Public evidence at milan-fpga `b67b3f67…/review-evidence/ppC2-r1`. All 468 `MANIFEST.json` entries match their `published_sha256`: 0 mismatches, 0 missing, 0 unlisted files (`receipts/evidence-manifest-verify.txt`). The tree holds the author's round-1 and round-2 packets and both round-1 review packets. The author's `PR-BODY.md` equals the live PR body, apart from one trailing newline.
6. Prior public review findings (R400-1 and R401-1) were read only after my own pass over the diff. They are resolved or retained in section 5.

## 2. Round-2 items, each with its failing arm or mutant

All runs used a `git archive` export of the head under `scratch/`, never the clone, and the pinned Verilator 5.050 (section 8).

| Commit | Item | Evidence at this head | Result |
|---|---|---|---|
| `4de2c60` | Release! honoured in every walker state, ordered by the entry's TX slot request. `W_OFF` starts on the engage level. | Code read: `W_IVAL` (`KL_pp_maap.sv:660-669`), `W_RX` (`:797-804`) and `W_IDLE` (`:747-752`) tear down on a fall before any slot request. The TX states withdraw the claim and latch `rel_pend_r` (`:588-593`). `W_POST` drops the entry's state change (`:719-728`). `W_OFF` starts on `eng_w` (`:597-611`). The head `tb/maap` suite run on the round-1 RTL fails 13 checks in U23 to U26 (2+4+3+4) and 4 in U28 (`receipts/prior-rtl/summary.txt`). The PR's five arms are KILLED. My three extra mutants are KILLED too: `r401-rx-serves-record-after-fall` (U26, U28), `r401-lane-not-latched` (U25) and `r401-post-ignores-a-fall-seen-in-post` (U23). | Correct, graded |
| `8ae76ee` | Footnote-a seed re-armed on every Release! (my R401-1-F1) | `W_OFF` clears `seed_used_r` (`:604`). Every Release! path reaches `W_OFF` (from `W_ADDR` directly, from every other state through `W_TEARDOWN`), and nothing else does except reset. U27 grades both arcs. It fails on the round-1 RTL and on the `4de2c60` RTL (2 FAIL each), and passes at the head. My round-1 probes P1 and P1c both probe the seed `91:E0:F0:00:20:00`. The PR's arm and my `r401-seed-rearmed-in-teardown-only` are both KILLED on U27. | Resolved |
| `fa21c58` | Seed clamp boundary | U18b: `0xFDF9` is clamped to `0xFDF8`, while `0xFDF8` and `0xFDF7` are taken as given, byte-exact with no draw. The PR's `seed-clamp-off-by-one` (compare boundary) is KILLED. So is my `r401-seed-clamp-target-minus-one` (clamp target), with 6 failures in U18 and U18b. | Correct, graded |
| `2c11d6f` | Link drop during a draw that fits (R400-1 F4) | U17c counts drops before the slot request, and after the fall it asserts no send, no adoption and a clean next probe. The PR's `release-waits-for-draw` is KILLED. So is my `r401-ival-keeps-draw-mark`, which leaves the interval draw's mark set on a `W_IVAL` fall (U17c, U23). | Correct, graded |
| `8382cf6` | Stale draw mark: both states named (my R401-1-F4) | The comment at `:614-628` and the README "RTL fix found by U17b" section name `W_ADDR` for an unseeded walk and `W_IVAL` for a seeded one. That matches the code: the unseeded draw arm never re-requests while the mark is set, and the seeded path goes to `W_IVAL`, which waits on the mark. | Resolved (S3 notes a ragged line wrap) |
| `ea79d8b` | Scenario order | `run()` (`sim_main.cpp:1464-1498`) runs U23 to U28 before U19 to U22, so the suite still ends on U22's claim. It is test-only, with no premise lost: head 191/191. | Correct |
| `d0acc9b` | Ruling point 1: no PDU generated after the fall, in all 12 walker states (U28) | See section 3. | Met |
| `4f6affc` | Ruling point 2: at most the one pre-fall frame drains, within 63 cycles (U23) | See section 3. | Met |
| `053f979` | Ruling point 3: `11` section 6 and banner wording and citations | See section 3. It changes comments and docs only: `git diff ea79d8b 053f979 -- hdl` has no non-comment line. | Met |

## 3. R400-1 F1 against the manager's ruling (three points)

**Point 1: no PDU generated after the fall, no slot request, no timer start or expiry, in every walker state.**
- U28 (`sim_main.cpp:1296-1462`) lands 17 falls, each first seen in a chosen walker state, and covers all 12 (mask `0xFFF`). It watches 33 s after each fall. There is no slot request, no timer start, no expiry and no claim, and the machine ends INITIAL. Head: PASS. Against the round-1 RTL it fails 4 checks.
- The PR's `idle-serves-a-latched-expiry-first` and `teardown-keeps-announce-timer` are KILLED. My `r401-teardown-keeps-probe-timer` is KILLED as well: expiries in 10 of 17 falls.
- **Independent extension.** Probes Q1 and Q2 (`scripts/r2_probe_scenarios.inc`) rerun U28's 15 non-bounce fall points with the fall driven by `cfg_en_i`, and by `cfg_count_i -> 0`, instead of `link_up_i`. They cover 10 walker states: all except `W_OFF` and `W_TEARDOWN`, which only the link-bounce points reach. Both give 0 slot requests, 0 starts, 0 expiries and 0 claims after the fall. Only the falls in `W_ALLOC` to `W_COMMIT` owe and drain exactly one frame (`receipts/probes/probes-r2.log`, 213/213).

**Point 2: at most the one frame requested before the fall drains, within the stated window.**
- U23 sweeps 80 fall offsets from the 4th PROBE's lane grant. Before the ANNOUNCE's slot request, 5 offsets send nothing. From the request on, 75 offsets drain exactly one byte-exact ANNOUNCE, with no slot request after it. The measured maximum from the fall to the lane grant is 63 cycles, and no claim is valid after the fall.
- The window check is tight: my `r401-drain-one-cycle-late` (one extra write cycle while a Release! is pending) is KILLED by exactly one of the 75 offsets. The PR's `drain-waits-for-the-link` is KILLED.
- The documented top-level limits are "longer in the top" and "unbounded while the egress stalls (U25)".
- **Independent stalled-drain probes.**
  - Q3 holds the lane for 700 ms behind the first PROBE after the fall. There is no slot request, no timer start and no claim, and the machine is INITIAL. Exactly one frame, the pre-fall PROBE, drains when the lane resumes, and nothing follows for 33 s.
  - Q4 raises the link inside the stall. The drained PROBE is followed by a fresh walk.
  - In both, the next walk's PROBEs are byte-exact and spaced 539 ms and 569 ms apart.
  - One engine timer expiry occurs during each stalled drain. It is inert: no frame, no state change, no stale expiry left for the next walk. This is the behaviour `11` section 6 discloses ("The timers stop once the lane has the frame, and an expiry meanwhile meets INITIAL"). S1 and S2 concern how the PR body and the suite state it.

**Point 3: `11` section 6 and the banner.**
- `11_maap_engine.md:136-168` cites Table B.7 (Release! row), B.3.1 c) and e), B.3.2 and B.3.5.2 for the ordering. It says "no PDU generated after the fall", and states the drain window and its top-level and stall limits.
- The banner `KL_pp_maap.sv:58-79` says the same. So do REQ-MAAP-007 (`00_MILAN_COMPLIANCE_REVIEW.md:453`: "no PDU generated after the fall (a frame an earlier entry already requested may drain)") and `tb/maap/README.md`.
- No unqualified "no PDU" claim remains in docs or RTL. The remaining in-body "no PDU" comments (`:664`, `:749`) sit in states with nothing in flight, so they are exact.

**The drain rule's premise holds at the top.** The pool-access arbiter records a builder's request on its first `alloc_req` pulse (`txc_pend_r`), locks ownership until that builder commits, and has an abort only for the CONTROLLER_AVAILABLE builder (`protocol_processor_top.sv:3665-3760`). An engine that stopped after requesting would therefore leave the pool locked. Recalling the frame needs a cancel port, which the ruling rules out.

## 4. Suites, campaign and static checks at the exact head

| Run | Result | Receipt |
|---|---|---|
| `tb/maap` run | rc 0, 191/191 | `receipts/head-tb-maap.log` |
| `make -C tb/maap mutants` (the PR's campaign) | rc 0. Its 3 controls pass: `tb/maap` 191/191, `tb/rx_validator` 453/453, `tb/pp_top maap-internal` 33 checks with 0 failures. All 24 arms are KILLED: `27 checks: 27 PASS`. | `receipts/head-mutants.txt`, `receipts/head-mutants/` |
| Reviewer-owned mutants (2 from round 1, 8 new) | 10 of 10 KILLED, each with a named failure | `receipts/own-mutants/summary.txt` |
| Round-1 probes P1, P1c, P2, P3, rerun | 209/209. P1 and P1c probe the seed. P2 re-probes after a 1-, 2-, 3- or 4-cycle fall. P3 drains 1 frame whose slot was requested before the fall, with 0 requests after it. The literal round-1 reading of P3 ("no PDU at all") is superseded by the ruling and reported as an OBS line. | `receipts/probes/probes-r1.log` |
| Round-2 probes Q1 to Q4 | 213/213 | `receipts/probes/probes-r2.log` |
| Head tb on round-1 RTL and on `4de2c60` RTL | 20 FAIL (U17c 1, U23 2, U24 4, U25 3, U26 4, U27 2, U28 4) and 2 FAIL (U27) respectively. This matches the PR's failing-first claims. | `receipts/prior-rtl/` |
| Lint of `KL_pp_maap` and `protocol_processor_top` (`lint_hdl.sh` flags) | rc 0, 0 warnings each | `receipts/static/` |
| `gen_matrix.py --check`, `check-links.py`, `git diff --check c951a9ff..053f979b` | rc 0 each. There are 0 gitlinks at the head, and none is required. | `receipts/static/summary.txt` |

The full processor bank, `make check`, Yosys, the SRP campaign and the parent banks were not run, as the scope requires. For the remaining suites I rely on two sources: the author's receipt (`run_suites.sh` 1,015,996 checks, 0 failing), and the hosted "Lint (zero tolerance) + every suite" step, which **executed and succeeded** at this exact head (section 6).

## 5. Findings

No MINOR, MAJOR or BLOCKER is open.

### R401-2-S1: SUGGESTION. Lenses: Docs, Conformance

- **Where:** the PR body, Round 2 section, "The Release! rule" and the per-finding row for `d0acc9b`. Also `tb/maap/README.md:142-165` (U28), and U28's check labels at `tb/maap/sim_main.cpp:1444` and `:1451`.
- **Evidence:** these texts state the Release! as "a stopped timer does not expire", "no timer expiry" and "no slot request follows the fall" without two qualifiers:
  - (a) **Timers during a drain.** The normative texts, `11_maap_engine.md:166-168` and the banner `:77-78`, carry the first qualifier: the timers stop only once the lane takes the drained frame, and an expiry meanwhile meets INITIAL. Probes Q3 and Q4 show one engine timer expiry after the fall during a 700 ms stalled drain. It is inert.
  - (b) **Retries at the top.** Under pool contention, the engine's retry of its pre-fall allocation (`W_GWAIT -> W_ALLOC`, `KL_pp_maap.sv:695-702`) keeps raising `txs_alloc_req_o` after the fall until the arbiter grants it (`protocol_processor_top.sv:3669-3671`). That is the same frame, not a new one.

  U28's labels are true in the unit bench, where the lane grants at once and the pool is never contended.
- **Impact:** none on behaviour. No PDU is generated after the fall in either case, and the normative `11` section 6 is accurate. A reader of the PR body or the README alone could take "timers stopped at the fall" and "no slot request" literally at the top.
- **Suggested outcome:** when next touched, scope these sentences as `11` section 6 does:
  - "timers stop when the lane takes the drained frame";
  - "no new slot request after the fall; a pending pre-fall allocation may still be retried".

### R401-2-S2: SUGGESTION. Lens: Tests

- **Where:** `tb/maap` U25 (`sim_main.cpp:1153-1196`).
- **Evidence:** `11` section 6's statement that "an expiry meanwhile meets INITIAL, where it is -x-" is not graded by any suite scenario. U25 stalls for 100 ms in DEFEND, where the 30 s announce timer cannot expire. Probes Q3 and Q4 grade it (a 700 ms stall in PROBE, with and without a rise inside the stall) and pass at the head.
- **Suggested outcome:** optionally add a Q3/Q4-shaped arm. No plausible mutant I tried survives: the drain always passes `W_POST`, which tears down and clears the latch. So this closes a documentation-to-test gap, not a behavioural one.

### R401-2-S3: SUGGESTION. Lens: Docs

- **Where:** the PR body's round-1 section "What remains", and `KL_pp_maap.sv:619-623`.
- **Evidence:** "What remains" still lists the two Release! corners (the seed re-arm and the frame after the fall) as "not in this scope; each would need its own issue". Round 2 has since resolved both, and the Round 2 section says so, but "What remains" carries no superseded note. Separately, the comment at `:619-623` has a ragged wrap ("never drawing / again, and so would a seeded next / walk, …").
- **Suggested outcome:** mark "What remains" as superseded by Round 2, and re-flow the comment when the file is next touched.

### Prior public review findings on this PR, at this head

| Finding | Status at `053f979b` | Basis |
|---|---|---|
| R401-1-F1 (MINOR, seed re-arm on the `W_ADDR` arc) | **Resolved**, outcome (a) | `8ae76ee`. P1 and P1c probe the seed. U27 is red on both earlier RTLs and green at the head. Two arms are KILLED (the PR's and mine). The banner `:315-322` and `11` section 6 agree with the RTL. |
| R401-1-F2 (SUGGESTION, short fall absorbed) | **Resolved** | `4de2c60`. `W_OFF` starts on the engage level. P2 re-probes after a 1- to 4-cycle fall. U26 grades it. `off-waits-for-an-edge` is KILLED. |
| R401-1-F3 (SUGGESTION, a frame after the fall in `W_IVAL` and the TX states) | **Resolved per the ruling** | `W_IVAL` now drops the entry. A frame requested before the fall drains (ruling option 2). P3's one frame was requested before the fall, with 0 requests after it. |
| R401-1-F4 (SUGGESTION, name both stalled states) | **Resolved** | `8382cf6` |
| R400-1-F1 (MINOR) | **Resolved against the ruling's three points** | Section 3 |
| R400-1-F2 (MINOR) | **Resolved** | The same change as R401-1-F1 |
| R400-1-F3 (MINOR, seed clamp boundary) | **Resolved** | U18b. Two boundary arms are KILLED. |
| R400-1-F4 (MINOR, drop during a draw that fits) | **Resolved** | U17c. Two arms are KILLED. |
| R400-1-S1, S2 (SUGGESTIONs) | **Retained** by the author as outside the round-2 assignment, as the PR body states | Not blocking |

## 6. Hosted checks at `053f979b`

Polled at 2026-09-29 15:33 UTC (`receipts/hosted-checks.txt`, `receipts/hosted-suites-steps.txt`). The only workflow run is 36588714000 (push), and the combined status was `pending`.

| Job | State |
|---|---|
| `docs-gates` | completed, **success** |
| `portability` | completed, **success** |
| `suites` | **in progress** |

The `suites` job's steps stood as follows:

| Step | State |
|---|---|
| Pinned-simulator cache | success |
| Simulator build | skipped (cache hit) |
| "Lint (zero tolerance) + every suite" | **executed, success** |
| SRP LeaveAll mutation campaign | running |
| **MAAP mutation campaign**, traceability, nvm_port figures | pending, **not yet executed** |

Hosted and act acceptance belong to the manager.

## 7. Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 is a SUGGESTION) | The ruling's clauses (Table B.7 Release!/PortOperational!, B.3.1 c) and e), B.3.2, B.3.5.2, footnotes a and c) against the walker. The drain premise in the top's pool-access arbiter and `KL_pp_tx_slots`. REQ-MAAP-007. U23 and U28, plus probes Q1 to Q4 for all three engage-fall sources. | R401-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| RTL | CLEAN | The full `KL_pp_maap.sv` walker at the head and each round-2 hunk. `rel_pend_r` set, clear and use. The reach of `W_OFF`. Draw-mark handling in `W_ADDR` and `W_IVAL`. Teardown timer cancels. Post-ruling commits are comment-only. Lint of the module and the top is rc 0. 10 reviewer mutants are KILLED. | R401-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Robustness | CLEAN | Short falls (P2, U26). A rise inside the teardown, drain or stall (U24, U25, Q4). A stalled drain longer than a probe interval (Q3). Falls from `cfg_en_i` and `cfg_count_i` (Q1, Q2). Stale draw marks. Top pool contention, reasoned in S1(b). The campaign driver: controls first, named failures, UNPROVEN on a build failure or a missing tally. | R401-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Tests | CLEAN (S2 is a SUGGESTION) | U17c, U18b and U23 to U28, and their premises. The head suite on two earlier RTLs, matching the failing-first claims. The PR campaign rerun at 27/27, with the same tallies as its ledger. Reviewer mutants for every round-2 commit. Round-1 probes rerun. | R401-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Docs | CLEAN (S1 and S3 are SUGGESTIONs) | `11_maap_engine.md` section 6, the banner and in-body comments, REQ-MAAP-007, `tb/maap/README.md` (the U17b to U28 text and the ledger), the PR body's Round 2 section (the ruling and its limits, closing references #66, #67 and #68), and the author's public `HANDOFF.md` design. | R401-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |

## 8. Real limits and pending manager duties

**Limits:**
- **Simulator launcher.** The launcher path given in the brief does not exist on this host. I used the manager's per-head 5.050 launcher for this lane instead. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and the binary it runs has sha256 `fb2cc573b1055cf096c90e1efc9966fe56bdb4b265c83590cf2a49f7a0defcdf` (`receipts/verilator-identity.txt`).
- **Manager bank receipts.** The public evidence tree at `b67b3f67` holds author and round-1 review packets only. I found no manager bank receipt at this head there, nor in public comments on #66 or #135, nor on milan-fpga #76 or #415 since 2026-09-29. So I could not inspect the manager's source, static, builder and native banks. I take them as the brief states them.
- **Unit bench only.** All drain and window evidence is from the unit bench. The top-level window ("longer") and the contention retry in S1(b) are reasoned from the source, not measured.
- **Standard text.** I did not consult the text of IEEE 1722-2016 (it is not distributed). Annex B judgements follow the clauses quoted in the ruling, the author's public HANDOFF and `11`.
- **Banks not run.** I did not run the full processor, parent, Yosys or builder banks, the SRP campaign or `make check`, as the scope requires.
- **Merge composition.** I did not judge the merge with processor main `b2db3a97` (the conflicts in `tb/pp_top/sim_main.cpp` and `tb/rx_validator`). That is a later round.
- **Hardware.** Physical calibration was **not run**. Field skips are not hardware proof.

**Pending manager duties:**
- Run and post the donor full bank and the parent consumer bank at milan-fpga dev `ec0cc0c1`.
- Accept the hosted `suites` job once its SRP campaign, MAAP campaign, traceability and figures steps have executed at this head.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`, live dev `ec0cc0c1`), and run the delta review of the merge of main `b2db3a97`.
- Decide on S1 to S3 (optional).

**Clone integrity after the probes (`receipts/clone-verify.txt`):**
- HEAD is `053f979b…` and the tree is `33087148…`. The index writes back the same tree.
- The worktree and index equal HEAD, with 0 untracked or ignored entries.
- All 332 tracked blobs match in bytes and mode.
- There are 0 gitlinks, and none is required at this head.

Every probe and mutant ran in `scratch/` exports only. No source edit, commit, push or GitHub write was made.

**Reproduce:** set `CLONE` (a clone holding the head) and `VLT` (a Verilator 5.050 launcher), then run from the packet root:

```
scripts/01_export_and_suites.sh
scripts/02_campaign.sh
scripts/03_probes.sh
PKT=$PWD python3 scripts/04_own_mutants.py
scripts/05_prior_rtl.sh
scripts/06_static.sh
scripts/07_verify_clone.sh
```

R401-2 FINISHED
