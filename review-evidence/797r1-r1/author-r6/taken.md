[A711f] TAKEN
Branch: `797-r1-regref` (PR #825), from head `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d`. Local commit only; nothing is pushed from this lane.
Authoritative references: R753-5 F1 (issuecomment-6576201147) and R754-5 F1 (issuecomment-6576176288), both NEGATIVE at `ef7dc985`; `hdl/common/csr/milan_csr.sv:3120-3128` (the `srp_fresh_r` clear on a provisioning `STRMW_CTRL` write).
Interpreted scope: add one SRP drive state to `scripts/register_read_sweep.py`: a poll answered, then a provisioning `STRMW_CTRL` write posted and left unanswered, then every swept word read. Reword the docstring (`:17-20`) and the harness comment so they list the orders the modes actually drive. One commit. No page, description, RTL or generator change; if one becomes necessary, STOP.
Validation plan: the sweep on both builds at the new head (rc 0); the m4 mutant (rc 1); m1, m2 and m5 (rc 1); the round 4 wording planted back (rc 1); every `run:` step of `.github/workflows/docs.yml` that can run outside GitHub; `gen_register_reference.py --selftest` and `--check`; `git diff --check 1f29f189 HEAD`; one merge base. On clean clones of the committed head, each log and rc in the receipts.
Blockers: none.
Posted: issuecomment-6576239786
