[R738] NEGATIVE - exact head b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce

# R738-6: external independent delta review of PR #812 (issue #665, round 8)

Tree `ffa577c3f64cf996b3561593ad02636ce2ce4ff9`. Delta `37e0393094..b7fe6a777e`: two commits, four files, no RTL, no firmware C, no gitlink.

One MINOR is open: R738-6-F1, under Conformance and Docs. Two RESIDUE items and one SUGGESTION are also recorded. RTL, Robustness and Tests are clean.

The code of this round is right, and nothing in this verdict asks for a code or test change. The refusal does what the ruling asks, its checks fail for their planted defects, and R737-4-F1's behaviour is resolved at the cause. The open item is one sentence the delta widened: `plat/README.md:102` says an image built on a map lacking either header hangs before its banner. I booted both one-header images. The one lacking `generated/mem.h` hangs. The one lacking `generated/csr.h` reaches ready and passes the split boot at 84.401 ms.

## 1. Focus results

| Focus | Result | Evidence |
|---|---|---|
| Refuses a map lacking either header, before the compiler is called | **Holds.** `refuse_placeholder` runs at `ctrl_plat_image.py:175`, ahead of `fw_rv32.compiler()` at `:176`. Refused runs leave the output directory empty (`files=0`). A directory at a header is refused as well. | `receipts/map_probes.txt`, `receipts/real_link_probe.txt` |
| The fixture has the complete map shape | **Holds.** `flash_map()` writes `generated/csr.h`, `generated/mem.h` and `flash_port.json`, the three paths `gen_flash_port.py:371-375` writes. | `ctrl_image_selftest.py:448-452` |
| JSON-only and each missing header tested, each with a planted mutant | **Holds.** My run at the head gives 40 checks, 7 of them `plat`. I replanted the mutant for each new check and the complete fixture: each fails where the published table says, with 4, 5, 6 and 3 `plat` checks green first. | `receipts/selftest_head.log`, `receipts/replay_mutants.txt` |
| The four universal statements are true or narrowed | **Narrowed, with one new false sentence.** All four moved from what an image carries to which headers it takes. The sentence added beside the third is R738-6-F1. Two of the four state no limit where they stand: R738-6-R1. | Section 2 |
| `sw/firmware/ctrl/README.md`, accepted | **Holds.** 40 checks and "last seven" match my run; the order of the prose matches `plat_cases`. | `receipts/selftest_head.log` |
| The size fixture stays out | **Holds.** `ctrl_srp_image.py` is not in the delta. | `receipts/mechanical.txt` |
| Comment rule on the delta | **Holds.** No lane label, round, reviewer ID or comment ID in an added line. | `receipts/mechanical.txt` |
| A complete map is still accepted | **Holds.** A published generated map with true archives: rc 0, ELF, `lui 0xf0004` 0 and `lui 0x20000` 0 in `ls_*`. My unedited boot control reproduces 84.372 ms and 4,218,617 CPU cycles. | `receipts/real_link_probe.txt`, `receipts/boots/control.log` |

## 2. Findings

**R738-6-F1 | MINOR | Conformance, Docs | `sw/firmware/ctrl/plat/README.md:101-102` | "Such an image hangs before its banner" is false for a map lacking only `generated/csr.h`: that image boots to ready.**
- Authority: the round 8 ruling (issuecomment-6692215350), "make the four universal statements true, or narrow them", which names `plat/README.md:101`. AGENTS section 6, `Docs`: changed contracts are reflected in authoritative docs.
- Evidence:
  - At `37e03930` the sentence described only the no-map image. The delta extends it: line 101 now covers a map lacking "`generated/csr.h` or `generated/mem.h`", and line 102 says of those, "on the boot SoC such an image hangs before its banner". The hang had been measured on the no-map image only, and R738-4 records that the stopping access was not traced.
  - Booted through `ctrl_split_boot/run.py`'s own driver at 1x1, one interface:

    | Image | `lui 0xf0004` / `0x20000` in `ls_*` | Loadable sha256 | Result |
    |---|---|---|---|
    | Control, generated map | 0 / 0 | `e1e0bf8a7080e08f` | `PASS (0 finding(s))`, ready at 84.372 ms |
    | Stand-in `mem.h`, generated `csr.h` | 0 / 1 | `48598bb71f72a0c1` | `FAIL`: no ready line, transcript `''`, time limit exceeded |
    | Stand-in `csr.h`, generated `mem.h` | 3 / 0 | `2c4448a3e21821e8` | `PASS (0 finding(s))`, ready at 84.401 ms, 4,220,051 CPU cycles, 1 banner, 18 of 18 writes equal |

  - The probe puts the stand-in where the header was. To show that equals the case the page describes, I deleted `generated/csr.h` from a map, removed the refusal in a copy and linked: rc 0, loadable hash `2c4448a3e21821e8`, the same bytes that were booted (`receipts/partial_boot_check.txt`).
  - The cause, by reading: the boot reads flash through the window, so the stand-in `SPIFLASH_BASE` stops it. The stand-in `csr.h` moves only the command master and `timer0`. The stand-in master base `0xf0003000` is the real `timer0_load` address (`flash_port.json`: 4026544128), and the real master is at `0xf0002810`.
