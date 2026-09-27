"""Build the findings page from all ten retained cycle analyses."""
from pathlib import Path
import hashlib,json,statistics,datetime
p=Path(__file__).resolve().parent.parent
repo=Path("$LANES/394-387-e1-cycles")
cycles=[json.loads((p/f"cycle{n:02d}"/'analysis.json').read_text()) for n in range(1,11)]
assert all(s['steady_recovered'] and s['proof_dut_alive'] for s in cycles)
for s in cycles:
 assert len(s['large_phc_discontinuities'])==1
 assert s['reset_epochs']==[1]
 assert {v for t,v in s['mac_status']}=={13}
 assert all(s['wire'][r]['pdus']==s['wire'][r]['valid_pdus'] and s['wire'][r]['post_tu1']==0 for r in ['dut','peer'])
 assert len(s['wire']['dut']['mr'])==3 and len(s['wire']['peer']['mr'])==1
 for key,bits in [('dut:counter-9-0',{'0':0,'1':0,'5':2}),('dut:counter-5-1',{'0':1,'1':1}),('dut:counter-36-0',{'0':1,'1':1}),('dut:counter-6-1',{'0':1,'1':1}),('peer:counter-6-2',{'0':1,'1':1})]:
  assert all(s['counter_endpoints'][key]['delta'][k]==v for k,v in bits.items()),(s['name'],key)
f=lambda x:f"{x:.2f}"
def delta(s,role,kind,idx,key):return s['counter_endpoints'][f"{role}:counter-{kind}-{idx}"]['delta'][str(key)]
def mr_sequence(s):
 vals=[v['2'] for t,v in s['counter_transitions']['dut:counter-6-1']]
 return ' > '.join(str(v) for i,v in enumerate(vals) if i==0 or v!=vals[i-1])
rows=[]
for n,s in enumerate(cycles,1):
 off=s['off'];on=s['on'];step=s['large_phc_discontinuities'][-1]['bracket'];media=s['media_locked_at']['dut'];servo=s['servo_locked_at'];relock=max(media,servo,s['gptp_recovered_at'])
 carrier=[(t-off,v) for t,v in s['carrier'] if t>off];down=next((t for t,v in carrier if v==0),None);up=next((t for t,v in carrier if v==1),None)
 tx=s['wire']['dut']['first_after_on']-off;rx=s['wire']['peer']['first_after_on']-off
 elapsed=f"{f(relock-step[1])}-{f(relock-step[0])}"
 rows.append(f"| {n} | {f(s['off_hold_s'])} | {f(down)} / {f(up)} | {f(s['first_gm']-off)} / {f(step[0]-off)}-{f(step[1]-off)} | {f(s['gptp_recovery_s'])} | {f(tx)} / {f(rx)} | {elapsed} | {len(s['wire']['dut']['mr'])-1} / {len(s['wire']['peer']['mr'])-1} | {mr_sequence(s)} |")
