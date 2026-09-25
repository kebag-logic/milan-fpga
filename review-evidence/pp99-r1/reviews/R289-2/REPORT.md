[R289] POSITIVE - exact head 9cde1c19dbfd859257be8e012d4455856fcfce3b

# R289-2 external independent delta review: processor issue #99 / PR #119

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Head under review:** `9cde1c19dbfd859257be8e012d4455856fcfce3b`, tree `899808411b924cd161e849039806685e939e6fc4`. Verified in `receipts/verify-clone.txt`. The live PR head is this commit.
- **Round-2 delta:** `663d50d..9cde1c1`. It is one commit, "Fix parameter owner anchors and document the inventory gate". Its parent, `663d50d`, is the head that R289-1 reviewed.
- **Round scope:**
  - The [A10] round-2 assignment is issue #99 comment 5827048744. It covers R288-1 F1 and F2, and R289-1 F1.
  - Executor [A302] posted the ready comment 5827134004.
  - The public review start is PR #119 comment 5827215676.
- **Lenses applied:** Conformance, RTL, Robustness, Tests and Docs.
  - I applied each lens independently at this head. Each has its own evidence below.
  - For everything outside the round-2 delta, my R289-1 ledger stands. The delta touches nothing that ledger examined, except the three docs files, which I re-examined here.
- **Order of work:** I formed the verdict and ledger before reading the other reviewer's public findings (`receipts/verdict-written-at.txt`). After that I read them and resolved each one below.

## Verdict

POSITIVE. No MINOR, MAJOR or BLOCKER finding is open at this head.

- **R289-1 F1 is resolved.**
  - `docs/architecture/09_verification.md:120` adds a `params` row to the section 7 `make check` table.
  - The row names `scripts/check-integrator-params.py` and states what it asserts.
  - That statement matches the checker's code (`scripts/check-integrator-params.py:91-128`) and the Makefile target (`Makefile:13,39-40`).
- **The owner-anchor item is resolved** (round-2 assignment, item 1).
  - `docs/guides/integrator.md:80-83` now use `#sec-desc-memory`. That explicit anchor already existed at `07_memory_maps.md:146`.
  - `docs/guides/integrator.md:88` now uses `#sec-resp-memory`, a new explicit anchor at `07_memory_maps.md:215`.
  - All five links resolve in the repository link gate. They also resolve in the HTML that GitHub renders for the exact head.
  - The superseded slugs are confirmed dead on GitHub.
- **Only the assigned files changed.**
  - The changed files are 07, 09 and the integrator guide: 7 insertions, 5 deletions and no mode changes. `git diff --check` is clean.
  - `hdl`, `tb`, `syn`, `scripts`, `.github` and the `Makefile` are byte-identical to `663d50d`.
- **All gates pass.** `make check` and every docs-gates command return 0.

## Findings

No open MINOR, MAJOR or BLOCKER findings.

### Suggestions

These are non-blocking and do not affect any lens verdict.

- **S6 (Tests, Docs): the link gate's heading slug differs from GitHub's.** This is new this round and outside the scope of this issue.
  - **The mismatch:** `scripts/check-links.py:20-24` collapses each run of whitespace into one hyphen. GitHub instead turns every space into a hyphen after it drops punctuation.
  - **Example:** for the heading "3.3.1 Realization — the image …", the gate accepts `#331-realization-the-…`. GitHub renders `#331-realization--the-…`. This mismatch is the root cause of the R288-1 F1 defect.
  - **Probe:** `revert-to-round1-slugs` (in `receipts/probe-anchors.txt`) puts the round-1 fragments back. The link gate still returns 0; only the GitHub-faithful check returns 1.
  - **Existing dead links:** at this head, four links are dead on GitHub. None of them is in a file this PR changes: `02_interfaces.md:554`, and `05_acmp_engine.md:81`, `:404` and `:415`. All four already exist at source base `008edbbf` (`receipts/github-anchors-all.txt`).
  - **Effect on 09:** the `links` row of `09_verification.md` section 7 claims "every `#anchor` exists in its target". That holds only under the gate's own slug.
  - **Recommendation:** open a separate issue, per section 4 of the parent AGENTS.md, to align the slug and fix the four links. This PR sidesteps the problem by using explicit anchors, which is the right choice.
