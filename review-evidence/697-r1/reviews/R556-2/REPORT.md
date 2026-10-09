[R556] NEGATIVE - exact head ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3

# R556-2 internal independent review: tsn-c-stack PR #16 (relates kebag-logic/milan-fpga#697)

- Repository: kebag-logic/tsn-c-stack (private), PR #16, branch `review-fixes` into `main`.
- Exact head `ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3`, tree `d8c4f1244d691e84b40a34cb0028b06d068613f3`.
- Base `ae982af85ec97286bd35b39403926d8f0eaec81d`, the owner squash of PR #1. Two commits: `086e5d3` (review fixes and RV32) and `ccb4ac3` (comment reduction).
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075089665
- Reviewer: R556, internal role, cleared context, own detached clone. No source edits, commits, pushes or GitHub writes.

Verdict: NEGATIVE. Three MINOR findings are open (F1 to F3).
Every R556-1 and R557-1 finding is resolved at this head.
The dual-target rule holds locally and on hosted runners.
All 22 core objects are byte-identical across the comment reduction.
The mutation campaign catches 311/311 plants by name on fresh and repeated runs.
The open items are integrator contract text lost in the comment reduction, a comment-gate gap for assembly comments, and a generic needle that the needle audit accepts.

## 1. Scope reconstructed

There is no AGENTS.md. I read CONTRIBUTING.md, README.md, SECURITY.md, CHANGELOG.md and every file under `docs/`.
On #697 I read the issue body and the owner and manager comments:
MIT 6074086970, repository 6074093506, name 6074191062, creation 6074219579, assignment 6074245112, round 2 6074721212, owner decisions and follow-up assignment 6074811248, and the dual-target decision 6074877336.
The governing items are round 2 (item A), the comment reduction with its proof list (item B), and the RV32 job (item C).
I then read the full diff `ae982af..ccb4ac3` and each commit separately. `086e5d3` touches no file in `src/` or `include/`.
The public evidence tree at milan-fpga `2ae0b85`, `review-evidence/697-r1/`, holds round-1 author material for `b9b9c20` only. It has no receipts for this head.
The PR has no manager evidence comments yet. Its only comments are the two review-start notices.
I read the R556-1 and R557-1 reports only after my own pass over the diff.
Branch `dev-linux` was not examined.

## 2. Findings

### F1 - MINOR - Conformance, Robustness, Docs - port-callback and public-field contracts were deleted from the headers but not moved to the docs

- Where: `include/acmp.h:250-253` (`struct acmp_source_state`), `include/acmp.h:305` (`admit`), `include/acmp.h:320` (`env->srp`), `include/acmp.h:389-400` (diagnostic counters), `include/acmp.h:418` (`acmp_tk_registered`), and the ADP and MAAP counter fields. The claims are `docs/IMPORT.md:78` ("Port contracts now live in the porting guide and architecture") and `CHANGELOG.md:9`.
- Authority: owner decision B in [6074811248](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248). Contract material that integrators need, "such as ... the port obligations, must already be in docs/ARCHITECTURE.md or docs/PORTING.md; move it there before deleting it from the header."
- Evidence: `receipts/contract-terms.txt`. I compared each comment removed from the four public headers at `086e5d3` with PORTING.md and ARCHITECTURE.md at the head. The ADP and MAAP port rules moved completely. These ACMP obligations did not move, and no document now states them:
  - `env->srp(ctx, sink, stream)`: a NULL stream means stop listening and clear (Milan v1.2 5.5.3.5.36 step 1). No document mentions the NULL case.
  - `ports->admit(...)`: the ingress passes that talker's ENTITY_AVAILABLE and ENTITY_DEPARTING for the sink on that interface. `bound=false` withdraws it. It is called on bind, unbind and rebind, and by `acmp_open` for each restored binding. PORTING.md:89 says only "bound-talker admission".
  - `struct acmp_source_state`: `dest_mac_valid` means MAAP holds a destination MAC for the source. `asking_failed` means a Listener Asking Failed attribute is registered. The integrator fills this structure. The header keeps only clause numbers, and no document names either field.
  - `acmp_tk_registered(..., failed)`: `failed` means the registered Talker attribute is Talker Failed.
  - The meanings of the public diagnostic counters, for example ACMP `rx_malformed` (includes another AVTP version), `busy_drops`, `unknown_sink`, `impossible` and `reentries`, ADP `stray_expiries` and `deferred_sends`, and MAAP `stale_expiries`. PORTING.md:61 asks integrators to inspect "overflow and discarded-input counters" but names only `probes_lost` and `departing_coalesced`.
