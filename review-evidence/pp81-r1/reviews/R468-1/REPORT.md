[R468] NEGATIVE - exact head db2c4eb823c47b2607fb52234b58ac6b93ff548b

# R468-1: internal independent review of PR #157 (issues #81 / GAP-07 and #84 / GAP-10)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #157 (`Closes #81`, `Closes #84`).
- Exact head `db2c4eb823c47b2607fb52234b58ac6b93ff548b`, tree `f0d2f707c92a961253cb311e5555a5f5b58c2666`; lane base `83999eba1ef4756e9e769e4fba164f5095761604`; merged `main` `c050d971`.
- Scope authorities: the #81 and #84 issue bodies (acceptance), the closeout assignment (#81 comment 5977862493), the manager rulings (#81 comment 5981958399), the area evidence comment (PR #157 comment 5981967051), docs/README.md conventions. The repository has no AGENTS.md or CONTRIBUTING.md. docs/README.md §6 is the author workflow it defines, and I followed it.
- Verdict: **NEGATIVE** on one MINOR finding (F1, a stale class claim in two normative tables and one enumeration). Everything else the assignment and rulings ask for is met and was re-executed. That includes the RTL, the TD default pin, the GDI serialization, the arms, the records and the area attribution.

## 1. What the PR changes (reconstructed from the diff)

`git diff 83999eba..7b95590` (the lane) and `git diff c050d971..db2c4eb` (the merge) are the same patch: 15 files, +374/-53. I compared them with `index` lines stripped, and they are byte-identical. The merge of `main` brings only PR #153's own files.

