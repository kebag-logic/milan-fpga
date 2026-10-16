[R638] POSITIVE - exact head 6f86eee604729b80684526fc5b9be720d94f179a

# R638-9: internal independent review of issue #737 / PR #738, round 9 (delta 1c4d722c..6f86eee6)

- Head `6f86eee604729b80684526fc5b9be720d94f179a`, tree `32964c6b4b2fc2422ea0f4d05532e2999820240f`, base `fa7347fc`.
- Reviewer role: internal, cleared context, own detached clone. No source edit, commit, push, registry login, Docker/act, GitHub write or hardware.
- Verdict: **POSITIVE**. Both guards that round 8 left open are now closed by construction. Every round-8 finding is resolved at its cause, except one PR-body wording residue (R3).
- Open findings: none at MINOR or above. Three RESIDUE items and four SUGGESTIONs are listed below so the author can take them in one pass.

## How the review was done

1. **Context.** AGENTS.md, issue #737 (body, scope change, fail-fast), the round-9 assignment (PR #738 comment 6204018211) and the author's REVIEW READY (issue comment 6207079152).
2. **Delta.** `git diff 1c4d722c..6f86eee6`: 15 files.
   - Code: `exec_operands.py` (the readers), `exec_files.py` (snapshot and identity), `exec_audit.py` (dispatch and judge), the self-test, `ci_shell_walk.py` and the fixtures.
   - Docs and data: the guide, the reviewed lists, the census, the lock, and the receipts.
   - I read the code in full at the head. I did not read prior findings until my independent pass was finished.
3. **Published evidence.** Evidence commit `3db87100`, `review-evidence/737-image-r1/author-r9/`. I fetched six round-9 files from it, and each matches its Git blob id (`receipts/author-r9/`).
4. **Own probes.** These are host-side and disposable, under `scratch/` only. I ran no image and no Docker.
   - The operand readers compared against the real interpreters: bash 5.3, Perl 5.42, Node 22, Tcl 8.6.16, CPython 3.12.13 and 3.14.
   - The head's own `audit_step` and `Origin.judge`, run on the host.
   - An offline recompute of the recipe digest, and checks of the reviewed lists' integrity.
5. **Restore.** After the probes I removed the clone's `__pycache__` directories. Then I verified:
   - the worktree and index are clean;
   - `git ls-files -s` equals `git ls-tree -r HEAD` (sha256 `7f5ad7cc…`, which covers modes, blobs and paths);
   - all six submodule gitlinks equal the receipt's list.

## Items judged against the assignment

| Item | Result | Evidence at this head |
|---|---|---|
| 1. Inline and streamed text fails closed | **Closed.** | See "Item 1 detail" below. |
| 2. Provenance on bytes | **Closed.** | See "Item 2 detail" below. |
| 3. R639-8-F2, loader errno | **Resolved.** | See "Item 3 detail" below. |
| 4. R638-8-N3, accepted sources | **Resolved in the guide and the docstring.** The PR body is residue R3. | The guide's per-kind table ("Execution audit") and the `exec_audit.py:36-49` docstring match `Origin.judge` branch by branch. `checkout_writes` holds one entry. The self-test's own entries moved to `CONTROLS` (`exec_audit_selftest.py:33-49`). `receipts/reviewed-lists-check.txt` shows that exactly those three entries were removed from the production lists. |
| 5. R638-8-N4, `realpath` | **Resolved.** | See "Item 5 detail" below. |
| 6. Residue R1 and R2 | **Resolved.** | R1: the exact text is at `ci_differential_fixtures.py:437`. R2: `CI_IMAGE.md:99-100` carries the reviewer's text, with "the call" in place of a word the bare-metal gate (#259) refuses in tracked files. That substitution is accepted. |
| 7. Population re-traced, inventory `--check` last | **Verified from receipts.** | See "Item 7 detail" below. |

### Item 1 detail: inline and streamed text fails closed

Every image interpreter reaches a text digest or a named refusal.

