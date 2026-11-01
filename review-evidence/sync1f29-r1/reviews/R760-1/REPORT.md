[R760] POSITIVE - exact head 9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1

External independent review of PR #830 / issue #665, round R760-1. Tree `291e6bdfa9460add122f7839d55ea305f8365d69`, source base `5b5f433698d8832b63573b8d106f10e839a4210e`, dev `1f29f189279f9fc0132f4918e47342b87d22f33a`, merge commit `97e9a3d396ec2d35b907f7c5c47823fbfcee6458`.

No BLOCKER, MAJOR or MINOR is open. Five RESIDUE items and four SUGGESTIONs follow. The merge keeps both lines, the two rulings are implemented as ruled, and I found no semantic conflict beyond the ones the lane already fixed. Every figure I could check reproduces, including three budget arms whose tables match the published ones byte for byte.

One author statement is wrong: the split boot simulation does carry both the new port and the PHY stage. No author gate ran it at this head, so I ran it. It passes at both shapes (R760-1-R5).

## Clean lenses

```text
[R760] PASS Conformance - comments 6553999730 and 6554243203 against sw/mailbox/mailbox.yaml:76-89, sw/mailbox/census_ports.py:131,:392,:302, sw/mailbox/census_plants.py:682, docs/design/MAILBOX_SPLIT.md:1160-1170,:1656-1661, export-compare.txt - rulings B and C implemented with nothing added, no REBOOT carrier, S1 item 5 holds: 105 of 105 export files equal dev's
[R760] PASS RTL - git diff of 97e9a3d3 against the recomputed merge tree, restricted to hdl/, and hdl/milan/mailbox/KL_mbx_pkg.sv, switch-on export gateware/alinx_ax7101.v against KL_mbx's port list, mbx-suites-head.txt - only MBX_VERSION_MINOR_C moved, by regeneration, no hdl edit after the merge, datapath, wrapper, CSR and KL_reboot_ctrl identical to dev, every port of the union bound on the SoC's instance
[R760] PASS Robustness - probe-reboot-terminal.txt, probe-merge-resolution.txt, split-boot-1x1-head.txt, split-boot-8x8-head.txt - the terminal holds against a second consumer, another input and another module; the merged generator terms each refuse their own removal, face.check aside (S3, pre-existing); the boot, which inherits the stage and the port, passes at both shapes
[R760] PASS Tests - census-head.log, gen-selftest-head.log, gen-check-head.log, mbx-suites-head.txt, mbx-mutants-quick-head.txt, union-check.txt, budget-P1-none-table.md, budget-P1-xip-512x1-table.md, budget-P1-xip-512x1-nostage-table.md - the ruled arm fails for its defect, 139 arms and 43 rules hold, both sides' mutants survive the merge and are caught, the re-measured tables reproduce byte for byte
[R760] PASS Docs - docs/design/MAILBOX_SPLIT.md:97,:994-996,:1120-1178,:1356-1364, tb/verilator/ctrl_service_budget/README.md:144,:228,:273-289,:817-836, contract-2.3-mentions.txt, docs-check-head.txt - every restated figure matches a run at this head, dated #799 records keep 2.3, living source-entry citations read 2.4, the remaining 2.3 citations name the face block
```

Coverage is clean under the owner's rule: RESIDUE does not leave a lens unclean, and a SUGGESTION does not affect coverage.

## Focus items

**(1) Conflict resolution in `97e9a3d3`.** Recomputed with `git merge-tree --write-tree --messages`: exactly the seven named files conflict, in 12 hunks. The whole difference between the conflict tree and the commit is in `merge-tree-vs-97e9a3d3.diff`.

