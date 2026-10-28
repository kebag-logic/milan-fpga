[R726] POSITIVE - exact head 4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020

External independent review, round R726-2, of kebag-logic/milan-fpga PR #802 (issues #799 and #790).
Exact head `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020`, tree `7d3a5c3aaa86349a2b48d2473f601a9d9f7f2c55`.
This is a delta round. The previously reviewed head is `ca39dc1b0bd917e3e033df9d9db762514318377a` (R726-1, NEGATIVE on one Docs MINOR). The source base is `97aab1d0`.

## Summary

- The delta `ca39dc1b..4f3ebffb` is two commits. They touch two files and nothing else (`receipts/delta_raw.txt`):
  - `docs/design/MAILBOX_SPLIT.md`: prose only, +5/-5.
  - `sw/mailbox/mailbox.yaml`: comment lines only, +3/-4.
- No gitlink, RTL, test, generated artifact or contract value changed. The submodule gitlinks are the same as at `ca39dc1b`: processor `f65c8ff7`, gPTP `55680bff`, verilog-axis `48ff7a7e`.
- The census figures on the design page now equal the census at this head:
  - 26 population nets, 41 reads, 4 unread nets.
  - The 41 reads split 11 field, 14 status and 16 processor.
- The page no longer claims that the retired text census counted these reads.
- The comment-ID residue in `mailbox.yaml` is gone, and the PR body says `Closes #790`.
- No BLOCKER, MAJOR or MINOR is open, so all five lenses are clean at this head. Open items:
  - two RESIDUE items: one comment line left unreflowed, and the PR body still naming `ca39dc1b` as the ready head;
  - two optional SUGGESTIONs.

## Evidence run at this head (reviewer-run, this clone)

| Check | Command | Result | Receipt |
|---|---|---|---|
| Delta scope | `git diff --raw ca39dc1b 4f3ebffb` | 2 files, both mode 100644, both M | `receipts/delta_raw.txt`, `receipts/delta_ca39dc1b_4f3ebffb.diff` |
| Publication census | `SV2V=<pinned sv2v v0.0.12> YOSYS=yosys python3 sw/mailbox/publication_census.py --check --jobs 6` | rc 0. `6 shape(s), checks: 246 failures: 0`. `26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESULT: PASS`. Every shape reports 41 reads and 4 unread nets. | `receipts/census_check.log`, `.rc` |
| Census row kinds | `Counter(r.kind for r in CENSUS.values())` | processor 16, status 14, field 11. 22 read nets. 25 wrapper class-D ports plus `aecp_strm_started_o` make 26 nets. | `receipts/census_kinds.txt` |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check` | rc 0, `gen_mailbox: 0 finding(s)` | `receipts/gen_mailbox_check.log`, `.rc` |
| Docs wording and privacy | `python3 scripts/docs_check.py` | rc 0, 0 findings across 210 md files and 1421 scrubbed text files | `receipts/docs_check.log` |
| Hygiene ratchet | `python3 scripts/check_hygiene.py --check` | rc 0, PASS | `receipts/check_hygiene_check.log` |
| Doc paths | `python3 scripts/check_doc_paths.py` | rc 0, 1068 cited paths resolve | `receipts/check_doc_paths.log` |
| Prior-finding probes | `git grep 6460917634`; 10-digit IDs and lane or round labels added in the delta; `text census` mentions; `mailbox.yaml` comment lines over 80 characters | No ID or label was added in the delta. One long comment line remains (RES-1). | `receipts/prior_findings_probe.txt` |
| PR metadata (read-only) | `gh pr view 802 --json ...` | head `4f3ebffb`, base `dev`, not draft. `closingIssuesReferences` = [790]. The body contains `Closes #790`. | `receipts/pr802.json` |
| Hosted check runs at exact head (read-only) | GitHub check-runs API | Finished: 45 success. Skipped: 1 (`Physical gPTP (nightly and manual)`). In progress when read: 10 (9 Verilator shards and `Fail fast across this head`). `rtl-fast`, `publication-census`, `yosys-elaboration`, the Yosys shards and the docs gates are success. | `receipts/hosted_check_runs_4f3ebffb.tsv` |
| Tool identity | pinned sv2v archive hash compared with the CI cache key | `ff8c9eea…5a00` equals the pin at `.github/workflows/rtl-fast.yml:391`. Yosys 0.66 (`86f2ddeb`), as in the CI Yosys key. | `receipts/tool_identity.txt` |
| Restore | `git rev-parse`, `git status --porcelain`, `ls-files -s` compared with `ls-tree -r HEAD`, submodule status | Clone at the exact head and tree with 0 porcelain lines. Index equals the HEAD tree (same digest). Gitlinks are as stated above. | `receipts/restore_verify.txt` |

`scripts/r726_2_probe.sh` reproduces the reviewer-run rows. Its arguments are a clone at this head, an output directory and the pinned sv2v.

The census needs the pinned sv2v. The first attempt used a newer sv2v from `PATH`. The tool refused it by name (`set SV2V and YOSYS to the pinned tools`) and exited 2 before elaborating anything. That run's log was overwritten by the pinned run. This behaviour is correct and is not a finding.

