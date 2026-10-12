[A606]
Closes #24

Expose the talker declaration predicate per source: valid destination AND (a probe answer younger than the entity-configured 15000 ms interval OR a registered Listener), per Milan v1.2 clause 4.3.3.1. One explicit Listener input updates core state without callbacks. Accepted responses start the wrapping-clock window; queued responses do not. Existing response behavior is preserved.

## Round 2

The shared entity round trip checks configuration propagation and one positive freshness path on both targets. Core tests independently cover the predicate terms. Zero disables probe demand while preserving Listener demand; initialization refuses intervals at or above 2^31 without changing state or calling ports.

## Round 3

Two serviced-wrap tests retain one answer through `2^32 + 100` ms, with query gaps at most 1000000000 ms. Withdrawing the Listener or restoring destination validity leaves the expired probe closed after the counter aliases a fresh age. Both suppression plants have separate killers.

## Round 4

Add regressions for a valid but wrong Listener interface, withdrawal while a probe remains fresh, and initialization with a Listener still registered. Add callback-budget assertions and explicit Asking Failed, timestamp-reset and input-guard checks. Production code is unchanged this round.

The verification guide maps all 31 behavior sentences in the added port contract and ACMP-11 to tests and registered plants, or an explicit reason for caller/authority obligations. All 42 distinct table plants fail exactly their named killer in the complete eight-binary suite (424 instances). Physically deleting only that test makes each plant escape with 423 completed instances, no failures and no skips. The unchanged supplied full-suite script catches all three requested review plants. Two older plants now isolate interface-range and probe-reset defects separately from the new regressions. TESTS and TRACEABILITY are regenerated.

All 28 validation gates return 0. All 388 registered mutation plants are caught, with zero escapes or errors. GCC, Clang sanitizers and coverage pass; ACMP remains at 792/792 lines and 392/392 branches. Both freestanding RV32 configurations link and execute their smoke checks. Post-commit privacy passes.

Release remains 36864 loadable bytes, versus 35792 on main (+1072, below the 2048-byte ceiling). Debug remains 47512 bytes, versus 45744 (+1768). Both images are byte-identical to Round 3.

Validate with the pinned dependencies:

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

The review packet supplies the unchanged full-suite runner, table-derived plants, grading scripts, per-row receipts and raw XML. From the packet directory, with the source checkout at `source`:

```sh
python3 review-scripts/full_suite_probe.py --repo source --work contract --plants plants_contract.json --jobs 4 --control --out contract-results.json
python3 grade_contract.py --repo source --work .
python3 review-scripts/full_suite_probe.py --repo source --work review-gap --plants review-scripts/plants_gap.json --jobs 2 --out review-gap-results.json
python3 grade_gap.py --repo source --work .
```

The unregistered exploratory clock-cache control is equivalent at this source head and is excluded from the registered campaign. Hosted mutation and wrap assertions complement the RV32 positive-path smoke; they do not establish physical timing or platform integration.
