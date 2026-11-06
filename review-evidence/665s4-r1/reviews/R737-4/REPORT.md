[R737] NEGATIVE - exact head 37e0393094e62d395edc2798a6a6da2f34badbec

# R737-4: internal independent delta review of PR #812 (issue #665, S4, round 7)

Tree `671949bf0b327496993ce1462ae2f61d4125525f`. Delta `7643aef613..37e0393094`: four commits, ten files, no RTL, no firmware C, no gitlink.

One MINOR is open: R737-4-F1, under Conformance, Robustness, Tests and Docs. One RESIDUE and two SUGGESTIONs are also recorded. RTL is clean.

The round's work is otherwise sound. The refusal does what the ruling's first sentence asks, the placement controls fail for every planted deviation, the 13.861 ms figures are right, and R737-3-F1, R738-4-F1, F2 and F3 are all resolved for the outcomes they required. F1 is a new, narrower gap: the refusal tests for the flag, not for the map, so a map directory without its headers still links the ruled-out image at exit 0.

## 1. Focus results

| Focus | Result | Evidence |
|---|---|---|
| `ctrl_plat_image.py` refuses a link with no `--flash-map` | **Holds.** Real archives, no map: rc 2, named refusal, no ELF. No map and no archives: rc 2 at the link, `No such file`, no ELF. | `receipts/identity-probe.log` |
| Every caller carries the map, or stops at the link | **Holds.** `run.py:197` always passes it. The only no-map caller is `ctrl_runs.py:85`, on absent archives. No workflow or script names the builder. | Search of the tree, `.github` included |
| Its lasting test is in the boundary gate | **Holds.** 37 checks, four of them `plat`. With the refusal removed, the self-test fails. With it made unconditional, `stopped_at_link` goes false. | `receipts/image-selftest.log`, `receipts/refusal-spot.log` |
| A map really is used when complete | **Holds, with F1.** True map: 0 and 0 stand-in loads at 1x1. The design page's own fence at 8x8 with two interfaces: rc 0, 0 and 0, `lui 0xf0003` 11 times. A complete map by relative path gives the same image. | `receipts/partial-map-probe.log`, `receipts/design-page-scan.txt`, `receipts/identity-probe.log` |
| Placement controls fail for planted deviations | **Holds.** 8 of 8 at both shapes on my own builds. Eight further mutants, beyond the author's nine, each gave the expected words. | `receipts/placement-1x1.log`, `receipts/placement-8x8.log`, `receipts/placement-mutants.log` |
| 13.861 ms | **Holds.** The receipt reads `13.86052` (`measurements.json:488,1350`), which rounds to 13.861. `check_nvm_capture.py` rc 0. 13.863 survives only in the design page's history. | `receipts/check-nvm-capture.log` |
| Boot figures do not move | **Holds.** My clones gave 84.372 ms and 4,218,617 cycles at 1x1, 184.622 ms and 9,231,088 at 8x8, equal to the receipts. | `receipts/boot-1x1.log`, `receipts/boot-8x8.log` |
| SIGTERM at `c2befb12` | See section 3. | |

Per the manager's ruling (issuecomment-6691621669), `ctrl_srp_image.py --layout split --with-aecp` is not reported.

The placement mutants were: a register the SoC lacks ignored, the window compared on base only and on size only, a true map always deviating, the refusal's words changed, the refusal naming no register, an unrelated failure before the guard, and an inert plant. The unrelated failure shows `OTHER` is reachable and is not counted as a refusal. The refusal naming no register shows the `MOVED in said` check is not vacuous.

## 2. Findings

