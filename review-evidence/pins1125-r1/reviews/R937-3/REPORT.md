[R937] POSITIVE - exact head d3cb3cf180f846a969f5baacf8b2bec34e4acd50

Round R937-3 is an internal, cleared-context, narrow re-review of kebag-logic/milan-fpga PR #1016 (Closes #1013).

- Exact head `d3cb3cf180f846a969f5baacf8b2bec34e4acd50`, tree `eb3ebcb7e1ad48818893afad260ff060937c6c96`. The PR's live head equals it.
- Source base `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.
- The delta is `e5d8a71b..d3cb3cf1`: one commit, a one-line message with no trailer. It changes 2 files (+5/-4):
  - a source comment in `tb/verilator/gptp_shadow/sim_main.cpp`;
  - one line in `CHANGELOG.md`.
- The PR body changed on two lines since the round-2 packet's `author/PR-BODY.md` (`receipts/pr-body-vs-r2-packet.diff`).

All five lenses were applied to the delta and to the PR body as it stands.

- The four named prior findings (R937-2 F1 and F2, R938-2 F1 and F2) are each resolved at their cause.
- The commit changes no behaviour. With whole-line comments removed, the C++ file is identical at both heads. No image input or gitlink moves.
- No BLOCKER, MAJOR or MINOR is open. One new SUGGESTION is recorded. One earlier RESIDUE is retained for the manager's checklist.

## Reconstruction

- **Contract:**
  - AGENTS.md sections 3 to 8.
  - CONTRIBUTING.md, which is authoritative where the two differ.
  - docs/README.md.
- **Task:**
  - The #1013 scope and acceptance, and its public pin ruling: gPTP `3ce71b768a2f6f6a5274c127080146e755d02275` and tsn-c-stack `a795471c0abc4e38f7e5146b4e539dd607b6f501`.
  - Both gitlinks are unchanged at this head (`receipts/delta_check.txt`).
- **Requirements:** the FPGA-gPTP #109 semantics carry unchanged from the earlier rounds, because the delta touches no product source:
  - 802.1AS-2011 11.2.2 b), Figure 11-8 and 11.2.13.2.1 f);
  - Milan v1.2 4.2.6.1.1 and 4.2.6.2.7.
  - These are stated at `tb/verilator/gptp_shadow/sim_main.cpp:2972-2980` and `tb/verilator/gptp_plane/sim_main.cpp:588-596`.
- **Order of reading:** I read the following before any prior finding:
  - the delta diff;
  - the phase-22 harness (`sim_main.cpp:2972-3080`) and `near()` (`:171-173`);
  - `gptp_plane` phase 6 (`tb/verilator/gptp_plane/sim_main.cpp:588-705`);
  - the change log's #109 block (`CHANGELOG.md:67-86`);
  - the live PR body.
  - Only then did I read the R937-2 and R938-2 findings, to resolve them.
- **Author packet:** `4b3b21e2104d37db96040622edfe75a5acbf2a76:review-evidence/pins1125-r2`, 14 files. It was produced at `e5d8a71b`.
  - Every downloaded blob's git id equals the tree's (`receipts/r2_packet_tree.txt`).
  - All 14 `MANIFEST.json` entries match their `published_sha256` (`receipts/claims.txt`).
  - Its executed receipts carry to `d3cb3cf1`, because the only C++ change is whole-line comments (`receipts/delta_check.txt`: comment-stripped digests EQUAL).
- **Hosted, at the exact head:** snapshot 2026-11-26T04:37Z (`receipts/hosted_summary.txt`).
  - Completed with success: `docs-check-no-git` and `wire-accountability`.
  - In progress: `docs-gates-0/1/2` and `Fail fast across this head`.
  - Queued: `elaborate-gates-0..4` and a second `Fail fast across this head`.
  - None of the in-progress or queued contexts is executed evidence. The manager owns hosted and act acceptance.

## Prior findings at this head

| Prior finding | Status at `d3cb3cf1` | Evidence |
|---|---|---|
| R937-2-F1 MINOR Tests, Docs: the PR's phase-22 row says the offset moves "only when" the floored delay is used, which claims more than a 64 ns band resolves | RESOLVED | The live row (`receipts/pr-body-live.md:94`) now reads "as it does when the plane uses that pair with the delay floored at -800 ns". This is the README's accurate wording (`tb/verilator/gptp_shadow/README.md:38`). It now states a sufficient condition, not a necessary one. That agrees with `near(after, before - kGradedOffsetNs, kOffsetNearNs)` at `sim_main.cpp:3053`. The resolution is also stated in the source comment at `:2987-2988` |
| R937-2-F2 MINOR Docs: `CHANGELOG.md:75` said "Nine planted defects" after two controls were added | RESOLVED | `CHANGELOG.md:75` reads "Eleven planted defects each fail a named check". In the #109 block that is `link_delay.py`'s eight plus `gptp_shadow/mutants.py`'s three. All eleven are absent at the base and present at the head (`receipts/claims.txt`). The round-2 receipts show each caught: the `gptp_plane` log has 8 `PASS planted defect` lines, and the `gptp_shadow` log has 3 `[ ok ]` #109 controls. The PR table lists 11 defect rows. The tsn-c-stack #37 plants in `ctrl_mutants.py` belong to that block's own lines, not to this count |
| R938-2-F1 MINOR Tests, Docs: the reproduction instruction predicted `15 FAIL` for the shadow suite | RESOLVED | `receipts/pr-body-live.md:193` now says `(25 FAIL)`. The hash-verified receipt `author/receipts/old-generator-red.log:63` reads `490 checks: 465 PASS, 25 FAIL`. The direct-engine figure (32, `:36`) and the PR's regression table (25 of 490) agree. The suite's checks are unchanged since that receipt |
| R938-2-F2 MINOR Tests, Docs: the tolerance comment specified an expected offset of 0 | RESOLVED | `sim_main.cpp:2985-2988` now says "its expected value, the offset before it less kGradedOffsetNs". That is exactly the second argument at `:3053`. The obsolete "nearest wrong link value (-263 ns used as 0)" sentence is gone. Its reference to `gptp_plane` phase 6 "grades the used delay to the nanosecond" is true: `gptp_plane/sim_main.cpp:687-688` checks the published used delay for equality, and `:693-694` checks the offset is exactly 0. No assertion or tolerance changed (`receipts/delta_check.txt`) |
| R938-2-R1 RESIDUE Docs: PR body status `:25` and limitations `:202` omit the harness changes | RETAINED (manager residue checklist) | Both sentences are unchanged in the live body. `:202` ("plus records and one comment in `link_delay.py`") now also omits this round's comment-only change to `gptp_shadow/sim_main.cpp`. R938-2's exact replacement text already covers it. This is wording only and affects no lens |
| R937-2-S1, R937-2-S2 SUGGESTION Docs (`SUBMODULES.md:1107`, `GPTP_PLANE.md:164`) | NOT TAKEN, optional | Both lines are unchanged and still true as written |

## Findings

### R937-3-S1 SUGGESTION - Tests, Docs - `tb/verilator/gptp_shadow/sim_main.cpp:2987`

"Used delays less than this far apart are not told apart here" is a little more absolute than the check.

- **Evidence:**
  - `near()` is an inclusive band (`:171-173`).
  - The servo's residual between trials moves `before` by a few nanoseconds. Round 2's clean probes measured every delta within 6 ns of -400.
  - So a used-delay error just under 64 ns can still fail at some trials. The intended meaning, that the check does not resolve such errors, is correct.
- **Impact:** none on any check, figure or verdict. The comment understates rather than overstates the check.
- **Optional rewording:** "Used delays less than this far apart are not reliably told apart here;".

No new RESIDUE.

- **Comment rule:** the delta's added comment lines state behaviour and reason. They contain no bench lane label, lane name, review round, reviewer identity, issue-comment id, or tool or model name. A scan of the added lines finds no non-ASCII byte (`receipts/delta_check.txt`).

## Lens results

- **[R937] PASS Conformance** - `receipts/delta_check.txt`; `CHANGELOG.md:67-86`.
  - The delta changes no product source and no image input. The checked paths are `hdl syn sw configs constraints avdecc` and every submodule.
  - All six gitlinks are equal at `e5d8a71b` and `d3cb3cf1`, among them gPTP `3ce71b76` and tsn-c-stack `a795471c`, per the #1013 ruling.
  - The change-log #109 block still states the adopted semantics: asCapable kept for negative delays, signed use floored at -800 ns, 800 good and 801 bad, the public word 0. Its new count matches the executed plant set.
- **[R937] PASS RTL** - `receipts/delta_check.txt`.
  - No RTL, firmware, configuration, constraint, ROM-ledger or gitlink change.
  - The comment-stripped `sim_main.cpp` digest is `623e7e03057c4649` at both heads.
  - The prior RTL verdict (R937-2 at `e5d8a71b`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:744-779`) depends on nothing this delta touches.
