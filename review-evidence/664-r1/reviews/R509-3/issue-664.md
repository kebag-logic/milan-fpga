**Owner decision, 2026-10-05** (discussion recorded on #640, comments 5991591637 to 5991745829). This is the **Mark II pivot**. It starts **after the protocol-processor program is finished** (the PP issues of program #415).

## Architecture the requirements must describe

- **ADP, ACMP, MAAP and SRP** run on the bare-metal software core, as the default Mark II use case.
- The fabric and the core exchange those protocols through **several packet mailboxes**.
- The fabric keeps:
  - framing and timestamps;
  - the gPTP plane;
  - the AECP engine and notifications (unless the owner rules otherwise);
  - an **ingress filter**, so the core receives only what it must act on.
- The **all-fabric build stays supported**. Placement is chosen per function at build time, and moving between the two must be easy.
- The software core **reads the saved entity state from the flash and applies it** at boot.
- The mailbox interface **ports from the RISC-V soft core to a hard core**:
  - block RAM rings, a doorbell and one interrupt;
  - 32-bit accesses only, no DMA;
  - a bus adapter per host;
  - portable C behind a small HAL;
  - one YAML contract that generates the fabric module, the C header and the documentation.

## Requirement changes

- `REQUIREMENTS.md` section 1 (product ownership): fabric MAAP and IEEE 1722.1 processing become build-selectable placements.
- `docs/reference/FR_NFR.md`:
  - **NFR-SCOUT-01**: the single control hart and how stream capacity grows.
  - **NFR-SCOUT-02**: who owns protocol control.
  - **NFR-SCOUT-03**: replace "never on firmware service latency" for ADP, ACMP, MAAP and SRP with a bounded firmware service latency inside each normative timeout, stated and tested per path. Audio and gPTP deadlines stay fabric-only.
  - The rows they trace to.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md`: the ownership rule for each placement.
- The traceability matrix and every document that cites these rows.

## Version: major 3

The **VERSION major moves to 3** so the new architecture is identifiable. This follows the versioning policy (`docs/reference/REGISTER_MAP.md`, VERSION row: a MAJOR is an entire redesign of blocks):
- `0x0003` opens the Mark II split era;
- MINOR stays flat and continuous across majors;
- the firmware string reads 3.<minor>.<patch>.

The landing follows the VERSION chain: pin **all five** simulations, including the `>> 16` major check in `tb/verilator/hostplane`, then the CSR documentation and the changelog.

## Acceptance

1. The requirement and architecture documents describe the split as the default and the all-fabric build as a supported option, with no contradiction left in the tree. The documentation gates pass.
2. Each moved function's timing obligation is stated as a bounded firmware service latency with a test hook defined.
3. VERSION reads `0x0003_xxxx` and the firmware string reads 3.x.x, with all five simulations and the CSR documentation pinned and green.
4. Reviewed as a normal PR with two reviews. The owner approves the requirement text before merge.

Relates to #640 and milestone 13.