**R737-4-F1 | MINOR | Conformance, Robustness, Tests, Docs | `sw/firmware/ctrl/test/ctrl_plat_image.py:15,58`; `sw/firmware/ctrl/test/ctrl_srp_image.py:55-63,78`; `sw/firmware/ctrl/test/ctrl_image_selftest.py:30,441`; `sw/firmware/ctrl/plat/README.md:101`; PR body line 217 | The refusal tests for the flag, not the map: a map directory without its headers links the no-map image byte for byte, at exit 0.**
- Authority: issuecomment-6689759393 item 1, headed "No silent placeholder image"; the option (a) ruling, "leaves no F1 placeholder in any split image". AGENTS section 6, `Robustness`: malformed and truncated input. `Tests`: each new test can fail for the defect it claims to detect.
- Evidence:
  - `refuse_placeholder` asks only whether `flash_map is None` (`ctrl_plat_image.py:58`).
  - `flash_port()` reads `clock_hz` from `flash_port.json` and returns `-I{flash_map}`. It never checks that the headers exist, and `aecp_inputs` keeps the stand-ins behind it on the include path (`ctrl_srp_image.py:78`). A map with no headers therefore falls through to the stand-ins with no diagnostic.
  - A directory holding only the true `flash_port.json`: rc 0, ELF, `lui 0xf0004` and `lui 0x20000` both present in `ls_*`. Without `generated/mem.h` only: rc 0, the stand-in window. Without `generated/csr.h` only: rc 0, the stand-in timer. Control, the complete map: rc 0, neither (`receipts/partial-map-probe.log`).
  - The JSON-only image is **byte-identical** to a no-map link with the refusal removed in a copy: both loadable images hash `52c20cff...`, and the true map's hashes `834f484b...` (`receipts/identity-probe.log`). It is exactly the image the ruling removes, and R738-4's receipts show that image never reaches ready.
  - `boot_soc.refuse_deviation` does not catch it either. `map_deviations` reads the JSON alone (`split_soc.py:102`), so the export takes this map (`receipts/json-only-export.log`).
  - The self-test's map fixture is this same shape, a lone `flash_port.json` (`ctrl_image_selftest.py:441`). Only its 1 Hz clock stops it.
  - Four statements are universal and false as written: `ctrl_plat_image.py:15` "no split image carries the port's RV32 stand-ins", `ctrl_image_selftest.py:30` "never links a split image on the flash port's RV32 stand-ins", `plat/README.md:101` "no split image is linked on the port's RV32 stand-ins", and PR body line 217 "`ctrl_plat_image.py` links no image on the stand-ins".
- Reachability, stated fully: `gen_flash_port.py:371-375` writes both headers first and the JSON last, so an interrupted generator cannot leave this state. No caller in the tree passes such a directory. It takes a hand-assembled or partly copied map. The published `author-r1/receipts/flash-map-1x1/` has that layout, with the headers flattened to `generated-csr.h` and `generated-mem.h`.
- Impact: an image that hangs before its banner, with exit 0, no diagnostic, and every guard in the chain passing. That is the failure the ruling names, on a narrower input.
- Why MINOR: the reachability above is why it is not MAJOR, and why R737-3-F1's "documented or ordinary invocation" stays resolved. It is not a SUGGESTION because the behaviour is demonstrated, the input class is one the `Robustness` lens names, and the compile had no map in any sense the image can tell: the headers are the map, and the JSON is its description. It is not RESIDUE because it concerns a generated artifact and a ruling claim.
- Required outcome: a `--flash-map` that does not supply the generated headers ends in a named refusal or no ELF, and a lasting check holds that, at the shape's true clock. The size fixture's no-map path is not touched by this. If the manager rules such a map outside the ruling, as it did for the size fixture, the four statements must instead be narrowed to what is true.
- Verification: `scripts/partial_map_probe.sh` gives rc 2 and no ELF for its three partial cases, and rc 0 with 0 and 0 for its control. `firmware_boundary` in both modes and S3's boot at both shapes stay rc 0. A planted removal of the new check turns the self-test red.

**R737-4-R1 | RESIDUE | Docs | PR body line 120 | The reproduction step pins the previous head.**
"How to get into the same state" still says `git checkout 7643aef613c5b87a246544f57d23ad9f1bf8311e`, where `--placement-controls` does not exist. Exact fix: `git checkout 37e0393094e62d395edc2798a6a6da2f34badbec`, or the final head at merge.

**R737-4-S1 | SUGGESTION | Docs | packet `author-r7/scripts/seq_boundary.sh` | The published script is not what ran.**
It runs both boundary modes in sequence on one clone. The head's receipts show `wt-bnd` from 17:00:05Z and `wt-bnd2` from 17:00:15Z, concurrently. The gate table's "clean clones" is right, so no gate claim moves, but a cold reviewer rerunning the script gets a different schedule.

**R737-4-S2 | SUGGESTION | Docs | packet `author-r7/receipts/kept/` | The kept failure's supporting claims have no receipts.**
The kept directory holds the log and rc. The 1.4 GB peak, the journal window, the session check and the overlap's times (`docs/runner.out` carries no timestamps) are statements only. Publishing the peak and journal window would cost little. "The journal shows no kill" is also weak evidence, since a journal does not record a user process's `kill`.

