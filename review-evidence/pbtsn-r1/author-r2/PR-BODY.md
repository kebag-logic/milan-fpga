# PocketBeagle USB bridge: entity configuration and AEM model

Base: `main`. Branch: `pocket-beagle` at 40c3111, with `main` bf02d81 merged. Issue: #42 (AEM-01).

## Why

The PocketBeagle 2 bridge connects a USB host's 24 playback and 24 capture channels to Milan.
It carries them in four AAF streams each way, 8, 8, 4 and 4 channels, plus one CRF stream each way.
Its control plane uses this library's ADP, ACMP and MAAP cores.
This branch adds the bridge's entity facts here, so they are tested on both targets.

## What changes

- **Main merged into the Linux branch.** This brings the ADP seed, ADP discovery and ACMP changed-sink fixes (#38, #40, #41), and #44's exemption of the #41 merge. The branch's own copy of that exemption is resolved into #44's single, documented entry.
- **Entity configuration** (`configs/pocketbeagle.yaml`): one interface, five sources and five sinks, five MAAP addresses, model ID `0x001BC5C52E47A158`. Its generated files are the fifth golden example. Round trips run on Linux and RV32. The plant `entity-dropped-clock-sink` is caught by `EntityYaml.AcmpRoundTrip`.
- **AEM model** (`include/pbaem.h`, AEM-01, issue #42): the bridge's 84 descriptors for a caller identity.
  - Layout: one stream port per AAF stream with mono clusters, static output maps, dynamic inputs (Milan v1.2 5.3.3.9), six clock sources, LOCALE `en-US`.
  - Formats: an AAF input accepts each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU, which includes every 48 kHz Base format (Milan v1.2 6.2, 6.4). The CRF input accepts the CRF format alone (7.3.2).
  - Generator: with the generator's identity, the descriptors equal the image that milan-fpga 58f7673b generates, byte for byte. Their golden CRC, 0xD891CD2F, is checked on both targets.
  - Tests: 100% of lines and branches. 27 planted defects cover every format field, the absent input, full-width identity strings, the caller's model ID and re-initialization.
- **Docs**: `docs/POCKETBEAGLE.md` gives the user view, the design, the golden's provenance and a conformance-by-clause table. It marks the board-side suites that are not yet published. PORTING has the model's contract.

## Review round 2

Every finding of both reviews is closed. Each test finding has a planted defect that is caught.
- AEM-01 traceability now points to #42.
- The format, bound and identity refusals are tested.
- The RV32 gate diagnostics name the AEM model.
- The Milan clause numbers are corrected.
- The LOCALE identifier is `en-US`.
- The #41 exemption is documented, via #44.
- The page states which evidence is not yet published.

## Validation

All of these pass at 40c3111, in a replica of the CI environment (Ubuntu 24.04, Clang 18, GoogleTest 1.14.0):

- `python3 scripts/validate.py --work build-validation --jobs 16`: all 27 gates. The campaign catches all 550 planted defects.
- `python3 scripts/baremetal.py --work build-rv32 --jobs 16`: Debug and Release on QEMU, with the five entity round trips and the AEM golden.
- `python3 scripts/render_graphs.py`: every diagram renders.

## Not in this change

- AECP, counters and SRP for the bridge are in its control firmware and the board support repository. Their suites at this shape are not yet published there.
- No board measurement is claimed here.
