[R759] NEGATIVE - exact head 9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1

Round R759-1, issue #665, PR #830: merge of dev `1f29f189` into dev-soft-core `5b5f4336`. Tree `291e6bdfa9460add122f7839d55ea305f8365d69`.

Two open MINOR findings make this NEGATIVE. Both are stale or unlabelled harness README figures. The merge itself, both rulings, the RTL, the census and the all-fabric export hold.

## Findings

### F1. MINOR. Conformance, Docs. `tb/verilator/ctrl_split_boot/README.md:78-79`: the split boot figures no longer match the harness this PR changed

- **Authority:** ruling 6553999730 owes a check of the harness against #814's stage, and a correction of the claim and figures that no longer hold. Focus item 3 asks for semantic conflicts the author missed.
- **Evidence:** `dcd56703` stages the flash in `split_soc.add_devices`. `boot_soc.py:86` calls that same function, so this SoC is staged too. The author's published handoff says the stage does not reach it (`with_spiflash=False`, built through `CtrlMailbox`). `with_spiflash=False` is at `boot_soc.py:79`, but the flash comes from `add_devices` and the mailbox from `StimulusMailbox`.

| Run at this head | Boot to ready | CPU cycles | `milan_status` span / first byte / longest gap |
|---|---:|---:|---|
| 1x1, README | 84.383 ms | 4,219,150 | 21.531 / 1.962 / 1.265 ms |
| 1x1, the `stage_spi_phy` call removed | 84.383 ms | 4,219,150 | 21.531 / 1.962 / 1.265 ms |
| 1x1, head | 84.393 ms | 4,219,673 | 21.530 / 1.962 / 1.265 ms |
| 8x8, README | 184.647 ms | 9,232,360 | 40.197 / 2.855 / 2.205 ms |
| 8x8, head | 184.658 ms | 9,232,883 | 40.200 / 2.855 / 2.206 ms |

  The 1x1 no-stage control equals the README, so the stage alone moves the 1x1 figure. No 8x8 control was run. Receipt: `receipts/boot-summary.txt`.
- **Impact:** the documented commands no longer print the table: 523 CPU cycles more at each shape, at most +0.012 %. No verdict moves: both shapes pass, with the trace 18 of 18 equal. The README names firmware `b8628704` but does not say the figures predate the stage, as the budget README now does for its own Results. This changes figures, so it is not RESIDUE.
- **Required outcome:** the Results table is restated at the head with the stage, or says it has no stage and gives the staged figures beside it.
- **Verification:** run the README's two `run.py` commands at the fixed head and compare each cell.

### F2. MINOR. Conformance, Docs. `tb/verilator/ctrl_service_budget/README.md:822-823`: a partial figure sits under "every backlog window"

- **Authority:** the same README, line 538: "Nor is a partial figure: a re-measure that leaves out a backlog row names it". The same ruling owes corrected figures.
- **Evidence:** the column at line 820 is "Composed maximum, every backlog window". The 1x1, 4 KiB rows give "at least 87.17" and "at least 86.54". Each graded table says "Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill not run)".
  - The published staged, no-stage and `5b5f4336` tables all carry that line. My staged run reproduces the staged table byte for byte (`receipts/budget-1x1-xip64-table.md`).
  - In my staged run the two windows ran and were refused. Each committed GM 12 against a defined 15, and they are two of that row's 5 in the "probes refused" column (`receipts/budget-1x1-xip64.log`). The no-stage row grades the same 16 groups, but no published receipt gives its refusal text.
- **Impact:** a reader compares 87.17 with the older row's 94.91, which covers all four windows, and line 834 attributes the difference to firmware. Part of it is two missing windows, and the two windows missing is not stated. "At least" stays a true lower bound, so no figure is wrong. I am not sure this is wording only, so under the owner rule it is MINOR.
- **Required outcome:** both cells name the partial coverage, as the Passes table does at lines 294 and 296, and the text says why both windows are missing at each stage setting.
- **Verification:** compare each cell with `results.json`'s `composed_maximum` and `refusals`.

### RES-1. RESIDUE. Comment rule. Issue-comment IDs in new source text

- `sw/mailbox/census_ports.py:59` and `:302`: "ruling 6554243203". Exact fix: "(#665, #787)".
- `sw/mailbox/mailbox.yaml:84-85`: "the ruling on #665, comment 6553999730". Exact fix: "the ruling on #665".
- Line 302 is a table reason string, recorded here because it is the same kind of text. The reflowed `comment 6088423771` in `milan_soc.py` was already on both sides and is not new. The design page may keep its links.

### RES-2. RESIDUE. PR body, Status

"Not yet pushed: this body is prepared for the PR." is stale: the PR is open at this head. Exact fix: delete the sentence.

### Suggestions (no effect on the verdict)

