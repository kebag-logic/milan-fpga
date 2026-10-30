[R744] NEGATIVE - exact head 18a4dc1fcf91528a52737d5ea830b5acd5d543c4

Issue #210 / PR #211, whole-PR review, round R744-1. Base `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`; tree `7cdbc61bb2296f923585b42d3cd0a01baf6d3991`. Two open MINOR findings fail the acceptance rule that a page marked current must agree with the source and its cited authority. No implementation regression was found.

**Independent reconstruction and scope**

The supplied repository instructions were read first. This tracked tree has no AGENTS.md or CONTRIBUTING.md. The documentation conventions and reading order, issue body, architecture/interface authorities, complete 36-file delta and five-commit history were examined. The delta is 33 Markdown files plus Makefile and two documentation checkers. The pinned public evidence was examined only after the independent diff pass.

The mandatory isolation rule took precedence over the requested comment-reading order: issue/PR comments were deferred until `INDEPENDENT-VERDICT.md` and its five-lens ledger were written. That checkpoint already records this negative verdict and both findings. Only then were the public scope decisions, manager review-start comments and prior-findings channels read. No private author material or another reviewer's report was read. No source fixes, commits, pushes or GitHub writes were made.

[Issue #210](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/210) freezes the four acceptance items. The [parent plan](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6518880512) schedules this work after processor #203; the source base contains that completed work. The [public scope statement](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/210#issuecomment-6519117148) permits Markdown and cheap documentation gates, leaving implementation changes to separate work. Later comment reconciliation did not change the independent verdict.

**Findings**

**F1 — MINOR — Conformance, Docs — retained known-invalid clause citation.**

- Artifact: `docs/architecture/02_interfaces.md:284`, read with the current status and claimed clause checks in `docs/INVENTORY.md:27` and its interfaces row.
- Evidence/authority: the page still says §34.6.1.1 defines the per-stream idleSlope. The [PR body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/211) and [pinned public handoff](https://github.com/kebag-logic/milan-fpga/blob/9167129dc46bad29d393b387766f91aaaed9a6a9/review-evidence/pp210-r1/author/HANDOFF.md) explicitly identify that clause as nonexistent in IEEE 802.1Q-2014 and identify §34.6.1 as the correct authority. This PR corrects the same reference at interfaces:587 and SRP engine:53, leaving interfaces:284 behind. The adopted-edition preview independently confirms the heading “34.6.1 Talker behavior”; its full clause body was unavailable, so this finding relies on the public edition-specific correction account for the nonexistent subclause, not on a claimed full-standard reread. See `authority-access.log`.
- Impact: a page newly classified current still sends an integrator to an authority the sweep itself says does not exist; the inventory's blanket clause-verification statement overstates the result.
- Required outcome: correct this remaining citation to IEEE 802.1Q-2014 §34.6.1, confirm the associated per-stream statement against that clause body, and update the inventory evidence to reflect the completed check.
- Verification: search all current Markdown for `34.6.1.1`, reconcile every remaining occurrence with the named edition, and rerun `make -j16 check`. A clause claim is outside the wording-only RESIDUE exception.

**F2 — MINOR — Conformance, RTL, Docs — current µISA inventory omits an implemented and emitted operation.**

- Artifact: `docs/architecture/06_aecp_engine.md:1427` says “29 operations”; the Data row at :1434 lists only MOVE, COMPARE and SET_MASKED. The inventory marks this architecture page current.
- Authority/evidence: `hdl/aecp/ucpu_pkg.sv:90` declares `OP_SHIFT_R = 5'd29`, the thirtieth operation in the 0..29 enumeration. `hdl/aecp/KL_aecp_ucpu.sv:681` executes a logical right shift of the 64-bit operand by `imm[5:0]`. `hdl/aecp/ucode/gen_ucode.py:33` assigns SHIFT_R opcode 29 and uses it in live descriptor programs. Reviewer regeneration found **13 opcode-29 words** in the 2048-word ROM, at addresses 613, 619, 658, 661, 665, 1157, 1163, 1195, 1540, 1955, 1965, 1975 and 1985. See `source-excerpts.log` and `construction.log`.
- Impact: the current programming reference gives the wrong instruction count and an incomplete instruction set. This is a source and generated-output contradiction, even though the stale text predates the sweep.
- Required outcome: state 30 operations and add SHIFT_R to the Data group with its actual operand width and shift-count semantics. Keep any historical instruction-set discussion explicitly historical.
- Verification: compare the revised table with the complete opcode enum and execution cases, regenerate the ROM and account for opcode 29, then rerun the documentation gates. This changes a numeric and instruction-set claim; it is not RESIDUE.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue acceptance and public scope; docs conventions; interface and command authorities; REBOOT/source trace and current-page numeric claims; F1, F2 | R744-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| RTL | UNCLEAN | Top interfaces and shutdown sequence; timer map; µCPU enum/execution; both ROM generators and outputs; document-to-source contradiction F2 | R744-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Robustness | CLEAN | Inventory implementation and 12-case selftest; independent stale-row, missing-row, missing-file, broken-target and broken-anchor probes; restored clean controls | R744-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Tests | CLEAN | Documentation/static gates and HDL lint; five focused suite executions; generated-output equality; workflow and exact-head hosted-status inspection | R744-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |
| Docs | UNCLEAN | Complete Markdown delta; 63-row inventory; glossary, navigation, summaries and retirement banners; 43 statement checks; F1, F2 | R744-1 | 18a4dc1fcf91528a52737d5ea830b5acd5d543c4 |

CLEAN records no defect found within that lens's examined evidence; it does not turn pending hosted execution or unavailable standard text into a pass.

**Executed evidence and construction proof**

`statement-checks.md` records **43 individually traced statements**, including the REBOOT routes, lock/notification ordering, command admission hold, RX discard, final-frame drain, held reset request, persistence boundary, and shipped-ROM list. REBOOT §6.11 is retained from the base, not a new implementation in this PR. Its source behavior was checked independently; full IEEE §7.4.43 and Milan clause text were not independently available.

| Check | Reviewer result | Receipt |
|---|---|---|
| `make -j16 check` | rc 0; 41 diagram-language blocks and 18 waveform blocks; all target checks pass | `docs.log`, `docs.rc` |
| Matrix freshness, µPC map, opcode selftest and opcode check | rc 0 | `static.log`, `static.rc` |
| HDL lint | rc 0 | `hdl-lint.log`, `hdl-lint.rc` |
| Inventory at head | 63 tracked Markdown files and 63 rows: 59 current, 1 generated, 3 superseded; all purpose/audience/describes/evidence cells populated | `inventory-audit.log`, `inventory-clean.log` |
| Stale row for absent file | rc 1, NO FILE | `inventory-stale-row.log` |
| New unlisted page | rc 1, NO ROW | `inventory-missing-row.log` |
| Existing page removed with row retained | rc 1, NO FILE | `inventory-missing-file.log` |
| Broken link target and invalid collapsed anchor | each rc 1, specific missing-target/anchor diagnostic | `link-broken-file.log`, `link-broken-anchor.log` |
| Restored probe controls | inventory and links rc 0 | `inventory-restored.log`, `links-restored.log` |
| prng / dispatch / desc_store / timer_map / dyn_state | rc 0 each; **76 / 211 / 586 / 1360 / 118** checks, all pass; dyn_state is 62 + 56 | corresponding `suite-*.log` and `.rc` |
| Base/head generated ROM comparison | both byte-identical | `construction.log` |
| Privacy/workflow attribution delta scan | no new private-path or assistant-attribution matches and no newly introduced R-labelled occurrences | `hygiene.log` |

The new gate and link-checker changes are read-only. The top Makefile only adds the inventory target, its prerequisite and explanatory comments; no hardware-build or render recipe changes. Every other non-Markdown tracked path and mode, including RTL, models, generators, suite build recipes, workflow and committed generated artifacts, is identical at base/head. Both shipped ROM kinds were regenerated at both revisions: microcode SHA-256 `49a993bede26a9a16179f66956387b4709d1f86dcd9bf5edb7a79c6e996e1176`; listener transitions `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`. The complete HDL read-memory initialization scan finds these two ROMs; no dispatch or response-size ROM is shipped. No full hardware build is asserted.

The pinned compiler's identity was verified before use (`compiler-identity.log`). Independent static jobs ran concurrently under one joined foreground runner. Focused suites used two concurrent workers, each limiting compiler build workers to four, with `make -j16`. Every disposable tree and temporary extraction stayed under packet `scratch/`. The original review checkout was never modified. Its **754 tracked blob bytes and executable modes, index tree, HEAD and worktree** were verified against the requested tree; the repository has **zero submodule gitlinks**. Final verification is in `final-integrity.log`.

**Public evidence and prior findings**

The [pinned evidence directory](https://github.com/kebag-logic/milan-fpga/tree/9167129dc46bad29d393b387766f91aaaed9a6a9/review-evidence/pp210-r1) contains the author's handoff and PR-body narratives, not raw gate execution logs. Their published hashes were verified (`published-evidence.log`). Author-reported gate passes remain distinct from the reviewer executions above. The author explicitly reports that the NVM figures gate did not finish. Base/head input equivalence is useful but does not constitute its executed pass.

After saving the independent verdict and ledger, the issue comments, PR comments, submitted reviews and inline review comments were queried. **No prior public FINDINGS on PR #211 were published at the final query**: the PR had the two review-start comments and zero submitted/inline reviews. Thus there are no earlier public findings to resolve or retain. `public-reconciliation.json` preserves the query result and timing. Disclosed existing review labels and existing source-comment citations remain separately tracked; they are not newly introduced defects here. The post-verdict reconciliation did not weaken or replace F1/F2.

Exact-head hosted push run [41043142178](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/41043142178) and PR run [41043150656](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/41043150656) had completed successful documentation and portability jobs when inspected. Their suites jobs were still running the lint/full-suite step; traceability execution, campaigns and NVM figures were pending. The compiler build step was skipped because its cache was used; this is not a skipped simulation pass. See `hosted-status.json`. Therefore **not every repository gate is yet evidenced green**. Hosted/act acceptance remains the manager's responsibility.

**Limits and pending duties**

- This review sampled the current claims as recorded above; it does not claim a sentence-by-sentence proof of every retained page. Complete IEEE 1722.1-2021, IEEE 1722-2016, IEEE 802.1Q-2014 and Milan v1.2 clause texts were not available through the attempted public sources. No newer edition was substituted. The exact standard-access limits, including the REBOOT clause limitation, are recorded in `authority-access.log`.
- Full parent/processor/timing/synthesis/builder banks, hardware and physical calibration were NOT RUN. Field skips and simulation receipts are not hardware proof.
- No manager source bank at this exact head exists or is inferred. Final current-dev merge-candidate builder/native validation is separate: the supplied source base is `a9e84b66`, live dev is `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. The manager must validate the actual merge candidate and publish its receipts at the merge turn.
- Close F1/F2 in a new reviewed head, complete hosted acceptance including the pending NVM figures step, obtain the required independent positive reviews, and preserve the owner's separate handling of the disclosed existing labels. This report authorizes no merge.

Portable reproductions are `run-gates.py SOURCE PACKET [COMPILER_DIRECTORY]`, `run-focused.py DISPOSABLE_HEAD PACKET COMPILER`, `probe-gates.py SOURCE PACKET`, and `verify-construction.py SOURCE PACKET`; invoke each with `python3`. Set up a disposable clone under `PACKET/scratch/` for gate/suite runs. Only REPORT.md and files named in MANIFEST.sha256 are publishable; scratch trees and downloaded PDFs are excluded.

R744-1 FINISHED
