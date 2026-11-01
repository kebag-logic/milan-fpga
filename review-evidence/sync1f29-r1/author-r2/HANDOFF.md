# [A723d] HANDOFF: sync dev 1f29f189 into dev-soft-core, round 2 (answering R759-1 and R760-1)

**Status: REVIEW READY at `fa01979959ebff05af34f5a752408de7b3c41cf1`.** Every gate this round requires exits 0 on that head (section 5). Nothing is pushed: PR #830 and the remote branch are still at `9f81df00`, and the PR body on GitHub is still the old one. Remote tips at the end: dev `1f29f189`, dev-soft-core `5b5f4336`.

- Lane: `$LANES/sync-dsc-1f29f189`, branch `sync-dev-1f29f189-into-dev-soft-core`.
- Reviews answered: R759-1 (NEGATIVE, issuecomment-6557739925), R760-1 (POSITIVE, issuecomment-6557637146).
- TAKEN: issuecomment-6557757402.
- Scratch: `$VALIDATION_STORAGE/sync-a723d` (`bin/` runners; `boot/` F1's four runs; `budget/` F2's two arms; `budget-u/` the other staged arms; `controls-u/` the controls and suites; `gates/` the required gates and `attest/` the re-attestation; `nostage/` the control tree).
- Evidence: `./evidence` (digests in `SHA256SUMS`, host paths redacted, nothing oversize).

## 1. Commits

All one-line subjects, no body, no trailers. The merge and every earlier commit are untouched.

| # | SHA | Closes | Files |
|---|---|---|---|
| 1 | `442da911d0c0c1d51931d0e48a6d29c49f2f6559` | RES-1, R760-1-R1 | `sw/mailbox/census_ports.py`, `sw/mailbox/mailbox.yaml` |
| 2 | `cb0be3cd4fa390329d182c7d6787274d847a0e3e` | F1, R760-1-R5 | `tb/verilator/ctrl_split_boot/README.md` |
| 3 | `fa01979959ebff05af34f5a752408de7b3c41cf1` | F2, R760-1-R4 | `tb/verilator/ctrl_service_budget/README.md` |

Commit 1 came first on purpose: it changes the firmware digest, so every measurement was made on it or later.

## 2. Findings, each with its verification

**F1. `tb/verilator/ctrl_split_boot/README.md:78-79`, now `:81-84`; also `:45` (R760-1-R5).** The stage reaches this SoC through `add_devices`. Measured at `442da911`, staged and against a no-stage control (`evidence/nostage.diff`, the one call removed), both shapes:

| Shape, stage | Boot to ready | CPU cycles | `milan_status` span / first byte / gap | `milan_gettime` (worst) |
|---|---:|---:|---|---|
| 1x1, staged | 84.393 ms | 4,219,673 | 21.530 / 1.962 / 1.265 ms | 2.524 / 1.238 / 1.267 ms |
| 1x1, none | 84.383 ms | 4,219,150 | 21.531 / 1.962 / 1.265 ms | 2.523 / 1.238 / 1.265 ms |
| 8x8, staged | 184.658 ms | 9,232,883 | 40.200 / 2.855 / 2.206 ms | 4.051 / 2.131 / 1.857 ms |
| 8x8, none | 184.647 ms | 9,232,360 | 40.197 / 2.855 / 2.205 ms | 4.051 / 2.131 / 1.857 ms |

The no-stage rows equal the old table cell for cell at both shapes, so the stage alone moved the figures (R759-1 ran that control at 1x1 only). The stage costs 523 CPU cycles at each shape. All four runs pass, trace 18 of 18.
- *Verification:* `verify_cells.py` compares every restated cell with its run's log: 0 mismatches (`evidence/verify-cells.log`). `run.py --regrade` on both staged builds at the head: rc 0, PASS.

**Correction to the earlier handoff.** `../sync-a723c/HANDOFF.md` section 3 says the split boot "builds through `CtrlMailbox` and `with_spiflash=False`, so neither item 3 nor item 4 reaches it". That is wrong. `boot_soc.py:79` does pass `with_spiflash=False`, but `boot_soc.py:86` calls `split_soc.add_devices`, which builds the staged PHY and the harness's own `KL_mbx` with `pub_src_sid_o`. So both changes reach this SoC, and no gate of that round ran it, which is how the wrong statement survived.

