"""Generate the public measurement page from retained cycle evidence."""
from pathlib import Path
from datetime import datetime,timezone
import collections,hashlib,json,math,re,statistics
p=Path(__file__).resolve().parent.parent
repo=Path('$LANES/75-reconnect-bench')
out=repo/'docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md'
rows={d:[json.loads(f.read_text()) for f in sorted(p.glob(d+'-[0-9][0-9][0-9]/analysis.json'))] for d in ['listener','talker']}
fmt=lambda v:'unavailable' if v is None else f'{v:.6f}'
def median(a):return statistics.median(a) if a else None
def percentile(a):return sorted(a)[math.ceil(.95*len(a))-1] if a else None
def slope(a):
 if len(a)<2:return None
 x=range(1,len(a)+1);mx=statistics.mean(x);my=statistics.mean(a)
 return sum((i-mx)*(v-my) for i,v in zip(x,a))/sum((i-mx)**2 for i in x)
def aggregate(rs,w,s):
 vals=[r['msrp'][w][s] for r in rs]
 if not vals:return dict(seconds=0,pdus=0,rate=None,la=0,ready=0,talker=0)
 sec=sum(v['seconds'] for v in vals);n=sum(v['pdus'] for v in vals)
 return dict(seconds=sec,pdus=n,rate=n/sec if sec else None,la=sum(v['leaveall_vectors'] for v in vals),ready=sum(v['target_ready'] for v in vals),talker=sum(v['target_talker'] for v in vals))
def declared(r,s,t):
 return sum(v for k,v in r['msrp']['whole'][s]['types'][t].items() if k in ['New','JoinIn','JoinMt'])
def pair(r,key):
 return str(r['msrp']['whole']['DUT'][key])+' / '+str(r['msrp']['whole']['bridge'][key])
