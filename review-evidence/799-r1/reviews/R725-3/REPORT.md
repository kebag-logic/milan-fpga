[R725] POSITIVE - exact head 4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020

Round R725-3 is the internal independent review of PR #802 (issues #799 and #790). It is a delta review of `f87da064..4f3ebffb`: one commit that answers R725-2 F2 and S2. The source base is `97aab1d0` and the head tree is `7d3a5c3aaa86349a2b48d2473f601a9d9f7f2c55`.

The verdict is POSITIVE:

- F2, the only open prior MINOR, is resolved at its cause.
- The delta adds no MINOR, MAJOR or BLOCKER.
- One new RESIDUE (R3) is recorded with its exact fix. The S2 reflow left a single 105-column comment line. It is comment layout only, so it does not affect the verdict.

## Verdict summary

| ID | Origin | Severity, lenses | Status at 4f3ebffb |
|---|---|---|---|
| F2 | R725-2 | MINOR, Docs | **Resolved.** The sentence ends at "16 are the answer face." No text-census comparison remains. |
| S2 | R725-2 | SUGGESTION, Docs | **Applied in part.** "decision 2 (a)" is now joined, but the rewrap was not finished. The leftover is reported as R3. |
| R3 | new | RESIDUE, Docs | **Open, carried to the residue checklist.** `sw/mailbox/mailbox.yaml:65` is 105 columns wide. |
| F1 | R725-1, R726-1 | MINOR, Docs | **Still resolved.** The page figures equal the census at this head (see the checks below). |
| R1 | R725-1, R726-1 | RESIDUE, Docs | **Still resolved.** `6460917634` appears in no source comment. |
| R2 | R725-1, R726-1 | RESIDUE, Docs | **Still resolved.** The PR body says `Closes #790` and `closingIssuesReferences` is `[790]`. |
| S1 | R725-1, R726-1 | SUGGESTION, Tests | **Retained, optional.** `sim_sid_move.cpp` and the `Makefile` are not in the delta. |

## What the delta is

`git diff --name-status f87da064..4f3ebffb` lists two files (`receipts/delta.diff`, `receipts/restore_check.txt`):

- `docs/design/MAILBOX_SPLIT.md:993`: `face: the same reads and kinds the text census counted before.` becomes `face.`. This is R725-2 F2's first prescribed outcome, word for word.
- `sw/mailbox/mailbox.yaml:63-65`: a three-line rewrap of the "Minor 3" comment, from 4 lines to 3. Only line breaks and `#` markers change. `git diff --word-diff` shows no word added or removed.

Nothing else changed:

- The commit has one parent, `f87da064`.
- No gitlink is in the delta (`0` gitlink entries in `git diff --raw`).
- No HDL, test, script, generator or generated output is in the delta.

## Checks run at this head

**Tools.** The census used the rtl-fast pins:

- sv2v v0.0.12, binary sha256 `b29952bc...`. It was extracted from a zip whose sha256 `ff8c9eea5bc029b3...` equals the pin in `.github/workflows/rtl-fast.yml`.
- Yosys 0.66, which equals `YOSYS_VERSION`. The census's own `pins` rule accepted both.

`scripts/delta_checks.sh` reproduces every run below.

| Check | Command | Result | Receipt |
|---|---|---|---|
| census check | `publication_census.py --check --jobs 12` | rc 0. `6 shape(s), checks: 246 failures: 0`; `26 class-D net(s) ..., 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESULT: PASS` | `receipts/census_check.log`, `.rc` |
| census list | `publication_census.py --list --jobs 12` | rc 0. 26 population lines (4 `(unread)`) and 41 read rows. All six shapes have 41 reads and 4 unread nets. | `receipts/census_list.log`, `.rc` |
| reads by kind | parse of the list's last column | `field 11`, `status 14`, `processor 16`, `total 41`. This equals `MAILBOX_SPLIT.md:991-993`: 11 on the wire, 14 CSR status, 16 the answer face. | `receipts/kind_counts.txt` |
| rule count on the page (`:996`) | AST count of `census_rules.RULES` | `rules 31`, which equals "31 in all" | `receipts/rule_count.txt` |
| generator | `gen_mailbox.py --check`; `--crosscheck` | both rc 0, `0 finding(s)`. The reflowed yaml comment reaches no tracked output. | `receipts/gen_mailbox_check.log` |
| doc style | `scripts/check_doc_style.py` | rc 0, OK (23 current documents) | `receipts/doc_style.*` |
| doc paths | `scripts/check_doc_paths.py` | rc 0, 1068 cited paths resolve | `receipts/doc_paths.*` |
| hygiene | `scripts/check_hygiene.py --check` | rc 0, PASS (1292 files) | `receipts/hygiene.*` |
| doc map | `docs/DOC_MAP.gen.py --check` | rc 0, OK | `receipts/doc_map.*` |
| TODO ownership | `scripts/check_todo_ownership.py` | rc 0, OK | `receipts/todo_owner.*` |
| em dash | `scripts/check_em_dash.py --base f87da064`, with the pinned Markdown renderer's Python | rc 0, `0 finding(s) over 1 added line(s)`, arms 339/339 | `receipts/em_dash.*` |
| text-census residue | `grep -n "text census" docs/design/MAILBOX_SPLIT.md` | no match. The page no longer mentions the retired text census anywhere. | (inline) |
| comment rule, delta | scan of the delta's added lines for lane labels, round or reviewer IDs and comment IDs | 0 hits. The added lines cite only issue IDs (`#799`, `#665`, `protocol-processor #202`). | `receipts/comment_rule_scan.txt` |
| contract comment width | `awk` for top-level `#` lines over 79 columns in `mailbox.yaml` | one line, `:65` at 105 columns. There were 0 at `f87da064`. | `receipts/yaml_long_comment_lines.txt` |

