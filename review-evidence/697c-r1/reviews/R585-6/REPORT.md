[R585] NEGATIVE - exact head 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1

# R585-6: external review of PR #705 (issue #697, lane 697c)

Exact head `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1`, tree `8584216aa1952f31eebcdbd33b6acd0f6f080f6a`.
The PR delta is judged against dev `aef7ac66605c4404900ce04cbaaeff88e41bb880`, the dev merged into the
lane at `386b8e69`. The source base is `8b61b70902f3ebf118e56967277e2686731081bd`. Live dev `ac2c5e77`
was not judged: the current-dev candidate is the manager's.

Scope, from the issue: #697 acceptance 1-5, as replaced for the repository case by owner decision
6074093506 (items 2-5), the name ruling 6074191062, the pin ruling 6092176555 (token-identical cores and
byte-identical images, not byte-identical files), the lane assignment 6091228902, the merge-dev order
6093389868 (AECP stays in milan-fpga) and the round-6 assignment 6102039501.

## Verdict

NEGATIVE on two MINORs (F1, F2), both scope gaps in the boundary gate. Neither is a live violation.
Each lets a planted defect through the required gate while its documents say it is caught.

Every acceptance measurement holds at this head, and I reproduced each one independently:

- the cores are token-identical to dev's copies at the pin, and differ at the next stack commit;
- all 35 linked RV32 images are byte-identical to dev;
- the coverage table is unchanged;
- the same 471 plants are caught, and every planted file is token-identical to dev's;
- the gate passes in both hosted forms, with all its controls.

## Findings

