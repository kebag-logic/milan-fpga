[R741] NEGATIVE - exact head 808602e08daee5e86ae21026bbaf2f9114db077a

Internal cleared-context review of kebag-logic/milan-fpga PR #815 (#797 lane D0) into `dev`, round R741-3. This is a delta review over the round-2 head `3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee`, with live dev merged in. Head tree `999f44a433d47f07cb695bb495b543d3f45e8821`; source base and live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`; processor pin `a9e84b66`, gPTP pin `135afd04`.

## Verdict basis

There is one open BLOCKER, F1 (Conformance, Tests, Docs). The delta makes a required hosted gate fail, and nothing else in this round's audit content is wrong. D0-063 to D0-065 write the literal path `protocol-processor/hdl/top/protocol_processor_top.sv` into `scripts/docs_inventory.json`, and `scripts/pp_srcs.py --check` refuses that literal outside `.md` files and `PROSE_OK`. `rtl-fast` therefore fails on this exact head, and its fail-fast cancels the docs workflow before the inventory gate runs.

The four items this round was asked to check, apart from that gate failure:

| Check | Result | Evidence |
|---|---|---|
| (1) Round-2 findings closed | Yes, each true against the merged pin | Section "Prior findings" |
| (2) Cross-page search | Yes at this tree: all 87 rows and every recorded spelling confirmed by a separately written search; planted copies fail | Section "Cross-page search" |
| (3) Corrections cite lines in their own cell, and are true | Yes: 8 of 8 changed corrections cite lines; every sampled line holds | Section "Sampling" |
| (4) Inventory describes the merged tree; docs workflow passes | Inventory yes. **Docs workflow: every local gate that could run here passes, but the hosted docs workflow did not pass** (F1) | Section "Inventory and gates" |

## Findings

### F1 - BLOCKER - Conformance, Tests, Docs - `scripts/docs_inventory.json:445,446,452,453,459,460` - the literal processor path fails `scripts/pp_srcs.py --check`, so the required `rtl-fast` context is red and the docs workflow is cancelled

Authority/evidence:

- AGENTS section 7 requires a successful `rtl-fast` verdict on the current head. `CONTRIBUTING.md:56-57` lists `rtl-fast` and `docs-check` among the seven required contexts. #797 acceptance requires all docs gates to pass. `CONTRIBUTING.md:514-515` states the rule the gate enforces.
- `scripts/pp_srcs.py:169` exempts `.md` files and `protocol-processor/` itself. `:178-186` refuses a literal in any other tracked file unless it is listed in `PROSE_OK`. The JSON data file has neither exemption. The rendered audit page does, which is why the page passes and the data file does not.
- Round-2 data had 0 occurrences of the literal. This head has 6, all added by D0-063, D0-064 and D0-065.
- Reproduced locally at this head: `python3 scripts/pp_srcs.py --check --selftest` rc 1 (`receipts/pp_srcs_check_head.txt`). In a disposable copy with only those 6 literals reworded, the same command gives rc 0.
- Hosted, exact head, run 41349428937, job `verilator-lint`, step "Prove protocol-processor source lists are derived": exit 1 with the same message. The watcher logs `{"first_failure": "verilator-lint"}` and cancels the sibling runs (`receipts/hosted_verilator_lint_excerpt.txt`).
- Failures were real or follow-on, per `receipts/hosted_jobs_at_head.tsv`:
  - the one real gate failure is `verilator-lint`;
  - `docs-gates-0` was cancelled at step 31, before step 50 "Documentation inventory freshness gate" ran;
  - `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability` then failed at their "every gate exactly once" or receipt steps because cancelled jobs left no receipts.
- `wire-accountability`, `docs-check-no-git` and `full-ci-gate` passed. Dev's push runs at `1f29f189` were `success` for `docs`, `elaborate`, `rtl-fast` and `rtl-full`, so the failure is this delta's.
- The author's "96 of 96" list is the docs workflow only and does not contain this `rtl-fast` command. The PR's "How to validate" list omits it too. So a cold reviewer following the PR gets all green on a head whose required context is red, and the PR body still reads `GREEN`.

Impact: the PR cannot merge. No hosted docs-workflow run at this head has executed the inventory gate. Later workflow gates at this head have no hosted evidence at all.

Required outcome: `python3 scripts/pp_srcs.py --check --selftest` exits 0 at the new head without weakening the gate. The gate's own message offers one route, an exact `PROSE_OK` entry with its reason; the other is a citation form that is not the literal path and still lets a reader find the file. The PR's status and validation list name the repository-wide gate, and any hand-off runs it.

