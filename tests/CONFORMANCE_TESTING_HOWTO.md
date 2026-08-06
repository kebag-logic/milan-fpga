# BDD Conformance Testing — How It Runs

**Branch:** `test-bdd-conformance`  
**Workspace:** `<worktree>`  
**Commit:** `382fe49` — `extend BDD conformance with ADP/SRP/entity-model/AECP/notification coverage`  
**Author:** hackerman-kl  

---

## 1. What the tests are

The BDD conformance suite is a set of **offline Python-model behave tests** that verify
Milan v1.2 protocol logic. The new `@milan_conformance` features run without a simulator,
FPGA, or external tools in under 1 second. The pre-existing `@tsn_gen` features use the
tsn-gen packet generator to build and decode wire-accurate frames. Together they form a
CI gate that runs in ~3 seconds.

The tests model the RTL behaviour described in:
- `hdl/ieee17221/acmp/acmp_pkg.sv` — ACMP status codes, state enum, timers
- `hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv` — listener binding state machine
- `hdl/ieee17221/acmp/KL_acmp_tlkr_ctx.sv` — talker PROBE_TX responder
- `hdl/ieee17221/adp/adp_advertiser.sv` — ADP advertise state machine
- `hdl/ieee8021q/srp/lwsrp_pkg.sv` — SR class, timers, bandwidth
- `hdl/ieee17221/aecp/KL_aecp_response_builder.sv` — AECP command handling
- `sw/builder/endstation_builder.py` — entity model generation
- `sw/builder/out/<config>/aem_overlay.json` — generated AEM overlay data

---

## 2. Prerequisites

### For the `@milan_conformance` features (new)

```bash
pip install behave   # the only dependency
```

No simulator, no FPGA, no external tools needed.

### For the `@tsn_gen` features (pre-existing)

The tsn-gen packet generator at `$HOME/tsn-gen`:

```bash
# The environment.py defaults to ~/tsn-gen (note: hyphen, not underscore)
# If it's elsewhere, export TSAGEN_DIR:
export TSAGEN_DIR=$HOME/tsn-gen

# The packet_gen binary must be built:
# $HOME/tsn-gen/build/traffic-gen/packet_gen --version  →  packet_gen 0.1.0
```

### For the bench-level features (in milan-tests-avb)

The sibling repo `$HOME/milan-tests-avb/` contains on-board test tools and
bench-level behave features that require real hardware:

```
milan-tests-avb/
├── fpga/tools/           gptp2csr.sh, counters_dump.py, stress_run.sh, ...
├── fpga/tests/           accept_tu_lease.sh, cbs-iperf3-interference.sh, ...
├── tests/features/       milan_listener_bind.feature, milan_clock_recovery.feature, ...
├── tools/                milan_torture.py (the torture campaign runner)
└── docs/                 testing-methodology.md, profishark-tap-topology.md, ...
```

These are NOT part of the offline CI gate — they run on the bench.

---

## 3. Files added on this branch

| File | Scenarios | Purpose |
|------|-----------|---------|
| `tests/features/milan_acmp_conformance.feature` | 37 | ACMP connection management, talker PROBE_TX, ADP advertise SM, command timeouts |
| `tests/features/milan_adp_advertisements.feature` | 12 | ADPDU format, available_index, cadence, GM change, ENTITY_DEPART |
| `tests/features/milan_srp_defaults.feature` | 12 | SRP Domain defaults, MRP timers, bandwidth gate, TSpec, LeaveAll |
| `tests/features/milan_entity_model_validation.feature` | 16 | Mandatory descriptors, CRF clock I/O, dynamic mapping, channel counts, firmware version |
| `tests/features/milan_aecp_extended_commands.feature` | 15 | SET/GET_STREAM_INFO, START/STOP_STREAMING, GET_AVB_INFO, GET_AS_PATH, GET_MILAN_INFO, GET_COUNTERS |
| `tests/features/milan_notifications.feature` | 12 | Unsolicited notifications, lock lifecycle, controller departure |
| `tests/steps/milan_acmp_conformance_steps.py` | — | Step definitions + offline models for ACMP/ADP |
| `tests/steps/milan_conformance_steps.py` | — | Step definitions + offline models for SRP/entity/AECP/notifications |
| `tests/CONFORMANCE_TESTING_HOWTO.md` | — | This document |

