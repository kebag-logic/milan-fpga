[R880] NEGATIVE - exact head 9413958c66c0dcd632b3e0e7ac44505314fed41a

External independent review of issue #665 / PR #960, round R880-2.
Tree: `83b2c214071b7f3f74c0eda10048ec674e3d5fdc`.
Source base: `59b098841b1e2826aaf7a38b557faa5345f91c82` (`dev-soft-core`).
Delta reviewed: `62477be4cb90336ca9b59ae7ab8377546e72557a..9413958c66c0dcd632b3e0e7ac44505314fed41a`, seven commits, twenty paths.

All five lenses were applied. The sweep placement, harness argument replacement, header accounting and documentation fixes check out. R880-1-F2 remains open: five identity operands are absent from the published Git tree, although the inner manifest lists them. The advertised replay fails and cannot complete its eleven mutation controls. A separate PR reproduction command names an absent branch.

**Scope and authorities**

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, #665's body and public decisions, REQUIREMENTS section 1, NFR-SCOUT-01/02/03/07, ARCHITECTURE_HW_SW_SPLIT section 7, MAILBOX_SPLIT's identity contract, the source diff/history, then executable evidence. The independent delta pass preceded the required prior-public-findings reconciliation. No unpublished author material or current-round reviewer report was used.

Public scope decisions examined: #665 comments 6410301079, 6799253003 item 6, 6845315282, 6930885185 and 7044585511. The bench re-check is comment 7063917242; the assignment and corrected REVIEW READY are 7065258935 and 7072252167. The two qualified AX7101 one-interface shapes become split-default; all-fabric remains explicitly selectable. Processor deletion, full release qualification and optional two-interface performance remain separate. NFR-SCOUT-02's end-state wording is unchanged; its reconciliation remains an owner duty, not an assertion of full qualification by this review.