- Impact: the page names the wrong failure mode for one of the three partial maps. A reader would take a clean boot as showing the map was whole, when this image passes the boot with its flash port's command master on `timer0`'s addresses. Behaviour at this head is not affected: the refusal stops the image. The result strengthens the case for that refusal, because the boot would not have caught this image.
- Why MINOR and not RESIDUE: the fix is one sentence, but the sentence states the runtime outcome of a generated artifact and a measurement contradicts it. Correcting it changes that stated outcome, not its phrasing, so the owner rule's "no generated artifact ... claim" test is not met. It also sits inside a statement the ruling named. Under the rule's tie-break, doubt lands on MINOR.
- Required outcome: the page claims the hang only for what shows it. For example: "The compiler would otherwise find the port's RV32 stand-ins in their place, with no diagnostic. On the boot SoC, an image on the stand-in `generated/mem.h` hangs before its banner, and one on the stand-in `generated/csr.h` alone boots to ready with the flash port's command master on `timer0`'s addresses."
- Verification: read the page against `receipts/boots/stand-in-csr.log` and `stand-in-mem.log`, or rerun `scripts/partial_boot.sh`. No code, test or figure changes, so no long gate is needed. The docs gates cover the edit.

**R738-6-R1 | RESIDUE | Docs | `sw/firmware/ctrl/test/ctrl_plat_image.py:16-17`; `sw/firmware/ctrl/test/ctrl_image_selftest.py:30` | Two narrowed statements carry no limit where they stand.**
Both say a linked image takes no header of the stand-ins. A map built by hand from them passes: with links to the stand-ins, or copies, and true archives, rc 0, ELF, `lui 0xf0004` 3 and `lui 0x20000` 1 (`receipts/real_link_probe.txt`). This is the limit the author already discloses at `ctrl_plat_image.py:65`, `plat/README.md:103` and PR body lines 219 and 424, and the ruling asked for a presence check, so behaviour is as ruled. A link is a sharper case than the disclosed "hand-edited header": the compiler then reads the stand-in file itself. It takes a deliberately built map, and pointing `--flash-map` at the stand-in directory itself is refused at `flash_port.json`'s read (`receipts/map_probes.txt`). Should the manager read this as a claim about a generated artifact, it becomes a MINOR under the same two lenses, which are already unclean.
Exact fix, `ctrl_plat_image.py:16-17`: "so the compiler cannot fall through to the port's RV32 stand-ins behind a map (#665); the refusal reads that both headers are there, not what they say". Exact fix, `ctrl_image_selftest.py:30`: "ctrl_plat_image.py links no image that falls through to a header of the flash port's RV32 stand-ins:".

**R738-6-R2 | RESIDUE | Docs | PR body line 422 | "The first step of `main`" is not literally first.**
`arguments()`, the config's `resolve` and `out.mkdir` come first (`ctrl_plat_image.py:170-173`). The conclusion drawn from it is true: nothing is written to the output directory. Exact fix: "the first step of `main`'s `try`".