**New totals:** 6 feature files, 2 step files, 98 new scenarios, 710 new steps.

---

## 4. How to run

### Run the full BDD suite (all 41 features, including tsn_gen)

```bash
cd <worktree>/tests

# tsn-gen is at $HOME/tsn-gen (environment.py defaults to ~/tsn-gen)
# If your checkout is elsewhere:
export TSAGEN_DIR=$HOME/tsn-gen

behave -f plain --no-capture
```

Output (last lines):
```
41 features passed, 0 failed, 0 skipped
480 scenarios passed, 0 failed, 0 skipped
3045 steps passed, 0 failed, 0 skipped
Took 0min 3.469s
```

### Run just the new conformance features

```bash
behave --tags @milan_conformance -f plain --no-capture
```

Output:
```
6 features passed, 0 failed, 35 skipped
98 scenarios passed, 0 failed, 382 skipped
710 steps passed, 0 failed, 2335 skipped
Took 0min 0.029s
```

The 35 skipped features are the pre-existing suite (not tagged `@milan_conformance`).

### Run by sub-tag

```bash
behave --tags @acmp -f plain          # ACMP + ADP state machine (37 scenarios)
behave --tags @adp -f plain           # ADP advertisements (12)
behave --tags @srp -f plain           # SRP Domain defaults (12)
behave --tags @entity_model -f plain  # Entity model validation (16)
behave --tags @aecp_extended -f plain # AECP extended commands (15)
behave --tags @notifications -f plain # Unsolicited notifications (12)
```

### Run a single named scenario

```bash
behave -n "a BIND_RX_COMMAND to a valid unbound sink returns SUCCESS" -f plain
```

---

## 5. How the offline models work

Each feature has a Python model class that mirrors the RTL state machine. The model
is instantiated in a `Given` step, driven by `When` steps, and asserted by `Then`
steps.

### Example: ACMP listener binding (Milan v1.2 §5.5.3.5.3)

The `ListenerSink` class in `milan_acmp_conformance_steps.py` encodes the 8-state
Milan listener binding SM:

```
UNBOUND → PRB_W_RESP → SETTLED_NO_RSV → SETTLED_RSV_OK
                ↓ (timeout)              ↓ (tk departed)
          PRB_W_RESP2              PRB_W_AVAIL
                ↓ (timeout)
          PRB_W_RETRY
```

Feature:
```gherkin
Scenario: a successful PROBE_TX_RESPONSE settles the sink
  Given the model has a sink at index 0 in state PRB_W_RESP
  When the talker responds with PROBE_TX_RESPONSE status 0
  Then the sink state is SETTLED_NO_RSV
  And the sink has stream parameters set
```

Step code:
```python
# When
def step_probe_resp(context, st):
    sink = list(context.acmp.sinks.values())[0]
    sink.probe_response(st)

# Then
def step_sink_state_check(context, state):
    sink = list(context.acmp.sinks.values())[0]
    expected = _state_from_name(state)
    assert sink.state == expected, f"state={STATE_NAMES[sink.state]}, expected {state}"
```

### Constants are sourced from the RTL

Status codes, state enum values, and timer values come directly from `acmp_pkg.sv`:

```python
ACMP_STATUS_SUCCESS              = 0     # acmp_pkg.sv:47
ACMP_STATUS_LISTENER_UNKNOWN_ID  = 1     # acmp_pkg.sv:48
ACMP_STATUS_TALKER_UNKNOWN_ID    = 2     # acmp_pkg.sv:49
ACMP_STATUS_CTLR_NOT_AUTHORIZED  = 16    # acmp_pkg.sv:51

TMR_NO_RESP_MS = 200   # acmp_pkg.sv:76
TMR_RETRY_MS   = 4000  # acmp_pkg.sv:77
TMR_NO_TK_MS   = 10000 # acmp_pkg.sv:78
```

