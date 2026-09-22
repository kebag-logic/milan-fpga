This file preserves unsuccessful executions and their attribution. Expected negative controls are detector evidence, never passing source gates.

| Owner / original execution | Result | Attribution / disposition | Raw receipt |
|---|---|---|---|
| R254 review_probes.original.py | exit 1, assertion at first-command continuation in yosys-shards step 9 | Probe expected the full checker to accept every shell-equivalent continuation. An unchanged specialized recognizer refuses this on both base and head; comparator-only acceptance is verified separately. | receipts/original-probes.stderr |
| R254 review_probes.second.py | exit 1, RTL_SIBLING_STEP_LISTS assertion | Preservation probe stripped existing physical-leg run records as well as new records. Corrected to remove only fields absent from base. No source defect or edit. | receipts/second-probes.stderr |
| R254 cli_controls.original.py | exit 1, three matching comparison strings | Mutant construction refused an ambiguous source replacement before running any mutant. Corrected to constrain the replacement to check_carrier_script. | receipts/original-cli.stderr |
| R254 cli_controls.second.py | exit 1, empty extracted new-failure list | Receipt parser expected the wrong failure prefix. Raw selftest already named 63 new truncation failures. Corrected parser reads the actual `FAIL mutation not caught: [rtl-script-439 ...]` format and retains record failures too. | receipts/second-cli.stderr; receipts/cli/accept-truncation--selftest.stdout |
| A181 initial remote dev lookup | exit 128 | Missing remote ref; inspection failure, exact supplied base used. | public/evidence/author/original-command-failures.txt |
| A181 path-filtered gh pr diff | exit 1 | Unsupported CLI arguments; inspection failure. | same |
| A181 first documentation patch | patch refused before write | Hunk did not match; corrected exact hunk used. | same |
| A181 template lookup | exit 1 | Case mismatch; inspection failure. | same |
| A181 baseline-sha-controls | exit 1 | Probe detected the two pre-existing unpinned SHA escapes at base; not a passing gate. Independently reproduced by R254 base-drop-block/base-exit-true CLI receipts. | public/evidence/author/commands.jsonl |
| A181 check_py_idiom.py --check | exit 2 | Unsupported argument; corrected invocation omits --check. | public/evidence/author/logs/py-idiom.stderr |
| A181 initial accept-content-drift / accept-missing-record mutation helpers | exit 1 each | Ambiguous replacement assertions (3 / 2 occurrences), before detector execution. These are setup refusals, not kills. | public/evidence/author/logs/mutation-accept-content-drift.stderr; mutation-accept-missing-record.stderr |
| A181 corrected weak-validator controls | exit 1 | Author-attributed detector results; not source passes. R254 ran nine independently selected weak validators. | public/evidence/author/mutation-results.json; commands.jsonl |
| R254 nine weak-validator default selftests | exit 1 each, pristine --check exit 0 | Expected attributable detector failures; all require new content controls. | receipts/cli-results.json and receipts/cli/ |
| R254 malformed pristine carrier controls | --check 1; --selftest 1 with traceback | Reproduces the retained optional R220 diagnostic suggestion. Fails closed. | receipts/malformed-results.json; blank-carrier and nameless-carrier stdout/stderr |
| R254 script-only / record-only maintenance and SHA controls | exit 1 at source | Expected refusals, not passing source gates. | receipts/disk-results.json and named stdout/stderr |

Only the unmodified source check/selftest and focused gates are called passing source gates. No failed setup command is silently replaced with a passing claim.