| Item | Change | Files |
|---|---|---|
| 1 (F08.1) | T-IDENT-BURST and T-IDENT-REARM are marked **landed** (#80), owned by `KL_aecp_notify`, built only with P-EN-IDENTIFY-NOTIFICATION = 1, and graded by `tb/pp_top` ID and `tb/aecp_notify` FT. T-CTR-OBSERVE is **integrator-owned**. 09's TIM row is narrowed to "every F08.1 row with RTL here". | `docs/architecture/08_timing.md:30-32`, `docs/architecture/09_verification.md:53` |
| 3 (reset) | 02 §2 rule 5 now states one synchronous active-low `rst_n`, no asynchronous flop reset, and boot order kept by holds. | `docs/architecture/02_interfaces.md:115-124` |
| 2 (defaults) | A sixth `tb/pp_top` build, `PP_TOP_TIM_DEFAULTS`, drops the wrap's two 400 ms overrides and keeps the 1 ms = 100 clk prescaler. Section TD adds TD1 (auto-unlock 60,000 to 60,020 ms after LOCK_ENTITY) and TD2 (TIME_LIMITED expiry 300,000 to 300,020 ms after REGISTER). It adds two arms that move the top's parameter defaults. | `tb/pp_top/pp_top_wrap.sv:549-557`, `tb/pp_top/Makefile:166-196`, `tb/pp_top/notify_phases.hpp:1608-1717`, `tb/pp_top/aecp_mutants.py:61-67`, `tb/pp_top/mutations/td-*.patch` |
| 4 (GDI) | In the F03.7 classifier, an AEM GET_DYNAMIC_INFO for this entity now presents `MAP_CFG` with the NONE key, which was `RO_SNAPSHOT`/NONE before. The change also updates the classifier comment, HZ1's GDI row, an HZ8 exception, HZ13a/b/c and four arms, plus 03 §6, 08 §4 and 09 §8.3. | `hdl/top/protocol_processor_top.sv:1542-1554,1645-1646`, `tb/pp_top/sim_main.cpp:13165-13167,13703-13743`, `tb/pp_top/aecp_mutants.py:176-189`, `tb/pp_top/mutations/hz-gdi-*.patch` |

## 2. Findings

### F1 (MINOR): F06.14, F03.7 and 03 §6's classifier enumeration still say GET_DYNAMIC_INFO is RO_SNAPSHOT

- **Lenses:** Docs, Conformance, Tests.
- **Where:**
  - `docs/architecture/06_aecp_engine.md:269`: F06.14's GDI row, Class column `RO per record`. F06.14's legend says "hazard class per 03 §6". PR #140 updated the SET_CONFIGURATION row of the same column to the landed class (`CFG_BARRIER (assigned by the top's classifier, 03 §6)`).
  - `docs/architecture/03_packet_engine.md:235`: F03.7's `RO_SNAPSHOT` row, "Members: all GETs, ...". The `MAP_CFG` row at `:238` does not name GET_DYNAMIC_INFO.
  - `docs/architecture/03_packet_engine.md:246-251`: the landed-classifier enumeration ends "SET_CONTROL `IDENTIFY`; every other command `RO_SNAPSHOT`". GET_DYNAMIC_INFO is not in the list. The same paragraph says 18 lines later (`:269`, `:274`) that it presents `MAP_CFG` and is "the one read outside `RO_SNAPSHOT`".
- **Authority and evidence:**
  - At this head the RTL gives GDI `MAP_CFG` (`hdl/top/protocol_processor_top.sv:1645-1646`), and HZ1 requires it (`tb/pp_top/sim_main.cpp:13167`). My reruns confirm both: HZ 189/0, `hz-gdi-key-none` fails HZ1 with "admitted RO_SNAPSHOT ... (want MAP_CFG)".
  - The HZ section declares its expectation to be "an independent transcription of F03.7 and F06.14" (`tb/pp_top/README.md:914-916`, `tb/pp_top/sim_main.cpp:12959`). On the GDI row it now contradicts both tables.
  - The assignment's item 4 asks to "Update 03 §6", and F03.7 is 03 §6's table.
- **Impact:**
  - A reader of the command master table, or of F03.7 (both are docs/README.md §2 figure IDs), is told GDI is a read snapshot that never blocks ACMP. In fact it waits for, and holds back, every ACMP stream step. 08 §4 counts that wait against `T-BUDGET-ACMP-RESP`.
  - The suite's stated oracle and its GDI expectation disagree.
  - The fix edits figures, so this is not prose-only RESIDUE.
- **Required outcome:**
  - F06.14's GDI Class cell names the landed admission class, in the style of the SET_CONFIGURATION cell. For example: `MAP_CFG at admission, no-descriptor key (assigned by the top's classifier, 03 §6); records RO`.
  - F03.7 records the exception. Either the `MAP_CFG` row lists "GET_DYNAMIC_INFO (whole batch, no-descriptor key; the accepted over-serialization)" or the `RO_SNAPSHOT` row reads "all GETs but GET_DYNAMIC_INFO".
  - The 03 §6 enumeration lists "GET_DYNAMIC_INFO `MAP_CFG` (below)" before "every other command `RO_SNAPSHOT`".
- **Verification:**
  - `make check` passes: lint, links, matrix, modmatrix, params, stale, wavedrom-check.
  - `grep -n "RO per record" docs/architecture/06_aecp_engine.md` is empty, or the cell carries the admission class.
  - HZ1's GDI row and the two tables agree.

### Suggestions (do not affect the verdict)

- **S1 (Tests, SUGGESTION): state or tighten TD's band.**
  - TD measures 60,003 and 300,002 ms against a window of [default, default + 20 ms]. A default moved by only a few ms therefore survives. My edge probes (`receipts/runs/p_td_*.log`) show what passes:
    - LOCK_TIMEOUT_MS_P 59,997 and 60,017, REG_TL_TIMEOUT_MS_P 299,998 and 300,018: all **pass**, measured 60,000 / 300,000 and 60,020 / 300,020.
    - 59,996 / 299,997 and 60,018 / 300,019: **fail**.
  - So TD pins each default to a 21 ms band: −3/+17 ms for the lock and −2/+18 ms for the registration. That is ample against any realistic typo (the arms use ±1 s), so acceptance 4 is met.
  - Either record the band in the README's TD paragraph and 09 §8.3, or narrow `SLACK_MS` toward the measured +3 ms.
- **S2 (Tests, SUGGESTION): HZ13 could grade more than admission.**
  - HZ13 discards the batch answers (`(void)`) and grades only one direction of the read pair. My probe (`scripts/probe-hz-extra-checks.patch`) adds 11 checks, and all pass at this head (HZ 200/0):
    - PROBE-A: HZ13a's batch answers SUCCESS, 102 bytes.
    - PROBE-B and PROBE-C: an ACMP GET_RX_STATE of sink 1 and a GET_TX_STATE of source 1 are admitted beside a held GDI.
    - PROBE-D: a talker DISCONNECT_TX of source 1 waits for a held GDI, the over-serialization on the talker side.
  - Adopting them is optional.
- **S3 (Docs/PR body, SUGGESTION):** item 3 also meets #71 acceptance 2 (02 §2 rule 5 matches the synchronous `rst_n`). #71 is one of #84's requirement tickets. A "Relates to #71" line would let the manager account for it. #71's other two acceptance items are untouched.

### Prior public review findings on this PR

PR #157 carried no review findings before this round. Its only comments are the area-evidence note and the two review-start notices, with zero review objects and zero inline comments. So there is nothing to resolve or retain.

The PR is the remedy for R419-2 F5, a finding on PR #140 that the manager ruled into this lane's item 4. I confirm it **resolved** at this head:
- HZ13a, R419-2's G0 graded on the batch, passes.
- Reverting to the NONE key (`hz-gdi-key-none`) reproduces G1: "admitted beside the held UNBIND_RX ... refused 0 clocks".

## 3. Lenses

### Conformance: UNCLEAN (F1)

**#81 acceptance 4, first half.** Ruling (1) is met.
- T-IDENT-BURST and T-IDENT-REARM have RTL: `hdl/aecp/KL_aecp_notify.sv:163-213`, the IDENT-BURST/REARM singletons.
- Their cited grading exists:
  - `tb/pp_top/notify_phases.hpp:187` onward, ID1 to ID8 in the third build;
  - `tb/aecp_notify/README.md:27-60`, FT1 to FT4 with the timebase arms;
  - `tb/pp_top/notify_mutants.py:52-90`.
- The head full suite's identify build ran 178/0.
- The 09 §8.4 anchor resolves (links 1,122 OK).
- T-CTR-OBSERVE is integrator-owned, consistent with 06 §6.6 and 08 §5.
- The narrowed TIM row is consistent. The only unimplemented rows are T-CTR-OBSERVE (named) and T-AECP-INPROG ("unused by policy").
- No other file claims the three rows are graded. I grepped docs/, tb/*/README.md and the top-level READMEs.

**#81 acceptance 4, second half.** Ruling (2) is met; see Tests.

**#84 acceptance 4.** Ruling (3) is met.
- Every `always_ff` in hdl/ is `@(posedge clk_i)`: 159 of 159, no `negedge`, no reset in a sensitivity list, no plain `always @`.
- The top has one reset port, `rst_n` (`hdl/top/protocol_processor_top.sv:233`).
- The boot holds the rule cites match 01 §5 (`docs/architecture/01_overview.md:102-110`).
- No other asynchronous-reset wording remains in docs/ or in the diagrams.

**GDI semantics.** The clauses are 03 §6 F03.7, IEEE 1722.1-2021 §7.4.76.1 and Milan §5.4.2.10.
- The batch now waits for an in-flight listener step of a sink its record names, as the stand-alone getter does.
- The over-serialization is the one the assignment accepted.
- F06.14, F03.7 and the 03 §6 enumeration still state the old class: **F1**.

### RTL: CLEAN

- **The change.** The only RTL change is one `unique case` arm, `16'h004B: hz_class_w = MAP_CFG`, and its comment. The key stays at the always_comb default, `HZ_KEY_NONE_C = {6'h3F, 10'h000}`. The arm overlaps no other item. It applies only under `hz_aem_cmd_w`, an AEM command for this entity. A response arriving as input, a foreign target, MVU and AA are untouched (HZ1 rows; arms `hz-foreign-target-classified` and `hz-response-classified` still killed).
- **What consumes the class.** `pp_txn_t.hazard_class` is read only at the scoreboard admission mux (`hdl/top/protocol_processor_top.sv:3569-3576`). Nothing else in hdl/ reads it, so lock refusal, deadline preemption and dispatch are unaffected.
- **The scoreboard matrix**, `hdl/packet_engine/KL_pp_scoreboard.sv:119-157`:
  - `MAP_CFG` against `STREAM_CFG` is the class-wide rule (5), which gives the intended hold.
  - Against `RO_SNAPSHOT` it is same-key only (rule 2). ACMP keys are `{5|6, uid}` and never `0x3F`, so the batch runs beside every ACMP read.
  - Against `LOCK_OP`, `CFG_BARRIER` or another `MAP_CFG`, only AECP presents those classes, and the AECP engine is single-issue, so no new pair is reachable.