### Entity model validation reads actual builder output

```python
def _read_overlay(config_name):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    path = os.path.join(root, 'sw', 'builder', 'out', config_name, 'aem_overlay.json')
    with open(path) as f:
        return json.load(f)
```

The test checks the **actual generated JSON**, not a hand-maintained copy.

---

## 6. How tsn_gen integration works (pre-existing)

The `@tsn_gen` features (e.g. `aecp_milan_v12_tsn_gen.feature`, `acmp_listener_tsn_gen.feature`)
use the tsn-gen `packet_gen` binary to:

1. Generate wire-accurate frames from YAML protocol models (`$HOME/tsn-gen/protocols/`)
2. Patch specific fields bit-exactly
3. Decode every patched field back through `packet_gen --decode` (bidirectional oracle)
4. Drive the Milan semantic models that mirror `KL_aecp_response_builder` / `KL_acmp_listener`

The `TSAGEN_DIR` environment variable (default `~/tsn-gen`) tells the test where to find
the `packet_gen` binary and protocol YAMLs. The environment.py at `tests/environment.py`
sets this up:

```python
TSAGEN_DIR = os.environ.get("TSAGEN_DIR", os.path.expanduser("~/tsn-gen"))
PACKET_GEN = os.path.join(TSAGEN_DIR, "build/traffic-gen/packet_gen")
```

When `TSAGEN_DIR` is not set or `packet_gen` is missing, the `@tsn_gen` scenarios
**skip cleanly** — they don't fail.

---

## 7. Step naming — the shadowing bug and its fix

The pre-existing `tsn_gen_steps.py` defines `@then('the model responds status {code:d}')`
which reads `context.model_status`. My initial `milan_conformance_steps.py` defined a
step with the same parse pattern `@then('the model responds status {s:d}')` which reads
`context.ext_status`. Behave's parse matcher treats `{code:d}` and `{s:d}` as the same
pattern, so the second-loaded module's step shadowed the first — causing all 74 `@tsn_gen`
scenarios to fail with `status=None`.

**Fix:** renamed my steps to avoid the collision:
- `the model responds status {s:d}` → `the aecp_ext model responds status {s:d}`
- `the model responds status {s:d} (NO_RESOURCES)` → `the notif model responds status {s:d} (NO_RESOURCES)`
- `the model responds status {s:d} (ENTITY_LOCKED)` → `the notif model responds status {s:d} (ENTITY_LOCKED)`

After the fix, all 41 features / 480 scenarios pass.

---

## 8. Mutation testing — proving assertions bite

Every model assertion was verified by breaking the model and confirming the test goes red.

| Mutation | What breaks | Failures |
|---|---|---|
| Invalid sink returns SUCCESS instead of LISTENER_UNKNOWN_ID | sink validation | 1 FAIL |
| Locked bind returns SUCCESS instead of CONTROLLER_NOT_AUTHORIZED | lock enforcement | 5 FAIL |
| First probe timeout → RETRY instead of RESP2 | probe retry sequence | 1 FAIL |
| TMR_ADVERTISE = 10 instead of 5 | ADP cadence | 1 FAIL |
| Invalid talker source returns SUCCESS | source validation | 1 FAIL |
| GET_CONFIGURATION returns ENTITY_LOCKED when locked | GET-while-locked | 1 FAIL |
| SET_STREAM_INFO out-of-range returns SUCCESS | descriptor range | 1 FAIL |
| Bandwidth port = 1Mbit (exceeds 75%) | bandwidth ceiling | 1 FAIL |
| ADP available_index never increments | index sequence | 4 FAIL |
| START_STREAMING skips bind check | start-streaming gate | 1 FAIL |

