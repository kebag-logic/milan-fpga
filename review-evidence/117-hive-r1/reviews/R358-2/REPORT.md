[R358] POSITIVE - exact head ecd36018a29f605efe790d33dd50382aec9c1201

# R358-2: internal independent delta review of PR #598 (issue #117, acceptance box 4, Hive row)

- **Head.** `ecd36018a29f605efe790d33dd50382aec9c1201`, tree `505fb4868a1b7a8808ca813e4b668582fe72cf11`.
  Base is dev `2a2a7bb655e528edc3087c88033cd3a47546feb4`. The PR head was confirmed by a read-only query (`receipts/pr598.json`).
- **Delta.** `bcba79a5..ecd36018` is one commit. It touches `docs/findings/117_GPTP_SILICON_EVIDENCE.md` only (+53/-15, `receipts/delta-bcba79a5-ecd36018.diff`).
  - The full `2a2a7bb6..ecd36018` diff also touches that file only.
  - The hunks are: header `:6-9`; Contents `:30` and `:33`; box 4 Milan row `:55`; the step 5 Milan row `:464` and the `:469` bullet; B4 `:540-552` and `:633-667`; Raw artifacts `:688-689`.
- **Scope authority.** The round-2 assignment (issue comment 5858871629, items 1 to 4) extends the frozen scope to the header, Contents and the step 5 Milan rows. I also read:
  - the owner decision and assignment (5858063707);
  - the [A376] TAKEN (5858883277) and STOP (5858985706) comments;
  - the coordinator's resolution of item 4 (5858999219).
- **Evidence judged.**
  - The public packet `review-evidence/117-hive-r1`, both at the page's pinned commit `557087b34479c9ba0f1fc1722b6e577a0ecc3998` and at the branch tip `34c3b1d6a4662120c90b26bfb04f16373fcd7710`, which adds `author-r2/`.
  - The upstream library source at `6d61a92e7f264c69f23cdc38f50d31114e567aa0`, with its `nih` pin `d777db8b` and its `json` pin `9cca280a`.
  - Issue #529, PR #534 and exact-head hosted checks, all read-only.
- **Method.** No bench action, no source change, no GitHub write.
- **Verdict.** POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. Six SUGGESTIONs follow; none blocks.

## Round-2 focus checks

### 1. Public pinned B4 locator and redacted hashes: holds

- **Locator.** `:652-654` names branch `117-hive-review-evidence`, commit `557087b3...` and path `review-evidence/117-hive-r1`. `:688-689` points there from Raw artifacts.
  - The `author/` tree is byte-identical at `89aa9f94` (the round-1 packet), at `557087b3` and at the tip `34c3b1d6`.
  - Between `557087b3` and `34c3b1d6`, `MANIFEST.json` changes only to add the `author-r2/` entries (`receipts/packet-commit-deltas.txt`).
- **Hashes.** `scripts/verify_b4_hashes.py` hashes each of the ten B4 table files at the pinned commit (`receipts/b4-hashes.txt`, rc 0 at both commits):
  - Seven match the published bytes.
  - The three entity dumps are the ones `:658-662` lists. Each page hash equals `MANIFEST.json` `original_sha256`, and each published file hashes to `published_sha256`: `7b687748...`, `455e024c...` and `db80b5f8...`.
  - Each published dump carries `"serial_number": "<device-serial>"`, as `:664` states.
- **Stale wording removed.** `grep` for "publication is pending", "pending" and "recorded bytes" finds nothing on the page.
- **Derived values.** The canonical static-tree hash `460b15ac...` and all three inventories reproduce from the published, redacted dumps (`receipts/summarize-on-published.txt`). `enumeration-summary.txt` reproduces byte for byte.

### 2. Dated Milan FAIL, superseded by the `9e9954e9` PASS: holds

- **Where the page says it.**
  - `:464` labels the FAIL as the 2026-09-23 `ede8d48e` record, superseded.
  - `:55` stands box 4's Milan row on the `9e9954e9` PASS and keeps the FAIL as a dated Step 5 record.
  - `:541-548` states the supersession. It gives #534/#529 as a likely cause and says so: "this is observational".
