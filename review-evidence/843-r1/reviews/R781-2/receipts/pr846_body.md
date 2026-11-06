[A737]

## Contents

- **[Status](#status)** -- Gate tally, open decisions and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, dependency and environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GATES GREEN, TWO OPEN DECISIONS -- `843-adopt-gptp-1616fc8f` -> `dev`, head `1105f54546b2f19d9577b7fad902c908e34f88ee`, base dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`.

- Full sweep, four shards: shards 0, 1 and 3 exit 0 (15, 17 and 16 suites). Shard 2 first exited 92: capture_coherence hit its 2,400 s limit while the CPUs were shared. Re-run alone on 4 CPUs: exit 0, 17/17 suites. 65 suites, 0 failed, 0 in-suite failures; preflight passed first time.
- milan_dp gptp and gptp-lat 212/212 each; gptp_shadow 326/326; gptp_plane 31/31; fw_service_budget 55 + 14, 0 failures.
- Builder bank: ALL GATES PASS EXCEPT 2 NOT RUN (the two dev also leaves unrun). Firmware self-test, coverage check and self-test, behave (508 scenarios), docs inventory check and self-test, lint, em dash, Vivado front-end, `git diff --check`: all rc 0.
- Every `run:` step of the docs workflow: 65 rc 0, 31 not run with a recorded reason (hosted-only steps), 0 bad.
- Physical gPTP suite: 151 + 6 + 20 + 14 + 14 checks, 0 failures (at the parent of this head; only the service oracle differs).
- Eight planted mutants, each caught by name.
- Open decision 1 (area and timing): the shipping route at this pin meets every constraint but misses the +0.03 ns build floor on its shipping directive, and the resource gate refuses it. See "Known limitations".
- Open decision 2 (issue item 4): the stricter-readings page is introduced by #842 and is not on dev, so this PR cannot point it at the merged behaviour. The text is prepared for whichever lands second.

## Linked Issue / roles

Relates to #843 (item 4 is not met on this base, so this PR does not close it)
Relates to #842 (the stricter-readings page)

Executor: `[A737]`
Internal cleared-context reviewer: to be named
External reviewer: to be named

## Description

Moves the `gptp-processor` gitlink from `135afd04` to FPGA-gPTP main `1616fc8f`, and makes clockAccuracy a per-board build value.

| Piece | Change |
|---|---|
| Gitlink | `135afd04` -> `1616fc8f`: FPGA-gPTP #98 / PR #99 (Follow_Up TLV walk) and #100 / PR #101 (Follow_Up information TLV values, announce receipt timeout from the received interval, the three stricter readings, `--clock-accuracy`). No engine port or parameter changes; no top-level port, parameter or register changes |
| Pin-derived records | ROM digest re-recorded by `syn/yosys/ooc.sh --record-rom-digests` (equal to the donor's tracked image); boundary and time-sync diagrams through their generators; donor links and the pin row |
| Builder | `gptp.clock_accuracy` joins the consumed set (`GPTP_ENGINE_CONSUMED`). `gptp_ucode_args()` passes it to `--clock-accuracy`; AVB_INTERFACE states the same octet. An omitted key is 0xFE (802.1AS-2011 8.6.2.3 b)); a value outside IEEE 1588-2008 Table 6 is refused. The comments and the refusal message no longer say the generator "consumes only" priority1, MAC and clock, or "announces this field from a constant" |
| Configs | Both AX7101 configs `clock_accuracy: 0x22` (the maintainer's 2026-11-05 decision); the three Arty configs `0xFE` (uncharacterised oscillator, 8.6.2.3 b)) |
| Model ids | The Arty configs announced 0xFE before and after, so their pinned hashes stay. The AX7101 hash-derived ids move with the descriptor content (1722.1-2021 6.2.2.8); no test pins them |
| Builder gates | Gate 1b: a clockAccuracy change must reach the image, and clock_accuracy left the refused set. Gate 26b: per-board AVB_INTERFACE bytes, the consumed set, the omitted-key default. New gate 26c: a 0x22 config (AX7101) and a 0xFE config (Arty) each build an image byte-equal to the generator's for that value, different under the other, and Table 6 refusals. The ROM clock contract's independent run states the config's value |
| gPTP legs | `milan_dp` `gptp` runs an image made through `gptp_ucode_args()` from the AX7101 config and requires 0x22 in every DUT Announce; `gptp-lat` runs the Arty config's image and requires 0xFE (`[CA]` checks, 802.1AS-2011 10.5.3.2.3). The AX7101 leg image is byte-identical to the previous rule's |
| Harnesses | `OUR_CQ` in `gptp_shadow` and `gptp_plane` comes from the generator the harness builds with, and each harness now grades it in the plane's own grandmaster Announce |
| Records | CHANGELOG, `SUBMODULES.md` adoption record with the route figures, `AREA_BUDGET.md` slice sentence, regenerated documentation inventory |

Each new check has a planted mutant that fails it by name (eight mutants, ten check runs).

## Authoritative references

- IEEE 802.1AS-2011 8.6.2.3 (clockAccuracy a) and b)), 10.5.3.2.3 and Table 10-7 (grandmasterClockQuality), 11.4.1, 10.2.8.2.1 i) to l), 10.2.9, 11.4.4.3, 10.3.9.1
- IEEE 1588-2008 7.6.2.5 and Table 6 (0x22: within 250 ns; 0xFE: unknown)
- IEEE 1722.1-2021 7.2.8 (AVB_INTERFACE clock fields) and 6.2.2.8 (entity_model_id)
- Milan v1.2 4.2.6.2.3 and 4.2.6.2.6
- #843 scope and acceptance; the maintainer decision of 2026-11-05 on clockAccuracy
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (the route recipe), `docs/integration/BUILDING.md` section 5 (the build floor), `docs/design/AREA_BUDGET.md`

