[R740] NEGATIVE - exact head 8607347675743fe8d1ccaa370c63905c5ca1ccd5

Independent whole-PR verdict, written before reading any issue/PR comments or another review. Base: 135afd043309369a87ddbc8d6550aff8ec52a157. Tree: 7791e003a4c235379f7dcdb2efc215b22c85c105. Scope: issue #96 / PR #97. All five lenses applied. Public-evidence and prior-finding reconciliation follows this sealed independent pass.

The delta is exactly eleven Markdown files and scripts/check_docs.py. No RTL, generator, generated image, test implementation, build rule or submodule changes. The checkout has 113 tracked files and no nested gitlinks. All tracked blob bytes, executable modes and the index match the requested head. No source fixes were made.

Repository AGENTS.md and CONTRIBUTING.md are absent. The supplied repository instruction was read. Reconstruction used docs/README.md and README.md, issue #96 body, linked issue bodies and pinned parent interface sources, the complete diff and four-commit history, then executable local gates. Comments were deliberately deferred to satisfy the stronger isolation instruction. Initial scope and authority limits are stated below.

Findings

F1 — MINOR — Conformance, RTL, Docs
Artifact: docs/INTEGRATION.md:14; docs/HDL_DEVELOPER.md:12.
The new summaries assert that publication outputs change together on pub_commit_o and only through a commit. Actual outputs directly expose staging registers: hdl/top/KL_gptp_engine.sv:994-997 writes GM, parent and flags independently under state writes; :1037-1053 writes the path independently; :1134-1146 continuously assigns those registers to outputs, and separately assigns the commit pulse. There is no output snapshot latch at commit. The existing path-stage assertion at :874-877 explicitly acknowledges raw transients before publication.
Impact: an integrator relying on stable, atomic wires between pulses can consume mixed state. This is a factual interface error, not wording residue.
Required outcome: describe pub_commit_o as the validity/sampling boundary for the completed staged tuple; state that raw outputs can change earlier. Preserve the consumer obligation to capture on commit. Correct both summaries and any equivalent unconditional stability claims.
Verification: trace each public output to its state writer and confirm the prose distinguishes staging from committed consumer capture. The RTL does not need changing for this documentation PR.

F2 — MINOR — Robustness, Tests, Docs
Artifact: scripts/check_docs.py:110, :388-404; docs/INTEGRATION.md:837.
CONSTANT_ROW_RE only recognizes unsigned, unformatted decimal cells. constant_findings silently skips every other row and succeeds if any other recognized constant remains. In an isolated exact-head tree, replacing SYNC_RTO_MS_C value 375 with either **376** or -1 leaves scripts/check_docs.py at rc 0. The unformatted stale 376 control correctly returns rc 1. Receipts: probe-formatted-stale-constant.log/.rc, probe-negative-stale-constant.log/.rc, probe-stale-constant.log/.rc and probe-results.json.
Impact: a visible stale value in the authoritative table passes the new freshness gate, contradicting its stated guarantee. Existing 23 self-test arms do not cover this escape.
Required outcome: recognize constant rows independently of their value syntax, then either parse supported Markdown formatting or reject invalid cells. Do not silently omit a named row. Add positive and negative controls for these cases.
Verification: unmodified head-equivalent input passes; the two escaped stale rows fail with a named-constant diagnostic; existing stale-value and status controls continue to work.

F3 — MINOR — Conformance, Docs
Artifact: docs/INTEGRATION.md:364-367, :381, :394, :406, :414, :458, :495-497, :705-707, :793-803, :843-859; docs/HDL_DEVELOPER.md:202; docs/TEST_DEVELOPER.md:129, :143, :153-154.
Issue #96 says values live in one table and are linked, never copied. The new constants table duplicates the retained step-threshold table (20/100 us versus 20,000/100,000 ns), receipt durations, rate bound and tracking-band values in current prose and other pages. Links added above these sections do not eliminate the copied numbers. The isolated duplicate-prose-drift probe changes the link-up table to 21 us and still passes the gate.
Impact: multiple independently editable authorities remain, so the requested single-source acceptance item is missing. This concerns numerical facts and is not residue.
Required outcome: keep each protocol setting in its canonical row, and reference its named setting/row elsewhere without repeating the value. Keep independently measured test stimuli and dated observations clearly distinct from configuration values.
Verification: audit each canonical setting across current pages, including unit-converted and spelled-out copies; no second normative value definition remains. Re-run documentation gates.

