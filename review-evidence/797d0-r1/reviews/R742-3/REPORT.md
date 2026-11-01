[R742] NEGATIVE - exact head 808602e08daee5e86ae21026bbaf2f9114db077a

PR #815, issue #797, external independent round R742-3. Tree `999f44a433d47f07cb695bb495b543d3f45e8821`. Delta from round-2 head `3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee`, with live dev `1f29f189279f9fc0132f4918e47342b87d22f33a` merged in at `97c7c48594`. The live dev tip was read back and is `1f29f189`, an ancestor of this head.

All three of my round-2 findings are closed at their causes, and the new corrections are true against the source. The verdict is NEGATIVE for one reason that blocks and one that does not.

- **F1:** the corrections that closed round-2 F1 put a submodule source path into a tracked non-Markdown file. That breaks a required gate, so `rtl-fast` is red at this head and every other hosted context ended cancelled, including the docs workflow.
- **F2:** the cross-page search finds every recorded statement and spelling in today's tree, but three kinds of real copy still pass it.

## Findings

### F1 - BLOCKER - Conformance, RTL, Tests, Docs - `scripts/docs_inventory.json:445-446`, `:452-453`, `:459-460` - The new findings break the derived source-list gate, so `rtl-fast` is red

- **Authority:**
  - AGENTS section 7 requires a successful `rtl-fast` verdict on the current head.
  - `.github/ci-templates/rtl-fast.yml:119` runs `python3 scripts/pp_srcs.py --check --selftest`.
  - `scripts/pp_srcs.py:142-144` states the rule: no tracked file outside `PROSE_OK` may name a submodule source literally. `:169` skips only `.md` files, so the generated audit page passes and its data file does not.
- **Evidence:**
  - `receipts/pp-srcs-head.txt` reproduces it locally with rc 1: `scripts/docs_inventory.json: names submodule source(s) literally that are not permitted prose: protocol-processor/hdl/top/protocol_processor_top.sv`.
  - The hosted job fails on the same line: run 41349428937, job `verilator-lint`, step "Prove protocol-processor source lists are derived" (`receipts/hosted-exact-head.txt`).
  - The cause is isolated. In a disposable clone, round-2's data file gives rc 0, and this head's data file with only that literal respelled gives rc 0. Round-2 data has 0 such lines and this head has 6, all in D0-063, D0-064 and D0-065.
  - The author's 96 gate commands (`receipts/published-verification.log`) are all rc 0, but none of them runs this gate. The author's REVIEW READY discloses that hosted CI and the local replica were not run.
- **Impact:**
  - The required context fails deterministically on every push of this data.
  - The hosted step failed at 20:58:09. `docs-gates-0` to `-2` were cancelled from 20:59:22 and the inventory freshness step was skipped. `docs-check` then failed at "Require every gate exactly once". `elaborate` and `rtl-full` ended cancelled.
  - So this head has no hosted docs result, and gates behind the cancellation have no hosted result either.
- **Required outcome:** `scripts/pp_srcs.py --check --selftest` passes at the new head, with D0-063 to D0-065 still identifying the processor file and its lines precisely. Either path the gate allows is acceptable: spell the citation so it is not a literal source reference, or add the exact literal to `PROSE_OK` with its reason. If `scripts/pp_srcs.py` changes, check its command-table digest too. The audit page must be regenerated in the same change.
- **Verification:** run the gate locally, regenerate and run `docs_inventory.py --check`, then get exact-head `rtl-fast` and docs workflow results with no cancelled gate.

### F2 - MINOR - Conformance, Robustness, Tests, Docs - `scripts/docs_inventory.py:32-35`, `:137-138`, `:373-397`; `scripts/docs_inventory.json:22`, `:176`, `:246`, `:414` - The cross-page search misses real copies, one kind against the module's own claim

