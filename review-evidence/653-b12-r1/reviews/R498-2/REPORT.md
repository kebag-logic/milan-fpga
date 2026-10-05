[R498] POSITIVE - exact head 2263c6288956a5edd841df62252326780edd4870

R498-2 internal independent review of issue #653 / PR #666. Tree: `04234de69a17538c76eff84e001cb4ec2c742a04`. Source base: `fa450d301805881ad713b67521477bf042ddadfd`. All five lenses are CLEAN for the assigned documentation and retained-evidence scope. No open BLOCKER, MAJOR or MINOR remains from the reviewed findings. No new RESIDUE or SUGGESTION is recorded.

The startup characterization and restoration proof now support their claims. Independently decoded presentation steps are **-23,612,829 ns** and **+521,369,096 ns**, both with `tv=1`. All 43 observations at each restoration endpoint are successful, complete and equal; all 18 binding observations per endpoint are zero. All fourteen adverse restoration controls fail as required.

I reconstructed the contract from AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, requirements and interface authorities, then the complete base-to-head diff/history and public evidence. The [B12 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892) and [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5994490678) govern this findings-only lane. The two commits change only `docs/findings/653_DISCONNECT_ORDER_BENCH.md`, adding 515 lines overall. Round 2 is one commit above `bef8dd7036f711bf286929fa4cba6bf724c7118d`.

