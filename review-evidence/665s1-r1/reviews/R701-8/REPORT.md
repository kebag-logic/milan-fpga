[R701] POSITIVE - exact head 614635b7f9aed7c9138aef53d0b93ca6030ae31e

# R701-8: internal cleared-context delta review of PR #795 (issue #665, lane S1), round 8

- **Head:** `614635b7f9aed7c9138aef53d0b93ca6030ae31e`, tree `7ad2d73e372b1adbff46fab44886bdd3941f139d`. This matches the PR's published head (`gh pr view 795`: `headRefOid`, base `dev-soft-core`, not draft).
- **Delta judged:** `0052e62e..614635b7`. That runs from the head R701-7 reviewed (NEGATIVE) to this head: six commits (`27c54171`, `c2c5abd2`, `0eda061a`, `bdad673a`, `124191ca`, `614635b7`) and ten files:
  - the CPU budget harness (`tb/verilator/ctrl_service_budget/`: `README.md`, `build.py`, `grade.py`, `run.py`, `scenario.py`, `selftest.py`, `selftest_mutants.py`, `split_soc.py`);
  - a comment in `sw/litex/ctrl_memory.py`;
  - two lines of `docs/design/SPLIT_CONTROL_MEMORY.md`.
- **Unchanged since earlier rounds:** No RTL, firmware, contract, generated file or CI file changes in the delta. The rest of S1's scope is byte-identical to `424b1489`, which R701-6 covered (POSITIVE). S2's merged files are byte-identical to `0052e62e`, which R701-7 covered.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items (pure wording) and four optional SUGGESTIONs are recorded below. R701-7-F1, R701-7-F2 and R701-7-W1 are resolved at this head.

## Scope reconstructed (public sources only)

