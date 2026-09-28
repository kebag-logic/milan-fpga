"""Assemble the author handoff from the final source and retained evidence."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

root=Path('$LANES/590-592-599-firmware')
out=Path(__file__).parent
scratch=Path('$VALIDATION_STORAGE/590-a411')
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],cwd=root,text=True).strip()
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
plans=('all','uart-paced','queued-input','queued-short','queued-builtins','device-wait')
runs={}
for shape in ('1x1','8x8'):
    for plan in plans:
        waits='3000000-5000' if plan=='device-wait' else '0-0'
        runs[shape,plan]=json.loads((scratch/('service-'+shape+'-'+plan)/('service-'+plan+'-1-'+waits+'.json')).read_text())

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])+'\n'

def location(path,anchor):
    lines=(root/path).read_text().splitlines()
    matches=[i+1 for i,line in enumerate(lines) if anchor in line]
    assert matches,(path,anchor)
    return f'`{path}:{matches[0]}`'

fw='sw/firmware/milan_baremetal/milan_baremetal.c'
max8=max(m['maximum_ms'] for m in receipt['measurements'] if m['shape']=='endstation_ax7101_8x8' and m['cpu_hz']==50000000)
margin=24.5-max8
gained=24.30246-max8
max_gap=max(d['heartbeat_max_gap_ms'] for d in runs.values())
sections=[f'''# Round 3 handoff

Role: author [A411]. Reviewers: [R368] and [R369].
Status: assigned implementation and local validation complete; independent review pending.
Final local head: `{head}`.
Measured implementation head: `{receipt['base']}`.
Measured tree: `{receipt['tree']}`.
Firmware SHA-256: `{receipt['product_firmware_sha256']}`.
Processor pin: `{receipt['processor_pins']['protocol-processor']}`.
Branch: `590-592-599-firmware`.
Starting head: `c64f8cd896a4462bd42c4b90b32861ac7fd35176`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
[Round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5865679172).
[TAKEN](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5865703318).

## Reviewer responses

''']
rows=[
('R368-1 F1 / R369-1 F1 (repair retained)',location(fw,'static unsigned int phy_mdio_bit('),'Sample-before-rise behavior remains unchanged. The pinned reader audit, unchanged phase probe, host late-sample mutant and native late-sample control confirm the IEEE phase.'),
('R368-1 F2 / R369-1 F2 (repair retained)',location('sw/litex/patches/0006-bios-dispatch-hook.patch','+\t\tcommand_dispatch_hook();'),'Both queued-builtins positives cover all 1051 lines with continuous backing. Removing the hook produces the named per-line and backing findings. Long single built-in bodies remain the documented residual.'),
('R368-1 F3 (repair retained)',location('sw/firmware/nvm_hosttest/test_nvm_firmware.py','def grade_partial_ownership('),'The partial-ownership case and edge-crossing mutant remain active. The unchanged review mutant is caught on every shape; the final host self-test also checks the named edge assertion.'),
('R368-2 N1 (Conformance, RTL, Robustness, Tests)',location(fw,'if (!nvm_started)'), 'Startup admission precedes service reads and writes. Identity or shape rejection never admits the writer. Existing tag-mismatch and retirement rules remain.'),
('N1 test',location('sw/firmware/nvm_hosttest/test_disabled_writer.py','def grade('),'Every shape runs all Milan commands plus empty and unknown lines, twice, immediately and after 2500 ms. hb/backed/stale remain zero. Removing admission fails both rejected states. The unchanged review probe agrees.'),
('R368-2 N2 / R369-2 F4 (Docs; F4 also Conformance)',location('docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md','Timing. MEASURED'),'Sections 18 and 20.6 now identify the current receipt, six maxima and floor ratios. Final margin and margin gained are computed from that receipt; old byte-copy maximum is explicitly historical.'),
('R369-2 F5 (Docs)',location('docs/integration/BAREMETAL_FIRMWARE.md','A built-in body can lapse')+'; '+location('docs/findings/397_SERVICE_BUDGET.md','A built-in body can lapse'),'Both pages state the approximately 1750 ms body threshold: 2000 ms liveness less up to 250 ms phase before dispatch.'),
('R369-2 F6 (Conformance, Tests, Docs)','`native-evidence/`, `native-artifacts.json`, `final-target-gates.json`','Both queued-builtins positives, remove-dispatch, target late-sample and byte-only have retained raw logs and JSON receipts. Final regrades reconstruct the kept bytes and verify their SHA-256 bindings.'),
('S5',location(fw,'bios_dispatch_hook_required();')+'; '+location('sw/litex/patches/0006-bios-dispatch-hook.patch','Strong link marker'),'Firmware requires a symbol supplied by patch 0006. Host and actual RV32 product-link controls succeed with the marker and fail by name without it. Dependency documented where the hook is introduced.'),
('S5 forced builder fixture',location('sw/builder/test_builder.py','void bios_dispatch_hook_required(void) { }'),'Gate 35 links the complete firmware against BIOS stand-ins. Its fixture now supplies the required marker. The initial full bank exposed the missing stand-in; no assertion or grading rule changed.'),
('S6',location('sw/litex/patches/apply.sh','0006-bios-dispatch')+'; '+location('sw/builder/test_builder.py','carries the four patches'),'Series header includes 0006. Current patch count is four; the old six-patch example is explicitly historical.'),
('S7',location('tb/verilator/fw_service_budget/run.py','def dispatch_controls(')+'; '+location('tb/verilator/fw_service_budget/run.py','dispatch removal escaped per-line check'),'Removal verdict requires backing loss and a named per-line finding. Portable controls isolate missing line service while backing remains healthy, and reject backing-only verdicts.'),
('S8',location('sw/firmware/nvm_hosttest/phy_host.c','NAK after BMSR'),'Register-5 NAK follows successful BMSR/BMCR reads. Firmware publishes down; ignoring ACK would falsely negotiate 100FD and is caught.'),
('S9',location('docs/findings/397_SERVICE_BUDGET.md','unchanged phase probe')+'; '+location('docs/findings/397_SERVICE_BUDGET.md','N/A means'),'The phase probe has a verified public locator. Empty and unknown rows now consistently show N/A for a separate protocol deadline; shared service bounds are explained.'),
]
sections.append(table(['Item','Location','Change and evidence'],rows))
sections.append('''
Builder changes in round 3 are two comment corrections for S6 and the gate-35 BIOS-marker stand-in forced by the new firmware link dependency. The pre-existing combined-lane fixture remains 2 to 4. No builder grading rule changed. No RTL, processor, configuration, hardware, push, PR edit or merge occurred. Product LiteX patch 0006 was migrated by reversing its old text, then applying the new patch; the dependency revision remains pinned.

## MDIO phase proof

The pinned LiteX reader is `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4:litex/soc/software/libliteeth/mdio.c`. It performs two turnaround clocks and samples each data bit with MDC low. IEEE 802.3 22.3.4 permits PHY output to advance 0-300 ns after a rising edge. Therefore edge k launches frame bit k+1, which is sampled before edge k+1.

| Zero-based clock | Sample before rising edge | PHY launch after rising edge |
| --- | --- | --- |
| 0-45 | STA preamble and command | Released input |
| 46 | First turnaround, discarded | TA zero |
| 47 | TA zero, checked as ACK | D15 |
| 48-62 | D15 through D1 | D14 through D0 |
| 63 | D0 | Released line |

The two 32-cycle half-period delays allow at least 64 CPU cycles after the previous rising edge before sampling: 1280 ns at 50 MHz and 640 ns at the comparison clock. Both exceed the PHY maximum output delay plus the synchronizer allowance. Both committed peers retain the IEEE phase. The unchanged review probe reports true BMSR 0x796d, PHYID1 0x001c and link_status=13 under PHASE=1. Host and native late-sample controls fail their named negotiation check. Source identities and probe receipts are retained. Physical MDIO confirmation remains #599 acceptance 4 after merge.

## Dispatch hook and service plan

Patch 0006 places the weak default hook immediately after readline and before parsing or the empty-line guard. The product's strong override receives every line through LiteX whole-archive linking. It performs one rate-limited heartbeat/PHY opportunity without starting an automatic commit. Startup admission prevents rejected writers from answering. A required symbol makes a BIOS missing patch 0006 fail to link.

The queued-builtins plan contains 1051 lines and 14363 bytes: 350 repetitions of bounded memory read, empty line and unknown command, then status. The 133-byte requirement applies to the queue because the pinned line buffer is 128 bytes.

''')
rows=[]
for shape in ('1x1','8x8'):
 d=runs[shape,'queued-builtins'];commands=[r for r in d['rows'] if 'command_index' in r]
 rows.append([shape,len(commands),min(r['tick_calls'] for r in commands),f"{d['heartbeat_max_gap_ms']:.5f}",'0',f"{d['phy']['down_edges']}/{d['phy']['up_edges']}"])
sections.append(table(['Shape','Lines','Minimum ticks per line','Heartbeat gap ms','Unbacked cycles','Down/up'],rows))
sections.append('''
Long single built-in bodies remain the approved residual. Large memory reads and memory tests lack internal opportunities. A body can lapse backing after approximately 1750 ms, depending on the 250 ms phase. They can also exceed the 500 ms heartbeat and 250 ms PHY publication bounds.

## Edge guard

The partial-ownership host test reopens a record whose closed predecessor ends unaligned, poisons the open bytes, changes the predecessor, and checks both stage preservation and byte-identical committed output. The unchanged reviewer edge-cross mutant (`next - i >= 1u`) is killed by the named assertion on all five shapes, including Arty. `edge-control.json` records its expected raw rc 1 and successful control grade. The unchanged firmware passes the full host gate.

## Capture table

''')
rows=[]
for m in receipt['measurements']:
 rows.append(['1x1' if '1x1' in m['shape'] else '8x8',m['cpu_hz']//1000000,m['traffic'],len(m['rows']),f"{m['minimum_ms']:.5f}",f"{m['maximum_ms']:.5f}",f"{49/m['maximum_ms']:.4f}x"])
sections.append(table(['Shape','CPU MHz','Traffic','Samples','Minimum ms','Maximum ms','49 ms floor ratio'],rows))
sections.append(f'''\nFinal 8x8 contract maximum: {max8:.5f} ms. Margin to 24.5 ms: {margin:.5f} ms. Margin gained over the historical pre-word-copy 24.30246 ms maximum: {gained:.5f} ms. All 96 captures pass attestation, byte equality and open-record checks. Traffic counters are positive in ON arms and zero in OFF arms. The 100 MHz rows are non-contract comparisons. The capture SoC compiles the PHY path out, but the receipt binds the entire firmware source. Neither timing STOP condition occurred.\n\n## #397 harness table\n\n''')
rows=[]
for (shape,plan),d in runs.items():
 rows.append([shape,plan,f"{d['heartbeat_max_gap_ms']:.5f}",f"{500-d['heartbeat_max_gap_ms']:.5f}",'0',f"{d['phy']['down_edges']}/{d['phy']['up_edges']}",len(d['service_findings'])])
sections.append(table(['Shape','Plan','Heartbeat gap ms','500 ms margin','Unbacked cycles','Down/up','Findings'],rows))
sections.append('\nDevice-wait includes 3 s erase and 5 ms page WIP. Short plans claim only their observed edges. The following tables report every duty; startup costs and physical limits are defined in the authoritative findings page.\n\n')
findings=(root/'docs/findings/397_SERVICE_BUDGET.md').read_text()
start=findings.index('**1x1 elapsed duty maxima.**')
end=findings.index('The heartbeat bound adds',start)
sections.append(findings[start:end])
start=findings.index('| Shape | One transaction ms')
end=findings.index('Both Clause-22 peers',start)
sections.append(findings[start:end])
sections.append('''\nThe scheduling charge is the complete poll P plus nine maximum MDIO transactions T. The steady-state comparison is 125 ms trigger + duty stretch + UART allowance + P + 9T <= 250 ms. The conservative charge also fits the 50 ms page-poll allowance. These are simulation claims; physical boot, ordering, latency and switch cycling remain unmeasured.\n\n## Mutant and control table\n\n''')
rows=[['Writer admission removed','Both rejected states fail hb/backed/stale checks','Caught'],['BIOS marker removed','Host and actual RV32 links fail on bios_dispatch_hook_required','Caught'],['MDIO ACK ignored','Negotiation-stage NAK gives named status failure','Caught'],['Late sample, host','IEEE-phase negotiation fails','Caught'],['Edge crossing','Named open-record assertion on all five shapes','Caught'],['Per-line oracle','Missing tick rejected with healthy backing; backing-only verdict refused','Pass'],['MDIO phase probe','PHASE=1 true values and link_status=13','Pass']]
for mutation,plan in [('remove-dispatch','queued-builtins'),('remove-dispatch','queued-short'),('late-sample','all')]:
 d=json.loads((scratch/('service-'+mutation+'-'+plan)/('service-'+plan+'-1-0-0.json')).read_text())
 named=[f for f in d['service_findings'] if f.startswith('console line lacks')]
 description=f"{d['heartbeat_max_gap_ms']:.5f} ms gap; {len(named)} lines lack dispatch" if mutation=='remove-dispatch' else 'Named initial gigabit negotiation finding'
 rows.append([mutation+' target '+plan,description,'Caught, driver rc 0'])
byte=json.loads((scratch/'capture-byte-only/measurement.json').read_text())
base=json.loads((scratch/'capture-8x8-50-on/measurement.json').read_text())
rows.append(['Byte-only',f"{byte['minimum_ms']:.5f}-{byte['maximum_ms']:.5f} ms; minimum {byte['minimum_ms']/base['maximum_ms']:.5f}x against 1.5x floor",'Detected, rc 0'])
rows.extend([['Missing copy / traffic','Named capture oracle findings','Caught, drivers rc 0'],['Missing publication','Named target missing-publication failure','Caught, driver rc 0'],['Host writer / PHY controls','Existing five writer and four PHY mutants','Caught'],['Portable service controls','47 grading and 14 flash checks','rc 0']])
sections.append(table(['Control','Evidence','Result'],rows))
sections.append('\n## Gate table\n\nEvery gate below returned zero at the final local head. Commands ran from the physical worktree, in the foreground, with explicit timeouts and without pipelines.\n\n')
rows=[]
for filename in ('final-builder-gates.json','final-gates.json','final-target-gates.json'):
 records=json.loads((out/filename).read_text())
 for entry in records:
  assert entry['head']==head and entry['rc']==0,(filename,entry)
  rows.append([entry['name'],entry['rc'],entry['seconds'],f'`{filename}`'])
sections.append(table(['Gate','rc','Seconds','Exact command and digest manifest'],rows))
sections.append('''
The full compiler-present builder bank includes the ordered firmware census. The absent bank verifies all three compiler candidates are hidden and explicitly omits compiler-dependent instruments. Physical-utilization calibration remains NOT RUN because its required report is absent. Hosted checks, independent review, current-dev merge validation and post-merge containment belong to the later authorized merge turn.

The initial full-bank attempt at `69d8337352d79ffd4a7c0895dc14f0ae0d58811e` exposed the missing gate-35 BIOS-marker stand-in. `builder-fixture-failure-gates.json` retains those results and log bindings. The fixture was corrected and both full banks were rerun at the final head above. Firmware and native compiled inputs did not change.

## Evidence retention and reproduction

`native-artifacts.json` binds every kept native log/receipt by raw size and SHA-256, and every stored file by size and SHA-256. `native-commands.json` records commands and the measured implementation head. Files above 200 KB are gzip-compressed; compressed payloads above the limit are split into ordered `.partNN` files. Concatenate parts in their listed order, decompress when the artifact name ends in `.gz`, and verify the raw binding. No individual packet file exceeds 200 KB.

`regrade_kept.py` performs that reconstruction and runs `run.py --regrade` with identical scenario arguments against the retained native build. `final-target-gates.json` records each successful final-head regrade. Native build trees, toolchains and binaries remain outside this packet; `native-build-identities.json` and `build-input-identities.json` record their identities. `final-audit.json` verifies every final gate log binding. `product-link-guard.json`, `probe-commands.json` and `edge-control.json` retain the additional controls. `ENVIRONMENT-NOTE.md` records the corrected pre-simulation PATH failure.

The handoff is an author evidence claim, not a reviewer-owned completion ledger. No push or PR edit was performed. The separate #599 physical acceptance remains open.
''')
(out/'HANDOFF.md').write_text(''.join(sections))
pr=(out/'PR-BODY.md').read_text()
pr=pr.split('\n## Round 3\n')[0]
pr=pr.replace('Queued Milan commands and long validation walks', 'Every console line and long Milan validation walks')
pr=pr.replace('both queued plans and the device-wait plan', 'all queued plans and the device-wait plan')
start=pr.index('All six capture arms pass')
end=pr.index('\n\nThe byte-only control',start)
pr=pr[:start]+f'''All six current capture arms pass 16 captures each at processor pin `16be6768`. The final 8x8 maximum is {max8:.5f} ms at 50 MHz, leaving {margin:.5f} ms below 24.5 ms. It gains {gained:.5f} ms of margin over the historical pre-word-copy 24.30246 ms maximum. Both shapes pass all six service plans with continuous backing; the largest heartbeat gap is {max_gap:.5f} ms. The derived publication bound remains 250 ms within the measured duties. Round 3 below gives the current receipt and gate head.'''+pr[end:]
start=pr.index('Required local gates return zero at')
end=pr.index('\n\nThe physical switch-cycle',start)
pr=pr[:start]+f"Required local gates return zero at `{head}`: both compiler modes of the full builder bank, all-shape host tests including Arty, firmware census, capture receipt, service checks, CI scope, source/documentation checks and whitespace. The original builder fixture remains 2 to 4; Round 3 corrects patch-count comments and adds the BIOS-marker stand-in required by the gate-35 host fixture. Physical-utilization calibration remains unrun because its report is absent; compiler-absent mode records its instrument omission."+pr[end:]
pr=pr.replace('Round 2 answers R368-1 and R369-1. Its measurements, controls and gate head supersede the round-1 figures above.', 'Round 2 answers R368-1 and R369-1. The following round-2 measurements and gate head are historical; Round 3 supersedes them.')
pr+='''\n\n## Round 3\n\nRound 3 answers R368-2 N1/N2 and R369-2 F4-F6, and implements S5-S9.\n\nStartup admission now guards every heartbeat path. Identity and shape rejection keep `hb=0`, `backed=0`, and `stale=0` through console input, including empty lines and every Milan command. The test passes all five shapes, including Arty; removing the guard fails both rejected states. Patch 0006 supplies a required link marker, and both host and actual RV32 link controls fail when it is absent.\n\nThe dispatch-removal verdict now requires both continuous-backing loss and its named per-line finding, with portable controls. A negotiation-stage NAK kills an ignored-ACK mutant. Patch-series wording and the phase-probe locator are corrected. The duty tables explain N/A deadlines. Both firmware pages state that a long built-in body can lapse backing after approximately 1750 ms because up to 250 ms of rate-limit phase can precede dispatch.\n\n'''
pr+=f"The refreshed capture receipt binds firmware `{receipt['product_firmware_sha256']}` and measured tree `{receipt['tree']}`. All six arms pass with zero byte mismatches and zero open-record copies. The final 8x8 maximum is {max8:.5f} ms; margin to 24.5 ms is {margin:.5f} ms and margin gained is {gained:.5f} ms. The snapshot-ownership authority now matches these values.\n\n"
pr+=table(['Shape','CPU MHz','Traffic','Maximum ms'],[['1x1' if '1x1' in m['shape'] else '8x8',m['cpu_hz']//1000000,m['traffic'],f"{m['maximum_ms']:.5f}"] for m in receipt['measurements']])
pr+=f'''\nBoth shapes pass all six service plans with zero unbacked cycles. Both queued-builtins arms service all 1051 lines. Native dispatch-removal, late-sample and byte-only controls pass their named oracles. Raw logs and JSON receipts are retained under `native-evidence/`, compressed where needed, with SHA-256 and size bindings. Regrading the kept service logs passes at `{head}`.\n\nRequired local gates return zero at that head: both full builder modes, firmware census, all-shape host self-test, capture gate, service oracle and kept-log regrades, CI scope, documentation/source gates and whitespace. No timing STOP condition occurred. Round-3 builder changes are patch-count comments and the BIOS-marker stand-in required by the gate-35 host fixture; grading rules are unchanged. The existing physical-utilization calibration remains unrun because its report is absent, and the compiler-absent bank records its instrument omission.\n\nThe physical #599 switch-cycle acceptance remains the post-merge lane. Independent review is pending.\n'''
assert pr.startswith('[A385]\n')
assert '/home/' not in pr
(out/'PR-BODY.md').write_text(pr)
print('Final handoff and Round 3 PR body assembled for '+head)
