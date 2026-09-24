[A257]

Closes #551

## Status

Ready for independent review. All assigned local gates pass.

## Description

A refused re-declaration could briefly license transmission through optimistic admission. Every CRF and AAF licence now requires ACTIVE and the real per-source admission grant. Refused cases produce no licence pulse, STREAM_START/STREAM_STOP pair, interval-counter reset or PDU.

The integration regression stages pending declaration requests and supplies real incoming Listener Ready frames. Both source indexes and both admission phases run. Matching admitted cases still stream, with 0--2 additional admission-clock cycles; ordinary Listener Ready arrivals add none. The required contract documents and register semantics are updated.

## How to reproduce and validate

Run the focused licence leg (`crflic`), its missing-term mutation campaign (`crflic-mutants`), and the default datapath sweep. The [issue assignment](https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5814963437) defines the acceptance cases. Also run the assigned documentation, source-list, language-style, syntax and whitespace gates.

## Definition of done

- Focused licence regression: 253 checks, zero failures.
- All six licence mutants caught; clean control passes.
- Default datapath sweep and all assigned static gates pass.
- Independent review and publication remain with the review handoff.
