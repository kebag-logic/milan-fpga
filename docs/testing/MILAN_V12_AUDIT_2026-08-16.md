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
| `gateware.current-version` | `implemented` | `0x0002_0055` |
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `stream-input.start-stop` | `implemented` | - |
| `stream-input.stopped-crf-observation` | `implemented` | - |
| `stream-format.set` | `implemented` | - |
| `stream-info.set-acc-lat` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
| `verification.long-gate-policy` | `implemented` | `local-required, remote-required` |
<!-- milan-feature-status:end -->

## Current verification record

This is the dated record for the audit revision named in this file, not
merge evidence for a later candidate. A repaired candidate must rerun every
applicable gate at its exact parent and submodule SHAs and report those fresh
counts in the pull request; counts in this table must not be carried forward.

| Gate | Result | Interpretation |
|---|---:|---|
| All 50 `tb/verilator/*/Makefile` suites | PASS | Every suite returned zero. Some suites still print explicit gap messages, so exit status alone is not a compliance verdict. |
| `tb/verilator/hostplane` after ROM fix | PASS | Both `ltn_rom.hex` and `ucode.hex` were generated before simulation. No missing `$readmem` image warning remained. |
| `tb/verilator/pp_shadow` | 273 checks passed | The 2026-08-17 rerun passed with zero failures. Milan `ACQUIRE_ENTITY` is checked on the wire for `NOT_SUPPORTED`, a zero owner, correct length, and correct addressing. The dynamic arty input also passed the GET_AUDIO_MAP body checks. |
| `tests/` Behave suite | 15 features and 334 scenarios passed | 1,571 steps passed with no skipped scenarios or steps in the 2026-08-18 rerun (the unimplemented-echo outline is retired: since 0x0002_0054 no mandatory command falls through to it). This is an offline behavior model, not an external compliance lab result. |
| Pinned protocol processor suites | 14,507 checks passed | All 27 processor suites passed. The processor's `pp_top` suite contributes 1,180 passing checks, including the START/STOP completion boundary read with no post-response delay, the exact 38 through 45 byte foreign-target AECP regression, the configuration overlay's fallback-versus-overlay evidence, GET_DYNAMIC_INFO batch coverage, record-level handling of the complete command-side status byte, getter-length drift detection, cdl 525 command rejection, and the stream-setter families: SET_STREAM_FORMAT's per-descriptor running refusal against a really bound sink and really streaming output, the one-gather format verdict in both refusal directions, SET_STREAM_INFO's 2021-only length rule with the 2013-size negative pinned, and the per-row settings publication graded beside every echo, plus the name-access family (the generated name table walked byte-exact, SET/GET/READ_DESCRIPTOR coherence, and the lock refusal carrying the current name). It also covers the 63-record mapping command maximum, atomic rejection of 64 mapping records, and exclusion between a reserved mapping edit and an ACMP stream-state transaction. The processor's zero-tolerance RTL lint and documentation gates also passed. |
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
evidence. The `dev merge bar` ruleset separately requires their stable remote
aggregate contexts, so neither result substitutes for the other.

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
`SET_STREAM_FORMAT`, `GET_STREAM_FORMAT`, `SET_NAME`, `GET_NAME`,
`SET_SAMPLING_RATE`, `GET_SAMPLING_RATE`,
`SET_CLOCK_SOURCE`, `GET_CLOCK_SOURCE`, Identify `SET_CONTROL` and
`GET_CONTROL`, `START_STREAMING`, `STOP_STREAMING`, `SET_STREAM_INFO`,
`GET_STREAM_INFO`,
`IDENTIFY_NOTIFICATION`, `GET_AVB_INFO`, `GET_AS_PATH` (grandmaster plus the
atomically published PathTrace tail),
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
VERSION `0x0053`. `START_STREAMING` and `STOP_STREAMING` are served from the
ACMP binding record and complete at it. A stopped Stream Input - AAF and CRF
alike - continues observing and counting received traffic while discarding its
media contribution (B12).

