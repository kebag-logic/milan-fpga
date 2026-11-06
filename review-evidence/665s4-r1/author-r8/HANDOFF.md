# [A698i] #665 S4 round 8

STATUS: REVIEW READY. Every gate of the round 8 ruling is rc 0 at `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, on clean clones.

- Head: `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, tree `ffa577c3f64cf996b3561593ad02636ce2ce4ff9`, local branch `s4-f1-target` in `$LANES/665-s4-f1-target`. PR #812 targets `dev-soft-core`. Nothing pushed; the live PR head is still `37e03930`.
- Two commits on `37e0393094`, no rebase, no force. Subjects are one line, with no body and no trailers.
- `origin` is `https://github.com/kebag-logic/milan-fpga.git`. `dev-soft-core` is `a68536fa`, live and the one merge base. No file under `hdl/` differs from it. No `.sv`, `.v`, `.c` or `.h` file and no gitlink changed this round.
- Assignment: [A10] issuecomment-6692215350. Reviews: R737-4 (issuecomment-6692178209, NEGATIVE), R738-5 (issuecomment-6692208886, POSITIVE).
- TAKEN: issuecomment-6692335687. REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6693602606 (`REVIEW-READY-COMMENT.md`).

## Read these first

1. **One file is outside the ruling's list.** The ruling says "Keep the change to these files". `sw/firmware/ctrl/README.md:711,719-722` quoted the self-test's 37 checks and its "last four", so the checks the ruling requires would have made that page false. I corrected it in `b7fe6a777e`, a commit of its own, so it can be dropped alone. TAKEN stated this before the edit, and no reply came. If you drop it, re-run the docs gates and the page is stale by exactly those lines.
2. **Two listed items were fixed by the same edit, as the ruling allows.**
   - R738-5-S2: the ruling's "before the compiler is called" needs a check, and that check lives in the helper the no-map cases share. Moving the refusal to just before the link now turns the self-test red.
   - R737-4-R1: the PR body's `How to validate` must expect 40 checks, which only this head gives, so its checkout had to name this head.
   - Nothing else was folded in. R738-5-S1, RES1 and RES2 are untouched, so RES1 and RES2 still go to #495 with the retained residue.
3. **The refusal's limit, stated in the tree.** It reads that both headers are there, not what they say. A hand-edited header holding the stand-ins' values passes it. Empty headers stop in the compiler (`receipts/runs/map-edges.log`). The four statements are worded to what the check proves: the image takes no header of the stand-ins.
4. **I ran more than the ruling's gates.** None of them links a real generated map, so a refusal that wrongly rejected a complete map would pass them all. S3's boots at both shapes and the probes cover that. They are not long gates.

## Changes

| Where (at the head) | What | Why |
|---|---|---|
| `sw/firmware/ctrl/test/ctrl_plat_image.py:56,58-59` | `MAP_HEADERS`, `PARTIAL_MAP` | What a map must hold, and the words naming what it lacks. |
| `sw/firmware/ctrl/test/ctrl_plat_image.py:62-71` | `refuse_placeholder` gains the header arm | The ruling. Already the first step of `main` (`:175`), so it runs before the compiler is looked up. |
| `sw/firmware/ctrl/test/ctrl_plat_image.py:14-19` | Docstring | Statement 1 of 4: narrowed to which headers an image takes, and to platform images. |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:30-38` | Docstring | Statement 2 of 4. |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:51,69-75` | `re`, `LACKS`, `MAP_CSR`, `MAP_MEM` | The words the new checks hold the refusal to. |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:440-445` | `plat_refused` | Words first, then an empty output directory: "before the compiler is called". |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:448-452` | `flash_map` | The fixture carries the complete map shape. It is no longer also the run's output directory. |
| `sw/firmware/ctrl/test/ctrl_image_selftest.py:455-475` | `plat_cases`, three new checks | JSON-only and each missing header, at the shape's clock, read from the clock check's own words. |
| `sw/firmware/ctrl/plat/README.md:101-103,126` | The refusal, why, and its limit | Statement 3 of 4. Line 126 names the same control. |
| `sw/firmware/ctrl/README.md:711,719-722` | 40 checks, the last seven | See item 1 above. |
| PR body, Round 6's "On no F1 placeholder" paragraph (the live body's line 217) | Narrowed the same way | Statement 4 of 4. |

