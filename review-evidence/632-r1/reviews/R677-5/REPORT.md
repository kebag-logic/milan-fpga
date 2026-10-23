[R677] NEGATIVE - exact head 24a292a0321df6f3516f25cb6e92e24fb1988e65

R677-5, internal independent review of kebag-logic/milan-fpga PR #770 (issues #632 and #764). The round is a delta review of `417ec528..24a292a0`: the author's round 8, three documentation and comment commits on the head R677-4 reviewed. Tree `c968fe214e70bc6c323068f146d5716729e6207e`.

## Scope

- **Read first:** AGENTS.md and CONTRIBUTING.md; the round-8 assignment (issuecomment-6369825862); R677-4 (issuecomment-6369812473) and R678-4 (issuecomment-6369815554); the review start (issuecomment-6372377589).
- **Delta judged:** `git diff 417ec528..24a292a0`. It changes 10 files, with 38 lines added and 32 removed. `git diff --stat 417ec528..HEAD -- hdl syn configs` is empty, and no submodule gitlink moves.
- **Context:** `e26f1816..24a292a0`, used for the added-line citation scan.
- **Standards:** I looked up every changed 802.1AS citation in local licensed copies of IEEE 802.1AS-2011, Cor1-2013, Cor2-2015 and 802.1AS-2020 (`receipts/clause_lookup.txt`, which lists each PDF's sha256).
- **Evidence used:** The author's round-8 packet at `c9d217d5:review-evidence/632-r1/author-r8/receipts/round8/`. Its MANIFEST.json was checked against the blobs: 2677 `author-r8/` entries, 0 missing or mismatched, and every file in the tree is listed (`receipts/evidence_manifest_round8.txt`). The evidence commit carries no GPG signature, so the manifest-to-blob match is the integrity check used. Exact-head hosted check runs were also inspected.
- **Not claimed:** No manager source bank runs at this head, and none is claimed or inferred. The physical calibration was NOT RUN, and field skips are not hardware proof.
- **Not re-reviewed:** Earlier rounds. Their code and gate coverage carries over at a tree that is unchanged outside these 10 files.

## Findings

### R677-5-F1 - MINOR - Conformance, Docs - the cross-edition pathTrace statement cites half of the 2020 rule and does not record the departure from the adopted edition

- **Where:** `docs/reference/REGISTER_MAP.md:1471-1475` (0x7DC section). The text reads: "IEEE 802.1AS-2011 10.3.10.2.1 d) writes pathTrace only from a received PathTrace TLV. When the selected Announce carries none, the engine publishes the empty sequence, the rule IEEE 802.1AS-2020 10.3.11.2.1 d) states, so count zero is preserved…"
- **Authority/evidence** (`receipts/clause_lookup.txt`):
  - **2020 10.3.11.2.1 d)** sets the per-port *receivedPathTrace* to the empty array when no TLV is present. It does not set the published pathTrace.
  - **2020 10.3.13.2.4 f) 5)** is what makes the published sequence empty. It copies receivedPathTrace to pathTrace "and, if it is not empty, thisClock is appended". Without f) 5), d) alone would yield `{thisClock}`, count one, the opposite of the stated behaviour. The PR body's own clause table describes d) as "receivedPathTrace emptied without a TLV", which confirms that d) is only half of the rule.
  - **2011** has no rule for a qualified Announce without a TLV. 10.3.10.2.1 d) writes pathTrace only when a TLV is present, so pathTrace keeps its previous value. That value is `{thisClock}` after 10.3.12.1.1 or 10.3.12.1.4 i), or the last TLV-derived trace.
  - The engine's count-zero publication is therefore a departure from the edition Milan v1.2 profiles. The author raised this as an open question in the REVIEW READY comment and in the PR body. The authoritative page does not call it a departure, and no public Issue holds the gPTP owner's decision.
  - AGENTS.md section 2 and section 8 say a specification conflict is published as one and marked as needing a decision, not left implicit.