`SET_STREAM_FORMAT` and `SET_STREAM_INFO` are served with their Milan 5.4.2.7
and 5.4.2.9 refusals: the per-descriptor `STREAM_IS_RUNNING` route (a bound
Stream Input or a streaming Stream Output), whole-command `NOT_SUPPORTED` on
any sub-flag beside MSRP_ACC_LAT_VALID, `BAD_ARGUMENTS` on a bit-31 offset,
and one integrator verdict on the proposed format that admits the addressed
row's declared base: the 48 kHz channel family for inputs, the row's own
declared shape for outputs and the advertised CRF format per direction for
the CRF rows, refusing any format that orphans a mapping-referenced channel. The set offset feeds the transit entries the
AAF and CRF framers stamp, and the set format is served as current and drives
Stream Input 0's acceptance filter. The wire framers do not yet re-shape from
a stored format; that deferral follows the `SET_CONFIGURATION` pattern and is
recorded with B3's media-plane scope.

The following mandatory surface still falls through to an unimplemented echo
or otherwise lacks the required behavior:

<!-- milan-feature-fact:missing_mandatory_aem_operations:start -->
None. Every operation Milan v1.2 mandates for this profile is served since
VERSION 0x0002_0054 (the stream setters at 0x0053, name access at 0x0054).
<!-- milan-feature-fact:missing_mandatory_aem_operations:end -->

Milan v1.2 section 5.4.2 requires these profile behaviors. A correctly formed
`NOT_IMPLEMENTED` response is transport-safe, but it is not implementation of
a mandatory command.

Implementation evidence:
[`KL_aecp_engine.sv`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/a25b5cc9794b8e7f70f738548f4d674e9669b469/hdl/aecp/KL_aecp_engine.sv),
the packet-level command cases in
[`sim_main.cpp`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/a25b5cc9794b8e7f70f738548f4d674e9669b469/tb/pp_top/sim_main.cpp), and the
current command table in
[`06_aecp_engine.md`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/a25b5cc9794b8e7f70f738548f4d674e9669b469/docs/architecture/06_aecp_engine.md).

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

### B4. CRF Stream Input counter coverage remains incomplete

Solicited `GET_COUNTERS` now serves every declared Stream Output with the five
mandatory Milan Table 5.17 counters in the compact quadlet layout. Counter
updates also produce a per-descriptor dirty pulse, and since 0x0002_0055 the
root serialises those pulses (AAF Stream Inputs, Stream Outputs, the AVB
Interface and the Clock Domain) through a lossless round-robin onto the
processor's counter-change face, whose scheduler pushes `GET_COUNTERS` at most
once per descriptor per second. The Table 5.22 asynchronous behavior is closed
for every descriptor the solicited face serves.

The declared CRF Media Clock Input is a separate mandatory gap. The root gather
face serves AAF Stream Input indices below `N_STREAMS`, but the appended CRF
Stream Input at index `N_STREAMS` returns an empty mask. Its Table 5.16 counter
outputs and dirty source are unconnected. This leaves the CRF Stream Input
requirements in Milan sections 5.3.8.10 and 5.4.2.25 open.

Solicited reads serve AAF Stream Input, Stream Output, AVB Interface, and
Clock Domain counters, and each of those pushes its Table 5.22 notification.
The CRF Stream Input has neither, and remains open under section 5.4.2.25.

### B5. Registered-controller liveness monitoring (closed at 0x0002_0055)

The processor stores unsolicited-notification registrations, applies the
time-limited expiry policy, and since 0x0002_0055 originates the random 30 to
60 s `CONTROLLER_AVAILABLE` monitor required by Milan section 5.4.5.3: one
retry 250 ms after an unanswered probe, a re-arm on any response status, and
the removal of a silent controller with the deregistration notification sent
to that controller alone. The command-driven half of section 5.4.5.2 closed in
the same version: every successful state-changing command pushes to the other
registered controllers and a no-op SET is silent.

Evidence: `protocol-processor/tb/aecp_notify`,
`protocol-processor/tb/ca_originator` and `protocol-processor/tb/pp_top` for
the mechanism; the `[NOTIFY]` section of
[`tb/verilator/milan_dp`](../../tb/verilator/milan_dp/README.md) for the wire
behavior through the root, with its timed leg measuring the probe, the retry
and the removal on the processor's compressed timebase (one of its
milliseconds is 100 fabric cycles).

### B6. Multi-bridge AS_PATH reporting (closed at 0x0002_0055)

