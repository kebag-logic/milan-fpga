[R930] POSITIVE - exact head ec727b64663b4eef2fc8da1ea5e0eae6541597d1

The delta closes the test defects at their causes. No open BLOCKER, MAJOR, MINOR, new RESIDUE or new SUGGESTION was found against this head. All five lenses are CLEAN within the limits below. Historical publication handling remains a manager duty under this round's explicit scope decision.

Scope and authorities

Reviewed [issue 37](https://github.com/kebag-logic/tsn-c-stack/issues/37), [PR 38](https://github.com/kebag-logic/tsn-c-stack/pull/38), source base `69bac7cd52815d2ae223a5a3aa6d022a1f1d35de`, previous head `e0b144904e57c96928f1dd3fca36a00df42f6ed3`, and exact head above, tree `00b9b9eebd1dd1f9ecdea206ead5a0a40ed67951`. Round two is one commit and eight changed files. The complete base-to-head change has two commits and eleven files. `src/` and `include/` are byte-identical to the previously reviewed head.

The supplied repository instructions, CONTRIBUTING.md, README.md, coding standard, architecture, port contract, requirements and verification guidance were examined. There is no tracked AGENTS.md or docs/README. The issue freezes rejection/counting of 0–55, acceptance of 56 and greater from the existing prefix, unchanged 82-byte minimum and transmit value, and fault-sensitive tests. The issue has no comments. The available manager PR comments are review-start notices, including [this round's start](https://github.com/kebag-logic/tsn-c-stack/pull/38#issuecomment-7172294104); they supply no additional execution receipts. No manager source bank is inferred.

The independent diff pass preceded prior-finding reconciliation. The independent verdict and ledger were recorded before explicitly reconciling the other prior review's findings. Only public source and published evidence were used. No private author material, private management material or other current-round review was consulted.

Conformance

The prior CLEAN conformance conclusion carries: implementation and clause authorities are unchanged by this delta. ADP-01 and PORTING agree with the frozen policy. The `< 56` comparison retains the complete `0x07FF` field, excludes valid_time, and follows the actual frame-size check. Rejection accounting, target selection and state transitions are unchanged. `adp_build` still writes 56; the public frame size remains 82.

Authorities remain [IEEE 1722.1-2021](https://standards.ieee.org/ieee/1722.1/6670/), 6.2.2.6 and 6.2.7.1.3; [Milan v1.2](https://avnu.org/resource/milan-specification/), 5.6.3.1 and Tables 5.50–5.51; and [IEEE 1722-2016](https://standards.ieee.org/ieee/1722/5979/), 4.4.5.4. Their previous clause inspection is carried, not represented as a new standards inspection. They do not expressly mandate accepting an extended ADPDU; broader receive tolerance is project policy. A declared length of 2047 is a robustness case, not proof of a conforming complete standard-MTU transmission.

RTL and consumer boundary

There is no RTL, ABI, callback, storage-layout or submodule delta. The prior RTL lens carries. Its limits remain: the split/mailbox path does not reject on this field, but the ADP mailbox capacity is 128 frame octets. Complete control lengths 57, 84 and 102 fit; a larger complete frame can be dropped upstream. The separate all-fabric validator's declared-payload check is neither changed nor proven by this C-library PR. No RTL execution is claimed.

The published `parent-consumer.patch` adds 256/2047 with absent surplus and a `0x00FF` fault, preserving valid_time rejection and exact-56 acceptance controls. It changes only `sw/firmware/ctrl/test/test_adp.cpp` and `ctrl_mutants.py`. Independent application checks pass without offsets at both the author-tested parent `5de21ff3661436ea5598718aca36934361e35340` and supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`: `parent-check.json`. That receipt records both parents' gitlinks. Stack pins differ (`715589c1...` and `70936b77...`); the protocol-processor pin remains `801ef2283ec793e35a2590fc6593c90313a64041`. These are read-only observations, not pin updates or final-candidate validation.

Verified author receipts report thirteen selected consumer arms passing and ten selected faults caught, with naming checked against the full 847-entry table. This supersedes the earlier subset-registration failure. It remains a selected author campaign at the stated parent, not a complete parent bank. The patch and draft parent description must accompany and be reconciled with the actual pin bump.

Prior findings, resolved or retained

Public findings: [R930-1](https://github.com/kebag-logic/tsn-c-stack/pull/38#issuecomment-7171620502) and [R929-1](https://github.com/kebag-logic/tsn-c-stack/pull/38#issuecomment-7171645025). Original severities and attributable lenses are retained below. Historical publication disposition is distinct from source-head acceptance.

| ID; severity; lenses | Artifact, authority and original impact | Required outcome and verification | Disposition |
|---|---|---|---|
| R930-1 F1; MINOR; Tests, Robustness | `tests/test_adp.cpp:840–867`; issue 37 criterion 1 and PORTING's readable-buffer contract. A larger shared allocation hid reads beyond 82 reported bytes. | Separate `bare(82)` at line 844 and `whole(26 + length)` at line 851 now exist. The child at lines 764–781 ends its frame immediately before a protected page; line 865 requires exit zero. An independent injected `frame[82]` read fails all five named boundary assertions in ordinary and instrumented runs. The instrumented accept-only run reports a read immediately after an 82-byte allocation. See `native-results.json`, `memory-results.json` and raw logs. | CLOSED at root. |
| R929-1 F1; MINOR; Tests | `tests/test_adp.cpp:843`, `tests/mutations.json`; issue 37 scope/criterion 2, ADP-01 and CONTRIBUTING. Three samples missed upper-field truncation and lost prior sensitivity. | The loop covers every value 57–2047, both accepted targets, valid_time 0/31, all five configurations. Independent runs catch each `0x03FF`, `0x01FF`, `0x00FF`, `0x007F` fault in all five named accept instances. Hash-verified author `own-mutants-head.txt` additionally records all fifteen earlier controls caught and the unchanged control passing. Counts/mappings agree in `delta-audit.json`. | CLOSED at root. |
| R929-1 F2; RESIDUE; Docs | `docs/REQUIREMENTS.md:117`, `CHANGELOG.md:5`; issue 37 replaces the exact-length portion of issue 3. Provenance was omitted. | The requested issue-37 sentence and change-log link are present with the intended exact wording. Independent checks pass in `delta-audit.json`; no behavior or clause claim changes. | CLOSED. |
| R929-1 F3; SUGGESTION; Tests, Docs | `examples/rv32/smoke.c:150–183`, `docs/VERIFICATION.md:136`; required RV32 target and ADP-01. The old smoke lacked a long-field control. | Length 256 is accepted in all five configurations and documented. Independent Debug RV32 exits are 0 unchanged, 64 with equality restored, 64 with the low-octet mask, and 63 with the bound removed: `rv32-controls.json` and raw receipts. Published Debug/Release gates both return 0. | CLOSED. |
| R929-1 F4; SUGGESTION; Tests | Published `parent-consumer.patch`, `PinAcceptsLongDiscoveryThroughMailbox`; same upper-bit weakness at the consumer. | Patch includes 256/2047 in 82-byte inputs and the low-octet fault. Independent application passes on both parents. Verified `consumer-plants.log` records that fault failing its named mailbox assertion and all ten selected faults caught. | CLOSED in proposed patch; carrying it with the pin bump remains pending. |
| R930-1 F2; MINOR; Docs; R929-1 F5; SUGGESTION; Docs | Round-one HANDOFF.md, REVIEW-READY.md and old-core receipt; CONTRIBUTING's publication privacy rule. Host locations disclosed workspace information. | All 25 round-two author files were fetched, hashed and scanned, with no host-location pattern found; prose, logs and patch were inspected. The round-one scan still identifies affected lines without repeating them. See `public-packet-verification.json`. | CLOSED for this head's packet. Historical item RETAINED for the manager under the explicit round-two instruction: the scrubber is fixed and history is not rewritten. No new open source-head finding. |

Tests and robustness

One foreground driver waited for three concurrent focused campaigns, using at most six simultaneous compilation jobs. Builds and mutations used disposable copies under `scratch/`; the checkout was never edited. `run_probes.py` accepts source and pinned test-prefix arguments. It checks the baseline count, nonzero fault outcomes, five failed instances and expected named messages. A crash alone is not counted as a named catch.

| Independent check | Result | Receipt |
|---|---|---|
| Ordinary ADP suite | 49/49 pass | `native-head-0.log`, `native-results.json` |
| Instrumented ADP suite | 49/49 pass | `memory-head-0.log`, `memory-results.json` |
| Eleven registered length faults | Eleven caught; five named instances each | `native-results.json`, `native-adp-*-0.log` |
| Faulty overread, protected page | Five named failures in each build mode | `native-adp-long-control-length-reads-surplus-0.log`, `memory-adp-long-control-length-reads-surplus-0.log` |
| Faulty overread, accept-only allocation | Expected heap boundary diagnostic at first excluded byte | `memory-adp-long-control-length-reads-surplus-1.log` |
| RV32 baseline and three faults | Expected exits 0/64/64/63 | `rv32-controls.json`, `rv32-*-smoke.rc` |
| ADP document links/provenance | 84 line/name links valid; 489 plants; issue links correct | `delta-audit.json` |
| Parent patch | Applies at both stated parents | `parent-check.json` |

The protected-page baseline executes 61,440 combinations: 2,048 field values, five configurations, two valid_time values and three targets. It checks the physical end boundary separately from behavioral assertions. Acceptance checks discard accounting and state/timer effects; inactive/delaying cases compare complete core and fake-port storage. Unchanged tests preserve the 0–55 field and actual 0–81 frame refusals. Added system calls are confined to hosted tests.

Published evidence and documents

Evidence was read at [publication commit d46de11e](https://github.com/kebag-logic/milan-fpga/tree/d46de11e7b5e590a914a9f86718477c6b203fbab/review-evidence/adpcdl-r2/author), separately from its [round-one packet](https://github.com/kebag-logic/milan-fpga/tree/d46de11e7b5e590a914a9f86718477c6b203fbab/review-evidence/adpcdl-r1). All 23 round-one author files and 25 round-two author files match published SHA-256 manifests. The publication commit is reported **unsigned**, and no signature file is present. Content identity was verified; signer authentication was not established. No signed-evidence claim is made.

Author receipts identify this head/tree and report all 28 Linux steps at zero, 489/489 caught faults, and Debug/Release RV32 checks at zero. Coverage remains 100% after existing exclusions. Raw ADP totals are 205/207 lines and 97/104 branches; the receive receipt executes every receive line and records 1,120 rejected versus 39,917 continued outcomes at the length comparison. The ratchet and exclusions are unchanged. These are published source receipts, not independently repeated full gates.

Exact-head hosted [run 45684809576](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45684809576) completed successfully. Both quality and bare-metal validation steps executed successfully; neither is a skipped context. `public-status.json` preserves job/step metadata. Hosted acceptance remains manager-owned.

All changed prose, JSON, source comments, generated ADP mappings and PR text were examined. ADP-01, PORTING, REQUIREMENTS, VERIFICATION, CHANGELOG, TESTS and TRACEABILITY agree. New comments contain standards/requirement references and introduce no prohibited review or bench identifiers. PR text matches the strengthened tests and distinguishes sender requirements from receive policy. No additional wording residue was found.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue 37; ADP-01; receive and transmit code; unchanged standard clauses and interface | R930-1 carried; R930-2 delta | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| RTL | CLEAN | No RTL or interface delta; published parent patch; clean application to tested parent and live dev; parent gitlinks | R930-1 carried; R930-2 patch | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Robustness | CLEAN | Exact allocation; protected-page child; independent injected read; full field sweep and four narrowed masks | R930-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Tests | CLEAN | 49 baseline ADP cases, eleven caught faults, instrumented boundary failure, RV32 controls, published gates | R930-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |
| Docs | CLEAN | All delta prose and generated mappings; issue link; 25 matching packet hashes and zero host-path hits | R930-2 | ec727b64663b4eef2fc8da1ea5e0eae6541597d1 |

Limits, restoration and pending manager duties

This is a delta review, not repetition of full source or parent gates. No full parent, processor, timing, synthesis or builder bank was run. No RTL simulation, hardware operation, shared installation, remote write, source fix, commit, push, merge or author contact occurred. Physical calibration NOT RUN. Field skips and host execution are not hardware proof.

`integrity-before.json` and `integrity-after.json` verify all 100 tracked source blobs against HEAD, including executable modes, exact index entries, head/tree and empty status. This source repository has no submodule gitlinks. Parent gitlinks were read and recorded, never modified. Disposable mutations required no checkout restoration. `scratch/` is excluded from publication; MANIFEST.sha256 lists publishable scripts and receipts. Logs replace only local source, packet and test-prefix locations with portable placeholders.

The manager must publish this report, obtain the required independent approvals, handle the historical publication item under the stated policy, carry the consumer patch with the eventual pin bump, and validate the final current-dev merge candidate with builder/native banks and linked receipts. Source base `69bac7cd52815d2ae223a5a3aa6d022a1f1d35de` and live parent dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct. Earlier equal-tree source trials and clean patch application do not validate that final candidate. Hosted acceptance and merge containment remain manager duties. No manager source bank is claimed.

R930-2 FINISHED
