<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# milan_dp — the `milan_datapath` integration suite

`make` builds **twelve elaborations** of `hdl/milan/milan_datapath.sv` (the PS-less
Section A.9 wrapper the LiteX SoC instantiates) and runs a self-checking harness
against each. `make` exits non-zero if any leg fails; **gate on the exit code**,
never on grepping the log — a compile error prints no `FAIL` line at all.

The `sim_nxn` legs regenerate their descriptor image in a unique directory
under `TMPDIR` (falling back to `/tmp`) and remove it after a successful load.
Set `TMPDIR` to a filesystem with enough quota when review lanes run in
parallel. A failed generator deliberately leaves that directory and names its
log in the failure so the artifact can be inspected.

| objdir | harness | shape | what it is for |
|---|---|---|---|
| `obj_dir` | `sim_main.cpp` | `endstation_arty_current`, N=1 | the legacy section list: CSR, TX/RX, PTP, CLKV, CRF, RMON, link guard |
| `obj_nxn` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4 | the 0x800 window → real engines, per-stream routing, TRAP-1 |
| `obj_nxndv` | `sim_nxn.cpp` | arty_4x4 with a GENERATED divergent header (input row 1 declares the 96 kHz base) | the per-row format facts: every tracked config is row-uniform, so only this leg can prove the verdict base and reset GET answer are the ADDRESSED row's and not row 0's -- same channel count on both rows, so the base is the one discriminator. `gen_divergent_shape.py` emits the header and the bench expectations at build time, like `ltn_rom.hex` |
| `obj_nxn8` | `sim_nxn.cpp` | `endstation_ax7101_8x8`, N=8 | the AX 8×8 target + the playback ring + the loopback lane |
| `obj_nxn4c` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4, 4 wire channels | the shipping Arty shape (framer width ≠ shadow reset) |
| `obj_nolpf` | `sim_main.cpp` | `endstation_arty_current`, `LPF_P=0` | the spent area lever: no digital acceptance surface may move |
| `obj_prune` | `sim_prune.cpp` | all six tier-1 blocks pruned | the inert values are STRUCTURAL zeros, not not-armed-yet zeros |
| `obj_txg` | `sim_txgrant.cpp` | `endstation_arty_current` | the CPU DMA-TX lane under control-lane load |
| `obj_ax1x1` | `sim_main.cpp` | `endstation_ax7101_1x1_tdm8` | the shape the AX7101 actually flashes |
| `obj_aclk` | `sim_aclk.cpp` | same, TRUE 391/1591 clk_audio ratio | the media-grid drift RATE |
| `obj_notify` | `sim_nxn.cpp` (`NOTIFY_TIMED_TB`) | `endstation_ax7101_1x1_tdm8`, `PP_TIM_DIV_US_P=1` + `PP_TIM_DIV_MS_P=100` | Milan 5.4.5 TIMED: the GET_COUNTERS one-second limit and the 30-60 s departing-controller monitor, with the processor's timebase compressed so one of its milliseconds is 100 fabric cycles. Exits right after the image is served; every other `sim_nxn` leg runs the same `[NOTIFY]` section untimed |
| `obj_gptp` | `sim_gptp.cpp` | `endstation_ax7101_1x1_tdm8`, fabric gPTP at a compressed 2 MHz | Product-owner publication from selected Announce through the atomic parent bank, live CSR and `GET_AS_PATH`; covers absent versus explicit `[GM]`, tail-only refreshes, coherent in-flight cutover, Table 5.22 pushes, software-store isolation, and the maximum eight-entry wire response |

## Contents

