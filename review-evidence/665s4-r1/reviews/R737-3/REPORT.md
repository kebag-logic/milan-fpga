[R737] NEGATIVE - exact head 7643aef613c5b87a246544f57d23ad9f1bf8311e

# R737-3: internal independent delta review of PR #812 (issue #665, S4, round 6)

Head `7643aef613c5b87a246544f57d23ad9f1bf8311e`, tree `17caf3136a3c92ede44987be7015e5288d8031c6`. Delta `4d9b901c..7643aef6`: the merge of `dev-soft-core` `a68536fa`, and round 6 under the ruling on #665 (issuecomment-6677095110), option (a).

One MINOR is open: R737-3-F1, under Conformance, Robustness and Docs. Two RESIDUE items and five SUGGESTIONs are also recorded. RTL and Tests are clean.

The split boot's code path is sound, and I reproduced its figures exactly. The defect is one step outside that path. The platform page's only documented link command still builds the placeholder image the ruling removes, and this delta deleted the page's warning about it.

My verdict and ledger were written to this file before I read any prior finding.

## 1. Focus results

**(1) The merge keeps both sides. Holds.**
- `git show --cc 36d12bd373` shows the two conflicted files, `split_soc.py` and `README.md`.
- `split_soc.py:373` wraps this lane's `FlashBoundary(pads, module, divisor)` in #814's `milan_soc.stage_spi_phy`, then builds `LiteSPI(..., with_master=True)`. That is the order `milan_soc.py:3871` uses.
- This lane's bank checks and `soc.csr.add('spiflash', ...)` remain.
- `README.md:129-130` keeps this lane's sentence and #814's. The module docstring (`split_soc.py:35-41`) keeps both.
- My 1x1 boot's `csr.csv` has one `spiflash` bank at `0xf0002800`, with phy, mmap and master registers. The stage adds no CSR.
- The stage is live: the published control removes that one call (`control-none.diff`) and the boot moves by 541 and 532 CPU cycles.

**(2) S3 takes the generated map. Holds on the boot path; see F1 for the documented link.**
- Each ruled item is present:
  - `ctrl_plat_image.py:101,126` accepts and forwards `--flash-map`.
  - `ctrl_split_boot/run.py:234-241` builds the shape's map and hands it to both links and both exports.
  - `boot_soc.py:63,96-98` calls `fixture_addresses(map)` and refuses a deviation.
  - `ctrl_configs.py:171-177` and both READMEs follow.
- Fresh runs of mine, on scratch copies of this head differing only in make job count:
  - 1x1: rc 0, `ctrl_split_boot: PASS (0 finding(s))`, ready at 84.372 ms, 4,218,617 CPU cycles.
  - 8x8: rc 0, `ctrl_split_boot: PASS (0 finding(s))`, ready at 184.622 ms, 9,231,088 CPU cycles.
  - Both match the published receipts to the cycle, with 18 of 18 writes equal.
- Self-test: I re-ran the native controls, 6 of 6 as required, and a regrade, which passes. The two plants rest on the published `splitboot-selftest.log` (rc 0, 2 of 2 caught). I did not rebuild them.
- The boot's image carries no flash placeholder. `nvm_flash_litespi.o` loads `0xf0003xxx` and `0x01000000`, and the final ELF has no `lui 0xf0004` anywhere. The two `lui 0x20000` left in that ELF are in `mbx_tx_send` and `aecp_command`, not the flash port (the only firmware source that includes the generated headers).
- Plant M1 links the final image with no map. The boot fails: no ready line, and the simulation exceeds its time limit. So the run detects a placeholder image.
- Refusal probes, 9 of 9 as required (`receipts/refusal_probe.log`): a clean `csr.csv` passes, and `map_deviations` catches a moved register, a moved timer register, an absent register, a moved window, a resized window and an absent window. A real `boot_soc.build` export refuses a moved register in the ruled words. `ctrl_plat_image.py` refuses a map clock that is not the shape's.

