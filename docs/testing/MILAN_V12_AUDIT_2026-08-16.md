# Milan v1.2 implementation audit, 2026-08-16

## Contents

- **[Verdict](#verdict)** -- Release-level compliance conclusion and declared scope.
- **[Current verification record](#current-verification-record)** -- Automated, decoder, build, and physical evidence available for this audit.
- **[Structural compliance blockers](#structural-compliance-blockers)** -- Mandatory work that remains before a compliant release can be claimed.
- **[Corrections made by this audit](#corrections-made-by-this-audit)** -- False-green fixes and verification improvements completed during the audit.
- **[Release rule](#release-rule)** -- Evidence required before the noncompliance verdict can change.

## Verdict

The tree reviewed by this audit is **not fully compliant with Milan v1.2**.
It must not be represented as a conformant or formally approved release.

The automated RTL and software gates are broadly green, and this audit closed
two false-green documentation and verification defects. Those results do not
override the structural blockers listed below.

The normative source used for this review is the consolidated Milan v1.2 Final
Approved specification dated 2023-11-30 from the local standards archive.

The target is the non-redundant PAAD profile. Milan chapter 8 redundancy is
outside this build's declared scope.

## Current verification record

| Gate | Result | Interpretation |
|---|---:|---|
| All 50 `tb/verilator/*/Makefile` suites | PASS | Every suite returned zero. Some suites still print explicit gap messages, so exit status alone is not a compliance verdict. |
| `tb/verilator/hostplane` after ROM fix | PASS | Both `ltn_rom.hex` and `ucode.hex` were generated before simulation. No missing `$readmem` image warning remained. |
| `tb/verilator/pp_shadow` | PASS | Milan `ACQUIRE_ENTITY` is now checked on the wire for `NOT_SUPPORTED`, a zero owner, correct length, and correct addressing. |
| `tests/` Behave suite | 15 features, 321 scenarios passed, 1 scenario skipped | 1,522 steps passed and 4 steps were skipped. This is an offline behavior model, not an external compliance lab result. |
| Pinned protocol processor suites | 13,504 checks passed | All 27 processor suites passed. The processor's zero-tolerance RTL lint and documentation gates also passed. |
| Stream Output counter suites | PASS | The diagnostic context passed 83 checks, the AAF NxN harness passed 42 checks, and the CRF transmitter passed 127 checks. Matching 4x4 and 8x8 entity integrations passed 1,255 and 3,759 checks, including every declared AAF and CRF Stream Output. |
| Official controller decoder | PASS | An actual 174-byte DUT response was decoded by [LA_avdecc v4.3.1 commit `2fd57534`](https://github.com/L-Acoustics/avdecc/tree/2fd57534ec7b32c66d9ada2c833e2c12dd5b95ea) through `protocol::aemPayload::deserializeGetCountersResponse`. It returned descriptor type `0x0006`, descriptor index `0`, valid mask `0x0000001F`, and five counter quadlets. |
| Pinned gPTP processor skeleton | 799 checks passed | 768 uCPU checks and 31 parser checks passed. Its own README states that the normative 802.1AS state machines are not implemented, and this submodule is not integrated by the root RTL. |
| Root RTL lint | PASS under ratchet | The ratchet remains at 100 existing warnings. This is not a zero-warning result. |
| Module matrix | PASS | 63 modules, 0 untested under the current matrix rules. |
| End-station builder gates | PASS | The AEM image, identity, shape, and base-format generation gates passed. |
| Documentation gate | PASS | It covered 204 Markdown files with zero findings after the final edits. |
| Pinned `tsn-gen` field campaign | 164 checks passed | The public generator revision pinned in `.github/workflows/rtl.yml` was built with parser tests disabled; the AAF/AVTP field campaign reported 164 pass, 0 fail, and 0 known gaps. |
| Vivado build and timing closure | NOT RUN | Vivado 2026.1 is not installed in this environment. |
| Current physical Milan interoperability bench | NOT RUN | The external bench repository contains valuable dated evidence, but its present worktree is active and its last recorded audio result used a mismatched peer format. |

The official controller decoder result is reproducible from the tracked DUT
capture without relying on the audit prose. Run:

```console
scripts/verify_la_avdecc_counters.sh
```

The script checks out LA_avdecc v4.3.1 at commit `2fd57534`, builds its static
library, and calls `deserializeGetCountersResponse` on
[`stream_output_counters_response.hex`](../../tb/verilator/milan_dp/reference/stream_output_counters_response.hex).
The fixture is the 174-byte response written by the NxN DUT harness when
`MILAN_COUNTER_FRAME_OUT` names an output file. Set `LA_AVDECC_DIR` to an
existing checkout at the pinned commit for an offline rerun.

## Structural compliance blockers

### B1. The mandatory AECP command set is incomplete

The pinned processor currently gives real behavior to `READ_DESCRIPTOR`,
`ACQUIRE_ENTITY`, `LOCK_ENTITY`, `ENTITY_AVAILABLE`, `SET_CONFIGURATION`, `GET_CONFIGURATION`,
`GET_STREAM_FORMAT`, `SET_SAMPLING_RATE`, `GET_SAMPLING_RATE`,
`SET_CLOCK_SOURCE`, `GET_CLOCK_SOURCE`, Identify `SET_CONTROL` and
`GET_CONTROL`, `GET_STREAM_INFO`, `GET_AVB_INFO`, `GET_AS_PATH`,
`GET_COUNTERS`, `GET_AUDIO_MAP`, the unsolicited registration pair, and Milan
`GET_MILAN_INFO`.

The following mandatory surface still falls through to an unimplemented echo
or otherwise lacks the required behavior:

`START_STREAMING` and `STOP_STREAMING` (Milan 5.4.2.19 / 5.4.2.20) belong in
this list and are called out here because an earlier revision of this document
placed them in the list above. They were implemented and then **withdrawn**
before merge: started/stopped already has a home in the ACMP binding record,
which clears on unbind and is persisted, and a second copy in the AECP dynamic
store would be neither. The work is preserved on branch
`78-start-stop-streaming` pending that decision.

- `SET_STREAM_FORMAT`
- `SET_STREAM_INFO`
- `SET_NAME` and `GET_NAME`
- `ADD_AUDIO_MAPPINGS` and `REMOVE_AUDIO_MAPPINGS`
- `GET_DYNAMIC_INFO`

Milan v1.2 section 5.4.2 requires these profile behaviors. A correctly formed
`NOT_IMPLEMENTED` response is transport-safe, but it is not implementation of
a mandatory command.

Implementation evidence:
[`KL_aecp_engine.sv`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/82281d550f04b78089d6445fc039d01ab231ddf0/hdl/aecp/KL_aecp_engine.sv) and
the current command table in
[`06_aecp_engine.md`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/82281d550f04b78089d6445fc039d01ab231ddf0/docs/architecture/06_aecp_engine.md).

### B2. Required state is not persistent

The integration intentionally exposes a blank-flash responder. The verified
reset result is `nvm_backed = 0`, `nvm_blank = 1`, and `restore_fail = 1`.
Bindings and the other Milan-specified dynamic state therefore do not survive
a power cycle.

This blocks the persistence requirements in Milan sections 5.3.6, 5.3.8,
5.3.11, 5.3.13, and the saved-state connection behavior in section 5.5.

Evidence: the `[P] saved state` checks in
[`sim_main.cpp`](../../tb/verilator/pp_shadow/sim_main.cpp) and the device face
in [`KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv).

### B3. The CRF media clock cannot be selected

The processor now accepts and stores `SET_CLOCK_SOURCE`, and
[`KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv) now does expose the
dynamic clock-source output to the root integration, where
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) receives it. Nothing
reads it: `CRF_CLK_SELECTED_C` is still a compile-time zero, so the published
selection reaches the datapath and stops there. The CRF Media Clock Input cannot select or steer
the media clock, and the shipping control-plane shape leaves the servo path
idle.

This blocks the media-clock behavior required by Milan section 7.2.2.

### B4. The full counter notification duty is incomplete

Solicited `GET_COUNTERS` now serves every declared Stream Output with the five
mandatory Milan Table 5.17 counters in the compact quadlet layout. Counter
updates also produce a per-descriptor dirty pulse. The processor notification
block does not yet connect those pulses to the rate-limited `GET_COUNTERS`
notification scheduler, so the full Milan Table 5.22 asynchronous behavior is
not closed.

This blocks Milan section 5.4.5.2. Solicited reads satisfy the Stream Output
portion of section 5.4.2.25.

### B5. The physical media clock and packet grid are not proven aligned

The true-ratio simulation measures the TDM frame clock at about 10.6 ppm below
the exact 48 kHz packet grid. The test currently passes by proving that the two
grids are not aligned and reports the result as an open finding. The selectable
CRF clock blocker prevents the intended closed-loop correction from being
exercised in the current integration.

Evidence: [`sim_aclk.cpp`](../../tb/verilator/milan_dp/sim_aclk.cpp).

### B6. Required external evidence is missing

No current Vivado place-and-route, timing report, bitstream build, physical
peer-format-matched audio run, long-duration gPTP run, or external lab run
was produced in this audit. Automated simulation cannot establish electrical,
clock-recovery, timing-closure, switch-interaction, or long-duration behavior.

## Corrections made by this audit

1. The host-plane suite now generates both processor ROM images before any
   simulator starts. Verilator otherwise warns and continues with an all-zero
   ROM, which allowed false-green integration runs.
2. The root processor integration now grades Milan `ACQUIRE_ENTITY` instead of
   printing a stale unconditional gap.
3. The repository README now describes the current VERSION `0x0002_004E`
   control-plane surface and the remaining blockers.
4. Documents whose August 13 status text materially contradicts the current
   processor pin are marked `[OBSOLETE + 2026-08-16]` at the top.
5. Stream Output counters now use Milan Table 5.17's compact mask and quadlet
   layout through the solicited processor path.
6. Packet-completion metadata now freezes the `tu` bit carried by each AAF and
   CRF PDU. `TIMESTAMP_UNCERTAIN` therefore counts transmitted wire state, not
   a later live clock verdict.
7. Every counter update, including a healthy `FRAMES_TX` interval, asserts the
   raw per-descriptor dirty source. Rate limiting and notification coalescing
   remain the scheduler work identified in B4.
8. The integration proof now boots each simulation with its matching entity
   image, checks every declared output, rejects the first undeclared output
   with a full empty response body, and exercises real AAF and CRF enable
   surfaces. The standalone diagnostic suite proves unique per-index state,
   reset behavior, and 32-bit wrap.
9. The CI checkout uses anonymous HTTPS for both required submodules, and all
   jobs that consume the processor initialize it explicitly.

## Release rule

Do not remove the **not compliant** verdict until all B1 through B6 items have
current evidence. A green regression is necessary, but it is not sufficient.
The final review must include a synchronized clause matrix, zero unresolved
mandatory rows, a successful bitstream and timing build, a matched-format
physical interoperability run, and the intended external conformance process.
