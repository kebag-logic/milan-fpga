[R929] POSITIVE - exact head ec727b64663b4eef2fc8da1ea5e0eae6541597d1

Round R929-2, issue kebag-logic/tsn-c-stack#37, PR #38. Tree `00b9b9eebd1dd1f9ecdea206ead5a0a40ed67951`, base `69bac7cd52815d2ae223a5a3aa6d022a1f1d35de`, previously reviewed head `e0b144904e57c96928f1dd3fca36a00df42f6ed3`. The delta is one commit.

Every round-1 finding on the PR is closed at its cause, shown with controls written for this round. No BLOCKER, MAJOR, MINOR or RESIDUE is open. Three SUGGESTIONS follow.

## Order and independence

The source tree has no AGENTS.md and no docs/README. Read in order: CONTRIBUTING.md, docs/VERIFICATION.md, the issue body (it has no comments), ADP-01 and its clauses, the diff and history, then the author's round-2 packet at evidence commit d46de11e.

The diff pass and all probes were done before any round-1 finding was opened. The two public round-1 findings comments were then read, before this ledger was written. The R930-1 comment was read only as far as its consumer section, which is past both of its findings. No round-2 report by another reviewer and no private author material was read.

## Round-1 findings at this head

| Finding | State | Own evidence |
|---|---|---|
| R930-1 F1 (MINOR): absent-surplus arm kept the surplus readable | CLOSED | `tests/test_adp.cpp:844-848` allocates exactly 82 octets. `ReadsNoOctetPastTheFrame` (`:764-781`, `:864-867`) reads 82 octets that end at a protected page. Ten own overreads were planted: every length, long only, 57 only, 2047 only, last surplus octet, octet 2072, short lengths only, WAITING only, foreign target only, valid_time 31 only. Plain, all ten fail that test by name. Under address sanitizer, all ten are reported. The unchanged core passes both builds. |
| R929-1 F1 (MINOR): upper length bits lost their test | CLOSED | Sweep 57 to 2047. Own masks 0x03FF, 0x01FF, 0x00FF, 0x007F, 0x003F, 0x05FF and 0x0FFF, refusal of 57, 1000 or 2047 alone, a cap at 1500, bounds 55 and 57, and a refusal of surplus-bearing frames are all caught, plain and sanitized. The four narrowed-mask plants are caught. |
| R929-1 F2 (RESIDUE): no link to issue 37 | CLOSED | Sentence at `docs/REQUIREMENTS.md:117`, worded as asked; link at `CHANGELOG.md:5`. |
| R929-1 F3 (SUGGESTION): no long length on RV32 | TAKEN | `examples/rv32/smoke.c:152-181`. Own runs, Debug and Release: head exits 0, exact comparison 64, mask 0x00FF 64, check removed 63. Codes 60 to 79 are used by no other check in the image. See S2. |
| R929-1 F4 (SUGGESTION): consumer patch lengths | TAKEN | `parent-consumer.patch` has 256 and 2047 with the surplus absent and a 0x00FF plant. It applies at 5de21ff3, and with offsets at dev e275d795. |
| R930-1 F2 (MINOR), R929-1 F5 (SUGGESTION): host paths in the packet | CLOSED for round 2 | 25 of 25 files match the manifest, with no absolute host path and no private, tool or model name. The round-1 copies stay a manager matter, as stated in the task. |

## Evidence by lens

- **Conformance.** `src/` and `include/` have no difference from e0b1449, so the round-1 clause reading stands. The citations added to the tests and the smoke checks are clauses already verified there. ADP-01 is unchanged. The new REQUIREMENTS sentence matches the issue. No test-plan or lab reference is in the added lines.
- **RTL.** No RTL, gitlink or layout change. The round-1 verdict carries. The trial merges with `main` and with `dev-linux` both give the head tree.
- **Robustness.** Beyond the overreads above, the guard itself was tested: without the protection call, or with the frame one octet away from the page, `adp-long-control-length-reads-surplus` escapes, so the campaign fails if the guard is lost. A failed page mapping exits 2 and fails the test; it cannot pass it. The sanitizer build passes 10 of 10 test programs.
- **Tests.** Old core with these tests: exactly the five accept instances fail, 44 pass. The campaign selection `adp-` caught 32 of 32, including all eleven length plants. The author's full 489 of 489 was not repeated. ctest 10 of 10; `adp.c` is at 100 % lines and branches after the existing exclusions. The sanitized accept instances take 50 to 90 ms each and the protected-page instances 28 to 51 ms.
- **Docs.** Plant count 485 + 4 = 489 matches `tests/mutations.json`. The VERIFICATION RV32 row and the change log match observed behaviour. Seven gates returned rc 0: traceability, test-inventory, needles, comments, licence, port-contracts and privacy. The posted PR body equals the packet's, and every claim in it that was probed is true. The commit message is one line with no trailer. No lane label, round, reviewer or comment ID is in an added source comment.

