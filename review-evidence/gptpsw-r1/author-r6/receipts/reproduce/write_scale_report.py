from pathlib import Path
import datetime,json
from zoneinfo import ZoneInfo
BASE=Path('/data-2/milan/tmp/opt-a837');SCALE=BASE/'scale'
OUT=Path('$MANAGEMENT/2026-09-23/opt-a837/round1')
analyses={arm:json.loads((SCALE/(arm+'-analysis.json')).read_text()) for arm in ('32-d0','32-d8')}
strict={arm:json.loads((SCALE/arm/'strict-grades.json').read_text()) for arm in analyses}
build64=json.loads((SCALE/'64-build-verdict.json').read_text())
now=datetime.datetime.now(ZoneInfo('Europe/Warsaw')).strftime('%Y-%m-%d %H:%M CET')
lines=[f'STATUS: {build64["verdict"]}. Updated {now}.', '', '# [A837] two-hart scale, round 1', '',
'#966 is locally review-ready at `44c566399002db32bf8a6ad3ce719488d418bcb0`. No push or PR edit was made.', '',
'## Source and measurement identity', '',
'The scale branch is `opt-hart2-a837-r1` in `/data-2/milan/lanes/opt-hart2`, head `fe009fa2c7741b8612bdbc74fe70909d57931503`, based on the #966 repair. It composes int4 `3f36b457`, A808’s scale ports, the interface-specific probe repair `fcad6d10`, tsn-c-stack `115df0bec6d45269979d4d7a9cebc4cd727b9fe1`, and lwSRP `0757869e6cd9af6ea4fd04824e3a501664698a39`. The scale-only transmit cap is 16 values and the attribute bucket count is 16. Zbb remains off.', '',
'The two 32x32 models were built at `368c2d1e9898e43849873bd242fba482924817f0`. Later edits affect self-tests, documentation and the native input manifest. The recorded source inputs and native executables remain byte-identical. The original manifest omitted the passive cost-observer header; the original manifests remain unchanged, and `scale-input-equivalence.json` supplies its build-head hash and compiler dependency evidence. The corrected builder refuses reuse without that header recorded.', '',
'The one-hart 32x32 ELF is byte-identical before and after the new observer/cache-selection changes: 196024 bytes, SHA-256 `2b05feba4c2c7ff44f0eda69dadf9dc882124b553ada835e7e93db9a0add1cc7`. This compares the composed scale baseline at `32d78e99` with `368c2d1e`; it does not assert identity across the earlier accepted fold and scale ports. Both two-hart cache arms use the same 211544-byte ELF, SHA-256 `c96b345a11fac7fb27aa656664c19c57a0b39e274c9e71292f761f7a12e9a553`.', '',
'## 32x32/2if: nine Arm A groups', '',
'Both harts run at 100 MHz. Hart 1 has 16 KiB instruction cache in both arms, with no data cache or 8 KiB data cache as named. Worst pass includes completed work passes and the maximum of idle-pass runs. THE SHARE is 2.0 ms (200000 cycles). These are Arm A measurements without staged firmware gPTP; its long-window charge is shown separately.', '',
'| Group | D$0 H0 ms | D$0 H1 ms | D$8 H0 ms | D$8 H1 ms | D$0 grade / strict | D$8 grade / strict |', '|---|---:|---:|---:|---:|---:|---:|']
groupmaps={arm:{g['group']:g for g in a['groups']} for arm,a in analyses.items()}
graders={arm:{g['group']:g for g in s['groups']} for arm,s in strict.items()}
order=('srp','backlog-owed','backlog-adp-refill','control','adp-link','acmp-noresp','maap','aecp','acmp-notk')
for name in order:
 vals=[groupmaps[arm][name]['harts'][h]['worst']/100000 for arm in analyses for h in (0,1)]
 grades=[f"{graders[a][name]['record_mode_rc']} / {graders[a][name]['strict_rc']}" for a in analyses]
 lines.append('| '+name+' | '+' | '.join(f'{v:.5f}' for v in vals)+' | '+' | '.join(grades)+' |')
lines+=['', 'The original commands record budget and SHARE findings; their exit codes do not waive recorded findings. The strict grades additionally make those findings fail. Every finding and original command is retained in the receipts. The quoted budget messages give total measured latency: for example, 64.226 ms is compared with 20 ms, not an additional 64.226 ms beyond it.']
for arm,a in analyses.items():
 launch=json.loads((BASE/('scale32-'+arm.split('-')[1]+'.log.json')).read_text())
 work=[sum(g['harts'][h]['work'] for g in a['groups']) for h in (0,1)]
 idle=[sum(g['harts'][h]['idle'] for g in a['groups']) for h in (0,1)]
 over=[sum(g['harts'][h]['work_over']+g['harts'][h]['idle_runs_over'] for g in a['groups']) for h in (0,1)]
 lines+=['',f'{arm}: original matrix command rc {launch["rc"]}; strict matrix rc {strict[arm]["strict_rc"]}. Work passes H0/H1 {work}; idle passes {idle}; over-SHARE work passes plus idle runs {over}.']
 lines+=['',f'{arm} nonzero grades / findings:', '']
 for name in order:
  p=SCALE/arm/'group-grades'/(name+'-verdict.json');g=json.loads(p.read_text())
  findings=g['refusals']+g['budget_misses']+g['share_misses']+g['other_findings']
  for f in findings:lines.append('- '+f)
