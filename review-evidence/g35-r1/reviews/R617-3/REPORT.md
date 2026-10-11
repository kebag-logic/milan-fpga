[R617] POSITIVE - exact head 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c

External independent delta review of issue #35 / PR #80, round R617-3. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains open. Two wording-only residues and three optional suggestions are recorded below, including retained prior findings.

The merge preserves the reviewed receive-error implementation and tests. Every file and mode matches a mechanical three-way merge except the two declared documentation conflicts. Each resolved file equals main's version with only its #35 risk entry removed. The remaining #48 gaps and parent citations are intact. Documentation gates pass.

Exact tree: `526a366bd9aff5cd8d0ad0278217dab22ac921ea`. Parents: `a70e38804cb16435c089d024c58e8c3fb4d39ff6` and `155de13789ac85bab7a14bea0ae86d1c376b490a`. Source/merge base: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The main parent contains PR #79's OOC clock changes and PR #81's #48 documentation alignment. [History](receipts/history.txt), [base diff](receipts/base.diff), [delta diff](receipts/delta.diff), [mechanical merge audit](receipts/merge-audit.log).

Reconstruction followed the requested order: session instructions and absence of repository AGENTS.md/CONTRIBUTING.md; docs map and README; issue acceptance and public scope decisions; linked parent requirements and interface sources; base/head diff and history; public author execution evidence and manager comments. The independent verdict and five-lens ledger were written to [INDEPENDENT_VERDICT.md](INDEPENDENT_VERDICT.md) before opening prior review comments. All prior public findings were then reconciled. The final refresh found no additional PR comments, submitted reviews or inline review comments. [Refresh receipt](receipts/public-refresh.txt).

**Conformance — CLEAN.**

