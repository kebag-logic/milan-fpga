# Development runs before the round-3 commits

On a copy of the working tree, before the first round-3 commit. The receipts of record are
the head's (`processor/`, `campaigns/`, `area/`). These show how the counts were found before
the commit; the head's SRP campaign log equals `dev-camp-full.log` line for line
(`campaigns/srp-834cc88/srp-vs-round2.txt` compares the head with round 2).

- `dev-camp-new.log`: the five new arms, the seven cut-again patches and two PS20 arms,
  `--only`, `--jobs 8`: 18 of 18.
- `dev-camp-full.*`: the full SRP campaign, `--jobs 8`: 280 of 280, coverage 167 of 167.
- `dev-sfsm-full.log`: `make -C tb/srp_stream_fsms` (the walk arms at four shapes, then the
  suite, 1,512 of 1,512).
- `dev-srptop.log` (recorded in RAW-RECORDS.txt): `make -C tb/srp_top`, 8,671 of 8,671.
- `dev-make-check.log`, `dev-lint5050.log`: `make check` and `scripts/lint_hdl.sh` (pinned
  5.050), rc 0. The copy had no git history, so `make check`'s git-based staleness step
  printed "does not have any commits yet"; the head's `make check` (`processor/`) ran in a
  clean clone.
