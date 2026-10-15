[R638] NEGATIVE - exact head 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267

# R638-8: internal independent review of issue #737 / PR #738, round 8 (delta feef7c9f..1c4d722c)

Head `1c4d722cb1d0279f0ec44b0fbe87c810adfb9267`, tree `bb73b9148913001339b3a7c9cfb00dfbfff5f439`. Source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`.

**Verdict:** NEGATIVE, with two MAJOR, two MINOR, two RESIDUE and four SUGGESTION items.

The round-8 class ruling (PR #738 comment 6196923564) asks, for each guard, whether it is closed by construction and whether its control refuses. Five of the eight items hold:

- 1, exec ABI: holds.
- 2, non-path exec: holds.
- 5, workflow `env:` allowlist: holds.
- 6, walker: holds, except one MINOR.
- 8, re-traced population and `--check` last: holds.

Two guards are **not** closed by construction. In both, the decision procedure exempts a whole class by name or by location, so the round's own refused controls run clean once renamed or moved:

- **R638-8-N1 MAJOR (item 3).** An unpinned `perl -e`, `perl -E` or `node -e` inline program is accepted with no finding, and `perl -le CODE` is read as a missing script. The guard's listed families include Perl and Node, but only shell and Python texts are ever judged.
- **R638-8-N2 MAJOR (item 4).** Program provenance depends on the name or directory, not on the bytes. The ruling's own refused control, a copy with one byte appended, runs clean in two cases:
  - when it is named `python3` and given a checkout script;
  - when it sits in an image directory under a listed name.

  A copy of `bash` renamed `dash` runs an unpinned `-c` program clean.

Each MAJOR was demonstrated in real seccomp-traced runs of the head's own `audit_step`. Each retains part of a round-7 finding at its cause: N1 retains part of R638-7-N1 and R639-7-F2, and N2 retains part of R639-7-F4.

RTL is CLEAN, because the delta contains no RTL. Conformance, Robustness, Tests and Docs are UNCLEAN.

## How the review was done

The review used a cleared context. Context was loaded in this order:

1. AGENTS.md and CONTRIBUTING.md (via AGENTS.md).
2. The issue body's acceptance, scope change and plan.
3. The round-8 ruling (6196923564) and the author's REVIEW READY (issue comment 6203674207).
4. The PR body (Round 8 and How to validate).
5. `git diff feef7c9f..1c4d722c`, 20 files, read by section: `ci/image/exec_audit.py`, `exec_operands.py`, `exec_files.py`, `exec_audit_selftest.py`, `audit_population.py`, `exec-audit.json`, `scripts/ci_shell_walk.py`, `ci_syntax.py`, `ci_tool_inventory.py`, `ci_differential*.py` and `docs/testing/CI_IMAGE.md`.
6. The committed receipts, then the author's published round-8 receipts.

The round-7 reviews (6196727731, 6196901768) were read only after the independent pass.

Probes ran on the host, outside Docker. Each imports the head's own `exec_audit` from the clone and calls its `audit_step` or `judge`. Each is portable, as `python3 -I probes/<p>.py <checkout> <scratch>`. Their receipts are under `receipts/`.

The host is kernel 7.2.9, CPython 3.14.7, perl 5.42.2, node 22.23.2, gcc 16.2.1 and bash 5.3.20 (`receipts/host_env.txt`). The verdicts on Perl, Node, `dash` and programs do not depend on the Python version. The Python-family arms were not used as probe subjects, because the host binary is `python3.14`, which the audit does not class as an interpreter.

The clone was restored and verified at the end (`receipts/restore_check.txt`):

- HEAD and tree are exact.
- Worktree and index are clean, including ignored files. The `__pycache__` the probes created was removed.
- The index (mode, blob, path) equals the HEAD tree, digest `9c90a850…`.
- All six gitlinks are present.

## Guards judged (ruling items 1-8)

| Item | Guard as built | Closed by construction? | Control refuses? | Evidence |
|---|---|---|---|---|
| 1 Exec ABI | `exec_audit.py:86-88` BPF: arch != x86-64 jumps to NOTIF; `JSET 0x40000000` (x32) jumps to NOTIF; `:632-635` refuses with EPERM | Yes. Hand-decoded jump offsets: 1+1+6, 3+1+4 and so on all land on insn 8 (`RET_USER_NOTIF`) | Yes | `receipts/p4_abi_target.txt`: i386 and x32 trampolines are refused by name, the marker never runs, and a static build stays clean. The author's in-image selftest gives 41 PASS (`receipts/author-round8-exec-audit-selftest.log`) |
| 2 Non-path exec | `_target`/`resolve` `:186-279`: walks components, refuses `/proc` and `/dev`, a memfd, a deleted file or a non-path fd, and requires the caller's own `/proc/<pid>/…` view to be the same inode | Yes | Yes | `receipts/p4_abi_target.txt`: the memfd, deleted and `/proc/self/fd` link execs are refused before they run |
| 3 Interpreter programs | `Origin.judge` `:420-430`, `judge` `:852-857`, `exec_operands.py` | **No** for Perl and Node inline. Shell and Python are closed | Shell and Python yes; Perl and Node no control | **R638-8-N1**. The 81 list entries are verified: 63 text digests and 18 variant rebuilds match (`receipts/p3_variants.txt`) |
| 4 Positive provenance | `Origin.judge` `:431-471`, `started_exec`/`ended` `:391-412` | **No**. Interpreter-named programs and image-directory programs never have their bytes judged | Only at the selftest's chosen name and directory | **R638-8-N2** (`receipts/p2_trace.txt`, `receipts/p5_interp_named.txt`) |
| 5 Workflow `env:` | `ci_syntax.py:21-48`, called per step at `ci_tool_inventory.py:196-201` over workflow, job and step `env` merged | Yes: an allowlist of 25 names, `BASH_FUNC_*` refused, `HOOKS` plus the `GIT_CONFIG_*` and `LD_*` prefixes refused | Yes | `ci/image/differential-receipt.json`: the 11 `R638-7-N3a-*` fixtures are all `refused`, with the expected reason |
| 6 Walker | `certain` `ci_shell_walk.py:422-438` (only `true`, `:` and assignments); `cd` without errexit is AMBIGUOUS (`:861-864`); `declaration` `:546-605` restricted to `-a`, `-A` and `-gA`, initializers expanded first, `+=` refused; replay digests checkout files at job start (`Origin`, after `reset(root)` at `audit_population.py:335-342`) | Yes for tests, `cd` and declarations. **No** for `$(realpath <literal>)` | Yes | **R638-8-N4 MINOR**. Fixtures: 7 `R639-7-F1-*` and 2 `R638-7-N3b-*` meet expectation; 211/211 overall, 0 mismatches |
| 7 Docs | `CI_IMAGE.md:62-96`, `:358-440` | Threat model stated. Two table rows overstate (N1, N2), two "as built" statements are false (N3), and one limit is unnamed (R638-8-R2) | n/a | See the findings |
| 8 Re-trace and `--check` last | committed `ci/image/exec-audit-receipt.json`; author `round8-final-checks.json` | Yes | n/a | Details below this table |

Item 8 detail. The receipt:

- covers 94 of 98 steps traced, `clean: true`, every exit 0 and 0 findings;
- holds 183,834 instances, with users 1000 and 0;
- was traced at `c2531c634`, which differs from the head only in the receipt (`git diff --stat c2531c634 1c4d722cb`);
- has a sha256 of `9f3ff908…`, equal to the author's `round8-population-receipt.json` pointer.

The author's checks: 26 run, all rc 0, under CPython 3.12.3, with `inventory-check-last` last. The three author receipts match the published `MANIFEST.json` digests (`receipts/author_manifest_check.txt`). All 341 inventory input digests match the head bytes (`receipts/inventory_inputs.txt`).

## Findings

### R638-8-N1 MAJOR: Perl and Node inline programs are accepted unjudged, and bundled Perl switches hide the program

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `ci/image/exec_operands.py:17-19`: `PINNABLE = {"shell", "python"}`.
- `ci/image/exec_operands.py:85-101` (`other_operands`):
  - Perl and Node inline gets `text: None`;
  - only the *first* letter after `-` is tested against `eEp`, so `-le`, `-ne` and `-wE` fall through to "script".
- `ci/image/exec_audit.py:424-426` (`Origin.judge`): an inline program with no digest gets provenance `unreadable`.
- `ci/image/exec_audit.py:852-857` (`judge`): `unreadable` is a finding only for `stream`. An `inline` with `unreadable` matches no branch, so it gets **no finding**.
- `ci/image/exec_audit.py:436-437`: a misparsed `-le CODE` becomes a script operand that does not resolve, and `absent` gets no finding.
- Documentation claims the guard covers Perl and Node inline:
  - `docs/testing/CI_IMAGE.md:79` (table row "Interpreter programs");
  - `CI_IMAGE.md:393` ("That holds for `bash`, Python, Perl, Node and Tcl, inline, streamed or from a file.");
  - `exec_audit.py:25-31` (docstring);
  - PR body Round 8 ("`python3`, `bash`, Perl, Node and Tcl programs by exact text digest").

**Authority:** the ruling's item 3 ("Every `-c`, `-` or stdin program ... pinned by the exact digest ... Any other inline or streamed program is refused by name"). The assignment names python3, bash, perl, node and tcl with `-c` and `-e`. R638-7-N1 required that "An unjudged inline or stream program does not yield `clean`", and R639-7-F2 that "An allowlisted interpreter alone must not authorize their contents". `perl`, `node` and `tclsh` are all in `exec-audit.json` `programs`.

**Evidence:** `probes/p2_trace.py` (receipt `receipts/p2_trace.txt`) runs real steps under the head's seccomp audit, each with its text pinned as step text.

| Step | Program ran | Clean | Provenance rows |
|---|---|---|---|
| `perl -e 'print qq(PERL-E-RAN\n)'` | yes | **true** | `inline perl unreadable` |
| `perl -le 'print q(PERL-LE-RAN)'` | yes | **true** | `script absent` |
| `node -e 'console.log("NODE-E-RAN")'` | yes | **true** | `inline node unreadable` |
| control: nested `bash -c 'echo …'` (unpinned) | yes | false | `unpinned inline program: bash …` |

`probes/p1_classify.py` (`receipts/p1_classify.txt`) gives the same classification without exec, and `perl -E` behaves the same. The current population has no Perl or Node inline instance (receipt rows), so the defect is latent. It is still a structural fail-open of the guard, not a contrived form: the family's primary inline option is affected. The selftest has no Perl or Node control (`exec_audit_selftest.py`; 41 controls, none Perl or Node).

**Impact:** a step that starts running `perl -e` or `node -e` code passes the execution authority clean, with nothing judged. That code may install by writing files, or `require` a checkout-external module. This is the exact drift item 3 exists to catch, for two of its five named families.

**Required outcome:**

- Any inline or streamed program whose text is not read and pinned is a finding, never clean. `unreadable` refuses for `inline` as it already does for `stream`. Either pin Perl and Node texts too, or refuse them by name.
- Perl and Node option reading finds the program as the interpreter does, including bundled switches (`-le`, `-ne`, `-pe`, `-wE`) and `--eval=…`. Otherwise it refuses any option it does not model, never classing the next word as a script.
- The docs, docstring and PR body state the families actually pinned.

**Verification:**

- New selftest controls `perl -e`, `perl -le`, `node -e`, each refused by name in the image with `--network none`.
- The existing 41 controls keep their results.
- The population is re-traced clean, or the population's own Perl and Node uses, if any appear, are pinned.

### R638-8-N2 MAJOR: program provenance is decided by name and directory, not bytes, so the item-4 controls pass once renamed or moved

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- (a) Interpreter-named programs. `exec_audit.py:752-776` (`invocation`) classes a program as an interpreter by its file **basename** (`interpreter(base)`). From then on only its operand (script, module, inline or stream) is judged. The program file's own bytes are never compared with the built set, the generated list or the image snapshot.
  - `:422-423` and `:462-463` grant `exec-only interpreter` to any program *named* `dash`, wherever it is.
  - `:845-846` checks only that the basename is listed.
- (b) Image directories. `exec_audit.py:440-441` returns `named` for any path under `SYSTEM_ROOTS` (`/usr/`, `/opt/`, `/etc/`, …). `:847-851` then checks only the basename against `programs` and `scripts`.
  - `Origin` already snapshots those directories at job start (`:327-332`), but uses the snapshot only for `image_copy`.
  - Image steps can write there: docs-check runs as uid 0, and the head's own selftest plants files in `/usr/local/bin` as root (`exec_audit_selftest.py:5-6`, `:66`, `:77-80`). The tree's workflows add tools exactly this way:
    - `.github/workflows/rtl-fast.yml:107` (`sudo make install`), `:176` (`ln -sf … /usr/local/bin/`) and `:190-191` (`install … /usr/local/bin/sv2v`);
    - `elaborate.yml:216` (`tar xzf … -C /opt`).
- Docs:
  - `CI_IMAGE.md:80` says "Programs outside the image | A traced build output's bytes, or the reviewed generated list";
  - `:390` says "A program or script in the image's own directories must be named". This is a name check over job-writable directories;
  - `:412-413` and `:90` say `dash` is exempt because "the image's `dash`" loads nothing, but the exemption is granted by name.

**Authority:**

- The ruling's item 4: "A non-inventory executable is accepted only if it is either the declared output … or on a reviewed list of generated programs … The byte-appended copy becomes a refused control."
- Item 3, for (a)'s `dash` arm.
- R639-7-F4 required "positive provenance that survives this case, or refuse programs whose provenance cannot be established".

**Evidence:** real traced steps under the head's `audit_step` (`receipts/p5_interp_named.txt`, `receipts/p2_trace.txt`).

| Step | Clean | Rows / findings |
|---|---|---|
| control: `cp /usr/bin/printenv zz_appended; printf '\0' >> zz_appended; ./zz_appended HOME` | false | `program without provenance: zz_appended` |
| same appended copy of `true`, named `python3`, run as `…/bin/python3 tool.py` (checkout script) | **true** | only `script tool.py checkout`. The binary that ran is not judged |
| copy of `bash` renamed `…/bin/dash`, `-c 'echo RENAMED-BASH-RAN; shopt -s extglob; echo $BASH_VERSION'` | **true** | `inline dash exec-only interpreter`. Bash ran an unpinned program in-process |
| appended copy of `printenv` at `<stand-in system root>/bin/cp` (listed name) | **true** | `program cp named` |

The last row points one extra entry of `SYSTEM_ROOTS` at a writable stand-in for `/usr/local/`, because the host run is unprivileged. The decision code is unchanged: `judge` reads the module's `SYSTEM_ROOTS` and needs nothing else. In the image the same bytes would land in `/usr/local/bin/cp` as uid 0.

**Why MAJOR and not RESIDUE under the ruling:** none of these is a new trick against a closed check. The check for item 4 is never applied to two whole classes, programs with an interpreter's basename and programs under the image directories. Each class is selected by a property, name or path, that the job controls and that says nothing about the bytes. A guard that refuses its control in `/tmp/x` and accepts it at `/usr/local/bin/cp` or under the name `python3` is not closed by construction. The fix is direct: `Origin.system` already holds the job-start snapshot.

**Impact:** a step that starts using a non-image tool passes clean when the tool is installed into `/usr/local` or `/opt` under a listed name, or ships under an interpreter's name. Examples are a re-installed tool, a tool restored or extracted from a cache or tarball, or a virtualenv-style interpreter. The image's pinned tool is then not what ran, and the audit cannot tell.

**Required outcome:**

- A program is accepted as an image program only if its file is the one the image held at job start: path present in `Origin.system` with an unchanged key or digest.
- Any other executable needs item-4 provenance, whatever its directory or name. That includes the interpreter binary itself when the operand is judged, and the `dash` exemption, which belongs to the image's `dash` file, not to the name.
- The docs state the rule as built.

**Verification:** new in-image controls, each refused by name:

- the appended copy installed as `/usr/local/bin/<listed name>`;
- the appended copy named `python3` running a checkout script;
- `bash` copied to a job path named `dash` running `-c`.

The existing controls stay clean: renamed and installed build outputs, a.out, LeakSanitizer and the `initctl` stub. The population is re-traced clean.

### R638-8-N3 MINOR: two "as built" statements in the image guide are false

**Lenses:** Docs, Conformance.

- (a) `docs/testing/CI_IMAGE.md:393-401` lists "a file in the checkout, unchanged since the job started" among accepted *interpreter program texts* for inline, streamed or file programs. The REVIEW READY and the PR body say the same for streamed programs. As built, `Origin.judge` `:420-430` accepts an inline or streamed text only as step text or a pinned entry. `bash < scripts/x.sh` and `bash -s < x.sh` on an unchanged checkout file are refused: `receipts/p6_stream_checkout.txt`, "unpinned streamed program: bash 612099db…", while `bash x.sh` stays clean. This fails closed, so there is no hole, but the guard is not stated as built (ruling item 7).
- (b) `CI_IMAGE.md:435` says the reviewed `checkout_writes` list "holds one entry". `ci/image/exec-audit.json:2-10` holds two. The second, `zz_reviewed_write.txt`, is the audit's own selftest control in the production list.

**Impact:** a reader, or the next reviewer, is told a streamed checkout script is accepted when it is refused, and gets a wrong count of reviewed exemptions.

**Required outcome:** the guide, docstring and PR body list exactly the accepted sources per kind: file program, inline and streamed. The count matches the list, or the selftest entry leaves the production list (the selftest could pass its own names).

**Verification:** read the corrected lines against `Origin.judge` and `exec-audit.json`. Optionally add a selftest control for `bash < checkout file` with whichever outcome is documented.

### R638-8-N4 MINOR: `$(realpath <literal>)` is still decided from the checkout's state

**Lenses:** Conformance, Robustness, Docs.

**Where:**

- `scripts/ci_shell_walk.py:349-351` (`exact_substitution`): `if target.exists(): return str(target.resolve())`, so the walker fixes the value from the links and paths at walk time.
- `docs/testing/CI_IMAGE.md:75` and `:233` say "Nothing is decided from the checkout's state, since an earlier program can change any path".
- `CI_IMAGE.md:307` says "`$(dirname <literal>)` and `$(realpath <literal>)` are exact functions of the operand".
- The shape is in use (census `bash:word.realpath` → fixture `bash-realpath`).

**Authority:** ruling item 6. The delta itself applies this reasoning to `$(cd X && pwd)` (`ci_shell_walk.py:325-333`, "Elsewhere an earlier program may have removed it"), and not to `realpath`.

**Evidence:** code reading. This could not be run on the host, because no checksum-pinned shfmt is available and the in-image differential needs Docker. The form is the round-7 R638-7-N3b form with `realpath` in place of `cd`. An earlier accepted program re-points or removes `sub/link`, then `X=$(realpath sub/link); bash "$X/run.sh"`. The walker follows the walk-time target, and bash runs the other one.

Neither replay check catches this:

- `exec_files.snapshot` keeps regular files only, so a link change in the checkout is never compared;
- the script that ran is an unchanged checkout file.

**Impact:** the walked script can differ from the one that runs. The execution audit still judges each exec the real script makes, so this is narrow; hence MINOR, not MAJOR.

**Required outcome:** either treat `$(realpath <literal>)` like `cd-pwd`, resolved only where its result cannot differ and runtime elsewhere, or scope the docs' claims at `:75`, `:233` and `:307` to what is built: tests and `cd` only, with `realpath` read from walk-time links.

**Verification:** a differential fixture in which an earlier program re-points a link before `$(realpath …)` is refused or resolved identically, or the docs are corrected.

### R638-8-R1 RESIDUE: new source comment names review rounds and reviewer IDs

- `scripts/ci_differential_fixtures.py:424`: `# R638-7 and R639-7 probes: workflow environment, checkout state, and local declarations.` This is new in this delta and breaks the owner's source-comment rule. The existing `:314`, `:351`, `:369` and `:396` are tracked by #746.
- **Exact fix:** `# Probes for workflow environment names, checkout state and local declarations.`