| File | Resolution checked |
|---|---|
| `docs/design/MAILBOX_SPLIT.md` | Both sides' rows and paragraphs kept. Only the census, mbx and model figures and the version citation were restated. |
| `sw/firmware/ctrl/test/ctrl_mutants.py` | Six face mutants and two source-entry mutants all present, and the author's campaign logs catch the ones I sampled from each side. |
| `sw/litex/milan_soc.py` | One docstring states both blocks. |
| `sw/mailbox/gen_mailbox.py` | The regex and the crosscheck list carry both register sets. Both sides' arms are present: 35 output arms and 49 contract arms, counted by calling the functions. |
| `sw/mailbox/mailbox.yaml` | Both history entries are kept, minor 3 stays the face block, and `version.minor` is 4. |
| `sw/mailbox/mailbox_skeleton.py` | The source whole-word check and `face.check` are both present. |
| `tb/verilator/mbx/README.md` | Dev's P row, then the line's F and T rows. |

`union-check.txt` lists every line either side added, over all 24 files both lines touched, that is absent at the head. All 56 are restated figures, version citations or the re-flowed regex, list and docstring lines, and no behaviour is dropped. Undoing each merged generator term fails the self-test (`probe-merge-resolution.txt`). The exception is removing `face.check`, which also survives at `5b5f4336`, so it is not this merge's doing (R760-1-S3). That receipt's "version minor back to 3" line survives only because `--selftest` skips the check (R760-1-R3): the same edit under `--check --crosscheck` gives rc 1 with 6 findings (`gen-check-minor3-probe.txt`).

**(2) The rulings.**
- Ruling B: minor 4 with the ruled history, and generated outputs clean under `gen_mailbox.py --check --crosscheck` (rc 0, 0 findings).
- Ruling C: `src_stream_id_o` is in class C and `reboot_req_o` in class G. The cone stops at `reboot_ctrl.reboot_req_i` only, and the exclusion is named as a placement-switch acceptance item in the docstring, the design page and Open items. The arm is at `census_plants.py:682`.
- Probes on the recipe netlist: without the terminal the request reaches the wire; a probe on the request net, another input of the cell and a same-named cell of another module are each refused by `g-on-wire`.
- Nothing beyond the rulings: no face-block field, no contract content, no new issue. The two semantic-conflict commits were allowed by the lane's scope.

**(3) Semantic conflicts both lines could hide.** Checked, no new finding:
- **#814:** every LiteSPI build is staged after `dcd56703`. The harness's other cuts need DRAM, which the split harnesses do not build. The switch-on SoC exports at the shipping shape with `KL_mbx`'s ports bound, the stage present and a different CPU netlist from the all-fabric build's (`switch-on-mbx-ports.txt`, `switch-on-cpu-and-stage.txt`).
- **#787:** `reboot_req_o` is the only new class-G cone. `KL_reboot_ctrl` reads `pp_nvm_*`, which are class F ports with carriers. The firmware's AECP does not serve REBOOT, which is out of scope by ruling.
- **#818:** the only live WNS rule text on this line is the restated area plan, and `--shipping-selection` is present. No split document cites the old limit.
- **#70:** the split firmware does not repeat the old "entity enabled" line, and `F_CTRL.READY` remains the release. The split boot trace still equals `configure_fabric()`'s first 15 writes.
- **#790 and #206:** the firmware gates GET_STREAM_INFO from its own ACMP view at `ctrl_app_aecp.c:48-63`, so the processor-side fix leaves no gap.
- **gPTP pathTrace head:** firmware GET_AS_PATH stays an explicit unavailable observation, so entry 0's change does not reach it.
- **Limits and inventories:** the Python idiom gate is at its ratchet, and `docs_check` reports 0 findings. `ci/image/tool-inventory.json` already differs from the file bytes on both parents, so the merge adds no new kind of drift.

**(4) The re-measured budget arms.**
- Three arms re-run at this head with the same commands: 1x1 cacheless staged, 1x1 32 KiB XIP staged, and 1x1 32 KiB XIP no-stage (a tree copy with only that line reverted). Each table is byte-identical to its published receipt.
- From my logs: CPI 9.42; BRAM fetch 9.09 (307); window load 266.14 (139-307); XIP CPI 13.28 against 13.21; refill 2,238.64 (2,122-2,292) against 2,220.57 (2,106-2,273); window load 265.40 (139-318) against 262.13 (138-314); worst pass 33.36 against 32.96 ms. All match the README and the handoff's table.
- Stage costs of +1 and +4 on a window load and +16 to +19 on a refill follow from those ranges. The published tables for the other arms match the README's paths, instances and composed figures (`budget-receipts.txt`).
- No verdict moves on the cacheless arms: 0 of 81 and 0 of 127 (`verdict-moves.txt`). On XIP the crossings are small and go both ways. The largest is 8x8 32 KiB, 9 newly missing and 3 newly fitting. "A few paths" is fair wording.
- The `dsc` tables are byte-identical to the no-stage tables, so the merge moved nothing in those arms but the stage. The corrected claim at `README.md:144` is accurate.

