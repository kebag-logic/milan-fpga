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

Machine-checked status rows are defined by the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gateware.current-version` | `implemented` | `0x0002_0051` |
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `missing` | - |
| `stream-input.start-stop` | `partial` | - |
| `stream-input.stopped-crf-observation` | `missing` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `partial` | - |
| `notifications.controller-liveness` | `missing` | - |
| `verification.long-gate-policy` | `implemented` | `local-required, remote-optional` |
<!-- milan-feature-status:end -->

## Current verification record

| Gate | Result | Interpretation |
|---|---:|---|
| All 50 `tb/verilator/*/Makefile` suites | PASS | Every suite returned zero. Some suites still print explicit gap messages, so exit status alone is not a compliance verdict. |
| `tb/verilator/hostplane` after ROM fix | PASS | Both `ltn_rom.hex` and `ucode.hex` were generated before simulation. No missing `$readmem` image warning remained. |
| `tb/verilator/pp_shadow` | 273 checks passed | The 2026-08-17 rerun passed with zero failures. Milan `ACQUIRE_ENTITY` is checked on the wire for `NOT_SUPPORTED`, a zero owner, correct length, and correct addressing. The dynamic arty input also passed the GET_AUDIO_MAP body checks. |
| `tests/` Behave suite | 15 features and 338 scenarios passed | 1,615 steps passed with no skipped scenarios or steps in the 2026-08-18 rerun. This is an offline behavior model, not an external compliance lab result. |
| Pinned protocol processor suites | 14,205 checks passed | All 27 processor suites passed. The processor's `pp_top` suite contributes 1,106 passing checks, including the exact 38 through 45 byte foreign-target AECP regression, the configuration overlay's fallback-versus-overlay evidence, GET_DYNAMIC_INFO batch coverage, record-level handling of the complete command-side status byte, getter-length drift detection, and cdl 525 command rejection. It also covers the 63-record mapping command maximum, atomic rejection of 64 mapping records, and exclusion between a reserved mapping edit and an ACMP stream-state transaction. The processor's zero-tolerance RTL lint and documentation gates also passed. |
| Stream Output counter suites | PASS | The diagnostic context passed 83 checks, the AAF NxN harness passed 42 checks, and the CRF transmitter passed 127 checks. Matching 4x4 and 8x8 entity integrations passed 1,278 and 4,326 checks, including every declared AAF and CRF Stream Output. The 8x8 integration also proves locked local mapping writes leave physical RAM and protocol ownership unchanged, then apply after unlock. |
| Official controller decoder | PASS | An actual 174-byte DUT response was decoded by [LA_avdecc v4.3.1 commit `2fd57534`](https://github.com/L-Acoustics/avdecc/tree/2fd57534ec7b32c66d9ada2c833e2c12dd5b95ea) through `protocol::aemPayload::deserializeGetCountersResponse`. It returned descriptor type `0x0006`, descriptor index `0`, valid mask `0x0000001F`, and five counter quadlets. |
| Pinned gPTP processor skeleton | 877 checks passed | 768 uCPU, 31 parser, and 78 engine checks passed. Its own README states that the normative 802.1AS state machines are not implemented, and this submodule is not integrated by the root RTL. |
| Root RTL lint | PASS under ratchet | The ratchet remains at 99 existing warnings. This is not a zero-warning result. |
| Module matrix | PASS | 63 modules, 0 untested under the current matrix rules. |
| End-station builder gates | PASS | The AEM image, identity, shape, and base-format generation gates passed. |
| Documentation gate | PASS | It covered 205 Markdown files with zero findings after the final edits. |
| `tsn-gen` field campaign | 164 checks passed | The AAF/AVTP field campaign reported 164 pass, 0 fail, and 0 known gaps with parser tests disabled. The result came from a working tree of the public generator, not solely from the `TSN_GEN_REV` commit pinned by `.github/workflows/rtl.yml`. CI exercises that pin, but this campaign count is a measured floor rather than a pin-reproducible result. |
| Vivado build and timing closure | NOT RUN | Vivado 2026.1 is not installed in this environment. |
| Current physical Milan interoperability bench | NOT RUN | The external bench repository contains valuable dated evidence, but its present worktree is active and its last recorded audio result used a mismatched peer format. |

The official controller decoder result is reproducible from the tracked DUT
capture without relying on the audit prose. Run:

The full local Verilator and Yosys portability sweeps are required validation
evidence. Their long remote copies are optional and need not delay review after
the local equivalents pass.

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

<!-- milan-feature-fact:served_aem_operations:start -->
The pinned processor currently dispatches or serves `READ_DESCRIPTOR`,
`ACQUIRE_ENTITY`, `LOCK_ENTITY`, `ENTITY_AVAILABLE`, `SET_CONFIGURATION`, `GET_CONFIGURATION`,
`GET_STREAM_FORMAT`, `SET_SAMPLING_RATE`, `GET_SAMPLING_RATE`,
`SET_CLOCK_SOURCE`, `GET_CLOCK_SOURCE`, Identify `SET_CONTROL` and
`GET_CONTROL`, `START_STREAMING`, `STOP_STREAMING`, `GET_STREAM_INFO`,
`IDENTIFY_NOTIFICATION`, `GET_AVB_INFO`, leaf-only `GET_AS_PATH`,
`GET_COUNTERS`, `GET_AUDIO_MAP`, `ADD_AUDIO_MAPPINGS`,
`REMOVE_AUDIO_MAPPINGS`, `GET_DYNAMIC_INFO`,
`REGISTER_UNSOLICITED_NOTIFICATION`, and
`DEREGISTER_UNSOLICITED_NOTIFICATION`.
<!-- milan-feature-fact:served_aem_operations:end -->

<!-- milan-feature-fact:served_mvu_operations:start -->
The served Milan Vendor Unique inventory is `GET_MILAN_INFO`.
<!-- milan-feature-fact:served_mvu_operations:end -->

`GET_DYNAMIC_INFO` implements the IEEE 1722.1-2021 section 7.4.76 fixed-getter
whitelist with a full pre-scan, independent record statuses, silent overflow
omission, continued processing after an omission, and Milan's 56-byte
`GET_STREAM_INFO` record body. Legal getters that are not implemented as
standalone commands receive record-level `NOT_SUPPORTED` with their command
data copied. A forbidden or malformed record rejects the complete command with
`BAD_ARGUMENTS` before any getter is processed.

The mapping pair validates the complete command before its first write, updates
the live map RAM, and reflects every successful command, including an
idempotent ADD, to other registered controllers. Only a changed command marks
persistence dirty. Mapping persistence remains blocked by B2 and #70. The
processor scoreboard holds MAP_CFG from dispatch through RX-slot
retirement and excludes ACMP STREAM_CFG. After the phase-1 output recheck, the
root also reserves every referenced AAF stream until phase 2, so SRP or local
bypass changes cannot start an output between validation and write-back. The
processor R19a and root T66 regressions drive both concurrency paths.

This inventory describes command handling and its integrated media effects at
VERSION `0x0051`. `START_STREAMING` and `STOP_STREAMING` are served from the
ACMP binding record. A stopped AAF Stream Input continues observing and counting
received traffic while discarding its media contribution. The CRF exception is
the issue #97 defect recorded in B12.

The following mandatory surface still falls through to an unimplemented echo
or otherwise lacks the required behavior:

<!-- milan-feature-fact:missing_mandatory_aem_operations:start -->
- `SET_STREAM_FORMAT`
- `SET_STREAM_INFO`
- `SET_NAME` and `GET_NAME`
<!-- milan-feature-fact:missing_mandatory_aem_operations:end -->

Milan v1.2 section 5.4.2 requires these profile behaviors. A correctly formed
`NOT_IMPLEMENTED` response is transport-safe, but it is not implementation of
a mandatory command.

Implementation evidence:
[`KL_aecp_engine.sv`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/07aa250cfc705aefe0b5debc26e324a56e69d1b6/hdl/aecp/KL_aecp_engine.sv),
the packet-level W8 cases in
[`sim_main.cpp`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/07aa250cfc705aefe0b5debc26e324a56e69d1b6/tb/pp_top/sim_main.cpp), and the
current command table in
[`06_aecp_engine.md`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/07aa250cfc705aefe0b5debc26e324a56e69d1b6/docs/architecture/06_aecp_engine.md).

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

### B3. Dynamic clock and sampling-rate state does not reach the media plane

The processor now accepts and stores `SET_CLOCK_SOURCE`, and
[`KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv) now does expose the
dynamic clock-source output to the root integration, where
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) receives it. Nothing
reads it: `CRF_CLK_SELECTED_C` is still a compile-time zero, so the published
selection reaches the datapath and stops there. The CRF Media Clock Input cannot select or steer
the media clock, and the shipping control-plane shape leaves the servo path
idle.

The same boundary applies to `SET_SAMPLING_RATE`: the processor stores the new
descriptor value, but the root media clock, packet grid, and audio engines do
not consume it. A controller can therefore read back a selected rate that the
media plane has not adopted.

This blocks the media-clock behavior required by Milan sections 5.3.5, 5.3.11,
and 7.2.2.

### B4. Counter coverage and notification duty are incomplete

Solicited `GET_COUNTERS` now serves every declared Stream Output with the five
mandatory Milan Table 5.17 counters in the compact quadlet layout. Counter
updates also produce a per-descriptor dirty pulse. The processor notification
block does not yet connect those pulses to the rate-limited `GET_COUNTERS`
notification scheduler, so the full Milan Table 5.22 asynchronous behavior is
not closed.

The declared CRF Media Clock Input is a separate mandatory gap. The root gather
face serves AAF Stream Input indices below `N_STREAMS`, but the appended CRF
Stream Input at index `N_STREAMS` returns an empty mask. Its Table 5.16 counter
outputs and dirty source are unconnected. This leaves the CRF Stream Input
requirements in Milan sections 5.3.8.10 and 5.4.2.25 open.

This also blocks Milan section 5.4.5.2. Solicited reads serve AAF Stream Input,
Stream Output, AVB Interface, and Clock Domain counters. The CRF Stream Input
and the Table 5.22 notification path remain open under section 5.4.2.25.

### B5. Registered-controller liveness monitoring is absent

The processor stores unsolicited-notification registrations and applies the
time-limited expiry policy, but it does not originate the random 30 to 60 s
`CONTROLLER_AVAILABLE` monitor required by Milan section 5.4.5.3. It therefore
cannot retry the probe once, re-arm the monitor on any response status, or
remove a silent controller and send the targeted deregistration notification.

This is a mandatory controller-liveness gap, separate from the Table 5.22
counter-change notification producer in B4.

### B6. Multi-bridge AS_PATH reporting is incomplete

The root gather face serves `GET_AS_PATH` as a zero-entry response when no
grandmaster is known, or as a one-entry response containing only the
grandmaster identity. The CSR PathTrace staging group stores and reads back a
tail, but the root leaves its path, count, and generation outputs disconnected.
The processor therefore never receives the traversed bridge identities.

This leaf-only behavior is useful but incomplete. A topology with one or more
bridges is reported without those bridges, so the mandatory IEEE 1722.1 path
semantics used by Milan are not closed.

Evidence: the disconnected `o_asp_path`, `o_asp_count`, and `o_asp_gen` ports
and the `GET_AS_PATH` gather selection in
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv), plus the staging
status in [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md).

### B7. Identify control has no public indication

The processor accepts Identify `SET_CONTROL` and stores its dynamic value, but
`KL_pp_shadow.sv` exports that value to the root wire
`pp_aecp_identify_w`. Nothing consumes the wire and the public `o_identify`
output is tied low, so no board indication can follow the control.

Evidence: the `o_identify` assignment in
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv).

### B8. GET_AVB_INFO omits the measured propagation delay

Software can publish the measured neighbor propagation delay through
`GPTP_PDELAY` at `0x6E4`, but the processor gather face does not consume that
CSR. `GET_AVB_INFO` always returns zero for `propagation_delay`, even when the
stored measurement is nonzero. This leaves the network-interface state
required by Milan section 5.3.6.1 and the mandatory section 5.4.2.23 response
incomplete.

Evidence: the `GET_AVB_INFO` gather selection in
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) and the `GPTP_PDELAY`
entry in [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md).

### B9. The debug bypass can defeat talker admission

`AAF_CTRL[1]` is an explicit bring-up escape hatch that bypasses both the ACMP
and SRP admission terms. It resets clear, but software can still enable it and
transmit without the Milan section 5.3.7.3 listener and reservation license.
Any conforming deployment must keep this control clear; its writable presence
remains a structural conformance defect.

Evidence: the admission composition graded by
[`milan_streaming_licence.feature`](../../tests/features/milan_streaming_licence.feature).

### B10. The physical media clock and packet grid are not proven aligned

The true-ratio simulation measures the TDM frame clock at about 10.6 ppm below
the exact 48 kHz packet grid. The test currently passes by proving that the two
grids are not aligned and reports the result as an open finding. The selectable
CRF clock blocker prevents the intended closed-loop correction from being
exercised in the current integration.

Evidence: [`sim_aclk.cpp`](../../tb/verilator/milan_dp/sim_aclk.cpp).

### B11. Required external evidence is missing

No current Vivado place-and-route, timing report, bitstream build, physical
peer-format-matched audio run, long-duration gPTP run, or external lab run
was produced in this audit. Automated simulation cannot establish electrical,
clock-recovery, timing-closure, switch-interaction, or long-duration behavior.

### B12. Stream Input START/STOP behavior is partial; persistence is open

The ACMP binding record is the single source of truth for the Stream Input
started state. `START_STREAMING` and `STOP_STREAMING` update that record, and
the AECP dynamic store's selector 6 is retired. A started Stream Input processes
its AVTPDUs. A stopped AAF input continues receiving, classifying, and counting
them while discarding their media contribution. The datapath suite also proves
a STOP/START pair does not forge a binding edge or reset the Stream Input
counters.

Two correctness defects keep this behavior partial under issue #97. The AECP
response can report `SUCCESS` after holder acceptance but before the record
walker commits the state. The CRF stopped predicate is also applied at the CRF
receive frame strobe, so stopped CRF traffic is hidden from observation and
counters instead of being observed while only timing consumption is suppressed.

Milan Section 5.3.8.7 also requires this state to be saved in nonvolatile memory
and restored after a power cycle. The record projects and restores the bit, but
`KL_pp_shadow` sets `NVM_BACKED_C = 1'b0` behind a blank-flash stub, so no
shipping build persists it. Issue #70 owns that remaining requirement.

Evidence: the command inventory in the pinned processor and the integrated
media gate in [`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv).

## Corrections made by this audit

1. The host-plane suite now generates both processor ROM images before any
   simulator starts. Verilator otherwise warns and continues with an all-zero
   ROM, which allowed false-green integration runs.
2. The root processor integration now grades Milan `ACQUIRE_ENTITY` instead of
   printing a stale unconditional gap.
3. The repository README now describes the current VERSION `0x0002_0051`
   control-plane surface and the remaining blockers.
4. First-line-obsolete documents are no longer current authorities. Current
   entry points route compliance verdicts to this audit and the generated
   module matrix.
5. Stream Output counters now use Milan Table 5.17's compact mask and quadlet
   layout through the solicited processor path.
6. Packet-completion metadata now freezes the `tu` bit carried by each AAF and
   CRF PDU. `TIMESTAMP_UNCERTAIN` therefore counts transmitted wire state, not
   a later live clock verdict.
7. Every served Stream Output counter update, including a healthy `FRAMES_TX`
   interval, asserts the raw per-descriptor dirty source. Rate limiting and
   notification coalescing remain the scheduler work identified in B4. The CRF
   Stream Input counter and dirty connections remain open.
8. The integration proof now boots each simulation with its matching entity
   image, checks every declared output, rejects the first undeclared output
   with a full empty response body, and exercises real AAF and CRF enable
   surfaces. The standalone diagnostic suite proves unique per-index state,
   reset behavior, and 32-bit wrap.
9. The CI checkout uses anonymous HTTPS for both required submodules, and all
   jobs that consume the processor initialize it explicitly.

## Release rule

Do not remove the **not compliant** verdict until all B1 through B12 items have
current evidence. A green regression is necessary, but it is not sufficient.
The final review must include a synchronized clause matrix, zero unresolved
mandatory rows, a successful bitstream and timing build, a matched-format
physical interoperability run, and the intended external conformance process.
