[R585] NEGATIVE - exact head 92b5be18817659c1c9903a0544450d29ca7ab3fd

# R585-5: external review of PR #705 (issue #697, lane 697c), round 5

- **Head:** `92b5be18817659c1c9903a0544450d29ca7ab3fd`, tree `33de4dc3c3be34efea3d50128211bd14a72ac510`. The PR head on GitHub is this commit.
- **Source base:** `8b61b70902f3ebf118e56967277e2686731081bd`. The lane merged dev `aef7ac66` (F5, AECP) in `386b8e69`, so the lane's own net change is `aef7ac66..92b5be18` (67 files). Dev `aef7ac66` is the "before" tree for images, kills and coverage below.
- **Round-5 delta:** `e07b3054..92b5be18`, five commits (`d6dd5936d`, `133ee559c`, `11529fadd`, `93540c3a8`, `92b5be188`). It adds the capture (`ctrl_capture.py`, `ctrl_shim.py`), moves the boundary step last in `firmware-unit`, runs the earlier steps under the capture, and updates the docs.
- **Reading order:** AGENTS.md, CONTRIBUTING.md (sections 2, 3, 6), docs/README.md, then the issue body. Then the owner decisions 6074086970, 6074093506 and 6074191062, the Linux/bare-metal rule, lane assignment 6091228902, the pin ruling 6092176555 and the round-5 assignment 6097800045. Then the author's REVIEW READY (round 5), the full diff and history, the published evidence `review-evidence/697c-r1` and the exact-head hosted runs.
- I read the prior public findings only after my own pass over the diff. That pass is recorded in `receipts/independent_pass_notes.txt`.

## Summary

- **Acceptance 1, 3, 4 and 5 hold at this head, re-proved independently.**
  - The pin `1a9f651c` is token-identical to dev's cores, 7 of 7 files. It is the newest such commit: the next one changes `src/adp.c`.
  - The lwSRP pin is unchanged.
  - 35 of 35 RV32 images are byte-identical between dev `aef7ac66` and the head, each tree built with its own builders.
  - No core test case was lost.
  - The firmware gate's 843 verdicts match dev's one for one. No mutant is caught by fewer checks.
  - Coverage is identical file by file over 30 files.
  - Only the intentional legacy map still names the old paths.
  - The docs gates pass on a clone without submodules.
- **Round-5 items 1 to 4 are met as built.**
  - My replica of the `firmware-unit` firmware steps under the capture recorded 23,213 invocations, the same number the author reported. The boundary step passed on it: 942 configurations, 89 boundary and 20 pin controls, 0 misbehaved.
  - Every form that rounds 2 to 4 found escaping now has a standing control that is caught.
  - A flag delivered through the environment, which no text reader could see, is caught end to end.
  - The hosted exact-head boundary step took 113 s of its 300 s budget (job 114282060753).
- **One class still escapes the capture: R585-5-F1 (MINOR).**
  - A `-D` passed to the compiler inside a GCC response file (`@FILE`) is neither a mode nor refused.
  - A real compile of a firmware unit, under that mode, included a stack `examples/` header, and the gate passed it with 0 findings.
  - No builder uses response files today (0 of 23,213 recorded invocations), so today's judgement is right. But the README's and round-5 item 1's "every `-D` ... exactly as the compiler was given it" does not hold.
- Four SUGGESTIONs, one RESIDUE (PR body), and the carried job-headroom note.

## 1. Findings

### R585-5-F1 - MINOR - Conformance, Robustness, Tests, Docs - a flag inside a compiler response file (`@FILE`) is neither a mode nor refused

`[R585] MINOR Conformance/Robustness/Tests/Docs - sw/firmware/ctrl/test/ctrl_shim.py:66-102 (parse), RECORDER; sw/firmware/ctrl/README.md:111 - a -D given to the compiler in an @response file escapes the capture's judgement`

