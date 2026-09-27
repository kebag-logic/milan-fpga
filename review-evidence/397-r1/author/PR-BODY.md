[A358] Refs #397

## Status

Measurement-only implementation is ready for independent review at
`7f997b60d5a74d46beca5c263d27496ccce0ae4f` on `397-service-budget`, targeting `dev`.
The commit is local. All required local assignment gates passed. The 8x8
scenario has budget findings; successful measurement does not approve timing.

## Linked Issue / roles

Refs #397. The architecture decision and bench liveness proof remain open.

Executor: `[A358]`
Internal reviewer: `[R348]`
External reviewer: `[R349]`

## Description

Adds a sibling harness that runs unchanged product firmware at 50 MHz and
measures boot, AEM copy/CRC, restore, journal operations and every registered
product UART command through external or enclosing markers. Two populated
scenarios each complete 17 command cases and two acknowledged commits.

At 8x8, NVM status reaches 788.87705 ms and the maximum heartbeat gap is
1,449.77764 ms, both exceeding the 500 ms comparison. Tables retain negative
margins. Receipts preserve integer cycles, raw observations and input hashes;
separate device projections use the existing erase and page-program maxima.

## Authoritative references

- Measurement-only assignment in #397, comment 5854787465.
- NFR-SCOUT-01/03, NFR-RES-01, NFR-PORT-01 and REQ-CSR-02.
- Saved-state section 9.4 and the bare-metal build/UART contracts.
- Milan v1.2 section 5.6.3 and IEEE 1722.1-2021 section 9.3.2.6.

## How to get into the same state

Use this branch from base `ac18b50968b12efe4d15c0a06301264b35656b31`, with
pinned submodules initialized. Follow the [committed reproduction recipe](docs/findings/397_SERVICE_BUDGET.md#reproduction-and-evidence)
using separate temporary build directories for both shapes.

## How to validate

Both populated simulations and their bound-log regrades return zero for valid
measurement evidence. The 1x1 scenario has no budget finding; 8x8 retains three
named refusals. All 14 device controls and eight timing/marker controls pass,
including rejection of an over-budget interval and a delayed recorded UART
response. Capture integrity, all 46 feature-status controls, documentation,
source-quality, hygiene and whitespace checks pass. The complete commands
and proof limits are in the reproduction record.

## Known limitations / out of scope

The 8x8 budget findings remain open. Fixed-phase simulation, immediate UART
handshakes and conditional device-limit projections do not establish physical
worst-case timing or the required twofold commit margin. Boot and AEM use an
enclosing interval without an invented numeric deadline. Future duties, the
hart decision, board proof and independent reviews remain outstanding.

## Definition of Done

- [ ] Full issue acceptance, including architecture decision and bench proof
- [x] Self-checking measurement and over-budget controls
- [x] Required local assignment gates recorded for this commit
- [ ] Evidence posted to the eventual review object
- [x] Requirement and interface contracts preserved
- [ ] Positive internal and external independent reviews
- [ ] Blocking findings resolved and re-reviewed
- [ ] Candidate merge and post-merge containment validated
- [x] Measurement method and limitations documented
