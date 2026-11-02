# D0 findings: testing and CI

Verified against dev `1e80128f`.
Source lines cite dev `1f29f189`.

## D0-057: docs/testing/TESTING.md:1810

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.
