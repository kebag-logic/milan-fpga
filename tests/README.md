# AECP Test Strategy

Three verification tiers, each building on the previous.

---

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

| Feature file | Scenarios | Tier |
|---|---|---|
| `aecp_packet_validator.feature` | 9 | T1 |
| `aecp_l0_state.feature` | 11 | T1 |
| `aecp_timers.feature` | 6 | T1 |
| `aecp_unsolicited.feature` | 6 | T1 |
| `aecp_stack_lock_acquire.feature` | 5 | T2 `@wip` |
| `aecp_stack_descriptor_walk.feature` | 5 | T2 `@wip` |

**Run T1 only (offline, no DUT):**
```bash
pip install behave
behave tests/features --tags ~@T2
```

**Skip WIP scenarios in CI:**
```bash
behave tests/features --tags ~@wip
```

**Environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `TSAGEN_DIR` | `/home/alex/tsn-gen` | tsn-gen checkout (protocol YAMLs + packet_gen binary) |
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
./scripts/run-verilator-lint.sh           # check all 13 AECP modules
./scripts/run-verilator-lint.sh --strict  # enables -Wall
```

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