**Evidence packet spot-check** (`review-evidence/799-r1` at `0829b8ae`). Four files were fetched that R725-2 did not check. Each one's sha256 equals its `published_sha256` in `MANIFEST.json` (`receipts/evidence_spotcheck.txt`):

- `author-r1/a692b/receipts/mailbox-generator-ca39dc1b/check-crosscheck.log`
- `author-r1/a692b/HANDOFF.md`
- `author-r1/a692b/receipts/docs-ca39dc1b/all/receipts.json`
- `author/HANDOFF.md`

The packet commit `0829b8ae` has no GPG signature (`verification.reason: unsigned`). Its integrity rests on the manifest hashes. The packet holds receipts up to `ca39dc1b` and the sweep at `41a78877`. It holds none for `f87da064` or `4f3ebffb`, which are doc-and-comment commits. My runs above are the execution evidence for this delta.

**Hosted checks at the exact head**, a snapshot at review time (`receipts/hosted_checks_4f3ebffb.tsv`): 51 check runs.

- 24 completed with success, 1 was skipped, 20 were in progress and 6 were queued.
- These completed with success: `publication-census`, `docs-check`, `docs-check-no-git`, and `docs-gates-0`, `-1` and `-2`.

This is a snapshot only. Hosted and act acceptance belong to the manager. No manager source bank runs at this head, and none is claimed.

## Findings

### R3 - RESIDUE - Docs - `sw/mailbox/mailbox.yaml:65` - the S2 reflow left one comment line at 105 columns

- **Authority/evidence:**
  - Line 65 now reads `# which the AAF and CRF talkers stamp. After a MAAP conflict the protocol owner moves a source to another`, which is 105 columns.
  - Every other top-level comment line in the file is at most 79 columns. At `f87da064` none was over 79 (`receipts/yaml_long_comment_lines.txt`).
  - The commit rewrapped lines 63 and 64. It then merged the old line 65 into the next one without rewrapping the rest of the paragraph, which R725-2 S2 asked for.
- **Why RESIDUE:**
  - This is purely the layout of comment prose. No word changes (`git diff --word-diff`).
  - `gen_mailbox.py --check` and `--crosscheck` are clean, and no gate reads the line.
  - It changes no measurement, figure, verdict, test, code, generated artifact or clause claim, and it touches no privacy rule.
- **Impact:** cosmetic. The one over-long line breaks the file's comment wrap.
- **Exact fix:** replace lines 63-68 with the following seven lines. They contain the same words and are at most 78 columns (`receipts/yaml_reflow_proposal.txt`):

```text
# Minor 3 (#799; #665 decision 2 (a)): a source entry per talker stream in the
# publication block, carrying the stream_id the source currently declares,
# which the AAF and CRF talkers stamp. After a MAAP conflict the protocol
# owner moves a source to another Stream ID (protocol-processor #202), so the
# plane that owns the Stream ID publishes the ID it declares. It only adds:
# the entries sit in the hole below the sink entries, and a firmware built
# against 2.2 leaves them at 0.
```

- **Verification:**
  - `awk '/^#/ && length($0)>79' sw/mailbox/mailbox.yaml` prints nothing.
  - `git diff --word-diff` shows no word change.
  - `gen_mailbox.py --check` stays at 0 findings.

### Observation, not a finding

`sw/mailbox/mailbox.yaml:58` carries `comment 6092086337`. That text is unchanged context at base `97aab1d0`, so it is an existing instance tracked by #746 and is not counted here.

## Lens results (clean lenses in findings format)