**Where**
- `ctrl_shim.parse` (`ctrl_shim.py:95`) reads any argument that does not start with `-` as a source. So `@/tmp/x/flags.rsp` is one source of language `other`, and nothing inside it is read.
- The C recorder classifies arguments the same way. Nothing in `ctrl_capture.py`, `ctrl_configs.py` or `ctrl_boundary.py` expands or refuses an `@` argument (code search: no handling).
- GCC and Clang both expand `@FILE` into further arguments. Those can carry `-D`, `-U`, `-I`, `-include` and source names.

**Authority**
- Round-5 assignment item 1 (issuecomment 6097800045): the shim "records each invocation's source, language and every `-D`, `-U` and `-I` argument". The class was to be ruled "by construction", by judging "the builders' actual compiler invocations".
- Lane scope 3 and acceptance 2: the gate holds the firmware-side direction. The firmware reaches only the stack's public headers.
- The head's own contract says the same in three places:
  - `sw/firmware/ctrl/README.md:111`: "The build modes are every `-D` and `-U` flag of every recorded invocation, exactly as the compiler was given it".
  - `ctrl_boundary.py:63`.
  - `ctrl_configs.py:22`.

**Evidence** (`receipts/probes/`, made by `scripts/run_capture_probes.sh` with `scripts/r585_probe_builder.py`)
- **Setup.** In a disposable clone of the head, `sw/firmware/ctrl/adp/adp_mbx.c` gains `#ifdef CTRL_R585_RSP` / `#include "adp_port.h"` / `#endif`, the stack's `examples/` header. A new builder under `sw/firmware/ctrl/test/` compiles that unit by the name `gcc`, so the capture's wrapper records it, with the mode passed in a different way per probe.
- **Judgement.** The gate is run with the hosted command (`--capture` the replica's capture plus the probe's capture, `--without verilator`).
- **`env` (control).** The flag comes from an environment variable, split by `shlex`. No builder text spells it.
  - Result: CAUGHT, rc 1.
  - `firmware [-DCTRL_R585_ENV]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers`, host and RV32.
  - 23 build modes, 944 configurations.
- **`rsp`.** The same flag is written into `flags.rsp` and passed as `@<path>/flags.rsp`.
  - The builder exits 0, so GCC compiled the unit with the mode and read the stack's example header.
  - The capture holds the invocation.
  - The gate: rc 0, `0 finding(s)`, `ctrl_boundary: PASS`, 22 build modes, 942 configurations. The mode is absent.
- **Today's builders.** None of the 23,213 invocations my replica recorded carries an `@` argument (`receipts/replica/capture_stats.txt`).

**Impact**
- Response files are the compiler's own, ordinary mechanism for long command lines. Build generators and Makefiles that pass many flags use them.
- A builder written that way compiles the firmware or the stack under modes the gate never explores. A boundary include under such a mode passes the required gate silently.
- By the same reading, a C++ source named only inside the response file is not recorded as a C++ source, so its units would not be judged as C++. That is from reading the code; I probed only the `-D` case.
- Severity is MINOR, not MAJOR, because no builder at this head uses response files. The hosted and replica verdicts at this head are correct.

