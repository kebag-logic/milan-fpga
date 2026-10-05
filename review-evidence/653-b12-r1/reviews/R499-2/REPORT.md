[R499] POSITIVE - exact head 2263c6288956a5edd841df62252326780edd4870

Round R499-2, external independent review of issue #653 / PR #666. All five lenses are CLEAN for this findings-only change. No open BLOCKER, MAJOR or MINOR remains from the examined source and current evidence. No new finding, RESIDUE or SUGGESTION is recorded.

Reviewed tree: `04234de69a17538c76eff84e001cb4ec2c742a04`. Source base: `fa450d301805881ad713b67521477bf042ddadfd`. The complete range adds 515 lines to `docs/findings/653_DISCONNECT_ORDER_BENCH.md`; its two commits are `bef8dd7036f711bf286929fa4cba6bf724c7118d` and the reviewed head. No implementation, interface, test or gitlink changes occur. Measurements concern the previously flashed `bbf704ec` image.

The public [B12 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892) and [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5994490678) govern this review. The original issue acceptance remains distinct from this document-and-retained-evidence round. Its earlier scope decision separated the CRF counter fix from bench characterization. This review neither establishes the original issue's universal ordering guarantee nor validates later source on hardware.

The supplied evidence link at `9649a107657bdc77d1c47d7ce735e6a282394235` contains round 1 only. I independently located and used the public [round-2 packet at 871fc1ae](https://github.com/kebag-logic/milan-fpga/tree/871fc1ae68e2fcdfa7abb134956973b455c8bee5/review-evidence/653-b12-r1/author-r2). Every packet filename below refers to that fixed `author-r2/` directory. All 90 publication entries match the outer publication manifest. Three transformed files retain their pre-publication hashes in the operator manifest; the outer manifest records their published hashes. See `publication-audit.json`.

Repository contracts, the documentation index, public issue scope, requirements and interface authorities preceded the independent diff/history and evidence pass. My independent verdict and five-lens ledger were written before reading the prior public review findings. Only then were comments 5994470019 and 5994500952 reconciled. No private author material or other checkout was read. `independence-checkpoint.json` and `prior-findings.json` record this boundary.

**Prior finding dispositions**

| Prior finding | All attributable lenses | Disposition at this head | Evidence |
|---|---|---|---|
| R498-1 F1 | Conformance, Robustness, Tests, Docs | RESOLVED | Findings page:775-838; `startup-headers.json`, `startup_decode.py`, `check_startup.py`, `short-polls.csv`; independently recomputed values below. |
| R498-1 F2 / R499-1 F1 | Conformance, Docs | DISPOSED BY PUBLIC RULING | Comment 5994490678 permits the configured DUT identity. The existing page:62 is therefore not a defect. Current packet identity handling and peer fields were separately checked. |
| R498-1 F3 / R499-1 F2 | Conformance, Robustness, Tests, Docs | RESOLVED | Findings page:840-866; both restoration projections; `restore_compare.py`; equal-success control and all fourteen rejected adverse controls. |
| R499-1 R1 | Docs | RESOLVED | Current public PR body has Status, Description, how-to-reproduce, how-to-validate and DoD. The formatting residue is cleared; `public-state.json` records the readback. |
| R499-1 S1 | Tests, Docs | IMPLEMENTED | Findings page:780-826 dates the earliest nonzero observations, keeps the clocks separate, decodes startup headers and preserves unresolved fault ownership. |

**Startup characterization**

The original 24-byte AVTP header projections decode independently. Byte 1 supplies `tv` and `mr`; byte 3 supplies `tu`; bytes 12-15 supply the big-endian presentation timestamp; byte 22 supplies `sp`. The interface definition in `hdl/ieee1722/avtp/avtp_stream_parser.sv:30` agrees with these common-header positions. All 48 retained headers have `tv=1`, `tu=0`, `mr=0`, `sp=0`, version zero and valid stream identity indication. All four twelve-PDU sequences are consecutive modulo 256.

| Cycle | First two presentation timestamps | Signed modulo-2^32 step, ns | Tap spacing, ns | Tap bind-to-first-PDU, ns |
|---|---|---:|---:|---:|
| BAAF0300-2 | d9353fed / d7ccf250 | -23612829 | 125025 | 20227033 |
| BAAF0900-5 | 113d7f85 / 3050f58d | 521369096 | 125016 | 20407250 |
| BAAF0300-1, clean control | cdcb2d53 / cdcd159a | 124999 | 123944 | 222566994 |
| BAAF0900-4, clean control | dba7c762 / dba9afa9 | 124999 | 125000 | 20091409 |

The flagged cases' remaining steps lie in 124999-125020 ns. The clean controls lie in 124999-125019 ns. The discontinuities are real in the retained header bytes despite valid sequence progression.

On the controller clock alone, the first EARLY read is `11:19:03.730732Z`, 29.880 ms after bind submission, 278.656 ms before unbind submission, and 318.532 ms before the callback; FRAMES_RX is 68. The first LATE read is `11:20:09.640696Z`, with corresponding intervals 29.947, 878.672 and 418.654 ms; FRAMES_RX is 67. The earlier polls are zero, and later reads retain the increments. Callback timestamps independently match `rule-increments.json`. These are observation bounds, not individual offending-packet times.

The NOT RUN for absolute gPTP correlation is justified. `run.py` filters plain and VLAN captures to EtherType 0x22f0; controller captures additionally select control subtypes. The startup export records only 0x22f0. There is no retained Sync/Follow_Up reference or measured tap-to-gPTP mapping. Neither a tap/controller subtraction nor an AVTP/tap subtraction is performed. The data characterizes the DUT's emitted startup timestamps but cannot determine absolute presentation lead/lag or assign timestamp-fault ownership. The stated investigation remains on #667.

**Restoration and adverse controls**

Both public projections contain 43 successful observations: DUT bindings/formats/maps/clocks are 4/4/2/2; reference-peer populations are 14/14/2/1. Descriptor identities, statuses and complete effective values agree at both endpoints. All 18 binding observations are zero. The two separately sourced DUT clock observations agree. Provenance names source files, line numbers, sizes and hashes; original transactions remain outside the bounded public packet.

The revised comparator requires exact nonempty inventory, correct endpoint/schema and descriptor identity, successful status, valid types and field lengths, complete mapping entries, no duplicate observation, and agreeing DUT clock reads. Only afterward does it accept equal effective values and zero bindings. Its actual CLI accepts the equal-success case with exit 0. All fourteen adverse cases return exit 1: changed source, changed binding, matching nonzero bindings, changed format, two-sided omission, one-sided omission, empty population, matching failed responses, conflicting duplicate, wrong descriptor, malformed observation, truncated format, truncated map and conflicting clock reads. `restore-controls.log` retains every response and return code. NVM sequence/commit increments remain separate monotonic residuals.

**Other independent evidence**

All 182 selected raw command/response/unlock triples match controller, listener, input and response sequence. Every response has successful status; every selected unlock is a successful unsolicited STREAM_INPUT counters response with valid ML/MU/SI/SEQ fields and values 1/1/0/0. All 182 displayed response-to-unlock intervals recompute exactly within their selected capture clock. The 140 fixed-hold cycles, 40 supplemental boundary cycles and two long windows match the tables. Actual-hold figures match the public summaries; omitted original bind-response/prior-push anchors were not independently replayed.

All 1,510 published poll rows have zero SEQ and SI, including 546 scheduled early reads and 600 long-window hold reads. Each retained initial sequence progresses modulo 256. Complete-capture frame totals and drop reports remain operator evidence; the complete captures were not recounted. Early zero counters alone are not proof that media had arrived or that its observation interval had completed.

The Connected-only unlock predicate, five unconditional error flags, cache initialization and reset handling match the [pinned application source](https://github.com/kebag-logic/Hive/blob/a13db9d97009dca49a00fb299805e379131dafb3/libs/modelsLibrary/controllerManager.cpp) at lines 93-104, 190-214 and 730-800. The tested function is byte-identical in both published probes and `rule_controls.cpp`. Eight rule controls pass; the inverted Connected predicate exits 1. This covers the extracted error rule, not the full graphical application's scheduling.

Independent synthetic capture controls cover response-first, reversed order, missing/prior unlock, foreign controller/input/response sequence and a solicited baseline. Five mutations of the startup input separately change tv, tu, mr, sp and timestamp bytes; every mutated startup check fails with exit 1. The operator's eight startup decoder controls also pass, including both rollover directions and truncation. See `offline-probes.log` and `startup-replay.log`.

The complete findings page and all 90 current packet files pass the repository's identity/local-information text patterns. All 546 current selected headers have neutral controller and reference-peer identity fields, and startup stream identities are zeroed. Compared with the earlier public receipts, all nonidentity protocol bytes and record timing/status/port metadata are unchanged. No reference-peer identity was found in the examined current page or round-2 packet. The original peer name, serial and interface descriptors are not public inputs, so the operator's broader eight-category audit was inspected but not independently rerun against private originals. `packet-privacy.log` and `independent-audit.log` state this limit.

All seven focused documentation/whitespace gates pass. One initial policy run refused because the temporary interpreter lacked YAML support; the available interpreter rerun passes with zero findings. That refusal remains in `policy.log`, and the successful retry is in `policy-retry.log`; it was not counted as a pass. Other checks and exact commands are retained in `execution.json`.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #653 body and comments 5980290102, 5993102892, 5994490678; REQUIREMENTS.md; page:395-909; decoded wire triples, startup headers and restoration projections | R499-2 | 2263c6288956a5edd841df62252326780edd4870 |
| RTL | CLEAN | Complete fa450d30..2263c628 diff/history; docs/overview/ARCHITECTURE.md:43-86; docs/reference/REGISTER_MAP.md:1548; AVTP parser interface:30-35; unchanged tracked source and required gitlinks | R499-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Robustness | CLEAN | probe_phase.cpp:579-590; forty boundary summaries; startup rollover/bit/truncation controls; strict restore comparator and fourteen adverse populations; independent selector probes | R499-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Tests | CLEAN | check_startup.py; check_restore.py; rule_controls.cpp; independent-audit.log; offline-probes.log; 1,510 poll rows, 182 wire triples and focused gate receipts | R499-2 | 2263c6288956a5edd841df62252326780edd4870 |
| Docs | CLEAN | Complete findings page, especially :775-909; current PR template; public scope; all 90 published hashes; decoded identity and text audit; explicit image and correlation limits | R499-2 | 2263c6288956a5edd841df62252326780edd4870 |

Each CLEAN row is a PASS for the named artifacts and stated scope. RTL coverage establishes that this change alters no clock, reset, CDC, width, port, parameter or implementation contract. It is not fresh full-regression or hardware proof.

**Limits and pending manager duties**

No hardware, physical calibration, full source banks, local workflow replica, source mutation or GitHub write was performed. Physical calibration remains NOT RUN. Full original captures, callback histories, restoration transactions and linked binaries were not available for independent replay. Clause interpretation used frozen public requirements, interface authorities and pinned protocol/application source; this is not a fresh audit of complete primary standards documents.

The assignment reports successful manager source static/builder and native banks. Those banks were not repeated or independently certified here. Their source evidence is distinct from final current-dev candidate validation, even though the supplied live dev and source base both equal fa450d30. Exact-head hosted metadata showed successful rtl-fast and several executed documentation/selection jobs; exhaustive suites, portability and physical jobs were explicitly skipped. docs-check was still in progress in the captured snapshot. Skipped contexts are not executed evidence. Hosted and local-replica acceptance remain the manager's responsibility.

The manager must publish this report and its listed receipts, refresh the PR's round-1 evidence link to the fixed round-2 packet above, and replace the stale statement that this already-published packet awaits publication. The accepted current packet is `author-r2/`; archived round-1 files are not replacement evidence. Publication handling for earlier copies remains with the manager. The remaining duties are the second independent review, no in-flight review at merge, hosted/local acceptance, current-dev candidate validation, explicit merge authorization, containment, and appropriate issue/project state. This verdict does not authorize merge or declare issue #653 complete.

Final integrity passes for all 1,802 tracked blobs across the parent and three required submodules, including file kind, raw bytes, executable modes and exact index entries. Required gitlinks match. The optional external gitlink remains pinned and uninitialized. The source checkout is clean. `checkout-final.log` and `public-state.json` retain this evidence.

Portable reproduction, after fetching the two named public evidence commits into the checkout object store:

```text
python3 -B extract_evidence.py <checkout> <review-output>
python3 -B run_checks.py <checkout> <review-output>/scratch/public-r2 <review-output> <markdown-python>
python3 -B audit_evidence.py <review-output>/scratch/public-r2 <review-output>/scratch/public-r1/author <checkout>
python3 -B offline_probes.py <review-output>/scratch/public-r2 <review-output>/scratch/probes
<markdown-python> -B packet_privacy.py <checkout> <review-output>/scratch/public-r2
python3 -B verify_checkout.py <checkout>
```

The markdown interpreter needs the repository's pinned markdown requirements; the policy interpreter needs YAML support. The runner joins all foreground subprocesses, with at most six concurrent lightweight checks and a separate log/return-code receipt for each. Disposable material stays under scratch/. Only REPORT.md and MANIFEST.sha256-listed files are intended for publication.

R499-2 FINISHED