- **[2026-08-13 — the control plane was SUBSTITUTED, and this suite was rewritten around it](#2026-08-13--the-control-plane-was-substituted-and-this-suite-was-rewritten-around-it)** — What the legacy-plane deletion did to this suite: which checks were repointed to the protocol processor's class-D face and the 0x920 window, and which were deleted because their subject no longer exists
- **[The device answers AECP now — and what this suite can and cannot see of it](#the-device-answers-aecp-now--and-what-this-suite-can-and-cannot-see-of-it)** — What the AECP µCPU answers, why every leg here drives the descriptor-memory ports into the documented degrade path deliberately, and the dynamic-output-map capability that the substitution cost
- **[Check counts, before and after](#check-counts-before-and-after)** — Per-leg check totals, with every row that was not re-measured after the last edit marked as such rather than projected
- **[Rules this suite is held to](#rules-this-suite-is-held-to)** — The standing contract: gate on exit codes, never repoint a check to a structural zero without naming it as one, and never leave a check that passes vacuously

## 2026-08-13 — the control plane was SUBSTITUTED, and this suite was rewritten around it

The entire legacy IEEE 1722.1 / SRP control plane is **deleted**:
`hdl/ieee17221/aecp/**`, `hdl/ieee17221/acmp/**`,
`hdl/ieee17221/adp/{adp_advertiser, KL_adp_parser, adp_pkg}.sv` and
`hdl/ieee8021q/srp/**`. `milan_datapath` instantiates `hdl/milan/KL_pp_shadow.sv`
**unconditionally** as THE control plane, `tx_drain_i` is 0, and the processor's
packed TX rides the control lane through `ctl_tx_mux`.

That is not a refactor from a test's point of view. Whole classes of witness
stopped existing, and a harness that kept reading them would have been asserting
against structural zeros — the exact failure mode the zeros are documented to
prevent. **Every deleted check below names its subject and why it is gone; every
repointed check names its old witness and its new one.** Nothing was neutered to
make a run pass.

### What the plane deletion cost this suite, honestly

Three things are structurally unreachable **on these legs**, and the reason is
arithmetic rather than a defect:

1. **The ADP advertisement.** Milan 5.6.3.5.2 makes the first advertisement wait
   `T-ADP-DELAY-START`, a PRNG draw of 0…2000 ms. `milan_dp` passes no
   `-GPP_TIM_DIV_*`, so the processor's millisecond is the silicon one —
   100,000 axis cycles — and the draw is up to 2·10⁸ of them. *Measured: no
   ADPDU in 40,000,000 cycles.*
2. **The talker's destination address, and therefore ACMP `SUCCESS`, the SRP
   Talker Advertise, MSRP/MVRP on the wire and every class-A tag.**
   `acmp_declaring_o` is reachable only through a MAAP `ALLOC_DA` success, and
   `KL_maap` is elaborated here at the silicon rate (`MAAP_CLK_HZ_P` defaults to
   `MILAN_CLK_FREQ_HZ`), so its Annex B claim walk — 3 probes × ~500 ms plus
   announce — is ~1.5·10⁸ cycles away. *Measured: still PROBING after
   40,000,000 cycles.* Waiting would add ~25 minutes **per elaboration** to a
   ten-leg suite.
3. **A MAAP-granted destination address for talkers `t > 0`**, which is the same
   arithmetic as (2) seen from the framer: a source that never reaches
   `acmp_declaring_o` never gets a DMAC. `cfg_aaf_bypass` (AAF_CTRL[1]) is the
   escape hatch these legs use to keep the framers awake without one.

**Where that coverage went:** `tb/verilator/pp_shadow` elaborates the *same*
gateware with both millisecond scales compressed onto one grid
(`-GPP_TIM_DIV_MS_P=100`, `-GMAAP_CLK_HZ_P=100000`) and grades the DA gate, the
`SUCCESS` `PROBE_TX` answer with its `stream_id` and `stream_dest_mac`, the
whole 82-octet ADPDU byte-exact against the `0x600` CSR group, and the
MSRP/MVRP frames sharing `ctl_tx_mux` with MAAP. It is not lost coverage; it
moved to the only suite that can run it.

**What stayed here** is everything the data path owns and everything the control
plane can still do at real-time rates: the listener BIND_RX ladder (the
processor answers, launches its own PROBE_TX, and settles — this harness now
plays the talker), the ACMP responder, the stream-table alias (TRAP-1), the SRP
**Domain adoption** surface (`0x788` and the AAF C-TAG really do move together),
AAF/CRF wire truth, the channel-map crossbars, the PCM ring and route policy,
I2S, CBS/queues/classifier, PTP, the TCAM/RX filter, latency taps, the loopback
lane, and the LiteX CSR boundary itself.

### Two RTL findings this suite used to report — both now CLOSED in `hdl/`

**`aecp_in0_fmt` was tied to `64'd0`.** That net is `fmt0_i` for
`KL_avtp_rx_monitor_ctx` — **the expected format for `STREAM_INPUT[0]`** — and
the monitor's first acceptance term is `subtype == fmt[63:56]`, so against a
zero format a *perfectly conformant* AAF PDU on the bound `stream_id` was
counted `UNSUPPORTED_FORMAT` and never reached the depacketizer or the PCM ring.
Stream 0 accepted nothing. `milan_datapath.sv` now folds the setting over the
declaration: `aecp_in0_fmt` reads the processor's published SET_STREAM_FORMAT
row 0 when a controller has set one and the generated `ADP_STRIN0_FMT_C`
otherwise, exactly as `aecp_pres_offset` folds set offsets over `PRES_DFLT_C`
rather than a zero. The declaration is the default; the setter owns the rest
(issue #67).

`sim_main.cpp` grades the acceptance path again end to end and byte-exact:
untagged and C-tagged conformant PDUs reach the PCM ring with their 48 payload
octets intact, `MEDIA_LOCKED` asserts, an unbound `stream_id` does not move
`FRAMES_RX`, and the TCAM prefilter section proves both halves of its property
again (the kernel DMA goes silent **while** the fabric ring keeps consuming).
The gate is shown to be *discriminating* and not merely open by the wrong-rate
PDU two sections later: `nsr 0x07` still counts `UNSUPPORTED_FORMAT` and
delivers no ring traffic.

**The CRF clock-source compare had no driver.** `aem_crf_clksrc_w` lost its
only writer with the old AECP response builder, while `KL_mmcm_drp_servo` and
`mcr_restart_p_w` still compared it against `aecp_clk_src`; `0 == 0` read TRUE,
so the fabric behaved as if the CRF media clock were selected. Both nets are
**deleted**. The current processor selection reaches an unconsumed root wire,
while `milan_datapath` declares
`CRF_CLK_SELECTED_C = 1'b0`, `MEDIA_CLK_SRC_IDX_C = 16'd0` (INTERNAL) and
`MEDIA_CLK_SRC_NONE_C = 16'hFFFF`, and the consumers read those constants.
`sim_main.cpp` and `sim_nxn.cpp` assert the consequence rather than the
plumbing: `mnco_servo_en_w` is 0 and `MCSRV_STAT[2:0]` is IDLE. On the broken
build `MCSRV_STAT` read `0x21`.

## The device answers AECP now — and what this suite can and cannot see of it

"No AECP" is dead as a premise. The protocol processor carries an AECP µCPU
(`KL_aecp_ucpu` + `KL_aecp_desc_store` + `KL_aecp_engine`, driven from
`ucode.hex`) and handles 30 AEM opcodes plus Milan `GET_MILAN_INFO`. The served
set includes descriptor reads, lock and configuration operations, read-side
stream and clock commands, sampling-rate and clock-source setters, the stream
setters (`SET_STREAM_FORMAT` both directions and `SET_STREAM_INFO`'s
MSRP_ACC_LAT_VALID sub-command, with this fabric answering the format verdict
and consuming the published settings - the `#67` block in `sim_nxn.cpp` grades
the whole loop), Identify,
registration, counters, AVB information, AS path, and both audio-map
directions. `IDENTIFY_NOTIFICATION` sent as a command returns `BAD_ARGUMENTS`
(IEEE Section 7.4.39.2 beats Section 9.3.5.3.3). Commands outside the implemented inventory
receive a conformant `NOT_IMPLEMENTED` echo with the command payload and length
preserved and the frame padded to the 60-octet minimum. The exact inventory is
gated by [`aecp_engine_steps.py`](../../../tests/steps/aecp_engine_steps.py) and
the pinned processor's
[`06_aecp_engine.md`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/44489453cf362c7a41c9e020f4896f967dc2a4d1/docs/architecture/06_aecp_engine.md).

**This suite backs no descriptor memory, on purpose and on record.**
`milan_datapath` exposes nine ports for the AEM image the store fetches
(`o_desc_mem_req_valid` … `i_desc_mem_rsp_err`). Every leg here drives
`i_desc_mem_req_ready` **low explicitly**, in the reset section, next to a
comment that says what that means: it is `KL_aecp_desc_store`'s documented
degrade path — the watchdog abandons the burst, the image never validates, and
`READ_DESCRIPTOR` comes back well formed but empty-handed. A zero left at a port
by accident and a zero driven by a decision look identical on a waveform, so it
is stated. The `[AECP]` checks in `sim_nxn.cpp` grade that path: an answer
arrives, it is an `AEM_RESPONSE`, its status is `BAD_ARGUMENTS` (an unvalidated
image reports `configurations_count = 0`, and the µprogram range-checks the
configuration index *before* it locates, so this is not
`NO_SUCH_DESCRIPTOR`), it carries the Section 7.4.5 stub at `cdl = 20`, and it is
padded to 60.

**The SERVED path lives in `tb/verilator/pp_shadow`**, which backs those ports
with a real `AEMI` image and grades `SUCCESS` with the descriptor bytes compared
octet for octet, the locate miss, the bad configuration index, the
`NOT_IMPLEMENTED` echo, the two silent-refusal cases, and the no-memory degrade
with recovery.

**`[NOTIFY]` is Milan 5.4.5 on the wire (issue #69).** These historical
software-staged notification legs elaborate with `GPTP_PLANE_EN_P=0`. Two controllers
register (a second `{source MAC, controller_entity_id}` identity, `CTL_B`,
beside the one every other call uses), and the section grades what reaches
the TX trunk with the unsolicited bit: a `SET_NAME` from A produces exactly
one push, to B, with B's sequence_id starting at 0 and the new name in the
body (the 5.4.5.2 exclusion gate: a push to the requester FAILS); the same
`SET_NAME` again pushes nothing (the no-op gate); B's change reaches A alone
with A's own sequence at 0, and the next change from A reaches B at sequence
1; the last push is byte-identical from the body on to the solicited
`GET_NAME` that follows (the content bar). A grandmaster CHANGE pushes
`GET_AVB_INFO` and `GET_AS_PATH` to both, each equal to the solicited read
after it. The PathTrace sequence proves the publication boundary rather than
only the happy-path push: it publishes an initial `{GM, slot 1}`, privately
re-COMMITs slot 1, and proves both zero push and a solicited read of the prior
publication before PUBLISH. A changed `PUBLISH` through `0x7DC`/`0x7E4`
atomically exposes the complete staged tail and count and pushes the new
`GET_AS_PATH` bytes with no `GET_AVB_INFO`; an identical re-PUBLISH advances
neither generation nor wire. Under this option-off contract, legacy count 0
and explicit count 1 are exercised in both directions and spend neither
generation nor a push. The harness then
holds TX, stops on the live first-count snapshot edge, changes the count and
multiple slots, and proves PUBLISH completes before the first entry request;
the in-flight wire body stays all-old and the next one is all-new. A separate
GM=0 arm changes and withdraws a real two-entry
publication while the served response stays empty, proving both false pushes
are suppressed. The CSR unit arm also proves a combined COMMIT+PUBLISH uses the
newly committed slot on that same edge. The FIRST grandmaster commit (zero to something) pushes both rows
while the ADP
GM_CHANGE duty stays untouched. The two arms that answer the Table 5.22
fields the root used to hold silent run next: the gPTP domain number is
changed at `0x62C` with the grandmaster set back to ZERO -- the reset and
GM-loss boundary where the ADP GM_CHANGE strobe is deliberately suppressed --
and must still push one `GET_AVB_INFO` to each controller, with no counter
push and no `GET_AS_PATH` behind it, the same value written again pushing
nothing, and the same change repeated with a grandmaster present; then
`GPTP_PDELAY` at `0x6E4` is walked 0 to 1 to `0xFFFFFFFF` to 0, each real
move pushing once per controller and reading back in the solicited
`propagation_delay` field, and the repeat of `0xFFFFFFFF` pushing zero times.
`await_aecp` demultiplexes on the u bit and
the originated-command message type, so a waiter for a solicited response
never mistakes a push for its echo; the pushes land in `uns_log` with their
cycle stamps. The timed leg (`obj_notify`) adds the counters row: a
`GET_COUNTERS(AVB_INTERFACE, 0)` push on the GPTP_GM_CHANGED move, equal to
the solicited read after it, a second move inside the same second WITHHELD
and then RELEASED at the limiter's full second (measured on the wire, 990 ms
floor for the selection-to-wire jitter), and the 5.4.5.3 monitor: the entity
originates `CONTROLLER_AVAILABLE` to the silent controller 30 to 60 s after
its last command, retries exactly once 250 ms later, removes it with a
`DEREGISTER_UNSOLICITED_NOTIFICATION` to that controller alone within a
second of the retry, never probes the controller that keeps talking, and
accepts the removed one back with its sequence restarted at 0. The
`[CTRS]`/`[CTRS-OUT]`/`[CTRS2]` sections also watch the descriptor arbiter's
scalar face (`pp_ctr_evt_*`): simultaneous per-output pulses must ALL be
delivered, which a clear-all picker or a non-accumulating pending set fails.

`sim_nxn.cpp`'s `[T66]` covers the other side of the same coin.
`GET_AUDIO_MAP` succeeds on both Stream Port directions, and
`ADD_AUDIO_MAPPINGS` plus `REMOVE_AUDIO_MAPPINGS` use the processor's two-pass
transaction face to update the live root stores. The harness proves full-page
ADD and readback, idempotent ADD, all-or-nothing refusal after a late invalid
row, duplicate-safe REMOVE, cross-port output ownership, running-output
refusal, and generated input-port geometry through the live crossbar RAM. It
derives the AX7101 output cluster count from the generated descriptor, accepts
and round-trips every published offset, preserves a clear fabric-source marker
for unbacked clusters, rejects same-key and cross-port replacement, and refuses
the first offset beyond the model.

## Check counts, before and after

"Before" is the state after the compile fix that made the suite build at all
(`sim_nxn.cpp` reached deleted RTL through Verilator XMRs and did not compile,
so *no* leg ran). **Every number below is measured**, all nine legs, on the same
`make` — this table carries no projection.

| leg | before (measured) | after (measured) | note |
|---|---|---|---|
| `obj_dir` (`sim_main`) | 273 checks / 75 fail | **244 / 0** | the `in0_fmt` acceptance path is graded again, byte-exact |
| `obj_nxn` (`sim_nxn`) | 378 / — (did not compile) | **145 / 0** | + the `[AECP]` no-memory degrade checks |
| `obj_nxn8` (`sim_nxn`) | 512 / not available | superseded | `[T66]` now grades atomic audio-map mutation; use the current run summary below |
| `obj_nxn4c` (`sim_nxn`) | 378 / — | **145 / 0** | |
| `obj_nolpf` (`sim_main`) | 273 / 75 | **244 / 0** | identical to `obj_dir`, as the pruned-LPF claim requires |
| `obj_prune` (`sim_prune`) | 31 / 0 | **31 / 0** | unchanged, untouched |
| `obj_txg` (`sim_txgrant`) | 14 / 3 | **15 / 0** | |
| `obj_ax1x1` (`sim_main`) | 273 / 73 | **242 / 0** | 5 sections guarded out on this shape |
| `obj_aclk` (`sim_aclk`) | 5 / 0 | **5 / 0** | unchanged, untouched |

Earlier re-measurement had stopped because the `protocol-processor` submodule
working tree went out from under the build — `protocol_processor_top.sv` had an
uncommitted `KL_aecp_engine` instantiation and a nine-pin `desc_mem_*` port that
the source list did not name, so elaboration failed with `MODMISSING`. That is
resolved: the submodule is at its recorded pin, the Makefile names
`ucpu_pkg.sv`, `KL_aecp_ucpu.sv`, `KL_aecp_desc_store.sv` and
`KL_aecp_engine.sv`, and it generates `ucode.hex` next to `ltn_rom.hex`.

The `sim_nxn` drop is the deleted lwSRP attribute-row and ACMP context-table
windows: eight whole sections whose subject is a table `milan_datapath` now ties
to zero. Each one is replaced in place by a block comment naming the subject,
the tie-off, the measurement behind "unreachable", and where the coverage went.

### Three checks that were failing for reasons worth writing down

* **`pb: t1 frames the SAME ring pair`** read talker 1 as *silent*. It was not:
  the TCTX case ~1300 lines earlier stages talker 1 with `uid 5` in
  `A_SW_DMAC_HI[31:16]`, and `KL_aaf_packetizer`'s documented rule is that a
  software-named `uid` outranks the fabric-derived one. Two now-deleted
  lwSRP/`0x800` cases used to put that field back before task #31 ran, so the
  section inherited `uid 5` while classifying by `uid 1` — the same file
  asserting both. Task #31 now stages its own precondition instead of leaning on
  a neighbour that may be deleted again.
* **`[T67]` cadence read 3072 cycles/PDU instead of 12500.** With
  `aecp_odmap_dyn_w` tied off, `CHMAP_CTRL[0]` is the *whole* selector between
  the `media_tick`-paced crossbar and the `clk_audio/512` zero-fill path, and
  `[T66]` had deliberately left it at 0. Every leg but `obj_aclk` clocks
  `clk_audio` 1:1 with `axis_clk`, so the static path measured 195.3 kHz and
  looked like a 6× cadence defect. `[T66]` now leaves the crossbar armed and
  `[T67]`'s banner states which grid it is on.
* **The `0x002C` boot seed.** There is no seeder any more, so key 0 reads empty.
  The check grades the two halves of the new structural truth — the read mux is
  still live, the RAM is empty, `CHMAP_CTRL[0]` is 0 — and will fail the day a
  seeder returns in any form.

## Rules this suite is held to

* **Gate on exit codes.** A compile error prints no `FAILED` line, so grepping
  the output for "fail" reads as green.
* **A check that asserts a structural zero must say so, and say why.**
  Otherwise it is deleted — a zero that nobody can distinguish from "idle" is
  not evidence.
* **No vacuous passes.** Where a property became unprovable (the 10.4.3 `mr`
  gate, the class-A tag withdrawal) the check is removed and the gap is printed
  as a `[GAP]` line on every run, rather than left passing for the wrong reason.
* **Name the shape.** Every leg puts its config's generated directory *first* on
  the include path. Without it the build falls through to
  `hdl/common/csr/gen/`, which is whichever config last ran `--write-rtl`.
