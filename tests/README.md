# AECP Test Strategy

Three verification tiers, each building on the previous.

---

## Contents

- **[T0 — Unit tests (Vivado XSIM)](#t0--unit-tests-vivado-xsim)** — Four SV-class benches, one per AECP module, with the stimulus each drives and its simulated run time. The only tier here that needs a vendor simulator.
- **[T1 — BDD (Verilator + behave)](#t1--bdd-verilator--behave)** — The conformance suite and a CI gate, and it runs **offline in about 3 seconds** against a Python model — no DUT, no simulator. Includes the per-feature scenario table (with the standing rule that a disagreeing run wins over the table), the `@tsn_gen` tier where frames are generated from protocol YAMLs and every patch is re-checked through `--decode`, and the pinned tsn-gen CDL `+8` deviation so it is never mistaken for wire truth again.
- **[T2 — Integration (full pipeline)](#t2--integration-full-pipeline)** — Two lines: blocked on two unimplemented modules, with the scenarios already written and tagged.
- **[Packet generator](#packet-generator)** — The SV class the scenarios build frames with, and its five entry points — one per AECP command family, plus the response validator that checks status and the `sequence_id` echo.
- **[Lint](#lint)** — Two commands over all thirteen AECP modules; the `--strict` form turns on `-Wall`.
- **[Containers (T1/T2 CI)](#containers-t1t2-ci)** — Copy-pasteable podman builds for the two CI images: the DUT simulation server and the BDD runner.

## T0 — Unit tests (Vivado XSIM)

SV-class testbenches targeting individual RTL modules.  
Part: `xc7a100tcsg324-1` · Clock: 125 MHz (`T=8 ns`)

| DUT | Location | Tests | Run time |
|-----|----------|-------|----------|
| `KL_aecp_packet_validator` | `tb/utests/aecp/kl-aecp-packet-validator/` | 50 valid · 25 bad msg_type · 25 short CDL | 200 µs |
| `KL_aecp_l0_state` | `tb/utests/aecp/kl-aecp-l0-state/` | reset · lock · C2-reject · 60001-tick expiry · post-release · acquire | 1 ms |
| `KL_aecp_timers` | `tb/utests/aecp/kl-aecp-timers/` | 1 kHz period · lock expiry · counter gate | 100 ms |
| `KL_aecp_common_parser` | `tb/utests/aecp/kl-aecp-common-parser/` | entity match · mismatch · READ_DESCRIPTOR fields | 200 µs |

**Run:**
```bash
cd tb/utests/aecp/<module>
vivado -mode tcl -source tb_top.tcl
```

---

## T1 — BDD (Verilator + behave)

Gherkin scenarios driven by the `avtp_aecp_packet_gen` class. Two paths:

- **Offline** (default, no DUT binary): Python model in `tests/steps/aecp_common_steps.py` emulates admission control and lock/acquire state for fast CI.
- **Live DUT**: Verilator-compiled binary serving AXI-Stream over a UNIX socket (harness pending).

**45 features / 594 scenarios / 3548 steps**, all passing, counted by running the
suite on 2026-08-06 (the run's own tally is authoritative — prose counts go
stale). It is the **conformance suite**, and it is a CI gate (the
`bdd-conformance` job in `.github/workflows/rtl.yml`).

| Feature file | Scenarios | Tier |
|---|---|---|
| `aecp_packet_validator.feature` | 11 | T1 |
| `aecp_l0_state.feature` | 11 | T1 |
| `aecp_timers.feature` | 6 | T1 |
| `aecp_unsolicited.feature` | 6 | T1 |
| `aecp_stack_lock_acquire.feature` | 5 | T2 `@wip` |
| `aecp_stack_descriptor_walk.feature` | 5 | T2 `@wip` |
| `aecp_milan_v12_tsn_gen.feature` | 6 | T1 `@tsn_gen` |
| `acmp_listener_tsn_gen.feature` | 7 | T1 `@tsn_gen` |
| `item10_acquire_entity.feature` | 4 | T1 |
| `item10_audio_maps.feature` | 9 | T1 |
| `item10_clock_source.feature` | 3 | T1 |
| `item10_configuration.feature` | 3 | T1 |
| `item10_control.feature` | 3 | T1 |
| `item10_get_milan_info.feature` | 3 | T1 |
| `item10_lock_entity.feature` | 6 | T1 |
| `item10_max_transit_time.feature` | 5 | T1 |
| `item10_name.feature` | 3 | T1 |
| `item10_read_descriptor.feature` | 5 | T1 |
| `item10_sampling_rate.feature` | 4 | T1 |
| `item10_stream_format.feature` | 4 | T1 |
| `item10_stream_info.feature` | 4 | T1 |
| `wire_truth_avtp.feature` | 37 | T1 `@torture` (offline; hand-built AVTP **and MSRP/MVRP** byte vectors through `tb/tools/avtp_wire_truth.py`) |
| `entity_firmware_version.feature` | 3 | T1 (offline; reads the shipped descriptor bytes + `milan_csr.sv`) |
| `counters_contract_milan.feature` | 44 (2 `@open-finding`, red on purpose) | T1 `@torture` + 4 × L1 (offline; the GET_COUNTERS mask/layout/invariant contract, the growth verdicts, and the masks + per-sink bounds the response builder really emits) |
| `audio_walking_tone_identity.feature` | 22 | T1 `@torture` + 3 × L1 (offline; channel identity through the production decode path, its per-area index coverage, and a THD+N method validated against an independent coherent DFT) |
| `torture_campaign_plan.feature` | 26 | T1 `@torture` (offline; audits `tb/tools/torture_campaign.py`'s own coverage, its assertion contract, the streaming-licence gate and the cross-participant invariants) |

> Counts in prose go stale. `behave -f plain` prints the authoritative totals on
> every run; if this table and the run disagree, the run wins.

**`@torture` tier (2026-07-30):** the desk half of the standing
torture/compliance campaign — see
[`../docs/testing/TORTURE_CAMPAIGN.md`](../docs/testing/TORTURE_CAMPAIGN.md) for
the whole thing, including the on-bench runner and **how to add a check in one
place**. These four features need no DUT, no simulator and no `numpy`; they
audit the campaign's plan, its payload decoders, its counter contract and its
audio properties, so the parts that can be wrong silently are wrong at a desk
instead of on the bench.

Two scenarios in `counters_contract_milan.feature` are tagged `@open-finding`
and **fail on purpose**. (1) The `CMD_GET_COUNTERS` arm (lines 1944-2012 of
`KL_aecp_response_builder.sv`) bounds its `STREAM_INPUT` reply with the literal
`w_gs_index < 16'd2` and references neither `AEM_N_STRIN_C` nor `w_in_fidx`, so
sinks >= 2 - including the CRF Media Clock Input - answer `BAD_ARGUMENTS`, while
Milan v1.2 5.3.8.10 keeps the counters "for each Stream Input" with no exemption.
(2) The per-input format registers live behind `` `ifdef AEM_PER_STREAM_FMT `` and
the `` `else `` arm defines only `fmt_in0_r`, which no shipped config enables, so
only Stream Input 0 has format storage. Run `behave --tags ~@open-finding` for a
clean gate; the findings stay visible instead of being written down and
forgotten.

```bash
cd tests && behave --tags @torture -f plain     # just the campaign features
cd tests && behave --tags ~@open-finding -f plain   # a clean gate
python3 tb/tools/avtp_wire_truth.py --self-test # the decoders' byte vectors
python3 tb/tools/torture_campaign.py --self-test
python3 tb/tools/torture_campaign.py --checklist # what a human must do at the bench
```

**`@tsn_gen` tier (2026-07-15, the AM65x-validation recipe):** frames are
GENERATED by the tsn-gen `packet_gen` binary from protocol YAMLs (seeded =
reproducible), fields are patched bit-exactly by the steps and every patch
is cross-checked through `packet_gen --decode` (bidirectional wire-layout
oracle), then the Milan v1.2 semantic models mirroring
`KL_aecp_response_builder` / `KL_acmp_listener` are driven and asserted.

ACMP has no YAML in tsn-gen, so the repo carries its own:
`tests/protocols/acmp/1722_1_acmp.yaml` (validated by
`packet_gen --validate`). The suite also PINS the known tsn-gen CDL model
deviation (+8: it counts `target_entity_id`) so it is never mistaken for
the wire truth again. Scenarios skip cleanly when `TSAGEN_DIR` has no
built `packet_gen`.

**Run everything (offline, no DUT, no simulator — finishes in ~3 s):**
```bash
cd tests && behave -f plain          # 45 features / 594 scenarios (2026-08-06)
cd tests && behave --tags @tsn_gen   # just the tsn-gen tier
```
`behave` is not installed system-wide here; any virtualenv with it will do
(CI does `python3 -m pip install behave`).

**Skip WIP scenarios:**
```bash
cd tests && behave --tags ~@wip
```

**Environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `TSAGEN_DIR` | *(set to the local tsn-gen checkout)* | tsn-gen checkout (protocol YAMLs + packet_gen binary) |
| `DUT_SOCKET` | `/work/sock/aecp.sock` | UNIX socket for live DUT |
| `PACKET_GEN` | `$TSAGEN_DIR/build/traffic-gen/packet_gen` | tsn-gen binary (optional) |

---

## T2 — Integration (full pipeline)

Pending `KL_aecp_response_builder` and `KL_aecp_egress_mux` implementation. Scenarios tagged `@T2` in the feature files above.

---

## Packet generator

`tb/avtp_packet_gen_sv/tb_classes/avtp_aecp_packet_gen.svh`  
Extends `avtp_control_subtype`. Key methods:

| Method | Command |
|--------|---------|
| `aecp_no_payload_gen()` | ENTITY_AVAILABLE, GET_CONFIGURATION, REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION |
| `aecp_acquire_entity_gen()` | ACQUIRE_ENTITY (with flags) |
| `aecp_lock_entity_gen()` | LOCK_ENTITY (with UNLOCK flag) |
| `aecp_read_descriptor_gen()` | READ_DESCRIPTOR |
| `check_response()` | Validate status + sequence_id echo |

---

## Lint

```bash
python3 scripts/lint_rtl.py           # sweep every module in hdl/, print the census
python3 scripts/lint_rtl.py --check   # the CI gate: fail on a NEW violation
python3 scripts/lint_rtl.py --pragmas # just the `lint_off` well-formedness gate
```

Replaces the AECP-only `run-verilator-lint.sh`: the sweep lints all 82 modules,
`KL_aecp_top` included, and the AECP directory carries 5 of the 188 ratcheted
violations. See [`../docs/testing/TESTING.md`](../docs/testing/TESTING.md) §4b.

---

## Containers (T1/T2 CI)

```bash
# DUT simulation server
podman build -f Containerfile.dut-sim -t aecp-dut .
podman run -v $(pwd):/work aecp-dut KL_aecp_packet_validator

# BDD runner
podman build -f Containerfile.bdd-runner -t aecp-bdd .
podman run -v $(pwd):/work aecp-bdd
```