**Required outcome**
- A recorded invocation whose arguments include `@FILE` is either:
  - expanded as the compiler expands it, with its `-D`, `-U`, directory, forced-include and source arguments recorded like the others (the file's text is kept, as written sources are); or
  - refused by name (fail closed).
- A standing control plants a builder that passes a mode through a response file, and that control is caught or refused.
- The three statements above then hold as written.

**Verification**
- `PROBES=rsp scripts/run_capture_probes.sh <disposable clone> <capture> <out> <scripts>` gives a finding naming `-DCTRL_R585_RSP`, or a refusal by name.
- `PROBES=env` stays CAUGHT.
- `ctrl_boundary.py --require-rv32 --selftest --capture ... --without verilator` passes with 0 misbehaved.

### R585-5-S1 - SUGGESTION - Robustness, Docs - a Python builder run with `-I` (or `-E`) loads no audit hook, so an unwrapped compiler it runs by path is not seen

- **How the hook loads.** It is a `sitecustomize` on `PYTHONPATH` (`ctrl_capture.py:248`, `:129`). `python3 -I` and `-E` ignore `PYTHONPATH`.
- **Probe** (`receipts/probes/abs_*`). A builder compiles once by the name `gcc` (recorded). Then it compiles the moded unit by `/usr/bin/gcc`.
  - Run as `python3 builder.py`, the gate is REFUSED by name: "ran /usr/bin/gcc, a compiler the capture does not wrap". This is the README:104 claim, and it holds.
  - Run as `python3 -I builder.py`, the gate passes with 0 findings.
- **Scope.** This is the class the PR body already discloses: a compiler a shell script or a compiled helper runs by path is not seen. No builder runs under `-I`.
- **Suggestion.** List the limits in the authoritative README next to `README.md:104`: a Python process started with `-I`/`-E`, a shell script, and a compiled helper. Today they are only in the PR body. Or close the case by refusing a capture whose Python commands run isolated.

### R585-5-S2 - SUGGESTION - Robustness, Docs - the recorder stops keeping header texts at 256 per compile, silently

- **The cap.** `ctrl_shim.py:118` (`CLOSURE 256`) and `:403` (`while (queued > 0 && kept->count < CLOSURE)`) stop following and keeping headers past 256 per compile. `add()` also returns silently when its table is full.
- **The claim.** `README.md:93` says "every header outside the checkout that a C++ source reaches in a builder's own directories" is kept.
- **Today's use.** At most 25 texts were kept for any one invocation in my replica capture (`receipts/replica/capture_stats.txt`), so no current builder is near the cap.
- **Suggestion.** Fail closed at the cap (exit 2, as a record that cannot be written already does), or state the bound in the README.

### R585-5-S3 - SUGGESTION - Docs - the budget paragraph's projection is now measured

`docs/testing/CI_WORKFLOWS.md:78` projects about 124 s "until a hosted run measures it". The exact-head hosted step took 113 s (job 114282060753, `receipts/hosted_firmware_unit_job_114282060753.json`), which leaves 187 s of the 300 s. Consider stating it the next time the file is touched. The text is true as written.

### R585-5-RS1 - RESIDUE - Docs (PR body only) - round-5 hosted status lines are stale

This is wording only. The fix changes no code, test, figure in the tree, or verdict.
- **Round 5 table, row "4. Budget".** Replace "Not measured hosted (not pushed)." with: "Hosted at `92b5be18` (job 114282060753): the boundary step took 113 s; the store suites (108 s) and the coverage ratchet (263 s) ran; the job took 2450 s of its 2700 s."
- **Known limitations, boundary bullet.** Replace "it is not yet measured on a hosted runner." with: "on a hosted runner at `92b5be18` it took 113 s (job 114282060753)."
- **Status.** After the `e07b3054` sentence, add: "Hosted checks at `92b5be18`: `rtl-fast` success; `firmware-unit` success in 2450 s, its boundary step in 113 s; `verilator-suites` and `yosys-portability` success."

### Carried: R585-4-S1 / R584-4-S2 - SUGGESTION - Robustness - the `firmware-unit` job's own headroom

- **At this head.** The job took 2450 s of its 2700 s (9.3 % headroom). Step 8 took 1933 s and the boundary step 113 s.
- **Across branches.** On 33 recent hosted runs on all branches, the job took 1428 to 2489 s (`receipts/hosted_firmware_unit_durations.txt`).
  - Dev itself ranged from 1551 to 2250 s.
  - Branches without this lane reached 2468 s.
  - So the thin margin is runner variance shared by every lane.
- The manager ruled it outside this lane. It is not re-opened here. A separate Issue is still advised.

### Retained optional items, unaddressed at this head

- **R584-3-S1** (the force-included SRP header named as a constant; a pin recipe that ignores its exit status): retained as SUGGESTION. Its multi-word-literal part is closed by construction: the control "a multi-word literal holds a mode" passes.
- **R585-2-S2** (`aecp_arms.py:83` still adds the submodule's `tests/` under an explicit `--stack`): retained as SUGGESTION.

## 2. Acceptance, re-proved at this head

| Item | Result | Receipt |
|---|---|---|
| 1. Cores, `wire.h` and core-only tests in the chosen location; lwSRP pin unchanged | The cores and core tests are removed from `sw/firmware/ctrl` and built from `third_party/tsn-c-stack` at `1a9f651c`. The pin is token-identical to dev's copies, 7 of 7, comments dropped by the compiler's own `-fpreprocessed`. The next `main` commits `5187037` and `98dc9e3` change `src/adp.c`. lwSRP is `9197193e` at base and head. Test census: ADP 21 to 26, ACMP 63 to 69, re-entry 3, MAAP 20, MAAP debug 1; 0 lost. `acmp_nvm.c` stays, as it serves lane F1's store (assignment 6091228902 lists the three cores and `wire.h`). | `token_identity_dev_aef7ac66_vs_pin.txt`, `test_name_census.txt`, `scripts/token_identity.sh` |
| 2. A gate refuses an include from the stack into mailbox, platform, register map or image, with a planted control; and the firmware-side direction | Stack side: controls for the HAL, the contract, the composition, the store's port, the loop through a macro, the platform header, the AECP header and a stack test reaching firmware are each caught (replica). Firmware side: examples, tests, sources and shadowing copies are caught. Pin controls: 20, 0 misbehaved. Hosted exact-head step: success. Gap: F1. | `replica/6-ctrl_boundary.log`, `probes/` |
| 3. Adapters, app, loop, HAL and image build unchanged; both images byte-identical | The only firmware text touched is a comment in `mbx/mbx_wire.h`. 35 of 35 ELFs are byte-identical between dev `aef7ac66` and the head: `ctrl_image.py` at 5 shapes, and `ctrl_srp_image.py` at 5 shapes, 1 and 2 interfaces, without SRP, with SRP and with AECP. Both trees used the pinned SDK (archive `d42680e9...`, libgcc `d8ebca8c...`) and the same locally built runtime archives. The 5 `ctrl_image` hashes also equal the author's published dev `8b61b709` hashes. | `images_dev_aef7ac66.sha256`, `images_head_92b5be18.sha256`, `images_*_rc.txt`, `images_runtime_archives.sha256`, `scripts/build_images.sh` |
| 4. Every old path updated; coverage 100 %; every campaign catches the same plants | Stale-path sweep: only `ctrl_build.LEGACY`. Docs gates on a clone without submodules all pass: `docs_check`, em-dash against `aef7ac66`, doc style, submodule diagram and docs and their self-tests, PNGs, TOC. With the docs job's three submodules: `ci_events --check` (1757 items) and `--selftest` (2387 arms), `check_py_idiom`, `check_baremetal_only` and its self-test. Coverage: 30 files, identical raw and adjusted counts at dev and head. Kills: 843 of 843 verdicts the same name and outcome at dev and head, 0 caught by fewer checks. Mutant tables: 714 rows, same names; 2 needles follow the stack's reworded size assertions, in the same test and check. CI: `firmware-unit` and the `rtl.yml` Verilator workers initialise the submodule. `act_ci.py` `TRUSTED_SUBMODULES` and its self-test arms were read; I did not run them. | `stale_path_sweep.txt`, `docs_gates/`, `coverage_dev_vs_head.txt`, `firmware_verdicts_dev_vs_head.txt`, `mutant_table_compare.txt`, `mutant_table_sizes.txt` |
| 5. README in the stack's location | `sw/firmware/ctrl/README.md`, "The TSN stack submodule": what it provides (four headers, linked at the pin), what it must not depend on, how to run its tests (CMake commands), MIT inside a CERN-OHL-W platform, and lwSRP as Apache-2.0. `THIRD_PARTY.md` and `docs/reference/SUBMODULES.md` list it. | code read; `docs_gates/summary.txt` |

## 3. Round-5 items, checked at this head

| Item | Result | Receipt |
|---|---|---|
| 1. Capture | My replica of the job's five firmware commands under `ctrl_capture.py` recorded 23,213 invocations (gcc 18,218; the C++ driver 4,621; RV32 374) with 0 bypass records. The firmware suite passed under the capture, as did the store suites, the coverage self-test and the `--check`. An environment-delivered flag is caught end to end (F1's `env` control). | `replica/*.rc`, `replica/capture_stats.txt`, `replica/capture_manifest.jsonl`, `probes/env_rsp_summary.txt` |
| 2. Fail closed | Standing controls refuse each of these by name: a missing, empty or builder-less capture; a compiler run by its own path (Python and Makefile); a builder found by text that compiled nothing; a no-file or stdin C++ source; a nameless `-D`; an unshipped stream count. Two cases I met: a capture holding a failed builder run was refused by name, and a hooked absolute-path compile was refused by name. Gaps: F1, and S1 (an isolated Python process). | `replica/6-ctrl_boundary.log`, `probes/abs_hooked_summary.txt` |
| 3. Plants | 88 plants and the base, all `[ok]`. Each form named in rounds 2 to 4 is present and caught: `patsubst`, `foreach`, `VAR+=-D`, `-D $(M)`, a computed name and value, `addprefix`, a mid-string f-string, a multi-word literal, a shell literal, `shlex`, conditional, `format`, join, `%`, an f-string name, a bare `-D` list. Also the C++ names (`wildcard`, join, `glob`, `iterdir`) and the written, formatted, copied and macro-computed sources. Five passing controls pass. | `replica/6-ctrl_boundary.log` |
| 4. Budget | Hosted exact head: the boundary step took 113 s; steps 10 (108 s) and 11 (263 s) ran; the job succeeded in 2450 s. Local replica: 106 s on a shared host at load 60 to 100. | `hosted_firmware_unit_job_114282060753.json`, `replica/6-ctrl_boundary.rc` |

## 4. Prior public findings at this head

| Finding | Status at `92b5be18` | Evidence |
|---|---|---|
| R585-4-F1 (MINOR): four `-D` spellings escaped | **Resolved by construction.** Each form is a standing control, caught. A form no text holds (environment) is caught too. | `replica/6-ctrl_boundary.log`; `probes/gate-env.log` |
| R584-4-F1 (MINOR): computed or written C++ sources escaped | **Resolved.** The controls for `wildcard`, f-string include, formatted template, copied template, header written beside the source, and macro-computed include are all `[ok]`. | `replica/6-ctrl_boundary.log` |
| R584-4-F2 (MINOR): `patsubst` and `foreach` escaped | **Resolved.** Both controls are `[ok]`. | as above |
| R585-4-RS1 / R584-4-RS1 (PR body, round 4) | **Applied.** The body states the `e07b3054` hosted figures. It is superseded for round 5 by R585-5-RS1. | PR body |
| R585-4-S2 / R584-4-S1 (hosted figure in CI_WORKFLOWS) | **Applied** for `e07b3054` (`CI_WORKFLOWS.md:76`). Superseded by R585-5-S3. | `docs/testing/CI_WORKFLOWS.md:76-79` |
| R585-4-S1 / R584-4-S2 (job headroom) | **Carried**, outside the lane by the manager's ruling. New data in section 1. | `hosted_firmware_unit_durations.txt` |
| R584-3-S1 (remaining parts), R585-2-S2 | **Retained** as optional SUGGESTIONs. | code read |
| Earlier rounds (R584-1/2/3, R585-1/2/3 MINOR and MAJOR) | **Still holding.** Pin controls 20/20; the stack-pin prerequisites hold on every bench target (dry-run and poisoned-clone controls); hosted `firmware-unit`, `verilator-suites` and `yosys-portability` are green at the head. | `replica/6-ctrl_boundary.log`; hosted check runs |

## 5. Lens lines

```text
[R585] MINOR Conformance - R585-5-F1 (ctrl_shim.py:66-102; README.md:111) - a -D in an @response file is neither derived nor refused; a real compile under it passes the gate. Otherwise checked: acceptance 1 (receipts/token_identity_dev_aef7ac66_vs_pin.txt, test_name_census.txt), acceptance 3 (images_*.sha256, 35/35), acceptance 4 (coverage_dev_vs_head.txt, firmware_verdicts_dev_vs_head.txt, stale_path_sweep.txt), acceptance 5 (sw/firmware/ctrl/README.md "The TSN stack submodule"), round-5 items 1-4 (replica/, hosted job 114282060753).
[R585] PASS RTL - tb/verilator/mbx/Makefile:43-115 (stack-pin order-only prerequisite on obj_fw/libctrlfw.a, run-cosim, run-if2; FW_SRC/FW_INC from the stack's src and include), ctrl_capture.py:150-249 and ctrl_shim.py RECORDER (wrapper execs the real compiler with the same argv; record written before exec; failure exits 2), images 35/35 byte-identical dev vs head, hosted verilator-suites and yosys-portability success at the head - no HDL file in the diff; the module and bench contracts hold.
[R585] MINOR Robustness - R585-5-F1 - @response-file flags escape. Otherwise checked: fail-closed paths (missing, empty, failed-run, unheld builder, hooked path bypass: receipts/replica/6-ctrl_boundary.log, probes/abs_hooked_summary.txt); the recorder's cap (S2) and isolated Python (S1) as latent; ctime rule unexercised hosted ("installed tools' own, not followed: none").
[R585] MINOR Tests - R585-5-F1 - no control plants a response-file mode, and the gate passes one. Otherwise checked: 89 boundary and 20 pin controls [ok] in my replica; 843/843 firmware verdicts equal to dev; 714 mutant rows with expectations unchanged but two reworded needles in the same check; coverage self-test 0 rc.
[R585] MINOR Docs - R585-5-F1 - sw/firmware/ctrl/README.md:111, ctrl_boundary.py:63 and ctrl_configs.py:22 claim every -D exactly as the compiler was given it. Otherwise checked: README.md:56-168, gtest/README.md, CI_WORKFLOWS.md:53-79,206-212, SUBMODULES.md, THIRD_PARTY.md, CONTRIBUTING.md:383-391, QUICKSTART.md, MAILBOX_SPLIT.md links; docs gates on a submodule-less clone (receipts/docs_gates/summary.txt); RS1 recorded with its exact fix.
```

## 6. Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R585-5-F1) | Issue acceptance 1-5 and owner decisions; round-5 items 1-4; pin token identity; 35 images; coverage; kills; hosted exact-head jobs | R585-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| RTL | CLEAN | `tb/verilator/mbx/Makefile`, the build lists in `ctrl_build.py`, the capture wrapper and recorder exec path, images byte-identical, hosted Verilator and Yosys at the head | R585-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Robustness | UNCLEAN (R585-5-F1) | `ctrl_capture.py`, `ctrl_shim.py` (parse, RECORDER), fail-closed controls, 4 end-to-end capture probes | R585-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Tests | UNCLEAN (R585-5-F1) | Replica self-test (89 + 20 controls), firmware gate dev vs head, mutant tables, coverage self-test and check | R585-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Docs | UNCLEAN (R585-5-F1); RS1 carried | Firmware, gtest, mbx bench and AECP/MAAP READMEs; CI_WORKFLOWS; SUBMODULES; THIRD_PARTY; CONTRIBUTING; QUICKSTART; MAILBOX_SPLIT; module docstrings; PR body | R585-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |

## 7. Real limits

- **No bank, merge candidate or act run.** I ran no manager source bank and no merge candidate; live dev `f88df731` is not validated here. I ran no act, and no `act_ci.py` self-test. The `TRUSTED_SUBMODULES` change was read only.
- **The Verilator path is not mine.** I did not run the standalone gate (no capture given, every known builder including the Verilator ones, about 49 min per the author). So the mailbox bench, the MAAP differential and the AECP wire comparison were not judged by me. The hosted job leaves them out by name, as designed.
- **The MAAP differential did not link here.** The static GoogleTest 1.14.0 libraries come before the harness objects in its link line, which this lane did not change. My log is `receipts/limits/`. Its pin refusal paths passed as controls in the replica.
- **Host toolchain.**
  - CPython 3.14, gcc 16.2.1 and GoogleTest 1.14.0. Its headers were given as a system include through a `g++` wrapper (`scripts/gxx-gtest114`), as the hosted runner has them.
  - Clang 18.1.3 for the stack's gate, through `scripts/clang18-wrapper.sh`.
  - The pinned RV32 SDK, installed from its archive with digest `d42680e9...` and verified.
  - The hosted runner uses gcc 13. Under gcc 16, `srp_mbx.c` measures 515/515, where the ratchet records 514/514. The check compares fractions only, and the dev and head measurements here are identical.
- **Runtime archives.** I built them from local Picolibc, compiler-rt and LiteX sources, without the stack protector, for both trees alike. The images are therefore compared dev against head, not against the author's SRP hashes. The 5 `ctrl_image.py` hashes match the published ones exactly.
- **Replica setup.**
  - The first replica attempt was discarded: an earlier process wrote into its output directory. The receipts come from a clean second run, in a fresh directory, on a clean clone.
  - The replica ran with `--jobs 12` (hosted: 4 for the firmware suite).
- **Hardware.** Physical calibration was NOT RUN. The skipped `Physical gPTP` context is not hardware proof.
- **Clone integrity.** I initialised `third_party/tsn-c-stack` and `third_party/lwSRP` in the review clone at their gitlinks. The tracked blobs, modes and index equal the head tree, `write-tree` is `33de4dc3...`, there are no assume-unchanged or skip-worktree entries, and both submodules are clean at their gitlinks (`receipts/clone_integrity.txt`). The probes ran in disposable clones under `scratch/`, which were restored and are clean.

## 8. Pending manager duties

- Merge-candidate validation on current dev `f88df731` (builder and native banks), with receipts linked on the PR.
- The first act run through the audited-install bootstrap, since this PR changes `scripts/act_ci.py`'s trusted manifest.
- Route R585-5-F1 to the author, and carry R585-5-RS1 to the residue checklist and the PR body.
- Decide on S1 to S3, and on the job-headroom Issue (carried R585-4-S1 / R584-4-S2).

## 9. Reproduce

- `scripts/token_identity.sh DIR_A DIR_B FILE...`
- `scripts/build_images.sh TREE OUT RUNTIME_DIR` (with `MILAN_RV32_CC` set to the pinned SDK compiler)
- `scripts/firmware_unit_replica.sh TREE OUT JOBS`
- `scripts/compare_verdicts.py DEV_LOG HEAD_LOG`
- `scripts/mutant_tables.py TREE_A TREE_B`
- `scripts/docs_gates.sh TREE BASE PYTHON OUT`
- `PROBES="env rsp" scripts/run_capture_probes.sh TREE CAPTURE OUT SCRIPTS_DIR`, and `PROBES=abs PYFLAGS=-I ...` for S1

R585-5 FINISHED
