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
protocol YAMLs, and there is nothing left to feed them to. Nothing in the
suite skips any more.

**2026-08-13 — part of the AECP tier came BACK, because the device answers
again.** The deletion above was made on the premise "this device answers no
AECP command at all". That premise expired when the protocol-processor landed
its AECP µCPU (`protocol-processor/hdl/aecp/**`). The device now answers
**READ_DESCRIPTOR** (0x0004) for real out of a static descriptor image;
answers **IDENTIFY_NOTIFICATION-as-a-command** with `BAD_ARGUMENTS`
(IEEE §7.4.39.2, the opcode-specific rule, over §9.3.5.3.3's fallback);
answers **every other opcode and message type** — AEM, ADDRESS_ACCESS and
MVU alike — with a conformant `NOT_IMPLEMENTED` echo at `message_type + 1`,
the command's own length and a matching `control_data_length`; and stays
**silent** for exactly two inputs: a command whose `target_entity_id` is not
ours, and an AECP *response* arriving as input. Two features cover that and
only that: `aecp_read_descriptor.feature` and `aecp_response_contract.feature`.

**Still genuinely absent, and deliberately NOT covered** — a scenario
asserting an answer nothing gives is a conformance claim with no device
behind it: SET/GET_CLOCK_SOURCE, SET/GET_MAX_TRANSIT_TIME, GET_COUNTERS and
the Table 5.22 unsolicited push, the audio-map getters/setters, entity
lock/acquire semantics beyond the generic echo, saved-state persistence, and
SET_CONFIGURATION / NAME / SAMPLING_RATE / STREAM_FORMAT / STREAM_INFO. Their
features stay deleted.

**14 features / 307 scenarios / 1460 steps**, all passing, counted by running
the suite on 2026-08-13 (the run's own tally is authoritative — prose counts
go stale). It is the **conformance suite**, and it is a CI gate (the
`bdd-conformance` job in `.github/workflows/rtl.yml`).

| Feature file | Scenarios | What it reads |
|---|---|---|
| `wire_truth_avtp.feature` | 34 | `@torture`; hand-built AVTP **and MSRP/MVRP** byte vectors through `tb/tools/avtp_wire_truth.py` |
| `counters_contract_milan.feature` | 36 | `@torture` + L1; the Milan Table 5.6 counter table, its mask arithmetic and update laws, the CRF sink's per-era obligations in `KL_crf_rx`, and the documented `A_STRMW_CNT0..9` window |
| `aecp_read_descriptor.feature` | 28 | the READ_DESCRIPTOR answer — the SUCCESS shape (28 + N), the NO_SUCH_DESCRIPTOR locate miss, the BAD_ARGUMENTS bad-configuration index, and the IEEE §7.4.5 four-octet {type, index} stub on **both** failure paths |
| `aecp_response_contract.feature` | 20 (+1 `@wip`) | the answer contract — the `NOT_IMPLEMENTED` echo over AEM/AA/MVU and the whole opcode space, IDENTIFY_NOTIFICATION → `BAD_ARGUMENTS`, and the two silent refusals asserted as **no frame at all** |
| `torture_campaign_plan.feature` | 27 | `@torture`; audits `tb/tools/torture_campaign.py`'s own plan, assertion contract and cross-participant invariants |
| `milan_8021q_conformance.feature` | 22 | the 5-queue architecture, the PCP→TC→queue map, the CBS algorithm and its idleSlope/hiCredit/loCredit budgets, and listener VID/format filtering |
| `audio_walking_tone_identity.feature` | 19 | `@torture` + L1; channel identity through the production decode path and a THD+N method validated against an independent coherent DFT |
| `clkv_tu_lease.feature` | 18 | the AVTP `tu` verdict and its CLKV lease |
| `wire_channel_accountability.feature` | 9 | the end-station builder's own width derivation over the shipping configs, plus the `milan_datapath` elaboration guards |
| `chmap_capture_identity.feature` | 9 | the capture-side chmap64 mux |
| `gptp_announce_receipt_timeout.feature` | 7 | the BMCA announce-receipt timeout |
| `item10_audio_maps.feature` | 4 | the chmap64 render-crossbar word format and its base_cluster + offset key space |
| `milan_streaming_licence.feature` | 4 | the AAF admission composition, the t>0 wire identity in `KL_aaf_packetizer`, and a byte-exact bench MSRPDU capture |
| `crf_sr_class_a.feature` | 3 | the CRF emitter's 802.1Q C-TAG and the lane it leaves on |

> Counts in prose go stale. `behave -f plain` prints the authoritative totals on
> every run; if this table and the run disagree, the run wins.

**`@torture` tier (2026-07-30):** the desk half of the standing
torture/compliance campaign — see
[`../docs/testing/TORTURE_CAMPAIGN.md`](../docs/testing/TORTURE_CAMPAIGN.md) for
the whole thing, including the on-bench runner and **how to add a check in one
place**. These features need no DUT, no simulator and no `numpy`; they
audit the campaign's plan, its payload decoders, its counter contract and its
audio properties, so the parts that can be wrong silently are wrong at a desk
instead of on the bench.

**`@open-finding`:** ONE, and it is also `@wip`, so it is out of the gate and
out of the default run and fails on purpose when you ask for it. Milan v1.2
Δ7 requires `ACQUIRE_ENTITY` to never succeed and to answer `NOT_SUPPORTED`
with `owner_id` zero; the shipped µcode has that program (`E_ACQ`) but the
engine's three-arm dispatch never selects it, so 0x0000 falls through to the
generic `NOT_IMPLEMENTED` echo like any other unimplemented opcode. The
scenario in `aecp_response_contract.feature` asserts what Δ7 requires, so it
is the oracle for the fix rather than a description of one — run it with
`behave --tags=wip`. The two older findings lived in
`counters_contract_milan.feature`, cited line numbers in
`KL_aecp_response_builder.sv` and were deleted with that file.

```bash
cd tests && behave --tags @torture -f plain     # just the campaign features
cd tests && behave --tags ~@open-finding -f plain   # the gate
python3 tb/tools/avtp_wire_truth.py --self-test # the decoders' byte vectors
python3 tb/tools/torture_campaign.py --self-test
python3 tb/tools/torture_campaign.py --checklist # what a human must do at the bench
```

**Run everything (offline, no DUT, no simulator — finishes in under a second):**
```bash
cd tests && behave -f plain          # 14 features / 307 scenarios (2026-08-13)
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
2026-08-13 a bench that sends one is no longer testing the absence of a reply:
the protocol-processor answers READ_DESCRIPTOR, and answers everything else
with a `NOT_IMPLEMENTED` echo — see the two `aecp_*` features under T1 for the
contract it has to meet. The AVTP/AAF generators in the same library are
unaffected.

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
See [`../docs/testing/TESTING.md`](../docs/testing/TESTING.md) §4b.

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
