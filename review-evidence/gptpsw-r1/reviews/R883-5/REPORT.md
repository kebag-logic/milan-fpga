[R883] NEGATIVE - exact head 0acf24d9b5060a263f725c02026446dde64c2574

# R883-5: narrow re-review of PR #966 (issue #884), the fix for R883-4-F1

- **Head:** `0acf24d9b5060a263f725c02026446dde64c2574`, tree `1becc48fafe08f26e617d3ade363e57a5a75f1db`. This is also
  the live `884-gptp-firmware` tip and the PR head (base `dev-soft-core-optimisation`, not draft).
- **Delta reviewed:** `44c56639..0acf24d9`, one commit. Its subject is one line with no trailers. It changes two files,
  both tests: `sw/firmware/ctrl/test/test_aecp.cpp` (+22/-15) and `sw/firmware/ctrl/test/aecp_face_mutants.py` (+5).
- **No product source changed.** `git diff --name-only 44c56639 0acf24d9` lists only those two paths. The blob of
  `aecp_face.c` at the head is `1cf772cc`. `sw/firmware/gtest/coverage.ratchet` is unchanged.
- **Packet checked:** `review-evidence/gptpsw-r1/author-r7` at `d5887167`. All 26 files match the published sha256 in
  `MANIFEST.json`. Two scripts, `env.sh` and `feed.sh`, carry the manager's path redaction. Their `original_sha256`
  values equal the author's `INDEX.md` prefixes (`receipts/packet-verify.txt`).

## Summary

The test fix works. R883-4-F1 is resolved at its cause:

- The software-gPTP AVB test now makes the datapath's bit 0 disagree with the owner's asCapable, both ways round, on
  every interface.
- The test checks AS_CAPABLE with its own words.
- My five planted leaks are caught by those words alone, and so is the author's row. The link-flags check does not
  fire for any of them.
- The unplanted test passes at one and two interfaces.

