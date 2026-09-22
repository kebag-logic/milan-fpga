https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5778608391
[A10] CURRENT-CANDIDATE STATIC / BUILDER VALIDATION COMPLETE

All 46 intended commands now have valid passing evidence at candidate `df53dfa116b34816db0193230ad9833e67bf46dd`, tree `fb7bbe66e6326d9d55b4ad13170446dff12a133a`, over dev `52711029f374650dc93830d5ea28e81cb5c8f410`. The bank used the scoped Verilator 5.050 selector. Final committed blobs/modes/index and all three required pins match.

The original bank completed with aggregate exit1: 45 commands passed and a manager-inherited `git diff --check` endpoint referenced absent author5bbf and exited128. That is preserved unchanged. The separate corrected command uses the exact live-base/candidate endpoints and passes. The [final composed ledger](https://github.com/kebag-logic/milan-fpga/tree/2f82e745f3353250139bbf664e7f945e3b7b1631/review-evidence/423-r1/candidate1/manager-builder-final) selects each original successful receipt and only that actual corrected invocation; it is not a rerun or relabeling of the failed original bank. The original spec/results/raw logs and public correction decision are in the same packet.

The full five-group native run is pending. Builder calibration gate 11 remains NOT RUN and provides no hardware evidence. No review approval or processor-pin adoption is claimed.