The supplied immutable link names the earlier packet. The current public [round-2 packet](https://github.com/kebag-logic/milan-fpga/tree/871fc1ae68e2fcdfa7abb134956973b455c8bee5/review-evidence/653-b12-r1/author-r2) is the executable evidence examined here. Below, `author-r2/` means that exact revision. No private author material, management workspace or other review report informed the independent pass. `independent-verdict.md` records my verdict and ledger before I opened the two prior public review comments; `public-pr-state.json` records its digest.

[R498] PASS Conformance - `docs/findings/653_DISCONNECT_ORDER_BENCH.md:465`, `:775`; `author-r2/startup-headers.json`, `restore-start.json`, `restore-end.json`; `independent-audit.log` - checked the frozen B12 scope and round-2 outcomes against the cited counter, timestamp and response authorities.

The standards examined were Milan v1.2 section 5.3.8.10/Table 5.6, sections 5.4.5.1-2/Table 5.22, 5.5.2.5 and 5.5.3.5.45/Table 5.36; IEEE 1722.1-2021 section 7.4.42.2.4/Tables 7-156/157; and IEEE 1722-2016 sections 4.4.4.5-.9 and AAF clause 7. Standards-file digests are in `authorities.json`. Counter reset at bind, delayed observation intervals, arbitrary initial sequence numbers, modulo-256 progression and normal AAF timestamp validity were distinguished. This is evidence of the stated sampled findings, not general protocol certification.

All 182 selected command/response/unlock triples match controller, listener, input and response sequence. Each response and unlock notification has successful status. All unlocks contain the required validity bits and ML/MU/SI/SEQ values 1/1/0/0. Each response precedes its unlock; all 182 printed intervals match the receipt timestamps to the displayed precision. Direction A intervals use the link capture, direction B intervals the controller capture. The 140 fixed holds contain five trials for every direction/kind/hold combination; the 40 phase trials remain separate, plus two long windows.

[R498] PASS RTL - complete `fa450d30..2263c628` changed-path inventory, `REQUIREMENTS.md` section 4, `docs/overview/ARCHITECTURE.md:62`, `docs/design/TIME_SYNC.md:28`, `docs/reference/REGISTER_MAP.md:1548`, and `integrity.log` - no RTL, reset, CDC, width, port, register, configuration or submodule-pin change occurs. The architecture distinguishes PHC presentation time from controller and capture clocks. The page preserves the flashed-image boundary at `bbf704ec` and the pre-#655 CRF limitation. No fresh source timing, area or hardware claim is made.

[R498] PASS Robustness - `author-r2/restore_compare.py:35`, `check_restore.py:63`, `startup_decode.py:11`, `probe_phase.cpp:579`, `restore-controls.log`, `focused-probes.log` - applied incomplete/failed inventory, duplicate, malformed, truncated, reset/wrap and foreign-event checks. The comparator requires success and its full expected inventory before equality and zero bindings. Five additional independent adverse restore probes reject changed mapping, matching AEM failure, matching binding failure, boolean status and wrong endpoint. A reordered but complete successful inventory passes. Startup controls cover flag bits, both rollover directions and truncation. Boundary evidence brackets the observed cadence, without claiming every fixed hold crossed with both phases or sub-millisecond race coverage.

[R498] PASS Tests - `author-r2/check_startup.py`, `check_restore.py`, `wire.py`, `rule_controls.cpp`, `startup-replay.log`, `restore-controls.log`, `focused-probes.log` - the tests detect the claimed defects. Startup replay matches 48 earlier first-PDU records and both earliest nonzero polls; all eight startup controls pass. Restore replay passes its equal-success case and rejects all fourteen adverse cases with exit 1. Nine independent synthetic wire/status controls pass, including reversed order, missing/prior push, foreign controller/input/response sequence, auxiliary solicited baseline and non-success status. Eight extracted application-rule controls pass; inversion of the Connected predicate exits 1.

The probe's selection, initialization and reset handling were compared with [the pinned application source](https://github.com/kebag-logic/Hive/blob/a13db9d97009dca49a00fb299805e379131dafb3/libs/modelsLibrary/controllerManager.cpp), at lines 93, 190 and 730. The full graphical application's scheduling was not tested. All 1,510 retained counter reads are successful and show zero SEQ/SI, including 546 early reads and 600 long-window hold reads. All 182 twelve-PDU samples are consecutive. These bounded checks do not independently recount millions of frames in the omitted full captures.

[R498] PASS Docs - `docs/findings/653_DISCONNECT_ORDER_BENCH.md:775`, `:837`, `:888`; `author-r2/project_startup.py`, `project_restore.py`, `privacy-r2.json`; publication `MANIFEST.json`; `docs-check.log` - measured fields, provenance, uncertainty and restoration residuals are stated consistently. The documentation/privacy gate reports zero findings, and the base-to-head whitespace check passes. All 89 source-manifest entries reconcile with the publication manifest. Three publication-redacted files (`identity.json`, `validation-r2.json`, `validation.json`) correctly use the outer manifest's published hashes; their original hashes remain in the source manifest. This is an explicit publication transform, not an unexplained checksum mismatch.

The current wire headers use permitted role tokens or the configured DUT identity. All 546 retain their nonidentity bytes against the earlier public receipts; its controller placeholder is normalized only within the identity span for comparison. The peer entity ID and derivable MAC scan has no matches in the current packet/page. The retained-source audit separately reports no matches across eight private-field categories, including names and serials. No peer identity was found. Exact peer name/serial comparison could not be independently repeated without the unpublished descriptor originals; this is a stated evidence limit. The DUT's configured public identity is permitted by the ruling.

The startup calculations independently reproduce:

| Cycle | First two presentation fields | Signed step (ns) | Tap spacing (ns) | Bind submission to first nonzero read (ms) | Read before unbind (ms) | Read to callback (ms) |
|---|---|---:|---:|---:|---:|---:|
| BAAF0300-2 | d9353fed / d7ccf250 | -23612829 | 125025 | 29.880 | 278.656 | 318.532 |
| BAAF0900-5 | 113d7f85 / 3050f58d | 521369096 | 125016 | 29.947 | 878.672 | 418.654 |

Both pre-bind timestamp counters are zero. First nonzero reads carry FRAMES_RX 68 and 67. The two clean controls step by 124999 ns initially; their full step ranges are 124999-125019 ns. The flagged samples' subsequent steps are 124999-125020 ns. All 48 headers decode `tv=1`, `tu=0`, `mr=0`, `sp=0`, and consecutive sequence values. Bind-to-first-PDU intervals are computed solely from tap times; the three controller intervals above use controller times only. Neither interval class is subtracted from the other.

**gPTP correlation is correctly NOT RUN.** The retained capture filters in `author-r2/run.py:23` select AVTP EtherType `0x22f0`, including tagged frames. The selected capture census contains no gPTP reference; no measured tap-to-gPTP mapping is supplied. Thus signed presentation-field progression is measurable, but absolute presentation lead/lag and timestamp fault ownership remain unresolved. The page explicitly carries this limitation and feeds #667; it does not label consecutive sequences as valid presentation timing.

Prior public findings were reconciled only after the independent pass:

| Prior ID and severity | All attributable lenses | Disposition at this head and verification |
|---|---|---|
| R498-1 F1 MINOR; R499-1 S1 SUGGESTION | Conformance, Robustness, Tests, Docs | RESOLVED. Page:775 supplies earliest reads, separate-clock bounds and decoded startup fields; 48-header replay and independent arithmetic match; absent correlation is explicitly NOT RUN. |
| R498-1 F2 MAJOR; R499-1 F1 MINOR | Conformance, Docs | CLOSED BY PUBLIC RULING as no defect for the configured DUT identity. Peer privacy remains applicable and was checked as described above. No peer identity finding remains. |
| R498-1 F3 MINOR; R499-1 F2 MINOR | Conformance, Robustness, Tests, Docs | RESOLVED. Page:837 and both complete projections expose successful per-descriptor effective values. Eight grouped comparisons reproduce at 4/4/2/2 DUT and 14/14/2/1 peer observations. Complete-inventory, success, equality and zero-binding guards reject all fourteen adverse controls and the additional probes. NVM residuals remain separate. |
| R499-1 R1 RESIDUE | Docs | RESOLVED. The current public PR body and `author-r2/PR-BODY.md` are byte-identical and contain Status, Description, how-to-reproduce, how-to-validate and DoD. `public-pr-state.json` records the digest and check. |

The prior findings are [R498-1](https://github.com/kebag-logic/milan-fpga/pull/666#issuecomment-5994470019) and [R499-1](https://github.com/kebag-logic/milan-fpga/pull/666#issuecomment-5994500952). The final public inventory contains these two verdicts, four review-start notices, zero formal reviews and zero inline comments. No other reviewer report was used before my own verdict and ledger. This review does not stand in for the separate external round.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page:465,775,837; startup headers; restore projections; decoded wire triples; independent-audit.log | R498-2 | 2263c6288956a5edd841df62252326780edd4870 |
| RTL | CLEAN | Entire source diff; REQUIREMENTS section 4; architecture/time/counter interfaces; integrity.log | R498-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Robustness | CLEAN | restore_compare.py:35; fourteen adverse controls; independent mapping/status probes; startup rollover/truncation controls | R498-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Tests | CLEAN | check_startup.py; check_restore.py; wire.py; rule_controls.cpp; startup-replay.log; restore-controls.log; focused-probes.log | R498-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Docs | CLEAN | Page:775,837,888; publication manifest; projections; privacy audit; current PR body; docs-check.log | R498-2 | 2263c6288956a5edd841df62252326780edd4870 |

Real limits: no new bench run, hardware access, calibration, source fix or full source bank was performed. Complete captures, full callback histories, original restore transactions and linked binaries are indexed rather than supplied for this replay. Startup decoding uses the published raw header projections. Source-to-projection fidelity for those new fields rests on the retained-source export/provenance, not a complete capture replay here. Build execution, zero-drop reports and full callback-state coverage remain operator evidence. The current report does not claim that physical restoration was repeated.

Physical calibration is NOT RUN, and field skips are not hardware proof. The assignment reports manager source static/builder and native banks passing at this head; the bounded packet supplies documentation receipts, not the complete manager bank logs. Hosted jobs and the local workflow replica were not inspected or executed here, so no skipped hosted context is counted as an executed test. Their acceptance remains with the manager.

Pending manager duties: publish this report and the manifest-listed receipts, link the current `author-r2` packet from the PR (its existing immutable link still points to round 1), and obtain the separate external verdict with no round left in flight. The PR's sentence saying the updated packet awaits publication should be refreshed during that publication step. Construct and validate the final candidate at then-current dev even though both supplied base references currently equal `fa450d301805881ad713b67521477bf042ddadfd`. Complete hosted/local acceptance, any explicitly authorized merge, containment and issue-state work under CONTRIBUTING. This positive review authorizes no merge and does not close #653 or the physical release obligations.

Portable reproduction, using this packet's scripts and a checkout containing the public evidence object:

```sh
rtk proxy git -C REPO fetch --no-tags https://github.com/kebag-logic/milan-fpga.git 871fc1ae68e2fcdfa7abb134956973b455c8bee5
rtk proxy python3 -B reproduce.py REPO OUTPUT_DIRECTORY
```

The driver waits in the foreground for all four bounded independent checks. Each produces a separate raw log and exit receipt. It then verifies tracked integrity. All disposable captures, builds and evidence extractions stay under `OUTPUT_DIRECTORY/scratch/`. `commands.json` records the invocations. Documentation and whitespace receipts come from the separately recorded focused checks.

Final integrity passes for all 1,012 parent blobs and 790 required-submodule blobs: raw bytes, executable modes, index entries and registered gitlinks match the requested head. Required pins are unchanged: protocol processor `631eeb342ca1e3fa80e734077a56a943aee76ff1`, gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and stream primitives `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The optional external gitlink remains pinned and uninitialized. No source bytes were modified. `MANIFEST.sha256` lists the publishable scripts and receipts; `scratch/` is excluded.

R498-2 FINISHED