Hosted at this exact head: both runs (pull request and push) concluded success for quality and bare-metal. In the pull-request run every step executed. The job logs could not be downloaded, so no per-gate line was read.

## Findings

### S1 - SUGGESTION - Tests, Robustness - a long length is not tested against the other refusals
- **Where.** `tests/test_adp.cpp:840-860`; `read_up_to_a_protected_page` (`:764-781`) drives a foreign target at every length but asserts nothing about it.
- **Evidence.** Four own defects pass all 49 tests: for a length above 56, skip the foreign-target check, skip the version check, skip the message-type check, or read the target eight octets late (`receipts/own-controls-head.txt`). The last passes because `discover()` zeroes the rest of the frame and a zero target is accepted.
- **Authority.** Milan v1.2 5.6.3.1, the discard reason this PR relies on; ADP-01.
- **Why not MINOR.** Each of those checks is one unconditional condition in `adp_rx`, with its own test and plant at length 56. The issue's acceptance list names none of these combinations, and the base refused every long length, so no earlier sensitivity is lost.
- **Outcome.** Optionally add an arm that requires a foreign target, message type 0 and version 1 to be refused at 57 to 2047.
- **Verification.** `scripts/suggested-arm.diff` adds such an arm. The unchanged core passes and all four defects are caught, plain and sanitized (`receipts/own-controls-with-suggested-arm.txt`).

### S2 - SUGGESTION - Tests - 1024 is a stronger RV32 length than 256
- **Where.** `examples/rv32/smoke.c:166`.
- **Evidence.** With 256, the masks 0x03FF and 0x01FF still exit 0. With 1024, all four narrowed masks, the exact comparison and the removed check exit nonzero, and head exits 0 (`receipts/rv32-controls.txt`). The hosted sweep already catches these masks, and no document claims the RV32 control does.
- **Outcome.** Optionally use 1024 and update the two documents that name 256.
- **Verification.** `scripts/rv32_controls.py TREE WORK`.

### S3 - SUGGESTION - Docs - the parent PR draft fits dev-soft-core only
- **Where.** Packet `author/PR-BODY-parent.md`, first paragraph; not part of this PR.
- **Evidence.** At 5de21ff3 the gitlink is 715589c1, and 715589c1 to 69bac7c changes no file in `src/`, `include/` or `examples/`, as the draft says. At dev e275d795 the gitlink is 70936b77, and that range changes `include/acmp.h`, `include/wire.h` and `src/acmp.c`.
- **Outcome.** If the bump targets dev, restate the starting pin and the scope of the range.
- **Verification.** `receipts/merge-and-scope.txt`.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue, ADP-01, REQUIREMENTS, citations in the delta; `src/adp.c` unchanged since round 1 | R929-1, delta R929-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| RTL | CLEAN | no RTL or gitlink in the delta; trial merge trees | R929-1, delta R929-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Robustness | CLEAN | ten overread defects plain and sanitized, guard self-control, sanitizer build, RV32 smoke and bare-metal gate | R929-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Tests | CLEAN | `tests/test_adp.cpp`, `tests/mutations.json`, 28 own defects and a control, 32-plant selection, red run, coverage, RV32 controls, consumer patch | R929-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Docs | CLEAN | CHANGELOG, REQUIREMENTS, VERIFICATION, TESTS, TRACEABILITY, PR body, round-2 packet | R929-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |

## Limits

- No manager source bank ran at this head and none is claimed. Source-head execution evidence is the author's published gate receipts and the focused reproductions here.
- Not repeated here: the full 489-plant campaign, static-analysis, mutation-controls, the entity, boundary, conditional, dependency, assertion-template and acmp-cache gates, gate self-tests, and graphs.
- The consumer arms and plants were not run; only the patch text, its application and the author's logs were checked. The standards were not reopened this round.
- The Release RV32 image and core objects hash as published. The Debug ones do not; the cause was not investigated.
- The packet's file hashes were verified. The evidence commit carries no signature that the host reports, so packet identity rests on the commit and manifest hashes.
- Receipts had the local work directory removed from paths; nothing else was changed.
- Physical calibration NOT RUN; field skips are not hardware proof. No RTL simulation.
- At the end the review clone has the head and tree above, an empty status including ignored files, an index equal to HEAD, all 100 tracked blobs matching, and no submodule gitlinks. Probes ran only in disposable copies.

## Pending manager duties

1. Build and validate the current-dev merge candidate (dev e275d795) at the merge turn and link its receipts.
2. Apply the consumer patch with the pin bump, run the complete parent firmware and boundary gates, and consider S3.
3. Decide on S1 and S2; neither blocks.
4. The already published round-1 packet copies.

R929-2 FINISHED