**(3) Figures are restated from receipts. Holds.**
- `scripts/figures_check.py` checks 35 figures, 0 mismatches. It covers the capture rows, every phase row, the boots, `slow-step`, the architecture line and S3's staged and none rows, against `target-*-table.md` and the `splitboot-*` and `control-none-*` logs.
- The fitted figures (11,066, 16,533, 265.8, 205.6, 9,499, 9,852) match `target-*-results.json`.
- The stage's cost arithmetic holds, and the largest UART difference across all three duties is 0.001 ms at each shape.
- A sweep of `docs`, `sw`, `tb`, `scripts` and the top-level pages finds none of the superseded values in a current statement. The only remaining mention, `ctrl_split_boot/README.md:90`, labels 84.393 and 184.658 ms as prior measurements.

**(4) docs.yml ran clean, with the pinned SDK verified. Holds, with one limit.**
- `docs-yml-table.md` has 71 steps at rc 0 and 24 NOT RUN, each with a reason. `verify.rc` is 0, and `tree-after` names this head with an empty status.
- All three SDK steps downloaded the archive, printed digest `d42680e9...`, and printed `SDK fresh installation: verified`. That digest is the pin in `scripts/ci_rv32_sdk.py` and `.github/workflows/docs.yml`.
- Limit: the replay driver is not in the published packet, so the empty `HOME` itself rests on the handoff's statement. The fresh-install path is consistent with it, since a retained `HOME` failed in round 5's STOP. See S5.

## 2. Findings

**R737-3-F1 | MINOR | Conformance, Robustness, Docs | `sw/firmware/ctrl/plat/README.md:91-92`; `sw/firmware/ctrl/test/ctrl_plat_image.py:13-15,101,126` | The only documented link command builds the placeholder image the ruling removes, and nothing warns of it.**
- Authority: the ruling says option (a) "leaves no F1 placeholder in any split image", and that option (b) "would re-admit the stand-in placement". AGENTS section 6 (`Docs`): changed contracts are reflected in authoritative docs.
- Evidence:
  - The page's command passes `--config`, `--csr-csv`, `--output`, `--libc` and `--compiler-runtime`, and no `--flash-map`.
  - No markdown page documents that flag on `ctrl_plat_image.py`. The two pages naming `--flash-map` (`ctrl_service_budget/README.md:135`, `nvm_split_target/README.md:61`) concern the other builder.
  - The delta removed the page's "Not yet done" item saying the flash port keeps its fixture addresses, and added only a sentence on what the simulation does (`:113-114`). So the warning went while the path stayed.
  - Run with those arguments and real archives, the builder exits 0 and links a valid ELF. M1's final link is that invocation, against the SoC's own `csr.csv`. Its `nvm_flash_litespi.o` loads the stand-ins (`lui 0xf0004` four times, `lui 0x20000` once).
  - The published REVIEW READY says the one no-map caller is the boundary gate and that it makes no image. That is true of code callers (`ctrl_runs.py:85`), but the page is a second, documented one that does make an image.
- Impact: a reader following the page gets a split image on stand-in flash addresses with no refusal and no warning. On the split SoC that image never reaches ready (`receipts/runs/boot-m1-final-link-no-map.log`).
- Why MINOR and not RESIDUE: the defect is in a command's output, a generated artifact, and it bears on the ruling's conformance claim. It is not wording alone.
- Required outcome: no documented or ordinary invocation yields a linked split image on the stand-ins without saying so. Correcting the page is the minimum: its command carries the map, the page says how the map is made, and it states what omitting the map does. A link-time refusal would also close it, provided the boundary gate's compile-only run still stops at its link.
- Verification: run the page's command as written, then confirm the flash port object carries the generated addresses and no `0xf0004` or `0x20000` load. If `ctrl_plat_image.py` changes, also re-run the firmware boundary gate and S3's boot at both shapes.

**R737-3-R1 | RESIDUE | Docs | `sw/firmware/ctrl/test/ctrl_plat_image.py:13` | A reworded source comment names a lane.**
"F1's flash port" uses a lane name, against the owner's comment rule. Exact fix: "the saved-state store's flash port". Existing instances elsewhere stay with #746.

**R737-3-R2 | RESIDUE | Docs | `sw/firmware/ctrl/test/ctrl_plat_image.py:101` | Help text is missing its possessive.**
Exact fix: "the split SoC's generated flash port map".