- **Facts checked.**
  - PR #534 "Serve the CRF Stream Input counters on GET_COUNTERS" merged as `50e78097...` (`receipts/pr534.json`).
  - `50e78097` is an ancestor of `9e9954e9` and of the head, and it is not an ancestor of `ede8d48e`.
  - Issue #529 was closed on 2026-09-24 by a comment citing #534's merge (`receipts/issue529*.json`, `receipts/issue529-closing-comment.txt`). "#534 closed #529" is therefore accurate, although GitHub records no closing keyword.
- **"CRF Stream Input 1 counters present" (`:546`).** Each published dump's Stream Input 1 (CRF, format `0x041060010000BB80`) carries exactly ten counters.
  - Those ten are the set the RTL mask `CTR_VALID_CRF_C = 32'h0000_0F3F` claims (`hdl/milan/milan_datapath.sv:3564`), with TIMESTAMP_VALID and TIMESTAMP_NOT_VALID unclaimed (`receipts/stream-input-counters.txt`, `receipts/crf-mask-vs-dump.txt`).
- **Box 4's remaining non-PASS rows (`:550-552`).** They are behave hardware tier, latency (#64/#213) and audio continuity, deferred to 2026-12-31. This matches the table at `:57-59` exactly.
- **Unchanged rows.** Every other NOT RUN line is byte-identical to base and to round 1 (`receipts/not-run-rows.txt`). The only NOT RUN lines removed are the two Hive rows, in round 1. The only sentence changed is B4's own summary line.
- **Header and Contents.**
  - Header `:6-9` dates both images and scopes the bench-step windows to 2026-09-23.
  - Contents `:30` and `:33` no longer say "downgrades" or "two blockers that remain".
  - `:469` is dated.
  - No present-tense Milan statement contradicts another.

### 3. Full default build define and option set: holds

- **Probe defines.** `:635-639` lists nine: `NDEBUG`, `HAVE_FMT`, `IGNORE_NEITHER...`, `CONTINUE_MISBEHAVE...`, `...REDUNDANCY`, `...STRICT_2018_REDUNDANCY`, `...JSON`, `...CBR` and `ALLOW_RECV_BIG...`. These are exactly the `-D` flags in `author/build-provenance.txt`.
- **Library options.**
  - The eleven enabled options, and `ALLOW_SEND_BIG_AECP_PAYLOADS` disabled, equal the feature and compatibility option block of `CMakeLists.txt:47-59` at `6d61a92e` (`receipts/upstream-cmake-options-6d61a92e.txt`).
  - Tag `v4.3.1.1` peels to `6d61a92e` (`receipts/upstream-tag.txt`).
  - The library's runtime self-report in each run log agrees, identically in all three runs (`receipts/run-log-lib-options.txt`). It lists Ignore Invalid Control Data Length, Ignore Invalid Non Success AEM Responses, Allow Get Audio Map Unsolicited, Allow Recv Big, Redundancy and JSON, and the controller options Ignore Neither, Continue Misbehave, Redundancy, Strict 2018, JSON and CBR. Allow Send Big is absent.
  - The controller-target defines follow from the upstream option-to-define mapping (`receipts/upstream-define-mapping-6d61a92e.txt`).
- **Warning qualification.** `:647-648` conditions "no warnings" on that default set, naming `IGNORE_INVALID_CONTROL_DATA_LENGTH`.

### 4. Packet addendum (`author-r2/PACKET-ADDENDUM.md`, coordinator-written): consistent as provenance

- **Include order.** The stated search order is the library `include/`, then `externals/3rdparty/json/include/`, then the probe directory. This matches `BUILD_FLAGS` in round-1 `author/build-provenance.txt`. With that order, every `<la/avdecc/...>` include resolves to the library's own tree first, so the directory can only add headers the library lacks.
- **Pins.** Submodule pins `d777db8b` (nih) and `9cca280a` (json) equal the gitlinks at `6d61a92e`.
- **Counts.**
  - The count of 48 `la/avdecc` headers equals the upstream installed public header set: `PUBLIC_HEADER_FILES` in `src/` and `src/controller/`, with JSON on (`receipts/upstream-public-headers.txt`).
  - The nih `networkInterfaceHelper.hpp` includes only standard headers, so one nih file is self-sufficient.
