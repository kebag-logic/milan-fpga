[R584] NEGATIVE - exact head 5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1

# R584-6: internal review of #697 / PR #705, round 6

Internal cleared-context review of lane 697c (executor [A583]) at exact head
`5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1`, tree `8584216aa1952f31eebcdbd33b6acd0f6f080f6a`.
The source base is `8b61b709`; the lane merged dev `aef7ac66` (F5) in `386b8e69`. The lane-only diff is
`aef7ac66..5b4f6fbe`: 69 files, 26 commits.

The verdict is NEGATIVE on one new MINOR, R584-6-F1. The firmware side of the boundary gate does not judge the
saved-state store's sources (`sw/firmware/ctrl_nvm`), yet both linked RV32 images compile them. A real-path
probe in which a store source reaches the stack's `examples/` passes the gate, and the image still builds.

Everything else I checked holds at this head:
- the pin;
- the 32 images I linked, byte-identical between base and head;
- coverage and its denominators;
- the 471 plants, token-identical and all caught;
- the stack-side real-path refusal;
- the round-5 spellings, re-probed on a real path;
- the new `firmware-verilator` job.

The three round-5 MINORs (R584-5-F1, R584-5-F2 and R585-5-F1) are resolved.

## 1. Scope reconstructed

- **Issue #697**, under the owner's repository decision:
  - Comment 6074093506: option (b), a submodule. Acceptance 1 to 6 there replace the in-repo items.
  - Comment 6074191062: the name `tsn-c-stack`.
  - Comment 6074086970: MIT for the stack. The platform's files stay CERN-OHL-W-2.0.
- **Lane assignment 6091228902:**
  - submodule `third_party/tsn-c-stack` at the newest commit whose cores match;
  - `git rm` of the copies;
  - both linked RV32 images byte-identical at every shape;
  - lwSRP pin unchanged;
  - a boundary gate with a planted control, running the stack's own gate and adding the milan-fpga-side direction;
  - every old path updated, with coverage at 100 % and the same denominators, and the same kills;
  - hosted jobs that need the stack check it out, and nothing silently skips;
  - a README note.
- **Issue Goal 2:** "The FPGA firmware (adapters, HAL, composition, image) consumes the stack through its public
  headers only."
- **Pin ruling 6092176555:** the property is token-identical cores plus byte-identical images. The pin is
  `1a9f651c`.

## 2. What was examined and run (this host, the exact head)

Toolchain:
- the pinned RV32 SDK, installed fresh by `scripts/ci_rv32_sdk.py` into scratch and verified;
- GoogleTest and GoogleMock 1.14.0 as system headers;
- Clang 18 and CMake for the stack's own gate;
- the scoped Verilator, which reports `Verilator 5.050 2026-07-01 rev v5.050`;
- host GCC 16.2.1, which is not CI parity.

Receipts are under `logs/`; the scripts are under `scripts/`.