## Prior findings at this head

| Prior finding | Status at 4f3ebffb | Evidence |
|---|---|---|
| F1 MINOR Docs (R725-1, R726-1): census counts at `MAILBOX_SPLIT.md:990-992` and `:1102` described the base (25 / 39 / 10 / 14 / 15) | **Resolved** | `docs/design/MAILBOX_SPLIT.md:990-993` states 26 nets, 41 reads, 4 unread and 11 / 14 / 16. The `:1102` table row states "41 reads of the 26 class-D nets". Both equal `receipts/census_check.log` and `receipts/census_kinds.txt`. `git grep` finds no other copy of the figures in the tree. The unchanged "118 plants" (116 in `census_plants.PLANTS` plus the 2 table plants of `census_selftest.py`) and "31 rules" (`len(census_rules.RULES)` = 31) are still accurate. |
| F2 MINOR Docs (R725-2): the edited sentence still said the retired text census counted the same reads | **Resolved** | The sentence now ends at "16 are the answer face." (`MAILBOX_SPLIT.md:992-993`). The only remaining "text census" text in the tree is `sw/mailbox/census_plants.py:440`, which is a historical section label and makes no count claim. |
| R1 RESIDUE (R725-1, R726-1): issue-comment ID in the `mailbox.yaml:63` source comment | **Resolved** | `mailbox.yaml:63` reads `# Minor 3 (#799; #665 decision 2 (a)): ...`. "Minor 3" is contract minor version 3 (`version.minor: 3`), not a review label. No 10-digit ID and no lane or round label was added anywhere in the delta. The pre-existing `comment 6092086337` and "round-3 ruling" at `mailbox.yaml:58` are outside the delta and tracked by #746. |
| R2 RESIDUE (R725-1, R726-1): PR body said `Relates to #790` | **Resolved** | The PR body contains `Closes #790` and the title says "closes #790". `closingIssuesReferences` = [790]. #799 is deliberately not closed, and the body explains why (bench qualification re-runs). |
| S2 SUGGESTION (R725-2): reflow the short comment line left by the R1 fix | **Partly addressed; carried as RES-1** | The short line was absorbed, but the reflow joined it into one 105-character line (`mailbox.yaml:65`). |
| S1 SUGGESTION Tests (R725-1, R726-1): sidmove8 named uid equals the derived uid (`tb/verilator/milan_dp/sim_sid_move.cpp`, `Makefile`) | **Retained, optional** | The delta touches nothing under `tb/`. |

## Findings

### RES-1 - RESIDUE - Docs - `sw/mailbox/mailbox.yaml:65` - the comment reflow left one 105-character line

- **Authority/evidence:** The commit says it reflows the contract comment. The neighbouring comment lines (`:56-68`) are 73-78 characters, but `:65` is 105 (`receipts/prior_findings_probe.txt`). No gate measures this: the hygiene ratchet rejects a line-length check by design, and `gen_mailbox.py --check` is clean, so the generated artifacts do not carry this comment.
- **Impact:** Layout only. It changes no value, generated artifact or claim.
- **Required outcome (exact fix):** Rewrap `:63-68` to the block's width:
  ```
  # Minor 3 (#799; #665 decision 2 (a)): a source entry per talker stream in
  # the publication block, carrying the stream_id the source currently declares,
  # which the AAF and CRF talkers stamp. After a MAAP conflict the protocol
  # owner moves a source to another Stream ID (protocol-processor #202), so the
  # plane that owns the Stream ID publishes the ID it declares. It only adds: the
  # entries sit in the hole below the sink entries, and a firmware built against
  # 2.2 leaves them at 0.
  ```
- **Verification:** `awk 'length>80 && /^#/' sw/mailbox/mailbox.yaml` prints nothing, and `gen_mailbox.py --check` is still 0 findings.

### RES-2 - RESIDUE - Docs - PR #802 body, "Status" and the reproduction "expected state" - the body still names `ca39dc1b` as the ready head

