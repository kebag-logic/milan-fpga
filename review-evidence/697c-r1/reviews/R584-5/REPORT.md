[R584] NEGATIVE - exact head 92b5be18817659c1c9903a0544450d29ca7ab3fd

# R584-5: internal review of #697 / PR #705, round 5

Exact head `92b5be18817659c1c9903a0544450d29ca7ab3fd`, tree `33de4dc3c3be34efea3d50128211bd14a72ac510`, source base `8b61b70902f3ebf118e56967277e2686731081bd` (merged dev `aef7ac66`).
Cleared-context internal review in an isolated detached clone, all five lenses applied.

**Verdict: NEGATIVE.** Two MINOR findings are open: R584-5-F1 and R584-5-F2.
Both are in the boundary gate's round-5 capture.
Everything the issue's acceptance measures holds at this head, and I reproduced it on this host:
- the pin;
- byte-identical images;
- identical coverage;
- identical plants, all caught.

All three MINORs open at `e07b3054` are resolved.

## 1. Scope reconstructed

- **Issue #697 acceptance 1 to 5, under the owner's repository decision.** The relevant comments are 6074093506 (option (b): a submodule), 6074191062 (named `tsn-c-stack`) and 6074086970 (MIT).
- **Lane 697c assignment (6091228902):**
  - submodule at `third_party/tsn-c-stack`, pinned at the newest commit whose cores match;
  - `git rm` of the copies, with the images byte-identical;
  - lwSRP pin unchanged;
  - a boundary gate in both directions, with planted controls;
  - every reference updated, with coverage at 100 % on the same denominator and every campaign keeping its kills;
  - a README note.
- **Pin ruling (6092176555).** The property is token-identical cores plus byte-identical images. The pin is `1a9f651c`.
- **Rounds 2 to 5 (6092628778, 6093389868, 6094873968, 6096148471, 6097800045).** These made the boundary judge every configuration the builders compile in, and pinned every gate that builds the stack. They kept the step within 5 minutes without dropping configurations or leaving the required job.
- **Round 5.** The gate judges the builders' actual compiler invocations, recorded by a capture, by construction. It fails closed on a missing or empty capture, or one missing a known builder.

## 2. What was examined and run (this host, the exact head)

The firmware gates ran on the host with gcc 16.2.1, CPython 3.14 and the pinned GoogleTest 1.14.0 prefix (as system headers). The RV32 builds used the pinned RV32 SDK. Verilator was the pinned 5.050 (`verilator --version` gives 5.050, rev v5.050).