**R738-6-S1 | SUGGESTION | Tests, Robustness | `sw/firmware/ctrl/test/ctrl_image_selftest.py:455-475`; `sw/firmware/ctrl/test/ctrl_plat_image.py:69` | `is_file()` carries weight that no lasting check holds.**
- Evidence: `is_file()` changed to `exists()` keeps `40 checks PASS`, rc 0. Under that mutant a directory at each header compiles silently on the stand-ins: the flash port object holds `lui 0xf0004` 4 times and `lui 0x20000` once, stopped at the link only because that probe's archives were empty (`receipts/mutants_r738.txt`, `receipts/map_probes.txt`). The head is right: it refuses, and `map_edges.sh` showed that once, by hand.
- Also: limiting the header refusal to runs whose archives exist keeps 40 checks. That one is harmless, since such a run still makes no ELF.
- Why a SUGGESTION: the ruling lists a JSON-only map and each missing header, and all are held. A directory at a header is not an input any generator writes.
- Optional outcome: one more `plat` row with a directory at a header.
- Verification: the `exists()` mutant goes red.

My fourth mutant, the refusal moved to just after `source_tree`, also escapes, and is equivalent: nothing has compiled or been written by then. Moved after `prepared`, it is caught by name (`receipts/mutants_r738.txt`).

## 3. Prior public findings at this head

Read after my own pass over the diff.

| Finding | State at `b7fe6a77` |
|---|---|
| R737-4-F1 (MINOR) | **Resolved at the cause for its behaviour.** A map lacking a header ends in a named refusal with no ELF, and a lasting check holds that at the shape's true clock. Its statements half is narrowed; the sentence added beside the third is new, and is R738-6-F1. |
| R737-4-R1 (RESIDUE) | **Resolved.** The checkout at PR body line 122 names this head. |
| R737-4-S1 (SUGGESTION) | **Resolved.** The round 8 packet has no `seq_boundary.sh`, and its gate table says the two modes ran concurrently. |
| R737-4-S2 (SUGGESTION) | **Retained.** It concerns the round 7 packet, which is unchanged. |
| R738-5-S2 (SUGGESTION) | **Resolved.** The check now sits in the helper the no-map cases share. The published `whole-refusal-after-compile` mutant and my `refusal-after-prepared` both go red. |
| R738-5-S1 (SUGGESTION) | **Retained.** `run.py` and `split_soc.py` are not in the delta. |
| R738-5-RES1, R738-5-RES2 (RESIDUE) | **Retained** in the PR body, as it says. |
| R738-4-RES1, R738-4-RES3, R737-2-R1, R738-3-RES1 (RESIDUE) | **Retained.** The delta does not touch their lines. |
| R738-4-S1, R738-4-S2, R737-3-S2, R737-3-S3, R737-3-S4, R737-1-S3, R737-1-S4, R737-2-S1, R737-2-S2, R737-2-S3, R738-3-S1 (SUGGESTION) | **Retained.** The delta does not touch their files. |
| R737-3-S1, R737-1-S2 (SUGGESTION) | **Retained in part**, as R738-5 left them. |
| R738-4-F1, R738-4-F2, R738-4-F3, R737-3-F1, R738-F1, R738-F2 (MAJOR and MINOR), and the prior RESIDUE and SUGGESTION items recorded as resolved | **Stay resolved.** Nothing they depend on changed. R738-4-F1's no-map refusal still holds in the self-test's first three `plat` checks. |

## 4. Per-lens results

```text
[R738] MINOR Conformance - sw/firmware/ctrl/plat/README.md:101-102 - see R738-6-F1; the rest of the ruling is met: ctrl_plat_image.py:62-71,175 and ctrl_image_selftest.py:440-475 against issuecomment-6692215350
[R738] PASS RTL - git diff --raw 37e0393094..b7fe6a777e - four .md and .py files, no HDL, no firmware C, 0 gitlinks changed; nothing in this lens's scope moved
[R738] PASS Robustness - ctrl_plat_image.py:62-71 at b7fe6a77 - absent path, a file, a directory at a header and a missing flash_port.json each end at rc 2 with no ELF (own runs and the published map-edges.log); the stand-in directory as a map is refused; a complete map links
[R738] PASS Tests - ctrl_image_selftest.py:425-475 at b7fe6a77 - own run 40 checks; four mutants replanted, each failing where published; four new mutants, three escapes classified: one SUGGESTION, one harmless, one equivalent
[R738] MINOR Docs - sw/firmware/ctrl/plat/README.md:102 - see R738-6-F1; sw/firmware/ctrl/README.md:711,719-722 checked true against the run; R738-6-R1 and R738-6-R2 recorded
```

