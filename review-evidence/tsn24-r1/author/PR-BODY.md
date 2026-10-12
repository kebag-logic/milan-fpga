[A606]
Closes #24

Expose the talker declaration predicate per source: a valid destination and either an accepted probe answer younger than the entity-configured 15000 ms interval or a registered Listener, per Milan v1.2 clause 4.3.3.1. One explicit Listener input updates core state without callbacks. Accepted responses start the wrapping-clock window; queued responses do not. Existing ACMP response behavior is preserved.

The entity generator supplies the interval. The porting guide documents Listener aggregation and regular declaration queries. New tests cover every predicate term, exact expiry, wrap, response backpressure, source/interface isolation and reset. All 363 mutation plants are caught; all 15 added hosted tests have individual physical-removal escapes. Coverage retains the ratchet.

Both hosted configurations and freestanding RV32 Debug/Release pass, as do all 28 validation entries. The Release loadable image grows by 1304 bytes, below the 2048-byte ceiling. Debug grows by 2208 bytes and is informational under the issue ruling.

Validate with the pinned dependencies:

```sh
python3 scripts/entity_yaml.py --examples --check
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```
