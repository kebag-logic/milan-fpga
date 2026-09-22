https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5778321629
[A10] CURRENT-DEV FULL VALIDATION STARTED

The unpublished author head `fed4f63f33e6185e5c7e4735a27234db99651d24` integrates with live dev `52711029f374650dc93830d5ea28e81cb5c8f410` as candidate `df53dfa116b34816db0193230ad9833e67bf46dd`, tree `fb7bbe66e6326d9d55b4ad13170446dff12a133a`. Intervening paths are disjoint and the complete issue patch is unchanged. Two isolated checkouts now run 46 static/builder commands and five full native groups: parent Verilator, Yosys, PP suites, gPTP suites and behave. The same verified scoped Verilator 5.050 selector is used; the ordinary host tool path and active author/reviewer lanes are unchanged.

The bank includes the changed containment default self-test plus the newly required base AEM-store self-test. After the full bar passes, the unpublished source may fast-forward to this exact tested integration object before its first PR and cleared R243/R244 review. No old receipt is relabeled with the candidate identity. A later dev change still requires current-candidate validation.

Actual gPTP processor PR62 and the adjacent/reverted retained-replay probes remain UNKNOWN/nonzero. No audit waiver, processor adoption or physical evidence is claimed.