- **No other class or key changed.** HZ1 grades all 33 AECP and 6 ACMP rows, and only the GDI row moved, from RO to MAP. My rerun: HZ 189/0. All 61 AECP arms match their README counts.
- **Lint:** `scripts/lint_hdl.sh` passes, 41 modules LINT OK.
- **Area.** The four published OOC 1x1 runs (milan-fpga `pp81-review-evidence` @ `a1b03e32`) hash-match their MANIFEST `published_sha256` (28 files). Their parameter files are identical. Their figures equal the PR body:
  - base 24,930 LUT / 25,465 FF; head 24,900 / 25,461, so **−30 LUT / −4 FF**;
  - main 24,130 / 23,418; merge 24,197 / 23,528, so +67 / +110.
- **The +110 FF.** The top RTL blob is identical between base and main (`1237d47e`) and between head and merge (`b6b8a52f`).
  - All +110 FF sit in the top's own hierarchy row: (u_pp) 3,169 → 3,279.
  - That fits the ruling's attribution. `arm_drain_pick` (`:2990-3000`) pops face 0 whenever its count is non-zero, because face 0 is first in the loop. So `armq_cnt_r[0]` never exceeds 1, and `armq_r[0][1..3]` (3 × 36 kept bits) plus two count bits are dead.
  - The ruling's 60/60 STOP line applies to the base→head pair, which is well inside it.

