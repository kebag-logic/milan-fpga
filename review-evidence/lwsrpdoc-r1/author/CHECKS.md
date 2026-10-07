# Round 2 checks

- Sentence checker: rc 0; 708 prose units; none exceed 25 words; no prose exemptions.
- Reference checker: rc 0; no detected unlinked references.
- Link checker: rc 1; 269 local link occurrences and 12 unique external URLs.
- Eight relative occurrences await LICENSE and NOTICE, which this lane must not add.
- Three repository URLs pass with authenticated API access. All nine other external URLs return anonymous HTTP 200.
- Graph renderer: rc 0; all 22 render commands return rc 0.
- Both documented configure/build sequences: rc 0.
- Both configured test invocations: rc 0.
- Direct configured suite: rc 0; nine tests and 1690 assertions.
- Isolated codec compile and execution: rc 0; nine tests and 1690 assertions.
- Both scenario runs: rc 0; three scenarios and ten steps pass.
- Scenario dry run: rc 0; all ten steps match; no behavior executed.
- All 16 shell command occurrences were executed in a scratch source snapshot, including duplicates.
- The source snapshot uses the merged source, build, and tests, plus the final documentation files.
- Existing scratch dependency discovery paths were supplied through the environment.
- Routing fixtures verify exact repository boundaries, foreign URLs, comment fragments, unsupported paths, and authentication failures.
- Negative link fixture: rc 1 as expected; two invalid line ranges, one absent file, and one missing heading fail. A valid range passes.
- Whitespace, scope, content, artifact size, and SPDX checks: rc 0.

[Round 2 published command results](ROUND2-PAGE-COMMANDS.md).
[Round 2 command ledger](ROUND2-COMMANDS.md).
[Historical Round 1 command ledger](COMMANDS.md).
[Historical Round 1 published command results](PAGE-COMMANDS.md).

Every command runs in the foreground with a timeout; no check is piped.
Every return code is preserved, including exploratory failures.
The first preview command returned rc 1 because its assumed package path was absent.
The corrected module resolution returned rc 0, and all four preview sheets were inspected.
The initial instruction read preceded knowledge of the command-prefix rule.
The recorder bootstrap completed with rc 0; a separate tool-state serialization attempt failed without affecting files or commands.

