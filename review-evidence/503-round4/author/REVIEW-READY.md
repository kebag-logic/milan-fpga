# [A154] REVIEW READY: PR #503 revision d

```text
[A154] REVIEW READY
Commit (page): 2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3
Commit (evidence): c1ee27d81c4a1e98f9584e979b73a88acfe238b3
```

## Heads

- **Page:** `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3`, branch
  `500-d3-materialization-adr`, clean. Base dev
  `2d8fd62fd986ea2d6a87d284e144f023034c0944` is an ancestor. Revision d is
  three commits over the reviewed `ab0fb23f`: `dcc97255`, `6a674171` and
  `2a2007cf`, all touching only `docs/design/SAVED_STATE_MATERIALIZATION.md`.
- **Evidence:** `c1ee27d81c4a1e98f9584e979b73a88acfe238b3`, branch
  `500-design-evidence`, clean and never merged. Its tree stays on dev
  `07294a76`, and every path outside `design-evidence` equals that commit.
  The EXECUTED-RUN sources are `a78c79afebab98d53b94c034c92f7191989e8806`.
  The four commits after it change only records, results and documentation
  (`git diff --name-only a78c79af c1ee27d8`).
- **Pins:** protocol-processor `424c688f`, gptp-processor `c1b61743`,
  verilog-axis `48ff7a7e`.

## What changed

- **S4, the listener's boot-owned admission** (answers R217 R3-F1).
  - New prototype `KL_pp_acmp_lsn_admit.proto.sv`.
  - The harness now instantiates the PINNED `KL_pp_acmp_listener`
    (unchanged, with its ROM from the pinned generator) and the pinned
    `KL_pp_timer_service`, fed by producers that hold a request until its
    handshake.
  - New cases L00 to L13, with L03b, L06b, L08a/b and L10 m1/0/p1; mutants
    LG01 to LG05; tracked controls L01 and L05, which must FAIL at the
    pinned wiring.
  - R217's round-three probe runs in an adapted copy, and there is an OOC
    wrapper for the gate in place.
- **Stage 1 owns the descriptor store's roll-back reset** (answers R218
  R3-F1). A `D3_STAGE1` build, cases S1a to S1h on R218's selector-only
  slot, mutant ST1, and R218's reproduction in an adapted copy.
- **Page.** Rules 7, 8 and 11; sections 2, 4, 5.1, 5.3, 6.2, 6.3, 8.1
  (the three release points), 8.6, 8.8, a new 8.9, and 10 to 16.
- **Tickets.** T1, T2, T4, T8, T9 and the index. T8 carries S1, S3 and
  S4; T1 owns both stores' roll-back resets.
- **A10's final-doc items.** The three release points, the START/STOP
  completion rule, and observed timestamps (`RESPONSE.md`).

## Validation

The model and probe commands ran synchronously at `a78c79af` from EMPTY
`D3_OUT`, `OOC_OUT` and `PROBE_OUT` trees under `<fresh-output-root>`,
pinned to CPUs 96-127, with at most 8 build jobs and one build pool. The
times are the observed modification times of each command's log (CEST).

