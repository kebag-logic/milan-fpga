[A535] #653 bench: disconnect order on the bbf704ec image (lane B11)

## Contents

- **[Status](#status)** -- Review state, the head and `653-b11-bench` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The Issue, the executor and both reviewers.
- **[Description](#description)** -- What the page adds, the result per #653 acceptance item, and the method in brief.
- **[Authoritative references](#authoritative-references)** -- The Issue, the rulings, the clauses and the library source the page cites.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- The exact head and the gate environment.
- **[How to validate](#how-to-validate)** -- The gate commands, their results at the head, and the receipts to re-read.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What the runs do not show.
- **[Round 2](#round-2)** -- The answers to R482-1 and R483-1.
- **[Definition of Done](#definition-of-done)** -- The merge bar and where this PR stands against it.

## Status

REVIEW READY for round 2 at `6b83de0009673ce2c438985a0f9720f079a3715d`: docs only, every docs gate rc 0, `653-b11-bench` -> `dev`. Two commits on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`: `6f76d612` (round 1, the bench run) and `6b83de00` (round 2, page wording only). Live dev is still `6c22d3ca`, so no merge commit was needed. Round 1 was reviewed NEGATIVE by R482-1 and R483-1 on two MINOR findings; round 2 answers them and waits for re-review.

## Linked Issue / roles

Refs #653

Executor: `[A535]`
Internal cleared-context reviewer: `[R482]`
External reviewer: `[R483]`

## Description

A findings page, `docs/findings/653_DISCONNECT_ORDER_BENCH.md`, with the dated section "#653 bench: disconnect order, 2026-10-04", and its row in `docs/findings/README.md`. No other file changes.

The page records the bench item of the [lane B11 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983239639): the disconnect order a real controller sees, on dev `bbf704ec` as booted (no flash).

**Result.** The owner's report is not reproduced on this bench. In all 23 disconnects the UNBIND_RX response left the DUT's port first. The la_avdecc controller library flagged nothing, but its one counter check accepts either order, so that silence is not evidence about the order.

| #653 acceptance | On this image |
|---|---|
| 1. UNBIND_RX response before the unlock's counters notification, AAF and CRF | Held, 23 of 23. Response 7.5 µs after the command; the unlock's GET_COUNTERS 114.2 to 116.8 µs later on AAF input 0, 99.3 and 99.7 ms later on CRF input 1 |
| 2. Bench capture with a control that fails the check | One tap capture per disconnect, read response first by the lane grader and by the provided decoder. In the control, the check reads counters first against the probe's own GET_COUNTERS |
| 3. LOCKED = UNLOCKED after the unbind, STREAM_INTERRUPTED not counted | AAF: 1/1, STREAM_INTERRUPTED 0, in the first push after the unbind. CRF: 1/0 until the 100 ms silence timeout, then 1/1, as expected before PR #655 |
| 4. 20 connects and disconnects with no counter error | No miscount flagged by the library; not a test of the order. One session, 20 AAF and 2 CRF cycles, no compatibility change, diagnostic, query error or lost notification. The library's one counter check accepts MEDIA_LOCKED = MEDIA_UNLOCKED or MEDIA_UNLOCKED + 1 in any connection state, so it could flag neither order nor the CRF 1/0 window. The owner's flag must come from the Hive application's own rules, which were not run |

The AAF talker was still streaming at every UNBIND_RX command (303 to 1,562 frames after it), so each unlock came from the bind fall.

**Method in brief.**

- A C++ probe on the controller host, linked against the bench's la_avdecc 4.3.1.1 build. The library's high-level controller enumerates both entities, registers for unsolicited notifications, binds, waits for MEDIA_LOCKED, and unbinds. A second, low-level entity reads both formats live before each bind (the binding rule; all equal, none set) and sends the control's own GET_COUNTERS.
- One tap capture at the DUT's port per cycle, under the bench lock. Each capture is decoded by the provided `tap_order_decode.py`, unchanged, and by a lane grader that orders by capture position and checks the tap timestamps.
- Restore: every format, map, binding and clock source read back as found. The CRF cycles left the DUT's servo in HOLDOVER; a set to INTERNAL and back on the DUT's CLOCK_DOMAIN, the listener's, returned it to IDLE. The probe and staging were removed from the controller host.

These are operator observations, not review verdicts.

## Authoritative references

- #653: the finding, acceptance 1 to 4 and the CRF item; the simulation lane's [STOP](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980272602) and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980290102) that left the hardware order to a capture at the DUT's port.
- The [lane B11 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983239639) and the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983716764).
- IEEE 1722.1 ACMP UNBIND_RX and AECP GET_COUNTERS (the offsets the grader reads); Milan v1.2 clause 5.3.8.10 (the STREAM_INPUT counters, MEDIA_LOCKED = MEDIA_UNLOCKED on an unsynchronized input).
- The controller library's STREAM_INPUT counter check at tag `v4.3.1.1`, commit `6d61a92e`: [`src/controller/avdeccControllerImpl.cpp:1611-1613`](https://github.com/L-Acoustics/avdecc/blob/6d61a92e7f264c69f23cdc38f50d31114e567aa0/src/controller/avdeccControllerImpl.cpp#L1611-L1613).
- [PR #655](https://github.com/kebag-logic/milan-fpga/pull/655), open: the CRF unlock at the bind fall, which this image predates.
- Round-1 reviews: [R482-1](https://github.com/kebag-logic/milan-fpga/pull/659#issuecomment-5983714179) and [R483-1](https://github.com/kebag-logic/milan-fpga/pull/659#issuecomment-5983705791).

## How to get into the same state

```sh
git fetch origin 653-b11-bench dev
git switch --detach 6b83de0009673ce2c438985a0f9720f079a3715d
# The pinned Markdown renderer, in a virtual environment outside the tree:
python3 -m venv <md-venv>
<md-venv>/bin/python -m pip install --require-hashes -r tools/markdown/requirements.txt
# The bare-metal gate needs pyyaml under the system interpreter.
python3 -c "import yaml"
```

## How to validate

```sh
<md-venv>/bin/python scripts/docs_check.py
<md-venv>/bin/python scripts/check_doc_style.py
<md-venv>/bin/python scripts/gen_toc.py --check
<md-venv>/bin/python scripts/gen_toc.py --verify-anchors
<md-venv>/bin/python scripts/check_em_dash.py --base 6c22d3ca
<md-venv>/bin/python scripts/check_doc_paths.py
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_feature_status.py --self-test
git diff --check 6c22d3ca HEAD
git diff --check 6f76d612 HEAD
```

Expected result / pass criteria: every command rc 0. At `6b83de00`, run unpiped on the physical worktree path:

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | rc 0, 0 findings |
| `scripts/check_doc_style.py` | rc 0 |
| `scripts/gen_toc.py --check`, `--verify-anchors` | rc 0 |
| `scripts/check_em_dash.py --base 6c22d3ca` | rc 0, 0 findings over 394 added lines |
| `scripts/check_doc_paths.py` | rc 0 |
| `scripts/ci_scope.py --selftest` | rc 0 |
| `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0 (the bare call is a usage error, rc 2) |
| `scripts/check_feature_status.py --self-test` | rc 0 |
| `git diff --check`, `git diff --check 6c22d3ca HEAD`, `git diff --check 6f76d612 HEAD` | rc 0 |

The same set passed on the uncommitted worktree first. Not run: act and the hosted workflows (nothing pushed by this lane).

Round 2's page edits can be re-read against: the library lines above at the tag; `summary/o653-grade.json` `own_rsp_to_cmd_us` and the provided decoder's C0 output for the control's two intervals; and the session probe logs for the library's counters updates. The lane packet carries three round-2 receipts for these, made from files already in it.

## Known limitations / out of scope

- One controller layer: the library's own reports, and its one counter check cannot flag the order. The Hive application, the only remaining source of the owner's flag, was not run; the owner's Hive and library versions are not known to this lane.
- The library check was read in the public source at the build's tag, not in the bench's installed binary.
- The control exercises the order comparison, not the grader's selection of the unlock's push.
- One registered controller; the order was captured at the DUT's port, not at the controller host.
- Every unbind came at least 2 s after the input's last counters push.
- The CRF 1/0 window is not re-measured on an image with PR #655.

## Round 2

Docs only, no bench access, under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983716764). One commit, `6b83de00`, changes the page's wording and the README row. No capture, measured order or interval in the per-cycle table changed.

| Finding | Change |
|---|---|
| R483-1 F2 = R482-1 F1: the library check | The page cites the check at tag `v4.3.1.1`, commit `6d61a92e`, `src/controller/avdeccControllerImpl.cpp:1611-1613`, in the function that stores every counters update, and ties the bench's source tree to that tag (its describe line, and the copied header equal to the tag's). It states the condition: the Milan flag is removed only when MEDIA_LOCKED is neither MEDIA_UNLOCKED nor one more, in any connection state; the library's one other MEDIA_UNLOCKED use lists the mandatory counters. So the check can flag neither order nor the CRF 1/0 window. Every update the library delivered carried 0/0 or 1/0 while Connected or 1/1 while NotConnected, all accepted. Acceptance row 4 reads "No miscount flagged by the library; not a test of the order"; the headline and the README row carry the same qualification. The CRF section says the held 1/0 was the update a second after the bind, while Connected, that no update reached the library inside either window, and that no miscount flagged is not evidence that a controller tolerates the window. The page states the conclusion: the owner's flag cannot come from this check and must come from the Hive application's own rules, which this lane did not run; Limits says the same |
| R483-1 F1 = R482-1 F2: the control interval | "The UNBIND_RX command left 1,629.8 µs after the probe's own GET_COUNTERS answer, and its response 1,637.3 µs after it." Both figures recomputed from the provided decoder's C0 output (1,629.836 and 1,637.340 µs); the first equals the grade's `own_rsp_to_cmd_us` |
| R483-1 R1, and R482-1 S1 | The identity row reads, as written: "Equal to the build's AEM image, except the three live-state fields below; the scripted gate reports FAIL on exactly those three". This also takes R482-1 S1, which asked for the same reconciliation |
| R483-1 R2 | This body, restructured into the template's sections with the round-1 content kept |
| R482-1 S2 = R483-1 S1 | Taken as one sentence in the control section and one line in Limits: the control exercises the comparison, not the selection of the unlock's push |
| R483-1 S2 | Not taken: no page change. The grader is the file as run; every capture holds one UNBIND_RX command and one response, so the page's agreement on all 23 stands |
| Merge dev | Not needed: live dev is `6c22d3ca`, the branch base |

Left for the manager, as both reports list: the hosted and act evidence at the head, the current-dev candidate validation, and the re-review of Conformance, Tests and Docs at `6b83de00`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied: this PR answers #653's bench item; acceptance 4 stays open at the Hive layer, so the PR refers to #653
- [ ] New or changed behavior has self-checking tests: not applicable, documentation only
- [x] Required local verification bar passes: the docs gates above, rc 0 at the head
- [ ] Self-test evidence is posted in a PR comment: for the manager; this lane writes nothing on the PR
- [x] No undocumented requirement or interface change remains: none changed
- [ ] Internal cleared-context review is positive: R482-1 NEGATIVE at `6f76d612`; re-review pending
- [ ] External review is positive: R483-1 NEGATIVE at `6f76d612`; re-review pending
- [ ] Blocking and major findings are fixed and re-reviewed: none were raised; the two MINORs are answered at `6b83de00` and await re-review
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed: the findings page and its index row
- [ ] Post-merge containment will be checked before the Issue moves to Done
