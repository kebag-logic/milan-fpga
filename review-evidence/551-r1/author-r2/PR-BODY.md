[A260]

Closes #551

## Status

Round 2 fixes are ready for independent review; all assigned local gates pass.
Merge and issue closure remain blocked until the processor #112 fix is adopted by a parent pin and
the unwarmed refusal case becomes a required pass.

## Description

Every CRF and AAF licence requires ACTIVE AND the real per-source admission
grant. ACTIVE alone permits optimistic admission; the raw grant alone lacks
the Listener requirement. The specification-facing scenario now pins both
terms and nothing else. Both single-term mutants fail that scenario.

A residual remains: a refused re-declaration whose TSpec differs from the
source's previous one can still receive about one round of licence because
the first-round grant uses the previous slope. This can produce a
STREAM_START/STREAM_STOP pair, Table 5.4 resets and a possible PDU with an
early Listener Ready. [Processor #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112)
owns the fix, following the [recorded decision](https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5816014072).

The fixture retains passing preloaded-TSpec cases and adds an opt-in
unwarmed refusal arm. The default run names its EXPECTED-FAIL skip and
processor dependency. An explicit run preserves all no-pulse assertions and
returns failure on this pin. Observed start latency is 0--2 cycles with a
warm pipeline; the reviewed changed-TSpec case took 4 cycles. These
measurements cover the two-source fixture.

Q-9/Q-10 again identify the admission module behind the parent interface,
with the processor status, original caveats and clause rationale. Generated
matrices restore the interface's 34.3/34.4 mapping. The oversized refusal
fixture does not establish the 75% boundary. Interface comments and contract
documents now describe both licence terms and the residual. This round
changes no RTL logic or processor pin.

## How to reproduce

Run the default `crflic` leg, then run its executable with
`--unwarmed-refusal` from the suite directory. The additional arm preloads
224 bytes, withdraws, and re-declares 20,000 bytes for both sources at both
round phases. The current pin produces 28 assertion failures and exit 1.

## How to validate

Run the full specification-facing suite, `crflic`, `crflic-mutants`, the
default `milan_dp` sweep and all assigned documentation, source, syntax,
idiom and whitespace gates. Both ACTIVE-only and raw-grant-only mutations
must fail the stream-gate scenario; clean controls must pass.

After adopting processor #112, make the unwarmed arm mandatory, require
zero failures, and re-measure start latency for both TSpec histories.

## Definition of done

- [x] Exact two-term gate scenario and both missing-term failing arms.
- [x] Restored clause mapping, bounded evidence claims and residual wording.
- [x] Explicit unwarmed EXPECTED-FAIL arm with unchanged acceptance assertions.
- [x] All assigned local gates, including the default sweep and mutation campaigns.
- [ ] Adopt processor #112 and make the unwarmed case a required pass.
- [ ] Independent re-review, current-candidate validation and publication gates.
