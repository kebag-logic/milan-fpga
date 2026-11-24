Observed public PR body at independent review.
URL: https://github.com/kebag-logic/milan-fpga/pull/988
Head: 43076d0f8c87b5118f6f4317d000a7eebdefc967

[A828]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `pf-train-1123` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why, and every statement this PR changes, with its figures.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses, rulings and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Ready for review. `pf-train-1123` -> `dev-soft-core` `aa30d77f`, head `43076d0f`.

Every gate passes at the head or, where the head changes none of the gate's inputs, at an earlier head whose inputs
are identical:
- the firmware gate with plants, all four shards;
- `ctrl_boundary` and `fw_coverage`;
- the builder legs and union;
- the twin and the platform ledger;
- the Verilator suites the PRs touch;
- the split boot and `nvm_split_target`;
- both routes, on #818's floor;
- the CPU budget harness's checks and self-tests;
- the docs gates.

The formal CPU budget measurement is complete at 1x1/1if and 8x8/1if: every arm and every group, 490 groups. Its
`kept_grade` passes at both points under the owner's amendment of #969's conditions
([#969, 2026-11-23](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252)).

## Linked Issue / roles

Closes #956
Closes #957
Closes #950
Closes #954
Closes #948
Closes #584
Closes #969
Closes #973
Closes #972
Relates to #665
Relates to #977

This is the one composition of the seven post-flip lab-fix PRs. Each was review-approved at the head merged here:

| PR | Issues | Head merged |
|---|---|---|
| #958 | #956, #957 | `1825ba4e` |
| #961 | #950, #954 | `287ca1ee` (and its `dev-soft-core` merge `aa30d77f`) |
| #959 | #948 | `64117b77`, then its reviewed head `8aeb2f0b` |
| #975 | #584 | `3cda030c` |
| #971 | #969 | `c113018d` |
| #978 | #973 | `87b2fc0f` |
| #974 | #972 | `77a74b2f` |

The seven PRs are superseded by this one and close unmerged once it merges.

Executor: `[A828]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

| Commit | What |
|---|---|
| `c812b438`, `e3de632b`, `078c60fb` | the #958 sync: PR #961 into PR #958, then `dev-soft-core` `854bd723`, then the stacked images' rom in the docs |
| `ee58b499` | merge of PR #959 (#948, the receive fan-out) at `64117b77`, no conflict |
| `8fac1fd2` | merge of PR #975 (#584, every 8x8 STREAM_PORT_INPUT's AUDIO_CLUSTER) at `3cda030c`. The AECP plant tables are kept together, and the ledger's entries are kept as history |
| `23ee9529` | merge of PR #971 (#969, the Talkers SRP keeps) at `c113018d`. #950/#954's `Streams` and #969's `Early` sink fixtures are kept whole, and #969's two Python constants are renamed `EARLY_S13`/`EARLY_S14` |
| `b04610c2` | merge of PR #978 (#973, a link-up inside a loop pass) at `87b2fc0f`: both SRP plant tables and both campaign prefixes kept |
| `d6c398c8` | merge of PR #974 (#972, the boot forms its link once) at `77a74b2f`: both CHANGELOG entries kept |
| `c2b2ba1a` | the ledger at the composed images' measured figures (below) |
| `0ad0bf2d` | `ctrl_configs.OUTSIDE` classifies #974's `sw/litex/mac_link_status.py`, which names the firmware's tree and compiles nothing. #974's own head fails `ctrl_boundary` the same way |
| `b6b2e603` | the firmware page's pin control count, as the self-test measures it (below) |
| `cfd99726` | the resolved texts held to the idiom gate; the SRP page's ledger reference made a link |
| `f5a1585e` | 8x8/1if `aecp_long` raised by the rule (below); section 13 records the formal measurement |
| `93c5ad84` | merge of PR #959's reviewed head `8aeb2f0b` (README only, the same 192 count): the tree is unchanged |
| `4df6751e` | merge of `dev-soft-core` `aa30d77f` (PR #961's merge). Both its parents were already composed, so the tree is unchanged |
| `ce8454cb` | `kept_grade.py` grades #969's conditions as the owner's amendment states them (below) |
| `43076d0f` | the harness README, `kept_window.py` and the design page record the amended conditions and the re-grade |

### The statements this PR changes

| Statement | Before | After | Measured | Why |
|---|---|---|---|---|
| 8x8/1if platform entry (`ctrl_memory.py`) | 59.0 RAMB36 | **59.5** | 141,616 B rom, 100,096 B sram | the owner's rule of 2026-11-15; S14 debt 3.5 |
| 8x8/2if platform entry | 64.0 RAMB36 | **64.5** | 143,368 B rom, 117,632 B sram | the same rule; S14 debt 8.5 |
| `ctrl_plat` at 8x8/1if, 8x8/2if, 1x1/2if | as each PR | **19,136, 21,888, 19,840 B** | 64 B more than #969 alone | measured on the composed images |
| 8x8/1if size fixture entry | 57.0 RAMB36 | **57.5** | 133,128 B rom (`declaring-outputs`) | the same rule; S14 debt 1.5 |
| 8x8/1if `poll_grade.EIGHT_ONE['aecp_long']` | 320 us | **325 us** | 30,948 CPU cycles (`declaring-outputs` `aecp-largest-notice`) | #665 ruling item 4, measurement + 5 %, every owner bound held |
| the firmware page's pin control count | 185 | **192** | `ctrl_boundary --selftest` | #948's seven `milan_dp` pin-control targets |
| #969's kept <= bound (`kept_grade.py`) | kept <= bound | **kept <= bound x 1.05**, printed with both figures and the margin | 8x8/1if arm A: kept Failed 142,582 against bound 142,137, +0.31 %, margin 6,661 to 149,243 | [#969's amendment](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252), item 1 |
| `srp-bound`'s build of one MRPDU and its passes over THE SHARE | a finding (build) / owed (SHARE) | **owed to #977** by name, as a pass and as THE TRANSMIT's tier-2 slice | 171,645 cycles against `CTRL_LOOP_BUILD_ONE_PASS_US`'s 147,500 (8x8/1if `answering-ports`); SHARE passes 216,785 (arm A) and 203,961 | the amendment, item 2; neither constant restated |

The two statements the #958 sync found exceeded hold on the composed images and are **not** raised:
- 1x1/1if `edit_rows.PACED`: 28,733 CPU cycles, 305 of 315 us.
- 8x8/1if `rows_tiers.LONG_RECORD_US`: 85,310 cycles, 900 of 1,720 us.

No owner bound changes. `CTRL_LOOP_BUILD_ONE_PASS_US`, `CTRL_LOOP_SRP_UNIT_US`, THE SHARE and every owner bound
are unchanged. The kept path's builds and its passes over THE SHARE stay findings: it has 0 passes over THE SHARE,
and its heaviest build of one is 86,018 cycles at 8x8/1if.

- **The resolutions.** Every conflict keeps both sides. Combined figures (the ROM ledger, `ctrl_plat`, the sink and
  plant counts, the pin controls) are measured on the composed tree, never added from the PRs' figures.
- **What changes no image.** After `c2b2ba1a` no commit changes an image input. `plat_ledger` at `43076d0f` gives
  all 24 image hashes identical to `c2b2ba1a`'s and `f5a1585e`'s. So the formal measurement's logs are the head's,
  and they are re-graded, not re-simulated.
- **What this PR does not touch.** It makes no RTL, mailbox-contract, lwSRP or owner-bound change, and the
  tsn-c-stack pin is unchanged at `715589c1`.

## Authoritative references

- [#665](https://github.com/kebag-logic/milan-fpga/issues/665):
  - the owner's rule of 2026-11-15 (an image past its entry raises it, owed to S14);
  - ruling item 4 of 2026-11-20 (a CPU-budget statement a measurement exceeds is restated at the measurement + 5 %,
    rounded up to 5 us);
  - the ruling on the #958 sync's STOP.
- [#969](https://github.com/kebag-logic/milan-fpga/issues/969): the owner's ruling of 2026-11-22 (the kept Talkers'
  records owed to #977 while kept_grade's conditions hold), and
  [its amendment of 2026-11-23](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252):
  kept <= bound held within the measurement rule; the bound path's build of one and its passes over THE SHARE owed
  to #977; every owner bound held.
- [#977](https://github.com/kebag-logic/milan-fpga/issues/977): the registration cost, which must clear THE SHARE and
  the build slice on the composed head before the post-flip in-house qualification closes.
- Each PR's own references, unchanged: Milan v1.2 5.3.3.8, 5.3.7.3, 5.3.8.5, 5.5.3.5.18, Tables 5.9, 5.10, 5.22, 5.47;
  IEEE 1722.1-2021 7.4.9, 7.4.16, 7.5, 8.2; IEEE 802.1Q-2018 10.7, 35.2.
- [docs/design/SPLIT_CONTROL_MEMORY.md](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 3, 5 and 13;
  [tb/verilator/ctrl_service_budget/README.md](../tb/verilator/ctrl_service_budget/README.md).

## How to get into the same state

```sh
git fetch https://github.com/kebag-logic/milan-fpga.git pf-train-1123
git checkout --detach FETCH_HEAD
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
git -C third_party/tsn-c-stack rev-parse HEAD   # 715589c1db7cf67e2f3259fd7083ebc7f0923376
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard K/4   # K = 0..3
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/ledger
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/sb-plants --self-test
python3 -B tb/verilator/nvm_split_target/run.py --self-test
python3 -I tb/verilator/ctrl_service_budget/kept_grade.py --selftest
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
# the formal CPU budget measurement, every arm and group, at 1x1/1if and 8x8/1if:
for v in none answering-ports shutdown-entry answering-later answering-every-port valid-destinations talker-notices declaring-outputs; do
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/b-1x1-$v --variant $v --record-budget-findings --record-share-findings
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir /tmp/b-8x8-$v --variant $v --record-budget-findings --record-share-findings
done
python3 -I tb/verilator/ctrl_service_budget/record_classes.py /tmp/b-1x1-*/results /tmp/b-8x8-*/results
for p in 1x1 8x8; do for v in none answering-ports; do
  python3 -I tb/verilator/ctrl_service_budget/kept_grade.py /tmp/b-$p-$v
done; done
```

Expected result / pass criteria:
- The firmware gate's four shards PASS with every plant caught.
- `ctrl_boundary` PASS with 0 findings (117 boundary, 192 pin and 4 figure controls).
- `plat_ledger` PASS with 0 findings.
- `kept_grade --selftest` PASS (24 checks). Kept 4 % over bound holds and 6 % over breaks. A kept pass over THE
  SHARE and a kept build of one over its slice are findings. The bound path's build of one and its SHARE pass are
  owed.
- The grade checks PASS:
  - `load_grade`: 0.512 / 0.744;
  - `flip_grade` at 1x1/1if: last queued notice 127.43 of 130 ms, ACMP 29.15 of 30, txL 47.98 of 49;
  - `flip_grade` at 8x8/1if: THE TRANSMIT 76.86 of 77 ms.
- The formal measurement:
  - no refusal;
  - only the 7 known held-egress misses;
  - no pass over THE SHARE but `srp-bound`'s, owed to #977;
  - `record_classes` PASS at both points;
  - 1x1/1if: 0 statements exceeded.
- `kept_grade` PASS with 0 findings in all four. In arm A the kept Talker Failed record is 142,582 against the bound
  record's 142,137 at 8x8/1if (within +5 %, margin 6,661) and 36,631 against 38,739 at 1x1/1if. It prints 4 owed at
  1x1/1if in both arms, 5 at 8x8/1if in arm A, and 6 at 8x8/1if in `answering-ports`, among them `srp-bound`'s build
  of one at 171,645 cycles.

## Known limitations / out of scope

- **The registration cost stays owed to #977.** The kept and bound Talkers' records are over `CTRL_LOOP_SRP_UNIT_US`
  at both points. At 8x8/1if `srp-bound` has one work pass over THE SHARE in each arm, and in `answering-ports` its
  build of one is past `CTRL_LOOP_BUILD_ONE_PASS_US`. By #969's amendment these are owed to #977, which must clear
  THE SHARE and the build slice on the composed head before the post-flip in-house qualification closes. Nothing here
  restates them.
- **The output map's largest edit at 1x1/1if is unmeasured** (pre-existing, #894's design). The harness measures the
  input map's edit wherever the input map can change. A scratch probe on the composed image, not committed, measured
  the output map's 63-mapping edit:
  - 176,099 cycles, 1,850 us, past the 975 us the input map's largest legal command states;
  - 2 of 105 work passes over THE SHARE.

  It is proposed as a new Issue and not changed here.
- **The 8x8 entries.** The 8x8/1if product image plans 59.5 RAMB36 and the 8x8/2if image 64.5. Both are S14 debt by
  the owner's rule of 2026-11-15; S14 moves the cold code to flash.
- **Two gate findings the composed head surfaced are fixed here:**
  - an unclassified builder from #974, which #974's own head carries (the file and the classification lists are
    identical there);
  - the firmware page's pin control count, 185 against the 192 the self-test measures with #948's seven `milan_dp`
    targets. PR #959's reviewed head `8aeb2f0b` states the same 192.

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