## 3. The SIGTERM at `c2befb12`

**Does the kept evidence support treating it as external? Yes for "external to the code under review", by exclusion. No for "a known external cause": no sender is identified.** The author's "cause not found" is the accurate wording and should stay. It is not a finding, and it does not weigh on this verdict.

What the kept log shows by itself: the direct child died of SIGTERM while `ctrl_boundary.py` lived on to print its refusal and the wrapper wrote its end line. `ctrl_capture.run` starts the child in the parent's process group, so this was not a unit-wide stop or a group signal: it reached that one process.

What I added:
- **No in-tree sender reaches it.** The firmware test tree sends no SIGTERM. Its timeouts are `subprocess` timeouts, which kill with SIGKILL and would show as -9. `ctrl_shim.py`'s `pass_on` only forwards downward to a compile. Neither submodule I searched (`tsn-c-stack`, `lwSRP`) holds a sender. The repository's real senders elsewhere (`owned_process.py`, `test_suite_cancellation.py`, the mutant drivers) act on their own children, and neither of those two scripts is named in a workflow. I read those two and did not audit every mutant driver.
- **A replay did not reproduce it.** The gate's exact command under its capture, at the head: exit 0 in 414 s, well past the 212 s mark, with the overlapping docs step looping beside it 330 times with no failure. A trace of every kill-family syscall across the whole subtree recorded **zero** calls (`receipts/sigterm-replay.log`, `receipts/sigterm-replay-kills.txt`). A positive control with the same flags recorded a child signalling its parent across a new session, so the zero can fail (`receipts/trace-control.txt`).
- **The code is the same.** `c2befb12..37e03930` changes two READMEs, so the head's passes speak for the ancestor's code.
- **The announced stop is not the cause.** The handoff says gates at `c2befb12` were stopped, but a mutant attempt at that commit started at 16:48:58Z, after the failure at 16:45:04Z, so that stop came later. A unit stop would also have taken the parent. This timing is my inference from the receipts.
- **Hosted:** the `firmware-boundary` check-run at this exact head concluded success.

Limits: this is one replay, and a sender outside the tree cannot be reproduced by nature. A same-user process signalling by name would fit everything above, and nothing here shows or excludes one.

## 4. Prior public findings at this head

| Finding | Disposition |
|---|---|
| R737-3-F1 (MINOR) | **Resolved** for its stated outcome: no documented or ordinary invocation yields the image. The narrower gap is R737-4-F1. |
| R738-4-F1 (MAJOR) | **Resolved** for its stated outcome: both pages' commands carry the map, a no-map link is refused, `stopped_at_link` holds, both modes pass in the author's receipts, and `nomap_probe.sh` shows the change. PR line 217 is restated, but overclaims: carried in R737-4-F1. |
| R738-4-F2 (MINOR) | **Resolved.** Both pages give 13.861. PR lines 53, 98 and 99 match the gated receipt and `nvm_split_target/README.md:180-181,211-214`. |
| R738-4-F3 (MINOR) | **Resolved.** The committed check is red with the guard removed and with `map_deviations` returning empty, green at the head, and runs last in `--self-test`. |
| R737-3-R1, R737-3-R2, R738-4-RES2 (RESIDUE) | **Resolved:** `ctrl_plat_image.py:13` and the help text are corrected. |
| R737-3-S1, R737-1-S2 (SUGGESTION) | Placement half and map-clock half **resolved** by F3's controls and the `plat` map case. `split_soc`'s remaining guard retained. |
| R737-3-S5 (SUGGESTION) | **Resolved:** `run_docs_yml.py` is published, and the committed controls replace `map_probe.py`. |
| R737-3-S4 (SUGGESTION) | **Retained.** `--flash-map` is still unresolved, and I confirmed a relative map gives the same image. `run.py` still restates `split-soc/flash-map`, now also at `:457,490`. |
| R737-3-S2, R738-4-S1, R737-3-S3 (SUGGESTION) | **Retained:** the pages are unchanged. |
| R738-4-RES1, R738-4-RES3 (RESIDUE) | **Retained:** `ctrl_split_boot/README.md:79`, `run.py:6`. Exact fixes as R738-4 gives them. |
| R738-4-S2 (SUGGESTION) | **Retained:** no hosted job runs the placement controls, as the page now says. |
| R738-F1, R738-F2 (MINOR), R737-1-R1, R737-1-S1 | **Stay resolved:** the delta touches nothing they depend on. |
| R737-1-S3, R737-1-S4, R738-3-S1, R738-3-RES1, R737-2-R1, R737-2-S1, S2, S3 | **Retained:** those files and lines are unchanged, and "alone in their place" and "leaves only" stand at `nvm_split_target/README.md:52`, `run.py:32` and PR body lines 30 and 85. |

