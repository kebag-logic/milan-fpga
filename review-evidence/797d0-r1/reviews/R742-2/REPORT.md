[R742] NEGATIVE - exact head 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee

PR #815, issue #797, external independent round R742-2. Tree `6d5ae1c3548e6dddd0224cae480db97db8035f6a`. Source base `1e80128f0a467b58bf884b7d9bf62e013a2fb141`; delta from round-1 head `bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a`.

The status rule and gate self-test are repaired. The named round-1 contradictions are now recorded and their pages are stale. Deeper sampling nevertheless found one release-facing page still incorrectly marked current and two inaccurate new corrections. These are factual claims, not stylistic preferences. No product change is requested: record the missing contradiction, correct the audit data, and regenerate.

## Findings

F1 - MAJOR - Conformance, RTL, Robustness, Docs - `docs/integration/INTEGRATION_GUIDE.md:60`, `:64`; `docs/DOCUMENTATION_AUDIT.md:272` - Current page misallocates GET_STREAM_INFO ownership.

- Authority/evidence: #797 D0 requires no release-facing current page to contradict the source. The guide says the processor owns four fields and the parent answers every other word and every validity flag. At the required processor pin `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`, `hdl/top/protocol_processor_top.sv:3573-3574` replaces the input VLAN with its full received `bound_vlan_r`, and `:3581-3585` clears flags `0x52000000`, the stream ID and destination MAC while the input is unsettled. The parent's `hdl/milan/milan_datapath.sv:6014-6022` and `:6413-6416` explicitly describe these overrides. The published author ledger marks guide line 64 `ok`, but the audit still says current/no recorded contradiction. Raw evidence is in `review-source-excerpts.txt`; ten verified-claim checks are in `sampling.md`.
- Impact: a cold integrator is told that these response values and validity decisions have the wrong final owner, including the re-probing boundary that must suppress stale stream identity. The generated audit omits the needed correction.
- Required outcome: record the additional processor-owned VLAN and settled-state filtering, their exact source locations, and mark the integration guide stale. The correction must preserve the parent's underlying gather data while naming the processor's final replacements/masking. No product-code change or page rewrite is required in D0.
- Verification: compare selectors 0, 2, 4 and 6 at the pinned processor and parent interfaces; require the generated finding and stale row; rerun the inventory gate.

F2 - MINOR - Conformance, Robustness, Docs - `scripts/docs_inventory.json:248`; `docs/DOCUMENTATION_AUDIT.md:476` - AEM correction invents a third validation check.

- Authority/evidence: D0-035 correctly identifies the firmware copy routine, then prescribes its “three checks (magic, compiled-in length, CRC32 after the copy)”. `sw/firmware/milan_baremetal/milan_baremetal.c:1845-1863` has two rejection predicates: bad magic and bad CRC. `MILAN_AEM_IMAGE_BYTES` bounds the copy and CRC calculation; there is no comparison or independent rejection of a length field. Its source cell already describes the actual sequence accurately.
- Impact: the generated repair instruction would retain the old page's false length-validation guarantee in revised form. This changes a numeric/error-path claim, so it is not wording residue.
- Required outcome: describe a magic check, a fixed compiled-length copy, and a post-copy CRC check, without claiming a third independent length check. Regenerate the audit.
- Verification: inspect the complete `load_aem_image()` function and its return paths; ensure the correction describes those two checks and the fixed length accurately; inventory gate passes.

F3 - MINOR - Conformance, Tests, Docs - `scripts/docs_inventory.json:192`; `docs/DOCUMENTATION_AUDIT.md:463` (D0-027) - New harness correction still claims a shipping trace producer.

- Authority/evidence: D0-027 says to keep the trace round-trip as the check of the “shipping trace producer”. D0-048 in the same data correctly establishes that the shipping firmware does not link it. `sw/firmware/milan_baremetal/Makefile:6` builds `milan_baremetal.o`; the firmware has no trace-producer include or call. The host round-trip tests the supplied `sw/trace/` producer, not its adoption by the shipping image. The published guide sampling at line 25 treats command existence as sufficient for the shipping claim.
- Impact: the area repair would preserve a false integration/evidence boundary, implying the host producer test validates code used by the shipping firmware.
- Required outcome: call it the standalone/supplied trace-producer round-trip, explicitly separate shipping integration, and make D0-027 agree with D0-048. Retain the correct shared host-harness recommendation.
- Verification: compare the firmware object list and producer call sites with both correction entries; regenerate and run the inventory gate. A new firmware integration is outside D0.

