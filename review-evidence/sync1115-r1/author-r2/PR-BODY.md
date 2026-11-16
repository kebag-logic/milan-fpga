[A787] Sync dev `6b66f66d` into dev-soft-core (owner branch policy, 2026-10-26: dev stays the all-fabric line, and dev-soft-core takes dev's merged work until the flip), as ruled in item 3 of the ruling on #665 on the S12b rehearsal's gPTP group, with dev-soft-core's `70f4056f` (#901) merged in as round 2 of the sync was ruled.

## Contents

- **[Status](#status)**: the open decisions, and `sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, executor and reviewers.
- **[Description](#description)**: both merges, their conflicts and resolution, the commits after them, the gPTP items, the ledger and the figures.
- **[Authoritative references](#authoritative-references)**: the branch policy, the rulings and both sides' merged PRs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and its dependencies.
- **[How to validate](#how-to-validate)**: the gate set and the expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what a sync does not do, and what it found.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

REVIEW READY posted on #665 (round 2). Three questions are open, and each blocks the merge but not the review:
- THE TRANSMIT's MRPDU rows wait for lwSRP's join timer, which the ruling's remedy does not reach. They miss at most LeaveAll phases at 8x8/1if, and #901's valid-destinations arm misses at 1x1/1if.
- The paced record class at 1x1/1if is 5 us over its statement after the composition.
- The release image's fast-corner hold is under +0.030.

`sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`. Head `9715a30a`. Base: `dev-soft-core` `70f4056f`.

## Linked Issue / roles

Relates to #665

Executor: `[A787]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

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

**Figures at the head.**
- **ROM per split image:** each grows 32 to 40 B over `70f4056f`, and none leaves its banks, its tiles or its ledger. The 8x8/1if platform plans 56.0 with 848 B to spare, so the BRAM rule (#923) adds no debt.
- **CPU service-budget harness at 1x1/1if:** arm A's 96 groups have 0, 0, 0 and 7 misses by quarter, the 7 being the ruled held-egress rows. The answering-every-port arm and the answering-ports leg pass. The flip and load checks pass (load 0.517 and 0.514 against 0.70).
  - **Fails:** #901's valid-destinations arm exits 1 on a late LeaveAll (see Status).
  - **Fails:** `record_classes.py` refuses the paced class: an accepted SET_CONFIGURATION is 28,700 cycles, 305 us by the rule, against its stated 300 us. #901's head measured 28,288.
- **At 8x8/1if:** arm A's parts 0 and 3 are as at round 1, part 3 now rc 0. Parts 1 and 2 each have `mrpdu.leaveall.if0` at 160.6 ms, at the product MAC's LeaveAll phase.
- **The LeaveAll phase spread at 8x8/1if** (ruling items 2 and 3): eleven phases. On the sync alone 9 miss, the worst 160.6 ms. On the trial merge with #914's `d539f162` 7 miss, the worst 160.6 ms, and its rows equal the sync's within 0.4 ms at every phase.
- **Split 1x1/1if route:** all three directives meet +0.030 ns. The best is ExtraTimingOpt, +0.196 / +0.036 ns.
- **Split 8x8/1if route:** the best of three, AltSpreadLogic_high, meets at +0.140 / +0.036 ns. ExtraTimingOpt (+0.014) and the recipe's directive (-0.595, 307 failing) do not. All three equal round 1's routes, figure for figure.
- **Release AX7101 1x1 route:** setup meets at all three directives, the best AltSpreadLogic_high at +0.209 ns. Fast-corner hold is +0.014 to +0.016 ns at all three, over the build gate's 0 and under +0.030. Its gateware export equals round 1's, which equals dev `6b66f66d`'s file for file.

## Authoritative references

- The owner branch policy (2026-10-26), recorded on #665.
- The ruling on #665 on the S12b rehearsal's findings and its gPTP group, item 3; the ruling on this sync's first STOP (#665 issuecomment-6907491626); the BRAM rule (#923 issuecomment-6906679024); #919 issuecomment-6907491954.
- The previous sync, #830.
- dev's #846 (#843): IEEE 802.1AS-2011 8.6.2.3, 10.3.9.1, 11.4.1; Milan v1.2 4.2.6.2.6. dev's #842 (#840), #841 (#839), #847 (#845), #852 (#851), #893 (#883: #857, #858, #860). dev-soft-core's #901 (#895).
- IEEE 802.1Q-2018 Table 10-3, 10.7.4, 10.7.9; IEEE 1722.1-2021 Table 7-2, 6.2.2.15.
- `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (sections 5 and 13), `docs/reference/FR_NFR.md` (NFR-SCOUT-01 to -03, 3.4.1), `tb/verilator/milan_dp/README.md`, `tb/verilator/ctrl_service_budget/README.md`.

## How to get into the same state

```sh
git fetch origin
git switch --detach 9715a30a
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

The pinned tools are those of `rtl-fast.yml` and `docs.yml`: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, and the RV32 SDK of `scripts/ci_rv32_sdk.py`. The LiteX legs and the CPU budget harness use the LiteX revisions of `sw/litex/litex_pins.txt`.

## How to validate

```sh
make -C tb/verilator/milan_dp split split-mutants twin twin-plants srptx
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant valid-destinations --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings --groups save-held,save-starved
python3 -I tb/verilator/ctrl_service_budget/record_classes.py <each leg's results directory>
python3 scripts/docs_inventory.py --check
bash scripts/run_all_suites.sh <logdir> --wait --shard k/4   # k = 0 to 3
```

Also every step of the four workflows. Expected at this head:
- Every step of the four workflows rc 0 or not run with its reason (154 and 256). The publication census: 6 shapes, 0 of 163 arms failed. All 65 suites of the sweep pass.
- `split`: 84 checks, 0 failures. `split-mutants`: 28 of 28.
- `twin` and `twin-plants` fail, as at `70f4056f`: the owed row `split-talker-failed` no longer holds, and plant `srp-plus-k` escapes (Known limitations).
- `srptx` fails as at `70f4056f` (#916).
- The flip and load checks pass. The 1x1 arm A has 7 misses, all `backlog-owed`'s held-egress rows.
- The valid-destinations arm exits 1, and `record_classes.py` refuses one 1x1/1if paced record: the open decisions.
- The 8x8-1if `save-held` has `mrpdu.leaveall.if0` 160.6 ms: the open miss.

## Known limitations / out of scope

- **THE TRANSMIT's MRPDU rows and lwSRP's join timer (open; decision asked).** In every late MRPDU at both points, the frame goes 0.44 to 1.56 ms after its participant's next join-timer run-out, and that run-out is 189.1 to 189.6 ms after the participant's previous build, one JoinTime. `mrp_transmit` sends nothing while `join_wait` is set (lwSRP `mrp_mad.c:1421`). Each transmission sets it for `join_cs`, 19 cs (`:1539-1540`). The CPU is busy for 12 to 22 % of the wait (97 to 99 % under the flood). THE TRANSMIT's builds are about 31,500 cycles, inside the slice. The misses therefore follow the MAC-seeded phase, not the CPU budget, and #914's composition does not move them.
- **The paced record at 1x1/1if (open; decision asked).** The merged image's accepted SET_CONFIGURATION is 129 cycles past what 300 us holds. Restating it to 305 us by the rule takes the model's tx row to 34.02 ms, past `CTRL_LOOP_TX_MS`'s 34. That is a firmware constant, and its change is not this sync's to make.
- **The twin, as at `70f4056f`.** #901 makes the split declare Talker Advertise once its destination is valid, so the twin's owed row `split-talker-failed` (the split's Talker Failed) no longer holds. Plant `srp-plus-k` names "Talker Failed" and escapes. Both fail identically on dev-soft-core `70f4056f`; #929 takes the row. The twin is not a CI gate, and the fix is not this sync's.
- **`make srptx` fails as at `70f4056f`**, on one finding kind (`[TIME]`). Its JoinTime is 20 cs against the adapter's 19 cs (#916).
- **#840's 1000BASE-T-only advertisement is not on the split.** #919 takes it.
- **The 8x8/1if split image's timing margin is thinner than at #810** (+0.140 on its best directive, AltSpreadLogic_high, against #810's +0.292 on ExtraTimingOpt at `084cf7a8`), on the EDIT window's path into the audio map's output claim. It meets the floor (the ruling on #665, issuecomment-6907491626); #927 takes the thin margin.
- **The release image's fast-corner hold is +0.014 to +0.016 ns at every directive**, under the +0.030 floor. The worst paths are inside the LiteX CPU. The image is dev's, file for file, so the margin is dev's (its area plan records +0.027 ns at an earlier round).

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