**F2. `tb/verilator/ctrl_service_budget/README.md:822-823`, and new text at `:837-860` (R760-1-R4).** Both cells now read `partial, 2 of 4 windows (`backlog-adp`, `backlog-adp-refill` refused): at least 87.17` and `... 86.54`. I measured rather than only relabelled, because the refused windows' figures and the no-stage refusal text were not published. Measured at `442da911`:

| Window | Stage | GM committed of 15 | Ring occupancy at open, of 16 | Graded | Longest pass, ms | Unreleased |
|---|---|---:|---:|---|---:|---|
| `backlog` | staged | 15 | 1 | yes | 87.17 | srp 27 |
| `backlog-owed` | staged | 15 | 0 | yes | 86.89 | srp 29 |
| `backlog-adp` | staged | 12 | 5 | refused | 81.40 | aecp 4, srp 32 |
| `backlog-adp-refill` | staged | 12 | 5 | refused | 88.32 | aecp 1, srp 32 |
| `backlog` | none | 15 | 1 | yes | 86.54 | srp 26 |
| `backlog-owed` | none | 15 | 1 | yes | 86.26 | srp 29 |
| `backlog-adp` | none | 13 | 4 | refused | 78.11 | aecp 4, srp 32 |
| `backlog-adp-refill` | none | 13 | 4 | refused | 84.98 | aecp 1, srp 32 |

Why both windows are refused at each stage setting: the raw log shows the first 11 grandmaster changes posted at once into the ring's 11 free slots (12 with no stage), then one more record when the firmware frees a slot, into which the rest coalesce (`KL_mbx_evt.sv` `gm_pend_r`). That gives 12 (13), against the defined 15, and `grade.check_load` refuses the window. At `5b5f4336`, before #814, the same two windows are refused at 13, so this is the firmware's and not the stage's. The refusal counts also resolve R760-1's inference: 5 is these two plus 3 probes, and 6 is these two plus 4.
- *Verification:* `verify_cells.py` against each `results.json`'s `composed_maximum` and `refusals`: 0 mismatches. `evidence/windows4.log` gives the window table, read with `grade.py`'s own functions by `bin/windows4.py`. Each arm's table is byte-identical to the one published at `9f81df00`.

**Third-figure sweep.** `git grep` finds `split_soc.add_devices` used only by `ctrl_service_budget/split_soc.py:469` and `ctrl_split_boot/boot_soc.py:86`, so those are the only two READMEs `dcd56703` reaches. No third stale figure remains:
- Budget README, every "at this head" statement (`:227-228`, `:274`, `:576`, `:596`, `:818`, `:911`, `:1056-1058`, `:1071`, at the head), and the flash figures at `:262-269`, `:583-584`, `:796-802`. The older figures are dated to `e76a755a` and stated to have no stage (`:224-228`).
- Those "at this head" control figures, which predated the stage, were re-run on `442da911`: `slow-adp-rx` 24.614 ms, caught; `as-built` cause 5 at `TRAP ... 0 5 00000020` on the cacheless and the cached CPU. All unchanged.
- The staged tables: all six arms re-run, each byte-identical.
- Other documents: `git grep` for the boot, composed, refill and window figures outside the two READMEs finds none (`docs/ARCHITECTURE_HW_SW_SPLIT.md:210`, `docs/design/SPLIT_CONTROL_MEMORY.md:107,:350` and `sw/firmware/ctrl/plat/README.md:111` link the harnesses and state no such figure).
- Not reached by `dcd56703`: `nvm_capture_cpu` and `fw_service_budget` take the stage directly from `MilanSoC.add_spi_flash` under dev's #814. Their READMEs state no flash timing figure.

**RES-1, R760-1-R1. `sw/mailbox/census_ports.py:59,:302`, `sw/mailbox/mailbox.yaml:84`.** Now `(#665, #787)`, `(#665, the exclusion)` and `(the ruling on #665)`, each as the review's exact fix.
- *Verification:* no added line since `9f81df00` holds a ten-digit ID. Against both parents, the only ten-digit ID left in added source text is `comment 6088423771` in `milan_soc.py`, which both parents already carry, as both reviews said. `gen_mailbox.py --check --crosscheck`: 0 findings, so no output regenerates.