- Impact: an integrator can no longer learn from the repository what `srp(NULL)`, `admit` or the two source-state flags require. A wrong port could mishandle stream teardown, talker admission or talker answers. The claim that port contracts live in the porting guide is incomplete. Code is unaffected.
- Required outcome: add these callback semantics, the two source-state field meanings and a short counter table (field and meaning, per core) to PORTING.md. Alternatively, restore them in the headers in a form the owner rule permits. Keep each new sentence short and linked.
- Verification: each comment removed from `include/*.h` in `ccb4ac3` that describes a callback, a public field or a precondition has a matching statement in PORTING.md or ARCHITECTURE.md. `srp`, `admit`, `dest_mac_valid`, `asking_failed`, `failed` and each counter name appear in PORTING.md.

### F2 - MINOR - Tests, Robustness - the comment gate accepts a `#` prose comment in assembly sources

- Where: `scripts/check_comments.py:10`, whose token pattern knows only `//` and `/* */`, and `scripts/check_comments.py:50`, which scans `.S` files. The scope claims are `docs/CODING_STANDARD.md:5` and `docs/VERIFICATION.md:28` ("Prose controls are refused").
- Authority: owner decision B covers `examples/`. Item (2) of this review requires the gate to refuse a planted prose comment.
- Evidence: `scripts/gate_probes.sh`, `receipts/runs/gate-probes.log`, `receipts/gate-probes/`. Five planted prose comments are refused (rc 1): a C source line, a header block, a REQ line with prose, a clause reference with prose, and a mutation fragment. A planted `# Clear BSS, then call the smoke checks ...` line before `_start:` in `examples/rv32/start.S` passes the gate (rc 0). The planted file still assembles with the RV32 cross compiler (rc 0), because `#` is the RISC-V assembler comment character.
- Impact: the shipped `start.S` is clean today, but the gate cannot keep it clean. Assembly is where a future port would naturally add `#` comments.
- Required outcome: in `.S` files, refuse any `#` line that is not a preprocessor directive, or treat its text as a comment under the same allowlist. Add a planted `.S` prose control to `--selftest`.
- Verification: `python3 scripts/check_comments.py --selftest` lists the assembly control as refused. The probe above returns rc 1. The real tree still passes.

### F3 - MINOR - Tests, Docs - one killer uses a gtest value printout as its needle, and the needle audit accepts such needles

- Where: `tests/mutations.json:4409` (`maap-stall-unqueued`, needle `"    Which is: 5"`), its assertion `tests/test_maap.cpp:375` (`ASSERT_EQ(r.frames.size(), 5u)`, no message), and the audit pattern `scripts/needle_audit.py:20`. The claims are `docs/VERIFICATION.md:27` ("No empty or generic needles, including the inherited MAAP cases") and `docs/VERIFICATION.md:95,99` ("assertion-specific message"; "All killers have specific needles. There are no inherited exceptions.").
- Authority: R556-1-F1 and round 2 item 2 ([6074721212](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074721212)). Every killer carries its assertion's own words, and the audit refuses an empty or generic needle.
- Evidence: `receipts/needle-audit-probe.txt`. The audit refuses `"  Actual: false"`. It accepts `"    Which is: 5"`, `"Which is: 1"` and `"Expected equality of these values:"`. These are gtest default value lines. They identify a value, not an assertion. In the campaign XML this plant fails ten assertions in its test. The needle matches line 375 only because no other failing assertion there prints 5. The export re-targeted this killer from a host test to this core test.
- Impact: one of the 311 grades depends on a value printout. It would also accept an unrelated failing assertion whose value happens to be 5. The documented claim of no generic needles is false for this entry.
- Required outcome: give `tests/test_maap.cpp:375` its own message, for example `<< "both owed frames and ANNOUNCE leave once room returns"`, and use that as the needle. Make the audit refuse gtest default-message lines such as `Which is:` and `Expected equality of these values:`. Add them as planted table controls.
- Verification: `python3 scripts/needle_audit.py --selftest` refuses the new controls and passes the table. A fresh campaign still reports 311 CAUGHT with every kill matched by name.

### RESIDUE (wording only; carried to the residue checklist; no verdict effect)

