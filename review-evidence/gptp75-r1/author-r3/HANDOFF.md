[A275]

# PR #76 / issue #75 — Round 3

Head: `3face0914efd9d5e71f36da7e30108cfe09c837d`. Branch: `75-slew-active`.

Starting head: `4a897e44243d39945df763d00b96049363a58e78`.

Commit: `Pin inactive asCapable loss and recovery in slew checks`.
The commit has one subject line, no body, and no trailers.

## Changes

- The engine harness (`sim_main.cpp`) loses asCapable through bad Pdelay responses while the slew level is low, holds capability lost for 200,000 cycles, recovers through good exchanges, and consumes pairs at 0 ns and +100 ns. It checks the low level and absence of every edge throughout, no rate write during loss/recovery, and one PI rate write per consumed pair.
- `mutants.py` adds `slew idle asCapable loss arms qualification`. Its pattern and replacement are byte-identical to X01. It must fail `slew: in-band pair after asCapable recovery stays inactive`.
- `docs/MANAGER.md` records the PR's measured engine figures, current measurement date, baseline delta, and published report link.

Only those three files changed: 45 insertions, two deletions. RTL, the generator, all ROM images, and parent sources are unchanged. The worktree is clean.

## Validation

Every local gate defined by the repository's Makefiles passed with return code 0. No CI workflows are tracked. Commands ran in the foreground with direct log capture and generous timeouts; no gate invocation was piped and no suite was skipped.

| Gate | Result |
|---|---|
| PHC contract | PASS |
| Arithmetic | 768 checks, all pass |
| Parser | 268 checks, all pass |
| Engine | 1,613 checks on each of three images, all pass |
| Engine mutation controls | 33/33 caught; positive control passes; all six slew controls fail their named checks |
| Adapters | 81 checks pass; 4/4 mutants caught |
| Independent packet generator | 288 checks pass; 3/3 mutants caught |
| Timestamp tags | PASS |
| Engine and bench lint | PASS |
| Documentation | PASS, including selftests; 20 exact source anchors and seven anchor controls |
| Diagrams | Nine assets and three source-bound images checked; ten selftest arms pass |
| Synthesis | Both blocks pass; timing met |

Fresh engine synthesis reproduces 4,853 LUTs, 3,652 registers, 466 memory LUTs, 1.5 BRAM tiles, four DSPs, and +1.773 ns WNS. The PR baseline has 4,773 LUTs and 3,646 registers: +80 LUTs and +6 registers. The standalone microCPU remains 1,643 LUTs, 733 registers, and +1.941 ns WNS.

The first documentation attempt rejected an eleven-word sentence. It was shortened, then the documentation gate passed. The guide's measurement date was subsequently aligned with the fresh synthesis run, and the documentation gate passed again. Only documentation changed after the functional checks; source hashes verify the tested harness, controls, RTL, and ROMs match this head.

## Reviewer reproductions

The public evidence was fetched read-only into temporary scratch from `kebag-logic/milan-fpga`, branch `gptp75-review-evidence`, archives `4999d8d6344e373e0204995cb36c93cf616e8f9e` and `945592db21cbeeea6d31431457d5ede93293b9ad`. Both archived reports match the public review comments.

- Unchanged `probe_mutants_r2.py`: control passes 1,613 checks; X01 is caught by the shipped harness at the new named check. X02, X04, and X05 are caught. X03 survives, as documented in the review's equivalence finding.
- Unchanged `make_gap_tree_r2.py`, followed by the unchanged driver on X01: Probe C control passes 1,631 checks; X01 fails its recovery check.
- The second unchanged round-2 driver catches R21 at the shipped check and catches R22: two probes caught.

The archived scripts' before/after hashes match. X03's survival is not counted as a caught defect. The existing active-direction asCapable reachability note remains unchanged.

## Evidence and delivery

`PR-BODY.md` contains the full updated PR body, starting with `[A275]`, including `Closes #75` and a Round 3 section. It is prepared locally; the PR was not edited.

- `gates.json` records final commands, return codes, and durations; matching logs retain the results.
- `gates-initial.json` and `docs-initial.log` retain the resolved documentation failure.
- `reviewer-r304/reviewer_00.json` proves X01 fails the shipped check; `reviewer-gap-c/` and `reviewer-r305.log` record the other reproductions.
- `candidate-sources.sha256`, `validation-audit.json`, `scope-and-mutation.json`, and `commit.json` bind validation to the source and commit.
- `reviewer-scripts-before.sha256` and `reviewer-scripts-after.sha256` record unchanged probe sources.
- `round3.patch`, synthesis reports, and `MANIFEST.sha256` complete the packet.

Temporary evidence and build copies were deleted after validation. No toolchains, SDKs, virtual environments, or source-tree exports are stored in this output packet. No push, PR edit, merge, parent edit, or hardware activity was performed.

Parent #545 retains the consumer connection and gates, mastership-retirement addend validation, acceptance of the ±100 ns/two-pair tolerance, and reconciliation of the 0.5 s premise with the measured 3.069413 s / 1.916689 s intervals and possible indefinite hold during lost measurements.