- **Not checkable here.** I cannot reach the controller host. The per-file inventory behind the aggregate hash `7711cedc...` is therefore not verifiable here; see Limits.
- **Omission list.** It is not exhaustive (S4).

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Docs - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:60` and `:34` - box 5 row and Contents still count two bench packets

- **Evidence.** Box 5 reads "both bench packets are published at a pinned commit ...; [Raw artifacts] gives the locator". Contents `:34` reads "Where the two published bench packets are".
  - The B4 packet is a third published packet, on another branch.
  - Raw artifacts now points to it (`:688-689`), so the claim is not false.
  - These lines were outside the round-2 edit scope.
- **Impact.** A cold reader counting packets from box 5 misses the B4 one on first read.
- **Optional outcome.** In a later docs pass, name the B4 packet in box 5 and Contents.
- **Verification.** Read box 5, Contents and Raw artifacts together.

### S2 - SUGGESTION - Docs, Conformance - `:54` and `:463` - the 2026-09-23 counters-probe and enumeration-statistics rows carry no image or date next to rows that now do

- **Evidence.** `:55`, `:56`, `:464` and `:466` carry image or date labels. `:54` (counters-probe parity PASS) and `:463` (the `ede8d48e` enumeration statistics) do not. Their image follows only from the header `:7-9` and the section.
- **Impact.** Box 4 now mixes rows from two images, and one of its PASS rows is not labelled with its image.
- **Optional outcome.** Label them "2026-09-23, `ede8d48e`" in a later docs pass. They were outside the round-2 scope.
- **Verification.** Every box 4 and step 5 result row names its image.

### S3 - SUGGESTION - Docs - `:656-657` - "original hashes" is ambiguous for `identity-aecp.jsonl`

- **Evidence.** For this file, `author/MANIFEST.sha256` and `MANIFEST.json` `original_sha256` both give `47d165ac...`, the packet bytes after interface-name substitution. `author/redaction.json` records a different pre-substitution `original_sha256` (`d0e6a5f8...`).
  - The page cites `47d165ac...`, and it matches the published bytes.
  - "The identity log" could also mean `identity-uart.txt`.
- **Impact.** A reader comparing the two "original" fields may think a hash is wrong.
- **Optional outcome.** Say that the cited `identity-aecp.jsonl` hash is of the substituted packet file, and name the file.
- **Verification.** `receipts/b4-hashes.txt` stays green.

### S4 - SUGGESTION - Docs - `review-evidence/117-hive-r1/author-r2/PACKET-ADDENDUM.md` at `34c3b1d6` - the omission list is not exhaustive

- **Evidence.** Upstream has 52 non-`.i` files under `include/la/avdecc` and 4 under nih `include/`.
  - With 48 and 1 files present, seven files are omitted.
  - The addendum names four: the umbrella `avdecc.h`, `networkInterfaceHelper.h`, `windowsHelper.hpp` and the virtual-entity interface header.
  - Three omitted C-binding headers go unnamed: `la/avdecc/internals/exports.h`, `la/avdecc/internals/typedefs.h` and nih `internals/exports.h`.
  - The core claims still hold: 49 files, all byte-identical, the include order, and that nothing else is added (`receipts/upstream-public-headers.txt`, `receipts/upstream-nih-headers.txt`).
- **Optional outcome.** Either name all seven, or say the directory equals the library's installed public headers plus `networkInterfaceHelper.hpp`.
- **Verification.** Compare against the upstream lists in the receipts.

### S5 - SUGGESTION - Docs - PR #598 body, "Round 2" item 4 - stale inventory status

- **Evidence.** Item 4 says the inventory "is awaiting an existing receipt". The same body's Status line, and coordinator comment 5858999219, say the inventory is in the addendum (`receipts/pr598.json`).
- **Optional outcome.** Edit the PR body. This is metadata only and needs no new commit.
- **Verification.** Read the PR body.

### S6 - SUGGESTION - Docs - `docs/reference/REGISTER_MAP.md:924`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:230`, `docs/findings/README.md:11` - follow-up: other pages predate the silicon Milan confirmation

