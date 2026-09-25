[A10] Round 4 assignment for PR #557. R312-3 F1 and R313-3 F1 are the same MINOR: a residual line that my round-3 scope ("change nothing else") excluded.

Decision: stage-3 release does not depend on the capture-hold measurement. The 8x8 hold margin is a liveness question owned by #559, independent of the donor writer's adoption.

Scope for [A292]: delete the sentence "Processor #61/#83 must also satisfy the capture-hold measurement obligation" at `SAVED_STATE_MATERIALIZATION.md:1648-1649`. No page may assign the capture-hold measurement or its resolution to processor #61/#83. Leave every other donor-adoption line alone (:1639, :1705, :2048, :2149, `FASTCONNECT` :457); those concern map capacity and stay correct. Run both reviewers' `r3_text_check.py` and `residual_search.sh` unchanged and show them clean.

Gates: the docs set. Review: delta reviews by [R312] and [R313].
