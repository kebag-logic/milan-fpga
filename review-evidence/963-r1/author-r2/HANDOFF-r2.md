# HANDOFF, lane 963 round 2 ([A819])

STATUS (2026-11-23 12:55 CET): DONE. `[A819] REVIEW READY` posted on #963 (issuecomment-7100166169) for head
`a18f0996`. Every finding of R898-1 and R899-1 is closed at its cause (below). No unit of this lane is running.
Nothing pushed: the manager pushes `pf-963-1` (one new local commit) and replaces PR #984's body with `PR-BODY.md`.
No firmware, RTL or `tb/` file touched. ETA: none (done).

Lane: /data-2/milan/lanes/fix-963, branch `pf-963-1`, head `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e`, one commit on
the reviewed head `4cca9569` (which PR #984 holds). The lane's working tree is clean. `dev-soft-core` is now `854bd723`
(#960 landed), and the merge base is `dd163e41`.

## The delta (`4cca9569..a18f0996`, test only)

- `sw/firmware/ctrl/test/test_aecp.cpp`, `Core.MapEditsAreTheirDefinitionRowForRow`:
  - **The new illegal mapping.** An illegal mapping may now name an existing stream (0 or 1) at the channel one past
    its format's (`past[in]`, read from the fixture's stream descriptors), not only stream 65535. The definition
    refuses either before its port is read (`illegal(in, r)`).
  - **The seeded edits.** The first 4,000 are drawn call for call as before (`c < ABSENT`, the extra draw only in the
    other branch). A further 4,000 carry the new mapping.
  - **The new floor.** At least 20 output edits must be refused at such a mapping of a stream not yet read
    (`Outcome::unread`); there are 86.
- `sw/firmware/ctrl/test/aecp_map_mutants.py`: row `map-read-before-legal`. It swaps `ILLEGAL` and `idle` at
  `aecp_maps.c:534`, and the edit test grades it on "the edit reads its port once for each output stream its
  definition reaches".
- **Why the first 4,000 were kept.** A first form drew the new kind among the 4,000. The new plant was caught, but two
  existing rows (`map-value-cluster-channel-ignored`, `map-illegal-unflagged`) then failed first on other words, since
  the loop stops at its first failing edit. Re-wording those rows would have rewritten the oracle around the change.
  Keeping the first 4,000 edits identical leaves each of them caught on its own words (`receipts/tests/focused-head/`).

## Findings, each closed

| Finding | Closure | Evidence |
|---|---|---|
| R898-1 F1 / R899-1-F1, "1,846 plants caught" | Each shard's own unit, counted from the gate's printed lines in each complete log. At `50d3f10e`: 1,756 plants (826 + 389 + 541; shard 3's are 359 + 167 + 15), 0 escaped, plus 2 pin controls; shard 0's 88 are suite arms. 1,846 = 1,756 + 88 + 2; R898's 1,758 = 1,756 + 2. At `a18f0996` the AECP campaign has 390, all caught | `receipts/firmware/plant-tally.txt` (each round-1 log's sha256 matches its published excerpt header), `scripts/count_plants.py` |
| R899-1-F2, verification bar marked complete | DoD box unchecked; Status has a what-ran-at-which-head table; the native sweep is NOT RUN, owed to the merge candidate; shard 0 was not re-run as a gate command at the final head | `PR-BODY.md` Status, Known limitations, Definition of Done |
| R898-1 R1, "The port is called exactly as before." | R898's exact sentence | `PR-BODY.md` Description, "The cut" |
| R898-1 S1, the order plant escapes | The test and plant above. Caught at `a18f0996`; escapes against `4cca9569`'s test | `receipts/tests/focused-head/`, `receipts/tests/probe-plant-on-r1-test/` |

## Gate table (this round, all at `a18f0996`, each on a fresh clone, in the foreground)

| Gate | Result | Receipt |
|---|---|---|
| Focused: both map-edit tests unplanted (app, work arms); `map-read-before-legal` and the 16 other rows the edit test grades | pass, pass; 17 of 17 caught on their words | `tests/focused-head/` |
| The new row against round 1's `test_aecp.cpp` | ESCAPED, rc 1, as wanted; controls pass | `tests/probe-plant-on-r1-test/` |
| Seeded tallies (floors raised in a disposable copy) | the new case 86; the others 117 to 3,023 | `tests/probe-tallies/` |
| Shard 0's AECP arms, after the gate's shard inventory | inventory PASS (`1848`, `[88, 827, 391, 542]`); 18 of 18 arms ok | `firmware/shard0-aecp-arms/` |
| Shard 2's table, `aecp_mutants.py --shard i 20`, i = 0..19 | 390 rows, each once, 390 caught, 0 escaped | `firmware/aecp-campaign/` |
| Coverage ratchet | `--selftest` rc 0; `--check` split into its two gate runs and its measurement: PASS (40 files), `aecp_maps.c` 352/352, 423/424 | `coverage/` |
| Docs workflow gate steps | 43 of 46 rc 0; em dash 0 findings over 1 added line vs `dd163e41` | `docs/group-1..4/` |

Not run or not completed at `a18f0996`, as the PR body says:
- **The full native Verilator sweep.** Owed to the merge candidate.
- **The firmware gate's shards as gate commands.** Shard 0 last ran at `25d3dd7a` and shards 1 to 3 at `50d3f10e`.
- **Docs `gate_24`.** Cut by the 570 s cap twice, rc 124 (`docs/gate_24-cut-by-cap-*`).
- **The builder legs `gate_25_0`, `gate_25_1`.** About 17 and 10 min in round 1. All three were rc 0 at `4cca9569`.
- **Unchanged since round 1.** The harness evidence at `25d3dd7a`; the twin and portable gates at `50d3f10e`.

## Notes

- **Foreground.** The tool caps one foreground call at 10 min, and the firmware shards run about an hour each. Every
  unit therefore ran under `timeout 570` (`scripts/fg.sh`), split along the tools' own seams: the campaign's partition
  entry point, the ratchet's gate runs, the workflow's step bodies. A cut unit is kept and named, never counted.
- **CPU.** No range booking. Units ran at the session's affinity (0-95) under a host load of about 110 to 130.
- **Side effect.** The gate's own shard-inventory self-check writes `dispatch-build/` relative to its working directory.
  This happened in the run clone, not the lane (`receipts/side-effects.txt`).
- **Round-1 REVIEW READY.** issuecomment-7096625846 is left as posted; the new comment says it supersedes its tally.
- **Receipts.** `receipts/INDEX.md`, 336 files, host paths replaced by round 1's placeholders. Raw logs and builds are
  in `/data-2/milan/tmp/963-a819/r2/`; clones `clones/r2-*`.

REVIEW READY a18f0996f4b1b654a232dfe56fa64ee7ecaf697e
