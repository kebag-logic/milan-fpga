[R469] POSITIVE - exact head db2c4eb823c47b2607fb52234b58ac6b93ff548b

R469-1, the external independent review of issue #81 (GAP-07) and issue #84 (GAP-10) through processor PR #157, in a cleared context.

- Head `db2c4eb823c47b2607fb52234b58ac6b93ff548b`, tree `f0d2f707c92a961253cb311e5555a5f5b58c2666`.
- Lane base `83999eba1ef4756e9e769e4fba164f5095761604`. The PR's GitHub base is `main` `c050d971`.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN.
- Two SUGGESTIONs: S1 (how tight the TD window is) and S2 (an item in #84's "What remains" that the frozen acceptance does not list).
- One RESIDUE: R1, wording in 09 under the single-source rule.

Every assignment item and manager ruling checks out at this head:
- **F08.1.** The rows are reclassified, and the cited identify tests exist and pass.
- **Defaults.** The 300 s and 60 s defaults are graded at the real count. The check is independent of the prescaler. Both arms that move a default are killed.
- **Reset.** 02 §2 rule 5 states the synchronous active-low reset, and the RTL implements it.
- **GET_DYNAMIC_INFO.** The batch now takes MAP_CFG and waits for every ACMP stream step, while it still runs beside ACMP reads. HZ8 is amended for exactly this case, and HZ13 is added. All four new arms are killed, and no other class or key changed.
- **Area.** The published OOC 1x1 figures reproduce exactly from the published reports. The ruling's attribution of the merge pair's +110 FF is consistent with the RTL.

## 1. Reconstruction, in the prescribed order

1. **Workflow rules.** This repository has no AGENTS.md or CONTRIBUTING.md. I read `README.md` and `docs/README.md`, including the single-source rules in §2 and the editing workflow in §6.
2. **Issue scope.**
   - #81 and #84 bodies, with their frozen acceptance: #81 items 1-4 and #84 items 1-4.
   - Every comment on #81 and #84.
   - The assignment, #81 comment 5977862493.
   - The rulings, #81 comment 5981958399. Ruling (1): T-IDENT-BURST and T-IDENT-REARM are landed and graded, and T-CTR-OBSERVE is integrator-owned. Ruling (2): item 4's cost is the base-to-head pair, and the merge pair's +67/+110 is untrimmed dead armq entries.
   - REVIEW READY 5981951639.
3. **Authorities.**
   - F03.7 and 03 §6.
   - `KL_pp_scoreboard.sv` rules (1) to (6). Rule 5 is the class-wide MAP_CFG and STREAM_CFG cross-lock.
   - F08.1 and 08 §4, 09 §8.3 and §8.4, 02 §2, the integrator guide §1, F01.5 and 01 §7.
   - The 00 GAP-07 and GAP-10 entries.
   - Clauses cited in the tree: IEEE 1722.1-2021 §7.4.2, §7.4.37.2 and §7.4.76.1; Milan v1.2 §5.4.2.2, §5.4.2.10 and §5.4.5.3. I read them through their in-tree quotations, because the specification PDFs are not distributed.
4. **Diff and history.**
   - `git diff 83999eba..db2c4eb`: 20 files, +802/−74.
   - The lane's own commits: 4ffd8f0, 371505d, bacad0e, beb7c22 and 7b95590.
   - The merge db2c4eb of `main` c050d971 (PR #153). `git merge-tree 7b95590 c050d97` gives exactly the head tree.
   - The stable patch-id of `83999eba..7b95590` equals that of `c050d97..db2c4eb`. So the merge adds nothing beyond the two sides (`receipts/static-checks.txt`).
5. **Public executable evidence.**
   - kebag-logic/milan-fpga `5de7b6be` `review-evidence/pp81-r1`: MANIFEST.json and the author packet.
   - The four OOC 1x1 runs under `review-evidence/pp81-r1/author-r1/vivado/`, which live at the branch head `a1b03e32`, not at `5de7b6be`. Every file I used matches its published git blob id.
   - The manager's evidence comment, PR #157 comment 5981967051.
6. **Prior findings.**
   - PR #157 has no prior public review finding. Its only comments are the evidence notice and the two review-start notices.
   - After my own pass, I read R419-2 F5 (PR #140 comment 5928298648). This lane resolves it (section 4).

## 2. Executable evidence produced by this round

Every run used `git archive` exports under `scratch/`, never the clone, with the pinned simulator 5.050 (`receipts/tool-identity.txt`). Each export's tracked blobs equal its commit's tree (`receipts/clone-integrity.txt`). Local paths in the logs are normalized to `<PACKET>`, `<CLONE>` and `<PINNED_ROOT>`.

| Receipt | What ran | Result |
|---|---|---|
| `receipts/probes-controls.txt`, `receipts/probes/control--*.log` | head: `make -C tb/pp_top timer-defaults` and `hazards` | TD **3/0**: auto-unlock 60,003 ms, expiry 300,002 ms, 6 monitor probes answered. HZ **189/0** |
| `receipts/probes-base.txt` | base `83999eba`: `hazards` | HZ **177/0**. The +12 equals HZ8's batch (3), HZ13a (3), HZ13b (2) and HZ13c (4) |
| `receipts/probes-dl-tb.txt` | head: `deadline` and `budget` | DL **64/0**, TB **56/0**. The TB histogram equals the 08 §4 table, for example GDI 12,852 clocks, GDI behind fan-out 24,681, GET_RX_STATE beside READ_DESCRIPTOR 172 |
| `receipts/probes-identify.txt` | head: `identify` (third build, `P-EN-IDENTIFY-NOTIFICATION` = 1) | ID build **178/0** |
| `receipts/aecp_notify.log` | head: `make -C tb/aecp_notify` | **30/30** (default 26, identify 4: FT) |
| `receipts/author-arms.txt`, `receipts/author-arms/` | the lane's own driver, `aecp_mutants.py --only` the six new arms, `--jobs 2` | controls `hazards` and `timer-defaults` PASS. **6/6 KILLED**: `td-lock-default-59s` (TD1, got 59,003 ms), `td-tl-default-301s` (TD2, no DEREGISTER, 6 probes answered), `hz-gdi-key-none`, `-held` and `-no-stream` (7 failures each: HZ1, HZ8 x2, HZ13a x2, HZ13c x2; HZ13a shows "refused 0 clocks", R419-2's G1), `hz-gdi-as-barrier` (2: HZ1, HZ13b) |
| `receipts/author-arms-counts.txt` | the three arms whose counts the lane says moved | `hz-stub-restored` **81**, `hz-acmp-reads-as-steps` **27**, `hz-barrier-no-priority` **139**, all KILLED. They equal the README and PR-body records |
| `receipts/probes-r469*.txt`, `probes/*.patch`, `scripts/r469_probes.py` | my own probes (table below) | as below |
| `receipts/docs-*.log` | head: `make links matrix params modmatrix lint` | all rc 0. Links **1,122**, matching the PR's record; 115 REQ rows; parameters 28/28/28; module matrix 94 rows, 0 untested; 41 mermaid and 18 wavedrom blocks |
| `receipts/lint-focused.txt` | `--lint-only` with `lint_hdl.sh`'s flags, top-module `protocol_processor_top`, `KL_aecp_notify` and `KL_pp_scoreboard` | rc 0, 0 findings each |
| `receipts/vivado-evidence-check.txt` | the published OOC 1x1 reports | totals, blob ids, images, chparam, the 8-4445 count and the `(u_pp)` rows (section 5, RTL) |
| `receipts/hosted-checks.txt` | hosted check runs at the exact head | docs-gates and portability success (push and pull_request). `suites` was still in progress when read |
| `receipts/static-checks.txt` | merge check, the lane's RTL diff, reset audit, hazard-field consumers | see sections 4 and 5 |

My probes. Each probe is one patch applied in a scratch copy of the head; the TD probes run `timer-defaults` and the GDI probes run `hazards`.

| Probe | Change | Outcome |
|---|---|---|
| `r469-td-prescaler-150clk` | the wrap's prescaler 1 ms = 150 clk instead of 100; defaults unchanged | **PASS** (60,002 / 300,001 ms). The check measures the top's own ms timebase (`dbg_now_ms_o` = `now_ms_w`), so a prescaler-only change does not trip it |
| `r469-td-keeps-override` | the `ifndef PP_TOP_TIM_DEFAULTS` guard removed, so the 400 ms overrides apply | **KILLED**: TD1 and TD2 |
| `r469-lock-59999` / `-59997` / `-60015` | `LOCK_TIMEOUT_MS_P` default 59,999 / 59,997 / 60,015 | **survive**: measured 60,002 / 60,000 / 60,018 ms, inside [60,000, 60,020] (S1) |
| `r469-tl-299999` / `-300016` | `REG_TL_TIMEOUT_MS_P` default 299,999 / 300,016 | **survive**: 300,001 / 300,018 ms (S1) |
| `r469-gdi-stream-cfg` | GDI classified STREAM_CFG, NONE key | **KILLED**, 7: HZ1, HZ8 x2, HZ13a x2, HZ13c x2 |
| `r469-gdi-lock-op` | GDI classified LOCK_OP | **KILLED**, 1: HZ1, the class pin |

## 3. Findings

### S1 - SUGGESTION - Tests (Conformance noted) - TD grades each default inside a 20 ms window, so a default a few ms off survives

- **Where.** `tb/pp_top/notify_phases.hpp:1620-1710` (`SLACK_MS = 20` at :1624; the TD1 and TD2 bounds `got - cmd_ms >= DEFAULT && <= DEFAULT + 20`), with the arm list at `tb/pp_top/aecp_mutants.py:61-67`.
- **Evidence.**
  - The probes above show that a lock default of 59,997 to 60,015 ms and a registration default of 299,999 to 300,016 ms pass TD.
  - The arm-to-notification latency is deterministic: 3 ms for the lock and 2 ms for the registration.
  - The lane's ±1,000 ms arms are killed. The check is prescaler-independent, which answers the manager's question: it catches a changed default, not a changed prescaler. Every plausible regression of the default is caught, for example a wrong unit, a truncated width, the two constants swapped in the shared adder, or the 400 ms override leaking into the build.
- **Impact.**
  - #81 acceptance 4 ("pinned by a check") is met at 20 ms resolution, not at 1 ms. The docs state the window truthfully (09 §8.3 TD row; README TD).
  - I record this as a SUGGESTION and not a defect: no stated claim is false, and every default change the acceptance targets is killed.
- **Suggested outcome.** Pin the default exactly:
  - tap the registry and lock arm (its `now_ms` and `deadline_w`), as `dbg_ident_gap_*` already does for IDENT-BURST, and assert deadline − arm ms == default;
  - add a ±1 ms arm on each default.
- **Verification.** `r469-lock-59999` and `r469-tl-299999` are killed.

### S2 - SUGGESTION - Docs, Conformance - #84 "What remains" (3), P-EN-PLAIN-IEEE-PROFILE's missing RTL consumer, is not recorded, and closing #84 drops it

- **Where.** `docs/architecture/01_overview.md:193` (F01.5: "selects IEEE ROM columns"), `:197-199`, and `docs/architecture/05_acmp_engine.md:487-488`.
- **Evidence.**
  - No RTL reads the parameter. `hdl/acmp/rom/gen_ltn_rom.py:8-10` says "The plain-IEEE column is ABSENT".
  - F01.5 already marks other names that are not RTL parameters, for example P-EN-MVU-*.
  - Issue #84's "What remains" item (3) asks for exactly this note. It is not one of #84's four frozen acceptance items, and the assignment did not include it, so the lane is not bound to it.
- **Impact.** After "Closes #84", nothing tracks this doc-versus-RTL gap. It is not this lane's change.
- **Suggested outcome.** The manager carries it to the residue checklist or to a follow-up issue: an F01.5 note that P-EN-PLAIN-IEEE-PROFILE has no RTL consumer, as for P-EN-MVU-*.
- **Verification.** F01.5's P-EN-PLAIN-IEEE-PROFILE row states that it has no RTL consumer.

### R1 - RESIDUE - Docs - 09 restates the two F08.1 values the single-source rule keeps in F08.1

- **Where.** `docs/architecture/09_verification.md:254` ("at the top's own defaults, 60,000 and 300,000 ms") and `:272` ("waits out the real 300,000 ms").
- **Authority.** `docs/README.md` §2: "Timing values only in F08.1 … everywhere else references the ID". The rule's three listed exceptions do not cover a test row. Line 201 is earlier precedent.
- **Impact.** Wording only. No measurement, test or claim changes.
- **Exact fix.**
  - `:254`: "at the top's own defaults ([F08.1](08_timing.md#fig-08-constants)), not the 400 ms override …".
  - `:272`: "waits out the real `T-NOTIF-TIMELIMITED`, 30 million clocks".

## 4. Assignment and rulings, item by item

1. **F08.1 (ruling 1).**
   - `08_timing.md:30-32`: T-IDENT-BURST and T-IDENT-REARM are marked landed (owner `KL_aecp_notify`, issue #80, only with P-EN-IDENTIFY-NOTIFICATION = 1). T-CTR-OBSERVE is marked integrator-owned.
   - The cited tests exist and grade those rows, and both pass at this head:
     - `tb/pp_top` ID: 09:295, README :2150-2210, arms `ident_burst_100ms` and `ident_no_rearm`. ID build 178/0.
     - `tb/aecp_notify` FT: README :45-59. FT build 4/4.
   - 09:53's TIM row is narrowed to "every F08.1 row with RTL here".
   - No other file claims T-CTR-OBSERVE is graded. 06 §6.6, the integrator guide :470 and 08 §5 :231/:241 already call it the integrator's.
2. **The defaults.**
   - The sixth build (`Makefile:185-196`, `pp_top_wrap.sv:549-557`) drops only the two overrides and keeps the 1 ms = 100 clk prescaler.
   - TD measures on the top's own ms timebase: 60,003 and 300,002 ms, reproduced.
   - Both default-moving arms are killed. A prescaler-only change passes; leaking the override fails.
   - `make` sums six tallies (`NR != 6`). CI's `run_suites.sh` and the `aecp-mutants` step cover the build and the arms.
   - Resolution limit: S1.
3. **02 §2 rule 5** (`02_interfaces.md:115-124`) states one synchronous active-low `rst_n`.
   - All `always_ff` in `hdl/` are `@(posedge clk_i)`. None names an edge of `rst_n`, and there is no `always @` or `negedge` (`receipts/static-checks.txt`).
   - The holds the rule names exist: `aecp_rx_hold_w = !d3_done_w && …` (`protocol_processor_top.sv:2849`), the listener's four work faces held from reset to the binding walk's end (`KL_pp_acmp_lsn_admit`, top banner :33-34), and `adp_enable_w = entity_enable_i && restore_done_o` (:1902).
   - No other reset wording in docs/architecture is asynchronous.
4. **GET_DYNAMIC_INFO.**
   - **The change.** It is the one case arm at `protocol_processor_top.sv:1645-1646` plus the classifier comment, and nothing else in `hdl/` changed. The batch now takes MAP_CFG with the NONE key `{0x3F, 0}`.
   - **How the scoreboard treats it:**
     - Rule 5 cross-locks it class-wide with every STREAM_CFG (all ACMP listener and talker stream steps).
     - Rule 2 admits it beside RO_SNAPSHOT unless the keys match. No ACMP key has type 0x3F.
     - Rules 3 and 4 (LOCK_OP, MAP_CFG per key) meet only AECP transactions, and the AECP engine is single-issue (`aecp_sb_active_r`).
   - **No other consumer.** `hazard_class` and `hazard_key` are read only by the scoreboard admission mux (`:3572-3576`), so the class has no other effect.
   - **No starvation.** The round-robin pick (`sb_prefer_aecp_r`) gives the GDI the next admission after an ACMP release.
   - **Tests and records.**
     - HZ1 pins the class: 39 rows, and only the GDI row changed.
     - HZ8 is amended for exactly the batch that names no stream.
     - HZ13a/b/c grade R419-2's G0 on the batch, its hold, and running beside a read.
     - The four new arm rows and two more class mutants of mine are killed.
     - Every changed campaign record listed in the PR body reproduces: 177→189, 74→81, 26→27, 127→139, and 5/55→6/61 by construction of the arm list.
     - 03 §6, 08 §4 :197-200, 09 §8.3 and the README match the RTL.
   - **R419-2 F5 is resolved at this head.** HZ13a is G1 inverted, and `hz-gdi-key-none` reproduces G1 ("refused 0 clocks").
5. **Area.** See section 5, RTL.

## 5. Lenses

- **Conformance.**
  - TD grades IEEE §7.4.37.2's 300 s and §7.4.2 / Milan §5.4.2.2's 60 s at the product defaults, with byte-exact notifications.
  - The GDI serialization meets F03.7's RO_SNAPSHOT "blocked vs in-flight write" for GET_STREAM_INFO records, which IEEE §7.4.76.1 treats each as an independent command. 08 §4 :215-217 records the accepted over-serialization's effect on ACMP latency (later than the 50 ms design target, within T-ACMP-CMD).
  - #81 acceptance 1-3 and #84 acceptance 1-3 were met by PR #140, per the rulings. The REGISTRY_OP ruling is stated in the PR body.
  - Notes: S1 and S2.
- **RTL.**
  - The lane's RTL diff is one opcode term and a comment. It adds no register: the `(u_pp)` own row's FF count is 3,167 at base and at head.
  - Focused lint is clean.
  - The merge with #153 is a clean union.
  - **Area.** The published reports reproduce the PR table exactly:

    | Pair | LUT | FF |
    |---|---|---|
    | base 24,930 → head 24,900 | −30 | −4 (25,465 → 25,461) |
    | main 24,130 → merge 24,197 | +67 | +110 (23,418 → 23,528) |

    - All +110 FF sit in `(u_pp)`'s own row: 3,169 → 3,279.
    - The RTL confirms the ruling's attribution. `arm_drain_pick` (:2990-3001) pops face 0 whenever its count is non-zero, so `armq_cnt_r[0]` never exceeds 1. Entries 1-3 (3 × 36 bits) and two count bits are dead: 110 FF.
    - The merge log lacks the constant-propagation lines on `armq_r_reg` that the other three logs carry. The finer per-register attribution cannot be seen in the published reports (section 6).
    - The four runs share the same images and chparam, and each log has exactly one Synth 8-4445 match.
- **Robustness.**
  - The batch cannot deadlock. Each engine holds at most one admission, and holds are taken atomically.
  - The batch cannot starve, because of the round-robin.
  - A GDI past its budget is still preempted. DL4 passes: DL 64/0.
  - ACMP reads are unaffected: TB5 172/154 clocks, unchanged.
  - TD's monitor answering isolates the timer under test. With the monitor it gets 6 probes; with the override leaking it fails.
- **Tests.**
  - The changed sections, controls and every new arm reproduce, as do the three moved arm counts.
  - My probes kill the class mutations and confirm the prescaler independence.
  - Note: S1.
- **Docs.**
  - The 02, 03, 08 and 09 hunks and the README records are accurate against the RTL and the runs.
  - Every PR-body line citation I checked resolves.
  - The docs gates are green.
  - Notes: R1 (residue) and S2.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #81/#84 acceptance and rulings; F08.1, 08 §4, F03.7 and 03 §6; TD1/TD2; HZ13; IEEE §7.4.2, §7.4.37.2 and §7.4.76.1; Milan §5.4.2.2 and §5.4.2.10 (in-tree quotations) | R469-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| RTL | CLEAN | `protocol_processor_top.sv` classifier, admission mux, armq; `KL_pp_scoreboard.sv` rules; `KL_aecp_notify.sv` deadline adder; reset audit; focused lint; merge-tree and patch-id; published OOC 1x1 reports (four runs) | R469-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Robustness | CLEAN | admission fairness and deadlock analysis; DL 64/0; TB 56/0 (TB5); TD monitor isolation; override-leak and prescaler probes | R469-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Tests | CLEAN | `tb/pp_top` sections HZ (head 189, base 177), TD, DL, TB, ID; `tb/aecp_notify` 30/30; the lane's six new arms and three count-moved arms with controls; reviewer probes (9 runs) | R469-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |
| Docs | CLEAN | 02 §2 rule 5; 03 §6; 08 F08.1 and §4; 09 TIM row and §8.3; `tb/pp_top` README; PR body; docs gates (links 1,122) | R469-1 | db2c4eb823c47b2607fb52234b58ac6b93ff548b |

## 6. Real limits

- **Not run here, by the rules of this review:**
  - the full `run_suites.sh` sweep;
  - all six `tb/pp_top` builds together, and the full 61-arm AECP campaign, `notify_mutants.py` and the other campaigns;
  - Yosys, the builder and the parent banks;
  - Vivado.

  I ran the sections and arms this lane touches (section 2). The manager's bank results at this head are taken as reported, not reproduced.
- **Area provenance.** Area is judged from the published reports. They carry no processor commit id, so binding each run label to its commit rests on the author's statement. The images and chparam are identical across the four runs. The finer face-0 attribution, entries 1-3, is not visible in the published logs. I confirmed it by RTL analysis and by the `(u_pp)` own-row delta.
- **Hosted CI.** The `suites` job at the exact head was still in progress when read. Only docs-gates and portability had completed (success).
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **PR #153.** Its content arrives through the merge of `main`, where it was reviewed in its own lane. Here it was checked only for a clean merge, `tb/aecp_notify` 30/30 and the TD run through the registry.

## 7. Pending manager duties

- The final current-dev candidate at the merge turn: source base `83999eba`, live dev `fea346e7`.
- The parent consumer set of 17 at dev `fea346e7`, with the c8, p2-p1, c10 and 232 patches. The author ran it at `241f9184`, where gate 16's T30 failure belongs to #643; #648 is merged at `fea346e7`, so gate 16 is expected to change there.
- The hosted `suites` result at the exact head.
- Carry S2 to the residue checklist or a follow-up issue before closing #84. Carry R1 to the residue checklist. Decide whether to take S1.
- The merge needs two independent positive reviews and the full completion bar.

R469-1 FINISHED
