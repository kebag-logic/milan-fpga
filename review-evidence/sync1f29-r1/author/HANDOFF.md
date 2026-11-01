# [A723c] HANDOFF: sync dev 1f29f189 into dev-soft-core (resume after two STOPs)

**Status: REVIEW READY at `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1`.** Every assigned gate exits 0 on that head (section 6). Local only: nothing is pushed, and no PR is open. Both remote tips were unchanged at the end: dev `1f29f189`, dev-soft-core `5b5f4336`.

- Lane: `$LANES/sync-dsc-1f29f189`, branch `sync-dev-1f29f189-into-dev-soft-core`, local only.
- Start head: the merge commit `97e9a3d3` (parents dev-soft-core `5b5f4336`, dev `1f29f189`); kept as made.
- Rulings: (B) issuecomment-6553999730 on the [A723] STOP; (C) issuecomment-6554243203 on the [A723b] STOP.
- TAKEN: issuecomment-6554259067.
- Conflict table and merge resolution: section 2, carried from `../sync-a723b/HANDOFF.md`.
- REVIEW READY: issuecomment-6556811075.
- Scratch: `$VALIDATION_STORAGE/sync-a723c` (`bin/` holds the runners; `final/` the gate logs; `budget/` and `budget-final/` the harness arms; `native/` the sweep). The shards' clones are `$LANES/sync-a723c-shard{0..3}`. Submodules initialised in the lane: `third_party/verilog-axis`, `protocol-processor`, `gptp-processor`, `third_party/tsn-c-stack`, `third_party/lwSRP`; `external` not.

## 1. Commits