The public operand packet is [491ffed7, review-evidence/s13-r1](https://github.com/kebag-logic/milan-fpga/tree/491ffed7fa0a1e1f502606a7bc23d2cecfce5127/review-evidence/s13-r1). All evidence paths below are relative to that directory unless explicitly local. PR metadata independently confirms the requested head and source base.

**R880-2-F1 / retained R880-1-F2 | MAJOR | Conformance, Tests, Docs**

Artifact: `author-r2/receipts/identity/MANIFEST.sha256`; `tools/replay.py:74`, `:355`, `:450`; the published Git tree at `491ffed7`.

Authority/evidence: the frozen validation plan carries the bench evidence only after complete image identity. The five files below are named by the inner manifest but absent from the pinned public Git tree:

- `shipping/1x1/dump/bench.cells.xz`
- `shipping/1x1/dump/flip.cells.xz`
- `groups/1x1/declaring-outputs/aecp-outputs.measured.log.gz`
- `groups/8x8-1if/declaring-outputs/aecp-outputs.head.log.gz`
- `groups/8x8-1if/declaring-outputs/aecp-outputs.measured.log.gz`

These are not extraction failures: `published-identity-tree.txt` records the actual tree inventory. The outer publication manifest verifies all 365 examined author entries but does not supply the five missing inner-manifest operands. The inner manifest expects 224 files; only 219 are present.

`python3 -I tools/replay.py <identity>` exits 1: it reports the missing manifest files and 1x1 cell dumps, then raises `AttributeError` when the first missing group log is opened. The unmodified `rmutants.py` exits 1 after the fifth mutation encounters the missing flip cell dump. The first control prints MISSED for its intended frame/INIT check; the part-name, instruction-byte and ROM-word controls reach their named failures. The placement control cannot be applied; the remaining six are not reached. This is not an eleven-control pass. See `replay.log`, `replay-plants.log`, their return-code files, and `independent-identity.log`.

Impact: complete 1x1 cell/INIT identity and two groups' complete raw-log comparisons cannot be independently checked. The supplied success transcript describes a more complete packet than the published one. The review cannot yet accept the full bench/CPU evidence carry. This does not demonstrate an unintended product change.

Required outcome: publish the five exact hash-matching operands, update the outer manifest, and identify the corrected immutable evidence commit. If they cannot be recovered, provide equivalent complete operands with explicit provenance. Replay must pass from that publication, followed by all eleven named mutation controls. No source change or full 64-part CPU re-measure is intrinsically required to close this publication defect.

Verification: repeat `independent_identity.py`, the unmodified replay, and all mutation controls on the corrected publication. Complete both shapes' cell/route/INIT comparison and all thirteen groups' JSON/raw-log comparison. Existing positive comparisons below need not be re-measured.

**R880-2-F2 | MINOR | Docs**

Artifact: PR #960 body, “How to get into the same state,” first command; `pr-metadata.json` and `pr-branch-check.txt`.

Authority/evidence: CONTRIBUTING and the Docs lens require a reproducible public review object. The command says `git fetch origin s13-flip-default && git checkout --detach FETCH_HEAD`. The remote advertises only `665-s13-flip-default` at the reviewed head; no `s13-flip-default` branch exists.

Impact: the published checkout recipe fails before obtaining the candidate. This is an executable reproduction error, not merely a descriptive label, so it is recorded as MINOR rather than wording-only residue.

Required outcome: replace the command with an exact-head fetch, preferably `git fetch origin 9413958c66c0dcd632b3e0e7ac44505314fed41a && git checkout --detach FETCH_HEAD`, or the actual branch plus an explicit head assertion.

Verification: the public recipe resolves to the reviewed full SHA in a fresh clone. No implementation or gate rerun is needed for this PR-text correction.

**R880-2-S1 | SUGGESTION | Tests**

Artifact: public `author-r2/receipts/identity/tools/rmutants.py:125`, `:131`.

Evidence: each result stores `hit or fails`, then the total counts any nonempty stored list. Consequently a non-target failure can count as caught even when that case prints MISSED. The first attempted mutation in this review demonstrates the distinction: its published marker is absent, but unrelated failures are nonempty.

Impact: the summary alone does not prove that each claimed semantic check rejected its plant. Current acceptance is already withheld by F1; this suggestion strengthens future diagnostics.

Suggested outcome: retain the explicit named-marker match separately; count only it, and require an unplanted successful replay before mutation grading.

Verification: a synthetic nonzero replay containing only an unrelated failure must print MISSED and fail the mutation aggregate.

**Prior finding reconciliation**

| Prior item | Disposition at this head | Evidence at its cause |
|---|---|---|
| R880-1-F1, MAJOR, Robustness/Tests | RESOLVED | `soc_sweep.py:65`, `:104`, `:133`; `sweep_plan.json` names all-fabric. Real builder/prepare probe succeeds with no ELF at all-fabric and refuses split before the export loop. Three self-test plants are caught. Published `f1/rsweep-a9da4c48.txt` records fresh ship and axilite exports with zero pre-existing platform images and all six expected refusals; `exports-a9da4c48.json` agrees. The only later source commit regenerates the docs inventory. |
| R880-1-F2, MAJOR, Conformance/Tests/Docs | RETAINED as R880-2-F1 | Most operands now exist and agree; the five absent files prevent complete replay. |
| R880-1-F3, MINOR, Tests/Docs | RESOLVED | Independent parsing of both complete `.bit` headers names every changed byte by field; corrected REVIEW READY uses those counts. |
| R880-1-F4, MINOR, Tests/Docs | RESOLVED | `MAILBOX_SPLIT.md:1808` explicitly exempts ENTITY firmware_version in `aem_overlay.json` and `aecp_aem_rom.svh`, matching gate 23o's `RECIPE_VERSION_ARTIFACTS`. Other shape equality and no tracked writes remain stated. |
| R879-F1, MINOR, Docs | Label defect RESOLVED | `register_page.py:519`, `:652`, `:714`; `REGISTER_MAP.md:151`, `:243` label all-fabric provenance, point to split memory layout, and state split CTRL_SPLIT_P=1. Regeneration and 61/61 controls pass. The requested public follow-up Issue for re-recording the split map remains a manager duty. |
| R879-F2, MINOR, Docs | RESOLVED | `BUILD_FLASH_BOOT.gen.py:22`, `:90`; README:298 names the split ELF prerequisite, ROM boot and major 3. Picture explicitly selects all-fabric and major 2. SVG, PNG and drawio regenerate byte-identically; the rendered picture was inspected. |
| R879-S1, Tests/Robustness | IMPLEMENTED | `build.py:355`, `:382` removes the old pair and supplies exactly one harness image. Both-shape checks pass; append-old-pair and keep-config-image plants both fail at both shapes. Empty, repeated and dangling-flag inputs were also checked. |
| R880-1-R1; R879-R1 | RESOLVED | ARCHITECTURE:4/19, FULL_FPGA_SOLUTION:3/19, MAILBOX_SPLIT:5/626 and MILAN_COMPLIANCE_MATRIX:6 now use the requested wording. |

The source self-tests and probes are in `focused_delta.py`, `focused-delta.log`, `soc-selftest.log` and `harness-checks.log`. The prepare probe suppresses only the unrelated archival Git bootstrap; it executes the real builder and prepare logic, and performs no SoC export. Actual fresh ship/axilite export execution and six refusal outcomes are the inspected, hash-verified author receipts, not new executions claimed by this review. Their base comparison preserves argv and gateware outside comments; the AXI-Lite XDC clock-group pairs are equal as a set, with every other line ordered and equal.

**Independent identity results and limits**

`independent_identity.py` imports none of the author's replay logic. It compares complete bytes, parses headers/ELF structures, reconstructs load maps, checks every JSON value and records each available log difference.

| Artifact | 1x1/1if | 8x8/1if |
|---|---|---|
| Whole bitstream delta | 103 bytes | 93 bytes |
| Header design name | SW_CRC 8 + SW_HDR_SHA256 63 = 71 bytes | SW_CRC 8 + SW_HDR_SHA256 61 = 69 bytes |
| Header date / time | 1 / 5 bytes | 1 / 4 bytes |
| Payload changes | CRC register 4 bytes; frame data 22 bytes / 22 bits | CRC register 4 bytes; frame data 15 bytes / 15 bits |
| Complete platform ELF | Exactly 6 loaded bytes; identical layout, symbols and remaining bytes | Exactly 6 loaded bytes; identical layout, symbols and remaining bytes |
| AEM CRC | 38a80323 -> db1deab5 | d6dd74b9 -> b730ec91 |
| ROM initialization | All 5 banks equal ELF segments, gaps and zero padding | Both banks equal ELF segments, gaps and zero padding |
| Routes | All 95,172 byte-identical | All 119,085 byte-identical |
| Cells | UNPROVED: missing dumps | 109,093 names/types/placements equal; only 15 INIT bits in 14 CSR/firmware ROM cells; separate 111-BRAM dump agrees |

The six firmware bytes are five bytes in the LUI/ADDI pair loading the independently computed descriptor CRC and the ENTITY firmware digit at descriptor offset 0x184, 2.96.0 -> 3.96.0. The opcodes and layout are unchanged. Each embedded descriptor equals its exported `aem_desc.bin`.

All 16 harness image pairs have that same six-byte classification and equal group partitions. All 13 group result JSON pairs are equal, including slash-bearing summary strings; none is excluded. Eleven complete raw-log pairs are available. Every difference in those logs is the ENTITY version digit in the transmitted bytes and corresponding mailbox word, with exact contexts retained in the receipt. The other two log comparisons remain unproved.

The export differences were independently enumerated: descriptor CRC, AEM SHA-256, bitstream payload hash, manifest VERSION/ELF hash, and the csr.csv generation timestamp. Descriptor maps, descriptor JSON and memory initialization otherwise agree. Bitstream part and payload length are identical. Header dates/times and SW_CRC/SW_HDR_SHA256 text are nonloaded metadata; this review does not claim to derive the vendor header digests' undocumented algorithm.

The 19/16-input carry receipts bind the routed-image build at `822e3af0` to `a9da4c48`; the last commit changes only DOCUMENTATION_AUDIT.md. There is no delta in RTL, builder, LiteX, configuration, descriptor-generation or firmware paths since the preceding reviewed head. These are source/receipt checks, not new image builds. The packet is hash-bound to a public immutable commit and published image identities. No commit signature or detached signature was supplied at this publication; no cryptographic signature verification is claimed.

**Documentation checks and remaining wording**

At this head, independent docs-check, style, paths, solution-docs, em-dash, register regeneration and register self-test pass. The diagram's three outputs reproduce exactly. The inspected author's exact-head docs-workflow receipt reports 99/103 commands passing; its four failures are the isolated runner install-directory row and three missing-event-environment rows. Those are not silently converted into executed passes here. No new prohibited lane/reviewer/comment identifier was found in added source comments.

R880-2-R1 | RESIDUE | Docs | `docs/reference/FR_NFR.md:173`, `docs/fpga/FPGA_DESIGN.md:313`, `docs/testing/TESTING.md:731`.

Evidence/impact: the author disclosed three remaining “shipping allocator” labels for KL_maap. These describe the retained all-fabric implementation; the split's MAAP ownership and Annex B claims are not changed by the label correction. Exact fix: in each of these three sentences replace “shipping allocator” with “all-fabric allocator.” Leave every clause, status, gate and behavioral claim unchanged. Verification: inspect these three substitutions and run the docs gates. This wording-only residue does not unclean a lens and goes to the manager's residue checklist. FR_NFR section 2.0 already scopes its implementation ledger to all-fabric; this proposal does not amend a normative MAAP requirement.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R880-2-F1) | #665 frozen decisions; REQUIREMENTS s1; NFR-SCOUT-01/02/03/07; split architecture s7; both shipping images, ELFs, ROMs and public bench/CPU identity operands | R880-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| RTL | CLEAN | `milan_csr.sv:2002`, `milan_datapath.sv:2850`; seven-commit path diff; complete ROM load comparisons and available routed dumps. No RTL or RTL-input change since R880-1's integrated clean/mutated VERSION checks | R880-2, carrying unchanged R880-1 RTL evidence | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| Robustness | CLEAN | `soc_sweep.py:65/73/104/133`, plan and three refusal plants; `build.py:355/382`, both shapes and two plants; fresh author export/refusal receipt; focused-delta.log | R880-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| Tests | UNCLEAN (R880-2-F1; S1 optional) | Changed sweep/harness self-tests; both bitstream and 18 ELF-pair comparisons; 13 group JSON pairs; replay and mutation driver; missing-file inventory; gate 23o exception | R880-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| Docs | UNCLEAN (R880-2-F1/F2; R1 residue) | MAILBOX_SPLIT identity; register generator/page; README pipeline source/rendered files; public REVIEW READY, PR recipe, packet manifests; independent docs gates | R880-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |

[R880] PASS RTL - `hdl/common/csr/milan_csr.sv:2002`, `hdl/milan/milan_datapath.sv:2850`, `delta.patch` - the placement-bound VERSION change and its consumers are unchanged from the preceding reviewed head; no new clock, reset, CDC, width, state or backpressure behavior enters this delta. Binary identity evidence limitations remain under F1's evidence lenses.

[R880] PASS Robustness - `syn/resmap/soc_sweep.py:104`, `tb/verilator/ctrl_service_budget/build.py:355`, `focused-delta.log`, public `f1/rsweep-a9da4c48.txt` - missing-image refusal precedes export; intended all-fabric preparation and both harness image replacements hold, with defect-detecting controls.

**Real limits and manager duties**

No manager source bank exists at this exact head and none is inferred. Full source execution evidence is the author's published receipts. This round ran focused checks only, no full parent/processor/gPTP/Yosys/builder banks, no simulator campaign, no hardware or route build, no local workflow runner, and no hosted acceptance. The preceding RTL verdict stands on unchanged source. Physical calibration NOT RUN, bench-blocked replays, field skips and known bench defects remain those outcomes; identity never upgrades them to hardware passes. #954 and the other explicitly post-flip work keep their public dispositions.

The manager must publish the missing evidence and arrange focused re-review, correct the PR recipe, open/link the split-register-map follow-up requested by R879-F1, carry the residue, and obtain the independent review bar. The current-dev candidate against `e275d7950ef3385753e6a15d2e191ba855b171ed` still needs the manager's builder/native evidence, required hosted/local acceptance, explicit merge authorization and post-merge containment. This source review does not certify that candidate or complete issue #665.

The first register runs used an interpreter lacking the renderer package; they failed setup. The equipped interpreter passes regeneration and 61/61 controls. The first archival prepare probe omitted the required gPTP generator; after extracting the pinned submodules into scratch, it passes. Initial logs are retained; these setup failures are not product findings. No shared installs were performed.

`tree-integrity.log` verifies all 1,935 parent files directly against committed blob bytes and modes, exact index equality, all six gitlinks, and raw files/modes/index of all five initialized submodules. The optional external checkout remains absent. No source fix, source commit, push, GitHub write or merge was made. Scratch trees are excluded from publication. Receipt path substitutions are documented in `receipt-normalization.json`; only REPORT.md and MANIFEST.sha256-listed files are publishable.

R880-2 FINISHED
