[A186] TAKEN
Branch: `423-retained-redundant-replay` (PR #519), reviewed head `4671e582cfa4bba4809b9e3a354ce5b6eb967f99`. First step: merge live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` so the corrected head descends from it.
Authoritative references: REQ-VER-04; CONTRIBUTING section 2.1 step 7; [settled G1/H/T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218); [R244-1 report](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5789494311) and its public probes/receipts; R251 F1/F2/F3 and their resolutions.
Interpreted scope:
- R244-A: Git filenames and patch text travel as raw bytes from Git output to Git argv/stdin in the touched-path arm, the patch/postimage helper and T. Any other decoded Git output that does not round-trip through the filesystem codec fails closed instead of being measured as other bytes. Permanent default-selftest controls: an in-process non-injective (Big5) codec control that always runs, plus fresh Big5 and strict UTF-8 processes (installed or disposable locale data; NOT RUN when unavailable).
- R244-D: path diagnostics are rendered from the exact bytes as ASCII, independent of locale; material decision: the pre-existing STRANDED `paths differing:` note quotes names the same way as the new UNKNOWN note. A control drives the CLI through a real strict UTF-8 stdout with several targets.
- R244-B: byte-exact source copies in the mutation harness; full default selftest under an ASCII parent.
- R244-C: controls that assert verdict and exit for rename unfolding, hostile `diff.renames`/`diff.ignoreSubmodules`, the single-merge-base rule (injection whose later measurements succeed), the ancestor type rule and replay distinctness, each with an in-suite guard mutation.
- Docs, docstrings and PR text claim only what is proved.
G1/H/T policy, verdicts, byte-defined fixtures, existing controls, pins and ratchets stay unchanged; #514 owns retention policy.
Validation plan: `check_merge_containment.py --selftest` under UTF-8, strict UTF-8, ASCII, Latin-1 and Big5 parents; the R244-1 Big5, guard, multi-target and mutation probes against the new head; docs, em-dash, TOC, doc-style, Python idiom and hygiene gates. At most 8 jobs. Full native/processor/Yosys/builder banks, act and hosted checks remain with the manager.
Reviewers: R251 (internal) and R244 (external), cleared context. No self-approval.
Blockers: none.
