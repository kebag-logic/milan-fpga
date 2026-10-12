[A606]
Closes #24

Expose the talker declaration predicate per source: a valid destination and either an accepted probe answer younger than the entity-configured 15000 ms interval or a registered Listener, per Milan v1.2 clause 4.3.3.1. One explicit Listener input updates core state without callbacks. Accepted responses start the wrapping-clock window; queued responses do not. Existing ACMP response behavior is preserved.

## Round 2

The generated-entity round trip checks configuration propagation and one successful freshness path on both targets. Individual core tests retain the predicate terms, exact expiry edge and wrap checks. The earlier removal claim covered individual binaries; the replacement evidence runs all eight hosted binaries. Each of the 15 existing freshness plants and both new plants is caught with its named test present and escapes after only that test is physically deleted: 418 completed test instances become 417. Both supplied review scripts were rerun unchanged; a supplemental complete-suite check covers physical removal of the entity test and grades fresh XML receipts.

Zero disables probe demand while a registered Listener still opens the gate. The registered zero-interval mutant protects that contract. Initialization refuses intervals at or above 2^31 ms without modifying the instance or calling ports. Positive-window plants preserve zero semantics to keep their individual necessity proofs. The port guide uses the requested acceptance-point attribution, and the configuration table lists all four plants.

All 28 validation entries pass, including GCC, Clang sanitizers, coverage, contracts, conditional matrix, traceability, inventory and the 365-plant mutation campaign. All plants are caught with zero escapes or errors. ACMP coverage is 792/792 lines and 392/392 branches. Freestanding RV32 Debug and Release both link and execute their smoke checks. The Release loadable image grows from 35792 to 36864 bytes (+1072), below the 2048-byte ceiling; Debug grows from 45744 to 47512 bytes (+1768).

Validate with the pinned dependencies:

```sh
python3 scripts/entity_yaml.py --examples --check
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

## Round 3

Protect the documented expiry latch while a registered Listener or invalid destination hides probe demand. Two tests service queries at gaps no larger than 1000000000 ms, below the 2^31 ms contract, and advance through `2^32 + 100` ms after one answer. Withdrawing the Listener or restoring destination validity must leave the gate closed even though the counter aliases a fresh 100 ms age. Production code is unchanged.

Both supplied expiry-suppression plants are registered with separate named killers. The unchanged gap script reports both CAUGHT; the unchanged physical-removal script reports `escapes: true` for each. Fresh complete-suite XML verifies 420 completed instances with exactly the named failure, and 419 after physically deleting only that test, across all eight binaries with no skips. The five original acceptance-term plants retain their individual catches and filtered escapes. TESTS and TRACEABILITY are regenerated.

All 28 validation entries return 0. The full 367-plant campaign has zero escapes or errors; ACMP coverage remains 792/792 lines and 392/392 branches with no new exclusions. Both freestanding configurations pass. Their loadable images match Round 2 byte for byte: Release 36864 bytes (+1072 from main), Debug 47512 bytes (+1768 from main), with zero growth this round. Post-commit privacy passes.

Validation commands above apply to this final source head. The wrap assertions execute in the hosted suite; the bare-metal smoke retains the generated positive freshness path. Physical timing and platform integration remain separate validation work.