complete=all(len(a)==100 or len(a)>=10 and all(r['status']=='FAIL' for r in a[-10:]) for a in rows.values())
status='PASS' if complete and all(r['status']=='PASS' for a in rows.values() for r in a) else 'FAIL' if any(r['status']=='FAIL' for a in rows.values() for r in a) else 'PENDING'
lines=['# Reconnect restart measurement','', 'Refs #75. Operator [A386], measured 2026-09-27.','',
'Measured transport: CRF, one direction at a time.',
'AAF restart timing remains unmeasured.','',
'## Contents','',
'- **[Scope and identity](#scope-and-identity)** -- Assignment, image, and simulation boundary.',
'- **[Method](#method)** -- Timing anchors, validity checks, and capture limits.',
'- **[Distribution](#distribution)** -- Restart times and the one-second acceptance.',
'- **[Growth](#growth)** -- Ordered blocks and latency trends.',
'- **[MSRP attribution](#msrp-attribution)** -- Sender counts, rates, and declaration events.',
'- **[Cycle evidence](#cycle-evidence)** -- Every measured restart and captured exchange.',
'- **[Counters and restoration](#counters-and-restoration)** -- Counter authority and restored state.',
'- **[Acceptance](#acceptance)** -- Evidence against each issue criterion.',
'- **[Artifacts](#artifacts)** -- Exact image hashes and full capture index.',
'- **[Validation](#validation)** -- Required gates and reproducible analysis.','',
'## Scope and identity','',
'[The assignment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5859652809)',
'requires 100 cycles per direction.',
'Ten consecutive overruns stop that direction.','',
'This evidence uses the assigned running image.',
'No product source changed.','',
'| Identity item | Recorded value |',
'|---|---|',
'| Image source | `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` |',
'| Evidence base | `8bc97021f28fb7f729418d3a00851c84ea0b50fd` |',
'| VERSION / firmware | `0x0002_0060` / `2.96.0` |',
'| ROM CRC32 | `9b6576a9` over 52,216 bytes |',
'| QSPI payload CRC32 | `3c18c276` over 3,825,788 bytes |',
'| AEM CRC32 | `93742dd2` over 7,352 bytes |',
'| ENTITY / CONFIGURATION | Exact assigned AEM descriptor bytes |',
'| Initial UART grader | PASS, 10/10 |','',
'Local bitstream and AEM SHA-256 match the assignment.',
'UART provides CRC consistency, not configured-fabric SHA-256 readback.','',
'Image-to-base product paths are unchanged.',
'Intervening changes concern documentation, evidence, and test infrastructure.','',
'[Phase-1 PR #321](https://github.com/kebag-logic/milan-fpga/pull/321)',
'pins the replacement SRP engine in simulation.',
'Six peer LeaveAll cycles emit at most 18 PDUs.','',
'Each cycle emits at most four PDUs.',
'Every cycle re-declares Listener Ready.','',
'The retired context module directly queued received-LeaveAll refresh.',
'It is absent from this running architecture.','',
'[Historical source](https://github.com/kebag-logic/milan-fpga/blob/eb375c131ef0e3b3b42ef42f4e546d8d8b20b494/hdl/ieee8021q/srp/KL_lwsrp_ctx.sv)',
'and [design](https://github.com/kebag-logic/milan-fpga/blob/eb375c131ef0e3b3b42ef42f4e546d8d8b20b494/docs/LWSRP_FPGA_ARCHITECTURE.md)',
'were read without restoring retired files.','',
'[Current SRP design](../../protocol-processor/docs/architecture/10_srp_engine.md)',
'defines the replacement and remaining LeaveAll-timer deviation.',
'This measurement neither changes RTL nor resolves that deviation.','',
'## Method','',
'Topology: DUT, inline tap, AVB bridge, reference peer.',
'The controller shares that AVB network.','',
'The same approved tap required its temporary capture driver.',
'Its three build inputs matched the previous operator’s hashes.','',
'| Direction | Talker output | Listener input | Format |',
'|---|---|---|---|',
'| DUT listener | Reference 2 | DUT 1 | `041060010000bb80` |',
'| DUT talker | DUT 1 | Reference 8 | `041060010000bb80` |','',
'These matching CRF streams require no format changes.',
'Both clock selections remain internal.','',
'Each cycle first records approximately three seconds.',
'The controller then sends `DISCONNECT_RX`.','',
'After success, it waits two seconds.',
'It then sends `CONNECT_RX`.','',
'The successful response starts the measured interval.',
'The first valid stream PDU ends it.','',
'Controller identity and sequence identify the response.',
'Stream identity and direction identify the resumed PDU.','',
'CRF validation checks version, stream-valid, type, frequency, and lengths.',
'It also checks interval, VLAN, priority, and settled destination.','',
'Source identity must match the bound stream.',
'The next packet must advance sequence and timestamp.','',
'The tap timestamps both endpoints on one hardware clock.',
'Its nanosecond word is unwrapped using capture-host timestamps.','',
'Host clock offsets do not enter the elapsed interval.',
'Printed precision does not establish absolute timestamp calibration.','',
'Each restart observation has a thirty-second cap.',
'Pre-capture and the mandated disconnect hold precede that observation.','',
'Capture continues three seconds after resumed traffic reaches collection.',
'Every cycle retains its full capture.','',
'Capture-host packet drops invalidate evidence.',
'Parsing errors and missing responses also invalidate evidence.','',
'Per-action foreground timeouts bound commands and capture children.','',
'Each action holds the bench lock until children exit.',
'Analysis runs after that lock is released.','',
'## Distribution','',
'All values are seconds; p95 uses nearest rank.','',
'| Direction | Cycles | Below 1 s | Min | Median | p95 | Max | Result |',
'|---|---|---|---|---|---|---|---|']
for d,a in rows.items():
 vals=[r['latency_s'] for r in a if r.get('latency_s') is not None]
 verdict='FAIL' if any(r['status']=='FAIL' for r in a) else 'PASS' if len(a)==100 else 'PENDING'
 lines.append(f"| DUT {d} | {len(a)} | {sum(r['status']=='PASS' for r in a)} | {fmt(min(vals) if vals else None)} | {fmt(median(vals))} | {fmt(percentile(vals))} | {fmt(max(vals) if vals else None)} | {verdict} |")
lines+=['','Initial binds are excluded from these distributions.',
'Any censored cycle remains a failure, outside numeric quantiles.','']
lines+=['| Initial bind, excluded from cycle count | Response to AVTP, seconds | Below 1 s |','|---|---|---|']
for direction in ['listener','talker']:
 f=p/(direction+'-setup/analysis.json')
 if f.exists():lines.append('| DUT '+direction+' | '+fmt(json.loads(f.read_text()).get('latency_s'))+' | '+('PASS' if json.loads(f.read_text())['latency_s']<1 else 'FAIL')+' |')
