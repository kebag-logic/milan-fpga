[R556] NEGATIVE - exact head b9b9c20a9a44650e176db0c72ad7c752bee20dc4

# R556-1 internal independent review: tsn-c-stack PR #1 (relates kebag-logic/milan-fpga#697)

- Repository: kebag-logic/tsn-c-stack (private), PR #1, branch `import-cores` into `main`.
- Exact head: `b9b9c20a9a44650e176db0c72ad7c752bee20dc4`, tree `f0706be728e592ba936d0cd3556f131d98782970`.
- Base: `b2fb516129fa941f43e8adcd10fb0a62cb686c50`. Source revision: milan-fpga `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/1#issuecomment-6074503705
- Reviewer: R556, internal role, cleared context, own detached clone. No source edits, commits, pushes or GitHub writes.

Verdict: NEGATIVE. Three MINOR findings are open (F1 to F3). The export itself is faithful, the history is clean and reproducible, and every gate passes locally and on hosted runners at this head. The open items are gate rigor and documentation-claim defects.

## 1. Scope reconstructed

There is no AGENTS.md in this repository. I read `CONTRIBUTING.md`, `README.md` and every file under `docs/`.
Then I read the issue body and the owner decisions on #697:
MIT (comment 6074086970), separate repository (6074093506), name `tsn-c-stack` (6074191062), repository created (6074219579), and the assignment (6074245112).
I compared the assignment's acceptance with the diff `b2fb516..b9b9c20` and the full 29-commit history.
After that I checked the public evidence at milan-fpga `2ae0b85`, `review-evidence/697-r1/` (MANIFEST.json plus eight author files), and the two hosted runs at this head.
The PR has no prior review findings to resolve. It has no reviews and no review comments. Its only comments are the two review-start notices.

## 2. Findings

### F1 - MINOR - Tests, Docs - 14 export-introduced killers are graded without an assertion needle, contrary to the documented campaign rule

- Where: `tests/mutations.json` lines 415, 2768, 2783, 2798, 2813, 2828, 2843, 2858, 2873, 2903, 2918, 2933, 2948 (`"needle": ""`) and 4678 (`"needle": "Expected: true"`). The mutants are `advertise-period-wrong`, the twelve `acmp-*-reads-the-clock*` / `acmp-*-samples-the-grandmaster` plants, and `maap-allocation-seam-disconnected`. The rule is enforced at `scripts/mutation.py:56-58`. The claims are at `docs/VERIFICATION.md:57` ("Every required killer must fail; an unrelated failed assertion is insufficient") and `docs/TESTS.md:5`, which `scripts/test_inventory.py:30` generates ("The campaign requires that named assertion to fail").
- Evidence: `receipts/needle-audit.txt`, `receipts/killer-classification.txt` and `receipts/mutant-table-compare.txt`. In the source table, each of these 14 plants was killed by a named assertion with its own words. Examples: `C1 GET_RX_STATE -> response` and `TMR_DELAY x DELAY(timer armed)`. Those killers lived in mailbox or processor-walk tests. The export moved them to new core tests with an empty or generic needle. `matches()` tests `'' in message`, which is always true. So any failed assertion in the named test now counts as a catch. For example, `acmp-expiry-reads-the-clock-twice` and `acmp-delay-reads-the-clock-again` share `AcmpCore.TimerPortBudgets` and cannot be told apart. In this run the right assertions did fire (`receipts/local-validation/mutation-results-summary.txt`). The grading does not require it, though. Eight more needle-less MAAP killers are inherited unchanged from the source table.
- Impact: The source campaign graded these 14 defects at assertion level. The export grades them at test level only. The published claim that an unrelated failed assertion is insufficient is false for 22 killers. This weakens "caught by name" for the replacement killers and affects a verification claim.
- Required outcome: Give each export-introduced killer its assertion's own words. The messages already exist, for example "GET_RX_STATE needs no clock" and "timer expiry never samples the grandmaster". For `advertise-period-wrong`, use a killer whose assertion carries a message, such as `AdpCore.A0toA2Schedule` / "A1 TMR_DELAY", or add one. Make the inventory or the driver refuse an empty or generic needle, except an explicit list of the eight inherited entries. Alternatively, give those entries needles too and state the remaining exception in VERIFICATION and TESTS.
- Verification: `python3 scripts/mutation.py --work <dir> --jobs 16` reports 311 CAUGHT. `scripts/needle_audit.py` reports 0 export-introduced unspecific killers. A planted table entry with an empty needle is refused.

### F2 - MINOR - Robustness, Tests - the include-boundary and no-heap gate is a text matcher that a digraph include or an indirect allocation bypasses

- Where: `scripts/check_boundary.py:25`, which only recognises a `#` directive introducer, and `scripts/check_boundary.py:31`, which only matches `malloc(`-style calls. The claim is at `docs/VERIFICATION.md:25` ("C library and owned headers only").
- Evidence: `receipts/boundary-probes.txt`, from `scripts/boundary_probes.sh` on a disposable clone. In ISO C11 the digraph `%:` introduces a directive. A planted `%:include <unistd.h>` or `%:include <pthread.h>` at the top of `src/adp.c` passes the gate (rc 0). It also compiles with `-std=c11 -Wall -Wextra -Werror` (rc 0). An allocation through a macro (`#define TSN_GET malloc` then `TSN_GET (4)`) or a function pointer (`= malloc;`) also passes. The `#include <unistd.h>` and `#include "mbx.h"` controls are refused, as documented. The shipped library itself is clean: `nm -u libtsn.a` shows only `memset` and the toolchain's `__stack_chk_fail` for both compilers (`receipts/library-builds.txt`).
- Impact: Acceptance item 2 of the assignment requires a gate that refuses any include outside the C library and the repository's own headers. A planted control must be caught. An outside include or heap use can reach the library while the gate reports pass. The no-heap and no-OS properties hold today only because no such code exists, not because the gate enforces them.
- Required outcome: Base the include check on the preprocessor. For example, check each library translation unit's dependency output (`-M`/`-H`) under the real compile flags against `include/` and the allowed C headers. Otherwise, recognise `%:` (and `??=`) introducers. Base the allocation check on the built objects' undefined symbols, or on preprocessed output. Add a planted control for each bypass above.
- Verification: `scripts/boundary_probes.sh <clone>` reports gate_rc=1 for the digraph and heap probes. `scripts/check_boundary.py --selftest` lists the new controls.

