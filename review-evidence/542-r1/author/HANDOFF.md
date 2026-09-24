[A233] HANDOFF -- issue #542 (milan_dp notification checks held a pointer into uns_log across an exchange that can reallocate it)

## State

- Lane: `$LANES/542-notify-pointer`, branch `542-notify-pointer`, clean worktree.
- Base: dev `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`.
- Head: `68117c0bec0b767d38d9bb1150542e2346b615b7` (NOT pushed; push, the PR and merge were outside this assignment).
- Posted: `[A233] REVIEW READY` on #542. No TAKEN comment was posted, because the assignment asked only for REVIEW READY. The takeover facts (branch, references, scope, validation) are in that comment.
- The project board still shows #542 as `Backlog`. It was not moved from this session.
- Only `tb/verilator/milan_dp/sim_nxn.cpp` changed. No RTL, Makefile or docs file changed; `hdl/milan/milan_datapath.sv` (#530) was not touched.

| Commit | Subject |
|---|---|
| `766b6a149` | Add a milan_dp bench lever that reallocates the unsolicited log on every wait |
| `6c5fa5566` | Keep copies, not pointers into the unsolicited log, across the milan_dp notification content bars' exchanges |
| `68117c0be` | Count only the milan_dp lever's moves of a log holding a real frame, not of its own empty entries |

The first commit on its own (old checks plus the lever) is the failing demonstration. Keep the history as it is when pushing (no squash before review), so the SHAs quoted in PR-BODY.md and on the issue still resolve.

## What was done

1. **Fix.** `notify_last()` returns a copy (empty = absent) instead of a pointer into `uns_log`. `notify_seq()` and `notify_same_from()` take that copy by const reference. The `[NOTIFY]` N5 bar (`nB2`), the `[NOTIFY-CRF]` bar (`n1`) and N2 (`nB1`) hold copies. Verdict semantics are unchanged, because every match is longer than 37 bytes, so empty is exactly the old null.
2. **Audit.** No other pointer, reference or iterator into `uns_log` outlives a call that can push into it (full list in PR-BODY.md). The `desc_of()` pointers into the `std::map` `desc_want` are stable and unchanged.
3. **Proof lever.** `-DNOTIFY_REALLOC_TB` makes `await_aecp` and `drain_tx`, the only two pushers, move the log to a fresh buffer and free the old one on every call. It is inert to every reader and compiled out of every Makefile leg. A liveness check in `notify_section` requires that it moved a log holding a real frame.

## Evidence (all Verilator 5.050, at most 8 compile jobs)

Leg builds come from the Makefile's own recipe (`make -n run`, joined), with an out-of-tree Mdir and optional extra flags appended: see `leg.sh`. Every build log's first line records the `sim_nxn.cpp` blob it compiled:

- `d81d8aa` = head `68117c0`
- `235afd9` = dev
- `ef86e5e` = `766b6a1`, the lever with the old checks
- `2504de6` = the head with `6c5fa55` reverse-applied (`sim_nxn.final-lever-old-checks.cpp`)

| Run | Source | Result | Logs |
|---|---|---|---|
| gate legs, plain | head | main 230/0, notify 146/0, nxn 1708/0, nxn8 3136/0, nxndv 1710/0, nxn4c 1708/0 | `build-gate-*.log`, `run-gate-*.log` |
| same legs, plain | dev | same tallies; notify/nxn/nxn8/nxndv/nxn4c output byte-identical to head | `run-dev-*.log` |
| lever | head | notify 147/0 (258 moves), nxn 1709/0 (1 move: the N5 exchange); only the lever's two lines differ from plain | `run-new-lever-*.log` |
| lever + ASan | head | 147/0, 0 sanitizer lines | `run-new-asan-notify.log` |
| lever | `766b6a1` | notify 147/2 (the N5 bar and the CRF bar), nxn 1709/1 (the N5 bar) | `run-old-lever-*.log` |
| lever + ASan | `766b6a1` | 4 heap-use-after-free (2 reads at each bar, freed in `force_uns_log_realloc` under `aecp_xact_from`), 147/2 | `run-old-asan-notify.log` |
| lever | head minus fix | notify 147/2, nxn 1709/1, the same bars | `run-revfix-lever-*.log` |
| lever + ASan | head minus fix | 4 heap-use-after-free at the same two bars, 147/2 | `run-revfix-asan-notify.log` |
| ASan, no lever | dev | 146/0, 0 sanitizer lines: the defect is latent without the lever | `run-dev-asan-notify.log` |
| PR-BODY "How to validate", run verbatim (only the Verilator path and the `cd` made absolute) | head | every expected result as documented | `validate-part12.log`, `validate-part3.log` |

Static gates at head:

- `python3 scripts/check_cpp_idiom.py` exit 0 (all ratchets 0 <= 0); `--selftest` 75/75.
- `python3 scripts/docs_check.py` 0 findings.
- `git diff --check 615b5a5d7 HEAD` clean.
- No U+2014 in the diff or the commit subjects.

Docs were not touched, so the markdown-only gates do not apply.

Pre-existing and unchanged: two `-Wformat-truncation` warnings in `sim_nxn.cpp` `snprintf` lines. They appear identically in the dev build.

Not run: hosted CI and the local `act` replica (nothing pushed), the full `make run` sweep's non-`sim_nxn` legs other than main, and hardware.

## Open questions for review

- Should the lever get a Makefile target and a README row (a follow-up Issue)? It was kept to C++ by the assignment, so today nothing runs it automatically.

## Next steps (coordinator)

1. Push `542-notify-pointer` as it is and open the PR against `dev` with `PR-BODY.md` (first line `[A233]`, contains `Closes #542`).
2. Move #542 on the board, and name the internal cleared-context reviewer and the external reviewer.
3. Run the act replica from a trusted dev worktree once the PR exists.

Scratch builds live under `$VALIDATION_STORAGE/542-a233-obj/` and can be deleted.
