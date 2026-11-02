[A711f] REVIEW READY
Commit: `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` (parent `ef7dc985`). Local branch `797-r1-regref`; the manager pushes.
Changed: R753-5 F1 / R754-5 F1 only, in one file, `scripts/register_read_sweep.py`. The new SRP state 6 answers a poll, then posts a provisioning `STRMW_CTRL` write and leaves it unanswered, then reads every swept word. The steal states move to 7 and 8, so the state that ends with a poll answer still runs last. The docstring (`:17-26`) and the harness comment (`:350-359`) list the orders the states drive. No page, description, RTL, generator or gate change, and no dev merge.
Why the new state is not last: appended as the last state, it hid m5. m5 is read only in each pass's state 0, after the previous pass's final poll answer and a `STRM_SEL` write. The new state's pending write is answered between passes, which clears the word first, and m5 then gave rc 0. That run was a local commit, amended before publication, and it is kept as a receipt. The comment now states the dependency.
Validation, on clean clones of the head, each log and rc in the receipts:
- the sweep: rc 0, 17 tables, 54,007 reads per build, 0 disagreements on shipping and on 2x2;
- m4 (`:3128` clear removed): rc 1, 144 disagreements, all in the new state (`STRMW_SRP` ship 24 and 2x2 72, `STRMW_SID_LO` and `STRMW_SID_HI` 24 each on 2x2);
- m1: rc 1, 144. m2: rc 1, 288. m5: rc 1, 96. The round 4 wording planted back: rc 1, 288. Each count equals its `ef7dc985` count;
- every `run:` step of `.github/workflows/docs.yml` that can run outside GitHub: 58 steps, 0 not rc 0;
- `gen_register_reference.py --selftest` rc 0, 61/61. `--check` rc 0, fresh. `--write` leaves the tree clean. A stale page planted: `--check` exits 1;
- `git diff --check 1f29f189 HEAD`: rc 0. `git merge-base --all origin/dev HEAD`: one base, `1f29f189`.
Acceptance criteria: F1's required outcome and its four verification items are met. The handoff gives each with file:line, rc and failing words.
Open risks/questions: the `STRM_SEL`-write clear has no dedicated state, only the carried-in state 0 described above. Block level only, because the datapath ties the SRP grant and the steal input to 0. Live dev `503bc97c` is not merged. Residue R753-3 RES2, RES3 and R754-3 R1 stays on the manager's list. Suggestions are not taken. Not run: Verilator suites, Yosys, behave suite, hardware, Vivado.
Posted: issuecomment-6576760481