| Check | Result | Receipt |
|---|---|---|
| Pin: token identity of the removed copies (at `aef7ac66`) against the stack at `1a9f651c`, `51870377` and `98dc9e30` | All 7 core files (`adp/acmp/maap .c/.h`, `wire.h`) and `acmp_fake.hpp` are token- and line-identical at `1a9f651c`. `51870377` changes `src/adp.c`, so `1a9f651c` is the newest. The pin is an ancestor of the stack's `main`, and the stack is PUBLIC. | `logs/pin_tokens.log`, `scripts/pin_tokens.py` |
| `firmware-unit` replica, every step under one capture (`scripts/chain_unit.sh`) | All six steps rc 0. `fw_rv32_selftest` passes. The firmware gate prints `tsn-c-stack at 1a9f651c…`, 59 arms `[ok]`, `mutants: 471 of 471 caught`, both lwSRP pin arms `[ok]` and `test_ctrl_firmware: PASS`. The store suites pass. Coverage self-test: `29 of 29`. `firmware coverage: PASS (30 files)`. | `logs/unit.1.log` to `logs/unit.5.log` |
| Boundary step on that capture (`--selftest --without verilator`) | PASS: 51 units (24 also as C++), 26 modes from 23,791 invocations, 948 configurations, 0 findings, 101 boundary and 20 pin controls, 0 misbehaved. This matches the author's figures. | `logs/unit.6.log` |
| `firmware-verilator` replica (`--require-rv32 --selftest --only verilator`) in a second clone | PASS. The bench exits 0. The MAAP differential `--self-test` exits 0. The AECP wire comparison runs at both references. V1 to V3 are caught by name, the 20 pin controls are `[ok]`, and 574 configurations come from 845 invocations. The pin check passes alone. | `logs/ver.1.log`, `logs/ver.2.log` |
| Images: each revision's own fixtures (`ctrl_image.py` at both shapes; `ctrl_srp_image.py` for 5 configs × 1/2 interfaces × plain / `--without-srp` / `--with-aecp`) | 32 of 32 rc 0 at base `aef7ac66` (its own cores) and at head (the submodule). All 32 ELF hashes are equal and all are distinct. Both sides link the same neutral runtime archives (`scripts/rt/`, built with `-fno-stack-protector`). | `logs/img.base.tsv`, `logs/img.head.tsv`, `scripts/images.sh` |
| Mutation tables, base against head | 471 names at both. File (path-mapped to the stack), arm and test are unchanged for every row. Planting each at both revisions gives token-identical programs: 471 of 471, 0 anchor faults. | `logs/mutants.base.tsv`, `logs/mutants.head.tsv`, `logs/plant_equiv.log`, `scripts/plant_equiv.py`, `scripts/mutant_tables.py` |
| Test inventory, base against head | All 385 base GoogleTest cases are defined at head, in `ctrl/test` or the stack's `tests/`. None is lost, and 12 new ones come from the stack. | `logs/test_inventory.log`, `scripts/test_inventory.py` |
| Coverage denominators | The stack's `src/acmp.c` 742/348, `adp.c` 204/95, `maap.c` 209/140 and `wire.h` 10/2 equal base's own copies. The base check at `aef7ac66` passes (30 files). `srp_mbx.c` measures 515/515 on this compiler at base and head; the ratchet's 514 is compared as a fraction (`fw_coverage.py:385-399`). | `logs/base_cov.log`, `logs/unit.5.log` |
| The stack's own suite, as `sw/firmware/ctrl/README.md` documents it (cmake, ctest) | 7 of 7 passed. | `logs/stack_cmake.log`, `logs/stack_ctest.log` |
| Probes: driver spellings, real path, against the replica capture | K0 (dormant plant, no mode) passes. Plain `-D`, `@response`, `-Wp,-D` and `-imacros` each fail by name on host and RV32: `firmware [-DR584_*_MODE]: maap/maap_csr.c includes tsn-c-stack/examples/adp_port.h`. | `logs/probe.K0.log`, `logs/probe.plain.log`, `logs/probe.rsp.log`, `logs/probe.wp.log`, `logs/probe.imacros.log`, `scripts/probe_spellings.sh`, `scripts/r584_probe_builder.py` |
| Probe S1: stack side on a real bump path (a commit in the submodule, staged as the gitlink) | Refused by name on host and RV32: `src/maap.c includes sw/firmware/ctrl/mbx/mbx_hal.h` and `src/acmp.c includes sw/firmware/ctrl_nvm/nvm_state.h`. The stack's own gate refuses too. | `logs/probe.S1.log`, `scripts/probe_more.sh` |
| Probe N1 / N1C / N1B: the saved-state store's sources | N1 (a reach into the stack's `examples/` from `ctrl_nvm/nvm_store.c`) gives **PASS**, rc 0. N1C (the same line also in `ctrl/maap/maap_csr.c`) fails on `maap_csr.c` only. N1B (the N1 plant in place) still links the 1x1 image, rc 0. | `logs/probe.N1.log`, `logs/probe.N1C.log`, `logs/probe.N1B.log`, `scripts/probe_nvm.sh`, `scripts/probe_more.sh` |
| Hosted at the exact head (inspected only) | Successes: `rtl-fast`, `firmware-unit` (job 114344992704, boundary step 93 s, job 31 min), `firmware-verilator` (job 114344992708, step 438 s; its Verilator build was skipped on a cache hit), Verilator shards 0-4, `verilator-suites`, `yosys-portability` and the docs jobs. Skipped: physical gPTP (nightly only). | `logs/hosted_checks.tsv`, `logs/hosted_steps.tsv` |
| Restoration | HEAD `5b4f6fbe`, `git write-tree` = `8584216a`. The worktree and index are clean, and index modes, blobs and paths equal the HEAD tree. All six gitlinks are at their recorded values. Both clones were restored. | `logs/restore.txt` |