**R737-3-S1 | SUGGESTION | Tests, Robustness | `tb/verilator/ctrl_split_boot/boot_soc.py:96-98`; `split_soc.py:99`; `ctrl_runs.py:85` | The new guard has no lasting check. This extends R737-1-S2.**
The refusal works, but only out-of-tree probes show it. The published probe shows that removing it lets a moved register through the export, and no gate in the tree would notice. `map_deviations` is a pure function, so a moved register and a moved window are cheap self-test checks. No hosted job compiles `ctrl_plat_image.py` with a map either. I rate this optional because the simulation itself fails on a placeholder image (M1).

**R737-3-S2 | SUGGESTION | Docs | `tb/verilator/ctrl_service_budget/README.md:656,804,895` | S2's 8x8 counts no longer match what the harness gives, and need an owner.**
At this head the harness reports 57 of 182 (29 of 129 paths); the page says 66 of 182 (34 of 129). The page labels its figures as earlier measurements (`:146`, `:229-233`), so it is not false, and the ruling does not assign S2's figures. A one-line pointer would stop readers carrying the counts over. The author's reading of the cause is an unproved inference, as they say.

**R737-3-S3 | SUGGESTION | Docs | `docs/design/SPLIT_CONTROL_MEMORY.md:218,220` | The platform's size rows are no-map images.**
With the map, `rom` needs 109,552 B at 1x1 and 123,296 B at 8x8, against the page's 109,560 and 123,304. My no-map 1x1 link gives exactly 109,560. Tiles are unchanged at 39.0 and 52.0, and the rows are labelled as measured at `b8628704`, so this is no defect today.

**R737-3-S4 | SUGGESTION | Robustness | `ctrl_plat_image.py:126`; `ctrl_split_boot/run.py:234` | Two small consistency points.**
`ctrl_plat_image.py` does not resolve `--flash-map` as `ctrl_srp_image.py` does. This is harmless today, because the compile runs in the same working directory. `run.py` also restates `split-soc/flash-map` rather than using `split_soc.FLASH_MAP`.

**R737-3-S5 | SUGGESTION | Docs | published packet `author-r6` | Two scripts behind published claims are not published.**
`map_probe.py` and `run_docs_yml.py` are named by receipts but absent from the packet, so a cold reviewer cannot rerun them. My `scripts/refusal_probe.py` replaces the first, except its removed-guard arm.

## 3. Prior public findings at this head

| Finding | Disposition |
|---|---|
| R738-F1 (MINOR) | Stays resolved. `nvm_split_target/*.py` are unchanged since `4d9b901c`, and the self-test gives `checks: 73   failures: 0`. |
| R738-F2 (MINOR) | Stays resolved, on the same evidence. The published real-refusal and reuse probes pass at this head. |
| R737-1-R1 (RESIDUE) | Stays resolved: `docs/ARCHITECTURE_HW_SW_SPLIT.md:225` names both clocks. |
| R737-1-S1 (SUGGESTION) | Stays resolved: the receipts' tables and results carry their clocks. |
| R737-1-S2 (SUGGESTION) | Retained and widened by R737-3-S1. |
| R737-1-S3 (SUGGESTION) | Retained: `gen_flash_port.py:246` is unchanged. |
| R737-1-S4 (SUGGESTION) | Retained: neither portable self-test appears in `.github/workflows` or `scripts/suite_shards.py`. |
| R738-3-S1 (SUGGESTION) | Retained: `target_selftest.py` is unchanged. |
| R738-3-RES1 (RESIDUE) | Retained: "alone in their place" is still at `nvm_split_target/README.md:52` and `run.py:32`. "Leaves only" is still in the PR body at lines 30 and 162. |
| R737-2-R1 (RESIDUE) | Retained: the broken docstring is still at `target_selftest.py:201-203`. |
| R737-2-S1, S2 (SUGGESTION) | Retained: `run.py` and `target_selftest.py` are unchanged. |
| R737-2-S3 (SUGGESTION) | Retained, with R738-3-RES1. |

## 4. Clean lenses

