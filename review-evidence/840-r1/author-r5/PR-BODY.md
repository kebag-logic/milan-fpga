[A732e]

Round 5: answered R775-3 N3 = R776-3 F6 under the [A10] ruling on #840. Validated head: `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa`, on dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. The firmware is unchanged. Register 0's power-down (0.11) and loopback (0.14) join the kept bits the two gigabit arms start in opposite states, as `power_down_kept` and `loopback_kept`, with `force-bit-0.11`, `drop-bit-0.11`, `force-bit-0.14` and `drop-bit-0.14`: fifty-one advertisement mutants. The wider claims now name the twelve graded bits, and the other pass-through bits are stated as unmodified by construction (`milan_baremetal.c:1065-1069`) and not graded. The test does not extend to them, as ruled. Gates on a clean clone of this head, each rc 0: `test_phy_firmware.py` (51 advertisement, 4 poll and 5 boot-path mutants caught by name; `PHY_BOOT_OK`); every `run:` step of `docs.yml` (65 rc 0, 31 not run with a reason, 0 bad); `docs_inventory.py --check` and `--selftest`; the command-table digests of this PR's files (3 rows match, 2 stale at dev too, 0 made stale, so nothing needed re-pinning); `git diff --check` against `87e9d03a`; one merge base; `push-privacy-check.py` at 0 private lines. The full sweep, the service plans and the standalone `test_builder.py --require-rv32` were not rerun: this round's gate list replaces them, and the sweep record stays at `cadb63b4`.