S1 - SUGGESTION - Docs - `scripts/docs_inventory.json:296-297` - Clarify the project-specific scratch terminology.

- Evidence: D0-042 follows existing “write-only scratch” terminology for registers with no product consumer. `milan_csr.sv:2050-2084` and `tb/verilator/csr/sim_main.cpp:531-542` show real stored-value readback. The existing register-class prose itself uses “write-only scratch” while saying writes read back.
- Impact: readers can mistake this local classification for WO bus access. This is not an additional factual finding because the existing project classification distinguishes effect from access.
- Suggested outcome: say “readable/writable scratch with no product consumer” in the correction, preserving the no-shaper claim.
- Verification: compare wording with shadow readback and leave code/tests unchanged. Optional; does not affect coverage.

## Independent checks and evidence

- Reconstructed repository contracts, documentation index, issue body and public D0 decisions before inspecting the full base diff and nine-commit delta. Product RTL, firmware, configuration and gitlinks are unchanged. No private author material or other reviewer report was read before this verdict and ledger were saved.
- `inventory-probes.log`: exact-head `--check` passes; `--selftest` passes 29 controls. A finding planted on current `docs/README.md` makes `--check` exit 1; `--write` renders stale and restores rc 0; forcing its cell current makes the gate fail by name. Three independent mutants (always-pass gate, untracked listing, removed status rule) all make the self-test exit 1. Disposable copies only, under packet scratch.
- `population.log`: independent tracked set equals all 210 rows; all 62 finding quotes locate; 176 current, 13 stale, 21 obsolete; every recorded-finding page is non-current.
- `sampling.md`: 15 newly recorded contradictions checked against sources (D0-034..045,047..049), plus 10 sentences the author marked verified. The latter includes the missed current-page claim F1. Recorded persistence observations remain dated evidence, not newly performed physical validation.
- `published-verification.log`: all 200 published author-round-2 files match the public manifest's published SHA-256 values at evidence commit `8e15dcfa654286db6da6d970b480b786a105d634`. The two source-head summaries record 96 commands with rc 0. Selected raw receipts are retained under `published-author/`, including the exact-head identity, inventory gates, workflow contract and mutation results. The large workflow self-test is published as a digest/first/last receipt, not its complete raw log.
- Signature limit: this evidence commit has no `gpgsig` header and `git verify-commit` exits 1. I verified published content hashes, not a cryptographic signer. No signed attestation was supplied in the inspected packet.
- The workflow/template, command-table script digest, exact `main(["--check"], root)` self-test entry, Git fixture listing, malformed-data controls, untracked exclusion, no-Git submodule exclusion and hook-environment isolation were inspected. Published source receipts support broader unchanged gates; no full product bank was rerun.
- Source comments in the delta remove the prior workflow label and narrow the freshness claim to rendered metadata/quoted findings. Arbitrary same-line semantic edits are still outside the gate's claim. No new source-comment label residue was found.

## Prior public findings reconciled at this head

The independent findings and five-lens ledger above were saved before fetching PR comments or reading the other reviewer's report. Afterwards, the published R741-1 body (comment 6520804068), own R742-1 report (6520356763), manager scope decision 6520804859, and PR review-start records were reconciled. No other round-2 report was read. Original lens assignments are preserved below.