[Issue #35](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35), the [any-byte scope decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6104916029), and the later [bank-write ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6105869522) bind this review. A valid-byte error refuses its complete frame with one drop and no event. Writes through the flagged byte's own parser-output edge are permitted; later writes are forbidden. Refused words are undefined and never named by an accepted event. The next accepted event must see its own frame's fields. The issue body's original zero-total-writes requirement was expressly amended, resolving R617-F1.

The contract remains intact in `hdl/wire/KL_gptp_rx_parser.sv:52-66,113-116` and `docs/INTEGRATION.md:65-106`. The merge audit separately verifies byte-identical receive sections in the integration and HDL guides. `feed_gap` explicitly drives the error input at `tb/verilator/parser/sim_main.cpp:258`, already true at the source base. No current README contains a parser total requiring revision; dated historical totals remain historical.

[Issue #48's scope](https://github.com/Mister-M-alt/FPGA-gPTP/issues/48#issuecomment-6105890010) requires default-on product ownership, the verification-only option-off path and visible remaining gaps. All 31 parent citation occurrences resolve to 14 distinct targets at `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. Direct comparison confirms the default-on parameter, fabric ownership, safe option-off publications, CSR selection, and control-TX bypass. Parent REQUIREMENTS.md:156-171 and GPTP_PLANE.md:350-366 retain the single owner of calibration constants and the exclusion of donor live tuning. README:51-55 and MANAGER:103-115 retain #58, #117, #64 and #488. Dropping their fixed #35 risk entries does not erase those remaining gaps. [Citation receipt](receipts/citations.log), [pinned authorities](authority/REQUIREMENTS.md).

**RTL — CLEAN.**

All 32 tracked `hdl/` and `tb/` paths, including parser RTL, harness, mutation definitions and images, are byte- and mode-identical to `a70e3880`. The root Makefile gains only the imported OOC checker selftest. The merge introduces no parser, engine or microcode behavior change. Three non-conflicted documentation files combine normally; README and MANAGER each differ from the main parent by exactly one removed #35 entry. [Merge audit](receipts/merge-audit.log).

The source-base repair at parser:652 sets existing `bad_r` only inside `rx_valid_i`, after the SOF clear at :411. Thus first-byte errors survive that clear. The direct EOF term at :632 handles the last byte before the register update becomes visible. Common writes use `!bad_r` at :460-480; body writes are inside the same guard at :487. The deferred event/write path requires `fin_ok_r` at :393-404. The new latch adds no separate drop-counter increment. Reset and a fresh SOF clear prior poison.

Engine:167 forwards the input to the parser. Bank selection advances on an accepted event at :307-308, matching the retained-bank successor oracle. Engine:275-279 releases a poisoned Announce reservation without an accepted event; :896-910 copies only the qualified path and clears inactive publication words. These consumer observations are source inspection, not a new engine error-input simulation.

The pinned parent wrapper ties `rx_err_i` low at `KL_gptp_shadow.sv:666`. Public author evidence at `a70e3880` records hierarchy counts 3567/3568, identical flattened statistics at 2432 cells and identical ROM digests; the [manager ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6105366046) accepts the hierarchical extra mux. Earlier public equivalence summaries report 748/748 tied-input cells proven, with `bad_r` unproven when the input is free. Those are inspected published measurements, supported here by unchanged production bytes; they are not new synthesis or proof runs at this merge head. No byte-identical raw netlist dump is asserted. [Author proof summary](public/author/evidence/equiv/summary.txt), [parent identity](public/author-r2/evidence/r2/parent/head/identity.txt), [flattened statistics](public/author-r2/evidence/r2/parent/head/flat.stat.txt).

**Robustness — CLEAN.**

Fresh execution covers the four required message types at all 284 byte positions, held errors, error-free recovery, invalid-cycle errors and eight immediate refused/clean successor pairs. The bank is retained across each pair; every expected successor field is compared at the accepted event. The first/middle/EOF write oracle also covers Announce's deferred write. No later write or refused event appeared. [Parser runtime](receipts/parser.log).

The following are before/on/after write counts at the parser's registered output edge. Every cell represents one drop and zero events; these are not physical memory-write timing measurements.

| Type | First byte | Byte 29 | EOF |
|---|---|---|---|
| Sync | 0 / 0 / 0 | 0 / 1 / 0 | 5 / 1 / 0 |
| Follow_Up | 0 / 0 / 0 | 0 / 1 / 0 | 7 / 0 / 0 |
| Pdelay_Req | 0 / 0 / 0 | 0 / 1 / 0 | 4 / 0 / 0 |
| Pdelay_Resp | 0 / 0 / 0 | 0 / 1 / 0 | 7 / 1 / 0 |
| Announce without PathTrace | 0 / 0 / 0 | 0 / 1 / 0 | 6 / 1 / 0 |

Eight planted defects all fail their assigned names: EOF-only sampling, lost first-byte flag, ignored EOF flag, repeated drop counting, ignored errors, persistent poison, gap sampling and skipped successor w2. The EOF-only control fails 27 required names; skipped w2 fails all eight stale-word names. This round reruns the committed controls with bounded build plumbing, rather than claiming a new independently designed stimulus campaign. [Mutation ledger](receipts/mutations.log), [EOF-only raw result](receipts/mutation-case1-run.log), [stale-word raw result](receipts/mutation-case8-run.log).

**Tests — CLEAN.**

The scoped compiler's 5.050 identity and executable digest were checked before use. Independent check streams ran concurrently under a foreground coordinator, with at most two four-job compiler builds and no detached jobs. All exports, object files and mutated source copies stayed under packet `scratch/`. [Identity receipt](receipts/compiler-identity.txt), [portable runner](run_focused.py).

| Exact-head local execution | Result | Receipt |
|---|---|---|
| Parser suite | 337 PASS, 0 FAIL; rc 0 | [parser](receipts/parser.log) |
| Clean control plus eight committed mutants | 9/9 expected outcomes; all eight defective runtimes rc 1, all named failures present | [ledger](receipts/mutations.log) |
| `make -j16 docs`, including diagram/source checks and selftests | rc 0; 9 assets, 3 bound previews; 11 current/17 historical pages; 20 exact anchors; selftests 10/10/7 arms | [docs](receipts/docs.log) |
| `make -j16 contract` | rc 0 | [contract](receipts/contract.log) |
| Imported OOC precheck and selftest | rc 0; 30 selftest arms | [precheck](receipts/ooc-clock.log), [selftest](receipts/ooc-clock-selftest.log) |
| Merge/content/index and citation audits | rc 0 | [merge](receipts/merge-audit.log), [citations](receipts/citations.log) |

The supplied [public evidence commit](https://github.com/kebag-logic/milan-fpga/tree/3e8c823acbb589151b5ccfd53f1399a89f4fa6ae/review-evidence/g35-r1) now contains raw round-two author gates. All 24 selected downloaded receipts match their published SHA-256 values. The gate identity explicitly names `a70e38804cb16435c089d024c58e8c3fb4d39ff6`, with tb/contract/lint/docs all rc 0. The logs show parser 337 plus 9/9, engine 1613 three times plus 34/34, and the other donor suites passing. This closes the earlier public-evidence availability limitation; it does not turn those gates into full execution at `49b9d0f`. [Download index](public/download-index.json), [author identity](public/author-r2/evidence/r2/gates-head/identity.txt), [gate exits](public/author-r2/evidence/r2/gates-head/rc.txt), [raw suite log](public/author-r2/evidence/r2/gates-head/tb.log).

**Docs — CLEAN.**

README and MANAGER retain the complete #48 gap list/table, exact parent citations and physical acceptance limits. The fixed #35 entries are the only conflict-resolution removals. Integration:71,84-106 states the any-valid-byte contract, inclusive write boundary, undefined refused words, clean next event and ignored invalid-cycle errors. Parser header/port and the preserved HDL receive section agree. Source anchors :393 and :475 remain exact. The inherited OOC figures explicitly name their measured base and distinguish constrained synthesis from historical unconstrained reports; they are not presented as measurements of this source head. Two prose residues below do not alter the contract or the measured evidence.

**Prior findings and current residue.**

The [round-one internal findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/80#issuecomment-6105577480), [round-one external finding](https://github.com/Mister-M-alt/FPGA-gPTP/pull/80#issuecomment-6105855128), [round-two internal findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/80#issuecomment-6106661289) and [round-two external dispositions](https://github.com/Mister-M-alt/FPGA-gPTP/pull/80#issuecomment-6106691388) were read after the independent verdict. Their disposition at this exact head is:

- **R617-F1 — MAJOR — RESOLVED — Conformance, RTL, Tests, Docs.** Artifact: parser:52-66,113-116,632,652; harness:215-299,1415-1501; PR acceptance item 2. Authority: public bank ruling 6105869522. The original zero-write mismatch would leave acceptance unproved. Required outcome was an explicit amendment plus aligned all-write oracle, successor proof and docs, or buffering. The amendment selects the first outcome. Fresh before/on/after results, eight clean successors and eight named skipped-w2 failures verify it. No open action remains.
- **R616-1-RES1 — RESIDUE — RESOLVED — Docs.** Artifact: parser:60-63 and PR opening/acceptance prose. Evidence: byte 29 may write w1 on its own edge. Exact required text, now present: “No bank write follows the flagged byte's own edge; words written up to and including it stay in the write bank like those of any refused frame, unnamed by any event.” The corresponding PR substitutions are present. Impact was prose precision only. Verification: direct text comparison and reproduced byte-29 count.
- **R616-1-S1 — SUGGESTION — RETAINED — Docs, Tests.** Artifact: `docs/SOURCE_EVIDENCE.md:12` and `scripts/check_source_evidence.py`. The any-byte row remains an unanchored file link outside the anchored expected map. Impact: that row does not detect future structural drift; functional tests still exercise the behavior. Optional outcome: anchor the latch and register the expected construct when that checker is next changed. Verification: the new anchor is checked and a moved/deleted construct fails. The main merge does not implement this suggestion.
- **R616-1-S2 — SUGGESTION — PARTLY ADDRESSED; REMAINDER RETAINED — Tests, Robustness.** Artifact: harness:1269-1288,1345,1417. Announce now participates in the before/on/after oracle. Additional-type, PathTrace, padding, runt and broader adjacency coverage remains in prior reviewer probes. Impact: some useful extra coverage is not a permanent donor regression. Optional outcome: retain selected cases in the suite. Verification: production controls and named defects distinguish each added behavior. The unchanged harness introduces no new obligation in this merge.
- **R616-2-RES1 — RESIDUE — RETAINED — Docs.** Artifacts: `docs/TEST_DEVELOPER.md:96` and `tb/verilator/parser/README.md:16`. The bank ruling and current runtime INFO lines allow refused words to remain, whereas these summaries say no stale words are left. Impact is wording only: the proven property is exclusion from the next accepted event. Exact fixes: `- Proves no refused frame's word reaches the next accepted event.` and `It proves no refused frame's word reaches the next accepted event.` Verification: compare these sentences with the retained-bank oracle and current INFO output. Carry to the residue checklist; no test, figure, contract, code or verdict changes.
- **R616-2-S1 — SUGGESTION — RETAINED — Tests, Robustness.** Artifacts: harness:1269,1337 and mutation definitions. The four permanent sweep frames end at declared length; they do not flag padding. The earlier reviews demonstrated a padding-only defect that survives the committed suite but fails their expanded probe. This round confirms those source files are unchanged and does not relabel that prior experiment as a fresh run. Impact: a possible future padding regression lacks a permanent error-position control. Optional outcome: add padded Sync bytes 58/59 and a padding-specific named mutant. Verification: production passes and that mutant fails the new names. This refines S2 and remains optional.
- **R617-3-RES1 — RESIDUE — OPEN — Docs.** Artifact: PR body, final paragraph of “Change”: “Nothing outside the parser, its tests and its documentation changes. No microcode, no engine RTL, no checker script.” Authority/evidence: the actual diff and merge parents now include main's OOC checker and documentation updates. Impact: this prose describes the author-only change without identifying the later import. Exact replacement: “The #35 commits change the parser, its tests and its documentation. This head also merges main's #79 OOC checks and #81 documentation alignment. Microcode and engine RTL are unchanged.” Verification: compare with both-parent history and the merge audit. This is only a clarification of the scope sentence; it changes no measurement, figure, verdict, test, code, generated artifact, requirement or clause claim. Carry to the residue checklist.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #35 frozen acceptance and amendments; #48 scope; pinned parent requirements/ownership/calibration; preserved receive contract; resolved R617-F1 | R617-3 independent delta and focused rerun | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| RTL | CLEAN | Parser latch/SOF/EOF/write/count paths; engine forwarding/bank/context; every merged blob/mode; previous-head identity; inspected author proof/ROM receipts | R617-3 independent delta and focused rerun | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Robustness | CLEAN | Every-byte and held/gap checks; before/on/after oracle; immediate successors; eight named mutant failures; retained optional padding coverage | R617-3 independent delta and focused rerun | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Tests | CLEAN | 337 parser checks; 9 mutation outcomes; docs/diagram/source selftests; contract; OOC precheck/30 arms; accurately scoped published source gates | R617-3 independent delta and focused rerun | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Docs | CLEAN | README/MANAGER conflict resolutions; receive header/port/guides; 31 pinned citations/14 targets; dated OOC notes; prior dispositions and wording residues | R617-3 independent delta and focused rerun | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |

**Limits and pending manager duties.**

No manager source bank ran at this exact head; none is claimed or inferred. Full source-gate execution evidence is the author's published `a70e3880` receipts, with the unchanged-content bridge and this round's focused exact-head checks stated separately. No full parent, protocol-processor, gPTP, synthesis or builder bank ran here. The imported OOC checker/selftest passed; no new OOC synthesis or timing measurement was performed. Parser-level behavior does not establish arbitrary downstream queue capacity, abandoned-frame accounting without EOF or physical receive behavior. Prior broader probes are retained as earlier evidence, not rerun claims.

Exact-head queries returned zero workflow runs, zero check runs and zero individual statuses; the empty aggregate status is `pending`. Thus there are neither executed nor skipped source hosted jobs to count in this snapshot. This is not hosted acceptance. [Runs](public/hosted-runs.json), [checks](public/check-runs.json), [statuses](public/commit-status.json).

Physical calibration **NOT RUN**. Field skips and historical silicon records are not hardware proof for this head. Parent #117, #64 and #488 remain open acceptance/calibration work. No certification claim is made.

The manager owns hosted/local-workflow acceptance, the required second independent exact-head positive review and the full completion bar. At the merge turn, the manager must build and validate the final current-dev candidate using builder and native banks, with source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and stated live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, then link its receipts on the PR. That candidate validation remains distinct from source validation. Carry R616-2-RES1 and R617-3-RES1 to the residue checklist. Parent adoption remains separate; review its new gitlink and ROM-ledger row together.

Final integrity verification checks all **107 tracked filesystem blobs and executable modes**, every index entry, exact head/tree and a clean worktree. This donor contains **zero nested submodule gitlinks**. The pinned parent's five gitlinks were read from its public tree; its `gptp-processor` still names source base `5dce647a`, with the other pins recorded in [parent-gitlinks.json](public/parent-gitlinks.json). No parent checkout or gitlink was changed. All builds and mutations stayed in packet scratch; original source bytes never changed. No source fixes, commits, pushes, GitHub writes, author contact or repository merge occurred.

[Reproduction instructions](REPRODUCE.md) identify portable scripts and expected positive/negative exits. `MANIFEST.sha256` lists every selected publishable receipt and script; scratch and all unlisted files are excluded. REPORT.md is the terminal review artifact.

R617-3 FINISHED