All 10 mutations turn red. All restorations return green. Zero stub steps remain
(verified by AST scan for `assert True` / `pass`-only bodies).

---

## 9. Adversarial verification

An adversarial subagent was dispatched to audit the tests for false positives. It found:

1. **CRF `0410` detection** — confirmed correct against actual builder output
   (`0x041060010000BB80`). FALSE ALARM.

2. **Stub steps** (`assert True`, `pass`-only) — 4 found and fixed with real data checks.

3. **Status-bypass tautologies** — 2 step functions hardcoded `ext_status = 0` instead
   of routing through the model. Fixed: both now call model methods.

4. **ADP interval under-approximation** — model hardcodes 5s; RTL has `MIN(5, MAX(1,
   valid_time/2))` + random delay. The test is genuine at `valid_time=10` but cannot
   catch a regression to 10s. Noted as a known limitation of offline model-based testing.

---

## 10. What is NOT tested by these features

- Driving the Verilator DUT (that's the `tb/verilator/` suite — 60 self-checking harnesses)
- ACMPDU/ADPDU wire byte-layout (that's `wire_truth_avtp.feature` with hand-built frames)
- The RTL's random advertisement jitter
- On-silicon behaviour (that's the bench torture campaign in `milan-tests-avb/tools/milan_torture.py`)
- The full Milan endstation validation test plan v1.9 (which requires a Milan Test Machine
  with two Ethernet interfaces, wire capture, and offline traffic analysis)

---

## 11. CI integration

The `bdd-conformance` job in `.github/workflows/rtl.yml` already runs:
```bash
cd tests && behave --no-capture -f plain
```

The new `@milan_conformance` features run as part of that job with no additional
configuration — behave discovers all `.feature` files automatically. The only
dependency is `behave` (already installed by the CI job).

The `@tsn_gen` features require `TSAGEN_DIR` to be set (or `~/tsn-gen` to exist
with a built `packet_gen`). They skip cleanly when absent.

---

## 12. Related repositories

| Repo | Path | Purpose |
|------|------|---------|
| milan-fpga | `~/prjs/milan-fpga` | The source RTL repo (main worktree) |
| milan-fpga-hermes | `<worktree>` | Clean clone for validation (this branch) |
| tsn-gen | `$HOME/tsn-gen` | Packet generator for wire-accurate frame building |
| milan-tests-avb | `$HOME/milan-tests-avb` | Bench-level tests, torture campaign, on-board tools |

---

## 13. Directory structure

```
tests/
├── features/
│   ├── milan_acmp_conformance.feature       ← NEW (37 scenarios)
│   ├── milan_adp_advertisements.feature      ← NEW (12)
│   ├── milan_srp_defaults.feature            ← NEW (12)
│   ├── milan_entity_model_validation.feature ← NEW (16)
│   ├── milan_aecp_extended_commands.feature  ← NEW (15)
│   ├── milan_notifications.feature           ← NEW (12)
│   ├── acmp_listener_tsn_gen.feature         (pre-existing, @tsn_gen)
│   ├── aecp_milan_v12_tsn_gen.feature       (pre-existing, @tsn_gen)
│   ├── aecp_response_contract.feature        (pre-existing, @tsn_gen)
│   ├── item10_*.feature                      (pre-existing, @tsn_gen × 14)
│   ├── wire_truth_avtp.feature              (pre-existing, @torture)
│   ├── ... (23 more pre-existing features)
├── steps/
│   ├── milan_acmp_conformance_steps.py       ← NEW
│   ├── milan_conformance_steps.py            ← NEW
│   ├── aecp_common_steps.py                  (pre-existing)
│   ├── tsn_gen_steps.py                      (pre-existing)
│   ├── ... (12 more pre-existing step files)
├── environment.py                            (behave setup — unchanged)
├── CONFORMANCE_TESTING_HOWTO.md              ← NEW (this document)
└── README.md                                 (test strategy doc)
```