**(5) All-fabric export.** Exported all five shipped configs at dev and at the head with no vendor tool, by the method in `MAILBOX_SPLIT.md` "Default build". 105 of 105 files compare equal after removing timestamps, output paths and the comment-only hierarchy tree, with the run's `litex.log` left out. The Arty configs are at 100 MHz, as that method states. `milan_soc.py` differs from dev only inside `CtrlMailbox`, `ctrl_cpu_args` and the `if ctrl_mailbox:` branch. `VERSION` stays `0x0002_0060`.

**(6) Restated figures.** All match my runs:
- Census: 41 reads of 22 of 26 nets, 4 unread, in six shapes; 219 ports (C 26, F 28, R 34, E 6, M 14, G 111); cones end at csr 7, memory 20, shim 4, reboot 1, wire 0; 139 arms, 19 of them port arms; 43 rules; rows 11, 14 and 16.
- mbx: 525, 570, 532, 577 and 490.
- Generator: 35 and 49.

**(7) 2.3 and 2.4.** The 11 living citations read 2.4. The eight dated ones keep 2.3 (`AREA_BUDGET.md:536,:541`, finding 234 `:22,:45,:61`, three `measured` strings). Every other "contract 2.3" names the face block (`contract-2.3-mentions.txt`).

**(8) Out of scope by ruling, not findings.** #70's PHY link gap on the split platform, and the REBOOT carrier.

**Prior public findings on this PR:** none to resolve or retain. After my verdict and ledger were written, the PR and issue threads still held only the two review-start notices and the author's REVIEW READY, and the PR has no review objects.

## Findings

No BLOCKER, MAJOR or MINOR.

### R760-1-R1 - RESIDUE - Docs
- **Where:** `sw/mailbox/census_ports.py:59`, `:302`; `sw/mailbox/mailbox.yaml:84-85`.
- **Authority:** owner comment rule of 2026-10-15. These are new issue-comment IDs in the reviewed delta. `sw/litex/milan_soc.py:2919` only re-flows a reference both parents carry, so it is existing and tracked by #746.
- **Impact:** wording only.
- **Exact fix:** `census_ports.py:59` to `(#665, #787)`; `:302` to `(#665, the exclusion)`; `mailbox.yaml` to `(the ruling on #665)`.
- **Verification:** the new source lines hold no ten-digit ID.

### R760-1-R2 - RESIDUE - Docs
- **Where:** PR #830 body, Status.
- **Evidence:** "Not yet pushed: this body is prepared for the PR." The PR is open at this head.
- **Impact:** wording only.
- **Exact fix:** delete that sentence.
- **Verification:** read the body.

### R760-1-R3 - RESIDUE - Docs
- **Where:** PR #830 body, "How to validate" and the gate table; REVIEW READY's table row.
- **Evidence:** `gen_mailbox.py:451` returns `selftest()` before the check runs, so `--check --crosscheck --selftest` runs only the self-test. The published `gen.log` has no findings line, so that receipt does not support "0 findings". The claim itself is true: `--check --crosscheck` alone at this head gives rc 0, 0 findings (`gen-check-head.log`).
- **Impact:** wording only. Nothing drifted.
- **Exact fix:** list two commands, `--check --crosscheck` and `--selftest`, with their own results.
- **Verification:** both commands exit 0.

