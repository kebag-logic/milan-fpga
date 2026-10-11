[R559] POSITIVE - exact head aa980479aafd1d72c72015707fa6618b5aa47cb1

External independent review R559-8 of issue #696 / PR #706. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR was found. R558-9-F1 and R558-9-R1 are resolved by the exact requested wording. Prior prose residues and optional suggestions remain explicitly recorded in [RECONCILIATION.md](RECONCILIATION.md), which is part of this verdict.

Reviewed tree: `a7adf20bdededdf76fd4b9fdc9f6b8c820be6082`. This is a delta/composition verdict; the manager's final merge duties remain pending.

## Scope and independence

The review reconstructed AGENTS/CONTRIBUTING, `docs/README.md`, the public issue and frozen scope decisions, linked requirements/interface authorities, the net diff `09c7231eca343607c97c0d66abebb2553688712c..aa980479aafd1d72c72015707fa6618b5aa47cb1` and history, then public execution evidence. An independent verdict and five-lens ledger were written before prior reports were read. Prior findings were then reconciled against this head. No private author material, another concurrent review, management checkout or private reasoning was used.

Authorities include [issue #696](https://github.com/kebag-logic/milan-fpga/issues/696), decisions [6076750392](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076750392), [6076940309](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076940309), [6079087547](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079087547), [6079463350](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079463350), [6089712293](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293) and [6102832618](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618), plus `REQUIREMENTS.md`, `FR_NFR.md`, `MAAP_FABRIC.md`, MAAP module/interface documentation, `AREA_BUDGET.md`, the resource recipe and register/counter interfaces. The issue assigns acceptance item 4 to the post-merge bench lane. M8 counting is withdrawn and documented; M6's one-response capacity is an explicit accepted limitation.

## Composition and record repair

`audit_delta.py` independently rebuilt the merge from ordered parents `32582421bbf095a7b5a7d4b953c4d737b86fe54b` and `09c7231eca343607c97c0d66abebb2553688712c`. Its tree equals `a7291311`'s tree, `0705eb4a691dcfb8211de9c7da79883cc357b249`, with no conflicts or additional edits. The next commit changes only the five requested plan sentences at lines 695, 696, 947, 706 and 968. See [composition.json](composition.json) and [composition-wording.diff](composition-wording.diff).

The MAAP RTL, entire MAAP suite, firmware differential sources and baseline JSON are unchanged from source head `32582421`. Against dev, the composed `milan_datapath.sv` contains only this PR's comment and two MAAP connections. Against the source, the incoming M6 counter selector/read interface is retained. Neither set of shared-file hunks was lost. See [composition-datapath.diff](composition-datapath.diff).

R558-9's unchanged public `record_vs_lane_routes.py` was run at dev, source and composed heads. At dev the 50,267 base rows equal the then-current record. Here the record is 50,013 LUT / 54,306 FF / 15,753 slices, WNS +0.233 ns and WHS +0.017 ns. Both M2 and M6 pass against it and against the historical record. The repaired sentences now identify those records correctly. The script's “base equals record: NO” at this head is the expected historical/current distinction, not a failed lane comparison. See [record-vs-lane-routes.log](record-vs-lane-routes.log).

`audit_record.py` independently verifies 66/66 current-inventory cells across all three endpoints and confirms net JSON changes affect only records and measurement attribution; policy/schema is unchanged. No additional unqualified statement that the current route record is 50,267 was found. Baseline/planning uses of “current” remain the previously classified wording residues, with exact fixes in the reconciliation. No lane deltas were added together or presented as a route of this composed tree.

## Exact-head focused execution

Builds ran in disposable copies under `scratch/`, with the verified pinned Verilator 5.050 executable (2026-07-01, rev v5.050). Independent processes ran concurrently through foreground orchestration, using `make -j16` and two compiler jobs per build. No broad bank, implementation route, hardware session, container job or hosted write was performed.

| Execution | Result | Receipt |
|---|---|---|
| Default MAAP target | 186 unit checks, 0 failures; 65 campaign rows: 63 named defect rejections, 2 clean controls | `maap-suite.log`, `.rc` |
| Separate real-datapath MAAP test | 5 checks, 0 failures | `maap-integration.log`, build/run `.rc` |
| `milan_dp` option-off and ax1x1 | 236 and 233 checks, 0 failures | `datapath-legs.log`, `.rc` |
| `milan_dp` 4x4 and 8x8 counter/MAAP legs | 1,967 and 3,751 checks, 0 failures | `counter-legs.log`, `.rc`, `counter_legs.mk` |
| Three independent wiring probes | Dropped link, link tied high and dropped clock all build, then fail their required named assertion | `wiring-results.json`, `wiring-*-build.log`, `wiring-*-run.log` |
| `lint_rtl.py --check --jobs 2` | PASS: 90 violations <= ratchet 90; 18 waived | `lint.log`, `.rc` |
| Scoped docs/record gates | 12/12 commands exit 0, including both TOC modes, em-dash against dev and `pp_resource_gate.py check-baseline` | `docs-results.json`, individual logs/rc files |
| Merge, record and checkout audits | Automatic merge equality; 66 cells match; bytes/modes/index and required pins exact | `composition.json`, `record-policy-delta.json`, `integrity-before.json`, `integrity-after.json`, empty `final-status.log` |

The counter legs exercise real GET_COUNTERS mask `0xFFF`, monitor values, timestamp valid/not-valid accounting, reserved quadlets zero, unclaimed-MAAP talker holds and MAAP-off restoration. This checks the incoming indexed counter path beside the MAAP engine; it is not the full datapath matrix. Independent wiring probes demonstrate that missing ports tolerated by the existing lint waiver cannot silently pass the integration checks. Their expected failures are separate from clean-suite results.

## Lens results

[R559] PASS Conformance - `hdl/ieee1722/maap/KL_maap.sv:141-203,248-259,311-339,380-386,430-497`; `hdl/milan/milan_datapath.sv:7181-7188`; issue #696 and decisions above - M1 uses octet-reversed MAC comparison in the two required Table B.7 cells; M2 echoes requested start and all 16 count bits separately from overlap fields; M3/M4 seed at first enable from MAC low 32 bits plus live clock, with zero fallback and stepped first draws. The power-of-two separation criterion is accurately scoped. M5 responds to the rising operational edge; M6 preserves the active frame and queues the allowed response; M7 uses 17-bit bounded ends; M8 requires all 42 bytes and discards malformed input without effect. Current unit/campaign and wiring results pass. No new register-map, filter or mailbox contract appears. Source resource attribution and bench limits are stated below.

[R559] PASS RTL - `hdl/milan/milan_datapath.sv:2124,2165,3000,3450-3533,6337-6344,7181-7188`; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:769-786`; `sw/litex/milan_soc.py:841-843`; full `KL_maap.sv`; merge/lint/counter receipts - both shared-file changes survive. The counter selector maps twelve columns, guards indexes/defaults and retains the valid-mask/reserved-word contract; real reads pass. Both clocks use `milan_cd` in the SoC binding and `eff_link_w` is already synchronous. New MAAP registers reset; pending-response cancellation/priority, arithmetic widths, first-enable selection and transmit snapshots match their contracts. No new CDC pattern appears. Lint passes at the existing ratchet.

[R559] PASS Robustness - `tb/verilator/maap/sim_main.cpp:442-471,536-566,781-941`; wiring/counter/option-leg receipts - applied malformed/truncated input, missing strobes, supplied-range boundaries, zero seed, reset/disable/link return during pending response, repeated events, long outage, backpressure and configuration-dependent behavior. The current campaign rejects loss-edge restart, zero-fallback and response-corruption plants. Integration rejects missing/constant link and missing clock. Reserved words and MAAP holds pass. Correct but individually ungraded details remain optional suggestions, not claimed executed coverage.

[R559] PASS Tests - `tb/verilator/maap/Makefile`, `integration.mk`, `sim_main.cpp:1089-1275`, `sim_integration.cpp`, `mutants.py`; firmware differential sources; MAAP/counter/wiring receipts - examined assertion oracles and mutation grading, not just exit status. Build failure cannot count as a killed mutant. Both controls pass and every planted defect reaches its named assertion. M2 below-offset echo and first-draw q1/q3/q9 fixes remain effective. Learned-map tests cover the stated word/carry domain, with finite linearity-validation limits disclosed. Test and differential sources are unchanged by composition; differential and coverage banks were not rerun here.

[R559] PASS Docs - `docs/design/MARK_II_AREA_PLAN.md:56,66-147,317,650-706,924-968,1086`; `AREA_BUDGET.md:104-160,365-387,410-470`; `MAAP_FABRIC.md:42-188,197-273`; MAAP module docs; firmware MAAP README; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`; findings index; public PR/issue evidence; docs/record receipts - the five replacements match the required outcome, inventory matches all records, and other historical/planning figures are qualified by context. M6/M8 deviations, first-draw criterion and source measurement attribution are stated. Docs gates and baseline check pass. Remaining wording residues and optional improvements are explicitly retained.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue rulings; MAAP RTL/instance; unit/campaign/integration; record policy | R559-8 | aa980479aafd1d72c72015707fa6618b5aa47cb1 |
| RTL | CLEAN | Datapath counter/MAAP hunks; monitor interface; clock binding; merge proof; lint/counter runs | R559-8 | aa980479aafd1d72c72015707fa6618b5aa47cb1 |
| Robustness | CLEAN | Boundary/reset/stall/outage tests; option-off/nxn legs; three wiring probes | R559-8 | aa980479aafd1d72c72015707fa6618b5aa47cb1 |
| Tests | CLEAN | MAAP assertions/build/campaign; first-draw checks; 63 defects plus controls; counter/wiring tests | R559-8 | aa980479aafd1d72c72015707fa6618b5aa47cb1 |
| Docs | CLEAN | Plan repair; budget/MAAP/interface/findings docs; 66-cell audit; docs gates; reconciliation | R559-8 | aa980479aafd1d72c72015707fa6618b5aa47cb1 |

RESIDUE and SUGGESTION do not make a lens unclean under the supplied owner rule. This ledger does not cover future changes. Every prior finding is resolved or explicitly retained in the linked reconciliation; no deferred code defect is treated as resolved.

## Limits and pending manager duties

The [supplied public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/97f433d668907446e83c074b21e81d03a34988af/review-evidence/696-r1) contains historical author receipts. Selected executable receipts were extracted and published hashes checked where indexed (`public-evidence/receipt-index.json`). They concern the earlier `0df48637` merge, not execution at this head. The [author source REVIEW READY](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6103504186) attributes later unit/differential/coverage/docs evidence to `32582421`. The retained resource record and design documentation attribute 50,013 LUT and MAAP 490/340 (+51/+60 against the stated baseline) to the source first-draw step at `bee1b0d7`. Those are author source evidence and attribution, not new measurements by this reviewer. Record equality does not measure the combined tree.

No manager source bank ran at this exact head; none is claimed or inferred. The manager must build and validate the final current-dev merge candidate, run required builder/native banks, and link receipts when published. The supplied source base and live dev are both `09c7231eca343607c97c0d66abebb2553688712c`; live state must be rechecked at the merge turn. This verdict does not substitute for candidate validation, required resource comparison, protected hosted contexts, local-replica acceptance, second review completion, explicit merge authorization or post-merge containment.

`hosted-observation.json` is one read-only snapshot: some actual jobs succeeded, others remained running/queued, and Physical gPTP was skipped. The selector named `full-ci-gate` succeeding does not establish completion of its pending shards. Hosted/local-replica acceptance belongs to the manager. Physical calibration is **NOT RUN**. Declared field skips and simulation are not hardware or bench interoperability proof.

No full parent, processor, gPTP, portability, builder or firmware bank ran here. No synthesis/route or new timing/area claim is made. The every-seed argument depends on structurally linear RTL maps; finite sample checks cannot alone exclude an arbitrary sparse nonlinear change. Existing one-response capacity, pool-mapping bias and optional ungraded details remain disclosed.

The manager should carry the exact residue fixes and suggestions in the reconciliation, finish the independent review/merge ledger, publish candidate receipts, and complete containment/issue updates after an authorized merge. This reviewer made no GitHub write, source edit, commit, push or merge.

Final verification covers 1,289 parent blobs and initialized required dependencies: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. All five parent gitlinks match the commit. Bytes, modes and index are exact; original checkout status is clean. Probes affected disposable copies only; no restore was needed and no job remains running.

[REPRODUCE.md](REPRODUCE.md) records commands and provenance. `MANIFEST.sha256` is the publication allowlist; `scratch/` is excluded. Compiler-location prefixes in build logs are replaced only for public-safe path attribution, with original/published hashes in `receipt-redactions.json`.

R559-8 FINISHED