### F3 - MINOR - Docs, Conformance - combined clause cells give one link for two standards; the generated matrix drops the second standard's link

- Where: `docs/REQUIREMENTS.md:11-14,16,20,22,26` (ADP-01, ADP-02, ADP-03, PORT-01, ACMP-02, ACMP-06, ACMP-08, MAAP-03) and `docs/TRACEABILITY.md:9-12,14,18,20,24`. The matrix is generated by `scripts/traceability.py:72`, which renders only `links[0]`.
- Evidence: In ADP-01 the text "Milan v1.2 5.6.3.1" sits inside a link to the IEEE 1722.1 page. In ACMP-08, "IEEE 1722.1-2021 8.2.1" sits inside a link to the Milan page. In MAAP-03, "Milan v1.2 4.3.5.1" sits inside a link to the IEEE 1722 working-group page. REQUIREMENTS.md adds a "companion reference" link. The generated TRACEABILITY.md, which the assignment names as the requirement-to-test-to-clause record, has no link at all for the second standard in these eight rows.
- Impact: The owner's public-docs rule says every reference is a link. Here eight clause references in the generated traceability record point to the wrong standard or to none. A reader following a Milan clause lands on an IEEE page. The fix touches a generator and a generated artifact, so this is not wording only.
- Required outcome: Give each cited standard in a clause cell its own link. One way is to split `clause` in `docs/requirements.json` into per-standard parts and render one link per part. Then regenerate `docs/TRACEABILITY.md`.
- Verification: `python3 scripts/traceability.py --selftest` passes. In both documents, every Milan clause links to the Milan page, every IEEE 1722.1 clause to the 1722.1 page, and every IEEE 1722-2016 clause to the 1722 page.

### RESIDUE (wording only; carried to the residue checklist; does not affect the verdict)