[R737] PASS RTL - `git diff a68536fa 7643aef613 -- hdl '*.sv' '*.v' '*.c' '*.h'` (empty); `split_soc.py:343-379`; `milan_soc.py:2583-2625,3871`; `receipts/runs/boot-1x1.log` - No RTL or firmware C differs from `dev-soft-core`, so RTL was not re-reviewed. The stage wraps the boundary before LiteSPI reads its faces, as the product does, the boundary's pad connections keep the original endpoints, and both boots pass through it.

[R737] PASS Tests - `receipts/runs/boot-m1-final-link-no-map.log`; `receipts/refusal_probe.log`; `receipts/nvm_target_selftest.log`; `receipts/gen_flash_port_selftest.log`; `receipts/budget_selftest.log`; `receipts/native-controls.log`; `author-r6/receipts/runs/splitboot-selftest.log` - The boot's checks can fail for the defect at issue: M1 fails on a placeholder image. Self-tests give 73 and 33 checks with 0 failures, and `self-test: 0 failures` for the budget harness. The missing lasting check on the guard is S1, optional under the same reasoning three earlier rounds applied.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling 6677095110 against `ctrl_plat_image.py`, `run.py`, `boot_soc.py`, `ctrl_configs.py`; both boots; `plat/README.md:91-92` | R737-3 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| RTL | CLEAN | Empty `hdl` and firmware diff against `a68536fa`; `split_soc.py:343-379`; `milan_soc.py:2583-2625,3871`; boot `csr.csv` | R737-3 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Robustness | UNCLEAN (F1) | `ctrl_plat_image.py:101,126`; M1; `receipts/refusal_probe.log`; regrade | R737-3 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Tests | CLEAN | M1; refusal probes; target, flash map and budget self-tests; native controls; published plants, D5 plant and gate summaries | R737-3 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Docs | UNCLEAN (F1) | `plat/README.md`; `ctrl_split_boot/README.md`; `nvm_split_target/README.md`; `ctrl_nvm/README.md`; `ARCHITECTURE_HW_SW_SPLIT.md`; `receipts/figures_check.log`; docs.yml receipts | R737-3 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |

Coverage note: a page-only fix to F1 leaves RTL and Tests banked. A change to `ctrl_plat_image.py` un-covers Tests and needs them covered again.

## 6. Evidence and limits

- **Published evidence:** the 336 `author-r6` files all match `MANIFEST.json`, none missing and none unlisted. The evidence commit `2540f263` is unsigned, so this proves integrity against the manifest, not authorship.
- **Run by me:** two clean boots, plant M1, the refusal probes, three self-tests, the native controls and a regrade.
- **Not run by me:** the 97 short and 11 long gates, S4's cases, the S2 harness, the docs.yml steps and the two S3 plants. Those rest on hash-verified published receipts.
- **Toolchain:** my runs used the gate environment's RV32 SDK, which the author reports is not the pinned build, and the scoped Verilator 5.050, identity checked. They add no evidence about the pinned SDK. The author's comparison covers S3's and S4's images, not the S2 harness or the firmware campaigns.
- **Hosted checks:** at inspection most exact-head contexts were queued or in progress. `bdd-conformance`, `changes`, `docs-check-no-git`, `firmware-aecp-mutants`, `firmware-unit`, `full-ci-gate` and `verilator-lint` had succeeded, and the physical gPTP context was skipped, which is not execution. I draw no acceptance from these.
- **No manager source bank** ran at this head, and I claim none. Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- **Clone state:** no probe ran in the clone. `receipts/restore-check.txt` records the exact head and tree, an empty status, index equal to head, 0 blob mismatches and all six gitlinks at their recorded commits (`external` not checked out, as at the start).

## 7. Pending manager duties

- Route F1, then re-review the corrected commit.
- Carry R737-3-R1, R737-3-R2 and the retained RESIDUE items to the residue checklist.
- Own hosted and act acceptance at the final head.
- Build and validate the current-dev merge candidate (live `dev` `87e9d03a`), and link its receipts.
- Decide the two questions the author raised: whether the gate environment moves to the pinned SDK, and who owns S2's 8x8 figures.

R737-3 FINISHED