- **Readers.** `exec_operands.py:51-237` model each interpreter's own rules:
  - shell `-c`, `-s`, `-o` and `-O`, with `+` forms;
  - CPython's option letters, with `-c`, `-m`, `-W` and `-X` values;
  - Perl's switch bundling (`-l` and `-0` octal, `-i`, `-F`, `-C` and `-I`) and one line added per `-e`;
  - Node's last-program-wins rule, `-p <arg>`, `-pe` and `--eval=`;
  - `Tcl_Main`'s rule: `-encoding NAME FILE`, otherwise a first word without `-`, otherwise stdin.
- **Refusals.** Anything a reader does not model is refused.
- **Judge.** `Origin.judge` (`exec_audit.py:462-481`) gives an inline or streamed program one of five results: exec-only, `unreadable`, step text, pinned (by masked digest and family) or `none`. `unreadable` and `none` are findings for both kinds (`:890-895`).
- **No interpreter judged as a plain program.** In the committed receipt, no row for an interpreter is judged as a plain program (`receipts/receipt-interpreter-rows.txt`).
- **Readers against the real interpreters** (`receipts/reader-probe.jsonl`):
  - `node -p X -e Y`: the reader and Node both take Y.
  - `node --eval X -p Y`: both take Y.
  - `tclsh -encoding utf-8 f`: script.
  - `tclsh -x`: stdin.
  - `perl -le A -e B`: the reader builds `A\nB\n`, as Perl does.
- **Self-test controls.** The author's in-image self-test log (blob `4814fe9f`) shows the round-8 probes `perl -e`, `perl -le` and `node -e` refused with the exact text digest. So are `perl -wE`, `perl -l012e … -e`, `node --eval=` and `node -p -e`, `| tclsh`, `| tclsh8.6`, `| python3`, and `perl5.38.2` as an unlisted spelling.
- **Refused options.** Perl `-M` and `-x`, Node `-r` and `-i`, shell `-i` and `--login`, and Python `-i` are refused by name. A socket stream is refused as unreadable. Pinned Perl, Node and Tcl texts stay clean.

### Item 2 detail: provenance on bytes

- **Snapshot before any job.** `Image` (`exec_files.py:124-160`) snapshots the image's directories once, before any job (`audit_population.py:321-344`).
- **Image program by key.** `Origin.identify` (`exec_audit.py:427-437`) marks a program as the image's own only through `Image.held`, which requires the path in that snapshot and an unchanged `(dev, ino, size, mtime, ctime)` key.
- **Interpreter by identity.** An interpreter family is assigned by file identity:
  - a family-named ELF file of the image;
  - or an image file with that file's bytes.
- **`dash` exemption.** `exec_only` is set only for the identity of the image's own `dash` file.
- **Every other program** goes through built-output or generated provenance (`:492-503`).
- **Controls refused by name:** `/usr/local/bin/cp` (an appended copy), an appended copy named `python3` given a checkout script, and `bash` copied as `dash` running `-c`.
- **Controls that stay clean:** the renamed and installed build outputs, `a.out`, LeakSanitizer and `initctl`.

### Item 3 detail: R639-8-F2, loader errno

- `executed` (`exec_audit.py:717-760`) answers `_loaded`'s own errno or reason and keeps the target separately.
- `notified` (`:711-715`) and `finish` (`:675-678`) turn any exception into a refusal or a kill. Every notification is answered.
- The bash ENOEXEC fallback (`:762-785`) matches bash's `shell_execve` and `check_binary_file`: a 128-byte sample, one line or two after `#!`, and an empty file runs nothing.
- Each control can fail for the defect it targets: without `fallback`, the job-written no-`#!` control would yield no finding.

### Item 5 detail: R638-8-N4, `realpath`

- `ci_shell_walk.py:325-359`: `realpath` is exact only when all of these hold:
  - it names the running script's own path or an ancestor;
  - nothing has run yet;
  - the path holds no link.