- RS1 - `CHANGELOG.md:3-11` - a "Review follow-up" section sits above "Unreleased", followed by a double blank line. Fix: delete lines 3-11 and add these bullets under `## Unreleased`:
  "- Require fresh complete mutation reports, specific assertion messages, compiler boundary checks and executable test registration."
  "- Link each standard separately. Record the inherited ADP input limits and caller validation obligations."
  "- Require Linux and freestanding RV32 validation in [CI](.github/workflows/quality.yml)."
  "- Link the complete RV32 library against a minimal port and run protocol smoke checks in Debug and Release."
  "- Reduce code comments to licence, requirement and standard tracing."
- RS2 - `docs/VERIFICATION.md:59` - the gate checks a subset, not a match. Fix: "The core imports must stay within the explicit port, memory and integer-helper allowlist."
- RS3 - PR #16 body, "This follow-up's results above are local." Fix: "Hosted runs [37889967433](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889967433) (pull_request) and [37889963458](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37889963458) (push) pass the quality and bare-metal jobs at `ccb4ac3`."

### SUGGESTION (no verdict effect)

- S1 - `include/acmp.h:47-127` and `include/adp.h:23-65` keep runs of 81 and 43 blank lines to preserve line positions. Once this proof is accepted, compact header blank runs that have no `__LINE__` effect.
- S2 - `scripts/mutation.py:45` - a kill that names a test absent from the binary raises an uncaught `CalledProcessError`. The campaign exits 1 and leaves an old `results.json` untouched (`receipts/driver-probes/unknown-test-abort.txt`). It fails closed on rc. Record ERROR for that plant, and remove any old `results.json` at campaign start.
- S3 - `scripts/baremetal.py:38-63` and `scripts/test_inventory.py:31-42` use Python `assert` for gate decisions. `PYTHONOPTIMIZE` would disable them. Raise explicit errors instead.
- S4 - `.github/workflows/quality.yml` - the quality job checks out the PR head, but the bare-metal job checks out the PR merge ref (PR run log: "HEAD is now at 96db9aa Merge ccb4ac3 into ae982af"). Use the same ref in both jobs.
- S5 - `scripts/check_comments.py` cannot see prose inside `#if 0` blocks (`receipts/runs/gate-probes.log`, `comment-if0-prose-block`). Consider refusing `#if 0` in the gated directories.

## 3. Prior findings at this head