### Robustness: CLEAN

- **The new wait is bounded.** An ACMP stream step can now wait for an in-flight GDI. GDI is deadline-preempted: the arm `dl-gdi-runs-on` is still killed (DL4). So the wait is bounded by `T-BUDGET-AECP-WC` plus the op in progress, a few ms. That is inside `T-ACMP-CMD` (200 ms).
- 08 §4 lists exactly this hold (`docs/architecture/08_timing.md:197-200`) and states that the answer can exceed the 50 ms design budget.
- **The over-serialization covers the talker side too.** PROBE-D: a DISCONNECT_TX waits for a held GDI. ACMP reads keep running beside a held GDI (PROBE-B/C). The batch still answers SUCCESS after it waits (PROBE-A).
- **Classifier mutations are caught.** My two extra classifier mutants are killed:
  - GDI → `STREAM_CFG`/NONE: 9 failures (HZ1, HZ8, HZ13a, HZ13c, PROBE-D).
  - GDI → `LOCK_OP`/NONE: 1 failure (HZ1). That class behaves identically at this top, and HZ1's exact class check is what pins it.
- **TD is robust in two ways.** Its registration is kept alive only by answering the monitor (6 probes answered), so only the timer under test can end it. Its expectation is byte-exact apart from the echoed sequence_id.

### Tests: UNCLEAN (F1's oracle statement; S1 and S2 are suggestions)

