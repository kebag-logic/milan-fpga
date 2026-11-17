# [A786] #920 round 3: reset tests and load disposition

Status: REVIEW READY at `81c9a1a0`; every round 3 gate passed. Posted once as [#920 issuecomment-6936474208](https://github.com/kebag-logic/milan-fpga/issues/920#issuecomment-6936474208). Resumed from clean `bd252db1`; no prior round 3 edits,
receipts or public comment were present. Round 2 remains archived at `4a3e37f8`.

## Scope and authorities

- R857-1, PR #938 issuecomment-6935233068: F-1 (Tests/Robustness), F-2
  (Conformance/Docs). R858-1 was positive at the preceding head.
- #920 issuecomment-6935243271: the load acceptance amendment.
- #665 issuecomment-6899740728: allowed mechanisms and unchanged first-dirty window.
- This round adds tests only. Firmware and gateware are unchanged.
- No push, PR edit, board action, route or sync onto #919 in this round.

## Changes and planted defects

| File:line | Reason and check | Named plant | Assertion failure words |
|---|---|---|---|
| `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:235` | `first_change_after_flight`: after two saves, a new first change waits 1,000 to 1,050 ms before erase | `next_now_not_reset` removes the capture reset of `next_now` | `first change after an immediate save must wait its full first-dirty window` |
| `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:252` | `retry_after_rewind`: a successful rewound capture, then a failed write, backoff change, retry and power-cycle restore | `rewound_not_reset` removes the capture reset of `rewound` | `retry after a rewind must capture the backoff change`; `retry after a rewind must restore the backoff change` |
| `sw/firmware/ctrl_nvm/test/nvm_mutants.py:373` | Both plants are registered with their named checks in the store suite's own self-test | As above | Both caught by name in `receipts/gates/new-reset-plants.txt` |
| `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:158,191` | Case 4's claim narrowed to its new record ahead of the rewound cursor, as F-1 permits | Existing case and plants retained | No new claim of distinguishing a refused join behind that cursor |
| `PR-BODY.md`, Description | F-2: both load figures and the amended acceptance line from the manager's ruling | Not applicable | Composition result remains outstanding |

Both reset-removal plants are now caught by the store suite's own self-test.
The full campaign passed: 566 tests at five shapes and all 154 plants caught, rc 0. Its log prints the first 110 characters
of each first failure; the full assertion wording is in the source patch.

R857-1's R-1/R-2 wording residues and S-1 suggestion remain outside the
requested F-1/F-2 delta. No source change is claimed for those items.

## Gates on a clean clone of the final head

| Gate | Status | Receipt |
|---|---|---|
| Store suite, five shapes, RV32 and self-test | rc 0: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`; 566 tests, all 154 plants caught; power-cut tests green; all five RV32 arms ran | `receipts/gates/store.log` and `.rc` |
| fw_coverage --check | rc 0: 39 files, including 100% measured lines and branches in `nvm_store.c` and `aecp_nvm.c`, with the existing exclusions | `receipts/gates/coverage.log` and `.rc` |
| Docs workflow jobs | rc 0: all five jobs report zero failed steps; verifier: 61 executed, 34 declared NOT RUN reasons, 0 bad | `receipts/docs/`; `receipts/gates/docs-verify.md` |
| Images byte-identical to bd252db1 | rc 0: eight ELFs and eight loadable binaries, independently rebuilt at both heads, byte-identical | `receipts/gates/images.log` |
| Load check | rc 0: 1x1/1if 0.517; 8x8/2if 0.798 reported | `receipts/gates/load-grade.log` |

The harness, routes and sweep carry: image identity is verified, and only the two store test files changed (`receipts/gates/source-identity.txt`). These are inherited results, not new executions. The carried receipts are under `receipts/carry/`.
The 8x8/1if routes are misses at the base, owed to #927:
ExtraPostPlacementOpt +0.011/+0.034 ns; ExtraTimingOpt +0.171/+0.014 ns;
AltSpreadLogic_high +0.215/+0.014 ns (WNS/WHS).

## Load acceptance and remaining composition work

1x1/1if is 0.517 of 0.70. The 8x8/1if load is graded by #914's gate
at the composition: 0.735 of 0.75 at #914's head. The 8x8/2if load
of 0.798 is the base's, identical at `70f4056f`, and owed to #890.
This PR changes no load term.

Amended acceptance: "the load within 0.70 at 1x1/1if, and within 0.75
at 8x8/1if by #914's gate at the composition; 8x8/2if's load is owed to #890".
Composition grading, the #919 sync, bench qualification, exact-head hosted
acceptance and independent re-review remain manager/reviewer work.

## Reproduction and provenance

Each gate starts from a clean clone at `81c9a1a0`, with initialized
submodules. The image comparison also creates a separate clean clone of
`bd252db1`. `receipts/reproduction/` holds the sanitized launch scripts.
The image build uses the same fixed flash maps and runtime archives for
both heads; no route or CPU netlist regeneration is involved.
The docs adapter executes the workflow's own run steps and verifies every
step against either its return-code receipt or an explicit NOT RUN reason.
Hosted bookkeeping, package installation already satisfied locally, and
uploads remain distinct from executed gates. Its no-git job deliberately
removes metadata; the adapter records that fact instead of attempting a
post-job Git query in that directory.

Units: `milan-920-a786-r3-store` (CPUs 56-63), `-coverage` (40-47),
`-images` (24-31), `-docs` (72-79). Each has MemoryMax 10 GB and
MemoryHigh 9 GB. No placeholder units were used.

## Publication and cleanup

The round 3 REVIEW READY text is `REVIEW-READY-r3.md`, posted once on #920 as issuecomment-6936474208. The read-back confirms one matching comment and identical text (`receipts/publication.json`).
`PR-BODY.md` is ready for the manager. Nothing was pushed or changed on the PR.
All four own gate units were stopped by their exact names; no active round 3
unit remains (`receipts/gates/units-closed.txt`). Completed clones and the
source tree are clean (`receipts/gates/completed-clone-audit.txt`).

Derived outputs of 72 completed mutant builds were removed only after their
self-test OK receipts existed; the logs were retained. Scratch stayed below
20 GB. No toolchain, environment, tree export or binary is included in this
packet. Sanitized receipts and their SHA-256 index are generated from the
files present. Logs exceeding 200 KB are represented by their hash, size
and a clearly marked excerpt.
