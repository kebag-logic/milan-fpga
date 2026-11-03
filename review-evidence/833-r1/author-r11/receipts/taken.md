[A726k] TAKEN

Branch: `833-owned-process`, round 10 head `fce77f0efc1425ef7732a8d70c02addc108f7afe` (PR #834). Commits go on top; nothing is pushed by this lane.
Authoritative references: the round 11 ruling (issuecomment-6595078798); R763-10 (PR #834 issuecomment-6595075381) and R764-10 (issuecomment-6595032567), with their packets; `docs/testing/TESTING.md` row 3.
Interpreted scope:
1. R763-10-F1, pinned rather than narrowed. Two listings go into `owner_stated_seconds`: a first-census parent whose live first-census child outlives its own `SIGKILL`, one beside a cancelled shell that is never resumed and one under it. Their events are R763-10-F1's: `SIGTERM` to parent and child at 0; `SIGKILL` to the child at 2 and to the parent at 4; at 14 `SIGKILL` to the shell, parent and child; then the verdict. `first-census-parent-unspared-beside-shell` joins `MUTANTS` with R763-10's edit byte for byte. It must be red on `owner_stated_seconds` with its words, and it is named in row 3.
2. The RESIDUE items whose text is exact: R763-10-R1, R764-10-R1 and R764-10-R2. R763-10-R1 and R764-10-R2 give different exact texts for the same two lines, so I take one of them and state why. R764-10-S1 is at my judgement, and I will give the reason. Then I re-run both reviewers' round 10 probes and sweeps at the head.
`scripts/owned_process.py` does not change. If a probe shows the product wrong, I stop.
Validation plan: before each commit, the quick gates, the table check and the full `--mutants` campaign. At the head: every `run:` step of `.github/workflows/docs.yml`, `scripts/test_suite_cancellation.py`, the gptp_shadow lifecycle test, the mutation table for every fix, `cd tests && behave`, `git diff --check 1f29f189`, and the preflight cost against round 10. All run with SIGHUP at its default.
Blockers: none.