Reading done:
- the lane diff `aef7ac66..5b4f6fbe` and its 26 commits;
- `ctrl_build.py` (`stack_gitlink`, `stack_pin`, `legacy_stack`, `source`);
- `ctrl_boundary.py` (both sides, `firmware_units`, `firmware_dirs`, `shadows`);
- `ctrl_image.py` and `ctrl_srp_image.py`;
- `maap_differential.py`, `aecp_wire.py` and `aecp_arms.py`;
- the bench Makefile;
- `act_ci.py` `TRUSTED_SUBMODULES` (`:234-238`) and its selftest arms (`:10734-10758`);
- `ci_scope.py`, `rtl-fast.yml` and `rtl.yml`, with every workflow job's submodule init mapped against what it runs;
- `.gitmodules`, `THIRD_PARTY.md` and `SUBMODULES.md`;
- the `ctrl/README.md` stack section;
- `CI_WORKFLOWS.md`, `MAILBOX_SPLIT.md`, `CONTRIBUTING.md`, `README.md` and `QUICKSTART.md`;
- the SPDX lines of every added and removed file.

## 3. Findings

### R584-6-F1 - MINOR - Conformance, Tests, Docs - the firmware side of the boundary does not judge the saved-state store's sources, which both linked images compile

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_boundary.py:650-654` (`firmware_units`) and `:533-536` (`firmware_dirs`). These take only top-level files of the directories under `sw/firmware/ctrl` and C sources under its `test/`.
  - `sw/firmware/ctrl/test/ctrl_image.py:97,176` and `sw/firmware/ctrl/test/ctrl_srp_image.py:59-60`. Both images compile `ctrl_nvm/nvm_klj2.c`, `nvm_store.c` and `plat/nvm_flash_litespi.c`.
  - `sw/firmware/ctrl/README.md:85`: "It preprocesses every firmware source and header, AECP's included, and every image source".
  - `docs/testing/CI_WORKFLOWS.md:67`: "The firmware reaches only the stack's public headers."
- **Authority:**
  - #697 Goal 2: "The FPGA firmware (adapters, HAL, composition, image) consumes the stack through its public headers only."
  - Lane assignment 6091228902 item 3: "add the milan-fpga-side direction".
  - The PR's own claim of that direction (README:74, 85).
- **Evidence:**
  - Probe N1: `#include "../../../third_party/tsn-c-stack/examples/adp_port.h"` added to `sw/firmware/ctrl_nvm/nvm_store.c`. The boundary gives `ctrl_boundary: PASS`, rc 0 (`logs/probe.N1.log`).
  - Control N1C: the same reach also placed in `sw/firmware/ctrl/maap/maap_csr.c` is refused. Only `maap/maap_csr.c` is named, on host and RV32 (`logs/probe.N1C.log`).
  - N1B: with the N1 plant in place, `ctrl_image.py --shape endstation_ax7101_1x1_tdm8` still links the image, rc 0 (`logs/probe.N1B.log`). The escape is a green build.
  - The stack side does refuse the reverse direction into the store (S1, `src/acmp.c includes sw/firmware/ctrl_nvm/nvm_state.h`). So only the firmware-side direction is open.
  - No prior round raised this.
