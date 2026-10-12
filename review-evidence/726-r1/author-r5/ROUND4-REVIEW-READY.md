[A605] REVIEW READY

Round 4 source head: `1add0cfbcc778c5292a5935631ca7b47c612b990`.
New commits: `77d78589efc1ea9d1aefae7a813f8a7fb8ff252a` and `1add0cfbcc778c5292a5935631ca7b47c612b990`.

Applied the corrected ruling in comment 6132483068:

- R628-3-F2: both captured make exports suppress directory banners. Clean counter legs print their actual `RESULT: PASS` into the enclosing suite log.
- R628-3-F1: grade spacing and every consecutive notification gap from the first notification, bounded by 1000 ms plus measured service. Grade the final wait and reject insufficient observations. Fixed bins are descriptive only; no startup exclusion remains. Capture ends with service measurement.
- Every start cycle through one simulated second preserves both verdicts: 1,000,001 starts per descriptor/recipient row. Separate starts at 0, 200, 300, 800 and 900 microseconds and one second pass at both shapes. The mailbox check covers all 1001 millisecond starts.
- Corrected the stream-counter document, audit, register-map wording and mailbox link. The replacement PR body removes R628-3-R1 / R629-3-R01 residue and retains `Relates to #726`.

Validation, all completed invocations rc 0:

```sh
MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1
make -j8 -C tb/verilator/milan_dp counters
```

The recursive target prints four `RESULT: PASS` verdicts. Parent uncertain-output runs pass 58 / 247 checks; frames-only runs pass 70 / 301. Baseline controls reproduce the required 12 / 54 failures. Ten parent and three mailbox plants each fail by name, then pass with only that named check omitted, including fixed-grid PHASE plants. Restoring the make-capture defect fails under inherited `-w` and escapes without that condition.

Behavior: 406 scenarios / 1977 steps, zero failures; grader: 80 self-tests. Source inventories, strict RTL closure and its 50-case self-test, lint ratchet, capture guard, all 78 executable docs-check commands and three companion commands pass. Final committed-head docs/style/TOC/em-dash/path and whitespace checks pass. The complete pinned builder exits 0 with 19 explicitly reported optional NOT RUN arms; none of those arms is claimed as tested. Its initial 570-second foreground observer was incomplete; a second foreground observer recovered the actual container exit and full log. An extra unsupported `--strict` invocation produced usage error 2; the documented strict-by-default source-list command passes.

| Shape | Consecutive gaps per corrected condition | Minimum | Maximum | Maximum service |
|---|---:|---:|---:|---:|
| Shipping | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Each descriptor/recipient row satisfies its own bound. Corrected input rows have four notifications; output rows have five. Baseline inputs have one followed by about four seconds of silence. Empty fixed bins reflect completion-stamp drift. Frames-only output counters and wire bits retain TU/MR zero. Mailbox gaps are 1000-1002 ms including the injected stall.

No production RTL or firmware implementation changed this round. Retained shipping area is 49,427 LUT (+35 against dev c6bd08c6's 49,392), 53,378 FF and 87.5 BRAM. Image input equivalence is recorded; capture guard passes, with no capture remeasurement triggered. Submodule pins and contents are unchanged; the worktree is clean. Service peak was 4,676,251,648 bytes with no OOM; the separately capped builder remained within the combined memory target. All lane-owned jobs finished.

`HANDOFF.md` and `PR-BODY.md` contain the Round 4 handoff. The packet includes per-descriptor before/after bins, gaps and timestamps, all 13 detection/escape receipts, the 81-command documentation ledger, source hashes and artifact sizes/hashes. Large artifacts remain hash-only.

Outstanding: the ruling's hosted shard 4/5 result at this new head, including counter verdicts in `suite-logs-4`, is NOT RUN here. This turn prohibits pushing, and the published PR remains at `e893e4d13d99eb5ba00745f0f5cf74ee847972c2`. F2's hosted condition is not discharged. After authorized publication, the trusted current-dev local workflow replica must precede hosted inspection. Independent re-review, the current-dev candidate bank and physical cadence/reference-peer reset/controller-display acceptance remain required. No push, PR edit, merge, bench access, existing-comment edit or submodule change occurred.
