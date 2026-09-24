[A228] REVIEW READY
Commit: 26a0cc3042300d5213edf7b1c0037a3ae2612ecd (tree dd03278237b213f237e911ce3c370e6471bc8be8)

- Branch `437-cmark-gfm`: one one-line commit, no trailers, on the reviewed head 196cb7d99cb06631df514715979a5f82fbb1f7aa.
- Not pushed: the assignment allows no push, so pushing is the manager's step.
- Packet: A228 (HANDOFF.md, COMMANDS.md, PR-BODY.md, MANIFEST.sha256, gates/, receipts/, probes/, render-cache/), for the manager to publish.

Changed:

- **F1 MAJOR (R237-5 F1 = R238-4 F1).**
  - The guard is wider than letter case. A character reference (`&#100;ata-...`) or a backslash escape in text, read as attributes of a raw tag the page leaves open, forges the position too.
  - At 196cb7d9 all four spellings (upper, mixed, character reference, escape) list the hidden heading and win the exemption through the shipped gate: rc 0, 1 exempt.
  - The renderer now also renders the page without positions (GitHub's own HTML) and reads the page as rendering nothing when that HTML spells the attribute in any ASCII case. Positions are the only difference between the two renderings, on 1062 recorded and fuzz pages and all 164 tracked pages.
  - `refusals()` names a page whose text spells the attribute in any case (R237-5 S2, R238-4 S1), so it is left alone and exempts nothing.
  - CONTRIBUTING 6.1, DOC_GENERATION.md and the module docstring state this.
- **R238-4 F1's anchor requirement.** 11 `file_view` pages recorded in GitHub's file view (`markdown` mode). On each, every heading `headings()` lists, label and anchor, must be one GitHub shows. At 196cb7d9 six of them fail.
- **R237-5 F2.**
  - The syntax-tree walk uses a stack.
  - New finding: where GitHub nests an element 256 deep, its content and everything after it are lost (255 block quotes, 128 list levels or 255 `<div>` tags, measured 2026-09-24). At 196cb7d9 a 256-deep page listed a heading GitHub drops.
  - A page nesting an element more than 200 deep now renders nothing. Tracked pages reach 8.
- **R237-5 F3.** One arm per own-element kind. `list` is observable only on a blank line it alone holds, and is armed there.
- **R238-4 F2.** M17: heading-tag arms. M15: `bind()` drift arms. M11: strikethrough. S3: the extension list is spelled.

Validation (all at 26a0cc30):

- Every `docs.yml` command: 96 runs, all rc 0 (`gates/EXITS.txt`, logs). This covers the no-git job in a `git archive` export, the RV32 SDK, compiler and builder steps (scratch HOME; builder `ALL GATES PASS EXCEPT 11 NOT RUN`), `check_py_idiom` (10 ≤ 10, 9 ≤ 9), `git diff --check 759da623 HEAD`, and `check_em_dash.py --base 759da623` (0 findings, 0 exempt).
- TOC self-test 1501/1501 (floor 1433 → 1501); em-dash 339 (was 332).
- The same TOC and em-dash gates pass under CPython 3.12.13 with the lock installed from its hashes.
- Mutations:
  - this round's 23: 23 killed at named arms, including the reverse mutant (guard back to case-sensitive) and R238-4's M22 fix-probe;
  - R238-4 `mutate.py`: 19 killed;
  - R237-5 `mutate.py`: 14 killed;
  - `mutate_own_element.py`: 6/6 killed.
  - The six reviewer mutants whose lines were rewritten map to equivalents that are killed.
- The reviewers' e2e probes at 26a0cc30 (R238-4 `emdash_spoof_e2e.sh`, R237-5 `probe_emdash_gate.py`) and a four-spelling probe: no hidden heading listed, 0 exempt.
- Both gates answer 1200-deep block-quote and list pages (rc 1, 0 exempt) where 196cb7d9 raised RecursionError.
- The 164 tracked pages give identical answers at both heads, and `--write` changes no owned page.

Acceptance criteria:

- 1: met, 362/362 shapes plus 11 file-view pages.
- 2: met.
- 3: met; every property both reviews listed has an arm shown to fail when removed.
- 4: met; no tracked page changes.
- 5: met.

GitHub renderings sent: 40 requests of synthetic pages, kept byte for byte. 21 are in the fixture and 19 are depth probes.

Open risks/questions:

1. Some withheld pages are not named by `refusals()`: a page nested past 200, and one spelling the attribute only through an escape. `--check` then reports drift and `--write` would drop their Contents block. This only withholds.
2. Proposed new issue: when a comment closes inside a block quote or list whose element it swallowed, a later visible line is labelled commented. This affects labels only, withholds only, and predates this PR (`receipts/partial-swallow-containers-at-26a0cc30.txt`).
3. The depth bound relies on GitHub's limit as measured on 2026-09-24.
4. Hosted CI, act and the candidate merge with live dev were not run by the author.
5. Not adopted: R237-5 S3/S4 and R238-4 S4 (refusal wording and extra raw-tag shapes), and R238-4 S2 (a pre-existing anchor, outside #437, for the manager).
