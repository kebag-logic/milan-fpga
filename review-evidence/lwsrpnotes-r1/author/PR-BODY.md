Adds upstream regressions for IEEE 802.1Q-2018 Table 10-3 notes 4 and 5, found during the parent's Mark II F4 review (milan-fpga [#690](https://github.com/kebag-logic/milan-fpga/pull/690), R532-1-F2 and R533-2-F2).

- Note 4: the VP and VO Applicant cells, with both PointToPointMAC values.
- Note 5: AA/rIn!, with both PointToPointMAC values.
- Each test has a named reversal in [`tests/check_reversals.py`](https://github.com/kebag-logic/lwSRP/blob/ced667d8ee35929ab5f9e77a1c5396e173a693d8/tests/check_reversals.py).
- Tests only, no source change. The branch merges `main` with `--no-ff`.

The validation results (both profiles, the reversals and the documentation checks) are recorded in the parent's F4 round-5 evidence.
