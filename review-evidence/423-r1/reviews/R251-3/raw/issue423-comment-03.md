https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5776812551
[R241] NEEDS DECISION: trusted head 88e9276b2a220c716f64a843f7e1eb8f9265e896; public scope is parent kebag-logic/milan-fpga#423 AC1–3, assignment comment 5776564663, and Mister-M-alt/FPGA-gPTP PR62 replay topology.

Readiness/design review only. This is not a POSITIVE merge verdict, implementation approval, containment waiver, or processor-pin adoption.

**Conclusion and smallest remaining decision.** The redundant merge can be accounted for structurally. Historical replay does not prove retention at the current target. I established a conservative current-entry criterion, but it adds no acceptance beyond the unchanged checker's existing path proof and does not accept the motivating later-extension case. I did not establish a useful new proof satisfying that positive case while refusing lost work.

Record whether the required positive may exclude the published same-file extension and the actual PR62 target tips. If so, explicitly retain those cases as unresolved; the conservative criterion below needs no new containment code. If those cases must pass, define and demonstrate the permitted relation between changed current postimages and the replayed work before implementation. Historical matching alone, or merely excluding exact inverse commits, is insufficient. Recommend keeping #423 in Backlog. This is a bounded finding, not a claim that no stronger algorithm can exist.