- R1 - `docs/COVERAGE.md:7-11` - "The no-callback rule in `adp.h`" names a file without a link, and the page has no links. Fix: change it to "The no-callback rule in [adp.h](../include/adp.h)" in each row. Add under the heading: "The [coverage reader](../scripts/coverage.py) applies these rows. The [ratchet](../tests/coverage.ratchet) records the result."
- R2 - `docs/REQUIREMENTS.md:4` - the edition names are not links. Fix: "The cited editions are [IEEE 1722.1-2021](https://standards.ieee.org/ieee/1722.1/6670/), [Milan v1.2](https://avnu.org/resource/milan-specification/) and [IEEE 1722-2016](https://sagroups.ieee.org/1722/)."
- R3 - PR #1 body - "Hosted execution awaits publication of this branch." is stale. Fix: "Hosted runs 37885778682 (pull_request) and 37885778700 (push) pass all 16 gates at `b9b9c20`."
- R4 - `docs/IMPORT.md` - the record does not say that the validation commit changes the imported test files. Fix: add "The validation commit adds `// REQ:` annotations and seven core cases to the imported tests: AdpCore.EntityFieldsUseIndependentCounts, AdpCore.LinkLevelsAndDisabledInputs, AdpCore.MockedPortOrder, AcmpCore.DepartingStopsEveryProbingTimer, AcmpCore.CommandPortBudgets, AcmpCore.TimerPortBudgets and AcmpCore.DiscoveryPortBudgets. No imported case body changes."

### SUGGESTION (no verdict effect)

- S1 - `.github/workflows/quality.yml` - pin `actions/checkout` and `actions/upload-artifact` to commit SHAs.
- S2 - `docs/IMPORT.md` - record the 26-row original-to-exported commit map in the repository. Today it is only in the milan-fpga evidence directory.
- S3 - `tests/coverage.ratchet` - it lacks the "Generated by scripts/coverage.py --write." header that `render_ratchet` writes. Regenerate it so a later `--write` produces no diff.
- S4 - Two cited clauses are not cited anywhere in the code or tests: ACMP-05 "Milan v1.2 5.5.2.3" and MAAP-03 "Milan v1.2 4.3.5.1". The source project's documents use 4.3.5.1 for "MAAP mandatory for talkers". Confirm against the standard text that each supports the stated requirement.

## 3. Evidence by acceptance area

### (1) Export fidelity - CLEAN

- All seven production files (`src/{adp,acmp,maap}.c`, `include/{adp,acmp,maap,wire}.h`) and `tests/acmp_fake.hpp` are byte-equal to their `6aa25dec` blobs. The only change is line 2, `CERN-OHL-W-2.0` to `MIT`. `SPDX-FileCopyrightText` lines are kept. These blobs are identical between `21d132b` and `b9b9c20`. See `receipts/export-compare.txt` and `receipts/export-reproduction.txt`. The sizes and hashes agree with the author's `production-proof.json`.
- Test split (`receipts/test-case-compare.txt`):
  - `test_adp.cpp` drops B1, C0-C6, E0-E4, E5 and F0-F7. Each uses `mbx_model`/`ctrl_app`.
  - `test_maap.cpp` drops the three `MaapCsr` cases (the register rig).
  - In every file, no retained case body changes, apart from added `// REQ:` lines.
  - The shared harness label and `fw_gtest.hpp` include are removed. The ADP header comment is replaced.
  - Seven new core cases are added in `b9b9c20` (see R4).
- No file touching the mailbox, register map, image or adapters is in the tree or in any of the 29 commits. Every path ever present is listed in the history check. Adapter mentions are comments only.
- `acmp_nvm` is excluded because it includes `nvm_state.h` (an external store interface). This matches the assignment's "only if core-only".
- Mutation table (`receipts/mutant-table-compare.txt`): the source campaign has 471 mutants, 311 of them on the exported core paths. All 311 are present by name with identical `old`/`new` plant text. No export-only mutants exist. `original_tests` equals the source killers for all 311. For 110 plants the killers changed. In every one of them the source killer is no longer in this repository, because it was an adapter, processor-walk or host-model test. No retained source killer was replaced (`receipts/killer-classification.txt`). See F1 for needle rigor.

### (2) History and privacy - CLEAN

