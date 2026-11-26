Public scope snapshot

Source: https://github.com/kebag-logic/milan-fpga/issues/1013

## Objective and observed evidence

`dev-soft-core` pins `gptp-processor` at 1213ac5b and `third_party/tsn-c-stack` at 715589c1. Both have merged fixes the platform does not carry:

- FPGA-gPTP 3009f9a2: a negative computed link delay of any magnitude is a good exchange, used signed with a -800 ns floor (its issue 109); the engine suite runs its passes at once (its PR 112).
- tsn-c-stack a795471c: an ENTITY_DISCOVER whose control_data_length is above 56 is processed by its first 56 octets (its issue 37).

## Scope

In scope: both pins, the adoption records, the consumer tests and planted defects the new behaviour needs. The published link delay stays clamped to 0 at the public bank.

Out of scope: any other behaviour change; the 128-octet frame limit of the `adp` mailbox channel.

## Acceptance criteria

1. Both gitlinks at the commits above; `docs/reference/SUBMODULES.md` and the change log updated through their generators.
2. Consumer tests: discovers of 57, 84, 102 and 256 (truncated frame) and 2047 (truncated frame) accepted, 0 and 55 refused; negative delays keep asCapable through the platform's transport and PHC, and the public value reads 0. Each rule has a caught planted defect.
3. The complete firmware gate, stack boundary gate, gPTP consumer gates and the `milan_dp` gPTP legs pass; the egress ledger is not worse.
4. The 1x1/1if and 8x8/1if images route at every corner, totals within the recorded band or declared.


Public scope decision: https://github.com/kebag-logic/milan-fpga/issues/1013#issuecomment-7178757153

[A10] **Ruling on the gPTP pin of #1013.** The pin is FPGA-gPTP `3ce71b768a2f6f6a5274c127080146e755d02275` (the merge of its PR #110), not `3009f9a2`.

- `3ce71b76` carries the whole negative-delay change (its issue 109): the verdict, the signed -800 ns floor, the microcode and the engine tests.
- `3ce71b76..3009f9a2` (its PR #112) changes only the engine's test runner: `tb/verilator/engine/Makefile`, `pass_run.py`, `passes_test.py`, `docs/TEST_DEVELOPER.md`. Those two Python files fail two of this repository's docs ratchets: the Python idiom budget, and the count of suite files that use host time or process deadlines. Neither ratchet moves.
- The image inputs (`hdl/` and the microcode generator) are identical between the two commits, so the routes stand.
- The test runner is adopted with a later pin, after a donor change brings it inside both ratchets. That change is tracked in FPGA-gPTP.
