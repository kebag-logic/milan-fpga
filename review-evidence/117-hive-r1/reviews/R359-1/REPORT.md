[R359] NEGATIVE - exact head bcba79a50ecd2eca99db91c4f3802d888eaac7e4

# R359-1: external review of PR #598 (issue #117, acceptance box 4, Hive row)

- Head `bcba79a50ecd2eca99db91c4f3802d888eaac7e4`, tree `b9db4da38ef2d848930ea76c3a0b215cfb309657`, one commit on dev `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
- Diff: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` only, +116/-3.
- Evidence read: `review-evidence/117-hive-r1` at `89aa9f94ffe46cf7fa9df54376d26771e118f103`.
- Scope authority: the issue #117 body, the owner decision and assignment (issue comment 5858063707), TAKEN (5858076185) and REVIEW READY (5858184304).
- Prior public findings on PR #598: none. After my own pass I read the PR's comments, reviews and review threads. The only comments are the two review-start notices, and there are no reviews or threads. Nothing needs to be retained or resolved.

## Verdict summary

The measurement holds up. I regenerated the shipping 1x1 TDM8 AEM image from the product-image commit `9e9954e9` myself. It hashes exactly to the assigned `9b077636...` and CRC `93742dd2`. The raw AECP ENTITY and CONFIGURATION responses are byte-identical to that image. All three runs' descriptor inventories match the image's descriptor index: 41 descriptors of 14 types, index for index.

The probe reports the library's own compatibility flags and cannot report `Milan` any other way. The library revision is the peeled `v4.3.1.1` tag, and the library ran with exactly its default CMake option set. The three runs were separate processes with identical static trees.

The verdict is NEGATIVE because of two MINOR documentation/conformance defects in how the page records this result:

- **F1:** a cold reader has no public locator for the new packet, and three of its hashes name files that were published only in redacted form.
- **F2:** the new Milan PASS sits next to the page's existing Milan FAIL statements, with no reconciliation.

## Findings

### F1: MINOR, Docs and Conformance: the B4 raw artifacts have no public locator, and three B4 hashes do not match the published bytes

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:629-632`. Also affected: the box-5 row at `:58` and `Raw artifacts` at `:653-661`.
- **Authority:**
  - Issue #117 acceptance box 5 requires raw artifacts and exact hashes.
  - The page's own box-5 row (`:58`) claims "PASS for the runs recorded here: both bench packets are published at a pinned commit ... [Raw artifacts] gives the locator".
  - The page's convention (`:659-661`) says which hashes name files published only in redacted form, and points to `MANIFEST.json`.
  - AGENTS section 6, Docs lens: there must be enough evidence for a cold reviewer.
- **Evidence:**
  - Line 629 names "the coordinator's `117-a373` evidence packet".
  - Line 630 says "publication is pending".
  - Line 632 says "Entity dumps and enumeration logs retain their recorded bytes."
  - The packet is now public at `89aa9f94`, but the page gives no locator for it.
  - At that commit, `author/run-1/2/3.entity.json` are `path_redacted` in `MANIFEST.json` (the DUT serial string is replaced by `<device-serial>`). The page's hashes for them (`2c4c801c...`, `11c4bca3...`, `3fd1d58c...`) match only the as-recorded originals, not any published file.
  - `receipts/page_hash_crosscheck.txt`: all 10 B4 hashes equal the author manifest and the recorded originals. Only 7 of 10 equal the published bytes.
- **Impact:**
  - Merged as-is, the page permanently says publication is pending.
  - A cold reader cannot get from the page to the B4 raw artifacts.
  - Three cited hashes cannot be checked against any public file unless the reader already knows about the undisclosed original-to-published mapping.
  - The box-5 PASS "for the runs recorded here" is then overstated for the B4 runs.
- **Required outcome:**
  - The page names the published B4 packet at a pinned commit, in B4 or in `Raw artifacts`, as it already does for the A200/A202 packets.
  - It drops "publication is pending".
  - It states that the three entity dumps are published redacted, with `MANIFEST.json` mapping each one to its published copy.
  - Whether `:58`/`:653` may be reworded under the frozen Hive-row/B4 scope is for the coordinator to decide publicly. Either way, the box-5 claim must not be left untrue for the B4 runs.
- **Verification:** every hash in the B4 table resolves at the named pinned commit, either directly by `sha256sum` or through `MANIFEST.json` `original_sha256` to a `published_sha256` that `sha256sum` confirms. `receipts/page_hash_crosscheck.txt` shows the method.

### F2: MINOR, Docs and Conformance: the new Milan PASS is not reconciled with the page's existing Milan FAIL statements

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:538-541`, against the retained lines at `:6-7`, `:28`, `:31`, `:53`, `:462` and `:467`.
- **Authority:**
  - Issue #117 acceptance box 4 says "pass without a stale or skipped mandatory row".
  - AGENTS section 5 requires authoritative documentation to be updated when the recorded result changes.
