[A775] REVIEW READY — round 11, head `16ba667d` (local, not pushed)

Commit: `16ba667d` (`895-talker-redeclare` on the PR's `1215bd82`, one commit, markdown only; the manager pushes). It answers R835-5 (PR #901 issuecomment-6901818182, NEGATIVE on one MINOR) and R836-5's residue (issuecomment-6901691558, POSITIVE). R835-6 is the one delta reviewer.

**For the merge candidate of `1215bd82`:** only markdown changed after `1215bd82`: `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md` and `sw/firmware/ctrl/plat/README.md`. No image input and no non-markdown path changed, so its native bank carries.

**R835-5-F1 (MINOR):** each listed statement now gives this head's figure, or names the image it describes by short commit.
- `plat/README.md:110`: 680 B of `rom` past 60.0 at this head. Round 6's 392 B and 1,656 B are bound to `bf0844f1`.
- `FR_NFR.md:383`: the 950 us slice and its 8 ms pace (txL 48.43, last 127.21, ACMP 28.95) are bound to #894's head `07ed787e`, in the past tense. The composition's 9 ms pace is bound to round 7B's merge `7e3db6b9`.
- `SPLIT_CONTROL_MEMORY.md`:
  - `:2603`: 245 / 220 us are bound to `bf0844f1`. This head's are 255 us (the dearest edit), 300 (paced) and 225 (ordinary).
  - `:2605`: 33.69 and 94.99 are bound to round 7A's `4c9757ee`. This head's are 34.00 and 104.25.
  - `:2606`: 1,656 is bound to `bf0844f1`. This head's is 1,368.
- **The sweep R835-5-S2 describes** (every "at this head", "at the head", "this head's" and "now" in section 13's marked subsections, FR_NFR 3.4.1 and the READMEs this PR touches) found three more, each fixed:
  - `:2595` "950 us now" (now "on #894's head");
  - `:2604` "now 9 ms" (now round 5's `62298ab5`, and 9 at this head);
  - `:2618` "at this head" in round 6's subsection (now `bf0844f1`).
- **The verification:**
  - The review's `scripts/f1_sites.py` reports **0 of 7 present**.
  - The corrected inventory (`receipts/docs/superseded-inventory.md`) holds the phrase sweep and the figure sweep. R835-5's missed figures are added: 392 B, 245, 220, 33.69, 94.99, 1,656 and 1,864. All 201 figure hits are classed, and none gives a superseded figure as this head's.
  - README lines this PR did not write, which predate the source base `cec88385`, are listed as `dev-soft-core`'s.

**Residues and suggestions:**
- **R835-5-RS1**, exactly: "held 124,876 B" (`:515`).
- **R835-5-RS2**, exactly: "its bound at 1x1/1if was, on #894's head," (`:2529`).
- **R836-5-RS1:** the roles link each review's start and verdict, with no "(next)" left.
- **R835-5-S2:** taken.
- **R835-5-S1 and R835-4-S3:** retained.

**Validation** at `16ba667d`, each on its own fresh clean clone:
- **docs.yml:** every job failed 0. `verify_wf.py`: 61 steps ran, 34 not run with a reason, 0 bad.
- **firmware-unit:** failed 0, its 6 steps rc 0. `fw_coverage.py --check` passes (39 files).
- **Whitespace and checks:** `git diff --check` against the source base and the merged #902 head, the idiom ratchets, `docs_check.py` (0 findings), `check_doc_style.py`, `check_doc_paths.py`, `check_gptp_docs.py` and `check_em_dash.py`: all rc 0.

**Not run:** act and the hosted exact-head contexts, which follow the push. Rows, images and firmware are unchanged since `1215bd82`.

Receipts: round 11's packet, with `INDEX.md`: the inventory, `f1-sites.txt` and the gates. Nothing was pushed.