- **Issue #665 body:** the split firmware behind the mailbox contract. The build switch's default stays all-fabric. Portable C. Each protocol's service-latency bound is tested.
- **Lane S1 assignment (issuecomment-6409739310):** census, contract 2.3, the face writer, tests, no datapath edit. The all-fabric export stays digest-identical and VERSION is unchanged. Rulings 6410169666, 6410301079 (all-fabric stays a supported placement), 6412739248 and 6425357821 (the one ledgered point, `8x8-two-interfaces`, at 57.5 RAMB36, used only by that point's measurement), and 6421238472 (only acknowledged state is visible).
- **This round's frozen items:**
  - **Round-8 assignment 6461128613** (answering R701-7):
    - F1: the harness names the ledgered point at 8x8/2if only; the default `add_ctrl_memory` still refuses; the comment wording is updated; the PR body states what `run.py --self-test` does not cover.
    - F2: every contract 2.3 port is connected as `CtrlMailbox` connects it; arm B is re-anchored; the README names its firmware head and its citations match.
    - W1 applied. Real builds at both points.
  - **Ruling 6461910715 (option (c)):** the harness's SoC pulses `fw_ack_p_i` at the contract bound, taken from the generated constant, not a literal, with every other face input idle by name. The README and PR body state this one difference and why. Real builds at both points, arms A and B, are compared with S2's figures.
  - **Ruling 6463964028:**
    - Item 1: the `as-built` control accepts cause 1 or 5, with a planted control showing that a clean image still escapes. "No other change".
    - Item 2: the PR body states arm B's SET_CONFIGURATION 1x1 miss and 8x8 ceiling excess, with #801 as the cause.

## Independent pass over the delta (before reading any prior finding)

| Area | Code at head | What I checked | Result |
|---|---|---|---|
| Acknowledgement model | `split_soc.py:207-218` `slowest_ack`; `:262-266` `face_ack_cycles`; `:269-279` `_CommitBench`; `:282-325` `ack_deviations`; `:427-429` refusal before the SoC build | Read against `KL_mbx.sv:485-496` (`face_commit`: an ack clears `fw_busy_r`; GO while busy is refused by `face_refused_w`, `:353`), `:648` (`fw_send_o = fw_busy_r`), `mailbox.yaml:443,463` ("within ack_cycles clk_i cycles", 64), and `mbx.c:281-296` (the firmware polls `F_STATUS.BUSY` `MBX_FACE_ACK_CYCLES + 1` times, at one bus read or more each). Then my own probe `scripts/probe_ack.py`, which runs `ack_deviations` on the head and on 7 planted defects. | **Holds.** The head gives no deviation. Each planted defect is refused with the deviation named: ack one cycle early, one cycle late, immediate, interface 1 never acknowledged, interfaces swapped, counter not re-armed, and a bound that differs from the firmware's (`receipts/probe-ack.txt`). An ack at rise + 64 sits at the bound, so it is "within" the contract. The ack and `KL_mbx` share one clock, so there is no crossing. |
| Face ports | `split_soc.py:240-259` `FACE_IDLE_INPUTS`, `face_ports` | My probe at 1 and 2 interfaces. My own 8x8 build's `verilate.log`. | 19 inputs held idle by name and 58 outputs; `fw_send_o` is 1 and 2 bits wide. The only PINMISSING pins in my 8x8 build are the CPU's `dma_bus_awregion`/`arregion`. No mailbox pin is missing. |
| PINMISSING refusal | `build.py:361-385` | My probe `scripts/probe_pinmissing.sh` feeds a LiteX-shaped top through the pinned Verilator 5.050 and through the PATH Verilator 5.052. | The parser names exactly the two planted mailbox pins and ignores the non-mailbox pin, under both versions (`receipts/probe-pinmissing.txt`). It fails open if the message format changes (S-1 below). |
| Ledgered point | `build.py:134-143` `LEDGERED_POINTS`, `:162-166`, `:452`; `split_soc.py:404-411` `ledgered_plan`, `:440-441`; comment `ctrl_memory.py:196-205`; `SPLIT_CONTROL_MEMORY.md:94-95` | Real builds at this head (below). `test_ctrl_memory.py` at this head. | 8x8/2if: `soc.json` names `8x8-two-interfaces`, plans 57.5, and the run gets past `image.log`, the SoC export, Verilator and `make`. 1x1 names none. `test_ctrl_memory.py`: 0 failures. Its `:50` check shows the SoC build's default `add_ctrl_memory` refusing the ledgered image at 57.5 (`receipts/test-ctrl-memory.txt`). The comment and doc wording follow ruling 6461128613 item 1. |
| Arm B re-anchoring | `build.py:59-87` `VARIANTS['answering-ports']` | Read against `ctrl_aecp_image.c:60-99` and `aecp_face.c:254-260` (`aecp_face_init` fills `ports`; the core takes `&image_face.ports` after it). The self-test's `build_checks` applies every arm and plant to the checkout. | Holds. The face's `stream`, `avb` and `counters` are replaced before `ctrl_app_compose_aecp`. `path` answers through the fixture's `a_path`. `format`, `changed` and `applied` stay the face's. |
| `as-built` control | `run.py:259-277` (`AS_BUILT_CAUSES`, `as_built_faults`, `verdict`); `selftest.py:671-693`; `selftest_mutants.py:401-408`; `scenario.py:928-934` | Self-test, plus my own real run at 1x1. I disassembled my built ELF and read `sim_main.cpp:259-263`. | Caught at this head: `TRAP 166 0 5 00000020`, rc 0, 18 s (`receipts/asbuilt-control-1x1.txt`). The regex matches the cause as a whole field with interrupt bit 0. My ELF is byte-identical to the author's (`fe939fff...`). The disassembly shows `lw t3,0(t0)` at 0x24 loading from `_fdata_rom` = 0x197b0 (bit 15 set). The trap line's last field is `last_pc_`, the last committed PC, so its 0x20 is the `bgeu` before the faulting load. The README's `:546` "lw at 0x24" is correct. Two prose places blur this (W-1, W-2). |
| Measurement claims | README `:46-52`, `:202-206`, `:693-697`; PR body `:24`, `:205-207` | My own real arm A `aecp` runs at this head. | 1x1/1if: 25 of 25 probes, 0 misses, rc 0, 209 s. 8x8/2if: 39 of 39 probes, 0 misses, rc 0, 378 s. Both `table.md` files are **byte-identical** to the author's published A1/A8 tables (`3a9094ed...`, `c77c89dc...`). The author's one-cycle-probe comparison (`compare/aecp-*-vs-probe1.md`, 64 of 64 rows +0.000 ms / +0 accesses) supports README `:697` ("identical figures"). |
| README citations | `MAILBOX_SPLIT.md:499-506`, `:506`, `:649-661`, `:757-762`; `aecp.c:66`, `aecp_commands.c:593`, `aecp.c:535-569` | Read at this head. | Each resolves to the cited rows or code (`retry_at = a->now + 1u` is at `aecp.c:569`). |
| Comment rule | Added lines in `*.py`, `*.c`, `*.h`, `*.sv`, `*.cpp`, `*.S` in the delta | Grepped for lane labels, bench labels, rounds, reviewer IDs and comment IDs. | No new instance. The only match, "around", is a false positive. |
| "No other change" (ruling 6463964028) | `git diff --stat bdad673a 614635b7` | Listed the files. | Five harness files only: `README`, `run.py`, `scenario.py` (docstring), `selftest.py`, `selftest_mutants.py`. |

## Findings

### R701-8-W1 - RESIDUE - Docs - PR #795 body, Known limitations, the `as-built` bullet (`:225`)

- **Text:** "At this head it is the start code's first `.data` copy load (pc 0x20); ... The trap line in the driver log names the address."
- **Evidence:**
  - The faulting load is the `lw` at 0x24. My disassembly of the 1x1 ELF, which is byte-identical to the author's, shows `24: lw t3,0(t0)` with `t0` = `_fdata_rom` 0x197b0.
  - `sim_main.cpp:262-263` prints `last_pc_`, the last committed instruction (the `bgeu` at 0x20), not the faulting address or the data address.
  - The README's own `:546` says "`lw` at 0x24".
- **Exact fix:** "At this head it is the start code's first `.data` copy load (`lw` at 0x24, reading 0x197b0); in S2's firmware it was a call to 0xb1ec (cause 1). The trap line in the driver log names the cause and the last committed PC (0x20 here, the instruction before the faulting load), not the faulting address."

### R701-8-W2 - RESIDUE - Docs - `tb/verilator/ctrl_service_budget/README.md:681`

- **Text:** "...caught with a load access fault, cause 5, at the start code's first `.data` copy load (`TRAP ... 0 5 00000020`)..."
- **Evidence:** The parenthesis reads as if 0x20 were the load's address. It is the last committed PC (see W1). `:546` gives the load as 0x24.
- **Exact fix:** "...at the start code's first `.data` copy load, the `lw` at 0x24 (`TRAP ... 0 5 00000020`; the trap line's last field is the last committed PC, the `bgeu` before it)..."

### SUGGESTIONs (optional)

- **R701-8-S1 - Tests, Robustness - `build.py:361-369`, `split_soc.py:249-259`, `:282-325`.** No standing self-test or mutant covers the three build-time guards this delta adds:
  - `ack_deviations`;
  - `mailbox_pins_missing`;
  - `face_ports`'s idle-input refusal.

  The PR body (`:193`) says so, and the author's one-off planted builds (`plant-ack-early`, `plant-ack-probe`) plus this review's probes show the guards refuse what they should. But a later edit that made `ack_deviations` return `[]`, or that broke the PINMISSING regex, would pass silently. `mailbox_pins_missing` fails open: if Verilator's wording changes, the regex matches nothing and the build proceeds. Two cheap additions would close this, and neither needs a build:
  - a self-test check that runs `ack_deviations` on the head and on one planted `slowest_ack`, which takes about 1 s in migen (`scripts/probe_ack.py` is a template);
  - a recorded PINMISSING fragment parsed to its expected pins.

  Optionally, the build could also refuse when the log carries a `PINMISSING` line the parser cannot read.
- **R701-8-S2 - Docs - `build.py:113-114`** (pre-existing code, which the new mutant `selftest_mutants.py:423` now relies on). `variant_fixture` reports "an anchor is not unique" when an anchor is **absent** (count 0). That is the message the earlier-rule arm-B mutant prints. "An anchor does not occur exactly once" would be accurate.
- **R701-8-S3 - Docs - PR body `:191`.** "...were not run again: neither changes a file they read" has no clear subject for "neither". Write "neither the merge nor round 8 changes a file they read".
- **R701-7-S1 (carried) - Docs - `sw/firmware/ctrl/test/ctrl_configs.py:180`.** This still reads "(#665 S1)" in a runtime classification string. It is optional, since runtime strings fall outside the comment rule.

## Prior findings at this head

| Prior item | Disposition at `614635b7` |
|---|---|
| **R701-7-F1** (MAJOR; Conformance, Tests, Docs): the harness could not build its 8x8 point | **Resolved.** Ruling 6461128613 decided that the harness's 8x8/2if build is "that point's measurement". `LEDGERED_POINTS` names it at `(endstation_ax7101_8x8, 2)` only (`build.py:138`), for the image (`:162-166`) and the SoC plan (`split_soc.py:440`). The self-test check and mutant (`selftest.py:750-771`, `selftest_mutants.py:421`) keep it at that point. My own `run.py --point 8x8` at this head gets past `image.log` and the SoC export and measures 39 of 39 (`receipts/armA-aecp-8x8.txt`, `soc.json ledgered: True`). `test_ctrl_memory.py` still refuses the ledgered image through the default `add_ctrl_memory` (`receipts/test-ctrl-memory.txt:50`). The comment (`ctrl_memory.py:198-201`) and the doc (`SPLIT_CONTROL_MEMORY.md:94-95`) no longer contradict the harness. The PR body states what the self-test does not cover (`:193`). |
| **R701-7-F2** (MINOR; RTL, Tests, Docs): the harness was not adapted to contract 2.3 or to S1's fixture | **Resolved.** Every face port is connected through `ctrl_mailbox_face_ports`, with inputs idle by name and refused unless they equal `CtrlMailbox`'s. The one exception, the commit acknowledgement at the contract's bound, was ruled under option (c) and is stated in README `:46-52`, `:96-108` and PR body `:21`, `:213`. My 8x8 build has no mailbox PINMISSING, and the build now refuses one. Arm B is re-anchored, and the self-test proves its anchors apply. The README names the firmware of its figures (`:202-206`), uses past tense for `e76a755a`, and its citations resolve at this head. |
| **R701-7-W1** (RESIDUE; retains R701-6-W1): the PR body's "change no file the following gates read" | **Resolved.** The sentence is gone. The rewritten paragraph (`:191`) makes no claim about `mailbox.yaml`. Its wording nit is S3 above. |
| R701-7-S1 | Carried (above). |
| R701-7-S2 (merge rounds should run the harness's build step) | Followed in practice this round: real builds at both points, in both arms. Carried as guidance. |
| R701-5/R702-5 F1-F3, R701-4/R702-4 and earlier findings | **Remain resolved.** The delta touches none of their causes (firmware, RTL, contract and tests unchanged since `424b1489`). |
| R701-6-S1 to S4, R701-5-S1/S2/S4, R701-4-S1/S2, R702-6 SG1-SG4 (SUGGESTION) | Carried, unchanged. The delta touches none of their files except `SPLIT_CONTROL_MEMORY.md:94-95`, which is not R701-6-S3's line `:188`. |

## Published evidence verified

- **Evidence tree:** `af4490faf13cf56cb76de0c9c750ab79f80c4dd5`, `review-evidence/665s1-r1/author-r8/{a680j,a680k}`.
- **Signatures:** The commit is unsigned, and so is the PR head (GitHub `verification.reason = unsigned`). Integrity therefore rests on `MANIFEST.json`.
- **Manifest check:** `scripts/verify_author_receipts.py` fetched 39 receipts. All 39 match `published_sha256`, with 0 mismatches (`receipts/author-receipts-verified.txt`). They are:
  - harness self-test, docs gates, firmware-boundary, behave;
  - the `as-built` run and its planted clean-image run;
  - the A1/A8/B1/B8 run summaries;
  - three acknowledgement comparisons;
  - the PR body.
- **Heads of the receipts:**
  - `gates/harness-selftest.txt.head` and `docs-gates.txt.head` name `614635b7` (clean).
  - The `as-built` runs are at `124191ca`. `614635b7` changes only the README.
  - The A/B runs are at `0eda061a`. Since then only `README`, `run.py` (verdict for `as-built`), `scenario.py` (docstring) and the self-test have changed. My own A1/A8 at `614635b7` reproduce their `table.md` byte for byte.
- **Spot-checked:**
  - Author harness self-test: 91 PASS, 68 mutants caught, 0 failures. Reproduced by mine, with the same counts (`receipts/harness-selftest.txt`).
  - Docs gates: 70 `rc=0` lines, none non-zero. `check_em_dash` reports 0 findings over 1,903 added lines (`e76a755a..HEAD`).
  - `firmware-boundary`: `ctrl_boundary: PASS`, rc 0.
  - `behave`: 1,977 steps passed.
  - Planted clean image: boots with no trap, reaches `aecp_image_load` (0xbbc4) by 7 ms, and the run prints ESCAPED, rc 1.
  - B1: 4 of 14 instances miss, rc 0. B8: 22 of 22 miss, rc 0. Both match the PR body `:206`.
- **Hosted at exact head:** snapshot in `receipts/hosted-checks-614635b7.tsv`. 8 success and 1 skipped. 20 were in progress and 14 queued at the time, including `publication-census`, `firmware-boundary` and Verilator shards. I make no claim on hosted or act acceptance; the manager owns it.

## Lens results

```text
[R701] PASS Conformance - split_soc.py:207-218,262-266,282-325,427-429; build.py:134-143,162-166,452; run.py:259-277; ctrl_memory.py:196-205; SPLIT_CONTROL_MEMORY.md:94-95; PR body :21,:193,:206,:221-223; receipts/probe-ack.txt, armA-aecp-8x8.txt, test-ctrl-memory.txt - checked against round-8 assignment 6461128613 (F1, F2, W1), ruling 6461910715 items 1-4 (bound from the generated constant FACE_ACK_CYCLES = mailbox.yaml ack_cycles 64, "within" per mailbox.yaml:443,463, other inputs idle by name), ruling 6463964028 items 1-2 (causes 1|5, planted clean control escapes, "no other change" = five harness files), and rulings 6412739248/6425357821 (ledgered point at its measurement only, default path refuses). No product file other than a comment changed, so the all-fabric export, VERSION and contract are untouched.
[R701] PASS RTL - split_soc.py:207-218 (slowest_ack), :269-279 (_CommitBench) against hdl/milan/mailbox/KL_mbx.sv:353,485-496,648 and sw/firmware/ctrl/mbx/mbx.c:281-296; my 8x8 verilate.log; receipts/probe-ack.txt - the ack is a one-cycle pulse at rise+64 in KL_mbx's clock domain (no crossing). KL_mbx clears busy on it, and a GO while busy is refused, so the bench's ack-first priority is equivalent. The firmware's poll window (65 bus reads) covers the bound. Every face port is connected, at 1 and 2 interfaces. No HDL changed in the delta.
[R701] PASS Robustness - receipts/probe-ack.txt (7 planted ack defects refused: early, late, immediate, missing interface, swapped, never re-armed, bound != firmware), probe-pinmissing.txt (parser under Verilator 5.050 and 5.052), harness-selftest.txt (as-built: clean boot, causes 2/7/15, interrupt 5 and bus error escape; ledgered name at no other shape or interface count) - back-to-back and overlapping commits, configuration-dependent paths (1 vs 2 interfaces, ledgered vs not) and the clean-image control all behave. The fail-open PINMISSING parse is optional hardening (S1).
[R701] PASS Tests - selftest.py:671-693,750-776; selftest_mutants.py:401-408,421-426; receipts/harness-selftest.txt (91 PASS, 68 mutants caught), asbuilt-control-1x1.txt, armA-aecp-1x1.txt, armA-aecp-8x8.txt - the new checks can fail for their defects (each mutant caught). The real builds reproduce the author's published tables byte for byte at both points, and the as-built control is caught at this head. The guard self-tests that are missing (S1) are disclosed in the PR body and do not hide a defect.
[R701] PASS Docs - tb/verilator/ctrl_service_budget/README.md:41-52,96-108,202-206,546,681-697; ctrl_memory.py:196-205; SPLIT_CONTROL_MEMORY.md:94-95; PR body :21,:24,:191-193,:205-225 - checked against the code at this head, my disassembly and runs, and the rulings. Citations resolve, the firmware head of each figure is named, and the one SoC difference and the #801 rows are stated. No lane label appears in new source comments. Two wording slips are RESIDUE (W1, W2), and they leave the lens clean under the owner rule.
```

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Rulings 6461128613, 6461910715, 6463964028, 6412739248, 6425357821 against `split_soc.py`, `build.py`, `run.py`, `ctrl_memory.py` comment, `SPLIT_CONTROL_MEMORY.md:94-95`, PR body; `receipts/probe-ack.txt`, `armA-aecp-8x8.txt`, `test-ctrl-memory.txt` | R701-8 | 614635b7f9aed7c9138aef53d0b93ca6030ae31e |
| RTL | CLEAN | `KL_mbx.sv:353,485-496,648`, `mbx.c:281-296`, `mailbox.yaml:443,463` against `split_soc.py:207-325`; face ports at 1/2 interfaces; my 8x8 `verilate.log` | R701-8 | 614635b7f9aed7c9138aef53d0b93ca6030ae31e |
| Robustness | CLEAN | `receipts/probe-ack.txt`, `probe-pinmissing.txt`, `harness-selftest.txt`, `asbuilt-control-1x1.txt`; author's planted clean-image run | R701-8 | 614635b7f9aed7c9138aef53d0b93ca6030ae31e |
| Tests | CLEAN | Harness self-test and mutants (mine and the author's); real arm A `aecp` builds at 1x1 and 8x8 and the `as-built` control at 1x1 (mine); author's B1/B8 and compare receipts; `test_ctrl_memory.py` | R701-8 | 614635b7f9aed7c9138aef53d0b93ca6030ae31e |
| Docs | CLEAN (W1, W2 RESIDUE) | Harness `README.md`, `ctrl_memory.py` comment, `SPLIT_CONTROL_MEMORY.md`, PR body; `receipts/docs-gates.txt` (docs_check, doc paths, doc style, py idiom, hygiene, bare-metal scope, TODO ownership, feature status, `git diff --check`: all rc 0); author's docs-gates receipt for `check_em_dash` | R701-8 | 614635b7f9aed7c9138aef53d0b93ca6030ae31e |

**Basis for the rest of the PR's scope:**

- S1's own artifacts outside this delta are byte-identical to `424b1489`: census, contract 2.3, `KL_mbx`/`KL_mbx_evt`, `CtrlMailbox`, the face writer, the AECP core, the planner's logic and its tests. R701-6 covered all five lenses clean at `424b1489`, an ancestor of this head. Nothing in those lenses' scope has changed since, apart from the delta reviewed here.
- S2's merged files are byte-identical to `0052e62e`, apart from this delta's harness edits, which are reviewed here.
- The ledger above applies to the whole PR at `614635b7`.

## Real limits

- **No manager source bank at this head.** I claim none and infer none. Source-head execution evidence is the author's published receipts plus this review's focused runs.
- **Not re-run here (author receipts relied on):**
  - firmware self-test shards, `fw_coverage.py`, `test_builder.py`, `test_ctrl_nvm.py`;
  - `ctrl_boundary` legs, `behave`, the four-shard Verilator sweep;
  - linked images at four points, `gen_mailbox.py --check`;
  - arm B runs, `slow-adp-rx`;
  - the full docs workflow.

  `slow-adp-shutdown` is not run at this head by anyone. The README states this.
- **`check_em_dash.py`** could not run here: the pinned Markdown renderer is not installed, and installing it is not allowed. A direct scan finds 0 em dashes in the delta's added lines. The author's receipt at this head reports 0 findings.
- **The harness's acknowledgement is a model of the slowest datapath the contract allows**, not a datapath. Window requests are never answered, so the measured figures cover the CPU budget with every window read at its timeout. Physical calibration is NOT RUN, and field skips are not hardware proof.
- **The `as-built` control** now accepts any cause-5 load access fault. A load fault from another cause would also count as caught. The ruling accepted this (option (a)), and the PR body states it as a limit.
- **Hosted checks** were still running at snapshot time.
- **Final candidate:** the current-dev merge candidate (source base `e76a755a`, live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`) was not built here.

## Pending manager duties

- Hosted and act acceptance at the exact head, separating executed jobs from skipped contexts.
- Build and validate the current-dev merge candidate (builder and native banks), and link its receipts on the PR.
- Carry R701-8-W1 (PR body) and R701-8-W2 (README) to the residue checklist. S1-S3 and the carried R701-7-S1 are optional.
- The second positive review (external) and the full completion bar remain. Merge only on explicit maintainer authorization.

R701-8 FINISHED