## 5. Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R738-6-F1) | ruling issuecomment-6692215350; `ctrl_plat_image.py:14-19,55-71,175`; `plat/README.md:101-103`; PR body lines 219, 399-510 | R738-6 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| RTL | CLEAN | `git diff --raw 37e0393094..b7fe6a777e`: no HDL, no C, no gitlink | R738-6 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Robustness | CLEAN | `ctrl_plat_image.py:62-71`; `receipts/map_probes.txt`; `receipts/real_link_probe.txt`; published `map-edges.log` | R738-6 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Tests | CLEAN | `ctrl_image_selftest.py:425-475`; `receipts/selftest_head.log`; `receipts/replay_mutants.txt`; `receipts/mutants_r738.txt`; published `mutants.md` | R738-6 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |
| Docs | UNCLEAN (R738-6-F1) | `plat/README.md:101-103,126`; `sw/firmware/ctrl/README.md:711,719-722`; `receipts/boots/*.log`; `receipts/partial_boot_check.txt`; docstrings at `ctrl_plat_image.py:14-19`, `ctrl_image_selftest.py:30-38` | R738-6 | `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce` |

## 6. Limits

- **The boot evidence is narrow.** One run per image, at 1x1 with one interface, in simulation, on the gate environment's RV32 SDK, not the pinned build. 8x8 was not booted. It disproves the sentence as a universal; it does not characterise every shape.
- **The stand-in `csr.h` image's flash write path was not exercised.** The boot passes. That the command master sits on `timer0`'s addresses is address arithmetic from the map, not a measured write.
- **I did not re-boot the no-map image.** Its hang is R738-4's measurement, and R737-4 found the JSON-only image byte-identical to it. Why the stand-in `mem.h` image stops is my reading of `ls_read`, not a trace.
- **The published packet's signature is not verified.** All 238 `author-r8` files match `published_sha256` in `MANIFEST.json`. I found no signature on the manifest, and the host reports commit `f0fbd984` as not verified. So this shows integrity against the manifest only.
- **Gates taken from receipts.** `firmware_boundary` in both modes and the `docs.yml` replay were not rerun. I spot-checked their rc files and logs (`receipts/author_spotcheck.txt`). I ran the self-test, my probes and `git diff --check` myself.
- **Two of my own first attempts failed for reasons unrelated to the head.** The system interpreter lacks `yaml`, so the self-test ran under the product environment's interpreter. My first manifest check read the wrong key and reported every file bad; `scripts/verify_packet.py` is the corrected check.
- **Hosted state is not accepted here.** At exact head I read 14 passing, 33 pending and 1 skipping, and I infer nothing from it. No manager source bank ran at this head and none is claimed.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Reproducing the boots needs the environment in the published `env.sh`, including the pinned Verilator, which reported 5.050 rev v5.050 here.

The clone is restored: head, tree, index, every tracked blob and mode, and all six gitlinks match, with no status or ignored lines (`receipts/restore_check.txt`). `external` was uninitialised from the start.

## 7. Pending manager duties

- Rule on R738-6-F1: the sentence's correction, and whether it stays MINOR. `plat/README.md` is already on the ruling's file list. The fix needs a new commit, then `Conformance` and `Docs` re-reviewed at that head. `Tests`, `Robustness` and `RTL` stay covered if only that page changes.
- Carry R738-6-R1 and R738-6-R2 to the residue checklist, #495, or fold them into the same edit.
- Decide whether `sw/firmware/ctrl/README.md`'s commit stays. This review was told it is accepted.
- Validate the current-dev merge candidate, and publish its receipts. Source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.
- Own hosted and act acceptance at the exact head, once the pending contexts finish.
- Hold the two standing questions: the gate environment's SDK, and an owner for S2's 8x8 page.
- Merge needs two independent positive reviews, the full completion bar and explicit maintainer authorization.

R738-6 FINISHED
