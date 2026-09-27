[A358] REVIEW READY

Commit: `7f997b60d5a74d46beca5c263d27496ccce0ae4f` on `397-service-budget`, parent `ac18b50968b12efe4d15c0a06301264b35656b31`. Local commit only; no push or PR action.

Changed: sibling product-CPU measurement under `tb/verilator/fw_service_budget/`; per-duty tables and complete raw-log/hash receipts under `docs/findings/397_SERVICE_BUDGET*`; findings index and testing-map entries. Firmware, RTL, submodules, normative requirements and `tb/verilator/nvm_capture_cpu` remain unchanged.

This completes the author deliverable in the [measurement-only re-scope](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854787465), not the full issue. **The 8x8 scenario exceeds the 500 ms service-window comparison for two NVM-status commands and the required maximum heartbeat period. These remain findings, not timing approval.** The hart decision belongs to the manager. Refs #397; bench items remain open. Reviewers remain [R348] and [R349].

The CPU runs at 50 MHz and the system at 100 MHz. Cycles below are elapsed CPU clock units, rounded upward from integer system cycles; milliseconds use the unrounded counter. These are maxima over the recorded fixed-phase scenarios, not a global worst-case proof. Each shape completes one populated-media cold boot, all 17 UART cases spanning all five product registrations, two acknowledged commits and four erases. The 1x1 run programs 26 pages / 6,528 bytes; 8x8 programs 100 pages / 25,360 bytes. Restore contains 8 and 32 matching backend read/response handshakes with no errors.

**1x1: populated A/B slots, 0 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 15,548,512 | 310.97023 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 15,548,512 | 310.97023 | N/A | N/A |
| Binding restore walk | 1,138 | 0.02276 | 3,000 | 2999.97724 |
| Journal erase envelope | 1,006,829 | 20.13657 | 3,500 | 3479.86343 |
| Journal START-to-ACK | 7,826,455 | 156.52910 | 8,000 | 7843.47090 |
| Maximum heartbeat gap | 21,531,153 | 430.62305 | 500 | 69.37695 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 115,696 | 2.31391 | 500 | 497.68609 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 10,425,165 | 208.50329 | 500 | 291.49671 |
| `milan_nvm commit` | 13,738,559 | 274.77117 | 8,000 | 7725.22883 |
| `milan_nvm wipe`, whole command | 2,017,180 | 40.34359 | N/A | N/A |
| Wipe erase envelope, maximum of two | 1,005,511 | 20.11022 | 3,500 | 3479.88978 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |

**8x8: populated A/B slots, 1 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 51,571,981 | 1031.43961 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 51,571,981 | 1031.43961 | N/A | N/A |
| Binding restore walk | 2,700 | 0.05400 | 3,000 | 2999.94600 |
| Journal erase envelope | 3,775,572 | 75.51143 | 3,500 | 3424.48857 |
| Journal START-to-ACK | 32,909,891 | 658.19782 | 8,000 | 7341.80218 |
| Maximum heartbeat gap | 72,488,882 | 1449.77764 | 500 | -949.77764 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 116,268 | 2.32535 | 500 | 497.67465 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 39,443,853 | 788.87705 | 500 | -288.87705 |
| `milan_nvm commit` | 55,457,868 | 1109.15735 | 8,000 | 6890.84265 |
| `milan_nvm wipe`, whole command | 7,554,712 | 151.09423 | N/A | N/A |
| Wipe erase envelope, maximum of two | 3,774,257 | 75.48514 | 3,500 | 3424.51486 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |


The ordinary-command 500 ms comparison comes from the writer heartbeat period, not a UART protocol deadline. Restore uses its 3,000 ms polling limit. Erase envelopes include verification and nearby service and are compared with 3,500 ms. Journal START-to-ACK uses the existing 8,000 ms deadline; the full console command also includes preceding capture/prefill. Wipe has two erase limits and no single 8,000 ms timer. AEM copy/CRC is bounded by the enclosing boot interval. Milan v1.2 section 5.6.3 fixes ADP validity and advertisement period, not a numeric power-on-to-enable deadline, so boot/AEM margins are not invented. Page-program activity is enclosed by the journal bracket; no isolated margin against its 50 ms polling limit is claimed. AECP response timing remains in the fabric under NFR-SCOUT-03.