- **Authority/evidence:** The body says "GREEN, ready for review at `ca39dc1b…`" and "The expected state: … head `ca39dc1b…`". The published head is `4f3ebffb`. The gate receipts it cites were genuinely taken at `ca39dc1b`, and `4f3ebffb` differs from it only in the two prose and comment hunks above (`receipts/delta_raw.txt`). So no measurement claim is wrong; only the head the reader is told to reproduce is stale.
- **Impact:** A cold reader following the reproduction block checks out `ca39dc1b` and reproduces a head carrying F1 and F2.
- **Required outcome (exact fix):** Name `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` as the ready head and as the expected state. Add one line: "Gate receipts were taken at `ca39dc1b`; `ca39dc1b..4f3ebffb` changes only `docs/design/MAILBOX_SPLIT.md` prose and a `sw/mailbox/mailbox.yaml` comment (census and generator re-checked rc 0 at `4f3ebffb`)."
- **Verification:** `gh pr view 802 --json body` names `4f3ebffb` as the head.

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_sid_move.cpp:863-868`, `tb/verilator/milan_dp/Makefile` (sidmove8 build)

Retained from R725-1 and R726-1, still optional, untouched by the delta. If the eight-stream leg's named uid differed from the derived uid, the leg could tell the two sources of the Stream ID apart.

### S3 - SUGGESTION - Docs - `docs/design/MAILBOX_SPLIT.md:817`

`(#799, the ruling on its STOP, comment 6460917634)` is a comment ID on a design page. Docs pages are outside the source-comment rule, and this line is not in the delta, so this is optional. A link in the style of `AREA_BUDGET.md:144` (`[owner decision of 2026-10-28](…#issuecomment-6460917634)`) reads better than a bare ID.

## Lenses applied this round

- **Conformance - CLEAN.**
  - The only contract-file change is comments at `sw/mailbox/mailbox.yaml:63-68`. `version` is still 2.3 and no field moved. `gen_mailbox.py --check` reports 0 findings.
  - The census contract holds at the head: 41 rows, 41 reads, every shape the same, 246 checks with 0 failures.
  - The PR closes #790 and leaves #799 open, as the body explains.
- **RTL - CLEAN.**
  - `receipts/delta_raw.txt` shows no `hdl/` or submodule change since `ca39dc1b`.
  - The census elaborated `hdl/milan/milan_datapath.sv` at this head in all six shapes: recipe 112979 cells up to ax7101_8x8 544991 cells, with the same population and reads.
  - The R726-1 RTL verdict at `ca39dc1b` therefore holds, because nothing it depends on changed.
- **Robustness - CLEAN.** The delta changes no behaviour. The cross-shape census agreement holds from one to eight streams, with and without the loopback lane (`receipts/census_check.log`). The R726-1 Robustness verdict at `ca39dc1b` holds, because nothing in its scope changed.
- **Tests - CLEAN.**
  - The delta changes no test.
  - The census `--check` (246 checks) and the generator `--check` pass at this head.
  - The hosted `publication-census` and `rtl-fast` runs are success at this head.
  - S1 is optional.
- **Docs - CLEAN.**
  - F1 and F2 are resolved. Every census figure on the page equals the tool output, and the "118 plants" and "31 rules" figures are rechecked.
  - R1 and R2 are resolved.
  - `docs_check`, the hygiene ratchet and `check_doc_paths` are rc 0.
  - RES-1 and RES-2 are wording residue and leave the lens clean.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sw/mailbox/mailbox.yaml:56-70` (diff and version), `gen_mailbox.py --check`, `publication_census.py --check` (6 shapes), `CENSUS` kinds, PR #802 closing references | R726-2 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |
| RTL | CLEAN | `receipts/delta_raw.txt` (no `hdl/` or gitlink change); census elaboration of `hdl/milan/milan_datapath.sv` in 6 shapes; prior coverage R726-1 at ancestor `ca39dc1b` with nothing in scope touched since | R726-2 (R726-1 at `ca39dc1b` remains valid) | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |
| Robustness | CLEAN | delta scope; census cross-shape agreement, 1-8 streams, with and without loopback; prior R726-1 coverage at `ca39dc1b`, nothing in scope touched since | R726-2 (R726-1 at `ca39dc1b` remains valid) | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |
| Tests | CLEAN | census `--check` (246 checks, 0 failures), generator `--check`, hosted `publication-census` and `rtl-fast` success; `tb/` untouched; S1 optional | R726-2 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |
| Docs | CLEAN | `docs/design/MAILBOX_SPLIT.md:975-1000`, `:1102`; `sw/mailbox/mailbox.yaml:63-68`; PR #802 body; `docs_check`, hygiene and doc-path gates; RES-1 and RES-2 residue | R726-2 | `4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020` |

## Real limits

- This was a delta round. Code the delta does not touch keeps the R726-1 verdicts at `ca39dc1b`. I did not re-run the mbx suite, the milan_dp suites, gsi-mutants, the firmware set, Yosys, Vivado, lint or the census `--selftest` at this head. Source-head execution evidence for those is the author's published receipts at `ca39dc1b`, whose RTL, tests and tools are byte-identical to this head.
- I did not separately re-verify the signed evidence packet at `0829b8ae…/review-evidence/799-r1`. I only listed its manifest: 581 entries, receipts at earlier heads `3ee2d969` and `a692b`. This round's claims rest on my own runs at the head.
- The census ran on the host's Yosys 0.66 (`86f2ddeb`, distribution build) and the CI-pinned sv2v v0.0.12 archive. This is the same version and hash as CI's key, but it is not CI's own build of Yosys.
- When I read the hosted runs, 10 contexts were still in progress (9 Verilator shards and `Fail fast across this head`). `Physical gPTP (nightly and manual)` was skipped, which is not execution. I make no claim about any unfinished context.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at this exact head, including the in-progress `verilator-suites` shards and `Fail fast across this head`.
- The current-dev merge candidate: source base `97aab1d0`, live dev `5fcec84b1aa72c43048eff28bb63a982add830dd`. This means builder and native banks, the candidate-merge validation and the post-merge containment, with receipts linked on the PR.
- Carry RES-1 and RES-2 to the residue checklist.
- Merge only with explicit maintainer authorization. #799 stays open for the bench qualification re-runs.

R726-2 FINISHED
