Status: REVIEW READY for the desk and entity scope, 2026-11-28 10:47. tsn-c-stack `pocket-beagle` head ef5e5ce. Bridge series `pb-interface/a866/patches-0cb0c07/0001..0007` handed to A865 (reply 4). Board validation not started: it waits for A865's image on <bench-board>.
ETA: board checks with A865 from their install (their ETA 2026-11-29). SRP through the <bench-switch> against the <peer-product-name> by 2026-12-01 midday (owner plan). Soak by 2026-12-02. The qual follows "in time" (owner 10:03).

## tsn-c-stack `pocket-beagle` (local only, nothing pushed)

| Commit | Content |
| --- | --- |
| 79c4ba8 | main 5a07d9b merged into dev-linux 9e1cd60 (first session) |
| aade92b | exact-commit exemption of main's PR 41 merge from the one-line rule (precedent: #29); owner decision flagged |
| 93ef150 | PocketBeagle entity config (5x5, five MAAP addresses), golden, round trips on Linux and RV32, plant, docs/POCKETBEAGLE.md |
| ef5e5ce | `pbaem` AEM model: 84 descriptors, byte-identical to the firmware image; AEM-01; 100% coverage; 15 plants; golden on RV32 |

Final gates in the CI replica: `validate.py` 27/27 (538 plants caught), `baremetal.py` Debug and Release rc 0, graphs 5/5 on the host. Receipts: `receipts/tsn-*-final.json`.

## Bridge (A865's repo, by patch)

Series on 0cb0c07, `make check` 11/11 (`receipts/bridge-check-4x4-rebased-0cb0c07.log`); 18 plants, all killed:

- 0001: datapath fields and the SET_STREAM_FORMAT verdict (Milan 5.4.2.7, 6.4).
- 0002: AECP suite at 4x4.
- 0003: SRP suite.
- 0004: nvm window.
- 0005: dynamic maps, gated on mediad's `maps_supported`.
- 0006: GET_STREAM_INFO REGISTERING.
- 0007: GET_AVB_INFO SRP_ENABLED and the adopted mapping.

## Open, for A865 / the owner

- A865: apply the series. Set `maps_supported` once the listener routes by maps. Commit the 4x4 config (their tree has it uncommitted).
- Owner: accept or replace the PR 41 exemption; open an issue for AEM-01 (no origin yet).
- Board-level evidence (Hive enumeration, 4x4 + CRF streams through the <bench-switch> with SRP, USB bit-exact, 1 h soak, flashable image) is not yet produced by either lane.

## Process

- Two rm slips, both logged late in disk-cleanup.log: an empty build dir, and a stray `rm -rf /dev/null` that could not act as uid 1000 (verified intact).
- Dissolving the clone's git alternates was declined; the CI replica mounts the object store read-only instead.
- No board, bench device or VM touched. Nothing pushed or posted.
