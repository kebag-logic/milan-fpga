'''Write the final handoff only after all required evidence is complete.'''
from pathlib import Path
import hashlib
import json
import subprocess
import re
root=Path.cwd()
out=Path(__file__).parent
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
fw=root/'sw/firmware/milan_baremetal/milan_baremetal.c'
firmware_hash=hashlib.sha256(fw.read_bytes()).hexdigest()
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
assert receipt['product_firmware_sha256']==firmware_hash
assert receipt['processor_pins']['protocol-processor']=='16be6768f710e79450aace277abacd6c2c3336e5'
gates=json.loads((out/'final-gates.json').read_text())+json.loads((out/'final-builder-gates.json').read_text())+json.loads((out/'final-target-gates.json').read_text())
assert all(g['rc']==0 and g['head']==head for g in gates)
plans=('all','uart-paced','queued-input','queued-short','device-wait')
runs={}
for shape in ('1x1','8x8'):
 for plan in plans:
  base=Path('/tmp/a385-final3-service-'+shape+('' if plan=='all' else '-'+plan))
  q=base/('service-'+plan+'-1-'+('3000000-5000' if plan=='device-wait' else '0-0')+'.json')
  d=json.loads(q.read_text());assert d['service_findings']==[]
  runs[shape,plan]=d

def table(headers,rows):
 return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])+'\n'
def max_duty(shape, duty):
 rows=[r for p in plans for r in runs[shape,p]['rows'] if r['duty']==duty or (duty in ('milan_settime','milan_utc') and r['duty'].startswith(duty+' '))]
 return max(r['no_tick_ms'] for r in rows)
parts=[f'''# [A385] Combined firmware lane handoff

Status: author implementation and assigned local validation complete; independent review pending.
Head: `{head}`. Branch: `590-592-599-firmware`.
Origin: `https://github.com/kebag-logic/milan-fpga.git`.
[Assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529).
[Scope correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453).
Internal reviewer: [R368]. External reviewer: [R369].

The preserved draft became three per-issue commits: #590 `4befe3f0d`, #592 `a133358f9`, #599 `f420e1a73`.
Merge `42f7f4fe7` incorporated dev `20aa4eabf` without conflicts or resolution edits.
The processor is initialized at `16be6768f710e79450aace277abacd6c2c3336e5`.
Commit `999a03255` changes only the authorized builder selection count from 2 to 4.
Commit `0d6f697ac` adds target service/control evidence; `7eae38744` services the wipe boundary.
Later commits bind the peer sources and record documentation and measurement evidence.
All subjects are one line, without bodies or trailers.

Firmware SHA-256: `{firmware_hash}`; size: {fw.stat().st_size} bytes.
All six final captures use this firmware and the merged processor pin.
Earlier `870ff88a` captures and the pre-wipe-tick merged-pin runs are historical only.
No push, PR operation, hardware action, RTL edit, processor source/configuration edit or extra checkout occurred.
The earlier STOP is resolved by the public fixture correction.
A later host probe found delayed recovery after a brief latched loss; the corrected poll publishes the loss and resolves recovered state in the same call.
All earlier final2 captures and service runs are historical after that correction.
Neither assignment timing STOP condition was reached.

## Per-issue changes and acceptance

| Issue | Changes with file:line | Acceptance evidence |
| --- | --- | --- |
| #590 | `sw/firmware/milan_baremetal/milan_baremetal.c:473` CRC opportunity every 256 bytes; `:636` validation every 16 records; `:1635`, `:1737`, `:1770`, `:1781`, `:1802` command-entry service; `:1754` between wipe erases | Same 250 ms heartbeat rate limit; 133 queued bytes on both shapes; continuous backing in every plan; dispatch-removal control loses backing; findings page refreshed |
| #592 | `sw/firmware/milan_baremetal/milan_baremetal.c:447`, `:1170` aligned word interiors within each closed record, byte edges; capture `firmware.py` and `run.py` preserve poison/traffic controls and add byte-only timing control | Six final arms, 16 captures each, byte-identical copies with no open-record copy; optimized 8x8 fits 24.5 ms; byte-only restores 24.30636 ms |
| #599 | `sw/firmware/milan_baremetal/milan_baremetal.c:773` derived 125 ms trigger; `:790` bit-bang; `:826` negotiation; `:873` discovery/publication; `:921` service entry | Clause-22 link/speed/duplex publication; host modes/error/discovery checks; actual MAC_STATUS and fabric counter simulation; no-publish mutation caught; acceptance 4 remains a later physical lane |
| Tests | `sw/firmware/nvm_hosttest/phy_host.c:30`, `test_phy_firmware.py:11`; `tb/verilator/fw_service_budget/phy.py:1`, `phy.hpp:8`, `run.py:344`, `sim_main.cpp:36` | All-shape host suite including Arty, target scheduling and explicit controls |
| Documentation | `docs/findings/397_SERVICE_BUDGET.md:1`, `docs/integration/BAREMETAL_FIRMWARE.md:66`, `docs/reference/REGISTER_MAP.md` MAC_STATUS, compliance matrix item 7.4.42.2, both harness READMEs | One-hart contract, timing derivation, ownership, historical clock correction, reproduction and limits |

## Tick placement and measured stretches

The table gives maximum no-tick stretches across five final plans on each shape.
CRC and record-validation placements jointly bound status/commit work.
Command-entry opportunities also bound repeated short commands that suppress idle service.
Wipe's midpoint separates two approximately 74 ms verification walks at 8x8.
''']
rows=[]
for label,duty in [('Dispatch status','milan_status'),('Dispatch gettime','milan_gettime'),('Dispatch settime variants','milan_settime'),('Dispatch UTC variants','milan_utc'),('Status CRC/record walks','milan_nvm'),('Commit CRC/record walks','milan_nvm commit'),('Wipe midpoint','milan_nvm wipe'),('Existing erase wait','erase_enclosed_to_first_program'),('Existing restore','restore_walk')]:
 rows.append([label,f'{max_duty("1x1",duty):.5f}',f'{max_duty("8x8",duty):.5f}'])