- **Evidence.**
  - Two pages still say "Confirmation by a Milan controller on silicon follows the merge (#117)". The B4 PASS and #529's closing comment now record that confirmation.
  - The findings index row describes the page as "on dev `ede8d48e`".
  - All three are outside this PR's frozen scope.
- **Optional outcome.** A follow-up issue or docs pass. This PR should not widen.
- **Verification.** Those lines cite the recorded silicon confirmation.

## Prior public findings at this head

I read my own round-1 findings (R358-1) after my independent pass over the delta. I read the other reviewer's round-1 findings (R359-1) only after writing this round's verdict and ledger (`receipts/independent-verdict-before-prior-findings.txt`).

| Prior finding | Status at `ecd36018` | Evidence |
|---|---|---|
| R358-1 F1 (MINOR) = R359-1 F1 (MINOR): no public B4 locator, "publication is pending", redacted dumps said to keep recorded bytes | RESOLVED | Focus check 1; `receipts/b4-hashes.txt` |
| R359-1 F2 (MINOR): Milan PASS not reconciled with the FAIL; header, Contents `:28`/`:31` and `:467` contradict | RESOLVED | Focus check 2; `:6-9`, `:30`, `:33`, `:55`, `:464`, `:469`, `:540-552` |
| R358-1 S1: no stated reason for the verdict change | RESOLVED (taken) | `:543-547` |
| R358-1 S2: Contents "two blockers that remain" | RESOLVED (taken) | `:33` |
| R358-1 S3 = R359-1 S2: full define and option set, "no warnings" conditioning | RESOLVED (taken) | Focus check 3 |
| R359-1 S3: probe include directory undescribed | RESOLVED in the packet (taken), with one residual wording SUGGESTION | Focus check 4; S4 |
| R359-1 S1: `summarize.py` does not gate diagnostics or statistics | RETAINED as a SUGGESTION, not taken by the coordinator's recorded decision (5858871629) | My probe M5 likewise survives (dynamic fields excluded by design); the page's CRF-counter sentence is checked independently in `receipts/crf-mask-vs-dump.txt` |

## Clean lenses