- **Impact:** This is the one cross-edition statement the round was asked to make accurate. A reader who follows the citation finds a rule about a different variable. A reader of the interface contract is not told that GET_AS_PATH's count-zero case departs from the adopted edition. That is a clause and conformance claim, so it is not RESIDUE. No engine or test behaviour is wrong because of it, and this PR changes no engine behaviour.
- **Required outcome:**
  1. The paragraph attributes the empty publication to IEEE 802.1AS-2020 10.3.11.2.1 d) together with 10.3.13.2.4 f) 5), still explicitly labelled 2020.
  2. It states that 2011 has no such rule, because pathTrace keeps its previous value (10.3.10.2.1 d), 10.3.12.1.1), so the count-zero publication departs from the adopted edition.
  3. It links the public Issue that holds the gPTP owner's decision. The author or the manager files that Issue.
  4. No engine change is made in this PR.
- **Verification:**
  - Read the paragraph against both texts.
  - The linked Issue exists.
  - `git grep -n '802.1AS-2020' docs/reference/REGISTER_MAP.md` shows only the labelled statement.
  - The docs gates (`docs_check.py`, `check_doc_paths.py`, `check_gptp_docs.py`, the em-dash gate) pass.

### R677-5-R1 - RESIDUE - Docs - two more review-history labels in the same file's module docstring

- **Where:** `tb/verilator/milan_dp/dynmap_mutants.py:29` and `:35`. Line 29 reads "The #637 round-2 controls follow (reviews R669-1 and R670-1): seven that". Line 35 reads "…and the round-1 ordering, which REMOVEs…".
- **Evidence:** These lines are the same class as R678-4-R1 and reached this PR through the dev merge. They are on dev `e5b480a3` too (`git log -L29,29` -> `df284d1d`), so #746 tracks them. They are not new in the round-8 delta. R678-4-R1's exact fix named five lines, and all five are done.
- **Exact fix:**
  - `:29`: "The #637 round-2 controls follow (reviews R669-1 and R670-1): seven that" -> "The #637 map-restore controls follow: seven that".
  - `:35`: "and the round-1 ordering, which REMOVEs" -> "and the former restore order, which REMOVEs".
  - Leave the `ROUND1_ORDER` identifier and the `:387` mutation label. They are executable data, and the label is printed in the campaign's verdict lines.
- **Effect:** This is wording only, so it does not change the verdict or leave a lens unclean. It is for the residue checklist and #746.

### SUGGESTIONS (optional)

- **S1.** `dynmap-mutants` assumes `milan_dp_render`'s generated inputs (`tdm8r_aemi.bin`, `ltn_rom.hex`, `ucode.hex`) already exist. In a fresh clone the listener clean control fails, as `round8/dynmap_mutants_24a292a0/attempt1_stopped/NOTE.txt` shows. Dev carries the same precondition, and TESTING.md does not state it. It should become the dev follow-up Issue the author proposes, either a stated precondition or a Makefile prerequisite.
- **S2.** `docs/design/GM_LOSS_RECOVERY.md:321` says "the PDUs stamped across the steps", but the row's subject is "One 1.5 s grandmaster step". The milan_dp README row says "across the step". This text was already there before the round-8 edit. Align it if the leg's graded event is the single step.

## Prior findings at this head

