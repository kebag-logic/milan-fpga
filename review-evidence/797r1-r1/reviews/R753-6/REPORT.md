[R753] POSITIVE - exact head 2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2

Round R753-6 is the internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1). It covers head `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2`, tree `eb629ae988ba3f1e9ef2a15969d39cd5216f76a8`. The round 6 delta is `ef7dc985..2c500d0a`: one commit, one file, `scripts/register_read_sweep.py`, +21/-11. The delta touches no `docs/`, `hdl/`, `scripts/register_descriptions.json`, `configs/`, `sw/`, `syn/` or gitlink path. The source base is `1e80128f`. Live dev `503bc97c` is not merged.

**Why POSITIVE:** R753-5 F1 and R754-5 F1 (the same defect) are resolved at their cause, and every verification item they set passes on my own runs. No BLOCKER, MAJOR or MINOR is open at this head. Two SUGGESTIONs are recorded and there is no new RESIDUE. The three residue items carried from round 3 are retained as they were.

## Round 6 delta, checked against the round 5 finding

**What the delta does** (`scripts/register_read_sweep.py`):

- `:342`: the SRP mode loop bound goes from 8 to 9.
- `:361-362`: new state 6. It answers a poll (`answer_srp()`), then writes `STRMW_CTRL` (`wr(0x810, ...)`) and records `srpw = o_srp_ctx_we`. The write is not answered before the reads.
- `:363-364`: the steal states move from 6 and 7 to 7 and 8. State 8 still runs last.
- `:350-359`: the harness comment lists all nine states. It says why state 8 must stay last: the carried-in state 0 is the only state that reads a poll answered before a `STRM_SEL` write.
- `:17-26`: the docstring now lists the orders the states drive. It replaces "in either order around the write", which round 5 found untrue.

**The record reads the new state as the page words it.** In state 6, `at_ans` (the poll grant) comes before `at_selwr` (the `0x810` handshake, `:252-253`). So at `:378`, `srppoll` is 0, `srpsince` is 0 and `srpsteal` is 0. The page clause "latest answer to the window was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write" (`docs/reference/REGISTER_MAP.md:3462`, `:3483`, `:3639`, `:3640`) is false, so the "any other case" row applies.

The RTL clears `srp_fresh_r` on `srp_prov_w` at `hdl/common/csr/milan_csr.sv:3128`. The pending write stays unanswered, so `srp_fresh_r` stays 0 through the reads.

**The pending write is drained at the end of each pass** (`:401`). That drain already existed for state 5. Because of it, no unanswered write carries into the next pass's selection.

**My runs.** Every sweep used Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, `Verilator 5.050 2026-07-01 rev v5.050`). The sweep script came from the head tree, run on disposable `git archive` copies. The script is `run_r753_6.sh` and the summary is `receipts/probe_summary.txt`.

| Run | What it is | rc | Disagreements (ship / 2x2) | Reads per build |
|---|---|---:|---|---:|
| head | exact head | 0 | 0 / 0 | 54,007 |
| m4 | `:3128` provisioning clear removed | **1** | 24 / 120 | 54,007 |
| m1 | `:3132` steal clear removed | 1 | 24 / 120 | 54,007 |
| m2 | `:3115` write-answer clear set to 1 | 1 | 48 / 240 | 54,007 |
| m5 | `:3119` `STRM_SEL` clear removed | 1 | 12 / 84 | 54,007 |
| round4 | head sweep against the `79fdea05` page (round 4 wording) | 1 | 48 / 240 | 54,007 |
| m4parent | m4 RTL against the **parent** (`ef7dc985`) sweep script | **0** | 0 / 0 | 48,007 |

- **The delta is what catches m4.** The parent sweep passes m4 at rc 0, which reproduces the round 5 gap. The head sweep fails it at rc 1.
  - The extra 6,000 reads per build are state 6: 240 passes × 25 words.
  - Every one of the 144 m4 disagreements has the state-6 signature `srp=1 srpw=1 srppoll=0 srpsteal=0 srpsince=0` (`receipts/disagree_by_state.txt`). By build and word: ship `STRMW_SRP` 24; 2x2 `STRMW_SRP` 72, `STRMW_SID_LO` 24 and `STRMW_SID_HI` 24.
  - States 2 and 3 share that signature, but they answer the write, and the write answer clears the word whether or not m4 is applied. Only state 6 can show m4.
