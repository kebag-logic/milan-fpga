[R737] NEGATIVE - exact head b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce

# R737-5: internal independent delta review of PR #812 (issue #665, S4, round 8)

Head `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, tree `ffa577c3f64cf996b3561593ad02636ce2ce4ff9`, against the round 8 ruling (issuecomment-6692215350). The delta is `37e0393094..b7fe6a777e`, four files.

**One open MINOR, and it is one sentence of prose.** The refusal, the fixture, the checks and their mutants are all right, and R737-4-F1 is resolved at its cause. But the sentence the delta wrote at `plat/README.md:102` says an image on the stand-ins hangs before its banner, and that is false for a map lacking `generated/csr.h`. Such an image boots to ready and passes the split boot at both shapes. The ruling named this statement to be made true or narrowed, so the verdict is NEGATIVE. No code, test or figure needs to change.

## 1. Focus results

| Ruling item | Result | Evidence |
|---|---|---|
| Refuses a map lacking either header | **Met** | `ctrl_plat_image.py:68-71`. Real map and archives: `receipts/link-probes.txt` and the published `author-r8/receipts/runs/partial-map-probe.log`. |
| Before the compiler is called | **Met, shown directly** | A logging compiler recorded 0 calls and 0 files left for no map, JSON-only, lacking `csr.h` and lacking `mem.h`. The complete-map control called it (`receipts/link-probes.txt`). |
| Self-test fixture has the complete map shape | **Met** | `ctrl_image_selftest.py:448-452,465-466`. It matches `gen_flash_port.py:372-373`, and it is no longer also the run's output directory. |
| JSON-only and each missing header tested, each with a planted mutant | **Met** | `ctrl_image_selftest.py:470-474`, at the shape's own clock. Published `mutants: 15 planted, 0 escaped`; I reproduced 4 of those and added 4 of my own (section 3). |
| The four universal statements true or narrowed | **Not met for one of the four** | Section 2 table; F1. |
| README `sw/firmware/ctrl/README.md` | **Accepted, and true** | Seven `plat` checks are the last group (`ctrl_image_selftest.py:492-495`), and `receipts/image-selftest.txt` prints 40. |
| Size fixture stays out | **Met** | `ctrl_srp_image.py` is not in the delta. |
| Scope held to the ruled files | **Met** | `git diff --name-status 37e0393094..HEAD` lists four files, all modes 100644. |

## 2. Findings

**R737-5-F1 | MINOR | Conformance, Docs | `sw/firmware/ctrl/plat/README.md:102` | "Such an image hangs before its banner" is false for a map that lacks `generated/csr.h`.**

- Authority: ruling issuecomment-6692215350, second bullet: make the four universal statements true, or narrow them, naming `plat/README.md:101`. AGENTS section 6, `Docs`: changed contracts are reflected truthfully.
- Evidence: round 7's sentence had one antecedent, a link with no map. The delta widened it to line 101's "or with a map that lacks `generated/csr.h` or `generated/mem.h`", and line 102 then says "such an image hangs before its banner". I booted each case at this head.

| Image | Stand-in loads in `ls_*` (`lui 0xf0004` / `lui 0x20000`) | Shape | Boot result |
|---|---|---|---|
| Complete map, the control | 0 / 0 | 1x1 | ready at 84.372 ms, 4,218,617 CPU cycles, `PASS (0 finding(s))` |
| Stand-in `mem.h` only | 0 / 1 | 1x1 | no banner, transcript `''`, simulation time limit |
| Both stand-ins, as no map or JSON-only | 3 / 1 | 1x1 | no banner, transcript `''`, simulation time limit |
| **Stand-in `csr.h` only** | **3 / 0** | 1x1 | **ready at 84.401 ms, 4,220,051 CPU cycles, banners 1, `PASS (0 finding(s))`** |
| **Stand-in `csr.h` only** | **3 / 0** | 8x8 | **ready at 184.677 ms, 9,233,841 CPU cycles, banners 1, `PASS (0 finding(s))`** |

- The plant is the real case: with the header refusal removed in a disposable copy, a true map with `generated/csr.h` deleted links an ELF byte-identical to the booted one (`e6a26030...`), and the same holds for `generated/mem.h` (`c293950a...`). See `receipts/fallback-elf.txt` and `receipts/boot-images.txt`. The control reproduces the published hash `9cdee285...` and the published cycles, so the environment is not the difference.
- Impact: the page misdescribes the failure this refusal exists for. A reader would expect a missing `csr.h` to announce itself on the boot SoC by never printing a banner. It does the opposite: the image boots and the split boot grades it clean, so this refusal is the only thing that stops it.
- Why MINOR and not RESIDUE: the edit is prose, but the sentence states a measured behaviour, the measurement contradicts it, and the ruling required it to be true. That is a claim, not phrasing. If the manager reads it as wording alone, the fix below stands unchanged.
- Required outcome: `plat/README.md:102` holds for every case line 101 names. Suggested text: "The compiler would otherwise find the port's RV32 stand-ins in their place, with no diagnostic. On the boot SoC, an image on the stand-in `generated/mem.h` hangs before its banner; one on the stand-in `generated/csr.h` alone reaches its ready line and passes the split boot simulation, so only this refusal stops it."
- Verification: the sentence against the table above, and the docs gates. Image bytes do not move.

### Universal statements

| Place | Result |
|---|---|
| `ctrl_plat_image.py:14-17` | **True.** The stand-in tree holds only `generated/csr.h` and `generated/mem.h` (`git ls-files sw/firmware/ctrl_nvm/test/rv32`), both are checked, the port includes them with angle brackets (`nvm_flash_litespi.c:44-45`), and the map's directory precedes the stand-ins (`ctrl_srp_image.py:77-78`). Complete map: 0 and 0 in `ls_*`. |
| `ctrl_image_selftest.py:30-38` | **True**, on the same grounds; each case it lists is a check. |
| `plat/README.md:101-103` | Lines 101 and 103 **true**. Line 102 **false in one case**: F1. |
| PR body, Round 6 paragraph (line 219) | **True**, with the limit stated. |

### RESIDUE

**R737-5-R1 | RESIDUE | Docs | PR body line 422 | "The first step of `main`" is not quite the first.** `main` parses its arguments and makes the output directory first (`ctrl_plat_image.py:170-173`); the conclusion, that the directory stays empty, is true. Exact fix: "the first step of `main` after it makes the output directory, so that directory stays empty". The REVIEW READY comment repeats the phrase.

### SUGGESTION

**R737-5-S1 | SUGGESTION | Tests | `ctrl_image_selftest.py:470-474` | The refusal's `is_file` is not pinned.** Changing `.is_file()` to `.exists()` leaves all seven checks green (`receipts/mutants.txt`). The published `map_edges.sh` shows a directory at a header is refused at this head, but nothing lasting holds that. Optional outcome: one more fixture with a directory at a header.

**R737-5-S2 | SUGGESTION | Tests | `ctrl_image_selftest.py:472` | A partial map with absent archives is not tested.** Limiting the header refusal to runs whose archives exist leaves all seven checks green. Such a run would compile on the stand-ins, stop at its link and make no ELF, so no image is at risk, but `plat/README.md:101` says it is refused before the compiler. Optional outcome: one case with absent archives.

**R737-5-S3 | SUGGESTION | Tests, Docs | `tb/verilator/ctrl_split_boot/run.py` grade | The split boot cannot see the `csr.h` half of the map.** F1's table shows `PASS (0 finding(s))` on an image whose flash port CSR accessors and timer are at stand-in addresses. No statement I found claims otherwise, and the ruling does not reach it, so this is not a finding against the round. But a boot PASS is no evidence that the port's CSR addresses are right; the `ls_*` scan is. Optional outcome: a new Issue for a lasting check, such as a boot-time flash port access or a committed scan of the linked image.

**R737-5-S4 | SUGGESTION | Docs | `ctrl_plat_image.py:53,58` | The refusal words keep "never linked".** A map whose header holds the stand-in's bytes is linked at rc 0, which is how these probes were built, so "is never linked on the flash port's RV32 stand-ins" is wider than the check. The limit is stated at `plat/README.md:103` and in the docstring, and the words print only when the link is in fact refused. Changing them also changes the self-test's expected words, so leave them unless that edit is wanted.

## 3. Executed evidence

Disposable copies only; the review clone was never mutated.

| Run | Result | Receipt |
|---|---|---|
| Full image self-test, head | rc 0, `40 checks PASS` | `receipts/image-selftest.txt` |
| Split boot control, 1x1 | rc 0, 84.372 ms, ELF equals published `9cdee285...` | `receipts/boot-base.txt` |
| Stand-in boots | Table in F1 | `receipts/boot-mem.txt`, `boot-both.txt`, `boot-csr.txt`, `boot-csr-8x8.txt` |
| True partial maps, refusal removed | Byte-identical to the planted images | `receipts/fallback-elf.txt` |
| Logging compiler | Four refusals: rc 2, 0 calls, 0 files. Control: compiler called | `receipts/link-probes.txt` |
| Complete map, absolute and relative | rc 0, 0 and 0, the same ELF | `receipts/link-probes.txt` |
| 8 mutants on the `plat` checks | 6 caught, 2 escaped (S1, S2) | `receipts/mutants.txt` |

Mutants: `header-refusal-removed` (4 checks green first), `mem-not-required` (5), `refused-only-when-both-missing` (4) and `refused-only-when-one-missing` (6) reproduce the published rows, with the same failing checks. Mine: `refusal-after-generators` caught at the first check, so moving the refusal to just before the first compile also fails; `headers-reversed` caught at JSON-only; `is-file-to-exists` and `partial-only-with-archives` escaped.

Published receipts: all 238 `author-r8` files at `f0fbd984` match `MANIFEST.json`'s `published_sha256`, with none unlisted. Spot-checked: `final-check.txt` 0 bad; `runs/identity.log` names this head and tree; `image-selftest.log`, `mutants2.log`, `partial-map-probe.log`, `map-edges.log`, `image-hashes.txt`; both `firmware_boundary` rc files 0, with `ctrl_boundary: PASS` in the first log; one docs step rc 0.

## 4. Prior public findings at this head

| Finding | Disposition |
|---|---|
| R737-4-F1 (MINOR) | **Resolved at its cause.** Three partial cases rc 2 with no ELF, control rc 0 with 0 and 0, a planted removal turns the self-test red, boundary and boots rc 0 in the receipts. Its statement list is resolved except the new sentence, which is F1. |
| R737-4-R1 (RESIDUE) | **Resolved:** PR body line 122 checks out this head. |
| R738-5-S2 (SUGGESTION) | **Resolved:** `plat_refused` holds the empty directory, and `refusal-after-generators` goes red. |
| R737-4-S1, R737-4-S2 (SUGGESTION) | **Retained:** they concern the round 7 packet, which is unchanged. |
| R738-5-S1 (SUGGESTION) | **Retained:** `run.py` is not in the delta. |
| R738-5-RES1, R738-5-RES2 (RESIDUE) | **Retained** for #495. The wording stands, now at PR body lines 337 and 388 among others. |
| R737-3-S4 (SUGGESTION) | **Retained:** `--flash-map` is still unresolved, and a relative map gives the same ELF. |
| R738-4-RES1, R738-4-RES3 (RESIDUE) | **Retained:** `ctrl_split_boot/README.md:79` and `run.py:6` are unchanged. |
| R737-3-S1 (remainder), R737-1-S2 (remainder), R737-3-S2, R737-3-S3, R738-4-S1, R738-4-S2, R737-1-S3, R737-1-S4, R737-2-S1, S2, S3, R738-3-S1 (SUGGESTION); R737-2-R1, R738-3-RES1 (RESIDUE) | **Retained:** the delta touches none of what they name. |

## 5. Per-lens results

[R737] UNCLEAN Conformance — `sw/firmware/ctrl/plat/README.md:102` against ruling issuecomment-6692215350 — F1. Every other ruling item is met (section 1): `ctrl_plat_image.py:62-71,175`, `ctrl_image_selftest.py:440-475`.

[R737] PASS RTL — `git diff --name-status 37e0393094..HEAD` and `receipts/final-state.txt` — no RTL file and no gitlink in the delta; the 1x1 image is byte-identical to round 7's (`9cdee285...`, `author-r8/receipts/runs/image-hashes.txt`), so nothing RTL depends on moved. Prior lens verdict stands.

[R737] PASS Robustness — `ctrl_plat_image.py:62-71` with `receipts/link-probes.txt` and `author-r8/receipts/runs/map-edges.log` — absent path, a file, a directory or dangling link at a header, flattened layout, empty headers and no JSON each end at rc 2 with no ELF; a relative map links correctly. A header holding stand-in bytes passes, which is the stated limit.

[R737] PASS Tests — `ctrl_image_selftest.py:440-475` with `receipts/mutants.txt`, `receipts/image-selftest.txt` and `author-r8/receipts/mutants.md` — each ruled check fails for its own planted defect, with earlier checks green. The two escapes are outside what the ruling asked (S1, S2).

[R737] UNCLEAN Docs — `sw/firmware/ctrl/plat/README.md:102` against `receipts/boot-csr.txt`, `boot-csr-8x8.txt` — F1. Checked and true: `plat/README.md:101,103,126`, `sw/firmware/ctrl/README.md:711,719-722`, both docstrings, PR body lines 122, 168, 219 and the Round 8 section apart from R1. The delta's comments and the diff show no lane label, round, reviewer ID or comment ID, and `git diff --check` is rc 0.

## 6. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling and size note; `ctrl_plat_image.py:14-19,53-71,175`; `ctrl_image_selftest.py:30-38,440-475`; `plat/README.md:101-103`; PR body | none: R737-5 found F1 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| RTL | CLEAN | Delta file list, gitlinks, `image-hashes.txt`, the control's ELF hash | R737-5 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Robustness | CLEAN | `refuse_placeholder`; `link-probes.txt`; `map-edges.log`; `ctrl_srp_image.py:55-63,77-78` | R737-5 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Tests | CLEAN | `ctrl_image_selftest.py:425-475`; `mutants.txt`; `image-selftest.txt`; published mutants and logs | R737-5 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Docs | UNCLEAN (F1) | `plat/README.md`; `sw/firmware/ctrl/README.md:711-722`; both docstrings; PR body; boot receipts | none: R737-5 found F1 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |

A fix confined to `plat/README.md` touches nothing in the RTL, Robustness or Tests scope, so those rows stay banked at this head as an ancestor; Conformance and Docs need re-covering at the corrected head.

## 7. Real limits

- All boots are simulation on the boot SoC with its stand-in register file. Physical calibration NOT RUN; nothing here is hardware proof.
- "Hangs" means no banner by the simulation's time limit, at 1x1 only for the `mem.h` and both-stand-in images. The `csr.h` image was booted at both shapes.
- I did not characterise what a stand-in `csr.h` image does after ready, such as a flash write. F1 rests only on its reaching ready.
- The RV32 SDK is the gate environment's, not the pinned build; this is the author's open question, and my hashes match theirs on it. The simulator was verified as 5.050 (`receipts/tools.txt`).
- `f0fbd984` is **unsigned** (the host reports `verified: false`, reason `unsigned`), so I could verify the packet's manifest hashes, not a signature.
- Not re-run, taken from receipts: `firmware_boundary` in both modes, the docs gates, the privacy check, the 8x8 control boot, and 11 of the 15 published mutants.
- No manager source bank exists at this head, and none is claimed. This is the source head on base `f4c9ad4f`, not the merge candidate.
- Hosted snapshot at this head, not a verdict: 17 success, 1 skipped (`Physical gPTP`, not executed), 14 in progress, 18 queued.
- `receipts/` holds trimmed copies with host paths replaced and command lines removed. `env.sh` and `job.sh` were made portable after the runs, changing path assignments only, and were syntax-checked, not re-run.

Clone state after review: head and tree as above, 0 status lines, index equal to the tree, six gitlinks unchanged (`receipts/final-state.txt`).

## 8. Pending manager duties

- Rule on F1, then route its one-sentence fix and a re-review of Conformance and Docs at the corrected head.
- Carry R737-5-R1 and the retained RESIDUE to #495.
- Decide whether R737-5-S3 becomes a new Issue.
- Own hosted and act acceptance on the final head; the jobs above were still running.
- Build and validate the current-dev merge candidate (source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`) and link its receipts.
- The standing questions remain: the gate environment's SDK, and an owner for S2's 8x8 page.

R737-5 FINISHED
