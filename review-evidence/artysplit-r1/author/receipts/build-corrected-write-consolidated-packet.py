"""Write the current report from immutable qualification and image receipts."""
import datetime,hashlib,json
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4')
def read(path):return json.loads(path.read_text())
q=read(r/'final-census/qualification.json');src=read(r/'qualified-source.json')
assert q['status']=='PASS' and q['groups']==145
head=src['head'];image=read(r/'image-ready.json') if (r/'image-ready.json').exists() else None
for name in ('REPORT.md','PR-BODY.md'):
 backup=r/(name.replace('.md','')+'-before-consolidation.log')
 if not backup.exists():backup.write_bytes((p/name).read_bytes())
status='IMAGE READY' if image else 'IN PROGRESS: qualified source committed; three implementation attempts running'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
owner='''| Bound | Qualified result | Limit |
|---|---:|---:|
| Long-window load | 0.49667711403508774 | 0.70 |
| Long transmit, txL | 48.74 ms | 49 ms |
| Maximum measured whole pass, THE SHARE | 1.6813375 ms (134507 cycles) | 2 ms |
| Last queued notice | 121.84 ms | 140 ms |
| ACMP | 28.82 ms | 30 ms |'''
ledger='''| Held-egress row | Original measurement, ms | Ledger, ms |
|---|---:|---:|
| backlog.owed.if0 | 62.79239 | 62.94 |
| backlog.owed_behind0.if0 | 62.92862 | 63.08 |
| backlog.owed_behind1.if0 | 63.06490 | 63.22 |
| backlog.owed_behind2.if0 | 63.19966 | 63.36 |
| backlog.owed_behind3.if0 | 63.33355 | 63.51 |
| backlog-owed.service.acmp.last.if0 | 62.10374 | 62.21 |
| backlog-owed.service.aecp.last.if0 | 61.88720 | 61.99 |'''
route='Three attempts are running. No routed result or qualified flash pair is claimed yet.'
inputs='Pending route qualification.'
route_short='Three implementation attempts and offline input checks remain pending.'
if image:
 assert image['head']==head and image['status']=='PASS'
 graded=read(r/'images/graded-images.json')
 lines=['| Directive | Result | Worst WNS, ns | Worst WHS, ns |', '|---|---|---:|---:|']
 for row in graded['candidates']:
  timings=[x['timing'] for x in row['corners'] if x['timing']]
  lines.append(f"| {row['directive']} | {row['status']} | {min(x['wns'] for x in timings):.3f} | {min(x['whs'] for x in timings):.3f} |")
 route='\n'.join(lines)+f"\n\nSelected: **{image['directive']}**, best worst-corner WNS among the qualifying attempts.\n\n"
 route+='| Signoff report | WNS, ns | WHS, ns | Failing setup / hold endpoints |\n|---|---:|---:|---:|\n'
 for row in image['corners']:
  t=row['timing'];route+=f"| {row['corner']} / {row['junction_c']} C | {t['wns']:.3f} | {t['whs']:.3f} | {t['failing_endpoints']} / {t['failing_hold_endpoints']} |\n"
 u=image['utilization']
 route+=f"\nSelected attempt's post-placement utilization report: {u['Slice LUTs']:g} LUTs, {u['Slice Registers']:g} FFs, {u['Block RAM Tile']:g} BRAM tiles and {u['Slice']:g} occupied slices."
 route+='\n\nAll four reports meet WNS >= +0.030 ns and WHS >= 0, with zero failing setup and hold endpoints. Slow/Fast are the fixed speed models; the 0/85 C endpoint temperatures are power metadata, not four independent PVT timing models.'
 lines=['| Input | Bytes | SHA256 |','|---|---:|---|']
 for name,a in image['artifacts'].items():
  rel=Path(a['path']).relative_to(p)
  lines.append(f"| [{name}]({rel}) | {a['bytes']} | `{a['sha256']}` |")
 inputs='\n'.join(lines)
 inputs+='\n\nThe durable deploy inputs are `image/gateware/digilent_arty.bit`, `image/flashboot_layout.json` and the matched `image/image_manifest.json`; the packet also preserves AEM inputs, the exact ELF, CSR maps and generated gateware. The manifest and layout retain their original bytes. Image identity and `deploy.sh check-images` pass before and after copying. Only offline input checks ran; no flash-pair programming command ran. The bitstream hash above is the SHA256 of the complete `.bit` file, distinct from any payload hash in the manifest.'
 route_short=f"All three directives completed; {image['directive']} is selected at worst WNS {image['worst_wns_ns']:.3f} ns and WHS {image['worst_whs_ns']:.3f} ns. All four reports meet the floor, and copied deployment inputs pass offline identity checks."
