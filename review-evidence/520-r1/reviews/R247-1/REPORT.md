[R247] POSITIVE - exact head 28e350b99ac240a750326b762c6d029f0653362c

Round R247-1: cleared-context internal source review of kebag-logic/milan-fpga issue #520 / PR #522. All five lenses were applied independently. No open BLOCKER, MAJOR, MINOR, or SUGGESTION finding remains from this review. The generated-ROM stale-cell defect is resolved at this head.

This is a source verdict, not merge authorization or completion of issue #520. External R248 Opus remains pending availability and is not waived. Manager-owned trusted replica, hosted exact-head evidence, final current-dev candidate validation, authorized merge, containment and Closed/Done remain required. No Actions/run/check API, `gh run`, `gh pr checks`, or `statusCheckRollup` was inspected.

The reviewed tree is `d17c117db03128e444b7b44742fe82f10746cb28`. Its actual parent/base is `483a133ed08867ea0d300d2b4a027b5b48a4282f`. PR metadata still identifies this exact published head; its recorded base is not evidence of the eventual live-dev merge candidate.

The review was reconstructed from these public authorities and executable artifacts:

- [Assignment](https://github.com/kebag-logic/milan-fpga/pull/522#issuecomment-5782249714), [issue #520 frozen scope and decisions](https://github.com/kebag-logic/milan-fpga/issues/520), and its public takeover/review-ready/source-validation comments. PR reviews and inline review comments were empty in the captured public state.
- `AGENTS.md` sections 6-7, `CONTRIBUTING.md` sections 2-3 and 5-6, `docs/README.md`, `REQUIREMENTS.md:217` (REQ-VER-02/04), `docs/guides/VERIFICATION_DEVELOPER.md`, `docs/overview/ARCHITECTURE.md:57`, `docs/integration/INTEGRATION_GUIDE.md:5`, and `docs/reference/SUBMODULES.md`. Root interfaces and donor ownership remain authoritative.
- [Immutable triage](https://github.com/kebag-logic/milan-fpga/tree/e4a2d05481b33e9b437023a50f2eb754ea0592eb/review-evidence/478-r1/throughput-cache-triage), the single implementation commit and complete six-file diff, and [immutable author/manager evidence](https://github.com/kebag-logic/milan-fpga/tree/34ba85c56b1f3bc0702691924f2c9ff38532ff1b/review-evidence/520-r1).
- Current result-cache contracts in `docs/testing/CI_WORKFLOWS.md:221` and `syn/yosys/README.md:99`, with public issues #350 and #270 for the existing trust boundary. No private author/reviewer transcript or scratchpad was read.

**Public defect and prior-observation disposition at this head**

| Public item | Disposition and evidence |
|---|---|
| #520 / triage round2: changed nonempty PP AECP ROM reused 1,141,365 cells while live synthesis measured 1,122,602 | RESOLVED. `run.sh:503`, `result_cache.py:52,95,154`, the independent PP experiment below, and the public raw stat/ROM audit show changed bytes miss and publish the live count. |
| Round2's investigated possibility of cached success hiding an uncached synthesis failure | NOT ESTABLISHED by the original evidence. Both original uncached and changed uncached synthesis succeed. This review likewise observed exit 0 for both; the defect is stale numeric evidence. |
| Triage round3: successful generator writes the wrong filename | EXISTING REFUSAL PRESERVED. Independent seed-only controls for every image in both modes return 2 before digest/lookup; shipped controls additionally cover writable cache and uncached paths. |
| Cross-checkout same-source cache miss due to staged sv2v hash changes | RETAINED as the separate #270 performance observation, expressly outside frozen #520 scope. No path normalization, performance improvement, native shared-seed enablement, or trust broadening is claimed. |
| Earlier PR review findings | None present in the captured public PR reviews/inline comments. No prior reviewer severity was downgraded or finding moved elsewhere to obtain clean coverage. |

**Independent results**

All commands and portable probes are listed in [COMMANDS.md](COMMANDS.md). Each command has raw stdout/stderr and an exit receipt. Tests used disposable state only, with no source edits, commits, pushes, other-checkout edits, shared installs, privilege, hardware, Docker/act, author contact, or other agents. No full native or builder bank was rerun. Native test concurrency remained below eight jobs. Focused synthesis used the measured Yosys 0.66 binary and sv2v v0.0.13 identities in [tools.json](tools.json); no Verilator execution was needed for this tooling-only diff.

| Check | Result | Receipt |
|---|---|---|
| Shipping `result_cache.py --selftest` | PASS | `unit.receipt.json` |
| Shipping `cache_selftest.py --logs ...` | PASS: five original live arms plus 54 ROM driver invocations | `live-bank.receipt.json`, `live-bank/` |
| Independent byte framing, key, record/stat and seed CLI controls | PASS: 95 commands, including seven deliberately defective copies rejected by the shipping selftest | `independent-controls/complete.json`, `commands.json`, raw streams |
| Independent real-driver seed-only refusal controls | PASS: 44 invocations, both modes and two selected real tops | `independent-driver/complete.json`, per-run receipts/stat JSON |
| Independent real PP-shadow comparison | PASS: seven runs including the labelled fault control below | `independent-pp/complete.json`, per-run inputs/stat JSON/result records |
| Shell syntax, Python/shell idioms, docs, workflow contract, actual-base em-dash and whitespace checks | All seven exit 0 | `focused-1.receipt.json` through `focused-7.receipt.json` |
| Public evidence and unchanged-contract audits | PASS | `public-evidence-audit.json`, `preserved-contracts.json` |

The independent PP probe ran the unchanged driver and real generators, then replaced only the disposable generated `ucode.hex` with the triage payload `INVALID_ROM_DATA\n`. Its separately labelled fault arm freezes the ROM digest to the baseline, deliberately simulating the missing input dependency. The source itself is never modified.

| Independent PP run | Exit | Cache hit | Cells |
|---|---:|---|---:|
| Baseline cold | 0 | No | 1,141,365 |
| Identical warm | 0 | Yes | 1,141,365 |
| Identical read-only seed | 0 | Yes | 1,141,365 |
| Deliberate frozen-digest fault with changed ROM | 0 | Yes, stale as expected | 1,141,365 |
| Changed ROM, correct digest, old head and seed available | 0 | No | 1,122,602 |
| Identical changed-ROM warm | 0 | Yes | 1,122,602 |
| Same changed-ROM input uncached | 0 | No | 1,122,602 |

Cold, changed-live and changed-uncached staged Verilog is byte-identical, SHA256 `5063eb17d0b7d5aea83688602a4a8fc72dc583e2867bf5dbfaec8fc2f89f88a8`. Actual lookup/store identities agree; only the ROM identity changes between baseline and changed input. Baseline bundle SHA256 is `15ec9c1dd64eedd61359f5998cc78b029995d320229cdc6eb9885a64fda45e73`; changed bundle is `04b9b3bffbf630f5d56ac03ccc6523863acd8df847243b348d1f39ef3754bcaf`. The generated ACMP and gPTP images, program and tool identities remain fixed. Live stat JSON independently supplies the published numbers. Same-input live/hit result records agree byte for byte. Read-only seed bytes and modes remain unchanged. The fault arm proves this experiment would expose reuse of the old PASS/stat pair; it is not a source pass or an uncached-failure claim.

**Lens evidence**

[R247] PASS Conformance - [syn/yosys/result_cache.py:52](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/result_cache.py#L52), [syn/yosys/run.sh:477](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/run.sh#L477), `independent-controls/`, `independent-pp/` - Checked frozen #520 criteria 1-4 against implementation and independent execution. The fixed lexical sequence is exactly `gptp_ucode.hex`, `ltn_rom.hex`, `ucode.hex`; each ASCII name plus NUL, eight-byte big-endian byte length and exact content enters SHA256. Independent binary-content framing, same-size byte changes, preserved timestamps, file order, unrelated files and swapped filename/content associations were checked. Schema 2 and the ROM input participate in both key and record verification. Criterion 5's source evidence is accepted below; its pending workflow/merge portions remain pending.

[R247] PASS RTL - [syn/yosys/run.sh:235](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/run.sh#L235), `run.sh:428,441,517,646,679`, `preserved-contracts.json`, `full.diff` - Checked synthesis architecture against the root integration and donor ownership contracts. Generation completes before any top lookup; one conservative three-image digest feeds lookup/store in full and elaborate modes. The common selected-top loop has no top-specific exception. Inventory remains exactly 54 tops. Source derivation, selection, tool identity, programs, live stat extraction, result serialization, structural gates/ownership, allocator and workflow cache scoping are byte-identical to the actual base. The original hit verifier still derives cells from stored stat JSON and requires field equality. Processor ROM consumers were examined at `protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:418`, `protocol-processor/hdl/aecp/KL_aecp_ucpu.sv:121`, and `gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv:107`. The complete diff and final blob/gitlink audit establish that HDL, firmware, generators, pins, interfaces and ratchets did not change. Wire fields, clocks, resets, CDC, FSM, backpressure and feature-state behavior therefore have no changed implementation artifact in this issue; this is not a new hardware-conformance claim.

[R247] PASS Robustness - [syn/yosys/run.sh:477](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/run.sh#L477), [syn/yosys/result_cache.py:154](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/result_cache.py#L154), `independent-driver/`, `independent-controls/` - Verified failed generation, absent/empty/wrong-name images and digest failure stop before lookup with the expected exit 2. Exercised every image under seed-only full/elaborate runs independently. Genuine schema-1 keys miss; relocated schema-1 PASS/stat records refuse and run live. Missing, malformed, mismatching and duplicate bundle fields, FAIL status, forged cells/stat and every old input-field mismatch refuse. Boolean, negative, fractional, string and null cell values cannot be cached. Writable-head precedence, valid read-only seed hits, bad-seed live fallback, no seed writes and no existing-entry rewrite remain intact. Runtime reset/timeout scenarios are outside the unchanged RTL scope established above.

[R247] PASS Tests - [syn/yosys/rom_cache_selftest.py:157](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/rom_cache_selftest.py#L157), `rom_cache_selftest.py:203,219`, `cache_selftest.py:85,132`, `result_cache.py:386,435`, independent probe receipts and public native logs - The five original integration arms remain called. New real-driver controls vary each of the three images with unchanged other identities, both modes, two selected tops, writable state and read-only seeds. They check explicit hit/miss behavior and lookup/store equality. Independent controls were written without importing the author's probe. Seven isolated mutants omitted each image, ignored content, omitted the key field, ignored record ROM equality, or accepted schema 1; all failed their expected selftest. The real PP frozen-digest arm independently exposes stale numeric evidence, and restored source behavior agrees with uncached synthesis. Dynamic cache coverage here is two small tops in both modes and PP-shadow in full mode; all 54-top propagation is also checked in the unchanged common loop, and public uncached native evidence covers all 54 tops. No claim of independent warm-cache synthesis of all 54 tops is made.

[R247] PASS Docs - [docs/testing/CI_WORKFLOWS.md:245](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/docs/testing/CI_WORKFLOWS.md#L245), [syn/yosys/README.md:104](https://github.com/kebag-logic/milan-fpga/blob/28e350b99ac240a750326b762c6d029f0653362c/syn/yosys/README.md#L104), #520/PR #522 public comments and `public-evidence-audit.json` - Current contract prose correctly describes names, framing/order, guard ordering, conservative scope, modes, two tiers and schema migration without guessing old evidence. The public distinction between stale cells and an uncached failure is maintained. There is enough immutable command/stat/ROM evidence to reconstruct the defect and result. The source/current-candidate, internal/external review and physical-evidence limits remain explicit; no new performance or hardware claim is accepted.

**Public full-source evidence accepted, with limits**

225 selected immutable public files were checked against their Git blob IDs. Of these, 181 downloaded source-evidence files were additionally checked against the publication manifest. The author PP stat JSON independently reads 1,141,365 / 1,122,602 / 1,122,602. Its cache records agree with those stats and with independently recomputed ROM bundle hashes. Publication redacted paths in staged Verilog: original SHA256 `46f2da70231c3b3fe1345fb908bf59fff692486dce876928c06c72bb7f9a3e4f` differs from published SHA256 `910c1c4b98cb197be7b06c4cfcc31a249608713b8f1ec79f7667c0cf436a694d`. The manifest declares this; the three published inputs remain mutually byte-identical. Original and published hashes were not conflated.

The manager's 48 static/builder commands and five native commands all record exit 0 at this source and actual base. Reviewed raw results include 55 parent suites, 2,118,264 checks and zero in-suite failures; 54 uncached Yosys PASS records with numeric cells and the structural results; PP-native 14,903 checks with zero failures; gPTP-native completion; and Behave 14 features / 316 scenarios / 1,515 steps, zero failures. Scoped Verilator 5.050 identity is recorded in the public evidence. These are manager execution results, not banks rerun by R247.

The builder's real-report calibration arm is NOT RUN, and four parent field-campaign/freshness skips ran nothing. These provide no physical calibration or hardware proof. Local Yosys/sv2v measurements do not substitute for hosted pinned-tool evidence. No native shared seed is authorized by this report. Acceptance criterion 5 and repository completion remain open for the manager's outstanding workflow, external-review, current-candidate and merge duties.

**Reviewer-owned completion ledger**

Clean means no open BLOCKER, MAJOR or MINOR under that lens for this source change. It does not certify the pending merge workflow.

| Lens | Covering round | Exact covered head |
|---|---|---|
| Conformance | R247-1 CLEAN | `28e350b99ac240a750326b762c6d029f0653362c` |
| RTL | R247-1 CLEAN | `28e350b99ac240a750326b762c6d029f0653362c` |
| Robustness | R247-1 CLEAN | `28e350b99ac240a750326b762c6d029f0653362c` |
| Tests | R247-1 CLEAN | `28e350b99ac240a750326b762c6d029f0653362c` |
| Docs | R247-1 CLEAN | `28e350b99ac240a750326b762c6d029f0653362c` |

Final integrity is in `final-integrity.json`: 852 parent tracked blobs plus all 856 index records verified directly for bytes/kinds/executable modes/stage/object identity, with replacement objects disabled. Required submodule tracked populations were likewise checked: verilog-axis 214 blobs at `48ff7a7e2ef782cf778d47910cf85835c64b1bce`; protocol-processor 222 at `424c688fa2205b934a7689a58f2aa766420f2326`; gptp-processor 103 at `c1b617435824929a790739ea8585c3fe1a328cc0`. All three gitlinks and checkout heads match. The unused optional external submodule was not initialized or used. Final source status is clean. This report is delivered locally for faithful manager publication after terminal execution; R247 published no comment or metadata.

R247-1 FINISHED