The new assertion words still break a gate. They contain the phrase `software gPTP owner`, which the repository's
bare-metal scope gate (#259) refuses. As a result `scripts/check_baremetal_only.py --check` fails at this head
(rc 1, 2 findings, both on lines this delta added) and passes at the parent `44c56639` (rc 0). The hosted
`docs-gates-0` job fails at this exact head in the same step, with the same two findings. The author's packet did not
run the docs workflow. Its reason was that the delta "changes only the two test files above, and those are read by
the firmware gate and the AECP campaign". That reasoning does not hold, because this gate scans every tracked
first-party file.

## Findings

### R883-5-F1 | MAJOR | Conformance, Tests, Docs | `sw/firmware/ctrl/test/test_aecp.cpp:4681`, `sw/firmware/ctrl/test/aecp_face_mutants.py:31` | The new AS_CAPABLE words fail the bare-metal scope gate (#259)

- **Authority/evidence:**
  - `scripts/check_baremetal_only.py:194` lists `"software gPTP owner"` in its class-R `RUNTIME_TERMS`. Under the
    #259 directive, class-R terms are refused in any tracked first-party file, including strings and test fixtures
    (module docstring, lines 4-35).
  - The delta adds that phrase twice:
    - in the assertion message `"AS_CAPABLE is the software gPTP owner's, whatever the datapath's bit 0 (...)"`
      (`test_aecp.cpp:4681`);
    - in the campaign needle `"AS_CAPABLE is the software gPTP owner's"` (`aecp_face_mutants.py:31`).
  - Local run at the head: `baremetal-only: FAIL (2 finding(s) across 1936 scanned file(s))`, rc 1, naming exactly
    those two lines (`receipts/baremetal-head.log`).
  - Local run at the parent `44c56639`: `baremetal-only: OK (0 findings ...)`, rc 0 (`receipts/baremetal-parent.log`).
  - Hosted: the `Bare-metal scope gate` step of job `docs-gates-0` (run 45415508824, head `0acf24d9`) fails with the
    same two findings (`receipts/hosted-docs-gates-0-baremetal.excerpt.log`). The gate is wired in
    `.github/workflows/docs.yml:306-307`.
  - The author's REVIEW-READY lists the docs workflow as "not re-run".
- **Impact:**
  - The head violates a repository-wide normative directive (#259).
  - A required hosted docs context is red at the exact head, so the completion bar in AGENTS.md section 7 cannot
    be met.
  - The fix cannot be a prose-only edit. The assertion text and the campaign's grading needle must change together,
    or the new mutant row becomes an escape. That is why this finding is MINOR or above and not RESIDUE.
- **Required outcome:**
  - Reword the assertion and the needle together so that neither contains a #259 term. The rest of the tree already
    says "firmware gPTP owner" (`docs/design/GPTP_SOFTWARE.md:153`), so "AS_CAPABLE is the firmware gPTP owner's"
    would satisfy the gate. The exact words are the author's choice.
  - Keep the needle a substring of the assertion text, and keep it distinct from "software gPTP keeps the
    datapath's link flags".
  - Before the next REVIEW READY, run the docs workflow's local gates. At minimum that is the bare-metal gate's
    `--check` and `--selftest`.
- **Verification:**
  - At the fixed head, `python3 scripts/check_baremetal_only.py --check` returns rc 0 with 0 findings, and
    `--selftest` passes.
  - Hosted `docs-gates-0` and `docs-check` succeed at that head.
  - The `face-software-gptp-keeps-datapath-capable` row is still caught on its new words in the AECP campaign.
    The two other software-gPTP face rows are still caught on their own words.
  - The unplanted AVB test passes at one and two interfaces. Running this packet's `probe_leaks.py`, with its `NEW`
    constant updated to the new words, should still return rc 0.

### R883-5-S1 | SUGGESTION | Tests | `sw/firmware/ctrl/test/test_aecp.cpp:4667-4679` | The link-flag bits are never varied

- The datapath's bits 1 to 7 are always `0x7a`'s, and the check is `flags & ~1u == 0x7au`. So, by inspection, the
  plant `out->flags = (uint8_t)(0x7au | (as_capable ? 1u : 0u))` would pass all four cases. That plant hard-codes the
  link flags instead of keeping the datapath's. I did not run it.
- This weakness was already present at `44c56639` and is outside this round's scope. The delta's new
  `Far::avb_flags` now makes it a one-line extension.
- **Optional:** add a datapath value whose upper bits differ, such as `0x84`/`0x85`, and expect `flags & ~1u` to equal
  `datapath & ~1u`.

### R883-5-S2 | SUGGESTION | Docs | `sw/firmware/ctrl/test/test_aecp.cpp:4667` | The new comment names no requirement ID

- The comment "the datapath's bit 0 is live (KL_ptp_clock_validity.sv): it meets the owner's verdict both ways round"
  gives its reason by file. It cites no requirement or issue ID.
- **Optional:** append "(IEEE 1722.1-2021 7.4.40.2, #884)".

### Source-comment rule

I scanned the three new comment lines (`test_aecp.cpp:4327`, `:4667`, `aecp_face_mutants.py:27`) and the two new
assertion strings. None contains a bench lane label, lane name, review round, reviewer ID or issue-comment ID, so no
new RESIDUE is recorded.

## Prior findings, resolved or retained at this head

| Finding | Status at `0acf24d9` | Evidence |
|---|---|---|
| R883-4-F1, MINOR, Tests | **RESOLVED at its cause.** The words used must change under R883-5-F1, and the fix is re-checked there. | `test_aecp.cpp:4666-4686` runs datapath `0x7a` and `0x7b` against capable true and false on every interface. Five reviewer plants all fail on "AS_CAPABLE is the software gPTP owner's" and none on the link-flag words: datapath wins, override removed, AND, OR spelled differently, owner inverted. The author's `face-software-gptp-keeps-datapath-capable` row behaves the same. `face-software-gptp-clears-link-flags` fails on the link-flag words only. The path-refusal row is caught. The table-drift control passes with the new row. The unplanted baseline is `[ PASSED ] 2 tests` at one and two interfaces. Receipts: `probe-leaks.filtered.log`, `probe-plant-excerpts.log`, `probe-results.json`, `probe-baseline*.log`. The author's leak escaped at `44c56639` (`author-r7/receipts/plant-old.log`). |
| R883-4-R1, RESIDUE, Docs | RETAINED on the residue checklist | PR body and `sw/firmware/gtest/README.md` are untouched by the delta |
| R883-4-R2, RESIDUE, Docs | RETAINED | The docstring at `aecp_face_mutants.py:3-9` is unchanged and now omits three software-gPTP rows. R2's exact fix already covers AS_CAPABLE, so it still applies as written. |
| R883-4-R3, RESIDUE, Docs | RETAINED | `test_unit_driver.cpp` is untouched |
| R883-4-S1, SUGGESTION, Tests | RETAINED | `test_unit_driver.cpp` is untouched |
| R883-3-F1/F2, R884-3-F1, and earlier F rows (R883-1, R883-2, R884-1, R884-2) | RESOLVED earlier, retained | Their artifacts are untouched by this tests-only delta |
| R883-3-R1 / R884-3-R1, RESIDUE (source-comment IDs) | RETAINED (#746) | No new instance |
| R883-1-S1 to S5, R883-2-S1 to S4 | As previously recorded | Artifacts untouched |

## Lens results (artifact evidence)

```text
[R883] MAJOR Conformance — test_aecp.cpp:4681, aecp_face_mutants.py:31 — head violates #259 (R883-5-F1); test-side AS_CAPABLE semantics otherwise match aecp_face.c:208-213 and IEEE 1722.1-2021 7.4.40.2 bit 0
[R883] PASS RTL — git diff --name-only 44c56639 0acf24d9 (no hdl/ path); hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:143,243 confirms the datapath bit 0 is live asCapable, so the fixture's 0x7b case is a real datapath state
[R883] PASS Robustness — test_aecp.cpp:4666-4692 — both disagreement cases on every interface, plus the unchanged silent-datapath refusal with no owner call; five reviewer plants caught, baseline green at 1 and 2 interfaces (receipts/probe-*)
[R883] MAJOR Tests — aecp_face_mutants.py:31 needle tied to test_aecp.cpp:4681 words that a required gate refuses (R883-5-F1); otherwise the plants are graded by name and words (receipts/probe-plant-excerpts.log)
[R883] MAJOR Docs — author-r7 REVIEW-READY "docs workflow ... not re-run" input analysis contradicted by receipts/baremetal-head.log and hosted docs-gates-0 (R883-5-F1)
```

## Gate evidence at the head

- **Author receipts** (manifest-verified, not re-executed by me):
  - `fw_coverage --check` rc 0, `firmware coverage: PASS (42 files)`. The figures match the ratchet: `aecp_face.c`
    229/229 and 204/204, `gptp.c` 665/704 and 346/437. The ratchet file is unchanged, so no recorded figure is
    lowered.
  - The four firmware shards (`--require-rv32 --self-test`) each report rc 0, `ESCAPED=0` and clone head
    `0acf24d9`. Shard 2 carries all three software-gPTP face rows `[ok]`.
  - `check_py_idiom.py` rc 0. `git diff --check` rc 0.
- **Reviewer runs:**
  - The plant probe and the AECP plant-table controls (above).
  - The bare-metal gate at the head (rc 1) and at the parent (rc 0).
- **Hosted, observed only; the manager owns acceptance:** at `0acf24d9`, `docs-gates-0` fails on the bare-metal
  gate. `docs-check`, `elaborate`, six `Union *` jobs and `verilator-suites` fail on aggregate "every gate/case
  exactly once" steps. Most Verilator and Yosys shards are cancelled, `yosys-portability` is queued and `rtl-fast` is
  cancelled. I did not determine the cause of the non-docs failures. They may be cascades of fail-fast cancellation.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R883-5-F1) | `test_aecp.cpp:4647-4692` against `aecp_face.c:191-215` (bit 0 AS_CAPABLE, 7.4.40.2); `scripts/check_baremetal_only.py:180-207` (#259) against the delta | R883-5 | `0acf24d9b5060a263f725c02026446dde64c2574` |
| RTL | CLEAN | Delta path list (no `hdl/`); `KL_ptp_clock_validity.sv:143,243` | R883-5 | `0acf24d9b5060a263f725c02026446dde64c2574` |
| Robustness | CLEAN | `test_aecp.cpp:4666-4692`, `Far::word` at `:4416-4437`; `receipts/probe-*` | R883-5 | `0acf24d9b5060a263f725c02026446dde64c2574` |
| Tests | UNCLEAN (R883-5-F1) | `test_aecp.cpp:4327,4398,4416,4434,4666-4686`; `aecp_face_mutants.py:24-36`; `aecp_mutants.py:891-970` (reader, controls, campaign); reviewer plants; author shard and coverage receipts | R883-5 | `0acf24d9b5060a263f725c02026446dde64c2574` |
| Docs | UNCLEAN (R883-5-F1) | `author-r7` REVIEW-READY, HANDOFF and INDEX against receipts and `MANIFEST.json`; delta comments (source-comment rule); `receipts/baremetal-*.log`; hosted `docs-gates-0` | R883-5 | `0acf24d9b5060a263f725c02026446dde64c2574` |

## Real limits

- **Not run by me:** any full firmware shard, `fw_coverage --check`, the full AECP campaign, boundary legs, the docs
  workflow beyond the bare-metal `--check`, or the bare-metal `--selftest`. Shard and coverage results are the
  author's manifest-verified receipts. My probes cover only the AVB test and the three software-gPTP face rows.
- **How my probes run:** they reuse the repository's own planting and grading functions (`aecp_mutants.campaign`,
  `caught`) on disposable copies. The checkout was never written. The first probe run graded every plant, then hit my
  580 s wall-clock bound during the two-interface baseline (`receipts/probe-leaks.rc` reads `rc=124`). I re-ran the
  baseline alone (`probe_leaks.py ... baseline`, `receipts/probe-baseline.rc` rc 0). Restore check: the HEAD tree, the index tree and
  the blobs and modes of the three touched files match the head. All six gitlinks are as recorded, and the status is
  clean (`receipts/restore-check.log`).
- **Not claimed:** no manager source bank exists at this head, and none is claimed or inferred. No Docker, act, host
  runner, hardware or physical calibration was run. Field skips are not hardware proof. I make no hosted acceptance
  claim.

## Pending manager duties

- Relay R883-5-F1 to the author. After the reword, the next head needs a delta re-review covering at least
  Conformance, Tests and Docs.
- Carry R883-4-R1 to R3 on the residue checklist.
- Own hosted and act acceptance at the new head, and run the current-dev merge-candidate builder and native banks at
  the merge turn (source base `59b09884`, live dev `e275d795`).

R883-5 FINISHED
