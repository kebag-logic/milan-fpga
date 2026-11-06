## Round 8: a flash map without its headers

Relates to #665.

[The ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6692215350) answers [R737-4](https://github.com/kebag-logic/milan-fpga/pull/812#issuecomment-6692178209), NEGATIVE at `37e0393094` on one MINOR. [R738-5](https://github.com/kebag-logic/milan-fpga/pull/812#issuecomment-6692208886) was POSITIVE at that head.

| Commit | Change |
|---|---|
| `81edf650cc` | `ctrl_plat_image.py` refuses a `--flash-map` that lacks `generated/csr.h` or `generated/mem.h`, before the compiler is called. `ctrl_image_selftest.py` carries a complete map fixture and tests each missing header. Three of the four statements are narrowed. |
| `b7fe6a777e` | `sw/firmware/ctrl/README.md` states the self-test's 40 checks and its partial map refusals. |

| Finding | Severity | Outcome |
|---|---|---|
| R737-4-F1 | MINOR | A map that lacks a header is refused by name, at exit 2, with no ELF. Round 8's checks are below. |
| R737-4-R1 | RESIDUE | Fixed by the same edit: `How to validate` now expects 40 checks, which only this head gives, so the checkout above it names this head. |
| R738-5-S2 | SUGGESTION | Fixed by the same edit: the ruling's "before the compiler is called" needs its check, and the no-map cases share that helper. Moving the refusal to just before the link now turns the self-test red. |

**One file outside the ruling's list.** The ruling keeps the change to the four named places. `sw/firmware/ctrl/README.md:711,719-722` quoted the self-test's 37 checks and described its last four, so the ruled checks would have made that page false. It is corrected in `b7fe6a777e`, a commit of its own, which can be dropped alone. This was stated in the TAKEN comment before the change was made.

Nothing else changed. The size fixture and `ctrl_srp_image.py` stay out, as [ruled](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6691621669).

### What a partial map does now

The refusal reads `REFUSED: the flash map lacks generated/csr.h and generated/mem.h: a split platform image is never linked on the flash port's RV32 stand-ins; gen_flash_port.py writes the whole map`, exit 2, and names only the headers that are missing. It is in `refuse_placeholder`, the first step of `main`, so the output directory stays empty.

**Its limit:** it reads that both headers are there, not what they say. A hand-edited header holding the stand-ins' values would pass it. The plat page and the function's docstring say so.

The reviewer's `partial_map_probe.sh`, unedited, on the true map and true archives of a fresh boot at this head:

| Map | rc | ELF | Result |
|---|---:|---|---|
| Complete | 0 | yes | `lui 0xf0004` 0, `lui 0x20000` 0 in `ls_*` |
| `flash_port.json` alone | 2 | no | names both headers |
| Without `generated/csr.h` | 2 | no | names `generated/csr.h` |
| Without `generated/mem.h` | 2 | no | names `generated/mem.h` |

The other shapes a map can take, on the same inputs (`map_edges.sh`):

| Map | rc | ELF | Stops at |
|---|---:|---|---|
| A directory in `generated/csr.h`'s place | 2 | no | the refusal |
| A dangling link in `generated/mem.h`'s place | 2 | no | the refusal |
| Headers flattened to `generated-csr.h` and `generated-mem.h`, the layout of the published receipts | 2 | no | the refusal |
| A path that does not exist | 2 | no | the refusal |
| A file, not a directory | 2 | no | the refusal |
| An empty `generated/csr.h` | 2 | no | the compiler: `ls_timer` |
| An empty `generated/mem.h` | 2 | no | the compiler: `ls_read` |
| No `flash_port.json`, both headers there | 2 | no | its read, as before |
| The complete map by a relative path | 0 | yes | `lui 0xf0004` 0, `lui 0x20000` 0 in `ls_*` |

No figure moves. The images at this head are byte-identical to round 7's at both shapes, and S3's boots land on the same cycles: 84.372 ms and 4,218,617 CPU cycles at 1x1, 184.622 ms and 9,231,088 at 8x8.

### The four statements

| Place | Now says |
|---|---|
| `ctrl_plat_image.py:14-17` | a link without the map, or with one that lacks either header, is refused before the compiler is called, "so a linked platform image takes no header of the port's RV32 stand-ins" |
| `ctrl_image_selftest.py:30-38` | "links no image that takes a header of the flash port's RV32 stand-ins", then what each case shows |
| `plat/README.md:101-103` | who is refused and why, and "The refusal reads that both headers are there, not what they say." |
| This body, [Round 6](#round-6-generated-flash-map-in-the-platform-boot) | "so an image `ctrl_plat_image.py` links takes no header of the stand-ins", with the same limit |

Each claim moved from what an image carries to which headers it takes, because that is what the check can prove. The size fixture is outside them: the two tree statements that said "split image" now say "platform image" or name the tool.

### New checks and their mutants

The self-test holds 40 checks, 7 of them `plat`. The map fixture is complete, and is no longer also the run's output directory. The partial maps are at the shape's own clock, read from the clock check's words, so only their refusal keeps them from the compiler. The JSON-only row below shows that: its run gets past the clock check and stops at the link.

Each mutant was planted literally in a clean clone of this head, one at a time, and every check is green with no mutant. The last column counts the `plat` checks that passed before the failure, so a mutant failing at 5 or 6 leaves the earlier new checks green.

| Check | Planted defect | Green first | Its words |
|---|---|---:|---|
| Lacking `csr.h` | the header refusal removed | 4 | `AssertionError: ('lacks-csr', ...`, a compile error |
| Lacking `csr.h` | `csr.h` not required | 4 | `AssertionError: ('lacks-csr', ...`, a compile error |
| Lacking `csr.h` | refused only when both are missing | 4 | `AssertionError: ('lacks-csr', ...`, a compile error |
| Lacking `csr.h` | the refusal names every header, not the missing one | 4 | `AssertionError: ('lacks-csr', "REFUSED: the flash map lacks generated/csr.h and ...` |
| Lacking `csr.h` | the header refusal moved after the compile | 4 | `AssertionError: ('lacks-csr', ...`, a compile error |
| Lacking `mem.h` | `mem.h` not required | 5 | `AssertionError: ('lacks-mem', ...`, a compile error |
| JSON-only | refused only when one is missing | 6 | `AssertionError: ('lacks-json-only', 'collect2: error: ld returned 1 exit status')` |
| JSON-only, nothing left | the JSON-only refusal moved after the compile | 6 | `AssertionError: ('lacks-json-only', 'went on before its refusal', ...` |
| Complete map | refused even when complete | 3 | `AssertionError: REFUSED: the flash map lacks : ...` |
| Complete map | the fixture cut back to a lone `flash_port.json` | 3 | `AssertionError: REFUSED: the flash map lacks generated/csr.h and generated/mem.h: ...` |
| No map, nothing left | the whole refusal moved after the compile (R738-5-S2's) | 0 | `AssertionError: ('both-archives', 'went on before its refusal', ...` |
| No map | the refusal's call removed | 0 | `AssertionError: ('both-archives', 'collect2: error: ld returned 1 exit status')` |
| No map | `any` archive changed to `all` | 1 | `AssertionError: ('the-C-library-alone', 'collect2: error: ld returned 1 exit status')` |
| Complete map | the no-map refusal fires with a map | 3 | `AssertionError: REFUSED: no --flash-map: ...` |
| `ctrl_runs.stopped_at_link` | refused with no archives as well | | `exit 2; ELF present False; stopped_at_link False` |

The last four replant round 7's mutants, because this round rewrote their function.

### Gates

Every gate ran on a clean clone of `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, the tree checked clean after each.

| Gate | rc | Result |
|---|---:|---|
| `ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 40 checks PASS` |
| `firmware_boundary --without verilator` | 0 | `ctrl_boundary: PASS`; its four `ctrl_plat_image.py` runs stopped at their link |
| `firmware_boundary --only verilator` | 0 | `ctrl_boundary: PASS`; its four `ctrl_plat_image.py` runs stopped at their link |
| `docs.yml`, every job, each on a fresh clone with an empty `HOME` and a new virtual environment | 0 | 71 steps ran, each rc 0; 24 not run, each with its reason; all three SDK steps downloaded the archive, verified `d42680e9...` and printed `SDK fresh installation: verified`. Its two builder legs print `ALL GATES PASS EXCEPT 16 NOT RUN` and `EXCEPT 1 NOT RUN`, the counts round 7's printed; this round has no separate builder run behind them |
| `git diff --check a68536fa`, merge bases | 0 | rc 0; one merge base, `a68536fa`, still `dev-soft-core`'s tip |
| The privacy check | 0 | `0 private line(s) in a68536fa..HEAD` |
| The fifteen literal mutants | 0 | `mutants: 15 planted, 0 escaped; clone clean after: True` |
| The reviewer's `partial_map_probe.sh`, unedited | 0 | three partial maps rc 2 with no ELF; the complete map rc 0 with 0 and 0 |
| `map_edges.sh` | 0 | as tabled above |
| S3's split boot, 1x1 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 84.372 ms |
| S3's split boot, 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 184.622 ms |
| `check_py_idiom.py` | 0 | no new finding |

The first five rows are the ruling's. The rest are additions: no named gate links a real generated map, so S3's boots and the probes are what show a complete map is still accepted.

The mutant driver's first run exited 1 with no defect escaped: one row's expected words had the wrong quote character, though that mutant went red at its own check. The words were corrected and the whole driver run again, with one mutant added.

This is local evidence; the hosted contexts on the pushed head remain mandatory.

### What this round did not run or change

- The 97 short gates, the other long gates, S2 and S4 at either point, the D5 plant, S3's self-test and its placement controls: the ruling names its gates and says no long gates. `split_soc.py`, `boot_soc.py`, `run.py`, the firmware C and the RTL are unchanged.
- No sweep and no Vivado route: RTL is unchanged.
- R738-5-S1, R738-5-RES1, R738-5-RES2 and the retained SUGGESTION and RESIDUE items: left as they are, for the checklist and #495. The wording R738-5-RES1 and RES2 name is unchanged in this body.
- The two open questions stand: the gate environment's SDK, and an owner for S2's 8x8 page. This round's runs used that same SDK.