| Command (from `proposal-evidence` unless noted) | Exit | Result | Log time |
|---|---|---|---|
| `python3 -B run.py prep` | 0 | 3 shapes; amended prototypes checked against their pinned sources | 16:30:22 |
| `python3 -B run.py build <every fourth build> --pool 1 --jobs 8`, four times | 0 each | 76 builds: 3 base shapes, the stage-1 build, the tracked glue, 71 mutants | 16:32:52, 16:35:23, 16:37:52, 16:40:23 |
| `python3 -B run.py run --pool 8` | 0 | `SUMMARY FULL builds 76, runs 386, checks 4560, verdict failures 0`; 71 of 71 mutants killed by every named check in completed runs; tracked glue fails its 9 named checks (L01, L05 included) and passes its 4 | 16:45:07 |
| `python3 -B run.py controls --pool 8` | 0 | `CONTROLS 8, not as required 0` | 16:45:48 |
| `r217_probes.py`, `r217_check.py` (round two, `reviewer-probes`) | 0, 0 | 9 runs, 0 not as demanded | 16:46:12 |
| `r218_probe_headers.py`, `r218_check.py` (round two) | 0, 0 | 6 runs, 0 not as demanded | 16:46:33 |
| `r217_r3_probe_preload.py`, `r217_r3_check.py` | 0, 0 | 20 runs (ten scenarios on the gate and on LG01), 0 not as demanded | 16:47:36 |
| `r218_r3_probe_stage1.py`, `r218_r3_check.py` (`FULL_OUT` = the run's `D3_OUT`) | 0, 0 | 12 runs, 0 not as demanded | 16:48:01 |
| R217's own `assert_review_observations.py` (`3d790bc1`) on the gate's and on LG01's results | 1, 1 | gate: both counterexample assertions false; LG01: the held assertion true again, the finite one false only by its exact cycle (107433 against 107431) | 16:48:11 |
| R217's own round-two `check_probes.py` (`7d9da877`) | 1 | `AssertionError` at its line 19, its first counterexample assertion | 16:48:15 |
| `ooc/run_ooc.sh` (inside `OOC_OUT`) | 0 | 26 rows; the 20 earlier rows identical | 16:55:12 |
| `syn/yosys/ooc.sh KL_nvm_backend` (repository root, the 1x1 calibration) | 0 | `1030 LUT, 0 LUTRAM, 468 FF, 6 DSP, 114 CARRY4`, identical to `cal-backend-1x1-n30` | 16:55:36 |
| `python3 -B run.py receipts` at `e70b057f` | 0 | 69 digests (50 evidence files, 19 repository inputs), 0 mismatches against immutable blobs with `GIT_NO_REPLACE_OBJECTS=1` | 17:22:41 |

The page gates ran on the committed page head `2a2007cf`, each as its own
command from the repository root. Every one exited 0:

- `python3 scripts/docs_check.py`: 0 findings
- `python3 scripts/check_doc_style.py`: OK
- `python3 scripts/check_doc_paths.py`: 824 cited paths resolve
- `python3 scripts/gen_toc.py --check`: OK
- `python3 scripts/gen_toc.py --verify-anchors`: 144 links reproduced
- `python3 scripts/check_em_dash.py --base 2d8fd62fd986ea2d6a87d284e144f023034c0944`:
  0 findings over 2,206 added lines
- `python3 scripts/check_hygiene.py --check`: PASS
- `python3 scripts/check_solution_docs.py`: OK
- `python3 scripts/check_feature_status.py`: 0 findings
- `python3 scripts/ci_scope.py --selftest`: PASS
- `python3 docs/traceability/gen_module_matrix.py --check`: up to date
- `python3 scripts/measure_naming.py --check`: PASS
- `python3 scripts/measure_fail_fast.py --check`: exit 0
- `python3 scripts/measure_test_evidence.py --check`: exit 0
- `git diff --check 2d8fd62f HEAD`: clean

Every numeric reading the page quotes was checked against `results.txt`,
`COMMAND_RESULTS.md` and `reviewer-probes/results.txt`. The quotes that
match none of them quote other sources (the firmware, the reviews, the spec,
the sibling page), and none of those changed since `ab0fb23f`.

## Acceptance

- **R217 R3-F1: met, with evidence.**
  - A concrete enforced mechanism owns the listener from the hard reset to
    the binding walk's drained terminal and integrates with the real
    listener.
  - The preload bound is finite by construction, and live handshakes are
    preserved after the release.
  - No ready is masked while a valid is consumed; START/STOP uses its
    completion rule. No request is lost, no stale timer work is admitted,
    and no fairness is claimed. Nothing is released on time.
  - The enable waits for the final preload write and arm, and the completed
    binding restore survives a D3 roll-back.
  - The case map for every required test is in `RESPONSE.md`.
- **R218 R3-F1: met, with evidence.**
  - The descriptor store's reset or re-walk is a mandatory stage-1 owner
    in T1 and on the page, and the debt guard is on the hard reset only.
  - Permanent selector-only controls run on the stage-1 build: below the
    watchdog, 5,000, 16,000, beyond the D3 deadline, and one error.
  - Finite delays end in DEFAULTS with commands served; excessive or
    unproven images end CLOSED. ST1 is killed, and DG01 and DG02 are
    retained.
- **Prior controls:** all retained and graded in the same FULL run.

## Limits, stated

- **Models.** The listener's producers (the dispatch queue, the event
  router, the START/STOP µprogram, ADP discovery) are modelled by their
  handshakes. So are its RX slot read, TX slot pool and PRNG. The
  processor's queue policies are not modelled.
- **Drain terms.** At the pinned timing the manager's registered done
  already follows the last preload's write and arm, so the gate's two drain
  terms (listener idle, strobe gone) are not separately observable. Every
  case grades the property itself.
- **Event traces.** The listener's events are counted per kind: n, n while
  owned, the first 16 cycles, the last one, and pop/take disagreements per
  face. Record writes are run-length encoded, and side effects are capped
  at 256 with a count. This bounds output to at most a few hundred KiB per
  case. Every graded property reads the counts, and no assertion was
  removed.
- **Area.** OOC figures are estimates of prototypes and proxies, not
  bounds. There is no integrated build, no board time and no hardware.
- **Not run.** Neither the product builder nor a full native sweep ran, as
  instructed. No hosted CI or `act` replica ran either: nothing was pushed
  and the PR is unchanged. The manager's and builder's checks and the
  cleared-context reviews remain.
- **Evidence base.** The evidence stays on dev `07294a76` (its examined
  base). Input differences against the page base are the manager's to
  check at integration.

## Open risks and questions

- A true separate defect in the pinned wiring (tracked L05). A read-only
  GET_RX_STATE during the boot binding walk erases a saved binding. It is
  published in `RESPONSE.md` for the manager; no issue has been filed.
- The remaining decisions are listed in `RESPONSE.md`: the live-write
  amendment, filing T8 and T9, #501 and #502, narrowing the gate's
  counter, board and integrated measurements, and the producers' queue
  policy.