- **Evidence:** once this PR lands, the same page states the following, in the present tense, for the same DUT and the same library build:
  - Contents `:28`: "the la_avdecc enumeration that downgrades the DUT from Milan".
  - `:53` and `:462`: Milan compatibility FAIL, "tracked in #529".
  - `:467`: "#529 tracks closing it".
  - The new rows `:54` and `:464`: Milan PASS on `9e9954e9`.

  The page never says why the verdict changed:
  - #529 closed on 2026-09-24 through PR #534.
  - #534's merge `50e780975` is an ancestor of the enumerated image `9e9954e9`.
  - The new dumps show STREAM_INPUT 1 (CRF) serving counters.
  - The evidence for all three is in `receipts/image_and_history.txt`.

  There are two further inaccuracies:
  - The header (`:6-7`) still describes the page as measured on 2026-09-23 on the `ede8d48e` image.
  - Contents `:31` still says "the two blockers that remain", although B1 to B4 are all RESOLVED after this PR.

  The new B4 text (`:541`) says the result "does not clear acceptance box 4's remaining NOT RUN rows". Box 4 also still carries the FAIL row at `:53`, and B4 does not say whether the new result supersedes it.
- **Impact:**
  - A reader cannot tell from the page whether the DUT is currently judged Milan-compatible, or which image each verdict belongs to.
  - Box 4's standing is ambiguous, which is exactly the stale-row condition that box 4 forbids.
