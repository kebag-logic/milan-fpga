[R737] POSITIVE - exact head 0e03192c050812c5f7d249edd8893d1ede151a78

# R737-6: internal independent delta review of PR #812 (issue #665, S4)

Head `0e03192c050812c5f7d249edd8893d1ede151a78`, tree `c40023bf15545478c40f80ecf35cfc0a3f15f362`. The delta is `b7fe6a777e..0e03192c05`: one file, one commit.

**No BLOCKER, MAJOR or MINOR is open.** The new sentences hold for every case the page's refusal line names, and R737-5-F1 and R738-6-F1 are both resolved at their cause. The sentences reach slightly further than my round 8 table did: they name no shape, and they say "with no map". I measured both gaps at this head instead of assuming them, and both hold. One RESIDUE is new: the PR body still points at the previous head.

## 1. Focus results

### Only one file changed

`receipts/delta.txt`: the recursive trees of `b7fe6a777e` and `0e03192c05` differ in one entry, `sw/firmware/ctrl/plat/README.md` (100644, blob `7bfdb032b8` to `73cb72c5e1`, 3 insertions, 1 deletion). No gitlink moved. `git diff --check` is rc 0. The commit is one line with no trailers, and its parent is `b7fe6a777e`.

Nothing in the tree pins this page's text: no script, test or feature names `plat/README`, and no tracked file cites a line of it. The old wording survives nowhere else in the tree.

### The sentences against the boots

Page lines 102-104 at this head, each against what was measured:

| Claim | Evidence | Result |
|---|---|---|
| Line 102: the compiler would otherwise find the stand-ins, with no diagnostic | With the refusals removed in a disposable copy, each partial map links at rc 0 on the stand-ins (`receipts/nomap-elf.txt`) | **True** |
| Line 103: an image on the stand-in `generated/mem.h` hangs before its banner | 1x1: `boot-mem.txt` in R737-5. 8x8: `receipts/boot-mem-8x8.txt`, new this round | **True at both shapes** |
| Line 103: an image with no map hangs before its banner | The true no-map link is byte-identical to the booted "both" image (below) | **True at both shapes** |
| Line 104: an image on the stand-in `generated/csr.h` alone boots to ready and passes the split boot | R737-5 `boot-csr.txt` and `boot-csr-8x8.txt`: ready at 84.401 ms and 184.677 ms, banners 1, `PASS (0 finding(s))` | **True at both shapes** |
| Line 104: this refusal is the only thing that stops it | Traced below | **True for the repository's link and boot path** |

All boots, with `ls_*` stand-in loads shown as `lui 0xf0004` / `lui 0x20000`:

| Image | Loads | Shape | Result | Receipt |
|---|---|---|---|---|
| Complete map, the control | 0 / 0 | 1x1 | ready at 84.372 ms, 4,218,617 CPU cycles, `PASS (0 finding(s))` | `receipts/boot-base.txt`, **this head** |
| Stand-in `mem.h` only | 0 / 1 | 1x1 | no banner, transcript `''`, time limit | R737-5 `boot-mem.txt` |
| Stand-in `mem.h` only | 0 / 1 | 8x8 | no banner, transcript `''`, time limit | `receipts/boot-mem-8x8.txt`, **this head** |
| Both stand-ins | 3 / 1 | 1x1 | no banner, transcript `''`, time limit | `receipts/boot-both-1x1.txt`, **this head** |
| Both stand-ins | 3 / 1 | 8x8 | no banner, transcript `''`, time limit | `receipts/boot-both-8x8.txt`, **this head** |
| Stand-in `csr.h` only | 3 / 0 | 1x1 | ready at 84.401 ms, 4,220,051 CPU cycles, `PASS (0 finding(s))` | R737-5 `boot-csr.txt` |
| Stand-in `csr.h` only | 3 / 0 | 8x8 | ready at 184.677 ms, 9,233,841 CPU cycles, `PASS (0 finding(s))` | R737-5 `boot-csr-8x8.txt` |

The two gaps I closed:

- **The sentence names no shape.** My round 8 table had the hang at 1x1 only, and I said so as a limit. The sentence says "On the boot SoC". I booted both hanging images at 8x8, and both hang.
- **"With no map" was a plant, not a link.** My table labelled the planted both-stand-in image "as no map or JSON-only" without linking one. With both refusals removed in a disposable copy, the true no-map link, a JSON-only map and a map lacking both headers all give `c86d8a01...`, which is the image booted above (`receipts/nomap-elf.txt`, `receipts/boot-images.txt`). So the no-map row is measured, and the "lacks both" case falls under line 103's `mem.h` clause.

The R737-5 boots ran at `b7fe6a777e`, and they still apply here. At this head a map lacking `csr.h` links to `e6a26030...` and one lacking `mem.h` to `c293950a...`, the hashes of those booted images, and the complete map links to `9cdee285...`. The control reproduces the earlier cycles exactly.

**"The only thing that stops it."** This is a universal claim, so I tried to falsify it rather than rely on my own earlier wording:

- The link audits in `ctrl_plat_image.py:178-196` read unresolved symbols, heap use, required names and sections. None reads an address. With the refusal removed, the `csr.h`-lacking map links at rc 0.
- `ctrl_srp_image.py:55-63` reads only the map's clock from `flash_port.json`.
- `split_soc.map_deviations` reads `flash_port.json` too, not the headers.
- The split boot grades such an image `PASS`.
- The only callers of `ctrl_plat_image.py` are the boundary gate, which has no archives and makes no ELF, and `ctrl_split_boot/run.py`. `nvm_split_target` and the CPU budget harness do exercise the port, but on `ctrl_srp_image.py` images, so they never see this image.

## 2. Findings

**R737-6-R1 | RESIDUE | Docs | PR body lines 20, 122, 457 and the Round 8 section | The PR body still describes the previous head.**

- Evidence: line 20 reads "REVIEW READY at `b7fe6a77...`", line 122 checks out that SHA, and line 457 cites `plat/README.md:101-103`, while those statements now run to line 105. The Round 8 commit and finding tables list neither `0e03192c05` nor the two findings it resolves.
- Why RESIDUE: this is PR body wording only. No measurement, figure, verdict or code changes. Every gate statement there is true of the head it names.
- Exact fix: line 20, name `0e03192c05` and state that the round 8 gates ran at `b7fe6a777e` and that only `plat/README.md` differs since. Line 122, check out `0e03192c050812c5f7d249edd8893d1ede151a78`. Line 457, cite `plat/README.md:101-105` and add which stand-in hangs and which boots to ready. Round 8 tables, add the commit and R737-5-F1 / R738-6-F1. Line 490 is a true record of `b7fe6a777e`, so leave it.

No other finding. The delta is prose in a page, so the source comment rule has nothing to apply to, and it carries no lane label, round, reviewer ID or comment ID anyway.

## 3. Executed evidence

Disposable copies under `scratch/` only; the review clone was never mutated.

| Run | Result | Receipt |
|---|---|---|
| Split boot control, 1x1, this head | rc 0, ELF `9cdee285...`, equal to R737-5 and to the published hash | `boot-base.txt`, `boot-images.txt` |
| Hang boots: both at 1x1; `mem` and both at 8x8 | rc 1, 3 findings each, no ready line | `boot-both-1x1.txt`, `boot-mem-8x8.txt`, `boot-both-8x8.txt` |
| True links, refusals removed | no-map = JSON-only = lacks-both = `c86d8a01...`; lacks-csr `e6a26030...`; lacks-mem `c293950a...`; control `9cdee285...` | `nomap-elf.txt` |
| Image self-test, `--require-rv32`, pristine copy of this head | rc 0, `40 checks PASS` | `image-selftest.txt` |
| Docs gates, this head | `docs_check` 0 findings across 216 md files, scrub 23/23, routing 4/4; `check_doc_paths` OK; `check_doc_style` OK | `docs-gates.txt` |

`check_doc_style` reads a fixed list of documents that does not name this page, so its pass is not evidence about these sentences. `docs_check` does cover every markdown file.

Published evidence: the packet at `f0fbd984` is immutable and predates this head. R737-5 matched all 238 `author-r8` files to their manifest hashes, and I reuse that. The author's source gate receipts are at `b7fe6a777e`; nothing they exercise differs at this head.

## 4. Prior public findings at this head

Read after my own pass over the delta.

| Finding | Disposition |
|---|---|
| **R737-5-F1 (MINOR)** | **Resolved at its cause.** Line 102 no longer makes one claim for every case. Lines 103-104 state each case's measured outcome, and they hold for every case line 101 names. |
| **R738-6-F1 (MINOR)** | **Resolved at its cause.** Its required outcome is that the page claims the hang only for what shows it, and it does. The example text's extra clause about the command master on `timer0`'s addresses was an example, not a requirement. Its table agrees with mine: 84.372 ms, 84.401 ms, 4,220,051 CPU cycles, the same `ls_*` counts. |
| R737-5-R1, R738-6-R2 (RESIDUE) | **Retained:** PR body line 422 still reads "the first step of `main`". |
| R738-6-R1 (RESIDUE) | **Retained:** `ctrl_plat_image.py` and `ctrl_image_selftest.py` are not in the delta. |
| R737-5-S1, R738-6-S1 (SUGGESTION) | **Retained:** `is_file()` is still not pinned by a lasting check. |
| R737-5-S2, R737-5-S4 (SUGGESTION) | **Retained:** the delta does not touch what they name. |
| R737-5-S3 (SUGGESTION) | **Docs half resolved:** line 104 now says the split boot passes such an image. **Tests half retained:** no lasting check reads the port's CSR addresses in a linked image. |
| R737-4-S2, R738-5-S1, R737-3-S1 (remainder), R737-1-S2 (remainder), R737-3-S2, R737-3-S3, R737-3-S4, R738-4-S1, R738-4-S2, R737-1-S3, R737-1-S4, R737-2-S1, R737-2-S2, R737-2-S3, R738-3-S1 (SUGGESTION) | **Retained:** the delta touches none of what they name. |
| R738-5-RES1, R738-5-RES2, R738-4-RES1, R738-4-RES3, R737-2-R1, R738-3-RES1 (RESIDUE) | **Retained:** the delta touches none of what they name. |
| All findings earlier rounds recorded as resolved | **Stay resolved:** nothing they depend on changed. |

