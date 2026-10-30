[R739] NEGATIVE - exact head 806957b35c3c23a36505744d205f9692720d19e2

# Independent delta review R739-2: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `806957b35c3c23a36505744d205f9692720d19e2`, tree `a3920c96afb9a4917515d337514de26ced4857b3`. Base main `135afd04`. Previously reviewed head `86073476`.
- Delta `86073476..806957b`: 8 Markdown files plus `scripts/check_docs.py` and `scripts/check_source_evidence.py`. No mode change, no gitlink, no RTL, generator, generated, test or Makefile path (`receipts/delta_scope_r2.txt`).
- Scope: the delta, and each named prior finding at its cause. Code the delta does not touch keeps its round-1 lens verdict.

## Order of work

- The isolation rule was followed. PR data came only from `gh pr view` with the permitted fields. The issue body, the issue-thread round-2 note and the ready notice were read. This reviewer's own round-1 report was read.
- No other reviewer's round-1 or round-2 report or packet was read. That includes the published `reviews/` directory of the evidence packet.
- Prior findings were resolved below against the source after the independent pass over the diff.

## Verdict basis

All five prior findings are resolved at their cause. The gate also passes at the head, and every planted defect the brief names fails it.

Two new MINOR findings remain. Both concern the gate this delta adds or reworks: what it claims covers more than it checks.
- **F1:** the duplicate constants-row rule has no self-test arm. A checker with that rule removed still passes all 41 arms. The PR body states every rule has a planted defect.
- **F2:** the copy rule misses decimal-converted and spelled-unit restatements. A Current page and the PR body both say those are rejected.

Either a small checker extension or narrowing the claims closes each one. Open MINORs make the verdict NEGATIVE.

## Resolution of named prior findings