- **Required outcome:**
  - The page states that the Step 5 Milan FAIL is the 2026-09-23 `ede8d48e` record, and why the `9e9954e9` result differs (#534 closing #529).
  - It states how box 4's Milan-compatibility row stands (superseded, or kept as a dated FAIL).
  - It lists box 4's remaining non-PASS rows accurately.
  - This can be done inside B4 within the frozen scope. Changing `:6-7`, `:28`, `:31` or `:467`, or deciding publicly to leave them, is for the coordinator.
- **Verification:** reading the page, no present-tense statement contradicts another about Milan compatibility, and B4 accounts for the `:53` row.

### S1: SUGGESTION, Tests: the packet's `tools/summarize.py` does not gate diagnostics or AECP statistics

- **Evidence:** `receipts/mutation_probes.txt`. The unmutated control exits 0, and 10 of 11 injected faults are killed: flags reduced to IEEE17221, added MILAN_WARNING, a compatibility event, a complaint, a query error, rc 5, static-model drift, a dropped cluster, a wrong model ID, and a diagnostics change in one run.
- **What survives:** a redundancy warning injected into all three runs. Diagnostics are caught only by cross-run equality.
- **Why it is only a suggestion:** the page's statistics and diagnostics claims (`:582-585`) are true in the raw data. `scripts/verify_packet.py` checks them directly.
- **Suggestion:** have `summarize.py` also assert the diagnostics and the retry, timeout and unexpected-response counters.

### S2: SUGGESTION, Docs: name the library's compatibility-leniency options

- **Where:** `:623-626` names four feature defines. The build and the runtime option list also carry:
  - `IGNORE_INVALID_CONTROL_DATA_LENGTH`
  - `IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES`
  - `IGNORE_NEITHER_STATIC_NOR_DYNAMIC_MAPPINGS`
  - `CONTINUE_MISBEHAVE_AEM_RESPONSES`
  - `ALLOW_GET_AUDIO_MAP_UNSOL`
  - `ALLOW_RECV_BIG_AECP_PAYLOADS`
- **Why it matters:** these are exactly the library's default CMake options at `6d61a92e` (`receipts/library_and_packet.txt`), which supports "same verdict as a stock build". However, `IGNORE_INVALID_CONTROL_DATA_LENGTH` demotes a malformed-length warning to a debug log. The "no warnings" result is therefore conditioned on the default option set, and one sentence saying so would make that explicit.

### S3: SUGGESTION, Tests and Docs: the probe build uses an include directory the packet does not describe

- **Evidence:** `author/build-provenance.txt` passes `-I$HOME/la_avdecc-probe/include`. `VALIDATION-NOTES.md` calls it "installed dependency headers", but the packet README gives no content list or versions for it.

## Focus items

1. **Identity gate: PASS.**
   - I regenerated the AEM image from `9e9954e9` with the builder and `avdecc/gen_aemi_image.py`, with submodules at its gitlinks. The result is 7,352 bytes, SHA-256 `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404`, CRC `93742dd2`, which equals the assignment and the UART readback.
   - The AECP READ_DESCRIPTOR payloads, minus the 4-byte configuration/reserved prefix, equal image offsets `0x110` (312 bytes) and `0x248` (106 bytes). Control_data_length is 328 and 122, which is payload + 12.
   - The UART VERSION is `00020060`. ROM, QSPI and AEM CRCs match `expected-crc.txt`.
   - `9e9954e9..2a2a7bb6` touches four docs/evidence files only, and the gitlinks are equal at the image commit and at the head.
   - The bitstream SHA-256 values are compared only against the author's build directory (see Limits).
2. **The probe uses the library's own judgement: PASS.**
   - The flags come only from `getCompatibilityFlags()` (`tools/enum_probe.cpp:164`), and `flags()` names every member of the v4.3.1.1 enum.
   - The JSON flags are the library's own serializer output.
   - Every Warn-or-higher log from any entity counts as a complaint.
   - The probe never prints PASS. Its rc is non-zero only for ABI mismatch, a missing guard or an absent DUT. The PASS on the page rests on the flags, which `summarize.py` asserts: 10 of 11 faults are killed (S1).
   - The revision `6d61a92e...` is the peeled public `v4.3.1.1` tag, and `4.3.1-beta1` is that tag's own version convention.
   - The runtime option list equals the CMake defaults.
   - Every probe API call exists at that revision.
3. **Independent runs and inventory: PASS.**
   - The three runs have distinct START/END windows, entity-online order, `available_index`, unsolicited counts and enumeration times. Each has its own fresh output directory (`exist_ok=False`).
   - The static trees are identical, and the canonical SHA-256 `460b15ac...` reproduces on the published (redacted) bytes.
   - The inventory recomputed from each dump equals the regenerated image's descriptor index: 41 descriptors of 14 types.
4. **Page scope: PASS for the scope, with F1 and F2 on content.**
   - A difflib comparison shows exactly three replaced regions: `:54`, `:464` and B4 (`:536-649`).
   - 9 of the 11 base lines carrying NOT RUN are byte-identical. The 2 removed are the two Hive rows.
   - The owner decision is cited twice (`receipts/page_scope_check.txt`).
5. **Public-evidence hygiene: PASS.**
   - The diff's 116 added lines carry no host, peer, switch, instrument, suite, serial, home path or interface names.
   - `docs_check.py` reports 0 findings. The other doc gates return rc 0 (`receipts/doc_gates.txt`).
   - The following are present, and each is in the accepted class or has precedent in the tree:
     - in the packet, the controller EUI `6805cafffe95b2ed`: this family is already tracked in `tb/tools/avdecc_ctl.py:313` and `tb/verilator/tsn_fuzz/wire.py:37`;
     - the peer entity ID `3cc0c60102030000` in the run logs: derived from the peer clock `3cc0c6fffe010203` already on the page at `:328`;
     - the DUT's own serial string in the ENTITY hex;
     - the g++ and libpcap versions: already on the page at `:211-212`.
   - Paths are `$HOME` placeholders and `/tmp` scratch paths only.

## Lens coverage (reviewer-owned ledger)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #117 acceptance boxes 4 and 5; owner decision 5858063707; page `:53-58`, `:462-467`, `:536-649`; regenerated `aem_desc.bin` and map; `identity-aecp.jsonl`; `identity-uart.txt`; `run-1..3.log` and `.entity.json`; la_avdecc `6d61a92e` sources | R359-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| RTL | CLEAN | Diff `2a2a7bb6..bcba79a5`: one Markdown file, no HDL or generated RTL. Gitlinks `external`, `gptp-processor` and `protocol-processor` are equal at image `9e9954e9` and at the head. `9e9954e9..2a2a7bb6` changes four docs/evidence files (`receipts/image_and_history.txt`). The enumerated image's descriptor ROM is reproduced from source (`receipts/aem_regen_and_verify.txt`) | R359-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Robustness | CLEAN | `tools/enum_probe.cpp:121-184`: ABI refusal, guard failure, absent-DUT rc 5, complaints counted over all entities, flags only from the library. `tools/enumerate_once.py`: 20 s/23 s bounds, fresh run directory. Library `avdeccControllerImpl.cpp:6343-6346`: MisbehaveContinue still sets Misbehaving. Repeated runs are idempotent (identical static trees) | R359-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Tests | CLEAN (S1 and S3 are SUGGESTIONs only) | `tools/summarize.py` under 11 fault probes (`receipts/mutation_probes.txt`); independent `scripts/verify_packet.py`, 21 checks, all OK; doc gates re-run at the head (`docs_check`, `check_doc_style`, `check_doc_paths`, `check_baremetal_only --check`, `check_em_dash --base 2a2a7bb6` over 116 lines, `gen_toc --check`, `git diff --check`), all rc 0 | R359-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Docs | UNCLEAN (F1, F2) | `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, whole page at the head against base `2a2a7bb6` (`receipts/page_scope_check.txt`); B4 hash table against the packet (`receipts/page_hash_crosscheck.txt`); packet README and manifests | R359-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |

## Limits

- I did not touch the bench or the DUT, and I did not repeat the enumeration. Everything above is judged from the published raw artifacts.
- I did not rebuild the bitstream. The bitstream file and payload SHA-256 values, and the ROM hash, are the author's computation from their build directory. The UART CRCs are consistent with those values, but that is not provenance proof. The AEM image is the one artifact I reproduced from source.
- I did not compile or run the probe. The library and probe binaries are recorded by hash only. I checked the probe's source against the library source at `6d61a92e`.
- The redaction in the published dumps lies in `entity_descriptor.dynamic`, outside the static tree.
- Hosted checks at the head, read-only: `rtl-fast`, `bdd-conformance`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `wire-accountability` and `changes` passed. `docs-check` was pending when I read it. The Verilator, Yosys and physical contexts are skipping for this docs-only scope, which is not execution evidence.
- Physical calibration is NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The merge-turn candidate build against live dev.
- A public scope decision for the F1/F2 lines outside the Hive rows and B4, if needed.
- Publishing this packet.
- Merge authorization rests with the maintainer.

## Receipts and restoration

- Scripts:
  - `scripts/run_regen.sh` regenerates the AEM image from `9e9954e9` and runs `scripts/verify_packet.py`.
  - `scripts/mutation_probes.py` runs the fault probes.
- Receipts are under `receipts/`. `MANIFEST.sha256` lists every published file.
- The review clone is restored and verified (`receipts/clone_integrity.txt`):
  - HEAD `bcba79a5`, and the index tree equals `b9db4da3`.
  - The worktree and index are clean.
  - The four gitlinks are unchanged.
  - The `scripts/__pycache__` created by my gate run was removed, leaving 0 untracked or ignored entries.
- Disposable trees stayed under `scratch/`.

R359-1 FINISHED
