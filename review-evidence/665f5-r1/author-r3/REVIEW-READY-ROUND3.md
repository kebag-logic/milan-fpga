[A572] REVIEW READY - Round 3

Commit: `fb9c57d2ae3484804ff90f67feb57bf420c93dfa` on `665-f5-aecp`.
Two new commits on `0ded1f269a44d107498f177c8276665656e07d30`; no rebase or amend. They are **unpushed**. PR #700 remains published at `0ded1f269a44d107498f177c8276665656e07d30`.

R564-2-F1 (Conformance, Tests, Docs) is addressed per [the Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6086491737). No production behavior changed.

- `test_aecp.cpp:794` now requests 765432 against saved latency 123456 in the ignored-flag/no-subcommand loop.
- `test_aecp.cpp:810`, `Core.SetStreamInfoWithoutSubcommandPreservesState`, checks flags 0/4/8/12 before and after a saved override. Response latency, complete latency store, override bit, callback silence and absence of a notification to a registered peer are all asserted.
- `aecp_wire.cpp:58` uses current 67890 and request 765432. `aecp_wire_oracle.py:103` expects requested latency only for a successful MSRP_ACC_LAT_VALID subcommand, otherwise current latency. Its seventh control plants a request echo and requires the exact latency diagnosis.
- `aecp/README.md:154` states the exception under IEEE 1722.1-2021 7.4.15.1 and Milan v1.2 5.4.2.9.

Both exact R564-2 plants, `nosub-applies-request-latency` and `nosub-reports-request-latency`, now fail **both** `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` and `Core.SetStreamInfoWithoutSubcommandPreservesState`. Their unchanged reviewer harness completed all 70 tests for each plant with assertion failures, not build failures. All three reviewer control plants were caught too. The maintained 72-plant table also includes `nosub-notifies-change` and requires the named diagnostics.

Validation, all command rc 0:

| Command family | Result |
|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 4` | 59 arms, 65 tallies, 1408 checks, zero failures |
| `aecp_arms.py --app --interfaces 1/2`, native and sanitizer runs | 70 tests per arm |
| `aecp_mutants.py --shard PART 2`, PART 0 and 1 | 72/72 plants caught; all 74 named tests have a plant |
| Unchanged R564-2 Q1-Q5 probes | 5/5 at each interface count; Q2 retains current latency |
| `fw_coverage.py --check --jobs 4 --lwsrp third_party/lwSRP` | 30 files pass; all eight AECP/application units raw 100% lines and branches; no exclusion or ratchet change |
| Coverage, tally and required-RV32 self-tests | Pass |
| `aecp_wire.py`, both pinned references | 132/137/137 records, seven oracle controls per ingress |
| Default mailbox target and `gen_mailbox.py --check` | Pass, including 369 host checks and five quick plants |
| Builder bank | Four ordinary and four profile partitions pass; exact table unions verified |
| Documentation workflow | All 73 commands plus final style and added-line checks pass |
| `ctrl_srp_image.py --with-aecp`, both shapes at one/two interfaces | All four full links pass; load bytes, sections and pools unchanged from Round 2 |

Builder gate 11's calibration row is explicitly NOT RUN: its historical placed-utilization report is absent. Physical calibration/routed fit is not claimed.

RAM spans, including the 8192-byte stack reservation: 140400 / 153056 / 194224 / **221728 bytes**. Maximum margin to 224000 is 2272 bytes. Round 3 delta is zero at all four points. The inherited 49 nominal / 55 packed tile estimate remains visible for integration.

The clean worktree contains only six changed test/documentation files across these two commits. No RTL, submodule pin, register map, generated output, default build or shipping image changed. No push, PR edit, merge or hardware operation was performed.

HANDOFF.md and PR-BODY.md have Round 3 sections. The handoff includes every changed file:line, all 74 test-to-defect mappings, coverage/gate tables, four size rows and remaining review obligations. The packet's `ROUND3-REPRODUCE.md`, exact command receipts, assertion logs, reference hashes and artifact digests support reproduction. No toolchain, runtime archive, tree export or file over 200 KB is stored in the packet.

Independent re-review of Conformance, Tests and Docs is owed. R564-2's RTL/Robustness coverage remains a reviewer-owned prior-head claim; no new review verdict or merge readiness is claimed. Publication and the full merge verification bar remain with the authorized lane owner.
