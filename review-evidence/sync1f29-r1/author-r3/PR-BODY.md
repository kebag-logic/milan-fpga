[A723d] Sync dev `1f29f189` into dev-soft-core (owner branch policy, 2026-10-26: dev stays the all-fabric line, and dev-soft-core takes dev's merged work until the flip).

## Contents

- **[Status](#status)**: the gate tally, and `sync-dev-1f29f189-into-dev-soft-core` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, executor and reviewers.
- **[Description](#description)**: the merge, its conflicts and their resolution, and the commits after it.
- **[Round 2](#round-2)**: what answers the reviews of `9f81df00`.
- **[Authoritative references](#authoritative-references)**: the branch policy, the rulings and both sides' merged PRs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and its dependencies.
- **[How to validate](#how-to-validate)**: the gate set and the expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what a sync does not do.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

GREEN locally: every gate this round touches exits 0 on the head, but for the budget harness arms that report refused probes, rc 1 as the table below states `fa019799` (the second table under [How to validate](#how-to-validate)); `sync-dev-1f29f189-into-dev-soft-core` -> `dev-soft-core`. Base: `dev-soft-core` `5b5f4336`.

## Linked Issue / roles

Relates to #665

Executor: `[A723d]` (the merge commit by `[A723b]`, its resolution by `[A723]`, the commits through `9f81df00` by `[A723c]`)
Internal cleared-context reviewer: `[R759]`
External reviewer: `[R760]`

## Description

One `--no-ff` merge of dev `1f29f189` (merge base `97aab1d0`, the #798 sync) into dev-soft-core `5b5f4336`, then one commit per item the rulings on #665 name and per semantic conflict found. The merge carries only work already merged on dev under the full bar: #786 (#396 part A); #802 (#799), the sixth processor pin adoption with each talker source's current Stream ID in the mailbox's source entries; #805 (#803) and #813 (#806), gPTP adoptions; #816 (#70); #821 (#817); #826 (#814), the SoC's SPI-flash, CPU memory-port and refresh cuts and the registered LiteDRAM refresher; #820 (#818), the route WNS gate; #822 (#787), the AECP REBOOT reset sequence.

**The merge, `97e9a3d3`.** Every textual conflict (7 files, 12 hunks) is this line's contract 2.3 face block (#795) against dev's contract 2.3 source entries (#802). Both are kept. Under the ruling of comment 6553999730 (option B), this line keeps minor 3 for the face block and the merge raises the contract to **2.4** for dev's source entries. `KL_mbx_pkg.sv`, `mbx_contract.h` and `MAILBOX_CONTRACT.md` are regenerated through `gen_mailbox.py --write` only.

| File | Resolution |
|---|---|
| `sw/mailbox/mailbox.yaml` | both history entries; dev's becomes Minor 4; `version.minor` 4 |
| `sw/mailbox/gen_mailbox.py` | one register-decode regex for both blocks; the register lists in contract order; both sides' output arms (35) and contract arms (49) |
| `sw/mailbox/mailbox_skeleton.py` | dev's publication stream_id check beside the sink check, then the face check |
| `sw/firmware/ctrl/test/ctrl_mutants.py` | both sides' model mutants |
| `sw/litex/milan_soc.py` | one `CtrlMailbox` docstring stating both blocks' unread outputs; the code auto-merged with both port sets |
| `tb/verilator/mbx/README.md` | dev's P rows, then this line's F and T rows |
| `docs/design/MAILBOX_SPLIT.md` | both sides' rows and paragraphs; the figures re-measured (below) |

**After the merge**, one commit each:

| Commit | What |
|---|---|
| `5d22d4fb` | The port census (ruling of comment 6554243203, option C). `src_stream_id_o` (#799) is class C, carried by 2.4's source entries. `reboot_req_o` (#787) is class G; its cone stops at the one cell input `reboot_ctrl.reboot_req_i` (`REBOOT_TERMINAL`). That exclusion is a placement-switch acceptance item, next to the `amr_fsm` exclusion, and has its own self-test arm: a probe reading the request's net past the terminal still fails `g-on-wire`. The REBOOT carrier on the split line is switch-over work, so it is an open item in `MAILBOX_SPLIT.md`. |
| `30973ef5` | dev's 11 living citations of "2.3" for the source entries become 2.4. The dated records of the #799 measurement at dev `97aab1d0` keep 2.3 (`AREA_BUDGET.md`, finding 234, `pp_resource_baseline.json`). |
| `73338019` | Semantic conflict: the CPU budget harness's own `KL_mbx` left dev's `pub_src_sid_o` unconnected, and its build refused (PINMISSING). It is now named and unread, as `CtrlMailbox` leaves it. |
| `fab0be5b` | Semantic conflict: each side grew `mailbox_emit.emit_doc`, and the merged function is 104 lines, over Rule 12's 100 (the Python idiom gate failed). The face block's sections move to their own function; the generated reference is byte-identical. |
| `dcd56703` | The S2 service-budget harness stages its LiteSPI PHY with `milan_soc.stage_spi_phy`, as `MilanSoC.add_spi_flash` stages every SoC since #814. The flash-window, refill and XIP arms are re-measured, each against the same head without the stage, and the "same access cost" claim and figures are corrected. |
| `9f81df00` | `MAILBOX_SPLIT.md`'s verification figures at the head: the census's 41 reads of 22 of 26 nets, 219 ports, 139 self-test arms and 43 rules; the mbx suite's 525 and 570 checks at one interface, 532 and 577 at two; the host model's 490. |

## Round 2

The reviews of `9f81df00`: `[R760]` POSITIVE, `[R759]` NEGATIVE with two MINOR findings. One commit each:

| Commit | Answers | What |
|---|---|---|
| `442da911` | `[R759]` RES-1, `[R760]` R1 | `census_ports.py` and `mailbox.yaml` cite the issue, not the comment ID. Comments and one table reason string only; the generated outputs are unchanged (`gen_mailbox.py --check --crosscheck`, 0 findings). |
| `cb0be3cd` | `[R759]` F1, `[R760]` R5 | `ctrl_split_boot/README.md` restates the boot's figures at the head. The stage reaches that SoC through `split_soc.add_devices`; the earlier statement that it does not was wrong. Each shape has a no-stage control, and the control equals the figures recorded at `b8628704`, cell for cell. The stage costs the boot 523 CPU cycles at each shape; no verdict moves. |
| `fa019799` | `[R759]` F2, `[R760]` R4 | `ctrl_service_budget/README.md`: both 1x1, 4 KiB composed maxima are labelled partial, 2 of 4 windows. The text says why. The event ring holds 5 records (4 with no stage) when `backlog-adp` and `backlog-adp-refill` open, so the coalesced grandmaster source commits 12 events (13 with no stage) against the defined 15, and the grader refuses both windows. The same refusal is at `5b5f4336`, before dev's #814. A new table gives all four windows' figures at each stage setting. |

Also answered, with no commit: `[R759]` RES-2 and `[R760]` R2 (the stale sentence is gone from this body) and `[R760]` R3 (the generator's two commands are listed separately below, because `--selftest` returns before `--check` runs).

**No third stale figure.** Only `ctrl_split_boot` and `ctrl_service_budget` reach `split_soc.add_devices`. Every other figure the stage could move in those two READMEs is either dated to `e76a755a` with the "no SPI PHY stage" statement, or was re-run on this round's head with the same result: the `slow-adp-rx` control still measures 24.614 ms, `as-built` is still caught with cause 5 on the cacheless and the cached CPU, and each staged arm's table is byte-identical to the one published at `9f81df00`. No other document states these figures.

**The firmware digest.** `442da911` changes `sw/mailbox`, which the harness's `tree:firmware` digest covers, so `--reuse-build` refuses every earlier harness build. All six staged arms were therefore built and run again on this round's commits, and the digest does not cover the two READMEs, so those builds attest at the head (`--reuse-build --regrade`). No RTL or firmware source changed, so the firmware shards, LiteX simulations, BDD and native sweep were not re-run; their results below are from `9f81df00`.

## Authoritative references

- The owner branch policy (2026-10-26), recorded on #665.
- Rulings on #665: comment 6553999730 (option B, the contract version) and comment 6554243203 (option C, `reboot_req_o`).
- `docs/design/MAILBOX_SPLIT.md` ("Versioning", "Every port, one class", "Verification", "Open items"); `sw/mailbox/mailbox.yaml` (the history); `sw/mailbox/census_ports.py` (the classes and exclusions).
- dev-soft-core's #795 (the face block, contract 2.3) and #792 and #796 (the CPU budget harness); dev's #802 (#799), #822 (#787) and #826 (#814).

## How to get into the same state

```sh
git fetch origin
git switch --detach fa01979959ebff05af34f5a752408de7b3c41cf1
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

The pinned tools are those of `rtl-fast.yml` and `docs.yml`: CPython 3.12.3 with `ci/constraints-ci.txt`, Verilator 5.050, sv2v v0.0.12, Yosys 0.66, the RV32 SDK of `scripts/ci_rv32_sdk.py`. The LiteX simulations and the CPU budget harness use the LiteX revisions of `sw/litex/litex_pins.txt` with the product patches.

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/mailbox/publication_census.py --check --selftest --jobs 5
for k in 0 1 2 3; do python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $k/4; done
scripts/run_litex_sims.sh --selftest && scripts/run_litex_sims.sh <logdir>
python3 scripts/ci_builder_legs.py run 0 --receipt <dir>/builder-leg-0.json -- python3 sw/builder/test_builder.py --require-rv32
python3 scripts/ci_builder_legs.py run 1 --receipt <dir>/builder-leg-1.json -- python3 sw/builder/test_builder.py --require-rv32
(cd tests && behave --no-capture -f plain)
bash scripts/run_all_suites.sh <logdir> --wait --shard k/4   # k = 0 to 3
git diff --check 97aab1d0f28bd753a3e11df6278d5cac54f964dd fa01979959ebff05af34f5a752408de7b3c41cf1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir>/xip-4k --xip --fetch-l1 64x1 --record-budget-findings
```

and every step of `.github/workflows/docs.yml`. Expected: every command exits 0, but for the last, which exits 1 as `run.py` reports refused probes.

Results of the full bar on `9f81df00`, whose code this round does not change:

| Gate | Result on `9f81df00` |
|---|---|
| ctrl firmware suites, 4 shards with the mutant campaigns | rc 0 each |
| LiteX simulations | rc 0: 8 of 8, self-test 10 of 10 |
| rtl-fast bdd | rc 0: 14 features, 508 scenarios |
| native suite sweep, 4 shards | rc 0: 65 of 65 suites, 2,192,828 checks, 0 in-suite failures, 0 timed out |

Results on this round's head:

| Gate | Result on `fa019799` |
|---|---|
| mailbox generator, `--check --crosscheck` | rc 0: 0 findings |
| mailbox generator, `--selftest` | rc 0: 0 arms failed |
| publication census, `--check --selftest` | rc 0: 6 shapes, 246 checks, 0 failures; 219 ports (C 26, F 28, R 34, E 6, M 14, G 111); no G cone on the wire; 139 arms, 43 rules, none unproven |
| builder bank, legs 0 and 1 | rc 0 each; the union accepted by `docs-check` |
| docs workflow | rc 0: every step of the gate jobs; 43 source gates exactly once |
| `git diff --check` against the merge base | rc 0 |
| split boot, 1x1 and 8x8, staged and no-stage | rc 0 each: both boots pass, trace 18 of 18 equal; every restated cell checked against its run's log |
| split boot, `--native-controls` and `--self-test` | rc 0: 6 of 6 native controls, 2 of 2 plants caught |
| CPU budget harness, `--self-test` | rc 0: 0 failures |
| CPU budget harness, the six staged arms | built and run again: rc 0 at 1x1 cacheless and 1x1 32 KiB, rc 1 on the four arms with refused probes, as `run.py` reports a refusal; each table byte-identical to the one published at `9f81df00`; each build attests and regrades identically at the head |
| CPU budget harness, the 1x1, 4 KiB no-stage control | rc 1, as above; table byte-identical to the one published at `9f81df00` |
| CPU budget harness, controls | `slow-adp-rx` caught, 24.614 ms; `as-built` caught with cause 5 on both CPUs |

## Known limitations / out of scope

- The split line has no REBOOT carrier: `reboot_req_o`'s cone stops at `reboot_ctrl.reboot_req_i` until the placement switch gives REBOOT its carrier (the ruling expects a face-block level). The firmware's AECP owner does not serve REBOOT yet.
- The split platform has no PHY link service for #70's boot-path publication (ruling of comment 6553999730); the switch-over lane picks it up.
- The CPU budget harness's Results and instruction-cache figures other than the flash's stay those measured at dev-soft-core `e76a755a`, as their README states.
- The harness's `table.md` words a refused backlog window as "not run"; the README now says what that means. The grader's wording is unchanged here.
- No Vivado, hardware or bench run: the sync changes no synthesis input of a shipping configuration beyond dev's own merged changes.

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