lines+=['', 'The cached MAAP run also has two join intervals of 180.928 and 180.929 ms, below 181.0 ms; these remain unwaived. The MAAP periodic-opportunity findings are retained. In each cache arm the reported interface-1 timer expiries predate that interface’s link-up; first subsequent MSRP and MVRP builds start within 0.55 ms. The current grader retains LINK timestamps but drops LINK values. This is diagnostic context, not a protocol verdict or a bound waiver.', '',
'## Per-hart long-window load and gPTP placement', '',
'These are demand-model loads, not measured CPU occupancy or a closed worst-case proof. The inherited arrival-rate equations are evaluated using sampled two-hart costs where available; each sample maximum receives 5% and rounds up to 5 us. Inclusive polls can only proxy individual owed items. All transferred terms remain listed below. The generated 32x32 shape has 33 slots; the conservative per-interface sink count is 17 and it has 68 counter-bearing descriptors.', '',
'| Hart 1 D$ | gPTP charged to | H0 load | H1 load |', '|---|---:|---:|---:|']
for arm,a in analyses.items():
 for case in a['charge_cases']:lines.append(f"| {arm} | {case['gptp_hart']} | {case['loads'][0]:.6f} | {case['loads'][1]:.6f} |")
lines+=['', 'The transferred charge is 0.0042 for both gPTP ports together, applied to each hart in turn. The #884 placement rule requires the 64x64 measured worst-pass comparison and load no greater than 0.70 on the selected hart. No placement decision is inferred from a 32x32 result alone.', '', 'Largest demand-model terms (fraction of one hart):', '']
for arm,a in analyses.items():
 for h in (0,1):lines.append(f'- {arm}, H{h}: '+', '.join(f'{k} {v:.6f}' for k,v in a['top_terms'][h][:6])+'.')
lines+=['', '## Cost samples and unmeasured terms', '',
'Inclusive completed-call shares below divide total completed-call cycles by total simulated CPU cycles across the nine groups. Nested calls overlap and must not be summed as occupancy. Unfinished calls and tail-call paths are not complete samples.', '']
for arm,a in analyses.items():
 for h in (0,1):lines.append(f'- {arm}, H{h} inclusive top calls: '+', '.join(f'{k} {100*v:.2f}%' for k,v in a['inclusive_function_fractions'][h][:6])+'.')
lines+=['', 'MAAP’s poll refreshes demand by walking sources. The declaring bitmap-clearing loop has no demand bits in this Arm A invalid-destination fixture. ACMP bitmap scans are not separately attributed. These samples do not establish a Zbb benefit; Zbb stays off.', '', '| Term | D$0 us / provenance | D$8 us / provenance |', '|---|---|---|']
for key in sorted(analyses['32-d0']['costs']):
 vals=[f"{a['costs'][key]} / {a['provenance'][key]['kind']}" for a in analyses.values()]
 lines.append('| '+key+' | '+' | '.join(vals)+' |')
lines+=['', 'Every transferred model cost is marked in the table. The historical centisecond entry is replaced in the final per-hart tick term by measured dispatch maxima: H0/H1 180/5 us without D$ and 150/5 us with 8 KiB D$, each plus the transferred 45 us event overhead. Additional unmeasured assumptions and rates:', '']
for key,value in analyses['32-d0']['external_terms'].items():lines.append(f'- {key}: {value}.')
lines+=['', 'The JSON receipts retain every sampled function’s count, sum, maximum, unfinished count and source group, plus each modeled cost’s exact provenance. This analysis does not alter repository cost statements or test floors.', '',
'## Memory, controls and outstanding checks', '',
'At 32x32 both cache arms require 179804 bytes ROM, 169104 bytes hart-0 SRAM and 153760 bytes hart-1 private RAM. The latter stays at the ruled power-of-two allocation of 262144 bytes, leaving 108384 bytes padding. Firmware memories plus the cross-hart RAM account for 150.5 RAMB36-equivalent tiles; cores, caches, peripheral and datapath memories are excluded. No route or fit is claimed. The largest objects are the hart-0 arena (144832 bytes), hart-1 maps (67584) and hart-1 values (41465).', '',
'The dedicated scale suite passes 21/21, including second-core removal from recorded build identities at both scale points and rejection of missing hart-1 execution observations. Second-hart unit checks pass 26/26. The observer passes its clean control and catches removed return observations. Actual completed 32x32 SRP traces also pass clean and fail after deleting hart-1 observations in both cache arms: four checks, zero failures. This last plant removes observations, not a physical core.', '',
'The full harness self-test is NOT accepted: rc 1, one failing baseline check containing six imported scale-model conflicts. The mutation campaign is not run on that failed baseline. The old shape model caps slices at 1600 us while the imported scale ports state 1935 us; its retained build-both cost is 10810 us against two 1935-us build-one costs; its built-point and poll tables omit scale points. No guard is relaxed. The composed lane also fails the unchanged Python style ratchet. These open failures are separate from the completed #966 local gates.', '',
'## 64x64 and stop condition', '', build64['detail'], '',
'No REBOOT implementation was made: item 2 did not complete its acceptance conditions. The requested acceptance-time filter ownership exception remains for a later authorized continuation.', '',
'## Reproduction and receipts', '',
'Exact launch arguments, heads, return codes and durations are in `receipts/scale/*.log.json`. The original native logs and models remain under `/data-2/milan/tmp/opt-a837/scale`; compact grades retain their raw-log hashes. `receipts/reproduce/scale_analysis.py` and `scale_strict_grades.py` generate the cost and strict-grade receipts. The original 32x32 manifests require the supplemental header evidence described above; they are not rewritten for reuse. `receipts/INDEX.md` indexes plain-text receipts smaller than 200 KB, with no compressed files.', '',
'No push, PR edit, board access or route occurred. The single results-only [A837] REPORT on #872 is recorded in PUBLICATION.md once posted.']
(OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
print('Wrote',OUT/'REPORT.md')