**RES-2, R760-1-R2, R760-1-R3. `PR-BODY.md`.** "Not yet pushed" is deleted. The generator's two commands are listed apart with their own results.
- *Verification:* read `PR-BODY.md`. Each command exits 0 alone (section 5).

**Left as they are (suggestions, optional by definition):** R759-1 S1 to S3 and R760-1 S1 to S4.

## 3. Conflict table (unchanged, carried from `../sync-a723c/HANDOFF.md`)

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

## 4. Semantic-conflict and regeneration lists

### Semantic conflicts (rounds 2 and 3, with this round's correction)

The files both sides changed since `97aab1d0` are listed in `../sync-a723b/HANDOFF.md` section 3 (24 files). Rounds 2 and 3 found these, each fixed in its own commit after the merge:

1. **The port census against dev's two new wrapper ports** (`sw/mailbox/census_ports.py` against `hdl/milan/KL_pp_shadow.sv`, ports added by #802 for #799 and by #822 for #787). The census failed on the merge (3 findings, every shape). Fixed in commit 1 under ruling (C).
2. **dev's living "2.3" citations of the source entries**, which this line numbers 2.4 under ruling (B). Fixed in commit 2, 11 places:
   `CHANGELOG.md:172`; `docs/reference/SUBMODULES.md:288`; `docs/design/MAILBOX_SPLIT.md:820`, `:1349` (the publication-block row; now `:1362`) and `:1595`; `sw/firmware/ctrl/test/ctrl_mutants.py:697`; `sw/litex/milan_soc.py:2917`; `tb/verilator/mbx/README.md:126` and `:330`; `tb/verilator/mbx/mutants.py:478`; `tb/verilator/mbx/suite.hpp:1710`.
   Kept as measured (dated records of dev's measurement at lane head `8b76de69` on dev `97aab1d0`, which carried 2.3): `docs/design/AREA_BUDGET.md:536` and `:541`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:22`, `:45` and `:61`, and the three `"measured"` strings of `syn/ooc/pp_resource_baseline.json`. This line's own "contract 2.3" citations name the face block, minor 3, and are unchanged.
3. **The CPU budget harness's own `KL_mbx` instance against dev's `pub_src_sid_o`** (`tb/verilator/ctrl_service_budget/split_soc.py` `unread_publication`, against #802's port in `KL_mbx.sv` and `CtrlMailbox`). Found in this round: the harness build refused, `the mailbox instances leave ports unconnected (verilate.log, PINMISSING): ['KL_mbx.pub_src_sid_o']`. `CtrlMailbox` auto-merged with the port; the harness restates `CtrlMailbox`'s publication outputs and did not. Fixed in commit 3: the port is named and unread, as `CtrlMailbox` leaves it; the harness README's mailbox paragraph says so.
4. **Rule 12's 100-line limit against the merged `emit_doc`** (`sw/mailbox/mailbox_emit.py`). dsc's face block (`05d0b575`) added its three register sections, windows and COUNTERS_CHANGED table to `emit_doc`, and dev's source entries (`3b42bcf2`) added the publication-source section. Each side kept the function within 100 lines; merged it is 104, so the docs workflow's Python idiom gate failed on the merge (`long function 10 > ratchet 9`, `scripts/py_idiom.budget`). Found in this round. Fixed in commit 4: the face block's sections move to `_face_sections`, unchanged; `gen_mailbox.py --check --crosscheck` rc 0 (the generated outputs are byte-identical) and `check_py_idiom.py` rc 0 (`long function: 9 <= 9`).
5. **The S2 service-budget harness against #814's `SPIPHYStage`** (`tb/verilator/ctrl_service_budget/split_soc.py` `add_devices`, against `milan_soc.MilanSoC.add_spi_flash`, `sw/litex/milan_soc.py:3871`). The harness built LiteSPI over its `FlashBoundary` with no stage, so its README's "the address does not change an access's cost" no longer held for the flash. Fixed in commit 5: `phy = milan_soc.stage_spi_phy(FlashBoundary(...))`, the claim corrected, and the flash-window, refill and XIP arms re-measured (section 5).
6. **`MAILBOX_SPLIT.md` verification figures.** Fixed in commit 6, from this head's own runs: census 41 reads of 22 of the 26 class-D nets, 4 unread, 219 ports (C 26, F 28, R 34, E 6, M 14, G 111), 139 arms (118 + 19 + 2), 43 rules (31 + 12); mbx 525 and 570 at one interface, 532 and 577 at two (45 handshake checks each way); host model 490 of 532. The census section's own counts moved in commit 1. Checked and already right: "26 population nets ... 41 reads ... 11 on the wire, 14 CSR status, 16 the answer face" (`:995`, against `publication_census.py --list`: 11 field, 14 status, 16 processor rows); the generator's "35 arms ... 49 arms" (`:97`).

Checked, no stale rule (round 2): `MARK_II_AREA_PLAN.md` against #818's WNS gate; the #814 DRAM-side cuts (the split harnesses build with `with_dram=False`); `scripts/port_docs.budget`. **Corrected in this round:** that line used to say the split boot builds through `CtrlMailbox` and `with_spiflash=False`, so the harness's mailbox port and PHY stage do not reach it. That was wrong. See "Correction" in section 2.

Round 2 of review added one, found by R759-1 and R760-1: the split boot against `dcd56703`'s stage (F1).

### Regeneration

| Commit | Generator | Outputs changed | Check |
|---|---|---|---|
| merge `97e9a3d3` | `gen_mailbox.py --write`, after `minor: 4` | `KL_mbx_pkg.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md` (`KL_mbx.sv` unchanged) | `--check --crosscheck --selftest` rc 0, 35 output arms, 49 contract arms |
| `fab0be5b` | none needed: `emit_doc` refactored | none: `gen_mailbox.py --check --crosscheck` rc 0, so every generated output is byte-identical | as left |

Tables of contents: no heading was added. `gen_toc.py --check` rc 0. The one contents description changed (`MAILBOX_SPLIT.md`, "The processor's other faces") is the human-owned part of the entry. Diagrams and records: no generator input changed; the docs gates' no-drift checks are in the gate table.

This round: no generator input changed in effect. `mailbox.yaml`'s edit is a comment, and `gen_mailbox.py --check --crosscheck` gives 0 findings, so nothing was regenerated. No heading was added to any page, so no table of contents changed (`gen_toc.py --check` runs in the docs workflow).

## 5. Gate table

Docs workflow, generator, census and diff check ran on the head `fa019799`, unpiped. Harness runs started on `442da911` or `cb0be3cd`; only the two READMEs differ from there to the head, and every build was re-attested at the head.

| Gate | Command | rc | Result |
|---|---|---:|---|
| generator check | `gen_mailbox.py --check --crosscheck` | 0 | 0 findings |
| generator self-test | `gen_mailbox.py --selftest` | 0 | 0 arms failed |
| generator, assigned form | `gen_mailbox.py --check --crosscheck --selftest` | 0 | runs the self-test only, as R760-1-R3 found, hence the two lines above |
| census | `publication_census.py --check --selftest --jobs 14` | 0 | 6 shapes, 246 checks, 0 failures; 41 reads of 22 of 26 nets, 4 unread; 219 ports, C 26, F 28, R 34, E 6, M 14, G 111; cones end at csr 7, memory 20, shim 4, reboot 1, wire 0; 139 arms, 0 failed; 43 rules, 0 unproven (1,648 s). A superset of the assigned `--check`, because `census_ports.py` changed. |
| docs workflow | every `run:` step of `wire-accountability`, `docs-check-no-git`, `docs-gates-0` to `-2`, each in a clean clone (`bin/docs_all.sh`) | 0 | all success (1,127 s) |
| docs-check | the same runner, over the three legs' receipts | 0 | "docs: 43 source gates exactly once; all worker jobs successful". **First two attempts rc 1, both my runner's setup:** it had no receipts placed, then no `needs` context. Neither is a head fault, and the head did not change. |
| builder leg 0 | `ci_builder_legs.py run 0 ... test_builder.py --require-rv32` (`docs-gates-1`) | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 1b) |
| builder leg 1 | `ci_builder_legs.py run 1 ...` (`docs-gates-2`) | 0 | "ALL GATES PASS EXCEPT 16 NOT RUN" (15 need a LiteX interpreter the docs workflow does not install; gate 11 a local build report) |
| diff check | `git diff --check 97aab1d0f28bd753a3e11df6278d5cac54f964dd fa019799` | 0 | no finding |
| split boot | `ctrl_split_boot/run.py` at 1x1 and 8x8, staged and no-stage | 0 | PASS, 0 findings, all four |
| split boot controls | `--native-controls`; `--self-test` | 0 | 6 of 6; 2 of 2 plants caught |
| budget self-test | `ctrl_service_budget/run.py --self-test` | 0 | 0 failures, at `442da911` and at the head |
| budget arms, staged | `run.py --point P --build-dir B [--xip] --fetch-l1 G --jobs 14 --record-budget-findings`, six arms | see note | P1-none 0, P1-xip-512x1 0, P8-none 1, P1-xip-64x1 1, P8-xip-64x1 1, P8-xip-512x1 1. rc 1 is `run.py` reporting refused probes, as before. Every table byte-identical to `9f81df00`'s. |
| budget arm, no stage | 1x1, 4 KiB in the control tree | 1 | as above; table byte-identical |
| budget controls | `--mutation slow-adp-rx`; `--cpu-regions as-built` at `none` and `64x1` | 0 | each caught, figures as the README states |
| re-attestation at the head | `run.py --reuse-build --regrade` on all six staged builds | see note | each attests and regrades to the same table; same rc as its run (`evidence/attest.log`) |
| README cells | `bin/verify_cells.py` | 0 | 0 mismatches |

**Firmware digest.** Commit 1 changes `sw/mailbox`, which the budget harness's `tree:firmware` digest covers (`build.py` `FIRMWARE_TREES`), so `--reuse-build` refuses every earlier build. What attests against it is that harness alone, so its six staged arms were rebuilt and re-run. The split boot has no such digest; it was re-run anyway, for F1.

**Not re-run, as assigned:** the firmware shards and mutant campaign, LiteX simulations, `behave` and the native sweep. No RTL or firmware source changed: `git diff --stat 9f81df00 fa019799` is the two `sw/mailbox` files (comments and one reason string) and the two READMEs. Their results stand from `9f81df00` (`../sync-a723c/HANDOFF.md` section 6).

Environment: as round 3 of the merge lane. The docs workflow, generator and census use CPython 3.12.3 with `ci/constraints-ci.txt`; the harnesses use the product LiteX tree on CPython 3.14.8 at the pinned revisions; Verilator 5.050, sv2v v0.0.12, Yosys 0.66. Units were capped at 10 GB (harness, census), 12 GB (docs) and 8 GB (docs-check), and pinned to booked CPU ranges.

Limits: the docs workflow ran locally (`ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` observe a hosted run and were not run; `apt` and `sudo install` provisioning is replaced by a presence check). No hosted run has seen this head, because nothing is pushed. No Vivado, hardware or bench run.

## 6. Open points for the manager

- **Pushing and the PR body are yours.** PR #830 still shows `9f81df00` and the old body; `PR-BODY.md` is the replacement.
- **The grader's wording is still misleading.** `run.py` reports a refused backlog window as "not run" in `table.md` and `not_run` in `results.json`, while `README.md:216` describes "not run" as a row the run did not include. The README now says what it means in these two rows. Changing the grader is outside this lane, and I may post nothing but TAKEN, REVIEW READY or STOP, so it has no Issue yet.
- **The worst-pass cells exclude refused windows.** For the 1x1, 4 KiB rows, 87.17 and 86.54 are the graded groups' worst; the refused `backlog-adp-refill` window reaches 88.32 staged. The README states this.
- Carried from before and unchanged: the pre-existing refused probes at `5b5f4336`; the census terminal's shape (R759-1 S1, R760-1 S1); `RUNNING_TESTS.md:84` and `CI_WORKFLOWS.md:451` saying 64 suites where the runner lists 65, which is dev's own text.
