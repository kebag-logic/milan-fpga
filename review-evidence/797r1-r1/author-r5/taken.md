[A711e] TAKEN
Branch: `797-r1-regref` (PR #825), from head `79fdea05ef54e2c99a0aa6efeadaa0f509076e92`. Local commits only; nothing is pushed from this lane.
Authoritative references: R753-4 F1 on PR #825 (issuecomment-6574539469), NEGATIVE at `79fdea05`; `hdl/common/csr/milan_csr.sv:3108-3133` (`srp_fresh_r`); section 2 of issuecomment-6522974767.
Interpreted scope: make the `srp_fresh_r` clause pair state every case that clears the word: a write answer after a later poll answer, a `STRM_SEL` or provisioning `STRMW_CTRL` write, and a beat another master took. Regenerate `docs/reference/REGISTER_MAP.md` through the generator. Extend the read sweep with states that separate the new clause from the weaker reading (a poll answered then a write answered; a stolen beat after a poll answer), its harness comment stating the page's words. One commit for the clause, one for the sweep. No other row, no suggestion, no new gate, no RTL change, no dev merge.
Validation plan: every `run:` step of `.github/workflows/docs.yml` that can run outside GitHub, `gen_register_reference.py --selftest` and `--check`, the extended sweep on both builds, the old wording planted back (must exit 1), `git diff --check 1f29f189 HEAD` and one merge base, on clean clones of the committed head, each log and rc in the receipts.
Blockers: none.
Posted: issuecomment-6575287329
