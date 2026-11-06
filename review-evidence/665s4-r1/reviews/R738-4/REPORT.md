[R738] NEGATIVE - exact head 7643aef613c5b87a246544f57d23ad9f1bf8311e

External cleared-context review R738-4 of issue #665 / PR #812, S4 rounds 5 and 6. Tree `17caf3136a3c92ede44987be7015e5288d8031c6`. Delta `4d9b901c..7643aef6`: the merge of `dev-soft-core` `a68536fa` and the ruling's option (a) (issuecomment-6677095110). Lane-only delta: `git diff 36d12bd3..7643aef6`, nine files.

## Verdict

NEGATIVE: one MAJOR and two MINORs are open.

Most of the round holds, and I reproduced much of it:

- The merge keeps both sides, and the map reaches both links and both exports.
- The refusal works.
- Every restated S3 and S4 figure I checked equals its receipt.
- `docs.yml` installed and verified the pinned SDK.

The MAJOR is the ruling's stated result. Following the platform page's own link command gives, with exit 0 and no warning, a split image on the F1 placeholders, and that image hangs before its banner on the boot SoC. The PR says the no-map path has one caller, which stops at its link. That is not so.

## Findings

**R738-4-F1 | MAJOR | Conformance, Robustness, Docs | `sw/firmware/ctrl/plat/README.md:88-92`; `sw/firmware/ctrl/test/ctrl_plat_image.py:101,126`; PR body line 213 | The documented platform link still produces a split image on the F1 placeholders, silently.**
- Authority: the ruling says option (a) "leaves no F1 placeholder in any split image" and rejects option (b) for re-admitting the stand-ins. The PR body (line 213) and the REVIEW READY comment limit the no-map path to "one caller", the boundary gate, "so it produces no image".
- Evidence:
  - The page's command at lines 91-92 has no `--flash-map`. The delta removed the "Not yet done" item for F1's port from this same page and left the command unchanged.
  - Run as written with real archives and a real `csr.csv`, it exits 0 and passes the link audits (`receipts/nomap-probe.txt`).
  - In its disassembly, `ls_call_begin`, `ls_late`, `ls_now_us` and `nvm_flash_litespi_power_on` take `lui 0xf0004`, the stand-in `timer0` at `0xf0003800`, where the mapped image has `0xf0003`. `ls_read` adds `lui 0x20000`, the stand-in window (`receipts/nomap-disasm.txt`).
  - Booted on the boot SoC through `run.py`'s own `export`, `verilate` and `grade`, it never reaches ready: `transcript ''`, `simulation exceeded its time limit` (`receipts/nomap-boot.log`). The same driver given the mapped image passes at 84.372 ms, so the image is the cause, not the driver (`receipts/mapped-boot-control.txt`).
- Impact: anyone linking the platform image as its page says gets an image with no refusal and no diagnostic, and it hangs before its first UART byte. On the split SoC map, its stand-in master address `0xf0003000` is `timer0`'s bank. Nothing ships this image at this base, which limits the reach but not the defect. The page has also lost the "Not yet done" warning that used to cover it.
- Required outcome: no documented or default path links a split platform image on the stand-ins. The page's command must carry the map and say where it comes from. A link without a map must not succeed silently. The boundary gate's compile-only use may stay, with `ctrl_runs.stopped_at_link` still true for it. PR line 213 must state what is then true.
- Verification: the page's command, as written, gives an image with no `0x20000` window or `0xf0003800` timer constant in `ls_*`. A link with no map is refused or cannot produce an ELF. `firmware_boundary`, both modes, stays rc 0. Re-running `scripts/nomap_probe.sh` shows the change.