- **S1 to S5 are retained as in R289-1, unchanged.** This round did not touch `scripts/`, the diagram 21 files, `docs/diagrams/README.md` or guide section 9.
- **S7 (Docs): two secondary lists still omit the params gate.** This was already noted as optional in R289-1 F1.
  - `docs/guides/hdl-engineer.md:218` and `docs/README.md:154` still do not name the params gate.
  - The assignment said "Change nothing else", so leaving them alone was correct for this round.

## Correction to my R289-1 evidence

- **What I recorded:** in R289-1, the Conformance lens said the 07 §3.3.1 and §3.3.2 anchors resolve. That rested on `check-links.py` alone.
- **What was actually true:** because of the slug mismatch in S6, that evidence did not prove the links resolve on GitHub. At `663d50d` the five links were dead on GitHub. The controls in `receipts/github-anchors-changed.txt` show this.
- **How it was found and fixed:** the other reviewer's round-1 findings raised the defect publicly, and it is fixed at this head.
- **What I added this round:** my R289-1 packet had no GitHub anchor script. For this round I wrote an independent GitHub-faithful checker, `github_anchor_check.py`. It checks each link in two ways:
  - offline, against GitHub's slug rules;
  - online, against the ids in GitHub's own HTML render of the target at the exact SHA. This uses read-only GET requests.

## Resolution of prior public review findings at this head

| prior finding | status at 9cde1c1 | evidence |
|---|---|---|
| R289-1 F1 (MINOR; Docs): the 09 §7 table omits the `params` target | RESOLVED | `09_verification.md:120`; wording checked against `check-integrator-params.py:91-128` and `Makefile:13,39-40`; `receipts/delta-audit.txt` |
| R288-1 F1 (MINOR; Conformance, Docs): five owner links point at anchors GitHub does not render | RESOLVED | `integrator.md:80-83,88` now point at `#sec-desc-memory` and `#sec-resp-memory`; online and offline both resolve (`receipts/github-anchors-changed.txt`); fault probes in `receipts/probe-anchors.txt` |
| R288-1 F2 (MINOR; Docs, Tests): 09 §7 omits `params` | RESOLVED | same defect and same evidence as R289-1 F1; the row includes the "empty or unparseable inputs fail" clause that finding asked for |
| R288-1 S1 (link-gate slug), S2 (hidden diagram text; order not enforced), S3 (`DESC_NAME_ENTRIES_P` could link `KL_aecp_desc_store.sv:248-249`, where 1..1024 is enforced by `$error`), S4 (README paragraph placement) | RETAINED as SUGGESTIONS | S1 is the same as my S6. S2 and S4 are the same as my R289-1 S1 and S4. I confirmed S3 at this head. None of these files changed this round, except `integrator.md:83`, where only the fragment changed |
| R288-2 | no findings at MINOR or above; its suggestions are the R288-1 ones above | this is the other reviewer's round-2 comment on this head; it adds no new finding to resolve |
| R289-1 S1 to S5 | RETAINED as SUGGESTIONS | unchanged artifacts |

## Lens evidence

### Conformance: clean

**Assignment item 1: the owner links.**

- `github_anchor_check.py` checked the three changed files. It found 59 links with fragments and 0 dead, both offline and online at `9cde1c1` (`receipts/github-anchors-changed.txt`).
- Rows 80-83 and 88 resolve with `online=True`. So do the related cross-links at guide:157 and 07:174.
- Three controls are dead, as they should be: the two superseded round-1 slugs, and `#sec-resp-memory` looked up in a file that lacks it.
- GitHub's render of 07 contains `user-content-sec-resp-memory` at `9cde1c1` and not at `663d50d`.

**Assignment item 1: the anchor style.**

- The new `<a id="sec-resp-memory"></a>` sits on its own line, after a blank line, directly before the heading. This matches the existing `sec-desc-memory` style at `07_memory_maps.md:146`.
- GitHub still renders "3.3.2 The other main-memory region …" as an `h4` heading at head. The inline anchor did not absorb the heading.

**Assignment item 2: the 09 row.**

The row says the guide §2 table and diagram 21's `integration-parameters` group "each equal the overridable parameter set … no missing, extra or duplicate names; empty or unparseable inputs fail". The checker does each of these:

- rejects duplicates in each of the three inventories (`:106-108`);
- rejects names missing from, or extra to, the top's set (`:110-117`);
- rejects an empty inventory (`:104-105`);
- turns parse, OS and XML errors into failures (`:100-103`).