- **Head full suite:** `make -C tb/pp_top` rc 0, 10,431 / 0 over six builds. Per build: default 9,943, fixture 20, identify 178, line 231, timebase 56, defaults 3. TD measured 60,003 ms and 300,002 ms with 6 monitor probes, as in the PR body.
- **Base:** the hazards section is 177/0. The head's is 189/0, so +12 = HZ8 batch 3, HZ13a 3, HZ13b 2, HZ13c 4.
- **Ruling (2): does TD catch a changed default rather than a changed prescaler?**
  - Moving only the top's parameter default moves the measurement 1:1. My edge probes fail at 59,996 / 299,997 and at 60,018 / 300,019. The two committed arms are killed (59,003 ms; no DEREGISTER by 300,020 ms).
  - Moving only the sixth build's prescaler leaves TD passing, because TD reads the DUT's own ms timebase (`dbg_now_ms_o` = `now_ms_w`). With 1 ms = 200 clk it measured 60,001 / 300,001; with 1 ms = 50 clk, 60,007 / 300,005.
  - So the check keys on the default, not on the prescaler. The band is S1.
- **AECP campaign at head**, full, `--jobs 8`: rc 0, 6 controls PASS, 61 of 61 KILLED. Every arm's failure count equals the README table, including:
  - `hz-stub-restored` 81, `hz-acmp-reads-as-steps` 27, `hz-barrier-no-priority` 139;
  - `hz-gdi-key-none` ×3 at 7, `hz-gdi-as-barrier` 2;
  - the TD arms at 1 each.
  - `receipts/runs/aecp_full.log`, `receipts/runs/aecp_readme_compare.txt`. The two "DIFF" lines there are a parser artefact on the README's "the same 12" row, and both arms do show 12.