| # | SHA | Subject | What |
|---|---|---|---|
| 0 | `97e9a3d396ec2d35b907f7c5c47823fbfcee6458` | Merge dev 1f29f189 into dev-soft-core (sync) | the merge, kept as made in round 2 (resolution, contract 2.4, the four generated outputs) |
| 1 | `5d22d4fbc30c2524fdac98ad3557cdd83ee36540` | Classify the wrapper's two new ports in the port census: ... (#665, #787) | ruling (C): `src_stream_id_o` class C; `reboot_req_o` class G, its cone stopped at `REBOOT_TERMINAL` (`reboot_ctrl`, `KL_reboot_ctrl`, `reboot_req_i`), the arm "the REBOOT request read past its terminal" (a probe on `pp_reboot_req_w`, refused by `g-on-wire`); the census report's `reboot` terminal count; `MAILBOX_SPLIT.md` "Every port, one class" (219 ports, C 26, G 111, the REBOOT exclusion as a placement-switch acceptance item, 19 port plants), its contents line and an open item |
| 2 | `30973ef5f1180f68e65048617937be6423f6ee8a` | Restate dev's living citations of the source entries as contract 2.4 ... (#665, #799) | the 11 citations (section 3 item 2) |
| 3 | `7333801943dccd94c3b85a0629b7ba0cee1f7f5e` | Connect KL_mbx's pub_src_sid_o in the CPU budget harness's own mailbox ... (#665, #799) | semantic conflict found in this round (section 3 item 3) |
| 4 | `fab0be5b0e683ea2f984a59c1d782142cfb75121` | Emit the contract reference's face-block sections from their own function ... (#665) | semantic conflict found in this round (section 3 item 4) |
| 5 | `dcd567038d4069a9b3f8f44ce6c6285a4368192c` | Stage the CPU budget harness's LiteSPI PHY as MilanSoC stages every SoC since #814 ... (#665, #814) | section 3 item 5 |
| 6 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` | Restate MAILBOX_SPLIT.md's verification figures at the merged head ... (#665) | section 3 item 6 |

All commits: one-line subject, no body, no trailers.

## 2. Conflict table

As resolved in the merge commit `97e9a3d3` (round 1's saved resolution, re-applied byte for byte in round 2, plus the (B) ruling's version). Carried unchanged from `../sync-a723b/HANDOFF.md` section 2.

Line numbers are in the conflicted merge tree (markers at the same lines in both rounds). dsc = dev-soft-core. Every textual conflict is #795's contract 2.3 face block against #802's contract 2.3 source entries.

| File:line | dsc side (commit) | dev side (commit) | Resolution, and why |
|---|---|---|---|
| `sw/mailbox/mailbox.yaml:63-83` | history "Minor 3 (#665)": the face block (`05d0b575`, wording `ecfb432e`) | history "Minor 3 (#799...)": the source entries (`3b42bcf2`, reflow `4f3ebffb`) | Both entries, dsc first. Per the (B) ruling, dsc's stays **Minor 3**. dev's becomes **Minor 4** ("a firmware built against 2.3 leaves them at 0"), with a note that dev added them as its own minor 3 over 2.2 and reaches 2.4 by adding the face block (ruling comment 6553999730). `version.minor` (auto-merged `3`) is set to **4**. |
| `sw/mailbox/gen_mailbox.py:86-91` | `SV_REG_REF` adds `FACE_REG`, `FACE_SRC_REG`, `FACE_SNK_REG` (`05d0b575`) | `SV_REG_REF` adds `PUB_SRC_REG` (`3b42bcf2`) | One regex that names every block's decode, so the crosscheck sees both blocks. |
| `sw/mailbox/gen_mailbox.py:135-141` | `every` adds the three face register lists (`05d0b575`) | `every` adds `pub_source_registers` (`3b42bcf2`) | Union in contract order: publication registers, sources and sinks, then face, then channel. |
| `sw/mailbox/gen_mailbox.py:285-306` | 5 face output arms (`05d0b575`) | 3 source-entry output arms (`3b42bcf2`, split `41a78877`) | Both lists: 35 output arms, each caught. |
| `sw/mailbox/gen_mailbox.py:372-407` | 11 face contract arms (`05d0b575`) | 6 source-entry contract arms (`3b42bcf2`, `41a78877`) | Both lists: 49 YAML arms, each refused. |
| `sw/mailbox/mailbox_skeleton.py:641-647` | `face.check(contract)` (`05d0b575`) | source stream_id whole-word check (`3b42bcf2`) | Both: dev's publication check beside the sink check it mirrors, then the face check. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:670-708` | 6 model face mutants (`717f8cc6`) | 2 model source-entry mutants (`3b42bcf2`) | Both lists. |
| `sw/litex/milan_soc.py:2917-2928` | CtrlMailbox docstring: the face block's outputs unread, answers held idle (`05d0b575`) | the same docstring: each source's stream_id unread (`3b42bcf2`) | One docstring that states both. The code auto-merged with both port sets (`o_pub_src_sid_o`, `ctrl_mailbox_face_ports`). |
| `tb/verilator/mbx/README.md:126-132` | F0 to F10 and T0 to T2 rows; P0 to P5 as at the base (`4ed323fb`) | P0 to P5 restated with the source entries (`3b42bcf2`) | dev's P row, then dsc's F and T rows. |
| `docs/design/MAILBOX_SPLIT.md:1343-1349` | census and mbx suite rows with the port census and face figures (`4ed323fb`, `4903da07`) | the same rows with the source-entry figures (`3b42bcf2`, `f87da064`) | dsc's rows as text. The figures are re-measured after the ruling (section 5). |
| `docs/design/MAILBOX_SPLIT.md:1354-1361` | face block row; host-model row with dsc figures (`4ed323fb`, `4903da07`) | publication row with the source entries; host-model row with dev figures (`3b42bcf2`) | dev's publication row, dsc's face row, dsc's host-model row. The figures are re-measured (section 5). |
| `docs/design/MAILBOX_SPLIT.md:1573-1610` | the face block's out-of-context measurement, 5,515 LUT and 7,632 FF (`7464b876`) | "the sixteen source entries ... were not measured with this recipe" (`3b42bcf2`) | Both paragraphs, dsc's first. Each stays true of what was measured. |

Also in the saved resolution (an auto-merged line, corrected in the merge): `MAILBOX_SPLIT.md:97`. The self-test counts "(32 arms) ... (43 arms)" became "(35 arms) ... (49 arms)", the merged generator's own counts.


## 3. Semantic-conflict list

The files both sides changed since `97aab1d0` are listed in `../sync-a723b/HANDOFF.md` section 3 (24 files). Rounds 2 and 3 found these, each fixed in its own commit after the merge:

1. **The port census against dev's two new wrapper ports** (`sw/mailbox/census_ports.py` against `hdl/milan/KL_pp_shadow.sv`, ports added by #802 for #799 and by #822 for #787). The census failed on the merge (3 findings, every shape). Fixed in commit 1 under ruling (C).
2. **dev's living "2.3" citations of the source entries**, which this line numbers 2.4 under ruling (B). Fixed in commit 2, 11 places:
   `CHANGELOG.md:172`; `docs/reference/SUBMODULES.md:288`; `docs/design/MAILBOX_SPLIT.md:820`, `:1349` (the publication-block row; now `:1362`) and `:1595`; `sw/firmware/ctrl/test/ctrl_mutants.py:697`; `sw/litex/milan_soc.py:2917`; `tb/verilator/mbx/README.md:126` and `:330`; `tb/verilator/mbx/mutants.py:478`; `tb/verilator/mbx/suite.hpp:1710`.
   Kept as measured (dated records of dev's measurement at lane head `8b76de69` on dev `97aab1d0`, which carried 2.3): `docs/design/AREA_BUDGET.md:536` and `:541`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:22`, `:45` and `:61`, and the three `"measured"` strings of `syn/ooc/pp_resource_baseline.json`. This line's own "contract 2.3" citations name the face block, minor 3, and are unchanged.
3. **The CPU budget harness's own `KL_mbx` instance against dev's `pub_src_sid_o`** (`tb/verilator/ctrl_service_budget/split_soc.py` `unread_publication`, against #802's port in `KL_mbx.sv` and `CtrlMailbox`). Found in this round: the harness build refused, `the mailbox instances leave ports unconnected (verilate.log, PINMISSING): ['KL_mbx.pub_src_sid_o']`. `CtrlMailbox` auto-merged with the port; the harness restates `CtrlMailbox`'s publication outputs and did not. Fixed in commit 3: the port is named and unread, as `CtrlMailbox` leaves it; the harness README's mailbox paragraph says so.
4. **Rule 12's 100-line limit against the merged `emit_doc`** (`sw/mailbox/mailbox_emit.py`). dsc's face block (`05d0b575`) added its three register sections, windows and COUNTERS_CHANGED table to `emit_doc`, and dev's source entries (`3b42bcf2`) added the publication-source section. Each side kept the function within 100 lines; merged it is 104, so the docs workflow's Python idiom gate failed on the merge (`long function 10 > ratchet 9`, `scripts/py_idiom.budget`). Found in this round. Fixed in commit 4: the face block's sections move to `_face_sections`, unchanged; `gen_mailbox.py --check --crosscheck` rc 0 (the generated outputs are byte-identical) and `check_py_idiom.py` rc 0 (`long function: 9 <= 9`).
5. **The S2 service-budget harness against #814's `SPIPHYStage`** (`tb/verilator/ctrl_service_budget/split_soc.py` `add_devices`, against `milan_soc.MilanSoC.add_spi_flash`, `sw/litex/milan_soc.py:3871`). The harness built LiteSPI over its `FlashBoundary` with no stage, so its README's "the address does not change an access's cost" no longer held for the flash. Fixed in commit 5: `phy = milan_soc.stage_spi_phy(FlashBoundary(...))`, the claim corrected, and the flash-window, refill and XIP arms re-measured (section 5).
6. **`MAILBOX_SPLIT.md` verification figures.** Fixed in commit 6, from this head's own runs: census 41 reads of 22 of the 26 class-D nets, 4 unread, 219 ports (C 26, F 28, R 34, E 6, M 14, G 111), 139 arms (118 + 19 + 2), 43 rules (31 + 12); mbx 525 and 570 at one interface, 532 and 577 at two (45 handshake checks each way); host model 490 of 532. The census section's own counts moved in commit 1. Checked and already right: "26 population nets ... 41 reads ... 11 on the wire, 14 CSR status, 16 the answer face" (`:995`, against `publication_census.py --list`: 11 field, 14 status, 16 processor rows); the generator's "35 arms ... 49 arms" (`:97`).

Checked, no stale rule (round 2): `MARK_II_AREA_PLAN.md` against #818's WNS gate; the #814 DRAM-side cuts (the split harnesses build with `with_dram=False`); `scripts/port_docs.budget`. The split boot harness builds through `CtrlMailbox` and `with_spiflash=False`, so neither item 3 nor item 4 reaches it.

## 4. Regeneration list

| Commit | Generator | Outputs changed | Check |
|---|---|---|---|
| merge `97e9a3d3` | `gen_mailbox.py --write`, after `minor: 4` | `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` (`KL_mbx.sv` unchanged) | `--check --crosscheck --selftest` rc 0, 35 output arms, 49 contract arms |
| `fab0be5b` | none needed: `emit_doc` refactored | none: `gen_mailbox.py --check --crosscheck` rc 0, so every generated output is byte-identical | as left |

Tables of contents: no heading was added. `gen_toc.py --check` rc 0. The one contents description changed (`MAILBOX_SPLIT.md`, "The processor's other faces") is the human-owned part of the entry. Diagrams and records: no generator input changed; the docs gates' no-drift checks are in the gate table.

## 5. Harness measurements (commit 5)

All at this head's firmware; `run.py --point P --build-dir B [--xip] --fetch-l1 G --record-budget-findings`, product LiteX tree, pinned Verilator 5.050, pinned RV32 SDK. Three sets:
- **staged**: the harness with `stage_spi_phy` (the head).
- **no stage**: the same tree without that line (run from a clean clone of `fab0be5b`), the control that isolates the stage.
- **dsc tip**: dev-soft-core `5b5f4336`, before the merge, for three arms.

| Arm | CPI | Flash window load, mean (range) | Refill, mean (range) | Groups, refused | Paths (instances) missing T_svc | Composed max, ms | Released only, ms | Worst pass, ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 none, staged | 9.42 | 266.1 (139-307) | n/a | 18, 0 | 20 of 81 (55 of 141) | at least 31.81 | 14.94 | 31.81 |
| 1x1 none, no stage | 9.42 | 262.9 (138-303) | n/a | 18, 0 | 20 of 81 (55 of 141) | at least 31.82 | 14.94 | 31.82 |
| 8x8 none, staged | 9.39 | 265.8 (139-307) | n/a | 17, 2 | 58 of 127 (100 of 180) | at least 44.49 | 24.84 | 59.89 |
| 8x8 none, no stage | 9.39 | 262.5 (138-303) | n/a | 17, 2 | 58 of 127 (100 of 180) | at least 44.50 | 24.84 | 59.08 |
| 8x8 none, dsc tip | 9.39 | 262.5 (138-303) | n/a | 17, 2 | 58 of 127 (100 of 180) | at least 44.50 | 24.84 | 59.08 |
| 1x1 XIP 4 KiB, staged | 35.53 | 265.4 (139-318) | 2,218 (2,122-2,292) | 16, 5 | 69 of 76 (104 of 116) | at least 87.17 | none | 87.17 |
| 1x1 XIP 4 KiB, no stage | 35.24 | 262.1 (138-314) | 2,201 (2,106-2,273) | 16, 6 | 68 of 75 (106 of 115) | at least 86.54 | none | 86.54 |
| 1x1 XIP 4 KiB, dsc tip | 35.24 | 262.1 (138-314) | 2,201 (2,106-2,273) | 16, 6 | 68 of 75 (106 of 115) | at least 86.54 | none | 86.54 |
| 1x1 XIP 32 KiB, staged | 13.28 | 265.4 (139-318) | 2,239 (2,122-2,292) | 18, 0 | 23 of 81 (67 of 141) | at least 32.05 | 23.56 | 33.36 |
| 1x1 XIP 32 KiB, no stage | 13.21 | 262.1 (138-314) | 2,221 (2,106-2,273) | 18, 0 | 23 of 81 (67 of 141) | at least 31.91 | 20.30 | 32.96 |
| 8x8 XIP 4 KiB, staged | 24.98 | 265.1 (139-318) | 2,227 (2,122-2,292) | 17, 13 | 104 of 116 (143 of 169) | at least 109.21 | none | 154.40 |
| 8x8 XIP 4 KiB, no stage | 24.85 | 261.8 (138-314) | 2,209 (2,106-2,273) | 17, 13 | 106 of 116 (154 of 169) | at least 109.86 | none | 152.07 |
| 8x8 XIP 4 KiB, dsc tip | 24.85 | 261.8 (138-314) | 2,209 (2,106-2,273) | 17, 13 | 106 of 116 (154 of 169) | at least 109.86 | none | 152.07 |
| 8x8 XIP 32 KiB, staged | 12.50 | 265.1 (139-318) | 2,226 (2,122-2,292) | 17, 1 | 80 of 128 (122 of 181) | at least 47.21 | 40.76 | 54.25 |
| 8x8 XIP 32 KiB, no stage | 12.44 | 261.8 (138-314) | 2,208 (2,106-2,273) | 17, 0 | 75 of 129 (117 of 182) | at least 49.94 | 40.55 | 54.05 |

- The three dsc-tip tables are byte-identical to their no-stage arms' (paths aside). So the merge moved nothing in these arms but the stage.
- The stage costs a window load +1 (continuation) to +4 (new burst) CPU cycles, +3.3 on average, and a 64-byte refill +16 to +19, about +18 on average. Both match `SPIPHYStage`'s docstring at the 2:1 clock ratio.
- **For the manager, not caused by this sync:** at `5b5f4336` the 8x8 cacheless arm already refuses two probes (`srp.domain.if1`, `acmp.tmr_no_adp.if0`), and the 4 KiB XIP arms refuse more than the `e76a755a` table records (6 and 13, against 3 and 4). The README's Results already say those figures are not re-measured at this head. No issue is filed from this lane: the assignment allows posting only TAKEN, REVIEW READY or STOP.

## 6. Gate table

Every gate on the head `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1`, unpiped, with its rc recorded; logs in `./evidence` (digests in `evidence/SHA256SUMS`, host paths redacted, sizes over 200 KB in `evidence/OVERSIZE.txt`).

| Gate | Command | rc | Result |
|---|---|---:|---|
| mailbox generator | `sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | 0 | 0 findings; "selftest: 0 arm(s) failed" |
| publication census | `sw/mailbox/publication_census.py --check --selftest --jobs 5` (the `rtl-fast` publication-census step) | 0 | 6 shapes, 246 checks, 0 failures; 219 ports, C 26, F 28, R 34, E 6, M 14, G 111; G cones end at csr 7, memory 20, shim 4, reboot 1, wire 0; 139 arms, 0 failed; 43 rules, 0 unproven; "port census: the REBOOT request read past its terminal" refused by `g-on-wire` (1,499 s) |
| ctrl firmware, shard 0/4 | `fw_rv32_selftest.py --require-rv32`, `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4`, `test_ctrl_nvm.py --require-rv32 --jobs 4` (the `firmware-unit` job's commands) | 0 | PASS; saved-state store gate OK across 5 shapes, 435 tests (651 s) |
| ctrl mutant campaign (`ctrl_mutants.py`), shard 1/4 | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4` | 0 | PASS (1,702 s) |
| AECP mutants, shard 2/4 | `--shard 2/4` | 0 | PASS (725 s) |
| SRP mutants and pin controls, shard 3/4 | `--shard 3/4` | 0 | PASS (1,139 s) |
| LiteX simulations | `scripts/run_litex_sims.sh --selftest`, `scripts/run_litex_sims.sh <out>` (the `elaborate` aggregate) | 0 | self-test 10 of 10; 8 of 8 simulations, 0 timed out (1,155 s). **First run: rc 92**, `test_soc_timing_cuts` `TIMEOUT (900s wall clock - result UNKNOWN, not a failure)`, 7 PASS: it shared CPUs 80-95 with the census, the docs workflow and a harness arm. Re-run unchanged on its own 16 CPUs: rc 0. Earlier lanes record that test at 585 to 789 s against the 900 s limit, and one of them hit the same timeout under load. |
| builder bank, leg 0 | `ci_builder_legs.py run 0 --receipt <r> -- python3 sw/builder/test_builder.py --require-rv32` (`docs-gates-1`) | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 1b, this make's limit, as the gate states) (1,767 s) |
| builder bank, leg 1 | `ci_builder_legs.py run 1 ...` (`docs-gates-2`) | 0 | "ALL GATES PASS EXCEPT 16 NOT RUN": fifteen need a LiteX interpreter (the docs workflow installs none; `elaborate.yml` runs them), gate 11 a local build report (399 s) |
| rtl-fast bdd | `cd tests && behave --no-capture -f plain` | 0 | 14 features, 508 scenarios, 2,330 steps, 0 failed |
| docs workflow | every job's every `run:` step, in order, each job in a clean clone of the head: `wire-accountability`, `docs-check-no-git`, `docs-gates-0` (49 run steps), `docs-gates-1`, `docs-gates-2`, then `docs-check` over their receipts | 0 | all success; `docs-check`: "docs: 43 source gates exactly once; all worker jobs successful". Not run: `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail`, which observe a hosted run through the GitHub API. Provisioning replaced by a presence check: the `apt` lines and `sudo install` of sv2v (`sv2v v0.0.12`, `rsvg-convert` present), each marked in `evidence/wf-*-steps.json`. The RV32 SDK step runs as written against the verified install. |
| diff check | `git diff --check 97aab1d0f28bd753a3e11df6278d5cac54f964dd 9f81df00` | 0 | no finding |
| harness self-test | `tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | 0 failures |
| harness arms on the head | `run.py` as in section 5 | see note | the five earlier staged builds are refused by `--reuse-build` (`tree:firmware`: the digest covers `sw/mailbox`, and `fab0be5b` changed `mailbox_emit.py`), so they were run again on this head: every `table.md` is byte-identical to the first run's, paths aside. `8x8 XIP 32 KiB` attests and regrades identically. rc 1 on the arms with refused probes (`8x8 none`, the 4 KiB arms, `8x8 XIP 32 KiB`), as `run.py` reports a refusal; rc 0 otherwise. |
| native suite sweep, 4 shards | `native-shards.py sync-a723c <spec> <out> 4 0-15 48-63 64-79 112-127`, pinned Verilator 5.050, sv2v v0.0.12, Make 4.3 | 0 | **65 of 65 suites, 2,192,828 checks, 0 in-suite failures, 0 timed out**: shard 0 15 suites, 360,921 checks; shard 1 17, 1,526,104; shard 2 17, 284,228; shard 3 16, 21,575. Union checked against `suite_shards.py`: none missing, none twice. **Shard 1 was run twice** (next note). |

Environment: CPython 3.12.3 venv with the `ci/constraints-ci.txt` packages for every gate but two (LiteX simulations and harness: the product LiteX venv, CPython 3.14.8, the revisions `sw/litex/litex_pins.txt` pins); Verilator 5.050 (pinned), Yosys 0.66 (`86f2ddeb`), sv2v v0.0.12, GNU Make 4.3, GoogleTest 1.14.0, Clang 18; the RV32 SDK verified under the lane's scratch HOME. Units capped: 10 GB (census, harness), 8 GB (firmware, LiteX), 12 GB (docs), 10 GB (shards).

Note on shard 1: its first run reported `gptp_shadow`, `gptp_tables` and `mbx` as FAIL, each in a script that reads `make`'s output, on `make[1]: Entering directory` lines (`evidence/native-shard-1-first-attempt.log`). The cause is this lane's spec, not the head. I put Make 4.3, CI's version, on the sweep's PATH, while `native-shards.py` sets `MAKEFLAGS=-j4` without CI's `--no-print-directory`. Under Make 4.3, a `make -C` passes its directory printing down, so a script's nested `make` writes those lines into the stdout it reads as data; Make 4.4.1, or the flag, does not (reproduced with a two-target Makefile). I stopped that shard at 11 of 17 suites, cleaned its clone and ran the whole shard again from the start with `MAKEFLAGS=-j4 --no-print-directory`, the flag CI's job budgets set: 17 of 17. Shards 0, 2 and 3 passed as first started, without the flag.

Note on the census terminal: like the CSR and shim terminals it is named by cell and port, not per G output. A second G output driven into `reboot_req_i` would stop there too. A reviewer may want it narrowed to `reboot_req_o`'s own cone; the ruling did not ask for it, and the existing terminals have the same shape.
