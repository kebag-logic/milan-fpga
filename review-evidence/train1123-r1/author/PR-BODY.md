[A828]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `pf-train-1123` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED: one owner decision is needed. `pf-train-1123` -> `dev-soft-core`, head `f5a1585e`, 14 commits on
`dev-soft-core` `854bd723`: the #958 sync's three, five merges, and five composition commits.

Every gate passes:
- the firmware gate with plants;
- `ctrl_boundary` and `fw_coverage`;
- the builder legs and union;
- the twin and the platform ledger;
- the Verilator suites the PRs touch;
- the split boot and `nvm_split_target`;
- both routes, on #818's floor;
- the docs gates.

The formal CPU budget measurement is complete at 1x1/1if and 8x8/1if: every arm and group, 490 groups. **The block:**
at 8x8/1if two of #969's owner-ruled conditions break on the composed image (Known limitations, first item). The
composition cannot restate either, so review waits on the owner's decision.

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

This is the one composition of the seven post-flip lab-fix PRs, each review-approved at the head merged here:
PR #958 (#956, #957) `1825ba4e`, PR #961 (#950, #954) `287ca1ee`, PR #959 (#948) `64117b77`, PR #975 (#584)
`3cda030c`, PR #971 (#969) `c113018d`, PR #978 (#973) `87b2fc0f` and PR #974 (#972) `77a74b2f`. The seven PRs are
superseded by this one and close unmerged once it merges.

Executor: `[A828]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

| Commit | What |
|---|---|
| `c812b438`, `e3de632b`, `078c60fb` | the #958 sync: PR #961 into PR #958, then `dev-soft-core` `854bd723`, then the stacked images' rom in the docs |
| `ee58b499` | merge of PR #959 (#948, the receive fan-out) at `64117b77`, no conflict |
| `8fac1fd2` | merge of PR #975 (#584, every 8x8 STREAM_PORT_INPUT's AUDIO_CLUSTER) at `3cda030c`: the AECP plant tables kept together; the ledger's entries kept as history |
| `23ee9529` | merge of PR #971 (#969, the Talkers SRP keeps) at `c113018d`: #950/#954's `Streams` and #969's `Early` sink fixtures kept whole, #969's two Python constants renamed `EARLY_S13`/`EARLY_S14` |
| `b04610c2` | merge of PR #978 (#973, a link-up inside a loop pass) at `87b2fc0f`: both SRP plant tables and both campaign prefixes kept |
| `d6c398c8` | merge of PR #974 (#972, the boot forms its link once) at `77a74b2f`: both CHANGELOG entries kept |
| `c2b2ba1a` | the ledger at the composed images' measured figures: the platform's 8x8 at 59.5 and 64.5 RAMB36, `ctrl_plat` 19,136 and 21,888 B (S14 debt 3.5 and 8.5); the size fixture's 8x8/1if at 57.5 (its `declaring-outputs` arm); `test_ctrl_memory.py`'s ledger image reaching 65.0 |
| `0ad0bf2d` | `ctrl_configs.OUTSIDE` classifies #974's `sw/litex/mac_link_status.py`, which names the firmware's tree and compiles nothing; #974's own head fails `ctrl_boundary` the same way |
| `b6b2e603` | the firmware page's pin controls, 192 with #948's seven `milan_dp` targets, as the self-test measures |
| `cfd99726` | the resolved texts held to the idiom gate; the SRP page's ledger reference made a link |
| `f5a1585e` | 8x8/1if `poll_grade.EIGHT_ONE['aecp_long']` 320 -> 325 us by the rule (30,948 CPU cycles, every owner bound held); section 13 records the formal measurement |

- **The resolutions.** Every conflict keeps both sides. Combined figures (the ROM ledger, `ctrl_plat`, the sink and
  plant counts, the pin controls) are measured on the composed tree, never added from the PRs' figures.
- **What changes no image.** After `c2b2ba1a` no commit changes an image input. `plat_ledger` at `f5a1585e` gives all
  24 image hashes identical to `c2b2ba1a`'s.
- **What this PR does not touch.** No RTL, mailbox-contract, lwSRP or bound change by the composition, and the
  tsn-c-stack pin is unchanged at `715589c1`.
- **The CPU budget against the #958 sync's STOP.** The two statements the sync found exceeded hold on the composed
  images:
  - 1x1/1if paced: 28,733 CPU cycles, 305 of 315 us.
  - 8x8/1if largest legal command: 85,310 cycles, 900 of 1,720 us. With #584 the input map can change at 8x8, so the
    group edits it there as at 1x1; the output map's edit on the same image measures 1,435 us, also within.
- So neither is raised. The one statement exceeded, 8x8/1if `aecp_long`, is raised by the rule.

## Authoritative references

- [#665](https://github.com/kebag-logic/milan-fpga/issues/665): the owner's rule of 2026-11-15 (an image past its
  entry raises it, owed to S14), ruling item 4 of 2026-11-20 (a CPU-budget statement a measurement exceeds is restated
  at the measurement + 5 %, rounded up to 5 us), and the manager's ruling on the #958 sync's STOP (the two
  answering-ports statements raised by that rule from the formal measurement of the composed head).
- [#969](https://github.com/kebag-logic/milan-fpga/issues/969): the owner's ruling of 2026-11-22. The kept Talkers'
  records are owed to #977 while each costs no more than the bound record of its own interface on the same image.
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
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check
# the formal CPU budget measurement, every arm and group, at 1x1/1if and 8x8/1if:
for v in none answering-ports shutdown-entry answering-later answering-every-port valid-destinations talker-notices declaring-outputs; do
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/b-1x1-$v --variant $v --record-budget-findings --record-share-findings
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir /tmp/b-8x8-$v --variant $v --record-budget-findings --record-share-findings
done
python3 -I tb/verilator/ctrl_service_budget/record_classes.py /tmp/b-1x1-*/results /tmp/b-8x8-*/results
python3 -I tb/verilator/ctrl_service_budget/kept_grade.py /tmp/b-8x8-none
```

