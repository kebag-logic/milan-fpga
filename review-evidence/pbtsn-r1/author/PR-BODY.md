# PocketBeagle USB bridge: entity configuration and AEM model

Base: `main`. Branch: `pocket-beagle` at ef5e5ce (from `dev-linux`, with `main` merged).

## Why

The PocketBeagle 2 bridge connects a USB host's 24 playback and 24 capture channels to Milan.
It carries them in four AAF streams each way, 8, 8, 4 and 4 channels, plus one CRF stream each way.
Its control plane uses this library's ADP, ACMP and MAAP cores.
This branch adds the bridge's entity facts here, so they are tested on both targets.

## What changes

- **Main merged into the Linux branch** (79c4ba8). `dev-linux` was 63 commits behind. The merge brings the ADP seed, ADP discovery and ACMP changed-sink fixes (#38, #40, #41). There were no conflicts.
- **Entity configuration** (`configs/pocketbeagle.yaml`): one interface, five sources and five sinks, five MAAP addresses. The model ID is the bridge's pinned AEM model, `0x001BC5C52E47A158`. Its generated files are the fifth golden example. The ADP, ACMP and MAAP round trips run on Linux and RV32. The plant `entity-dropped-clock-sink` must be caught by `EntityYaml.AcmpRoundTrip`.
- **AEM model** (`include/pbaem.h`, requirement AEM-01): the bridge's 84 descriptors for a caller identity.
  - Layout: one stream port per AAF stream with mono clusters, static output maps, dynamic inputs (Milan v1.2 5.3.3.9), and six clock sources.
  - Formats: AAF inputs accept every 48 kHz base format of 1 to 8 channels (Milan v1.2 6.4). The CRF input accepts the CRF format only (7.3.2).
  - With the board's identity, the descriptors equal the bridge's generated AEM image byte for byte. Their golden CRC is checked on both targets.
  - Coverage is 100% of lines and branches. Fifteen planted defects cover the model.
- **Docs**: `docs/POCKETBEAGLE.md` gives the user view (stream, channel and cluster layout, formats, clock sources) and the design. It includes a conformance-by-clause table and states where each part's evidence lives.
- **Privacy gate**: the merge of #41 is exempted from the one-line rule by its exact commit, as the merge of #29 already is. Its message carries the review record in a second paragraph, so `main` currently fails its own privacy gate. **Owner decision:** accept this exemption, or handle it on `main`.

## Validation

All of these pass on the branch head, in a replica of the CI environment (Ubuntu 24.04, Clang 18, GoogleTest 1.14.0):

- `python3 scripts/validate.py --work build-validation --jobs 16`: all 27 gates. They cover both compilers, sanitizers, 100% coverage, static analysis and all 538 planted defects.
- `python3 scripts/baremetal.py --work build-rv32 --jobs 16`: Debug and Release on QEMU, including the five entity round trips and the AEM golden.
- `python3 scripts/render_graphs.py`: every diagram renders.

## Not in this change

- AECP, counters and SRP for the bridge are in its control firmware and the board support repository, not here. The [PocketBeagle page](docs/POCKETBEAGLE.md) says which suite covers each clause.
- No board measurement is claimed here.
- AEM-01 has no tracked issue yet. The contribution rules want one; please open it, or name the issue to cite.
