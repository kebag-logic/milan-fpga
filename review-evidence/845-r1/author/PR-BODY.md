[A738]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `b16f0175ac402e124314a40d1ea9573e431684dc`: 65 suites pass, 0 failed, 0 timed out, 2,192,435 checks, 0 in-suite failures. `845-adopt-pp-92100657` -> `dev`. The firmware self-test, the builder, behave, the docs gates and the docs inventory pass at this head, and its route meets the WNS floor. One open question needs an owner's answer before merge: see the first item under known limitations.

## Linked Issue / roles

Closes #845

Executor: `[A738]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Moves the `protocol-processor` gitlink from `a9e84b66` to processor main `92100657`, the merge of processor PR #213 (processor issue #212). Its tree is the reviewed head `6162885f`'s.

The SRP Listener now applies a Talker Advertise or Talker Failed that the port registered before a Stream Input's ACMP settle: the input declares Listener Ready (or Asking Failed) within one T-MRP-JOIN of the settle, and its SRP state, GET_RX_STATE and GET_STREAM_INFO read at the settle. Before, the first settle waited for the talker's next declaration. A re-bind to the same stream keeps its registration. A link down or up now ends every Talker registration, a settled input's too, which reports it as a registration that timed out.

| Commit | Change |
|---|---|
| `ddb6a71b` | the gitlink |
| `a29a7411` | ROM ledger rows through `./syn/yosys/ooc.sh --record-rom-digests` (both images equal the `a9e84b66` rows), the pin-table row, the boundary diagram through its generator |
| `f569b5cf` | the pin page (`docs/reference/SUBMODULES.md`), the CHANGELOG and the integration contract (`docs/integration/INTEGRATION_GUIDE.md`): the pre-settle path, its reach at the shipping `N_STREAM_IN_P` = 2 (the AAF input and the CRF input), the link-change behaviour and the shipping route |
| `151cc49c` | `tb/verilator/pp_shadow/README.md` row U no longer says the processor ignores every attribute before the settle |
| `0d9c942e` | `docs/DOCUMENTATION_AUDIT.md` through `scripts/docs_inventory.py --write` |
| `d8e95dd9` | names processor issue #212 in the integration contract and row U, and states the join interval there as MRP joinTime, 200 ms |
| `519d9c2b` | test only: re-anchors the first arm of `make -C tb/verilator/milan_dp unb-mutants`, and records that campaign at 499 checks |

The reach at the shipping N: the listener keeps one port Talker registrar per Stream Input, so the port holds two Talker values. A value that arrives while both are taken is not held, and its input's first settle still waits for the talker's next declaration, at the latest its re-join after the next LeaveAll. A port receives every Talker declaration of its VLAN, so with more than two Talker values most power-on settles wait.

No top-level port, parameter or register changes; `KL_pp_shadow` and `milan_datapath` are unchanged.

**The re-anchored arm.** Processor #203 renamed the ACMP lane's request `arb_want_w` and gated it into `arb_req_w`, so since dev's pin `a9e84b66` this arm has matched nothing and the campaign has failed on dev. The arm now holds the same request one stage earlier, so what it plants is unchanged. At this head it fails exactly the four U2 order checks, to each controller on each input, 4 of 499, and its holds pass. The campaign reports 6 of 6.

Shipping route (AX7101 1x1 TDM8, one placement directive, ExtraPostPlacementOpt), measured at this head. It equals the `a29a7411` measurement in every figure; the generated top is identical but for the build directory's name, and the ROM images are byte-identical.

| Figure | dev `cc204c6f`, same recipe | This PR | Change |
|---|---:|---:|---:|
| Slice LUT | 51,994 | 52,497 | +503 |
| Slice register | 54,101 | 54,579 | +478 |
| Slice, of 15,850 | 15,841 | 15,780 | -61 |
| Block RAM tile | 87.5 | 87.5 | 0 |
| DSP | 13 | 13 | 0 |
| WNS, slow corners | +0.236 ns | +0.198 ns | -0.038 ns |
| WHS, worst corner | +0.036 ns | +0.015 ns | -0.021 ns |

The build floor (WNS >= +0.03 ns, WHS >= 0 at every corner) is met. The worst setup path is in the SoC's SDRAM controller, outside the processor and the datapath.

## Authoritative references

- Milan v1.2 5.3.8.5 (a settled Stream Input with a matching Talker Advertise being received declares Listener Ready), 5.5.3.5.18 step 4 (the settle starts the SRP reservation), Table 4.3 (joinTime default 200 ms; leavealltimer)
- IEEE 802.1Q-2022 10.7, 10.7.8 (one Registrar per registered attribute value), Table 10-4 (Begin! and Flush! take the Registrar to MT), Table 10-7 (JoinTime)
- Processor `docs/architecture/10_srp_engine.md` 6.4, "A Talker registered before the settle", and `docs/guides/integrator.md` at `92100657`
- `docs/integration/BUILDING.md` section 5 (the build floor), `docs/design/AREA_BUDGET.md` (the resource gate)
- `docs/reference/SUBMODULES.md`, `CHANGELOG.md`

## How to get into the same state

```sh
git fetch origin 845-adopt-pp-92100657
git checkout --detach b16f0175ac402e124314a40d1ea9573e431684dc
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git submodule status
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
git diff --check 87e9d03aa2a4797957ac0124d0c7851a2eec234c HEAD
./syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code -- syn/yosys/rom_digests.tsv
python3 scripts/check_submodule_docs.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
scripts/run_all_suites.sh suite-logs --wait --shard 0/4
scripts/run_all_suites.sh suite-logs --wait --shard 1/4
scripts/run_all_suites.sh suite-logs --wait --shard 2/4
scripts/run_all_suites.sh suite-logs --wait --shard 3/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8
python3 sw/builder/test_builder.py --require-rv32
cd tests && behave --no-capture -f plain && cd ..
python3 scripts/docs_inventory.py --check
make -C tb/verilator/milan_dp unb-mutants
make -C tb/verilator/milan_dp gsi-mutants
```

Expected result / pass criteria: every command exits 0. Measured at `519d9c2b`, each gate on a clean clone: the four sweep shards pass 65 suites with 2,192,435 checks and 0 failures; milan_dp alone reports 12,075 `[ok]`, 1,301 `[PASS]` and 0 `[FAIL]`. The firmware shards report the unit suites PASS, 523 of 523 control mutants caught, and the AECP and both SRP mutation campaigns PASS. The builder ends "ALL GATES PASS EXCEPT 17 NOT RUN" without a LiteX interpreter, and "ALL GATES PASS EXCEPT 2 NOT RUN" with `MILAN_LITEX_PYTHON` naming one. behave passes 14 features, 508 scenarios and 2,330 steps. `unb-mutants` reports 6 checks, 6 PASS; `gsi-mutants` reports 15 checks, 15 PASS, both clean legs at 499 of 499. Of the `run:` steps of `.github/workflows/docs.yml`, 72 ran and exit 0; the other 24 cannot run off a hosted runner or need sudo, each with its reason on record.

## Known limitations / out of scope

- **Owner decision wanted: the resource gate.** `docs/integration/BUILDING.md` section 5 has the resource gate judge an adoption, but this route was assigned one directive and is not in that gate's recipe form, so the gate exits 2, not comparable, and has no verdict here. Against the gate's `route-1x1` record the arithmetic is LUT +485 of +500, slices 0 of +80, and **FF +872 of +600**: dev alone is +394, and this adoption's +478 crosses the tolerance. The record used single-thread synthesis, so a recipe measurement may differ. `docs/design/AREA_BUDGET.md` also says the next growth needs its own owner decision. Issue #845's acceptance names the WNS floor only, and that is met.
- The CI image's declarations are not refreshed. `python3 scripts/ci_tool_inventory.py --check` refuses alike on dev and at this head, on `sw/builder/endstation_builder.py`, and no workflow runs it: 34 of 150 reviewed script pins already differ from dev's tree, the sibling `gsi_mutants.py` among them. This PR's `unb_mutants.py` makes that 35. Refreshing the table belongs to its own issue.
- `dev` moved past this branch's base, `cc204c6f`, when PR #834 merged. A trial merge conflicts in one file only, the generated `docs/DOCUMENTATION_AUDIT.md`, which `python3 scripts/docs_inventory.py --write` regenerates.
- No parent harness drives a Talker registered before the settle through `milan_datapath`; the processor's own suites grade it (`tb/srp_stream_fsms` PS1 to PS24, `tb/srp_top` LK1, `tb/pp_top` AS7 to AS9).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests (graded in the processor; no parent harness, see above)
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
