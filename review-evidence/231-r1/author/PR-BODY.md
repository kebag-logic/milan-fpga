[A328]

Closes #231

Commit: `af6d19c553ad8c445a80528344baf2273b41ad46`

Establish the current protocol processor area and timing baseline for the shipping 1x1 and supported 8x8 product configurations. Add a reproducible recipe derived from the shipping build, complete wrapper parameters and image hashes, hierarchical resource tables, and mapping comparisons. No RTL or donor changes.

The shipping 1x1 route uses 48,618 LUTs, including 22,441 in the protocol wrapper, with final setup slack +0.013 ns and hold slack +0.014 ns under the existing constraints. Integrated 8x8 synthesis uses 68,136 LUTs against 63,400 available. The baseline distinguishes standalone estimates from integrated results and preserves the historical substitution provenance.

Validation: both full builder modes and every requested local gate returned rc 0. The compiler-backed run exercised 855 target compiler invocations. The historical mf48 calibration report was unavailable in both builder modes; the compiler-absent mode also deliberately skipped target compile evidence. Both documentation CI modes passed. Complete evidence and command records accompany the author handoff.

The existing clock-constraint warnings and I/O-delay omissions remain documented limitations. The three placement runs all pass their final setup and hold checks; the best measured setup slack is +0.123 ns. The complete reports retain the exact shipping result separately.