Verification: the command above at the new head; exact-head hosted `rtl-fast`, `docs-check` and the remaining required contexts; `python3 scripts/docs_inventory.py --check` and `--selftest` after the data change.

### R1 - RESIDUE - Docs - PR #815 body, "Known limitations" - stale statement about the push

Exact fix: delete "Hosted CI and the local replica have not run on this head; it is not pushed." and state the hosted result of the head then under review. The head was pushed; hosted runs exist.

### R2 - RESIDUE - Docs - `scripts/docs_inventory.json:453` (D0-064 correction) - citation is one line short

The correction cites "probing_status other than PROBING_COMPLETED (line 3621)". The PROBING_COMPLETED test is at `protocol_processor_top.sv:3622`; line 3621 is the index bound of the same predicate. Exact fix: "(lines 3621-3622)". The behaviour stated is true for every in-range input.

### R3 - RESIDUE - Docs - `scripts/docs_inventory.py:33`, PR body - "emphasis" means asterisks only

`INLINE_MARKUP_RE` at `:138` strips `` ` `` and `*`; `__x__` and `_x_` are not stripped. Exact fix: "asterisk emphasis". S1 covers the behaviour. A search of tracked Markdown outside the archive finds this form in one file, and the separately written search that does strip it adds no row at this tree.

### S1 - SUGGESTION - Robustness, Tests - `scripts/docs_inventory.py:137-138,373-377` - markup forms the search does not see

`receipts/plant_probes.txt`: each form below, planted on a current page, gives no row, and the page stays `current` after `--write`. `--check` fails first only because the line count moved.

- a word in a Markdown link;
- `<br>` or `<b>`;
- a `\` hard break;
- underscore emphasis.

Of 213 planted forms (every statement and spelling, in three shapes), 211 are found. The other 2 are D0-013 wrapped before its `+`: "`MILAN_N_TALKERS`\n+ 1 in" has the `+ ` removed as a list marker. No real page is affected at this tree (`receipts/independent_search.txt`, `receipts/raw_wrap_search.txt`). The PR discloses the paraphrase limit, and `also` can record any of these spellings. Strip link targets and inline HTML if a future copy needs it.

### S2 - SUGGESTION - Robustness - `scripts/docs_inventory.py:355` - a spelling that normalises to nothing is accepted

`"also": ["**"]` passes the `value.strip()` refusal and matches every page: 199 D0-001 rows. `"also": ["the"]` gives 204. This fails loudly in the diff, so it is not a silent defect. Refusing an empty `normal_form` would close it; the existing control only tries `" "`.

### S3 - SUGGESTION - Tests - `scripts/docs_inventory.py` `--selftest` - mutants that survive

`receipts/mutants3.txt`: 27 mutants, 22 killed by the self-test. Survivors:

| Mutant | Reading |
|---|---|
| `no-nfkc` | no arm exercises compatibility normalisation |
| `no-whitespace-collapse` | no arm has inner double spaces |
| `held-not-updated` | the real tree's `--check` catches it (rc 1), the fixture does not |
| `origin-rows-use-search` | no arm has a wrapped recorded quote |
| `copies-only-at-recording-order` | contrived; it drops the last page, which holds no fixture copy |

The named mutant `search-disabled` is killed. The author's published list (36 of 36 killed) does not contain these five, so the two lists do not conflict. Carried from R741-2 S1: `parser-cells-ignore-escapes` still survives.

### S4 - SUGGESTION - Docs - `sw/trace/test_trace_roundtrip.py:17-18` - the cited lines also carry the contradicted claim

D0-066 cites these lines as compiling the producer on the host, which is true. The same sentence says "the same barectf.c + milan_trace.c the bare-metal image links", which D0-048 and D0-066 contradict. The script is not an inventoried page, so no row reaches it. Naming it in D0-066's correction would give the area lane the second copy.

Carried, unchanged and optional: R741-2 S2 (per-page checked counts), R741-2 S3 (a committed re-verify row passes; none exists at this head), R742-2 S1 (the word "scratch" in D0-042).

No new source-comment label: the added lines in `docs_inventory.py`, the workflow template and `ci_events.py` carry no bench label, lane name, review round, reviewer ID or comment ID. "Area lane" in the generator is a pre-existing generic term and is only generated-page text or a re-flowed docstring line.

## Prior findings, judged at this head

Read after the independent pass above.

| Prior finding | At `808602e0` | Result |
|---|---|---|
| R741-2 F1 MINOR, `REQUIREMENTS.md:27` current | Copy row D0-001 at line 27 from the search; page stale; conflict published for a maintainer decision in the PR and REVIEW READY | RESOLVED |
| R742-2 F1 MAJOR, GET_STREAM_INFO ownership | D0-063 (:60), D0-064 (:64), D0-065 (:65); page stale with 3 findings. Selectors 0, 2, 4, 5, 6, 7 and the Stream Output pass-through read against `protocol_processor_top.sv:3593-3595,3624-3648`, and the parent's `milan_datapath.sv:6048-6053,6194-6217,6392-6456`. Mask `0x52000000` decoded to bits 30, 28, 25 = STREAM_ID_VALID, STREAM_DEST_MAC_VALID, STREAM_VLAN_ID_VALID. The old-pin lines 3573-3574 and 3581-3585 show the same logic | RESOLVED; carrying F1 and R2 |
| R742-2 F2 MINOR, D0-035 | Two predicates: magic `:1869-1873`, CRC `:1877-1883`; `MILAN_AEM_IMAGE_BYTES` only bounds at `:1874-1878`; verdict `:1913,:1915` | RESOLVED |
| R742-2 F3 MINOR, D0-027 | "Supplied" producer, not linked: Makefile line 6 is `OBJECTS = milan_baremetal.o`; no non-`sw/trace` source includes `milan_trace.h`; D0-066 records guide line 25 | RESOLVED |

## Cross-page search

- `scripts/independent_search.py`, written apart from the generator and with a stronger normaliser, searches all 65 findings and spellings over 211 pages. Every one of the 87 audit rows is found.
- It reports two pairs with no row, both correct under the designed "already held" rule: D0-040 on `REGISTER_MAP.md` (D0-058 records those words there) and D0-058 on the archive `MILAN_V12_DEPENDENCY_MATRIX.md` (D0-040's row holds them). `scripts/raw_wrap_search.py`, which keeps line markers, reports the same two.
- All 22 copy rows were read as a list; sampled contexts such as `TESTING.md:1810`, `FPGA_DESIGN.md:196` and `FR_NFR.md:322` are real copies, not false matches.
- Planted through the real gate on a current page, each of these gives its own row and `stale` after `--write`: plain, wrapped block quote, bold and code, table cell, upper case, no-break spaces, CRLF wrapped, wrapped list, and the origin quote copied elsewhere (`receipts/plant_probes.txt`).
- The author's claims hold: 13 pages carry the placement judgement, and 9 of them carry nothing else, so they would return to current.
- An archive copy keeps `obsolete` rather than `stale`. The assignment says "stale", but #797 keeps the archive unedited, the page is not `current`, the status rule holds, and the PR discloses it. Not a finding.

## Sampling

- Corrections changed or added: D0-001, D0-017, D0-027, D0-035, D0-063, D0-064, D0-065, D0-066. Each cites source lines in its own cell (`receipts/json_delta.txt`).
- All citations printed at the head (`receipts/citations_at_head.txt`); no path is missing and no line is past end of file.
- 35 citations the round left unchanged were compared across the merge: identical text at `1e80128f` and the head (`receipts/citations_unchanged_compare.txt`).
- Read and true at the merged tree:
  - D0-001: `milan_soc.py:2854-2856,4097`.
  - D0-017: `milan_baremetal.c:1099-1102,1106,1671,1900-1903`; `milan_soc.py:1958-1972,2184-2185`.
  - D0-024, D0-040, D0-049: `:1405,:1656,:1914`; `milan_soc.py:173`.
  - D0-025: `KL_pp_shadow.sv:1128`.
  - D0-026: `run_litex_sims.sh:99-108`.
  - D0-034: `milan_soc.py:1413,1810,1871-1873`.
  - D0-036: `:3287-3302,:3309`.
  - D0-038, D0-039: `:3270-3274,:4298-4301`.
  - D0-047: `README.md:136-139`.
  - D0-061: `:1828`.
  - D0-062: `SUBMODULES.md:511-517`, `AREA_BUDGET.md:149-150`, `BAREMETAL_FIRMWARE.md:2291`.
- D0-009's removal is correct: `phy_live = 1` at `:1671` precedes the shape check, and `:1099-1102` ticks the PHY on that path, so `REGISTER_MAP.md:423` is true past `nvm_boot()`. D0-017 carries the remaining identity-mismatch case.

## Inventory and gates

- `docs_inventory.py --check` rc 0 (550 lines), `--selftest` rc 0 (42 controls). `git ls-files` gives 212 documents, as the page says; 166 current, 25 stale, 21 obsolete; 0 re-verify rows. `cited_at` is `1f29f189`.
- One merge base, `1f29f189`. The diff to dev touches only the lane's 10 files.
- `receipts/gates_head_summary.tsv`: 94 static commands from the docs, `rtl-fast` and `elaborate` workflows, run in a disposable copy. 84 rc 0.
- `receipts/gates_head_renderer.txt`: the four renderer-dependent commands (the three `gen_toc.py` forms and `check_em_dash.py --base 1f29f189`), plus `docs_check.py` and `check_doc_paths.py`, rc 0 with the pinned renderer.
- Not this delta: `gen_hdl_reference.py --selftest` (pinned parser absent here), `ci_litex_env.py` (dependency absent here), and three selftests stopped at my 500 s limit (`ooc_tcl_selftest.py`, two `ctrl_boundary.py`). None reads the changed files' content. Their rc values are environment or time limits, not passes.
- **The one failure with a cause in this head is `pp_srcs.py`, F1.**

## Author packet

Evidence commit `03ffa10d` is unsigned (`verification.reason` = `unsigned`), so no signature could be verified; the brief's "signed packet" is not what was published. Five spot-checked files match the public manifest's `published_sha256` (`receipts/author_packet_spot_hashes.txt`). Two of those five are `citations-round3.txt` and `moved-citations.txt`; they were hash-matched, not read, and the citations were re-derived independently instead. The author's two mutant receipts were read and do not conflict with mine. The author's probe receipts were not read. `ci_tool_inventory.py --check` exits 2 at both head and dev in my environment, but on an absent tool, so the author's digest explanation is neither confirmed nor contradicted here.

## Completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #797 acceptance and D0 round-3 assignment; `CONTRIBUTING.md:56-57,514-515`; AGENTS section 7; D0-001, 017, 027, 035, 063-066 against their source lines; hosted run 41349428937 | R741-3 | `808602e08daee5e86ae21026bbaf2f9114db077a` |
| RTL | CLEAN | No RTL in `git diff 1f29f189..808602e0`; `protocol_processor_top.sv:3593-3595,3621-3622,3624-3648` at `a9e84b66`; `milan_datapath.sv:6048-6053,6194-6217,6392-6456`; the source-list gate protects build inputs, and no build input changed | R741-3 | `808602e08daee5e86ae21026bbaf2f9114db077a` |
| Robustness | CLEAN (S1, S2 optional) | `docs_inventory.py:137-138,355,373-420`; 213 planted forms, 15 gate plants, bad-data plants (`receipts/plant_probes.txt`) | R741-3 | `808602e08daee5e86ae21026bbaf2f9114db077a` |
| Tests | UNCLEAN (F1) | `receipts/gates_head_summary.tsv`, `receipts/pp_srcs_check_head.txt`, `receipts/mutants3.txt` (22 of 27 killed, S3), author mutant receipt | R741-3 | `808602e08daee5e86ae21026bbaf2f9114db077a` |
| Docs | UNCLEAN (F1) | `docs/DOCUMENTATION_AUDIT.md` regenerated and fresh; `scripts/docs_inventory.json` delta; PR body status and validation list; R1, R2, R3 are residue | R741-3 | `808602e08daee5e86ae21026bbaf2f9114db077a` |

## Real limits

- Physical calibration NOT RUN; no hardware, Vivado, Docker, replica, builder bank or source bank. Field skips are not hardware proof.
- The 500 s stops and two absent dependencies above are unexercised here. The hosted runs were cancelled before most jobs ran, so they provide no evidence for them either.
- Sampling covers this round's delta. Round 2's read-only statements and dev's new lines on release-facing pages stay unchecked, as the PR says; the brief did not extend coverage.
- `S1` was probed on planted text in one disposable tree, not on every possible markup form.
- PR comments added after this review started were not read.

## Pending manager duties

- Maintainer decision on what "Mark II default" names; one answer settles all 13 pages.
- The decision on the owner additions of 2026-10-30, which the author left unapplied.
- After the F1 fix: a new exact-head re-review of the changed data, hosted and local-replica acceptance, the merge-turn candidate banks, the external review, and post-merge containment. `ci/image/command-table.json` may need its digest updated if the fix edits a pinned script.
- Residue R1, R2 and R3 go to the checklist.

Exact bytes verified after probes: `HEAD` `808602e0`, tree `999f44a4`, no tracked or ignored change, index hash equals the tree listing hash, gitlinks `a9e84b66`, `135afd04`, `70936b77`, `48ff7a7e` unchanged and each submodule clean.

R741-3 FINISHED