**Public reconstruction.** Read the [issue body and all three available comments](https://github.com/kebag-logic/milan-fpga/issues/423), including the [assignment](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5776564663), and [donor PR62](https://github.com/Mister-M-alt/FPGA-gPTP/pull/62), its commit and empty comment/review collections. Updates carrying R242's report identity were filtered before display; none were present. No other reviewer's report or private directories were read.

Fetched all eight public blobs under [the published evidence commit](https://github.com/kebag-logic/milan-fpga/tree/6181e900cd9f7ae618e1603e2ea867a5bb4d41a6/readiness-evidence/423). Their Git blob IDs and all six MANIFEST entries verify. Both issue-body patch SHA-256 values reproduce with `git show --format=`. Full-index patch renderings, stored separately, also compare byte-for-byte between each original/replay pair. Evidence: `public/`, `logs/public-verification.json`, `logs/issue-patch-hashes-verified.json`, `logs/donor-evidence.json`.

Let P=7fa64e99490b4648797374d3fdb1fedf08145e91, A=9790ac736e6d10301ad814ffdf73dbe37b59768b, M=f27b45500cb02a5277b5cb32cef408658c1f914e, and C=3db86812096830fada2f5f276fa5f4d9f37d1d14. Actual parents are A:[P], M:[P,A], C:[M]. M and A have tree cf1818d9e3d1da24ffd75b6177f155ef8b0c04f7. Thus P is A's immediate sole parent, not merely an ancestor.

A replays as 20927af74752620b2ad0f973e8be3203994b5547; C replays as 5602e70bb4cf70c2e0e39e846e26925e27659e32. Each pair has identical patches, touched-path postimages, and whole trees. Target merges 377b8c428b226a796adde099fe07152151fd6c5d and 676d2f6be46b2775b8a008800d394c9855a5efc3 carry those respective trees.

At both original target f0f1c055ee5226f08e656c27cb1bf4c355be11ae and observed donor main c1b617435824929a790739ea8585c3fe1a328cc0, the unchanged CLI exits 1 and counts three source commits outside the target. The historical scratch predicate exits 0; the retention predicate exits 1. Four of the five protected paths differ at each target: both `tb/{tsngen,verilator/gaskets}/Makefile` and both corresponding `mutants.py` files. Changes include compiler flags, annotations, documentation and shared-header staging. These are not whitespace-identical postimages. Their semantic preservation was not established by this review. Raw differences are in `logs/donor-*-touched-paths.diff`.

**Bounded safe floor, not an adopted implementation.** `scripts/predicate.py` measures only this exact three-commit source shape:

1. `T..C` is exactly {A,M,C}; P is an ancestor of T; the ordered parent lists are exactly those above. Refuse additional source merges, octopus parents, unrelated parents and a longer incoming chain.
2. `tree(M)=tree(A)`. Additional merge resolution work is outside this shortcut, even when ordinary commits match. Independent existing proofs remain available.
3. Require a distinct whitespace-exact replay for each of A and C, using the unchanged linear helper's verbatim patch IDs and exact touched-path postimages. No linear commit is silently omitted.
4. For the union of paths changed by A and C, require C and current T to have identical `(mode, kind, object ID)` entries, including absence. Renames are unfolded; paths are literal. Incomplete history, active grafts and measurement failures cannot pass; replacement objects are disabled.

Safety conclusions: step 2 removes no merge-specific tree work; step 3 accounts for every linear source patch; step 4 proves the required final bytes/entries exist now. This is a tree-content proof, not semantic or RTL validation. Unrelated later extensions can pass. Same-file edits, even legitimate appends/refactors, are deliberately unresolved. A revert that loses a required current entry fails, whether isolated, partial, combined with other changes, or introduced by a target merge.

The unchanged path proof already accepts this conservative subset: every net-changed source path is among these protected paths. Therefore adding this predicate would not resolve #423. Do not extend the existing linear policy by silently normalizing M away. Existing ancestry and linear historical arms can accept later reverts; this was measured separately and is not changed or endorsed as current-retention evidence here.

**Executable counterexamples.** Actual process exits below: U = unchanged CLI; H = structural plus historical proof only; R = the strict scratch retention proof. H=0 never means current retention. R is a standalone scope probe, not a replacement for existing successful proofs. Every row has individual raw logs; all 25 cases and object IDs are in `logs/fixture-results.json`.

| Cases | U | H | R |
|---|---:|---:|---:|
| Exact replay; unrelated later extension; target merge retaining entries | 0 | 0 | 0 |
| Published same-file append (conservative false negative) | 1 | 0 | 1 |
| Exact revert of A or C; partial revert; revert plus unrelated work | 1 | 0 | 1 |
| Target merge discarding replayed work | 1 | 0 | 1 |
| Missing A; missing C; omitted incoming linear work | 1 | 1 | 1 |
| Missing merge-resolution work | 1 | 1 | 1 |
| Whitespace-different replay postimage | 1 | 1 | 1 |
| Later whitespace, executable-mode or file-kind change | 1 | 0 | 1 |
| Multiple source merges with later extension | 1 | 1 | 1 |
| Octopus/unrelated parents with later extension | 1 | 1 | 1 |
| Octopus/unrelated parents, exact current endpoint | 0 | 1 | 1 |
| Existing purely linear or ancestry proof after revert | 0 | 1 | 1 |
| Append exactly restores a deleted tail | 1 | 0 | 1 |

The last row defeats a tempting prefix/append-only relaxation: A changes `keep\ndeleted tail\n` to `keep\n`; after replay, appending `deleted tail\n` exactly undoes A. Retaining a postimage as a prefix is insufficient. The partial/composite revert rows also rule out checking only for a whole-commit inverse.

**Acceptance and design lenses.** AC1 is reproduced, including the unchanged public fixture. AC2 has a safe structural boundary and conservative byte criterion, but no useful adopted extension. AC3's simple exact replay passes and negative controls refuse; the published later extension and actual PR62 remain unresolved. AC4 is not satisfied by a design review: production implementation, applicable gates and final-head independent reviews remain future work.

| Lens | Named artifacts examined | Design-only result |
|---|---|---|
| Conformance | `CONTRIBUTING.md:178`, `AGENTS.md:91`, #423 AC1–3, `check_merge_containment.py:437,482,519` | MAJOR readiness gap: accepting changed postimages needs a settled retention/supersession contract. |
| RTL | `REQUIREMENTS.md:213`, #423 objective, PR62 changed-file list | PASS for scope boundary only: no product RTL/protocol change is proposed; no RTL behavior or gate coverage claimed. |
| Robustness | `scripts/predicate.py`, all fixture rows, `merge_containment_selftest_content.py:298,470` | MAJOR readiness gap: historical/prefix shortcuts admit lost work; strict rule refuses but leaves positives unresolved. |
| Tests | `merge_containment_selftest.py:57`, content controls at `:231,261,298,470`, `logs/fixture-results.json` | MAJOR readiness gap: a useful current-retention acceptance predicate lacks its positive proof. Existing self-test and bounded probes passed. |
| Docs | `AGENTS.md:191,359`, `REQUIREMENTS.md:213`, public assignment, this report | MAJOR readiness gap: public decision must specify accepted later changes and deliberate false negatives before takeover. |

These are design findings, not a production lens ledger. Required change for the shared readiness gap: record the positive-case boundary above, and bind any stronger rule to executable current-tip positives and lost-work negatives. Verification must preserve the current checker controls and distinguish historical replay from present retention.

**Validation and lane impact.** Unchanged self-test: exit 0, 145 assertions. Deterministic offline matrix: 25 cases, 75 process exits, runner exit 0. Two initial baseline expectations were corrected to reflect existing exact-endpoint acceptance; initial measurements and the explanation are retained. No production test was weakened. Public fixture: exit 0, reproducing both refusals and the unsafe historical helper results. No hardware, builds, installs, Docker/act, public writes, implementation commits or other agents were used. Other lanes and gates remain unaffected. #423 stays Backlog pending public resolution; A170's #372 author assignment is unaffected.

Initial/final checkout snapshots are byte-identical: HEAD above, clean status, index SHA-256 e9b72a6b5bb16136b6f925c6f78ccbe3bea62e1a768861e1bbf796696623a7a2, and all 855 enumerated checkout entries' bytes/kind/mode unchanged. See `logs/integrity-comparison.json`. Reproduction commands and artifact descriptions are in `REPRODUCE.md`. Manager publication only, with path neutralization.

R241-DESIGN FINISHED
