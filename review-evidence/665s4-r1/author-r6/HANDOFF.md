# [A698g] #665 S4 round 6, resumed

STATUS: REVIEW READY. Every gate and run of the round 6 assignment is rc 0 at `7643aef613c5b87a246544f57d23ad9f1bf8311e`, on clean clones.

- Head: `7643aef613c5b87a246544f57d23ad9f1bf8311e`, local branch `s4-f1-target` in `$LANES/665-s4-f1-target`. PR #812 targets `dev-soft-core`. Nothing pushed; the live PR head is still `4d9b901c`.
- One commit added on `1de390e104`, no rebase, no force. **The head named in the resume is not the head of this result.** Why is in [the commit](#the-commit-this-session-added).
- Assignment: the [A10] ruling issuecomment-6677095110, and the manager's resume. Prior packet: `665s4-a698f`.
- `origin` is `https://github.com/kebag-logic/milan-fpga.git`. `dev-soft-core` is `a68536fa`, live and tracked, and the one merge base. `f4c9ad4f` is an ancestor. `git diff --check a68536fa` is clean. No file under `hdl/` differs from `a68536fa`, and no firmware C changed in round 6.
- TAKEN by [A698f] (issuecomment-6682509505) counts, as the resume says; not reposted.
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6689289532 (`REVIEW-READY-COMMENT.md`).

## Three things the manager should read first

1. **The head moved, by one documentation commit.** I reviewed `1de390e1` against the ruling before running gates. It had damaged a table no gate reads, so gates at that head would have passed with the damage in place. Every gate here is at the new head.
2. **The gate environment's SDK is not the pinned build** (below). Round 3's `env.sh` calls it pinned, and every round repeated that. It does not move a figure this PR states, by direct comparison, but the shared environment is the manager's question.
3. **S2's 8x8 grade moved** to 57 of 182, where its page says 66 and round 4 measured 62 (below). rc 0, no bound applies, and I left that shared page alone. It needs an owner.

## The commit this session added

`7643aef613` "Restore the saved-state case table and the split boot's PHY stage control rows, and list the flash map among its build steps (#665)". Documentation only: a docstring and two READMEs. Nothing that compiles or runs changes.

| Where | What, and why |
|---|---|
| `tb/verilator/nvm_split_target/README.md:101-104` | `1de390e1`'s restatement of the boot figures also replaced the `valid`, `absent`, `torn` and `version` rows of the **case table**: three measurement cells under a four-column header, and the statement of what each case must show gone. Restored byte for byte from `65bbbe21`; the case table now equals that commit's. The boots table keeps its figures. No gate reads table shape, which is why nothing caught it. |
| `tb/verilator/ctrl_split_boot/README.md:75-92` | `400c7ca7` deleted the `none` control rows and the stage-cost sentences, rather than restating them as the ruling's item 2 asks. Restored, re-measured at `1de390e1`: the same tree with `stage_spi_phy`'s one call removed (`receipts/runs/control-none.diff`). The stage now costs 541 CPU cycles at 1x1 and 532 at 8x8; the page had said 523. Each figure was checked against its log by script, and no UART figure moves by more than 0.001 ms. |
| `tb/verilator/ctrl_split_boot/run.py:6-14` | The docstring lists the build steps "in order" and round 6 added one before them; it now lists the flash map first. No behaviour. |

Checked in the same review and found sound: every other figure in `1de390e1` against `target-*/table.md` and `results.json`; `boot_soc.build` against the ruling; `ctrl_configs.py`'s entry; no stale old figure on any page.

## Round 6's earlier commits, for the record

From [A698f]'s handoff, re-read against the diff:

- `93c6e9a544`: `sw/firmware/ctrl/test/ctrl_plat_image.py:101,126` accepts and forwards `--flash-map`. `tb/verilator/ctrl_split_boot/run.py` builds the shape's map with `build.flash_map` and passes it to both links and exports. `boot_soc.py:61,96` places devices from the map and refuses a deviation. `ctrl_configs.py:171`, `ctrl_split_boot/README.md:30`, `sw/firmware/ctrl/plat/README.md:112` follow, and the "F1's flash port" item is closed.
- `400c7ca712`: `ImageMaps` in `run.py`, keeping `image()` inside the six-parameter limit (the Python idiom gate had refused seven); line wraps.
- `1de390e104`: figures in `nvm_split_target/README.md`, `sw/firmware/ctrl_nvm/README.md:352`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:225`.

Shared files touched in round 6: those paths, all named by the ruling or S3/S4 documentation. This session touched only `ctrl_split_boot/README.md` and `ctrl_split_boot/run.py` (S3's, both in the ruling's scope) and `nvm_split_target/README.md` (this lane's).

"No F1 placeholder in any split image" holds: both links the boot makes use the generated map. `ctrl_plat_image.py` keeps a no-map path for one caller, `ctrl_runs.py:85`, the boundary gate. That run is given absent runtime archives and stops at its link by design (`ctrl_runs.stopped_at_link`), so it makes no image.

## The docs.yml stop, resolved as authorised

`scripts/run_docs_yml.py` gives each job a fresh clone, an empty `HOME` and a new virtual environment. Installer and workflow are unchanged, and no receipt was written by hand.

All three SDK steps took the real path: `SDK download`, `SDK archive verified ... sha256=d42680e9...`, `SDK fresh installation: verified`, zero cache hits (`receipts/docs-final/docs-gates-{0,1,2}__ci_step_*.log`). The receipt lists 5,007 entries.

Differences from [A698f]'s replay, each toward the hosted run: the empty `HOME`; job and step `env:` applied; a failed step no longer ends a job; the cheap steps it skipped now run, so `not_run.json` holds only hosted-only and `apt`/`sudo` steps. `gate_42` stays in the `--network=none` container, because it executes the candidate's `act_ci.py`, which AGENTS.md section 5 confines to a disposable CI boundary. Lane 845's replay driver runs it on the host; I did not copy that part.

Result: `71 steps ran, 24 not run with a reason, 0 bad`, verifier rc 0 (`receipts/docs-final/docs-yml-table.md`).

The builder legs print `EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. Fifteen of the 16 are arms that need LiteX, absent as on a fresh runner, and the gate-environment `builder_require_rv32` has LiteX and covers them. Gate 11 (a vendor build tree) runs nowhere, as in every round. Leg 0's one is gate 1b's mutation arm, not run under the replay's make; it runs in the gate-environment builder gate.

## The SDK finding

`receipts/sdk-and-state/`. `$WORKSPACE_HOME/br-milan-rv32/host`, which the gates compile with, has no receipt and no `share/buildroot/sdk-location`. It reports Buildroot 2026.05; the pinned archive reports Buildroot 2021.11-18033-g83947c7bb6. Both are GCC 14.3.0 for `riscv32-buildroot-linux-gnu`. Of the receipt's 5,007 entries, 2,564 match, 1,680 differ and 763 are absent. The differing files include the compiler driver and assembler.

I did not change the gate environment. I tested whether it matters, on a separate clone, with a verified copy from the repository's own installer as the only RV32 toolchain reachable (`sdk-boot-compiler.txt` records the compiler actually used):

| Compared | Result |
|---|---|
| S3's image, 1x1 and 8x8 | every allocated section byte-identical; same ready time and cycles (`elf-compare.txt`) |
| S4's `fixture`, `capture-all`, `guard-probe` images, 1x1 and 8x8 | every allocated section byte-identical (`sdk-target-compare.txt`) |
| S4's `results.json`, `table.md`, both points | byte-identical |
| The files as a whole | same symbols in each, in a different order; the differing bytes lie inside `.symtab` |

**So no figure this PR states depends on the difference.** Not compared: the S2 harness's images, and the firmware campaigns. The claim stops there.

My first version of `elf_compare.py` printed `.symtab: same` for non-loaded sections from `objcopy -O binary`, which writes nothing for them: an empty-against-empty compare. Caught when the whole-file hashes still differed; it now reads symbols with `readelf`.

**Question for the manager:** should the shared gate environment move to the pinned SDK? Not this lane's to decide. `env.sh` here still says "pinned", copied unchanged from earlier rounds for comparability; read that word as wrong.

## S2's 8x8 grade

rc 0, `17 groups graded, 0 refusals, 57 T_svc misses (57 of 182 probe instances, 29 of 129 paths)`. This is the first complete 8x8 run at the merged base; [A698f]'s was cancelled.

- 1x1 is unmoved: 34 of 141, its table byte-identical to round 5's at `65bbbe21`, and equal to the page's row.
- At 8x8 the page's row is 66 of 182 (34 of 129) and round 4 measured 62 of 182 (30 of 129).
- Against round 4, path by path: 123 common paths, 5 verdicts flip, in both directions; mean change -0.114 ms, extremes -15.3 and +15.4 ms, about one loop pass. For example `acmp.disconnect_tx.if0` 16.452 to 1.151 ms, and `acmp.get_tx_state.if0` 1.157 to 16.547 ms.

That shape is what probes landing in a different pass after the image changed would give, not a slowdown. That is my reading of the spread; I did not prove the mechanism. The page labels its figures as measured on the stand-in addresses, so it is not false, but its "the address does not change an access's cost" invites the reading that its whole-run counts carry over, and at 8x8 they do not. The ruling assigns S4's and S3's figures, not S2's, and the file is shared, so I left it. It needs an owner (S2b, or a line in a later round).

Also for S2b's merge: the owner's round 18 ruling (issuecomment-6681686082) relaxes SRP/MRP's bound to T_svc = 20 ms, so the tree's "the 18 ms of SRP's" wording in `nvm_split_target/README.md` will go stale. It stays true at this base, where the grade is 10 ms, so I did not move the head for it.

## New checks: planted mutant and failing words

| Check | Planted defect | Failing words | Receipt |
|---|---|---|---|
| `boot_soc.build` placement guard | `spiflash_master_cs` expected four bytes off, in a scratch map | `the boot SoC does not place the flash port's devices as the split SoC does`; guard removed, the export succeeds and the probe reports the escape | `receipts/runs/map-probe.log` |

The guard's check is a probe, not a self-test in the tree. This session added no new check.

## Measurements

CPU 50 MHz, bus 100 MHz. All fresh at the head, and each equal to the figures the READMEs state.

| Point | S3 ready, cycles | Capture CPU | Capture elapsed | Longest step | Boots valid / absent / torn / version, CPU cycles |
|---|---|---|---:|---:|---|
| 1x1 | 84.372 ms, 4,218,617 | 1,367,366, 27.347 ms | 542.977 ms | 2.023 ms | 5,050,293 / 506,900 / 8,300,664 / 504,932 |
| 8x8 | 184.622 ms, 9,231,088 | 5,168,647, 103.373 ms | 1,641.818 ms | 2.641 ms | 24,519,265 / 1,747,362 / 37,436,744 / 1,745,393 |

`target-*` `results.json` and `table.md` are byte-identical to [A698f]'s at `93c6e9a5`.

## Gates

All at `7643aef613`, on clean clones, tree clean after each. Receipts in `receipts/`, indexed in `receipts/INDEX.md`.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| 97 short | 0 | `0 of 97 gates nonzero or left the tree dirty`; the same 97 names as round 4 | `gates-short/summary.md` |
| `bdd_conformance` (within the 97) | 0 | 14 features, 508 scenarios, 2,330 steps passed; CPython 3.12.3 and the CI constraints | `gates-short/` |
| `nvm_target_selftest` (within the 97) | 0 | `checks: 73   failures: 0` | `gates-short/` |
| 11 long, together | 0 | `0 of 11 gates nonzero or left the tree dirty` | `gates-long/runner.log` |
| `ctrl_memory` | 0 | `test_ctrl_memory: 0 failure(s)` | `gates-long/` |
| `builder_require_rv32` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN`, gate 11 | `gates-long/` |
| `ctrl_nvm` | 0 | `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` | `gates-long/` |
| `ctrl_firmware` | 0 | `test_ctrl_firmware: PASS`; 1,053 plants caught, none escaped | `gates-long/ctrl_firmware-tally.txt` |
| `fw_coverage_selftest` | 0 | `29 of 29 planted cases read as planted` | `gates-long/` |
| `fw_coverage` | 0 | `firmware coverage: PASS (35 files)`: 100 % lines and branches after the gate's exclusions (raw `nvm_flash_litespi.c` 63/64 branches) | `gates-long/` |
| `firmware_boundary_verilator` | 0 | `ctrl_boundary: PASS` | `gates-long/` |
| `nvm_cosim`, `nvm_cosim_lint` | 0 | `465 checks: 465 PASS, 0 FAIL`; `39 of 39 mutant(s) killed by their named check` | `gates-long/` |
| `firmware_boundary` | 0 | `ctrl_boundary: PASS` | `gates-long/` |
| `publication_census` | 0 | `checks: 246   failures: 0`; `selftest: 0 of 139 arm(s) failed` | `gates-long/` |
| S3 split boot, 1x1 and 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))` at each; 18 of 18 writes | `runs/splitboot-*.log` |
| S3 self-test | 0 | `6 of 6 native controls as required; 2 of 2 plants caught` | `runs/splitboot-selftest.log` |
| S4 target, 1x1 and 8x8 | 0 | every case passes, every control caught | `runs/target-*` |
| S2 harness, 1x1 | 0 | `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)` | `runs/budget-1x1*` |
| S2 harness, 8x8 | 0 | `17 groups graded, 0 refusals, 57 T_svc misses (57 of 182 probe instances, 29 of 129 paths)` | `runs/budget-8x8*` |
| D5 plant | 0 | `PLANT CAUGHT`: planted `FAIL: OFF timing limit was ignored`; unplanted `PASS` | `runs/d5-plant.log` |
| Reuse probe | 0 | `PROBE PASS` | `runs/reuse-probe.log` |
| Real refusal, 1x1 and 8x8 | 0 | `PROBE PASS` at each | `runs/real-refusal-*.log` |
| Map probe | 0 | `map probe: PASS` | `runs/map-probe.log` |
| docs.yml, every job | 0 | 71 ran, 24 not run with a reason, 0 bad | `docs-final/docs-yml-table.md` |
| `git diff --check a68536fa`, one merge base, clean tree | 0 | as listed | `final-identity.txt` |

**One first attempt failed, and is kept.** The D5 plant's first run exited 1 with `FileNotFoundError` on its scratch directory: my run script had not created it, and nothing was planted. With the directory created, it passed. `runs/d5-plant-no-scratch-dir.{log,rc}` keep the failed attempt.

**Reused receipts: none.** The resume allowed reusing valid receipts at this head, but the head moved, so everything ran fresh here. The one exception is `control-none-*`, measured at `1de390e1` because the commit needed their figures; that tree differs from the head only in documentation, and the page says which commit measured them.

## Resources

All work ran on the booked CPUs 56-63, at nice 10, in units capped at MemoryMax 10G and MemoryHigh 8G. No range was taken from another lane; `cpu_ranges.py pick` found none free. `receipts/sdk-and-state/unit-peaks.txt` has each unit's memory peak: the highest was 8,595,374,080 bytes (8.0 GiB) against the 10 GiB cap. The main unit peaked at 1,858,715,648 bytes, against the last session's recorded 15.6 GB. No Vivado, sweep, hardware, flashing or sub-agents.

## Not done

- No full sweep: RTL is unchanged. No Vivado route.
- `nvm_capture_cpu`'s capture runs: as in round 4, that writer and its harness are unchanged, and `check_nvm_capture.py` regrades the receipt.
- Hosted CI has not run on this head, because nothing is pushed. All of this is local evidence.
- A review: this head has had none. Round 4's POSITIVE was at `4d9b901c`.

`PR-BODY.md` is round 4's live body with its stale lines updated (the checkout, the `slow-step` figures, the elapsed time, the T_svc note, the merge limitation), plus round 5 and round 6 sections. It is not published.