maxgap=max(s['max_console_gap_s'] for s in cycles)
minrec=min(s['gptp_recovery_s'] for s in cycles);maxrec=max(s['gptp_recovery_s'] for s in cycles)
minwire=min(s['wire'][r]['first_valid_after_wire_return_s'] for s in cycles for r in ['dut','peer']);maxwire=max(s['wire'][r]['first_valid_after_wire_return_s'] for s in cycles for r in ['dut','peer'])
media_range=[max(s['media_locked_at']['dut'],s['servo_locked_at'],s['gptp_recovered_at'])-s['large_phc_discontinuities'][-1]['bracket'][0] for s in cycles]
text="""<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Ten e1 switch power cycles

Measured on 2026-09-27, under the [bench assignment](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5858215210).

| Acceptance | Verdict | Evidence |
|---|---|---|
| #394 acceptance 2, e1 only | FAIL | Recovery succeeded, but LINK_UP and LINK_DOWN never advanced. DUT link-edge timestamps therefore remain unavailable. |
| #387 acceptance 4, assigned CRF measurement | PASS | Ten PHC steps were bracketed. Each recovered gPTP and locked media automatically, within one further stream restart. Raw observations are retained. |

This evidence leaves #394 open.

It does not close #75 or grade #593.

## Contents

- **[Identity and setup](#identity-and-setup)** -- Identify the image, port, streams and starting state.
- **[Method and limits](#method-and-limits)** -- Define capture boundaries, timing uncertainty and observable quantities.
- **[Per-cycle results](#per-cycle-results)** -- Record each outage, recovery and media transition.
- **[Counter and restart findings](#counter-and-restart-findings)** -- Separate the failed link counters from measured media behavior.
- **[Restore and validation](#restore-and-validation)** -- Record the restored bench and local gates.
- **[Artifact hashes](#artifact-hashes)** -- Locate retained raw evidence through its hashes and sizes.

## Identity and setup

The assigned image derives from `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.

The lane base is `2a2a7bb655e528edc3087c88033cd3a47546feb4`.

Only documentation and evidence differ between those commits.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| ROM CRC32, 52,216 bytes | `9b6576a9` |
| QSPI payload CRC32, 3,825,788 bytes | `3c18c276` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Bitstream SHA-256, 3,825,992 bytes | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| AEM SHA-256 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| CSR map SHA-256, 9033 bytes | `92981a367616f79dc5d5382257afdb0aeff211845f86ea3b322102292c562e35` |
| Live ENTITY and CONFIGURATION | Exact matches to the assigned AEM descriptors |
| e1 constraints | RX clock K18, MDIO L16; match the [platform](../../sw/litex/platforms/alinx_ax7101.py) |

Readback proves CRC consistency, not configuration SHA-256.

The existing [identity method](117_GPTP_SILICON_EVIDENCE.md#candidate-image-and-identity-proof) was repeated.

All seven outlets initially read ON.

All eighteen queried stream states were unbound.

The DUT initially selected INTERNAL, source 0.

The reference peer retained INTERNAL and its original sampling rate.

| Direction | Binding | Format |
|---|---|---|
| DUT to reference peer | Output 1 to input 8 | CRF, `041060010000bb80` |
| Reference peer to DUT | Output 2 to input 1 | Same CRF format |

DUT source 1 selected the bound CRF input.

Both listeners reported MEDIA_LOCKED before the first outage.

The DUT reported `SYNC=1`, `ASCAPABLE=1`, `TU=0`.

Its media servo reported LOCKED.

The 12-second baseline captured 6,000 PDUs in each direction.

All carried `tu=0`.

AAF render timing was not measured by this CRF run.

## Method and limits

Only OUT4, the bench AVB switch, was cycled.

Cycle 1 repeated the earlier [OUT4 proof](117_GPTP_SILICON_EVIDENCE.md#out4-is-the-switch).

Switch messages stopped, and the controller port lost carrier.

DUT console replies continued; its reset epoch remained 1.

The reference peer's advertisement index continued increasing.

Its grandmaster-change counter also continued, without resetting.

Every other outlet remained ON.

No later cycle started before this proof passed.

Every action held the bench lock for its own duration.

All commands and captures ran in bounded foreground processes.

The DUT was never rebooted, flashed or power-cycled.

No controller re-bind occurred during any cycle.

The console sampled every 250 ms.

Each cycle retained these independent observations:

- DUT console health, PHC time, reset epoch and MAC status.
- `CLKV_STAT`, `CLKV_TUCNT`, `A_MCSRV_STAT` and CRF emission words.
- Controller GET_COUNTERS and retained ACMP bindings, approximately every second.
- Inline capture on the DUT link, including both CRF directions.
- Controller-port capture, carrier edges, and timed outlet commands.

Counter snapshots cover AVB_INTERFACE, STREAM_INPUT, STREAM_OUTPUT and CLOCK_DOMAIN.

The [register map](../reference/REGISTER_MAP.md) defines the sampled fields.

Captures use the earlier tap envelope and timestamp decoder.

Within-capture intervals use unwrapped hardware timestamps.

Cross-host comparisons use three clock probes before and after.

The quickest round trip supplies each clock-offset estimate.

Those estimates and their half-round-trip bounds remain in every analysis.

Console resolution is 250 ms; controller observations are coarser.

Table decimals identify estimates, not matching absolute accuracy.

The console and controller record request-observation times.

Clock-probe half-round-trip bounds were approximately 0.15 s and 0.07 s.

The tap anchor spread was approximately plus or minus 0.05 s.

USB acquisition latency was not independently calibrated.

PHC steps are inferred from discontinuous UART PHC readings.

Each recorded bracket spans the final pre-step and first post-step reads.

No hardware step strobe or exact step counter was available.

The large observed steps cannot be explained by UART sampling jitter.

Valid CRF PDUs match the bound stream and advertised format.

The checks include subtype, version, length, frequency and timestamp interval.

They also require the expected VLAN and priority.

Every resumed PDU carried `tu=0`.

The recovery clock starts at the first returning Announce or Sync.

It ends when asCapable, sync and `tu=0` coexist.

The [documented bound](../design/GM_LOSS_RECOVERY.md#recovery-bound) is five seconds.

That contract permits one further stream restart for media recovery.

The [step policy](../design/TIME_SYNC.md#step-policy) supplies the media context.

DUT MAC_STATUS stayed `0x0d` throughout each outage.

Thus no DUT link-down or link-up timestamp was observable.

Controller carrier edges describe another switch port, not DUT edges.

Cycle 1 carrier loss was delayed by blocking controller queries.

Later cycles used a separate 100 ms carrier sampler.

Both carrier methods and their raw records are retained.

The first returning tapped frame supplies a separate wire landmark.

The requested one-second restart comparison uses that observable landmark.

It cannot replace an exact physical link-up measurement.

Issue [#75](https://github.com/kebag-logic/milan-fpga/issues/75) separately starts timing at CONNECT_RX success.

These automatic returns issued no CONNECT_RX from the controller.

They do not satisfy that issue's hundred-reconnect experiment.

## Per-cycle results

All table times are seconds.

Carrier edges, GM return, PHC step brackets and first PDUs are relative to OFF.

Recovery is measured from the first returning GM message.

Step-to-media uses the measured step bracket.

Its endpoint requires DUT MEDIA_LOCKED, `tu=0` and servo LOCKED.

The raw analysis separately records each contributing observation.

It also retains every GM, health and servo-state transition.

The range brackets step timing; polling adds observation latency.

The final two columns report observations without applying #593.

| Cycle | OFF duration | Controller down / up | GM return / PHC step | gPTP recovery | First DUT / peer PDU | Step to media | DUT / peer mr changes | DUT MEDIA_RESET sequence |
|---|---|---|---|---|---|---|---|---|---|
"""+'\n'.join(rows)+'\n\n'
text+=f"All ten gPTP recoveries passed: {f(minrec)} to {f(maxrec)} seconds.\n\n"
text+=f"The longest observed step-to-media endpoint was {f(max(media_range))} seconds.\n\n"
text+="Every cycle regained both streams and retained both bindings.\n\nEach talker counted one further STREAM_START and one STREAM_STOP.\n\nNo cycle approached the 180-second stop deadline.\n\n"
text+=f"The largest console sampling gap was {maxgap:.3f} seconds.\n\n"
text+="DUT reset epoch remained 1 in every sample.\n\n"
text+=f"First valid PDUs followed wire return by {f(minwire)}-{f(maxwire)} seconds.\n\n"
text+="Those observed restart intervals all exceed one second.\n\nExact DUT link-up-to-PDU delays remain unmeasured.\n\n"
text+="""## Counter and restart findings

The link-counter failure reproduced in all ten cycles.

LINK_UP remained 1; LINK_DOWN remained 0.

Their valid-mask bits were present in every successful response.

This confirms the earlier [flat-counter observation](117_GPTP_SILICON_EVIDENCE.md#return-and-recovery).

The [integration source](../../sw/litex/milan_soc.py) explains the status dependency.

It initializes software-published link status to up.

This run never wrote that status to manufacture edges.

| DUT observation | Per-cycle result |
|---|---|
| AVB_INTERFACE LINK_UP / LINK_DOWN | `+0 / +0`, defect |
| AVB_INTERFACE GPTP_GM_CHANGED | `+2`, selected itself and then the switch |
| CRF STREAM_INPUT MEDIA_LOCKED / MEDIA_UNLOCKED | `+1 / +1` |
| CLOCK_DOMAIN LOCKED / UNLOCKED | `+1 / +1` |
| CRF STREAM_OUTPUT STREAM_START / STREAM_STOP | `+1 / +1` |
| Stream reservation and ACMP binding | Recovered automatically; both bindings retained |

The media servo moved LOCKED, HOLDOVER, ACQUIRE, then LOCKED.

One large PHC discontinuity accompanied each grandmaster return.

The first step was approximately minus 358,781 seconds.

Cycle 2 stepped approximately minus 162.46 seconds.

Cycles 3 to 10 stepped between minus 95.74 and minus 96.47 seconds.

The raw analysis records each measured amount and time bracket.

DUT outgoing `mr` changed at loss and on resumed transmission.

The reference peer's captured `mr` stayed unchanged.

No claim counts unseen toggles during the wire gap.

DUT MEDIA_RESET was observed at 2 after loss.

It returned to 1 after the new STREAM_START.

STREAM_START resets its observation-interval count to zero.

That reset follows the [counter contract](../../hdl/ieee1722/avtp/KL_talker_diag_ctx.sv).

Endpoint subtraction would incorrectly hide those increments.

The table therefore preserves each observed counter sequence.

Polling caught the intermediate zero in five of ten cycles.

The other five do not prove the timing of that reset.

The reference listener also reset counters on reacquisition.

Its raw trajectory records unlock before the reset.

This run reports these restart observations without grading #593.

The #387 verdict covers the assigned CRF recovery measurement.

It does not assert AAF render timing or waveform continuity.

## Restore and validation

All seven outlets were restored ON, matching the starting census.

All eighteen stream states were unbound after both disconnections.

DUT clock source 0, INTERNAL, was restored.

Original configurations, clock sources, rates and descriptors compared equal.

Final UART health was sync 1, asCapable 1 and `tu=0`.

Reset epoch remained 1, and the media servo returned IDLE.

The final 12-second tap capture contained no CRF PDUs.

The bare-metal UART grader passed 10 of 10 checks.

The temporary capture driver was unloaded and its build removed.

Temporary controller files were removed, with no acquisition process remaining.

The bench lock was released and its availability verified.

The required documentation, scope, bare-metal and feature-status gates are recorded in the packet.

No RTL or firmware changed in this lane.

## Artifact hashes

The operator packet contains the scripts, transcripts and analyses.

The packet is identified as `2026-09-23/394-a375`.

Large raw captures remain under `/tmp/a375/cycleNN/`.

Each cycle's `raw-artifacts.json` lists paths, sizes and SHA-256.

`MANIFEST.sha256` covers retained packet files, excluding itself.

Raw retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

The assigned build and CSR map are identified by hashes.

The initial capture preflight failed before any outlet operation.

The tap was attached but lacked a matching capture driver.

A temporary rebuild restored the same capture interface.

No driver source change, permanent installation or wiring change occurred.

The successful baseline then proved both tapped directions.

| Cycle | Raw artifact | Bytes | SHA-256 |
|---|---|---:|---|
"""
for n in range(1,11):
 manifest=json.loads((p/f"cycle{n:02d}"/'raw-artifacts.json').read_text())
 for r in manifest:
  name=Path(r['path']).name
  if name in ['console.jsonl','controller.jsonl','tap.pcap','controller-wire.pcap','events.jsonl']:
   text+=f"| {n} | `{name}` | {r['size']} | `{r['sha256']}` |\n"
(repo/'docs/findings/394_387_E1_SWITCH_CYCLES.md').write_text(text)
print('Findings page built from ten complete analyses.')
