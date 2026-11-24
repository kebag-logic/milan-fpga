STATUS: STOP — 64x64 two-hart firmware does not build. Item 1 is REVIEW READY; both 32x32 nine-group measurements and the single public report are complete (2026-11-24 12:49 CET). ETA: none; this round has ended.

# [A837] optimisation line, round 1

Authority: manager ruling on #872, issuecomment-7124686692, and owner instruction 2026-11-24. The user explicitly requires reporting 32x32 and stopping if 64x64 does not build. No REBOOT work, memory-limit change, route or hardware access followed the failed build.

## PR 966 — locally ready for independent review

Repair head: `44c566399002db32bf8a6ad3ce719488d418bcb0`; branch `884-gptp-firmware` in `/data-2/milan/lanes/opt-gptp-sw`. Starting head: `165476c755e4728a044c12ea6bc33ce0a0a9d28f`. Five local commits, tests/test plumbing/records/docs only; no product C or RTL changed. No push or PR edit. The manager controls pushing and review.

Item 1: coverage check passes at 7ad1e7df55, rc 0 in 712 s; earlier checks at 17bd60c698 and ee9b42b103 also pass. aecp_face 229/229 lines and 204/204 branches; mbx 384/384 and 202/202; gptp.c 665/704 and 346/437; gptp.h 2/2. No floor lowered. The final README prose correction states the gPTP floor accurately; the 21 parsed exclusions and ratchet figures remain identical to the measured head. The stale platform gate exclusion is removed.
All four firmware shards pass with --require-rv32 --self-test; shard 1 catches all 828 of 828 control mutants. AECP catches all 387 defects, including both new face defects. The control table has 828 entries. Its two new driver entries were extracted into gptp_driver_mutants.py to keep the parent within its 1000-line limit; serialization proves all entries and order identical.
The cancelled-job checks exposed missing gPTP test-build plumbing: the simulation ignored STACK_DIR, lacked the pin prerequisite, and was absent from the boundary builder registry. The two gPTP defect campaigns also lacked their suite classification. All are now registered or wired as appropriate; no product C or RTL changed. The pin-control count rises to 199, including the simulation's 11 new checks. The Verilator boundary leg passes: 1181 compiled sources, 0 findings, 6 boundary + 199 pin + 4 figure controls, 0 misbehaved. The non-Verilator leg also passes: 3863 compiled sources, 0 findings, 112 boundary + 199 pin + 4 figure controls, 0 misbehaved.
Coverage/tally/RV32 controls, lint, conformance, CDC, all five Yosys fast steps, offline runner controls and the gPTP modelled-peer baseline pass. The gPTP simulation defect campaign passes all 14 planted defects, 0 failures. The full builder gate passes rc 0 with two explicitly uncovered arms (make mutation inert on this make; historical calibration report absent). All docs substantive steps now have a passing result: the Python module-length replay passes at 7ad1e7df. The publication census passes. LiteX passes 8/8: the initial timing-cut timeout (rc 92) is retained and its foreground replay passes rc 0 in 1269 s with a 7200 s limit.


The complete updated PR body is `966/PR-BODY.md`; exact commands, heads, evidence relationships and limitations are in `966/REVIEW-READY.md`. These are author evidence, not an approval. Hosted evidence on the new local head is not claimed.

## Two-hart scale — measured at 32x32, blocked at 64x64

Worktree `/data-2/milan/lanes/opt-hart2`, branch `opt-hart2-a837-r1`, source head `fe009fa2c7741b8612bdbc74fe70909d57931503`. It is based on the #966 repair and composes int4, A808 scale ports, probe fix `fcad6d10`, and lwSRP `0757869` with the 16-value cap. The accepted stack fold is `115df0be`.

The native models were built at `368c2d1e`; later changes affect docs/self-tests/input-manifest coverage. Their original recorded inputs and executable hashes match. `scale-input-equivalence.json` supplies the omitted observer-header hash and compiler dependency evidence without rewriting the original manifests. A new build records that header normally; a reuse attempt with the old manifest is correctly refused.

All nine Arm A groups completed in both configurations: srp, backlog-owed, backlog-adp-refill, control, adp-link, acmp-noresp, maap, aecp and acmp-notk. Both harts run at 100 MHz; hart 1 has 16 KiB I$.