| Finding | Original severity | State at ccb4ac3 | Evidence |
|---|---|---|---|
| R557-1-F1 stale XML graded | MAJOR | RESOLVED | `scripts/mutation.py:43` deletes the report before every baseline and mutant run. Lines 51-66 refuse missing, partial, skipped, errored, duplicate and mismatched reports. `mutation-controls` rc 0. My controls: a planted complete-looking XML plus an `exit(0)` plant gives ESCAPED, and the old XML is deleted. Crash and unrelated-needle plants also ESCAPE. The genuine plant is CAUGHT under a hostile `GTEST_FILTER` (`receipts/driver-probes/`). Fresh and repeated campaigns in one work directory both give 311/311 by name (`receipts/regrade-fresh1.json`, `receipts/regrade-repeat.json`). |
| R557-1-F2 digraph include | MINOR | RESOLVED | Dependency output (`-M`) under the real flags plus `nm` undefined symbols. Twelve compiling self-test controls under both compilers. My plants `unistd.h`, `pthread.h`, `sys/select.h`, `sys/types.h`, `alloca.h`, `endian.h`, `malloc` and `puts` are all refused (`receipts/runs/gate-probes.log`). |
| R557-1-F3 column-zero test regex | MINOR | RESOLVED | The inventory reconciles with `--gtest_list_tests`. On a real test file, an indented multiline `TEST` with an unknown ID fails traceability (rc 1). With a known ID and no plant it fails the inventory (rc 1) (`receipts/trace-probes/`). |
| R557-1-F4 ADP input contract | MINOR | RESOLVED | The owner chose documentation. REQUIREMENTS ADP-01 and "ADP input limit", PORTING "ADP input validation" and DEVIATIONS DEV-08 state the limits. Four parameterized controls and the RV32 smoke check pin them. [Issue 3](https://github.com/kebag-logic/tsn-c-stack/issues/3) is open. `086e5d3` leaves `src/` unchanged. |
| R556-1-F1 empty or generic needles | MINOR | RESOLVED as scoped | The 14 named killers carry assertion messages. The audit refuses empty needles and six planted controls, and the driver refuses a bad table before running. A generic needle outside those 14 remains as new finding F3. |
| R556-1-F2 text-matching boundary | MINOR | RESOLVED | As R557-1-F2. Heap and OS use are refused from object symbols, including the macro and pointer forms. |
| R556-1-F3 one link per clause cell | MINOR | RESOLVED | `docs/requirements.json` has one record per standard. REQUIREMENTS.md and the generated TRACEABILITY.md link each standard separately. |
| R556-1-R1 to R4 | RESIDUE | RESOLVED | COVERAGE.md is linked; its rows now point at the porting guide because the rule left `adp.h`. REQUIREMENTS.md:4 links each edition. R3 is superseded by the merge of PR #1. IMPORT.md:65-69 records the added cases. |
| R556-1-S1 to S4 | SUGGESTION | S1-S3 adopted; S4 stated | Actions are SHA-pinned. IMPORT.md holds the commit map. The ratchet carries its generator header. REQUIREMENTS.md says both Milan clauses were checked; I hold no standard text (limit). |

## 4. Assigned checks

### (1) Dual target

- Linux, local, exact head: `scripts/validate.py --jobs 5 --graphs` returns 0. All 20 gates are rc 0 (`receipts/validation/gates.json`). GCC with coverage and Clang with ASan, UBSan and leak detection each run 7 binaries with 369 test instances. Coverage is 100% lines and branches after the five listed rows; raw ADP is 203/205 lines and 93/100 branches.
- RV32, local, exact head: `scripts/baremetal.py` returns 0 (`receipts/rv32/results.json`). Debug and Release link with `-march=rv32i -mabi=ilp32 -ffreestanding -nostdinc`. The final images have no undefined symbols. Core imports are `memcpy`, `memset`, `__mulsi3`, `__umodsi3`, `port_assert_failed` and `ctrl_reentry_assert`. QEMU smoke checks pass in both configurations.
- Refusal: a planted `unistd.h`, heap symbol, OS symbol, failing smoke check and core period defect each make the RV32 gate return 1. Each job fails on its own gate, so either failure fails the workflow.
- Hosted: see (6).

### (2) Comment reduction is comments only

- Same path, same toolchain, CI configurations. I recompiled every core translation unit from `compile_commands.json` with `-g0`, plus `-frandom-seed=0` for GCC. 8 GCC coverage, 8 Clang sanitizer, 3 RV32 Debug and 3 RV32 Release objects are byte-identical between `086e5d3` and `ccb4ac3` (`receipts/runs/objcmp.log`, `receipts/objcmp/`). As-built RV32 objects are identical even with debug information.
- All 369 test cases give the same results at both commits.
- Each of the 311 plants, applied with its own commit's table, compiles to the same core object for every arm, with the same killers (`receipts/plantcmp.json`).
- Line counts are unchanged in all seven core files. All 251 line links in the documents point at non-empty lines. Every TESTS and TRACEABILITY link points at a test declaration. No relative link is broken.
- All 288 clause references left in core comments occur in the original comments (`receipts/refcheck.txt`).
- The gate refuses planted prose in C sources, headers, tests and mutation fragments, but not in assembly (F2).
- Contract migration is incomplete (F1).

### (3) Mutation campaign

- Fresh campaign: 311 CAUGHT, 0 ESCAPED, 0 ERROR. My per-arm regrade from the XML reports matches all 329 kill entries by test name and needle (`receipts/regrade-fresh1.json`).
- Repeated campaign in the same work directory: the same result (`receipts/regrade-repeat.json`).
- Stale, partial and early-exit controls: see R557-1-F1. The author's `mutation_selftest.py` also passes. It refuses nine report variants, and a genuine catch followed by an early `exit(1)` escapes.
- One needle is generic (F3).

### (4) Dependency, symbol, heap and OS gates

- `check_boundary.py --selftest` passes. Ten forbidden controls are refused and two pass controls pass, under GCC and Clang. My eight Linux and three RV32 plants are all refused.
- The standard-header allowance is the closure of the C11 headers under strict `-std=c11`. POSIX headers such as `sys/types.h` and `alloca.h` fall outside it and are refused.

### (5) Documents

- No sentence outside tables and code exceeds 25 words (`receipts/doc-lint.txt`). Every relative link resolves. The README keeps the persona table.
- Claims checked against code: both target commands and flags, the minimal-port symbol set, the ELF class and ABI checks, the QEMU timeout, the 22-object proof, the unchanged core line positions, 311 plants and 329 kills, ten boundary controls, six needle controls, and the static-analysis anchors `maap.c:262`, `adp_port.c:32/40/46` and `smoke.c:137`.
- Three Mermaid diagrams render (graphs gate rc 0).
- Open: the F1 and F3 claims, and RS1 to RS3 wording.

### (6) Hosted CI at the head

- `gh pr checks 16`: quality and bare-metal pass in both runs (`receipts/hosted-pr-checks.txt`, `receipts/hosted-runs.tsv`).
- Run 37889963458 (push) checked out `ccb4ac3` and ran both jobs. Run 37889967433 (pull_request) ran quality on `ccb4ac3` and bare-metal on merge ref `96db9aa`. That merge tree equals the head tree because the head already contains the base.
- Both quality logs show all 20 gates at rc 0. Both bare-metal logs show Debug and Release rc 0 with empty `unresolved_final` (`receipts/hosted-*-extract.txt`). No gate step was skipped.
- I only inspected this evidence. Hosted and act acceptance stay with the manager.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Owner decisions A, B, C and the dual-target rule; REQUIREMENTS, requirements.json, TRACEABILITY, DEVIATIONS DEV-08; 288 clause references in core comments against the originals; ADP input controls and issue 3 | R556-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| RTL (C implementation) | CLEAN | `src/` and `include/` with unchanged code (22 identical objects, 369 identical test results); `examples/rv32/` start-up, link layout, runtime, headers and smoke checks; the CMake freestanding target; `cmake/rv32.cmake`; local and hosted RV32 builds and QEMU runs | R556-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Robustness | UNCLEAN (F1, F2) | `mutation.py`, `mutation_selftest.py`, `check_boundary.py`, `baremetal.py`, `check_comments.py`, `test_registry.py`, `validate.py`, the workflow; driver, boundary, RV32 and comment probes | R556-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Tests | UNCLEAN (F2, F3) | `tests/*.cpp`; `mutations.json` (311 plants, 329 kills); fresh and repeated campaigns with per-arm regrade; plant-object comparison; coverage ratchet; registration and traceability controls on real files; needle audit probes | R556-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |
| Docs | UNCLEAN (F1, F3; RS1-RS3 residue) | README, CONTRIBUTING, SECURITY, CHANGELOG, all `docs/*.md`, the PR body; link, line-link and sentence lint; claims checked against code | R556-2 | ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3 |

## 6. Real limits

- I hold no standard texts. Clause references were checked against the original code comments and the requirement records, not against IEEE 1722.1-2021, Milan v1.2 or IEEE 1722-2016.
- Local tools: GCC 16.2.1, Clang 23.1.1, RISC-V GCC 16.2.0, QEMU 11.1.2, CMake 4.4.4, cppcheck 2.22.0, GoogleTest 1.18.0, Python 3.14.7 and Mermaid CLI 11.16.0 (`receipts/tool-versions.txt`). Hosted runners use Ubuntu packages, including RISC-V GCC 13.2.0 and QEMU 8.2.2. The object proof is same-toolchain only. ELF hashes differ between toolchains, as expected.
- Clang objects built with debug information differ between the two commits. I did not investigate this. The claim and the owner requirement concern `-g0`.
- Local runs used at most 12 parallel jobs to respect the review cap, not the documented 16.
- Graph readability was judged from the Mermaid source and successful rendering, not by viewing the images.
- QEMU smoke checks are not board evidence. Physical calibration NOT RUN. Host unit tests are not hardware proof.
- No manager source bank ran at this head, and I claim none. No author gate receipts for this head are published. The exact-head execution evidence here is my local runs plus the hosted runs.

## 7. Pending manager duties

- Hosted and act acceptance at the head.
- The merge-turn current-dev candidate (source base ae982af85ec97286bd35b39403926d8f0eaec81d, live dev 6aa25dec977c6ad78bf4ff6275de47fb81d0c246) with its builder and native banks.
- Required status checks cannot be enforced on this private repository; the branch-protection and ruleset APIs return 403. The dual-target refusal therefore rests on the merge bar. Confirm both jobs are green at merge.
- Carry RS1 to RS3 to the residue checklist.
- Two independent positive reviews are still required. Publication stays an owner action.

## 8. Packet

Scripts: `scripts/objcmp.sh`, `scripts/plantcmp.py`, `scripts/regrade_mutations.py`, `scripts/gate_probes.sh`, `scripts/driver_probes.sh`, `scripts/refcheck.py` and `scripts/run_logged.sh`. Receipts are under `receipts/`, with host paths redacted. MANIFEST.sha256 lists every published file.

R556-2 FINISHED
