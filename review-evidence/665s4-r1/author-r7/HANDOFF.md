# [A698h] #665 S4 round 7

STATUS: REVIEW READY. Every gate of the round 7 assignment is rc 0 at `37e0393094e62d395edc2798a6a6da2f34badbec`, on clean clones. One earlier attempt at an ancestor failed and is kept; its cause was not found.

- Head: `37e0393094e62d395edc2798a6a6da2f34badbec`, local branch `s4-f1-target` in `$LANES/665-s4-f1-target`. PR #812 targets `dev-soft-core`. Nothing pushed; the live PR head is still `7643aef6`.
- Four commits on `7643aef613`, no rebase, no force. Commit subjects are one line, with no body and no trailers.
- `origin` is `https://github.com/kebag-logic/milan-fpga.git`. `dev-soft-core` is `a68536fa`, live and the one merge base. No file under `hdl/` differs from it, and no firmware C changed.
- Assignment: [A10] issuecomment-6689759393. Reviews: R737-3 (issuecomment-6689752907), R738-4 (issuecomment-6689696235).
- TAKEN: issuecomment-6689876018. REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6691584700 (`REVIEW-READY-COMMENT.md`).

## Read these first

1. **A second no-map link existed that neither review listed.** `docs/design/SPLIT_CONTROL_MEMORY.md:319` is a documented `ctrl_plat_image.py` link with no map. It would have been refused as written after item 1, so it now carries the map. I ran it unedited: 59.0 tiles, ledgered, no stand-ins.
2. **Question for the manager: does the ruling's "any split image" reach the size fixture?** `ctrl_srp_image.py --layout split --with-aecp` still links on the stand-ins with no map, and the design page documents that command. I left it: it is a separate builder, not a booted image (`sw/firmware/ctrl/README.md:654`), `build.flash_map` needs it to make the first export the map is read from, and the assignment names the platform image. The reviews did not file it.
3. **One gate attempt failed and I could not find why.** `firmware_boundary`'s first attempt at `c2befb12` was refused because `test_ctrl_firmware.py` exited -15, a SIGTERM, 212 s in. See [the kept failure](#the-kept-failure).
4. **The head moved once mid-round.** At `c2befb12` a grep found `sw/firmware/ctrl/README.md:711` still saying 33 checks. Those gates were stopped, the fix went in as `37e03930`, and every gate below ran fresh at that head.

## Changes

| Where (at the head) | What | Why |
|---|---|---|
| `sw/firmware/ctrl/test/ctrl_plat_image.py:51,55-59,163` | `NO_FLASH_MAP`, `refuse_placeholder`, called first in `main` | Item 1. Refuses when `--flash-map` is absent and any runtime archive exists, before the compiler is even looked up. |
| `sw/firmware/ctrl/test/ctrl_plat_image.py:13-17,113-114` | Docstring and `--flash-map` help | Say what is now true. These lines had to change, so R737-3-R1, R737-3-R2 and R738-4-RES2 are applied in them. |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:30-35,65-67,417-445,465` | `plat_link`, `plat_cases`, four new checks | Item 1's lasting test. It runs in the boundary gate, so the hosted firmware boundary job runs it. |
| `sw/firmware/ctrl/plat/README.md:16,88-102,124` | The generator line and the map in the command; where the map comes from; what omitting it does | Item 1 as ruled. It also restores the warning the round 6 delta removed. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:316-321` | The map in the second documented link | Would be refused as written otherwise. |
| `tb/verilator/ctrl_split_boot/boot_soc.py:61-66,104` | `refuse_deviation`, extracted, same behaviour and words | Item 3: gives the planted defect one name to replace. |
| `tb/verilator/ctrl_split_boot/run.py:104-120,203-217,453-504,520,535,546` | `DEVIATES`, `MOVED`, `PLACEMENTS`, `GUARD_PLANTS`, `exported`, `edited_map`, `export_verdict`, `placement_controls`, `--placement-controls` | Item 3. `export()` keeps its signature and only delegates, so the reviewers' scripts still run. |
| `tb/verilator/ctrl_split_boot/README.md:25,38-39,73` | The command, and the control | Documents item 3, including that no hosted job runs it. |
| `tb/verilator/nvm_split_target/README.md:158`, `sw/firmware/ctrl_nvm/README.md:338` | 13.861 ms | Item 2. |
| `sw/firmware/ctrl/README.md:711,719-721` | 37 checks, and what the last four are | My change made the page's 33 stale. |

