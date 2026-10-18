<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Parser suite

This suite verifies byte-level frame parsing.

Run it directly:

```sh
make
```

The harness builds independent wire-format frames.

It checks acceptance, refusal, and message-bank writes.

It proves refused frames leave no stale words.

Its mutation arm plants receive-error defects in the RTL.

Each defect must fail the checks it names.

See the [test developer guide](../../../docs/TEST_DEVELOPER.md).

Dated details remain [archived](../../../docs/history/v1/testing/PARSER_TEST_RECORD.md).