Round 4: answered R775-2 and R776-2. Validated head: `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`, on dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. The firmware is unchanged: the pin-level peer gains the mixed start values and two refused-read arms, three command-table rows are re-pinned, and dev is merged. See [Round 4](#round-4). No full sweep ran, as the assignment says.

Round 3: merged dev `cc204c6f` without conflicts, regenerated the documentation inventory, and replaced six local interface spellings with `<host-iface>`. Validated head: `beb38447d07cceac5170ba0a35c7615f5714b7f7`. Inventory check/self-test, builder, PHY peer and both reviewer mutant sets, whitespace, one-merge-base check and privacy check exited 0; privacy reports 0 private lines. Documentation verifier: 65 steps ran, 31 not run with a reason, 0 bad. The full sweep was not rerun, as instructed. The body below preserves the live round-2 report; its inventory limitation is resolved by this round. No push or PR edit performed. Builder summaries: Full builder: ALL GATES PASS EXCEPT 2 NOT RUN; Documentation builder leg 0: ALL GATES PASS EXCEPT 1 NOT RUN; Documentation builder leg 1: ALL GATES PASS EXCEPT 16 NOT RUN.

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — The answer to both round-1 reviews, item by item.
- **[Round 4](#round-4)** — The answer to both delta reviews, item by item, with this head's gates.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN. 65/65 suites pass at `cadb63b4985c0ad4fb7dc036a23bf9fe93eb6276`. `840-identity-link-cert` -> `dev`

The table below is the full gate record at `cadb63b4`. [Round 4](#round-4) lists the gates run at `3d1ca52f`, and the round 5 line lists those at `27df6e08`. Each gate ran on a clean clone of its head; every listed command exited 0 unless stated.

| Gate | Result |
|---|---|
| Full sweep, four shards (`scripts/run_all_suites.sh --wait --shard k/4`, `MAKEFLAGS=-j4 --no-print-directory`) | 65 suites passed, 0 failed, 0 timed out; 2,192,435 checks, 0 in-suite failures; preflight passed |
| `tb/verilator/fw_service_budget/run.py --enforce-service`: queued-input, queued-short, queued-builtins and device-wait, on both shapes | 8 runs, each `budget findings: 0`; no PHY service finding in any of the twelve plan runs; all twelve regrade at the head |
| `sw/firmware/nvm_hosttest/test_phy_firmware.py` | 26 PHY mutants and 5 boot-path mutants caught by name; `PHY_BOOT_OK` |
| Both round-1 reviewers' `phy_extra_mutants.py`, unchanged | R775-1: 8 of 8 mutants fail a named assertion; R776-1: 8 of 8 |
| `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | pass |
| `sw/firmware/gtest/fw_coverage.py --selftest` and `--check` | pass |
| `sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | pass |
| `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32` | pass |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`, four shards | pass |
| `sw/builder/test_builder.py --require-rv32` | pass; two environment-dependent arms not run (gate 1b: this make does not re-read MAKEFLAGS mid-parse; gate 11: needs an Arty build tree) |
| `sw/builder/test_builder.py --gates test_station_mac_ul_bit_warns`, plus six planted mutants | pass; each mutant fails gate 28b |
| `cd tests && behave` | 14 features, 508 scenarios, 2330 steps passed |
| `scripts/check_nvm_capture.py`, and its five `--mutation` runs | pass; each mutation exits 1 for its named reason |
| `tb/verilator/fw_service_budget/run.py --self-test` | pass (55 oracle checks) |
| Every `run:` step of `.github/workflows/docs.yml` | 64 steps rc 0; 31 not run, each with its reason (hosted-only recording, uploads and installs already satisfied); 0 bad |
| `scripts/docs_inventory.py --check` | pass at `27df6e08` |
| `git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD` | pass |
| `make -C tb/verilator/milan_dp_gptp` (scheduled physical suite) | pass; the AX 1x1 gPTP leg reports thisClock `0x24b4cfffe4b4c01` |

## Linked Issue / roles

Relates to #840
Relates to FPGA-gPTP #100

This PR relates to #840. certification_version needs no change: the device stays uncertified, so the field stays 0.0.0.0. See Known limitations.

Executor: `[A732]` (round 1), `[A732b]` (round 2), `[A732c]` (round 3), `[A732d]` (round 4), `[A732e]` (round 5)
Internal cleared-context reviewer: `[R775]` (round 1, NEGATIVE at `dd764ed7`; round 2, NEGATIVE at `beb38447`; round 3, NEGATIVE at `3d1ca52f`)
External reviewer: `[R776]` (round 1, NEGATIVE at `dd764ed7`; round 2, NEGATIVE at `beb38447`; round 3, NEGATIVE at `3d1ca52f`)

## Description

The maintainer decisions of 2026-11-05 on #840, items 1 to 4, and the identity change of the same day.

| Piece | Change |
|---|---|
| Configs | AX7101 station MAC `02:4b:4c:4b:4c:01`, Arty `02:4b:4c:4b:4c:02`, so no octet of either EUI-64 identity is `00`. entity_id and clockIdentity stay MAC-derived: `024B4CFFFE4B4C01` and `024B4CFFFE4B4C02`. |
| Builder | `identity_warnings()` warns on stderr, never refuses, when the station MAC has the U/L bit set. Gate 28b (`test_station_mac_ul_bit_warns`) pins every config's decided identity, refuses a zero octet in it, and pins the warning's channel and exit status. |
| Firmware | `phy_advertise_gigabit_only()`: register 9 with 1000BASE-T full duplex only (MASTER-SLAVE bits kept; test-mode, half duplex and reserved bits zero), register 4 without 10/100 or 100BASE-T4 (selector and pause bits kept, reserved bit 14 zero), then one write of register 0 that enables and restarts auto-negotiation with reset and isolate clear. It writes only a PHY reporting 1000BASE-T full duplex ability (bits 1.8 and 15.13). `phy_mdio_bit()` is inlined into both frame loops. |
| Firmware test | The pin-level Clause 22 peer starts every bit the init clears at one, and two gigabit arms start twelve kept bits in opposite states: the selector, pause, MASTER-SLAVE, power-down and loopback bits. The init's other pass-through bits, register 4 bits 15, 13 and 12 and register 0 bits 13 and 8 to 0, are unmodified by construction (`milan_baremetal.c:1065-1069`) and not graded. The host driver grades those properties by name, the retry after an unacknowledged read, two PHYs without the ability (one of them read once per boot), and a gigabit PHY with auto-negotiation disabled. Fifty-one planted advertisement mutants each fail their named assertion. |
| Service budget | The scripted PHY accepts Clause 22 writes. The poll charge counts the init's four reads and three writes (sixteen transactions). `oracle.json` is regenerated by `gen_oracle.py`. |
| Capture | The harness addresses its controller traffic to the config's station MAC and MAC-derived entity_id (`probe_config.hpp`). `measurements.json` is re-measured: six arms at the head that carries the firmware and identity. |
| Fixtures | The gptp, AX 1x1 gPTP and gmstep legs carry the shipping image's identity (MAC and ADP CSRs, AECP target, the AX 1x1 gPTP ROM's `--mac` and thisClock). Also the command table entry for that Makefile line, and the bench tools' defaults and usage examples. |
| Docs | The [stricter readings page](docs/reference/STRICTER_READINGS.md), linked from `docs/README.md` and registered with the style gate. Also the firmware guide's PHY section, the builder parameter docs, the service-budget README, the [service-budget findings page](docs/findings/397_SERVICE_BUDGET.md#phy-poll-derivation-and-simulation) and the capture section of `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`. |

**Material assumption: the 1000BASE-T ability gate.** The issue says "the MAC is 1 Gb/s only". That holds for the AX7101's GMII build. The retired Arty recipe (`phy: mii-100`) pairs a 10/100 PHY with a MAC that runs 10 and 100 Mb/s (`sw/litex/milan_soc.py`, `_BOARD_PHY_MODEL` and `_PHY_MODEL_MIN_MBPS`). The Arty platform routes MDIO, so its firmware compiles the same PHY init. Unconditionally, the init would strip that PHY's only abilities, and an Arty image would never link. The init therefore writes only a PHY whose bits 1.8 (IEEE 802.3-2022 22.2.4.2.16) and 15.13 (22.2.4.4.3) report 1000BASE-T full duplex ability. Any other PHY keeps its own advertisement, as at the base. On the AX7101 the behaviour is exactly the issue's.

**Identity sources.** The station identity is produced in this repository only: `platform.mac_address`, `derive_entity_id()` and the builder's `--mac` to the gPTP microcode generator. Harness-chosen identities, such as `sw/firmware/ctrl/test/test_aecp.cpp:46-47` and the avtp and crf stream ids, assert no config identity and are left as they are. Bench findings pages keep the identity they measured.

**certification_version** stays `0.0.0.0` (item 3). It is a GET_MILAN_INFO response field (Milan v1.2 5.4.4.1, Figure 5.4), not a descriptor field. Tests asserting it already exist: check M2 of the protocol processor's `tb/pp_top` harness (the real microprogram), and `tests/features/aecp_response_contract.feature:150-154` (the model). So no test is added.

## Round 2

The round-2 assignment on #840 (issuecomment-6670627857) is answered item by item. Both reviews, R775-1 (issuecomment-6669957820) and R776-1 (issuecomment-6670614456), raised the same three findings.

| Item | Finding | What changed | Evidence |
|---|---|---|---|
| 1 | F3 (MAJOR): the raised PHY poll charge was never graded on target data | A per-transaction probe showed every MDIO transaction at `dd764ed7`, reads included, at about 16,900 cycles against the base's 8,793. `phy_mdio_write()` had given `phy_mdio_bit()` a second caller, so the compiler stopped inlining it; on the cacheless core each bit became a call and return. `phy_mdio_bit()` is now `always_inline`; `phy_mdio_read()` compiles to the base's code exactly. The bound and the trigger are unchanged. All six service plans ran on both shapes at `4ab1bca0`. `397_SERVICE_BUDGET.md` states `C = P + 16*T` and the new figures; the firmware guide's grading lines are refreshed. | Eight enforced runs: 0 findings. 8x8: T 0.12457 ms, P 1.31864 ms, C 3.31176 ms, reserve 3.19136 ms (base 4.46039). 1x1: C 3.30696 ms, reserve 41.82117 ms. Largest per-run PHY publication bound 246.80864 ms (8x8, `milan_nvm`). |
| 2 | F1 (MINOR): five claimed PHY init properties could not fail the peer | The peer starts every bit the init clears at one, and the pause and MASTER-SLAVE bits set (registers 0, 4 and 9 at `0x9400`, `0x4fe1`, `0xfdff`). Each property is its own named assertion. New arms: a gigabit PHY with auto-negotiation disabled, and a 10/100 PHY's register 15 read once per boot (reads are counted per register). Ten more mutants join the table, matched on the exact assertion message. | Both reviewers' `phy_extra_mutants.py`, run unchanged at the head: every mutant fails on a named assertion (R775-1: 8 of 8; R776-1: 8 of 8). `test_phy_firmware.py`: 26 PHY mutants and 5 boot-path mutants caught. |
| 3 | F2 (MINOR): the capture design document stated the superseded receipt | `measurements.json` is re-measured at `4ab1bca0` (six arms) for the round-2 assignment, which its `remeasurement_assignment` now names. Section 18 and section 20 item 6 state its commit, tree, firmware, pins, maxima, ratios, margins and per-arm table. The `d62417f1` receipt is history, stated as lane-started, and so is the #70 receipt. | 8x8 contract maximum 13.86384 ms (3.5344x, 10.63616 ms margin); 1x1 3.96810 ms (12.3485x). `check_nvm_capture.py` passes, and its five mutations exit 1. |
| 4 | Identity change | Station MAC `02:4B:4C:4B:4C:01` (AX7101) and `02:4B:4C:4B:4C:02` (Arty); entity_id and clockIdentity `024B4CFFFE4B4C01` and `024B4CFFFE4B4C02`. Configs, gate 28b (now also refusing a zero octet), the gPTP, AX 1x1 gPTP and gmstep legs, the Makefile `--mac` and command table, the bench tools and the stricter-readings page. The oracle is regenerated through `gen_oracle.py` and the capture receipt through fresh arms. | Gate 28b passes and six planted mutants fail it, including `entity_id 024B4CFFFE000002 has a zero octet`. The AX 1x1 gPTP leg asserts thisClock `0x24b4cfffe4b4c01`. |
| 5 | Residue | R776-1 R1: the three bench usage examples carry the AX7101 identity. R776-1 R2: the column list matches the tables. R776-1 S1: the gmstep leg's MAC and ADP registers and its AECP target are the shipping image's identity. R775-1 reported no residue. | commits `5825abd9`, `4ab1bca0`, `8d39b1b5` |
| 6 | Dev sync | Not applicable this round. When round 2 started, dev was `604899c0` without PR #815. PR #815 merged about 40 minutes later, so the dev merge falls to the next round. Live dev then differs in no config, firmware or measurement-harness file. | `git ls-remote` at the start and the end |

**The assignment's condition for lowering the cost did not arise.** The four enforced 8x8 plans were also run on `dd764ed7`'s firmware: all exited 0 with no finding. Their largest PHY publication bound was 248.68507 ms (`milan_nvm`, queued-input), 1.3 ms under 250. The cost was lowered anyway because the measured cause is this lane's own doubling of every PHY transaction, and the fix restores the base's code; that plan now grades 246.34096 ms.

Not taken: R776-1 S2 (once per boot is the documented design). R775-1 S1 is met in passing: the line had to change for item 4 and now derives the MAC words from `kStationMac`. R775-1 S2 is not in the assignment.

## Round 4

The round-4 assignment on #840 (issuecomment-6683958840) is answered item by item. Both delta reviews, R775-2 (issuecomment-6683678472) and R776-2 (issuecomment-6683953603), were NEGATIVE with MINOR findings under Tests only. Nothing under `sw/firmware/milan_baremetal`, `hdl`, `syn`, `sw/litex` or a submodule differs from `beb38447`.

| Item | Finding | What changed | Evidence |
|---|---|---|---|
| 1 | R775-2 N1: the kept fields were graded only from all-ones | The two gigabit arms start the ten bits of the selector, pause and MASTER-SLAVE fields in opposite states: the selector `00001` then `11110`, pause `10` then `01`, MASTER-SLAVE `101` then `010` (registers 4 and 9 at `0x4be1`, `0xf5ff`, then `0x47fe`, `0xe9ff`). `selector_kept`, `pause_bits_kept` and `master_slave_kept` grade them. `force-pause-on`, `force-manual-master` and `force-manual-config-only` join the table, with each of those ten bits forced and dropped. | Every one fails its named assertion. With both arms put back at their `beb38447` values, 13 of the 25 new mutants escape; each arm alone lets some escape |
| 2 | R775-2 N2 = R776-2 F5: the retry was graded for two of four registers | Registers 4 and 0 each get a refused-read arm, with `no_write_before_its_register_4_read` and `no_write_before_its_register_0_read`. `nak-reg4-not-checked` and `nak-reg0-not-checked` join the table. The register 4 arm does not use `expect_poll()`: that poll still publishes a link, because the gigabit resolution reads no register 4. | Each mutant fails by name, and escapes once its arm is removed |
| 3 | R776-2 F4: three stale script digests | `fw_service_budget/run.py`, `nvm_capture_cpu/run.py` and `nvm_capture_cpu/soc.py` are re-pinned at their bytes, three `sha256` lines and nothing else. | Against dev: 37 mismatches at both, none added, none removed. Rerunning the re-pin on a clean clone of the commit before it reproduces the committed table byte for byte |
| 4 | Dev sync | `git merge --no-ff origin/dev` at `87e9d03a`, then the inventory through `docs_inventory.py --write`, then `--check`. The only conflict was the generated audit page. | The lane's delta against dev has the same patch id before and after the merge, audit page excluded |

The firmware guide and the stricter-readings page change only where they state the peer's start values and the mutant count, now forty-seven.

**How the rows were re-pinned.** The assignment says through the table's own tool, and no repository command writes these pins: `ci_tool_inventory.py --write` writes only `tool-inventory.json`, and it refuses before writing. So the digest comes from `ci_command_table.sha256()`, the function the checker compares with, and the file from `ci_tool_inventory.serialized()`, the form the table's own harness writes. Nothing was typed by hand. A reviewer who reads the route differently should say so.

**What the re-pin does not show.** The table's checker, run with its authenticated parser, exits 2 at this head and at dev with the same words: `changed declared script 'sw/builder/endstation_builder.py'`. That is #838. In a throwaway clone, re-pinning every stale row moves the refusal to `exec`, as #838 records, and allowing `exec` moves it to `compile`, which #838 does not name. So the checker never reaches the three rows, and their re-review is the executor's reading of three small diffs against their declared reasons, for a reviewer to accept. `sw/builder/endstation_builder.py` and `sw/builder/test_builder.py` are also pinned files this PR changes; both rows are stale at dev too, so they stay #838's. `tool-inventory.json` is not regenerated, for the same reason.

Gates at `3d1ca52f8e9a3ec59076b423c0812982945c7a8b`, each on a clean clone, each rc 0:

| Gate | Result |
|---|---|
| `sw/firmware/nvm_hosttest/test_phy_firmware.py` | 47 advertisement and 4 poll mutants caught, each by its named assertion; 5 boot-path mutants caught; `PHY_BOOT_OK` |
| Both round-1 reviewers' mutant scripts, unchanged | R775-1 and R776-1: 8 of 8 each caught by name |
| `sw/builder/test_builder.py --require-rv32` | pass; 2 arms not run, as at `beb38447` (gate 1b: this make does not re-read MAKEFLAGS mid-parse; gate 11: needs an Arty build tree) |
| Every `run:` step of `.github/workflows/docs.yml`, each job on a new, empty HOME | 65 steps rc 0; 31 not run, each with its reason; 0 bad. All three SDK steps report a fresh installation |
| `scripts/docs_inventory.py --check` and `--selftest` | pass; 50 controls |
| Command-table digests of this PR's files | 3 rows match; 0 made stale by this PR; 2 stale at dev too |
| `git diff --check 87e9d03aa2a4797957ac0124d0c7851a2eec234c HEAD` | pass |
| `git merge-base --all HEAD origin/dev` | one, `87e9d03a` |
| `push-privacy-check.py . origin/dev` | 0 private lines |

Not taken, because the assignment does not ask for them: RES-4 and RES-5 (wording in the stricter-readings and service-budget pages), S1 to S5 of R775-2, and S3 to S5 of R776-2. The reviewers' own scripts still report their survivors: `init-on-failed-bmsr`, `clear-next-page`, `clear-remote-fault`, `reg0-from-constant`, `write-4-before-9`, `bmsr-unacked-still-inits`, `write-frame-no-release` and `init-before-found`. The first and sixth are one defect; the reviews name them as suggestions or discount them. RES-1, the PR title, is the manager's. RES-2, RES-3 and R4 are applied in this body, with this round's head and dev.

## Authoritative references

- #840 items 1 to 4 and its acceptance; the round-2 assignment; FPGA-gPTP #100 items 3 to 5 (listed on the page, not implemented here).
- IEEE 802-2014 8.2 and 8.4 (U/L bit); IEEE 802.1AS-2011 8.5.2.2.1 and NOTE 2; IEEE 1588-2008 7.5.2.2.2 and NOTE 1; IEEE 1722.1-2021 6.2.2.7.
- IEEE 802.3-2022 22.2.4.1.1, 22.2.4.1.4, 22.2.4.1.6, 22.2.4.1.7, 22.2.4.2.13, 22.2.4.2.16, 22.2.4.4.3, 22.2.4.5, 28.2.4.1.3 (Table 28-2), Figure 28-18, Annex 28B (Table 28B-1), 40.5.1.1 (Table 40-3).
- IEEE 802.1BA-2011 6.5 d); Milan v1.2 Chapter 1, 4.2.6.2.2 (Table 4.1), 4.2.6.2.3 (Table 4.2), 4.2.6.2.6, 5.4.4.1 (Figure 5.4).
- IEEE 802.1AS-2011 Figure 10-13 (as Cor1 changes it), B.2.3, 11.2.15.1.10, Figure 11-8, 11.5.3, 8.6.2.3; IEEE 1588-2008 7.6.2.5, Table 6.
- [Stricter readings page](docs/reference/STRICTER_READINGS.md); [firmware guide, PHY section](docs/integration/BAREMETAL_FIRMWARE.md); [service-budget findings](docs/findings/397_SERVICE_BUDGET.md).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git fetch origin 840-identity-link-cert
git checkout --detach 27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

The firmware, builder and behave gates need the RV32 SDK and the docs virtual environment that `.github/workflows/docs.yml` installs. The sweep needs Verilator 5.050, sv2v 0.0.12 and GNU Make 4.3 first on `PATH`. The service-budget and capture simulations need the product LiteX environment that `tb/verilator/nvm_capture_cpu/README.md` describes.

## How to validate

```sh
python3 sw/firmware/nvm_hosttest/test_phy_firmware.py
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8
python3 sw/builder/test_builder.py --gates test_station_mac_ul_bit_warns
python3 sw/builder/test_builder.py --require-rv32
cd tests && behave && cd ..
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 scripts/check_nvm_capture.py
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
MAKEFLAGS="-j4 --no-print-directory" bash scripts/run_all_suites.sh /tmp/sweep-logs --wait --shard 0/4
git diff --check 87e9d03aa2a4797957ac0124d0c7851a2eec234c HEAD
```

Repeat the sweep line for shards 1/4 to 3/4. Each enforced service plan, per shape (`endstation_ax7101_1x1_tdm8`, `endstation_ax7101_8x8`):

```sh
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/svc-8x8-qi --populated --plan queued-input --enforce-service
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/svc-8x8-qs --populated --plan queued-short --enforce-service
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/svc-8x8-qb --populated --plan queued-builtins --enforce-service
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/svc-8x8-dw --populated --plan device-wait --device-wait-us 3000000 --program-wait-us 5000 --enforce-service
```

Expected result / pass criteria: every command exits 0. `test_phy_firmware.py` prints `PHY_MUTANT <name>: caught by <assertion>` for every mutant and `PHY_BOOT_OK`. Each enforced plan prints `budget findings: 0`. Each sweep shard reports `failed: 0`.

## Known limitations / out of scope

- **certification_version STOP clause (acceptance item 5, for the maintainer).** The acceptance says to STOP and name the file if certification_version is produced inside a processor submodule. It is: `protocol-processor/hdl/aecp/ucode/gen_ucode.py:177`, `MILAN_CERT_VERSION = 0x00000000`. Item 3 requires no change there, so the lane named the file in its TAKEN comment and went on. Nothing in the submodule is edited.
- The gPTP readings (FPGA-gPTP #100 items 3 to 5) are recorded on the page and land with that issue and a gitlink update.
- The addresses are locally administered prototype addresses, not IEEE-assigned EUI-48 values; a production build needs an owned MA-L, MA-M or MA-S block.
- No hardware was used: the no-link behaviour against a 10/100-only partner and the PHY init's register writes are shown by the pin-level peer and the service-budget simulation only. #599 holds the physical switch-cycle rerun.
- The PHY init runs once per boot (R776-1 S2 not taken: that is the documented design).
- FPGA-gPTP #100 item 3 says Figure 10-13's tie is "not ordered". Figure 10-13 (Cor1) guards CURRENT to AGED with `!rcvdMsg`; the page states both.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
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



