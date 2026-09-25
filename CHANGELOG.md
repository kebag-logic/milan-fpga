# Milan FPGA product changelog

This file records current bare-metal product revisions.

Older campaigns remain available in Git history.

The [archived throughput record](docs/history/v1/findings/PERFORMANCE_GOAL.md) preserves closed campaign measurements.

## Contents

- **[Unreleased - processor pin 990f9652](#unreleased---processor-pin-990f9652)** -- Probing and failure fields move.
- **[Unreleased - one media event per PHC step](#unreleased---one-media-event-per-phc-step)** -- Toggles `mr` once.
- **[Unreleased - licence and LeaveAll scope](#unreleased---licence-and-leaveall-scope)** -- No Listener Ready, no stream.
- **[Unreleased - CRF input counters served](#unreleased---crf-input-counters-served)** -- The CRF input answers GET_COUNTERS.
- **[Unreleased - gPTP egress launch time](#unreleased---gptp-egress-launch-time)** -- The queue leaves t1.
- **[At 0x0002_0060 - two descriptor fields name the device](#at-0x0002_0060---two-descriptor-fields-name-the-device)** -- Image only.
- **[Release 0x0002_0060 - saved-state pending bit widened](#release-0x0002_0060---saved-state-pending-bit-widened)** -- Pending covers more cases.
- **[Release 0x0002_005F - saved-state snapshot ownership](#release-0x0002_005f---saved-state-snapshot-ownership)** -- Durable means in a slot.
- **[Release 0x0002_005E - board timestamp latency](#release-0x0002_005e---board-timestamp-latency)** -- The fabric corrects its stamps.
- **[Release 0x0002_005C - SRP status words](#release-0x0002_005c---srp-status-words)** -- Four bits read their subject.
- **[Release 0x0002_005B - SET_SAMPLING_RATE list check](#release-0x0002_005b---set_sampling_rate-list-check)** -- An unlisted rate is refused.
- **[Release 0x0002_005A - GET_TX_STATE Listener code](#release-0x0002_005a---get_tx_state-listener-code)** -- Asking Failed sets the flag.
- **[Release 0x0002_0059 - PPS output](#release-0x0002_0059---pps-output)** -- Six CSR words, one metrology pin.
- **[Release 0x0002_0058 - slip counters readable](#release-0x0002_0058---slip-counters-readable)** -- Two RO words, prefill retired.
- **[Release 0x0002_0057 — live media-clock selection](#release-0x0002_0057--live-media-clock-selection)** -- CRF selection steers the grids.
- **[Release 0x0002_0056 — ownerless gPTP verification form](#release-0x0002_0056--ownerless-gptp-verification-form)** -- Verification only.
- **[Release 0x0002_0055 — fabric gPTP product ownership](#release-0x0002_0055--fabric-gptp-product-ownership)** -- Shipping time owner.
- **[Release 0x0002_0054 — generated names](#release-0x0002_0054--generated-names)** -- Serves generated names and writable overlays.
- **[Release 0x0002_0053 — stream setters](#release-0x0002_0053--stream-setters)** -- Adds supported stream setters.

## Unreleased - processor pin 990f9652

- The processor pin moves from `09f9bf38` to `990f9652` (#508).
- Processor issues 92 and 93: saved bindings survive the walk.
- The walk now has a deadline: 20 ms by default.
- The ACMP listener waits from reset for the walk.
- So `PP_CTRL[1]` must start the walk on every boot.
- The firmware's `nvm_boot()` already does; the harnesses now do too.
- Processor issue 94: a descriptor-memory guard holds a late burst.
- No port changes; the guard's debt output stays internal.
- Processor issues 43 and 49: GET_STREAM_INFO reads processor state.
- Input probing and ACMP status come from the listener record.
- Input failure code and bridge id come from SRP.
- Input selectors 5 and 7 never reach the datapath.
- Its bound/settled approximation and zero bridge id are gone.
- It leaves the input failure-code byte of selector 4 zero.
- Every change of those fields pushes GET_STREAM_INFO once.
- Processor issue 112: a re-declaration drops the grant until evaluated.
- `LWSRP_STATUS[9]` and `LWSRP_SLOPE` follow; no gate reads them.
- A round that meets a pending declaration now publishes nothing.
- Processor issue 116: parent-gate comments and mutation deadlines corrected.
- No behavior or external port changes; parent ratchets stay unchanged.
- Processor issue 113: latency-only input changes now push GET_STREAM_INFO.
- Unchanged refreshes stay silent; simultaneous field changes coalesce.
- Its ROM digests are re-recorded; the images are unchanged.
- `tb/verilator/milan_dp` `obj_notify` grades the seam in `[GSI]`.
- `make gsi-mutants` holds its eight failing arms.
- VERSION is unchanged; the release step owns the bump.

## Unreleased - one media event per PHC step

- Issue #387 decided a PHC step's media reaction.
- Every step now toggles `mr` once, on every running stream.
- That holds whatever the media clock source.
- Each talker's MEDIA_RESET counts the toggle it sends.
- The render stage re-centres once, on the step.
- A grandmaster identity change no longer re-centres it.
- So a change that steps counts one re-base, not two.
- Software settime and plane-off adjtime are steps too.
- A step on a pending `mr` restart merges with it.
- A restart stays pending until its level is sent.
- Exactly one toggle follows; nothing is cancelled.
- Before, a second request flipped the target back.
- Neither restart then reached the wire.
- The restart target is therefore per stream.
- The `milan_dp` gmstep leg joins the default sweep: 48/48.
- Three negative controls run with it.
- `make gmstep-mutants` plants all eleven.
- Two of them grade the option-off leg's settime and INTERNAL-source `mr`.
- `tkdiag` T17 grades the merge; T18 grades its end.
- Four mutants must fail them.
- No CSR moves.

## Unreleased - licence and LeaveAll scope

- Silicon streamed the CRF output before any Listener Ready (#530).
- Every talker gate read the processor's raw admission verdict.
- The Talker Advertise declaration alone raises that verdict.
- The gates require ACTIVE and the real per-source grant (#551).
- ACTIVE needs a Listener Ready or Ready Failed as well.
- That covers the CRF licence and every AAF talker gate.
- `CRFT_CTRL[6]` and `LWSRP_STATUS[8]` follow.
- So do the `0x82C` talker lobs above index 0.
- `LWSRP_STATUS[9]` remains the OR of real admission grants.
- `LWSRP_SLOPE` remains their diagnostic sum; no shaper consumes it.
- ACTIVE can lead admission by up to three rounds.
- That needs a Listener Ready decoded within those rounds.
- Each declaration clears its registered Listener first.
- A refused stream can keep ACTIVE until optimism expires.
- With the same TSpec preloaded, its licence stays closed.
- No `STREAM_START`/`STREAM_STOP` pair, interval-counter reset or PDU follows.
- Residual: the refused TSpec differs from that source's previous one.
- The first-round grant still uses the previous slope.
- With early Listener Ready, about one round's licence remains.
- Counter pairs, interval resets and a possible PDU remain exposed.
- [Processor #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) owns the pending fix.
- That fix must be pinned before #551 can close.
- `LWSRP_STATUS[6]` remains raw ACTIVE ORed over all sources.
- The default licence simulation covers re-declarations with identical TSpecs.
- Its unwarmed refused-TSpec arm is opt-in and EXPECTED-FAIL (#112).
- Grant-removal mutants must fail its refused-source checks.
- Warm-pipeline added latency: 0--2 admission cycles on two sources.
- A changed-TSpec admission took 4 cycles (R296-1, CRF phase 0).
- This remains within three rounds on the measured two-source shape.
- Ordinary Listener Ready arrivals add no cycles.
- A bound CRF talker also ended its own bursts.
- The processor pin moves to `09f9bf38` (processor issue 106).
- Its LeaveAll now flags every MSRP attribute type.
- It applies a received LeaveAll per attribute type.
- Its ROM digests are re-recorded; the images are unchanged.
- FRAMES_TX read 16: Table 5.4 counts intervals, not PDUs.
- `CRFT_COUNT` is the PDU total; its row now says so.
- VERSION is unchanged; the release step owns the bump.
- No descriptor changes.
- `tb/verilator/milan_dp` `obj_crflic` proves it at compressed time.
- `make crflic-mutants` holds its failing arms.

## Unreleased - CRF input counters served

- The CRF Media Clock Input's counters mask was empty.
- Controllers therefore rated the entity IEEE 1722.1 only (#529).
- `KL_crf_rx` already kept all ten Table 5.16 counters.
- The root now serves them for STREAM_INPUT `N_STREAMS`.
- Each is 32 bits wide, at its Table 7-157 quadlet.
- `counters_valid` is `0xF3F`; the two tv tallies stay unclaimed.
- The AAF inputs keep `0xFFF`.
- An undeclared index still answers NO_SUCH_DESCRIPTOR.
- Its dirty pulse now reaches the Table 5.22 arbiter.
- That row pushes at most once a second.
- Generic synthesis of `milan_datapath` grows by 1,134 cells (0.07%).
- VERSION is unchanged; the release step owns the bump.
- `tb/verilator/milan_dp` proves it in `[CTRS-CRF]` and `[NOTIFY-CRF]`.

## Unreleased - gPTP egress launch time

- The egress timestamp was the first accepted MAC-boundary beat.
- Two crossings and a store-and-forward buffer follow that beat.
- That queue entered t1 and biased the peer delay (#360).
- t1 is now the frame's launch.
- It is observed one register stage before the pads.
- `KL_gptp_gmii_launch` reports one ordered record per frame.
- `KL_gptp_txticket` allocates one entry per admitted frame.
- `KL_gptp_txret` owns the ledger and the correction.
- It also owns the fence and the recovery demand.
- Identity is position; generation and tags cross-check it.
- The correction is 426 ns of register stages.
- No term of it is a queue allowance.
- An unreconstructable launch is a counted loss.
- `GPTP_DROPE[31:16]` publishes that count.
- The word's low half is unchanged.
- VERSION is unchanged; the release step owns the bump.
- `tb/verilator/gptp_txts` closes the loop over the converted MAC.
- `sw/litex/test_gptp_tx_timestamp.py` proves that conversion behaves.

## At 0x0002_0060 - two descriptor fields name the device

- The model told a controller two untrue things.
- AVB_INTERFACE `port_number` said 0.
- The gPTP plane announces port 1.
- It is in every sourcePortIdentity.
- A controller saw one port under two numbers.
- The descriptor now takes the engine's number.
- `gptp_engine_port_number` parses `OUR_PORTNUM_C` from the generator.
- It derives on every load.
- No second literal is kept.
- The IDENTIFY CONTROL's `reset_time` said 3.
- 7.2.22 reads that as a 3 ms return.
- Nothing in this entity performs it.
- `SET_CONTROL` writes the volatile IDENTIFY row.
- No timer reads that row back.
- Milan 5.3.12 clears the value on RESET.
- That reset is a power cycle.
- Milan 5.4.2.17 and .18 add no expiry.
- So no clause required the promised reset.
- `reset_time` is now 0: no automatic reset.
- Both fields are descriptor content under 6.2.2.8.
- Every tracked config's `entity_model_id` moves.
- Four are hash-derived and rotate.
- `endstation_arty_current`'s pin steps to `0x001BC50AC1000005`.
- `AEM_LAYOUT_REV` stays 3.
- No descriptor byte layout moved.
- Each `aem_desc.bin` changes in those three fields.
- It changes nowhere else.
- No CSR address, width, access or meaning moves.
- No RTL changes.
- The processor serves the image bytes unchanged.
- The gateware VERSION is unchanged.
- No release step is owed.
- `test_builder.py` gate 37 reads both emitted fields.
- It parses the engine generator itself.
- A planted port number is refused.
- The pre-change `reset_time` is refused.

## Release 0x0002_0060 - saved-state pending bit widened

- 0x005F defined `PP_STAT[11]` `nvm_pend` but could not fully raise it.
- The pinned processor exported only the AECP store's dirty level.
- Two of the bit's three terms read a constant zero.
- The pinned processor now exports the other two.
- `nvm_unflushed_o` is the binding manager's per-sink dirty vector.
- `aecp_nvm_stb_o` and `aecp_nvm_mark_o` are a committed command's mark.
- `KL_pp_shadow` binds both in the one place reserved for them.
- The dirty vector is ORed into the backend's `pend_i`.
- Class 6 is a channel map, class 7 a name.
- Either mark sets a sticky pending source.
- Class 1 is not taken; `aecp_dyn_dirty_o` already publishes it.
- A binding accepted inside the manager's debounce now reads pending.
- So does an uncommitted channel map or user name change.
- No record writer exists for either group.
- Only reset clears that source.
- The durable reading is honest for a controller host.
- Before, those cases could be polled as durable.
- No CSR address, width, access or other field moves.
- Donor scopes D1 and D2 are retired.
- KNOWN LIMITATION: donor scope D3 stays open.
- It is materialization of the non-binding fields, UNRESOLVED 1.
- A map or name change is reported, never made durable.
- `tb/verilator/nvm_cosim` case E3 is now an ordinary passing case.
- It was the suite's one labelled expected failure.
- The suite grades 465 checks at both shapes.
- No labelled failure is left.
- The protocol-processor pin moves to `424c688f` (processor issue 90).
- Both ROM images are byte-identical at the new pin.
- Only the pin column of `syn/yosys/rom_digests.tsv` moves.
- Issue 496 carries this step and the ledgers.

## Release 0x0002_005F - saved-state snapshot ownership

- Every allocated record carries an OPEN bit.
- A mutating grant sets it.
- Only a whole-record WRITE with done clears it.
- The writer copies closed records into a private stage.
- A bounded hold defers mutating requests during that copy.
- The backend attests the copy.
- Only an attested copy reaches flash.
- The acknowledgement quotes the capture identity word.
- A completion after the arm therefore stays owned.
- `nvm_dirty` is now the committable work.
- `PP_STAT[11]` `nvm_pend` carries the rest.
- The durable reading gains that bit 0.
- The backend checks RELOAD and accepts one per reset.
- A boot accepting no load opens no capture.
- A reported flash failure revokes `nvm_backed`.
- So does the manager alarm.
- The generator withdraws `MILAN_NVM_IMAGE_BASE`.
- It publishes a live base and a stage base.
- An older writer no longer compiles against this gateware.
- `tb/verilator/nvm_cosim` grades 469 checks at both shapes.
- One named check kills each of its 39 mutants.
- A 2-bit capture identity must alias.
- The shipping 16 bits must not.
- A capture identity that wraps to 0 is ordinary.
- The writer acknowledges it like any other.
- That arm runs at 2 identity bits, the contract's minimum.
- A width outside 2..16 is refused at elaboration.
- Issue 484 carries the contract and the evidence.

## Release 0x0002_005E - board timestamp latency

- The fabric gPTP plane applies two per-board latency corrections.
- Ingress is subtracted from every arrival stamp.
- Egress is added to every reconstructed launch.
- An inline tap measured 875 ns of total stamp error.
- The published peer delay sat above the 800 ns bound.
- A conformant bridge withholds Announce and Sync above it.
- The two values are declared in the board configuration.
- `gptp.ingress_latency_ns` and `gptp.egress_latency_ns`, both required.
- The builder refuses a board that omits either.
- A generated default would hide an unmeasured board.
- The Arty configurations declare zero and say so.
- `GPTP_LAT` `0x7F0` publishes the applied pair, read-only.
- `PTP_INGRESS_LAT` and `PTP_EGRESS_LAT` stay inert scratch.
- A correction two owners apply is applied twice.
- The digital distance inside `milan_datapath` measures zero both ways.
- `tb/verilator/milan_dp` prints and grades that count.
- So the remainder is physical plus the LiteEth chain.
- The split is 3:1 receive to transmit.
- That is 656 ns and 219 ns.
- This PHY's datasheet states no latency figure.
- The split moves the synchronized offset, not the peer delay.
- Issue 488 owns the instrument that would close it.
- 0x005D was never released.
- A parallel lane held it and landed as 0x005F.
- Part of issue 358; the board's ten checks close it.

## Release 0x0002_005C - SRP status words

- `LWSRP_STATUS` `0x694` `[3:0]` describes one subject again.
- That subject is the Listener attribute registered on source 0.
- `[2]` listener registered now counts Asking Failed in.
- It had read bit 1 of that value instead.
- So an asking Listener reported that nobody wanted the stream.
- `[1:0]` and `[3]` had described our own Listener.
- `[3]` listener ready is the Milan 5.3.7.3 pair.
- `ACMPL_STATE` `0x6A4` `[6]` is live for sink 0.
- It compares the registered Talker code against ADVERTISE.
- Bit 1 of that code is FAILED, reading backwards.
- The map had called `[6]` and `[7]` structural zeros.
- Both are real, and the map now says so.
- `tb/verilator/pp_shadow` groups T and U grade all four bits.
- Their registrations are real MSRP frames on the RX port.
- No CSR address, width or access moves.
- Issues 471 and 472 carry the measurements.

## Release 0x0002_005B - SET_SAMPLING_RATE list check

- The protocol-processor pin moves to `ce448dd` (#483).
- SET_SAMPLING_RATE now refuses a rate the AUDIO_UNIT list omits.
- The refusal is BAD_ARGUMENTS carrying the current rate.
- That is Milan v1.2 Section 5.4.2.13.
- The microprogram had checked the lock and stored any rate.
- An unlisted rate was accepted, read back and announced.
- The refusal stores nothing, marks nothing and notifies nothing.
- `tb/verilator/pp_shadow` group R grades both rates end to end.
- No parent consumer reads the rate, so no grid moved.
- Only `VERSION` moves in this repository's RTL.
- No CSR address moves.
- This build also carries the gPTP egress entry above.

## Release 0x0002_005A - GET_TX_STATE Listener code

- The protocol-processor pin moves to `6a9a124` (#473).
- GET_TX_STATE now flags a registered Listener Asking Failed.
- REGISTERING_FAILED no longer follows a Listener Ready Failed.
- That is Milan v1.2 Section 5.5.4.3.
- The talker had used a private Listener code order.
- It now reads `srp_pkg::srp_decl_e`, the engine's own codes.
- GET_STREAM_INFO already read those codes and is unchanged.
- `tb/verilator/pp_shadow` group T grades all four Listener cases.
- Only `VERSION` moves in this repository's RTL.
- No CSR address moves.
- This build also carries the gPTP egress entry above.

## Release 0x0002_0059 - PPS output

- The PHC can drive a pulse-per-second pin (#260).
- Six words land at `0x548`-`0x55C`.
- `PTP_PPS_CTRL` holds the enable, the arm strobe and a built bit.
- `PTP_PPS_TGT_{LO,HI}` carries the second boundary to arm.
- `PTP_PPS_RD_{LO,HI}` reads the live target back.
- It advances by exactly `1e9` per pulse, so drift is measurable.
- `PTP_PPS_WIDTH` publishes the elaborated width in PHC cycles.
- `PPS_CTRL[16]` reads 0 when the comparator was never built.
- Arm and enable can go in one word.
- That write emits no pulse before the boundary.
- The comparator is gated on having been armed.
- The output is off by default and needs `--pps` to exist.
- On the AX7101 it is J11 pin 35, ball `C17`.
- No existing CSR address moves.

## Release 0x0002_0058 - slip counters readable

- `SLIP_LB` (`0x8D4`) and `SLIP_TDM` (`0x8D8`) expose the media-boundary slip counters (#390).
- `SLIP_LB` counts the loopback ring; `SLIP_TDM` counts the TDM junction.
- Each word is live RO, `{skip[31:16], dup[15:0]}`, saturating.
- Read twice and difference for a rate below the ceiling.
- A starved fed pair counts one dup per tick.
- A half at `0xFFFF` is spent until reset.
- `SLIP_LB` is a structural zero without the loopback lane.
- The true-ratio leg feeds the ring at the physical rate.
- At INTERNAL each fed pair dups once per beat period.
- Under CRF the same window shows zero: one grid.
- The `PB_PREFILL_C` bench override is retired.
- Every suite grades the shipped prefill.
- No existing CSR address moves.

## Release 0x0002_0057 — live media-clock selection

- The stored `SET_CLOCK_SOURCE` index reaches the media plane (#74).
- One registered resolve compares it against the generated CRF index.
- A CRF-less shape resolves structurally false through the `16'hFFFF` fold.
- The verdict arms the MMCM servo, the align chain, and `mr`.
- `KL_media_grid_align` holds the packet grid on the physical fsync grid.
- The chain runs CRF, MMCM, fsync, then tick.
- The MMCM status slice belongs to the MMCM alone.
- INTERNAL remains bit-exact free-run with slips accepted and now counted. Since 0x0002_0058 they read at `SLIP_LB`/`SLIP_TDM` (`0x8D4`/`0x8D8`).
- `KL_chan_map_capture` gains TDM junction slip counters.
- The true-ratio leg proves the INTERNAL drift.
- The same leg proves its close under CRF.
- Received toggles and source changes both fire `mr`.
- The 10.4.3 scoping negative holds at INTERNAL.
- The CLOCK_SOURCE shape constants join `adp_shape_defaults.svh`, derived.
- Every shape carries its own CRF index.
- The 8-listener shapes read index 9.
- No CSR addresses move.

The bench probe stays open on issue #74.

## Release 0x0002_0056 — ownerless gPTP verification form

- The fabric gPTP plane remains the sole shipping time owner.
- It owns protocol, servo, and publication state.
- `GPTP_PLANE_EN_P=0` remains buildable only for verification.
- Its GM, parent, PathTrace, and peer-delay publications remain zero.
- Sync and asCapable remain zero.
- `tu` remains one.
- Compatibility writes remain inert.
- Bare-metal UART status exposes the complete timing record.
- The smoke grader validates every published field.
- The bare-metal gate rejects superseded runtime surfaces.
- Mutation controls cover every tracked path class.
- `milan_datapath` no longer instantiates classifier or queue stages.
- It also omits credit shaping and record stamping.
- Their only packet source left under #259.
- Product sources already join the downstream trunk.
- CSR addresses remain stable.
- Retained classifier and shaping registers are scratch.
- Retired capability and diagnostic bits read structural zero.
- The builder drops `--cbs-queues-mask`.
- Standalone suites and Yosys tops retain block coverage.
- Fabric credit shaping remains separately scoped.
- `milan_datapath` shrinks by 180,840 Yosys cells.
- Issue #259 removes 163 files and 57,135 lines.
- Commit `59ba6ffb` preserves them in Git history.
- Removed surfaces include campaign and vendor-build infrastructure.
- They also include superseded audio staging and benches.
- Target-era findings, logs, product pages, tests, and diagrams left.
- The archive lost only material covered by #259.
- The bare-metal scanner guards future reintroduction.
- General archives retain visibly labelled obsolete evidence.
- Issue #259 keeps target-only material solely in Git history.
- Other protocol records remain in the general archive.
- Current authorities replace stale status pages.

Physical closure still requires #70 and #117 evidence.

## Release 0x0002_0055 — fabric gPTP product ownership

- Product configurations select the integrated fabric gPTP engine.
- One atomic bank publishes GM, parent, and PathTrace.
- It also publishes delay, sync, asCapable, and AVTP `tu`.
- Fabric publication writes cannot be forged through CSRs.

## Release 0x0002_0054 — generated names

- `SET_NAME` and `GET_NAME` serve generated AEM names.
- Responses and `READ_DESCRIPTOR` share one writable overlay.

## Release 0x0002_0053 — stream setters

- Stream-format setters apply descriptor-specific validation.
- Supported stream-info setters apply equivalent validation.
- Accepted presentation offsets reach their fabric consumers.
- Accepted stream formats reach their fabric consumers.

Earlier revisions remain in this file's Git history.

The CSR RTL history provides the version source.
