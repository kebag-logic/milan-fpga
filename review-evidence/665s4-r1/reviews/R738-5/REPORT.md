[R738] POSITIVE - exact head 37e0393094e62d395edc2798a6a6da2f34badbec

External cleared-context review R738-5 of issue #665 / PR #812, S4 round 7. Tree `671949bf0b327496993ce1462ae2f61d4125525f`. Delta `7643aef6..37e03930`: four commits, ten files, Python and Markdown only. Judged against the round 7 assignment (issuecomment-6689759393) and the manager's note on the size fixture (issuecomment-6691621669).

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open. All five lenses are clean at this head. Two SUGGESTIONs and two RESIDUE items are new.

All three named checks hold:

- **The refusal.** `ctrl_plat_image.py` refuses a link with no `--flash-map` by name, and its test runs in the boundary gate.
- **The placement controls.** They fail for their planted deviations, and for two literal edits of mine. A narrower mutant survives them (S1), though the code at this head handles that case.
- **The 13.861 ms figures.** They match the gated receipt.

The kept SIGTERM supports "external to this change and to the gate's own process tree". It does not identify a sender, so it should stay recorded as unexplained. See [The kept SIGTERM](#the-kept-sigterm).

My own 1x1 and 8x8 boots reproduced the published figures to the cycle.

## Focus results

**1. The refusal, and its lasting test. Holds.**

- `sw/firmware/ctrl/test/ctrl_plat_image.py:55-59,163`: the refusal is the first step in `main`, before the compiler lookup.
- Edge probes (`receipts/raw/refusal-edges.log`), all with real archives unless stated:

| Case | Result |
|---|---|
| No map, both archives | rc 2, named refusal, no ELF |
| No map, C library alone | rc 2, named refusal, no ELF |
| No map, compiler runtime alone | rc 2, named refusal, no ELF |
| No map, a directory as an archive | rc 2, named refusal, no ELF |
| No map, both absent | rc 2 at the link, no ELF |
| No map, dangling symlinks | rc 2 at the link, no ELF |
| Map path absent, or empty directory | rc 2, `REFUSED`, no ELF |
| True map | rc 0, ELF |

- The refused run's output directory is empty, so nothing compiled.
- The gate's own four no-map runs, from `ctrl_runs.image_runs` and judged by its `stopped_at_link`: rc 2, `stopped_at_link True`, no ELF (`receipts/raw/stopped-probe.log`).
- `ctrl_image_selftest.py --require-rv32` at this head: `37 checks PASS`, including the four `plat:` lines (`receipts/raw/image-selftest.log`).
- `ctrl_runs.py:69` runs that self-test in `owned()`, and any nonzero exit refuses the gate. The author's receipts show it `exit 0` in both modes, with four `stopped at its link` lines for `ctrl_plat_image.py` in each.
- Hosted `firmware-boundary` and `firmware-verilator` report success at this exact head (`receipts/raw/hosted-boundary.txt`).
- Both documented fences, extracted from their pages and run unedited:
  - plat page: rc 0;
  - design page, 8x8 with two interfaces: rc 0, 59.0 tiles, ledgered;
  - each: 12 flash port functions, with no `lui 0xf0004` and no `lui 0x20000` (`receipts/raw/page-plat-scan.txt`, `page-design-scan.txt`).
- The aligned-word scan of the plat image finds each stand-in value once, and neither is the flash port's (`receipts/raw/data-word-trace.txt`):
  - `0xf0003800` is `env+0x8`, `CTRL_PLAT_UART_RXTX`: the split SoC's real UART, per its `csr.csv`.
  - `0x20000000` is `aecp_entity_image+0xc`, descriptor data.
- No other documented or scripted no-map link exists: `ctrl_plat_image.py` appears as a command only in those two fences, `run.py` and `ctrl_runs.py`.
- The size fixture is ruled out of the refusal, so I do not report it.

**2. The placement controls. Hold for the planted deviations.**

- My runs give `8 of 8 as required` at 1x1 and 8x8, and inside `--self-test`: `6 of 6 native controls as required; 2 of 2 plants caught; 0 placement controls wrong`.
- Literal edits of mine (`receipts/raw/literal-guard-mutants.log`, `own-mutants.log`):

| Edit | Result |
|---|---|
| `boot_soc.py:104` call removed | `export-refuses: WRONG (export TAKEN)`, rc 1 |
| `map_deviations` returns `[]` | five controls WRONG, rc 1 |
| Window compared by base only | `7 of 8`, rc 1 |
| Refusal reads the C library only | self-test assertion, rc 1 |

- The export control is not vacuous: the two in-tree plants turn the same map from REFUSED to TAKEN, so the refusal is what stops that export.
- My own real deviation: the boot SoC's `timer0` placed 0x800 higher on the true map, with no map edit. The export is refused and names the `timer0_*` registers.
- Moving the `spiflash` bank or the window that way stops earlier, in LiteX or the SoC's own check. That fits `run.py:108`: "only a register can deviate in a real export".
- An empty build directory gives rc 2 (`REFUSED`), and `--regrade` still passes after the controls have run (`receipts/raw/placement-edges.log`).

**3. The 13.861 ms figures. Hold.**

- `tb/verilator/nvm_capture_cpu/measurements.json:488,1350` reads 13.86052. `tb/verilator/nvm_split_target/README.md:158` and `sw/firmware/ctrl_nvm/README.md:338` give 13.861.
- `scripts/check_nvm_capture.py` passes at this head.
- `13.863` as a figure survives only in `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1681,1683,1710,1863-1864`, labelled as earlier receipts.
- PR body lines 53, 98 and 99 now give 13.861, 101.0 / 166.0 / 490.4 / 748.7 ms, and 11,066 + 265.8 and 16,533 + 205.6, the head's values as R738-4 listed them.

## The kept SIGTERM

**Does the kept evidence support treating it as external? Yes, for "external to this change and to the gate's own process tree". No, if "external" means the cause is known.** The sender is not identified, and nothing kept can identify it.

What supports it:

- **Only the driver took the signal.**
  - The kept log shows `test_ctrl_firmware.py ... exit -15 (212 s)`, an empty tail, `REFUSED`, gate rc 2, and an `# end` line.
  - I sent SIGTERM to that one PID in a live gate and reproduced those lines (`receipts/raw/sigterm-pid.log`).
  - SIGTERM to the gate's process group gives a different result: the gate itself dies at -15 with no `REFUSED` (`sigterm-group.log`). The gate and the driver share that group (same receipt).
  - So a group-wide kill did not happen. By inference, neither did a unit stop, which signals every process in the unit.
- **No changed code was running.**
  - The failing step is in `captures()`, `ctrl_boundary.py:494`, which finishes before `owned()` at `:495`, the only place the gate reaches the delta's Python.
  - The driver's import closure of 26 modules holds none of the delta's Python modules (`receipts/raw/driver-closure.txt`).
  - No Python file differs between `c2befb12` and this head. Only two Markdown pages do.
- **No in-tree sender on that path.**
  - None of those 26 modules has a signal-sending call (`receipts/raw/driver-signal-grep.txt`).
  - The compile recorder in `ctrl_shim.py` only forwards a signal down to its compile.
  - A subprocess timeout would kill a child with SIGKILL, not SIGTERM its parent.
  - An out-of-memory kill would be SIGKILL too, so -9, not -15.
- **The same code passes.** The author's receipts show both modes passing at this head on fresh clones, and the two hosted jobs succeeded at this head.

What limits it:

- The kept log is 610 bytes and says nothing about the sender.
- The peak memory, the journal check and "no `pkill`" are statements in the hand-off, with no receipt in the packet. The hand-off says the user journal only.
- The hand-off says the author stopped gates at that ancestor, but not how or when. A targeted kill from the lane's own session would match this log.
- The receipts argue against that being the sender, without excluding it: a new `c2befb12` mutant run started at 16:48:58Z, nearly four minutes after the 16:45:04Z end. The fix commit came at 16:59:59Z.
- I did not read host logs, which were outside this review's probe scope.

So it is not a finding and does not touch any lens. The right record is "sender unidentified, not this change", which is what the PR body says apart from RES2.

## Findings

**R738-5-S1 | SUGGESTION | Tests | `tb/verilator/ctrl_split_boot/run.py:105,109-114` | The controls move one register, so a narrowed `map_deviations` survives.**
- Evidence: two mutants of `split_soc.py`'s comparison, one limited to `spiflash*` registers and one to `spiflash_master_cs` plus the invented name, each keep `8 of 8 as required`, rc 0. Under each, a real `timer0` shift of 0x800 is TAKEN (`receipts/raw/own-mutants.log`).
- Why a SUGGESTION: the code at this head is right, since the same real shift is refused unedited. The ruling's item, a committed negative test with a mutant caught by name, is met. The boot itself fails on a misplaced image, as R737-3's M1 showed, so a second check stands behind this guard. It matters a little more than one register suggests, because the stand-in the ruling is about is a timer address.
- Optional outcome: run `register-moved` once for each name in `port['registers']`. It is pure Python and needs no export.
- Verification: both mutants go red.

**R738-5-S2 | SUGGESTION | Tests | `sw/firmware/ctrl/test/ctrl_image_selftest.py:30-35,417-429` | "Before anything compiles" is stated and not checked.**
- Evidence: moving the refusal to just before the link leaves `37 checks PASS`, rc 0 (`receipts/raw/own-mutants.log`). The behaviour at this head is as stated: the refused run's output directory is empty.
- Why a SUGGESTION: the ruling asks for a named refusal or no ELF, not for its timing, and the statement is true.
- Optional outcome: `plat_link` also asserts that the output directory holds no object.
- Verification: that mutant goes red.

**R738-5-RES1 | RESIDUE | Docs | PR body lines 335, 368 | "Equals" holds for the addresses, not the file.**
The map the plat page's generator writes differs from `split-soc/flash-map` only in the two `source` digests, because the run's map was read from the stand-in export. It is byte-identical to `split-soc/flash-map-again`. The author's comparison strips `source`. Exact fix, line 335: "equals the run's `split-soc/flash-map` apart from its `source` digests, and `split-soc/flash-map-again` byte for byte". Line 368: "its map's addresses equal the run's".

**R738-5-RES2 | RESIDUE | Docs | PR body line 386 | "The journal" is the user journal.**
The hand-off says the user journal. Exact fix: "the user journal shows no kill".

## Prior findings at this head

| Finding | State at `37e03930` |
|---|---|
| R738-4-F1 (MAJOR), R737-3-F1 (MINOR) | **Resolved at the cause.** Named refusal, both fences carry the map, the plat page says where the map comes from and what omitting it does (`plat/README.md:88-102`). PR line 217 states what is now true. |
| R738-4-F2 (MINOR) | **Resolved.** See focus 3. |
| R738-4-F3 (MINOR) | **Resolved.** Committed negative test, true map accepted, both literal edits caught by name. It runs in lane gates only, as the PR says; that is R738-4-S2 below. |
| R737-3-R1, R737-3-R2, R738-4-RES2 (RESIDUE) | **Resolved** at `ctrl_plat_image.py:13` and the `--flash-map` help. |
| R737-3-S1 (SUGGESTION) | **Resolved in part.** The guard now has a lasting check. Still no hosted job compiles `ctrl_plat_image.py` to a link with a map. |
| R737-3-S5 (SUGGESTION) | **Resolved.** `run_docs_yml.py` is in the packet; `map_probe.py` is superseded by the committed control. |
| R737-1-S2 (SUGGESTION) | **Resolved in part.** The shared `map_deviations` and the map-clock refusal now have committed checks. `split_soc.build`'s own raise does not. |
| R738-4-RES1 (RESIDUE) | Retained, now `ctrl_split_boot/README.md:79`. |
| R738-4-RES3 (RESIDUE) | Retained at `run.py:6`. |
| R738-4-S1, R737-3-S2 (SUGGESTION) | Retained. S2's 8x8 page still needs an owner. |
| R738-4-S2 (SUGGESTION) | Retained; the PR says so. |
| R737-3-S3 (SUGGESTION) | Retained; rows labelled, 8 bytes off, tiles equal. |
| R737-3-S4 (SUGGESTION) | Retained; harmless. |
| R737-1-S3, R737-1-S4, R737-2-S1, R737-2-S2, R737-2-S3, R738-3-S1 (SUGGESTION) | Retained; the delta does not touch their files. |
| R737-2-R1, R738-3-RES1 (RESIDUE) | Retained; the delta does not touch their source files. |
| R738-F1, R738-F2 (MINOR), R737-1-R1 (RESIDUE), R737-1-S1 (SUGGESTION) | Stay resolved; nothing they depend on changed. |

## Per-lens results

[R738] PASS Conformance - issuecomment-6689759393 items 1 to 4 against `ctrl_plat_image.py:51-59,163`, `plat/README.md:88-102`, `ctrl_runs.py:93-98`, `run.py:453-504`, PR body lines 53, 98, 99, 217 - Each item is met and the ruling's verification reproduced: `receipts/raw/refusal-edges.log`, `stopped-probe.log`, `page-plat-scan.txt`, `page-design-scan.txt`. The delta changes no protocol behaviour.

[R738] PASS RTL - `receipts/raw/identity.txt`; `boot_soc.py:61-66,104`; `receipts/raw/boot-1x1.log`, `boot-8x8.log` - No `hdl/`, `.sv`, `.v`, `.c` or `.h` file and no gitlink is in the delta. `refuse_deviation` keeps its words and its place after the export. The boots land on the same cycles as round 6, 4,218,617 and 9,231,088, so round 6's RTL verdict stands at this head.

[R738] PASS Robustness - `ctrl_plat_image.py:55-59`; `run.py:464-472`; `receipts/raw/refusal-edges.log`, `placement-edges.log`, `sigterm-pid.log` - Every edge above ends at rc 2 with no ELF, or at the true map. A missing finished run is refused, not traced back. The gate refuses a killed builder instead of passing on less. S1 and S2 do not touch runtime behaviour.

[R738] PASS Tests - `ctrl_image_selftest.py:417-445`; `run.py:109-120,453-504`; `receipts/raw/image-selftest.log`, `literal-guard-mutants.log`, `own-mutants.log`, `boot-selftest.log` - Each new control went red under a literal edit, and the plants are not vacuous. Three of my narrower mutants survive, recorded as S1 and S2 with reasons. None is a defect in what the controls claim to catch.

[R738] PASS Docs - `sw/firmware/ctrl/README.md:711-721`; `plat/README.md:16,88-102,124`; `docs/design/SPLIT_CONTROL_MEMORY.md:316-321`; `ctrl_split_boot/README.md:25,38-39,73`; `nvm_split_target/README.md:158`; `ctrl_nvm/README.md:338`; PR body - The 37 is 33 plus `plat_cases`' four. Both fences run as written. No added source line carries a lane label, reviewer ID or comment ID. `git diff --check` rc 0, commits one line, no private path in the delta. RES1 and RES2 are wording only.

## Execution evidence

- **Packet:** all 259 `author-r7/` files match `published_sha256` in the manifest, none missing, none unlisted, and each matches its tree blob (`receipts/raw/packet-check.txt`). The evidence commit `60974211` has no verified signature, so this check rests on the manifest's hashes.
- **Receipt heads:** 16 run logs carry this head, 2 carry `c2befb12` (the two disclosed kept attempts) and 2 carry `7643aef6`. The one nonzero `.rc` is the kept SIGTERM attempt.
- **My boots, from a disposable clone:**
  - 1x1: PASS, 84.372 ms, 4,218,617 CPU cycles, the first 18 window writes equal.
  - 8x8: PASS, 184.622 ms, 9,231,088 CPU cycles, the first 18 window writes equal.
- **Identity:** one merge base `a68536fa`, live `dev-soft-core` still `a68536fa`, live PR branch at this head (`receipts/raw/identity.txt`).
- **Hosted, at my last look (`receipts/raw/hosted-checks.txt`):** 25 SUCCESS, 19 in progress, 9 queued, 1 SKIPPED. Among the successes are `firmware-boundary`, `firmware-verilator`, `docs-check`, `docs-gates-0` to `-2` and `bdd-conformance`. `Physical gPTP` is SKIPPED, which is not evidence. Job logs were not yet readable, because the run is still going, so the hosted `ctrl_image_selftest.py: exit 0` line is inferred from the gate's success.
- **Restore:** the review clone is unchanged: tree `671949bf`, index tree equal, no status entries, gitlinks as required. Every mutant ran in a disposable clone, and those clones ended clean.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment items 1 to 4; `ctrl_plat_image.py`; `plat/README.md`; `ctrl_runs.py`; PR body; refusal and page probes | R738-5 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| RTL | CLEAN | Empty `hdl`, C and gitlink delta; `boot_soc.py`; both boots' cycles | R738-5 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Robustness | CLEAN | Refusal edges; placement edges; gate behaviour under SIGTERM | R738-5 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Tests | CLEAN | `plat_cases`; placement controls; plants; own mutants; self-test at head | R738-5 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Docs | CLEAN | Six changed pages; both fences; `measurements.json`; PR body; comment rule on added lines | R738-5 | `37e0393094e62d395edc2798a6a6da2f34badbec` |

## Real limits

- I did not run `firmware_boundary` to completion in either mode. That rests on the author's receipts and the hosted job results. My two gate runs were deliberately killed.
- I did not re-run the docs gates, the 97 short gates, the other long gates, S2, S4 or the D5 plant. The delta does not touch what those depend on, and they keep their prior verdicts.
- My probes used the same workstation RV32 SDK the author reports as not the pinned build (Buildroot 2026.05).
- Real-deviation exports ran at 1x1 only.
- Simulation only. Physical calibration NOT RUN, and field skips are not hardware proof. No manager source bank ran at this exact head, and none is claimed.

## Pending manager duties

- The current-dev merge candidate (source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`), its builder and native banks, and hosted and act acceptance, including the jobs still running above.
- Rule on the two open questions: the gate environment's SDK, and an owner for S2's 8x8 page.
- Carry RES1, RES2 and the retained residue to the checklist.
- A later commit touching a lens's scope un-covers that lens.

R738-5 FINISHED