CPU-side service below is measured elapsed time minus configured flash WIP, still including bus/DDR stalls, serial transfers and verification. The CPU polls during WIP; subtraction does not measure spare CPU capacity. Saved-state section 9.4 supplies 3,000 ms per erase and 5 ms per page program.

| Shape / operation | Measured service (ms) | Modeled WIP (ms) | Device maxima (ms) | Conditional total (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1x1 journal START-to-ACK | 156.52910 | 0 | 3,065 | 3221.52910 |
| 1x1 whole console commit | 274.77117 | 0 | 3,065 | 3339.77117 |
| 1x1 journal erase envelope | 20.13657 | 0 | 3,000 | 3020.13657 |
| 1x1 whole wipe | 40.34359 | 0 | 6,000 | 6040.34359 |
| 8x8 journal START-to-ACK | 607.19782 | 51 | 3,250 | 3857.19782 |
| 8x8 whole console commit | 1058.15735 | 51 | 3,250 | 4308.15735 |
| 8x8 journal erase envelope | 74.51143 | 1 | 3,000 | 3074.51143 |
| 8x8 whole wipe | 149.09423 | 2 | 6,000 | 6149.09423 |


These device-limit totals are conditional projections, not measured worst-device runs or proof of the required twofold commit margin. More WIP polling and arbitrary bus contention are not bounded. Physical SPI is replaced at the device stream boundary; DDR uses the existing simulation model; external packet traffic is absent. UART has immediate byte handshakes, with separate 115,200-baud allowances retained per command (maximum 33.07292 ms). BIOS CRC/delay/memory-test exclusions are inherited from the capture recipe. Restore covers the present binding walk, not the seven remaining saved-state items. Future update writing, fault logging, PHY management and temperature logging are unmeasured. The architecture decision and physical liveness torture remain open.

Validation: all final commands ran in the foreground, without pipelines, from `$LANES/397-service-budget`; all final rc 0.

- `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/397-a358-1x1 --reuse-build --populated`: all 17 commands completed; zero measured budget findings.
- `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/397-a358-8x8 --reuse-build --populated --device-wait-us 1000 --record-budget-findings`: all 17 commands completed; overruns retained explicitly. Final bound-log `--regrade` runs pass for both shapes; 8x8 has three named findings including heartbeat. No native product input changed between execution and final analysis.
- `python3 -B tb/verilator/fw_service_budget/run.py --self-test`: 14 device controls and eight oracle controls, zero failures. An exact-budget interval passes; one extra system cycle is caught. Delaying the recorded final UART response must trigger that command's budget refusal; a heartbeat refusal alone is insufficient.
- `python3 -B scripts/check_nvm_capture.py`: unchanged pinned harness, existing receipt and all seven controls pass.
- `python3 -B scripts/check_feature_status.py --self-test`: 46/46 controls, zero findings.
- `python3 -B scripts/docs_check.py`: zero findings, scrub 23/23 and routing 4/4.
- `python3 -B scripts/check_doc_paths.py`, `python3 -B scripts/check_doc_style.py`, `python3 -B scripts/check_archive.py`, `python3 -B scripts/gen_toc.py --check`: pass, using the existing pinned Markdown environment where required.
- `python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31`: exact committed head, zero findings, 339/339 controls.
- `python3 -B scripts/check_py_idiom.py`, `python3 -B scripts/check_cpp_idiom.py`, `python3 -B scripts/check_hygiene.py --check`, `python3 -B scripts/measure_test_evidence.py --check`: existing ratchets pass, none changed.
- `git diff HEAD --check` before commit and `git diff --check` after commit: pass; final worktree clean.

The default harness rejects budget overruns after preserving their receipt. The explicit measurement-only reporting option retains and prints every refusal while requiring valid marker, command, build and device evidence. Its successful result is measurement integrity, not a pass for the missed budgets. Both committed receipts reproduce their analysis from raw logs and bind to the current input hashes. CPU netlist and unchanged firmware digests match the documented capture/product identities.

Acceptance: external/enclosing markers, unchanged firmware/capture harness, both measurement tables, device-wait separation and planted-over-budget detection are delivered. No duty triggered the re-scope's STOP condition. Open risks/questions: the measured 8x8 misses; unbounded physical/bus worst cases; future duties; manager architecture disposition; independent review and bench proof. No approval or full-issue completion is claimed.
