[R221] NEGATIVE - exact head d81a302760b84f32d2aa019643f57682bb6e052c

R221-1 independently applied Conformance, RTL, Robustness, Tests, and Docs to parent issue #478 / PR #512. One MAJOR finding remains open. The loader implementation and its focused tests satisfy the frozen functional acceptance; the added documentation link breaks two required documentation jobs. This verdict does not approve a later correction or authorize merge.

Reviewed tree: `4903a00f30752bc86a99e9bf112ff5ad01827c5d`. The review checkout and its three required submodules passed initial and final index/blob/kind/mode verification. No source fixes, commits, pushes, public messages, metadata changes, other agents, hardware operations, installations, privileged operations, Docker/act execution, or full native RTL/Yosys reruns were performed by R221. Executable probes used isolated scratch sources. No parallel compilation was used.

The review was reconstructed from candidate AGENTS/CONTRIBUTING, [issue #478](https://github.com/kebag-logic/milan-fpga/issues/478), its public decisions and author/manager evidence, linked standards, pinned processor documents, parent architecture/interfaces, the PR diff/history, and executable artifacts. No private author reasoning or other reviewers' reports were read. The manager's later documentation-failure notice was read during review; the finding below was then independently reproduced.

[R221] MAJOR Docs - `docs/ENDSTATION_BUILDER.md:963` - F1: new L10 link fails without initialized processor files.

[R221] MAJOR Conformance - `REQUIREMENTS.md:222`, `.github/workflows/docs.yml:52`, `.github/workflows/docs.yml:451` - F1: required documentation gates do not satisfy REQ-VER-04.

[R221] MAJOR Robustness - `docs/ENDSTATION_BUILDER.md:963`, `.github/workflows/docs.yml:444` - F1: the reference depends on a populated submodule in supported Git and archive checkout configurations.

[R221] MAJOR Tests - `.github/workflows/docs.yml:52`, `.github/workflows/docs.yml:451` - F1: existing required documentation checks regress; initialized native validation masks the failing configuration.

These four lines attribute one defect to every affected lens; they are not four independent defects.

Requirement/evidence: REQ-VER-04 requires green documentation and artifact gates. `docs-check` runs `python3 scripts/docs_check.py` before the submodule fetch at workflow line 129. `docs-check-no-git` removes Git metadata and runs the same gate without fetching submodules. The newly added relative link points into `protocol-processor/`. `scripts/docs_check.py:642` resolves local links against files actually present.

Independent reproduction, using the unchanged checker and unchanged candidate document:

| Scratch population | Exit | Result |
|---|---:|---|
| Exact head, Git metadata, no submodules | 1 | One broken link at `docs/ENDSTATION_BUILDER.md:963` |
| Exact head, no Git metadata, no submodules | 1 | Same single broken link |
| Integrated base `ec34fcde`, no Git metadata, no submodules | 0 | Zero findings |
| Exact head, Git metadata, pinned processor files populated | 0 | Zero findings |
| Exact head, no Git metadata, pinned processor files populated | 0 | Zero findings |

Receipts: [docs-probe results](receipts/docs-probe/results.json), [complete probe output](receipts/docs-probe.log), and [reproducer](docs_probe.py). No document correction was applied in these controls. Populating the existing pinned files alone changes the result.

Both hosted failures corroborate this: [docs-check](https://github.com/kebag-logic/milan-fpga/actions/runs/35723340746/job/106731058055) and [docs-check-no-git](https://github.com/kebag-logic/milan-fpga/actions/runs/35723340746/job/106731058157). Their check-run metadata is associated with source head `d81a3027`; their actual checkout was GitHub merge commit `9fea8a3cf41d3d996155aaca7a3aa1c167c057cf`, tree `5aa23f2ce461b9671619221412ab50699942292c`, with parents `88e9276b` and `d81a3027`. That tree matches the manager's newer candidate tree. R221's separate probes establish the failure directly at the requested source head. Downloaded logs and commit metadata are retained under `receipts/hosted-docs-*`.

Impact: the authoritative builder reference is unavailable in the supported uninitialized checkout/archive populations, and the head cannot meet the protected documentation merge bar. The failure does not change emitted rates or establish an RTL defect.

Required outcome: make the reference usable without local processor initialization while retaining the existing `424c688fa2205b934a7689a58f2aa766420f2326` authority and L10 meaning. A link to that exact public processor revision fits the manager's bounded correction. Do not weaken the checker or expand initialization/workflow scope to conceal the defect.

Verification: independently rerun the documentation gate in Git and no-Git checkouts with no initialized submodules, verify the exact pinned destination and section anchor, and require successful corrected-head hosted documentation checks. The corrected commit also owes the repository's remaining validation and re-review duties. F1 remains open until the correction is examined; the manager's proposed fix is not evidence that it has landed.

The frozen functional contract was checked as follows.

- The [readiness decision](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770832729) and [assignment](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5770949009) require the eight-entry loader boundary, independent distinct-ninth and duplicate refusals, unchanged order/defaults/shipping rates, and a comparison of the deliberate `pp_shadow` literal array's values and declared length against YAML. They do not require eight arbitrary rates to pass stream-format generation or run on hardware.
- Pinned processor `docs/architecture/07_memory_maps.md:92` states L10: offset 144 and at most eight complete sampling-rate words. `docs/architecture/06_aecp_engine.md:346` and `hdl/aecp/ucode/gen_ucode.py:1330` corroborate the immediate-address walk, whole-word comparison, and refusal beyond the walk. The parent pin remains `424c688`; advanced donor main is not the reviewed dependency.
- Milan v1.2 section 5.3.3.3 requires truthful supported rates and current-rate membership. IEEE 1722.1-2021 section 7.2.3/Table 7-5 defines offset 144 and permits up to 91 entries; eight is this processor's narrower integration contract, not the IEEE maximum. Section 7.4.21.1 defines the sampling-rate command/response value. Local standards were read directly; their identities and paraphrased conclusions are in [standards receipt](receipts/standards.json).
- `sw/builder/endstation_builder.py:1197` places the sole production `MAX_AUDIO_UNIT_RATES = 8` beside `BASE_RATE_HZ` with its L10 reference. Lines 3788 and 3801-3810 preserve integer normalization, apply the named count bound, reject duplicates, and retain current-rate membership. Neither sorting nor truncation is introduced. Omitted lists still become the current rate. A list violating both count and uniqueness receives the count refusal first; the separately distinct ninth-entry fixture cannot be masked by duplicate detection.
- `sw/builder/test_builder.py:23524` uses a literal eight-entry oracle independently of the implementation constant, unsorted entries, and the current rate last. Five negative cases check their causes. R221 ran all three gate-36a functions, 115 additional loader checks, seven independent loader mutations, and five changes to the actual scratch C++ declaration. All expected refusals occurred. The mutations covered bounds nine/seven, missing count/duplicate/membership checks, reversed order, wrong default, and C++ value/order/length/initializer/comment drift. See [focused results](receipts/focused/focused-results.json) and [output](receipts/focused.log).
- `sw/builder/test_builder.py:23957` includes all three new functions in the normal main-loop dispatch. R221 executed that exact loop with unrelated gates explicitly stubbed: all three real gates ran, and each independent assertion sentinel propagated. This is dispatch evidence, not a complete builder-suite rerun. The manager's full builder log separately records all three executing in the unmodified normal run.
- `sw/builder/test_builder.py:23590` compares the literal C++ declaration after removing comments, requires one declaration, checks its declared length and ordered literal values, and rejects missing initializer elements. `tb/verilator/pp_shadow/sim_main.cpp:827` remains the three-entry hand-built array; lines 876-881 actually use it in the hand-built AUDIO_UNIT. The source and Makefile are unchanged. Its existing five control fixtures pass their expected refusal checks. No generated-header requirement was invented.
- The eight-entry loader fixture fails downstream image generation with `unsupported sampling rates`, as expected from `avdecc/aem_specs.py:219`. The change does not widen that consumer's 48/96/192 kHz restriction or claim runtime-rate support. Parent #399's per-rate planned marks remain outside this repair. Public PP89 and parent #509 explicitly keep generic offset/count/length/L6 enforcement and wider ownership decisions outside #478.

R221 independently ran builder gate 1 for all five shipping configurations and gate 32 for the schema key map; both passed. The schema census still discloses 17 untaken loader arms and is not claimed as exhaustive execution of those arms. R221 also generated and independently decoded every complete packed image, checking AEMI header/checksum/length, AUDIO_UNIT length/offset/count/current rate, and ordered rate words.

| Shipping configuration | Advertised rates (Hz) | AUDIO_UNIT bytes | Complete `aem_desc.bin` bytes |
|---|---|---:|---:|
| `endstation_arty_current.yaml` | 48000, 96000, 192000 | 156 | 5792 |
| `endstation_arty_4x4.yaml` | 48000 | 148 | 10112 |
| `endstation_arty_8ch.yaml` | 48000 | 148 | 15360 |
| `endstation_ax7101_8x8.yaml` | 48000 | 148 | 18288 |
| `endstation_ax7101_1x1_tdm8.yaml` | 48000 | 148 | 7352 |

Every list starts at offset 144 and every current rate is 48000. All five configuration hashes and all five entire packed images match independently generated original-base `b17580b9` outputs, byte for byte. Their hashes also match the author's original `099e191` receipts. This establishes equality of those YAML files and complete `aem_desc.bin` files only; it does not establish equality of every generated artifact, bitstream, deployed image, or hardware behavior. See [image comparison](receipts/image-and-archive-comparison.json), [current images](receipts/current-images/images.json), [base images](receipts/base-images/images.json), and [shipping builds](receipts/shipping-builds.log). Gate 36a itself asserts the shipping rate fields, not whole-image equality against a historical baseline.

[R221] PASS RTL - `avdecc/aem_descriptors.py:240`, `hdl/milan/KL_pp_shadow.sv:439`, `tb/verilator/pp_shadow/sim_main.cpp:827`, pinned `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1330` - producer layout, descriptor-memory boundary, deliberate integration image, and eight-entry consumer walk agree for this change. `docs/overview/ARCHITECTURE.md:59` and `docs/integration/INTEGRATION_GUIDE.md:78` were checked against those artifacts. The exact three-file issue diff changes no RTL, ports, clocks, resets, CDC, FSM, backpressure, timeouts, firmware, generator implementation, shipping configuration, or submodule gitlink. New cycle-level stress tests are therefore inapplicable to this delta; this is not a fresh whole-product RTL certification.

Evidence identity and limits:

- The complete binary diff `b17580b9..099e191` is byte-identical to `ec34fcde..d81a3027`, SHA-256 `f072ec203633281a03ef10331e934a50bf0713091cd2b54bc28cd48391906ad6`. Only the two builder Python files and `docs/ENDSTATION_BUILDER.md` belong to the issue patch. Integration from the author head changed only `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md` through #505. See [diff identity](receipts/diff-identity.json).
- R221 downloaded 196 files from the immutable [b671cc6 author/manager archive](https://github.com/kebag-logic/milan-fpga/tree/b671cc625534af2d50f91f1fd0f8dac1ab49c991/review-evidence/478-r1), verified their Git blob IDs, and verified all 195 published manifest entries. All 73 entries in the earlier `00ffa6bd` manifest are identical in the later archive. Public hashes are verified; original pre-neutralization hashes are retained assertions, not an independent comparison to private files.
- The [completed native comment](https://github.com/kebag-logic/milan-fpga/issues/478#issuecomment-5775843006), command/result/completion records, logs, and both integrity receipts consistently identify `d81a3027`, tree `4903a00f`, against `ec34fcde`. They record 40 static/builder commands and five native commands exiting zero. The parent sweep records 55/55 suites and 2,118,264 checks; the pinned PP suite records 14,903 checks; the parent `pp_shadow` log records 371 checks; behave records 316 scenarios. Yosys and the gPTP suite have successful completion records. These are independently inspected manager executions, not R221 reruns.
- The native pass remains accurate for its initialized source-head population. It does not supersede F1 or certify the newer current-dev candidate. Four field-campaign skips contribute zero checks. Builder gate 11's absent calibration-report arm remains NOT RUN. Neither is hardware evidence. R221's first scratch probe attempt omitted the gPTP dependency and failed setup; those logs are retained, and only subsequent fully populated runs are counted.
- The latest inspected [manager cleanup comment](https://github.com/kebag-logic/milan-fpga/pull/512#issuecomment-5776057482) records runner exit 130 and wrapper exit 1 after supported SIGINT cleanup. The local replica is not a pass. It also records that both newer candidate native units were stopped and their partial results superseded. PR #512 was draft, source still `d81a3027`, and dev still `88e9276b2a220c716f64a843f7e1eb8f9265e896` at the final public-state observation. Completion/cleanup here is attributed to the manager's public record, not to direct R221 process inspection.

Reviewer-owned coverage ledger:

| Lens | Covering round | Exact head | Coverage |
|---|---|---|---|
| Conformance | R221-1, applied | `d81a302760b84f32d2aa019643f57682bb6e052c` | UNCLEAN: F1 open |
| RTL | R221-1 | `d81a302760b84f32d2aa019643f57682bb6e052c` | CLEAN |
| Robustness | R221-1, applied | `d81a302760b84f32d2aa019643f57682bb6e052c` | UNCLEAN: F1 open |
| Tests | R221-1, applied | `d81a302760b84f32d2aa019643f57682bb6e052c` | UNCLEAN: F1 open |
| Docs | R221-1, applied | `d81a302760b84f32d2aa019643f57682bb6e052c` | UNCLEAN: F1 open |

Open findings: F1 only, MAJOR under the four lenses above. No MINOR or optional SUGGESTION findings are filed. Clean functional subchecks do not clear those lenses while F1 remains open.

Outstanding manager obligations: implement and validate the bounded reference correction in the authorized lane; publish exact corrected-head evidence; obtain independent re-review and the required two positive verdicts with reviewer-owned clean coverage; finish the required native, trusted replica, and hosted checks on their proper identities; validate the candidate against then-current dev. The stopped `443c46acd8a53177aec61e7c9619ce42a3e8ee8b` candidate, tree `5aa23f2ce461b9671619221412ab50699942292c`, supplies no completed full candidate bar. Any further dev movement requires the actual new candidate to be validated. Wait for all review rounds, obtain explicit maintainer merge authorization, verify actual merge containment, and only then close/move the issue to Done. Manager publishes this factual report with public path neutralization; R221 does not self-publish.

Final integrity: all 850 parent tracked files, 222 processor files, 103 gPTP files, and 214 verilog-axis files match their commit blobs and kinds/modes; each index matches its tree and each initialized submodule matches its gitlink. Initial and final snapshots are identical. The optional unused `external` import remains uninitialized. [Initial receipt](receipts/integrity-initial.json), [final receipt](receipts/integrity-final.json), [reproduction instructions](RECEIPTS.md).

R221-1 FINISHED
