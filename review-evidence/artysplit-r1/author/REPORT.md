Status: IMAGE READY.
Updated: 2026-11-24T19:24:39.946319+00:00. ETA: complete for the author image handoff; manager bench and independent review remain pending.

[A829] #878, round 4. Branch `pf-arty-split-1` -> `dev-soft-core`.
Local head: `248d85c1453213b0f1642967a4046f395c82c56b`. Base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`.
The branch has not been pushed. No hardware was accessed.

## Implementation and authority

The option-1 entity remains one interface, one AAF talker, one AAF listener and one CRF input: FPGA shape `(1,1,2)`. The system bus and CPU run at exactly 80,000,000 Hz; the VCO is 800 MHz, datapath 50 MHz and exact-divider margin zero. Output divisors are 10/32/16/4 for 80/25/50/200 MHz. The Arty configs, launch recipe and documentation agree. The round-1 port and missing split boot, region, timestamp-correction and console support are included. Writable corrections remain configuration-gated and reset to 1409/100 ns.

The authoritative owner decisions are [option 1](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), and [held-egress ledger](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930). They were rechecked before the local commit. Normative references include Milan v1.2 7.2.2/7.2.3 for the entity and 4.2.1 incorporating IEEE 802.1BA-2011 Table 6-1 and 6.5 for Ethernet modes. The MII initializer advertises only 100BASE-TX full duplex. No Linux scheduler row is added; #983 owns that separate host entry.

## Complete 80 MHz service qualification

All 145 native cases across eight firmware variants pass final qualification. All thirteen final command checks and all six qualification checks pass: owner model, SHARE, record classes, retry costs, transmit costs and held-egress ledger. Qualification SHA256: `f6f1d2f535a8de0ec2348dbb0998a152103f3583e9bf4cc72b0115552ef1886c`. Frozen firmware source digest: `7e5a1ae880340481da1ca0b8850e3f2a07e57b366405d2cbef2c358fa22eca63`. The only post-campaign source edits were the three final documentation updates; all eleven documentation gates then passed.

| Bound | Qualified result | Limit |
|---|---:|---:|
| Long-window load | 0.49667711403508774 | 0.70 |
| Long transmit, txL | 48.74 ms | 49 ms |
| Maximum measured whole pass, THE SHARE | 1.6813375 ms (134507 cycles) | 2 ms |
| Last queued notice | 121.84 ms | 140 ms |
| ACMP | 28.82 ms | 30 ms |

The existing rules derive a 950 us slice, 9 ms pace, 125 ms queued-notice bound and 30 ms ordinary-transmit statement. Costs use the Arty's own measured cycles at 80 MHz, plus 5 percent rounded upward to 5 us. No AX7101 cost or 100 MHz conversion supplies this point. Both-MRPDU build is 1035 us, one-MRPDU build 660 us, aged SRP step 1060 us, centisecond work 150 us and SRP record 300 us. Since 1035 us exceeds the slice, the existing scheduler builds one MRPDU per pass. Retry cold/attempt/notice statements are 125/30/230 us, from 9285/1947/17196 cycles. Transmit notice/response/long-response statements are 205/45/380 us. The derived ordinary transmit row is 29.96 ms. The four pre-existing shape blocks and all existing cost-table rows remain byte-identical.

### Seven authorized held-egress rows

These remain misses against their original 20 ms service budgets. The owner permits only their recorded extent. Each unchanged Arty ledger is `HOLD_MS + 1.05 * measured service`, with HOLD_MS = 60 and rounding upward to 0.01 ms. A new or larger miss fails. Complete fresh qualification introduces neither. The ledger self-test catches all eighteen plants, including all seven Arty entries and an overrun by one cycle.

| Held-egress row | Original measurement, ms | Ledger, ms |
|---|---:|---:|
| backlog.owed.if0 | 62.79239 | 62.94 |
| backlog.owed_behind0.if0 | 62.92862 | 63.08 |
| backlog.owed_behind1.if0 | 63.06490 | 63.22 |
| backlog.owed_behind2.if0 | 63.19966 | 63.36 |
| backlog.owed_behind3.if0 | 63.33355 | 63.51 |
| backlog-owed.service.acmp.last.if0 | 62.10374 | 62.21 |
| backlog-owed.service.aecp.last.if0 | 61.88720 | 61.99 |

## Firmware memory ledger

A new Arty ledger was added in `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15. ELF: 159532 bytes, SHA256 `b81f300e205f1067170458898b8b62f8407ecdb46bd38467e540efb89b9e84e5`. Sections: text 112748, rodata 11558, data 100, bss 45072 and stack 8192 bytes. ROM live extent is 124412 bytes; SRAM including stack is 53392 bytes. ROM allocation is 30.5 RAMB36 equivalents and SRAM 13.5, totaling **44 against 56**. The linked size receipt contains the bank decomposition. This firmware allocation is separate from the routed design's total BRAM use.