The root gather face serves `GET_AS_PATH` as a zero-entry response when no
grandmaster is known, and otherwise as the grandmaster identity followed by
the last complete PathTrace tail the daemon published through the `0x7DC`
CSR group. Slot LO/HI writes and `COMMIT` update a private staging bank only;
they cannot change a solicited response or arm a notification. A changed
`PUBLISH` atomically transfers the complete staged tail and count to the
published bank, advances the publication generation, and arms the Table 5.22
`GET_AS_PATH` notification. Publishing content identical to the current
snapshot is silent. The response gather holds one publication generation, so
a publish interleaved with a read yields the complete old or complete new path,
never a mixed vector. A tail that has not been published leaves the one-entry
path seen by a leaf directly under its grandmaster.

What the daemon must do for the report to be complete is stage every tail entry
from the latest Announce PathTrace TLV and issue `PUBLISH` only after the tail
is complete. The root serves only the controller-visible published snapshot; incomplete
staging remains private.

Evidence: the `asp_served_count_w` / `asp_served_entry_w` selection and the
`gsi_asp_chg_w` strobe in
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv), the `[NOTIFY]`
atomic COMMIT/PUBLISH and identical-publish arms of `tb/verilator/milan_dp`,
and the staging group in
[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md).

### B7. Identify control has no public indication

The processor accepts Identify `SET_CONTROL` and stores its dynamic value, but
`KL_pp_shadow.sv` exports that value to the root wire
`pp_aecp_identify_w`. Nothing consumes the wire and the public `o_identify`
output is tied low, so no board indication can follow the control.

Evidence: the `o_identify` assignment in
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv).

### B8. GET_AVB_INFO propagation delay (closed at 0x0002_0055)

Software publishes the measured neighbor propagation delay through
`GPTP_PDELAY` at `0x6E4`, and since 0x0002_0055 the root selects that word --
or the fabric gPTP plane's own `pub_pdelay_ns_o` when `GPTP_PLANE_EN_P` is
set, the same selection the grandmaster identity uses -- as the effective
`propagation_delay` the gather face serves. One wire feeds both the served
answer and its change detector, so the Milan section 5.4.2.23 response
reports the stored measurement and a change to it is a Table 5.22
`GET_AVB_INFO` trigger. Until then the CSR output was discarded and the served
field was a structural zero.

The same trigger set closed the two neighbouring gaps this finding sat beside:
the gPTP domain number at `0x62C` and the grandmaster identity are
snapshot-compared in the root, none of them conditioned on grandmaster
presence, so a domain or delay update during startup or GM loss is announced
rather than swallowed.

Evidence: the `GET_AVB_INFO` gather selection and the `gsi_avb_chg_w` detector
in [`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv), the `GPTP_PDELAY`
entry in [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md), and the domain and
propagation-delay arms of the `[NOTIFY]` section of
[`tb/verilator/milan_dp`](../../tb/verilator/milan_dp/README.md) -- two
registered controllers, the delay walked 0 to 1 to `0xFFFFFFFF` to 0 with the
repeat write silent, and every push body compared against the solicited
`GET_AVB_INFO` that follows it.

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

### B12. Stream Input START/STOP completes at the record; persistence is open

The ACMP binding record is the single source of truth for the Stream Input
started state. `START_STREAMING` and `STOP_STREAMING` update that record, and
the AECP dynamic store's selector 6 is retired. A started Stream Input processes
its AVTPDUs. A stopped AAF input continues receiving, classifying, and counting
them while discarding their media contribution. The datapath suite also proves
a STOP/START pair does not forge a binding edge or reset the Stream Input
counters.

Issue #97 closed this behavior's two correctness defects at `0x0052`. The AECP
response now completes only after the record walker commits the state or
confirms the required no-op - a request the walker cannot start answers
`ENTITY_MISBEHAVING` inside a bounded window with no record side effect - and
the CRF stopped predicate moved off the receive frame strobe onto the
engine's own stop port, so stopped CRF traffic is observed and counted while
only timing consumption and the restart echo are suppressed.

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
3. The repository README now describes the current VERSION `0x0002_0053`
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
   interval, asserts the raw per-descriptor dirty source, which the root now
   delivers to the processor's rate-limited scheduler (B4). The CRF Stream
   Input counter and dirty connections remain open.
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

Any candidate that changes `protocol-processor` must also use a durable gitlink:
after fetching the donor repository's default branch, the exact pinned commit
must be its ancestor. A branch-only donor commit is not mergeable evidence.
Repin first, then rerun the parent repository's complete gate set at that exact
superproject/submodule pair; results from an earlier gitlink do not transfer.