## How to get into the same state

```sh
git fetch origin 843-adopt-gptp-1616fc8f
git checkout --detach 1105f54546b2f19d9577b7fad902c908e34f88ee
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
git submodule status
```

## How to validate

```sh
suite_logs=$(mktemp -d)
bash scripts/run_all_suites.sh "$suite_logs" --wait --shard 0/4
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
make -C tb/verilator/gptp_shadow run
make -C tb/verilator/gptp_plane run
python3 sw/builder/test_builder.py --gates test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board
python3 sw/builder/test_builder.py --require-rv32
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8
(cd tests && behave)
python3 scripts/docs_inventory.py --check
git diff --check cc204c6fd2349b543d73f15c97162a2c4434c86e HEAD
```

Run the sweep line for each shard 0/4 to 3/4.

Expected result / pass criteria: every command exits 0. The gptp leg prints `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A` and gptp-lat `... 0xF8FE436A`, each `212 checks: 212 PASS, 0 FAIL`; gptp_shadow `326 checks: 326 PASS`; gptp_plane `31 checks: 31 PASS`; the builder bank ends `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's MAKEFLAGS arm on this make, and gate 11's absent calibration tree, as on dev).

The shipping route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged; the figures are read with:

```sh
python3 syn/ooc/pp_resource_gate.py check <gateware directory> --endpoint route-1x1 --shipping-selection
```

## Known limitations / out of scope

- **Area and timing need an owner decision.** route-1x1 (shipping directive ExtraPostPlacementOpt only), against dev `cc204c6f`:

  | Figure | dev | this head | change |
  |---|---:|---:|---:|
  | LUT | 51,994 | 52,695 | +701 |
  | FF | 54,101 | 54,288 | +187 |
  | Slice of 15,850 | 15,841 | 15,846 | +5 |
  | RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 |
  | DSP | 13 | 15 | +2 |
  | WNS, slow corners | +0.236 ns | +0.018 ns | -0.218 ns |
  | WHS, fast corners | +0.036 ns | +0.015 ns | -0.021 ns |

  Both routes complete with no routing error and no failing endpoint. At this head the slow corners miss the +0.03 ns build floor, and `pp_resource_gate.py` refuses the LUT (+683 over the record, tolerance 500), DSP (+2, tolerance 0) and WNS floor rows. The worst path is the SoC's SDRAM controller (16 levels, 6.4 ns of routing), outside the gPTP engine and `milan_datapath`, so the fall is placement pressure at 4 free slices. The engine growth is FPGA-gPTP #100's TLV logic (+2 DSPs, the frequency multiply). The #818 ruling judges WNS on the best of three directives; the other two were not routed here.
- **Issue item 4.** The stricter-readings page arrives with #842. Its gPTP section's replacement text (the last column at `1616fc8f`, the clockAccuracy row per board) is prepared for whichever PR lands second.
- `ci/image/command-table.json` is not regenerated: `scripts/ci_tool_inventory.py --check` already refuses on dev, no PR gate runs it, and #842 edits that file.
- The physical `ax1x1gptp` leg's image rule is unchanged (its default 0x22 equals the AX7101 config's); #842 edits that line.
- Nothing here measures the AX7101 oscillator; the 0x22 claim is the maintainer's decision.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 4 and the area decision are open)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