Shared files touched: `ctrl_image_selftest.py` and `sw/firmware/ctrl/README.md` (the control firmware's), and S3's `plat/README.md`. Not touched: `ctrl_srp_image.py`, `ctrl_runs.py`, `split_soc.py`, `boot_soc.py`, `run.py`. The size fixture stays out, as ruled in issuecomment-6691621669.

PR body: the live body with `[A698i]`, the status, the Contents (Round 7 was missing, Round 8 added), the executor line, the checkout, the 40 checks, the fourth statement, and a round 8 section.

## New checks: planted mutant and failing words

Each planted literally in a clean clone of the head, one at a time, by `scripts/mutants.py`. Every check is green with no mutant first. Result: `mutants: 15 planted, 0 escaped; clone clean after: True` (`receipts/mutants.md`, `receipts/mutants/`, `receipts/runs/mutants2.log`).

"Green first" counts the `plat` checks that passed before the failure, so a mutant failing at 5 or 6 shows that check can fail while the earlier new checks stay green.

| Check | Planted defect | Green first | Failing words |
|---|---|---:|---|
| Lacking `csr.h` | `header-refusal-removed` | 4 | `AssertionError: ('lacks-csr', ...`, a compile error's last line |
| Lacking `csr.h` | `csr-not-required` | 4 | same |
| Lacking `csr.h` | `one-header-accepted`, refused only when both are missing | 4 | same |
| Lacking `csr.h` | `names-every-header` | 4 | `AssertionError: ('lacks-csr', "REFUSED: the flash map lacks generated/csr.h and generated/mem.h: ...` |
| Lacking `csr.h` | `header-refusal-after-compile` | 4 | `AssertionError: ('lacks-csr', ...`, a compile error's last line |
| Lacking `mem.h` | `mem-not-required` | 5 | `AssertionError: ('lacks-mem', ...`, a compile error's last line |
| JSON-only | `lone-json-accepted`, refused only when one is missing | 6 | `AssertionError: ('lacks-json-only', 'collect2: error: ld returned 1 exit status')` |
| JSON-only, nothing left | `json-only-refused-after-compile` | 6 | `AssertionError: ('lacks-json-only', 'went on before its refusal', ...` |
| Complete map | `complete-map-refused` | 3 | `AssertionError: REFUSED: the flash map lacks : ...` |
| Complete map | `fixture-json-only`, the fixture cut back | 3 | `AssertionError: REFUSED: the flash map lacks generated/csr.h and generated/mem.h: ...` |
| No map, nothing left | `whole-refusal-after-compile` (R738-5-S2's) | 0 | `AssertionError: ('both-archives', 'went on before its refusal', ...` |
| No map | `no-map-refusal-removed` | 0 | `AssertionError: ('both-archives', 'collect2: error: ld returned 1 exit status')` |
| No map | `any-archive-to-all` | 1 | `AssertionError: ('the-C-library-alone', 'collect2: error: ld returned 1 exit status')` |
| Complete map | `refused-with-a-map` | 3 | `AssertionError: REFUSED: no --flash-map: ...` |
| `ctrl_runs.stopped_at_link` | `compile-only-refused` | | `exit 2; ELF present False; stopped_at_link False` |

`lone-json-accepted` is the proof of "at the shape's true clock": its run passes the clock check and stops at the link, on R737-4's exact defect. The single-header mutants stop in the compiler instead, because the fixture's held header is empty; they still go red at their own check.

The driver's first run exited 1 with no defect escaped. `names-every-header` went red at its own check, but my expected words used a single quote where Python printed a double one. I corrected the words, added `json-only-refused-after-compile`, and re-ran the whole driver. Kept as `receipts/kept/mutants-attempt1-driver-word.log`.

## Verification R737-4 names

`receipts/runs/partial-map-probe.log`: the reviewer's `partial_map_probe.sh`, unedited, on a fresh boot's true map and archives. Its three partial cases give rc 2 and no ELF, each naming what it lacks. Its control gives rc 0, with `lui 0xf0004` 0 and `lui 0x20000` 0.

`receipts/runs/map-edges.log`: `scripts/map_edges.sh`, the shapes an existence check might miss.

| Map | rc | ELF | Stops at |
|---|---:|---|---|
| Complete (control) | 0 | yes | 0 and 0 in `ls_*` |
| Empty `generated/csr.h` | 2 | no | the compiler, `ls_timer` |
| Empty `generated/mem.h` | 2 | no | the compiler, `ls_read` |
| A directory at `generated/csr.h` | 2 | no | the refusal |
| A dangling link at `generated/mem.h` | 2 | no | the refusal |
| Flattened, as `author-r1/receipts/flash-map-1x1/` | 2 | no | the refusal |
| An absent path | 2 | no | the refusal |
| A file, not a directory | 2 | no | the refusal |
| No `flash_port.json`, both headers there | 2 | no | its read, as before |
| Complete, by a relative path | 0 | yes | 0 and 0 in `ls_*` |

`receipts/runs/image-hashes.txt`: the loaded ELFs at this head are byte-identical to round 7's at both shapes (`9cdee285...` at 1x1, `35ee29fa...` at 8x8). No figure moves.

## Gates

All at `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, each on a clean clone, every clone clean after. Receipts in `receipts/`, indexed in `receipts/INDEX.md`. The first five rows are the ruling's; the rest are additions.

| Gate | rc | Result |
|---|---:|---|
| `ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 40 checks PASS` |
| `firmware_boundary --without verilator` | 0 | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link; `ctrl_image_selftest.py: exit 0` |
| `firmware_boundary --only verilator` | 0 | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link |
| `docs.yml`, every job, each on a fresh clone with an empty `HOME` and a new virtual environment | 0 | 71 steps ran, each rc 0; 24 not run, each with its reason; all three SDK steps downloaded the archive, verified `d42680e9...` and printed `SDK fresh installation: verified`. Its two builder legs print `ALL GATES PASS EXCEPT 16 NOT RUN` and `EXCEPT 1 NOT RUN`, the counts round 7's printed; this round has no separate builder run behind them |
| `git diff --check` and the privacy check | 0 | rc 0 against `a68536fa` and `37e03930`; `0 private line(s) in a68536fa..HEAD`; one merge base, still `dev-soft-core`'s tip |
| The fifteen literal mutants | 0 | `mutants: 15 planted, 0 escaped; clone clean after: True` |
| The reviewer's `partial_map_probe.sh`, unedited | 0 | as above |
| `map_edges.sh` | 0 | as above |
| S3's split boot, 1x1 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 84.372 ms, 4,218,617 CPU cycles, 18 of 18 writes |
| S3's split boot, 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 184.622 ms, 9,231,088 CPU cycles, 18 of 18 writes |
| `check_py_idiom.py` | 0 | no new finding |

The two boundary modes ran concurrently on two clones (`wt-bnd`, `wt-bnd2`), beside the docs replay. There is no `seq_boundary.sh` this round, so nothing published disagrees with what ran (R737-4-S1's point).

## Not done

- The 97 short gates, the other long gates, S2 and S4 at either point, the D5 plant, S3's self-test and its placement controls: the ruling names its gates and says no long gates. `split_soc.py`, `boot_soc.py`, `run.py`, the firmware C and the RTL are unchanged.
- A review of this head. Hosted CI: nothing pushed, so all of this is local evidence.
- R738-5-S1, R738-5-RES1, R738-5-RES2, R737-4-S1, R737-4-S2 and the retained items: not in the ruling, left alone.
- The two open questions stand: the gate environment's SDK is not the pinned build (this round's `env.sh` says so), and S2's 8x8 page needs an owner.

## Resources

CPUs 88-95, this session's own, at nice 10, in units capped at MemoryMax 10G and MemoryHigh 8G. The highest recorded gate peak was 4,585,979,904 bytes (4.3 GiB), `firmware_boundary_verilator`, against the 10 GiB cap. The docs unit peaked at 6,305,370,112 bytes (5.9 GiB). No Vivado, sweep, hardware, flashing or sub-agents.