| Hart 1 D$ | H0 worst ms | H1 worst ms | SHARE misses | Original / strict matrix rc |
|---|---:|---:|---:|---:|
| None | 0.83224 | 0.91832 | 0 | 1 / 1 |
| 8 KiB | 0.83225 | 0.78905 | 0 | 1 / 1 |

Each matrix has seven owed-backlog responses over the nominal 20 ms budget. The no-D$ MAAP grade has two periodic-opportunity findings; the cached grade has those plus join intervals 180.928 and 180.929 ms below 181.0. The periodic expiries predate interface-1 link-up, while the grader drops LINK values; that diagnostic does not waive the grades. No refusal or over-SHARE pass was observed. Record-mode backlog rc 0 retains its misses; strict rc is 1.

Demand-model loads, H0/H1 (estimates with explicit transferred and unstaged terms, not CPU occupancy):

| Hart 1 D$ | gPTP on H0 | gPTP on H1 |
|---|---|---|
| None | 0.599170 / 0.397682 | 0.594970 / 0.401882 |
| 8 KiB | 0.596170 / 0.390626 | 0.591970 / 0.394826 |

Both-port gPTP charge is 0.0042, transferred from its lane. No #884 placement decision is made without a 64x64 measured comparison. `REPORT.md` and the analysis receipts name every unmeasured term, sampled proxy, possible overlap and inherited rate. Early analyses that substituted unstaged retained/notice/probe costs are explicitly marked superseded; the completed analysis retains their historical costs.

Top observed inclusive call shares: H0 SRP poll about 27.9%; H1 MAAP poll 36.47% without D$ and 31.33% with 8 KiB. Nested spans overlap. MAAP refreshes demand by scanning sources; ACMP bitmap costs are not separately attributed and the declaring bitmap loop has no demand bits in this Arm A fixture. No measured Zbb benefit is claimed; it remains off.

One-hart ELF identity passes across the new observer/cache changes at the composed scale baseline: 196024 bytes, SHA-256 `2b05feba4c2c7ff44f0eda69dadf9dc882124b553ada835e7e93db9a0add1cc7`. This is not an identity claim across the earlier accepted fold and scale ports. The cache arms share one two-hart ELF.

Dedicated scale controls: 21/21; second-hart unit checks: 26/26; observer clean and planted-return controls: zero failures; actual SRP trace clean/removed-H1-observation controls: four checks, zero failures. The full self-test remains rc 1: one baseline check reports six imported shape-model conflicts; its mutation campaign is not run on a dirty baseline. Python style ratchet also remains red. These failures are not waived and are separate from #966's local gates.

32x32 unrouted firmware memory: ROM 179804 bytes, H0 SRAM 169104, H1 needed 153760 and allocated 262144 (108384 padding). Firmware plus cross-hart memory is 150.5 RAMB36 equivalents, excluding cores, caches and other memories. The power-of-two allocation remains unchanged.

64x64/2if two-hart build at `fe009fa2`: linker reports `.hart1.bss` does not fit `hram`, overflow **92064 bytes** against a 262144-byte region. The image builder returns 2 and foreground wrapper 1 in 6.781 s. There is no 64x64 executable, native measurement or load claim. The explicit STOP applies; no REBOOT change has started.

## Receipts and remaining handoff

`REPORT.md` holds the full measurement and open findings. `receipts/INDEX.md` indexes text receipts below 200 KB, no .gz; exact commands and launch heads are retained. Scratch `/data-2/milan/tmp/opt-a837` remains below 40 GB. Parallel foreground workers were used with available memory above 30 GB. The inspected native-shards runner launches detached sweep units, so the requested foreground runs used the harness worker pool instead.

No push, PR edit, board/test-machine access, route or review verdict. The single results-only [A837 report](https://github.com/kebag-logic/milan-fpga/issues/872#issuecomment-7130585273) is published and verified; its receipt is `PUBLICATION.md`. The manager may push/review #966 independently; the scale composition is not accepted because the full self-test and grades remain nonzero and 64x64 does not build.

STOP: 64x64 two-hart firmware overflows hart 1 RAM by 92064 bytes; report 32x32, no REBOOT work.