### R760-1-R4 - RESIDUE - Docs
- **Where:** `tb/verilator/ctrl_service_budget/README.md:822-823`.
- **Evidence:** the two 1x1 4 KiB cells sit under "Composed maximum, every backlog window", but their receipts say "over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill not run)". The README's own arm B rows spell this "partial, 3 of 4 windows". Both figures stay true lower bounds.
- **Impact:** wording only. No figure changes.
- **Exact fix:** write `partial, 2 of 4 windows (backlog-adp, backlog-adp-refill not run): at least 87.17` and the same with `86.54`.
- **Verification:** compare with the published `budget-P1-xip-64x1-table.md:92`.

### R760-1-R5 - RESIDUE - Docs
- **Where:** published `author/HANDOFF.md` section 3; `tb/verilator/ctrl_split_boot/README.md:45` and its Results.
- **Evidence:** the handoff says the split boot "builds through `CtrlMailbox` and `with_spiflash=False`, so neither item 3 nor item 4 reaches it". In fact `boot_soc.py:86` calls `split_soc.add_devices`, which builds the staged PHY (`split_soc.py:359`) and the mailbox with `pub_src_sid_o` (`:237`). The exported boot SoC shows `stage (SPIPHYStage)` under `phy (FlashBoundary)`. Run at this head it passes: 84.393 ms at 1x1 and 184.658 ms at 8x8, against the recorded 84.383 and 184.647 at `b8628704`, all UART duties in bound, trace 18 equal.
- **Impact:** wording only. The README's Results are dated by firmware commit and stay true.
- **Exact fix:** add under Results "These predate #814's SPI PHY stage, which this SoC now carries; at `9f81df00` the boots read 84.393 and 184.658 ms." Correct the statement wherever the handoff is reused.
- **Verification:** `split-boot-1x1-head.txt`, `split-boot-8x8-head.txt`, `split-boot-soc-hierarchy.txt`.