The row sits between `modmatrix` and `stale`, which is the prerequisite order in `Makefile:13`.

**Assignment item 3: "change nothing else".**

`receipts/delta-audit.txt` shows:

- The guide lines equal the base once the 07 fragments are normalised.
- 07 equals the base plus the one anchor line.
- 09 equals the base plus the one row.
- The content lines of the author's published `round2.patch` equal the real diff. Its sha256 also matches the author's manifest.

**Issue acceptance still holds.**

- The elaborator lists the same 24 GPARAMs as in R289-1 (`receipts/rtl-identity-elab.txt`).
- The checker reports `top 24, guide 24, diagram 24, OK` (`receipts/gates.txt`).

### RTL: clean

- These subtree ids are identical at `663d50d` and at `9cde1c1`: `hdl`, `tb`, `syn`, `scripts` and `.github`.
- The `protocol_processor_top.sv` blob is `cb81d642…`, the same as in R289-1.
- I re-elaborated the top with the pinned simulator, version 5.050. It gives the same 24 overridable parameters in the same order (`receipts/rtl-identity-elab.txt`). The wrapper sha256 `905795b9…` and the version string are in `receipts/tool-identity.txt`.
- This round changes no RTL, clocking, reset, CDC or interface.

### Robustness: clean

I ran fault probes on disposable exports of the head (`probe-anchors.sh`, `receipts/probe-anchors.txt`). Each row gives the return code of the repository link gate, then of the GitHub-faithful check:

| probe | link gate rc | GitHub-faithful rc |
|---|---|---|
| baseline | 0 | 0 |
| typo in the 3.3.2 fragment | 1 | 1 |
| new `sec-resp-memory` anchor deleted | 1 | 1 |
| existing `sec-desc-memory` anchor deleted | 1 | 1 |
| round-1 single-hyphen slugs restored | 0 | 1 |
| GitHub double-hyphen slugs | 1 | 0 |

- Every result matched its expectation.
- The explicit anchors are the only form of these links that both the gate and GitHub accept.
- If someone later removes or mistypes the new anchor, the CI link gate fails.

### Tests: clean (S6 recorded as a suggestion)

**My runs at this head** (`receipts/gates.txt`), all returning 0:

- `check-links.py`: 916 OK.
- `check-matrix.py`: 115 rows, 17 GAP findings, OK.
- `check-integrator-params.py`: 24/24/24, OK.
- `render-wavedrom.py --check`: 18 OK.
- `make stale`.
- `make check`: lint (41 mermaid and 18 wavedrom blocks), links, matrix, modmatrix (92 rows, 0 untested), params and stale.

**The link gate can fail:** the Robustness probes show it catching a broken or missing new anchor.

**Hosted runs at the exact head** (`receipts/hosted-runs.txt`, queried 2026-09-25T05:22:27Z). These are push run `36097408423` and pull_request run `36097411757`:

- `docs-gates` ran and succeeded in both, including the parameter step.
- `portability` ran and succeeded in both.
- `suites`: the lint-plus-suites step and the matrix step succeeded. The job was still in progress at the nvm-figures step.
- The Verilator build step was skipped because of a cache hit. That is a skipped step, not a failure.

**Author evidence consulted** (`review-evidence/pp99-r1/author-r2` at kebag-logic/milan-fpga `81a6fb3a`):

- `validation.json`, `make-check.log` and `github-anchors.log`;
- the sha256 of `round2.patch`.

### Docs: clean (S6 and S7 recorded as suggestions)

- **Examined at this head:**
  - `docs/architecture/09_verification.md:109-121`. The row wording is accurate; see Conformance.
  - `docs/architecture/07_memory_maps.md:134-230`.
  - `docs/guides/integrator.md:46-105,135-160`.