- **Authority:** the round-3 assignment says a recorded statement is searched, normalised, across every inventoried page, and each page carrying it gets a row and renders stale. The docstring at `:32-35` claims normalisation of "emphasis and code spans", and limits the known gap to a paraphrase.
- **Evidence:** `receipts/probe-e2e.txt`, planted on `docs/guides/BOARD_DEPLOYMENT.md` in a disposable clone. In each missed case `--check` fails only for the changed line count, then `--write` passes green with the contradicted statement on a page still marked `current`.

| Planted copy | After `--write` |
|---|---|
| Exact, block-quote wrapped, or a recorded `also` spelling | 1 row, stale |
| `_ADP, ... firmware._` (underscore emphasis) | 0 rows, current, rc 0 |
| One word of the statement as a Markdown link | 0 rows, current, rc 0 |
| "The protocol processor's NVM face is answered by a blank-flash responder." (D0-025's sentence, ended normally) | 0 rows, current, rc 0 |
| The same sentence-ending change for D0-035, D0-059 and D0-002 | 0 rows, current, rc 0 |

- **Causes:**
  - `INLINE_MARKUP_RE` strips only `` ` `` and `*`. `_` is also a word character, so the boundary check at `:394-395` refuses it too.
  - Link syntax is not normalised.
  - A recorded quote is a cut from one line, so it can carry words from the next clause: "`, so a`" in D0-025, "`, so the`" in D0-035, "`. The`" in D0-058 and D0-059, "`See the mandatory gaps in`" in D0-047, "`but nothing there`" in D0-002. These are the same sentence, not paraphrases, so the disclosed limit does not cover them.
- **Impact:** future only. No real-tree miss exists today (`receipts/probe-search.txt`).
  - An independent wider search, which also strips `_`, links and typographic variants, found two extra hits. Both are D0-040 and D0-058 on pages already holding the same words.
  - A 6-word fragment search found seven pages, none of them a missed copy. D0-001 on `AXIS_CORES_ON_BAREMETAL_SOC.md` is already held by D0-033. D0-025 on `docs/overview/ARCHITECTURE.md:102` correctly names `KL_nvm_backend`. D0-040 and D0-058 are held. The three D0-050 hits are generic table cells.
  - Underscore emphasis is rare: 1 line against 353 for asterisk emphasis, outside the archive and the audit page.
- **Required outcome:** a planted copy in each form above gets a row and a stale page. Alternatively, narrow the docstring to what is normalised and record each tail-carrying statement's own sentence under `also`. Either way the claim and the behaviour must agree.
- **Verification:** rerun `probe_e2e.sh` on a clone of the new head, and add one self-test arm per form kept.

### R1 - RESIDUE - Docs - `scripts/docs_inventory.json` D0-024 source cell (`:172`) - A line number reads as the wrong file

"`sw/litex/milan_soc.py` line 173; `nvm_commit()` (line 1405)" names `milan_soc.py` last, but 1405, 1656 and 1914 are firmware lines. The cited facts are true: `milan_baremetal.c:1405` is `nvm_commit`, `:1656` is `nvm_boot`, `:1914` is its call. Exact fix: write "`nvm_commit()` (`sw/firmware/milan_baremetal/milan_baremetal.c` line 1405)".

### S1 - SUGGESTION - Tests - `scripts/docs_inventory.py:137`, `:375`, `:417` - Four mutants survive the self-test

`receipts/mutants.txt`: 26 of 30 killed. The survivors are list markers no longer stripped, ordered-list markers no longer stripped, NFKC removed, and copies not added to `held`. The first two are close to equivalent for a statement that merely starts inside a list item, because the search matches inside the line anyway. The docstring still claims list markers, so an arm or a narrower claim would settle it. NFKC has no arm. The fourth is order-dependent and has no arm. All other cross-page mutants die, including the search-disabled one.

### S2 - SUGGESTION - Docs - `sw/trace/test_trace_roundtrip.py:17-18`, cited by D0-066 - The cited lines also repeat the claim D0-066 refutes

D0-066 cites these lines for "compile it on the host", which they support. They also say "the same barectf.c + milan_trace.c the bare-metal image links". `sw/firmware/milan_baremetal/Makefile:6` builds `milan_baremetal.o` alone, and no file under `sw/firmware` or `sw/litex` names the producer. D0-066 is true. A cold area lane would meet the conflict in the cited text, so a short note in the cell or an item for the comment's owner would help. It is not a Markdown page, so this does not widen the audit.

## Round-3 checks

### (1) Round-2 findings at the merged pin

| Prior item | Disposition | Evidence at this head |
|---|---|---|
| R742-2 F1 MAJOR, GET_STREAM_INFO ownership | RESOLVED at cause. F1 above is a new defect in how it was recorded, not a re-opening. | D0-063 (`INTEGRATION_GUIDE.md:60`), D0-064 (`:64`), D0-065 (`:65`). The page is stale, 3 findings. See the checks below. |
| R742-2 F2 MINOR, D0-035 third check | RESOLVED | `milan_baremetal.c:1869-1873` is the magic rejection and `:1879-1883` the CRC rejection. `MILAN_AEM_IMAGE_BYTES` only bounds the loop and the CRC at `:1874-1878`; no length is compared. `:1913` and `:1915` pass the verdict to `entity_advertise()`. |
| R742-2 F3 MINOR, D0-027 shipping producer | RESOLVED | The cell names the supplied producer's round-trip and states that the shipping image does not link it, in agreement with D0-048. `Makefile:6` confirms. D0-066 records the same sentence on `VERIFICATION_DEVELOPER.md:25`. |
| R742-2 S1 SUGGESTION, D0-042 scratch wording | RETAINED, optional | The correction is unchanged. |

GET_STREAM_INFO, read at processor pin `a9e84b66` (`receipts/citations-probe.txt`):

- `protocol_processor_top.sv:3593-3595` keeps selectors 5 and 7 away from the parent. `:3625` is the pass-through default and `:3626` the input gate, so an output's words are unchanged.
- `:3628` writes the failure code, `:3629` the bridge, `:3631-3632` the VLAN and `:3633` the status.
- `:3641-3643` clear `0x52000000`, the stream ID and the destination MAC while unsettled. 0x52000000 is bits 30, 28 and 25, matching the three flags named at `milan_datapath.sv:6195`, `:6197` and `:6200` by their position in the concatenation.
- `:3621` defines settled.
- Parent lines hold as cited: `milan_datapath.sv:6194-6217`, `:6401`, `:6413`, `:6421`, `:6430`, `:6444-6445`, `:6451`, `:6048-6053`, and `:6392-6456` as the answer block.
- Each selector 0 to 7 has its writer named. The logic at the earlier pin's cited lines was read and matches.

### (2) Cross-page search

- **Population:** an independent tracked listing equals the generator's 212 pages.
- **Real tree:** 65 recorded findings and 22 copy rows make 87 rows. Each copy I read is a real copy: `REQUIREMENTS.md:27`, `FR_NFR.md:322`, `TESTING.md:1810` and `FPGA_DESIGN.md:196`. The other 18 were read as rows in the audit, not on their pages.
- **Planted copies (exact, wrapped, block-quoted, `also`):** each fails `--check`, then gets its row and renders stale.
- **Named mutant:** with the search disabled, the self-test exits 1.
- **Other controls hold:** two spellings give one row, a longer word and a blank-line split give no row, and the audit page itself is not searched.
- **Exceptions:** F2 and S1.
- **Disclosed by the author and accepted as stated:** a paraphrase needs `also`; removing an entry removes its copy rows with no gate; a copy on an archive page keeps `obsolete` (9 rows), consistent with `status_rule()`.

### (3) Sampling

- **Corrections added or changed:** D0-001, 017, 027, 035, 063, 064, 065, 066. Each cites its source lines in its own cell, and I read every cited line.
- **D0-001:** `milan_soc.py:2854-2856` and `:4097`. True.
- **D0-017 and the removal of D0-009:** `phy_live = 1` at `milan_baremetal.c:1671` comes before the shape check, `:1099-1102` and `:1106` poll on both paths, and `:1900-1903` returns before `nvm_boot()`. `phy_link_tick` has no other caller. Both are true.
- **Restated sources:** D0-038 (`milan_soc.py:3270-3274`, `:4301`) and D0-062 (`SUBMODULES.md:511-517`, `AREA_BUDGET.md:149-150`, +0.365 ns, 63 of 15,850 slices) are true.
- **Moved citations, compared programmatically between rounds (top-level tree files only):** of 39, 28 carry identical text. The other 11 were read:
  - D0-024's three firmware lines, which my parser attributed to `milan_soc.py` (R1), all hold.
  - D0-034's two lines, which my parser also misattributed, hold: `milan_soc.py:1413` is `_AXIS_CDC_DEPTH = 16` and `:1810` is `tx_sf`.
  - D0-026 now starts at `INVENTORY=(`. D0-033 and D0-056 widen one line to three. D0-038 is the disclosed restatement.
  - D0-035's and D0-049's ranges start on the same text and extend over the merged function. Both ranges were read.
- **Kept citations:** 43 are unchanged. One kept citation now reads different text: D0-026's `run_litex_sims.sh:150`, which now correctly lands on `run_aggregate() {`.

### (4) Regenerated inventory and docs workflow

- **Inventory:** `--check` rc 0 at this head, and rc 0 in a clone with no submodules (`receipts/docs-gates-head.txt`, `receipts/probe-e2e.txt`). I parsed the page independently: 212 rows, 166 current, 25 stale, 21 obsolete; no current page has a finding row; no stale page lacks one (`receipts/audit-facts.txt`). `ci/image/command-table.json:13698` carries the generator's real digest.
- **Docs gates locally:** rc 0 for `docs_inventory.py --check` and `--selftest` (42 controls), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_baremetal_only.py --check`, `ci_gate_workflows.py --check`, `ci_events.py --check`, `check_py_idiom.py`, `check_hygiene.py --check`, and the ten in `receipts/more-gates-head.txt`. `gen_toc.py --verify-anchors` and `--check` refused here with rc 2 because the pinned Markdown renderer is not installed on this host; the author's receipts show rc 0.
- **Docs workflow hosted: NOT passed.** The run concluded cancelled, `docs-check` failed, and the inventory step was skipped, all downstream of F1. `docs-check-no-git` and `wire-accountability` succeeded.

### Other delta checks

- **Published evidence:** all 129 author-round-3 files match the public manifest. The 96 gate rows are all rc 0. The evidence commit `03ffa10d` is unsigned, so I verified content hashes, not a signer.
- **Scope:** the delta after the merge touches the docs template, command table, audit page, data file and generator only. No RTL, firmware or gitlink differs from dev.
- **Comment rule:** the added comments and docstrings name no lane, round, reviewer, bench label or comment ID. `D0` strings in the delta are finding identifiers and existing rendered labels, not new comment labels. No residue from this rule.

## Prior public findings reconciled at this head

My verdict and ledger were saved in the report before I read any other reviewer's finding. I then read the published R741-2 report's findings section only. I did not read R741-3 or any other in-flight report.

| Prior item | Original lenses | Disposition |
|---|---|---|
| R741-2 F1 MINOR, `REQUIREMENTS.md:27` still current | Conformance, Docs | RESOLVED. The search gives the row and the page is stale. All copies now carry one judgement, and D0-001's correction sends the normative copy to a maintainer decision. That decision is still open. |
| R741-2 S1 SUGGESTION, escaped-pipe parser | Tests | RETAINED, optional. `parser-cells-ignore-escapes` still survives in the author's published receipt. |
| R741-2 S2 SUGGESTION, statements checked per page | Docs | RETAINED, optional. The page's baseline sentence remains. |
| R741-2 S3 SUGGESTION, re-verify row passes once regenerated | Robustness | RETAINED, optional. Designed behaviour; there are no re-verify rows at this head. |
| R741-1 S1, S2, S3 SUGGESTION | Gate, source comments, ownership | RETAINED, optional, as at round 2. |

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Round-3 assignment items 1-4; AGENTS section 7; D0-001, 017, 027, 035, 063-066 against their cited lines; `REQUIREMENTS.md:27` | R742-3 | 808602e08daee5e86ae21026bbaf2f9114db077a |
| RTL | UNCLEAN: F1 only | `scripts/pp_srcs.py:142-186` source-list contract; `protocol_processor_top.sv:3593-3648` at `a9e84b66`; `milan_datapath.sv:6048-6053`, `:6194-6217`, `:6392-6456`. The recorded ownership facts are true. | R742-3 | 808602e08daee5e86ae21026bbaf2f9114db077a |
| Robustness | UNCLEAN: F2 | `docs_inventory.py:365-420` against 25 planted spellings and 9 end-to-end arms; wider real-tree search; firmware refusal paths `milan_baremetal.c:1671-1686`, `:1900-1903` | R742-3 | 808602e08daee5e86ae21026bbaf2f9114db077a |
| Tests | UNCLEAN: F1, F2 | Hosted runs 41349428937 and 41349429098; author's 96 gate rows; 42 self-test controls; 30 own mutants; focused local gates | R742-3 | 808602e08daee5e86ae21026bbaf2f9114db077a |
| Docs | UNCLEAN: F1, F2 | `scripts/docs_inventory.json` delta; regenerated audit page and its counts; generator docstring; moved-citation comparison | R742-3 | 808602e08daee5e86ae21026bbaf2f9114db077a |

All five lenses were applied. No lens is banked clean while a listed finding is open. R1 and S1-S2 do not affect coverage.

## Real limits

- **Broader gate replay not done.** A replay of the remaining pure-Python gates listed in `receipts/py-gates.list` was declined by this session's permission mode, and I did not work around it. I ran 22 focused gate commands instead, two of which refused for the missing renderer. Because the hosted runs were cancelled, a further gate failure behind F1 cannot be excluded until those runs complete.
- **Hosted cancellations.** I read the failed job behind F1 and the `docs` job steps. I took the failures in `elaborate` and `rtl-full`, named "Require ..." and "Union ...", from job and step names as consequences of cancellation. I did not inspect them individually.
- **Not run:** full parent, processor, gPTP, Yosys or builder banks; Docker or the local replica; hardware. Physical calibration is NOT RUN, and field skips are not hardware proof. No manager source bank exists or is inferred at this head.
- **Standards:** licensed clause text was not re-derived. The bit meanings of `0x52000000` were checked against the repository's own Table 5.9 comments and field order.
- **Audit coverage:** this is a delta review and does not extend the sweep. The author discloses that dev's new lines on release-facing pages were not checked statement by statement, and that round 2's 823 read-only statements remain read-only.
- **Tree integrity:** `receipts/tree-integrity.log` rc 0. All tracked blobs of the root (1,461) and five initialised dependencies match in bytes, modes and index at their pinned commits. Optional `external` remains uninitialised. Mutants and plants ran in scratch clones or scratch copies. Read-only gates ran in the reviewed clone, which is clean.

## Pending manager duties

- Return F1 and F2 to the executor, then re-review the corrected commit.
- Obtain the maintainer decision on what "Mark II default" names. D0-001, D0-033 and D0-056 and nine copy pages depend on it.
- Decide how the owner additions of 2026-10-30 apply. The author records them as not applied.
- Carry R1 to the residue checklist.
- Own hosted and local-replica acceptance on the corrected head, the second independent verdict, current-dev candidate validation, merge authorization and containment.

No merge approval is given.

R742-3 FINISHED