## 5. Per-lens results

[R737] PASS Conformance — `sw/firmware/ctrl/plat/README.md:101-105` against ruling issuecomment-6692215350 and `receipts/boot-*.txt`, `receipts/nomap-elf.txt` — every case line 101 names has a true, measured outcome at lines 103-104, so the ruling's "make the statement true or narrow it" is met; the rest of the ruling stands from R737-5, unchanged.

[R737] PASS RTL — `receipts/delta.txt` and `receipts/final-state.txt` — no HDL file and no gitlink differs from `b7fe6a777e`, and the control's cycles and ELF hash are unchanged at this head; the prior lens verdict stands.

[R737] PASS Robustness — `receipts/delta.txt` and `ctrl_plat_image.py:62-71` — the refusal's blob is unchanged, so its edge results stand from R737-5; the new page text describes the failure paths, and `receipts/nomap-elf.txt` shows what they would produce without it.

[R737] PASS Tests — `ctrl_image_selftest.py:440-475` with `receipts/image-selftest.txt` — no test file differs, 40 checks pass at this head, and no test pins the changed page, so the delta needs no new test. S1, S2 and the Tests half of S3 stay optional.

[R737] PASS Docs — `sw/firmware/ctrl/plat/README.md:101-105` with `receipts/docs-gates.txt` — the sentences are true (section 1), no copy of the old wording remains in the tree, and line 105's limit stays consistent with line 104. The PR body is R737-6-R1, RESIDUE, which does not leave this lens unclean.

## 6. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling issuecomment-6692215350; `plat/README.md:101-105`; boot receipts here and in R737-5; `nomap-elf.txt` | R737-6 | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| RTL | CLEAN | `delta.txt`; gitlinks in `final-state.txt`; control boot and ELF hash | R737-6 (depth: R737-5 at ancestor `b7fe6a777e`, nothing in scope touched since) | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Robustness | CLEAN | `delta.txt`; `ctrl_plat_image.py:62-71`; `nomap-elf.txt` | R737-6 (depth: R737-5 at ancestor `b7fe6a777e`, nothing in scope touched since) | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Tests | CLEAN | `delta.txt`; `ctrl_image_selftest.py:440-475`; `image-selftest.txt` | R737-6 (depth: R737-5 at ancestor `b7fe6a777e`, nothing in scope touched since) | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Docs | CLEAN | `plat/README.md:101-105`; `docs-gates.txt`; tree search for the old wording; PR body | R737-6 | `0e03192c050812c5f7d249edd8893d1ede151a78` |

## 7. Real limits

- All boots are simulation on the boot SoC with its stand-in register file. Physical calibration NOT RUN, field skips are not hardware proof, and nothing here is hardware evidence.
- "Hangs" means no banner by the simulation's time limit. I did not trace the stopping access.
- "The only thing that stops it" is verified for this repository's link audits, the split boot and the callers of `ctrl_plat_image.py`. I did not characterise what a stand-in `csr.h` image does after ready, such as a flash write, or on hardware.
- A map holding stand-in bytes is stopped by nothing. Line 105 states that limit, and R738-6-R1 keeps it open as RESIDUE.
- The stand-in `csr.h` and 1x1 `mem.h` images were not re-booted at this head. They were linked here, their hashes match the images booted at `b7fe6a777e`, and no file those boots depend on differs.
- The RV32 SDK is the gate environment's, not the pinned build, which is the author's open question. The simulator was verified as 5.050 (`receipts/tools.txt`).
- `f0fbd984` is **unsigned** (the host reports `verified: false`, reason `unsigned`), so its manifest hashes were checkable but no signature was.
- Not re-run: `firmware_boundary`, the mutants and the 8x8 control boot, all taken from R737-5 and the published receipts.
- No manager source bank exists at this head and none is claimed. This is the source head on base `f4c9ad4f`, not the merge candidate.
- Hosted snapshot at this head, not a verdict (`receipts/hosted.txt`): 1 success, 1 in progress, 7 queued. The head is minutes old, so no exact-head long gate has reported.
- `receipts/` holds trimmed copies with host paths replaced and command lines removed.

Clone state after review: head and tree as above, 0 status lines, 0 ignored files, index equal to the tree, 0 blob or mode differences, six gitlinks unchanged (`receipts/final-state.txt`).

## 8. Pending manager duties

- Update the PR body per R737-6-R1, and carry it with the retained RESIDUE to the checklist (#495).
- Decide whether the Tests half of R737-5-S3 becomes a new Issue.
- Own hosted and act acceptance on this head; the jobs above had barely started.
- Build and validate the current-dev merge candidate (source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`) and link its receipts.
- The standing questions remain: the gate environment's SDK, and an owner for S2's 8x8 page.
- This is the internal positive only. The full bar still needs the second independent positive at this head.

R737-6 FINISHED