| Prior item | Original lenses | Disposition and evidence at 3e6d92c1 |
|---|---|---|
| R742-1 F1 MAJOR | Conformance, RTL, Docs | RESOLVED for D0: D0-024/025 record journal use/backend/restore and separate remaining physical limits; QSPI page is stale. Backend :1123 and firmware slots :329-331, commit :1393, boot :1641/:1890 checked. New F2 concerns a different correction on that page. |
| R742-1 F2 MINOR | Conformance, Tests, Docs | RESOLVED at original cause: D0-026 records the aggregate and D0-027 names the shared host harness; guide is stale. run_litex_sims.sh:98-106,150-163 and gtest/README.md:4-13 checked. New F3 records the introduced shipping-trace claim. |
| R742-1 F3 MINOR | Conformance, RTL, Docs | RESOLVED: D0-028 gives q2=gPTP, q3=class B; egress page is stale. ethernet_packet_pkg.sv:220-221 and CSR map :2008 agree. |
| R741-1 F1 MINOR | Conformance, Docs | RESOLVED: D0-029..032 explicitly cover matrix rows 262-264/267; page remains stale. Parent :654-664 and :8552-8558 confirm no instantiated chain/slope consumer. The C-TAG correction preserves live framer/parser ownership. |
| R741-1 F2 MINOR | Conformance, Docs | RESOLVED: D0-033 records the repeated placement claim; AXIS integration page renders stale, consistent with README. SoC :2621 and current build-default scope checked. |
| R741-1 F3 MINOR | Tests | RESOLVED: self-test now invokes main(["--check"], root), stages Git fixtures and exercises git ls-files. Published mutant receipt kills both always-green forms and untracked listing; own probes independently kill always-pass/untracked/status-rule mutants. |
| R742-1 R1 / R741-1 R1 RESIDUE | Conformance, Docs (R742); source-comment item (R741) | RESOLVED: docs_inventory.py:98-99 states the release-facing scope without the workflow label. |
| R741-1 R2 RESIDUE | Docs wording item | RESOLVED: template :422-433 limits freshness to line count/title/audience/paths/standards/quoted findings, consistent with the generator docstring. |
| R741-1 S1 SUGGESTION | Gate behavior | RETAINED optional: regenerated missing-quote rows pass as explicit re-verification requests. This is documented, controlled behavior; no stronger requirement was added. |
| R741-1 S2 SUGGESTION | Source comments | RETAINED optional for source-comment/area follow-up: unchanged clause/reset comments are outside D0 edits. No claim that moving paperwork fixes their content. |
| R741-1 S3 SUGGESTION | Ownership reference | RETAINED optional: the closed coordination issue still holds its record; confirm the remaining work's owner during the area rewrite. |

This closes the six named prior findings at their original causes, but the new F1-F3 remain open. The earlier all-green gate evidence is not approval of these newly sampled assertions.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1-F3 | #797 frozen D0 decisions; REQUIREMENTS.md:128,308; data and 210-row audit; 15 findings and 10 verified sentences | R742-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| RTL | UNCLEAN: F1 | Full diff and unchanged gitlinks; pinned processor top:3566-3588; parent gather:5995-6025,6413; backend, queue enum/reset, CDC and clock bindings | R742-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Robustness | UNCLEAN: F1,F2 | Unsettled-response masking and image rejection paths; generator status/refusal/population logic; 29 controls and planted status/mutation probes | R742-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Tests | UNCLEAN: F3 | Workflow/template and actual gate-entry self-test; public 96-command source receipts; shared host harness, aggregate runner and standalone trace integration boundary | R742-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Docs | UNCLEAN: F1-F3 | Generated audit/data, prior target pages, source comments, public sampling ledgers, correction accuracy and scope decisions | R742-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |

All five lenses were applied. Gate behavior is clean within its stated metadata-consistency scope; this does not clear the unrelated factual claims above. No lens is banked as clean while its listed finding remains open.

## Limits and pending duties

This is a source-head delta review, not final merge-candidate validation. No manager source bank is claimed or inferred. The manager owns local/hosted acceptance and the current-dev merge candidate's builder/native banks; skipped contexts do not count as executed jobs. No full parent/processor/gPTP/synthesis/builder banks, hardware, physical calibration, source fixes, commits, pushes, external writes, sub-agents or workflow-container execution were performed. Physical calibration is NOT RUN; field skips are not hardware proof. Licensed standards were not newly rederived for unchanged clause-only findings.

The public author packet discloses 823 sentences read without per-sentence source evidence and five partly checked. This review samples that audit rather than certifying every sentence. The new style-gating/register-generation/diagram requirements on the umbrella issue are not silently treated as completed by this frozen D0 delta. The overall documentation sweep remains open. Public guard/reset and link-status scope conflicts remain for their owning decisions.

Final integrity: `tree-integrity.log` verifies all 1,449 root tracked blobs and all tracked blobs of five initialized dependencies, including exact bytes, file kinds, executable modes, indexes and pinned commits. The four required dependencies match their gitlinks; optional external remains uninitialized. The publication manifest lists every retained receipt and script; scratch and raw API captures are excluded.

The manager must obtain fixes and re-review affected lenses, collect the other independent verdict, complete final current-dev candidate validation and required evidence, obtain merge authorization, and perform containment. No merge approval is given.

R742-2 FINISHED