- 29 commits. Every author and committer is `hackerman-kl <hackerman-kl@kebag-logic.com>`.
- Subjects are one line with no body: 26 times "Update portable protocol cores and tests", then the merge "Import portable protocol cores and core tests", then "Add standalone validation and portable stack documentation".
- `e529a7b` merges `b2fb516` and `21d132b`. It adds only the 13 exported paths over the base.
- Provenance is adequate. I re-ran `scripts/export_history.py` against a full clone of milan-fpga at `6aa25dec`. It reproduced head `21d132baa148f4731a1622b425e4327c1ac7a44f` with 26 commits. Its commit map is identical to the published `retained-commit-map.tsv` (`receipts/export-reproduction.txt`). The 3628 examined commits match the source count.
- My own scan covers all 87 reachable blobs and every commit message (`receipts/history-scan.txt`, `scripts/history_scan.py`, plus a reviewer-held term list). It finds no host or home paths, no personal or account names, no private devices, network addresses, product or model names, or secrets. The only email is the holder identity.
- The remaining hits are inherited neutral labels in byte-equal source comments: lane and reviewer labels, and milan-fpga issue numbers. They are neutral role labels. The repository gate `check_privacy.py` also passes (29 commits, 87 blobs, 51 files).

### (3) Stand-alone build and boundary - CLEAN except F2

- `-DTSN_TESTS=OFF` library builds with gcc and clang use `-std=c11 -Wall -Wextra -Werror` and return rc 0.
- Each source also compiles with `-pedantic-errors`, in the debug and re-entry variant, with both compilers.
- Each public header compiles as C++20 with `-Werror`.
- `libtsn.a` has no undefined heap, thread, time or I/O symbols (`receipts/library-builds.txt`).
- The boundary gate refuses its seven documented controls. F2 shows bypasses.

### (4) Tests, coverage, mutation, sanitizers, static analysis - CLEAN except F1

- Local `scripts/validate.py --jobs 16 --graphs` passes all 16 gates with rc 0 (`receipts/local-validation/`):
  - 365 test instances in 7 binaries. GMock `StrictMock` is used in `AdpCore.MockedPortOrder`.
  - Coverage is 100% lines and branches after the 5 listed rows, which name 7 arcs and 2 statements of `src/adp.c`. The rows are identical to the source exclusion table. The raw ADP figures are 203/205 lines and 93/100 branches.
  - Mutation: 311 CAUGHT, 0 ESCAPED, 0 ERROR, with 325 required killer failures.
  - Sanitizers, static analysis with the 5 listed suppressions, boundary, licence, traceability, test inventory, coverage controls, privacy, and 3 graphs all pass.
- The ADP denominator is one line and two arcs smaller than the source ratchet (204/95). This matches the documented exclusion of debug-assert instructions (`src/adp.c:29`).
- Gate sensitivity probes (`receipts/probes.txt`):
  - UBSan aborts on a planted signed shift in `wire.h`.
  - The coverage gate refuses a planted dead branch.
  - The mutation driver marks an equivalent plant and a wrong-killer plant as ESCAPED, rc 1.
  - Static analysis refuses a planted uninitialized return.
  - The licence gate refuses a wrong identifier and a missing identifier on real files.
  - Traceability refuses an unknown ID.
- Killer prefix overlap was checked. Exact `--gtest_filter` patterns stop sibling parameter instances (for example `TableB7/1` and `TableB7/10`) from satisfying each other.

### (5) Quality documents - UNCLEAN (F1, F3; R1-R4 residue)

- All required documents are present. A link check over all Markdown found no broken relative links (`receipts/doc-lint.txt`) and no sentence over 25 words outside tables.
- Personas are covered: the README table names developer, integrator, tester and manager, and PORTING and VERIFICATION address their roles.
- Claims I checked against code match:
  - frame sizes 82/70/60;
  - ADP two owed departures and one owed advertisement;
  - MAAP 16 queued frames, at most two sends per poll, and `MAAP_SERVICE_MS` 10;
  - ACMP owed queue of 8;
  - the suppression locations `maap.c:262` and `adp_port.c:32/40/46`;
  - the counts of 7 boundary controls and 3 licence controls;
  - the coverage exclusion counts.
- `requirements.json` and REQUIREMENTS.md agree for all 17 IDs. The generated TRACEABILITY.md and TESTS.md are current.
- The requirements cite clauses and copy no standard text.