Shared files touched: `ctrl_image_selftest.py` and `sw/firmware/ctrl/README.md` (the control firmware's), `SPLIT_CONTROL_MEMORY.md` (the split's design page), and S3's `plat/README.md`, `run.py`, `boot_soc.py`. Not touched: `split_soc.py`, `ctrl_runs.py`, `ctrl_configs.py`. Nothing else imports `run.py` or `boot_soc.py`, and no firmware source changed.

PR body: the live body with `[A698h]`, the status, lines 53, 98, 99 and 213 corrected, the guard's row under line 233 saying what is now in the tree, `How to validate` and `Known limitations` extended, and a round 7 section. Its line 180 tick is now true.

## New checks: planted mutant and failing words

Each planted literally in a scratch clone of the head, one at a time, by `scripts/mutants.py`. All three checks are green with no mutant first. Result: `mutants: 9 planted, 0 escaped; clone clean after: True` (`receipts/mutants.md`, `receipts/mutants/`).

| Check | Planted defect | Failing words |
|---|---|---|
| `ctrl_image_selftest.py` plat | the refusal's call removed | `AssertionError: ('both archives', 'collect2: error: ld returned 1 exit status')` |
| same | `any` changed to `all` | `AssertionError: ('the C library alone', 'collect2: error: ld returned 1 exit status')` |
| same | refused even with a map | `AssertionError: REFUSED: no --flash-map: ...` |
| `ctrl_runs.stopped_at_link`, the boundary gate's own argv and verdict (`scripts/stopped_probe.py`) | refused with no archives too | `exit 2; ELF present False; stopped_at_link False` |
| `run.py --placement-controls` | `refuse_deviation`'s call removed (R738-4's `boot_soc.py:96-98`) | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| same | the `raise` removed | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| same | `map_deviations` returns `[]` | `PLACEMENT register-moved: WRONG (deviations [])` |
| same | the window comparison removed | `PLACEMENT window-moved: WRONG (deviations [])` |
| the boot itself | the guard refuses a true map | `RuntimeError: the boot SoC does not place the flash port's devices as the split SoC does: []`, exit 2 |

In the tree as well: `GUARD_PLANTS` runs two of these on every `--self-test`, printing `PLANT guard-removed: caught` and `PLANT deviations-empty: caught`.

The driver's first full run, at `c2befb12`, exited 1 with two bugs of mine and no escaped mutant: wrong expected words for `refused-with-a-map` (the check had gone red, rc 1), and an anchor that matched twice. Kept as `receipts/kept/mutants-attempt1-driver-bugs.log`.

## Verification the assignment names

- `receipts/runs/nomap-probe.log`: the reviewer's script, unedited: `no-map link rc=2`, the refusal, and no ELF (`objdump` reports the file missing).
- `receipts/runs/page-plat.log`: the plat page's `sh` fence, extracted by `scripts/page_probe.py` and run unedited with `SOC=<build>/split-soc/mapped/soc` and `RUNTIME=<build>/runtime`: exit 0, `lui 0xf0004` 0 and `lui 0x20000` 0 across the 12 `ls_*` and `nvm_flash_litespi*` functions, 39.0 tiles, and the generated map equals the run's `split-soc/flash-map`.
- `receipts/runs/page-design.log`: the design page's fence at 8x8 with two interfaces: exit 0, both 0, 59.0 tiles ledgered.
- `receipts/runs/nomap-base-disasm.txt`: the same scan on a no-map image linked before the refusal: `lui 0xf0004` 4 times, `lui 0x20000` once, in `ls_call_begin`, `ls_late`, `ls_now_us`, `nvm_flash_litespi_power_on` and `ls_read`. So the scan can fail.

`gen_flash_port.py` refuses the boot SoC's export (`REFUSED flash window`, `REFUSED journal`), which is why the page's `$SOC` is the product split export.

## Gates

All at `37e0393094e62d395edc2798a6a6da2f34badbec`, each on a clean clone, tree clean after. Receipts in `receipts/`, indexed in `receipts/INDEX.md`.

