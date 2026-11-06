[R769] POSITIVE - exact head 6162885ffee5d8e8897732be6479982b8dceaec9

# Internal independent review R769-4: processor PR #213 (issue #212), round 4

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #213, branch `212-srp-presettle-talker`.
- Exact head `6162885ffee5d8e8897732be6479982b8dceaec9`, tree `16b9d3fa90901d34a1225ae6821b693218431061`. Its parent `834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1` is the round-3 head; both round-3 reviews of it were POSITIVE.
- Source base `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Live parent dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- Scope of this round: the delta `834cc88..6162885`. It is one commit that splits three declarations which the parent's `scripts/check_cpp_idiom.py` refused under Rule 11. Code the delta does not touch keeps its round-3 lens verdict. Nothing in the delta changes what that code depends on.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are clean.

- One new RESIDUE (R1): wording in the PR body's Round 4 paragraph.
- Two round-3 RESIDUEs are carried open (R770-3 R1 and R2). They are wording only and go to the residue checklist.
- One SUGGESTION (S1).

The delta does what the assignment asks:

- **Behaviour-identical.** Types, initialisers and widths are unchanged.
- **No other line changed.**
- **Both suites keep their full counts:** pp_top 11,064 and srp_stream_fsms 1,512, equal to round 3 shard by shard.
- **The parent checker passes.** With this head as the protocol-processor gitlink, `check_cpp_idiom.py` returns rc 0 with `multi-declarator declaration: 0 <= 0`. With `834cc88` it still refuses with "3 > ratchet 0" at the same three sites.

## The delta, line by line (Conformance, RTL, Tests)

`git diff --raw 834cc88 6162885` shows two files, both modes `100644` → `100644`, 7 insertions and 4 deletions, and no mode or rename entry. `git diff --check` returns rc 0 (`receipts/delta.txt`).

| Site | Before | After | Why it is identical |
|---|---|---|---|
| `tb/pp_top/sim_main.cpp:10619-10620` (`listener_is`) | `int e = -1, q = -1;` | `int e = -1;` / `int q = -1;` | Both are still `int` with initialiser `-1`. Both still bind to `listener_value(..., int& ev, int& fp)` (`:10584-10585`), and the `&&` chain is unchanged. |
| `tb/pp_top/sim_main.cpp:10625-10626` (`listener_any`) | same | same split | same |
| `tb/srp_stream_fsms/sim_main.cpp:2895-2896, 2899` (PS12) | `const int sinks[] = {0, 3};` … `l_decl(sinks[0])`, `l_decl(sinks[1])` | `const int sink_a = 0;` `const int sink_b = 3;` … `l_decl(sink_a)`, `l_decl(sink_b)` | The element type was `const int` and the values were 0 and 3. Now they are two `const int`s with 0 and 3. `l_decl(int s)` (`:325`) takes them by value, so the arguments are the same. |

- **No other code changed.** Neither does any HDL, doc, README, Makefile or campaign file (`git diff --quiet 834cc88 6162885 -- docs hdl tb/srp_top tb/*/README.md` holds).
- **Comment rule.** The delta adds no source comments, so it adds no lane label, round, reviewer ID or comment ID.
- **No new warnings.** None of the builds at either head prints a compiler `warning:` (`-Wall -Wextra`).
- **All three sites were added by this PR.** `git diff a9e84b6 834cc88` adds both `int e = -1, q = -1;` lines and `const int sinks[] = {0, 3};`.

## Executed evidence (reviewer runs, this packet)

The toolchain is Verilator 5.050 at the scoped path, identity checked: wrapper sha256 `905795b9…e92f`, `--version` "Verilator 5.050 2026-07-01 rev v5.050" (`receipts/verilator-identity.txt`). All runs used disposable clones under `scratch/`.

### Parent checker

`scripts/run_idiom.sh` runs the parent's checker at dev `cc204c6`, with `gptp-processor` at its pin `135afd0` and the protocol-processor gitlink staged at each pin. Each pin's `git submodule status` shows a leading space (on-pin).

| Pin | Result |
|---|---|
| `6162885` | rc 0. 351 translation units (165 C). Every refused rule is 0 and every ratchet is `0 <= 0`, including `multi-declarator declaration: 0 <= 0`. `--list` has no per-file row. `--selftest` passes 75 of 75. |
| `834cc88` | rc 1: "multi-declarator declaration 3 > ratchet 0". `--list` names `tb/pp_top/sim_main.cpp=2` and `tb/srp_stream_fsms/sim_main.cpp=1`. |
| `a9e84b6` (base) | rc 0, every rule 0. |

The tool's sha256 values are in `receipts/idiom-tool.sha256`. `check_cpp_idiom.py` is byte-identical at evidence commit `c566121` and at dev `cc204c6` (`a059f01c…f228`).

### Suites

**`tb/srp_stream_fsms` (`make run`):** 1512 checks, 1512 PASS, 0 FAIL at both `6162885` and `834cc88`. The two logs are identical once clone paths are normalised.

**`tb/pp_top`:** the default build's single simulation runs longer than one bounded foreground call allows. My `make run` attempts were cut at 570 s (rc 124 from my own `timeout`, `receipts/pp_top-*.fullrun-bounded.*`). That is not a suite failure. I reproduced the recipe in stages instead (`scripts/pp_top_staged.sh`; the build steps come from `make -n run` without the simulations):

- **Seven builds** at each head, all rc 0.
- **Six single-section builds**, identical at both heads: fixture 20, identify 178, line 292, timebase 56, defaults 3, interfaces 6. Total 555.
- **The default build as 19 shards**, run through its own `--<section>-only` flags (`main`, `sim_main.cpp:16256-16300`). Every shard is rc 0 with 0 failures, and the per-shard tallies are identical at both heads (`receipts/shards-6162885.txt` == `receipts/shards-834cc88.txt`). They sum to 11,243.
- **Reconciling the count.** The `--aecp-dispatch-only` shard also runs the dispatch focus "A5b+M9+V: 734 checks", which the default build does not. The default build's sections therefore sum to 10,509, which equals the author's receipt "[build default …] 10509 checks". The total is 10,509 + 555 = **11,064** (`receipts/pp_top-reconstruction.txt`).
- **Where the delta runs.** The `--acmp-only` shard runs `run_acmp` → `AcmpPathPhase` (`:12003`), which holds every caller of the split helpers (AS7, AS8, AS9: `:10561-10748`). It reports 62 checks, 0 failures at both heads, and its logs are identical.

### Falsification probes

`scripts/probes.sh` edits one line per probe in a disposable clone, then restores it.

- **M1** inverts `q == fp` in `listener_is`. The ACMP shard then gives 62 checks with 4 failures, all named AS7, AS8 or AS9. So the split `q` still feeds those rows.
- **M2** sets `sink_b = 2`. srp_stream_fsms then gives 1512 checks, 1511 PASS, 1 FAIL, and the failure is named "PS12: both register at the settle…". So the renamed constant still carries sink 3 into the check.
- **Restore.** After the probes the clone's `git status --porcelain` is empty (`receipts/probe-restore.status`).

## Published author evidence checked

- **Round-4 packet.** It is at `kebag-logic/milan-fpga` commit `d7250b05a10850d8d71ddf67fc2b5d3cba324e26`, branch `pp212-review-evidence`, under `review-evidence/pp212-r1/author-r4/`.
  - All 68 files match their `published_sha256` in `MANIFEST.json`, and none is unlisted (`receipts/author-r4-manifest-verify.txt`).
  - One row is path-redacted (`receipts/tools/gate.sh`).
  - The commit carries no signature object. Its integrity rests on the manifest digests.
- **Receipts spot-checked:**
  - `pp_top` rc 0, "11064 checks: 11064 PASS, 0 FAIL";
  - `srp_stream_fsms` rc 0, "1512 checks: 1512 PASS, 0 FAIL";
  - `check_cpp_idiom` at pin 6162885 rc 0;
  - the 834cc88 repro list shows the same 2 + 1 sites;
  - `git_diff_check` rc 0.
  - `round4.diff` has the same sha256 as my own `git diff 834cc88 6162885` (`85c571f2…be3f`).
- **The round-1 to round-3 tree** at `c5661216` was not re-examined for this delta. It keeps its round-3 standing.
- **Hosted, at the exact head.** These are hosted jobs, not a manager source bank. The workflow `hdl` ran twice (push 42163103420, pull_request 42163108720):
  - `docs-gates`: success in both runs;
  - `portability`: success in both runs;
  - `suites`: **in_progress** in both runs when I recorded them (2026-11-06 05:14 UTC, `receipts/hosted-check-runs.tsv`).
  - I make no claim about the hosted suites' result. The manager owns hosted/act acceptance.

## Findings

### R1 — RESIDUE — Docs (PR body)

**The PR body calls the PS12 array a multi-declarator declaration.**

- **Where:** PR body, "## Round 4", first paragraph. The text is "refused three multi-declarator declarations this PR added … Round 4 splits each into one declarator per statement".
- **Evidence:** `const int sinks[] = {0, 3};` has one declarator, an array with a braced initialiser. The checker counts it because its line pattern `MULTI_DECL_RE` (`check_cpp_idiom.py:269-270`) matches any comma before the `;` outside parentheses, and that includes the comma inside the braces. So there was nothing to "split into one declarator". The array was replaced by two named constants, which the same paragraph's next sentence says correctly.
- **Impact:** wording only. The figures, receipts, code, test counts and checker verdict are all unchanged. The commit subject's "Declare one variable per statement … the PS12 sink pair" has the same imprecision. History is immutable, so no change is asked for there.
- **Exact fix:** replace "refused three multi-declarator declarations this PR added (Rule 11 of the parent's code-quality guide). Round 4 splits each into one declarator per statement and changes nothing else:" with "refused three declarations this PR added under its multi-declarator rule (Rule 11 of the parent's code-quality guide): two real multi-declarators and one braced array initialiser, whose comma the rule's line pattern also counts. Round 4 rewrites each and changes nothing else:".
- **Verification:** the PR body text. No run is needed.

### S1 — SUGGESTION — Tests

**PS12 uses the new name in one place and the literal 3 in others.**

- **Where:** `tb/srp_stream_fsms/sim_main.cpp:2892-2899`. `sink_b = 3` is used in `h.l_decl(sink_b)`, while `h.ctl(true, 3, …)` and `h.l_app(3)` in the same row keep the literal 3.
- **Suggested outcome:** use `sink_b` (and `sink_a`) throughout PS12, or name them for their role, for example `joiner = 0` and `rider = 3`, as the message text does ("one applicant (sink 0) … the rider").
- **Why only a suggestion:** it is readability only, and there is no behaviour difference (probe M2).
- **Parent checker (outside this repository):** `MULTI_DECL_RE` counts a braced initialiser list such as `{0, 3}` as a multi-declarator. That is a false positive. The rule could exclude a comma inside `{…}`, which would let a constant array stay an array. This is a note for the parent's owners.

## Prior public review findings at this head

I read these after my own pass.

| Finding | Status at `6162885` | Evidence |
|---|---|---|
| R769-1 F1/R1/S1-S3; R770-1 F1-F5; R769-2 F1 = R770-2 F1; R769-2 R1, R2 = R770-2 R1; R769-2 S1; R770-2 S1, S2 | stay **RESOLVED** / taken | The delta touches no HDL, doc, README or campaign file. Every row they depend on still passes at full count: srp_stream_fsms 1,512, including PS16 to PS24; pp_top 11,064, including AS7 to AS9. |
| R770-3 R1 (RESIDUE): `tb/srp_top/README.md:901` "(the exception before this row)" | **OPEN, carried** (wording) | Unchanged at `:901`. The exact fix stays R770-3's: "(the settled-sink exception the listener had before PS24)". |
| R770-3 R2 (RESIDUE): PR body "(README cells re-recorded)" for eight arms | **OPEN, carried** (wording) | Still in the Validation paragraph. The exact fix stays R770-3's: "(the seven README cells that record a count re-recorded; the issue #188 table, which holds `listener-reprobe-abandons-leave`, records none)". |
| R769-3 S1-S4, R770-3 S1-S4 (SUGGESTIONs) | not taken in round 4; **retained** as suggestions | Round 4 was scoped to the Rule 11 split. None of them is affected by it. |
| R769-2 S2 / R769-3 S4 (`msrp_fail_bridge_o` note) | retained as a note | RTL unchanged. |

## Lens evidence

- **Conformance — CLEAN.** The delta is test-bench C++ only, with no HDL, register, interface or clause text. The requirement rows that grade the Milan v1.2 §5.3.8.5 / IEEE 802.1Q-2022 §10.7 behaviour still pass unchanged: PS12 in srp_stream_fsms, AS7 to AS9 in pp_top. The parent's Rule 11 gate now passes, and it refuses the round-3 pin as before.
- **RTL — CLEAN.** No `hdl/` byte changed (`git diff --quiet 834cc88 6162885 -- hdl`). The seven pp_top builds and the srp_stream_fsms build elaborate the same RTL at both heads. The round-3 lint and area verdicts stand, and the manager's round-3 parent route (`834cc88`) holds for this head because the RTL is identical.
- **Robustness — CLEAN.** The test-bench semantics are unchanged: the initialisers, the by-reference binding and the by-value sink indices are the same. Probes M1 and M2 show that the split names still feed their checks, so the refactor did not silently disconnect an assertion.
- **Tests — CLEAN.** srp_stream_fsms has 1512 of 1512 at both heads, with identical logs. pp_top has 11,064: per-shard and per-section tallies are identical at both heads, and they reconcile to the author's receipt. The parent checker passes 75 of 75 in selftest. S1 is a suggestion.
- **Docs — CLEAN (R1 RESIDUE; R770-3 R1 and R2 carried as RESIDUE).** The delta has no doc change and none is needed: no doc names the old array, and no count moved. The PR body's Round 4 and Changes entries describe the delta, with R1's wording point. The Validation section names the round-4 gates and the scratch-parent result, and that result matches my run.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta `834cc88..6162885` (both files); parent `check_cpp_idiom.py` at 3 pins with `--list` and `--selftest`; PS12 and AS7-AS9 rows | R769-4 (delta); R769-3 (rest) | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| RTL | CLEAN | `git diff 834cc88 6162885 -- hdl` empty; 7 pp_top builds and the srp_stream_fsms build at both heads | R769-4 (delta); R769-3 (RTL) | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Robustness | CLEAN | type, initialiser and binding analysis of the 3 sites; probes M1 (AS7-AS9 fail) and M2 (PS12 fails); clone restore | R769-4 | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Tests | CLEAN | srp_stream_fsms 1512/1512 at both heads; pp_top 7 builds + 19 shards at both heads, reconciled to 11,064; author round-4 receipts (68/68 digests) | R769-4 | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Docs | CLEAN (R1, R770-3 R1/R2 RESIDUE) | PR body Round 4, Changes and Validation; READMEs and docs unchanged by the delta | R769-4 | 6162885ffee5d8e8897732be6479982b8dceaec9 |

## Real limits

- **pp_top was not run as one `make run` in my packet.** The single default-build simulation exceeds my bounded call. I ran every build and all six section simulations as the recipe does, plus the default build as 19 section shards. The sections run on separate model instances, not in one sequence. The per-shard equality across heads and the reconciliation to 10,509 are my evidence. The author's receipt is the one-process run.
- **Campaigns, the other suites and area were not re-run.** This covers the SRP and ACMP mutant campaigns, the other 34 suites, the REQ-tag check and the area runs. The delta does not reach them: it changes no HDL and none of their inputs except these two test-bench files. The two suites that compile these files were run.
- **Hosted `suites` jobs were in progress** when I recorded them. Their result is not known to this review.
- **The checker ran on a scratch parent** at dev `cc204c6` with the gitlink staged, not committed. No parent builder or native bank was run.
- **Physical calibration NOT RUN.** No hardware was used. Field skips are not hardware proof.
- **The author's evidence commit carries no signature.** Its integrity was checked against `MANIFEST.json` digests only.

## Pending manager duties

- The merge-turn current-dev candidate on dev `cc204c6`: the builder and native banks, and their receipts on the PR. No manager source bank was claimed or inferred at this head.
- Hosted/act acceptance, including the outcome of the two in-progress `suites` jobs at `6162885`.
- Carry R1, R770-3 R1 and R770-3 R2 to the residue checklist.
- Merge still needs two independent positive reviews and the full completion bar.

## Clone integrity after the probes

The review clone is at HEAD `6162885ffee5d8e8897732be6479982b8dceaec9`. Its tree and `git write-tree` both give `16b9d3fa90901d34a1225ae6821b693218431061`. `git status --porcelain --ignored` is empty. The working tree equals HEAD, and every tracked blob re-hashes to its index entry. Index modes and blobs equal `ls-tree -r HEAD`. The repository has no submodules (no `.gitmodules`, no mode-160000 entries). The required parent gitlink, `protocol-processor` = `6162885`, was proved in the scratch parent (`receipts/idiom-6162885.pins`). See `receipts/clone-integrity.txt`.

## Packet

- `scripts/run_idiom.sh`, `scripts/run_suites.sh`, `scripts/pp_top_staged.sh`, `scripts/probes.sh`: portable, all paths are arguments.
- `receipts/`: every listed log, rc, diff and record. Local paths are redacted to `<packet>`, `<clone>`, `<toolchain>`, `<verilator-5.050>` and `<home>`.
- `MANIFEST.sha256` lists every published receipt. `scratch/` is not published.

R769-4 FINISHED
