[A368]

Closes #580

## Status

Round 2 local work is complete at `d02db63c367daf9adc7d709840bd81077e781d80`. All assigned local gates passed.
Independent re-review remains pending; the local commit has not been pushed.

## Description

Adopt processor `16be6768`, including the body/key type and index refusal from
`493e5e4b`. Record current ROM digests while retaining prior rows, classify the
packer unit test, update F7 and pin references, and regenerate the boundary
diagram. All five configurations retain their AEM images and builder outputs.
Round 2 regenerated all 65 artifacts and matched the public round-1 hash table.

## Round 2

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857045698) corrects the earlier receipt's provenance.
Fresh capture runs measured parent `499b15f97eb0a469b7cd1308fbba7af3c64d1851`, tree
`83b988d3b59a398a7d0cd1977194c50be92522da`, with processor
`16be6768f710e79450aace277abacd6c2c3336e5`. Both shapes ran at 50 MHz, traffic ON/OFF,
with 16 captures per arm, plus the labelled 100 MHz 8x8 comparison: 96 captures.

All rows passed and reproduce the previous numerical results. The 8x8 maximum
is **24.30246 ms**, below the 24.5 ms stop threshold and giving 2.0163× margin
against the 49 ms hold floor. The receipt refreshes provenance, commands and
recomputed digests; snapshot section 18 and the changelog record remeasurement.
Firmware, RTL, harness, copy and hold behaviour are unchanged in this round.

The ownership page states the audit pin historically; the submodule reference
links the processor PRs. The cluster wording records #122's retained Milan
5.3.3.8 minimum and parent
#584's responsibility for the non-conforming zero-cluster 8x8 input pools.

## How to reproduce

Follow the capture README's six-arm offline procedure and the receipt's commands
and environment. Generate all five configurations and pack their AEM overlays
with a 576-byte line limit. Compare with the [published artifact hashes](https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5856703787).

## How to validate

All assigned gates returned rc 0: new capture-receipt check, both complete
86-test builder modes, ROM digest check, test-evidence and port-contract checks,
default wrapper/datapath suites, 33 documentation checks and whitespace checks.
The suites report 2,068 and 11,206 checks respectively, with zero failures.

The existing external calibration arm remains NOT RUN in both builder modes;
the compiler-absent mode also reports the RV32-dependent instruments NOT RUN.
Simulation evidence does not establish physical latency. The 100 MHz point is
non-contract. Full commands and receipts accompany the round-2 issue evidence.

## DoD

- [x] Pin adoption and associated records updated.
- [x] Five-configuration output equality verified.
- [x] Fresh six-arm capture receipt and section 18 complete.
- [x] Assigned documentation findings addressed and local gates passed.
- [ ] Independent re-review and required publication/CI evidence complete.
