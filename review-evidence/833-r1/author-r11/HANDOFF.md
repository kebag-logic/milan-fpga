# #833 round 11 HANDOFF ([A726k])

Status: REVIEW READY, posted on #833 as issuecomment-6596102308 (`receipts/ready.md`, `ready-url.txt`). TAKEN: issue #833 issuecomment-6595166638 (`receipts/taken.md`, `taken-url.txt`).

Base: round 10 head `fce77f0e`. Head `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea`, 2 commits on top, one per item. Nothing pushed.

Sources:
- The manager's round 11 ruling: issue #833 issuecomment-6595078798. It is the authority for this round.
- R763-10 (PR #834 issuecomment-6595075381): NEGATIVE on MINOR F1; RESIDUE R1 and R2; R764-6-S1 retained.
- R764-10 (issuecomment-6595032567): POSITIVE; RESIDUE R1, R2 and R3; SUGGESTION S1.
- Both packets were copied with links dereferenced into scratch. Both `MANIFEST.sha256` check OK (`receipts/final/833-r76*-10.manifest-check.txt`).

`scripts/owned_process.py` is byte-identical to `fce77f0e` (and to `c1b29617`). No probe or mutant showed the product wrong.

## The findings, each with its change and control

TSC is `scripts/test_suite_cancellation.py`, PTS `scripts/process_test_support.py`, the guide `docs/testing/TESTING.md`. Line numbers are at the head.

| Finding | IDs | Change at the head | Control: words | Evidence |
|---|---|---|---|---|
| Row 3 claims a first-census parent whose live first-census child outlives its own `SIGKILL`, beside or under a shell never resumed; no listing had one | R763-10-F1; ruling item 1 | TSC:827-829: two listings after every other one, "a stubborn parent beside a stopped shell" and "... under a stopped shell". These are R763-10's `natural10.py` EXTRA words and its stated events: `SIGTERM` parent and child at 0; `SIGKILL` child at 2 and parent at 4; at 14 `SIGKILL` shell, parent and child; then the verdict. PTS:913-916: `first-census-parent-unspared-beside-shell`, R763-10's edit byte for byte. Guide:283 (the listings), row 3 (:316) | `owner_stated_seconds`: "a stubborn parent beside a stopped shell's" | `item1/`; `final/r763-10-natural10.log`: killed, red on `owner_stated_seconds` and the whole test, green on the other nine controls; `final/r763-10-per-listing.log`: red on its 2 listings of 48, no other |
| Guide and docstring said "grows after the first pass", wider than the rule | R763-10-R1 = R764-10-R2 | R763-10-R1's exact text, both places: guide:298, TSC:779 | | `item2/` |
| "The last cell" now pointed at the 1 s row | R764-10-R1 | Its exact text: guide:296 | | `item2/` |
| Sweep survivors outside every stated domain | R763-10-R2, R764-10-R3 | None asked; re-run below | | |
| `f"an early {words[2:]}"` assumes "a " | R764-10-S1, at judgement: not taken | Reason: TSC is at the 1000-line limit after item 1. Neither the assert nor the split fits on the existing line (126 columns). No growing listing's words start otherwise | | |
| Direct preflight under a SIGHUP-ignoring launcher | R764-6-S1, retained, not taken | As in rounds 7 to 10: outside #833 | | |

### Interpretations made public

- **The listings come after every other listing.** Placed beside "a stubborn parent", they pre-empt two existing mutants' first failure: `resume-with-one-live` and `parent-under-unresumed-shell-unspared` would print the new words, not their own. That run is `item1/placement-early-mutants.log`. Placed last, every round 10 entry keeps its words: `--mutants` PASS, 150 mutants, 147 with a control.
- **R763-10-R1 and R764-10-R2 give exact but different texts for the same two lines.** I took R763-10-R1's for both, so the guide and the docstring agree. R764-10-R2's docstring text needs a third docstring line (130 columns), and the module has no line left. R764-10-R2 is therefore taken through R763-10-R1, as round 10 took R764-9-S2 through R763-9-R1.
- **Words.** The listing words are `natural10.py`'s EXTRA words. The `MUTANTS` words are the failure's first words, "a stubborn parent beside a stopped shell's", so that the entry fits on four lines.

## Room under the module limit

Before the round, TSC had 999 lines and PTS 996. `check_py_idiom.py` counts a module over 1000 lines as "long module", with a budget of 10 and 10 measured. The `MUTANTS` entry takes 4 lines, so PTS is now at 1000. Written plainly, as `natural10.py`'s EXTRA, the listings take 6 lines in TSC. Only 1 was free.

What the listing needed, and nothing else:
- `stubborn` (TSC:791-793) names the stubborn parent's stated events, the same literal, and the new listings reuse them with the shell's `SIGKILL` at 14 s inserted. "a stubborn parent" keeps its 3 lines.
- Two listings are re-laid with no code change: "a stopped shell" (TSC:805-806) and "a live new descendant beside a stopped shell" (TSC:852-854).

`tools/layout_check.py` (`item1/layout-check.log`) checks this. Every round 10 `kept` call has an identical AST at the head. "a stubborn parent" has an identical literal, now named. With the new loop removed and the name inlined, the module's AST is identical to `fce77f0e`. No reviewer probe anchors on a re-laid line, and every probe below ran at the head unchanged. Final sizes: TSC 1000, PTS 1000; `long module: 10 <= 10`.

## Probes and sweeps at the head

Each probe ran unchanged from its manifest-checked packet copy, on a clean clone of the head (`$VALIDATION_STORAGE/833-a726k/wt-head`), with SIGHUP at its default (`SigIgn 0`, `final/*.sigign`). Receipts are in `receipts/final/`.

| Probe | Result | Receipt |
|---|---|---|
| R763-10 `natural10.py <head> <scratch> 7` | `none` equivalent: its listing, all ten controls and the whole test green. `first-census-parent-unspared-beside-shell` killed: red on `owner_stated_seconds` ("a stubborn parent beside a stopped shell's ...") and on the whole test, green on the other nine. `parent-unspared-beside-stopped-shell` killed | `r763-10-natural10.*` |
| R763-10 `per_listing.py`, every stated-seconds mutant and `none` | `none` 0 of 48; the new mutant red on its 2 listings only; `parent-under-unresumed-shell-unspared` red on 3 (the new under-shell listing too) | `r763-10-per-listing.*` |
| R763-10 `sweep.py`, 4224 mutants, 7 chunks, 10 jobs | 2716 equivalent; 1110 killed (R763-10's run: 1108); 398 survivors (400). Every survivor here survived in R763-10's run. The 2 now killed (`r7-shell-killed-in-resume-pass\|four\|none\|shell`, `r8-trap-no-window\|two-half\|any\|either`) were killed by `owner_shell_window`, whose real-process timing decides its resume's class. Host load 38 to 175 during the chunks | `sweep/sweep-r*-.*` |
| R763-10 `classify10.py` | The same 82 classes; the same 12 touch a listed cell, its own out-of-domain ones (6 `five-half`, 6 between listed passes). Class list identical to R763-10's `sweep-classified.txt` | `sweep/classified10.*` |
| R763-10 `probe_cells.py`, `table_check.py` | 65 of 65; no row lacks its control, no controlled mutant unnamed | `r763-10-probe-cells.*`, `r763-10-table-check.*` |
| R763-10 `natcheck.py`; R764-10 `byte_match_r9.py`; `tools/byte_f1.py` | round 9's natural mutants SAME / byte-identical; F1's edit SAME as `natural10.py`'s | `r763-10-natcheck.*`, `r764-10-byte-match-r9.*` (an empty manifest: the published `MANIFEST.json` is not in this clone, and the script only prints its entry), `a726k-byte-f1.*` |
| R763-10 `modcheck.py`, R764-10 `module_moves.py`, prev = round 9's head `e803d94b` | `BLOCKING` byte-identical; 143 entries unchanged and in order; 8 appended | `r763-10-modcheck.*`, `r764-10-module-moves.*`. First run with prev = round 10's head: `modcheck.py` stops at `KeyError: 'BLOCKING'` (it checks round 10's move): `*-prev-r10-head.*` |
| R764-10 `cell_sweep.py --jobs 8` | 99 mutants, 48 cells, `none` passes all. The same 25 red on none as at round 10 (`diff` empty): 24 survive every control and the whole test, 1 red on `owner_shell_window` and whole | `r764-10-cell-sweep.*` (its JSON in scratch) |
| R764-10 `whole_rerun.py` | head PASS; 24 of 25 PASS; `B-trap-command-unspared/live/shell/R7-interior-past` red, as at round 10 | `r764-10-whole-rerun.*` |
| R764-10 `cell_sweep.py --author` | 150 of 150 entries mapped on 48 listings; 23 red on none, each with another control or none | `r764-10-author-cellmap.*`, `author-cellmap-none-controls.txt` |
| R763-10 `stress_owner_report.py <head> 3000 8` | 0 red of 3000, load 62 to 134 | `r763-10-stress-head.*` |
| R764-10 `repeat_control.sh <head> owner_report 8 375` | 0 red of 3000, mean load 49.4 | `r764-10-repeat-head.*` |
| `--matrix`, 4 parts, 10 jobs | 1694 runs, each part PASS; `tools/tabulate.py`: problems none (`none` green on all 11; each of 147 red on its control with its words and on whole; 3 with no control green on all 11) | `matrix-part*.*`, `matrix-table.md` |

No survivor is new, and none is inside a stated domain. The round 10 classifications (R763-10-R2, R764-10-R3) stand.

## Cost

`final/inproc-cost.txt`, `final/cost.txt`: round 10's head against this one, interleaved, beside the docs.yml jobs, host load 36 to 71.
- `owner_stated_seconds` in one process, 20 calls a tree, 3 times: median 51.6 to 52.3 ms at round 10, 53.2 to 53.9 ms here.
- As its own process: 0.16 s at both. Every other control is within 0.05 s.
- The whole test, 4 runs each, 8 at once: mean 60.6 s at round 10, 60.7 s here.

**Round 11 adds about 2 ms to the preflight**, well under the 1 s allowed.

## Gates

All at head `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea`, one log and rc each, never piped. The lane gates ran on a fresh clean clone (`receipts/gates/lane.sh`, round 10's with this head and this scratch). `tree-after.txt` is empty with `--ignored`. SIGHUP was at its default in every launcher: `SigIgn 0` for the lane gates, item checks, campaigns and probes.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's runner and verifier. Only the venv and HOME paths point at this round's scratch (`gates/runner-vs-round10.diff`); `not_run.json` is round 1's, unchanged. Fresh venv, identical to round 8's freeze (`gates/venv-freeze-new.txt` = `requirements-round8.txt`), fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job (`docsyml/*__tree-after.txt`; the no-git job has no `.git` to check). Builder legs: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. Jobs 05:27 to 06:17, in the background, polled. The launcher's `SigIgn` is `0x4` (SIGQUIT only), as in rounds 7 to 10 (`gates/sigign-docsyml.txt`); SIGHUP at its default | `gates/docsyml-*`, `gates/docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants --jobs 4` | 0 | `owned-process mutants: PASS (150 mutants, 147 with a control that must fail)` | `gates/lane/mutants.*` |
| `--matrix`, 4 parts | 0 each | 1694 runs, problems none | `final/matrix-*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`; sha256 and size in `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py` (`long module: 10 <= 10`), `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` | 0 each | before each commit (also inside docs.yml) | `item*/quick/` |
| Full sweep | not run | Round 11 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

Before each commit (`receipts/item1/`, `item2/`): quick gates, table check, per listing at `none` (48 listings, none missed), and `--mutants`: PASS at 150/147 both times. Item 1 also has `layout-check.*`, `per-listing-all.log` and the placement experiment (`placement-*`).

## Incidents, no harm

- **Memory:** the unit's peak was 14.9 GB, over the 12 GB asked. Anonymous memory stayed under 0.7 GB. The rest was page cache (up to 7.8 GB) and slab (3.4 GB), while docs.yml's builder clones, both sweeps and the matrix ran at once. Once found, the finished sweep trees, experiment trees and the lane-gate clone were deleted, which brought the unit to 10.6 GB. The remainder was docs.yml's running clones.
- Host load reached about 175 during R763-10's sweep chunks r4 to r6, from the docs.yml builder legs beside other work on the host. The only effect seen is that two `owner_shell_window`-timed survivors were killed, which is in the conservative direction.
- One experiment ran on two scratch exports (`wt-a`, `wt-b`), never in the lane: the listings placed early and placed last, before item 1 was written. Its logs are kept in `item1/placement-*`.
- Every run set `TMPDIR` to scratch. Nothing was signalled by name.
- Nothing was pushed; no PR or issue text was edited.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `7b3b7e6f` | 1 | List a stubborn parent from the first census beside a stopped shell never resumed, and under it, ... (full subject in `git log`) |
| `5843d1af` | 2 | Say that a listing whose census has grown by the second pass is kept again early, ... |