| Check | Result | Receipt |
|---|---|---|
| Cores at the pin, token by token against dev's copies (comments stripped by the preprocessor) | All 7 files (`adp/acmp/maap .c/.h`, `wire.h`) TOKEN-IDENTICAL at `1a9f651c` against both `8b61b709` and `aef7ac66`. The next stack commit, `51870377`, changes `src/adp.c`. So `1a9f651c` is the newest such pin. | `receipts/core_tokens.txt`, `scripts/core_tokens.sh` |
| lwSRP gitlink | `9197193e` at base, dev and head | `receipts/verify_tree.txt` |
| `ctrl_image.py`, 5 shipped shapes, head against dev `aef7ac66`, each built by its own revision's tool in its own checkout | 5 of 5 ELF hashes identical. The core objects are identical by content and differ only in name (`src_adp.o` and `adp_adp.o`). | `receipts/images/` |
| `ctrl_srp_image.py`, 5 shapes x 1/2 interfaces x without-SRP/SRP/AECP (30 fixtures), head against dev, empty runtime archives so each stops at its link | 730 object hashes, in link order, identical. The link inputs are equal, so the linked images are equal for any runtime. | `receipts/images/srp-objects-*.txt`, `receipts/images/srp-objects.diff` (empty), `scripts/srp_objects.sh` |
| Mutation tables (`ctrl_mutants.MUTANTS`, `aecp_mutants.DEFECTS`) | 471 + 74 plants, identical to dev by name, file and killing test | `receipts/mutants-*.tsv`, `receipts/mutants.diff` (empty) |
| Test cases, dev's firmware tests against the head's plus the stack's at the pin | All 415 dev cases are present, and 12 stack-only cases are added | `receipts/test_names.txt` |
| The hosted `firmware-unit` firmware steps, each under `ctrl_capture.py` (control gate as two `--mutation-shard`s) | All exit 0. Per shard: 59 arms. Control 236 + 235 = 471 of 471, AECP 37 + 37 = 74, SRP 169 and 68, lwSRP pin 2/2, no verdict other than `[ok]`. Store gate PASS. RV32 self-test 17 PASS. Coverage self-test 29 of 29, `--check` PASS on 30 files. | `receipts/capture/` |
| Coverage, dev against head, same toolchain | All 30 rows identical. Head's ratchet row `srp_mbx.c 514/514` (dev 515/515) is the hosted gcc 13.3 measurement: dev's own hosted run (job 114089603191) and the head's (job 114282060753) both print 514/514. The row was refreshed, not changed. | `receipts/coverage_compare.txt`, `receipts/coverage-*.log`, `receipts/hosted_evidence.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --capture ... --without verilator` (the hosted command) on that capture | PASS: 22 build modes, 942 configurations, 0 findings, 89 boundary and 20 pin controls, 0 misbehaved, 126 s on a loaded host | `receipts/gate/ctrl_boundary-hosted-mode.*` |
| Reviewer probes through the gate's own `planted` / `control_capture` / `judge` | K0 harness control CAUGHT. V1 to V3 and F1 to F7 ESCAPED (section 3). | `scripts/boundary_probes.py`, `receipts/gate/probes-*.log` |
| `aecp_wire.py --interfaces 1` under a capture | PASS, 142 observations. Records `-DPP_TOP_TIM_DEFAULTS`, `-DAECP_WIRE_INTERFACES=1` and Verilator's `-DVERILATOR=1`/`-DVM_*`. | `receipts/capture/aecp_wire-if1.*` |
| Hosted, exact head (read-only) | Runs 38075657991/65/68/53 have `head_sha` 92b5be18 and are all success; Physical gPTP is SKIPPED (not hardware proof). `firmware-unit` 40 min 50 s; boundary step 11 113 s; three `LEFT OUT` lines; 22 build modes. | `receipts/hosted_evidence.txt` |
| No HDL change | `git diff aef7ac66..HEAD -- '*.sv' '*.v' '*.svh' hdl/` is empty | this report |
| Restore | 1271 tracked entries hash to HEAD by bytes and mode, and the index equals HEAD. 5 gitlinks are at their pins. `ctrl_build.py --stack-pin` passes. Nothing untracked or ignored remains. | `receipts/verify_tree.txt`, `scripts/verify_tree.py` |

## 3. Findings