## 5. Per-lens results

- [R737] UNCLEAN Conformance - `ctrl_plat_image.py:58,163`; `plat/README.md:88-102`; issuecomment-6689759393 - The four items are met as written for a link with no flag. Open: F1.
- [R737] PASS RTL - `receipts/delta-scans.txt`; `tb/verilator/ctrl_split_boot/boot_soc.py:61-66,104` - No HDL, firmware C or gitlink in the delta. `refuse_deviation` moves the same statements to the same point in `build`, and both boots reproduce the published cycle counts exactly. The prior RTL verdict stands.
- [R737] UNCLEAN Robustness - `receipts/partial-map-probe.log`; `ctrl_srp_image.py:55-63` - The no-flag, relative and wrong-clock paths behave. Open: F1, the truncated map.
- [R737] UNCLEAN Tests - `ctrl_image_selftest.py:417-445`; `run.py:453-504`; `receipts/placement-mutants.log` - Each new control can fail, and seventeen plants, the author's nine and my eight, show it. Open: F1, since the self-test claims more than it can detect.
- [R737] UNCLEAN Docs - `plat/README.md:88-102`; `SPLIT_CONTROL_MEMORY.md:316-322`; `ctrl/README.md:711,719-721`; `ctrl_split_boot/README.md:25,38,73`; PR body - Commands, paths, the 37 count and the figures are true. Open: F1's four statements.

The comment rule: 175 added source lines scanned raw, no new instance (`receipts/delta-scans.txt`). `git diff --check` rc 0. Commit bodies are empty.

## 6. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling and its four items, `ctrl_plat_image.py`, both pages' commands, PR body | R737-4 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| RTL | CLEAN | Delta file list, `boot_soc.py` refactor, boot cycle counts at both shapes | R737-4 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Robustness | UNCLEAN (F1) | Refusal and map input classes, `flash_port()`, partial-map and identity probes | R737-4 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Tests | UNCLEAN (F1) | `plat_cases`, `placement_controls`, plants, author's mutant receipts, my mutants | R737-4 | `37e0393094e62d395edc2798a6a6da2f34badbec` |
| Docs | UNCLEAN (F1) | Six delta pages, PR body lines 53, 98, 99, 120, 217, evidence packet | R737-4 | `37e0393094e62d395edc2798a6a6da2f34badbec` |

## 7. Evidence and limits

- **Packet:** all 1,689 published files of `6097421109` match `MANIFEST.json`, with none missing and none unlisted (`receipts/evidence-manifest-verify.txt`). The commit itself carries no signature, so that check proves integrity against the manifest, not authorship. Redacted files were verified as published.
- **Author receipts spot-checked, not re-run:** `docs.yml` (71 ran, 24 not run, 0 bad), `firmware_boundary` in both modes, `boot-selftest`, `nomap-probe`, the mutant table. I did not re-run `firmware_boundary` whole, `--self-test` or the docs gates.
- **Not run:** a boot of the JSON-only image. Its hang rests on byte identity with the no-map image, which R738-4 booted at the previous head.
- **My SDK** is the gate environment's, not the pinned build: the open question the author records.
- **Hosted, at the snapshot** (`receipts/hosted-check-runs.txt`): of 54 check-runs, 25 succeeded, 1 was skipped, 19 were running and 9 queued. The skipped one is the physical gPTP context and proves nothing. Job logs were not available while the run was in progress, so I could not read the `firmware-boundary` log, and the claim that the `plat` control ran there rests on the check-run and the gate's own code.
- **No manager source bank** exists at this head and none is claimed. Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Restoration:** every probe ran in disposable copies. The review clone stayed at the exact head and tree, status empty, all six gitlinks as recorded.

## 8. Pending manager duties

- Rule on R737-4-F1, or assign it. Either outcome in its required-outcome line closes it.
- Carry R737-4-R1 and the retained RESIDUE items to the residue checklist.
- Hosted and act acceptance at the final head, including the running contexts above.
- The current-dev merge candidate (builder and native banks; source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`).
- The two open questions: the gate environment's SDK, and an owner for S2's 8x8 page.

R737-4 FINISHED