lines+=['','The initial DUT-talker binding exceeds one second.',
'Its capture retains the delayed Listener Ready arrival.','',
'Bridge Listener Ready arrives after 6.888605 seconds.',
'Valid CRF follows another 0.000793 seconds later.','',
'DUT Talker Advertise repeats while that Ready is absent.',
'A bridge LeaveAll precedes the eventual Ready.','',
'This locates the observed wait before Ready reaches DUT.',
'Peer-side capture is required for further causal attribution.','',
'## Growth','',
'Ordered blocks expose changes hidden by pooled quantiles.',
'Regression uses cycle number against latency in seconds.','',
'| Direction | First ten median | Last ten median | Slope, seconds/cycle |',
'|---|---|---|---|']
for d,a in rows.items():
 v=[r['latency_s'] for r in a if r.get('latency_s') is not None]
 lines.append(f'| DUT {d} | {fmt(median(v[:10]))} | {fmt(median(v[-10:]))} | {fmt(slope(v))} |')
lines+=['','| Direction | Cycles | Median, seconds | Maximum, seconds | Combined MSRP PDUs/s |',
'|---|---|---|---|---|']
for d,a in rows.items():
 for start in range(0,len(a),10):
  v=[r['latency_s'] for r in a[start:start+10] if r.get('latency_s') is not None]
  rate=sum(aggregate(a[start:start+10],'whole',sender)['rate'] for sender in ['DUT','bridge'])
  lines.append(f'| DUT {d} | {start+1}-{min(start+10,len(a))} | {fmt(median(v))} | {fmt(max(v) if v else None)} | {fmt(rate)} |')
lines+=['','Growth interpretation awaits the complete ordered series.','',
'## MSRP attribution','',
'Every captured MSRP vector is decoded and attributed.',
'Counts include all types and all packed attribute events.','',
'Only two MSRP transmitters appear on the tapped segment.',
'Their source addresses distinguish DUT and adjacent bridge.','',
'Peer-origin stream attributes arrive as bridge declarations.',
'The peer’s original link-local MSRP exchange is not tapped.','',
'LeaveAll counts represent type-scoped vectors, not PDUs.',
'Ready counts include New, JoinIn, and JoinMt declarations.','',
'The packet preserves individual events in each `msrp.tsv`.',
'Raw captures preserve original first values and full payloads.','',
'Before spans capture start through successful disconnect.',
'After spans successful reconnect through capture end.','',
'Resumed spans first valid CRF through capture end.',
'Rates divide packet totals by summed window durations.','',
'| Direction | Sender | Before PDUs/s | After PDUs/s | Resumed PDUs/s | Whole PDUs | LeaveAll vectors |',
'|---|---|---|---|---|---|---|']
for d,a in rows.items():
 for s in ['DUT','bridge']:
  whole=aggregate(a,'whole',s)
  lines.append(f"| DUT {d} | {s} | {fmt(aggregate(a,'before',s)['rate'])} | {fmt(aggregate(a,'after',s)['rate'])} | {fmt(aggregate(a,'resumed',s)['rate'])} | {whole['pdus']} | {whole['la']} |")
lines+=['','Exchange boundedness awaits the complete captured series.','',
'| Direction | Sender | Attribute | New | JoinIn | In | JoinMt | Mt | Lv | LeaveAll |',
'|---|---|---|---|---|---|---|---|---|---|']
for d,a in rows.items():
 for s in ['DUT','bridge']:
  for typ in ['TalkerAdvertise','TalkerFailed','Listener','Domain']:
   c=collections.Counter()
   for r in a:c.update(r['msrp']['whole'][s]['types'][typ])
   lines.append(f'| DUT {d} | {s} | {typ} | '+' | '.join(str(c[e]) for e in ['New','JoinIn','In','JoinMt','Mt','Lv','LeaveAll'])+' |')
lines+=['','## Cycle evidence','',
'Paired counts use DUT / bridge order.',
'Counts cover each complete capture, including the unbound interval.','',
'TA and Listener counts include New, JoinIn, and JoinMt.',
'Ready counts require packed Ready within those declarations.','',
'| Direction | Cycle | Restart, seconds | PDUs | LeaveAll | TA declarations | Listener declarations | Ready | Result |',
'|---|---|---|---|---|---|---|---|---|']
for d,a in rows.items():
 for i,r in enumerate(a,1):
  ta=' / '.join(str(declared(r,s,'TalkerAdvertise')) for s in ['DUT','bridge'])
  li=' / '.join(str(declared(r,s,'Listener')) for s in ['DUT','bridge'])
  lines.append(f"| DUT {d} | {i} | {fmt(r.get('latency_s'))} | {pair(r,'pdus')} | {pair(r,'leaveall_vectors')} | {ta} | {li} | {pair(r,'ready')} | {r['status']} |")
