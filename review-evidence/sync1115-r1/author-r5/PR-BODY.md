[A787]

Sync dev `6b66f66d` into dev-soft-core under the owner's 2026-10-26 branch policy: dev remains the all-fabric line; dev-soft-core takes its merged work until the flip. Includes the ruled merge of dev-soft-core `70f4056f` (#901), participant-owned LeaveAll grading requested by PR #934's external review, the lateness of a build that sends nothing timed from its timer's owner's transmit opportunity, requested by its internal review, and every MRP timer's expiry with no recorded owner failing the run, as ruled.

## Contents

- **[Status](#status)**: what stays open, and `sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, executor and reviewers.
- **[Description](#description)**: both merges, their conflicts and resolution, the commits after them, the harness change, the gPTP items, the ledger and the figures.
- **[Authoritative references](#authoritative-references)**: the branch policy, the rulings and both sides' merged PRs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and its dependencies.
- **[How to validate](#how-to-validate)**: the gate set and the expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what a sync does not do, and what it found.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

Rounds 5 and 5b at local head `e2be92b0` (round 5 `ccc98b11`, on round 4's `c10c549e`); nothing pushed this round. [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6942387001), covering rounds 4 and 5, for independent re-review of R854-001 and of R853-1's F1 and F2 ([PR #934 issuecomment-6938623769](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6938623769)); composed-head acceptance remains pending.

- **R853-1 F1** is R854-001, fixed in round 4 (`c10c549e`). The reviewer's case B fails on if0 MSRP, skipped at its 1,180 ms opportunity, at round 4's grader and at this head, once the probe's timer entries carry the owners the testbench records. Round 5 adds case B as a self-test arm, which the earlier-rule mutant fails.
- **R853-1 F2** is fixed in `ccc98b11`. A build that sends nothing is late past 49 ms after its timer's owner's first transmit opportunity, derived from the posted TICKs and the owner recorded at the expiry. It is never measured from a join timer's callback, nor from another participant's opportunity. The reviewer's C0 and C both fail as late (59.979 ms). A self-test arm and a mutant hold it.
- **Round 5b, `e2be92b0`, as ruled:** an MRP timer's expiry with no recorded owner fails the run by name, "(owner unresolved)", as an unowned LeaveAll does. No fallback stands in. A self-test arm and two mutants hold it: the fallback restored, and an unowned run-out not failing.
- The harness self-test passes: 879 checks, 261 mutants caught. The docs jobs: 63 steps rc 0 and 34 NOT RUN with reasons, 0 bad.
- Round 4's thirteen re-simulated legs, regraded at `e2be92b0`: every table is byte-identical to round 4's, and each rc is round 4's. All 1,871 MRP run-outs in the 26 traces have their owner recorded; none is unowned. All 44 owned LeaveAlls of the eleven 8x8/1if phases are sent, and the 1x1/1if valid-destinations leg passes. Round 2's owner-less logs now fail, as expected: all 4,122 of their run-outs are unowned.
- The 305 us paced SET_CONFIGURATION and CTRL_LOOP_TX_MS 35 remain #898's; neither constant changes here. The 8x8 STATED cost findings remain #914's.
- Every recorded route meets #818's floor on its best directive: +0.030 ns setup and 0 ns hold at every corner.

`sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`. Incorporated base: `70f4056f`.

## Linked Issue / roles

Relates to #665

Executor: `[A787]`
Internal cleared-context reviewer: `[R853]` (R853-1 NEGATIVE at `6ceed753`; F1 fixed in round 4, F2 in round 5, the fallback ruled out in round 5b; awaiting independent re-review)
External reviewer: `[R854]` (R854-1 NEGATIVE at `6ceed753`; R854-001 fixed in round 4, awaiting independent re-review)

## Description

Two `--no-ff` merges, each followed by one commit per semantic conflict found and per regeneration:
- dev `6b66f66d` (merge base `1f29f189`, the #830 sync) into dev-soft-core `659d7687`. It carries only work already merged on dev under the full bar: #828, #831, #836, #815, #834, #841 (#839), #842 (#840), #849, #847 (#845), #846 (#843), #852 (#851), #825, #835, #862, #875, #893 (#883) and #913.
- dev-soft-core `70f4056f` (#901, SRP's Talker declarations, #895), as round 2's ruling asks.

**The merge of dev, `62625941`.** Ten files conflicted, in 13 hunks. Both sides are kept in each.

| File | Resolution |
|---|---|
| `docs/design/MAILBOX_SPLIT.md` | dev's sentence-per-line status block, with this line's S1 and S6 sentences in that form |
| `docs/design/MARK_II_AREA_PLAN.md` | dev's Mark II summary, plus one bullet for the measured integrated split route (M8a-2) |
| `docs/reference/FR_NFR.md` | NFR-SCOUT-01: this line's RV32IM and caches, plus dev's "(firmware only after the switch-over)". NFR-SCOUT-02: dev's. NFR-SCOUT-03: this line's approved T_svc = 20 ms, with dev's split of the audio and gPTP sentence |
| `sw/builder/endstation_builder.py` | both keys of `build()`'s result: `nvm_split` and `warnings` |
| `tb/verilator/milan_dp/Makefile` | both cases, `split` and `bootsa`, and the union of `clean` |
| `tb/verilator/milan_dp/README.md` | both sides' contents entries and sections |
| `docs/diagrams/submodule_boundaries.*`, `PNG_MANIFEST.json` | through `submodule_boundaries.gen.py`, from the merged gitlinks |
| `docs/diagrams/flash_layout.png` | rendered from the merged SVG with the generator's documented `rsvg-convert -w 1800`, which reproduces both parents' PNGs byte for byte |

**Pins.** gptp-processor `1616fc8f` and protocol-processor `801ef228` follow dev; each is a fast-forward of the old pin. tsn-c-stack stays at this line's `715589c1` (#892), which descends from dev's `70936b77`. No other submodule moved, and the merge of `70f4056f` moves none.

**After it**, one commit each:

| Commit | What |
|---|---|
| `a563a83d` | Semantic conflict. dev's #839 gates the control lane through `pp_txs_*`, and the split's `KL_ctrl_split` still drove `pp_tx_tvalid_w`, so the split build refused (`%Error-UNDRIVEN: ... 'pp_txs_tvalid_w'`). The split now binds the gated handshake, as the all-fabric wrapper does. The split firmware writes both station MAC halves before it enables any CSR-addressed transmitter (`ctrl_plat_csr.c:38-39`). |
| `dfcd8eed` | Semantic conflict. The split leg's `[TX]` frame then waited for a MAC the bench never wrote. The bench writes it as the platform does, and `[TX]` checks the hold, before the MAC is written and with its low half alone. `split_mutants.py` plants the lane taken past the gate and the gate opened by one half; 28 of 28 are caught. |
| `b84d095a`, `d2da3159` | Semantic conflict. dev's area plan said #810 is not merged and linked this line's FR_NFR as proposing 10 ms. On this line #810 merged on 2026-11-13 and 20 ms is approved. |
| `d8c8c4b7`, `1facd42e` | Semantic conflict. The two-placement stimulus and its rows held the shipping config's pre-#840 identity, so at the merge neither half answered AECP. They take 02:4B:4C:4B:4C:01. lwSRP seeds its LeaveAll draws from the MAC (`srp_mbx.c`, `mrp_port_configure`), which moves one count and one plant's timestamp. |
| `3c94c76c` | Semantic conflict. Processor `801ef228` (#893) fixes the fabric's #857, #858 and #860, so the twin's four owed rows reported "the defect has gone". They are deleted with their six plants. |
| `3a5ba178`, `f5750b3d` | Restatement and regeneration: section 5's images, and `docs/DOCUMENTATION_AUDIT.md`. |

**The merge of dev-soft-core `70f4056f`, `10b2fe21`.** Two files conflicted, both documentation. Both sides are kept:

| File | Resolution |
|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md` | section 5: dev-soft-core's rewrite whole, plus this line's sentence on the sync's delta (its figures restated in `30c5d3d6`) |
| `tb/verilator/milan_dp/README.md` | the contents list: the split (twenty-eight plants) and twin (fourteen plants) lines and #901's srptx line |

No code conflicted. #901 changes no RTL.

| Commit | What |
|---|---|
| `30c5d3d6` | Restatement. Section 5's sync sentence at the merge: 32 to 40 B more `rom` than `70f4056f` at each point, no tile moved. |
| `4cb7d7ab` | Regeneration. `docs/DOCUMENTATION_AUDIT.md`, through `docs_inventory.py --write` (two rows: the budget harness's and milan_dp's READMEs). |
| `9715a30a` | Semantic conflict of the dev merge, found by the sweep. dev's newer reads in the `pp_shadow` bench (#862's drop probes) and in `milan_dp`'s bootsa bench address KL_pp_shadow at dev's flat path. On this line the wrapper sits in `generate if (CTRL_SPLIT_P == 0) begin : g_af_pp`, so both benches failed to compile. The five reads take the `g_af_pp` path, as the bench's other nine already did. `pp_shadow` passes; bootsa 67 of 67. |
| `6ceed753` | Round 3: time THE TRANSMIT's row from the participant's transmit opportunity and check the first opportunity. |
| `c10c549e` | Round 4: record the expiry's participant independently of output, use it throughout LeaveAll grading, and add owner controls and mutants for R854-001. |
| `ccc98b11` | Round 5: time a build that sends nothing from its timer's recorded owner's transmit opportunity, never another participant's join callback (R853-1 F2); case B of R853-1 F1 as a self-test arm. |
| `e2be92b0` | Round 5b: fail an MRP timer's run-out whose owner the testbench did not record at the expiry, with no other participant's opportunity standing in, as ruled. |

**THE TRANSMIT's grading, `6ceed753`, `c10c549e`, `ccc98b11` and `e2be92b0`.** Q1 of #665 issuecomment-6930885185 times the row from the participant's transmit opportunity (IEEE 802.1Q-2018 10.7.4.1). The first implementation inferred the owner from whichever future LeaveAll arrived first; R854-001 demonstrated that overlapping MSRP and MVRP timers could hide a skipped opportunity. Round 4 replaces that association:

| Artifact | Final behavior |
|---|---|
| `sim_main.cpp:335`, `:422`, `:444`; `observe.vlt:43`; `observers.py:30` | Observe the callback argument at expiry. Bind its timer argument to application at creation and interface at the adapter's Domain publication. Each timer ENTRY records `if<n> MSRP` or `MVRP`, or explicitly unresolved. PARTICIPANT records expose the binding. No firmware hook or product change is needed. |
| `grade.py:166`; `mrpdu_grade.py:243`, `:249`, `:281` | Use the recorded owner for its opportunity, first MRPDU, LeaveAll, missing/late output and service row. Another participant's frame cannot answer it. |
| `join_grade.py:85`; `run.py:186` | Count and name skipped, late, absent and unowned expiries; each fails the run. A log ending before the opportunity and bound reports unresolved and proves nothing for that expiry. |
| `selftest_leaveall.py:151`, `:199`; `selftest_mutants.py:881` | Cover overlapping timers, clean reordered output, both applications and interfaces, skipped/late/absent output and missing/unresolved owner records. Keep the earlier single-participant controls and eight mutants; add four owner mutants. |
| Harness README and `FR_NFR.md` 3.4.1 | State exactly what the grader proves at commit, how the opportunity is derived, and the unresolved and wire-timing limits. |

The supplied overlap now fails on **if0 MSRP**, its original **1,180 ms** opportunity: its 1,181 ms MRPDU omits LeaveAll and its LeaveAll comes at 1,371 ms, **191 ms** later. MVRP's valid LeaveAll at 1,221 ms answers only MVRP. The matching clean overlap and legitimately reordered clean case pass. Restoring the old association is caught by the overlap control itself.

**A build that sends nothing, `ccc98b11`** ([R853-1 F2](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6938623769)). A run-out whose first build sends nothing was late only past 49 ms after the last `on_join_timer` callback between them, of any participant. So another participant's join callback could restart the count: the reviewer's case C passed a build 60 ms after its run-out.

| Artifact | Final behavior |
|---|---|
| `mrpdu_grade.py` `resolve`, `anchor`, `recorded_owner` | That build's lateness counts from its timer's owner's first transmit opportunity: the owner the testbench recorded at the expiry, the opportunity as `opportunity()` derives it from the posted TICKs. Never from a join callback, nor from another participant's opportunity. A frame's lateness is unchanged. |
| `join_grade.py` `held` | A late build that sends nothing is named from that anchor. |
| `selftest_leaveall.py` `anchor_checks`; `selftest_mutants.py` | Case B of F1, and an arm holding the anchor: the reviewer's C0 and C late at 59.979 ms; another participant's running join timer late; the owner's own running one holding. The mutant: the anchor from any join callback (the earlier rule). |
| Harness README and `FR_NFR.md` 3.4.1 | State that for every MRP timer's expiry the testbench recorded its owner, and where its first build sends nothing, that build runs within 49 ms of the owner's first transmit opportunity. |

**An expiry with no recorded owner, `e2be92b0`** (the manager's ruling on round 5's open question, #665). Round 5 timed an owner-less build that sends nothing from the latest of the log's participants' opportunities, which could lie up to a JoinTime after the run-out.

| Artifact | Final behavior |
|---|---|
| `mrpdu_grade.py` `resolve`, `anchor` | Every MRP timer's run-out, a join, periodic or LeaveAll timer's, whose owner the testbench did not record at the expiry, or recorded unresolved, is `unowned` whatever its builds sent. `unowned` is in `FAILING`. Its frames are still its builds' (`released`). The fallback is removed. |
| `join_grade.py` `held`; `run.py` `run_out_miss` | An unowned run-out is named "(owner unresolved)", with whether its owner was recorded unresolved or not at all, and fails the run. |
| `selftest_leaveall.py` `unowned_checks`; `selftest_mutants.py` | No owner with an empty build; no owner while another participant's join timer runs, where the fallback held the build; the owner recorded unresolved with an on-time frame, whose join interval is still graded. Two mutants: the fallback restored, and an unowned run-out not failing. `selftest_polls` and `selftest_notice` give their synthetic timers owners, as the testbench writes them. |
| Harness README and `FR_NFR.md` 3.4.1 | State that an expiry with no recorded owner fails the run. |

The service-row budget remains 20 ms and THE TRANSMIT's conformance bound remains **49 ms**. Firmware, product RTL, testbench, configuration and pins are unchanged by rounds 5 and 5b; firmware, product RTL, configuration and pins by rounds 3 to 5b.

**The gPTP items and the identity on the split images.** The split keeps the fabric gPTP plane until #665 F6 (`milan_datapath.sv`, on `GPTP_PLANE_EN_P` alone). Its ROM is the builder's, from the config. The merge of `70f4056f` touches neither the configs, nor the builder, nor the pins.
- **clockAccuracy 0x22** (IEEE 802.1AS-2011 8.6.2.3) reaches the split images through both AX7101 configs. It goes to the engine ROM as `--clock-accuracy 0x22`, and to the AEM's AVB_INTERFACE as `clock_accuracy` 0x22, which the split firmware serves.
- **The three engine fixes** come with gptp-processor `1616fc8f`: the Announce at the timeout instant (10.3.9.1), the unknown first Follow_Up TLV (11.4.1) and the late Pdelay response (Milan v1.2 4.2.6.2.6).
- **The identity 02:4B:4C:4B:4C:01** (#840) reaches the entity ID, the AEM, the firmware's generated constants, the station-MAC CSR writes and the engine ROM's `--mac`.
- **#840's 1000BASE-T-only advertisement does not reach the split.** It lives in the release firmware's PHY init, and the split firmware has no MDIO path. #919 takes it (#919 issuecomment-6907491954).

**The ledger.** #847, #852 and #893 fixed the fabric processor. Each has a split counterpart:

| Fix | Split counterpart | Test |
|---|---|---|
| #847 (#845): a Talker registered before the settle, and the registrars on a link change | `srp_mbx.c:618`, `:829`, `:997`, `:1045` | `Srp.HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep`, mutant `binding-change-not-copied` |
| #852 (#851): one vector per value per MRPDU | lwSRP `mrp_mad.c:1351`, `:1410` | srptx `[WIRE]`, plant `doubled-declaration` |
| #893 (#857): LeaveAll with nothing declared | lwSRP `mrp_mad.c:779` | the twin's LeaveAll grade |
| #893 (#860): New twice, and JoinIn only when IN | lwSRP `mrp_mad.c:149`, `:1278` | the twin's Table 10-3 grade and its plants |
| #893 (#858): ENTITY `available_index` | `ctrl_app_aecp.c:113` | `App.EntityReadSeesTheLastAdvertisedIndex`, two mutants |

**Figures and their source heads.** Rounds 3 to 5 change harness observation/grading and documentation only; image and earlier full-gate measurements retain their recorded source heads.
- **ROM per split image:** each grows 32 to 40 B over `70f4056f`, and none leaves its banks, its tiles or its ledger. The 8x8/1if platform plans 56.0 with 848 B to spare, so the BRAM rule (#923) adds no debt.
- **CPU service-budget harness at 1x1/1if:** arm A's 96 groups have 0, 0, 0 and 7 misses by quarter, the 7 being the ruled held-egress rows. The answering-every-port arm and the answering-ports leg pass. The flip and load checks pass (load 0.517 and 0.514 against 0.70). **#901's valid-destinations leg passes** (round 2: a late LeaveAll; rerun at `c10c549e`, regraded at `e2be92b0`). `record_classes.py` refuses the paced class's SET_CONFIGURATION, 305 us by the rule against its stated 300 us; #898 restates it (Q2).
- **At 8x8/1if:** arm A's four parts and the legs as at round 2, but for the MRPDU rows. Parts 1 and 2's `mrpdu.leaveall.if0` is 0.557 and 0.506 ms (round 2: 160.6), with 0 misses. The `STATED` lines remain, the point being held to 1x1/1if's stated costs (#914's scope).
- **The eleven LeaveAll phases at 8x8/1if, rerun with recorded owners:** all 44 LeaveAlls in the 22 save-held/save-starved groups meet the first-opportunity check; zero skipped, late, absent, unresolved or unowned expiries. Every probe row is within its bound. Worst MRPDU rows: LeaveAll 1.64360 ms (seed 12102, save-starved), periodic 2.96879 ms (seed 13602, save-starved), join 1.86217 ms (seed 10592, save-held), against the unchanged 20 ms. The 49 ms conformance bound is unchanged. Each phase leg retains rc 1 on its two #914 polls-base cost statements; these are not passing whole legs. Seed changes are harness-only experiments. The seed clones have the exact head's harness and unchanged product sources except the experiment MAC; all thirteen rebuilt firmware ELFs match their respective earlier images byte for byte. Across all 26 rerun groups, every trace line other than the new ownership records equals the earlier execution. This new ownership evidence supersedes round 3's unsupported participant-association conclusion. **Regraded at `e2be92b0`:** every leg's table is byte-identical to round 4's, and every group's rows, run-outs and LeaveAlls are the same. All 1,871 MRP run-outs in the 26 traces have their owner recorded. 769 are builds that send nothing; the owner's anchor moves 334 of them earlier by at most 5 us and changes no outcome. The latest such build runs 0.832 ms after its owner's opportunity, against 49 ms.
- **The additional 8x8/1if valid-destinations run:** rc 1 on the previously recorded #914 build/slice cost statements, while both LeaveAlls are sent and no service-row miss occurs. This is not a passing whole-leg result.
- **Routes against #818's floor** (+0.030 ns setup and 0 ns hold at every corner, on the best of three directives; issuecomment-6930885185, Q3):
  - split 1x1/1if meets on all three directives, best ExtraTimingOpt at +0.196 / +0.036 ns;
  - split 8x8/1if meets on AltSpreadLogic_high at +0.140 / +0.036 ns. ExtraTimingOpt (+0.014) and the recipe's directive (-0.595) miss setup;
  - release AX7101 1x1 meets on all three, best AltSpreadLogic_high at +0.209 / +0.016 ns. Its export comparison with round 1 and dev `6b66f66d` holds after path/generation normalization and exclusion of comment-only hierarchy ordering; this is not raw export or bitstream identity;
  - round 1's six routes meet the same way.

## Authoritative references

- The owner branch policy (2026-10-26), recorded on #665.
- The ruling on #665 on the S12b rehearsal's findings and its gPTP group, item 3; the ruling on this sync's first STOP (#665 issuecomment-6907491626); the rulings on its round-2 REVIEW READY (#665 issuecomment-6930885185: Q1, Q2 with #898 and #897 issuecomment-6928240632, Q3 with #818); the BRAM rule (#923 issuecomment-6906679024); #919 issuecomment-6907491954.
- The previous sync, #830; PR #934 issuecomment-6932841237 (R854-001) and issuecomment-6938623769 (R853-1, F1 and F2).
- dev's #846 (#843): IEEE 802.1AS-2011 8.6.2.3, 10.3.9.1, 11.4.1; Milan v1.2 4.2.6.2.6. dev's #842 (#840), #841 (#839), #847 (#845), #852 (#851), #893 (#883: #857, #858, #860). dev-soft-core's #901 (#895).
- IEEE 802.1Q-2018 Table 10-3, 10.7.4, 10.7.4.1, 10.7.9; IEEE 1722.1-2021 Table 7-2, 6.2.2.15.
- `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (sections 5 and 13), `docs/reference/FR_NFR.md` (NFR-SCOUT-01 to -03, 3.4.1), `tb/verilator/milan_dp/README.md`, `tb/verilator/ctrl_service_budget/README.md`.

## How to get into the same state

```sh
git fetch origin
git switch --detach e2be92b0
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

Use the pinned build environment defined by `.github/workflows/rtl-fast.yml`, `.github/workflows/docs.yml`, `scripts/ci_rv32_sdk.py` and `sw/litex/litex_pins.txt`.

## How to validate

```sh
make -C tb/verilator/milan_dp split split-mutants twin twin-plants srptx
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant valid-destinations --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings --groups save-held,save-starved
python3 -I tb/verilator/ctrl_service_budget/record_classes.py <each leg's results directory>
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 scripts/docs_inventory.py --check
bash scripts/run_all_suites.sh <logdir> --wait --shard k/4   # k = 0 to 3
```

Also every step of the four workflows. Expected at this head:
- At `e2be92b0`: harness self-test rc 0, 879 checks and 261 mutants caught; docs jobs, 63 steps rc 0 and 34 NOT RUN with reasons, 0 bad. R853-1's probe: case B fails on if0 MSRP (owned); C0 and C fail as late (owned) or as unowned (as written). Round 4's thirteen legs regrade with byte-identical tables and no unowned run-out. Round-5 receipts contain the commands, logs, rc files and large-log digests for `ccc98b11` and `e2be92b0`; round 4's contain the reruns, the supplemental 24-case owner matrix and the earlier evidence copied under `receipts/carried/` at its recorded source heads.
- Earlier full workflow evidence stays at `9715a30a`: 154 steps rc 0, 256 NOT RUN with reasons. The four-shard sweep is 62 passing suites at `4cb7d7ab` plus the three corrected/repeated suites at `9715a30a`; the interrupted or failed attempts are not passes. Round 4 does not rerun that unrelated bank.
- The combined earlier sweep evidence supports all 65 suites. The earlier publication census is 6 shapes, 0 of 163 arms failed.
- `split`: 84 checks, 0 failures. `split-mutants`: 28 of 28.
- `twin` and `twin-plants` fail, as at `70f4056f` (#929).
- `srptx` fails as at `70f4056f` (#916).
- The flip and load checks pass. The 1x1 arm A has 7 misses, all `backlog-owed`'s held-egress rows. The valid-destinations arm passes.
- The eleven 8x8-1if phases have 44 owned LeaveAlls sent, no failed first-opportunity check, no late, absent or unowned run-out and no probe-row miss, regraded at `e2be92b0`. Each phase leg retains rc 1 on its two existing #914 `STATED` polls-base lines; the additional 8x8 valid-destinations leg retains rc 1 on nineteen build/slice statements. These remain open whole-leg failures.
- `record_classes.py` refuses the 1x1/1if paced record until #898's restatement (Q2).

## Known limitations / out of scope

- **The paced record at 1x1/1if (Q2).**
  - The merged image's accepted SET_CONFIGURATION is 28,700 cycles, 305 us by the rule, against `edit_rows.PACED`'s 300 us.
  - #898 round 7 restates it to 305 us, with `CTRL_LOOP_TX_MS` 35 at 1x1/1if, by the rule (#897 issuecomment-6928240632). #898 lands before this sync, and the sync regrades on its merge.
  - Neither constant changes here.
- **The twin, as at `70f4056f`.** #901 makes the split declare Talker Advertise once its destination is valid, so the twin's owed row `split-talker-failed` (the split's Talker Failed) no longer holds. Plant `srp-plus-k` names "Talker Failed" and escapes. Both fail identically on dev-soft-core `70f4056f`; #929 takes the row. The twin is not a CI gate, and the fix is not this sync's.
- **`make srptx` fails as at `70f4056f`**, on one finding kind (`[TIME]`). Its JoinTime is 20 cs against the adapter's 19 cs (#916).
- **#840's 1000BASE-T-only advertisement is not on the split.** #919 takes it.
- **The 8x8/1if split image's timing margin is thinner than at #810** (+0.140 on its best directive, AltSpreadLogic_high, against #810's +0.292 on ExtraTimingOpt at `084cf7a8`), on the EDIT window's path into the audio map's output claim. It meets #818's floor. #927 adds setup margin after the flip.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
