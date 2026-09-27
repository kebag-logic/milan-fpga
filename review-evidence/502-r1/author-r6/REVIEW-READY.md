[A354] REVIEW READY

Commit: `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d` (one local commit on `502-pending-live-write`, not pushed).

Changed: the current pending equation in snapshot ownership section 13; full-read consistency corrections in both design pages; case tags for GET_AUDIO_MAP exact-record diagnostics; CSR comment wrap. The full reads cover every section, including dated evidence and proposed D3 behavior. Current reporting includes the direct live-write pulse and its sticky history. The handoff records every section and every whole-tree grep result.

R329-4 F1, S1 and S2 are addressed. Reset/terminal pending summaries follow the existing backend ownership rule; proposed D3 stage retirement includes both live pulse and history. The only HDL edit is a comment wrap. Shadow, datapath and backend are byte-identical to the starting head, and CSR code tokens are unchanged. Harness stimuli, assertions, expected values and check counts are unchanged.

Validation, all rc 0 from `$LANES/502-pending-live-write`, foreground and without pipelines:

```sh
make -C tb/verilator/pp_shadow
make -C tb/verilator/pp_shadow pending-mutant
python3 scripts/docs_check.py
GIT_DIR=/dev/null python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 831f94f4
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
git diff --check
git diff --check 92c6154a HEAD
git grep -n -E "pend_i *=|D2 sticky|D2 bit"
```

Default: 591 + 591 + 591 + 295 checks, zero failures. Mutation target: clean 295/0, historical late-mark mutant detected by 12 required K10/K12 failures. Verilator 5.052; documentation uses the hash-locked Markdown packages. Both documentation inventory modes report zero findings; no-Git mode explicitly skips Git inventory parity. The em-dash gate passes on the committed head with 339/339 controls.

The final grep has six hits: two current equations, two explicitly proposed D3 equations and two backend harness input assignments. No D2-sticky or D2-bit shorthand remains. `HANDOFF.md`, `PR-BODY.md` and compact gate receipts are in the assigned handoff directory; the live PR body is unchanged.

Acceptance criteria: the assigned documentation/comment/diagnostic corrections are complete; the existing K10/K12 checks remain green. Broader gates and hardware were not rerun. Independent re-review and merge validation remain required. No push, PR edit, merge or submodule edit was performed.

Open risks/questions: none for this assignment. D3 materialization remains outside this reporting correction.