| Prior finding | Resolution at this head | Evidence |
|---|---|---|
| R740-1 F4 = R739-1 F1, Follow_Up clause | **Resolved.** `docs/GLOSSARY.md:19` now reads "Two-step timestamp message: Follow_Up or Pdelay_Resp_Follow_Up \| 11.4.4, 11.4.7". This matches IEEE 802.1AS-2011 numbering (11.4.4 Follow_Up, 11.4.7 Pdelay_Resp_Follow_Up), the parser, generator and engine-suite citations, and the independent decoder descriptions. No Current page cites 11.4.3 any longer. Only history pages carry other 11.4.x citations, and those are correct. | grep at head; round-1 citation map |
| R740-1 F1 = R739-1 F3, publication timing | **Resolved.** The summaries at `docs/INTEGRATION.md:12-16`, `README.md:60`, `docs/HDL_DEVELOPER.md:12` and `:319-323`, and `docs/MANAGER.md:20,34` no longer claim atomic outputs. `docs/INTEGRATION.md:557-567` now matches the RTL: `hdl/top/KL_gptp_engine.sv:1134-1146` assigns `pub_*_o` straight from the staging registers, and `pub_commit_o = ucpu_commit_w \|\| boot_pub_commit_r`. `KL_gptp_ucpu.sv:442` makes `eff_commit_o` the execute-cycle OP_COMMIT, by which point earlier staging writes have landed. Wording residue in RES-1 and RES-2. My round-1 RES-1 and RES-2 are applied (`docs/INTEGRATION.md:12-15`). | RTL read at head |
| R739-1 F2, archive pointer | **Resolved.** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32` links the tree URL `.../tree/4999d8d6.../review-evidence/gptp75-r1/author`, the same target the base MANAGER page linked. The visible text is label-free: "measurement reports". That directory at `4999d8d6` holds the eight `.rpt` reports: baseline and candidate engine timing, util and util_hier, and ucpu util. | `receipts/parent_4999d8d6_reports.txt` |
| R740-1 F2 = R739-1 F4, stale constants escape | **Resolved.** Rows are found by name (`scripts/check_docs.py:113`). A non-plain-decimal cell is a named finding (`:421-424`). The 17 expected names are required (`:115-120`, `:430-434`). Planted bold, negative, unit-bearing, hex and badly grouped stale cells fail, and so do a deleted row, an unnamed row, stale `DEPTH` and a changed generator constant. The unmutated tree passes. | `receipts/plant_probes_r2.txt` |
| R740-1 F3 = R739-1 F5, duplicated values | **Resolved.** Every copy named in round 1 is replaced by a link to its constants row. That includes the servo threshold table, now `docs/INTEGRATION.md:366-369`, which names constants only. An audit grep of the 14 Current pages for every constants-table value, outside the Protocol constants section, finds only the gated ROM budget table (`docs/MANAGER.md:61-62`). Remaining numbers are dated measurements, the clock period and test stimuli. A new copy gate backs the rule (limits in F2). | `receipts/value_copies_r2.txt`, `receipts/value_words_r2.txt` |

Round-1 RES-3 is applied (`docs/MANAGER.md:45-49`). Round-1 S-3 is applied: `load_generator` sets `sys.dont_write_bytecode`, and no `__pycache__` appears after `make docs`. Round-1 S-2 (also checking the `--sync-seq-seed` image) is not taken and stays a suggestion (S-4).

## Findings

### F1 - MINOR - Tests

- **Where:**
  - `scripts/check_docs.py:415` (`duplicate constant row` finding);
  - the self-test constants arms at `:676-712`;
  - the claim at `docs/INTEGRATION.md:856`, "It also fails on a missing, duplicate or formatted row.";
  - the PR body, "Every rule has a true control that passes and planted defects that fail it."
- **Evidence:**
  - The duplicate-constant check is replaced with `pass` in a disposable copy, and `--selftest` still passes 41 arms (`receipts/checker_mutants.txt`, `no_const_duplicate`).
  - The equivalent ROM weakening is killed (`no_rom_duplicate`), and so are six other weakenings.
  - The production rule works: a duplicated `SYNC_RTO_MS_C` row in the real tree fails with "duplicate constant row" (`dup_const_row_real_tree`).
  - The rule dates from `59d562d`. This delta rewrote the constants arms "to isolate the rule each names" and added the ROM duplicate arm, but no constants duplicate arm.
- **Impact:** a later edit can silently drop a rule that a Current page advertises, and the self-test will not notice. The PR's coverage statement is not true for this rule.
- **Required outcome:** add a self-test arm that duplicates one row of the true constants table and expects a finding containing "duplicate constant row".
- **Verification:** rerun `scripts/checker_mutants.sh <clone> <scratch>`. `no_const_duplicate` must give selftest rc 1, every other mutant still rc 1, and the control rc 0.

### F2 - MINOR - Robustness, Tests, Docs

- **Where:**
  - `scripts/check_docs.py:439-456` (`value_spellings`);
  - the claim at `docs/INTEGRATION.md:860`, "`make docs` rejects a timed value restated with its unit.";
  - the PR body, "Unit-converted and spelled forms count".
- **Evidence:** in disposable copies of the head, each of these lines appended to `docs/HDL_DEVELOPER.md` passes the gate with rc 0:
  - "A 0.375 s watch." (`SYNC_RTO_MS_C` converted to a decimal larger unit);
  - "A 375 milliseconds watch." (unit spelled out).

  See `receipts/plant_probes_r2.txt`, `limit_decimal_seconds` and `limit_spelled_unit`. Only integer conversions (ms to s, ns to us) and whole-minute words are generated. The integer forms, minute words and µs variants all fail correctly (8 copy probes, on README, GLOSSARY, MANAGER, TEST, INTEGRATION and a `tb` README).
- **Impact:** a Current page states a guarantee the gate does not give. Ordinary prose restatements ("0.1 ms", "20 microseconds", "375 milliseconds") would pass. This is the same class as round-1 F4: a stated guarantee does not hold.
- **Required outcome:** either
  - (a) extend `value_spellings` to decimal larger-unit forms (for example 0.375 s, 0.1 ms) and unit words (nanoseconds, microseconds, milliseconds, seconds, minutes), with planted arms for each; or
  - (b) narrow `docs/INTEGRATION.md:860` and the PR body to what is checked, for example "`make docs` rejects a timed or rate constant restated as an integer with its unit symbol, or as whole minutes."
- **Verification:** with (a), both `limit_*` probes above give rc 1 and the controls stay rc 0. With (b), the sentence matches `value_spellings`.

### RESIDUE (wording only; does not change the verdict)

- **RES-1:** `docs/INTEGRATION.md:567`. "Only the commit cycle presents one complete tuple." After a commit the outputs keep that tuple until the next staging write, so "only" overstates. The stated contract, sample on `pub_commit_o`, is right and unchanged. Exact fix: "The commit cycle is the one cycle guaranteed to present a complete tuple."
- **RES-2:** `docs/HDL_DEVELOPER.md:12`. "staging moves outputs earlier" is unclear. Exact fix: "- Consumers sample publication on `pub_commit_o`; staging writes change the outputs before it."
- **RES-3:** the new source comments at `scripts/check_docs.py:111-112`, `:121-122` and `:394` state behaviour and reason but carry no issue ID, contrary to the owner comment rule. Exact fix: end each with "(#96)". They carry no lane, round, reviewer or comment-ID label.

### SUGGESTION (non-blocking)

- **S-1:** the copy gate matches by value, so a coincident unrelated figure is reported as a copy. For example, a Sync cadence of "125 ms" written on another page is reported as restating `FU_RTO_MS_C`, and a "100 ns" timing figure as `SLEW_SETTLED_NS_C`. The gate errs on the safe side. Consider naming the coincidence in the finding text.
- **S-2:** copy detection for a constant depends on its Meaning cell ending ", ms", ", ns" or ", ppm" (`scripts/check_docs.py:123`). Rewording `syncReceiptTimeout, ms` to `syncReceiptTimeout (ms)` silently disables the copy rule for that constant (`limit_meaning_unit_dropped`). Derive the unit from the name suffix (`_MS_C`, `_NS_C`, `_PPM_C`), or require a unit for an expected set.
- **S-3:** unitless constants are outside the copy gate: `LOST_CLEARS_AT_C` written as "fifth", `DEPTH` as "1,024 words", `ASCAP_UP_C` as "two good exchanges" (`limit_unitless_ordinal`, `limit_unitless_depth`). The pages comply today (audit grep). The issue rule is enforced for them by review only.
- **S-4 (round-1 S-2, carried):** the Seeded ROM row is checked only against `--seq-seed 0x200000` (`scripts/check_docs.py:556`). The engine suite also builds `--sync-seq-seed 0x10000`.
- **S-5:** the top-level `make lint` recipe calls `verilator` from `PATH`, with no override variable (`Makefile:20`). On this host that resolves to 5.052 unless the pinned build is put first. Gate rc is 0 either way. A `VERILATOR ?=` variable would make the pinned identity explicit.

## Check results

### Gates at the head (`receipts/head_gates.txt`, `receipts/head_*.log`)

- `make docs` rc 0: 14 Current, 18 historical; selftest 41 arms; source evidence 20 exact, selftest 7 arms.
- `make diagrams-check` rc 0, `make contract` rc 0, `git diff --check 135afd04 HEAD` rc 0.
- `make lint` rc 0 with the pinned Verilator 5.050 first on `PATH` (identity: `receipts/verilator_identity.txt`; the log shows only 5.050). A first run used the host's 5.052 and is superseded.

### Planted defects in copies of the real tree (`scripts/plant_probes_r2.sh`; `receipts/plant_probes_r2.txt`, `_full.log`)

- The control passes.
- 24 planted defects fail with rc 1 and the matching named finding:
  - **Stale constants (10):** plain, bold, negative, unit-bearing, hex and badly grouped stale cells, a deleted row, an unnamed row, stale `DEPTH`, and a changed generator constant.
  - **Broken ROM rows (6):** stale count, bold count, word-form free count, slash form, deleted row and duplicate row.
  - **Restated unit-bearing values on Current pages (8):** "375 ms" on HDL, "20 us" on TEST, "200 ppm" on GLOSSARY, "five-minute" on MANAGER, "300 s" on README, "100µs" in `tb/tsngen/README.md`, "20,000 ns" on INTEGRATION, and the reverted round-1 HDL line.
- 5 coverage-limit probes pass. They are F2 (2) and S-2/S-3 (3).

### Checker weakenings (`scripts/checker_mutants.sh`; `receipts/checker_mutants.txt`)

- Seven of eight weakenings make `--selftest` fail with the expected arm: required set, decimal parsing, us conversion, minute words, home exemption, ROM duplicate, and lookbehind.
- The constants-duplicate weakening survives (F1).

### Published author evidence (milan-fpga `84d4dd7f`, `review-evidence/gptp96-r1/author-r2`)

- All seven files match `MANIFEST.json` `published_sha256` (`receipts/evidence_manifest_check.txt`).
- The manifest is a hash list. The evidence commit reports `unsigned` (`receipts/evidence_commit_verification.txt`), so integrity rests on hashes, not a signature.
- The author's plant log (15 defects, 7 mutants, 0 failures) agrees with the independent probes here. Their mutant set does not include a constants-duplicate weakening.
- The author's suite and parent-gate results are handoff statements, without logs in the packet. The delta does not touch their inputs.

### Delta prose against source

New statements checked:
- `STEP_LOCKED_NS_C / RATE_PPM_C` ms: 100,000 ns / 200 ppm = 500 ms = 0.5 s; units ns/ppm = ms. Holds.
- `--p1` default equals `P1_C`: by value, literal 248 (author's code note).
- `ROM_CID_HI_C`/`ROM_GMCAP_BIT_C` naming of word 1022 bit 32.
- "Drives Sync every 250 ms, Follow_Up 60 ms after": `tb/verilator/engine/sim_main.cpp:202`.
- The lost-response and cease wording against `LOST_CLEARS_AT_C` and `CEASE_MS_C`.
- The `check_source_evidence.py` key rename, consistent with `docs/SOURCE_EVIDENCE.md:26`.

All hold.

### Privacy and labels

The delta's added lines carry no lane, round, reviewer or comment-ID label, no host or device name, and no private path (`receipts/delta_scope_r2.txt`). The one round-labelled path is inside the restored archive URL, which is the target round 1 required; its visible text is label-free.

### Clone integrity (`receipts/clone_integrity.txt`)

- HEAD, index tree and worktree match `806957b` / `a3920c96`, and `git status --ignored` is empty.
- `ls-files -s` equals `ls-tree -r HEAD` (blobs and modes).
- The tree has no gitlinks, and none are required.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | GLOSSARY Follow_Up row and 11.4.x citations across pages; constants-table references; delta clause text; round-1 citation map | R739-2 (delta), R739-1 (rest) | 806957b35c3c23a36505744d205f9692720d19e2 |
| RTL | CLEAN | delta scope (no `hdl/` change); publication staging, output assigns and commit pulse (`KL_gptp_engine.sv:864-935,1134-1146`, `KL_gptp_ucpu.sv:442`) against new prose; lint with pinned 5.050 | R739-2 | 806957b35c3c23a36505744d205f9692720d19e2 |
| Robustness | UNCLEAN (F2) | `check_docs.py` new row, decimal, required-set, copy and ROM parsing; 29 real-tree probes; bytecode side effect; clone cleanliness | R739-2 | 806957b35c3c23a36505744d205f9692720d19e2 |
| Tests | UNCLEAN (F1, F2) | selftest 41 arms; 8 checker weakenings; author plant log and manifest; delta leaves suite inputs untouched (round-1 suite runs stand) | R739-2 (delta), R739-1 (suites) | 806957b35c3c23a36505744d205f9692720d19e2 |
| Docs | UNCLEAN (F2) | all 8 changed Markdown files; constants section; value-copy audit of 14 Current pages; archive link target; summaries; RES-1..RES-3 | R739-2 | 806957b35c3c23a36505744d205f9692720d19e2 |

## Real limits

- The IEEE 802.1AS-2011 (Cor1/Cor2) and Milan v1.2 texts were not available here. The Follow_Up clauses were checked against the repository's citations, the independent decoder's 2011 descriptions and the round-1 numbering map.
- Test suites (ucpu, parser, engine, gaskets, tsngen, bench) were not rerun. The delta changes none of their inputs; round-1 runs and the author's handoff stand. The engine mutation arm and `make ooc` were not run by anyone at this head.
- Parent consumer gates were not run (that would be a parent bank). The author reports that the parent's gPTP-docs and submodule-docs gates fail identically at the previous head and this one until the parent pins are re-pinned.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus the focused runs here.
- The published evidence is hash-listed but unsigned.
- Physical calibration was NOT RUN. Simulation and field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `135afd04`, live dev `1e80128f`) with the builder and native banks at the merge turn, and link the receipts.
- At the parent bump, re-pin the parent gPTP-docs and submodule-docs pages.
- Carry RES-1..RES-3 to the residue checklist.
- Hosted/act acceptance.

R739-2 FINISHED