F4 — MINOR — Conformance, Docs
Artifact: docs/GLOSSARY.md:19.
The new Follow_Up companion definition cites 802.1AS-2011 11.4.3. That clause defines Sync. Follow_Up is 11.4.4; its preciseOriginTimestamp field is 11.4.4.2.1. The publicly indexed primary standard text shows Table 11-8 under Sync and Table 11-9 under Follow_Up. If the term also covers Pdelay_Resp_Follow_Up, distinguish its responseOriginTimestamp and cite its own message clause.
Authority: IEEE Std 802.1AS-2011, clauses 11.4.3 and 11.4.4, https://www.ida.liu.se/~sohsa65/courses/tsn-course-2021/stds/8021AS-2011.pdf (indexed primary text; direct download currently returns 404).
Impact: a current glossary directs a new engineer to the wrong normative message definition. Clause errors are not residue.
Required outcome: cite 11.4.4 for Follow_Up, with precise terminology for any response companion.
Verification: compare the revised row to the adopted edition message definitions.

No BLOCKER or MAJOR is asserted. No source-comment label was added in the reviewed delta. No wording-only residue is needed for these findings.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | issue #96 body; all current guides; linked interface bodies; primary indexed clauses; F1/F3/F4 | R740-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| RTL | UNCLEAN | engine state-port/publication wiring; parser; serializer; timer; microCPU; generator; four ROM images; F1 | R740-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Robustness | UNCLEAN | checker row parsers and isolated stale/format/negative/duplicate probes; F2 | R740-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Tests | UNCLEAN | Makefile entry points, all docs self-tests, lint, interface contract, clock-check self-test, fault controls; F2 | R740-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Docs | UNCLEAN | fourteen current pages, archive index/banners, all eleven Markdown deltas, start-here/glossary, pinned parent connections; F1-F4 | R740-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |

Source spot checks (read source, not just the documentation checker)

| # | Current statement / location | Source at exact head | Result |
|---|---|---|---|
| 1 | P1_C = 248, Integration:843 | generator:513 and CLI:2501 | Match |
| 2 | ASCAP_UP_C = 2, Integration:844 | generator:520, :2146 | Match |
| 3 | LOST_N_C = 3, Integration:845 | generator:521 | Match |
| 4 | Fifth loss clears capability, Integration:846 | generator:525, :1702-1708 | Match |
| 5 | Positive delay threshold 800 ns, Integration:847 | generator:518, :2137 | Match |
| 6 | Negative delay floor magnitude 80 ns, Integration:848 | generator:519, :2131-2137 | Match |
| 7 | Sync watch 375 ms, Integration:849 | generator:526, :1087-1088 | Match |
| 8 | Follow_Up watch 125 ms, Integration:850 | generator:527 | Match |
| 9 | Multiple-responder threshold 3, Integration:851 | generator:536, :1654 | Match |
| 10 | Default cease 300,000 ms, Integration:852 | generator:537, :2505 | Match |
| 11 | Link-up step threshold 20,000 ns, Integration:853 | generator:541, :1002-1009 | Match |
| 12 | Locked step threshold 100,000 ns, Integration:854 | generator:542, :1069-1070 | Match |
| 13 | Inclusive tracking band 100 ns, Integration:855 | generator:546, :1034-1036 | Match |
| 14 | Rate policy bound 200 ppm, Integration:856 | generator:547, :568-575, :1050, :1065 | Match in rounded addend units |
| 15 | ROM depth 1,024, Integration:857 | generator:323; microCPU:106 and package widths | Match |
| 16 | thisClock high word at 1,022, Integration:858 | generator:505 | Match |
| 17 | Grandmaster-capable bit 32, Integration:859 | generator:510 | Match |
| 18 | Shipping 1,022 / seeded 1,023 used words, Manager:61 | generator build/packing:2404-2485; executed both seed modes | Match |
| 19 | SERVO@0 and FUTO@254, Manager ROM budget | generator emitted placement for all four images | Match |
| 20 | Integer MAC CLI, Integration:812-821 | generator:2498; executed documented command | Match |
| 21 | Single synchronous clock/reset, Integration:64-76 | engine:70-71 and always_ff blocks | Match |
| 22 | Result ready low during reset/pending, Integration:171-173 | engine:411-412, :434 | Match |
| 23 | Four queue entries, HDL event arbitration | engine:467-485 | Match |
| 24 | Parser wins simultaneous pushes | engine:494-505 | Match |
| 25 | Eight timer slots | engine:447-450 | Match |
| 26 | Warm scratch retention / cold clear | engine:304-309, :880-916, :963 | Match |
| 27 | Invalidated claims/pairing/best record after reset | engine:826-837, :910-916 | Match |
| 28 | PHC pulses, retained data and reset zero | engine:901-906, :921-922, :1060-1067 | Match |
| 29 | Two in-band pairs complete correction | generator:1033-1043; engine:1060-1074 | Match |
| 30 | Unstarted disabled frame withdrawn; started frame finishes | serializer:127-132, :140-158 | Match |
| 31 | Path append, empty path, absent TLV retention | engine:1037-1053 | Match |
| 32 | Self publication at reset release | engine:889-900, :924-925 | Match |
| 33 | Low port clears outstanding claims | engine:1096-1102 | Match |
| 34 | First post-reset port sample is reference | engine:1116-1129 | Match |
| 35 | Parent slew connection now implemented | pinned parent shadow:150, :706; datapath:3061-3064, :7329, :8875 at 1e80128f | Match |
| 36 | Independent decode skips if dependency absent | tb/tsngen/run_tsngen.py:36-58 | Match; skip is not execution |
| 37 | Bare make adds parser/engine/gasket/decode mutants | respective Makefiles, all/default targets | Match |
| 38 | Publication changes only on commit | engine state writes and output assigns | Mismatch, F1 |

