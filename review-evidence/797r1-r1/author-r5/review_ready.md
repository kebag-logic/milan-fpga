[A711e] REVIEW READY
Commit: `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d`. Local branch `797-r1-regref`; the manager pushes.
Changed: R753-4 F1 only. `f24695e4`: the `srp_fresh_r` wording pair now states every case that clears the word (`milan_csr.sv:3108-3133`): "the SRP table's latest answer to the window was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write, with no other master using the table since", with its negation. `docs/reference/REGISTER_MAP.md` is regenerated, and only the four rows in `STRMW_SID_LO`, `STRMW_SID_HI` and `STRMW_SRP` change. It uses "with" rather than the finding's ", and", because a read-table cell is one conjunction split on " and ". `ef7dc985`: the sweep records, by clock edge at the block's ports, the table's answers, the `STRM_SEL`/`STRMW_CTRL` writes and other masters' beats. It reads the clause from that record in the page's words. It adds four SRP states: a poll answered after a write and then the write answered, the same with the write unanswered, a poll then a stolen beat, and a stolen beat then a poll. No RTL change, no other row, no new gate, no dev merge. Suggestions not taken.
Validation, on clean clones of the head, each log and rc in the receipts:
- every `run:` step of `.github/workflows/docs.yml` that can run outside GitHub: 58 steps, 0 not rc 0;
- `gen_register_reference.py --write` leaves the tree clean, then `--check` is rc 0 and fresh; `--selftest` rc 0, 61/61;
- `register_read_sweep.py`: rc 0, 17 tables, 48,007 reads per build, 0 disagreements on shipping and on 2x2;
- the reviewer's probe, rerun with its sequences unchanged: all 25 states agree with the new rows, including the four it marked;
- the old wording planted back: the sweep exits 1 with 288 disagreements (48 shipping, 240 on 2x2): 144 from a poll then a write answer, 144 from a poll then a stolen beat;
- the page or the descriptions planted back to the old wording: `--check` exits 1;
- `git diff --check 1f29f189 HEAD`: rc 0. `git merge-base --all origin/dev HEAD`: one base, `1f29f189`.
Acceptance criteria: R753-4 F1's required outcome and its four verification items are met. The handoff gives each with file:line and a receipt.
Open risks/questions: block level only, because the datapath ties the SRP grant and the steal input to 0. Live dev `503bc97c` is not merged. Residue R753-3 RES2, RES3 and R754-3 R1 is still on the manager's list. Not run: Verilator suites, Yosys, behave suite, hardware, Vivado.
Posted: issuecomment-6575839701
