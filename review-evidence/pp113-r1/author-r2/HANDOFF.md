[A287]

PR #115 / issue #113, Round 2 is ready for delta review at `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e` on `113-latency-notify`.
The commit is `Test every latency comparator bit through notification responses` (one line, no body or trailers).

Implemented the four items in the [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113#issuecomment-5823271483). The delta from `29840136bb2d21bc0fbe92c7c533368f40837ff6` changes only the response test, existing mutation runner, test README and compliance evidence wording. Every tracked RTL byte is unchanged. See [source provenance](round2/head-provenance.json) and [patch](round2/round2.patch).

The walking one runs on the Advertise sink, then the walking zero on the Failed sink. Each bit 0..31 is isolated on the outgoing and returning transition by returning to zero or all ones between values. All 128 changes require exactly one complete, byte-exact response; all 128 unchanged repeats require none. Solicited reads, other-sink state and notification isolation are checked each time. Discovery and 64 separately graded unchanged peer refreshes keep the long sequence live without substituting registration events for latency events.

| Check population | Original | Added | Total |
|---|---:|---:|---:|
| Focused GI | 614 | 5,568 | 6,182 |
| Processor top | 2,074 | 5,568 | 7,642 |
| Full bank, 33 suites | 1,009,045 | 5,568 | 1,014,613 |

All other suite counts match the published Round 1 bank exactly. The new subtotal is printed by the test: 128 changed refreshes × 21 checks + 128 unchanged repeats × 15 checks + 64 maintenance refreshes × 15 checks = 5,568. See [count and gate audit](round2/verification-summary.json).

The existing mutation runner detects all 20 retained mutations, including the original trigger removal and all six requested comparator truncations. Golden and restored runs each pass 6,182 checks. Each mutation compiles successfully, completes simulation, and returns 1 with its required named failure; compile failures are not accepted.

| Added mutation | Required observed failure | Build / simulation rc |
|---|---|---|
| `latency-cmp-low8` | `GI LATENCY-WALK-ONE bit 8 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |
| `latency-cmp-low16` | `GI LATENCY-WALK-ONE bit 16 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |
| `latency-cmp-high16` | `GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |
| `latency-cmp-low31` | `GI LATENCY-WALK-ONE bit 31 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |
| `latency-cmp-high2` | `GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |
| `latency-cmp-bit31-dropped` | `GI LATENCY-WALK-ONE bit 31 step: exactly one unsolicited response for sink 0, got 0` | 0 / 1 |

The reviewers' scripts were fetched read-only at archives `634c5f71fbc0a4df90560def8fdf1de187de6052` and `5597b96dbf392d809cc794dcee8f733ace97e159`. Their original truncation variants ran unchanged against `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e`, with no reviewer test additions. Both golden runs pass 6,182 checks. All eight variants compile with rc 0 and complete with simulation rc 1; every variant fails in both walking sequences and both directions. [Script hashes](round2/review-probe-provenance.json), [named failures](round2/reviewer-named-checks.json), [R310 receipts](round2/reviewer-r310/probes.jsonl), [R311 receipts](round2/reviewer-r311/results.json).

| Reviewer probe | First named failure | Exact-count failures |
|---|---|---:|
| R310 `cmp-low3` | `GI LATENCY-WALK-ONE bit 3 step: exactly one unsolicited response for sink 0, got 0` | 116 |
| R310 `cmp-high2` | `GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response for sink 0, got 0` | 120 |
| R310 `cmp-no-bit31` | `GI LATENCY-WALK-ONE bit 31 step: exactly one unsolicited response for sink 0, got 0` | 4 |
| R310 `cmp-low16` | `GI LATENCY-WALK-ONE bit 16 step: exactly one unsolicited response for sink 0, got 0` | 64 |
| R311 `r-cmp-low16` | `GI LATENCY-WALK-ONE bit 16 step: exactly one unsolicited response for sink 0, got 0` | 64 |
| R311 `r-cmp-no-bit31` | `GI LATENCY-WALK-ONE bit 31 step: exactly one unsolicited response for sink 0, got 0` | 4 |
| R311 `r-cmp-low8` | `GI LATENCY-WALK-ONE bit 8 step: exactly one unsolicited response for sink 0, got 0` | 96 |
| R311 `r-cmp-high16` | `GI LATENCY-WALK-ONE bit 0 step: exactly one unsolicited response for sink 0, got 0` | 64 |

Every local gate required by the processor workflow returns rc 0: documentation links, requirement matrix, rendered diagrams, staleness, module traceability, zero-tolerance lint, all suites, historical NVM figures, portability and response-memory mapping. The [command ledger](round2/COMMANDS.md) maps each command to its status and complete receipt. Commands ran in the foreground with their own exit status preserved.

Parent consumer: base `573f0052a0e4412e81f0845438fcec2086ce5d55`, local candidate `399cb14f75ad1c73995bca4a0adebfab607dd640`, processor gitlink `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e`. The only parent delta is the gitlink. All seven Round 1 commands pass again: both language idiom gates, front-end ratchet, RTL source lists, processor source check with self-test, builder and consumer simulation. The consumer passes 371 checks with zero failures. The four existing front-end findings remain at the ratchet. The builder reports one historical resource-calibration arm unrun because its reference placement report is absent. This is the existing limitation, not new evidence of physical calibration. [Parent identity](round2/parent-provenance.json).

The earlier area measurements are retained because RTL is unchanged; no new physical or routed-timing claim is made. Delta reviews of the two F1 findings remain the reviewers' responsibility. Optional suggestions were outside this assignment. The source branch and parent candidate are clean, local commits only ([final integrity](round2/final-integrity.json)). No push, PR edit, merge or hardware action occurred. Downloaded review archives, probe sources and disposable exports were deleted after verification.

[PR-BODY.md](PR-BODY.md) is the full current PR body fetched anew and updated locally, with the issue-closing line retained. It is ready for the authorized publisher.