parts.append(table(['Placement/duty','1x1 no-tick ms','8x8 no-tick ms'],rows))
parts.append('''
The authoritative findings page includes every duty's elapsed time, tick gap, full UART allowance,
500 ms conditional heartbeat comparison and PHY comparison.
The ordinary-command duration comparison is not a UART protocol deadline.
Long commands are serviced internally; old duration findings remain visible in raw receipts.
Boot's initial unarmed prefix precedes the first heartbeat.

## MDIO poll-period derivation

One hart has 500 ms maximum heartbeat period minus the unchanged 250 ms rate-limit phase.
The stated publication period bound is 250 ms.
Allocate 125 ms to the PHY trigger, reserving 125 ms for
pending duty time, full TX serialization and a conservative poll scheduling charge.
The steady-state check is `125 + no-tick + UART allowance + scheduling charge <= 250 ms`.
Startup AEM/restore entries report isolated service-plus-poll costs; they are not whole startup publication bounds.
Actual publication-readback gaps independently check startup and runtime against 250 ms.
The poll envelope begins at retired heartbeat entry and includes clock acquisition,
all Clause-22 transactions, resolution and publication bookkeeping.
The scheduling charge is `C = P + 9*T`: the largest measured complete poll plus nine
maximum measured transactions. The nine-read ceiling covers discovery, two BMSR reads,
BMCR, extended status and both local/peer negotiation pairs.
This deliberately counts observed transaction time twice and covers the longer fallback
path without claiming that every fallback was target-measured.
''')
rows=[]
for shape in ('1x1','8x8'):
 tx=max(runs[shape,p]['phy']['max_transaction_sys_cycles'] for p in plans)/100000
 poll=max(runs[shape,p]['phy']['max_poll_sys_cycles'] for p in plans)/100000
 gaps=[(b['cycle']-a['cycle'])/100000 for p in plans for reads in [[e for e in runs[shape,p]['events'] if e['kind']=='phy_read']] for a,b in zip(reads,reads[1:])]
 rows.append([shape,f'{tx:.5f}',f'{poll:.5f}',f'{poll+9*tx:.5f}',f'{max(gaps):.5f}',f'{50-poll-9*tx:.5f}'])