```text
[R358] PASS Conformance - docs/findings/117_GPTP_SILICON_EVIDENCE.md:6-9,30,33,55,464,469,540-552,633-667,688-689 against issue comment 5858871629 items 1-3; receipts/b4-hashes.txt (10/10 B4 hashes resolve at 557087b3); receipts/pr534.json, receipts/issue529-closing-comment.txt, merge-base 50e78097 < 9e9954e9 and not < ede8d48e; receipts/upstream-cmake-options-6d61a92e.txt and receipts/run-log-lib-options.txt - each required statement is present, dated and true against the public record
[R358] PASS RTL - receipts/scope-and-gitlinks.txt (2a2a7bb6..ecd36018 and 9e9954e9..ecd36018 touch no hdl/tb/config/firmware file; gitlinks unchanged); hdl/milan/milan_datapath.sv:3564 CTR_VALID_CRF_C 0x0F3F against receipts/crf-mask-vs-dump.txt (all three published dumps serve exactly that counter set on CRF Stream Input 1) - no RTL change in the PR, and the page's observational cause is consistent with the RTL the image carries
[R358] PASS Robustness - receipts/summarize-on-published.txt (static tree 460b15ac and inventories reproduce from the redacted dumps, so masking does not break verification); PACKET-ADDENDUM.md include order against author/build-provenance.txt BUILD_FLAGS (library include/ first, so the probe directory cannot shadow library headers); page :647-648 conditions the no-warnings result on the option set, whose tolerant options are named - the degraded and configuration-dependent reading paths are stated and checkable
[R358] PASS Tests - receipts/gates-summary.txt (docs_check, check_doc_style, gen_toc --check, check_em_dash --base 2a2a7bb6 over 161 added lines with arms 339/339, check_doc_paths, ci_scope --selftest, check_baremetal_only --check, git diff --check: all rc 0 at the head); receipts/mutation-probes.txt (control green; hash change, undeclared redaction, published-byte change and a dropped Milan flag all turn red; M5 survival explained) - the delta adds no test; its evidence checks can fail for the defects they cover
[R358] PASS Docs - page delta (receipts/delta-bcba79a5-ecd36018.diff), Contents regenerated and gen_toc --check green, em-dash gate green, docs_check identity/privacy scrub 0 findings; author-r2/PACKET-ADDENDUM.md (receipts/PACKET-ADDENDUM.as-read.md); PR #598 body - accurate; S1-S6 are optional improvements only
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5858871629 items 1 to 4 and owner decision 5858063707. Page `:6-9`, `:30`, `:33`, `:55`, `:464`, `:469`, `:540-552`, `:633-667` and `:688-689`. B4 hashes at `557087b3`. #534 and #529 records, with ancestry. Upstream options at `6d61a92e` | R358-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| RTL | CLEAN | Name-only diffs from the base and from the image commit to the head. Gitlinks. `hdl/milan/milan_datapath.sv:3564` mask against the published dumps | R358-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Robustness | CLEAN | Redacted-dump recompute. Addendum include order against `build-provenance.txt`. Option-set conditioning with the runtime option self-report | R358-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Tests | CLEAN | Eight docs gates, all rc 0. Mutation probes M0 to M5. NOT RUN row comparison | R358-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Docs | CLEAN (S1 to S6 SUGGESTION only) | Page delta, Contents and header. Packet addendum. PR body. Docs and hygiene gates | R358-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |

## Limits

- **Bench.** I had no bench or controller-host access. The round-2 addendum's per-file header inventory and its aggregate hash (`7711cedc...`) are coordinator statements. I judged them for consistency with the round-1 include order and the upstream header sets, not by reading the directory.
- **Simulator.** The scoped simulator was not used. The path the assignment named does not exist on this host, and the delta has no RTL or test-bench change. The CRF counter RTL was inspected statically, not simulated.
- **Binaries.** The library and probe binaries, the bitstream and the AEM image were not rebuilt in this round. Round 1 covered the AEM image. The identity of the other binaries rests on their recorded SHA-256 values and on the library's runtime self-report.
- **Gate interpreter.** `check_baremetal_only.py` first failed with rc 2 under the markdown-lock virtual environment, which lacks `pyyaml`. That is an environment failure, not a finding. It returned rc 0 under the system interpreter (`receipts/gates/baremetal_only_system.txt`).
- **Hosted checks at 19:33Z (read-only).**
  - Completed with success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0 to 3, and Verilator shards 0 and 3.
  - Still in progress: `docs-check` and Verilator shards 1, 2 and 4.
  - Skipped, which is not execution: Physical gPTP (`receipts/hosted-check-runs-2.txt`).
- **Physical scope.** Physical calibration is NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- **Hosted and local-replica acceptance at the exact head.** `docs-check` and three Verilator shards had not finished when I checked.
- **Merge turn.** The manager still owns:
  - the final current-dev candidate build and validation (source base `2a2a7bb6`, live dev `6d5ebd73...`);
  - post-merge containment;
  - the second independent verdict (R359-2);
  - maintainer merge authorization.
- **Issue state.** Acceptance box 4 keeps its NOT RUN rows: behave hardware tier, latency #64/#213, and audio continuity deferred to 2026-12-31. Issue #117 stays open.
- **Follow-ups.** S1, S2 and S6 are optional follow-ups outside this PR's frozen scope.

## Receipts and restoration

- **Scripts** (portable; paths are passed as arguments):
  - `scripts/verify_b4_hashes.py`
  - `scripts/run_doc_gates.sh`
  - `scripts/mutation_probes.sh`
- **Receipts.** They are under `receipts/`. Every published file is listed in `MANIFEST.sha256`.
- **Clone restoration** (`receipts/clone-state-after.txt`).
  - HEAD `ecd36018` and tree `505fb486` are unchanged.
  - The index listing (mode, blob, path) equals the HEAD tree listing. Every tracked blob rehashes to its index entry, and the executable bits match the index modes.
  - All four gitlinks are unchanged: `external` `efeb541a` (uninitialized; this round ran no submodule command), `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e`.
  - The `scripts/__pycache__` my gate run created was removed. That leaves 0 untracked or ignored entries.
- **Scratch.** Disposable trees (packet extractions, upstream sources, the markdown-lock environment, mutants) stayed under `scratch/` and are not published.

R358-2 FINISHED
