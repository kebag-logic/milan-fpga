[R841] POSITIVE - exact head 8e523a2b17faf17c4564e5af155b73f95dc2a0a5

Round R841-2 is the internal cleared-context review of PR #913 (issue #911, the XC7A200T variant of the ALINX AX7101 board). It is a delta review from the round-1 head `4958ca4f` to the head `8e523a2b17faf17c4564e5af155b73f95dc2a0a5` (tree `2c53a871df1f717ba7cb72f77147c549155beed5`, base and live dev `b7d692952305e4e0e132abb8f99c339eeb17a873`): six commits by the executor.

**Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR finding is open.
- Every round-1 finding of both reports is closed at its cause: R841-1 F1-F3 (MINOR), F4 and F5 (SUGGESTION) and RS1, and R842-1 F1 (MINOR) and R1.
- This round adds five SUGGESTIONs and three RESIDUE items, all listed below, so the author can take them in one pass.
- All five lenses were applied and each is clean at this head.

## Authority reconstructed

- AGENTS.md and CONTRIBUTING.md (roles, lenses, completion bar). docs/README.md for the document map.
- Issue #911: scope, acceptance 1-4, and the two maintainer scope changes (issuecomment-6876968816: integrator docs instead of a kit; issuecomment-6877123911: the "Flash an image set over JTAG" section and the `INSTALLED_BUILD` definition). #818 sets the WNS +0.030 ns / WHS 0 ns floor at every signoff corner.
- Interface authorities: `docs/integration/QSPI_FLASHBOOT.md`, `docs/guides/BOARD_DEPLOYMENT.md`, `docs/integration/BUILDING.md`.
- Delta: `git diff 4958ca4f..8e523a2b` (9 files, +205/-27) and its six commits. The whole PR was checked against `b7d69295..8e523a2b` where the delta depends on it.
- Evidence: the author packet `review-evidence/911-r1/author-r2` at archive `489e06bd`, and the REVIEW READY round 2 comment on #911. Prior review findings were read only after this round's own pass over the diff.

## Evidence integrity

- `receipts/evidence-verify.txt`: all 295 entries of the archive's `MANIFEST.json` match their published sha256, and no file is unlisted. All 95 rows of `author-r2/receipts/INDEX.md` match in bytes and in their sha256 prefix.
- `author-r2/receipts/gates/workflow-steps.md`: 150 steps rc 0 and 522 NOT RUN, each with a reason. That matches the claimed 150/522. `gates/lane-gates.txt` lists 27 lane gates at `8e523a2b`, all rc 0.
- The Verilator shards were not re-run. That holds: the delta touches no file under `hdl/`, no testbench, no platform, no `milan_soc.py`, no `flash_map.py`, no `layout_from_soch.py` and no config (`git diff --stat 4958ca4f HEAD -- hdl sw/litex/platforms sw/litex/milan_soc.py sw/litex/flash_map.py sw/litex/layout_from_soch.py configs` is empty).

## Round-1 findings at this head

