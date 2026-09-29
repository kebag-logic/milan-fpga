[A444] REVIEW READY
Commit: `d76763733e088cd21bbdd587927c8cf2f26cc8b3` on `b2-bench-0929`, one commit on the round-1 head `c37f1d04e39be0344dfde77e793cdfa441bd4869`, local and not pushed. Tree `2e2dcd08dd16575aee614c8ff694a2c6c964b95c`. Docs only, no bench access, under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5886531640).

Changed: three Markdown pages, modes 100644, and no gitlink:
- `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`:
  - `:17` and `:23` (verdict rows) and `:27-45` (the reading as decided) answer F1.
  - `:209-229` (Cycle 22, "Why the registrar was LV") answers F3.
  - `:414-434` (saved-state layer) answers F2.
  - `:140` (2.742 s) takes R405-1 S1.
- `docs/findings/606_FIRST_BIND_MEASUREMENT.md`:
  - `:19` and `:198-199` (MSRP spacing) take the S2 suggestions.
  - `:239` and `:243-283` (saved-state layer with its derivation and cause) answer F2.
- `docs/findings/README.md:11-13`: index rows for both pages, and the #75 row corrected (R404-1 S1, R405-1 S3).

F1, the #608 reading as decided ([ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887), [correction](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5886425487)):
- 99 of 99 withdrawals that reached an IN registrar stopped within one PDU.
- Cycle 22 is attributed to the processor #108 deviation.
- #608 item 3 is met without qualification only after the pin adoption of processor PR #133 and a re-run. Processor #134 still grades the LV stop.
- The #75 row reads "Met under the ruling: 100 cycles, 99 of 99 demonstrated restarts". The literal count stays as history.

F3, cycle 22's attribution:
- The bridge's LeaveAll to the DUT's own is 0.401121 s.
- Table 10-5 and clause 10.6 are cited, and the deviation text is `10_srp_engine.md` section 6.5 at `c951a9ff`.
- 67 DUT LeaveAlls, in 64 of the 112 captures, came less than 10 s after a received bridge LeaveAll (gaps 0.199564-4.807277 s).
- "Genuine LeaveAll cycle" is qualified.

F2, the saved-state layer. Both restore sections carry this table, derived from the archived console captures:

| Saved-state field | Identity gate, 06:49:58Z | Final restore, 07:20:45Z |
|---|---|---|
| NVM slots A / B, image sequence | 229 / 230, image 230 | 229 / 230, image 230 |
| Records, writer | 53 records, 3,264 B, writer live | same |
| Commits ok / failed | 2 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000c44`, 1 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc34000e4`, pend 1 | `0xc34000e4`, pend 1 |

The cause:
- `PP_STAT` read `0x5b000c44` in all 226 console samples: dirty, stale and alarm 0, pend and backed 1.
- The only state-changing commands were 105 `CONNECT_RX` and 105 `DISCONNECT_RX`, all to the peer's Stream Input 8. No AECP write was sent.
- The DUT's two stream inputs read connection count 0 in all 340 polls.
- Binding records `0x20`-`0x2F` are indexed by the DUT's stream inputs. So none of the binds, unbinds or cycles wrote a record, and no commit ran.
- `nvm_pend` 1 is lane B1's residue: PR #620's final column is identical.
- Between the two reads the samples carry `PP_STAT` only.
- The persisted records were not compared with the found state.

F4: resolved by the maintainer's redacted archive (`666d8897`).

Validation, all rc 0 at `d7676373`, foreground, not piped, from the physical `/data` worktree:
- In the pinned Markdown environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870` (902 added lines, 0 findings) and `check_doc_paths.py`.
- Also: `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`, and `git diff --check` over 13eda870..HEAD and c37f1d04..HEAD.
- Extra checks, also rc 0: 53 of 53 links and anchors resolve (R405-1's `check_links.py`), and `gen_toc.py --verify-anchors` passes.

Measurement tables: byte-identical, proved by diff.
- Every table except the two verdict tables is unchanged: 8 of 8 on the #606 page, 9 of 9 on the #608 page, and the PR body's per-bind table.
- The measurement-table diff is empty, and a literal `diff` of all table lines returns rc 0. The only removed table lines are three verdict rows.
- The new tables are the two saved-state tables.

Inputs: all 226 console files and 112 `msrp.tsv` read are git-blob-equal to archive `666d8897`, and every file read matches the archive's `original_sha256`.

Token scan: clean. R404-1's `token_scan.py` and R405-1's `scan_tokens.py` ran over every file of the round-2 packet except the scan's own receipt, and over the three pages, with 19 private patterns held outside the packet:
- R404-1's scan: no hit in any class, in the packet or the pages.
- R405-1's scan: 0 hits in its `ipv4`, `abs-path`, `hostname`, `iface` and `serial` classes and in all 19 private classes. Its only identifier hits are the DUT's own locally administered entity ID and one MAAP destination, both already on the #606 page in round 1.

Acceptance: F1, F2 and F3 are answered as ruled, F4 is disposed by the maintainer, and the listed suggestions are taken. The reviews decide.

Open risks/questions:
1. The correction says "67 of 112 captures". The 67 counts DUT LeaveAll PDUs, which fall in 64 captures (R405-1's 64). The page states both numbers. Please confirm or correct the wording.
2. Not pushed; the PR body is proposed in the packet's `PR-BODY.md`, and the PR is unedited. Hosted checks and act at this head are pending the push.
3. The round-2 packet (scripts, receipts, manifest) is in the author's output directory for the manager to archive. It holds no private identity.
4. Carried from round 1: #606's post-reset path needs a DUT reset, and when an LV registration expires is not measured.