Expected result / pass criteria: - The firmware gate's four shards PASS with every plant caught.
- `ctrl_boundary` PASS with 0 findings.
- `plat_ledger` PASS with 0 findings.
- The grade checks PASS: `load_grade` 0.512 / 0.744; `flip_grade` 1x1/1if last 127.43 of 130 ms, ACMP 29.15 of 30,
  txL 47.98 of 49; 8x8/1if THE TRANSMIT 76.86 of 77 ms.
- The formal measurement: no refusal; only the 7 known held-egress misses; no pass over THE SHARE but `srp-bound`'s
  (owed to #977); `record_classes` PASS at both points; 1x1/1if 0 statements exceeded.
- `kept_grade` PASS at 1x1/1if. **At 8x8/1if `kept_grade` FAILS** on #969's two conditions (below) until the owner
  decides them.

## Known limitations / out of scope

- **#969's two conditions at 8x8/1if (the block).** The owner's ruling on #969 (2026-11-22) owes the kept Talkers'
  records to #977 while `kept_grade`'s conditions hold. On the composed image:
  - **Arm A, kept <= bound:** the kept Talker Failed's record is 142,582 CPU cycles against the bound record's
    142,137. At #969's head they were 142,909 against 153,208, so the bound path got about 11,000 cycles cheaper.
  - **`answering-ports`, a build pass within its statement:** `srp-bound`'s build of one MRPDU is a pass of 171,645
    cycles, past `CTRL_LOOP_BUILD_ONE_PASS_US`'s 147,500 (1,475 us, tier 2's slice at that shape).
  - 1x1/1if holds both in both arms. Neither is a statement the rule restates: the first is the ruling's own condition
    and the second a firmware constant.
- **The output map's largest edit at 1x1/1if is unmeasured** (pre-existing, #894's design). A scratch probe on the
  composed image, not committed, measured the output map's 63-mapping edit at 176,099 cycles, 1,850 us. That is past
  the 975 us that the input map's largest legal command states, which is the edit the harness measures. Proposed as a
  new Issue, not changed here.
- **The 8x8/1if entry.** The 8x8/1if product image plans 59.5 RAMB36 and the 8x8/2if image 64.5, both as S14 debt by
  the owner's rule of 2026-11-15; S14 moves the cold code to flash.
- **Two gate findings the composed head surfaced are fixed here.** One is an unclassified builder from #974, which
  #974's own head carries: the file and the classification lists are identical there. The other is the firmware
  page's pin control count, 185, against the 192 the self-test measures with #948's seven `milan_dp` targets; #948's
  own head was not re-run for it.

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
