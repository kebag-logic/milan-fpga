# Fabric and bare-metal firmware ownership

This page defines the supported product boundary at VERSION `0x0002_0056`.
The AX7101 image contains one RV32I bare-metal firmware and a fabric-owned
Milan datapath/control plane. There is no alternate product runtime.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gptp.fabric-product-owner` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. Ownership rule](#1-ownership-rule)** — Separates deterministic wire-time fabric work from bare-metal policy and diagnostics.
- **[2. Boot sequence](#2-boot-sequence)** — Orders identity, AEM verification and entity enable without a second runtime.
- **[3. Fabric publication boundary](#3-fabric-publication-boundary)** — Defines the atomic gPTP and protocol-processor state consumed by public faces.
- **[4. Verification-only option OFF](#4-verification-only-option-off)** — Documents the buildable but unshippable zero-owner comparison form.
- **[5. Known incomplete boundaries](#5-known-incomplete-boundaries)** — Lists persistence and physical-evidence work that remains open.
- **[6. Verification boundary](#6-verification-boundary)** — Maps digital gates and physical acceptance to their respective claims.

## 1. Ownership rule

State has one authoritative owner. Firmware performs finite boot and
management transactions; continuous packet, timing, and protocol behavior
stays in fabric.

| Function | Owner | Contract |
|---|---|---|
| Boot policy and image pairing | bare-metal firmware | Accept only the generated bitstream/AEM pair and keep the entity disabled if verification fails |
| Identity and static product policy | bare-metal firmware | Program generated entity/MAC values once during boot |
| UART diagnostics | bare-metal firmware | Report image identity, control enables, PHC movement, and the fabric gPTP publication |
| Required saved state | bare-metal firmware plus NVM backend | Not complete: the blank-flash backend in #70 remains a release blocker |
| PHC, gPTP protocol, servo, BMCA, and peer delay | fabric | The integrated gPTP engine is the sole product clock owner |
| GM, parent, PathTrace, peer delay, sync, and asCapable publication | fabric | One atomic selected-state bank feeds every public consumer |
| AVTP `tu` decision | fabric | `KL_ptp_clock_validity` combines fabric sync with same-edge discontinuity holdover |
| ADP, AECP/AEM, ACMP, and SRP | fabric | The pinned protocol processor owns the served protocol state; MAAP remains in the root fabric |
| Classification, queues, CBS, timestamping, AAF/CRF, and audio routing | fabric | Per-frame behavior has no firmware round trip |
| External measurement and artifact packaging | bench workstation | Host tools observe the board; they are not part of the product image |

## 2. Boot sequence

1. The FPGA configures from the paired QSPI bitstream.
2. RV32I firmware validates CSR identity and holds ADP/protocol advertising
   disabled.
3. Firmware programs generated identity and static product policy.
4. Firmware checks the generated AEM image in its dedicated QSPI slot, copies
   the exact bytes into the processor descriptor window, and verifies the
   generated CRC.
5. Only a valid descriptor image permits the entity enable bits to be set.
6. UART remains available for identity, image, PHC, and fabric-publication
   diagnostics.

The gPTP engine and PHC are live independently of descriptor enumeration. A
missing AEM image disables entity advertising; it does not introduce another
time owner.

## 3. Fabric publication boundary

The fabric gPTP engine commits GM, parent identity, PathTrace, peer delay,
sync, asCapable, and discontinuity as one selected-owner transaction. That
transaction feeds:

- CSR `0x624/0x628`, `0x6E4`, `0x730/0x734`, `0x77C`, and `0x7E4`;
- ADP and AECP `GET_AVB_INFO` / `GET_AS_PATH` answers;
- Table 5.22 observed-change notification signatures; and
- the AVTP `tu` verdict used by every talker.

The 64-bit GM and parent CSR pairs snapshot on the first half-read and remain
coherent through the complementary half. Path count/tail publication is
atomic, so an in-flight protocol answer is wholly old or wholly new.

## 4. Verification-only option OFF

`GPTP_PLANE_EN_P=0` exists only to elaborate and test the hardware boundary.
It has no flashable product image and no runtime clock owner:

- GM, parent, PathTrace, and peer delay read zero;
- sync and asCapable are zero;
- AVTP `tu` is one;
- the retired publication/control addresses stay mapped but read zero and
  ignore writes; and
- attempted writes cannot trigger a notification, counter, or owner change.

This form is a negative control, not a second supported architecture.

## 5. Known incomplete boundaries

- #70: the protocol processor NVM face still has no persistent backend.
- #117: exact-candidate two-board gPTP, GM transition, wire, and audio evidence has
  not been recorded.
- Media clock-source selection is stored and reported, but the audio clock
  plane does not yet consume it.
- #64 and #213 retain their physical timestamp-latency measurements.

These gaps are tracked in the canonical
[`reference/MILAN_FEATURE_STATUS.md`](reference/MILAN_FEATURE_STATUS.md).

## 6. Verification boundary

Desk acceptance combines builder/elaboration checks, CSR and clock-validity
benches, the full datapath/N×N matrix, protocol-processor suites, lint,
portable synthesis, documentation/path checks, and the repository-wide
bare-metal policy gate. Physical requirements remain open until their owning
issues contain exact hashes, image identities, topology, raw captures, and
measured verdicts.
