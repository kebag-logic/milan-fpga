# A219 receipts: PR #535 correction round 1 (#408, #409)

Head `ef9034578f97ebc2951801d867b7c57f8196423d` (three commits on the reviewed
head `a13b6e2e`, base dev `759da623`). Pinned SDK
`$VALIDATION_STORAGE/504-manager-r1/sdk-install` (`00-sdk-verify.log`, GCC 14.3.0);
Verilator 5.050 from the scoped tool directory (`10-verilator.txt`).

| Receipt | Command | Result |
|---|---|---|
| `00-sdk-verify.log` | `python3 scripts/ci_rv32_sdk.py --destination <sdk> --verify-only` | exit 0 |
| `10-head.txt` | `git rev-parse HEAD; git status --short` before and after the gate runs | clean tree at `ef903457` |
| `11-gate1b-sdk.{log,audit.jsonl}` | `python3 -B sw/builder/test_firmware_compiler.py --sdk-destination <sdk> --audit ...` | exit 0; 255/255 mutations; 29/29 + 4/4 accepted; 55/55 lexer spellings re-measured; 0 NOT RUN |
| `12-gate1b-absent.{log,audit.jsonl}` | `python3 -B sw/builder/test_firmware_compiler.py --absent --audit ...` | exit 0; 198/198; 29/29 + 4/4; 55/55 as recorded; 1 registered NOT RUN (33 census/resolver + 24 retired-rule entries skipped) |
| `30-builder-sdk.{log,audit.jsonl}` | `tools/run_builder.py --mode sdk` (whole `test_builder.py` main, `--require-rv32`) | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: no local Vivado report), 504 s |
| `31-builder-absent.{log,audit.jsonl}` | `tools/run_builder.py --mode absent` | exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's compiler arm, gate 11), 424 s |
| `20-static-gates.log` | `tools/static_gates.sh` (38 commands: docs, em-dash `--base 759da623`, style, TOC, paths, baremetal-only `--check`/`--selftest`, firmware-compiler `--selftest`, hygiene, idiom, ratchets, `git diff --check`) | 38/38 rc=0 |
| `cpp/` | GCC 14.3 `-std=gnu99 -E` over 49 directive spellings (`gcc-directive-spellings*.txt`) and the 55-entry lexer corpus the gate embeds (`corpus-measured.txt`, from `tools/corpus.py`) | the recorded outcomes gate 1b pins |
| `probes/SUMMARY.md` | `tools/probe.py` over `cases/{hostile,accepted}.json` at `759da623` (`--rev`), `a13b6e2e` (`--rev`) and this head, each with the SDK and with no compiler | every case: verdict and answering rule |
| `probes/{base,head}-limits-*.json` | the four pre-existing directive gaps R272-1 listed (`\f#undef`, `\f#pragma`, `\f#include`, `_Pragma` push) | base: accepted without a compiler; head: refused on every machine |

Disconnect matrix (`../disconnect/final/TABLE.md`): each fix this round adds
removed in turn by a count-checked in-memory patch (`../disconnect/patch-*.json`),
over the 43 round-two controls (`../disconnect/labels-round2.txt`), with the SDK
and with no compiler.

Tools (`../tools/`): `probe.py` (in-memory gate 1b grader; never writes into the
lane), `make_cases.py` (the reviewers' published cases, rebuilt verbatim),
`corpus.py`, `summary.py`, `run_builder.py`, `static_gates.sh`.

`../scratch/` was emptied during the session by nothing this lane ran (about
01:24 local); every result cited above is in `receipts/` or `disconnect/`.