report=f'''Status: {status}.
Updated: {now}. {'ETA: complete for the author image handoff; manager bench and independent review remain pending.' if image else 'ETA: approximately 2–4 hours from 2026-11-24 19:00 UTC, subject to shared-host and route-slot contention.'}

[A829] #878, round 4. Branch `pf-arty-split-1` -> `dev-soft-core`.
Local head: `{head}`. Base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`.
The branch has not been pushed. No hardware was accessed.

## Implementation and authority

The option-1 entity remains one interface, one AAF talker, one AAF listener and one CRF input: FPGA shape `(1,1,2)`. The system bus and CPU run at exactly 80,000,000 Hz; the VCO is 800 MHz, datapath 50 MHz and exact-divider margin zero. Output divisors are 10/32/16/4 for 80/25/50/200 MHz. The Arty configs, launch recipe and documentation agree. The round-1 port and missing split boot, region, timestamp-correction and console support are included. Writable corrections remain configuration-gated and reset to 1409/100 ns.

The authoritative owner decisions are [option 1](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), and [held-egress ledger](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930). They were rechecked before the local commit. Normative references include Milan v1.2 7.2.2/7.2.3 for the entity and 4.2.1 incorporating IEEE 802.1BA-2011 Table 6-1 and 6.5 for Ethernet modes. The MII initializer advertises only 100BASE-TX full duplex. No Linux scheduler row is added; #983 owns that separate host entry.

## Complete 80 MHz service qualification

All 145 native cases across eight firmware variants pass final qualification. All thirteen final command checks and all six qualification checks pass: owner model, SHARE, record classes, retry costs, transmit costs and held-egress ledger. Qualification SHA256: `{hashlib.sha256((r/'final-census/qualification.json').read_bytes()).hexdigest()}`. Frozen firmware source digest: `{src['firmware_tree']}`. The only post-campaign source edits were the three final documentation updates; all eleven documentation gates then passed.

{owner}

The existing rules derive a 950 us slice, 9 ms pace, 125 ms queued-notice bound and 30 ms ordinary-transmit statement. Costs use the Arty's own measured cycles at 80 MHz, plus 5 percent rounded upward to 5 us. No AX7101 cost or 100 MHz conversion supplies this point. Both-MRPDU build is 1035 us, one-MRPDU build 660 us, aged SRP step 1060 us, centisecond work 150 us and SRP record 300 us. Since 1035 us exceeds the slice, the existing scheduler builds one MRPDU per pass. Retry cold/attempt/notice statements are 125/30/230 us, from 9285/1947/17196 cycles. Transmit notice/response/long-response statements are 205/45/380 us. The derived ordinary transmit row is 29.96 ms. The four pre-existing shape blocks and all existing cost-table rows remain byte-identical.

### Seven authorized held-egress rows

These remain misses against their original 20 ms service budgets. The owner permits only their recorded extent. Each unchanged Arty ledger is `HOLD_MS + 1.05 * measured service`, with HOLD_MS = 60 and rounding upward to 0.01 ms. A new or larger miss fails. Complete fresh qualification introduces neither. The ledger self-test catches all eighteen plants, including all seven Arty entries and an overrun by one cycle.

{ledger}

## Firmware memory ledger

A new Arty ledger was added in `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15. ELF: 159532 bytes, SHA256 `b81f300e205f1067170458898b8b62f8407ecdb46bd38467e540efb89b9e84e5`. Sections: text 112748, rodata 11558, data 100, bss 45072 and stack 8192 bytes. ROM live extent is 124412 bytes; SRAM including stack is 53392 bytes. ROM allocation is 30.5 RAMB36 equivalents and SRAM 13.5, totaling **44 against 56**. The linked size receipt contains the bank decomposition. This firmware allocation is separate from the routed design's total BRAM use.

## Routed implementation

The three prescribed directives run through the management slot wrapper, at most two concurrently and only with MemAvailable >=20 GB. The source commit and exact firmware hash are fixed in `images/inputs.json`.

{route}

## Deployment inputs

{inputs}

## Verification and reproducibility

The [receipt index](receipts/INDEX.md) maps compressed logs, command records and hashes. The final active-phase receipts have the `build-corrected-` prefix; earlier calibration receipts retain their original phase and are not promoted to final qualification.

| Verification | Result and primary receipt |
|---|---|
| Four firmware shards, including Arty host/RV32 cases | PASS; `build-corrected-final-firmware-results.json.gz` and per-shard command/log receipts |
| Complete service campaign and cost census | PASS, 145 cases / eight variants; `build-corrected-final-census-qualification.json.gz` |
| Service grader controls | PASS, 297 mutants caught; `build-corrected-final-service-selftest.log.gz` |
| Arty boot and fault controls | PASS; six native controls, six plants and eight placement controls; `build-corrected-final-boot-controls-fixedseed.log.gz` |
| Arty region decode | PASS, positive and both original mutants with exact expected findings; `region-commit-result.json.gz`; two wrong-clock controls in `region-clock-controls.json.gz` |
| MII mode policy | PASS, eight host cases and seven plants; `mii-campaign.log.gz`, plus complete firmware shard evidence |
| Writable timestamp corrections | PASS, 237 integration checks; `milan-dp-latw-rerun.log.gz` |
| Timestamp return and shadow behavior | PASS, 17 timestamp and nine shadow plants; `gptp-txts.log.gz`, `gptp-shadow-mutants-rerun.log.gz`; fixture restoration verified |
| PLL exact-divider contract | PASS, required clocks/VCO and three controls; `pll-contract.log.gz` |
| AX7101 identity | PASS, 42 generated/product and thirteen controlled raw SoC-export comparisons; `build-corrected-identity-final-compare.json.gz`, `build-corrected-identity-final-export-compare.json.gz` |
| Existing scheduler rows | PASS, exact existing source bytes; `build-corrected-old-row-final.json.gz` |
| Builder checks | Every executed consolidated gate passes with RV32/elaboration enabled; historical area calibration is SKIP because its external reference report is absent; `builder-consolidated-receipt.json.gz` |
| RTL lint / front end | PASS, 89/89 lint ratchet and nineteen documented waivers, zero front-end findings; `rtl-lint.log.gz`, `xvlog-gate.log.gz` |
| Final documentation | PASS, eleven gates after measured prose; `build-corrected-docs-after-service-results.json.gz` |

Core commands, each run from the candidate checkout with an owned build directory:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --self-test --require-rv32 --shard N/4 --jobs 1 --build-dir <scratch>/firmware-N
python3 tb/verilator/ctrl_service_budget/selftest.py
PYTHONHASHSEED=0 python3 tb/verilator/ctrl_split_boot/run.py --shape endstation_arty_split --interfaces 1 --build-dir <scratch>/boot
PYTHONHASHSEED=0 python3 tb/verilator/ctrl_split_boot/run.py --shape endstation_arty_split --interfaces 1 --self-test --build-dir <scratch>/boot-controls
PYTHONHASHSEED=0 python3 tb/verilator/ctrl_region_decode/run.py --shape endstation_arty_split --self-test --build-dir <scratch>/region
```

N runs over 0, 1, 2, 3, with no more than four concurrent harness legs. The archived `run-final-census.py`, `run-pipeline.py`, `qualification-launch.json`, per-image `build.json`, native manifest and thirteen qualification command records specify the full 145-case enumeration, variants, exact traces and cost derivation. Documentation commands are listed individually in their results receipt. Route command records preserve the complete environment, slot wrapper and directive argv. Reproduction must supply the repository's documented dependencies and an owned scratch directory.

## Identity scope and execution notes

Both AX7101 full firmware ELFs remain byte-identical: 1x1/1if `f5a6b98df27667ce6d7998327051e42a533139374faaabb00f0b13fe42e6ca74`; 8x8/1if `0add4cbd25ffc66df02b4410cc6c125d791a9d618d978c9b8034d8c7655878d7`. The controlled raw SoC comparison uses equal timestamp/hash-seed inputs and deterministic instance names in hierarchy comments. AX bitstreams were not rebuilt. The baseline's three commits above dev-soft-core affect documentation only; the ancestry receipt records that scope.

Calibration found understated SRP and two-MRPDU costs. Their statements were corrected by the existing measurement rule, then firmware, boot, product and all 145 service cases were rerun on the frozen final source. No owner bound was waived. Earlier failures, interrupted exploratory traces and provisional images remain separately labeled in the receipts. The unseeded boot export refusal was resolved by pinning PYTHONHASHSEED=0 without weakening byte comparison. Region observations were updated for the shipping system-clock CPU and data cache, with both original mutants and wrong-clock controls retained.

An early exploratory bootstrap briefly admitted a fifth native leg. It was terminated, excluded and rerun within the four-leg limit; `concurrency-correction.json.gz` records this deviation. The final campaign uses four shared slots. Scratch stays below 30 GB; only generated precompiled headers from closed attempts were reclaimed, with pre-removal hash inventories. Source, executables, traces and receipts were retained. No other existing checkout was modified.

The author image handoff does not claim independent review, hosted gates, the full merge bar or hardware qualification. The manager runs the bench after IMAGE READY. Internal/external review assignment, candidate-merge validation, merge and Issue completion remain pending. No push, flash, JTAG, console or bench operation was performed.
'''
(p/'REPORT.md').write_text(report)
pr=f'''[A829]

## Description

The Arty split image now retains its required one AAF talker, one AAF listener and one CRF input at exactly 80 MHz sys/CPU and 50 MHz datapath. Its `(1,1,2)` FPGA scheduler point uses independently measured costs, a 950 us slice and 9 ms pace. All five owner bounds pass across the complete 145-case campaign: load 0.4966771140, txL 48.74 ms, maximum pass 1.6813375 ms, last notice 121.84 ms and ACMP 28.82 ms.

MII advertises only 100BASE-TX full duplex under Milan v1.2 4.2.1 and IEEE 802.1BA-2011 Table 6-1 and 6.5. The port includes split boot/region support and configuration-gated writable timestamp corrections. Seven held-egress misses retain their authorized, independently measured 80 MHz ledger; a new or larger miss still fails. Existing scheduler rows and AX7101 generated/product artifacts remain byte-identical. No Linux scheduling entry is added.

The new Arty firmware ledger records a 159532-byte ELF and 44/56 RAMB36 equivalents. {route_short}

## Linked Issue / roles

Closes #878
Relates to #665, #818, #829, #894, #983

Target: `pf-arty-split-1` -> `dev-soft-core`.
Executor: `[A829]`.
Internal cleared-context reviewer: pending assignment.
External reviewer: pending assignment.

## Authoritative references

- [Issue #878 and its three owner rulings](https://github.com/kebag-logic/milan-fpga/issues/878).
- Milan v1.2 7.2.2/7.2.3 and 4.2.1; IEEE 802.1BA-2011 Table 6-1 and 6.5.
- `ctrl_loop.h`, THE SHAPES and THE SHARE; `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15.
- `docs/AAF_LATENCY_TAPS.md`, `docs/litex/CLOCK_DOMAINS.md`, `docs/integration/BUILDING.md`.

## How to get into the same state

Local commit `{head}` on base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. The branch has not been pushed. The round-4 report and receipt index contain exact source, firmware, trace and deployment-input hashes and reproducible command records.

## Validation

- Four complete firmware shards, including Arty host and RV32 cases: PASS.
- All 145 service cases across eight variants, complete cost census and all six qualification checks: PASS; 297 grader mutants caught.
- Arty boot, six native controls, six planted defects and eight placement controls: PASS.
- Region decode and both original mutants, plus wrong-clock controls: PASS.
- MII policy: eight host cases and seven planted defects pass.
- Writable timestamp integration: 237 checks pass; seventeen timestamp and nine shadow defects caught.
- Exact clocks and VCO, existing scheduler-row identity, 42 AX generated/product and thirteen raw SoC-export comparisons: PASS.
- Builder checks, RTL lint, front-end checks and eleven final documentation gates: PASS for executed checks; historical area calibration skipped for its absent external reference.

## Limitations and remaining work

The seven held-egress rows remain recorded misses against 20 ms; their ledger is not a normative wait allowance. AX identity covers generated artifacts, full firmware images and controlled SoC exports; AX bitstreams were not rebuilt. The manager performs the bench after IMAGE READY. Independent reviews, hosted checks and candidate-merge validation remain pending. No push or hardware operation occurred.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including the manager's bench work
- [x] Changed behavior has self-checking tests
- [ ] Full required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] Changed contracts and the Arty memory ledger are documented
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [ ] Post-merge containment is checked before the Issue moves to Done
'''
(p/'PR-BODY.md').write_text(pr)
(r/'packet-consolidation.json').write_text(json.dumps(dict(time=now,status=status,head=head,image=bool(image)),indent=2)+'\n')
print(status)