- Anywhere else it is runtime.
- `quiet` is captured before the substitution's own commands run. `capture` and `restore` do not reset it, so a sibling substitution that runs a program clears it.
- The `certain()` pre-read restores `quiet` only for word reading that the real walk then repeats.
- The new fixture `bash-realpath-after-a-program` (`ci_differential_fixtures.py:81-85`) has real outcomes `ok` and `hidden`, and the walker refuses it (`differential-receipt.json`). The receipt and census digests are bound in `tool-inventory.json`, and both match the files at the head.

### Item 7 detail: population and final checks

- **Committed receipt.** `ci/image/exec-audit-receipt.json` has sha256 `56e0a419…` and 546,532 bytes, as the author's population receipt states. It holds:
  - 94 traced steps;
  - 0 findings;
  - every exit status 0;
  - 183,831 instances.
- **Traced source.** The receipt's source tree `6932e0aa` is the tree of `84caae9a`. The only change from `84caae9a` to the head is the receipt itself.
- **Final checks.** The author's `round9-final-checks.json` names head `6f86eee6`. It records 26 checks with rc 0, and the inventory `--check` is last.
- **Lock.** The recipe digest, recomputed offline at the head, is `53fb5abd…`, the same as `image.lock.json` (`receipts/recipe-recompute.txt`).

## Findings

There is no BLOCKER, MAJOR or MINOR finding.

Under the round-8 class ruling, a new trick against a closed guard is RESIDUE. R1 and R2 are classed that way, and the reason is given for each. R3 is pure PR-body wording.

### R638-9-R1 RESIDUE (class ruling): a shell made a login shell by its `argv[0]` reads start files before a pinned program

- **Lenses:** Conformance, Robustness, Docs. None is left unclean, because this is a new trick against a closed guard.
- **Where:**
  - `ci/image/exec_operands.py:56`: `shell_operands` starts at word 1 and never reads `argv[0]`.
  - The claim at `exec_operands.py:8-11` and `docs/testing/CI_IMAGE.md:415-416`: options that read code from start files are refused.
- **Evidence:**
  - bash treats a leading `-` in `argv[0]` as a login shell. You get that from the `exec -l` or `exec -a -su` builtins, or from `sudo -i`.
  - A non-interactive `-su` shell reads `/etc/profile` and `~/.bash_profile` in stock bash. Builds with `NON_INTERACTIVE_LOGIN_SHELLS` do the same for any `-` name.
  - `receipts/reader-probe.jsonl`: host bash read `~/.bash_profile` for both `-su` and `-bash`, and the reader returned `inline` with the plain text.
  - `receipts/login-probe.json`: the head's own `audit_step` judged `exec -l bash -c 'echo program ran'` with the inner text `pinned` and no refusal, while `~/.bash_profile` ran (`start_file_ran: true`). The probe step's one finding is the host's `/etc/profile` running `tty`, a host artifact.
  - For `dash`, the same `argv[0]` rule reads `$HOME/.profile`. That code is `dash` code, so the exemption already judges it by its execs.
- **Why RESIDUE and not MAJOR:**
  - The options guard is an allowlist over the interpreter's options, and it holds.
  - `argv[0]` can only be chosen by a calling program: `exec`, `sudo` or a job-written program. The static command table bounds every `exec` and `sudo` form by exact pattern (`command-table.json` `commands/exec`, `commands/sudo`). Job-written programs are accepted only by reviewed digest.
  - Reaching this therefore needs reviewed source that chooses it, which the threat model leaves to code review.
- **Exact fix (optional code):** in `shell_operands`, refuse a shell whose `words[0]` starts with `-`, with the reason "shell started as a login shell reads code from start files".
- **Docs:** change `CI_IMAGE.md:416` to "That covers shell `-i`, `-l`, `--login` and a login shell named by its `argv[0]`, and Python `-i`."
- **Verification:** add a self-test control, `exec -l bash -c true`, refused by name.

### R638-9-R2 RESIDUE (class ruling): an interpreter's script operand is judged by reading it at the exec, before the interpreter opens it