- **Impact:** a store source linked into both RV32 images can depend on the stack's private layout, through `src/`, `tests/` or `examples/`, and the required gate passes. A later stack bump can then break or silently change the image through files the stack does not publish. The firmware-side direction holds for `sw/firmware/ctrl` only, while README:85 and CI_WORKFLOWS:67 state it for all firmware and image code.
- **Required outcome (one of):**
  - (a) The firmware side judges every source either image builder compiles, and the headers they read. That includes the saved-state store's three sources, at the configurations the store's builders compile them in. A planted control shows a non-public reach from a `ctrl_nvm` source refused by name.
  - (b) A public decision limits the firmware-side direction to `sw/firmware/ctrl`, and README:85 and CI_WORKFLOWS:67 say exactly that.
- **Verification:** rerun `scripts/probe_nvm.sh <packet> <checkout>`. Under (a), N1 must fail by name and the self-test must hold the new control. Under (b), the decision must be linked and the two doc lines must match it.

### R584-6-RS1 - RESIDUE - Docs (PR body only) - stale and duplicated hosted-status sentences

The PR body's Status says "Round 6's hosted figures come after its push". They exist now:
- `firmware-unit` succeeded in 31 min (job 114344992704), its boundary step in 93 s;
- `firmware-verilator` succeeded (job 114344992708), its step in 438 s;
- `rtl-fast`, `verilator-suites` and `yosys-portability` succeeded at `5b4f6fbe`.

Status also states the `92b5be18` hosted result twice: once as "success in 2450 s", then again as "Hosted at `92b5be18`: … 40 min 50 s".

Known limitations repeats one clause: "on a hosted runner at `92b5be18` it took 113 s (job 114282060753); the hosted step took 113 s at `92b5be18` (job 114282060753)".

**Exact fix:**
- Replace "Round 6's hosted figures come after its push." with the four figures above.
- Delete the second `92b5be18` sentence in Status.
- Delete "; the hosted step took 113 s at `92b5be18` (job 114282060753)" in Known limitations.

### Suggestions (optional; no lens effect)

- **R584-6-S1, Docs.** Several tests of this repository include the stack's test fixture `tests/acmp_fake.hpp`, which is not a public header: `acmp_walk.cpp`, and the AECP tests through `aecp_arms.py` and `STACK_TESTS`. The README's stack section says what the firmware may include, but not that this repository's tests use the stack's test fakes. One sentence would let a stack maintainer know that a rename in `tests/` breaks this repository.
- **R584-6-S2, Robustness.** `ctrl_build.stack_pin` (`ctrl_build.py:211-244`) compares blob ids and the symbolic-link bit, but not the executable bit (`100644` against `100755`). This is harmless for C sources. If the scripts it proves are ever executed by path, the mode belongs in the comparison too.
- **Retained:**
  - R584-5-S3: a compiler run from a shell by path is not recorded. It is now a stated limit in the README.
  - R585-2-S2: `aecp_arms.py` takes the submodule's `tests/` under an explicit `--stack`.
  - R584-3-S1 remainder.
- **Retired:**
  - R584-5-S1 (`CI_WORKFLOWS.md` now states the hosted 113 s).
  - R584-5-S2 (`firmware-unit` took 31 of its 45 minutes hosted at this head).

## 4. Prior findings at this head