- **The other mutants and the old wording still exit 1.** m5 is still caught in the carried-in state 0 (`srp=0 srpw=0`), as the comment at `:356-357` says.
- **My logs are byte-identical to the author's.** All six of my head, m1, m2, m4, m5 and round4 logs have the same sha256 as `author-r6/receipts/sweeps/*.log`. The sha256 values are listed in `MANIFEST.json` at `f4a3fb86` (`published_sha256`). The author's delta receipt `lane/delta_ef7dc985_2c500d0a.diff` is byte-identical to my `git diff ef7dc985 2c500d0a`.
- **The provenance of the mutants and the round 4 page:**
  - The mutant patches are the author's `author-r6/receipts/patches/m*.rtl.diff`, copied to `receipts/inputs/`. They are the same four clears round 5 named.
  - The round 4 page I built from `receipts/inputs/round4_wording.page.diff` is byte-identical to `git show 79fdea05:docs/reference/REGISTER_MAP.md`.
- **The author's first attempt, disclosed and checked.** `author-r6/receipts/sweeps_first_attempt/sweep_m5.rc` is 0. The author's REVIEW READY note explains it: the new state was first appended last, and its write drain cleared the word before state 0's read, which hid m5. The published head orders the states differently, and m5 exits 1 on my run. That receipt is a superseded local attempt, not evidence about this head.

## Findings

### Prior findings at this head

| Finding | Status at 2c500d0a | Evidence |
|---|---|---|
| R753-5 F1 / R754-5 F1 (MINOR, Tests): no state separates the `STRMW_CTRL`-write clear | **Resolved** at its cause | State 6 at `:361-362`. Docstring `:17-26` states the driven orders. Head rc 0 on both builds. m4 rc 1 (144) where the parent script gives rc 0. m1, m2 and m5 rc 1. The round 4 wording rc 1. |
| R753-5 S1 (SUGGESTION, Docs, Robustness): "since" has no stated anchor | Retained, not taken. Optional. | Page rows and `register_descriptions.json` are unchanged in the delta. |
| R754-4 S1, S2 (SUGGESTION) | Retained, not taken. Optional. | The delta does not touch `register_sv.py`. The sweep's `SHAPE_INCLUDE` (now at `:62-63`) still maps the 2x2 build to `configs/generated/endstation_arty_4x4`, and the delta does not touch it. |
| R753-3 RES2 | Retained, residue checklist | `docs/reference/REGISTER_MAP.md:4503` is unchanged. |
| R753-3 RES3 | Retained, residue checklist | `docs/design/CSR_REGISTER_NOTES.md:974` is unchanged. |
| R754-3 R1 | Retained, residue checklist | `docs/design/CSR_REGISTER_NOTES.md:78` is unchanged. |

I made every run above, and reached this round's verdict on the delta, before I read the round 5 reports (`receipts/order_of_work.txt`). Reading them changed nothing.

### S1 - SUGGESTION - Tests, Robustness - `scripts/register_read_sweep.py:342`, `:356-357`, `:401` - the `STRM_SEL`-write clear is caught only by loop order

- **Evidence:**
  - m5 (`milan_csr.sv:3119` removed) is caught only in the first state-0 pass after state 8. That pass reads after a `STRM_SEL` write that follows state 8's poll answer.
  - Any reorder that puts a state with a drained write last hides it, because the `:401` drain answers the write and clears the word first. The author's first attempt proves this: `sweeps_first_attempt/sweep_m5.rc` is 0.
  - The comment at `:356-357` now states the dependency, and m5 exits 1 at the head. So this is not a defect today.
  - The author lists the same point as an open risk in REVIEW READY.
- **Optional change:** add a dedicated state: a poll answered, then the same `STRM_SEL` value written again, then the reads. The clear would then no longer depend on loop order.

### S2 - SUGGESTION - Docs - `scripts/register_read_sweep.py:20-23`, `:352-353` - "a provisioning write" also names selections where the write does not provision

- **Evidence:** in states 2, 3 and 6, the `0x810` write also runs at selections where `srp_prov_w` (`milan_csr.sv:3091-3093`) is 0. Those are out-of-range selections and talker index 0, so `srpw` is 0 there.
  - Those selections never answer a poll, so no read value depends on the gap.
  - The harness comment already says "a STRMW_CTRL write". The docstring says "a provisioning write".
- **Optional change:** in the docstring, write "a `STRMW_CTRL` write (provisioning where the selection has an SRP row)", or match the comment's words.

### Residue

None new.

- The added lines of the delta (`receipts/delta_ef7dc985_2c500d0a.diff`) contain no non-ASCII character.
- They carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. The new comments state behaviour.
- The commit message is one line with no trailer.

## Lens results (each lens applied at 2c500d0a)