- **Lenses:** Robustness, Docs.
- **Where:**
  - `ci/image/exec_audit.py:482-496`, `Origin.judge`. The operand is resolved and digested at the notification, but nothing requires a regular file there. Exec targets do require one, at `_target` `:294`.
  - The boundary list at `CI_IMAGE.md:99-100` names only the exec-target gap.
- **Evidence:**
  - `receipts/fifo-judge-probe.json`: the head's `Origin.judge`, given a bash operand that is a named pipe, read it (consuming it) and returned `copy of ok.sh`. The next reader of the pipe received `echo UNREVIEWED`.
  - `receipts/fifo-probe-exec-writer-hang.txt`: end to end, the head's `audit_step` deadlocked for 600 s. The audit was blocked reading the pipe, while the writer's own exec waited for the audit to answer.
  - A regular job-written file rewritten between the judgment and the interpreter's open is the same gap, made racy instead of deterministic.
- **Why RESIDUE:**
  - It needs a deliberately built pipe or a timed rewrite.
  - A benign pipe operand fails closed: the audit consumes the program, and the result is a hang or a finding, never a clean receipt for unreviewed text.
- **Exact fix:** add to the boundary list after `CI_IMAGE.md:100`:

  ```text
  - An interpreter's script is judged when its exec is notified, before the interpreter opens it.
    A job-written file replaced between the two is not reported.
  ```

- **Optional code:** refuse a script operand that is not a regular file, by name, as exec targets already are. That also removes the deadlock.
- **Verification:** a self-test control with a named-pipe operand is refused by name.

### R638-9-R3 RESIDUE (wording, PR body): the PR body does not list the accepted sources per kind, and its Round 8 row still states the superseded list

- **Lenses:** Docs.
- **Where:**
  - PR #738 body, Round 9 row "Accepted sources (N3)" (body line 331), says only "The guide and the docstring list exactly…".
  - The Round 8 row "Inline and streamed programs" (body line 289) still says "by exact text digest in `inline_programs`, the step's own text, or a checkout file". As built, a streamed checkout file is refused, and texts are keyed by masked digest.
- **Authority:** R638-8-N3 required "the guide, docstring and PR body list exactly the accepted sources per kind".
- **Exact fix:** in the Round 9 row, replace "The guide and the docstring list exactly the accepted sources per kind;" with:

  ```text
  File program: an image file present before the job and unchanged, named in `scripts`; a checkout file unchanged since the job started, or a byte copy of one; a job-written copy of an image executable, judged as that file by its name; the step's own text; a reviewed `generated_programs` entry of its interpreter. Inline or streamed program: the step's own text, or a reviewed `inline_programs` entry of its interpreter, by its masked digest. The image's own `dash` file is judged by its execs;
  ```

  Then append " (superseded in Round 9)" to the Round 8 row's first cell.

### Suggestions (non-blocking)

- **R638-9-S1 (Robustness).** `exec_audit.py:318` splits a `#!` line at the first space only. The kernel (`fs/binfmt_script.c`) splits at a space or a tab. With `#!/bin/sh<TAB>-e`, the audit fails the exec with ENOENT, where the kernel would run `/bin/sh -e`. This fails closed but changes what runs. Splitting on either blank would match the kernel.
- **R638-9-S2 (Robustness).** `fallback` (`exec_audit.py:771`) decides bash's in-process run by the caller file's basename `bash`, while every other interpreter decision is by file identity. Using `family == "shell" and not exec_only` would cover an image file with bash's bytes under another name. No such file appears in the receipt.
- **R638-9-S3 (Docs, Robustness).** The 23 new pinned Tcl stream texts name held checkout paths under the trace's checkout root `/work/` (for example `source {/work/sw/litex/timing_grade.tcl}`). Round 8's 81 entries named none (`receipts/reviewed-lists-check.txt`). These digests therefore hold only at the documented `/work` mount, and a run at another checkout path would refuse them (fail closed). Either say so in the guide's reviewed-list paragraph, or mask the checkout root itself to a placeholder.
- **R638-9-S4 (Tests).** The appended-copy `python3` control copies `/usr/bin/true`. A control that appends to the image's own `python3` bytes would also show that a job copy of real interpreter bytes gains no family. The bytes rule makes this hold by construction, so this is optional.
- **Carried, optional.** R638-8-S3 (residue location binding, real-tool statuses) and R638-8-S4 (Make walker walk-time existence) are unchanged by this delta.