### R584-5-F1 - MINOR - Conformance, Robustness, Tests, Docs - the capture reads a mode only in the `-D`/`-U` spellings: five GCC driver spellings and a file read first define macros the boundary never judges

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_shim.py:48-49,88-101` (`parse`, and the recorder's copy of the option list at `:307`);
  - `sw/firmware/ctrl/test/ctrl_configs.py:83` (`FORCED`, one named header);
  - `sw/firmware/ctrl/README.md:111-112`;
  - `ctrl_boundary.py:63-64`.
- **Authority:**
  - Round 5 item 1 says the recorder records "every `-D`, `-U` and `-I` argument" and the gate "judges exactly the recorded invocations", closing the class by construction.
  - README:111-112 says the build modes are every `-D` and `-U` flag "exactly as the compiler was given it ... So a mode is judged whatever form its builder writes it in".
- **Evidence:**
  - gcc defines the macro for each of these: `-Wp,-DX`, `-Xpreprocessor -DX`, `--define-macro=X`, `--define-macro X`, a response file `@f` holding `-DX`, and `-imacros h` (`receipts/gcc_forms.txt`).
  - The capture records each compile, but `ctrl_shim.parse` reads no flag from any of them. `-imacros` is kept only as a forced file, and its definitions become no mode (`receipts/gate/driver-forms-parse.txt`).
  - Through the gate's own control path, with the ADP adapter reaching a stack example's header only under the mode, F1 to F6 ESCAPE and the gate passes. In the same run, the same plant under a recorded mode (K0) is CAUGHT (`receipts/gate/probes-hosted-mode.log`).
- **Impact:** a builder that writes a mode in one of these ordinary forms gets a firmware unit or a stack source compiled across the boundary. `-Wp,-D` is a common hardening spelling, and response files are what build generators emit for long command lines. The required gate passes. This is the class round 5 ruled closed by construction, reached at the capture's own argument reader.
- **Required outcome:**
  - The modes, include directories and files read first that the boundary judges are those the compiler reads from the recorded invocation. For example, take them from the driver's own expansion of it.
  - Otherwise, every argument the reader cannot interpret refuses the gate by name: a response file, `-Wp,`, `-Xpreprocessor`, the long `--define-macro`/`--undefine-macro`/`--include-directory` forms, and a file read first other than one the gate models.
  - Each spelling above is a standing control.
  - README:112 claims no more than that.
- **Verification:** rerun `scripts/boundary_probes.py <checkout> --capture ... --without verilator --only F`. F1 to F6 must each be CAUGHT, or refused by name, and the self-test must hold the new controls.

### R584-5-F2 - MINOR - Conformance, Robustness, Tests, Docs - configurations only the Verilator builders compile are judged by no required job, and the AECP wire comparison's documented two-interface build by no run of the gate

- **Where:**
  - `.github/workflows/rtl-fast.yml:310` (`--without verilator`);
  - `sw/firmware/ctrl/test/ctrl_configs.py:112-133` (`BUILDERS`: `aecp_wire.py` run with `--interfaces 1` only, `:132-133`);
  - `ctrl_boundary.py:37-52`;
  - `sw/firmware/ctrl/README.md:90,105`;
  - `docs/testing/CI_WORKFLOWS.md:63`.
- **Authority:**
  - Round 5 item 1 names the Verilator C++ compile among the compiles to capture.
  - Round 5 item 2 says the gate "refuses ... any builder from the known set that produced no records".
  - Round 4 item 1: "Do not drop configurations ... or move the gate out of the required job".
  - `ctrl_boundary.py:37-39` says each unit is judged "in every configuration its builders compile it in, and nothing about either is listed here".
  - `sw/firmware/ctrl/aecp/README.md:136-139` documents `aecp_wire.py --interfaces 2`.
- **Evidence:**
  - The hosted step at this head prints `LEFT OUT` for the bench, the MAAP differential and the AECP wire comparison, and judges 22 build modes (job 114282060753, `receipts/hosted_evidence.txt`).
  - Adding the AECP wire comparison's own capture raises the universe to 33 modes.
  - **V1:** `#if defined(PP_TOP_TIM_DEFAULTS)` then an include of a stack example's header, in `aecp/aecp_image.h`, which `aecp_wire.cpp` reaches. It ESCAPES in the hosted mode, and is CAUGHT as `firmware c++ [-DPP_TOP_TIM_DEFAULTS]: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h` once that capture is given.
  - **V2 and V3:** the same under `PP_TOP_IF2` or `AECP_WIRE_INTERFACES > 1`, which only the documented `--interfaces 2` build gives. They ESCAPE in both runs, because no gate run records that build (`receipts/gate/probes-hosted-mode.log`, `receipts/gate/probes-with-aecp-wire-capture.log`).
  - Round 4's derivation read these builders' modes in the hosted job.
- **Impact:** an include across the boundary under a mode only these builders give passes the required hosted gate. Under the two-interface AECP wire modes it passes every run of the gate, including the standalone local command `CI_WORKFLOWS.md` lists.
- **Required outcome (one of):**
  - The Verilator builders' compiles are judged in a required gate: captured where they run hosted, or captured and given. The two-interface AECP wire compile is captured too, with no hand-listed `--interfaces 1`.
  - A maintainer decision, recorded publicly, accepts that these configurations are judged only locally (and which). `ctrl_boundary.py:37-52`, README:90 and CI_WORKFLOWS state that limit, so no document claims "every configuration its builders compile it in".
- **Verification:** V1 to V3 are CAUGHT by name in the gate the outcome names, or the decision is linked and the docs match it.

### R584-5-RS1 - RESIDUE - Docs (PR body only) - the round-5 status lines say no hosted run covers this head

The PR body's Status ends "Round 5 is not pushed, so no hosted run covers it yet". The Round 5 table's item 4 ends "Not measured hosted (not pushed)", and Known limitations says "it is not yet measured on a hosted runner".

**Exact fix:**
- In Status, replace that sentence with: "Hosted at `92b5be18`: `rtl-fast` success; `firmware-unit` passed in 40 min 50 s of its 45 (job 114282060753), its boundary step in 113 s, with the store suites and the coverage ratchet run."
- In item 4 and Known limitations, replace the not-measured clause with "the hosted step took 113 s at `92b5be18` (job 114282060753)".

### Suggestions (optional; no lens effect)