### R638-8-R2 RESIDUE: an unnamed remaining limit (ruling item 7)

The audit judges an exec target when the call is notified, then lets the kernel's own lookup run (`exec_audit.py:537-543`, `CONTINUE`). A file replaced between the two is not seen. This is the standard seccomp user-notification limit. Under this threat model it can only be reached deliberately, but the guide does not name it among "The remaining limits".

**Exact fix:** add to the boundary list at `docs/testing/CI_IMAGE.md:84-96`:

```text
- An exec target is judged when its call is notified, before the kernel looks it up again.
  A file replaced between the two looks is not reported.
```

### Suggestions (non-blocking)

- **R638-8-S1 (Robustness).** `exec_audit.py:321`: the job-temporary mask `(?:/[A-Za-z0-9_.-]+)*` admits `.` and `..` components. So `/tmp/../usr/…` masks to `/tmp/<job>`, and two generated scripts reaching different files outside `/tmp` share a digest. Excluding `.` and `..` components would keep "carries no command" and also make it "names only job-temporary files". This is contrived under the threat model.
- **R638-8-S2 (Tests).** The author's open risk 1 (`dash` not pinned) is sound only if the exemption is bound to the image's `dash` binary; see N2(a). Once that binding exists, the `dash` boundary is closed by construction. The selftest's loader check (`PASS: the exec-only interpreter dash imports no dynamic loader entry`) then covers it. I recommend the manager accept the boundary on that condition.
- **R638-8-S3 (Tests).** R638-7-S1 (residue outcome not bound to the unresolved command's location) and R638-7-S2 (real-tool statuses recorded but not compared) are not addressed. They remain optional.
- **R638-8-S4 (Robustness).** `ci_make_walk.py:704`, `:718` and `:753` still decide built-in rule applicability and `prerequisite-file` from walk-time existence. This code is outside the delta and backstopped by the audit (any `cc` that runs is judged). Ruling item 6 names only shell tests. It is noted for completeness only.

## Prior findings at this head (read after the independent pass)

| Prior finding | Status at `1c4d722c` | Basis |
|---|---|---|
| R638-7-N1 (inline and streamed programs unjudged) | **Partly retained as R638-8-N1** | Python and bash are fixed (local-wheel `-c` and `-` controls refused, a pinned `print(1)` clean; author selftest). Perl and Node inline are still clean unjudged (`receipts/p2_trace.txt`) |
| R638-7-N2 (foreign ABI; fd and memfd exec) | Resolved | `receipts/p4_abi_target.txt`; author selftest |
| R638-7-N3a (env denylist) | Resolved | allowlist `ci_syntax.py:21-48`; 11 fixtures refused |
| R638-7-N3b (certain `cd` from the checkout) | Resolved for `cd` and tests | `certain` `ci_shell_walk.py:422-438`, AMBIGUOUS `:861-864`; fixtures refused. The `realpath` analogue is R638-8-N4 |
| R638-7-N3c (rewritten followed script) | Resolved | `Origin.judge` `:446-447` and `sweep` `:367-381`; selftest controls `rewritten.sh` and `sourced.sh` |
| R639-7-F1 (local and declare semantics) | Resolved | `declaration`/`declared_value` `:546-605`; 7 fixtures identical, appending refused |
| R639-7-F2 (inline code authorized by interpreter) | **Partly retained as R638-8-N1** | as R638-7-N1 |
| R639-7-F3 (compat-ABI exec) | Resolved | as R638-7-N2 |
| R639-7-F4 (changed copy mistaken for build output) | Fixed for its exact form; **cause retained as R638-8-N2** | the appended copy is refused only outside image directories and under a non-interpreter name |
| R638-7-S1, S2 | Open (optional) | R638-8-S3 |
| R638-7-S3 (`/sbin//initctl`) | Resolved | receipt row `copy of /sbin/initctl` |
| R638-7-S4 (subcommand after options) | Resolved | `subcommand` `:779-784`; selftest `cargo +stable -v install` |
| R639-7-S1 (residue comparison base) | Resolved in wording | REVIEW READY: "The 45 tool records and 303 residue lines are unchanged" |
| R639-7-S2 (PYW2 sentinel) | Resolved | `differential-receipt.json` `R638-6-python-PYW2`: statuses `[0]`, refused by name |

## Clean-lens evidence

```text
[R638] PASS RTL — git diff --stat feef7c9f..1c4d722c (20 files: ci/image/*, docs/testing/CI_IMAGE.md, scripts/ci_*.py; no hdl/, tb/, syn/ RTL or constraint file) — the delta changes CI image tooling only; no clock, reset, CDC, FSM, width or interface contract is touched, and no product RTL or product-test assertion changed.
```

Clean results within the unclean lenses (they are recorded for the next round, and do not bank the lens):

- **Conformance:**
  - items 1, 2 and 5 hold as ruled: `exec_audit.py:86-88`, `:186-279`, `ci_syntax.py:21-48`, with receipts p4 and the differential receipt;
  - the reviewed lists are well formed: 63 text and 18 variant digests reproduce (p3);
  - the receipt is bound: traced at `c2531c634` with only the receipt changed since, sha `9f3ff908…`;
  - the inventory inputs match: 341/341.
- **Tests:** the 41 author controls pass in the image (manifest-verified log). The 211/211 differential outcomes equal their expectations, with 0 mismatches. The round-8 expectation changes (`bash-if-certain` and `bash-or-certain` now refused) follow item 6 and do not weaken a test.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N1, N2, N3, N4) | ruling 6196923564 items 1-8; `exec_audit.py`, `exec_operands.py`, `exec_files.py`, `ci_syntax.py`, `ci_shell_walk.py`, `ci_tool_inventory.py:180-219`, `exec-audit.json`; receipts p1-p6 | R638-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| RTL | CLEAN | delta file list (no RTL); `git diff --stat feef7c9f..1c4d722c` | R638-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Robustness | UNCLEAN (N1, N2, N4) | option parsing (`exec_operands.py`), provenance classes (`exec_audit.py:414-471`), mask regex, walker `realpath`; probes p2, p5, p6 | R638-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Tests | UNCLEAN (N1, N2) | `exec_audit_selftest.py` (41 controls, none Perl or Node inline, none interpreter-named or image-directory provenance); `ci_differential_fixtures.py` ROUND7; `differential-receipt.json` | R638-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Docs | UNCLEAN (N1, N2, N3, N4; RESIDUE R1, R2) | `docs/testing/CI_IMAGE.md:62-96`, `:229-310`, `:358-440`; module docstrings; PR body Round 8; REVIEW READY | R638-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |

## Real limits

- No Docker or act was run, so nothing was re-run in the image. The in-image figures come from the author's published round-8 receipts, verified against the published `MANIFEST.json` digests:
  - the 41 selftest controls, the 26 final checks and `inventory --check` last under CPython 3.12.3;
  - two cold builds, the lock and the archive verification;
  - the 133 smoke records and the 211 differential outcomes.

  The evidence commit `dedfaa3f` is unsigned. No signed round-8 packet manifest was found, so integrity rests on the manifest digests and the committed-receipt digest equality.
- The probes ran on the host kernel (7.2.9) with host tool versions, not in the image. The system-directory arm of N2 uses a writable stand-in system root, not `/usr/local` itself, because no privilege was used. That image steps can write `/usr/local/bin` as root comes from the head's own selftest and the docs-check user (uid 0 in the receipt).
- N4 was established by code reading only: there is no pinned shfmt on the host and no in-image differential run.
- `git fsck --connectivity-only` in the clone printed a commit-graph parse warning for a history object. Tracked bytes were verified separately: index equals the HEAD tree, with modes, blobs and gitlinks.
- No manager source bank exists at this head, and none is claimed or inferred. Hosted contexts were not judged. Physical calibration was NOT RUN, and no hardware was used. A field skip is not hardware proof.

## Pending manager duties

- Carry R638-8-R1 and R638-8-R2 to the residue checklist with their exact fixes.
- Decide the author's open risk 1 (`dash` unpinned). I recommend accepting it once the exemption is bound to the image's `dash` file (N2(a), S2).
- Decide the author's open risks 2-4:
  - 2, masked temporary paths: acceptable, with S1 suggested;
  - 3, checkout watch over the inventory inputs: acceptable;
  - 4, self-test expectation changes: consistent with item 6, not a weakening.
- After the fixes: a re-trace of the reached population in the image with `--network none`, and `inventory --check` last.
- At the merge turn: build and validate the current-dev merge candidate (source base `fa7347fc`, live dev `973e681b`) with the builder and native banks, and link its receipts on the PR.
- Own hosted and act acceptance.

R638-8 FINISHED