Checked and not a finding:

- `probe='R638-8-N4'` (`ci_differential_fixtures.py:82`) is fixture data. Under the file's documented convention (`:8`, "`probe` names the review finding it reproduces") it is not a source comment, so it falls outside the comment rule.
- Python `-W ignore::mod.Cls` imports `mod` at start-up. On CPython 3.12.13 and 3.14 it found no user-site module, because `-W` options are applied before `site` adds that path (`receipts/reader-probe.jsonl`), so this is not a reading path.
- No new source comment in the delta names a lane, round, reviewer or comment ID.

## Prior findings at this head (read after the independent pass)

| Finding | Disposition | Evidence |
|---|---|---|
| R638-8-N1 = R639-8-F1 (Perl and Node text unjudged; bundled switches) | **Resolved** | Item 1 above. The readers, the `unreadable` finding for inline, and 10 text controls plus 7 option controls in the image. |
| R638-8-N2 (provenance by name and directory) | **Resolved** | Item 2 above. The job-start key, identity-based families and the three named controls. |
| R638-8-N3 (as-built accepted sources; `checkout_writes` count) | **Resolved** in the guide, the docstring and the count. The PR-body wording is retained as **R638-9-R3** (RESIDUE). | Item 4 above. |
| R638-8-N4 (`realpath` from walk-time links) | **Resolved** | Item 5 above. |
| R638-8-R1 = R639-8-RES1 (comment with round and reviewer IDs) | **Resolved** | `ci_differential_fixtures.py:437` has the manager's exact text. |
| R638-8-R2 (unnamed notify-then-lookup limit) | **Resolved** | `CI_IMAGE.md:99-100`. |
| R639-8-F2 (loader errno dispatch) | **Resolved** | Item 3 above. |
| R639-8-S1 (`dash` scope decision and wording) | **Resolved as ruled** | The exemption is bound to the image `dash` identity. "Runs nothing in-process" is replaced by the wording on loaded code and builtins (`CI_IMAGE.md:90-93`). |
| R638-8-S1 (no `.` or `..` masked) | **Taken** | `COMPONENT` at `exec_audit.py:121`; a self-test control. |
| R638-8-S2 (`dash` binding) | **Taken** | Item 2 above. |
| R638-8-S3, R638-8-S4 | Open, optional | Unchanged. |

## Clean-lens evidence

