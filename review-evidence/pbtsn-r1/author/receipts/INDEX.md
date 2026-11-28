# Receipts

Private. Not for any public repository.

## Start

- Initial state: clean pocket-beagle at 9e1cd60 (dev-linux); dev-linux never committed to or pushed.
- Main integration: merge 79c4ba8 of origin/main 5a07d9b; no conflicts.
- `gcc-configure.log`: the first session's failed configure (GoogleTest 1.18 on the host, 1.14.0 required).

## Entity model for the board

- `aem-firmware-image-4x4.txt`: every descriptor the firmware generator (milan-fpga 58f7673b) emits for `pb-interface/a866/endstation_pb2_4x4.yaml`.
- `aem-pbaem-4x4.txt`: the same, from tsn-c-stack's `pbaem` with the generator's identity.
- `aem-compare.txt`: 84/84 identical; CRC-32 0x1e668fba over 8105 bytes.

## Bridge (milan-linux, A865's repo, via patches)

- `bridge-aecp-4x4-first.log`: the unmodified AECP suite at 4x4: 97 pass, 10 fail (1x1 expectations only).
- `bridge-srp-netns.log`, `bridge-srp-plants.txt`: my first SRP attachment (superseded by A865's 1124eaf) and its plants.
- `bridge-check-snapshot-f97f1e2.log`: `make check` 10/10 on that snapshot.
- `bridge-check-4x4-e312273.log`: patches 0001..0004 on 10ea9b4, `make check` 11/11.
- `bridge-check-4x4-0005.log`, `bridge-check-4x4-0006.log`: with 0005 and 0006, 11/11.
- `bridge-check-4x4-0007.log`: with 0007 on 10ea9b4, 11/11.
- `bridge-check-4x4-rebased-0cb0c07.log`: 0001..0007 rebased onto 0cb0c07, 11/11.
- `bridge-entity-plants.txt`: 18 planted defects, all killed.

## tsn-c-stack

- `tsn-validate-gates-entity.json`: `validate.py` 27/27 in the CI replica at the entity-config tree.
- `tsn-rv32-results-entity.json`: `baremetal.py` Debug and Release, five entity round trips.
- `tsn-validate-gates-final.json`, `tsn-mutation-results-final.json`: `validate.py` 27/27 at ef5e5ce, 538 plants caught.
- `tsn-rv32-results-final.json`: `baremetal.py` at ef5e5ce, Debug and Release, with the AEM golden.
