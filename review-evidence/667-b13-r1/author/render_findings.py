"""Render the bounded measurement tables into the assigned findings page."""
import csv,hashlib,json,sys
from pathlib import Path
out=Path(sys.argv[1]);target=Path(sys.argv[2])
def read(name):return json.loads((out/name).read_text())
def csvrows(name):return list(csv.DictReader((out/name).open()))
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','|'+'|'.join('---' for _ in head)+'|']+['| '+' | '.join(map(str,r))+' |' for r in rows])
a=read('startup-summary.json');s=read('soak-summary.json');r=read('restore-summary.json');assert a['cycles']==100 and r['result']=='PASS'
cycles=csvrows('startup-cycles.csv');soak=csvrows('soak-cycles.csv');ctr=csvrows('counter-deltas.csv');console=read('console-restore.json')
startup_table=table(['Cycle','EARLY','LATE','First sequence','First step (ns)','First offset (ns)'],[[x['cycle'].split('-')[1],x['early'],x['late'],x['first_sequence'],x['first_step_ns'],x['first_offset_from_steady_ns']] for x in cycles])
distribution=table(['First-to-second step (ns)','Binds'],[[k,v] for k,v in a['first_step_ns']['histogram'].items()])
counter_table=table(['Role','Descriptor','Index','Counter','Start','End','Delta'],[[x[k] for k in ('role','descriptor','index','counter','start','end','delta')] for x in ctr])
soak_table=table(['Cycle','Elapsed (s)','Counter errors','Segment gaps','Recovered by overlap'],[[x[k] for k in ('cycle','elapsed_s','counter_errors','segment_sequence_gaps','overlap_recovered')] for x in soak])
artifacts=['build-provenance.json','counter-deltas.csv','soak-cycles.csv','startup-cycles.csv','startup-first-ten.csv','restore-summary.json','capture-artifacts.jsonl']
artifact_table=table(['Packet receipt','Bytes','SHA-256'],[[name,(out/name).stat().st_size,hashlib.sha256((out/name).read_bytes()).hexdigest()] for name in artifacts])
text=f"""<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Talker startup and soak observations

Refs #667. Operator [A549]. These are operator observations.

The [B13 assignment](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6009837251) defines this findings-only lane.
The assigned image is dev `28f9666f`, seed `asl`.

## Contents

- **[#667 bench: talker start on dev 28f9666f, 2026-10-06](#667-bench-talker-start-on-dev-28f9666f-2026-10-06)** -- Records the startup measurements and their limits.
- **[Soak record](#soak-record)** -- Records periodic counters and retained stream captures.
- **[Method and authorities](#method-and-authorities)** -- Defines field decoding and counter interpretation.
- **[Restoration and evidence](#restoration-and-evidence)** -- Records final readbacks and reproducible checks.

## #667 bench: talker start on dev 28f9666f, 2026-10-06

The four assigned ATDECC identity fields matched.
Console VERSION `0x00020060` and AEM CRC `5ba355eb` also matched.

All 100 binds and unbinds succeeded.
Each bind held the DUT talker for two seconds.
The reference peer reported EARLY in {a['early_positive_cycles']} binds.
The total EARLY count was {a['early_total']}.
LATE remained zero across all 100 binds.

All 14 EARLY-positive binds had backward first-to-second timestamp steps.
Those steps ranged from -544,469,385 to -279,759,747 ns.
The other 86 steps ranged from 124,999 to 125,020 ns.
Each increment was observed before unbind submission.
The observation lead was at least 1,900.062 ms.

The startup behavior remains observable on this image.
The [B12 characterization](653_DISCONNECT_ORDER_BENCH.md#b12-startup-characterization-2026-10-05) found two affected binds among 70.
Its first-to-second steps were -23,612,829 ns and +521,369,096 ns.
[PR #666](https://github.com/kebag-logic/milan-fpga/pull/666) records that earlier evidence.
These batches describe observations; they establish no rate trend.

Every bind retains its first ten AAF headers.
All 1,000 headers have `tv=1` and `tu=0`.
Sequence progression remains consecutive within every captured start.

First-step distribution:

{distribution}

The next table reports every bind independently.
A step is the signed timestamp difference, PDU 2 minus PDU 1.
The offset is the steady period minus that step.
The packet also retains each header against PDU 10's trend.

{startup_table}

## Soak record

The soak ran from 05:27:00.782 to 07:27:04.752 UTC.
Its duration was {s['elapsed_s']:.3f} seconds on 2026-10-06.
AAF and CRF were bound in both directions.
All 145 counter checkpoints had zero assigned error-class increases.
Grandmaster, asCapable and path observations remained unchanged.

Each checkpoint issued nine GET_COUNTERS requests.
These covered every DUT counter descriptor and both bound peer inputs.
DUT ENTITY counters consistently returned NOT_SUPPORTED.
The other eight requests consistently returned SUCCESS.
Together, they exposed 61 valid counters.

The longest checkpoint interval was {s['max_poll_interval_s']:.3f} seconds.
Each checkpoint also read GET_AVB_INFO and GET_AS_PATH.
Both entities received those timing requests.
This exceeded the assigned five-minute timing cadence.

The table preserves each counter's first and last bound observation.
Input counters reset on binding, as Milan requires.
Frame-counter values can represent observation intervals, rather than packet totals.
Milan Tables 5.4 and 5.6 define that distinction.

{counter_table}

There were 145 overlapping segments for each capture type.
The tap retained plain and VLAN-tagged AVTP separately.
A companion controller capture retained control traffic.
Nine segment-local sequence gaps were fully recovered by overlap.
There were no uncovered boundaries between successive stream segments.

Of 435 capture receipts, 434 included a zero drop statistic.
Segment 063's VLAN receipt omitted that statistic.
Its captured and received totals remain available.
The independent sequence and overlap receipts cover that segment.

A final AAF media-reset toggle followed the CRF-input unbind response.
The adjacent sequence numbers were 159 and 160.
That transition occurred after the completed soak window.
The packet retains the control and media boundary timestamps.

Per-checkpoint results follow.
Segment gaps refer to individual files before overlap recovery.

{soak_table}

## Method and authorities

Each bind read both current stream formats.
Every observed listener format already matched its talker.
The runner adapts a differing listener before binding.

The pinned controller library is `a71ffa99`.
The application counter rule is pinned at `a13db9d9`.
The library and probe were built from verified source.
Both builds returned zero.
The earlier build was absent on the controller host.

Foreground actions held the shared bench lock.
Every action had an explicit deadline.

Each tap record contains a 28-byte prefix.
Timestamp decoding uses high-word then low-word ordering.
Raw bytes independently checked the decoded field positions.
Presentation steps use signed modulo-2^32 timestamp differences.
Sequence checks use modulo-256 progression.

The steady period uses timestamp steps following the first ten PDUs.
Absolute gPTP correlation is NOT RUN.
No measured tap-to-gPTP clock mapping is available.
Counter observations bound event timing within the controller's clock.
They do not identify individual offending packets.

| Authority | Applied rule |
|---|---|
| IEEE 1722-2016, Sections 4.4.4.3 and 4.4.4.5-4.4.4.9; Clause 7 | Media reset, timestamp validity, sequence, uncertainty and AAF presentation fields. |
| IEEE 1722.1-2021, Sections 7.4.40-7.4.42 | Interface timing, path and descriptor counter readbacks. |
| IEEE 1722.1-2021, Sections 8.2.1, 8.2.4 and 8.2.5 | ACMP field identities and successful connection responses. |
| Milan v1.2, Section 5.3.7.7, Table 5.4 | Output counter meanings and observation intervals. |
| Milan v1.2, Section 5.3.8.10, Table 5.6 | Input counter meanings and reset upon binding. |

## Restoration and evidence

The final survey matched all 42 effective-state observations.
Both descriptor inventories also matched.
All eighteen final binding readbacks were zero.
All eighteen stream formats matched their saved values.
Both source selections and all four mapping fingerprints matched.

The documented source-release sequence restored the idle servo state.
Final MCSRV_STAT was `0x00000020`; MCSRV_CTRL was zero.
The audio control and status readback matched its initial bytes.

NVM image sequence advanced from 230 to {console['nvm_end']['image_sequence']}.
Successful commits advanced from zero to {console['nvm_end']['commits_ok']}.
Failed commits, dirty and stale state remained zero.
Those monotonic bookkeeping values were retained, rather than reset.

Both controller sessions deregistered from both entities successfully.
Every temporary capture and probe process exited.
The bench lock was released and checked free.
Host prerequisites remained present at final readback.

The local packet is `667-b13-a549`.
It includes per-cycle headers, counter receipts and restoration comparisons.
Its manifest covers the bounded files.
Large captures remain outside the packet under `/tmp`.
Their index records each size and SHA-256 value.
The decoder and restoration checks passed 22 offline controls.

{artifact_table}
"""
target.write_text(text)
print(json.dumps({'file':target.name,'bytes':len(text.encode())}))