- **Other pp_top campaigns at head** (each rc 0, the PR body's record):
  - `aecp_dispatch_mutants.py`: 44 of 44;
  - `acmp_mutants.py`: 19 of 19, goldens PASS;
  - `ctr_mutants.py`: 18 of 18;
  - `gsi_mutants.py`: 20 detected, golden and restored PASS;
  - `name_wr_mutant.py`: killed, golden and restored PASS.
- **F1** applies here because the HZ section's declared oracle (F03.7 and F06.14) no longer matches its GDI expectation.

### Docs: UNCLEAN (F1)

- **Gates** at head, in a scratch clone: `make lint links matrix modmatrix params stale wavedrom-check` all rc 0.
  - links 1,122 OK (the PR body's figure);
  - matrix 115 REQ rows and 17 GAP findings;
  - modmatrix 94 rows, 0 untested;
  - params 28/28/28;
  - wavedrom 18 blocks.
  - `git diff --check` is rc 0 for both pairs.
- **PR body citations** at head match the cited lines. I checked 08:30-32, :170-171, :197-200; 09:53, :254, :270-272; wrap :549-557; Makefile :169-170, :185-196; notify_phases :1608-1717; aecp_mutants :61-67, :176-189; top :1542-1554, :1645-1646.
- The README's records, build tables and the campaign note match my reruns.
- **F1** is the stale class claim in F06.14, F03.7 and the 03 §6 enumeration.

## 4. Records that changed (base → head, checked)

| Record | PR body | Reviewer rerun at head |
|---|---|---|
| `tb/pp_top` HZ | 177 → 189 | base 177/0, head 189/0 |
| `tb/pp_top` sixth build TD | none → 3 | 3/0 (60,003 / 300,002 ms) |
| `tb/pp_top` total | 10,416 → 10,431 | 10,431/0, six tallies |
| `make check` links | 1,120 → 1,122 | 1,122 OK |
| AECP campaign | 5 controls / 55 arms → 6 / 61 | 6 PASS / 61 KILLED |
| `hz-stub-restored` / `hz-acmp-reads-as-steps` / `hz-barrier-no-priority` | 74→81 / 26→27 / 127→139 | 81 / 27 / 139 |
| dispatch, ACMP, counters, GSI, NAME_WR campaigns | identical | identical totals (above) |
| `run_suites.sh` sweep | +15 | not re-run (the +15 is `tb/pp_top`'s, rerun above) |

## 5. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #81/#84 acceptance and rulings; 08 F08.1, 09 TIM, 02 §2 rule 5, 03 §6 F03.7, 06 F06.14; RTL reset sweep; identify RTL and suites | R468-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| RTL | CLEAN | classifier arm and comment; scoreboard matrix; hazard_class consumers; lint_hdl 41/41; four OOC runs, hashes, hierarchy; arm-queue logic | R468-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Robustness | CLEAN | 08 §4 hold bound; deadline arm DL4; PROBE-A..D; two extra classifier mutants; TD keep-alive | R468-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Tests | UNCLEAN (F1) | head `tb/pp_top` 10,431/0; base/head HZ; TD edge and prescaler probes; full AECP campaign 61/61 with per-arm counts; dispatch, ACMP, counters, GSI, NAME_WR campaigns | R468-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Docs | UNCLEAN (F1) | docs gates; PR body citations; tb/pp_top README records; F06.14/F03.7/03 §6 text | R468-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |

## 6. Real limits

- **Not re-run by me:** `./scripts/run_suites.sh`, the Yosys bank, the D3, notify, MAAP and ADP campaigns, and the parent consumer set of 17 at dev `fea346e7` with the c8, p2-p1, c10 and 232 patches. Those are full banks the assignment reserves to the manager, or campaigns the lane diff does not build. No Vivado run. Area is judged from the published runs.
- **Area trimming evidence.** The published synthesis logs do not name the trimmed `armq_r[0][1..3]` registers: Vivado caps the repeated INFO messages at 100. So the "trimmed in three builds, kept in the merge build" mechanism rests on the hierarchy's top-own FF delta (+110, exact) and the RTL argument, not on a netlist listing.
- **Evidence location.** The evidence commit named in the assignment, milan-fpga `5de7b6be`, contains only `review-evidence/pp81-r1/author/` and MANIFEST.json. The OOC runs are in its child `a1b03e32`, the `pp81-review-evidence` branch head named by PR comment 5981967051. I found no public receipts for the manager's source static/builder and native banks in either commit, so I could not check that claim.
- **Hosted CI** at the exact head, at the time I checked (`receipts/hosted_checks_snapshot.txt`): `docs-gates` and `portability` succeeded for both the push and the pull_request event. `suites` was still in progress for both. Nothing there is accepted by me.
- **Not hardware proof.** Physical calibration was NOT RUN. Field skips are not hardware proof. This review is source validation only, not the final current-dev candidate.

## 7. Pending manager duties

- Carry F1 back to the lane, or rule on it.
- Build the final current-dev candidate at the merge turn: source base `83999eba`, live dev `fea346e7`.
- Run the parent consumer set of 17, applying PR #153's own `parent-adoption-232-241f9184.patch`, which the pin bump owes for gate 9. Gate 16's T30 checks belong to milan-fpga #643 / PR #648.
- Accept the hosted and act results once `suites` completes at the exact head.
- Publish or point to the manager bank receipts this review could not locate.
- Take S1 to S3 into account at your discretion.

## 8. Receipts and clone state

Every publishable receipt is listed in `MANIFEST.sha256`, with paths relative to the packet root:

- `scripts/run_probes.sh` and the `scripts/probe-*.patch` files reproduce the probes from `git archive` exports. The prescaler probes are `probe-td_presc.patch` (1 ms = 50 clk) and `probe-td_presc2.patch` (1 ms = 200 clk).
- `receipts/runs/` holds every run log and rc file: the head full suite, base and head hazards, the TD edge and prescaler probes, the HZ extra-check probe and its mutants, the selected and full AECP campaigns, the five other campaigns, the docs gates and lint.
- `receipts/aecp_full/` holds the per-arm logs.
- `receipts/area/area_extract.txt` holds the area figures and hash check.
- `receipts/clone_integrity.txt` is the post-run clone check.

The review clone was never written. Every probe ran in an export under scratch/. After the runs, HEAD is `db2c4eb8`, the tree is `f0d2f707`, `git status --porcelain --ignored` is empty, the index equals the tree, and every worktree blob equals its index blob (519 files: 504 at mode 100644, 15 at 100755). This repository tracks no submodule gitlinks.

R468-1 FINISHED
