[R686] POSITIVE - exact head c7e87c8c87494f3444000b46954648ba1a94dcb8

Independent external review R686-1 of issue #775 / PR #777. All five lenses are CLEAN. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION finding was identified in the reviewed delta. This is a source review verdict, not merge authorization or hardware acceptance.

Reviewed tree: `0b62e515c36a7c5c3781f7745c9a6f2a800878c2`. Base: `a032c6d6e3775f145349d5a495c1e1ad12294936`. The three commits are `0ee987f4`, `6ff2880a`, and `c7e87c8c`; the delta contains twelve files. The isolated source checkout was never edited.

Authority and reconstruction

The review started from AGENTS.md, CONTRIBUTING.md and docs/README.md, then [issue #775](https://github.com/kebag-logic/milan-fpga/issues/775) and its [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/775#issuecomment-6379902989), REQUIREMENTS.md, FR-STR-03, the architecture and listener interfaces, then the diff and history. [PR #769](https://github.com/kebag-logic/milan-fpga/pull/769) explains the preceding format discard. The controlling public ruling interprets Milan v1.2 Table 5.6 and 4.4.2.2: an off-format received PDU advances sequence state, counts only UNSUPPORTED_FORMAT, and presents nothing. A gap or repeat on the rejected PDU itself therefore counts nothing; a subsequent accepted PDU is compared with that rejected PDU's sequence. This review applies that recorded ruling; it does not claim a new independent reading of an external standards archive.

The [public receipt tree](https://github.com/kebag-logic/milan-fpga/tree/976fb2d33b358f41bbff082a69f76fba6b749a77/review-evidence/775-r1) was inspected after the independent source pass. Only public receipt material was read. No other review report or private author material informed this verdict or ledger.

[R686] PASS Conformance - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1010`, `hdl/ieee1722/crf/KL_crf_rx.sv:598`, `docs/reference/FR_NFR.md:271` - both rejected paths implement the frozen sequence rule. AAF replaces prev_seq with the received byte; CRF computes the next expected byte modulo 256. Both retain the format-only anomaly event gate. The next in-order accepted PDU produces no mismatch, and a real gap still counts. Independent clean, base-RTL and planted-defect executions establish the distinction.

[R686] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:281`, `:638`, `:718`, `:1010`, `:1061`; `KL_crf_rx.sv:399`, `:598`; `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:987` - the new state fits the existing four-bit enum. It writes exactly word 8 using the existing engine-priority RAM port, then returns to idle. `{ram_q_r[31:8], cur_w.seq}` preserves lock, settle, wire channels, mr seed/reference and reserved upper bits. No accepted verdict, timestamp-word walk, accepted counter event, silence refresh or channel shadow update is introduced. The current bundle and stream index stay stable through the added cycle. The reference receives the corresponding timing/state edit. CRF changes only exp_seq_r within the existing reject branch; have_seq_r remains untouched, and existing settle-reset and timeout rules remain intact. No clock, reset, crossing, port, parameter or register-layout change occurs. The one added reject service cycle remains shorter than the accepted walk. N=1/N=8 lockstep reset, queue and read-modify-write regressions pass.

[R686] PASS Robustness - `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1000`, `tb/verilator/crf_rx/sim_main.cpp:1624`, `sim_discontinuity.cpp:130`, plus `probes/aaf_wrap_state.run.log`, `probes/crf_wrap.run.log` - examined late/early rejected PDUs carrying mr and tu, a real gap after a reject, first-PDU rejection, bind/reset ordering, stream isolation, sequence wrapping, and unchanged timeout behavior. The AAF extension places the reject at sequence 255, then accepts 0, and directly checks all upper MON_STATE bits, LAST_TS and stream 0's state. The CRF extension also places the rejection at 255. Both pass. The first rejected CRF PDU still cannot seed an era. Existing discontinuity and lockstep regressions pass. This is focused coverage, not an exhaustive proof of every event coincidence.

[R686] PASS Tests - `tb/verilator/avtp_rxmon/format_mutants.py:65`, `tb/verilator/crf_rx/mutants.py:85`, both `[SQ]` harness sections, and `probe_results.json` - the new assertions observe actual output/counter changes across two following intervals. Presentation absence and genuine post-reject loss are checked separately. The lockstep reference is not used as the oracle for the new rule. All five specified controls compile and exit 1 at their named check; both base RTL substitutions reproduce the defect. Every changed pre-existing stimulus/check hunk was examined: rejects now consume sequence numbers, the CRF replica receives the sequence, and pre-existing check expectations remain unchanged, including `tb/verilator/milan_dp/sim_nxn.cpp:7065`.

[R686] PASS Docs - `docs/reference/FR_NFR.md:271`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:192`, `docs/testing/TESTING.md:617`, `:628`, PR #777 and the published receipt set - the rule, scope, reference change and runnable checks are documented consistently. New source comments explain behavior with issue/specification references; no new bench lane label, review round, reviewer identity or issue-comment identity was found. The PR records the extra reject cycle and the unchanged flat instrument. The gate claims are supported with the qualifications below.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #775 assignment; FR-STR-03; ctx:1010; crf:598; `[SQ]` logs | R686-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| RTL | CLEAN | ctx RAM mux/FSM:638/718/1010/1061; crf:399/598; reference:987; lockstep logs | R686-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Robustness | CLEAN | `[SQ]` and discontinuity harnesses; wrap/state/isolation probes; lockstep reset/hazard checks | R686-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Tests | CLEAN | Both mutant drivers; both counter harnesses; base substitutions; milan_dp:7065; published sweep receipts | R686-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Docs | CLEAN | FR_NFR:271; compliance matrix:192; TESTING:617/628; PR #777; evidence_audit.json | R686-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |

Independent executions

`run_probes.py CHECKOUT PACKET PINNED_SIMULATOR` rebuilds eleven cases concurrently with eight workers, `make -j16` and one compiler build job per worker. The supplied simulator identity was verified as version 5.050, revision v5.050. All binaries, altered inputs and temporary files are beneath `scratch/`. No planted defect changes the checkout.

| Case | Result | Receipt |
|---|---|---|
| AAF clean N=4 stack | 169 checks, 0 failures | probes/aaf_clean.run.log |
| CRF clean unit | 15,714 checks, 0 failures | probes/crf_clean.run.log |
| AAF no sequence advance | exit 1, `[SQ2c]` fails | probes/aaf_no_advance.run.log |
| AAF whole MON_STATE write | exit 1, `[SQ2d]` fails | probes/aaf_whole_state.run.log |
| AAF timestamp walk | exit 1, `[SQ1d]` fails | probes/aaf_timestamp_walk.run.log |
| CRF no sequence advance | exit 1, `[SQ-b2]` fails | probes/crf_no_advance.run.log |
| CRF rejected PDU seeds cursor | exit 1, `[SQ-d1]` fails | probes/crf_reject_seeds.run.log |
| Base AAF / CRF RTL with new harnesses | exit 1; `[SQ2c]` / `[SQ-b2]` fail | probes/aaf_base.run.log; probes/crf_base.run.log |
| AAF wrap and state preservation | 172 checks, 0 failures | probes/aaf_wrap_state.run.log |
| CRF wrap | 15,714 checks, 0 failures | probes/crf_wrap.run.log |
| N=1 / N=8 lockstep | 116 / 119 checks, 0 failures | probes/lockstep1.run.log; probes/lockstep8.run.log |
| CRF discontinuity | 2,201 checks, 0 failures | probes/discontinuity.run.log |

`run_regressions.py CHECKOUT PACKET` reproduces the last two rows. Initial convenience run targets could not launch executables when given absolute output directories because the recipes prepend `./`. Builds succeeded; direct execution passed. The portable script uses build targets and explicit executable paths. The initial return-code-2 receipts are retained as reviewer invocation errors, not DUT failures.

Published source-head evidence

These are author executions at the reviewed source head, not manager source-bank runs. `audit.py` verified all 323 published receipt hashes against the public manifest's published hashes. Redacted files intentionally differ from original-byte hashes. Reviewer compiler logs have private installation paths replaced by `<simulator-root>`, with original and published hashes in `receipt_redactions.json`; raw originals remain under unpublished scratch/. Measurements and verdict lines are unchanged. Selected author receipts are copied under `published_receipts/`; the complete public set remains available at the pinned URL above.

- Four shard receipts report 15 + 16 + 17 + 16 distinct suites, all passing, totaling 2,189,615 checks and no failures. Field campaigns and their freshness checks explicitly skipped when their generator was absent. These skipped arms contribute no executed checks.
- Synthesis: 60/60 tops, rc 0. Lint: 89 findings against the ratchet of 89, rc 0. Thirty static gates report rc 0.
- Docs: 42 executed steps ultimately return 0 under Make 4.3. The first two builder attempts refused a dependency origin; separate same-head rerun receipts show both passing. The candidate host-runner contract and metadata-stripped docs step remain skipped. In-place docs checks do not establish metadata-stripped execution.
- route-1x1: the receipt names the exact source head, shows exclusive-lock acquisition, rc 0 and fully routed status. The resource comparison matches the eleventh record in `syn/ooc/pp_resource_baseline.json`: SLICE 15,833 versus 15,835 (-2), LUT +54, FF +10, RAMB/DSP unchanged, WNS +0.141 ns, WHS +0.019 ns. The +5-slice STOP condition is not reached. These are placed/routed desk measurements, not physical calibration.

Flat-instrument risk disposition

The unchanged `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:265` reject path is real, but it is outside shipping RTL. The tracked-source instance census (`flat_instantiations.json`) finds only `tb/verilator/avtp_rxmon/avtp_rxmon_wrap.sv:85` and `tb/verilator/aaf_audio_loop/aaf_audio_loop_wrap.sv:122`. The field harness uses the former. Shipping `hdl/milan/milan_datapath.sv:7461` instantiates `KL_avtp_rx_monitor_ctx` for every configured N_STREAMS, including 1. References in shipping comments and synthesis top inventories are not instantiations. This does not leave a shipping defect open under this change's scope; the flat instrument is not evidence of the repaired sequence rule.

Prior public findings

After writing the independent verdict and ledger, the PR comments, submitted reviews and inline review threads were checked. The public PR contained two review-start notices, zero submitted reviews and zero inline review threads; no prior public findings were available to resolve or retain. The issue contained its assignment, takeover and review-ready evidence. No other reviewer report was read. This observation is scoped to the retrieval time recorded in `public_review_state.json`; the manager must reconcile later findings before merge.

Limits and pending manager duties

No full parent, processor, builder or synthesis bank was independently rerun. No hardware, physical calibration, hosted workflow or local workflow-replica acceptance is claimed. Physical calibration is NOT RUN. Field skips and routed timing are not hardware proof. Hosted executed jobs were not audited in this round; skipped contexts must not be presented as executed validation.

There is no manager source bank at this head. The manager still owns current-dev candidate construction, builder/native banks and linked receipts at the merge turn, hosted/local-workflow acceptance, the other independent review, resolution of any later public findings, maintainer merge authorization, containment, and issue/project closure. This source ledger cannot be carried across later artifact changes without the required re-review.

Final exact-byte verification in `integrity.json` covers 1,441 parent blobs, the index and modes, plus the required processor, axis and stack submodules and lwSRP at their gitlinks. All match HEAD; status is clean. The unused external submodule remains uninitialized. No source fixes, commits, pushes or GitHub writes occurred. Only MANIFEST.sha256-listed files and this report are publishable; scratch/ is disposable and excluded.

R686-1 FINISHED
