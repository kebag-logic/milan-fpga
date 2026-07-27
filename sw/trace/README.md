# `sw/trace/` — the CTF fault log

Binary trace logging for "what was happening when it broke". CSR-plane state,
not text; a DRAM ring, not a file on flash; rotating independent `xz` segments
in `/user/log`, written only when something has gone wrong.

**Design record, and the reason every choice was made:**
[`../../docs/design/TRACE_LOGGING.md`](../../docs/design/TRACE_LOGGING.md).

```
milan_trace.yaml ──barectf──▶ generated/metadata        the DECODE ABI
                           ▶ generated/barectf.[ch]     the PRODUCER
                                    │
             milan_trace.[ch]  ─────┴──▶ DRAM ring, 4 KiB CTF packets
                                            │  WARN+ record, rate-limited,
                                            │  flash-wear budgeted
                                            ▼
                      /user/log/seg-NNNNNN.ctf.xz   (board daemon: private repo)
                                            │
        trace_segment.py unpack ────────────┴──▶ ctf_read.py / babeltrace2
```

## Contents

- **[Files](#files)** — One line per file, and the two that carry ABI weight: `milan_trace.yaml` (23 event types, the `sev`/`src` context, the packet shape) and `generated/metadata`, the copy of which travels with every unpacked trace because it is what a reader decodes against.
- **[Run the gate](#run-the-gate)** — One command. Notable: `barectf`, `dtc` and `babeltrace2` are each optional and each produce a *loud skip* when absent, never a silent pass.
- **[Look at a trace](#look-at-a-trace)** — The verify / unpack / read sequence over `/user/log`, including `--min-sev WARN` and the `babeltrace2` fallback.
- **[Change the ABI](#change-the-abi)** — The venv recipe that gets barectf 3.1.2 installed past its stale pins, and the sharp edge behind it: barectf numbers event types by *sorted name*, so adding one event renumbers its alphabetical successors — hence `EVENT_IDS` and the ABI version must move in the same commit.
- **[Build the producer into something](#build-the-producer-into-something)** — The single `cc` line; freestanding C99 with three headers. Use the `MILAN_TRACE()` macro rather than the raw call, so severity reaches the flush arming and not just the record.
- **[What is NOT here](#what-is-not-here)** — The board half — CSR poller, compressor, `/user/log` writer, init ordering — lives in the private test repo; where the boundary is drawn.

## Files

| File | Role |
|------|------|
| `milan_trace.yaml` | **the contract.** barectf config: 23 event types, the `sev`/`src` common context, the clock, the packet shape. Read its header before changing anything — it is an ABI |
| `generated/metadata` | CTF 1.8 TSDL. **This is what a reader needs**, and a copy travels with every unpacked trace |
| `generated/barectf.[ch]`, `generated/barectf-bitfield.h` | the generated producer, checked in so the gate runs without barectf |
| `milan_trace.[ch]` | barectf platform layer: the DRAM ring, flush arming by severity, the rate limiter, the flash-wear token bucket, the segment API |
| `trace_selftest.c` | a scripted replay of this project's real faults through the **shipping** producer; writes raw CTF segments |
| `trace_segment.py` | `pack` / `unpack` / `verify` / `rotate` / `ratio` — the `/user/log` container format, with the pinned xz chain |
| `ctf_read.py` | CTF 1.8 reader, python3 stdlib only, driven by the shipped `metadata` |
| `test_trace_roundtrip.py` | the 14-gate round trip: ABI → producer → segments → xz → truncation → decode |

## Run the gate

```sh
python3 sw/trace/test_trace_roundtrip.py     # -> ALL GATES PASS
```

Needs `python3` and a C compiler. `barectf`, `dtc` and `babeltrace2` are each
optional and each produce a **loud skip** when missing, never a silent pass.

## Look at a trace

```sh
python3 sw/trace/trace_segment.py verify /user/log
python3 sw/trace/trace_segment.py unpack /user/log -o /tmp/trace
python3 sw/trace/ctf_read.py /tmp/trace --format summary
python3 sw/trace/ctf_read.py /tmp/trace --min-sev WARN
babeltrace2 /tmp/trace                       # if installed
```

## Change the ABI

`generated/` is **generated**, and the gate proves it. To change the event set:

```sh
python3 -m venv /tmp/bcvenv
/tmp/bcvenv/bin/pip install setuptools wheel
/tmp/bcvenv/bin/pip install --no-deps barectf
/tmp/bcvenv/bin/pip install "setuptools<81" jinja2 jsonschema termcolor pyyaml
#   (barectf 3.1.2 pins older jsonschema/pyyaml/termcolor than pip will build on
#    a current python; the newer ones work, and `pkg_resources` needs
#    setuptools<81. --no-deps sidesteps the pin, the second install supplies the
#    libraries.)

# edit sw/trace/milan_trace.yaml, then
/tmp/bcvenv/bin/barectf generate \
    --code-dir sw/trace/generated --headers-dir sw/trace/generated \
    --metadata-dir sw/trace/generated sw/trace/milan_trace.yaml

python3 sw/trace/test_trace_roundtrip.py     # gate 3 will show the id renumber
```

Then update `EVENT_IDS` in `test_trace_roundtrip.py` **in the same commit** and
bump `environment.milan_trace_abi`. barectf numbers event types by *sorted
name*, so adding one event renumbers its alphabetical successors — which is
exactly why gate 3 pins the map and why `metadata` travels with the segments.

## Build the producer into something

```sh
cc -std=c99 -O2 -I sw/trace -o app \
   app.c sw/trace/milan_trace.c sw/trace/generated/barectf.c
```

Freestanding C99; `milan_trace.c` uses only `<stdint.h>`, `<stddef.h>` and
`<string.h>`. Emit records with the `MILAN_TRACE()` macro so severity reaches
both the record and the flush arming:

```c
MILAN_TRACE(link, MILAN_TRACE_SEV_WARN, MILAN_TRACE_SRC_LINKMON,
            linkg_stat, link_ctrl, bounce, state, rx, tx, ethrst, grst);
```

## What is NOT here

The board daemon: the CSR poller, the liblzma compressor, the `/user/log`
writer and the init-script ordering all live in the private test repo. The
boundary and a bench recipe for that half are
[`TRACE_LOGGING.md`](../../docs/design/TRACE_LOGGING.md) §11-§12.