| Gate | rc | Result |
|---|---:|---|
| The reviewer's `nomap_probe.sh`, unedited | 2 at its link, as required | `no-map link rc=2`, the named refusal, no ELF |
| The plat page's command, as written | 0 | no stand-in load in `ls_*`; 39.0 tiles; its map equals the run's |
| The design page's command, as written | 0 | no stand-in load in `ls_*`; 59.0 tiles, ledgered |
| `firmware_boundary --without verilator` | 0 | `ctrl_boundary: PASS`; its `ctrl_plat_image.py` runs stopped at their link |
| `firmware_boundary --only verilator` | 0 | `ctrl_boundary: PASS` |
| S3's split boot, 1x1 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 84.372 ms, 18 of 18 writes |
| S3's split boot, 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 184.622 ms, 18 of 18 writes |
| S3's self-test | 0 | `6 of 6 native controls as required; 2 of 2 plants caught; 0 placement controls wrong` |
| `--placement-controls`, 1x1 and 8x8 | 0 | `ctrl_split_boot placement controls: 8 of 8 as required` at each |
| `ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 37 checks PASS` |
| The nine literal mutants | 0 | `mutants: 9 planted, 0 escaped; clone clean after: True` |
| The reviewers' `refusal_probe.py`, `portable_checks.sh` | 0 | `misses: 0`; each of its checks rc 0, `guard on the real map: []` |
| `check_nvm_capture.py` | 0 | `PASS: capture census, clocks, both timing arms and receipt agree` |
| `check_py_idiom.py` | 0 | no new finding |
| `docs.yml`, every job, each on a fresh clone with an empty `HOME` and a new virtual environment | 0 | 71 steps ran, each rc 0; 24 not run, each with its reason; all three SDK steps downloaded the archive, verified `d42680e9...` and printed `SDK fresh installation: verified` |
| `git diff --check a68536fa`, merge bases | 0 | rc 0; one merge base, `a68536fa`, still `dev-soft-core`'s tip |
| The privacy check | 0 | `0 private line(s) in a68536fa..HEAD` |
| `rg '13\.863'` | | only `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, where it records history |

## The kept failure

`receipts/kept/firmware_boundary-attempt1-sigterm.log`, rc 2, at `c2befb12`: `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32: exit -15 (212 s)`.

What I checked, and what it rules out:
- Memory: the gate's peak was 1.4 GB in a 10 GB cap, and a cgroup kill is SIGKILL.
- The user journal shows nothing at that second.
- `sw/builder/test_firmware_compiler.py`, the docs step running then, has no kill or signal call.
- The manager's session shows no `pkill` that day.
- The overlap: the passing run's `test_ctrl_firmware.py` (17:00 to 17:08 UTC) overlapped that same docs step (17:03 to 17:12 UTC) and was not killed.

**The cause is not found.** I cannot tie it to this delta or clear it of one by a mechanism. What I can state is that the same gate passed at the final head, on a fresh clone, in both modes.

## Measurements

CPU 50 MHz, bus 100 MHz, the same as round 6's; this round does not move them.

| Shape | Boot to ready | CPU cycles | Trace | `milan_status` span / first byte / longest gap |
|---|---:|---:|---|---|
| 1x1 | 84.372 ms | 4,218,617 | 18 of 18 | 21.546 / 1.963 / 1.266 ms |
| 8x8 | 184.622 ms | 9,231,088 | 18 of 18 | 40.224 / 2.856 / 2.207 ms |

## Not done

- The 97 short gates, the rest of the 11 long, S2 and S4 at either point, the D5 plant: not re-run. The assignment's gates are those the delta touches, and `split_soc.py`, the firmware C and the RTL did not change. Coverage for those rests on `7643aef6`'s receipts and the reviewers' judgement.
- A review of this head. Hosted CI: nothing pushed, so all of this is local evidence.
- R738-4-RES1 (`ctrl_split_boot/README.md`, now line 79) and R738-4-RES3 (`run.py:6`): not in the assignment, left for the residue checklist, along with the retained items.
- `SPLIT_CONTROL_MEMORY.md` section 5's size rows (R737-3-S3): still the no-map figures, labelled as measured at `b8628704`. `rom` is 8 B lower with the map (109,552 and 125,040 B measured here); tiles do not change at the two points measured.
- R737-3-S4: `ctrl_plat_image.py` still does not resolve a relative `--flash-map`. Harmless, as both reviews found.
- The two open questions stand: the gate environment's SDK is not the pinned build (`env.sh` here says so), and S2's 8x8 page needs an owner.

## Resources

CPUs 120-127, this lane's own, at nice 10, in units capped at MemoryMax 10G and MemoryHigh 8G. The highest recorded gate peak was 4,407,095,296 bytes (4.1 GiB), `firmware_boundary_verilator`, against the 10 GiB cap, and the session's own unit peaked at about 0.9 GiB. The docs replay unit ran under the same cap and its peak was not recorded. No Vivado, sweep, hardware, flashing or sub-agents.
