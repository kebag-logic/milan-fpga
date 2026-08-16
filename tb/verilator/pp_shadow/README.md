<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# pp_shadow — milan_datapath with the protocol processor AS the control plane

`make` - exit 0 = PASS. **248 checks, 0 failures, 0 warnings** at the time of
writing. The suite carries no `-Wno-*` at all (not even `-Wno-fatal`), so any
Verilator warning stops the build; gate on the **exit code**, never on a warning
count.

## Contents

- **[The premise inverted (2026-08-13)](#the-premise-inverted-2026-08-13)** — This suite used to prove the processor transmitted NOTHING; with the legacy plane deleted its TX is the wire, so every discipline check was turned around
- **[What it proves](#what-it-proves)** — The class-D fabric face, the byte-exact ADPDU rebuilt from the 0x600 CSR group, the ACMP answer, and clean interleaving with MAAP through the shared control arbiter
- **[The AECP answer, and the memory behind it](#the-aecp-answer-and-the-memory-behind-it)** — What the µCPU actually answers, why every check decodes the response frame instead of a counter, and how the harness backs the nine descriptor-memory ports with a real AEMI image
- **[The blanket PINMISSING waivers came out (2026-08-13)](#the-blanket-pinmissing-waivers-came-out-2026-08-13)** — Why a tree-wide missing-pin waiver is an undriven input in disguise, what the six findings it was hiding turned out to be, and the two files now waived by name
- **[What is no longer here](#what-is-no-longer-here)** — The drain-mode and absolute-silence sections, and the parity-against-the-shipping-planes argument, all of which lost their subject when those planes were deleted
- **[Two traps this suite exists to not fall into](#two-traps-this-suite-exists-to-not-fall-into)** — The tvalid-only monitor tap (gh #65) and the false green a silently-skipped build produces
- **[Time compression — and why this suite carries the control-plane coverage](#time-compression--and-why-this-suite-carries-the-control-plane-coverage)** — Why the timer prescalers are compressed for simulation, and why this is now the only suite exercising 1722.1/SRP behaviour end to end
- **[Note on group B's frame (corrected 2026-08-12)](#note-on-group-bs-frame-corrected-2026-08-12)** — A correction to the frame this group injects, kept as a record of what the earlier version measured and why it was wrong
- **[Note on group I's third probe (2026-08-13)](#note-on-group-is-third-probe-2026-08-13)** — Why the third probe in group I behaves differently from the first two, recorded so it is not mistaken for a flake

## The premise inverted (2026-08-13)

This suite used to be the *shadow* half of a parity contract: the processor was
elaborated beside a live legacy 1722.1/SRP plane with `tx_drain_i = 1`, and its
safety property was that the MAC TX port stayed **silent** no matter how hard
the processor wanted to transmit. `milan_dp` proved the OFF side.

**There is no OFF side any more.** The legacy ADP advertiser, ACMP
talker/listener, AECP/AEM engine and lwSRP applicant are deleted from this
repository. `milan_datapath` instantiates `KL_pp_shadow` unconditionally, ties
`tx_drain_i` to 0, and merges the processor's packed TX with MAAP's through
`ctl_tx_mux`. So the property is the exact opposite of what it was: **the
processor's frames MUST reach the MAC**, and a silent wire is now the failure.

The name is kept because the wrapper's name is kept; the suite is a
**substitution harness**.

## What it proves

| # | Check group | What it establishes |
|---|---|---|
| A | presence + CSR window | `PP_STAT[31:24]` is a constant `0x5B` tag, so a structural zero can never be read as "present and idle"; `TXARB_DIAG` decodes with its `0xA7` tag and its lanes 7:4 read the documented structural zero |
| P | **the saved-state verdict does not lie** | with `restore_go` driven pre-enable, `PP_STAT` must NOT read as a successful restore on a build whose NVM device face is a blank-flash responder. Graded through the decoder software already has (`done && !fail && !alarm`), so the fix had to land in an encoding existing readers understand, plus `[6] nvm_backed = 0` and `[7] nvm_blank = 1` for the three-way distinction. Before `0x0045` this read `0x5B00_0004`, byte-identical to a genuine restore of every sink |
| B | RX classify → FIFO → serializer → validator | an ADP `ENTITY_DISCOVER` is accepted end to end; the counter only moves when the **processor** took a whole frame |
| C | the classifier rejects non-control traffic | 8 IPv4 frames leave `rx_frames` flat. This is the check that protects the board — see the rate note below |
| D | **substitution** | the processor is run until *it* transmits (`tx_frames > 0`) and frames must **egress** at the MAC boundary over the same window. Catches a build that left `tx_drain_i` asserted or never connected the `ctl_tx_mux` leg — with the legacy plane gone, a drained processor answers nothing at all |
| E | side port over the CSR bridge | the snapshot window answers with the processor's own magic `0x4B4C5050` "KLPP" — generated inside `protocol_processor_top`, so it is proof the fabric is alive and clocked, not that the bridge returns a plausible constant |
| F | **the ADPDU, decoded byte-exact** | the `ENTITY_AVAILABLE` that egresses is rebuilt from the `0x600` CSR identity group (entity_id, entity_model_id, capabilities, the RO `0x618`/`0x61C` shape words, the gPTP pair) and compared **octet for octet**; `available_index` is graded separately for strict growth |
| G | the **class-D fabric face** is reachable *and live* | `adp_next_avail_index_o` reads 0 before the first advertisement and has advanced after it |
| H | the **MAAP adapter refuses safely** | with no claimed block, every request is still accepted **and answered** (`ok = 0`), the DA gate stays shut, the plane keeps serving — and the refusal is visible on the wire as `TALKER_DEST_MAC_FAILED(3)` |
| I | the **MAAP adapter grants** | with `KL_maap` in ANNOUNCE the request returns `ok = 1` with `base + source_index` (checked against `MAAP_STAT0`), `acmp_declaring_o` goes HIGH, and the next `PROBE_TX` is answered **SUCCESS** naming `{station MAC, uid}` and the granted `stream_dest_mac` |
| L | **the device ANSWERS AECP** | `READ_DESCRIPTOR` returns `SUCCESS` with `configuration_index`/`reserved`/the descriptor **byte-exact against the image**; a locate miss returns `NO_SUCH_DESCRIPTOR` and a bad configuration index `BAD_ARGUMENTS`, both with the IEEE §7.4.5 4-byte `{type, index}` stub; `GET_COUNTERS` and `GET_AUDIO_MAP` are answered from this repository's own faces (the Table 7-157 mux; the render map RAM under the 0x001C index law, cross-read through `CHMAP_LOOP`); an unimplemented opcode returns a conformant `NOT_IMPLEMENTED` **echo**; `IDENTIFY_NOTIFICATION` sent as a command returns `BAD_ARGUMENTS`; and the two cases the standard allows to be ignored are ignored *without wedging* |
| M | **no descriptor memory** | with the memory model withdrawn, `READ_DESCRIPTOR` degrades to a well-formed `NO_SUCH_DESCRIPTOR` rather than hanging the µCPU, and the store serves again once memory returns |
| K | **the shared control lane** | both legs of `ctl_tx_mux` transmitted, every frame is well formed, and no TX-trunk arbiter aborted or stalled. AECP responses are in that census, so a response that was well formed in isolation but corrupted by the shared lane fails here |
| J | global anti-wedge invariant | `accepted == answered` over every cycle simulated, and **no `RELEASE_DA` is reachable in this shape**: `milan_datapath` ties `cfg_src_en_i` to all-ones, so no talker source can leave the configuration. Graded rather than assumed, because the owed-release law (a release booked per source and retried until the face ACCEPTS it, ahead of any `ALLOC_DA`) is proven in `protocol-processor/tb/acmp_talker` section L. Wire `cfg_src_en_i` to anything live and this check goes red, which is the reminder to bring that path under test here too |

### Group F — why a decode and not a count

A frame census cannot tell an `ENTITY_AVAILABLE` from a runt, and it cannot tell
a correctly assembled ADPDU from one whose `talker_stream_sources` came from a
boot script frozen at another shape. The whole 82-octet frame is rebuilt from
the CSRs and compared. That comparison doubles as the **sharpest corruption
detector for the shared lane**: one MAAP beat spliced into the ADPDU and the
compare fails at a named octet offset.

The **wire-vs-CSR shape law** (`ADPDU talker_stream_sources == 0x618` and its
three siblings) used to live in `milan_dp`. It moved here, because the
advertiser is the processor's now and its cadence is out of reach at
`milan_dp`'s real-time millisecond — see "Time compression" below. `milan_dp`
keeps the other half of that law, the one about elaboration rather than about a
plane: the count and the capability bit must agree.

### Group K — what "interleave cleanly" is graded as

`ctl_tx_mux` merges the processor's packed TX with `KL_maap`'s
PROBE/ANNOUNCE PDUs. The graded facts are:

* **both legs transmitted** — an interleave test in which only one source ever
  sends proves nothing, so the census must show processor PDUs *and* MAAP PDUs;
* **every frame is well formed** — for each AVTP control PDU the declared
  `control_data_length` must account for the frame's actual length
  (`14 + 12 + cdl`, padded to 60). A beat spliced in from the other leg makes
  the length disagree;
* **no partial `tkeep` before `tlast`** — a mid-frame short beat is a
  truncation;
* **every MAAP PDU carries `KL_maap`'s own DA** `91:E0:F0:00:FF:00`;
* **`A_TXARB_DIAG` `0x784` is clean** on the two muxes in the path — an *abort*
  is the watchdog injecting a close beat into a stalled frame, i.e. a runt on
  the wire, and a *stall* is the same event one level down.

The lane map is LSB-first `0 ctl_tx, 1 aaf_final, 2 crf_dp, 3 adp_tx`
(the MAC boundary), and bits 7:4 are a documented structural zero — the cascade
collapsed from eight muxes to four when the legacy plane's five control legs
were deleted. Anything decoding `0x784` by the old numbering reads the wrong
mux.

## The AECP answer, and the memory behind it

"This device does not answer AECP" was true of the first substitution build and
is **dead as a premise**. `KL_aecp_engine` pops the dispatch queue's AECP head,
runs `KL_aecp_ucpu` against `KL_aecp_desc_store` and emits a byte-exact AECPDU:

* `0x0004 READ_DESCRIPTOR` is answered for real;
* `0x0029 GET_COUNTERS` is answered for real, the values coming from this
  repository's Table 7-157 mux over `KL_avtp_rx_monitor_ctx`;
* `0x002B GET_AUDIO_MAP` is answered for real on `STREAM_PORT_INPUT`, the
  geometry and records coming from this repository's 7.4.44 answer block over
  the render crossbar's map RAM (the same flops `CHMAP_LOOP` 0x914 reads -
  group L provisions the map through the CSR `0x900` window, reads it back
  through `CHMAP_SNAP`/`CHMAP_LOOP`, then fetches it over the wire: two
  independent readers of one store). A page past `number_of_maps` is
  `BAD_ARGUMENTS` (7.4.44.1), an index past the image is
  `NO_SUCH_DESCRIPTOR` (the store rules existence), and any other
  descriptor type - the recorded `STREAM_PORT_OUTPUT` gap - keeps the
  `NOT_IMPLEMENTED` echo;
* `0x0026 IDENTIFY_NOTIFICATION` *sent as a command* is `BAD_ARGUMENTS` — IEEE
  1722.1 §7.4.39.2's opcode-specific rule beats §9.3.5.3.3's fallback;
* every other opcode gets a conformant `NOT_IMPLEMENTED` **echo**: the command
  back with `message_type + 1`, its own payload copied through and its own
  length declared. Never silence, never a malformed frame;
* a command whose `target_entity_id` is not ours, and any AECP **response**
  arriving as input, are freed **without a reply**.

Every check in group L **decodes the response frame**. A counter that moved
cannot tell a conformant AECPDU from a runt, and this is precisely where the
difference bites: a controller enumerates by `READ_DESCRIPTOR` and gives up at
the first malformed answer.

**The image lives in the integrator's memory, so the harness has to be it.**
The entity model is far too large to spend block RAM on, so `milan_datapath`
grew nine top-level ports (`o_desc_mem_req_valid`, `i_desc_mem_req_ready`,
`o_desc_mem_req_addr`, `o_desc_mem_req_beats`, `i_desc_mem_rsp_valid`,
`o_desc_mem_rsp_ready`, `i_desc_mem_rsp_data`, `i_desc_mem_rsp_last`,
`i_desc_mem_rsp_err`) and the store fetches from `PP_DESC_BASE_P`
(`0x2000_0000`). `sim_main.cpp` builds a real `AEMI` image — header with magic,
layout version and the checksum that must make the eight header words sum to
`0xFFFFFFFF`, a three-entry index map, an `ENTITY` descriptor, **two**
`CONFIGURATION` descriptors and a `STREAM_PORT_INPUT` whose Table 7-23 body
declares the elaborated shape's 2 clusters with `number_of_maps` 0 (the
§7.2.13 dynamic-mapping convention) - and serves it one outstanding burst at
a time.

Two details are deliberate. The image is assembled **in the harness**, not
shelled out to `gen_desc_image.py`: an image produced by the tool the DUT trusts
and then compared against itself proves only that the tool is self-consistent.
And `CONFIGURATION` carries two descriptors so that index 1 can only be answered
correctly if the store applies `elem_off + index × elem_stride` — a store that
ignored the index would return index 0's bytes and fail the compare.

**Leaving `i_desc_mem_req_ready` at 0 is not neutral**, which is why group M
drives it low *on purpose* and says so. It is the store's documented degrade
path: the watchdog abandons the burst and `READ_DESCRIPTOR` comes back well
formed but empty-handed. `milan_dp` backs no memory on any leg and therefore
lives permanently on that path — its `[AECP]` check records exactly that, and
the status there is `BAD_ARGUMENTS` rather than `NO_SUCH_DESCRIPTOR` because an
unvalidated image reports `configurations_count = 0` and the µprogram
range-checks the configuration index before it ever locates.

Milan 5.4.2.1 `ACQUIRE_ENTITY` is graded on the wire. The suite requires a
`NOT_SUPPORTED` response, never `SUCCESS`, with the IEEE 1722.1 7.4.1 body and
an all-zero `owner_id`. The generic `NOT_IMPLEMENTED` echo fails this check.

## The blanket PINMISSING waivers came out (2026-08-13)

`waivers.vlt` used to carry `lint_off -rule PINMISSING -file "*/hdl/*"` and
`lint_off -rule PINMISSING -file "*/protocol-processor/hdl/*"`. Both are
**deleted**, and so are the eleven per-file `PINMISSING` entries that sat
alongside them. A missing pin is an undriven input dressed as style debt, and a
blanket waiver for it is exactly what lets a port added upstream arrive
unnoticed — which is how a nine-port descriptor-memory hole could have built
clean while the suite exited 0.

Removing them surfaced 22 findings, all of one kind: `interface axi_stream_if`
declares an `(input bit clk, input bit rst_n)` pair that nothing in the
interface body ever references, so all 28 instantiations in `hdl/` leave it
unconnected. Four files in this build contain such an instantiation —
`milan_datapath.sv` (8), `ptp_ts_top.sv` (9),
`traffic_controller_802_1q.sv` (2) and `traffic_classifier.sv` (1).

What replaces the blanket is **eight waivers scoped to the file *and* the
message**:

```
lint_off -rule PINMISSING -file "*milan_datapath.sv" -match "*missing pin: 'clk'*"
lint_off -rule PINMISSING -file "*milan_datapath.sv" -match "*missing pin: 'rst_n'*"
…and the same pair for the other three files
```

`-match` is the point, not decoration. A bare `-file "*milan_datapath.sv"`
would also silence a real missing pin in the one file most likely to grow one:
that file instantiates `KL_pp_shadow`, and the nine `desc_mem_*` ports arrived
on that instantiation this round. Pinning each waiver to the two port *names* of
the vestigial interface pair means a missing `desc_mem_req_ready` — or any other
omitted pin, in any file including these four — still stops the build.
**Verified**: an instantiation omitting `desc_mem_req_ready` raises `PINMISSING`
with this exact waiver file in place. (`-match` must follow a `-file` in
Verilator 5.050; on its own it is a syntax error.)

An unconnected *interface* port that the interface never reads cannot tie a live
input to zero. The real fix — deleting the vestigial pair from
`axi_stream_if.sv` — is a 28-call-site edit in RTL this suite does not own, and
`scripts/lint_rtl.py` is that campaign's gate.

## What is no longer here

**The package-collision preflight is gone.** The Makefile used to refuse to
build while this repository and the protocol-processor both declared
`adp_pkg` / `acmp_pkg`, because under `-Wno-fatal` Verilator rates a duplicate
package as a *warning*, exits 0 and silently keeps the FIRST declaration —
compiling the processor's engines against the consumer's constants with no error
anywhere. That was a real trap and it was fixed at the source (the processor
namespaced its copies to `pp_adp_pkg` / `pp_acmp_pkg` / `KL_pp_acmp_listener`).
It is now **unreachable in the other direction too**:
`hdl/ieee17221/adp/adp_pkg.sv` and `hdl/ieee17221/acmp/acmp_pkg.sv` are
**deleted**, so the consumer side of the collision set is permanently empty and
the guard can never fire again. A guard that cannot fire is not a guard, it is a
line nobody re-reads — so it is deleted rather than left in place looking
vigilant. The `waivers.vlt` entries that named `adp_pkg.sv` went with it.

**`-GPP_PLANE_P=1` is gone** — there is no parameter; the plane is
unconditional.

**`ucode.hex` is no longer missing.** The Makefile generated `ltn_rom.hex` and
not the AECP µcode image, so Verilated `$readmem` printed
`%Warning: ucode.hex:0: $readmem file not found` and **carried on with an
all-zero ROM**: the µCPU ran a microcode image of nothing while the suite exited
0. On a suite that carries no `-Wno-*`, one warning is a failure of its own
posture — and group L cannot mean anything without the real image. There is now
a `ucode.hex` rule alongside `ltn_rom.hex`, and both are `clean` targets.

**`-GPP_SRC_EN_P` / `-DPP_SRC_EN` are gone.** `KL_pp_shadow`'s
`SRC_EN_MASK_P` is deleted and `milan_datapath` drives `cfg_src_en_i` from the
**entity shape** (`{ACMP_SRC_C{1'b1}}` — every declared `STREAM_OUTPUT`
enabled and no other index). Groups H and I need the talker half awake and it is
awake on every build of every shape, so the "no source enabled" arm has nothing
left to select.

**`PP_SRCS` is gone from this Makefile.** `milan_dp`'s `SRCS` now *begins* with
the protocol-processor sources plus `KL_pp_shadow` / `KL_pp_maap_shim`, because
the processor is part of the datapath. Naming those files a second time on one
`verilator` command line is a duplicate module definition, and with warnings
fatal here that is a build failure — so the source list comes wholly from
`$(MAKE) -s -C ../milan_dp print-srcs`.

## Two traps this suite exists to not fall into

**Lane order.** Frames are injected LITTLE-LANE (`tdata[7:0]` = first wire
byte). That is the silicon convention of the RX tap: `KL_maap.sv:154` states it
outright and tests the EtherType at lanes 4/5. The `vlan_frame()` helper in
`milan_dp/sim_main.cpp` packs the **other** way for the TX classifier path —
copying it here would feed the processor byte-swapped frames and every accept
check in group B would read a silent zero.

**Rate.** `protocol_processor_top` eats a 1 byte/clk stream, which at 100 MHz is
100 MB/s against gigabit's 125 MB/s. A serializer fed from the raw tap cannot
keep up with line rate and would corrupt frames by lagging rather than by
dropping them — so the tap is classified first and only control frames reach
the FIFO. Group C is what keeps that filter honest.

## Time compression — and why this suite carries the control-plane coverage

`-GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100` gives 1 ms = 100 clk (the
`tb/pp_top` ratio). The ADP advertise cadence is *seconds* of real time; at
silicon rates group D would need ~10⁹ cycles to see a single attempt. Both
values feed the gateware only, and the C++ side is told the ratio by `-D` so
the two cannot drift into disagreeing about what a millisecond is.

**ONE GRID.** `KL_maap` keeps its *own* millisecond (`CLK_FREQ_HZ_P/1000`
cycles) and its Annex B claim walk is 3 probes × ~500 ms — 1.5·10⁸ cycles at a
real 100 MHz, which no harness can run, so `addr_valid_o` would never assert and
group I would be unreachable. `-GMAAP_CLK_HZ_P=100000` makes one MAAP
millisecond 100 clk, **the same** compressed millisecond the processor uses.
Two planes on two different compressed scales would be a harness measuring its
own arithmetic. `MAAP_CLK_HZ_P` defaults to `MILAN_CLK_FREQ_HZ`, so silicon and
`milan_dp` are untouched.

That default is exactly why the control-plane coverage lives here.
`milan_dp` elaborates KL_maap and the processor's timer service at silicon
rates, so on those legs no source can ever hold a destination address
(measured: still PROBING after 40,000,000 cycles), no ADPDU is ever emitted, and
no Talker Advertise is ever declared. Everything that depends on those —
the `SUCCESS` `PROBE_TX` answer, the DA gate, the ADPDU decode, MSRP/MVRP on the
wire — is graded **here**, on the compressed grid, and `milan_dp` records the
gap in the sections that used to carry it.

## Note on group B's frame (corrected 2026-08-12)

`build_adp_discover()` used to put the message type in wire byte 16 and leave
byte 15 at 0 — but byte 15 is sv/version/**message_type** and byte 16 is
valid_time + `control_data_length[10:8]`, so the frame declared msg_type 0 with
`control_data_length` 512 against a 68-byte payload and the processor's V1
length rule discarded it every time. Group B stayed green throughout, because
`rx_frames_o` counts frames the **wrapper** handed to the processor, not frames
the processor **accepted**. What exposed it was group G: a level that only moves
when the ADP engine actually transmits cannot be satisfied by a frame the ADP
engine never took.

## Note on group I's third probe (2026-08-13)

The allocation is asynchronous to the answer. A `PROBE_TX` against a source in
`GS_NO_DA` **issues** the `ALLOC_DA` and is answered `TALKER_DEST_MAC_FAILED` in
the same walk, because the walker must not park waiting for the allocator
(`KL_pp_maap_shim`'s decision 1 — parking it would make the whole talker half of
ACMP deaf for 1024 cycles per attempt). So the probe that *triggers* the grant
still gets a refusal, and the first `SUCCESS` is the **next** probe. Grading the
triggering probe would have been grading the race.