- **S1.** The REBOOT terminal accepts any G output. A probe OR-ing `pp_tx_frames_w[0]` into `reboot_req_i` passes the census, rc 0 (`receipts/probe-reboot-second-output.log`). This is the author's open risk, and the ruling did not ask for it to be narrower. The placement switch removes the exclusion anyway.
- **S2.** "At no other input of that cell" holds: a probe driving `ms_tick_i` from the request is refused by `g-on-wire` in every shape (`receipts/probe-reboot-second-input.log`). From reading the plants, no in-tree arm proves it: the ruled arm reads the net outside that cell. An in-tree arm would keep it true.
- **S3.** The harness self-test does not notice the stage being removed: rc 0 with the call removed (`receipts/harness-selftest-nostage.log`). A build-time check, like `FACE_IDLE_INPUTS`, would hold the "as the product does" claim.

## Focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Conflict resolution in `97e9a3d3` | Holds. 7 files, 12 hunks recomputed. Both sides kept in every hunk. The merge differs from the auto-merged tree only in those 7 files and the 3 regenerated outputs | `receipts/merge-conflict-hunks.txt`, `merge-autotree-to-97e9a3d3.diff` |
| 2 | Rulings 6553999730 and 6554243203 | Implemented as ruled, nothing more. Face block stays minor 3, source entries are minor 4, `version.minor` 4. `src_stream_id_o` class C, `reboot_req_o` class G, terminal `reboot_ctrl.reboot_req_i`, named as an acceptance item, own arm refused by `g-on-wire`. No carrier added and no issue filed | `sw/mailbox/mailbox.yaml:63-85`, `census_ports.py`, `receipts/census.log` |
| 3 | Semantic conflicts | One missed: F1. Checked with no conflict: see the list below | below |
| 4 | Re-measured arms and corrected claim | Reproduced 2 of the 15 published arms; each table is byte-identical. F2 stands against one table's labelling | `receipts/budget-repro.txt`, `budget-1x1-none-stats.txt`, `budget-1x1-xip64-stats.txt` |
| 5 | All-fabric export | Holds for all five shipped configs. See below | `receipts/export-dev-vs-head.txt`, `export-dev-vs-dev.txt`, `export-tcl-sources.txt` |
| 6 | `MAILBOX_SPLIT.md` figures | All match: 41 reads of 22 of 26 nets, 4 unread, 219 ports (C 26, F 28, R 34, E 6, M 14, G 111), 139 arms, 43 rules, 525/570 and 532/577, model 490 of 532, 35 and 49 generator arms, reads 11 + 14 + 16 | `receipts/census.log`, `mbx-make.log`, `gen.log` |
| 7 | 2.3 and 2.4 citations | Holds. All 11 living citations read 2.4, and the generated page reads 2.4 by the generator. Dated records keep 2.3: `AREA_BUDGET.md:536,541`, finding 234 lines 22, 45, 61, baseline lines 451, 919, 1377. Other "contract 2.3" text names the face block | `receipts/citations.txt` |
| 8 | #70 PHY link gap and REBOOT carrier | Recorded out of scope by ruling. Not findings | issue comments 6553999730, 6554243203; `MAILBOX_SPLIT.md:1656` |

**Semantic checks with no conflict (item 3):**

- **#814:**
  - The only LiteSPI builds outside `MilanSoC` are the harness's and, through it, the boot SoC's.
  - A split export at this head carries the stage, the ICAPE2, the PHY hold and `pub_src_sid_o` (`receipts/split-export.log`).
  - The DRAM-side cuts are not built by these harnesses (`with_dram=False`).
- **#787:**
  - The cone stops at the named input. `reboot_ctrl`'s saved-state inputs read `F_NVM`'s class F carriers, which exist.
  - The boot grader's check set is unchanged, and both boots pass.
- **#818:**
  - `pp_resource_gate.py check-baseline` passes.
  - No split-side document states the old WNS rule. The remaining WNS text is dated measurement.
- **#70:**
  - The split platform has no PHY service, as ruled.
  - It never writes the two enables, so the "enable requested" reporting does not reach it. The trace is 18 of 18 equal.
- **Processor #205 and #206 against the firmware:**
  - `third_party/tsn-c-stack/src/acmp.c:427-430` zeroes an unsettled view's stream.
  - `sw/firmware/ctrl/app/ctrl_app_aecp.c:59` clears the three flags.
  - `acmp.c:971` echoes the listener fields on TALKER_UNKNOWN_ID.
- **#202:** `MAILBOX_SPLIT.md` already records "none yet" for the source entry writer.

**All-fabric export (item 5).** Dev and head were exported from one tree path, plus a second dev run as a noise control:

- Each config has 3,876 files on both sides. Every generated Verilog body line is equal.
- The TCL and XDC are byte-identical, and none of the 124 sources the TCL reads changed from dev to head.
- The remaining differences are run stamps, the hierarchy comment's order and the log's interleaving. Two dev runs differ the same way.
- `hdl/` differs from dev only in the three mailbox files, which no shipped config reads.
- The Arty configs ran at 100 MHz, as `MAILBOX_SPLIT.md` "Default build" records.

## Clean lens results