- **R584-5-S1 (retains R584-4-S1 / R585-4-S2), Docs.** `docs/testing/CI_WORKFLOWS.md:76-78` scales a local figure "until a hosted run measures it". The hosted step took 113 s at this head; state that figure.
- **R584-5-S2 (retains R584-4-S2 / R585-4-S1), Robustness.** `firmware-unit` took 40 min 50 s of its 45 at this head (step 8 alone took 32 min 13 s), and nothing enforces the boundary step's 5-minute budget.
- **R584-5-S3, Robustness.** A compile run from a shell string by an absolute path is neither recorded nor refused (probe F7 ESCAPED). The repository's Python idiom gate already refuses `shell=True` and `os.system` in tracked Python, and Makefile recipes are read by make's dry run, so this is optional.
- **R585-2-S2 retained.** `aecp_arms.py:83` takes the submodule's `tests/` while `:144` pins `--stack`.
- **R584-3-S1 retained** for its remaining parts: the `FORCED` constant overlaps F1, and the pin recipe that ignores its exit status was not re-examined.

## 4. Prior findings at this head

| Finding | State at `92b5be18` | Evidence |
|---|---|---|
| R584-4-F1 (MINOR): a computed or written C++ source passes silently | **Resolved.** These controls are `[ok]` in my run and in the hosted step: wildcard, join, glob, iterdir, written from a literal, f-string or formatted template, copied template, header written beside, computed include, and copied out with an old mtime. | `receipts/gate/ctrl_boundary-hosted-mode.log` |
| R584-4-F2 (MINOR): a `-D` make computes in a function word | **Resolved.** patsubst, foreach, `VAR+=`, `-D $(M)`, `-D$(MODE)`, `-DNAME=$(VALUE)` and addprefix are each `[ok]`. | same |
| R585-4-F1 (MINOR): a `-D` not at the start of a literal or word | **Resolved for its spellings.** A mid f-string, a split literal, a shell literal, shlex, str.format, `+` and `%` are each `[ok]`. The class continues at the capture's argument reader as R584-5-F1. | same |
| R584-4-RS1, R585-4-RS1 (PR body, round 4) | Resolved for round 4; the round-5 lines are R584-5-RS1. | PR body |
| R585-3-F1 (MAJOR, hosted timeout) | **Remains resolved.** The job is green at this head, step 11 took 113 s, and steps 9 and 10 ran. | `receipts/hosted_evidence.txt` |
| R584-1/2/3 and R585-1/2/3 MINORs (pin, `run-if2`, shapes, C++ judgement, named C++ sources) | **Remain resolved.** The 20 pin controls (each bench target on a poisoned `wire.h`, the differential, the AECP tools) are `[ok]`, and so are the shape, contract, C++ and named-source controls. | `receipts/gate/ctrl_boundary-hosted-mode.log` |
| R584-4-S1/S2, R585-4-S1/S2, R585-2-S2, R584-3-S1 | Retained as suggestions (above). | |

## 5. Lens results