**R738-4-F2 | MINOR | Docs | `tb/verilator/nvm_split_target/README.md:158`; `sw/firmware/ctrl_nvm/README.md:338`; PR body lines 53, 98, 99 | Figures not restated at the merged head.**
- Evidence, the current writer's maximum:
  - Both pages say "its 8x8 maximum of 13.863 ms stays gated". The merge brought `14e956f0c6`, and the gated receipt at this head reads `"maximum_ms": 13.86052` (`tb/verilator/nvm_capture_cpu/measurements.json:488,1350`).
  - `measurements.json` holds 13.86328 at `4d9b901c` and 13.86052 at `a68536fa` and at this head.
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1678` states the new figure and names 13.86328 as the previous one.
  - The hand-off says "no stale old figure on any page". The 2-decimal "13.86 ms" lines remain right.
- Evidence, the PR body:
  - Lines 98-99, in the Description and not marked historical, still give `nvm_store_boot` as 100.5 / 165.1 / 488.5 / 745.1 ms and the capture fit as 11,062 + 263.7 and 16,500 + 205.5. Those are pre-merge figures; the head's are 101.0 / 166.0 / 490.4 / 748.7 ms and 11,066 + 265.8 and 16,533 + 205.6.
  - Line 53, in the historical status, says "that writer and its harness are unchanged since", which no longer holds for its measurement.
- Impact: the pages name a value the gated receipt does not hold, and the PR's body gives two values for one measurement. The difference is 0.003 ms and no bound is near it. It is not RESIDUE because each fix changes a stated figure.
- Required outcome: the two pages give the receipt's figure, 13.861 ms or 13.86052. PR lines 98-99 are restated or marked historical. Line 53 stops saying unchanged.
- Verification: `rg '13\.863'` finds it only where the design page records history, and `check_nvm_capture.py` stays rc 0.

**R738-4-F3 | MINOR | Tests | `tb/verilator/ctrl_split_boot/boot_soc.py:96-98`; PR body lines 180, 233 | The ruled refusal has no committed negative test.**
- Authority: the ruling's "refuses a deviation"; AGENTS.md section 5, "add or update self-checking tests for changed behavior", and failure paths.
- Evidence:
  - The guard is correct. On a real `csr.csv`, `map_deviations` returns empty for the true map and names a shifted register, a stand-in timer register and a stand-in window (`receipts/portable-checks.txt`).
  - Nothing in the tree exercises the guard or `map_deviations`: no reference in `selftest.py`, no plant in `run.py`'s `PLANTS`, no native control. So by that search, not by a run, deleting those three lines would leave every in-tree check green.
  - The author's hand-off says so: "a probe, not a self-test in the tree". The PR heads it "New check" and ticks "New or changed behavior has self-checking tests".
  - `map_probe.py` is not in the published packet, so its 318-byte log cannot be reproduced from public state.
  - This is the same class as R737-1-S2, kept optional for `split_soc`'s own guard. It is MINOR here because this refusal is a ruling item, new in this delta, and its only evidence is an unpublished probe.
- Impact: a later edit can remove the guard with every gate green. Round 5's break already showed that no hosted job runs this path.
- Required outcome: a committed negative check that fails when the guard goes, and accepts a true map. The function needs no build, so it can be portable. The PR text must match what is in the tree.
- Verification: the check is red with `boot_soc.py:96-98` removed, or with `map_deviations` returning empty, and green at the head.

**R738-4-RES1 | RESIDUE | Docs | `tb/verilator/ctrl_split_boot/README.md:76` | An issue-comment ID on a page.** Exact fix: "(#665, decision 6677095110)" to "(#665)".

**R738-4-RES2 | RESIDUE | Docs | `sw/firmware/ctrl/test/ctrl_plat_image.py:13` | New lane label in a docstring (comment rule).** Exact fix: "F1's flash port" to "the saved-state flash port".

**R738-4-RES3 | RESIDUE | Docs | `tb/verilator/ctrl_split_boot/run.py:6` | "all outside the checkout" is no longer true.** `build.flash_map` reaches `soc_export`, whose end-station build writes the checkout's ignored directories. My runs left `configs/generated/ltn_rom.hex`, `ucode.hex` and `sw/builder/out/`. Exact fix: "Builds, in order, under --build-dir, apart from the end-station builder's ignored outputs in the checkout:".

**R738-4-S1 | SUGGESTION | Docs | `tb/verilator/ctrl_service_budget/README.md:146` | S2's 8x8 count.** I do not file 57 of 182 against the page's 66 as a defect. The page says its figures have "not been measured again at this head" and were measured on the stand-ins. Optional: one sentence saying a whole-run count does not carry across images. The owner question stays open for the manager.

**R738-4-S2 | SUGGESTION | Tests | `sw/firmware/ctrl/test/ctrl_configs.py` entry for `run.py` | No hosted job runs the split boot.** Round 5's break was invisible to CI. Optional: a hosted or portable check of the call chain, as a new Issue.

## Prior findings at this head

| Finding | State at `7643aef6` |
|---|---|
| R738-F1 (MINOR) | Remains resolved: the run receipts carry `cpu_hz` 50,000,000 and `sys_hz` 100,000,000 and name them above each table. `tb/verilator/nvm_split_target/*.py` is untouched by the delta. |
| R738-F2 (MINOR) | Remains resolved: same files untouched; `checks: 73   failures: 0` re-run; `real-refusal-*` and `reuse-probe` receipts rc 0. |
| R737-1-R1 (RESIDUE) | Remains resolved: section 5 still names both clocks. |
| R737-1-S1 (SUGGESTION) | Remains resolved. |
| R737-1-S2 (SUGGESTION) | Retained for `split_soc`; its placement half is now also F3. The map-clock refusal works (`receipts/mapflag-probe.txt`) and has no committed control. |
| R737-1-S3 (SUGGESTION) | Retained: `gen_flash_port.py` is untouched by the delta. |
| R737-1-S4 (SUGGESTION) | Retained: the target self-test is still in lane gates only. |
| R737-2-R1 (RESIDUE) | Retained: the docstring break at `target_selftest.py:201-203` is unchanged. |
| R737-2-S1, S2 (SUGGESTION) | Retained: files untouched. |
| R737-2-S3 (SUGGESTION), R738-3-RES1 (RESIDUE) | Retained: "alone in their place" stands at target README:52, `run.py:32` and PR body line 85. Fix as R738-3-RES1 gives it. |
| R738-3-S1 (SUGGESTION) | Retained: `target_selftest.py` is untouched. |

## Per-lens results

[R738] UNCLEAN Conformance - `git show --cc 36d12bd3`; `ctrl_plat_image.py`; `boot_soc.py:61-98`; `run.py:229-245`; `plat/README.md:88-92` - Applied against the ruling's items 1 to 4. Open: F1.
- Focus (1) holds. `split_soc.py:373-374` stages this lane's `FlashBoundary`, with `with_master=True`. Both README hunks keep both sentences. My boot SoC's `csr.csv` has one `spiflash` base at `0xf0002800` holding the PHY, mmap and master registers, master at `0xf0002810`, `timer0` at `0xf0003000`, window at `0x0100_0000` (`receipts/boot-soc-csr-rows.txt`).
- Focus (2) holds for `run.py`: the map reaches both links and both exports. It fails for "no placeholder in a split image" (F1).
- Focus (4) holds: 71 ran plus 24 not run equals the workflow's 95 run steps. Each of the three SDK steps logged a download, `sha256=d42680e9...` (the workflow's pin), the 25 installer tests and `SDK fresh installation: verified` (`receipts/docs-sdk-check.txt`).

[R738] PASS RTL - `git diff --stat a68536fa 7643aef6 -- hdl` (empty); gitlinks equal to `a68536fa`; `sw/litex/milan_soc.py:2614-2625`; `receipts/identity.txt` - No HDL or submodule difference from `dev-soft-core`, so its RTL verdicts stand. `stage_spi_phy` moves only `sink`, `source` and `cs`, and its submodule adds no CSR, which the `csr.csv` above confirms.

[R738] UNCLEAN Robustness - `ctrl_plat_image.py:101,126`; `ctrl_srp_image.py:55-63`; `receipts/mapflag-probe.txt`; `receipts/1x1-if2-summary.txt` - Open: F1, the silent default.
- A relative map gives the same loaded bytes as an absolute one. A missing map exits 2 with `REFUSED`, and a map at another clock exits 2.
- A two-interface boot on the one-interface map passes: ready at 91.835 ms, 18 of 18 writes.
- By reading `run()` and `main`, a guard failure in the export child becomes `REFUSED`, exit 2. The author's probe log shows the child's nonzero exit; I did not run that path end to end.

[R738] UNCLEAN Tests - `receipts/nomap-boot.log`; `receipts/mapped-boot-control.txt`; `receipts/portable-checks.txt`; `ctrl_service_budget/selftest.py` - Open: F3.
- The boot run can fail for the defect the ruling removes: dropping the map fails it with `NATIVE` and `BOOT` findings.
- The self-test receipt shows 6 of 6 native controls and 2 of 2 plants. I re-ran the native controls: 6 of 6.
- Also re-run at the head, all rc 0: target self-test `checks: 73   failures: 0`, `gen_flash_port.py --self-test` 33 checks, the budget self-test, `check_nvm_capture.py`.

[R738] UNCLEAN Docs - `receipts/figure-check.txt`; `nvm_split_target/README.md`; `ctrl_nvm/README.md`; `ARCHITECTURE_HW_SW_SPLIT.md`; `ctrl_split_boot/README.md`; `sw/firmware/ctrl/plat/README.md`; PR body - Open: F1, F2.
- `scripts/figure_check.py` compared 37 restated figures with the published receipts, with 0 mismatches. That covers the capture, phases, boots, controls and both boot tables, staged and none.
- The case table is restored. The stage cost of 541 and 532 cycles is arithmetic on the rows.
- No page still gives 84.393 or 184.658 as current, and `ctrl_configs.py`'s entry matches the code.

## Execution evidence

- Packet: all 336 `author-r6/` files at evidence commit `2540f263` match `published_sha256`, with none missing or unlisted. The commit carries no verified signature; the check is the manifest's hashes.
- Gate receipts: `gates-short` 0 of 97, `gates-long` 0 of 11, each at this head; all run `.rc` files are 0 except the kept `d5-plant-no-scratch-dir` attempt, which the author discloses. These are the author's, and I did not re-run them.
- My split boot at 1x1, from this clone: PASS, 84.372 ms, 4,218,617 CPU cycles, equal to the page (`receipts/1x1-if1-summary.txt`).
- Identity: `git diff --check a68536fa` rc 0, one merge base, live `dev-soft-core` still `a68536fa`, delta commits one line with no trailers (`receipts/identity.txt`).
- Restore: index tree equals `17caf313`, no status entries, gitlinks as required (`receipts/restore.txt`).
- My first `mapflag_probe.sh` compare piped `objcopy` to a stream and proved nothing. I replaced it with a file compare and re-ran it; only that result is kept.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | ruling 6677095110; `--cc` merge; `run.py`; `boot_soc.py`; `plat/README.md`; docs replay receipts | R738-4 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| RTL | CLEAN | empty `hdl` diff against `a68536fa`; gitlinks; `stage_spi_phy`; `csr.csv` rows | R738-4 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Robustness | UNCLEAN (F1) | map flag probes; no-map link; two-interface boot | R738-4 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Tests | UNCLEAN (F3) | no-map and mapped boots; self-tests; guard function probes | R738-4 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |
| Docs | UNCLEAN (F1, F2) | 37-figure check; five pages; PR body | R738-4 | `7643aef613c5b87a246544f57d23ad9f1bf8311e` |

## Real limits

- I ran the boot at 1x1 only, with one and two interfaces. 8x8 rests on the author's receipts, whose figures match the page.
- I did not re-run the 97 short or 11 long gates, S4 at either point, S2 at either point, or the split boot's plants.
- My probes used the same workstation RV32 SDK the author reports as not the pinned build (Buildroot 2026.05). The author's comparison of S3's and S4's images against the pinned SDK is receipt-only here, and the S2 images and firmware campaigns were compared by no one.
- The replay's empty `HOME` is inferred from the logged download. Its driver, `run_docs_yml.py`, is neither in the repository nor in the packet.
- A no-map image's hang is shown at 1x1. I did not trace which access stops it.
- This is simulation only. Physical calibration NOT RUN, and field skips are not hardware proof. No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Rule on the two open questions: moving the shared gate environment to the pinned SDK, and an owner for S2's 8x8 page.
- The current-dev merge candidate, its builder and native banks, and hosted and act acceptance. At my last look, `docs-gates-0` and `-2`, `bdd-conformance`, `docs-check-no-git` and `wire-accountability` were SUCCESS at this head, `docs-gates-1` and most shards were still running, and `Physical gPTP` was SKIPPED, which is not evidence.
- Carry RES1 to RES3 and the retained residue to the checklist.
- Any fix head needs this report's three findings re-reviewed, with coverage re-banked at that head.

R738-4 FINISHED