```text
[R759] PASS RTL - hdl/milan/mailbox/KL_mbx.sv, KL_mbx_pkg.sv, sw/litex/milan_soc.py at the head - merged decode, reset and read-back of source entries beside the face block; generator check, lint at ratchet, Yosys on the 3 mailbox tops, split export, no new crossing in the merge's own delta
[R759] PASS Robustness - tb/verilator/mbx/suite.hpp and suite_face.hpp at the head - holes, absent interfaces, partial strobes, reset and refused writes through both adapters and the model, 7 quick and 207 full mutants caught; two terminal probes; boot native controls 6 of 6
[R759] PASS Tests - sw/mailbox/census_plants.py:682, gen_mailbox.py arms, tb/verilator/mbx/mutants.py - the ruled arm is refused by g-on-wire; 139 arms, 43 rules none unproven; 87 generator results; 207 of 207; merged model mutants caught in the published campaign (570 of 570)
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | rulings, `mailbox.yaml`, `census_ports.py`, both harness READMEs, firmware against processor #205 and #206, export comparison | R759-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_pkg.sv`, `KL_pp_shadow.sv`, `milan_soc.py`, split export, lint, Yosys on 3 tops | R759-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Robustness | CLEAN | mbx suites, model, mutants, census probes, refused-window paths, boot controls | R759-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Tests | CLEAN | census self-test, generator self-test, mbx mutants, harness self-tests, published firmware campaigns | R759-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |
| Docs | UNCLEAN (F1, F2) | `MAILBOX_SPLIT.md`, both harness READMEs, `MARK_II_AREA_PLAN.md`, `SUBMODULES.md`, `CHANGELOG.md`, `MAILBOX_CONTRACT.md`, PR body | R759-1 | `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` |

RESIDUE leaves no lens unclean. A fix limited to the two READMEs, the two comment sites and the PR body changes no RTL or test artifact. The two comment sites are in `sw/mailbox`, whose digest the harness's `--reuse-build` attests, so existing harness builds must be re-attested.

## Commands run by this round at the head

All rc 0 unless stated:

- `gen_mailbox.py --check --crosscheck --selftest`.
- `publication_census.py --check --selftest --jobs 6`: 6 shapes, 246 checks, 139 arms.
- `make -C tb/verilator/mbx`, and `mutants.py --jobs 6`: 207 of 207.
- `ctrl_split_boot/run.py` at 1x1 and 8x8, the no-stage control at 1x1, and `--native-controls`.
- `ctrl_service_budget/run.py --self-test`.
- `ctrl_service_budget/run.py --point 1x1 --fetch-l1 none`: rc 0.
- `ctrl_service_budget/run.py --point 1x1 --xip --fetch-l1 64x1`: rc 1, as `run.py` reports refused probes, matching the author's rc for that arm.
- The two refused windows alone on that build: rc 1, as above.
- `lint_rtl.py --check`, `run.sh --top` for the 3 mailbox tops, and `pp_resource_gate.py check-baseline`.
- Five all-fabric exports three times, and one split export.
- Two census probes: the second-input plant returned rc 1, as a plant must; the second-output plant returned rc 0 (S1).

The clone is restored: tree, index, modes and the five submodule gitlinks verified, and the shared CPU netlist directory unchanged (`receipts/clone-restored.txt`).

## Prior public findings

No review finding on this PR predates this round.

## Real limits

- **Reproduced arms:** 2 of the 15 published arms, both 1x1. For the other rows, paths and composed figures were checked against the published tables. Their CPU-per-instruction, refill and worst-pass figures have no published raw receipt beyond the author's handoff table.
- **Not run here:** the firmware shards, LiteX simulations, builder bank, BDD, native sweep and docs workflow. For these I read the author's published receipts only. The published digests match the evidence manifest; 3 receipts differ from `SHA256SUMS` only because the manifest marks them path-redacted.
- **Environment:** LiteX ran on CPython 3.14.8 from the product tree, not CI's fresh 3.12.3. The Arty exports ran at 100 MHz.
- **Export scope:** export-level only. No bitstream was built.
- **No Vivado run:** physical calibration NOT RUN, no hardware, and field skips are not hardware proof.
- **Hosted evidence:** seen in progress and not accepted here. No manager source bank ran at this head, and none is claimed.
- **Noted outside this review:** `docs/testing/RUNNING_TESTS.md:84` and `CI_WORKFLOWS.md:451` say 64 suites, while the runner lists 65 on dev and on this head. This is dev's own text, not this merge's, so it is not a finding here.
- **Reading discipline:** a comment listing taken after my findings were formed showed the first line of the other reviewer's published report. I had not read its body when this verdict and ledger were written.

## Pending manager duties

- Carry RES-1 and RES-2 to the residue checklist, and route F1 and F2 to the executor.
- Re-review at the corrected head, covering Conformance and Docs again.
- Build and validate the current-dev merge candidate, accept hosted and act evidence, and hold the second positive and merge authorization.

R759-1 FINISHED