### (6) Hosted workflow - CLEAN

- Runs 37885778682 (pull_request) and 37885778700 (push) ran on `ubuntu-24.04` and checked out exactly `b9b9c20`. Both concluded success.
- In each run the "Validate the portable cores" step executed, and all 16 gates in the uploaded `gates.json` show rc 0. That covers 311 CAUGHT, 7/7 ctest under gcc and under clang with sanitizers, the 100% coverage table, privacy (29/87/51) and 3 graphs (`receipts/hosted-evidence.txt`).
- No gate was skipped. The workflow installs no FPGA tool.
- I only inspected this evidence. Hosted and act acceptance stay with the manager.

## 4. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | REQUIREMENTS.md, requirements.json, TRACEABILITY.md, DEVIATIONS.md, clause citations in `src/`, `include/` and tests, byte-equality of the production cores to `6aa25dec` | R556-1 | b9b9c20a9a44650e176db0c72ad7c752bee20dc4 |
| RTL (C implementation) | CLEAN | `src/*.c`, `include/*.h` (byte-equal export), `examples/adp_port.{c,h}`, CMakeLists.txt, gcc and clang library builds, undefined symbols, pedantic, debug and C++20 header compiles | R556-1 | b9b9c20a9a44650e176db0c72ad7c752bee20dc4 |
| Robustness | UNCLEAN (F2) | `scripts/check_boundary.py`, `check_license.py`, `check_privacy.py`, `validate.py`, `mutation.py`, `coverage.py`, the workflow, and the boundary, sanitizer, coverage, mutation, static and licence probes | R556-1 | b9b9c20a9a44650e176db0c72ad7c752bee20dc4 |
| Tests | UNCLEAN (F1, F2) | `tests/*.cpp`, `acmp_fake.hpp`, `main.cpp`, `mutations.json` against the 471 source mutants, the coverage ratchet, the local full kit and the hosted artifacts of two runs | R556-1 | b9b9c20a9a44650e176db0c72ad7c752bee20dc4 |
| Docs | UNCLEAN (F1, F3; R1-R4 residue) | README, CONTRIBUTING, SECURITY, CHANGELOG, `docs/*.md`, the PR body, the link and sentence lint, and claims checked against code | R556-1 | b9b9c20a9a44650e176db0c72ad7c752bee20dc4 |

## 5. Real limits

- I had no standard texts. Clause numbers were checked against the in-code clause citations and the source project's documents, not against IEEE 1722.1-2021, Milan v1.2 or IEEE 1722-2016.
- The production cores are byte-equal to reviewed source. I did not re-review their protocol logic beyond that equality and the passing core tests.
- Local runs used gcc 16.2.1, clang 23.1.1, cppcheck 2.22.0, GoogleTest 1.18.0 and Python 3.14.7. These are the same versions as the author's `versions.txt`. The hosted runs supply an independent toolchain (ubuntu-24.04).
- I judged graph readability from the Mermaid source and from successful rendering. I did not inspect the images visually.
- I extracted the source mutation table by importing the source repository's own table modules from a disposable extraction.
- No manager source bank ran at this head, and I claim none. Physical calibration was NOT RUN. Host unit tests are not hardware proof.

## 6. Pending manager duties

- Own hosted and act acceptance for this head. Carry R1-R4 to the residue checklist.
- Collect the second independent review (R557). Merge needs two independent positive reviews at one exact head, after F1-F3 are resolved.
- Keep the repository private until the licence and documentation PRs merge with two reviews each. Publication is a separate owner action.
- The milan-fpga consumer PR is outside this lane. It covers the submodule pin, `.gitmodules`, `TRUSTED_SUBMODULES`, byte-identical RV32 images and the current-dev candidate validation at the merge turn.

## 7. Packet

The receipts, portable scripts and raw logs are listed in `MANIFEST.sha256`, with paths relative to the packet root. Absolute host paths in the logs are replaced by `$SCRATCH`, `$PACKET` and `$CLONE`. The review clone was verified after the probes. It is at `b9b9c20`, its index equals HEAD, every tracked blob, byte and mode matches the tree, and the working tree is clean. This repository has no submodule gitlinks.

R556-1 FINISHED
