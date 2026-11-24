[A10] Manager docs commit for R909-4-N1 and R909-4-R1
Head: 1516b2ffe321337858389ec8e42897f8a80644bb (one commit on c413d33a)

- docs/testing/CI_WORKFLOWS.md suite-budget table: rows for input_loopback and input_loopback_dp (300 s each, provisional at their own arm under the new-suite steps in the selector's docstring, from cold local runs, hosted windows owed) and reboot_ctrl (300 s, provisional); the 'every other default suite 1800 s' row stays true.
- docs/testing/TESTING.md:442: R909-4-R1's exact wording.
- No code, test or image input changed. docs_check 0 findings; documentation style OK; no U+2014 in added lines (receipts/).
