# AECP Test Strategy

Three verification tiers, each building on the previous.

---

## Contents

- **[T0 — Unit tests (Vivado XSIM)](#t0--unit-tests-vivado-xsim)** — Four SV-class benches, one per AECP module, with the stimulus each drives and its simulated run time. The only tier here that needs a vendor simulator.
- **[T1 — BDD (behave)](#t1--bdd-behave)** — The conformance suite and a CI gate, and it runs **offline in under a second** — no DUT, no simulator. Includes the per-feature scenario table (with the standing rule that a disagreeing run wins over the table), the record of what the 2026-08-12 control-plane deletion took out of it, and what came back on 2026-08-13 when the protocol-processor's AECP µCPU started answering again.
- **[T2 — Integration (full pipeline)](#t2--integration-full-pipeline)** — Two lines: blocked on two unimplemented modules, with the scenarios already written and tagged.
- **[Packet generator](#packet-generator)** — The SV class the scenarios build frames with, and its five entry points — one per AECP command family, plus the response validator that checks status and the `sequence_id` echo.
- **[Lint](#lint)** — Two commands over all thirteen AECP modules; the `--strict` form turns on `-Wall`.
- **[Containers (T1 CI)](#containers-t1-ci)** — The one image left: `Containerfile.bdd-runner`, built and run in two lines to get the BDD suite going in CI. Records that the DUT-simulation server image is **gone** — it existed only to run the AECP module benches over a UNIX socket, and both the RTL and the driver were deleted on 2026-08-13.

## T0 — Unit tests (Vivado XSIM)

SV-class testbenches targeting individual RTL modules.
Part: `xc7a100tcsg324-1` · Clock: 125 MHz (`T=8 ns`)

The four AECP module benches that used to be listed here were DELETED on
2026-08-13 along with the RTL they targeted: this repository's AECP/AEM,
ACMP, ADP and lwSRP engines are gone and the protocol-processor submodule is
the control plane. What remains under `tb/utests/` is `1722/`,
`802_1q_traffic_shaper/`, `ethernet_events/` and `ptp_timestamp/`; `ls
tb/utests/` is the authority, and the Verilator suites in `tb/verilator/`
supersede this tier for regression either way.

**Run:**
```bash
cd tb/utests/<family>/<module>
vivado -mode tcl -source tb_top.tcl
```

---

## T1 — BDD (behave)

Gherkin scenarios, offline: every one of them runs against a Python model or
reads a shipped source file, so the suite needs no DUT and no simulator.

**2026-08-12 — the AECP/ACMP/ADP/lwSRP tiers were DELETED, not skipped.** The
legacy IEEE 1722.1 and SRP control-plane RTL (`hdl/ieee17221/aecp/**`,
`hdl/ieee17221/acmp/**`, the ADP advertiser/parser, `hdl/ieee8021q/srp/**`)
has been removed from this repository; the protocol-processor submodule is
the control plane now, through `hdl/milan/KL_pp_shadow.sv`.
33 feature files and 9 step modules that tested only that RTL were deleted
with it, and the mixed features below were pruned scenario by scenario. The
`@tsn_gen` tier went with them: it generated AECP/ACMP frames from tsn-gen
protocol YAMLs, and there is nothing left to feed them to. No scenario is
currently excluded from the default suite.

**2026-08-16: the AECP tier follows the processor's served inventory.** The
protocol-processor AECP uCPU (`protocol-processor/hdl/aecp/**`) serves the
opcodes listed in `tests/steps/aecp_engine_steps.py`, including
READ_DESCRIPTOR and GET_COUNTERS. Unsupported commands receive a conformant
NOT_IMPLEMENTED fallback. IDENTIFY_NOTIFICATION as a command receives
BAD_ARGUMENTS. The engine stays silent for a command whose target_entity_id is
not ours and for an AECP response arriving as input.

`aecp_read_descriptor.feature`, `aecp_response_contract.feature` and
`counters_contract_milan.feature` cover the standards-facing contract. The
processor `pp_top` suite and root `milan_dp` suite cover the RTL and integrated
wire path. The Milan Table 5.22 unsolicited counter-change producer and
commands outside the served inventory remain explicit gaps.

These repeated claims are checked against the
[Milan feature status ledger](../docs/reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `missing` | - |
| `notifications.change-events` | `partial` | - |
<!-- milan-feature-status:end -->

**15 features / 338 scenarios / 1,615 steps**, all passing, counted by running
the suite on 2026-08-18 (the run's own tally is authoritative -- prose counts
go stale). It is the **conformance suite**, and it is a CI gate (the
`bdd-conformance` job in `.github/workflows/rtl.yml`).

| Feature file | Scenarios | What it reads |
|---|---|---|
| `wire_truth_avtp.feature` | 37 | `@torture`; hand-built AVTP **and MSRP/MVRP** byte vectors through `tb/tools/avtp_wire_truth.py` |
| `counters_contract_milan.feature` | 86 | `@torture` + L1; the Milan Table 5.6 counter table, its mask arithmetic and update laws, the CRF sink's per-era obligations in `KL_crf_rx`, and the documented `A_STRMW_CNT0..9` window |
| `aecp_read_descriptor.feature` | 28 | the READ_DESCRIPTOR answer -- the SUCCESS shape (28 + N), the NO_SUCH_DESCRIPTOR locate miss, the BAD_ARGUMENTS bad-configuration index, and the IEEE Section 7.4.5 four-octet {type, index} stub on **both** failure paths |
| `aecp_response_contract.feature` | 19 | the served-inventory and fallback contract, IDENTIFY_NOTIFICATION → `BAD_ARGUMENTS`, Milan Delta 7 ACQUIRE_ENTITY refusal, and the two silent refusals asserted as **no frame at all** |
| `torture_campaign_plan.feature` | 27 | `@torture`; audits `tb/tools/torture_campaign.py`'s own plan, assertion contract and cross-participant invariants |
| `milan_8021q_conformance.feature` | 22 | the 5-queue architecture, the PCP→TC→queue map, the CBS algorithm and its idleSlope/hiCredit/loCredit budgets, and listener VID/format filtering |
| `milan_base_formats.feature` | 14 | the required Base Audio Format family for every declared AAF Stream Input, with Stream Output and CRF exclusions |
| `audio_walking_tone_identity.feature` | 22 | `@torture` + L1; channel identity through the production decode path and a THD+N method validated against an independent coherent DFT |
| `clkv_tu_lease.feature` | 22 | the AVTP `tu` verdict and its CLKV lease |
| `wire_channel_accountability.feature` | 11 | the end-station builder's own width derivation over the shipping configs, plus the `milan_datapath` elaboration guards |
| `chmap_capture_identity.feature` | 11 | the capture-side chmap64 mux |
| `gptp_announce_receipt_timeout.feature` | 10 | the BMCA announce-receipt timeout |
| `item10_audio_maps.feature` | 4 | the chmap64 render-crossbar word format and its base_cluster + offset key space |
| `milan_streaming_licence.feature` | 4 | the AAF admission composition, the t>0 wire identity in `KL_aaf_packetizer`, and a byte-exact bench MSRPDU capture |
| `crf_sr_class_a.feature` | 3 | the CRF emitter's 802.1Q C-TAG and the lane it leaves on |

> Counts in prose go stale. `behave -f plain` prints the authoritative totals on
> every run; if this table and the run disagree, the run wins.

**`@torture` tier (2026-07-30):** the desk half of the standing
torture/compliance campaign. See the current
[`testing/TESTING.md`](../docs/testing/TESTING.md) map and the
[`harness/README.md`](../harness/README.md) runner contract. These features need
no DUT, no simulator and no `numpy`; they
audit the campaign's plan, its payload decoders, its counter contract and its
audio properties, so the parts that can be wrong silently are wrong at a desk
instead of on the bench.

**`@open-finding`:** none at present. Milan Delta 7 `ACQUIRE_ENTITY` is part of
the default response-contract run and must return `NOT_SUPPORTED` with no owner.

```bash
cd tests && behave --tags @torture -f plain     # just the campaign features
cd tests && behave --tags ~@open-finding -f plain   # the gate
python3 tb/tools/avtp_wire_truth.py --self-test # the decoders' byte vectors
python3 tb/tools/torture_campaign.py --self-test
python3 tb/tools/torture_campaign.py --checklist # what a human must do at the bench
```

**Run everything (offline, no DUT, no simulator — finishes in under a second):**
```bash
cd tests && behave -f plain          # 15 features / 338 scenarios (2026-08-18)
```
`behave` is not installed system-wide here; any virtualenv with it will do
(CI does `python3 -m pip install behave`).

**Environment variables:** `tests/environment.py` still reads `TSAGEN_DIR`,
`DUT_SOCKET` and `PACKET_GEN`, but no surviving scenario uses any of them: the
frame-generating tier is gone, and every feature here is self-contained.

---

## T2 — Integration (full pipeline)

RETIRED. This tier was pending an AECP response builder and egress mux that no
longer exist in this repository, and no `@T2` scenario survives.

---

## Packet generator

`tb/avtp_packet_gen_sv/tb_classes/avtp_aecp_packet_gen.svh` still builds AECP
command frames and is still useful as a CONTROLLER-side instrument. Since
2026-08-13 a bench that sends one is no longer testing the absence of a reply.
The protocol processor serves the declared AECP inventory, including descriptor
reads, state and control operations, stream and gPTP information, counters,
audio-map reads, unsolicited registration, and Milan information. Unsupported
operations receive the correctly sized `NOT_IMPLEMENTED` echo. See the
`aecp_*` features under T1 and the current audit for the exact contract. The
AVTP/AAF generators in the same library are unaffected.

---

## Lint

```bash
python3 scripts/lint_rtl.py           # sweep every module in hdl/, print the census
python3 scripts/lint_rtl.py --check   # the CI gate: fail on a NEW violation
python3 scripts/lint_rtl.py --pragmas # just the `lint_off` well-formedness gate
```

It sweeps every module under `hdl/` and ratchets per directory against
`scripts/lint.budget`; a normal run only ever LOWERS a budget entry. Run it
for the live census rather than quoting a count here.
See [Section 4b of `../docs/testing/TESTING.md`](../docs/testing/TESTING.md#4b-rtl-lint---scriptslint_rtlpy-the-ratcheted-gate).

---

## Containers (T1 CI)

The DUT-simulation server image is GONE: it existed only to run the AECP
module benches over a UNIX socket, and both the RTL and the driver were
deleted on 2026-08-13.

```bash
# BDD runner
podman build -f Containerfile.bdd-runner -t milan-bdd .
podman run -v $(pwd):/work milan-bdd
```