- **[R937] PASS Robustness** - `tb/verilator/gptp_shadow/sim_main.cpp:3022-3056`, `:171-173`; `receipts/delta_check.txt`.
  - The phase-22 code is byte-identical apart from comments. Every changed line is a whole-line `//` comment, and none ends in a line continuation.
  - So the round-2 probes still apply at this head: the absent pair, the unused pair, the stale bank, the bank stale only on negative delays, the wrong sign and the servo residual.
  - The new comment's statement of the band's resolution agrees with round 2's p6 result: the -3 ns trial passes when built as if the delay were 0.
- **[R937] PASS Tests** - `sim_main.cpp:2985-2992`, `:3045-3053`; `gptp_plane/sim_main.cpp:687-694`; `author/receipts/old-generator-red.log:36,63,68`; `author/receipts/gptp_shadow.log`; `receipts/pr-body-live.md:193`.
  - The tolerance comment now describes the assertion it governs.
  - The reproduction instruction predicts the executed tallies: 32, 25, and 3 of 242.
  - Round 2's source-head receipts carry by the comment-only proof: 490/490 PASS, 16/16 controls, lifecycle PASS, `gptp_plane` 102/102.
  - No test was weakened. No constant, tolerance or check name changed.
- **[R937] PASS Docs** - `CHANGELOG.md:75`; `receipts/pr-body-live.md:94,97-111,193`; `tb/verilator/gptp_shadow/README.md:38`; `receipts/docs_gates.txt`.
  - The count, the phase-22 row and the instruction all agree with the source and the receipts.
  - `check_doc_style.py` is rc 0 (25 current documents).
  - `docs_check.py` is rc 0: 0 findings across 226 md files.
  - `check_em_dash.py --base c34e7d8b` cannot judge on this host: rc 2, the pinned renderer is not installed. Hosted `docs-gates-*` run it and were in progress at the snapshot.
  - The delta adds no non-ASCII byte.
  - The retained R938-2-R1 is RESIDUE and does not leave the lens unclean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta diff and gitlinks (`receipts/delta_check.txt`); `CHANGELOG.md:67-86`; #1013 pin ruling | R937-3 | `d3cb3cf180f846a969f5baacf8b2bec34e4acd50` |