| Finding | Status | Evidence at 8e523a2b |
|---|---|---|
| R841-1 F1 (MINOR, Tests) | CLOSED | `sw/builder/test_builder.py:19131-19160`: `on_200t()` sets the bitstream budget and the AEM offset to `0xA00000`, pads the payload to 9,730,652 B, then requires writes `[0xA00000, 0]` through `build.sh flash ax7a200t`, with the payload at 0 and `aem_desc.bin` at `0xA00000` on readback. `sw/builder/test_timing_grade.py:216-273` (`test_layout_from_soch`) renders a soc.h per die with LiteX's `get_soc_header` and the SoC's own `_add_flashboot_constants`. It asserts the budget equals the AEM offset (0x400000 and 0xA00000) and the layout equals the SoC's export. It also checks the flash device `n25q128a13`/0x20BA18 and that the 200T payload passes `validate_artifact_pair`. The builder gate `test_commercial_timing_grade` (`test_builder.py:29564`) runs it. Reproduced: K7 turns both timing-grade gates red, and K9 turns gate 1e and both timing-grade gates red (`receipts/probes.txt`). |
| R841-1 F2 (MINOR, Conformance, Docs) | CLOSED | `guide-run/02-update-200t-D-to-R.rc` and `03-...R-to-D.rc` are both 0. `stub-calls.log` shows the AEM written at 10485760, then the bitstream with `-f`, with the payload at 0 and the AEM at 0xa00000 on readback. The REVIEW READY round 2 acceptance 4 states that the second set is the delivered one with one payload byte changed. The AX7101 release's raw reports are now published (`ax7101-release/*.rpt`, device `7a100t-fgg484`). This round recounted their CDC rules against build C's: the same eight rules (CDC-2/3/5/6/9/10/15/26). Clock-interaction rows differ only in slack values. |
| R841-1 F3 (MINOR, Conformance, Docs) | CLOSED | `docs/guides/BOARD_DEPLOYMENT.md:309-345` ("The board check", "Image sets built before #911") states three things. A layout without `flash_device`/`flash_jedec_id` is refused as a target and still serves as `INSTALLED_BUILD`. The remedies are a rebuild, regenerating from the build's soc.h, or the plain JTAG commands with P and O set by hand. The check has run against a stub programmer only, with no bench run on either board. `docs/integration/QSPI_FLASHBOOT.md:91-107` repeats this for both boards. Receipts `05` (rc 2: refused after `--detect` only, no dump or write), `06` (the guide's regeneration command, rc 0) and `07` (rc 0) run the stated path. |
| R841-1 F4 (SUGGESTION) | CLOSED | `test_builder.py:19105-19113` adds two disagreeing JEDEC IDs, a 100T+200T chain and two 100T dies, on flash-pair, flash and flash-images, each refused with no dump or write. K3, K4 and the reviewer's distinct-model control R1 each turn gate 1e red. |
| R841-1 F5 (SUGGESTION) | CLOSED | `vivado-buildC-route/*_timing_summary.rpt` (raw Vivado output read from build C's routed checkpoint). Slow 0/85 C: WNS 0.174, WHS 0.102. Fast 0/85 C: WNS 1.633, WHS 0.036. TNS/THS 0, WPWS 0.264. All corners meet the #818 floor and match the stated figures. `buildC_route_cdc_details.rpt` equals the signoff CDC report below its header; this round diffed it. |
| R841-1 RS1 (RESIDUE) | CLOSED | `BOARD_DEPLOYMENT.md:394` reads "The JTAG cable is a Digilent FT232H.", which agrees with `:26`. The PR body says the same. |
| R842-1 F1 (MINOR, Conformance, Docs) | CLOSED | `docs/integration/BUILDING.md:472-491` scopes each die's slot and AEM offset in a table, names `FLASHBOOT_BITSTREAM_SLOT` and `layout_for()`, and keeps the ROM and 64 KiB facts. It agrees with `flash_map.load_map()` for both dies (`building-vs-load_map.txt`) and with the guide's generated table. Every other 4 MiB / 0x400000 statement on the four pages is scoped: the AX7101 section of the QSPI page, `QSPI_FLASHBOOT.md:252`'s new bullet, `BAREMETAL_FIRMWARE.md:103-108` and the `build.sh:62-64` comment. |
| R842-1 R1 (RESIDUE) | CLOSED | `BUILDING.md:312,363` name `BUILD_DIES`, which exists at `scripts/check_sweep_shape.py:73`. |

## The round's new behaviour

- **Chain of two equal dies:** `sw/litex/qspi_owner_transition.py:334-341` now counts the `model` lines one per line rather than as a set. The control is in `test_builder.py:19110-19112`. Reverting the check to distinct models (`len(set(models)) != 1`, probe R1) turns gate 1e red with "two XC7A100T devices on one chain flash-pair: accepted".
- **First-check message:** `sw/litex/deploy.sh:249` now reads "the image set's layout or the FPGA on the cable fails the board check". check-board prints its specific reason first (receipt `05` shows both lines). No gate reads this line: reverting it (probe R5) leaves gate 1e green. See S1. The refusal itself (rc 2, no programmer I/O past `--detect`) is controlled.
- **No gateware input changed.** Between the image commit `1e604e1b` and the head, the only changes outside docs, tests and scripts are these four:
  - `milan_soc.py`: a type annotation and an import.
  - `build.sh`: a comment.
  - `deploy.sh`: the message and comment.
  - `qspi_owner_transition.py`: the chain count.

  None of them is a build input. That agrees with the author's identity receipts (`identity/identity-ax7a200t-8e523a2b.txt`: 150 build inputs, list `b77eb73a76bf9acc` at both commits and in build C's own clone; outputs identical apart from generated-on stamps). So the delivered image stands.

## Reviewer probes (this round)

`scripts/r841_2_probes.py`. Ten cases, each in its own clone of the head with the submodules at their gitlinks, run concurrently. Result: `receipts/probes.txt`, 10/10 expectations met, rc 0; logs in `receipts/probe-logs/`.