| Finding | Required outcome | Status at 24a292a0 | Evidence |
|---|---|---|---|
| R677-4-F1 / R678-4-F1 | Matrix 4.4.4.5/.9 row and AAF_LATENCY_TAPS state the per-event rule, the once-per-PDU counts and the untimed rule, and keep the physical limits | **Resolved at cause** | `MILAN_COMPLIANCE_MATRIX.md:221` and `AAF_LATENCY_TAPS.md:105-109` now state it, and they agree with `KL_render_queue.sv:75-97`: per-event late and early drops, once in `refused_o`/`late_o`/`early_o`, `tv=0` untimed counted once in `untimed_o`. The SILICON and #117 limits are kept. The retired wording returns no hit outside `docs/history` (`receipts/findings_resolution.txt`) |
| R677-4-F2 / R678-4-F2 | `GM_LOSS_RECOVERY.md:321` reads 21 controls plus two clean legs, 23 checks, and keeps the five-control sweep text. README:90 describes the current leg | **Resolved at cause** | `CONTROLS` has 21 entries (AST). The counts agree at `GM_LOSS_RECOVERY.md:253` and `:321`, `TESTING.md:278` (16+5) and `README.md:1139`. `README.md:90` names `tu`, refused and counted PDUs, and no render re-base |
| R677-4-F3 | TESTING row says notify passes at the adopted pin and names the gsi-mutants gate. "until the pin moves" is gone | **Resolved at cause** | `TESTING.md:647`. `git grep 'until the pin moves'` is empty. `gsi_mutants.py:113-169` plants the GET_STREAM_INFO-word gate against `[NOTIFY] … CRF step 3` |
| R678-4-F3 | The nine gPTP citations cite correct 2011 clauses, with corrigenda where they apply. Review `:1471`. Scan the added lines | **Resolved for the nine sites, with `:1471` retained as R677-5-F1** | Boot and reset sites: 2011 10.3.12.1.4 b)/i), and Cor1-2013 restates that clause, so citing it is correct. Append sites: 2011 10.3.10.2.1 d), which Cor1 and Cor2 leave unchanged. Cor2-2015 touches only Figure 11-8. `:1480` is corrected too. The added-line scan finds one 2020 citation, `:1474` (`receipts/added_line_scans.txt`). That statement is labelled 2020 but incomplete: see F1 |
| R678-4-R1 | The exact fix at five lines | **Resolved as specified** | `dynmap_mutants.py:154`, `:168`, `:316`, `:345` and `:386` are fixed, and the AST is identical to 417ec528. Same-class lines `:29` and `:35` are recorded as R677-5-R1 |
| R677-4-S1, S2 | optional | not re-judged | They are outside the delta |

## Applied-lens evidence

```text
[R677] MINOR Conformance - docs/reference/REGISTER_MAP.md:1471-1475 - cross-edition pathTrace statement (R677-5-F1)
[R677] PASS Conformance - REGISTER_MAP.md:1051,:1478,:1480; SUBMODULES.md:242,:244; MILAN_COMPLIANCE_MATRIX.md:221; AAF_LATENCY_TAPS.md:105-109 - each checked against 802.1AS-2011 10.3.12.1.4 b)/i) (+Cor1-2013), 10.3.10.2.1 d), and against KL_render_queue.sv:75-97 for the IEEE 1722-2016 4.4.4.9 per-event rule (clean except F1, so the lens is not clean)
[R677] PASS RTL - git diff --stat 417ec528..24a292a0 -- hdl syn configs (empty) and unchanged gitlinks (receipts/comment_only_check.txt, receipts/clone_integrity.txt) - nothing in RTL scope changed; R677-4's RTL verdict at 417ec528 carries over to an RTL tree identical to the one it covered
[R677] PASS Robustness - receipts/comment_only_check.txt - sim_gptp.cpp and sim_ax1x1gptp.cpp tokens with comments stripped are identical to 417ec528, and the dynmap_mutants.py AST is identical, so no malformed-input, reset or timeout path changed; R677-4's verdict carries over
[R677] PASS Tests - round8/legs_24a292a0 (gptp 185/185 rc 0; ax1x1gptp 155 checks, 0 failures, rc 0; Verilator 5.050), round8/dynmap_mutants_24a292a0 (68/68 = 5 clean legs + 63 caught, matching the 63 MUTATIONS entries), round8/lint_24a292a0 (89 <= 89, check-baseline PASS, py_compile ok), gmstep CONTROLS = 21 against every page that states a count - the evidence is at the exact head and the inventory matches
[R677] MINOR Docs - docs/reference/REGISTER_MAP.md:1471-1475 - R677-5-F1 (also attributable to Conformance)
[R677] PASS Docs - the other 9 delta files; docs gates round8/docs_steps_24a292a0 (44 steps: 42 rc 0 under GNU Make 4.3, 2 skipped by rule; the 5 markdown gates on CPython 3.12.3; no-git pair rc 0); own spot check receipts/docs_gate_spotcheck.txt (docs_check, check_doc_paths, check_doc_style, check_gptp_docs, check_submodule_docs rc 0); comment-rule scan of the delta's added source lines finds no new instance (receipts/added_line_scans.txt) - Docs is not clean because of F1
```