```text
[R753] PASS Conformance - docs/reference/REGISTER_MAP.md:3462,:3483,:3639,:3640 against hdl/common/csr/milan_csr.sv:3105-3141 - page, descriptions and RTL unchanged in ef7dc985..2c500d0a (git diff --quiet); the printed SRP-served clause predicts every head read in the new state 6 and the eight prior states (receipts/sweeps/sweep_head.log: 0 of 54,007 per build), including a poll answered before an unanswered provisioning write, where the page's "after the last STRMW_CTRL write" gives the any-other-case 0
[R753] PASS RTL - hdl/common/csr/milan_csr.sv:3091-3093,:3112-3132 - no RTL in the delta; the sweep now exercises the srp_prov_w clear at :3128 at block level, and each of the four non-reset clears of srp_fresh_r is shown necessary by an rc 1 mutant (m1, m2, m4, m5)
[R753] PASS Robustness - scripts/register_read_sweep.py:361-364,:401 - new state 6 posts the write and leaves it unanswered, the :401 drain answers it before the next pass's selection, the snapshot write of the same pass does not touch the SRP master, the non-provisioning selections in state 6 read 0 at the head (0 disagreements), and loop-order dependence of the STRM_SEL-clear detection is stated at :356-357 (S1 optional)
[R753] PASS Tests - receipts/sweeps/sweep_{head,m1,m2,m4,m5,round4,m4parent}.{log,rc} - head rc 0 both builds; m4 rc 1 at head and rc 0 at the parent script, so the new state is what detects it; all 144 m4 disagreements carry the state-6 signature (receipts/disagree_by_state.txt); m1, m2, m5 and the round 4 wording rc 1; logs byte-identical to author-r6 receipts
[R753] PASS Docs - scripts/register_read_sweep.py:17-26,:350-359 - docstring and harness comment list the nine orders actually driven (checked line by line against :361-371), state why 8 runs last, and replace the round 5 untrue "either order around the write"; no page or notes change was required by the delta; S2 optional wording
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REGISTER_MAP.md:3462`, `:3483`, `:3639-3640`; `milan_csr.sv:3105-3141`; `receipts/sweeps/sweep_head.log`; nothing in this lens's scope changed in the delta | R753-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| RTL | CLEAN | `milan_csr.sv:3091-3093`, `:3112-3132`; mutant runs m1, m2, m4 and m5; no RTL in the delta | R753-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Robustness | CLEAN (S1 optional) | `register_read_sweep.py:342`, `:361-364`, `:378`, `:401`; `receipts/disagree_by_state.txt` | R753-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Tests | CLEAN (S1 optional) | `receipts/sweeps/*.log`, `*.rc` (7 runs); author-r6 sweep receipts, matched by sha256 | R753-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Docs | CLEAN (S2 optional) | `register_read_sweep.py:17-26`, `:350-359`; commit message; delta added lines | R753-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |

## Real limits

- **Block level only.** The sweep elaborates `milan_csr` alone. The shipping datapath ties the SRP grant and the steal input to 0. So states 1 to 8 are block-level contract evidence, not evidence about the integrated behaviour.
- **What I did not run:** the Verilator suites, Yosys, the behave suite, the docs gate workflow, `gen_register_reference.py --check`/`--selftest`, any parent/PP/gPTP bank, act or hosted CI, Vivado, hardware or physical calibration.
  - For the generator and docs gates I rely on the author's published receipts at `f4a3fb86`. The delta does not touch the generator's inputs or outputs, and no gate invokes the sweep. I grepped `.github/`, `scripts/*.py` and the Makefiles for any reference to the sweep and found none.
- **The evidence commit is unsigned.** GitHub reports `f4a3fb86` as `verified=false`, reason `unsigned`. I trusted the receipts only where I reproduced them: six sweep logs were byte-identical, and so was the delta diff.
- **No manager source bank runs at this head, and I claim none.** This review is source-head validation. It is not the current-dev merge candidate (source base `1e80128f`, live dev `503bc97cd4f24ad07596c17e7188f2024617972d`).
- **Hosted checks were still in progress at 2026-11-02T13:17:05+01:00** (`receipts/hosted_checks_snapshot.txt`). `docs-check-no-git` and `wire-accountability` had succeeded. `docs-gates-0..2`, `elaborate-gates-0..1` and the fail-fast contexts were still running. I draw no conclusion from them.
- **The clone is unchanged.** At the end, HEAD, the tree, `git write-tree`, the index and the worktree all match `2c500d0a`. The sweep blob is `5fc7b9e5`, mode 100644. All six gitlinks are as recorded (`receipts/clone_integrity.txt`). A `scripts/__pycache__` that my compile check created was removed, and `git status --ignored` is empty.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (builder and native banks) against live dev `503bc97c`, with its receipts linked on the PR.
- The residue checklist: R753-3 RES2 and RES3, and R754-3 R1. Also the optional suggestions: R753-5 S1, R754-4 S1 and S2, and this round's S1 and S2.
- The external review at this head.
- Maintainer merge authorization.

R753-6 FINISHED