| Case | Edit | Result |
|---|---|---|
| BASE | none | gate 1e, `test_timing_grade.py` and `test_commercial_timing_grade` all rc 0. Both timing logs print the `test_layout_from_soch` line. |
| K3 | `len(ids) != 1` -> `not ids` | gate 1e red: "two disagreeing JEDEC IDs in the flash read flash-pair: accepted" |
| K4 | `len(models) != 1` -> `not models` | gate 1e red: "an XC7A100T and an XC7A200T on one chain flash-pair: accepted" |
| K7 | layout_from_soch budget fixed at 0x40_0000 | both timing-grade gates red (budget 4194304 against the AEM at 10485760) |
| K9 | deploy budget capped at 4 MiB | gate 1e red ("installed bitstream payload 9730652 B exceeds 4194304 B slot"); both timing-grade gates red |
| R1 | the chain count back to distinct models | gate 1e red: "two XC7A100T devices on one chain" |
| R2 | deploy.sh emits the AEM row at 0x400000 | gate 1e red: writes `[(1, 4194304, ...aem.fbi), (2, 0, ...)]` |
| R3 | `FLASHBOOT_BITSTREAM_SLOT = {}` | both timing-grade gates red (the guide's variant table differs from the source) |
| R4 | the 200T arm keeps the AX7101 map | gate 1e red: the 9,730,652-B payload exceeds the 4 MiB slot, so the arm truly runs on the 0xA00000 map |
| R5 | first refusal line reverted | gate 1e green, as expected (S1) |

Gates also run here in the head clone (`receipts/gates/*.rc`, all 0):
- `git diff --check b7d69295 HEAD` and `docs_inventory.py --check`;
- `check_doc_style`, `check_doc_paths` and `docs_check`;
- `check_sweep_shape`, `check_deploy_shape` and `check_solution_docs`;
- `board_variants.py` with `--selftest`;
- `check_py_idiom` and `check_sh_idiom`;
- `build.sh ax7a200t --dry-run` and `build.sh ax7101 --dry-run`.

`shellcheck` is not installed on this host (rc 127), so it was not run.

The installed programmer (v1.2.0) still contains the format strings the parser reads: `\tmodel  %s`, `read %x` and `JEDEC ID: 0x%06x`. It also has its own "more than one FPGA found / Use --index-chain" refusal.

## Findings

### S1 - SUGGESTION - Tests - `sw/litex/deploy.sh:249`; `sw/builder/test_builder.py:19074-19097`

- **Evidence:** probe R5 reverts the round's new first-refusal wording and gate 1e stays green. `refuse_board` checks check-board's reason (`needle`), not deploy.sh's summary line.
- **Impact:** none on behaviour. The refusal, rc and absence of I/O are all controlled. Only the line the round changed can drift unseen.
- **Suggested outcome:** in the `bridge=False` arms, also assert "fails the board check" in the output.
- **Verification:** R5 turns gate 1e red.

### S2 - SUGGESTION - Tests - `sw/builder/test_builder.py:19141`

- **Evidence:** `on_200t()` writes `0xA00000` by hand rather than reading `flash_map.layout_for(...)` or `FLASHBOOT_BITSTREAM_SLOT`. It needs no LiteX for that, since `flash_map.literal` reads the source.
- **Impact:** if the slot table changes, gate 1e keeps testing the old map. The drift itself is caught elsewhere: R3 and K7 go red in the timing-grade gates.
- **Suggested outcome:** derive the value in the gate from `flash_map.load_map("xc7a200t-fbg484-2")`.
- **Verification:** a changed slot entry moves the gate's expected offsets with it.

### S3 - SUGGESTION - Robustness, Docs - `docs/guides/BOARD_DEPLOYMENT.md:67-76` with `:343-345`

- **Evidence:** on a pre-#911 layout the guide's read snippet prints a `KeyError` traceback, then continues and echoes "part , entity model at , flash ID " with P and O empty. The shell rc is 0: author receipt `guide-run/04-read-layout-old-X-no-flash-id.{log,rc}`.
- **Impact:** the guide does say "Set `P` and `O` by hand" for such sets, but 270 lines later. A reader who runs the snippet first gets empty, unquoted `$P`/`$O` in the write commands. This round did not verify, without hardware, how the programmer parses those commands.
- **Suggested outcome:** make the snippet fail closed, for example `|| { echo "layout names no flash_jedec_id: set P and O by hand"; false; }`, or use `d.get` and test `[ -n "$O" ]`. Alternatively, point to "Image sets built before #911" from the top section.
- **Verification:** the snippet run on a pre-#911 layout exits non-zero with that message.

### S4 - SUGGESTION - Docs - `docs/guides/BOARD_DEPLOYMENT.md:333-337`

- **Evidence:** the regeneration command rewrites `$B/flashboot_layout.json` in place. The rewritten layout drops `erase_block`, `flash_size` and `reserved` (author receipt `guide-run/X-layout-diff.txt`). It still flashes (receipt `07`, rc 0).
- **Impact:** an integrator loses the original layout file without warning.
- **Suggested outcome:** say that it overwrites the layout, and suggest keeping a copy.
- **Verification:** the docs gates pass with the sentence present.

### S5 - SUGGESTION - Robustness - `sw/litex/qspi_owner_transition.py:290,334-341`

- **Evidence:** `_DETECT_MODEL` matches only `xc7a\d+`, so a chain of one Artix-7 plus another 7-series family (`xc7k`, `xc7s`, `xc7z`) counts as one device. The programmer's own "more than one FPGA found" refusal backs this at write time.
- **Impact:** none on this board, which has a single device.
- **Suggested outcome:** either count every `model` line, or keep the Artix-7 scope and state it (see RS-1).
- **Verification:** a planted `xc7k` second device refuses, or the wording states the scope.

### RS-1 - RESIDUE - Docs - the PR body's `qspi_owner_transition.py, deploy.sh` row; `sw/litex/qspi_owner_transition.py:334`

- **Evidence:** the PR body says check-board refuses "a JTAG chain with more than one 7-series device". The code comment says "One entry per chain device". The code counts Artix-7 (`model xc7a…`) lines only.
- **Exact fix:**
  - PR body: "a JTAG chain with more than one Artix-7 device".
  - Comment: "One entry per Artix-7 device on the chain, so a chain of two equal dies is refused too: ...".

### RS-2 - RESIDUE - Docs - `sw/litex/deploy.sh:248`

- **Evidence:** the comment "The reason above: a layout naming no flash device, or the die." omits the third cause the first check-board call refuses: a detect output naming no single FPGA model.
- **Exact fix:** "# check-board printed the reason above: a layout naming no flash device, a chain with no single Artix-7 model, or another die."

### RS-3 - RESIDUE - Docs - `docs/integration/BAREMETAL_FIRMWARE.md:103`

- **Evidence:** "The offsets above are the AX7101's." The journal slot offsets in that table (`0xEE0000`, `0xEF0000`) are the XC7A200T's too: `flash_map.load_map("xc7a200t-fbg484-2")` keeps the journal at `0xEE0000`.
- **Exact fix:** "The bitstream and AEM rows above are the AX7101's; the journal slots are the same on both dies."

There are no new instances of the comment rule in the delta. A scan of the added lines under `sw/` and `scripts/` found no lane label, review round, reviewer ID or issue-comment ID.

## Lens results

```text
[R841] PASS Conformance - issue #911 acceptance 1-4 and issuecomment-6876968816/-6877123911; docs/integration/BUILDING.md:472-491; docs/guides/BOARD_DEPLOYMENT.md:289-345,384-396; docs/integration/QSPI_FLASHBOOT.md:44-112,252; author-r2 guide-run 01-07 receipts and stub-calls.log; vivado-buildC-route/*_timing_summary.rpt; identity/identity-ax7a200t-8e523a2b.txt; git diff 1e604e1b..8e523a2b - acceptance 1 (every corner at or above the #818 floor, raw reports), 2 (header part, hashes unchanged), 3 (AX7101 inputs identical, the layout's two new fields stated), 4 (update step rc 0 both ways on 200T sets, refusals controlled, untested-on-silicon and stub-only stated for both boards); delivered image still stands
[R841] PASS RTL - git diff --stat 4958ca4f..8e523a2b -- hdl sw/litex/platforms sw/litex/milan_soc.py sw/litex/flash_map.py sw/litex/layout_from_soch.py configs (empty); git diff 1e604e1b..8e523a2b -- sw/litex/milan_soc.py sw/litex/build.sh (annotation and comment only); vivado-buildC-route/buildC_route_{Slow,Fast}_{0,85}C_timing_summary.rpt and buildC_route_cdc_{summary,details}.rpt against ax7101-release/*.rpt - no gateware input in the delta; per-corner WNS/WHS/TNS/THS and CDC rule counts match the stated signoff and the AX7101 release; prior RTL coverage depends on nothing the delta touched
[R841] PASS Robustness - sw/litex/qspi_owner_transition.py:287-364; sw/litex/deploy.sh:223-261,474,491,534,564-574; programmer v1.2.0 format strings; probes K3, K4, R1, R2 - two disagreeing IDs, mixed and equal-die chains, a deviceless layout and the AEM offset each refused or caught before any dump or write; only flash, flash-images and flash-pair write, and all three call prove_board; S3 and S5 are optional
[R841] PASS Tests - sw/builder/test_builder.py:18666-18684,19074-19160,29553-29565; sw/builder/test_timing_grade.py:216-273,310-312; receipts/probes.txt (K3, K4, K7, K9, R1-R4 red; R5 green as designed); author mutants/K3-K4-K7-K9-at-head.txt and K9-words-C1-C2-at-head.txt - each new test fails for the defect it names; S1 and S2 are optional
[R841] PASS Docs - docs/guides/BOARD_DEPLOYMENT.md (delta), docs/integration/BUILDING.md (delta), docs/integration/BAREMETAL_FIRMWARE.md:96-108, docs/integration/QSPI_FLASHBOOT.md (delta); PR #913 body; REVIEW READY round 2 comment; receipts/gates doc_style, docs_inventory, doc_paths, docs_check rc 0; comment-rule scan of the delta - the changed contracts are stated, every 4 MiB claim is scoped, and the evidence is openable; RS-1..RS-3 are residue, S3 and S4 optional
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #911 acceptance 1-4 and both scope comments; BUILDING.md:472-491; BOARD_DEPLOYMENT.md:289-345,384-396; QSPI_FLASHBOOT.md:44-112,252; guide-run 01-07 receipts; build C raw timing/CDC reports; identity receipts; diff 1e604e1b..head | R841-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| RTL | CLEAN | delta file list (no hdl/platform/SoC/flash-map/config change); milan_soc.py and build.sh diffs since 1e604e1b; buildC_route per-corner timing summaries and CDC reports against ax7101-release reports | R841-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Robustness | CLEAN | qspi_owner_transition.py:287-364; deploy.sh:223-261,474,491,534,564-574; programmer format strings; probes K3, K4, R1, R2 | R841-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Tests | CLEAN | test_builder.py:18666-18684,19074-19160,29553-29565; test_timing_grade.py:216-273,310-312; reviewer probes (10 cases); author mutant receipts | R841-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Docs | CLEAN (RS-1..RS-3 residue) | BOARD_DEPLOYMENT.md, BUILDING.md, BAREMETAL_FIRMWARE.md, QSPI_FLASHBOOT.md deltas; PR body; REVIEW READY round 2; docs gates rc 0; comment-rule scan | R841-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |

## Real limits

- **No hardware was touched.** Physical calibration was NOT RUN, and field skips are not hardware proof. The board check has run only against stub programmers, here and in the author's receipts.
- **No Vivado run.** The timing, CDC and IO figures are the author's raw Vivado reports, read and recounted here, not regenerated. The 9.7 MB bitstream is not published, so its header part and sha256 were not re-read.
- **Gateware identity was not re-elaborated.** It was checked by inspecting the source diff since `1e604e1b` and against the author's identity receipts.
- **No manager source bank** runs at this head, and none is claimed or inferred. The full parent, Verilator, Yosys and LiteX-simulation banks were not run. The 150-step pass and the 65/65 sweep from round 1 are the author's receipts.
- **Not run here:** `shellcheck` (not installed), the em-dash renderer gate and the handover-layout `board_variants.py --layout` gate. The handover layout sits in a private path.
- **Hosted checks were read only** (`receipts/hosted-checks-8e523a2b.txt`, read at 2026-11-14T20:41:15Z): 9 success, 1 skipped (the nightly physical job), 11 in progress and 30 queued.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts. Live dev is `b7d692952305e4e0e132abb8f99c339eeb17a873`, equal to the source base.
- Own hosted and local-replica acceptance at the exact head, including `verilator-suites` and `yosys-portability` once they finish.
- Carry RS-1, RS-2 and RS-3 to the residue checklist. Offer S1-S5 to the author.
- The handover links the guide at `1e604e1b`. If the PR is squash-merged, confirm that commit stays reachable, or relink to the merged commit.
- Out of scope and pre-existing: #912 (`qspi_owner_transition.py --self-test` NameError) and BAREMETAL_FIRMWARE.md's journal-slot "read and written" wording, which needs its own issue.

R841-2 FINISHED
