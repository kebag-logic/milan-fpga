# `harness/` — the unattended validation + torture harness

One entry point runs a validation campaign that may take **days**, with nobody
watching. It never prompts, it survives board reboots and network blips, it
checkpoints after every item, and it wakes a human **only** when something is
actually wrong.

> ### ⚠ Status: never run against real boards
>
> Written 2026-07-27. **This harness has driven a mock bench and nothing else.**
> No step below has touched an FPGA, a switch, a power strip or a capture tap.
> Read [Proven vs inferred](#proven-vs-inferred) before trusting any claim on
> this page — a harness that has never driven hardware is exactly the thing that
> reads as validated when it is not.

```sh
harness/run.sh                       # start, or CONTINUE the newest run
harness/run.sh --new                 # force a fresh run id
harness/run.sh --from validation     # resume at a phase
harness/run.sh --only es-4.7         # one item
harness/run.sh --dry-run             # every phase against a mock bench
harness/tests/test_harness.py        # the harness's own gates
```

Detach it however you like — it holds no terminal:

```sh
setsid nohup harness/run.sh > /dev/null 2>&1 &
systemd-run --user --unit=milan-campaign harness/run.sh
```

## Contents

- **[The 3am page (operator contract)](#the-3am-page-operator-contract)** — Written for someone woken with no context: seven numbered steps from "is it alive" (two files, no log parsing) to restarting it. The load-bearing one is step 4 — `FAIL` means the device did something wrong, `BLOCKED` means the harness could not run the item, and only the first ever wakes you.
- **[What is here, and what deliberately is not](#what-is-here-and-what-deliberately-is-not)** — This directory is machinery only. The `es-N.M` item registry lives in the private repo because of what it derives from; the harness reads it by config path and reports a clean `BLOCKED` when absent, so the open tree stays runnable for anyone.
- **[Layout](#layout)** — One row per file: which module owns orchestration, logging, transport, the register ABI, recovery, THD+N, the report, the mock. Start here to find where a behaviour is implemented.
- **[Configuration](#configuration)** — Every bench-identifying value lives in the TOML and nowhere in the scripts, and a leftover placeholder makes the harness refuse to start rather than guess. Also the interpreter split: everything but THD+N runs on bare `python3 ≥ 3.11`, so no-numpy means skipped gates, not failures.
- **[The eight phases](#the-eight-phases)** — What each phase establishes, phase 0 through 7. Note that `baseline` is deliberately read-only — a baseline that perturbs what it measures is worthless — and that everything later is diffed against it.
- **[Logging, and why it is shaped this way](#logging-and-why-it-is-shaped-this-way)** — The run-directory file contract, plus the claim it is built to support: a run is fully reconstructable from the logs alone, which `--report-only` proves by rebuilding the report from JSONL with no bench present. Then the reasoning subsections — how resume works, and *why* `FAILED` and `BLOCKED` are separate, why the alert fires exactly once, and why an undeliverable webhook must never fail a campaign. Ends with the board-side flash-logging path, which is written but has no mtd node in any deployed tree.
- **[Safety rails](#safety-rails)** — Six refusals, not warnings, each traceable to something that already went wrong: no `t > 0` talker with the lwSRP engine off (unpaced ~56 k frames/s takes the peer down), no `A_STRMW_CTRL` commit without staging a sid for that index, destructive steps that revert two ways including a watchdog armed *before* the write, and a recovery check that asserts known-good rather than "responds".
- **[Board-side rules baked into the scripts](#board-side-rules-baked-into-the-scripts)** — The constraints the board imposes: no `scp`, no Python, and `devmem` at ~0.75 s per call — which is why a full snapshot is one `dd` plus one `od`, self-validating against the `ID` magic. Also the `0x800` window discipline and the fact that a bind edge clears the per-stream error counters.
- **[Testing the harness](#testing-the-harness)** — Three commands: the gate suite, a full mock campaign, and the fault-injection form. The gates run real code rather than inspecting it, and explicitly do not touch hardware.
- **[Proven vs inferred](#proven-vs-inferred)** — The honesty section, and the reason for the banner at the top of the page. A claim-by-claim table of what the 107 gates actually established (THD+N recovers a known distortion to 0.5 dB; the alert fires once; a torn JSONL line does not lose the run), then an itemised list of everything that needs a board and has therefore never run — board scripts, the detached revert, every controller-driven item. One-line summary: the machinery is tested, the bench interaction is not.
- **[Limits](#limits)** — Three kinds of gap kept visible rather than silent: hardware this lane did not have, the four things that need a human (first contact, outlet characterisation, reading a `BLOCKED` tail, transcribing the stub rows), and a table of items that **cannot** be automated at all with the reason each one reports `BLOCKED` — several of which are wire injectors that do not exist, and one of which is a real parser gap (`mr` is not extracted).

## The 3am page (operator contract)

You have been woken. You have no context. This section is the whole contract.

**1. Is it alive?** Two small files answer it; you never have to parse a log.

```sh
cat <run-root>/<run-id>/STATUS          # RUNNING | FAILED | DONE + one line
cat <run-root>/<run-id>/heartbeat.json  # {phase, item, iteration, timestamp, pid}
```

A `timestamp` older than a few times `[run].heartbeat_secs` (default 15 s) means
the process is gone or wedged — the run itself is resumable either way.

**2. What does `STATUS` mean?**

| value | meaning | what you do |
|---|---|---|
| `RUNNING` | in progress | nothing |
| `DONE` | finished; everything that could run passed | nothing. If it also says *"(N blocked)"*, N items could not be run — see step 4 |
| `FAILED` | a real defect was found | step 3 |

**3. On `FAILED`.** The alert body already named the item and the reason. The
evidence is captured and stands alone:

```sh
ls   <run-root>/<run-id>/forensics/          # one bundle, from the FIRST failure
cat  <run-root>/<run-id>/forensics/*/failure.json   # item, reason, seed, both boards' CSRs
tail -50 <run-root>/<run-id>/forensics/*/harness.log.tail
```

The run does **not** stop at the first failure and does **not** alert again —
later failures are recorded normally. Read `report.md` for the full picture.

**4. Is it a device defect or a harness problem?** That distinction is the
verdict itself, and you do not have to infer it:

* **`FAIL`** = the device did something wrong. Only this raises an alert.
* **`BLOCKED`** = the harness could not run the item — board unreachable, tool
  missing, no injector for that provoker, registry not configured. Every
  `BLOCKED` record carries the reason in plain words. **These never alert.**

```sh
# every blocked item and why, from the record alone
grep '"verdict": "BLOCKED"' <run-root>/<run-id>/jsonl/*.jsonl
```

**5. Restart it.** With no arguments it continues the newest run from its
persisted cursor — completed phases are skipped and it resumes at the next item.

```sh
harness/run.sh                      # continue where it stopped
harness/run.sh --from adversarial   # or force a phase
harness/run.sh --only es-4.7        # or one item
harness/run.sh --report-only <run-id>   # rebuild the report, no bench needed
```

**6. Is the bench safe right now?** Every destructive step reverts itself two
ways and the harness proves the box is known-good afterwards (see
[Safety rails](#safety-rails)). If you want to check by hand:

```sh
ssh <board> 'sh -s' -- <csr-base> <version> <netif> < harness/board/known_good.sh
```

**7. Where is everything?** `<run-root>` is `[run].root` from your config;
`<run-id>` is the newest `run-*` directory under it. Layout is in
[Logging](#logging-and-why-it-is-shaped-this-way).

## What is here, and what deliberately is not

This directory is **machinery**: the runner, the eight phase drivers, the
logging / resume / heartbeat / `STATUS` layer, the analysis code (THD+N,
latency), the config schema, the board-side POSIX `sh` scripts, and the
self-tests.

The **item registry** — the `es-N.M` rows with their procedures, expected values
and pass criteria — is *not* here. It lives in the private test repository's
`validation/` directory, because it is derived from material that must not enter
this tree. The harness reads it from a path in the config and reports a clean
`BLOCKED` when that path is absent, so the open tree stays runnable and
self-testing for anyone.

Only item **IDs** appear in this repo. The current compliance verdict and
public evidence are in
[`../docs/testing/MILAN_V12_AUDIT_2026-08-16.md`](../docs/testing/MILAN_V12_AUDIT_2026-08-16.md).

## Layout

| Path | What |
|---|---|
| `run.sh` | the entry point (interpreter resolution + `python3 -m milanharness`) |
| `milanharness/runner.py` | phase/item orchestration, timeouts, checkpoints, escalation |
| `milanharness/log.py` | run directory: JSONL, human log, `STATUS`, heartbeat, cursor, forensics |
| `milanharness/config.py` | config loading + validation (stdlib `tomllib`) |
| `milanharness/registry.py` | item registry loader (file lives in the private repo) |
| `milanharness/transport.py` | ssh / jump host / board script push, retry + outage records |
| `milanharness/csr.py` | register ABI, batched reads, SNAP discipline, safety rails |
| `milanharness/recovery.py` | restore the binding, then PROVE known-good |
| `milanharness/counters.py` | the counter audit engine (provoke / expect / neighbours) |
| `milanharness/thdn.py` | coherent, un-windowed THD+N |
| `milanharness/latency.py` | tap decode, in-system split, pto sweep verdict |
| `milanharness/notify.py` | the one-shot alert hook |
| `milanharness/report.py` | the final report, rebuilt from the JSONL alone |
| `milanharness/mock.py` | the mock bench `--dry-run` runs against |
| `milanharness/phases/` | `p0_baseline` … `p7_soak` |
| `board/*.sh` | board-side POSIX `sh` (no Python on the boards) |
| `config/bench.example.toml` | the config template — every bench value lives here |
| `config/counters.toml` | the counter audit table |
| `tests/test_harness.py` | the gates (`ALL GATES PASS`) |

## Configuration

Everything bench-identifying is in the config file and **nowhere in the
scripts**: ssh aliases, interface names, outlet numbers, the alert webhook. A
placeholder left in place makes the harness refuse to start rather than guess.

```sh
cp harness/config/bench.example.toml ~/.config/milan-harness.toml
$EDITOR ~/.config/milan-harness.toml
MILAN_HARNESS_CONFIG=~/.config/milan-harness.toml harness/run.sh
```

Register **offsets** are compiled in — they are the stable ABI of
[`../docs/reference/REGISTER_MAP.md`](../docs/reference/REGISTER_MAP.md). Only
the window base is configuration.

### Interpreter

Everything except THD+N runs on a bare `python3 >= 3.11` (`tomllib` is standard
library there — no third-party dependency, so the harness starts on a jump
host). THD+N needs `numpy`, which is **not** installed system-wide on the dev
box; point `[exec].python` (or `$MILAN_HARNESS_PYTHON`, or a `.venv` beside
`run.sh`) at a virtualenv that has it. Without it the THD+N items report
`BLOCKED` and the self-tests report those gates as skipped, not failed.

## The eight phases

| # | Phase | What it establishes |
|---|---|---|
| 0 | `baseline` | full CSR/counter/state snapshot of both boards + the controller host, latency taps, RMON capability. Read-only — a baseline that perturbs what it measures is worthless. Everything later is diffed against it |
| 1 | `smoke` | the post-flash contract: `VERSION` reads the expected word, host plane up, chmap + slot 0 re-armed, peer re-bound **and accepting**. Explicit abort criteria |
| 2 | `validation` | every `es-N.M` item, plus the BDD conformance suite (`cd tests && behave`) |
| 3 | `counters` | the ATDECC counter audit |
| 4 | `matrix` | formats × channel counts × rates, randomised per stream with a recorded seed; mapping permutations; BRAM vs DRAM ring; wire vs MAC loopback; the peer board as an independent oracle |
| 5 | `adversarial` | controller storms, two controllers contending, pto and stream-format changes mid-stream, reservation exhaustion, link events, combinations |
| 6 | `quality` | THD+N over all frames per configuration; the pto sweep; in-system latency |
| 7 | `soak` | long run with periodic assertions: counter saturation, ring lap, servo drift |

## Logging, and why it is shaped this way

Everything lands in `<[run].root>/<run-id>/`:

| File | Contract |
|---|---|
| `STATUS` | **the** contract: one of `RUNNING` / `FAILED` / `DONE` plus a one-line reason |
| `heartbeat.json` | `{phase, item, iteration, timestamp, pid}`, rewritten every `[run].heartbeat_secs` — answers "is it alive" without parsing a log |
| `jsonl/<phase>.jsonl` | append-only, one record per check: item id, phase, verdict, measured values, timestamp |
| `harness.log` | human-readable, rotated and gzipped at `[run].human_log_max_bytes`, at most `[run].human_log_keep` parts |
| `cursor.json` | the resume cursor (completed phases + items) |
| `forensics/<item>-<time>/` | captured once, on the first failure |
| `report.md` / `report.json` | the final report |

**A run is fully reconstructable from the logs alone.** The report is rebuilt
from the JSONL rather than from memory, which is what proves that claim —
`run.sh --report-only <run-id>` regenerates it from a finished or crashed run
with no bench present.

**Bounded growth** matters on a multi-day run: JSONL rotates per phase (never
rewritten — append-only), the human log rotates and gzips with a cap on parts,
per-item captured output is capped by `[run].max_item_output_bytes`, and a phase
refuses to start below `[run].min_free_disk_mb`.

### Resume

The cursor is written **after every item, before the next one starts**. Running
with no arguments picks it up: completed phases are skipped (with a `resume`
record saying exactly what was skipped) and the run continues at the next item.
`--from <phase>` and `--only <item>` override it. A crashed run never means
starting over.

### `FAILED` vs `BLOCKED` — and why they are separate

Contract: [Section 6b of `../docs/testing/TESTING.md`](../docs/testing/TESTING.md#6b-unattended-campaigns----status-file-and-alert-webhook). The
field names and POST shape here follow that section rather than inventing their
own.

* **`FAILED`** — a real defect in the device. On the **first** one: `STATUS` goes
  `FAILED`, a forensic bundle is captured (both boards' full CSR snapshots, the
  failing item's inputs, the RNG seed, log and record tails), and the alert hook
  fires **once**.
* **`BLOCKED`** — the harness could not run the item: board unreachable, tool
  missing, registry absent, no injector for a provoker. Counted and reported,
  **never alerted on**.

**Why separate.** Waking someone because a board was unreachable is the false
alarm that teaches people to ignore the *next* alert — and the next one is the
real defect. Silence has to mean "healthy", so anything that is not a device
fault must not break the silence. The split also keeps the report honest: a
`DONE` run that says *"(31 blocked)"* is visibly not the same claim as a `DONE`
run with none.

**Why the alert fires once.** A single defect at 02:00 that re-alerts per
subsequent failure produces a hundred messages by morning, which is
indistinguishable from noise and gets the channel muted. One message, then the
run continues recording. Escalation state survives a resume: the runner reloads
it from the run's own records, so restarting a `FAILED` run does not re-alert.

**Why a failed webhook must never fail the campaign.** The endpoint being down
says nothing about the device under test. Treating a delivery failure as a test
result would throw away hours of valid campaign because a notifier was
restarting. So `curl` is timeout-bounded (`[notify].alert_timeout_s`), its exit
status is recorded in the JSONL, and the run carries on either way. An alert
that cannot be delivered is a logging problem, not a test result.

**Why the endpoint is config, not code.** It is site information; it also
changes far more often than the harness does. Unset is a clean no-op — the
campaign still runs and still records everything, it simply has no off-site
channel.

### Board-side flash logging — and why the host owns the record

The **host** log is the primary record and is complete on its own; no result
depends on board-side storage. Two reasons, both structural:

* **Capacity.** A multi-day campaign produces far more than the 2 MiB the board
  reserves for a writable area. The host has no such ceiling.
* **Survivability.** The host is the only thing guaranteed to outlive a board
  that hangs. A record that lives on the thing being tested disappears exactly
  when it matters most.

Board-side flash logging therefore exists only for the case the host *cannot*
observe: a fault where the board dies before it can report.

**That path is not available today.** `sw/dts/mtd-partitions.dtsi` is generated
but nothing appends it to the base tree, and its own banner records that no
deployed tree carries an mtd node and no mtd driver is known to bind to this
controller in this kernel configuration. `board/flashlog.sh` therefore degrades
silently to host-only and records the falsifier's answer
(`cat /proc/mtd`) in the run. When a partition appears and is mounted, it starts
working with no code change and the harness picks it up automatically.

## Safety rails

These are refusals, not warnings.

1. **Never arm a `t > 0` talker with the lwSRP engine off.** Class-A pacing on
   the extra-talker path comes from the reservation bandwidth gate, not a timer:
   with the engine off an armed extra context transmits unpaced (~56 k frames/s
   measured against the paced ~10.4 k/s) and takes the peer board off the
   network — and the arm is silently dropped in that state anyway. `arm_context()`
   verifies the engine on the board rather than trusting the caller, and a
   disarm sweep runs at the end of every phase that could have armed one.
2. **Never commit `A_STRMW_CTRL` without staging a sid for that index.** An
   unstaged commit is what detached the entry-0 ACMP alias.
3. **Every destructive step auto-reverts, two ways.** `board/reverting_step.sh`
   sets a `trap` for ordinary death *and* arms a detached watchdog **before** the
   destructive write, so the register is restored even if the script is killed
   or the board panics the shell.
4. **Steps that cut our own session run detached and are read back.** Link
   events, MAC loopback and MAC reinit go through `push_sh_detached()` +
   `read_detached()`; the ssh channel is not allowed to be load-bearing.
5. **Recovery asserts KNOWN-GOOD, not "responds".** `board/known_good.sh` runs
   positive checks per plane and one **movement** check on the RX parser —
   because a board that answers ssh, answers `devmem` and reports a bound
   listener can still be accepting nothing, and half-recovered is the dangerous
   outcome.
6. **Power outlets are characterised, never assumed.** Nothing is allowed to
   treat an outlet as "the cable" until a toggle-observe-restore pass in *this*
   run says what it drops.

## Board-side rules baked into the scripts

* **No `scp`** (dropbear): scripts are pushed with `ssh <board> 'sh -s' < script`.
* **No Python on the boards**: board-side steps are POSIX `sh` + `devmem`.
* **`devmem` costs ~0.75 s per invocation** on the softcore — 800 calls once took
  over ten minutes. `board/csr_snapshot.sh` therefore block-reads `/dev/mem`
  with ONE `dd` and decodes it with ONE `od`, **self-validating against the `ID`
  magic** before the decode is trusted, and falling back to per-register
  `devmem` (recording which path it used) when the block reader cannot prove
  itself.
* **The `0x800` window discipline**: write `SEL`, write `SNAP`, poll busy, then
  read. Until a re-poll lands the snapshot-served words read a literal `0`,
  which looks exactly like "no bind" and is not — `csr.window()` reports
  `fresh: false` for that case.
* **A bind edge clears the per-stream error counters**, so anything that cares
  is read *before* a re-bind.

## Testing the harness

```sh
harness/tests/test_harness.py        # ALL GATES PASS
harness/run.sh --dry-run --new       # full campaign against the mock bench
harness/run.sh --dry-run --dry-run-fault known_good:media-plane
```

The gates run real code rather than inspecting it. They do **not** run against
hardware — see the next section for exactly where the line is.

## Proven vs inferred

Written 2026-07-27. Numbers below come from the commands named beside them, run
on the dev box in this worktree. **No board, switch, power strip or capture tap
was involved in any of them.**

### Proven — the harness's own gates and a full mock campaign

`harness/tests/test_harness.py` → **107 gates, `ALL GATES PASS`** under a venv
with numpy; **101 gates + 1 skipped** (the THD+N block) under the system
`python3` 3.14 with no numpy. Specifically established:

| Claim | How it was established |
|---|---|
| THD+N recovers a *known* distortion level | a synthesised exact-period tone with one injected harmonic at −80 / −60 / −40 dB is measured back to within 0.5 dB |
| a clean synthesised tone reads far below the acceptance threshold | measured < −120 dBFS on the same path |
| the windowing trap is real, not a style opinion | a Hann window on the same coherent capture inflates the residual by > 20 dB versus no window |
| a non-exact-period tone is refused, not approximated | 997 Hz at 48 kHz raises rather than returning a number |
| in-system latency excludes the pto stage correctly | synthetic tap words → RX `d0+d1` = 0.80 µs last / 0.85 µs max at 100 MHz, while the whole chain including the ring-fill is 125.8 µs |
| a timed-out / saturated tap chain is flagged untrustworthy | `LTAP_RX_INFO` with a nonzero timeout count flips `trustworthy` false |
| the pto sweep fails on ONE bad point, not on average | three-point sweep with one outlier verdicts false |
| JSONL is append-only, per-phase, sequenced, and capped | records written, re-read, sequence continuity checked across a re-open |
| a torn last record does not lose the run | a truncated trailing line is skipped and the rest still parses |
| the human log rotates, gzips and is bounded | 200 forced writes → rotated parts capped at `human_log_keep` |
| `STATUS` transitions RUNNING → FAILED → DONE | written and read back through the public API |
| the resume cursor really resumes | a run stopped after `baseline` skips it, records a `resume` mark, and continues into `smoke` |
| `--only` restricts to one item | 1 check recorded, all of it the selected item |
| the alert fires exactly once | second failure recorded, no second dispatch |
| the alert body matches the documented shape and length | `milan campaign FAILED: <item> - <reason> (host …, run …)`, ≤ 220 chars |
| an undeliverable alert does not fail the campaign | `curl` rc 7 recorded, run continues |
| the endpoint URL is not copied into the record | the JSONL says `configured`, never the URL |
| BLOCKED never alerts | 21 blocked items in the failure run, still exactly 1 alert |
| the forensic bundle stands alone | item, reason, seed, both boards' CSR snapshots, log tail, record tail |
| the report is rebuilt from the JSONL alone | `report.build()` over the records reproduces the run |
| a failing run does not claim the verdict line | "Milan validated" absent from a `FAILED` report |
| the counter engine catches a mis-wired counter | a neighbour moving fails the row; a counter going backwards fails; an unreadable one is BLOCKED |
| declared-unsupported RMON lanes are checked on BOTH halves | `STATS_CAP` bit 0 *and* the lane reading 0 |
| the `t > 0` / engine-off rail refuses | `SafetyViolation` raised; a correctly staged arm with the engine on is allowed |
| an unstaged `A_STRMW_CTRL` commit refuses | `SafetyViolation` raised |
| a transient outage is survived | 2 injected unreachable attempts, then success |
| a persistent outage becomes BLOCKED, never FAIL | `Outage` raised and mapped to BLOCKED |
| a full CSR snapshot costs ONE remote call | 114 registers in 1 call against the mock |
| every board script is valid POSIX `sh` | `sh -n` on all six |
| the snapshot fast path is a block read, self-validating | asserted structurally: one `dd`, one `od`, and the `ID` magic check |
| the watchdog is armed BEFORE the destructive write | asserted on source order in `reverting_step.sh` |
| no script carries a bench identity | home paths, address literals and bench hostnames grepped for across all board scripts and Python sources |

`harness/run.sh --dry-run --new` drove **all eight phases** against the mock and
reached `DONE` with 31 blocked (no controller tool, no registry configured in
that config). With the registry and a controller configured, the fixture's
implemented items execute their runners and its stubs still appear as visible
`not-implemented` rows — 5 of 5 fixture rows produced a record.

`--dry-run-fault known_good:media-plane` reached `STATUS FAILED`, wrote exactly
one forensic bundle, dispatched exactly one alert, and left the 21 blocked items
in the same run silent.

### Inferred — designed, reviewed against the tree, never exercised

Everything that requires a board is **unexercised**. Named individually so none
of it reads as tested:

* **The board scripts have never run on a board.** `sh -n` proves syntax, not
  behaviour. In particular the `dd`/`od` block read in `csr_snapshot.sh` depends
  on busybox option support this bench has not been asked about — which is
  precisely why it self-validates against the `ID` magic and falls back to
  per-register `devmem`, and why the chosen path is recorded per snapshot. First
  real run: check `#METHOD=` in the record before believing a timing claim.
* **The detached self-reverting step has never been killed for real.** The
  `trap` plus pre-armed watchdog is the design; the mock returns its verdict
  immediately and cannot simulate a board that panics mid-step.
* **`devmem` cost** (~0.75 s per invocation; 800 calls > 10 min) is a bench
  measurement reported to this lane, not something re-measured here. It is the
  premise for batching, not a result of it.
* **Every register semantic** is read from
  [`../docs/reference/REGISTER_MAP.md`](../docs/reference/REGISTER_MAP.md) at
  `VERSION 0x0001_0013`. The mock reproduces those semantics *as documented*; if
  the map and the gateware ever disagree, the mock agrees with the map.
* **The latency shape in the mock** (RX `d0` ≈ 50 cyc, `d1` ≈ 30 cyc, `d2` ≈
  10378–12541 cyc) is seeded from the silicon reading recorded 2026-07-26 in
  [`../docs/AAF_LATENCY_TAPS.md`](../docs/AAF_LATENCY_TAPS.md). It is a
  *fixture*, not a measurement by this harness.
* **The THD+N reference** (−147.99 dBFS, acceptance ≤ −120 dBFS) is a bench
  result supplied to this lane, carried into the config as a threshold. This
  harness has measured only synthesised tones.
* **The audio capture path** (`arecord -t raw -f S32_BE`, the base64 pull) is
  untried: no card was present.
* **Power-strip behaviour** is deliberately uncharacterised. The harness
  enumerates outlets and refuses to treat any of them as "the cable" until a
  toggle-observe-restore pass in a real run says what each one drops.
* **Controller-driven items** (most of `es-*`, most counter provokers, the pto
  sweep, the storms) have never issued a real command; the mock answers every
  unrecognised command with rc 0, so the dry run exercises the harness's control
  flow around them and *not* the device's response.
* **The 60 stub registry rows** have no runner at all. They are visible, not
  verified.

**The one-line summary an auditor should take away:** the machinery is tested,
the bench interaction is not. First contact with hardware should be
`--dry-run`-free but `--phases baseline` only, with `#METHOD=` and the
known-good verdict read by a human before anything destructive is enabled.

## Limits

### What needs hardware this lane did not have

Nothing in [Inferred](#inferred--designed-reviewed-against-the-tree-never-exercised)
has been exercised: two boards, a jump host, a power strip, a capture tap, an
ALSA capture device and a controller host are all required external bench
equipment only, not target runtime, and none was available. A new bitstream
was building while this was written, and the brief
was explicitly to deliver scripts plus their self-tests, not a bench run.

### What needs a human

* **First contact.** Read `#METHOD=` (block vs `devmem`) and the known-good
  verdict by eye before enabling any destructive phase.
* **Outlet characterisation.** The harness enumerates outlets and refuses to
  assume; deciding to toggle one is an operator act.
* **Reading a `BLOCKED` tail.** A run finishing `DONE (N blocked)` is not
  "Milan validated" — someone has to decide whether each blocked item is
  acceptable for that campaign.
* **Transcribing the 60 stub registry rows** (private repo `validation/`).

### What cannot be automated at all, and why

Recorded here rather than left as silent gaps — each of these reports `BLOCKED`
with its reason on every run:

| Item / counter | Why |
|---|---|
| `es-1.1` DUT-wins-BMCA variant | the bench switch outranks every profile-legal end-station value and has no management interface; needs a gPTP claimant model on the wire |
| `stream_input.SEQ_NUM_MISMATCH` | needs a wire injector that skips one `sequence_num` |
| `stream_input.TIMESTAMP_UNCERTAIN` | needs a talker `tu` edge on a real GM change — the switch owns the GM claim |
| `stream_input.MEDIA_RESET` | the parser does not extract the `mr` bit, so nothing can tick it (a known gap, not a harness limitation) |
| `stream_output.MEDIA_RESET` | no CSR view of it exists to read |
| `rmon.RX_ERROR_BAD_FCS`, `rmon.RX_ERROR_BAD_FRAME` | the NIC computes FCS in hardware; needs a bad-FCS / malformed-preamble injector |
| `rmon.RX_FIFO_BAD_FRAME` | needs a raw-socket runt injector on the controller host |
| `clock_domain.FORMAT_ERR`, `clock_domain.SEQ_ERR` | need an off-profile CRF injector |
| Consume-path audio on a sealed listener | the capture tap does not exist on a device we do not control |
| Board-side flash logging | no mtd node in any deployed tree (falsifier: `cat /proc/mtd`) |