### F1 - MINOR - Tests, Robustness, Docs - the firmware-side boundary does not judge the image's `ctrl_nvm` sources

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_boundary.py:650-654`: `firmware_units` takes its units from the
    directories under `sw/firmware/ctrl` and from `test/*.c`. They are judged at
    `ctrl_boundary.py:789-793`.
  - `sw/firmware/ctrl/test/ctrl_image.py:97,176`: every measured image compiles `NVM_SOURCES`
    (`nvm_klj2.c`, `nvm_store.c`, `plat/nvm_flash_litespi.c`).
  - `ctrl_srp_image.py:59`: the `--with-aecp` image compiles `ctrl_nvm` sources too.
- **What the documents claim:**
  - `docs/testing/CI_WORKFLOWS.md:67`: "The firmware reaches only the stack's public headers."
  - The PR body's Description, Boundary row: "the firmware and image code reach only the stack's
    `include/`".
  - `sw/firmware/ctrl/README.md:85`: "every image source".
- **Authority:**
  - #697 Goal: "The FPGA firmware (adapters, HAL, composition, image) consumes the stack through its
    public headers only".
  - Lane assignment 6091228902 item 3: add the milan-fpga-side direction.
- **Evidence:** probe Q5 (`scripts/boundary_probes.sh`, `receipts/boundary_probes.txt`,
  `receipts/probe_Q5.log`).
  - The plant gives `sw/firmware/ctrl_nvm/nvm_store.c` the line
    `#include "../../../third_party/tsn-c-stack/examples/rv32/include/string.h"`, a stack file
    outside `include/`.
  - The gate's own `ctrl_image.py` run compiled it into the image (`exit 0`).
  - Judged against my capture of the hosted firmware steps, the gate printed `0 finding(s)` and
    `ctrl_boundary: PASS`.
  - The same include is refused by name in `sw/firmware/ctrl/srp/srp_mbx.c` (Q3), and through a
    symbolic link in `sw/firmware/ctrl/adp` (Q2). So the gap is the unit list, not the path handling.
  - No `ctrl_nvm` file includes a stack file at this head (`git grep`).
- **Impact:**
  - Code linked into the measured RV32 images can come to depend on the stack's sources, tests or
    examples while the required gate stays green.
  - Two authoritative texts say the firmware is held to the public headers.
  - The units are listed by directory. They are not taken from what the recorded compiles compile.
- **Required outcome**, one of:
  - Judge on the firmware side every source and header that a recorded firmware or image compile
    compiles, outside the stack and the test equipment. That includes the `ctrl_nvm` sources. Add a
    standing control like Q5, refused by name.
  - Or state in the CI page, the PR body and the README that the firmware side judges
    `sw/firmware/ctrl` only, and name the image's `ctrl_nvm` sources as outside it, with the reason.
- **Verification:** rerun Q5 against a capture of the firmware steps. It must be refused by name, or
  the narrowed texts must match `firmware_units`.

### F2 - MINOR - Conformance, Robustness, Tests, Docs - the stack side is judged on a fixed include path, not each compile's, so a builder-only directory can stand in for a C library header

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_boundary.py:589-610`: `stack_side` preprocesses the stack's sources
    and headers with `search(trees, work)`.
  - `ctrl_boundary.py:539-543`: `search` is a fixed path: `ctrl_build.includes` plus the
    `sw/firmware/ctrl` directories.
  - `sw/firmware/ctrl/test/ctrl_image.py:157-161,185`: the image builder compiles every source,
    including the stack's `src/*.c`, with `-I` for the shape's generated headers, `ctrl_nvm`,
    `ctrl_nvm/plat` and `ctrl_nvm/test/rv32`. These come before the compiler's own `-isystem`
    headers.
  - The expansion's search directories are used only to follow C++ sources (`ctrl_configs.py:708-745`,
    `ctrl_boundary.py:676-720`).
- **What the documents claim:**
  - The PR body's Status says "each recorded compile's modes, search path and files read first are the
    compiler's own expansion of its arguments".
  - `sw/firmware/ctrl/README.md` says "Every unit is judged as its builders compile it".
  - The gate's docstring section is titled "AS ITS BUILDERS COMPILE IT".
- **Authority:**
  - #697 acceptance 2: "A gate refuses any include from the stack into the mailbox, platform,
    register-map or image code."
  - Round-6 assignment 6102039501 item 1: take "the include search path and the files read first from
    the compiler's own expansion".
- **Evidence:** probe Q7 (`scripts/boundary_probes2.sh`, `receipts/boundary_probes2.txt`,
  `receipts/probe_Q7.log`, `receipts/probe_Q7_image_deps.txt`).
  - The plant adds `sw/firmware/ctrl_nvm/plat/stdbool.h`, a platform header named like the C library
    header that `adp.h`, `acmp.h` and `maap.h` include.
  - Under the image builder's own flags and include path, `-M` shows that the stack's `src/adp.c` and
    `src/maap.c` read `sw/firmware/ctrl_nvm/plat/stdbool.h`.
  - The gate prints `0 finding(s)` and `ctrl_boundary: PASS`.
  - Comparison Q8 puts the same file in `sw/firmware/ctrl_nvm/`, which is on the gate's fixed path. It
    is refused with 19 findings ("the stack's tests/acmp_fake.hpp includes
    sw/firmware/ctrl_nvm/stdbool.h"). The earlier Q4 in `sw/firmware/ctrl/port/` is refused too ("the
    stack's src/adp.c includes sw/firmware/ctrl/port/stdbool.h").
  - The clean controls Q1, Q6 and Q9 pass.
- **Impact:** a platform header in a directory that only a builder searches can replace a C library
  header for the stack's sources. The stack, as linked into the measured image, then depends on milan
  platform code (acceptance 2's direction), and the required gate passes.
- **Required outcome:**
  - Judge each stack unit, and each firmware unit, on the include search path that each recorded
    invocation compiling it reports, or on every directory any such invocation searched.
  - Refuse any header resolved to a file outside the stack's public headers and the C
    implementation's headers.
  - Add a standing control like Q7, refused by name.
- **Verification:** rerun `scripts/boundary_probes2.sh`. Q7 must be refused by name, and Q9 must pass.

### S1 - SUGGESTION - Docs - the CI page can now cite the hosted figures

`docs/testing/CI_WORKFLOWS.md:101` ends "a hosted run gives the figure that counts". At this head the
hosted figures are:

- the `firmware-verilator` step: 438 s (job 114344992708); the whole job took 473 s, 20% of its 40 min;
- the `firmware-unit` boundary step: 93 s (job 114344992704).

This is optional. The manager owns the hosted report.

### RS1 - RESIDUE - PR body - two duplicated sentences

This affects the PR body only. It is wording, and no figure changes. Exact fix:

1. In Status, delete the sentence "Hosted at `92b5be18`: `rtl-fast` success; `firmware-unit` passed
   in 40 min 50 s of its 45 (job 114282060753), its boundary step in 113 s, with the store suites and
   the coverage ratchet run." The "Hosted checks at `92b5be18`" sentence before it already says this
   (2450 s = 40 min 50 s).
2. In Known limitations, in the boundary self-test bullet, delete "; the hosted step took 113 s at
   `92b5be18` (job 114282060753)". It repeats the clause before it.

## Lens results

```text
[R585] PASS RTL — git diff aef7ac66..5b4f6fbe -- hdl syn configs sw/mailbox tb/common is empty; sw/firmware/ctrl/test/ctrl_build.py:59-62 PORTABLE keeps the link order with stack paths; tb/verilator/mbx/Makefile:40-115; receipts/D_boundary_standalone.log (make -C tb/verilator/mbx exit 0, maap_differential.py --self-test exit 0, aecp_wire.py --every exit 0); hosted verilator-suites success at the head — no HDL, register-map or mailbox-contract change; the firmware's interface to the fabric is unchanged: byte-identical images, and the bench and the MAAP differential pass against the stack's cores
```

Conformance, Tests, Robustness and Docs are UNCLEAN: F1 covers Tests, Robustness and Docs, and F2
covers all four. The clean evidence under each lens:

- **Conformance:**
  - Cores: token-identical at `1a9f651c` (7 of 7 files), and different at `51870377`
    (`receipts/core_tokens_pin.txt`, `receipts/core_tokens_next.txt`).
  - Images: 35 of 35 byte-identical to dev `aef7ac66`, with a planted-stack control that changes the
    hash (`receipts/images_base.sha256`, `receipts/images_head.sha256`,
    `receipts/image_sensitivity_control.txt`). `ctrl_image.py --base aef7ac66` gives `+0` in every
    section (`receipts/ctrl_image_base_delta.log`).
  - Gitlinks: lwSRP `9197193e` and every other gitlink are unchanged.
  - Coverage: per file, the hosted coverage tables at dev and at the head are identical apart from the
    paths (30 files, 100%). That includes the stack's `src/adp.c` at 204/206 and 95/102 with the same
    exclusions. `srp_mbx.c` is 514/514 on both.
  - Plants: the same 471 are caught.
  - Tests: no core test case is lost (108 to 119, `receipts/test_inventory.txt`).
  - README: it says what the stack provides, what it must not depend on, how to run its tests, and its
    MIT licence (`sw/firmware/ctrl/README.md:56-187`). The stack suite commands work
    (`receipts/stack_own_suite.log`, 7 of 7).
  - Licences: every remaining file keeps CERN-OHL-W-2.0, and the stack is MIT.
- **Tests:**
  - `receipts/E_fw_steps_captured.log` runs the hosted firmware steps under capture: `mutants: 471 of
    471 caught`, `test_ctrl_firmware: PASS`, coverage self-test 29 of 29, and `firmware coverage: PASS
    (30 files)`.
  - `receipts/plant_tokens_compare.txt`: all 471 planted files are token-identical to dev's, and 311
    now plant into the stack.
  - `receipts/hosted_mutant_counts_dev_vs_head.txt`: the plant set is the same, and no plant's
    failing-check count is lower (24 higher, 447 equal).
  - `receipts/hosted_gate_verdicts_dev_vs_head.diff`: only those counts and the first-failure names
    differ.
  - `receipts/F_boundary_hosted_form.log` (the hosted form): 101 boundary and 20 pin controls, 0
    misbehaved, 948 configurations. This matches hosted job 114344992704 exactly.
  - `receipts/D_boundary_standalone.log` (standalone): 105 and 20 controls, with V1 to V3 caught by
    name.
- **Robustness:**
  - `receipts/pin_probes.txt`: refused are an added source, a CRLF header, `include/` swapped for a
    symlink, an edit hidden with skip-worktree, and build junk under `tests/`. Accepted, and harmless,
    are a docs edit, a mode bit and an empty directory.
  - `receipts/pin_probe_uninitialised.txt`: an uninitialised stack is refused by name.
  - The boundary probes Q2, Q3, Q4 and Q8 are refused by name.
- **Docs:**
  - `scripts/docs_check.py`: 0 findings over 202 Markdown files. `scripts/check_submodule_docs.py`: OK
    (6 gitlinks). The diagram's `--check` and `--selftest`: OK.
  - `scripts/ci_events.py --check`: OK (1848 items). Its `--selftest`: PASS (2530 arms).
    `scripts/ci_scope.py --selftest`: PASS.
  - No stale reference to the removed paths remains (`git grep`). The one exception is the intended
    `LEGACY` map at `ctrl_build.py:247-249`.
  - The README's control counts (1 base + 95 + 5 = 101, plus 4 on the Verilator side) and the gtest
    README's test counts (adp 34, acmp 91) match the runs.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issue acceptance and rulings; token, image, coverage, mutation, inventory and licence receipts; probe Q7 | R585-6 | 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1 |
| RTL | CLEAN | empty HDL/contract delta; PORTABLE order; mbx Makefile; bench, MAAP differential and AECP wire runs | R585-6 | 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1 |
| Robustness | UNCLEAN (F1, F2) | pin probes, uninitialised probe, boundary probes Q1-Q9 | R585-6 | 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1 |
| Tests | UNCLEAN (F1, F2) | captured firmware steps, plant token digests, hosted verdict diff, both boundary forms, stack suite | R585-6 | 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1 |
| Docs | UNCLEAN (F1, F2) | ctrl README, gtest README, CI page, SUBMODULES, THIRD_PARTY, CONTRIBUTING, QUICKSTART, README, mbx README, aecp README, PR body; docs gates | R585-6 | 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1 |

## Prior public findings, rounds 1 to 5, at this head

I read these only after the verdict and ledger above were written. I did not read the concurrent
internal round-6 report.

| Finding | State at this head | Evidence |
|---|---|---|
| R584-1-F1 = R585-1-F2 (gates building an unpinned stack) | Resolved | 20 pin controls `[ok]` in the hosted step and locally; `receipts/pin_probes.txt` |
| R584-1-S1, R585-1-S1 (pin trusts `git status`; scripts not covered) | Resolved | `ctrl_build.py:188-240` hashes files and never reads the index; my skip-worktree probe is refused |
| R584-1-S2 (stack tests outside the boundary) | Resolved | `tests_side`; Q8 is refused through `tests/acmp_fake.hpp` |
| R585-1-F1, R584-2-F1, R585-2-F1 (single configuration; shapes; C++) | Resolved | 948 configurations, 24 units also as C++; hosted controls `[ok]` |
| R584-2-F2 = R585-2-F2 (`run-if2` unpinned) | Resolved | `tb/verilator/mbx/Makefile:115` (`run-if2: if2-gen \| stack-pin`); poisoned-`wire.h` controls `[ok]` for all, run-cosim, run-if2, the library and stack-pin |
| R584-2-S1 = R585-2-S1, R585-3-S1, R585-4-F1, R584-4-F2 (mode spellings in builder text) | Resolved by construction | modes come from the compiler's expansion of the captured invocation |
| R584-3-F1, R585-3-S2, R584-4-F1 (C++ sources not followed or computed) | Resolved | hosted controls `[ok]`; 253 C++ sources followed standalone |
| R585-3-F1 (MAJOR, hosted timeout) | Resolved and holding | `firmware-unit` green in 1861 s of 2700 at this head; boundary step 93 s of 300 |
| R584-5-F1 (GCC driver spellings and a file read first) | Resolved for modes | controls `[ok]` in hosted job 114344992704: `-Wp,`, `-Xpreprocessor`, `--define-macro=`, `--define-macro NAME`, `-imacros`, a precompiled header and a response file. The include-path part of the round-6 item is not met for C units; see F2 |
| R584-5-F2 (Verilator-only configurations in no required job) | Resolved | required `firmware-verilator` in the `rtl-fast` aggregate; green at this head (step 438 s, job 114344992708); V1 to V3 caught by name |
| R585-5-F1 (response file `@FILE`) | Resolved | three response-file controls `[ok]` |
| R585-5-S1, R584-5-S3 (compilers run by path, unseen) | Resolved as a stated limit | `sw/firmware/ctrl/README.md:114` |
| R585-5-S2 (silent header cap) | Resolved | `ctrl_shim.py:68,79`: 1024, exit 2 |
| R585-5-S3, R584-5-S1, R584-4-S1, R585-4-S2 (hosted figure in CI page) | Applied for `92b5be18`; the new head's figure is S1 above | `CI_WORKFLOWS.md:79-82` |
| R585-4-S1 = R584-4-S2 = R584-5-S2 (`firmware-unit` headroom) | Carried; the manager's separate issue | 1861 s of 2700 at this head |
| R584-3-S1 (remaining parts: `FORCED` named as a constant; a pin recipe ignoring its exit status) | Retained, SUGGESTION, optional | not addressed |
| R585-2-S2 (explicit `--stack` while the AECP tests take the submodule's `tests/`) | Retained, SUGGESTION, optional | `aecp_arms.py:83,144` |
| R585-1-R1 to R5, R584-2-R1, R585-2-RS1 to RS3, R585-3-RS1, R584-4-RS1, R585-4-RS1 | Applied or superseded | PR body at review time |
| R584-5-RS1, R585-5-RS1 (round-5 hosted status) | Applied for round 5; the round-6 hosted lines are the manager's report | PR body Status |

## Executed evidence (local, this round)

- Toolchain:
  - pinned RV32 SDK, freshly installed and verified (`scripts/ci_rv32_sdk.py`, archive sha256
    `d42680e9...`);
  - GoogleTest and GoogleMock 1.14.0 as system headers;
  - Verilator 5.050, identity checked (`verilator --version`);
  - host gcc 16.2 and CPython 3.14.
- Campaigns:
  - the hosted firmware steps under `ctrl_capture.py`: rc 0, 2835 s;
  - the boundary in the hosted form against that capture: rc 0, 132 s under a host load of about 30
    to 60;
  - the standalone boundary self-test with every builder: rc 0, 3390 s;
  - coverage `--selftest` and `--check`: rc 0.
- Image comparison: `scripts/images.sh` links all 35 images at the extracted dev tree and at the head,
  with one runtime pair (`scripts/runtime.sh`: picolibc 1.8.10, compiler-rt and LiteX sources, built
  with the builder's flags plus `-fno-stack-protector`).
- Restoration: `receipts/restore_verification.txt`.
  - The index tree equals the head tree.
  - Every tracked blob hashes to its id, and the modes match.
  - The submodules are at their gitlinks and clean.
  - The bench's ignored build outputs are removed.

## Real limits

- This is a source-head review. No manager source bank or current-dev candidate exists at this head,
  and none is claimed.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The hosted Physical gPTP context is `skipped` at this head, as on any PR.
- Local runs used the host's gcc 16 and CPython 3.14, not the CI-parity Ubuntu 24.04 image.
  - Under gcc 16, `srp_mbx.c` measures 515/515 lines. CI measures 514/514 at dev and at the head. The
    ratchet compares fractions.
  - The standalone run derives 48 build modes. The hosted runs derive 26 and 28.
  - The hosted-form judgement of my capture matched the hosted job exactly.
- The image runtime archives are built from public sources I chose (picolibc 1.8.10, compiler-rt and
  LiteX master), not from an archived pin. Both sides used the same archives, so the comparison is
  relative.
- I did not run the `--only verilator` form separately. The standalone run covered those builders and
  V1 to V3, and the hosted job 114344992708 ran that form green.
- Not run, by rule: act and `act_ci.py --selftest`, and Docker.
- One base-tree coverage attempt was refused because an extracted tree has no git metadata. It was
  dropped; the hosted dev table stands in for it.
- At the start of the round I stopped my own aborted run with a command-line pattern match. Only my
  own shell is known to have been hit. Afterwards, another lane's processes that did not carry the
  pattern were still running. Every later stop was by recorded process id.

## Pending manager duties

- Hosted and act acceptance at the merge turn. That includes the audited-install bootstrap for the
  new `third_party/tsn-c-stack` trusted-submodule entry, since act has not run on this PR.
- The current-dev candidate on live dev `ac2c5e77`: builder and native banks, image hashes against
  the candidate's dev.
- The round-6 hosted figures in the PR body (S1, RS1).
- The `firmware-unit` headroom issue, which is carried.

R585-6 FINISHED