**My own spot check of the docs gates:**
- CPython 3.14.8, scripts run directly at the exact head.
- The em-dash gate could not run here because `html5lib` is not installed. The author's receipt shows that gate at rc 0: 0 findings over 1178 added lines, `e5b480a3..HEAD`.

**Hosted checks at the exact head, sampled 2026-10-23T19:01Z** (`receipts/hosted_checks_24a292a0.txt`):
- 6 completed with success: bdd-conformance, changes, docs-check-no-git, full-ci-gate, Prepare pinned Yosys and wire-accountability.
- 1 skipped: Physical gPTP, nightly and manual only.
- 38 were still queued or in progress, so they are not evidence. The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R677-5-F1 open) | REGISTER_MAP.md:1051,1471-1480; SUBMODULES.md:242,244; MILAN_COMPLIANCE_MATRIX.md:221; AAF_LATENCY_TAPS.md:105-109; the 2011, Cor1, Cor2 and 2020 texts; KL_render_queue.sv:75-97 | R677-5 | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| RTL | CLEAN | the empty hdl/syn/configs diff and the gitlinks; R677-4's coverage carries over to an unchanged RTL tree | R677-5 (delta), R677-4 (body) | 24a292a0321df6f3516f25cb6e92e24fb1988e65 (RTL identical to 417ec528) |
| Robustness | CLEAN | the comment-only proof (comment-stripped C++ tokens and Python AST identical) | R677-5 (delta), R677-4 (body) | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| Tests | CLEAN | round8 leg, dynmap, lint and py_compile receipts at the exact head; CONTROLS and MUTATIONS inventories; manifest verification | R677-5 | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| Docs | UNCLEAN (R677-5-F1 open) | all 7 delta docs pages, README.md:90, the docs gate receipts, my own gate spot check, the comment-rule scan | R677-5 | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |

## Limits and pending manager duties

**Limits:**
- This is a delta review only. Earlier rounds' code and gate coverage was not re-executed.
- I ran no Verilator leg or campaign. The execution evidence is the author's exact-head receipts, and the identical-token and identical-AST proof shows the delta cannot change any executed line.
- My docs spot check used CPython 3.14.8 and GNU Make 4.4.1, not 4.3. The 4.3 and 3.12.3 evidence is the author's.
- The em-dash gate was not reproduced here because html5lib is missing.
- No manager source bank exists or is inferred at this head.
- Physical calibration is NOT RUN, and field skips are not hardware proof.
- The standards texts are local licensed copies. The extractions are not published; the receipts carry only clause numbers and short quotations.

**Pending manager duties:**
- Carry R677-5-R1 to the residue checklist and #746.
- Ensure the gPTP owner's decision on the count-zero pathTrace (F1's linked Issue) is filed.
- Consider S1 as a dev follow-up.
- Build and validate the current-dev merge candidate (source base e26f1816, live dev e5b480a3) with builder and native banks at the merge turn.
- Accept the hosted and act results at the exact head once they complete.
- Obtain the second independent positive review and the full completion bar before any merge.

**Integrity:**
- The clone is restored: HEAD and index tree are c968fe21, `git status --porcelain` is empty, and the ignored `scripts/__pycache__` created by my gate runs was removed.
- The six gitlinks are unchanged: external efeb541a, gptp-processor 55680bff, protocol-processor 93fb0b2d, lwSRP 08ee86e8, tsn-c-stack 70936b77, verilog-axis 48ff7a7e.
- I made no GitHub write.

R677-5 FINISHED