- **The live PR body** equals the author's published `PR-BODY.md`, apart from one trailing blank line. It keeps `Closes #99` and describes round 2, so a cold reviewer has enough to go on.
- R289-1 F1 is closed.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5827048744 items 1-3; `integrator.md:80-83,88`; `07_memory_maps.md:146,215`; `09_verification.md:120`; `check-integrator-params.py:91-128`; GitHub render of 07 at head and at `663d50d`; `receipts/github-anchors-changed.txt`, `delta-audit.txt`, `rtl-identity-elab.txt`; R289-1 ledger for the unchanged remainder | R289-2 (delta) + R289-1 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| RTL | CLEAN | subtree ids of `hdl`/`tb`/`syn`/`scripts`/`.github` at `663d50d` vs head; top blob `cb81d642`; pinned-simulator elaboration; `receipts/rtl-identity-elab.txt`, `tool-identity.txt`; R289-1 ledger | R289-2 (delta) + R289-1 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Robustness | CLEAN | 6 anchor fault probes on disposable exports; `receipts/probe-anchors.txt`; R289-1 checker probes (34 controls; the checker is unchanged) | R289-2 (delta) + R289-1 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Tests | CLEAN | `make check` and the docs-gates commands; hosted runs 36097408423 and 36097411757, jobs and steps; author-r2 evidence; `receipts/gates.txt`, `hosted-runs.txt`, `github-anchors-all.txt` | R289-2 (delta) + R289-1 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |
| Docs | CLEAN | `09_verification.md:109-121`; `07_memory_maps.md:134-230`; `integrator.md:46-105,135-160`; live PR body vs author-r2 `PR-BODY.md`; `receipts/delta-audit.txt` | R289-2 (delta) + R289-1 | 9cde1c19dbfd859257be8e012d4455856fcfce3b |

## Real limits

- **Not run:** the processor suite bank, HDL lint, yosys portability, the nvm figures, and any parent bank or build. The scope excluded all of them.
  - For these I rely on the manager's statement that the source static/builder and native banks passed at this head.
  - The public evidence tree I inspected at kebag-logic/milan-fpga `81a6fb3a` holds the author's round-2 gate logs. It does not hold a manager bank log for this head, so I did not independently locate that bank evidence.
- **The online anchor check** uses GitHub's contents API with the rendered-HTML media type at the exact SHA. I take that as equivalent to the rendering on the github.com page; it is not a browser test.
- **The GitHub-faithful checker's offline slug** follows GitHub's published rules. It matched GitHub's rendered ids on every link it checked (344 links in 56 files).
- **`suites` job:** in both hosted runs it was still in progress when I recorded them.
- **Parent consumer:** I did not assess a parent commit pinning `9cde1c1`. The R289-1 parent static gates ran against a pin of `663d50d`. This round changes only markdown, so no parent-consumed RTL or source list changed.
- **Physical calibration:** NOT RUN. Nothing here is hardware proof, and field skips are not hardware proof.
- **Source validation only:** this review validates the source head. The manager builds the final current-dev candidate at the merge turn (source base `008edbbf`, live dev `c533b481`), and I did not assess it.
- **Clone cleanup:** the gate run created an ignored `.venv-wavedrom/` in the clone. I removed it and re-verified the clone:
  - HEAD, tree, and index modes and blobs match;
  - the rehashed bytes of all 247 tracked files match;
  - there are no untracked or ignored files.

  The processor repository has no gitlinks and no `.gitmodules`.

## Pending manager duties

- Hosted and act acceptance at this head, including the `suites` jobs of runs 36097408423 and 36097411757.
- Build and validate the final current-dev candidate at the merge turn.
- Adopt the parent consumer pin at the final head and publish it.
- Decide whether S1 to S7 and the other reviewer's retained suggestions become follow-up issues. S6 in particular covers four links already dead on GitHub.
- The merge decision under the completion bar, with two independent positive reviews at the same exact head.

## Scripts and receipts

Paths are relative to the packet, and every file below is listed in MANIFEST.sha256.

**Scripts:**

- `github_anchor_check.py`
- `delta-audit.sh`
- `probe-anchors.sh`
- `run-doc-gates.sh`
- `elab-params.sh`
- `verify-clone.sh`

**Receipts:**

- `receipts/github-anchors-changed.txt`
- `receipts/github-anchors-all.txt`
- `receipts/delta-audit.txt`
- `receipts/probe-anchors.txt`
- `receipts/gates.txt`
- `receipts/rtl-identity-elab.txt`
- `receipts/tool-identity.txt`
- `receipts/hosted-runs.txt`
- `receipts/verify-clone.txt`
- `receipts/verdict-written-at.txt`

In the receipts, local absolute paths are redacted to `$PACKET`, `$CLONE` and `$PINNED`.

R289-2 FINISHED