```text
[R638] PASS Conformance - ci/image/exec_operands.py:51-247, ci/image/exec_audit.py:427-523 and :848-923, ci/image/exec_files.py:124-160, scripts/ci_shell_walk.py:325-370, author round9-exec-audit-selftest.log (blob 4814fe9f) - each of the assignment's items 1-7 checked against the code at 6f86eee6 and the in-image controls; the round-8 probes are refused, pinned texts are clean, and the N2 controls are refused by name; R1 and R3 are residue only.
[R638] PASS RTL - git diff --stat 1c4d722c..6f86eee6 (no HDL, testbench or synthesis source changed); the audit's dispatch state machine at ci/image/exec_audit.py:692-809 - every notification path answers once (errno, refusal, continue or kill), the exception paths fail closed, and the module split keeps the documented interfaces (invocation, operands, built_output, Image.held).
[R638] PASS Robustness - receipts/reader-probe.jsonl, receipts/login-probe.json, receipts/fifo-judge-probe.json, receipts/fifo-probe-exec-writer-hang.txt - readers checked against real interpreters for ordering and last-wins rules, unreadable streams, and non-regular operands; the escapes found need deliberately built forms (R1, R2: residue by class ruling).
[R638] PASS Tests - ci/image/exec_audit_selftest.py:271-358 (74 controls; author log rc 0), scripts/ci_differential_fixtures.py:72-85, ci/image/differential-receipt.json (213/213; realpath fixtures ok/hidden refused) - each new control can fail for its defect (fallback, masks, unpinned digests asserted exactly); no existing expectation was weakened (the stricter changes are listed in the PR's decision point 5).
[R638] PASS Docs - docs/testing/CI_IMAGE.md:62-100 and 366-530, ci/image/exec_audit.py:1-55, ci/image/exec_operands.py:1-16, PR #738 body Round 9 - the guide and docstrings match the code branch by branch, and the counts (103 inline or streamed, 450 generated, 1 checkout write) match exec-audit.json; the PR-body list is residue R3, and the boundary wording is residue R1 and R2.
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `exec_operands.py`, `exec_files.py`, `exec_audit.py` judge and dispatch, `ci_shell_walk.py` `realpath`/`own`, assignment items 1-7, author self-test log, committed receipt | R638-9 | `6f86eee604729b80684526fc5b9be720d94f179a` |
| RTL | CLEAN (no HDL in the delta; tooling architecture and dispatch error paths applied) | diff stat; `exec_audit.py:692-809`; module interfaces | R638-9 | `6f86eee604729b80684526fc5b9be720d94f179a` |
| Robustness | CLEAN (R1 and R2 are RESIDUE by class ruling) | host reader, login and pipe probes; `Origin.judge`; mask regexes `exec_audit.py:119-121`, `:342-352`, `:407-417` | R638-9 | `6f86eee604729b80684526fc5b9be720d94f179a` |
| Tests | CLEAN | `exec_audit_selftest.py` (74 controls), differential fixtures and receipt (213/213), `ci_inventory_exact_selftest.py` expectation changes | R638-9 | `6f86eee604729b80684526fc5b9be720d94f179a` |
| Docs | CLEAN (R1, R2 and R3 are RESIDUE) | `CI_IMAGE.md`, the docstrings, the PR #738 body, `exec-audit.json` counts | R638-9 | `6f86eee604729b80684526fc5b9be720d94f179a` |

## Real limits

- **No image execution here.** I ran no image, Docker or act. The in-image self-test (74 controls), the 213 differential fixtures, the population trace and the cold builds rest on the author's published receipts, which I verified by Git blob id.
- **Unsigned evidence.** The evidence commit is not verified as signed, so these are verified public bytes, not an authenticated signed packet.
- **Host probes.**
  - They used host interpreter versions: bash 5.3, Perl 5.42, CPython 3.12.13 and 3.14, Node 22 and Tcl 8.6.16. The image has Perl 5.38, CPython 3.12.3 and bash 5.2.
  - The R1 behaviour for `-bash` depends on the build flag `NON_INTERACTIVE_LOGIN_SHELLS`. `-su` reads the files in stock bash, by bash's own source.
- **Host gates not rerun.** `ci_inventory_exact_selftest.py` and the inventory `--check` need the checksum-pinned shell parser, which is not on this host. Their results are the author's.
- **Not regenerated.** I did not regenerate the 450 generated or 103 inline entries from their generators. I checked the key-to-text integrity of the 85 text entries and that the retained entries are unchanged since round 8.
- **Not hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted CI only partly complete.** At the time of review, hosted contexts at this head were partly complete (`receipts/hosted-checkruns-snapshot.tsv`). This review claims no hosted or act acceptance, and no manager source bank ran at this head.

## Pending manager duties

- Hosted and act acceptance at this head. This includes telling executed jobs from skipped contexts; for example, `Physical gPTP` is skipped.
- Building and validating the current-dev merge candidate (base `fa7347fc`, live dev `734eb780`) with the builder and native banks at the merge turn, then linking those receipts on the PR.
- Carrying R638-9-R1, R2 and R3 to the residue checklist. Deciding whether to adopt the optional code changes in R1, R2 and S1-S3.
- The second independent review and the maintainer's merge authorization. Registry publication and the round-trip check remain pending.

R638-9 FINISHED