| Prior finding | State at `5b4f6fbe` | Evidence |
|---|---|---|
| R584-5-F1 (MINOR): modes in `-Wp,`, response files, long options, `-imacros` and precompiled headers are not judged | **Resolved.** My real-path probes caught `@response`, `-Wp,-D` and `-imacros` by name on host and RV32. The plain `-D` positive control was caught too, and the dormant K0 passed. The self-test holds standing controls for `-Wp`, `-Xpreprocessor`, both `--define-macro` forms, the response file, `-imacros` and the PCH, plus three refusal cases, all `[ok]`. | `logs/probe.rsp.log`, `logs/probe.wp.log`, `logs/probe.imacros.log`, `logs/probe.plain.log`, `logs/probe.K0.log`; `logs/unit.6.log` lines 111-121 |
| R585-5-F1 (MINOR): a `-D` inside an `@response` file escapes | **Resolved**, as above (`logs/probe.rsp.log`). | same |
| R584-5-F2 (MINOR): Verilator-only configurations are judged by no required job | **Resolved.** `firmware-verilator` is in the `rtl-fast` aggregate's `needs` and result list (`.github/workflows/rtl-fast.yml:319-379,386,397,407`). It succeeded hosted at this head and ran its boundary step for 438 s. My replica passes with V1 to V3 caught by name. | `logs/ver.1.log`, `logs/hosted_steps.tsv` |
| R584-5-RS1, R585-5-RS1 (PR body) | Applied for round 5. The round-6 status lines carry R584-6-RS1. | PR body |
| R584-1 to R584-4 and R585-1 to R585-4 MINORs (pin on the differential and the bench, `run-if2`, the shapes and C++ judgement, named and computed C++ sources, make-computed `-D`) | **Remain resolved.** The 20 pin controls are `[ok]` in both of my replicas (every bench target on a poisoned `wire.h`, both differential modes, the three AECP tools). All 101 boundary controls are `[ok]`. | `logs/unit.6.log`, `logs/ver.1.log` |
| R585-3-F1 (MAJOR): boundary step timed out | **Remains resolved.** The hosted boundary step took 93 s at this head, and the job took 31 of its 45 minutes. | `logs/hosted_steps.tsv` |

## 5. Lens results

```text
[R584] MINOR Conformance — sw/firmware/ctrl/test/ctrl_boundary.py:650-654; sw/firmware/ctrl/README.md:85 — R584-6-F1: the firmware-side direction (lane item 3, #697 Goal 2) does not cover the store sources both images link. Otherwise checked against #697 acceptance 1-6 (6074093506), 6091228902 and 6092176555: pin 1a9f651c token-identical and newest (logs/pin_tokens.log); copies removed (git diff --stat aef7ac66..5b4f6fbe); lwSRP gitlink 9197193e unchanged; .gitmodules and act_ci.py TRUSTED_SUBMODULES (:234-238) with four refusal arms (:10734-10758); 32/32 images byte-identical (logs/img.*.tsv); 471 plants equal and caught (logs/plant_equiv.log, logs/unit.2.log); coverage 100 % with equal denominators (logs/unit.5.log, logs/base_cov.log); README stack section (sw/firmware/ctrl/README.md:56-187); stack PUBLIC, MIT, its README naming lwSRP under Apache-2.0; platform SPDX lines unchanged.
[R584] PASS RTL — git diff aef7ac66..5b4f6fbe -- hdl '*.sv' '*.v' '*.svh' (0 files); tb/verilator/mbx/Makefile:43-115 (FW_SRC/FW_INC from the stack's src/ and include/, stack-pin an order-only prerequisite of obj_fw/libctrlfw.a, run-cosim and run-if2) — checked against the bench run in logs/ver.1.log (make -C tb/verilator/mbx exit 0) and its six poisoned-wire.h pin controls [ok]; sw/firmware/ctrl/test/maap_differential.py:23-41 links the stack's maap.c into the Verilated KL_maap differential (its --self-test exit 0 in logs/ver.1.log); no fabric module or interface contract changes.
[R584] PASS Robustness — sw/firmware/ctrl/test/ctrl_build.py:177-244 (stack_gitlink, stack_pin: blob hashes read from the files, added files refused, index never read) and the capture's fail-closed paths — checked by the 20 pin controls and the missing, empty and dropped-builder capture controls [ok] (logs/unit.6.log), the real-path stack-bump probe S1 refused by name on host and RV32 (logs/probe.S1.log), the four driver-spelling probes caught (logs/probe.*.log), and an off-pin edit refused by the bench, the differential and the AECP tools (logs/ver.1.log). R584-6-F1 is filed under the lenses above, not here.
[R584] MINOR Tests — sw/firmware/ctrl/test/ctrl_boundary.py:650-654; sw/firmware/ctrl/test/ctrl_plants.py (no ctrl_nvm control) — R584-6-F1: no control plants a non-public reach from a store source, and the gate passes one (logs/probe.N1.log). Otherwise checked: 101 boundary and 20 pin controls [ok]; my K0 and N1C controls behave; 59 arms, 471/471 mutants and the AECP, SRP and lwSRP campaigns PASS (logs/unit.2.log); 385/385 base tests present at head (logs/test_inventory.log); coverage self-test 29/29 (logs/unit.4.log).
[R584] MINOR Docs — sw/firmware/ctrl/README.md:85; docs/testing/CI_WORKFLOWS.md:67 — R584-6-F1: both state the firmware and image direction for code the gate does not judge. Otherwise checked: sw/firmware/ctrl/README.md:56-187 (contents, must-not-depend list, how to run the stack's suite — run here, 7/7 — and MIT inside CERN-OHL-W-2.0); CI_WORKFLOWS.md firmware-unit and firmware-verilator paragraphs against hosted jobs 114344992704 and 114344992708; SUBMODULES.md, THIRD_PARTY.md:21, CONTRIBUTING.md:383-392, QUICKSTART.md:157-162 and MAILBOX_SPLIT.md links pinned at 1a9f651c. PR body: R584-6-RS1 (residue).
```

