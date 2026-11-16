[A787] Sync dev `6b66f66d` into dev-soft-core (owner branch policy, 2026-10-26: dev stays the all-fabric line, and dev-soft-core takes dev's merged work until the flip), as ruled in item 3 of the ruling on #665 on the S12b rehearsal's gPTP group.

## Contents

- **[Status](#status)**: the gate tally, the open decision, and `sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, executor and reviewers.
- **[Description](#description)**: the merge, its conflicts and their resolution, the commits after it, the gPTP items, the ledger and the figures.
- **[Authoritative references](#authoritative-references)**: the branch policy, the ruling and both sides' merged PRs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and its dependencies.
- **[How to validate](#how-to-validate)**: the gate set and the expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what a sync does not do, and what it found.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

STOP posted on #665: one 8x8/1if service-budget row is over its bound after the merge. The decision is open; this body is drafted for the PR once it is ruled. `sync-dev-6b66f66d-into-dev-soft-core` -> `dev-soft-core`. Head `d2da3159`. Base: `dev-soft-core` `659d7687`.

## Linked Issue / roles

Relates to #665

Executor: `[A787]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

One `--no-ff` merge of dev `6b66f66d` (merge base `1f29f189`, the #830 sync) into dev-soft-core `659d7687`. After it comes one commit per semantic conflict found and per regeneration. The merge carries only work already merged on dev under the full bar: #828, #831, #836, #815, #834, #841 (#839), #842 (#840), #849, #847 (#845), #846 (#843), #852 (#851), #825, #835, #862, #875, #893 (#883) and #913.

**The merge, `62625941`.** Ten files conflicted, in 13 hunks. Both sides are kept in each.

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

**Pins.** gptp-processor `1616fc8f` and protocol-processor `801ef228` follow dev; each is a fast-forward of the old pin. tsn-c-stack stays at this line's `715589c1` (#892), which descends from dev's `70936b77`. No other submodule moved.

**After the merge**, one commit each:

| Commit | What |
|---|---|
| `a563a83d` | Semantic conflict. dev's #839 gates the control lane through `pp_txs_*`, and the split's `KL_ctrl_split` still drove `pp_tx_tvalid_w`, so the split build refused (`%Error-UNDRIVEN: ... 'pp_txs_tvalid_w'`). The split now binds the gated handshake, as the all-fabric wrapper does. The split firmware writes both station MAC halves before it enables any CSR-addressed transmitter (`ctrl_plat_csr.c:38-39`). |
| `dfcd8eed` | Semantic conflict. The split leg's `[TX]` frame then waited for a MAC the bench never wrote. The bench writes it as the platform does, and `[TX]` checks the hold, before the MAC is written and with its low half alone. `split_mutants.py` plants the lane taken past the gate and the gate opened by one half; 28 of 28 are caught. |
| `b84d095a`, `d2da3159` | Semantic conflict. dev's area plan said #810 is not merged and linked this line's FR_NFR as proposing 10 ms. On this line #810 merged on 2026-11-13 and 20 ms is approved. |
| `d8c8c4b7`, `1facd42e` | Semantic conflict. The two-placement stimulus and its rows held the shipping config's pre-#840 identity, so at the merge neither half answered AECP. They take 02:4B:4C:4B:4C:01. lwSRP seeds its LeaveAll draws from the MAC (`srp_mbx.c:347-348`), which moves one count and one plant's timestamp. |
| `3c94c76c` | Semantic conflict. Processor `801ef228` (#893) fixes the fabric's #857, #858 and #860, so the twin's four owed rows reported "the defect has gone". They are deleted with their six plants. Twin: 0 findings, 14 of 14 plants refused. |
| `3a5ba178` | Restatement. `SPLIT_CONTROL_MEMORY.md` section 5's images at the head: 24 to 40 B more rom each, from the identity's immediates, and no tile moved. |
| `f5750b3d` | Regeneration. `docs/DOCUMENTATION_AUDIT.md`, through `docs_inventory.py --write`. |

**The gPTP items and the identity on the split images.** The split keeps the fabric gPTP plane until #665 F6 (`milan_datapath.sv:9160`, on `GPTP_PLANE_EN_P` alone). Its ROM is the builder's, from the config (`milan_soc.py:1044`).
- **clockAccuracy 0x22** (IEEE 802.1AS-2011 8.6.2.3) reaches the split images through both AX7101 configs. It goes to the engine ROM as `--clock-accuracy 0x22`, and to the AEM's AVB_INTERFACE as `clock_accuracy` 0x22, which the split firmware serves.
- **The three engine fixes** come with gptp-processor `1616fc8f`: the Announce at the timeout instant (10.3.9.1), the unknown first Follow_Up TLV (11.4.1) and the late Pdelay response (Milan v1.2 4.2.6.2.6).
- **The identity 02:4B:4C:4B:4C:01** (#840) reaches the entity ID, the AEM, the firmware's generated constants, the station-MAC CSR writes and the engine ROM's `--mac`.
- **#840's 1000BASE-T-only advertisement does not reach the split.** It lives in the release firmware's PHY init, and the split firmware has no MDIO path.

**The ledger.** #847, #852 and #893 fixed the fabric processor. Each has a split counterpart:

| Fix | Split counterpart | Test |
|---|---|---|
| #847 (#845): a Talker registered before the settle, and the registrars on a link change | `srp_mbx.c:530`, `:695`, `:862`, `:910` | `Srp.HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep`, mutant `binding-change-not-copied` |
| #852 (#851): one vector per value per MRPDU | lwSRP `mrp_mad.c:1351`, `:1410` | srptx `[WIRE]`, plant `doubled-declaration` |
| #893 (#857): LeaveAll with nothing declared | lwSRP `mrp_mad.c:779` | the twin's LeaveAll grade |
| #893 (#860): New twice, and JoinIn only when IN | lwSRP `mrp_mad.c:149`, `:1278` | the twin's Table 10-3 grade and its plants |
| #893 (#858): ENTITY `available_index` | `ctrl_app_aecp.c:113` | `App.EntityReadSeesTheLastAdvertisedIndex`, two mutants |

**Figures.**
- **ROM per split image:** every image grows 24 to 40 B, and none leaves its banks, its tiles or its ledger.
- **CPU service-budget harness at 1x1/1if:** leg for leg as at the base. Arm A's 96 groups have 0, 0, 0 and 7 misses by quarter, the 7 being the ruled held-egress rows. The answering-every-port arm and the answering-ports leg pass. The flip check passes, and the load is 0.516 and 0.512 against 0.70.
- **At 8x8/1if:** as at the base but for one row (the STOP).
- **Split 1x1/1if route:** all three directives meet +0.030 ns. The best is AltSpreadLogic_high, +0.399 / +0.036 ns.
- **Split 8x8/1if route:** the best of three, AltSpreadLogic_high, meets at +0.140 / +0.036 ns. ExtraTimingOpt (+0.014) and the recipe's directive (-0.595) do not.
- **Release AX7101 1x1:** its gateware export equals dev `6b66f66d`'s file for file, and its datapath elaborates identically in every shape.

## Authoritative references

- The owner branch policy (2026-10-26), recorded on #665.
- The ruling on #665 on the S12b rehearsal's findings and its gPTP group, item 3; the rehearsal report's gPTP group.
- The previous sync, #830.
- dev's #846 (#843): IEEE 802.1AS-2011 8.6.2.3, 10.3.9.1, 11.4.1; Milan v1.2 4.2.6.2.6. dev's #842 (#840), #841 (#839), #847 (#845), #852 (#851), #893 (#883: #857, #858, #860).
- IEEE 802.1AC-2016 11.1, IEEE 802.1Q-2022 6.8.1; IEEE 802.1Q-2018 Table 10-3, 10.7.6.3, 10.7.9; IEEE 1722.1-2021 Table 7-2, 6.2.2.15.
- `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (sections 5 and 13), `docs/reference/FR_NFR.md` (NFR-SCOUT-01 to -03, 3.4.1), `tb/verilator/milan_dp/README.md`, `tb/verilator/ctrl_service_budget/README.md`.

## How to get into the same state

```sh
git fetch origin
git switch --detach d2da3159
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

The pinned tools are those of `rtl-fast.yml` and `docs.yml`: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, and the RV32 SDK of `scripts/ci_rv32_sdk.py`. The LiteX legs and the CPU budget harness use the LiteX revisions of `sw/litex/litex_pins.txt`.

## How to validate

```sh
make -C tb/verilator/milan_dp split split-mutants twin twin-plants
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings --groups save-held
python3 scripts/docs_inventory.py --check
bash scripts/run_all_suites.sh <logdir> --wait --shard k/4   # k = 0 to 3
```

Also every step of the four workflows. Expected:
- `split`: 84 checks, 0 failures. `split-mutants`: 28 of 28. `twin`: 0 findings. `twin-plants`: rc 0.
- The flip and load checks pass.
- The 1x1 arm A: 7 misses, all `backlog-owed`'s held-egress rows.
- The 8x8-1if `save-held`: `mrpdu.leaveall.if0` 161 ms, the open decision.

## Known limitations / out of scope

- **The 8x8/1if LeaveAll row (the STOP).** lwSRP's MAC-seeded LeaveAll draw meets THE TRANSMIT's over-slice build at 8x8/1if under the held load. The over-slice build is #914's scope and predates the sync.
- **#840's 1000BASE-T-only advertisement is not on the split.** The split has no MDIO path, and #919's PHY poll does not list it.
- **`make srptx` fails at the base as at the head.** Its JoinTime is 20 cs against the adapter's 19 cs (#916).
- **The 8x8/1if split image's timing margin is thinner than at #810** (+0.140 against +0.292, on its best directive), on the EDIT window's path into the audio map's output claim.
- **The 4-shard sweep and the release route** are recorded with the round that completes them.

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