### R760-1-S1 - SUGGESTION - Tests
- **Where:** `sw/mailbox/census_ports.py:392`.
- **Evidence:** the terminal behaves as documented, but three properties are not pinned (`probe-reboot-terminal.txt`). A mutant widening the terminal to every input of the cell passes the ruled arm. A different G output driven into `reboot_req_i` is accepted (the author's open risk 1). A terminal no cone reaches is not refused, though the map writer's exclusion refuses a stale name.
- **Decision:** the ruling asked for one arm and did not ask for these, and the exclusion is dropped at the switch. I accept the terminal as ruled and do not require narrowing.
- **If wanted:** one arm each, in the switch-over lane.

### R760-1-S2 - SUGGESTION - Tests
- **Where:** `tb/verilator/ctrl_service_budget/split_soc.py:359`.
- **Evidence:** nothing refuses an unstaged harness. The no-stage control builds and exits 0, and the harness self-test names no stage. `FACE_IDLE_INPUTS` (`:247`) is this file's precedent for a guard that tracks `CtrlMailbox`.
- **If wanted:** refuse a PHY without `stage` in `add_devices`.

### R760-1-S3 - SUGGESTION - Tests, Robustness
- **Where:** `sw/mailbox/gen_mailbox.py:451`; `sw/mailbox/mailbox_skeleton.py:644`.
- **Evidence:** both predate this PR. `--selftest` silently drops `--check` and `--crosscheck` given with it. Removing `face.check` passes the self-test, on this head and at `5b5f4336`.
- **If wanted:** a new Issue. Run all the named modes, and add a contract arm that reaches `mailbox_face.check`.

### R760-1-S4 - SUGGESTION - Docs
- **Where:** `docs/design/MAILBOX_SPLIT.md:839`, `:1627`.
- **Evidence:** `SRC_SID_LO/HI` have no firmware writer ("none yet"), and the talkers' stamps and GET_STREAM_INFO read `src_stream_id_o`, which those entries carry in the split. The table says so; Open items, which the placement switch reads, does not.
- **If wanted:** one Open items bullet.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings 6553999730 and 6554243203, issue #665 scope, `mailbox.yaml`, `census_ports.py`, `census_plants.py`, `MAILBOX_SPLIT.md`, five-config export against dev | R760-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| RTL | CLEAN | `hdl/` diffs against the merge tree and dev, `KL_mbx_pkg.sv`, dev's `milan_datapath.sv`, `KL_pp_shadow.sv` and `milan_csr.sv` diffs, switch-on export's `KL_mbx` instance, mbx suites | R760-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Robustness | CLEAN | census terminal probes, generator resolution probes, split boot at 1x1 and 8x8, `SPIPHYStage` and `stage_spi_phy` in the harness | R760-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Tests | CLEAN | census `--check --selftest`, generator self-test and check, mbx suites and quick mutants, union check, three budget arms, published firmware and native receipts | R760-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Docs | CLEAN, five RESIDUE | `MAILBOX_SPLIT.md`, harness README, boot README, 2.3 and 2.4 mentions, `docs_check`, PR body, REVIEW READY, handoff | R760-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |

## Reproduce

Scripts are under `scripts/`, with raw receipts under `receipts/`. Set `PACKET`, `LITEX_VENV`, `SDK_BIN`, `VERILATOR_DIR` and `SV2V_DIR`, source `scripts/env.sh`, then from a tree copy:

```sh
python3 sw/mailbox/publication_census.py --check --selftest --jobs 6
python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck
make -C tb/verilator/mbx -j8 run-wb run-axil run-if2
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir B
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir B --fetch-l1 none --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir B --xip --fetch-l1 512x1 --jobs 4 --record-budget-findings
scripts/export_all_fabric.sh TREE OUT; python3 scripts/export_compare.py OUT_DEV OUT_HEAD
```

Tools: pinned Verilator 5.050, sv2v v0.0.12, Yosys 0.66, the product LiteX venv at CPython 3.14.8, and the pinned RV32 SDK whose archive digest I verified. CPU netlists came from the cache through a private copy of the CPU data package, so no shared tree was written.

## Real limits

- **Budget arms:** I ran 3 of the 15 published arms. The other arms' CPI, refill, window-load and worst-pass figures are not in the published tables, so they rest on the author's handoff, which agrees with the README. The 8x8 arms and the `dsc` arms were compared as published, not re-run.
- **1x1 4 KiB refusal counts:** "5" and "6" read as 3 and 4 no-start rows plus the 2 windows not graded. That composition is inferred from the tables, not reproduced.
- **Not run by this round:** the ctrl firmware bank and its full mutant campaign (I sampled source and face mutants from the author's receipts), full mbx mutants, `run-cosim`, builder legs, `behave`, the native sweep, the docs workflow beyond `docs_check` and the idiom gate, Yosys banks, and any Vivado run. These rest on the author's published receipts.
- **Evidence integrity:** every published file matches `MANIFEST.json`'s `published_sha256`. Three receipts differ from `SHA256SUMS` because of path redaction, which the manifest records.
- **Export comparison:** the normalizer removes the comment-only hierarchy tree and leaves out `litex.log`. The Arty configs are compared at 100 MHz, not their shipping 83.333 MHz, as the method states.
- **Hosted evidence:** when last read, 67 checks passed and 1 was skipped (`Physical gPTP (nightly and manual)`), with none failing. `rtl-fast`, `elaborate`, `verilator-suites` and `yosys-portability` completed with success on the exact head, and `docs-check`, `docs-check-no-git` and `wire-accountability` passed. I did not inspect their logs. A skipped context is not hardware proof, and acceptance is the manager's.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **No source bank at this head:** this review neither claims nor infers a manager source bank.

## Pending manager duties

- The current-dev candidate merge, with builder and native banks and their receipts.
- Hosted and `act` acceptance on the exact head.
- The second positive review.
- Carrying R1 to R5 to the residue checklist.
- Deciding whether S3 and the author's open risk 2 become new Issues. The pre-existing refused probes are confirmed by the byte-identical `dsc` tables.
- Post-merge containment.

The clone is restored and verified at the exact head: 1,506 blobs with bytes and modes equal, index equal to the tree, and the five required gitlinks match (`clone-verify.txt`).

R760-1 FINISHED