| RTL | CLEAN | delta file list, 0 image-input paths, comment-stripped digest equality; `KL_gptp_shadow.sv:744-779` unchanged since R937-2 | R937-3 | `d3cb3cf180f846a969f5baacf8b2bec34e4acd50` |
| Robustness | CLEAN | `gptp_shadow/sim_main.cpp:171-173,3022-3056`, behaviour-identical to `e5d8a71b`; round-2 probe results carried by that proof | R937-3 | `d3cb3cf180f846a969f5baacf8b2bec34e4acd50` |
| Tests | CLEAN | `gptp_shadow/sim_main.cpp:2985-2992,3045-3053`; `gptp_plane/sim_main.cpp:687-694`; r2 receipts `old-generator-red.log`, `gptp_shadow.log`, `gptp_plane.log` (hash-verified); live PR body `:193` | R937-3 | `d3cb3cf180f846a969f5baacf8b2bec34e4acd50` |
| Docs | CLEAN (RESIDUE R938-2-R1 carried) | `CHANGELOG.md:75`; live PR body `:25,:94,:97-111,:193,:202`; `gptp_shadow/README.md:38`; `receipts/docs_gates.txt` | R937-3 | `d3cb3cf180f846a969f5baacf8b2bec34e4acd50` |

## Real limits

- I ran no simulation this round. The behaviour-identity proof (`receipts/delta_check.txt`) carries round 2's executed evidence and probes from `e5d8a71b` to this head.
- The author's round-2 receipts were hash-verified and read by section. They were not re-executed.
- The evidence commit `4b3b21e2` and the head are unsigned (`receipts/evidence_commit_signature.txt`). This review verifies content identity by git blob id and SHA-256, not a cryptographic signer.
- The em-dash gate could not judge locally because its renderer is missing. Hosted `docs-gates-*` were in progress at the snapshot, so no hosted result is claimed.
- No manager source bank ran at this head, and none is claimed or inferred.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Accept hosted and act results at this exact head, including the em-dash gate in `docs-gates-*`, the elaborate gates, and exact-head `verilator-suites` and `yosys-portability` evidence.
- Carry R938-2-R1 (PR body `:25` and `:202`) to the residue checklist. Optionally offer R937-3-S1, R937-2-S1 and R937-2-S2.
- Obtain the external reviewer's verdict at this head.
- At the merge turn, build and validate the current-dev merge candidate with the builder and native banks, and link the receipts. The source base is `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`; live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`, refreshed then. Source-head receipts do not validate that tree.
- Merge authorization, post-merge containment and issue/project completion remain separate duties.

## Clone state

After review, the clone is unchanged (`receipts/clone_audit.txt`):

- HEAD `d3cb3cf1`, tree `eb3ebcb7`, and `git write-tree` equals it.
- The porcelain status is empty, and the index equals HEAD.
- All 1,984 tracked non-gitlink files equal their blob bytes and modes.
- The five initialised gitlinks are at their recorded commits. `external` stays intentionally uninitialised.
- No probe wrote inside the clone.

## Receipts

`MANIFEST.sha256` lists every published file. The scripts are portable: `tools/delta_check.sh CLONE OLD NEW`, `tools/claims.sh CLONE R2DIR PRBODY BASE` and `tools/clone_audit.sh CLONE HEAD TREE`. Here R2DIR is a download of `review-evidence/pins1125-r2`.

R937-3 FINISHED