```text
[R584] MINOR Conformance - R584-5-F1, R584-5-F2 (above). Otherwise checked: acceptance 1-5 under 6091228902/6092176555 - pin 1a9f651c token-identical and newest (receipts/core_tokens.txt), copies removed (git ls-files sw/firmware/ctrl), lwSRP 9197193e unchanged, 5 ctrl_image ELFs and the 30 SRP/AECP fixtures' 730 objects identical to dev aef7ac66 (receipts/images/), coverage rows identical (receipts/coverage_compare.txt), 471+74 plants identical and caught (receipts/mutants.diff, receipts/capture/fw*.log), .gitmodules and scripts/act_ci.py:234-238 TRUSTED_SUBMODULES with its four refusal arms (:10734-10758), rtl-fast.yml:255 and rtl.yml:161 fetch the stack, sw/firmware/ctrl/README.md:56-168.
[R584] PASS RTL - git diff aef7ac66..92b5be18 -- '*.sv' '*.v' '*.svh' hdl/ (empty); tb/verilator/mbx/Makefile:45-122 (FW_SRC/FW_INC from the stack, stack-pin an order-only prerequisite of obj_fw/libctrlfw.a, run-cosim and run-if2) - checked against the 20 pin controls run here (receipts/gate/ctrl_boundary-hosted-mode.log) and the exact-head hosted verilator-suites and yosys-portability success (receipts/hosted_evidence.txt); no clock, reset, CDC or RTL interface contract is touched.
[R584] MINOR Robustness - R584-5-F1, R584-5-F2 (above). Otherwise checked: ctrl_build.stack_pin (sw/firmware/ctrl/test/ctrl_build.py:191-244) blob hashing with added files refused; the capture's fail-closed paths (missing, empty, failed run, dropped builder, bypass by path or by its own PATH, nameless -D, unknown stream count) - each control [ok] in receipts/gate/ctrl_boundary-hosted-mode.log.
[R584] MINOR Tests - R584-5-F1, R584-5-F2 (above): no control covers the driver spellings or the Verilator-only modes, and each escapes. Otherwise checked: 89 boundary and 20 pin controls reach their verdicts; my K0 harness control is caught; all 415 dev test cases present at head plus stack (receipts/test_names.txt); every campaign verdict [ok] (receipts/capture/).
[R584] MINOR Docs - R584-5-F1 (sw/firmware/ctrl/README.md:111-112, ctrl_boundary.py:63-64), R584-5-F2 (README.md:90, ctrl_boundary.py:37-52). Otherwise checked: README.md:56-168, docs/testing/CI_WORKFLOWS.md:56-79,209-214,1575-1583,2327-2336, docs/reference/SUBMODULES.md, THIRD_PARTY.md, CONTRIBUTING.md:381-391, QUICKSTART.md:154-160, docs/design/MAILBOX_SPLIT.md, the maap, aecp and mbx READMEs, sw/firmware/gtest/README.md:173-300 - links at the pin, licence statements (an MIT stack inside the CERN-OHL-W platform), repository public and MIT. R584-5-RS1 is RESIDUE in the PR body and does not affect coverage.
```

## 6. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R584-5-F1, F2) | issue acceptance and rounds 2 to 5; pin and token comparison; images and objects against dev; coverage; mutation tables and campaigns; manifest and workflows | R584-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| RTL | CLEAN | HDL diff (empty); `tb/verilator/mbx/Makefile` pin wiring and 20 pin controls; hosted Verilator and Yosys contexts at the head | R584-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Robustness | UNCLEAN (R584-5-F1, F2) | `ctrl_shim.py`, `ctrl_capture.py`, `ctrl_configs.py`, `ctrl_boundary.py`, `ctrl_build.stack_pin`; 11 probes | R584-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Tests | UNCLEAN (R584-5-F1, F2) | `ctrl_plants.py` (89 controls), `ctrl_pin.py` (20), firmware, store, RV32 and coverage gates under the capture, test-name census | R584-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |
| Docs | UNCLEAN (R584-5-F1, F2; RS1 is residue only) | firmware README, CI_WORKFLOWS, SUBMODULES, THIRD_PARTY, CONTRIBUTING, QUICKSTART, design and module READMEs, module docstrings | R584-5 | `92b5be18817659c1c9903a0544450d29ca7ab3fd` |

## 7. Real limits

- The firmware gates ran on this host's gcc 16.2.1 and CPython 3.14, not the CI-parity gcc 13.3 container. The coverage comparison is same-toolchain (dev and head both measured here). The gcc 13.3 rows come from the hosted logs.
- The control campaign ran as two `--mutation-shard`s, each with `--jobs 4`. That is the same plant set as one `--self-test` run, but not the identical command. My capture therefore holds more invocations than the hosted one (31,331 against 23,791), with the same 22 modes and 942 configurations.
- The standalone gate (every builder, Verilator included, about 49 minutes) was not run. The bench and the MAAP differential were not captured. The Verilator side was judged only through the AECP wire comparison's capture.
- `ctrl_srp_image.py` images were compared as their complete link inputs (objects in link order), not as linked ELFs. Linking needs runtime archives built from external Picolibc, compiler-rt and LiteX sources, which this review did not provision.
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN. The skipped Physical gPTP context is not hardware proof.
- I did not run act. The hosted contexts above were read, not accepted.

## 8. Pending manager duties

- Publish this report and its manifest; carry R584-5-RS1 to the residue checklist.
- Route R584-5-F1 and R584-5-F2 to the lane, or obtain and record a maintainer decision for F2's local-only alternative.
- Hosted and act acceptance at the next head, and the current-dev candidate merge (builder and native banks) against live dev `f88df731`, with its receipts linked on the PR.
- Merge only with explicit maintainer authorization, after two independent positive reviews and the full completion bar.

R584-5 FINISHED
