[A312]

Closes #551

## Status

Merge-dev changes are committed locally for full independent review.
All assigned local gates pass. Publication and full independent review remain pending.

## Description

Every CRF and AAF licence requires ACTIVE AND the real per-source admission
grant. ACTIVE includes the Listener requirement and optimistic admission;
the real grant waits for evaluation of the current TSpec. The
specification-facing scenario pins both terms and nothing else.

A refused re-declaration cannot open the licence, including when its TSpec
differs from the source's previous one. The default licence fixture requires
no licence pulse, STREAM_START/STREAM_STOP pair, Table 5.4 reset or PDU for
both sources at both admission phases. Nonzero counter histories make
unintended resets observable.

The fixture retains passing preloaded-TSpec cases and makes the unwarmed
refusal arm mandatory. Matching admitted cases stream in both histories.
Measured added start latency is 5/5 cycles for AAF and 3/5 for CRF at the two
phases, for both identical and changed TSpecs. That is 30--50 ns at the
fixture's 100 MHz clock. Ordinary Listener Ready adds no cycles.
These measurements cover the two-source fixture.

Q-9/Q-10 retain the admission module mapping, processor status, original
caveats and clause rationale. Generated matrices retain the interface's
34.3/34.4 mapping. The oversized refusal fixture does not establish the 75%
boundary. Interface comments and contract documents now describe both
licence terms and the current-TSpec grant guarantee.

## Merge-dev

Merged `864b36f5e9450ef64f75ca3f0d68c44330e447d7` into this branch.
Head: `f219a5edaa19` on merge `8dc98a429` ([A315] split the round into a merge holding only the conflict resolutions and one content commit; the tree is identical to [A312]'s `9eee4383`).
The resulting processor pin is `990f96526bb89356c963a260ebbdcf2a77e6623a`,
which includes [processor PR #114](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/114)
and its merge `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`.
This implements step 3 of the [recorded decision](https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5816014072).

The three conflicted files preserve the two-term licence, the published-round
and pending-declaration rules, the CSR bit distinctions, and the new
GET_STREAM_INFO coverage. The former residual-window claims and default
skip are removed. The handoff records all five conflict hunks.

A local control temporarily repinned the processor to `7a47f5788ff504f099a47ad4407c340771bb6bdb`,
before the fix. The unchanged unwarmed refusal arm failed 28 assertions:
all four source/phase cases pulsed a licence, added counter edges and reset
interval counters. The merged pin was restored; the control is not shipped.

## How to reproduce

Run the default `crflic` leg. The former `--unwarmed-refusal` invocation now
runs the same mandatory cases. The unwarmed refusal arm preloads 224 bytes,
withdraws, and re-declares 20,000 bytes for both sources at both round phases.
The reverse TSpec change measures admitted-start latency.

## How to validate

Run the full specification-facing suite, `crflic`, `crflic-mutants`, the
default `milan_dp` sweep and all assigned documentation, source, syntax,
idiom and whitespace gates. The licence leg must pass all 415 checks.
The missing-grant controls must fail their named refused-source checks;
the unmodified control must pass.

## Definition of done

- [x] Exact two-term gate scenario and both missing-term failing arms retained.
- [x] Clause mapping, bounded evidence claims and generated matrices retained.
- [x] Processor fix adopted and unwarmed refusal made a required default pass.
- [x] Admitted latency re-measured for identical and changed TSpecs.
- [x] Local pre-fix control fails the unchanged unwarmed refusal assertions.
- [x] All assigned local gates, including the default sweep and mutation campaign.
- [ ] Full independent review, publication gates and final merge validation.