```text
[R725] PASS Conformance - sw/mailbox/mailbox.yaml@4f3ebffb (delta :63-65), gen_mailbox.py --check/--crosscheck (receipts/gen_mailbox_check.log) - the delta changes only comment line breaks; no field, offset, version or doc string moved, and the generated SV/C/pages still equal the contract; the census rows' fields (BINDING.*, SID_LO.SID, SRC_SID_LO.SID, DA_GATE.OPEN, LICENCE.ACTIVE, SR_DOMAIN.*, TALKER_DECL.DECLARED) map to contract registers at this head (receipts/census_list.log); unchanged scope keeps the R725-1 / R726-1 / R725-2 Conformance verdicts because the delta touches nothing they depend on
[R725] PASS RTL - receipts/delta.diff and receipts/restore_check.txt (no HDL, no gitlink in the delta; all six gitlinks equal), receipts/census_check.log - the head datapath elaborates in all six shapes under the pinned sv2v/Yosys with 0 of 246 checks failing; prior RTL verdicts at ca39dc1b/f87da064 hold, as no RTL input changed
[R725] PASS Robustness - receipts/census_list.log, receipts/census_check.log - the six-shape agreement (same 26 population, same 4 unread, same 41 reads and cone-end classes) holds at this head; the delta changes no behaviour, configuration or error path; prior Robustness verdicts hold
[R725] PASS Tests - receipts/rule_count.txt, receipts/kind_counts.txt, receipts/evidence_spotcheck.txt - no test, gate, plant or self-test source is in the delta; the page's census figures (31 rules, 26/41/4, 11/14/16) equal the code and the census output at this head; the docs gates pass at this head; S1 remains optional
[R725] PASS Docs - docs/design/MAILBOX_SPLIT.md:988-997@4f3ebffb against publication_census.py --check/--list; sw/mailbox/mailbox.yaml:63-68; PR body closing refs (receipts/prior_findings_check.txt); docs gates - F2 resolved at its cause, F1/R1/R2 still resolved, the delta adds no comment-rule instance; the only new defect, R3, is RESIDUE
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `mailbox.yaml` delta; `gen_mailbox.py --check` and `--crosscheck` (0 findings); census field rows; unchanged scope covered by the prior rounds | R725-3 (delta). R725-2, R725-1 and R726-1 cover the scope the delta leaves untouched. | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` (prior coverage at ancestors `f87da064` and `ca39dc1b`, untouched since) |
| RTL | CLEAN | delta file list (no HDL, gitlinks unchanged); six-shape census elaboration at head | R725-3; R725-2, R725-1 and R726-1 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` (prior at `ca39dc1b`, untouched since) |
| Robustness | CLEAN | six-shape census agreement at head; the delta changes no behaviour | R725-3; R725-2, R725-1 and R726-1 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` (prior at `ca39dc1b`, untouched since) |
| Tests | CLEAN | rule count; read-kind counts; evidence manifest spot-check; docs gates at head; S1 optional | R725-3; R725-2, R725-1 and R726-1 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` (prior at `ca39dc1b`, untouched since) |
| Docs | CLEAN | `MAILBOX_SPLIT.md:988-997` against the census; `mailbox.yaml:63-68`; PR body; docs gates; R3 is RESIDUE | R725-3 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |

## Real limits

- I ran no simulation, Verilator, Yosys portability, firmware, builder or Vivado bank at this head. The delta changes no input any of them reads.
- I did not run the census self-test at this head. The census sources and the plant table are unchanged since the author's hash-verified self-test log.
- The hosted checks at the exact head were still running when I took the snapshot. I make no hosted or act acceptance claim.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The final current-dev merge candidate (source base `97aab1d0`, live dev `5fcec84b1aa72c43048eff28bb63a982add830dd`) was not built or validated here.
- The evidence packet was spot-checked on 4 more of its 581 manifest entries, not verified in full. Its commit is unsigned, so its integrity rests on the manifest hashes.

## Pending manager duties

- Carry R3 to the residue checklist, with its exact fix.
- Build and validate the current-dev merge candidate (builder and native banks) and link the receipts on the PR.
- Own hosted and act acceptance at the final head. Several exact-head contexts were still in progress at the snapshot.
- Obtain the second independent positive review, which is the external one, at this head or at the final head.
- S1 is optional.

## Restoration

After all runs the clone is unchanged (`receipts/restore_check.txt`):

- `HEAD` is `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020`.
- `git write-tree` gives `7d3a5c3aaa86349a2b48d2473f601a9d9f7f2c55`, which equals the head tree.
- `git diff-index`, `git diff-files` and porcelain status are all empty.
- Both delta files' worktree hashes equal their head blobs, with mode 100644.
- All six gitlinks are unchanged: `external` efeb541a, `gptp-processor` 55680bff, `protocol-processor` f65c8ff7, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 70936b77, `third_party/verilog-axis` 48ff7a7e.

R725-3 FINISHED