lines+=['','## Counters and restoration','',
'The [register map](../reference/REGISTER_MAP.md) defines counter authority.',
'Legacy per-plane PDU counters are structural zeros.','',
'| Word | Meaning | Observed use |',
'|---|---|---|',
'| `0x650` | Legacy ACMP responder counts | Retained zero readbacks |',
'| `0x69C` | Legacy MSRP RX/TX counts | Retained zero readbacks |',
'| `0x6B0` | Legacy listener command/probe counts | Retained zero readbacks |',
'| `0x930` | Aggregate processor RX/TX and drops | Retained before/after readbacks |',
'| AECP GET_COUNTERS | Stream, interface, clock-domain counters | Retained before/after snapshots |','',
'Zero legacy words cannot measure current protocol traffic.',
'The per-cycle wire counts supply that measurement.','',
'Restoration verification is pending.','',
'## Acceptance','',
'| Issue criterion | Result | Evidence |',
'|---|---|---|']
lines.append(f'| First valid AVTP below one second | {status} for measured CRF | Per-direction distribution and all cycle records |')
lines.append('| Restart latency does not grow | PENDING | Ordered blocks and fitted trends |')
lines.append('| Firmware, topology, capture, distribution documented | PENDING | Identity, method, full capture index, restore evidence |')
lines+=['','This is an operator measurement, not an independent review.',
'It does not close #75 or qualify unmeasured formats.','',
'## Artifacts','',
'Raw files remain in private storage.',
'Artifact identifiers below map through `RAW-ARTIFACTS.json`.','',
'Each identifier records size and SHA-256.',
'No raw capture or binary enters the repository.','',
'| Image artifact | Bytes | SHA-256 |','|---|---|---|']
for r in json.loads((p/'image-artifacts.json').read_text()):
 lines.append(f"| `{r['artifact']}` | {r['size']} | `{r['sha256']}` |")
lines+=['','| Capture identifier | Bytes | SHA-256 |','|---|---|---|']
for f in sorted(p.glob('*/raw-artifacts.json')):
 for r in json.loads(f.read_text()):
  identifier=f.parent.name+'/tap.pcap'
  lines.append(f"| `{identifier}` | {r['size']} | `{r['sha256']}` |")
lines+=['','| Method artifact | Bytes | SHA-256 |','|---|---|---|']
for name in ['action.py','analyze.py','reconnect.py','capture.py','controller.py','avdecc_ro.py','wire_summary.py','integrity.py','report.py']:
 f=p/'tools'/name;b=f.read_bytes()
 lines.append('| \u0060tools/'+name+'\u0060 | '+str(len(b))+' | \u0060'+hashlib.sha256(b).hexdigest()+'\u0060 |')
lines+=['','The handoff packet contains acquisition and analysis source.',
'It also contains transcripts, decoded events, and manifests.','',
'## Validation','',
'Assigned validation gates remain pending.','',
'Reproduce analysis with the retained `analyze.py` and capture index.',
'Rebuild the page with retained `report.py`.','',
'Bench retention follows [TESTING.md section 6b](../testing/TESTING.md#6b-bench-evidence-retention).',
'All bench changes require complete restoration before handoff.','']
text='\n'.join(lines)
if (p/'conclusions.json').exists():
 c=json.loads((p/'conclusions.json').read_text())
 for old,key in [('Growth interpretation awaits the complete ordered series.','growth'),('Exchange boundedness awaits the complete captured series.','msrp'),('Restoration verification is pending.','restore'),('Assigned validation gates remain pending.','validation')]:
  text=text.replace(old,c[key])
 text=text.replace('| Restart latency does not grow | PENDING |', '| Restart latency does not grow | '+c['growth_result']+' |')
 text=text.replace('| Firmware, topology, capture, distribution documented | PENDING |', '| Firmware, topology, capture, distribution documented | PASS |')
out.write_text(text)
print(out.name,len(lines),'lines',out.stat().st_size,'bytes')