## 6. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R584-6-F1) | #697 acceptance and owner and lane comments; pin token proof; images; plants; coverage; licences; act manifest | R584-6 | `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` |
| RTL | CLEAN | no HDL in the lane diff; `tb/verilator/mbx/Makefile:43-115`; MAAP differential and bench builds under the Verilator replica | R584-6 | `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` |
| Robustness | CLEAN | `ctrl_build.py:177-244`; capture fail-closed controls; probes S1, K0, plain, rsp, wp, imacros | R584-6 | `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` |
| Tests | UNCLEAN (R584-6-F1) | firmware gate, coverage and boundary replicas; Verilator replica; plant equivalence; test inventory; probes N1, N1C, N1B | R584-6 | `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` |
| Docs | UNCLEAN (R584-6-F1) | `ctrl/README.md` stack section; `CI_WORKFLOWS.md`; `SUBMODULES.md`; `THIRD_PARTY.md`; `CONTRIBUTING.md`; `README.md`; `QUICKSTART.md`; `MAILBOX_SPLIT.md`; PR body (RS1, residue only) | R584-6 | `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` |

## 7. Real limits

- **Not CI parity:**
  - This host's GCC 16.2.1 and CPython measured coverage. `srp_mbx.c` reads 515 lines here, against the ratchet's 514 for the runner's GCC 13; both are 100 %.
  - GoogleTest 1.14.0 entered as a system include directory, as the runner's `/usr/include` copy does. A first attempt with it as a plain `-I` was refused by GCC 16's `-Werror` inside GoogleTest's own templates. That was an environment fault, rerun as described (`logs/attempt1/`).
- **The image runtime archives are my own minimal ones** (`scripts/rt/`), not `ctrl_image_runtime.py`'s Picolibc and compiler-rt builds. Identity is shown for the same archives on both sides, which is the property. 32 images were linked, against the author's 35. Mine are every shipped config × 1/2 interfaces × three compositions, plus both `ctrl_image` shapes.
- **External termination:** the first `--only verilator` replica was terminated by a SIGTERM from outside this round (rc 143, `logs/attempt2/`), while another review ran on the same shared host. The rerun with a private `TMPDIR` passed.
- **Not run:**
  - act and the host `act_ci.py --selftest`, which this round does not allow;
  - the full parent, PP, gPTP, Yosys and builder banks;
  - the docs job's command list;
  - `ci_events.py`.
- **No physical calibration or hardware.** Field skips are not hardware proof.
- **No manager source bank exists at this head, and none is claimed.**
- **The current-dev candidate was not built.** Live dev `ac2c5e77` adds 24 files over `aef7ac66` (litex, syn, docs, tb); none of them is a file this lane changes.

## 8. Pending manager duties

- Build and validate the current-dev merge candidate (dev `ac2c5e77`), with the builder and native banks, and link the receipts.
- Run act through the audited-install bootstrap for the new `third_party/tsn-c-stack` manifest entry.
- Own hosted and act acceptance.
- Carry R584-6-RS1 to the residue checklist.
- Route R584-6-F1 to the executor, or record decision (b).

R584-6 FINISHED
