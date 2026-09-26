[A330] REVIEW READY
Commit: `c9484ac8e86cb33d1120471530f9e1762bd4af1f`
Branch: `567-pp-pin-0922e434`; starting head `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`.

Changed: the repository recorder added exactly two rows to `syn/yosys/rom_digests.tsv` for processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d`. No other repository file changed in Round 2. The one-line commit has no body or trailers; the working tree is clean.

Digest comparison with `990f96526bb89356c963a260ebbdcf2a77e6623a`:

| Image | SHA-256 at both pins | Result |
|---|---|---|
| `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | MATCH |
| `ucode.hex` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | MATCH |

All 37 existing rows and the ledger header are unchanged. The processor HDL tree is identical at both pins. The exact-pin key, rather than changed ROM bytes, requires the re-record under the [Round 2 decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786).

Validation: all assigned gates returned 0. Commands ran in the foreground, without gate pipelines.

| Command | Result |
|---|---|
| `cd syn/yosys && ./ooc.sh --record-rom-digests` | rc 0 |
| `cd syn/yosys && ./ooc.sh KL_pp_shadow` | rc 0; normal ledger validation and full wrapper synthesis |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | rc 0; 3/3 tops pass, matching the fast job's command |
| `python3 -B scripts/docs_check.py` in Git mode | rc 0; 0 findings, 23/23 scrub and 4/4 routing controls |
| `python3 -B scripts/docs_check.py` in a metadata-free export of this head | rc 0; 0 findings, 22/22 scrub and 4/4 routing controls; inventory parity explicitly skipped because it requires Git |
| `python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | rc 0; 0 findings, 339/339 controls |
| `git diff --check`; `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD`; pre-commit `git diff --cached --check` | rc 0 each |

Synthesis used local Yosys 0.66 and the verified pinned sv2v v0.0.12 release. The initial em-dash attempt refused with rc 2 for a missing renderer dependency; installing the repository's hash-locked dependencies in an isolated temporary environment produced the recorded rc 0 without changing tracked files.

Acceptance: Round 2 items 1-3 are met: generated rows only, identical previous/new digests, normal OOC and the assigned fast elaboration command pass. `HANDOFF.md` includes the ledger diff, digest comparison and gate table; `PR-BODY.md` is prepared in the assigned output directory.

Open review context: Inherited prose at `CHANGELOG.md:44` and `docs/reference/SUBMODULES.md:53,57` still describes an unchanged ledger and an unresolved acceptance decision. Those statements are superseded by the public Round 2 decision and this commit. They were left untouched because the assignment explicitly requires the ledger-only delta. Independent review must account for this documentation consistency gap; this handoff does not claim full issue completion.

The head remains local. This is an author handoff, not a review verdict or a claim that hosted checks have run.