parts.append(table(['Shape','Transaction ms','Complete poll ms','Scheduling charge ms','Largest observed publication gap ms','50 ms page-poll margin'],rows))
rows=[]
for shape in ('1x1','8x8'):
 poll=(max(runs[shape,p]['phy']['max_poll_sys_cycles'] for p in plans)+9*max(runs[shape,p]['phy']['max_transaction_sys_cycles'] for p in plans))/100000
 grouped={}
 for plan in plans:
  for r in runs[shape,plan]['rows']:
   duty=r['duty']
   if duty in ('boot_to_entity_enabled','aem_copy_crc','restore_walk','maximum_heartbeat_gap'): continue
   if duty.startswith(('milan_settime ','milan_utc ')): duty=duty.split()[0]
   grouped.setdefault(duty,[]).append(r)
 cost=max(max(r['no_tick_ms'] for r in group)+max(r['uart_tx_allowance_ms'] for r in group)+poll for group in grouped.values())
 assert cost <= 125
 rows.append([shape,f'{cost:.5f}',f'{250-cost:.5f}','125.00000',f'{125-cost:.5f}'])
parts.append(table(['Shape','Worst duty + UART + charge ms','Maximum permissible trigger ms','Selected trigger ms','Remaining reserve ms'],rows))

parts.append('''
The simulations read MAC_STATUS through a separate bus master and sample actual fabric counters.
Every queued/device-wait plan sees one down/up cycle and no repeated-publication counter increments.
1000-to-100 Mb/s negotiation is visible in MAC_STATUS after 2.4 s.
Short plans claim only their observed edges.
Physical switch-cycle acceptance remains #599 acceptance 4, after merge.

## Capture table
''')
rows=[]
for d in receipt['measurements']:
 maximum=max(r['sys_cycles'] for r in d['rows'])/100000
 rows.append([d['shape'],d['cpu_hz']//1000000,d['traffic'],len(d['rows']),f'{maximum:.5f}',f'{24.5-maximum:.5f}','rc 0'])
parts.append(table(['Shape','CPU MHz','Traffic','Captures','Maximum ms','24.5 ms margin','Result'],rows))
contract_max=max(d['maximum_ms'] for d in receipt['measurements'] if d['shape']=='endstation_ax7101_8x8' and d['cpu_hz']==50000000)
parts.append(f'\nThe previous 8x8 maximum was 24.30246 ms, leaving 0.19754 ms. The new capture gains {24.30246-contract_max:.5f} ms of margin.\n')
parts.append('''
The four 50 MHz arms are contract evidence. The 100 MHz 8x8 pair is a labelled non-contract comparison.
All destination-byte/open-record checks pass; traffic-on arms also have concurrent requests, responses and reads.
The replaced receipt binds the final firmware digest, processor pin, generated CPU/BIOS/image identities and harness.

## #397 harness table
''')
rows=[]
for shape in ('1x1','8x8'):
 for plan in plans:
  d=runs[shape,plan]
  rows.append([shape,plan,f'{d["heartbeat_max_gap_ms"]:.5f}','0',f'{d["phy"]["down_edges"]}/{d["phy"]["up_edges"]}','rc 0'])
parts.append(table(['Shape','Plan','Max heartbeat gap ms','Unbacked cycles','Down/up edges','Service verdict'],rows))
parts.append('''
All plans use populated A/B media. Device-wait uses 3000000 us erase and 5000 us page WIP; other plans use zero WIP.
Both queued-input plans contain 133 bytes; both queued-short plans contain 350 status commands.
The historical 8x8 #397 generation declared gPTP/lwSRP at 100 MHz despite its 50 MHz CPU override.
Both current configurations and generated constants declare 50 MHz.

## Mutants and controls

| Control | Observed result |
| --- | --- |
| Dispatch removed, 350 queued status commands | Driver rc 0; heartbeat gap 2769.99979 ms; 77036936 unbacked system cycles; named backing refusal |
| Unmodified 350-command positive | Both shapes pass; zero unbacked cycles |
| Byte-only 8x8 capture | Two captures, driver rc 0, maximum 24.30636 ms versus the merged-pin historical 24.30246 ms; old copy cost restored |
| Missing-copy capture | Driver rc 0; destination poison/byte oracle rejects missing word and byte stores |
| Missing traffic | Driver rc 0; concurrent-traffic oracle rejects the traffic-on claim |
| Publisher removed, host | Named publication assertion rejects mutation |
| Latched recovery deferred, host | Current-state assertion rejects the old second-poll delay |
| Publisher removed, target | Driver rc 0; named missing-publication evidence check rejects mutation |
| Four existing NVM host mutants | Every planted defect caught across the all-shape self-test |
| Capture receipt controls | Seven planted receipt/grading errors refused by the final gate |
| Service portable controls | 42 grading controls and 14 flash controls, rc 0 |
| PHY reuse inventory | Both new peer files bound to compiled reuse; changed-file controls refuse stale builds |

## Gate table

Every command runs from the physical workspace path with a foreground timeout and no output pipeline.
The following final results name the same committed head shown above.
Large logs remain outside this output directory; each artifact has a recorded size and SHA-256.
''')
rows=[]
for g in gates:
 rows.append([g['name'],'`'+' '.join(g['command'])+'`',g['rc'],Path(g['path']).name])
parts.append(table(['Gate','Exact command','rc','Log artifact'],rows))
parts.append('''
The compiler-present full bank retains one NOT RUN arm: its existing physical utilization-report calibration.
The report is absent and hardware is outside this lane.
The absent bank additionally registers the compiler-dependent instrument group as NOT RUN.
All elaboration arms execute; those explicit omissions are not presented as passes.
The absent wrapper hides all three cross-compiler candidates while retaining real host probes and the entire builder bank.

## Reproduction and artifact limits

`capture-artifacts-final.json` and `service-artifacts-final.json` record large artifact hashes and sizes.
`final-gates.json`, `final-builder-gates.json` and `final-target-gates.json` bind command results to the final head.
`control-artifacts-final.json` records the corresponding control receipts and logs.
`replace_capture_receipt.py` checks all six capture oracles and byte-binds instrumented firmware before replacement.
`refresh_service_findings.py` requires all ten successful service plans before generating the tables.
All target commands use the existing offline product environment, explicit physical workspace and external build directories.
Capture timeout is 14400 seconds; service timeout is 28800 seconds.
Use the retained per-run command inventory and repository recipes to reproduce each arm.

No output-directory file exceeds 200 KB; toolchains, packages, generated trees and executables remain outside it.
The SPI boundary remains optimistic (historical 67/65 cycles for 8 bits and 259/257 for 32 bits).
DDR is simulated and only one deterministic clock phase is measured.
No physical boot, twofold physical commit margin or field torture acceptance is claimed.
Future update, fault-log and temperature duties remain unmeasured under #397.

The branch is local and ready for the assigned independent reviewers.
Hosted gates and the deferred physical #599 rerun remain subsequent workflow steps.
No author validation in this packet is a review verdict.
''')
mutant=json.loads(Path('/tmp/a385-final3-service-remove-dispatch/service-queued-short-1-0-0.json').read_text())
byte_control=json.loads(Path('/tmp/a385-final3-capture-byte-only/measurement.json').read_text())
byte_ms=max(r['sys_cycles'] for r in byte_control['rows'])/100000
lost=re.search(r'BACKING armed=1 unbacked_cycles=(\d+)',mutant['raw_log'])
assert lost and int(lost[1])>0 and 'continuous backing lost' in mutant['service_findings']
text='\n'.join(parts)
text=text.replace('2769.99979',f'{mutant["heartbeat_max_gap_ms"]:.5f}')
text=text.replace('77036936',lost[1]).replace('24.30636',f'{byte_ms:.5f}')
(out/'HANDOFF.md').write_text(text)
print('Wrote final handoff',head)