## Routed implementation

The three prescribed directives run through the management slot wrapper, at most two concurrently and only with MemAvailable >=20 GB. The source commit and exact firmware hash are fixed in `images/inputs.json`.

| Directive | Result | Worst WNS, ns | Worst WHS, ns |
|---|---|---:|---:|
| ExtraPostPlacementOpt | FAIL | 0.009 | 0.021 |
| AltSpreadLogic_high | PASS | 0.589 | 0.017 |
| ExtraTimingOpt | PASS | 0.617 | 0.017 |

Selected: **ExtraTimingOpt**, best worst-corner WNS among the qualifying attempts.

| Signoff report | WNS, ns | WHS, ns | Failing setup / hold endpoints |
|---|---:|---:|---:|
| Slow / 0 C | 0.617 | 0.102 | 0 / 0 |
| Slow / 85 C | 0.617 | 0.102 | 0 / 0 |
| Fast / 0 C | 1.613 | 0.017 | 0 / 0 |
| Fast / 85 C | 1.613 | 0.017 | 0 / 0 |

Selected attempt's post-placement utilization report: 33411 LUTs, 40479 FFs, 78.5 BRAM tiles and 14119 occupied slices.

All four reports meet WNS >= +0.030 ns and WHS >= 0, with zero failing setup and hold endpoints. Slow/Fast are the fixed speed models; the 0/85 C endpoint temperatures are power metadata, not four independent PVT timing models.

## Deployment inputs

| Input | Bytes | SHA256 |
|---|---:|---|
| [Bitstream](image/gateware/digilent_arty.bit) | 3281691 | `1046292da1e73b2b595f65c66d9c429fb183a43e3466e160d95024651014735c` |
| [flashboot_layout.json](image/flashboot_layout.json) | 1002 | `a096b7612353ce756440111ce4b89b0b241dd25ae3481e4d5ff0d16360f4b84f` |
| [Matched image_manifest.json](image/image_manifest.json) | 608 | `81ade1bd936f258d58921666e4b1c5508ca29392e35ed1ea46c20b6337de47f2` |
| [AEM image](image/aem_desc.bin) | 5952 | `019bced16c167794869a794af3b5389103b3665f5d4a45878ea2bdeaf55a9463` |
| [AEM manifest](image/aem_desc.json) | 261 | `e1dc362f1d4a087d13fb08e7eb3f30f8da17c22fd82078fc16ca2bb8646b5ad8` |
| [Firmware ELF](image/ctrl_app.elf) | 159532 | `b81f300e205f1067170458898b8b62f8407ecdb46bd38467e540efb89b9e84e5` |

The durable deploy inputs are `image/gateware/digilent_arty.bit`, `image/flashboot_layout.json` and the matched `image/image_manifest.json`; the packet also preserves AEM inputs, the exact ELF, CSR maps and generated gateware. The manifest and layout retain their original bytes. Image identity and `deploy.sh check-images` pass before and after copying. Only offline input checks ran; no flash-pair programming command ran. The bitstream hash above is the SHA256 of the complete `.bit` file, distinct from any payload hash in the manifest.

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
