# The torture / compliance campaign — one entry point, one place to extend

Status: 2026-08-01. The standing campaign the USER asked for: *"test everything,
every combination of streams, analyse every aspect — payload, counters,
controller information — against Milan v1.2, iterate until everything passes,
create scripts/behave tests to be re-used every time, extend them on everything
you notice, be creative and combine many tests in one run, AUDIO SHALL NEVER BE
FORGOTTEN, torture the end-station in every possible condition"*, plus the
standing amendment that **every participant in a stream is a measured party** —
*"not only the DUT (ARTY or Alinx) are to be checked, but the counters from the
test machine / received counters on the [peer device] or any test machine
involved."*

This page is the contract, and it is meant to be enough on its own. It says what
each script is, how to run it with every flag explained, **every assertion it
makes with the clause behind it and what makes it fail**, which sides each
verdict was measured on, how to read the output, how to extend it, what it costs
in wall-clock time, and — as importantly — what it deliberately does **not**
cover.

> **A verdict derived from one side's counters is a claim. A verdict corroborated
> across every side is a fact.** That distinction is the organising idea of the
> whole layer, and every JSONL record names the sides it used so a reader can
> tell which one they are looking at.

## Contents

- **[1. The five pieces and why they are separate](#1-the-five-pieces-and-why-they-are-separate)** — Each script, the question it answers, and the one rule that decides where a new check belongs.
- **[2. Prerequisites and the bench it assumes](#2-prerequisites-and-the-bench-it-assumes)** — What must be installed and reachable, what permissions, which hosts, and how to change the topology with flags instead of source edits.
- **[3. How to run it](#3-how-to-run-it)** — Copy-pasteable invocations for every real case, with every flag, its default, and when to change it.
- **[4. What it asserts — the full inventory](#4-what-it-asserts--the-full-inventory)** — All 70 plan assertions and all 31 wire-truth check families: name, clause, severity, what makes it FAIL, what a SKIP means, and which sides it measures.
- **[5. How to read the output](#5-how-to-read-the-output)** — The JSONL schema field by field, every verdict value, the exit-code contract, and worked examples of a pass, a failure and a skip.
- **[6. How to extend it](#6-how-to-extend-it)** — One recipe per kind of addition, each with a worked example and its mandatory negative control.
- **[7. The human-action checklist, and the physical (powerstrip) family](#7-the-human-action-checklist-and-the-physical-powerstrip-family)** — The physical interventions, what to do and what to observe — and the powerstrip hook (§7.1) that automates the two power cycles. §7.1 also holds the two verdicts a partition and a cold boot *actually* owe: the GM story is a topology question (a permanent grandmaster owes CONTINUITY, only a follower owes an advance), and the Milan 5.3.8.1 persistence *shall* grades `KNOWN-PENDING`, not `FAIL`, on a build with no store to hold it.
- **[8. The traps](#8-the-traps)** — The semantic and measurement traps a future maintainer *will* hit, each with its evidence.
- **[9. Limits, cost and non-coverage](#9-limits-cost-and-non-coverage)** — Exhaustive and honest, including runtime.

---

## 1. The five pieces and why they are separate

| piece | where | level / oracle | what it is | what it needs |
|---|---|---|---|---|
| the **plan** | [`tb/tools/torture_campaign.py`](../../tb/tools/torture_campaign.py) | L3 / the clause | Every pair, every index, every **concurrency set**, every churn sequence, every adverse condition — as **data**, with the assertions each step owes, the clause behind each, and the shared verdict functions (counter decode, the invariants, the licence decode, the cross-side and concurrency invariants). **No I/O at all.** | python3 |
| the **payload / wire analyser** | [`tb/tools/avtp_wire_truth.py`](../../tb/tools/avtp_wire_truth.py) | L5 on a capture, L3 on byte vectors / the wire + the clause | AVTP AAF + CRF + AVDECC control decode, **and MSRP/MVRP decode**, with the declared-versus-actual invariants. A library **and** a CLI, so the runner and the desk suite use one decoder. | python3, a capture |
| the **bench runner** | [`milan-tests-avb/tools/milan_torture.py`](#) | L5 / the wire on hardware | Turns plan steps into `avdecc_l2.py` calls, reads the test machine's own NIC statistics, and turns the answers into verdicts. The only piece that needs the bench. | python3, raw sockets, the peer host |
| the **runner's unit tests** | `milan-tests-avb/tools/test_milan_torture.py` | L3 / a fake wire | 87 offline tests over a `FakeWire`, concentrating on the part that can be wrong *silently*: which verdict is drawn from which answer, and whether the runner says SKIP-with-a-reason instead of PASS when it measured nothing. | python3 |
| the **desk suite** | [`tests/features/`](../../tests) ×4 features | L3 + L1 | Audits the plan's own coverage, the analyser's decoders, the counter contract and the audio properties — in ~3 s, with no hardware. | `behave` |

**The rule that decides where a new check goes:** *anything that can be decided
without hardware must be decidable without hardware.* A runner that chooses its
own coverage as it goes can only be audited by *running it*, and bench time is
the scarce, shared, serial resource this whole campaign exists to spend well.
That is why the plan is data and the coverage audit is a behave feature.

**Why index 0 is never enough** (a standing user rule, with its evidence). On
this fabric the `0x800` per-stream window makes **index 0 a hard alias of the
legacy flat registers** ([REGISTER_MAP.md](../reference/REGISTER_MAP.md), "the
alias rule"), so an index-0 pass exercises the alias path and not the indexed
one. Four separate per-index defects hid behind index-0-only testing:
`GET_STREAM_INFO` serving index 0's answer for every index, `MAX_TRANSIT_TIME`
existing only at index 0, `GET_COUNTERS` answering only index 0 (with sinks ≥ 2
falling to an empty mask), and the window's talker state bits hardwired 0 above
index 0. `plan_covers_every_index()` makes the rule executable — and it is
audited **per area**, because computed over the whole plan the matrix area's full
coverage *masks* every other area, which is exactly how the audio area stayed
index-0-only under a green coverage report.

---

## 2. Prerequisites and the bench it assumes

### Software

| need | where | what happens without it |
|---|---|---|
| `python3` (≥ 3.9) | everywhere | nothing runs |
| `behave` | the desk suite only | `cd tests && behave` fails; `pip install behave` in any virtualenv |
| `numpy` | **the THD+N step only, and nowhere else** | `audio.thdn` reports SKIP; every other check is unaffected |
| `sudo` + `CAP_NET_RAW` | the bench runner only | raw AVDECC sockets cannot open; the runner refuses to start unless `--dry-run` or `--no-sudo` |
| `tcpdump` | the tap host only | no captures, so the wire-truth and audio-identity checks SKIP with the exact command to run |
| `MILAN_FPGA_ROOT` | the bench runner | it searches `$MILAN_FPGA_ROOT`, `~/prjs-avb-on-fpga/milan-fpga`, `~/milan-fpga` and exits with the list it tried; a missing plan checkout is a hard explained failure and never a silent degradation |

### The three kinds of host, and why they are three

| host | role | what it can see |
|---|---|---|
| **the DUT board** (Arty; Alinx when it rejoins) | device under test | its own fabric CSRs — the licence word `0x694`, the RMON good-frame lanes `0x21C`/`0x230` behind the `STATS_CTRL` (`0x200`) snapshot latch, the per-stream lwSRP row `0x85C`. **Nothing else can read these**, so they are required inputs to the runner. |
| **the controller host** (the peer host) | runs `milan_torture.py` and `avdecc_l2.py` | AVDECC on `91:E0:F0:01:00:00`, and its **own** NIC statistics from `/sys/class/net/<iface>/statistics/`. It can **never** see MSRP/MVRP. |
| **the tap host** | carries the inline taps | **everything on the link**, including MSRP/MVRP on `01:80:C2:00:00:0E` — which no bridge forwards, so this is the *only* place the Listener Ready half of the Milan 5.3.7.3 licence exists on the wire. It is a **different machine** from the controller host. |

The taps are Profitap ProfiShark 1G+ units, inline on the board links. Their
host and interface are **configuration** (`--tap-host`, `--tap-iface`), never
source constants.

### Topology is configuration, not a source edit

The default shape is the Arty 4×4 (+ the CRF pair at index 4) against the
reference peer (4 talkers, 10 listeners). Change it with flags:

```bash
# the 8x8 Alinx shape, no source edit
--dut 'name=ax,entity=020000fffe000008,mac=020000000008,talkers=8,listeners=8,crf_out=8,crf_in=8'
# a different reference end station
--peer 'name=other,entity=aabbccddeeff0000,mac=aabbccddeeff,talkers=2,listeners=4'
# and the test machine, which is a measured party in its own right
--test-machine 'iface=enp6s0'
```

Recognised fields: `name`, `entity`/`entity_id`, `mac`, `iface`, `talkers`,
`listeners`, `crf_out`, `crf_in`, `formats` (`|`-separated), `role`,
`reference`, `csr_path`. **A misspelled field is refused, not ignored** — a
silently dropped `listners=10` would run the whole campaign against the wrong
shape and then report full coverage of it.

---

## 3. How to run it

### 3.1 Safe while the board is live (no wire traffic, no console, no sudo)

```bash
# the whole plan as a table: every step, its op, its assertions
python3 tb/tools/torture_campaign.py --plan
# only one area, as JSON, for a runner or a review
python3 tb/tools/torture_campaign.py --plan --areas matrix --json
# the per-index coverage audit, whole-plan …
python3 tb/tools/torture_campaign.py --coverage
# … and PER AREA, which is the only form that can say no about one area
# while another covers everything (exit 1 if any area is short)
python3 tb/tools/torture_campaign.py --coverage-by-area
# the plan for a different shape, without touching a line of source
python3 tb/tools/torture_campaign.py --plan --dut 'talkers=8,listeners=8,crf_out=8,crf_in=8'
# the entries a HUMAN has to perform, as a printable checklist
python3 tb/tools/torture_campaign.py --checklist
# the offline unit tests of the plan, the counter tables and the invariants
python3 tb/tools/torture_campaign.py --self-test      # 28 tests
# the offline byte-vector tests of every decoder and every payload check
python3 tb/tools/avtp_wire_truth.py --self-test       # 24 tests
# the desk conformance suite
cd tests && behave -f plain                            # everything
cd tests && behave --tags @torture -f plain            # just this campaign
cd tests && behave --tags ~@open-finding -f plain      # a clean gate (see §5.4)
```

`torture_campaign.py` flags: `--plan` (table), `--json` (the plan as JSON),
`--areas a,b` (default: all six), `--coverage`, `--coverage-by-area`,
`--checklist`, `--self-test`, `--dut`/`--peer` (topology, §2).

### 3.2 The wire analyser over a capture

Take the capture **on the tap host**:

```bash
# EVERYTHING on the link, for a DURATION.  Never -c N: see §8.3.
ssh <tap-host> sudo timeout 8 tcpdump -i <tap-if> -s 0 -w /tmp/cap.pcap
# or just the SRP exchange.  The tap's 28-octet record header shifts every
# ether offset by +28, so the EtherType is at ether[40:2]:
ssh <tap-host> sudo timeout 12 tcpdump -i <tap-if> -s 0 \
    'ether[40:2]=0x22ea or ether[40:2]=0x88f5' -w /tmp/srp.pcap
```

> **Tap bring-up trap.** `ip link set <if> up` is **not** sufficient —
> `rx_packets` stays 0 until a capture socket opens the device in promiscuous
> mode, and simply starting `tcpdump` starts the flow. `operstate` reads
> `unknown` even when the tap is working, so **never gate on `operstate`**; gate
> on `rx_packets` *after* opening a capture.

Then analyse it anywhere:

```bash
# a tap capture: 28-octet record header AND the FCS present
python3 tb/tools/avtp_wire_truth.py cap.pcap --tap \
    --expect-aaf-format 0205022001006000 --sr-vid 2
# one JSON verdict per line, for a morning diff
python3 tb/tools/avtp_wire_truth.py cap.pcap --tap --jsonl > verdicts.jsonl
# a bound-but-unfed talker owes SILENT FRAMES, not silence (Milan 5.3.7.3)
python3 tb/tools/avtp_wire_truth.py cap.pcap --tap --silent-stream 0200000000020000
# WHICH of my Stream Outputs never declared a Talker Advertise?  Pass the whole
# set; without it the check can only see a stream that streams UNDECLARED, never
# one that is silently undeclared.  This found a real defect: 2 of 5 declaring.
python3 tb/tools/avtp_wire_truth.py srp.pcap --tap \
    --talker-stream 0200000000020000 --talker-stream 0200000000020001 \
    --talker-stream 0200000000020002 --talker-stream 0200000000020003 \
    --talker-stream 0200000000020004
# the class-A transit check needs a gPTP reference or it SKIPS, on purpose
python3 tb/tools/avtp_wire_truth.py cap.pcap --tap --gptp-ref-ns 1234567890
# a capture that arrives already stripped of its record header
python3 tb/tools/avtp_wire_truth.py cap.pcap --tap-header 0
```

| flag | default | when to change it |
|---|---|---|
| `--tap` | off | set it for any ProfiShark capture: 28-octet record header **and** FCS |
| `--tap-header N` | `28` with `--tap`, else `0` | `0` for an already-stripped capture. Assuming a header that is not there decodes to nothing — and so does missing one that is |
| `--strip-fcs` | implied by `--tap` | a capture whose FCS was already removed |
| `--expect-aaf-format HEX` | none → the declared-vs-wire check SKIPs | the `GET_STREAM_FORMAT` readback: the comparison is wire-versus-what-a-controller-was-promised |
| `--expect-crf-format HEX` | the Milan Table 7.1 constant `0x041060010000BB80` | a device using a different CRF format |
| `--sr-vid N` | `2` | the bench SR VID. `None` makes the VID check SKIP rather than invent one |
| `--silent-stream HEX` | none | a stream that is bound but unfed: it must be **present and all-zero** |
| `--fed-stream HEX` | none | a stream that must carry non-zero audio |
| `--adp-entity HEX` | none | an entity that must keep advertising through the capture |
| `--talker-stream HEX` | none → falls back to the streams seen | the entity's whole Stream Output set, for the undeclared-talker check |
| `--gptp-ref-ns N` | none → the transit check SKIPs | the gPTP nanoseconds at the capture's first frame |
| `--max-transit-ns N` | `2000000` | a `SET_MAX_TRANSIT_TIME` other than the class-A 2 ms |
| `--jsonl` | off (a table) | for a diffable artifact |
| `--fail-on-skip` | off | for a gate that must be fully wired: exit 2 if anything SKIPped |

### 3.3 The bench runner

```bash
export MILAN_FPGA_ROOT=~/prjs-avb-on-fpga/milan-fpga     # where the plan lives

# what a full run WOULD do — touches nothing, exits 0, safe with the board live
python3 tools/milan_torture.py --dry-run
# the human checklist, and the plan
python3 tools/milan_torture.py --checklist
python3 tools/milan_torture.py --plan --areas torture

# ONE AREA FOR REAL.  Supply the licence: every frames-advance verdict is
# conditional on it, and without it they all SKIP (§8.1).  Read 0x694 on the DUT
# first — see the pre-step below.
sudo -E python3 tools/milan_torture.py --areas matrix --iface enp6s0 \
     --licence-status 0x1fe \
     --test-machine iface=enp6s0 \
     --tap-host <tap-host> --tap-iface <tap-if> \
     --jsonl ~/torture/$(date +%F-%H%M).jsonl

# ONE PAIR, for a bisect: --areas matrix over a one-talker one-listener shape
sudo -E python3 tools/milan_torture.py --areas matrix \
     --dut 'talkers=1,listeners=1,crf_out=,crf_in=' --peer 'listeners=1'

# THE PHYSICAL FAMILY (the powerstrip-driven switch cycle + DUT power cycle):
# an explicit opt-in, runs LAST, full recipe and safety contract in §7.1
sudo -E python3 tools/milan_torture.py --areas physical \
     --powerstrip-cmd "ssh amx-pi 'powerstrip {action} {outlet}'" \
     --switch-outlet 4 --dut-outlet 0

# feed the payload / audio areas their captures
sudo -E python3 tools/milan_torture.py --areas payload --pcap cap.pcap
sudo -E python3 tools/milan_torture.py --areas audio --pcap cap.pcap \
     --pcm-dump ring.s32be

# a gate that must be FULLY WIRED: any SKIP is exit 2
sudo -E python3 tools/milan_torture.py --areas matrix --fail-on-skip

# the runner's own offline tests (no hardware, no network, no sudo)
python3 tools/test_milan_torture.py                      # 87 tests
```

**The documented licence pre-step.** `0x694` is a DUT-board CSR and no AVDECC
command returns it, so the runner cannot fetch it on its own. Read it on the
board and hand it in:

```bash
# on the DUT, once per bind state you care about
devmem2 0x90000694 w          # or the project's CSR read helper
# then, on the controller host
--licence-status 0x1fe        # bit 8 set  -> the gate is OPEN
--licence-status 0x30         # bit 8 clear -> the gate is SHUT, and a silent
                              #                talker there is CONFORMANT
# or let the runner fetch it, if you have a path to the board
--csr-cmd 'ssh dut devmem2 0x9000{addr} w'
# any other DUT CSR the same way
--csr 0x21c=0x0012d687 --csr 0x85c=0x0000a53f
```

| flag | default | meaning / when to change |
|---|---|---|
| `--iface` | `enp6s0` | the test machine's interface: raw AVDECC sockets **and** its own NIC statistics both come from here |
| `--areas a,b` | all six (`matrix,multi,churn,payload,audio,torture`) | scope a run. A full run is ~2 h (§9.3) |
| `--dry-run` | off | emit one SKIP per assertion so the whole assertion list is visible; exits 0, touches nothing |
| `--checklist` / `--plan` | off | print and exit |
| `--jsonl PATH` | none (stdout only) | append verdicts to a diffable file |
| `--run-id ID` | a UTC timestamp | so two mornings sort and diff |
| `--no-sudo` | off | when the interpreter already has `CAP_NET_RAW` |
| `--pcap PATH` | none | a capture for the payload and audio-identity areas |
| `--pcm-dump PATH` | none | a raw S32BE PCM ring dump for the THD+N gate |
| `--tap-header N` | `28` | record header octets; `0` for an already-stripped capture |
| `--tap-host` / `--tap-iface` | none | the tap host and interface, used in the capture hand-off commands |
| `--dut` / `--peer` / `--test-machine` | Arty 4×4 / reference peer / `--iface` | topology (§2) |
| `--licence-status HEX` | none → the frames-advance verdicts SKIP | the DUT's `0x694` word |
| `--board-addr IP` | none → the stress load steps SKIP naming it | the DUT's IP, the best-effort load's target (§4.2.1) |
| `--board-cmd 'CMD {cmd}'` | none → iperf3 unprobeable, RX falls back to the UDP blast, TX SKIPs | a way to run one command on the DUT, e.g. `ssh root@dut {cmd}` |
| `--host-addr IP` | none → the TX-direction load SKIPs | this host's IP as the board's iperf3 client target |
| `--csr ADDR=WORD` | none | any other DUT CSR, repeatable |
| `--csr-cmd 'CMD {addr}'` | none | a command the runner may run to fetch one |
| `--fail-on-skip` | off | exit 2 if anything SKIPped |
| `--quiet` | off | suppress the per-line JSONL on stdout and the summary on stderr |

---

## 4. What it asserts — the full inventory

### 4.0 How to read this inventory

Every row gives the assertion's **name** (the stable JSONL key), the **clause**
it is held to, its **severity**, and **what makes it FAIL** versus **what a SKIP
means**. The general rules, which hold for every row:

* **A SKIP always carries a `why`.** A silent skip is how a campaign reports
  having tested something it never ran. A SKIP is *never* evidence of health.
* **A SKIP is never a violation.** Every unavailable reading — an unanswered
  `GET_COUNTERS`, a missing capture, an absent licence word, a peer mid-reflash
  — produces SKIP with the reason and the thing to supply.
* **Severity comes from the plan, not from the runner.** `SHALL` grades the run
  to exit 1; `RECOMMENDED` to exit 2; `INFO` is recorded and never failed.
* **`sides_used` / `side` say what was measured.** A verdict from one side is a
  claim; the `xside.*` family is what turns claims into facts.

### 4.1 Every bound-and-streaming step (`BOUND_STREAMING_ASSERTS`, 14)

Emitted by the **connect** op. Note what is *not* here: the two frames-advance
assertions. They depend on the Milan 5.3.7.3 licence, which a bind step has no
way to read, so they belong to the licence-owning step — see §4.2. Emitting them
from the bind is what turned ~135–285 *conformant* bound-but-ungated steps per
run into SHALL failures.

| assertion | sides | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `acmp.status` | listener | 1722.1-2021 8.2.2.5 / Milan 5.5.3 | the response carries a status other than SUCCESS for a compatible pair | no ACMP response at all (a peer mid-reflash is not a conformance failure) |
| `adp.alive` | DUT | 1722.1-2021 6.2.6 | the entity was not discovered in 2 × 11 s **and** a well-formed AECP command also went unanswered | not discovered but no MAC to probe with — absence is not proven (§8.4) |
| `counters.avb_interface.mask` | **DUT and peer, one verdict each** | 1722.1-2021 Tables 7-152/7-153 + Milan 5.4.2.25 | the mask omits `LINK_UP`/`LINK_DOWN`/`GPTP_GM_CHANGED` (`0x023`) | that end did not answer `GET_COUNTERS` |
| `counters.stream_input.mandatory-mask` | listener | Milan 5.3.8.10 + Table 5.6 | the mask does not claim all ten (`0xF3F`); the missing names are listed | `stream_input` did not answer |
| `counters.stream_output.mandatory-mask` | talker | Milan 5.3.7.7 + Table 5.4 | the mask does not claim all five (`0x01F`) | `stream_output` did not answer |
| `counters.stream_input.lock-invariant` | listener | Milan Table 5.6: *"either MEDIA_LOCKED=MEDIA_UNLOCKED … or MEDIA_LOCKED=MEDIA_UNLOCKED+1"* | neither holds | the mask does not claim both counters |
| `counters.stream_output.start-stop-invariant` | talker | Milan Table 5.4: *"either STREAM_START=STREAM_STOP+1 … or STREAM_START=STREAM_STOP"* | neither holds | the mask does not claim both |
| `counters.stream_input.tv-plus-tnv` | listener | 1722.1-2021 Table 7-157 | `FRAMES_RX` **exceeds** TV+TNV, which neither reading permits | the mask does not claim all three, **or all three read zero** — Milan 5.3.8.10 zeroes the block at the bind, so that snapshot is vacuous (§8.2). Read **after** the window. |
| `counters.stream_input.no-late-or-early-growth` | listener | Milan Table 5.6 LATE/EARLY_TIMESTAMP | either counter **ticked at all** across the window: one tick is one bad observation interval | the counters are not claimed. A **negative** delta is INFO: the block reset or a 32-bit counter wrapped, so the window measured nothing |
| `counters.stream_input.no-seq-mismatch-growth` | listener | Milan Table 5.6 + 1722-2016 4.4.4.6 | `SEQ_NUM_MISMATCH` ticked | as above |
| `counters.stream_input.no-unsupported-format-growth` | listener | Milan Table 5.6 UNSUPPORTED_FORMAT | `UNSUPPORTED_FORMAT` ticked. This is the 2026-07-27 escape: 296,294 of 296,294 frames discarded | as above |
| `counters.stream_input.tu-consistent-with-wire` | listener | Milan Table 5.6 + 1722-2016 4.4.4.7 | — (INFO by construction: the verdict needs the wire, so pair it with a tap capture) | `TIMESTAMP_UNCERTAIN` not claimed. `tu = 1` is **correct** for a board whose gPTP has not leased clock validity (`CLKV_CTRL 0x778`) |
| `xside.errors-static-all-sides` | **DUT, peer, test machine** | Milan Table 5.6 + 1722.1-2021 Table 7-153 `RX_CRC_ERROR` | any **device** error/discard counter moved across the window | nothing was readable. If only the **test machine's** loss lanes moved it is `INSTRUMENT-SUSPECT`, not FAIL (§4.6) |
| `instrument.test-machine-lossless` | test machine | the instrument rule (§4.6) | `rx_dropped`/`tx_dropped`/`rx_errors`/`tx_errors`/`rx_missed_errors`/`rx_over_errors`/`rx_fifo_errors` moved. **INFO severity — it never grades the run** | `/sys/class/net/<iface>/statistics/` was not readable |

Plus, on a bind: `counters.stream_input.reset-on-not-bound-to-bound` (and its
INFO companion `counters.stream_input.rebind-not-a-reset-boundary`) and
`wire.matches-declared-format`.

| assertion | sides | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `counters.stream_input.reset-on-not-bound-to-bound` | listener | Milan 5.3.8.10: *"shall reset all of these counters to zero each time the Stream Input changes its state from not bound to bound"* | the runner's own tracking proves the FROM-state was **not bound** and a counter carried its pre-bind value across the bind **beyond what a post-reset re-tick could rebuild** (event counters may re-tick to ≤ 8, interval/tally counters to ≤ 64: `MEDIA_LOCKED [1,1]` is reset→0→re-lock, not evidence). A counter that **dropped** proves the reset; a large counter still stuck beside drops is a *partial* reset and still FAILs — the clause says **all** | the block was not readable on both sides of the bind; was **already all zero** before it (a reset would be indistinguishable); the FROM-state is **unknown** (first touch this run — a leftover bind from a previous round makes the transition bound → bound, where the clause requires nothing); or the input was **already bound**: 5.5.3.5.43 handles a BIND_RX at a bound input by updating the binding parameters **without transiting UNBOUND**, so an implicit rebind owes no reset — the trigger is the *state transition*, never the BIND_RX message. ax-rv32-e filed 31 conformant binds (26 re-lock shapes + 5 rebinds/leftovers) as SHALL violations before these distinctions. Note the asymmetry the clause states: it does **not** reset going bound → not bound, so a zeroed block on an *unbind* is its own separate finding |
| `counters.stream_input.rebind-not-a-reset-boundary` | listener | Milan 5.5.3.5.43 (same talker: step 2 exits; different talker: steps 3–12 re-probe — never through UNBOUND) | never — **INFO by construction**: the clause is silent on the rebind case in both directions, so whether the device reset anyway is *recorded*, not judged | the bind did not succeed |
| `wire.matches-declared-format` | wire | 1722-2016 I.2.4.1 | (on a capture) the AVTPDU fields differ from the declared `stream_format` | always, on a control-plane step: it is a **wire** verdict. The SKIP hands off to `--areas payload --pcap <capture>` for the same talker index |

### 4.2 The licence-owning step (`LICENSED_STREAMING_ASSERTS`, 10)

Emitted by the **start_stream_if_needed** op, which follows *every* bind. This
step exists because the licence is a different reading from a different place,
and mixing it into the bind made a conformant device read as a violation.

| assertion | sides | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `srp.streaming-licence` | DUT (CSR `0x694`) | Milan 5.3.7.3: the licence is a **conjunction** — *"declaring a Talker Advertise attribute **and** receiving a Listener Ready or Listener Ready Failed attribute"* | never FAILs. PASS = gate open; INFO = gate shut, which is a legitimate state | no `0x694` reading was supplied. The SKIP names the register and `--licence-status` |
| `stream.starts-on-bind-alone` | talker | Milan 5.3.7.3: *"This specification excludes the possibility for a Stream Output to be stopped (STREAMING_WAIT state shall not be implemented)"* | the gate is **open** and `FRAMES_TX` did not move: the talker needs an AECP `START_STREAMING`, i.e. it has implemented the state the clause forbids | the gate is shut or unknown; `FRAMES_TX` unreadable; **or this talker index was left streaming by an earlier pair and the stop was not verified** (§8.5) |
| `counters.stream_output.frames-tx-advances` | talker | Milan 5.3.7.3 | the gate is open and `FRAMES_TX` still does not move after an explicit `START_STREAMING` | gate shut/unknown, or `FRAMES_TX` unreadable |
| `counters.stream_input.frames-rx-advances` | listener | Milan 5.3.7.3 + Table 5.6 `FRAMES_RX` | the gate is open and the listener's `FRAMES_RX` does not move | gate shut/unknown, `FRAMES_RX` unreadable, or the step carries no listener |
| `xside.growth-corroborated` | **talker + listener + test machine** | Milan 5.3.7.3 ties the talker's streaming to the listener's declaration | the sides **disagree** about whether the stream is running — a one-sided claim of streaming is itself the defect, in both directions | any side unreadable (named), or fewer than two independent sides supplied |
| `xside.unlicensed-silent-everywhere` | all | Milan 5.3.7.3 | the gate is **shut** and frames moved on any side: unreserved, unshaped traffic | the licence is unknown, or the stream *is* licensed (the invariant does not apply) |
| `xside.listener-not-more-than-talker` | talker + listener | 1722.1-2021 Table 7-153 (raw totals) | a listener counted more frames than the talker sent, beyond the snapshot skew — a second talker on the same `stream_id`, or a wrong counter | either side unreadable |
| `xside.absent-where-not-registered` | all + bystanders | 802.1Q-2018 8.8.4 | stream frames reached an interface that never registered as a listener for them. This bench has measured untagged frames at 500 pps on a port with no listener, so **absence is asserted, not assumed** | no registration set supplied |
| `xside.interval-ticks-agree` | talker + listener | Milan Table 5.4/5.6 | one side's **observation-interval** counter ticked and the other's did not, or — with **both sides interval-conformant** — they differ by more than the window edges explain. **Compares intervals, never frames** — the name says so on purpose (§8.6). When exactly **one** side ticks at wire frame rate (beyond `max(600, 150/s × window)` — no ≤ 1 s interval can tick that much, while a class A per-frame deviant reads ~8000/s) the pair verdict **PASSes for the conformant side by name** and the deviation moves to `xside.peer-counter-semantics`: a generic pair-FAIL would smear the side that earned its pass. ax-rv32-e smeared 37 pairs that way | one side's interval counter unreadable; or **both** sides tick per-frame — no interval-conformant baseline remains, and each side gets its own attributed finding |
| `xside.peer-counter-semantics` | **the deviant side, by name** | Milan Table 5.4/5.6 (*"at the end of every observation interval"*, ≤ 1 s) vs 1722.1-2021 Table 7-157 (per-frame) | a side's stream-descriptor `FRAMES_TX`/`FRAMES_RX` advanced at wire frame rate: it keeps the 1722.1 per-frame reading where Milan requires interval ticks. **Every participant is a measured party** — a reference device's deviation is a first-class SHALL finding attributed to *that* device with its measured rate, never smeared onto the conformant peer and never silently passed | only emitted when a deviation is measured |
| `instrument.test-machine-lossless` | test machine | §4.6 | as §4.1 (INFO) | as §4.1 |

### 4.2.1 The multi-stream concurrency area (`multi`)

The matrix walks **pair by pair** — bind one, verify, unbind, next — and four
whole defect classes are invisible to that walk because they only exist under
**aggregate load**: CBS shaping with several class A streams in the shaped queue
at once, the multi-slot rings actually multiplexing, per-index counter
**isolation** (an unbound index ticking while a neighbour streams — the
alias/bleed class that shipped four real defects under index-0-only testing),
and **cross-stream independence at teardown**. Real deployments run many streams
simultaneously; a campaign that only ever binds one at a time certifies a shape
no deployment uses.

Three concurrency sets, each derived from the device **specs** and never
hardcoded (`plan_multi()`):

| set | pairs | what it loads |
|---|---|---|
| `primaries` | every **reachable** reference listener fed at once — the listener set is the peer spec's `listener_indices()`, which on a redundant device names the (p) primaries only (the reference peer: 0/2/4/6/8). Talkers are the DUT's AAF set, assigned cyclically, so on the AX 8×8 this is the plain zip t0..t4 → l0/2/4/6/8; a DUT with fewer talkers than the peer has listeners reuses a talker with **two listeners on one stream**, which 1722.1-2021 8.2.2.6.2.1 permits | the egress path, CBS and the wire under full concurrent load |
| `selfloop` | the DUT's own tN → lN | every packetizer **and** depacketizer in the same fabric at once; needs no peer |
| `mixed` | outbound and loopback interleaved, when the shapes allow | the egress path serving the wire and the loopback simultaneously |
| `stress` | **everything the shapes allow at once**: every DUT AAF talker outbound (reachable reference listeners first, self-loops to fill — on the AX 8×8: t0..t4 → the primaries, t5..t7 looped home), **plus the inbound direction** (peer AAF talkers into whatever DUT listeners remain free) | the maximal concurrent stream set — and then **best-effort load over the same link while it all flows** (see below) |

Each set runs `bind-all → verify-concurrent → teardown-one → teardown-rest`
(the stress set inserts `load-rx → load-tx → verify-after-load` between verify
and teardown), and sets run **serially, each fully torn down before the next**,
so a set's verdicts are never polluted by a predecessor.

**One shared window.** The verify step reads *every* side — each bound talker's
`FRAMES_TX`, each bound listener's `FRAMES_RX` + lock + growth counters, and
every **unbound** stream input — around **one** sleep (`Wire.multi_deltas`).
`deltas()`-per-pair would measure S serial windows in which cross-stream
interference is invisible by construction.

**The licence gates it exactly as the pairwise steps.** The supplied `0x694`
word is the global/idx-0 gate (the per-index rows at `0x85C` sit behind the
`0x800` window select — a board-side pre-step), so SHUT or UNKNOWN SKIPs every
flow verdict, never fails one. `START_STREAMING` is probed **only when every
readable pair is dead** (that is the pairwise STREAMING_WAIT finding again, and
the probe records itself in `needed_start_streaming`); when only *some* pairs
are dead the probe must **not** fire — the asymmetry *is* the defect, and
starting streams mid-measurement would destroy the evidence.

The set-level assertions (the per-pair rows reuse the §4.1/§4.2 families, with
`pair` in the detail):

| assertion | sides | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `multi.concurrent-all-flowing` | every bound talker + listener | Milan 5.3.7.3 **per Stream Output**: each pair holds its own licence, so with the gate open every pair's interval counters advance **together** (Table 5.4/5.6 interval terms, never frames) | any readable pair is static — including one-sided movement — while the licence is OPEN; the dead pairs are named. One stream starving under aggregate load is the defect a pairwise walk can never see | licence SHUT/UNKNOWN; or a pair unreadable on both sides (named) with nothing else dead — a **measured dead pair outranks a measurement gap** |
| `multi.unbound-counters-static` | every **unbound** stream input, both devices | Milan 5.3.8.10 keeps the Table 5.6 counters **per Stream Input** | an unbound index's counters ticked while its neighbours streamed — the per-index aliasing/bleed class. Asserted regardless of the licence: an unbound index owes silence either way | no unbound index in the set, or none readable. A negative delta is INFO (reset/wrap — the window measured nothing) |
| `multi.neighbour-streams-survive-teardown` | the survivors after **one** unbind | Milan 5.3.7.3: the unbind removes only the torn-down stream's Listener Ready, so every other pair keeps its licence and keeps streaming | a survivor went static in the shared window right after the neighbour's unbind — the cross-stream-independence defect the staged teardown exists to catch | licence SHUT/UNKNOWN, or a survivor unreadable on both sides with none dead |

**The stress load steps** (`multi.stress.load-rx` / `load-tx`). While the
maximal set flows, best-effort load runs over the **same link**, both
directions sequentially: host → DUT TCP is RX stress on the RSC-less ingress
path, DUT → host is TX stress against the shaped egress queues. Then the load
goes **off** and `verify-after-load` re-runs the full verify machinery — the
before/during/after sandwich is what attributes a failure to the load.

* **The load engine is probed, never assumed.** The board is a busybox
  rootfs: `--board-cmd` lets the runner probe `iperf3 --version` there and
  drive the board-side pieces (`--board-addr` is the target, `--host-addr`
  the board's client target for the TX direction). With iperf3 on both ends
  the load is `iperf3-tcp` and the throughput comes from the `-J` summary.
* **The RX fallback is named honestly.** With no board iperf3, the runner
  blasts blind UDP from the controller host at the board's discard port —
  `iperf3 -u` cannot do this, its UDP mode still opens the TCP control
  connection a tool-less board can never answer — so the fallback is an
  in-process socket loop. It loads the **link** honestly, but nothing
  acknowledges it, so the recorded number is the **send rate, not goodput**,
  and every record carries `load_mode: udp-blast-fallback` plus the reason.
* **TX with no board tooling SKIPs.** Only the board can source board→host
  traffic; the step names what to supply rather than pretending.
* **The reads ride the loaded wire.** AVDECC is best-effort too, and the
  adverse practice says control-plane responsiveness is *not* expected under
  high-rate BE — so a pair whose `GET_COUNTERS` goes unanswered during the
  load window is named and SKIPped, never failed.

| assertion | sides | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `multi.streams-immune-to-best-effort-load` | every bound talker + listener, during the load | 802.1Q-2018 8.6.8.2 (credit-based shaper) + clause 34 (FQTSS): an admitted class A stream travels in a reserved, shaped queue **above** best-effort, so BE load SHALL NOT disturb it. **Deliberately distinct from the torture storm entries**: those are line-rate adverse traffic and stay RECOMMENDED per the recommended practice; a cooperative BE load inside the unreserved remainder is the shaper's design point, so this is SHALL | any pair's interval ticks went static while the load ran — the shaping/coexistence defect | licence SHUT/UNKNOWN; no load could be generated (named); a pair unreadable on both sides with none dead |
| `counters.stream_input.no-seq-mismatch-growth` / `no-late-or-early-growth` | each bound listener, across the loaded window | Milan Table 5.6: the error counters are static under coexistence — frames that keep flowing but arrive corrupted or late are what a ticks-only check calls a pass | the counter ticked in the loaded window | the load could not be generated, or the block was unreadable |
| `multi.best-effort-headroom` | the load itself | *info:* no clause grades this — 802.1Q reserves the streams, not the leftover. The achieved BE throughput is the measured headroom left by the reservations, a datum for capacity planning | — (INFO by construction, never graded) | no load path (naming the flag to supply) |

**The staged teardown.** `teardown-one` unbinds a pair whose talker serves
exactly one listener in the set (so silence is owed and `stream.stop-takes-effect`
applies verbatim; if the set's shape forces a shared talker, the plan sets
`expect_talker_silent: false` and the runner SKIPs the stop question with the
reason — the talker keeps its licence through the remaining Listener Ready).
`teardown-rest` then unbinds everything else and verifies the stop **per
talker** once its last binding is gone, the same discipline that protects the
next pair from a latched talker (§8.5).

### 4.3 The other control-plane assertions

| assertion | op / area | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `aecp.stream-format-readback` | `set_format`, matrix | 1722.1-2021 7.4.9/7.4.10 + Milan 5.5.1.2 | an unexpected status. `BAD_ARGUMENTS(7)`, `NOT_SUPPORTED(11)` and `STREAM_IS_RUNNING(12)` are recorded as `CONFORMANT-REFUSAL`, not failures — a talker's wire width is an elaboration fact | no response |
| `aecp.stream-format-round-trip` | `set_format`, matrix | same | a `SET` that returned SUCCESS does not read back | — |
| `stream.stop-takes-effect` | `disconnect`, matrix + churn | Milan 5.3.7.3 + 1722.1-2021 7.4.36 | `FRAMES_TX` is still advancing after the UNBIND **and** the `STOP_STREAMING`: the talker is framing with no reservation. A `NOT_IMPLEMENTED`/`NOT_SUPPORTED` status is recorded as a conformant refusal — the wire is the verdict | no talker MAC on the step, or `FRAMES_TX` unreadable after the stop. An unproven stop is treated as **still latched**, so the next pair SKIPs rather than guessing (§8.5) |

### 4.4 The payload / wire-truth families (31)

Every family emits at least one verdict on every capture — including an empty
one, where each emits a **SKIP naming what was absent**. Eight of these used to
emit *nothing* on an empty capture and `wt.control.length-honest` used to emit
**PASS**, because `not []` is True.

| family | clause | FAILs when |
|---|---|---|
| `wt.capture.stream-frames-present` | BENCH_TOPOLOGY: a mirror port sees control frames only | the capture holds no AAF and no CRF frames. **An empty capture is a FAIL, never a clean pass** |
| `wt.aaf.declared-vs-wire.<sid>` | 1722-2016 I.2.4.1 | the wire `channels_per_frame`/`nsr`/`format`/`bit_depth`/`samples_per_frame` differ from the declared `stream_format` |
| `wt.aaf.header-legal.<sid>` | 1722-2016 7.3.3, 7.3.4, Tables 9 and 11 | `channels_per_frame` 0, `bit_depth` 0 or wider than the format, a reserved `format`/`nsr`, `sv` 0 with a stream_id, non-zero `version` |
| `wt.aaf.payload-arithmetic.<sid>` | 1722-2016 4.4.4.10 + 7.3.5 | `stream_data_length` exceeds the payload present, or is not a whole number of sample events |
| `wt.aaf.seq-continuity.<sid>` / `wt.crf.seq-continuity.<sid>` | 1722-2016 4.4.4.6 / **10.4.6 — the CRF sequence_num is ONE octet, so FF→00 is a wrap** | a step other than +1 modulo 256 |
| `wt.aaf.tv-set.<sid>` | 1722-2016 4.4.4.5 / 7.5 | `tv = 0` on a frame with `sp = 0` |
| `wt.aaf.pts-step.<sid>` | 1722-2016 7.5 / Milan 5.3.7.6 | the presentation time does not advance by `sample_frames/fs` ± one media clock tick |
| `wt.aaf.class-a-transit.<sid>` | 802.1BA-2011 class A 2 ms | a presentation time further ahead than the budget. **SKIPs without `--gptp-ref-ns`** — a pcap timestamp is the capture host's `CLOCK_REALTIME` and comparing the two produces a confident number that means nothing |
| `wt.{aaf,crf}.c-tag-present/-pcp/-dei/-vid.<sid>` | 802.1Q-2018 9.5/9.6, 34.5 + Milan 7.3.3 / 4.2.7.2.1 | an untagged SR stream frame; a PCP other than 3; DEI set; a VID other than the SR VID. **VID 0 gets its own field** because that is the specific past defect: the tag is stripped on egress and the frames flood unshaped |
| `wt.aaf.zero-fill-silent/-present/fed-non-silent.<sid>` | Milan 5.3.7.3 | a stream declared silent-but-bound carries non-zero samples; or **no frames reached the tap at all** — absence and silence are different verdicts; or a stream declared fed is all-zero |
| `wt.crf.milan-format.<sid>` | Milan 7.3.2 + Table 7.1 | `base_frequency` ≠ 48000, `timestamp_interval` ≠ 96, one timestamp per PDU, or the wrong `type`/`pull` |
| `wt.crf.pdu-rate.<sid>` | Milan 7.3.2 + 1722-2016 10.4.12 | the observed PDU rate is not `base_frequency / (timestamp_interval × timestamps_per_pdu)` = 500 PDU/s, ± 5 % |
| `wt.crf.timestamp-step.<sid>` | 1722-2016 10.4.12/10.4.13 | consecutive CRF timestamps are not one `timestamp_interval` of media events apart |
| `wt.adp.frame-82.<eid>` | 1722.1-2021 6.2.1 | an ADPDU that is not 82 octets on the wire, or whose `control_data_length` is not 56 |
| `wt.adp.available-index-advances.<eid>` | 1722.1-2021 6.2.2.10 | a repeated `available_index` — silicon-diagnosed 2026-07-12: bump-on-change-only made controllers treat the entity as incoherent |
| `wt.adp.alive.<eid>` | 1722.1-2021 6.2.6 | an expected entity never advertised in the whole capture (the dormancy signature) |
| `wt.control.length-honest` | 1722.1-2021 9.2.1.1.6 | a control frame shorter than its own `control_data_length` claims. The defect a status-byte-only tool cannot see: our `SET/GET_NAME` path once declared 84 and put 20 octets on the wire |
| **`wt.msrp.talker-advertise-declared`** | Milan 5.3.7.2: *"For each of the Stream Outputs of its currently set Configuration, a PAAD shall always declare an MSRP Talker attribute as soon as it has valid SRP parameters"* | a declared Stream Output has no Talker Advertise. **This found a real fabric defect from the wire alone: only 2 of 5 talker stream_ids declaring.** Pass `--talker-stream` for the whole set or the check can only see a stream that streams *undeclared* |
| **`wt.msrp.listener-declaration-present`** | Milan 5.3.7.3 | a stream is on the wire without a Listener **Ready** or **Ready Failed**: it carries no reservation. An *Asking Failed* is not the licence |
| **`wt.msrp.declared-dmac-matches-wire`** | Milan 5.3.7.4: the Stream Destination MAC Address is an SRP parameter | the wire DMAC differs from the declared `DataFrameParameters.destination_address` |
| **`wt.msrp.declared-vid-matches-wire`** | Milan 5.3.7.4 + 802.1Q-2018 9.6 | the C-TAG VID differs from the declared `vlan_identifier` |
| **`wt.msrp.tspec-declared`** | 802.1Q-2018 35.2.2.8.5 | a frame larger than the declared `MaxFrameSize`, or `MaxIntervalFrames` = 0 — the stream is outside the reservation it claims |
| **`wt.msrp.domain-declared`** | 802.1Q-2018 35.2.2.9 + Milan 4.2.7.2.1 | the SR class A Domain attribute declares a priority other than 3 |
| **`wt.mvrp.sr-vid-declared`** | 802.1Q-2018 11.2.3.1.2 | MVRP never registered the SR VID — an unregistered VID is not pruned to the listeners and the stream floods |

All seven `wt.msrp.*` / `wt.mvrp.*` families SKIP with *"an INLINE TAP capture is
required; a mirror port and the controller host can never see these"* when the
capture holds no MRP frames.

The decoded MSRP Talker Advertise FirstValue is the 25-octet layout of 802.1Q-2018
35.2.2.8: `StreamID(8 = 6-octet MAC + 2-octet unique_id)` +
`DataFrameParameters(destination_address 6 + vlan_identifier 2)` +
`TSpec(MaxFrameSize 2 + MaxIntervalFrames 2)` + `PriorityAndRank(1)` +
`AccumulatedLatency(4)`. The Listener attribute is 8 octets — the StreamID only —
and its declaration type (`Ignore`/`Asking Failed`/`Ready`/`Ready Failed`) rides a
**separate** FourPackedEvents vector, two bits per value; a decoder that looks for
it in the value sees nothing.

### 4.5 Audio — never forgotten

Three shapes, because **presence testing cannot see identity or distortion**, and
**every AAF index**, because index 0 is the least representative one here. A CRF
Media Clock Stream carries timestamps and not audio samples, so it is
deliberately out of scope for the identity checks — stated, not assumed.

| assertion | op | clause | FAILs when | SKIPs when |
|---|---|---|---|---|
| `audio.identity.uncrossed` | `audio_identity_capture`, `audio_identity_loop` | 1722-2016 7.3.5: the payload is a chronological sequence of sample frames, one sample per channel **in channel order** | a channel carries a value that belongs to another channel. The pattern is a **walking tone**: channel *c* carries `1 << c`, so a swap, a duplicate and a drop are three *different* failures. A pattern that repeated a value across channels could not fail on a swap at all (methodology R4) | no capture, or the capture holds no AAF frames |
| `audio.identity.no-duplicate-neighbour` | `audio_identity_capture` | 1722-2016 7.3.5 | two adjacent channels carry identical content — the signature of a mux stuck on one pair | as above |
| `audio.identity.no-silent-channel` | `audio_identity_capture` | 1722-2016 7.3.5 + Milan 5.3.10.1 | a mapped channel carries nothing: a dropped channel, which presence testing cannot see | as above |
| `audio.identity.channel-preserved` | `audio_identity_loop` | Milan 5.3.10.1 | the channels sent did not come back on the same channels. Frames arrive, counters tick, and the audio is on the wrong pair — the failure a counter-only check calls a pass | no capture of the **return** leg |
| `acmp.status` / `counters.stream_input.frames-rx-advances` | `audio_identity_loop` | as §4.1/§4.2 | either of the loop's two binds refused, or the return leg's sink does not count | — |
| `audio.thdn.worst-channel` | `thdn_gate` | USER acceptance: THD+N ≤ −120 dBFS end to end (the digital source itself measures −147.99 dBFS, so the wire + ring path must add nothing) | the worst channel exceeds the limit, or the capture is **clipped** — a clipped capture is not a measurement | no `--pcm-dump`, or `numpy` is absent |
| `audio.thdn.coherent-not-windowed` | `thdn_gate` | the method itself | the analyser applies a window or fails to truncate to whole periods. The pilot tone is exact-period (48 samples = 1 kHz at 48 kHz), so a window spreads the fundamental into neighbouring bins which the residual then counts as distortion: it **manufactures the number it is supposed to measure**. The desk suite quantifies it — ≈ −3 dB on a mathematically perfect sine with a Hann window, and ≈ −7 dB un-truncated on samples that read −269 dB truncated | — |

The loop's oracle is a **foreign implementation** (methodology L4): stream to the
reference device's ch 1/2 and it returns on ch 1/2. That is the only kind of
oracle that can find our own bugs.

### 4.6 The test machine is an instrument before it is a witness

If the test machine's `rx_dropped` / `tx_dropped` / `rx_errors` / `tx_errors` /
`rx_missed_errors` / `rx_over_errors` / `rx_fifo_errors` moved during a window,
then **every listener-side and capture-derived verdict in that window was taken
through a lossy instrument**. Those verdicts are downgraded to
`INSTRUMENT-SUSPECT` carrying the delta — not reported as device failures.
`INSTRUMENT-SUSPECT` never grades the run.

This is not hypothetical: promiscuous mode drowning the softcore, and an
unscoped background storm, have both manufactured listener-side failures on this
bench. A saturated test host inventing device defects is the exact class of fake
red this campaign keeps tripping over.

The rule is applied to `counters.stream_input.tv-plus-tnv`, the three growth
assertions, `counters.stream_input.frames-rx-advances` and
`xside.errors-static-all-sides`. A **device** error counter that moves still
FAILs with a clean instrument — that control is in the tests.

### 4.7 The adverse-condition matrix, and its honest severities

The Milan **adverse-network-conditions recommended practice** covers exactly one
condition — sustained high-rate traffic, in four traffic classes — and it is a
**recommendation**: *"It is not a current requirement for a Milan device to
support the features mentioned."* It says nothing about malformed packets. It is
cited generically here, with no version: the version is a detail visible only to
a document holder and no technical claim needs it. Two rules follow, and both are
asserted by `torture_campaign_plan.feature`:

* storm entries carry severity **RECOMMENDED**, and control-plane responsiveness
  under storm is **INFO** — the same clause says *"As AVDECC traffic is
  Non-Priority, it is not expected that a Milan device remains responsive to
  AVDECC commands while subjected to high rate Non-Priority traffic."* Failing an
  entity there would assert the opposite of the document;
* malformed/truncated-frame entries cite **IEEE 1722.1-2021 9.2.1.1.6 / 9.2.1.2**
  and 1722-2016, never that document.

| group | entries | severity | driven by |
|---|---|---|---|
| sustained high-rate traffic | non-priority broadcast, **unicast to our own MAC** (the case the recommendation names explicitly), AVDECC flood, AVB Management (`01:80:C2:00:00:00`/`:0E`/`:21`), SR class B | RECOMMENDED | **no runner op yet** → SKIP naming `background_load` |
| link | software PHY bounce ×5 | SHALL | **no runner op yet** → SKIP naming `link_bounce` |
| link | **cable pull, same port then a different port** | SHALL | human — a powerstrip has no per-port outlet |
| gPTP | **grandmaster change**, **grandmaster loss** — both now delivered by the `physical` area's **switch cycle** (§7.1): the partition *is* the loss, the re-join *is* the change | SHALL | physical: powerstrip, or human without the hook |
| malformed | overstated / understated `control_data_length`, truncated AECP payload, short ACMPDU, bad AVTP version, overstated AAF `stream_data_length`, channel mismatch, unknown AEM command, wrong `target_entity_id` (**silence is correct there**) | SHALL | **no runner op yet** → SKIP naming `malformed_frame` |
| MAAP | DMAC conflict → *withdraw, wait 2 LeaveAll periods, reallocate* (Milan Table 5.3) | SHALL | **no runner op yet** → SKIP naming `maap_conflict` |
| VLAN | wrong SR VID; **VID 0 as its own case** | SHALL | **no runner op yet** → SKIP naming `vlan_misconfig` |
| starvation | talker source removed (silence **with** frames); listener stream stops (`STREAM_INTERRUPTED` advances) | SHALL | **no runner op yet** → SKIP naming `starve_source` / `stop_talker` |
| power | **DUT power cycle** → the non-volatile requirements of Milan 5.3.10.1 / 5.3.8.1 / 5.3.7.6, counters back at zero, and the zero-touch boot ladder — the `physical` area (§7.1) | SHALL | physical: powerstrip, or human without the hook |

### 4.8 The three counter reading traps this campaign encodes rather than repeats

1. **The bit numbering is MSB-first in the table and LSB-first on the wire.**
   1722.1-2021 Table 7-156 lists *"Bit # 31 … MEDIA_LOCKED"*, and MEDIA_LOCKED
   is the counter at block **offset 0**. Table 6-2 numbers `entity_capabilities`
   the same way, and there the *"Bit # 31"* entry is `EFU_MODE` — the flag every
   implementation writes as `1u << 0`. So the table's bit number is
   `31 - offset/4` and the wire mask is `1 << offset/4`.
   `counters_valid_bit_ieee()` produces both so nobody reconstructs the
   conversion from memory.

2. **STREAM_OUTPUT has two layouts and they are not compatible.** Milan Table 5.4
   is a **dense five** (`FRAMES_TX` at slot 4); 1722.1-2021 Table 7-159 is
   **eight** (`FRAMES_TX` at slot 7, `STREAM_INTERRUPTED` at slot 2). la_avdecc
   carries both enums side by side for exactly this reason. Decoding ours with
   the wrong table renames `FRAMES_TX` to `TIMESTAMP_UNCERTAIN`, and the runner
   names its choice in `milan_torture.BLOCKS`.

3. **`FRAMES_RX` / `FRAMES_TX` mean two different things, ~8000× apart** — see
   §8.6, which is the full trap including the cross-device consequence.

---

## 5. How to read the output

### 5.1 The JSONL record, field by field

One line per **assertion**, not per step — a step that emits one line can only
report its worst outcome, and then a morning diff cannot tell which assertion
changed.

```json
{"schema":"milan-torture/1","run":"20260730T0914",
 "step":"out.artyt0-peerl3.connect","area":"matrix",
 "assertion":"counters.stream_input.lock-invariant","verdict":"PASS",
 "severity":"SHALL","clause":"Milan v1.2 Table 5.6: 'either MEDIA_LOCKED=…'",
 "detail":{"side":"peer","index":3,"media_locked":5,"media_unlocked":4,
           "synchronized":true},
 "ts":1785392340.123}
```

| field | meaning |
|---|---|
| `schema` | `milan-torture/1`. Bump it if the shape changes, so an old diff tool fails loudly |
| `run` | the run id (`--run-id`, default a UTC timestamp), so two mornings sort and diff |
| `step` | the plan step id. Stable across runs by construction; `no two steps share an id` is a desk-suite scenario |
| `area` | `matrix` \| `multi` \| `churn` \| `payload` \| `audio` \| `torture` \| `precheck` \| `meta` |
| `assertion` | the stable assertion name — the key you grep and diff on |
| `verdict` | see §5.2 |
| `severity` | `SHALL` \| `RECOMMENDED` \| `INFO`, straight from the plan |
| `clause` | the clause text the assertion is held to, carried in the record so a reviewer needs nothing else open |
| `detail` | everything measured. Conventions: `side`/`sides_used` name the participants; `why` is mandatory on a SKIP; `index` is the descriptor index; `tolerance_*` always travels with its `tolerance_reason` |
| `ts` | wall-clock seconds, rounded to ms |

**No local filesystem paths appear in this file.** `FPGA_ROOT` used to be
interpolated into `run.start` and into every capture/analyse hint, and the log is
a diffable artifact compared line for line between hosts — so one machine's home
directory made every line differ. The hints are path-relative to the two
checkouts instead.

The first record of a run is `run.start`, which names the participants, the
areas, the step and assertion counts, whether the licence was supplied, and
whether `--fail-on-skip` is on. The last is `run.summary` with the counts and the
exit code.

### 5.2 The verdicts

| verdict | means | grades the run? |
|---|---|---|
| `PASS` | measured, and the clause holds | no |
| `FAIL` | measured, and the clause does not hold | **yes**: exit 1 at SHALL, exit 2 at RECOMMENDED |
| `SKIP` | **not measured**, and `detail.why` says why. Never evidence of health, never a violation | no — unless `--fail-on-skip` |
| `INFO` | recorded on purpose because the clause is silent, or because the verdict needs a different measurement | no |
| `CONFORMANT-REFUSAL` | the device refused, and the clause permits the refusal (a talker's `SET_STREAM_FORMAT` `NOT_SUPPORTED`; `STREAM_IS_RUNNING` while bound) | no |
| `NEEDS-HUMAN` | a physical intervention is outstanding | exit 2 |
| `INSTRUMENT-SUSPECT` | the **test machine** lost frames in this window, so the measurement is inadmissible — not a device failure and not a pass | no |
| `KNOWN-PENDING` | the clause is real and unsatisfiable **by construction on this build**, so the assertion is kept, the gap is named in `detail.why`, and the same assertion goes live untouched the day the build can satisfy it. First user: `state.restored-after-power-cycle` on a DUT with no non-volatile store (§7.1) | no |

### 5.3 Exit codes

| code | meaning |
|---|---|
| 0 | nothing outstanding |
| 1 | at least one `SHALL`-severity `FAIL` |
| 2 | only `RECOMMENDED` failures, or `NEEDS-HUMAN` entries outstanding, **or** `--fail-on-skip` and anything SKIPped |

A `SKIP` alone never fails a run — it is honest — but it is counted in the
summary so it cannot hide, and `--fail-on-skip` exists for a gate that must be
fully wired. Without it, a run in which *every* assertion SKIPped (no licence
supplied, no captures, a peer mid-reflash) exits 0 and reads as a clean campaign.

The analyser's exit codes are the same idea: 0 clean, 1 a `FAIL`, 2 with
`--fail-on-skip` and any `SKIP`.

### 5.4 Worked examples

**A real pass**, corroborated on three sides:

```json
{"assertion":"xside.growth-corroborated","verdict":"PASS","severity":"SHALL",
 "detail":{"sides_used":["arty","peer","testhost"],
           "sources":{"arty":"avb_interface","peer":"avb_interface","testhost":"nic"},
           "frames":{"arty":8003,"peer":8001,"testhost":8002},
           "moving":{"arty":true,"peer":true,"testhost":true},
           "tolerance_frames":8000,
           "tolerance_reason":"the sides are not sampled atomically: …"}}
```

Read it as: three independent counters agree that this stream is running, and the
comparison used only frame-accurate sources.

**A real failure** — the one-sided claim:

```json
{"assertion":"xside.growth-corroborated","verdict":"FAIL","severity":"SHALL",
 "detail":{"sides_used":["arty","peer","testhost"],
           "moving":{"arty":true,"peer":false,"testhost":false},
           "why":"the sides disagree about whether this stream is running. …"}}
```

The talker says it is streaming; the listener and the wire see nothing. Exit 1.

**A skip that is not a problem** — the licence is a required input:

```json
{"assertion":"stream.starts-on-bind-alone","verdict":"SKIP","severity":"SHALL",
 "detail":{"side":"arty","index":2,"licence_state":"SHUT",
           "licence":{"raw":"0x30","talker_declared":true,"domain_ok":true,
                      "listener_declaration":"none/ignore",
                      "stream_gate_open":false},
           "why":"LWSRP_STATUS bit 8 (stream gate) is SHUT, so Milan v1.2
                  5.3.7.3's licence … is not complete. A talker emitting nothing
                  here is CORRECT, so the frames-advance assertions are SKIPped
                  rather than failed"}}
```

This is a **conformant device** and a correctly silent one. Filing it as a
failure — which the layer used to do, ~135–285 times per run — is worse than not
testing it at all.

### 5.5 Diffing two mornings

```bash
# what changed, by assertion
jq -r '[.step,.assertion,.verdict]|@tsv' a.jsonl | sort > a.tsv
jq -r '[.step,.assertion,.verdict]|@tsv' b.jsonl | sort > b.tsv
diff a.tsv b.tsv
# only the SHALL failures
jq -r 'select(.verdict=="FAIL" and .severity=="SHALL")|[.step,.assertion]|@tsv' b.jsonl
# every one-sided (uncorroborated) green
jq -r 'select(.verdict=="PASS" and (.detail.sides_used|length)<2)|.assertion' b.jsonl
# what SKIPped, and why
jq -r 'select(.verdict=="SKIP")|[.assertion,.detail.why]|@tsv' b.jsonl | sort -u
```

### 5.6 The two deliberately-red desk scenarios

`counters_contract_milan.feature` carries two scenarios tagged `@open-finding`
that **fail today and should**. Run `behave --tags ~@open-finding` for a clean
gate; the findings stay visible and cannot be forgotten.

**(1) `GET_COUNTERS` answers only Stream Inputs 0 and 1.** Milan v1.2 5.3.8.10:
*"For each Stream Input of the currently set Configuration, the PAAD-AE shall
keep track of the counters in Table 5.6"*, and 5.4.2.25 makes `GET_COUNTERS`
mandatory per descriptor. In `hdl/ieee17221/aecp/KL_aecp_response_builder.sv`:

* the `CMD_GET_COUNTERS` case spans lines 1944–2012;
* that block contains **no** `w_in_fidx` and **no** `AEM_N_STRIN_C`;
* its only `STREAM_INPUT` guard is `w_gs_index < 16'd2`;
* it calls `load_input_counters_consts(w_gs_index == 16'd0)`, which emits mask
  `0xF3F` and loads real counter **values** only for sink 0.

So sinks ≥ 2 — including the CRF Media Clock Input at index 4 — fall through to
`BAD_ARGUMENTS`, and sink 1 answers `0xF3F` over an all-zero block.

> **A note on how to argue with this scenario.** It was briefly re-scoped to grep
> the *whole* builder for `w_gs_index < 16'(AEM_N_STRIN_C)`, which passes by
> matching line 395 — the `w_in_fidx` declaration, whose own comment says *"range
> validity is decided separately in the STREAM_FORMAT arm"* and which is used
> only for `AEM_STRIN_FMT_C`. A whole-file grep standing in for an arm-anchored
> check is exactly the descriptor-context-free defect this layer exists to
> remove, so the check is anchored on the arm and its failure message prints the
> guard text it found. **Silicon evidence to the contrary is welcome and must be
> reconciled against those four bullets and those line numbers** — not against a
> broader pattern match.

**(2) Only Stream Input 0 has somewhere to store a stream format.** The per-input
format registers live behind `` `ifdef AEM_PER_STREAM_FMT ``, and the `` `else ``
arm defines exactly one — `fmt_in0_r` (line 707). No file under `configs/`
defines that macro. Milan v1.2 5.5.1.2 makes the Listener's current format the
value a bind is checked against, and the standing directive is that a controller
must **always** `SET_STREAM_FORMAT` the listener to the talker's format rather
than refuse the bind — so a sink with no format storage cannot participate in
that. This is a **different subsystem** from finding (1) and is tracked
separately.

---

## 6. How to extend it

Every kind of check has exactly one place to add it, and every addition owes a
**negative control** (methodology R2: a check that cannot fail is not a check).
The standing requirement is that this suite **grows every round**.

### (a) A new payload / wire invariant

One method on `avtp_wire_truth.WireTruth`, one line in `checks()`, one
byte-vector test in `self_test()` proving it fails on a bad frame **and** passes
on a good one, and one scenario in `wire_truth_avtp.feature`.

```python
def check_my_thing(self) -> list[Verdict]:
    if not self.aaf:                       # THE EMPTY-COLLECTION RULE
        return [_nothing_to_check("wt.aaf.my-thing", "IEEE 1722-2016 x.y",
                                  "AAF frames")]
    out = []
    for sid, recs in sorted(self.aaf.items()):
        bad = [i for i, (_t, _e, p) in enumerate(recs) if p.evt != 0]
        out.append(_v(f"wt.aaf.my-thing.{sid:016x}", not bad,
                      "IEEE 1722-2016 x.y: <the quoted clause>",
                      violations=bad[:8], frames=len(recs)))
    return out
```

Then add `out += self.check_my_thing()` to `checks()`, and add the family name to
`WT_FAMILIES` in `tests/steps/wire_truth_steps.py` so the empty-capture scenario
notices if it ever stops emitting. **Never return an empty list**: a check whose
loop body never ran must SKIP, not vanish and not pass.

### (b) A new counter obligation

The name tuples and mask constants at the top of `torture_campaign.py`, an
invariant function beside `check_lock_invariant()`, and a scenario in
`counters_contract_milan.feature`. If the standards disagree about the counter's
meaning, the function **reports which reading is in force** rather than picking
one — see `check_tv_tnv()`. If the counter is an observation-interval counter,
the verdict is a **growth** verdict (`check_no_growth()`), never a rate.

### (c) A new assertion on an existing step

One `AssertSpec(name, clause, severity)` and add it to the step's `asserts`
tuple — or to `BOUND_STREAMING_ASSERTS` if every bind owes it, or to
`LICENSED_STREAMING_ASSERTS` if it is only meaningful once the licence is known
open. The desk suite then enforces that it has a clause and a valid severity, and
that every bind carries it. **The runner must emit it**, even if only as a SKIP
that names it: the set-equality test in `test_milan_torture.py`
(`test_a_healthy_bind_EMITS_EVERY_ASSERTION_IT_OWES`) will red immediately
otherwise. That test exists because two planned assertions were never emitted at
all for exactly as long as the check was per-op instead of per-assertion.

### (d) A new adverse condition

One `Step(...)` in `plan_torture()` with its clause, its assertions, and
`needs_human=True` + `human_action="…"` if a person must do it. Then one
`op_<name>()` method on `milan_torture.Runner`, plus a fake-wire test in
`test_milan_torture.py`. **An op with no runner method is a SKIP that names the
op** — and if it stays that way, it must also appear in §9.

### (e) A new device or a new participant

Nothing in source. `--dut` / `--peer` / `--test-machine` take
`key=value,…` specs (§2), `tc.participants()` returns the measured parties in a
stable order, and `Device.role` decides whether a participant is a DUT, a
reference end station or an instrument. Add a *third* end station by giving it a
`--peer` spec and running the areas that name it.

### (f) A new area

One function in `torture_campaign.py`, one entry in `AREAS`, and one entry in
`area_index_expectations()` saying **which index families that area is expected
to walk** — an empty expectation is allowed but must be *stated*, because the
per-area coverage audit is what makes "we test every index" checkable.

---

## 7. The human-action checklist, and the physical (powerstrip) family

Three entries need a person at the bench, and they are **printed, never silently
skipped** — a skipped adverse-condition entry that nobody sees is how *"we tested
link loss"* becomes true in a report and false on the bench.

```bash
python3 tb/tools/torture_campaign.py --checklist
```

emits, for each: the step id, the exact action, the assertions to make
afterwards, the clause, and the note. On a real run each becomes a
`NEEDS-HUMAN` verdict, which grades the run to exit 2 until it is performed —
**unless** the runner has the powerstrip hook (§7.1), in which case the two
power-cycle entries run automated and only the cable pull stays on the list.

| # | do this | then observe |
|---|---|---|
| 1 `torture.link.cable-pull` | unplug the DUT's Ethernet cable for 5 s and plug it back into **the same** switch port; then repeat into a **different** port | `LINK_UP`/`LINK_DOWN` both advance and stay within one of each other; the entity is discoverable again; the stream returns **without a controller**; and the SRP reservation is re-established — a stream that returns without a reservation is streaming unshaped |
| 2 `phys.switch-cycle.gm-partition` | power off the AVB switch (DN-1) for ~20 s, then power it back on and wait for links, ssh and gPTP | see §7.1 — the partition *is* the GM loss, the re-join *is* the GM change |
| 3 `phys.dut-cycle.power-cycle` | power-cycle the DUT at the outlet (off ≥ 8 s), wait for the network with **no manual intervention** | see §7.1 — the persistence story: state restored, counters zeroed, boot-to-healthy unattended |

### 7.1 The physical family: powerstrip-driven power cycles

**Authorization.** USER authorization 2026-08-02: the `amx-pi` powerstrip may
be driven by the campaign — **OUT4 = the AVB switch ("DN-1")**, **OUT0 = the
DUT** (the established AX cold-cycle lever: cutting OUT0 loses the SRAM
gateware and QSPI boots it back, which is exactly what makes it a *true* cold
boot). **Per-port cable pulls remain NEEDS-HUMAN** — a powerstrip cannot pull
one cable, and faking a port bounce by cutting the whole switch would assert
something the cable-pull step does not claim.

**Activation.** The hook is an explicit opt-in on the runner; without it the
two cycle steps are handed back `NEEDS-HUMAN` exactly as before (the
no-regression path), and the family's snapshot/proof steps SKIP naming the
flag:

```bash
sudo ./milan_torture.py --areas physical \
     --powerstrip-cmd "ssh amx-pi 'powerstrip {action} {outlet}'" \
     --switch-outlet 4 --dut-outlet 0 \
     --board-cmd 'ssh root@<dut> {cmd}' \
     --csr-cmd 'ssh root@<dut> devmem2 0x90000{addr#0x} w'   # illustrative
```

The strip is probed at startup with a harmless `status` read (never a
switch); a strip whose CLI has no such verb fails the probe harmlessly and is
then **trusted as documented**. `--board-cmd` feeds the uptime, the
shield-posture flags and the `/proc/mtd` persistence probe, `--csr-cmd` (or
`--csr`) the `VERSION` (0x004) and `CLKV_STAT` (0x77C) words — all optional,
and every assertion that misses its input SKIPs naming it. A missing reading
now says **which** of the two causes it was: no `--board-cmd` at all, or a
`--board-cmd` whose command failed or timed out. (`ax-phys-a` supplied
`--board-cmd` and still lost every board reading to a 25 s bound that
`Csr.read` had already had to raise to 60 s for this bench — an ssh-via-pw0
hop into a loaded single-hart softcore. Both are 60 s now, and the SKIP no
longer blames a flag that is already there.)

**The switch cycle** (`phys.switch-cycle.*` — replaces the old gm-change and
gm-loss human entries and adds a trunk-wide link bounce): pre-snapshot (GM
identity on both sides from the ADPDUs, the `AVB_INTERFACE` counters, licence
word, uptime, `VERSION`) → `off 4` → **the partition**: the controller host
reaches both end stations *through* the switch under test, so total
unreachability is the condition applied, not a result — the CSR/board feeds
are paused, one bounded discovery probe records the darkness, and **timeouts
inside the window are never failures** → hold ~20 s (an order of magnitude
past the 3 s announce-receipt timeout, so each island provably elects its own
GM — unverifiable live, verified retroactively) → `on 4` → the recovery
ladder: both entities discoverable again (budget 240 s: the DN-1 must itself
boot before any board is reachable), then exactly **one** non-zero GM in both
ADPDUs (budget 180 s more; `priority1` untouched — recovery must be
automatic, never a forced win) → the retroactive verdicts: **the GM story,
graded against the topology** (below), the counter read twice across a settle
gap and **not still climbing**, asCapable evidenced by someone following a
*remote* GM, the tu lease re-established (`CLKV_STAT` bit 0 back to 0 — the
lease is software, so it is exactly what a recovery can lose), and the DUT
**survived without a reboot** (uptime monotonic; counter monotonicity as the
fallback) → a full **proof pair** (set-format / bind / licence / unbind at the
highest **AAF** indices — never the index-0 alias path, and never the peer's
CRF Media Clock Input), because "the bench recovered" is only a fact once a
stream flows again.

**The GM story is a topology question, not a constant.** `GPTP_GM_CHANGED` is
"gPTP grandmaster change count" (1722.1-2021 Table 7-153; Milan v1.2: "Number
of gPTP GM changes, since boot") — it counts **changes of the grandmaster**.
So which verdict a partition owes depends on what the DUT *was* before it, and
the runner reads that from the pre-snapshot's ADPDU GM view rather than
assuming:

| the DUT was… | assertion | requirement |
|---|---|---|
| the **domain grandmaster** (this bench: `priority1` 238 vs the bridge's 246, so it wins permanently, is alone in its island while the domain is cut, and wins again on the re-join) | `counters.avb_interface.gptp-gm-continuity` | the ADPDU `gptp_grandmaster_id` is **unchanged** and the delta is **exactly 0**. A counter that moves with an unchanged id is a torn latch / partial-id re-read; a changed id with `priority1` untouched is an election it should have held. `…gptp-gm-changed-advances` SKIPs naming why |
| a **follower** of a remote GM | `counters.avb_interface.gptp-gm-changed-advances` | it really did lose its grandmaster, so a small bounded **advance** is owed and a frozen counter slept through the partition. `…gptp-gm-continuity` SKIPs naming why |
| either | `counters.avb_interface.peer-gptp-gm-changed-advances` | the **other** end station is where a permanent-GM DUT's partition is observable, so its counter is read too; a reference device that does not serve `GET_COUNTERS` SKIPs naming that, never a verdict about the DUT |
| either | `counters.avb_interface.link-event-observed` (**INFO**) | `LINK_UP`/`LINK_DOWN` deltas as context. Whether a switch outage is even a PHY event for the DUT is a **cabling** fact: tap1 is an inline regenerating tap on the DUT link and holds the board-side PHY up while the switch side is dark, so a zero delta is expected and is never graded |

Demanding an advance from a permanent GM demands a *non-conformant* count.
Run `ax-phys-a` (2026-08-02) filed exactly that fake red — see
[PHYSICAL_FAMILY_TRIAGE_0802.md](../findings/PHYSICAL_FAMILY_TRIAGE_0802.md).

**The DUT cycle** (`phys.dut-cycle.*` — the old power-cycle entry): 
pre-snapshot → `off 0` → 8 s drain → `on 0` → the zero-touch boot ladder:
discovered again within 360 s (QSPI load + kernel + link guard measured
~5.5 min worst case on this bench — the budget is a bench fact, not a
clause), `VERSION` unchanged (a changed word = the golden-image fallback
engaged), shield posture restored (`eth0` flags `0x1203`, promisc **gated** —
promisc outranks the TCAM drop, so a promiscuous boot has voided its own RX
shield), **the persistence story** (below), the counter block back at zero
(7.4.42 volatility), one GM within 120 s more, the tu lease re-armed → the
proof pair.

**Persistence: the clause is unconditional, the verdict is not.** Milan v1.2
**5.3.8.1**: *"The current format shall be saved in a non-volatile memory and
restored after a power cycle"* (5.3.7.1 for a Stream Output, 5.3.8.2/5.3.8.3
for the bound state and binding parameters, 5.3.10.1/5.3.9.1 for the channel
mappings, 5.3.7.6 for the presentation time offset). It is a **shall**, so
`state.restored-after-power-cycle` is never deleted. But a build with no
writable flash cannot satisfy it by construction, and a red that can never go
green is a red the reader learns to skip past. So the verdict is decided by a
**probe** — `/proc/mtd` over `--board-cmd`, overridable with `--nvm
present|absent`, never inferred from a failed read:

| situation | verdict |
|---|---|
| nothing differs | `PASS` — a device that keeps it, passes, whatever the probe says |
| differs, store **present** | `FAIL` — violated by something that could have held it |
| differs, store **absent** | `KNOWN-PENDING`, naming the clause, what must persist and where it would have to live; it does not fail the run and goes live as a `FAIL` untouched the day the store lands |
| differs, store **unknown** | `SKIP` naming `--nvm` |

Two records sit beside it so a cycle is never left with no verdict on its own
state: `state.self-consistent-after-power-cycle` (**SHALL**, gradable with no
store at all — every descriptor that answered `GET_STREAM_FORMAT` before the
cycle answers again after it with a well-formed 8-octet format: 5.3.8.1's
first sentence plus 1722.1-2021 7.4.10) and `state.format-after-power-cycle`
(**INFO** — what each descriptor actually read back, pre vs post, which is
what makes the gap measurable before it is fixed). On the AX7101 today
`/proc/mtd` lists a header and nothing else, so this grades `KNOWN-PENDING`:
see [PHYSICAL_FAMILY_TRIAGE_0802.md](../findings/PHYSICAL_FAMILY_TRIAGE_0802.md).

**Serialization and the bench-alive guarantee.** The physical area is
registered **last** in `AREAS` — a partition mid-matrix would pollute every
later verdict — and the two families are strictly serial; the `PowerStrip`
interlock refuses to switch a second outlet off while one is dark, so no
future plan edit can violate that silently. If a recovery misses its budget
the runner issues **one** more `on` with an extended wait; if the bench is
still unreachable it FAILs the rung loudly, latches the family dead, SKIPs
every remaining physical step naming the reason, and never touches the strip
again. The campaign ends with the bench alive or loudly declared dead —
never silently dark. A refused `off` is the opposite case: the bench was
never touched, so it is a SKIP and the family continues.

**What still needs a person, and why:** the cable pull (no per-port outlet;
it exercises the link guard, the MAC and the reservation for *one* port while
its neighbours stay up — the switch cycle cannot claim that), and everything
in §9.1's no-runner-op list. Neither is ever faked into a powerstrip step.

---

## 8. The traps

Each of these has cost this project time. They are here so the next maintainer
pays once, not twice.

### 8.1 A bind is not a licence

Milan v1.2 5.3.7.3, verbatim: *"As long as a PAAD is declaring a Talker Advertise
attribute **and** receiving a Listener Ready or Listener Ready Failed attribute
for a Stream Output, it shall be streaming AVTP packets."* The licence is a
**conjunction**, and the second half arrives over MSRP from the listener — an
ACMP `BIND_RX` returning SUCCESS does **not** grant it.

So a bound talker emitting nothing is often a *correct* talker. On this fabric
`LWSRP_STATUS` (`0x694`) bit 8 is the answer, and `0x30` — talker declared,
domain ok, **gate shut** — is what that state reads. The plan orders
set-format → connect → start-if-needed, so this is the state in which *most* binds
are first measured. An earlier version of this layer emitted the frames-advance
verdicts from the bind step, before any `START_STREAMING`, and so filed roughly
**135–285 conformant steps per run** as SHALL violations. The licence is now a
required input and its absence is a SKIP.

### 8.2 An all-zero counter block cannot conclude anything

Milan 5.3.8.10: *"The PAAD-AE shall reset all of these counters to zero each time
the Stream Input changes its state from not bound to bound."* A snapshot taken
immediately after a bind therefore reads 0/0/0 **on a correct device** — and
`abs(0 - 0) <= tolerance` is a definite PASS that also announces which of the two
`FRAMES_RX` readings the device implements, from zero samples. That was the only
state `check_tv_tnv()` was ever called in. All three at zero is now SKIP, and the
block is re-read **after** the streaming window.

### 8.3 A frame budget is not a capture duration

A running AAF stream is ~8000 frames/s. `tcpdump -c 400` therefore captures about
**50 ms** of wire time and shows **zero** ADP, MRP or AECP even though all three
are present — MRP re-declares on its own timers, not per frame. This was briefly
mis-read as *"no MRP on the link."* Capture for a **duration**
(`timeout 8 tcpdump …`), or filter **for** the low-rate protocol you want.

Related: the ProfiShark record header shifts **every** ether offset by +28, so in
a BPF filter the EtherType is at `ether[40:2]`, the destination MAC at 28 and the
source MAC at 34; in a decoder the real Ethernet frame is `pkt[28:]`. The
analyser makes the offset a parameter (`--tap-header`, default 28 with `--tap`)
and its self-test carries a byte vector **with** the header present, because
assuming a header that is not there decodes to nothing — and so does missing one
that is.

And the bring-up trap: `ip link set <if> up` does not start the flow. The tap
passes no frames until a capture socket opens it promiscuously, and `operstate`
reads `unknown` even when it works. **Gate on `rx_packets` after starting
tcpdump**, never on `operstate`.

### 8.4 A short passive discovery window manufactures phantom absences

`avdecc_l2.py`'s `discover` is **purely passive** — it never transmits an ADP
`ENTITY_DISCOVER` — and Milan mandates a 5 s advertise cadence. A 6 s window is a
1.2× margin with no retry, and at ~200 call sites per campaign a spurious *"entity
gone"* FAIL was near-certain every run. The window is now ≥ 11 s (two advertise
intervals) with a retry, and a discovery miss **alone** is a SKIP: only a miss
*plus* an unanswered well-formed AECP command — the real liveness discriminator —
is a FAIL.

### 8.5 An unverified stop destroys the next pair's measurement

There was no `STOP_STREAMING` anywhere in the layer. After the first
`START_STREAMING` latched a talker it stayed latched, so every later pair
measured an **already-streaming** talker and `stream.starts-on-bind-alone`
reported PASS — a false PASS for **94 of the matrix's 95 pairs**. The assertion
that exists to catch a `STREAMING_WAIT` implementation destroyed its own premise.

Every unbind now sends `STOP_STREAMING` and **verifies** it against `FRAMES_TX`.
An unverified or unreadable stop is recorded as *still latched*, and the next
pair SKIPs the question rather than answering it wrongly.

### 8.6 The same counter name means two different things, ~8000× apart

* IEEE 1722.1-2021 **Table 7-153**, `AVB_INTERFACE`: `FRAMES_TX` is *"Total
  number of frames sent out of this interface"*, `FRAMES_RX` *"Total number of
  frames received through this interface"* — **raw totals since boot**.
* Milan v1.2 **Table 5.4** `STREAM_OUTPUT` `FRAMES_TX` and **Table 5.6**
  `STREAM_INPUT` `FRAMES_RX`: *"Incremented at the end of every observation
  interval during which at least one Stream Data AVTPDU has been
  transmitted/received"*, the interval being *"implementation-specific and shall
  be less than or equal to 1 second"* — **observation-interval ticks**.
* IEEE 1722.1-2021 **Table 7-157/7-159** define the *stream-descriptor* symbols
  per **frame**. Both readings are legitimate; they differ by the frame rate.

Consequences, all encoded rather than commented:

1. `TV + TNV == FRAMES_RX` is a **1722.1 identity and not a Milan one**, so
   `check_tv_tnv()` reports which reading is in force instead of asserting one. A
   checker that asserts it unconditionally files a conformant interval counter as
   an 8000× defect — which has already happened once here.
2. A **frame-accurate cross-device comparison may use only** the `AVB_INTERFACE`
   totals, the DUT's RMON lanes, the test machine's NIC statistics or the pcap
   count. `tc.assert_frame_accurate()` **raises** `CounterSemanticError` on a
   stream-descriptor source, so the wrong comparison cannot be *expressed*.
3. The cross-side comparison in **interval terms** is a separate assertion named
   `xside.interval-ticks-agree`, and the word *interval* is in the name so nobody
   later reads it as a frame count.
4. Every cross-side tolerance travels with the reason it is that size:
   8000 frames for snapshot skew (*two AECP round trips plus the DUT's
   `STATS_CTRL` `0x200` snapshot latch put up to ~1 s between the first and last
   read, and one second of class A is 8000 frames*), 2 ticks for interval
   comparisons (*the window edges cut a partial interval at each end*), 8000
   frames for capture edges (*tcpdump starts and stops on its own schedule*). A
   cross-check with an unjustified tolerance is a guess.

Finally: the clause bounds the observation interval **from above only**. So any
interval in (0, 1 s] is conformant — a 5 ms interval ticking 200/s is *not* a
defect. The first version of the band table called 4.001/s … 3999/s "neither",
i.e. the defect, and a passing unit test hardcoding 200.0/s as "the defect"
cemented it. `"neither"` is now reserved for nothing moving at all, and for an
implied interval **longer** than a second.

### 8.7 A lossy test machine invalidates its own verdicts

See §4.6. If the instrument dropped frames, the listener-side numbers it produced
are not evidence about the device.

### 8.8 Index 0 is the alias path

The `0x800` per-stream window makes index 0 a **hard alias** of the legacy flat
registers, so an index-0 pass exercises the alias and not the indexed path. Four
per-index defects hid there. And the coverage audit must be **per area**: over the
whole plan the matrix area's full coverage masks every other area, which is
exactly how the audio area stayed index-0-only under a green report.

### 8.9 An empty collection is a SKIP

`not []` is True. Eight of the analyser's twelve original check families emitted
**nothing** on an empty capture — so the log could not tell *"did not apply"* from
*"was not run"* — and `wt.control.length-honest` emitted **PASS**, with no control
frames present at all. An empty capture is this project's commonest false green
(a mirror port that never joined the stream multicast group). Every family now
emits one SKIP naming what was absent, and the desk suite asserts that no check
PASSes on an empty capture.

---

## 9. Limits, cost and non-coverage

Written down so nobody has to infer it from a green run. This list is meant to be
**exhaustive**; if you find something missing from it, that is a defect in this
page.

### 9.1 What has no runner implementation yet

These `Step`s exist in the plan with their clauses and assertions, and the runner
has no `op_` method for them, so each logs **SKIP naming the op**. That is the
visible edge of the work, not a hole in it — but it *is* an edge:

* `background_load` — the five traffic storms (5 steps, 20 assertions);
* `link_bounce` — the software PHY bounce;
* `malformed_frame` — all nine malformed/truncated-frame mutations (9 steps);
* `maap_conflict` — the DMAC conflict and reallocation;
* `vlan_misconfig` — the wrong SR VID and the VID-0 case (2 steps);
* `starve_source` and `stop_talker` — the two starvation cases;
* `human_action` — by design: these become `NEEDS-HUMAN`.

The physical family's `switch_power_cycle` / `dut_power_cycle` ops **are
implemented**, but run only with the §7.1 powerstrip hook; without it they too
become `NEEDS-HUMAN`, by design and not as a gap.

### 9.2 What is implemented but needs an input it cannot fetch

* **The streaming licence.** `0x694` is a DUT-board CSR and no AVDECC command
  returns it. Without `--licence-status` / `--csr-cmd` every frames-advance and
  unlicensed-silence verdict SKIPs. Same for the RMON lanes (`0x21C`/`0x230`) and
  the per-stream lwSRP row (`0x85C`).
* **Captures.** The runner does not take its own. The `payload` area and both
  audio-identity ops emit the exact `tcpdump` command, the exact filter and the
  exact analyser invocation, and SKIP until a capture is handed to them with
  `--pcap`. Same for the THD+N gate and `--pcm-dump`.
* **The audio identity ops are IMPLEMENTED** (`op_audio_identity_capture` runs
  the production walking-tone decoder over a capture; `op_audio_identity_loop`
  drives **both** binds and grades the return leg's `FRAMES_RX`), but their
  identity verdicts are wire verdicts and so need a capture. Previous versions of
  this page omitted them from the non-coverage list while the runner implemented
  neither, which was the worse of the two failures.
* **`wire.matches-declared-format` on a bind step** always SKIPs and hands off to
  the payload area — a control-plane step has no wire.
* **The stress load needs `--board-addr`** (and `--board-cmd` + `--host-addr`
  for the full iperf3 paths). Without the address there is no load of any kind
  and the load steps SKIP naming it; without a board command path iperf3 is
  unprobeable — never assumed on the busybox rootfs — so RX uses the
  UDP-blast fallback (named in every record; its number is a send rate, not
  goodput) and the TX direction SKIPs, because only the board can source
  board→host traffic.

### 9.3 What it costs

A **full matrix run is roughly 1–1.5 hours, and it is not a smoke test.** The
default 4×4-plus-CRF Arty against the peer's five reachable primaries produces
70 talker×listener pairs (25 outbound, 20 return, 25 intra-DUT loopback) and
262 matrix steps. Each pair
spends about 50 s in deliberate measurement:

* three 4 s counter windows (the bind's growth window, the licence step's
  TX/RX window, the unbind's stop window) plus the cross-side windows;
* one ≥ 11 s ADP discovery per connect and per disconnect — 140 of them, which is
  the single largest cost and the price of not manufacturing phantom absences
  (§8.4).

The `multi` area adds 19 steps (three 4-phase sets plus the 7-phase stress
set). Its verify, load and survivor windows are **shared** across all pairs of
a set, so a whole set costs roughly one bind round + a few 4 s windows (+ two
~16 s load windows for the stress set) + one ≥ 11 s discovery per phase —
minutes, not the matrix's hours — while exercising the aggregate-load shape the
matrix never reaches.

`--plan` prints the totals for whatever shape you configure. Scope a run with
`--areas`; the desk suite is the ~3 s half and should be run every time.

Current totals for the default shape (from `--plan`): **355 steps, 2739
assertions, 3 need a human**, across `matrix` 262 / `multi` 19 / `churn` 25 /
`payload` 7 / `audio` 9 / `torture` 21 / `physical` 12 steps. The physical
area's two cycle steps count among the 3 human entries until the runner is
given the §7.1 powerstrip hook; its budgets put a full physical run at
roughly 10–20 minutes of mostly waiting (20 s hold + up to 240 s + 180 s
switch recovery, 8 s + up to 360 s + 120 s DUT boot, two proof pairs).

### 9.4 What it cannot see at all

* **It does not judge presentation time against gPTP unless a reference is
  supplied.** A pcap timestamp is the capture host's `CLOCK_REALTIME`, not the
  gPTP timebase; comparing them yields a confident number that means nothing.
  Without `--gptp-ref-ns` the class-A transit check reports `SKIP` with that
  reason (methodology R5).
* **It does not flash anything and never touches the console bridge.** It
  power-cycles **only** what it was explicitly armed for — the §7.1 powerstrip
  hook (`--powerstrip-cmd` + the outlet flags), user-authorized 2026-08-02 for
  the switch (OUT4) and the DUT (OUT0), last in the campaign, strictly serial,
  with the bench-alive guard. Without the hook it power-cycles nothing.
* **It does not verify SRP reservations at the *bridge*.** It reads the DUT's own
  `LWSRP_STATUS` as the licence precondition, and it decodes the MSRP/MVRP
  declarations from an inline tap — but whether the *bridge* actually admitted
  the reservation, and what it did with the class measurement interval, needs the
  bridge itself to be queried. That is not done here.
* **It does not measure shaper behaviour** (CBS credit, idleSlope in force,
  per-queue admission). Those are the `0x400` CBS window's own gates.
* **It does not test redundancy (Milan network redundancy), AVDECC
  authentication, or the AEM descriptor tree.** The descriptor tree has its own
  gate and is deliberately not duplicated here.
* **It does not test gPTP itself** — no `sync`/`Follow_Up`/`Pdelay` timing
  analysis, no BMCA state machine checks. It observes `GPTP_GM_CHANGED` and the
  ADPDU's `gptp_grandmaster_id`, which is the AVDECC-visible surface only.
* **It does not test AECP command coverage.** Which AEM commands the entity
  implements, and their per-command payload rules, are the `item10_*` behave
  features' subject.
* **It does not exercise more than one listener per talker beyond the two
  `churn.bind-while-streaming` steps and the `multi` primaries set's cyclic
  assignment** (which shares a talker only when the DUT has fewer AAF talkers
  than the peer has reachable listeners), and it does not test
  `max_supported_streams` at its limit.
* **The `multi` area's licence reading is the global/idx-0 gate (`0x694`).**
  The per-index lwSRP rows (`0x85C`) sit behind the `0x800` window select,
  which needs a board-side pre-step per index; until that is scripted, ONE
  supplied word gates a whole concurrency set, and a per-stream licence
  divergence inside a set is invisible to the runner (the set-level flow
  verdict still catches its consequence).
* **It does not test the CRF stream as an audio path** — a CRF Media Clock Stream
  carries timestamps, so the audio identity checks deliberately exclude the CRF
  index. Its format, rate and timestamp step *are* checked by the analyser.
* **It cannot tell whether the fabric is right about anything it never puts on a
  frame or a counter.** Those are the L0/L1/L2 tiers — the Verilator suites and
  the `check_*.py` gates.
* **`numpy` is confined to the THD+N step.** On a host without it that one step
  reports `SKIP`; the two coherence guards inside
  [`harness/milanharness/thdn.py`](../../harness/milanharness/thdn.py) sit
  *after* its `import numpy`, so they cannot fire there — recorded in
  `audio_walking_tone_identity.feature` rather than worked around.
* **The desk suite carries two deliberately-failing scenarios** (§5.6) — the
  `GET_COUNTERS` per-sink bound and the per-input `STREAM_FORMAT` store. Use
  `--tags ~@open-finding` for a gate. Both are L1 source bindings: they say what
  the RTL in this tree does, and neither is a claim about silicon.
* **The `xside.absent-where-not-registered` pruning check needs a bystander
  side** to be supplied before it can find a leak; with only the talker and the
  listener configured it has no unregistered interface to look at, and SKIPs.
* **The MSRP decode is read-only and best-effort on truncation.** It parses what
  a capture contains and stops at the first field it cannot read (a tap can
  legitimately start mid-PDU); it does not reconstruct MRP state machine timers,
  LeaveAll cycles, or registrar state.

---

> **On the grandmaster entries:** the standing rule is that recovery must be
> **automatic**. Never force the grandmaster back — a forced win hides exactly
> the defect the entry is looking for.
