[A615] REVIEW READY

PR: #738. Relates to #737.
Commit: `6f86eee604729b80684526fc5b9be720d94f179a` on `737-ci-image` (local, not pushed).
Round-nine assignment: PR #738 comment 6204018211. Reviews answered: R638-8 (6204009418) and R639-8 (6203890877).

Changed:
- Item 1, text fails closed (R638-8-N1 = R639-8-F1).
  - Every image interpreter reads its program as the interpreter does, under every installed spelling: `bash`, `dash`, Python, Perl, Node and Tcl, including `tclsh8.6` and `perl5.38.2`.
  - Perl bundles switches and adds one line per `-e`. Node's last `-e`, `--eval`, `-p` or `-pe` program wins. `tclsh` reads stdin unless its first word is a script.
  - Inline and streamed text is accepted only as the step's own text or a reviewed entry of that interpreter. Unreadable text is refused.
  - An option a reader does not model is refused by name. So is one that reads code other than the program: Perl `-M`, `-x`; Node `-r`, `-i`; shell `-i`, `--login`; Python `-i`.
  - Each unlisted `perl -e`, `perl -le`, `perl -wE`, `node -e`, `node --eval=…`, `printf … | tclsh` and `| tclsh8.6` control is refused with the digest of the text the interpreter runs. Pinned Perl, Node and Tcl texts stay clean.
- Item 2, provenance on bytes (R638-8-N2; S1 decided as ruled).
  - A program is the image's own only if its path is in the snapshot of the image's directories taken before any job, with an unchanged key.
  - An interpreter is such a file that the image names for its family, or one that holds such a file's bytes. The `dash` exemption belongs to the image's `dash` file.
  - Every other program needs a traced build output's bytes or the reviewed generated list, whatever its name or directory.
  - Refused by name: an appended copy installed as `/usr/local/bin/cp`; an appended copy named `python3` given a checkout script; `bash` copied to a job path named `dash` running `-c`.
  - Build outputs (renamed, installed, `a.out`), LeakSanitizer and the `initctl` stub stay clean.
- Item 3 (R639-8-F2).
  - The load's own errno or reason is answered, with the target kept apart. An exec the audit cannot judge is refused, never left unanswered.
  - A text file without `#!` that the image's `bash` runs in-process is judged as a bash script; `dash`'s re-exec of `/bin/sh` is observed.
  - A missing `#!` interpreter and a binary file run nothing. `#!/proc/self/exe` is refused with its own reason.
- Item 4 (R638-8-N3). The guide, docstring and PR body list the accepted sources per kind as built. A streamed checkout file is refused. The self-test's own entries now live in the self-test; the production `checkout_writes` holds one entry.
- Item 5 (R638-8-N4).
  - `$(realpath <literal>)` yields a path only for the running script's own unlinked path, or an ancestor, before the script runs a command. Elsewhere it is runtime.
  - New fixture `bash-realpath-after-a-program`: an earlier program re-points a link. The real runs differ and the walker refuses.
- Item 6. R1 is the manager's exact comment text. R2 is the reviewer's boundary text, with "the call" in place of one word the bare-metal gate (#259) refuses in tracked files. R638-8-S1 is taken: no `.` or `..` component is masked.

Validation:
- Every reached step was re-traced in the image with `--network none` at `84caae9af`.
  - docs-check 46/46 (root) and rtl-fast 48 (uid 1000): 94 of 98 reached steps traced, every exit status 0, zero findings, 183,831 exec instances; the other 4 are the cache-miss Verilator and Yosys builds the image replaces. All 115 round-six gate commands were observed, 111 with the listed arguments. All 103 inline or streamed and 450 generated reviewed entries are used. Against round eight, 555 rows are relabelled `named` to `image`, and the three `tclsh8.6` program rows become the Tcl scripts and streams they run.
  - Committed as `ci/image/exec-audit-receipt.json` in `6f86eee60`, which changes only the receipt.
- Self-test in the image: 74/74 controls (41 kept, 33 new). Differential fixtures: 213/213 over 178 census shapes. The 45 tool records and 303 residue lines are unchanged.
- Image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059` is unchanged; recipe `53fb5abd`. Two `--no-cache` cold builds took 411,216 and 493,323 ms. `--record-lock` passes on export A and `--check-lock --verify-archive` on export B.
- 26 checks at `6f86eee60` under CPython 3.12.3 return rc 0, with the inventory `--check` last.

Open risks/questions (decision points):
1. Inline and streamed texts are now keyed by their masked digest, as generated programs already were. The builder gates' timing-grade Tcl names a per-run report directory. A text without a temporary path keeps its exact digest, so all 80 earlier entries are unchanged.
2. A checkout path in a program text is masked below the part the checkout held at job start. The OOC Tcl harness sources a mutant it writes under a random `mkstemp` name in `syn/ooc/`. Masked paths now start a word and have no `.` or `..` component. Checked against the round-eight traces, no earlier reviewed digest changes.
3. The readers also refuse start-file and preload options that the controls did not name. None occurs in the reached population.
4. Expectation changes are each stricter: the exact self-test's step-level `realpath` is now refused as runtime; the `bash-realpath` fixture is now non-focus; and the refusal names change from "system program/script" to "image program/script". The idiom gate's module limit moved code into `exec_files.py` and `exec_operands.py`.
5. The receipt names its traced parent `84caae9af`. This is local evidence, not hosted CI and not a review verdict.

A read-only merge with the current dev `734eb780` has no conflict. HANDOFF.md and PR-BODY.md have Round 9 sections: the change map with file:line, the reviewed lists, evidence and decision points. No push, registry login, PR edit, merge, firmware or linked-image change, or product-test assertion change occurred. Independent re-review and the reviewer-owned coverage ledger are required.