All four tracked generated images were regenerated only under scratch and matched byte-for-byte. The source-audit receipt records their hashes and generated packing reports.

Executable evidence

make -j16 docs passes: 14 current pages, 18 archived pages, 23 documentation self-test arms, 20 exact source anchors, 7 source-evidence self-test arms, 9 pinned diagram assets, 3 source-bound previews and 10 diagram self-test arms. make -j16 lint, make -j16 contract and the out-of-context clock checker self-test pass. The diff whitespace check passes. There is no repository .github workflow or additional standalone hygiene target in this checkout. Parent hygiene is separate from these source gates.

Fault probes use a disposable git archive beneath scratch. Unmodified control passes. Plain stale constant, stale ROM count and missing status row fail. Formatted/negative stale constants escape (F2). A duplicate identical ROM row also passes; this is supplementary robustness evidence, not a separate blocking finding. A drifted repeated threshold passes (F3). run_review_checks.py reproduces all arms and writes individual raw logs and return codes. No detached background jobs were used; independent short gates ran concurrently within one awaited foreground runner.

Start-here routing, glossary links and four role summaries exist and are readable. The status table covers each maintained page once; archived records have index entries and successor banners. The new archive removes the old workflow label from its copied prose. The review did not introduce any source comments. Current numerical and clause claims still fail F1/F3/F4, so the new Current labels are not yet justified for all pages.

Limits and pending duties

The public indexed 2011 standard corroborates the corrected neighbor-rate and propagation-delay clauses (11.2.15.2.3/.4) and role-selection section 10.3.12.1.4; the glossary Follow_Up reference is wrong. Direct retrieval of the indexed 2011 PDF returned 404, and the official Milan v1.2 PDF returned 403. Full corrigenda and every clause claim were therefore not independently re-certified from complete primary documents. Remaining edition checks must retain this limitation, including Figures 11-6/11-8 and Milan Annex B.1.1; no substitute edition was treated as the authority.

No full simulation bank, synthesis, parent builder/native bank, hosted acceptance, physical calibration or hardware run was performed here. Physical calibration is NOT RUN. Field skips are not hardware proof. There is no manager source bank at this head. The manager still owns the current-dev merge candidate against live dev 1e80128f0a467b58bf884b7d9bf62e013a2fb141, parent pin reconciliation, builder/native receipts and hosted/act acceptance. Source validation does not establish that candidate.

Public acceptance comments, exact published gate receipts and prior public FINDINGS have not yet been read at this independent seal. Their reconciliation will be appended after the seal; the independent findings above already establish NEGATIVE.

R740-1 FINISHED
